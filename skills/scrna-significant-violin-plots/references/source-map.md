# Source Map

## Coverage

- Skill: `scrna-significant-violin-plots`
- Source artifact: `C:\Users\simon\.codex\attachments\926e5ad9-3f49-414f-814c-5cba94c46a09\pasted-text.txt`
- Focus: Seurat expression visualization, especially grouped violin plots with per-cell-type significance annotation.

## Extracted Pattern

- Use `FetchData()` or a cached expression matrix to build a per-cell data frame with `expression`, `group`, and `celltype`.
- Run `wilcox.test(expr ~ group, exact = FALSE)` separately inside each cell type.
- Apply BH correction across the per-cell-type tests.
- Compute a dynamic `y_pos` from the local maximum expression so the stars do not overlap the violin body.
- Draw the final figure with `ggplot2::geom_violin()` plus optional boxplot or jitter, then add `geom_text()` for `*`, `**`, `***`, `****`, or `ns`.

## Use This Reference When

- The user pasted or named the same tutorial-like code and wants it turned into reusable code.
- The user wants the significance-annotated violin output but still cares about neighboring `FeaturePlot`, `VlnPlot`, or `DotPlot` conventions from the same source.
- The user wants one PDF and one CSV per gene rather than only an on-screen plot.

## Notes

- The original source computes both raw and adjusted p values. Prefer stars from `p_adj` unless the user explicitly asks for raw-p-value stars.
- `Seurat::VlnPlot(..., split.by = "group")` is good for a fast comparison panel, but once stars are required it is cleaner to switch to a ggplot data frame workflow.
