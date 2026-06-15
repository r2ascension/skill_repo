---
name: geoagent-geo-discovery
description: Use when the user mentions JiekaiLab/GEOAgent or needs GEO-first dataset discovery, metadata curation, omics identification, sample pairing, or bioStream-oriented preprocessing orchestration from natural-language queries or GEO accessions.
---

# geoagent-geo-discovery

Use this skill when:
- the user names `GEOAgent`, `JiekaiLab/GEOAgent`, `GSE`, `GSM`, or asks for GEO dataset discovery by natural language
- the task starts from public GEO accession triage rather than from already curated local matrices
- the workflow needs sample metadata tables, omics or platform identification, renaming cleanup, or multi-omics pairing logic
- the user wants a reproducible handoff from GEO screening into `bioStream` or another preprocessing pipeline

Advantage zone:
- best for GEO-centric search and ranking, especially when the user has a disease, tissue, assay, or accession query but not yet a finalized cohort
- strong fit for standardized dataset summaries, sample-level metadata extraction, and assay-type inference before downstream analysis begins
- strong fit for single-cell multi-omics pairing, ChIP-seq Input or IP matching, and other accession-driven curation logic
- good choice when the deliverable is a clean preprocessing launch point, not yet a full literature-plus-hypothesis research narrative

Prefer another skill first when:
- the main job is literature synthesis, cross-paper reasoning, uploaded private document analysis, or hypothesis generation; use `bioagents-agentkit`
- the user has already selected datasets and now needs classical downstream workflows such as bulk DEG, Scanpy, Seurat, or figure generation
- the work is not GEO-first and instead centers on general manuscript, review, or citation production

Examples:
- search GEO for airway epithelial single-cell cohorts and prepare a preprocessing handoff
- inspect GSE metadata, identify assay types, and standardize sample naming
- find paired ChIP-seq Input and IP samples before launching downstream workflows
