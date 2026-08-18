---
description: On-page conversion rate optimisation pass.
argument-hint: "[context or target]"
---
# /cro — On-page CRO platform-agent (on-demand run)

Run the **on-page CRO listener agent** for one brand's page, here in Claude. Same spine that deploys to Hermes: brand kit → collect (GA4 funnel + Clarity friction + a rendered snapshot) → reason with `page-cro`/`form-cro` + LIFT/ICE/PIE → report. **Read + suggest only; diagnostic, not experimentation.**

**ARGUMENT:** `<brand>` = `axia` | `vlc` | `hcc`  and a `<url>` (the page to audit)

---

## Phase 1 — Brand kit (the lens)

Load the brand pack for goals + lead definition (Axia = GHL form-fill; VLC/HCC = enquiry, never `purchase`) + banned language. GA4 property + GHL location come from the pack.

## Phase 2 — Collect (evidence)

- **One-run evidence collector (live now)** — gathers everything the doctrine reasons over as DATA, not a checklist:
  ```
  python3 projects/marketing-agent-system/tasks/2026-07-21-platform-agent-system/build/cro-listener/cro_collector.py \
      --url <url> --property-id <ga4-id> --lead-event generate_lead --start 90daysAgo --end yesterday
  ```
  Returns graded `flags[]` over four sources:
  1. **GA4 landing-page performance** (`ga4-cli report`, path-filtered) — sessions, key events, **conversion rate**, engagement %, bounce %, avg session. *(Verified live on Axia `/photocopier-leasing-in-sydney`: 335 sessions, 0.9% CR, 63.9% bounce.)*
  2. **GA4 funnel drop-off** (`ga4-cli funnel`, real `runFunnelReport`) — session_start → viewed-this-page (`pageLocation` CONTAINS path — note: `pagePath` is NOT valid inside funnel steps) → the lead event. *(Verified: 352 page views → 3 leads = 99.1% page-to-lead drop.)* Pass `--lead-event` to match the property's real key event (Axia = `generate_lead`; VLC/HCC = enquiry, never `purchase`).
  3. **Clarity behavioural friction** (Data Export API) — rage/dead/quick-back/excessive-scroll/script-error counts. Tag is **installed**; set `CLARITY_API_TOKEN` (project JWT: Clarity → Settings → Data Export). NOTE the API is AGGREGATE, project-wide, last 1-3 days, ~10 calls/day — per-page replay stays in the Clarity dashboard.
  4. **Form + CTA structure** (static parse) — native field count vs `form-cro` cost bands, competing-CTA count, click-to-call. **GHL forms render in an iframe → fields are NOT statically countable**; the collector flags the embed and routes field-count to Playwright / the GHL API.
- **Page snapshot + fill-submit-verify (live now):** Playwright MCP — `browser_navigate` + `browser_snapshot` + `browser_console_messages` + `browser_network_requests` on `<url>`. This is where the **GHL form gets its real field count** and a fill-submit-verify (which beats GA4 `form_submit`, misfiring on GHL/AJAX forms) + render regression.
  GA4 property per brand: axia `360021775`, vlc `537597660` (live) / `325023990` (legacy), hcc `304607343`. Full `ga4-cli` surface: `report`/`funnel`/`realtime`/`pivot`/`batch`/`compatibility`/`admin`, all retry/backoff on 429.

## Phase 3 — Reason (doctrine)

Load `skills/digital-marketing/page-cro` + `form-cro` + `conversion-copywriting`. Score the snapshot with **LIFT** (Value Prop / Relevance / Clarity / Urgency / Anxiety / Distraction) + **ICE** + **PIE**. Apply `form-cro` field-cost bands (3 / 4–6 / 7+ fields → 10–25% / 25–50% loss). Rank issues. Tag confidence. `[SILENT]` if the page is clean.

## Phase 4 — Report (format-out)

Ranked CRO report: each issue = what + evidence (the rendered surface / friction metric) + a LIFT-scored fix + priority. No live-page writes. Live A/B serving and heatmap replay are separate paid/build decisions, not this run.

## Notes

- Only Playwright + doctrine run with zero credentials today; GA4 + Clarity are the wiring the deploy adds.
- Same spine deploys to Hermes as `cro-daily-listener.workflow.json` (pending the Playwright-on-VPS test).

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
