---
name: plan
description: Scope a task and produce a lightweight SOW: outcome, scope, success criteria and sequence.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a non-trivial task is scoped into outcome, success criteria and sequence
  does_not_fire_when:
    - the task spans many sessions and needs governing -> /build-plan
    - the plan already exists and the work is execution -> /build
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: outcome
      is: the observable end state
    - id: sequence
      is: the steps in order, each with what proves it done
    - id: out_of_scope
      is: what this deliberately does not cover
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- slash-commands/plan.md is canonical; .claude/commands/plan.md must match exactly | Workflow: plan-and-build.workflow.json | Phase: plan -->
# /plan — Scope a task and produce a lightweight SOW

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write: `git fetch origin`, then confirm the target folder is canonical on GitHub with `git ls-tree -r --name-only origin/main <path>`. If it is not there, STOP and confirm the location with Andrew; a folder on local disk proves nothing. **Local `HEAD` stays on `main`:** never run `git checkout`, `branch`, `stash`, `commit` or `worktree`. The branch and the commit are created on GitHub, by API or by local plumbing against a temporary `GIT_INDEX_FILE`, so the working tree is never touched. Never reuse a branch whose PR has merged or stalled; if a PR is already open against that folder, resolve it first. Full text in `protocols/file-home-gate.md`.

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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
