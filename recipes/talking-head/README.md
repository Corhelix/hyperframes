# Talking-head: EDL → composition

Turns a word-level transcript plus an edit decision list into a HyperFrames
composition with captions, a lower third, and callouts.

This is the last two stages of a long-form talking-head pipeline. It does not
decide the cuts — it consumes an EDL produced upstream (by `video-use`, Gling,
TimeBolt, Descript, or your own silence/filler detector) and turns it into
something HyperFrames can render.

```
hyperframes transcribe → detect cuts → [ EDL ] → build_composition.py → preview → render
         ↑                     ↑                          ↑
   already in the CLI    upstream, not             this folder
                         in this folder
```

Timestamp extraction is **not** re-implemented here. `hyperframes transcribe
video.mp4` writes `transcript.json` in exactly the shape this script reads —
it manages the whisper.cpp binary, model download, language selection, SRT /
VTT / OpenAI import, and speech-onset stripping. Both the whisper path and the
import path converge on the same normalised `[{"text","start","end"}]` array.

## Quick start

```bash
cd recipes/talking-head

# clips mode — the EDL becomes the composition
python3 build_composition.py \
  --edl sample/edl.json \
  --transcript sample/transcript.json \
  --callouts sample/callouts.json \
  --mode clips --out clips/index.html

# overlay mode — graphics only, transparent, composited later
python3 build_composition.py \
  --edl sample/edl.json \
  --transcript sample/transcript.json \
  --callouts sample/callouts.json \
  --mode overlay --out overlay/index.html --comp-id talking-head-overlay
```

Both outputs are checked in and both report **0 errors, 0 warnings** from
`hyperframes lint`. No Python dependencies — standard library only.

## Two modes

### `clips` — the EDL _is_ the composition

Each kept range becomes a `<video>`/`<audio>` pair trimmed with
`data-media-start`, laid end to end on the output timeline:

```html
<video
  id="clip-v-1"
  src="media/source.mp4"
  data-start="8.8"
  data-duration="7.3"
  data-media-start="10.9"
  data-track-index="0"
  muted
  playsinline
></video>
<audio
  id="clip-a-1"
  src="media/source.mp4"
  data-start="8.8"
  data-duration="7.3"
  data-media-start="10.9"
  data-track-index="1"
  data-volume="1"
></audio>
```

No ffmpeg pre-cut, one render, and no way for the cut timeline and the caption
timeline to drift apart. The engine only extracts frames for ranges a clip
actually references (`videoFrameExtractor.ts` passes `data-media-start` and the
clip duration straight to ffmpeg's `-ss`/`-t`), so removed footage never gets
decoded.

Use for: shorts, single scenes, anything up to a few minutes.

### `overlay` — graphics only

No media elements at all. Transparent background, captions and callouts timed
against a `rough_cut.mp4` you cut separately:

```bash
npx hyperframes render -d overlay --format webm -o overlay.webm
ffmpeg -i rough_cut.mp4 -i overlay.webm \
  -filter_complex "[0:v][1:v]overlay=format=auto" \
  -c:a copy final.mp4
```

**Use this for long-form.** The frame extractor pre-extracts every video clip
to JPEGs on disk at composition fps before compositing starts. A 20-minute
source at 30fps is ~36,000 1080p frames — order of 10–15 GB and a long pre-pass
(estimate, not measured) before a single output frame exists. In overlay mode
the source never enters the extractor.

## Inputs

| File              | Time base  | Shape                                                                                                                                                   |
| ----------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `transcript.json` | source     | `[{"text","start","end"}]` — exactly what `hyperframes transcribe` writes. Optional: omit `--transcript` to build the cut and callouts with no captions |
| `edl.json`        | source     | `{"source","fps","keeps":[{"start","end"}],"cuts":[{"start","end","reason"}]}`                                                                          |
| `callouts.json`   | **output** | `[{"text","start","dur","x","y","w","size"}]`                                                                                                           |

Callouts are authored on the _output_ timeline because you write them after you
can see the cut — the same convention as `callouts-sop.json` in the
long-form-shorts-engine. Transcript and EDL are on the source timeline and get
remapped for you.

## What the generator handles

**Frame quantisation.** Every boundary is snapped to the frame grid before any
arithmetic. `overlapping_clips_same_track` is a strict `end > start`, so a
nanosecond of accumulated float error across a few hundred clips is both a lint
error and a real one-frame seam.

**Caption remapping.** Cues are built from the transcript _and_ the EDL
together, and a cue never spans a cut. Building captions from a de-timestamped
"polished script" is the most common way this pipeline goes wrong: a cue that
straddles a removed range inherits the removed duration and drifts out of sync
for the rest of the video.

**Cut softeners.** A short dip at each interior cut (`--cut-softener`, default
0.12s, `0` disables). A true cross-dissolve is not available: it needs either
overlapping clips on one track (`overlapping_clips_same_track`, error) or an
opacity tween on a clip element (`gsap_animates_clip_element`, error) — the
framework owns clip visibility. A dip on a non-clip overlay div is the
framework-compatible option.

**Studio-editable captions.** Cues are emitted as an inline
`var TRANSCRIPT = [...]` with JSON-quoted keys, which is what the studio caption
editor looks for.

**`var`, not `const` — do not "fix" this.** `hyperframes transcribe` also runs
`patchCaptionHtml()`, which walks every `.html` under the project directory and
overwrites `const TRANSCRIPT = [...]` with the raw word list. On an
EDL-remapped composition that is wrong twice over: the words are on the source
timeline, and they include everything the EDL cut. The patcher's regex matches
`const` only, so declaring `var` opts out of the rewrite while staying readable
to the studio caption editor and to the `caption_transcript_not_inline` lint
rule, both of which accept `const`, `let`, or `var`.

## Options

| Flag                              | Default                 |                                           |
| --------------------------------- | ----------------------- | ----------------------------------------- |
| `--mode`                          | `clips`                 | `clips` or `overlay`                      |
| `--source`                        | EDL `source`            | media src relative to the composition dir |
| `--comp-id`                       | `talking-head`          | must be unique per composition            |
| `--width` / `--height` / `--fps`  | 1920 / 1080 / EDL `fps` |                                           |
| `--words-per-cue` / `--min-words` | 5 / 3                   | short trailing cues merge backwards       |
| `--gap`                           | 0.35                    | seconds of silence that forces a new cue  |
| `--cut-softener`                  | 0.12                    | seconds of dip per cut; `0` disables      |
| `--title` / `--subtitle`          |                         | lower-third text                          |

## Linting `clips/`

`clips/index.html` references `media/source.mp4`. `hyperframes lint` checks that
`<audio>` sources exist on disk (`audio_src_not_found`, error) — with no footage
present you get:

```
✗ audio_src_not_found: <audio> element references file(s) not found in the project: media/source.mp4
```

Drop your own footage at `clips/media/source.mp4` and it lints clean. Source
video is gitignored. `overlay/` has no media elements and lints clean from a
fresh checkout.

## Known limits

- **Cue breaks are mechanical.** Fixed word counts split noun phrases
  ("So most teams treat video" / "editing as a manual craft"). Fix in the studio
  caption editor, or raise `--words-per-cue`.
- **Cut detection is not here.** The EDL is an input. Filler/silence/bad-take
  detection, the last-take rule, and minimum-gap enforcement are upstream.
- **No visual cut scoring.** Nothing checks whether a cut lands on an awkward
  head position or gesture. Cut softeners paper over it; they don't detect it.
- **`clips` mode is unproven at high clip counts.** Three clips is fine. Each
  clip triggers its own extraction range, so measure before committing to a cut
  list with a few hundred of them — or use `overlay`.
