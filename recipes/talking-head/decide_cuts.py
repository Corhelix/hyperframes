#!/usr/bin/env python3
"""
Candidates -> decisions, with reasons.

REQUIREMENT.md asks for "keep/cut ranges with reasons", and §2 asks the
system to "decide whether a pause is intentional (e.g., before a key
point) or just dead air". Neither is a threshold. A reason is what an
editor would tell you: "left three ums, it flowed and sounded natural".
A category label is not a reason, and a rule cannot produce one.

This is the pass that makes the decision contextual. Each candidate
arrives with the transcript either side of it, and comes back with an
action and a written justification that goes into the EDL and stays
there. The reasons are the point: they are what lets the framing be
adjusted, because you can read why something was left in and disagree
with it.

Usage:
    python3 decide_cuts.py \
        --candidates candidates.json \
        --out clean.edl.json

Without credentials it writes the deterministic proposals through
unchanged, each labelled as unreviewed, so the pipeline still runs and
nobody mistakes a threshold for a judgement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MODEL = "claude-opus-5"
CHUNK = 40

BRIEF = """\
You are cutting a talking-head recording. Decide, for each candidate, whether it
is removed, left alone, or shortened, and say why in one plain sentence.

What governs the edit:

Fewest cuts wins. A cut is a cost. Every one risks reading as "this has been
edited", so nothing is removed unless leaving it in is worse than the splice.

Breathing space over tight cutting. Half a second of pause is healthy. One or
two seconds is still someone thinking. Nobody speaks in a continuous stream, and
an edit with no air in it is a failure, not a tight result.

A pause is not dead air because of its length. It is dead air because nothing is
happening. The same two seconds is a stall after a throwaway line and a
deliberate beat before a reveal. Read what comes before and after and decide
which it is. A pause that sets up a punchline, a reveal, or the answer to a
question just asked is doing work: keep it.

Fillers are worth removing when they are stumbles. A few scattered "um"s can
read as natural speech, and cutting every one costs a splice each. Say so when
you leave them.

Prefer shortening to removing. A long pause reduced to a beat keeps the rhythm;
deleted, it closes a gap the speaker meant to leave.

Actions:
  cut      remove the range entirely
  keep     leave it exactly as it is
  shorten  reduce it, giving the start and end of what should be REMOVED from
           the middle, leaving air on both sides

Write the reason as you would tell the editor. "Left this, it lands after the
question and the beat is doing the work" is a reason. "silence" is not.\
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "decisions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "action": {"type": "string", "enum": ["cut", "keep", "shorten"]},
                    "start": {"type": "number"},
                    "end": {"type": "number"},
                    "reason": {"type": "string"},
                },
                "required": ["id", "action", "start", "end", "reason"],
                "additionalProperties": False,
            },
        },
        "notes": {
            "type": "string",
            "description": "How the section reads overall, and anything left in on purpose.",
        },
    },
    "required": ["decisions", "notes"],
    "additionalProperties": False,
}


def deterministic(candidates: list[dict]) -> tuple[list[dict], str]:
    """Proposals passed through when no model is available, labelled as such."""
    return (
        [
            {
                "id": c["id"],
                "action": "cut" if c["proposal"] == "cut" else "keep",
                "start": c["start"],
                "end": c["end"],
                "reason": (
                    f"Unreviewed. Threshold proposed {c['proposal']} for a "
                    f"{c['duration']}s {c['kind']}; nothing read the context."
                ),
            }
            for c in candidates
        ],
        "No model available, so no judgement was applied. These are thresholds, "
        "not decisions, and the pauses in particular deserve a second look.",
    )


def decide(payload: dict, chunk_size: int, effort: str) -> tuple[list[dict], str]:
    try:
        import anthropic
    except ImportError:
        print("  anthropic SDK not installed, falling back to thresholds", file=sys.stderr)
        return deterministic(payload["candidates"])

    client = anthropic.Anthropic()
    candidates = payload["candidates"]
    pacing = payload.get("pacing", {})
    decisions: list[dict] = []
    notes: list[str] = []

    # The brief and the speaker's pacing are identical across every chunk, so
    # they sit at the front behind a cache breakpoint and are read once.
    system = [
        {"type": "text", "text": BRIEF, "cache_control": {"type": "ephemeral"}},
        {
            "type": "text",
            "text": (
                f"This speaker pauses {pacing.get('median', '?')}s at the median and "
                f"{pacing.get('p90', '?')}s at the 90th percentile. Judge against their "
                "rhythm, not a general one."
            ),
        },
    ]

    for start in range(0, len(candidates), chunk_size):
        batch = candidates[start : start + chunk_size]
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=16000,
                thinking={"type": "adaptive"},
                output_config={"effort": effort, "format": {"type": "json_schema", "schema": SCHEMA}},
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Decide each candidate. `before` and `after` are the "
                            "transcript either side of it.\n\n"
                            + json.dumps(batch, indent=2)
                        ),
                    }
                ],
            )
        except Exception as err:  # noqa: BLE001 - reported, then degraded
            for kind, label in (
                ("AuthenticationError", "no valid credentials"),
                ("RateLimitError", "rate limited"),
                ("BadRequestError", "request rejected"),
            ):
                if type(err).__name__ == kind:
                    print(f"  {label}: {err}", file=sys.stderr)
                    break
            else:
                print(f"  {type(err).__name__}: {err}", file=sys.stderr)
            print("  falling back to thresholds for the remainder", file=sys.stderr)
            remaining, note = deterministic(candidates[start:])
            return decisions + remaining, " ".join(notes + [note])

        text = next(b.text for b in response.content if b.type == "text")
        parsed = json.loads(text)
        decisions.extend(parsed["decisions"])
        if parsed.get("notes"):
            notes.append(parsed["notes"])
        print(f"  decided {len(decisions)}/{len(candidates)}", file=sys.stderr)

    return decisions, " ".join(notes)


def to_edl(payload: dict, decisions: list[dict]) -> dict:
    """Decisions become removals; keeps become the record of what was left."""
    by_id = {c["id"]: c for c in payload["candidates"]}
    removals, kept = [], []
    for decision in sorted(decisions, key=lambda d: d["id"]):
        candidate = by_id.get(decision["id"])
        if candidate is None:
            continue
        if decision["action"] == "keep":
            kept.append(
                {
                    "start": candidate["start"],
                    "end": candidate["end"],
                    "kind": candidate["kind"],
                    "reason": decision["reason"],
                }
            )
            continue
        removals.append(
            {
                "start": round(max(candidate["start"], decision["start"]), 3),
                "end": round(min(candidate["end"], decision["end"]), 3),
                "action": decision["action"],
                "kind": candidate["kind"],
                "reason": decision["reason"],
            }
        )

    removals = [r for r in removals if r["end"] > r["start"] + 1e-6]
    removals.sort(key=lambda r: r["start"])
    extent = payload["sourceDuration"]
    keeps, cursor = [], 0.0
    for removal in removals:
        if removal["start"] > cursor + 1e-9:
            keeps.append({"start": round(cursor, 3), "end": round(removal["start"], 3)})
        cursor = max(cursor, removal["end"])
    if extent > cursor + 1e-9:
        keeps.append({"start": round(cursor, 3), "end": round(extent, 3)})

    return {
        "source": payload["source"],
        "fps": payload["fps"],
        "keeps": keeps,
        "cuts": removals,
        "kept": kept,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Judge cut candidates in context.")
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--chunk", type=int, default=CHUNK)
    parser.add_argument("--effort", default="high", choices=("low", "medium", "high", "xhigh", "max"))
    parser.add_argument(
        "--no-model",
        action="store_true",
        help="Skip the model and pass the thresholds through, labelled unreviewed.",
    )
    args = parser.parse_args()

    try:
        payload = json.loads(args.candidates.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {args.candidates}")
    except json.JSONDecodeError as err:
        raise SystemExit(f"Invalid JSON in {args.candidates}: {err}")
    if not payload.get("candidates"):
        raise SystemExit(f"{args.candidates} has no candidates. Run detect_cuts.py --candidates first.")

    decisions, notes = (
        deterministic(payload["candidates"]) if args.no_model
        else decide(payload, args.chunk, args.effort)
    )
    edl = to_edl(payload, decisions)
    edl["review"] = {
        "reviewedBy": "thresholds only" if args.no_model else MODEL,
        "notes": notes,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(edl, indent=2) + "\n", encoding="utf-8")

    actions = {a: sum(1 for c in edl["cuts"] if c["action"] == a) for a in ("cut", "shorten")}
    print(f"Wrote {args.out}")
    print(f"  reviewed by   {edl['review']['reviewedBy']}")
    print(f"  decisions     {len(decisions)} over {len(payload['candidates'])} candidates")
    print(f"  removals      {actions['cut']} cut, {actions['shorten']} shortened")
    print(f"  left in       {len(edl['kept'])}, each with a reason")
    print(f"  sections      {len(edl['keeps'])}")
    if notes:
        print(f"  notes         {notes[:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
