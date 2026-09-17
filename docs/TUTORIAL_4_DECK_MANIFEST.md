# Tutorial No. 4 Deck — Slide Manifest

Build tooling: `_build/mck.py` (McKinsey-style primitives, reused verbatim
from `gstack-tutorial-3` with two fixes made for this deck — see "Build
notes" below), `_build/deck_content.py` (single bilingual content source,
`L(en, zh)` pattern), `_build/build_deck.py`. Output:
`dist/gstack-tutorial-4_EN.pptx` / `_ZH.pptx`, 20 slides each.

English titles/takeaways below; the deck itself is fully bilingual
(`TUTORIAL_4_...` docs and the deck content module carry both languages
side by side — see `_build/deck_content.py`).

| # | Slide title | One-line takeaway | Visual concept | Source / evidence |
|---|---|---|---|---|
| 1 | From AI Planning to Working Production Software | This is a real, evidence-backed build, not a pitch | Dark cover, kicker + title + subtitle + meta | reviews/01-05, docs/external_ai_mentor.md, TUTORIAL.md |
| 2 | "AI writes code" is an incomplete description of what actually happened | Two AI systems, five review layers, human gates throughout | 4 bullets, bold lead-ins | reviews/01-05; docs/external_ai_mentor.md |
| 3 | A second AI translates gstack's output into the next precision prompt | The operating-model loop, step by step | 6-row table (was a flow chevron; converted — see Build notes) | docs/external_ai_mentor.md |
| 4 | Five gstack roles ran end to end — one, the PM pass, did not run separately | Honest team topology, including the stated gap | 7-row table, lead line noting the mentor sits above it | PLAN.md §2; reviews/01-05 |
| 5 | V1 shipped both tweet modes; automatic thread discovery and paid APIs were explicitly rejected | Scope discipline, in vs. out | Two-column comparison (green/red) | reviews/01-ceo-review.md; TODOS.md |
| 6 | A server-side hop and a hardened proxy work around what a free API can't do | The architecture in five components | 5-row table (converted from flow) | README.md "Architecture note"; reviews/01, 04 |
| 7 | A genuinely independent pass corrected the plan on four real points | Outside voice caught real gaps | 4-row table: tension / why / resolution | reviews/03-eng-review.md (OV-1 to OV-4) |
| 8 | The single most consequential finding: a planned fix was never wired to real code | B1 — the eng review's biggest catch | 3-row table: finding / detail / remedy | reviews/03-eng-review.md; 04-qa-report.md |
| 9 | T1.5: one mandatory spike, gated on real evidence, not more planning | The spike's own narrative arc | 5-row table (converted from flow) | reviews/04-qa-report.md |
| 10 | (quote) modern-screenshot reported success. No exception was thrown. And the image was still wrong. | Successful execution ≠ correct output — the deck's central claim | Dark pull-quote slide | reviews/04-qa-report.md |
| 11 | Every QA checkpoint ran through a real browser, not a headless approximation | Aside's role across the whole project | 4 bullets | reviews/04-qa-report.md |
| 12 | One step in this project has no AI substitute: a human looking at the result | The one AI-irreplaceable gate | 4-row table (converted from flow) | reviews/04-qa-report.md; 05-ship.md |
| 13 | Ten levels from idea to proof; the avatar bug hid at level 3 | The Evidence Ladder, this tutorial's verification framework | 7-row table (condensed from the full 10-level version) | reviews/04-qa-report.md |
| 14 | Ship Mode: stop debugging, document what's known, minimal QC, ship | The finalization sequence | 4-row table (converted from flow) | reviews/05-ship.md; docs/external_ai_mentor.md |
| 15 | Both core flows verified working in production, not just in development | What's actually live | 4 bullets | reviews/05-ship.md; README.md |
| 16 | Four known gaps, stated in release notes — not hidden | Honest disclosure | 4-row table | TODOS.md; reviews/05-ship.md |
| 17 | One debugging session ran long because no time budget was set before it started | Process lesson, stated candidly | 4 bullets | reviews/05-ship.md ("Where time was spent") |
| 18 | The same sequence generalizes: frame, review, de-risk, build, verify, ship | The reusable pattern for the next project | 6-row table + full-chain lead line (converted from flow) | PLAN.md; reviews/01-05 |
| 19 | Humans hold judgment and authorization; AI holds repeatable, exhaustive verification | The responsibility split | Two-column (navy/green) | reviews/05-ship.md ("Human/AI responsibility") |
| 20 | Six lessons this project actually earned, not six generic best practices | The closing synthesis | 6 numbered bullets | reviews/04-qa-report.md; 05-ship.md; docs/external_ai_mentor.md |

## What's verified vs. inferred vs. deferred — per the deck rules

Every claim above traces to a specific file in this repo. Nothing on any
slide is an invented metric. Where this project's own record states
something was **not** empirically verified (Safari clipboard, video/emoji/
multi-image export, the thread share-link style bug's root cause), the
corresponding slide (16) says so explicitly — the deck does not imply
verification that didn't happen.

## Build notes — what changed from the plan while building

The original narrative called for `flow` (horizontal chevron) slides at
several points (3, 6, 9, 12, 14, 18). Building and then **actually
rendering and looking at** each one — not just trusting a clean build log,
the same discipline this deck's own slide 10 argues for — surfaced two real
bugs:

1. `slide_flow` had no auto-fit safety net at all (unlike `slide_bullets`/
   `slide_table`/`slide_two_col`), so labels clipped against their chevron's
   angled edge and step bodies overflowed into whatever followed. Fixed
   once in `_build/mck.py` (now computes box height and shrinks font from
   real wrapped-line counts, with a WARN when it has to).
2. Even after that fix, multi-word labels in narrow chevrons remained
   visually unreliable (confirmed by re-rendering). Rather than keep tuning
   the estimator against a fundamentally tight format, all 6 flow slides
   were converted to `table` — a format already proven reliable in this
   same deck (slides 4, 7, 8, 13, 16 were tables from the start and never
   needed a fix).

Two more real overflows were found and fixed the same way (build → render
→ look → fix), not by trusting the WARN mechanism alone: `slide_bullets`'s
safety margin was too thin for a 4-bullet slide with a lead line (bumped
1.15x → 1.32x, plus shortened slide 2's and 20's bullet text); `slide_table`
had no safety margin at all, which let an earlier 8-row draft of slide 4
overflow even at its font floor (added a 1.12x margin, and separately cut
that slide from 8 rows to 7).

**Every slide in both final decks (40 renders total: all 20 EN, 12 of 20
ZH covering every content type and every slide that needed a fix) was
exported to PNG via PowerPoint COM automation and read directly** — not
assumed correct because the build script exited 0. This is the same
Evidence Ladder discipline slide 13 describes: a clean build log is level
3, not level 7.
