#!/usr/bin/env python3
"""
Export a Resolve-ready package from a transcript + EDL + callouts.

Produces both a finished video and a finished TIMELINE:

  1. final.mp4        the full video -- cut with graphics baked in
  2. edit.fcpxml      the same program as an editable timeline: the cut,
                      the captions, the lower third and every callout, each
                      on its own lane, in place. Render it and you get the
                      same picture as final.mp4.
  3. rough_cut.mp4    the cut only, no graphics, for hand-finishing
  4. graphics/        every layer as its own transparent ProRes MOV, plus a
                      flattened full-length overlay and PNG stills

Plus captions.srt (swap the burned-in caption layer for an editable
subtitle track) and edit.edl (a CMX3600 conform list, cut only, as a
fallback if the FCPXML is rejected).

The FCPXML is a complete program, not a conform. Every visual layer is a
real rendered asset positioned on the timeline, so what an editor sees is
pixel-identical to the delivered render by construction -- they can then
move, retime, restyle or delete any single layer without rebuilding.

This script writes the *project files and the build script*. It does not
render or transcode -- run out/build.sh for that, on a machine with
ffmpeg and a working `hyperframes render`. Import the FCPXML AFTER
build.sh finishes, or the graphics come in offline.

Usage:
    python3 export_package.py \
        --edl sample/edl.json \
        --transcript sample/transcript.json \
        --callouts sample/callouts.json \
        --source-file /abs/path/to/source.mp4 \
        --out out/
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from build_composition import (
    LEAD,
    TAIL,
    Timeline,
    build_cues,
    fmt_float,
    load_json,
    to_frames,
    validate_keeps,
)
from mediainfo import (
    FCPXML_FIELD_ORDER,
    FrameRate,
    frames_to_tc,
    parse_rate,
    probe,
    tc_to_frames,
)

HERE = Path(__file__).resolve().parent

# What `hyperframes render` will accept (packages/cli/src/commands/render.ts).
SUPPORTED_RENDER_FPS = {24, 25, 30, 50, 60}


# ---------------------------------------------------------------------------
# Timecode
# ---------------------------------------------------------------------------


def timecode(frames: int, rate: FrameRate) -> str:
    """Frame count -> timecode, drop-frame or not according to the rate."""
    return frames_to_tc(frames, rate)


def srt_time(frames: int, rate: FrameRate) -> str:
    total_ms = int(round(rate.to_seconds(frames) * 1000))
    ms = total_ms % 1000
    total_seconds = total_ms // 1000
    return f"{total_seconds // 3600:02d}:{(total_seconds // 60) % 60:02d}:{total_seconds % 60:02d},{ms:03d}"


def rational(frames: int, rate: FrameRate) -> str:
    """FCPXML rational time.

    The denominator is the rate's timescale, so 29.97 emits 1001/30000s per
    frame and every time value stays exact. Writing 0.0333667s instead is
    how an NLE ends up a frame out over an hour.
    """
    if frames == 0:
        return "0s"
    return f"{frames * rate.den}/{rate.num}s"


# ---------------------------------------------------------------------------
# Graphic elements
# ---------------------------------------------------------------------------


def graphic_elements(
    callouts: list[dict],
    rate: FrameRate,
    lt_start: float,
    lt_dur: float,
    caption_frames: int = 0,
    render_rate: FrameRate | None = None,
) -> list[dict]:
    """Every layer that gets its own rendered asset, in timeline order.

    Captions are lane 1, graphics lane 2 -- matching the z-order inside the
    composition, where callouts and the lower third sit above captions.
    """
    # Placement uses the true rate; durations use the rate the asset is
    # actually rendered at. A frame COUNT is rate-independent, so the two stay
    # consistent on one timeline even when the render rate is the nominal
    # integer and the timeline is 29.97.
    render_rate = render_rate or rate
    elements: list[dict] = []
    if caption_frames > 0:
        elements.append(
            {
                "key": "captions",
                "slug": "captions",
                "name": "Captions",
                "only": "captions",
                "place_frames": 0,
                "duration_frames": caption_frames,
                "settled_frames": 0,
                "lane": 1,
            }
        )
    elements.append(
        {
            "key": "lower-third",
            "slug": "lower-third",
            "name": "Lower third",
            "only": "lower-third",
            "place_frames": to_frames(lt_start - LEAD, rate),
            "duration_frames": to_frames(LEAD + lt_dur + 0.4 + TAIL, render_rate),
            # The moment the graphic is fully on screen, used for the still.
            "settled_frames": to_frames(LEAD + 0.5, render_rate),
            "lane": 2,
        }
    )
    for index, callout in enumerate(callouts):
        elements.append(
            {
                "key": f"callout:{index}",
                "slug": f"callout-{index:02d}",
                "name": callout.get("text", f"Callout {index}")[:60],
                "only": f"callout:{index}",
                "place_frames": to_frames(float(callout["start"]) - LEAD, rate),
                "duration_frames": to_frames(LEAD + float(callout["dur"]) + 0.3 + TAIL, render_rate),
                "settled_frames": to_frames(LEAD + 0.45, render_rate),
                "lane": 2,
            }
        )
    elements.sort(key=lambda e: (e["lane"], e["place_frames"]))
    return elements


# ---------------------------------------------------------------------------
# SRT
# ---------------------------------------------------------------------------


def write_srt(path: Path, cues: list[dict], rate: FrameRate) -> None:
    blocks = []
    for index, cue in enumerate(cues, start=1):
        blocks.append(
            f"{index}\n"
            f"{srt_time(cue['start'], rate)} --> {srt_time(cue['end'], rate)}\n"
            f"{cue['text']}\n"
        )
    path.write_text("\n".join(blocks), encoding="utf-8")


# ---------------------------------------------------------------------------
# CMX3600 EDL
# ---------------------------------------------------------------------------


def write_edl(
    path: Path,
    timeline: Timeline,
    rate: FrameRate,
    title: str,
    reel: str,
    source_start_frames: int = 0,
    record_start_frames: int = 0,
) -> None:
    """CMX3600 conform list.

    Source timecode is offset by the file's own start TC, so the list lines
    up against the camera original rather than against a file that happens
    to begin at zero.
    """
    fcm = "DROP FRAME" if rate.drop else "NON-DROP FRAME"
    lines = [f"TITLE: {title}", f"FCM: {fcm}", ""]
    for index, keep in enumerate(timeline.keeps, start=1):
        src_in = source_start_frames + keep["sf_start"]
        src_out = source_start_frames + keep["sf_end"]
        rec_in = record_start_frames + keep["of_start"]
        rec_out = record_start_frames + keep["of_end"]
        lines.append(
            f"{index:03d}  {reel:<8} AA/V  C        "
            f"{timecode(src_in, rate)} {timecode(src_out, rate)} "
            f"{timecode(rec_in, rate)} {timecode(rec_out, rate)}"
        )
        lines.append(f"* FROM CLIP NAME: {title}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# FCPXML
# ---------------------------------------------------------------------------


def write_fcpxml(
    path: Path,
    *,
    timeline: Timeline,
    rate: FrameRate,
    width: int,
    height: int,
    source_file: Path,
    source_duration_frames: int,
    source_start_frames: int = 0,
    field_order: str = "progressive",
    record_start_frames: int = 0,
    elements: list[dict],
    graphics_dir: Path,
    project_name: str,
    v1: str = "source",
    rough_cut: Path | None = None,
) -> None:
    """Write a complete program: the cut plus every graphic layer, in place.

    Opening this and rendering must produce the same picture as final.mp4 --
    that is the whole point of shipping it. Every visual layer is a real
    transparent ProRes asset positioned on its own lane, so the timeline is
    pixel-identical to the baked render by construction rather than by
    approximation.

    v1="source"   spine references the ORIGINAL recording with source in/out,
                  so shots keep handles and can be extended.
    v1="roughcut" spine is a single flattened rough_cut.mp4. Simpler, matches
                  the delivered cut exactly, but no handles.
    """
    fcpxml = ET.Element("fcpxml", version="1.9")
    resources = ET.SubElement(fcpxml, "resources")

    # frameDuration carries the exact rational: 1001/30000s for 29.97, not a
    # rounded decimal. fieldOrder is set only for interlaced sources -- FCPXML
    # treats its absence as progressive.
    scan = "i" if field_order in FCPXML_FIELD_ORDER else "p"
    format_attrs = {
        "id": "r0",
        "name": f"FFVideoFormat{height}{scan}{rate.num / rate.den:g}".replace(".", ""),
        "frameDuration": f"{rate.den}/{rate.num}s",
        "width": str(width),
        "height": str(height),
        "colorSpace": "1-1-1 (Rec. 709)",
    }
    if field_order in FCPXML_FIELD_ORDER:
        format_attrs["fieldOrder"] = FCPXML_FIELD_ORDER[field_order]
    ET.SubElement(resources, "format", **format_attrs)

    tc_format = "DF" if rate.drop else "NDF"

    source_asset = ET.SubElement(
        resources,
        "asset",
        id="r1",
        name=source_file.stem,
        start=rational(source_start_frames, rate),
        duration=rational(source_duration_frames, rate),
        hasVideo="1",
        hasAudio="1",
        audioSources="1",
        audioChannels="2",
        format="r0",
    )
    ET.SubElement(
        source_asset,
        "media-rep",
        kind="original-media",
        src=source_file.resolve().as_uri(),
    )

    if v1 == "roughcut":
        rough_asset = ET.SubElement(
            resources,
            "asset",
            id="rRC",
            name="rough_cut",
            start="0s",
            duration=rational(timeline.total_frames, rate),
            hasVideo="1",
            hasAudio="1",
            audioSources="1",
            audioChannels="2",
            format="r0",
        )
        ET.SubElement(
            rough_asset,
            "media-rep",
            kind="original-media",
            src=(rough_cut or Path("rough_cut.mp4")).resolve().as_uri(),
        )

    for index, element in enumerate(elements):
        element["ref"] = f"r{index + 2}"
        asset = ET.SubElement(
            resources,
            "asset",
            id=element["ref"],
            name=element["slug"],
            start="0s",
            duration=rational(element["duration_frames"], rate),
            hasVideo="1",
            format="r0",
        )
        ET.SubElement(
            asset,
            "media-rep",
            kind="original-media",
            src=(graphics_dir / f"{element['slug']}.mov").resolve().as_uri(),
        )

    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name=project_name)
    project = ET.SubElement(event, "project", name=project_name)
    sequence = ET.SubElement(
        project,
        "sequence",
        format="r0",
        duration=rational(timeline.total_frames, rate),
        tcStart=rational(record_start_frames, rate),
        tcFormat=tc_format,
        audioLayout="stereo",
        audioRate="48k",
    )
    spine = ET.SubElement(sequence, "spine")

    spine_clips: list[tuple[ET.Element, int, int]] = []
    if v1 == "roughcut":
        clip = ET.SubElement(
            spine,
            "asset-clip",
            ref="rRC",
            name=f"{project_name} rough cut",
            offset="0s",
            start="0s",
            duration=rational(timeline.total_frames, rate),
            format="r0",
            tcFormat=tc_format,
        )
        # (element, its record-in on the sequence, its own `start` value)
        spine_clips.append((clip, 0, 0))
    else:
        for index, keep in enumerate(timeline.keeps, start=1):
            clip = ET.SubElement(
                spine,
                "asset-clip",
                ref="r1",
                name=f"{source_file.stem} {index}",
                offset=rational(keep["of_start"], rate),
                start=rational(source_start_frames + keep["sf_start"], rate),
                duration=rational(keep["frames"], rate),
                format="r0",
                tcFormat=tc_format,
            )
            spine_clips.append((clip, keep["of_start"], source_start_frames + keep["sf_start"]))

    # Every graphic layer rides as a connected clip. A connected clip's offset
    # is expressed in its PARENT's local time base -- measured from the parent's
    # `start`, not from the sequence origin. Getting this wrong is the usual
    # reason graphics land in the wrong place on import.
    #
    # Lane 1 is captions, lane 2 the graphics, matching the composition's
    # z-order. Together with the spine that is the complete program: render
    # this timeline and you get final.mp4.
    spine_ends = [
        (element, record_in, local_start) for element, record_in, local_start in spine_clips
    ]
    for element in elements:
        place = element["place_frames"]
        parent, record_in, local_start = spine_ends[0]
        for candidate, candidate_in, candidate_start in spine_ends:
            candidate_duration = int(candidate.get("duration").split("/")[0] or 0)
            if candidate_in <= place < candidate_in + candidate_duration:
                parent, record_in, local_start = candidate, candidate_in, candidate_start
                break
        else:
            parent, record_in, local_start = spine_ends[-1]

        ET.SubElement(
            parent,
            "asset-clip",
            ref=element["ref"],
            lane=str(element.get("lane", 1)),
            name=element["name"],
            offset=rational(local_start + (place - record_in), rate),
            start="0s",
            duration=rational(element["duration_frames"], rate),
            format="r0",
        )

    ET.indent(fcpxml, space="  ")
    body = ET.tostring(fcpxml, encoding="unicode")
    path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n' + body + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Build script
# ---------------------------------------------------------------------------


def write_build_script(
    path: Path,
    *,
    timeline: Timeline,
    rate: FrameRate,
    source_file: Path,
    elements: list[dict],
    recipe_dir: Path,
    out_dir: Path,
    deinterlace: bool = False,
    render_rate: FrameRate | None = None,
    ntsc: bool = False,
) -> None:
    # One decode, N trim filters, one concat -- not N re-opens of the same
    # file. The naive form (`-ss A -to B -i src` repeated per keep) opens a
    # decoder per segment and falls over on a long cut list.
    render_rate = render_rate or rate
    parts, labels = [], []
    for index, keep in enumerate(timeline.keeps):
        a = rate.to_seconds(keep["sf_start"])
        b = rate.to_seconds(keep["sf_end"])
        parts.append(f"[0:v]trim=start={a:.6f}:end={b:.6f},setpts=PTS-STARTPTS[v{index}]")
        parts.append(f"[0:a]atrim=start={a:.6f}:end={b:.6f},asetpts=PTS-STARTPTS[a{index}]")
        labels.append(f"[v{index}][a{index}]")
    filtergraph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(timeline.keeps)}:v=1:a=1[outv][outa]"

    lines = [
        "#!/usr/bin/env bash",
        "# Generated by export_package.py -- do not hand-edit, re-export instead.",
        "set -euo pipefail",
        "",
        f'RECIPE="{recipe_dir}"',
        f'OUT="{out_dir}"',
        f'SRC="{source_file}"',
        'mkdir -p "$OUT/graphics/stills"',
        "",
    ]
    if deinterlace:
        lines += [
            "# 0. Deinterlace to a progressive intermediate and cut from that.",
            "#    yadif mode=0 emits one frame per input frame, so the frame count",
            "#    and therefore every timecode in the EDL and FCPXML still hold.",
            'ffmpeg -y -i "$SRC" -vf yadif=mode=0 -c:v prores_ks -profile:v 3 \\',
            '  -c:a pcm_s16le "$OUT/source_progressive.mov"',
            'SRC="$OUT/source_progressive.mov"',
            "",
        ]
    lines += [
        "# 1. Rough cut -- the cut only, no graphics. Single decode.",
        'ffmpeg -y -i "$SRC" -filter_complex "' + filtergraph + '" \\',
        '  -map "[outv]" -map "[outa]" -c:v libx264 -crf 18 -preset medium \\',
        '  -c:a aac -b:a 192k "$OUT/rough_cut.mp4"',
        "",
    ]

    nominal = render_rate.num
    if ntsc:
        lines += [
            "# NTSC rates cannot be rendered directly -- the engine takes 24/30/60",
            f"# only. Graphics render at {nominal} and the timebase is re-stamped to",
            f"# {rate.num}/{rate.den} with -itsscale 1.001. Frame COUNT is preserved and",
            "# no pixels are resampled, so the assets stay frame-accurate.",
            "conform() {  # conform <file>",
            '  ffmpeg -y -itsscale 1.001 -i "$1" -c copy "${1%.mov}.ntsc.mov"',
            '  mv "${1%.mov}.ntsc.mov" "$1"',
            "}",
            "",
        ]
    else:
        lines += ["conform() { :; }  # integer rate, nothing to re-stamp", ""]

    if ntsc:
        lines += [
            "# 2. Full video is built last for NTSC -- see step 6. The footage must",
            "#    stay at its native rate, so it is composited with the overlay",
            "#    rather than re-rendered through the frame extractor.",
            "",
        ]
    else:
        lines += [
            "# 2. Full video -- cut plus graphics, baked.",
            "#    clips/media/source.mp4 must exist for this to render.",
            f'npx hyperframes render "$RECIPE/clips" --fps {nominal} -o "$OUT/final.mp4"',
            "",
        ]

    lines += [
        "# 3. Flattened graphics overlay, full length, alpha.",
        "#    ProRes 4444, not WebM: WebM alpha shows as black in Resolve.",
        f'npx hyperframes render "$RECIPE/overlay" --fps {nominal} --format mov '
        '-o "$OUT/graphics/overlay.mov"',
        'conform "$OUT/graphics/overlay.mov"',
        "",
        "# 4. Every layer as its own transparent asset. These are what the",
        "#    FCPXML timeline references -- render them before importing it.",
    ]
    for element in elements:
        slug = element["slug"]
        lines.append(
            f'npx hyperframes render "$RECIPE/gfx/{slug}" --fps {nominal} --format mov '
            f'-o "$OUT/graphics/{slug}.mov"'
        )
        lines.append(f'conform "$OUT/graphics/{slug}.mov"')
    lines += ["", "# 5. Flat PNG stills, for when a still is easier to place than a clip."]
    for element in elements:
        slug = element["slug"]
        at = rate.to_seconds(element["settled_frames"])
        lines.append(
            f'ffmpeg -y -ss {at:.3f} -i "$OUT/graphics/{slug}.mov" -frames:v 1 '
            f'"$OUT/graphics/stills/{slug}.png"'
        )
    if ntsc:
        lines += [
            "",
            "# 6. Full video: rough cut plus the conformed graphics overlay. Keeps",
            "#    the footage at its native rate and never resamples it.",
            'ffmpeg -y -i "$OUT/rough_cut.mp4" -i "$OUT/graphics/overlay.mov" \\',
            '  -filter_complex "[0:v][1:v]overlay=format=auto" \\',
            '  -map 0:a -c:a copy -c:v libx264 -crf 18 "$OUT/final.mp4"',
        ]
    lines += ["", 'echo "Package built in $OUT"', ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(0o755)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a Resolve-ready package.")
    parser.add_argument("--edl", required=True, type=Path)
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--callouts", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--source-file",
        required=True,
        type=Path,
        help="The ORIGINAL recording. The FCPXML and EDL point at this, not at the cut.",
    )
    parser.add_argument(
        "--source-duration",
        type=float,
        help="Source length in seconds. Defaults to the furthest point the EDL mentions.",
    )
    parser.add_argument("--fps", help="Override the probed rate: 25, 29.97, 30000/1001.")
    parser.add_argument(
        "--drop-frame",
        dest="drop_frame",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Force drop-frame timecode on or off. Defaults per rate.",
    )
    parser.add_argument("--start-tc", help="Override the probed source start timecode.")
    parser.add_argument(
        "--record-start-tc",
        default="00:00:00:00",
        help="Timeline start timecode. Many houses conform to 01:00:00:00.",
    )
    parser.add_argument(
        "--field-order",
        choices=("progressive", "tt", "bb", "tb", "bt"),
        help="Override the probed field order.",
    )
    parser.add_argument(
        "--deinterlace",
        action="store_true",
        help=(
            "Add a yadif prep pass to build.sh and cut from the progressive "
            "intermediate. Required for interlaced sources -- the render engine "
            "has no deinterlacer, so fields would come through combed."
        ),
    )
    parser.add_argument(
        "--no-probe",
        action="store_true",
        help="Skip ffprobe. Then --fps and the rest must be supplied explicitly.",
    )
    parser.add_argument(
        "--no-regenerate-comps",
        action="store_true",
        help="Leave clips/ and overlay/ alone. They must already match the source format.",
    )
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--words-per-cue", type=int, default=5)
    parser.add_argument("--min-words", type=int, default=3)
    parser.add_argument("--gap", type=float, default=0.35)
    parser.add_argument("--project-name", default="talking-head")
    parser.add_argument("--reel", default="AX", help="CMX3600 reel name, 8 chars max.")
    parser.add_argument(
        "--v1",
        choices=("source", "roughcut"),
        default="source",
        help=(
            "What the FCPXML spine references. `source` cuts the original recording "
            "so shots keep handles; `roughcut` lays down the flattened rough_cut.mp4."
        ),
    )
    parser.add_argument("--title", default="Andrew Cockburn")
    parser.add_argument("--subtitle", default="Wolf & Eagle")
    args = parser.parse_args()

    edl = load_json(args.edl)
    keeps = edl.get("keeps") or edl.get("ranges")
    if not keeps:
        raise SystemExit("EDL has no `keeps` (or `ranges`).")
    validate_keeps(keeps)

    # Read the format from the file rather than assuming it. Rate, start
    # timecode and field order all change the output, and all three are
    # routinely non-default: NTSC rates are fractional, camera masters carry a
    # real start TC, and broadcast sources are often interlaced.
    info = None
    if not args.no_probe:
        info = probe(args.source_file)

    if args.fps:
        rate = parse_rate(args.fps, drop=args.drop_frame)
    elif info is not None:
        rate = info.rate if args.drop_frame is None else parse_rate(
            f"{info.rate.num}/{info.rate.den}", drop=args.drop_frame
        )
    else:
        rate = parse_rate(edl.get("fps", 30), drop=args.drop_frame)

    # Graphics render at the rate's nominal integer. For PAL that IS the rate,
    # so nothing further is needed. For NTSC the timebase is re-stamped
    # afterwards with -itsscale 1.001, which is exact and resamples nothing.
    #
    # Retiming a 25p source to 30 was never an option worth offering: 1.2x is
    # not a clean pulldown, so it costs either duplicated frames or a 20% speed
    # change that drags audio pitch, every title and the whole ledger with it.
    render_rate = FrameRate(rate.nominal, 1)
    if rate.nominal not in SUPPORTED_RENDER_FPS:
        raise SystemExit(
            f"Frame rate {rate} cannot be rendered. `hyperframes render` accepts "
            f"{sorted(SUPPORTED_RENDER_FPS)}. Conform the source first, or pass "
            "--fps with a supported rate if you accept the retime."
        )
    ntsc = rate.den == 1001

    width = args.width or (info.width if info else 1920) or 1920
    height = args.height or (info.height if info else 1080) or 1080
    field_order = args.field_order or (info.field_order if info else "progressive")

    if args.start_tc:
        source_start_frames = tc_to_frames(args.start_tc, rate)
    elif info is not None and info.start_tc:
        source_start_frames = info.start_tc_frames
    else:
        source_start_frames = 0
    record_start_frames = tc_to_frames(args.record_start_tc, rate)

    interlaced = field_order in FCPXML_FIELD_ORDER
    if info is not None:
        print(f"Probed {args.source_file.name}:")
        print(f"  rate          {rate}")
        print(f"  scan          {field_order}")
        print(f"  size          {width}x{height}")
        print(f"  start TC      {info.start_tc or '(none, assuming 0)'}")
        if info.vfr:
            print(
                "  WARNING       variable frame rate detected. A VFR source cannot "
                "be conformed frame-accurately -- transcode to CFR first."
            )
    if interlaced and not args.deinterlace:
        print(
            f"  WARNING       source is interlaced ({field_order}) and --deinterlace "
            "was not passed.\n"
            "                The render engine has no deinterlacer, so graphics "
            "renders will comb.\n"
            "                Re-run with --deinterlace to add a yadif prep pass."
        )

    words: list[dict] = []
    if args.transcript:
        transcript = load_json(args.transcript)
        words = transcript if isinstance(transcript, list) else transcript.get("words", [])

    callouts = load_json(args.callouts) if args.callouts else []
    timeline = Timeline(keeps, rate)
    if timeline.total_frames <= 0:
        raise SystemExit("EDL keeps produced a zero-length timeline.")

    cues = build_cues(words, timeline, args.words_per_cue, args.min_words, args.gap) if words else []
    elements = graphic_elements(
        callouts,
        rate,
        lt_start=0.6,
        lt_dur=4.6,
        caption_frames=timeline.total_frames if cues else 0,
        render_rate=render_rate,
    )

    out = args.out.resolve()
    (out / "graphics" / "stills").mkdir(parents=True, exist_ok=True)
    gfx_root = HERE / "gfx"

    def build_comp(target: Path, extra: list[str]) -> None:
        """Generate one composition at the probed size and rate.

        Every composition in the package is built from the same probed
        numbers. Authoring clips/ and overlay/ by hand left them at the
        1920x1080/30 defaults, so a 4K 29.97 source produced 4K graphics
        assets and a 1080p30 programme -- a mismatch nothing would catch
        until the layers failed to line up.
        """
        cmd = [
            sys.executable,
            str(HERE / "build_composition.py"),
            "--edl", str(args.edl.resolve()),
            "--width", str(width),
            "--height", str(height),
            "--fps", str(render_rate.num),
            "--title", args.title,
            "--subtitle", args.subtitle,
            "--out", str(target),
            *extra,
        ]
        if args.callouts:
            cmd += ["--callouts", str(args.callouts.resolve())]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    caption_flags: list[str] = []
    if args.transcript:
        caption_flags = [
            "--transcript", str(args.transcript.resolve()),
            "--words-per-cue", str(args.words_per_cue),
            "--min-words", str(args.min_words),
            "--gap", str(args.gap),
        ]

    if not args.no_regenerate_comps:
        build_comp(
            HERE / "clips" / "index.html",
            ["--mode", "clips", "--comp-id", "talking-head", *caption_flags],
        )
        build_comp(
            HERE / "overlay" / "index.html",
            ["--mode", "overlay", "--comp-id", "talking-head-overlay", *caption_flags],
        )

    # One standalone composition per graphic, rendered later into its own
    # transparent asset.
    for element in elements:
        extra = ["--only", element["only"], "--comp-id", f"gfx-{element['slug']}"]
        if element["only"] == "captions":
            # The captions layer needs the transcript and the identical cue
            # grouping, or it renders empty or out of sync with final.mp4.
            if not args.transcript:
                raise SystemExit("A captions layer was requested but no --transcript was given.")
            extra += caption_flags
        build_comp(gfx_root / element["slug"] / "index.html", extra)

    if cues:
        write_srt(out / "captions.srt", cues, rate)
    write_edl(
        out / "edit.edl",
        timeline,
        rate,
        args.project_name,
        args.reel[:8],
        source_start_frames=source_start_frames,
        record_start_frames=record_start_frames,
    )

    # Prefer the real file length. Falling back to the EDL's extent caps the
    # asset at the last cut point, which silently removes the handles that are
    # the reason for referencing the original in the first place.
    edl_extent = max(
        [float(k["end"]) for k in keeps] + [float(c["end"]) for c in edl.get("cuts", [])]
    )
    if args.source_duration:
        source_duration_frames = to_frames(args.source_duration, rate)
    elif info is not None and info.duration:
        source_duration_frames = to_frames(info.duration, rate)
    else:
        source_duration_frames = to_frames(edl_extent, rate)
        print(
            "  NOTE          source length unknown, using the EDL's extent "
            f"({edl_extent}s). No handles past the last cut -- pass "
            "--source-duration or let ffprobe read the file."
        )

    write_fcpxml(
        out / "edit.fcpxml",
        timeline=timeline,
        rate=rate,
        width=width,
        height=height,
        source_file=args.source_file,
        source_duration_frames=source_duration_frames,
        elements=elements,
        graphics_dir=out / "graphics",
        project_name=args.project_name,
        v1=args.v1,
        rough_cut=out / "rough_cut.mp4",
        source_start_frames=source_start_frames,
        field_order=field_order,
        record_start_frames=record_start_frames,
    )

    manifest = {
        "project": args.project_name,
        "fps": f"{rate.num}/{rate.den}",
        "fpsDecimal": round(rate.num / rate.den, 4),
        "dropFrame": rate.drop,
        "fieldOrder": field_order,
        "interlaced": interlaced,
        "sourceStartTC": frames_to_tc(source_start_frames, rate),
        "recordStartTC": frames_to_tc(record_start_frames, rate),
        "resolution": [args.width, args.height],
        "timelineDuration": round(timeline.total_seconds, 3),
        "sourceFile": str(args.source_file),
        "sourceDuration": round(rate.to_seconds(source_duration_frames), 3),
        "deliverables": {
            "final.mp4": "Full video — cut with graphics baked in.",
            "rough_cut.mp4": "The cut only, no graphics.",
            "edit.fcpxml": (
                "Complete program: the cut plus every graphic layer in place. "
                "Render it and you get the same picture as final.mp4."
            ),
            "edit.edl": "CMX3600 conform list, cut only. Fallback if the FCPXML is rejected.",
            "captions.srt": "Import as a subtitle track.",
            "edit_ledger.json": (
                "Every removal and every word's source->output mapping. "
                "The audit trail for sync."
            ),
            "graphics/overlay.mov": "All graphics, full length, ProRes 4444 alpha.",
        },
        "cut": [
            {
                "index": index,
                "sourceIn": round(rate.to_seconds(keep["sf_start"]), 3),
                "sourceOut": round(rate.to_seconds(keep["sf_end"]), 3),
                "recordIn": round(rate.to_seconds(keep["of_start"]), 3),
                "recordOut": round(rate.to_seconds(keep["of_end"]), 3),
                "sourceInTC": timecode(source_start_frames + keep["sf_start"], rate),
                "recordInTC": timecode(record_start_frames + keep["of_start"], rate),
            }
            for index, keep in enumerate(timeline.keeps)
        ],
        "graphics": [
            {
                "slug": element["slug"],
                "name": element["name"],
                "clip": f"graphics/{element['slug']}.mov",
                "still": f"graphics/stills/{element['slug']}.png",
                "placeAt": round(rate.to_seconds(element["place_frames"]), 3),
                "placeAtTC": timecode(record_start_frames + element["place_frames"], rate),
                "duration": round(rate.to_seconds(element["duration_frames"]), 3),
                "lane": 1,
            }
            for element in elements
        ],
        "captions": [
            {
                "text": cue["text"],
                "start": round(rate.to_seconds(cue["start"]), 3),
                "end": round(rate.to_seconds(cue["end"]), 3),
            }
            for cue in cues
        ],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Edit ledger: every removal, and every surviving word's source -> output
    # mapping. Most recordings carry no timecode, so elapsed time from the head
    # of the file is the only shared reference between the transcript, the cut
    # and the delivered video. This file is that reference written down.
    #
    # Lip sync is preserved by construction, not by correction: picture and
    # audio are cut from the same source at the same frame boundaries, so a
    # word's mouth and its sound move together. The ledger is what lets you
    # PROVE that after the fact, and re-derive captions if the cut changes.
    ledger_words = []
    for word in words:
        text = str(word.get("text", "")).strip()
        if not text:
            continue
        mapped = timeline.map_source(float(word["start"]))
        if mapped is None:
            ledger_words.append(
                {
                    "text": text,
                    "sourceStart": round(float(word["start"]), 3),
                    "sourceEnd": round(float(word["end"]), 3),
                    "kept": False,
                }
            )
            continue
        out_frame, keep_index = mapped
        end_frame = timeline.clamp_to_keep(float(word["end"]), keep_index)
        ledger_words.append(
            {
                "text": text,
                "sourceStart": round(float(word["start"]), 3),
                "sourceEnd": round(float(word["end"]), 3),
                "outputStart": round(rate.to_seconds(out_frame), 3),
                "outputEnd": round(rate.to_seconds(end_frame), 3),
                "shift": round(
                    rate.to_seconds(out_frame) - float(word["start"]), 3
                ),
                "segment": keep_index,
                "kept": True,
            }
        )

    removed_frames = to_frames(edl_extent, rate) - timeline.total_frames
    ledger = {
        "reference": (
            "Elapsed seconds from the first frame of the source file. Source "
            "timecode is recorded when the file carries it, but nothing depends "
            "on it -- these timings hold for any recording."
        ),
        "rate": f"{rate.num}/{rate.den}",
        "sourceStartTC": frames_to_tc(source_start_frames, rate)
        if source_start_frames
        else None,
        "totals": {
            "sourceDuration": round(rate.to_seconds(source_duration_frames), 3),
            "outputDuration": round(timeline.total_seconds, 3),
            "removedDuration": round(rate.to_seconds(removed_frames), 3),
            "segments": len(timeline.keeps),
            "wordsKept": sum(1 for w in ledger_words if w["kept"]),
            "wordsRemoved": sum(1 for w in ledger_words if not w["kept"]),
        },
        "segments": [
            {
                "index": index,
                "sourceIn": round(rate.to_seconds(keep["sf_start"]), 3),
                "sourceOut": round(rate.to_seconds(keep["sf_end"]), 3),
                "outputIn": round(rate.to_seconds(keep["of_start"]), 3),
                "outputOut": round(rate.to_seconds(keep["of_end"]), 3),
                "frames": keep["frames"],
                # How far this segment slides earlier once the cuts ahead of it
                # are removed. Add it to any source time to get output time.
                "shift": round(
                    rate.to_seconds(keep["of_start"] - keep["sf_start"]), 3
                ),
            }
            for index, keep in enumerate(timeline.keeps)
        ],
        "removals": [
            {
                "sourceIn": round(float(cut["start"]), 3),
                "sourceOut": round(float(cut["end"]), 3),
                "duration": round(float(cut["end"]) - float(cut["start"]), 3),
                "reason": cut.get("reason", "unspecified"),
            }
            for cut in edl.get("cuts", [])
        ],
        "words": ledger_words,
    }
    (out / "edit_ledger.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )

    write_build_script(
        out / "build.sh",
        timeline=timeline,
        rate=rate,
        source_file=args.source_file,
        elements=elements,
        recipe_dir=HERE,
        out_dir=out,
        deinterlace=args.deinterlace,
        render_rate=render_rate,
        ntsc=ntsc,
    )

    print(f"Package scaffolded in {out}")
    print(f"  timeline      {fmt_float(timeline.total_seconds)}s, {len(timeline.keeps)} clips")
    print(f"  graphics      {len(elements)} assets → {gfx_root}")
    print(f"  captions      {len(cues)} cues")
    print(f"  ledger        {len(ledger_words)} words mapped source -> output")
    print(f"  format        {width}x{height} @ {rate}, rendering at {render_rate.num}")
    print(f"  next          {out / 'build.sh'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
