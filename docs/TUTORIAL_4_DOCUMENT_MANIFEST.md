# Tutorial No. 4 — Document Manifest

Provenance table: every major claim in `TUTORIAL.md`/`TUTORIAL.zh.md` and
the Word executive memo, traced to the source file(s) it's grounded in and
the evidence asset (if any) that backs it. Built so a skeptical reader — or
a future editor — can check any claim against its source in one lookup,
matching the discipline `docs/TUTORIAL_4_DECK_MANIFEST.md` already
established for the slide deck.

| Section | Main claims | Source files | Evidence assets |
|---|---|---|---|
| Part 0 — Mental model | Two-AI operating loop; 16-stage sequence | `docs/external_ai_mentor.md`, `PLAN.md` §1-2 | — |
| Part 1 — AI CEO | No free X-API alternative (verified live); thread mode redefined mid-review; SSRF hole closed pre-code; 6/8 scope expansions accepted | `reviews/01-ceo-review.md` | — |
| Part 2 — AI Project Manager | PM role not run separately; stated gap, not hidden | `reviews/02-spec.md`, `PLAN.md` §2, `TODOS.md` | — |
| Part 3 — Architecture | Tweet-data and export data paths; CORS-driven server hop; no-DB V1 scope | `README.md` ("Architecture note"), `reviews/01`, `04` | `src/lib/media-hosts.ts`, `src/app/api/image-proxy/route.ts` (read directly) |
| Part 4 — Security + UX | Exact-hostname allowlist; HTTPS-only; redirect revalidation; size cap; MIME check; thread partial-failure UX | CEO review §3, §11 | `src/lib/media-hosts.ts` |
| Part 5 — Independent second opinion | OV-1 through OV-8 tensions; same-model fallback stated as a limitation | `reviews/03-eng-review.md` | — |
| Part 6 — Engineering review | B1-B5 findings; B1 classified BLOCKER; verdict PROCEED WITH FIXES | `reviews/03-eng-review.md` | — |
| Part 7 — High-risk spike | react-tweet/modern-screenshot source reading; avatar bug; blob: vs data: URL root cause; visual proof; capture-time improvement | `reviews/04-qa-report.md` | Corrected export PNG (read directly during the spike) |
| Part 8 — AI Engineer implementation | Component list; component boundaries; stale-response protection; DRY-as-hypothesis (OV-7) | `reviews/04-qa-report.md`, source tree | — |
| Part 9 — Aside browser QA | Aside-first rule; three evidence layers; Aside tooling quirk vs. app bug | `reviews/04-qa-report.md`, `docs/external_ai_mentor.md` | — |
| Part 10 — Human-in-the-loop testing | Local + production manual test; two human-only gates | `reviews/05-ship.md` | User-reported testing (not independently AI-verifiable, by design) |
| Part 11 — Evidence Ladder | 10-level framework; level 5 as the trap; level 7 as what caught the avatar bug | `reviews/04-qa-report.md` | — |
| Part 12 — Debugging waste | Thread share-link style bug episode; timebox principle | `reviews/05-ship.md` ("Where time was spent") | — |
| Part 13 — Rapid finalization | Fix-list vs. defer-list; two mentor interventions; the actual pivot away from the suggested protocol | `TODOS.md`, `reviews/05-ship.md`, `docs/external_ai_mentor.md` | — |
| Part 14 — Deployment | `npx vercel` (no global install); human-run login/authorization; AI-completed deploy sequence | `reviews/05-ship.md` | — (privacy-cleared: no real account/team identifiers) |
| Part 15 — Production result | Both core flows verified in production; no fatal console errors in tested flows | `reviews/05-ship.md`, `README.md` | — |
| Part 16 — Known limitations | Rate limiting never built; thread style bug; unverified media scenarios; unverified Safari clipboard | `TODOS.md`, `reviews/05-ship.md` | — |
| Part 17 — Reusable workflow | 16-stage table with purpose/output/exit criterion/human gate | `docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md` (derived from `PLAN.md`, all `reviews/`) | — |
| Part 18 — Final lessons | Ten lessons synthesized from Parts 1-17 | Synthesis of all `reviews/` | — |
| Deck (companion artifact) | 20-slide bilingual version of the same narrative | `_build/deck_content.py` | `dist/gstack-tutorial-4_{EN,ZH}.pptx`, `docs/TUTORIAL_4_DECK_MANIFEST.md` |
| Word memo (companion artifact) | Shorter executive-memo version, same source facts | `_build/doc_content.py` | `dist/gstack-tutorial-4_{EN,ZH}.docx` |

## What is explicitly NOT a source for any of the above

Per `docs/TUTORIAL_4_PRIVACY_REVIEW.md` and the fixed source policy for this
documentation phase:

- `ChatGPT-gstack-20260917.pdf` — private source only, never quoted, embedded, or
  directly reused in any published material
- The original unredacted transcript (`docs/SESSION_TRANSCRIPT_20260917.md`)
  — internal-only; `docs/SESSION_TRANSCRIPT_20260917_PUBLIC.md` is the
  redacted copy safe to reference
- Any real Windows username, machine hostname, Vercel account/team name,
  OAuth device-authorization code, or device-auth URL

## Cross-check discipline

Every row above should resolve to a real file in this repository. If a
future edit to `TUTORIAL.md` adds a claim not traceable to a row here, add
the row before publishing — this manifest exists specifically so "where did
that number/claim come from" always has a one-hop answer.
