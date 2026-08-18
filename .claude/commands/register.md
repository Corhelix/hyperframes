---
description: Scaffold a decision-tagged review surface.
argument-hint: "[context or target]"
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
