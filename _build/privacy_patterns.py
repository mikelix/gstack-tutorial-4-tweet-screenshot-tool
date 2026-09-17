# -*- coding: utf-8 -*-
"""Shared, public-safe privacy scan patterns for this repo's validators.

Public-release rule: this repo must contain zero literal private
identifiers anywhere, including in its own privacy-check tooling. Earlier
revisions of the deck/doc privacy scanners hardcoded the real Windows
username, hostname, and Vercel account/team name as literal strings --
functional, but itself a form of publishing the thing the scan exists to
catch. This module replaces those literals with two things instead:

1. GENERIC PATTERNS -- structural regexes that catch the *shape* of a leak
   (a Windows user-profile path, a Vercel CLI login/team-output line, a
   Git Bash hostname prompt, an OAuth device-authorization URL) without
   encoding any specific real value. These are what every validator in
   this repo runs by default, and they are safe to publish: matching
   "C:\\Users\\<anything>" tells a reader nothing about which username was
   ever real.

2. AN OPTIONAL LOCAL DENYLIST (`.privacy-denylist.local`, repo root) -- for
   a contributor who wants to additionally check for specific values they
   know are sensitive (this machine's real username, a specific account
   name, anything project-specific). Gitignored, never committed, never
   required: the generic patterns above run with or without it, so public
   CI and a fresh clone both work with zero configuration.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_DENYLIST_FILE = ROOT / ".privacy-denylist.local"

GENERIC_PATTERNS = {
    "Windows user-profile path": re.compile(r"C:\\Users\\[^\\\"'<>\s]+"),
    "OAuth device-authorization URL": re.compile(r"oauth/device\?user_code=[A-Za-z0-9-]+"),
    "Vercel CLI 'Logged in as' output": re.compile(r"(?i)logged in as [a-z0-9][a-z0-9_-]*"),
    "Vercel CLI 'Active team' output": re.compile(r"(?i)active team:\s*[a-z0-9][a-z0-9_-]*"),
    "Git Bash hostname prompt": re.compile(r"[a-zA-Z0-9_.-]+@[A-Za-z0-9][A-Za-z0-9_-]{3,}\s+MINGW64"),
    "generic OAuth/device user_code param": re.compile(r"(?i)user_code=[A-Za-z0-9-]{4,}"),
}


def load_local_denylist():
    """Optional, gitignored, absent by default. Returns a list of raw
    strings to additionally scan for (case-insensitive substring match),
    one per non-comment, non-blank line."""
    if not LOCAL_DENYLIST_FILE.exists():
        return []
    lines = LOCAL_DENYLIST_FILE.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def scan_text(text):
    """Returns a list of (label, matched_snippet) for every hit -- generic
    patterns always, plus the optional local denylist if present."""
    hits = []
    for label, rx in GENERIC_PATTERNS.items():
        m = rx.search(text)
        if m:
            hits.append((label, m.group(0)))
    for literal in load_local_denylist():
        idx = text.lower().find(literal.lower())
        if idx != -1:
            hits.append((f"local denylist entry", text[max(0, idx - 20):idx + len(literal) + 20]))
    return hits
