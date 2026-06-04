# Seurat V5 Workflow

## Data Reading

Choose the loader by input type:

- 10X directory with `barcodes.tsv`, `features.tsv` or `genes.tsv`, and `matrix.mtx`: use `Read10X(data.dir = ...)`.
- 10X h5: use `Read10X_h5(...)`.
- Plain matrix: load with `read.table`, `read.csv`, `readRDS`, or `readxl`, then convert rows to genes and columns to cells.
- Existing object: use `readRDS(...)`.

Minimal object creation pattern:

```r
library(Seurat)
counts <- Read10X(data.dir = "filtered_feature_bc_matrix")
seu <- CreateSeuratObject(counts = counts, project = "project", min.cells = 3, min.features = 200)
seu[["percent.mt"]] <- PercentageFeatureSet(seu, pattern = "^MT-")
```

For mouse, mitochondrial genes usually use `^mt-`; for human, `^MT-`.

## Single-Sample Backbone

Use this order unless the project has a reason to change it:

```r
seu <- subset(seu, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)
seu <- NormalizeData(seu, normalization.method = "LogNormalize", scale.factor = 10000)
seu <- FindVariableFeatures(seu, selection.method = "vst", nfeatures = 2000)
seu <- ScaleData(seu, features = rownames(seu))
seu <- RunPCA(seu, features = VariableFeatures(seu))
ElbowPlot(seu)
seu <- FindNeighbors(seu, dims = 1:15)
seu <- FindClusters(seu, resolution = 0.2)
seu <- RunUMAP(seu, dims = 1:15)
DimPlot(seu, reduction = "umap", label = TRUE)
```

Tune `dims` and `resolution` from PCA, cell number, and biological granularity. Do not treat the tutorial values as universal.

## Seurat V5 Layers And Memory

Seurat V5 introduces layers. If counts cannot be retrieved in older style code, inspect `Layers(seu[["RNA"]])` and use layer-aware accessors. Avoid `as.matrix` on large sparse matrices except for a small subset.

Set parallel and memory options when running expensive integration or marker loops:

```r
library(future)
plan("multisession", workers = 8)
options(future.globals.maxSize = 20 * 1024^3)
```

## Multi-Sample Integration

Use simple merge only when batch effects are small or the goal is exploratory inspection:

```r
merged <- merge(obj1, y = list(obj2, obj3), add.cell.ids = c("S1", "S2", "S3"))
merged$sample <- sapply(strsplit(colnames(merged), "_"), `[`, 1)
```

Use Seurat anchor or CCA integration for stronger batch correction, accepting higher memory and time cost.

Use Harmony when speed and memory are priorities:

```r
library(harmony)
seu <- NormalizeData(seu)
seu <- FindVariableFeatures(seu)
seu <- ScaleData(seu)
seu <- RunPCA(seu)
seu <- RunHarmony(seu, group.by.vars = "sample")
seu <- FindNeighbors(seu, reduction = "harmony", dims = 1:20)
seu <- FindClusters(seu, resolution = 0.4)
seu <- RunUMAP(seu, reduction = "harmony", dims = 1:20)
```

Inspect UMAP colored by sample before and after correction to make sure biological separation was not erased.

## Annotation

Combine at least two evidence types:

- Known markers from CellMarker, PanglaoDB, literature, or project-specific markers.
- Cluster marker discovery with `FindAllMarkers`.
- SingleR with built-in references for broad immune and tissue classes.
- Custom SingleR reference when a matched atlas is available.
- Seurat transfer or `TransferData` when a high-quality reference object exists.

Manual renaming pattern:

```r
markers <- FindAllMarkers(seu, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.25)
new.ids <- c("Naive CD4 T", "CD14 Mono", "B", "CD8 T")
names(new.ids) <- levels(seu)
seu <- RenameIdents(seu, new.ids)
seu$cell_type <- Idents(seu)
```

## Differential Expression

Decide the comparison level first:

- Cluster marker discovery: `FindAllMarkers`.
- Pairwise groups within a cell type: subset the cell type, set `Idents` to group, then `FindMarkers`.
- Many cell types or many groups: loop and save a table per contrast.

Example:

```r
sub <- subset(seu, subset = cell_type == "Fibroblast")
Idents(sub) <- "group"
deg <- FindMarkers(sub, ident.1 = "Disease", ident.2 = "Control", min.pct = 0.1)
deg$gene <- rownames(deg)
```

## Enrichment

Use GO and KEGG for ranked or thresholded DE genes; use GSEA when a full ranked list is available; use GSVA when comparing sample or cell-level pathway scores.

```r
library(clusterProfiler)
ego <- enrichGO(gene = genes, OrgDb = org.Hs.eg.db, keyType = "SYMBOL", ont = "BP")
dotplot(ego)
```
