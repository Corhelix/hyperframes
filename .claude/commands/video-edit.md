---
name: video-edit
description: Edit a recorded talking-head video into a natural cut, with optional layers, subtitles and XML, following the Video Edit SOP. The script is the authority; only repeated redos are cut without Andrew's sign-off.
argument-hint: "[path to recording]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a recording is to be cut, tidied or turned into a finished video, a Loom, a course module or a client explainer
    - Andrew asks for subtitles, callouts, a 9:16 version or an editable XML timeline for a recording
  does_not_fire_when:
    - the work is a script, brief or content strategy for a video -> /cmo
    - the ask is a video from scratch with generated footage -> the pletor or higgsfield routes
  loads:
    always:
      - alc-group andrew-cockburn/content/video-edit-sop/ (latest DRAFT or APPROVED): How to run, Work order, Pauses and cuts, Verify and Scripts tabs
      - Corhelix/hyperframes corhelix/video-edit/README.md
      - command-includes/_VERIFICATION-STANDARD.md
    conditional:
      - when: a callout is not a Hyperframes template
        load: [Corhelix/secrets-vault catalogue/internal.yaml entry "21st Dev"]
  returns:
    - id: cut
      is: the natural cut as MP4, with cuts/script-lock.json showing every removed span and why it was allowed
    - id: verify_pack
      is: contact sheets for every join, check results, FILES.md
    - id: handoff
      is: what was checked and what was not, naming the audience first
  acceptance:
    - the work order was confirmed with Andrew before anything was cut
    - script_lock.py passes on the final EDL, and every authorisation quotes words Andrew typed
    - a contact sheet exists for every join and was read before the first render
    - every non-template HTML callout has a recorded 21st.dev lookup in design_ref
    - nothing is called approved; frame checks are not a watch-through (V9 is a person)
  graded_by: cmo-verify

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: slash-commands/video-edit.md. .claude/commands/video-edit.md must match exactly -->

# /video-edit

The method is the Video Edit SOP. The scripts are in `Corhelix/hyperframes` `corhelix/video-edit/current/`. The gates are the `video-edit-*` hooks (`global/hooks/README-video-edit-gates.md`), which run whether or not this file is remembered. If a gate holds a step, clear what it names. Do not work around it.

## Phase 0: Load
Read the SOP tabs and the tool README listed under `loads`. Check the machine (`ffmpeg`, `ffprobe`, `~/Documents/video-use`, `uv`). Media stays in `~/Movies/<date>-<slug>/` and is never committed. Documents go to GitHub through the API.

## Phase 1: Work order
Fill in the SOP Work order for this recording (format, look, subtitles, XML, screen mix, extra sources) and confirm it with Andrew before anything is cut. Stage 01: confirm the file by its time and first minute. Write `brief.json` and `FILES.md`.

## Phase 2: Transcript
Reuse any Scribe transcript that exists. Do not run the paid one twice.

## Phase 3: Script lock
The recording's words are the script. Build the cut list from the transcript.
- Cut without asking: a repeated redo (the speaker restarts with the same opening words, usually after saying "redo"), and silence at a join under 0.3 s.
- Everything else, including fillers, dead air, trimmed heads and tails and any reorder, is proposed to Andrew with the exact words and times of the span. His typed answer becomes an entry in `cuts/authorisations.json` with his words in `quote`. Never write the quote yourself.
- Run `script_lock.py` and fix what it names until it passes.

## Phase 4: Contact sheets
Run `gap_sheets.py` for every join before any render. Read each sheet by eye and choose the splice. Mark a join "for review" if no pair looks right.

## Phase 5: Render, audio, layers
Render the cut, then audio, then beats and the layer plan, from this recording's transcript only. For HTML callouts use a Hyperframes template. If none fits, run `twentyfirst_lookup.py search` (or `video-blocks`) from the project folder, pick a result, `get` its code to port, then run `twentyfirst_lookup.py record --layer-id <id> --slug <slug>` to write `design_ref` onto the layer row. The helper takes the key from the secrets vault and never prints it, and `record` accepts only a slug or id that a logged lookup returned. Do not use 21st's `generate`: it spends AI credits.

## Phase 6: Verify
Run V1 to V9. Say what was checked. Frame checks are not a watch-through; V9 is a person watching the whole video at 1x.

## Phase 7: Review
Open a fresh branch and PR under `andrew-cockburn/content/` in alc-group for documents. Nothing is approved until Andrew says so.
