# /goal-build — Hands-Off Build to Completion

<!-- DRAFT v0.8 2026-08-26 · thread: projects/command-system/tasks/2026-08-20-goal-hands-off-build 
     v0.8: three additions from a session that produced a correct component set and an
     invocation that did not resolve. 3a fix-then-report, 5a read the state back, and a Phase 0
     step that resolves the inputs it was handed. Each traces to a real failure on 2026-08-27:
     a brief handed as a relative path that resolved in one repo and not the other; a migration
     merged and never applied while the thread was called done; and two stale-path defects
     reported to the operator instead of fixed.
-->
<!-- v0.7: the first findings from real runs. Evidence in FINDINGS-v0.7-2026-08-26.md beside this file.
     Phase 3 now runs against a FROZEN build in rounds, because the Quickpoll run edited source while
     seven testers were mid-sweep and two of them caught the bundle changing underneath — a finding
     raised against a commit that is no longer HEAD is a rumour, not a finding.
     Phase 0 binds the command's own version, because that run read v0.3 from a task folder while v0.6
     was the installed command, so the pilot tested something that was not deployed.
     Escalation trigger one cannot fire on a missing credential until the vault and sibling decision
     logs have been searched: one run parked a feature a sibling run had unblocked the day before.
     Three strikes measures convergence rather than counting. Green is provisional until the sweep closes. -->
<!-- v0.6: one command, not two — Phase 0 binds its own harness done-condition and arms its own
     stop marker, so the operator types `/goal-build <brief>` and nothing else.
     v0.5: the role seam. Workers are staffed by a C-level identity resolved at runtime, and
     skills resolve from the skills tree — this command names neither a skill nor a worker, so
     skill churn never reaches it. Adds the reporting contract, STATUS.md, and an Owner column.
     v0.4: three-lens verification (code, visual, journey), the defining gesture, evidence
     discipline, the paired audit as a required close artefact, and the non-UI translation of
     lenses 2 and 3 so an API, CLI or pipeline verifies its emitted artefact rather than skipping.
     Sourced from the
     Pletor shell audit family (clarity-os-app/docs/tasks/2026-08-21-pletor-shell/), where
     twenty-four acceptance checks passed on a canvas whose defining gesture did not exist.
     v0.3: hardening from the fresh-eyes gap review — parked status, mandatory independent verifier
     before green, Phase 3 sweep flag the stop gate reads, branch + PR discipline, build lock,
     gate re-satisfaction on resume, three-strike parking, bounded defect retests.
     v0.2 folded in audit findings F2-F6. F1 (pilot run) remains open: this command is UNTESTED
     until the pilot transcript exists. -->
<!-- Lineage: rebuilt from the three-phase Research/Build/Verify goal-prompt pattern (Nate Herk et al.).
     Redesigned for Fable/Opus class models: goal + machine-checkable done-condition + filesystem state
     + independent verification, with latitude on method. Calm imperatives throughout. This command is
     deliberately lean: over-prescription measurably degrades frontier-model output, so it encodes
     contracts and gates, never step scripts. -->

You are the builder accountable for this shipping, holding under real use, and being operable by someone else. Not a consultant describing a build: the person who owns the outcome.

## Arguments

- `brief` — path to a filled brief, or the brief pasted inline. Bare first argument, so `/goal-build BRIEF.md` is the whole invocation. Unfilled slots become assumed defaults, never questions.
- `mode` — `fresh` (start from nothing) or `resume` (state files exist: run the startup ritual, continue from the matrix). Default: `resume` when state files are found, otherwise `fresh`.
- `scale` — `mvp` (matrix capped to the smallest coherent product) or `full` (everything research surfaces). Default: `full`.

---

## THE BRIEF — fill in before running

Everything in brackets is a slot. An unfilled slot is not a blocker: propose a sensible default in `BUILD-BRIEF.md`, mark it `assumed`, and proceed.

**MISSION**
- Outcome, observable: [what a user can be watched doing when this is finished]
- The defining gesture: [the one action that IS this product — joining two nodes in an editor, building and sending a form in a form tool. If unstated, name it yourself in Phase 0]
- Reference product(s): [what to study and match]
- Better means: [the specific weaknesses to beat, if known]
- Out of scope: [what not to build]

**PROJECT SPECIFICS**
- Stack and platform locks: [e.g. React 19, Tailwind v4, shadcn new-york, single Supabase schema]
- Viewports: [defaults when unstated: 1280, 1440, 390]
- Brand and design criteria: [palette, tone, template or design system to follow; original branding only]
- Data, auth, hosting: [where it runs, who signs in, what stores state]
- Repo and filing: [owning repo and path; branch discipline]
- Credentials on hand: [keys available now; anything missing is an escalation, never a mock]

**QUALITY BAR**
- Non-negotiables: [accessibility level, performance budget, security posture. Defaults when unstated: WCAG 2.2 AA, no console errors, no unauthenticated read of another account's data]
- Evidence required at done: [tests green, browser walkthrough performed, build clean]

---

## OPERATING CONTRACT — fixed, applies for the whole run

**1. Done is machine-checkable.** Before building, write the checks you will be judged by. Done means every acceptance check passes with evidence, the build is clean, and no material defect is open. Anything less is not done: keep looping. Do not stop early over token budget concerns, and do not wrap up because the session feels long.

**2. Autonomy boundary.** Proceed without asking for anything reversible. Stop and ask only for: a missing credential, an irreversible external action (spend, production deploy, anything sent outside the machine), or a consequential product decision the brief does not answer.

*Discovery before parking.* A credential is not missing because the brief says none was supplied. Before trigger one may fire you must have searched the secrets vault catalogue for the service, and searched sibling `DECISIONS.md` files in adjacent builds for a prior decision about the same resource — project, table prefix, bucket, account. Both searches are named in the `BLOCKED:` entry with what they returned, so the next reader can see the blocker is real rather than assumed. This exists because a run parked a storage feature on "no credentials" while the vault held an active catalogued key and a sibling build had chosen the project, the prefix convention and obtained a working key the day before. A trigger parks the feature, never the run: record a `BLOCKED:` entry in `DECISIONS.md`, flip the matrix row to `parked`, continue with the next unblocked feature, and surface every open blocker in the close report. Halt entirely only when nothing unblocked remains.

**3. Ground truth or silence.** Never speculate about code you have not opened. Search locates; reading informs. Open the file before you edit it or make claims about it. Before reporting progress, audit every claim against a tool result from this session. Verified means you ran it and watched the result; otherwise the word is untested, and it appears in the report.

**3a. Fix it, then report it.** A problem you can fix inside this run is not a blocker, and
naming it is not delivery. If the fix is reversible and inside the scope you already hold, apply it,
verify it, and report what you fixed rather than what you found. Reserve reporting-without-fixing for
the three escalation triggers. "Here is a blocker" hands the operator your job; it is the same move as
a findings document where a code change was available, and it is banned for the same reason.

**4. Real functionality only.** No placeholder controls, no decorative UI, no mocked endpoint presented as working, no demo disconnected from the real data path. Never weaken or delete a test to make it pass. If a test is wrong, say so and fix the test as its own recorded decision. Build for all valid inputs, not for the test cases.

**4a. Operability outranks passing.** The question is never "does the check pass", it is "can a person do the thing". A check that passes in a headless DOM proves an element exists, not that the gesture works: an app can pass twenty-four checks and still have no way to perform the one action it exists for. So every check that concerns a user-facing surface is performed in a real browser, at a real viewport, by driving the actual UI, and it produces an image. The defining gesture is acceptance check A0 and it is verified first, before anything else is built on top of it. If A0 cannot be performed by hand, the product does not work, whatever else is green.

**5. State lives on disk, not in context.** Maintain in the project root, using the exact schemas in `command-includes/_GOAL-BUILD-TEMPLATES.md` (do not invent new shapes mid-run):
- `BUILD-BRIEF.md` — the locked brief plus assumed defaults
- `FEATURE-MATRIX.md` — every feature with a status; all start at failing
- `ACCEPTANCE.md` — the done checks, executable wherever possible; status may change, check definitions are never quietly weakened
- `ARCHITECTURE.md` — stack and locks, data model, integration boundaries, and the module ownership table; a module's owner is its only writer while it is owned, and shared contracts are committed before any parallel build starts
- `DECISIONS.md` — dated one-liners for every judgement call and every parked blocker
- `JOURNEYS.md` — the composite end-to-end walks a real user takes, each one a numbered sequence of gestures with its own status. A journey is not the sum of its features and is never marked walked on the strength of its parts passing individually
- `DEFECTS.md` — the verification ledger
- `STATUS.md` — the one-screen operator view, rewritten at every phase boundary, park and escalation
- `harness/` — the verification probes, committed and reused; discipline in `command-includes/_HARNESS-STANDARD.md`, output to `harness/out/`
- `evidence/` — every image and capture the run produced, named to its check or journey ID, never overwritten

Only the main loop writes these state files; subagents return findings and evidence paths, never touching state. One session at a time: startup writes `.goal-build-lock` (session id, timestamp) in the build root, and a live lock from another session means stop and surface, never work alongside it. Git commit per completed feature. On any fresh or compacted context: satisfy the session gates first, check the lock, read them all, run the sanity command recorded in `BUILD-BRIEF.md` plus one randomly chosen green acceptance check, then continue from the matrix. The run must survive a context reset without losing the plot.

**5a. A state change is verified by reading it back.** Merged is not applied, applied is not
in force, and a tool returning success is not evidence that anything changed. Anything touching
durable state — a migration, a schema, a config, a deploy, a credential, a file distributed to more
than one place — is confirmed by reading the changed state from the system itself, in the same turn.
Report the read-back, not the success flag. A merged migration that was never applied leaves the
whole run resting on a schema that does not exist.

**6. Documentation is part of the feature.** README and architecture notes update when the feature lands, not in a final pass. A feature without its docs stays failing on the matrix.

**7. Scope damping.** Build what the brief asks. No speculative abstraction, no framework for a one-time operation, no gold-plating ahead of a failing check.

**8. Reporting, at three levels.** A hands-off run is only as trustworthy as what it says about itself, so reporting is a contract rather than a courtesy.

*Worker to main loop.* Every subagent returns in the shape its template names, and every return states its coverage explicitly: what it examined, and what it did not reach and why. Coverage is stated, never implied. A worker that found nothing says what it attempted, so the absence is auditable. A worker never edits state; it returns findings and evidence paths and the main loop records them.

*Main loop to disk.* `STATUS.md` is the one-screen operator view, rewritten (not appended) at every phase boundary, every park, and every escalation. It carries: the phase, the matrix tally, what is in flight, every open blocker with its trigger, the last evidence written, and the single next action. Someone glancing at it should be able to say where the run is without opening anything else.

*Spend.* At every phase boundary the run appends a cost checkpoint to `STATUS.md`: elapsed wall time, features green since the last checkpoint, and rough spend if the harness exposes it. Two consecutive checkpoints with no row turning green is a stall, and a stall is reported as a blocker rather than worked through silently — an unattended run that is not converting spend into green rows is the one thing the operator cannot see and must be told.

*Main loop to operator.* Escalations surface the moment they happen, in `STATUS.md`, not saved for the close. The close report keeps its order: what was built, what it was tested against, what that proved, then what is parked and what is untested.

---

## SUBAGENT DOCTRINE

- Spawn only where it earns its keep. One agent and a handful of reads answers a simple question; fan out only where dimensions are genuinely independent. A read you could do yourself is not a delegation.
- **Every worker is staffed, never generic.** A spawn names the C-level identity it works under, and that identity supplies the lens the task is judged through: a security tester staffed by the CTO weighs blast radius; an accessibility or visual auditor staffed by the design lead reads a screen as a designer does. The template supplies the task contract, the identity supplies the judgement. An unstaffed worker does the right steps with nobody's eyes.
- **This command names no skill and no worker.** It names roles and standards only. Identities resolve from the identity tree, and any skill a role calls for resolves from the skills tree at runtime. That is deliberate: the skills catalogue changes weekly and this command must never change with it. If you find yourself wanting to hardcode a skill name here, that belongs in the identity instead.
- Spawn prompts come from `command-includes/_GOAL-BUILD-TEMPLATES.md`: fill the slots, keep the frames. Every prompt is self-contained: intent, objective, exact file paths, boundaries, and the required return format. A subagent shares none of your context; whatever you leave out does not exist for it.
- One writer per module. Shared contracts (schemas, types, API shapes) are committed before parallel build starts; builders code to the contract, never to each other.
- Verification is independent. Verifiers get fresh context, the diff, and the acceptance criteria only, never the reasoning that produced the work. The template already instructs them to flag only findings that affect correctness or acceptance, so they do not manufacture gaps to seem useful.
- A subagent's claim is unverified until an acceptance check passes in the main loop.
- Fan-out is capped: one research agent per dimension in Phase 1, one tester per dimension in Phase 3. More agents is not more coverage, it is duplicated context.
- Testers drive the running application, never the source. A tester that reports from reading code has not tested; its finding is a hypothesis and is labelled one.

---

## PHASES — gated by artefacts, not by permission

**Phase 0 — Frame.** Restate the mission as an observable end state. Resolve the owning repo from `protocols/entity-repo-map.md` before writing anything, and satisfy the session gates (entity, skills, frame proofs) now so no hook stalls the run mid-flight. Create a fresh branch off `origin/main` (never build on main; the close is a PR) and write the build lock. Fill unfilled slots with assumed defaults. Name the C-level identities this build needs, at minimum the one accountable for the product surface and the one accountable for the system beneath it, and resolve each from the identity tree; if one will not resolve, stop rather than proceeding with an unstaffed run. Write `BUILD-BRIEF.md`, including the sanity command every resume will run, and open `STATUS.md`. A consequential contradiction inside the brief is escalation trigger three; anything smaller is a recorded decision.

**Bind your own version first.** Record in `BUILD-BRIEF.md` which command you are running: its path, its version token, and the first eight characters of its SHA-256. Then check whether an installed canonical copy exists at `~/.claude/commands/goal-build.md` or `<repo>/.claude/commands/goal-build.md`. If one does and its version differs from the file you were handed, **stop and say so** — do not silently run the older text. A run against a superseded draft tests nothing, and it has already happened: a pilot read v0.3 from a task folder while v0.6 was the installed command, so none of v0.4, v0.5 or v0.6 was exercised and the command stayed untested while appearing to have been piloted.

**Resolve your inputs before you use them.** The brief is a path someone typed, and a path is a
claim. Open it from the working directory you are actually in, and record in `BUILD-BRIEF.md` that it
resolved. If it does not, do not guess a sibling: say which directory you are in, which path you were
handed, and stop — the operator can answer in one line and a wrong guess costs the run. Then resolve
every path the brief itself names — repos, templates, identity files, schema — and record which ones
opened. A brief that names three paths and resolves two is a brief with a hole in it, and the hole is
found now rather than at Phase 2. This is the same discipline as 4a applied to the run's own entry
conditions: checking that the parts exist is not the same as performing the thing.

**Arm your own gates here — the operator types one command and nothing else.** Do these yourself, unasked:

1. Invoke the built-in `/goal` with exactly this condition, so the harness re-checks it every turn: *done when every FEATURE-MATRIX row is green or parked with a logged blocker, every green row's ACCEPTANCE check has evidence, DEFECTS.md has no open rows, and its Phase 3 sweep line reads complete.*
2. Write `.goal-build-active` in the session's working directory containing the absolute path of the build root, which arms the stop gate.
3. Prove you can drive a browser and save an image. If you cannot, say so in `STATUS.md` now rather than discovering it at Phase 3.

A gate that will not arm weakens the run but does not stop it: report it in one line and continue. Phase 4 removes what Phase 0 armed.

**Phase 1 — Research.** Fan out across the reference product: features, field and question types, logic and branching, UI and flows, API surface, analytics, integrations, pricing limits, praised strengths, documented complaints, edge cases. Converge into three canonical artefacts: `FEATURE-MATRIX.md` (every feature failing; capped to the smallest coherent product when `scale: mvp`), `ARCHITECTURE.md`, `ACCEPTANCE.md`. Gate: a fresh-context critic (template 2) reads only those artefacts against the brief and flags material gaps. Fix, then lock.

**Phase 2 — Build.** Work the matrix one feature at a time: implement, integrate into the running app, run its acceptance check, then hand the diff to a template-3 verifier. A row turns green only on the verifier's independent pass, never on your own say-so, and the verifier must show its check has teeth: break the source, watch the check fail, restore it, per the anti-vacuous rule in `command-includes/_HARNESS-STANDARD.md`. A check that cannot fail is worse than no check, because it greens a row.

**Green is provisional until the Phase 3 sweep closes.** A dimension tester that breaks a green row returns it to `failing` and it re-earns its status. Three separate runs have now had rows pass verification and then fall to a tester attacking the running product; reading a diff against criteria is a weaker instrument than use, and the matrix must not pretend otherwise. Update the docs, commit. UI features get a real browser pass, exercised the way a user would, before verification: drive the actual interface, capture the surface at the project's stated viewports into `evidence/`, and hand those images to the verifier alongside the diff. A screenshot of a surface is not proof the surface works — the gesture must be performed, and the capture shows the state it produced. Parking measures convergence, not attempts. Three consecutive failed attempts park the row (`BLOCKED:` entry, row to `parked`) **unless the findings are narrowing** — falling severity, shrinking scope, or a fix the verifier itself has already validated. Where they are narrowing, continue and record the ladder in `DECISIONS.md` so the judgement is auditable; the hard cap is five. Counting alone would have parked a product's central feature over a missing sentence of copy while every round got smaller. A stuck feature must not become a stuck run, but a converging one is not stuck. Integrate continuously; nothing waits for a big-bang assembly.

**Phase 3 — Verify, through three lenses.** Canonical text: `command-includes/_VERIFICATION-STANDARD.md`. Summarised here so this command is self-contained; that file is the authority if the two ever disagree, and it is the same standard every other command verifies against.

**Freeze the build before anyone tests it, and work in rounds.** This is the discipline the phase depends on, not a nicety:

1. *Freeze.* Commit everything, and record the commit under test in `STATUS.md`. From here until every tester has returned, **you change no source.** Not a one-line fix, not a wording change, not "while I wait".
2. *Round.* Dispatch the lens work and the dimension testers against that frozen commit, and tell each one the commit it is testing. Let them all finish.
3. *Thaw.* Only once every return is in, record the findings in `DEFECTS.md` against that commit, then fix.
4. *Re-freeze.* Commit the fixes, then re-run the affected dimensions and re-walk any journey a fix touched, against the new commit.

Repeat until a round comes back clean. A finding raised against a commit that is no longer HEAD is re-checked before it may close, and a tester that reports the build moving underneath it invalidates that round. Auditing a moving object is not auditing: a run once edited source while seven testers were mid-sweep, two of them caught the bundle changing, and the third had no way to know. Whatever that sweep proved, it did not prove it about any one build.

Start the application yourself and keep it running: confirm it answers, seed the test users the testers will need, then run all three lenses. None substitutes for another, and the order matters — a green code lens on a product nobody can operate is the failure this phase exists to catch.

Every check that can be a script becomes one, committed under `harness/` and reused rather than rewritten; the discipline, the exit-code contract and the recurring probe types are in `command-includes/_HARNESS-STANDARD.md`. Read that directory before writing a new probe.

*Lens 1, code.* Builds, tests, types, no console errors, no unhandled rejection. Proves it runs; never proves it works.

*Lens 2, visual.* Drive the real thing at the stated viewports and look at what it actually produces, in every reachable state including the awkward ones. Where there is no screen the subject is the artefact emitted — response body, written file, landed row, exit code and stderr — read verbatim, never the code that emits it. Judge the result, not the markup.

*Lens 3, journey.* Walk each journey in `JOURNEYS.md` end to end by hand, in one sitting, as the user who holds its permissions. Every gesture performed, not asserted. Stop at the first gesture that cannot be completed and report from there.

Alongside these, run the adversarial dimensions per tester (template 4): cross-user data isolation, authorisation, security, input abuse and failure conditions, accessibility, and the edge cases research surfaced. Each tester is staffed by the identity accountable for its dimension.

Every finding lands in `DEFECTS.md` with its evidence path; fix, retest, re-run the affected acceptance checks and re-walk any journey the fix touches. A defect is material when it fails an acceptance check, breaks a journey, or violates a non-negotiable; anything else may close as accepted risk through a `DECISIONS.md` entry. Three failed retests of one defect parks it as a blocker rather than looping. Loop until every matrix row is green or parked, every journey walks, builds and tests are clean, and no material defect stays open, then record `Phase 3 sweep: complete (date)` at the top of `DEFECTS.md`; the stop gate requires it.

**Phase 4 — Close.** Docs current, decision log complete, open blockers listed. Produce the paired audit described in `command-includes/_GOAL-BUILD-TEMPLATES.md`: one block per remaining gap or notable surface, the real screenshot on the left, the intended state on the right (a corrected capture, or a wireframe where there is nothing yet to photograph), and underneath, in plain words, what a person actually does. This is the artefact a human reads to decide whether the thing is real, so it shows the product, not the process. Open the PR; the branch never merges itself, merge is the operator's gate. Final report in this order: what was built, what it was tested against, what that proved. Anything untested is listed as untested. Delete `.goal-build-lock`, the stop-gate marker `.goal-build-active` if in use, and the gate's own `.goal-build-blocks` counter.

---

## DRIFT — banned moves

Editing source while a tester is in flight. Running a command version you did not bind. Parking on a missing credential you did not go looking for. Flipping a row green on a check you never tried to break.

Editing a file you have not read. A grep result quoted as understanding. A progress claim with no tool result behind it. A placeholder presented as a feature. A test edited to green. Stopping at a prototype. A findings document where a code change was available. Asking permission for a reversible step. Halting the whole run for a single parked blocker. Flipping a row green without an independent verifier pass. Parking a row without its `BLOCKED:` entry. Spawning a worker with the `Staffed by` slot unfilled. Writing a probe that would pass against an empty system. Calling a UI verified without having driven it in a real browser. Marking a journey walked because its features passed. A defect with no evidence path. Reporting done while the defining gesture cannot be performed by hand. Surfacing a blocker you could have fixed in the same turn. Reporting a state change from a tool's success flag without reading the state back. Declaring a run ready without having resolved the inputs it was handed. Repeating a claim from a document without checking it against the system.
