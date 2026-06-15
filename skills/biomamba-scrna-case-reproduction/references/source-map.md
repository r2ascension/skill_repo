# Source Map

## Routed Sources

- fibrotic skin scRNA case: `E:/BaiduNetdiskDownload/scRNA-seq揭示人纤维化皮肤病中的成纤维细胞异质性和间充质成纤维细胞增加.html`
- HNSCC early metastasis scRNA case: `E:/BaiduNetdiskDownload/scRNA-seq揭示头颈癌早期转移过程中潜在的免疫逃避机制.html`
- postnatal liver development scRNA case: `E:/BaiduNetdiskDownload/单细胞转录组学对产后肝脏发育和成熟的时间分析.html`

## Included Here

- Paper interpretation and figure-reproduction order.
- Dataset-specific download and object-loading choices.
- Case-specific subsetting, subclustering, trajectory, communication, and biological interpretation.

## Merged Content

The three sources all repeat Seurat object creation, integration, annotation, and standard visualization. Those shared steps are not copied three times. Use `$biomamba-scrna-seurat-v5` as the common backbone and this skill for case-specific decisions.

## Excluded To Avoid Conflicts

- General Figure 1 recipes live in `$biomamba-scrna-figure1-plots`.
- General doublet workflows live in `$biomamba-scrna-doublet-filtering`.
- SCENIC and hdWGCNA are separate.
