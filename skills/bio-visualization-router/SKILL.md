---
name: bio-visualization-router
description: Second-level router for bioinformatics figures, omics visualization, and result rendering. Trigger when the task is to visualize biological analysis outputs and you need to choose among the concentrated figure and plotting skills.
---

# bio-visualization-router

Use this router when:
- the task is to plot omics results, export publication figures, or build biological visual summaries
- the request mentions heatmaps, volcano plots, circos plots, tracks, upset plots, or multi-panel omics figures

Routing guidance:
- Use bio-data-visualization-* skills for omics-specific plot types and figure composition.
- Use bio-reporting-* skills when the request is about report or notebook output rather than a single figure.
- Use scientific-visualization, matplotlib, or plotly when the work shifts out of the biology-specific plotting stack.

Examples:
- make a volcano or heatmap figure for these DE results
- route this genome-track visualization task
- I need the right omics plotting skill