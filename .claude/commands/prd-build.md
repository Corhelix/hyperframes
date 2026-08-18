<!-- Source: .claude/commands/prd-build.md | Workflow: prd-assembly.workflow.json | Phase: build -->
# /prd-build — PRD Stage 3: Architecture, Data & Milestones

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

You are the Product Lead wearing the CTO hat. This is Stage 3 of 3. Stage 1 defined who and why. Stage 2 defined what they see and do. This stage answers: **how is it built, what's the data model, what are the risks, and what does done look like?**

By the end of this stage, a developer has everything: the problem (Stage 1), the UX (Stage 2), and the technical blueprint (this stage). No guessing required.

Requires PRD-1-DISCOVERY.md and PRD-2-UX.md from previous stages.

5 phases: context → task → skills → execute → quality gate.

---

## Canonical output scaffold (MANDATED)

PRDs are dense with decisions — architecture choices, data model decisions, risk acceptances, milestones, acceptance criteria. Every one becomes a row Andrew has to stamp LOCK / REVISE / DROP / DEFER. **Always start the HTML output from `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`** (modules + Decision Register + Archive section + tagging UI). Never hand-write the brand CSS or invent a layout — copy from the canonical and fill placeholders. ID convention: `D` decisions · `R` risks · `M` milestones · `T` tasks · `S` schema/sections · `Q` open questions.

If the canonical is missing, STOP and ask. See `alc-group/brand-ops/templates/README.md` for selection rules.

---

## Rationalisations

<!-- Source: addyosmani/agent-skills · MIT
     skills/test-driven-development/SKILL.md @ f17c6e8 (vendored 2026-05-18)
     Pattern lifted: "Common Rationalizations" two-column table.
     Content adapted to /prd-build phases (architecture / data / milestones). -->

Common excuses for skipping Stage 3 rigour, with rebuttals.

| Thought | Reality |
|---|---|
| "Architecture is implied by the stack." | 3.2 trade-offs must be named. "We use React" is not a decision; the data-fetch + state + auth patterns within React are. |
| "Data model can be figured out in code." | Migration debt starts here. PRD-3 names the tables, columns, RLS, indexes. |
| "Auth is later, building UI first." | Auth model is foundation. Defer it and every screen has to be retrofitted for permissions. |
| "We can refactor after MVP." | Don't design for hypothetical futures — but don't pretend "for now" either. Lock the boundary that will hold for the next 6 months. |
| "Definition of done is obvious for each milestone." | Obvious is unstated. Unstated is unmeasurable. Every milestone gets a checkbox list. |
| "Stack rationale: we already use Supabase." | "Why for THIS project" is the rationale, not "what we already use". Document the project-specific reason. |
| "API contracts will emerge from the build." | They never emerge — they get assumed. PRD-3 fixes the contract before the build. |

## Red Flags

Stop signs. Do not stamp PRD-3 APPROVED if any of these is true.

- Data model section missing or noted as "TBD"
- Auth decisions deferred to a later doc
- Milestones without a definition-of-done checklist
- Stack choices stated without the "why for THIS project" rationale
- API contracts assumed instead of defined (shapes, error codes, auth)
- Architecture rows (`D`-tagged) with no Context7 verification when they cite library APIs
- Schema rows that don't match the existing repo's actual Supabase tables (when audited via MCP)
- Risks without mitigation in the code (named risks without mitigations are decoration — same rule as /cto)

---

## MCP Tools Available

This stage produces a decision-bearing HTML PRD. Use these MCPs where they apply:

| MCP | Where it plugs in | Use for |
|-----|-------------------|---------|
| **Context7** (`mcp__context7__*`) | Phase 1.2 (Load technical context), Architecture decisions | Pull current library docs (Supabase, React 19, Tailwind v4, Trigger.dev) before locking architecture rows. Stops the PRD shipping hallucinated API references |
| **Supabase** (`mcp__supabase__*`) | Data model decisions, schema rows | Inspect actual columns + RLS on existing repos before authoring schema rows. PRD data model must match reality. Read-only |
| **Playwright** (`mcp__playwright__*`) | Phase 5 (Quality gate) | Render the generated PRD HTML, snapshot, validate the canonical template renders cleanly across viewports before APPROVED stamp |

**Rule:** every architecture decision row (D-tagged) that names a library API must have been verified via Context7 in the same session, or stamped as `REVISE` for verification.

---

## Phase 1 — CONTEXT

### Step 1.1 — Load Stage 1 + Stage 2

Read PRD-1-DISCOVERY.md and PRD-2-UX.md from the task folder. These are your foundation.

If either doesn't exist: **stop.** "Run `/prd-discovery` and `/prd-ux` first — I need the problem definition and UX spec before defining architecture."

### Step 1.2 — Load technical context

If codebase exists: read project structure, package.json, existing patterns, database schema, API routes, auth setup. Understand what's already built.

If greenfield: note that — all decisions are open.

### Step 1.3 — Context checkpoint

```
BUILDING: [product]
UX SCREENS: [count from Stage 2]
USER FLOWS: [count from Stage 2]
EXISTING STACK: [what exists — or "greenfield"]
CONSTRAINTS: [from Stage 1 — budget, timeline, platform]
```

**GATE — present for confirmation:**
> PRD Build: [product] | Stage 1+2 refs: [file paths]. Correct?

Wait for response.

---

## Phase 2 — TASK

Think through as the CTO:
- What's the simplest architecture that supports every screen and flow from Stage 2?
- What patterns already exist? Follow them unless there's a compelling reason to diverge.
- Where does data live? How does it flow from database to UI and back?
- What's the auth model? Who can see/do what?
- What will break? What happens when it breaks?
- What's the deployment model? How does this get to production?

---

## Phase 3 — SKILLS

Propose skills from:
- `frontend/senior-fullstack.md` — architecture patterns, data layer, code review
- `frontend/senior-frontend.md` — React patterns, state management
- `product/prd-builder.md` — acceptance criteria
- `qa-testing/senior-qa.md` — test strategy
- `knowledge-bank/product-management.md` — product strategy

**Ask:** "These are the skills I'd use. Add, remove, or swap?"

---

## Phase 4 — EXECUTE

Write **PRD-3-BUILD.md** with these sections:

### 1. System Architecture

```
STACK:
- Frontend: [framework, version, why]
- Backend: [framework/serverless, why]
- Database: [type, service, why]
- Auth: [provider, model, why]
- Hosting: [platform, why]
- Key dependencies: [list with rationale]

ARCHITECTURE PATTERN:
[Describe the pattern — monolith, serverless, microservices, etc. WHY this pattern for this product.]

DATA FLOW:
[How a request moves from user click → API → database → response → UI update. Trace the primary flow end-to-end.]
```

Trade-offs: for every choice, name what you're trading away.

### 2. Data Model

For each entity in the system:

```
[Entity Name]
├── id: uuid (PK)
├── [field]: [type] — [what it stores, why]
├── [field]: [type] — [constraints, defaults]
├── created_at: timestamp
├── updated_at: timestamp
└── Relationships:
    ├── belongs_to: [Entity] (FK: [field])
    └── has_many: [Entity]

RLS Policy: [who can read/write, conditions]
```

Include:
- Every table / collection
- Relationships (foreign keys, join tables)
- Row-level security policies (who can access what)
- Indexes (what queries need to be fast)
- Migrations strategy (how schema evolves)

### 3. API Contract

For each endpoint or server action:

```
[METHOD] /api/[route]
  Auth: [required / public]
  Input: { [field]: [type], ... }
  Validation: [what's checked, when]
  Response (success): { [field]: [type], ... }
  Response (error): { error: string, code: string }
  Rate limit: [if applicable]
```

Or if using Server Actions:

```
[actionName](input: [type]): Promise<[type]>
  Auth: [required / public]
  Validation: [what's checked]
  Success: [what's returned]
  Error: [what's thrown]
  Revalidation: [what cache is invalidated]
```

### 4. Auth & Permissions

```
AUTH MODEL:
- Provider: [Clerk / Auth0 / custom]
- Session: [JWT / cookie / token]
- Sign-up flow: [email + password / social / magic link]

ROLES:
- [Role 1]: can [actions]. Cannot [actions].
- [Role 2]: can [actions]. Cannot [actions].

PROTECTED ROUTES:
- /dashboard/* → requires auth
- /admin/* → requires admin role
- /api/* → requires auth (except /api/public/*)
- / → public
```

### 5. Integration Points

For each external service:

```
[Service Name]
- Purpose: [what it does in this system]
- API: [endpoint pattern]
- Auth: [how we authenticate — API key, OAuth, webhook secret]
- Rate limits: [what they are, how we handle them]
- Failure mode: [what happens when it's down — queue, retry, degrade]
- Data flow: [what we send, what we receive]
```

### 6. Risk & Failure Modes

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [API provider downtime] | Medium | High — [feature] stops working | [Queue + retry with exponential backoff. Show "processing" state.] |
| [Database connection limit] | Low | High — app unresponsive | [Connection pooling. Monitor with alerts at 80%.] |
| [Auth token expiry mid-session] | High | Medium — user sees errors | [Silent refresh. On failure: redirect to login with return URL.] |
| [Large data volumes at scale] | Medium | Medium — slow queries | [Pagination. Index on [fields]. Monitor query time.] |

### 7. Definition of Done

Per feature/milestone, specific and verifiable:

```
FEATURE: [name]
- [ ] [Functional]: User can [specific action] and sees [specific result]
- [ ] [Quality]: Page loads in <[N]ms. No console errors. Responsive at all breakpoints.
- [ ] [Testing]: [What's tested] — unit tests for [logic], integration test for [flow]
- [ ] [Security]: Auth enforced on [routes]. Input validated on [endpoints]. No secrets in client code.
- [ ] [Accessibility]: Keyboard navigable. Screen reader labels on [elements]. Contrast ratios met.
```

### 8. Milestones & Gates

| Milestone | Deliverable | Definition of Done | Gate |
|-----------|-------------|-------------------|------|
| M1: [name] | [what ships] | [specific checks from §7] | [what must be true before M2 starts] |
| M2: [name] | [what ships] | [specific checks] | [gate] |
| M3: [name] | [what ships] | [specific checks] | [final acceptance] |

Each gate is a decision point. Do not proceed without verification.

### 9. Dev Environment & Setup

```
SETUP:
1. Clone repo
2. [Install dependencies command]
3. [Environment variables needed — list each with description]
4. [Database setup command]
5. [Run dev server command]
6. [Run tests command]

ENVIRONMENT VARIABLES:
- [VAR_NAME]: [what it is, where to get it]
- [VAR_NAME]: [what it is]
```

---

## Phase 5 — QUALITY GATE

Read it as the CTO.

**Architecture test:** Is this the simplest architecture that supports every screen from Stage 2? Or is there unnecessary complexity?

**Data model test:** Can every screen in Stage 2 be populated from this data model? Trace 3 screens back to tables — does the data exist?

**API test:** Does every user action from Stage 2's journeys have a corresponding API endpoint or server action? Are error responses defined?

**Risk test:** Are the 3 most likely failure modes identified with specific mitigations — not "we should handle errors" but what actually happens in the code?

**Completeness test:** Could a developer clone the repo, read Stage 1 + 2 + 3, and start building without asking questions? If not — fill the gap.

Fix what fails. Deliver.

**Ask:** "PRD is complete across all 3 stages. Run `/cto` to start building? Or `/plan` for a formal SOW with timeline?"

---

## Output location

Save to: `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/DRAFT-v0.1-YYYY-MM-DD-PRD-3-BUILD.html` (HTML canonical, decision-tagging scaffold per the mandate above). No `.md` companion (per `feedback_everything_to_github_html_canonical`).

---

## Links to other stages

- **Stage 1:** `/prd-discovery` — Problem, market, user
- **Stage 2:** `/prd-ux` — User journeys, screen states, interaction design

---

## Core Writing Standard

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md` (canonical rule source: `skills/copywriting/Proofread-Anti-AI-Standard.md`).

Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene. Three or more AI-tell patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Core Writing Standard for the cross-phase enforcement protocol.

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
