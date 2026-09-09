---
name: meta
description: Meta Ads platform agent: audit, build and optimise campaigns.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - Meta Ads work is audited, built or optimised
  does_not_fire_when:
    - the platform is Google -> /google, or Microsoft -> /microsoft
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: changes
      is: what changed, by campaign or ad set, with the reason for each
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
