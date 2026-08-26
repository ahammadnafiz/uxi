# Heuristics, laws, and interface writing

Read this when auditing an interface, arguing for a change, or writing the words inside a screen.

Contents: the ten heuristics translated per surface class, the behavioral laws worth knowing, the ones people misapply, Gestalt grouping, and interface writing.

## The ten usability heuristics, translated

Jakob Nielsen's set from 1994, still the most useful audit vocabulary in the field. Below is each one plus what it actually means on an expert tool versus a first-visit page, because the untranslated version is where most bad reviews come from.

### 1. Visibility of system status

Keep people informed about what is happening, with feedback fast enough to feel connected to their action.

Acquisition and Transaction: progress through a multi-step flow, what happened after a submit, whether the payment went through.

Application: this becomes system honesty. Counts that are accurate. Progress bars that track real work rather than animating on a timer. "Saved" that means saved. A product that sells speed and takes three seconds to save disproves itself to the same person hundreds of times a day.

Feedback under about 400ms keeps a person in flow with the system. Past roughly a second, attention starts to drift and you need to say something. Past ten seconds, people leave the tab.

Common failures: an action fires and nothing visibly happens, optimistic UI that lies when the request fails, a spinner with no timeout and no error path.

### 2. Match between the system and the real world

Use the words and concepts your people already use, not internal jargon, and order information the way they think about it.

Acquisition: lead with outcomes, not features or architecture.

Application: expert jargon is correct here. A radiologist wants the radiology word. The failure is your jargon, not their jargon, so "orphaned entity" is bad and "unassigned order" is good.

Test: read every label out loud to someone who does the job. Anything they have to translate is a defect.

### 3. User control and freedom

People act by mistake constantly. They need a marked exit that does not require walking the whole path backwards.

Support undo and redo. Make cancel visible and honest, meaning it actually cancels. Never trap someone in a flow with no way out but completing it.

Reversibility beats confirmation almost every time. A confirm dialog taxes every correct action to catch the rare wrong one, and it trains dismissal, which means it stops working exactly when you need it. Use undo, and reserve confirmation for actions that cannot be undone (sending money, sending an email, deleting production data). When you do confirm, state the blast radius specifically: "Delete 14 variants and 3 images" beats "Are you sure?"

### 4. Consistency and standards

Internal consistency means the same thing looks and behaves the same way across your product. External consistency means following the conventions of the platform and the wider web.

External consistency is worth more than designers usually admit, because people spend nearly all their time in other products and arrive with expectations already formed. Every deviation spends their learning budget. Spend it where you differentiate, not on where the close button goes.

Where this gets misused: "be consistent" is not "be uniform". Consistency is about meeting expectations, not about forcing one component to serve two different jobs.

### 5. Error prevention

The best error message is the one that never fires. Remove error-prone conditions, or catch them before commit.

Two kinds of error, and they need different fixes. Slips are unconscious, caused by inattention during a familiar task, and you prevent them with constraints, good defaults, and generous targets. Mistakes are conscious, caused by a mismatch between someone's mental model and your system, and you prevent them with clearer models, better labels, and preview.

Practical moves: constrain input types instead of validating after the fact, default to what most people pick, separate destructive actions from adjacent safe ones, and never put "Delete" where "Duplicate" was yesterday.

### 6. Recognition rather than recall

Make actions, options, and information visible instead of asking people to remember them across screens.

This is the rung 3 carried-state score from the main skill. Anything a person copies down, memorizes, or re-derives after a navigation is a defect with a measurable cost.

Application surfaces fail this constantly: an ID shown on one screen and required on another, a filter that resets on back, a wizard that forgets what was entered in step two.

### 7. Flexibility and efficiency of use

Serve the novice and the expert with the same interface by layering accelerators on top of the obvious path.

Keyboard shortcuts, bulk actions, saved views, command palettes, sensible personalization. The rule is that the accelerator must be discoverable but never required, so the visible path always works and the fast path rewards learning.

On a daily-use Application, this is the difference between a tool people like and one they tolerate. On a once-a-year Transaction, it barely matters and can add clutter. Weigh by visit frequency.

### 8. Aesthetic and minimalist design

Every extra unit of information competes with the relevant ones and lowers their visibility.

This does not mean flat, sparse, or fashionable. It means everything on screen earns its place. On a dense Application surface the right question is not "how many elements" but "is this density resolved" through alignment, consistent gutters, and one rhythm per column type. A two hundred row table can pass this heuristic easily. A marketing page with four competing calls to action fails it.

### 9. Help people recognize, diagnose, and recover from errors

Say what went wrong in plain language, say precisely where, and offer the way out.

An error message needs three things: cause in their terms, location as close to the problem as possible, and a next action. Codes belong in a copyable detail line for support, never as the whole message. Avoid blame and avoid interjections, since "Oops!" reads as insincere to someone who just lost work.

"That password is too short" is worse than "Use at least 8 characters." One reports, the other resolves.

### 10. Help and documentation

Best case, nothing needs explaining. When it does, put help in context at the moment of need rather than in a manual nobody opens.

People start using software immediately and skip the tutorial, reliably and across decades. Design for that: inline hints, empty states that teach, and searchable task-shaped docs rather than feature-shaped docs.

## Behavioral laws worth knowing

Shorthand for effects that show up repeatedly. Use them to explain a decision, not to win an argument. Names come from the Laws of UX collection; this section keeps the ones you reach for mid-conversation, and `laws-of-ux.md` carries all thirty in full with origins and misuse notes.

**Jakob's law.** People spend most of their time on other products, so they expect yours to work like those. The strongest argument for convention there is.

**Hick's law.** Decision time rises with the number and complexity of choices. Applies to menu length, plan tables, and form option counts. Note the catch: the effect is about equally-weighted choices being scanned, so a long list of familiar, well-grouped items is not the same as five unfamiliar ones.

**Fitts's law.** Time to hit a target is a function of distance and size. Make important and frequent targets bigger and closer, keep destructive targets away from frequent ones, and remember that screen edges and corners are effectively infinite targets on desktop.

**Miller's law.** Often quoted as seven plus or minus two, which is the part people get wrong. Miller's point was chunking, and modern working memory estimates are closer to three or four items. Design for three to five chunks, not seven.

**Doherty threshold.** Productivity climbs when the system responds fast enough that neither party waits on the other, roughly under 400ms. Below that people stay in flow. Perceived performance counts, so optimistic UI and skeleton states buy you real time.

**Peak-end rule.** People judge an experience by its most intense moment and its ending, not by the average. Budget craft accordingly: the confirmation screen, the first successful result, and the error you cannot avoid deserve more attention than the middle of a flow.

**Serial position effect.** First and last items in a series are best remembered. Put the most important navigation items at the ends.

**Von Restorff effect.** The item that differs is the one remembered. This is why exactly one primary action per state works and why two primary buttons cancel each other out.

**Goal-gradient effect.** Motivation increases with proximity to the goal, which is why progress indicators and pre-filled steps improve completion. This is also the effect most often weaponized, so keep the progress honest.

**Zeigarnik effect.** Unfinished tasks stay in memory. Useful for resumable flows and saved drafts. Manipulative when used to nag.

**Postel's law.** Be liberal in what you accept and conservative in what you send. Accept phone numbers with spaces, dates in several formats, and pasted values with stray whitespace. Normalize on your side, silently.

**Tesler's law.** Every system has irreducible complexity. The only question is who absorbs it, the user or the system. Absorb it in the system whenever you can, and when you cannot, be honest about where it landed.

**Aesthetic-usability effect.** People perceive attractive designs as more usable and tolerate small problems in them. Two consequences: presentation quality drives perceived trust before a single argument is read, and good looks can hide real problems during testing. Fix presentation when trust metrics are poor, and never let a pretty prototype substitute for a task success number.

**Paradox of the active user.** People start using software immediately rather than reading instructions, even when reading would be faster. Stop fighting it, design for it.

**Occam's razor.** Among designs that perform equally, take the one with fewer assumptions and fewer parts.

**Pareto principle.** Roughly 80 percent of use comes from 20 percent of features. Find your 20 percent and make it excellent before touching the rest.

**Parkinson's law.** Work expands to fill the time available. In interfaces this shows up as flows that feel longer when they are given more room, which is why a shorter perceived path can beat a technically identical longer one.

**Selective attention.** People filter to what serves their current goal and genuinely do not see the rest. Banner blindness is this, not stupidity. If something must be seen, it has to sit in the goal path, not beside it.

## Gestalt grouping

How people parse a layout before reading a word of it. These do the work that borders and labels otherwise have to do.

- **Proximity.** Things near each other read as related. The single highest-leverage tool you have. Most "cluttered" screens are actually spacing failures, not content failures.
- **Common region.** A shared bounded area groups items even when they are far apart. Cards work because of this.
- **Similarity.** Items sharing shape, color, or size read as one class. Which is why a non-clickable element styled like a button is a real bug.
- **Uniform connectedness.** Visually connected elements read as most related of all, stronger than proximity or similarity. Lines, containers, and connectors.
- **Prägnanz.** People resolve ambiguous or complex forms into the simplest interpretation available, because it costs the least. Ambiguity gets resolved whether or not you intended a meaning.

Practical use: before adding a divider or a border, try changing spacing. Before adding a container, try alignment. Add ink last.

## Interface writing

Words are interface. Most "confusing UI" is confusing copy.

**Voice, then tone.** Voice is constant and comes from what the product is for. Tone shifts with the moment. The same product should sound calm and direct during a failure and warm when someone hits a milestone. Write a short list of your common terms and reuse them, because inconsistent vocabulary is a usability defect, not a style quibble.

**Labels.** Use a verb for anything that acts. Prefer the specific verb over the generic one, so "Send invite" beats "Submit" and "Save draft" beats "OK". Avoid clever labels in functional positions.

**Be concise, not terse.** Cut every word that does not change meaning. Do not cut the words that carry the meaning.

**Possessives and pronouns.** "Favorites" says what "Your favorites" says, in less space. Pick one convention and hold it. Avoid "we" entirely, especially in errors: "Unable to load content" beats "We're having trouble loading this content", because nobody knows who "we" is or what they are doing about it.

**Capitalization.** Pick sentence case or title case per element type and apply it everywhere. Sentence case reads as more casual and is easier to localize. Being consistent matters more than which one you pick.

**Empty states.** Explain what belongs here and give the first action. "No data" is a failure. This is the highest-leverage and least-designed surface in most products, since it is a person's first impression of a feature and their only chance to learn it in context.

**Error messages.** Cause, location, next action. Plain language, no codes as the headline, no blame, no interjections. If a single error affects many people, that is a design problem to fix rather than a message to word better.

**Placeholder and hint text.** Show the expected format ("name@example.com") and never use placeholder text as the only label, since it disappears exactly when someone needs it and screen readers treat it inconsistently.

**Multi-step flows.** Decide the vocabulary once. Get started to begin, Continue or Next through the middle, Done at the end. Do not swap synonyms mid-flow.

**Settings.** Describe what the setting does when it is on, and let people infer the off state. If the label is not enough, add one line of description rather than making the label longer.

**Device wording.** Say tap on touch, click on pointer, select when it could be either or when a keyboard or switch is in play. Never describe a gesture as the only way to do something.
