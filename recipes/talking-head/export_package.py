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
    fmt_seconds,
    load_json,
    to_frames,
    validate_keeps,
)

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Timecode
# ---------------------------------------------------------------------------


def timecode(frames: int, fps: int) -> str:
    """Frames -> HH:MM:SS:FF, non-drop.

    Drop-frame is deliberately not emitted. At 29.97 or 23.976 a non-drop
    list and a drop-frame list disagree by ~3.6s/hour, and silently
    conforming to the wrong one is the classic way an EDL round-trip
    drifts. --fps is validated as an integer for the same reason.
    """
    frames = max(0, int(frames))
    ff = frames % fps
    total_seconds = frames // fps
    return f"{total_seconds // 3600:02d}:{(total_seconds // 60) % 60:02d}:{total_seconds % 60:02d}:{ff:02d}"


def srt_time(frames: int, fps: int) -> str:
    total_ms = int(round(frames * 1000 / fps))
    ms = total_ms % 1000
    total_seconds = total_ms // 1000
    return f"{total_seconds // 3600:02d}:{(total_seconds // 60) % 60:02d}:{total_seconds % 60:02d},{ms:03d}"


def rational(frames: int, fps: int) -> str:
    """FCPXML rational time, e.g. 264/30s. Exact -- no decimal rounding."""
    return "0s" if frames == 0 else f"{frames}/{fps}s"


# ---------------------------------------------------------------------------
# Graphic elements
# ---------------------------------------------------------------------------


def graphic_elements(
    callouts: list[dict],
    fps: int,
    lt_start: float,
    lt_dur: float,
    caption_frames: int = 0,
) -> list[dict]:
    """Every layer that gets its own rendered asset, in timeline order.

    Captions are lane 1, graphics lane 2 -- matching the z-order inside the
    composition, where callouts and the lower third sit above captions.
    """
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
            "place_frames": to_frames(lt_start - LEAD, fps),
            "duration_frames": to_frames(LEAD + lt_dur + 0.4 + TAIL, fps),
            # The moment the graphic is fully on screen, used for the still.
            "settled_frames": to_frames(LEAD + 0.5, fps),
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
                "place_frames": to_frames(float(callout["start"]) - LEAD, fps),
                "duration_frames": to_frames(LEAD + float(callout["dur"]) + 0.3 + TAIL, fps),
                "settled_frames": to_frames(LEAD + 0.45, fps),
                "lane": 2,
            }
        )
    elements.sort(key=lambda e: (e["lane"], e["place_frames"]))
    return elements


# ---------------------------------------------------------------------------
# SRT
# ---------------------------------------------------------------------------


def write_srt(path: Path, cues: list[dict], fps: int) -> None:
    blocks = []
    for index, cue in enumerate(cues, start=1):
        blocks.append(
            f"{index}\n"
            f"{srt_time(cue['start'], fps)} --> {srt_time(cue['end'], fps)}\n"
            f"{cue['text']}\n"
        )
    path.write_text("\n".join(blocks), encoding="utf-8")


# ---------------------------------------------------------------------------
# CMX3600 EDL
# ---------------------------------------------------------------------------


def write_edl(path: Path, timeline: Timeline, fps: int, title: str, reel: str) -> None:
    lines = [f"TITLE: {title}", "FCM: NON-DROP FRAME", ""]
    for index, keep in enumerate(timeline.keeps, start=1):
        lines.append(
            f"{index:03d}  {reel:<8} AA/V  C        "
            f"{timecode(keep['sf_start'], fps)} {timecode(keep['sf_end'], fps)} "
            f"{timecode(keep['of_start'], fps)} {timecode(keep['of_end'], fps)}"
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
    fps: int,
    width: int,
    height: int,
    source_file: Path,
    source_duration_frames: int,
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

    ET.SubElement(
        resources,
        "format",
        id="r0",
        name=f"FFVideoFormat{height}p{fps}",
        frameDuration=f"1/{fps}s",
        width=str(width),
        height=str(height),
        colorSpace="1-1-1 (Rec. 709)",
    )

    source_asset = ET.SubElement(
        resources,
        "asset",
        id="r1",
        name=source_file.stem,
        start="0s",
        duration=rational(source_duration_frames, fps),
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
            duration=rational(timeline.total_frames, fps),
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
            duration=rational(element["duration_frames"], fps),
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
        duration=rational(timeline.total_frames, fps),
        tcStart="0s",
        tcFormat="NDF",
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
            duration=rational(timeline.total_frames, fps),
            format="r0",
            tcFormat="NDF",
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
                offset=rational(keep["of_start"], fps),
                start=rational(keep["sf_start"], fps),
                duration=rational(keep["frames"], fps),
                format="r0",
                tcFormat="NDF",
            )
            spine_clips.append((clip, keep["of_start"], keep["sf_start"]))

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
            offset=rational(local_start + (place - record_in), fps),
            start="0s",
            duration=rational(element["duration_frames"], fps),
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
    fps: int,
    source_file: Path,
    elements: list[dict],
    recipe_dir: Path,
    out_dir: Path,
) -> None:
    # One decode, N trim filters, one concat -- not N re-opens of the same
    # file. The naive form (`-ss A -to B -i src` repeated per keep) opens a
    # decoder per segment and falls over on a long cut list.
    parts, labels = [], []
    for index, keep in enumerate(timeline.keeps):
        a = keep["sf_start"] / fps
        b = keep["sf_end"] / fps
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
        "# 1. Rough cut -- the cut only, no graphics. Single decode.",
        'ffmpeg -y -i "$SRC" -filter_complex "' + filtergraph + '" \\',
        '  -map "[outv]" -map "[outa]" -c:v libx264 -crf 18 -preset medium \\',
        '  -c:a aac -b:a 192k "$OUT/rough_cut.mp4"',
        "",
        "# 2. Full video -- cut plus graphics, baked.",
        '#    clips/media/source.mp4 must exist for this to render.',
        'npx hyperframes render "$RECIPE/clips" -o "$OUT/final.mp4"',
        "",
        "# 3. Flattened graphics overlay, full length, alpha.",
        "#    ProRes 4444, not WebM: WebM alpha shows as black in Resolve.",
        'npx hyperframes render "$RECIPE/overlay" --format mov -o "$OUT/graphics/overlay.mov"',
        "",
        "# 4. Every layer as its own transparent asset. These are what the",
        "#    FCPXML timeline references -- render them before importing it.",
    ]
    for element in elements:
        slug = element["slug"]
        lines.append(
            f'npx hyperframes render "$RECIPE/gfx/{slug}" --format mov '
            f'-o "$OUT/graphics/{slug}.mov"'
        )
    lines += ["", "# 5. Flat PNG stills, for when a still is easier to place than a clip."]
    for element in elements:
        slug = element["slug"]
        at = element["settled_frames"] / fps
        lines.append(
            f'ffmpeg -y -ss {at:.3f} -i "$OUT/graphics/{slug}.mov" -frames:v 1 '
            f'"$OUT/graphics/stills/{slug}.png"'
        )
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
    parser.add_argument("--fps", type=int)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
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

    fps = args.fps or int(edl.get("fps", 30))
    if abs(fps - round(fps)) > 1e-9:
        raise SystemExit("Only integer frame rates are supported. See the drop-frame note.")

    words: list[dict] = []
    if args.transcript:
        transcript = load_json(args.transcript)
        words = transcript if isinstance(transcript, list) else transcript.get("words", [])

    callouts = load_json(args.callouts) if args.callouts else []
    timeline = Timeline(keeps, fps)
    if timeline.total_frames <= 0:
        raise SystemExit("EDL keeps produced a zero-length timeline.")

    cues = build_cues(words, timeline, args.words_per_cue, args.min_words, args.gap) if words else []
    elements = graphic_elements(
        callouts,
        fps,
        lt_start=0.6,
        lt_dur=4.6,
        caption_frames=timeline.total_frames if cues else 0,
    )

    out = args.out.resolve()
    (out / "graphics" / "stills").mkdir(parents=True, exist_ok=True)
    gfx_root = HERE / "gfx"

    # One standalone composition per graphic, rendered later into its own
    # transparent asset.
    for element in elements:
        target = gfx_root / element["slug"] / "index.html"
        cmd = [
            sys.executable,
            str(HERE / "build_composition.py"),
            "--edl",
            str(args.edl.resolve()),
            "--only",
            element["only"],
            "--comp-id",
            f"gfx-{element['slug']}",
            "--width",
            str(args.width),
            "--height",
            str(args.height),
            "--fps",
            str(fps),
            "--title",
            args.title,
            "--subtitle",
            args.subtitle,
            "--out",
            str(target),
        ]
        if args.callouts:
            cmd += ["--callouts", str(args.callouts.resolve())]
        if element["only"] == "captions":
            # The captions layer needs the transcript and the identical cue
            # grouping, or it renders empty or out of sync with final.mp4.
            if not args.transcript:
                raise SystemExit("A captions layer was requested but no --transcript was given.")
            cmd += [
                "--transcript",
                str(args.transcript.resolve()),
                "--words-per-cue",
                str(args.words_per_cue),
                "--min-words",
                str(args.min_words),
                "--gap",
                str(args.gap),
            ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    if cues:
        write_srt(out / "captions.srt", cues, fps)
    write_edl(out / "edit.edl", timeline, fps, args.project_name, args.reel[:8])

    source_duration_frames = (
        to_frames(args.source_duration, fps)
        if args.source_duration
        else to_frames(
            max(
                [float(k["end"]) for k in keeps]
                + [float(c["end"]) for c in edl.get("cuts", [])]
            ),
            fps,
        )
    )

    write_fcpxml(
        out / "edit.fcpxml",
        timeline=timeline,
        fps=fps,
        width=args.width,
        height=args.height,
        source_file=args.source_file,
        source_duration_frames=source_duration_frames,
        elements=elements,
        graphics_dir=out / "graphics",
        project_name=args.project_name,
        v1=args.v1,
        rough_cut=out / "rough_cut.mp4",
    )

    manifest = {
        "project": args.project_name,
        "fps": fps,
        "resolution": [args.width, args.height],
        "timelineDuration": round(timeline.total_frames / fps, 3),
        "sourceFile": str(args.source_file),
        "sourceDuration": round(source_duration_frames / fps, 3),
        "deliverables": {
            "final.mp4": "Full video — cut with graphics baked in.",
            "rough_cut.mp4": "The cut only, no graphics.",
            "edit.fcpxml": (
                "Complete program: the cut plus every graphic layer in place. "
                "Render it and you get the same picture as final.mp4."
            ),
            "edit.edl": "CMX3600 conform list, cut only. Fallback if the FCPXML is rejected.",
            "captions.srt": "Import as a subtitle track.",
            "graphics/overlay.mov": "All graphics, full length, ProRes 4444 alpha.",
        },
        "cut": [
            {
                "index": index,
                "sourceIn": round(keep["sf_start"] / fps, 3),
                "sourceOut": round(keep["sf_end"] / fps, 3),
                "recordIn": round(keep["of_start"] / fps, 3),
                "recordOut": round(keep["of_end"] / fps, 3),
                "sourceInTC": timecode(keep["sf_start"], fps),
                "recordInTC": timecode(keep["of_start"], fps),
            }
            for index, keep in enumerate(timeline.keeps)
        ],
        "graphics": [
            {
                "slug": element["slug"],
                "name": element["name"],
                "clip": f"graphics/{element['slug']}.mov",
                "still": f"graphics/stills/{element['slug']}.png",
                "placeAt": round(element["place_frames"] / fps, 3),
                "placeAtTC": timecode(element["place_frames"], fps),
                "duration": round(element["duration_frames"] / fps, 3),
                "lane": 1,
            }
            for element in elements
        ],
        "captions": [
            {
                "text": cue["text"],
                "start": round(cue["start"] / fps, 3),
                "end": round(cue["end"] / fps, 3),
            }
            for cue in cues
        ],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    write_build_script(
        out / "build.sh",
        timeline=timeline,
        fps=fps,
        source_file=args.source_file,
        elements=elements,
        recipe_dir=HERE,
        out_dir=out,
    )

    print(f"Package scaffolded in {out}")
    print(f"  timeline      {fmt_seconds(timeline.total_frames, fps)}s, {len(timeline.keeps)} clips")
    print(f"  graphics      {len(elements)} assets → {gfx_root}")
    print(f"  captions      {len(cues)} cues")
    print(f"  next          {out / 'build.sh'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
