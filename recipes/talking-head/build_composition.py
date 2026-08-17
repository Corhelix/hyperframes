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

# Sentence-final punctuation ends a caption cue.
SENTENCE_END = (".", "!", "?", "…")

GSAP_CDN = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"


# ---------------------------------------------------------------------------
# Time handling
#
# Everything is quantised to the frame grid before any arithmetic. Clip
# boundaries must land exactly on frames: HyperFrames' overlapping_clips_
# same_track rule is a strict `current.end > next.start`, so accumulated
# float error of even 1e-9 across a few hundred clips turns into a lint
# error and a real one-frame seam in the render.
# ---------------------------------------------------------------------------


def to_frames(seconds: float, fps: int) -> int:
    return int(round(float(seconds) * fps))


def fmt_seconds(frames: int, fps: int) -> str:
    """Frame count -> a compact decimal string for an HTML attribute."""
    value = round(frames / fps, 6)
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return text or "0"


class Timeline:
    """Source <-> output time mapping built from the EDL keeps."""

    def __init__(self, keeps: list[dict], fps: int) -> None:
        self.fps = fps
        self.keeps: list[dict] = []
        cursor = 0
        for keep in keeps:
            sf_start = to_frames(keep["start"], fps)
            sf_end = to_frames(keep["end"], fps)
            if sf_end <= sf_start:
                continue
            length = sf_end - sf_start
            self.keeps.append(
                {
                    "sf_start": sf_start,
                    "sf_end": sf_end,
                    "of_start": cursor,
                    "of_end": cursor + length,
                    "frames": length,
                }
            )
            cursor += length
        self.total_frames = cursor

    def map_source(self, t: float) -> tuple[int, int] | None:
        """Source seconds -> (output frame, keep index), or None if cut."""
        frame = to_frames(t, self.fps)
        for index, keep in enumerate(self.keeps):
            if keep["sf_start"] <= frame < keep["sf_end"]:
                return keep["of_start"] + (frame - keep["sf_start"]), index
        return None

    def clamp_to_keep(self, t: float, index: int) -> int:
        """Source seconds -> output frame, clamped inside the given keep."""
        keep = self.keeps[index]
        frame = min(max(to_frames(t, self.fps), keep["sf_start"]), keep["sf_end"])
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
    fps = timeline.fps
    gap_frames = to_frames(gap_threshold, fps)

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
    fps = timeline.fps
    lines: list[str] = []
    for index, keep in enumerate(timeline.keeps):
        start = fmt_seconds(keep["of_start"], fps)
        duration = fmt_seconds(keep["frames"], fps)
        media_start = fmt_seconds(keep["sf_start"], fps)
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
    fps: int,
    timeline: Timeline,
    source: str,
    cues: list[dict],
    callouts: list[dict],
    title: str,
    subtitle: str,
    softener_frames: int,
) -> str:
    total = fmt_seconds(timeline.total_frames, fps)
    scope = f'[data-composition-id="{comp_id}"]'
    is_overlay = mode == "overlay"

    media_markup = "" if is_overlay else render_clips(timeline, source)
    dip_markup = "" if is_overlay else render_cut_softeners(timeline, softener_frames)

    # Cue and callout data are emitted as inline JSON. `var TRANSCRIPT = [...]`
    # with JSON-quoted keys is what the studio caption editor looks for, and
    # what the caption_transcript_not_inline rule expects.
    transcript_json = json.dumps(
        [
            {
                "text": cue["text"],
                "start": round(cue["start"] / fps, 3),
                "end": round(cue["end"] / fps, 3),
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
      var DIP = {round(softener_frames / fps, 3)};
      var CUT_POINTS = {json.dumps([round(k["of_start"] / fps, 3) for k in timeline.keeps[1:]])};
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
        bottom: 120px;
        height: 200px;
        z-index: 20;
        pointer-events: none;
      }}
      {scope} .caption-cue {{
        position: absolute;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        max-width: 1500px;
        margin: 0 auto;
        padding: 0 40px;
        text-align: center;
        font-size: 54px;
        font-weight: 700;
        line-height: 1.25;
        color: #fff;
        text-shadow: 0 3px 14px rgba(0, 0, 0, 0.72);
        opacity: 0;
        visibility: hidden;
      }}
      {scope} .lower-third {{
        position: absolute;
        left: 96px;
        bottom: 380px;
        z-index: 22;
        opacity: 0;
        visibility: hidden;
      }}
      {scope} .lower-third .lt-name {{
        font-size: 44px;
        font-weight: 700;
        color: #fff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
      }}
      {scope} .lower-third .lt-role {{
        margin-top: 8px;
        font-size: 28px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.82);
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
      }}
      {scope} .lower-third .lt-rule {{
        width: 132px;
        height: 5px;
        margin-bottom: 18px;
        border-radius: 3px;
        background: #4da3ff;
      }}
      {scope} .callout {{
        position: absolute;
        left: 96px;
        top: 140px;
        max-width: 760px;
        padding: 26px 32px;
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 18px;
        background: rgba(18, 32, 54, 0.55);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 18px 48px rgba(0, 0, 0, 0.38);
        font-size: 38px;
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

      <div class="lower-third" id="lower-third">
        <div class="lt-rule"></div>
        <div class="lt-name">{html.escape(title)}</div>
        <div class="lt-role">{html.escape(subtitle)}</div>
      </div>

      <script src="{GSAP_CDN}"></script>
      <script>
        window.__timelines = window.__timelines || {{}};

        // Caption cues on the OUTPUT timeline, already remapped through the
        // EDL. Inline and JSON-shaped so the studio caption editor can read
        // and rewrite them.
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

        // Lower third.
        var lowerThird = document.getElementById("lower-third");
        tl.set(lowerThird, {{ visibility: "visible" }}, 0.6);
        tl.fromTo(
          lowerThird,
          {{ opacity: 0, x: -40 }},
          {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }},
          0.6,
        );
        tl.to(lowerThird, {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, 5.2);
        tl.set(lowerThird, {{ opacity: 0, visibility: "hidden" }}, 5.6);

        // Callouts, authored on the output timeline.
        var stage = document.querySelector('[data-composition-id="{comp_id}"]');
        CALLOUTS.forEach(function (callout, index) {{
          var el = document.createElement("div");
          el.className = "callout";
          el.id = "callout-" + index;
          el.textContent = callout.text;
          if (callout.x !== undefined) el.style.left = callout.x + "px";
          if (callout.y !== undefined) el.style.top = callout.y + "px";
          if (callout.w !== undefined) el.style.maxWidth = callout.w + "px";
          if (callout.size !== undefined) el.style.fontSize = callout.size + "px";
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
    parser.add_argument("--transcript", required=True, type=Path)
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
    parser.add_argument("--fps", type=int)
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
    args = parser.parse_args()

    edl = load_json(args.edl)
    transcript = load_json(args.transcript)

    if isinstance(transcript, dict):
        words = transcript.get("words") or transcript.get("segments") or []
    else:
        words = transcript
    if not words:
        raise SystemExit(
            "Transcript is empty. Expected [{\"text\", \"start\", \"end\"}, ...] "
            "as written by `hyperframes transcribe`."
        )

    keeps = edl.get("keeps")
    if not keeps:
        raise SystemExit("EDL has no `keeps`. Nothing to build.")
    validate_keeps(keeps)

    fps = args.fps or int(edl.get("fps", 30))
    source = args.source or edl.get("source")
    if args.mode == "clips" and not source:
        raise SystemExit("clips mode needs a media source (--source or `source` in the EDL).")

    timeline = Timeline(keeps, fps)
    if timeline.total_frames <= 0:
        raise SystemExit("EDL keeps produced a zero-length timeline.")

    cues = build_cues(words, timeline, args.words_per_cue, args.min_words, args.gap)
    callouts = load_json(args.callouts) if args.callouts else []

    markup = build_html(
        mode=args.mode,
        comp_id=args.comp_id,
        width=args.width,
        height=args.height,
        fps=fps,
        timeline=timeline,
        source=source or "",
        cues=cues,
        callouts=callouts,
        title=args.title,
        subtitle=args.subtitle,
        softener_frames=to_frames(args.cut_softener, fps),
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markup, encoding="utf-8")

    source_frames = to_frames(max(float(k["end"]) for k in keeps), fps)
    removed = source_frames - timeline.total_frames
    print(f"Wrote {args.out}")
    print(f"  mode          {args.mode}")
    print(f"  clips         {len(timeline.keeps)}")
    print(
        f"  duration      {fmt_seconds(timeline.total_frames, fps)}s "
        f"({fmt_seconds(removed, fps)}s removed)"
    )
    print(f"  caption cues  {len(cues)}")
    print(f"  callouts      {len(callouts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
