# -*- coding: utf-8 -*-
"""Mechanical EN/ZH structural parity check for TUTORIAL.md / TUTORIAL.zh.md.

Counts structural markers by regex, not by eye. This caught two real
staleness bugs in a prior revision of TUTORIAL.md (see commit d215288) --
the discipline is kept here as a real, runnable script rather than a
one-off manual grep.

Exit 0 if every count matches, 1 otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MARKERS = {
    "H1 (#)": re.compile(r"^# ", re.M),
    "H2 (##)": re.compile(r"^## ", re.M),
    "H3 (###)": re.compile(r"^### ", re.M),
    "checkboxes (all)": re.compile(r"- \[[ x]\]", re.M),
    "checkboxes (checked)": re.compile(r"- \[x\]", re.M),
    "code fences (```)": re.compile(r"^```", re.M),
    "tables (header rows, |---|)": re.compile(r"^\|[-: |]+\|$", re.M),
}

failures = []


def count_all(text):
    return {label: len(rx.findall(text)) for label, rx in MARKERS.items()}


def main():
    en_path = ROOT / "TUTORIAL.md"
    zh_path = ROOT / "TUTORIAL.zh.md"
    en = en_path.read_text(encoding="utf-8")
    zh = zh_path.read_text(encoding="utf-8")

    en_counts = count_all(en)
    zh_counts = count_all(zh)

    print(f"{'marker':<28}{'EN':>6}{'ZH':>6}  match")
    for label in MARKERS:
        e, z = en_counts[label], zh_counts[label]
        ok = e == z
        print(f"{label:<28}{e:>6}{z:>6}  {'OK' if ok else 'MISMATCH'}")
        if not ok:
            failures.append(label)

    # Part/appendix titles must appear in the same order in both files
    # (structure, not translated wording -- so match by leading number/tag)
    en_parts = re.findall(r"^## (Part \d+|Troubleshooting|Disciplines worth keeping|Appendix [A-C])", en, re.M)
    zh_parts = re.findall(r"^## (第 \d+ 部分|故障排查|值得保留的纪律|附录 [A-C])", zh, re.M)

    def tag_en(p):
        if p.startswith("Part"):
            return "Part"
        if p == "Troubleshooting":
            return "Troubleshooting"
        if p == "Disciplines worth keeping":
            return "Disciplines"
        return "Appendix"

    def tag_zh(p):
        if p.startswith("第"):
            return "Part"
        if p == "故障排查":
            return "Troubleshooting"
        if p == "值得保留的纪律":
            return "Disciplines"
        return "Appendix"

    en_seq = [tag_en(p) for p in en_parts]
    zh_seq = [tag_zh(p) for p in zh_parts]
    seq_ok = en_seq == zh_seq
    print(f"{'section order sequence':<28}{len(en_seq):>6}{len(zh_seq):>6}  {'OK' if seq_ok else 'MISMATCH'}")
    if not seq_ok:
        failures.append("section order sequence")

    print()
    if failures:
        print(f"FAILED -- {len(failures)} mismatch(es): {', '.join(failures)}")
        sys.exit(1)
    print("PASSED -- EN/ZH tutorial structural parity confirmed mechanically.")
    sys.exit(0)


if __name__ == "__main__":
    main()
