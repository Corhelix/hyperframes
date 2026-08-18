<!-- Source: .claude/commands/build-plan.md | Workflow: plan-and-build.workflow.json | Phase: govern | Emits: workflow-v1 twin -->
# /build-plan — Generate and govern the one build-plan work-order for a thread

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

You own delivery of a build thread across many sessions. This command kills two recurring failure modes:

1. **Document sprawl.** One thread ends up with a handoff `.md`, a SOW, and a build plan — three artefacts that drift, disagree on what they are, and force a "this is the plan the last one wasn't" redo. (Reproduced live in the client-intake thread, 2026-07-17: `HANDOFF-v1.md` + `DRAFT-SOW-v1.html` + `DRAFT-BUILD-PLAN-v0.2.html`, one tagged `data-object-type="sow"` while titled "Build Plan". This is the `/auto-sow` F2 finding in the wild.)
2. **Wandering, and thin plans.** A session opens, half-reads the context, invents its own plan, drops the buildable spec that matters (screens, states, data model, RPC contracts, auth), and builds something that was never agreed.

The fix is one artefact and one command that owns both ends of it.

## The core principle — a SOW and a build plan are two altitudes of ONE artefact

- The **work-order altitude** reads top-to-bottom, the surface Andrew reviews: Purpose · Scope (in/out) · Deliverables · Work breakdown + acceptance · Dependencies · Milestones · Roles · Governance.
- The **build altitude** lives underneath, in the *same* document: the screen inventory + states, components, data model, API/RPC contracts, auth, architecture, per-task file map and verification.
- Generated **once** from the source (a PRD chain, a strategy HTML, a handoff `.md`, or an audit), fresh-read in order, re-strategising nothing. Updated **in place**. One thread → one plan → one branch.

`/build-plan` GENERATE writes that one artefact. GOVERN reads it and works the thread against it. There is never a second "SOW".

Invocation: `/build-plan <thread>` · `/build-plan <thread> next` · `/build-plan <thread> status` · `/build-plan <thread> render`. `<thread>` is a module (`m7`), a thread folder, or a path to the source handoff/strategy/PRD.

---

## STEP 0 — FRESH-READ GATE (mandatory, before anything else)

Nothing — no status claim, no "next task", no edit — happens until the real sources have been read *this session, in the order the plan gives*.

1. **Resolve the thread and its home.** One thread = one folder = one branch. The plan lives in that folder — a module folder (`docs/modules/m<N>-*/`) or a dated thread folder under `docs/reports/<date-slug>/`, `docs/strategy/<date-slug>/`, or `docs/audits/<date-slug>/`. Code-side threads live in `clarity-os-app`. If ambiguous, list candidates and ask. Never guess.
2. **Read the plan if it exists** → GOVERN. If not → GENERATE.
3. **Read the Source of truth, in order.** The plan's ordered source list, or (generating) the handoff/strategy/PRD's ordered links. **If a PRD chain exists** (`PRD-1-DISCOVERY`, `PRD-2-UX`, `PRD-3-BUILD`), those are primary sources — read them. **Read the real code and boot the real app** where a task touches UI; never build or judge from a summary.
4. **Read the Settled list and the ADRs it cites.** Locked inputs, not open questions. Do not re-litigate them.
5. **GitHub over local for currency.** For "current state / latest / what changed", confirm against GitHub (`gh api`, `git log origin/main`), not the local clone. On conflict, GitHub wins — pull fresh.

If you are about to state status, name a next task, or edit the plan without having done the above this session — stop. That skip is the drift.

---

## Enforcement — making the fresh-read bite (real hooks only)

Prose gates are skippable, and this is the command whose job is to stop skipping. Enforcement here uses hooks that actually exist in this workspace — do NOT reference a `cmo-gate.js` or `.cmo-active` marker; that hook is not wired here, and pointing at it is authority theatre.

- **The session entity+skills gate is already live.** `skills-gate-v2.sh` blocks every Write/Edit until this session has written its entity + skills markers (it fires on the first plan write). A plan cannot be authored from a session that skipped setup — real, and free.
- **The fresh-read proof is a required artefact, not a claim.** Before the GENERATE write, write `<thread-dir>/framing-<YYYY-MM-DD>.md` containing, in this order: the ordered list of sources you actually read this session; the goal + success metric lifted from them; and a **coverage line** naming which ⚑ sections apply to this thread and confirming each is filled. Where `frame-gate-v1.sh` is wired it enforces this file on the write; where it is not, the file is still the required, inspectable proof — no framing, no plan.
- **Human turn before it lands.** The plan is presented for browser review and not committed until Andrew replies (the standing SHOW-BEFORE-COMMIT rule) — that is the confirmation gate, not a bespoke marker.

GOVERN reads and status edits are never gated.

---

## DRIFT DETECTION — read before acting

You are drifting if you are:
- Acting from the handoff summary without reading the real files/code it points to → **SUMMARY DRIFT**. Read the sources, in order. Boot the app.
- Producing a second SOW/plan/handoff for a thread that already has one → **DIVERGENCE** (the F2 defect). One artefact. Update it in place; never ship a rival document.
- Writing a plan that omits screens/states/data-model/contracts/auth when the thread has UI or data → **ABSTRACTION DRIFT**. That omission is exactly what forced intake `v0.2`. Carry the build altitude.
- Producing a thinner parallel screen/schema list when a PRD-2/PRD-3 already exists → **PRD DIVERGENCE**. Reference the PRD and lift its rows; do not re-derive a weaker copy.
- Working a task that is not the next unblocked one in plan order → **SCOPE JUMP**.
- Adding a deliverable/phase no source calls for → **SCOPE INVENTION**. Log it as an open decision; do not silently build it.
- Re-opening anything on the Settled list or in an ADR → **RE-LITIGATION**. Locked. Raise a successor explicitly if it genuinely must change.
- Marking a task done on assertion, not evidence (dry-run green, a screenshot vs the reference screen, a merged PR, a live row) → **STATUS THEATRE**. Verify, then mark.
- Ignoring a named gotcha (`.rpc()` not `.from()`, `extensions.digest(...)`, "autosave-failed must be visible + retryable") → **GOTCHA DRIFT**. Gotchas are acceptance criteria.
- Emitting a plan whose tasks are not `workflow-v1` nodes (no `upstream`, no typed `output_schema`, no `execute → audit` pairing) → **NODE DRIFT**. A plan that can't topo-sort or barcode is not a handoff — it is a document the inbuilt system can't run.

**Self-test at each gate:** Read the ordered sources (and booted the app if UI) this session? Exactly one governing artefact? Does it carry the build altitude — screens, states, data model, contracts, auth? Can I point to the plan line that authorises this task? Is every done backed by evidence? If any answer is no → go back.

---

## MCP Tools Available

GOVERN reconciles against live state and verifies before marking done; GENERATE reads current code. Use these — do not narrate availability.

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Supabase** (`mcp__supabase__*`) | GENERATE (data model), GOVERN reconcile + verify | Inspect real schema, RLS, row counts before writing a data-model section or marking a DB task done. Read-only; never mutate during reconcile |
| **Context7** (`mcp__context7__*`) | GENERATE (architecture), GOVERN work-the-task | Verify any library API a task calls exists in the installed version before the plan asserts it |
| **Playwright** (`mcp__playwright__*`) | GOVERN verify-before-done for UI | Screenshot the rendered surface against the reference screen; the verification a UI task's done-when names |

**Rule:** a task marked done on runtime behaviour needs a live observation via the right MCP, not an inference from static code.

---

## Agent Spawning Protocol

GENERATE reads many sources in order and boots apps (the intake source alone is 7 files across repos). Fan those reads out to cheap agents so the governing thread's context stays clean. Agents do NOT inherit CLAUDE.md or the tool rules — lead every agent prompt with the preamble.

- **Model per spawn:** `haiku` for reading/scanning/summarising a source; `sonnet` for drafting a plan section from already-loaded context; `opus` only for the hard sequencing/architecture call.
- **Preamble, verbatim, at the top of every agent prompt:** "TOOL DISCIPLINE: Use the Grep tool (not Bash grep/rg) for content search. Use the Glob tool (not Bash find) for file discovery. Use Read with limit/offset (not Bash cat/head/tail) for file inspection. Never use Bash for file reads, searches, or discovery."
- **Return ≤800 words.** The agent's raw reads stay in its own context; only the distillate reaches this thread.

---

## The artefact — the two-altitude work-order

One file per thread, in the thread's folder. Branded HTML on the CLARITY OS template, carrying `artefact-v1` metadata (ADR-0017): `data-schema-id="artefact-v1"`, `data-object-type="build-plan"`, `data-run-id`, `data-entity-id`, `data-client-id`, `data-project-id`, `data-workstream`, `data-version`, `data-date`, `data-status`, `data-confidence` — the ids every barcode and node emission inherits. It ships with a runnable `workflow-v1` twin (next section), so the same plan is both reviewable by Andrew and executable by Hermes without rework.

**Versioning (one file, in place — never a `-v0.1-`/`-v0.2-` chain):** name it the house way but WITHOUT a version integer — `DRAFT-<thread>-BUILD-PLAN-YYYY-MM-DD.html`, where the date is the **creation** date and is NOT re-minted per edit. Revisions update that same file in place; the living version + last-reconciled date live INSIDE as `data-version` / `data-date` (as the M7 doc does), bumped in place. The only rename is the single `DRAFT- → APPROVED-` at sign-off. A new `-v0.2-` file, or re-minting the filename date on each edit, is a second document — the DIVERGENCE this command exists to kill.

**Machine-readable status (so GOVERN never hand-edits branded HTML):** the artefact carries one status block that both the render and the reconcile read and write:
```html
<script type="application/json" id="plan-state">
{ "version":"0.1", "date":"YYYY-MM-DD", "last_reconciled":"YYYY-MM-DD",
  "tasks":[ {"id":"T1","status":"done","evidence":"PR #66 merged"},
            {"id":"T2","status":"blocked","blocker":"apply M0 after review"} ] }
</script>
```
The page carries a tiny inline script that reads `#plan-state` on load and paints each row from it, so the JSON is the SINGLE source and the visible rows are derived — never a second hand-maintained copy that can desync:
```html
<script>
const S=JSON.parse(document.getElementById('plan-state').textContent);
S.tasks.forEach(t=>{const el=document.querySelector(`[data-task="${t.id}"]`);
  if(el){el.dataset.status=t.status; const p=el.querySelector('.status'); if(p)p.textContent=t.status;}});
</script>
```
GOVERN edits ONLY the JSON block; rows repaint on next open. Status is data, not a manual CSS edit. Status vocabulary: **done** (evidence on main/live), **in-flight** (branch/PR, unmerged), **blocked** (waiting on a dependency/decision), **not-started**.

**Section order.** Work-order altitude in the open; build altitude carried as first-class sections, not a clause. Sections marked ⚑ are MANDATORY when the thread has a UI or a data model; the framing **coverage line** (see Enforcement) must name which ⚑ sections apply and confirm each is filled — that is how completeness is checked, not a machine gate. **Scale to the thread** — sections are as-needed, not a quota: a small single-surface, no-data thread collapses to Goal · Source · Settled · Scope · State · Work breakdown · Run log. If the plan needs more than a handful of phases, the thread is too big — split it.

1. **Goal + success metric** — one sentence, plus the measurable success number lifted from discovery. The whole-plan acceptance.
2. **Source of truth** — read these first, in order. Verified-live links/paths. **List the PRD chain (PRD-1/2/3) here when it exists** — the plan references and lifts from it, never re-derives it.
3. **Settled — do not relitigate** — the locked decisions carried from the source (D0–D6 / OTP-not-GHL / port-as-written class).
4. **Scope** — in, and explicitly out.
5. **State** — what is done *and verified* (with the evidence), plus the named gotchas the next session will hit.
6. ⚑ **Screen inventory** — every screen, grouped. Per screen: its **5 states** (empty / loading / populated / error / edge), the data it reads/writes, and the exact **RPC/endpoint it calls**. Lift from PRD-2 §1/§3 where it exists; else read the real instrument/app.
7. ⚑ **Components** — build or reuse, each with the reference component to mirror (e.g. `MonitorPage`). From PRD-2 §4.
8. ⚑ **Interaction & validation contract** — forms, validation timing + error display, save/loading/notification behaviour, destructive-action confirms. From PRD-2 §5. Named UX gotchas (e.g. visible-retryable autosave) live here as acceptance criteria.
9. ⚑ **Data model / schema** — tables, columns, RLS, indexes, DDL. From PRD-3 §2 / read live via Supabase.
10. ⚑ **API / RPC contract** — each endpoint/RPC: input, validation, response, error shape, auth. From PRD-3 §3.
11. ⚑ **Auth model** — provider, session, roles, protected routes. From PRD-3 §4 + the Settled list.
12. ⚑ **Architecture / data-flow** — the request path (client → RPC → store → UI), not just repo ownership. From PRD-3 §1.
13. **Work breakdown & acceptance** — the WP/task table (work-order altitude): each task's deliverable, dependency, **done-when**. Under each task, the file map + verification + gotcha. Tasks **lift the rows** from the sections above and the PRD — they do not restate them thinly.
14. **Dependencies & open decisions** — needed-from-Andrew vs assumed; flag what is *not* needed for the next milestone so the build isn't falsely blocked.
15. **Ground rules / cross-cutting** — the governance every task inherits (below).
16. **Landing map** — which repo/system owns which piece.
17. **Risk register** — risk · source · the mitigation *in the code*.
18. **Run log** — append-only, newest first: what moved, which PR/commit, what blocker appeared.

Responsive + accessibility (PRD-2 §6/§7) fold into the Interaction contract or the relevant screen rows; carry them where the thread has a client UI.

---

## Hermes-runnable output — the `workflow-v1` twin (node-based, barcoded)

The plan is not only for Andrew to read — it must drop into the inbuilt execution system (Hermes `workflow-run-hermes` + `engine/cmo_engine/executor.py`, ADR-0058; slash-command→workflow port precedent ADR-0045) with **no rework**. So GENERATE emits, beside the human HTML, a runnable node graph: `<thread>-BUILD.workflow.json` (`schema_version: "workflow-v1"`). The Work Breakdown tasks and the workflow nodes are the SAME list in two projections — task `Tn` ↔ node `id` — so the twin can never diverge (DIVERGENCE extends to it). Contracts are pinned in `docs/strategy/2026-07-20-build-plan-hermes-alignment/research/` (read those before authoring the twin).

**Workflow (top level):** `schema_version:"workflow-v1"`, `workflow_id`, `name`, `version`, `status`, `source_commands`, `related_adrs`, `inputs` (typed), `tier_policy` (`default_tier`/`premium_tier`/`mid_tier`/`free_tier` + `per_node_overrides` + `max_premium_calls`/`fallback_on_quota`), `execution` (`runner_skill:"workflow-run-hermes"`, `default_backend`, `fallback_backend`), `per_node_emission` (`enabled:true`, `schema:"node-v1"`, `emit_timing:"at_node_completion"`, `barcode_format`, `output_path_template:"hermes-ops/runs/{run_barcode}/nodes/{node-id}-{node-seq}.json"`, `surfaces`), `nodes[]`, `edges[]` (`{from,to,when?}`).

**Each task → one node:**
```json
{ "id":"T3", "type":"execute", "execution_kind":"ai", "label":"Autosave endpoint + retry",
  "tier":"mid", "model":null, "human_gate":false,
  "upstream":["T2"], "context_refs":["T1"],
  "prompt_template":"…", "output_schema":{ "files":"array", "rpc":"string", "verified":"boolean" },
  "on_fail_reroute_to":null }
```
- `type` = semantic_type (`frame|brand|task|research|execute|audit|output|custom`); `execution_kind` (`ai|mcp|fan_out|emit|audit`) derives from `type` if omitted; `mcp` nodes add `tool`.
- `upstream[]` is the DAG (from task deps) — the runner topo-sorts on it; prose sequencing will not sort.
- `output_schema` is the task's **done-when as a validatable contract** — the runner sets `output_schema_valid` against it. This is where the ⚑ build-layer sections (screens/schema/API) become machine-checkable.
- `human_gate:true` + `gate_note` on any node needing sign-off (SHOW-BEFORE-COMMIT points); `tier`/`model` feed `tier_policy` resolution (multi-provider rule).

**The review→redo→continue loop is declared, not invented** — it already lives in `executor.py` (`max_reroutes=2`) and the runner's three-strike `audit` (ADR-0040/0058/0060). Pair every `execute` (build) node with an `audit` node whose `on_fail_reroute_to` points back to the execute node; the executor reroutes on `decision_state:"revise"|"failed"`, carries `feedback` forward, up to 2 retries, then stops `failed`. That IS "contextual agent reviews, redoes, continues" — structure the plan as `execute → audit` pairs, never a bolt-on. **Scoring** = `output_schema_valid` + the audit node's `decision_state`; **error handling** = `decision_state` + `on_fail_reroute_to`. The runner owns both.

**Barcodes + stamps (declared here, emitted at run):** the HTML plan carries `artefact-v1` (ADR-0017); each node emits `node-v1` AT COMPLETION (ADR-0040 Part D — non-negotiable) → `ea_node_emissions` (ADR-0068) + `hermes-ops/runs/{barcode}/nodes/`, barcode `RUN-YYYY-MM-DD-{ENTITY}-{WORKFLOW}-{SEQ}/NODE-{id}-{seq}`. The plan declares the nodes; `workflow-run-hermes` emits the barcodes when it runs them.

**Passable-handoff acceptance (in the framing coverage line):** the twin validates against the runner's required fields — `schema_version`, `workflow_id`, `name`, `nodes[]` each with `id`/`type`/`label`/`upstream`, `edges[]`, `tier_policy`, `execution.runner_skill`, `per_node_emission`. If it would not topo-sort, or a node lacks `output_schema`, it is NOT passable — fix before handoff.

---

## GENERATE mode — write the one artefact from the source

Only when no build plan exists for the thread.

1. **Read the source, in order** (STEP 0). Where a PRD chain exists, it is the primary source — reference it, lift its rows. Where it does not, boot the app and read the real code so screens, field counts, RPC names and schema are true, not summarised. (The intake `v0.1→v0.2` gap was a summarised instrument; the fresh read found 72 fields + the missing resume RPCs.)
2. **Write the fresh-read proof** (Enforcement above): `<thread-dir>/framing-<date>.md` — sources read in order + goal + success metric + the ⚑-coverage line. No plan is written without it.
3. **Write both altitudes into one artefact, plus the runnable twin.** Fill every section; the ⚑ sections are mandatory when the thread has UI/data. Seed the `plan-state` block. Emit the `workflow-v1` twin (every task a node; `execute → audit` pairs). Never emit a separate SOW.
4. **Seed State from reality, not optimism.** Cross-check each task against real git/live state. Done only with evidence; else not-started/in-flight/blocked. Record gotchas.
5. **Present, don't commit.** Show the render for browser review. Land it (branch → PR → your review → merge) only on Andrew's word. Nothing to `/tmp`; it lives in the thread folder.

---

## GOVERN mode — hold the plan and work the next task (default)

When a plan exists. The loop every build session runs.

### 1 — Reconcile
Read the `plan-state` block; compare against real state (git on `origin/main`, open PRs via `gh`, live Supabase rows). Report drift and correct the block to truth:
> Plan says T4 in-flight; PR #66 open + unmerged → confirmed in-flight.
> Plan says T2 not-started; commit `abc123` on main implements it → correcting to done.
> Two artefacts found (SOW-v1 + plan-v0.2) → DIVERGENCE; consolidate into this one, retire the rival.

### 2 — Readout (always show)
```
<thread> — <one-line goal>   (metric: <success number>)
Done: <n>  In-flight: <n>  Blocked: <n>  Not-started: <n>
Next unblocked task: <id> — <task>
Blocked: <id> — <task> (waiting on <blocker>)  |  not needed for next milestone: <ids>
Open decisions: <id> — <the call needed>
```

### 3 — Work the next task (when asked, or invoked with `next`)
- Take the **single next unblocked task** in plan order. Not a later easy one. Not three at once.
- Read the real code / boot the real app for that task first. Honour its named gotchas — acceptance criteria.
- Hand the build to `/build`, `/cto`, or `/n8n` (this command governs; those execute), or do it inline if trivial. Respect the Settled list, the ADRs, and the ground rules.
- If the task needs a decision not in the source → stop, log it as an open decision, surface it. Do not freelance it.
- **Verify against the done-when before marking done** — dry-run green, screenshot vs the reference screen, a passing run. Not assertion.

### 4 — Write back (end of every working session)
- Update the task's status in the `plan-state` block; re-render. Append one Run-log entry (newest first).
- Bump `data-version` / `last_reconciled`.
- Reflect material state changes up into `docs/module-status.md`.
- Branch → PR → browser review; nothing pushed or merged until Andrew has reviewed the render.

---

## Sub-modes

- `<thread> status` — STEP 0 + GOVERN 1–2 (reconcile + readout from `plan-state`). No building.
- `<thread> next` — STEP 0 + GOVERN 1–3.
- `<thread> regenerate` — rebuild from the source (GENERATE), preserving the existing Run log + `plan-state` history. Use when the plan has drifted from its source.
- `<thread> render` — re-render the current plan (and its `plan-state`) to HTML for browser review.

---

## Ground-rule gates (baked into every task)

- **Read real code / boot the real app.** Never build or judge UI from a summary.
- **Verify DB work by transactional dry-run, then ROLLBACK. Additive only** — no deletes on the shared Supabase; new tables/RPCs, partial indexes, scoped lookbacks.
- **Branch → PR → browser review → merge.** Nothing merged or applied to live until Andrew has reviewed the render. Nothing to `/tmp`; work lands in the thread folder.
- **Settled = locked.** The Settled list and ADRs are inputs; a change is raised explicitly as a successor, never quietly absorbed.
- **Hermes-operable + multi-provider + light-theme-only** apply to any code the tasks produce (per the cockpit rules and `reference_clarity_os_design_system`).

---

## What this command does NOT do

- PRD discovery / UX / build spec → `/prd-discovery`, `/prd-ux`, `/prd-build`. This command **consumes** their output as a source and lifts it into the plan; it does not replace them.
- Strategy → `/strategise` (a source for GENERATE).
- Architecture decisions → `/cto` (ADRs are law here).
- Writing the actual code / workflow → `/build`, `/cto`, `/n8n`.
- Stampable build-queue SOW dispatch → `/auto-sow`. **Boundary rule:** a thread with a build plan governs through `/build-plan`; `/auto-sow` is only for stamping a build-queue SOW where no plan governs. Never run both on one thread — that is the divergence.

---

## Core Writing Standard

This command produces written output. Before any draft is presented, written to disk, or rendered to HTML, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md`. Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene (no emojis — inline SVG icons in HTML renders). Three or more AI-tell patterns in one section equals full rewrite, not find-and-replace.

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
