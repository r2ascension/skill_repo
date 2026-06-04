---
name: biomamba-bulk-rnaseq-practice
description: "Use only when the user mentions Biomamba, 转录组实战, the provided HTML notes, or asks to reproduce that FASTQ download, QC, HISAT2, featureCounts, TPM/FPKM, edgeR/limma, volcano, heatmap, enrichment, or rMATS workflow. For generic bulk RNA-seq prefer existing RNA-seq workflow skills; do not use for scRNA-seq."
---

# Biomamba Bulk RNA-seq Practice

## Scope

Use this skill for bulk RNA-seq hands-on analysis from raw FASTQ to expression matrix, differential expression, visualization, enrichment, and optional alternative splicing.

Do not use this skill for scRNA-seq Seurat workflows or miRNA target database queries.

For generic end-to-end RNA-seq pipelines that are not specifically tied to the Biomamba tutorial wording, prefer `bio-workflows-rnaseq-to-de`.

## Repository Fit

When applying this tutorial inside `/home/h2048`:

- Put reusable shell wrappers under `script/bash` and reusable R analysis code under `script/R`; keep one-off probes in `temp/`.
- Prefer staging bulk inputs under `data/bulk/` or `data/source/`, not ad hoc numbered folders at the repository root.
- Write dated outputs under `data/R/<YYYYMMDD>/...` or `data/py/<YYYYMMDD>/...`, logs under `logs/<YYYYMMDD>/...`, and record substantive runs in `docs/experiments/WORKLOG-YYYYMMDD.md`.

## Workflow

1. Confirm species, reference genome, annotation file, layout, and sample metadata.
2. Download FASTQ files, often with Aspera when links come from public repositories.
3. Run FASTQ QC and trimming or filtering.
4. Align reads with HISAT2 or another splice-aware aligner.
5. Count reads with featureCounts.
6. Build count, TPM, or FPKM matrices.
7. Run differential expression with edgeR, limma-voom, or DESeq2.
8. Draw volcano, heatmap, and enrichment panels.
9. Run alternative splicing with rMATS if the task includes splicing.

## References

Read `references/workflow.md` for commands and analysis patterns.
Read `references/source-map.md` for source routing.
