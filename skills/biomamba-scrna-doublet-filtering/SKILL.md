---
name: biomamba-scrna-doublet-filtering
description: "Use only when the user mentions Biomamba, 双细胞过滤手册, the provided HTML notes, or asks for that DoubletFinder, cxds, bcds, scds, pN, pK, pANN workflow. For generic doublet removal prefer existing generic single-cell doublet skills; do not use for Seurat preprocessing or Figure 1 plotting."
---

# Biomamba scRNA Doublet Filtering

## Scope

Use this skill after initial Seurat QC and before final downstream interpretation. It covers doublet detection and removal, especially DoubletFinder and `scds` methods such as `cxds` and `bcds`.

Use `biomamba-scrna-seurat-v5` for generic object creation, QC, and clustering. Return here when the user asks about doublets, singlets, pANN, pK, pN, homotypic doublets, DoubletFinder, cxds, bcds, or scds.
For generic doublet workflows not tied to the Biomamba tutorial, prefer `bio-single-cell-doublet-detection`.

## Repository Fit

When applying doublet review inside `/home/h2048`:

- This repo commonly uses Seurat v5 plus DoubletFinder / `scds`; if the input is a repo-generated `.h5ad`, hand off through `GetSeurat()` or an existing `.rds` before running doublet calls.
- Run per sample or lane when experimentally appropriate, and persist the exact thresholds / expected rate / final metadata column used for singlet filtering.
- Save filtered objects and QC summaries under `data/R/<YYYYMMDD>/...`, logs under `logs/<YYYYMMDD>/...`, and document the decision in `docs/experiments/`.

## Workflow

1. Start with a Seurat object that has already removed obvious low-quality cells.
2. Keep distinct 10X lanes or library preparations separate for doublet calling unless the experimental design proves they can be mixed.
3. Run DoubletFinder when accuracy and interpretability matter.
4. Run `cxds` or `bcds` from `scds` when speed, memory, and large data scaling matter.
5. Visualize doublet scores by cluster and embedding before removing cells.
6. Remove cells by expected doublet count, score quantile, suspicious cluster, or a combination; document the rule.
7. Rerun dimensionality reduction and clustering after filtering.

## References

Read `references/workflow.md` for parameters and code patterns.
Read `references/source-map.md` for boundaries and provenance.
