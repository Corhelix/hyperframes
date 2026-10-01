---
name: book-forge
description: Build a nonfiction book FORWARD from raw material and an argument.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a nonfiction book is built forward from raw material and an idea
  does_not_fire_when:
    - drafts exist and have diverged -> /book-spine
    - a finished manuscript needs layout -> /book-layout
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: thesis
      is: the claim the book carries, in one sentence
    - id: spine
      is: the chapter sequence and what each chapter must prove
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: slash-commands/book-forge.md — .claude/commands/book-forge.md must match exactly -->
<!-- Skill: ~/.claude/skills/book-forge/ (SKILL.md + references/ + scripts/ + templates/)
     Pattern: forward/generative nonfiction authoring. The counterpart to /book-spine.
     Contextual strategy — diagnose the material + argument state, then pick the move.
     Shared contract: spine.yaml (forge produces it; book-spine consumes it). Built 2026-07-15. -->

# /book-forge — Build a nonfiction book FORWARD from raw material and an argument

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write: `git fetch origin`, then confirm the target folder is canonical on GitHub with `git ls-tree -r --name-only origin/main <path>`. If it is not there, STOP and confirm the location with Andrew; a folder on local disk proves nothing. **Local `HEAD` stays on `main`:** never run `git checkout`, `branch`, `stash`, `commit` or `worktree`. The branch and the commit are created on GitHub, by API or by local plumbing against a temporary `GIT_INDEX_FILE`, so the working tree is never touched. Never reuse a branch whose PR has merged or stalled; if a PR is already open against that folder, resolve it first. Full text in `protocols/file-home-gate.md`.

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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
