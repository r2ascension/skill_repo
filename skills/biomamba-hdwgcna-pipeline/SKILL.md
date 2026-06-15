---
name: biomamba-hdwgcna-pipeline
description: "Source-specific Biomamba hdWGCNA_pipline overlay for single-cell Seurat metacell co-expression modules. Use only when the user mentions Biomamba, hdWGCNA_pipline, the provided HTML notes, or asks to reuse that hdWGCNA tutorial's metacell, soft-power, module eigengene, hub gene, trait correlation, enrichment, marker overlap, DME, or motif workflow. Do not use for SCENIC regulons or generic Seurat preprocessing."
---

# Biomamba hdWGCNA Pipeline

## Scope

Use this skill for hdWGCNA analysis on a prepared Seurat object. It starts after basic single-cell preprocessing and focuses on metacell-based co-expression modules.

Keep boundaries clear:

- Use `$biomamba-scrna-seurat-v5` before hdWGCNA if the object is not ready.
- Use `$biomamba-scenic-regulons` for TF regulons and AUCell, not this skill.

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
