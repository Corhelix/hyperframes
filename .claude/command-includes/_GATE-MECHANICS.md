<!-- Source: .claude/commands/_GATE-MECHANICS.md — canonical. Inlined into every
     command the hooks actually gate. If you change it here, change it in every
     command that carries the block, and say so in the commit. -->

# Gate mechanics — what actually enforces these commands

Applies to `/cto`, `/cmo`, `/cmo_2`, `/audit-cto`, `/audit-cmo`, `/build-plan`,
`/prd-build`, `/auto-sow`, and anything that writes a file.

Nothing here is a promise made in a command file. All of it is code that returns
`deny`, and a command that omits it does not become unenforced — it becomes
**undocumented while still being denied**. That is the failure this block exists
to prevent: the 2026-08-14 re-audit found a rewritten `/cto` that never armed the
frame gate, so `frame-gate-v1.sh` sat inert for the one command it was built for.

## The four markers

Per-session, under `<root>/.claude/sessions/<session_id>/`, where `<root>` is
`$PROJECT_DIR/.claude` when the project has one, else
`$HOME/Documents/DEFAULT-CLAUDE/.claude`. The SessionStart hook creates the
directory and injects the exact paths into session context — use those, do not
guess them.

| Marker | Written when | Gate that reads it |
|---|---|---|
| `.entity-loaded` | entity context loaded, or `no-entity` for platform work | `skills-gate-v2.sh` |
| `.skills-approved` | skills proposed and approved | `skills-gate-v2.sh` |
| `.frame-required` | **Phase 1, before any analysis** | `frame-gate-v1.sh` |
| `.frame-locked` | all six analysis points complete | `frame-gate-v1.sh` |

Legacy `.claude/.entity-loaded` and `.claude/.skills-approved` are **ignored**.
Writing there satisfies nothing.

## Arm the frame gate in Phase 1

`frame-gate-v1.sh` is **inert without `.frame-required`**. A command that skips
this step is not running ungated by design — it is running ungated by accident,
and every write in the session goes unchecked.

```bash
echo '{"kind":"system","codebase":"<path>","target":"<path>"}' \
  > "<session-marker-dir>/.frame-required"
```

Release it only once the analysis is genuinely complete:

```bash
echo '{"kind":"system","target":"<codebase>","framing_locked":true,
       "all_six_complete":true,"frame_spec_ref":"derived",
       "as_of":"YYYY-MM-DD","timestamp":"<ISO8601>"}' \
  > "<session-marker-dir>/.frame-locked"
```

Both fields must be `true` or the gate keeps denying. If any analysis point is
missing, do not lock — go back and finish it.

## Load order, enforced on reads

`command-load-order-gate.py` arms off the operator's own typed prompt
(UserPromptSubmit), not off anything the model does, and denies out-of-order
reads while armed. Phase 1 runs 1.1 → 1.2 → 1.3 → 1.4 → 1.5 in that order, and
1.1 ends by **waiting for a typed answer**.

A denied Read is the gate working, not a tooling failure. Present the Step 1.1
gate and stop. Emergency escape hatch: `CLARITY_LOAD_ORDER_GATE=off`.

## File home, enforced on writes

`clean-path-gate.py` enforces `github.com/Corhelix/<repo>/<path>` ==
`~/Documents/CLEAN/<repo>/<path>`. There is no third location: worktrees, `-wt`
directories, the session scratchpad, `/tmp` and the Desktop are all denied.

Since 2026-08-14 the first path segment must also be a **real repo** — named in
`protocols/repo-map.json` or present on disk with a `.git`. An invented directory
under CLEAN is denied, where it used to pass silently.

## Tool discipline, enforced on Bash

`block-bash-fileops.py` denies `cat`/`head`/`tail`/`less`/`more`, `grep` and
friends, and `find` — **in every pipeline position**, and including
path-qualified forms (`/usr/bin/grep`), alias escapes (`\grep`), transparent
wrappers (`env grep`, `xargs grep`) and quoted payloads (`bash -c "cat …"`).

Use Read, Grep and Glob. To bound payload, use Read's `offset`/`limit` or Grep's
`head_limit` — piping into `head` is not an approved substitute, and is denied.
The bypass is an operator control exported into Claude Code's environment; an
inline `BASH_FILEOPS_BYPASS=1 …` prefix does not work and is not honoured.

## If a gate denies you

Read the denial. Every one names the exact path to write or the exact tool to
use. Satisfying a gate by working around it — writing the marker without doing
the work, or reaching for a wrapper the gate does not yet catch — is the drift
the gates exist to catch, and it is caught in audit.
