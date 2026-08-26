#!/usr/bin/env python3
"""WCAG 2.2 contrast checker. Stdlib only, no dependencies.

Usage:
  python contrast_check.py "#1a1a2e" "#ffffff"
      One pair: prints the ratio and pass/fail for every WCAG threshold.

  python contrast_check.py --pairs pairs.json
      pairs.json is a list of objects:
      [{"name": "body on surface", "fg": "#333333", "bg": "#f5f5f5",
        "use": "text"}]
      "use" is one of: text, large-text, ui. Defaults to text.

  python contrast_check.py --scan styles.css
      Pulls every hex color out of a CSS file and reports the ratio for
      every foreground candidate against the most common colors. Noisy by
      design; a starting point, not a verdict.

Thresholds live in one place (THRESHOLDS) and every verdict is derived
from it, so changing a number changes every message that quotes it.

Alpha is dropped from 4- and 8-digit hex, and flagged when it is not
opaque: a translucent foreground composites against whatever is behind
it, so its real contrast is lower than its hex implies.

Exit codes: 0 everything passes AA for its declared use, 1 something
fails, 2 usage or input error. So it can gate a CI step.
"""

from __future__ import annotations

import re
import sys

from _common import (CliError, alpha_of, contrast_ratio, load_json,
                     normalize_hex, read_text, run)

THRESHOLDS: dict[str, tuple[float, float | None]] = {
    # use: (AA, AAA)
    "text": (4.5, 7.0),        # under 24px regular / 18.66px bold
    "large-text": (3.0, 4.5),  # 24px+ regular or 18.66px+ bold
    "ui": (3.0, None),         # component boundaries, icons, focus rings
}
TEXT_AA = THRESHOLDS["text"][0]
UI_AA = THRESHOLDS["ui"][0]


def _verdict(ratio: float, threshold: float | None) -> str:
    if threshold is None:
        return ""
    return "pass" if ratio >= threshold else "fail"


def _warn_alpha(*colors: str) -> None:
    for color in colors:
        alpha = alpha_of(color)
        if alpha is not None and alpha < 255:
            print(f"  note: {color} is {alpha / 255:.0%} opaque. Alpha is "
                  "dropped here; the real ratio against what shows through "
                  "is lower than this.")


def report_pair(name: str, fg: str, bg: str, use: str) -> bool:
    if use not in THRESHOLDS:
        raise CliError(f"unknown use {use!r} for {name!r}; "
                       f"expected one of {', '.join(THRESHOLDS)}")
    aa, aaa = THRESHOLDS[use]
    ratio = contrast_ratio(fg, bg)
    passes = ratio >= aa
    tail = ""
    if aaa is not None:
        tail = f"  AAA({aaa}:1) {_verdict(ratio, aaa)}"
    print(f"{name}: {fg} on {bg}  ratio {ratio:.2f}:1  "
          f"AA({use}, {aa}:1) {'pass' if passes else 'FAIL'}{tail}")
    _warn_alpha(fg, bg)
    return passes


def check_pairs(path: str) -> bool:
    pairs = load_json(path)
    if not isinstance(pairs, list) or not pairs:
        raise CliError(f"{path} must be a non-empty JSON list of "
                       "{{name, fg, bg, use}} objects")
    results = []
    for i, pair in enumerate(pairs):
        if not isinstance(pair, dict) or "fg" not in pair or "bg" not in pair:
            raise CliError(f"pair {i + 1} in {path} needs both 'fg' and 'bg'")
        results.append(report_pair(pair.get("name", f"pair {i + 1}"),
                                   pair["fg"], pair["bg"],
                                   pair.get("use", "text")))
    return all(results)


def scan_css(path: str) -> bool:
    text = read_text(path)
    counts: dict[str, int] = {}
    for raw in re.findall(r"#[0-9a-fA-F]{3,8}\b", text):
        try:
            color = normalize_hex(raw)
        except ValueError:
            continue
        counts[color] = counts.get(color, 0) + 1
    colors = sorted(counts, key=lambda c: counts[c], reverse=True)
    if len(colors) < 2:
        print(f"{path}: fewer than two distinct colors found, nothing to "
              "compare. This is not a pass, it is a no-op.")
        return True
    print(f"{len(colors)} distinct colors in {path}. Pairs below "
          f"{TEXT_AA}:1 against the two most common colors "
          "(likely backgrounds):")
    ok = True
    for bg in colors[:2]:
        for fg in colors:
            if fg == bg:
                continue
            ratio = contrast_ratio(fg, bg)
            if ratio < TEXT_AA:
                ok = False
                large_ui = "passes" if ratio >= UI_AA else "fails"
                print(f"  {fg} on {bg}: {ratio:.2f}:1  "
                      f"(fails text AA; {large_ui} ui/large AA)")
    if ok:
        print(f"  none. Every combination clears {TEXT_AA}:1.")
    return ok


def report_single(fg: str, bg: str) -> bool:
    passes = report_pair("pair", fg, bg, "text")
    ratio = contrast_ratio(fg, bg)
    for use in ("large-text", "ui"):
        aa, aaa = THRESHOLDS[use]
        tail = f", AAA {_verdict(ratio, aaa)}" if aaa is not None else ""
        print(f"  as {use}: AA {_verdict(ratio, aa)}{tail}")
    return passes


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        raise CliError(__doc__ or "")
    if argv[0] in ("--pairs", "--scan"):
        if len(argv) != 2:
            raise CliError(f"{argv[0]} takes exactly one file path")
        if argv[0] == "--pairs":
            return 0 if check_pairs(argv[1]) else 1
        return 0 if scan_css(argv[1]) else 1
    if len(argv) == 2:
        try:
            return 0 if report_single(argv[0], argv[1]) else 1
        except ValueError as exc:
            raise CliError(str(exc)) from exc
    raise CliError("expected two hex colors, --pairs FILE, or --scan FILE")


if __name__ == "__main__":
    run(main)
