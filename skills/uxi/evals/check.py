#!/usr/bin/env python3
"""Check the mechanical half of evals.json. Stdlib only.

Usage: python evals/check.py

Runs every `deterministic` block (a command, an expected exit code, and
substrings its output must contain) and confirms every `fixtures` path
resolves. It does not grade the `must` and `must_not` assertions; those
need a judge.

This exists so the numbers in assets/fixtures/ANSWERS.md cannot drift
away from what the scripts actually print. When a script changes, this
tells you which expectations went stale.

Exit codes: 0 all checks pass, 1 something failed, 2 could not run.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_command(block: dict) -> list[str]:
    """Return the problems with one deterministic block, empty if fine."""
    result = subprocess.run(shlex.split(block["command"]), cwd=ROOT,
                            capture_output=True, text=True)
    output = result.stdout + result.stderr
    problems = []
    if result.returncode != block["expect_exit"]:
        problems.append(f"exited {result.returncode}, expected "
                        f"{block['expect_exit']}")
    problems += [f"output is missing {sub!r}"
                 for sub in block["expect_substrings"] if sub not in output]
    return problems


def main() -> int:
    path = ROOT / "evals" / "evals.json"
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"error: cannot read {path}: {exc.strerror}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}", file=sys.stderr)
        return 2

    checked = 0
    failed = 0

    for eval_case in doc.get("evals", []):
        label = f"eval {eval_case.get('id')} {eval_case.get('name')}"

        for fixture in eval_case.get("fixtures", []):
            checked += 1
            if not (ROOT / fixture).exists():
                failed += 1
                print(f"[FAIL] {label}: fixture {fixture} does not exist")

        for block in eval_case.get("deterministic", []):
            checked += 1
            problems = check_command(block)
            if problems:
                failed += 1
                print(f"[FAIL] {label}: {block['command']}")
                for problem in problems:
                    print(f"       {problem}")

    print(f"\n{checked} checks, {failed} failed")
    if failed:
        print("An expectation drifted from what the scripts print. Re-run "
              "the commands, fix the code or the expectation, and update "
              "assets/fixtures/ANSWERS.md in the same commit.")
        return 1
    judged = sum(1 for e in doc.get("evals", [])
                 if not e.get("deterministic"))
    print(f"The mechanical half holds. {judged} of {len(doc.get('evals', []))}"
          " evals still need a judge for their must and must_not lists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
