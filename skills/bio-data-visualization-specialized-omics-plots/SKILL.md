---
name: bio-data-visualization-specialized-omics-plots
description: "Use when creating volcano, MA, or enrichment plots."
tool_type: mixed
primary_tool: ggplot2
---

## Version Compatibility

Reference examples tested with: DESeq2 1.42+, edgeR 4.0+, ggplot2 3.5+, matplotlib 3.8+, numpy 1.26+, scanpy 1.10+, scikit-learn 1.4+

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures
- R: `packageVersion('<pkg>')` then `?function_name` to verify parameters

If code throws ImportError, AttributeError, or TypeError, introspect the installed
package and adapt the example to match the actual API rather than retrying.

# Specialized Omics Plots

**"Create omics-specific plots"** → Generate MA plots, PCA biplots, sample correlation heatmaps, and other domain-specific visualizations for genomics data.
- Python: `scanpy.pl.pca()`, `matplotlib` custom plots
- R: `DESeq2::plotMA()`, `PCAtools::biplot()`

## Scope

This skill provides **reusable plotting functions** for common omics visualizations that can be applied across different analysis types:
- Volcano plots (any DE result)
- MA plots (any log-fold-change data)
- PCA plots (any high-dimensional data)
- Enrichment dotplots (manual, not enrichplot)
- Expression boxplots with statistics
- Survival curves

**For DESeq2/edgeR built-in functions** (plotMA, plotPCA, plotDispEsts), see `differential-expression/de-visualization`.
**For enrichplot-specific functions** (dotplot, cnetplot, emapplot, gseaplot2), see `pathway-analysis/enrichment-visualization`.

## Volcano Plot (R)

### Basic ggplot2 Volcano

```r
library(ggplot2)
library(ggrepel)

volcano_plot <- function(res, fdr = 0.05, lfc = 1, top_n = 10) {
    res <- res %>%
        mutate(
            significance = case_when(
                padj < fdr & log2FoldChange > lfc ~ 'Up',
                padj < fdr & log2FoldChange < -lfc ~ 'Down',
                TRUE ~ 'NS'
            ),
            label = ifelse(rank(padj) <= top_n & significance != 'NS', gene, '')
        )

    ggplot(res, aes(log2FoldChange, -log10(pvalue), color = significance)) +
        geom_point(alpha = 0.6, size = 1.5) +
        geom_text_repel(aes(label = label), color = 'black', size = 3, max.overlaps = 20) +
        scale_color_manual(values = c('Up' = '#E64B35', 'Down' = '#4DBBD5', 'NS' = 'grey60')) +
        geom_vline(xintercept = c(-lfc, lfc), linetype = 'dashed', color = 'grey40') +
        geom_hline(yintercept = -log10(fdr), linetype = 'dashed', color = 'grey40') +
        labs(x = expression(Log[2]~Fold~Change), y = expression(-Log[10]~P-value)) +
        theme_bw() + theme(panel.grid = element_blank())
}
```

### Manual ggplot2 with Gene Labels

Add non-overlapping gene name labels for top significant genes or genes of interest:

```r
# Label top significant genes
top_genes <- df %>%
    filter(padj < 0.05, abs(log2FoldChange) > 1) %>%
    arrange(pvalue) %>%
    head(20)

ggplot(df, aes(x = log2FoldChange, y = -log10(pvalue))) +
    geom_point(aes(color = significance), alpha = 0.6, size = 1.5) +
    scale_color_manual(values = c(Up = '#E64B35', Down = '#4DBBD5', NS = 'gray70')) +
    geom_text_repel(
        data = top_genes,
        aes(label = gene),
        size = 3,
        max.overlaps = 20,
        box.padding = 0.5,
        segment.color = 'gray50'
    ) +
    theme_classic()

# Label specific genes of interest
genes_of_interest <- c('TP53', 'BRCA1', 'MYC', 'EGFR')
highlight_df <- df %>% filter(gene %in% genes_of_interest)

ggplot(df, aes(x = log2FoldChange, y = -log10(pvalue))) +
    geom_point(aes(color = significance), alpha = 0.4, size = 1.5) +
    geom_point(data = highlight_df, color = 'black', size = 3) +
    geom_text_repel(data = highlight_df, aes(label = gene), fontface = 'bold') +
    theme_classic()
```

### EnhancedVolcano (R)

```r
library(EnhancedVolcano)

# Basic EnhancedVolcano
EnhancedVolcano(df,
    lab = df$gene,
    x = 'log2FoldChange',
    y = 'pvalue',
    pCutoff = 0.05,
    FCcutoff = 1,
    title = 'Treatment vs Control',
    subtitle = 'DE genes highlighted')

# Customized EnhancedVolcano
EnhancedVolcano(df,
    lab = df$gene,
    x = 'log2FoldChange',
    y = 'pvalue',
    pCutoff = 0.05,
    FCcutoff = 1,
    xlim = c(-5, 5),
    ylim = c(0, 50),
    pointSize = 2,
    labSize = 3,
    colAlpha = 0.6,
    col = c('gray70', '#4DBBD5', '#00A087', '#E64B35'),
    legendLabels = c('NS', 'Log2FC', 'p-value', 'p-value and Log2FC'),
    legendPosition = 'right',
    drawConnectors = TRUE,
    widthConnectors = 0.5,
    maxoverlapsConnectors = 20,
    selectLab = genes_of_interest,  # Only label specific genes
    boxedLabels = TRUE)

# EnhancedVolcano with custom keyvals for multi-category highlighting
keyvals <- ifelse(df$log2FoldChange > 2 & df$padj < 0.01, '#E64B35',
           ifelse(df$log2FoldChange < -2 & df$padj < 0.01, '#4DBBD5',
           ifelse(df$padj < 0.05, '#00A087', 'gray70')))
names(keyvals)[keyvals == '#E64B35'] <- 'Highly Up'
names(keyvals)[keyvals == '#4DBBD5'] <- 'Highly Down'
names(keyvals)[keyvals == '#00A087'] <- 'Moderate'
names(keyvals)[keyvals == 'gray70'] <- 'NS'

EnhancedVolcano(df,
    lab = df$gene,
    x = 'log2FoldChange',
    y = 'pvalue',
    colCustom = keyvals,
    legendPosition = 'right')
```

## Volcano Plot (Python)

### Basic Python Volcano

```python
import matplotlib.pyplot as plt
import numpy as np

def volcano_plot(df, fdr=0.05, lfc=1, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    sig_up = (df['padj'] < fdr) & (df['log2FoldChange'] > lfc)
    sig_down = (df['padj'] < fdr) & (df['log2FoldChange'] < -lfc)
    ns = ~(sig_up | sig_down)

    ax.scatter(df.loc[ns, 'log2FoldChange'], -np.log10(df.loc[ns, 'pvalue']),
               c='grey', alpha=0.5, s=10, label='NS')
    ax.scatter(df.loc[sig_up, 'log2FoldChange'], -np.log10(df.loc[sig_up, 'pvalue']),
               c='#E64B35', alpha=0.7, s=15, label='Up')
    ax.scatter(df.loc[sig_down, 'log2FoldChange'], -np.log10(df.loc[sig_down, 'pvalue']),
               c='#4DBBD5', alpha=0.7, s=15, label='Down')

    ax.axhline(-np.log10(fdr), ls='--', c='grey', lw=0.8)
    ax.axvline(-lfc, ls='--', c='grey', lw=0.8)
    ax.axvline(lfc, ls='--', c='grey', lw=0.8)

    ax.set_xlabel('Log2 Fold Change')
    ax.set_ylabel('-Log10 P-value')
    ax.legend()
    return ax
```

### Python Volcano with Gene Labels (adjustText)

```python
from adjustText import adjust_text

# Color by significance
colors = np.where((df['padj'] < 0.05) & (df['log2FoldChange'] > 1), '#E64B35',
         np.where((df['padj'] < 0.05) & (df['log2FoldChange'] < -1), '#4DBBD5', 'gray'))

# Get top genes to label
top_idx = df.nsmallest(15, 'pvalue').index

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(df['log2FoldChange'], -np.log10(df['pvalue']), c=colors, alpha=0.5, s=15)

# Add labels with adjust_text to avoid overlaps
texts = []
for idx in top_idx:
    texts.append(ax.text(df.loc[idx, 'log2FoldChange'],
                         -np.log10(df.loc[idx, 'pvalue']),
                         df.loc[idx, 'gene'],
                         fontsize=8))

adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
plt.tight_layout()
```

### Threshold Customization

```r
# Standard thresholds
# FC > 1 (2-fold change): Common for RNA-seq
# FC > 0.58 (~1.5-fold): More sensitive, use for subtle effects
# padj < 0.05: Standard FDR threshold
# padj < 0.01: Stringent, fewer false positives
# padj < 0.1: Relaxed, use for exploratory analysis

# Adjust thresholds based on your data
pval_threshold <- 0.05
fc_threshold <- 1  # log2 scale

df$significance <- case_when(
    df$padj < pval_threshold & df$log2FoldChange > fc_threshold ~ 'Up',
    df$padj < pval_threshold & df$log2FoldChange < -fc_threshold ~ 'Down',
    TRUE ~ 'NS'
)
```

### Save Publication-Ready Volcano

```r
# R - high resolution
ggsave('volcano.pdf', width = 8, height = 6)
ggsave('volcano.png', width = 8, height = 6, dpi = 300)

# EnhancedVolcano returns ggplot object
p <- EnhancedVolcano(df, lab = df$gene, x = 'log2FoldChange', y = 'pvalue')
ggsave('volcano.pdf', p, width = 10, height = 8)
```

```python
# Python
plt.savefig('volcano.pdf', bbox_inches='tight')
plt.savefig('volcano.png', dpi=300, bbox_inches='tight')
```

## MA Plot

```r
ma_plot <- function(res, fdr = 0.05) {
    res <- res %>%
        mutate(significant = padj < fdr & !is.na(padj))

    ggplot(res, aes(log10(baseMean), log2FoldChange, color = significant)) +
        geom_point(alpha = 0.5, size = 1) +
        scale_color_manual(values = c('FALSE' = 'grey60', 'TRUE' = '#E64B35')) +
        geom_hline(yintercept = 0, color = 'black', linewidth = 0.5) +
        labs(x = expression(Log[10]~Mean~Expression), y = expression(Log[2]~Fold~Change)) +
        theme_bw() + theme(panel.grid = element_blank(), legend.position = 'none')
}
```

## PCA Plot (R)

**Goal:** Create a PCA scatter plot from a variance-stabilized expression matrix, colored by experimental condition.

**Approach:** Select the top most-variable genes, run PCA on transposed assay data, extract variance-explained percentages, and plot PC1 vs PC2 with 95% confidence ellipses per group.

```r
pca_plot <- function(vsd, intgroup = 'condition', ntop = 500) {
    rv <- rowVars(assay(vsd))
    select <- order(rv, decreasing = TRUE)[seq_len(min(ntop, length(rv)))]
    pca <- prcomp(t(assay(vsd)[select, ]))
    percentVar <- round(100 * pca$sdev^2 / sum(pca$sdev^2), 1)

    pca_df <- data.frame(PC1 = pca$x[, 1], PC2 = pca$x[, 2], colData(vsd))

    ggplot(pca_df, aes(PC1, PC2, color = .data[[intgroup]])) +
        geom_point(size = 3) +
        stat_ellipse(level = 0.95, linetype = 'dashed') +
        labs(x = paste0('PC1 (', percentVar[1], '%)'),
             y = paste0('PC2 (', percentVar[2], '%)')) +
        theme_bw() + theme(panel.grid = element_blank())
}
```

## PCA Plot (Python)

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def pca_plot(df, metadata, color_by, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    pca = PCA(n_components=2)
    pcs = pca.fit_transform(df.T)

    for group in metadata[color_by].unique():
        mask = metadata[color_by] == group
        ax.scatter(pcs[mask, 0], pcs[mask, 1], label=group, alpha=0.8, s=50)

    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
    ax.legend()
    return ax
```

## Dotplot for Enrichment

**Goal:** Visualize enrichment analysis results as a dot plot showing gene ratio, count, and significance for top pathways.

**Approach:** Sort terms by adjusted p-value, compute numeric gene ratios, and plot with dot size proportional to gene count and color mapped to significance on a log scale.

```r
library(ggplot2)

enrichment_dotplot <- function(enrich_result, top_n = 20) {
    df <- enrich_result %>%
        arrange(p.adjust) %>%
        head(top_n) %>%
        mutate(Description = factor(Description, levels = rev(Description)),
               GeneRatio_numeric = sapply(strsplit(GeneRatio, '/'), function(x) as.numeric(x[1])/as.numeric(x[2])))

    ggplot(df, aes(GeneRatio_numeric, Description, size = Count, color = p.adjust)) +
        geom_point() +
        scale_color_gradient(low = '#E64B35', high = '#4DBBD5', trans = 'log10') +
        scale_size_continuous(range = c(3, 10)) +
        labs(x = 'Gene Ratio', y = NULL, color = 'Adj. P-value', size = 'Count') +
        theme_bw() + theme(panel.grid.major.y = element_blank())
}
```

## Boxplot with Statistics

```r
library(ggpubr)

expression_boxplot <- function(df, gene, group_var) {
    ggboxplot(df, x = group_var, y = gene, color = group_var,
              add = 'jitter', palette = 'npg') +
        stat_compare_means(method = 't.test', label = 'p.signif') +
        labs(y = paste0(gene, ' Expression')) +
        theme(legend.position = 'none')
}
```

## UMAP/tSNE Plot

```python
import scanpy as sc
import matplotlib.pyplot as plt

def umap_plot(adata, color, ax=None, **kwargs):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    sc.pl.umap(adata, color=color, ax=ax, show=False, **kwargs)
    return ax

# With custom styling
sc.pl.umap(adata, color='leiden', palette='tab20', frameon=False,
           title='', legend_loc='on data', legend_fontsize=8)
```

## Correlation Plot

```r
library(corrplot)

cor_mat <- cor(t(top_genes_mat), method = 'pearson')
corrplot(cor_mat, method = 'color', type = 'lower', order = 'hclust',
         tl.col = 'black', tl.cex = 0.7, col = colorRampPalette(c('#4DBBD5', 'white', '#E64B35'))(100))
```

## Violin Plot with Split

```r
ggplot(df, aes(cluster, expression, fill = condition)) +
    geom_split_violin(alpha = 0.7) +
    geom_boxplot(width = 0.2, position = position_dodge(0.5), outlier.shape = NA) +
    scale_fill_manual(values = c('#4DBBD5', '#E64B35')) +
    theme_bw()
```

## Survival Curves

```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, status) ~ group, data = df)
ggsurvplot(fit, data = df, risk.table = TRUE, pval = TRUE,
           palette = c('#4DBBD5', '#E64B35'),
           legend.labs = c('Low', 'High'))
```

## Related Skills

- data-visualization/ggplot2-fundamentals - Base plotting
- data-visualization/color-palettes - Color selection
- differential-expression/de-visualization - DE-specific plots
- pathway-analysis/enrichment-visualization - Enrichment plots
