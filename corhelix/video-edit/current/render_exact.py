"""render.py with exact segment lengths (video edit SOP v0.4, stage 07 and V6).

video-use's render.py extracts each EDL range with `-t duration`. The source is 30 fps and the cut is
24 fps, so a range whose start sits between 24 fps frames comes out one frame long, and on a long
cut the video runs ahead of the audio and the output misses the EDL sum. This wrapper loads render.py
unchanged and replaces only extract_segment: it adds `-frames:v N` where N = round(duration x 24),
so each segment's video is exactly its EDL length. Use frame-aligned EDL ranges (multiples of 1/24 s).

Usage (same arguments as render.py):
    render_exact.py EDL.json -o out.mp4 [--preview] [--no-subtitles] ...
"""
import subprocess, sys
from pathlib import Path

VIDEO_USE = Path.home() / "Documents" / "video-use" / "helpers"
sys.path.insert(0, str(VIDEO_USE))
import render  # noqa: E402


def extract_segment(source, seg_start, duration, grade_filter, out_path, preview=False, draft=False):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    portrait = render.is_portrait_source(source)
    scale = ("scale=-2:1280" if portrait else "scale=1280:-2") if draft else ("scale=-2:1920" if portrait else "scale=1920:-2")
    vf = ",".join(([render.TONEMAP_CHAIN] if render.is_hdr_source(source) else []) + [scale] + ([grade_filter] if grade_filter else []))
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0.0, duration - 0.03):.3f}:d=0.03"
    preset, crf = ("ultrafast", "28") if draft else (("medium", "22") if preview else ("fast", "20"))
    frames = round(duration * 24)
    cmd = ["ffmpeg", "-y", "-ss", f"{seg_start:.3f}", "-i", str(source), "-t", f"{duration:.3f}", "-frames:v", str(frames),
           "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", preset, "-crf", crf, "-pix_fmt", "yuv420p", "-r", "24",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


render.extract_segment = extract_segment

if __name__ == "__main__":
    render.main()
