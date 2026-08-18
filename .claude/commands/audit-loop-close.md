---
description: Close the Agentive Learning System loop.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/audit-loop-close.md — .claude/commands/audit-loop-close.md must match exactly -->
# /audit-loop-close — Close the Agentive Learning System loop

You are the system architect closing the feedback loop on the Agentive Learning System. The runner produces daily reports under `reports/daily/YYYY-MM-DD.md`. Each report names systemic recommendations across five passes (skill usage, skill quality, decision-making, repo quality, strategy gaps). Most recommendations sit unactioned.

This command reads the latest report (or a specified date), extracts every actionable recommendation, presents them as stamp-able decisions delivered via **email**, and ships the LOCKs as PRs on a separate pickup invocation.

This command is SELF-CONTAINED. It is the single authority when invoked.

---

## Two-mode operation

This command runs in one of two modes:

**GENERATE mode** (default) — extracts recommendations, writes HTML, emails the stamp surface to Andrew, ends the session. Andrew stamps in his own time.

**PICKUP mode** — triggered when invoked with pasted stamps or `pickup` keyword. Reads the previously generated HTML, parses stamps, ships PRs per blast radius.

Mode detection (Step 0):
- Invocation contains the word `pickup` or `--stamps` flag → PICKUP mode
- Pasted text in the invocation matches the stamp markdown pattern (lines containing `R\d+\s+\b(LOCK|REVISE|DROP|DEFER)\b`) → PICKUP mode
- Otherwise → GENERATE mode

If PICKUP mode is detected but no prior HTML is found at `projects/system-architecture/tasks/YYYY-MM-DD-audit-loop-close/`, STOP and ask: "No prior audit-loop HTML found for [date]. Run generate first, or specify a date."

---

## Canonical output scaffold (MANDATED)

Decision-bearing — every recommendation becomes a row Andrew has to stamp LOCK / REVISE / DROP / DEFER. **Start the HTML from `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`** (modules + Decision Register + Archive section + tagging UI). Never hand-write the brand CSS or invent a layout.

ID convention: `R1`, `R2`, ... for recommendations (`R` for recommendation).

If the canonical template is missing, STOP and ask. See `alc-group/brand-ops/templates/README.md`.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Re-running the audit logic instead of READING the existing report → **DUPLICATING THE RUNNER**
- Summarising the report in prose instead of extracting discrete recommendations → **NARRATIVE DRIFT**
- Inventing recommendations not in the report → **FABRICATION**
- Stamping recommendations yourself instead of presenting for Andrew → **AUTHORITY THEATRE**
- Skipping the email step and just opening the HTML locally → **STALE PATTERN** (replaced by email-led loop on 2026-05-20)
- Marking everything LOCK without per-row deliberation → **TICK-BOX BYPASS**
- Treating a "Recommendation" header in the report differently from a numbered finding → **SCOPE INCONSISTENCY**. Both are actionable. Extract both.
- Continuing to wait for stamps in the same session after sending the email → **BLOCKING THEATRE**. GENERATE mode ENDS after the email. PICKUP is a separate invocation.

---

# GENERATE mode

## Phase 1 — LOAD REPORT

### Step 1.1 — Pick the report

Default: the most recent file in `reports/daily/` (lexicographic sort gives the latest date).

If the user specifies a date (e.g. `/audit-loop-close 2026-05-13`), load that file instead.

Use `ls reports/daily/ | sort | tail -1` only when the user did not supply a date.

### Step 1.2 — Confirm + read

**GATE — present:**
> Report: `reports/daily/YYYY-MM-DD.md` ([size]KB, [N] sessions analyzed per its summary). Proceed?

Wait for response.

Then `Read` the file in full (do not paginate). Confirm:
- Total sessions analysed
- Repo health score
- Total violations
- The five pass sections are present

If any pass section is missing → flag and ask whether to continue partial.

---

## Phase 2 — EXTRACT RECOMMENDATIONS

### Step 2.1 — Scan all five passes

For each pass section, extract every actionable item. Sources include:
- `## Recommendations` blocks (numbered or bulleted)
- `### Top N` lists
- `### Priority Actions` tables
- Any **bold** sentence in a summary that names a fix
- Any item flagged as "Not actioned" or "Needs fix"

Do NOT extract:
- Observational findings without a fix ("Bash dominates at 51%" with no action)
- Statistics for context
- Quoted user prompts

For each extracted recommendation, capture:
- `id`: R1, R2, R3, ...
- `pass`: 1-5 (which pass surfaced it)
- `summary`: one-line impact (≤120 chars)
- `what`: the proposed fix in 2-3 sentences from the report
- `why`: the observation that drove it
- `risk`: blast radius if wrong (low/med/high), and what to mitigate
- `dependency`: any other R# that must land first
- `references`: source path(s) in the report (e.g. "Pass 1 §5 rec 2")

### Step 2.2 — Cross-reference with prior reports

Check the previous report (if exists). If a recommendation appears in BOTH reports and was not stamped LOCK previously → mark it `STALE` (age in days). Stale items get visual emphasis in the output.

### Step 2.3 — Cross-reference with already-shipped PRs

For each recommendation, search recent merged PRs (`gh pr list --state merged --limit 30`) for a closing reference. If a PR title or body addresses the recommendation, mark the row as `CLOSED-BY-PR-#N` so Andrew can stamp DROP rather than re-stamp something already shipped.

---

## Phase 3 — DRAFT DECISION HTML

Copy the canonical template (see §Canonical output scaffold). Populate:

- **Cover banner**: `Agentive Learning System · Recommendation Loop Close · YYYY-MM-DD`
- **Cover h1**: One sentence summarising the report's main systemic finding (pull verbatim from the report's summary or pass 1 lead)
- **Cover lede**: 2-3 sentences naming what the report found and how many recommendations need stamping
- **Decision register**: One row per recommendation. Each row:
  - `id`, `summary` (the ≤120 char hook), `Action` button group (LOCK / REVISE / DROP / DEFER)
  - Expandable detail: What / Why / Risk / Dependency / References / Note input
  - `CLOSED-BY-PR-#N` flag where applicable
- **Deliberately rejected section**: anything the report flagged as a fix the previous /audit-loop-close session DROPPED (for audit trail)
- **Refs section**: link to the source report, the runner's n8n workflow ID, and the Notion database

Output path: `projects/system-architecture/tasks/YYYY-MM-DD-audit-loop-close/DRAFT-v0.1-YYYY-MM-DD.html`

DO NOT `open` the file locally — the email step delivers it.

---

## Phase 4 — EMAIL NOTIFICATION (mandatory)

### Step 4.1 — Compose the email

Use the `Skill` tool with `gws-gmail-send` (already authed against `andrew@wolfandeagle.agency`).

**To:** `andrew@wolfandeagle.agency`

**Subject:** `[Audit Loop] YYYY-MM-DD · N recommendations to stamp`

**Body** (Markdown, rendered by Gmail):

```
Agentive Learning System — audit loop close, YYYY-MM-DD

[Report headline — verbatim from cover h1]

N recommendations to stamp across 5 passes.

PASS 1 — Skill Usage: R1, R2, R3, ...
PASS 2 — Skill Quality: R4, R5, ...
PASS 3 — Decision Making: R...
PASS 5 — Strategy Gaps: R...

Quick wins (low blast): R{ids}
Hot path / keystone: R{id} — {one-line why}
Already closed by recent PRs: R{id} → PR #{N}

To stamp, open the HTML:
file://projects/system-architecture/tasks/YYYY-MM-DD-audit-loop-close/DRAFT-v0.1-YYYY-MM-DD.html

When stamped, hit Copy in the browser, start a new Claude Code session, and run:
  /audit-loop-close pickup YYYY-MM-DD
…then paste the stamps.

Full report: reports/daily/YYYY-MM-DD.md
```

**Attach:** the HTML file itself (so the email is the durable backup).

### Step 4.2 — Send + confirm

Skill returns a message ID. Capture it.

State to the chat:
> Email sent to andrew@wolfandeagle.agency (Gmail message: <id>). HTML at: <path>. End of GENERATE mode. Stamp at your leisure, then run `/audit-loop-close pickup YYYY-MM-DD` in a fresh session.

End the session. Do NOT wait for stamps. Do NOT open the file locally.

---

# PICKUP mode

Triggered by `/audit-loop-close pickup YYYY-MM-DD` or by pasted stamps detected in the invocation.

## Phase 5 — PARSE + SHIP

### Step 5.1 — Read the prior HTML

Locate `projects/system-architecture/tasks/YYYY-MM-DD-audit-loop-close/DRAFT-v0.1-YYYY-MM-DD.html`. Read it to recover the recommendation register (id → what/why/risk/dependency/references).

If multiple drafts exist for the date, use the highest version number.

### Step 5.2 — Parse the stamps

Andrew pastes the stamp markdown directly into the chat. Lines look like:
```
R1 LOCK — note: fix this first, gate is theatre until it lands
R2 DROP — closed by PR #261
R3 DEFER — revisit 2026-06-15
...
```

Parse:
- `id` → R\d+
- `action` → LOCK | REVISE | DROP | DEFER
- `note` → everything after the em-dash

Reconcile against the recommendation register. Any recommendation without a stamp → flag as missing, ask Andrew before proceeding.

### Step 5.3 — Plan the work for each LOCK

For each LOCKed recommendation:
- Identify the target file(s) to modify (e.g. `slash-commands/cmo.md`, `~/.claude/hooks/skills-gate-v2.sh`, `skills/digital-marketing/<name>/SKILL.md`)
- Draft the change as a diff or new file
- Branch name: `audit-loop/YYYY-MM-DD-R{N}-{slug}`

### Step 5.4 — Group by blast radius

- **Low blast** (memory file edits, skill description tweaks, doc updates): bundle into one PR
- **Medium blast** (slash command edits, knowledge bank additions): one PR per recommendation
- **High blast** (hook changes, settings.json, ROUTER.md): one PR per recommendation, with explicit test plan

### Step 5.5 — Ship

For each PR group:
1. Create branch
2. Apply changes
3. Commit with format: `audit-loop: close R{N} — {recommendation summary} (report YYYY-MM-DD)`
4. Push
5. Open PR linking back to the source report and the audit-loop HTML

Andrew reviews and merges. He is the sole reviewer.

### Step 5.6 — Update DRAFT → APPROVED

Rename `DRAFT-v0.1-YYYY-MM-DD.html` → `APPROVED-YYYY-MM-DD.html`. The R# → action → PR# index lives inline in the HTML (a table or section near the end). No `.md` companion (per `feedback_everything_to_github_html_canonical`).

REVISE / DROP / DEFER decisions also recorded in the APPROVED file with Andrew's notes.

---

## Phase 6 — REPORT BACK

Post a one-screen summary to the chat:

```
Audit Loop Close — YYYY-MM-DD report
─────────────────────────────────────
Recommendations stamped: N
  LOCK:   N → PRs #X, #Y, #Z
  REVISE: N (with revised pattern)
  DROP:   N (incl. M already-closed by prior PRs)
  DEFER:  N (revisit date)
Stale items (carried from prior reports): N
Health-score delta since prior loop close: +/- N pts
```

Optional: send a second email summarising what shipped, replying to the original thread (subject: `Re: [Audit Loop] YYYY-MM-DD · N PRs opened`). Use `gws-gmail-reply` if the thread ID was captured.

Stop. The loop is closed for this report. Next run loads the next dated report.

---

## Cadence guidance

This command is designed for **weekly** invocation (every Sunday after the weekly Agentive Learning System deep-scan fires). Daily invocation is overkill; quarterly invocation is what the system audit found to be broken.

Pair with the session-start unresolved-items banner so any LOCKed-but-not-merged work stays visible day-to-day.

---

## Core Writing Standard

This command produces written output (HTML stamp surfaces, email body, PR descriptions on shipped LOCKs). Before any artefact is sent or merged, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md` (canonical rule source: `skills/copywriting/Proofread-Anti-AI-Standard.md`).

Pass 1 AusE spelling. Pass 2 anti-AI tells (em-dash misuse, stock vocab, false-balance, tricolons, generic openers/closers). Pass 3 brand hygiene (no emojis, no sales-negative, no invented frameworks). Three or more AI-tell patterns in one section equals full rewrite.

See `protocols/output-protocol.md` § Core Writing Standard for the cross-phase enforcement protocol.

---

## Change history

- 2026-05-17 — initial spec, single-flow HTML + chat paste-back
- 2026-05-20 — split into GENERATE / PICKUP modes; email delivery via `gws-gmail-send`; added cross-ref with merged PRs in Step 2.3 to avoid re-stamping closed items

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
