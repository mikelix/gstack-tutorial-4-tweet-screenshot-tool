# Tweet Screenshot

Paste an X/Twitter tweet URL, customize it, export a PNG. No X API key required.

**Live demo:** https://tweet-screenshot-tool.vercel.app

## What this project does

Turns a tweet URL into a styled, downloadable image — for blogging, decks, or
sharing a tweet somewhere that isn't X itself. Built as the demo project for
**Gstack Tutorial No. 4** — a worked example of running a second, independent
AI as a review and prompt-drafting layer above gstack's specialist AI roles,
end to end from planning through production deployment — and later extended by
**Tutorial No. 4.1**, a second case study on the same codebase covering a
post-launch product design revision and a real production bug found and fixed
after the first release.

## Features

- Paste a tweet URL → live preview (text, avatar, media, replies count)
- Customize: background preset, padding, export scale (1x/2x/3x), light/dark theme
- Download as PNG, or copy the image straight to your clipboard
- Copy a shareable link that restores the tweet + your styling for someone else
- Manual thread builder (`/thread`): add several tweets, reorder, export as one
  combined image

## Stack

- **Next.js** (App Router, TypeScript) — [`react-tweet`](https://github.com/vercel/react-tweet)
  for pixel-perfect tweet rendering via X's free public syndication endpoint
  (no paid API, no API key)
- **[modern-screenshot](https://github.com/qq15725/modern-screenshot)** for
  DOM → PNG export
- **Vercel** for hosting
- **[Aside](https://aside.com)** — the real-browser tool used for QA during
  development (see the plan/implementation log for the full test evidence)

## Run locally

```bash
npm install
npm run dev
```

Then open:

- Single tweet: `http://localhost:3000`
- Thread builder: `http://localhost:3000/thread`

## Tutorial No. 4 / 4.1

This repo is the demo project for gstack Tutorial No. 4 (Parts 0-18: from
planning to first production deploy) and its extension, Tutorial No. 4.1
(Parts 20-23: a post-launch product design revision and a real production
bug, found and fixed after the first release) — read the full walkthrough,
in either language:

- **English:** [`TUTORIAL.md`](TUTORIAL.md)
- **中文:** [`TUTORIAL.zh.md`](TUTORIAL.zh.md)

Shorter companion artifacts, generated from the same source facts (see
`docs/TUTORIAL_4_DOCUMENT_MANIFEST.md` for provenance):

- **Executive-memo Word documents:** [`dist/gstack-tutorial-4_EN.docx`](dist/gstack-tutorial-4_EN.docx) · [`dist/gstack-tutorial-4_ZH.docx`](dist/gstack-tutorial-4_ZH.docx)
- **Slide decks:** [`dist/gstack-tutorial-4_EN.pptx`](dist/gstack-tutorial-4_EN.pptx) · [`dist/gstack-tutorial-4_ZH.pptx`](dist/gstack-tutorial-4_ZH.pptx)

## Known limitations

- The official X API has no free tier in 2026 — this tool deliberately avoids
  it, fetching tweets via X's public syndication endpoint instead. That
  endpoint is undocumented and unowned by this project; if X changes it,
  tweet loading breaks until `react-tweet` (the library this project depends
  on for that) catches up.
- Thread mode is **manual** — paste each tweet's URL yourself, in order. There
  is no automatic "discover the rest of this thread" feature (the free data
  source can't support it without falling back to paid APIs or scraping,
  which this project intentionally avoids).
- A shared thread link's tweets and order always restore correctly; the saved
  style (background/padding/theme) sometimes doesn't on first load. See
  `TODOS.md` for the known-issue writeup.
- Native photo/video media exposed by X's free syndication data renders and
  exports normally (verified — see Tutorial No. 4.1, Part 22). X Broadcast
  (`x.com/i/broadcasts/...`) rich preview cards are not exposed by that free
  data path, so a tweet quoting one may show as text + link rather than
  X.com's full animated broadcast card. This is a known upstream data
  limitation, not a bug in this project or in `react-tweet` — see Tutorial
  No. 4.1, Part 21, and `TODOS.md` for the full investigation.
- See `TODOS.md` for the full list of deferred verification and polish items
  (video tweet *export* was fixed and verified in Tutorial No. 4.1; emoji
  rendering and multi-image thread export aren't yet empirically verified,
  though the code paths for them exist).

## Architecture note

- Tweet data is fetched server-side, through `/api/tweet/[id]`, which calls
  `react-tweet`'s syndication-endpoint client — never from the browser
  directly (that endpoint doesn't allow cross-origin browser requests).
- Media images (avatars, photos) are fetched through `/api/image-proxy`
  **only at export time**, not for the live preview — a hostname-allowlisted,
  SSRF-hardened proxy that exists specifically so the browser can safely read
  the image's pixels into the export canvas (cross-origin images can be
  *displayed* freely, but not *read into a canvas* without this).
- No X API key, no paid API, no database. Customization state lives in the
  URL, not a server.

## Reproducing the tutorial artifacts

`TUTORIAL.md`/`.zh.md`, `dist/*.docx`, and `dist/*.pptx` are all built or
checked from source in this repo, not just handed over as finished files —
`_build/` holds the generic content modules and validators, reused verbatim
from gstack Tutorial No. 3's own tooling (see `docs/GSTACK_TUTORIAL_4_OUTLINE.md`
and `docs/TUTORIAL_4_DOCUMENT_MANIFEST.md` for how each maps to its source
material).

```bash
# Rebuild the Word executive memo (needs python-docx)
python _build/build_docx.py

# Rebuild the slide deck (needs python-pptx)
python _build/build_deck.py

# Validate: Markdown EN/ZH parity, docx/pptx structure, and privacy scans
python _build/verify_tutorial_parity.py
python _build/verify_doc_structure.py
python _build/verify_docx.py
python _build/verify_doc_privacy.py
python _build/validate_content.py
python _build/verify_deck.py
```

## What's intentionally not in this repo

This is a sanitized public release, built from an explicit allowlist against
a private development repository — not a full history export. Deliberately
excluded: the raw AI-mentor conversation transcript/PDF this project's early
planning drew from, the unredacted session transcript, and any local
credentials, account identifiers, or machine-specific paths. See
`docs/TUTORIAL_4_PRIVACY_REVIEW.md`, `docs/TUTORIAL_4_DECK_PRIVACY_CHECK.md`,
and `docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md` for exactly what was
reviewed, what was excluded, and why. The redacted, publication-safe session
transcript (`docs/SESSION_TRANSCRIPT_20260917_PUBLIC.md`) is included in its
place.

## License

MIT — see [`LICENSE`](LICENSE).
