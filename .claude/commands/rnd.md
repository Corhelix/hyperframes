---
name: rnd
description: R&D Tax Offset Capture.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - R&D tax offset capture, or new scope and stack investigation
  does_not_fire_when:
    - the stack decision is settled and needs building -> /cto
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: finding
      is: the claim, its evidence, and whether it is eligible or in scope
    - id: record
      is: the dated record the offset claim or stack decision rests on
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- slash-commands/rnd.md is canonical; .claude/commands/rnd.md must match exactly | Workflow: research-pass.workflow.json | Mode: RnD -->
# /rnd — R&D Tax Offset Capture

You are the R&D Documentation Lead. This command captures ATO-eligible R&D activity from a work session — technical uncertainties explored, hypotheses tested, experiments run, and evidence produced. This feeds directly into the FY 2025-2026 R&D tax offset claim.

**This is not a session report.** Run `/report` for the session log. Run `/rnd` when the session involved genuine technical uncertainty.

5 phases: context → eligibility → capture → evidence → file.

---

## Phase 1 — CONTEXT

### Step 1.1 — Load R&D framework

Read the ATO R&D Framework overlay: `identities/overlays/ato-rnd-framework.md`

Read the R&D Registry: `projects/rnd/RND-REGISTRY.md`

**GATE — present for confirmation:**
> R&D capture: [activity] | Entity: [name] | Period: [dates]. Correct?

Wait for response.

### Step 1.2 — Identify the project

Ask:
1. **Which R&D project does this session belong to?** (Check the registry for active projects)
2. **Is this a new R&D project?** (If yes, it needs a project entry in the registry)

If the project already has an existing thesis/overview doc (like `projects/rnd/WolfEagle_RD_Project_Overview_2025-2026.md`), read it for the existing uncertainty register.

---

## Phase 2 — ELIGIBILITY CHECK

Think through whether this session's work qualifies:

**R&D-eligible** = work where the outcome was genuinely unknown at the start. You were:
- Trying an approach where you didn't know if it would work
- Experimenting to solve a problem that existing tools/knowledge couldn't solve
- Building something where the method, architecture, or feasibility was uncertain
- Testing whether an AI/automation approach could achieve a specific quality/accuracy/cost threshold

**Not R&D** = routine work with known solutions:
- Implementing a feature against a clear spec with established patterns
- Copy production using known frameworks
- Bug fixes with known root causes
- Configuration, admin, project management

**The ATO test:** Could a competent professional in the field have predicted the outcome with reasonable confidence before starting? If yes → not R&D. If no → R&D.

If the session wasn't R&D-eligible, say so: "This session was routine [implementation/production/maintenance]. No R&D activity to capture. Run `/report` for the session log."

---

## Phase 3 — CAPTURE

### Step 3.1 — Technical Uncertainty

What was genuinely uncertain? Be specific — not "will this work" but the exact technical question.

```
TECHNICAL UNCERTAINTY:
[The specific question that couldn't be answered from existing knowledge, tools, or methods.]

Example: "Whether a single Claude prompt chain could maintain factual accuracy
across 15+ persona-specific content variants without hallucinating school-specific
details not present in the input data."

WHY THIS WAS UNCERTAIN:
[Why existing knowledge wasn't sufficient. What made this non-routine.]

Example: "No documented method existed for constraining LLM output to entity-specific
facts across multiple persona variations while maintaining natural language quality.
Standard prompt engineering techniques (system prompts, few-shot examples) had not
been tested at this variation count with this accuracy requirement."
```

### Step 3.2 — Hypothesis

```
HYPOTHESIS: [What we expected to find / what approach we thought would work]

TEST METHOD: [How we tested — what was built, what was measured, what data was used]

RESULT: [VALIDATED / INVALIDATED / INCONCLUSIVE / PARTIALLY VALIDATED]

LEARNING: [What we now know that we didn't before. Be specific.]
```

If multiple hypotheses were tested in one session, capture each separately.

### Step 3.3 — Experiment Log

| # | Date | What was tried | Approach | Result | Key learning |
|---|------|---------------|----------|--------|-------------|
| 1 | [YYYY-MM-DD] | [specific experiment] | [method] | [worked / failed / partial] | [what we learned] |
| 2 | ... | ... | ... | ... | ... |

---

## Phase 4 — EVIDENCE

### Step 4.1 — Link evidence artifacts

```
EVIDENCE:
- Commits: [list git commit hashes that demonstrate the R&D activity]
- Files: [list files created/modified as part of the experiment]
- Test results: [any measurable output — accuracy rates, performance metrics, error rates]
- Logs: [session logs, build logs, test output that shows the experiment]
```

### Step 4.2 — Time allocation

```
TIME ESTIMATE:
- Total session: [hours]
- R&D-eligible activity: [hours] — [description of what was R&D]
- Routine (BAU) activity: [hours] — [description of what was not R&D]
```

Be honest about the split. Not all time in an R&D session is R&D. Setup, configuration, known-solution implementation is BAU even if it happens during an R&D session.

### Step 4.3 — R&D vs BAU separation

```
R&D ACTIVITY (eligible):
[The experimentation, uncertainty resolution, hypothesis testing, novel approach development]

BAU ACTIVITY (not eligible):
[Routine implementation, known-solution work, configuration, admin, copy production]
```

---

## Phase 5 — FILE

### Step 5.1 — Save the R&D record

Save to: `projects/rnd/<project-name>/DRAFT-v0.1-YYYY-MM-DD-RND.md`

If the project folder doesn't exist in `projects/rnd/`, create it.

### Step 5.2 — Update the registry

Read `projects/rnd/RND-REGISTRY.md`. Update:
- Evidence quality rating (Strong / Partial / Minimal) if it changed
- Last activity date
- If new project: add entry with project name, description, and initial evidence quality

### Step 5.3 — Update hypothesis tracker (if exists)

If the project has a `_HYPOTHESIS_TRACKER.md` (like the More Than Marks project), update it with the hypothesis result from Phase 3.

---

## Output format

The R&D record should be structured as:

```
# R&D Activity Record
Date: [YYYY-MM-DD]
Project: [name from registry]
Session: [brief description]

## Technical Uncertainty
[from Phase 3.1]

## Hypothesis & Result
[from Phase 3.2]

## Experiment Log
[from Phase 3.3]

## Evidence
[from Phase 4.1]

## Time Allocation
[from Phase 4.2]

## R&D vs BAU
[from Phase 4.3]

## Registry Update
- Evidence quality: [unchanged / upgraded to X]
- Hypothesis tracker: [updated / N/A]
```

---

## Reference

- **ATO R&D Framework:** `identities/overlays/ato-rnd-framework.md`
- **R&D Registry:** `projects/rnd/RND-REGISTRY.md`
- **Working example:** `projects/rnd/More than Marks/_SESSION_MASTER/2026-02-02/`
- **W&E R&D Thesis:** `projects/rnd/WolfEagle_RD_Project_Overview_2025-2026.md`

---

## What this command does NOT do

- Write a general session report (use `/report`)
- Produce code, copy, or specs (use `/cmo`, `/cto`, `/build`)
- Assess whether a project qualifies for R&D at a program level (that's the ATO overlay + accountant)
- This captures per-session R&D evidence. The ATO claim is assembled from these records at tax time.

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
