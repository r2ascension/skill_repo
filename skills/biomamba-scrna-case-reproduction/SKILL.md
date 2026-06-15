---
name: biomamba-scrna-case-reproduction
description: "Source-specific Biomamba scRNA paper-reproduction overlay combining the three provided case HTMLs: fibrotic skin fibroblast heterogeneity, head and neck cancer early metastasis immune evasion, and postnatal liver development. Use only for these paper-specific reproduction plans, figure routing, and case-specific Seurat, trajectory, subcluster, proportion, or communication analyses. For reusable methods prefer the generic scRNA skills or the other Biomamba overlays."
---

# Biomamba scRNA Case Reproduction

## Scope

Use this skill for the three paper-specific reproduction tutorials. It intentionally merges their shared Seurat backbone and splits their unique biological analyses by case.

If the user asks for generic preprocessing, plotting, doublet filtering, SCENIC, or hdWGCNA, route to the specialized skill instead.

## Case Router

- Fibrotic skin disease fibroblast heterogeneity: read 10X data, integrate samples, annotate broad cell types, focus on fibroblast subclusters, mesenchymal fibroblast signatures, ligand-receptor analysis, POSTN and collagen signals, and scleroderma comparison.
- Head and neck cancer early metastasis: read provided R data, inspect primary and lymph-node states, visualize immune and malignant compartments, calculate EMT and trajectory signals, use CytoTRACE and T cell analyses, and focus on immune evasion in early metastasis.
- Postnatal liver development: read h5 data, analyze liver cell types over time, split hepatocytes by timepoint, run Monocle2 trajectory, examine endothelial, mesenchymal, immune, macrophage, transcription-factor, metabolic, and cell-communication dynamics.

## References

Read `references/cases.md` for the routed workflows.
Read `references/source-map.md` for exact source files and overlap decisions.
