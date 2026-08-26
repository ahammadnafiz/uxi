#!/usr/bin/env python3
"""Craft lint for CSS. Checks the coherence rung mechanically.

Usage:
  python craft_lint.py styles.css [--scale 4] [--tokens tokens.json]
                                  [--root-font-size 16]

Flags may come before or after the path.

What it checks:
  1. Spacing values off the scale. Every margin, padding, and gap value is
     checked against a base-N scale (default 4). rem and em are converted
     at --root-font-size (default 16px) so a rem-based codebase is really
     checked rather than silently passed. Positioning offsets (top, left)
     are deliberately excluded: a -1px hairline nudge is a legitimate
     optical correction, not scale drift.
  2. Near-miss colors. Pairs of distinct hex colors within a small RGB
     distance. This is a crude proxy, not a perceptual metric, and it
     exists to catch one value that drifted rather than to rank colors.
  3. Off-token colors, when a tokens.json is given: any hex in the CSS
     that is not in the token list. tokens.json format:
     {"colors": ["#1a1a2e", "#ffffff", ...]}
  4. Tiny type: font-size below 12px (or the rem equivalent).
  5. Focus removal: outline none or 0 in a rule with no real replacement.
     `border: none` does not count as a replacement.
  6. Rogue durations: the duration of each transition and animation,
     against a small sane set. Looping animations are exempt.
  7. Type families: more than two distinct primary font families.
  8. Elevation: more than five distinct box-shadow values, against the
     base / raised / overlay / modal / toast ladder.
  9. Radii: more than four distinct border-radius values.
 10. Reduced motion: motion defined with no prefers-reduced-motion block.
 11. Target size: interactive-looking rules sized under 24 CSS px.

Findings here are prompts for judgment, not automatic defects: a value can
be off-scale on purpose. The point is that it should be on purpose.

Exit codes: 0 clean, 1 findings, 2 usage or input error.
"""

from __future__ import annotations

import re
import sys

from _common import CliError, load_json, normalize_hex, parse_hex, read_text, run

SPACING_PROPS = ("margin", "padding", "gap", "row-gap", "column-gap")
SANE_TRANSITION_MS = (100, 120, 150, 200, 250, 300, 400, 500)
MAX_SLOW_MS = 500          # visual-craft.md: past this, motion is waiting
MAX_TYPE_FAMILIES = 2      # SKILL.md rung 4: "two type families at most"
MAX_SHADOWS = 5            # base, raised, overlay, modal, toast
MAX_RADII = 4
MIN_TYPE_PX = 12
MIN_TARGET_PX = 24         # WCAG 2.2 AA, 2.5.8
NEAR_MISS_DISTANCE = 12
GENERIC_FAMILIES = {"inherit", "initial", "unset", "revert", "sans-serif",
                    "serif", "monospace", "cursive", "fantasy", "system-ui",
                    "ui-sans-serif", "ui-serif", "ui-monospace", "-apple-system"}
INTERACTIVE_SELECTOR = re.compile(
    r"button|\.btn|\[role=[\"']?button|\bicon-btn\b|\ba[:.\[]", re.I)
TIME_TOKEN = re.compile(r"(\d*\.?\d+)\s*(ms|s)\b")
LENGTH = re.compile(r"(-?\d*\.?\d+)\s*(px|rem|em)\b")


def rules(css: str) -> list[tuple[str, str]]:
    """Return (selector, body) with comments stripped. Naive but adequate."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [(m.group(1).strip(), m.group(2))
            for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css)]


def declarations(body: str) -> list[tuple[str, str]]:
    """Return (property, value) pairs from a rule body."""
    out = []
    for chunk in body.split(";"):
        prop, sep, value = chunk.partition(":")
        if sep:
            out.append((prop.strip().lower(), value.strip()))
    return out


def to_px(number: float, unit: str, root_px: float) -> float:
    return number * root_px if unit in ("rem", "em") else number


def check_spacing(all_rules: list[tuple[str, str]], base: int,
                  root_px: float) -> list[str]:
    off_scale: dict[str, list[str]] = {}
    for selector, body in all_rules:
        for prop, value in declarations(body):
            if not prop.startswith(SPACING_PROPS):
                continue
            for raw, unit in LENGTH.findall(value):
                px = to_px(float(raw), unit, root_px)
                if px and (px % base or px != int(px)):
                    off_scale.setdefault(f"{raw}{unit}", []).append(
                        selector[:60])
    return [f"spacing off the {base}px scale: {value} in {len(sels)} "
            f"rule(s), e.g. {sels[0]}"
            for value, sels in sorted(off_scale.items())]


def check_colors(css: str, tokens: list[str] | None) -> list[str]:
    findings = []
    seen = set()
    for raw in re.findall(r"#[0-9a-fA-F]{3,8}\b", css):
        try:
            seen.add(normalize_hex(raw))
        except ValueError:
            continue          # not a color, e.g. an id fragment in a url()
    palette = sorted(seen)
    if tokens is not None:
        allowed = set()
        for token in tokens:
            try:
                allowed.add(normalize_hex(token))
            except ValueError as exc:
                raise CliError(f"tokens file: {exc}") from exc
        findings += [f"color not in the token palette: {color}"
                     for color in palette if color not in allowed]
    for i, first in enumerate(palette):
        for second in palette[i + 1:]:
            a, b = parse_hex(first), parse_hex(second)
            distance = sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
            if distance <= NEAR_MISS_DISTANCE:
                findings.append(
                    f"near-miss colors {first} and {second} (RGB distance "
                    f"{distance:.0f}); almost certainly one value that "
                    "drifted.")
    return findings


def check_type(css: str, all_rules: list[tuple[str, str]],
               root_px: float) -> list[str]:
    findings = []
    for _, body in all_rules:
        for prop, value in declarations(body):
            if prop != "font-size":
                continue
            match = LENGTH.search(value)
            if match and to_px(float(match.group(1)), match.group(2),
                               root_px) < MIN_TYPE_PX:
                findings.append(
                    f"font-size {match.group(0)} is below {MIN_TYPE_PX}px; "
                    "hard to read and often an accessibility fail.")
    families = set()
    for _, body in all_rules:
        for prop, value in declarations(body):
            if prop != "font-family":
                continue
            primary = value.split(",")[0].strip().strip("'\"").lower()
            if primary and primary not in GENERIC_FAMILIES:
                families.add(primary)
    if len(families) > MAX_TYPE_FAMILIES:
        findings.append(f"{len(families)} type families "
                        f"({', '.join(sorted(families))}); the coherence "
                        f"rung allows {MAX_TYPE_FAMILIES}.")
    return findings


def check_focus(all_rules: list[tuple[str, str]]) -> list[str]:
    findings = []
    for selector, body in all_rules:
        decls = declarations(body)
        removes = any(prop in ("outline", "outline-style", "outline-width")
                      and value.split()[:1] and value.split()[0].lower()
                      in ("none", "0", "0px") for prop, value in decls)
        if not removes:
            continue
        replaced = any(
            (prop == "box-shadow" and value.lower() != "none")
            or (prop.startswith("border") and value.lower() not in
                ("none", "0", "0px"))
            or (prop in ("outline", "outline-style", "outline-width")
                and value.split()[:1] and value.split()[0].lower()
                not in ("none", "0", "0px"))
            for prop, value in decls)
        if not replaced:
            findings.append("focus indicator removed with no replacement "
                            f"in rule: {selector[:60]}")
    return findings


def check_motion(css: str, all_rules: list[tuple[str, str]]) -> list[str]:
    findings = []
    has_motion = False
    sane = ", ".join(str(ms) for ms in SANE_TRANSITION_MS)
    for _, body in all_rules:
        for prop, value in declarations(body):
            root = prop.split("-")[0]
            if root not in ("transition", "animation"):
                continue
            if prop in ("transition-property", "animation-name",
                        "transition-timing-function",
                        "animation-timing-function", "transition-delay",
                        "animation-delay"):
                continue
            has_motion = True
            for segment in value.split(","):
                match = TIME_TOKEN.search(segment)
                if not match:
                    continue
                # The first time in a shorthand segment is the duration;
                # a second one would be the delay, which may sit anywhere.
                ms = float(match.group(1)) * (1000 if match.group(2) == "s"
                                              else 1)
                looping = "infinite" in value.lower()
                if root == "animation" and looping:
                    continue
                if root == "animation":
                    if ms > MAX_SLOW_MS:
                        findings.append(
                            f"animation runs {ms:.0f}ms; past {MAX_SLOW_MS}ms "
                            "people are waiting on you, not being oriented.")
                elif ms not in SANE_TRANSITION_MS:
                    findings.append(
                        f"transition duration {ms:.0f}ms is off the common "
                        f"set ({sane}); timing is a token, keep one value "
                        "per class of motion.")
    if has_motion and "prefers-reduced-motion" not in css:
        findings.append("motion is defined but no prefers-reduced-motion "
                        "block exists; the setting has to be honored.")
    return findings


def check_elevation(all_rules: list[tuple[str, str]]) -> list[str]:
    findings = []
    shadows = set()
    radii = set()
    for _, body in all_rules:
        for prop, value in declarations(body):
            flat = " ".join(value.split()).lower()
            if prop == "box-shadow" and flat not in ("none", ""):
                shadows.add(flat)
            if prop.startswith("border") and prop.endswith("radius") and flat:
                radii.add(flat)
    if len(shadows) > MAX_SHADOWS:
        findings.append(f"{len(shadows)} distinct box-shadow values; the "
                        "ladder is base, raised, overlay, modal, toast, so "
                        f"{MAX_SHADOWS} is the ceiling.")
    if len(radii) > MAX_RADII:
        findings.append(f"{len(radii)} distinct border-radius values "
                        f"({', '.join(sorted(radii)[:6])}...); radii belong "
                        "on a scale like everything else.")
    return findings


def check_target_size(all_rules: list[tuple[str, str]],
                      root_px: float) -> list[str]:
    findings = []
    for selector, body in all_rules:
        if not INTERACTIVE_SELECTOR.search(selector):
            continue
        for prop, value in declarations(body):
            if prop not in ("width", "height", "min-width", "min-height"):
                continue
            match = LENGTH.fullmatch(value.strip())
            if match and to_px(float(match.group(1)), match.group(2),
                               root_px) < MIN_TARGET_PX:
                findings.append(
                    f"{selector[:40]} sets {prop}: {value}, under the "
                    f"{MIN_TARGET_PX}px minimum target size. Pad it out "
                    "even when the glyph itself is small.")
    return findings


def check(path: str, base: int = 4, tokens: list[str] | None = None,
          root_px: float = 16.0) -> int:
    css = read_text(path)
    all_rules = rules(css)
    findings = (check_spacing(all_rules, base, root_px)
                + check_colors(css, tokens)
                + check_type(css, all_rules, root_px)
                + check_focus(all_rules)
                + check_motion(css, all_rules)
                + check_elevation(all_rules)
                + check_target_size(all_rules, root_px))
    print(f"\n{path}: {len(findings)} finding(s)")
    for finding in findings:
        print(f"  - {finding}")
    if not findings:
        print("  clean. Values sit on the scale, palette is tight, focus "
              "survives, motion is consistent.")
    return len(findings)


def _flag_value(argv: list[str], flag: str) -> str | None:
    if flag not in argv:
        return None
    index = argv.index(flag)
    if index + 1 >= len(argv):
        raise CliError(f"{flag} needs a value")
    return argv[index + 1]


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        raise CliError(__doc__ or "")

    flags = {"--scale", "--tokens", "--root-font-size"}
    scale = _flag_value(argv, "--scale")
    tokens_path = _flag_value(argv, "--tokens")
    root = _flag_value(argv, "--root-font-size")

    skip: set[int] = set()
    for i, arg in enumerate(argv):
        if arg in flags:
            skip.update({i, i + 1})
    paths = [arg for i, arg in enumerate(argv) if i not in skip]
    if len(paths) != 1:
        raise CliError("expected exactly one CSS file path, got "
                       f"{len(paths)}")

    try:
        base = int(scale) if scale else 4
        root_px = float(root) if root else 16.0
    except ValueError as exc:
        raise CliError(f"--scale and --root-font-size take numbers: "
                       f"{exc}") from exc
    if base <= 0 or root_px <= 0:
        raise CliError("--scale and --root-font-size must be positive")

    tokens = None
    if tokens_path:
        doc = load_json(tokens_path)
        if not isinstance(doc, dict) or not isinstance(doc.get("colors"),
                                                       list):
            raise CliError(f'{tokens_path} must look like '
                           '{"colors": ["#ffffff", ...]}')
        tokens = doc["colors"]

    return 1 if check(paths[0], base, tokens, root_px) else 0


if __name__ == "__main__":
    run(main)
