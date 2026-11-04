"""Render the callouts in layers.json as transparent WebM overlays with Hyperframes (SOP v0.4, stage 12).

For each callout it fills template.html, writes a small Hyperframes project, lints it, and renders
a transparent WebM at the cut's frame rate. Nothing is rendered into this repo: projects and
renders go to --out.

Usage:
    build_callouts.py --layers layers.json --out OUTDIR [--only C01,C02] [--fps 24] [--workers 3]
Writes OUTDIR/hf/<id>/ (the project) and OUTDIR/<id>.webm.
"""
import argparse, html, json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAGS = {"quote": "Recommendation"}


def head_px(c):
    n = len(c["head"])
    if c["type"] == "stat":
        return 80 if n <= 14 else 64 if n <= 24 else 54
    return 60 if n <= 22 else 48 if n <= 38 else 42


def make_project(c, out, fps):
    d = Path(out) / "hf" / c["id"]
    d.mkdir(parents=True, exist_ok=True)
    dur = round(c["out_out"] - c["out_in"], 3)
    head = html.escape(c["head"], quote=False)
    if c["type"] == "quote":
        head = "“" + head + "”" if not c["head"].startswith("…") else "“" + head + "”"
    page = (HERE / "template.html").read_text()
    for k, v in {"{{HEAD_PX}}": str(head_px(c)), "{{DURATION}}": f"{dur}", "{{TAG}}": TAGS.get(c["type"], ""),
                 "{{HEAD_CLASS}}": c["type"] if c["type"] in ("stat", "quote") else "",
                 "{{HEAD}}": head, "{{LABEL}}": html.escape(c.get("label", ""), quote=False)}.items():
        page = page.replace(k, v)
    (d / "index.html").write_text(page)
    (d / "meta.json").write_text(json.dumps({"id": f"callout-{c['id'].lower()}", "name": f"Callout {c['id']}"}))
    (d / "hyperframes.json").write_text(json.dumps({"name": f"callout-{c['id'].lower()}"}))
    (d / "package.json").write_text(json.dumps({"name": f"callout-{c['id'].lower()}", "private": True, "type": "module"}))
    return d, dur


def run(c, out, fps):
    d, dur = make_project(c, out, fps)
    lint = subprocess.run(["npx", "--yes", "hyperframes@0.9.10", "lint", str(d)], capture_output=True, text=True)
    target = Path(out) / f"{c['id']}.webm"
    r = subprocess.run(["npx", "--yes", "hyperframes@0.9.10", "render", str(d), "--format", "webm", "--fps", str(fps),
                        "--output", str(target)], capture_output=True, text=True)
    ok = r.returncode == 0 and target.exists()
    return c["id"], ok, lint.returncode, (lint.stdout + lint.stderr)[-400:], (r.stdout + r.stderr)[-400:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--layers", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=""); ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    L = json.load(open(a.layers))["callouts"]
    only = set(filter(None, a.only.split(",")))
    todo = [c for c in L if not only or c["id"] in only]
    Path(a.out).mkdir(parents=True, exist_ok=True)
    bad = 0
    with ThreadPoolExecutor(a.workers) as ex:
        for cid, ok, lrc, lout, rout in ex.map(lambda c: run(c, a.out, a.fps), todo):
            print(f"{cid}: lint rc {lrc}, render {'ok' if ok else 'FAILED'}")
            if lrc != 0 or not ok:
                bad += 1; print("  lint:", lout.strip()[-300:]); print("  render:", rout.strip()[-300:])
    print(f"{len(todo) - bad}/{len(todo)} callouts rendered")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
