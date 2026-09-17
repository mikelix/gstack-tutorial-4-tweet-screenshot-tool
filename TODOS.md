# TODOS

Deferred, non-blocking work for the Tweet Screenshot Tool. None of these block
Tutorial No. 4 — the core paste → customize → export flow (single tweet and
thread) works and was verified with real evidence (see plan/implementation log).

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

- [ ] Real video tweet export (poster-frame swap implemented, unverified against a real `<video>`)
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
