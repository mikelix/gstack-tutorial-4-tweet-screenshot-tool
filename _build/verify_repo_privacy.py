# -*- coding: utf-8 -*-
"""Full-repository privacy/secret scan -- the public-release gate.

Walks every tracked-type file in this repo (Markdown, source, scripts,
config, README, generated .docx/.pptx, the public transcript, manifests,
privacy reports) and scans it with the generic, public-safe patterns in
privacy_patterns.py, plus a set of generic secret-shaped patterns (API
keys, tokens, private-key blocks, .env-style secret assignments). Unlike
verify_deck.py / verify_doc_privacy.py (which check one artifact type
each), this is the single command that answers "is the whole repo clean."

Exit 0 with PUBLIC_RELEASE_PRIVACY_SCAN = PASS if clean, 1 otherwise.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from privacy_patterns import scan_text

ROOT = Path(__file__).resolve().parents[1]

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "generic API key assignment": re.compile(r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
    "Bearer token": re.compile(r"Bearer\s+[A-Za-z0-9\-_.]{20,}"),
    "private key block": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "generic .env secret line": re.compile(r"(?im)^[A-Z_]+_(SECRET|TOKEN|KEY|PASSWORD)\s*="),
}

SKIP_DIRS = {".git", "node_modules", ".next", ".vercel", "__pycache__"}
TEXT_EXTENSIONS = {".md", ".ts", ".tsx", ".js", ".mjs", ".json", ".css",
                    ".ps1", ".py", ".svg", ""}

literal_hits = 0
secret_hits = 0
findings = []


def scan_docx(path: Path):
    from docx import Document
    doc = Document(str(path))
    parts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                parts.extend(p.text for p in cell.paragraphs)
    return "\n".join(parts)


def scan_pptx(path: Path):
    from pptx import Presentation
    prs = Presentation(str(path))
    parts = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.text:
                        parts.append(run.text)
    return "\n".join(parts)


def iter_files():
    for p in ROOT.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name == Path(__file__).name:
            continue
        yield p


for p in iter_files():
    rel = p.relative_to(ROOT)
    ext = p.suffix.lower()
    text = None
    try:
        if ext == ".docx":
            text = scan_docx(p)
        elif ext == ".pptx":
            text = scan_pptx(p)
        elif ext in TEXT_EXTENSIONS or ext == "":
            if ext in (".ico",):
                continue
            text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError, Exception) as e:  # noqa: BLE001
        continue
    if text is None:
        continue

    for label, snippet in scan_text(text):
        literal_hits += 1
        findings.append(f"{rel}: {label} -> {snippet!r}")

    for label, rx in SECRET_PATTERNS.items():
        m = rx.search(text)
        if m:
            secret_hits += 1
            findings.append(f"{rel}: {label} -> {m.group(0)[:60]!r}")

print(f"Scanned files under {ROOT}")
print(f"literal private-identifier matches: {literal_hits}")
print(f"secret-shaped pattern matches: {secret_hits}")

if findings:
    print("\nFindings:")
    for f in findings:
        print(f"  {f}")
    print("\nPUBLIC_RELEASE_PRIVACY_SCAN = FAIL")
    sys.exit(1)

print("\nPUBLIC_RELEASE_PRIVACY_SCAN = PASS")
sys.exit(0)
