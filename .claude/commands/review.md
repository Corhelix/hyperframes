---
description: Review a deliverable through the relevant viewport lens.
argument-hint: "[context or target]"
---
<!-- slash-commands/review.md is canonical; .claude/commands/review.md must match exactly | Workflow: audit.workflow.json | Lens: Review -->
# /review — Full-depth viewport review

Load and apply a complete viewport analysis to a piece of work. This is the deep review — it loads the full viewport file (CMO, CTO, or PM) and runs every check at full depth.

Use this when you want the quality assurance of the full recipe system without the ceremony.

---

## Usage

Specify the lens: `/review CMO`, `/review CTO`, or `/review PM`

You can also combine: `/review CMO CTO` (both lenses).

---

## MCP Tools Available

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| ~~**Semgrep**~~ — **DEPRECATED 2026-08** | — | Deprecated server-side. Only `mcp__semgrep__deprecation_notice` remains; every scanning tool is gone. Do not plan a static-analysis step around it until a replacement is wired |
| **Playwright** (`mcp__playwright__*`) | CMO lens (marketing surfaces), CTO lens (UI work) | Snapshot live page when reviewing marketing surfaces. Render generated HTML when reviewing UI commits |
| **Context7** (`mcp__context7__*`) | CTO lens — verify any library API the reviewed code calls actually exists in the installed version |
| **Supabase** (`mcp__supabase__*`) | CTO lens — verify the reviewed code matches the live schema. Read-only |

---

## Procedure

### Step 1 — Identify what's being reviewed

Ask (if not already clear):
1. **What are you reviewing?** (a draft from `/draft`, code from `/build`, a spec from `/spec`, or existing work)
2. **Which lens?** (CMO / CTO / PM / multiple)

**GATE — present for confirmation:**
> Reviewing: [asset] | Through: [CMO/CTO/PM lens] | Entity: [name]. Correct?

Wait for response.

### Step 2 — Load the full viewport

Read the complete viewport file:
- **CMO:** `viewports/cmo.md` — all 6 steps, all failure modes
- **CTO:** `viewports/cto.md` — all 6 steps, all failure modes
- **PM:** `viewports/pm.md` — all 6 steps, all failure modes

This is the ONE command that loads viewports. The other commands embed condensed governance — this one uses the full depth.

If entity context is needed and not already loaded, run the entity loading step (from `/entity`).

### Step 3 — Run the viewport audit

Follow the viewport's Step 6 audit exactly as written.

**CMO Audit** (from `viewports/cmo.md` Step 6):

| Check | Pass condition |
|-------|---------------|
| Tactical drift | No tactic selected before strategy was defined. No framework applied as template. |
| Generic framework | All framework choices derived from strategic analysis, not defaults. |
| Brand drift | Output is on-voice AND on-strategy. Locked lines correct. Banned patterns absent. |
| ICP drift | Output speaks to real person, not demographic. Uses their language. |
| Funnel fragmentation | Asset connects coherently to adjacent funnel stages. |
| AI writing patterns | Passes full 13-step universal writing guardrails sweep (`alc-group/writing-system/writing-guardrails.md` § 10). |

**CTO Audit** (from `viewports/cto.md` Step 6):

| Check | Pass condition |
|-------|---------------|
| Premature coding | No code before architecture was defined. |
| Pattern violation | All new code follows existing patterns. |
| Over-engineering | Complexity matches problem. No hypothetical abstractions. |
| Under-engineering | Error handling, validation, edge cases all present. |
| Architecture bypass | Data flows through intended layers. No shortcuts. |
| Security | No secrets, input validated, auth enforced. |
| Functionality | Demonstrably works through all three lenses below — not builds-and-tests-pass, which is Lens 1 alone. |

**PM Audit** (from `viewports/pm.md`):

| Check | Pass condition |
|-------|---------------|
| Scope adherence | Work matches the SOW. Nothing added. Nothing skipped. |
| Outcome delivery | Success criteria from the SOW are met (binary). |
| Constraint compliance | Timeline, budget, and platform constraints respected. |
| Milestone completion | Each milestone's acceptance criterion verified. |

### Step 4 — Produce the review

```
REVIEW: [lens] — [asset/file name]
Date: [YYYY-MM-DD]

OVERALL: [PASS / NEEDS WORK / FAIL]

[For each check:]
## [Check name] — [PASS / FAIL]
Evidence: [specific citation from the work being reviewed]
[If FAIL:] Fix: [exactly what to change]

SUMMARY:
- [X/Y checks passed]
- Priority fixes: [list in order]
- Recommendation: [approve / revise / rework]
```

---

## Chains to

- `/draft` — to revise copy based on CMO review findings
- `/build` — to fix code based on CTO review findings
- `/report` — to document the review

---

## Visual review — when the artefact has a diagram, wireframe or rendered page

Read `alc-group/brand-ops/templates/VISUAL-LANGUAGE.md` and check the marks, not only the argument:

- **Invented values.** Any colour, alpha, shadow, radius or blur not in the kit's
  `:root` is a defect. There is one tint at 6%, two shadows, radius 4/8/14/pill, and
  no glass beyond the sticky nav at 94% / 12px.
- **Containers around a workflow.** Lanes, bands, grid rows, summary columns or cards
  around a process are a defect. Glyph, label, time, line. Ownership is the glyph.
- **Wireframe headings written as real text.** Headings and body are greyboxed; only
  the section tag, eyebrow, CTA labels, field labels, tiles, embeds and footer carry
  words.
- **Invented data.** Figures, names or dates the source did not supply must be
  bracketed and visibly pending.
- **A register where a register does not belong.** Audits stamp. Strategies, research
  and proposals do not — they take a whole-document sign-off plus per-section
  Yes / Revise and notes.

State each as a finding with the file and line, then what to change.

## Output location

Save review document to:
`projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/DRAFT-REVIEW-v0.1-YYYY-MM-DD.md`

When approved: `APPROVED-REVIEW-YYYY-MM-DD.md`

---

## When to use this vs /audit

- `/audit` = lightweight, embedded checks, 7-point pass/fail, fast
- `/review` = heavyweight, loads full viewport, every check at full depth, thorough

Use `/audit` for daily work. Use `/review` for final quality gate before delivery.
---

## Universal Quality Layer

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the universal writing guardrails: `alc-group/writing-system/writing-guardrails.md`.

Covers AI-tells detection (banned vocab, bloated verbs, dead openings/transitions), negative parallelism (5A-5I), analogy and metaphor control (6), AU/UK spelling (11), and the 13-step sweep (10). Three or more patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Universal Quality Layer for the full enforcement protocol across phases.

---

## VERIFICATION — what "verified" means here

Canonical text: `command-includes/_VERIFICATION-STANDARD.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

This command is the final quality gate before delivery, so it is the one place a
Lens-1-only pass does the most damage. Verified means a person performed it and
watched the result. Anything else is untested, and the word "untested" appears in
the review output.

**Lens 1 — Code.** Builds, tests pass, types check, no console error, no unhandled
rejection, no silent catch. Proves it starts. Proves nothing is reachable, legible,
correctly placed, or connected to anything a person wants to do.

**Lens 2 — Visual.** Drive the real thing and judge the rendered result, not the
markup. Every reachable state at the stated viewports: empty, loading, populated,
error, and the ones nobody remembers — exactly one item, a very long value, a failed
request, a slow response. For anything without a screen, the subject is the artefact
it emits: the response body, the written file, the row that landed, the exit code.

**Lens 3 — Journey.** Walk each journey end to end by hand, in one sitting, as the
user who holds that journey's permissions. Every gesture performed, not asserted. No
shortcutting by URL, no seeding state through the API. Stop at the first gesture that
cannot be completed and report from there — a journey broken at step 3 of 9 is more
useful than nine checks reported green.

Twenty-four honest acceptance checks once passed on a canvas that could not join two
nodes, which was the entire product. The checks were not wrong; they were atomic, and
a product is not the sum of its gestures.

Every finding carries an evidence path — a defect nobody captured is a rumour. A lens
is never skipped for want of a surface; it translates. Skipping one is a recorded
decision naming which lens and why, never a silence.

**Probes are artefacts, not scratch.** `command-includes/_HARNESS-STANDARD.md` carries
the exit-code contract and the recurring probe types. Read the harness directory before
writing a new one. Exit `0` pass, `1` fail, `2` misconfigured — the third is not
decoration, because without it a broken probe reads as a passing product.

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
