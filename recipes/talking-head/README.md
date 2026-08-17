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
npx hyperframes render overlay --format webm -o overlay.webm
ffmpeg -i rough_cut.mp4 -i overlay.webm \
  -filter_complex "[0:v][1:v]overlay=format=auto" \
  -c:a copy final.mp4
```

**Use this for long-form.** The frame extractor pre-extracts every video clip
to JPEGs on disk at composition fps before compositing starts. A 20-minute
source at 30fps is ~36,000 1080p frames — order of 10–15 GB and a long pre-pass
(estimate, not measured) before a single output frame exists. In overlay mode
the source never enters the extractor.

## Package export — finished _and_ re-openable

`export_package.py` produces both outcomes from one job, so a video can ship as
is or be re-opened in DaVinci Resolve:

```bash
python3 export_package.py \
  --edl sample/edl.json \
  --transcript sample/transcript.json \
  --callouts sample/callouts.json \
  --source-file /abs/path/to/interview.mp4 \
  --out out/

out/build.sh          # runs the renders and transcodes
```

| Deliverable             | What it is                                                          |
| ----------------------- | ------------------------------------------------------------------- |
| `final.mp4`             | Full video — the cut with graphics baked in                         |
| `edit.fcpxml`           | **The same program as an editable timeline**                        |
| `rough_cut.mp4`         | The cut only, no graphics                                           |
| `edit.edl`              | CMX3600 conform list, cut only — fallback if the FCPXML is rejected |
| `captions.srt`          | Swap the caption layer for an editable subtitle track               |
| `graphics/*.mov`        | Every layer alone, ProRes 4444 with alpha                           |
| `graphics/overlay.mov`  | All graphics, flattened, full length                                |
| `graphics/stills/*.png` | Flat stills, for when a still places easier than a clip             |
| `manifest.json`         | Every clip and layer with its timecode and lane                     |

### The FCPXML is a finished program, not a conform

Open it and you get the whole output on one timeline — the cut, the captions,
the lower third and every callout, each on its own lane, in place. Render it and
the picture matches `final.mp4`. Nothing to assemble, nothing to import
separately:

```
lane 2   [lower third]     [callout 1]    [callout 2]    [callout 3]
lane 1   [────────────── captions ──────────────────────────────────]
spine    [── clip 1 ──][──── clip 2 ────][───── clip 3 ─────]  + audio
```

Every layer is a real rendered ProRes asset placed at its exact frame, so the
timeline is pixel-identical to the baked render **by construction** rather than
by approximation — the graphics are literally the same renders. From there any
single layer can be moved, retimed, restyled or deleted without rebuilding
anything.

**Import the FCPXML after `build.sh` finishes**, or the graphics come in
offline — the timeline references assets the build step creates.

**`--v1 source` (default) vs `--v1 roughcut`.** By default the spine cuts the
original recording with source in/out timecode, so shots keep handles and can be
extended — the way a real edit looks. `--v1 roughcut` instead lays down the
single flattened `rough_cut.mp4`: exactly the delivered cut, simpler to relink,
but no handles.

**ProRes MOV, not WebM, for anything going into Resolve.** Both carry alpha, but
`docs/guides/rendering.mdx:278` is explicit that WebM alpha shows as _black_ in
every editor. WebM is fine for the ffmpeg composite path above; it is wrong for
an NLE.

Captions ride the timeline as a rendered layer so the styling survives exactly.
`captions.srt` ships alongside for when you'd rather delete that layer and use
an editable subtitle track instead.

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
- **The FCPXML has not been opened in Resolve.** Its structure, spine
  continuity, and connected-clip offsets are verified by arithmetic, and the XML
  is well-formed 1.9 — but Resolve is fussy about `<format>` and asset
  declarations, and no one has confirmed it imports cleanly. Expect one round of
  fixes. `edit.edl` is the fallback: far simpler, and near-certain to conform.
- **Integer frame rates only.** 29.97 and 23.976 need drop-frame timecode, and a
  non-drop list conformed as drop-frame drifts ~3.6s per hour. The exporter
  refuses non-integer fps rather than emit a list that looks right and isn't.
- **Source start timecode is assumed `00:00:00:00`.** If your camera files carry
  real start TC, every event in the EDL and FCPXML shifts by that offset.
- **Nothing here has been rendered.** `build.sh` is syntax-checked and the
  commands match the current CLI, but this container has no ffmpeg and no
  network access to the GSAP CDN, so no render or transcode has been executed.
