---
name: video-sop
description: Turn a video into an SOP booklet on the accepted LinkedIn study-booklet standard, through the video SOP engine's stages and gates, with no deviation.
argument-hint: "<YouTube link or local file, plus any supplied transcript or notes>  [rung: C1|C2|C3|C4]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a video, recording or talk is to be turned into an SOP booklet or study guide
  does_not_fire_when:
    - reference videos are to be studied for the engine's research (that is /video-study)
    - a video is to be cut or edited (that is /video-edit)
  loads:
    always:
      - Corhelix/N8n-projects:projects/video-sop-engine/ACCEPTANCE-VSOP.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/drafts/DRAFT-video-sop-engine-plan-v0.4-2026-10-22.html@main
      - Corhelix/N8n-projects:projects/video-sop-engine/pipeline/CHANGELOG.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/renderer/README.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/harness/README.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/reference/README.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/segment-analyst-booklet.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/chapter-plan.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/step-rewrite.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/picker-v2.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/figure-verifier-v2.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/fidelity-verifier.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/walker-v2.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/gap-adjudicator.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/orchestrator-gate.md@main
      - Corhelix/N8n-projects:projects/video-sop-engine/prompts/investigator.md@main
      - Corhelix/alc-group:andrew-cockburn/content/tasks/2026-10-16-linkedin-video-guide/ACCEPTANCE-V2.md@main
      - Corhelix/alc-group:andrew-cockburn/content/tasks/2026-10-16-linkedin-video-guide/LEARNINGS.md@main
      - Corhelix/alc-group:andrew-cockburn/content/tasks/2026-10-16-linkedin-video-guide/research/time-review-and-template-plan.md@main
      - Corhelix/claude-system:global/hooks/README-video-sop-gates.md@main
    skills: []
  returns:
    - id: booklet
      is: runs/<slug>/booklet/, built by renderer/build.py, every gate GO
    - id: evidence
      is: runs/<slug>/evidence/scorecard.json and gate files, written by checks/vsop_gate.py only
  acceptance:
    - the /video-sop hooks were armed in block mode before the first tool call (the arm message is in the transcript)
    - checks/read_proof.py --verify passed before S1 (output quoted)
    - checks/vsop_gate.py printed GO for every stage in order, ending S10 (outputs quoted)
    - every agent was briefed from a prompts/ file named in its prompt, and no reviewer built what it judged
  graded_by: cmo-verify
status: DRAFT v0.1, 2026-11-11. Built after the Lara Acosta batch failed (PR 51) because no command or hook enforced the SOP. First run is a C1 clip.
---

# /video-sop: a video into an SOP booklet, on the SOP, with no deviation

You are the orchestrator. You own the outcome: a booklet of the same kind as the accepted LinkedIn study booklet, for this video. That means:
- a cover, how to use page, contents, and a divider and checklist per chapter;
- guide sheets where each guide has what you'll achieve, before you start, numbered steps with a do line and a why line, a picture only where the screen shows what the step names, common mistakes, a key takeaway, a watch link and an up-next pointer;
- a source page.

You coordinate. You never do an analyst's, picker's, rewriter's, verifier's, reviewer's or builder's job, and you never mark a stage done: only `checks/vsop_gate.py` does.

**Home:** `C:\Users\hello\Documents\CLEAN\N8n-projects\projects\video-sop-engine\`, on GitHub `Corhelix/N8n-projects` `projects/video-sop-engine/`. All paths below are relative to it.

**The hooks are on.** While this command runs, the `/video-sop` gate hooks deny:
- any hand-written HTML;
- any write under a run's `out/` or `booklet/` except by `renderer/build.py`;
- any write to the scorecard, gate or read-proof files except by the gate scripts;
- any new code file, and any script outside `pipeline/`, `checks/`, `renderer/` and `harness/`;
- any agent briefed without a `prompts/` file;
- a render before its gates are GO.

A denial is the SOP speaking. Do not look for a way round it. Read the denial, then do the step the SOP names.

## Phase 0: get in the zone (S0)

1. **Branch.** In `Corhelix/N8n-projects`, a new branch off `origin/main` through GitHub: `feat/<date>-vsop-<slug>`.
2. **Run folder.** `runs/<YYYY-MM-DD>-<channel>-<slug>/` with `media/`.
   - Download with `yt-dlp` up to 1080p with `--write-info-json` into `media/source.mp4` and `media/source.info.json`.
   - Or copy a local file; never move it.
   - Log what Andrew supplied, verbatim, into `supplied/` with sha256.
   - Write `course.json` (keys in `renderer/README.md`).
3. **Preflight.** `python pipeline/doctor.py`. A NO-GO on memory or tools is Andrew's to clear: say exactly what, and wait (`checks/vsop_gate.py <run> --wait andrew --reason "..."`).
4. **Read every load in full.**
   - Run `python checks/read_proof.py <run> --challenge`.
   - Read each file it lists, in full, from GitHub main.
   - Look at every reference page shot in `reference/` with the Read tool.
   - Write the answers to `<run>/read-answers.json`: `{"<load>": {"<line>": "<first 8 words>"}}`.
   - Run `python checks/read_proof.py <run> --answer <run>/read-answers.json`. It must print `READ PROOF OK`.
5. **PLAN.md.** One page:
   - the rung (C1 to C4 by length);
   - the source;
   - the booklet title as Andrew would say it;
   - the presenter's own sections, from the chapter list or the opening;
   - what the screen shows (talking head, slides, screen recording);
   - the known traps: sponsor segments, the presenter's own products, claims to attribute.
6. **S0 gate.**
   - Run `python checks/vsop_gate.py <run> S0`. It returns the `JUDGED` hash.
   - Dispatch the **orchestrator** (Opus, `prompts/orchestrator-gate.md`) with PLAN.md, ACCEPTANCE-VSOP.md and the hash.
   - It writes `reviews/orchestrator-S0.md`.
   - Re-run the gate until it prints `S0: GO`.

## Phase 1: the mechanical stages (S1 to S4)

`python pipeline/run_reference.py <run>`. Never chain the stage scripts by hand. Then gate each stage in order: `python checks/vsop_gate.py <run> S1`, `S2`, `S3`, `S4`.

A stop is an incident. Triage it with `checks/incidents.py --triage`, using the engine's rule:
- **Fix now** only if it blocks and is small, with a changelog row and a failing check first. Engine code may be edited only while that incident is open.
- **Otherwise flag it** and carry on, or park it.

## Phase 2: the first-segment stop (pilot, segment 1)

Every step below is one agent per unit. Each agent is briefed with the named prompt file, quoted by path in its prompt.

| Step | Agent and prompt | Writes | Gate |
|---|---|---|---|
| S5 | Segment analyst, booklet mode: `prompts/segment-analyst-booklet.md` (one per segment, at most 6 at once) | `data/segments/seg-NN.booklet.json` | `vsop_gate.py <run> S5@pilot` |
| S7 | `pipeline/s7_stitch.py <run> --list`, then the chapter planner (`prompts/chapter-plan.md`), then `pipeline/s7_stitch.py <run>`, then step rewriters (`prompts/step-rewrite.md`, one per batch) | `data/chapters.json`, `work/topic-map.json`, `work/guides/`, `data/steps/b*.json` | `S7@pilot` |
| S6 | `pipeline/s6_candidates.py <run>`, then pickers (`prompts/picker-v2.md`), then a FRESH blind batch of figure verifiers (`prompts/figure-verifier-v2.md`, new agents, never the pickers), then `pipeline/s6_figures.py <run>` | `work/figures.json`, `work/figs/` | `S6@pilot` |
| S9 | `COURSE_ROOT=<run> python renderer/build.py --measure --out <run>/work/measure-book`, then `python renderer/measure_units.py`, then `COURSE_ROOT=<run> python renderer/build.py --gate S9@pilot --only <pilot guide ids>` | `booklet/` | `S9@pilot` |
| S10 | Six independent reviewers (brand, figure, fidelity, walk with gap adjudication, contextual on the CMO lens, owner checklist), each seeing only the source and the built booklet, each writing `reviews/<reviewer>-S10@pilot.json` with the build hash. Findings go to a fixer agent (never the builder or a reviewer), then fresh reviewers. Then the orchestrator. | `reviews/` | `S10@pilot` |

If the pilot's S10 is NO-GO, apply the orchestrator's edits and re-gate from the stage they touch. After three NO-GOs on one criterion, change the approach, record why in the run's `DECISIONS.md`, and carry on.

## Phase 3: the full run

S5, S7, S6, S9 and S10 again over every segment, on the rules the pilot settled, ending `vsop_gate.py <run> S10: GO`.

For C1 and C2, record `--wait andrew` and show Andrew the booklet in Chrome. No longer run starts until he has agreed to a C1 and a C2.

## Phase 4: publish

- Commit `course.json`, `PLAN.md`, `data/`, `reviews/`, `evidence/`, `booklet/` and `supplied/`. Never `media/` or `work/`.
- Open a PR. Merge only on Andrew's word.
- Open every booklet page in Chrome from the CLEAN view copy.

## Report back

One message:
- the gate line of every stage;
- the orchestrator's final verdict line;
- the reviewers' coverage, as "reviewed N of M";
- the PR link;
- every flag-later incident.

Australian English, no em dashes.

## Drift: banned moves

The hooks deny most of these; the rest are on you.
- Writing any page, builder, brief or check of your own.
- Briefing an agent without its prompt file.
- Picking or judging a figure yourself.
- A verifier or reviewer who saw the builder's notes.
- Calling a stage done without its gate's GO.
- Skipping the pilot.
- Quoting a reviewer's verdict without its build hash.
- Sampling a review and calling it complete.
- Committing `media/` or `work/`.
- Merging without Andrew.
