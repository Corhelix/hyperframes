---
name: checkpoint
description: a run-often mini-handoff to disk.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - the session state is captured mid-thread
  does_not_fire_when:
    - the thread is ending and must transfer -> /handoff
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: state
      is: where the work is, what is decided, what is next
    - id: open
      is: what is unresolved, so nothing is silently dropped
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: .claude/commands/checkpoint.md | Skill: session-report.skill.md | Mode: checkpoint -->
# /checkpoint — a run-often mini-handoff to disk

A lightweight `/handoff`. It writes the thread's load-bearing state to a durable file so a
compaction, fork, or fresh session loses nothing. Run it whenever the context sensor nudges
(delta past a band), before a risky step, or at any natural seam. Cheap, repeatable, no
ceremony. It is NOT the full handoff — no gather, no HTML, no memory — just the distillate to
disk.

## Rule it serves
Compaction and fork are lossy or heavy. A checkpoint on disk is lossless-by-design: the
load-bearing state survives independently of the thread, so nothing rides on the model
remembering it.

## Procedure

1. **Find the thread folder.** Use the current task/thread folder if one exists
   (`docs/reports/<YYYY-MM-DD>-<slug>/` or the thread's working folder). If none exists yet,
   create `docs/reports/<YYYY-MM-DD>-<slug>/` on the current branch. NEVER `/tmp`.

2. **Append a checkpoint file** `CHECKPOINT-<YYYY-MM-DD-HHMM>.md` with exactly these sections,
   filled from the ACTUAL thread (not a template):
   - **Decisions settled** — each with a one-line rationale. Do not re-litigate these.
   - **Open questions** — each with an owner.
   - **Files & artefacts** — every reference as a FULL URL (PRs, branches, blobs). A bare path
     is a defect; a fresh reader knows no locations.
   - **Next step** — the single next action, concretely.
   - **Canonical vocabulary** — any fixed terms/enums the thread relies on.

3. **Keep it tight.** A checkpoint is the distillate, not a transcript. If a section is empty,
   write "none yet" rather than padding.

4. **Confirm in chat**: the checkpoint path (full), and the one next step. Do not commit unless
   the user asks; the file is durable on disk regardless.

## Naming
`CHECKPOINT-<YYYY-MM-DD-HHMM>.md` in the thread folder. ISO dates. One thread = one folder =
one branch. Later checkpoints supersede earlier ones; keep them all (cheap, and they show the
trail). When the thread ends, `/handoff` produces the full transferable record.

## Relationship to the sensor
The context sensor (statusline + Stop hook) nudges when the conversation-delta crosses a band.
`/checkpoint` is the cheap response to that nudge: distil now, keep going or hand off with the
state already safe. The PreCompact hook also prompts for it before an auto-compaction.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
