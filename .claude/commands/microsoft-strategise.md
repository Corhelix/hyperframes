---
name: microsoft-strategise
description: Microsoft Advertising account strategy of record: whether to run the platform at all, then what the account should be.
argument-hint: "[brand or account id]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - the Microsoft Ads strategy of record is set
  does_not_fire_when:
    - campaigns are being built -> /microsoft
  loads:
    always:
      - command-includes/_MICROSOFT-ADS-BUILD-STANDARD.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: strategy_of_record
      is: the account's structure and budget logic, with what it rules out
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- Source: slash-commands/microsoft-strategise.md — .claude/commands/microsoft-strategise.md must match exactly -->
# /microsoft-strategise — Microsoft Ads account strategy of record

Decides what a Microsoft Advertising account **should be**: whether the platform is worth running for
this ICP at all, then architecture, intent clusters, budget, the bidding ladder, negative
architecture, audience strategy and measurement truth. `/microsoft` reports how the live account
performs against what this command decides. Run this first.

**ARGUMENT:** a brand slug or a Microsoft `AccountId`.

## HARD RULE — read-only, always

This command produces a strategy document. It reads the account to ground the strategy in reality and
changes nothing.

## The question this command must answer before any other

**Should this account run Microsoft Ads at all?**

`/google` never has to ask this, because Google is where the demand is. Microsoft in Australia is a
different proposition and the honest answer is sometimes no. Answer it explicitly, first, in the
strategy document, and show the working:

- **Bing's Australian share is roughly 16.5% of desktop and 0.54% of mobile** (StatCounter, August
  2026). Microsoft's own Comscore-derived figure of 26.6% desktop counts the whole Microsoft Search
  Network rather than Bing-branded search. Both are defensible and they measure different things.
  Name which you are using.
- **If the ICP is mobile-first, Microsoft reaches almost none of them here.** That belongs at the top
  of the strategy, not buried in a device table.
- **The case for Microsoft is usually one of three things**: desktop-heavy B2B intent, LinkedIn
  profile targeting that Google cannot match, or cheaper clicks on head terms an account is already
  losing on Google. If none of the three applies, say so and recommend against.
- **A thin account will not clear the 30-conversion floor**, so automated bidding will not optimise.
  Factor that into the forecast rather than assuming Google-equivalent performance at lower cost.

An enthusiastic Microsoft strategy for a mobile-first consumer brand is the failure mode this section
exists to prevent.

## DRIFT DETECTION — read before doing anything

- **You are about to port the Google strategy.** A Microsoft account is not a Google account with a
  smaller budget. Different bid strategies, different limits, different network, different audience
  capability. The Google Ads import makes porting technically easy and strategically lazy.
- **You are about to recommend the Google import as the build method.** Read § Import strategy below
  before you do. It is a legitimate tool with a documented failure mode, and the default settings are
  the wrong ones.
- **You are about to recommend a share-of-voice bidding approach.** There is no Target Impression
  Share strategy on this platform.
- **You are about to scope a LinkedIn company list as an upload.** It is manual entry only, capped at
  1,000, and it is a bid modifier rather than a filter.

## Phase 0 — Doctrine load (mandatory, before anything else)

Run `_shared/card-awareness-context-load.md` in full, then load
`command-includes/_MICROSOFT-ADS-BUILD-STANDARD.md`. The build standard is shared with `/microsoft`
and is what makes "build a complete campaign" a specifiable instruction rather than a wish.

## Phase 1 — Scope and brand kit

Resolve the ICP, the primary goal, the conversion-truth metric and any scope exclusion from the card.
Establish whether the ICP is desktop-reachable, because the whole strategy turns on it.

## Phase 2 — Account reality sweep (read-only, mandatory, no shortcuts)

```bash
msads doctor
msads accounts
msads import-jobs --account <id>
msads campaigns --account <id>
msads report --account <id> --timezone SydneyAustralia --complete-only
```

If the account does not exist yet, this phase produces a greenfield brief instead, and every
subsequent phase is stated as a specification rather than a gap.

## Phase 3 — Intent clustering

Cluster head terms by intent and commercial value. Microsoft's keyword volumes are lower, so clusters
that are viable on Google may be too thin here to justify their own ad group. Consolidate more
aggressively than the Google structure and say why, rather than mirroring the Google account and
producing twenty ad groups with three impressions each.

## Phase 4 — Strategic analysis (complete all seven, do not abbreviate)

1. **Platform case.** The go or no-go from the section above, with the working shown.
2. **Account architecture.** Campaign and ad-group structure, against the 10,000 campaign and 20,000
   ad-group-per-campaign limits, and consolidated for lower volume.
3. **Budget allocation.** Including whether Microsoft earns its budget against the same money spent
   on Google, which is the real alternative.
4. **Bidding ladder.** Explicitly against the **30 conversions in 30 days** floor. Below it, Enhanced
   CPC, stated as the correct choice rather than a fallback. Note that Target CPA is Search only and
   Target Impression Share does not exist here.
5. **Negative architecture.** Against the **20 negative-keyword-lists-per-account** cap, which is a
   real design constraint and is tighter than Google's. Plan the list structure before creating any.
6. **Audience strategy.** Including whether LinkedIn profile targeting justifies the platform on its
   own. If so, design it as a bid modifier with negative adjustments elsewhere, since it does not
   filter, and scope the company list as manual data entry within the 1,000 cap.
7. **Measurement truth.** UET tag, conversion goals, and which metric is the truth. The UET tag is a
   separate implementation from the Google tag; never assume it exists because Google's does.

## Phase 5 — Import strategy (Microsoft-specific, no Google equivalent)

The Google Ads import is fully API-controllable and is the fastest way to stand an account up. It is
also the most common way these accounts break. Decide explicitly, in the strategy document, which of
three postures applies, and record the reasoning:

| Posture | Configuration | When it is right |
|---|---|---|
| **One-off seed** | run once, `UpdateEntities` irrelevant after | the account will be managed natively from here. **Default recommendation for any managed account.** |
| **Scheduled, Microsoft-owned** | `NewEntities=true, UpdateEntities=false, PauseNewCampaigns=true` | new Google campaigns should flow in, but Microsoft-side optimisation must survive |
| **Scheduled, Google-owned** | Microsoft's defaults, `UpdateEntities=true` | only when nobody will ever optimise the Microsoft account natively, and the client accepts that. Say that out loud in the document. |

**Never leave the defaults in place by omission.** `UpdateEntities` and roughly 45 sub-flags default
true; `PauseNewCampaigns` defaults false. Microsoft's own help article concedes the import "may
overwrite existing campaign data, this includes bids, budgets, and settings", and a Q and A thread
runs from 2020 to 2026 including a 2026 case of three billing cycles of unwanted spend with the
refund declined. There is no undo beyond a 30-day per-entity change history.

Also decide and record: who mints the import credential. It is UI-only, interactive, and bound to the
Microsoft user who created it. Rotate that identity and every scheduled job breaks.

## Phase 6 — Output

Strategy of record, branded HTML per the output conventions, filed to the owning repo resolved from
`protocols/entity-repo-map.md`. Leads with the platform go or no-go, not with the tactics.

## Phase 7 — Self-check

- Did the document answer whether to run the platform at all, before describing how?
- Is every share figure labelled with which measurement base it came from, and split by device?
- Is the bidding recommendation checked against the 30-conversion floor with the account's actual
  conversion volume?
- Is the import posture decided explicitly rather than left to defaults?
- Is any threshold quoted as observed when it is only documented?

## Chains to

`/microsoft` (grade the live account against this) · `/cmo` (messaging above the account) ·
`/seo` · `/report`

## What this command does NOT do

- It does not write to the account. Nothing here mutates.
- It does not close the Bing Webmaster Tools gap.
- It does not cover Microsoft Advertising Scripts authoring, though it may recommend Scripts as the
  home for in-account automation.

## Core Writing Standard

Three passes on every text artefact before delivery: Australian and UK English, anti-AI-tell removal,
brand hygiene. Three or more AI tells in a section means rewriting the section, not a find-replace.
Source: `skills/copywriting/Proofread-Anti-AI-Standard.md`.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
