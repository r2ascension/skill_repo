---
name: single-cell-functional-activity
description: "Use when analyzing single-cell functional activity scores such as DoRothEA/VIPER transcription factor activity, PROGENy pathway activity, GSVA/ssGSEA/AUCell/scMetabolism metabolic pathway scores, or summarizing activity matrices by cell type, sample, tissue, or condition."
---

# Single-Cell Functional Activity

## Overview

Use this skill to infer, summarize, validate, and visualize single-cell functional activity matrices from Seurat objects. It covers three common activity engines:

- **DoRothEA + VIPER** for transcription factor activity.
- **PROGENy** for signaling pathway activity.
- **GSVA/ssGSEA/AUCell/scMetabolism** for metabolic or custom pathway activity.

The core abstraction is always:

1. scoring engine produces `activity_matrix` (`feature × cell`),
2. matrix becomes a long table joined with cell metadata,
3. long table is summarized by `celltype`, `sample`, `tissue`, or `condition`,
4. summaries are visualized as heatmaps, dot plots, UMAP overlays, or violin plots.

## When to Use

Use for:

- Inferring TF activity with `dorothea::run_viper()` or `viper`/`decoupleR`.
- Running `progeny()` on single-cell data and plotting pathway activities.
- Scoring custom metabolic pathways with `GSVA::gsva()` / `ssgseaParam()` or `AUCell`.
- Comparing activity scores across cell types, lineages, tissues, conditions, or samples.
- Building reproducible activity score tables for downstream differential analysis.

Do not use as the primary reference for raw scRNA-seq QC, clustering, or cell annotation. Use the dedicated single-cell preprocessing/annotation skills for those steps.

## Required Preflight Checks

Before scoring, confirm:

- Input object is a Seurat object or an expression matrix with cells as columns.
- The requested assay exists and contains normalized data when required.
- Metadata columns such as `celltype`, `sample`, `tissue`, or `condition` exist.
- Gene identifiers match the regulon/pathway database (`SYMBOL` vs `ENSEMBL`).
- Gene-set/regulon overlap is high enough; warn if overlap is below 20%.
- Dense conversion is safe before calling functions that require dense matrices.
- Random seed, package versions, scoring parameters, and gene-set versions are recorded.

## Environment

Core packages:

- `Seurat`, `SeuratObject`, `Matrix`, `data.table`, `dplyr`, `tidyr`, `ggplot2`
- `dorothea`, `viper`, `decoupleR`
- `progeny`
- `GSVA`, `GSEABase`, `AUCell`, optional `scMetabolism`, optional `VISION`
- `pheatmap`, `ComplexHeatmap`, `circlize`, `RColorBrewer`, `viridis`
- `AnnotationDbi`, `org.Hs.eg.db`, `org.Mm.eg.db`, optional `biomaRt`

In the current workstation environment, most core packages are available. Known optional gaps at the time this skill was drafted: `qs2`, `scMetabolism`, and `ReactomePA` may need installation if those routes are used.

## Helper Files

- `R/activity_common.R` — shared preflight, safe assay extraction, matrix reshaping, summaries, and heatmap helper.
- `R/dorothea_viper.R` — DoRothEA/VIPER wrapper and differential TF helper.
- `R/progeny.R` — PROGENy wrapper and extraction helper.
- `R/metabolism.R` — GSVA/ssGSEA/AUCell metabolic scoring skeleton.
- `examples/example_functional_activity.R` — minimal wiring example.

## Workflow: Activity Matrix to Heatmap

1. Extract normalized expression using `safe_get_assay_matrix()`.
2. Run the selected engine:
   - `run_dorothea_viper_activity()`
   - `run_progeny_activity()`
   - `run_metabolism_ssgsea()` or `run_metabolism_aucell()`
3. Convert activity matrix to long format with `activity_matrix_to_long()`.
4. Join metadata and summarize with `summarize_activity_by_group()`.
5. Convert summary to matrix and plot with `plot_activity_heatmap()`.
6. Save raw activity matrix, long table, summary table, plot, and `sessionInfo()`.

## Method Notes

### DoRothEA + VIPER

- Use high-confidence regulons by default (`A`, `B`, `C`).
- For human data use `dorothea_hs`; for mouse data use `dorothea_mm` when available.
- Always report regulon-target overlap with the expression matrix.
- Differential TF activity can use Seurat markers for exploration, but pseudobulk is preferred when biological replicate metadata exists.

### PROGENy

- Use `organism = "Human"` or `"Mouse"` explicitly.
- Default `top = 500`, `perm = 1` is fast and typical for single-cell exploration.
- Run `ScaleData(assay = "progeny")` before row-standardized heatmaps.
- Use `pivot_longer()` / `pivot_wider()` instead of deprecated `gather()` / `spread()`.

### Metabolic Activity

- For custom pathways, require a long table with columns `pathway` and `gene`.
- Filter gene sets by size before scoring; default recommended range is 5–500 genes.
- Avoid dense conversion of large sparse matrices unless memory has been checked.
- For very large datasets, prefer pseudobulk by `celltype × sample` before GSVA/ssGSEA.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Regulon/pathway genes do not match expression row names | Detect gene ID type and report overlap before scoring. |
| Dense conversion of a huge sparse matrix causes OOM | Estimate memory first; filter genes or pseudobulk. |
| `top_n()` used for smallest p-values | Use `slice_min(p_val_adj, n = ...)`. |
| Heatmap colors are not centered at zero | Use symmetric breaks for centered/z-scored matrices. |
| Seurat v5 layers accessed via fragile slots | Prefer `GetAssayData()` and helper wrappers. |
| Activity scores are compared without sample-level replication | Add sample-aware pseudobulk or report exploratory limitation. |

## Minimal Verification

After running any engine, verify:

- `nrow(activity_matrix) > 0` and `ncol(activity_matrix) == ncol(seurat_obj)`.
- No unexpected all-NA feature rows.
- Summary table contains expected `feature × group` combinations.
- Heatmap row/column names match annotation row names.
- `sessionInfo()` and parameter metadata are written to the output directory.
