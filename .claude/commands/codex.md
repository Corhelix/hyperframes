---
name: codex
description: /codex.
argument-hint: "[context or target]"
disable-model-invocation: true

contract:
  writes: true
  fires_when:
    - work is prepared for or executed in the Codex runtime
  does_not_fire_when:
    - the work runs here -> the matching Claude command
  loads:
    always:
      - viewports/cmo.md
      - viewports/cto.md
      - viewports/document.md
      - viewports/pm.md
      - viewports/research.md
    skills: []   # names no skill; see _COMMAND-CONTRACT on Phase 0
  returns:
    - id: prepared
      is: the work packaged so the other runtime can run it without this session
  acceptance:
    - the declared always-loads appear as Read calls in the transcript
    - every claim carries an evidence label per _VERIFICATION-STANDARD Lens 4
  graded_by: none

includes: [_GATE-MECHANICS, _BLOCKED-ACTION]
---

# /codex

> **STEP 0: FILE-HOME GATE (mandatory).** Before any Write: `git fetch origin`, then confirm the target folder is canonical on GitHub with `git ls-tree -r --name-only origin/main <path>`. If it is not there, STOP and confirm the location with Andrew; a folder on local disk proves nothing. **Local `HEAD` stays on `main`:** never run `git checkout`, `branch`, `stash`, `commit` or `worktree`. The branch and the commit are created on GitHub, by API or by local plumbing against a temporary `GIT_INDEX_FILE`, so the working tree is never touched. Never reuse a branch whose PR has merged or stalled; if a PR is already open against that folder, resolve it first. Full text in `protocols/file-home-gate.md`.

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

## Shared blocks

Declared in this command's `includes:`. Read the file when the situation arises.

- `command-includes/_GATE-MECHANICS.md`
- `command-includes/_BLOCKED-ACTION.md`
- `command-includes/_COMMAND-CONTRACT.md` — what the block above means
