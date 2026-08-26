#!/usr/bin/env python3
"""Research statistics that UX work actually needs. Stdlib only.

Three subcommands:

  python research_stats.py sus responses.csv
      Scores the System Usability Scale. CSV: one row per participant,
      ten columns q1..q10 with values 1-5. A header row is optional and
      is detected, not assumed. Extra leading columns (a participant id,
      a timestamp) are tolerated: the ten question columns are located
      and the choice is printed, never guessed at silently. Odd items
      are positive, even items negative, standard scoring: sum of
      (odd-1) and (5-even), times 2.5, giving 0-100 per participant.
      Every skipped row is reported with its reason.

  python research_stats.py completion 14 20
      Task completion: successes and attempts. Prints the rate with a
      95 percent Wilson score interval, which behaves properly at the
      small sample sizes usability studies actually have (a plain
      proportion plus normal error bars does not).

  python research_stats.py times 34,41,29,88,37,45
      Time on task, seconds, comma separated. Reports median and
      geometric mean (task times are right skewed, so the arithmetic
      mean overstates the typical experience), plus min and max.

The larger point these encode: report qualitative counts as counts
("14 of 20"), attach honest uncertainty to small-sample rates, and never
summarize skewed times with a plain average.

Exit codes: 0 success, 1 no usable data, 2 usage or input error.
"""

from __future__ import annotations

import csv
import math
import sys

from _common import CliError, run

QUESTIONS = 10
SUS_MIN, SUS_MAX = 1, 5


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float,
                                                             float]:
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return p, max(0.0, center - half), min(1.0, center + half)


def _score_row(cells: list[str], offset: int) -> list[int]:
    """Parse ten answers starting at offset. Raises ValueError if unusable.

    Cells are read by position. They are deliberately not compacted first:
    dropping the blanks used to shift every later answer one column left
    and score the participant anyway, silently, on the wrong questions.
    """
    window = cells[offset:offset + QUESTIONS]
    if len(window) < QUESTIONS:
        raise ValueError(f"only {len(window)} of {QUESTIONS} columns present")
    values = []
    for i, cell in enumerate(window):
        text = cell.strip()
        if not text:
            raise ValueError(f"q{i + 1} is blank")
        try:
            value = int(float(text))
        except ValueError as exc:
            raise ValueError(f"q{i + 1} is {text!r}, not a number") from exc
        if not SUS_MIN <= value <= SUS_MAX:
            raise ValueError(f"q{i + 1} is {value}, outside {SUS_MIN}-"
                             f"{SUS_MAX}")
        values.append(value)
    return values


def _read_rows(path: str) -> list[list[str]]:
    try:
        with open(path, newline="", encoding="utf-8") as handle:
            return [row for row in csv.reader(handle) if any(
                c.strip() for c in row)]
    except OSError as exc:
        raise CliError(f"cannot read {path}: {exc.strerror}") from exc


def sus(path: str) -> int:
    rows = _read_rows(path)
    if not rows:
        raise CliError(f"{path} is empty")

    widths = {len(row) for row in rows}
    width = max(widths)
    offset = width - QUESTIONS
    if offset < 0:
        raise CliError(f"{path} has {width} columns; SUS needs {QUESTIONS} "
                       "(q1..q10, plus any leading id columns)")
    if offset:
        print(f"note: rows have {width} columns, so columns "
              f"{offset + 1}-{width} are being read as q1..q10. Check that "
              "is right before trusting the numbers.")

    scores = []
    skipped = []
    for number, row in enumerate(rows, start=1):
        try:
            values = _score_row(row, offset)
        except ValueError as exc:
            skipped.append((number, str(exc)))
            continue
        odd = sum(values[i] - 1 for i in (0, 2, 4, 6, 8))
        even = sum(SUS_MAX - values[i] for i in (1, 3, 5, 7, 9))
        scores.append((odd + even) * 2.5)

    if skipped:
        first_is_header = skipped and skipped[0][0] == 1
        print(f"skipped {len(skipped)} row(s):")
        for number, reason in skipped:
            label = " (looks like the header row)" if (
                first_is_header and number == 1) else ""
            print(f"  row {number}: {reason}{label}")

    if not scores:
        print(f"no usable rows in {path}. Expect {QUESTIONS} columns of "
              f"{SUS_MIN}-{SUS_MAX} per participant.")
        return 1

    n = len(scores)
    mean = sum(scores) / n
    sd = ((sum((s - mean) ** 2 for s in scores) / (n - 1)) ** 0.5
          if n > 1 else 0.0)
    print(f"SUS over {n} participants: mean {mean:.1f}, sd {sd:.1f}, "
          f"min {min(scores):.1f}, max {max(scores):.1f}")
    if mean >= 80.3:
        band = "A: top decile territory, people are likely to recommend it"
    elif mean >= 68:
        band = "B/C: above the benchmark average of about 68"
    elif mean >= 51:
        band = "D: below average, real problems to find and fix"
    else:
        band = "F: among the worst scores recorded, expect abandonment"
    print(f"interpretation: {band}")
    print("Remember SUS measures perceived usability. Pair it with task "
          "success; the aesthetic-usability effect inflates it for "
          "attractive products.")
    return 0


def completion(successes: str, attempts: str) -> int:
    try:
        s, n = int(successes), int(attempts)
    except ValueError as exc:
        raise CliError(f"successes and attempts must be whole numbers: "
                       f"{exc}") from exc
    if s < 0 or n <= 0:
        raise CliError("attempts must be positive and successes cannot be "
                       "negative")
    if s > n:
        raise CliError(f"successes ({s}) cannot exceed attempts ({n})")

    p, lo, hi = wilson(s, n)
    print(f"completion: {s} of {n} = {p:.0%}")
    print(f"95% Wilson interval: {lo:.0%} to {hi:.0%}")
    if n < 20:
        print(f"With n={n} the honest claim is the count itself. Say "
              f"'{s} of {n} completed', and use the interval to show how "
              "wide the truth could be, not to fake precision.")
    return 0


def times(csv_values: str) -> int:
    values = []
    for chunk in csv_values.split(","):
        text = chunk.strip()
        if not text:
            continue
        try:
            values.append(float(text))
        except ValueError as exc:
            raise CliError(f"{text!r} is not a number") from exc
    if not values:
        raise CliError("no values given")
    if any(v < 0 for v in values):
        raise CliError("task times cannot be negative")

    values.sort()
    n = len(values)
    median = (values[n // 2] if n % 2
              else (values[n // 2 - 1] + values[n // 2]) / 2)
    geo = (math.exp(sum(math.log(v) for v in values) / n)
           if all(v > 0 for v in values) else float("nan"))
    mean = sum(values) / n
    print(f"time on task, n={n}: median {median:.1f}s, geometric mean "
          f"{geo:.1f}s, arithmetic mean {mean:.1f}s, range {values[0]:.0f}"
          f"-{values[-1]:.0f}s")
    if geo == geo and mean > geo * 1.15:   # geo == geo screens out NaN
        print("The arithmetic mean sits well above the geometric mean, "
              "which means a long tail is dragging it. Report median or "
              "geometric mean as the typical experience.")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    usage = ("usage: research_stats.py sus FILE.csv | "
             "completion SUCCESSES ATTEMPTS | times 34,41,29")
    if not argv or argv[0] in ("-h", "--help"):
        raise CliError(usage)

    command, rest = argv[0], argv[1:]
    if command == "sus" and len(rest) == 1:
        return sus(rest[0])
    if command == "completion" and len(rest) == 2:
        return completion(*rest)
    if command == "times" and len(rest) == 1:
        return times(rest[0])
    raise CliError(usage)


if __name__ == "__main__":
    run(main)
