---
description: PRD Stage 2: User Journeys & UX Specification.
argument-hint: "[context or target]"
---
<!-- slash-commands/prd-ux.md is canonical; .claude/commands/prd-ux.md must match exactly | Workflow: prd-assembly.workflow.json | Phase: ux -->
# /prd-ux — PRD Stage 2: User Journeys & UX Specification

You are the Product Lead. This is Stage 2 of 3. Stage 1 (`/prd-discovery`) defined who, what, and why. This stage answers: **what does the user SEE, DO, and EXPERIENCE at every step?**

This is the stage that most PRDs skip. It's the reason developers have to guess what the UI looks like, what happens on error, what the empty state shows, and how navigation works. By the end of this stage, a developer should be able to build every screen without asking "what happens when...?"

Requires PRD-1-DISCOVERY.md from Stage 1 (loads it as input).

5 phases: context → task → skills → execute → quality gate.

---

## Rationalisations

<!-- Source: addyosmani/agent-skills · MIT
     skills/test-driven-development/SKILL.md @ f17c6e8 (vendored 2026-05-18)
     PLUS ragnar-pwninskjold/tech-snacks · MIT
     plugins/tech-snacks/skills/prd-to-ux/SKILL.md @ 977891d (vendored 2026-05-18)
     Pattern lifted: Rationalisations table + "skill never auto-selects" rule. -->

Common excuses for skipping Stage 2 rigour, with rebuttals. If you catch yourself thinking one of these — stop.

| Thought | Reality |
|---|---|
| "UX model is dashboard — obvious from Stage 1." | **Step 1.5 UX Philosophy gate (forthcoming).** Diverge 10 organising metaphors, filter, synthesise 3, user picks. Never auto-select. |
| "Empty state and error state can come later." | Every screen gets all 5 states (empty / loading / populated / error / edge). No screen ships with undefined states. |
| "Mobile is just stack the desktop." | Section 6 is a re-layout, not a checklist. What changes, what's hidden, what reflows — per screen. |
| "Accessibility is post-launch polish." | ARIA + keyboard nav are not afterthoughts. Section 7 is mandatory. |
| "Validation rules live in the code, the PRD doesn't need them." | Section 5 interaction patterns IS the contract. Validation timing, error display, save behaviour — all defined here. |
| "The dev will figure out the loading indicator." | Loading indicator placement, skeleton shape, button state — all defined per screen per state. No guesses. |
| "Skip the journey for the rare path." | First-time activation, core loop, return visit, error recovery, settings — five journeys mandatory. Document the rare one. |

## Red Flags

Stop signs. Do not produce PRD-2 with any of these true.

- UX model selected without divergent options + user choice (auto-selection = drift)
- Any screen without all 5 states (empty / loading / populated / error / edge)
- Vague journey descriptions ("user navigates to settings")
- Missing failure-flow journeys (error recovery is a journey, not a single screen)
- Component decisions without layout / primary content / navigation / actions / data-display columns
- Form validation rules without timing + error-display contract
- Responsive section listing breakpoints without specifying what reflows at each
- Accessibility section missing keyboard nav or ARIA labels for icon-only buttons

---

## Phase 1 — CONTEXT

### Step 1.1 — Load Stage 1 output

Read the PRD-1-DISCOVERY.md from the task folder. This is your foundation — the problem statement, switching dynamics, competitive frame, outcome, and scope boundary.

If it doesn't exist: **stop.** "Run `/prd-discovery` first — I need the problem and user definition before designing UX."

### Step 1.2 — Load technical context (if exists)

If there's a codebase: read the project structure, existing UI patterns, component library, design system.

If entity involved: load brand context for design tokens, visual identity.

### Step 1.3 — Context checkpoint

```
BUILDING: [product — from Stage 1]
THE USER: [from Stage 1 — emotional state, what they've tried]
OUTCOME: [from Stage 1 — what changes when this ships]
SCOPE: [from Stage 1 — what's in/out]
EXISTING UI: [what patterns exist — or "greenfield"]
```

**GATE — present for confirmation:**
> PRD UX: [product] | Stage 1 ref: [file path]. Correct?

Wait for response.

---

## Phase 2 — TASK

Ask (if not clear):
1. **What's the UX model?** (dashboard, wizard, single-page app, admin panel, mobile-first)
2. **What's the primary user flow?** (the one thing they do most — the core loop)
3. **Any design constraints?** (existing design system, brand guidelines, accessibility requirements, responsive targets)

Think through as the Product Lead:
- What's the user's first screen after signup/login? Not a dashboard — what do they NEED first?
- What's the core loop? The thing they'll do 80% of the time. Make that 2 clicks, not 7.
- What's the activation moment? When do they first feel the value? Make that happen faster than whatever they were doing before.
- What about the person who comes back tomorrow? What do they need to see immediately?
- What about the person who has 50 projects, not 3? Does the UI scale?

---

## Phase 3 — SKILLS

Propose skills from:
- `frontend/design-guardrails.md` — design system constraints
- `frontend/ui-design-system.md` — UI patterns, component architecture
- `frontend/senior-frontend.md` — React patterns, state management
- `frontend/frontend-design.md` — frontend design principles
- `product/product-manager-toolkit.md` — user story mapping
- `product/prd-builder.md` — acceptance criteria

**Ask:** "These are the skills I'd use for UX specification. Add, remove, or swap?"

---

## Phase 4 — EXECUTE

Write **PRD-2-UX.md** with these sections:

### 1. Screen Inventory

List every screen/page the user encounters. Name them clearly. Group by area.

```
ONBOARDING:
- Welcome / Sign-up
- Onboarding Wizard (Step 1: [what], Step 2: [what], Step 3: [what])

CORE:
- Dashboard (home after login)
- [Primary entity] List (all items, filterable)
- [Primary entity] Detail (single item view)
- [Core action] Interface (the main thing they DO)

SETTINGS:
- Profile
- Billing
- Team / Permissions

EDGE:
- 404 / Not Found
- Error boundary
- Maintenance page
```

### 2. User Journeys (click-by-click)

For each primary flow, document every click:

```
JOURNEY: [Name] — [one sentence: what the user accomplishes]

TRIGGER: [what causes them to start this flow]

1. User is on [Screen]. Sees [what's visible]. Clicks [element].
2. [What happens]: [modal opens / page navigates / inline form appears].
3. User fills [fields]. Validation: [when it fires, what it checks].
4. User clicks [action button].
   - LOADING: [button shows spinner / fields disabled / skeleton appears]
   - SUCCESS: [what they see — toast, redirect, inline confirmation]
   - ERROR: [what they see — field-level message, toast, retry option]
5. User lands on [resulting screen]. Sees [confirmation of what happened].
```

Write journeys for:
- **First-time activation** (signup → first value moment)
- **Core loop** (the thing they do 80% of the time)
- **Return visit** (what they see when they come back)
- **Error recovery** (what happens when things break)
- **Settings/account management** (profile, billing, team)

### 3. Screen States (for every screen)

| Screen | Empty | Loading | Populated | Error | Edge cases |
|--------|-------|---------|-----------|-------|------------|
| Dashboard | "No [items] yet" + CTA | Skeleton matching layout | Full data, sorted by [default] | "Something went wrong" + retry | 100+ items: pagination/virtualization |
| [Entity] List | "Create your first [entity]" | Skeleton cards/rows | Filtered, sorted, paginated | Retry button | Search with no results: "No matches" |
| [Entity] Detail | N/A (always has data) | Skeleton matching layout | Complete data | 404 if not found | Long content: scroll behavior |

### 4. Component Decisions

For each screen, specify the UI patterns:

```
[Screen Name]:
- Layout: [sidebar + main / full-width / split-panel / centered card]
- Primary content: [cards in grid / table rows / timeline / form]
- Navigation: [sidebar items / tabs / breadcrumbs]
- Actions: [button placement, primary/secondary/destructive styling]
- Data display: [how information is organised — cards, tables, lists, metrics]
```

### 5. Interaction Patterns (global)

Define once, apply everywhere:

```
FORMS:
- Validation: [on blur / on submit / real-time]. Error display: [below field in red].
- Required fields: [asterisk / inline "required" text / no indicator, all required by default].
- Save: [button shows spinner, fields disabled. Success: inline toast, 3s. Error: toast + fields re-enabled].

DESTRUCTIVE ACTIONS:
- Always: confirmation dialog. "[Action] [item name]? This cannot be undone." Red destructive button.
- Never: single click to delete without confirmation.

LOADING:
- Page load: skeleton placeholders matching the layout structure. Not spinners. Not blank pages.
- Action loading: button spinner. Disable form inputs during save.
- Long operations (>3s): progress indicator or status message.

NAVIGATION:
- Page transitions: [instant / fade / none]. Sidebar highlight updates immediately.
- Back button: respects browser history. Modal close returns to previous page state.
- Breadcrumbs: [where they appear, depth limit].

NOTIFICATIONS:
- Success: toast, bottom-right, 3s auto-dismiss, dismiss on click.
- Error: toast, persists until dismissed, includes action (retry/dismiss).
- System: banner at top of page, persistent until resolved.
```

### 6. Responsive Behaviour

```
DESKTOP (>1024px): [sidebar visible, multi-column, full data density]
TABLET (768-1024px): [sidebar collapsible, 2-column, same data density]
MOBILE (<768px): [bottom nav / hamburger, single column, simplified cards]
```

For each screen: what changes, what's hidden, what reflows.

### 7. Accessibility Notes

- Keyboard navigation: [tab order, focus management for modals/dialogs]
- Screen reader: [ARIA labels on icon-only buttons, live regions for toasts]
- Colour: [contrast ratios met, not colour-only indicators]

---

## Phase 5 — QUALITY GATE

Read it as the Product Lead. Then as a developer who has to build this.

**The developer test:** Pick any screen. Can you build it from this document without asking:
- "What does the empty state look like?"
- "What happens when the API fails?"
- "Where does the loading indicator go?"
- "What's the mobile layout?"
- "How does the form validate?"

If ANY screen has undefined states, fill them in.

**The user test:** Walk through the first-time activation journey. Is it faster than their current workflow? Is every step earning its existence, or is there a setup wall before value?

**The scale test:** Imagine 50 items, not 3. Does the UI still work? Is there pagination, search, filtering? Or does it break at scale?

Fix what fails. Deliver.

**Ask:** "Ready for Stage 3? Run `/prd-build` to define architecture, data model, and milestones."

---

## Canonical output scaffold (MANDATED)

PRD-2 is decision-bearing — every screen, every state, every interaction pattern becomes a row Andrew has to stamp LOCK / REVISE / DROP / DEFER. **Always start the HTML output from `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`** (modules + Decision Register + Archive section + tagging UI). Never hand-write the brand CSS or invent a layout.

ID convention: `S` screens · `J` journeys · `I` interaction patterns · `D` design decisions · `Q` open questions.

If the canonical is missing, STOP and ask.

---

## Output location

Save to: `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/DRAFT-v0.1-YYYY-MM-DD-PRD-2-UX.html` (HTML canonical, decision-tagging scaffold). No `.md` companion (per `feedback_everything_to_github_html_canonical`).

---

## Links to other stages

- **Stage 1:** `/prd-discovery` — Problem, market, user (input to this stage)
- **Stage 3:** `/prd-build` — Architecture, data model, milestones, definition of done
---

## Core Writing Standard

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md` (canonical rule source: `skills/copywriting/Proofread-Anti-AI-Standard.md`).

Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene. Three or more AI-tell patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Core Writing Standard for the cross-phase enforcement protocol.

---

## VERIFICATION — writing journeys that can actually be walked

Canonical text: `command-includes/_VERIFICATION-STANDARD.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

This command does not verify anything — it **produces** the journeys and states that
`/goal-build` and `/review` will later verify against. So the standard applies here as
a writing constraint: a journey written loosely cannot be walked, and an unwalkable
journey is checked off by whoever is tired rather than by whoever is right.

**Every journey must name its walker.** Which user, holding which permissions. A
journey written for "the user" gets walked as an admin, and the member-facing hole is
found in week three. Section 2 already documents click-by-click; add the role.

**Every journey must end in an observable final state.** Not "user lands on the
resulting screen" but what is visibly true when they arrive — the record that now
exists, the confirmation shown, the email that arrives. A journey with no observable
end cannot pass or fail, so it will pass.

**Name the defining gesture.** Every product has one action that *is* the product:
building a form and receiving a response, a stranger booking a slot, joining two nodes.
Name it in Section 2 and put it first. It becomes the first acceptance check and the
first journey walked, and it is verified before anything is stacked on top of it. If it
cannot be performed by hand, the product does not work, whatever else is green.

**Section 3 is the verification surface, not a table to fill in.** Empty, loading,
populated, error, and the ones nobody remembers — exactly one item, a very long value,
a failed request, a slow response. Every cell left generic becomes a defect found in a
browser later, at far greater cost than defining it here.

**Section 6 viewports are the capture list.** State them as numbers, because a defect
at 1280 is not a defect at 1440, and every later capture is named to the viewport it
was taken in.

Phase 5's user test asks you to walk the activation journey. Walking it on paper is a
legibility check, not verification. Say so in the output rather than letting a paper
walkthrough be read later as evidence the flow works.

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
