---
name: bulk-rnaseq-router
description: Focused router for bulk RNA-seq analysis and downstream interpretation workflows. Trigger when the task is bulk RNA-seq preprocessing, DEG analysis, enrichment, visualization, immune infiltration, GEO or TCGA workflows, or expression-matrix interpretation and you want one canonical entrypoint before picking the exact bulk RNA-seq skill.
---

# bulk-rnaseq-router

Use this router when:
- the task is bulk RNA-seq rather than single-cell RNA-seq
- the request mentions DEG, DESeq2-style downstream work, TCGA or GTEx bulk analysis, enrichment, or bulk expression visualization
- you want a stable first pass across the many bulk-rnaseq-* skills

Routing guidance:
- Use bulk-rnaseq-* skills for downstream bulk analysis modules and comparisons.
- Use bio-workflows-rnaseq-to-de when the request is an end-to-end raw-to-DE pipeline.
- Use bio-learning-public-datasets-and-bulk-expression, bio-learning-enrichment-and-pathway-interpretation, or bio-learning-de-wgcna-and-network-analysis when the user wants maintained bulk-expression learning content organized by function rather than direct execution on a dataset.
- Use geoagent-geo-discovery when the first job is GEO cohort discovery, GSE or GSM metadata cleanup, or standardized preprocessing handoff before bulk analysis.
- Use bioagents-agentkit when the user wants literature-grounded interpretation or hypothesis generation around already curated bulk datasets.
- Use genomics-sequencing-router when the main task is file-level read processing rather than bulk expression interpretation.
- Use bio-visualization-router when the chosen bulk workflow is primarily about plotting results.

Examples:
- route a bulk RNA-seq DEG workflow
- which skill covers TCGA or GTEx bulk analysis
- I need the canonical bulk-rnaseq entrypoint