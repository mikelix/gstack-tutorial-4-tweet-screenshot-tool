# Tutorial No. 4 — Editorial Outline

Editorial map for `TUTORIAL.md` / `TUTORIAL.zh.md`: what each Part teaches,
what evidence backs it, and the one governing lesson it exists to deliver.
Use this to navigate the tutorial, or to check that a claim in the tutorial
has a named source (cross-check against
`docs/TUTORIAL_4_DOCUMENT_MANIFEST.md` for the full provenance table).

| Part | Learning objective | Main evidence | Figures | Governing lesson |
|---|---|---|---|---|
| 0 — Mental model | Replace "AI writes code" with the real two-AI, human-gated loop | `docs/external_ai_mentor.md` | Operating-model diagram, 16-stage sequence diagram | *(sets up Parts 1-18; no single lesson of its own)* |
| 1 — AI CEO | See a premise challenge change an architecture before code exists | `reviews/01-ceo-review.md` | Decisions table | Architecture and scope decisions are cheap to change before code exists |
| 2 — AI Project Manager | Understand a stated process gap and why it's disclosed, not hidden | `reviews/02-spec.md`, `TODOS.md` | — | A task breakdown is only as trustworthy as the plan it came from |
| 3 — Architecture | Trace the tweet-data and export paths and why each hop is structurally required | `README.md`, `reviews/01`, `04` | Two data-flow diagrams, components table | Architecture should remove the most important constraints with the fewest moving parts |
| 4 — Security + UX review | Distinguish security failure, product failure, and user confusion | CEO review §3, §11 | Controls table, UX table | A feature is not finished when only the happy path works |
| 5 — Independent second opinion | Recognize a genuine cross-model tension vs. a rubber-stamp | `reviews/03-eng-review.md` (OV-1 to OV-8) | Tension table | Independent review is valuable when it creates productive disagreement |
| 6 — Engineering review | Classify findings by severity and understand why B1 was a blocker | `reviews/03-eng-review.md` (B1-B5) | Findings table | Product plans describe intent; engineering reviews test whether the intent is implementable |
| 7 — The high-risk spike | Walk the full evidence chain from assumption to visual proof | `reviews/04-qa-report.md` | Investigation narrative, bug/fix/proof sequence | Successful execution is not proof of correct output |
| 8 — AI Engineer implementation | See component boundaries enforced and DRY treated as a hypothesis | Source tree, `reviews/04` | Component boundary table | Build the smallest vertical slice that produces evidence |
| 9 — Aside AI Browser QA | Understand the three separate evidence layers and where each applies | `reviews/04-qa-report.md` | Layer table | Real-browser behavior is a separate evidence layer from code correctness |
| 10 — Human-in-the-loop testing | Name what only a human tester can confirm | `reviews/05-ship.md` | — | AI can produce evidence; a human still decides whether the evidence is good enough |
| 11 — The Evidence Ladder | Use the 10-level ladder to judge how much verification a claim needs | `reviews/04-qa-report.md` | 10-level table | Evidence becomes stronger as it gets closer to the real user and real output |
| 12 — When debugging becomes waste | Recognize when an investigation has stopped reducing uncertainty | `reviews/05-ship.md` ("Where time was spent") | Layer-isolation diagram | Persistence is not progress if the experiment is not reducing uncertainty |
| 13 — Rapid finalization | Sort issues into fix-now vs. defer-and-document | `TODOS.md`, `reviews/05-ship.md` | Fix/defer table | Shipping speed comes from choosing what not to investigate |
| 14 — Deployment and the human authorization gate | Identify the one action only a human can perform | `reviews/05-ship.md` | Agent/human handoff diagram | Consequential authorization remains a human gate even in an AI-native workflow |
| 15 — Production result | Distinguish verified production flows from untested ones | `reviews/05-ship.md`, `README.md` | — | Production evidence matters more than localhost confidence |
| 16 — Known limitations | Sort gaps into implemented-but-unverified / known-bug / deferred / pre-scale-required | `TODOS.md`, `reviews/05-ship.md` | Limitations table | Known limitations are acceptable when they are explicit, bounded, and compatible with the release goal |
| 17 — Reusable operating system | Have a 16-stage checklist ready for the next project | `docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md` | 16-stage table | The reusable asset is not the code — it is the development system that produced the code |
| 18 — Final lessons | Carry ten concrete, earned lessons forward | Synthesis of all prior Parts | — | *(ten lessons, not one — see Part 18 directly)* |
| 20 — Product design 4.1 | See a shipped, working product judged unfinished on trust signals, and revised through the same human-gated discipline | `docs/DESIGN_REVIEW_4_1_*.md` | Engineering-QA vs. product-QA table | Product design is not decoration; it reduces user uncertainty |
| 21 — X Broadcast fidelity | Trace a missing output through five real layers to find where the data actually disappears | `TODOS.md`, `docs/DESIGN_REVIEW_4_1_RELEASE.md` | Five-layer pipeline diagram | Before fixing a missing output, find the first layer where the information disappears |
| 22 — Thread export failure | Watch a plausible first hypothesis get killed by one cheap experiment, then find the real root cause in library source | `src/lib/export-image.ts`, `TODOS.md` | Scale/result/time table, hang mechanism code excerpt | Good debugging is not proving your first hypothesis; it is killing the wrong hypothesis quickly |
| 23 — Human evidence ladder | Extend the Evidence Ladder past "the promise resolved" to real cross-application confirmation | `docs/DESIGN_REVIEW_4_1_RELEASE.md` | Extended Evidence Ladder diagram | Human testing catches failures that automated checks cannot even formulate |

## Supporting sections (not chapter-numbered)

| Section | Purpose | Source |
|---|---|---|
| Troubleshooting | Concrete symptom → cause → response for this project's actual failure modes | Session record |
| Disciplines worth keeping | A ten-item checklist distilled from the whole tutorial | Synthesis |
| Appendix A — Command reference | Only the commands actually needed to reproduce this project | `README.md`, session record |
| Appendix B — Bilingual glossary | Consistent EN/ZH terminology for every recurring concept | Synthesis |
| Appendix C — Definition of Done | Explicit, checkable completion criteria for this documentation phase | `PLAN.md` pattern |
