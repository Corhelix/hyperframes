---
name: cro
description: On-page conversion rate optimisation pass.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - one brand page is assessed for conversion with live evidence
  does_not_fire_when:
    - new copy is being written -> /cmo
    - the page does not exist yet -> /seo-webpage or /cmo
  loads:
    always:
      - command-includes/_VERIFICATION-STANDARD.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: issues
      is: each with the rendered evidence, a LIFT-scored fix and a priority
    - id: coverage
      is: which sources were pulled, when, and what could not be resolved
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
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

## VERIFICATION — what "verified" means here

Canonical text: `command-includes/_VERIFICATION-STANDARD.md`. Summarised here so this
command is self-contained; that file is the authority if the two ever disagree.

This run is diagnostic and read-only, so what needs verifying is the **evidence**, not
a build. Verified means a person performed it and watched the result. A flag inferred
from a static parse, or a metric quoted from a collector run that failed, is untested,
and the word "untested" appears beside it.

**Lens 2 — Visual, and it is the load-bearing one here.** Judge the rendered page, not
the markup. The collector already flags that GHL forms render in an iframe and are not
statically countable — that is this lens stating itself. Anything the static parse
cannot see (real field count, competing CTAs below the fold, a control that draws but
sits beneath something else, text colliding at a narrower width) is resolved in a real
browser at the stated viewports or it is not resolved. Capture every reachable state,
including the ones nobody remembers: a validation error, a slow response, a failed
submit.

**Lens 3 — Journey.** The fill-submit-verify is a journey walk and should be treated
as one: every gesture performed, in one sitting, ending in an observed confirmation.
It beats GA4 `form_submit` precisely because it observes the outcome rather than
trusting an event that misfires on GHL and AJAX forms. Stop at the first gesture that
cannot be completed and report from there; a form broken at step 3 is a more useful
finding than a LIFT score on a page nobody can submit.

**Read `manifest.json` before quoting any number.** A failed collector pull leaves no
file, and an absent file read as a zero is how a wrong conversion rate reaches a
report. Carry every failure into the output as a named gap.

Every issue carries an evidence path — the capture, the flag, or the metric with its
pull date. An issue nobody captured is a rumour, and a ranked list of rumours is worse
than a short list of proven ones.

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
