---
name: single-cell-deg-visualization
description: "Use when comparing groups within annotated single-cell clusters or cell types, running Seurat FindMarkers by cell type, detecting pseudoreplication risks, exporting merged DEG tables, selecting top marker labels, or creating multi-cluster volcano plots such as jjVolcano figures."
---

# Single-Cell DEG Visualization

## Overview

Use this skill to compare biological groups within annotated single-cell populations and visualize the results. It focuses on robust `FindMarkers` wrappers, pseudobulk-aware design checks, standardized DEG tables, top gene labels, and publication-style multi-cluster volcano plots.

This skill assumes the object has already been QC-filtered, integrated or normalized as appropriate, clustered, and annotated.

## When to Use

Use for:

- Comparing `group1` vs `group2` inside each `celltype`.
- Looping over annotated clusters and collecting DEG results.
- Creating `scRNAtoolVis::jjVolcano` plots with top genes labelled.
- Exporting per-celltype DEG tables and summary Excel workbooks.
- Detecting whether a sample-aware pseudobulk approach is more appropriate.

Do not use this as a substitute for experimental design. If biological replicates exist, evaluate pseudobulk before interpreting cell-level Wilcoxon tests.

## Required Preflight Checks

Before differential analysis, check:

- Input is a Seurat object.
- `celltype_col` and `group_col` exist in metadata.
- `ident.1` and `ident.2` exist in `group_col`.
- Every analyzed cell type has enough cells in both groups.
- If `sample_col` exists, each group has enough biological samples for pseudobulk.
- The requested assay and slot/layer are available.
- Seurat output has a recognizable log fold-change column.

## Environment

Core packages:

- `Seurat`, `SeuratObject`, `Matrix`, `dplyr`, `tidyr`, `tibble`, `data.table`
- `ggplot2`, `ggrepel`, `scRNAtoolVis`, `RColorBrewer`, `viridis`, `patchwork`
- `openxlsx` or `writexl`
- Optional pseudobulk: `edgeR`, `limma`, `DESeq2`, `SingleCellExperiment`, `glmGamPoi`, `MAST`

`scRNAtoolVis` is optional. If unavailable, fall back to the ggplot2 volcano helper in `R/celltype_deg_volcano.R`.

## Helper Files

- `R/celltype_deg_volcano.R` — preflight, per-celltype DEG wrapper, table normalization, top labels, and volcano helpers.
- `examples/example_celltype_deg.R` — minimal celltype-wise group comparison workflow.

## Core Workflow

1. Run `preflight_celltype_deg()`.
2. Loop through cell types using `run_celltype_findmarkers()`.
3. Normalize result columns with `standardize_deg_table()`.
4. Add significance labels with `label_deg_thresholds()`.
5. Select top genes using `select_top_deg_labels()`.
6. Save raw, filtered, and summary DEG tables.
7. Draw `plot_multicluster_volcano()`.
8. Save `sessionInfo()` and parameter metadata.

## DEG Table Schema

Standardized DEG output should include:

- `gene`
- `celltype`
- `group_1`
- `group_2`
- `log2FC`
- `p_val`
- `p_val_adj`
- `pct.1`
- `pct.2`
- `direction`
- `significance`
- `method`
- `n_cells_group_1`
- `n_cells_group_2`

## Statistical Guidance

Cell-level Wilcoxon tests are useful for exploration, but can inflate significance when cells from the same patient/sample are treated as independent. If `sample_col` exists and each group has biological replicates, prefer pseudobulk or at least report the limitation.

Recommended behavior:

- No sample column: run cell-level DEG and label exploratory.
- Sample column with >=3 samples per group: recommend pseudobulk.
- Small groups: skip celltype or warn loudly.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Missing or mismatched group labels | Validate `group_col`, `ident.1`, and `ident.2` before looping. |
| Cell type has too few cells in one group | Skip and record in summary table. |
| Using deprecated `top_n()` | Use `slice_max()` / `slice_min()`. |
| Seurat logFC column name changes | Detect `avg_log2FC`, `avg_logFC`, or `log2FC` and standardize to `log2FC`. |
| Hard-coded color vector too short | Generate colors dynamically based on number of cell types. |
| Interpreting cell-level p-values as replicate-level evidence | Add pseudobulk check and warning. |

## Minimal Verification

After running, verify:

- Every requested cell type appears in either DEG output or skipped summary.
- `log2FC`, `p_val_adj`, and `gene` are present.
- No infinite `-log10(p_val_adj)` values remain unhandled in plots.
- Volcano labels are selected from significant genes only unless explicitly requested.
- Excel/CSV/PDF files are written and non-empty.

## Related Skills

- **bio-differential-expression-de-visualization** - The general (non-bio-single-cell-specific) equivalent covering bulk DE visualization with DESeq2/edgeR built-in plots.
