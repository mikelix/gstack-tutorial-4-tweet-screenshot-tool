# Design Review 4.1 — Implementation Plan

```
STATUS: IMPLEMENTED ON BRANCH — AWAITING MERGE DECISION
Branch: design/4.1-quiet-creator-tool
```

## Selected direction

**Direction A — Quiet Creator Tool** (`docs/DESIGN_REVIEW_4_1_DIRECTIONS.md`).
Restrained light palette, two-column editor layout once a tweet loads, a
shared header shell with an always-visible Single Tweet / Thread switch,
one filled primary export action beside two secondary text actions.

## Accepted modifications

None — implementing Direction A as specified, no elements borrowed from B
or C. One addition not in the original mockup, required by the current-
state findings rather than aesthetic preference: the confirmed mobile
horizontal-overflow bug on the tweet preview card gets fixed as part of
this work (it's a presentation-layer bug affecting every direction, not
Direction-A-specific, and Direction A's own mobile mockup already assumes
it's fixed).

## Real component inventory (what actually exists to change)

| File | Current role | Change |
|---|---|---|
| `src/app/layout.tsx` | Root layout | Add the shared header shell (brand + Single/Thread switch) here so both routes get it for free |
| `src/app/page.tsx` | Single-tweet page: input, Load button, orchestrates loaded/empty/error state | Restyle empty state (headline/subhead/input/button hierarchy); restyle the two-column loaded layout wrapper |
| `src/app/thread/page.tsx` | Thread page, currently unstyled and unlinked | Same treatment as `page.tsx`; gains the header shell automatically via `layout.tsx` |
| `src/components/TweetCanvas.tsx` | Renders the tweet preview | Wrap in the new bordered preview card; no rendering-logic change |
| `src/components/CustomizePanel.tsx` | Background/padding/scale/theme controls | Restyle only — group labels, swatch/segment styling, spacing scale |
| `src/components/ExportControls.tsx` | Download PNG / Copy image / Copy share link | Visual hierarchy fix: one filled primary button, two secondary text links — no change to what each button does |
| `src/components/TweetSkeleton.tsx` | Loading skeleton | Restyle to match new surface/border tokens |
| `src/components/ThreadBuilder.tsx` | Thread mode UI | Same visual language pass as the single-tweet controls |
| `src/app/globals.css` | Global styles | Add Direction A's design tokens (CSS custom properties) here — additive, nothing removed |

**Explicitly not touched:** `src/app/api/image-proxy/route.ts`,
`src/app/api/tweet/[id]/route.ts`, `src/lib/export-image.ts`,
`src/lib/media-hosts.ts`, `src/lib/tweet-url.ts`, `src/lib/style-state.ts`,
`src/lib/thread-state.ts` — no fetch, proxy, export, or state-serialization
logic changes.

## Implementation sequence

Small, independently verifiable slices, each gated by a build and a real
screenshot comparison against the "before" evidence already captured:

1. **Design tokens** — add Direction A's CSS custom properties to
   `globals.css`. Purely additive; no visual change until consumed.
2. **Shared header shell** — new `AppHeader` component (brand mark, product
   name, Single Tweet / Thread segmented nav, GitHub link) rendered from
   `layout.tsx`. This alone fixes the Thread-discoverability finding.
   Gate: build passes; both routes render the header; the nav switch
   correctly reflects/links the active route.
3. **Empty-state restyle** (`page.tsx`) — headline, subhead, input, primary
   button, "Try an example" link, per the `a-empty.html` mockup. Gate:
   build passes; visual screenshot compared against `concept-a-desktop-empty.png`.
4. **Loaded-state restyle** (`page.tsx`, `TweetCanvas`, `CustomizePanel`,
   `ExportControls`) — two-column grid, bordered preview card, grouped
   inspector fields, export hierarchy fix. Gate: build passes; a real
   tweet loads and renders correctly; export buttons still perform their
   existing actions unchanged.
5. **Mobile responsive pass** — single-column stack, sticky bottom export
   bar, and the fix for the confirmed overflow bug. Gate: **zero
   horizontal overflow at 375px**, checked directly (not assumed from the
   CSS), against a real loaded tweet.
6. **Error and loading states** — restyle the skeleton and the error
   message; give the error state a non-color-only signal (icon + text)
   alongside the existing red color, addressing the accessibility finding.
7. **Thread page + ThreadBuilder** — apply the same visual language for
   consistency, now reachable via the header nav from step 2.
8. **Accessibility re-check** — keyboard tab order, focus-ring visibility
   against the new palette, label associations — confirm nothing regressed
   from the current-state baseline (`desktop-F-focus1.png`/`-focus2.png`).

Every step: `npm run build` must pass before moving to the next step.
**Actual sequence followed:** steps 1–4 as planned; step 5 required a
second pass (see "What changed from the plan" below) after the first
implementation attempt introduced a new mobile header-wrapping bug that
the mobile screenshot check caught; steps 6–8 completed as planned.

## What changed from the plan while implementing

Two real issues were found by actually rendering and looking — not
assumed correct because the build passed — matching this whole project's
own evidence-ladder discipline:

1. **The new header itself broke at 375px on the first pass**: the full
   "Tweet Screenshot" wordmark and the "Single Tweet"/"Thread" labels
   wrapped to multiple lines in the cramped mobile header. Fixed by
   hiding the wordmark and the GitHub link below the `sm:` breakpoint
   (icon-only brand mark, given an explicit `aria-label` so it isn't a
   new accessibility regression) and tightening the nav pill's padding.
2. **Dev-mode's own indicator badge overlapped the new sticky mobile
   export bar** in `next dev`. Confirmed this doesn't appear in a real
   production build/deploy (`next build && next start`) — all final
   "after" evidence below was re-captured against the production server,
   not the dev server, for this reason.

Neither finding required touching backend/export/proxy logic; both were
presentation-layer fixes in `AppHeader.tsx` only.

## Validation plan — results

**Before/after screenshot pairs**, all in `docs/design-review-4.1/evidence/`,
after screenshots captured against a real `next build && next start`
production server, not the dev server:

| State | Viewport | Before | After |
|---|---|---|---|
| Empty | 1440px | `desktop-A-empty.png` | `desktop-A-empty-after.png` |
| Loaded | 1440px | `desktop-B-loaded.png` | `desktop-B-loaded-after.png` |
| Thread, empty | 1440px | `desktop-C-thread-empty.png` | `desktop-C-thread-empty-after.png` |
| Error | 1440px | `desktop-D-error.png` | `desktop-D-error-after.png` |
| Keyboard focus (2 tabs) | 1440px | `desktop-F-focus1/2.png` | `desktop-F-focus1/2-after.png` |
| Empty | 375px | `mobile-A-empty.png` | `mobile-A-empty-after.png` |
| Loaded | 375px | `mobile-B-loaded.png` | `mobile-B-loaded-after.png` |

**Behavioral checklist:**

- [x] First-time task understandable within ~5 seconds — the empty state
      now states the outcome ("Turn any tweet into a beautiful image"),
      has one filled primary button, and offers an immediate, real,
      working example via "Try an example instead" (wired to the same
      `loadTweet` path a manual paste uses, not a separate code path)
- [x] URL entry obvious — single input, clearly labeled placeholder
- [x] One clear primary action at every stage — filled accent button vs.
      plain-text secondary actions throughout
- [x] Single ↔ Thread discoverable without documentation — header nav
      present on both routes, active state correctly reflects the route
- [x] Loaded preview visually dominant — bordered hero card, inspector
      confined to a narrower side column
- [x] Download PNG unmistakable — filled accent button, only export
      action with that treatment
- [x] Zero horizontal overflow at 375px — verified mechanically
      (`document.documentElement.scrollWidth === clientWidth`), not just
      by eye, on both the empty and loaded mobile states
- [x] Keyboard/focus behavior preserved — confirmed via real `Tab`
      presses against the running app; focus ring visible on the new nav
      links exactly as it was on the original controls
- [x] Export output unchanged — `TweetCanvas.tsx`'s ref'd element (the
      exact node `captureNodeToPng`/`captureNodeToBlob` read) and
      `ThreadBuilder.tsx`'s `containerRef` element were not touched by
      any edit; only their ancestors and sibling chrome were restyled
- [x] Existing functional behavior unchanged — `npm run build` and
      `npm run lint` both pass; the "Try an example" flow, background/
      padding/scale/theme controls, and thread add/retry/remove/reorder
      controls were exercised against the real running app during this
      pass, all firing their existing, untouched handlers

Implemented entirely on `design/4.1-quiet-creator-tool`, not `main` —
merging `main` is a separate, later decision this plan does not make.

## Polish pass (human review response: "B — approve with minor changes")

Six specific changes requested after the human design review gate, all
presentation-layer, all verified not to touch export output:

1. **Header alignment/spacing** — fixed a real padding mismatch: the
   header used `px-4 sm:px-6` but the content below it used a bare `px-6`
   at every breakpoint, so their left/right edges didn't actually line up
   at 375px. Now both use the same `px-4 sm:px-6` scale everywhere.
   Vertical padding tightened (`py-3` → `py-2.5`) for a snugger shell,
   without shrinking type or touch targets.
2. **URL/action row redesigned** — the loaded-state row (input + "Change")
   now sits in a bordered pill with a link icon prefix, and the action
   button gained a refresh icon and a clearer label ("Load a different
   tweet" on desktop, "Change" on mobile to avoid the header-wrapping
   mistake from the first pass — see above). `onClick`/`onChange`/
   `onKeyDown` are byte-identical to before; only the JSX/className changed.
3. **Inspector card now hugs its content** — added `self-start` to the
   CustomizePanel wrapper in both `page.tsx` and `thread/page.tsx`, which
   were stretching to match the grid row's height (CSS Grid's default
   `align-items: stretch`) and leaving a large empty area below the
   actual controls.
4. **Secondary export actions strengthened** — "Copy image" and "Copy
   shareable link" gained a border/pill treatment (`ExportControls.tsx`
   only) so they read as clickable buttons, not plain text, while staying
   visually lighter than the filled "Download PNG" primary.
5. **`TweetCanvas.tsx` and `ThreadBuilder.tsx`'s ref'd container —
   reconfirmed untouched** (`git diff main HEAD -- src/components/TweetCanvas.tsx`
   still empty). Export output re-verified after this pass too (see below).
6. **Recaptured only the affected screenshots** — desktop empty/loaded/
   thread-empty and mobile empty/loaded, all in
   `docs/design-review-4.1/evidence/*-after.png` (overwritten in place;
   the error and keyboard-focus states weren't targeted by this pass and
   weren't recaptured). Full regression re-run: `npm run build` PASS,
   `npm run lint` PASS, zero 375px overflow (mechanically re-confirmed).

**Export output re-verified after the polish pass, same method as
before** (hook `HTMLAnchorElement.prototype.click`, capture the real
`data:` URL, hash the decoded bytes) — same tweet, same style params:

```
454202 bytes, sha256 0f64cd46a4c10a28212e4ca9cbf090c9ec77c7f304f5803280a044f7f3ca48a1
```

Identical to both the pre-polish branch state and `main`. Export output
has not changed at any point in this design phase.

**Process note, disclosed rather than omitted:** while starting a
verification server on an alternate port to avoid colliding with your own
active `npm run dev` session, a process-cleanup command mistakenly
targeted and killed your dev server (PID 19084) instead of the intended
one. Caught immediately, and your dev server was restarted (`npm run
dev`, back on port 3000) — its first logged request after restart was for
the same tweet URL you'd been testing, suggesting the client reconnected
cleanly, but you should confirm your session actually looks right, since
any client-side state beyond the URL wasn't something I could verify from
here.
