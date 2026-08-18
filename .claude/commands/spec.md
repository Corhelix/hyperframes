---
description: Produce a technical specification or PRD.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/spec.md — .claude/commands/spec.md must match exactly -->
# /spec — Produce a technical specification or PRD

Define what needs to be built, how it should work, and what done looks like. Produces a structured spec that governs downstream build work.

---

## Canonical output scaffold (MANDATED)

Specs are decision-bearing — requirements, open questions, acceptance criteria, scope items all become rows Andrew has to stamp LOCK / REVISE / DROP / DEFER. **Always start the HTML output from `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`** (modules + Decision Register + Archive section + tagging UI). Never hand-write the brand CSS or invent a layout — copy from the canonical and fill placeholders. ID convention: `S1`, `S2`, ... for sections; `D1`, `D2`, ... for design decisions; `T1`, `T2`, ... for tasks/requirements; `Q1`, `Q2`, ... for open questions.

If the canonical is missing, STOP and ask. See `alc-group/brand-ops/templates/README.md` for selection rules.

> **Landscape Module Doctrine (AUTHORITY 2026-06-10):** the spec's stamping surface stays the decision-tagging pattern above. But any *presented* read-and-deliver summary of the spec (an exec walk-through, a stakeholder briefing) is built as fixed 1920×1080 landscape modules off `protocols/templates/LANDSCAPE-MODULE-TEMPLATE.html`, rendered via the user's native Print → Save as PDF. Module schema: `protocols/landscape-module-schema.md`.

---

## MCP Tools Available

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Context7** (`mcp__context7__*`) | Step 2 (Load context), Step 3.4 (Integration points) | Pull current docs for any library or platform API the spec will name. Verify endpoints exist in the installed version BEFORE locking spec rows. Hallucinated APIs in a spec produce builds that fail at compile time |
| **Supabase** (`mcp__supabase__*`) | Step 3.4 (Integration points), data model rows | Inspect actual schema + RLS on existing Supabase repos. Spec data model rows must match reality. Read-only |

**Rule:** every `T` (task/requirement) row that names a library or platform API must trace to a Context7 verification in this session, or be stamped `Q` (open question) for verification before the next stage.

---

## Procedure

### Step 1 — Establish scope

Ask (if not already clear):
1. **What are you building?** (feature, app, workflow, integration, API, page)
2. **Is there an existing codebase?** If yes, what's the path?
3. **What's the desired outcome?** (not features — what should users be able to DO?)
4. **Any constraints?** (tech stack, timeline, budget, existing commitments, platform limits)
5. **Is there an entity involved?** (if building for a brand, entity context governs design tokens and copy)

**GATE — present for confirmation:**
> Specifying: [what] | Codebase: [path or new] | Entity: [name or none]. Correct?

Wait for response.

### Step 2 — Load technical context

If there's an existing codebase: read the project structure, key files, existing patterns, package.json, config files. Understand what's already built and how.

If an entity is involved: read `protocols/entity-repo-map.md` → load brand context for design tokens, copy guidelines.

If `/strategise` was already run this session, use that strategic context.

### Step 3 — Technical analysis (answer all 6)

Write each answer out. These form the spec.

**3.1 — User journey**
Who uses this? Map the critical flows end-to-end:
- Entry point → key actions → success state
- What data do they need to see?
- What actions do they need to take?
- What happens when things go wrong?

**3.2 — Architecture decisions**
What's the system architecture and why?
- Tech stack rationale (not just "React + Supabase" — WHY for this project)
- Data model and relationships
- Auth model and session management
- State management approach
- API contract patterns

Document trade-offs, not just choices.

**3.3 — Existing patterns**
What patterns already exist? (If greenfield, define the patterns to establish)
- Component structure and naming
- Data fetching approach
- Error handling patterns
- Styling approach
- Test patterns

New code MUST follow existing patterns unless there's an explicit decision to change them.

**3.4 — Integration points**
What external systems does this touch?
- APIs: endpoints, auth, rate limits, payload schemas
- Databases: tables, RLS policies, migrations
- Workflows: n8n/Trigger.dev tasks, webhooks, events
- Third-party services: what can fail, fallbacks

Map the data flow through each integration.

**3.5 — Risk and failure modes**
What can go wrong?
- API down? Auth failure? Bad data? Performance bottleneck? Security surface?
- For each risk: what's the mitigation?

**3.6 — Definition of done**
What does "complete" look like? Must be specific and verifiable.
- Functional requirements (what it must DO — list each)
- Quality requirements (builds clean, no console errors, responsive, accessible)
- Test requirements (what must be tested and how)
- Documentation requirements (what must be documented)

### Step 4 — Output the spec

Present as a structured document:

```
# [Project/Feature Name] — Technical Spec

## Overview
[One paragraph: what this is, who it's for, what outcome it produces]

## User Journey
[From 3.1]

## Architecture
[From 3.2 — include a simple diagram if helpful]

## Existing Patterns
[From 3.3]

## Integration Points
[From 3.4]

## Risks & Mitigations
[From 3.5]

## Definition of Done
[From 3.6 — as a checklist]

## Out of Scope
[Explicitly: what this spec does NOT cover]
```

### Step 5 — Self-check before delivering

| Check | Pass condition |
|-------|---------------|
| **Outcome-driven** | Spec defines what users can DO, not just what gets built |
| **Trade-offs documented** | Architecture decisions explain WHY, not just WHAT |
| **Patterns respected** | If existing codebase, new work follows its conventions |
| **Definition of done is verifiable** | Each criterion can be demonstrated, not asserted |
| **Risks are real** | Not hypothetical — specific to this system |

---

## Output location

Save to: `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/DRAFT-v0.1-YYYY-MM-DD-SPEC.md`

---

## Chains to

- `/plan` — to break the spec into milestones and a SOW
- `/build` — to execute against this spec
- `/review CTO` — for full-depth CTO viewport analysis

---

## What this command does NOT do

- Write code (use `/build`)
- Marketing strategy (use `/strategise`)
- Audit existing code (use `/audit`)
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
