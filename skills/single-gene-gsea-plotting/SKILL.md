---
name: single-gene-gsea-plotting
description: "Use when performing single-gene GSEA, ranking genes by correlation with a target gene, running clusterProfiler GSEA from a named numeric vector, fixing gseaplot2 or GseaVis multi-pathway color-order mismatches, or creating NES-ordered GSEA curve figures with reliable legends."
---

# Single-Gene GSEA Plotting

## Overview

Use this skill to perform gene-centric GSEA and create reliable multi-pathway enrichment curve figures. The key visualization rule is simple: sort pathways by NES first, then assign colors and legends from that sorted order. Never trust implicit plotting order when showing multiple pathways.

## When to Use

Use for:

- Exploring pathways associated with one target gene or hub gene.
- Ranking all genes by Spearman/Pearson correlation with the target gene.
- Running `clusterProfiler::GSEA()` with a GMT or TERM2GENE table.
- Plotting multiple `enrichplot::gseaplot2()` curves with NES-consistent colors.
- Auditing figures where GSEA legend colors appear mismatched.

## Required Preflight Checks

Before GSEA, check:

- Expression matrix orientation is genes × samples/cells.
- Target gene exists exactly once in row names.
- Constant genes and all-NA genes are removed before correlation.
- Correlation vector is numeric, named, finite, and sorted decreasing.
- Gene IDs in the ranked vector match the GMT/TERM2GENE identifiers.
- GSEA result contains selected pathway IDs, not just pathway descriptions.
- Color vector length and names match the NES-ordered pathway vector.

## Environment

Core packages:

- `clusterProfiler`, `enrichplot`, `DOSE`
- `ggplot2`, `patchwork`, `cowplot`, `RColorBrewer`, `viridis`, `colorspace`
- `dplyr`, `tidyr`, `tibble`, `data.table`
- `psych` or base `stats::cor()`
- Optional ID mapping: `AnnotationDbi`, `org.Hs.eg.db`, `org.Mm.eg.db`, `biomaRt`

## Helper Files

- `R/single_gene_gsea_plotting.R` — correlation ranking, GSEA wrapper, NES sorting, safe colors, and plot composition helpers.
- `examples/example_single_gene_gsea.R` — minimal single-gene GSEA workflow.

## Core Workflow

1. Load expression matrix with genes as rows and samples/cells as columns.
2. Validate target gene and remove unusable genes.
3. Compute correlations against target gene.
4. Build `geneList = sort(named_numeric_vector, decreasing = TRUE)`.
5. Run `clusterProfiler::GSEA()`.
6. Filter results and sort selected pathways by NES.
7. Assign colors to the sorted pathway order.
8. Generate gseaplot2 curves and a manually constructed legend.
9. Export complete GSEA results, selected pathway table, color map, and PDF.

## Color and Legend Rule

Always construct a named color vector after NES ordering:

- Names should be pathway descriptions or IDs used in the legend.
- Values should be assigned in exactly the order of the plotted curves.
- Save the color map as a table for audit.

If a package assigns colors implicitly, verify the mapping or override it.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Expression matrix is samples × genes | Detect orientation and transpose intentionally. |
| Target gene has duplicated row names | Stop and require disambiguation. |
| `geneList` is unnamed or unsorted | Build and assert a named decreasing numeric vector. |
| GMT uses Entrez but matrix uses symbols | Map IDs or use a matching GMT. |
| Filtering by `Description` but plotting by `ID` | Keep both and use `ID` for `geneSetID`. |
| Color order follows user input instead of NES | Sort by NES before assigning colors. |
| Too many pathways for a qualitative palette | Use generated palettes or plot fewer pathways. |

## Minimal Verification

After plotting, verify:

- `all(names(color_map) == selected_pathways$Description)` or equivalent legend labels.
- `selected_pathways` is sorted exactly as intended by NES.
- `geneSetID` values exist in `gsea_result@result$ID`.
- Saved selected table and color map match the figure legend.
- Full GSEA result table is exported for review.
