---
name: chipseq-router
description: Focused router for ChIP-seq and closely related chromatin immunoprecipitation analysis skills. Trigger when the task is peak calling, motif analysis, binding analysis, visualization, or an end-to-end ChIP-seq pipeline and the library contains both bio-chip-seq and bio-chipseq naming variants.
---

# chipseq-router

Use this router when:
- the request is specifically about ChIP-seq analysis
- the task mentions peak calling, motif analysis, differential binding, super enhancers, or ChIP-seq visualization
- you need a single canonical entrypoint for both bio-chip-seq and bio-chipseq naming families

Routing guidance:
- Use the bio-chip-seq-* and bio-chipseq-* skills as one combined family; do not treat the hyphenation difference as a conceptual difference.
- Use chipseq-pipeline-and-annotation or bio-workflows-chipseq-pipeline when the request is full-pipeline rather than a single operation.
- Use bio-visualization-router for downstream plotting emphasis after the core ChIP-seq task is selected.

Examples:
- route this ChIP-seq peak-calling task
- which ChIP-seq skill should handle motif analysis
- I need the canonical entrypoint for chipseq skills