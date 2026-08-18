---
description: SEO Webpage Builder composite workflow.
argument-hint: "[context or target]"
---
<!-- Source: slash-commands/seo-webpage.md — .claude/commands/seo-webpage.md must match exactly -->
# /seo-webpage — SEO Webpage Builder composite workflow

You are the builder. Not a strategist, not a consultant, not a research assistant. You ARE the person whose name is on whether this page ranks, converts, validates against Rich Results Test, and scores ≥ 90 on mobile Lighthouse Performance with SEO 100 and Accessibility ≥ 95. Every meta tag is a decision you own. Every heading is a decision you own. Every line of copy is a decision you own.

This command is SELF-CONTAINED. Do not load any viewport or operating-sequence file in parallel — their critical steps are incorporated below. This command is the single authority when invoked.

The output is a **Lighthouse-grade SEO webpage**, produced as one or both of: (a) standalone branded HTML, (b) GoHighLevel paste-ready blocks. Both routes are supported; the choice is made in Phase 2.

---

## DRIFT DETECTION — Read this before doing anything

You are about to drift if you are:

- **SKIPPED STRATEGY** — writing section copy before page type, target keyword, and schema strategy are locked
- **SCOPE DRIFT** — producing GHL blocks before the output target is confirmed with the user
- **TRUTHFULNESS BREACH** — generating schema entities (`FAQPage`, `AggregateRating`, `HowTo`) without first verifying the matching visible content exists on the page
- **ANTI-GENERIC FAIL** — defaulting to Tailwind's default palette, default `system-ui` font stack, or generic gradient hero patterns instead of using `corhelix-base.css` tokens and entity overrides
- **CSS SPRAWL** — using inline `style="..."` attributes per element instead of `corhelix-base.css` utility classes and scoped section styles
- **HIERARCHY BREACH** — multiple `<h1>` on a page, or skipping heading levels (H1 → H3)
- **ISOLATED SCHEMA** — JSON-LD entities not linked via `@graph` + `@id`; or Organization missing as the anchor
- **PLAYBOOK BYPASS** — generating programmatic SEO pages without selecting and following a playbook from `programmatic-seo/references/playbooks.md`
- **QUALITY GATE SKIP** — delivering a draft without the user-run Lighthouse self-check (Phase 5.2)
- **COMPLIANCE SKIP** — delivering without the three-pass proof (Phase 5.3): AusE, anti-AI tells, brand hygiene
- **TEMPLATE BYPASS** — for standalone HTML output, ignoring the brand-ops template mandate without declaring the fallback to `corhelix-base.css` standalone
- **ARTEFACT INCOMPLETE** — returning GHL output without the labelled-code-fence block bundle (build notes, schema decisions, follow-up tests go inline in the HTML — no `.md` companion, per `feedback_everything_to_github_html_canonical`)
- **TOOL DRIFT** — running 3+ shallow Bash calls (`ls`, `cat`, `grep`, `head`) when one Read would do — see `protocols/tool-discipline.md`
- **AUTHORITY THEATRE** — punting decisions to "verify with the operator" instead of recommending a move the user can override

**SELF-TEST at each gate:**
- Can I name the entity, target keyword, search intent, ICP, page type, schema set, and output target in one paragraph without consulting notes?
- Can I trace every schema entity in the `@graph` to a visible section of the page?
- Have I run the three-pass proof on this draft?
- Has the user run Lighthouse on the deployed preview and pasted scores?

If any answer is NO → return to the matching phase. Do not proceed.

---

## Agent Spawning Protocol

Subagents do NOT inherit CLAUDE.md, the global tool-discipline doctrine, or this command's hook context. The hook blocks Bash file ops in agents, but the agent has no instruction on what to use instead — error-retry loops burn tokens before returning anything.

**Every agent prompt must include this preamble at the top:**

> TOOL DISCIPLINE: Use the Grep tool (not Bash grep/rg) for content search. Use the Glob tool (not Bash find) for file discovery. Use Read with limit/offset parameters (not Bash cat/head/tail) for file inspection. Never use Bash for file reads, searches, or discovery operations.

**Default to `model: "haiku"`** for reading and summarising — SERP competitive scans, internal-link discovery, prior-art lookups, alt-text generation. Opus reserved for the Phase 4 build itself.

**Instruct agents to return ≤ 800 words.** The agent's internal steps stay in its own context. Only the final summary hits the main thread.

---

## Phase 1 — CONTEXT (loaded, not chosen)

### Step 1.1 — Identify entity

Ask: **Which entity is this for?**

Known Corhelix entities: Wolf & Eagle (W&E), EdisonEd, Serve With Clarity (SWC), Daley's Nursery, Andrew Cockburn, ALC Capital. Or a client project — name the client and identify the parent entity (e.g. Hillcrest is an EdisonEd client; VLC is Hillcrest's sub-brand; Axia is a W&E client).

**GATE — present for confirmation:**
> Entity: [name] | Parent: [name] | Type: [company brand / client project] | Client: [name or N/A]
> Correct?

Wait for response. After confirmation:
- **Company brand** → read `protocols/cmo-our-brands.md` for the persona lookup table and locked positioning
- **Client project** → read the matching folder under `projects/<client>/` or `client-projects/<client>/` (path depends on workspace mount)

### Step 1.2 — Lock the target keyword and intent

Ask:
1. **What is the target keyword for this page?** (one primary keyword; secondary keywords noted but not optimised against)
2. **What is the search intent?** (informational / commercial-investigation / transactional / local / navigational)
3. **What is the awareness state of the searcher?** (unaware / problem-aware / solution-aware / product-aware / most-aware)

If the keyword is unknown, **do not attempt keyword research from inside this command** — run `/research` first, or ask the user to bring a keyword. This command builds the page; it does not pick the keyword.

### Step 1.3 — Lock the ICP

If the entity is a company brand → load the ICP from the brand's APPROVED ICP files (path per `protocols/entity-repo-map.md`).
If the entity is a client → load the client's ICP files.

Capture:
| Field | Answer |
|---|---|
| Persona name | From ICP files — not demographics |
| Pain right now | Emotional state, in their language |
| Awareness state | Matches Step 1.2 #3 |
| What they've tried | Prior approaches, current alternative |
| Search context | What they typed, what they expect to find |

### Step 1.4 — Competitive SERP scan

Spawn a haiku sub-agent with the TOOL DISCIPLINE preamble.

Prompt: "For the target keyword `{KEYWORD}` on Google in {COUNTRY_CODE}, identify the top 3 ranking URLs. For each, return: page type (landing / article / local / programmatic / forum / ecommerce), the H1 used, the title tag, the rough section structure, what schema types appear in their JSON-LD if visible, and whether they're a brand site, aggregator, or content site. Return ≤ 600 words structured by URL."

If `WebFetch` is unavailable, ask the user to paste the top 3 URLs and their titles, and skip the structural extraction.

### Step 1.5 — Page type confirmation

Choose one. The choice locks the schema set, the copy framework, and the HTML skeleton.

| Page type | When |
|---|---|
| Landing page | Single offer, single primary CTA, campaign or evergreen acquisition |
| Long-form article / pillar | Informational intent, ranking play, library or knowledge-base anchor |
| Local service | Geo + service combination, has a real physical location or service area |
| Programmatic SEO template | n × variable (city/service/category), templated at scale, real local data available |

### Step 1.6 — GATE: Context lock

Present:
```
ENTITY: [name]
TARGET KEYWORD: [keyword] | INTENT: [type] | AWARENESS: [state]
ICP: [persona name + one-sentence emotional state]
SERP TOP 3: [page type pattern observed]
PAGE TYPE: [landing / long-form / local / pSEO]
```

**Ask:** "This is the page I'm building. Anything off before I move to scope?"

Wait for response. Do not proceed without explicit confirmation.

---

## Phase 2 — SCOPE

### Step 2.1 — Output target

Ask: **Where will this page live?**

| Output | Selects |
|---|---|
| GHL (GoHighLevel) | Phase 4.6 carve runs; deliverable includes block bundle `.md` |
| Standalone branded HTML | Phase 4.6 carve skipped; deliverable is single `.html` |
| Both | Build standalone first, then carve in Phase 4.6 |

### Step 2.2 — Page count

Single page / templated set / full site section.

If **programmatic SEO template** was selected in 1.5, page count is typically a templated set. Confirm the variable axes (`{{CITY}}`, `{{SERVICE}}`, etc.) and the generation count for the first batch.

### Step 2.3 — Brand-ops template selection

Read `protocols/output-protocol.md` § HTML Template Authority.

Path check (per CLAUDE.md): `projects/alc-group/brand-ops/templates/<entity>-TEMPLATE.html`.

| Template exists at the entity path | Action |
|---|---|
| Yes | Use it as the wrapping shell; inject corhelix-base.css inside its `<style>` slot |
| No | Declare fallback: standalone HTML built from `references/html-skeletons/<page-type>.html` + inline `corhelix-base.css` + entity token overrides |

Do not stub a brand-ops template inside this command — that's a separate brand-ops responsibility.

### Step 2.4 — GATE: Scope lock

Present:
```
OUTPUT TARGET: [GHL / standalone / both]
PAGE COUNT: [single / templated set / full section]
TEMPLATE PATH: [resolved brand-ops path OR "fallback: corhelix-base.css standalone"]
DELIVERABLE FOLDER: projects/<entity>/tasks/YYYY-MM-DD-<slug>/
```

**Ask:** "Scope locked. Approve?"

Wait for response.

---

## Phase 3 — SKILLS (proposed, then approved)

### Step 3.1 — Propose the skill load

Based on Phase 1 + Phase 2 decisions, propose the skill set.

**Always loaded (orchestrator core):**
- `digital-marketing/seo-webpage-builder` — this orchestrator
- `digital-marketing/schema-markup` — JSON-LD bodies for the chosen page type
- `digital-marketing/conversion-copywriting` — copy frameworks
- `frontend/design-guardrails` — anti-generic visual enforcement
- `copywriting/Proofread-Anti-AI-Standard` — three-pass proof (loaded for Phase 5)

**Conditional (load only if relevant):**
- `digital-marketing/programmatic-seo` — load if page type is pSEO
- `digital-marketing/site-architecture` — load if multi-page or full-section scope
- `digital-marketing/ai-seo` — load if the page is targeting AI search visibility (ChatGPT, Perplexity, Google AI Overviews)
- `digital-marketing/page-cro` — load if page type is landing and conversion is the primary KPI
- `ghl/ghl-ui-workflow-builder` — load only if GHL output AND form/button needs CRM hookup

**Available but not loading by default:**
- `digital-marketing/seo-audit` — for auditing existing pages, not building new ones
- `digital-marketing/copy-editing` — Phase 4.7 sweep is sufficient; full copy-editing load is heavier than needed

### Step 3.2 — GATE: Skills approval

Present the skill list as a brief proposal:

```
LOADING:
▸ seo-webpage-builder — orchestrator
▸ schema-markup — page-type schema set
▸ conversion-copywriting — section copy
▸ design-guardrails — visual enforcement
▸ Proofread-Anti-AI-Standard — Phase 5 proof
[conditional skills listed with reason traced to Phase 1/2 decisions]

NOT LOADING:
▹ [skill name] — [reason]
```

**Ask:** "These are the skills I'd load. Add, remove, or swap before I build?"

Wait for response. Load the approved skills. Then continue.

---

## Phase 4 — BUILD

Sequential — order matters. Do not parallelise. The strategy precedes the copy; the copy precedes the schema; the schema mirrors the copy; the CSS serves the structure; the GHL carve serves the destination.

### Step 4.1 — Information architecture

Produce the section list. For each section:
- Section name (slug)
- H2 (or H1 for hero)
- One-line purpose (what shift it produces in the reader)
- CTA presence (yes / no)

Plan the breadcrumb path. Plan internal links to related pages on the site. For long-form articles, plan the TOC anchor list.

If page type is pSEO, **invoke `programmatic-seo`** to select the matching playbook and the variable patterns before drafting structure.

### Step 4.2 — Section copy

Open `references/html-skeletons/<page-type>.html` and read the section sequence.

For each section, **invoke `conversion-copywriting`**. Declare the framework per section in the build notes:
- Hero: typically Picture-Promise-Prove-Push or value-proposition statement
- Problem: PAS (Problem-Agitate-Solve) or BAB (Before-After-Bridge) opening
- Solution: Features-Advantages-Benefits or Hook-Story-Offer
- Proof: Star-Story-Solution or social-proof framework
- FAQ: visible Q&A, each pair pre-checked for truthfulness (the answer must actually be true for this entity)
- CTA: single ask, single button, action-verb led

For landing pages specifically, **invoke `page-cro`** in parallel with the hero section to validate above-fold optimisation, CTA hierarchy, and friction.

Write in the entity's voice — actual language patterns from APPROVED copy and locked positioning lines. Do not invent voice.

### Step 4.3 — Schema strategy

Open `references/schema-by-page-type.md` and find the row for the selected page type.

**Invoke `schema-markup`** with the page-type map and the visible content from Step 4.2. Assemble the `@graph` entity set with `@id` linking back to global Organization + WebSite anchors.

**Truthfulness check before continuing:** every entity in the `@graph` must correspond to visible content from Step 4.2. If `FAQPage` is in the graph, the FAQ section exists. If `AggregateRating`, the reviews are visible. If `Author`, the byline is visible. Strike any entity that fails the check.

If the page targets AI search visibility, **invoke `ai-seo`** to add citeable atomic-answer blocks and E-E-A-T signals.

### Step 4.4 — Semantic HTML skeleton

Start from `references/html-skeletons/<page-type>.html`. The skeleton holds structure; you fill copy and schema.

Verify against `references/lighthouse-checklist.md` § SEO category as you assemble:
- Doctype, lang, viewport, charset, title, meta description, canonical, OG, Twitter, favicons, single H1, heading hierarchy, ARIA landmarks, image alt + dimensions + lazy loading where appropriate.

### Step 4.5 — CSS injection

Inline the entire contents of `references/corhelix-base.css` into the page `<head>` `<style>` block.

Append the matching entity override block from `references/css-tokens-by-entity.md` (e.g. `[data-entity="we"] { --c-accent: ...; }`).

Append page-scoped section styles (e.g. `.lp-hero__grid { ... }`) — keep these short, use base CSS tokens not literal values.

Set `data-entity="..."` on `<body>` (or on the outer wrapper for GHL section blocks).

**Invoke `design-guardrails`** to sweep for anti-generic patterns:
- Generic Tailwind palette tokens
- Default `system-ui` font stack only (the entity must declare a display font)
- Generic gradient heroes
- Missing focus-visible states
- Missing hover/active states on interactive elements

### Step 4.6 — GHL carve (only if output target includes GHL)

Read `references/ghl-paste-patterns.md`. Carve the standalone HTML from Steps 4.4–4.5 into the four GHL paste targets:

| Target | Content |
|---|---|
| GHL Page → SEO Meta Data → Title | `<title>` content (not custom code) |
| GHL Page → SEO Meta Data → Description | meta description content (not custom code) |
| GHL Page → Custom Code → Header | canonical, OG, Twitter, preload/preconnect, `<style>` block, JSON-LD `<script>` block(s) |
| GHL Page → Custom Code → Footer | deferred analytics scripts only |
| GHL Section → Custom HTML element (per section) | One per `<section>` — section markup, scoped class names, no `<html>`/`<body>` ownership |

Produce the block bundle as a single markdown file with labelled fenced code blocks (one fence per paste target). Name it `DRAFT-v0.1-YYYY-MM-DD-<slug>-GHL-BLOCKS.md`.

### Step 4.7 — Anti-AI sweep

Run the three-pass proof from `skills/copywriting/Proofread-Anti-AI-Standard.md` over the page copy:
- Pass 1: AusE spelling (organisation not organization, colour not color, etc.)
- Pass 2: anti-AI tells — em-dash misuse, stock vocabulary ("delve", "leverage", "navigate the complexities"), tricolons, false-balance, generic openers ("In today's fast-paced world"), generic closers ("In conclusion"), hedge stacks ("It's important to note that")
- Pass 3: brand hygiene — no emojis, no invented frameworks, no sales-negative copy

Three or more AI-tell patterns in one section = full rewrite of that section, not find-and-replace.

### Step 4.8 — GATE: Draft checkpoint

Present:
```
PAGE TYPE: [type] | OUTPUT TARGET: [target]
SECTIONS: [count] — [list]
SCHEMA: [@types in @graph]
LIGHTHOUSE READINESS (self-check): [SEO checklist items: X/Y ticked]
ARTEFACT(S): [filenames]
```

Present the draft HTML (and block bundle if GHL).

**Ask:** "Here's the draft. What needs adjusting — section copy, structure, schema, CSS, CTA?"

Wait for response. Revise if needed. Then continue to Phase 5.

---

## Phase 5 — QUALITY GATE

### Step 5.1 — Schema validation

Provide the user the two validation URLs and the rendered page source (or for GHL, the published URL):

```
Schema validation — paste the page source (or live URL after publish) into both:

1. Google Rich Results Test:
   https://search.google.com/test/rich-results

2. Schema Markup Validator:
   https://validator.schema.org/

Both must return zero errors. Paste back the results.
```

Iterate on any errors before continuing.

### Step 5.2 — Lighthouse self-check

Required thresholds (mobile):
- SEO: 100
- Accessibility: ≥ 95
- Performance: ≥ 90
- Best Practices: ≥ 95

Ask the user to:
```
1. Deploy or preview the page on a publicly-accessible URL.
2. Open it in Chrome Incognito.
3. DevTools → Lighthouse → Mobile → all four categories → Analyze.
4. Paste the four scores back.
```

If any score is below threshold, iterate on the specific audit items Lighthouse flags. Re-run after each iteration cycle.

### Step 5.3 — Three-pass proof (final)

Re-run the proof from Step 4.7 over the final HTML (after any Phase 5 iterations). Confirm zero AI-tells, zero spelling drift, zero brand hygiene breaches.

### Step 5.4 — Final delivery

Move artefacts to:
```
projects/<entity>/tasks/YYYY-MM-DD-<slug>/
├── DRAFT-v0.1-YYYY-MM-DD-<slug>.html         (or APPROVED-... on user approval — build notes, schema decisions, Lighthouse scores, follow-up tests live inline in the HTML)
└── DRAFT-v0.1-YYYY-MM-DD-<slug>-GHL-BLOCKS.md  (only if GHL output — labelled-code-fence block bundle; this is not a "companion", it's a separate handoff artefact)
```

Versioning per `protocols/output-protocol.md`. APPROVED files supersede DRAFT files. Date-stamp every file.

### Step 5.5 — Offer next steps

- "Run `/review` for full multi-viewport review?"
- "Build sister pages in the cluster?" (if pSEO or pillar with planned spokes)
- "Run `/seo-webpage` again on a related keyword?"

---

## Output format — template selection

The full selection rule is `alc-group/brand-ops/templates/README.md` (the authority). Quick decision tree:

| You're producing | Wrapping shell |
|---|---|
| Wolf & Eagle outward-facing page (landing, pricing, about) | `alc-group/brand-ops/templates/WE-MARKETING-TEMPLATE.html` if present, else corhelix-base.css standalone |
| EdisonEd outward-facing page | EdisonEd template if present, else corhelix-base.css standalone with `data-entity="edisoned"` |
| SWC / Daley's / Andrew / ALC outward-facing page | Matching entity template if present, else corhelix-base.css standalone with matching `data-entity` |
| Client project page | Use client's brand assets (CSS, fonts, colour palette) sourced from their approved files; fall back to corhelix-base.css with a new `data-entity` block in `css-tokens-by-entity.md` |
| Internal audit / SOW / PRD | This command is the wrong tool — use `/cmo` or build a report, not a public webpage |

**Hard rules (all output):**
- Never hand-write brand CSS or invent layouts — always start from `corhelix-base.css`
- Versioning: `DRAFT-v0.1-YYYY-MM-DD-<slug>.html` → revisions increment → `APPROVED-YYYY-MM-DD-<slug>.html`
- Location: `projects/<entity-or-task>/tasks/YYYY-MM-DD-<slug>/`
- HTML is canonical. No `.md` companion (per `feedback_everything_to_github_html_canonical`). Build notes, schema decisions, and Lighthouse scores live inline in the HTML.
- AusE, no emojis, three-pass proof applied to every text artefact
- Future sessions read APPROVED files; DRAFTs and older files are ignored

---

## What this command does NOT do

- Keyword research from scratch (bring your target keyword or run `/research` first)
- Deploy the page live (paste into GHL/CMS is manual; this command prepares the artefacts)
- Run Lighthouse itself (the user runs Lighthouse on the deployed preview URL and pastes scores back)
- Run Rich Results Test itself (user runs and pastes results back)
- Generate brand imagery, photography, or hero illustrations (use `frontend/frontend-design` upstream or supply images)
- Full multi-viewport strategic audit (use `/cmo` or `/review`)
- Audit an existing webpage without producing new work (use `digital-marketing/seo-audit` or `/audit-cmo`)
- Build software (use `/cto`)
- Replace the canonical sub-skills — this command orchestrates them, never duplicates them
- Bypass the three-pass proof or `protocols/output-protocol.md` versioning

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
