# Visual craft

Read this when building or reviewing the look of something: type, color, spacing, layout, motion, tokens, and the states everyone forgets.

This file gives you a defensible default, not a house style. When a project has its own design file or brand guide, that wins and you follow it. Use this to fill gaps and to judge whether what exists is internally consistent.

## Where craft comes from

People read easy-to-process interfaces as more trustworthy and more usable, so visual consistency is doing work on the trust metric before anyone reads a word. It also means near-miss inconsistency costs more than obvious difference: a spacing value three pixels off the scale reads as sloppy in a way that a deliberately different value does not, because perception is sharpest at small differences.

The practical version: pick a small set of values, use only those values, and let repetition do the work.

## Type

**Families.** Two at most. One is fine. A common split is a display or brand face for headings and a system face for body copy, since system faces are drawn for legibility at small sizes and get platform text features for free.

**Scale.** Use a ratio rather than picking numbers by feel. A minor third (1.2) suits dense interfaces, a major third (1.25) is a reliable general default, and a perfect fourth (1.333) suits editorial layouts. Round to whole pixels. A workable default set:

| Role | Size | Line height | Weight |
|---|---|---|---|
| Display | 48 | 1.1 | 600 to 700 |
| H1 | 32 | 1.2 | 600 |
| H2 | 24 | 1.3 | 600 |
| H3 | 20 | 1.4 | 600 |
| Body | 16 | 1.5 | 400 |
| Small | 14 | 1.45 | 400 |
| Caption | 12 | 1.4 | 400 or 500 |

**Line height.** Roughly 1.5 for body text, tighter as size grows, looser for long-form reading and for wide columns. Three or more lines of text should never get tight leading.

**Measure.** 45 to 75 characters per line for body copy. Past that, people lose their place returning to the next line. Set a max-width on prose containers rather than letting them fill the viewport.

**Weight.** Regular, medium, semibold, and bold cover almost everything. Skip ultralight and thin below display sizes, since they lose legibility fast at small sizes and in bright light.

**Hierarchy.** Change one variable at a time where you can. Size, weight, color, and spacing are all levers, and using all four at once produces noise. If everything is emphasized, nothing is.

**Alignment.** Left-aligned for Latin scripts, and mirror for right-to-left languages. Center headings if you like, never center a paragraph. Align a paragraph to its own language rather than to the surrounding context, so an English paragraph inside an Arabic page stays left-aligned.

**Numbers.** Use tabular figures for anything in a column. Never reverse the digit order of a number when mirroring a layout, since numbers read the same way everywhere.

## Color

**Structure the palette semantically, not by hue.** You want roles, not swatches: surface levels, content levels, borders, interactive, and status. Name them by job so a theme swap does not require touching a component.

A workable minimum set:

- Surface: base, raised, sunken, overlay
- Content: primary, secondary, tertiary, disabled, on-accent
- Border: subtle, default, strong, focus
- Interactive: accent plus hover, active, and disabled variants
- Status: success, warning, danger, info, each with a surface and a content variant

**One accent, used sparingly.** Reserve full accent saturation for the primary action and for status. If every control is tinted, nothing stands out and control labels get harder to read against colorful content.

**Never let color be the only signal.** Pair it with an icon, a label, or a shape. Also check what your palette means in the markets you serve, since a rising line is green in some places and red in others.

**Light, dark, and increased contrast are three designs, not one.** Do not derive dark mode by inverting. Dark surfaces need less saturated accents and different elevation cues, since shadows barely read on dark backgrounds and you use surface lightness instead. Check contrast separately in every mode.

**Prefer system-defined colors on native platforms.** They already have accessible and high-contrast variants, and they adapt to platform appearance changes without you doing anything. Do not hard-code the documented values, since they shift between OS releases. Use the API.

**Color management.** Apply color profiles to images, and use sRGB when in doubt. Wide-gamut P3 is worth it for photography and rich media, with the caveat that two similar P3 colors can be hard to tell apart on an sRGB display, and P3 gradients can clip.

## Spacing and layout

**One scale, no exceptions.** A 4 point base with a 4, 8, 12, 16, 24, 32, 48, 64, 96 ramp covers almost everything. Android lays out on an 8 dp rhythm for the same reason. If a value is not on the scale, it is a bug, not a decision.

**Proximity is your primary grouping tool.** Related things get less space, unrelated things get more. Reach for spacing before you reach for a border or a card, because ink is expensive and space is free.

**Grid.** A 12 column grid is flexible enough for most layouts. What matters more than the column count is that gutters and margins come from the same scale as everything else.

**Breakpoints.** Design for a handful of width classes rather than devices, since the device list never stops growing. Two common systems:

| System | Classes |
|---|---|
| Material window size classes | Compact under 600 dp, medium 600 to 840, expanded 840 to 1200, large 1200 to 1600, extra-large 1600 and up |
| Common web set | 640, 768, 1024, 1280, 1536 |

Start with one breakpoint and add more only when a layout genuinely breaks. Test at the resize boundaries and at both extremes first, since that is where the bugs live.

**Adaptivity is not just width.** Handle orientation, resizable windows, external displays, text size changes, and right-to-left layout. Defer switching to a compact layout as long as possible when a window shrinks, since stability is worth more than optimality. For a complex layout, hide the tertiary column (inspectors, filters) before restructuring the primary content.

**Safe areas and edges.** Respect platform-defined safe areas, since that is what keeps content clear of notches, camera housings, home indicators, and rounded corners. Extend backgrounds to the edges while keeping content inside the safe area. On TV, inset content well from the edges, since overscan and viewing distance both cut in.

**Reading order.** People scan top to bottom and leading to trailing, so the most important thing goes near the top and the leading edge. Reading order flips for right-to-left languages, and so should your layout, but not your logos, photographs, universal marks like a checkmark, or icons of real-world objects like clocks.

## Density

Density is a decision, not a default, and it should follow the surface class.

- Comfortable for Acquisition, mobile, and anything used occasionally.
- Compact for Application surfaces used all day by experts. Cutting row height in a table from 48 to 32 pixels can be a genuine productivity win.
- Offer a density toggle when both audiences exist in the same product.

The rule to hold onto: dense is fine, unresolved is not. A dense table passes when alignment is strict, gutters are consistent, and each column type has one rhythm (numbers right-aligned and tabular, text left-aligned, status in a consistent position).

## Elevation and depth

Use depth to communicate layering, not to decorate. Define a small set of levels and stick to it: base, raised (cards), overlay (dropdowns, popovers), modal, and toast. Each level gets one shadow value and one surface value.

On light backgrounds, shadow carries the layering. On dark backgrounds, shadow barely reads, so use surface lightness instead. On platforms with a system material such as glass or blur, let the system handle the effect rather than baking your own highlights and shadows into assets, since custom effects are static and system effects respond to context.

## Motion

Motion should explain what happened, not perform.

**Durations.** 100 to 150 ms for small state changes such as hover and toggle, 200 to 300 ms for entrances, exits, and layout shifts, 300 to 500 ms for large transitions covering a lot of screen. Anything over 500 ms had better be doing real work, since past that people start waiting on you.

**Easing.** Ease-out for things entering, ease-in for things leaving, and a standard ease-in-out for things moving within the view. Pick one curve per class of motion and reuse it. Timing is a token, same as color.

**What to animate.** Transform and opacity, because they are cheap. Avoid animating layout properties in loops.

**What not to animate.** Anything that delays a person who already knows what they want. Anything decorative that repeats. Anything that moves in peripheral vision while someone is reading.

**Reduced motion.** Honor the setting. Replace movement with fades, cut bounce, avoid depth changes, and never animate into or out of a blur.

## Iconography

One family, one grid, one stroke weight, one optical size ramp. Icons carrying meaning need a text label unless the symbol is genuinely universal, and "genuinely universal" is a much shorter list than designers think (search, close, play, back). Match icon weight to adjacent text weight. Keep interactive icons at the platform minimum target size even when the glyph itself is small, using padding.

Mirror directional icons for right-to-left layouts, and do not mirror logos, universal marks, tools, or objects like clocks.

## Design tokens

Tokens are the mechanism that makes coherence maintainable. Three layers, and the layering is the whole point:

1. **Primitive.** Raw values with descriptive names. `blue-600`, `space-4`, `radius-2`.
2. **Semantic.** Roles that point at primitives. `color-surface-raised`, `color-content-primary`, `space-inset-md`.
3. **Component.** Component-specific names that point at semantic tokens. `button-primary-background`.

Components reference semantic tokens, never primitives. That is what lets you re-theme, ship dark mode, or rebrand without touching component code. Keep one source of truth and generate the platform outputs from it (CSS custom properties, Swift, Kotlin, Figma variables) rather than maintaining them separately.

If you are starting a design system, do tokens first, then a handful of components, then documentation about when to use each one. A system with three well-documented components beats one with forty undocumented ones.

## The states everyone forgets

Design these explicitly, or they will be designed by accident. Score each on three questions: where am I, why is this happening, what do I do next.

- **Empty.** Explain what belongs here and offer the first action. Not "No data". For a filtered list, distinguish "nothing here yet" from "nothing matches your filter", and offer to clear the filter in the second case.
- **First run.** The genuine first impression on an Application surface. Nobody reads the tour, so teach inside the task.
- **Loading.** Match the geometry of the loaded state so nothing jumps. Use skeletons where the shape is known. For long operations report real progress rather than motion. Do not swap a spinner for content of a different height.
- **Partial.** Some content arrived and some has not. Say which is which rather than blocking everything on the slowest request.
- **Error.** Cause, location, next action. Always a route forward.
- **Offline or stale.** Mark what is stale, say what was preserved, and say what happens when the connection returns.
- **Permission denied.** Say who can grant access, not just that the person lacks it.
- **Destructive confirm.** State the blast radius specifically, or replace it with undo.
- **Success.** Confirm what happened, where the thing went, and what a person can do next. This is a peak-end moment and it is usually wasted.

Nothing should reflow between these states. Same container, same geometry, different content.

## Data visualization

- Pick the chart from the question. Trend over time is a line. Comparison across categories is a bar. Part-to-whole with few parts is a stacked bar, and pie charts stop working past about three slices. Correlation is a scatter.
- Label directly on the series when you can, since a legend makes people look away and match colors from memory.
- Never truncate a bar chart axis. Truncating a line chart axis is sometimes legitimate but say so on the chart.
- Order categorical bars by value unless there is a natural order such as days of the week.
- Keep the palette to six series or fewer. Past that, aggregate or split into small multiples.
- Never encode meaning in color alone. Add labels, direct annotation, or pattern.
- Check colorblind safety, and check the chart in grayscale.
- Say what the takeaway is in a sentence next to the chart. A chart with no stated conclusion is a puzzle you handed someone.
