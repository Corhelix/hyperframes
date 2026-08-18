---
description: SEO platform agent: audit, strategy and on-page work.
argument-hint: "[context or target]"
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
