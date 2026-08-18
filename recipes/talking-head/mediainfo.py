#!/usr/bin/env python3
"""
Frame rates, timecode, and source probing.

Everything downstream counts in whole frames and carries a rational rate,
because the rates that matter in practice are not integers: 23.976 is
24000/1001, 29.97 is 30000/1001, 59.94 is 60000/1001. Storing those as
floats and multiplying by a duration is how a conform ends up a second
out over a long programme.

Run `python3 mediainfo.py --selftest` to check the timecode maths.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

# Decimal shorthands people actually type, mapped to their exact rationals.
NTSC_ALIASES: dict[str, tuple[int, int]] = {
    "23.98": (24000, 1001),
    "23.976": (24000, 1001),
    "29.97": (30000, 1001),
    "47.95": (48000, 1001),
    "47.952": (48000, 1001),
    "59.94": (60000, 1001),
    "119.88": (120000, 1001),
}

# Rates for which drop-frame timecode is defined and conventional.
DROP_FRAME_RATES = {(30000, 1001), (60000, 1001)}


class FrameRate:
    """An exact frame rate, plus the timecode convention that goes with it."""

    def __init__(self, num: int, den: int = 1, drop: bool | None = None) -> None:
        frac = Fraction(num, den)
        self.num = frac.numerator
        self.den = frac.denominator
        # The nominal rate is what timecode counts to before rolling a second:
        # 30 for 29.97, 60 for 59.94, 24 for 23.976.
        self.nominal = int(round(self.num / self.den))
        self.drop = (
            drop if drop is not None else ((self.num, self.den) in DROP_FRAME_RATES)
        )

    @property
    def is_exact_integer(self) -> bool:
        return self.den == 1

    def to_frames(self, seconds: float) -> int:
        return int(round(float(seconds) * self.num / self.den))

    def to_seconds(self, frames: int) -> float:
        return frames * self.den / self.num

    def __str__(self) -> str:
        if self.is_exact_integer:
            return f"{self.num}"
        return f"{self.num}/{self.den} ({self.num / self.den:.3f}{'DF' if self.drop else 'NDF'})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FrameRate)
            and (self.num, self.den, self.drop) == (other.num, other.den, other.drop)
        )


def parse_rate(text: str, drop: bool | None = None) -> FrameRate:
    """Accept `30`, `29.97`, `30000/1001`."""
    text = str(text).strip()
    if "/" in text:
        num, den = text.split("/", 1)
        return FrameRate(int(num), int(den), drop)
    if text in NTSC_ALIASES:
        num, den = NTSC_ALIASES[text]
        return FrameRate(num, den, drop)
    value = float(text)
    if abs(value - round(value)) < 1e-9:
        return FrameRate(int(round(value)), 1, drop)
    # An unrecognised decimal: assume it is an NTSC-style rate and recover the
    # exact rational rather than carrying the rounding forward.
    nominal = int(round(value))
    candidate = FrameRate(nominal * 1000, 1001, drop)
    if abs(candidate.num / candidate.den - value) < 0.01:
        return candidate
    raise SystemExit(f"Unrecognised frame rate: {text!r}. Use e.g. 25, 29.97 or 30000/1001.")


# ---------------------------------------------------------------------------
# Timecode
# ---------------------------------------------------------------------------


def frames_to_tc(frames: int, rate: FrameRate) -> str:
    """Frame count -> HH:MM:SS:FF, or HH:MM:SS;FF for drop-frame."""
    frames = max(0, int(frames))
    nominal = rate.nominal

    if rate.drop:
        # Drop-frame skips frame *numbers* (never frames) at the top of each
        # minute except every tenth, so the clock tracks wall time.
        dropped = 2 if nominal == 30 else (nominal // 15)
        per_10min = nominal * 600 - 9 * dropped
        per_min = nominal * 60 - dropped
        tens, rest = divmod(frames, per_10min)
        frames += dropped * 9 * tens
        if rest >= dropped:
            frames += dropped * ((rest - dropped) // per_min)
        separator = ";"
    else:
        separator = ":"

    ff = frames % nominal
    ss = (frames // nominal) % 60
    mm = (frames // (nominal * 60)) % 60
    hh = (frames // (nominal * 3600)) % 24
    return f"{hh:02d}:{mm:02d}:{ss:02d}{separator}{ff:02d}"


def tc_to_frames(text: str, rate: FrameRate) -> int:
    """HH:MM:SS:FF or HH:MM:SS;FF -> frame count."""
    cleaned = str(text).strip()
    drop = ";" in cleaned or "." in cleaned
    parts = cleaned.replace(";", ":").replace(".", ":").split(":")
    if len(parts) != 4:
        raise SystemExit(f"Bad timecode: {text!r}. Expected HH:MM:SS:FF.")
    hh, mm, ss, ff = (int(p) for p in parts)
    nominal = rate.nominal
    total = ((hh * 60 + mm) * 60 + ss) * nominal + ff
    if drop or rate.drop:
        dropped = 2 if nominal == 30 else (nominal // 15)
        total -= dropped * (hh * 54 + mm - mm // 10)
    return total


# ---------------------------------------------------------------------------
# Probing
# ---------------------------------------------------------------------------


class ProbeResult(dict):
    """ffprobe findings, with attribute-ish access for readability."""

    def __getattr__(self, item: str):
        try:
            return self[item]
        except KeyError as err:
            raise AttributeError(item) from err


def probe(path: Path) -> ProbeResult:
    """Read rate, start timecode, dimensions and field order from the file."""
    if shutil.which("ffprobe") is None:
        raise SystemExit(
            "ffprobe not found. Install ffmpeg, or pass --fps / --start-tc / "
            "--field-order explicitly. Guessing these is how a conform drifts."
        )
    if not path.exists():
        raise SystemExit(f"Source not found: {path}")

    raw = subprocess.run(
        [
            "ffprobe", "-v", "error", "-print_format", "json",
            "-show_streams", "-show_format", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return parse_probe(json.loads(raw))


def parse_probe(data: dict) -> ProbeResult:
    """Pull what we need out of ffprobe JSON. Split out so it can be tested."""
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video is None:
        raise SystemExit("No video stream found in the source.")
    audio = [s for s in streams if s.get("codec_type") == "audio"]

    rate_text = video.get("r_frame_rate") or video.get("avg_frame_rate") or "30/1"
    rate = parse_rate(rate_text)

    avg_text = video.get("avg_frame_rate")
    vfr = False
    if avg_text and avg_text not in ("0/0", rate_text):
        try:
            avg = Fraction(avg_text)
            vfr = abs(float(avg) - rate.num / rate.den) / (rate.num / rate.den) > 0.1
        except (ZeroDivisionError, ValueError):
            vfr = False

    # Timecode can live on the container, the video stream, or a tmcd track.
    start_tc = (
        data.get("format", {}).get("tags", {}).get("timecode")
        or video.get("tags", {}).get("timecode")
        or next(
            (
                s.get("tags", {}).get("timecode")
                for s in streams
                if s.get("tags", {}).get("timecode")
            ),
            None,
        )
    )

    field_order = (video.get("field_order") or "progressive").lower()
    duration = data.get("format", {}).get("duration") or video.get("duration")

    return ProbeResult(
        rate=rate,
        start_tc=start_tc,
        start_tc_frames=tc_to_frames(start_tc, rate) if start_tc else 0,
        width=int(video.get("width") or 0),
        height=int(video.get("height") or 0),
        field_order=field_order,
        interlaced=field_order not in ("progressive", "unknown", ""),
        vfr=vfr,
        duration=float(duration) if duration else None,
        has_audio=bool(audio),
        audio_channels=int(audio[0].get("channels") or 2) if audio else 0,
        codec=video.get("codec_name") or "",
    )


# FCPXML wants a human field-order string; progressive omits the attribute.
FCPXML_FIELD_ORDER = {
    "tt": "upper first",
    "tb": "upper first",
    "bb": "lower first",
    "bt": "lower first",
}


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def selftest() -> int:
    failures: list[str] = []

    def check(label: str, got, want) -> None:
        if got != want:
            failures.append(f"{label}: got {got!r}, want {want!r}")

    ndf30 = FrameRate(30)
    df2997 = parse_rate("29.97")
    ndf2997 = parse_rate("29.97", drop=False)
    df5994 = parse_rate("59.94")
    ndf2398 = parse_rate("23.976")
    pal = FrameRate(25)

    check("29.97 is 30000/1001", (df2997.num, df2997.den), (30000, 1001))
    check("29.97 defaults to drop", df2997.drop, True)
    check("23.976 is 24000/1001", (ndf2398.num, ndf2398.den), (24000, 1001))
    check("23.976 is never drop", ndf2398.drop, False)
    check("25p is not drop", pal.drop, False)
    check("59.94 is 60000/1001", (df5994.num, df5994.den), (60000, 1001))
    check("30000/1001 parses", parse_rate("30000/1001").num, 30000)

    # Non-drop is plain arithmetic.
    check("30 NDF @90", frames_to_tc(90, ndf30), "00:00:03:00")
    check("29.97 NDF @1800", frames_to_tc(1800, ndf2997), "00:01:00:00")

    # Drop-frame: two frame numbers skipped each minute bar every tenth, so an
    # hour of 29.97DF is 107892 frames, not 108000.
    check("29.97 DF @0", frames_to_tc(0, df2997), "00:00:00;00")
    check("29.97 DF @1800", frames_to_tc(1800, df2997), "00:01:00;02")
    check("29.97 DF @17982 (10 min)", frames_to_tc(17982, df2997), "00:10:00;00")
    check("29.97 DF @107892 (1 hr)", frames_to_tc(107892, df2997), "01:00:00;00")
    check("59.94 DF @215784 (1 hr)", frames_to_tc(215784, df5994), "01:00:00;00")

    # Round trips.
    for rate, name in ((ndf30, "30"), (df2997, "29.97DF"), (df5994, "59.94DF"), (pal, "25")):
        for frame in (0, 1, 999, 1800, 17982, 107891, 215784):
            tc = frames_to_tc(frame, rate)
            back = tc_to_frames(tc, rate)
            if back != frame:
                failures.append(f"round trip {name} @{frame}: tc {tc} -> {back}")

    # Probe parsing, without needing ffprobe present.
    sample = {
        "streams": [
            {
                "codec_type": "video",
                "r_frame_rate": "30000/1001",
                "avg_frame_rate": "30000/1001",
                "width": 1920,
                "height": 1080,
                "field_order": "tt",
                "codec_name": "h264",
                "tags": {"timecode": "01:00:00;00"},
            },
            {"codec_type": "audio", "channels": 2},
        ],
        "format": {"duration": "3600.0", "tags": {}},
    }
    info = parse_probe(sample)
    check("probe rate", (info.rate.num, info.rate.den), (30000, 1001))
    check("probe interlaced", info.interlaced, True)
    check("probe field order", FCPXML_FIELD_ORDER.get(info.field_order), "upper first")
    check("probe start tc frames", info.start_tc_frames, 107892)
    check("probe audio", info.has_audio, True)

    if failures:
        print("FAILED:")
        for line in failures:
            print("  " + line)
        return 1
    print("mediainfo selftest: all checks passed")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Frame rate / timecode helpers.")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--probe", type=Path, help="Probe a media file and print findings.")
    args = parser.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if args.probe:
        info = probe(args.probe)
        info["rate"] = str(info["rate"])
        print(json.dumps(info, indent=2))
        sys.exit(0)
    parser.print_help()
