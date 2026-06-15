# SCENIC Regulon Workflow

## Inputs

Use a clean expression matrix and metadata:

- Rows are genes, columns are cells.
- Gene symbols match the organism and motif database.
- Low-quality cells and obvious doublets have already been filtered.
- Cell-type and group annotations are available for interpretation.

## Core Stages

SCENIC has three conceptual stages:

1. Infer TF-target co-expression modules, often with GENIE3 or GRNBoost.
2. Prune modules with motif enrichment to build regulons.
3. Score regulon activity per cell with AUCell.

Pseudocode:

```r
library(SCENIC)
library(AUCell)
library(RcisTarget)
library(GENIE3)

scenicOptions <- initializeScenic(
  org = "hgnc",
  dbDir = "cisTarget_databases",
  datasetTitle = "project"
)

genesKept <- geneFiltering(exprMat, scenicOptions)
exprMat_filtered <- exprMat[genesKept, ]
runCorrelation(exprMat_filtered, scenicOptions)
runGenie3(exprMat_filtered, scenicOptions)
scenicOptions <- runSCENIC_1_coexNetwork2modules(scenicOptions)
scenicOptions <- runSCENIC_2_createRegulons(scenicOptions)
scenicOptions <- runSCENIC_3_scoreCells(scenicOptions, exprMat_filtered)
```

Use the exact organism code and cisTarget database build that matches the species.

## Attach Activity To Seurat

```r
auc <- loadInt(scenicOptions, "aucell_regulonAUC")
auc_mat <- getAUC(auc)
regulon_activity <- t(auc_mat)
seurat_obj[["RegulonAUC"]] <- CreateAssayObject(counts = t(regulon_activity))
```

Or store selected regulon AUC scores in `meta.data` for plotting:

```r
seurat_obj$MYC_regulon <- as.numeric(auc_mat["MYC(+)", colnames(seurat_obj)])
FeaturePlot(seurat_obj, features = "MYC_regulon")
VlnPlot(seurat_obj, features = "MYC_regulon", group.by = "cell_type", pt.size = 0)
```

## Differential Regulon Activity

Compare regulon activity across cell types, conditions, or clusters:

```r
Idents(seurat_obj) <- "condition"
deg_auc <- FindMarkers(seurat_obj, ident.1 = "Disease", ident.2 = "Control", assay = "RegulonAUC")
```

If using `meta.data` activity columns, use `ggplot2`, Wilcoxon tests, or linear models with sample-level caution.

## Output Interpretation

Common SCENIC outputs include:

- Co-expression modules before motif pruning.
- Regulon target lists.
- Regulon AUC matrix.
- Binary regulon activity matrix.
- Regulon specificity scores.

Interpret high AUC as activity of a TF regulon, not necessarily higher TF mRNA expression.

## Network Plotting

Build a TF-target edge table from selected regulons:

```r
library(igraph)
library(ggraph)

edges <- data.frame(
  from = rep("TF", length(targets)),
  to = targets,
  weight = importance
)
graph <- graph_from_data_frame(edges, directed = TRUE)
ggraph(graph, layout = "fr") +
  geom_edge_link(aes(width = weight), alpha = 0.4) +
  geom_node_point() +
  geom_node_text(aes(label = name), repel = TRUE)
```

Keep networks small enough to read; filter by top targets or differential regulons.
