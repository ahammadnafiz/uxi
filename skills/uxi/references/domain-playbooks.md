# Domain playbooks

Read the entry that matches the work. Each one covers what changes from the general procedure, the failure modes that show up over and over, and the metrics worth watching.

The general rungs still apply everywhere. These playbooks tell you where to aim first.

## Ecommerce and checkout

Surface classes: Acquisition on category and product pages, Transaction from cart onward.

What changes: the cost of a defect is measured in abandoned orders, and the checkout is the single highest-value flow you will ever touch. Also the flow with the most regulatory attention.

Aim first at: total cost visible from the first step, guest checkout, express wallets (Apple Pay, Google Pay, and whatever else your buyers carry) offered early since they collapse the address and card steps, address and card autofill, a cart that survives a session, and clear delivery expectations. Product pages need real photography at the size people zoom to, an honest stock signal, and reviews with the volume shown.

Failure modes: shipping revealed at step four, forced account creation, a coupon field that sends people off to search for a code, silent stock changes between cart and payment, one long form instead of steps, mobile keyboards that do not match the field type, and error messages that clear the entered card details.

Metrics: cart-to-order conversion, checkout step drop-off, form field error rate, time to first purchase, return and refund rate, support contacts per thousand orders.

## SaaS admin and internal tools

Surface class: Application, almost entirely, with System states everywhere.

What changes: everything you know from marketing pages inverts. Density is the product. People use this all day, so the second visit matters more than the first, and small per-interaction costs multiply into real hours.

Aim first at: carried state (anything a person must remember across a navigation), work lost on refresh or session expiry, bulk actions, keyboard support, saved views and filters that persist, and the empty state of every list.

Failure modes: an ID shown on one screen and required on another, filters that reset on back, a modal that loses a half-finished form, a confirm dialog on every save that trains dismissal, tables that cannot be sorted or exported, and a first-run experience nobody designed because the team's accounts all have data.

Metrics: task completion time for the top five tasks, error and retry rate, support tickets by screen, feature adoption among daily users, and time to first success for new accounts.

## Mobile apps

Surface class: varies, but the constraints are constant.

What changes: one hand, interruption, bad network, small screen, and a system that has strong conventions you should follow rather than reinvent.

Aim first at: thumb reach for primary actions, targets at platform minimums with real spacing, offline and slow-network states, permission requests asked in context with a reason rather than on launch, and state restoration after the app is killed in the background.

Failure modes: desktop layouts squeezed down, gestures with no visible alternative, permission prompts on first launch before any value is shown, forms that do not switch keyboard type, content hidden behind the home indicator or notch, and destructive swipe actions without undo.

Platform notes: follow the platform's navigation model rather than porting one across. Support Dynamic Type or its equivalent, since a large share of people run larger text than default. Respect reduced motion. Test one-handed, outdoors, and on the cheapest device you support.

Metrics: day 1 and day 7 retention, time to first value, crash-free sessions, permission grant rate, and completion rate on the top task by device tier.

## Marketing sites and landing pages

Surface class: Acquisition.

What changes: you get a couple of seconds, the decision is made before conscious evaluation, and visual quality is read as product quality.

Aim first at: a hero that states what this is and who it is for in plain words, one primary action, proof that is real, and load performance, since a slow page loses people before design matters at all.

Failure modes: a headline that describes the company rather than the offer, four competing calls to action, jargon in the first paragraph, stock photography that says nothing, autoplay video, a cookie banner that covers the content, and a form asking for eleven fields before anyone knows what they get.

Metrics: scroll depth to the primary action, click-through on that action, and the downstream conversion rate rather than the click, because optimizing the click alone is how you get a good landing page feeding a bad funnel.

## Forms and onboarding

Surface class: Transaction.

What changes: every field is a chance to lose someone, and errors carry more emotional weight here than anywhere else.

Aim first at: cutting fields to what you genuinely need now, one column, visible persistent labels, autofill attributes, inline validation that fires on blur rather than on every keystroke, and preserving entered data through every error.

Failure modes: placeholder-as-label, red asterisks as the only required marker, validation that fires while typing, clearing the form on a server error, splitting fields that people think of as one thing (name, phone, card number), rejecting valid input formats, and a password rule list revealed only after a failure.

For onboarding specifically: nobody reads the tour. Teach inside the first real task, defer anything you can ask later, and make the first success happen fast. Show progress honestly. Let people skip and come back.

Metrics: field-level error rate, field-level drop-off, completion rate, time to complete, and time to first success after signup.

## Search, navigation, and information architecture

Surface class: Content.

What changes: people arrive with a goal and a word for it, and your job is matching their word to your structure.

Aim first at: labels drawn from their vocabulary rather than your org chart, a search that tolerates typos and synonyms, useful zero-result states that suggest alternatives, filters that show counts and can be cleared, and a structure verified by tree testing rather than by internal debate.

Failure modes: navigation that mirrors the company structure, categories named with internal terms, search that only matches exact strings, filters that reload the page and lose scroll position, no indication of how many results exist, and pagination with no sense of where you are.

Method pairing worth knowing: card sort to build the structure, tree test to verify it, then analytics on internal search queries to find what people ask for that you do not have. Internal search logs are the cheapest research data most teams already own and ignore.

Metrics: search success rate, zero-result rate, refinement rate, findability score from tree testing, and time to find.

## Data-heavy tools: tables, dashboards, analytics

Surface class: Application.

What changes: comprehension is the whole job. The interface is a lens on the data, and the failure mode is a wrong conclusion drawn confidently.

Aim first at: column rhythm (numbers right-aligned and tabular, text left, status consistent), sticky headers, sortable columns, obvious empty and loading states that match the loaded geometry, and a stated takeaway next to every chart.

Failure modes: pie charts with eight slices, truncated bar axes, meaning carried by color alone, legends that force you to look away and match by memory, dashboards that reorder cards between sessions, and metric names that nobody can define when asked.

Practical rules: pick the chart from the question rather than from variety. Label series directly when you can. Cap at about six series and use small multiples past that. Publish the definition of every metric next to it, since arguing about whether the number is right is where most dashboard time actually goes.

## Fintech and anything moving money

What changes: consequence. A mis-tap costs real money and confidence, and it is a regulated space where the copy is part of the compliance surface.

Aim first at: preview before commit with the exact amount, recipient, fees, and arrival time. Confirmation that is proportional to irreversibility. Clear transaction states, since pending is not the same as sent and people need to know which one they are in. Plain-language explanations of fees.

Failure modes: amount fields without clear currency, no review step, ambiguous pending states, error messages that do not say whether money moved, and reversibility implied where none exists.

Add friction deliberately here. This is one of the few places where a confirm step earns its cost, and even here prefer a review screen showing the full picture over a yes/no dialog.

## Health, clinical, and safety-critical

What changes: errors can hurt people, and users are often stressed, interrupted, or working fast under load.

Aim first at: preventing wrong-patient and wrong-value errors by design, unambiguous units, no ambiguous abbreviations, alert design that does not cause fatigue, and clear separation between similar-looking actions.

Failure modes: alert fatigue from over-alerting, which trains people to dismiss everything including the one that mattered. Free-text where structured input belongs. Dense screens where the critical value is not visually dominant. Timeouts that lose work mid-task.

Do not run this without domain experts and real clinical testing, and do not let a generalist design review substitute for that. Everything in this file is a starting point, not a sign-off.

## Education and learning

What changes: the person is here to change, not to complete a transaction, so time on task can be a good sign rather than a bad one.

Aim first at: progress that is visible and honest, chunking that matches attention spans, immediate feedback on attempts, the ability to resume, and difficulty that adapts or at least offers options.

Failure modes: gamification that rewards streak-keeping over learning, progress bars that measure content consumed rather than skill gained, punishing wrong answers rather than teaching from them, and no way to review what was covered.

Metrics: completion, return rate, demonstrated skill on a later assessment, and time to first success. Watch the gap between engagement and learning, since the two come apart easily.

## AI, chat, and agentic interfaces

Newer surface class, and the conventions are still forming, but the failures are already consistent.

Aim first at: setting expectations about what the system can do before someone asks, showing progress on long operations, making outputs editable rather than take-it-or-leave-it, making the source of a claim visible, and making it easy to undo or reject an action the system took.

Failure modes: a blank prompt box with no hint of capability, confident wrong answers with no uncertainty signal, no way to correct a misunderstanding without starting over, long silent waits, actions taken on a person's behalf without a preview or a receipt, and losing conversation state on refresh.

Design principles that transfer well here: preview before commit is more important than usual, since decisions from description underweight what actually happens. Reversibility beats confirmation. And the honesty rung matters more than anywhere else, because a system that speaks fluently is trusted more than it has earned.

Metrics: task success without human correction, correction and retry rate, abandonment mid-task, and how often people accept output unedited (which is a quality signal in both directions and needs interpreting carefully).

## Developer tools

What changes: your users read documentation, will accept complexity for power, and notice inconsistency immediately.

Aim first at: error messages that name the cause and the fix with a copyable identifier, sensible defaults with everything overridable, a fast path from install to first working result, and keyboard and CLI parity with the graphical path.

Failure modes: stack traces as the entire error surface, docs organized by your architecture rather than by task, tutorials that assume state a new user does not have, and a graphical layer that cannot do what the command line can.

Metrics: time to first successful run, error rate on setup, doc search queries with no result, and the ratio of support questions that the error message itself could have answered.
