#!/usr/bin/env python3
"""
Transcript -> clean.edl.json.

Step 1 of REQUIREMENT.md: produce the edit decision list instead of
consuming a hand-authored one. Detects dead air and filler words from
word-level timestamps and emits the keeps/cuts schema the rest of the
recipe already reads.

Conservative by default. It is easier to tighten a cut list after
watching it than to recover a moment that was removed, so the defaults
leave short pauses alone and only remove fillers that are unambiguous.

Usage:
    python3 detect_cuts.py \
        --transcript transcript.json \
        --out clean.edl.json \
        --source media/source.mp4 --fps 25

The safety property, asserted before anything is written: every word that
survives lies wholly inside a keep. A cut never lands inside a word.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from build_composition import load_json

# A gap shorter than this is word spacing, not a pause anyone hears.
WORD_SPACING = 0.25

# Unambiguous hesitation sounds. These carry no meaning and are always safe to
# remove. Words like "like", "so" and "right" are frequently load-bearing and
# are only treated as filler under --aggressive-fillers.
CLEAR_FILLERS = {"um", "uh", "erm", "er", "ah", "mm", "mmm", "hmm", "uhm", "eh"}
AMBIGUOUS_FILLERS = {"like", "so", "right", "basically", "actually", "literally"}
AMBIGUOUS_PHRASES = [("you", "know"), ("sort", "of"), ("kind", "of"), ("i", "mean")]

# Whisper emits these for music and noise. They are not speech.
NON_SPEECH = re.compile(r"^[♪-♯�\s]+$")

PUNCTUATION = ".,!?;:\"'()[]{}…-–—"


def normalise(text: str) -> str:
    return text.strip().strip(PUNCTUATION).lower()


def analyse_pacing(words: list[dict]) -> dict:
    """The speaker's own rhythm, read off the gaps between their words.

    A fixed silence threshold is arbitrary: 0.6s is a natural beat for one
    speaker and dead air for another. The gap distribution is the pacing,
    so the thresholds are derived from it rather than guessed.
    """
    gaps = sorted(b["start"] - a["end"] for a, b in zip(words, words[1:]))
    pauses = [g for g in gaps if g >= WORD_SPACING]
    if not pauses:
        return {"pauses": 0, "median": 0.0, "p90": 0.0, "longest": 0.0}

    def pct(values: list[float], q: float) -> float:
        return values[min(len(values) - 1, int(len(values) * q))]

    return {
        "pauses": len(pauses),
        "median": round(pct(pauses, 0.5), 3),
        "p90": round(pct(pauses, 0.9), 3),
        "longest": round(pauses[-1], 3),
    }


def load_words(path: Path) -> list[dict]:
    """Word-level transcript in the shape `hyperframes transcribe` writes."""
    raw = load_json(path)
    words = raw if isinstance(raw, list) else raw.get("words") or raw.get("segments") or []
    cleaned: list[dict] = []
    for word in words:
        text = str(word.get("text", ""))
        if not text.strip() or NON_SPEECH.match(text):
            continue
        try:
            start, end = float(word["start"]), float(word["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if end < start:
            start, end = end, start
        cleaned.append({"text": text.strip(), "start": start, "end": end})
    cleaned.sort(key=lambda w: w["start"])
    if not cleaned:
        raise SystemExit(
            f"No usable words in {path}. Expected [{{'text','start','end'}}, ...] "
            "as written by `hyperframes transcribe`."
        )
    return cleaned


def mark_fillers(words: list[dict], aggressive: bool) -> set[int]:
    """Indices of words to remove as filler."""
    vocabulary = CLEAR_FILLERS | (AMBIGUOUS_FILLERS if aggressive else set())
    marked = {i for i, w in enumerate(words) if normalise(w["text"]) in vocabulary}
    if aggressive:
        forms = [normalise(w["text"]) for w in words]
        for i in range(len(words) - 1):
            if (forms[i], forms[i + 1]) in AMBIGUOUS_PHRASES:
                marked.update({i, i + 1})
    return marked


def derive_thresholds(pacing: dict) -> tuple[float, float]:
    """Only obviously dead air is touched, and it is shortened, not removed.

    A pause of half a second is healthy. One or two seconds is still
    someone thinking, and cutting it is what makes an edit feel airless.
    Dead air starts well beyond that, so the floor is 2.5s and rises for
    a speaker who naturally pauses longer.

    The target is what a trimmed pause becomes: a beat this speaker
    actually uses, never silence.
    """
    # Clamped at both ends. The floor protects healthy pauses; the ceiling
    # stops a short sample, where p90 is just the longest gap, from
    # concluding that nothing is dead air.
    min_silence = min(4.0, max(2.5, pacing["p90"] * 3)) if pacing["pauses"] else 2.5
    target = min(1.2, max(0.6, pacing["median"] * 2)) if pacing["pauses"] else 0.8
    return round(min_silence, 3), round(target, 3)


def build_removals(
    words: list[dict],
    fillers: set[int],
    min_silence: float,
    extent: float,
    pause_target: float,
) -> list[dict]:
    """Intervals to remove, before any padding or merging.

    A long pause is shortened to `pause_target`, not deleted. Removing it
    outright is the difference between a tight edit and an airless one.
    """
    removals: list[dict] = []

    for index in sorted(fillers):
        removals.append({"start": words[index]["start"], "end": words[index]["end"], "reason": "filler"})

    # Head and tail have nothing to breathe against, so they go entirely
    # bar a short lead-in.
    head = words[0]["start"]
    if head >= min_silence:
        removals.append({"start": 0.0, "end": max(0.0, head - pause_target), "reason": "silence"})

    for current, following in zip(words, words[1:]):
        gap = following["start"] - current["end"]
        if gap >= min_silence:
            slack = (gap - pause_target) / 2
            removals.append(
                {
                    "start": current["end"] + slack,
                    "end": following["start"] - slack,
                    "reason": "pace",
                }
            )

    tail = extent - words[-1]["end"]
    if tail >= min_silence:
        removals.append(
            {"start": words[-1]["end"] + pause_target, "end": extent, "reason": "silence"}
        )

    removals.sort(key=lambda r: r["start"])
    merged: list[dict] = []
    for interval in removals:
        if merged and interval["start"] <= merged[-1]["end"] + 1e-9:
            merged[-1]["end"] = max(merged[-1]["end"], interval["end"])
            if interval["reason"] == "filler":
                merged[-1]["reason"] = "filler"
        else:
            merged.append(dict(interval))
    return merged


def complement(removals: list[dict], extent: float) -> list[dict]:
    keeps: list[dict] = []
    cursor = 0.0
    for interval in removals:
        if interval["start"] > cursor + 1e-9:
            keeps.append({"start": cursor, "end": interval["start"]})
        cursor = max(cursor, interval["end"])
    if extent > cursor + 1e-9:
        keeps.append({"start": cursor, "end": extent})
    return keeps


def apply_padding(keeps: list[dict], removals: list[dict], pad: float, extent: float) -> None:
    """Give each keep a little air so consonants are not clipped.

    Whisper places word boundaries slightly inside the audio, so cutting
    exactly on them shaves the start of a word. Padding never takes more
    than 40% of the adjacent removal from either side, so a filler cannot
    be padded back into audibility.
    """
    if pad <= 0:
        return
    gaps = {round(r["start"], 6): r for r in removals}
    ends = {round(r["end"], 6): r for r in removals}
    for keep in keeps:
        before = ends.get(round(keep["start"], 6))
        # A paced gap already carries its air; padding into it would undo
        # the shortening and re-open the dead space.
        room = 0.0 if before and before["reason"] == "pace" else (
            (before["end"] - before["start"]) * 0.4 if before else keep["start"]
        )
        keep["start"] = max(0.0, keep["start"] - min(pad, room))
        after = gaps.get(round(keep["end"], 6))
        room = 0.0 if after and after["reason"] == "pace" else (
            (after["end"] - after["start"]) * 0.4 if after else extent - keep["end"]
        )
        keep["end"] = min(extent, keep["end"] + min(pad, room))


def drop_wordless_keeps(keeps: list[dict], words: list[dict], fillers: set[int]) -> list[dict]:
    """A section with no surviving speech in it is not a section.

    Two fillers close together leave a sliver of dead air between them.
    Without this it survives as a keep, and the edit gains a fragment
    that holds nothing.
    """
    surviving = [w for i, w in enumerate(words) if i not in fillers]
    return [
        k
        for k in keeps
        if any(w["start"] >= k["start"] - 1e-6 and w["end"] <= k["end"] + 1e-6 for w in surviving)
    ]


def merge_short_gaps(keeps: list[dict], removals: list[dict], min_gap: float) -> list[dict]:
    """Collapse a cut that is too short to be worth making.

    Only silence removals are collapsed. A filler is always worth cutting
    however brief it is, otherwise the "um" stays audible.
    """
    filler_spans = [(r["start"], r["end"]) for r in removals if r["reason"] == "filler"]
    merged = [dict(keeps[0])] if keeps else []
    for keep in keeps[1:]:
        gap = keep["start"] - merged[-1]["end"]
        spans_filler = any(
            s < keep["start"] + 1e-9 and e > merged[-1]["end"] - 1e-9 for s, e in filler_spans
        )
        if gap < min_gap and not spans_filler:
            merged[-1]["end"] = keep["end"]
        else:
            merged.append(dict(keep))
    return merged


def label_cuts(keeps: list[dict], removals: list[dict], extent: float) -> list[dict]:
    cuts = []
    for interval in complement(keeps, extent):
        overlapping = [
            r for r in removals if r["start"] < interval["end"] and r["end"] > interval["start"]
        ]
        reason = "filler" if any(r["reason"] == "filler" for r in overlapping) else "silence"
        cuts.append(
            {
                "start": round(interval["start"], 3),
                "end": round(interval["end"], 3),
                "reason": reason,
            }
        )
    return cuts


def assert_no_mid_word_cuts(keeps: list[dict], words: list[dict], fillers: set[int]) -> None:
    """Every surviving word lies wholly inside a keep.

    This is the property the whole step is judged on. A cut that lands
    inside a word clips a consonant, and no amount of downstream care
    recovers it.
    """
    offences = []
    for index, word in enumerate(words):
        if index in fillers:
            continue
        inside = any(
            k["start"] <= word["start"] + 1e-6 and k["end"] >= word["end"] - 1e-6 for k in keeps
        )
        if not inside:
            offences.append(f'{word["text"]!r} at {word["start"]:.3f}-{word["end"]:.3f}')
    if offences:
        raise SystemExit(
            "Refusing to write: "
            f"{len(offences)} surviving word(s) are split by a cut. First: {offences[0]}. "
            "This is a bug in detection, not a tuning problem."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect cuts from a word-level transcript.")
    parser.add_argument("--transcript", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--source", help="Media path recorded in the EDL for downstream steps.")
    parser.add_argument("--fps", default="25", help="Recorded in the EDL. Detection is rate-free.")
    parser.add_argument(
        "--source-duration",
        type=float,
        help="Seconds. Without it the timeline ends at the last word, so trailing silence stays.",
    )
    parser.add_argument(
        "--min-silence",
        default="auto",
        help=(
            "Seconds of pause before it counts as dead air, or `auto` to derive it "
            "from the speaker's own pause distribution. Floor is 2.5s: half a second "
            "is healthy, one or two is still someone thinking."
        ),
    )
    parser.add_argument(
        "--pause-target",
        default="auto",
        help=(
            "What a shortened pause becomes, or `auto` to use a beat this speaker "
            "actually uses. Never silence: 0 deletes the pause outright and makes "
            "the edit airless."
        ),
    )
    parser.add_argument("--pad", type=float, default=0.06, help="Air added to each side of a keep.")
    parser.add_argument("--min-gap", type=float, default=0.25, help="Shorter cuts are collapsed.")
    parser.add_argument("--min-keep", type=float, default=0.4, help="Shorter sections are dropped.")
    parser.add_argument(
        "--aggressive-fillers",
        action="store_true",
        help="Also remove like, so, right, basically, actually, literally, you know, sort of.",
    )
    args = parser.parse_args()

    words = load_words(args.transcript)
    extent = args.source_duration if args.source_duration else words[-1]["end"]
    if extent < words[-1]["end"]:
        raise SystemExit(
            f"--source-duration {extent}s is before the last word at {words[-1]['end']:.3f}s."
        )

    pacing = analyse_pacing(words)
    auto_silence, auto_target = derive_thresholds(pacing)
    min_silence = auto_silence if args.min_silence == "auto" else float(args.min_silence)
    pause_target = auto_target if args.pause_target == "auto" else float(args.pause_target)

    fillers = mark_fillers(words, args.aggressive_fillers)
    removals = build_removals(words, fillers, min_silence, extent, pause_target)
    keeps = complement(removals, extent)
    apply_padding(keeps, removals, args.pad, extent)
    keeps = drop_wordless_keeps(keeps, words, fillers)
    keeps = merge_short_gaps(keeps, removals, args.min_gap)
    keeps = [k for k in keeps if k["end"] - k["start"] >= args.min_keep] or keeps[:1]
    if not keeps:
        raise SystemExit("Detection removed everything. Check --min-silence and the transcript.")
    assert_no_mid_word_cuts(keeps, words, fillers)

    keeps = [{"start": round(k["start"], 3), "end": round(k["end"], 3)} for k in keeps]
    cuts = label_cuts(keeps, removals, extent)
    kept = sum(k["end"] - k["start"] for k in keeps)

    edl = {
        "source": args.source or "media/source.mp4",
        "fps": args.fps,
        "keeps": keeps,
        "cuts": cuts,
        "detection": {
            "tool": "detect_cuts.py",
            "minSilence": min_silence,
            "pauseTarget": pause_target,
            "pacing": pacing,
            "pad": args.pad,
            "minGap": args.min_gap,
            "minKeep": args.min_keep,
            "aggressiveFillers": args.aggressive_fillers,
            "sourceDuration": round(extent, 3),
            "keptDuration": round(kept, 3),
            "removedDuration": round(extent - kept, 3),
            "words": len(words),
            "fillersRemoved": len(fillers),
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(edl, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {args.out}")
    print(f"  source        {extent:.1f}s, {len(words)} words")
    print(
        f"  pacing        {pacing['pauses']} pauses, median {pacing['median']}s, "
        f"p90 {pacing['p90']}s, longest {pacing['longest']}s"
    )
    print(f"  thresholds    dead air over {min_silence}s, shortened to {pause_target}s")
    print(f"  keeps         {len(keeps)} sections, {kept:.1f}s")
    print(f"  removed       {extent - kept:.1f}s ({(extent - kept) / extent * 100:.1f}%)")
    print(f"  fillers       {len(fillers)} words")
    by_reason = {r: sum(1 for c in cuts if c["reason"] == r) for r in ("filler", "pace", "silence")}
    print(f"  cuts          {len(cuts)} total: {by_reason['filler']} filler, "
          f"{by_reason['pace']} pause shortened, {by_reason['silence']} head/tail")
    return 0


if __name__ == "__main__":
    sys.exit(main())
