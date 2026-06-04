# GO & KEGG Combined Enrichment Analysis — Full Workflow
# Reference: clusterProfiler 4.10+ | Verify API if version differs
#
# This script runs the complete GO + KEGG enrichment pipeline
# from a DEG list to publication-ready figures.

# ---- Setup ----
library(clusterProfiler)
library(org.Hs.eg.db)
library(enrichplot)
library(openxlsx)
library(ggplot2)
library(dplyr)
options(stringsAsFactors = FALSE)

# ============================================================
# Configuration — adjust these to your data
# ============================================================

DEG_FILE   <- "data/DEG.csv"    # Path to your DEG results
ORG_DB     <- "org.Hs.eg.db"    # Organism annotation DB
KEGG_CODE  <- "hsa"             # KEGG organism code (hsa=human, mmu=mouse, rno=rat)
KEY_TYPE   <- "SYMBOL"          # Gene ID type in your DEG file
PADJ_CUT   <- 0.05              # Adjusted p-value cutoff
TOP_N      <- 8                 # Number of top terms per ontology to plot
KEGG_TOP_N <- 25                # Number of top KEGG pathways to plot

# ============================================================
# 1. Load and Prepare Gene List
# ============================================================

cat("===== Loading gene list =====\n")

if (file.exists(DEG_FILE)) {
  # If DEG file exists, read from it
  deg_data <- read.csv(DEG_FILE)
  # Try row names first, then common column names
  if (!is.null(rownames(deg_data)) && !all(grepl("^[0-9]+$", rownames(deg_data)))) {
    gene_list <- rownames(deg_data)
  } else if ("SYMBOL" %in% colnames(deg_data)) {
    gene_list <- unique(deg_data$SYMBOL)
  } else if ("gene_symbol" %in% colnames(deg_data)) {
    gene_list <- unique(deg_data$gene_symbol)
  } else if ("gene" %in% colnames(deg_data)) {
    gene_list <- unique(deg_data$gene)
  } else if (ncol(deg_data) >= 1) {
    gene_list <- unique(deg_data[, 1])
  } else {
    stop("Cannot identify gene symbols in DEG file. Please specify the gene column.")
  }
} else {
  # Fallback: generate mock data for demonstration
  cat(sprintf("WARNING: DEG file '%s' not found. Using mock data.\n", DEG_FILE))
  set.seed(42)
  all_genes <- keys(org.Hs.eg.db, keytype = "SYMBOL")
  gene_list <- sample(all_genes, 500)
}

cat(sprintf("Gene list loaded: %d genes\n", length(gene_list)))

# ============================================================
# 2. GO Enrichment Analysis
# ============================================================

cat("\n===== GO Enrichment Analysis =====\n")

GO <- enrichGO(
  gene          = gene_list,
  OrgDb         = ORG_DB,
  keyType       = KEY_TYPE,
  pAdjustMethod = "BH",
  pvalueCutoff  = 1,
  minGSSize     = 5,
  ont           = "all",
  readable      = TRUE
)

go <- as.data.frame(GO@result)
rownames(go) <- 1:nrow(go)
cat(sprintf("Raw GO terms: %d\n", nrow(go)))

# Filter
go <- go[go$p.adjust < PADJ_CUT, ]
go <- go[go$Count > 1, ]
go <- go[order(go$Count, decreasing = TRUE), ]

cat(sprintf("Significant GO terms: %d\n", nrow(go)))
cat("Ontology breakdown:\n")
print(table(go$ONTOLOGY))

write.xlsx(go, file = "01.GO.xlsx")

# ============================================================
# 3. GO Visualization
# ============================================================

cat("\n===== GO Visualization =====\n")

# Extract top N per ontology
go_bp <- go[go$ONTOLOGY == "BP", ] |> arrange(desc(Count)) |> head(TOP_N)
go_cc <- go[go$ONTOLOGY == "CC", ] |> arrange(desc(Count)) |> head(TOP_N)
go_mf <- go[go$ONTOLOGY == "MF", ] |> arrange(desc(Count)) |> head(TOP_N)
go_plot <- rbind(go_bp, go_cc, go_mf)

n_bp <- nrow(go_bp)
n_cc <- nrow(go_cc)
n_mf <- nrow(go_mf)
cat(sprintf("Plotting: BP=%d, CC=%d, MF=%d terms\n", n_bp, n_cc, n_mf))

if (nrow(go_plot) > 0) {

  # Style 1: Labeled bar plot
  go_plot <- go_plot %>%
    mutate(
      ONTOLOGY    = factor(ONTOLOGY, levels = c("BP", "CC", "MF")),
      Description = factor(Description, levels = rev(Description[order(ONTOLOGY, -Count)]))
    ) %>%
    arrange(ONTOLOGY, -Count)

  ontology_colors <- c("BP" = "#e4945b", "CC" = "#b7a8cf", "MF" = "#5a91c8")

  p_go1 <- ggplot(go_plot, aes(x = Count, y = Description, fill = ONTOLOGY)) +
    geom_bar(stat = "identity", width = 0.7) +
    geom_text(aes(label = Description, x = 0.1),
              hjust = 0, color = "black", size = 4.3) +
    scale_fill_manual(values = ontology_colors) +
    labs(title = "GO Enrichment Analysis Results",
         x = "Count (Number of Genes)", y = "", fill = "Ontology") +
    theme_minimal() +
    theme(
      plot.title         = element_text(hjust = 0.5, size = 16, face = "bold"),
      axis.text.y        = element_blank(),
      axis.ticks.y       = element_blank(),
      panel.grid.major.y = element_blank(),
      legend.position    = "right"
    ) +
    scale_x_continuous(expand = expansion(mult = c(0, 0.15)))
  ggsave("02.GO_enrichment_barplot.pdf", p_go1, width = 8, height = 8)

  # Style 2: Faceted significance plot
  go_plot$neg_log10_p <- -log10(go_plot$p.adjust)
  go_plot <- go_plot[order(go_plot$ONTOLOGY, go_plot$neg_log10_p, decreasing = FALSE), ]
  go_plot$Description <- factor(go_plot$Description, levels = unique(go_plot$Description))

  p_go2 <- ggplot(go_plot, aes(x = neg_log10_p, y = Description, fill = p.adjust)) +
    geom_col(width = 0.7) +
    geom_text(aes(label = Count), hjust = -0.2, size = 3.5, color = "black") +
    geom_vline(xintercept = -log10(0.05), linetype = "dashed", color = "#10467f", linewidth = 0.8) +
    scale_fill_gradient(low = "#b02013", high = "lightblue", name = "p.adjust") +
    labs(x = expression(-log[10](p.adjust)), y = "Pathway",
         title = "GO Enrichment Analysis Results") +
    facet_wrap(~ ONTOLOGY, scales = "free_y", ncol = 1) +
    theme_bw() +
    theme(
      axis.text           = element_text(color = "black", size = 10),
      panel.grid.major.y  = element_blank(),
      strip.background    = element_rect(fill = "#f0f0f0"),
      strip.text          = element_text(face = "bold")
    ) +
    scale_x_continuous(expand = expansion(mult = c(0.01, 0.1)))
  ggsave("02.GO_plot.pdf", p_go2, width = 8, height = 5.5)

  cat("Saved: 01.GO.xlsx, 02.GO_enrichment_barplot.pdf, 02.GO_plot.pdf\n")
} else {
  cat("WARNING: No significant GO terms to plot. Try relaxing p.adjust cutoff.\n")
}

# ============================================================
# 4. KEGG Pathway Enrichment
# ============================================================

cat("\n===== KEGG Pathway Enrichment =====\n")

# ID conversion
gene_transform <- bitr(
  gene_list,
  fromType = KEY_TYPE,
  toType   = c("ENTREZID", "ENSEMBL"),
  OrgDb    = ORG_DB
)
cat(sprintf("ID mapping: %d / %d genes mapped (%.1f%%)\n",
            nrow(gene_transform), length(gene_list),
            100 * nrow(gene_transform) / length(gene_list)))

# KEGG enrichment
kk <- enrichKEGG(
  gene         = gene_transform$ENTREZID,
  organism     = KEGG_CODE,
  keyType      = "kegg",
  pvalueCutoff  = 0.05,
  qvalueCutoff  = 1
)
kk <- setReadable(kk, OrgDb = ORG_DB, keyType = "ENTREZID")

hh <- as.data.frame(kk@result)
rownames(hh) <- 1:nrow(hh)

hh <- hh[hh$p.adjust < PADJ_CUT, ]
hh <- hh[hh$Count > 1, ]
hh <- hh[order(hh$Count, decreasing = TRUE), ]

cat(sprintf("Significant KEGG pathways: %d\n", nrow(hh)))
if (nrow(hh) > 0) {
  cat("Top pathways:\n")
  print(head(hh[, c("Description", "Count", "p.adjust", "category")],
             min(10, nrow(hh))))
}

write.xlsx(hh, file = "03.KEGG.xlsx")

# ============================================================
# 5. KEGG Visualization
# ============================================================

cat("\n===== KEGG Visualization =====\n")

if (nrow(hh) > 0) {

  # Style 1: Category-colored bar plot
  kk_plot <- hh[1:min(KEGG_TOP_N, nrow(hh)), ]

  kegg_colors <- c(
    "Environmental Information Processing" = "#e4945b",
    "Human Diseases"                       = "#5a91c8",
    "Genetic Information Processing"       = "#9ad7cc",
    "Organismal Systems"                   = "#d7d067",
    "Cellular Processes"                   = "#fdbca9",
    "Metabolism"                           = "#96b99b",
    "other"                                = "#7f7f7f"
  )

  kk_plot <- kk_plot[order(kk_plot$Count), ]
  kk_plot$Description <- factor(kk_plot$Description, levels = unique(kk_plot$Description))

  p_kegg1 <- ggplot(kk_plot, aes(x = Count, y = Description, fill = category)) +
    geom_bar(stat = "identity", width = 0.7) +
    geom_text(aes(label = Description, x = 0.1),
              hjust = 0, color = "black", size = 4.3) +
    scale_fill_manual(values = kegg_colors) +
    labs(title = "KEGG Enrichment Analysis Results",
         x = "Count (Number of Genes)", y = "", fill = "Category") +
    theme_minimal() +
    theme(
      axis.text.y        = element_blank(),
      axis.ticks.y       = element_blank(),
      panel.grid.major.y = element_blank()
    ) +
    scale_x_continuous(expand = expansion(mult = c(0, 0.15)))
  ggsave("04.KEGG_barplot.pdf", p_kegg1, width = 9, height = 8)

  # Style 2: Significance bar plot
  hh$neg_log10_p <- -log10(hh$p.adjust)
  hh <- hh[order(hh$neg_log10_p, decreasing = FALSE), ]
  hh$Description <- factor(hh$Description, levels = hh$Description)

  p_kegg2 <- ggplot(hh, aes(x = neg_log10_p, y = Description, fill = p.adjust)) +
    geom_col(width = 0.7) +
    geom_text(aes(label = Count), hjust = -0.2, size = 3.5, color = "black") +
    geom_vline(xintercept = -log10(0.05), linetype = "dashed", color = "#10467f", linewidth = 0.8) +
    scale_fill_gradient(low = "#b02013", high = "lightblue", name = "p.adjust") +
    labs(x = expression(-log[10](p.adjust)), y = "Pathway",
         title = "KEGG Enrichment Analysis Results") +
    theme_bw() +
    theme(
      axis.text          = element_text(color = "black", size = 10),
      panel.grid.major.y = element_blank()
    ) +
    scale_x_continuous(expand = expansion(mult = c(0.01, 0.1)))
  ggsave("05.KEGG_plot.pdf", p_kegg2, width = 8, height = 5)

  cat("Saved: 03.KEGG.xlsx, 04.KEGG_barplot.pdf, 05.KEGG_plot.pdf\n")
} else {
  cat("WARNING: No significant KEGG pathways to plot.\n")
  cat("Suggestions:\n")
  cat("  1. Relax pvalueCutoff (e.g., 0.1)\n")
  cat("  2. Check gene ID mapping accuracy\n")
  cat("  3. For <50 DEGs, consider GSEA instead\n")
}

# ============================================================
# 6. Summary
# ============================================================

cat("\n===== Enrichment Analysis Complete =====\n")
cat(sprintf("  GO terms:    %d significant\n", nrow(go)))
cat(sprintf("  KEGG pathways: %d significant\n", nrow(hh)))
cat("\nOutput files:\n")
cat("  01.GO.xlsx                    - Full GO results\n")
cat("  02.GO_enrichment_barplot.pdf  - GO labeled bar plot\n")
cat("  02.GO_plot.pdf                - GO faceted significance plot\n")
cat("  03.KEGG.xlsx                  - Full KEGG results\n")
cat("  04.KEGG_barplot.pdf           - KEGG category bar plot\n")
cat("  05.KEGG_plot.pdf              - KEGG significance bar plot\n")
