# Review 01 — CEO (`/plan-ceo-review`)

```
Date:            2026-09-17
Reviewer role:   CEO
Command:         /plan-ceo-review, SCOPE EXPANSION mode
Scope reviewed:  product definition, architecture shape, scope, security posture (Section 3), UX (Section 11)
Verdict:         PASS, with a mid-review scope redefinition (thread mode)
```

See `docs/external_ai_mentor.md` — the External AI Mentor drafted the reply
to nearly every finding below; none of these were the human's own first-draft
prompt.

---

## Premise challenge (Step 0)

The question that had to be answered before any architecture decision: is
there already a working open-source competitor? **Verified live, not
assumed** — the two closest candidates (Twimage, Laureate) are both built on
the official X API, which has had **no free tier since 2026**. That single,
checked fact eliminated every existing competitor and set the entire
architecture: whatever this project builds cannot depend on a paid API,
which rules out both "fork a dead-API app" and "server-side headless-browser
screenshot" as alternatives.

**Decision:** proceed with `react-tweet` (renders via X's free public
syndication endpoint) + `modern-screenshot` (DOM→PNG) on Next.js/Vercel.

## Architecture (Section 1)

Initial dependency graph and state machine. The syndication endpoint blocks
direct browser CORS requests — verified live against the real endpoint, not
assumed — meaning a server-side hop is structurally required. Next.js Route
Handlers reuse `react-tweet`'s own server-side fetch pattern rather than
hand-rolling a proxy.

## Security (Section 3)

Found and closed, before any code existed: an SSRF hole in the
not-yet-built image proxy. Host-substring matching would have let
`evil-twimg.com.attacker.net` through; fixed to exact-hostname matching.
(The proxy's remaining hardening gaps — redirect re-validation, protocol
check, size cap, MIME check — surfaced later, in the engineering review; see
`03-eng-review.md`.)

## Findings requiring a product decision

| # | Finding | Why it mattered | Remedy | Gate |
|---|---|---|---|---|
| 2A | Silent wrong font if capture fires before web fonts finish loading | Wrong output, zero error signal — the worst class of bug | `await document.fonts.ready` before capture | `AskUserQuestion`, accepted |
| 3A | Image-proxy SSRF (see Security above) | Classic, actively-scanned vulnerability class | Exact-hostname allowlist, https-only | `AskUserQuestion`, accepted |
| 4A | Stale response overwrites a newer one | User changes their mind about which tweet to load mid-fetch; the *older* response could win | Request-token + `AbortController`, only latest response applied | `AskUserQuestion`, accepted |
| 4B | Back/forward navigation and style state | Versioned URL state needed to survive `popstate` | Verified against real DOM attributes in implementation (Phase 6) | `AskUserQuestion`, accepted |
| 8A/9 | Observability, post-deploy verification | No plan for confirming a deploy actually works | Live smoke test against the deployed URL, not just local | `AskUserQuestion`, accepted |
| 11A | Thread partial-failure UX | A failed tweet in a thread must never be silently dropped from export | Inline error card, export blocked until resolved or removed | `AskUserQuestion`, accepted |
| 11B/11C | Mobile responsiveness, accessibility baseline | Table-stakes for a public tool | Keyboard-operable controls, ARIA labels, focus states (baseline, not full audit — see `TODOS.md`) | `AskUserQuestion`, accepted |

## Scope expansion ceremony

6 of 8 proposed expansions accepted: export polish, clipboard copy,
shareable links, thread mode. **Thread mode was redefined mid-review** —
from "auto-stitch a thread automatically" to "manual multi-URL builder" —
once it became clear no free data source can discover a thread's next tweet
without falling back to a paid API or scraping, both of which this project
explicitly rejects.

## Decision

Proceed to the outside-voice pass (`03-eng-review.md`).

## What was NOT reviewed here

- Whether the engineering plan is actually buildable as written — that's
  the engineering review's job, not the CEO review's (and it found real
  gaps the CEO review missed — see B1 in `03-eng-review.md`).
- A dedicated design review (`/plan-design-review`) was never run separately
  — Section 11 covered UX inside this review instead. Stated here as a
  scope gap, not hidden.
