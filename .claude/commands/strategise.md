---
description: Strategic analysis pass: diagnosis, guiding policy and coherent actions.
argument-hint: "[context or target]"
---
<!-- slash-commands/strategise.md is canonical; .claude/commands/strategise.md must match exactly | Workflow: frame-and-execute.workflow.json | Lens: Strategy -->
# /strategise — Strategic analysis for a brand entity

Produce a structured strategic analysis: ICP state, switching dynamics, positioning validation, competitive frame, funnel mapping. This is the thinking that governs all downstream work — copy, specs, campaigns.

This command is SELF-CONTAINED. It is the single authority when invoked.

---

## MCP Tools Available

Strategy is human reasoning, not MCP-driven analysis. MCPs are used only to verify facts the strategy depends on.

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Context7** (`mcp__context7__*`) | Anywhere the analysis cites a platform behaviour, library capability, or technical constraint | Verify the cited fact is current. A positioning conclusion that depends on "Platform X supports Y" must be Context7-verified before being locked |
| **Playwright** (`mcp__playwright__*`) | Competitive frame, funnel mapping when the analysis depends on live competitor surface state | Snapshot the actual page being analysed rather than relying on memory or assumed state |

**Rule:** strategy is reasoning, not retrieval. Use MCPs to verify, never to substitute for thinking. If you find yourself asking an MCP "what is the strategy here", you have drifted — go back to the strategic frame.

---

## Procedure

### Step 1 — Establish scope

Ask (if not already clear):
1. **What entity** is this for?
2. **What's the strategic question?**
3. **Which ICP(s)** are in scope?
4. **Any constraints?**
5. **Company brand work or client project work?**

**GATE — present for confirmation:**
> Entity: [name] | Type: [brand/client] | Question: [one line] | ICPs: [list]
> Correct?

Wait for response.

**After confirmation — route by type:**
- **Company brand work** → Read `protocols/cmo-our-brands.md` for persona lookup table and locked positioning statements.
- **Client project work** → Skip CMO-OUR-BRANDS. Load client context from `client-projects/`.

### Step 2 — Load and align entity context

Read `protocols/entity-repo-map.md` → load ALL files for the entity. Assess currency — APPROVED files take precedence over DRAFTs. Flag superseded files, do not absorb.

If critical files are missing (ICP, positioning), **stop and flag**.

**GATE — present for confirmation:**
> Loaded [N]/[total] files. Current: [list]. Superseded: [list or "none"]. Gaps: [list or "none"]. Confirm?

Wait for response.

### Step 3 — Load strategic lenses

Read these BEFORE analysis. They are HOW YOU THINK:
- `knowledge-bank/strategy-foundations.md` — competitive positioning, category design
- `knowledge-bank/marketing-and-gtm.md` — GTM architecture, positioning
- `skills/digital-marketing/product-marketing-context/SKILL.md` — switching dynamics, JTBD
- `skills/digital-marketing/competitor-alternatives/SKILL.md` — competitive framing
- `skills/copywriting/Proofread-Anti-AI-Standard.md` — applies to the strategy doc you produce

### Step 4 — Strategic analysis (complete all 6 points)

Write each answer out. Do not abbreviate. Do not skip.

**4.1 — ICP State Analysis**
For each ICP in scope:
- What are they feeling right now? (emotional state, not demographics)
- What situation are they in? (the trigger that makes them look)
- What language do they use to describe their problem? (from ICP files, not your words)
- What have they already tried? What failed?
- What do they believe is true that may be wrong?

**4.2 — Switching Dynamics**
For each ICP in scope, map all four forces:
- **Push:** What is driving them away from their current situation? Be specific — not "frustration" but "spending 3 hours a week on reports that nobody reads"
- **Pull:** What is attracting them toward this offer? What's the magnet?
- **Habit:** What inertia keeps them where they are? What default behaviour works against change?
- **Anxiety:** What specific fear or doubt could kill the decision? What's the "yeah but..."?

For each force: name the section of any downstream asset where it should be addressed.

**4.3 — Positioning Validation**
- State the current positioning (from positioning.md)
- Test it: Does it clearly differentiate from what the ICP is actually comparing against?
- Identify any positioning gaps: where the claim is strong but the evidence is weak
- Identify any positioning drift: where the brand is saying one thing but doing another

**4.4 — Competitive Frame**
- Who is the ICP actually comparing this to? (not who you think the competitors are — who the ICP considers alternatives)
- What does each alternative offer that this brand doesn't?
- What does this brand offer that no alternative does?
- Where is the brand vulnerable? Where is it strongest?

**4.5 — Funnel Mapping**
- Current funnel: traffic sources → landing experiences → conversion points → retention
- For each stage: what awareness level does the ICP have? What must shift?
- Where are the leaks? Where is the funnel strong?
- What's the next asset needed to fill the biggest gap?

**4.6 — Strategic Recommendations**
Based on 4.1-4.5:
- What is the single most important strategic move?
- What should be done first? (sequence matters)
- What should explicitly NOT be done yet? (scope boundary)
- What data or context is missing that would change these recommendations?

### Step 5 — Output the analysis

Present as a structured document with clear headers for each section (4.1-4.6). Include specific evidence from entity files — quote ICP language, cite positioning statements, reference knowledge passes.

### Step 6 — Self-check before delivering

| Check | Pass condition |
|-------|---------------|
| **Grounded in evidence** | Every claim traces to a specific entity file. No fabricated context. |
| **ICP language, not marketing language** | Descriptions use words from the ICP files, not polished abstractions |
| **Actionable** | Recommendations specify what to do, in what order, with what outcome |
| **Honest about gaps** | Missing data is flagged, not papered over |

---

## Output location

Strategic recommendations are decision-bearing. Save as `DRAFT-STRATEGY-v0.1-YYYY-MM-DD.html` using the canonical decision-tagging scaffold (`../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`) so each recommendation is a stamp-able row (LOCK / REVISE / DROP / DEFER). ID convention: `D` decisions · `R` risks · `Q` open questions · `S` scope boundaries.

Location: `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/`. When approved: `APPROVED-YYYY-MM-DD.html`. HTML is canonical, no `.md` companion (per `feedback_everything_to_github_html_canonical`).

---

## Chains to

- `/cmo` — to produce copy governed by this strategic analysis
- `/spec` — to produce a technical spec informed by this strategy
- `/plan` — to scope a project based on strategic recommendations
- `/review CMO` — for full-depth CMO viewport analysis on top of this

---

## What this command does NOT do

- Produce copy or creative output (use `/cmo`)
- Build software (use `/spec` → `/build`)
- Audit existing copy (use `/audit-cmo`)
- Audit existing code (use `/audit-cto`)
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
