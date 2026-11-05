"""Composite slides, the speaker panel and callouts over the cut (video edit SOP v0.4, stage 12).

Layout (16:9, 1920x1080), from the SOP geometry:
  mode A  speaker full frame (no layer)
  mode B  a callout over the speaker, bottom-left
  mode C  a slide at (40, 40) 1280x720 on a 1920x1080 canvas, the speaker in a rounded panel at
          (1360, 455) 520x585, radius 28, and any callout in the caption band from y 790

Reads layers.json (made by build_callouts' sibling build_layers.py). Slide canvases are drawn with PIL;
callouts are the transparent WebM renders from callouts/build_callouts.py, laid on with
setpts=PTS-STARTPTS+T/TB so frame 0 of each lands at its out time (SOP hard rule 4). Audio is copied
from the base untouched. Subtitles are a sidecar, so nothing is burned in here.

Usage:
    compose.py --layers layers.json --base preview-cut.mp4 --slides SLIDEDIR --callouts CALLOUTDIR \
               --work WORKDIR --out draft.mp4 [--crf 20] [--only-window START,END]
"""
import argparse, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

BG = {"white": (255, 255, 255), "blue": (30, 91, 255), "own": (10, 26, 58)}
SX, SY, SW, SH = 40, 40, 1280, 720
HX, HY, HW, HH = 1360, 455, 520, 585


def canvas(slide_path, bg, out):
    cv = Image.new("RGB", (1920, 1080), BG[bg])
    s = Image.open(slide_path).convert("RGBA")
    s.thumbnail((SW, SH), Image.LANCZOS)
    if bg != "own":
        pad = Image.new("RGBA", s.size, BG[bg] + (255,)); pad.alpha_composite(s); s = pad
    cv.paste(s, (SX + (SW - s.width) // 2, SY + (SH - s.height) // 2), s)
    cv.save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--layers", required=True); ap.add_argument("--base", required=True)
    ap.add_argument("--slides", required=True); ap.add_argument("--callouts", required=True)
    ap.add_argument("--work", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--subs", help="folder with subs-chunks.json and the subsNN.webm renders (text layer, laid last)")
    ap.add_argument("--crf", default="20")
    ap.add_argument("--only-window", help="START,END in output seconds: render just that slice (for checks)")
    a = ap.parse_args()
    L = json.load(open(a.layers)); work = Path(a.work); work.mkdir(parents=True, exist_ok=True)
    slides, callouts = L["slides"], L["callouts"]

    m = Image.new("L", (HW, HH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, HW - 1, HH - 1), radius=28, fill=255)
    m.save(work / "headmask.png")
    inputs = ["-i", str(a.base), "-loop", "1", "-framerate", "24", "-i", str(work / "headmask.png")]
    rhs = L.get("layout") == "rhs_all"                  # speaker small on the right for every section, white canvas throughout
    if rhs:
        Image.new("RGB", (1920, 1080), BG["white"]).save(work / "bg.png")
        inputs += ["-loop", "1", "-framerate", "24", "-i", str(work / "bg.png")]
    first = 3 if rhs else 2
    for k, s in enumerate(slides):
        p = work / f"slide{k + 1:02d}.png"
        canvas(Path(a.slides) / s["file"], s["bg"], p)
        inputs += ["-loop", "1", "-framerate", "24", "-i", str(p)]
    first_call = first + len(slides)
    for c in callouts:
        inputs += ["-c:v", "libvpx-vp9", "-i", str(Path(a.callouts) / f"{c['id']}.webm")]

    chunks = json.load(open(Path(a.subs) / "subs-chunks.json")) if a.subs else []
    first_sub = first_call + len(callouts)
    for ch in chunks:
        inputs += ["-c:v", "libvpx-vp9", "-i", str(Path(a.subs) / ch["file"])]

    fc = ["[0:v]split=2[base][hsrc]",
          f"[hsrc]crop=960:1080:480:0,scale={HW}:{HH},format=rgba[hs]",
          f"[1:v]format=gray,scale={HW}:{HH}[mk]", "[hs][mk]alphamerge[head]"]
    cur = "[base]"
    if rhs:
        fc.append("[base][2:v]overlay=0:0:shortest=0[bgv]"); cur = "[bgv]"
    for k, s in enumerate(slides):                       # 0.3 s fades in and out, so a slide never flashes on or off
        fc.append(f"[{k + first}:v]format=rgba,fade=t=in:st={s['out_in']}:d=0.3:alpha=1,fade=t=out:st={s['out_out'] - 0.3:.3f}:d=0.3:alpha=1[sf{k}]")
        fc.append(f"{cur}[sf{k}]overlay=0:0:enable='between(t,{s['out_in']},{s['out_out'] + 0.01})':shortest=0[v{k}]")
        cur = f"[v{k}]"
    en = "+".join(f"between(t,{s['out_in']},{s['out_out']})" for s in slides)
    fc.append(f"{cur}[head]overlay={HX}:{HY}" + ("" if rhs else f":enable='{en}'") + ":shortest=0[vp]")
    cur = "[vp]"
    for k, c in enumerate(callouts):
        i = first_call + k
        x, y = c["box"][0], c["box"][1]
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS+{c['out_in']}/TB,format=yuva420p[co{k}]")
        fc.append(f"{cur}[co{k}]overlay={x}:{y}:eof_action=pass[vc{k}]")
        cur = f"[vc{k}]"
    for k, ch in enumerate(chunks):                      # subtitles LAST (SOP hard rule 1); strip 1920x220 sits at y 860
        i = first_sub + k
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS+{ch['start']}/TB,format=yuva420p[sb{k}]")
        fc.append(f"{cur}[sb{k}]overlay=0:860:eof_action=pass[vs{k}]")
        cur = f"[vs{k}]"
    fc.append(f"{cur}format=yuv420p[vout]")
    script = work / "filter.txt"; script.write_text(";\n".join(fc))

    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(a.base)],
                         capture_output=True, text=True).stdout.strip()
    win = []
    if a.only_window:
        s0, s1 = (float(v) for v in a.only_window.split(","))
        win = ["-ss", f"{s0}", "-t", f"{s1 - s0}"]
    cmd = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *inputs, "-filter_complex_script", str(script),
           "-map", "[vout]", "-map", "0:a", *win, "-t", dur if not win else win[3], "-c:v", "libx264", "-preset", "medium",
           "-crf", a.crf, "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "copy", "-movflags", "+faststart", str(a.out)]
    json.dump([[s["out_in"], s["out_out"]] for s in slides], open(work / "windows.json", "w"))
    print(f"{len(slides)} slides, {len(callouts)} callouts -> {a.out}")
    subprocess.run(cmd, check=True)
    print("done")


if __name__ == "__main__":
    sys.exit(main())
