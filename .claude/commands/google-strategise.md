---
description: Google Ads account strategy of record.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/google-strategise.md — .claude/commands/google-strategise.md must match exactly -->
# /google-strategise — Google Ads account strategy of record

Produce the **strategy of record** for a Google Ads account: what campaigns should exist and why, how intent is clustered, where budget goes, which rung of the bidding ladder the account is on, what counts as a conversion, and what the negative architecture protects. This is the thinking that governs `/google`, every build, and every go-live.

`/google` reports what the account **is doing**. `/google-strategise` decides what the account **should be**. Run this first; run `/google` against it afterwards.

This command is SELF-CONTAINED. It is the single authority when invoked. Do not also load the CMO viewport or the operating sequence.

**ARGUMENT:** `<brand>` = `axia` | `vlc` | `hcc` | `we`

---

## HARD RULE — read-only, always

This command **never mutates**. Not with `--apply`, not "just a pause", not "just one negative". It reads, it reasons, it writes a strategy document. Execution belongs to a separate, explicitly authorised pass.

If the strategy concludes that something must change in the account, the output is a **stamp-able recommendation with a written, validated payload attached** — not an applied change. Every payload referenced by this document must have been run `validate-only` and its result recorded. A payload that has not been dry-run does not go in the document.

Andrew names what gets applied. Nothing else does.

---

## DRIFT DETECTION — read before doing anything

You are drifting if you are:

- **Reporting findings instead of deciding architecture** → that is `/google`. This command answers "what should the account be", not "what went wrong last week".
- **Ranking wasted spend as the main output** → **LISTENER DRIFT**. Wasted spend is an input to the strategy, not the strategy.
- **Writing the strategy from the campaign list you found** → **INVENTORY CAPTURE**. The account as built is evidence, not the plan. Start from intent, then say what the account should hold.
- **Skipping Phase 2 because the handoff already described the account** → **INHERITED STATE**. Handoffs go stale and describe intent, not reality. The Axia 2026-07-29 pass found a live experiment, a mis-read radius unit and a two-of-three negative-list gap that no handoff mentioned. Read the account.
- **Asserting a setting without a GAQL row behind it** → **UNVERIFIED CLAIM**. Every number in the output traces to a query in this session.
- **Writing "confirm with the client's ops person" or gating on a named operator** → **AUTHORITY THEATRE**. Andrew is the decision-maker. Stamp a recommendation he can override.
- **Presenting three options and asking which** → **OPTIONALITY DRIFT**. Recommend. He redirects if wrong.
- **Producing a second audit document when a strategy was asked for** → stop and write the strategy.

**SELF-TEST before Phase 5:** can I state, in one sentence, what this account is for and what it will not do? If not, go back to 4.3.

---

## Phase 0 — Doctrine load (mandatory, before anything else)

Read these in your next action. Path resolution: relative to this repo root.

1. `skills/digital-marketing/ad-ops/37-google-ads-audit` — thresholds and audit doctrine
2. `skills/digital-marketing/paid-ads/SKILL.md` — platform operating model
3. `knowledge-bank/strategy-foundations.md` — the kernel: diagnosis, guiding policy, coherent actions
4. `knowledge-bank/marketing-and-gtm.md` — funnel architecture, unit economics, CAC and payback
5. `skills/digital-marketing/product-marketing-context/SKILL.md` — switching forces, customer language
6. `skills/copywriting/Proofread-Anti-AI-Standard.md` — applies to the document you produce
7. `command-includes/_GOOGLE-ADS-BUILD-STANDARD.md` — **what a complete campaign physically contains.** You cannot specify an architecture without it: a strategy that names campaigns and budgets but no asset set is incomplete, and will be written straight over an account with blank ad surfaces without noticing

**GATE — present after the six reads:**
> Doctrine loaded: ad-ops thresholds + paid-ads model + strategy kernel + GTM + switching forces + writing standard + build standard.

If a file is missing, flag it explicitly (`MISSING: <path>`) and continue. A missing lens is a system bug, not a licence to reason without it.

---

## Phase 1 — Scope and brand kit

### 1.1 — Establish scope

Ask, if not already clear from the invocation:

1. **Which brand?** (`axia` / `vlc` / `hcc` / `we`)
2. **What is the strategic question?** One line. "Rebuild the account", "we are spending $135 a day with no plan", "should we run PMax".
3. **What is the commercial goal?** Leads, calls, enrolments, booked jobs. Name the thing that has value.
4. **What is the budget envelope?** Total per day, and whether it is fixed or arguable.
5. **What is out of bounds?** Channels, campaign types, claims, geographies.

**GATE:**
> Brand: [name] | Account: [customer id] | Question: [one line] | Goal: [conversion that matters] | Budget: [$/day] | Out of bounds: [list]
> Correct?

Wait for the reply.

### 1.2 — Brand kit (the lens)

**Direct-access accounts.** The OAuth user has DIRECT access to these and is NOT a manager on MCC `7884229147`, so do **not** pass `--mcc`:

| brand | Google Ads customer | note |
|---|---|---|
| axia | `6895092429` "Axia Office" (AUD) | conv `AW-384327269`; Ads-conversion import broken, so lead truth is GHL |
| vlc | `6326592203` "Hillcrest - All HCC and VLC" (shared) | campaign `16399373755`. Read `VLC-OPERATING-RULES.md` before anything |
| hcc | `6326592203` (shared) | campaign `22536229604` HCC Generic PMAX |
| we | `6410934496` "Wolf and Eagle" | W&E's own account |

CLI: `projects/marketing-agent-system/tasks/2026-07-21-platform-agent-system/build/cli/gads-cli`

### 1.3 — Load entity and prior strategy

Read `protocols/entity-repo-map.md`, load the brand's files, and find the current strategy of record. **APPROVED beats DRAFT; the newest HTML beats any JSON or `.md` sidecar.** Name what you are superseding.

**GATE:**
> Loaded [N] files. Strategy of record: [path]. Superseded: [list or "none"]. Gaps: [list or "none"]. Confirm?

---

## Phase 2 — Account reality sweep (READ-ONLY, mandatory, no shortcuts)

Run every block. Record the answer even when it is boring, because the boring answers are what later steps get wrong. This sweep exists because each query below has caught a real, load-bearing surprise in production.

**2.1 — Campaign inventory, budgets, bid strategies**
```
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
       campaign.bidding_strategy_type, campaign_budget.amount_micros
FROM campaign WHERE campaign.status != 'REMOVED'
```
Record the true bid strategy. `TARGET_SPEND` is Maximise clicks, not Manual CPC. Read the ceiling: `campaign.target_spend.cpc_bid_ceiling_micros`.

**2.2 — Experiments and trial arms (the one everyone misses)**
```
SELECT experiment.experiment_id, experiment.name, experiment.status,
       experiment.start_date, experiment.end_date FROM experiment
```
```
SELECT experiment_arm.name, experiment_arm.control, experiment_arm.campaigns,
       experiment_arm.traffic_split FROM experiment_arm
```
```
SELECT campaign.id, campaign.name, campaign.experiment_type, campaign.base_campaign
FROM campaign WHERE campaign.status != 'REMOVED'
```
An ENABLED experiment whose end date has passed still splits traffic. A campaign with `experiment_type = EXPERIMENT` cannot be paused by a campaign mutate and will reject with `CANNOT_MODIFY_FOR_TRIAL_CAMPAIGN`. If any campaign in scope is a base or a trial arm, that fact outranks everything else in the sequence.

**2.3 — Negative architecture and its coverage**
```
SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.member_count
FROM shared_set WHERE shared_set.status != 'REMOVED'
```
```
SELECT campaign.id, campaign.name, shared_set.id, shared_set.name FROM campaign_shared_set
```
```
SELECT campaign.id, campaign_criterion.keyword.text FROM campaign_criterion
WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'
```
Build a **coverage matrix**: lists down the side, campaigns across the top. Shared lists are almost never linked to campaigns created later than the lists. Newly built campaigns routinely inherit none of them.

**2.4 — Ad groups, keywords, ads actually present**
```
SELECT campaign.id, ad_group.id, ad_group.name, ad_group.status FROM ad_group
WHERE ad_group.status != 'REMOVED'
```
```
SELECT ad_group.id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
FROM keyword_view WHERE ad_group_criterion.status != 'REMOVED'
```
```
SELECT campaign.id, ad_group.id, ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad
WHERE ad_group_ad.status != 'REMOVED'
```
Note ENABLED ads sitting inside PAUSED ad groups. They do not serve, and the ad-group pause is the only thing holding them.

**2.5 — Geo and schedule, with units**
```
SELECT campaign.id, campaign_criterion.type, campaign_criterion.location.geo_target_constant,
       campaign_criterion.proximity.radius, campaign_criterion.proximity.radius_units,
       campaign_criterion.ad_schedule.day_of_week, campaign_criterion.ad_schedule.start_hour,
       campaign_criterion.ad_schedule.end_hour
FROM campaign_criterion WHERE campaign_criterion.type IN ('LOCATION','PROXIMITY','AD_SCHEDULE')
```
```
SELECT campaign.id, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign
```
**Always read `radius_units`.** MILES and KILOMETERS both appear in the same account. A radius of 30 is 48 km or 30 km depending on a field most people never select.

**2.6 — Conversion truth**
```
SELECT conversion_action.id, conversion_action.name, conversion_action.status,
       conversion_action.type, conversion_action.category,
       conversion_action.primary_for_goal FROM conversion_action
```
```
SELECT campaign.id, campaign_conversion_goal.category, campaign_conversion_goal.origin,
       campaign_conversion_goal.biddable FROM campaign_conversion_goal
```
Ask the harder question: does the conversion the account bids on correspond to a thing with commercial value? For Axia the Ads import is broken and lead truth lives in GHL, which means the account is optimising to a signal that is not the business's definition of a lead.

**2.7 — Demand and waste**
```
SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM search_term_view WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.cost_micros DESC
```
```
SELECT campaign.id, metrics.search_impression_share,
       metrics.search_rank_lost_impression_share, metrics.search_budget_lost_impression_share
FROM campaign WHERE segments.date DURING LAST_30_DAYS
```
`cost_micros / 1e6`. Discount the last seven days for conversion lag. Distinguish `conversions` from `all_conversions`. PMax does not expose raw search terms; use `campaign_search_term_insight_view`.

**GATE — present the sweep as a state table, not a wall of JSON:**
> Campaigns [N] ([n] enabled) · Experiments [N] ([n] live) · Shared lists [N] ([n] linked to all in-scope campaigns) · Ad groups [N] · Keywords [N] · Ads [N] · Conversion goals [N] biddable · Geo units [MILES/KM] · Spend last 30d [$X]
> Surprises against the handoff: [list, or "none"]
> Confirm before I reason on this?

---

## Phase 3 — Intent clustering

Before deciding what campaigns should exist, decide what the demand actually is. Work from `search_term_view` and the keyword set, not from the campaign names.

For each cluster:

| Field | Answer |
|---|---|
| Cluster name | Plain language, the job the searcher is doing |
| Representative queries | Verbatim from search terms, not invented |
| Intent stage | Research / compare / price / ready-to-buy / support |
| Commercial value | What a conversion here is worth, and why |
| Current home | Which campaign and ad group serves it today, or "unserved" |
| Verdict | Own it / defend it / decline it |

A cluster you decline is a strategic decision and belongs in the negative architecture. Say so explicitly.

---

## Phase 4 — Strategic analysis (complete all seven, do not abbreviate)

**4.1 — Intent state.** For each cluster in scope: what is the searcher doing at the moment of the query, what have they already tried, what do they believe that may be wrong, and what would make them close the tab. Use their language from the search terms.

**4.2 — Switching dynamics on the SERP.** Map all four forces, and for each name the **ad asset and the landing surface** that carries it:

| Force | Ad asset | Landing surface | Mechanism |
|---|---|---|---|
| **Push** | | | |
| **Pull** | | | |
| **Habit** | | | |
| **Anxiety** | | | |

Anxiety is the one paid accounts skip. On a considered purchase the click is cheap and the doubt is expensive.

**4.3 — Account architecture.** The core of this document. State what the account should hold and why:

- Campaigns that should exist, each with its cluster, its budget and its job
- Campaigns that should not exist, and what happens to them
- Ad group granularity and the reason for that granularity
- Match-type doctrine, and what broad is allowed to do
- The negative architecture: which shared lists exist, what each protects against, and which campaigns each must be linked to. **Every campaign gets every list unless there is a written reason it does not.**
- **The asset set each campaign will carry**, specified against `command-includes/_GOOGLE-ADS-BUILD-STANDARD.md`: sitelinks and their destinations, callouts, structured snippet, images, logo, business name, call or lead form. An architecture that names campaigns and budgets but no assets is not finished
- One sentence: what this account is for, and what it will not do

**4.4 — Competitive frame.** Who else is in the auction, from auction insights and impression share. Where impression share is lost to rank versus budget, and what that says about the offer rather than the bid. Do not raise budget where rank-lost share exceeds 50 per cent.

**4.5 — Budget and the bidding ladder.** State the rung the account is **actually** on, from 2.1, not the one the plan assumes. The climb is Maximise clicks with a CPC ceiling, then Maximise conversions, then target CPA, and each step needs conversion volume the previous step earned. Name the volume threshold that unlocks the next rung and the evidence that would say the climb was wrong. Allocate budget across campaigns with a reason per line.

**4.6 — Measurement truth.** What the account bids on, what the business counts as a lead, and the distance between them. If they differ, closing that gap outranks every optimisation in this document, because everything downstream optimises toward the wrong thing until it is closed.

**4.7 — Recommendations, sequenced.** The single most important move. What is done first and why the order matters. What is explicitly not done yet. What evidence would change the plan.

---

## Phase 5 — Output

Write the **strategy of record** as branded HTML using the decision-tagging scaffold at `../alc-group/brand-ops/protocols/HTML-DECISION-TAGGING-PATTERN.html`, so every recommendation is a stamp-able row (LOCK / REVISE / DROP / DEFER).

ID convention: `D` decisions · `R` risks · `Q` open questions · `S` scope boundaries.

**Required sections:**
- Account reality table from Phase 2, with the surprises called out
- Coverage matrix from 2.3, rendered visually
- Intent clusters from Phase 3
- Architecture from 4.3, as the centrepiece
- Bidding ladder with the current rung marked
- Measurement gap from 4.6
- Sequenced recommendations, each stamp-able
- Any validated payload attached, with its dry-run result recorded

**Location:** `client-projects/<parent>/clients/<client>/tasks/YYYY-MM-DD-<slug>/` for client accounts, resolved from `protocols/repo-map.json` before writing. Never this repo's `projects/` for client work.

**Naming:** `DRAFT-GOOGLE-STRATEGY-v0.1-YYYY-MM-DD.html`, incrementing to `APPROVED-YYYY-MM-DD.html` on Andrew's stamp. HTML is canonical, no `.md` companion.

**Delivery:** one thread, one folder, one branch off `origin/main`. Commit and PR only after Andrew has opened the render in his browser and said go.

---

## Phase 6 — Self-check

| Check | Pass condition |
|---|---|
| **Every number has a query** | No figure appears that was not read this session |
| **Units read, not assumed** | Radius units, micros, conversions vs all_conversions all explicitly handled |
| **Experiments checked** | The experiment and base/trial queries were run and the answer recorded, including "none" |
| **Coverage matrix complete** | Every in-scope campaign appears against every shared list |
| **Architecture is decided** | The document says what the account should be, not only what it is |
| **Ladder rung is real** | The current bid strategy came from 2.1, not from a prior document |
| **Measurement gap named** | The distance between bid signal and business lead is stated, even if zero |
| **Asset set specified** | Every campaign in the architecture states its asset set against the build standard |
| **Nothing applied** | No mutate ran with `--apply`. Any payload referenced was dry-run only |
| **Writing standard** | Three-pass proof applied: AusE, anti-AI tells, brand hygiene |

Then spawn `cmo-verify` (`agentType: "cmo-verify"`, read-only) against the deliverable, the brief and the entity evidence file. On FAIL, fix every `must_fix` item before the document is presented as final.

---

## Chains to

- `/google <brand>` — run the listener against this strategy to see where the account has drifted from it
- `/cmo` — write the RSA copy the architecture calls for
- `/seo` — where a cluster is better answered organically than bought
- `/report` — document the session

## What this command does NOT do

- Apply anything to the account (execution is a separate authorised pass)
- Weekly performance reporting (use `/google`)
- Write ad copy (use `/cmo`)
- Meta, LinkedIn or Microsoft strategy (use `/meta`, or build the sibling)

---

## Core Writing Standard

This command produces written output. Before any draft is presented, written to disk, or marked APPROVED, apply the Core Writing Standard: `skills/copywriting/Proofread-Anti-AI-Standard.md`.

Pass 1 AusE spelling. Pass 2 anti-AI tells. Pass 3 brand hygiene. Three or more AI-tell patterns in one section equals full rewrite, not find-and-replace.

See `protocols/output-protocol.md` § Core Writing Standard for the cross-phase enforcement protocol.

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
