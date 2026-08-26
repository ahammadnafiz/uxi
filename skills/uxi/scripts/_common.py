#!/usr/bin/env python3
"""Shared helpers for the uxi scripts. Stdlib only, no dependencies.

Not a tool itself. It exists because colour parsing used to be copied
into two scripts and the copies drifted: one validated its input and one
crashed on any hex that was not 3, 6, or 8 digits.

Exit code contract, shared by every script here:
  0  clean / pass
  1  findings / fail  (the thing being checked has problems)
  2  usage or input error  (the tool could not run at all)
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, NamedTuple

HEX_DIGITS = "0123456789abcdefABCDEF"


class CliError(Exception):
    """A usage or input problem. Reported cleanly, exits 2, no traceback."""


class Rgb(NamedTuple):
    r: int
    g: int
    b: int


def parse_hex(value: str) -> Rgb:
    """Parse #rgb, #rgba, #rrggbb, or #rrggbbaa into an Rgb triple.

    Alpha is dropped; see alpha_of() to check whether any was present,
    because a translucent foreground does not have the contrast its
    opaque hex implies.
    """
    v = value.strip().lstrip("#")
    if len(v) in (3, 4):
        v = "".join(c * 2 for c in v)
    if len(v) == 8:
        v = v[:6]
    if len(v) != 6 or any(c not in HEX_DIGITS for c in v):
        raise ValueError(f"not a hex color: {value!r}")
    return Rgb(*(int(v[i:i + 2], 16) for i in (0, 2, 4)))


def alpha_of(value: str) -> int | None:
    """Return the 0-255 alpha of a #rgba/#rrggbbaa value, else None."""
    v = value.strip().lstrip("#")
    if len(v) == 4 and all(c in HEX_DIGITS for c in v):
        return int(v[3] * 2, 16)
    if len(v) == 8 and all(c in HEX_DIGITS for c in v):
        return int(v[6:8], 16)
    return None


def normalize_hex(value: str) -> str:
    """Canonical lowercase #rrggbb, so equal colors compare equal."""
    return "#%02x%02x%02x" % parse_hex(value)


def relative_luminance(rgb: Rgb) -> float:
    """WCAG 2.x relative luminance."""
    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    """WCAG 2.x contrast ratio between two hex colors, 1.0 to 21.0."""
    l1 = relative_luminance(parse_hex(fg))
    l2 = relative_luminance(parse_hex(bg))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def read_text(path: str) -> str:
    """Read a file, or raise CliError instead of a traceback."""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError as exc:
        raise CliError(f"cannot read {path}: {exc.strerror}") from exc


def load_json(path: str) -> Any:
    """Load JSON, or raise CliError instead of a traceback."""
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise CliError(f"cannot read {path}: {exc.strerror}") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"{path} is not valid JSON: {exc}") from exc


def run(main: Callable[[], int]) -> None:
    """Entry point wrapper: clean errors, honest exit codes, no traceback."""
    try:
        sys.exit(main())
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        # piped into head/less and the reader closed early; not our problem
        sys.exit(0)
