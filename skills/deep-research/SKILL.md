---
name: deep-research
description: "Use when conducting comprehensive or multi-step research on any topic, including literature reviews, competitive analysis, investigative deep dives, evidence synthesis, recent-source searches, or broad question answering from multiple angles."
---

# Deep Research

Autonomous multi-step research that searches multiple sources, reads full content, synthesizes findings, and produces a structured report.

## When to Use

- User wants a thorough understanding of a topic (medical condition, drug, treatment, technology)
- User asks for a literature review or evidence summary
- User wants competitive or landscape analysis
- User wants to investigate an open question with multiple angles
- User asks "what does the research say about X"

## Research Strategy

### Step 1: Query Decomposition
Break the research question into 3–5 sub-questions covering:
- Core definition / mechanism
- Current evidence / state of the art
- Debates, limitations, or contradictions
- Clinical / practical implications (if medical)
- Recent developments (last 1–2 years)

### Step 2: Multi-Source Search
Run searches across complementary sources using the available search tools:

```python
# Use multi-search-engine for broad web coverage
# Use pubmed-search for peer-reviewed medical literature
# Use agent-browser to read full-text articles and retrieve content blocked by snippets
```

**Search order:**
1. PubMed (if medical/biomedical topic) — for peer-reviewed evidence
2. Multi-search-engine (Bing, Google, DuckDuckGo) — for guidelines, reviews, news
3. Wikipedia — for background and structured overviews
4. agent-browser — for reading full articles, PDFs, clinical guidelines

### Step 3: Source Evaluation
For each source note:
- Publication type (RCT, meta-analysis, guideline, review, news)
- Date (prefer sources within 5 years for medical topics)
- Authority (journal impact, organization credibility)
- Relevance to the specific sub-question

### Step 4: Synthesis
Synthesize across sources into a coherent narrative. Do NOT just concatenate summaries — identify:
- Points of consensus
- Contradictions or conflicting evidence
- Knowledge gaps
- Strongest evidence vs. weak/preliminary evidence

### Step 5: Structured Report
Produce a well-formatted Markdown report with:

```markdown
# [Topic] — Deep Research Report

## Summary
2–3 sentence executive summary of the key finding.

## Background
What is this? Core definitions, mechanisms, or context.

## Current Evidence
What does the research show? Organized by sub-question or theme.

## Key Debates / Open Questions
Where do experts disagree? What is still unknown?

## Clinical / Practical Implications
(For medical topics) What should clinicians or patients know?

## Recent Developments
Anything notable from the past 12–24 months.

## Sources
Numbered list of all sources with titles, URLs/DOIs, and dates.
```

## Medical Research Guidelines

When researching medical topics:
- **Prioritize evidence hierarchy**: Systematic reviews > RCTs > Cohort studies > Case reports > Expert opinion
- **Include safety information**: Drug interactions, contraindications, adverse effects
- **Note population specifics**: Pediatric vs. adult, special populations, comorbidities
- **Flag regulatory status**: FDA/EMA approval status, off-label use
- **Cite clinical guidelines**: NICE, AHA, ACC, IDSA, WHO guidelines where relevant
- **Distinguish mechanistic from clinical evidence**: Lab/animal data ≠ human evidence

## Depth Levels

Adapt depth to user request:
- **Quick overview** (user asks briefly): 3–5 sources, 1-page summary
- **Standard research** (default): 8–15 sources, full structured report
- **Comprehensive review** (user asks explicitly): 20+ sources, deep synthesis with evidence grading

## Swarm / Parallel Execution Mode

For exhaustive topics requiring broad coverage, use a parallel agent swarm approach to research multiple sub-questions simultaneously.

### When to Use Swarm Mode
- Topic spans multiple distinct sub-disciplines
- User explicitly requests comprehensive/exhaustive review
- Topic benefits from searching 5+ databases in parallel
- Need to verify findings by cross-referencing independent sources

### Swarm Workflow

1. **Decompose into Parallel Tasks** (3-5 agents):
   - Agent 1: PubMed / biomedical literature
   - Agent 2: Web search (guidelines, news, regulatory)
   - Agent 3: Preprint servers (bioRxiv, medRxiv, arXiv)
   - Agent 4: Specialized databases (ClinicalTrials.gov, FDA)
   
2. **Coordinate Execution**: Launch agents in parallel, each searching their designated sources with the same core research question.

3. **Aggregate Findings**: Collect all results into a unified evidence table.

4. **Cross-Validate**: Compare findings across agents to identify:
   - Points of consensus (strong evidence)
   - Contradictions (needs deeper investigation)
   - Unique findings from specific sources

5. **Synthesize Report**: Compose final report with all findings, noting where evidence originated.

### Architecture
```python
# Conceptual parallel search coordinator
agents = [
    {"name": "pubmed_agent", "source": "pubmed-search"},
    {"name": "web_agent", "source": "multi-search-engine"},
    {"name": "preprint_agent", "source": "biorxiv-search"},
    {"name": "trial_agent", "source": "clinicaltrials-search"}
]

# Launch all in parallel, collect results
results = parallel_execute(agents, query=topic)
report = synthesize(collect(results))
```

### Performance Target
Generate comprehensive literature review with >50 verified citations in <5 minutes using parallel execution.

## Example Execution

**User:** "Research the evidence for metformin use in longevity/anti-aging"

1. Decompose: mechanism of action → RCT evidence → observational data → safety profile → current trials
2. Search PubMed for "metformin longevity aging", "TAME trial metformin"
3. Search web for "metformin anti-aging clinical trials 2024"
4. Read key papers with agent-browser
5. Synthesize: strong mechanistic evidence, TAME trial ongoing, limited long-term human RCT data
6. Produce structured report with citations
