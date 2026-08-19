#!/usr/bin/env python3
"""
batch.py -- run the built chain (transcribe -> detect_cuts -> decide_cuts ->
export_package -> build.sh) across every video in a source directory.

The recipe is one-video-per-invocation by design (see README.md, HANDOFF.md).
This does not change that contract or invent new pipeline stages -- it loops
the documented sequence over N source files, each fully isolated in its own
output directory, and writes a per-video + summary report.

It does not fake anything GOAL.md marks as not built: no polished_script.txt,
no frame-context / visual-cut-scoring pass. Only the built stages run.

Usage:
    python3 batch.py --source-dir clips/ --out-dir batch-out/
    python3 batch.py --source-dir clips/ --out-dir batch-out/ --no-model --skip-render

Each video's per-stage stdout+stderr lands in
<out-dir>/<video-name>/<stage>.log so a failure is diagnosable without
re-running. report.json at the batch root is the machine-readable summary;
report.md is the human one.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO_EXTS = {".mp4", ".mov", ".mxf", ".mkv", ".m4v"}


def resolve_npx() -> str:
    npx = shutil.which("npx")
    if npx:
        return npx
    raise SystemExit("npx not found on PATH -- needed for `hyperframes transcribe`.")


def probe(video: Path) -> tuple[float, str]:
    """Return (duration_seconds, fps_as_string) via ffprobe. Stdlib-adjacent:
    ffprobe is already a hard prerequisite of this recipe (HANDOFF.md)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=r_frame_rate:format=duration",
         "-of", "json", str(video)],
        capture_output=True, text=True, check=True,
    ).stdout
    data = json.loads(out)
    duration = float(data["format"]["duration"])
    fps_raw = data["streams"][0]["r_frame_rate"]  # e.g. "25/1" or "30000/1001"
    num, den = fps_raw.split("/")
    fps = float(num) / float(den)
    return duration, f"{fps:g}"


def run_stage(cmd: list[str], cwd: Path, log_path: Path) -> tuple[bool, float]:
    # Subprocess children (npx/hyperframes/ffmpeg) can emit bytes outside the
    # Windows console's default cp1252 codepage. text=True would decode with
    # that default and crash the reader thread -- explicit UTF-8 + replace
    # keeps the batch running instead of losing a video to a decode error.
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True,
                           encoding="utf-8", errors="replace")
    dur = time.time() - t0
    log_path.write_text(
        f"$ {' '.join(cmd)}\n\n--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n",
        encoding="utf-8",
    )
    return proc.returncode == 0, dur


def process_one(video: Path, out_root: Path, npx: str, args) -> dict:
    name = video.stem
    workdir = out_root / name
    workdir.mkdir(parents=True, exist_ok=True)
    result = {"video": video.name, "workdir": str(workdir), "stages": {}, "ok": False}

    try:
        duration, fps = probe(video)
    except Exception as e:
        result["error"] = f"probe failed: {e}"
        return result
    result["duration_s"] = round(duration, 2)
    result["fps"] = fps

    transcript = workdir / "transcript.json"
    ok, dur = run_stage(
        [npx, "--yes", "hyperframes", "transcribe", str(video),
         "-d", str(workdir), "--model", args.model],
        HERE, workdir / "01-transcribe.log",
    )
    result["stages"]["transcribe"] = {"ok": ok, "seconds": round(dur, 1)}
    if not ok or not transcript.exists():
        result["error"] = "transcribe failed or wrote no transcript.json"
        return result

    candidates = workdir / "candidates.json"
    thresholded = workdir / "thresholded.edl.json"
    ok, dur = run_stage(
        [sys.executable, "detect_cuts.py",
         "--transcript", str(transcript), "--out", str(thresholded),
         "--candidates", str(candidates),
         "--source", str(video), "--fps", fps,
         "--source-duration", str(duration)],
        HERE, workdir / "02-detect_cuts.log",
    )
    result["stages"]["detect_cuts"] = {"ok": ok, "seconds": round(dur, 1)}
    if not ok:
        result["error"] = "detect_cuts failed"
        return result

    clean_edl = workdir / "clean.edl.json"
    decide_cmd = [sys.executable, "decide_cuts.py",
                  "--candidates", str(candidates), "--out", str(clean_edl)]
    if args.no_model:
        decide_cmd.append("--no-model")
    ok, dur = run_stage(decide_cmd, HERE, workdir / "03-decide_cuts.log")
    result["stages"]["decide_cuts"] = {"ok": ok, "seconds": round(dur, 1)}
    if not ok or not clean_edl.exists():
        result["error"] = "decide_cuts failed or wrote no clean.edl.json"
        return result

    out_pkg = workdir / "out"
    ok, dur = run_stage(
        [sys.executable, "export_package.py",
         "--edl", str(clean_edl), "--transcript", str(transcript),
         "--source-file", str(video.resolve()), "--out", str(out_pkg)],
        HERE, workdir / "04-export_package.log",
    )
    result["stages"]["export_package"] = {"ok": ok, "seconds": round(dur, 1)}
    if not ok:
        result["error"] = "export_package failed"
        return result

    if not args.skip_render:
        build_sh = out_pkg / "build.sh"
        ok, dur = run_stage(["bash", str(build_sh)], out_pkg, workdir / "05-build.log")
        result["stages"]["build"] = {"ok": ok, "seconds": round(dur, 1)}
        if not ok:
            result["error"] = "build.sh failed"
            return result

    result["ok"] = True
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source-dir", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--no-model", action="store_true", help="Skip decide_cuts' model judging (fast, unreviewed).")
    ap.add_argument("--skip-render", action="store_true", help="Stop after export_package; don't run build.sh.")
    args = ap.parse_args()

    videos = sorted(p for p in args.source_dir.iterdir() if p.suffix.lower() in VIDEO_EXTS)
    if not videos:
        print(f"No video files ({', '.join(sorted(VIDEO_EXTS))}) found in {args.source_dir}", file=sys.stderr)
        return 2

    npx = resolve_npx()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, video in enumerate(videos, 1):
        print(f"[{i}/{len(videos)}] {video.name} ...")
        r = process_one(video, args.out_dir, npx, args)
        results.append(r)
        status = "pass" if r["ok"] else f"FAIL ({r.get('error', 'unknown')})"
        print(f"    {status}")

    passed = sum(1 for r in results if r["ok"])
    summary = {"total": len(results), "passed": passed, "failed": len(results) - passed, "results": results}
    (args.out_dir / "report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [f"# Batch report", "", f"{passed}/{len(results)} passed", ""]
    for r in results:
        lines.append(f"## {r['video']} -- {'PASS' if r['ok'] else 'FAIL'}")
        if not r["ok"]:
            lines.append(f"- error: {r.get('error')}")
        for stage, s in r.get("stages", {}).items():
            lines.append(f"- {stage}: {'ok' if s['ok'] else 'FAILED'} ({s['seconds']}s)")
        lines.append("")
    (args.out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"\n{passed}/{len(results)} passed. Report: {args.out_dir / 'report.md'}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
