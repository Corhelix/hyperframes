---
name: review
description: Review a deliverable through the relevant viewport lens.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a finished deliverable, PR or artefact is judged through a viewport
  does_not_fire_when:
    - the work is being produced rather than judged -> the producing command
    - a full technical audit is wanted -> /audit-cto
  loads:
    always:
      - viewports/audit.md
      - command-includes/_VERIFICATION-STANDARD.md
      - command-includes/_HARNESS-STANDARD.md
      - viewports/cmo.md
      - viewports/cto.md
      - viewports/pm.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: verdict
      is: approve, approve with changes, or hold, with the specific defect for each change
    - id: evidence
      is: a path per finding; a defect nobody captured is a rumour
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: cmo-verify

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
