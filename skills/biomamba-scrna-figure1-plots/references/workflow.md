# Figure 1 Panel Recipes

## Standard Panel Set

A typical single-cell Figure 1 can include:

- UMAP or t-SNE by cell type, sample, and condition.
- Confidence ellipse or contour around major groups.
- QC distributions for `nFeature_RNA`, `nCount_RNA`, and `percent.mt`.
- Marker expression by known cell type.
- Cell-type proportions across groups.
- Enrichment summary from top cell-type markers or differential genes.
- A final composed layout.

## Embedding With Confidence Regions

```r
library(ggplot2)
emb <- as.data.frame(Embeddings(seu, "umap"))
emb$cell_type <- seu$cell_type
ggplot(emb, aes(UMAP_1, UMAP_2, color = cell_type)) +
  geom_point(size = 0.2, alpha = 0.7) +
  stat_ellipse(aes(group = cell_type), linewidth = 0.4, show.legend = FALSE) +
  theme_classic()
```

Use ellipses only when they clarify cluster-level spread. For dense atlases, contours or no confidence region may be cleaner.

## QC Summary

```r
VlnPlot(seu, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3, pt.size = 0)
FeatureScatter(seu, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
FeatureScatter(seu, feature1 = "nCount_RNA", feature2 = "percent.mt")
```

For manuscript panels, prefer violin or box summaries with minimal points to avoid visual clutter.

## Marker Panels

```r
DotPlot(seu, features = marker_list, group.by = "cell_type") +
  RotatedAxis()

VlnPlot(seu, features = c("COL1A1", "PECAM1", "PTPRC"), group.by = "cell_type", pt.size = 0)

FeaturePlot(seu, features = c("COL1A1", "PECAM1"), reduction = "umap")
```

Make marker lists explicit and ordered by cell type.

## Cell Proportions

```r
library(dplyr)
prop <- as.data.frame(table(seu$group, seu$cell_type))
colnames(prop) <- c("group", "cell_type", "n")
prop <- prop %>% group_by(group) %>% mutate(frac = n / sum(n))

ggplot(prop, aes(group, frac, fill = cell_type)) +
  geom_col(position = "fill", width = 0.75) +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

For statistical comparison of proportions, decide whether samples or cells are the unit. Do not run cell-level tests when biological replicates are required.

## Enrichment Panel

Use enrichment on cell-type markers or group DE genes. Typical display choices:

- `clusterProfiler::dotplot`
- `enrichplot::cnetplot`
- top terms as a custom `ggplot2` bar chart

## Layout

```r
library(patchwork)
final <- (p_umap | p_qc) / (p_marker | p_prop)
ggsave("figure1.pdf", final, width = 10, height = 8)
```

Keep labels and colors consistent. Export vector PDF for editing and high-resolution TIFF or PNG for submission systems that require raster images.
