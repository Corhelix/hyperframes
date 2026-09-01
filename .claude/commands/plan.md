---
description: Scope a task and produce a lightweight SOW: outcome, scope, success criteria and sequence.
argument-hint: "[context or target]"
---
<!-- slash-commands/plan.md is canonical; .claude/commands/plan.md must match exactly | Workflow: plan-and-build.workflow.json | Phase: plan -->
# /plan — Scope a task and produce a lightweight SOW

Define what's being done, what's out of scope, what success looks like, and the sequence of work. Produces a SOW document that governs subsequent `/build` or `/draft` sessions.

---

## MCP Tools Available

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Context7** (`mcp__context7__*`) | Step 2 (Load context), Step 3 (Sequence the work) | Verify any library or platform API named in the plan actually exists in the installed version. A plan that names a non-existent endpoint produces a build that fails before sprint 1 |

**Rule:** if the plan sequences work against a library API, that API must be Context7-verified before the plan is locked. Otherwise stamp it as an open question Andrew must resolve.

---

## Procedure

### Step 1 — Establish what's being scoped

Ask (if not already clear):
1. **What's the project or task?**
2. **What's the desired outcome?** (what should exist when this is done?)
3. **What entity or codebase** is this for?
4. **Constraints?** (timeline, budget, platform, dependencies, blockers)

**GATE — present for confirmation:**
> Planning: [outcome] | Entity: [name or none] | Type: [new/modify/audit]. Correct?

Wait for response.

### Step 2 — Load context

If a `/strategise` or `/spec` was already run this session, use that analysis.

Otherwise: load context needed for scoping:
- If entity work → read `protocols/entity-repo-map.md`, load entity files
- If codebase work → read the relevant source files, package.json, existing specs
- If strategic work → read prior strategy docs from `projects/<entity>/tasks/`

### Step 3 — Define scope

Write out:

**Outcome:** One sentence. What exists when this is done that doesn't exist now.

**In scope:** Specific deliverables (list each).

**Out of scope:** What this does NOT include. Be explicit — ambiguous scope is where drift lives.

**Success criteria:** 3-5 binary pass/fail checks. Not "improved user experience" but "user can complete checkout in under 3 clicks."

**Dependencies:** What must exist before this can start? What blocks progress?

**Risks:** What could go wrong? What's the mitigation?

### Step 4 — Define the sequence

Break into phases or milestones. Each milestone has:
- **What** gets produced
- **Acceptance criterion** (how you know it's done)
- **Estimated scope** (small / medium / large)

Keep it simple. 3-5 milestones for most tasks. If you need more than 7, the scope is too big — split into multiple SOWs.

**Where the thread has screens, the UX milestones come first and no build milestone may precede them.** In this order: the screen inventory with five states per screen; the journeys written click by click, every gesture carrying an observable success criterion and the thing it passes forward to the next screen; then unbranded clickable shells sitting inside the product's real header and side nav, walked in a browser. Only after those are confirmed does a milestone exist that writes product code, and styling is a milestone of its own at the end rather than part of any build milestone. A plan that puts a screen-bearing build milestone before its journeys is a plan built on a flow nobody has seen.

### Step 5 — Output the SOW

```
# SOW: [Project Name]
Date: [YYYY-MM-DD]
Entity: [if applicable]

## Outcome
[One sentence]

## Scope
### In scope
- [deliverable 1]
- [deliverable 2]

### Out of scope
- [explicitly excluded 1]
- [explicitly excluded 2]

## Success Criteria
- [ ] [binary check 1]
- [ ] [binary check 2]
- [ ] [binary check 3]

## Milestones
### 1. [Milestone name]
Deliverable: [what]
Done when: [acceptance criterion]

### 2. [Milestone name]
...

## Dependencies
- [what must exist before starting]

## Risks
- [risk]: [mitigation]
```

---

## Output location

Save to: `projects/<entity-or-task>/DRAFT-v0.1-YYYY-MM-DD-SOW.md`

---

## Chains to

- `/build` — to execute against this SOW
- `/draft` — to produce copy defined in this SOW
- `/report` — to close the SOW with a session report
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
