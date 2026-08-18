# The guide

The specification this work exists to satisfy, in its own words.

**Do not condense this file into rules.** That is exactly what went wrong. The
guide is explicit about _what_ and _why_, and every drift so far came from
keeping a rule and dropping the reason attached to it. "Cut pauses over 0.6s"
is a rule. "Decide whether a pause is intentional or just dead air" is the
requirement, and it is not the same thing.

Read this before changing anything here. If a change cannot be justified
against it, it does not belong.

---

## Part 1 — The pipeline

> For each raw talking-head video:
>
> 1. **Audio pass (Python)**
>    - Transcribe, detect silences / filler words / bad takes, output:
>      - `clean.edl.json` (keep/cut ranges with reasons)
>      - `polished_script.txt` (cleaned transcript)
> 2. **Frame/context pass (Python + FFmpeg)**
>    - Use the EDL to:
>      - Extract frame grabs at cut points and scene changes.
>      - Optionally score cuts for visual smoothness (head position, lighting).
>    - Refine EDL if needed.
> 3. **Rough cut (FFmpeg)**
>    - Apply the final EDL.
> 4. **Hyperframes composition (Claude + HTML/GSAP)**
>    - Claude reads `polished_script.txt` + metadata.
>    - Generates `index.html` with the video as a clip, and captions /
>      lower-thirds / callouts as GSAP-timed HTML elements.
> 5. **Preview & render (Hyperframes CLI)**
>    - `preview` to iterate, `render` to produce the final.

The guide also supplied Python skeletons for the audio pass and the ffmpeg
assembly. They were illustrative starting points, superseded by
`detect_cuts.py` and `export_package.py`. The prose below is the part that
governs.

---

## Part 2 — What each pass is for, in the guide's words

### 1. Strip audio, polish script, cut bad bits

> **Goal: turn raw talking-head footage into a clean, tight rough cut with
> timestamps for every cut.**
>
> - Transcribe the full recording.
> - Detect and timestamp: silences / dead air; filler words ("um", "uh",
>   "like"); bad takes / restarts / repeated phrases.
> - Apply rules like:
>   - **"Last-take" rule: if a sentence is repeated, keep the second attempt.**
>   - **Minimum gap between cuts to avoid jump-cut jitters.**
>   - **Keep intentional pauses (before punchlines, reveals, etc.).**
>
> Output: a cleaned audio/video plus a timestamped cut list (JSON with in/out
> points and reasons: "silence", "filler", "bad_take").

### 2. Slice frames for context awareness

> **Goal: give the AI visual context so it doesn't make cuts that look weird or
> break continuity.**
>
> - From the cleaned timeline, extract frame grabs at: each cut point; regular
>   intervals (e.g., every 1–2 seconds); scene changes.
> - Pair each frame with: surrounding transcript (e.g., ±5 seconds of text);
>   audio features (energy, pitch, speaker ID if multi-speaker).
> - Feed this into a vision+language model so it can:
>   - **Detect mid-word cuts, awkward head jumps, gesture breaks.**
>   - **Decide whether a pause is intentional (e.g., before a key point) or just
>     dead air.**

### 3. Edit in loops

> **Goal: iteratively refine pacing, framing, and on-screen text until it feels
> right.**
>
> **Pass A — Pacing & cuts.** Assemble a rough timeline from the cut list.
> Re-run audio analysis on the assembled cut: check for unnatural jumps, breath
> cuts, or clipped consonants. **Adjust cut points by a few frames where
> needed.**
>
> **Pass B — Visual consistency.** For each segment check head position and
> framing changes across cuts, and sudden lighting or background shifts. If
> jumps are too harsh: insert micro-dissolves or very short crossfades, or
> replace some cuts with B-roll / screen captures.
>
> **Pass C — Text overlays & captions.** From the polished transcript and
> timestamps, generate word or phrase-level captions, lower-thirds, callouts and
> emphasis highlights. Render as HTML/GSAP, preview, tighten, re-render until
> the timing matches the audio and visual rhythm.

### The division of labour

> - **Claude** orchestrates the logic and prompts.
> - **FFmpeg** handles trimming, frame extraction, and encoding.
> - **Hyperframes** handles motion graphics and captions as code.

---

## Reasons that must not be dropped

Each of these is a _why_. A rule implementing one of them without carrying the
reason is how this drifted before.

| The requirement                                                             | What it rules out                                                                                                                          |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Decide whether a pause is intentional or just dead air                      | A fixed silence threshold. Intent is contextual, so classification needs frames, surrounding transcript and audio features, not a constant |
| Keep intentional pauses, before punchlines and reveals                      | Cutting on duration alone. A long pause before a key point is the point                                                                    |
| Minimum gap between cuts, to avoid jump-cut jitters                         | Many small cuts. The gap exists to stop the edit reading as edited                                                                         |
| Last-take rule: if a sentence is repeated, keep the second                  | Guessing which attempt was wanted                                                                                                          |
| Give the model visual context so cuts do not look weird or break continuity | Deciding cuts from the transcript alone                                                                                                    |
| Adjust cut points by a few frames where needed                              | Treating a cut point as fixed once chosen. It is nudged, not just kept or dropped                                                          |
| Detect mid-word cuts, awkward head jumps, gesture breaks                    | Assuming a cut that is clean in the audio is clean on screen                                                                               |

## Later clarifications, which sit on top of the guide

**Slices, not a flat render.** The system takes an hour-long source and slices,
reorders and reconnects. The deliverable is the slices plus one linear XML that
reconnects them, layered and aligned, project defaults matching the source: same
fps, same pixel size, same field order. No monolithic rough cut and no required
flat render.

**Fewest cuts wins.** The point is the least amount of cuts, not more, so that it
flows without hard cuts or anything that reads as "this has been edited".

**Breathing space over tight cutting.** Healthy pauses of half a second or more,
even one or two seconds, are pacing and stay. Nobody speaks in a continuous
stream, and an edit with no air in it is the failure.

**Sampling cadence is not a cutting threshold.** Frames are sampled often, for
contextual view. Cuts stay rare. Opposite frequencies.

**Delivery is part of the system.** The speaker can say "redo", or pause and
retake a section, which turns bad-take detection from a heuristic into a
certainty. See `RECORDING-PROTOCOL.md`.

---

## Built against it

| Requirement                                                             | State                                                                                                           |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1. Transcription                                                        | Built, `hyperframes transcribe`                                                                                 |
| 1. Silence and filler detection                                         | Built, `detect_cuts.py`. **Threshold-based, which is a stand-in** for the contextual classification §2 requires |
| 1. Last-take rule and bad takes                                         | Built, `detect_cuts.py`, via spoken marker and repeated opening                                                 |
| 1. Minimum gap between cuts                                             | Built, `--min-gap`                                                                                              |
| 1. Keep intentional pauses                                              | **Partial.** Duration is used as a proxy for intent. Nothing yet knows a punchline is coming                    |
| 1. `polished_script.txt`                                                | **Not built**                                                                                                   |
| 2. Frame grabs at cut points, intervals, scene changes                  | **Not built**                                                                                                   |
| 2. Pair frames with ±5s transcript and audio features                   | **Not built.** Audio energy and pitch are unused, and they are available without vision                         |
| 2. Vision pass: mid-word cuts, head jumps, gesture breaks, pause intent | **Not built.** This is what makes the pause decision contextual rather than numeric                             |
| 3. Pass A, re-analyse the assembled cut, nudge cut points by frames     | **Not built**                                                                                                   |
| 3. Pass B, visual consistency, micro-dissolves where a join is harsh    | **Not built**                                                                                                   |
| 3. Pass C, captions and overlays as HTML/GSAP                           | Built                                                                                                           |
| Slices plus reconnected XML                                             | Built                                                                                                           |
| Preview and render                                                      | Built                                                                                                           |
