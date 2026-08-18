# Goal

The measurable target for this recipe. `REQUIREMENT.md` is what was asked for;
this is how we know whether it is met. Refer to this before starting work and
measure against it after.

---

## The goal

**Drop a one-hour raw talking-head recording in, run one command, open the XML,
and the edit is already there: fillers and dead air gone, every section a
separate file, every cut visible and movable, captions and graphics aligned, at
the source's own fps and pixel size.**

Watchable end state. If it cannot be watched happening, it is not met.

---

## How it is measured

One repeatable harness, not opinion. `tests/hour.py` builds a synthetic
55-minute source with 300 cuts and asserts:

| Measure                                            | Threshold         | Current          |
| -------------------------------------------------- | ----------------- | ---------------- |
| Slices emitted, one per kept section               | = number of keeps | 300 / 300        |
| Longest generated command line                     | < 4000 chars      | 162              |
| Monolithic re-encode of the whole programme        | none              | none             |
| XML spine contiguous, summing to sequence duration | exact             | exact            |
| XML project fps and pixel size                     | = source          | = source         |
| Re-run cost when slices already exist              | near zero         | guarded, skips   |
| Largest single graphics asset                      | < 2 GB            | captions now SRT |
| EDL authored by hand                               | no                | **yes, still**   |

The last row is the open one. Everything above it passes today.

---

## Sprints

**1. Cut detection.** Produce `clean.edl.json` from the transcript instead of
consuming one. Silence, fillers, and a minimum gap between cuts.
_Success looks like:_ `detect_cuts.py --transcript t.json --out clean.edl.json`
runs on a real recording, and when you watch the slices the "um"s and the dead
air are gone and nothing is clipped mid-word.

**2. Polished script.** Emit `polished_script.txt` from the surviving words.
_Success looks like:_ the file reads as clean prose, and its word count equals
the ledger's `wordsKept`.

**3. Bad takes.** Repeated phrases and self-corrections detected, last-take rule
applied, intentional pauses before a punchline kept.
_Success looks like:_ on a recording with a deliberate double-take, the second
attempt survives and the first does not.

**4. Frame context.** Grabs at each cut point, scored for visual smoothness.
_Success looks like:_ a cut that lands on a head-turn is flagged before you see
it in the timeline.

**5. The loop.** Frames and transcript to a vision model, EDL adjusted, re-cut.
_Success looks like:_ running it twice on the same source produces a better cut
the second time, and you can see which cuts moved and why.

Sprints 1 to 3 are the polish step and are what the system is missing. 4 and 5
are the context-aware layer and are deferred until 1 to 3 are proven on real
footage.

---

## The loop

> **build, test, learn, iterate, rebuild, repeat until solid**

Analysis earns its place by choosing the next build. It never substitutes for
one. Nothing here is done until it has been run against a real recording on the
Mac, not against a synthetic harness.
