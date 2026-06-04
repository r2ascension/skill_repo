---
name: data-visualization-biomedical
description: "Use when creating publication-quality plots and visualizations using matplotlib, seaborn, and scanpy. Covers volcano plots, heatmaps, UMAP plots, dot plots, survival curves, forest plots, multi-panel figures, and general-purpose scientific charts (scatter, line, box, violin, bar). Includes journal-ready aesthetics, proper statistical annotations, and colorblind-safe palettes."
license: Proprietary
---

<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Biomedical Data Visualization

## Overview

This skill enables creation of professional scientific visualizations using **matplotlib**, **seaborn**, and **scanpy** for biomedical data. It covers both general-purpose chart types (scatter, line, box, violin, bar, heatmap) and domain-specific plots (volcano, UMAP, dotplot, multi-panel figures) with publication-quality styling and proper statistical annotations.

## Publication-Quality Settings

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import gridspec
import matplotlib.patches as mpatches

# Nature/Blood style settings
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8,
    'axes.labelsize': 8,
    'axes.titlesize': 9,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
})

# Set style for publication-quality plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Color palettes
NATURE_COLORS = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', '#8491B4']
BLOOD_COLORS = ['#D62728', '#1F77B4', '#2CA02C', '#FF7F0E', '#9467BD', '#8C564B']
```

## General-Purpose Plot Types

### Basic Scatter Plot
```python
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(x_data, y_data, s=20, alpha=0.6, c='steelblue', edgecolors='k', linewidths=0.5)
ax.set_xlabel('Gene Expression (log2)', fontsize=12)
ax.set_ylabel('Cell Count', fontsize=12)
ax.set_title('Expression vs. Cell Count', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('scatter_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Line Plot with Multiple Series
```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(time_points, group1_values, marker='o', label='Group 1', color='#E74C3C', linewidth=2)
ax.plot(time_points, group2_values, marker='s', label='Group 2', color='#3498DB', linewidth=2)
ax.plot(time_points, group3_values, marker='^', label='Group 3', color='#2ECC71', linewidth=2)
ax.set_xlabel('Time Point', fontsize=12)
ax.set_ylabel('Expression Level', fontsize=12)
ax.set_title('Gene Expression Over Time', fontsize=14, fontweight='bold')
ax.legend(frameon=True, loc='best', fontsize=10)
ax.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('line_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Box Plot and Violin Plot
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Box plot
sns.boxplot(data=df, x='cluster', y='expression', palette='Set2', ax=ax1)
ax1.set_title('Box Plot: Expression by Cluster', fontsize=12, fontweight='bold')
ax1.set_xlabel('Cluster', fontsize=11)
ax1.set_ylabel('Expression Level', fontsize=11)
ax1.tick_params(axis='x', rotation=45)

# Violin plot
sns.violinplot(data=df, x='cluster', y='expression', palette='muted', ax=ax2, inner='quartile')
ax2.set_title('Violin Plot: Expression Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('Cluster', fontsize=11)
ax2.set_ylabel('Expression Level', fontsize=11)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('box_violin_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Bar Plot with Error Bars
```python
fig, ax = plt.subplots(figsize=(7, 5))
categories = ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
means = [120, 85, 200, 150]
errors = [15, 10, 25, 20]

bars = ax.bar(categories, means, yerr=errors, capsize=5,
               color=['#E74C3C', '#3498DB', '#2ECC71', '#F39C12'],
               edgecolor='black', linewidth=1.2, alpha=0.8)
ax.set_ylabel('Cell Count', fontsize=12)
ax.set_title('Cell Counts by Cluster', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(means) * 1.3)

# Add value labels on bars
for bar, mean in zip(bars, means):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{mean}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('bar_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Density Plot
```python
from scipy.stats import gaussian_kde

fig, ax = plt.subplots(figsize=(8, 6))
xy = np.vstack([x_data, y_data])
z = gaussian_kde(xy)(xy)
idx = z.argsort()
x, y, z_data = x_data[idx], y_data[idx], z[idx]

scatter = ax.scatter(x, y, c=z_data, s=20, cmap='viridis', alpha=0.6, edgecolors='none')
plt.colorbar(scatter, ax=ax, label='Density')
ax.set_xlabel('UMAP1', fontsize=12)
ax.set_ylabel('UMAP2', fontsize=12)
ax.set_title('Density Scatter Plot', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('density_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Custom Color Palette
```python
# Define custom colors
custom_palette = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
sns.set_palette(custom_palette)

# Or create color dict for specific mapping
color_dict = {
    'T cells': '#E74C3C',
    'B cells': '#3498DB',
    'Monocytes': '#2ECC71',
    'NK cells': '#F39C12'
}

for cell_type, color in color_dict.items():
    mask = df['celltype'] == cell_type
    ax.scatter(df.loc[mask, 'x'], df.loc[mask, 'y'],
               c=color, label=cell_type, s=20, alpha=0.7)
ax.legend()
```

## Volcano Plot

### Function-Based Volcano Plot (Python)
```python
def volcano_plot(df, log2fc_col='log2FC', pval_col='pval_adj', 
                 gene_col='gene', fc_thresh=1, pval_thresh=0.05,
                 highlight_genes=None, figsize=(4, 4)):
    """Publication-quality volcano plot."""
    fig, ax = plt.subplots(figsize=figsize)
    
    df = df.copy()
    df['-log10pval'] = -np.log10(df[pval_col].clip(lower=1e-300))
    
    # Categorize points
    df['category'] = 'NS'
    df.loc[(df[log2fc_col] > fc_thresh) & (df[pval_col] < pval_thresh), 'category'] = 'Up'
    df.loc[(df[log2fc_col] < -fc_thresh) & (df[pval_col] < pval_thresh), 'category'] = 'Down'
    
    colors = {'NS': '#CCCCCC', 'Up': '#E64B35', 'Down': '#4DBBD5'}
    
    for cat, color in colors.items():
        subset = df[df['category'] == cat]
        ax.scatter(subset[log2fc_col], subset['-log10pval'], 
                   c=color, s=10, alpha=0.7, edgecolors='none', label=cat)
    
    # Add threshold lines
    ax.axhline(-np.log10(pval_thresh), color='grey', linestyle='--', linewidth=0.5)
    ax.axvline(-fc_thresh, color='grey', linestyle='--', linewidth=0.5)
    ax.axvline(fc_thresh, color='grey', linestyle='--', linewidth=0.5)
    
    # Label specific genes
    if highlight_genes:
        for gene in highlight_genes:
            if gene in df[gene_col].values:
                row = df[df[gene_col] == gene].iloc[0]
                ax.annotate(gene, (row[log2fc_col], row['-log10pval']),
                           fontsize=6, ha='center')
    
    ax.set_xlabel('log2 Fold Change')
    ax.set_ylabel('-log10 Adjusted P-value')
    ax.legend(frameon=False, loc='upper right')
    
    plt.tight_layout()
    return fig, ax

# Simplified inline volcano for DEG analysis
# deg_df should have columns: gene, log2FC, pvalue
fig, ax = plt.subplots(figsize=(8, 7))
deg_df['-log10_pvalue'] = -np.log10(deg_df['pvalue'])
deg_df['significant'] = 'Not Significant'
deg_df.loc[(deg_df['log2FC'] > 1) & (deg_df['pvalue'] < 0.05), 'significant'] = 'Up-regulated'
deg_df.loc[(deg_df['log2FC'] < -1) & (deg_df['pvalue'] < 0.05), 'significant'] = 'Down-regulated'

for category, color in zip(['Not Significant', 'Up-regulated', 'Down-regulated'],
                            ['gray', 'red', 'blue']):
    mask = deg_df['significant'] == category
    ax.scatter(deg_df.loc[mask, 'log2FC'], deg_df.loc[mask, '-log10_pvalue'],
               c=color, label=category, s=20, alpha=0.6, edgecolors='none')

ax.axvline(x=1, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=-1, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(y=-np.log10(0.05), color='black', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('log2 Fold Change', fontsize=12)
ax.set_ylabel('-log10(p-value)', fontsize=12)
ax.set_title('Volcano Plot: Differential Expression', fontsize=14, fontweight='bold')
ax.legend(frameon=True, loc='upper right')
plt.tight_layout()
plt.savefig('volcano_plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Heatmap

### Clustered Heatmap with scipy
```python
import scipy.cluster.hierarchy as sch
from matplotlib.colors import LinearSegmentedColormap

def clustered_heatmap(data, row_labels=None, col_labels=None,
                      cmap='RdBu_r', center=0, figsize=(8, 10),
                      row_cluster=True, col_cluster=True):
    """Hierarchically clustered heatmap."""
    
    if row_cluster:
        row_linkage = sch.linkage(data, method='ward')
        row_order = sch.dendrogram(row_linkage, no_plot=True)['leaves']
        data = data[row_order, :]
        if row_labels is not None:
            row_labels = [row_labels[i] for i in row_order]
    
    if col_cluster:
        col_linkage = sch.linkage(data.T, method='ward')
        col_order = sch.dendrogram(col_linkage, no_plot=True)['leaves']
        data = data[:, col_order]
        if col_labels is not None:
            col_labels = [col_labels[i] for i in col_order]
    
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(data, aspect='auto', cmap=cmap, 
                   vmin=center-np.abs(data).max(), vmax=center+np.abs(data).max())
    
    if row_labels:
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels)
    if col_labels:
        ax.set_xticks(range(len(col_labels)))
        ax.set_xticklabels(col_labels, rotation=45, ha='right')
    
    plt.colorbar(im, ax=ax, shrink=0.5, label='Expression (z-score)')
    plt.tight_layout()
    return fig, ax

# Seaborn heatmap (simpler alternative)
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    gene_expression_matrix,
    cmap='viridis',
    cbar_kws={'label': 'Expression'},
    xticklabels=True,
    yticklabels=True,
    linewidths=0.5,
    linecolor='gray',
    ax=ax
)
ax.set_title('Gene Expression Heatmap', fontsize=14, fontweight='bold')
ax.set_xlabel('Samples', fontsize=12)
ax.set_ylabel('Genes', fontsize=12)
plt.tight_layout()
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Scanpy Visualization Enhancements

```python
import scanpy as sc

def enhanced_dotplot(adata, genes, groupby, figsize=(10, 8)):
    """Enhanced dot plot with proper visibility."""
    sc.pl.dotplot(
        adata, var_names=genes, groupby=groupby,
        expression_cutoff=0.0001,
        mean_only_expressed=False,
        standard_scale='None',
        smallest_dot=0.1,
        dot_max=1.0,
        cmap='Reds',
        colorbar_title='Mean expression',
        size_title='Fraction of cells (%)',
        figsize=figsize,
        show=False
    )
    plt.tight_layout()
    return plt.gcf()

def multi_batch_umap(adata, color_by, batch_key='batch', figsize_per=(4, 4)):
    """UMAP plots per batch."""
    batches = adata.obs[batch_key].unique()
    n_batches = len(batches)
    
    fig, axes = plt.subplots(1, n_batches, 
                              figsize=(figsize_per[0]*n_batches, figsize_per[1]))
    if n_batches == 1:
        axes = [axes]
    
    for ax, batch in zip(axes, batches):
        adata_batch = adata[adata.obs[batch_key] == batch]
        sc.pl.umap(adata_batch, color=color_by, ax=ax, show=False,
                   title=f'{batch}')
    
    plt.tight_layout()
    return fig
```

### UMAP/tSNE Visualization (Manual)
```python
# Assuming adata.obsm['X_umap'] exists and adata.obs['clusters'] exists
fig, ax = plt.subplots(figsize=(8, 7))
clusters = adata.obs['clusters'].unique()
n_clusters = len(clusters)
colors = plt.cm.tab20(np.linspace(0, 1, n_clusters))

for i, cluster in enumerate(clusters):
    mask = adata.obs['clusters'] == cluster
    ax.scatter(
        adata.obsm['X_umap'][mask, 0],
        adata.obsm['X_umap'][mask, 1],
        c=[colors[i]],
        label=f'Cluster {cluster}',
        s=10,
        alpha=0.7,
        edgecolors='none'
    )

ax.set_xlabel('UMAP1', fontsize=12)
ax.set_ylabel('UMAP2', fontsize=12)
ax.set_title('UMAP Projection by Cluster', fontsize=14, fontweight='bold')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, fontsize=9)
plt.tight_layout()
plt.savefig('umap_clusters.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Gene Expression Dot Plot (Manual)
```python
from matplotlib.colors import Normalize

# dot_size_matrix: % cells expressing (0-100)
# color_matrix: mean expression level
fig, ax = plt.subplots(figsize=(10, 6))

for i, gene in enumerate(genes):
    for j, cluster in enumerate(clusters):
        size = dot_size_matrix[i, j] * 5  # Scale factor
        color_val = color_matrix[i, j]
        ax.scatter(j, i, s=size, c=[color_val], cmap='Reds',
                   vmin=0, vmax=color_matrix.max(),
                   edgecolors='black', linewidths=0.5)

ax.set_xticks(range(len(clusters)))
ax.set_xticklabels(clusters, rotation=45, ha='right')
ax.set_yticks(range(len(genes)))
ax.set_yticklabels(genes)
ax.set_xlabel('Cluster', fontsize=12)
ax.set_ylabel('Gene', fontsize=12)
ax.set_title('Marker Gene Expression', fontsize=14, fontweight='bold')

norm = Normalize(vmin=0, vmax=color_matrix.max())
sm = plt.cm.ScalarMappable(cmap='Reds', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.02)
cbar.set_label('Mean Expression', rotation=270, labelpad=15)
plt.tight_layout()
plt.savefig('gene_dotplot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### QC Metrics Visualization
```python
# Assuming adata.obs has QC columns: n_genes, n_counts, percent_mito
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(adata.obs['n_genes'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0].axvline(adata.obs['n_genes'].median(), color='red', linestyle='--', label='Median')
axes[0].set_xlabel('Genes per Cell', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Genes per Cell Distribution', fontsize=12, fontweight='bold')
axes[0].legend()

axes[1].scatter(adata.obs['n_counts'], adata.obs['n_genes'],
                s=5, alpha=0.5, c='coral')
axes[1].set_xlabel('UMI Counts', fontsize=11)
axes[1].set_ylabel('Genes Detected', fontsize=11)
axes[1].set_title('UMIs vs Genes', fontsize=12, fontweight='bold')

sns.violinplot(y=adata.obs['percent_mito'], ax=axes[2], color='lightgreen')
axes[2].axhline(y=20, color='red', linestyle='--', label='20% threshold')
axes[2].set_ylabel('Mitochondrial %', fontsize=11)
axes[2].set_title('Mitochondrial Content', fontsize=12, fontweight='bold')
axes[2].legend()

plt.tight_layout()
plt.savefig('qc_metrics.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Statistical Annotation

```python
from scipy import stats

def add_significance(ax, x1, x2, y, h, p_value):
    """Add significance bar to plot."""
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], 'k-', linewidth=0.5)
    
    if p_value < 0.0001:
        sig = '****'
    elif p_value < 0.001:
        sig = '***'
    elif p_value < 0.01:
        sig = '**'
    elif p_value < 0.05:
        sig = '*'
    else:
        sig = 'ns'
    
    ax.text((x1+x2)/2, y+h, sig, ha='center', va='bottom', fontsize=8)
```

## Multi-Panel Figure Assembly

### Using GridSpec
```python
from matplotlib.gridspec import GridSpec

def create_figure_panel(n_rows, n_cols, width_ratios=None, height_ratios=None):
    """Create multi-panel figure."""
    fig = plt.figure(figsize=(3*n_cols, 3*n_rows))
    gs = GridSpec(n_rows, n_cols, figure=fig,
                  width_ratios=width_ratios or [1]*n_cols,
                  height_ratios=height_ratios or [1]*n_rows,
                  wspace=0.3, hspace=0.3)
    
    axes = []
    for i in range(n_rows):
        row = []
        for j in range(n_cols):
            ax = fig.add_subplot(gs[i, j])
            row.append(ax)
        axes.append(row)
    
    return fig, axes

def label_panels(axes, labels=None, fontsize=12, fontweight='bold'):
    """Add A, B, C... labels to panels."""
    if labels is None:
        labels = [chr(65+i) for i in range(len(axes))]
    
    for ax, label in zip(axes, labels):
        ax.text(-0.15, 1.05, label, transform=ax.transAxes,
                fontsize=fontsize, fontweight=fontweight, va='top')

# Example: Complex multi-panel figure
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :2])
ax1.scatter(x_data, y_data, c=cluster_labels, cmap='tab10', s=10, alpha=0.6)
ax1.set_title('A. UMAP Projection', fontsize=12, fontweight='bold', loc='left')
ax1.set_xlabel('UMAP1')
ax1.set_ylabel('UMAP2')

ax2 = fig.add_subplot(gs[0, 2])
sns.violinplot(data=df, y='expression', palette='Set2', ax=ax2)
ax2.set_title('B. Expression', fontsize=12, fontweight='bold', loc='left')

ax3 = fig.add_subplot(gs[1, :])
sns.heatmap(matrix, cmap='coolwarm', center=0, ax=ax3, cbar_kws={'label': 'Z-score'})
ax3.set_title('C. Gene Expression Heatmap', fontsize=12, fontweight='bold', loc='left')

plt.savefig('multi_panel_figure.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Export for Journals

```python
def save_figure(fig, filename, formats=['pdf', 'png', 'svg']):
    """Save in multiple formats for journals."""
    for fmt in formats:
        fig.savefig(f"{filename}.{fmt}", format=fmt, dpi=300, 
                    bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {filename}.{{{'|'.join(formats)}}}")
```

## Best Practices

1. **Figure Size**: Use appropriate dimensions for target medium (papers: 6-8 inches wide, posters: larger)
2. **DPI**: Save at 300 DPI for publications, 150 DPI for presentations
3. **Colors**: Use colorblind-friendly palettes (e.g., `viridis`, `Set2`, `tab10`)
4. **Fonts**: Keep font sizes readable (titles: 12-14pt, labels: 10-12pt, ticks: 8-10pt)
5. **Transparency**: Use alpha for overlapping points to show density
6. **Layout**: Always call `plt.tight_layout()` before saving to prevent label clipping
7. **File Format**: PNG for general use, SVG for vector graphics (editable in Illustrator)
8. **Close Figures**: Call `plt.close()` after saving to free memory when generating many plots
9. **Privacy**: Avoid plotting PII (names, emails) directly
10. **Accuracy**: Ensure axes are labeled correctly with units
11. **Readability**: Use appropriate scales (log vs linear) and avoid clutter

## Troubleshooting

### "Figure too cluttered with many points"
Use transparency and smaller point sizes:
```python
ax.scatter(x, y, s=5, alpha=0.3, edgecolors='none')
```

### "Legend overlaps with data"
Place legend outside the plot area:
```python
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
```

### "Labels are cut off in saved figure"
Use `bbox_inches='tight'`:
```python
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

### "Colors don't match between plots"
Define color palette once and reuse:
```python
PALETTE = {'Group A': '#E74C3C', 'Group B': '#3498DB'}
```

### "Heatmap text too small"
Adjust figure size or font size:
```python
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(data, ax=ax, annot_kws={'fontsize': 8})
```

## Technical Notes

- **Libraries**: Uses `matplotlib`, `seaborn`, `scanpy`, `scipy`, `numpy`, `pandas` (widely supported, stable)
- **Execution**: Runs locally in the agent's sandbox
- **File Formats**: Supports PNG, PDF, SVG, JPEG
- **Performance**: Typical plot generation takes <1 second for standard plots, 2-5 seconds for complex multi-panel figures
- **Memory**: Keep figure count reasonable; close figures after saving if generating many plots

## References

- See `references/color_guidelines.md` for accessibility standards.
- See `scripts/figure_templates.py` for pre-built templates.
- Matplotlib documentation: https://matplotlib.org/stable/contents.html
- Seaborn documentation: https://seaborn.pydata.org/
- Matplotlib gallery: https://matplotlib.org/stable/gallery/index.html
- Seaborn gallery: https://seaborn.pydata.org/examples/index.html


<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->
