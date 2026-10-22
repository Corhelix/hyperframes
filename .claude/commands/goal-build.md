---
name: goal-build
description: Drive a goal to completion hands-off across many steps, verifying each before the next.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a goal is driven to completion hands-off across many steps
  does_not_fire_when:
    - a single scoped change is wanted -> /build
    - the goal is not yet stated as a watchable end state -> /plan
  loads:
    always:
      - command-includes/_VERIFICATION-STANDARD.md
      - command-includes/_GOAL-FIRST-CONTRACT.md
      - command-includes/_GOAL-BUILD-TEMPLATES.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: goal
      is: one observable end state someone could watch happen
    - id: shipped
      is: what was built and the check that proves each step landed
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
    - v1.2 runs: goal-build-read-check.py exits 0 before Phase 1a and the read gate has not been waived
    - v1.2 runs with a base app: goal-build-screens-check.py exits 0 and goal-build-nav-crawl.mjs reaches every journey screen and the primary surface
    - v1.3 document or surface runs: goal-build-design-check.py exits 0 against the entity template, goal-build-content-check.py measure exits 0, and every review return passes its coverage check
  graded_by: cmo-verify

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

# /goal-build — Hands-Off Build to Completion

<!-- v1.3 2026-10-22 · MEASURE THE PRODUCT, NOT THE FILES. Evidence: Corhelix/alc-group PRs 438 and 439, a LinkedIn booklet and a screen-recording booklet.
     Both passed every structural check and were judged "technically correct, contextually a fail", then "not a booklet, not an SOP, too many images". Measured afterwards, the
     second held 229 figures for 229 steps, 76 repeats of a picture already on the page, 72 captions admitting that nothing was shown, 70 steps over 40 words, a filler line
     on 18 of 41 pages, and a stylesheet copied from the first build with 7 colours and 8 font families that the entity template does not contain. Every check had asked
     whether a thing exists. None had asked whether it is any use. The "copy the exemplar's CSS" line came from the brief, and nothing refused a brief that said it.
     WHAT CHANGED. Each change has a script that refuses it when skipped; global/tests/goal-build-content-suite.py plants each fault and requires the refusal.
     (1) Phase 1e: for a document or surface the design source is the entity template and its tokens; another build's output never is. goal-build-design-check.py.
     (2) Phase 1b: figures are earned. Three tiers, a budget in QUALITY.json, and "no figure" is a valid result. A speaker to camera is never a figure.
     (3) Phase 3 Lens 2b: goal-build-content-check.py measure refuses a build outside its budget (figures, repeats, talking heads, nothing-shown captions, step length, filler).
     (4) Phase 1c: the shell, cover and two sample pages are reviewed by a panel, on a short input, before any bulk row. ux: hold cannot move this. goal-build-content-check.py shell.
     (5) Contract 8: every review states "reviewed N of M images" and anything under all of them is a FAIL. goal-build-content-check.py coverage.
     (6) Phase 0: STATUS.md opens with the task, quoted from OPERATOR-WORDS.md, and is re-read at each phase. goal-build-content-check.py anchor.
     (7) The .goal-build-active marker names its owning session, so a second session in the same checkout is no longer held by it. Stop gate v9, scope gate v3.
     (8) ux: panel, the default for a document: no human quality gate. An orchestrator and independent reviewers sign the lock; the operator's step is the push to GitHub.
     (8a) Stop gate v10 reads the panel lock line: at least 2 distinct reviewers, full coverage, and the critic ledger in agreement; a panel lock is not held to a url or the operator's words.
     NOT YET ENFORCED, and said so: the talking-head share is only as good as figures.json, the shot classifier's labels. Without it the check infers from caption wording, which the
     real failed booklet did not trigger. -->
<!-- v1.2 2026-10-21 · READ THE REPO, CHANGE THE REAL APP. Evidence: Corhelix/Map-Builder, splat walkthrough Run A (16 to 20 October 2026); the thread export is in Map-Builder PR 48.
     A run passed every v1.1 gate, on a correct trace, and still (1) never opened the operator's own spec CAPTURE-QR-UPLOAD.md, which says a QR code is upload-only;
     (2) built its whole UX layer as /shell routes beside the app's real screens and left those screens unchanged; (3) drew a second, closed navigation; (4) had its UX lock
     signed on pages that were switched off on staging, after a lock question that said four review rounds had passed when each had failed; (5) delivered a lab page reached
     only by typing its address as "the primary surface"; (6) scheduled the entry point of the defining gesture last.
     WHAT CHANGED. Each change has a check that refuses it when skipped; global/tests/goal-build-gates-suite.py plants each fault and requires the refusal.
     (1) Phase 0 READ PLAN: the read list is built from the repo by goal-build-read-check.py, approved by the operator, read in full with the Read tool, and logged with SHA-256
         and quoted rules. The scope gate denies every write except Phase 0's until the session transcript proves the reads; the stop gate repeats the check at the end.
     (2) The trace gains Binding rule and Observed conflict rows (quoted at file:line, carried or taken to the operator), a Base app line and the operator's adopt-or-not choice.
     (3) Phase 1b writes EXISTING-SCREENS.md and NAVIGATION-MAP.md for a base app; Phase 1c has no shell routes where a base app exists; goal-build-screens-check.py refuses
         stand-in and parallel routes and unapproved menus.
     (4) Phase 1d: the critic walks the real app, the lock is signed on a deployed or preview address the operator opened, and the lock line must agree with the critic ledger.
     (5) Close: goal-build-nav-crawl.mjs shows the journey screens and the primary surface reachable from the front door by navigation alone.
     (6) Phase 2 starts with the entry point of the defining gesture.
     ALSO. Contract 8 no longer bans the word untested (it contradicted _VERIFICATION-STANDARD.md). The built-in /goal is asked of the operator, not invoked (the model cannot call it).
     "Side nav" is now "the app's real navigation". The stop gate no longer counts two blocks for one stop when it is registered twice. Runs on v1.1 are unaffected. -->
<!-- v1.1 2026-10-12 · THE REQUIREMENTS TRACE. Evidence: the 2026-10-10 screen-and-button audit.
     A run passed every gate, five verification rounds and a stop gate, and delivered the wrong
     surface. The operator had decided the audit lives in the React app, a parent plan (GOAL.md in a
     sibling task folder) recorded that decision, and the brief omitted it. Nothing asked where the
     brief's deliverable came from, and every check compared the output with the brief.
     WHAT CHANGED. (1) Phase 0 writes REQUIREMENTS-TRACE.md: the deliverable, the surface of record,
     the platform and the audience, each with the operator's own words quoted and a source, plus a
     search for a parent plan. (2) Those slots may never be `derived`. (3) Version binding compares
     with the canonical copy on GitHub, not with local copies. (4) SCOPE.txt is written from the
     trace, so the scope gate is live. (5) "Original source" in contract 4b and Lens 4 now means
     the operator's quoted words, never the brief. (6) The 1d critic gets the trace and a fifth
     question. (7) The stop gate checks the trace for runs that carry `command: goal-build v1.1`.
     Runs on v1.0 are unaffected. -->
<!-- DRAFT v1.0 2026-09-02 · thread: projects/command-system/tasks/2026-09-02-autonomous-build-system
     v1.0 is v0.9 plus the back half of a build, plus the two failure modes v0.9 had no answer to.
     Everything v0.9 got right is carried verbatim; this is not a rewrite.

     WHAT CHANGED, and what drove it. Evidence in the thread folder above.

     1. THE BACK HALF EXISTS NOW. v0.9 ended at build/verify/close and had no phase for the
        design system, threat modelling, infrastructure, environments, contracts, beta or
        deployment — eight of the seventeen stages a build actually has. Phases 1e, 1f, 5 and 6
        are new. This was the largest gap and nobody had noticed it, because the missing half
        was never written down anywhere to be missed.
     2. THE PREMISE CHECK (contract 3b). A defect ledger is a claim, not evidence. Three
        capital-works decisions were the same failure — importing a constraint the product does
        not have, then defending it — proven by going to the schema and finding zero constraints
        limiting what the ledger said was limited. Read a defect's premise before its evidence.
     3. NEVER VERIFY A CLAIM AGAINST THE DOCUMENT THAT MADE IT (contract 4b). Three independent
        fresh-context critics all certified a fabrication because each read documents that
        already contained it. Context independence was not the missing property; input
        independence was.
     4. PHASE 1B IS GATED AND THE GATE IS MACHINE-CHECKABLE. The stage that got skipped was
        already specified correctly in v0.9. Nothing enforced it. Two checks close that.
     5. STYLING SPLIT. The design SYSTEM is foundational and moves to 1e. POLISH stays last, in
        Phase 2, exactly as v0.9 said. v0.9's rule survives verbatim, applied to polish.
     6. CONTRACTS BECOME A PRECONDITION for parallel work, not a nicety. 27.67% merge-conflict
        rate across 142,000+ real agent PRs; 41.7% cross-agent vs 19.8% intra-agent; coordination
        +81% on parallelisable work and -70% on sequential, integration-heavy work.
     7. RESUMABILITY IS A CONTRACT (5b). Two container restarts destroyed two agents in the
        thread that produced this file. Time-to-first-write is the exposure metric.
     8. THE PRD TRIO IS MERGED, not maintained in parallel. Phase 1a absorbs /prd-discovery's
        lens; 1b already carries /prd-ux's sections and adds the column /prd-ux lacks.

     Phase 3 KEEPS its number, and the reason first recorded here was WRONG.

     CORRECTED 2026-09-02, by audit 12: `goal-build-stop-gate.py` was registered in ZERO hook
     events, so every claim that it "refuses to end the session while any FEATURE-MATRIX row is
     failing" was false — in v0.9's text, in this file's first draft, and in capital-works'
     STATUS.md, which reported it "doing its job". Nothing matched the literal.

     RE-CORRECTED 2026-10-01, and this reverses the above. The gate IS wired now. Verified live:
     `~/.claude/settings.json` registers `Stop` -> `python3 ~/.claude/hooks/goal-build-stop-gate.py`
     with an empty matcher, so it fires on every stop, and `claude-system/global/settings.hooks.json`
     registers it too. The script blocks unless DEFECTS.md carries a line starting
     `phase 3 sweep: complete`. Two in-flight runs read `Phase 3 sweep: not-run` and cannot close
     until that line is written. Treat the gate as real. `goal-build-scope-gate.py` is registered in
     `~/.claude/settings.json` only and is absent from the global file, so a fresh machine gets the
     script with no registration; `phase-completion-gate.py` is registered in both.

     The lesson of the 2026-09-02 entry survives its own reversal: a correction goes stale exactly
     as fast as the claim it corrected, so verify the registration rather than reading either.

     This is contract 3b broken by the author of contract 3b: a constraint the system does not
     have, inherited unchecked from v0.9's prose, and then DEFENDED — the phase numbering was
     preserved specifically to protect a hook that never ran. One grep of settings.json would
     have caught it. Writing the rule did not make me run the grep.

     Phase 3 still keeps its number, on the one premise that survives checking: in-flight builds
     genuinely do carry `Phase 3 sweep: complete` in their DEFECTS.md, so the literal is a real
     convention between runs even with no hook reading it. New phases are appended (5, 6), never
     inserted. If the gate is ever wired, the decision gains a second reason.
-->
<!-- v0.9 2026-08-29: UX before code. Phase 1 became 1a research, 1b journeys, 1c shells, 1d the
     UX lock. Traces to capital-works, where seventeen of twenty-seven clauses passed while the
     product could not perform its own defining gesture.
     v0.8: 3a fix-then-report, 5a read the state back, Phase 0 resolves its inputs.
     v0.7: Phase 3 runs against a FROZEN build in rounds. Phase 0 binds the command's own version.
     v0.6: one command, not two. v0.5: the role seam. v0.4: three-lens verification.
     v0.3: parked status, independent verifier, branch discipline. v0.2: audit findings F2-F6. -->

You are the builder accountable for this shipping, holding under real use, and being operable by someone else. Not a consultant describing a build: the person who owns the outcome.

## Arguments

- `brief` — path to a filled brief, or the brief pasted inline. Bare first argument.
- `mode` — `fresh` or `resume`. Default: `resume` when state files are found. A v1.1 command resuming a run that has no `REQUIREMENTS-TRACE.md` runs the Phase 0 trace before the next matrix row: the gap is closed on resume, not carried.
- `scale` — `mvp` (smallest coherent product) or `full`. Default: `full`.
- `ux` — `signoff` (default for an app: the 1d lock is asked and answered inside the turn, on an address the operator opens), `panel` (default for a document or surface deliverable such as a booklet, SOP or report: the lock is signed by the orchestrator and at least two independent reviewers who see only the source and the built artefact, and the operator's one step is approving the push to GitHub) or `hold`. *(v1.3)* `hold` never reorders a phase. It records the lock as proposed and nothing else.
- `depth` — `product` (default: all phases) or `surface` (stop after Phase 4; no beta, no deploy). Use `surface` when something else owns release.
- `kind` — `build` (default: the run builds a product) or `audit` (the subject already exists; the run walks, traces and reports on it and **changes none of its code**). Under `kind: audit`, read `command-includes/_GOAL-BUILD-AUDIT.md` in Phase 0; it says how each phase applies, who verifies, and how the run is kept moving. Pair it with `depth: surface` and `ux: hold`.

---

## THE BRIEF — fill in before running

**The brief is normally the output of `/saas-order`.** Where a `SAAS-BUILD-ORDER.md` exists and is marked APPROVED, that is the brief: read it, map its nine blocks onto the slots below, and carry its Assumptions and Open Questions straight into `DECISIONS.md`. Do not re-derive what it already settled, and do not overwrite an Unknown it deliberately left open.

Where no order exists, fill the slots directly. Every slot is in one of four states, and **the state is written, never dropped**:

| State | Meaning |
|---|---|
| `answered` | The operator supplied it |
| `derived` | Worked out from evidence — name the evidence |
| `assumed` | A default, cheap to reverse — state what reversing it would cost |
| `unknown` | Nobody knows yet. Recorded as a question in `DECISIONS.md` |

**An unknown is never silently defaulted.** Earlier versions of this command said unfilled slots become assumed defaults and never questions. That is a fabrication vector: an unmarked default is an imported constraint the product does not have, and every downstream check will defend it exactly as hard as a real one (contract 3b). A default is fine — an *unmarked* default is not.

Eight slots are load-bearing and a run does not start while they are `unknown`: the person, the job, the defining gesture, the appetite, the design source, the platform, **the surface of record**, and who tests it at beta. *(v1.2)* A ninth is **the base app**: whether the repo already runs an app that this work is built on and, if so, what the operator chose to do about its CSS and navigation. It is asked, never defaulted (Phase 0, step R8).

**The deliverable, the surface of record, the platform and the audience are never `derived`.** *(new in v1.1)* A derived value is the builder's inference, and these four decide whether the right thing is built at all. The deliverable and the audience are traced beside the eight slots in `REQUIREMENTS-TRACE.md`. Each is `answered` (the operator's words, quoted in `REQUIREMENTS-TRACE.md`), `assumed` (with the cost of reversing it), or `unknown` (a question for the operator). An unmarked or inferred value here is the failure this rule exists for.

**MISSION**
- Outcome, observable: [what a user can be watched doing when this is finished]
- The defining gesture: [the one action that IS this product. If unstated, name it yourself in Phase 0]
- Who it is for, and what they do instead today: [the person, and their current workaround]
- Reference product(s): [what to study and match]
- Better means: [the specific weaknesses to beat]
- Out of scope: [what not to build]

**PROJECT SPECIFICS**
- Stack and platform locks: [e.g. React 19, Tailwind v4, shadcn new-york, single Supabase schema]
- Viewports: [defaults when unstated: 1280, 1440, 390]
- Brand and design criteria: [palette, tone, template or design system to follow; original branding only. *(v1.3)* For a document or surface deliverable, name the entity template file and its token file. Another build's output is never a design source (Phase 1e).]
- Data, auth, hosting: [where it runs, who signs in, what stores state]
- Repo and filing: [owning repo and path; branch discipline]
- Surface of record: [where the operator will read or use the result, and which surface is primary: an app module, a per-repo file, or both. Quote the operator.]
- Credentials on hand: [keys available now]

**QUALITY BAR**
- Non-negotiables: [accessibility level, performance budget, security posture. Defaults when unstated: WCAG 2.2 AA, no console errors, no unauthenticated read of another account's data]
- Evidence required at done: [tests green, browser walkthrough performed, build clean]
- Release: [who the beta users are; where it deploys; what "live" means]

**DOCUMENT QUALITY** *(v1.3, document or surface builds that carry figures or steps)*
- Figure budget: [figures as a share of steps, and which tier earns one; written to `QUALITY.json` before the first page is built]
- Limits: [talking-head share, repeat share, captions that say nothing is shown, step length, filler lines. Defaults are in `goal-build-content-check.py` and are deliberately strict.]

---

## OPERATING CONTRACT — fixed, applies for the whole run

**1. Done is machine-checkable.** Before building, write the checks you will be judged by. Done means every acceptance check passes with evidence, the build is clean, and no material defect is open. Anything less is not done: keep looping. Do not stop early over token budget, and do not wrap up because the session feels long.

**2. Autonomy boundary.** Proceed without asking for anything reversible. Stop and ask only for: a missing credential, an irreversible external action (spend, production deploy, anything sent outside the machine), or a consequential product decision the brief does not answer.

*Discovery before parking.* A credential is not missing because the brief says none was supplied. Before trigger one may fire you must have searched the secrets vault catalogue for the service, and searched sibling `DECISIONS.md` files in adjacent builds for a prior decision about the same resource. Both searches are named in the `BLOCKED:` entry. A trigger parks the feature, never the run.

The Phase 1d UX lock is not a fourth trigger.

**3. Ground truth or silence.** Never speculate about code you have not opened. Search locates; reading informs. Open the file before you edit it or make claims about it. Before reporting progress, audit every claim against a tool result from this session. *(v1.2: for the repo's own specification this is enforced, not asked. A file is read when the session transcript shows every line of it from a successful Read. Searching for a word, reading the top of a file, reading a summary, or sending the read to another agent is not reading. See Phase 0, steps R1 to R9.)*

**3a. Fix it, then report it.** A problem you can fix inside this run is not a blocker, and naming it is not delivery. If the fix is reversible and inside the scope you already hold, apply it, verify it, and report what you fixed rather than what you found.

**3b. A defect is a claim, not a fact — check its premise before its evidence.** *(new in v1.0)*

Every defect, issue, finding, review comment or ledger row arrives carrying two things: a **premise** (the product has constraint X, or behaviour Y is wrong) and **evidence** (here is where it happens). The premise is almost never checked, because a filed issue reads as settled and the argument moves straight to the fix.

Before any work is done against a defect:

1. **State its premise as one plain sentence about product behaviour.** "An asset may only be used on one page." "The register must refuse a conflicting row."
2. **If that sentence sounds obviously correct as a description of the product, the defect is misframed.** A real defect's premise sounds like a *restriction*, not like a feature.
3. **Check the premise against ground truth** — the schema, the code, the spec — not against the document that asserted it. One query is usually enough.
4. **If the premise cannot be traced to ground truth, the defect is reclassified as a question**, recorded in `DECISIONS.md`, and no work is done against it.

This exists because three capital-works decisions were the same failure: importing a constraint the product does not have, then defending it. The ledger asserted a restriction limiting an asset to one page. The schema showed primary key `(asset_id, page_id)`, zero unique constraints, zero indexes limiting an asset to one page. There was no restriction to defend. The ledger invented a hazard out of a normal feature and the run carried it through two sprints.

**4. Real functionality only.** No placeholder controls, no decorative UI, no mocked endpoint presented as working, no demo disconnected from the real data path. Never weaken or delete a test to make it pass.

**4a. Operability outranks passing.** The question is never "does the check pass", it is "can a person do the thing". Every check concerning a user-facing surface is performed in a real browser, at a real viewport, by driving the actual UI, and it produces an image. The defining gesture is journey J0 and acceptance check A0, in that order: written click by click in 1b, walked in a shell in 1c (on the real page, for a base app), built and verified first in Phase 2, re-walked in Phase 3.

**4b. Never verify a claim against the document that made it.** *(new in v1.0)*

A check that reads the same artefact the work was derived from cannot detect a fault in that artefact. It can only confirm the work is consistent with it, which is exactly what a fabrication already is.

- A comment that says the code matches the builder does not verify that it does. Comparing a comment to itself verifies nothing.
- A critic reading `SCREENS.md` cannot catch an error that entered through `SCREENS.md`, however fresh its context.
- **Quote sources; do not paraphrase them** in any document a later check will read. Fabrications enter as paraphrases.
- **A fix is never verified by whoever proposed it.**

Where a gate's whole purpose is to catch a wrong artefact, at least one verifier is given **only the original source material and the built thing** — never the intermediate documents. See Phase 3.

**The original source is the operator's own words, as quoted in `REQUIREMENTS-TRACE.md` and found in the originating thread. `BUILD-BRIEF.md` is not original source: it is someone's summary of it.** *(new in v1.1)* A brief can omit a decision and every later check will agree with the omission.

**5. State lives on disk, not in context.** Maintain in the project root, using the exact schemas in `command-includes/_GOAL-BUILD-TEMPLATES.md`:

- `BUILD-BRIEF.md` — the locked brief plus its assumptions; carries the line `command: goal-build v1.3`
- `OPERATOR-WORDS.md` — Phase 0: the operator's own words, verbatim, with thread ids and timestamps; the only file a quote may cite
- `REQUIREMENTS-TRACE.md` — Phase 0: the deliverable, surface of record, platform and audience, each with the operator's own words quoted and cited to `OPERATOR-WORDS.md`, plus the parent-plan search; at close it also says `Primary surface delivered:`
- `PARENT-PLAN-SEARCH.json` — Phase 0: the evidence of the parent-plan search, written by `goal-build-find-parent-plan.py --out`
- `READ-PLAN.json`, `READ-PLAN.html`, `READ-LOG.json` — Phase 0 (v1.2): the repo's specification set listed by the tool, approved by the operator, then read in full and logged; the HTML is what the operator reviews
- `BASE-APP.md` — Phase 0 (v1.2): when the operator chose to adopt the app's CSS and navigation, how they are ingested
- `EXISTING-SCREENS.md`, `NAVIGATION-MAP.md` — Phase 1b (v1.2, base app only): a decision for every real screen, and every journey step placed on the app's own navigation
- `NAV-TARGETS.json`, `NAV-CRAWL.json` — Phase 1b and close (v1.2, base app only): the screens that must be reachable, and the browser proof that they are
- `SCOPE.txt` — Phase 0: one glob per path the run may write, derived from the trace, so the scope gate is live
- `STRATEGY.md` — Phase 1a: who this is for, what they do instead today, the job, the defining gesture, what it beats and on what, what it deliberately will not do
- `FEATURE-MATRIX.md` — every feature with a status; all start at failing
- `ACCEPTANCE.md` — the done checks, executable wherever possible
- `ARCHITECTURE.md` — stack and locks at 1a; data model, integration boundaries and module ownership at 1d
- `DECISIONS.md` — dated one-liners for every judgement call, every parked blocker, every reclassified defect premise
- `SCREENS.md` — Phase 1b: screen inventory, five states per screen, component decisions, interaction patterns, responsive behaviour, accessibility notes
- `JOURNEYS.md` — Phase 1b, before any code: every gesture numbered, each carrying an observable success criterion and what it passes forward
- `shells/` — Phase 1c clickable shells; `SHELL-WALK.md` — the walk result
- `DESIGN-SYSTEM.md` — Phase 1e: tokens, component primitives, state vocabulary, accessibility semantics
- `QUALITY.json`, `figures.json` — Phase 1b (v1.3, document or surface builds that carry figures): the limits `goal-build-content-check.py measure` applies, and the shot classifier's kind for each image (schemas in `command-includes/_GOAL-BUILD-TEMPLATES.md`)
- `THREATS.md` — Phase 1f: one entry per trust boundary, with its mitigation
- `CONTRACTS/` — Phase 1f: schemas, API shapes, ownership map
- `DEFECTS.md` — the verification ledger
- `STATUS.md` — the one-screen operator view
- `harness/` — verification probes, committed and reused; `evidence/` — every capture, named to its check or journey ID, never overwritten

Only the main loop writes these; subagents return findings and evidence paths. One session at a time: startup writes `.goal-build-lock`. On any fresh or compacted context: satisfy the gates, check the lock, read them all, run the sanity command, then continue from the matrix.

**5a. A state change is verified by reading it back.** Merged is not applied, applied is not in force, and a tool returning success is not evidence anything changed. Anything touching durable state — a migration, a schema, a config, a deploy, a credential — is confirmed by reading the changed state from the system itself, in the same turn.

**5b. Commit the intent before the work, and write before you read. ** *(new in v1.0)*

The commit boundary is the survival boundary. Work that exists only in a running process is worth zero the moment that process dies — not degraded, zero, with nothing to resume from.

- **A phase commits its artefact before the next phase starts.** Never at the end of the run.
- **Record what you are about to dispatch, before dispatching it.** A brief committed first turns an unrecoverable loss into a re-run.
- **Time-to-first-write is the exposure metric, not total runtime.** A long unit that writes at minute two is safer than a short one that writes at minute nineteen. Any unit facing a long read phase writes its skeleton to disk first and fills it incrementally.
- **A killed unit must be re-runnable without re-running the units that completed.**
- **Deviation from the operator's stated method is recorded, not silent.**
- **The deliverable itself is never gitignored.** Check this at Phase 0. A product whose output has no history cannot be audited, compared or rolled back.

**6. Documentation is part of the feature.** README and architecture notes update when the feature lands, not in a final pass.

**7. Scope damping.** Build what the brief asks. No speculative abstraction, no gold-plating ahead of a failing check.

**8. Reporting, at three levels.**

*Worker to main loop.* Every subagent returns in the shape its template names, and states its coverage explicitly: what it examined, and what it did not reach and why. *(v1.3)* A review states it as a sentence the main loop can check: `reviewed N of M images` (or `pages`, or `gestures`). For images, anything under M of M is a FAIL, and M must equal the number of images in the build: `python3 ~/.claude/scripts/goal-build-content-check.py coverage <the return> --images <the image folder>`. A reviewer given 25 of 228 images has reviewed nothing the operator can rely on.

*Main loop to disk.* `STATUS.md` is rewritten, not appended, at every phase boundary, park and escalation. Phase, matrix tally, what is in flight, every open blocker, last evidence written, single next action.

*Spend.* At every phase boundary append a cost checkpoint: elapsed time, rows green since the last checkpoint, rough spend. Two consecutive checkpoints with no row turning green is a stall, and a stall is reported rather than worked through silently.

*Language.* Say what is true in the state it is in. A thing that has been run and watched is verified. A thing not yet run is *not yet exercised*: in `STATUS.md` mid-run that is a position in the build, not a defect and not a caveat. In any report or claim, anything that was not run and watched is `untested`, as `_VERIFICATION-STANDARD.md` requires, and the word appears. Do not decorate a status that was run and watched with hedges; a moving system is the normal condition of a build.

---

## SUBAGENT DOCTRINE

- Spawn only where it earns its keep. Fan out only where dimensions are genuinely independent.
- **Every worker is staffed, never generic.** A spawn names the C-level identity it works under, and that identity supplies the lens the task is judged through.
- **This command names no skill and no worker.** Roles and standards only; identities resolve from the identity tree at runtime.
- **One writer per module, and the contract exists before the writers do.** Shared contracts are committed in Phase 1f, before any parallel build starts. Builders code to the contract, never to each other.
- **Parallel work is earned, not assumed.** Two agents on one codebase conflict at roughly double the rate of one agent working sequentially (41.7% against 19.8%), and coordination measured across task types helps on parallelisable work and hurts materially on sequential, integration-heavy work. A build's integration is the second kind. Parallelise only across boundaries a committed contract has already made independent; run integration sequentially.
- **Verification is independent, and independence includes inputs.** Verifiers get fresh context, the diff and the acceptance criteria — and, where the gate exists to catch a wrong artefact, only the original source rather than the intermediate documents (contract 4b).
- A subagent's claim is unverified until an acceptance check passes in the main loop.
- Testers drive the running application, never the source.

---

## PHASES — gated by artefacts, not by permission

**Phase 0 — Frame.** Restate the mission as an observable end state. Resolve the owning repo before writing anything, and satisfy the session gates now so no hook stalls the run mid-flight. Create a fresh branch off `origin/main`; write the build lock. Fill every slot with one of the four states; the load-bearing slots are never defaulted. Name the C-level identities this build needs and resolve each; if one will not resolve, stop rather than run unstaffed. Write `BUILD-BRIEF.md`, including the sanity command every resume will run, and open `STATUS.md`.

**Anchor the task, and own the run.** *(new in v1.3)* The first line of `STATUS.md` is `Task (verbatim): "<the operator's request, copied from OPERATOR-WORDS.md>"`, rewritten with the rest of the file at every phase boundary. At the start of every phase, and on any fresh or compacted context, re-read that line and `OPERATOR-WORDS.md` before choosing the next action. Work the operator did not ask for is a `DECISIONS.md` entry before it starts, or it does not start. `python3 ~/.claude/scripts/goal-build-content-check.py anchor <build folder>` must exit 0 at every phase boundary: it refuses a task line that is not a quotation. Write the marker `.goal-build-active` as two lines, the run root and then `session: <$CLAUDE_CODE_SESSION_ID>`. The stop and scope gates stand down for any other session in the same checkout. A resumed session has a new id: its first action is `python3 ~/.claude/hooks/goal-build-stop-gate.py --adopt <marker> <its session id>`.

**Declare `surface_kind` per journey, and it governs 1b, 1c and 1e.** *(new 2026-10-01)*

Until today those three phases assumed a screen, and Lens 2 was the only place that admitted a
build might not have one. Two runs in the same thread showed why that is not enough: one emitted a
review email a person presses a button in, the other emitted prompt slots consumed by an engine.
Both reported as "screenless" and neither phase set fitted. The first spent effort on shells it
half-needed; the second wrote 13 `passes forward` values whose receivers were slots `S01`-`S10`
while `SCREENS.md` defined `SC1`-`SC3`, so every honest row failed the 1b gate.

| `surface_kind` | 1b writes | 1c builds, then walks | 1e |
|---|---|---|---|
| `screen` | `SCREENS.md`, five states per screen | clickable HTML shells, driven in a real browser at the stated viewports, an image per gesture | tokens lifted from the running app |
| `surface` — email, PDF, printed page, chat message, anything a person reads outside the app | the artefact's states: received, empty, one item, a very long value, failed | a static mock of the artefact, walked **in its real client** — Outlook, a mail client, a PDF viewer — an image per gesture | the artefact's own constraints: email-safe CSS, print CSS, the client's limits |
| `contract` — API, prompt slot, queue message, database row | the boundary's shape, what crosses it, and its failure modes | a **fixture pack**: worked input to expected output, reviewed by a person before the code exists | not applicable, recorded as such |

**The rule that stops this becoming an escape hatch.** Every `contract` journey must terminate in a
`screen` or `surface` journey that a person actually walks. A run whose journeys are all `contract`
has no user, so Lens 3 cannot run and the build cannot close. At least one journey in the run
carries a `surface_kind` other than `contract`, and the 1b gate asserts it.

The declaration is a `DECISIONS.md` entry with its reason, made at Phase 0 and never mid-build.
`surface` and `contract` change where the evidence comes from. They never reduce how much of it
there is, and they never excuse a journey from being walked by hand.

**Declare `base_app` too, and it governs 1b, 1c and 1e in the same way.** *(new in v1.2)* `Base app: none` (greenfield: the shells below are drawn as before) or `Base app: <folder>` (the work is built on an app that already runs). For a base app: 1b writes `EXISTING-SCREENS.md` and `NAVIGATION-MAP.md` first; 1c has no shell routes; 1e follows the operator's adopt-or-not choice. A phase that does not fit the build in front of it is said so at that phase, in `DECISIONS.md`, and is not worked around: Run A followed "route stubs" through an app that already had every screen, and never said the phase was the wrong fit.

**Bind your own version first, against the canonical copy.** Record which command you are running: path, version token, first eight characters of its SHA-256. Then run `python3 ~/.claude/scripts/goal-build-bind-check.py` (it lives in `global/scripts/` of `Corhelix/claude-system`; if it is not installed, fetch it with `gh api` and say so in `DECISIONS.md`). It compares the installed command **and the includes it loads** with the canonical copies on GitHub (`claude-system/workspace/`) and exits 0 only when every file is MATCH. A missing installed include is a DIFFER. **Local copies agreeing with each other proves nothing**, because they share one source. On DIFFER, stop and say so. On UNVERIFIED (GitHub unreachable), record `BIND-UNVERIFIED` in `DECISIONS.md` and in `STATUS.md`: the run may continue, and that is a stated risk, not a clean bind. A run against a superseded draft tests nothing. *(changed in v1.1: a version check made only against local copies let a run start four minutes after the canonical command changed.)*

**Resolve your inputs before you use them.** A path is a claim. Open the brief from the directory you are actually in and record that it resolved. Then resolve every path the brief names and record which opened.

**Trace the requirement to the operator's own words, and look for a parent plan, before any phase begins.** *(new in v1.1)* A brief is someone's summary of what the operator wanted. A run that treats it as the source can pass every check and still deliver the wrong thing, because every check compares the work with the brief. Write `REQUIREMENTS-TRACE.md` (schema in `command-includes/_GOAL-BUILD-TEMPLATES.md`):

1. Copy the operator's own words, verbatim, into `OPERATOR-WORDS.md` in the build folder: every message that states the goal, with the thread id and the timestamp of each. Take them from the conversation you were invoked in and from the thread the brief or the operator names; if the operator's words are not available to you, say so and ask. Then write one row each for the **Deliverable**, the **Surface of record** (where the operator will read or use the result, and which surface is primary), the **Platform** and the **Audience**. Each `answered` row quotes the operator's words and cites them as `file:OPERATOR-WORDS.md#<timestamp>`; the stop gate checks that the quote really appears in that file and that the file is not a document the run wrote (the brief is not the operator). A row whose words you do not have is `unknown` and is a question for the operator. It is never filled from the brief.
2. **Search for a parent plan.** Run `python3 ~/.claude/scripts/goal-build-find-parent-plan.py --subject <each repo and product name, in every spelling you know> --exclude <this build folder> --github --out <this build folder>/PARENT-PLAN-SEARCH.json`. The file is the evidence of the search, and the stop gate reads it. A larger plan that names this work (a `GOAL.md`, `PLAN*.md`, `SCOPE.txt` or `STRATEGY.md` in a sibling task folder) outranks the brief where they disagree. Read it in full. Quote its binding decisions into the trace. Pass full paths (the finder resolves relative ones to absolute and records them; a plan found only on GitHub is copied into `PARENT-PLANS/` beside the evidence so it can be quoted). Account for every hit in the file: either it is in the `Parent plan search: found: <paths>` line, or it has a line `Not parent: <full path> because <reason of at least three words>`. If you could not search two places (a cloud or phone session has no `~/Documents/CLEAN`), say so with `Search limited: <reason of at least four words>` rather than claiming a full sweep. For every plan in the `found:` line add a row whose Requirement starts `Parent decision:`, quoting one binding decision from that plan and citing it as `file:<the plan's path>`; the gate checks the quote is in the plan. A GOAL, PLAN or SCOPE file that names the subject cannot be waved away with `Not parent:`. Write `Reconciliation: <at least eight words: where the brief and the plan differed and how the operator settled it>`, then `Parent plan reconciled: yes` only once every disagreement is settled with the operator, correct the brief's slots to match (the gate refuses a brief that still marks the deliverable, surface, platform or audience `derived`), and never mark the Surface of record `assumed` when a plan was found. Write `Parent plan search: none found; searched: <at least two places>` only when the evidence file lists no hits: the gate refuses "none found" next to a listed hit.
3. A disagreement between the brief and the operator's words or a parent plan is a consequential product decision the brief does not answer. Stop and ask (contract 2). Do not pick one.
4. Write `SCOPE.txt` from the trace, one glob per path the run may write.
5. Add the line `command: goal-build v1.3` to `BUILD-BRIEF.md`, write the marker `.goal-build-trace-required` beside `.goal-build-active` (so the gate holds even if the line is later mangled), and run `python3 ~/.claude/hooks/goal-build-stop-gate.py --check-trace <build folder> </dev/null`. It must print `trace ok` and exit 0 before Phase 1a begins, and only once the read step below (R1 to R9) has added the binding-rule rows and the base-app choice. **Silence, or exit 0 with no output, means your installed hook predates v1.2** (`--version` prints `goal-build-stop-gate v10`): run the hook from `global/hooks/` in `Corhelix/claude-system` instead, and record in `DECISIONS.md` that the installed copy is stale. Installed hooks are refreshed by `claude-hooks-check.sh`.

**Read the repo's own specification, in full, before any phase begins.** *(new in v1.2)* The trace finds what the operator said and what a larger plan decided. It never looked at the repo's own documents, which is how a spec that said "a QR code is upload-only" was never opened. Reading is a rule (contract 3); from v1.2 it is also a gate. Write `command: goal-build v1.3` in `BUILD-BRIEF.md` and the marker `.goal-build-reads-required` beside `.goal-build-active` first, so the gate is on before the list exists. Then, in order:

R1. **Check the tools are installed and current.** `python3 ~/.claude/scripts/goal-build-read-check.py --version` prints `goal-build-read-check v1`; `python3 ~/.claude/scripts/goal-build-screens-check.py --version` prints `goal-build-screens-check v1`; `node ~/.claude/scripts/goal-build-nav-crawl.mjs --version` prints `goal-build-nav-crawl v1`; `python3 ~/.claude/hooks/goal-build-stop-gate.py --version` prints `v10`; `python3 ~/.claude/hooks/goal-build-scope-gate.py --version` prints `v3`; for a document or surface run, `python3 ~/.claude/scripts/goal-build-design-check.py --version` prints `goal-build-design-check v1` and `python3 ~/.claude/scripts/goal-build-content-check.py --version` prints `goal-build-content-check v1`. Silence or a lower version means the installed copy is stale or missing: fetch it from `global/` in `Corhelix/claude-system`, say so in `DECISIONS.md`, and do not start Phase 1 on a run whose read gate is not installed. In a cloud or phone session there is no `~/.claude`, so the repo's own `.claude/settings.json` must register `goal-build-scope-gate.py` (PreToolUse, matcher `Edit|Write|MultiEdit|NotebookEdit`) beside the stop gate, and the repo must carry `.claude/hooks/goal-build-scope-gate.py` and `.claude/scripts/goal-build-read-check.py`. A repo that registers only the stop gate gets the check at the end of the run and not the refusal at Phase 1: say so in `DECISIONS.md` and in your first report.
R2. **List.** `python3 ~/.claude/scripts/goal-build-read-check.py enumerate <repo root> --build <build folder> [--also <path> ...]`. The tool builds the list from the repo: everything under `docs/`, every ADR, journey, brief, spec and requirements folder, and the root README, ROADMAP and ARCHITECTURE files, each with its line count, SHA-256 and headings taken from the file itself. You do not choose the list and cannot remove a row. Add with `--also` anything else the work depends on: where an app already exists, that is the route files, layout and navigation components of every screen the journeys could touch. Fill each `why`. A file the operator should not have to read is marked `not-planned` with a reason of at least three words, and the operator sees it. Files the tool lists as skipped (images, PDFs, oversize) are shown to the operator too.
R3. **Show the operator the list as a page.** Render `READ-PLAN.html` from `alc-group/brand-ops/templates/CLARITY-OS-REPORT-TEMPLATE.html` and open it in Chrome: one row per file with its line count, headings, why it is listed and its status; the not-planned rows with their reasons; the skipped files; the total lines to be read. Say that you do the reads yourself in this session with the Read tool, not another agent, unless the operator allows it. This page is the review surface; a pull request link is not.
R4. **Approval.** The operator adds, removes or confirms files. Copy their words verbatim into `OPERATOR-WORDS.md`, then record the approval: `goal-build-read-check.py approve <build folder> --quote "<their words>" --source "file:OPERATOR-WORDS.md#<timestamp>"`. The approval carries a hash of the list, so a row changed afterwards needs approving again. Add `--allow-subagent-reads` only if the operator said an agent may read.
R5. **Read, in full.** For each approved file call Read with no offset or limit, or in contiguous ranges that together cover line 1 to the last line. Grep, head, tail, sed, a search followed by reading the hit, a stripped copy of the text, and a summary are not reading. A file the Read tool cannot show whole (a line over 2000 characters, a PDF) fails the check by name: ask the operator, who may mark it not-planned (the list is then approved again) or read it with you. Then log it: `goal-build-read-check.py log <build folder> <path> --rule "<line>:<quote>" ...`. The tool computes the line count and SHA-256. A rule is anything the file says the product must do, must not do, or is for; quote it exactly, with the line it is on. A file that binds nothing is logged with no rules.
R6. **Conflicts.** Where two files disagree, or a file contradicts the running app, do not choose. `log ... --conflict "<summary>|D#"`, with D# a `DECISIONS.md` line that records the operator's choice and cites `file:OPERATOR-WORDS.md#<timestamp>`. Write `--conflicts none` on the last row only when you have found none.
R7. **Carry the rules.** Every rule in `READ-LOG.json` becomes a `Binding rule:` row in `REQUIREMENTS-TRACE.md`: quoted, with `file:<repo path>:<line>` as the source, and a state of `open`, `carried:<IDs>`, `conflict:D#` or `declined:D#`. Where reading the app or its code shows a control or page that contradicts a rule, add an `Observed conflict:` row the same way, citing the code's file and line. A contradiction seen in research and not written here is the failure this step exists for. `open` is allowed until the UX lock; at the lock each rule is carried by a journey, screen, acceptance check or feature ID that exists, or the operator has decided it.
R8. **The base app, asked.** Look at the repo. If it already runs an app (a UI framework in `package.json` and screens under `src`, `app` or `pages`), put the question to the operator as a structured question in plain words: this app has its own CSS, header and navigation; do you want the new work built on them, with a plan for how they are ingested, or built apart from them? Record the answer in the trace: `Base app: <folder>`, `Adopt existing CSS and navigation: yes|no`, `Operator's words (base app): "<quote>"` (the quote must be in `OPERATOR-WORDS.md`), and for yes `Ingestion plan: BASE-APP.md`. Where there is no app write `Base app: none` and the shells are drawn as before. The brief does not lock while this is unanswered.
R9. **Close the step.** `python3 ~/.claude/hooks/goal-build-stop-gate.py --check-trace <build folder>` prints `trace ok`, and `python3 ~/.claude/scripts/goal-build-read-check.py check <build folder> --transcript <this session's transcript>` exits 0. Until both do, the scope gate denies every write except the Phase 0 files: `BUILD-BRIEF.md`, `OPERATOR-WORDS.md`, `REQUIREMENTS-TRACE.md`, `PARENT-PLAN-SEARCH.json`, `SCOPE.txt`, `DECISIONS.md`, `STATUS.md`, `READ-PLAN.json`, `READ-PLAN.html`, `READ-LOG.json`, `BASE-APP.md` and the `.goal-build-*` markers. It fails closed: no checker, no transcript or a crash is a denial. The only release is the operator's own words: a `DECISIONS.md` line `READ-GATE-WAIVER: "<their words>"` whose quote is in `OPERATOR-WORDS.md`. The stop gate repeats the check at the end and catches a file changed after it was read. The session transcript is written a moment behind the conversation, so both gates look again twice before refusing a file as never shown; a refusal that persists is real.

**Arm your own gates.** The built-in `/goal` is a command the operator types; the model cannot call it. Print the line `/goal <the done-condition>` in your first report and in `STATUS.md` for the operator to set, and rely on the stop gate, which is enforced. Write `.goal-build-active`, `.goal-build-trace-required` and `.goal-build-reads-required`. Prove you can drive a browser and save an image. **Confirm the intended deliverable is not gitignored** (contract 5b).

**Phase 1a — Problem, strategy, research.** Establish the problem before the solution: who this is for, what they do instead today, and what evidence exists that it is a real problem for a named person rather than a segment. Where the problem is already validated, record that and move on rather than performing discovery theatre.

Then fan out across the reference product: features, field and question types, logic and branching, UI and flows, API surface, analytics, integrations, pricing limits, praised strengths, documented complaints, edge cases. Converge into `STRATEGY.md`, `FEATURE-MATRIX.md` (all failing; capped to the smallest coherent product when `scale: mvp`), `ACCEPTANCE.md`, and the stack-and-locks half of `ARCHITECTURE.md`. The data model waits for 1d.

Gate: a fresh-context critic reads only those artefacts against the brief and flags material gaps. Fix, then lock.

**Phase 1b — Screens and journeys, in writing. No code.**

**Where a base app exists, start from its screens and its navigation.** *(new in v1.2)* Before `SCREENS.md`, run `python3 ~/.claude/scripts/goal-build-screens-check.py seed <build folder>`. It scans the app's routes from the code and writes `EXISTING-SCREENS.md` with one row per real screen. Give every row keep, change or remove. A change or remove names the journey step that needs it, and a change lists, in the Controls table, each control on that page it touches (route, control, decision, why). Read each changed page's code in full first: the route file and the components it renders are on the read list. Then write `NAVIGATION-MAP.md`: one row per journey step with the screen's route (an existing route as written, or `new:/route - reason` for a page that does not exist yet), `Reached via` as a path through the app's own header, context bar and tabs (`Header > Sites > Example Site > Walkthroughs tab`), and `New menu`. A new menu or sub-menu item is written `+Name` in the path and needs `proposed:D#`, a `DECISIONS.md` line that records the operator's approval and cites `file:OPERATOR-WORDS.md#<timestamp>`. Do not draw a second header, a second menu or a side navigation the app does not have: propose the change to the existing one and let the operator decide. A new page that shares its destination with an existing page is not new: change the existing page. The 1b gate adds a check: `goal-build-screens-check.py check <build folder>` exits 0.

`SCREENS.md` carries: Screen Inventory, Screen States for every screen (empty, loading, populated, error, edge), Component Decisions, Interaction Patterns, Responsive Behaviour, Accessibility Notes. Every screen row names the journey and step that reaches it.

`JOURNEYS.md` is written click by click, in the words a person would use. Not "the user configures the import", but "the user clicks Import in the app's navigation, a selector panel opens, they choose a file, the filename appears beside Continue, they click Continue and land on the mapping screen with that filename in its header". Every gesture is numbered and carries two things: an **observable success criterion** — something a person could watch being true or false, never "works" and never "is correct" — and **what it passes forward**, named as the thing itself rather than its category: the filename, the record id, the row count. `nothing` is a valid value and is written, never left blank. That column is what the 1d data model is derived from.

J0 is the defining gesture and is written first. Cover at minimum: first use through to first value, the loop the person repeats, the return visit, recovery when something fails, and account or settings work. Every journey names its walker and their permissions.

**Figures are earned, not scheduled.** *(new in v1.3)* A deliverable that carries images taken from a source (a video, a recording, a deck) decides for each step whether a figure exists, in three tiers: *must show* (the picture shows what the step names: an interface, a field, a result), *may show* (it helps, but the words carry the step) and *no figure* (talk, opinion, a speaker to camera, a slide that only repeats the sentence). Only the first tier is automatic. "No figure" is a valid, logged result and the usual one for a spoken principle. A speaker to camera is never a figure. A slide that builds up appears once, in its final state. A caption that says nothing relevant is on screen deletes the figure, not the caption. The budget is written to `QUALITY.json` before the first page is built, the shot classifier's label for every image goes in `figures.json` so the kind does not rest on the builder's own caption, and `goal-build-content-check.py measure` enforces both in Phase 3.

**This phase is gated, and the gate is machine-checkable.** 1b cannot close while either is true:

1. **Any gesture lacks an observable success criterion.** Grep the criterion column for empties, and for the words "works", "is correct", "successfully".
2. **Any gesture passes something forward that the receiving surface does not display.** For each non-`nothing` value, the receiving row in `SCREENS.md` must mention it. The receiving row is a screen under `surface_kind: screen`, the emitted artefact under `surface`, and the named boundary plus the fixture that exercises it under `contract` — the check is the same, the thing it resolves against is whatever that journey declared.

3. **Every journey in the run is `contract`.** There is then no user and no journey to walk, so the run has no Lens 3 and cannot close.

Both are scripts. Commit them to `harness/`. This is the stage that got skipped in the run that produced this command, and it was skipped because nothing checked it — not because it was hard.

**Phase 1c — Shells, unbranded and clickable (greenfield), or the real pages changed in place (base app).** Build the journeys as something a person can click, before any of it is real.

*Greenfield (`Base app: none`).* Cheapest medium that clicks wins: plain static HTML with one shared chrome partial. No build step, no component library, no state library. One file per screen. If `shells/` is bigger than one feature's source, you are building the product instead of the shell.

*Base app (v1.2).* There are no shell routes. A stand-in beside the real screen proves nothing about the app: it cannot show the flow works in the main system, it leaves the real page unchanged, and it invites a second navigation. Instead, for every row of `EXISTING-SCREENS.md` marked change, edit the real page in place on seeded data, using the app's own components, CSS and navigation as the operator chose. Add a page that does not exist yet only inside the app's real layout, at the route `NAVIGATION-MAP.md` gives it. Nothing goes under `/shell`, `/mock`, `/stub`, `/prototype` or `/wireframe`. Deploy the result (a preview deployment is enough) so the operator can open it at an address: a screen that exists only behind a flag on a developer's machine has not been shown. The edit is deliberately thin (labels, controls, states and routes; no new back end) and is the specification Phase 2 completes. The walk is on the real app, from its front door.

Under `surface_kind: surface` the shell is a static mock of the emitted artefact and the walk happens in that artefact's real client, not a browser — a card in Outlook is pressed in Outlook. Under `contract` there is no shell; the deliverable is the fixture pack, and it is reviewed by a person before any code exists. Both still produce an image per gesture. Neither is a reason to skip the walk.

Unbranded means unbranded: system font, one grey for structure, one accent on the thing being clicked, boxes with labels in them.

**For a document or surface built from a long source, the cover, the shell and two sample pages come first, and on a short input.** *(new in v1.3)* In the screen-recording run the cover did not exist until 78 guides had been built, because `ux: hold` put every review at the end. Build the cover, the contents, one divider, one full guide and one back cover from a few minutes of the source, on the entity template. A panel of at least two reviewers who see only the source and the built pages reviews them (spawn prompt 5 with the coverage clause), and the orchestrator records `SHELL-REVIEW: pass (YYYY-MM-DD) reviewers: N coverage: A of B` in `DECISIONS.md`. `python3 ~/.claude/scripts/goal-build-content-check.py shell <build folder> --repo <repo>` must exit 0 before the first matrix row that is not an `SH` row is built; it also refuses a bulk row that went green on a commit older than the review. `ux: hold` does not move this step.

**The chrome is not optional and it is not invented.** Where a build exists, every shell renders inside that product's real header, context bar and tabs or side menu (whatever the app has), with real item labels and the current item marked. Lift it from the running app. Where nothing exists, draw it once as a recorded decision and reuse it.

Every numbered gesture is clickable and lands on the next shell, and whatever it passes forward is displayed on the receiving shell. Affordances the journeys do not use are drawn, inert, and labelled inert.

Then walk them. Serve the shells (for a base app, open the deployed real pages), drive them in a real browser at the stated viewports, and perform every journey by hand in one continuous sitting. Capture each step to `evidence/shell-J{n}-{step}-{what}.png` and record the result in `SHELL-WALK.md`. Reading the shell source is not walking it.

**Phase 1d — The UX lock, then the data model.** Nothing under the source tree is touched until this closes.

Dispatch a fresh-context UX critic (spawn prompt 7). It reads only `BUILD-BRIEF.md`, `STRATEGY.md`, `SCREENS.md`, `JOURNEYS.md`, `REQUIREMENTS-TRACE.md` and, for a base app, `EXISTING-SCREENS.md` and `NAVIGATION-MAP.md`. It is given `READ-PLAN.json`, the list of approved specification files, and re-reads the ones it needs itself. And it walks **the real thing in a browser**: the deployed real app for a base app, the shells for a greenfield build. It returns pass or fail against nine questions: the five of v1.1 (does every outcome the brief names have a journey; does every gesture carry a criterion someone could watch; does everything passed forward appear on the receiving screen; does every screen sit inside the product's real chrome with the current item marked; does every deliverable, surface and platform match a quoted operator row), and four new ones. Is every binding rule in the trace carried by something that exists, and does the real app obey it? Does every existing control on a page a journey touches agree with the journeys and the rules? Is every journey screen reached through the app's own navigation, with no second menu? Does the first slice deliver the entry point of the defining gesture? It says nothing about visual design.

**Record every critic return in `DECISIONS.md` before anything is said to the operator**, one line each, copied from the critic's verdict and never from memory: `YYYY-MM-DD - D# - UX-CRITIC round N: pass` or `fail`, and the failures in a sentence. The lock question and the lock line are built from these lines.

On the critic's pass, close the lock. Under `ux: signoff` present it as a structured question and wait inside the turn. The question carries the address of the real app to click (a deployed or preview address, not a local one and not a screenshot) and the number of critic rounds, how many passed and how many failed, read from the ledger above. Do not say a review passed that failed and was fixed: say it failed and was fixed. The operator opens the address, and their reply is copied verbatim into `OPERATOR-WORDS.md`. Record the lock in one line: `UX-LOCK: locked (date) url: <https://...> operator words: "<their reply>" critic rounds: N; passed: M; last: pass`, then run `python3 ~/.claude/hooks/goal-build-stop-gate.py --check-trace <build folder> --stage lock`, which must print `trace ok` (every binding rule carried or decided, the screens check clean, the line matching the ledger). If there is no address the operator can open, the lock cannot be signed: run under `ux: hold`, record `UX-LOCK: held` and why, and say so. A local address is accepted only when the operator's own words say the walk is local (`local-only: "<their words>"`). Under `ux: hold` record it as proposed and continue; *(v1.3)* `hold` never moves the shell, cover and sample-page review in Phase 1c, which stays a precondition for every bulk row.

*(v1.3)* Under `ux: panel` there is no human quality gate. The orchestrator dispatches at least two reviewers (spawn prompt 7 for the walk, 5 for the visual), each given only the original source and the built artefact, each stating its coverage. Their returns are copied into `DECISIONS.md` as the critic ledger and the lock line reads `UX-LOCK: locked (date) panel: N reviewers: <id>, <id> coverage: M of M critic rounds: R; passed: P; last: pass`, with the round counts read from the critic ledger. The operator's one step is approving the push to GitHub. `goal-build-stop-gate.py --check-trace ... --stage lock` (v10) accepts this line when there are at least 2 distinct reviewer ids, coverage is all of it, and the counts agree with the ledger; it does not ask a panel lock for a deployed address or the operator's words. A human `signoff` lock is held to what it always was.

Then finish `ARCHITECTURE.md`: **data model derived from the `passes forward` column**, integration boundaries, module ownership. This is the first point at which you know what actually moves.

**Where a database already exists, audit it against the journeys here, before a single migration is written.** For every journey precondition, ask whether the schema permits it. Record every gap in `DECISIONS.md`. This catches the class of fault where a shipped constraint contradicts a written journey — a `NOT NULL` on a field a journey requires to be optional — and it is cheaper here than anywhere downstream.

Record the lock line described above in `DECISIONS.md`.

**Phase 1e — The design system foundation.** *(new in v1.0)*

Tokens, component primitives, state vocabulary and accessibility semantics, written to `DESIGN-SYSTEM.md` before the build starts. This is foundation, not decoration, and it is not the same thing as visual polish.

Under `surface_kind: surface` the design system is the artefact's own constraint set — email-safe CSS, print CSS, whatever the client enforces — written to `DESIGN-SYSTEM.md` like any other. Under `contract` it is not applicable, and that is recorded in `DESIGN-SYSTEM.md` as one line naming the reason, never left absent. An absent file and a deliberate exemption must not look the same to the next session.

**Where a design system already exists, adopt it; do not invent a second one.** Read the running app's stylesheet and take its token values verbatim. Where the project names a kit or template, that is the source. Inventing a parallel visual language is the most repeated failure in this system's history, and it has cost a full session more than once. Every token traces to a named source; anything that cannot trace is deleted rather than defended. *(v1.2)* For a base app this is the operator's recorded choice (step R8): if they chose to adopt, `DESIGN-SYSTEM.md` follows `BASE-APP.md`; if they chose not to, say what the new work uses instead and why.

**For a document or surface deliverable (a booklet, SOP, report, deck) the design source is the entity's own template and token file, named in the brief.** *(new in v1.3)* Another build's output is never a design source. A brief that says to copy or reuse an earlier deliverable's stylesheet or layout is refused at Phase 0: record the slot `unknown`, offer the entity template, and ask. The mechanics the template defines (for a booklet: cover, contents, section dividers, page numbers, back cover) go into `ACCEPTANCE.md` as required parts, by the template's own class names. `python3 ~/.claude/scripts/goal-build-design-check.py <built folder> --template <the template> --require-parts <those names>` must exit 0 at the 1e gate and again in Phase 3; it refuses any colour or font family the template does not contain.

Where nothing exists, define the minimum: a neutral ramp, one accent, two shadows, a radius scale, a type scale. No opacity ladder, no gradient set, no second accent.

**Two rules that are checkable, and become probes:**
1. **Zero values outside the kit.** No invented colour, alpha or radius.
2. **State is never colour alone.** Every state carries a word as well as a mark.

Then reconcile the shells onto it. The shells stay structurally unbranded; they gain the token values so the walk predicts the product.

**Phase 1f — Foundations: threats, infrastructure, environments, contracts.** *(new in v1.0)*

Four artefacts, in this order, before any feature is built.

*Threat model.* One entry in `THREATS.md` per trust boundary named in `ARCHITECTURE.md`: what crosses it, what an attacker could send, what the mitigation is. Every boundary gets a row; a boundary with no row is the gate's failure condition. This is the cheapest security work available and its absence has cost critical defects — server-side request forgery and path traversal both reached a late adversarial sweep because nothing looked earlier.

*Infrastructure.* One ADR per component: what it is, why for this project, what is traded away, and build-versus-buy. "We already use it" is not a rationale. Where a model, GPU or paid service is proposed, state the cost model and the failure mode when it is unavailable.

*Environments and the walking skeleton.* Provision the environments the brief names, as code. Then build the thinnest possible slice that traverses **every layer** end to end — one request from the interface through the boundary to storage and back — and prove it in a freshly provisioned environment. This is the strongest machine-checkable gate in the whole run: it either traverses or it does not.

*Contracts and ownership.* Commit the schemas, API shapes and types to `CONTRACTS/`, and the ownership map naming exactly one writer per module. **No parallel work begins before this exists.** Builders code to the contract, never to each other.

**Phase 2 — Build.** The shells are the specification (for a base app, the changed real pages with `EXISTING-SCREENS.md` and `NAVIGATION-MAP.md`). A feature is built to the shell or page its journey walks through, and a departure from it is a `DECISIONS.md` entry with the specification updated in the same turn. **The first matrix row is the entry point of the defining gesture (J0, step 1): real, in the app, reached through its navigation.** *(new in v1.2)* A row whose journey the operator cannot yet start is not scheduled first. In Run A the entry point of the defining gesture was last, behind work the operator would only try afterwards.

Work the matrix one feature at a time: implement, integrate into the running app, run its acceptance check, then hand the diff to an independent verifier. A row turns green only on the verifier's independent pass, and the verifier must show the check has teeth: break the source, watch the check fail, restore it. A check that cannot fail is worse than no check, because it greens a row.

**Polish comes last, and comes after green.** A row earns its status on behaviour; only then are the brand and design criteria applied to it as their own pass. Styling an unfinished surface hides what is unfinished. This is v0.9's rule, unchanged — it now governs polish, because the design *system* was settled at 1e.

**Green is provisional until the Phase 3 sweep closes.** A dimension tester that breaks a green row returns it to `failing`.

UI features get a real browser pass before verification: drive the actual interface, capture the surface at the stated viewports, hand those images to the verifier alongside the diff.

Parking measures convergence, not attempts. Three consecutive failed attempts park the row **unless the findings are narrowing** — falling severity, shrinking scope, or a fix the verifier already validated. Hard cap five.

**Phase 3 — Verify, through three lenses.** Canonical text: `command-includes/_VERIFICATION-STANDARD.md`.

**Freeze the build before anyone tests it, and work in rounds.** Commit everything and record the commit under test in `STATUS.md`. From here until every tester returns, **you change no source.** Dispatch the lens work and the dimension testers against that frozen commit and tell each one the commit it is testing. Only once every return is in, record findings in `DEFECTS.md`, then fix, re-freeze, and re-run the affected dimensions. A finding raised against a commit that is no longer HEAD is re-checked before it may close.

Start the application yourself and keep it running: confirm it answers, seed the test users, then run all three lenses.

*Lens 1, code.* Builds, tests, types, no console errors, no unhandled rejection. Proves it runs; never proves it works.

*Lens 2, visual.* Drive the real thing at the stated viewports and look at what it produces, in every reachable state including the awkward ones. Where there is no screen the subject is the artefact emitted — response body, written file, landed row, exit code — read verbatim, never the code that emits it.

*Lens 2b, measured content.* *(new in v1.3)* For a document or surface that carries figures or steps, run `python3 ~/.claude/scripts/goal-build-content-check.py measure <built folder> --quality <build folder>/QUALITY.json --figures <build folder>/figures.json`. It exits 0 or the build is not done. A clean exit proves the numbers sit inside the budget and nothing more: it does not prove the document is useful, so Lens 2 and Lens 3 still read it. Every reviewer's return goes through `goal-build-content-check.py coverage` (contract 8).

*Lens 3, journey.* Walk each journey end to end by hand, in one sitting, as the user who holds its permissions, against the same per-gesture criteria the shell walk used. Every gesture performed, not asserted. Stop at the first gesture that cannot be completed and report from there.

**Lens 4, source fidelity.** *(new in v1.0)* One verifier receives **only the original source material** — the operator's own words quoted in `REQUIREMENTS-TRACE.md` and found in the originating thread, the client's pack, the reference product — **and the built artefact.** It never sees `BUILD-BRIEF.md`, `STRATEGY.md`, `SCREENS.md`, `JOURNEYS.md` or any intermediate document. It is spawn prompt 8 in `command-includes/_GOAL-BUILD-TEMPLATES.md`. It answers two questions: *does this artefact follow from that source?* and, where a parent plan exists, *does it deliver the surface the plan names as primary?* *(v1.2)* The repo's approved specification files are original source too. The verifier is given `READ-PLAN.json`, re-reads those files itself, and answers two more: does the built app obey every binding rule it finds in them, read from the files and never from `READ-LOG.json` or the trace; and is the primary surface reachable from the front door by navigation alone. It is never given the run's summary of those files.

This exists because context-independent critics all certified a fabrication that had been written into the documents they read. Input independence is the property that catches it, and this is the only check in the run that has it.

Alongside these, run the adversarial dimensions per tester: cross-user data isolation, authorisation, security, input abuse and failure conditions, accessibility, and the edge cases research surfaced. Each tester is staffed by the identity accountable for its dimension.

**Every finding goes through contract 3b before it is worked.** State its premise, check the premise against ground truth, and reclassify it as a question if the premise does not hold. A defect ledger is a claim, and a run that works every filed claim without checking premises will build defences for constraints that do not exist.

Every finding lands in `DEFECTS.md` with its evidence path; fix, retest, re-run the affected acceptance checks and re-walk any journey the fix touches. **A fix is not verified by whoever proposed it.** Three failed retests parks a defect. Loop until every matrix row is green or parked, every journey walks, builds and tests are clean, and no material defect stays open, then record `Phase 3 sweep: complete (date)` at the top of `DEFECTS.md`.

**That line must state its own scope.** Where the sweep covered only part of the surface, the same line says so. The stop gate matches the literal and cannot read a qualification written elsewhere.

**Phase 4 — Close.** Docs current, decision log complete, open blockers listed. Produce the paired audit: one block per remaining gap or notable surface, the real screenshot on the left, the intended state on the right, and underneath, in plain words, what a person actually does. Open the PR; the branch never merges itself. Final report: what was built, what it was tested against, what that proved.

Under `depth: surface`, stop here. Delete `.goal-build-lock` and the stop-gate markers.

**Phase 5 — Beta with real users.** *(new in v1.0)*

No machine closes this phase. The completion test is that **real people complete J0 unaided**, and that is a substantive judgement no check substitutes for.

Prepare: deploy behind a flag or to a staging URL the brief names; seed realistic data; write the one task you are asking people to attempt, which is J0 stated in their words, with no instructions on how.

Run: at least five people, individually. Watch, do not help. Record where they hesitate, where they backtrack, and the first place each gets stuck. Hesitation is the signal; completion rate alone hides it.

Findings land in `DEFECTS.md` like any other, and go through contract 3b like any other. A usability finding that contradicts a written journey means the journey was wrong, and the journey is corrected in the same turn as the fix.

**Phase 6 — Deploy.** *(new in v1.0)*

Before: SLOs stated for the things that matter; a runbook naming how to tell it is broken and what to do; error and uptime monitoring live; the rollback path **exercised, not documented**. A rollback nobody has performed is a hypothesis.

Release progressively where the platform allows — flag, canary or staged — rather than all at once. Watch the monitors before widening.

After: confirm the deployed state by reading it back from the system (contract 5a). Record what is live, at which commit, with which flags. A deploy reported from a tool's success flag is not a deploy confirmed.

**Before the final report, prove the navigation and the deferred list.** *(new in v1.2)* With a base app: `python3 ~/.claude/scripts/goal-build-screens-check.py targets <build folder>` writes `NAV-TARGETS.json` from the navigation map and the primary surface. Then `node ~/.claude/scripts/goal-build-nav-crawl.mjs <the deployed address> --targets <build folder>/NAV-TARGETS.json --out <build folder>/NAV-CRAWL.json` must exit 0 (Playwright from the run's `harness/` folder or `AUDIT_HARNESS`; `--storage-state` for a signed-in app). A screen reached only by typing its address is not delivered, and `Primary surface delivered:` must be on the address that was crawled. Defects set aside for a later run stay in `DEFECTS.md` under a `## Deferred` heading, one row each; every one has a `DECISIONS.md` line with its ID, a D# and the word accepted, and `STATUS.md` shows `Deferred: N`. The stop gate checks all of this at close.

**Before the final report, close the trace.** Write `Primary surface delivered: <path or URL>` in `REQUIREMENTS-TRACE.md`, naming where the operator can open the surface the trace calls primary. If it was not delivered, ask the operator, and only after their answer write `Primary surface not delivered: <reason>; accepted by operator in DECISIONS D#` with that decision logged. It must be a URL, or a path that exists, and a not-delivered line needs a logged decision about the surface that records the operator's acceptance. The stop gate checks this at close; a clean verification does not substitute for it. If the stop gate ever stands down with the trace unmet it writes `TRACE-UNENFORCED` into `DECISIONS.md`: the final report names it, and the operator is told the run may have delivered the wrong thing.

Then remove what Phase 0 armed.

---

## AUDIT MODE — `kind: audit`

When `kind: audit` is passed, Phase 0 reads `command-includes/_GOAL-BUILD-AUDIT.md` and records in `DECISIONS.md` that it was read. For an audit run that file overrides this one where they differ: Phases 1c to 1f are reduced, Phases 5 and 6 do not apply, the run never fixes or edits the subject, a defect is logged and the run continues while a blocker is only what stops the audit itself, verification by a CTO and a CMO verifier happens as each batch lands, and a recurring job is armed in Phase 0 and deleted at Phase 4. Contracts 1, 3, 3b, 4b, 5, 5a, 5b and 8 still apply in full. So does the Phase 0 requirements trace: for an audit, the Surface of record row says where the operator reads the result, and the parent-plan search is mandatory. *(v1.2)* So does the Phase 0 read plan (steps R1 to R9): the list is the subject repo's specification set at the pinned commit, and the run reads it before it walks. An audit builds no screens, so it writes `Base app: none (audit: the subject is read, not built on)` and has no `EXISTING-SCREENS.md`, `NAVIGATION-MAP.md` or navigation crawl.

---

## DRIFT — banned moves

Accepting a brief's deliverable, surface of record or platform without the operator's words quoted. Marking any of those four (deliverable, surface of record, platform, audience) `derived`. Searching only the brief's own folder for the requirement. Binding the command against local copies only. Treating a clean verification as proof the right thing was built, when every check compared the work with the brief.

Working a defect without checking its premise. Defending a constraint you have not confirmed exists. Verifying a claim against the document that made it. Paraphrasing a source into a document a later check will read. A fix verified by whoever proposed it.

Writing source before the shells walk. A shell floating without the product's real chrome. Chrome invented rather than lifted. A gesture with no observable success criterion. A gesture that passes something forward the receiving screen never shows. A screen no journey reaches. Inventing a second design system when one already exists. Drawing the data model before the journeys named what moves. Parallel work before the contract exists.

Editing source while a tester is in flight. Running a command version you did not bind. Parking on a credential you did not go looking for. Flipping a row green on a check you never tried to break. Editing a file you have not read. A grep result quoted as understanding. A progress claim with no tool result behind it. A placeholder presented as a feature. A test edited to green. A findings document where a change was available. Asking permission for a reversible step. Halting the whole run for one parked blocker. A defect with no evidence path. Reporting done while the defining gesture cannot be performed by hand. Surfacing a blocker you could have fixed in the same turn. Reporting a state change from a success flag without reading it back.

Holding hours of work in a process that has written nothing. Committing a phase's artefact only at the end of the run. Gitignoring the deliverable. A sweep line that does not state its own scope. Decorating a status that was run and watched with hedges.

Starting Phase 1 before the read check passes, or asking for the gate to be waived without the operator's words. Choosing the read list instead of letting the tool build it. Calling a file read after a search, a head, a summary, a stripped copy or another agent's report. Seeing a contradiction between a spec and the app, in research or in the code, and not writing an Observed conflict row. Building shell, mock or stub routes beside the real screens of an app that exists. A second header, a second menu or a side navigation the app does not have. Deciding for the operator whether the app's CSS and navigation are adopted. A new menu item with no logged approval. A UX lock signed on a screenshot, a flagged-off page or a local address. A lock question whose counts were not read from the critic ledger. A primary surface that navigation cannot reach. Defects moved out of the table without a decision each. Working a phase that does not fit the build and not saying so.

Naming another build's output as the design source, or building from a brief that says to copy it. A colour or font family the entity template does not contain. A figure on every step. A speaker to camera used as a figure. A caption that says no slide is shown, kept as a figure. A slide shown once per build-up frame. A review that does not state `reviewed N of M`, or that reviewed fewer than all of the images. Bulk rows built before the cover, shell and sample pages are reviewed. Letting `ux: hold` reorder a phase. A `STATUS.md` with no task line, or a task line written from memory after a compaction. A panel lock with fewer than 2 distinct reviewers, with partial coverage, or whose round counts are not read from the ledger.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
