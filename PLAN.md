# PLAN — gstack-tutorial-4

Scope, team topology, verification approach, ranked risks, Definition of Done.
Authored following [`gstack-tutorial-3/PLAYBOOK.md`](../gstack_tutorial3/PLAYBOOK.md)
§8 "Adapting this to Tutorial No. 4" — this repo (the tweet-screenshot-tool
app itself) doubles as both the demo project and the tutorial repo, the same
way tutorial #3's own `starter/` doubled as working pipeline and teaching
material.

---

## 1. Scope

**Subject.** Not a new technical domain (tutorial #3 was video captioning;
this one is a Next.js tweet-screenshot tool) — the actual subject is a
**process upgrade**: a second, independent AI (the "External AI Mentor," see
[`docs/external_ai_mentor.md`](docs/external_ai_mentor.md)) sitting above
gstack's own specialist roles, translating gstack's raw output into the next
precision prompt, in a loop the reader can run themselves:

```
You -> External AI mentor -> optimized strategic prompt -> gstack specialist team
   -> evidence / code / QA -> you verify -> next optimized prompt
```

**The one thing a reader can do afterwards that they could not before:** run
a second, independent AI alongside gstack — in a *separate* session/provider,
not a subagent inside the same context — specifically to draft the prompts
that go into gstack's specialist roles, and know from a real worked example
what that mentor is actually good for (translating raw review output into a
decision a time-constrained human can evaluate; catching specific errors the
specialist team made, like the html2canvas overreach and the "no secrets"
contradiction; and intervening when a debugging session stops converging,
something the AI doing the debugging is not positioned to notice from
inside it).

**In scope**
- The full five-review audit trail (`reviews/01`-`05`), each one honestly
  cross-referencing where the External AI Mentor authored the actual prompt
  gstack's review ran against — see `docs/external_ai_mentor.md`.
- A runnable verification script (`verify.ps1`/`verify.sh` — see §3) that
  checks what this project can actually check mechanically: typecheck,
  lint, build, and the three live SSRF-proxy probes documented in
  `reviews/04-qa-report.md`.
- The Evidence Ladder (10 levels, `reviews/04-qa-report.md`) as this
  tutorial's verification *framework* — the honest replacement for tutorial
  #1-#3's mechanical gate chain, because this project's real risks are
  silent-wrong-output bugs (the avatar bug) that a pass/fail script cannot
  catch by itself; only climbing the ladder (culminating in a human looking
  at a real exported pixel) catches them.
- A reusable session-transcript extractor (`docs/extract_transcript.py`) —
  a genuinely new artifact this tutorial adds to the series' own toolkit.

**Out of scope (stated, not hidden)**
- A mechanical T1-T5-style gate chain like tutorials #2/#3 had. This
  project's central lesson (Evidence Ladder, `reviews/04-qa-report.md`) is
  explicitly that a passing mechanical check is not proof of correct
  output for a pixel-generation feature — building a gate chain that implies
  otherwise would undercut the tutorial's own thesis. What *is* mechanically
  checked is scoped narrowly and honestly in §3 below.
- A genuine cross-model outside-voice pass. `reviews/03-eng-review.md`
  states plainly that this project's "outside voice" was a same-model
  fresh-context subagent, not Codex or another provider, because neither
  was available in that environment. Stated as a gap, not silently upgraded
  for the tutorial's sake.
- Rebuilding what's already missing. `tweet-screenshot-tool-plan.md`, the
  primary source for most of this project's own history, was deleted before
  a git repository existed to track it (see the repo's initial commit
  message). This tutorial does not pretend to reconstruct it byte-for-byte
  — the five-review split is built from the retrospective document and this
  session's own record, and says so.
- A second, formal automated test suite retrofitted after the fact. The gap
  (no unit tests were written) is real and stated in `reviews/05-ship.md`;
  fixing it belongs to actual project work, not to padding this plan.

**Positioning (concrete claim, not a percentage)**
This is a process tutorial about *running a second AI as a review/drafting
layer*, not a claim that doing so guarantees better code. The falsifiable
claim: a reader who already has gstack working can add an external-mentor
loop to their next project and point to at least one concrete moment where
the mentor caught something the specialist team's own review missed — the
html2canvas correction, the "no secrets" contradiction, or the
debugging-thrash intervention are the three real, checkable examples this
project provides (`docs/external_ai_mentor.md`).

---

## 2. Team topology

| Role | Command | Duty | Ran this project? |
|---|---|---|---|
| External AI Mentor | (separate session, no gstack command) | Translate gstack's output into the next precision prompt; correct specific errors; intervene on stalled debugging | Yes — see `docs/external_ai_mentor.md`. **Above** the table below, not one row inside it. |
| CEO | `/plan-ceo-review` | Scope, positioning, premise challenge | Yes — `reviews/01-ceo-review.md` |
| PM | (none — see gap) | Task breakdown | **Not run separately** — stated gap, `reviews/02-spec.md` |
| Second Opinion | fresh-context subagent (documented fallback, not genuine cross-model) | Independent tension-finding before eng review | Yes, with a stated limitation — `reviews/03-eng-review.md` |
| Engineer / Eng Reviewer | `/plan-eng-review` (against a mentor-authored charter) | Buildability, the B1-B5 findings | Yes — `reviews/03-eng-review.md` |
| QA / Browser QA | manual QC loop + Aside | Silent-wrong-output detection, the Evidence Ladder | Yes — `reviews/04-qa-report.md` |
| DevOps / Ship | Ship Mode (mentor-authored) | Finalize, deploy, disclose gaps | Yes — `reviews/05-ship.md` |

**Authority note, adapting tutorial #2/#3's two-key contract:** the mentor
never touches the repository or talks to gstack directly — every exchange
crosses through the human. On a genuine disagreement between the mentor's
recommendation and gstack's own output, the human decides; neither AI's
opinion is binding on its own. This is a weaker, single-key contract
compared to tutorial #2's "physics wins" rule, deliberately — the mentor's
job is to inform the human's decision, not to override the specialist
team's.

---

## 3. Verification approach

No T1-T5 gate chain (see §1's Out of scope). Instead, two layers:

**Mechanical (runnable, narrow, honest about what it can't catch):**
`verify.ps1` / `verify.sh` runs, in order: `tsc --noEmit` → `eslint` →
`npm run build` → three live probes against `/api/image-proxy` (bad host →
expect 400, non-HTTPS → expect 400, legit host → expect 200). Exits 2
(VOID) if the target dev/prod server isn't reachable at all, rather than
silently skipping the probes and reporting green.

**Evidence Ladder (the actual verification discipline this tutorial
teaches):** ten levels, idea through human production test, documented in
full in `reviews/04-qa-report.md`. The avatar bug is the worked example of
why level 5 ("looks like proof, isn't") is a trap, and why nothing below
level 7 (a human or AI actually looking at the output pixels) counts as
evidence for a pixel-generation feature.

---

## 4. Ranked risks

1. **The mentor pattern doesn't generalize past this one project.** Every
   correction attributed to the mentor in `docs/external_ai_mentor.md` is
   real and sourced from the PDF transcript, but four data points isn't
   proof the pattern reliably pays for itself on a different project. State
   this honestly in `TUTORIAL.md` rather than oversell it.
2. **The deleted plan.md undermines trust in the audit trail.** Addressed
   directly in `reviews/05-ship.md` rather than hidden — but a skeptical
   reader is right to weigh this five-review reconstruction as slightly
   less authoritative than tutorial #3's reviews, which were genuinely
   written at the time.
3. **No genuine cross-model second opinion.** If Tutorial No. 4 is authored
   on a host where Codex CLI or another provider *is* available, re-running
   the outside-voice pass for real (not the same-model fallback) would
   strengthen the tutorial's own claims about independent review.
4. **PowerShell/Bash inconsistency in this environment** (noted in
   `reviews/05-ship.md`) cost real tool calls. Low-severity, but worth a
   troubleshooting-appendix entry in `TUTORIAL.md`, same as tutorial #3's
   PowerShell-quoting appendix.

---

## 5. Definition of Done

- [x] `reviews/01`-`05` complete, each with a one-word verdict, each
      honestly cross-referencing `docs/external_ai_mentor.md` where the
      mentor drove the content
- [x] `docs/external_ai_mentor.md` documents the mentor pattern with at
      least the four sourced correction examples, not asserted generally
- [x] `verify.ps1`/`verify.sh` runnable, with a stated VOID condition
- [x] `TUTORIAL.md` + `.zh.md` walk a reader through running the
      mentor-loop pattern themselves, not just reading about this project's
      instance of it
- [x] The Evidence Ladder is presented as this tutorial's verification
      framework, explicitly contrasted with tutorials #1-#3's gate-chain
      model, not silently dropped
- [x] `ChatGPT-gstack-20260917.pdf` and the manual-testing screenshots have
      had a privacy/content review before any public push — see
      `docs/TUTORIAL_4_PRIVACY_REVIEW.md` (PDF stays private; screenshots
      clear; one open history decision flagged for the actual ship step)
- [ ] Known gaps (rate limiting never built, thread-style bug, no automated
      tests, deleted plan.md) restated in release notes, not hidden
- [x] McKinsey-style bilingual deck — `dist/gstack-tutorial-4_{EN,ZH}.pptx`,
      20 slides each, verified structurally (`_build/validate_content.py`),
      privacy-scanned on rendered output (`_build/verify_deck.py`,
      `docs/TUTORIAL_4_DECK_PRIVACY_CHECK.md`), and visually inspected
      slide-by-slide (`docs/TUTORIAL_4_DECK_MANIFEST.md`). Market-value
      pricing against tutorial #3's grounded design-agency-tier methodology
      is a separate, not-yet-done follow-up.
