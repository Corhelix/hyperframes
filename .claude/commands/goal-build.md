# /goal-build — Hands-Off Build to Completion

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

     CORRECTED 2026-09-02, same day, by audit 12. `goal-build-stop-gate.py` IS NOT WIRED TO
     ANYTHING. It exists as code in three places — this repo's `hooks/`, the archived global
     config at `claude-system/global/hooks/`, and the 2026-08-20 task folder — and is registered
     in ZERO hook events. This repo's `.claude/settings.json` declares no `Stop` event at all.
     The machine's global config does declare one, running five other scripts; the goal-build
     gate is not among them. `phase-completion-gate.py` is in the same state.

     So every claim that the stop gate "refuses to end the session while any FEATURE-MATRIX row
     is failing" is false — in v0.9's text, in this file's first draft, and in capital-works'
     STATUS.md, which reported it "doing its job". Nothing matched the literal. Nothing stopped
     anything.

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
- `mode` — `fresh` or `resume`. Default: `resume` when state files are found.
- `scale` — `mvp` (smallest coherent product) or `full`. Default: `full`.
- `ux` — `signoff` (default: the 1d lock is asked and answered inside the turn) or `hold`.
- `depth` — `product` (default: all phases) or `surface` (stop after Phase 4; no beta, no deploy). Use `surface` when something else owns release.

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

Seven slots are load-bearing and a run does not start while they are `unknown`: the person, the job, the defining gesture, the appetite, the design source, the platform, and who tests it at beta.

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
- Brand and design criteria: [palette, tone, template or design system to follow; original branding only]
- Data, auth, hosting: [where it runs, who signs in, what stores state]
- Repo and filing: [owning repo and path; branch discipline]
- Credentials on hand: [keys available now]

**QUALITY BAR**
- Non-negotiables: [accessibility level, performance budget, security posture. Defaults when unstated: WCAG 2.2 AA, no console errors, no unauthenticated read of another account's data]
- Evidence required at done: [tests green, browser walkthrough performed, build clean]
- Release: [who the beta users are; where it deploys; what "live" means]

---

## OPERATING CONTRACT — fixed, applies for the whole run

**1. Done is machine-checkable.** Before building, write the checks you will be judged by. Done means every acceptance check passes with evidence, the build is clean, and no material defect is open. Anything less is not done: keep looping. Do not stop early over token budget, and do not wrap up because the session feels long.

**2. Autonomy boundary.** Proceed without asking for anything reversible. Stop and ask only for: a missing credential, an irreversible external action (spend, production deploy, anything sent outside the machine), or a consequential product decision the brief does not answer.

*Discovery before parking.* A credential is not missing because the brief says none was supplied. Before trigger one may fire you must have searched the secrets vault catalogue for the service, and searched sibling `DECISIONS.md` files in adjacent builds for a prior decision about the same resource. Both searches are named in the `BLOCKED:` entry. A trigger parks the feature, never the run.

The Phase 1d UX lock is not a fourth trigger.

**3. Ground truth or silence.** Never speculate about code you have not opened. Search locates; reading informs. Open the file before you edit it or make claims about it. Before reporting progress, audit every claim against a tool result from this session.

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

**4a. Operability outranks passing.** The question is never "does the check pass", it is "can a person do the thing". Every check concerning a user-facing surface is performed in a real browser, at a real viewport, by driving the actual UI, and it produces an image. The defining gesture is journey J0 and acceptance check A0, in that order: written click by click in 1b, walked in a shell in 1c, built and verified first in Phase 2, re-walked in Phase 3.

**4b. Never verify a claim against the document that made it.** *(new in v1.0)*

A check that reads the same artefact the work was derived from cannot detect a fault in that artefact. It can only confirm the work is consistent with it, which is exactly what a fabrication already is.

- A comment that says the code matches the builder does not verify that it does. Comparing a comment to itself verifies nothing.
- A critic reading `SCREENS.md` cannot catch an error that entered through `SCREENS.md`, however fresh its context.
- **Quote sources; do not paraphrase them** in any document a later check will read. Fabrications enter as paraphrases.
- **A fix is never verified by whoever proposed it.**

Where a gate's whole purpose is to catch a wrong artefact, at least one verifier is given **only the original source material and the built thing** — never the intermediate documents. See Phase 3.

**5. State lives on disk, not in context.** Maintain in the project root, using the exact schemas in `command-includes/_GOAL-BUILD-TEMPLATES.md`:

- `BUILD-BRIEF.md` — the locked brief plus assumed defaults
- `STRATEGY.md` — Phase 1a: who this is for, what they do instead today, the job, the defining gesture, what it beats and on what, what it deliberately will not do
- `FEATURE-MATRIX.md` — every feature with a status; all start at failing
- `ACCEPTANCE.md` — the done checks, executable wherever possible
- `ARCHITECTURE.md` — stack and locks at 1a; data model, integration boundaries and module ownership at 1d
- `DECISIONS.md` — dated one-liners for every judgement call, every parked blocker, every reclassified defect premise
- `SCREENS.md` — Phase 1b: screen inventory, five states per screen, component decisions, interaction patterns, responsive behaviour, accessibility notes
- `JOURNEYS.md` — Phase 1b, before any code: every gesture numbered, each carrying an observable success criterion and what it passes forward
- `shells/` — Phase 1c clickable shells; `SHELL-WALK.md` — the walk result
- `DESIGN-SYSTEM.md` — Phase 1e: tokens, component primitives, state vocabulary, accessibility semantics
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

*Worker to main loop.* Every subagent returns in the shape its template names, and states its coverage explicitly: what it examined, and what it did not reach and why.

*Main loop to disk.* `STATUS.md` is rewritten, not appended, at every phase boundary, park and escalation. Phase, matrix tally, what is in flight, every open blocker, last evidence written, single next action.

*Spend.* At every phase boundary append a cost checkpoint: elapsed time, rows green since the last checkpoint, rough spend. Two consecutive checkpoints with no row turning green is a stall, and a stall is reported rather than worked through silently.

*Language.* Say what is true in the state it is in. A thing that has been run and watched is verified. A thing not yet exercised is *not yet exercised* — that is a position in the build, not a defect and not a caveat. Do not decorate a status with hedges; a moving system is the normal condition of a build.

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

**Phase 0 — Frame.** Restate the mission as an observable end state. Resolve the owning repo before writing anything, and satisfy the session gates now so no hook stalls the run mid-flight. Create a fresh branch off `origin/main`; write the build lock. Fill unfilled slots with assumed defaults. Name the C-level identities this build needs and resolve each; if one will not resolve, stop rather than run unstaffed. Write `BUILD-BRIEF.md`, including the sanity command every resume will run, and open `STATUS.md`.

**Bind your own version first.** Record which command you are running: path, version token, first eight characters of its SHA-256. If an installed canonical copy exists and differs, stop and say so. A run against a superseded draft tests nothing.

**Resolve your inputs before you use them.** A path is a claim. Open the brief from the directory you are actually in and record that it resolved. Then resolve every path the brief names and record which opened.

**Arm your own gates.** Invoke the built-in `/goal` with the done-condition. Write `.goal-build-active`. Prove you can drive a browser and save an image. **Confirm the intended deliverable is not gitignored** (contract 5b).

**Phase 1a — Problem, strategy, research.** Establish the problem before the solution: who this is for, what they do instead today, and what evidence exists that it is a real problem for a named person rather than a segment. Where the problem is already validated, record that and move on rather than performing discovery theatre.

Then fan out across the reference product: features, field and question types, logic and branching, UI and flows, API surface, analytics, integrations, pricing limits, praised strengths, documented complaints, edge cases. Converge into `STRATEGY.md`, `FEATURE-MATRIX.md` (all failing; capped to the smallest coherent product when `scale: mvp`), `ACCEPTANCE.md`, and the stack-and-locks half of `ARCHITECTURE.md`. The data model waits for 1d.

Gate: a fresh-context critic reads only those artefacts against the brief and flags material gaps. Fix, then lock.

**Phase 1b — Screens and journeys, in writing. No code.**

`SCREENS.md` carries: Screen Inventory, Screen States for every screen (empty, loading, populated, error, edge), Component Decisions, Interaction Patterns, Responsive Behaviour, Accessibility Notes. Every screen row names the journey and step that reaches it.

`JOURNEYS.md` is written click by click, in the words a person would use. Not "the user configures the import", but "the user clicks Import in the side nav, a selector panel opens, they choose a file, the filename appears beside Continue, they click Continue and land on the mapping screen with that filename in its header". Every gesture is numbered and carries two things: an **observable success criterion** — something a person could watch being true or false, never "works" and never "is correct" — and **what it passes forward**, named as the thing itself rather than its category: the filename, the record id, the row count. `nothing` is a valid value and is written, never left blank. That column is what the 1d data model is derived from.

J0 is the defining gesture and is written first. Cover at minimum: first use through to first value, the loop the person repeats, the return visit, recovery when something fails, and account or settings work. Every journey names its walker and their permissions.

**This phase is gated, and the gate is machine-checkable.** 1b cannot close while either is true:

1. **Any gesture lacks an observable success criterion.** Grep the criterion column for empties, and for the words "works", "is correct", "successfully".
2. **Any gesture passes something forward that the receiving screen does not display.** For each non-`nothing` value, the receiving screen's row in `SCREENS.md` must mention it.

Both are scripts. Commit them to `harness/`. This is the stage that got skipped in the run that produced this command, and it was skipped because nothing checked it — not because it was hard.

**Phase 1c — Shells, unbranded and clickable.** Build the journeys as something a person can click, before any of it is real. Cheapest medium that clicks wins: plain static HTML with one shared chrome partial, unless the app already runs a framework, in which case route stubs inside its real layout. No build step, no component library, no state library. One file per screen. If `shells/` is bigger than one feature's source, you are building the product instead of the shell.

Unbranded means unbranded: system font, one grey for structure, one accent on the thing being clicked, boxes with labels in them.

**The chrome is not optional and it is not invented.** Where a build exists, every shell renders inside that product's real header and side nav, with real item labels and the current item marked. Lift it from the running app. Where nothing exists, draw it once as a recorded decision and reuse it.

Every numbered gesture is clickable and lands on the next shell, and whatever it passes forward is displayed on the receiving shell. Affordances the journeys do not use are drawn, inert, and labelled inert.

Then walk them. Serve the shells, drive them in a real browser at the stated viewports, and perform every journey by hand in one continuous sitting. Capture each step to `evidence/shell-J{n}-{step}-{what}.png` and record the result in `SHELL-WALK.md`. Reading the shell source is not walking it.

**Phase 1d — The UX lock, then the data model.** Nothing under the source tree is touched until this closes.

Dispatch a fresh-context UX critic. It reads only `BUILD-BRIEF.md`, `STRATEGY.md`, `SCREENS.md` and `JOURNEYS.md`, walks the shells in a browser itself, and returns pass or fail against four questions: does every outcome the brief names have a journey that reaches it; does every gesture carry a criterion someone could watch being true or false; does everything a gesture passes forward appear on the receiving screen; does every shell sit inside the product's real chrome with the current item marked. It says nothing about visual design — the shells are deliberately unbranded.

On the critic's pass, close the lock. Under `ux: signoff` present it as a structured question and wait inside the turn. Under `ux: hold` record it as proposed and continue.

Then finish `ARCHITECTURE.md`: **data model derived from the `passes forward` column**, integration boundaries, module ownership. This is the first point at which you know what actually moves.

**Where a database already exists, audit it against the journeys here, before a single migration is written.** For every journey precondition, ask whether the schema permits it. Record every gap in `DECISIONS.md`. This catches the class of fault where a shipped constraint contradicts a written journey — a `NOT NULL` on a field a journey requires to be optional — and it is cheaper here than anywhere downstream.

Record `UX-LOCK: locked (date)` in `DECISIONS.md`.

**Phase 1e — The design system foundation.** *(new in v1.0)*

Tokens, component primitives, state vocabulary and accessibility semantics, written to `DESIGN-SYSTEM.md` before the build starts. This is foundation, not decoration, and it is not the same thing as visual polish.

**Where a design system already exists, adopt it; do not invent a second one.** Read the running app's stylesheet and take its token values verbatim. Where the project names a kit or template, that is the source. Inventing a parallel visual language is the most repeated failure in this system's history, and it has cost a full session more than once. Every token traces to a named source; anything that cannot trace is deleted rather than defended.

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

**Phase 2 — Build.** The shells are the specification. A feature is built to the shell its journey walks through, and a departure from the shell is a `DECISIONS.md` entry with the shell updated in the same turn.

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

*Lens 3, journey.* Walk each journey end to end by hand, in one sitting, as the user who holds its permissions, against the same per-gesture criteria the shell walk used. Every gesture performed, not asserted. Stop at the first gesture that cannot be completed and report from there.

**Lens 4, source fidelity.** *(new in v1.0)* One verifier receives **only the original source material** — the brief, the client's pack, the reference product — **and the built artefact.** It never sees `STRATEGY.md`, `SCREENS.md`, `JOURNEYS.md` or any intermediate document. It answers one question: *does this artefact follow from that source?*

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

Then remove what Phase 0 armed.

---

## DRIFT — banned moves

Working a defect without checking its premise. Defending a constraint you have not confirmed exists. Verifying a claim against the document that made it. Paraphrasing a source into a document a later check will read. A fix verified by whoever proposed it.

Writing source before the shells walk. A shell floating without the product's real chrome. Chrome invented rather than lifted. A gesture with no observable success criterion. A gesture that passes something forward the receiving screen never shows. A screen no journey reaches. Inventing a second design system when one already exists. Drawing the data model before the journeys named what moves. Parallel work before the contract exists.

Editing source while a tester is in flight. Running a command version you did not bind. Parking on a credential you did not go looking for. Flipping a row green on a check you never tried to break. Editing a file you have not read. A grep result quoted as understanding. A progress claim with no tool result behind it. A placeholder presented as a feature. A test edited to green. A findings document where a change was available. Asking permission for a reversible step. Halting the whole run for one parked blocker. A defect with no evidence path. Reporting done while the defining gesture cannot be performed by hand. Surfacing a blocker you could have fixed in the same turn. Reporting a state change from a success flag without reading it back.

Holding hours of work in a process that has written nothing. Committing a phase's artefact only at the end of the run. Gitignoring the deliverable. A sweep line that does not state its own scope. Hedging a status with "untested" when the honest statement is that the thing has not been exercised yet, which is a position in a build and not a fault.
