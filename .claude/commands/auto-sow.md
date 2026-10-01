---
name: auto-sow
description: Generate a stamp-able SOW, HTML plus JSON, for the build queue.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a stamp-able SOW is generated for the build queue
  does_not_fire_when:
    - the plan itself is still unsettled -> /plan or /build-plan
  loads:
    always:
      - command-includes/_GOAL-FIRST-CONTRACT.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: sow_html
      is: a stampable SOW in the branded template, ready for the build queue
    - id: sow_json
      is: the machine-readable twin matching sow-schema.json
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: .claude/commands/auto-sow.md | Workflow: sow-build.workflow.json -->
# /auto-sow — Generate a stamp-able SOW for the build queue

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

Generates a tabbed HTML SOW Andrew stamps in the browser before dispatch. Writes both the operator surface (SOW.html) and the machine contract (SOW.json) to `builds/queue/<slug>/` on the `build-queue` branch.

This command does NOT write a finished SOW. Andrew writes the SOW by stamping the surface this command generates.

---

## When to run

When you want to dispatch a build and need to produce the SOW Claude will execute. Replaces hand-writing SOW.md.

Usage:
```
/auto-sow [output_type] [slug]
```

Examples:
```
/auto-sow workshop-section eai-section-6-narrative
/auto-sow audit clarity-os-build-queue
/auto-sow strategy-doc mtm-pricing-architecture
/auto-sow                                          # no args — proposes from latest Reflect
```

Valid `output_type` values: `workshop-section`, `audit`, `page-copy`, `prd`, `report`, `code-module`, `strategy-doc`.

---

## STEP 0: FILE-HOME GATE (MANDATORY, before any Write, Edit, or render)

No output is written until this thread has a home in the real repo. The home exists first, so nothing is ever dumped to `/tmp`, a scratchpad, a worktree, or an invented "central" folder. Positive routing, not clean-up after.

Do all four before producing anything. Do not Write, Edit, or render until they are done.

1. **GitHub first.** Resolve current state and any referenced files from GitHub (`gh api`), not the local clone. Local is trusted only after it matches HEAD; on any conflict, GitHub wins, so pull fresh.
2. **Resolve and confirm the home.** From the client / entity / task, resolve the owning repo and area from `protocols/repo-map.json` (the one lookup), or this command's own declared output target if it has one (`/auto-sow` files to `builds/queue/<slug>/` on the `build-queue` branch). Propose the dated, terminology-rich folder (`<repo>/<area>/tasks/YYYY-MM-DD-<slug>/`) and get a one-line confirm. Confirmed, never assumed.
3. **Create it in the real checkout.** `mkdir -p` that folder inside the actual repo working tree. Never `/tmp`, never `~/Documents/.worktrees`, never a folder you invented.
4. **Cut the thread's branch.** If already on a non-main, non-`capture/*` feature branch whose thread folder is present, keep it and skip the cut. Otherwise `git fetch origin main`, then `git checkout -b <type>/<slug>-YYYY-MM-DD origin/main` (types: `feat|fix|docs|chore|context`). Every output for this thread lands in the step-3 folder on this branch; the capture-all safety net then commits to this branch, not a shared one.

Only when all four are done, proceed. On handoff, commit the thread's folder and open the PR. Nothing is pushed, PR-opened, or merged until Andrew has reviewed the render in his browser.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Asking 5 questions and accepting whatever Andrew types → **REACTIVE WIZARD**
- Pre-filling outcome with "improve the system" or audience with "users" → **VAGUE INTAKE**
- Skipping the required-ref-set for the chosen output_type → **REF GAP**
- Writing the SOW directly without opening the stamp surface → **NO STAMP GATE**
- Marking the SOW as committed without checking that all gates passed → **PREMATURE COMMIT**
- Running 3+ shallow Bash calls (`ls`, `cat`, `grep`, `head`) when one Read would do → **TOOL DRIFT** (see `protocols/tool-discipline.md`)

**SELF-TEST at each gate:**
- Does the output_type match a sow-types/*.json template?
- Did I pre-fill from latest Reflect (compounding intelligence)?
- Did I reject vague Brief entries?
- Did I write SOW.html AND SOW.json (both, or neither)?
- Did I open the file in browser and tell Andrew the stamp URL?

If any answer is NO → go back. Do not proceed.

---

## MCP Tools Available

This command writes SOW.html for Andrew to stamp in the browser. Use these MCPs where they apply:

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Playwright** (`mcp__playwright__*`) | Before writing SOW.html to `builds/queue/<slug>/` | Render the generated SOW.html, snapshot, verify the tabbed stamp UI loads, the canonical template renders, and no CSS regressions. If render fails, fix before pushing to the `build-queue` branch |
| **Context7** (`mcp__context7__*`) | When the SOW body references library APIs | Pull current docs for any library API named in the SOW. Stops SOWs from queuing builds against deprecated/non-existent endpoints |

**Rule:** the SOW.html must render cleanly in Playwright before the `build-queue` push. A SOW that won't render is a SOW Andrew can't stamp.

---

## Phase 1 — INTAKE (gathered, then validated)

### Step 1.1 — Resolve args

Parse arguments:
- If both `output_type` and `slug` provided → use them.
- If only `output_type` provided → propose a slug from current date + ask for short-description.
- If neither provided → read latest 3 entries from `builds/reflect/` and propose the next-recommended-SOW. If no Reflect exists, ask explicitly: "What output_type? What slug?".

Validate `output_type` against the enum. Reject if not in list — point at the 7 valid types.

### Step 1.2 — Load output-type template

Read `protocols/templates/sow-types/<output_type>.json`. This carries:
- `_meta` — what this SOW type does
- `required_refs` — minimum ref set Andrew must lock
- `sub_tasks` — the pre-filled handoff chain

If the file doesn't exist for the chosen output_type, flag it as a missing template — do not proceed. Suggest creating it as a new SOW.

### Step 1.3 — Pre-populate Brief from context

Read in parallel:
- `MEMORY.md` — for entity / locked-decisions context
- `builds/reflect/` — last 3 Reflects (for `next-recommended-SOW` hints)
- If output_type is entity-bound (workshop-section, page-copy, prd): also read `protocols/entity-repo-map.md` to find the entity's locked-lines + ICP files

Pre-fill these Brief fields where possible:
- `working_folder` — derived from entity → repo path (or asked if unclear)
- `voice_register` — from entity tone.md if entity-bound, else "system-only"
- `target_repo_branch` — `Corhelix/<repo> @ build-queue`

Do NOT pre-fill `outcome`, `audience`, `strategic_intent`, `final_state_criteria` — these MUST come from Andrew. Vague pre-fills produce vague SOWs.

### Step 1.4 — Confirm with Andrew (the only intake gate)

Present a tight 4-line intake:

```
output_type: workshop-section
slug:        2026-05-04-eai-section-6-narrative
working_folder: ../client-projects/serve-with-clarity/clients/effective-aid/brand-kit/
voice_register: Quiet Builder

Tell me:
1. outcome (verb + object + measurable shift, one line)
2. audience (specific role/ICP)
3. strategic_intent (what shift this output must produce)
4. final_state_criteria (numbered, verifiable — one per line)
5. anything explicitly out of scope?
```

Wait for Andrew's response. If any answer is vague, push back ONCE per field with the specific reason it failed validation. Do not accept on second try if still vague — flag as INTAKE-FAILED and stop.

---

## Phase 2 — BUILD (generate SOW.html + SOW.json)

### Step 2.1 — Build SOW.json from template + intake

Take the sow-types JSON template + Andrew's Brief inputs. Replace `<working_folder>`, `<slug>`, `<n>`, `<prev>`, etc. placeholders in:
- `required_refs[].path_pattern` → resolved absolute paths
- `sub_tasks[].output_path` → resolved absolute paths
- `sub_tasks[].action` → fully-resolved instructions

Validate the resulting object against `protocols/templates/sow-schema.json`. Any schema violation → fix or ask. Do not proceed with invalid SOW.json.

### Step 2.2 — Render SOW.html from SOW-TEMPLATE.html

Read `protocols/templates/SOW-TEMPLATE.html`. Replace placeholders:
- `{{slug}}`, `{{date}}`, `{{output_type}}`, `{{outcome}}`, `{{strategic_intent}}`, `{{audience}}`, `{{voice_register}}`, `{{working_folder}}`, `{{target_branch}}`, `{{final_state_criteria}}`, `{{out_of_scope}}`
- `{{required_set_hint}}` — generated from sow-types/<type>.json `required_refs` purpose_hints
- `{{refs_rows}}` — pre-populate one row per required_ref (tag + suggested path + purpose, verdict empty for Andrew to stamp LOCK)
- `{{subtasks_rows}}` — pre-populate one row pair (summary + detail) per sub_task from the template, verdict empty

### Step 2.3 — Write to local + commit to build-queue

Local write path:
```
projects/<entity-or-task>/tasks/<YYYY-MM-DD-slug>/
  SOW-DRAFT-v0.1.html
```

Then commit to GitHub via `gh api`:
```bash
# Get build-queue branch sha
SHA=$(gh api "repos/Corhelix/Agent-and-Config-Files/branches/build-queue" --jq '.commit.sha')

# Write SOW.html to builds/queue/<slug>/SOW.html
gh api --method PUT "repos/Corhelix/Agent-and-Config-Files/contents/builds/queue/<slug>/SOW.html" \
  -f message="auto-sow: queue <slug>" \
  -f branch="build-queue" \
  -f content="$(base64 < SOW.html)"

# Write SOW.json sibling
gh api --method PUT "repos/Corhelix/Agent-and-Config-Files/contents/builds/queue/<slug>/SOW.json" \
  -f message="auto-sow: queue <slug> (machine contract)" \
  -f branch="build-queue" \
  -f content="$(base64 < SOW.json)"
```

### Step 2.4 — Open in browser + report

Run `open <local-path>/SOW-DRAFT-v0.1.html` so Andrew can stamp.

Tell Andrew:
- The local path opened
- The remote path on `build-queue` branch
- What he needs to stamp before dispatch:
  - Every Brief field (required)
  - At least the required ref set per output_type
  - At least one sub-task LOCK'd
- That clicking "Commit to queue" copies SOW.json to clipboard for the dispatch trigger

---

## Phase 3 — POST-STAMP (after Andrew clicks Commit)

When Andrew pastes the SOW.json back into chat after stamping:

1. Validate the pasted JSON against `sow-schema.json`. Any failures → flag specific fields.
2. Re-write `builds/queue/<slug>/SOW.json` on `build-queue` branch with the stamped version (overwrite).
3. Confirm to Andrew: "SOW <slug> committed. Trigger Workflow A from n8n when ready."

Do NOT trigger Workflow A automatically. Dispatch is Andrew's call.

---

## Output locations

- Local draft (Andrew stamps): `projects/<entity-or-task>/tasks/<date>-<slug>/SOW-DRAFT-v0.1.html`
- Remote queue (post-stamp): `builds/queue/<slug>/SOW.html` + `SOW.json` on `build-queue` branch
- After Workflow A picks up: moves to `builds/active/worker-N/`
- After build complete: archives to `builds/done/<slug>/`
- Reflect: `builds/reflect/<slug>-REFLECT.html` written by close ceremony

---

## What this command does NOT do

- Trigger Workflow A (manual — Andrew's call)
- Run the build (Workflow A → runner → Claude does that)
- Approve the SOW (Andrew stamps in browser; this command never auto-approves)
- Hand-write SOW content (it generates the stamp surface; Andrew writes by stamping)

---

## Universal Quality Layer

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the universal writing guardrails: `alc-group/writing-system/writing-guardrails.md`.

The SOW HTML carries acceptance criteria, sub-task actions, and Brief fields — all written output, all subject to AU/UK spelling, banned vocab sweep, and the 13-step pass.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
