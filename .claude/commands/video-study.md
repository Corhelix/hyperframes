---
name: video-study
description: Study reference videos for the video SOP engine, end to end, with independent audit and a done gate per video.
argument-hint: "<YouTube links or local files, plus any supplied notes>  [batch: NN]"

contract:
  writes: true
  fires_when:
    - one or more reference videos are supplied for the video SOP engine's research corpus
  does_not_fire_when:
    - a video is to be turned into an SOP booklet or enhanced video (that is the engine itself, /video-sop, not yet built)
  loads:
    always:
      - projects/video-sop-engine/SOP-reference-video-study.md
      - projects/video-sop-engine/README.md
      - projects/video-sop-engine/pipeline/CHANGELOG.md
      - the newest projects/video-sop-engine/research/synthesis/*-synthesis.md
      - the newest projects/video-sop-engine/drafts/DRAFT-video-sop-engine-plan-*.html (Goal, Callouts, Stills, Review, Batch sections)
      - projects/video-sop-engine/research/2026-10-22-attention-cadence/README.md
      - projects/video-sop-engine/prompts/segment-analyst-reference.md
      - projects/video-sop-engine/templates/reference-report.md
  returns:
    - id: studies
      is: one folder per video under research/reference-videos/ that passes checks/validate_study.py
    - id: synthesis
      is: research/synthesis/<date>-batch-NN-synthesis.md, and the plan's next version folding it in
  acceptance:
    - checks/test_pipeline_fixes.py --teeth passed before the first video started (output quoted)
    - checks/validate_study.py exits 0 for every video (output quoted)
    - every analysis and audit was written by the agent its contract names, and no reviewer saw section 8
  graded_by: cmo-verify
status: DRAFT v0.1, 2026-10-22. Proven on batch 01 by hand; first run as a command is batch 02.
---

# /video-study: study reference videos for the video SOP engine

You are the orchestrator. You own the outcome: every video ends as a study that passes its done gate, and the batch ends as a synthesis that changes the engine. You coordinate; you do not do an analyst's or an auditor's job for them, and you never mark your own work done without the gate.

Home: `C:\Users\hello\Documents\CLEAN\N8n-projects\projects\video-sop-engine\`. All paths below are relative to it. Pipeline commands run from `pipeline/`.

## Phase 0: get in the zone

1. **Read every file in `loads.always`.** Quote back, in one line each: the current plan version; the three rules in the SOP's "not optional" list you think most likely to be broken on this batch; the last three changelog rows. If a file does not resolve, stop and say which.
2. **Branch.** In the canonical clone, a new branch off `origin/main`: `feat/<date>-m1-batch-NN`.
3. **Preflight.** `python pipeline/doctor.py`. Quote every FAIL and WARN line and the verdict. NO-GO stops the run before any video starts. Triage each FAIL with the rule below: an environment FAIL (memory, a tool missing) is Andrew's to clear, so say exactly what to do and wait; a code FAIL that is small is fixed now with a changelog row and a check.
4. **Log what was supplied, verbatim** (SOP step 1), before touching anything else.

## The triage rule (applies to every error, every phase)

When anything fails, decide at once, against the contract, and write the decision with `checks/incidents.py --triage`:

| Blocks the contract output? | Fix size | Decision |
|---|---|---|
| yes | small (cause understood, contained, checkable, about 20 minutes or less) | fix now: changelog row, failing check, fix, resume |
| yes | large | flag-later and park that study; carry on with the rest; report it |
| no | any | flag-later; carry on at once; do not fix it now |

Standing rules: one study's failure never stops the batch; no fix is started unless it is for a blocking incident; never stop to ask about something the rule already decides. Stop and ask Andrew only for a credential, an irreversible or outward action, or an environment fault only he can clear.

## Phase 1: per video, the mechanical stages

For each video (they may run one after another; the GPU stages never run two at once):

- SOP steps 2 to 4. `run_batch.py <studies>` (or `run_reference.py` for one), never a hand-chained shell command.
- A study that stops: read its `STATUS.md` and incident, triage, then either fix and re-run the same command (finished stages are skipped) or park it and move on. The other studies are not held up.

## Phase 2: per video, segment analysis (fan-out)

Dispatch one **segment analyst** per segment, in parallel (at most 6 at once). A segment with more than 13 contact sheets is split between two analysts.

**Work contract: segment analyst**

| | |
|---|---|
| Role | general-purpose agent, reads images |
| Reads | `prompts/segment-analyst-reference.md` and follows it exactly; its segment's `work/shot-sheets/<seg>.md`; its named contact sheets in `media/sheets/`; `work/transcript.json` for exact timing |
| May write | exactly one file: `data/segments/<seg or seg-part>.analysis.json` |
| Must not | read any other segment's files, the report, or any audit |
| Returns | one line: the file path and the count of sheets read, graphics, key sentences |
| Done when | its file parses, `sheets_read` lists every sheet it was given, every graphic sits inside its time range |

Brief each analyst with the video's title, URL, its segment bounds and sheet names, and two or three sentences on what that stretch of video contains (from the shot sheet).

**Contract check on return:** `python checks/validate_analysis.py <file> --start <s> --end <e> --sheets <its sheets>`. Errors go back to the same analyst once, verbatim, with "fix only these". A second failure is an incident for stage `s5:<seg>`, triaged by the rule; the other segments carry on.

Then: close every coverage gap in the main loop (SOP step 6). Gate: `validate_study.py <study> --stage analyses`.

## Phase 3: per video, probes and the report

- `python probe_keys.py <study>`; review `data/probe-keys-unmatched.json`.
- `python s6_probe.py <study> --keys <study>/data/probe-keys.json`.
- Read every `media/probe/_review-*.jpg`. Write `data/probe-picks.json`. A probe that misses its moment gets a new key and a re-probe, never a fudged pick.
- Measure timing (SOP step 10) from word times. State the 2 fps resolution with every number.
- Write `data/report-analysis.md`, then `python build_reference_report.py <study>`.
- Gate: `validate_study.py <study> --stage independence`.

## Phase 4: per video, independent audit

Dispatch one **auditor** per video, in parallel.

**Work contract: auditor**

| | |
|---|---|
| Role | general-purpose agent on **Opus**; adopts `~/.claude/viewports/cmo.md` with `~/.claude/viewports/audit.md` stacked |
| Reads | `work/report-for-audit.md` (section 8 withheld), every image in `frames-selected/`, the contact sheets you name for the stretches closest to the engine's use, the plan's Goal section, the cadence log, the newest synthesis |
| Must not | read `report.md`, `data/report-analysis.md`, or any other video's audit |
| May write | exactly one file: `cmo-audit.md`, verdict line first |
| Answers | (1) is the report true and sufficient, checked against frames; (2) what helps or hurts our booklet and our enhanced video, by time; (3) and (4) the two questions most specific to this video; (5) 3 to 7 concrete engine changes tied to evidence; (6) strategic view: where the value is and the biggest risk |
| Not asked | language, spelling or prose style |
| Returns | the verdict line and its change table |

Gate: `validate_study.py <study>`. It must print `DONE`. Quote it.

## Phase 5: the batch

1. **Synthesis** (SOP step 15). Where a report and its audit disagree, open the frames and use whichever the frames support; say which.
2. **Changelog.** Every fault met in this batch is a row, and every row names its check. A fault without a check is still open.
3. **Plan.** A new version folds the synthesis in, surgically: copy, edit only what changed, archive the old version, validate the HTML (balanced tags, anchors resolve, no em dashes or banned words).
4. **Publish** (SOP step 16): commit without `media/`, `work/` or `__pycache__`; PR; merge only on Andrew's word.

## Report back

One message: per video, the gate line and the audit's verdict line; the batch's three changes that matter most; the PR link; then **Flags**: every incident decided flag-later this batch (from `checks/incidents.py --flags`), each with whether it blocks and why it waits. `python checks/incidents.py` must report nothing untriaged. Australian English, no em dashes.

## Drift: banned moves

Starting a video before the doctor says GO. Stopping the batch for one study. Fixing something that does not block the contract output. Stopping to ask about a decision the triage rule already makes. Leaving an incident untriaged. Chaining stages by hand. Writing an analysis or an audit yourself when its contract names an agent. Showing an auditor section 8. Fudging a probe pick. Quoting a first-pass shot kind as fact. Quoting a timing number without its sampling resolution. Calling a study done without the gate's `DONE` line. Fixing a fault without adding its check. Committing `media/` or `work/`.
