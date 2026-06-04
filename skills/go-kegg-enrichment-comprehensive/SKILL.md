---
name: go-kegg-enrichment-comprehensive
description: "Use when performing end-to-end GO and KEGG enrichment analysis on differential expression gene lists, including both over-representation testing and publication-quality visualization (bar plots, faceted significance plots). Covers gene ID conversion, multi-ontology GO analysis (BP/CC/MF), KEGG pathway mapping, result filtering/sorting, Excel export, and result interpretation. Triggers on requests like 'do GO/KEGG enrichment on my DEGs', 'visualize enrichment results', 'pathway analysis for RNA-seq'."
tool_type: r
primary_tool: clusterProfiler
related_tools: [org.Hs.eg.db, enrichplot, GOplot, openxlsx, ggplot2, dplyr]
version: 1.1.0
---

## Version Compatibility

Reference examples tested with: R >= 4.0, clusterProfiler >= 4.10, org.Hs.eg.db >= 3.18, enrichplot >= 1.22, GOplot >= 1.0.2, openxlsx >= 4.2, ggplot2 >= 3.5

Before using code patterns, verify installed versions match. If versions differ:
- R: `packageVersion('<pkg>')` then `?function_name` to verify parameters

If code throws errors, introspect the installed package and adapt the example to match the actual API rather than retrying.

# GO & KEGG Enrichment Analysis — Complete Workflow

## Overview

After differential expression analysis, you typically have a long list of significantly up/down-regulated genes. Individual gene names offer limited insight — enrichment analysis reveals the **biological themes** behind these coordinated changes.

- **GO (Gene Ontology)**: Standardized functional annotation across three dimensions — Biological Process (BP), Cellular Component (CC), Molecular Function (MF). Answers: *"What are these genes doing?"*
- **KEGG (Kyoto Encyclopedia of Genes and Genomes)**: A pathway map integrating genes, proteins, and metabolites into signaling and metabolic networks. Answers: *"Which pathways are these genes working together in?"*

> **TL;DR**: GO tells you what genes do; KEGG tells you where they work together.

## When to Use This Skill

| Your situation | What to do |
|---|---|
| You have a DEG list (padj < 0.05, \|log2FC\| > 1) and want biological interpretation | Full workflow below |
| You have a ranked gene list (no arbitrary cutoff) | Use `bio-pathway-analysis-gsea` instead |
| You only need GO analysis | Core workflow below (Step 2) |
| You only need KEGG analysis | Use Step 3 below |
| You want publication-ready figures | Use the visualization sections in this skill |
| You have < 20 significant genes | ORA has low power; consider GSEA or relax cutoffs |

### ORA vs GSEA Decision Guide

| Scenario | Method | Why |
|----------|--------|-----|
| Clear DE gene list with arbitrary cutoff (padj + FC) | ORA, but consider GSEA instead | ORA discards magnitude; GSEA uses all genes ranked by statistic |
| Genes from co-expression module, GWAS loci, screen hits | ORA | No ranking available; ORA is appropriate |
| All genes with DE statistics available | GSEA (gseGO) | Avoids arbitrary cutoff; detects subtle coordinated changes |
| Very few DE genes (< 20) | GSEA | ORA has no power with small lists |
| RNA-seq with known length bias | GOseq (goseq package) | Standard ORA ignores length bias; longer genes are more likely DE |

ORA converts continuous measures into binary (significant/not), losing information. When in doubt, run both ORA and GSEA and compare.

## Prerequisites

```r
# Install if missing
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")

packages <- c("clusterProfiler", "org.Hs.eg.db", "enrichplot", "GOplot", "openxlsx", "ggplot2", "dplyr")
for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    if (pkg %in% c("clusterProfiler", "org.Hs.eg.db", "enrichplot", "GOplot")) {
      BiocManager::install(pkg)
    } else {
      install.packages(pkg)
    }
  }
}
```

## Step 1: Prepare Gene List

**Goal:** Convert your DEG results into a character vector of gene IDs suitable for enrichment.

**Approach:** Read the DEG table and extract the gene identifiers from row names or a gene column.

```r
library(clusterProfiler)
library(org.Hs.eg.db)
library(enrichplot)
library(GOplot)
library(openxlsx)
library(ggplot2)
library(dplyr)
options(stringsAsFactors = FALSE)

# Read DEG list — adjust file path to your actual data
gene_list <- rownames(read.csv("data/DEG.csv"))
# Or if gene symbols are in a column:
# gene_list <- read.csv("data/DEG.csv")$gene_symbol |> unique()

# For clusterProfiler, convert IDs if needed
# From SYMBOL to ENTREZID:
gene_ids <- bitr(gene_list, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
gene_entrez <- gene_ids$ENTREZID

# Multiple output types
gene_ids_multi <- bitr(gene_list, fromType = 'SYMBOL', toType = c('ENTREZID', 'ENSEMBL'), OrgDb = org.Hs.eg.db)
```

**Key point:** `enrichGO` accepts SYMBOL, ENTREZID, ENSEMBL, etc. The `keyType` parameter must match your input. For mouse, use `org.Mm.eg.db` instead of `org.Hs.eg.db`.

### ID Conversion with bitr

Check available key types:
```r
keytypes(org.Hs.eg.db)
```

**Pitfalls:**
- **Many-to-many mappings**: one Ensembl gene can map to multiple Entrez IDs. Deduplicate after `bitr()` to avoid counting genes multiple times.
- **Lost genes**: if > 15% of genes fail to convert, results may be unreliable. Always report the conversion rate.
- **Best practice**: use the same ID type throughout the pipeline. Convert at the last step if possible.

## Step 2: GO Enrichment Analysis

### 2.1 Background Universe (Critical)

**Goal:** Improve enrichment specificity by restricting the background to genes actually tested in the experiment.

**Approach:** Pass all expressed genes (not just significant ones) as the universe parameter to enrichGO.

The background must be genes that *could have* appeared in the list. Getting this wrong is the single most common ORA error. Using the whole genome (~20,000 genes) when only 12,000 were expressed inflates significance for tissue-specific pathways.

| Experiment Type | Correct Background |
|----------------|-------------------|
| RNA-seq | All genes with detectable expression (e.g., > 1 CPM in >= N samples) |
| Microarray | All probes on the array (mapped to genes) |
| Proteomics | All detected proteins |
| Targeted panel | Only genes on the panel |

```r
# Background = all genes that were tested (NOT the full genome)
# For DESeq2: genes with non-NA pvalue survived independent filtering
all_tested <- de_results$gene_id[!is.na(de_results$pvalue)]
universe_ids <- bitr(all_tested, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)

ego <- enrichGO(
    gene = gene_list,
    universe = universe_ids$ENTREZID,
    OrgDb = org.Hs.eg.db,
    keyType = 'ENTREZID',
    ont = 'BP',
    pAdjustMethod = 'BH',
    pvalueCutoff = 0.05
)
```

**Warning:** clusterProfiler silently drops unannotated genes from the background. To prevent this: `options(enrichment_force_universe = TRUE)` before running enrichGO.

### 2.2 Run enrichGO

**Goal:** Test for over-representation of GO terms across all three ontologies (BP, CC, MF) simultaneously.

**Approach:** Use `ont = "all"` to get all three ontologies in one call. Set `pvalueCutoff = 1` to defer filtering.

```r
GO <- enrichGO(
  gene        = gene_list,
  OrgDb       = "org.Hs.eg.db",
  keyType     = "SYMBOL",        # Match your gene ID type
  pAdjustMethod = "BH",
  pvalueCutoff  = 1,             # Defer filtering
  minGSSize    = 5,              # Minimum genes per term
  ont          = "all",          # BP + CC + MF
  readable     = TRUE
)

GO_result <- GO@result
go <- as.data.frame(GO_result)
rownames(go) <- 1:nrow(go)
```

### 2.3 Filter and Sort

**Goal:** Retain only statistically significant terms with sufficient gene counts, then sort by enrichment strength.

```r
go <- go[go$p.adjust < 0.05, ]
go <- go[go$Count > 1, ]
go <- go[order(go$Count, decreasing = TRUE), ]

# Quick summary
dim(go)           # How many significant terms?
table(go$ONTOLOGY) # BP, CC, MF counts

# Save full results
write.xlsx(go, file = "01.GO.xlsx")
```

### 2.4 Extract Top 8 per Ontology for Plotting

**Goal:** Select the most gene-rich terms from each ontology to keep visualizations readable.

```r
go_res <- go

Go_bp <- go_res[go_res$ONTOLOGY == "BP", ] |> arrange(desc(Count)) |> slice_head(n = 8)
Go_cc <- go_res[go_res$ONTOLOGY == "CC", ] |> arrange(desc(Count)) |> slice_head(n = 8)
Go_mf <- go_res[go_res$ONTOLOGY == "MF", ] |> arrange(desc(Count)) |> slice_head(n = 8)

go_res2 <- rbind(Go_bp, Go_cc, Go_mf)
```

### 2.5 GO Visualization — Style 1: Labeled Bar Plot

**Goal:** Create a bar chart where pathway names are placed directly on the bars, avoiding cluttered y-axis labels. Ideal for presentations with long pathway names.

**Approach:** Use `geom_text` with `hjust = 0` to place labels at a fixed x-offset, and hide the y-axis text.

```r
go_res2 <- go_res2 %>%
  mutate(
    ONTOLOGY    = factor(ONTOLOGY, levels = c("BP", "CC", "MF")),
    Description = factor(Description, levels = rev(Description[order(ONTOLOGY, -Count)]))
  ) %>%
  arrange(ONTOLOGY, -Count)

ontology_colors <- c("BP" = "#e4945b", "CC" = "#b7a8cf", "MF" = "#5a91c8")

ggplot(go_res2, aes(x = Count, y = Description, fill = ONTOLOGY)) +
  geom_bar(stat = "identity", width = 0.7) +
  geom_text(aes(label = Description, x = 0.1),
            hjust = 0, color = "black", size = 4.3) +
  scale_fill_manual(values = ontology_colors) +
  labs(
    title = "GO Enrichment Analysis Results",
    x     = "Count (Number of Genes)",
    y     = "",
    fill  = "Ontology"
  ) +
  theme_minimal() +
  theme(
    plot.title          = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.text.y         = element_blank(),
    axis.ticks.y        = element_blank(),
    panel.grid.major.y  = element_blank(),
    legend.position     = "right"
  ) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15)))

ggsave("02.GO_enrichment_barplot.pdf", width = 8, height = 8)
```

### 2.6 GO Visualization — Style 2: Faceted Significance Plot

**Goal:** Show enrichment significance (-log10 p.adjust) with gene counts annotated, faceted by ontology. This style emphasizes statistical strength and allows direct comparison across ontologies.

**Approach:** Compute -log10(p.adjust), facet by ONTOLOGY, and annotate bars with Count values.

```r
go_res2$neg_log10_p <- -log10(go_res2$p.adjust)
go_res2 <- go_res2[order(go_res2$ONTOLOGY, go_res2$neg_log10_p, decreasing = FALSE), ]
go_res2$Description <- factor(go_res2$Description, levels = unique(go_res2$Description))

p <- ggplot(go_res2, aes(x = neg_log10_p, y = Description, fill = p.adjust)) +
  geom_col(width = 0.7) +
  geom_text(aes(label = Count), hjust = -0.2, size = 3.5, color = "black") +
  geom_vline(xintercept = -log10(0.05), linetype = "dashed", color = "#10467f", linewidth = 0.8) +
  scale_fill_gradient(low = "#b02013", high = "lightblue", name = "p.adjust") +
  labs(
    x     = expression(-log[10](p.adjust)),
    y     = "Pathway",
    title = "GO Enrichment Analysis Results"
  ) +
  facet_wrap(~ ONTOLOGY, scales = "free_y", ncol = 1) +
  theme_bw() +
  theme(
    axis.text           = element_text(color = "black", size = 10),
    panel.grid.major.y  = element_blank(),
    strip.background    = element_rect(fill = "#f0f0f0"),
    strip.text          = element_text(face = "bold")
  ) +
  scale_x_continuous(expand = expansion(mult = c(0.01, 0.1)))

ggsave("02.GO_plot.pdf", p, width = 8, height = 5.5)
print(p)
```

**Outputs from Step 2:**
| File | Content |
|---|---|
| `01.GO.xlsx` | Full GO enrichment table (all significant terms) |
| `02.GO_enrichment_barplot.pdf` | Labeled bar plot — best for showing pathway names |
| `02.GO_plot.pdf` | Faceted significance plot — best for comparing statistical strength |

### 2.7 Simplify Redundant GO Terms

**Goal:** Remove highly similar GO terms to reduce redundancy in enrichment results.

**Approach:** Cluster GO terms by semantic similarity and retain representative terms using the simplify function.

GO terms form a DAG (directed acyclic graph), not a flat list. If "mitotic cell cycle" is enriched, parent terms ("cell cycle", "cell cycle process") will also be enriched because they contain supersets of the same genes. Always simplify before interpretation.

```r
# Remove redundant GO terms (keeps representative terms)
ego_simplified <- simplify(ego, cutoff = 0.7, by = 'p.adjust', select_fun = min)

# measure options: 'Wang' (default, graph-based, stable across releases),
# 'Resnik', 'Lin', 'Jiang', 'Rel' (IC-based, depend on annotation version)
ego_simplified <- simplify(ego, cutoff = 0.7, measure = 'Wang')
```

**Limitations:** `simplify()` does NOT work with `ont='ALL'` -- run BP, MF, CC separately. Cutoff 0.7 is a reasonable default; lower retains more terms, higher is more aggressive.

### 2.8 Group GO Terms by Ancestor

**Goal:** Classify genes by broad GO slim categories for a high-level functional overview.

**Approach:** Use groupGO to assign genes to GO terms at a specific hierarchy level.

```r
# Classify genes by GO slim categories
ggo <- groupGO(
    gene = gene_list,
    OrgDb = org.Hs.eg.db,
    ont = 'BP',
    level = 3,  # GO hierarchy level
    readable = TRUE
)
```

### 2.9 RNA-seq Gene Length Bias (GOseq)

In RNA-seq, longer transcripts produce more fragments, increasing statistical power to detect DE. This systematically biases ORA toward pathways enriched in long genes (extracellular matrix, cell adhesion) and against short-gene pathways (ribosomal, mitochondrial). Standard normalization (RPKM, TMM) does NOT fix this.

For length-corrected GO enrichment, use GOseq:
```r
library(goseq)
pwf <- nullp(de_vector, 'hg38', 'ensGene', bias.data = gene_lengths)
goseq_results <- goseq(pwf, 'hg38', 'ensGene', method = 'Wallenius')
```

### 2.10 Make Results Readable

```r
# Convert Entrez IDs to gene symbols in results
ego_readable <- setReadable(ego, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')

# Or use readable = TRUE directly (only works with ENTREZID input)
ego <- enrichGO(
    gene = gene_list,
    OrgDb = org.Hs.eg.db,
    keyType = 'ENTREZID',
    ont = 'BP',
    readable = TRUE  # Converts to symbols
)
```

### 2.11 Different Organisms

```r
# Mouse
library(org.Mm.eg.db)
ego_mouse <- enrichGO(gene = genes, OrgDb = org.Mm.eg.db, ont = 'BP')

# Zebrafish
library(org.Dr.eg.db)
ego_zfish <- enrichGO(gene = genes, OrgDb = org.Dr.eg.db, ont = 'BP')

# Yeast
library(org.Sc.sgd.db)
ego_yeast <- enrichGO(gene = genes, OrgDb = org.Sc.sgd.db, ont = 'BP', keyType = 'ORF')

# Rat
library(org.Rn.eg.db)
ego_rat <- enrichGO(gene = genes, OrgDb = org.Rn.eg.db, ont = 'BP')
```

### 2.12 Key Parameters Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| gene | required | Vector of gene IDs |
| OrgDb | required | Organism database |
| keyType | ENTREZID | Input ID type |
| ont | BP | BP, MF, CC, or ALL |
| pvalueCutoff | 0.05 | P-value threshold |
| qvalueCutoff | 0.2 | Q-value (FDR) threshold |
| pAdjustMethod | BH | BH, bonferroni, etc. |
| universe | NULL | Background genes |
| minGSSize | 10 | Min genes per term |
| maxGSSize | 500 | Max genes per term |
| readable | FALSE | Convert to symbols |

### 2.13 Interpreting Results

Always examine effect size alongside p-values. A pathway with 500 genes can achieve p < 1e-15 with a modest 1.2x fold enrichment, while a 10-gene pathway with 4x enrichment at p = 0.01 is biologically more interesting.

- **Fold enrichment** = GeneRatio / BgRatio. Values > 2 suggest strong enrichment.
- **Count**: number of query genes in the term. Very large counts (> 50) may indicate overly broad terms.
- `minGSSize=10, maxGSSize=500` filters out uninformative extremes.

## Step 3: KEGG Pathway Enrichment

### 3.1 ID Conversion (SYMBOL → ENTREZID)

**Goal:** Convert gene symbols to Entrez IDs, because `enrichKEGG` requires NCBI Entrez Gene IDs.

```r
gene_transform <- bitr(
  gene_list,
  fromType = "SYMBOL",
  toType   = c("ENTREZID", "ENSEMBL"),
  OrgDb    = "org.Hs.eg.db"
)
```

> **Note:** `bitr` drops genes without a match. Check `nrow(gene_transform)` vs `length(gene_list)` — expect some loss. If loss > 30%, verify your `fromType` matches the actual ID format.

### 3.2 Run enrichKEGG

```r
kk <- enrichKEGG(
  gene          = gene_transform$ENTREZID,
  organism      = "hsa",          # Human; use "mmu" for mouse, "rno" for rat
  keyType       = "kegg",
  pvalueCutoff   = 0.05,
  qvalueCutoff   = 1
)

# Convert ENTREZID back to SYMBOL for readability
kk <- setReadable(kk, OrgDb = "org.Hs.eg.db", keyType = "ENTREZID")
```

### 3.3 Filter, Sort, and Save

```r
kegg_result <- kk@result
hh <- as.data.frame(kegg_result)
rownames(hh) <- 1:nrow(hh)

hh <- hh[hh$p.adjust < 0.05, ]
hh <- hh[hh$Count > 1, ]
hh <- hh[order(hh$Count, decreasing = TRUE), ]

dim(hh)  # How many significant KEGG pathways?

write.xlsx(hh, file = "03.KEGG.xlsx")
```

### 3.4 KEGG Visualization — Style 1: Category-Colored Bar Plot

**Goal:** Display the top 25 KEGG pathways with pathway names on bars, colored by KEGG category.

**Approach:** KEGG classifies pathways into broad categories (Metabolism, Human Diseases, Environmental Information Processing, etc.). Use these categories for fill color.

```r
# Select top 25 by Count
kk_df <- hh[1:min(25, nrow(hh)), ]

# KEGG category colors — adjust based on actual categories present
kegg_category_colors <- c(
  "Environmental Information Processing" = "#e4945b",
  "Human Diseases"                       = "#5a91c8",
  "Genetic Information Processing"       = "#9ad7cc",
  "Organismal Systems"                   = "#d7d067",
  "Cellular Processes"                   = "#fdbca9",
  "Metabolism"                           = "#96b99b",
  "other"                                = "#7f7f7f"
)

kk_df <- kk_df[order(kk_df$Count), ]
kk_df$Description <- factor(kk_df$Description, levels = unique(kk_df$Description))

ggplot(kk_df, aes(x = Count, y = Description, fill = category)) +
  geom_bar(stat = "identity", width = 0.7) +
  geom_text(aes(label = Description, x = 0.1),
            hjust = 0, color = "black", size = 4.3) +
  scale_fill_manual(values = kegg_category_colors) +
  labs(
    title = "KEGG Enrichment Analysis Results",
    x     = "Count (Number of Genes)",
    y     = "",
    fill  = "Category"
  ) +
  theme_minimal() +
  theme(
    axis.text.y        = element_blank(),
    axis.ticks.y       = element_blank(),
    panel.grid.major.y = element_blank()
  ) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15)))

ggsave("04.KEGG_barplot.pdf", width = 9, height = 8)
```

### 3.5 KEGG Visualization — Style 2: Significance Bar Plot

**Goal:** Rank pathways by -log10(p.adjust) to emphasize statistical significance.

```r
hh$neg_log10_p <- -log10(hh$p.adjust)
hh <- hh[order(hh$neg_log10_p, decreasing = FALSE), ]
hh$Description <- factor(hh$Description, levels = hh$Description)

p_kegg <- ggplot(hh, aes(x = neg_log10_p, y = Description, fill = p.adjust)) +
  geom_col(width = 0.7) +
  geom_text(aes(label = Count), hjust = -0.2, size = 3.5, color = "black") +
  geom_vline(xintercept = -log10(0.05), linetype = "dashed", color = "#10467f", linewidth = 0.8) +
  scale_fill_gradient(low = "#b02013", high = "lightblue", name = "p.adjust") +
  labs(
    x     = expression(-log[10](p.adjust)),
    y     = "Pathway",
    title = "KEGG Enrichment Analysis Results"
  ) +
  theme_bw() +
  theme(
    axis.text          = element_text(color = "black", size = 10),
    panel.grid.major.y = element_blank()
  ) +
  scale_x_continuous(expand = expansion(mult = c(0.01, 0.1)))

ggsave("05.KEGG_plot.pdf", p_kegg, width = 8, height = 5)
print(p_kegg)
```

**Outputs from Step 3:**
| File | Content |
|---|---|
| `03.KEGG.xlsx` | Full KEGG enrichment table |
| `04.KEGG_barplot.pdf` | Category-colored bar plot |
| `05.KEGG_plot.pdf` | Significance-ranked bar plot |

## Step 4: Result Interpretation

### GO Results — What to Look For

| Ontology | If enriched in... | What it suggests |
|---|---|---|
| **BP** | Inflammatory response, chemotaxis, cytokine production | Immune or inflammatory processes are activated |
| **BP** | Cell cycle, DNA replication, mitosis | Cell proliferation is altered |
| **BP** | Apoptosis, programmed cell death | Cell death pathways are active |
| **CC** | Extracellular matrix, secretory vesicles | Gene products are secreted or remodeling the ECM |
| **CC** | Mitochondrion, respiratory chain | Energy metabolism is affected |
| **CC** | Nucleus, nucleolus, chromatin | Transcriptional regulation is involved |
| **MF** | Receptor binding, growth factor activity | Cell signaling is modulated |
| **MF** | Calcium ion binding, metal ion binding | Ion signaling or transport changes |
| **MF** | ATP binding, kinase activity | Phosphorylation cascades are involved |

**Practical tips:**
- If BP terms number in the hundreds, apply a stricter `p.adjust` threshold (e.g., 0.01) or focus on the top 20 by Count
- Overly general terms (e.g., "cell process", "biological regulation") are less informative — filter by `Count > 10` to focus on specific terms
- Check whether BP, CC, and MF results tell a coherent story — e.g., "inflammatory response" (BP) + "secretory granule" (CC) + "cytokine receptor binding" (MF) is internally consistent

### KEGG Results — What to Look For

- **Classic signaling pathways** (PI3K-Akt, MAPK, NF-kB, JAK-STAT): Indicate specific signaling cascades are altered
- **Metabolic pathways** (Glycolysis, Oxidative phosphorylation, Fatty acid metabolism): Suggest metabolic reprogramming
- **Disease pathways** (Pathways in cancer, Alzheimer disease): These are broad compilations — drill into specific sub-pathways for mechanistic insight
- **"Pathways in cancer"**: Don't panic — this is a summary pathway. Check which specific oncogenic/tumor-suppressor sub-pathways are enriched

### Integration

Cross-reference GO and KEGG results: if GO BP shows "inflammatory response" and KEGG shows "NF-kappa B signaling pathway" and "TNF signaling pathway", these reinforce each other — NF-kB is a master regulator of inflammation.

## Common Organism Codes for KEGG

| Organism | KEGG code | OrgDb package |
|---|---|---|
| Human | `hsa` | `org.Hs.eg.db` |
| Mouse | `mmu` | `org.Mm.eg.db` |
| Rat | `rno` | `org.Rn.eg.db` |
| Zebrafish | `dre` | `org.Dr.eg.db` |
| Fruit fly | `dme` | `org.Dm.eg.db` |
| C. elegans | `cel` | `org.Ce.eg.db` |
| Yeast (S. cerevisiae) | `sce` | `org.Sc.sgd.db` |
| Arabidopsis | `ath` | `org.At.tair.db` |

## Common Errors and Solutions

### No significant GO/KEGG terms found

**Causes and fixes:**
1. **Too few DEGs (< 50)**: ORA loses power with small gene sets. Try relaxing `pvalueCutoff = 0.1`, or use GSEA instead
2. **Threshold too strict**: Set `pvalueCutoff = 0.1` for discovery, then filter post-hoc
3. **Wrong gene ID type**: Verify `keyType` matches your input. Use `head(gene_list)` to inspect the actual ID format
4. **Background too small**: `enrichGO` uses all genes in the OrgDb as background. If your platform only measures a subset, use `universe` parameter

### Subscript out of bounds / missing ONTOLOGY column

If `go_res$ONTOLOGY` doesn't exist, your `ont` parameter may have been set to a single ontology (e.g., `"BP"`). Set `ont = "all"` or adjust the filtering code accordingly.

### Chinese character rendering issues in PDF

Add to `theme()`: `text = element_text(family = "Arial")`, or use the `showtext` package to load a Chinese font:

```r
library(showtext)
showtext_auto()
font_add("SimHei", "SimHei.ttf")  # or your system's Chinese font
```

### bitr drops too many genes

**Checklist:**
1. Is `fromType` correct? (SYMBOL vs ENSEMBL vs ENTREZID)
2. Are the gene names current? Some symbols change over time — try `bitr(..., fromType = "ALIAS")` as a fallback
3. For non-model organisms, check if the OrgDb package has good coverage

### KEGG API connection errors

The `enrichKEGG` function queries the KEGG web API. If it fails:
1. Check internet connectivity
2. KEGG servers occasionally have outages — retry after a few minutes
3. As a fallback, download KEGG gene sets locally and use `enricher()` instead

## Visual Style Decision Guide

| Goal | Use Style | Rationale |
|---|---|---|
| Presentation with long pathway names | Labeled Bar Plot (Style 1) | Labels on bars save horizontal space |
| Comparing statistical significance | Faceted Significance Plot (Style 2) | -log10(p.adjust) directly visualizes strength of evidence |
| Showing KEGG category context | Category-Colored Bar Plot | Category colors add functional grouping |
| Manuscript figure | Significance Plot (Style 2) | Shows both significance and gene count; more information-dense |
| Quick exploration | Bar Plot (Style 1) | Faster to read pathway names at a glance |

## Related Skills

- `bio-pathway-analysis-kegg-pathways` — Core KEGG patterns, KEGG ID conversion, organism codes
- `bio-pathway-analysis-gsea` — Gene Set Enrichment Analysis for ranked gene lists
- `bio-pathway-analysis-enrichment-visualization` — Enrichment-specific plots (dotplot, cnetplot, emapplot, treeplot)
- `bio-pathway-analysis-reactome-pathways` — Reactome pathway enrichment alternative
- `bio-pathway-analysis-wikipathways` — WikiPathways enrichment alternative
- `data-visualization-ggplot2-fundamentals` — ggplot2 customization and theming
- `bio-data-visualization-specialized-omics-plots` — Volcano plots, heatmaps, and other omics-specific figures
