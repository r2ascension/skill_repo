---
name: bio-single-cell-router
description: Second-level router for single-cell and single-nucleus omics workflows. Trigger when the task is scRNA-seq, single-cell ATAC, trajectory, cell annotation, cell communication, or Scanpy or Seurat style analysis and you need to choose among the large single-cell skill cluster.
---

# bio-single-cell-router

Use this router when:
- the task is scRNA-seq, snRNA-seq, single-cell ATAC, multimodal single-cell, or cell-state analysis
- the user mentions annotation, clustering, doublets, trajectory, velocity, or cell communication in a single-cell context

Routing guidance:
- Use bio-single-cell-* skills for precise single-cell operations grouped by task such as preprocessing, clustering, annotation, communication, and trajectory inference.
- Use scrna-* skills when the workflow is Seurat, Harmony, Monocle, module scoring, CNV calling, or other scRNA-specific analysis stacks.
- Use biomamba-scrna-* skills when the request matches those prebuilt practice and plotting workflows.
- Use scanpy, scvi-tools, or scvelo when the user explicitly wants those concrete libraries.
- Use bio-learning-single-cell-core-analysis, bio-learning-single-cell-qc-and-parameter-tuning, bio-learning-single-cell-experimental-design-and-multiplexing, or bio-learning-cell-communication-and-microenvironment when the user is asking for maintained single-cell learning content organized by function rather than a direct analysis workflow.
- Use geoagent-geo-discovery before this router when the real bottleneck is finding or standardizing GEO single-cell cohorts, sample pairings, or assay labels instead of analyzing an already selected dataset.

Examples:
- route this scRNA-seq annotation task
- I need the right single-cell clustering or doublet skill
- help choose between Scanpy, Seurat, and trajectory skills