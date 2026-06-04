# Source Map

## Routed Source

- bulk RNA-seq practice: `E:/BaiduNetdiskDownload/转录组实战.html`

## Included Here

- Aspera download.
- FASTQ quality filtering.
- HISAT2 reference index and alignment.
- featureCounts count matrix.
- TPM and FPKM calculation.
- Differential expression and visualization.
- Enrichment and rMATS alternative splicing.

## Repo-Local Note

- In `/home/h2048`, translate the tutorial's scratch directories into repository conventions such as `data/bulk/`, `data/R/<YYYYMMDD>/...`, `data/py/<YYYYMMDD>/...`, and `logs/<YYYYMMDD>/...`.
- Reusable wrappers belong in `script/bash` and reusable downstream code belongs in `script/R` or `script/py`.

## Excluded To Avoid Conflicts

- Single-cell workflows are in the Biomamba scRNA skills.
- multiMiR target database queries are in `biomamba-multimir-mirna`.
