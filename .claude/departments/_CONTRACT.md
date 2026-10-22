# Department contract

Every department file in `departments/` follows this shape. No exceptions, because flows are **composed** from these files rather than hand-written, and composition only works if every department declares its boundary the same way.

## Why departments and not skills

Skills are commodity. Kai CMO Harness ships 49 commands, 67 playbooks and 36 checklists; Corey Haines' repo covers conversion, copy, SEO and ads. Any of it can be downloaded this afternoon. None of it knows what a CMO is, which is why both read as execution frameworks with guardrails rather than a model of the role.

The scarce asset is the **lens and the wiring**: the standing questions a role cannot stop asking, and what it hands to whom. That is what this repo holds. Skills sit underneath and are only ever loaded *through* an active department.

## Why the identity cannot live in a command file

From the Hybrid Orchestration strategy, 2026-04-11:

> Context degradation in chat is architectural, not fixable by prompting. After 3-4 feedback exchanges, RLHF training overwrites explicit process instructions. The fix is external process enforcement — flows inject framing per-call, not models remembering instructions.

A department file is therefore **not a document a session is trusted to keep obeying**. It is a `context_ref` the runner injects into every node call. Writing a longer, sterner command file is the approach this architecture already rejected. A 40KB command with eight confirmation gates produces a compliant record of steps taken and no decision.

---

## Part A — the declaration block

Machine-read. This is what lets `flows/` compose and emit a `workflow.json` for the Hermes `workflow-runner`.

```yaml
---
id: cmo                            # registry key, lowercase, stable forever
name: Chief Marketing Officer
one_line: Makes the brand easier to choose, easier to remember, more profitable to grow.

# Which stages this department leads, and where it only advises.
# Leading means it owns the decision. Advising means it is consulted and can object.
# Never make every department equal in every conversation — use the one that matches the stage.
leads: [opportunity, positioning, go-to-market, launch]
advises: [product-definition, experience-design, pricing]

# What this department WANTS before it starts. It is NOT a gate.
# A missing input never halts the work. The department assumes explicitly,
# logs a decision register entry, flags the sensitivity, and proceeds.
# `blocking: true` must be argued, never assumed — see OPERATING-MODEL.md §4.
needs:
  - id: business_objective
    from: ceo                      # a department id, `operator`, or `research`
    is: one sentence naming the commercial outcome
    blocking: true                 # rare. without it there is no goal to serve
  - id: entity_context
    from: operator
    is: the brand's own files — positioning, ICP, proven lines, competitors
    blocking: true
  - id: unit_economics
    from: cfo
    is: payback, margin and pricing sensitivity
    blocking: false                # THE DEFAULT
    if_absent: assume and flag. "I have no financial plan for this" never stops the work

# Who grades this department's output, and what this department grades from below.
reports_to: ceo
grades: [market-diagnosis, belief-gap, copy-production]   # worker outputs it accepts or returns
grading_worker: cmo-audit                                  # the audit node run at promotion

# What crosses the boundary when this department is done. Named artefacts, not "a report".
produces:
  - id: positioning
    is: the position, the comparison set including doing nothing, and who this is not for
  - id: icp_state
    is: what the customer believes today, in their language, and the gap to what we intend

# Where the work goes next, and under what condition. `when` is copied
# straight onto the flow edge, so an unmet condition skips the stage.
hands_to:
  - to: product-manager
    when: problem is validated and a segment is chosen
    carries: [icp_state, positioning]
  - to: ceo
    when: the opportunity needs funding or a trade-off only the founder can make
    carries: [positioning]

# The workers this department can staff. Each becomes a node.
# Tier follows the approved three-tier split (D2): judgement premium, production mid or free.
workers:
  - node: market-diagnosis
    execution_kind: ai
    tier: mid
    is: segments, competitors, category shifts, experience gaps, performance by segment
  - node: positioning-call
    execution_kind: ai
    tier: premium                  # a judgement node. never downgrade this one
    human_gate: true
    gate_note: Andrew confirms the position and the comparison set before anything is built on it
  - node: copy-production
    execution_kind: ai
    tier: free
    is: drafting against an already-decided position

# Skills this department may pull, only ever through its own lens.
skills: [copywriting/conversion, copywriting/anti-ai-standard, marketing/positioning]
---
```

**Rules for the block**

- `id` never changes once in the registry. Flows reference it.
- **`needs` is not a gate.** Default `blocking: false`. A missing input produces a decision register entry and the work continues on a named assumption. Only argue for `blocking: true` where any assumption would make the output actively misleading, or where the decision is expensive, irreversible and cheap to wait for. A department that stops because another department has not finished is not a department, it is a queue.
- `produces` names artefacts. "Strategy doc" is not an artefact; "the comparison set including doing nothing" is.
- `hands_to.when` is the conditional edge, and it governs ROUTING, not permission to start. Linked, not forced, means the next stage may be skipped or returned to — never that this stage waits indefinitely for a sibling.
- `grading_worker` is an `execution_kind: audit` node. Grading is not a new mechanism; it is the audit node with a three-strike cap that `workflow-runner` already implements.
- Exactly one worker per department should be `tier: premium`. If everything is premium, nothing was prioritised, which is the same failure the department is meant to prevent.

- **A `skills:` entry is an address, and three forms are valid.** Ruled 2026-10-01, after a resolver found that 7 of 14 declared addresses pointed at loose technique files and the catalogue would never see them.
  1. **Package** — `<address>/SKILL.md`. Indexed by the skills catalogue, invocable by name in chat.
  2. **Technique file** — `<address>.md`. A single-file technique. **Not** a catalogue entry and deliberately not one: wrapping a one-file technique in package scaffolding adds ceremony and no capability. The settled rule that technique files are not skills governs what the *register counts*, not what a department may *address*. Those are different questions and conflating them is what produced 7 dead references.
  3. **Leaf name** — resolves where the root is flat rather than nested by domain. Reported as a loose match, never as a correct address, so it is visible as something to tighten.
  Resolution order is the declared home, then the library, then the live global library, then project skills. The declared home wins, so porting a skill shadows its origin and the port is a migration rather than a fork. `bin/resolve-skills.py` is the implementation and exits non-zero on any address that resolves in no root.

- **Take the address from the command that already does the job, never from memory.** `registry.json` said of the CFO *"a /cfo slash command already exists with live Xero behaviour, port it, do not rewrite it"*, and the first draft of `cfo.md` was written without reading it: four invented `finance/*` paths, one of them (`xero-access`) naming a capability that exists only as a reference file inside another skill. `/cfo`'s own routing block already named the correct five. Where a command covers a department's ground, its routing block is the source for `skills:`.

---

## Part B — the lens

Prose. This is what gets injected as the framing `context_ref`. Ten parts, in this order.

**1. Stance.** One paragraph: thinks like X, feels responsible for Y, operates like Z. This is the sentence that makes the role recognisable to someone who has held it.

**2. How this role thinks.** The standing questions it cannot stop asking. Not a checklist to complete once. If the questions are generic enough to fit two departments, they are not the questions.

**3. What it feels responsible for.** The stewardship. The thing it loses sleep over. Include the productive tension of the role, because every senior role has two duties that pull against each other and the tension is the job.

**4. What it owns.** Capability table: capability, what it means in practice, the outcome it produces.

**5. Reading the context through this identity.** The sequencing, and it is fixed:

> **I am this department** → therefore, for **this brand or product**, what matters is X → therefore **this audience or system** is really in state Y → therefore **this task** must do Z.

Never open the context files first and then reach for the lens. The identity decides which parts of those files are load-bearing and which are noise. Reversed, you get a summary of what the files contained, which is what a skills-first system produces every time.

**6. How it is outworked.** The operating model, staged. What the role actually does to convert judgement into a system rather than an artefact.

**7. Operating rhythm.** Daily, weekly, monthly, quarterly, annually. This is what makes a department schedulable on cron rather than only reactive.

**8. The test.** The questions any initiative must answer before this department will pass it. Include at least one that forces a trade-off to be named. An initiative with no trade-off named has not been decided, only added.

**9. Failure modes.** Table: the failure, what it looks like in real output, what prevents it. Write these against the identity, not against the steps.

**10. Handoffs in prose.** What this department needs before it can start, what it hands over, and what it will refuse to proceed without. The declaration block is the machine version; this is the reasoning, so a human reviewing a flow can see why the boundary sits where it does.

---

## What a department is not

- **Not a persona.** "Act as a CMO" produces a voice. A department produces a decision with a named trade-off and a defined artefact.
- **Not a process.** Six numbered STEPs with confirm blocks is a procedure wearing a lens as a label. The old viewports were exactly this and it is why they never changed an output.
- **Not a container for skills.** Skills are pulled through the lens on demand. A department that lists forty skills has no lens.
- **Not equal to every other department in every conversation.** Use the one that matches the stage. Generating a large multi-role response every time is the failure, not the goal.

---

## How this reaches the runner

A flow in `flows/` composes departments and emits a `workflow.json` matching the authoritative contract shape in `hermes-ops/hermes-state/workflows/sow-build.workflow.json`. The mapping is direct:

| Department contract | `workflow.json` |
|---|---|
| `workers[].node` | `nodes[].id` |
| `workers[].execution_kind` | `nodes[].execution_kind` |
| `workers[].tier` | `nodes[].tier` + `tier_policy.per_node_overrides` |
| `workers[].human_gate` / `gate_note` | `nodes[].human_gate` / `gate_note` |
| `needs` + `produces` | `nodes[].context_refs[]` and `nodes[].upstream[]` |
| `hands_to.when` | `edges[].when` |
| Part B, the lens | a `context_ref` injected into the node's `prompt_template` |

Nothing here is a new engine. `workflow-runner` already walks the graph, resolves per-node model and tier, emits `node-v1` at each node completion, passes outputs downstream via `context_refs`, applies three-strike retry on audit nodes, and runs on Hermes cron. This repo supplies the layer that was always missing: who the workers are, and how the work crosses between them.
