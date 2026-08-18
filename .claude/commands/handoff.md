---
description: Turn the current thread into a transferable handoff a fresh session can pick up cold.
argument-hint: "[context or target]"
---
<!-- Source: .claude/commands/handoff.md | Skill: session-report.skill.md | Mode: handoff -->
# /handoff — full, transferable session handoff

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write, run the file-home gate: read GitHub first, resolve and confirm the dated task folder against `repo-map.json`, create it in the real repo, then cut a feature branch. Full text in `protocols/file-home-gate.md`. Enforced at commit by the pre-commit lane-guard.

Invoke the **`handoff`** skill (Skill tool, `skill: "handoff"`) before anything else, then
follow its phases. `/handoff` turns the current thread — of any kind — into a self-contained
handoff a fresh session can pick up cold.

It is domain-agnostic. It works for a build, a research thread, an audit, a strategy session, a
bug hunt — anything. The rule it serves: **a fresh session knows no file locations and holds no
prior context, so every reference is a full URL and every settled decision is stated.**

## What it does

1. **Gathers** the mechanical facts — runs `skills/handoff/scripts/gather_session.py` to collect
   this thread's PRs, changed files, and the **full GitHub URLs** across the repos in play (plus
   any reference files pinned with `--extra-file`), verified.
2. **Synthesises** the `handoff-v1` doc from the real conversation: **topic, goal, inputs**
   (what the human supplied), **research** (with sources + numbers), **learnings** (findings,
   gotchas, the corrections made), **decisions** (settled vs open), **files & artefacts** (full
   URLs), **canonical vocabulary/categories** (fixed enums so past configuration is reused),
   **next task & flow**, and **ground rules**.
3. **Produces** the artefacts under `docs/reports/<YYYY-MM-DD>-<slug>/`: a summarised
   `README.md`, the `HANDOFF-v1-<slug>.md` doc, and — only when the learnings/data double as
   content — a rich multi-tab HTML report from the skill's template (opened in the browser).
   **If the thread has a governing `/build-plan`, the handoff's resume anchor is that plan's
   full URL + its `plan-state` (readiness, current stage, next unblocked task, outstanding
   prerequisites) — it points at the plan, it does not restate it. The next session resumes with
   `/build-plan <thread> status`, not a cold re-read.**
4. **Logs memory** — the durable facts written to the memory system (decisions/gotchas as
   `project`/`feedback`, external resources as `reference`), with pointers in `MEMORY.md`.
5. **Prints the full detailed prompt in chat** — paste-ready, self-contained, full URLs inline.
6. **Commits** — branch off current `main`, single-concern PR, merge after browser review of any
   HTML — and returns the merged URLs plus the paste-ready prompt.

## Arguments (optional)

- `/handoff <slug>` — set the thread slug (else derived from the topic).
- `/handoff since:YYYY-MM-DD` — override the gather cutoff (else the session start).

## Rules

- **Never write a deliverable, report, or handoff to `/tmp`, `/private/tmp`, or the
  scratchpad** — those are temp-only. Every artefact lands in the repo folder on a branch; a
  `file:///tmp/...` path handed to the user is a defect.
- Every reference in every artefact is a **full, verified URL** — never a bare path.
- State **settled** decisions so a fresh session does not re-litigate them; name **open**
  questions with an owner.
- If a `/build-plan` governs the thread, **reference it as the single resume anchor** — full
  URL + `plan-state` — rather than producing a rival summary of stages/tasks. One plan, pointed
  at, never re-derived.
- Learnings carry the **why** — including dead-ends and corrections — so they are not
  re-discovered the hard way.
- Pin the **canonical vocabulary** (fixed enums, naming) so prior configuration is not wasted.
- Apply the naming/dating convention: `docs/reports/<YYYY-MM-DD>-<slug>/`, ISO dates, one thread
  = one folder = one branch.
- Show any HTML deliverable in the browser before merge.

The skill (`skills/handoff/SKILL.md`) is the single authority once invoked.

---

## GATE MECHANICS — the hooks that will deny you

Canonical text: `command-includes/_GATE-MECHANICS.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

**The session markers.** `.entity-loaded` (or `no-entity` for platform work) and
`.skills-approved` gate every Write and Edit via `skills-gate-v2.sh`. Since v2.4
the skills proof is checked for content, not length: the frame needs eight
distinct words, at least one proposed skill must resolve against
`skills-catalogue.json`, and if this session invoked skills the proposal must name
one of them. Legacy `.claude/.entity-loaded` and `.claude/.skills-approved` paths
are ignored.

**Load order, enforced on reads.** `command-load-order-gate.py` arms off the
operator's typed prompt, not off anything the model does. A denied Read is the
gate working, not a tooling failure.

**File home, enforced on writes.** `clean-path-gate.py` allows only
`~/Documents/CLEAN/<repo>/<path>`, and the first segment must be a real repo — in
`repo-map.json` or present on disk with a `.git`.

**Tool discipline, enforced on Bash.** `block-bash-fileops.py` denies `cat`,
`head`, `tail`, `grep` and `find` in every pipeline position, including
`/usr/bin/grep`, `\grep`, `env grep`, `xargs grep` and `bash -c "cat ..."`. Use
Read, Grep and Glob. Bound payload with Read's `offset`/`limit` or Grep's
`head_limit`. If the dedicated tool is absent from the session, `git grep` and
`python3` are allowed and are not bypasses.

Working around a gate rather than satisfying it is the drift the gates exist to
catch, and it is caught in audit.

## When something is blocked: present a form, do not halt

A denial that arrives as a paragraph of instructions is homework. The operator has
to read the prose, work out what the decision actually is, and then run commands by
hand. That is the failure mode, not the block itself.

**Every blocked action that needs operator authorisation is presented as a
structured approval question — AskUserQuestion — never as prose asking them to go
and run something.**

Distinguish the two cases first, because they need opposite responses.

**A gate blocking work it should not** is a defect. Do not ask for approval to work
around it. Fix the gate, or report it as a defect with the reproduction. Examples
from 2026-08-16: the skills gate denying the write that satisfied it; a proposal
denied for naming skills the session had not invoked; a catalogue blind to
project-level skills. None of those warranted an approval prompt. They warranted a
fix.

**A guard blocking work it should** is not a defect. `gh secret set` writing
credentials, `apply_migration` running DDL against a shared production database,
anything destructive or outward-facing. Never route around these, and never ask for
a standing allow-rule when a single decision is what is needed.

For the second case, the response is a form with:

  - the one decision, stated as a question the operator can answer without reading
    the transcript
  - what was already tried and why it failed, in one line each — a blocked action
    reported without the routes attempted is a ghost blocker
  - the blast radius, named. Shared database, live credentials, how many repos
  - options that are genuinely different, each with its consequence, and a
    recommendation. An options menu with no recommendation is banned by the
    goal-first contract and that applies here
  - what happens to the rest of the work either way. If other items are unblocked,
    say you are proceeding with those, then proceed

Then keep working on whatever does not depend on the answer. A session that halts
entirely on one blocked item, when six others are unblocked, has turned one
permission decision into a stopped thread.
