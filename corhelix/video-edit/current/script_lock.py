#!/usr/bin/env python3
"""Script lock: the cut gate for SOP stages 05 to 07.

The script (the speaker's own words, as transcribed) is the authority. Every span of the
recording that the EDL leaves out must be one of:

  redo        a repeated take: the speaker restarts with the same opening words, usually after
              saying "redo". The only cut that needs no sign-off.
  splice      silence no longer than --silence-tol, which is padding at a join, not an edit.
  authorised  covered by an entry in authorisations.json that carries Andrew's own words.

Anything else is reported as an unauthorised cut and the check fails. It also fails on a range
edge inside a word, and on ranges that run out of order (the script is never reordered).

Usage:
  script_lock.py --transcript T.json --edl edl.json [--source A] \
                 [--authorisations cuts/authorisations.json] [--report cuts/script-lock.json]

Exit codes: 0 pass, 1 findings, 2 bad input.

authorisations.json:
  [{"start": 12.4, "end": 15.1, "authorised_by": "Andrew",
    "quote": "cut that bit about the invoice", "reason": "aside"}]
"""
import argparse
import json
import re
import sys

TOL = 0.06            # seconds: a range edge this close to a word edge counts as on it
REDO_MIN_WORDS = 3    # opening words that must repeat when the speaker gave no cue
CUES = {"redo"}       # spoken cue words
SILENCE_TOL = 0.3     # seconds of pure silence treated as join padding (confirmed by Andrew, 5 Nov 2026)


def norm(text):
    return re.sub(r"[^a-z0-9']+", "", text.lower())


def mid(w):
    return (w["start"] + w["end"]) / 2


def is_redo(removed, kept):
    """removed: texts of the words in the cut span. kept: texts of the words that follow it."""
    rn = [x for x in (norm(t) for t in removed) if x]
    kn = [x for x in (norm(t) for t in kept) if x]
    cue_at = max((i for i, x in enumerate(rn) if x in CUES), default=None)
    take = rn[:cue_at] if cue_at is not None else rn
    if cue_at is not None and not take:
        return True, "cue word only"
    m = 0
    while m < len(take) and m < len(kn) and take[m] == kn[m]:
        m += 1
    need = min(REDO_MIN_WORDS, len(take)) if cue_at is not None else REDO_MIN_WORDS
    if need >= 1 and m >= need:
        how = "after a redo cue" if cue_at is not None else "no cue"
        return True, "%d opening words repeat (%s)" % (m, how)
    return False, "opening words do not repeat in the kept take"


def removed_spans(ranges, duration):
    spans, prev_end = [], 0.0
    for r in sorted(ranges, key=lambda r: r["start"]):
        if r["start"] - prev_end > TOL:
            spans.append((prev_end, r["start"]))
        prev_end = max(prev_end, r["end"])
    if duration - prev_end > TOL:
        spans.append((prev_end, duration))
    return spans


def covering(auths, span):
    for a in auths:
        if a["start"] <= span[0] + TOL and a["end"] >= span[1] - TOL:
            return a
    return None


def check(words, ranges, duration, auths=None, silence_tol=SILENCE_TOL):
    auths = auths or []
    ws = [w for w in words if w.get("type") == "word"]
    findings, spans = [], []

    for a in auths:
        if a.get("authorised_by") != "Andrew" or not str(a.get("quote", "")).strip():
            findings.append({"kind": "bad_authorisation", "start": a.get("start"), "end": a.get("end"),
                             "detail": "an authorisation needs authorised_by 'Andrew' and his own words in quote"})
    good = [a for a in auths if a.get("authorised_by") == "Andrew" and str(a.get("quote", "")).strip()]

    for i in range(1, len(ranges)):
        if ranges[i]["start"] < ranges[i - 1]["end"] - TOL:
            findings.append({"kind": "out_of_order", "start": ranges[i]["start"], "end": ranges[i]["end"],
                             "detail": "range %d starts before range %d ends; the script is never reordered" % (i, i - 1)})

    for n, r in enumerate(ranges):
        for edge in ("start", "end"):
            t = r[edge]
            for w in ws:
                if w["start"] + TOL < t < w["end"] - TOL:
                    findings.append({"kind": "cut_inside_word", "start": t, "end": t,
                                     "detail": "range %d %s lands inside '%s' (%.2f to %.2f)" % (n, edge, w["text"], w["start"], w["end"])})

    for s in removed_spans(ranges, duration):
        inside = [w for w in ws if s[0] <= mid(w) < s[1]]
        after = [w for w in ws if mid(w) >= s[1]][:8]
        text = " ".join(w["text"] for w in inside)
        row = {"start": round(s[0], 3), "end": round(s[1], 3), "text": text}
        if not inside and s[1] - s[0] <= silence_tol:
            row.update(decision="splice", why="silence of %.2f s, join padding" % (s[1] - s[0]))
        else:
            ok, why = is_redo([w["text"] for w in inside], [w["text"] for w in after]) if inside else (False, "")
            a = None if ok else covering(good, s)
            if ok:
                row.update(decision="redo", why=why)
            elif a:
                row.update(decision="authorised", why='Andrew: "%s"' % a["quote"])
            else:
                kind = "silence" if not inside else "words"
                row.update(decision="UNAUTHORISED", why="no redo and no authorisation covers this %s" % kind)
                findings.append({"kind": "unauthorised_cut", "start": row["start"], "end": row["end"],
                                 "detail": "%.2f s removed%s" % (s[1] - s[0], (": " + text) if text else " (silence)")})
        spans.append(row)

    return {"passed": not findings, "spans": spans, "findings": findings}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--transcript", required=True)
    p.add_argument("--edl", required=True)
    p.add_argument("--source", help="EDL source id to check (default: the first source)")
    p.add_argument("--authorisations")
    p.add_argument("--report")
    p.add_argument("--silence-tol", type=float, default=SILENCE_TOL)
    a = p.parse_args(argv)
    try:
        tr = json.load(open(a.transcript))
        edl = json.load(open(a.edl))
        auths = json.load(open(a.authorisations)) if a.authorisations else []
        src = a.source or next(iter(edl["sources"]))
        ranges = [r for r in edl["ranges"] if r["source"] == src]
        words = tr["words"]
        duration = tr.get("audio_duration_secs") or max(w["end"] for w in words)
    except (OSError, KeyError, ValueError, StopIteration) as e:
        print("bad input: %s" % e, file=sys.stderr)
        return 2
    res = check(words, ranges, duration, auths, a.silence_tol)
    for s in res["spans"]:
        print("%8.2f -> %8.2f  %-12s %s" % (s["start"], s["end"], s["decision"], s["why"]))
    for f in res["findings"]:
        print("FAIL %s: %s" % (f["kind"], f["detail"]))
    print("PASS" if res["passed"] else "FAIL: %d finding(s)" % len(res["findings"]))
    if a.report:
        json.dump(res, open(a.report, "w"), indent=1)
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
