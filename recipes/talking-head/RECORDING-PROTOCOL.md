# Recording protocol

How to deliver so the edit comes out well. Half the quality of an automated cut
is decided before the camera stops, not after.

The tool is deliberately conservative: it will not guess at your intent, and it
would rather leave something in than take something out. These habits give it
signals it can act on with certainty, so it makes fewer, better cuts.

## The two that matter most

**Say "redo" when a take goes wrong.** Then pause and take it again. The whole
attempt before the marker is removed in one cut, and the marker goes with it.
Also recognised: "scratch that", "take two", "start again", "from the top".

This is worth more than any heuristic. A spoken marker is certain, and it costs
you two seconds. Without it the tool is guessing from repeated words, which is
reliable only when you happen to restart the same way.

**Restart a sentence with the same opening words.** If you fluff a line, pause
about a second, then begin again with the same few words. The earlier attempt is
dropped and the later one kept, because the later one is the one you meant.
Four matching words is the threshold.

## What the tool already handles, so do not perform for it

**Pause naturally.** Half a second, one second, two seconds are all healthy and
all kept. Only dead air past about three seconds is touched, and even then it is
shortened to a breath rather than removed. You do not need to talk in a
continuous stream, and doing so makes the result worse, not better.

**Hesitate.** Clear fillers are removed: um, uh, er, ah, mm, hmm. You do not
need to avoid them, though every one costs a cut, so fewer is still better.

**Think out loud.** A pause before a point lands is deliberate and reads as
deliberate. It survives.

## Things that cost you later

**Do not restart mid-word.** A cut can only land in the gap between words. If
you break off halfway through one, the fragment stays.

**Do not stack retakes without markers.** Three attempts with no "redo" and no
repeated opening leaves the tool no way to tell which one you want, and all
three survive.

**Leave a beat at the top and tail.** A second of air before your first word and
after your last gives the cut somewhere to land.

**Keep the framing still across a retake.** The cut joins two moments that may
be seconds apart. If you have moved, the join shows, and no amount of detection
fixes a visible jump.

## Tuning after the first pass

Run one recording through, watch the slices, then adjust:

| It feels                          | Change                                            |
| --------------------------------- | ------------------------------------------------- |
| Airless, rushed, obviously edited | Raise `--min-silence` and `--pause-target`        |
| Slow, too much dead air left      | Lower `--min-silence`                             |
| Choppy, too many small cuts       | Drop `--no-aggressive-fillers`, raise `--min-gap` |
| Fillers still audible             | Add `--aggressive-fillers`                        |
| A good section was removed        | Lower `--max-retake`, or raise `--min-repeat`     |

Two or three passes should settle it. The numbers printed by `detect_cuts.py`
tell you your own pacing, so the thresholds are yours, not defaults.
