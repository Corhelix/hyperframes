---
name: ui-cloner
description: Reverse-engineer any web page into a brand-aligned replication prompt.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - an existing UI is reproduced from a reference
  does_not_fire_when:
    - the design is original rather than reproduced -> /cto with the frontend skills
  loads:
    always: []
    skills:
      - skills/ui-cloner/references/iterator.md
  returns:
    - id: reproduction
      is: the built UI, with the reference it was matched against
    - id: divergences
      is: where it deliberately differs from the reference, and why
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: slash-commands/ui-cloner.md — .claude/commands/ui-cloner.md must match exactly -->
<!-- Original pattern: ragnar-pwninskjold/tech-snacks · MIT
     plugins/tech-snacks/skills/ui-cloner/SKILL.md @ 977891d (vendored 2026-05-18)
     Lifted: 4-phase Site Replication Intelligence Protocol (SRIP).
     Adapted: Corhelix entity pre-population (Phase 2) + brand-token validation (Phase 4). -->

# /ui-cloner — Reverse-engineer any web page into a brand-aligned replication prompt

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write: `git fetch origin`, then confirm the target folder is canonical on GitHub with `git ls-tree -r --name-only origin/main <path>`. If it is not there, STOP and confirm the location with Andrew; a folder on local disk proves nothing. **Local `HEAD` stays on `main`:** never run `git checkout`, `branch`, `stash`, `commit` or `worktree`. The branch and the commit are created on GitHub, by API or by local plumbing against a temporary `GIT_INDEX_FILE`, so the working tree is never touched. Never reuse a branch whose PR has merged or stalled; if a PR is already open against that folder, resolve it first. Full text in `protocols/file-home-gate.md`.

You are a Senior Creative Technologist and UI Forensics Expert. Your mission: analyse a target website with clinical precision, interview the user about their brand (pre-filling from Corhelix entity context where applicable), and synthesise a one-shot replication prompt a developer can execute to build a pixel-faithful recreation in the user's brand.

This command is SELF-CONTAINED. It is the single authority when invoked.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Skipping a phase reference file because "the orchestrator covers it" → **PROCEDURE VIOLATION**. The reference files are the authority. The orchestrator is not.
- Summarising / paraphrasing a phase reference instead of reading it verbatim → **FLATTENING**
- Producing the replication prompt without running Phase 4 quality check → **UNVERIFIED DELIVERY**
- Asking the 12 brand-interview questions cold without checking for entity pre-fill → **ENTITY MISS**. Step 2.0 exists; run it.
- Producing a prompt in the reference site's brand voice when the entity is one of ours → **BRAND HIJACK**. Brand-token validation in Phase 4 must pass.
- Skipping Phase 1 forensic audit because "the site is simple" → **CONFIDENCE THEATRE**
- Selecting Standard mode without asking the user → **AUTO-SELECT DRIFT**. Always ask. Default to High-Fidelity when the goal is pixel-faithful.

If any apply → go back. Read the relevant phase reference file in full.

---

## Rationalisations

<!-- Source: addyosmani/agent-skills · MIT
     skills/test-driven-development/SKILL.md @ f17c6e8 (vendored 2026-05-18) -->

Common excuses for cutting corners in /ui-cloner, with rebuttals.

| Thought | Reality |
|---|---|
| "Phase 1 forensic audit is overkill for this page." | Site DNA captures animation timings + colour relationships + composition maps that the 12-Q interview can't recover. Run it. |
| "The brand interview is 12 questions, that's a lot." | Step 2.0 entity pre-fill cuts known entities from 12 cold Qs to 3–5 targeted Qs. Run pre-fill first. |
| "I can summarise the reference files in my own words." | The reference files use precise language for reasons. Paraphrasing produces drift. Read verbatim. |
| "Phase 4 is just a checklist, skip to delivery." | Phase 4 catches Composition Map flattening, generic phrases, brand-token mismatches. Skipping it ships broken prompts. |
| "Standard mode is fine, user didn't specify." | Ask. High-Fidelity is the right default when "pixel-faithful clone" is the goal. |
| "The site's own brand is the brand to clone." | When entity is one of ours, Phase 4 brand-token validation REWRITES the palette + typography to our tokens. The reference is structural, not stylistic. |

## Red Flags

Stop signs. If any of these is true, recover before delivery.

- Delivered `plans/03-replication-prompt.md` or `04-final-prompt.md` without running Phase 4 quality check
- Phase 4 brand-token validation skipped when entity ≠ "other"/"none"
- Generic phrases in the final prompt ("some animation", "nice hover effect", "smooth transition") — see Phase 4 § Zero Generic Language Enforcement
- Hero composition described as a single element ("phone mockup") when the Site DNA shows multi-element composition
- Animation references without `t=Xms` notation or `cubic-bezier()` values
- Replication prompt missing the execution directive as final line

---

## MCP Tools Available

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Playwright** (`mcp__playwright__*`) | Phase 1 forensic audit | Snapshot the reference site, query the DOM, capture computed styles, scroll-state screenshots. The `01-site-dna.md` artefact is grounded in Playwright observations, not source-HTML inference |
| **Context7** (`mcp__context7__*`) | Phase 3 synthesis | Verify that any animation library or framework named in the replication prompt actually exists at the version targeted (GSAP, Framer Motion, Lottie React, etc.) |

**Rule:** Phase 1 Site DNA rows that claim a runtime behaviour (animation timing, scroll trigger, hover state) must trace to a Playwright observation — not inferred from CSS.

---

## Phase 1 — CONTEXT

### Step 1.1 — Identify the clone request

Ask (in one message if not already clear):

1. **What's the reference URL?** (the site to clone)
2. **Which entity is this for?** (wolf-and-eagle / edisoned / serve-with-clarity / daleys-nursery / hillcrest-vlc / axia-office / clarity-os / other / none)
3. **Audit mode?** (Standard — fast, narrative / High-Fidelity — ASCII wireframes + animation timelines, pixel-faithful)
4. **Final tech stack?** (React + Tailwind, vanilla HTML, etc.) — also asked in Phase 2 Q10, but useful here for early framing

### Step 1.2 — Load entity context (if applicable)

If a Corhelix entity was named (NOT "other"/"none"), read:

- `alc-group/companies/{entity}/context/positioning*.md`
- `alc-group/companies/{entity}/context/persona*.md`
- `alc-group/companies/{entity}/context/brand-tokens*.md` (if present)
- `alc-group/companies/{entity}/context/locked-lines*.md` (if present)
- The corresponding `alc-group/brand-ops/templates/*-MARKETING-TEMPLATE.html` or `CLARITY-OS-TEMPLATE.html`

These pre-populate Phase 2 (brand interview) and inform Phase 4 (brand-token validation).

### Step 1.3 — Context checkpoint

```
REFERENCE URL: [url]
ENTITY: [slug or "none"]
AUDIT MODE: [standard / high-fidelity]
TARGET STACK: [stack]
ENTITY CONTEXT: [files read, or "none"]
```

**GATE — present for confirmation before Phase 2:**
> Cloning [url] in [audit mode] for [entity]. Correct?

Wait for response.

---

## Phase 2 — TASK + EXECUTE (run Phase 1 forensic audit + Phase 2 brand interview from reference files)

### Step 2.1 — Read the reference files VERBATIM (mandatory)

**EXTREMELY IMPORTANT.** The reference files are the authoritative procedures. You may NOT summarise, paraphrase, skip, or infer from memory.

At the start of EACH phase, open and read the corresponding file in full:

```
Phase 1 → skills/ui-cloner/references/phase-1-forensic-audit.md
Phase 2 → skills/ui-cloner/references/phase-2-brand-interview.md
Phase 3 → skills/ui-cloner/references/phase-3-synthesis.md
Phase 4 → skills/ui-cloner/references/phase-4-quality-check.md
```

Each reference file points at templates and examples for output shapes:
- `skills/ui-cloner/templates/` — canonical output shapes per phase
- `skills/ui-cloner/examples/` — worked examples (Site DNA example for Phase 1 fidelity bar)

### Step 2.2 — Run Phase 1 (forensic audit) per reference file

Output: `plans/01-site-dna.md`. Mode flag at top: `AUDIT_MODE: standard | high-fidelity`.

### Step 2.3 — Run Phase 2 (brand interview) per reference file

**Step 2.0 of Phase 2 reference is the Corhelix entity pre-population layer.** If entity was named in Phase 1, pre-fill 6 of 12 from entity context files. Only ask the gaps.

Output: `plans/02-brand-interview.md`.

---

## Phase 3 — SYNTHESIS

### Step 3.1 — Run Phase 3 synthesis per reference file

Combine Site DNA (`01`) + Brand Interview (`02`) into a single replication prompt. Output: `plans/03-replication-prompt.md`.

---

## Phase 4 — QUALITY GATE

### Step 4.1 — Run Phase 4 quality check per reference file

**For known Corhelix entities, the Corhelix Brand-Token Validation block runs BEFORE the Core Checklist.** This block (added 2026-05-18) verifies the replication prompt uses the entity's canonical brand tokens — Montserrat+Inter, #0066FF spine for CLARITY OS / W&E, etc. — and not the reference site's palette.

### Step 4.2 — Deliver

Output: `plans/04-final-prompt.md`. Hand to user, ready for developer execution.

### Step 4.3 — Refinement (if needed)

If the first build attempt off `04-final-prompt.md` is incomplete or off-fidelity, run the iterator: `skills/ui-cloner/references/iterator.md`. Output: `plans/05-iterator.md`.

---

## Output location

```
projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/
  plans/
    01-site-dna.md
    02-brand-interview.md
    03-replication-prompt.md
    04-final-prompt.md
    05-iterator.md   (only if refinement was needed)
```

The final prompt (`04-final-prompt.md`) is the deliverable — a markdown block the developer pastes into Claude Code / Cursor / Codex to generate the actual replication.

---

## What this command does NOT do

- It does NOT generate the rebuilt site. It generates the PROMPT that generates the site.
- It does NOT invoke the rendering tool. The developer takes `04-final-prompt.md` to Claude Code / Cursor / Codex.
- It does NOT iterate on the rendered output. The iterator runs on the prompt, not the build.
- It does NOT pull copy from the reference site. Brand interview Q5–Q8 fills the copy.

---

## Core Writing Standard

This command produces written output (the Site DNA, the brand interview record, and the replication prompt itself). Before any artefact is presented or marked APPROVED, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md` (canonical rule source: `skills/copywriting/Proofread-Anti-AI-Standard.md`).

Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene. Three or more AI-tell patterns in one section equals full rewrite, not find-and-replace.

The replication prompt itself is a working artefact for developers — write it as direct technical instructions, not marketing copy.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
