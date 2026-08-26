# UX research

Read this when someone needs to find something out about their users, or when a design argument has stalled because nobody has evidence.

The mistake nearly every team makes is picking the method they already know and then bending the question to fit it. Pick the method from the question.

## Start from the question

Write down the question first, in one sentence, then classify it.

| The question sounds like | You need | Typical method |
|---|---|---|
| Why do people abandon this? | Qualitative, behavioral | Usability test, session replay plus follow-up interview |
| How many people hit this problem? | Quantitative, behavioral | Analytics, benchmark test, A/B test |
| What do people actually need? | Qualitative, generative | Interviews, field study, diary study |
| Which of these two performs better? | Quantitative, behavioral | A/B test, benchmark comparison |
| How do people think about this domain? | Qualitative, attitudinal | Card sort, interviews, mental model work |
| Where should this live in the nav? | Both | Card sort to build, tree test to verify |
| Do people want this at all? | Qualitative then quantitative | Concept test, then survey for scale |
| How do people feel about the brand? | Attitudinal | Survey, desirability study, focus group |
| Are we getting better over time? | Quantitative, summative | Benchmark study repeated on the same script |

Three axes underpin that table, and they are worth holding in your head.

**Attitudinal versus behavioral.** What people say versus what people do. These diverge constantly and predictably. Attitudinal data is limited to what someone is aware of and willing to report, which makes it good for mental models, expectations, and satisfaction, and bad for predicting behavior. Lean behavioral for anything about usability.

**Qualitative versus quantitative.** Qualitative means you observed or heard it directly, which lets you ask why and adapt mid-session. Quantitative means you measured it through an instrument, which lets you say how many. Qualitative answers why and how to fix it. Quantitative answers how many and how much, which is what you need for prioritization.

**Context of use.** Natural use (field studies, analytics), scripted use (usability tests, benchmarks), limited use (card sorting, concept tests, participatory design), or no use at all (brand and desirability studies). Natural gives you external validity and less control. Scripted gives you control and less realism.

## Match method to the product stage

| Stage | Goal | Methods |
|---|---|---|
| Strategize | Find directions and opportunities. Generative. | Field studies, diary studies, interviews, surveys, participatory design, concept testing |
| Design | Improve the thing you are building. Formative. | Card sorting, tree testing, usability testing, moderated and unmoderated remote testing |
| Launch and assess | Measure against yourself or competitors. Summative. | Usability benchmarking, unmoderated testing at scale, A/B testing, analytics, surveys |

The most common sequencing error is running a summative method during the design stage. A/B testing a flow that has a fundamental comprehension problem tells you which broken version is less broken.

## Method notes

**Usability testing.** One person, one facilitator, a set of realistic tasks. The core method, and the one most worth learning properly. Five to eight participants per audience segment finds most of the serious problems in a focused flow. Run it as a series of small rounds rather than one big study, since fixing between rounds is where the value is.

**Field study and contextual inquiry.** Watch people in the place they actually work. Expensive and irreplaceable for complex domains, because the workarounds people have built are invisible in a lab. If someone has a sticky note on the monitor, that sticky note is a design brief.

**Diary study.** Participants record over days or weeks. The right method for anything longitudinal: onboarding, habit formation, infrequent tasks, emotional arcs. Only ask for things people can easily record.

**Interviews.** One on one, in depth. Best for context, history, and mental models. Worst for predicting future behavior, since people are bad at that about themselves.

**Focus groups.** Weak for usability, because of group dynamics and because you are collecting opinions on something people have not used. Useful for early reactions to a concept or brand positioning, and for hearing the vocabulary a group uses.

**Card sorting.** People group and name items, exposing their mental model. Open sort to discover categories, closed sort to validate ones you have.

**Tree testing.** Test findability in a structure without visual design in the way. Pairs with card sorting: sort to build the structure, tree test to verify it, and re-test after changes to show improvement.

**Concept testing.** Put the idea in front of people before you build. You are testing whether the value proposition lands, not the details of the interface.

**Analytics and clickstream.** Tells you what happened at scale and never why. Its main use in research is targeting: find the step where the drop-off is, then go run a qualitative method on that step.

**A/B testing.** Real behavior at scale with proper controls. Powerful and narrow. It compares options you already thought of, cannot tell you why a variant lost, and rewards whatever the metric is, which is exactly how manipulative patterns get shipped by well-meaning teams. Always pair the business metric with a user metric.

**Surveys.** Cheap to run, easy to run badly. Good for attitudes, segmentation, and scale. Keep them short, avoid leading and double-barreled questions, and never ask people to predict their own future behavior.

**Unmoderated testing.** Scales cheaply and loses the ability to probe. Good for benchmarking and simple task validation, weak for exploration.

**Eye tracking.** Tells you where attention went. Expensive, and usually a careful observation of hesitation and mouse behavior gets you far enough.

## Sample sizes, honestly

Small qualitative rounds find most usability problems, and that is the strongest practical argument for testing at all. But treat the familiar "five users find 85 percent of problems" line as a rule of thumb rather than a coverage guarantee, because it assumes a per-user problem detection rate that does not hold for complex products, multiple audiences, or infrequent tasks.

Working guidance:

- Qualitative usability testing: 5 to 8 per distinct audience segment. Two segments means 10 to 16, not 5.
- Card sorting: around 15 to 20 for stable groupings.
- Tree testing and other quantitative tasks: 30 or more per variant.
- Benchmark studies: 30 or more, more if you want confidence intervals worth quoting.
- Surveys: depends on the population and the precision you need, but under 100 responses rarely supports a segment breakdown.
- A/B tests: calculate it from your baseline rate and the minimum effect you care about. Do not stop early because it looked significant on Tuesday.

Test more where the consequence of failure is high. Checkout, authentication, anything clinical, anything financial, anything a person only does once and cannot redo.

## Writing tasks that work

Task quality determines study quality more than participant count does.

Write scenarios, not instructions. "You want to send $200 to your sister who banks elsewhere. Show me how you would do that" beats "Click the transfer button and complete the form." The second one tests whether they can follow directions.

Rules that hold up:

- Never use words that appear in the interface. If your nav says "Transfers" do not say "transfer" in the task.
- Give a motivation, not a procedure.
- One task, one goal. Compound tasks produce uninterpretable results.
- Define what done looks like so you can score it consistently.
- Order tasks so an early one does not teach the answer to a later one, and randomize where you can.
- Pilot with one person before the real sessions. You will rewrite at least one task, every time.

## Moderating

Your job is to stay out of the way and to get people talking while they work.

- Ask people to think out loud, and remind them gently when they go quiet.
- Silence is your best tool. Wait. People fill it with the thing you needed to hear.
- Never answer a question during a task. Turn it back: "What would you expect to happen?"
- Never say "just" or "simply". Never defend the design. Never say "correct".
- Watch for the moment before the click, which is where hesitation lives.
- When someone struggles, that is data, not a failure of hospitality. Let it run a bit before rescuing, then rescue kindly.
- Save your opinion questions for the end, after the behavior is recorded, so you do not prime the tasks.

Consent, always: what you are recording, who sees it, how long you keep it, and that they can stop at any time. Never record credentials or real financial data, and use test accounts.

## Synthesis

Do not skip straight from notes to recommendations, and do not let the loudest session dominate.

1. Capture observations as they happened, one per note, with the participant ID. Keep the observation separate from your interpretation.
2. Group observations into patterns. A pattern needs more than one person, or one person plus a plausible mechanism.
3. Rate each pattern on severity (impact if it happens), frequency (how many hit it), and persistence (can they recover on their own).
4. Turn each pattern into a finding: what happened, who it happened to, why it happened, what to change.
5. Rank by severity times frequency, and be ruthless about the tail. Three well-evidenced findings get acted on. Forty findings get filed.

Report structure that people actually read: the headline finding first, then evidence, then what to change, then what is working well. Keep clips short and let them carry the weight, since 20 seconds of someone struggling moves a stakeholder further than a page of prose.

## Metrics

**Define success before you build.** Otherwise you measure what is easy and optimize the wrong thing.

Pair every business metric with a user metric. Conversion alone rewards manipulation. Task completion rate and error rate do not.

Core usability measures, worth more than most dashboards:

- Task completion rate, unassisted.
- Time on task, for tasks people want to finish quickly.
- Error rate and error recovery rate.
- Time to first success, which is the onboarding metric that matters.

Frameworks that help structure this:

- **HEART** (happiness, engagement, adoption, retention, task success) with goals, signals, and metrics for each. Its value is forcing you to write down the goal before the metric.
- **Top tasks**, which is simply identifying the handful of things most people come to do and measuring only those. Underrated, cheap, and hard to argue with.

Watch for Goodhart's law: once a metric becomes a target, it stops measuring what it measured. High conversion with poor retention is a deceptive pattern smell. Rising time on page is good for a content site and usually bad for an admin tool, so never import a metric without importing its context.

## Common analysis mistakes

- Treating a preference as a finding. What people say they prefer often loses to what they use successfully.
- Reporting counts from a qualitative study as if they were rates. Say "three of six participants", not "50 percent".
- Recruiting whoever is convenient and then generalizing. Convenience samples are fine for finding problems and unusable for estimating prevalence.
- Confirming the design you already made. Write down what result would change your mind before you run the study.
- Confusing a novelty effect for an improvement. Measure again after two weeks.
- Ignoring the people who did not respond, did not finish, or dropped out. That group usually holds the finding.
