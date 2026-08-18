<!-- Source: .claude/commands/_GOAL-FIRST-CONTRACT.md — canonical. Inlined into every
     build-shaped command. If you change it here, change it in every command that
     carries the block, and say so in the commit. -->

# The goal-first contract

Applies to `/cto`, `/audit-cto`, `/build-plan`, `/prd-build`, `/auto-sow`, and anything
that produces a build artefact.

Every artefact opens with these three, in this order, before any analysis.
No preamble. No framing essay. No restating the brief back.

## 1. The /goal

One sentence naming what success is, as an **observable end state** someone could
watch happen — not an intention, not a capability, not an improvement.

- Good: *"A thought typed on my phone shows up as a tracked contract on the board inside 30 seconds, and I never lose one."*
- Bad: *"Improve the capture pipeline."* *"Close the integration gap."* *"Establish a foundation for…"*

If the goal cannot be watched happening, it is not a goal yet.

## 2. Sprints to get there (roughly)

A numbered list. One line each, plus its own **success looks like** — again, a thing
you could watch.

Rough is expected. Wrong-but-concrete beats vague-but-safe, because concrete gets
corrected on contact and vague never does. If you cannot say what success looks like
for a sprint, **write `success: unknown` and say why** rather than composing a
plausible sentence. A fabricated success criterion is worse than an admitted gap.

## 3. The loop

State it, and mean it:

> **build, test, learn, iterate, rebuild, repeat until solid**

Everything below this line is subordinate to it. Analysis earns its place only by
choosing the next build. It never substitutes for one.

---

## Banned in any artefact these commands produce

| Pattern | Why it is banned |
|---|---|
| Hypothesis written as finding | If it is not verified against live state, label it **unverified** in the same sentence. |
| A findings document where a code change was available | If it could have been built, build it. Report the diff, not the diagnosis. |
| An options menu with no recommendation | Pushing the decision back without a call is not deference, it is abdication. State the call; it gets overridden if wrong. |
| Restating the problem as though restating were progress | The reader already knows the problem. They are here for the move. |
| Any section that would read identically against a different codebase | It is filler. Delete it. |
| Counting artefacts produced as work done | Documents are not deliverables unless the deliverable *is* a document. |

## The test before you output

> **Does this move a build forward, or does it describe a build?**

If it describes — delete it and go build. If you genuinely cannot build (blocked on
access, a credential, or a decision only the operator can make), then say exactly
what is blocked, in one line, and build the next unblocked thing instead of writing
about the blocked one.

## Reporting back

State what you built, what you tested it against, and what it proved — in that order.
"Verified" means you ran it and watched the result. If you did not watch it, the word
is "untested", and it goes in the output.
