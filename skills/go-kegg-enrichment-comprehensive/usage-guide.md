# GO & KEGG Enrichment Analysis — Usage Guide

## Quick Start

After running differential expression analysis, ask Claude:

> "Run GO and KEGG enrichment analysis on my DEG list in data/DEG.csv"

Or for more specific requests:

> "Do GO enrichment on my significant genes and create publication-ready bar plots"
> "Which KEGG pathways are enriched in my up-regulated genes?"
> "Visualize my GO BP/CC/MF results as faceted significance plots"

## Prerequisites

Install required packages (one-time setup):

```r
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(c("clusterProfiler", "org.Hs.eg.db", "enrichplot", "GOplot"))
install.packages(c("openxlsx", "ggplot2", "dplyr"))
```

For non-human organisms, install the appropriate OrgDb (e.g., `org.Mm.eg.db` for mouse).

## Input Requirements

Your input must be a list of differentially expressed genes. The script expects one of:

| Format | Example | How to specify |
|---|---|---|
| DEG CSV with gene symbols as row names | `rownames(read.csv("data/DEG.csv"))` | Default in examples |
| DEG CSV with gene symbol column | `read.csv("data/DEG.csv")$SYMBOL` | Modify `gene_list` assignment |
| Character vector in R | `c("TP53", "BRCA1", "EGFR", ...)` | Use directly |

## What the Agent Will Do

The workflow produces:

1. **GO enrichment results** (`01.GO.xlsx`) — All significant terms across BP, CC, MF
2. **GO bar plot** (`02.GO_enrichment_barplot.pdf`) — Top 8 terms per ontology with labels
3. **GO significance plot** (`02.GO_plot.pdf`) — Faceted -log10(p.adjust) plot
4. **KEGG enrichment results** (`03.KEGG.xlsx`) — All significant pathways
5. **KEGG bar plot** (`04.KEGG_barplot.pdf`) — Top pathways colored by category
6. **KEGG significance plot** (`05.KEGG_plot.pdf`) — Pathways ranked by significance

## Customizing the Analysis

### Different species

- **Mouse**: Replace `org.Hs.eg.db` → `org.Mm.eg.db`, and `organism = "hsa"` → `organism = "mmu"`
- **Rat**: Use `org.Rn.eg.db` and `organism = "rno"`
- **Zebrafish**: Use `org.Dr.eg.db` and `organism = "dre"`
- See SKILL.md for the full organism code table

### Different gene ID types

If your genes are already ENTREZID or ENSEMBL:
- Change `keyType = "SYMBOL"` to `keyType = "ENTREZID"` or `keyType = "ENSEMBL"`
- Skip the `bitr` conversion step for KEGG

### Adjusting stringency

- **More stringent**: `pvalueCutoff = 0.01` or add `qvalueCutoff = 0.05`
- **Less stringent**: `pvalueCutoff = 0.1` (useful for small gene lists)
- **More terms in plots**: Change `slice_head(n = 8)` to `slice_head(n = 10)` or `slice_head(n = 15)`

### Filtering by direction

To analyze up- and down-regulated genes separately:

```r
degs <- read.csv("data/DEG.csv")
up_genes   <- rownames(degs)[degs$log2FoldChange > 1 & degs$padj < 0.05]
down_genes <- rownames(degs)[degs$log2FoldChange < -1 & degs$padj < 0.05]
```

Then run the enrichment workflow separately on each list.

## Interpreting Results

### GO Enrichment

| Signal | Interpretation |
|---|---|
| Many BP terms related to inflammation | Immune/inflammatory response activated |
| Cell cycle terms dominate | Proliferation changes |
| Extracellular matrix (CC) + receptor binding (MF) | Cell-ECM communication altered |
| Mitochondrial terms | Energy metabolism affected |

### KEGG Enrichment

| Signal | Interpretation |
|---|---|
| PI3K-Akt, MAPK, Ras enriched | Growth factor signaling altered |
| NF-kappa B, TNF enriched | Inflammatory signaling active |
| Glycolysis, OxPhos enriched | Metabolic reprogramming |
| Pathways in cancer enriched | Drill into sub-pathways for specific mechanisms |

### Cross-Validation

Results are more convincing when GO and KEGG tell a consistent story. Example:
- GO BP: "inflammatory response", GO MF: "cytokine receptor binding" → KEGG: "NF-kappa B signaling", "TNF signaling"
- These reinforce each other: NF-κB is a master regulator of inflammatory cytokines

## Common Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| 0 significant GO terms | Too few genes or too strict cutoff | Relax to `pvalueCutoff = 0.1` |
| 0 significant KEGG terms | ID conversion lost many genes | Check `fromType` in `bitr` matches actual IDs |
| Plots have garbled Chinese text | Missing Chinese font | Use `showtext` package or switch to English labels |
| KEGG API timeout | Server issues | Retry; or download gene sets locally |
| `ONTOLOGY` column not found | `ont` not set to `"all"` | Check `ont` parameter in `enrichGO` call |

## Related Skills

- **bio-pathway-analysis-go-enrichment** — Deep dive into GO-specific patterns
- **bio-pathway-analysis-kegg-pathways** — Deep dive into KEGG-specific patterns
- **bio-pathway-analysis-gsea** — Gene Set Enrichment Analysis (no arbitrary cutoff)
- **bio-pathway-analysis-enrichment-visualization** — More plot types (dotplot, cnetplot, emapplot)
- **differential-expression-deseq2-basics** — DESeq2 workflow upstream of enrichment
- **differential-expression-edger-basics** — edgeR workflow upstream of enrichment
