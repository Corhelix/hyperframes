---
name: seo
description: SEO platform agent: audit, strategy and on-page work.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - an SEO audit, strategy or on-page pass is the work
  does_not_fire_when:
    - a single page is being built -> /seo-webpage
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: findings
      is: each issue with its page, its evidence, and the fix
    - id: priority
      is: ranked by traffic or conversion effect, not by ease
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

# /seo — SEO platform-agent (on-demand run)

Run the **SEO listener agent** for one brand, here in Claude. Same spine that deploys to Hermes as a daily Telegram listener: load the brand kit (the lens) → collect → reason with `seo-audit` + `ai-seo` doctrine → report. **Read + suggest only. No writes to any live property.**

This is NOT `/seo-webpage` (that BUILDS a page). This AUDITS / LISTENS.

**ARGUMENT:** `<brand>` = `axia` | `vlc` | `hcc`  (optionally a specific `<url>`)

---

## Phase 1 — Brand kit (the lens, read every run)

Resolve the brand's reference sheet. Load the strategy pack for goals / personas / thresholds / banned language, and the GSC site + URL:

| brand | GSC site | URL | pack |
|---|---|---|---|
| axia | `sc-domain:axiaoffice.com.au` | `https://axiaoffice.com.au/` | `../client-projects/wolf-and-eagle/clients/axia-office/tasks/2026-07-21-strategy-pack/DRAFT-AXIA-STRATEGY-PACK-v0.1-2026-07-21.html` |
| vlc | `sc-domain:virtual.hillcrest.qld.edu.au` | `https://virtual.hillcrest.qld.edu.au/` | `../client-projects/edisoned/clients/hillcrest-christian-college/tasks/2026-07-21-strategy-pack-vlc/…` |
| hcc | `https://www.hillcrest.qld.edu.au/` | `https://www.hillcrest.qld.edu.au/` | `.../2026-07-21-strategy-pack-oncampus/…` |

For `vlc` / `hcc`, read `VLC-OPERATING-RULES.md` first (locked rules).

## Phase 2 — Collect (evidence)

- **Zero-auth (live now):**
  ```
  python3 projects/marketing-agent-system/tasks/2026-07-21-platform-agent-system/build/seo-listener/pagespeed_robots_collector.py --url <url> --strategy mobile
  ```
  Returns Core Web Vitals + robots.txt AI-bot access flags. Set `PAGESPEED_API_KEY` env for quota (keyless 429s).
- **GSC signals (ranking / CTR / index / sitemap) — LIVE via `sc-cli`** (verified 2026-07-21: siteOwner on all 3 brands, no `gsc-cli` build needed):
  ```
  sc-cli query --site sc-domain:axiaoffice.com.au --start <YYYY-MM-DD> --end <YYYY-MM-DD> --dimensions query,page
  sc-cli sitemaps list --site sc-domain:axiaoffice.com.au   # returns errors/warnings/lastDownloaded per sitemap
  sc-cli inspect-url --site sc-domain:axiaoffice.com.au --url <page>
  ```
  Brand sites: axia `sc-domain:axiaoffice.com.au`; vlc `sc-domain:virtual.hillcrest.qld.edu.au`; hcc `https://www.hillcrest.qld.edu.au/`.
  **Full `sc-cli` surface (2026-07-21):** `sites list/add/delete` · `query` (with `--paginate`, `--type`, and `--raw '<body>'` for `dimensionFilterGroups`/`aggregationType`) · `sitemaps list/get/submit/delete` (`get` = per-sitemap errors/lastDownloaded) · `inspect-url`. Writes (`sitemaps submit/delete`, `sites`) are dry-run unless `--apply` — stay human-gated. Retry/backoff on 429.

## Phase 3 — Reason (doctrine)

Load `skills/digital-marketing/seo-audit` + `ai-seo`. Rank the collected flags by severity × impact against the brand thresholds. Tag every finding `confirmed / supported / indicated / assumed`. **Never invent a metric not in the collected data.** If nothing crossed a threshold, say `[SILENT]`.

## Phase 4 — Report (format-out)

Output a ranked report: each finding = the offending metric (evidence) + a suggestion + priority. Inline by default; write an HTML report to the task folder only if asked. No sitemap submit / no writes — those stay human-gated.

## Notes

- Runs read-only. The identical spine is `build/seo-listener/seo-zero-auth-listener.workflow.json`, which deploys to Hermes for the autonomous daily run.
- AEO/GEO score + schema-regression are fast-follows once the collectors exist.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
