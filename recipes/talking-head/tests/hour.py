#!/usr/bin/env python3
"""
The harness GOAL.md is measured against.

Builds a deterministic 55-minute talking-head transcript with fillers and
dead air, runs detection and the package export over it, and asserts the
measures in GOAL.md. Exit code is the verdict.

    python3 tests/hour.py

This is the case the system exists for. It had never been run before
2026-08-18, and running it found three failures that a three-cut sample
could not surface.
"""

from __future__ import annotations

import json
import random
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FILLERS = ["um", "uh", "er", "ah", "mm"]
SPEECH = ["the", "system", "makes", "this", "visible", "before", "anyone", "asks", "for", "it"]

results: list[tuple[str, str, str, bool]] = []


def check(measure: str, threshold: str, actual, passed: bool) -> None:
    results.append((measure, threshold, str(actual), passed))


def build_transcript(path: Path, minutes: float = 55.0) -> tuple[float, int]:
    """Speech runs separated by dead air, with a filler at most boundaries."""
    rng = random.Random(11)
    words: list[dict] = []
    t = 0.9
    while t < minutes * 60:
        for _ in range(rng.randint(14, 40)):
            dur = rng.uniform(0.18, 0.44)
            words.append({"text": rng.choice(SPEECH), "start": round(t, 3), "end": round(t + dur, 3)})
            t += dur + rng.uniform(0.02, 0.09)
        if rng.random() < 0.75:
            t += rng.uniform(0.15, 0.4)
            dur = rng.uniform(0.16, 0.3)
            words.append({"text": rng.choice(FILLERS), "start": round(t, 3), "end": round(t + dur, 3)})
            t += dur
        t += rng.uniform(0.7, 2.2)
    path.write_text(json.dumps(words), encoding="utf-8")
    return t + 3.0, len(words)


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stdout + proc.stderr)
        raise SystemExit(f"command failed: {' '.join(cmd[:3])}")
    return proc.stdout


def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="hour-"))
    transcript = work / "transcript.json"
    duration, word_count = build_transcript(transcript)
    edl = work / "clean.edl.json"
    source = work / "source.mp4"
    source.write_bytes(b"")

    run([sys.executable, str(HERE / "detect_cuts.py"), "--transcript", str(transcript),
         "--out", str(edl), "--source", "media/source.mp4", "--fps", "25",
         "--source-duration", str(duration)])
    cut_list = json.loads(edl.read_text())
    keeps, words = cut_list["keeps"], json.loads(transcript.read_text())

    # Detection: the safety property, and that it actually removed something.
    fillers = [w for w in words if w["text"] in FILLERS]
    split = [
        w for w in words if w["text"] not in FILLERS
        and not any(k["start"] <= w["start"] + 1e-6 and k["end"] >= w["end"] - 1e-6 for k in keeps)
    ]
    check("Words split by a cut", "0", len(split), not split)
    surviving_fillers = [
        w for w in fillers
        if any(k["start"] <= w["start"] + 1e-6 and k["end"] >= w["end"] - 1e-6 for k in keeps)
    ]
    check("Fillers left audible", "0", len(surviving_fillers), not surviving_fillers)
    disjoint = all(a["end"] <= b["start"] + 1e-9 for a, b in zip(keeps, keeps[1:]))
    check("Keeps disjoint and ascending", "yes", "yes" if disjoint else "no", disjoint)
    removed = cut_list["detection"]["removedDuration"]
    check("Dead air removed", "> 0s", f"{removed:.0f}s", removed > 0)
    check("EDL authored by hand", "no", "no", True)

    out = work / "out"
    run([sys.executable, str(HERE / "export_package.py"), "--edl", str(edl),
         "--transcript", str(transcript), "--source-file", str(source),
         "--source-duration", str(duration), "--no-probe", "--fps", "25", "--out", str(out)])

    build = (out / "build.sh").read_text()
    longest = max(len(line) for line in build.splitlines())
    slice_jobs = build.count("|| ffmpeg")
    check("Slices emitted, one per section", f"= {len(keeps)}", slice_jobs, slice_jobs == len(keeps))
    check("Longest generated command", "< 4000 chars", longest, longest < 4000)
    monolithic = "trim=start=" in build or f"concat=n={len(keeps)}" in build
    check("Monolithic re-encode", "none", "present" if monolithic else "none", not monolithic)

    root = ET.parse(out / "edit.fcpxml").getroot()
    clips = root.find(".//spine").findall("asset-clip")
    total, contiguous = 0, True
    for clip in clips:
        offset = int(clip.get("offset").split("/")[0]) if "/" in clip.get("offset") else 0
        if offset != total:
            contiguous = False
        total += int(clip.get("duration").split("/")[0])
    seq = int(root.find(".//sequence").get("duration").split("/")[0])
    check("XML spine contiguous", "exact", "exact" if contiguous and total == seq else "broken",
          contiguous and total == seq)
    check("XML sections", f"= {len(keeps)}", len(clips), len(clips) == len(keeps))
    fmt = root.find(".//format")
    check("XML project fps", "1/25s", fmt.get("frameDuration"), fmt.get("frameDuration") == "1/25s")
    check("XML pixel size", "1920x1080", f'{fmt.get("width")}x{fmt.get("height")}',
          (fmt.get("width"), fmt.get("height")) == ("1920", "1080"))
    renders = build.count("hyperframes render")
    check("Full-length graphics renders", "<= 2", renders, renders <= 2)

    width = max(len(r[0]) for r in results)
    print(f"\n  {'Measure'.ljust(width)}  {'Threshold'.ljust(16)}  {'Actual'.ljust(10)}")
    for measure, threshold, actual, passed in results:
        print(f"  {measure.ljust(width)}  {threshold.ljust(16)}  {actual.ljust(10)}  "
              f"{'pass' if passed else 'FAIL'}")
    failed = [r for r in results if not r[3]]
    print(f"\n  {len(results) - len(failed)}/{len(results)} measures pass. "
          f"Source {duration / 60:.0f} min, {word_count} words, {len(keeps)} sections.\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
