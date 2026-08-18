---
description: Load an entity or client context cascade before working on their material.
argument-hint: "[context or target]"
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
