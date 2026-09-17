# -*- coding: utf-8 -*-
"""Structural validation for deck_content.py, run before every build.

Checks things a build failure or a visual inspection might not catch
cleanly: table row/header column-count mismatches (a row with fewer
columns than its header silently drops content or shifts columns), and
EN/ZH list-length mismatches within any L() pair (bullets, table rows,
flow steps).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deck_content import SLIDES, L

errors = []


def check_len_parity(path, en_list, zh_list):
    if len(en_list) != len(zh_list):
        errors.append(f"{path}: EN has {len(en_list)} items, ZH has {len(zh_list)}")


for i, (kind, raw) in enumerate(SLIDES):
    tag = f"slide {i+1} ({kind})"
    if kind == "table":
        headers = raw["headers"]
        n_cols = len(headers[0])
        assert len(headers[1]) == n_cols, f"{tag}: header EN/ZH column count mismatch"
        rows_en, rows_zh = raw["rows"]
        check_len_parity(f"{tag} rows", rows_en, rows_zh)
        for ri, row in enumerate(rows_en):
            if len(row) != n_cols:
                errors.append(f"{tag}: EN row {ri} has {len(row)} cols, header has {n_cols} -- {row}")
        for ri, row in enumerate(rows_zh):
            if len(row) != n_cols:
                errors.append(f"{tag}: ZH row {ri} has {len(row)} cols, header has {n_cols} -- {row}")
    elif kind == "bullets":
        b_en, b_zh = raw["bullets"]
        check_len_parity(f"{tag} bullets", b_en, b_zh)
    elif kind == "flow":
        s_en, s_zh = raw["steps"]
        check_len_parity(f"{tag} steps", s_en, s_zh)
    elif kind == "two_col":
        l_en, l_zh = raw["left"]
        r_en, r_zh = raw["right"]
        check_len_parity(f"{tag} left lines", l_en[1], l_zh[1])
        check_len_parity(f"{tag} right lines", r_en[1], r_zh[1])

print(f"Checked {len(SLIDES)} slides.")
if errors:
    print(f"FAIL -- {len(errors)} structural mismatch(es):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("PASS -- no structural mismatches.")
