# Fixture answer key

Every number here was captured from an actual run, not predicted. Re-run
the commands after changing a script and update this file in the same
commit; a stale key is worse than no key, because it fails honest work.

The fixtures are a mid-size ecommerce checkout at step 3 of 4. They are
deliberately ordinary: the defects are the kind that arrive through six
months of small commits, not invented ones. Several tool findings are
**judgment traps** — correct output that a good analyst must *not* report
as a defect. Those are marked. An answer that parrots every line of tool
output fails the eval even though every line came from the tool.

---

## `a11y_lint.py assets/fixtures/checkout.html`

Exit 1. **12 errors, 1 warning.**

| Line | Severity | Finding |
|---|---|---|
| 6 | error | viewport `maximum-scale=1` blocks zoom |
| 35 | error | heading jumps h1 → h3 |
| 44 | error | promo input labeled only by placeholder |
| 45 | error | `<div onclick>` with no interactive role |
| 58 | error | `<div role="button">` with no tabindex |
| 64 | warn | `target=_blank` without `rel=noopener` |
| 74, 81 | error | icon-only buttons with no accessible name |
| 75, 82 | error | remove-icon `<img>` with no alt |
| 89, 90, 91 | error | payment logo `<img>` with no alt |

**Must also be said, and no tool can see it:** this is 5 of the 10 common
failures in `references/accessibility.md`. Colour-as-only-signal, sticky
headers covering focus, text baked into images, dark-mode-only contrast
breaks, and auto-dismissing toasts are invisible here. The `.toast` rule
in the CSS is a live instance of the last one and the lint says nothing
about it. A clean lint would still not mean accessible.

**Judgment trap:** the three payment-logo images at lines 89-91 are
decorative next to the words "Visa, Mastercard, Amex" nowhere present —
so they are *not* decorative, and `alt=""` is the wrong fix. An answer
that recommends `alt=""` for all five images has missed that two of them
(the remove buttons) are the sole accessible name for a control.

---

## `craft_lint.py assets/fixtures/checkout.css --tokens assets/fixtures/tokens.json`

Exit 1. **16 findings.**

Real defects, rung 4:
- `0.9rem` and `13px` spacing off the 4px scale
- `#2563ef` off-palette and a near-miss against `#2563eb` (distance 4) —
  one brand blue that drifted, the textbook case
- `#9aa3af` off-palette entirely
- 11px hint text, below the 12px floor
- 3 type families (Inter, Söhne Breit, SF Mono) against a ceiling of 2
- `.btn:focus { outline: none }` with no replacement — failure #1 in
  `accessibility.md`, and a rung 1 issue found by a rung 4 tool
- 333ms transition off the token set
- 800ms toast animation past the 500ms ceiling
- no `prefers-reduced-motion` block anywhere
- 7 box-shadow values against the 5-level ladder
- 8 border-radius values (4, 6, 8, 10, 11, 12, 14, 16px)
- `.icon-btn` at 20×20, under the 24px target minimum (two findings,
  width and height)

**Judgment trap:** `near-miss colors #fbfcfd and #ffffff (distance 5)`.
This one is correct output and not a defect. `#fbfcfd` is the summary
card's deliberate off-white tint against the page's `#ffffff`; a subtle
surface step is how the card reads as raised without a heavy shadow.
Reporting it as drift is the failure mode the tool's own docstring warns
about — findings are prompts for judgment, not verdicts.

---

## `contrast_check.py --pairs assets/fixtures/contrast-pairs.json`

Exit 1. **3 of 9 pairs fail.**

| Pair | Ratio | Verdict |
|---|---|---|
| step counter `#9aa3af` on `#ffffff` | 2.55:1 | FAIL text AA |
| hint text `#9aa3af` on `#fbfcfd` | 2.48:1 | FAIL text AA |
| ghost button border `#e4e7ec` on `#ffffff` | 1.24:1 | FAIL ui AA |
| primary button label | 5.17:1 | passes AA, fails AAA |
| muted text `#5b6472` | 5.98:1 | passes AA, fails AAA |

The `#9aa3af` failures and the invisible `#e4e7ec` border are rung 1
blockers, not styling notes: a control boundary at 1.24:1 is a control
some people cannot find.

## `contrast_check.py --scan assets/fixtures/checkout.css`

Exit 1, 8 flagged pairs. **This mode is noisy by design and most of its
output here is not a defect.** `#f2f4f7 on #ffffff` (1.10:1) and
`#fbfcfd on #ffffff` (1.03:1) are background-against-background pairs
that never carry text, and the `on #16181d` block compares against the
ink colour as though it were a surface. Only `#9aa3af` and `#e4e7ec`
survive as real findings, and `--pairs` already found those with the
declared use attached. A good answer uses `--scan` to *discover*
candidates and `--pairs` to *decide*, and says so.

---

## `research_stats.py sus assets/fixtures/sus-responses.csv`

Exit 0. **Mean 64.7, sd 24.4, n=9, band D.** 4 rows skipped, each named:

- row 1 — header
- row 6 (P05) — q3 blank
- row 9 (P08) — q1 is 7, outside 1-5
- row 11 (P10) — only 9 of 10 columns

It also prints that columns 2-11 were read as q1..q10 because of the
participant id column.

**Must be said:** 64.7 sits below the ~68 benchmark, and with n=9 and an
sd of 24.4 the spread matters more than the mean — participants are
split, not uniformly mildly unhappy. Reporting "SUS 64.7, slightly below
average" and stopping is the failure. Three of twelve participants were
dropped for data problems, which is itself a finding about how the study
was run.

**Judgment trap:** SUS measures perceived usability. It cannot be used to
argue the checkout's hidden delivery cost is acceptable because the score
is mid-range; the aesthetic-usability effect inflates exactly this kind
of score.

---

## `audit_report.py validate assets/fixtures/invalid-findings.json`

Exit 1. **9 problems**, one per category the validator enforces:

1. missing `surface_class`
2. missing `headline_fix`
3. empty `working_well`
4. finding 1 severity `critical` — not in the vocabulary (blocker,
   serious, minor, note)
5. finding 2 blocker with no fix
6. finding 3 serious with no fix
7. finding 3 evidence 3 chars, under the 20-char floor
8. finding 5 rung 7, outside 1-5
9. 8 minors against 2 real findings, over the limit of 6

`render` on the same file exits 1 and refuses.

The fixed version of this document is `assets/example-findings.json`,
which validates clean and renders. The gap between the two files is the
whole method: draft, check, fix, repeat.
