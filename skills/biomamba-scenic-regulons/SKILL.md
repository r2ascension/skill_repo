---
name: biomamba-scenic-regulons
description: "Use only when the user mentions Biomamba, SCENIC转录因子调控网络分析, the provided HTML notes, or asks to reproduce that SCENIC workflow for co-expression inference, regulon construction, AUCell scoring, differential regulon activity, or network plotting. Do not use for hdWGCNA modules."
---

# Biomamba SCENIC Regulons

## Scope

Use this skill for SCENIC transcription factor regulon analysis and network plotting. It covers the compact Biomamba SCENIC workflow and downstream visualization of regulon activity.

Use `biomamba-hdwgcna-pipeline` for hdWGCNA modules. Use `biomamba-scrna-seurat-v5` for preprocessing before SCENIC.
For generic pySCENIC methodology rather than Biomamba-tutorial reproduction, prefer `bio-gene-regulatory-networks-scenic-regulons`.

## Repository Fit

When applying SCENIC in `/home/h2048`:

- Keep heavy intermediates such as adjacency tables, regulon objects, and AUC matrices under `data/py/<YYYYMMDD>/...` or `int/` when they are intentionally shared across scripts.
- If the starting object comes from the repo Python→R handoff, keep `sample`, `tissue`, `celltype`, and `seurat_clusters` style metadata synchronized before attaching regulon activity back to the object.
- Put reusable wrappers under `script/py` or `script/R`, keep logs under `logs/<YYYYMMDD>/...`, and journal substantive runs in `docs/experiments/`.

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
