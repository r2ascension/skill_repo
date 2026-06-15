---
name: bioagents-agentkit
description: Use when the user mentions bio-xyz/BioAgents, AgentKit, BioAgents Literature API, or BioAgents Data Analysis, or wants an open-ended biology research agent that combines literature synthesis, uploaded dataset analysis, planning, reflection, and hypothesis generation with citations.
---

# bioagents-agentkit

Use this skill when:
- the user names `BioAgents`, `AgentKit`, `BioAgents Literature API`, `BioAgents Data Analysis`, or `deep research`
- the task is an open-ended biology or life-science research conversation rather than a narrow database lookup
- the workflow needs literature search plus uploaded file analysis plus hypothesis generation in one loop
- the user wants a private or custom knowledge base layered into the research assistant

Advantage zone:
- best for literature-plus-analysis workflows where questions evolve across multiple turns
- strong fit for uploaded PDF, CSV, Excel, Markdown, JSON, or TXT datasets that need agent-style interpretation
- strong fit for research planning, iterative investigation, and cited synthesis instead of one-shot data retrieval
- good choice when the user wants one framework that can swap literature and analysis backends while preserving a shared conversation state

Prefer another skill first when:
- the real bottleneck is GEO dataset discovery, GSM metadata normalization, or accession-level sample pairing; use `geoagent-geo-discovery`
- the user already knows the downstream analysis stack and mainly needs DESeq2, Scanpy, Seurat, Nextflow, or plotting help; use the narrower domain skill directly
- the task is now manuscript drafting, review writing, or citation formatting rather than agentic research execution

Examples:
- use BioAgents-style deep research on these uploaded assay tables
- plan an investigation, search the literature, and generate hypotheses about this pathway
- compare several candidate mechanisms with cited evidence and dataset-aware analysis
