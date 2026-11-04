"""Subtitles for the cut (video edit SOP v0.4, stages 11 and 12): subtitles.json, captions.srt and
Hyperframes text-layer renders.

Cue rules follow the N8n tool's build_cues: about 5 words a cue, a cue never spans a cut, a break at
sentence end or a longer gap, a short cue folds into its neighbour inside the same kept range.
Times are on the output timeline of the rendered cut (real segment durations from layers.json).
Cleaning, all logged in subtitles.json: fillers dropped, cut-off fragments dropped, stutter prefixes
resolved ("digi-digital" to "digital"), immediate repeats collapsed, brand fixes, Australian spelling.
captions.srt carries every cue. The text layer skips a cue while a callout is on screen, so a
subtitle never overlaps a callout, a slide or the speaker panel.

Usage:
    build_subtitles.py --layers layers.json --edl edl.json --transcript scribe.json \
                       --tools-dir TOOLS --data-out DIR --render-out DIR [--no-render] [--workers 3]
Writes DATA/subtitles.json, DATA/captions.srt, RENDER/hf/subsNN/ and RENDER/subsNN.webm,
and RENDER/subs-chunks.json (file, start offset) for compose.py.
"""
import argparse, html, json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILLERS = {"uh", "um", "er", "erm", "ah", "hmm", "mm", "uhm", "eh"}
BRAND = {"newsxtend": "News Xtend"}
SENTENCE_END = (".", "!", "?", "…")
NORM = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def clean_tokens(words, log):
    out = []; prev = None
    for w in words:
        t = w["text"].strip()
        n = NORM(t)
        if not n or n in FILLERS:
            log["fillers"] += 1
            if out and out[-1]["text"].endswith(","):      # "I'm, um, adept" reads "I'm adept", not "I'm, adept"
                out[-1] = dict(out[-1], text=out[-1]["text"][:-1])
            continue
        if t.endswith("-") or t.startswith("-"):
            log["fragments"] += 1; continue
        m = re.match(r"^([A-Za-z]+)-([A-Za-z].*)$", t)
        if m and m.group(2).lower().startswith(m.group(1).lower()) and len(m.group(1)) < len(m.group(2)):
            t = m.group(2); n = NORM(t); log["stutters"] += 1
        if n == prev and not n.isdigit():
            log["repeats"] += 1; continue
        prev = n
        if n in BRAND:
            t = BRAND[n] + re.sub(r"^[A-Za-z0-9]+", "", t)
            log["brand"] += 1
        out.append(dict(w, text=t))
    return out


def srt_time(s):
    ms = int(round(s * 1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); sec, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def render_chunk(job):
    cue_html, dur, name, out = job
    d = Path(out) / "hf" / name; d.mkdir(parents=True, exist_ok=True)
    page = (HERE / "template.html").read_text().replace("{{DURATION}}", f"{dur:.3f}").replace("{{CUES}}", cue_html)
    (d / "index.html").write_text(page)
    (d / "meta.json").write_text(json.dumps({"id": name, "name": name}))
    (d / "hyperframes.json").write_text(json.dumps({"name": name}))
    (d / "package.json").write_text(json.dumps({"name": name, "private": True, "type": "module"}))
    lint = subprocess.run(["npx", "--yes", "hyperframes@0.9.10", "lint", str(d)], capture_output=True, text=True)
    target = Path(out) / f"{name}.webm"
    r = subprocess.run(["npx", "--yes", "hyperframes@0.9.10", "render", str(d), "--format", "webm", "--fps", "24",
                        "--output", str(target)], capture_output=True, text=True)
    return name, lint.returncode, r.returncode == 0 and target.exists(), (lint.stdout + lint.stderr)[-300:], (r.stdout + r.stderr)[-300:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--layers", required=True); ap.add_argument("--edl", required=True)
    ap.add_argument("--transcript", required=True); ap.add_argument("--tools-dir", required=True)
    ap.add_argument("--data-out", required=True); ap.add_argument("--render-out", required=True)
    ap.add_argument("--words-per-cue", type=int, default=5); ap.add_argument("--min-words", type=int, default=3)
    ap.add_argument("--gap", type=float, default=0.7); ap.add_argument("--chunk-s", type=float, default=100.0)
    ap.add_argument("--no-render", action="store_true"); ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    sys.path.insert(0, a.tools_dir)
    from au_spelling import to_ause

    L = json.load(open(a.layers)); R = json.load(open(a.edl))["ranges"]; cum = L["segment_out_starts"]
    words = [w for w in json.load(open(a.transcript))["words"] if w.get("type") == "word"]
    log = dict(fillers=0, fragments=0, stutters=0, repeats=0, brand=0)

    def locate(t):
        for i, r in enumerate(R):
            if r["start"] <= t <= r["end"]: return i, cum[i] + (t - r["start"])
        return None, None

    kept = []
    for w in words:
        i, o = locate(w["start"])
        if i is None: continue
        _, oe = locate(min(w["end"], R[i]["end"]))
        kept.append(dict(w, keep=i, o_in=o, o_out=max(oe, o + 0.02)))
    kept = clean_tokens(kept, log)

    cues, cur = [], None
    for w in kept:
        brk = (cur is None or cur["keep"] != w["keep"] or len(cur["w"]) >= a.words_per_cue or cur["ended"]
               or w["o_in"] - cur["o_out"] > a.gap)
        if brk:
            if cur: cues.append(cur)
            cur = dict(w=[w["text"]], keep=w["keep"], o_in=w["o_in"], o_out=w["o_out"], ended=w["text"].endswith(SENTENCE_END))
        else:
            cur["w"].append(w["text"]); cur["o_out"] = w["o_out"]; cur["ended"] = w["text"].endswith(SENTENCE_END)
    if cur: cues.append(cur)
    merged = []
    for c in cues:
        if merged and len(c["w"]) < a.min_words and merged[-1]["keep"] == c["keep"] and c["o_in"] - merged[-1]["o_out"] <= a.gap:
            merged[-1]["w"] += c["w"]; merged[-1]["o_out"] = c["o_out"]
        else: merged.append(c)
    cues = merged
    # a cue on screen for under 0.9 s cannot be read: fold it into the shorter neighbour in the same kept range (up to 8 words)
    changed = True
    while changed:
        changed = False
        for k, c in enumerate(cues):
            if c["o_out"] - c["o_in"] >= 0.9: continue
            opts = []
            if k > 0 and cues[k - 1]["keep"] == c["keep"] and len(cues[k - 1]["w"]) + len(c["w"]) <= 8: opts.append(k - 1)
            if k + 1 < len(cues) and cues[k + 1]["keep"] == c["keep"] and len(cues[k + 1]["w"]) + len(c["w"]) <= 8: opts.append(k + 1)
            if not opts: continue
            j = min(opts, key=lambda x: len(cues[x]["w"]))
            a_, b_ = (cues[j], c) if j < k else (c, cues[j])
            a_["w"] = a_["w"] + b_["w"]; a_["o_out"] = b_["o_out"]; a_["ended"] = b_["ended"]
            cues.pop(k if j < k else k + 1)
            changed = True
            break
    for k, c in enumerate(cues):
        nxt = cues[k + 1]["o_in"] if k + 1 < len(cues) else 1e9
        seg_end = cum[c["keep"]] + (R[c["keep"]]["end"] - R[c["keep"]]["start"])
        c["out"] = round(max(c["o_out"] + 0.25, c["o_in"] + 0.8), 3)
        c["out"] = round(min(c["out"], nxt - 0.02, seg_end), 3)
        c["in"] = round(c["o_in"], 3)
        c["text"] = re.sub(r"[,;:]+$", "", to_ause(" ".join(c["w"])).strip())

    slides, callouts = L["slides"], L["callouts"]
    out = []
    for k, c in enumerate(cues):
        mode = "c" if any(s["out_in"] <= c["in"] < s["out_out"] for s in slides) else "a"
        hit = next((x["id"] for x in callouts if c["in"] < x["out_out"] and c["out"] > x["out_in"]), None)
        out.append(dict(id=f"T{k + 1:03d}", text=c["text"], out_in=c["in"], out_out=c["out"], position=mode,
                        words=len(c["w"]), suppressed_by=hit))
    Path(a.data_out).mkdir(parents=True, exist_ok=True)
    json.dump({"version": 1, "rules": "5 words a cue, no cue across a cut, fillers and cut-off fragments dropped, "
               "immediate repeats collapsed, brand fix News Xtend, Australian spelling; text layer skips cues under a callout",
               "cleaning": log, "cue_count": len(out), "shown_in_text_layer": sum(1 for c in out if not c["suppressed_by"]),
               "cues": out}, open(Path(a.data_out) / "subtitles.json", "w"), indent=1)
    (Path(a.data_out) / "captions.srt").write_text("\n".join(
        f"{i + 1}\n{srt_time(c['out_in'])} --> {srt_time(c['out_out'])}\n{c['text']}\n" for i, c in enumerate(out)))
    print(f"{len(out)} cues ({sum(1 for c in out if c['suppressed_by'])} skipped in the text layer under callouts); cleaning {log}")
    if a.no_render: return 0

    shown = [c for c in out if not c["suppressed_by"]]
    chunks, cur_chunk = [], []
    for c in shown:
        if cur_chunk and c["out_in"] - cur_chunk[0]["out_in"] >= a.chunk_s:
            chunks.append(cur_chunk); cur_chunk = []
        cur_chunk.append(c)
    if cur_chunk: chunks.append(cur_chunk)
    jobs, meta = [], []
    for n, ch in enumerate(chunks):
        t0 = ch[0]["out_in"]; dur = ch[-1]["out_out"] - t0 + 0.1
        cue_html = "\n".join(
            f'      <div class="clip cue {c["position"]}" data-start="{c["out_in"] - t0:.3f}" data-duration="{c["out_out"] - c["out_in"]:.3f}" '
            f'data-track-index="0"><span class="pill">{html.escape(c["text"], quote=False)}</span></div>' for c in ch)
        name = f"subs{n + 1:02d}"; jobs.append((cue_html, dur, name, a.render_out)); meta.append(dict(file=f"{name}.webm", start=round(t0, 3), duration=round(dur, 3)))
    Path(a.render_out).mkdir(parents=True, exist_ok=True)
    bad = 0
    with ThreadPoolExecutor(a.workers) as ex:
        for name, lrc, ok, lo, ro in ex.map(render_chunk, jobs):
            print(f"{name}: lint rc {lrc}, render {'ok' if ok else 'FAILED'}")
            if lrc != 0 or not ok: bad += 1; print("  lint:", lo.strip()[-250:]); print("  render:", ro.strip()[-250:])
    json.dump(meta, open(Path(a.render_out) / "subs-chunks.json", "w"), indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
