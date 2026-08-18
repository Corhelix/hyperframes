---
description: CFO workflow: pull the live numbers, run the review, and return a decision with owners. Modes: review / cashflow / decision / report.
argument-hint: "[review | cashflow | decision | report] [context]"
---
<!-- slash-commands/cfo.md is canonical; .claude/commands/cfo.md must match exactly | Skill: virtual-cfo | Phase: analysis -->
# /cfo — Virtual CFO

Run one of four CFO workflows against live Xero data. This is the analysis layer:
it explains what the numbers mean and what to do next. It does not post entries,
lodge anything, or give a statutory tax position.

**Load `.claude/skills/virtual-cfo/SKILL.md` before Step 1.** It carries the
operating rules, the three standing checks and the standard output. This command
sequences the work; the skill governs how it is done.

---

## Modes

| `$1` | Runs | Reads |
|---|---|---|
| `review` | Monthly or quarterly close and review | `monthly-close.md` |
| `cashflow` | Rolling 13-week direct cash forecast | `cashflow-13-week.md`, `scenario-analysis.md` |
| `decision` | Business case: hire, spend, price, borrow, buy | `decision-modelling.md`, `scenario-analysis.md` |
| `report` | One-page management report, or a board or lender pack | `management-reporting.md`, `board-and-owner-reporting.md` |

No mode given: ask which, do not guess. The four produce different artefacts and
running the wrong one wastes a full data pull.

---

## Procedure

### Step 1 — Frame it

Establish, and do not proceed on assumption:

1. **Which entity?** Wolf & Eagle is the only connected Xero organisation. If
   the answer is anything else, stop and run the intake block in SKILL.md.
2. **Which period?** State it explicitly. Every figure downstream inherits it.
3. **What decision does this feed?** A review with no decision attached is a
   filing exercise.

**GATE — present for confirmation:**
> CFO [mode] · Entity: [name] · Period: [from]–[to] · Decision: [what this feeds]. Correct?

Wait for response.

### Step 2 — Prove the connection before quoting anything

```sh
cd companies/wolf-and-eagle/finance/xero
set -a; . ~/.config/xero/.env; set +a
.venv/bin/python check_scopes.py
```

This is not ceremony. A Xero Custom Connection fails the entire token mint if one
requested scope is missing, so a missing scope kills the pull rather than
degrading it.

**If `accounting.transactions.read` or `accounting.reports.read` are off:** say so
plainly, name the two-tick fix, then follow the skill's third standing check.
Find what *is* live and build the partial answer from it. Payroll is enabled even
when the accounting scopes are not, which gives real wages, PAYG withholding and
super. Stopping at the gap is only right once there is no live path to a usable
answer.

### Step 3 — Pull

```sh
.venv/bin/python cfo_pack.py --out-dir /tmp/cfo-<period>
```

**Read `manifest.json` first.** A failed pull leaves no file, and an absent file
read as a zero is how a wrong number reaches a report. Carry every failure into
the output as a named gap.

For `decision` mode a full pack is often unnecessary; pull what the decision
turns on.

### Step 4 — Run the mode

Follow the reference file for the mode. Do not improvise a structure; these
shapes exist so this month's output is comparable to last month's.

Run the three standing checks from SKILL.md regardless of mode:
working capital whenever a balance sheet is in hand, money-that-is-not-yours
stated even without figures, and what-is-live before reporting any gap.

### Step 5 — Label every explanation

**confirmed** (traced to a source), **probable** (consistent with the data, not
proven), or **needs investigation**. An unlabelled explanation reads as fact and
will be acted on as one.

The temptation in a review is to explain every movement. An honest "this moved
and I do not yet know why, here is how I will find out" beats a plausible story,
because the plausible story stops the investigation.

### Step 6 — Output

Standard output block from SKILL.md. Every recommendation carries an owner and a
date. Close with both source blocks: what was used, and what is still needed.

**GATE — before writing any file:**
> [N] figures, [N] labelled probable, [N] actions, [N] accountant questions. Write to a document, or leave in thread?

### Step 7 — Document, if asked

Build from `brand-ops/templates/CLARITY-OS-TEMPLATE.html`. Never from a prior
one-off and never invent CSS. Route the PDF through `html-to-a4-pdf`.
File under `alc-advisory/projects/YYYY-MM-DD-<task-slug>/drafts/` per the naming
SOP.

---

## Hard rules

**Never invent a number.** Every figure traces to a pull, a named file, or a
stated assumption. An admitted gap gets fixed; an invented figure gets acted on.

**Read `ReportDate`, never the filename.** The cached
`balancesheet-2026-06-30.json` carries a report date of 16 June 2026. Two
evaluation runs quoted it as year-end and both were wrong.

**Never substitute a cached export for a live pull** and present it as current.
Quote it with its pull date attached, or not at all.

**Read-only.** This command does not write to Xero. If the analysis concludes
something must be recoded or journalled, that is a recommendation with an owner,
routed through `accounting-and-tax`.

**Redact.** No tax file numbers, no full bank account numbers, no customer
personal details in any deliverable.

**Route, do not restate.** GST codes, BAS mechanics, PAYG, super rates, FBT and
lodgement dates belong to `accounting-and-tax`; raw pulls to `xero-accounting`;
the R&D claim to `rd-tax-offset`; entity structure to `small-business`. Never
quote a rate or due date from memory. Read
`systems/accounting/sources/anchors.json` and check its `checked_at`.

**Stop and route to the registered agent** for final tax positions, BAS sign-off,
payroll and super compliance conclusions, statutory accounts, restructuring,
trusts, Division 7A, related-party transactions, PSI, FBT, capital gains,
property, foreign income, crypto, or any arrangement whose main purpose is the
tax outcome.

---

## GATE MECHANICS — the hooks that will deny you

Canonical text: `command-includes/_GATE-MECHANICS.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

**Arm the frame gate in Phase 1, before any analysis.** `frame-gate-v1.sh` is
inert without `.frame-required`, so skipping this does not run the command
ungated by design — it runs it ungated by accident, and every write in the
session goes unchecked. Write the marker into this session's marker dir (the
SessionStart hook injects the exact path):

```bash
echo '{"kind":"system","codebase":"<path>","target":"<path>"}' > "<session-marker-dir>/.frame-required"
```

Release it only when the analysis is genuinely complete, with both fields true:

```bash
echo '{"kind":"system","target":"<codebase>","framing_locked":true,"all_six_complete":true,"frame_spec_ref":"derived","as_of":"YYYY-MM-DD","timestamp":"<ISO8601>"}' > "<session-marker-dir>/.frame-locked"
```

**The other three markers.** `.entity-loaded` (or `no-entity` for platform work)
and `.skills-approved` gate every Write and Edit via `skills-gate-v2.sh`. Legacy
`.claude/.entity-loaded` and `.claude/.skills-approved` paths are ignored.

**Load order, enforced on reads.** `command-load-order-gate.py` arms off the
operator's typed prompt, not off anything the model does. A denied Read is the
gate working: present the Step 1.1 gate and stop. Escape hatch:
`CLARITY_LOAD_ORDER_GATE=off`.

**File home, enforced on writes.** `clean-path-gate.py` allows only
`~/Documents/CLEAN/<repo>/<path>`, and since 2026-08-14 the first segment must be
a real repo — in `repo-map.json` or present on disk with a `.git`.

**Tool discipline, enforced on Bash.** `block-bash-fileops.py` denies `cat`,
`head`, `tail`, `grep` and `find` in every pipeline position, including
`/usr/bin/grep`, `\grep`, `env grep`, `xargs grep` and `bash -c "cat ..."`. Use
Read, Grep and Glob. Bound payload with Read's `offset`/`limit` or Grep's
`head_limit` — piping into `head` is denied, and the inline
`BASH_FILEOPS_BYPASS=1` prefix does not work.

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
