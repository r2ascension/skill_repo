---
name: cellchat-visualization
description: "Use when visualizing or comparing CellChat communication results across multiple groups, conditions, tissues, samples, or cell types, especially CellChat bubble plots, source or target signaling views, ligand-receptor interaction probabilities, pathway filtering, and globally ordered multi-panel ggplot figures."
---

# CellChat Visualization

## Overview

Use this skill to extract structured communication tables from CellChat objects and create comparable multi-group visualizations. The main pattern is to call `netVisual_bubble(..., return.data = TRUE)`, standardize the returned `communication` table, merge across groups, apply global ordering, and draw a unified ggplot bubble plot.

This skill is for visualization and comparison of already-computed CellChat objects. It does not replace the upstream CellChat workflow (`computeCommunProb()`, `computeCommunProbPathway()`, `aggregateNet()`, etc.).

## When to Use

Use for:

- Comparing CellChat results from control vs treatment vs disease groups.
- Showing one target cell type as sender (`source`) or receiver (`target`).
- Creating publication-ready multi-group bubble plots with shared probability scales.
- Extracting CellChat ligand-receptor/pathway tables for downstream statistics.
- Avoiding independent CellChat plots with inconsistent x/y axis ordering.

## Required Preflight Checks

Before plotting, check:

- Each input object inherits from `CellChat`.
- The target cell type exists in `cellchat_obj@idents` or equivalent identity field.
- CellChat probability/pathway calculations were already run.
- `netVisual_bubble(..., return.data = TRUE)` returns a usable `communication` table.
- Required columns can be standardized: source, target, interaction, pathway, probability/weight, optional p-value.
- Empty groups are handled explicitly rather than silently disappearing.
- Group order and color mapping are fixed before plotting.

## Environment

Core packages:

- `CellChat`, `ggplot2`, `dplyr`, `tidyr`, `data.table`, `forcats`, `stringr`, `purrr`
- Optional: `patchwork`, `cowplot`, `RColorBrewer`, `viridis`, `readr`, `qs`, `qs2`

Use `qs::qread()` or `readRDS()` depending on object format. If tutorials mention `qs2::qs_read()` but `qs2` is unavailable, prefer a project-level compatibility wrapper that tries `qs2`, then `qs`, then `readRDS` based on file extension.

## Helper Files

- `R/cellchat_multigroup_bubble.R` — extraction, validation, ordering, and plotting helpers.
- `examples/example_multigroup_bubble.R` — minimal source/target bubble workflow.

## Core Workflow

1. Load CellChat objects into a named list; names become group labels.
2. For each object, call `extract_cellchat_bubble_data()` with `role = "source"` or `"target"`.
3. Standardize columns and create `source_target = paste(source, target, sep = " -> ")`.
4. Merge all groups with `data.table::rbindlist()`.
5. Filter by probability, p-value, global top pathways, and per-group top ligand-receptor interactions.
6. Compute global factor levels for `interaction_name` and `source_target`.
7. Plot with `plot_multigroup_cellchat_bubble()` and `facet_grid(. ~ group, scales = "free_x", space = "free_x")`.
8. Export both plot and tables for audit.

## Recommended Outputs

Always save:

- `cellchat_bubble_merged_communication.tsv`
- `cellchat_bubble_global_pathway_ranking.tsv`
- `cellchat_bubble_per_group_top_lr.tsv`
- `cellchat_bubble_axis_order.tsv`
- `cellchat_multigroup_source_bubble.pdf` or `cellchat_multigroup_target_bubble.pdf`
- `sessionInfo.txt`

## Sorting Rules

Use deterministic ordering:

- `interaction_name`: mean or max probability across all groups, descending; ties by name.
- `source_target`: max probability across all groups, descending; ties by name.
- `group`: explicit user-provided order, never alphabetical unless requested.

This prevents false visual differences from independent per-group ordering.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Target cell type not present in one group | Warn and return a standard empty table for that group. |
| Bubble sizes are scaled independently per group | Map `size = prob` on the merged table and use one global scale. |
| Axis order differs between facets | Compute global factor levels before plotting. |
| Returned column names differ across CellChat versions | Use alias mapping for `prob`, `weight`, `pval`, and pathway columns. |
| Plot is too crowded | Lower per-group top N, filter pathways, increase width, or paginate. |
| Large CellChat objects exhaust memory | Extract communication tables one object at a time, then discard objects and call `gc()`. |

## Minimal Verification

After extraction, verify:

- `table(df$group)` contains all expected groups or explicit empty-group records.
- `all(c("source", "target", "interaction_name", "pathway_name", "prob", "group") %in% names(df))`.
- `summary(df$prob)` is finite and non-negative.
- Factor levels for `interaction_name` and `source_target` are identical across facets.
- Saved PDF opens and tables match plotted data.
