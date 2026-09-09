# _VERIFICATION-STANDARD — what "verified" means, for every command

<!-- Include, not a command. Lives beside the commands, like _GATE-MECHANICS.md. v0.1 2026-08-21 -->
<!-- This is a COMMON EXPECTATION, not a department concern. A designer does not own "check it in a
     browser" any more than a CTO owns "run the tests" — both are simply what verification means
     here. It is authored once, in this file, and referenced by every command that verifies
     anything: /goal-build, /build, /review, /audit-cto, /audit-cmo, /cro, /prd-ux.
     If a command restates it, this file is the authority when the two disagree. -->

## The standard, in one line

Verified means a person performed it and watched the result. Anything else is untested, and the word "untested" appears in the output.

For a claim rather than a build, verified means a file reference or a check someone else can re-run. Anything else carries one of the four other labels in Lens 4, in the sentence.

## Why it needs stating

An artefact can pass every check it was given and still be unusable. In the Pletor shell build, twenty-four honest acceptance checks passed on a canvas that had no way to join two nodes, which was the entire product; sixteen further defects surfaced the moment someone opened a real browser, and every one would have passed a headless verifier. The checks were not wrong. They were atomic, and a product is not the sum of its gestures.

So verification runs through three lenses. None substitutes for another, and the order matters.

## Lens 1 — Code: does it run

Build clean, tests pass, types check, no console error on any surface, no unhandled rejection, no silent catch.

Proves the thing starts and executes. Never proves anything is reachable, legible, correctly placed, or connected to anything a person wants to do.

## Lens 2 — Visual: is what is produced right

Drive the real thing and look at what it actually produces. For a screen, that means a real browser at the stated viewports, capturing every surface and every reachable state: empty, loading, populated, error, and the ones nobody remembers — exactly one item, a very long value, a failed request, a slow response. Judge the rendered result, not the markup: overlap, clipping, truncation, contrast, alignment, a control that draws but sits beneath something else, text that collides at a narrower width, a state indistinguishable from a different state.

For anything without a screen — an API, a CLI, a pipeline, a workflow — the subject is the artefact it emits: the response body, the written file, the row that landed, the message that arrived, the exit code and what went to stderr. Read the emitted artefact, never the code that emits it, and keep it as evidence exactly as a capture would be kept.

Proves the output exists and is right. Never proves the parts connect.

## Lens 3 — Journey: can a person do the job

Walk each journey end to end by hand, in one continuous sitting, as the user who holds that journey's permissions. Every gesture performed, not asserted. No shortcutting by URL, no seeding state through the API, no skipping a step because it is covered elsewhere; the composite is the point. Gestures are clicks for a UI and calls or commands for anything else.

A journey passes only when its final state is reached and observed, with evidence. At the first gesture that cannot be completed, stop and report from there: a journey broken at step 3 of 9 is more useful than nine features reported green.

Proves a person can start with an intention and finish with the outcome. Never proves the thing is safe or fair under hostile use — that is what the adversarial dimensions are for.

## Lens 4 — Claim: is what you wrote true

The three lenses above verify a thing you built. This one verifies the thing you wrote about
it, and it is the lens most often absent, because an analysis has no surface to photograph.

**Every non-trivial claim carries one of five labels, in the sentence, not in a footnote.**

| Label | What it requires |
|---|---|
| **verified** | A file reference, or a check someone else can re-run and get the same answer |
| **documented but unverified** | A source says so. Nobody confirmed it. Name the source |
| **missing** | Looked for, absent. Say where you looked |
| **stale** | Present, with the date it stopped being true |
| **conflicting** | Two sources disagree. Cite both. Do not resolve it silently |

Picking one per claim is the whole mechanism. It makes certainty cost something, because
"inferred" sitting beside a confident sentence looks exactly as weak as it is.

**The ratio is the acceptance test.** An artefact that is mostly unverified is not findings,
it is an opinion piece, and it says so at the top. A summary assembled from keyword matches
fails this automatically, which is the point.

**Banned, by name, because each one converts not-knowing into looking-finished:**

- A coverage fraction offered as comprehension. "54 of 54 files" says how many files were
  opened and nothing about whether any were understood.
- A citation attached to a claim that did not need one, borrowing the texture of evidence.
- An artefact count offered as work done.
- A hypothesis written as a finding without "unverified" in the same sentence.
- "Verified" for anything you did not run and watch. The word is then "untested".

**State what you did not check.** A verification record without a limits section claims
unbounded scope. Name the host, the date, what passed, and what was not tested at all.

## Findings that survive

A finding that vanishes between audits was never a finding, it was an observation. The
estate has an audit loop 110 days stale with roughly eleven unresolved recommendations,
which is what happens when each run starts from nothing.

**Every finding gets a stable ID** of the form `<AUDIT>-<NN>`, assigned once and preserved
across runs. Match by affected target and failure mode, not by wording. A finding that moves
file keeps its ID; a reworded finding is not a new one.

**Carry the whole previous ledger forward**, including items outside this run's scope. An
item omitted from the recommended actions is not closed.

| Status | What it requires |
|---|---|
| **New** | First observed. Say newly detected, not newly introduced, unless prior evidence establishes the latter |
| **Still open** | Rechecked, and the defect remains |
| **Resolved** | The original completion check passes with current evidence. A proposed edit, a changed timestamp, an installed copy or a self-reported success does not establish resolution |
| **Reopened** | Previously resolved, same failure demonstrated again. Keep the ID |
| **Not rechecked** | Not covered this run. Preserve the last verified state. This is neither pass nor fail |
| **No longer applicable** | Evidenced scope change. Explain why. This is not a repair |

**"Not rechecked" is the load-bearing one.** Refusing to collapse unknown into either pass or
fail is what makes a comparison across runs honest. A previously resolved finding not checked
today is Not rechecked with last verified state Resolved, never a reopened defect.

**Separate four things when reporting progress:** actual repairs, newly verified evidence,
regressions, and changes in coverage. A score that rose because more was checked is not an
improvement. Do not claim progress because the open count shrank.

## Proving a boundary from the wrong side

A boundary test that checks the right data arrived proves nothing about whether the wrong data
also arrived. Test it from the side that fails silently.

Plant a uniquely named marker in every place the system must never read: the private file, the
excluded folder, the credential, the other tenant's row. Then assert the marker appears
nowhere in the output. The presence check is what everyone writes; the absence check is what
catches the leak.

This applies wherever exclusion is the requirement rather than inclusion: secrets that must not
reach a transcript, one tenant's data that must not reach another, an archived folder that must
not be ingested, a draft that must not ship.

## The defining gesture

Every product has one action that *is* the product: joining two nodes in an editor, building a form and receiving a response, a stranger booking a slot. Name it before building. It becomes the first acceptance check and the first journey, and it is verified before anything is stacked on top of it. If it cannot be performed by hand, the product does not work, whatever else is green.

## Evidence

Every finding carries an evidence path; a defect nobody captured is a rumour. Captures are named to their check or journey and to the viewport or environment they were taken in, because a defect at 1280 is not a defect at 1440. Never overwrite — a second capture of the same thing is a new version, so before and after both survive. Captions and alt text state what is visibly in the frame and nothing else; a caption that interprets or excuses is a caption that hides.

## Skipping a lens

A lens is never skipped for want of a surface — it translates. Skipping one is a recorded decision naming which lens and why, never a silence.

## The close artefact

Findings are reported as paired blocks, not prose: what it does now on the left (the real capture, or the emitted artefact verbatim), what it should do on the right (a corrected capture, or a wireframe where there is nothing yet to photograph, since that absence is itself the finding), and underneath, in plain words, what a person does — including the second route most people try first, and what the product does when the gesture is refused. Silence on refusal is a defect in its own right.
