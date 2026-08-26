#!/usr/bin/env python3
"""Validate audit findings and render the report. The validation loop.

The workflow this enables:
  1. Draft findings as JSON while auditing (structure below).
  2. Run: python audit_report.py validate findings.json
     Fix every complaint. The validator enforces the discipline the
     skill asks for: evidence on every finding, a fix on every blocker
     and serious, rungs declared, surface class declared, something in
     "working well", and no severity inflation via a wall of minors.
  3. Run: python audit_report.py render findings.json > report.md
     Renders the markdown report in the deliverables.md structure:
     the lowest failing rung and the headline recommendation on top,
     then findings grouped by severity, ordered by rung within each
     group, since that is the order a product team triages in.

Findings JSON structure:
{
  "scope": "checkout flow, mobile Safari, guest path, 2026-08-26",
  "surface_class": "transaction",
  "method": "heuristic review",
  "headline_fix": "Show total cost including shipping from step 1",
  "working_well": ["Cart persists across sessions", "..."],
  "could_not_assess": ["Screen reader pass; no device available"],
  "findings": [
    {
      "title": "Shipping cost appears only at the final step",
      "rung": 5,                # 1 access, 2 orientation, 3 task,
                                # 4 coherence, 5 honesty
      "severity": "blocker",    # blocker | serious | minor | note
      "where": "checkout step 4, order summary",
      "evidence": "3 of 5 observed sessions abandoned at step 4 ...",
      "impact": "abandonment plus a hidden-costs pattern exposure",
      "fix": "estimate shipping from postcode on step 1",
      "effort": "medium"
    }
  ]
}

Exit codes: 0 valid, 1 invalid or unrenderable, 2 usage or input error,
so the loop is scriptable.
"""

from __future__ import annotations

import sys
from typing import Any

from _common import CliError, load_json, run

RUNGS = {1: "Access", 2: "Orientation", 3: "Task completion",
         4: "Coherence", 5: "Arrangement and honesty"}
# One ordered structure: severity, its heading, and its rank. Two parallel
# lists used to drift apart whenever a severity was added or renamed.
SEVERITY_HEADINGS = (("blocker", "Blockers"), ("serious", "Serious"),
                     ("minor", "Minor"), ("note", "Notes"))
SEVERITIES = tuple(name for name, _ in SEVERITY_HEADINGS)
REAL = ("blocker", "serious")
CLASSES = ("acquisition", "transaction", "application", "content", "system")

MIN_EVIDENCE_CHARS = 20   # shorter than this is a label, not evidence
MINOR_RATIO = 3           # minors per real finding before it reads as padding
MINOR_FLOOR = 8           # minors tolerated when there are no real findings


def validate(doc: Any) -> list[str]:
    if not isinstance(doc, dict):
        return ["top level must be a JSON object, see the docstring"]

    problems: list[str] = []

    def need(key: str, why: str) -> None:
        if not doc.get(key):
            problems.append(f"missing '{key}': {why}")

    need("scope", "say what was reviewed, where, and when, or nobody can "
         "reproduce or bound the audit")
    need("surface_class", "the class picks the rule set; without it the "
         "verdicts are not defensible")
    surface = doc.get("surface_class")
    if isinstance(surface, str) and surface.lower() not in CLASSES:
        problems.append(f"surface_class must be one of {CLASSES}")
    need("headline_fix", "lead with the single highest-leverage change; a "
         "report without one is a list, not a recommendation")
    if not doc.get("working_well"):
        problems.append("empty 'working_well': teams need to know what not "
                        "to break, and an all-negative report reads as an "
                        "attack rather than an audit")

    findings = doc.get("findings", [])
    if not isinstance(findings, list):
        return problems + ["'findings' must be a list"]
    if not findings:
        problems.append("no findings at all; if the surface is genuinely "
                        "clean, record that as a note-level finding with "
                        "the evidence that supports it")

    for i, finding in enumerate(findings):
        tag = f"finding {i + 1}"
        if not isinstance(finding, dict):
            problems.append(f"{tag}: must be an object")
            continue
        tag = f"{tag} ({finding.get('title', 'untitled')!r})"
        if finding.get("rung") not in RUNGS:
            problems.append(f"{tag}: rung must be 1-5")
        if finding.get("severity") not in SEVERITIES:
            problems.append(f"{tag}: severity must be one of {SEVERITIES}")
        for key in ("title", "where", "evidence"):
            if not finding.get(key):
                problems.append(f"{tag}: missing '{key}'; a finding without "
                                "evidence and a location is an opinion")
        if finding.get("severity") in REAL and not finding.get("fix"):
            problems.append(f"{tag}: {finding.get('severity')} findings must "
                            "carry a concrete fix, not just a complaint")
        evidence = finding.get("evidence") or ""
        if isinstance(evidence, str) and 0 < len(evidence) \
                < MIN_EVIDENCE_CHARS:
            problems.append(f"{tag}: evidence is thin ({len(evidence)} "
                            f"chars, want {MIN_EVIDENCE_CHARS}+); say what "
                            "was observed or which heuristic applies and why")

    counts = {s: 0 for s in SEVERITIES}
    for finding in findings:
        if isinstance(finding, dict) and finding.get("severity") in counts:
            counts[finding["severity"]] += 1
    real = counts["blocker"] + counts["serious"]
    # With real findings present, minors are padding once they swamp them.
    # With none present, a short list of minors is just a clean surface
    # honestly reported, so only an absurd pile counts as padding.
    limit = MINOR_RATIO * real if real else MINOR_FLOOR
    if counts["minor"] > limit:
        problems.append(f"{counts['minor']} minors against {real} blocker or "
                        f"serious finding(s), over the limit of {limit}. "
                        "Padding with minors trains readers to ignore the "
                        "report; cut or group them.")
    return problems


def lowest_failing_rung(findings: list[dict[str, Any]]) -> int | None:
    blocking = [f["rung"] for f in findings
                if isinstance(f, dict) and f.get("severity") in REAL
                and f.get("rung") in RUNGS]
    return min(blocking) if blocking else None


def render(doc: dict[str, Any]) -> str:
    findings = doc.get("findings", [])
    low = lowest_failing_rung(findings)
    out = [f"# UX audit: {doc.get('scope', '')}", "",
           f"**Surface class:** {str(doc.get('surface_class', '')).title()}  ",
           f"**Method:** {doc.get('method', 'heuristic review')}", "",
           "## The short version"]
    if low:
        out.append(f"The lowest failing rung is **{low}. {RUNGS[low]}**. "
                   "Fixes above this rung will underperform until it holds.")
    else:
        out.append("No blocker or serious findings. The rungs hold.")
    out.append(f"The single change with the most leverage: "
               f"{doc.get('headline_fix', '')}")
    out.append("")

    for severity, heading in SEVERITY_HEADINGS:
        group = sorted((f for f in findings if f.get("severity") == severity),
                       key=lambda f: f.get("rung", 9))
        if not group:
            continue
        out.append(f"## {heading}")
        for finding in group:
            rung = finding.get("rung")
            out.append(f"### {finding.get('title', '')}")
            out.append(f"**Rung:** {rung} ({RUNGS.get(rung, '?')})  ")
            out.append(f"**Where:** {finding.get('where', '')}  ")
            out.append(f"**Evidence:** {finding.get('evidence', '')}  ")
            for key, label in (("impact", "Impact"), ("fix", "Fix"),
                               ("effort", "Effort")):
                if finding.get(key):
                    out.append(f"**{label}:** {finding[key]}  ")
            out.append("")

    for key, heading in (("working_well", "What is working"),
                         ("could_not_assess",
                          "What this audit could not assess")):
        if doc.get(key):
            out.append(f"## {heading}")
            out += [f"- {item}" for item in doc[key]]
            out.append("")
    return "\n".join(out)


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) != 2 or argv[0] not in ("validate", "render"):
        raise CliError("usage: audit_report.py validate|render findings.json")

    doc = load_json(argv[1])
    problems = validate(doc)

    if argv[0] == "validate":
        if problems:
            print(f"{len(problems)} problem(s):")
            for problem in problems:
                print(f"  - {problem}")
            return 1
        print("valid.")
        low = lowest_failing_rung(doc.get("findings", []))
        if low:
            print(f"lowest failing rung: {low} ({RUNGS[low]})")
        return 0

    # render refuses invalid input so a broken report cannot ship quietly
    if problems:
        print("refusing to render an invalid findings file. Run validate.",
              file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(render(doc))
    return 0


if __name__ == "__main__":
    run(main)
