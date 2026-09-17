# Tutorial No. 4 Documentation Phase — Privacy Check

```
Date:            2026-09-17
Scope:           TUTORIAL.md, TUTORIAL.zh.md, docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md,
                 docs/GSTACK_TUTORIAL_4_OUTLINE.md, docs/TUTORIAL_4_DOCUMENT_MANIFEST.md,
                 dist/gstack-tutorial-4_EN.docx, dist/gstack-tutorial-4_ZH.docx
Method:          scan the RENDERED text of the built .docx files (via
                 python-docx, every paragraph and table-cell run), not just
                 the source Markdown/Python content
Verdict:         PASS — zero forbidden identifiers in either built document
```

## Why the rendered file, not just the source

`docs/TUTORIAL_4_PRIVACY_REVIEW.md` already cleared the underlying source
material this documentation phase draws from (`reviews/`,
`docs/external_ai_mentor.md`, the redacted transcript, cleared screenshots).
But a clean source doesn't guarantee a clean built *artifact* — the same
principle this whole tutorial teaches about code (a passing check upstream
is not proof the output downstream is correct). `_build/verify_doc_privacy.py`
therefore opens the actual `.docx` files Word will render and scans every
paragraph and table cell, in both languages, matching the discipline
`_build/verify_deck.py` already established for the slide deck
(`docs/TUTORIAL_4_DECK_PRIVACY_CHECK.md`).

## What was checked

Every identifier the source privacy review flagged as sensitive: the real
Windows username, the real machine hostname, the real Vercel account/team
name, the specific device-authorization code observed in the source PDF,
the device-auth URL pattern itself, and any Windows user-profile path. The
actual literal values are intentionally not reproduced in this public
document — see `_build/verify_doc_privacy.py`'s own `FORBIDDEN` list for
the exact patterns the check runs against.

The same pattern list also doubles as a manual scan target for the two
Markdown tutorials and the three new supporting docs — all five were
authored directly from cleared sources (`reviews/`, `docs/external_ai_mentor.md`,
`PLAN.md`, `README.md`, `TODOS.md`) and contain no such identifiers by
construction; `_build/verify_doc_privacy.py` is the mechanical check on the
one artifact type (built binary `.docx`) that a plain-text source grep
cannot cover.

## Result

```
gstack-tutorial-4_EN.docx -- OK, zero forbidden identifiers (8767 chars scanned)
gstack-tutorial-4_ZH.docx -- OK, zero forbidden identifiers (3941 chars scanned)

PASS -- both documents clean.
```

## Source policy compliance

- `ChatGPT-gstack-20260917.pdf` was never opened, read, or referenced while
  writing `_build/doc_content.py` or either Markdown tutorial — every
  section sources from `reviews/`, `docs/external_ai_mentor.md`, `PLAN.md`,
  `README.md`, or `TODOS.md`.
- No screenshot or raster image is embedded in the Word document — cover
  and section content are text, tables, and code blocks only, so no
  question of which screenshots cleared review applies here.
- Real account/team identifiers, device-authorization codes, and OAuth
  URLs are named as categories of thing that were excluded (Part 14 of
  `TUTORIAL.md`) rather than shown as examples with placeholder values.

## What this does NOT clear

This is a string scan on rendered text, not a design or copy-editing
review. Structural parity (section count, table row/column counts, bullet
counts) is verified separately by `_build/verify_doc_structure.py` before
build, and the mandatory 3-part docx structural check plus CJK font
check (per `MCKINSEY_DOCX_PLAYBOOK.docx` §5-6) is verified by
`_build/verify_docx.py` after build — both passed cleanly for both
languages.

**Automated rendering was blocked; human visual inspection closed the gap.**
Unlike the slide deck (which was rendered to PNG via PowerPoint COM
automation and visually inspected page by page — see
`docs/TUTORIAL_4_DECK_MANIFEST.md`), the two Word documents could not be
rendered to PDF/XPS via Word COM automation in this environment.
`SaveAs2`/`ExportAsFixedFormat` hung indefinitely on every attempt
(multiple parameter variants tried), and the hang reproduced identically
on a minimal one-paragraph control document built with the same
python-docx version — confirming this is an environment-level COM/PDF-filter
issue in this sandbox, not a defect in `_build/build_docx.py`'s output.
This was disclosed rather than worked around silently, and the three
mechanical checks above (ZIP integrity, body structure, no duplicate runs,
eastAsia-on-every-run, EN/ZH structural parity, privacy scan) stood as the
verification evidence at that point.

**Final evidence: human visual inspection, 2026-09-17.** A human opened
both `dist/gstack-tutorial-4_EN.docx` and `dist/gstack-tutorial-4_ZH.docx`
directly in Microsoft Word and confirmed both look correct. Per this
tutorial's own Evidence Ladder (`TUTORIAL.md` Part 11), a human looking at
the actual rendered artifact is stronger evidence than an automated render
would have been — this closes the one item that was open, and no known
gap remains for either document.
