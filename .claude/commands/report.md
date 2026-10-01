---
name: report
description: Document the current session as a structured report.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - a completed session is documented as a structured report
  does_not_fire_when:
    - the work is still in progress -> /checkpoint
  loads:
    always: []
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: report
      is: what was done, what it was tested against, what it proved, in that order
    - id: untested
      is: anything not observed working, using that word
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

<!-- slash-commands/report.md is canonical; .claude/commands/report.md must match exactly | Skill: session-report.skill.md -->
# /report — Session Report

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write: `git fetch origin`, then confirm the target folder is canonical on GitHub with `git ls-tree -r --name-only origin/main <path>`. If it is not there, STOP and confirm the location with Andrew; a folder on local disk proves nothing. **Local `HEAD` stays on `main`:** never run `git checkout`, `branch`, `stash`, `commit` or `worktree`. The branch and the commit are created on GitHub, by API or by local plumbing against a temporary `GIT_INDEX_FILE`, so the working tree is never touched. Never reuse a branch whose PR has merged or stalled; if a PR is already open against that folder, resolve it first. Full text in `protocols/file-home-gate.md`.

Snapshot THIS thread. Decisions made + files changed + findings + next steps. Nothing else.

---

## Hard rule — thread-only

This command extracts from the **current conversation only**. Do NOT read:
- Template files (no HTML-DECISION-TAGGING-PATTERN.html, no CLARITY-OS-TEMPLATE.html)
- Writing guardrails (no 13-step sweep on session content — Andrew already approved it by producing it)
- Entity files, locked-lines, ICP, positioning (those informed the session; the session is the authority now)
- Memory pointers, MEMORY.md, or auto-memory files
- Prior reports

If something was decided/produced in the session, capture it. If it lives outside the session, link to it — don't re-load it.

The CSS for the report is inlined below. No external scaffold fetch.

---

## Procedure

### Step 1 — Extract from thread

Walk the conversation in order. Build six lists:

| List | What goes in it |
|---|---|
| Task | First user message + slash command invoked. One sentence. |
| What was done | Each tool call that wrote files / committed / pushed / opened a PR. Action + outcome + file path. |
| Decisions made | User stamps (LOCK / approve / "yes" / "do it"), corrections issued, locked choices. Decision + rationale + impact. |
| Files created / modified | Every Write / Edit / Bash that touched disk during the session. File + action + purpose. |
| Findings | Drift modes called out, gaps surfaced, audit results. Severity + what + next action. |
| Next steps | What's pending, what's queued for the next SOW, what was deferred. Checkboxes (open) + checkmarks (done). |

No Step 2 gate. Extract → write → present.

### Step 2 — Write the HTML report

Inline the CSS block below. Do NOT fetch templates.

Output path:
- If a dated task folder exists for the session's primary work → `projects/<entity-or-task>/tasks/<YYYY-MM-DD>-<slug>/DRAFT-REPORT-v0.1-<YYYY-MM-DD>.html`
- Otherwise → `projects/<entity-or-task>/DRAFT-REPORT-v0.1-<YYYY-MM-DD>.html`

After writing: run `open <path>` so Andrew can review in browser.

### Step 3 — Self-check (3 lines, not a full sweep)

- Complete: cold reader understands what happened + what's next?
- Honest: gaps and failures documented, not hidden?
- AU/UK spelling: -ise not -ize, -our not -or, -re not -er.

That's the entire quality check for /report. No 13-step sweep. No banned-vocab regex. The session content is what it is.

---

## Inline CSS block (use verbatim — copy into the report's `<style>` tag)

```css
*{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#0066FF;--blue-light:rgba(0,102,255,.06);--green:#16A34A;--green-light:rgba(22,163,74,.10);--amber:#F59E0B;--amber-light:rgba(245,158,11,.10);--red:#E53E3E;--red-light:rgba(229,62,62,.10);--text:#333;--text-500:#777;--text-400:#999;--border:#E2E6EA;--canvas:#F7F9FA;--radius:14px;--heading:'Montserrat',system-ui,sans-serif;--body:Inter,-apple-system,system-ui,sans-serif}
body{font-family:var(--body);background:#fff;color:var(--text);line-height:1.7;font-size:16px;-webkit-font-smoothing:antialiased}
.banner{background:var(--blue);padding:14px 40px;text-align:center}
.banner span{font-family:var(--heading);font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#fff}
section{padding:48px 48px 32px;max-width:1100px;margin:0 auto}
section.alt{background:var(--canvas)}
h1{font-family:var(--heading);font-size:clamp(28px,3.4vw,38px);font-weight:900;color:#111;line-height:1.05;margin-bottom:12px}
h2{font-family:var(--heading);font-size:clamp(20px,2.4vw,26px);font-weight:800;color:#111;margin-bottom:14px}
h4{font-family:var(--heading);font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--blue);margin-bottom:8px}
p{margin-bottom:12px;color:#4A4A4A;font-size:14.5px}
.eyebrow{font-family:var(--heading);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--blue);margin-bottom:14px}
.rule{height:3px;background:var(--blue);width:56px;margin:14px 0 18px}
.lede{font-size:17px;line-height:1.55;color:var(--text);max-width:840px}
table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin:16px 0}
th{text-align:left;padding:12px 14px;font-family:var(--heading);font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--text-400);background:var(--canvas);border-bottom:2px solid var(--border)}
td{padding:12px 14px;border-bottom:1px solid #F0F2F4;vertical-align:top;color:#4A4A4A;line-height:1.5}
tr:last-child td{border-bottom:none}
.callout{border-radius:var(--radius);padding:18px 22px;margin:14px 0;border:1px solid var(--border);border-left:5px solid var(--blue);background:var(--blue-light)}
.callout.green{border-left-color:var(--green);background:var(--green-light)}
.callout.amber{border-left-color:var(--amber);background:var(--amber-light)}
.callout.red{border-left-color:var(--red);background:var(--red-light)}
.callout h4{margin-bottom:6px}
.callout.green h4{color:#15803D}
.callout.amber h4{color:#B45309}
.callout.red h4{color:var(--red)}
.callout p{margin-bottom:0;font-size:13.5px}
ul.todo{list-style:none;padding:0;margin:8px 0}
ul.todo li{padding:6px 0 6px 28px;position:relative;font-size:14px}
ul.todo li.done::before{content:"\2713";position:absolute;left:0;color:var(--green);font-weight:900;font-size:16px}
ul.todo li.open::before{content:"\2610";position:absolute;left:0;color:var(--text-400);font-size:16px}
code{font-family:'SFMono-Regular',Consolas,Menlo,monospace;font-size:12.5px;background:#f4f5f7;padding:1px 5px;border-radius:3px;border:1px solid var(--border)}
.foot{border-top:1px solid var(--border);padding:24px 48px;text-align:center;background:var(--canvas);margin-top:32px;font-size:12px;color:var(--text-400)}
```

Plus the Google Fonts link in `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

That's the entire visual package. Self-contained.

---

## HTML structure

```
<!DOCTYPE html>
<html lang="en-AU"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Session Report — {{date}}</title>
<link href="..." rel="stylesheet">
<style>{{inline CSS from block above}}</style>
</head><body>
<div class="banner"><span>CLARITY OS · Session Report · {{date}}</span></div>

<section>
  <p class="eyebrow">Session Report · {{date}}</p>
  <h1>{{task one-liner}}</h1>
  <div class="rule"></div>
  <p class="lede">{{2-3 sentence summary of the session}}</p>
</section>

<section class="alt">
  <h4>What was done</h4>
  <h2>Actions + outcomes.</h2>
  <table><thead><tr><th>Action</th><th>Outcome</th><th>File</th></tr></thead><tbody>
    {{rows}}
  </tbody></table>
</section>

<section>
  <h4>Decisions</h4>
  <h2>What got locked.</h2>
  <table><thead><tr><th>Decision</th><th>Rationale</th><th>Impact</th></tr></thead><tbody>
    {{rows}}
  </tbody></table>
</section>

<section class="alt">
  <h4>Files created or modified</h4>
  <table><thead><tr><th>File</th><th>Action</th><th>Purpose</th></tr></thead><tbody>
    {{rows — each file path linked relatively}}
  </tbody></table>
</section>

<section>
  <h4>Findings</h4>
  <h2>What surfaced.</h2>
  {{callout blocks per finding — green/amber/red by severity}}
</section>

<section class="alt">
  <h4>Next steps</h4>
  <ul class="todo">
    <li class="done">{{completed}}</li>
    <li class="open">{{open}}</li>
  </ul>
</section>

<div class="foot">
  <p><strong>Branch:</strong> {{branch}} · <strong>Commit:</strong> {{hash if committed}} · {{date}}</p>
</div>

</body></html>
```

---

## Output location

- **Task folder exists** (from /cmo, /cto, /spec, /prd-*, /auto-sow): `projects/<entity-or-task>/tasks/<YYYY-MM-DD>-<slug>/DRAFT-REPORT-v0.1-<YYYY-MM-DD>.html`
- **No task folder**: `projects/<entity-or-task>/DRAFT-REPORT-v0.1-<YYYY-MM-DD>.html`

When approved: rename to `APPROVED-REPORT-<YYYY-MM-DD>.html`. No `.md` companion (the HTML is enough).

After write: `open <path>`.

---

## What this command does NOT do

- Read templates, guardrails, entity files, memory, or prior reports (zero external file reads — thread is the authority)
- Run a 13-step writing sweep (session content is already approved by being produced)
- Produce new strategic work (use /cmo, /cto, /spec, /build, /auto-sow)
- Capture R&D evidence (use /rnd for ATO-ready documentation)
- Carry decision-tagging UI (deliverables produced IN the session carry their own; the report just links)
- Block on a "confirm scope" gate (extract → write → present in one pass)

---

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
