# _GOAL-BUILD-AUDIT: running /goal-build with `kind: audit`

<!-- Include, not a command. Lives beside the commands. v0.4 2026-10-21 (v0.3 2026-10-16, v0.2 2026-10-12, v0.1 2026-10-10).
     v0.4 (21 Oct 2026, Map-Builder Run A): the run is goal-build v1.2, so the subject's own specification is read in full before the walk (section 4, item 0b);
     the scratch advice no longer sends files to the session scratchpad, which the filing law and a hook forbid (the working area in section 6 is the one place).
     v0.3 (16 Oct 2026, ad-manager pilot, decisions D1-D19 in clarity-os-docs docs/audits/adintel/ad-manager/goal-build/DECISIONS.md):
     FIXTURE becomes a fourth evidence label; subject resolved from the Estate (trunk before duplicate); model split; weekly-usage
     gate and progress email; walker wording rules; lint-evidence gate before the CTO verifier; verifier round caps; import into the
     app; injected-data method for the walker. New scripts: lint-evidence, build-as-built-prd, usage-report; enumerate is Playwright.
     v0.2: the requirements trace. A v0.1 audit delivered per-repo HTML while a parent plan named the app
     module as the primary surface; nothing made the run look for the plan or quote the operator. Section 4
     item 0 and section 10 now carry the fix; the command is /goal-build v1.1.
     Why it exists: /goal-build assumes the run BUILDS a product. A screen-and-button audit of existing
     software has no product to build, so phases 1c-1f, 5 and 6 either do nothing or invite the run to
     fix the subject, which an audit must never do. This file says how each phase applies, who verifies
     what, and how the run is kept moving. Nothing here relaxes contracts 1, 3, 3b, 4b, 5, 5a, 5b or 8. -->

Read this file in Phase 0 when `kind: audit` is passed. Where it and the command disagree, this file wins for an audit run, and only for an audit run.

## 1. What an audit run is

The subject is existing software that can be run. The deliverable is an evidence report, one file per subject repo. **No line of the subject's code is changed, ever.** The run's own artefacts (the report, the harness probes, the state files) are built and fixed as normal.

A **defect** is anything observed on screen or read in code. It is logged with evidence and the run continues. A **blocker** is only something that stops the audit being completed (the subject will not start; a required identity will not resolve). A broken, phantom or ugly control is a finding, never a blocker. A hypothesis is never written as either.

## 2. Contract overrides

| Contract | In an audit |
|---|---|
| 3a Fix it, then report it | Applies to the run's own artefacts only. Never to the subject. A tempting fix goes in the finding's `portNotes`. |
| 3b Premise check | A finding's premise is "this control should do X". If X cannot be traced to the subject's own UI text, route name or schema, write the finding as an observation of behaviour, not as a defect. |
| 4 Real functionality only | Becomes the **classification vocabulary** in section 5. The audit reports what is real, it does not demand it. |
| 4b Never verify against the document that made it | Section 8 applies it to the CTO verifier. |
| 8 Reporting | Adds one line to STATUS.md: batches walked, verified, written up. |

## 3. Phase map

| Phase | Audit mode |
|---|---|
| 0 Frame | Applies, with the additions in section 4, **including the requirements trace and the parent-plan search**. |
| 1a Strategy | One page. The "reference product" is the subject itself: enumerate its routes from the router file on GitHub. |
| 1b Screens and journeys | Written for the **report** as the surface (`surface_kind: surface`): how a reader finds a screen, reads a verdict, checks a REAL claim. |
| 1c Shells | The report shell (all tabs present, every one marked NOT YET WALKED) is the shell. Walk it in a real browser at both viewports. |
| 1d UX lock | Short. Default `ux: hold`. |
| 1e Design system | Adopt the project's report template. One line naming the source. |
| 1f Foundations | Reduced to the **findings contract** (section 5), committed before any agent writes, and a one-page boundary note naming the real boundaries (scratch database, outbound calls, who writes where). |
| 2 Build | The walk. One matrix row per batch of screens. A row turns green only when the CTO verifier passes that batch (section 8). |
| 3 Verify | Lens map in section 8. |
| 4 Close | Publish each report to **every surface of record the trace names**, open them, delete the cron job, run cleanup. |
| 5, 6 | Do not apply. Record that in DECISIONS.md at Phase 0. |

## 4. Phase 0 additions

0. **Bind the command and trace the requirement, before anything else.** Run the canonical-version check and write `OPERATOR-WORDS.md`, `REQUIREMENTS-TRACE.md` and `PARENT-PLAN-SEARCH.json` as `/goal-build` Phase 0 says (bind to the canonical copies on GitHub, includes and all; the operator's own words, cited, for the deliverable, the **surface of record**, the platform and the audience; the parent-plan search; `SCOPE.txt`). For an audit the surface of record is where the operator reads the report: a per-repo file, an app module, or both, with one named primary. **An audit of one repo is often one slice of a larger audit.** Run `~/.claude/scripts/goal-build-find-parent-plan.py --out PARENT-PLAN-SEARCH.json` with the subject repo names, in every spelling, before accepting the brief's output path: a larger plan's contract and surfaces outrank the brief. `--check-trace` must exit 0 before step 1.
0b. **Read the subject's own specification before walking it.** *(v1.2)* Write `command: goal-build v1.2` in `BUILD-BRIEF.md` and the marker `.goal-build-reads-required`, then do steps R1 to R9 of `/goal-build` Phase 0 over the pinned download of the subject (item 2 below; enumerate its repo root, not a local checkout), so the audit reads the subject's intent documents in full and logs them before any agent walks a screen. An audit builds no screens: the trace says `Base app: none (audit: the subject is read, not built on)`, and there is no EXISTING-SCREENS.md, NAVIGATION-MAP.md or navigation crawl. The scope gate holds the walk's state files until the read check passes.
0a. **Resolve the subject from the Estate, before pinning.** Read `src/features/estate/data/estate.json` in `Corhelix/clarity-os-app` on GitHub `main`. Its `audits` array, in `seq` order, is the run order; a run with no subject given takes the first row whose `stage` is `Not started`. For each product, audit its repos in that order. A repo whose Estate `sits` role is `Duplicate` is audited only after its product trunk, and its report is labelled as the duplicate. Never take the subject from a parent plan alone: the pilot audited a duplicate (ad-manager) while the trunk (AdIntelPlatform) waited, because nothing checked the repo's Estate role (D19, OPERATOR-WORDS 10). Write the resolved product, repo and role into `REQUIREMENTS-TRACE.md`.
1. **Pin the subject.** Read each subject repo's `main` SHA from GitHub. Never from a local checkout. Record the commit SHA and the tree SHA of the app source (everything except the run's own `docs/`). A newer `main` found later is re-pinned in DECISIONS.md before the next batch. If the only changed files are the run's own deliverables, the source pin is unchanged and the note says so.
   **The running app is the authority for the screen list.** Declared routes seed it; a live crawl of links and redirects completes it. A route the app serves that has no tab is a gap, and an acceptance check asserts zero such routes or lists them.
2. **Run the subject from a fresh GitHub download** in the working area (section 6). If it needs a database, start a throwaway one and give every concurrent agent its own copy and its own app instance, so writes cannot collide. Write `harness/start-*.sh` and `harness/sanity.sh` first. Sanity is the command every resume runs first.
3. **Scratch writes.** The filing-law hook gates the Write tool to repo paths. Scripts and raw captures for the run are written under the working area (section 6) by shell command; the session scratchpad and the system temp folder are blocked and are never used. Ask the operator once in the brief; record the answer in DECISIONS.md. Deliverables are written only to repo paths.
4. **Resolve the identities.** CTO (`viewports/cto.md`, stacked with `audit.md`) and CMO (`viewports/cmo.md`, agent `cmo-verify`). If either will not resolve, stop.
5. **Write the probes** before any agent runs: `validate-findings` (checks a findings file against the contract), `check-report` (checks a report file is finished: no NOT YET WALKED, every control row classified and labelled, images embedded and within the size limit), `enumerate` (independent count of interactive elements on a live page, including clickable non-button elements found by pointer cursor). Each exits 0 pass, 1 fail, 2 misconfigured, and prints the numbers it saw. Run them once against the shell so their failures are seen to be real.
6. **Arm the cron job** (section 9) after the lock and `.goal-build-active` exist.

## 5. The findings contract (committed in Phase 1f)

Each agent returns one `findings.json` for its batch. The lead alone writes the report.

```
{"screens":[{"slug","route","purpose","who","problemItSolves","condition","states":[],
  "controls":[{"n","label","selector","pressed","happened","network","urlChange","reloadSurvives",
               "codeRef","dbTable","needs","classification","verdict","evidence"}],
  "problems":[],"portNotes":[],"screenshots":[{"file","caption"}]}]}
```

| Field | Allowed values |
|---|---|
| classification | `NAV` plain navigation that lands on a real route. `REAL` reaches a database or external service and the result is read back; proved by a before-and-after query. `LOCAL-ONLY` changes state that lives only in the browser on that device: lost on reload, or kept in localStorage or IndexedDB and surviving reload. Record which in `reloadSurvives`; the verdict says it is not shared and not on a server. `HARD-CODED` renders constants or mock data. `PHANTOM` does nothing, only logs or toasts, or points at a missing target. `BROKEN` throws, returns an error status or lands on an error. `UNCONFIGURED` could not be tested because the app lacks something it needs; `needs` names it: an env variable, or `isolated database` where the only database the app points at holds live data. An unconfigured control is never `BROKEN` or `PHANTOM`. |
| evidence | `observed` (seen in the browser or database this run, on the subject's own data), `FIXTURE` (seen in the browser only on test data the audit injected into its own browser), `code-only` (read in source, not seen), `observed+code-only`, or `FIXTURE+code-only`. A row whose behaviour depends on injected data is never `observed`; its `pressed` text begins "On the FIXTURE state:". |

Rules: a caption states only what is visible in the frame; a filename is not a caption. One control per row (an identical group is one row that says how many). `codeRef` is `path:line` at the pin. Navigation is never `REAL`. In a subject with no server and no configured data client any `REAL` is a violation; a browser data client (for example Supabase from the page) counts as a backend, so its controls can be `REAL`. **Never press a write against live data:** `REAL` is proved only on an isolated database copy; where none exists the write control is `UNCONFIGURED`, `needs: isolated database`, with `codeRef` and `dbTable` traced from the code. Never request a credential to make a control testable. Raw captures are `raw/<slug>__<nn>-<control>.png`, never overwritten. Shrinking comes after analysis: maximum 500 px wide, JPEG quality 60, named to match, embedded in the report and kept beside it in `shots/`.

## 6. Batching and concurrency

- Contract first, writers second (command section on subagents). The contract in section 5 exists before the first agent starts.
- One agent per batch of screens. **Start at four at once**, one browser instance each with its own temporary profile, its own output folder, and (where there is a database) its own database and app instance. The real limits are the database copies and the CPU, not browsers. Raise the number only while the sanity script's response time stays under two seconds, and drop it when it does not. Never drive the session's shared Playwright tool from parallel agents: it is one browser and refuses a second caller.
- Agents return findings and evidence paths. They never write the report or any state file.
- **Per-screen checkpoint.** After each screen an agent writes `findings.partial.json` (all screens finished so far) and notes the screen it is on in `CURRENT`. A killed agent costs one screen, not the batch. At the end it renames the file to `findings.json`.
- A batch that was interrupted resumes from the screen named in `CURRENT`. It is re-run from its start only if its partial file fails `validate-findings`. Passing is not verified: it only means the file is well formed.
- **Models (D8).** Orchestration and every checker (the CTO verifier, the CMO verifier, the requirements fidelity verifier) run on Opus. Walkers, the PRD writer, the shrinker and the importers run on Sonnet. Name the model in every spawn call.
- **Usage gate and progress email (D9, D10).** Before starting any agent, run `scripts/usage-report.py --gate` (with `AUDIT_RUN`, `AUDIT_PKG`, `AUDIT_PR` set or passed as `--run`, `--pkg`, `--pr`). Exit 2 means the week is at or over 75% of the allowance: start nothing, email the hold (`--email`), flag it in STATUS.md and stop. Exit 3 means there is no reading: say so, never estimate. Run `--auto` at every stage change so Andrew gets a progress email on each one.
- **Populated states when no data is reachable (D12).** A walker that cannot reach populated states may answer GET requests to the dead database address with synthetic rows inside its own browser only. It never fakes writes, webhooks or an OAuth redirect: those fail for real. It aborts requests to real third parties. Every row, state, caption and problem that depends on injected data carries the FIXTURE label.
- **Live data in CLARITY OS (decision 3 of the audit plan, Andrew 16 October).** Screens of `clarity-os-app` are audited against the live Supabase project with reads allowed and every write blocked inside the auditing browser: the walker aborts every non-GET request to the Supabase REST, RPC, storage and functions endpoints and every request to an outside service. A save or delete is traced from code and the migration and is `UNCONFIGURED` with `needs: write blocked on live data`. Sign-in uses Andrew's magic link, which an unattended walker cannot open: when no signed-in browser state is available, park that row with `BLOCKED: sign-in needed`, email it, and continue with the next row. Never ask for or store a password.
- **Working area.** The subject's download, its running copy, raw captures and harness live on the Hillcrest-L SSD under `/Volumes/Hillcrest-L/audit-runs/<date>/<product>/<repo>/` (Andrew, 14 October). The session scratchpad and the system temp folder are blocked by the shell hook and are never used.
- An agent that cannot write because of a gate reports that as a **tooling stall**. The lead resolves the stall from the brief, never by instructing the agent to bypass a gate the operator has not approved.

## 7. Spawn prompts

### A. Walker and tracer (staffed by the CTO identity)
```
Staffed by: CTO. This is an AUDIT, not a build. Log every defect with evidence and continue. Never fix,
never edit the subject's code, never follow a tangent. A blocker is only what stops you completing the
audit; a broken or phantom control is a finding.
Subject: [name] running at [url], code at [path of the pinned GitHub download], pin [SHA]. Database
(if any): [connection, your own copy]. Your screens: [list]. Viewports: [1440x900, 390x844]. Settle before each capture (scripts/settle.mjs: finite animations finished and layout still for 300 ms),
then poll for the specific change a control should cause before judging it. Contract: [path to findings contract].
For each screen: enumerate EVERY interactive element, including clickable non-button elements. For each
one, reload fresh, press it, record what changed, the URL, the network requests, console errors and
whether the effect survives a reload. Screenshot before and after every change. Then trace the handler to
its end in the code (and the database) and classify it. Prove every REAL with a before-and-after query.
Mark every claim observed, FIXTURE or code-only. Judge each screen as the person it is for: who, the problem it
solves, its condition, and what that person cannot do.
Wording rules (a verifier fails a batch on these, so follow them from the first row):
- Observed columns (pressed, happened, network, urlChange, reloadSurvives) carry only what you saw or measured.
- Every Problems claim you did not see is marked "Code-only:" or "Inference:" at its start.
- No bare screenshot IDs in any text; say what the frame shows.
- No service names taken from config or code in an observed column.
- Never take another agent's result, or the lead's, as your own observation.
- Anything reached only with injected data carries the FIXTURE label, in the row, the state, the caption and the problem.
Write scripts and captures under [scratch output folder] by shell command. Write nowhere else.
Return: findings.json path (checkpointed per screen); screens done; counts by classification; what you did not reach and why.
```

### B. Shrinker (staffed by the CMO identity)
```
Staffed by: CMO. Input: [raw folder] and [findings.json]. For each screenshot named in the findings,
write a JPEG at most 500 px wide, quality 60, to [shots folder] under the same name with .jpg. Do not
open or alter the findings. Return the list of files with sizes and the total.
```

### C. Narrative writer (staffed by the CMO identity)
```
Staffed by: CMO. Input: [findings.json] and its screenshots. For each screen write, in plain words at
Year 9 reading level, Australian spelling, no emojis, no hedging: what the screen is for, who uses it,
the problem it solves, its condition, and what the person cannot do. Use only facts in the findings and
the images. Quote, do not paraphrase, any label or message the app shows. Return text per screen. Write
no files.
```

### D. CTO verifier (Lens 4 inputs only)
```
Staffed by: CTO (audit lens). You are verifying a finished report file for [subject]. You get the live
subject at [url], the pinned source at [path], and the finished report [path]. You do NOT get any agent's
findings or notes, deliberately.
Work out the answer first, then compare. 1. Enumerate every interactive element on each screen yourself;
the count and names must match the control table. 2. Re-press at least 3 controls per screen, or 10%,
whichever is larger, including one the report calls PHANTOM and one it calls REAL or LOCAL-ONLY; results
must match. 3. Every REAL has a before-and-after query that you re-run. 4. Every code reference resolves
at the pin and the code does what the row says. 5. Every claim is labelled observed, FIXTURE or code-only and no
code-only claim reads as something seen, and nothing seen only on injected data is labelled observed. Grade each failure BLOCKING or MINOR; pass when none is BLOCKING. 6. The download equals the pin (git diff empty). 7. Show the
check can fail: alter one verdict in a copy and confirm your comparison catches it.
Return VERDICT pass or fail, with the evidence you generated. A verdict without evidence is a fail.
```

### E. CMO verifier (agent `cmo-verify`)
```
Staffed by: CMO. Read the finished report [path] against the screenshots embedded in it. Judge: 1. each
screen's who, problem solved and condition agree with its screenshots and control table; 2. no invented
figure, name, date or quote, every number recomputes from the table; 3. each caption states only what the
image shows; 4. Australian spelling, no em-dash connectors, no stock AI vocabulary, no emojis, no hedging;
5. PRD status states match the evidence tabs they link to; 6. a Year 9 reader can say what a screen does.
Grade each failure BLOCKING or MINOR; pass when none is BLOCKING.
Return VERDICT pass or fail, with the quoted lines that failed.
```

## 8. Verification

**Verified as each batch lands, not once at the end.** A wrong batch is caught before the next is written up.

| Lens | In an audit |
|---|---|
| 1 Code | Both probes exit 0 on every findings file and report file. The report loads with no console error and its navigation works. |
| 2 Visual | The report viewed at 1440 and 390 in every navigation state. The CMO verifier (E) reads it against its own images. |
| 3 Journey | The reader journeys written in Phase 1b, walked by hand. |
| 4 Source fidelity | **Two verifiers.** The requirements fidelity verifier (spawn prompt 8 in `_GOAL-BUILD-TEMPLATES.md`): given only the operator's words (`OPERATOR-WORDS.md` and the trace), any parent plan, and the finished surface; it answers whether the report follows from what the operator asked for and whether the primary surface was delivered. The CTO verifier (D): given only the live subject, the pinned source and the finished report; it answers whether the report is true of the app. Neither is given the brief. |

**Evidence lint gate (D16).** `scripts/lint-evidence.py` must exit 0 on every findings file before a CTO verifier starts: it catches by rule what the verifiers otherwise find by reading (code in observed columns, unmarked code claims in Problems, bare screenshot IDs, narrating captions, and a row labelled observed that rests on injected data). Run `check-findings-quality.py` and `validate-findings.py` alongside it.

**Round caps (D18).** At most 3 CTO rounds and 3 CMO rounds. Each verifier grades every failure BLOCKING or MINOR and passes the batch when none is BLOCKING; MINOR points are listed in STATUS.md, not re-verified. After the cap, publish as the documents stand, record the open points in STATUS.md and hold for the operator. Do not start a further Opus round.

A fix to the report is never verified by whoever made it. A row turns green only on the verifier's pass.

## 9. Cron

Arm one recurring job in Phase 0, after the lock exists, with the scheduling tool the session provides. Every 20 minutes, offset from the hour (for example :07, :27, :47).

Prompt: `Resume the [name] audit. Read STATUS.md, FEATURE-MATRIX.md and REQUIREMENTS-TRACE.md in [build folder]. Run harness/sanity.sh first. Continue the first failing row. Audit only: never fix or edit the subject. Stop and report if every row is green or a real blocker is written against a row.`

An unattended estate run uses the same job: after a row closes, the next prompt resolves the next `Not started` row from the Estate (section 4, item 0a). The usage gate (section 6) runs before every agent, so the job holds itself at 75% of the weekly allowance and emails.

It runs on the subscription, never on an API key. It is deleted at Phase 4. Two consecutive checkpoints with no row turning green is a stall: report it, do not work through it silently.

## 10. Close

Publish each report with the project's publish script, one pull request per repo, **to every surface of record the trace names**. If the trace names an app module as primary and this run only produces the per-repo archive, the run is not done: say so in STATUS.md and hand over the findings in the shape that module needs. Open each file locally. Delete the cron job. Run cleanup: stop servers, delete scratch downloads and the database. Raw captures in the working area are kept until the operator says delete, and the operator is asked first with file counts and sizes. Before the final report, close the trace: write `Primary surface delivered: <path or URL>` in `REQUIREMENTS-TRACE.md` (the stop gate checks it). **Output to the app (after the CMO pass).** Import the verified run with `scripts/import-audit-run.py` in `Corhelix/clarity-os-app` (merged in PR #220): `--id --name --repo --findings --prd --report --archive-url --audited-on --shots-held`. In the same single clarity-os-app pull request, update the product's `audits` row in `src/features/estate/data/estate.json`: `stage`, `reportUrl`, `prdUrl` and `note`. Screenshots are not copied into `public/` until Andrew decides decision 4 of the audit plan (the live site serves `public/` without sign-in); say so in `--shots-held`. Build the as-built PRD with `scripts/build-as-built-prd.py` on the CLARITY report template, and run `scripts/check-report.py` on the report before publishing.

The branch never merges itself.

## 11. Banned moves in an audit

Fixing, or editing, the subject. Calling a hypothesis a defect or a blocker. Counting artefacts (tables, routes, mock arrays) and calling it an audit. A control row with no classification or no evidence label. A row labelled observed that rests on injected data. A REAL claim with no before-and-after query. Navigation labelled REAL. Writing the report before the contract exists. An agent writing the report. A verifier that reads the findings it is verifying. Verifying a batch only at the end. Instructing an agent to bypass a gate the operator has not approved. Running agents past the point where sanity response time exceeds two seconds. Starting an agent while the usage gate says hold. Starting a CTO verifier before lint-evidence exits 0. A fourth verifier round. Auditing a Duplicate repo before its product trunk. Leaving servers, databases or scratch downloads running after Phase 4. Taking the brief's output path as the requirement without the operator's words quoted in the trace. Auditing a repo that a parent audit plan already covers without reading that plan. Reporting the per-repo archive as the deliverable when the trace names another surface as primary. Walking before the read check has passed. Calling a specification file read after a search, a head or a summary. Delegating the reads to an agent the operator did not allow.
