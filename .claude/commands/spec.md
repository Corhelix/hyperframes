---
name: spec
description: Produce a technical specification or PRD.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a technical specification or PRD is the deliverable
  does_not_fire_when:
    - the work is a build against an existing spec -> /build
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: spec
      is: schemas, payloads and contracts defined before implementation
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
