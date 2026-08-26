# Deliverable templates

Use these when the output needs to be a document someone else acts on. Adapt the headings to the job, keep the order, and cut sections that carry nothing rather than filling them with padding.

One rule across all of them: put the answer first. Nobody reads to the end of a design document to find out what you recommend.

## UX audit

```markdown
# UX audit: [surface or flow]

**Scope:** what was reviewed, on what device, in what state, on what date
**Surface class:** Acquisition / Transaction / Application / Content / System
**Method:** heuristic review, or observed sessions with N participants, or both

## The short version
The lowest failing rung is [rung]. [One sentence on what breaks.]
The single change with the most leverage is [change], because [reason].

## Blockers
### 1. [What is wrong, stated as the problem not the fix]
**Where:** exact screen and element
**Evidence:** what you observed, or the heuristic and why it applies
**Impact:** who cannot finish, what it costs
**Fix:** the concrete change
**Effort:** rough size

## Serious
[same structure]

## Minor
[one line each, grouped]

## What is working
[Two to four things worth protecting, so nobody breaks them fixing the rest.]

## What I could not assess
[Anything out of scope, blocked by access, or needing real users to answer.]
```

Severity language: blocker means people cannot complete, lose work, or are excluded. Serious means they complete but pay in time, errors, or support contacts. Minor means friction. Note means a judgment call worth discussing.

Do not pad with minors to look thorough. Three well-evidenced blockers get acted on. Forty findings get filed and you get ignored next time.

## Design spec for handoff

```markdown
# [Component or screen name]

## Purpose
What this is for and when to use it. One paragraph. Include when not to use it.

## Anatomy
Named parts with the tokens each uses. Not pixel values.

## States
Default, hover, focus, active, disabled, loading, error, empty, selected.
Include what changes and what stays fixed. Geometry must not move between states.

## Behavior
- Interaction: what responds to what
- Keyboard: full key map including Escape and arrow behavior
- Focus: where focus goes on open, on close, on submit
- Validation: when it fires and what it says
- Motion: duration and easing tokens, and reduced-motion behavior

## Responsive
What happens at each width class. What collapses first, what never collapses.

## Content
Label rules, character limits, truncation behavior, empty text, error text.

## Accessibility
Role and name, ARIA where a native element will not do, contrast requirements,
target size, screen reader announcement for each state change.

## Edge cases
Longest realistic content, zero items, one item, many items, slow network,
failed request, right-to-left, longest localized string.

## Open questions
```

The edge cases section is the one that saves the most engineering time. Fill it in properly.

## Research plan

```markdown
# Research plan: [topic]

## The question
One sentence. If there is more than one, rank them.

## Why now
What decision is waiting on this, and who makes that decision.

## What would change my mind
The result that would make us not do the thing we are planning.
Write this before running the study.

## Method and why
Method, and why it fits this question rather than the one we usually run.

## Participants
Who, how many, from where, screening criteria, exclusions.
If there are multiple segments, sample size per segment.

## Tasks or topics
[For usability: scenario-based tasks, none using interface vocabulary,
with a definition of success for each.]
[For interviews: topic areas and opening questions, not a script.]

## Logistics
Dates, sessions per day, tools, incentive, who observes.

## Consent and data
What is recorded, who sees it, retention period, how it is deleted.
Test accounts only. No real credentials or financial data.

## Analysis
How findings will be grouped and rated, and when the readout happens.
```

## Usability test script

```markdown
## Before
- Thanks, here is what we are doing and how long it takes.
- We are testing the design, not you. There are no wrong answers,
  and if something is confusing that is exactly what we need to hear.
- Please think out loud as you go.
- Recording consent, and you can stop at any time.
- Any questions before we start?

## Warm-up
Two or three questions about how they currently do this, in their own words.
This gets them talking and gives you context.

## Tasks
For each:
- Read the scenario aloud and give them a copy
- Stay quiet
- Note the moment before each click, hesitations, and their words
- Post-task: "How did that go?" and "Was anything unexpected?"

## Wrap-up
- Overall impressions
- If you could change one thing
- Anything I should have asked

## Facilitator reminders
Never answer during a task. Turn it back: "What would you expect?"
Never say just, simply, correct, or obviously.
Silence is the tool. Wait longer than feels comfortable.
```

## Design system documentation page

```markdown
# [Component]

## Use it when
## Do not use it when
## Alternatives
[Link to the component they probably want instead]

## Examples
Do and Don't pairs, with the reason under each. Reasons matter more than the images.

## Props or API

## Accessibility
Built in vs. what the consumer must provide.

## Content guidelines
Voice, length, capitalization, what to avoid.

## Changelog
```

The "do not use it when" and "alternatives" sections are what stop a system from drifting. Most component docs skip them and then wonder why people build their own.

## Design decision record

For choices worth remembering, especially ones that will be questioned later.

```markdown
# [Decision]
**Date, status (proposed / accepted / superseded), decided by**

## Context
The situation and constraints. What made this a question.

## Options considered
Each with the case for and the case against. Include the one you rejected
that seems obvious, and say why it does not work here.

## Decision
What we are doing.

## Why
The reason that would still make sense to someone reading this in a year.

## Consequences
What this makes easy, what it makes hard, what we will need to revisit.

## How we will know if this was wrong
The signal to watch for.
```

That last section is the one that makes these documents worth keeping.
