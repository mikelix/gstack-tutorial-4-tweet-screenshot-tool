# Tutorial No. 4 Deck — Privacy Check

```
Date:            2026-09-17
Scope:           dist/gstack-tutorial-4_EN.pptx, dist/gstack-tutorial-4_ZH.pptx
Method:          scan the RENDERED text (via python-pptx, every run in
                 every shape in every slide), not the source content file
Verdict:         PASS — zero forbidden identifiers in either deck
```

## Why the rendered file, not the source

`docs/TUTORIAL_4_PRIVACY_REVIEW.md` already cleared every source document
this deck draws from (`reviews/`, `docs/external_ai_mentor.md`, `TUTORIAL.md`,
`README.md`, `TODOS.md`, `PLAN.md`). But a clean source doesn't guarantee a
clean *artifact* — the same lesson this project's own central bug teaches
(a passing check upstream is not proof the output downstream is correct).
So `_build/verify_deck.py` opens the actual built `.pptx` files and scans
every text run PowerPoint will actually display, in both languages.

## What was checked

`_build/verify_deck.py` scans for every identifier the source privacy
review flagged as sensitive: the real Windows username, the real machine
hostname, the real Vercel account/team name, the specific device-authorization
code observed in the source PDF, the device-auth URL pattern itself (in case
a different code ever appeared), and any Windows user-profile path. The
actual literal values are intentionally not reproduced in this public
document — see `_build/verify_deck.py`'s own `FORBIDDEN` list for the exact
patterns the check runs against.

## Result

```
EN: gstack-tutorial-4_EN.pptx -- 20 slides
ZH: gstack-tutorial-4_ZH.pptx -- 20 slides

PASS -- both decks 20/20 slides, zero forbidden identifiers in rendered text.
```

## Source policy compliance

- `ChatGPT-gstack-20260917.pdf` was never opened, read, or referenced while
  writing `_build/deck_content.py` — every slide sources from
  `docs/external_ai_mentor.md` (the already-cleared distillation) or from
  `reviews/`, `PLAN.md`, `README.md`, `TODOS.md`.
- No screenshot is embedded in the deck — all 20 slides use
  `mck.py`-generated vector/text layouts, not raster images, so the
  question of which PNGs passed the source privacy review doesn't apply to
  this deck's content (it would apply if a future revision embeds one of
  the three cleared screenshots).
- The redacted transcript (`docs/SESSION_TRANSCRIPT_20260917_PUBLIC.md`)
  was not used as deck source material either — the deck sources from the
  structured `reviews/`/`docs/` files, not the raw dialogue transcript.

## What this does NOT clear

This check is a string scan, not a design review — it confirms no
forbidden identifier is *present*, not that every claim is perfectly
phrased or that the deck is otherwise ready to publish. Bilingual
structural parity (slide count, table/bullet row counts) is verified
separately by `_build/validate_content.py`, and layout correctness
(no visual overflow) was verified by rendering every slide to PNG and
reading it directly — see `docs/TUTORIAL_4_DECK_MANIFEST.md`'s "Build
notes" section for what that process actually caught.
