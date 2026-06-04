# hdWGCNA Workflow

## Setup

```r
library(Seurat)
library(hdWGCNA)
library(WGCNA)
library(tidyverse)

seurat_obj <- SetupForWGCNA(
  seurat_obj,
  gene_select = "fraction",
  fraction = 0.05,
  wgcna_name = "tutorial"
)
```

Use `gene_select = "fraction"` when you want genes expressed in at least a fraction of cells. Adjust the fraction by dataset size and sparsity.

## Metacells

Metacells reduce single-cell sparsity. Group by cell type plus sample when possible:

```r
seurat_obj <- MetacellsByGroups(
  seurat_obj = seurat_obj,
  group.by = c("cell_type", "Sample"),
  reduction = "harmony",
  k = 25,
  max_shared = 10,
  ident.group = "cell_type"
)
seurat_obj <- NormalizeMetacells(seurat_obj)
```

Build networks within a coherent cell class or lineage, not across unrelated compartments unless the research question truly requires it.

## Expression Matrix And Soft Power

```r
seurat_obj <- SetDatExpr(
  seurat_obj,
  group_name = "INH",
  group.by = "cell_type",
  assay = "RNA",
  slot = "data"
)

seurat_obj <- TestSoftPowers(seurat_obj, networkType = "signed")
PlotSoftPowers(seurat_obj)
```

Choose a soft power that balances scale-free topology fit and mean connectivity.

## Construct Network And Modules

```r
seurat_obj <- ConstructNetwork(
  seurat_obj,
  tom_name = "INH",
  overwrite_tom = TRUE
)

seurat_obj <- ModuleEigengenes(seurat_obj, group.by.vars = "Sample")
seurat_obj <- ModuleConnectivity(seurat_obj, group.by = "cell_type", group_name = "INH")
seurat_obj <- ResetModuleNames(seurat_obj, new_name = "INH-M")
```

Use harmonized module eigengenes when sample or batch effects are present.

## Module And Hub Visualization

```r
ModuleFeaturePlot(seurat_obj, features = "hMEs", order = TRUE)
ModuleCorrelogram(seurat_obj)
DotPlot(seurat_obj, features = GetModules(seurat_obj)$module) + RotatedAxis()
HubGeneNetworkPlot(seurat_obj, n_hubs = 5, n_other = 10)
```

Hub genes come from module connectivity and should be interpreted with expression specificity and biology.

## Trait Correlation

Prepare metadata carefully before correlation:

```r
traits <- c("age", "sex", "disease_score")
seurat_obj <- ModuleTraitCorrelation(seurat_obj, traits = traits, group.by = "cell_type")
PlotModuleTraitCorrelation(seurat_obj)
```

Convert categorical traits to factors and numeric traits to numeric before correlation.

## Enrichment And Marker Overlap

```r
enrich <- RunEnrichr(
  seurat_obj,
  dbs = c("GO_Biological_Process_2021", "KEGG_2021_Human")
)
PlotEnrichrBar(enrich)

markers <- FindAllMarkers(seurat_obj, group.by = "cell_type")
overlap <- OverlapModulesDEGs(seurat_obj, deg_df = markers)
```

Use enrichment as module interpretation, not as proof of cell identity by itself.

## Differential Module Eigengenes

Use DME to compare module activity between groups:

```r
dme <- FindDMEs(seurat_obj, group.by = "condition", group1 = "Disease", group2 = "Control")
PlotDMEsLollipop(dme)
```

For multi-group comparisons, loop contrasts and keep the reference group explicit.

## Motif Overlap

Motif overlap is optional and more fragile. Use when the user explicitly asks about TF motif enrichment in modules:

```r
seurat_obj <- MotifScan(seurat_obj, species = "human")
overlap <- MotifOverlap(seurat_obj)
```

Validate genome build, species, and gene naming before interpreting motif results.
