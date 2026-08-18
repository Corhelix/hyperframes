---
description: Google Ads platform agent: audit, build and optimise campaigns.
argument-hint: "[context or target]"
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

Before reporting, grade the live account against this standard. It is brand-agnostic — the same checklist runs on the first build and the fiftieth listener pass, on any brand. It exists because a gap audit found one campaign carrying image assets, a logo, a business name and a structured snippet while the other, holding the larger budget, carried none: a build that was structurally correct and visually absent, on surfaces Google gives away for free. Findings against this standard are not a footnote — they fold into the Phase 5 report as their own ranked block.

| Check | What fails without it | How to verify |
|---|---|---|
| Full asset set on every enabled campaign, at every level it applies | One campaign carries image assets, a business logo, business name and a structured snippet; another, often holding the larger budget, carries none. A missing logo or image asset is not cosmetic — it is the account leaving surfaces unused that cost nothing to fill | List assets at account, campaign and ad-group level. Confirm image assets (minimum 3), a business logo (square and landscape), business name, at least 4 callouts, one structured snippet header with 3+ values, and a call or lead-form asset wherever the lane converts on a call or a form — on every enabled campaign. Presence alone is not enough; count against the minimum |
| Minimum 6 sitelinks, verified destinations | A campaign runs 3 or 4 sitelinks against a plan of 6, or a sitelink points at a page with no real content | Count live sitelinks against the plan. Open every destination and confirm substantive content. An HTTP 200 is not proof of a working page |
| Sitelinks match the lane, not just the count | A Canon campaign runs zero Canon sitelinks; a Sharp lane runs zero Sharp. The count target can be met while the account still fails, because none of the sitelinks say anything about what that campaign actually sells | Every sitelink on a campaign must be relevant to that campaign's own product or service lane. A lane-neutral sitelink (a shared quote form, for example) can sit on any campaign; a brand- or product-specific sitelink may only sit on the campaign for that brand or product |
| Exact-match coverage for every head term | Without an exact-match variant living in its own lane, a head term's phrase- or broad-match in a neighbouring lane can win the auction instead, so the account bids against itself and pays its own margin away | For every head term, confirm an exact-match keyword exists in the ad group it belongs to. Pull search terms by lane and confirm each head term's clicks land in the ad group built for it, not a neighbour |
| RSA copy carries no near-me phrasing | "Near me" assumes a walk-in visit. For a lease, service or B2B account with no retail premises, it misrepresents the offer and reads as a contextual mismatch the moment the click lands | Read every live headline and description for "near me", "nearby", or other local-visit phrasing. None may appear unless the business genuinely trades from a walk-in location |
| Extensions match current ad copy | A claim removed from ad copy, including a factually wrong one, keeps serving in a callout or sitelink | After any ad-copy change, diff live extension text against the current copy rulings. Extensions are assets, not ads, so they carry no serving risk and get fixed first, not last |
| Callouts add, they don't repeat | Callouts duplicate headline text, or near-duplicate each other, and waste the surface instead of extending it | No callout may repeat text already in a headline. No two callouts in the same set may be near-duplicates. Read the whole set together, not one callout at a time |
| Extensions meet the writing standard | An extension carries an exclamation mark, or a contentless line such as "Contact and save today" | Run extension copy through the same proofing pass as ad copy, not a lighter one |
| Non-www canonical, always | Mixed www and non-www final URLs cause a redirect hop and inconsistent tracking within the same account, and a redirect chain is its own policy and page-speed risk | Check every final URL and sitelink URL. None may use www. None may resolve through more than one redirect hop |
| Final URL matches the lane's intent | A Canon ad sending traffic to a generic quote page, or a lease ad landing on a purchase page, breaks the promise made in the click | Open every lane's final URL and confirm the landing page answers the specific query that ad group targets, not a generic fallback |

### Measurement traps that produce false findings

- `keyword_view` folds ad-group negatives into its counts. Filter `ad_group_criterion.negative = FALSE`, or counts read roughly three times too high.
- Negative-conflict checks must be scoped by campaign and ad group. Unscoped, a clean account reads as majority-blocked.
- Counting `<form>` tags misses lead capture embedded in a cross-origin iframe (a GoHighLevel quiz, for example). Check for iframes and visible inputs before concluding a page has no conversion path.

## Phase 5 — Report (format-out)

Ranked report: wasted-spend / QS / pacing findings plus build-standard gaps from Phase 4, evidence, suggested action, $ impact. **Negative-keyword additions** may be proposed (`free`/`jobs`/`DIY`/`how to`/`login`/`salary`/`reddit`), but as a stamp-and-apply, never auto-run — present the exact `mutate` operation and wait for Andrew's explicit go before applying it.

## Notes

- PMax raw search terms are not exposed by Google — only `campaign_search_term_insight_view`.
- Same spine deploys to Hermes as `google-daily-listener.workflow.json` once `gads-cli` + the `gaql` verb are on the box.

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
