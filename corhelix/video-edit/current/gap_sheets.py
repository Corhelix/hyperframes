"""Every-frame contact sheets for one splice, read by eye (video edit SOP v0.4, stage 06).

A splice joins an OUT point (end of the last kept word) to an IN point (start of the next
kept word). The pause that stays is whatever looks and sounds natural, so the useful
frames are the ones just after the last word and just before the next one. This script
slices EVERY frame of two windows, not a sample:

    out window  [out_from, out_from + window]   frames just after the last kept word
    in window   [in_to - window, in_to]         frames just before the next kept word

Each frame is cropped to the head and shoulders, drawn with a thin grid (thirds) and a
centre crosshair, labelled with its time, and tiled in order. No tracking software is
involved: a person reads the two sheets and picks the pair where the head sits at the same
place, with the same tilt and turn, and no frame is mid-blink or mid-movement.

For a gap inside one run, out_from is the last word's end and in_to is the next word's
start. For a splice across removed material, out_from is the end of the last kept word
before it and in_to is the start of the first kept word after it.

Usage:
    gap_sheets.py VIDEO OUTDIR LABEL OUT_FROM IN_TO [--window 2.0] [--fps 30]
                  [--crop 0.344,0.208,0.359,0.653] [--cols 10] [--tile 180x184]

Writes OUTDIR/LABEL-out.png, OUTDIR/LABEL-in.png and OUTDIR/LABEL-frames.json.
"""
import argparse, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def grab(video, t0, dur, fps, crop, tw, th):
    cx, cy, cw, ch = crop
    vf = f"fps={fps},crop=iw*{cw}:ih*{ch}:iw*{cx}:ih*{cy},scale={tw}:{th}"
    raw = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(video),
         "-vf", vf, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
        capture_output=True, check=True).stdout
    n = len(raw) // (tw * th * 3)
    return [(t0 + k / fps, Image.frombytes("RGB", (tw, th), raw[k * tw * th * 3:(k + 1) * tw * th * 3])) for k in range(n)]


def sheet(frames, path, cols, tw, th, title):
    label_h = 16
    rows = (len(frames) + cols - 1) // cols
    head = 22
    img = Image.new("RGB", (cols * tw, head + rows * (th + label_h)), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((6, 5), title, fill=(0, 0, 0))
    for i, (t, fr) in enumerate(frames):
        fr = fr.copy()
        g = ImageDraw.Draw(fr)
        for k in (1, 2):                                   # thirds
            g.line((tw * k // 3, 0, tw * k // 3, th), fill=(0, 102, 255), width=1)
            g.line((0, th * k // 3, tw, th * k // 3), fill=(0, 102, 255), width=1)
        g.line((tw // 2 - 6, th // 2, tw // 2 + 6, th // 2), fill=(255, 0, 0), width=1)   # centre crosshair
        g.line((tw // 2, th // 2 - 6, tw // 2, th // 2 + 6), fill=(255, 0, 0), width=1)
        x, y = (i % cols) * tw, head + (i // cols) * (th + label_h)
        img.paste(fr, (x, y))
        d.text((x + 3, y + th + 2), f"{t:.2f}", fill=(0, 0, 0))
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("outdir"); ap.add_argument("label")
    ap.add_argument("out_from", type=float); ap.add_argument("in_to", type=float)
    ap.add_argument("--window", type=float, default=2.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crop", default="0.344,0.208,0.359,0.653", help="x,y,w,h as fractions of the frame")
    ap.add_argument("--cols", type=int, default=10)
    ap.add_argument("--tile", default="180x184")
    a = ap.parse_args()
    crop = tuple(float(v) for v in a.crop.split(","))
    tw, th = (int(v) for v in a.tile.split("x"))
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    o = grab(a.video, a.out_from, a.window, a.fps, crop, tw, th)
    i = grab(a.video, a.in_to - a.window, a.window, a.fps, crop, tw, th)
    sheet(o, out / f"{a.label}-out.png", a.cols, tw, th, f"{a.label} OUT window {a.out_from:.2f} to {a.out_from + a.window:.2f} s, {len(o)} frames")
    sheet(i, out / f"{a.label}-in.png", a.cols, tw, th, f"{a.label} IN window {a.in_to - a.window:.2f} to {a.in_to:.2f} s, {len(i)} frames")
    json.dump({"label": a.label, "out_frames": [round(t, 3) for t, _ in o], "in_frames": [round(t, 3) for t, _ in i]},
              open(out / f"{a.label}-frames.json", "w"))
    print(f"{a.label}: {len(o)} out frames, {len(i)} in frames")


if __name__ == "__main__":
    sys.exit(main())
