# Doublet Filtering Workflow

## Practical Tool Choice

The tutorial emphasizes the benchmark tradeoff:

- `DoubletFinder`: strong overall accuracy and usability, good default choice for Seurat workflows.
- `cxds`: fast and scalable, useful for large datasets or quick screening.
- `bcds`: useful score from the same `scds` family; combine with `cxds` if desired.
- `Solo`, `Scrublet`, and `DoubletDetection`: relevant alternatives, especially outside pure R workflows.

## Input Rules

Do not feed raw low-quality data into doublet detection. First run basic QC, normalization, variable features, PCA, and an initial clustering or embedding.

DoubletFinder should usually be run per sample or lane. Mixing lanes can create artificial doublets that could never occur experimentally.

## DoubletFinder Pattern

```r
library(Seurat)
library(DoubletFinder)

seu <- NormalizeData(seu)
seu <- FindVariableFeatures(seu)
seu <- ScaleData(seu)
seu <- RunPCA(seu)
seu <- RunUMAP(seu, dims = 1:20)
seu <- FindNeighbors(seu, dims = 1:20)
seu <- FindClusters(seu, resolution = 0.4)

sweep.res <- paramSweep(seu, PCs = 1:20, sct = FALSE)
sweep.stats <- summarizeSweep(sweep.res, GT = FALSE)
bcmvn <- find.pK(sweep.stats)
```

Pick `pK` from the BCmvn peak, then estimate expected doublets:

```r
expected_rate <- 0.08
nExp <- round(ncol(seu) * expected_rate)
homotypic.prop <- modelHomotypic(seu$seurat_clusters)
nExp.adj <- round(nExp * (1 - homotypic.prop))

seu <- doubletFinder(
  seu,
  PCs = 1:20,
  pN = 0.25,
  pK = 0.09,
  nExp = nExp.adj,
  reuse.pANN = FALSE,
  sct = FALSE
)
```

The output metadata column name contains parameter values, for example `DF.classifications_0.25_0.09_120`.

## Visual Review

Inspect both score and final classification:

```r
VlnPlot(seu, features = "pANN_0.25_0.09_120", group.by = "seurat_clusters", pt.size = 0)
DimPlot(seu, group.by = "DF.classifications_0.25_0.09_120")
FeaturePlot(seu, features = "pANN_0.25_0.09_120")
```

Remove only after checking whether high-scoring cells are technical artifacts or biologically plausible transitions.

## scds cxds and bcds Pattern

Convert through `SingleCellExperiment` when using `scds`:

```r
library(SingleCellExperiment)
library(scds)
sce <- as.SingleCellExperiment(seu)
sce <- cxds(sce)
sce <- bcds(sce)
sce <- cxds_bcds_hybrid(sce)

seu$cxds_score <- colData(sce)$cxds_score
seu$bcds_score <- colData(sce)$bcds_score
seu$hybrid_score <- colData(sce)$hybrid_score
```

Score-based removal pattern:

```r
cutoff <- quantile(seu$bcds_score, 0.92, na.rm = TRUE)
seu_singlet <- subset(seu, subset = bcds_score < cutoff)
```

## After Filtering

Recompute variable features, PCA, neighbors, clustering, and UMAP on singlets. Recheck cluster marker purity and cell proportions because doublet removal can change both.
