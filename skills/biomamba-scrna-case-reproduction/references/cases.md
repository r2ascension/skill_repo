# scRNA Case Reproduction Workflows

## Shared Reproduction Rules

1. Start by writing a figure-to-analysis map before coding.
2. Load or recreate the Seurat object.
3. Attach sample, group, tissue, patient, and timepoint metadata immediately.
4. Reproduce broad UMAP and cell-type annotation before subset analyses.
5. For each subanalysis, save an intermediate object so failures do not require restarting from raw data.
6. Expect version and random-seed differences; aim to reproduce analysis logic, not pixel-identical figures.

Shared Seurat backbone:

```r
seu <- NormalizeData(seu)
seu <- FindVariableFeatures(seu)
seu <- ScaleData(seu)
seu <- RunPCA(seu)
seu <- RunHarmony(seu, group.by.vars = "sample")
seu <- FindNeighbors(seu, reduction = "harmony", dims = 1:20)
seu <- FindClusters(seu, resolution = 0.4)
seu <- RunUMAP(seu, reduction = "harmony", dims = 1:20)
```

## Fibrotic Skin Disease Case

Biological focus:

- Human fibrotic skin disease and scar tissue.
- Fibroblast heterogeneity.
- Mesenchymal fibroblast expansion.
- Ligand-receptor interactions among fibroblast subclusters and other compartments.
- POSTN-associated collagen expression.
- sC1 versus sC4 fibroblast mesenchymal-like state.
- Scleroderma comparison.

Reproduction order:

1. Download or load 10X matrices.
2. Merge samples and add disease or scar group metadata.
3. Run Harmony or equivalent integration.
4. Annotate broad cell classes.
5. Subset fibroblasts and recluster.
6. Score or visualize mesenchymal markers and collagen markers.
7. Run ligand-receptor or cell-communication analysis.
8. Validate POSTN and collagen relationships with expression plots and group comparisons.

Useful plot types: broad UMAP, fibroblast subcluster UMAP, marker dot plot, group proportion stacked bar, violin or feature plot for `POSTN`, `COL1A1`, `COL1A2`, and communication bubble or chord plots.

## Head And Neck Cancer Early Metastasis Case

Biological focus:

- Primary tumor and lymph-node metastasis.
- Early metastatic immune evasion.
- Malignant cell state changes.
- CD8 T cell evolution, dysfunction, exhaustion, and clone-related interpretation.
- Pre-metastatic or nodal microenvironment.

Reproduction order:

1. Load the provided R data object.
2. Clean metadata for tissue, lesion type, patient, and broad cell classes.
3. Draw broad UMAP and marker violin plots.
4. Summarize cell-type proportions by group.
5. Calculate EMT scores on malignant or epithelial compartments.
6. Run trajectory analysis and CytoTRACE where appropriate.
7. Subset malignant cells and T cells for focused reclustering.
8. Interpret CD8 T cell exhaustion or dysfunction using marker panels.

Code skeleton:

```r
seu <- readRDS("case_object.rds")
DimPlot(seu, group.by = "cell_type", label = TRUE)
VlnPlot(seu, features = c("EPCAM", "PTPRC", "CD3D", "CD8A"), group.by = "cell_type")
seu <- AddModuleScore(seu, features = list(emt_genes), name = "EMT_score")
FeaturePlot(seu, features = "EMT_score1")
```

## Postnatal Liver Development Case

Biological focus:

- Postnatal liver development and maturation.
- Timepoint-specific hepatocyte transcriptional profiles.
- Transcription factor activity and metabolic function dynamics.
- Endothelial and mesenchymal development.
- Hematopoietic and immune population changes.
- Transient macrophage subtype around postnatal day 7.
- Predicted liver cell communication.

Reproduction order:

1. Read the h5 matrix with `Read10X_h5`.
2. Create Seurat object and attach timepoint metadata.
3. Run standard clustering and annotate liver cell types.
4. Split hepatocytes by timepoint and recluster if needed.
5. Run Monocle2 pseudotime for developmental ordering.
6. Show marker and timepoint distributions with UMAP, ridge, violin, and heatmap plots.
7. Summarize immune and macrophage proportions over time.
8. Run cell-communication analysis for developmental interactions.

Monocle2 skeleton:

```r
library(monocle)
expr <- GetAssayData(hep, assay = "RNA", slot = "counts")
pd <- new("AnnotatedDataFrame", data = hep@meta.data)
fd <- new("AnnotatedDataFrame", data = data.frame(gene_short_name = rownames(expr), row.names = rownames(expr)))
cds <- newCellDataSet(expr, phenoData = pd, featureData = fd)
cds <- estimateSizeFactors(cds)
cds <- estimateDispersions(cds)
cds <- reduceDimension(cds, method = "DDRTree")
cds <- orderCells(cds)
```
