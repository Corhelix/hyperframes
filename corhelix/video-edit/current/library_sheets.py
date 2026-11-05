"""Labelled contact sheets of a whole image library, for the edit pass (SOP stage 11, beats to visuals).

Every tile shows the id, kind (IMG, CLIP or REC), status, brand and the catalogue description, so an editor
can read the tags across the whole library before choosing what best shows a phrase.

  python library_sheets.py --catalogue <dir with INDEX-catalogue-ids.csv> --out <dir>
                           [--recordings <dir of screen recordings>] [--extra <video> ...]

Writes <out>/sheet-NN.jpg (5 x 6 tiles each) and <out>/index.json (every item with its text and source path).
Video items get a poster frame. Needs Pillow and ffmpeg.
"""
import argparse
import csv
import json
import os
import subprocess
import textwrap

from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--catalogue", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--recordings")
ap.add_argument("--extra", nargs="*", default=[])
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
VID = (".mp4", ".mov", ".mkv", ".webm")


def poster(src, name, at=1.0):
    dst = os.path.join(a.out, f"_t_{name}.jpg")
    if not os.path.exists(dst):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at), "-i", src, "-frames:v", "1", "-vf", "scale=480:-2", dst])
    return dst


items = []
for r in csv.DictReader(open(os.path.join(a.catalogue, "INDEX-catalogue-ids.csv"), encoding="utf-8-sig")):
    src = os.path.join(a.catalogue, r["file"])
    vid = src.lower().endswith(VID)
    items.append(dict(id=r["id"], kind="CLIP" if vid else "IMG", status=r["status"], brand=r["brand"],
                      desc=r["description"], note=r["note"], file=src, src=poster(src, r["id"]) if vid else src))
recs = []
if a.recordings:
    recs = [os.path.join(a.recordings, f) for f in sorted(os.listdir(a.recordings)) if f.lower().endswith(VID)]
for n, src in enumerate(recs + a.extra, 1):
    try:
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                 capture_output=True, text=True).stdout.strip())
    except ValueError:
        d = 2.0
    items.append(dict(id=f"REC{n:02d}", kind="REC", status="recording", brand="", desc=os.path.basename(src), note="",
                      file=src, src=poster(src, f"REC{n:02d}", d * 0.3)))

try:
    F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    F2 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
except OSError:
    F = F2 = ImageFont.load_default()
TW, TH, CAP, COLS, ROWS = 320, 180, 62, 5, 6
COL = {"approved": "#0066FF", "held": "#C00000", "recording": "#7C3AED"}
sheets = []
for s in range(0, len(items), COLS * ROWS):
    chunk = items[s:s + COLS * ROWS]
    im = Image.new("RGB", (COLS * TW, ROWS * (TH + CAP)), "white")
    d = ImageDraw.Draw(im)
    for n, it in enumerate(chunk):
        x, y = (n % COLS) * TW, (n // COLS) * (TH + CAP)
        try:
            t = Image.open(it["src"]).convert("RGB")
            t.thumbnail((TW - 8, TH - 6))
            im.paste(t, (x + 4 + (TW - 8 - t.width) // 2, y + 3 + (TH - 6 - t.height) // 2))
        except Exception:
            d.text((x + 10, y + 80), "no preview", fill="red", font=F2)
        d.text((x + 6, y + TH + 2), f"{it['id']} {it['kind']} {it['status'].upper()} {it['brand'][:18]}", fill=COL.get(it["status"], "#333"), font=F)
        for k, ln in enumerate(textwrap.wrap(it["desc"], 52)[:3]):
            d.text((x + 6, y + TH + 20 + k * 13), ln, fill="#222", font=F2)
    p = os.path.join(a.out, f"sheet-{len(sheets) + 1:02d}.jpg")
    im.save(p, quality=82)
    sheets.append({"sheet": p, "ids": [c["id"] for c in chunk]})
json.dump({"sheets": sheets, "items": items}, open(os.path.join(a.out, "index.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(items), "items,", len(sheets), "sheets in", a.out)
