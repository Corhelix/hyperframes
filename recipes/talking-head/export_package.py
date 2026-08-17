#!/usr/bin/env python3
"""
Export a Resolve-ready package from a transcript + EDL + callouts.

Produces four deliverables so the same job can be either finished or
re-opened:

  1. final.mp4        the full video -- cut with graphics baked in
  2. rough_cut.mp4    the cut only, no graphics, for hand-finishing
  3. edit.fcpxml      layered timeline: V1 the cut, V2+ the graphics
  4. graphics/        each graphic as its own transparent ProRes MOV,
                      plus a flattened full-length overlay and PNG stills

Plus captions.srt (a native Resolve subtitle track) and edit.edl (a
CMX3600 conform list as a fallback if the FCPXML is rejected).

This script writes the *project files and the build script*. It does not
render or transcode -- run out/build.sh for that, on a machine with
ffmpeg and a working `hyperframes render`.

The FCPXML references the ORIGINAL source with source in/out points, not
rough_cut.mp4. That is deliberate: pointing at the cut file would lock
the editor to these cut points with no handles, which defeats the reason
for shipping an editable timeline at all.

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


def graphic_elements(callouts: list[dict], fps: int, lt_start: float, lt_dur: float) -> list[dict]:
    """Every graphic that gets its own rendered asset, in timeline order."""
    elements: list[dict] = [
        {
            "key": "lower-third",
            "slug": "lower-third",
            "name": "Lower third",
            "only": "lower-third",
            "place_frames": to_frames(lt_start - LEAD, fps),
            "duration_frames": to_frames(LEAD + lt_dur + 0.4 + TAIL, fps),
            # The moment the graphic is fully on screen, used for the still.
            "settled_frames": to_frames(LEAD + 0.5, fps),
        }
    ]
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
            }
        )
    elements.sort(key=lambda e: e["place_frames"])
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
) -> None:
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

    spine_clips = []
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
        spine_clips.append((clip, keep))

    # Graphics ride as connected clips on lane 1. A connected clip's offset is
    # expressed in its PARENT's local time base -- i.e. measured from the
    # parent's `start`, not from the sequence origin. Getting this wrong is the
    # usual reason graphics land in the wrong place on import.
    for element in elements:
        place = element["place_frames"]
        parent, keep = spine_clips[0]
        for candidate, candidate_keep in spine_clips:
            if candidate_keep["of_start"] <= place < candidate_keep["of_end"]:
                parent, keep = candidate, candidate_keep
                break
        else:
            if place >= spine_clips[-1][1]["of_end"]:
                parent, keep = spine_clips[-1]

        local_offset = keep["sf_start"] + (place - keep["of_start"])
        ET.SubElement(
            parent,
            "asset-clip",
            ref=element["ref"],
            lane="1",
            name=element["name"],
            offset=rational(local_offset, fps),
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
        "# 4. Each graphic as its own transparent asset, for free repositioning.",
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
    elements = graphic_elements(callouts, fps, lt_start=0.6, lt_dur=4.6)

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
            "edit.fcpxml": "Layered timeline. V1 references the ORIGINAL source with handles.",
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
