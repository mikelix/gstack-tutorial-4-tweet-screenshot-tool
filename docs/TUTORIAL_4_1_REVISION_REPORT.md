# Tutorial No. 4.1 — Revision Report

```
Release status: READY_FOR_HUMAN_TUTORIAL_4_1_REVIEW
Date:           2026-09-18
Supersedes:     Tutorial No. 4 (docs/TUTORIAL_4_RELEASE_REPORT.md), which
                remains intact as the historical record of the first release.
```

## What this revision is

A second case study on the same codebase, run after the original Tutorial
No. 4 app (`docs/TUTORIAL_4_RELEASE_REPORT.md`) was already live in
production. Two real events drove it: a human product design review that
judged the shipped app functionally correct but visually unfinished, and a
human-reported production bug (thread export hanging on media-heavy
threads) that turned out to be broader — and more interesting to debug —
than first reported. Both are documented as a teaching case study, not
just fixed silently.

## Application

- **Production URL:** https://tweet-screenshot-tool.vercel.app (unchanged
  from the original Tutorial No. 4 release — same app, revised in place)

## What changed

**Code** (`src/`) — presentation-layer redesign (Direction A, "Quiet
Creator Tool": persistent header/nav, headline hierarchy, two-column
preview + inspector layout, export button hierarchy, mobile overflow fix)
plus one correctness fix in the export pipeline
(`src/lib/export-image.ts` — see Part 22). Export architecture, API
routes, image-proxy security, and the exact DOM node the app rasterizes
were confirmed byte-for-byte unchanged from pre-revision `main` before
this revision's code was accepted — a design or bug-fix pass does not get
to quietly touch what a prior correctness review already signed off on.

**Tutorial** (`TUTORIAL.md` / `TUTORIAL.zh.md`) — four new Parts (20-23),
appended after the original Part 18, teaching the design review, the
X Broadcast fidelity investigation, the thread-export debugging session,
and the extended human-evidence ladder. The original Parts 0-18 are
unmodified.

**Companion artifacts** (`dist/*.docx`, `dist/*.pptx`) — regenerated to
include a condensed Tutorial 4.1 section; see
`docs/TUTORIAL_4_DOCUMENT_MANIFEST.md` and
`docs/TUTORIAL_4_DECK_MANIFEST.md` for exactly what was added.

## Teaching artifacts

| Artifact | Path |
|---|---|
| English Markdown tutorial (Parts 20-23 added) | [`TUTORIAL.md`](../TUTORIAL.md) |
| Chinese Markdown tutorial (Parts 20-23 added) | [`TUTORIAL.zh.md`](../TUTORIAL.zh.md) |
| English Word executive memo | [`dist/gstack-tutorial-4_EN.docx`](../dist/gstack-tutorial-4_EN.docx) |
| Chinese Word executive memo | [`dist/gstack-tutorial-4_ZH.docx`](../dist/gstack-tutorial-4_ZH.docx) |
| English slide deck | [`dist/gstack-tutorial-4_EN.pptx`](../dist/gstack-tutorial-4_EN.pptx) |
| Chinese slide deck | [`dist/gstack-tutorial-4_ZH.pptx`](../dist/gstack-tutorial-4_ZH.pptx) |

## Verification evidence

| Check | Result |
|---|---|
| Public repo code sync vs. private working repo | PASS — the 10 changed/new `src/` files are byte-for-byte identical between repos |
| Production application build (`npm run build`) | PASS |
| Lint (`npm run lint`) | PASS |
| Local production smoke test (plain tweet, video tweet, previously-failing thread, Broadcast fixture) | PASS — all exported successfully, zero console errors, no 375px overflow |
| Export byte-hash regression (plain-text tweet, before vs. after the video-export fix) | PASS — byte-for-byte identical, `sha256 eb9b38e6392fad1ea450e77fff3d7423b58ee5b9605450b450f2f66c5490785b`, 405691 bytes |
| Markdown EN/ZH structural parity (`_build/verify_tutorial_parity.py`) | PASS — 29/29 H2, 12/12 H3, 65/65 checkboxes, 24/24 code fences, 15/15 tables, exact section-order match |
| DOCX/PPTX rebuild and structural/privacy validation | See below (Phase 13-17 of the revision process) |
| Full-repository privacy scan (`_build/verify_repo_privacy.py`) | See below |
| Human production sign-off (design revision) | Complete — recorded in the private working repo's `docs/DESIGN_REVIEW_4_1_RELEASE.md` |
| Human production sign-off (thread/video export fix) | Complete — Download PNG, Copy image, and a Windows 11 Paint paste-and-look confirmation, all against the live production URL |

## Private material intentionally excluded

Same categories as the original release (`docs/TUTORIAL_4_PRIVACY_REVIEW.md`),
plus, specific to this revision:

- The private working repository's full evidence trail (screenshots,
  process logs) beyond what's reproduced here as vetted, cropped, or
  regenerated public-safe evidence
- Any screenshot showing personal browser chrome (bookmarks bar, other
  open tabs) — cropped to remove that chrome before inclusion, or excluded
  entirely where cropping wasn't sufficient
- Local file-system paths, process IDs, and machine-specific identifiers
  from the debugging session

## Known limitations (current, after this revision)

- X Broadcast (`x.com/i/broadcasts/...`) rich preview cards do not render
  — documented upstream limitation, Part 21. Not fixable within the free
  syndication data path this project deliberately restricts itself to.
- Thread shared-link style preset doesn't always restore on first load —
  pre-existing, unrelated to this revision (`TODOS.md`).
- No rate limiting on the public API routes — pre-existing, unrelated to
  this revision (`TODOS.md`).
- Emoji rendering and multi-image thread export remain implemented but
  not empirically verified.

## Reproducibility

```bash
# Clone
git clone https://github.com/mikelix/gstack-tutorial-4-tweet-screenshot-tool.git
cd gstack-tutorial-4-tweet-screenshot-tool

# Install and run locally
npm install
npm run dev
# Single tweet:   http://localhost:3000
# Thread builder: http://localhost:3000/thread

# Production build
npm run build

# Regenerate and validate the tutorial artifacts
python _build/build_docx.py
python _build/build_deck.py
python _build/verify_tutorial_parity.py
python _build/verify_doc_structure.py
python _build/verify_docx.py
python _build/verify_doc_privacy.py
python _build/validate_content.py
python _build/verify_deck.py
python _build/verify_repo_privacy.py
```

## License

MIT — see [`LICENSE`](../LICENSE).

## Final status

**`READY_FOR_HUMAN_TUTORIAL_4_1_REVIEW`**
