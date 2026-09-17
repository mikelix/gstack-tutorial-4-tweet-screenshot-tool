# Review 05 — Ship (`/ship`)

```
Date:            2026-09-17
Reviewer role:   DevOps
Command:         Ship Mode (mentor-authored rapid-finalization prompt — see docs/external_ai_mentor.md)
Scope reviewed:  release contents, deployment, known-gaps disclosure
Verdict:         SHIP WITH KNOWN LIMITATIONS
```

---

## Rapid finalization

Once the human confirmed the core prototype looked good enough for the
tutorial, the project explicitly switched modes: stop open-ended debugging,
document non-blockers instead of chasing them, remove diagnostic code,
clean up starter-template residue (page title, metadata, README), run one
final QC pass, ship.

**The mode switch traces to two mentor interventions** (`docs/external_ai_mentor.md`):
first, when shown a transcript of the thread-style bug investigation running
~35 minutes / ~99k tokens with no isolated root cause, the mentor said *"I
would stop this current debugging run now and reset the debugging method"*
and drafted a five-layer binary-search protocol. **What actually happened
next:** the human did not run that specific protocol — having already
completed successful manual testing, they asked for a faster "finalize this
project ASAP" prompt instead, citing "minimal QC and rapid shipping is the
key for any AI startup." The mentor's response was the full Ship Mode
prompt. The underlying principle (stop, timebox, document rather than
chase) survived the pivot even though the specific protocol wasn't the one
executed — worth stating plainly rather than implying the five-layer
protocol was followed when it wasn't.

## Deployment

Vercel deployment required one real human action no AI performed or should
perform: account authentication. The human ran `npx vercel login`
themselves, completed browser-based authorization, confirmed `npx vercel
whoami` succeeded, then handed control back. From there: confirmed auth,
final production build, created the Vercel project (`tweet-screenshot-tool`,
under the project owner's personal Vercel account/team — redacted here; see
`docs/TUTORIAL_4_PRIVACY_REVIEW.md`), deployed via `npx vercel --yes`.
Vercel's own behavior means the first deployment for a new project always
becomes production directly — no separate preview to gate on — so the
production smoke test ran against the live URL immediately.

The `npx vercel`-without-a-global-install distinction, and the exact
numbered deployment sequence (confirm auth → build → create/link project →
preview → Aside smoke test → production → final ship report), came from the
mentor's "Authorize Vercel Deployment and Ship" handoff prompt.

## Human/AI responsibility — what this project actually demonstrated

| Task | Best suited | Why |
|---|---|---|
| Reading a library's real compiled source to verify an API contract | AI | Exhaustive, patient verification an AI does well and a human would reasonably skip |
| Constructing a deterministic reproduction of a race condition | AI | Turns a rare, hard-to-catch bug into a repeatable check |
| Security review of a new public endpoint (SSRF, allowlist correctness) | AI | Systematic, checklist-driven |
| Running the same 3-command QC loop dozens of times | AI | Repeatable, zero fatigue cost |
| Driving a browser through dozens of real-world scenarios | AI | Pace and consistency beyond manual clicking |
| Vercel account login/authorization | Human | A real credential-granting action — the AI explicitly declined to attempt it |
| Judging whether an exported screenshot actually *looks good* | Human | An AI can confirm correct pixels in roughly the right place; not "does this feel right to share" |
| Deciding a bug investigation has gone on long enough | Human | The AI's own debugging ran without resolution across many tool calls; the human's explicit stop instruction ended it |
| Deciding the project moves from review to build | Human, with AI input | Every scope/mode/remedy decision went through the human via `AskUserQuestion` |
| Translating a specialist AI team's output into the next precision prompt | A *different* AI (the mentor), not the same one doing the work | Self-review loses the independence the CEO review's own principle depends on |
| Relaying messages between two separate AI systems | Human | No automated bridge existed; every prompt crossed the gap because a human moved it, and could stop or edit at any point |

## Known, stated gaps (not silent)

- Thread share-link *style* restoration bug — investigated one bounded
  pass (including a full Turbopack cache clear + dev-server restart to rule
  out staleness), root cause not found in the time allotted. Tweets and
  order restore correctly; style sometimes doesn't. `TODOS.md`.
- Rate limiting on both public API routes — planned, reviewed twice
  (OV-1, B4), never implemented in code. Acceptable for a tutorial-scale
  demo; a real gap before real public traffic.
- Video/emoji/multi-image export and real-Safari clipboard behavior are
  implemented but not empirically verified — `TODOS.md`.
- No automated test suite. The plan specified unit tests for URL parsing
  and state encode/decode; none were written. Every verification in this
  project ran through manual Aside-driven browser checks instead, gated on
  finding real, currently-live tweet IDs per scenario — slower and less
  repeatable, and the direct reason several items remain unverified.
- **`tweet-screenshot-tool-plan.md` — the primary source for most of this
  audit trail — no longer exists in the repo.** Deleted during Ship Mode's
  "remove prototype debris" step, and unrecoverable because no git history
  existed at the time (see this repo's own initial commit message). This
  five-review split is reconstructed from the project's own retrospective
  document and this session's own record, not from the original plan file
  itself. Stated here because pretending otherwise would repeat exactly the
  failure this review series exists to prevent.

## Where time was spent without proportional payoff

Two places, named plainly rather than smoothed over:

1. **The thread share-link style bug.** React state was directly confirmed
   correct via temporary instrumentation on every render, yet the rendered
   DOM was still wrong — survived a Strict Mode toggle, a full cache clear,
   and a server restart. The right move would have been timeboxing this
   *before* it consumed as many tool calls as it did, not after.
2. **No automated test suite was written**, despite the plan specifying
   one. Every scenario requiring a real tweet (text, image, long-text) was
   verified by hand-hunting for a currently-live example instead of a mock
   — the direct reason emoji, multi-image, and video-tweet coverage stayed
   incomplete.

A smaller, environment-only cost: an inconsistent `bash` in this session
(missing on first use, present-but-missing coreutils later) cost a handful
of redone tool calls through PowerShell instead — not a real time sink, and
not something either side could have anticipated.

## Final ship verdict

**SHIP WITH KNOWN LIMITATIONS.** Both core flows (single tweet, thread)
verified working in production via real-browser automation and reported by
the human as manually tested and visually confirmed, both locally and
against the deployed Vercel URL.

## What was NOT reviewed here

- No independent second reviewer signed off on the ship decision — the same
  session that built and QA'd the project also made the ship call, gated
  only by the human's own manual test, not by a separate `/ship`-review
  role. Worth naming as a gap Tutorial No. 4's own next iteration could
  close by running a genuinely separate reviewer at this stage.
