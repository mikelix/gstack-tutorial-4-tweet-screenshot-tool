# -*- coding: utf-8 -*-
"""Verify the built decks: slide count, EN/ZH parity, and a privacy scan of
the ACTUAL RENDERED TEXT (not the source content file) -- checking the
generator's output, not just trusting deck_content.py was clean, is the
same discipline this whole project's own history argues for (a passing
check on the source is not proof the rendered artifact is correct).

Privacy patterns are generic and public-safe (see privacy_patterns.py) --
this scanner never hardcodes a real identifier, so it's safe to publish and
still catches the *shape* of a leak (a Windows path, a Vercel CLI login
line, a device-auth URL) rather than one specific known value.
"""
import sys
from pathlib import Path

from pptx import Presentation

sys.path.insert(0, str(Path(__file__).parent))
from privacy_patterns import scan_text

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

errors = []

for lang in ("EN", "ZH"):
    path = DIST / f"gstack-tutorial-4_{lang}.pptx"
    prs = Presentation(str(path))
    print(f"{lang}: {path.name} -- {len(prs.slides)} slides")

    all_text = []
    for si, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.text:
                        all_text.append(run.text)
    joined = "\n".join(all_text)

    for label, snippet in scan_text(joined):
        errors.append(f"{lang}: {label} matched: ...{snippet}...")

    if len(prs.slides) != 20:
        errors.append(f"{lang}: expected 20 slides, got {len(prs.slides)}")

print()
if errors:
    print(f"FAIL -- {len(errors)} issue(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("PASS -- both decks 20/20 slides, zero forbidden identifiers in rendered text.")
