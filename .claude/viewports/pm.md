# PM VIEWPORT
# Non-negotiable strategic context layer for all scoping, planning, and delivery governance tasks.
# This viewport can be combined with CMO and/or CTO viewports when the task requires multiple lenses.

---

## WHAT THIS IS

This viewport is the scope and delivery context layer that governs WHAT gets built and WHEN.
It does not tell you what steps to follow (that's the identity SOP).
It does not give you domain knowledge (that's the skills).
It tells you WHAT MATTERS — what's in scope, what's out, what success looks like, what the milestones are, and how to verify the work stays within boundaries.

Without this viewport loaded, work expands without control. Features creep in. Scope shifts silently. "Just one more thing" becomes the operating mode. The output might be good — but it's not what was agreed.

You do not skip steps. You do not reorder steps.
You load context before scoping. You lock scope before building.
You do not produce deliverables until Steps 1–3 are complete and confirmed.

---

## WHEN THIS VIEWPORT APPLIES

Load this viewport when the task involves ANY of:
- New project scoping (greenfield or new phase of existing project)
- MVP definition, acceptance criteria, or milestone planning
- PRD writing or technical specification
- Project recovery, re-scoping, or realignment
- Multi-session work that needs tracked progress
- Any task where scope boundaries matter

This viewport stacks with CMO (for market-facing scope decisions) and CTO (for technical feasibility and architecture governance).

---

## STEP 1 — LOAD PROJECT CONTEXT

Before anything else, understand the project landscape:

- **Prior work** — Check `projects/<name>/` for existing SOWs, LOGs, REPORTs
- **Existing specs** — PRDs, briefs, user stories, requirements docs
- **Entity context** — If scoping for a client, load from `protocols/entity-repo-map.md`
- **Constraints** — Budget, timeline, team size, platform restrictions, compliance requirements
- **Stakeholders** — Who decides? Who builds? Who uses it?
- **Current state** — What exists today? What's working? What's broken?

If this is a continuation of prior work, read the most recent SOW and LOG before proceeding. What was decided? What was deferred? What changed?

**Confirm:**
> STEP 1 COMPLETE — Project context loaded:
> - Project: [name]
> - Prior work: [SOW dates + key decisions, or "clean start"]
> - Constraints: [budget, timeline, platform, team]
> - Stakeholders: [who decides, who builds, who uses]
> - Current state: [what exists today]
> - Files read: [list with paths]
> - Gaps: [what's missing — no spec? no budget? no timeline?]

---

## STEP 2 — LOAD SCOPING LENSES

Load and internalise the relevant scoping skill files. These help you THINK about scope — what to include, what to exclude, and how to structure delivery.

Typical scoping lenses for PM viewport:
- `product/product-manager-toolkit` — outcome definition, success metrics, RICE
- `product/prd-builder` — MVP scope, acceptance criteria, PRD structure
- `frontend/senior-fullstack` — technical feasibility validation
- `knowledge-bank/product-management.md` — product strategy theory (on demand)
- `knowledge-bank/strategy-foundations.md` — strategic scoping (on demand)

These are not templates. They are lenses.
Scope is governed by outcomes — not by features.
You do not include a feature because it seems useful. You include it because it serves a measurable outcome within the agreed constraints.

**Confirm:**
> STEP 2 COMPLETE — Scoping lenses loaded: [list files read]

---

## STEP 3 — SCOPE ANALYSIS (REQUIRED BEFORE ANY WORK)

Complete all six points. Do not abbreviate. Do not skip.
This is the scope foundation for the task. It will be written to the SOW before work begins.

### 3.1 — Outcome
One sentence. What is the business outcome this project must produce?
Not what we're building — what changes when it's built.
Not "build a dashboard" — "give the team visibility into pipeline health so they can forecast revenue."

### 3.2 — User Value
Who benefits and how? For each user type:
- What can they do after this that they can't do now?
- What pain does this remove?
- How will we know they're getting value? (Observable behaviour, not survey)

### 3.3 — MVP Boundary
What is IN scope:
- [Feature/deliverable 1] — serves [outcome]
- [Feature/deliverable 2] — serves [outcome]

What is explicitly OUT of scope:
- [Feature/deliverable A] — deferred because [reason]
- [Feature/deliverable B] — not needed for [outcome]

The out-of-scope list is as important as the in-scope list. Unlisted items default to OUT.

### 3.4 — Constraints Register
| Constraint | Impact | Mitigation |
|---|---|---|
| [Budget: $X] | [limits scope to Y] | [prioritise core features] |
| [Timeline: N weeks] | [limits iterations] | [MVP first, iterate post-launch] |
| [Platform: must run on X] | [restricts tech choices] | [use Y framework] |
| [Compliance: must meet Z] | [adds review steps] | [build compliance into workflow] |

### 3.5 — Success Criteria
How do we know this is DONE? Specific, verifiable criteria:
- [Criterion 1] — how to verify
- [Criterion 2] — how to verify
- [Criterion 3] — how to verify

These are not aspirational. They are binary: met or not met.
If you cannot verify a criterion — it's not a criterion, it's a wish.

### 3.6 — Milestones & Decision Gates
Break the work into phases with gates:

| Milestone | Deliverable | Gate (what must be true to proceed) |
|---|---|---|
| M1: [name] | [what's delivered] | [what's verified before moving on] |
| M2: [name] | [what's delivered] | [what's verified] |
| M3: [name] | [what's delivered] | [final acceptance criteria] |

Each gate is a decision point. Do not proceed past a gate without verification.

---

After completing 3.1–3.6, write this analysis into the SOW.
It must exist before any deliverables are produced.

**Confirm:**
> STEP 3 COMPLETE — Scope analysis written to SOW.
> Ready to begin execution within defined boundaries.

---

## STEP 4 — DELIVERABLE GOVERNANCE

Before execution begins, confirm how each deliverable maps to scope:

| Deliverable | Outcome it serves (from 3.1) | Milestone (from 3.6) | Acceptance criteria (from 3.5) |
|---|---|---|---|
| [name] | [which outcome] | [which milestone] | [how verified] |

A deliverable without an outcome is scope creep waiting to happen.
Every deliverable must trace back to the outcome. If it can't — cut it.

**Confirm:**
> STEP 4 COMPLETE — Deliverables governed: [list]
> Proceeding to execution within scope boundaries.

---

## STEP 5 — SCOPE CHECKS (DURING AND AFTER EXECUTION)

As work proceeds, run these checks continuously.

### 5.1 — Outcome Alignment
Does the current work serve the outcome defined in 3.1?
Is any work happening that doesn't map to an outcome? That's scope creep — log it as a future item, don't do it now.

### 5.2 — User Value Delivery
Are we building what users actually need (3.2)?
Or are we building what's technically interesting?
Can we demonstrate the user value at each milestone?

### 5.3 — MVP Boundary Integrity
Has anything from the OUT list (3.3) crept into the work?
Has the scope expanded without a conscious decision?
If scope changed — was the SOW updated and re-approved?

### 5.4 — Constraint Adherence
Are we still within the constraints (3.4)?
Is the timeline holding? Is the budget holding?
If constraints shifted — flag it before it becomes a surprise.

### 5.5 — Success Criteria Tracking
Can we still meet the success criteria (3.5)?
Which criteria are on track? Which are at risk?
If a criterion is unachievable — flag it now, not at delivery.

### 5.6 — Milestone Progress
Are we progressing through milestones (3.6)?
Did each gate get verified before proceeding?
Or did we skip gates and keep building?

---

## STEP 6 — PM AUDIT (BEFORE DELIVERY)

After work is complete, run the PM audit before delivering.

Ask: *If the project sponsor reviewed this cold — with no context about the process, just the deliverables — would they say "this is what I asked for"?*

| Check | Pass condition |
|---|---|
| **Scope drift** | All deliverables map to the agreed scope. Nothing was added without approval. Nothing agreed was dropped without communication. |
| **Outcome delivery** | The business outcome defined in 3.1 is served by the deliverables. Not "we built features" — the OUTCOME is achievable. |
| **Constraint compliance** | Work stayed within budget, timeline, and platform constraints. No surprises. |
| **Success criteria** | Every criterion from 3.5 can be verified. Not "we think it works" — it demonstrably meets the criteria. |
| **Gate integrity** | Every milestone gate was verified before proceeding. No gates were skipped. |
| **Documentation** | SOW exists. LOG exists. Report will be written. The project trail is clean. |

If any check fails: return to the relevant step, resolve, and re-audit.
Do not deliver work that fails audit. Fix it or flag it.

**Confirm:**
> PM AUDIT: [PASS / FAIL — with notes on any adjustments]

---

## FAILURE MODES

| Failure mode | What it looks like | Which step prevents it |
|---|---|---|
| **Scope creep** | "While we're at it, let's also..." without updating the SOW | Step 3.3 — MVP boundary must be explicit. Step 5.3 checks integrity. |
| **Feature-first scoping** | "We need a dashboard, a settings page, and an API" before defining the outcome | Step 3.1 — outcome first, features second |
| **Missing constraints** | "We didn't know about the deadline" | Step 3.4 — constraints must be surfaced and documented |
| **Skipped gates** | Proceeding to M2 without verifying M1 is actually done | Step 3.6 — gates are mandatory. Step 5.6 tracks progress. |
| **Unmeasurable success** | "The user should have a good experience" | Step 3.5 — criteria must be specific and verifiable |
| **Invisible progress** | No LOG, no SOW, no report. "Trust me, it's done." | Step 6 — documentation check. The paper trail IS the proof. |
| **Decoration** | "The PM lens says define scope" then building whatever feels right | Step 3 analysis must be WRITTEN. Step 5 checks must be RUN. Step 6 audit must PASS. |

---

## COMBINING WITH OTHER VIEWPORTS

When PM viewport stacks with CMO or CTO:

- **PM + CMO** (e.g., marketing project): PM governs scope, milestones, and delivery boundaries. CMO governs strategic quality (ICP alignment, positioning, copy quality). PM audit checks scope adherence. CMO audit checks output quality.

- **PM + CTO** (e.g., technical build): PM governs scope, milestones, and acceptance criteria. CTO governs architecture, code quality, and technical decisions. PM audit checks scope adherence. CTO audit checks technical quality.

- **PM + CMO + CTO** (e.g., full product build): All three. PM owns scope and delivery governance. CMO owns brand/ICP context and messaging quality. CTO owns architecture and code quality. Each viewport's analysis, checks, and audit run independently. All must pass.

Viewports do not conflict. They see the same work through different lenses. If a viewport check fails, the work has a problem — not the viewport.
