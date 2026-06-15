---
name: bio-workflows-router
description: Second-level router for end-to-end bioinformatics pipelines and workflow orchestration. Trigger when the task is a full omics pipeline, not a single analysis primitive, and you need to choose among the many bio-workflows and workflow-management skills.
---

# bio-workflows-router

Use this router when:
- the user wants an end-to-end pipeline from raw data to outputs
- the request mentions workflow management, Nextflow, Snakemake, WDL, CWL, or a named omics pipeline

Routing guidance:
- Use bio-workflows-* skills for modality-specific end-to-end pipelines such as rnaseq-to-de, scrnaseq-pipeline, spatial-pipeline, or proteomics-pipeline.
- Use bio-workflow-management-* skills for Nextflow, Snakemake, CWL, or WDL orchestration concerns.
- Use biomaster-workflows when the user wants a broader workflow backbone rather than a modality-specific pipeline.
- Use geoagent-geo-discovery when the workflow begins with public GEO discovery and needs metadata curation plus bioStream-style preprocessing launch commands before the main pipeline starts.
- Use bioagents-agentkit only when the workflow is research-assistant style exploration rather than deterministic pipeline orchestration.

Examples:
- which skill covers an end-to-end RNA-seq pipeline
- route this Nextflow or Snakemake task
- I need a spatial or single-cell full pipeline