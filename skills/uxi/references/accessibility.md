# Accessibility

Read this whenever you are auditing, building, or specifying anything people will use. This is rung 1 of the ladder, so nothing above it counts while this is broken.

Framing that works better than "compliance": you are removing single points of failure. An interface that only works through sight, only through a mouse, or only through fine motor control has one point of failure per channel. Everything here also helps people with no disability at all, on a cracked screen, in sunlight, one-handed, on a train.

## How WCAG is structured

Web Content Accessibility Guidelines 2.2 became a W3C Recommendation in October 2023. Four principles, thirteen guidelines, and a set of testable success criteria at three levels.

The four principles, usually shortened to POUR:

- **Perceivable.** Information has to be available to at least one sense that the person has.
- **Operable.** Every function has to be reachable by more than one input method.
- **Understandable.** Content and behavior have to be predictable.
- **Robust.** It has to keep working with assistive technology and future user agents.

Levels: A is the floor, AA is the practical target and what most laws reference, AAA is not expected across a whole product but is worth adopting selectively. Target AA. Adopt individual AAA criteria where the consequence of failure is high.

WCAG 2.2 added nine criteria over 2.1 and removed 4.1.1 Parsing as obsolete. The nine:

| Criterion | Level | What it requires |
|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | A focused element is not entirely hidden by your own content, such as a sticky header or cookie bar |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | No part of the focused element is hidden |
| 2.4.13 Focus Appearance | AAA | The focus indicator is large enough and contrasts enough to see |
| 2.5.7 Dragging Movements | AA | Anything you can drag can also be done with a single pointer action |
| 2.5.8 Target Size (Minimum) | AA | Targets are at least 24 by 24 CSS pixels, with defined exceptions for spacing, inline text links, and browser-controlled elements |
| 3.2.6 Consistent Help | A | Help is in the same place on every page where it appears |
| 3.3.7 Redundant Entry | A | Do not make people re-enter information they already gave you in the same process |
| 3.3.8 Accessible Authentication (Minimum) | AA | Login does not require a cognitive function test such as solving a puzzle, transcribing, or recalling |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | Same, with fewer exceptions |

If you conform to 2.2 you also conform to 2.1 and 2.0.

## The numbers you will be asked for

### Contrast

| Content | Minimum ratio (AA) |
|---|---|
| Body text under 18pt (24px) regular | 4.5:1 |
| Large text, 18pt (24px) regular or 14pt (18.66px) bold and up | 3:1 |
| UI component boundaries, icons carrying meaning, focus indicators, chart elements | 3:1 |
| Decorative graphics, disabled controls, logos | No requirement |

AAA raises body text to 7:1 and large text to 4.5:1. Worth adopting for long-form reading, for anything used outdoors, and for anything used by an older population.

Check both light and dark themes separately, since a palette that passes in one often fails in the other. Also check the increased-contrast system setting if your platform has one. Apple's guidance for its platforms follows the same thresholds: up to 17pt needs 4.5:1, 18pt needs 3:1, and bold text at any size needs 3:1.

Do not rely on color alone to carry meaning anywhere. Add an icon, a shape, a label, or a pattern. Red-green and blue-orange pairings are the common traps, and error states are the common failure.

### Target size and spacing

| Platform | Recommended | Minimum |
|---|---|---|
| WCAG 2.2 AA (web, 2.5.8) | 44 by 44 for AAA | 24 by 24 CSS px |
| iOS and iPadOS | 44 by 44 pt | 28 by 28 pt |
| watchOS | 44 by 44 pt | 28 by 28 pt |
| macOS | 28 by 28 pt | 20 by 20 pt |
| tvOS | 66 by 66 pt | 56 by 56 pt |
| visionOS | 60 by 60 pt | 28 by 28 pt |
| Android and Material | 48 by 48 dp | 48 dp, laid out on an 8 dp rhythm |

Spacing matters as much as size. Around 12 pt of padding works for elements with a visible bezel and around 24 pt for elements without one. Adjacent destructive and safe actions need more separation than the minimum, not less.

### Type

| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

On the web, 16px is the practical floor for body text and never set a fixed size that blocks the browser zoom. Support text enlargement to at least 200 percent (140 percent on watch-class devices) without loss of content or function. Avoid ultralight, thin, and light weights for anything small, and if you must use a thin weight, size up.

## The checks, in the order I would run them

### 1. Keyboard alone

Unplug the mouse. Tab through the whole screen.

- Every interactive element is reachable and every one is actionable with Enter or Space.
- Focus is always visible and never obscured by sticky headers, footers, chat widgets, or cookie bars.
- Focus order follows the visual order.
- No keyboard trap: you can always tab out of any component, including embedded players and third-party widgets.
- Modals trap focus while open, return focus to the trigger on close, and close on Escape.
- Skip link to main content exists and works.
- Custom controls respond to the keys their native equivalents do, so a custom select handles arrows, Home, End, and type-ahead.

This one test catches more real defects than any automated tool.

### 2. Structure and semantics

- Headings are a real, ordered outline. One h1, no skipped levels, no headings used for visual size.
- Landmarks are present: header, nav, main, footer, and named regions when there is more than one of a kind.
- Lists are lists, tables are tables with proper header cells and scope, buttons are buttons and links are links. A div with a click handler is a defect.
- Every input has a programmatically associated label. Placeholder text is not a label.
- Images have alt text that serves the purpose: describe the content if it carries meaning, leave it empty if it is decoration, describe the destination if it is a link.
- Page and view titles are unique and say where you are.
- Language is declared, and changes of language within a page are marked.

### 3. Screen reader pass

Run one real screen reader end to end on the primary task: VoiceOver on macOS or iOS, NVDA on Windows, TalkBack on Android.

Listen for: unlabeled buttons announced as "button", state that is not announced (expanded, selected, checked, current), dynamic changes that pass silently (use a live region), reading order that does not match visual order, and duplicate or noisy announcements from decorative content.

### 4. Motion, timing, and media

- Respect reduced motion. When it is on, cut automatic and repetitive animation, avoid z-axis depth changes, and swap movement for fades. Track gestures directly rather than animating loosely.
- Nothing flashes more than three times per second, ever.
- No auto-playing audio or video without a control to stop it.
- No content that auto-dismisses on a timer unless the person can extend or turn it off. This hurts anyone who reads slowly or navigates with assistive technology.
- Video has captions, audio has transcripts, and anything conveyed visually in video has an audio description or an equivalent in text.
- Pair audio cues with a visual cue and, where the platform supports it, a haptic one.

### 5. Forms

Forms are where accessibility failures cost the most, because they sit on the transaction path.

- Labels are visible and persistent, not placeholder-only.
- Errors are announced, tied to the field, and stated in plain language with a fix.
- Required fields are marked in text, not only with a red asterisk.
- Autocomplete attributes are set for name, email, address, and payment fields. That attribute is how browsers and assistive tech know what a field is, so treat it as an accessibility requirement as much as a convenience.
- Do not require re-entering information already given earlier in the same process.
- Do not require a cognitive test to log in. Support password managers and passkeys, allow paste, and never block it.
- Give enough time, and if there is a session timeout, warn and allow extension.

### 6. Cognitive load

The least automated and often the most impactful.

- Use plain language. Aim around a lower secondary reading level for consumer content, and simplify sentences before simplifying vocabulary.
- Keep interactions simple and consistent. Prefer familiar system gestures to custom ones.
- Always give an alternative to any gesture, so a swipe-to-delete also has a visible delete.
- Break long tasks into single-idea steps, and let people save and resume.
- Confirm twice for anything hard to recover from in simplified modes.
- Be consistent about where help lives.

## Testing, honestly

Automated tools (axe, Lighthouse, Accessibility Inspector, WAVE) catch roughly a quarter to a third of issues. They are worth running in CI because they catch regressions cheaply, but a passing automated score means very little on its own. Everything in the keyboard, screen reader, and cognitive sections above needs a human.

A workable cadence: automated checks in CI on every build, a keyboard pass in every pull request that touches UI, a screen reader pass before release on the primary flows, and testing with disabled people on anything high stakes. There is no substitute for the last one. Persona-based simulation is a rehearsal, not a result.

## Common failures, ranked by how often I see them

1. Focus indicator removed in CSS, usually by an `outline: none` that nobody replaced.
2. Div or span with a click handler instead of a button.
3. Placeholder text used as the label.
4. Color as the only signal for state, especially validation.
5. Custom dropdowns and modals built without keyboard support.
6. Icon-only buttons with no accessible name.
7. Sticky headers covering the focused element.
8. Text in images, which does not scale, translate, or get read.
9. Contrast that passes in light mode and fails in dark.
10. Auto-dismissing toasts carrying information that appears nowhere else.

## Beyond WCAG

Conformance is the floor, not the goal. A page can pass every criterion and still be miserable to use with a screen reader. When you are choosing between a technically conformant option and a genuinely usable one, take the usable one and document why.

If your platform offers accessibility disclosure to users, such as the App Store's accessibility labels, fill it in accurately. Overclaiming is worse than not claiming.
