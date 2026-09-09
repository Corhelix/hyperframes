---
name: entity
description: Load an entity or client context cascade before working on their material.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - entity context is loaded before brand or client work
  does_not_fire_when:
    - the work is platform engineering with no entity -> /cto
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: context
      is: the entity's ICP, positioning, voice and locked decisions, filtered not listed
    - id: superseded
      is: which files were dropped as out of date, and why
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- slash-commands/entity.md is canonical; .claude/commands/entity.md must match exactly | Context-cascade (artefact-v1) — no workflow -->
# /entity — Load and verify entity context

Load all context files for a brand entity. Verify completeness. Flag gaps.

---

## Procedure

### Step 1 — Identify the entity

Ask: **Which entity is this for?**

Known entities: Wolf & Eagle, EdisonEd, Serve With Clarity, Daleys Nursery, Andrew Cockburn, ALC Capital.

If the user names a client (e.g., "Axia Office", "Hillcrest"), identify the parent entity first (Axia → Wolf & Eagle, Hillcrest → EdisonEd). Load the parent entity context AND the client deliverables folder.

### Step 2 — Load entity files

Read `protocols/entity-repo-map.md`. Find the entity's table. Read **every file listed** — no exceptions, no tiers, no "on-demand."

Path resolution:
- `alc-group/` → ``
- `client-projects/` → `../client-projects/`

If a file doesn't exist, mark it as **GAP** — do not skip silently.

### Step 3 — Load cross-entity resources (if copy/content task)

If the task involves written output, also read:
- Universal Writing Guardrails: `alc-group/writing-system/writing-guardrails.md` (canonical, applies to all written output, includes AU/UK spelling)

### Step 4 — Confirm what's loaded

Output a context summary:

```
ENTITY LOADED: [name]

ICPs:
- [ICP 1 name]: [one-line — emotional state + buying trigger]
- [ICP 2 name]: [one-line]

Brand voice: [3-4 key characteristics from tone.md]
Positioning: [one-sentence from positioning.md]
Locked lines: [count] lines loaded (or "none defined")
Banned patterns: AI writing guardrails loaded (or "not loaded — no copy task")

Knowledge passes loaded:
✓ [pass name] — [one-line what it contains]
✗ GAP: [pass name] — file missing

Files read: [count]/[expected]
Gaps: [list missing files and what they block]
```

### Step 5 — Flag blockers

If critical files are missing (ICP, positioning, brand), **stop and flag**:
> "Cannot proceed with [task type] — [file] is missing. This blocks [specific capability]."

Do not infer missing ICP language. Do not fabricate positioning.

---

## Chains to

After `/entity` completes, the user typically runs:
- `/strategise` — for strategic analysis using this entity context
- `/draft` — for copy production using this entity context
- `/audit` — for auditing existing copy against this entity context

The entity context stays in the conversation and is available to subsequent commands.

---

## What this command does NOT do

- Produce any output, copy, or analysis (use `/draft`, `/strategise`, `/audit`)
- Make strategic decisions (use `/strategise`)
- Modify entity files (flag gaps, don't fix them)
---

## Universal Quality Layer

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the universal writing guardrails: `alc-group/writing-system/writing-guardrails.md`.

Covers AI-tells detection (banned vocab, bloated verbs, dead openings/transitions), negative parallelism (5A-5I), analogy and metaphor control (6), AU/UK spelling (11), and the 13-step sweep (10). Three or more patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Universal Quality Layer for the full enforcement protocol across phases.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
