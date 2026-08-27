# _GOAL-BUILD-TEMPLATES — state schemas and spawn prompts for /goal-build

<!-- Include, not a command. Lives beside the commands, like _GATE-MECHANICS.md. v0.2 2026-08-21 -->
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

## Mission
[outcome, reference products, better means, out of scope — from the brief]

## Specifics
[stack locks, brand, data/auth/hosting, repo, credentials on hand]

## Quality bar
[non-negotiables, evidence required at done]

## Sanity
[the one command that proves the app still boots — every resume runs it first]

## Assumptions
| Slot | Value chosen | Source |
|---|---|---|
| [slot] | [value] | given / assumed |
```

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

### JOURNEYS.md

```
| ID | Journey | As whom | Owner | Gestures (numbered, in order) | Final state observed | Status | Evidence |
|---|---|---|---|---|---|---|---|
| J1 | [what the person is trying to achieve] | [role/permissions] | [C-level identity] | 1. [gesture] 2. [gesture] … | [what proves it worked] | not-walked | — |
```

Rules: a journey is a composite, and its status is independent of the features inside it — never mark it walked because its parts passed. Status values are `not-walked`, `walked`, `broken`. It becomes `walked` only when someone performed every gesture in one continuous sitting in a real browser and observed the final state, with a capture to show it. J0 is always the defining gesture.

### STATUS.md

Rewritten in full at every phase boundary, every park and every escalation. It is a snapshot, never a log, and it fits on one screen.

```
# STATUS — [project] · [ISO timestamp]

Phase:      [0-4, and what is happening right now]
Matrix:     [n] green · [n] parked · [n] failing   (of [total])
Journeys:   [n] walked · [n] broken · [n] not-walked
Defects:    [n] open · [n] fixed · [n] retested    Phase 3 sweep: [not-run|complete]

In flight:  [the row or journey being worked, and its owner]
Blocked:    [F# — trigger, one line each; or "none"]
Last evidence: [most recent path written]
Next:       [the single next action]
```

Rule: an operator reading only this file knows where the run is. If that is not true, the file is wrong.

### evidence/ — the naming law

```
evidence/A{n}-{surface-or-state}-{viewport}.png     acceptance check capture
evidence/J{n}-{step}-{what}.png                     journey step capture
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

