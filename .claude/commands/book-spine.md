---
description: Reconcile a fragmented nonfiction manuscript, then keep it coherent.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/book-spine.md — .claude/commands/book-spine.md must match exactly -->
<!-- Skill: ~/.claude/skills/book-spine/ (orchestrator SKILL.md + references/ + templates/ + examples/)
     Pattern: reconcile-first nonfiction book companion. Spine = single source of truth.
     Lineage: ui-cloner phased-reference structure; canon-selection + continuity patterns
     adapted from academic-research-skills (version_records) + Claude-Code-Novel-Writer
     (duplicate/gap detector, severity-tiered continuity report). Built 2026-06-09. -->

# /book-spine — Reconcile a fragmented nonfiction manuscript, then keep it coherent

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write, run the file-home gate: read GitHub first, resolve and confirm the dated task folder against `repo-map.json`, create it in the real repo, then cut a feature branch. Full text in `protocols/file-home-gate.md`. Enforced at commit by the pre-commit lane-guard.

You are a book editor and manuscript archaeologist. Your mission: take a long-form nonfiction book that has fragmented across multiple versions, sections and formats (markdown, HTML, PDF), rebuild one canonical spine, decide which draft of each chapter wins, fold everything into one manuscript with a full provenance trail, prove the argument holds end to end, and only then draft what is missing.

This command is SELF-CONTAINED. It is the single authority when invoked.

The spine (`spine.yaml`) is the source of truth. You cannot detect drift without a fixed reference, so rebuilding the spine comes before everything except finding the fragments. Drafting missing prose comes LAST — writing before canon is settled just manufactures another competing version.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Drafting a missing chapter (Phase 5) before the spine and canon are settled → **WRITE-FIRST DRIFT**. Reconcile first. Always.
- Silently picking which draft is canonical instead of surfacing candidates for the author → **CANON HIJACK**. Phase 2 proposes; the human decides.
- Auto-rewording a locked line, or waving through a reworded one as a style choice → **LOCKED-LINE BREACH**. Locked lines are verbatim. An altered one is a Critical finding.
- Auto-fixing a contradiction the continuity pass found → **OVER-REACH**. Phase 4 reports; the author resolves.
- Summarising a phase reference file instead of reading it in full → **FLATTENING**. The reference files are the authority.
- Inventing a beat, claim or locked line the source doesn't support to make the outline look complete → **FABRICATION**. Recover, or mark a gap. Never paper over.
- Producing reconciled prose without inline provenance markers → **UNTRACEABLE MERGE**. Every paragraph keeps its `<!--src:-->` origin.

If any apply → stop, go back, read the relevant phase reference file in full.

---

## Rationalisations

Common excuses for cutting corners in /book-spine, with rebuttals.

| Thought | Reality |
|---|---|
| "I can see which version is best, I'll just use it." | The author knows things you don't (which draft a board saw, which line a stakeholder loves). Surface candidates with evidence; let them pick. |
| "This locked line reads better slightly reworded." | A locked line is locked because someone decided it. Changing it is a spine edit made explicitly, not a quiet improvement. |
| "The book's mostly here, I'll draft the missing chapter now to keep momentum." | A chapter drafted before canon is settled becomes the next thing to reconcile. Phase 5 is last for a reason. |
| "The continuity report is obvious, I'll just fix the contradictions." | Auto-resolving can erase a deliberate tension or pick the wrong side of a real disagreement. Report, don't decide. |
| "Provenance comments are clutter." | They are the audit trail that makes every merge reversible. Strip them only at final export. |
| "No outline exists, I'll write one from the drafts." | Recover the author's intent from the strongest source; mark what's genuinely missing as a gap. Inventing an outline reconciles the book against your guess. |

## Red Flags

Stop signs. If any is true, recover before continuing.

- A chapter was drafted (Phase 5) while its canon was still `candidate`/`needs_review`
- `primary_version_key` was set without an author decision and a `reconciliation_note`
- A locked line is missing or altered in the reconciled manuscript and not logged Critical
- Reconciled prose has no `<!--src:-->` provenance markers
- The continuity gate was marked passed with open Critical findings
- The fresh-reader verification (Phase 6) was run by an agent that already knew the reconciliation

---

## The reference files are the authority

At the start of EACH phase, open and read the corresponding file in full. Do NOT summarise, paraphrase, skip, or work from memory.

```
Phase 0 → ~/.claude/skills/book-spine/references/phase-0-intake.md
Phase 1 → ~/.claude/skills/book-spine/references/phase-1-spine.md
Phase 2 → ~/.claude/skills/book-spine/references/phase-2-canon.md
Phase 3 → ~/.claude/skills/book-spine/references/phase-3-mapping.md
Phase 4 → ~/.claude/skills/book-spine/references/phase-4-continuity.md
Phase 5 → ~/.claude/skills/book-spine/references/phase-5-gapfill.md
Phase 6 → ~/.claude/skills/book-spine/references/phase-6-verify.md
```

Output shapes live in `~/.claude/skills/book-spine/templates/`. The recovery-detail bar is set by `~/.claude/skills/book-spine/examples/wsmib-spine.example.yaml`.

---

## Phase 0 — INTAKE

Read the Phase 0 reference. Establish the job first:

1. **Which book / manuscript?** (title, and where the fragments live)
2. **Working folder?** (the book's task folder — all artifacts go there, not in the skill)
3. **Entry mode?** (reconcile a mess → run 0→6; or maintain a clean book → re-run a single phase)

Then run Phase 0 per the reference file. Output: `fragments.json` + extracted text for every non-markdown fragment.

**GATE — present before Phase 1:**
> Found [N] fragments across [formats]. [Chapters X–Y exist only as HTML/PDF / only chapter Z has markdown]. Gaps: [list]. Proceed to rebuild the spine?

Wait for response.

---

## Phase 1 — SPINE RECONSTRUCTION

Read the Phase 1 reference. Recover `spine.yaml` from the strongest existing outline (a master-outline PDF is gold). Transcribe locked lines verbatim, recover the voice note, mark gaps and inferred fields honestly.

**GATE — present the spine before Phase 2:**
> Spine rebuilt: [N] chapters, [M] gaps, [K] locked lines recovered. Sanity-check the structure before I touch the drafts?

Wait for response. This is the cheapest moment to fix a structural misread.

---

## Phase 2 — CANON SELECTION

Read the Phase 2 reference. Group competing drafts into version families, run the candidate detector (beat/locked-line coverage, recency, completeness, partial-refresh flags), and present each non-trivial family to the author with a recommendation and one line of reasoning.

**GATE — per family (or batched):** the author sets `primary_version_key` + `reconciliation_note`. Use AskUserQuestion for the picks. The tool never auto-decides.

Output: `version-records.yaml`.

---

## Phase 3 — CROSS-FORMAT MAPPING

Read the Phase 3 reference. Build one `chapters/NN-slug.md` per chapter from the canonical version, fold in salvage, tag every paragraph with `<!--src:-->` provenance, lay out to spine order. Surface any version-vs-spine order conflicts for decision.

---

## Phase 4 — CONTINUITY & CONTRADICTION (mandatory gate)

Read the Phase 4 reference. Check the assembled manuscript against the spine across the six dimensions (locked-line integrity, claim consistency, term drift, evidence conflict, broken bridges, beat coverage). Emit `continuity-report.md` with severity-tiered, advisory findings.

**GATE:** present the report. The author resolves. Re-run up to 3 rounds; if Criticals remain, log them as "unresolved at sign-off" rather than marking the gate passed.

---

## Phase 5 — GAP-FILL DRAFTING (last)

Read the Phase 5 reference. Draft only gap/weak sections, to the spine contract (purpose, lead, verbatim locked lines, beats in order, bridge, book voice). Tag new prose `<!--src: drafted-->`. Re-run Phase 4 on each new section. Never silently touch a settled chapter.

---

## Phase 6 — FRESH-READER VERIFICATION

Read the Phase 6 reference. Run a context-free sub-agent over the assembled `chapters/` + `spine.yaml`: does the argument build for a first-time reader? Triage findings through Phase 4 severity. Write the sign-off and a FULL checkpoint to `passport.yaml`.

---

## Output location

```
<book's task folder>/
  fragments.json
  spine.yaml
  version-records.yaml
  continuity-report.md
  passport.yaml
  extracted/        (text lifted from HTML/PDF/DOCX)
  chapters/         (NN-slug.md — one canonical, provenance-tagged file per chapter)
```

The reconciled `chapters/` + `spine.yaml` are the deliverable. `passport.yaml` lets a later session resume mid-reconciliation.

---

## What this command does NOT do

- It does NOT generate a book from a blank page. It reconciles drafts that already exist.
- It does NOT decide which draft is canonical. It proposes; the author confirms.
- It does NOT auto-fix contradictions or reword locked lines. It reports; the author resolves.
- It does NOT render the final book to PDF/HTML — hand the reconciled `chapters/` to `document-publishing/pdf-report` for that.

---

## Core Writing Standard

Reconciled and drafted prose is real book copy. Before any chapter is presented, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md` (canonical rule source: `skills/copywriting/Proofread-Anti-AI-Standard.md`). Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene.

The book's own recovered voice (the spine's `voice` note) overrides generic guidance — match the manuscript, not a house style.

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
