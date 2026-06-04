# KEGG Pathway Enrichment Analysis — Complete Example
# Reference: clusterProfiler 4.10+ | Verify API if version differs
#
# This script performs KEGG pathway enrichment on a DEG list
# and produces two visualization styles.

# ---- Setup ----
library(clusterProfiler)
library(org.Hs.eg.db)
library(enrichplot)
library(openxlsx)
library(ggplot2)
library(dplyr)
options(stringsAsFactors = FALSE)

# ---- Step 1: Prepare gene list ----
# Replace with your actual DEG file path
# gene_list <- rownames(read.csv("data/DEG.csv"))

# Example: generate a mock gene list for demonstration
set.seed(123)
all_genes <- keys(org.Hs.eg.db, keytype = "SYMBOL")
gene_list <- sample(all_genes, 500)
cat(sprintf("Input: %d significant genes (SYMBOL)\n", length(gene_list)))

# ---- Step 2: ID conversion (SYMBOL -> ENTREZID) ----
gene_transform <- bitr(
  gene_list,
  fromType = "SYMBOL",
  toType   = c("ENTREZID", "ENSEMBL"),
  OrgDb    = "org.Hs.eg.db"
)
cat(sprintf("Genes mapped: %d / %d (%.1f%%)\n",
            nrow(gene_transform), length(gene_list),
            100 * nrow(gene_transform) / length(gene_list)))

# ---- Step 3: Run KEGG enrichment ----
kk <- enrichKEGG(
  gene         = gene_transform$ENTREZID,
  organism     = "hsa",       # Human
  keyType      = "kegg",
  pvalueCutoff  = 0.05,
  qvalueCutoff  = 1
)

# Convert ENTREZID back to SYMBOL for readability
kk <- setReadable(kk, OrgDb = "org.Hs.eg.db", keyType = "ENTREZID")

# ---- Step 4: Filter, sort, and save ----
kegg_result <- kk@result
hh <- as.data.frame(kegg_result)
rownames(hh) <- 1:nrow(hh)

hh <- hh[hh$p.adjust < 0.05, ]
hh <- hh[hh$Count > 1, ]
hh <- hh[order(hh$Count, decreasing = TRUE), ]

cat(sprintf("\nSignificant KEGG pathways (padj<0.05, Count>1): %d\n", nrow(hh)))
if (nrow(hh) > 0) {
  cat("\nTop 10 pathways:\n")
  print(head(hh[, c("Description", "Count", "p.adjust", "category")], 10))
}

write.xlsx(hh, file = "03.KEGG.xlsx")
cat("\nSaved: 03.KEGG.xlsx\n")

# Only proceed with plotting if there are significant results
if (nrow(hh) == 0) {
  cat("\nWARNING: No significant KEGG pathways found. Try:\n")
  cat("  - Relaxing pvalueCutoff to 0.1\n")
  cat("  - Checking that gene IDs were correctly mapped\n")
  cat("  - Using GSEA instead of ORA for small gene lists\n")
  quit(save = "no", status = 0)
}

# ---- Style 1: Category-Colored Bar Plot (Top 25) ----
kk_df <- hh[1:min(25, nrow(hh)), ]

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

p1 <- ggplot(kk_df, aes(x = Count, y = Description, fill = category)) +
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

ggsave("04.KEGG_barplot.pdf", p1, width = 9, height = 8)
cat("Saved: 04.KEGG_barplot.pdf\n")

# ---- Style 2: Significance Bar Plot ----
hh$neg_log10_p <- -log10(hh$p.adjust)
hh <- hh[order(hh$neg_log10_p, decreasing = FALSE), ]
hh$Description <- factor(hh$Description, levels = hh$Description)

p2 <- ggplot(hh, aes(x = neg_log10_p, y = Description, fill = p.adjust)) +
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

ggsave("05.KEGG_plot.pdf", p2, width = 8, height = 5)
cat("Saved: 05.KEGG_plot.pdf\n")

cat("\n===== KEGG enrichment analysis complete =====\n")
