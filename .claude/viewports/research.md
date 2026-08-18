# RESEARCH VIEWPORT
# Non-negotiable strategic context layer for all research, intelligence, and analysis tasks.
# This viewport can be combined with CMO and/or PM viewports when the task requires multiple lenses.

---

## WHAT THIS IS

This viewport is the analytical rigour layer that governs HOW you gather, evaluate, and synthesise information.
It does not tell you what steps to follow (that's the identity SOP).
It does not give you domain knowledge (that's the skills).
It tells you WHAT MATTERS — what questions must be answered, what sources are credible, what constitutes evidence vs opinion, and how to verify the research serves the decision it was commissioned for.

Without this viewport loaded, research is a content dump. A competitor analysis without a strategic question is a wiki page. Market research without decision context is trivia. Intelligence without a thesis is noise.

You do not skip steps. You do not reorder steps.
You define the question before gathering data. You evaluate sources before citing them.
You do not produce findings until Steps 1–3 are complete and confirmed.

---

## WHEN THIS VIEWPORT APPLIES

Load this viewport when the task involves ANY of:
- Competitor analysis, market research, or industry landscape mapping
- Business intelligence, trend analysis, or opportunity identification
- Due diligence, feasibility studies, or risk assessment
- Data synthesis from multiple sources into actionable findings
- Strategic research to inform a decision (pricing, positioning, market entry)
- Technology evaluation, vendor comparison, or tool selection

This viewport stacks with CMO (for market-facing research that informs positioning) and PM (for research that informs scoping or feasibility).

---

## STEP 1 — LOAD RESEARCH CONTEXT

Before anything else, understand what this research is FOR:

- **Decision context** — What decision will this research inform? Who is the decision-maker?
- **Prior work** — Check `projects/<name>/` for existing SOWs, LOGs, REPORTs with relevant findings
- **Entity context** — If researching for a client, load from `protocols/entity-repo-map.md` (their market, competitors, positioning)
- **Existing knowledge** — What do we already know? What's confirmed vs assumed?
- **Constraints** — Timeline, depth required, access to sources, confidentiality boundaries
- **Output expectations** — Briefing? Full report? Data table? Decision recommendation?

If the research has no clear decision context, stop and ask: "What decision does this inform?" Research without purpose is browsing.

**Confirm:**
> STEP 1 COMPLETE — Research context loaded:
> - Research for: [entity/project]
> - Decision this informs: [what decision, who decides]
> - Prior findings: [relevant prior work, or "none"]
> - Known context: [what's already established]
> - Constraints: [timeline, depth, access, confidentiality]
> - Expected output: [format and purpose]
> - Files read: [list with paths]
> - Gaps: [what context is missing]

---

## STEP 2 — LOAD ANALYTICAL LENSES

Load and internalise the relevant analytical skill files. These are not research methods — they are evaluation lenses that help you THINK about what you're finding.

Typical analytical lenses for Research viewport:
- `digital-marketing/product-marketing-context` — competitive positioning, market dynamics
- `digital-marketing/marketing-psychology` — buyer behaviour, decision frameworks
- `knowledge-bank/strategy-foundations.md` — competitive strategy, Porter's forces
- `knowledge-bank/strategy-frameworks-library.md` — 139 analytical frameworks (on demand)
- `knowledge-bank/marketing-and-gtm.md` — market analysis, GTM strategy
- `knowledge-bank/corporate-development-and-ma.md` — due diligence, valuation (on demand)
- `knowledge-bank/risk-and-governance.md` — risk assessment frameworks (on demand)

These are not templates. They are lenses.
Framework selection is governed by the research question — not the reverse.
You do not apply SWOT because SWOT exists. You apply SWOT because the decision context requires understanding internal capabilities vs external conditions.

**Confirm:**
> STEP 2 COMPLETE — Analytical lenses loaded: [list files read]

---

## STEP 3 — RESEARCH DESIGN (REQUIRED BEFORE ANY GATHERING)

Complete all six points. Do not abbreviate. Do not skip.
This is the research foundation for the task. It will be written to the SOW before work begins.

### 3.1 — Research Question
One clear question. What must this research answer?
Not "research competitors" — "Which competitors are winning enterprise deals in [segment], and what positioning do they use to displace incumbents?"
The question must be specific enough that you can tell when it's answered.

### 3.2 — Thesis
State your starting hypothesis. What do you expect to find?
This is not bias — it's analytical discipline. A thesis gives you something to test against.
If the findings contradict the thesis — that's a valuable finding. If they confirm it — you need to check whether you only looked for confirming evidence.

### 3.3 — Source Strategy
Where will you look and why?
- **Primary sources**: Direct data (entity repos, client data, product usage, financial records)
- **Secondary sources**: Published data (market reports, competitor websites, industry publications)
- **Tertiary sources**: Synthesised data (analyst opinions, review aggregators, social sentiment)

For each source type: what's available, what's credible, what's the recency requirement?
State what you CANNOT access and what impact that has on findings quality.

### 3.4 — Evidence Standard
What counts as evidence for this research?
- **Confirmed**: Directly verified from a primary source
- **Supported**: Corroborated by 2+ independent secondary sources
- **Indicated**: Suggested by a single credible source (flag as provisional)
- **Assumed**: Not evidenced — stated as an assumption requiring validation

Every claim in the output MUST carry one of these labels. Unlabelled claims are assertions — not research.

### 3.5 — Scope Boundaries
What is IN scope for this research:
- [Area 1] — because [it serves the research question]
- [Area 2] — because [it serves the research question]

What is explicitly OUT of scope:
- [Area A] — because [tangential / insufficient data / deferred]
- [Area B] — because [not relevant to the decision]

Research without boundaries becomes an infinite task. Define the edges.

### 3.6 — Output Specification
What does the final deliverable look like?
- Format: [briefing doc / data table / SWOT matrix / recommendation report / slide deck input]
- Audience: [who reads this — technical team? CMO? external client?]
- Decision it enables: [restate from 3.1 — what can the decision-maker DO with this?]
- Length/depth: [executive summary + detail? comprehensive? single-page brief?]

---

After completing 3.1–3.6, write this analysis into the SOW under "What Good Looks Like."
It must exist before any research gathering begins.

**Confirm:**
> STEP 3 COMPLETE — Research design written to SOW.
> Ready to begin gathering with analytical context active.

---

## STEP 4 — SOURCE GOVERNANCE

Before gathering begins, confirm how each source type is governed:

| Source Type | What it provides on THIS task | Evidence standard it can achieve (from 3.4) | Known limitations |
|---|---|---|---|
| [source] | [what data/insight] | [confirmed/supported/indicated] | [recency, bias, access] |

A source without an evidence standard produces uncalibrated findings — could be fact, could be opinion, no way to tell.
Every source must have a declared evidence ceiling. If it can only achieve "indicated" — that's fine, but it must be stated.

**Confirm:**
> STEP 4 COMPLETE — Sources governed: [list]
> Proceeding to gather with evidence standards active.

---

## STEP 5 — OUTPUT CHECKS (DURING AND AFTER GATHERING)

As the identity SOP executes the research, run these checks continuously.

### 5.1 — Question Alignment
Does every finding serve the research question defined in 3.1?
Is any gathering happening that doesn't map to the question? That's scope creep — note it as a future research item, don't pursue it now.

### 5.2 — Thesis Testing
Are you testing the thesis (3.2) or confirming it?
Have you actively looked for disconfirming evidence?
If all findings support the thesis — have you checked for confirmation bias?

### 5.3 — Evidence Labelling
Is every claim labelled with its evidence standard (3.4)?
Are "indicated" findings clearly distinguished from "confirmed" findings?
Are assumptions stated as assumptions — not disguised as findings?

### 5.4 — Source Triangulation
Are findings from a single source cross-referenced where possible?
Where triangulation isn't possible — is that stated?
Are source limitations (from Step 4) reflected in the confidence level of findings?

### 5.5 — Scope Integrity
Has the research stayed within the boundaries defined in 3.5?
Did you go down a rabbit hole that doesn't serve the research question?
If scope expanded — was the SOW updated and re-approved?

### 5.6 — Decision Utility
Can the decision-maker actually USE these findings (per 3.6)?
Are recommendations actionable — not just "consider X" but "do X because Y"?
Is the output structured for the stated audience — not for a general reader?

---

## STEP 6 — RESEARCH AUDIT (BEFORE DELIVERY)

After output is complete, run the Research audit before delivering.

Ask: *If an analyst reviewed this cold — with no context about the process, just the findings — would they trust these conclusions?*

| Check | Pass condition |
|---|---|
| **Premature conclusions** | No conclusions were drawn before evidence was gathered. No recommendations before 3.1–3.6. |
| **Evidence integrity** | Every claim carries an evidence label (confirmed/supported/indicated/assumed). No unlabelled assertions. |
| **Confirmation bias** | Disconfirming evidence was actively sought. Thesis was tested, not just confirmed. |
| **Source transparency** | Source limitations are stated. What could NOT be verified is as clear as what was verified. |
| **Scope discipline** | Research stayed within boundaries. Tangential findings are logged as future items, not included as padding. |
| **Decision utility** | Output enables the stated decision. Recommendations are specific and actionable, not generic "consider" statements. |

If any check fails: return to the relevant step, resolve, and re-audit.
Do not deliver research that fails audit. Fix it first.

**Confirm:**
> RESEARCH AUDIT: [PASS / FAIL — with notes on any adjustments]

---

## FAILURE MODES

| Failure mode | What it looks like | Which step prevents it |
|---|---|---|
| **Questionless research** | "Research the competitors" with no specific question or decision context | Step 3.1 — research question must be specific and decision-linked |
| **Confirmation bias** | Finding only evidence that supports the starting thesis | Step 5.2 — thesis must be tested, not just confirmed |
| **Unlabelled assertions** | "Company X is the market leader" with no source or evidence standard | Step 3.4 + 5.3 — every claim must carry an evidence label |
| **Source laundering** | Citing a secondary source as if it were primary evidence | Step 4 — source governance declares evidence ceiling per source |
| **Infinite scope** | Research that keeps expanding because "this is also relevant" | Step 3.5 — scope boundaries must be explicit |
| **Trivia delivery** | Comprehensive data that doesn't help the decision-maker decide anything | Step 3.6 + 5.6 — output must serve the stated decision |
| **Decoration** | "The Research lens says check sources" then citing the first Google result | Step 5 checks must be RUN. Step 6 audit must PASS. |

---

## COMBINING WITH OTHER VIEWPORTS

When Research viewport stacks with CMO or PM:

- **Research + CMO** (e.g., competitive intelligence for positioning): Research governs evidence quality, source credibility, and analytical rigour. CMO governs what the findings mean strategically — how they inform ICP messaging, positioning, and competitive differentiation. Research audit checks evidence integrity. CMO audit checks strategic utility.

- **Research + PM** (e.g., feasibility research for scoping): Research governs data quality and source credibility. PM governs how findings translate into scope decisions, constraints, and milestone planning. Research audit checks evidence integrity. PM audit checks whether findings enable scoping.

- **Research + CMO + PM** (e.g., market entry research): All three. Research owns evidence quality. CMO owns strategic interpretation (positioning, ICP fit). PM owns scoping implications (what's feasible, what's not, what milestones follow). Each viewport's analysis, checks, and audit run independently. All must pass.

Viewports do not conflict. They see the same work through different lenses. If a viewport check fails, the work has a problem — not the viewport.
