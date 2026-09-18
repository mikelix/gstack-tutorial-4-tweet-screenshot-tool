# Design Review 4.1 — Human Review

```
Branch:      design/4.1-quiet-creator-tool  (HEAD 90ea006)
main:        bffbb00 — unchanged
Status:      NOT MERGED, NOT DEPLOYED
```

This document exists to make the redesign easy to judge — it doesn't
render a verdict. Every claim below is either a mechanical fact (build,
lint, a hash comparison) or explicitly marked as something only a human
can judge.

---

## 1. Branch state

| | |
|---|---|
| Current branch | `design/4.1-quiet-creator-tool` |
| HEAD | `90ea006192d2ae243ac4459eb047153809ae1096` |
| `main` HEAD | `bffbb009ea380ecc020998ffb65008f530a63669` (unchanged since before this design phase started) |
| Working tree | clean except one unrelated line in `.gitignore` (a `.gstack/` entry auto-appended by gstack's own tooling, pre-dating this task) |

**Files changed vs. `main`** (18 total — `git diff main HEAD --stat`):

```
docs/DESIGN_REVIEW_4_1_IMPLEMENTATION_PLAN.md      | 161 ++++++++++++++++++---
docs/design-review-4.1/evidence/*-after.png        | 8 new files
src/app/globals.css                                |  31 ++--
src/app/layout.tsx                                 |   6 +-
src/app/page.tsx                                   | 146 ++++++++++++++-----
src/app/thread/page.tsx                            |  83 +++++++----
src/components/AppHeader.tsx                       |  58 ++++++++ (new file)
src/components/CustomizePanel.tsx                  |  56 +++----
src/components/ExportControls.tsx                  |  31 +++-
src/components/ThreadBuilder.tsx                   |  56 ++++---
src/components/TweetSkeleton.tsx                   |  25 +---
```

**Backend/export/security/state files — reconfirmed untouched**
(`git diff main HEAD --stat -- <path>` returns empty for every one):
`src/app/api/image-proxy/route.ts`, `src/app/api/tweet/[id]/route.ts`,
`src/lib/export-image.ts`, `src/lib/media-hosts.ts`, `src/lib/tweet-url.ts`,
`src/lib/style-state.ts`, `src/lib/thread-state.ts`,
`src/components/TweetCanvas.tsx`, `next.config.ts`, `package.json`.

---

## 2. Visual evidence index

All screenshots already existed in `docs/design-review-4.1/evidence/` —
none were recaptured for this document.

### Desktop, 1440px

| State | Before | After | What changed | Intended benefit | What to inspect |
|---|---|---|---|---|---|
| Empty | [`desktop-A-empty.png`](design-review-4.1/evidence/desktop-A-empty.png) | [`desktop-A-empty-after.png`](design-review-4.1/evidence/desktop-A-empty-after.png) | Header shell added; headline/subhead given real typographic hierarchy; input+button restyled; a real, working "Try an example" link added | A first-time visitor sees a clear headline, one obvious action, and a way to see output before committing a tweet | Does the headline read as a clear outcome statement? Is the primary button unmistakable? Is "Try an example" noticeable without being loud? |
| Loaded | [`desktop-B-loaded.png`](design-review-4.1/evidence/desktop-B-loaded.png) | [`desktop-B-loaded-after.png`](design-review-4.1/evidence/desktop-B-loaded-after.png) | Two-column editor layout (preview card + inspector card) replaces the unbordered flex row; export actions given a hierarchy (filled primary vs. plain-text secondary) | The tweet preview reads as the hero; customization feels like an editor, not a form | Is the preview still the first thing your eye lands on? Is it obvious which export button is "the" one? Does the inspector feel organized? |
| Thread, empty | [`desktop-C-thread-empty.png`](design-review-4.1/evidence/desktop-C-thread-empty.png) | [`desktop-C-thread-empty-after.png`](design-review-4.1/evidence/desktop-C-thread-empty-after.png) | Same header/card treatment as the single-tweet page; Thread nav item now shows active state | Thread mode looks and feels like part of the same product, not a separate unstyled page | Does it feel consistent with the single-tweet page? Is it obvious you're in Thread mode? |

### Mobile, 375px

| State | Before | After | What changed | Intended benefit | What to inspect |
|---|---|---|---|---|---|
| Loaded | [`mobile-B-loaded.png`](design-review-4.1/evidence/mobile-B-loaded.png) | [`mobile-B-loaded-after.png`](design-review-4.1/evidence/mobile-B-loaded-after.png) | Fixed the confirmed horizontal-overflow bug; single-column stack; sticky bottom "Download PNG" bar | The page no longer clips content off-screen; the primary action stays reachable while scrolling | **Look specifically at the right edge of the tweet card** — the "before" image clips the platform icon and "Copy link"; confirm the "after" doesn't. Does the sticky bar feel helpful or in the way? |

Two additional pairs exist but weren't required by this review's table —
included for completeness: the error state
([before](design-review-4.1/evidence/desktop-D-error.png) /
[after](design-review-4.1/evidence/desktop-D-error-after.png), now with a
non-color-only warning icon) and keyboard focus progression
([before](design-review-4.1/evidence/desktop-F-focus1.png) /
[after](design-review-4.1/evidence/desktop-F-focus1-after.png)).

---

## 3. Five-second test — HUMAN JUDGMENT REQUIRED

I am not marking this PASS or FAIL. Open
[`desktop-A-empty-after.png`](design-review-4.1/evidence/desktop-A-empty-after.png)
for **no more than five seconds**, then look away, and answer from memory:

1. What does this product do?
2. Where would you click to start?
3. What kind of output would you expect to get?
4. Did you notice that both a single-tweet mode and a thread mode exist?
5. If you had a tweet loaded, would you know which button actually
   finishes the job?

My own read, stated as a hypothesis for you to check, not a claim: (1)
and (2) are likely clear from the headline/input alone; (3) is likely
*inferred* from the headline text ("a beautiful image") but not *shown* —
Direction A deliberately doesn't lead with a rendered example the way
Direction B would have; (4) is genuinely uncertain — the Single Tweet /
Thread switch is in the header, but it's easy to skim past on a first
look; (5) is likely clear once a tweet is loaded (one filled button), but
that's a different screenshot than the one this test uses.

---

## 4. Design review checklist

Unscored — for you to check off while looking at the evidence.

**Visual hierarchy**
- [ ] Preview is the visual hero once a tweet is loaded
- [ ] Headline/input hierarchy is clear on the empty state
- [ ] Primary CTA (Create / Download PNG) is unmistakable at every stage
- [ ] Secondary actions (Copy image, Copy share link, Try an example) are
      visibly subordinate, not competing for attention

**Product clarity**
- [ ] Purpose is understood immediately from the empty state
- [ ] "Try an example" is noticeable without reading every line of copy
- [ ] Single/Thread navigation is obvious, not just present
- [ ] The loaded state feels like an editor/workspace, not a plain form

**Polish**
- [ ] Spacing feels deliberate, not accidental
- [ ] Typography hierarchy (headline vs. body vs. labels) feels professional
- [ ] Borders/shadows/radii feel consistent across cards and controls
- [ ] No element still looks like raw browser-default UI
- [ ] No decoration that doesn't serve a purpose

**Mobile**
- [ ] No horizontal overflow (see evidence note above)
- [ ] Header is understandable in its compact mobile form (icon + Single/Thread only)
- [ ] Preview is readable at 375px
- [ ] Controls are easy to use at touch size
- [ ] The sticky export bar doesn't obscure content you need to see
- [ ] Touch targets feel adequately sized

**Trust / startup quality**
- [ ] Feels like a real product, not a coding demo
- [ ] Interface is restrained rather than flashy
- [ ] No fake marketing language or visual clutter
- [ ] Product value is more obvious than in the "before" screenshots

**Accessibility**
- [ ] Keyboard focus is visible (see `desktop-F-focus1/2-after.png`)
- [ ] Contrast looks acceptable throughout
- [ ] Labels are understandable (field group labels, button text)
- [ ] Icon-only elements have accessible names — specifically check the
      mobile header's icon-only brand mark
      (`aria-label="Tweet Screenshot — home"` in code; worth confirming it
      reads sensibly with a screen reader or the browser's accessibility
      inspector, not just trusting the attribute exists)

---

## 5. Before/after change summary

| Area | Before | After | Intended effect |
|---|---|---|---|
| Header | None — page title only, no shared chrome | Persistent header: brand mark, Single Tweet / Thread switch, GitHub link | Gives Thread mode a navigation path; establishes product identity |
| Headline | "Tweet Screenshot" (15px default text) | "Turn any tweet into a beautiful image." (38px, tight tracking) | States the outcome, not just the product name |
| URL input | Plain, unstyled, default browser input | Rounded, bordered, focus-ringed input at two sizes (empty-state large, loaded-state compact) | Reads as an intentional control, not default HTML |
| Try an example | Did not exist | A real link that loads a fixed neutral tweet via the existing fetch path | Lets a skeptical visitor see output before committing their own tweet |
| Single/Thread navigation | No link existed between the two pages | Segmented control in the header, present on both routes, reflects active route | Fixes the current-state finding that Thread mode was undiscoverable |
| Preview workspace | Unbordered `<div>`, tweet card just sat in a flex row | Bordered card, centered, two-column grid with the inspector | Establishes the preview as the visual hero in its own container |
| Customization panel | Bare `<fieldset>`s, default browser radio/range styling | Bordered card, uppercase micro-labels, styled swatches/segments with a selected-state ring | Reads as a grouped inspector, not a raw HTML form |
| Export controls | Three plain buttons, identical weight | One filled primary button (Download PNG) + two plain-text secondary actions | Makes the "normal completion path" visually unambiguous |
| Mobile layout | Flex-wrap fallback; tweet card overflowed the viewport horizontally | Single-column stack; overflow fixed (verified: `scrollWidth === clientWidth`); sticky bottom export bar | Removes a real rendering bug; keeps the primary action reachable while scrolling |

---

## 6. Regression safety

| Check | Result | Evidence |
|---|---|---|
| `npm run build` | **PASS** | Clean build, no TypeScript errors, on `design/4.1-quiet-creator-tool` HEAD |
| `npm run lint` | **PASS** | Zero ESLint errors or warnings |
| No 375px overflow | **PASS** | `document.documentElement.scrollWidth === clientWidth` checked live against the running app on both the empty and loaded mobile states — not inferred from CSS |
| Keyboard navigation | **PASS** | Real `Tab` presses against the running app; focus ring visible on the new header nav links, same as the original controls (`desktop-F-focus1/2-after.png`) |
| Example loading works | **PASS** | "Try an example" clicked against the running app; loads the real tweet via the existing `loadTweet`/`/api/tweet/[id]` path, confirmed by screenshot and zero console errors |
| Thread navigation works | **PASS** | Header's Thread link navigated to `/thread` against the running app; active state correctly reflects the route (`desktop-C-thread-empty-after.png`) |
| Captured `TweetCanvas` DOM unchanged | **PASS** | `git diff main HEAD -- src/components/TweetCanvas.tsx` is empty — the exact element `captureNodeToPng`/`captureNodeToBlob` read is byte-identical source |
| Captured `ThreadBuilder` DOM unchanged | **PASS** | Same check on `src/components/ThreadBuilder.tsx`'s `containerRef` element — only sibling/child chrome outside the ref'd node changed; the ref'd node's own inline style is untouched |
| Export architecture untouched | **PASS** | `git diff main HEAD --stat` empty for `export-image.ts`, `media-hosts.ts`, both API routes |

**Export visual output — actually re-tested, not inferred:**

The exported PNG was regenerated on both branches for the identical
tweet and style parameters
(`id=20&v=1&bg=twitter-blue&p=48&s=2&t=light`, the "just setting up my
twttr" tweet), by hooking `HTMLAnchorElement.prototype.click` in the
live running app to intercept the real `data:` URL `handleDownload()`
produces, decoding it, and computing its SHA-256:

```
main        (before): 454202 bytes, sha256 0f64cd46a4c10a28212e4ca9cbf090c9ec77c7f304f5803280a044f7f3ca48a1
design/4.1  (after):  454202 bytes, sha256 0f64cd46a4c10a28212e4ca9cbf090c9ec77c7f304f5803280a044f7f3ca48a1
```

**Byte-identical.** This is the actual exported artifact, produced by the
real `handleDownload` → `captureNodeToPng` code path in each branch's
running app — not a code-review inference.

---

## 7. Open questions for human review

No more than five, genuine judgment calls only:

1. Is the header too prominent relative to the tweet preview, or does it
   read as appropriately quiet chrome?
2. Does the empty state show enough evidence of product value, or does
   Direction B's "show an example before any interaction" idea deserve a
   second look even after choosing A?
3. Is "Try an example instead" sufficiently visible, or does it need more
   visual weight now that it's a real, working feature?
4. Does the customization inspector feel genuinely polished, or does it
   still read as a restyled form rather than a designed panel?
5. Is the mobile sticky "Download PNG" bar helpful, or does it feel
   intrusive/redundant given the in-flow export button still exists above
   the fold on most phones?

---

## STATUS

```
READY_FOR_HUMAN_DESIGN_REVIEW
```

**HUMAN DECISION REQUIRED:**

A — Approve Direction A as implemented
B — Approve with minor changes
C — Request another design iteration
D — Compare against Direction B before deciding
E — Reject Direction A

Do NOT merge. Do NOT deploy. STOP AND WAIT.
