# Review 04 — QA / Verification

```
Date:            2026-09-17
Reviewer role:   QC (typecheck/lint/build) + Browser QA (Aside)
Command:         tsc --noEmit, eslint, npm run build (repeated); aside repl (real-browser)
Scope reviewed:  the T1.5 spike, main implementation (Phases 1-8), thread mode
Verdict:         PASS with one significant caught-and-fixed bug (the avatar bug); several items deferred, stated not hidden
```

---

## The T1.5 spike — the most important phase in the project

**Why it existed:** B1 from `03-eng-review.md` was a real, unresolved
technical unknown, not a product question — *does this actually work*, not
*should we build this*. This project's operating principle for
implementation was "build evidence, not volume," and this was the
highest-risk assumption to de-risk first.

**How the unknown was actually resolved — by reading source, not memory or
documentation:**

- Read `node_modules/react-tweet/dist/twitter-theme/*.js` directly. Found
  `EmbeddedTweet` accepts a `components` prop that can override avatar/media
  rendering, and `TweetMediaVideo` renders a real `<video poster={...}>`
  with the poster URL already present as a live attribute.
- Read `node_modules/modern-screenshot/dist/index.mjs` directly. Found
  `fetchFn(url)` is called for every remote image during capture, consumed
  exactly like the library's own `responseType: "dataUrl"` fetch path — the
  fact that turned out to matter most.
- Found `onCloneNode`/`onCloneEachNode` hooks fire on the *cloned* DOM tree
  right before rasterization — the natural place to swap a `<video>` for its
  poster-frame `<img>` without touching the live, interactive page.
- **Why DOM rewriting turned out not to be needed:** `fetchFn` intercepts
  assets at capture time only. The live preview keeps pointing at real
  `pbs.twimg.com` URLs (fine — cross-origin images *display* normally; CORS
  only bites when canvas tries to *read* pixel data). Only the capture step
  needed the SSRF-hardened proxy.

### The bug this spike actually caught

First real capture attempt passed the "no exception thrown" bar —
`modern-screenshot` reported success — and the exported PNG showed a
**broken-image icon where the avatar should have been.** Everything else
(text, font, gradient background, rounded corners) was correct. A textbook
silent-wrong-output failure: the code "worked" by every naive check and
still produced the wrong result.

**Root cause, found by reading source, not guessing:** the image-proxy
route itself tested fine (`200 image/jpeg`, valid binary data). The fetch
wrapper (`proxyAwareFetch`) returned a `blob:` object URL via
`URL.createObjectURL()` — works for a normal `<img src>`, but
`modern-screenshot` serializes the cloned DOM into an SVG string and reloads
*that* as a fresh image resource. A `blob:` URL created in the live
document does not reliably resolve once embedded in that re-loaded SVG.

**Fix:** return a self-contained base64 `data:` URL via
`FileReader.readAsDataURL()`, matching `modern-screenshot`'s own
`responseType: "dataUrl"` contract.

**Proof, visually, not just "tests pass":** the corrected PNG was saved to
disk and read directly with an image tool — the real profile photo
appeared, correctly circular-cropped. Capture time also dropped (1046ms →
468ms), a secondary confirmation a slower, failing path had been replaced.

## Bugs and risks caught before ship

| Problem | Found by | Fix | Status |
|---|---|---|---|
| CORS blocks direct browser fetch | CEO review, live probe | Server-side Route Handler | Fixed (architectural, never a runtime bug) |
| SSRF via image-proxy | CEO review / eng review B2 | Exact-hostname allowlist, https-only, redirect re-validation, size cap, MIME check | Fixed, verified live (bad host → 400, non-HTTPS → 400, legit host → 200) |
| Image-proxy never wired to real DOM (B1) | Eng review, confirmed empirically in T1.5 | `fetchFn` hook wired to the proxy | Fixed, with visual proof |
| **Avatar rendered as broken-image icon despite "successful" capture** | T1.5 spike, real capture + visual PNG inspection | `blob:` → base64 `data:` URL | Fixed, with before/after visual proof |
| Silent wrong font before fonts load | CEO review 2A | `await document.fonts.ready` | Fixed (not separately stress-tested under artificial delay — see `TODOS.md`) |
| Same class for images not decoded | Eng review B3 | `await Promise.all(images.map(img => img.decode()))` | Fixed (not separately stress-tested) |
| Stale response race | CEO review 4A | Request-token + `AbortController` | Fixed, verified with a deterministic network-delay test |
| Safari/iOS clipboard gesture break | OV-2 | `ClipboardItem` wraps `Promise<Blob>` directly | Implemented, NOT empirically verified on real Safari/iOS |
| Video-tweet export undefined | OV-3 | Poster-frame swap + badge | Implemented, NOT empirically verified against a real video tweet |
| Thread URL length uncapped | OV-4 | Hard cap ~12 tweets | Implemented; exact-boundary cases not exercised |
| Silent thread-item drop | CEO review 11A | Inline error card, export blocked | Fixed, verified via Aside (valid → invalid → valid, remove resolves it) |
| Rate-limiter/"no secrets" contradiction | OV-1 | Plan corrected to Upstash/KV | **Planned and reviewed, NOT implemented in code** — see Evidence Ladder below |
| Thread share-link *style* doesn't reliably restore | This phase's browser checkpoint | Investigated one bounded pass; root cause not found | **Documented, deferred, NOT fixed** — `TODOS.md` |

## Aside browser QA

Every checkpoint from T1.5 through the production smoke test ran through
Aside — network-delay injection to force the stale-request race
deterministically, real `window.history.back()/forward()` checked against
actual DOM attributes (not Aside's own accessibility-snapshot rendering of
`aria-pressed`, which turned out unreliable for one component — a tooling
quirk, not an app bug), real downloaded PNGs read and visually inspected.
Per `docs/external_ai_mentor.md`, the "Aside first, never install
Playwright/Chromium without explicit approval" rule held under real
pressure — a rejected `npm install -D playwright` call was abandoned in
favor of the already-verified `aside` CLI mid-session.

## The Evidence Ladder — the central lesson of this review

Weakest to strongest, as this project actually climbed it:

1. Idea — removes zero feasibility uncertainty.
2. Architecture assumption — removes uncertainty about intent, not truth.
3. Code compiles (`tsc --noEmit`) — type correctness only.
4. Unit/component test — **not actually written for most of this project's
   logic** (see `05-ship.md`'s process-gap note).
5. Local browser behavior "succeeding" — the T1.5 spike's first attempt sat
   exactly here and was still wrong. The level that most convincingly
   *looks* like proof and most often isn't.
6. Aside real-browser test with a deterministic setup (the network-delay
   race test) — makes a hard-to-reproduce failure reproducible on demand.
7. Exported PNG visually inspected — **this is what actually caught the
   avatar bug.** Removes the "no error means correct" assumption.
8. Human manual test — reported by the user, not independently verifiable
   by the AI; catches blind spots automated checks share.
9. Production deployment — "works in dev" vs. "works with real
   infrastructure."
10. Human production test — does the actual shipped thing hold up.

**Core principle:** do not confuse implementation with evidence. Writing the
code that should fetch and rewrite an avatar is not evidence it renders
correctly — only climbing to level 7 was. A second, related principle: do
not confuse a reviewed plan with a shipped implementation — the
rate-limiting fix (OV-1) climbed through three review passes and was still
never written into the code. A plan decision is not evidence past level 2
until it's built and tested.

## What was NOT reviewed here

- No automated test suite exists (see `05-ship.md` Part 7 equivalent). Every
  verification above happened through manual Aside-driven browser checks,
  gated on finding real, currently-live tweet IDs for each scenario —
  slower and less repeatable than a mocked test would have been, and the
  direct reason emoji/multi-image/video-tweet remain unverified.
- Deferred verification items (real video tweet, emoji, multi-image thread,
  Safari clipboard, delayed-network handling, broken-image 404 handling,
  oversized-export timeout) are listed in full in `TODOS.md`, not repeated
  here.
