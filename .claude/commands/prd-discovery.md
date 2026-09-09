---
name: prd-discovery
description: PRD Stage 1: Problem, Market & User.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a new module's problem, market and user are established
  does_not_fire_when:
    - the problem is already settled and journeys are next -> /prd-ux
  loads:
    always: []
    skills:
      - knowledge-bank/marketing-and-gtm.md
      - knowledge-bank/strategy-foundations.md
  returns:
    - id: problem
      is: the problem, the market and the user, in the user's own language
    - id: assumptions
      is: what must be true for this to be worth building, stated so it can be tested
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
