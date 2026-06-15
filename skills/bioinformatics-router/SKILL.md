---
name: bioinformatics-router
description: Top-level router for bioinformatics, omics, sequencing, single-cell, spatial, proteomics, and computational biology workflows. Trigger when the task is biological data analysis or domain-specific research code and the exact omics subdomain or pipeline skill is not yet clear.
---

# bioinformatics-router

Use this router when:
- the task is sequencing, single-cell, bulk RNA-seq, spatial omics, genomics, proteomics, metabolomics, or pathway analysis
- the user wants computational biology help and there are many plausible subdomain skills
- the task is computational but the bio domain assumptions and assay-specific choices matter

Routing guidance:
- Use the bio-* family for precise omics operations, file handling, QC, and domain pipelines.
- Use scrna-*, bulk-*, scanpy, spatial-*, or biomamba-* skills when the analysis family is already obvious.
- Use bio-learning-r-linux-and-environment-foundations, bio-learning-public-datasets-and-bulk-expression, bio-learning-enrichment-and-pathway-interpretation, bio-learning-spatial-and-multiomics, bio-learning-bioinformatics-software-and-tooling, bio-learning-network-pharmacology-target-databases, bio-learning-ppi-cytoscape-network-analysis, bio-learning-molecular-docking-and-structure-visualization, bio-learning-causal-inference-and-mendelian-randomization, bio-learning-de-wgcna-and-network-analysis, bio-learning-tumor-immunology-literature, or bio-learning-research-case-reproduction when the user wants maintained learning content organized by concrete function rather than by creator or album source.
- Use geoagent-geo-discovery when the job starts with GEO search, GSE or GSM curation, assay identification, or preprocessing handoff rather than downstream analysis.
- Use bioagents-agentkit when the job is a broader biology research loop spanning literature synthesis, uploaded datasets, analysis planning, and hypothesis generation.
- Use literature and manuscript routers only after the biological analysis workflow is complete or when the request shifts to writing.
- Use software-engineering-router when the main problem is pipeline code quality, environment repair, framework integration, or implementation debugging rather than biological workflow choice.
- Use scientific-computing-router when the work is more generic numerical or plotting logic than assay-specific analysis.

Examples:
- which skill should handle this scRNA-seq task
- route a bulk RNA-seq differential expression workflow
- I need the right bioinformatics pipeline skill