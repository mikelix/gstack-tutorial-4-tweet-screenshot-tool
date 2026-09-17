# Reusable gstack Project Operating System

The reusable asset from Tutorial No. 4 is not the Tweet Screenshot Tool's
code — it's the 16-stage sequence that produced it. This document exists to
be copied onto your *next* project, kept concise enough to actually use as
a checklist rather than a document to admire. Full narrative context for
every stage lives in `TUTORIAL.md` Parts 0-18; this is the compressed,
reusable form (`TUTORIAL.md` Part 17, "Reusable gstack Project Operating
System").

**How to size it.** This project ran one domain reviewer's worth of
independent challenge (stage 5), not two, and skipped a dedicated PM role
(stage 2) because the CEO review already covered it. Copy the *judgment*
about when a stage can be folded into another, not the exact role count.

| # | Stage | Purpose | Expected output | Exit criterion | Typical human gate |
|---|---|---|---|---|---|
| 0 | Problem framing | Challenge the premise before scoping a solution | A verified fact (or its absence) that determines feasibility | The premise has been checked against reality, not assumed | None — this stage is prerequisite to every later gate |
| 1 | AI CEO | Product scope, positioning, what's in vs. out | A review document with individually-resolved decisions | Every scope decision has an explicit reason, not a batch approval | Human reads and can restate the one fact that shaped the architecture |
| 2 | AI PM | Task breakdown, dependency ordering | An ordered implementation task list with priorities | Every task has a stated dependency and acceptance criterion | Human confirms the sequence matches their own priority sense |
| 3 | Architecture | Choose the components and data paths | A diagram + component table, grounded in verified library behavior | Every arrow in the diagram is either verified or explicitly flagged as an assumption | Human accepts the fewest-moving-parts tradeoff |
| 4 | Security + UX | Close obvious holes and gaps before code exists | A control list (security) and a state list (UX) | Every control has a concrete bypass it prevents, named | Human accepts the residual risk that remains |
| 5 | Independent second opinion | Find contradictions between decisions, not just typos | A tension table: tension / contradiction / resolution | Each tension is resolved with a decision, not silently dropped | Human reviews any tension that was skipped or softened |
| 6 | Engineering review | Test whether the plan can actually be built as written | A findings list, classified (BLOCKER / DECISION / TEST REQUIREMENT / DEFER / NO ACTION) | Every BLOCKER has an inserted remediation step before implementation proceeds | Human accepts the verdict (PROCEED / PROCEED WITH FIXES / HOLD) |
| 7 | High-risk spike | Resolve the single riskiest technical unknown with real code, before broad implementation | A minimal reproduction, a root cause, a fix, and visual proof | The artifact the spike produced has been looked at, not just executed | Human reviews the visual proof directly |
| 8 | AI Engineer | Build vertical slices that each produce evidence | Working code, in phases, with component boundaries stated | Each phase compiles, runs, and produces an inspectable artifact | Human spot-checks one slice before the next begins |
| 9 | Evidence checkpoint | Decide how much verification a given claim needs | A climb up the Evidence Ladder appropriate to the claim's risk | The claim has reached the ladder level its risk requires (see `TUTORIAL.md` Part 11) | Human agrees the evidence is strong enough for this claim |
| 10 | Browser QA | Verify real application behavior in a real browser | Deterministic test runs, screenshots, exported artifacts | Every claim about UI behavior has been observed in a real browser, not inferred from code | None required if stage 9's bar is met — informs it |
| 11 | Human-in-the-loop test | Confirm subjective quality and usability no automation can judge | A human's direct report of using the product | A human has actually used the feature end to end | This IS the human gate |
| 12 | Minimal QC | Distinguish release-blocking issues from everything else | A fix-list and a defer-list, each with a reason | Every remaining issue is sorted, none left ambiguous | Human confirms the defer-list is acceptable for this release |
| 13 | Deploy | Ship to production infrastructure | A live URL, a clean production build | The account-authorization step was done by a human, not automated | Human performs the login/authorization step personally |
| 14 | Production smoke test | Confirm the live thing actually works, not just the local build | A real pass through the core flow(s) against the live URL | Zero fatal errors in the tested flow | Human or AI browser confirms against the live URL |
| 15 | Freeze + retrospective | Record what shipped, what's deferred, and what was learned | A known-limitations list and a lessons list | Every known gap is named, none silently dropped | Human reads and accepts the final disclosure |

## Notes on reuse

- **Stages can merge when the underlying work already covers them.** Stage
  2 (AI PM) folded into stage 1's own output in this project — a stated
  choice, not a silent skip; see `TUTORIAL.md` Part 2.
- **The External AI Mentor pattern is a layer above this table, not a row
  in it.** It sits between the human and every stage, translating each
  stage's raw output into the next stage's precision prompt — see
  `docs/external_ai_mentor.md`. Its generalization past this one project is
  unproven; test it on your own next project before trusting it blindly.
- **Stage 7 (the high-risk spike) is the stage most likely to get skipped
  under time pressure, and the one this project's own evidence says matters
  most** — it's what caught the avatar bug (`TUTORIAL.md` Part 7) before it
  reached production.
- **The exit criteria are deliberately about evidence, not about time
  spent.** A stage is done when its exit criterion is met, not when a fixed
  amount of effort has gone into it.
