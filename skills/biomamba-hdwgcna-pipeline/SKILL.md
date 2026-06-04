---
name: biomamba-hdwgcna-pipeline
description: "Use only when the user mentions Biomamba, hdWGCNA_pipline, the provided HTML notes, or asks to reproduce that hdWGCNA tutorial's metacell, soft-power, module eigengene, hub gene, trait correlation, enrichment, marker overlap, DME, or motif workflow. Do not use for SCENIC regulons or generic Seurat preprocessing."
---

# Biomamba hdWGCNA Pipeline

## Scope

Use this skill for hdWGCNA analysis on a prepared Seurat object. It starts after basic single-cell preprocessing and focuses on metacell-based co-expression modules.

Keep boundaries clear:

- Use `biomamba-scrna-seurat-v5` before hdWGCNA if the object is not ready.
- Use `biomamba-scenic-regulons` for TF regulons and AUCell, not this skill.
- For bulk-expression WGCNA rather than single-cell metacell modules, prefer `bulk-wgcna-analysis`.

## Repository Fit

When using this tutorial inside `/home/h2048`:

- The R side of this repo is Seurat v5-first; if the starting point is a repo-produced `.h5ad`, prefer the existing `GetSeurat()` handoff or a saved `.rds` object rather than rebuilding from raw matrices.
- Keep lineage- or cell-type-specific networks separate; this repository usually analyzes coherent compartments rather than a whole mixed atlas in one hdWGCNA run.
- Save reusable code under `script/R`, dated outputs under `data/R/<YYYYMMDD>/...`, logs under `logs/<YYYYMMDD>/...`, and journal substantive runs in `docs/experiments/`.

## Workflow

1. Load the Seurat object and required packages.
2. Initialize hdWGCNA with `SetupForWGCNA`.
3. Build metacells by cell type, sample, or another grouping variable.
4. Set expression data for one biologically coherent subset at a time.
5. Test soft powers and select a power.
6. Construct the co-expression network.
7. Compute module eigengenes, harmonized MEs, module connectivity, and hub gene scores.
8. Visualize modules, correlations, network structure, hub genes, and module-trait relationships.
9. Run enrichment, marker overlap, DME analysis, and optional motif overlap.

## References

Read `references/workflow.md` for hdWGCNA code patterns.
Read `references/source-map.md` for source routing.
