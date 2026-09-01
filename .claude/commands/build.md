---
description: Execute a build against an approved plan or spec.
argument-hint: "[context or target]"
---
<!-- slash-commands/build.md is canonical; .claude/commands/build.md must match exactly | Workflow: plan-and-build.workflow.json | Phase: build -->
# /build — Execute a defined build task

Write code, build workflows, or implement configurations against an existing spec, plan, or clear task definition. This command produces working output — not plans.

---

## MCP Tools Available

This command has access to the following MCP servers. Use them — do not narrate availability.

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Context7** (`mcp__context7__*`) | Step 2 (Load context), Step 4 (Build) | Pull current docs for any library API you are about to call. Use BEFORE writing the call, not after it fails |
| **Supabase** (`mcp__supabase__*`) | Step 4 (Build) for DB-touching code, Step 5 (Verify) | Inspect schema + RLS before writing queries. Verify writes landed after building. Read-only by default |
| **Playwright** (`mcp__playwright__*`) | Step 5 (Verify) for UI output | Snapshot the rendered output, grade against the canonical template (CLARITY OS / W&E per `alc-group/brand-ops/templates/README.md`), fix and re-snapshot until clean. Replaces the manual "open the HTML and eyeball it" check |

**Self-grading loop (UI work):** after writing UI code or HTML, take a Playwright snapshot, compare against the canonical template that applies, list any deviations as a fix list, apply fixes, re-snapshot. Loop until clean before declaring done.

---

## Procedure

### Step 1 — Establish what to build

Ask (if not already clear):
1. **What are you building?** (feature, fix, workflow, integration, page)
2. **Is there a spec or plan?** (from `/spec` or `/plan` — use it as the governing document)
3. **What's the codebase?** (path to the project)
4. **What specifically should be done in this session?** (scope — not "build the whole app" but "implement the auth flow")

If there's no spec and the task is non-trivial, suggest running `/spec` first:
> "This looks like it needs a spec before building. Run `/spec` first?"

For small, well-defined tasks (bug fix, add a field, update a component), proceed without a spec.

**GATE — present for confirmation:**
> Building: [what] | Codebase: [path] | Spec: [reference]. Correct?

Wait for response.

### Step 2 — Load technical context

Read the codebase:
- Project structure (ls key directories)
- Package.json / config files (understand the stack)
- Existing patterns (how routes, components, data fetching, error handling work)
- Any relevant existing files for the area being modified

If an entity is involved (brand design tokens, copy), load entity context from `protocols/entity-repo-map.md`.

### Step 3 — Confirm approach (before writing code)

State in 3-5 lines:
- **What** you're going to build
- **Where** the changes go (which files, new or modified)
- **How** it follows existing patterns
- **What** could go wrong

Get confirmation before writing code. This replaces the full SOW — it's a lightweight scope check.

### Step 3a — UX first, when the task has screens

**If the task touches a user-facing surface, this step is mandatory and Step 4 cannot start without it.** A task that is purely a data migration, a script or a backend contract skips it, and says in one line that it skipped it and why.

Three artefacts, in this order, before a line of product code:

1. **The screens.** Every screen the task touches, each with its five states: empty, loading, populated, error, edge. Each one names the journey and step that reaches it. A screen nothing reaches is an orphan, and a step with no screen means the list is short.
2. **The journeys, written click by click,** in the words a person would use. Not "the user configures the import", but "the user clicks Import in the side nav, a selector panel opens, they choose a file, the filename appears beside Continue, they click Continue and land on the mapping screen with that filename in its header". Every gesture is numbered and carries an observable success criterion, something a person could watch being true or false, plus the thing it passes forward to the next screen, named as the thing itself rather than its category. `nothing` is a valid handoff and is written rather than left blank.
3. **Unbranded clickable shells.** Cheapest medium that clicks: plain static HTML with one shared chrome partial, or route stubs inside the app's real layout. System font, one grey, one accent on the thing being clicked. No palette, no logo, no imagery, no spacing polish. **The chrome is lifted from the running app, never approximated:** every shell sits inside the product's real header and side nav with the current item marked, because an isolated screen floating on white proves nothing about where the gesture lives. Then drive them in a browser and walk every journey by hand.

Confirm the shells with the operator, then build to them. The shells are the specification: a departure from a shell is a recorded decision with the shell updated in the same turn, never a silent improvement. Style comes last, after the behaviour works, as its own pass.

### Step 4 — Build

Write the code. During implementation, check:

- [ ] **Pattern compliance** — follows existing codebase conventions. Same naming, same data fetching, same error handling.
- [ ] **No competing patterns** — don't introduce a new way of doing something that already has an established pattern.
- [ ] **Error handling** — not just the happy path. What happens with bad data? Failed API calls? Auth issues?
- [ ] **Security** — no hardcoded secrets. Input validated at boundaries. Auth enforced where needed.
- [ ] **Completeness** — not skeleton code. No "TODO" comments, no placeholder pages, no "coming soon."

### Step 5 — Verify

After building:
1. Does it build without errors?
2. Does it render / run correctly?
3. Are there console errors or warnings?
4. Does it handle the edge cases identified in Step 3?

If there are tests: run them. If tests should be written: write them.

### Step 6 — Self-audit before delivering

| Check | Pass condition |
|-------|---------------|
| **Pattern compliance** | All new code follows existing codebase patterns |
| **No over-engineering** | Complexity matches the problem. No abstractions for hypothetical needs. |
| **No under-engineering** | Error handling exists. Validation exists. Edge cases covered. |
| **Architecture respected** | Data flows through intended layers. No shortcuts. |
| **It works** | Demonstrably works — not "should work." Build passes. Functions run. |

### Step 7 — Deliver

Present:
- What was built (summary)
- Files created or modified (list)
- How to test it (specific steps)
- Any known limitations or follow-up items

---

## Output location

Save build artefacts (specs, notes, implementation docs) to:
`projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/DRAFT-v0.1-YYYY-MM-DD.md`

When approved: `APPROVED-YYYY-MM-DD.md`

---

## Chains to

- `/audit` — to audit the code quality
- `/review CTO` — for full-depth CTO viewport analysis
- `/report` — to document what was built

---

## What this command does NOT do

- Write specs (use `/spec`)
- Marketing copy (use `/draft`)
- Strategic analysis (use `/strategise`)
- Full architecture review (use `/audit` or `/review CTO`)
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
