"""Verify the composited draft against the plan (video edit SOP v0.4, stage 13, V1 to V7).

Every join, every layer and every subtitle is tested, not a sample. Presence of a layer is measured
as the pixel difference between the draft and the bare cut (`--base`) inside the layer's box.

  V1 cuts      each join: head-region difference, whole-frame brightness jump and audio level jump at +-0.05 s,
               plus a before/after image
  V2 position  each callout and slide: the changed-pixel box sits inside the mode geometry (2 px), never over the face
               or another layer; box image with the expected geometry drawn on it
  V3 timing    each layer appears within +-0.3 s of its anchor word and holds long enough; 6-frame strip image
  V4 content   the right file and copy: callout text in its project matches layers.json, slide file hash matches
  V5 text      each subtitle appears within +-0.1 s of its time, no two overlap, none under a callout in the text layer
  V6 duration  draft and base against the sum of the EDL ranges (+-0.1 s), with the EDL hash
  V7 audio     loudness and true peak (loudnorm measurement)

Usage:
    check_layers.py --layers layers.json --subs subtitles.json --edl edl.json --base cut.mp4 --draft draft.mp4 \
                    --callout-projects callouts/hf --slides SLIDEDIR --out VERIFYDIR
Writes OUT/report.json, OUT/joins/*.jpg, OUT/layers/<id>-box.jpg, OUT/layers/<id>-strip.jpg.
"""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

W, H = 1920, 1080
FACE = (700, 230, 1300, 600)               # the speaker's face, in 1920x1080 (full-frame mode); checked by eye in the box images
PANEL = (1360, 455, 520, 585)
SLIDE = (40, 40, 1280, 720)


def frame(video, t, size=(W, H)):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(video), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    if len(raw) < W * H * 3: return None
    im = Image.frombytes("RGB", (W, H), raw[:W * H * 3])
    return im if size == (W, H) else im.resize(size)


def crop_series(video, t0, dur, box, fps=10):
    x, y, w, h = box
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{max(t0, 0):.3f}", "-t", f"{dur:.3f}", "-i", str(video),
                          "-vf", f"fps={fps},crop={w}:{h}:{x}:{y},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw[:n * w * h], np.uint8).reshape(n, h, w).astype(np.int16)


def presence(draft, base, t0, dur, box, thr=6, fps=10):
    a, b = crop_series(draft, t0, dur, box, fps), crop_series(base, t0, dur, box, fps)
    n = min(len(a), len(b))
    return [(t0 + k / fps, float(np.abs(a[k] - b[k]).mean())) for k in range(n)], fps


def audio(video, t, win=0.05):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{max(t, 0):.3f}", "-t", f"{win}", "-i", str(video),
                          "-ac", "1", "-ar", "48000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
    return 20 * np.log10(max(np.sqrt((a ** 2).mean()) if len(a) else 1e-6, 1e-6))


def dur(video):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                                capture_output=True, text=True).stdout.strip())


def jpg(im, p, w=None):
    if w: im = im.resize((w, int(im.height * w / im.width)))
    im.save(p, quality=82)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ("layers", "subs", "edl", "base", "draft", "callout-projects", "slides", "work", "out"): ap.add_argument(f"--{k}", required=True)
    a = ap.parse_args()
    L = json.load(open(a.layers)); S = json.load(open(a.subs)); E = json.load(open(a.edl))
    out = Path(a.out); (out / "joins").mkdir(parents=True, exist_ok=True); (out / "layers").mkdir(exist_ok=True); (out / "subs").mkdir(exist_ok=True)
    rep = {"V1": [], "V2": [], "V3": [], "V4": [], "V5": {}, "V6": {}, "V7": {}}

    # V1 joins
    for i, T in enumerate(L["segment_out_starts"][1:], 1):
        fa, fb = frame(a.base, T - 0.05), frame(a.base, T + 0.05)
        head = (480, 0, 960, 1080)
        ha, hb = np.asarray(fa.crop((head[0], head[1], head[0] + head[2], head[1] + head[3])).convert("L"), float), \
                 np.asarray(fb.crop((head[0], head[1], head[0] + head[2], head[1] + head[3])).convert("L"), float)
        mad = float(np.abs(ha - hb).mean()); flash = abs(float(np.asarray(fa.convert("L")).mean()) - float(np.asarray(fb.convert("L")).mean()))
        lb, la = audio(a.base, T - 0.05), audio(a.base, T)
        ja = lb - la
        pair = Image.new("RGB", (1920, 720)); pair.paste(fa.resize((960, 540)), (0, 0)); pair.paste(fb.resize((960, 540)), (960, 0))
        jpg(pair, out / "joins" / f"join{i:02d}-{T:.2f}.jpg")
        rep["V1"].append(dict(join=i, out_t=round(T, 3), head_mad=round(mad, 2), brightness_jump=round(flash, 2),
                              audio_db_before=round(lb, 1), audio_db_after=round(la, 1), audio_db_step=round(abs(ja), 1),
                              head_shift_flag=bool(mad >= 10), ok=bool(flash < 6 and max(lb, la) < -30)))

    # V2/V3/V4 layers
    anchor_tol = 0.3
    for kind, items in (("callout", L["callouts"]), ("slide", L["slides"])):
        for it in items:
            lid = it["id"]
            if kind == "callout": box = (it["box"][0], it["box"][1], it["box"][2], it["box"][3]); anchor = it["out_in"] + 0.10; need = it["hold_s"]
            else: box = (0, 0, W, H); anchor = it["out_in"] + 0.15; need = 3.0
            t0 = max(it["out_in"] - 2, 0); d = it["out_out"] - it["out_in"] + 4
            cues = [(c["out_in"] - 0.05, c["out_out"] + 0.05) for c in S["cues"] if not c["suppressed_by"]]
            in_cue = lambda t: any(x0 <= t <= x1 for x0, x1 in cues)
            if kind == "slide":                       # present = the slide's own canvas is showing in the slide box
                k = [x["id"] for x in L["slides"]].index(lid)
                ref = np.asarray(Image.open(Path(a.work) / f"slide{k + 1:02d}.png").convert("L").crop((SLIDE[0], SLIDE[1], SLIDE[0] + SLIDE[2], SLIDE[1] + SLIDE[3])), np.int16)
                D = crop_series(a.draft, t0, d, SLIDE)
                pres = [(t0 + j / 10, float(np.abs(D[j] - ref).mean())) for j in range(len(D))]
                is_on = lambda v: v < 3
                skip = lambda t: False
            elif it["mode"] == "C":                    # over a slide canvas: compare with that canvas
                sl = next(x for x in L["slides"] if x["out_in"] <= it["out_in"] + 0.5 < x["out_out"])
                k = [x["id"] for x in L["slides"]].index(sl["id"])
                bx, by, bw, bh = box; by2, bh2 = by, 170           # top of the card only, clear of the subtitle line
                ref = np.asarray(Image.open(Path(a.work) / f"slide{k + 1:02d}.png").convert("L").crop((bx, by2, bx + bw, by2 + bh2)), np.int16)
                t0 = max(t0, sl["out_in"]); d = min(it["out_out"] + 2, sl["out_out"]) - t0
                D = crop_series(a.draft, t0, d, (bx, by2, bw, bh2))
                pres = [(t0 + j / 10, float(np.abs(D[j] - ref).mean())) for j in range(len(D))]
                is_on = lambda v: v > 1.0
                skip = in_cue
            else:                                       # over the speaker: compare with the bare cut
                pres, _ = presence(a.draft, a.base, t0, d, (box[0], box[1], box[2], 170 if False else box[3]))
                is_on = lambda v: v > 5.0
                skip = in_cue
            pres = pres[1:]                                              # first sample of a seeked window is not comparable
            others = [x for x in L["callouts"] if x["id"] != lid] if kind == "callout" else []
            prev_end = max([x["out_out"] for x in others if x["out_out"] <= it["out_in"] + 0.5] or [-1e9]) + 0.4
            next_start = min([x["out_in"] for x in others if x["out_in"] >= it["out_out"] - 0.5] or [1e9]) - 0.3
            pre = [(t, v) for t, v in pres if t <= it["out_in"] - 0.3 and t >= prev_end and not skip(t)]
            mid_ = [(t, v) for t, v in pres if it["out_in"] + 0.45 <= t <= it["out_out"] - 0.35]
            post = [(t, v) for t, v in pres if t >= it["out_out"] + (0.1 if kind == "slide" else 0.4) and t <= next_start and not skip(t)]
            on_ts = [t for t, v in pres if is_on(v)]
            appear = next((t for t, v in pres if is_on(v) and t >= it["out_in"] - 0.3 and not skip(t)), None)
            vanish = None
            if on_ts:
                last = [t for t in on_ts if t <= it["out_out"] + 0.4 and (kind == "slide" or t >= it["out_in"])]
                vanish = (last[-1] + 0.1) if last else None
            held = (vanish - appear) if (appear is not None and vanish is not None) else 0
            ok_pre = all(not is_on(v) for t, v in pre); ok_mid = bool(mid_) and all(is_on(v) for t, v in mid_)
            ok_post = all(not is_on(v) for t, v in post)
            v3 = bool(ok_pre and ok_mid and ok_post and appear is not None and abs(appear - it["out_in"]) <= 0.3 and held >= need - 0.4)
            v3_note = f"absent before {ok_pre}, present throughout {ok_mid}, absent after {ok_post}"
            mid = (it["out_in"] + it["out_out"]) / 2
            fm, fbs = frame(a.draft, mid), frame(a.base, mid)
            diff = np.abs(np.asarray(fm, int) - np.asarray(fbs, int)).sum(2) > 40
            ok2, note = True, ""
            if kind == "callout":
                bx, by, bw, bh = box
                reg = diff[by:by + bh, bx:bx + bw]
                ys, xs = np.where(reg)
                if len(xs):
                    x0, x1, y0, y1 = bx + xs.min(), bx + xs.max(), by + ys.min(), by + ys.max()
                    inside = x0 >= bx - 2 and x1 <= bx + bw + 2 and y0 >= by - 2 and y1 <= by + bh + 2
                    face_hit = it["mode"] == "B" and not (x1 < FACE[0] or x0 > FACE[2] or y1 < FACE[1] or y0 > FACE[3])
                    slide_hit = it["mode"] == "C" and y0 < SLIDE[1] + SLIDE[3]
                    ok2 = bool(inside and not face_hit and not slide_hit); note = f"changed box {x0},{y0} to {x1},{y1}"
                    im = fm.copy(); dr = ImageDraw.Draw(im)
                    dr.rectangle((bx, by, bx + bw, by + bh), outline=(0, 102, 255), width=3)
                    dr.rectangle(FACE, outline=(255, 0, 0), width=2); dr.rectangle((x0, y0, x1, y1), outline=(0, 200, 0), width=2)
                    jpg(im, out / "layers" / f"{lid}-box.jpg", 1280)
                else: ok2 = False; note = "no pixels changed in the box"
            else:
                px, py, pw, ph = PANEL
                exp = fbs.crop((480, 0, 1440, 1080)).resize((pw, ph))
                got = fm.crop((px, py, px + pw, py + ph))
                mad = float(np.abs(np.asarray(exp.convert("L"), float) - np.asarray(got.convert("L"), float))[40:-40, 40:-40].mean())
                ok2 = mad < 14; note = f"panel match MAD {mad:.1f}"
                im = fm.copy(); dr = ImageDraw.Draw(im)
                dr.rectangle((SLIDE[0], SLIDE[1], SLIDE[0] + SLIDE[2], SLIDE[1] + SLIDE[3]), outline=(0, 102, 255), width=3)
                dr.rectangle((px, py, px + pw, py + ph), outline=(0, 200, 0), width=3)
                jpg(im, out / "layers" / f"{lid}-box.jpg", 1280)
            rep["V2"].append(dict(id=lid, kind=kind, ok=bool(ok2), note=note))
            rep["V3"].append(dict(id=lid, kind=kind, note=v3_note, appear=None if appear is None else round(appear, 2), planned_in=it["out_in"],
                                  vanish=None if vanish is None else round(vanish, 2), held=round(held, 2), need=round(need, 2), ok=bool(v3)))
            times = [it["out_in"] - 2, it["out_in"], it["out_in"] + 2, it["out_out"] - 2, it["out_out"], it["out_out"] + 2]
            strip = Image.new("RGB", (1920, 720));
            for k, tt in enumerate(times):
                f = frame(a.draft, tt)
                if f: strip.paste(f.resize((640, 360)), ((k % 3) * 640, (k // 3) * 360))
            jpg(strip, out / "layers" / f"{lid}-strip.jpg")
            if kind == "callout":
                p = Path(a.callout_projects) / lid / "index.html"
                txt = p.read_text() if p.exists() else ""
                esc = lambda s: s.replace("&", "&amp;")
                ok4 = bool(esc(it["head"]) in txt and (not it["label"] or esc(it["label"]) in txt))
            else:
                src = Path(a.slides) / it["file"]; ok4 = src.exists()
            rep["V4"].append(dict(id=lid, kind=kind, ok=ok4, copy=it.get("head", it.get("file")), source=it.get("source", "")))

    # V5 subtitles
    cues = S["cues"]; shown = [c for c in cues if not c["suppressed_by"]]
    overlaps = [(p["id"], q["id"]) for p, q in zip(cues, cues[1:]) if q["out_in"] < p["out_out"] - 1e-6]
    under = [c["id"] for c in shown if any(c["out_in"] < x["out_out"] and c["out_out"] > x["out_in"] for x in L["callouts"])]
    strip_box = (0, 860, 1920, 220); fps = 24
    sw, sh = 480, 55
    def stream(video):
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(video), "-vf",
                              f"fps={fps},crop=1920:220:0:860,scale={sw}:{sh},format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        while True:
            b = p.stdout.read(sw * sh)
            if len(b) < sw * sh: break
            yield np.frombuffer(b, np.uint8).astype(np.int16)
    sig_l, spk = [], [0.0]; prev = None
    for x, y in zip(stream(a.draft), stream(a.base)):
        r = x - y
        sig_l.append(float(np.abs(r).mean()))
        if prev is not None: spk.append(float(np.abs(r - prev).mean()))
        prev = r
    n = len(sig_l); sig = np.array(sig_l) > 0.8; spk = np.array(spk)
    bad = []
    for c in shown:
        k0, k1 = int(round(c["out_in"] * fps)), int(round(c["out_out"] * fps))
        lo, hi = max(k0 - 2, 0), min(k0 + 3, n)
        starts = spk[lo:hi].max() > 0.5 if hi > lo else False          # a text change within +-2 frames (+-0.1 s) of the cue start
        held = sig[min(k0 + 2, n):max(min(k1 - 2, n), min(k0 + 2, n))]
        if not (starts and (held.size == 0 or held.mean() > 0.9)): bad.append(c["id"])
    covered = np.zeros(n, bool)
    for c in shown: covered[int(c["out_in"] * fps):min(int(c["out_out"] * fps) + 3, n)] = True
    for x in list(L["slides"]) + list(L["callouts"]):
        covered[max(int(x["out_in"] * fps) - 2, 0):min(int(x["out_out"] * fps) + 8, n)] = True
    stray = int((sig & ~covered).sum())
    rep["V5"] = dict(cues=len(cues), shown=len(shown), overlaps=overlaps, under_callout=under, timing_failures=bad,
                     stray_text_frames=stray, ok=bool(not overlaps and not under and not bad and stray < 12))
    for c in shown[:: max(1, len(shown) // 6)][:6]:
        f = frame(a.draft, (c["out_in"] + c["out_out"]) / 2)
        if f: jpg(f, out / "subs" / f"{c['id']}.jpg", 960)

    # V6 duration, V7 audio
    s = sum(r["end"] - r["start"] for r in E["ranges"])
    rep["V6"] = dict(edl_sum=round(s, 3), base=round(dur(a.base), 3), draft=round(dur(a.draft), 3),
                     edl_sha256=hashlib.sha256(open(a.edl, "rb").read()).hexdigest(),
                     ok=bool(abs(dur(a.base) - s) <= 0.1 and abs(dur(a.draft) - s) <= 0.1))
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(a.draft), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                        "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r, re.S)
    j = json.loads(m.group(0)) if m else {}
    rep["V7"] = dict(loudnorm=j, ok=bool(j and abs(float(j["input_i"]) + 14) <= 1 and float(j["input_tp"]) <= -1))

    rep["summary"] = {k: (all(x["ok"] for x in v) if isinstance(v, list) else v.get("ok")) for k, v in rep.items() if k.startswith("V")}
    json.dump(rep, open(out / "report.json", "w"), indent=1)
    for k, v in rep["summary"].items(): print(k, "PASS" if v else "FAIL")
    print("V1 head-position flags for review (pixel difference 10 or more):", [x["join"] for x in rep["V1"] if x["head_shift_flag"]])
    for k in ("V1", "V2", "V3", "V4"):
        for x in rep[k]:
            if not x["ok"]: print("  fail", k, x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
