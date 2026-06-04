# Source Map

## Routed Source

- hdWGCNA pipeline: `E:/BaiduNetdiskDownload/hdWGCNA_pipline.html`

## Included Here

- hdWGCNA setup, metacell creation, network construction, visualization, trait correlation, enrichment, marker overlap, DME, and motif overlap.

## Repo-Local Note

- In `/home/h2048`, prefer existing Seurat objects or `GetSeurat()` imports as hdWGCNA inputs, save outputs under `data/R/<YYYYMMDD>/...`, and keep reusable orchestration code in `script/R`.

## Excluded To Avoid Conflicts

- Generic Seurat object preparation is in `biomamba-scrna-seurat-v5`.
- SCENIC regulon activity analysis is in `biomamba-scenic-regulons`.
