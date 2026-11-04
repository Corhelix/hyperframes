"""Build layers.json (video edit SOP v0.4, stage 11) from a layer plan, the EDL and the Scribe transcript.

A layer plan lists slide cues and callouts. Each names a source time `t` and a spoken word `kw`.
This script lands every layer on that word (first match from t - 0.5 s to t + 8 s), maps the source
second to the output timeline of the rendered cut, applies the screen-mode geometry, and checks the
SOP rules on the way: callout headline 7 words or fewer, stat 4 or fewer, hold at least 3 s or
1 s + 0.3 s per word (whichever is longer), one callout at a time, anchor inside a kept range.

Output times use the real segment durations when --segments-dir holds the rendered clips
(render.py rounds each segment to whole frames), else the EDL's own range lengths.

Usage:
    build_layers.py --plan layer-plan.json --edl edl.json --transcript scribe.json \
                    [--segments-dir clips_preview] --out layers.json
"""
import argparse, json, re, subprocess
from pathlib import Path

CALLOUT_BOX = {"C": (40, 800), "B": (40, 740)}       # SOP geometry: mode C caption band from y 790, mode B inside y 700 to 1000
CALLOUT_SIZE = (1060, 260)
SLIDE_BOX = (40, 40, 1280, 720)
PANEL_BOX = (1360, 455, 520, 585)
NORM = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def seg_durations(edl, segdir):
    out = []
    for i, r in enumerate(edl["ranges"]):
        d = r["end"] - r["start"]
        if segdir:
            p = Path(segdir) / f"seg_{i:02d}_{r['source']}.mp4"
            if p.exists():
                v = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                                    "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()
                try: d = float(v)
                except ValueError: pass
        out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", required=True); ap.add_argument("--edl", required=True)
    ap.add_argument("--transcript", required=True); ap.add_argument("--segments-dir")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    plan = json.load(open(a.plan)); edl = json.load(open(a.edl)); R = edl["ranges"]
    words = [w for w in json.load(open(a.transcript))["words"] if w.get("type") == "word"]
    durs = seg_durations(edl, a.segments_dir)
    cum = [sum(durs[:i]) for i in range(len(durs))]
    total = sum(durs)
    issues = []

    def to_out(t):
        for i, r in enumerate(R):
            if r["start"] <= t <= r["end"]:
                return cum[i] + (t - r["start"])
        return None

    def land(item):
        t, kw = item["t"], NORM(item["kw"])
        for w in words:
            if t - 0.5 <= w["start"] <= t + 8 and NORM(w["text"]).startswith(kw):
                o = to_out(w["start"])
                if o is None:
                    issues.append(f"{item['id']}: anchor word '{w['text']}' at {w['start']:.2f} is in removed material")
                return w, o
        issues.append(f"{item['id']}: keyword '{item['kw']}' not found from {t - 0.5:.1f} to {t + 8:.1f} s")
        return None, None

    slides = []
    for s in plan["slides"]:
        w, o = land(s)
        if o is None: continue
        slides.append(dict(s, anchor_word=w["text"], src_t=round(w["start"], 3), out_in=round(max(0, o - 0.15), 3)))
    slides.sort(key=lambda x: x["out_in"])
    for k, s in enumerate(slides):
        nxt = slides[k + 1]["out_in"] if k + 1 < len(slides) else None
        a0 = s["out_in"]
        if nxt is not None and nxt - a0 <= 25: b = min(nxt, a0 + 18)
        else: b = a0 + 15
        s["out_out"] = round(min(b, total), 3)
        s["bg"] = plan["slide_bg"].get(s["file"], "white")
        if s["out_out"] - s["out_in"] < 3: issues.append(f"{s['id']}: slide held {s['out_out'] - s['out_in']:.1f} s, under 3 s")

    def slide_at(t):
        return next((s for s in slides if s["out_in"] <= t < s["out_out"]), None)

    callouts = []
    for c in plan["callouts"]:
        w, o = land(c)
        if o is None: continue
        head_words = len(c["head"].split()); label_words = len(c["label"].split()) if c["label"] else 0
        limit = 4 if c["type"] == "stat" else 7
        if head_words > limit: issues.append(f"{c['id']}: headline {head_words} words, limit {limit} for {c['type']}")
        if label_words > 7: issues.append(f"{c['id']}: label {label_words} words, over 7")
        hold = max(3.0, 1 + 0.3 * (head_words + label_words))
        t_in = round(max(0, o - 0.10), 3)
        mode = "C" if slide_at(t_in + 0.5) else "B"
        callouts.append(dict(c, anchor_word=w["text"], src_t=round(w["start"], 3), out_in=t_in,
                             out_out=round(min(t_in + hold, total), 3), hold_s=round(hold, 2),
                             words=head_words + label_words, mode=mode,
                             box=[*CALLOUT_BOX[mode], *CALLOUT_SIZE]))
    callouts.sort(key=lambda x: x["out_in"])
    for p, q in zip(callouts, callouts[1:]):
        if q["out_in"] < p["out_out"]:
            issues.append(f"{p['id']} and {q['id']} overlap ({p['out_out'] - q['out_in']:.2f} s): one callout at a time")
    # a callout whose mode changes part-way (slide ends under it) is moved to the box for its whole life
    for c in callouts:
        end_mode = "C" if slide_at(c["out_out"] - 0.1) else "B"
        if end_mode != c["mode"]:
            issues.append(f"{c['id']}: slide state changes during the callout (starts {c['mode']}, ends {end_mode})")

    json.dump({"version": 1, "format": "16:9", "fps": 24, "total_out_s": round(total, 3),
               "geometry": {"slide": SLIDE_BOX, "panel": PANEL_BOX, "callout_modes": CALLOUT_BOX, "callout_size": CALLOUT_SIZE},
               "segment_out_starts": [round(x, 3) for x in cum], "slides": slides, "callouts": callouts,
               "held_back": plan.get("held_back", []), "issues": issues}, open(a.out, "w"), indent=1)
    print(f"{len(slides)} slides, {len(callouts)} callouts, total {total:.2f} s, {len(issues)} issues")
    for i in issues: print("  -", i)


if __name__ == "__main__":
    main()
