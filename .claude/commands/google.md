---
name: google
description: Google Ads platform agent: audit, build and optimise campaigns.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a Google Ads account is audited, built or optimised
  does_not_fire_when:
    - the question is account strategy rather than execution -> /google-strategise
    - the platform is Meta, Microsoft or LinkedIn -> that platform's command
  loads:
    always:
      - command-includes/_GOOGLE-ADS-BUILD-STANDARD.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: changes
      is: what changed in the account, by campaign, with the reason for each
    - id: evidence
      is: the metric that justified the change and the date it was pulled
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

# /google — Google Ads platform-agent (on-demand run)

Run the **Google Ads listener agent** for one brand, here in Claude. Same spine that deploys to Hermes: brand kit → collect (`gads-cli` GAQL) → reason with `ad-ops/37` + mathiaschu doctrine → report. **Read + suggest; the one safe-write (negative-keyword append) stays human-gated.**

**ARGUMENT:** `<brand>` = `axia` | `vlc` | `hcc`

**Strategy above this command:** `/google-strategise <brand>` decides what the account should be — architecture, intent clusters, budget allocation, bidding ladder, negative architecture, measurement truth. This command reports how the live account is performing against that. If no strategy of record exists for the brand, run `/google-strategise` first; a listener with nothing to compare against produces findings nobody can act on.

---

## Phase 1 — Brand kit (the lens)

**Direct-access accounts** (verified via `gads-cli accounts list` 2026-07-21 — the OAuth user has DIRECT access to these three and is NOT a manager on MCC `7884229147`, so do **not** pass `--mcc`):

| brand | Google Ads customer | note |
|---|---|---|
| axia | `6895092429` "Axia Office" (AUD) | conv `AW-384327269`; Ads-conversion import broken → lead truth is GHL. pack: `.../axia-office/tasks/2026-07-21-strategy-pack/…` |
| vlc | `6326592203` "Hillcrest - All HCC and VLC" (shared) | campaign `16399373755`. Read `VLC-OPERATING-RULES.md`. |
| hcc | `6326592203` (shared) | campaign `22536229604` HCC Generic PMAX |
| (w&e) | `6410934496` "Wolf and Eagle" | W&E's own account |

Query **direct — no `--mcc`**. The brand-pack "`manager_id=7884229147`" note is wrong for this CLI's OAuth user (corrected 2026-07-21; the pack still needs updating).

## Phase 2 — Collect (evidence)

`gads-cli gaql` is **LIVE** (added + tested vs Axia 2026-07-21; also in `build/cli/gads-cli`). Run read-only GAQL directly:
```
gads-cli gaql --customer-id 6895092429 --query "SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC"
```
Pulls to run: `search_term_view` (wasted spend: `cost_micros`>0 AND `conversions`=0), `keyword_view` + `ad_group_criterion.quality_info.*` (QS drops), `campaign_budget.amount_micros` + `metrics.cost_micros` (pacing), `metrics.average_cpc` vs baseline. **`cost_micros` is micros → divide by 1e6.**

**Full `gads-cli` surface (2026-07-21):** `gaql` (any read) · `mutate --operations '<MutateOperation[]>'` (the whole write API — campaigns/keywords/budgets/bids/ads/audiences; validate-only unless `--apply`) · `call --service X --method Y` (services `gaql`/`mutate` miss: `KeywordPlanIdeaService.generate_keyword_ideas`, `ReachPlanService`, `GeoTargetConstantService`) · the safe named verbs (`campaigns update`, `conversion-actions`). This agent reads; the only write it proposes is the negative-keyword add below. Read-and-suggest only: it is always presented for Andrew's stamp before applying via `mutate`, never auto-run. (Note 2026-08-05: earlier drafts of this command referenced "the six-gate chain" as the approval mechanism — that phrase had no definition anywhere in the repo and has been removed. A real, named approval spec is proposed but not yet built; see `projects/command-system/tasks/2026-08-05-audit-command-gate-depth/`.)

## Phase 3 — Reason (doctrine)

Load `skills/digital-marketing/ad-ops/37-google-ads-audit` (hardened 2026-08-05, v2.0.0 — full GAQL
per sub-audit, absorbs QS/structure/extension/geo/device, includes the RSA/ad-copy audit block) +
`paid-ads`. For ad-copy generation or a fatigued-RSA refresh, hand off to
`skills/digital-marketing/ad-ops/rsa-build-audit` (Direction A) — this is the bidirectional RSA skill
that closes the "doesnt write RSA" gap; 37's Sub-audit 7 is its audit-direction twin. Both run the
three G1 cross-cutting contracts before anything else:
`skills/digital-marketing/ad-ops/_shared/{card-awareness-context-load,seven-field-finding-schema,brand-clean-guardrails-lint}.md`
— card load, then the seven-field per-finding schema, then the brand-clean lint pass. Apply the
thresholds (QS non-brand ≥7/red<5, CTR ≥1.5%/red<1%, CVR ≥8%/red<3%, IS >80%/red<50%) and the
**mathiaschu hard rules**: `cost_micros/1e6`; discount last 7 days (conversion-lag); `conversions` vs
`all_conversions`; no budget-up if IS-lost-to-rank >50%. Order: QS → IS → Smart Bidding →
Conversions → Search Terms. Rank by $ impact. Tag confidence. `[SILENT]` if quiet.

The numbered `01-30` ad-ops brochures are quarantined (`ad-ops/_quarantined-brochures-2026-08-05/`,
G0 2026-08-05) — do not load any skill by a `NN-name` path from that range; each capability now lives
in the hardened skill named above or its own future G-phase build (see the quarantine README for the
per-file disposition).

## Phase 4 — Grade against the build standard (what good looks like)

**Load `command-includes/_GOOGLE-ADS-BUILD-STANDARD.md` and grade the live account against
every row.** That file is the authority and is shared with `/google-strategise`, so the
definition of a complete campaign cannot drift between the command that specifies one and the
command that grades one.

It covers: full asset set per enabled campaign (images, logo, business name, callouts,
structured snippet, call or lead form), minimum 6 sitelinks with verified destinations,
sitelinks matching the lane, no duplicate destinations in a set, both sitelink descriptions
populated, exact-match coverage for head terms, no near-me phrasing, extensions matching
current ad copy, callouts that add rather than repeat, structured-snippet values matching their
header, non-www canonical, final URL matching lane intent, and full negative-list coverage on
every campaign. It also carries the measurement traps that produce false findings.

Findings against this standard are not a footnote — they fold into the Phase 5 report as their
own ranked block.

> **Do not skip this phase.** On 2026-08-28 an Axia audit ran Phases 2 and 3, chased a
> conversion defect, and never reached Phase 4. Lane 2 was spending $237 a week with zero
> sitelinks, no snippet, no logo and no business name, and Demand Gen was running with no
> images or callouts at all. The checklist existed and was not executed.

## Phase 5 — Report (format-out)

Ranked report: wasted-spend / QS / pacing findings plus build-standard gaps from Phase 4, evidence, suggested action, $ impact. **Negative-keyword additions** may be proposed (`free`/`jobs`/`DIY`/`how to`/`login`/`salary`/`reddit`), but as a stamp-and-apply, never auto-run — present the exact `mutate` operation and wait for Andrew's explicit go before applying it.

## Notes

- PMax raw search terms are not exposed by Google — only `campaign_search_term_insight_view`.
- Same spine deploys to Hermes as `google-daily-listener.workflow.json` once `gads-cli` + the `gaql` verb are on the box.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
