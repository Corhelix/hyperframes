# _COMMAND-CONTRACT — the mini contract every command declares

<!-- Include, not a command. Lives beside the commands. v0.1 2026-09-08 -->

A command file is two things stacked: a **contract** a machine can check, and **instruction**
a model reads. Today they are mixed together and only the second exists, which is why nothing
can verify that a command loaded what it said it would.

The contract is YAML frontmatter. It is short, it is machine-readable, and
`command-contract-check.py` fails on it. The instruction stays prose.

## The block

```yaml
---
name: cto
description: Contextual technical strategy. Builds and changes systems.
argument-hint: "[codebase or target]"
disable-model-invocation: false

contract:
  writes: true
  fires_when:
    - a system will be changed as a result
    - a codebase, schema or workflow is named
  does_not_fire_when:
    - the subject is understood rather than changed  -> /research
    - the ask is to frame or scope                   -> /strategise, /plan
  loads:
    always:
      - viewports/cto.md
      - command-includes/_VERIFICATION-STANDARD.md
      - command-includes/_GOAL-FIRST-CONTRACT.md
    conditional:
      - when: task touches UI
        load: [skills/frontend/senior-frontend.md, skills/frontend/ui-design-system.md]
      - when: task touches API and UI together
        load: [skills/frontend/senior-fullstack.md]
  returns:
    - id: goal
      is: one observable end state someone could watch happen
    - id: verdict
      is: PASS or REVISE, from the three lenses, with an evidence path per finding
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every finding carries an evidence path
    - no claim is unlabelled under Lens 4
  graded_by: cmo-verify

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---
```

## Field rules

**`writes`** — true if the command creates or edits anything. A command with `writes: true`
must set `disable-model-invocation: true` unless it is purely diagnostic. This is the input
half of reliability: a command that writes files should not fire because the model
half-recognised a phrase.

**`fires_when` / `does_not_fire_when`** — the triggering contract. `does_not_fire_when` names
the command to hand to. A command that cannot say what it is not for will be invoked for
everything, which is how a build command ran an operating-model research question for hours
on 2026-09-08.

**`loads.always`** — paths that must be read before the command acts. Every path is checked
for existence by the contract checker, and checked for an actual Read call by the transcript
checker. This is what makes loading verifiable rather than requested. Declared and unread is
the failure this field exists to catch.

**`loads.conditional`** — `when` in plain words, `load` as paths. Same existence check, no
transcript check, because the condition may not have applied.

**`returns`** — the output contract. Each entry has an `id` and an `is`. "Produce a
deliverable" is not a return shape. A specified shape is the difference between output that
can be checked and output that has to be read.

**`acceptance`** — how you would know this run was good, written so a grader can test it.
These are the assertions `graded_by` runs against.

**`graded_by`** — the agent that grades the output independently. A command cannot define
whether its own output passed. If a command has no grader, say `graded_by: none` and mean it.

**`includes`** — shared blocks, by name, resolved from `command-includes/`. The block text
does **not** appear in the command file. It is loaded when the situation arises, not on every
invocation.

## Why the includes are references and not inlined text

Measured 2026-09-08 across 43 commands: 12,481 lines total, of which 4,817 are the same four
blocks repeated verbatim. Thirty-eight per cent of every command load is text identical to
forty other files, and it is the procedural part, which is the least useful for the work and
the most expensive to carry.

Those commands are then copied into 22 repos, so the gate-mechanics text exists roughly nine
hundred times on disk. `_GATE-MECHANICS` already has **four divergent variants** across the 41
commands carrying it. Duplication has already produced the drift it was meant to prevent.

The old justification was self-containment for iOS, where `command-includes/` was absent from
canonical. It was added to `claude-system/workspace/` on 2026-09-08, so the includes now travel
with the commands and that reason no longer holds.

## What the contract does not do

It does not stop a model ignoring the prose beneath it. Nothing in a file does that; a resident
instruction decays across a conversation, which is the finding behind the 2026-04-11
architecture decision.

What it does is make three things checkable by something outside the model: whether the command
should have fired, whether it loaded what it declared, and whether its output has the shape it
promised. That is a smaller claim than reliability, and it is true.
