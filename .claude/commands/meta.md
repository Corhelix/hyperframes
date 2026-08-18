---
description: Meta Ads platform agent: audit, build and optimise campaigns.
argument-hint: "[context or target]"
---
# /meta — Meta platform-agent (on-demand run)

Run the **Meta Ads listener agent** for one brand, here in Claude. Same spine that deploys to Hermes: brand kit → collect (the analyzer + insight pulls) → reason with `paid-ads` + Breakdown-Effect doctrine → report. **Read + suggest only.**

**ARGUMENT:** `<brand>` = `vlc` | `hcc`  (Axia has **no** Meta account — out of scope; refuse `axia`.)

---

## Phase 1 — Brand kit (the lens)

| brand | Meta ad account | note |
|---|---|---|
| vlc | `act_1150009252219808` | 2 live campaigns; pack: `.../2026-07-21-strategy-pack-vlc/…`. Read `VLC-OPERATING-RULES.md`. |
| hcc | `act_280879759942648` | pack: `.../2026-07-21-strategy-pack-oncampus/…` |

## Phase 2 — Collect (evidence)

**`meta-cli` is LIVE** (added + tested 2026-07-21; also in `build/cli/meta-cli`) — a full Graph/Marketing API passthrough. Needs `META_ACCESS_TOKEN` in env. Run the insight pulls directly:
```
meta-cli get act_1150009252219808/insights --param level=ad --param date_preset=last_30d --fields ad_id,ad_name,impressions,spend,clicks,ctr,cpm,actions,video_play_actions --all
meta-cli get act_1150009252219808/adsets --fields name,daily_budget,lifetime_budget,frequency,reach --all   # frequency + pacing
meta-cli get <pixel_id>/stats --param aggregation=event                                                     # pixel/CAPI health
```
- **Creative deep-scoring:** for hook rate / CES per ad, the analyzer (`~/.claude/skills/meta-ads-creative-internal-analyzer/`) still adds value; or reason directly over the `insights` pull above.
- **Credential state:** live token is Andrew's **personal** token, expires **2026-09-15**, no refresh. Durable path: mint the System User token (`122133885891158955`, W&E Agency BM) and set `META_ACCESS_TOKEN` from it. Ad accounts: vlc `act_1150009252219808`, hcc `act_280879759942648`.

## Phase 3 — Reason (doctrine)

Load `skills/digital-marketing/paid-ads` + `ad-creative`. Reason with Breakdown-Effect / Learning-Phase (a naive read calls normal fluctuation failure). Rank fatigue / pacing / CPA flags. Tag confidence. `[SILENT]` if nothing moved. Audience-overlap output is an **estimate** (no API); EMQ is blind.

## Phase 4 — Report (format-out)

Ranked report: creative-fatigue + pacing findings, evidence (the metric), a fix using `ad-creative` specs / `paid-ads` cadence, priority. No writes: pausing / budget nudges are proposed only, always presented for Andrew's explicit go, never auto-applied. (Note 2026-08-05: this previously referenced "the six-gate chain" — undefined anywhere in the repo, removed. A real approval spec is proposed but not yet built; see `projects/command-system/tasks/2026-08-05-audit-command-gate-depth/`.)

## Notes

- Meta is the lowest-effort agent — the analyzer seed already works; the build is the token mint + the five extra pulls.
- Same spine deploys to Hermes as `meta-daily-listener.workflow.json` (fast-follow).

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
