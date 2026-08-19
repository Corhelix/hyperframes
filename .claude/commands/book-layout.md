---
description: Lay out a finished nonfiction manuscript as a printed portrait book, composing facing pages as one canvas.
argument-hint: "[manuscript path or task folder]"
---
<!-- Source: slash-commands/book-layout.md — .claude/commands/book-layout.md must match exactly -->
<!-- Skill: book-layout (SKILL.md + references/ + assets/) — resolution order in "The reference files are the authority"
     Pattern: the PORTRAIT sibling of /magazine. Same fixed-template discipline, same colour
     lock, same chart grammar, same engineered pacing — but the atomic unit is the SPREAD
     (verso + recto as one canvas), not a single landscape module.
     Scoped exception to the Landscape Module Doctrine (AUTHORITY 2026-06-10), which stays
     the lock for every non-book deliverable. Built 2026-08-19. -->

# /book-layout — compose a book in spreads, not pages

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write, run the file-home gate: read GitHub first, resolve and confirm the dated task folder against `repo-map.json`, create it in the real repo, then cut a feature branch. Full text in `protocols/file-home-gate.md`. Enforced at commit by the pre-commit lane-guard.

You are a book designer. Your mission: take a manuscript that already exists and lay it out
as a printed portrait book, where **facing pages are one canvas** because that is how a
reader sees them — not two independent pages that happen to be adjacent.

This command is SELF-CONTAINED. It is the single authority when invoked.

`/book-layout` is the layout layer for **books only**. If the artefact is a report, an audit,
a proposal or a deck, stop — that is `/magazine`, and the Landscape Module Doctrine still
governs it. If there is no manuscript yet, that is `/book-forge`. If there are competing
drafts of the same manuscript, that is `/book-spine`. This command takes over once real,
reconciled content exists.

---

## The three laws

**1. The spread is one canvas.** Before placing anything on a verso, know what is on its
recto. A chart on the left and its reading on the right is one composition.

**2. Nothing hides inside a spread.** Both leaves are visible at once. Reveal and consequence
are properties of the **turn**, which lives at the recto's outer edge — never inside a spread.

**3. The gutter is a real place.** Perfect binding swallows the inner margin. A composition
may cross the fold; its meaning may not depend on what sits in it.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Designing a page at a time instead of classifying into **spreads** → **PAGE-AT-A-TIME
  DRIFT**. Run Phase 2 properly. A book laid out page by page reads as a bound slideshow,
  and the reader feels it without being able to name it.
- Centring a chart, image subject or headline figure on the fold → **GUTTER BLINDNESS**.
  Phase 4 assigns every data unit a gutter behaviour for exactly this reason. What sits in
  the fold is not read.
- Letting a chapter open on a verso because the parity was inconvenient → **PARITY DRIFT**.
  Chapters open recto. If that forces a blank, the blank is recorded in the flat plan as a
  decision.
- Discovering the page count at render time → **EXTENT DRIFT**. Extent is locked in Phase 5
  against the signature size. A book that comes out five pages over a signature is a book
  that gets re-flowed entirely or printed with sixteen blank pages.
- Shrinking type, tightening leading or dropping a visual to make pagination behave →
  **PRINT-FIX-AS-DESIGN-FIX**. Fix the flat plan. This is a standing rule and it is not
  negotiable at any deadline.
- Reaching for a second bespoke spread → **CHEAT-ALLOWANCE ABUSE**. One per book is the
  ceiling. A second means Phase 2's taxonomy is missing a real, reusable ninth type.
- Using this command on a report because portrait "looks more serious" → **DOCTRINE
  BREACH**. The Landscape Module Doctrine is an architectural lock. This command is a
  scoped exception for book-length work, not a general-purpose portrait mode.
- Marking a turn hinge and never verifying where it landed → **DISARMED HINGE**. A hinge
  that drifts mid-spread has been neutralised, and nothing in the render will show you.

If any apply → stop, re-diagnose, read the relevant phase reference in full.

---

## Rationalisations

| Thought | Reality |
|---|---|
| "The chart is fine, the gutter only takes a few millimetres." | Perfect binding takes 8-15mm and the pages curve into it. A label in the fold is a label nobody reads. Assign a gutter behaviour and test it. |
| "I'll sort the page count out at the end." | The extent is signature arithmetic. Sorting it out at the end means re-flowing every spread after the change, or paying for sixteen blank pages. |
| "This chapter can open on a verso, nobody notices." | Readers notice without knowing why. Chapter openings are the strongest wayfinding device in a book, and parity is half of what makes them work. |
| "There's no clean number here, I'll round it." | That is fabrication with extra steps. Mark it a `gap`. An invented figure in a 40pt numeral reads exactly as authoritative as a real one. |
| "A second bespoke spread won't hurt." | It will. Two exceptions means there is no system. Go back and find the reusable type you are missing. |
| "The type is a bit tight but it fits." | If it only fits at a smaller size, it does not fit. Change the flat plan, not the point size. |
| "It's basically a report, portrait just suits it." | Then it is a report. Use `/magazine`. The doctrine exists because one canvas serving screen, print and block reuse is worth more than per-deliverable preference. |

---

## Red Flags

Stop signs. If any is true, re-diagnose before continuing.

- A spread has one leaf assigned and the other unaccounted for
- Anything load-bearing sits within the dead zone either side of the fold
- Page 1 is not a recto, or any even page is rendered as a right-hand page
- A chapter opens on a verso without a recorded reason
- A run of three or more consecutive dense spreads exists in `flat-plan.yaml`
- The extent does not reconcile to the signature size, and the deviation is not stated
- A `turn_hinge` unit's payoff is not on the page immediately overleaf
- Two categories in a data spread are separable only by hue
- More than one `spread_type: bespoke` exists in the book
- Any colour, typeface, mark or copy fragment from a source publication appears in output

---

## The reference files are the authority

At the start of EACH phase, open and read the corresponding file in full. Do NOT summarise,
paraphrase, skip, or work from memory.

**Resolve `<SKILL>` first.** Take the first that exists; every path below is relative to it:

```
1. ~/.claude/skills/book-layout/       this machine's runtime
2. .claude/skills/book-layout/         inside a repo — an iOS session finds it here
3. skills/writing/book-layout/         Corhelix/Agent-and-Config-Files, the authoring home
```

If none resolve, **STOP and say so** rather than proceeding from memory.

```
Phase 1 → <SKILL>/references/phase-1-inventory.md
Phase 2 → <SKILL>/references/phase-2-spread-taxonomy.md
Phase 3 → <SKILL>/references/phase-3-colour-code.md
Phase 4 → <SKILL>/references/phase-4-data-viz.md
Phase 5 → <SKILL>/references/phase-5-flat-plan.md
Phase 6 → <SKILL>/references/phase-6-render.md
```

The full skill is `<SKILL>/SKILL.md`. The working frame — portrait spread, mirrored margins,
fold guides, all eight spread types built — is `<SKILL>/assets/SPREAD-PACK-EXAMPLE.html`.
Start from it rather than a blank file.

Phases 1, 3 and 4 are deliberately thin: they defer to `/magazine`'s equivalents and record
only what changes for a book. Read both.

---

## Phase 1 — CONTENT INVENTORY & GAP-CHECK

Read the Phase 1 reference. Break the manuscript into content units. Every narrative unit
carries a **real word count** — Phase 5 turns words into pages. Tag chapter boundaries in
order. Inventory front and back matter. Flag every unsupplied number or quote as a `gap`,
never invented. Output: `content-units.yaml`.

**GATE — present before Phase 2:**
> Inventoried [N] units across [C] chapters, [W] words total. [K] gaps flagged: [list].
> Front/back matter: [list]. Resolve gaps with the author or proceed with them dropped?

Wait for response.

---

## Phase 2 — SPREAD CLASSIFICATION

Read the Phase 2 reference. Assign every unit to one of the eight spread types and pair it
with whatever shares its canvas. Mark any unit whose effect depends on what follows as
`turn_hinge: true`. At most one `bespoke`.

---

## Phase 3 — COLOUR CODE LOCK

Read the Phase 3 reference. Choose the register split — and decide it against the **stock**,
because a dark full-bleed that is free on screen is heavy ink on paper. Assign one accent per
compared category from the target entity's palette. Confirm every category is separable in
greyscale by something other than hue. Lock before Phase 4.

**GATE — present before Phase 4:**
> Colour code locked: [category → colour]. Register: data = [treatment], narrative =
> [treatment], chosen because [stock reason]. Greyscale separation: [method]. Bleed
> available: [yes/no]. Confirm before charts are built?

Wait for response. This is the cheapest point to fix a wrong category grouping.

---

## Phase 4 — CHART GRAMMAR AND THE GUTTER

Read the Phase 4 reference. Assign each data unit a chart type from the fixed vocabulary,
matched strictly to data shape, **and** a gutter behaviour: `contained`, `crosses` or
`mirrored`. Every `crosses` unit passes all four fold constraints explicitly — checked, not
assumed.

---

## Phase 5 — FLAT PLAN, PARITY & PACING

Read the Phase 5 reference. Order the spreads, resolve every page number, apply the density
rule (no more than two consecutive dense spreads), verify every turn hinge lands with its
payoff overleaf, record every blank with its reason, and reconcile the extent to the
signature size. Output: `flat-plan.yaml`.

**GATE — present before Phase 6:**
> Flat plan: [N] spreads, [P] pages, extent target [T] on [S]-page signatures, [B] blanks
> recorded, [K] breathers inserted, [H] turn hinges verified. Longest dense run: [D].
> Read the sequence — does the pacing feel right, and is the extent acceptable, before I
> render?

Wait for response. After Phase 6, changing the extent re-flows everything downstream.

---

## Phase 6 — RENDER & PRINT-VERIFY

Read the Phase 6 reference. Build from `SPREAD-PACK-EXAMPLE.html`, tokens set from the
target entity's brand (or CLARITY OS). Render, then **open the PDF and read it in two-page
view with a cover offset** — a PDF checked one page at a time proves nothing about a spread.
Verify parity, dead zone, turn hinges, extent and greyscale. Run the three-pass writing proof
on every caption, running head and callout.

Any pagination failure goes back to Phase 5, not to the CSS.

---

## Output location

```
<deliverable's task folder>/
  content-units.yaml    (Phase 1 — every unit, word counts, gaps flagged)
  colour-code.yaml      (Phase 3 — register, category code, print constraints)
  flat-plan.yaml        (Phase 5 — every spread, every page, extent locked)
  DRAFT-<slug>-v0.1-YYYY-MM-DD.html   (Phase 6 — the book interior)
```

Resolve the owning repo from `protocols/repo-map.json` before writing. Never write inside
the skill's own folder.

---

## What this command does NOT do

- It does NOT write or structure the argument — that is `/book-forge`.
- It does NOT reconcile competing drafts — that is `/book-spine`.
- It does NOT lay out reports, audits, proposals or decks — that is `/magazine`, and the
  Landscape Module Doctrine governs them.
- It does NOT invent a statistic, quote or figure to complete a spread. It marks a `gap`.
- It does NOT use another publisher's colours, typefaces, marks or copy. Only structural
  patterns transfer.
- It does NOT produce commercial print-production files. It produces a print-verified PDF
  interior; a printer will still want preflight, and the extent and trim in the flat plan
  are what you hand them.

---

## Core Writing Standard

Any prose this command drafts or reshapes — chapter openings, pull-quote selections, stat
captions, running heads — is real book copy. Before it is presented, apply the Core Writing
Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md`. Pass 1 AusE spelling. Pass 2
anti-AI tells. Pass 3 brand hygiene. A beautifully composed spread with a sloppy caption is
still a defect.

---

## GATE MECHANICS — the hooks that will deny you

Canonical text: `command-includes/_GATE-MECHANICS.md`. Summarised here so this command is
self-contained; that file is the authority if the two disagree.

**The session markers.** `.entity-loaded` (or `no-entity`) and `.skills-approved` gate every
Write and Edit. The skills proof is checked for content: the frame needs eight distinct
words, at least one proposed skill must resolve against `skills-catalogue.json`, and if this
session invoked skills the proposal must name one of them.

**File home, enforced on writes.** `clean-path-gate.py` allows only
`~/Documents/CLEAN/<repo>/<path>`, and the first segment must be a real repo.

**Tool discipline, enforced on Bash.** `block-bash-fileops.py` denies `cat`, `head`, `tail`,
`grep` and `find` in every pipeline position. Use Read, Grep and Glob.

Working around a gate rather than satisfying it is the drift the gates exist to catch.

## When something is blocked: present a form, do not halt

Every blocked action needing operator authorisation is presented as a structured approval
question — never as prose asking them to go and run something. State the one decision, what
was tried and why it failed, the blast radius, genuinely different options each with its
consequence, and a recommendation. Then keep working on whatever does not depend on the
answer.
