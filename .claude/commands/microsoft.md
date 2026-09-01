---
description: "Microsoft Advertising (Bing Ads) platform agent: audit a live account against the build standard."
argument-hint: "[brand or account id]"
---
<!-- Source: slash-commands/microsoft.md — .claude/commands/microsoft.md must match exactly -->
# /microsoft — Microsoft Advertising listener agent (on-demand run)

Run the **Microsoft Ads listener** for one account. Same spine as `/google`: identity → collect
(`msads` REST CLI) → reason with `ad-ops/microsoft-ads-audit` → grade against the build standard →
report. **Read-only throughout.** The access layer has no write commands, deliberately: Microsoft has
no account-level undo, only a 30-day per-entity change history applied by hand.

**ARGUMENT:** a brand slug or a Microsoft `AccountId`.

**Strategy above this command:** `/microsoft-strategise` decides what the account should be. This
command reports how the live account performs against that. If no strategy of record exists, run
`/microsoft-strategise` first; a listener with nothing to compare against produces findings nobody
can act on.

---

## HARD RULE — read-only, always

This command reads and reports. It proposes no mutation and applies none. Where a fix is obvious,
it is written as a specific, executable instruction in the report for Andrew to stamp, never run.

## DRIFT DETECTION — read before doing anything

- **You reached for a Google threshold.** Microsoft's limits are not Google's. Three active RSAs per
  ad group, not more. No Target Impression Share strategy. A documented 30-conversion floor. If you
  are about to apply a number from `37-google-ads-audit`, stop and check the Microsoft build standard.
- **You are about to report a blended search-share figure.** Bing's Australian desktop and mobile
  shares differ by roughly thirtyfold. A blended number hides the entire strategic question.
- **You found no import job and are about to report the account as import-free.** A manager-account
  schedule does not appear on the account's own job list and will still overwrite it. Say what you
  checked.
- **You are about to quote a threshold as observed.** As of v1.0.0 this skill has never run against a
  live account. Every threshold is documented, not observed. Say which.
- **The account returned nothing and you are about to call it a connection problem.** Check
  `msads doctor` first. A missing client ID and an empty account both look like silence.

## Phase 0 — Preflight

```bash
msads doctor
```

Confirms environment (sandbox against production is error 105), whether the registration is a web app
or a device-bound public client, and token state. A failure here is a configuration finding, not an
account finding, and it is reported as such.

## Phase 1 — Identity (the lens)

Run `_shared/card-awareness-context-load.md` in full, then resolve identity. On this platform that is
a two-step call, not a single customer ID:

```bash
msads accounts        # GetUser -> SearchAccounts
```

Cache which `CustomerId` each `AccountId` is reachable through. **Never use `AccountNumber`** — the
eight-character value in the web UI is not the identifier the API accepts, and Microsoft's own docs
warn about the confusion.

> **No account inventory exists yet.** Unlike `/google`, this command has no per-brand account table,
> because no Microsoft Ads account has been catalogued for any entity. Build the table here from the
> first live `msads accounts` run and commit it, rather than resolving identity from scratch each time.

## Phase 2 — Collect (evidence)

```bash
msads import-jobs --account <id>     # ALWAYS FIRST, see Phase 3
msads campaigns --account <id>
msads report --account <id> --type SearchQueryPerformanceReportRequest --timezone SydneyAustralia
msads raw <service> <path> --body '<json>'   # escape hatch for unmodelled read operations
```

Every operation is POST, including reads. The v13 REST surface is RPC over HTTP, not resource REST.
Set `ReportTimeZone` on every report; the API default is US Pacific and silently misdates Australian
reporting.

## Phase 3 — Reason (doctrine)

Load `skills/digital-marketing/ad-ops/microsoft-ads-audit` plus `paid-ads`. Both run the three G1
cross-cutting contracts first, in order:
`skills/digital-marketing/ad-ops/_shared/{card-awareness-context-load,seven-field-finding-schema,brand-clean-guardrails-lint}.md`.

**Sub-audit 1 (Google import posture) runs before everything, including conversion tracking.** On
Google, a broken conversion denominator poisons downstream numbers. Here there is a failure mode
above that: if an import owns the account, every finding you produce is reverted on the next
scheduled run. That changes what the report should lead with, not just what it contains.

The numbered `01-30` ad-ops brochures are quarantined (`ad-ops/_quarantined-brochures-2026-08-05/`) —
do not load any skill by a `NN-name` path from that range.

## Phase 4 — Grade against the build standard

**Load `command-includes/_MICROSOFT-ADS-BUILD-STANDARD.md` and grade the live account against every
row.** That file is the authority and is shared with `/microsoft-strategise`, so the definition of a
complete campaign cannot drift between the command that specifies one and the command that grades one.

It covers import posture, measurement, the ad surface including the Copilot logo gate and the
callout 2-to-20 cliff, Microsoft's RSA limits, targeting and structure, the documented bidding floor,
and network reporting truth. It also carries the measurement traps that produce false findings and
the three unsettled contradictions between official Microsoft sources.

Findings against this standard fold into the Phase 5 report as their own ranked block.

> **Do not skip this phase.** It exists for the same reason the Google one does. On 2026-08-28 an
> Axia audit ran collect and reason, chased a conversion defect, and never reached the grading phase.
> A lane spending $237 a week had zero sitelinks, no snippet, no logo and no business name. The
> checklist existed and was not executed.

## Phase 5 — Report (format-out)

Seven-field schema per finding, ranked by dollar impact, with the literal `msads` command in the
`Query` field so a reader can re-run it. Where an import owns the account, every finding's
`card-filter` states so and the report leads with the import configuration rather than with the
largest dollar figure. A big number the operator cannot hold is worth less than a small one they can.

State confidence honestly: until a live run is recorded at `live_execution_proof` in the skill's
frontmatter, thresholds are documented rather than observed and no finding carries HIGH on a
threshold not read directly from the account.

## Notes

- The `msads` CLI is zero-dependency standard library. Neither official Python SDK is used: `bingads`
  is on a deprecation clock and `msads` does not import on a clean install, and both packages occupy
  the same import namespace.
- SOAP is feature-frozen from 2026-10-01 and scheduled for deprecation on 2027-01-31. Ignore SOAP
  examples; this command is REST throughout.
- Microsoft Advertising Scripts is a second programmatic surface, resident inside the account with
  its own scheduling. It is the right home for automation that should keep running when nothing of
  ours is invoked. Out of scope for this command, worth naming when the recommendation calls for it.
- **This does not close the Bing Webmaster Tools gap** listed in the digital marketing stack docs.

---

## GATE MECHANICS — the hooks that will deny you

Canonical text: `command-includes/_GATE-MECHANICS.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

**The session markers.** `.entity-loaded` (or `no-entity` for platform work) and
`.skills-approved` gate every Write and Edit via `skills-gate-v2.sh`. Since v2.4
the skills proof is checked for content, not length: the frame needs eight
distinct words, at least one proposed skill must resolve against
`skills-catalogue.json`, and if this session invoked skills the proposal must name
one of them. Legacy `.claude/.entity-loaded` and `.claude/.skills-approved` paths
are ignored.

**Load order, enforced on reads.** `command-load-order-gate.py` arms off the
operator's typed prompt, not off anything the model does. A denied Read is the
gate working, not a tooling failure.

**File home, enforced on writes.** `clean-path-gate.py` allows only
`~/Documents/CLEAN/<repo>/<path>`, and the first segment must be a real repo — in
`repo-map.json` or present on disk with a `.git`.

**Tool discipline, enforced on Bash.** `block-bash-fileops.py` denies `cat`,
`head`, `tail`, `grep` and `find` in every pipeline position, including
`/usr/bin/grep`, `\grep`, `env grep`, `xargs grep` and `bash -c "cat ..."`. Use
Read, Grep and Glob. Bound payload with Read's `offset`/`limit` or Grep's
`head_limit`. If the dedicated tool is absent from the session, `git grep` and
`python3` are allowed and are not bypasses.

Working around a gate rather than satisfying it is the drift the gates exist to
catch, and it is caught in audit.

## When something is blocked: present a form, do not halt

A denial that arrives as a paragraph of instructions is homework. The operator has
to read the prose, work out what the decision actually is, and then run commands by
hand. That is the failure mode, not the block itself.

**Every blocked action that needs operator authorisation is presented as a
structured approval question — AskUserQuestion — never as prose asking them to go
and run something.**

Distinguish the two cases first, because they need opposite responses.

**A gate blocking work it should not** is a defect. Do not ask for approval to work
around it. Fix the gate, or report it as a defect with the reproduction. Examples
from 2026-08-16: the skills gate denying the write that satisfied it; a proposal
denied for naming skills the session had not invoked; a catalogue blind to
project-level skills. None of those warranted an approval prompt. They warranted a
fix.

**A guard blocking work it should** is not a defect. `gh secret set` writing
credentials, `apply_migration` running DDL against a shared production database,
anything destructive or outward-facing. Never route around these, and never ask for
a standing allow-rule when a single decision is what is needed.

For the second case, the response is a form with:

  - the one decision, stated as a question the operator can answer without reading
    the transcript
  - what was already tried and why it failed, in one line each — a blocked action
    reported without the routes attempted is a ghost blocker
  - the blast radius, named. Shared database, live credentials, how many repos
  - options that are genuinely different, each with its consequence, and a
    recommendation. An options menu with no recommendation is banned by the
    goal-first contract and that applies here
  - what happens to the rest of the work either way. If other items are unblocked,
    say you are proceeding with those, then proceed

Then keep working on whatever does not depend on the answer. A session that halts
entirely on one blocked item, when six others are unblocked, has turned one
permission decision into a stopped thread.
