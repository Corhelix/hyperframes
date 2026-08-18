# Requirement of record

The original specification, verbatim, from the conversation that started this
work. It was never written down, and every drift since traces to that.

Read this before changing anything here. If a change cannot be justified
against this file, it does not belong.

---

## The pipeline, as specified

For each raw talking-head video:

1. **Audio pass.** Transcribe, detect silences / filler words / bad takes,
   output `clean.edl.json` (keep/cut ranges with reasons) and
   `polished_script.txt`.
2. **Frame/context pass.** Extract frame grabs at cut points and scene changes,
   score cuts for visual smoothness (head position, lighting), refine the EDL.
3. **Rough cut.** Apply the final EDL.
4. **HyperFrames composition.** Captions, lower-thirds and callouts as
   GSAP-timed HTML over the footage.
5. **Preview and render.**

Plus the context-aware loop: frames and transcript to a vision model, ask which
cuts look jumpy or land mid-word, adjust the EDL, re-cut.

Enhancements named in the spec, none of them built yet: bad-take detection via
repeated phrases and self-corrections, a last-take rule, minimum gap between
cuts, keeping intentional pauses before punchlines, speaker diarisation.

## What the output is meant to be

Clarified 2026-08-18, and it overrides step 3 above.

The system takes an hour-long source and **slices, reorders and reconnects**.
The deliverable is **the slices plus one linear XML** that reconnects them,
layered and aligned, with project defaults matching the source: same fps, same
pixel dimensions, same field order.

There is deliberately **no monolithic rough cut and no required flat render**.
Sections as separate files are easier to edit, move, and see where the cuts
are, and an XML that references them is exactly how an NLE expects chunked
sections to arrive. A flat file is available with `--final ffmpeg` when one is
actually wanted, and is not the point of the system.

## Built / not built

| Step                                                 | State                              |
| ---------------------------------------------------- | ---------------------------------- |
| 1. Audio pass: transcription                         | Built, `hyperframes transcribe`    |
| 1. Audio pass: silence / filler / bad-take detection | **Not built.** The EDL is an input |
| 1. `polished_script.txt`                             | **Not built**                      |
| 2. Frame/context pass and cut scoring                | **Not built**                      |
| 3. Slices and reconnection                           | Built                              |
| 4. Composition: captions, lower-third, callouts      | Built                              |
| 5. Preview and render                                | Built                              |
| Context-aware loop                                   | **Not built**                      |
