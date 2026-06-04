# Source Map

## Routed Source

- SCENIC regulon network analysis: `E:/BaiduNetdiskDownload/SCENIC转录因子调控网络分析.html`

## Included Here

- SCENIC preparation and compact workflow.
- Co-expression network and regulon construction.
- GRN score or AUCell activity interpretation.
- Output files and downstream regulon network plotting.

## Repo-Local Note

- In `/home/h2048`, place reusable orchestration code under `script/py` or `script/R`, and store large SCENIC outputs under `data/py/<YYYYMMDD>/...` or shared `int/` intermediates rather than the repository root.

## Excluded To Avoid Conflicts

- hdWGCNA module analysis lives in `biomamba-hdwgcna-pipeline`.
- Generic Seurat preprocessing lives in `biomamba-scrna-seurat-v5`.
