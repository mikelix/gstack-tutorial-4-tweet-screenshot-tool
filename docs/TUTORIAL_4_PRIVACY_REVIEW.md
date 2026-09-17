# Tutorial No. 4 — Privacy / Content Review

```
Date:            2026-09-17
Reviewer role:   Privacy/content gate (per explicit user request, ahead of the deck stage)
Scope reviewed:  ChatGPT-gstack-20260917.pdf, 3 manual-testing screenshots,
                 docs/SESSION_TRANSCRIPT_20260917.md, and every committed
                 .md file's prose for leaked identifiers
Verdict:         CLEARED TO PROCEED, with two required actions taken and
                 one open decision before this repo's first public push
```

This gate exists because `PLAN.md`'s Definition of Done and `reviews/05-ship.md`
both flagged it as pending, and because this project's own central lesson
(the avatar bug — a passing check is not proof of a correct result) applies
here too: "I skimmed it, looks fine" is not a privacy review. What follows
is grounded in an actual full-text extraction and pattern scan of the PDF
(206 pages, via PyMuPDF), a direct read of all three screenshots, and a
`grep` sweep of every committed markdown file — not a sample.

---

## Method

- **PDF:** extracted full text with `docs/extract_pdf_text.py` (PyMuPDF),
  then pattern-scanned for personal identifiers, credentials, local
  infrastructure, and account/team names across all 206 pages. Not a
  page-sample — every page's text was in the scanned corpus.
- **Screenshots:** read directly, full image, by a human-equivalent visual
  pass (this review), checking browser chrome, address bar, visible tabs,
  and account UI for anything beyond the intended tweet content.
- **Markdown files:** `grep`-swept the whole repo for the specific strings
  the PDF scan surfaced (Windows username, machine hostname, Vercel
  account/team name), not just the files this review expected to check.
  This is how the leak in `reviews/05-ship.md` and the retrospective —
  neither obviously "evidence," both prose I authored — was actually
  found, not assumed absent.

---

## Findings by asset

### 1. `ChatGPT-gstack-20260917.pdf`

**Classification: DO_NOT_PUBLISH (as-is).**

| Category | Found | Detail |
|---|---|---|
| Personal identifiers | Yes — pervasive | The real Windows username, embedded in Windows user-profile paths, dozens of times across the document (shell prompts, tool output, file paths pasted into the chat). The real machine hostname (from a Git Bash prompt). |
| Credentials / security-sensitive | Yes — one item | A live Vercel OAuth device-authorization URL with a real `user_code`, pasted into the chat as part of the real `npx vercel login` flow. The code itself is almost certainly expired by now (device codes are short-lived), but publishing it is the wrong default — device-auth URLs are exactly what the user's own request asked to check for. |
| Private/local infrastructure | Minor | A local dev-server startup log shows a benchmarking-range network address (not a home/office IP) and a local process ID. Low sensitivity, no tutorial value either way. |
| Third-party/account content | Yes — out of scope for this tutorial | The PDF is one continuous ChatGPT conversation covering the **entire day**, not just this project. It also contains an earlier browser-automation task against an unrelated third-party site from this same session — a different site's login/upload workflow that has nothing to do with Tutorial #4's subject, plus a local path to an unrelated video file. |
| Vercel account/team name | Yes | The real Vercel account name and real team name, shown verbatim as real CLI output pasted into the chat. |
| Tutorial relevance | The *lessons* are high-value (the html2canvas correction, the "no secrets" contradiction, the debugging-thrash intervention, the Ship Mode prompt) — all already fully and safely captured in `docs/external_ai_mentor.md` with zero identifiers. The *raw document* itself adds no additional teaching value beyond what's already extracted. |

**Why DO_NOT_PUBLISH rather than SAFE_AFTER_REDACTION:** the username alone
appears so many times, interleaved with real conversational text (not a
clean, mechanically-redactable header/footer), that a manual or regex
redaction pass over 206 pages of organic dialogue is both disproportionate
effort and genuinely error-prone — missing even one instance defeats the
purpose, and this review cannot be confident of catching all of them by
hand at this volume. Combined with the out-of-scope Canvofire content
(which isn't even about this tutorial), the PDF as a whole is the wrong
artifact to publish regardless of redaction effort.

**Recommended disposition:** keep the PDF as a **private source-of-truth
only** — present in this local repo for the author's own reference, never
pushed to a public remote. `docs/external_ai_mentor.md` remains the public
distillation and needs no changes; it already contains everything the PDF
is cited for, with none of the identifiers. If a publishable excerpt is
ever wanted, treat it as RECREATE_WITH_SAFE_DATA: run a fresh, short,
purpose-built mentor conversation specifically for public sharing, rather
than attempting to extract a clean slice of this one.

**Action taken:** none to the file itself (not modified, not moved — still
present locally). Its exclusion from any public push is a decision to make
explicitly at ship time (see "Open decision" below), the same way
gstack-tutorial-3 excluded pilot video clips via `.gitignore` rather than
committing and hoping nobody looks.

---

### 2-4. Manual-testing screenshots

| File | Classification | Notes |
|---|---|---|
| `human_in_the_loop_manual_testing_resutl_Sep2026.png` | **SAFE_AS_IS** | Aside browser window, `localhost:3000` in the address bar, the app's own export-controls UI, one real public tweet rendered (`@RohOnChain`). No other tabs, no account UI, no file paths, no credentials visible. |
| `tweet_screenshot_human_test_download_tweet_sep2026.png` | **SAFE_AS_IS** | The downloaded PNG export itself — no browser chrome at all, just the product's own output. |
| `tweet_screenshot_human_test_download_tweet_Vercel1_sep2026.png` | **SAFE_AS_IS** | Same export, from the production/Vercel build — confirms parity between local and deployed output. No URL bar, no account info. |

**On the tweet content itself:** all three show the same real, public tweet
(`@RohOnChain`, posted publicly on X). This is not private content — it's
the product's own core function being demonstrated, the same way any tech
article embeds a public tweet as a worked example. No redaction needed;
this is the intended teaching content, not incidental exposure.

**Action taken:** none — verified safe, no changes.

---

### 5. `docs/SESSION_TRANSCRIPT_20260917.md` (already committed)

**Classification: SAFE_AFTER_REDACTION.**

The extracted Claude Code session transcript (generated by
`docs/extract_transcript.py`, committed in `9a2f140`) contains the real
Windows username 40 times (mostly tool-call breadcrumbs referencing local
paths), plus the real Vercel account name (1 occurrence) and real team name
(3 occurrences — two of them embedded directly in real deployment/inspector
URLs).

**Action taken:** created `docs/SESSION_TRANSCRIPT_20260917_PUBLIC.md`, a
redacted copy, via `docs/redact_transcript.py` (a small, purpose-built
script — not a general tool, its pattern list is specific to what this
file actually leaked). **The original file was not modified.** Verified the
redacted copy is clean: zero remaining matches for the username, hostname,
Vercel account, or team name, plus a broader sweep for emails/tokens/other
account patterns (6 incidental matches, all confirmed false positives —
internal Claude Code subagent task IDs, not credentials).

**Which copy to reference publicly:** `SESSION_TRANSCRIPT_20260917_PUBLIC.md`
only. The original stays in the repo as the internal, complete record.

---

### 6-7. `reviews/05-ship.md` and `docs/GSTACK_TUTORIAL_4_PROJECT_RETROSPECTIVE.md` (already committed)

**Classification: SAFE_AFTER_REDACTION — fixed directly, not via a copy.**

Both are prose I authored (not raw captured evidence — the retrospective is
a reconstructed project record, `05-ship.md` is a review document I wrote),
so unlike the PDF/screenshots/transcript, editing them in place is the
correct fix rather than producing a parallel sanitized copy. Both
originally named the real Vercel team name verbatim when describing the
deployment step.

**Action taken:** both edited directly. The team name is now replaced with
"the project owner's personal Vercel account/team," with a note pointing to
this review document. The teaching content (Vercel's first-deploy-becomes-
production behavior, the deployment sequence) is fully preserved — only the
account identifier was removed.

**Gap found and fixed during the release-phase re-scan (2026-09-17):** this
earlier pass caught the team name in the retrospective's deployment-step
prose, but missed a second, separate occurrence of the real Vercel
*account* name in the retrospective's Part-comparison table (row 12, "AI
Ship / Deployment"). Fixed in the same way — the account identifier
replaced with a generic description, teaching content preserved. This is
recorded here as a genuine finding, not swept past: the original privacy
pass was not exhaustive on its first attempt, and this release-gate
re-scan is what caught the remainder.

---

### 8. Local-only files (gitignored, never tracked — checked for completeness)

`dev-stdout.log`, `dev-stderr.log`, `dev-pid.txt`, `.next/dev/logs/next-development.log`,
`.vercel/` — all already excluded by `.gitignore` (confirmed: none appear in
`git status` or any commit). **No action needed**; listed here only so this
review can say it checked, not assumed.

---

## Classification summary

| Asset | Classification |
|---|---|
| `ChatGPT-gstack-20260917.pdf` | **DO_NOT_PUBLISH** (as-is) — keep private, `docs/external_ai_mentor.md` is the public substitute |
| `human_in_the_loop_manual_testing_resutl_Sep2026.png` | SAFE_AS_IS |
| `tweet_screenshot_human_test_download_tweet_sep2026.png` | SAFE_AS_IS |
| `tweet_screenshot_human_test_download_tweet_Vercel1_sep2026.png` | SAFE_AS_IS |
| `docs/SESSION_TRANSCRIPT_20260917.md` (original) | Keep private/internal; publish `docs/SESSION_TRANSCRIPT_20260917_PUBLIC.md` instead |
| `docs/SESSION_TRANSCRIPT_20260917_PUBLIC.md` (new, redacted) | SAFE_AS_IS — this is the one to reference publicly |
| `reviews/05-ship.md` | SAFE_AS_IS (fixed in place) |
| `docs/GSTACK_TUTORIAL_4_PROJECT_RETROSPECTIVE.md` | SAFE_AS_IS (fixed in place) |
| `dev-*.log`, `.next/`, `.vercel/` | SAFE_AS_IS (already gitignored) |

---

## Open decision — required before this repo's first public push

**The original, unredacted `docs/SESSION_TRANSCRIPT_20260917.md` is already
in local git history** (commit `9a2f140`), with the username baked into 40
places. Nothing has been pushed to any remote yet for this project — no
`gh repo create`, no `git push` has run — so this is genuinely a
**before-first-push decision, not an already-leaked one.** Two honest
options, not resolved by this review because they're a judgment call, not
a mechanical one:

1. **Accept it as low-severity and push as-is.** It's a Windows username,
   not a credential — low real-world sensitivity. Simpler; matches this
   project's own "don't rewrite history, the audit trail is the product"
   principle from `PLAYBOOK.md`-style discipline elsewhere in this series.
2. **Rewrite local history before the first push** (e.g. `git filter-repo`)
   to scrub the original transcript's committed content, keeping only the
   redacted version in history. Cleaner, but it's exactly the kind of
   one-way, history-altering operation this project's own tooling (Claude
   Code, in this session) should not perform without explicit, deliberate
   authorization from the repo owner — not something to default into
   quietly during a privacy pass.

This review's recommendation: **option 1**, on the grounds that a Windows
username is meaningfully lower-severity than the Vercel account name or the
device-auth code (both already handled by keeping the PDF private and
publishing only the redacted transcript copy), and rewriting history for a
low-severity item sets a precedent this series has otherwise avoided. Stated
as a recommendation, not a decision made on the repo owner's behalf —
confirm before the actual ship/publish step in a future `reviews/`-style
gate, the same way gstack-tutorial-3's own publish step was a separate,
explicit go-ahead.

---

## `TUTORIAL.md` / `TUTORIAL.zh.md` — updated?

**Yes, both, one line each** (see commit) — the Definition of Done's
`ChatGPT-gstack-20260917.pdf` / privacy-review line updated from "still
pending" to reflect this review's actual outcome and point at this
document. No other lines in either tutorial referenced a specific asset
closely enough to need further clarification — neither file embeds images
or quotes the PDF/transcript directly.
