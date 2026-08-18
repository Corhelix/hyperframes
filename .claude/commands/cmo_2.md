---
description: CMO workflow, fresh-eyes variant: spawns a clean-context strategist, then renders from its spec.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/cmo_2.md — .claude/commands/cmo_2.md must match exactly -->
# /cmo_2 — CMO fresh-eyes launcher (A/B test against /cmo)

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write, run the file-home gate: read GitHub first, resolve and confirm the dated task folder against `repo-map.json`, create it in the real repo, then cut a feature branch. Full text in `protocols/file-home-gate.md`. Enforced at commit by the pre-commit lane-guard.

EXPERIMENTAL. Runs the CMO workflow as a FRESH, ISOLATED Opus subagent (`cmo-spine`) instead of inline in this thread. Built to test the fresh-eyes architecture alongside the normal `/cmo`. Run both on the same brief and compare drift, token cost, and output quality.

You are the LAUNCHER, not the CMO. Do NOT do the CMO reasoning in this thread. The thinking happens in a clean room. Your job is to orchestrate, gate, and deliver.

## The two rules that make this work (read before Step 1)

A 20-run audit of every CMO era (`Corhelix/clarity-os-docs -> docs/clarity-os-tooling/tasks/2026-05-11-printing-press-strategy-research/audit-cmo-flow-2026-06-16/CROSS-REFERENCE.md`) found one failure repeated across the command's whole life: **the spine is substitutable, so it gets substituted.** Launchers swapped in Explore or general-purpose agents, or ran the analysis inline, and only the two runs that actually spawned `cmo-spine` produced a clean accepted output. These two rules are not style — they are the fix:

1. **The spine is `cmo-spine` or it does not run.** You may NOT substitute an Explore agent, a general-purpose agent, or inline reasoning for the spine. If the task is not CMO copy, you refuse (Step 1), you do not adapt the spine to another domain.
2. **No deliverable ships without a validated content-spec.** This is now real, not self-attested: `.claude/hooks/cmo-gate.js` (PreToolUse, Node — it runs on this stack; the old bash+jq gate silently never fired because `jq` is absent) blocks the render write until a `content-spec-<date>.json` validating against `protocols/schemas/content-spec-v1.json` exists in the task folder. A run that skipped the spine has no such file, so it cannot render. The gate is the enforcement; these steps are how you satisfy it.

## Step 1 — Resolve inputs (and refuse a non-CMO task)

- `brand` — from the `/cmo_2 <brand>` argument, or ask once.
- `frame_spec_path` — `protocols/frame-specs/<brand-slug>.md` if it exists (check with Glob/Read), else "none".
- `task` — the asset requested. If a task is sitting in the conversation, that is the task; do not expand on it here, just carry it.

**Mismatch refusal (do this first).** If the task is not a marketing/CMO asset — an R&D tax build, a scribe/thought-capture job, a code task, a generic research dump — STOP. Do not arm the gate, do not adapt the spine. Say in one line which command fits (`/cto`, `/rnd`, `/research`, plain chat) and hand off. Run-04 of the audit "adapted the spine to R&D" and burned 34 spawns on the wrong frame; that is the exact move this refusal exists to stop.

## Step 2 — Arm the gate (content-spec required)

Determine the dated task folder first (`<entity>/.../YYYY-MM-DD-<slug>/`) and commit the task/brief into it (`brief-<date>.md`, or the supplied JD as `job-ad-source.md`). Then arm the gate by writing the **per-session** active marker the hook reads (the filename carries your session id so two concurrent `/cmo` sessions never collide):
```bash
echo '{"workflow":"cmo","slug":"<brand-slug>","task_dir":"<absolute task dir>","gates_confirmed":false,"skills_approved":true}' > ".claude/.cmo-active.$CLAUDE_CODE_SESSION_ID.json"
```
(PowerShell: use `$env:CLAUDE_CODE_SESSION_ID`. Env vars do not persist between Bash calls — reference it inline every time.) The gate now blocks any `.html`/`.md` deliverable in the task folder until: a brief exists (> 300 bytes), a `content-spec-<date>.json` validating against `protocols/schemas/content-spec-v1.json` exists, and the checkpoint is human-confirmed. The brief, the content-spec and the markers are always writable — only the deliverable is blocked.

## Step 3 — Spawn the fresh-eyes spine (cmo-spine only)

Use the Agent tool to spawn the `cmo-spine` subagent (`agentType: "cmo-spine"`, Opus, read-only, clean context). Pass it ONLY:
> brand: `<brand>`
> frame_spec_path: `<path or none>`
> task: `<the task>`
> Run your doctrine and return the content-spec as structured JSON matching `protocols/schemas/content-spec-v1.json` (frame, analysis with all six 3.1-3.6 points, content_spec, frame_spec_delta, cmo_note).

Do NOT paste prior conversation into the spawn. The whole point is that the spine starts clean — fresh eyes.

**No substitution.** If the spine spawn fails (e.g. "Prompt is too long" in a loaded session, see R3), the fix is a fresh session, NOT a different agent. Spawning Explore or general-purpose in its place is the substitution the audit caught — it does not produce a content-spec and the gate will block your render anyway. Reading brand files yourself in this thread is the inline drift `/cmo_2` exists to prevent.

## Step 4 — Receive, gate, deliver (back in this thread)

The spine returns a content-spec (frame + 3.1-3.6 analysis + content-spec + any frame-spec delta). Then:

1. **Serialise the content-spec to a file** so the gate can validate it (Bash is not gated; only Write/Edit are), into the task folder:
   ```bash
   cat > "<task-dir>/content-spec-<YYYY-MM-DD>.json" <<'EOF'
   { ...the spine's content-spec as JSON, matching content-spec-v1.json... }
   EOF
   ```
   On Windows, heredoc quoting is fragile — write it with the Write tool instead; `content-spec-*.json` is an artefact, never gated.
2. Present the content-spec to the operator for the draft checkpoint, then **WAIT for the operator's typed reply** — do not proceed in the same turn. The gate reads the live transcript and requires a real human reply that lands *after* the content-spec was written; you cannot self-certify past it.
3. On confirm, **lift the checkpoint gate** — re-write the per-session marker with `gates_confirmed:true`:
   ```bash
   echo '{"workflow":"cmo","slug":"<brand-slug>","task_dir":"<absolute task dir>","gates_confirmed":true,"skills_approved":true}' > ".claude/.cmo-active.$CLAUDE_CODE_SESSION_ID.json"
   ```
4. **Adversarial verify.** Spawn `cmo-verify` (`agentType: "cmo-verify"`, read-only) on the content-spec + brief + evidence file. On FAIL, fix the `must_fix` items and re-run before rendering.
5. **Render** the deliverable from the content-spec onto the named canonical template, date-stamped `DRAFT-v0.1-YYYY-MM-DD.html`. Never invent CSS — start from the canonical template file. The gate now permits the write because every artefact is present.
6. If the spine returned a frame-spec delta, persist it to `protocols/frame-specs/<slug>.md` via a Bash heredoc.
7. **Disarm** for the next task: `rm -f ".claude/.cmo-active.$CLAUDE_CODE_SESSION_ID.json"` (and any task-local `.skills-approved`).

## Why this exists

`/cmo` runs inline and inherits this thread's accumulated context — drift risk and token cost both rise with conversation length. `/cmo_2` runs the judgment in a fresh isolated Opus context fed only the frame and the task. If fresh-eyes wins the A/B, this becomes the default and `/cmo` retires; if not, we keep `/cmo`.

## Requirements + caveats

- `CLAUDE_CODE_SUBAGENT_MODEL` must be UNSET (else the env pin forces the spine to haiku regardless of its `model: opus`). Removed 2026-06-02.
- Best tested in a FRESH session. A heavily-loaded session can overflow the spawn ("Prompt is too long"); the restricted toolset on `cmo-spine` mitigates this but a clean session is the right test bed.
- v1 spawns one spine. Tiered haiku readers (brand-reader, lens-reader) feeding the spine are the v2 token optimisation, added once fresh-eyes is validated.
- The independent verify/rate step (audit D7, PRD M3) is not yet wired here. When it lands, it runs between Step 4.2 and 4.3: a separate read-only agent scores the content-spec against the proof standard, the positioning NOT-column, and locked lines, writing the `verify` block of the content-spec before render.

## Agent model defaults (per-spawn)

The spine is the one Opus node — it earns it, it does the hard framing. Set model PER SPAWN via the `model` parameter, never via the global `CLAUDE_CODE_SUBAGENT_MODEL` env var (that pin forces every subagent to one model and is exactly why it stays UNSET here).

When the v2 reader agents land (brand-reader, lens-reader, or any read / research / summarise helper), default them to `haiku`, open each prompt with the tool-discipline preamble, and cap the return at ≤800 words so only the compressed read reaches the spine, never raw file dumps:

> TOOL DISCIPLINE: Use the Grep tool (not Bash grep/rg) for content search. Use the Glob tool (not Bash find) for file discovery. Use Read with limit/offset (not Bash cat/head/tail) for file inspection. Never use Bash for file reads, searches, or discovery.

---

## GATE MECHANICS — the hooks that will deny you

**Arm the frame gate in Phase 1, before any analysis.** `frame-gate-v1.sh` is
inert without `.frame-required`, so skipping this does not run the command
ungated by design — it runs it ungated by accident.

```bash
echo '{"kind":"<system|entity>","target":"<target>"}' > "<session-marker-dir>/.frame-required"
```

Release it only when the analysis is genuinely complete, both fields true:

```bash
echo '{"kind":"<system|entity>","target":"<target>","framing_locked":true,"all_six_complete":true,"as_of":"YYYY-MM-DD"}' > "<session-marker-dir>/.frame-locked"
```

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
