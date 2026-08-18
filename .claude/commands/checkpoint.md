---
description: a run-often mini-handoff to disk.
argument-hint: "[context or target]"
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
