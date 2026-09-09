---
name: register
description: Scaffold a decision-tagged review surface.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - an item is recorded into a register
  does_not_fire_when:
    - a full session record is wanted -> /report
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: entry
      is: the item recorded, with its date, owner and the decision it captures
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: slash-commands/register.md — .claude/commands/register.md must match exactly -->
# /register — Scaffold a decision-tagged review surface

Build a fresh HTML deliverable from the canonical decision-tagging pattern (modules + Decision Register + archive + LOCK/REVISE/DROP/DEFER tagging UI). Use when the doc contains reviewable items needing approval — decisions, options, advances, risks, phases, audit findings, or any list of things Andrew has to stamp.

This command is the explicit invocation of the pattern. The same pattern is also the default for `/spec`, `/prd-build`, `/audit`, and `/report` — those produce category-specific docs that already use the scaffold. `/register` is for ad-hoc decision tracking that doesn't fit any of those categories (vendor selection, tech stack choice, cross-doc decision matrix, etc.).

---

## Canonical scaffold

**Always read from:** `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`

This is the single source of truth. Do NOT hand-write the brand CSS, module structure, register table, or action bar — copy from the canonical and fill in placeholders. If the canonical is missing, STOP and ask.

---

## Procedure

### Step 1 — Establish scope

Ask (if not already clear):
1. **What's the doc title?** (one short line — e.g. "Vendor selection: monitoring stack")
2. **What's the slug?** (kebab-case — e.g. `vendor-monitoring-stack`)
3. **What kinds of items will the register track?** Pick from: `D` decisions · `ADV` advances · `R` risks · `P` phases · `M` messaging · `O` outputs · `S` sections · `T` tasks. Mixed kinds OK.
4. **How many rows initially?** (rough number — placeholder modules + register rows scaffold this many)
5. **Which entity owns the doc?** (resolves output path via `protocols/entity-repo-map.md`)

**GATE — present for confirmation:**
> Title: [...] | Slug: [...] | Kinds: [...] | Rows: [N] | Entity: [...] | Output: [path/DRAFT-REGISTER-{slug}-v0.1-YYYY-MM-DD.html]
> Confirm before scaffolding?

Wait for response.

### Step 2 — Generate the deliverable

1. **Read** the canonical scaffold from `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`.
2. **Replace** the `{{...}}` placeholders:
   - `{{Document Title}}` → user's title
   - `{{Banner Text}}` → "CLARITY OS · {Title} · v0.1"
   - `{{document-slug}}` → user's slug (used in `STORAGE_KEY`)
   - `{{YYYY-MM-DD}}` → today's date
   - `{{Decision Document}}` → "Decision register"
3. **Generate** N module placeholders + N matching register rows for the requested kinds. Each module:
   - `id="section-{ID}"` `data-id="{ID}"` `data-kind="{kind}"` `data-version="v0.1"` `data-status="current"`
   - h3 placeholder for title
   - `module-body` with one paragraph placeholder
4. **Update** `TOTAL_ROWS` to the row count (or replace with auto-count: `document.querySelectorAll('tr[id^="row-"]').length`).
5. **Write** to the resolved output path. Open in browser.

### Step 3 — Confirm + handover

Present:
- File path
- Row count
- Storage key (so user knows which localStorage key to clear if needed)
- One-line "next step" (typically: fill in module bodies, then stamp register rows)

---

## Output location

Resolve entity → repo via `protocols/entity-repo-map.md` (Output Routing section). Subfolder = `reviews/`.

Examples:
- clarity-os-app → `../clarity-os-app/docs/reviews/YYYY-MM-DD-{slug}/DRAFT-REGISTER-{slug}-v0.1-YYYY-MM-DD.html`
- alc-group entity → `../alc-group/companies/{entity}/reviews/YYYY-MM-DD-{slug}/DRAFT-REGISTER-{slug}-v0.1-YYYY-MM-DD.html`
- client → `../client-projects/{parent}/clients/{client}/reviews/YYYY-MM-DD-{slug}/DRAFT-REGISTER-{slug}-v0.1-YYYY-MM-DD.html`

**HARD RULE:** Never write to `DEFAULT-CLAUDE/projects/`. If the entity → repo can't be resolved, STOP and ask the user to add the entity to the Product Repos table first.

---

## Chains to

- After stamping: paste the markdown export back to me; I produce surgical edits per REVISE row, generate companion v0.2 with only-pending rows.
- When all rows LOCKED: I write `APPROVED-{slug}-YYYY-MM-DD.html` consolidating all decisions in final state. Older versions move to the Archive section.

---

## What this command does NOT do

- Author the actual decision content (you fill in module bodies, or feed me one decision at a time and I write each module)
- Replace `/spec`, `/prd-build`, `/audit`, `/report` for those category-specific docs — those already use the scaffold
- Persist decisions to a database (pre-CLARITY-OS this is browser localStorage; post-v6b it becomes `clos_decisions` rows)

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
