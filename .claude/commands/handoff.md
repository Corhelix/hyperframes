---
name: handoff
description: Turn the current thread into a transferable handoff a fresh session can pick up cold.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a thread is turned into a transferable handoff for a cold session
  does_not_fire_when:
    - the session continues -> /checkpoint
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: handoff
      is: everything a cold session needs: goal, state, sources, next unblocked task
    - id: blockers
      is: what is blocked and on whom, named rather than implied
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
