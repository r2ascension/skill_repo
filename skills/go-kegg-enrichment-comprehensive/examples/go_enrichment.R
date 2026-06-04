# GO Enrichment Analysis — Complete Example
# Reference: clusterProfiler 4.10+ | Verify API if version differs
#
# This script performs GO over-representation analysis on a DEG list
# and produces two visualization styles.

# ---- Setup ----
library(clusterProfiler)
library(org.Hs.eg.db)
library(enrichplot)
library(GOplot)
library(openxlsx)
library(ggplot2)
library(dplyr)
options(stringsAsFactors = FALSE)

# ---- Step 1: Load gene list ----
# Replace with your actual DEG file path
# gene_list <- rownames(read.csv("data/DEG.csv"))

# Example: generate a mock gene list for demonstration
set.seed(42)
library(org.Hs.eg.db)
all_genes <- keys(org.Hs.eg.db, keytype = "SYMBOL")
gene_list <- sample(all_genes, 500)  # Simulate 500 significant DEGs
cat(sprintf("Input: %d significant genes\n", length(gene_list)))

# ---- Step 2: Run GO enrichment ----
GO <- enrichGO(
  gene          = gene_list,
  OrgDb         = "org.Hs.eg.db",
  keyType       = "SYMBOL",
  pAdjustMethod = "BH",
  pvalueCutoff  = 1,       # Defer filtering to post-hoc
  minGSSize     = 5,
  ont           = "all",   # BP + CC + MF
  readable      = TRUE
)

GO_result <- GO@result
go <- as.data.frame(GO_result)
rownames(go) <- 1:nrow(go)
cat(sprintf("Raw GO terms: %d\n", nrow(go)))

# ---- Step 3: Filter and sort ----
go <- go[go$p.adjust < 0.05, ]
go <- go[go$Count > 1, ]
go <- go[order(go$Count, decreasing = TRUE), ]

cat(sprintf("Significant GO terms (padj<0.05, Count>1): %d\n", nrow(go)))
cat("\nOntology breakdown:\n")
print(table(go$ONTOLOGY))

# Save full results
write.xlsx(go, file = "01.GO.xlsx")
cat("\nSaved: 01.GO.xlsx\n")

# ---- Step 4: Extract top 8 per ontology for plotting ----
go_res <- go

Go_bp <- go_res[go_res$ONTOLOGY == "BP", ] |> arrange(desc(Count)) |> head(8)
Go_cc <- go_res[go_res$ONTOLOGY == "CC", ] |> arrange(desc(Count)) |> head(8)
Go_mf <- go_res[go_res$ONTOLOGY == "MF", ] |> arrange(desc(Count)) |> head(8)

go_res2 <- rbind(Go_bp, Go_cc, Go_mf)
cat(sprintf("Plotting terms: BP=%d, CC=%d, MF=%d\n", nrow(Go_bp), nrow(Go_cc), nrow(Go_mf)))

# ---- Style 1: Labeled Bar Plot ----
go_res2 <- go_res2 %>%
  mutate(
    ONTOLOGY    = factor(ONTOLOGY, levels = c("BP", "CC", "MF")),
    Description = factor(Description, levels = rev(Description[order(ONTOLOGY, -Count)]))
  ) %>%
  arrange(ONTOLOGY, -Count)

ontology_colors <- c("BP" = "#e4945b", "CC" = "#b7a8cf", "MF" = "#5a91c8")

p1 <- ggplot(go_res2, aes(x = Count, y = Description, fill = ONTOLOGY)) +
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
    plot.title         = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.text.y        = element_blank(),
    axis.ticks.y       = element_blank(),
    panel.grid.major.y = element_blank(),
    legend.position    = "right"
  ) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15)))

ggsave("02.GO_enrichment_barplot.pdf", p1, width = 8, height = 8)
cat("Saved: 02.GO_enrichment_barplot.pdf\n")

# ---- Style 2: Faceted Significance Plot ----
go_res2$neg_log10_p <- -log10(go_res2$p.adjust)
go_res2 <- go_res2[order(go_res2$ONTOLOGY, go_res2$neg_log10_p, decreasing = FALSE), ]
go_res2$Description <- factor(go_res2$Description, levels = unique(go_res2$Description))

p2 <- ggplot(go_res2, aes(x = neg_log10_p, y = Description, fill = p.adjust)) +
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
    axis.text          = element_text(color = "black", size = 10),
    panel.grid.major.y = element_blank(),
    strip.background   = element_rect(fill = "#f0f0f0"),
    strip.text         = element_text(face = "bold")
  ) +
  scale_x_continuous(expand = expansion(mult = c(0.01, 0.1)))

ggsave("02.GO_plot.pdf", p2, width = 8, height = 5.5)
cat("Saved: 02.GO_plot.pdf\n")

cat("\n===== GO enrichment analysis complete =====\n")
