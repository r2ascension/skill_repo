---
name: biomamba-bulk-rnaseq-practice
description: "Source-specific Biomamba 转录组实战 overlay for tutorial-style bulk RNA-seq shell and R code. Use only when the user mentions Biomamba, 转录组实战, the provided HTML notes, or asks to reuse that FASTQ download, QC, HISAT2, featureCounts, TPM or FPKM, edgeR or limma, volcano, heatmap, enrichment, or rMATS workflow. For generic bulk RNA-seq prefer existing RNA-seq workflow skills; do not use for scRNA-seq."
---

# Biomamba Bulk RNA-seq Practice

## Scope

Use this skill for bulk RNA-seq hands-on analysis from raw FASTQ to expression matrix, differential expression, visualization, enrichment, and optional alternative splicing.

Do not use this skill for scRNA-seq Seurat workflows or miRNA target database queries.

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
