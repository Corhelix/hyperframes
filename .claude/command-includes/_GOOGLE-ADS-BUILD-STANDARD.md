# _GOOGLE-ADS-BUILD-STANDARD — what a complete Google Ads campaign contains

**Shared include. Loaded by `/google` and `/google-strategise`, and by any command that
proposes, grades or rebuilds a Google Ads campaign.**

This is the physical definition of a finished campaign. It is brand-agnostic — the same
checklist applies to the first build and the fiftieth listener pass, on any account.

> **Why this is a shared include, not a section inside `/google`.** On 2026-08-28 an audit of
> Axia Office found Lane 2 Managed Print spending $237 a week with **zero sitelinks, no
> structured snippet, no business logo and no business name**, and a Demand Gen campaign — a
> visual-first channel — running with **no images, no logo and no callouts at all**. The
> checklist that would have caught it existed, but only inside `/google` Phase 4.
> `/google-strategise` had no concept of assets, so a strategy could be written for that
> account, specifying architecture and budget, without anything flagging that half the ad
> surfaces were blank. A strategy cannot be written against a standard the command does not
> carry. Both commands now load this file.

---

## The standard

| Check | What fails without it | How to verify |
|---|---|---|
| Full asset set on every enabled campaign, at every level it applies | One campaign carries image assets, a business logo, business name and a structured snippet; another, often holding the larger budget, carries none. A missing logo or image is not cosmetic — it is the account leaving surfaces unused that cost nothing to fill | List assets at account, campaign and ad-group level. Confirm image assets (minimum 3), a business logo, business name, at least 4 callouts, one structured snippet header with 3+ values, and a call or lead-form asset wherever the lane converts on a call or a form — on **every enabled campaign**. Presence alone is not enough; count against the minimum |
| Minimum 6 sitelinks, verified destinations | A campaign runs 2 or 4 sitelinks against a plan of 6, or a sitelink points at a page with no real content | Count live sitelinks per campaign. Open every destination and confirm substantive content. An HTTP 200 is not proof of a working page; follow redirects and check hop count |
| Sitelinks match the lane, not just the count | A Canon campaign runs zero Canon sitelinks; a Sharp lane runs zero Sharp. The count target can be met while the account still fails | Every sitelink on a campaign must be relevant to that campaign's own product or service lane. A lane-neutral sitelink (a shared quote form) can sit anywhere; a brand- or product-specific one may only sit on its own lane |
| No duplicate destinations within one sitelink set | Google typically shows four sitelinks at once. Two pointing at the same URL wastes a slot | Diff destination URLs within each campaign's set. Two links to one page is allowed only when the link text and descriptions serve genuinely different intent |
| Both sitelink descriptions populated | A sitelink with one description or none renders smaller and carries less | Every sitelink has description1 and description2 |
| Exact-match coverage for every head term | Without an exact-match variant in its own lane, a head term's phrase match in a neighbouring lane can win instead, so the account bids against itself. Quality Score is also computed on *exact-query* history, so phrase-only keywords may never earn a score at all | For every head term, confirm an exact-match keyword exists in the ad group it belongs to. Pull search terms by lane and confirm each head term's clicks land in the ad group built for it |
| RSA copy carries no near-me phrasing | "Near me" assumes a walk-in visit. For a lease, service or B2B account with no retail premises it misrepresents the offer | Read every live headline and description for "near me", "nearby" or other local-visit phrasing |
| Extensions match current ad copy | A claim removed from ad copy, including a factually wrong one, keeps serving in a callout or sitelink | After any ad-copy change, diff live extension text against current copy rulings. Extensions carry no serving risk, so they get fixed first, not last |
| Callouts add, they don't repeat | Callouts duplicate headline text, or near-duplicate each other, wasting the surface | No callout repeats text already in a headline. No two callouts in a set are near-duplicates. Read the whole set together |
| Structured snippet values match the header | A "Service catalog" header carrying ad headlines rather than services reads as noise and may be disapproved | The values under a header must be instances of that header's category. Services under Services, brands under Brands, models under Models |
| Extensions meet the writing standard | An extension carries an exclamation mark, or a contentless line such as "Contact and save today" | Run extension copy through the same proofing pass as ad copy, not a lighter one |
| Non-www canonical, always | Mixed www and non-www final URLs cause a redirect hop and inconsistent tracking within one account | Check every final URL and sitelink URL. None may use www. None may resolve through more than one redirect hop |
| Final URL matches the lane's intent | A Canon ad sending traffic to a generic quote page, or a lease ad landing on a purchase page, breaks the promise made in the click | Open every lane's final URL and confirm the landing page answers the specific query that ad group targets |
| Every enabled campaign carries the full negative-list set | A campaign created after the shared lists exist inherits none of them | Build a coverage matrix: lists down the side, campaigns across the top. Every campaign gets every list unless there is a written reason it does not |

## Measurement traps that produce false findings

- `keyword_view` folds ad-group negatives into its counts. Filter `ad_group_criterion.negative = FALSE`, or counts read roughly three times too high.
- Filter `ad_group.status = 'ENABLED'` as well as campaign and ad status. Dormant ad groups leak in and produce phantom landing pages and phantom assets.
- Negative-conflict checks must be scoped by campaign and ad group. Unscoped, a clean account reads as majority-blocked.
- Counting `<form>` tags misses lead capture inside a cross-origin iframe (a GoHighLevel quiz, for example). Check for iframes and visible inputs before concluding a page has no conversion path.
- Asset counts must be measured **per campaign**, not by summing campaign-level and account-level rows. Mixing the two makes every campaign look identically equipped.

## How each command uses this file

| Command | Use |
|---|---|
| `/google` | **Grade** the live account against every row. Findings fold into the ranked report as their own block, not a footnote |
| `/google-strategise` | **Specify** against it. Any architecture the strategy proposes states the asset set each campaign will carry. A strategy that names campaigns and budgets but no assets is incomplete |
