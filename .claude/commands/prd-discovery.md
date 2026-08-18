---
description: PRD Stage 1: Problem, Market & User.
argument-hint: "[context or target]"
---
<!-- slash-commands/prd-discovery.md is canonical; .claude/commands/prd-discovery.md must match exactly | Workflow: prd-assembly.workflow.json | Phase: discovery -->
# /prd-discovery — PRD Stage 1: Problem, Market & User

You are the Product Lead. This is the first of 3 stages that produce a buildable PRD. This stage answers: **who is this for, what problem does it solve, and why would they switch?**

This stage combines the CMO lens (ICP, switching dynamics, competitive frame) with the PM lens (outcome, constraints, scope boundary). It produces PRD-1-DISCOVERY.md — the foundation that Stage 2 and Stage 3 build on.

5 phases: context → task → skills → execute → quality gate.

---

## Rationalisations

<!-- Source: addyosmani/agent-skills · MIT
     skills/test-driven-development/SKILL.md @ f17c6e8 (vendored 2026-05-18)
     Pattern lifted: "Common Rationalizations" two-column table.
     Content adapted to /prd-discovery phases (problem / market / user). -->

Common excuses for skipping Stage 1 rigour, with rebuttals. If you catch yourself thinking one of these — stop.

| Thought | Reality |
|---|---|
| "The user described the problem, I have enough." | Switching dynamics aren't in the brief. Ask. |
| "Market is obvious for this category." | Competitive frame requires named alternatives. "Fragmented competition" is not a competitor. |
| "Scope can flex into Stage 2." | UX drift starts in scope drift. Lock the boundary before `/prd-ux`. |
| "Outcome is implied." | Implied outcome = unmeasured outcome. State what changes when this ships. |
| "I'll write narrative, structure can come later." | PRD-1 carries decision tags. Narrative goes inside structure, not instead of. |
| "Stage 1 is the discovery phase, I can speculate." | Speculation labelled as discovery becomes locked context for Stage 2 + 3. Mark unknowns as `Q`. |

## Red Flags

Stop signs. Do not advance to Stage 2 if any of these is true.

- Problem statement without LOCK status from Andrew
- Competitive frame with zero named alternatives
- Outcome stated as a feature ("ships a dashboard")
- Scope written as wishlist, not boundary (in / out / deferred)
- Switching force untested ("they want a better tool")
- Discovery claim about a competitor or platform without a Playwright snapshot or Context7 fetch in the same session (must stamp `Q`)

---

## MCP Tools Available

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Context7** (`mcp__context7__*`) | Phase 1.2 (Load context) when researching market, competitors, platform constraints | Pull current docs / specs / official references for any platform the discovery names (eg. WordPress block patterns, Shopify capabilities, GHL custom fields). Stops discovery rows from naming behaviours that no longer exist |
| **Playwright** (`mcp__playwright__*`) | Phase 1.2 for competitive context | Snapshot competitor sites + own brand surfaces to ground the switching-dynamics analysis in observed reality, not assumed state |

**Rule:** any discovery claim about a competitor's current behaviour or a platform's capability must trace to a Playwright snapshot or Context7 doc fetch in this session — otherwise stamp as `Q` (open question) for verification before Stage 2.

---

## Phase 1 — CONTEXT

### Step 1.1 — Identify the product

Ask:
1. **What are you building?** (product, feature, platform, tool)
2. **Who is it for?** (entity, ICP, internal team, external users)
3. **Is there prior work?** (existing codebase, previous PRDs, strategy docs)

### Step 1.2 — Load context

If entity involved: `protocols/entity-repo-map.md` → load ALL files. ICP profiles, positioning, switching dynamics, competitive landscape.

Check `projects/<name>/` for existing SOWs, LOGs, specs.

If codebase exists: read project structure to understand what's already built.

### Step 1.3 — Context checkpoint

```
THE PRODUCT: [what — one sentence]
THE USER: [who — emotional/situational state in their language]
THE MARKET: [competitive context — what they're comparing against]
PRIOR WORK: [what exists, what's been decided]
```

**GATE — present for confirmation:**
> PRD Discovery: [product] | Entity: [name or none] | Market: [target]. Correct?

Wait for response.

---

## Phase 2 — TASK

Ask (if not clear):
1. **What triggered this?** (new product, feature request, pivot, competitive pressure)
2. **What's the desired outcome?** (not features — what changes when this ships)
3. **What constraints?** (budget, timeline, team, platform, compliance)

Think through as the Product Lead:
- Who is this person right now? What are they struggling with?
- What have they tried? What failed and why?
- What's driving them away from their current solution (push)?
- What's attracting them here (pull)?
- What habits work against adoption?
- What anxiety could kill the decision?
- What alternatives exist? How is this actually different?

---

## Phase 3 — SKILLS

Propose skills from:
- `digital-marketing/product-marketing-context/SKILL.md` — ICP, switching dynamics
- `digital-marketing/competitor-alternatives/SKILL.md` — competitive framing
- `knowledge-bank/marketing-and-gtm.md` — GTM, market analysis
- `knowledge-bank/strategy-foundations.md` — competitive strategy
- `product/product-manager-toolkit.md` — outcome definition, RICE
- `product/prd-builder.md` — PRD structure

**Ask:** "These are the skills I'd use. Add, remove, or swap?"

---

## Phase 4 — EXECUTE

Write **PRD-1-DISCOVERY.md** with these sections:

### 1. Problem Statement
- **The user right now:** Who are they? What's their emotional/situational state? In their language, not yours. Quote real pain points if available.
- **What they've tried:** Previous solutions, workarounds, tools. What worked, what failed, and why.
- **The core problem:** One paragraph. The specific gap between what they need and what exists.

### 2. Switching Dynamics
- **Push:** What's making their current situation untenable? Be specific — not "frustration" but "spending 3 hours rebuilding context every new Claude session."
- **Pull:** What's the magnet? What would make them try this?
- **Habit:** What default behaviour works against adoption? What inertia must be overcome?
- **Anxiety:** What specific fear could kill the decision? The "yeah but..." that stops them.

### 3. Competitive Frame
- **Real alternatives** (what the ICP actually compares against — including "do nothing"):
  For each: what it does, where it falls short, why people stay anyway.
- **This product's position:** How is this different? Not a tagline — the structural advantage.

### 4. Product Outcome
- **Outcome:** What changes when this ships? One sentence.
- **User value:** What can they do after that they can't do now? Per user type.
- **Success metric:** The one number that tells you this worked. Specific, measurable.

### 5. Scope Boundary (high-level)
- **In scope:** Major capability areas (not features yet — that's Stage 2)
- **Out of scope:** What this explicitly does NOT include and why
- **Constraints:** Budget, timeline, platform, team, compliance

### 6. Open Questions
- What don't we know yet that would change these decisions?
- What needs validation before Stage 2?

---

## Phase 5 — QUALITY GATE

Read it as the Product Lead.

- Does the problem statement describe a real person in a real situation — or a market segment?
- Are switching dynamics specific enough to design against — or generic "pain points"?
- Is the competitive frame honest about what alternatives do well — or just a hit list?
- Is the outcome measurable — or aspirational?
- Would a developer reading this understand WHO they're building for and WHY?

Fix what fails. Deliver.

**Ask:** "Ready for Stage 2? Run `/prd-ux` to define user journeys and screen-level UX."

---

## Canonical output scaffold (MANDATED)

PRD-1 is decision-bearing — every problem statement, switching-dynamic, competitive frame becomes a row Andrew has to stamp LOCK / REVISE / DROP / DEFER. **Always start the HTML output from `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`** (modules + Decision Register + Archive section + tagging UI). Never hand-write the brand CSS or invent a layout.

ID convention: `D` decisions · `Q` open questions · `S` scope items · `R` risks.

If the canonical is missing, STOP and ask.

---

## Output location

Save to: `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/DRAFT-v0.1-YYYY-MM-DD-PRD-1-DISCOVERY.html` (HTML canonical, decision-tagging scaffold). No `.md` companion (per `feedback_everything_to_github_html_canonical`).

---

## Links to other stages

- **Stage 2:** `/prd-ux` — User journeys, screen inventory, all states, interaction design
- **Stage 3:** `/prd-build` — Architecture, data model, milestones, definition of done

---

## Core Writing Standard

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md` (canonical rule source: `skills/copywriting/Proofread-Anti-AI-Standard.md`).

Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene. Three or more AI-tell patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Core Writing Standard for the cross-phase enforcement protocol.

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
