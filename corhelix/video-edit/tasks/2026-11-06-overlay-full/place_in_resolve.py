"""Place the rendered overlay .mov files on the Resolve timeline (video edit SOP v0.4, stage 12).

Run with the davinci-resolve-mcp venv python while Resolve is open with the project loaded and the
in-app bridge running (Workspace > Scripts > resolve_bridge):

  python place_in_resolve.py --scenes scenes.json --renders F:/gravitate-video-edit/media/work/overlay/full-v0.1

What it does, all on the timeline named by --timeline (never Timeline 1):
  - imports every <id>.mov into a bin named after the renders folder
  - clears tracks V6 to V8 (the overlay's own tracks) and re-lays them:
      V6 and V7 scenes (a scene goes on V7 only when it overlaps the one before it), V8 callouts
  - switches off tracks V3 to V5 (the raw stills the overlay replaces); nothing is deleted
  - checks every placed clip's start frame and length against scenes.json and prints any mismatch
"""
import argparse
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--scenes", required=True)
ap.add_argument("--renders", required=True)
ap.add_argument("--timeline", default="Timeline 1 · beat images v0.3")
ap.add_argument("--mcp", default=os.path.expanduser("~/tools/davinci-resolve-mcp"))
a = ap.parse_args()

sys.path.insert(0, a.mcp)
from src.utils import resolve_bridge_client as bridge  # noqa: E402

scenes = json.load(open(a.scenes, encoding="utf-8"))
r = bridge.connect(require_enabled=False)
p = r.GetProjectManager().GetCurrentProject()
t = next((p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount() + 1) if p.GetTimelineByIndex(i).GetName() == a.timeline), None)
if t is None:
    sys.exit(f"no timeline named {a.timeline!r}")
p.SetCurrentTimeline(t)
mp = p.GetMediaPool()
root = mp.GetRootFolder()
bin_name = "Overlays " + os.path.basename(os.path.normpath(a.renders))
binf = next((f for f in root.GetSubFolderList() if f.GetName() == bin_name), None) or mp.AddSubFolder(root, bin_name)
mp.SetCurrentFolder(binf)

paths = [os.path.join(a.renders, s["id"] + ".mov") for s in scenes]
missing = [x for x in paths if not os.path.exists(x)]
if missing:
    print("missing renders:", [os.path.basename(x) for x in missing])
existing = {c.GetName(): c for c in (binf.GetClipList() or [])}
to_import = [x for x in paths if os.path.exists(x) and os.path.basename(x) not in existing]
if to_import:
    mp.ImportMedia(to_import)
pool = {c.GetName(): c for c in (binf.GetClipList() or [])}

while t.GetTrackCount("video") < 8:
    t.AddTrack("video")
for k, name in ((6, "Overlay scenes A"), (7, "Overlay scenes B"), (8, "Callouts")):
    t.SetTrackName("video", k, name)
    old = t.GetItemListInTrack("video", k) or []
    if old:
        t.DeleteClips(old)
for k in (3, 4, 5):
    try:
        t.SetTrackEnable("video", k, False)
    except Exception:
        for c in t.GetItemListInTrack("video", k) or []:
            c.SetClipEnabled(False)

end_a = 0
plan = []
for s in scenes:
    it = pool.get(s["id"] + ".mov")
    if it is None:
        continue
    frames = round(s["dur"] * 24)
    if s["track"] == "callout":
        tr = 8
    else:
        tr = 6 if s["frame"] >= end_a else 7
        if tr == 6:
            end_a = s["frame"] + frames
    res = mp.AppendToTimeline([{"mediaPoolItem": it, "trackIndex": tr, "recordFrame": s["frame"], "mediaType": 1}])
    if not res:
        print("append failed", s["id"])
        continue
    plan.append((s["id"], tr, s["frame"], frames))

placed = {}
for tr in (6, 7, 8):
    for c in t.GetItemListInTrack("video", tr) or []:
        placed[(tr, c.GetStart())] = (c.GetName(), c.GetDuration())
bad = [(sid, tr, f, n, placed.get((tr, f))) for sid, tr, f, n in plan if not placed.get((tr, f)) or abs(placed[(tr, f)][1] - n) > 1]
print(f"placed {len(plan)} of {len(scenes)} | V6 {sum(1 for x in plan if x[1]==6)} V7 {sum(1 for x in plan if x[1]==7)} V8 {sum(1 for x in plan if x[1]==8)} | mismatches {len(bad)}")
for b in bad:
    print("  MISMATCH", b)
