---
name: phylogenetics-router
description: Focused router for phylogenetics and tree-analysis skills. Trigger when the task is evolutionary tree inference, tree IO, distance calculations, divergence dating, or phylogenetic visualization and the library contains both bio-phylo and bio-phylogenetics naming families.
---

# phylogenetics-router

Use this router when:
- the task is phylogenetic tree building, tree manipulation, divergence dating, or evolutionary distance analysis
- the request mentions phylo or phylogenetics and you want one canonical entrypoint

Routing guidance:
- Use bio-phylo-* and bio-phylogenetics-* as one family during routing.
- Use the plain phylogenetics skill or tooluniverse-phylogenetics when the request is broader or tool-aggregation oriented.
- Use scientific-computing-router only when the task is generic graph or numerical logic rather than domain phylogeny.

Examples:
- route a phylogenetic tree inference task
- which skill should handle tree visualization
- canonical entrypoint for bio-phylo and bio-phylogenetics