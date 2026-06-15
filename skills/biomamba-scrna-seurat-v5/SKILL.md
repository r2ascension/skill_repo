---
name: biomamba-scrna-seurat-v5
description: "Source-specific Biomamba Seurat V5 single-cell RNA-seq tutorial overlay. Use only when the user explicitly mentions Biomamba, scRNA-Seq学习手册_Seurat_V5版, the provided HTML notes, or asks to reuse that tutorial's R workflow for import, QC, clustering, integration, annotation, differential expression, or enrichment. For general scRNA tasks prefer existing generic single-cell skills; do not use for doublet filtering, Figure 1 plotting, paper-specific cases, SCENIC, or hdWGCNA."
---

# Biomamba scRNA Seurat V5

## Scope

Use this skill for the shared Seurat V5 backbone from the Biomamba scRNA-seq handbook: data reading, object creation, QC, dimensionality reduction, clustering, multi-sample integration, annotation, group differential expression, and enrichment.

Keep this skill as the foundation. Route specialized tasks elsewhere:

- Doublet detection: `$biomamba-scrna-doublet-filtering`
- Publication Figure 1 panels: `$biomamba-scrna-figure1-plots`
- Three paper reproductions: `$biomamba-scrna-case-reproduction`
- SCENIC regulons: `$biomamba-scenic-regulons`
- hdWGCNA modules: `$biomamba-hdwgcna-pipeline`

## Workflow

1. Confirm input type: 10X folder, h5, expression matrix, or saved Seurat object.
2. Build or load a Seurat object and calculate QC metrics such as `nFeature_RNA`, `nCount_RNA`, and `percent.mt`.
3. Filter cells and genes with dataset-specific thresholds; avoid copying PBMC thresholds blindly.
4. Run normalization, variable-feature selection, scaling, PCA, neighbor graph, clustering, and UMAP or t-SNE.
5. For multiple samples, compare simple merge, Seurat anchor or CCA integration, and Harmony. Prefer Harmony when memory and speed matter.
6. Annotate clusters with marker databases, manual marker review, SingleR, custom SingleR references, or Seurat label transfer.
7. Run differential expression at the cluster, cell-type, or group level; then visualize with violin, box, dot, heatmap, and volcano-style plots.
8. Interpret differential genes with GO, KEGG, GSEA, or GSVA.

## References

Read `references/workflow.md` for the detailed routed workflow and code patterns.
Read `references/source-map.md` when exact provenance or conflict boundaries matter.
