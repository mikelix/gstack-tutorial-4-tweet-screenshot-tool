# Design Review 4.1 — Design Directions

```
Status:   CONCEPT ONLY — NOT IMPLEMENTED
Scope:    three distinct product-interface directions, rendered as
          disposable HTML/CSS mockups and screenshotted, not built
          against production code
Sources:  docs/DESIGN_REVIEW_4_1_CURRENT_STATE.md (evidence + diagnosis)
```

All three directions differ in **product interaction and hierarchy**, not
merely color — see each direction's "Information architecture" and
"Navigation model" for the structural difference. Concept files:
[`docs/design-review-4.1/concepts/`](design-review-4.1/concepts/) (`a-*.html`,
`b-*.html`, `c-*.html`); rendered screenshots in the same folder.

---

## Direction A — Quiet Creator Tool

**1. Name:** Quiet Creator Tool

**2. One-sentence concept:** A restrained, editor-like utility where the
tweet preview is the unambiguous hero and every control earns its place —
closest in spirit to a mature, professional creator tool.

**3. Target user behavior:** Arrive with a specific tweet already in mind,
paste it, adjust one or two settings, export. Optimized for a confident,
returning user as much as a first-timer.

**4. Information architecture:** Flat, two-state (empty → loaded). No
onboarding layer, no examples-first detour. Header shell → primary input
→ (on load) two-column editor.

**5. Desktop layout:** `a-desktop-empty.png` / `a-desktop-loaded.png` —
centered content column on arrival (max-width, not full-bleed like
today); on load, a two-column grid: preview card left (~65%), inspector
panel right (~35%), export bar centered below the preview.

**6. Mobile layout:** `a-mobile-loaded.png` — single column, preview
first, inspector stacks below as a bordered card, export actions become
a **sticky bottom bar** (Download PNG as a full-width primary button,
Copy image / Copy share link as smaller secondary text beside it).

**7. Navigation model:** A segmented control (`Single Tweet | Thread`) in
the header shell, present on every page — this alone fixes the Thread
discoverability finding from the current-state review.

**8. Empty state:** Large headline + one-line subhead, single input +
primary button, a quiet "Try an example instead" text link below it (not
emphasized — this direction deliberately does *not* lead with a demo; see
Direction B for that hypothesis).

**9. Loaded state:** Editor-style two-column layout; preview in a bordered
card, inspector in a matching bordered card, restrained borders instead of
shadows or gradients on the chrome itself (the tweet card's own gradient
background is the one place color is allowed to be expressive).

**10. Customize experience:** Grouped fields with uppercase micro-labels
(Background / Padding / Export scale / Theme), swatches as rounded squares
with a visible selected-state ring, sliders and segmented buttons styled
consistently — same controls as today, meaningfully better presented.

**11. Export hierarchy:** One filled primary button ("Download PNG"), two
plain-text secondary links beside it — visually unambiguous which action
is the normal completion path.

**12. Thread-mode treatment:** A first-class, always-visible nav item, not
a separate unlinked page.

**13. Visual language:** Off-white background, white surface cards, thin
neutral borders (`#e5e5e3`), a single blue accent (`#1d4ed8`) used
sparingly — for the primary button, the focus ring, and the selected
swatch/segment state only.

**14. Typography approach:** One system sans-serif family throughout;
a distinct display size for the headline (38px, tight tracking), a
smaller consistent body size (14–16px), uppercase micro-labels (12px,
letter-spaced) for field groups — three or four sizes total, not a large
scale.

**15. Spacing philosophy:** Generous but not empty — comfortable padding
inside cards (20–28px), consistent gaps between fields (22px), page
margins that keep content readable at wide viewports instead of
stretching it edge to edge.

**16. Surface/border/shadow philosophy:** Borders over shadows. Flat
white/off-white surfaces with a 1px neutral border define every
container; the only shadow in the whole interface is the tweet card's own
drop shadow inside its gradient background, which already exists in
production and is worth keeping.

**17. Primary CTA:** "Create" (empty state) / "Download PNG" (loaded
state) — a single filled button at each stage, always the same accent
color.

**18. Secondary actions:** "Try an example," "Copy image," "Copy share
link," the Single/Thread switch, "Change" (to edit the URL after loading)
— all rendered as lighter-weight text or outline-style controls.

**19. Advantages:** Lowest implementation risk of the three (mostly CSS
and layout restructuring on the existing DOM shape); immediately fixes
the two most severe current-state findings (hierarchy, thread
discoverability) without inventing new product concepts; easiest to reason
about for accessibility since it's the closest to today's actual markup.

**20. Risks:** Doesn't address the cold-start "no evidence of output
quality" problem as directly as Direction B — a skeptical first-time
visitor still has to act on faith before seeing a result.

**21. Implementation complexity:** Low–medium. Primarily component styling
and a new header shell; no new client-side state beyond what already
exists (tweet ID, style state, thread state are all unchanged).

**22. What existing code could remain unchanged:** All backend/API routes,
`export-image.ts`, `media-hosts.ts`, `tweet-url.ts`, `style-state.ts`,
`thread-state.ts` — this direction is a presentation-layer restyle of the
existing component tree, not a rearchitecture.

---

## Direction B — Instant Demo / Product-Led

**1. Name:** Instant Demo / Product-Led

**2. One-sentence concept:** Show the value before asking for anything —
a pre-rendered example output is visible the instant the page loads, so
comprehension and trust are established before the user types a single
character.

**3. Target user behavior:** Arrive skeptical or unfamiliar with the
product, see a finished example immediately, and either try that exact
example (lowest-friction possible first action) or paste their own link
having already seen proof the output looks good.

**4. Information architecture:** Three-tier arrival: headline → live
example card (not interactive, just shown) → dual entry point ("paste
your own" input, or "try this example" button). This is a genuine
structural difference from Direction A, not a re-skin — it inserts an
entire proof-of-value layer before the primary input that Direction A
intentionally omits.

**5. Desktop layout:** `b-desktop-empty.png` / `b-desktop-loaded.png` — a
centered, dark-themed hero with the example card presented inside its own
bordered "demo" panel, labeled explicitly ("Live example — try it
below"); on load, the same two-column editor as Direction A, so the
*loaded* experience converges with A once the user is past the cold
start.

**6. Mobile layout:** `b-mobile-loaded.png` — identical stacking approach
to Direction A (preview → inspector → sticky bottom export bar), dark
theme carried through.

**7. Navigation model:** Same segmented `Single Tweet | Thread` control
as Direction A.

**8. Empty state:** The example card *is* the empty state's centerpiece —
this is the direction's core hypothesis and its main point of difference.

**9. Loaded state:** Converges with Direction A's loaded layout (two-column
editor) — the directions differ primarily in the *arrival* experience, not
the working state, which is a deliberate scoping choice: don't reinvent
the part that already demonstrably works.

**10. Customize experience:** Same control set and grouping as Direction A,
restyled for the dark palette (outline buttons instead of filled-neutral,
since dark surfaces make filled light buttons read as heavier).

**11. Export hierarchy:** Identical pattern to Direction A — one filled
primary action, two secondary text actions.

**12. Thread-mode treatment:** Same always-visible nav switch as
Direction A.

**13. Visual language:** Deep near-black background (`#0b0b10`), dark
elevated surfaces (`#141420`) for cards, a violet accent (`#7c5cff`) —
distinctly different from Direction A's light, restrained palette, chosen
to read as more "product," less "internal tool," and to make the example
card's own gradient pop harder against a dark canvas.

**14. Typography approach:** Similar scale to Direction A but slightly
tighter/denser headline treatment; an explicit small-caps "LIVE EXAMPLE"
eyebrow label above the demo card, a pattern this direction introduces
that A doesn't need.

**15. Spacing philosophy:** Similar to A once loaded; the empty state is
intentionally denser (headline, demo, input, and a "try example" button
all visible without scrolling at 900px height) because it has more to
communicate before the first interaction.

**16. Surface/border/shadow philosophy:** Elevated dark cards with a
visible border and a stronger shadow under the demo card specifically
(it's meant to look like a physical object sitting above the page), same
flat-border approach as A for the inspector once loaded.

**17. Primary CTA:** "Create" alongside a secondary "Try this example
tweet" affordance on the empty state — genuinely two entry points, which
is this direction's main product bet.

**18. Secondary actions:** Same export/thread/change-URL set as Direction A.

**19. Advantages:** Most directly answers the five-second test's weakest
finding (no evidence of output quality on arrival) and the Phase 6
cold-start problem by name; likely the strongest first-time comprehension
of the three, in principle — see Evaluation Matrix for why this is stated
as a hypothesis, not a fact.

**20. Risks:** The demo card needs real, safe, neutral sample content
decided on and possibly kept in sync with the real component (risk of the
static demo drifting visually from the actual live renderer over time);
dark theme is a bigger visual departure from the current product, which
carries more subjective-taste risk in review.

**21. Implementation complexity:** Medium. Needs a static or lightly
componentized example render on the landing view in addition to
Direction A's layout work — more new surface area than A, though the
loaded state reuses the same components.

**22. What existing code could remain unchanged:** Same backend/export/
proxy/state files as Direction A. The example card can be built from the
same `TweetCanvas` component with a hardcoded/mock tweet object, meaning
even the new surface area mostly reuses existing rendering code rather
than inventing a new one.

---

## Direction C — Canvas-First Creator Workspace

**1. Name:** Canvas-First Creator Workspace

**2. One-sentence concept:** Treat the product like a lightweight design
tool — a large, centered, dominant canvas with a compact inspector rail
and a persistently accessible floating export action, rather than a
form-with-a-preview.

**3. Target user behavior:** Optimized for a repeat or power user who
treats this as a small creative tool they return to, not just a one-shot
utility — closer to opening a design file than filling out a form.

**4. Information architecture:** Workspace-first, not form-first. The
"empty state" is framed as "start a new canvas," and the header shell is
compact (52px), closer to an application toolbar than a marketing page
header — a genuinely different mental model from A and B's "page with a
form" framing.

**5. Desktop layout:** `c-desktop-empty.png` / `c-desktop-loaded.png` —
full-height, full-width dark canvas with a dotted background texture, a
narrow (280px) right-hand inspector rail, and a floating pill-shaped
export control anchored to the bottom-center of the canvas rather than
below the preview in-flow.

**6. Mobile layout:** `c-mobile-loaded.png` — canvas becomes a fixed-height
region up top, inspector rail becomes a horizontal wrapping row of fields
below it, floating export pill stays anchored to the canvas.

**7. Navigation model:** Same segmented switch, presented smaller/more
compact to match the toolbar-density header.

**8. Empty state:** A centered "start a new canvas" prompt with a `+`
icon tile — deliberately more like opening a new document in a creative
tool than a landing-page headline.

**9. Loaded state:** The tweet card floats on an open, textured canvas
rather than sitting inside a bordered container — the strongest sense of
"preview as hero" of the three directions, since nothing else on screen
competes with it for a container edge.

**10. Customize experience:** Same fields, denser presentation (smaller
type, tighter gaps, two-column field wrapping on mobile) — styled to feel
like a real inspector panel, not a settings form.

**11. Export hierarchy:** A distinct pattern from A/B: a floating pill
containing the primary "Download PNG" button plus two icon-only buttons
for copy-image / copy-link, persistently visible without scrolling
regardless of canvas content — this direction's answer to "export should
be persistently accessible."

**12. Thread-mode treatment:** Same nav switch; the canvas framing extends
naturally to a multi-card thread layout (not mocked here, but the
workspace metaphor scales to "multiple objects on a canvas" more
naturally than A/B's linear list).

**13. Visual language:** Charcoal/near-black canvas (`#1a1a1e`) with a
cyan accent (`#22d3ee`), dotted-grid canvas texture evoking design-tool
canvases (Figma/Canva-adjacent *in category*, not visually cloned).

**14. Typography approach:** Smaller base sizes throughout (11–15px) than
A/B, consistent with a denser, tool-like information density rather than
a marketing-page scale.

**15. Spacing philosophy:** Tight and functional — this direction
explicitly trades some breathing room for density, on the hypothesis that
a returning/power user values screen-efficiency over generous whitespace.

**16. Surface/border/shadow philosophy:** Strong shadow under the floating
canvas card and the floating export pill (both need to read as "floating
above" the canvas texture); the inspector rail uses a single left border
with no card treatment, more toolbar than form.

**17. Primary CTA:** "Load" (empty) / "Download PNG" inside the floating
pill (loaded) — same semantic action as A/B, different container.

**18. Secondary actions:** Icon-only copy-image / copy-link buttons in the
export pill — a real risk to name explicitly: icon-only controls need
labels for accessibility (addressed in Phase 14 below, not solved by the
concept mockup alone).

**19. Advantages:** Makes the preview maximally dominant; the persistent
floating export control means "how do I export" is answerable from
anywhere on the canvas, including after scrolling the inspector; the
workspace framing is the most natural fit if Thread mode later grows into
something closer to a real multi-object editor.

**20. Risks:** Furthest from the current implementation, so the highest
implementation and regression risk of the three; icon-only secondary
export actions need explicit accessible labels or they regress the
current (plain-text, self-describing) export links; a dark, dense,
tool-like aesthetic is a bigger departure that may read as *more*
intimidating to a first-time casual user, not less — this is a real
tension with Direction B's first-time-comprehension goal, worth weighing
explicitly rather than assuming density always reads as "premium."

**21. Implementation complexity:** Medium–high. Floating/absolute-positioned
export control, canvas texture, and rail-based inspector are all new
layout patterns relative to today's simple stacked/grid layout.

**22. What existing code could remain unchanged:** Same backend/export/
proxy/state files as A and B — this is still a presentation-layer
direction. The floating export control and canvas framing are new
components, but they wrap the same underlying export/copy/share logic
(`export-image.ts`) unchanged.

---

## Desktop comparison

| | A — Quiet Creator | B — Instant Demo | C — Canvas-First |
|---|---|---|---|
| Cold-start content | Headline + input only | Headline + live example + input | "Start a new canvas" prompt |
| Palette | Light, restrained | Dark, product-led | Dark, dense, tool-like |
| Preview container | Bordered card | Bordered card | Free-floating on open canvas |
| Export placement | Below preview, in-flow | Below preview, in-flow | Floating pill, canvas-anchored |
| Inspector | Right column, card | Right column, card | Right rail, toolbar-style |
| Density | Medium | Medium | High |

The meaningful difference is **not color** — it's *when the user first
sees evidence of output quality* (immediately in B, only after their own
first load in A and C) and *how persistent the export action is* (in-flow
in A/B, always-floating in C).

## Mobile comparison

All three solve the current-state horizontal-overflow bug and adopt a
single-column stack, but differ in what stays persistently visible while
scrolling:

- **A / B:** a sticky bottom bar keeps "Download PNG" reachable without
  scrolling back up, once a tweet is loaded.
- **C:** the floating export pill stays anchored to the canvas region
  itself rather than the viewport bottom — reachable as long as the
  canvas is in view, but not viewport-sticky the way A/B's bar is. This
  is a real, named tradeoff, not an oversight: C's canvas-anchored pill
  suits a shorter canvas region; a viewport-sticky bar would suit a
  taller one. Worth deciding explicitly if C is selected.

---

## Proposed design system (tokens + primitives)

One shared token *shape* across directions; values differ per direction's
palette (A = light, B/C = dark), shown here as the shape plus each
direction's actual values.

### Colors

| Token | A (light) | B (dark) | C (dark, denser) |
|---|---|---|---|
| `--bg` (page background) | `#fafafa` | `#0b0b10` | `#1a1a1e` |
| `--surface` | `#ffffff` | `#141420` | `#232327` |
| `--surface-elevated` | `#ffffff` + border | `#141420` + border | `#232327` + border |
| `--border` | `#e5e5e3` | `#26263a` | `#333338` |
| `--text-primary` | `#18181b` | `#f4f4f6` | `#f4f4f5` |
| `--text-secondary` | `#71717a` | `#9a9ab0` | `#8b8b93` |
| `--accent` | `#1d4ed8` | `#7c5cff` | `#22d3ee` |
| `--accent-hover` | `#1e40af` | `#6a48f0` | `#0891b2` |
| `--danger` | `#dc2626` | `#f87171` | `#f87171` |

`--success` omitted from all three — nothing in the current product
genuinely needs a distinct success color (export completion is
communicated by the browser's own download UI, not an in-app toast).

### Typography

| Token | Role |
|---|---|
| `display` | Empty-state headline (32–38px, tight tracking, 600–650 weight) |
| `page-title` | Product name in header shell (14–15px, 600 weight) |
| `body` | Standard copy, field values (13–16px, 400 weight) |
| `label` | Field group labels (11–12px, 600 weight, uppercase, letter-spaced) |
| `metadata` | Timestamps, secondary hints (11–12px, 400 weight, secondary color) |

### Spacing

A small coherent scale: `4 · 8 · 12 · 16 · 20 · 24 · 32 · 48` (px). Every
mockup above uses only values from this set.

### Radii

`small` = 6–7px (buttons, small chips) · `medium` = 8–10px (inputs,
inspector fields) · `large` = 12–16px (cards, the tweet preview container).

### Shadows

`subtle` = a 1px border, no blur — used for every default card in
Direction A and the inspector in B/C. `elevated` = a soft, larger blur
shadow — used only where something should read as floating above its
context (the tweet card's own background treatment in all three; the demo
card in B; the floating export pill in C).

### Interaction states

`hover` (slightly darker/lighter surface or accent), `focus` (2px accent
outline, 1px offset — carried through from the current product's already-
present default focus ring, just made intentional instead of default),
`active` (pressed, slightly darker accent), `disabled` (reduced opacity,
no pointer events), `loading` (the existing skeleton pattern, restyled to
match whichever direction is chosen, not replaced).

### Reusable primitives (not implemented yet)

`Button` (primary/secondary/icon variants) · `Input` · `Card` ·
`SegmentedControl` (used for Single/Thread and for Export-scale/Theme
toggles — one component, several instances) · `SectionLabel` · `Slider` ·
`Toast/status` (for the error state, replacing color-only red text with an
icon + text pattern) · `EditorPanel` (the bordered/rail container wrapping
the customize fields).

---

## Comparison matrix

Strengths and tradeoffs, not scores — see the Recommendation section of
the final report for a separate, explicit "test first" call.

| Criterion | A — Quiet Creator | B — Instant Demo | C — Canvas-First |
|---|---|---|---|
| Five-second comprehension | Improves hierarchy, but cold start still shows no output example | Directly targets this — hypothesis, not yet measured | Improves hierarchy; "start a canvas" framing may read as less immediately obvious to a first-timer than A's plain headline |
| Path to first successful export | Same number of steps as today, clearer at each step | One extra affordance ("try example") that could shorten perceived effort | Same step count as A; export is persistently reachable once loaded |
| Visual hierarchy | Strong improvement over current state | Strong improvement, plus an explicit proof layer | Strongest single-element dominance (the canvas), traded against overall density |
| Preview prominence | High | High | Highest — nothing else has a competing container edge |
| Thread discoverability | Fixed (nav switch) | Fixed (nav switch) | Fixed (nav switch) |
| Desktop clarity | High, familiar layout pattern | High, more novel arrival sequence | Most novel; clarity depends on user's familiarity with tool-like UIs |
| Mobile usability | Sticky export bar, standard pattern | Same as A | Canvas-anchored export, a named tradeoff vs. viewport-sticky |
| Repeat-user efficiency | Good | Good | Likely best — closest to a tool a returning user opens and works in |
| Accessibility | Lowest-risk — closest to current semantics | Same as A, plus needs the demo card's non-interactive state clearly marked (not a real, loadable tweet) | Needs explicit labels added to icon-only export buttons, or it regresses today's self-describing text links |
| Implementation risk | Lowest | Medium (new landing-view surface area) | Highest (new layout primitives: floating/anchored positioning, canvas texture) |
| Regression risk | Lowest — closest to current DOM/behavior shape | Low-medium | Medium — floating export control changes interaction geometry most |
| Design-system reuse | Baseline system defined here | Same system, dark values | Same system, denser values; introduces the one genuinely new primitive (floating pill) |
