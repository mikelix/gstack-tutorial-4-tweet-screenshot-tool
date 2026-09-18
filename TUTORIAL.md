# gstack Tutorial #4 — From AI Planning to Working Production Software

**What you will be able to do afterwards:** run gstack the way tutorials
#1-#3 taught, plus one new capability — a second, independent AI in its own
session whose only job is translating gstack's raw output into your next
precision prompt — and know, from a real worked example, what a full
19-stage AI-native development system actually looks like end to end: from
premise challenge through production deployment, with a human gate at every
consequential step.

**Time:** 3-5 hours to read this tutorial closely; the project behind it
(a full app, five review passes, and a production deploy) took one long
session. Scaling is in wall-clock per stage, not in new steps. Parts 0-18
are that original session. Parts 20-23 — **Tutorial No. 4.1** — are a
second, later session on the same codebase, covering a product design
revision and a real production bug found and fixed after the Part 15
deploy; add roughly 1-1.5 hours to read that extension closely.

**Prerequisites:** gstack already working (tutorials #1-#3 cover this); a
second AI chat you can open in a separate window — any provider; Node.js
and npm for the demo app itself.

中文版：[`TUTORIAL.zh.md`](TUTORIAL.zh.md)

> **Educational use notice.** This tutorial, and the demo application it
> documents (the Tweet Screenshot Tool), are provided for educational
> purposes only — to teach a verifiable, AI-native development workflow.
> It does not grant rights to any third-party content displayed by the
> demo application (tweets remain their authors' content, shown only as
> public embeds the way any browser or news article would). Nothing here
> is legal advice.

---

## Part 0 — The mental model

### 0.1 What we are building

The Tweet Screenshot Tool: paste a tweet URL, the app fetches it
server-side, renders a pixel-perfect live preview, you customize it
(background, padding, export scale, light/dark theme), and export it as a
PNG, a clipboard image, or a shareable link that restores the same tweet
and styling for someone else. A second mode (`/thread`) does the same for
a manually-assembled list of tweets, exported as one combined image.

V1 shipped both modes in production. Deliberately excluded: automatic
thread discovery (no free data source supports it), a browser extension,
and a public headless generation API — stated exclusions, not silent gaps
(`reviews/01-ceo-review.md`, `TODOS.md`).

### 0.2 Why "AI writes code" is the wrong model

That phrase describes roughly one stage out of nineteen this project
actually ran. What happened instead:

```
Human founder / learner
        |
External AI Mentor / Meta-Agent   <- a SEPARATE AI, own session
        |
Optimized prompt
        |
gstack specialist role             <- CEO, PM, Architect, Reviewer, Engineer...
        |
Evidence / artifact
        |
Human gate
        |
Next specialized role
```

Planning, challenging, implementing, testing, and human verification are
different jobs, done by different roles, each producing evidence the next
role or the human can actually check. Tutorials #1-#3 already taught the
gstack half of this (CEO/PM/Architect/QA/DevOps plus a mechanical gate
chain). What's new here is the layer above it: a second, independent AI
whose entire job is translating gstack's raw output into the next precise
instruction — see `docs/external_ai_mentor.md` for the full pattern and
four sourced examples of it catching something gstack's own framing got
wrong.

The full sequence this tutorial walks through:

```
0. Problem framing         6. Engineering review     12. Minimal QC
1. AI CEO                  7. High-risk spike         13. Deploy
2. AI PM                   8. AI Engineer             14. Production smoke test
3. Architecture            9. Evidence checkpoint      15. Freeze + retrospective
4. Security + UX          10. Browser QA
5. Independent 2nd opinion 11. Human-in-the-loop test
```

This exact sequence, generalized for reuse, is written out in full in
[`docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md`](docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md).

**Checkpoint 0**
- [ ] You can name the two AI systems involved in this project and what
      each one's job was
- [ ] You understand that "AI writes code" is stage 8 of 19, not the whole
      workflow

---

## Part 1 — AI CEO

**Governing lesson:** *architecture and scope decisions made before code
exists are cheap to change; the ones made after are not.*

`/plan-ceo-review` opened with a premise challenge, not a feature list: is
there already a working free alternative? **Verified live, not assumed** —
the two closest open-source candidates are both built on the official X
API, which has had no free tier since 2026. That single, checked fact
eliminated every existing competitor and set the whole architecture: no
paid API, which rules out both "fork a dead-API app" and "server-side
headless-browser screenshot" as alternatives.

**Decisions locked at this stage:**

| Decision | Reasoning |
|---|---|
| `react-tweet` + `modern-screenshot`, Next.js on Vercel | Renders via X's free public syndication endpoint; no paid API, no scraping |
| Thread mode redefined mid-review: manual, not auto-discovery | No free data source can discover a thread's next tweet without a paid API or scraping — caught during the review itself, not after building the wrong thing |
| SSRF hole closed before any code existed | Host-substring matching would have let `evil-twimg.com.attacker.net` through; fixed to exact-hostname matching in the plan, before implementation |
| 6 of 8 proposed scope expansions accepted | Export polish, clipboard copy, shareable links, thread mode; two declined |

**Evidence produced at this stage:** `reviews/01-ceo-review.md` — an
11-section review with 25 findings, each resolved through an individual
decision, not a batch approval.

**Checkpoint 1**
- [ ] You can state the one live-verified fact that shaped this entire
      architecture
- [ ] You can name one scope decision that changed mid-review, and why

---

## Part 2 — AI Project Manager

**Governing lesson:** *a task breakdown is only as trustworthy as the plan
it came from — and skipping this role is a real, checkable gap, not a
free pass.*

**Stated gap, not hidden:** no dedicated PM role ran separately in this
project. The CEO review's own output covered the function instead — an
Implementation Tasks list (T1-T14, prioritized P1/P2/P3) and `TODOS.md`
entries for explicitly out-of-scope items. This worked here because the
CEO review was thorough enough to double as a task breakdown. It is not a
pattern to copy uncritically on a larger project — a bigger codebase could
hit real sequencing mistakes a dedicated PM pass would have caught
(`reviews/02-spec.md`).

The one sequencing decision that actually mattered — inserting a spike
(T1.5, see Part 7) before broad implementation — came from the
*engineering* review, not a PM pass. That is arguably the right place for
it: sequencing driven by a genuine technical unknown belongs with the
review that found the unknown.

**Checkpoint 2**
- [ ] You can explain why "no PM ran" is recorded as a stated gap rather
      than silently absorbed into the CEO review's output

---

## Part 3 — Architecture

**Governing lesson:** *architecture should remove the most important
technical constraints with the fewest moving parts.*

### 3.1 The tweet-data path

```
Browser
  |
Next.js application
  |
/api/tweet/[id]              <- server-side only
  |
react-tweet
  |
X/Twitter public syndication endpoint
```

The syndication endpoint blocks direct browser CORS requests — verified
live against the real endpoint, not assumed. A server-side hop is
structurally required, not a stylistic choice. `/api/tweet/[id]` reuses
`react-tweet`'s own server-side fetch pattern rather than hand-rolling a
proxy.

### 3.2 The export path

```
Rendered tweet DOM
  |
modern-screenshot
  |
capture-time asset handling
  |
/api/image-proxy             <- SSRF-hardened
  |
PNG
```

The live preview can display remote images freely — cross-origin `<img>`
tags render normally in any browser. Export is different: turning DOM into
a canvas requires *reading pixel data*, and CORS blocks that for
cross-origin images unless they're served through something the browser
trusts. That's the whole reason the image proxy exists, and why it only
matters at **capture time**, never for the live preview — a distinction
found the hard way in Part 7.

### 3.3 Components

| Component | Role |
|---|---|
| Next.js | App Router, TypeScript, hosted on Vercel |
| react-tweet | Fetches via X's free public syndication endpoint |
| modern-screenshot | DOM → PNG export, routed through the proxy at capture time |
| Server route | `/api/tweet/[id]` — server-side only |
| Image proxy | `/api/image-proxy` — SSRF-hardened |
| URL-based share state | Customization state lives in the URL, not a server |
| No database | V1 has no accounts, no persistence layer |

A working component is not the same thing as a complete product
architecture — this covers what V1 actually needed, not everything a
mature product would eventually have (see Part 16 for the honest gap list).

**Checkpoint 3**
- [ ] You can explain why the live preview needs no proxy but export does
- [ ] You can name the fewest-moving-parts constraint this architecture
      removes

*Source: `README.md` "Architecture note"; `reviews/01`, `04`.*

---

## Part 4 — Security and UX review

**Governing lesson:** *a feature is not finished when only the happy path
works.*

Both were reviewed before broad implementation, embedded in the CEO
review's Sections 3 and 11 rather than run as separate roles.

### 4.1 Security

| Control | Detail |
|---|---|
| Exact-hostname allowlist | `pbs.twimg.com`, `abs.twimg.com`, `video.twimg.com` — substring matching was rejected explicitly (it would let `evil-twimg.com.attacker.net` through) |
| HTTPS-only | Non-`https:` URLs rejected outright |
| Redirect revalidation | Every redirect hop is re-checked against the same allowlist — blind redirect-following is a classic SSRF bypass |
| Response-size cap | 10MB, checked both via header and after download |
| MIME validation | Only `image/*` and `video/*` content-types accepted |
| No credential forwarding | The proxy never forwards cookies or auth headers upstream |

### 4.2 UX

| Concern | Resolution |
|---|---|
| Loading state | A tweet-shaped skeleton, not a spinner |
| Thread partial failure | Inline error card; **export is blocked** until the failing tweet is resolved or removed — never silently dropped |
| Retry / Remove | Both available per failed thread item |
| Mobile / responsive | A tested baseline, not a full audit |
| Accessibility | Keyboard-operable controls, ARIA labels, focus states — a baseline, not a full audit |

**Distinguishing three failure classes, precisely, matters:** a *security
failure* is an attacker reaching something they shouldn't (the SSRF class
above); a *product failure* is the software doing the wrong thing with no
attacker involved (silently dropping a failed thread tweet from an
export); *user confusion* is the software doing the right thing in a way a
person can't follow (no loading state, no error message). All three get
different fixes — conflating them produces the wrong fix.

**Checkpoint 4**
- [ ] You can name the specific SSRF bypass the exact-hostname allowlist
      prevents
- [ ] You can distinguish a security failure from a product failure from
      user confusion, with an example of each from this project

---

## Part 5 — Independent second opinion and cross-model tension

**Governing lesson:** *independent review is valuable when it creates
productive disagreement.*

A "cross-model tension" is not a typo an approver missed — it's when an
independent reviewer finds that two apparently reasonable decisions
*conflict*, or that a fix approved earlier quietly breaks a requirement
approved later. **Stated limitation:** this pass ran as a same-model
fresh-context subagent, not a genuinely different model or provider —
Codex CLI and bash were unavailable in this environment. It still found
real things a same-context review likely would have missed.

```
Initial plan
  |
independent challenge
  |
contradiction / hidden assumption
  |
decision
  |
revised plan
```

| # | Tension | The contradiction | Resolution |
|---|---|---|---|
| OV-1 | Rate limit vs. "no secrets" | Serverless in-memory counters reset every cold start — a limiter built that way silently does nothing, but real limiting needs a shared-state credential the "no secrets" pillar had ruled out | Corrected: real limiting needs Upstash/KV, fail-open on backend errors |
| OV-2 | Safari clipboard gesture | The already-approved clipboard fix (await fonts, await capture, then write) breaks Safari/iOS's requirement that `clipboard.write()` fire within the same synchronous gesture chain as the click | `ClipboardItem` wraps a `Promise<Blob>` directly, never awaited first |
| OV-3 | Video export undefined | Nothing in the plan said what "export a video tweet" even means for a static-image tool | Poster-frame swap + play-icon badge, so it reads as intentional |
| OV-4 | Thread URL length uncapped | A real thread's URL-encoded share state has no natural ceiling | Hard cap ≈ 12 tweets, explicit message, never silent truncation |
| OV-7 | Premature shared-component assumption | The plan asserted "single-tweet and thread modes will obviously share `TweetCanvas`" before any thread code existed | Softened to an explicit re-evaluation checkpoint rather than treated as settled |

6 of 8 tensions were accepted outright, 1 (OV-7) was softened rather than
accepted or rejected, 1 was skipped as low-value given independently
verified evidence. A second model that only approves the first model's
output is not adding a review layer — it's adding latency.

**Checkpoint 5**
- [ ] You can explain, in your own words, what made OV-1 a genuine
      *contradiction* rather than just a missing feature
- [ ] You understand why "the second model agreed" is not itself evidence
      of anything

*Source: `reviews/03-eng-review.md` (OV-1 to OV-8).*

---

## Part 6 — Engineering review

**Governing lesson:** *product plans describe intent; engineering reviews
test whether the intent is implementable.*

The question changes here from "what should we build?" to "can this plan
actually be built safely and cleanly, as written?" `/plan-eng-review` ran
against a 12-point charter the External AI Mentor drafted (architecture
integrity, external dependency risk, export correctness, security,
async/data-flow correctness, component/API design, implementation
sequencing, testing strategy, failure modes/observability, deployment
feasibility, simplicity/over-engineering, scope discipline) — not gstack's
own default prompt. See `docs/external_ai_mentor.md`.

| # | Finding | Class |
|---|---|---|
| B1 | The image-proxy "fix" from the CEO review had never actually been wired to any real DOM element — `react-tweet` renders plain `<img>` tags pointing straight at `pbs.twimg.com`; nothing in the plan rewired that | **BLOCKER** |
| B2 | Proxy hardening was incomplete: no redirect re-validation, protocol check, size cap, or MIME check specified | IMPLEMENTATION DECISION |
| B3 | No wait for images to finish decoding before capture — same silent-wrong-output class as the already-found font race | TEST REQUIREMENT |
| B4 | The rate-limiter (from OV-1) had no defined failure behavior — a fail-closed limiter turns an Upstash outage into a full app outage | IMPLEMENTATION DECISION |
| B5 | Thread per-tweet vs. whole-thread styling scope was never decided, which also affects the URL-length cap math from OV-4 | IMPLEMENTATION DECISION |

**B1 is the single most consequential finding in the whole project** — a
"fix" that, as planned, would never have run. It's why the implementation
sequence changed: **a mandatory spike (T1.5) was inserted before any broad
Route Handler code**, specifically to verify the image-proxy wiring
question with real code instead of more planning. Verdict: **PROCEED WITH
FIXES**.

**Checkpoint 6**
- [ ] You can explain why B1 is a BLOCKER and B2/B4/B5 are not, even
      though B2 is also security-relevant
- [ ] You can state, precisely, what "a plan that was never actually wired
      to real code" means for B1

*Source: `reviews/03-eng-review.md`.*

---

## Part 7 — The high-risk spike

**Governing lesson:** *successful execution is not proof of correct
output.*

This is the most important Part in the whole tutorial. **The question:**
how does `react-tweet`'s rendered media actually reach `modern-screenshot`,
and how should remote media be handled during export? B1 made this a real,
unresolved technical unknown — not a product question, a *does this
actually work* question.

### 7.1 The evidence-driven investigation

Not from documentation or memory — by reading the installed packages' real
compiled source:

- `node_modules/react-tweet/dist/twitter-theme/*.js` — `EmbeddedTweet`
  accepts a `components` prop that can override how avatars and media
  render; `TweetMediaVideo` renders a real `<video poster={...}>` with the
  poster URL already present as a live attribute.
- `node_modules/modern-screenshot/dist/index.mjs` — `fetchFn(url)` is
  called for every remote image *during capture*, consumed exactly like
  the library's own `responseType: "dataUrl"` fetch path. This fact turned
  out to matter enormously.
- The same source-reading pass found `onCloneNode`/`onCloneEachNode` hooks
  that fire on the *cloned* DOM tree right before rasterization — the
  natural place to swap a `<video>` for its poster-frame `<img>` without
  touching the live, interactive page.
- **DOM rewriting turned out not to be needed at all**, because `fetchFn`
  intercepts assets at capture time only. The live preview keeps pointing
  at real `pbs.twimg.com` URLs — fine, since cross-origin images *display*
  normally; CORS only bites when a canvas tries to *read* their pixels.
  Only the capture step needed the SSRF-hardened proxy.

### 7.2 The bug this spike actually caught

```
Assumption:    the image-proxy fix should just work once wired up
Experiment:    read the library's real source; wire fetchFn to the proxy
First result:  "Success" -- modern-screenshot reported no exception
Bug found:     the exported PNG showed a broken-image icon where the
               avatar should have been
Root cause:    proxyAwareFetch returned a blob: object URL via
               URL.createObjectURL() -- works fine for a normal <img
               src>, but modern-screenshot serializes the cloned DOM into
               an SVG string and reloads THAT as a fresh image resource;
               a blob: URL from the live document does not reliably
               resolve once embedded in that re-loaded SVG
Fix:           return a self-contained base64 data: URL instead, via
               FileReader.readAsDataURL() -- matching exactly what
               modern-screenshot's own responseType: "dataUrl" contract
               expects
Visual proof:  the corrected PNG was saved to disk and read directly --
               the real profile photo appeared, correctly
               circular-cropped, in place of the broken-image icon.
               Capture time also dropped (1046ms -> 468ms), a secondary
               confirmation that a slower, failing path had been replaced
```

Everything else in that first capture — text, font, gradient background,
rounded corners — was correct. This is a textbook silent-wrong-output
failure: the code "worked" by every naive check and still produced the
wrong result.

**Checkpoint 7**
- [ ] You can explain, precisely, why a `blob:` URL fails inside a
      re-loaded SVG resource but works fine in a normal `<img src>`
- [ ] You can state what "no exception thrown" actually proved here (and
      what it didn't)

*Source: `reviews/04-qa-report.md`.*

---

## Part 8 — AI Engineer implementation

**Governing lesson:** *build the smallest vertical slice that produces
evidence.*

Implementation proceeded in phases (per the External AI Mentor's 14-phase
instruction — see `docs/external_ai_mentor.md`), not one giant code dump:
baseline, the T1.5 spike, the real UI, interaction correctness, thread
mode.

### 8.1 Component boundaries

| Component | Owns | Does not own |
|---|---|---|
| `TweetCanvas` | Rendering one tweet | Fetch state, thread state, export state |
| `ExportPipeline` (`export-image.ts`) | Receiving a DOM node and producing a PNG | Whether that node represents one tweet or a whole thread |
| `ThreadBuilder` | Ordered multi-tweet behavior: add, reorder, retry, remove | Single-tweet rendering |
| URL state (`style-state.ts`, `thread-state.ts`) | Serialization/deserialization only | Any rendering or fetch logic |

### 8.2 What actually got built

- Tweet URL parsing (`tweet-url.ts`)
- `/api/tweet/[id]` — server-side fetch, reused `react-tweet`'s own pattern
- `/api/image-proxy` — the SSRF-hardened proxy from Parts 3-4
- `TweetCanvas`, `CustomizePanel`, `ExportControls`, `TweetSkeleton`
- Stale-response protection: a request-token + `AbortController` pair —
  the *later* of two racing requests always wins, verified with a
  deterministic network-delay test, not luck
- Versioned URL state with `popstate` back/forward support — verified
  against real DOM attributes, after discovering the browser-automation
  tool's own `back()`/`forward()` wrapper doesn't support pushState-based
  SPA routing (a tooling limitation, caught and worked around, not an app
  bug — see Part 9)
- `ThreadBuilder`: manual multi-URL builder, independent fetch-per-item,
  reorder, duplicate-prevention, retry, remove, the inline error card from
  Part 4, shared style across the whole stack

### 8.3 DRY as a hypothesis, not a religion

OV-7 (Part 5) flagged "TweetCanvas will obviously be shared between
single-tweet and thread modes" as an unverified assumption stated before
any thread code existed. It was softened to a re-evaluation checkpoint
rather than either accepted or rejected outright — the honest position
when you don't yet have the second use case in front of you to check
against.

**Checkpoint 8**
- [ ] You can name one component boundary above and explain why the split
      matters (what breaks if the boundary is crossed)
- [ ] You can explain what "DRY as a hypothesis" means in your own words

---

## Part 9 — Aside AI Browser and real-browser QA

**Governing lesson:** *real-browser behavior is a separate evidence layer
from code correctness.*

Aside — an AI-native real browser — was already installed on this Windows
11 machine from a prior session, along with its command-line automation
interface. The explicit rule (drafted by the External AI Mentor, not a
one-line user preference): *"use Aside as the primary browser for all
interactive browser work; do NOT install a separate Chromium; if Aside
fails, STOP and report why rather than automatically switching browser
engines unless explicitly approved."* This rule held under real pressure —
a rejected `npm install -D playwright` call was abandoned mid-session in
favor of the already-verified Aside CLI, not silently worked around.

Three distinct evidence layers, not interchangeable:

| Layer | Verifies |
|---|---|
| Automated tests | Deterministic logic in isolation |
| AI browser QA (Aside) | Real application behavior, in a real browser |
| Human browser testing | Usability and perceived correctness |

Every checkpoint from the T1.5 spike through the final production smoke
test ran through Aside: network-delay injection to force the stale-request
race deterministically (Part 8); real `window.history.back()/forward()`
checked against actual DOM attributes, after Aside's own
accessibility-snapshot rendering of `aria-pressed` turned out unreliable
for one component (a tooling quirk, caught mid-session, not a real app
bug); real downloaded PNGs read and visually inspected — this is what
actually caught the avatar bug in Part 7.

**Checkpoint 9**
- [ ] You can state the explicit rule that governed which browser engine
      to use, and the one real moment it was tested
- [ ] You can name one thing Aside's own tooling got wrong during this
      project, and how the team told that apart from an app bug

---

## Part 10 — Human-in-the-loop manual testing

**Governing lesson:** *AI can produce evidence; a human still decides
whether the evidence is good enough.*

This is reported by the user, not independently verifiable by the AI —
**that is exactly the point.**

**Local test:** opened PowerShell, ran the Next.js dev server, opened the
app in Aside manually, tested the single-tweet and thread interfaces,
exported a PNG, opened the downloaded file, and visually inspected it.

**Production test:** opened the deployed Vercel application, repeated the
core flow, visually confirmed the result.

What this added that no automation did: subjective visual quality ("does
this look right?"), whether the product *feels* usable rather than merely
functions, confidence in the exported artifact as something a person would
actually want to share, and the consequential approval decisions —
including two human-only gates no AI performed or should perform: Vercel
account authentication, and the decision to ship.

**Checkpoint 10**
- [ ] You can name three things human testing added that no AI-driven
      check in this project could have produced
- [ ] You can name the two human-only authorization gates in this project

---

## Part 11 — The Evidence Ladder

**Governing lesson:** *evidence becomes stronger as it gets closer to the
real user and the real output.*

Ten levels, weakest to strongest, as this project actually climbed them:

| Level | What it actually removes uncertainty about |
|---|---|
| 1. Idea | Nothing about feasibility yet |
| 2. Plan / architecture assumption | Intent, not truth |
| 3. Code compiles / builds | Type correctness only |
| 4. Automated test | Isolated function behavior — **not written this project, a stated gap** |
| 5. Local browser "succeeds" | Looks like proof — usually isn't. **The avatar bug hid exactly here.** |
| 6. Real-browser behavior (Aside, deterministic setup) | A specific, hard-to-reproduce failure, made repeatable |
| 7. Exported artifact visually inspected | "No error" ≠ "correct output" — **this is what caught the avatar bug** |
| 8. Human visual inspection | Blind spots automated checks share |
| 9. Production deployment | "Works in dev" vs. "works with real infrastructure" |
| 10. Human production test | Does the *actual shipped thing* hold up |

**The rule this project's own history proves:** "the capture function
returned successfully" was much weaker evidence than "a human visually
inspected the exported PNG." Treat "returned without throwing" as the
*start* of verification, not the end — climb to level 7 (at minimum)
before calling a visible-output feature verified.

Tutorial #3 taught a mechanical gate chain (T1-T5, pass/fail/VOID) as its
verification model, appropriate for a subject with deterministic
mechanical checks. This project's real risk — a silent-wrong-output bug a
pass/fail script cannot catch by construction — is why this tutorial
teaches the Evidence Ladder instead: a framework for *how much* verification
a claim needs, not just whether one check passed.

**Checkpoint 11**
- [ ] You can name which Evidence Ladder level your own last "it works"
      claim actually reached
- [ ] You can explain, precisely, why level 5 is the trap level

*Source: `reviews/04-qa-report.md`.*

---

## Part 12 — When debugging becomes waste

**Governing lesson:** *persistence is not progress if the experiment is
not reducing uncertainty.*

The real episode: a thread share-link's style preset sometimes failed to
restore on initial load. React state was directly confirmed correct via
temporary instrumentation on every render — `style.backgroundId` really
was `"midnight"` — while the rendered DOM's own `aria-pressed` attribute
still showed the default. A genuine state-vs-DOM discrepancy, not a logic
bug in the decoder or component code (both verified correct in isolation).
It survived a Strict Mode toggle, a full Turbopack cache clear, and a dev
server restart. This consumed the largest single block of investigation
time in the project.

**The better debugging model — check the first layer that could be wrong,
not the tenth:**

```
URL
  |
decoder
  |
hydration
  |
React state
  |
component props
  |
DOM
  |
browser observation
```

**Rule, at each layer:** PASS → stop changing that layer, move to the
next. FAIL → investigate *that* layer first, don't jump ahead.

**The timebox principle:** if roughly 20-30 minutes of debugging isn't
meaningfully narrowing the hypothesis space, stop adding logs. Make the
experiment smaller. Isolate one boundary. The right move here would have
been timeboxing this investigation *before* it consumed as many tool calls
as it did, not after — the eventual decision to stop and document it was
correct, and should have arrived sooner.

**Checkpoint 12**
- [ ] You can explain why "React state was confirmed correct" did not end
      this investigation
- [ ] You can state the timebox rule in one sentence

*Source: `reviews/05-ship.md` ("Where time was spent").*

---

## Part 13 — Rapid finalization

**Governing lesson:** *shipping speed comes from choosing what not to
investigate.*

The deliberate transition from "investigate everything" to "fix
release-critical issues, document the rest, ship."

| Fix | Defer |
|---|---|
| Build failures | Minor styling |
| Crashes | Speculative refactors |
| Core export failure | Perfect test coverage |
| Serious security issues | Rare non-core edge cases |
| Obviously broken core interactions | V2 functionality |

Concretely: `TODOS.md` records verification debt explicitly (implemented-
but-unverified vs. known-bug vs. intentionally-deferred, each labeled, not
blended together); diagnostic code was removed; starter-template residue
(page title, metadata, README) was cleaned up; a final production build
ran; one rapid Aside smoke test replaced a full re-audit.

This mode switch traces to two External AI Mentor interventions (full
detail in `docs/external_ai_mentor.md`): first, shown a transcript of the
Part 12 debugging session running long with no isolated root cause, the
mentor said *"I would stop this current debugging run now and reset the
debugging method"* and drafted a five-layer binary-search protocol.
**What actually happened next is worth teaching honestly:** the human did
not run that specific protocol. Having already completed human-in-the-loop
testing (Part 10), they asked instead for a faster "finalize this project
ASAP" prompt — which produced the Ship Mode instruction this Part follows.
The specific protocol didn't survive the pivot; the underlying principle
(stop, timebox, document rather than chase) did.

**Checkpoint 13**
- [ ] You can sort three hypothetical bugs into "fix now" vs. "defer,
      documented"
- [ ] You can explain why the mentor's specific suggested protocol not
      being used doesn't undermine the intervention's value

---

## Part 14 — Deployment and the human authorization gate

**Governing lesson:** *consequential authorization remains a human gate
even in an AI-native workflow.*

```
Agent prepares deployment
  |
human authorizes account access
  |
agent deploys
  |
AI browser verifies production
  |
human verifies production
```

The Vercel CLI was not globally installed; `npx vercel` was used
throughout — no permanent install needed. The human ran `npx vercel login`
themselves, in their own terminal; authorization completed manually inside
Aside; `npx vercel whoami` confirmed success before control was handed
back to the AI. From there the AI completed the deployment sequence
autonomously: confirmed auth, ran a final production build, created the
Vercel project, deployed. Vercel's own documented behavior means the first
deployment for a new project always becomes production directly — there
was no separate preview URL to gate on, so the production smoke test ran
against the live URL immediately.

**What this Part deliberately does not show:** real usernames, team names,
device-authorization codes, or OAuth URLs. Those were reviewed and
excluded before this tutorial was written — see
`docs/TUTORIAL_4_PRIVACY_REVIEW.md`. The *sequence* is the teaching content;
the specific account is not.

**Checkpoint 14**
- [ ] You can name the one action in this entire deployment sequence that
      the AI could not and should not have performed
- [ ] You can explain why "the first deploy becomes production" changed
      the verification sequence

---

## Part 15 — Production result

**Governing lesson:** *production evidence matters more than localhost
confidence.*

**Verified production flows:**

- **Single tweet:** load a tweet → customize → export PNG / clipboard /
  share link
- **Thread:** load multiple tweets → export as one combined PNG

Both were confirmed via real-browser automation (Aside) and reported by
the human as manually tested against the live deployed URL, separately
from the local test in Part 10. No fatal console errors were observed in
the tested flows.

**What this tutorial does not claim:** video-tweet export, emoji
rendering, and multi-image tweets are implemented but were not empirically
verified this session — see Part 16. Untested behavior is not claimed as
working; it's named as untested.

**Checkpoint 15**
- [ ] You can name the two flows this project actually verified in
      production, and the ones it explicitly did not

---

## Part 16 — Known limitations and verification debt

**Governing lesson:** *known limitations are acceptable when they are
explicit, bounded, and compatible with the release goal.*

| Item | Status |
|---|---|
| Rate limiting on both public API routes | Planned, reviewed twice (OV-1, B4), never implemented in code |
| Thread share-link style restoration | Investigated one bounded pass (Part 12); root cause not found |
| Video / emoji / multi-image export | Implemented, not empirically verified |
| Safari / iOS clipboard | Implemented, not empirically verified on real Safari |
| Automated test suite | Not written, despite the plan specifying one — a stated process gap |

**Four distinct categories, not one blur:** *implemented but unverified*
(clipboard, video/emoji/multi-image — the code path exists, nobody has
exercised it with real data); *known bug* (the thread style restoration);
*intentionally deferred feature* (rate limiting — a real gap the SSRF
hardening does not cover, acceptable for a tutorial-scale demo, not for
real public traffic); *security control required before scaling* (rate
limiting again, stated as such rather than implied fixed).

None of these blocked shipping Tutorial No. 4's V1, because none of them
touch the two verified core flows from Part 15, and every one of them is
named here rather than discovered by a reader the hard way.

**Checkpoint 16**
- [ ] You can sort each item above into its correct category
- [ ] You can explain why "rate limiting was reviewed twice" does not mean
      "rate limiting is safe to skip"

*Source: `TODOS.md`; `reviews/05-ship.md`.*

---

## Part 17 — Reusable gstack Project Operating System

**Governing lesson:** *the reusable asset is not the code — it is the
development system that produced the code.*

The full 16-stage sequence (Part 0's diagram, expanded with purpose, exit
criterion, and human gate for each stage) is written out in full in
[`docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md`](docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md) —
concise enough to actually reuse on your next project, not just admire.
Two structural notes worth carrying forward before you open that document:

- **Size the topology to the subject.** This project ran one domain
  reviewer's worth of independent challenge (Part 5), not two, and skipped
  a dedicated PM role (Part 2) because the CEO review already covered it.
  Copy the *judgment*, not the exact role count.
- **The mentor pattern's generalization is unproven beyond this one
  project.** Four sourced correction examples (`docs/external_ai_mentor.md`)
  are enough to teach the pattern, not enough to prove it always pays for
  itself. Test it on your own next project before trusting it blindly.

**Checkpoint 17**
- [ ] You have opened `docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md` and can
      name its exit criterion for the high-risk-spike stage

---

## Part 18 — Final lessons

Ten lessons this project actually earned, not ten generic best practices:

1. Plan before coding, but do not over-plan — the CEO review took one
   pass, not five.
2. Separate AI roles by decision type: product judgment, technical
   feasibility, and correctness verification are not the same question.
3. Independent review should challenge assumptions, not just approve the
   first draft — see Part 5's four real contradictions.
4. Test the highest-risk assumption early, with a mandatory spike, before
   broad implementation — B1 and the T1.5 spike (Parts 6-7).
5. A green function call can still produce the wrong artifact — the avatar
   bug is this project's proof, not a hypothetical.
6. Real-browser evidence matters, and it's a separate layer from both
   automated tests and human judgment, not a replacement for either.
7. Human visual judgment remains irreducible — no automated check in this
   project could confirm "this looks right."
8. Known limitations do not automatically block shipping — they need to
   be explicit, bounded, and outside the release goal's core flows.
9. Humans retain consequential authorization and the ship decision, every
   time, with no exception this project made.
10. Finishing is an engineering skill — Part 13's rapid finalization was a
    deliberate mode switch, not giving up.

---

## Tutorial No. 4.1 — Post-launch iteration

Parts 0-18 above are the original, complete Tutorial No. 4: premise
through first production deploy. They are left intact — this is not a
rewrite. The four parts below are a second, later case study on the same
codebase: a product design revision and a real production bug, both
discovered and resolved *after* the app in Part 15 was already live. If
Tutorial No. 4 teaches how AI-native development gets you to a working
first release, Tutorial No. 4.1 teaches what happens next — because
"shipped" is not "finished," and the discipline that got you to
production is exactly the discipline you need to keep it correct once
real humans start using it.

## Part 20 — Product Design 4.1: From Engineering Prototype to Startup Product

**Governing lesson:** *product design is not decoration; it reduces user
uncertainty.*

Part 15's production app was functionally verified and genuinely
working. It was also, on a fresh human look weeks later, judged to read
as an engineering prototype rather than a product someone would trust
with their own content. Those are two different questions, and this
project had only ever answered the first one:

| | Engineering QA asks | Product design QA asks |
|---|---|---|
| The question | "Does it work?" | "Does the user immediately understand and trust it?" |
| Evidence | Passing tests, correct output | A five-second first impression, held to the same evidentiary standard as Part 11's Evidence Ladder |

A current-state review of the live app found real, specific gaps, not
vague dissatisfaction: no persistent header or navigation, so Thread mode
(a real, working feature) was undiscoverable from the single-tweet page;
a plain, unstyled `<input>` and default-browser form controls; the tweet
preview sitting in an unbordered flex row rather than reading as the
page's visual hero; three export buttons of identical visual weight, so
"which one finishes the job" had no clear answer; and a confirmed
horizontal-overflow bug at 375px that clipped real content off the right
edge of the screen. None of these were logic bugs — the app was correct
and the export byte-identical to what shipped in Part 15. They were
trust signals a first-time visitor reads in seconds, before ever clicking
anything.

**The five-second test**, borrowed directly here so you can run it
yourself on your own project's landing state: look at the empty-state
screen for no more than five seconds, then look away, and answer from
memory — *what does this product do? Where would you click to start?
What output would you expect? Would you notice a second mode (Thread)
exists? If you had output loaded, would you know which button actually
finishes the job?* Write your own hypothesis for each answer *before*
checking it against the real UI — the point is not to grade the design,
it's to notice which of your assumptions about "obviously discoverable"
don't survive contact with a first look.

**Three design directions were drafted as standalone HTML concept
mockups** (not live code — throwaway comparison artifacts, deliberately
cheap to produce and discard) before any implementation began. A human
selected **Direction A — "Quiet Creator Tool"**: a persistent header
establishing product identity and cross-linking Single Tweet/Thread
modes, a real headline stating the outcome ("Turn any tweet into a
beautiful image") instead of just the product's name, a two-column
preview + inspector layout for the loaded state, and one filled primary
export action against two visually lighter secondary ones.

**Implementation happened on an isolated branch**, never touching `main`
until explicitly merged — the same human-authorization-gate discipline
from Part 14, applied to a design change instead of a first deploy. The
build and lint gates from Part 6 ran clean on the branch before any
human looked at it visually. The redesign was also, deliberately, proven
*not* to be a rewrite in disguise: export architecture, the API routes,
and the exact DOM node `captureNodeToPng` actually rasterizes were
diffed byte-for-byte against pre-redesign `main` and confirmed unchanged
— a design review earns no license to quietly change what a correctness
review already signed off on.

**Human review verdict: "B — approve with minor changes."** Not a flat
approve, not a rejection — six specific, named items came back: a real
header/content padding mismatch at 375px (not a personal-taste note, a
measurable bug in the redesign itself), a redesigned loaded-state
URL/action row, an inspector card that was stretching to fill unused grid
height instead of hugging its own content, and a border/pill treatment
for the two secondary export buttons so they read as clickable. All six
were presentation-layer only, all six were re-verified against the same
export-architecture and byte-identity checks as the first pass, and the
polish commit disclosed something else worth keeping in the record
rather than quietly fixing: while starting a second local server on an
alternate port for verification, a process-cleanup command briefly
targeted and stopped the *wrong* process — the human's own active `npm
run dev` session, not the intended verification server. It was caught
immediately and the dev server was restarted; the mistake is recorded
here because a tutorial that hides its own author's mistakes teaches a
falsely smooth process.

A second human visual pass on the polished branch, then the same
merge-into-`main` gate from Part 14 — human authorization required, no
exception — closed this Part.

**Checkpoint 20**
- [ ] You can name three specific trust-signal gaps this review found that
      no unit test could ever catch
- [ ] You can explain why "the export is byte-identical before and after"
      is a *design-review* claim as much as an engineering one
- [ ] You can state, in one sentence, why the wrong-PID mistake belongs in
      this tutorial rather than being quietly edited out

*Source: `docs/DESIGN_REVIEW_4_1_CURRENT_STATE.md`,
`docs/DESIGN_REVIEW_4_1_DIRECTIONS.md`,
`docs/DESIGN_REVIEW_4_1_HUMAN_REVIEW.md`,
`docs/DESIGN_REVIEW_4_1_RELEASE.md`.*

---

## Part 21 — Fidelity Testing: The X Broadcast Boundary

**Governing lesson:** *before fixing a missing output, find the first
layer where the information disappears.*

A human reviewer, comparing the live app against the real tweet at
`x.com/elonmusk/status/2100296847344783441`, found a real, reproducible
gap: the quoted post inside that tweet embeds a live X Broadcast, and
X.com renders it as a rich, animated card — title, live speaker avatars,
a duration ticker, a view count. The app rendered the same quoted tweet
as plain text plus a bare `x.com/i/broadcasts/…` link. No card, no
thumbnail, nothing rendered wrong so much as nothing rendered at all.

**The instinct to avoid: guessing which layer dropped the data and
patching that guess.** The disciplined alternative is the same
first-failing-layer method Part 12 already taught for a different bug —
walk the pipeline in order, and stop at the first layer that actually
fails, not the first layer you suspect:

```
Original X.com page (rich Broadcast card, rendered by X's own
  authenticated, proprietary client-side JS)
  |
free syndication payload  (cdn.syndication.twimg.com/tweet-result --
  the ONLY data source this app is allowed to use; no paid X API)
  |
react-tweet  (the open-source embed library this app renders through)
  |
this app's DOM
  |
PNG capture
```

**Layer 2 is where the trail goes cold.** The raw syndication payload for
this exact tweet was fetched and inspected directly: the quoted tweet's
JSON contains only a plain URL entity pointing at the broadcast link —
no `card`, no `mediaDetails`, no poster, no title, no duration, no
participant data, anywhere in the response. X's other free endpoint,
oEmbed, was checked too, and confirms *why*: it returns nothing but a
bare `<blockquote>` and a `<script src="widgets.js">` tag — the real
card is assembled entirely client-side, by X's own proprietary script,
against X's authenticated internal APIs. There is no static, fetchable
representation of a Broadcast card anywhere in the free data surface.

**Layer 3 was checked too, not assumed clean.** `react-tweet`'s own
TypeScript types and rendering components were read directly: there is no
`card` or `broadcast` field anywhere in its type definitions, and a
full-text search of its distributed source for either word returns zero
matches. The library was never built with a concept of link/broadcast
preview cards — this is not a regression, it is a capability that never
existed.

**A contrast test is what turns "the data is missing" into "the data is
missing *specifically here*, not everywhere.**" An ordinary tweet with
native video — where the syndication payload *does* include
`mediaDetails`/`video` — was captured and exported through the exact same
app, and rendered correctly: poster frame, play badge, "Watch on X"
label, all present. That single control case is what separates the
correct conclusion from the tempting overreach:

> This tutorial does not say "video does not work." It says: X Broadcast
> (`x.com/i/broadcasts/…`) rich-card fidelity is bounded by what the free
> syndication path exposes — ordinary native photo and video media,
> confirmed by the control case, is unaffected.

**Classification: known upstream limitation, not a bug.** modern-screenshot
(the export library) was never reached in this investigation and is not
implicated — the information was already absent three layers upstream of
where capture even begins. No fix exists inside the free-data
constraint this project deliberately operates under (Part 0 rules out a
paid X API from the start). A generic, honest fallback was scoped as an
optional idea, explicitly **not implemented**: a static label reading
"X Broadcast — preview unavailable · Open on X" — truthful about what
isn't there, never a fabricated title, poster, duration, or viewer count
standing in for data the app was never given.

**Checkpoint 21**
- [ ] You can draw the five-layer pipeline above from memory and name
      which layer actually failed
- [ ] You can explain what the native-video control test proved that the
      Broadcast test alone could not
- [ ] You can state why "show a fabricated poster image" would have been
      a worse fix than no fix at all

*Source: `TODOS.md` ("Known upstream limitation"),
`docs/DESIGN_REVIEW_4_1_RELEASE.md` ("Media fidelity boundary").*

---

## Part 22 — Thread Export Failure: When the First Hypothesis Is Wrong

**Governing lesson:** *good debugging is not proving your first
hypothesis; it is killing the wrong hypothesis quickly.*

A human, testing a real, media-heavy two-tweet thread in production,
hit "Export timed out — try a lower scale" — the app's own honest
failure message, not a crash. A printed PDF of the thread page (captured
before attempting export) proved the DOM itself had rendered correctly:
both tweets visible, both their embedded videos showing a normal poster
frame. The failure was somewhere in the export stage specifically, not
in loading or rendering.

**Hypothesis 1, the obvious one: this thread is just too big for the
requested export scale.** Cheap, specific, and directly testable — export
the exact same fixture at 1×, 2×, and 3× and see whether the failure
scales with pixel area the way a real size problem would.

| Scale | Result | Time to failure |
|---|---|---|
| 1× | FAIL | ~8.2s |
| 2× | FAIL | ~8.2s |
| 3× | FAIL | ~8.2s |

**All three failed at the same time, to the second.** A genuine
pixel-budget problem would fail *later* at 1× than at 3× — more scale
means more raw canvas area, more work, a longer failure curve. Identical
failure timing at every scale is not weak evidence against Hypothesis 1;
it actively disproves it. The 8.2-second mark was also suspicious on its
own: it matches the app's fixed 8-second capture timeout almost exactly,
which raises a different question — is 8 seconds really the constraint,
or is something else *always* taking at least that long, at any size?

**The disciplined next move was not "just raise the timeout."** The
capture timeout was temporarily bumped to 60 seconds, purely as a
diagnostic — never as a proposed fix — and the same export was attempted
again, with the app's own resource-timing instrumentation watching
exactly when each individual media request actually fired.

**Result: still failed, at 60 seconds, having made zero image-proxy
requests the entire time.** Not "slow" — stuck. Something was hanging
*before* the export pipeline ever reached the step of fetching a single
image. That single data point reframed the whole investigation: pixel
count was never the variable that mattered.

**Hypothesis 2, narrower and testable in under a minute: is this actually
about threads at all, or about video?** Both tweets in the failing
fixture happened to contain native video. A *single*, non-threaded tweet
with a native video, exported alone, hung identically — same unbounded
stall, same zero proxy requests. The bug had nothing to do with threads;
threads just happened to be where a human first noticed it, because this
particular fixture had two videos instead of the usual one.

**Reading the actual library source, not guessing at it, found the real
mechanism.** modern-screenshot's own internal video-cloning step —
completely separate from and running *before* this app's own
poster-frame-swap logic ever gets a chance to run — does this:

```
clonedVideo.currentTime = video.currentTime
await new Promise(resolve =>
  clonedVideo.addEventListener("seeked", resolve, { once: true })
)
```

This app's videos are never played — they sit at their default poster
frame, so `video.currentTime` is always exactly `0`. Reassigning `0` to
a clone whose `currentTime` is *already* `0` performs no actual seek in
Chromium, so the `seeked` event this code is waiting for never fires.
The `await` hangs forever — not for a long time, forever — and it hangs
inside the library's own clone step, before this app's `onCloneNode`
video-poster-swap hook is ever invoked. That hook had existed in the
codebase since before Part 15 and had never actually been exercised
against a real playing video; `TODOS.md` had honestly flagged it as
"implemented, unverified" rather than claiming it worked. It could not
have worked, structurally, no matter how it was written, because it ran
on the wrong side of the hang.

**The fix removes the hazard instead of working around it.** Before
handing anything to modern-screenshot, the app now clones the export node
itself, swaps every `<video>` element for its poster `<img>` on that
clone — attached off-screen so layout and computed styles resolve
exactly as on the live node — and only then passes the sanitized clone to
the capture library. modern-screenshot never sees a real `<video>`
element, so its internal seek-wait path never runs. No timeout was
raised. No pixel cap or scale restriction was added. There was nothing
to raise a timeout *for* — the process was never going to finish, at any
duration, until the actual hazard was removed.

**Verification, the same discipline as Part 11's Evidence Ladder,
climbed a second time:** a plain-text tweet's export was hashed
byte-for-byte identical before and after the fix
(`sha256 eb9b38e6392fad1ea450e77fff3d7423b58ee5b9605450b450f2f66c5490785b`,
405691 bytes) — proof the fix touched nothing about how ordinary content
is captured. The originally failing fixture then exported successfully
at 1×, 2×, and 3× in roughly 0.6-2 seconds each, both against a local
production build and, separately, in the actual production deployment.

> Byte-identical regression tests prove unchanged behavior; they do not
> prove the behavior was complete or correct in the first place. The
> plain-tweet hash never moved, through this entire investigation — and
> the video-export path was still completely broken the whole time. A
> passing regression suite and a working product are not the same claim.

**Checkpoint 22**
- [ ] You can state what "identical failure time at every scale" actually
      disproves, and why that's stronger than it first sounds
- [ ] You can explain why bumping the timeout to 60 seconds was a
      diagnostic step, not a candidate fix, and how the result told you that
- [ ] You can describe, from memory, why `currentTime = 0` assigned to an
      already-`0` value never fires `seeked` in Chromium
- [ ] You can explain why "the poster-swap code already existed" did not
      mean the video bug was already handled

*Source: `src/lib/export-image.ts`, `TODOS.md` ("Fixed: video tweet
export hung indefinitely"), `docs/DESIGN_REVIEW_4_1_RELEASE.md` ("Thread/
video export fix").*

---

## Part 23 — Human Evidence as the Final Layer

**Governing lesson:** *human testing catches failures that automated
checks cannot even formulate.*

Part 11 built an Evidence Ladder for a single artifact. Tutorial No. 4.1
extends it across an entire iteration cycle, because both bugs in this
Part's story were *found* by a human, not by automation — Part 20's
design gaps and Part 22's export hang were both invisible to every
passing test this project had. Extend the ladder one more rung past
where Part 11 left it:

```
Automated test
  |
Browser QA (Part 9)
  |
Exported artifact exists
  |
Human visual inspection
  |
Cross-application use          <-- new this cycle
  |
Production confirmation
```

**"Copy succeeded" is weaker evidence than "the copied image was pasted
successfully into another real application and visually confirmed."**
The distinction matters concretely here: this project's clipboard-copy
code path had sat in `TODOS.md` for the entire original tutorial as
"implemented, not empirically verified" (Part 16) — the `navigator
.clipboard.write()` call resolving without throwing was the only signal
anyone had ever checked. After the 4.1 fixes shipped to production, a
human ran the real test that signal alone can't stand in for: click Copy
image in Thread mode on the live production app, open Windows 11 Paint,
paste, and look at what actually landed on the canvas. It matched.
That is the rung "the promise resolved" cannot climb to by itself.

**The full chain of human evidence this cycle, in order:** a local
redesign review before any human ever saw the deployed result; the
original X.com page held directly against the app's rendering to find
the Broadcast gap in Part 21; a printed PDF of the thread page, captured
*before* attempting the export that would go on to hang, standing as
proof the DOM existed and had rendered correctly independent of whatever
export did next; a production Download PNG test on the fixed thread; a
production Copy image test; and the Paint paste-and-look step above,
closing the loop a programmatic clipboard check never could.

**Checkpoint 23**
- [ ] You can explain, in your own words, why "the clipboard API resolved
      without an error" and "a human pasted the image and looked at it"
      are different claims
- [ ] You can name one bug from this Part 20-23 cycle a human found that
      no automated check in this entire project's history would have
      caught
- [ ] You can redraw the extended Evidence Ladder above from memory

*Source: `docs/DESIGN_REVIEW_4_1_RELEASE.md` ("Thread/video export
fix" — human manual verification).*

---

## Troubleshooting

| Symptom | Likely cause | Minimal response |
|---|---|---|
| Port 3000 already in use | Another `npm run dev` still running | `taskkill /PID <pid> /F` (Windows) or use the port the tool suggests instead |
| `vercel` command not recognized | Vercel CLI not globally installed | Use `npx vercel` for every Vercel command — no permanent install needed |
| Aside CLI not found on PATH | Fresh install, PATH not yet updated in this shell | Re-open the terminal, or add the CLI's install directory to PATH explicitly |
| Browser automation says one thing, human sees another | Automation and human testing verify different things (Part 9) | Trust neither alone; re-check the specific claim by hand |
| Capture "succeeds" but the exported image is wrong | Silent-wrong-output — see Part 7 | Climb the Evidence Ladder (Part 11) to level 7 before trusting a capture |
| Running low on session context/tokens mid-task | Long investigation, verbose tool output | Checkpoint progress explicitly; don't let an unbounded debugging session (Part 12) consume the whole budget |
| A source document looks stale or contradicts the code | Documentation written before a later fix | Trust the code and the review files over prose; file it as a doc fix |
| EN/ZH tutorials seem to drift | No mechanical check was run | Run the parity script before trusting either language is current — see `docs/TUTORIAL_4_DOCUMENT_MANIFEST.md` |
| A deck or document "built successfully" but looks wrong | A clean build is not proof of correct rendering (Part 11's own lesson, applied to this tutorial's own tooling) | Render and inspect the actual output before calling it done |
| A working feature suddenly "hangs" with no error, ever | The library you're calling may be waiting on an event that never fires (Part 22's `seeked` case) | Check whether zero forward progress is being made at all (e.g. zero network requests) before assuming it just needs more time |
| A fix seems to scale-cap or pixel-cap a failure away | You may be treating the symptom, not the cause | Confirm the failure timing is actually correlated with size first (Part 22) — identical failure time at every size means size isn't the variable |
| Content visible on the real source site doesn't render in your app | Could be any of several layers, not necessarily "the library is broken" | Walk the pipeline in order and find the first layer that actually fails (Part 12, extended in Part 21) before patching anything |

---

## Disciplines worth keeping

- Evidence over confidence — climb the ladder, don't just check the box.
- The smallest experiment that could disprove your assumption.
- The high-risk spike goes first, not last.
- State verification debt explicitly; don't blend "untested" with
  "working."
- Separate AI roles by decision type, sized to the subject.
- Human authorization gates are non-negotiable, every time.
- Privacy review before publication, not after.
- Mechanically verify bilingual parity — don't trust it by eye.
- Render and inspect every generated artifact — a clean build is level 3,
  not level 7.
- Stop when the release goal is met; don't chase completeness for its own
  sake.
- "Ships" is not "finished" — a product design review after launch is not
  a failure of the first review, it's the next stage (Part 20).
- When a hypothesis about *why* something fails is cheap to test, test it
  before acting on it — identical failure timing across three different
  scales was the signal that killed the wrong hypothesis in one step
  (Part 22).
- A promise resolving without an error is not the same claim as a human
  confirming the result by hand in a second, real application (Part 23).

---

## Appendix A — Command reference

Only commands actually useful to reproduce this project. No real
credentials or account identifiers appear below or anywhere in this
tutorial — see `docs/TUTORIAL_4_PRIVACY_REVIEW.md`.

```bash
# Install and run locally
npm install
npm run dev              # http://localhost:3000  (single tweet)
                          # http://localhost:3000/thread (thread mode)

# Build and typecheck
npm run build
npx tsc --noEmit
npm run lint

# Deploy (no global install required)
npx vercel login         # opens a browser for account authorization
npx vercel whoami         # confirm authentication before deploying
npx vercel                # preview deployment
npx vercel --prod         # production deployment

# Aside readiness probe (conceptual shape -- see docs/external_ai_mentor.md)
aside repl 'console.log("ASIDE_READY " + pwd)'
```

## Appendix B — Bilingual glossary

| English | 中文 |
|---|---|
| AI CEO | AI CEO |
| AI Project Manager | AI 项目经理 |
| AI Architect | AI 架构师 |
| Security Review | 安全复核 |
| UX Review | 用户体验复核 |
| Second Opinion | 第二意见（外部意见） |
| Cross-model tension | 跨模型张力 |
| Engineering Review | 工程复核 |
| High-risk spike | 高风险验证性小试 |
| Evidence Ladder | 证据阶梯 |
| Human-in-the-loop | 人机协同（人工参与） |
| Browser QA | 浏览器 QA |
| Verification debt | 验证债务 |
| Minimal QC | 最低限度质检 |
| Ship gate | 上线关卡 |
| Meta-agent / External AI Mentor | 元智能体 / 外部 AI 导师 |
| Product design review | 产品设计复核 |
| Five-second test | 五秒测试 |
| First-failing-layer method | 首个失效层定位法 |
| Known upstream limitation | 已知上游限制 |
| Cross-application human test | 跨应用人工测试 |

## Appendix C — Definition of Done

- [x] EN tutorial (`TUTORIAL.md`) covers all 19 stages with a governing
      lesson and checkpoint per Part
- [x] ZH tutorial (`TUTORIAL.zh.md`) matches section-for-section
- [x] Structural parity verified mechanically, not by eye
      (`_build/verify_tutorial_parity.py`)
- [x] Privacy review complete — `docs/TUTORIAL_4_PRIVACY_REVIEW.md`,
      `docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md`
- [x] Word EN (`dist/gstack-tutorial-4_EN.docx`) built
- [x] Word ZH (`dist/gstack-tutorial-4_ZH.docx`) built
- [x] Word documents rendered and visually inspected, not just built —
      automated COM rendering hung in this environment (see
      `docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md` for that disclosed
      limitation); a human opened and reviewed both
      `dist/gstack-tutorial-4_EN.docx` and `_ZH.docx` directly in Microsoft
      Word and confirmed both look correct — this is the stronger evidence
      layer and stands as the completed check
- [x] Word documents privacy-scanned on rendered output
      (`_build/verify_doc_privacy.py`)
- [x] `docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md` complete
- [x] `docs/GSTACK_TUTORIAL_4_OUTLINE.md` complete
- [x] `docs/TUTORIAL_4_DOCUMENT_MANIFEST.md` complete
- [x] No stale "not yet written" claims remain anywhere in this tutorial
- [x] No private identifiers (username, hostname, account/team name, device
      codes) anywhere in this tutorial or its companion documents
- [x] Known limitations documented in Part 16, not hidden
- [x] Tutorial No. 4.1 (Parts 20-23) covers the post-launch design
      revision and the real production bug found and fixed after Part 15,
      in both EN and ZH, with the same governing-lesson/checkpoint format
- [x] Public code (`src/`) matches the verified, deployed Tutorial 4.1
      behavior — confirmed by a byte-for-byte diff against the private
      working repo's final commit
- [x] The X Broadcast limitation (Part 21) is stated accurately as a known
      upstream limitation, not a claimed fix
- [x] The thread/video export fix (Part 22) is documented as fixed, not
      left as a stale "known bug"
- [x] `docs/TUTORIAL_4_RELEASE_REPORT.md` and companion release docs
      updated to reflect the Tutorial 4.1 state
