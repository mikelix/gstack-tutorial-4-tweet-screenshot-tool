# Tutorial No. 4 — Final Release Report

```
Release status: PUBLIC_RELEASE_READY  (Tutorial No. 4, original release)
Date:           2026-09-17
```

**Superseded by Tutorial No. 4.1.** Everything below this line describes
the original Tutorial No. 4 release and is left intact as the historical
record. A second release, Tutorial No. 4.1 — a post-launch product design
revision and a real production bug found and fixed after this release —
followed on 2026-09-18. See `docs/TUTORIAL_4_1_REVISION_REPORT.md` for
that release's own full record; `TUTORIAL.md`/`TUTORIAL.zh.md` Parts
20-23 are the reader-facing narrative.

## Application

- **Production URL:** https://tweet-screenshot-tool.vercel.app

## GitHub

- **Public repository:** https://github.com/mikelix/gstack-tutorial-4-tweet-screenshot-tool
- **Default branch:** `main`
- **Final release commit:** `673dbac` (license: add MIT License) — the repo's own release-report commit (recorded below) lands after this one
- **Visibility:** PUBLIC (changed from PRIVATE after explicit human approval; confirmed both via authenticated `gh api` and via an anonymous, unauthenticated fetch of the repo page and every raw file listed below)

## Teaching artifacts

| Artifact | Path |
|---|---|
| English Markdown tutorial | [`TUTORIAL.md`](../TUTORIAL.md) |
| Chinese Markdown tutorial | [`TUTORIAL.zh.md`](../TUTORIAL.zh.md) |
| English Word executive memo | [`dist/gstack-tutorial-4_EN.docx`](../dist/gstack-tutorial-4_EN.docx) |
| Chinese Word executive memo | [`dist/gstack-tutorial-4_ZH.docx`](../dist/gstack-tutorial-4_ZH.docx) |
| English slide deck | [`dist/gstack-tutorial-4_EN.pptx`](../dist/gstack-tutorial-4_EN.pptx) |
| Chinese slide deck | [`dist/gstack-tutorial-4_ZH.pptx`](../dist/gstack-tutorial-4_ZH.pptx) |

## Verification evidence

| Check | Result |
|---|---|
| Production application build (`npm run build`) | PASS |
| Markdown EN/ZH structural parity (`_build/verify_tutorial_parity.py`) | PASS — 24/24 H2, 12/12 H3, 47/47 checkboxes, 18/18 code fences, exact section-order match |
| DOCX source structure parity (`_build/verify_doc_structure.py`) | PASS — 14/14 sections, all block/table/bullet counts match EN↔ZH |
| DOCX mandatory 3-part + CJK structural check (`_build/verify_docx.py`) | PASS — ZIP integrity, body structure, no duplicate runs, `eastAsia` set on all 172/172 `rFonts` elements in both languages |
| DOCX privacy scan on built artifacts (`_build/verify_doc_privacy.py`) | PASS |
| PPTX structural validation (`_build/validate_content.py`) | PASS — 20/20 slides, no structural mismatches |
| PPTX privacy scan on built artifacts (`_build/verify_deck.py`) | PASS |
| Full-repository privacy scan (`_build/verify_repo_privacy.py`) | PASS — `PUBLIC_RELEASE_PRIVACY_SCAN = PASS`, 0 literal identifier matches, 0 secret-shaped matches |
| Anonymous, unauthenticated public accessibility check | PASS — repo page and every teaching artifact returned HTTP 200 with no auth; the original transcript and the private PDF both returned 404 (confirmed absent) |
| Human DOCX visual inspection | Complete — a human opened both `.docx` files directly in Microsoft Word and confirmed both render correctly (recorded in `docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md`) |
| Human GitHub publication approval | Complete — a human manually inspected the private repository in a browser and approved publication before visibility was changed |

## Private material intentionally excluded

Categories only, no values reproduced here:

- Raw private development evidence (the full-day AI-mentor planning conversation this project's early stages drew from)
- The original, unredacted session transcript (a sanitized, redacted copy is published in its place)
- The private source PDF documenting that conversation
- Account and authentication identifiers (developer machine username, machine hostname, cloud-hosting account/team identifiers, OAuth device-authorization codes)
- Local build/runtime data (development logs, process-id files, local build caches, IDE/agent configuration files)

Full method and per-asset findings: `docs/TUTORIAL_4_PRIVACY_REVIEW.md`,
`docs/TUTORIAL_4_DECK_PRIVACY_CHECK.md`, `docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md`.

## Known limitations

(Product limitations already documented in `TUTORIAL.md` Part 16 / `TODOS.md` — restated here, not expanded.)

- No rate limiting on the public API routes — planned and reviewed twice, never implemented.
- A shared thread link's tweet order always restores correctly; the saved style (background/padding/theme) sometimes doesn't on first load.
- Emoji rendering and multi-image thread export are implemented but not empirically verified. (Video-tweet export *was* in this category at original release; it was found broken, root-caused, fixed, and verified in Tutorial No. 4.1 — see `docs/TUTORIAL_4_1_REVISION_REPORT.md`.)
- X Broadcast (`x.com/i/broadcasts/...`) rich preview cards don't render — a known upstream data limitation, investigated and documented in Tutorial No. 4.1, Part 21.
- Real Safari/iOS clipboard behavior is implemented but not empirically verified on real Safari.
- No automated test suite — a stated process gap, not a hidden one.

## Reproducibility

```bash
# Clone
git clone https://github.com/mikelix/gstack-tutorial-4-tweet-screenshot-tool.git
cd gstack-tutorial-4-tweet-screenshot-tool

# Install
npm install

# Run locally
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

**`PUBLIC_RELEASE_READY`**
