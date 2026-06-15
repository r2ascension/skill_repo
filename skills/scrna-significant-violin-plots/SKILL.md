---
name: scrna-significant-violin-plots
description: Seurat and ggplot2 violin-plot significance annotation for single-cell expression comparisons. Use when adding per-cell-type group comparisons to VlnPlot or geom_violin outputs, extracting gene expression from Seurat objects, running Wilcoxon tests with BH correction, placing significance stars above violins, exporting per-gene PDF or CSV outputs, or adapting classroom or pasted scRNA visualization snippets into reusable code.
---

# scRNA Significant Violin Plots

## Overview

Use this skill to turn a Seurat expression view into a grouped violin plot with statistical annotation. It is optimized for the common pattern in which each `celltype` compares two biological groups, writes a Wilcoxon summary table, and saves a violin PDF with stars above each cell type.

## Quick Start

- Read [references/source-map.md](references/source-map.md) when the request is clearly adapting the pasted tutorial-style example.
- Source [scripts/significant_violin_plots.R](scripts/significant_violin_plots.R) when you want reusable helpers instead of rewriting the plotting code inline.
- Prefer the ggplot path for significance annotation. Plain `Seurat::VlnPlot()` is fine for quick inspection, but it is awkward once stars, per-cell-type tests, or exported stats tables are required.

## Workflow

1. Normalize the plotting intent before coding.
   Confirm the gene list, the comparison groups, the cell-type column, and whether the stars should reflect raw `p_value` or adjusted `p_adj`.
2. Build a tidy per-cell data frame.
   For Seurat inputs, use `Seurat::FetchData()` or the helper `fetch_seurat_violin_data()`. Only sync `active.ident` into a metadata column when that is truly the intended `celltype`.
3. Compute per-cell-type statistics.
   Run `wilcox.test(expression ~ group, exact = FALSE)` inside each cell type, skip cell types that do not contain both groups, and apply BH correction across the tested cell types.
4. Place annotations dynamically.
   Compute `y_pos` from the observed range in each cell type instead of hard-coding a fixed label height.
5. Plot and export.
   Use `geom_violin()` plus optional boxplot or jitter layers, add `geom_text()` for stars, and save both the plot and the CSV stats table when the user wants a reproducible figure bundle.

## Guardrails

- Set the group order explicitly. Do not trust alphabetical ordering when the labels carry biological meaning such as `control` and `AML`.
- State whether the stars come from raw p values or BH-adjusted p values. The pasted source computes both; the helper defaults to stars from `p_adj`.
- Use the ggplot route once significance is required. `split.by` in `VlnPlot()` is good for visual comparison, but it is not the cleanest path for per-cell-type annotation.
- Cache extracted expression when looping many genes. Repeatedly pulling from a large Seurat object is slower than reusing a prepared data frame or expression matrix.
- Keep the output table. The plot is only half of the result; the table is what lets the user audit sample sizes, medians, and adjusted p values later.

## Output Rules

- Return code that can run against the user's real metadata column names instead of classroom placeholders.
- Preserve the comparison labels, color mapping, and cell-type order in the output code.
- When exporting multiple genes, write one PDF and one CSV per gene unless the user asks for a combined artifact.

## Resources

- [scripts/significant_violin_plots.R](scripts/significant_violin_plots.R)
  Use this helper when you want a reusable Seurat-to-ggplot workflow with built-in per-cell-type Wilcoxon testing, BH correction, and batch export.
- [references/source-map.md](references/source-map.md)
  Read this when you need the provenance and the exact pattern extracted from the pasted example.

## Minimal Pattern

```r
source("C:/Users/simon/.codex/skills/scrna-significant-violin-plots/scripts/significant_violin_plots.R")

plot_df <- fetch_seurat_violin_data(
  seurat_object = seurat_obj,
  gene = "MS4A1",
  group_col = "group",
  celltype_col = "celltype"
)

result <- plot_significant_violin(
  plot_df,
  fill_colors = c(control = "#4E79A7", AML = "#E15759"),
  title = "MS4A1",
  star_by = "p_adj"
)

ggplot2::ggsave("MS4A1.geom_violin.pdf", result$plot, width = 7, height = 5)
write.csv(result$stats, "MS4A1.wilcox_results.csv", row.names = FALSE)
```
