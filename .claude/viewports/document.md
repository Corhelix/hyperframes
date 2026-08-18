# DOCUMENT VIEWPORT
# Non-negotiable strategic context layer for all document production, proposals, and formatted business output.
# This viewport can be combined with CMO and/or PM viewports when the task requires multiple lenses.

---

## WHAT THIS IS

This viewport is the document quality layer that governs HOW you produce structured business documents.
It does not tell you what steps to follow (that's the identity SOP).
It does not give you domain knowledge (that's the skills).
It tells you WHAT MATTERS — who the reader is, what the document must achieve, what format and standard it must meet, and how to verify the output is fit for its purpose.

Without this viewport loaded, documents are content without craft. A proposal without reader journey is a feature list. A report without executive framing is a data dump. A branded document without format governance is a Google Doc with a logo.

You do not skip steps. You do not reorder steps.
You define the reader and purpose before writing. You define the structure before filling it.
You do not produce document content until Steps 1–3 are complete and confirmed.

---

## WHEN THIS VIEWPORT APPLIES

Load this viewport when the task involves ANY of:
- Proposals, pitch decks, or client-facing business documents
- Research reports, briefing documents, or executive summaries
- SOWs, project plans, or scope documents (beyond internal templates)
- Branded documents requiring visual/format standards (DOCX, PDF, PPTX)
- Board papers, investor updates, or governance documents
- Any document that leaves the internal team — a document someone else reads

This viewport stacks with CMO (for brand-governed, ICP-targeted documents), PM (for scope-governed deliverables), and Research (for evidence-based reports).

---

## STEP 1 — LOAD DOCUMENT CONTEXT

Before anything else, understand the document's purpose and environment:

- **Reader** — Who reads this? What's their role, context, and attention budget?
- **Purpose** — What must this document DO? (Persuade, inform, govern, record, propose)
- **Prior work** — Check `projects/<name>/` for existing documents, SOWs, templates
- **Entity context** — If producing for a client, load from `protocols/entity-repo-map.md` (brand, tone, visual identity)
- **Format requirements** — DOCX, PDF, PPTX, Markdown? Template exists? Brand guidelines?
- **Constraints** — Page limits, approval process, compliance requirements, delivery deadline
- **Lifecycle** — Is this a one-time document or a living document that gets updated?

If the reader is undefined, stop and ask: "Who reads this and what do they do with it?" A document without a reader is a file.

**Confirm:**
> STEP 1 COMPLETE — Document context loaded:
> - Document for: [entity/project]
> - Reader: [who, role, context]
> - Purpose: [persuade / inform / govern / record / propose]
> - Format: [DOCX / PDF / PPTX / Markdown / other]
> - Brand requirements: [template, voice, visual identity, or "none"]
> - Constraints: [pages, timeline, approval, compliance]
> - Files read: [list with paths]
> - Gaps: [what context is missing — no brand guide? no template?]

---

## STEP 2 — LOAD PRODUCTION LENSES

Load and internalise the relevant document production skill files. These help you THINK about document structure and quality — not just write content.

Typical production lenses for Document viewport:
- `document-publishing/docx-proposal` — DOCX proposal structure and formatting
- `document-publishing/pdf-report` — **default deliverable lens** — 1920×1080 landscape modules + native Print → Save as PDF (Landscape Module Doctrine)
- `document-publishing/pptx-deck` — **deprecated for default use** — only when an editable native PowerPoint is a genuine requirement
- `document-publishing/xlsx-data` — Data document structure

> **Landscape Module Doctrine (AUTHORITY 2026-06-10)** governs deliverable format.
> Reports, decks, audits, and strategy docs compose from fixed 1920×1080 landscape
> modules (template: `protocols/templates/LANDSCAPE-MODULE-TEMPLATE.html`) and render
> via the user's native Print → Save as PDF — not A4-portrait HTML and not a separate
> 16:9 deck. See `CLAUDE.md` § Architectural Locks. Text-dense exceptions (long
> contract, dense PRD) may stay portrait, but must be declared as named exceptions in 3.5.
- `digital-marketing/conversion-copywriting` — persuasive writing (if the document must persuade)
- `knowledge-bank/marketing-and-gtm.md` — GTM framing (on demand, for proposals)
- `knowledge-bank/strategy-foundations.md` — strategic framing (on demand, for board/exec docs)

These are not templates. They are lenses.
Document structure is governed by reader need — not by format convention.
You do not use a 10-slide deck template because decks have 10 slides. You use whatever structure serves the reader's decision-making process.

**Confirm:**
> STEP 2 COMPLETE — Production lenses loaded: [list files read]

---

## STEP 3 — DOCUMENT DESIGN (REQUIRED BEFORE ANY WRITING)

Complete all six points. Do not abbreviate. Do not skip.
This is the document design. It will be written to the SOW before content production begins.

### 3.1 — Reader State
Who is this reader right now? What context do they arrive with?
- What do they already know about this topic?
- What are they expecting from this document? (Brief? Comprehensive? Persuasive?)
- How much time will they give it? (30 seconds? 5 minutes? Deep read?)
- What's their emotional state? (Curious? Sceptical? Overwhelmed? Under pressure?)
Use the specific reader context — not a generic "business decision-maker."

### 3.2 — Document Intent
One sentence. What must this document DO to the reader?
Not what it contains — what shift it must produce.
Not "present our capabilities" — "give the reader enough confidence in our approach to approve a $15K engagement."

### 3.3 — Reader Journey
Map the reading path:
- **Entry**: What does the reader see first? What keeps them reading?
- **Middle**: What evidence, logic, or narrative builds the case?
- **Exit**: What does the reader do when they finish? (Approve, decide, share, act)

Each section of the document must serve one stage of this journey. If a section doesn't serve the journey — it's filler.

### 3.4 — Structure
Define the document architecture before writing content:

| Section | Purpose | Reader state at entry | Reader state at exit |
|---|---|---|---|
| [section name] | [what it does] | [what they think/feel arriving] | [what they think/feel leaving] |

The structure is the skeleton. Content fills it. If the skeleton is wrong, no amount of good writing fixes it.

### 3.5 — Format & Brand Governance
What format rules apply?
- **Template**: [existing template to use, or "create from brand guidelines"]
- **Brand voice**: [from entity context — formal/conversational/technical/warm]
- **Visual identity**: [colours, fonts, logo placement, header/footer standards]
- **Locked lines**: [approved copy that must appear verbatim]
- **Banned patterns**: [language, framing, or approaches to avoid]
- **Page/slide limits**: [if applicable]

If no brand governance exists — state that explicitly. The document will default to professional-neutral.

### 3.6 — Success Criteria
How do we know this document is DONE and GOOD?
- [Criterion 1] — how to verify (e.g., "reader can identify our approach in 30 seconds")
- [Criterion 2] — how to verify (e.g., "all pricing is sourced from approved rate card")
- [Criterion 3] — how to verify (e.g., "passes brand compliance check")

These must be specific and verifiable, not "it looks professional."

---

After completing 3.1–3.6, write this analysis into the SOW under "What Good Looks Like."
It must exist before content production begins.

**Confirm:**
> STEP 3 COMPLETE — Document design written to SOW.
> Ready to begin production with structure and governance active.

---

## STEP 4 — CONTENT GOVERNANCE

Before writing begins, confirm how each section maps to the reader journey:

| Section | Reader journey stage (from 3.3) | Format rule (from 3.5) | Success criterion it serves (from 3.6) |
|---|---|---|---|
| [name] | [entry / middle / exit] | [brand voice, template rule, locked line] | [which criterion] |

A section without a journey purpose is padding.
Every section must trace back to the reader journey. If it can't — cut it.

**Confirm:**
> STEP 4 COMPLETE — Content governed: [list]
> Proceeding to production with document design active.

---

## STEP 5 — OUTPUT CHECKS (DURING AND AFTER PRODUCTION)

As the identity SOP produces the document, run these checks continuously.

### 5.1 — Reader Alignment
Does this speak to the reader defined in 3.1?
Is it calibrated for their knowledge level, attention budget, and emotional state?
Or is it written for the writer's comfort rather than the reader's need?

### 5.2 — Intent Check
Does every section serve the intent defined in 3.2?
If a section exists but doesn't advance the document's purpose — it's filler. Cut it.
Can you draw a straight line from the document to the intended reader action?

### 5.3 — Journey Coherence
Does the document follow the reader journey mapped in 3.3?
Does each section hand off cleanly to the next?
Does the entry hook? Does the middle build? Does the exit compel action?

### 5.4 — Structure Integrity
Does the content match the structure defined in 3.4?
Has any section expanded beyond its purpose?
Has any section been added that wasn't in the design?

### 5.5 — Brand & Format Compliance
Does the document follow the format rules from 3.5?
Are locked lines used verbatim? Are banned patterns absent?
Is the visual identity consistent? Does it match the template?

### 5.6 — Success Criteria
Does the document meet every criterion from 3.6?
Can you demonstrate (not assert) that each criterion is met?
Would the reader have the experience the criteria describe?

### 5.7 — Module & Render Compliance (Landscape Module Doctrine)
For deliverables under the doctrine (reports, decks, audits, strategy docs):
- Is it composed from fixed 1920×1080 landscape modules off the canonical template?
- Does every module carry a stable `id="m-{seq}-{slug}"` plus `data-tag` / `data-log-id`?
- Does each module hold one complete thought without overflowing the frame?
- Does the browser print preview render each module as one clean landscape page (no split, no cut-off)?
- If portrait or flatten-to-image was used, is it declared as a named exception in 3.5?

---

## STEP 6 — DOCUMENT AUDIT (BEFORE DELIVERY)

After the document is complete, run the Document audit before delivering.

Ask: *If the reader opened this cold — with no context about how it was made, just the document in front of them — would it do its job?*

| Check | Pass condition |
|---|---|
| **Content before design** | No content was written before the document structure was defined. No sections created before 3.1–3.6. |
| **Reader misfit** | Document is calibrated for the actual reader (knowledge level, attention, context) — not a generic audience. |
| **Journey failure** | Reader journey is coherent entry → middle → exit. No dead ends. No missing steps. No logical jumps. |
| **Brand drift** | Document is on-brand AND on-purpose. Not just "looks nice" — serves the intent while following brand rules. Locked lines used. Banned patterns absent. |
| **Format compliance** | Template followed. Visual identity consistent. Page/slide limits met. No formatting inconsistencies. Under the Landscape Module Doctrine: built from 1920×1080 modules with valid anchors, prints one clean landscape page per module (Step 5.7). |
| **AI writing patterns** | No puffery, no abstraction, no inflated claims, no "leverage" or "empower." Passes Appendix A sweep if applicable. Real language for real readers. |

If any check fails: return to the relevant step, resolve, and re-audit.
Do not deliver a document that fails audit. Fix it first.

**Confirm:**
> DOCUMENT AUDIT: [PASS / FAIL — with notes on any adjustments]

---

## FAILURE MODES

| Failure mode | What it looks like | Which step prevents it |
|---|---|---|
| **Writing before designing** | Drafting content before the structure, reader, and purpose are defined | Step 3 — must be complete before any content |
| **Reader blindness** | A proposal written for the writer, not the reader. Too detailed for executives. Too high-level for technical buyers. | Step 3.1 — reader state must be specific |
| **Feature dumping** | Document lists features/capabilities instead of building a case for the reader | Step 3.3 — reader journey governs what goes where |
| **Brand cosmetics** | Correct logo and colours but wrong voice, tone, or messaging standards | Step 3.5 — brand governance includes voice, not just visuals |
| **Filler sections** | "About Us" or "Our Approach" sections that don't serve the reader journey | Step 5.2 — every section must serve the intent |
| **Format drift** | Inconsistent headers, broken templates, visual identity violations | Step 5.5 — format compliance is continuous |
| **Decoration** | "The Document lens says design first" then dumping content into a template | Step 3 analysis must be WRITTEN. Step 5 checks must be RUN. Step 6 audit must PASS. |

---

## COMBINING WITH OTHER VIEWPORTS

When Document viewport stacks with other viewports:

- **Document + CMO** (e.g., branded proposal): Document governs structure, reader journey, and format. CMO governs brand voice, ICP alignment, positioning, and strategic messaging. Document audit checks structural quality. CMO audit checks strategic quality.

- **Document + Research** (e.g., research report): Document governs reader experience, structure, and format. Research governs evidence quality, source credibility, and analytical rigour. Document audit checks readability and structure. Research audit checks evidence integrity.

- **Document + PM** (e.g., SOW or project plan as deliverable): Document governs reader experience and format quality. PM governs scope completeness and milestone accuracy. Document audit checks document quality. PM audit checks scope adherence.

- **Document + CMO + Research** (e.g., market intelligence report for a client): All three. Document owns structure and format. CMO owns brand, ICP framing, and strategic interpretation. Research owns evidence quality and source credibility. Each viewport's analysis, checks, and audit run independently. All must pass.

Viewports do not conflict. They see the same work through different lenses. If a viewport check fails, the work has a problem — not the viewport.
