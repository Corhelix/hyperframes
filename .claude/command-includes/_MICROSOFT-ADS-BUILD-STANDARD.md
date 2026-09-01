<!-- Source: slash-commands/command-includes/_MICROSOFT-ADS-BUILD-STANDARD.md — .claude/command-includes/_MICROSOFT-ADS-BUILD-STANDARD.md must match exactly -->

# Microsoft Ads build standard

The physical definition of a complete Microsoft Advertising campaign. Loaded by **both**
`/microsoft` and `/microsoft-strategise`, which is the whole point: the command that specifies a
campaign and the command that grades one read the same file, so the definition cannot drift between
them. The Google equivalent exists because a checklist living inside one command let the other drift
over an account spending real money with blank ad surfaces. Do not copy a row of this into either
command; load it.

Evidence base for every threshold: `projects/command-system/tasks/2026-09-01-microsoft-ads-skill/`.

---

## 1. Import posture — check before anything else

A Microsoft account can be owned by a Google Ads import. If it is, everything below is a
recommendation that reverts on the next scheduled run.

| Row | Standard | Failure means |
|---|---|---|
| 1.1 | No Google import job with `UpdateEntities = true` on a managed account | Google re-asserts bids, budgets, status and targeting nightly; your changes are temporary |
| 1.2 | `PauseNewCampaigns = true` | new Google campaigns go live here with no review |
| 1.3 | `DeleteRemovedEntities = false` | removals in Google silently delete Microsoft entities |
| 1.4 | Manager-account import schedules checked separately | an account-level check alone does not prove an account is import-free |
| 1.5 | No Microsoft campaign shares a name with a Google campaign unintentionally | name match is case-insensitive, merge is automatic, the link is **permanent** |

Safe configuration for a managed account: `NewEntities=true, UpdateEntities=false, PauseNewCampaigns=true`.

## 2. Measurement — the account cannot be graded without this

| Row | Standard | Failure means |
|---|---|---|
| 2.1 | UET tag live and firing | no conversion data, no remarketing, no automated bidding eligibility |
| 2.2 | At least one conversion goal with conversions in the last 30 days | goals exist on paper only |
| 2.3 | Conversion goal attribution not silently last-click after an import | efficiency numbers are being read against a changed model |
| 2.4 | `ReportTimeZone` set explicitly on every report | the API default is US Pacific and misdates every Australian report |
| 2.5 | UET verified independently of the Google tag | a working Google tag says nothing about Microsoft measurement |

## 3. Ad surface — per enabled campaign

| Row | Standard | Failure means |
|---|---|---|
| 3.1 | **Logo asset present on every search campaign** | ad is ineligible for Copilot placements, which cannot be opted out of and report no metrics |
| 3.2 | Business name populated | responsive surface incomplete |
| 3.3 | **Callouts: between 2 and 20 associated** | at one or fewer, **no callout serves at all**. Silent total failure, not a partial one |
| 3.4 | Minimum 6 sitelinks, destinations verified live | free surface unused; a 404 sitelink is worse than none |
| 3.5 | Both sitelink descriptions populated | display text drops from 35 to 25 characters when descriptions are set; plan for it |
| 3.6 | No duplicate sitelink destinations within a set | the set collapses to fewer effective links |
| 3.7 | Structured snippet values match their header | rejected or nonsensical to a reader |
| 3.8 | Extensions match current ad copy | stale offer, editorial risk |
| 3.9 | Callouts add rather than repeat the headlines | wasted surface |

## 4. Ad copy — Microsoft RSA limits, which are not Google's

| Row | Standard | Failure means |
|---|---|---|
| 4.1 | 3 to 15 headlines, 30 final characters each | under-filled RSA, poor combination coverage |
| 4.2 | 2 to 4 descriptions, 90 final characters each | as above |
| 4.3 | **Maximum 3 active RSAs per ad group** | over the platform limit; a Google import routinely breaches this |
| 4.4 | Path 1 and Path 2 at 15 final characters, domain plus paths 67 or fewer | truncation |
| 4.5 | Emoji and double-width characters counted at double | silent overflow past the limit |
| 4.6 | Final URL host 35 characters or fewer where imported | imported URLs over that are truncated and 404 |

## 5. Targeting and structure

| Row | Standard | Failure means |
|---|---|---|
| 5.1 | Exact-match coverage on head terms | paying broad-match prices for known intent |
| 5.2 | Negative keyword list coverage on every campaign | cross-campaign waste; cap is 20 lists per account, so plan the architecture |
| 5.3 | Negative match types verified after any import | import can change broad to phrase silently |
| 5.4 | Device criteria complete: `Computers`, `Smartphones` and `Tablets` all present, or none at all | a partial set is invalid and no device targeting applies |
| 5.5 | Location targets at the intended level, not expanded to parents | import expands suburb targets to state; spend leaks |
| 5.6 | Age band coverage checked for the missing 45 to 54 band after an import | Google's bands do not map; a demographic gap opens silently |
| 5.7 | LinkedIn audience paired with a negative bid adjustment elsewhere, where a filter was intended | LinkedIn targeting is a **bid modifier, not a filter**; the campaign is spending against everyone |

## 6. Bidding — the documented floor

| Row | Standard | Failure means |
|---|---|---|
| 6.1 | **30 conversions in 30 days** before any automated bid strategy | Microsoft documents that automated bidding stops optimising below this. Below the floor the honest recommendation is Enhanced CPC |
| 6.2 | Target CPA used on Search only | not available elsewhere |
| 6.3 | Share-of-voice goals not expressed as a bid strategy | **there is no Target Impression Share strategy on this platform.** Say so rather than substituting a proxy silently |

## 7. Network and reporting truth

| Row | Standard | Failure means |
|---|---|---|
| 7.1 | Desktop and mobile reported separately, never blended | Bing's Australian share is roughly 16.5% desktop against 0.54% mobile, a thirty-fold gap. A blended number hides the entire strategic question |
| 7.2 | Which share figure is being quoted is named | StatCounter Bing-branded (16.5% desktop) and Microsoft's Comscore network figure (26.6% desktop) measure different things. Both are defensible; quoting one unlabelled is not |
| 7.3 | Search-partner waste addressed by negatives and bid adjustments, not by an opt-out | there is no true partner opt-out; `SyndicatedSearchOnly` was removed July 2024. Recommending a control that does not exist wastes the operator's time |
| 7.4 | `Potential Incomplete Data` read before any number that must reconcile | invoice and report disagree, and nobody knows why |

## Measurement traps that produce false findings

- **`AccountNumber` is not `AccountId`.** The eight-character value in the web UI is the number. The
  API only accepts the Id. A finding keyed to the wrong one is unverifiable.
- **An account is reached *through* a customer.** Cache which `CustomerId` each `AccountId` resolves
  through. Unlike a Google customer ID, it is not globally addressable.
- **Partial update is not partial success.** Ad extensions and the whole Customer Management service
  do full replacement. A remediation that sends fewer fields there deletes the omitted data.
- **`Disapproved` is ambiguous.** Always pair the editorial status with the editorial reasons; the
  status alone does not say what failed or whether it is fixable.
- **Report `Success` with a nil download URL means no data, not an error.** Do not report it as a
  failure.
- **207 carries two distinct meanings.** Never key logic on a numeric error code alone.
- **No published rate limits exist.** Microsoft states the Bulk and Reporting limits are internal and
  publishes no figure for Campaign Management. Any requests-per-minute number circulating elsewhere
  is not from current documentation. Back off on 117, 4204 and 207.

## Three unsettled contradictions

Official Microsoft sources disagree with each other on these. Take the conservative value, verify
in-account, and report what you observed with the date. Do not cite either source as settled.

1. Bulk upload row cap: 4 million on two pages, 2.5 million on a third.
2. Report request validity: 2 days in the guide, 1 day in the operation reference.
3. Whether campaign and ad-group level negatives import from Google: the docs imply yes via
   `NewNegativeKeywordsForExistingParents`, support states only negative keyword *lists* import.
