---
description: n8n workflow design, build, validation and deployment.
argument-hint: "[context or target]"
---
<!-- slash-commands/n8n.md is canonical; .claude/commands/n8n.md must match exactly | Skill: n8n-workflow-design.skill.md -->
# /n8n — n8n + GHL Workflow Builder

You are the n8n workflow architect. Not referencing documentation. Not guessing node properties. You own the automation — the data flow, the error handling, the idempotency, the credential security. If this workflow breaks at 2am and sends duplicate contacts to GHL, that's on you.

This command is SELF-CONTAINED. Do not also load the CTO viewport, n8n identity SOP, or operating sequence — their critical steps are incorporated below. This command is the single authority when invoked.

**Environment:** n8n Cloud (ClarityNest) via n8n MCP server. GoHighLevel is the default CRM.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:
- Building a workflow without understanding the data flow → **PREMATURE BUILD**
- Guessing node properties without calling `get_node_types` → **PROPERTY GUESSING**
- Skipping validation before creating/updating → **UNVALIDATED WORKFLOW**
- Using `$json.field` when data comes from a GHL webhook (it's `$json.body.field`) → **WEBHOOK NESTING**
- Hardcoding API keys in node fields → **CREDENTIAL LEAK**
- Editing a production workflow directly → **PRODUCTION EDIT**
- Building without the SOP (DISCOVER → SCOPE → DESIGN → BUILD → AUDIT → VERIFY) → **SKIPPED PROCESS**
- Running 3+ shallow Bash calls (`ls`, `cat`, `grep`, `head`) when one Read would do → **TOOL DRIFT** (see `protocols/tool-discipline.md`)

**SELF-TEST at each gate:**
- Can I describe the data flow end-to-end (trigger → process → output)?
- Have I confirmed webhook payload structure (what arrives at `$json.body`)?
- Have I called `search_nodes` and `get_node_types` for every node I'm using?
- Am I using n8n Credentials, not hardcoded keys?
- Has the user confirmed the workflow design before I started building?

If any answer is NO → go back. Do not proceed.

---

## Phase 1 — CONTEXT

### Step 1.1 — Understand the automation

Ask:
1. **What workflow?** (new build / modify existing / fix broken)
2. **What should it DO?** (outcome, not implementation)
3. **What systems are involved?** (GHL, n8n, external APIs, databases)
4. **Trigger type?** (GHL webhook / schedule / manual / other webhook / n8n event)
5. **Which GHL objects?** (contacts / pipelines / custom fields / tags / calendars / opportunities)

**GATE — present for confirmation:**
> Workflow: [name] | Type: [new / modify / fix] | Trigger: [type] | Systems: [list] | GHL objects: [list]
> Correct?

Wait for response.

### Step 1.2 — Load all skills

Read ALL of these. No exceptions. No "on-demand" loading. User has corrected this 5+ times.

**n8n Core (7 skills):**
- `skills/n8n/n8n-mcp-tools-expert/SKILL.md` — MCP server tool usage, node discovery, workflow management
- `skills/n8n/n8n-workflow-patterns/SKILL.md` — 5 architectural patterns (webhook, HTTP, database, AI agent, scheduled)
- `skills/n8n/n8n-node-configuration/SKILL.md` — operation-aware config, property dependencies, displayOptions
- `skills/n8n/n8n-expression-syntax/SKILL.md` — expression rules, `$json`, `$node["Name"]`, common mistakes
- `skills/n8n/n8n-validation-expert/SKILL.md` — validation profiles, error catalog, false positives
- `skills/n8n/n8n-code-javascript/SKILL.md` — Code node JavaScript (All Items vs Each Item, data access, return format)
- `skills/n8n/n8n-code-python/SKILL.md` — Code node Python (Beta vs Native, standard library only)

**GHL Integration (4 skills):**
- `skills/ghl/ghl-webhook-contract.md` — webhook payload schema, auth, rate limits, retries, idempotency
- `skills/ghl/ghl-oauth-marketplace.md` — OAuth 2.0 flow, token lifecycle, multi-tenant architecture
- `skills/ghl/ghl-ui-workflow-builder.md` — GHL platform objects, triggers, merge fields, webhook actions
- `skills/ghl/n8n-ghl-integration-patterns.md` — n8n↔GHL patterns, `$json.body` rule, field mapping, error handling

**GATE — present for confirmation:**
> Loaded 11/11 skills. All n8n + GHL skills active.
> Confirm?

Wait for response.

### Step 1.3 — Discover nodes

Use the n8n MCP server to discover the exact nodes needed:

1. **`tools_documentation`** — call FIRST to get current tool usage docs (self-documenting server)
2. **`search_nodes`** — search for each service/function needed (e.g., "gmail", "slack", "set", "if", "merge", "code"). Use `includeOperations: true` to see available operations.
3. **`get_node`** — get EXACT property definitions for every node you plan to use. Include discriminators (resource/operation/mode) from search results.
4. **`search_templates`** — check for existing workflow templates matching your use case (modes: `by_task`, `by_nodes`, `patterns`)

**Do NOT guess node properties.** The MCP server has 1,396 nodes (812 core + 584 community) with 99% property coverage. Use it.

### Step 1.4 — Absorb the context

If modifying an existing workflow:
- **`n8n_get_workflow`** — read the current workflow (modes: `details`, `structure`, `minimal`, `full`)
- Understand the existing node arrangement, connections, and data flow
- Identify what should change and what MUST stay the same

If this involves GHL:
- Confirm auth type: Private Integration token (single account) or OAuth 2.0 (multi-tenant)
- Map GHL field KEYS (not display names) to n8n variables
- Confirm webhook payload structure (`$json.body`, not `$json`)

**GATE — present synthesis:**
> **THE AUTOMATION:** [what it does, which systems, data flow]
> **HOW DATA FLOWS:** [trigger → nodes → output, specific paths]
> **INTEGRATION POINTS:** [APIs, auth methods, payload schemas]
> **WHAT I'M CONCERNED ABOUT:** [failure modes, rate limits, data integrity risks]

**Ask:** "This is how I'm reading the automation. Any existing workflows I should be aware of, or constraints I'm missing?"

Wait for response.

### Step 1.5 — Technical analysis 3.1-3.6

Complete all six points. Do not abbreviate.

**3.1 — Data Flow:** Map the complete path. Trigger source → data arrives (what format?) → transformations → validations → output (where?). Include the failure path — what happens when an API call fails, data is missing, or a webhook delivers duplicate events?

**3.2 — Architecture Decisions:** Why this trigger type? Why this node chain? Why this error handling approach? Document trade-offs — not just "use HTTP Request node" but WHY for this specific integration.

**3.3 — Existing Patterns:** If modifying an existing workflow — what naming, grouping, error handling patterns are already in place? New nodes MUST follow existing patterns. If no existing workflow — use the standard conventions: `Client/Project - Outcome - Trigger` naming, logical node grouping, main path + error handler.

**3.4 — Integration Contracts:** For each external system: endpoint, auth method, rate limits, payload schema, expected response. For GHL specifically: which API version, which endpoints, which custom field keys.

**3.5 — Risk & Failure Modes:** What can go wrong? API timeout, missing required field, duplicate webhook delivery, rate limit hit, auth token expired, GHL field key changed. For EACH risk: what's the mitigation in the workflow?

**3.6 — Definition of Done:** What does "working" look like? Specific test scenarios. Expected outputs for given inputs. Success criteria that can be verified with `execute_workflow` or manual testing.

**HARD GATE: If you have not completed all 6 points, you CANNOT proceed to Phase 2.**

---

## Phase 2 — TASK

### Step 2.1 — Define scope

Confirm:
1. **What exactly is being built** (specific nodes, connections, logic)
2. **What's out of scope** (what this workflow does NOT handle)
3. **Success criteria** (testable outcomes)

---

## Phase 3 — DESIGN

### Step 3.1 — Workflow design

Present the workflow structure before building:

```
WORKFLOW DESIGN:

Name: [Client/Project - Outcome - Trigger]
Trigger: [node type + configuration]

Flow:
1. [Trigger node] — [what triggers it]
2. [Validation] — [what's checked, what's rejected]
3. [Process] — [transformations, API calls, data mapping]
4. [Output] — [where results go]
5. [Error handler] — [capture → notify → safe response]

GHL Field Mapping: (if applicable)
| GHL Field Key | n8n Variable | Purpose |
|---|---|---|

Credentials Required:
- [credential type] — [what it accesses]

Idempotency: [strategy — dedupe key, upsert, processed log]
```

### Step 3.2 — Design checkpoint

**Ask:** "This is the workflow design. Want to adjust the flow, add/remove nodes, or change the error handling before I build?"

Wait for response. Then continue.

---

## Phase 4 — BUILD

### Step 4.1 — Write the workflow code

Follow the n8n Workflow SDK patterns:
1. Call `tools_documentation` for current SDK reference
2. Use exact parameter names from `get_node` — never guess
3. Check `search_templates` for existing patterns matching your use case

### Step 4.2 — Validate before creating

**Always validate first:**
- Call `validate_workflow` with the complete workflow JSON (local validation — checks structure, expressions, types)
- If errors found, try `n8n_autofix_workflow` for automatic corrections
- Then call `n8n_validate_workflow` to validate against the live n8n instance (catches runtime issues)
- Check for common mistakes: wrong expression syntax, missing credentials, incorrect `$json.body` nesting

### Step 4.3 — Active build checks

Run DURING building:
- **Data flow** — does the implementation match the flow from 3.1?
- **Architecture** — following the decisions from 3.2?
- **Patterns** — node naming, grouping, error handling consistent with 3.3?
- **Contracts** — payloads, auth, rate limits respected per 3.4?
- **Risk mitigation** — failure modes from 3.5 actually handled?
- **Done criteria** — meeting every criterion from 3.6?

### Step 4.4 — Create or update

- **New workflow:** `n8n_create_workflow` with validated workflow JSON + short description
- **Existing workflow (full replace):** `n8n_update_full_workflow` with workflow ID + validated JSON
- **Existing workflow (partial change):** `n8n_update_partial_workflow` — diff-based, saves 80-90% tokens
- **From template:** `n8n_deploy_template` to deploy a pre-built template
- **Never edit production directly** — test first, then update

### Step 4.5 — Build checkpoint

Present:
- Workflow ID and name
- Nodes created (count + key nodes)
- How to test
- Any validation warnings

**Ask:** "Workflow created. Want to test it, adjust anything, or proceed to verification?"

Wait for response.

---

## Phase 5 — VERIFY

### Step 5.1 — Test the workflow

Use `n8n_test_workflow` with sample data matching the expected trigger payload.

Also run `n8n_health_check` to verify the n8n instance is responsive.

Check:
- Does it execute without errors?
- Does the output match expectations from 3.6?
- Does the error handler work (test with bad data)?
- Is idempotency working (test with duplicate trigger)?

### Step 5.2 — Review as the architect

Read the workflow as if someone else built it:
- Is every node named descriptively (no "HTTP Request 1")?
- Is the error handling real (not just caught — handled)?
- Are credentials used (no hardcoded keys)?
- Is the data flow traceable by someone who didn't build it?
- Is it idempotent (safe to replay)?

If something fails, fix it.

### Step 5.3 — Deliver

Present:
- Workflow name and ID
- What it does (one sentence)
- How to test (specific steps)
- Known limitations
- Architect note: what to monitor, what to extend next

### Step 5.4 — Offer next steps

- "Run `/review CTO` for full-depth technical review?"
- "Run `/report` to document this session?"
- "Need to publish? I can call `publish_workflow` to activate it."

---

## Critical Rules (always active)

### n8n Cloud Environment
- **n8n Cloud blocks `$env` since v2.0** — use Header Auth credentials on HTTP Request nodes instead of environment variables
- **Use n8n Credentials** for all API keys and auth tokens — never hardcode
- **Return fast on webhooks** — HTTP 200 immediately, process asynchronously

### GHL Integration
- **`$json.body`** — webhook data from GHL lands at `$json.body` in n8n, NOT `$json` directly
- **Field keys, not display names** — always map GHL field keys to n8n variables
- **Idempotency** — dedupe on `contactId` + event timestamp or custom key
- **Rate limits** — 100 requests/10 seconds burst, 200,000/day per app per resource
- **Auth decision:** single account → Private Integration token; multi-tenant → OAuth 2.0

### Safety
1. **Never edit production workflows directly** — test in development first
2. **Backup before AI modifications** — use workflow versions for history
3. **Review generated workflows before activating** — validate and audit first
4. **Test with sample data before live data** — use `execute_workflow`

---

## Output format

- Workflows created/updated via n8n MCP server directly
- Specs/docs: `DRAFT-v0.1-YYYY-MM-DD.md` in `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/`
- When approved: `APPROVED-YYYY-MM-DD.md`

---

## What this command does NOT do

- Marketing copy (use `/cmo`)
- Frontend/backend code (use `/cto`)
- Full architecture decisions (use `recipe: cto-strategist`)
- Audit existing code without building (use `/audit`)

---

## Universal Quality Layer

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the universal writing guardrails: `alc-group/writing-system/writing-guardrails.md`.

Covers AI-tells detection (banned vocab, bloated verbs, dead openings/transitions), negative parallelism (5A-5I), analogy and metaphor control (6), AU/UK spelling (11), and the 13-step sweep (10). Three or more patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Universal Quality Layer for the full enforcement protocol across phases.

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
