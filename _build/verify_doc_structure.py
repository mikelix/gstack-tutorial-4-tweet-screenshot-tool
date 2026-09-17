# -*- coding: utf-8 -*-
"""Structural EN/ZH parity check on doc_content.py's DOC dict, before build.

Mirrors validate_content.py's discipline for deck_content.py: assert
structural counts (section count, block count per section, table row/col
counts, bullet counts) directly on the source content, rather than trusting
a clean docx build. A clean build is level 3 on the Evidence Ladder, not
proof the two languages actually match structurally.

Exit 0 if every count matches, 1 otherwise.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from doc_content import DOC, pick, L

failures = []


def check(label, ok, detail=""):
    print(f"  {'OK  ' if ok else 'FAIL'} {label}" + (f" — {detail}" if not ok and detail else ""))
    if not ok:
        failures.append(label)


def main():
    en = pick(DOC, "en")
    zh = pick(DOC, "zh")

    check("meta line count", len(en["meta"]) == len(zh["meta"]),
          f"{len(en['meta'])} vs {len(zh['meta'])}")
    check("exec_paras count", len(en["exec_paras"]) == len(zh["exec_paras"]),
          f"{len(en['exec_paras'])} vs {len(zh['exec_paras'])}")
    check("metrics_headers count",
          len(en["metrics_headers"]) == len(zh["metrics_headers"]))
    check("metrics_rows count", len(en["metrics_rows"]) == len(zh["metrics_rows"]),
          f"{len(en['metrics_rows'])} vs {len(zh['metrics_rows'])}")
    check("toc entry count", len(en["toc"]) == len(zh["toc"]),
          f"{len(en['toc'])} vs {len(zh['toc'])}")
    check("toc count matches section count",
          len(en["toc"]) == len(en["sections"]),
          f"toc={len(en['toc'])} sections={len(en['sections'])}")
    check("section count", len(en["sections"]) == len(zh["sections"]),
          f"{len(en['sections'])} vs {len(zh['sections'])}")

    for i, (se, sz) in enumerate(zip(en["sections"], zh["sections"]), 1):
        label = f"section {i} ({se['title'][:30]!r})"
        check(f"{label}: block count",
              len(se["blocks"]) == len(sz["blocks"]),
              f"{len(se['blocks'])} vs {len(sz['blocks'])}")
        for j, (be, bz) in enumerate(zip(se["blocks"], sz["blocks"]), 1):
            check(f"{label} block {j}: kind matches", be[0] == bz[0],
                  f"{be[0]} vs {bz[0]}")
            if be[0] == "table" and bz[0] == "table":
                _, he, re_, we = be
                _, hz, rz, wz = bz
                check(f"{label} block {j}: table header cols", len(he) == len(hz))
                check(f"{label} block {j}: table row count", len(re_) == len(rz),
                      f"{len(re_)} vs {len(rz)}")
                for k, (rowe, rowz) in enumerate(zip(re_, rz)):
                    check(f"{label} block {j} row {k}: col count",
                          len(rowe) == len(rowz))
            if be[0] == "bullets" and bz[0] == "bullets":
                check(f"{label} block {j}: bullet count", len(be[1]) == len(bz[1]),
                      f"{len(be[1])} vs {len(bz[1])}")
            if be[0] == "code" and bz[0] == "code":
                check(f"{label} block {j}: code line count", len(be[1]) == len(bz[1]),
                      f"{len(be[1])} vs {len(bz[1])}")

    print()
    if failures:
        print(f"FAILED — {len(failures)} mismatch(es).")
        sys.exit(1)
    print(f"PASSED — {len(en['sections'])} sections, structural parity confirmed "
          f"before build.")
    sys.exit(0)


if __name__ == "__main__":
    main()
