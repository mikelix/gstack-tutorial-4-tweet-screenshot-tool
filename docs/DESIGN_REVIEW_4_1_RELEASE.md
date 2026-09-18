# Design Review 4.1 — Release Record

```
main HEAD:    693ac0e — fix: video tweet export hanging forever (Export timed out)
Production:   https://tweet-screenshot-tool.vercel.app/
Deployment:   dpl_tDLgQu6dRXny2Z2zfKq2QsJz37Ca (Ready, target=production)
```

## Selected direction

**A — Quiet Creator Tool.**

## Human review result

Approved after a minor polish pass (human decision: "B — approve with
minor changes"). Six presentation-only changes were made in response
(header/content padding alignment, loaded-state URL row redesign,
inspector card sizing, secondary export button treatment) — see
`docs/DESIGN_REVIEW_4_1_HUMAN_REVIEW.md` for the original review gate.

## What changed

Presentation layer only: persistent header with Single Tweet/Thread nav,
headline/subhead hierarchy, two-column preview + inspector layout on the
loaded state, styled customization panel, export button hierarchy (one
filled primary + two lighter secondary actions), mobile single-column
stack with a fixed overflow bug and a sticky export bar.

Plus one **export-pipeline correctness fix**, found and fixed after the
design was approved and deployed (see "Thread/video export fix" below).

## What did not change

Core export/API/security/state behavior: `src/app/api/image-proxy/route.ts`,
`src/app/api/tweet/[id]/route.ts`, `src/lib/media-hosts.ts`,
`src/lib/tweet-url.ts`, `src/lib/style-state.ts`, `src/lib/thread-state.ts`,
`next.config.ts`, `package.json`, and the captured `TweetCanvas`/
`ThreadBuilder` DOM nodes themselves — confirmed unchanged by source diff
against pre-redesign `main`. (`src/lib/export-image.ts` *did* later change,
but only to fix the video-export hang described below — not as part of the
visual redesign.)

## Regression evidence

- `npm run build` — PASS (repeated at every stage: pre-merge, post-merge,
  post video-export-fix)
- `npm run lint` — PASS (zero errors/warnings, every stage)
- Export byte-hash regression — a plain-text tweet export is
  **byte-for-byte identical** before the redesign, after the redesign, and
  after the video-export fix: `405691 bytes, sha256
  eb9b38e6392fad1ea450e77fff3d7423b58ee5b9605450b450f2f66c5490785b`,
  verified with a direct side-by-side comparison against `main` in a
  temporary git worktree (same session, same browser, same tweet)
- Mobile 375px — zero horizontal overflow, mechanically reconfirmed at
  every stage
- Keyboard focus, "Try an example", Single/Thread navigation — all
  reconfirmed working against the running app at every stage

## Thread/video export fix

Deployed after initial production sign-off, a real bug was found during
human review: any tweet containing a native `<video>` element — single
tweet or thread, any export scale — hung forever on export, eventually
showing "Export timed out — try a lower scale". Root cause (measured):
`modern-screenshot`'s own internal video-cloning step awaits a `seeked`
event that never fires because our videos are never played (`currentTime`
is always `0`, and reassigning `0` to an already-`0` element doesn't fire
`seeked` in Chromium). This happened before our own poster-frame-swap hook
ever got a chance to run — it could never have prevented the hang. Fixed
by swapping `<video>` → poster `<img>` on our own off-screen clone of the
export node *before* handing anything to `modern-screenshot`, so it never
sees a real `<video>` element. Full writeup: `TODOS.md`, "Fixed: video
tweet export hung indefinitely."

**Automated verification** (commit `693ac0e`, both locally and in
production): the exact failing production fixture
(`/thread?ids=2100619720772694036,2100906305661612541`) now exports
successfully at 1×/2×/3× in ~0.6–2s each (previously: infinite hang at
every scale, identically, regardless of scale). A single video tweet,
previously also hung, now exports correctly at all three scales. The
X Broadcast known-limitation fixture, a small thread, and a plain-text
tweet were all re-verified working with zero regression.

**Human manual verification** (production, post-deploy):

- Thread mode → Download PNG: **PASS**
- Thread mode → Copy image: **PASS**
- Copied image pasted successfully into Windows 11 Paint: **PASS**
- Visual output inspected manually and judged correct

The previously failing thread/video export path is now verified in
production by **both** automated (Aside-driven, byte-level) and human
(manual, real clipboard/paste) testing.

## Media fidelity boundary

- Native tweet video/photo media: renders and exports correctly — verified
  both automated and (for the Copy image path) by hand.
- X Broadcast (`x.com/i/broadcasts/...`) rich preview cards: **known,
  documented upstream limitation**, not a bug. A tweet quoting a live X
  Broadcast shows text + link only, because X's free syndication data path
  never exposes broadcast card metadata (no title, poster, duration, or
  participant data) for this content type — confirmed by inspecting the
  raw syndication payload and X's oEmbed endpoint directly; the real card
  is rendered client-side by X's own proprietary, authenticated
  `widgets.js`. `react-tweet` has no card/broadcast concept anywhere in
  its source. No fix exists within the free-data path. Full investigation:
  `TODOS.md`, "Known upstream limitation (investigated, not a bug)".
- **Engineering note preserved from the investigation:** a byte-identical
  export hash proves the redesign didn't alter existing export behavior;
  it does not prove the upstream data representation contains every
  element visible on X.com — those are two different claims, and only the
  first is what hash-equality actually verifies.

## Production verification

- Desktop: empty/loaded/thread states — clean, zero console errors
- Mobile 375px: no overflow, sticky export bar, controls usable
- Thread export (the previously failing fixture): PASS at 1×/2×/3×, both
  automated and human-verified (Download PNG, Copy image → Paint)
- X Broadcast fixture: behaves exactly as documented (text + link, export
  still succeeds)
- Console: clean on every page checked, every stage

## Known limitations

- X Broadcast rich preview cards do not render (documented above) — a
  genuine free-data-path limitation, not something this app or
  `react-tweet` can fix without paid/authenticated X API access.
- Pre-existing, unrelated to this design phase: thread shared-link style
  preset doesn't always restore on first load (`TODOS.md`); no rate
  limiting yet on the public API routes (`TODOS.md`).

## Final status

```
DESIGN_4_1_PRODUCTION_READY_WITH_KNOWN_LIMITATIONS
```
