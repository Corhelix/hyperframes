#!/usr/bin/env python3
"""
EDL -> HyperFrames composition generator.

Takes a word-level transcript and an edit decision list and emits an
index.html that satisfies the HyperFrames composition contract (see
skills/hyperframes/SKILL.md) and passes `hyperframes lint`.

Two output modes:

  clips    The EDL is expressed natively as sequential <video>/<audio> clip
           pairs trimmed with data-media-start. One render, no ffmpeg
           pre-cut, no drift between the cut and the caption timeline.
           The engine only extracts frames for kept ranges, so removed
           footage never reaches the frame extractor.

  overlay  Graphics only, transparent background, timed against an
           already-cut rough_cut.mp4. Render with --format webm and
           composite with a single ffmpeg pass. Use this for long-form:
           the source video never enters the frame extractor at all.

Usage:
    python3 build_composition.py \
        --edl sample/edl.json \
        --transcript sample/transcript.json \
        --callouts sample/callouts.json \
        --mode clips \
        --out clips/index.html

Time bases:
    transcript.json  source timeline (raw recording)
    edl.json         source timeline (raw recording)
    callouts.json    OUTPUT timeline (after cuts) -- same convention as
                     the long-form-shorts-engine callouts-sop.json, since
                     callouts are authored once you can see the cut.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

from mediainfo import FrameRate, parse_rate

# Sentence-final punctuation ends a caption cue.
SENTENCE_END = (".", "!", "?", "…")

GSAP_CDN = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"

# --only assets: a short lead-in before the graphic animates, and a tail after
# it clears, so the rendered file contains the whole animation with a little
# slack at each end for the editor to trim into.
LEAD = 0.1
TAIL = 0.2


# ---------------------------------------------------------------------------
# Time handling
#
# Everything is quantised to the frame grid before any arithmetic. Clip
# boundaries must land exactly on frames: HyperFrames' overlapping_clips_
# same_track rule is a strict `current.end > next.start`, so accumulated
# float error of even 1e-9 across a few hundred clips turns into a lint
# error and a real one-frame seam in the render.
# ---------------------------------------------------------------------------


def to_frames(seconds: float, rate: FrameRate) -> int:
    return rate.to_frames(seconds)


def fmt_float(value: float) -> str:
    """Shortest decimal that reparses to the identical double.

    Not a fixed number of places. At 29.97 a frame boundary is
    1001/30000s, which does not terminate in decimal, so rounding each
    clip's start and duration independently lets `start + duration` land a
    hair past the next clip's start -- and overlapping_clips_same_track is
    a strict `end > start`. Emitting the exact doubles this script already
    accumulated keeps the arithmetic identical on both sides.
    """
    text = repr(float(value))
    return text[:-2] if text.endswith(".0") else text


def fmt_seconds(frames: int, rate: FrameRate) -> str:
    """Frame count -> a decimal string for an HTML attribute."""
    return fmt_float(rate.to_seconds(frames))


class Timeline:
    """Source <-> output time mapping built from the EDL keeps."""

    def __init__(self, keeps: list[dict], rate: FrameRate) -> None:
        self.rate = rate
        self.keeps: list[dict] = []
        cursor = 0
        # Seconds are accumulated alongside the frame counts, not derived from
        # them afterwards, so each clip's start is literally the previous
        # start plus the previous duration in float arithmetic.
        cursor_seconds = 0.0
        for keep in keeps:
            sf_start = to_frames(keep["start"], rate)
            sf_end = to_frames(keep["end"], rate)
            if sf_end <= sf_start:
                continue
            length = sf_end - sf_start
            duration_seconds = rate.to_seconds(length)
            self.keeps.append(
                {
                    "sf_start": sf_start,
                    "sf_end": sf_end,
                    "of_start": cursor,
                    "of_end": cursor + length,
                    "frames": length,
                    "start_s": cursor_seconds,
                    "dur_s": duration_seconds,
                }
            )
            cursor += length
            cursor_seconds += duration_seconds
        self.total_frames = cursor
        self.total_seconds = cursor_seconds

    def map_source(self, t: float) -> tuple[int, int] | None:
        """Source seconds -> (output frame, keep index), or None if cut."""
        frame = to_frames(t, self.rate)
        for index, keep in enumerate(self.keeps):
            if keep["sf_start"] <= frame < keep["sf_end"]:
                return keep["of_start"] + (frame - keep["sf_start"]), index
        return None

    def clamp_to_keep(self, t: float, index: int) -> int:
        """Source seconds -> output frame, clamped inside the given keep."""
        keep = self.keeps[index]
        frame = min(max(to_frames(t, self.rate), keep["sf_start"]), keep["sf_end"])
        return keep["of_start"] + (frame - keep["sf_start"])


def validate_keeps(keeps: list[dict]) -> None:
    ordered = sorted(keeps, key=lambda k: float(k["start"]))
    for previous, current in zip(ordered, ordered[1:]):
        if float(previous["end"]) > float(current["start"]):
            raise SystemExit(
                f"EDL error: keep ending at {previous['end']}s overlaps the keep "
                f"starting at {current['start']}s. Keeps must be disjoint."
            )


# ---------------------------------------------------------------------------
# Captions
# ---------------------------------------------------------------------------


def build_cues(
    words: list[dict],
    timeline: Timeline,
    words_per_cue: int,
    min_words: int,
    gap_threshold: float,
) -> list[dict]:
    """Group surviving words into caption cues on the output timeline.

    A cue never spans a cut. A cue that did would inherit the removed
    footage's duration and drift out of sync with the audio for the rest
    of the video -- the single most common failure when captions are
    built from a de-timestamped "polished script" instead of from the
    transcript and the EDL together.
    """
    rate = timeline.rate
    gap_frames = to_frames(gap_threshold, rate)

    cues: list[dict] = []
    current: dict | None = None

    for word in words:
        text = str(word.get("text", "")).strip()
        if not text:
            continue
        mapped = timeline.map_source(word["start"])
        if mapped is None:
            continue  # word fell inside a cut
        out_start, keep_index = mapped
        out_end = timeline.clamp_to_keep(word["end"], keep_index)
        if out_end <= out_start:
            out_end = out_start + 1

        should_break = (
            current is None
            or current["keep_index"] != keep_index
            or len(current["words"]) >= words_per_cue
            or current["ended_sentence"]
            or out_start - current["end"] > gap_frames
        )

        if should_break:
            if current is not None:
                cues.append(current)
            current = {
                "words": [text],
                "start": out_start,
                "end": out_end,
                "keep_index": keep_index,
                "ended_sentence": text.endswith(SENTENCE_END),
            }
        else:
            current["words"].append(text)
            current["end"] = out_end
            current["ended_sentence"] = text.endswith(SENTENCE_END)

    if current is not None:
        cues.append(current)

    # Merge any cue left below the minimum word count into its neighbour,
    # as long as that neighbour is inside the same keep.
    merged: list[dict] = []
    for cue in cues:
        if (
            merged
            and len(cue["words"]) < min_words
            and merged[-1]["keep_index"] == cue["keep_index"]
        ):
            merged[-1]["words"].extend(cue["words"])
            merged[-1]["end"] = cue["end"]
        else:
            merged.append(cue)

    return [
        {
            "text": " ".join(cue["words"]),
            "start": cue["start"],
            "end": cue["end"],
        }
        for cue in merged
    ]


# ---------------------------------------------------------------------------
# HTML emission
# ---------------------------------------------------------------------------


def render_clips(timeline: Timeline, source: str) -> str:
    """Sequential video/audio clip pairs expressing the EDL.

    Video is muted on track 0; audio is a separate element on track 1
    pointing at the same file. This is not stylistic -- the producer's
    audio extractor only matches media elements that carry data-start
    (packages/producer/src/services/audioExtractor.ts), and the linter
    errors on a <video> with data-start that is not muted.
    """
    rate = timeline.rate
    lines: list[str] = []
    for index, keep in enumerate(timeline.keeps):
        start = fmt_float(keep["start_s"])
        duration = fmt_float(keep["dur_s"])
        media_start = fmt_seconds(keep["sf_start"], rate)
        lines.append(
            f'      <video id="clip-v-{index}" src="{html.escape(source)}" '
            f'data-start="{start}" data-duration="{duration}" '
            f'data-media-start="{media_start}" data-track-index="0" '
            f"muted playsinline></video>"
        )
        lines.append(
            f'      <audio id="clip-a-{index}" src="{html.escape(source)}" '
            f'data-start="{start}" data-duration="{duration}" '
            f'data-media-start="{media_start}" data-track-index="1" '
            f'data-volume="1"></audio>'
        )
    return "\n".join(lines)


def render_cut_softeners(timeline: Timeline, softener_frames: int) -> str:
    """One dip overlay per interior cut.

    A true cross-dissolve between two clips is not available: it needs
    overlapping clips on one track (overlapping_clips_same_track, error)
    or an opacity tween on a clip element (gsap_animates_clip_element,
    error) -- the framework owns clip visibility. A short dip on a
    non-clip overlay div is the framework-compatible way to take the edge
    off a hard cut on a talking head.
    """
    if softener_frames <= 0 or len(timeline.keeps) < 2:
        return ""
    lines: list[str] = []
    for index in range(1, len(timeline.keeps)):
        lines.append(f'      <div class="cut-dip" id="cut-dip-{index}"></div>')
    return "\n".join(lines)


def build_html(
    *,
    mode: str,
    comp_id: str,
    width: int,
    height: int,
    rate: FrameRate,
    timeline: Timeline,
    source: str,
    cues: list[dict],
    callouts: list[dict],
    title: str,
    subtitle: str,
    softener_frames: int,
    lt_start: float = 0.6,
    lt_dur: float = 4.6,
    show_lower_third: bool = True,
    duration_override: float | None = None,
) -> str:
    total = (
        fmt_seconds(to_frames(duration_override, rate), rate)
        if duration_override is not None
        else fmt_float(timeline.total_seconds)
    )
    scope = f'[data-composition-id="{comp_id}"]'

    # Type and spacing below are authored in 1080-space pixels. Matching the
    # source frame size only helps if the graphics scale with it -- a 54px
    # caption on a 2160-tall canvas is half the size it looks at 1080.
    scale = height / 1080

    def px(value: float) -> int:
        return max(1, round(value * scale))
    is_overlay = mode == "overlay"

    media_markup = "" if is_overlay else render_clips(timeline, source)
    dip_markup = "" if is_overlay else render_cut_softeners(timeline, softener_frames)

    lower_third_markup = (
        f"""      <div class="lower-third" id="lower-third">
        <div class="lt-rule"></div>
        <div class="lt-name">{html.escape(title)}</div>
        <div class="lt-role">{html.escape(subtitle)}</div>
      </div>"""
        if show_lower_third
        else ""
    )

    lt_out = round(lt_start + lt_dur, 3)
    lower_third_js = (
        f"""
        // Lower third.
        var lowerThird = document.getElementById("lower-third");
        tl.set(lowerThird, {{ visibility: "visible" }}, {lt_start});
        tl.fromTo(
          lowerThird,
          {{ opacity: 0, x: -40 }},
          {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }},
          {lt_start},
        );
        tl.to(lowerThird, {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, {lt_out});
        tl.set(lowerThird, {{ opacity: 0, visibility: "hidden" }}, {round(lt_out + 0.4, 3)});"""
        if show_lower_third
        else ""
    )

    # Cue and callout data are emitted as inline JSON. `var TRANSCRIPT = [...]`
    # with JSON-quoted keys is what the studio caption editor looks for, and
    # what the caption_transcript_not_inline rule expects.
    transcript_json = json.dumps(
        [
            {
                "text": cue["text"],
                "start": round(rate.to_seconds(cue["start"]), 3),
                "end": round(rate.to_seconds(cue["end"]), 3),
            }
            for cue in cues
        ],
        indent=2,
    )
    callouts_json = json.dumps(callouts, indent=2)

    stage_bg = "transparent" if is_overlay else "#000"
    body_bg = "transparent" if is_overlay else "#000"

    dip_css = (
        ""
        if is_overlay
        else f"""
      {scope} .cut-dip {{
        position: absolute;
        inset: 0;
        background: #000;
        opacity: 0;
        pointer-events: none;
        z-index: 5;
      }}"""
    )

    dip_js = (
        ""
        if is_overlay or softener_frames <= 0 or len(timeline.keeps) < 2
        else f"""
      // Cut softeners: a short dip at each interior cut point.
      var DIP = {round(rate.to_seconds(softener_frames), 3)};
      var CUT_POINTS = {json.dumps([round(k["start_s"], 3) for k in timeline.keeps[1:]])};
      CUT_POINTS.forEach(function (at, i) {{
        var dip = document.getElementById("cut-dip-" + (i + 1));
        if (!dip) return;
        tl.to(dip, {{ opacity: 0.85, duration: DIP / 2, ease: "power1.in" }}, at - DIP / 2);
        tl.to(dip, {{ opacity: 0, duration: DIP / 2, ease: "power1.out" }}, at);
        tl.set(dip, {{ opacity: 0 }}, at + DIP / 2);
      }});"""
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{html.escape(title)}</title>
    <style>
      html,
      body {{
        margin: 0;
        padding: 0;
        background: {body_bg};
      }}
      {scope} {{
        position: relative;
        width: {width}px;
        height: {height}px;
        overflow: hidden;
        background: {stage_bg};
        font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
      }}
      {scope} video {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }}
      {scope} .caption-layer {{
        position: absolute;
        left: 0;
        right: 0;
        bottom: {px(120)}px;
        height: {px(200)}px;
        z-index: 20;
        pointer-events: none;
      }}
      {scope} .caption-cue {{
        position: absolute;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        max-width: {px(1500)}px;
        margin: 0 auto;
        padding: 0 {px(40)}px;
        text-align: center;
        font-size: {px(54)}px;
        font-weight: 700;
        line-height: 1.25;
        color: #fff;
        text-shadow: 0 {px(3)}px {px(14)}px rgba(0, 0, 0, 0.72);
        opacity: 0;
        visibility: hidden;
      }}
      {scope} .lower-third {{
        position: absolute;
        left: {px(96)}px;
        bottom: {px(380)}px;
        z-index: 22;
        opacity: 0;
        visibility: hidden;
      }}
      {scope} .lower-third .lt-name {{
        font-size: {px(44)}px;
        font-weight: 700;
        color: #fff;
        text-shadow: 0 {px(2)}px {px(10)}px rgba(0, 0, 0, 0.6);
      }}
      {scope} .lower-third .lt-role {{
        margin-top: {px(8)}px;
        font-size: {px(28)}px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.82);
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
      }}
      {scope} .lower-third .lt-rule {{
        width: {px(132)}px;
        height: {px(5)}px;
        margin-bottom: {px(18)}px;
        border-radius: {px(3)}px;
        background: #4da3ff;
      }}
      {scope} .callout {{
        position: absolute;
        left: {px(96)}px;
        top: {px(140)}px;
        max-width: {px(760)}px;
        padding: {px(26)}px {px(32)}px;
        border: {px(1)}px solid rgba(255, 255, 255, 0.28);
        border-radius: {px(18)}px;
        background: rgba(18, 32, 54, 0.55);
        backdrop-filter: blur({px(18)}px);
        -webkit-backdrop-filter: blur({px(18)}px);
        box-shadow: 0 {px(18)}px {px(48)}px rgba(0, 0, 0, 0.38);
        font-size: {px(38)}px;
        font-weight: 600;
        line-height: 1.3;
        color: #fff;
        z-index: 21;
        opacity: 0;
        visibility: hidden;
      }}{dip_css}
    </style>
  </head>
  <body>
    <div
      data-composition-id="{comp_id}"
      data-start="0"
      data-duration="{total}"
      data-width="{width}"
      data-height="{height}"
    >
{media_markup}
{dip_markup}
      <div class="caption-layer" id="caption-layer"></div>

{lower_third_markup}

      <script src="{GSAP_CDN}"></script>
      <script>
        window.__timelines = window.__timelines || {{}};

        // Caption cues on the OUTPUT timeline, already remapped through the
        // EDL. Inline and JSON-shaped so the studio caption editor can read
        // and rewrite them.
        //
        // Declared with `var`, deliberately. `hyperframes transcribe` runs
        // patchCaptionHtml(), which walks every .html under the project and
        // overwrites a const-declared TRANSCRIPT with raw source-timeline
        // words. On this composition that would be wrong twice over: the
        // words are on the source timeline, and they include everything the
        // EDL cut. The patcher's regex only matches `const`, so `var` opts
        // out while staying readable to the studio caption editor.
        //
        // Do not write the const form literally anywhere in this file, not
        // even in a comment: the studio's detector regex scans for the first
        // occurrence and would capture from the comment to the real array,
        // yielding a span that is not valid JSON.
        var TRANSCRIPT = {transcript_json};

        var CALLOUTS = {callouts_json};

        var COMP_DURATION = {total};

        var tl = gsap.timeline({{ paused: true }});

        // Captions. Built synchronously at load -- the capture engine reads
        // window.__timelines immediately after load, so nothing here may be
        // deferred into a promise or a timeout.
        var captionLayer = document.getElementById("caption-layer");
        var FADE = 0.12;
        TRANSCRIPT.forEach(function (cue, index) {{
          var el = document.createElement("div");
          el.className = "caption-cue";
          el.textContent = cue.text;
          captionLayer.appendChild(el);

          // Hold until the cue's own end, but never past the moment the next
          // cue appears. Cues stack at the same screen position, so an
          // unbounded fade would ghost two lines over each other.
          var next = TRANSCRIPT[index + 1];
          var holdUntil = Math.max(cue.end, cue.start + 0.4);
          if (next) {{
            holdUntil = Math.min(holdUntil, next.start - FADE);
            holdUntil = Math.max(holdUntil, cue.start + 0.1);
          }}
          var fade = next ? Math.max(Math.min(next.start - holdUntil, FADE), 0.04) : FADE;

          tl.set(el, {{ visibility: "visible" }}, cue.start);
          tl.fromTo(
            el,
            {{ opacity: 0, y: 14 }},
            {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }},
            cue.start,
          );
          tl.to(el, {{ opacity: 0, duration: fade, ease: "power1.in" }}, holdUntil);
          // Deterministic kill. Exit tweens on captions can be left half-applied
          // when neighbouring cues overlap; the hard set guarantees the cue is
          // gone on every seek.
          tl.set(el, {{ opacity: 0, visibility: "hidden" }}, holdUntil + fade);
        }});

{lower_third_js}

        // Callouts, authored on the output timeline.
        var stage = document.querySelector('[data-composition-id="{comp_id}"]');
        // Callout geometry in the JSON is authored in 1080-space, same as the
        // stylesheet, so it scales by the same factor.
        var GFX_SCALE = {scale!r};
        CALLOUTS.forEach(function (callout, index) {{
          var el = document.createElement("div");
          el.className = "callout";
          el.id = "callout-" + index;
          el.textContent = callout.text;
          if (callout.x !== undefined) el.style.left = callout.x * GFX_SCALE + "px";
          if (callout.y !== undefined) el.style.top = callout.y * GFX_SCALE + "px";
          if (callout.w !== undefined) el.style.maxWidth = callout.w * GFX_SCALE + "px";
          if (callout.size !== undefined) el.style.fontSize = callout.size * GFX_SCALE + "px";
          stage.appendChild(el);

          var out = callout.start + callout.dur;
          tl.set(el, {{ visibility: "visible" }}, callout.start);
          tl.fromTo(
            el,
            {{ opacity: 0, y: 24, scale: 0.97 }},
            {{ opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }},
            callout.start,
          );
          tl.to(el, {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, out);
          tl.set(el, {{ opacity: 0, visibility: "hidden" }}, out + 0.3);
        }});{dip_js}

        window.__timelines["{comp_id}"] = tl;
      </script>
    </div>
  </body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def load_json(path: Path):
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")
    except json.JSONDecodeError as err:
        raise SystemExit(f"Invalid JSON in {path}: {err}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a HyperFrames composition from a transcript and an EDL.",
    )
    parser.add_argument("--edl", required=True, type=Path)
    parser.add_argument(
        "--transcript",
        type=Path,
        help="Word-level transcript. Omit to build the cut and callouts with no captions.",
    )
    parser.add_argument("--callouts", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mode", choices=("clips", "overlay"), default="clips")
    parser.add_argument(
        "--source",
        help="Media src, relative to the composition dir. Defaults to the EDL's `source`.",
    )
    parser.add_argument("--comp-id", default="talking-head")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument(
        "--fps",
        help="Frame rate: 25, 29.97, 30000/1001. Defaults to the EDL's `fps`.",
    )
    parser.add_argument(
        "--drop-frame",
        dest="drop_frame",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Force drop-frame timecode on or off. Defaults per rate (on for 29.97/59.94).",
    )
    parser.add_argument("--words-per-cue", type=int, default=5)
    parser.add_argument("--min-words", type=int, default=3)
    parser.add_argument(
        "--gap",
        type=float,
        default=0.35,
        help="Seconds of silence that forces a new caption cue.",
    )
    parser.add_argument(
        "--cut-softener",
        type=float,
        default=0.12,
        help="Seconds of dip at each interior cut. 0 disables.",
    )
    parser.add_argument("--title", default="Andrew Cockburn")
    parser.add_argument("--subtitle", default="Wolf & Eagle")
    parser.add_argument(
        "--only",
        help=(
            "Emit one graphic on its own, rebased to start at 0.1s, for rendering "
            "as a standalone transparent asset. `lower-third` or `callout:N`."
        ),
    )
    args = parser.parse_args()

    edl = load_json(args.edl)

    # Timestamp extraction is not done here. `hyperframes transcribe <file>`
    # already writes transcript.json in exactly this shape -- it manages the
    # whisper.cpp binary, model download, language selection, SRT/VTT/OpenAI
    # import and speech-onset stripping. Re-implementing that in Python would
    # be a second, worse copy.
    words: list[dict] = []
    if args.transcript:
        transcript = load_json(args.transcript)
        if isinstance(transcript, dict):
            words = transcript.get("words") or transcript.get("segments") or []
        else:
            words = transcript
        if not words:
            raise SystemExit(
                'Transcript is empty. Expected [{"text", "start", "end"}, ...] '
                "as written by `hyperframes transcribe`."
            )

    # `keeps` is this recipe's name; `ranges` is what the long-form-shorts-engine
    # tools (whisper_transcribe.py, make_captions.py) write. Same meaning, so
    # accept either and the two toolchains can share one EDL file.
    keeps = edl.get("keeps") or edl.get("ranges")
    if not keeps:
        raise SystemExit("EDL has no `keeps` (or `ranges`). Nothing to build.")
    validate_keeps(keeps)

    rate = parse_rate(args.fps or edl.get("fps", 30), drop=args.drop_frame)
    source = args.source or edl.get("source")
    if args.mode == "clips" and not source:
        raise SystemExit("clips mode needs a media source (--source or `source` in the EDL).")

    timeline = Timeline(keeps, rate)
    if timeline.total_frames <= 0:
        raise SystemExit("EDL keeps produced a zero-length timeline.")

    cues = build_cues(words, timeline, args.words_per_cue, args.min_words, args.gap)
    callouts = load_json(args.callouts) if args.callouts else []

    mode = args.mode
    lt_start, lt_dur, show_lower_third = 0.6, 4.6, True
    duration_override: float | None = None
    place_at_frames = 0

    if args.only:
        # One layer, alone, so it can be rendered as a standalone transparent
        # asset and placed on its own lane in an NLE. `place_at_frames` records
        # where it belongs on the output timeline.
        mode = "overlay"
        if args.only == "captions":
            # Captions keep their real output-timeline times and run the full
            # length, so the asset drops onto the timeline at 00:00.
            callouts = []
            show_lower_third = False
            duration_override = timeline.total_seconds
        elif args.only == "lower-third":
            # Single graphics rebase to LEAD so the rendered file starts almost
            # immediately rather than carrying dead frames at the head.
            cues = []
            callouts = []
            lt_start, lt_dur = LEAD, 4.6
            duration_override = LEAD + lt_dur + 0.4 + TAIL
            place_at_frames = to_frames(0.6 - LEAD, rate)
        elif args.only.startswith("callout:"):
            cues = []
            index = int(args.only.split(":", 1)[1])
            if index < 0 or index >= len(callouts):
                raise SystemExit(f"--only {args.only}: no such callout (have {len(callouts)}).")
            original_start = float(callouts[index]["start"])
            chosen = dict(callouts[index])
            chosen["start"] = LEAD
            callouts = [chosen]
            show_lower_third = False
            duration_override = LEAD + float(chosen["dur"]) + 0.3 + TAIL
            place_at_frames = to_frames(original_start - LEAD, rate)
        else:
            raise SystemExit("--only takes `captions`, `lower-third`, or `callout:N`.")

    markup = build_html(
        mode=mode,
        comp_id=args.comp_id,
        width=args.width,
        height=args.height,
        rate=rate,
        timeline=timeline,
        source=source or "",
        cues=cues,
        callouts=callouts,
        title=args.title,
        subtitle=args.subtitle,
        softener_frames=to_frames(args.cut_softener, rate),
        lt_start=lt_start,
        lt_dur=lt_dur,
        show_lower_third=show_lower_third,
        duration_override=duration_override,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markup, encoding="utf-8")

    print(f"Wrote {args.out}")
    if args.only:
        print(f"  mode          {mode} (--only {args.only})")
        print(f"  duration      {fmt_seconds(to_frames(duration_override, rate), rate)}s")
        print(f"  place at      {fmt_seconds(place_at_frames, rate)}s on the output timeline")
        return 0

    source_frames = to_frames(max(float(k["end"]) for k in keeps), rate)
    removed = source_frames - timeline.total_frames
    print(f"  mode          {mode}")
    print(f"  rate          {rate}")
    print(f"  clips         {len(timeline.keeps)}")
    print(
        f"  duration      {fmt_float(timeline.total_seconds)}s "
        f"({fmt_seconds(removed, rate)}s removed)"
    )
    print(f"  caption cues  {len(cues)}")
    print(f"  callouts      {len(callouts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
