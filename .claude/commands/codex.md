---
description: /codex.
argument-hint: "[context or target]"
---
# /codex

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write, run the file-home gate: read GitHub first, resolve and confirm the dated task folder against `repo-map.json`, create it in the real repo, then cut a feature branch. Full text in `protocols/file-home-gate.md`. Enforced at commit by the pre-commit lane-guard.

Purpose: route Codex into the canonical DEFAULT-CLAUDE governing layer without duplicating command, viewport, protocol, identity, or skill files.

Canonical root:

`.`

## Usage

`/codex <mode> <task>`

Examples:

- `/codex cto audit this repo`
- `/codex cmo review this landing page`
- `/codex n8n design a GHL workflow`
- `/codex review this document using CMO + Document`
- `/codex router handle this task through normal intake`

## Routing

If `<mode>` matches a slash command, load and follow:

`slash-commands/<mode>.md`

Aliases:

- `strategize` -> `slash-commands/strategise.md`
- `router`, `normal`, `intake` -> `ROUTER.md`

If `<mode>` matches a viewport, load the viewport and follow normal routing:

- `cmo` -> `viewports/cmo.md`
- `cto` -> `viewports/cto.md`
- `pm` -> `viewports/pm.md`
- `research` -> `viewports/research.md`
- `document` -> `viewports/document.md`

If `<mode>` matches an identity, load:

- `identities/<mode>/IDENTITY.md`
- `identities/<mode>/skills.txt`

Then load any required overlays or skills referenced by that identity.

## Rules

- Do not duplicate source files into this command.
- Reopen canonical files by path when needed.
- If a slash command is selected, the slash command file is authority.
- If no slash command is selected, use `ROUTER.md`.
- Software work loads `identities/overlays/software-build-process.md`.
- Entity work loads `protocols/entity-repo-map.md`.
- Active Codex system/developer instructions remain higher priority than this workspace command.

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
