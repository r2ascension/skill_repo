---
name: biomamba-scrna-figure1-plots
description: "Source-specific Biomamba 单细胞Figure1的常见图表 overlay for tutorial-derived scRNA manuscript panels. Use only when the user mentions Biomamba, 单细胞Figure1, the provided HTML notes, or asks to reuse those UMAP, QC, marker, cell proportion, enrichment, or patchwork recipes. For generic publication layout prefer multipanel figure skills; do not use for preprocessing or doublet calling."
---

# Biomamba scRNA Figure 1 Plots

## Scope

Use this skill when the data object already exists and the task is to make first-figure style panels for a single-cell paper.

Keep data processing elsewhere:

- Seurat preprocessing: `$biomamba-scrna-seurat-v5`
- Doublet filtering: `$biomamba-scrna-doublet-filtering`
- Paper-specific case reproduction: `$biomamba-scrna-case-reproduction`

## Workflow

1. Confirm the object contains cell type, group, sample, and QC metadata.
2. Decide the panel set: embedding overview, QC, marker expression, cell proportion, enrichment, and layout.
3. Use consistent colors for cell types and groups across panels.
4. Save individual panels as vector or high-resolution raster files.
5. Compose multipanel figures with `patchwork`; leave manual finishing to Illustrator only for final layout polish.

## References

Read `references/workflow.md` for panel recipes.
Read `references/source-map.md` for provenance and boundaries.
