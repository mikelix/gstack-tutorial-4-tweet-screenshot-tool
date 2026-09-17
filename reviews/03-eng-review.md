# Review 03 — Outside Voice + Engineering Review

```
Date:            2026-09-17
Reviewer role:   Second Opinion (fresh-context subagent), then Engineer
Command:         Outside-voice pass, then /plan-eng-review (against a mentor-authored 12-point charter)
Scope reviewed:  cross-model tensions, then buildability of the reviewed plan
Verdict:         6/8 tensions accepted, 1 softened, 1 skipped; engineering verdict PROCEED WITH FIXES
```

See `docs/external_ai_mentor.md` — the 12-point charter and A-H output
format this engineering review actually ran against was authored by the
External AI Mentor, not gstack's own default `/plan-eng-review` prompt.

---

## Outside-voice pass — stated limitation first

**This did not run as a genuine cross-model check.** Codex CLI and even a
bash shell were unavailable in this environment, so this used the
documented fallback path — a fresh-context Claude subagent, not a different
model or provider. Stated here rather than left implicit, because "outside
voice" implies more independence than a same-model fresh context actually
provides. It still found real things a same-context review would likely
have missed.

| # | Tension | Why it mattered | Resolution |
|---|---|---|---|
| OV-1 | "No secrets" architecture pillar contradicts real rate limiting | Serverless in-memory counters reset every cold start — a rate limiter built that way would silently do nothing | Accepted; plan corrected to Upstash/Vercel KV, fail-open on backend errors. **Never actually implemented in code** — see `04-qa-report.md`'s Evidence Ladder discussion |
| OV-2 | Approved clipboard fix breaks on Safari/iOS | `navigator.clipboard.write()` requires firing within the same synchronous gesture chain as the click; the approved "await fonts, await capture, then write" fix violates that | Accepted; fixed to pass a `Promise<Blob>` directly into `ClipboardItem`, never awaited first |
| OV-3 | Video-tweet export undefined | Would have shipped as "whatever frame the browser happens to paint," randomly | Accepted; force poster frame + play-icon badge |
| OV-4 | Thread share-link URL length uncapped | A real thread could silently produce a broken/truncated share link | Accepted; hard cap ~12 tweets, explicit message, never silent truncation |
| OV-7 | Premature "TweetCanvas will obviously be shared" assumption | Asserted before any thread code existed | Softened to an explicit re-evaluation checkpoint rather than treated as settled |
| OV-5, OV-6, OV-8 | (lower-value tensions) | — | 1 skipped as low-value given independently-verified evidence; remainder accepted |

## Engineering review — the most consequential finding in the project

**B1 — the image-proxy "fix" from the CEO review was never actually wired to
any real DOM element.** `react-tweet` renders plain `<img>` tags pointing
straight at `pbs.twimg.com`; nothing in the CEO-reviewed plan rewired that.
A "fix" that fixes nothing. This single finding is why T1.5 (a mandatory
spike, not optional) was inserted before any broad implementation — see
`04-qa-report.md` for how the spike resolved it.

| # | Finding | Severity | Remedy |
|---|---|---|---|
| B1 | Image-proxy fix never connected to real code path | Highest — plan's own SSRF hardening would never have been used | T1.5 spike, mandatory, gating broader implementation |
| B2 | SSRF hardening incomplete | No redirect re-validation, protocol check, size cap, MIME check | Added all four before any code existed |
| B3 | No wait for images to finish decoding before capture | Same silent-wrong-output bug class as the font race (2A) | `await Promise.all(images.map(img => img.decode()))`; emoji rendering also named in the test plan for the first time here |
| B4 | Rate-limiter had no defined failure behavior | If it fails closed on an Upstash outage, a second infra dependency takes the whole app down — even though the already-accepted single-point-of-failure on the X endpoint was fine | Fail-open specified in the plan (see OV-1 for whether this was ever built) |
| B5 | Thread per-tweet vs. whole-thread styling scope undecided | Affects the URL-length cap math from OV-4 | Decided: shared style across the whole stack |

## Decision

**PROCEED WITH FIXES.** Implementation sequencing changed: insert T1.5
before broad Route Handler code. Start implementation immediately.

## What was NOT reviewed here

- The outside-voice pass's own limitation (same-model fresh context, not a
  genuine cross-model check) is stated above, not corrected — a future
  project on a host with Codex CLI or bash available should use the
  documented genuine cross-model path instead.
- Whether B1-B5's fixes were actually *built*, not just planned, is a
  separate question this review cannot answer — see `04-qa-report.md`.
