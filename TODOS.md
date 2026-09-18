# TODOS

Deferred, non-blocking work for the Tweet Screenshot Tool. None of these block
Tutorial No. 4 — the core paste → customize → export flow (single tweet and
thread) works and was verified with real evidence (see plan/implementation log).
Two items below were found and resolved after the original Tutorial No. 4
release, during Tutorial No. 4.1 (`TUTORIAL.md` Parts 20-23) — kept here with
the same status the tutorial itself claims: one fixed, one a documented
upstream limitation.

## Fixed: video tweet export hung indefinitely ("Export timed out")

- **Any tweet containing a native `<video>` element — single tweet or
  thread, any export scale — hung forever on export**, eventually showing
  "Export timed out — try a lower scale" after the fixed 8-second capture
  timeout. Root cause (measured, not guessed — full trace in Tutorial No.
  4.1 Part 22): `modern-screenshot`'s own internal video-cloning step
  (`cloneVideo`) sets `clonedVideo.currentTime = video.currentTime` and
  awaits a `seeked` event before continuing. This app's video elements are
  never played, so `currentTime` is always `0` — reassigning `0` to an
  element already at `0` does not fire `seeked` in Chromium, so that
  `await` never resolves. This happens inside `modern-screenshot`'s own
  clone step, before this app's `onCloneNode` hook (the poster-frame swap,
  `replaceVideoWithPosterImage`) ever runs — so that hook could never have
  prevented the hang; it ran too late in the pipeline. Confirmed with
  resource-timing instrumentation: zero `/api/image-proxy` fetches ever
  fired, at 1x/2x/3x, even with the timeout temporarily raised to 60s — the
  hang is unconditional, not a "just needs more time" situation, and
  scale-independent (rules out a pixel/canvas-size cause). A single,
  non-threaded video tweet hung identically to the reported thread case,
  so this was never actually thread-specific.

  **Fix** (`src/lib/export-image.ts`): swap every `<video>` for its poster
  `<img>` on this app's own off-screen clone of the export node, before
  handing anything to `domToPng`/`domToBlob` — so `modern-screenshot` never
  sees a real `<video>` element and its internal `cloneVideo`/seek-wait
  path never runs. The clone is attached (`position:fixed; left:-99999px`,
  not `display:none`) so layout/computed styles resolve exactly as on the
  live node. `onCloneNode: replaceVideoWithPosterImage` was removed from
  the `domToPng`/`domToBlob` calls (now redundant/ineffective) in favor of
  this pre-capture sanitization step.

  **Verified after the fix:** a plain-text tweet's export is byte-for-byte
  identical before and after this fix (`sha256
  eb9b38e6392fad1ea450e77fff3d7423b58ee5b9605450b450f2f66c5490785b`,
  405691 bytes) — confirming zero regression for non-video content. A
  previously-hanging two-video-tweet thread now exports successfully at
  1x/2x/3x in roughly 0.6-2 seconds each, both locally and in production.
  The original 8-second capture timeout was left unchanged — it was never
  the real constraint once the hang itself was removed.

## Known upstream limitation (investigated, not a bug)

- **X Broadcast (`x.com/i/broadcasts/...`) rich preview cards don't render.**
  When a tweet quotes a post that embeds a live X Broadcast, X.com shows an
  animated rich card (title, live speaker avatars, duration, viewer count).
  This app shows the quoted text plus the plain broadcast link instead.
  Investigated end-to-end (full trace in Tutorial No. 4.1 Part 21): the free
  syndication payload (`cdn.syndication.twimg.com/tweet-result`, what
  `fetchTweet()` calls) never includes broadcast card metadata for this
  content type — no title, thumbnail, duration, or participant data, only a
  plain URL entity. X's other free endpoint, oEmbed, confirms this: it
  returns a bare `<blockquote>` plus X's own `widgets.js`, meaning the real
  card is rendered by proprietary client-side JS pulling from X's
  authenticated internal APIs, not from any static, fetchable data.
  `react-tweet` itself has no card/broadcast concept anywhere in its source
  (checked types and components) — it was never built to support this. This
  app's own code (`/api/tweet/[id]`, `TweetCanvas.tsx`) passes the payload
  through unmodified; there is nothing for it to drop, because the data was
  never present. Reproduced with
  `https://x.com/elonmusk/status/2100296847344783441`. A contrast test on an
  ordinary tweet with native video (upstream `mediaDetails`/`video` present)
  rendered correctly, confirming the gap is specific to Broadcast/card
  previews, not video support generally. **No fix is available within the
  free-data path** — there's no static poster/thumbnail/title anywhere to
  build a fallback from, and reproducing the card would require scraping
  X's proprietary JS or paid/authenticated API access, both out of scope.
  **Priority:** documented limitation, non-blocking. **Possible V2 (not
  implemented):** for `x.com/i/broadcasts/...` URLs, show a generic,
  non-fabricated fallback like "X Broadcast — preview unavailable · Open on
  X" — must not invent title/poster/duration/viewer data.

## Known non-blocking bug

- **Thread page: shared-link style preset doesn't reliably restore on initial
  load.** Opening a thread share link (`/thread?ids=...&bg=midnight...`)
  correctly restores the tweet ids and their order (verified repeatedly), but
  the background/padding/scale/theme preset sometimes renders as the default
  ("Twitter Blue") instead of the shared value, even though the app's own
  React state was directly confirmed correct at that point (diagnostic
  instrumentation showed `style.backgroundId` was "midnight" on every render,
  while the rendered DOM's `aria-pressed` attribute showed "Twitter Blue" —
  a genuine state-vs-DOM discrepancy, not a logic bug in `decodeThreadState`
  or the component code, both of which were verified correct in isolation).
  Reproduced consistently across a clean Turbopack cache + dev server
  restart, so it is not simple dev-cache staleness either. The equivalent
  code path on the single-tweet page (`/`) — `popstate`-driven style
  restoration — was verified working correctly with real DOM evidence
  (Phase 7), and manually changing style via the UI (no navigation involved)
  also works correctly. The bug is narrow: initial hydration of style
  specifically on the thread page's shared-link path.
  **Impact:** cosmetic only — the thread's tweets, order, and export still
  work; a restored share link just might show default styling instead of the
  saved one. **Priority:** P2. **Investigate:** whether this is a React
  hydration/Suspense interaction specific to how `ThreadBuilder`'s own
  mount-time fetches interleave with the parent's initial render, using
  React DevTools' Profiler (not available in this session) rather than more
  manual browser-automation probing.

## Deferred (security-adjacent, not implemented this session)

- **Rate limiting on `/api/tweet/:id` and `/api/image-proxy` (plan 3B/OV-1) was
  planned but not implemented.** Both routes are public and unauthenticated,
  with no cap on request volume — a real cost/abuse-amplification risk if this
  ever gets real traffic. Not a data-exposure or injection vulnerability (the
  SSRF-hardening — exact-hostname allowlist, https-only, redirect
  re-validation, size cap, MIME check — IS implemented and verified working),
  just an unbounded-usage gap. Acceptable for a tutorial-scale demo; add
  Upstash/Vercel KV-backed rate limiting (fail-open on backend errors, per
  the plan) before any real public/production traffic.

## Deferred verification (not converted to PASS without evidence — see plan file)

- [ ] Emoji rendering in export
- [ ] Multi-image tweet export
- [ ] Manual clipboard verification in Aside / real Safari (automation-inconclusive this session)
- [ ] Delayed-image handling under real network latency
- [ ] Delayed-font handling under real network latency
- [ ] Broken-image handling (a media URL that 404s after passing the proxy)
- [ ] Oversized-export timeout/error behavior (very large thread at 3x scale)
- [ ] WebKit/Safari clipboard validation (Playwright's `webkit` approximates but isn't identical to real Safari)

## Deferred features (scope, from the CEO review — see plan file for full rationale)

- [ ] Browser extension for one-click capture from x.com (D7)
- [ ] Public headless generation API/CLI (D8)

## Deferred polish

- [ ] Broader mobile layout polish beyond the responsive baseline
- [ ] Deeper accessibility audit (current baseline: keyboard-operable controls, ARIA labels, focus states — not a full audit)
- [ ] Advanced thread URL edge cases (e.g. compact encoding to raise the share-link length ceiling beyond the current ~12-tweet cap)
- [ ] Production-grade monitoring/alerting beyond the basic uptime check recommended in the plan
- [ ] Broader automated E2E coverage (Playwright suite) beyond this session's manual Aside-driven QA
