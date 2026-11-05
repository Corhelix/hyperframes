"""Sentence packets for the edit pass (SOP stage 11, beats to visuals).

Maps the Scribe words through the EDL to output time, splits them into sentences, and attaches what is on
screen at each sentence (from a shots list of rendered stills), so an editor works sentence by sentence:
what is he saying, and out of the whole library what best shows it.

  python edit_pass_packets.py --transcript <scribe.json> --edl <edl.json> --out <dir>
                              [--shots <shots.json>] [--split 0,195,395,592]

Writes <out>/partN.json: [{start, end, text, words: [[t, word], ...], on_screen: [...]}].
"""
import argparse
import json
import os
import re

ap = argparse.ArgumentParser()
ap.add_argument("--transcript", required=True)
ap.add_argument("--edl", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--shots")
ap.add_argument("--split", default="0")
a = ap.parse_args()

words_in = json.load(open(a.transcript, encoding="utf-8"))["words"]
ranges = json.load(open(a.edl, encoding="utf-8"))["ranges"]
words, cum = [], 0.0
for r in ranges:
    for w in words_in:
        if w.get("type") == "word" and r["start"] <= w["start"] < r["end"]:
            words.append([round(cum + w["start"] - r["start"], 2), w["text"]])
    cum += r["end"] - r["start"]

sents, cur = [], []
for w in words:
    cur.append(w)
    if re.search(r"[.?!]$", w[1]):
        sents.append(cur)
        cur = []
if cur:
    sents.append(cur)

shots = json.load(open(a.shots, encoding="utf-8")) if a.shots else []


def on_screen(s, e):
    return [{"still": x["scene"], "type": x["type"], "span": x["span"], "still_path": x.get("file")}
            for x in shots if x["span"][0] < e and x["span"][1] > s]


cuts = [float(x) for x in a.split.split(",")] + [cum + 1]
os.makedirs(a.out, exist_ok=True)
for i in range(len(cuts) - 1):
    part = []
    for s in sents:
        st, en = s[0][0], round(s[-1][0] + 0.4, 2)
        if cuts[i] <= st < cuts[i + 1]:
            part.append({"start": st, "end": en, "text": " ".join(w[1] for w in s), "words": s, "on_screen": on_screen(st, en)})
    json.dump(part, open(os.path.join(a.out, f"part{i + 1}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"part{i + 1}: {len(part)} sentences")
