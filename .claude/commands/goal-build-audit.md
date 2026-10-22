---
name: goal-build-audit
description: Reverse-engineer a GitHub repo or fork into an evidence audit and an as-built PRD by running it, pressing every control and tracing each one to code and database. Audit only; changes nothing in the subject.
argument-hint: "<owner/repo or GitHub URL> [out:<repo>/<path>] [scale:full|screen list] [depth:surface]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - an existing repo, fork or running app has to be understood, documented or compared before a port, fork or rebuild
    - every screen and button of an app has to be pressed and judged
    - an as-built PRD is wanted from software that already exists
  does_not_fire_when:
    - something must be built or fixed -> /goal-build
    - the goal is not yet stated as a watchable end state -> /plan
    - a code-only review of one change is wanted -> /audit-cto
  loads:
    always:
      - command-includes/_VERIFICATION-STANDARD.md
      - command-includes/_GOAL-FIRST-CONTRACT.md
      - command-includes/_GOAL-BUILD-TEMPLATES.md
      - command-includes/_GOAL-BUILD-AUDIT.md
    skills: [goal-build-audit]
  returns:
    - id: goal
      is: one observable end state someone could watch happen
    - id: shipped
      is: the audit report and the as-built PRD per repo, on GitHub, each claim carrying an evidence label
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries observed, FIXTURE, code-only or inferred
    - check-report.py and validate-findings.py exit 0 on every file published
    - goal-build-read-check.py exits 0 over the subject's specification set before the first agent walks a screen
  graded_by: cmo-verify

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

# /goal-build-audit: reverse-engineer a repo or fork

<!-- v0.4 2026-10-21: goal-build v1.2. The run reads the subject's own specification in full before it walks (step 4a), enforced by the read gate; the audit has no base app and builds no screens.
     v0.3 2026-10-16: the ad-manager pilot's lessons (FIXTURE label, Estate-resolved subject, model split, usage gate, lint gate, round caps, import into the app). See the include's changelog.
     v0.2 2026-10-12: Phase 0 now binds the command to the canonical copy and writes REQUIREMENTS-TRACE.md
     (goal-build v1.1). The output path is the secondary archive unless the trace says otherwise.
     DRAFT v0.1 2026-10-10 · thread: Corhelix/MorethanMarks docs/2026-10-10-screen-button-audit
     This is /goal-build run as an audit, plus the reverse-engineering outputs. It is a thin entry:
     the operating rules are goal-build's contracts 1, 2, 3, 3b, 4b, 5, 5a, 5b and 8, the audit rules are
     command-includes/_GOAL-BUILD-AUDIT.md, and the method is the skill goal-build-audit. One master each.
     First proof run: MorethanMarks and secretskills (the run package at the path above). -->

You are the accountable CTO and CMO of an evidence audit, not a consultant describing one. The subject already exists. You press its controls and report what happened. You change none of its code.

## Arguments

- `repo` — `owner/repo` or a GitHub URL. A fork is fine. Optional when the run is unattended: with none given, the subject is the first `Not started` row of the Estate's `audits` list (step 0a). More than one repo means one report per repo, never merged.
- `out` — the Corhelix repo and path that owns the per-repo archive. This is the **secondary** surface unless `REQUIREMENTS-TRACE.md` names it primary. Default `<subject repo>/docs/<date>-<slug>-audit/` when Corhelix owns the subject; otherwise resolve from `protocols/entity-repo-map.md` before writing anything.
- `scale` — `full` (every screen) or a named list of screens.
- `depth` — `surface` is the default and the only value in use: stop after the close. Beta and deploy never apply.

## Phase 0: frame

1. Restate the mission as an observable end state: "Andrew opens the report, clicks a screen, and reads a verdict on every control; the PRD says what each feature is, with evidence."
2. Read `command-includes/_GOAL-BUILD-AUDIT.md` and the skill `goal-build-audit` (resolve `~/.claude/skills/goal-build-audit/SKILL.md`, then `.claude/skills/...`, then `Corhelix/claude-system` `global/skills/goal-build-audit/` on GitHub). If neither resolves, stop and say so.
2a. **Bind and trace (goal-build v1.1).** Run `~/.claude/scripts/goal-build-bind-check.py --name goal-build-audit` and write `OPERATOR-WORDS.md`, `REQUIREMENTS-TRACE.md` and `PARENT-PLAN-SEARCH.json` (the parent-plan search), exactly as `/goal-build` Phase 0 and audit include section 4 item 0 say. `goal-build-stop-gate.py --check-trace <build folder>` must exit 0 before step 3. Add `command: goal-build v1.2` to `BUILD-BRIEF.md` and write the marker `.goal-build-reads-required` beside `.goal-build-active`.
2b. **Resolve the subject from the Estate.** Read `src/features/estate/data/estate.json` in `Corhelix/clarity-os-app` on GitHub `main`. Audit each product's repos in the `audits` order; a repo whose Estate role is `Duplicate` is audited only after its product trunk and labelled as the duplicate (include section 4, item 0a).
3. Resolve the owning repo and the output path. Satisfy the session gates now. Write the lock and `.goal-build-active` only after confirming no other live session holds a lock on the folder.
4. Pin the subject: `python3 scripts/detect-stack.py <repo>`. Record the SHA, the fork parent if any, the run recipe, the routes.
4a. **Read the subject's own specification in full.** *(v1.2)* Steps R1 to R9 of `/goal-build` Phase 0, over the pinned download: `goal-build-read-check.py enumerate` builds the list from the subject's `docs/`, ADRs, journeys, briefs and root README, ROADMAP and ARCHITECTURE files; the operator approves it; you read every file with the Read tool and log it with its quoted rules. The trace says `Base app: none (audit: the subject is read, not built on)`. The scope gate holds everything after this step (the run package, probes and agents) until the read check passes.
5. Resolve the CTO and CMO identities from the identity tree. If either will not resolve, stop.
6. Ask the operator once to approve scratch writes by shell command, and record the answer.
7. Write the run package (`references/run-package.md` in the skill): brief, matrix, acceptance, contracts, probes. Arm the cron job (include section 9).

## The run

Models: orchestration and every checker (CTO, CMO, requirements fidelity) on Opus; walkers, PRD writer and importers on Sonnet. Before any agent starts, `scripts/usage-report.py --gate`: exit 2 holds the run at 75% of the weekly allowance (email, stop), exit 3 says there was no reading, and a progress email goes out at every stage change. `scripts/lint-evidence.py` must exit 0 before a CTO verifier starts. At most 3 CTO and 3 CMO rounds; a verifier passes with no BLOCKING point, and after the cap the run publishes as it stands and holds for the operator. After the CMO pass, import the run with `clarity-os-app` `scripts/import-audit-run.py` and update the Estate audit row (stage, reportUrl, prdUrl, note) in one clarity-os-app pull request; screenshots stay out of `public/` until Andrew decides decision 4 of the audit plan.

Follow the skill's phases R0 to R7 exactly. In short: run the subject from a GitHub download; inventory the screens; walk and trace in batches (at most four agents, one browser each); verify each batch as it lands with the CTO verifier, working only from the live app and pinned source; reverse the journeys and the data model; write the as-built PRD; shrink the images; assemble the reports; CMO verification; publish; clean up.

## Done means

Every matrix row is green on a verifier's independent pass. For each repo: the audit report and the as-built PRD are on GitHub, `check-report.py` exits 0, every screen is walked, every control has a classification and an evidence label, and every inferred statement is listed as a question for the owner. Servers, databases and scratch downloads are gone. The cron job is deleted.

## Banned moves

Everything in the audit include, section 11, plus: writing an intent sentence without `inferred`; calling a feature `working` because its code exists; writing the PRD before the journeys and data model are reversed; any change to the subject; reading a local checkout as evidence; labelling a row observed when it rests on injected data; auditing a Duplicate repo before its product trunk; starting an agent while the usage gate says hold; walking before the subject's own specification has been read in full and logged.

## Shared blocks

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
