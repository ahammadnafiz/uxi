---
name: uxi
description: UX research and UI design guidance for any product in any domain. Use this whenever the work touches interface design, usability, design critique, accessibility, design systems, user research, information architecture, onboarding, forms, dashboards, landing pages, empty and error states, or interface copy. Trigger it even when the request sounds like plain frontend work ("build a settings page", "make this look better", "our signup is leaking users", "review this screen"), because in those requests the design decisions are the hard part and the code is the easy part. Covers heuristic evaluation, WCAG 2.2 conformance, visual craft, research method selection, success metrics, and deceptive-pattern screening, with runnable Python tools for contrast checking, HTML accessibility linting, CSS craft linting, research statistics, and audit validation.
license: MIT
---

# UX

This is a working procedure for designing interfaces and for checking whether they actually work. It is domain agnostic on purpose. A checkout, a radiology dashboard, a game settings menu, and an internal deploy console all get the same procedure. What changes is the surface class and the failure modes, and this skill names both for you.

Two things it will not do. It will not hand you a visual style, because that belongs to the project's own design file or brand. And it will not let you skip framing the problem before you draw, because that is where most bad interfaces come from.

## Start here: what kind of ask is this?

| The request sounds like | Do this | Read next |
|---|---|---|
| "Review this screen / is this good?" | Run the audit in Step 2, report by rung | `references/heuristics.md` |
| "Design a screen / flow / app" | Step 0, Step 1, then build, then the ship gate | `references/visual-craft.md`, the matching playbook |
| "Why is this metric bad?" | Step 1 question 3, then diagnose bottom up | `references/research.md` |
| "Is this accessible?" | Run the accessibility pass on its own | `references/accessibility.md` |
| "Should we build X pattern?" | Check the floor first, then Step 1 | `references/ethics.md` |
| "How do we find out what users want?" | Pick a method by question type, not by habit | `references/research.md` |
| "Write the copy for this state" | Voice, then clarity, then the specific state rules | `references/heuristics.md` (writing section) |
| "Set up a design system" | Tokens before components, always | `references/visual-craft.md` |
| Anything shaped like a deliverable | Use the matching template | `references/deliverables.md` |

If the ask is explicit and expert ("write this microcopy in this voice"), just do it well and flag risks briefly. Do not restart the whole process on someone who already knows what they want.

## Step 0. Name the surface class

Takes ten seconds and decides which rules apply. Getting it wrong produces confident, wrong verdicts.

| Class | Examples | Visit pattern | Optimizes for |
|---|---|---|---|
| Acquisition | Landing pages, marketing sections, pricing, app store listing | First visit, low commitment | Comprehension, trust, memory |
| Transaction | Checkout, signup, booking, upload, payment, onboarding | First or rare, high stakes | Completion without regret |
| Application | Dashboards, admin panels, editors, IDEs, CRMs, clinical tools | Daily, repeat, expert | Speed, task completion, reversibility |
| Content | Docs, articles, search results, catalogs, feeds | Variable, scanning | Findability and readability |
| System | Empty, loading, error, offline, permission denied, destructive confirm | Interstitial, unplanned | Orientation and recovery |

Declare mixed screens per region, not per page. A product detail page is Acquisition in the hero and Transaction in the buy box. A dashboard is Application in the table and System in its empty state.

This matters because almost every published UX heuristic was calibrated on marketing pages. Applied without translation to an expert tool they produce nonsense: a data table "fails" for having too many interactive elements, an order screen "fails" for having no call to action above the fold, an internal console "fails" for having no social proof. On an expert surface, density is the product. What you score there is unresolved density, not density.

## Step 1. Frame before you draw

Answer these six before proposing anything. Each one is a sentence or two, not a document.

1. Who is this for, specifically? Not "users." A warehouse supervisor on a cracked Android in bad light is a different design than an analyst on two monitors.
2. What job are they trying to finish, in their words? If you cannot say it in their vocabulary, you have not researched enough.
3. What does success look like as a number? Pick one user metric and one business metric. Conversion on its own rewards manipulation. Task completion rate and error rate do not.
4. What do they already know? People spend nearly all their time in other products, so their expectations are set elsewhere. Deviating from a convention costs you their learning time, so the deviation had better be worth it.
5. What are the real constraints? Device, network, locale, reading level, regulation, existing system, team capacity.
6. What does it cost someone if this goes wrong? A mis-tap in a music app costs three seconds. A mis-tap in a dosage field costs more than that. Consequence sets how much friction you are allowed to add.

Hold off on solutions until these are answered. Solution-first thinking quietly narrows the requirement space: you stop seeing what the constraints demand and start seeing what your idea already provides.

## Step 2. Diagnose in order

Work bottom up. A break at a lower rung eats the attention the higher rungs need, so polishing persuasion while the keyboard path is broken is wasted work. Report findings by rung, and say which rung is the lowest failure. That single fact is usually the whole recommendation.

### Rung 1. Access

Can a person perceive and operate this at all, including with a screen reader, a keyboard, one hand, a tremor, low vision, or in sunlight?

Check contrast, target size and spacing, keyboard reachability, visible focus, labels and names, motion preferences, and text scaling. Nothing above this rung counts if this one is broken, and in most jurisdictions this is also the legally exposed rung. Full checklist and numbers in `references/accessibility.md`.

### Rung 2. Orientation

Within a couple of seconds: where am I, what is this, and where do I go next?

On Acquisition, the hero is the argument, and visual quality has to match the price point. On Application, the first impression fires on the empty state and the first run, not on a hero. On repeat visits it becomes time to anchor: can their eye reach the thing they came for that fast? Layout stability across sessions is the asset. A dashboard that reshuffles its cards resets that judgment every visit.

Loading states are part of this rung. When the shape of the content is already known, a bare spinner makes people judge nothing at all.

### Rung 3. Task completion

Can they finish, and can they recover when they do not?

Count decisions from entry to done and delete every field not required to complete the task. Score carried state: anything a person must hold in their head across a navigation boundary (an ID to copy, a filter to reapply, a value from the previous screen) is a chunk spent, and working memory holds roughly three to five. Three or more carried chunks in one task is a serious defect. Work lost on refresh, navigate-away, or session expiry is a critical one, since interrupted knowledge work is expensive to recover from.

Every failure state has to offer a next action. An error that reports without a route forward is a dead end wearing an error message.

### Rung 4. Coherence

Does this feel like one thing made by one team?

Two type families at most, one real spacing scale, unified radii and shadows and motion, values pulled from tokens rather than typed in by hand. Geometry should not move between loading, loaded, empty, and error. Interaction timing is a token too: the same class of action gets the same duration and easing everywhere.

Near-miss deviations cost more than far-miss ones. A brand color three percent off reads as broken in a way that a clearly different color does not, because perception is sharpest at small differences.

Coherence is also why aesthetics are not decoration. People rate attractive interfaces as easier to use, and they tolerate small usability problems in them. That effect is real, and it cuts both ways: it can mask problems during testing, so never let a good-looking prototype substitute for a task success measurement.

### Rung 5. Arrangement and honesty

Every layout is a nudge. There is no neutral arrangement, so the question is never whether you are influencing the choice, only whether you are being honest about it.

One unambiguous primary action per screen state, and when the action changes with state (Save, then Publish, then Revert), make the change legible. Prefer reversibility over confirmation: undo costs one interaction after the fact, a confirm dialog costs one on every pass and trains people to dismiss it. Preview before commit, because decisions made from a description underweight what actually happens. Match register to commitment distance, since "Save" and "Publish to your live site" are different psychological distances and must not read alike.

Then screen against the floor below.

## The floor

These do not ship, whatever the projected lift. Full catalog, severity, and regulatory exposure in `references/ethics.md`.

- Costs revealed late in a flow.
- Anything added to a cart or order the person did not choose.
- Consent, marketing, or data sharing checked by default.
- A trial that becomes a charge without warning, or a cancellation harder than the signup.
- Scarcity, countdowns, or viewer counts not backed by real data.
- Guilt-shaming the decline option, or styling it weaker than the accept.
- Destructive actions that are irreversible and easy to trigger.
- Errors that state a code and nothing else.

If you build components other people use (a page builder, a template library, a component kit), ask the sharper version of this question: which of these patterns does my platform make easy? Three positions, and you should pick one deliberately per component rather than by default: do not ship the capability at all; ship it bound to truth, so a countdown needs a real deadline and a stock badge can only read real inventory; or ship it with the builder warned, which is the weakest option and only for when the first two genuinely do not work.

## Step 3. Ship gate

Every line is pass or fail. A failure at a lower rung blocks, because higher rungs cannot compensate for a broken foundation.

- [ ] Surface class declared, and the matching rule set applied.
- [ ] Access: contrast, target size, keyboard path, visible focus, labels, motion preference, text scaling to 200 percent.
- [ ] Orientation: empty and first-run states designed. Loading matches loaded geometry. Layout stable across sessions.
- [ ] Task: a first-time user finishes the primary task without a "where do I click" moment. No carried state across navigation. No work lost on refresh.
- [ ] Coherence: squint test passes, nothing off-token, nothing reflows between states.
- [ ] Honesty: copy matches behavior. One primary action per state. Destructive actions reversible or blast radius stated specifically ("deletes 14 variants"). Every error routes forward.
- [ ] Floor: no pattern from the catalog. For platform components, the position is chosen and written down.
- [ ] Measurement: one user metric and one business metric defined before launch, not after.

Missing empty states and missing error states are defects, not omissions. Treat them as such in the report.

## How to report an audit

Lead with the lowest failing rung and the single change with the most leverage. Then findings grouped by rung, each with the evidence, the severity, and a concrete fix. Then what is working, because teams need to know what not to break. Templates in `references/deliverables.md`.

Severity language that survives contact with a product team:

- Blocker: people cannot complete the task, lose work, or are excluded. Ship date moves.
- Serious: people complete the task but pay for it in time, errors, or support tickets.
- Minor: friction or inconsistency, fix it in the normal queue.
- Note: a judgment call worth discussing, not a defect.

Do not pad a report with minors to look thorough. Three well-evidenced blockers beat forty nitpicks, and the nitpicks train people to ignore you.

## When to skip most of this

Rigor is valuable when it is the scarce resource and expensive when it is not.

- Renaming a button inside an established system.
- Purely technical work with no user-facing change.
- A hotfix under real time pressure. Ship it, write down the debt, come back.
- An explicit expert request, where re-framing the problem is just friction.

The floor and the access rung are the exceptions. Those apply every single time.

## What this skill will not pretend

Being honest about the soft spots is part of using them well.

Heuristic evaluation finds problems, not solutions, and different evaluators find different problems. Treat any numeric usability score as an estimate and trust the ordering (which rung failed lowest) rather than the number.

"Five users find most usability problems" is a good argument for testing at all, not a coverage guarantee. It assumes a per-user detection rate that does not hold for complex or multi-audience products. Test more for checkout and for anything with a safety consequence, less for a settings toggle.

Best practices are priors, not verdicts. Convention is a strong prior because people learn it elsewhere, but a measured result from your own users beats any guideline in this skill, including this sentence.

## Scripts and the validation loop

The `scripts/` folder holds five tools, all plain Python with no dependencies. Run them instead of eyeballing whenever the input exists as a file, because a measured number beats a squint every time, and the exit codes let any of them gate a CI step. Every one of them exits 0 when clean, 1 when it found something, and 2 when it could not run at all, so a red build means a finding and never a typo in the invocation. (`_common.py` alongside them is shared color and file handling, not a tool.)

- `contrast_check.py`: WCAG 2.2 contrast ratios. One pair, a JSON list of token pairs, or `--scan` over a CSS file. Knows the text, large-text, and UI thresholds, and flags translucent hex values rather than scoring them as if they were opaque.
- `a11y_lint.py`: static HTML pass for the mechanical accessibility failures. Of the ten common failures in `references/accessibility.md` a parser can see five: focus removed inline, click handlers on divs, placeholder-as-label, custom widget roles that cannot be focused, and icon-only controls with no accessible name. It adds missing alt, missing lang, skipped headings, positive tabindex, zoom-blocking viewport meta, and autoplay with sound. The other five failures (color as the only signal, sticky headers covering focus, text baked into images, contrast that only breaks in dark mode, auto-dismissing toasts) are invisible to it. A clean run means no mechanical defects, never "accessible"; the keyboard and screen reader passes still happen by hand.
- `craft_lint.py`: the coherence rung, measured. Off-scale spacing in px, rem, and em, near-miss color drift, off-token colors, sub-12px type, more than two type families, focus removal without a real replacement, transition durations off the token set, animations that outstay 500ms, motion defined with no `prefers-reduced-motion` block, more than five elevation shadows or four radii, and interactive rules sized under the 24px target minimum. Findings are prompts for judgment: a value may be off-scale on purpose, and the point is that it should be on purpose.
- `research_stats.py`: SUS scoring with interpretation, Wilson intervals for small-sample completion rates, and time-on-task summaries that use the median and geometric mean because task times are skewed. It reads answer columns by position and reports every row it skipped and why, because a silently mis-scored participant is worse than a missing one.
- `audit_report.py`: the loop itself. Draft findings as JSON while auditing, then `validate` until it stops complaining, then `render` for the markdown report. The validator enforces the discipline this skill asks for: evidence and a location on every finding, evidence long enough to be evidence rather than a label, a fix on every blocker and serious, surface class declared, something in "working well", and a cap on minor-finding padding that scales with how many real findings you have. `render` refuses invalid input, so a sloppy report cannot ship quietly. A worked example lives at `assets/example-findings.json`.

The loop for an audit, concretely: run the linters first to clear the mechanical layer, do the human passes (keyboard, screen reader, task walk-through), write findings into the JSON as you go, validate, fix what it flags, render, and only then write the prose summary. Draft, check, fix, repeat is the whole method, and it applies to your own work exactly as it applies to the interface under review.

`evals/evals.json` holds twelve test prompts for checking that the skill itself still produces good output after edits. Each carries `must` and `must_not` assertions, because most of the ways this skill fails are things it should not have said: parroting tool output as if every line were a defect, running the whole procedure on a one-word label change, or being argued off the floor by a conversion number. Four of them also carry `deterministic` blocks (a command, an expected exit code, and required substrings) which grade without a judge.

Those evals run against real fixtures in `assets/fixtures/`: a checkout page and stylesheet carrying the ordinary kind of drift, a token file, a messy SUS export with a blank answer and an out-of-range typo, and a findings draft that fails validation in nine named ways. `assets/fixtures/ANSWERS.md` records what every tool actually reports on them, including the findings that are correct output but *not* defects: the deliberate surface tint that reads as color drift, and the contrast scan comparing two backgrounds that never carry text. An answer that reports those as defects fails the eval even though it came straight from the tool. `python evals/check.py` runs the deterministic blocks and confirms every fixture path resolves, so a script change that invalidates the answer key shows up as a failing check rather than as a quietly wrong number; update the key in the same commit.

Read the file when the work needs it, not all of them at once.

- `references/laws-of-ux.md`: all thirty Laws of UX in full, each with the claim, its research origin, what to do with it, and how it gets misused in arguments.
- `references/heuristics.md`: the ten usability heuristics applied per surface class, the behavioral laws worth knowing and the ones commonly misapplied, Gestalt grouping, interface writing.
- `references/accessibility.md`: WCAG 2.2 structure and the numbers, per-platform target and type sizes, keyboard and screen reader procedure, common failures, how to actually test.
- `references/visual-craft.md`: type scale, spacing, color and tokens, layout and breakpoints, density, elevation, motion, dark mode, state design, data visualization.
- `references/research.md`: choosing a method by the question you have, sample sizes, task writing, interview technique, synthesis, metrics frameworks, common analysis mistakes.
- `references/ethics.md`: deceptive pattern catalog with severity, the regulations that bite, the platform question, honest alternatives that still perform.
- `references/domain-playbooks.md`: what changes for ecommerce, SaaS admin, mobile, marketing, forms and onboarding, search and IA, data-heavy tools, fintech, health, education, AI and chat interfaces, dev tools.
- `references/deliverables.md`: templates for audits, design specs, research plans, usability test scripts, and design system docs.

## Sources

This skill is written from public guidance and restates it in its own words rather than reproducing it. Go to the originals when a specific ruling matters.

- Nielsen Norman Group, 10 usability heuristics and the UX research method landscape (nngroup.com).
- Apple Human Interface Guidelines, design principles, accessibility, layout, typography, color (developer.apple.com/design).
- Laws of UX by Jon Yablonski, CC BY-NC-ND (lawsofux.com).
- W3C Web Content Accessibility Guidelines 2.2, W3C Recommendation, October 2023 (w3.org/WAI).
- Google Material Design 3 foundations, tokens, and adaptive layout (m3.material.io).
- UK Government Design Principles, Open Government Licence (gov.uk/design-principles).
- Design system documentation from Shopify Polaris, IBM Carbon, Atlassian, and Microsoft Fluent.
- Deceptive pattern taxonomies from Harry Brignull (deceptive.design) and Gray et al., 2018.
