---
name: biomamba-scenic-regulons
description: "Source-specific Biomamba SCENIC转录因子调控网络分析 overlay for tutorial-derived single-cell regulon work. Use only when the user mentions Biomamba, SCENIC转录因子调控网络分析, the provided HTML notes, or asks to reuse that SCENIC workflow for co-expression inference, regulon construction, AUCell scoring, differential regulon activity, or network plotting. Do not use for hdWGCNA modules."
---

# Biomamba SCENIC Regulons

## Scope

Use this skill for SCENIC transcription factor regulon analysis and network plotting. It covers the compact Biomamba SCENIC workflow and downstream visualization of regulon activity.

Use `$biomamba-hdwgcna-pipeline` for hdWGCNA modules. Use `$biomamba-scrna-seurat-v5` for preprocessing before SCENIC.

## Workflow

1. Prepare a filtered expression matrix and matching Seurat metadata.
2. Run SCENIC co-expression inference.
3. Build regulons using motif databases.
4. Score regulon activity with AUCell or load SCENIC outputs.
5. Attach regulon activity to the single-cell object.
6. Compare regulon activity between cell types or conditions.
7. Draw transcription factor regulatory network plots when the task asks for network-level interpretation.

## References

Read `references/workflow.md` for SCENIC stages, outputs, and plotting.
Read `references/source-map.md` for source routing.
