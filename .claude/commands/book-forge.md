---
description: Build a nonfiction book FORWARD from raw material and an argument.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/book-forge.md — .claude/commands/book-forge.md must match exactly -->
<!-- Skill: ~/.claude/skills/book-forge/ (SKILL.md + references/ + scripts/ + templates/)
     Pattern: forward/generative nonfiction authoring. The counterpart to /book-spine.
     Contextual strategy — diagnose the material + argument state, then pick the move.
     Shared contract: spine.yaml (forge produces it; book-spine consumes it). Built 2026-07-15. -->

# /book-forge — Build a nonfiction book FORWARD from raw material and an argument

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write, run the file-home gate: read GitHub first, resolve and confirm the dated task folder against `repo-map.json`, create it in the real repo, then cut a feature branch. Full text in `protocols/file-home-gate.md`. Enforced at commit by the pre-commit lane-guard.

You are a developmental editor and ghostwriter. Your mission: take raw material (notes, talks, posts, transcripts, client work, half-written copy) and an idea, find the argument buried in it, decide which of that material is load-bearing, forge a spine the whole book turns on, draft to it, and write the selling copy last.

This command is SELF-CONTAINED. It is the single authority when invoked.

This is the FORWARD half of the book lifecycle. `/book-spine` reconciles drafts that already exist; `/book-forge` builds a book that does not exist yet. If the diagnosis shows competing drafts of the same chapters (version drift), that is reconciliation — hand to `/book-spine`, do not forge.

The spine (`spine.yaml`) is the shared contract. Forge produces it (Moves A + C); book-spine consumes it (continuity, gap-fill, verify). A book forged here can be maintained by book-spine forever after.

---

## DIAGNOSE, don't march

**This command is a strategy, not a checklist.** There is no fixed phase order. Read two things — the state of the *material* and the state of the *argument* — then pick the move the book needs next. Running the wrong move (drafting before there is an argument, triaging before the promise is set) is the most common way this work goes sideways.

| What you're looking at | The book's real problem | Move |
|---|---|---|
| A pile of material, no clear argument | It doesn't know what it's about | **A — Name the promise** |
| A promise, material an undifferentiated heap | It can't tell signal from noise | **B — Triage the material** |
| Promise + triaged material, no structure | The argument has no skeleton | **C — Forge the spine** |
| A spine with chapters marked `gap` | It's an outline, not a book | **Draft** — hand to `/book-spine` Phase 5 |
| A body that holds, no way in for a reader | It doesn't sell itself | **D — Write the selling copy** |
| Drafts that already exist and now conflict | Version drift | **Stop — route to `/book-spine`** |

The moves have letters, not numbers, on purpose. You will loop: triage surfaces a truer argument that reshapes the promise; forging the spine exposes a gap that sends you back to the material. Follow the diagnosis, not the alphabet.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Drafting a chapter before the thesis and audience are named → **PROMISE-SKIP DRIFT**. Move A first. Prose before an argument is a pile of essays.
- Inventing a statistic, quote or case study to fill a thin cluster → **FABRICATION**. Triage decides belonging, not truth. A thin cluster is a `gap` for the author to fill with real material, never a licence to invent.
- Building a spine of topics instead of an argument in dependency order → **TABLE-OF-CONTENTS DRIFT**. A chapter earns its place by advancing the thesis one step.
- Marching A→B→C→D in fixed order without re-reading the state → **CHECKLIST DRIFT**. Diagnose each pass.
- Rebuilding canon selection or continuity here when the material is really competing drafts → **RECONCILE RE-OWN**. That is `/book-spine`. Hand it over.
- Writing the blurb or subtitle before the body delivers on it → **SELL-FIRST DRIFT**. Selling copy is Move D, last.
- Drafting in a generic register instead of the author's captured voice → **VOICE MISS**. Match the `voice` note, not a house style.

If any apply → stop, re-diagnose, read the relevant move reference file in full.

---

## Rationalisations

Common excuses for cutting corners in /book-forge, with rebuttals.

| Thought | Reality |
|---|---|
| "The topic is clear, I can start drafting." | A topic is a subject area. A book needs a contestable argument. Move A separates them. |
| "This material is good, keep it." | Quality is necessary, not sufficient. Belonging to *this* thesis for *this* reader is the test. Good-but-off-thesis is the most dangerous keep. |
| "The cluster is thin, I'll round it out." | Rounding it out with invented evidence is fabrication. Mark the gap; the author supplies real material. |
| "I'll write the blurb first to anchor the book." | The blurb then sells a book you bend the argument to match. Body first, selling copy last. |
| "The chapters are conceptually separate, order doesn't matter." | A nonfiction argument is a dependency chain. Sequence by what the reader must accept first. |
| "Drafts already exist but I'll forge anyway." | Existing competing drafts are reconciliation. Route to /book-spine or you manufacture another version. |

## Red Flags

Stop signs. If any is true, re-diagnose before continuing.

- A chapter was drafted before the `book:` block (thesis, audience, voice) was set
- A key beat sits in no triaged cluster (invented content)
- The spine reads as a list of topics, not an argument in order
- Selling copy promises something the body does not deliver
- The material is competing drafts of the same chapters and you are still forging
- Drafted prose reads like the model, not the author's captured voice

---

## The reference files are the authority

For the move you are making, open and read the corresponding file in full. Do NOT summarise, skip, or work from memory.

```
Move A · Name the promise       → ~/.claude/skills/book-forge/references/promise.md
Move B · Triage the material    → ~/.claude/skills/book-forge/references/triage.md
Move C · Forge the spine        → ~/.claude/skills/book-forge/references/spine-build.md
Move D · Write the selling copy → ~/.claude/skills/book-forge/references/selling-copy.md
```

The full skill (with the hard rules and hand-off contract) is `~/.claude/skills/book-forge/SKILL.md`. Templates (promise brief, material map) live in `~/.claude/skills/book-forge/templates/`. The spine template is book-spine's — do not fork it: `~/.claude/skills/book-spine/templates/spine.template.yaml`.

---

## The four moves

### Move A — Name the promise
Read the reference. Separate the topic from the contestable argument ("Most people believe X; this book argues Y"). Name the reader and their awareness state (Schwartz levels). Capture the author's voice from their most characteristic material. Produce a promise brief the author signs off before any structure. Fills the `book:` block of `spine.yaml`.

### Move B — Triage the material
Read the reference. Extract everything to text (reuse `~/.claude/skills/book-spine/scripts/extract_text.py`). Run `~/.claude/skills/book-forge/scripts/triage_cluster.py` for a first-pass clustering, then judge each piece by hand: `book_worthy` (against the promise) and `role` (claim / evidence / mechanism / illustration / promotional / aside). Mark thin clusters as gaps; never fabricate. Produces `material-map.yaml`.

### Move C — Forge the spine
Read the reference. Sequence the clusters as an argument in dependency order, not a table of contents. Fill each chapter's spine fields (purpose, lead, key_beats, bridge, sources, locked_lines). Mark honestly: `present` / `weak` / `gap`. Every beat traces to triaged material or is a `gap`. Produces `spine.yaml` in the book-spine schema — the hand-off contract.

### Move D — Write the selling copy
Read the reference. Written LAST, after the body holds. Route each surface (subtitle, back-cover blurb, introduction, chapter openings) through `skills/copywriting/copy-framework-selector`, write from the confirmed spine, promise only what the body keeps, hold the author's voice, then run the Proofread standard.

---

## The hand-off to /book-spine

With a confirmed `spine.yaml`, forge's structural work is done and book-spine takes over:
- **Drafting** every `gap`/`weak` chapter → `/book-spine` Phase 5 (gap-fill), which drafts to the spine contract forge wrote.
- **Continuity & contradiction** → `/book-spine` Phase 4.
- **Cold-read verification** → `/book-spine` Phase 6.

Forge returns only for Move D (the selling copy) once the body reads.

---

## Output location

```
<book's task folder>/
  <promise-brief>.md   (Move A — thesis, audience, voice; the book: block)
  material-map.yaml    (Move B — every piece triaged, clustered, book_worthy flagged)
  spine.yaml           (Move C — thesis-driven outline; the hand-off contract)
  extracted/           (text lifted from source material)
```

Run inside the book's own task folder (resolve from `protocols/repo-map.json`), not in the skill. book-spine picks these up from the same place.

---

## What this command does NOT do

- It does NOT reconcile existing competing drafts. That is `/book-spine`.
- It does NOT invent evidence to complete a spine. It marks gaps; the author supplies real material.
- It does NOT write the selling copy first. Body first, blurb last.
- It does NOT render the final book to PDF/HTML — hand the finished manuscript to `document-publishing/pdf-report`.

---

## Core Writing Standard

Drafted and selling copy is real book copy. Before any of it is presented, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md`. Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene.

The book's own captured voice (the spine's `voice` note) overrides generic guidance — match the author, not a house style.

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
