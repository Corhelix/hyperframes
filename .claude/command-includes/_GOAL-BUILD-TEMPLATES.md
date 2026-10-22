# _GOAL-BUILD-TEMPLATES — state schemas and spawn prompts for /goal-build

<!-- Include, not a command. Lives beside the commands, like _GATE-MECHANICS.md. v0.2 2026-08-21 -->
<!-- v0.5 2026-10-21: goal-build v1.2 (Map-Builder Run A). BUILD-BRIEF carries `command: goal-build v1.2`; REQUIREMENTS-TRACE gains Binding rule and
     Observed conflict rows and the Base app lines; new schemas for READ-PLAN/READ-LOG, EXISTING-SCREENS, NAVIGATION-MAP and the DECISIONS lines the gate reads;
     spawn prompt 7 (UX lock critic) now walks the real app and answers nine questions; spawn prompt 8 (fidelity verifier) re-reads the approved specification
     files itself and checks navigation reach; "side nav" is now "the app's real navigation". -->
<!-- v0.4 2026-10-12: BUILD-BRIEF follows the v1.0 four-state slots (answered, derived, assumed, unknown) and
     carries `command: goal-build v1.1`; adds REQUIREMENTS-TRACE.md and SCOPE.txt; the UX lock critic reads
     the trace and answers five questions; adds spawn prompt 8, the requirements fidelity verifier. -->
<!-- v0.3 adds the Owner column, STATUS.md, and the `Staffed by` slot on every spawn prompt:
     a worker is staffed by a C-level identity resolved at runtime, and skills resolve from the
     skills tree. No template names a skill or a worker.
     v0.2 added JOURNEYS.md, the evidence naming law, the paired visual audit artefact, and the
     visual-auditor and journey-walker spawn prompts. -->

Why this file exists: a matrix whose shape is reinvented every run can be quietly weakened, and a verifier whose prompt is improvised by the builder inherits the builder's framing. These shapes are fixed so neither happens. Fill the slots in brackets; keep the frames.

---

## State file schemas

### BUILD-BRIEF.md

```
# BUILD-BRIEF — [project name]
Locked: [date] · mode: [fresh|resume] · scale: [mvp|full]
command: goal-build v1.2

## Mission
[outcome, reference products, better means, out of scope — from the brief]

## Specifics
[stack locks, brand, data/auth/hosting, repo, credentials on hand]

## Quality bar
[non-negotiables, evidence required at done]

## Sanity
[the one command that proves the app still boots — every resume runs it first]

## Assumptions
| Slot | State | Value chosen | Source |
|---|---|---|---|
| [slot] | answered / derived / assumed / unknown | [value] | [for answered: where the operator said it; for derived: the evidence; for assumed: what reversing it costs; for unknown: the question] |
```

Rules: the deliverable, the surface of record, the platform and the audience are never `derived`, and an `unknown` blocks the run from starting. The brief is a summary: the operator's own words live in `REQUIREMENTS-TRACE.md`.

### OPERATOR-WORDS.md

The operator's own words, copied verbatim, nothing else. It is the only file a quote in the trace may cite. The stop gate checks that every `answered` quote appears in it, so it is as good as the copy: take the words from the conversation you were invoked in and the thread the operator names, never from the brief.

```
# OPERATOR-WORDS: [project name]
Thread: [thread or session id] · Copied by: [who] · Copied: [date]

## [timestamp]
[the operator's message, verbatim, complete]

## [timestamp]
[the next message, verbatim]
```

### REQUIREMENTS-TRACE.md

Written in Phase 0, before any phase. It holds what the operator actually asked for, and every row is checked against `OPERATOR-WORDS.md`. The stop gate reads it (`goal-build-stop-gate.py --check-trace`), and the original source for every verification is this file and the words it cites.

```
# REQUIREMENTS-TRACE: [project name]
Opened: [date] · Operator: [name]

| ID | Requirement | Operator's words (verbatim) | Source | State |
|---|---|---|---|---|
| T1 | Deliverable: [what is to exist when this is done] | "[quoted]" | file:OPERATOR-WORDS.md#[timestamp] | answered |
| T2 | Surface of record: [where the operator reads or uses it, and which surface is primary] | "[quoted]" | file:OPERATOR-WORDS.md#[timestamp] | answered |
| T3 | Platform: [where it runs] | "[quoted]" | file:OPERATOR-WORDS.md#[timestamp] | answered |
| T4 | Audience: [who it is for] | "[quoted]" | file:OPERATOR-WORDS.md#[timestamp] | answered |
| T5 | Parent decision: [one binding decision of the found plan] | "[quoted from the plan]" | file:[the plan's path] | answered |
| T6 | Binding rule: [what the repo's own file says the product must do, must not do, or is for] | "[quoted from the file]" | file:[repo path]:[line] | open |
| T7 | Observed conflict: [a control or page in the app that contradicts a rule or a journey] | "[quoted from the code or the page]" | file:[repo path]:[line] | open |

Parent plan search: found: [path, path] | none found; searched: [place one; place two; ...]
Not parent: [full path] because [reason of at least three words]
Search limited: [reason of at least four words]   (only if fewer than two places could be searched)
Reconciliation: [at least eight words: where the brief and the plan differed, and how the operator settled it]
Parent plan reconciled: yes
Base app: none | [folder of the app already in the repo]
Adopt existing CSS and navigation: yes | no   (only with a base app)
Operator's words (base app): "[quote]"   (only with a base app; the quote must be in OPERATOR-WORDS.md)
Ingestion plan: BASE-APP.md   (only when adopting)
Primary surface delivered: [a URL, or a path that exists]   (written at close)
```

Rules:
- One row at least for each of Deliverable, Surface of record, Platform and Audience. State is `answered` (a quote of at least a clause, cited as `file:<path>` to a file that is not a document the run wrote, and the quote must appear in it), `assumed` (the Source column states what reversing it costs), or `unknown` (a question for the operator; blocks the run). `derived` is not allowed on these four.
- `PARENT-PLAN-SEARCH.json` is written by `goal-build-find-parent-plan.py --out`. Every hit in it (local or GitHub) appears either in the `found:` line or in a `Not parent: <path> because <reason of at least three words>` line; a GOAL, PLAN or SCOPE file that names the subject cannot be waved away that way. A `found:` path must be one the search found. 'none found' is refused while the file lists a hit, and names at least two different places searched. The file's subjects must appear in the brief, and the places it lists must exist.
- If a parent plan is found, add at least one row per found plan whose Requirement starts `Parent decision:`, quoting a binding decision from that plan and citing it as `file:<the plan's path>` (the gate checks the quote against the plan). Write `Parent plan reconciled: yes` only after every disagreement with the brief has been settled with the operator. The Surface of record cannot be `assumed` when a plan was found.
- At close, `Primary surface delivered:` names, as a URL or a path that exists, where the operator can open the surface the trace calls primary. If it was not delivered: `Primary surface not delivered: <reason>; accepted by operator in DECISIONS D#`, with D# logged as a decision about the surface that records the operator's acceptance.
- Do not cite the brief, the strategy or any derived document as a source. A `|` inside a quote breaks the table: replace it.
- The gate cannot tell a faithful excerpt from an invented one. That is what the operator reading the trace, and spawn prompt 8, are for.
- v1.2: a `Binding rule:` or `Observed conflict:` row quotes the file at the line it cites, and the gate checks the quote is there. State is `open` (allowed until the UX lock), `carried:J2,S4,A7` (each ID must exist in JOURNEYS.md, SCREENS.md, ACCEPTANCE.md or FEATURE-MATRIX.md), `conflict:D12` or `declined:D12` (D12 is a DECISIONS.md line that records the operator's words and cites `file:OPERATOR-WORDS.md#<timestamp>`). Every rule in READ-LOG.json must have a row.
- v1.2: with a base app, what happens to its CSS and navigation is the operator's choice in their own words. `Base app: none` on a repo that already runs an app is refused.

### SCOPE.txt

One glob per line, `#` for comments. It lists every path the run may write outside its own build folder, derived from the trace. Each glob starts with a literal path at least three segments deep (`fnmatch` lets `*` cross `/`, so `/Users/**` or `~/**` is a catch-all and is refused). `goal-build-scope-gate.py` denies a write that matches none of them, and is inert when the file is absent or empty, which is why a v1.1 run may not close without it.

```
# [project] - see REQUIREMENTS-TRACE.md
[absolute path or glob the run may write]
```

### READ-PLAN.json, READ-PLAN.html and READ-LOG.json (v1.2)

Written by `goal-build-read-check.py`, not by hand. `enumerate` builds the plan from the repo: a row per specification file with `path`, `lines`, `sha256`, `heading`, `headings`, `why`, `status` (`to-read` or `not-planned`) and `reason`. `approve` adds the operator's approval with a hash of the list. `log` adds a row per file read: `path`, `lines`, `sha256` and `rules` (`[{"quote": "...", "line": 5}]`), and sets the file-level `conflicts` (`"none"` or `[{"summary": "...", "decision": "D12"}]`). `check` proves the log against the files and the session transcript. `READ-PLAN.html` is the page the operator reviews, rendered from the plan on the CLARITY report template: one row per file (path, lines, headings, why, status), the not-planned rows with their reasons, the skipped files, and the total lines to be read.

Rules: the plan lists every file the tool found; a row is never removed, only marked not-planned with a reason of at least three words and approved again; a rule is anything the file says the product must do, must not do, or is for.

### EXISTING-SCREENS.md and NAVIGATION-MAP.md (v1.2, base app only)

`EXISTING-SCREENS.md` is seeded by `goal-build-screens-check.py seed`; the routes are scanned from the code:

```
| Route | File | Decision | Journey steps |
|---|---|---|---|
| /walkthroughs/[projectId] | src/app/walkthroughs/[projectId]/page.tsx | change | J1.2 |

## Controls

| Route | Control | Decision | Why |
|---|---|---|---|
| /walkthroughs/[projectId] | Upload walkthrough button | change | becomes the upload code |
```

`NAVIGATION-MAP.md` places every journey step on the app's own navigation:

```
| Journey step | Screen route | Reached via | New menu |
|---|---|---|---|
| J1.2 | /walkthroughs/[projectId] | Header > Sites > Example Site > Walkthroughs tab | no |
| J1.1 | new:/sites/[id]/overview - the site home the IA defines | Header > Sites > Example Site | no |
```

Rules: every real route has a row and a decision (keep, change, remove); a change lists its controls; a screen a journey uses is not marked remove; a new route is written `new:/route - reason`, is not a shell, mock or stub route, and does not share its destination with a real one (`distinct:D#`, with the operator's logged decision, is the only exception); `Reached via` is a path through the app's navigation written A > B > C; a new menu item is `+Name` in the path and the `New menu` cell is `proposed:D#`.

### Lines the gate reads in DECISIONS.md (v1.2)

```
YYYY-MM-DD - D# - UX-CRITIC round N: pass | fail - [the verdict, copied from the critic]
YYYY-MM-DD - D# - UX-LOCK: locked (date) url: https://[deployed or preview address] operator words: "[their reply]" critic rounds: N; passed: M; last: pass
YYYY-MM-DD - D# - [DEFECT-ID] accepted as risk, deferred to [run]; operator [words], file:OPERATOR-WORDS.md#[timestamp]
```

The lock line must agree with the critic lines (rounds, passes and the last result), and the quote must be in OPERATOR-WORDS.md. Deferred defects sit under a `## Deferred` heading in DEFECTS.md, one row each, and STATUS.md says `Deferred: N`.

### FEATURE-MATRIX.md

```
| ID | Feature | Acceptance | Status | Owner | Docs | Commit |
|---|---|---|---|---|---|---|
| F1 | [feature] | A1 | failing | [C-level identity] | — | — |
```

**Owner sits to the right of Status on purpose.** The stop gate reads Status as the fourth cell of a matrix row; a column inserted to its left breaks the gate. Owner names the C-level identity accountable for the row, so its verifier is chosen rather than generic and a parked row has someone it is parked on.

Rules: rows are appended or their Status flipped; a locked row is never deleted or reworded without a `DECISIONS.md` entry naming it. Status values are `failing`, `green` and `parked`, nothing else. A row turns green only when its acceptance check passed, an independent verifier (spawn prompt 3) returned pass, and its docs are updated. A row turns parked only alongside a `BLOCKED:` entry in `DECISIONS.md` naming it; the stop gate checks that pairing.

### ARCHITECTURE.md

```
# ARCHITECTURE — [project name]
[stack and locks; data model pointer; integration boundaries]

## Module ownership
| Module | Owner (one writer at a time) | Contract files |
|---|---|---|
| [module] | [agent or main loop] | [schema/type/API files] |
```

Rules: contracts are committed before any parallel build starts; a module's owner is the only writer while it is owned. Ownership changes are a `DECISIONS.md` entry.

### ACCEPTANCE.md

```
| ID | Check (exact command or walkthrough steps) | Expected evidence | Status | Evidence |
|---|---|---|---|---|
| A1 | [runnable command or numbered browser steps] | [what passing looks like] | failing | — |
```

Rules: Status and Evidence change freely, with evidence. The Check text itself changes only through a `DECISIONS.md` entry. A check nobody can run is a defect in the check, not a reason to eyeball it.

### DECISIONS.md

One line per entry:

```
YYYY-MM-DD — D1 — [decision], because [reason]; affects [F#/A#]
YYYY-MM-DD — D2 — BLOCKED: [trigger one/two/three: detail] on F#; parked, continuing with F#
```

### DEFECTS.md

```
Phase 3 sweep: not-run

| ID | Lens | Severity | Repro | Status | Evidence | Re-run |
|---|---|---|---|---|---|---|
| X1 | code/visual/journey/[dimension] | [low/med/high/critical] | [exact steps] | open | evidence/X1-*.png | — |
```

**Keep the column order anyway.** Since gate v4 the Status column is located by name from the header row, so inserting a column no longer makes a run un-endable — the trap caught two real runs before it was closed. Position (fifth cell of a defect row, fourth of a matrix row) is now only the fallback for a table with no header. Keep the canonical order regardless: every reader, script and reviewer downstream still expects it.

Status path: `open` to `fixed` to `retested`. A defect closes only at `retested`, with the affected acceptance checks re-run, any journey the fix touches re-walked, and the Re-run column naming them. Every row carries an evidence path — a defect nobody photographed is a rumour. Material means it fails an acceptance check, breaks a journey, or violates a non-negotiable; anything else may close as accepted risk through a `DECISIONS.md` entry. The header line flips to `Phase 3 sweep: complete (YYYY-MM-DD)` only after every dimension tester has run; the stop gate reads it.

### STRATEGY.md

Written in Phase 1a. One page. If it runs to two, the product is two products.

```
# STRATEGY — [project name]

For:            [who, and what they are doing instead today]
The job:        [the one thing they hire this to do]
Defining gesture: [the action that IS this product]
Beats [reference] on: [the named weakness, and how]
Will not do:    [the deliberate omissions]
Success, observable: [what a person can be watched doing when this is right]
```

### SCREENS.md

Written in Phase 1b, before `JOURNEYS.md`. Sections in this order, under these names, because they are `/prd-ux`'s names and the two commands stay one vocabulary:

1. Screen Inventory — every screen, grouped, each with an S-id
2. Screen States — a row per screen: empty, loading, populated, error, edge
3. Component Decisions — per screen: layout, primary content, navigation, actions, data display
4. Interaction Patterns — global: form validation timing, destructive actions, loading, navigation, notifications
5. Responsive Behaviour — per screen, what changes at each stated viewport
6. Accessibility Notes — keyboard order, focus management, ARIA on icon-only controls, contrast

```
| ID | Screen | Reached by | Empty | Loading | Populated | Error | Edge |
|---|---|---|---|---|---|---|---|
| S1 | [name] | [J1 step 1] | [what shows] | [what shows] | [what shows] | [what shows] | [the awkward one] |
```

Rule: `Reached by` names a journey and a step. A screen with an empty `Reached by` is either an orphan or a missing journey, and both are found here rather than at Phase 3.

### JOURNEYS.md

Authored in Phase 1b, before any code. Two levels: the index says which journeys exist, and a detail block per journey is what actually gets walked.

The index, unchanged:

```
| ID | Journey | As whom | Owner | Gestures (numbered, in order) | Final state observed | Status | Evidence |
|---|---|---|---|---|---|---|---|
| J1 | [what the person is trying to achieve] | [role/permissions] | [C-level identity] | 1. [gesture] 2. [gesture] … | [what proves it worked] | not-walked | — |
```

Then one detail block per journey, below the index:

```
### J1 — [what the person is trying to achieve]
As: [role/permissions] · Owner: [C-level identity] · Screens: S1 → S2 → S3

| # | Gesture (what the person does) | What happens on screen | Success criterion (observable) | Passes forward |
|---|---|---|---|---|
| 1 | clicks Import in the app's navigation | a selector panel opens over the list | the panel is visible and its Choose file control is operable | nothing |
| 2 | chooses a file | the filename appears beside Continue, Continue enables | the chosen filename is shown verbatim | the file, to S2 |
| 3 | clicks Continue | the mapping screen loads | the mapping screen header shows that same filename | the file and its column list, to S3 |

Final state observed: [what proves the whole journey worked]
```

Rules: a journey is a composite, and its status is independent of the features inside it — never mark it walked because its parts passed. Status values are `not-walked`, `walked`, `broken`. It becomes `walked` only when someone performed every gesture in one continuous sitting in a real browser and observed the final state, with a capture to show it. J0 is always the defining gesture.

Every gesture row carries a success criterion someone could watch being true or false, never "works" and never "is correct", because a gesture with no observable criterion cannot be walked and gets ticked instead. `Passes forward` names the thing itself rather than its category: the filename, the record id, the row count. It is the column the Phase 1d data model is derived from. `nothing` is a valid value and is written, never left blank.

### SHELL-WALK.md

Written in Phase 1c, after the shells have been driven in a browser.

```
| ID | Journey | Shell path | Walked in browser | Broke at step | Evidence |
|---|---|---|---|---|---|
| J1 | [name] | shells/j1-*.html | yes/no | — or step n | evidence/shell-J1-*.png |
```

Rule: `yes` means someone drove it in a real browser and captured every step. Reading the shell source is not walking it.

### STATUS.md

Rewritten in full at every phase boundary, every park and every escalation. It is a snapshot, never a log, and it fits on one screen.

```
# STATUS — [project] · [ISO timestamp]
Task (verbatim): "[the operator's request, copied word for word from OPERATOR-WORDS.md; at least 5 words]"

Phase:      [0, 1a, 1b, 1c, 1d, 2, 3 or 4, and what is happening right now]
Matrix:     [n] green · [n] parked · [n] failing   (of [total])
Journeys:   [n] walked · [n] broken · [n] not-walked
UX lock:    [not-proposed | proposed (date) | locked (date) | revised (date)]   Shells: [n] walked · [n] broken
Defects:    [n] open · [n] fixed · [n] retested    Phase 3 sweep: [not-run|complete]
Trace:      [ok (date) | missing]   Bind: [MATCH sha8 | DIFFER | BIND-UNVERIFIED]
Reads:      [n of N files read and logged | not started]   Deferred: [n]   /goal line for the operator: [the line]

In flight:  [the row or journey being worked, and its owner]
Blocked:    [F# — trigger, one line each; or "none"]
Last evidence: [most recent path written]
Next:       [the single next action]
```

Rule: an operator reading only this file knows where the run is. If that is not true, the file is wrong.

*(v1.3)* The first line after the title is the task anchor. `goal-build-content-check.py anchor <build folder>` refuses a line that is not a quotation from `OPERATOR-WORDS.md`, so the task cannot be restated from memory after a compaction.

### QUALITY.json, figures.json, and the review lines (v1.3, document or surface builds)

`QUALITY.json` in the build folder. Every key is optional; an absent key takes the strict default in `goal-build-content-check.py`. The brief sets the values and `Lens 2b` applies them.

```
{
  "max_figure_share_of_steps": 0.35,
  "max_talking_head_share": 0.05,
  "max_repeat_share": 0.05,
  "max_nothing_shown": 0,
  "long_step_words": 40,
  "max_long_step_share": 0.10,
  "max_step_words": 60,
  "max_filler_pages": 0,
  "near_dup_bits": 5
}
```

`figures.json`: `{"<image file name>": "<kind>"}`, where kind is `talking-head`, `slide`, `screen` or another label the shot classifier uses. It is written by the classifier, not by the builder. Without it the talking-head share is inferred from caption wording, which a caption that never mentions the camera defeats.

Lines `goal-build-content-check.py` reads in `DECISIONS.md`:

```
YYYY-MM-DD - D# - SHELL-REVIEW: pass (YYYY-MM-DD) reviewers: N coverage: A of B
YYYY-MM-DD - D# - UX-LOCK: locked (YYYY-MM-DD) panel: N reviewers: <id>, <id> coverage: M of M critic rounds: R; passed: P; last: pass
```

`SHELL-REVIEW` needs `N` of at least 2 and `A` equal to `B`. Matrix rows with IDs starting `SH` are the shell, cover and sample pages and are exempt from the ordering check; every other row must go green on a commit dated on or after the review.

### evidence/ — the naming law

```
evidence/A{n}-{surface-or-state}-{viewport}.png     acceptance check capture
evidence/J{n}-{step}-{what}.png                     journey step capture
evidence/shell-J{n}-{step}-{what}.png               Phase 1c shell walk capture
evidence/X{n}-{symptom}.png                         defect capture
evidence/gap{n}-actual-{what}.png                   paired-audit "what it does now"
```

Rules: never overwrite — a second capture of the same thing gets `-v2`, so the before and after both survive. Every filename says what it shows, so the ledger reads without opening the images. Captures record the viewport they were taken at, because a defect at 1280 is not a defect at 1440. Alt text and captions state what is visibly in the frame and nothing else; a caption that interprets or excuses is a caption that hides.

---

## The paired audit — the Phase 4 close artefact

Built from `CLARITY-OS-TEMPLATE.html`. For a product with no screen the left pane carries the emitted artefact instead of a screenshot — the response body, the file, the row, the terminal output — in a `<pre class="code">` block, captured verbatim and never paraphrased. Everything else about the block is unchanged, including the requirement to say what a person does and what happens when they are refused. One block per gap or notable surface. Left is the running app, right is what should be there, underneath is what a person does. Where the thing does not exist yet there is nothing to photograph, so the right pane carries an inline SVG wireframe instead — that absence is itself the finding.

```html
<div class="gap">
  <div class="gap-head">
    <span class="n">Gap {n} &middot; {category}</span>
    <h3>{the defect stated plainly, as a sentence}</h3>
    <p>{what is missing or wrong, in one short paragraph, no hedging}</p>
  </div>
  <div class="pair">
    <div class="pane now">
      <h4>What it does now</h4>
      <img class="shot" src="evidence/gap{n}-actual-{what}.png" alt="{what is visibly in the frame}">
      <p class="cap">{captured at {viewport}. What the image shows, as fact.}</p>
    </div>
    <div class="pane should">
      <h4>What it should do</h4>
      <!-- a corrected capture, or an inline SVG wireframe when nothing exists to photograph -->
      <svg class="wire" viewBox="0 0 520 300" role="img" aria-label="{describe the wireframe}">…</svg>
      <p class="legend">{the one behaviour the wireframe is asserting}</p>
    </div>
  </div>
  <div class="ux">
    <h5>What a person does</h5>
    <p>{gesture by gesture, in plain words, present tense}</p>
    <p><strong>Second route:</strong> {the other way a person would try it}</p>
    <p><strong>Refusals are shown, never silent:</strong> {what the product does when the gesture is not allowed, and how the person learns why}</p>
  </div>
</div>
```

The supporting CSS (`.gap`, `.pair`, `.pane`, `.shot`, `.cap`, `.ux`, `svg.wire`, `.legend`) is carried in the template's own extension block; lift it from the template, do not reinvent it.

---

## Spawn prompts

**Coverage clause (v1.3). Append to prompts 3, 5, 6, 7 and 8.**

```
Coverage: your return states, as its own sentence, "reviewed N of M images" (or pages, or gestures),
where M is the number you were given and N is the number you actually opened and looked at. Anything
you did not open is listed by name. If N is less than M for images, your verdict is FAIL and says so;
you do not pass a build you only partly saw.
```

### 1. Research dimension agent (Phase 1)

```
Staffed by: [C-level identity accountable for this dimension]. Work through that lens.
Intent: we are building [outcome] to beat [reference] on [better means]. Your slice is [dimension].
Objective: enumerate everything [reference] does inside [dimension]: behaviours, limits, defaults,
praised strengths, documented complaints, edge cases. Sources: [docs, product, reviews, tools].
Boundaries: research only; write no files. Do not study other dimensions; other agents own those.
Return: one line per finding — what it is, how it behaves, evidence (URL or quote). End with the
three weakest points you found in [dimension].
```

### 2. Consolidation critic (Phase 1 gate)

```
Staffed by: [the C-level identity that owns this stage]. Judge as that role judges.
You have fresh eyes and no stake in this build. Read only these files: [paths to BUILD-BRIEF.md,
FEATURE-MATRIX.md, ARCHITECTURE.md, ACCEPTANCE.md].
Objective: find material gaps — a brief requirement no matrix row covers, a matrix row no
acceptance check judges, an acceptance check too weak to prove its feature (a render check
greening a logic feature), an architecture choice that cannot deliver a matrix row.
Flag only gaps that affect correctness or acceptance. Do not comment on style, naming or
thoroughness, and do not manufacture findings to seem useful. "No material gaps" is a valid and
welcome answer.
Return: numbered gaps, each naming the file and row it concerns, or the single line: no material gaps.
```

### 3. Feature verifier (turning a row green, and Phase 3 re-checks)

```
Staffed by: [the owner named on the matrix row]. Its lens decides what matters here.
You are verifying one feature with fresh eyes. You get the diff and the criteria, nothing else,
deliberately: do not ask for the reasoning behind the work.
Feature: [F# name]. Acceptance check: [A# check text and expected evidence]. Diff: [commit range or files].
Objective: try to refute the claim that this feature passes. Run the check yourself. If this feature
has any user-facing surface, drive it in a real browser at [viewports] and capture what you see —
reading the markup is not verifying. Inspect the diff for the failure the check would miss: a
hardcoded happy path, a weakened check, a placeholder behind the control, a control that renders but
cannot be operated.
Flag only findings that affect correctness or acceptance.
Return: VERDICT: pass or fail, then the evidence you personally generated (command output, what you
watched happen). A verdict without evidence is a fail.
```

### 4. Dimension tester (Phase 3)

```
Staffed by: [C-level identity for this dimension — the system owner for security and isolation,
the product owner for accessibility and visual].
The application is running at [url or start command]. Test users: [credentials]. Your dimension:
[data isolation / authorisation / security / input abuse and failure conditions / accessibility /
visual and device coverage / researched edge cases].
Objective: break it inside your dimension. Work as a hostile or unlucky user would, in the real UI
and API, not by reading code.
Boundaries: fix nothing; test no other dimension.
Return: one DEFECTS.md row per finding (ID left blank): dimension, severity, exact repro steps,
what happened versus what should have. If nothing broke, list what you attempted so the coverage
is auditable.
```

### 5. Visual auditor (Phase 3, lens 2)

```
Staffed by: [the identity accountable for the product surface]. Read the screen as that role reads it.
The application is running at [url]. Viewports: [1280, 1440, 390]. If this product has no screen,
your subject is the artefact it emits — response bodies, written files, landed rows, terminal output —
captured verbatim; everything below applies to that artefact instead of a rendering. Credentials: [creds].
Your surfaces: [named routes/screens]. Reference intent: [brief lines and reference-product notes
that say what these surfaces are meant to be].
Objective: look at what is actually on screen and report where it departs from the intent. Reach
every state a user can reach on your surfaces — empty, loading, populated, error, and the awkward
ones: exactly one item, a very long value, a failed request, a slow response. Capture each into
evidence/ using the naming law, at each viewport.
Judge the rendered result, not the markup: overlap, clipping, truncation, contrast, misalignment,
a control that draws but cannot be reached or operated, text that collides at a narrower width,
a state that looks identical to a different state.
Boundaries: fix nothing; touch no state file; stay on your surfaces.
Return: one DEFECTS row per finding (ID blank) with its evidence path, plus for each surface one
line saying what you reached and what you could not reach. "This surface matches intent" is a
valid finding and is worth saying.
```

### 6. Journey walker (Phase 3, lens 3)

```
Staffed by: [the identity that owns this journey].
The application is running at [url]. You are [role], credentials [creds].
Your journey: [J# name]. Gestures, in order: [numbered list from JOURNEYS.md].
Final state that proves it worked: [observable].
Objective: perform the journey by hand, in the browser, in one continuous sitting. Click what a
person would click. Do not shortcut by URL, do not seed state through the API, and do not skip a
gesture because it is "covered elsewhere" — the point of this walk is the composite.
At the first gesture you cannot complete, stop and report from there: where you got to, what you
tried, what the screen did instead. A journey that breaks at step 3 of 9 is a more useful finding
than nine features reported green.
Capture each step into evidence/ as J{n}-{step}-{what}.png, and capture the final state.
Boundaries: fix nothing; touch no state file.
Return: VERDICT walked or broken; the step it broke at if broken; the evidence paths in order; and
one plain-words paragraph describing what the experience was actually like to perform.
```

Reused unchanged at Phase 1c against the shells: point [url] at the shell server and capture to `evidence/shell-J{n}-{step}-{what}.png`.

### 7. UX lock critic (Phase 1d gate)

```
Staffed by: [the identity accountable for the product surface]. Judge as that role judges.
You have fresh eyes and no stake in this build. Read only: [BUILD-BRIEF.md, STRATEGY.md, SCREENS.md,
JOURNEYS.md, REQUIREMENTS-TRACE.md, and for a base app EXISTING-SCREENS.md and NAVIGATION-MAP.md].
You are also given READ-PLAN.json, the list of the repo's specification files the operator approved. Open the ones
you need and read them yourself. Do not rely on any summary of them, including the rules the trace quotes.
Then walk the real thing yourself in a real browser at [viewports]. For a base app that is the deployed real app at
[the address the operator will be asked to open], starting from its front door; for a greenfield build it is the
shells at [shell path]. Click; do not read source. If a person would have to use the navigation to reach a page, do
the same: do not type its address.
Objective: answer nine questions and nothing else.
1. Does every outcome the brief names have a journey that reaches it?
2. Does every gesture carry a success criterion someone could watch being true or false?
3. Does everything a gesture passes forward actually appear on the receiving screen?
4. Does every screen sit inside the product's real navigation (header, context bar, tabs or side menu: whatever the
   app has), with the current item marked, rather than floating as an isolated screen?
5. Does every deliverable, surface and platform the brief states match a quoted operator row in
   REQUIREMENTS-TRACE.md, and does the brief omit nothing the trace or a found parent plan makes binding?
6. Is every Binding rule and Observed conflict row in the trace carried by a journey, screen or check that exists,
   and does the real app, as you walk it, obey each rule? Name any rule you find in the specification files that
   the trace does not list.
7. For every existing page a journey touches, does every control on that page agree with the journeys and with the
   binding rules? A control that does the opposite of a rule (a link that opens a view where the spec says the
   code only uploads) is a failure.
8. Is every journey screen reached through the app's own navigation, with no second header, second menu or parallel
   set of pages, and no new menu item the operator has not approved?
9. Does the first slice of the build plan deliver the entry point of the defining gesture, real, in the app?
Boundaries: fix nothing; write no files; do not comment on visual design, wording, spacing or colour (a base app keeps
its own).
Return: VERDICT pass or fail. On fail, the numbered failures, each naming the journey or screen and which of the nine
questions it fails. "Pass" is a valid and welcome answer.
```

### 8. Requirements fidelity verifier (Phase 3, source fidelity)

```
Staffed by: [the identity accountable for the product surface]. You have no stake in this build.
You receive exactly four things: (1) the operator's own words (OPERATOR-WORDS.md and the thread it was copied from,
which you re-read yourself) and the parent plan if one was found; (2) READ-PLAN.json, the approved list of the repo's
specification files, which you open and read yourself; (3) the built artefact, running or published at [address];
(4) nothing else. You are NOT given BUILD-BRIEF.md, STRATEGY.md, SCREENS.md, JOURNEYS.md, READ-LOG.json, the trace's
Binding rule rows or any agent's notes: the brief is a summary of the operator, not the operator, and a summary of a
specification is not the specification.
Objective: answer four questions, with evidence you generated yourself.
1. Does the artefact follow from the operator's words: the deliverable, the surface of record, the platform and the
   audience?
2. If a parent plan names a primary surface, does the artefact deliver that surface, or only a secondary one? Name which.
3. Does the artefact obey every binding rule you find in the specification files, read from the files yourself and not
   from any summary? Quote each rule and show where in the running app it holds or fails.
4. Starting from the app's front door and using only its navigation, can you reach the primary surface and each journey
   screen? Name any you could reach only by typing an address.
Boundaries: fix nothing; write no files; do not judge visual design.
Return: VERDICT pass or fail. On fail, the numbered gaps, each quoting the operator's words or the specification line
and what exists instead. "Pass" is a valid and welcome answer.
```
