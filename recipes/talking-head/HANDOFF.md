# Handoff — talking-head pipeline

**Status:** merged to `main` at `16302ce`. Nothing outstanding in git.
**Where:** `recipes/talking-head/` in `Corhelix/hyperframes`.
**Next action:** run it on a Mac against real footage and import the FCPXML into
Resolve. That import is the one thing never tested.

---

## What this is

The back half of a long-form talking-head pipeline. It takes a word-level
transcript and an edit decision list and produces both a finished video and a
finished, editable timeline.

It does **not** decide the cuts. The EDL is an input, produced upstream by
`video-use`, Gling, TimeBolt, Descript, or your own silence/filler detector.

```
hyperframes transcribe → detect cuts → [ EDL ] → export_package.py → build.sh → Resolve
        ↑                      ↑                        ↑
  already in the CLI     upstream, not here        this folder
```

## Prerequisites on the Mac

| Need                 | Check                    | Notes                                                                                                                                    |
| -------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| ffmpeg               | `ffmpeg -version`        | Plain build is enough — the scripts use `trim`/`atrim`/`concat`, `libx264`, `aac`. No libass needed (nothing burns text in ffmpeg here). |
| Chrome for rendering | `npx hyperframes doctor` | Also verifies the rest of the environment. `npx hyperframes browser` manages it.                                                         |
| whisper.cpp          | —                        | `hyperframes transcribe` installs it on first use.                                                                                       |
| Python 3             | `python3 --version`      | Standard library only. No pip install, no venv.                                                                                          |
| DaVinci Resolve      | —                        | For the FCPXML import.                                                                                                                   |

## Run it

```bash
git pull
cd recipes/talking-head

# 1. Footage in place. This path is gitignored — nothing gets committed.
cp /path/to/interview.mp4 clips/media/source.mp4

# 2. Transcript (word-level timestamps)
npx hyperframes transcribe clips/media/source.mp4 -d . --model small.en

# 3. Your EDL — keeps on the SOURCE timeline. See the schema below.
#    Callouts are authored on the OUTPUT timeline, after you can see the cut.

# 4. Scaffold the package — rate, start TC, field order and length are
#    read off the file. Add --deinterlace if it warns that the source is
#    interlaced; add --record-start-tc 01:00:00:00 for house convention.
python3 export_package.py \
  --edl edl.json \
  --transcript transcript.json \
  --callouts callouts.json \
  --source-file "$PWD/clips/media/source.mp4" \
  --out out/

# 5. Render everything (this is the slow step)
out/build.sh

# 6. Import out/edit.fcpxml into Resolve
```

**Step 5 must finish before step 6.** The timeline references graphics that
`build.sh` creates; import early and they come in offline.

### Input schemas

```jsonc
// edl.json — SOURCE timeline. `ranges` also accepted, for parity with
// the long-form-shorts-engine tools.
{ "source": "media/source.mp4", "fps": 30,
  "keeps": [{ "start": 0.6, "end": 9.4 }],
  "cuts":  [{ "start": 9.4, "end": 10.9, "reason": "filler" }] }

// callouts.json — OUTPUT timeline (after cuts)
[{ "text": "...", "start": 6.5, "dur": 3.2, "x": 96, "y": 140, "w": 760, "size": 38 }]

// transcript.json — SOURCE timeline, written by `hyperframes transcribe`
[{ "text": "So", "start": 0.62, "end": 0.8 }]
```

## What you get in `out/`

| File                    | What it is                                          |
| ----------------------- | --------------------------------------------------- |
| `final.mp4`             | Full video — cut with graphics baked in             |
| `edit.fcpxml`           | The same program as an editable timeline            |
| `rough_cut.mp4`         | The cut only, no graphics                           |
| `edit.edl`              | CMX3600 conform list, cut only — fallback           |
| `captions.srt`          | For swapping the caption layer for a subtitle track |
| `graphics/*.mov`        | Every layer alone, ProRes 4444 with alpha           |
| `graphics/overlay.mov`  | All graphics flattened, full length                 |
| `graphics/stills/*.png` | Flat stills                                         |
| `manifest.json`         | Every clip and layer with timecode and lane         |

The FCPXML is a finished program, not a conform:

```
lane 2   [lower third]   [callout 1]  [callout 2]  [callout 3]
lane 1   [──────────────── captions ─────────────────────────]
spine    [─ clip 1 ─][─── clip 2 ───][──── clip 3 ────] + audio
```

Every layer is a real rendered ProRes asset at its exact frame, so the timeline
is pixel-identical to `final.mp4` by construction — the graphics are the same
renders. Any single layer can be moved, retimed, restyled or deleted without
rebuilding.

## Verified vs not

**Verified here, by arithmetic and parsing:**

- Timecode maths self-tested at 30, 25, 29.97DF and 59.94DF, including
  round-trips and the hour marks (107892 and 215784 frames). Run
  `python3 mediainfo.py --selftest`.
- A full 29.97DF interlaced export was generated against a stubbed ffprobe:
  exact `1001/30000s` frame duration, `fieldOrder="upper first"`, `FCM: DROP
FRAME`, source TC offset by the file's `01:00:00;00`, and all five layers
  still landing on their intended frames.

- FCPXML is well-formed 1.9; spine contiguous with no gaps or overlaps, summing
  exactly to the sequence duration.
- All five layers resolve to their intended timeline positions; the captions
  layer spans the full timeline and its cues are identical to the baked
  render's.
- EDL record-outs meet the next record-in to the frame.
- Every composition's inline transcript parses as JSON.
- All seven generated compositions: `hyperframes lint` 0 errors, 0 warnings.
- `build.sh` is syntax-checked; commands match the current CLI.

**Not verified — this is what your Mac is for:**

- **Nothing has been rendered.** No ffmpeg and no access to the GSAP CDN in the
  build environment, so no render or transcode ever executed.
- **The FCPXML has never been opened in Resolve.** Resolve is fussy about
  `<format>` and asset declarations. Budget one round of fixes.

## Gotchas

- **Interlaced sources need `--deinterlace`.** The render engine has no
  deinterlacer, so fields come through combed. The flag adds a `yadif=mode=0`
  prep pass (frame count preserved, so all timecode still holds) and cuts from
  the progressive intermediate. You get a warning if you forget.
- **VFR cannot be conformed.** ffprobe VFR detection warns; transcode to CFR
  first.
- **Render rate is capped at 24/30/60** by the engine. NTSC renders at the
  nominal integer and gets `-itsscale 1.001` applied — exact, nothing resampled.
  **PAL 25/50 is refused outright.**
- **No timecode required.** Elapsed time from the head of the file is the
  reference. `out/edit_ledger.json` records every removal and every word's
  source→output mapping, which is the audit trail for sync.
- **ProRes MOV for anything entering Resolve.** WebM carries alpha but renders
  as black in editors. WebM is only for the ffmpeg composite path.
- **`clips` mode vs `overlay` mode.** `clips` puts the source through the frame
  extractor, which pre-extracts every frame to disk as JPEG. Fine for shorts;
  for a 20-minute source that is ~36,000 1080p frames, order of 10–15 GB
  (estimate, not measured). Use `overlay` for long-form.
- **`gfx/` and `out/` are gitignored.** They regenerate from `export_package.py`.
  Only `clips/` and `overlay/` are committed reference compositions.
- **Do not rename `var TRANSCRIPT` to `const`.** `hyperframes transcribe` runs
  `patchCaptionHtml()`, which walks every `.html` under the project and
  overwrites a const-declared TRANSCRIPT with raw source-timeline words —
  wrong timeline, and including everything the EDL cut. `var` opts out. This
  also means step 2 above is safe to run inside this folder.
- **Cue breaks are mechanical.** Fixed word counts split noun phrases. Fix in
  the studio caption editor, or raise `--words-per-cue`.

## If Resolve rejects the FCPXML

Send back the Resolve error text and `out/edit.fcpxml`. Most import failures are
`<format>` or asset-declaration fussiness and are quick to fix.

To keep moving meanwhile: `out/edit.edl` conforms the cut alone in any NLE, then
drop `graphics/overlay.mov` on a track above it — that gets you the same picture
with a flat graphics layer.

## Useful flags

| Flag                                      | Default    |                                                                                                      |
| ----------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| `--v1 source\|roughcut`                   | `source`   | `source` cuts the original so shots keep handles; `roughcut` lays down the flattened `rough_cut.mp4` |
| `--mode clips\|overlay`                   | `clips`    | on `build_composition.py`                                                                            |
| `--only captions\|lower-third\|callout:N` | —          | emit one layer alone as a standalone asset                                                           |
| `--words-per-cue` / `--min-words`         | 5 / 3      | caption grouping                                                                                     |
| `--cut-softener`                          | 0.12       | seconds of dip per cut; `0` disables                                                                 |
| `--source-duration`                       | EDL extent | set it if the source runs past the last cut, so handles are available                                |

## Still unbuilt

The two genuine gaps, both upstream of this folder:

1. **Cut detection.** Filler/silence/bad-take detection, the last-take rule,
   minimum-gap enforcement. Currently delegated to `video-use` per the
   long-form-shorts-engine strategy lock.
2. **Visual cut scoring.** Nothing checks whether a cut lands on an awkward head
   position or mid-gesture. Cut softeners paper over it; they don't detect it.

Related work lives in `Corhelix/N8n-projects/projects/long-form-shorts-engine/`
— `sop_enhance.py`, `social_enhance.py`, `social_reframe.py`, `make_captions.py`.
Those are ffmpeg/PIL based and do not call HyperFrames; this recipe is the
HyperFrames path to the same outcome.
