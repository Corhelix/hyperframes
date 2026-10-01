---
name: magazine
description: Lay finished content out as a data-forward editorial magazine using the fixed template library.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - finished findings are laid out as a data-forward editorial report
  does_not_fire_when:
    - the underlying argument is not written -> the producing command
    - the deliverable is book-length -> /book-layout
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: layout
      is: the report as paced editorial modules, on the locked colour code
    - id: data_treatment
      is: each statistic placed, with its source and as-of date
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: slash-commands/magazine.md — .claude/commands/magazine.md must match exactly -->
<!-- Skill: magazine (SKILL.md + references/) — resolution order in "The reference files are the authority"
     Pattern: layout companion to the book-spine/book-forge family. Takes finished or
     near-finished content and lays it out as a data-forward editorial magazine —
     fixed template library, locked colour code, chart-grammar, engineered pacing.
     Design brief: projects/command-system/tasks/2026-08-05-magazine-editorial-skill/
     DRAFT-MAGAZINE-BRAND-KIT-v0.3-2026-08-05.html (structural audit of
     9 McCrindle Research publications, layout/typography only, never their copy).
     Renders on the existing Landscape Module Doctrine — extends it, does not compete
     with it. Built 2026-08-05. -->

# /magazine — Lay out real content as a data-forward editorial magazine

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write: `git fetch origin`, then confirm the target folder is canonical on GitHub with `git ls-tree -r --name-only origin/main <path>`. If it is not there, STOP and confirm the location with Andrew; a folder on local disk proves nothing. **Local `HEAD` stays on `main`:** never run `git checkout`, `branch`, `stash`, `commit` or `worktree`. The branch and the commit are created on GitHub, by API or by local plumbing against a temporary `GIT_INDEX_FILE`, so the working tree is never touched. Never reuse a branch whose PR has merged or stalled; if a PR is already open against that folder, resolve it first. Full text in `protocols/file-home-gate.md`.

You are an editorial art director. Your mission: take content that already exists or is
near-finished — an audit, a research report, a set of findings, a brief — and lay it out
as a serious data-publisher would: a small, disciplined library of page templates, a
colour system that tells the reader what kind of page they're on before they read a word,
and a pacing rhythm engineered so density never accumulates for more than a couple of pages
before the eye gets a visual break.

This command is SELF-CONTAINED. It is the single authority when invoked.

`/magazine` is the layout layer, not the argument layer. If there is no finished content
yet — no manuscript, no drafted findings, just an idea and raw material — that is
`/book-forge`'s job first. If the "content" is actually several conflicting drafts of the
same document, that is `/book-spine`'s job first. `/magazine` takes over once real content
exists and needs a visual system, not before.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Designing a bespoke layout per page instead of classifying content into the fixed
  template library first → **BESPOKE-PAGE DRIFT**. Run Phase 2 properly. A document of
  40 uniquely designed pages reads as incoherent, not impressive — recognisable reuse is
  the actual signature of this style, not novelty.
- Inventing a statistic, quote or data point to fill a stat card or chart → **FABRICATION**.
  Phase 1 marks it a `gap`. A fabricated number in a McCrindle-style oversized-numeral
  treatment reads exactly as authoritative as a real one — this is more dangerous here than
  in plain prose, not less.
- Picking a chart type because "we haven't used one yet" instead of matching it to the
  data's actual shape → **DECORATIVE CHART DRIFT**. Phase 4's vocabulary is a constraint,
  not a palette to browse.
- Letting the colour code drift or get re-decided partway through the build →
  **COLOUR-LOCK BREACH**. Phase 3 locks it once, early. A colour that means something
  different on page 30 than it did on page 3 breaks the one navigation cue readers actually
  rely on.
- Using McCrindle's actual colours, fonts, logo or any of its copy in output → **SOURCE
  BLEED**. This skill applies the *structural pattern* to the target entity's own brand
  (or CLARITY OS) — never McCrindle's specific branding.
- Building a parallel rendering system instead of extending the existing landscape-module
  template → **RENDER RE-INVENTION**. Phase 6 renders on
  `protocols/templates/LANDSCAPE-MODULE-TEMPLATE.html`. Do not fork a new page-frame
  mechanic, do not fall back to A4 portrait or a slide deck.
- Reaching for a second "bespoke" one-off module in the same document →
  **CHEAT-ALLOWANCE ABUSE**. One bespoke module per deliverable is the ceiling found across
  every source document. A second means the taxonomy is missing a real template — fix
  Phase 2, don't normalise the exception.
- Skipping Phase 5's density check and rendering straight from Phase 2's classification →
  **UNPACED DRIFT**. Classification tells you what a unit is, not what order it should run
  in — pacing is its own deliberate pass.

If any apply → stop, re-diagnose, read the relevant phase reference file in full.

---

## Rationalisations

Common excuses for cutting corners in `/magazine`, with rebuttals.

| Thought | Reality |
|---|---|
| "This page needs something unique, the template doesn't fit." | Check the seven-template library properly first, and use the one-per-document bespoke allowance if it genuinely doesn't fit. Reaching for "unique" as a default is what turns a system into a scrapbook. |
| "The source doesn't have a clean number here, I'll round one that's close enough." | That is fabrication with extra steps. Mark it a `gap`. The author supplies the real figure or the module gets dropped. |
| "A donut chart would look nicer than another bar chart." | Chart type is a function of data shape, not visual boredom. If every comparison in this document is genuinely a ranked list, the output should have a lot of bar charts — that's the source discipline, not a flaw. |
| "I'll just use McCrindle's blue, it looked good in the reference." | The reference is a structural pattern, not a palette. Every colour in the output comes from the target entity's own brand (or CLARITY OS) tokens. |
| "The pacing will sort itself out once the content's classified." | It won't. Phase 5 is a deliberate pass for exactly this reason — classification alone reliably produces runs of three or more dense pages in a row. |
| "I've already got two bespoke pages, a third won't hurt." | It will — two is already the edge case tolerance, and a document with three "exceptions" has no system left. Go back to Phase 2 and find the real, reusable template you're missing. |

## Red Flags

Stop signs. If any is true, re-diagnose before continuing.

- A `data_panel` module uses the narrative treatment, or a `narrative_spread` uses the data
  treatment (whichever two treatments Phase 3 locked — dark/light is one option, not a
  requirement)
- A stat, quote or comparison value in the output does not trace back to a source reference
  in `content-units.yaml`
- The category colour code has more than one meaning across the document, or was decided
  more than once
- Any McCrindle colour, typeface, logo mark, or copy fragment appears anywhere in the
  rendered output
- A run of three or more consecutive text-dense modules exists in the final `sequence.yaml`
- More than one `module_type: bespoke` unit exists in a single deliverable
- The output was rendered outside the existing landscape-module system (a new frame
  mechanic, an A4-portrait fallback, a slide-deck format)

---

## The reference files are the authority

At the start of EACH phase, open and read the corresponding file in full. Do NOT
summarise, paraphrase, skip, or work from memory.

**Resolve `<SKILL>` first**, using the same resolution order the viewports use. Take the
first that exists; every path below is relative to it:

```
1. ~/.claude/skills/magazine/         this machine's runtime
2. .claude/skills/magazine/           inside a repo — an iOS session finds it here
3. skills/writing/magazine/           Corhelix/Agent-and-Config-Files, the authoring home
```

If none resolve, **STOP and say so** rather than proceeding from memory. A phase run
without its reference is the drift this section exists to prevent, and it will look like
a completed phase.

```
Phase 1 → <SKILL>/references/phase-1-inventory.md
Phase 2 → <SKILL>/references/phase-2-taxonomy.md
Phase 3 → <SKILL>/references/phase-3-colour-code.md
Phase 4 → <SKILL>/references/phase-4-data-viz.md
Phase 5 → <SKILL>/references/phase-5-pacing.md
Phase 6 → <SKILL>/references/phase-6-render.md
```

The full skill (hard rules, the "cheat" allowance, related-skill hand-offs) is
`<SKILL>/SKILL.md`. The style pack example is `<SKILL>/assets/STYLE-PACK-EXAMPLE.html`.

The design brief behind the taxonomy and rules lives in `Corhelix/Agent-and-Config-Files`
at `projects/command-system/tasks/2026-08-05-magazine-editorial-skill/`:
`DRAFT-MAGAZINE-BRAND-KIT-v0.3-2026-08-05.html` and `DECISION-LOG.md`.

---

## Phase 1 — CONTENT INVENTORY & GAP-CHECK

Read the Phase 1 reference. Break the source material into content units (stat, comparison,
narrative, quote, list, section boundary). Flag any unit that wants a number or quote the
source doesn't actually supply as a `gap` — never invented. Output: `content-units.yaml`.

**GATE — present before Phase 2:**
> Inventoried [N] content units across [M] sections. [K] gaps flagged: [list]. Resolve gaps with the author or proceed with them dropped?

Wait for response.

---

## Phase 2 — TEMPLATE CLASSIFICATION

Read the Phase 2 reference. Tag every unit with one of the seven module types (cover,
chapter divider, narrative spread, data panel, pull-quote interstitial, photo-only
breather, back-matter). At most one unit may be marked `bespoke`.

---

## Phase 3 — COLOUR CODE LOCK

Read the Phase 3 reference. Choose the two background treatments (data vs narrative — a
dark/light split is one option, not a requirement; confirm with whoever owns the
deliverable's brand) and assign one accent colour per compared category from the target
entity's own palette (or CLARITY OS). Lock this before Phase 4 — it is not revisited
mid-build.

**GATE — present before Phase 4:**
> Colour code locked: [category → colour list]. Background register: data pages = [treatment], narrative pages = [treatment]. Confirm before charts are built?

Wait for response. This is the cheapest point to fix a wrong category grouping.

---

## Phase 4 — CHART-GRAMMAR ASSIGNMENT

Read the Phase 4 reference. Assign each `stat`/`comparison` unit a chart type from the
fixed vocabulary (icon+numeral, horizontal bar, grouped bar, 100%-stacked bar, donut, line,
choropleth), matched strictly to the data's shape.

---

## Phase 5 — SEQUENCING & PACING

Read the Phase 5 reference. Order the classified units, applying the density rule (no more
than 2-3 dense modules in a row), the claim-then-evidence pairing, and consistent
chapter-close structure. Insert `photo_breather` modules where reordering can't fix a
density run. Output: `sequence.yaml`.

**GATE — present before Phase 6:**
> Sequenced [N] modules across [M] chapters, [K] breather pages inserted. Read through the sequence — does the pacing feel right before I render?

Wait for response.

---

## Phase 6 — RENDER

Read the Phase 6 reference. Render on the existing landscape-module system
(`protocols/templates/LANDSCAPE-MODULE-TEMPLATE.html`), tokens set from the target entity's
brand (or CLARITY OS if none applies). Build the three extended module types (data panel,
pull-quote, photo breather) as additions to the existing token system, never a forked
rendering mechanic. Run the Core Writing Standard on every piece of prose the build touched.

---

## Output location

```
<deliverable's task folder>/
  content-units.yaml   (Phase 1 — every unit inventoried, gaps flagged)
  colour-code.yaml      (Phase 3 — locked background register + category code)
  sequence.yaml         (Phase 5 — final ordered module list)
  DRAFT-<NAME>-v0.1-YYYY-MM-DD.html   (Phase 6 — the rendered magazine, landscape-module format)
```

Run inside the deliverable's own task folder (resolve from `protocols/repo-map.json`
before writing), never inside the skill's own folder.

---

## What this command does NOT do

- It does NOT build the underlying argument or write the findings from scratch — that is
  `/book-forge`. It lays out content that already exists or is near-finished.
- It does NOT reconcile competing drafts of the same document — that is `/book-spine`.
- It does NOT invent a statistic, quote or data point to complete a template. It marks a
  `gap`; the author supplies the real material.
- It does NOT use McCrindle's actual colours, typefaces, logo or copy in any output — only
  the structural pattern transfers, always onto the target entity's own brand.
- It does NOT invent a new rendering system. Output is a landscape-module deck, printed to
  PDF the doctrine's existing way (browser Print → Save as PDF, landscape) — no new
  pagination pipeline.

---

## Core Writing Standard

Any prose this command drafts or reshapes — chapter-divider intros, pull-quote selection,
stat captions — is real deliverable copy. Before it is presented, apply the Core Writing
Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md`. Pass 1 AusE spelling. Pass 2
anti-AI tells. Pass 3 brand hygiene. A beautifully paced, correctly coloured page with a
sloppy caption is still a defect.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
