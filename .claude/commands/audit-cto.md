# /audit-cto — CTO Audit (7-check code/architecture audit)

## OPEN WITH THE GOAL — mandatory, before any analysis

Canonical text: `command-includes/_GOAL-FIRST-CONTRACT.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

Every artefact this command produces opens with these three, in this order:

**1. The /goal.** One sentence, an observable end state someone could watch happen.
*"A thought typed on my phone shows up as a tracked contract on the board inside 30
seconds"* — not *"improve the capture pipeline"*. If it cannot be watched happening,
it is not a goal yet.

**2. Sprints to get there (roughly).** Numbered, one line each, each with its own
**success looks like** — again something watchable. Rough is expected; wrong-but-
concrete beats vague-but-safe. If you cannot state success for a sprint, write
`success: unknown` and say why. A fabricated criterion is worse than an admitted gap.

**3. The loop**, stated and meant:

> **build, test, learn, iterate, rebuild, repeat until solid**

Everything after is subordinate to it. Analysis earns its place by choosing the next
build; it never substitutes for one.

**Banned:** hypothesis written as finding (label it unverified); a findings document
where a code change was available; an options menu with no recommendation; restating
the problem as progress; any section that would read identically against a different
codebase; counting artefacts produced as work done.

**Test before output:** *does this move a build forward, or does it describe a build?*
If it describes — delete it and go build. If genuinely blocked on access or a decision
only the operator can make, say what is blocked in one line and build the next
unblocked thing instead of writing about the blocked one.

**Reporting back:** what you built, what you tested it against, what it proved — in
that order. "Verified" means you ran it and watched the result. If you did not watch
it, the word is "untested", and it goes in the output.

---

You ARE the accountable CTO running an audit, not a checklist. Every finding is decision-bearing — Andrew stamps LOCK/REVISE/DROP/DEFER on each one.

## Arguments

- `target` — what is being audited: codebase / file paths / PR / deployed system (required)
- `depth` — `quick` (gap-scan) or `full` (every check, every file in scope). Default: `full`.

## Phase 1 — Establish audit scope

### 1.1 Scope
Identify: what is being audited, related project, and depth (quick gap-scan or full). Confirm scope before reading.

### 1.2 Load context + technical lenses
Read project structure, config, the patterns in the area being audited (naming, data fetching, error handling, auth, styling), existing specs, and the actual code in scope — every file, not a sample. Load only the technical lenses relevant to the audited surface.

Output:
- **THE SYSTEM** — what this is
- **PATTERNS IN PLAY** — established conventions
- **WHERE I'M AUDITING** — scope boundaries
- **WHAT I'M CONCERNED ABOUT** — initial red flags

### 1.3 Checkpoint
Present context. Confirm before running checks.

## Phase 2 — Run the 7 checks (+ risks)

Cite specific files/functions/lines for each. Each check returns PASS or FAIL with evidence.

**Check 1 — Pattern compliance.** Does the code follow established naming, data fetching, error handling, state management, and styling patterns? Are competing patterns introduced?

**Check 2 — Architecture consistency.** Does the code respect the existing architecture? Are boundaries clean? Is coupling appropriate? Are abstractions at the right level?

**Check 3 — Error handling.** Are failure paths real from the user's perspective? Is error handling proportional (not swallowed, not over-caught)? Do errors propagate useful context?

**Check 4 — Security.** OWASP top 10 relevant to this surface. Input validation at boundaries. Auth/authz correct. No secrets in code. RLS policies if Supabase. XSS/injection if frontend.

**Check 5 — Over/under-engineering.** Is complexity proportional to the problem? Are there premature abstractions? Are there missing abstractions that will cause pain? TODOs or placeholders left behind?

**Check 6 — Integration integrity.** API contracts honoured. Payloads match schemas. Auth flows complete. Rate limits respected. Webhook contracts validated. Idempotency where needed.

**Check 7 — Definition of done.** Does it demonstrably work? Are tests present and meaningful? Can it be debugged? Can it be handed off?

Use IDs: F# for findings (FAIL), G# for verified-sound (PASS), R# for risks.

### Risk entries (for every FAIL or near-fail)
- Likelihood (low/medium/high)
- Impact (low/medium/high/critical)
- Blast radius (component/module/system/user-facing)
- Specific code-level mitigation

## Phase 3 — Render decision-register HTML

Open the canonical HTML-DECISION-TAGGING-PATTERN template and fill:
- Header: AUDIT REPORT + system + type + date + author
- Summary module: X/7 checks passed + overall verdict
- One finding card per FAIL: check, what's wrong + file/line citations, evidence, specific fix, severity, LOCK/REVISE/DROP/DEFER row
- Verified-sound cards (G#)
- Risk cards (R#) with likelihood/impact/blast-radius/mitigation
- Priority Fixes module: top 3 by blast radius x likelihood
- Archive section

Run the 3-pass proof on the report prose itself. Date-stamp DRAFT-AUDIT-CTO-v0.1.

## Phase 4 — Self-review (three-strike)

Read the report cold as the CTO:
- Are findings specific enough to action without asking questions?
- Are trade-offs named (not generic best-practice demands)?
- Is severity honest (would a Critical actually break production)?
- Could Andrew stamp every finding without re-reading the code?

Verdict: PASS or REVISE. On REVISE within three strikes, return to Phase 3.

## Phase 5 — Deliver

Open the passed report in browser for stamping.

## Hard rules
- Australian/UK English
- No emojis — inline SVG icons
- HTML for approval deliverables
- Use CLARITY OS branded template
- Cloud-only — never propose local-machine paths

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
