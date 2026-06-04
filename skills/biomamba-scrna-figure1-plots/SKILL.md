---
name: biomamba-scrna-figure1-plots
description: "Use only when the user mentions Biomamba, 单细胞Figure1, the provided HTML notes, or asks to reproduce those UMAP, QC, marker, cell proportion, enrichment, or patchwork recipes. For generic publication layout prefer multipanel figure skills; do not use for preprocessing or doublet calling."
---

# Biomamba scRNA Figure 1 Plots

## Scope

Use this skill when the data object already exists and the task is to make first-figure style panels for a single-cell paper.

Keep data processing elsewhere:

- Seurat preprocessing: `biomamba-scrna-seurat-v5`
- Doublet filtering: `biomamba-scrna-doublet-filtering`
- Paper-specific case reproduction: `biomamba-scrna-case-reproduction`

## Repository Fit

When building Figure 1 style panels inside `/home/h2048`:

- Save panels into the corresponding dated result folder's `figures/` subdirectory rather than a new top-level figure tree.
- Keep cell-type and group colors consistent with the surrounding report or lineage output.
- Use `bizard` or `scientific-figure-decision` for generic visualization choice / design trade-offs, and use this skill only when the target is specifically a Biomamba-style first-figure panel set.

## Workflow

1. Confirm the object contains cell type, group, sample, and QC metadata.
2. Decide the panel set: embedding overview, QC, marker expression, cell proportion, enrichment, and layout.
3. Use consistent colors for cell types and groups across panels.
4. Save individual panels as vector or high-resolution raster files.
5. Compose multipanel figures with `patchwork`; leave manual finishing to Illustrator only for final layout polish.

## References

Read `references/workflow.md` for panel recipes.
Read `references/source-map.md` for provenance and boundaries.
