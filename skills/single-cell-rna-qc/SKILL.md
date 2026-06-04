---
name: single-cell-rna-qc
description: "Use when users request QC analysis, filtering low-quality cells, assessing data quality, or following scverse/scanpy best practices for single-cell analysis."
measurable_outcome: Produce filtered .h5ad files, before/after plots, and qc_summary.json within 20 minutes per dataset.
allowed-tools:
  - Read
  - Bash
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

# Single-Cell RNA-seq Quality Control

Automated QC workflow for single-cell RNA-seq data following scverse best practices.

## At-a-Glance
- **description (10-20 chars):** QC autopilot
- **keywords:** scRNAseq, MAD, h5ad, QC, plots

## When to Use This Skill

Use when users:
- Request quality control or QC on single-cell RNA-seq data
- Want to filter low-quality cells or assess data quality
- Need QC visualizations or metrics
- Ask to follow scverse/scanpy best practices
- Request MAD-based filtering or outlier detection

**Supported input formats:**
- `.h5ad` files (AnnData format from scanpy/Python workflows)
- `.h5` files (10X Genomics Cell Ranger output)
- 10X Genomics directory (raw_feature_bc_matrix/ with .mtx, barcodes.tsv, features.tsv)

**Default recommendation**: Use Approach 1 (complete pipeline) unless the user has specific custom requirements or explicitly requests non-standard filtering logic.

## Approach 1: Complete QC Pipeline (Recommended for Standard Workflows)

For standard QC following scverse best practices, use the convenience script `scripts/qc_analysis.py`:

```bash
python3 scripts/qc_analysis.py input.h5ad
# or for 10X Genomics .h5 files:
python3 scripts/qc_analysis.py raw_feature_bc_matrix.h5
# or for 10X Genomics directory:
python3 scripts/qc_analysis.py /path/to/raw_feature_bc_matrix/
```

The script automatically detects the file format and loads it appropriately.

**When to use this approach:**
- Standard QC workflow with adjustable thresholds (all cells filtered the same way)
- Batch processing multiple datasets
- Quick exploratory analysis
- User wants the "just works" solution

**Requirements:** anndata, scanpy, scipy, matplotlib, seaborn, numpy

**Parameters:**

Customize filtering thresholds and gene patterns using command-line parameters:
- `--output-dir` - Output directory
- `--mad-counts`, `--mad-genes`, `--mad-mt` - MAD thresholds for counts/genes/MT%
- `--mt-threshold` - Hard mitochondrial % cutoff
- `--min-cells` - Gene filtering threshold
- `--mt-pattern`, `--ribo-pattern`, `--hb-pattern` - Gene name patterns for different species
- `--no-log1p` - Disable log1p transform on counts/genes before MAD calculation (enabled by default)

Use `--help` to see current default values.

**Outputs:**

All files are saved to `<input_basename>_qc_results/` directory by default (or to the directory specified by `--output-dir`):
- `qc_metrics_before_filtering.png` - Pre-filtering visualizations
- `qc_filtering_thresholds.png` - MAD-based threshold overlays
- `qc_metrics_after_filtering.png` - Post-filtering quality metrics
- `<input_basename>_filtered.h5ad` - Clean, filtered dataset ready for downstream analysis
- `<input_basename>_with_qc.h5ad` - Original data with QC annotations preserved
- `qc_summary.json` - Machine-readable QC summary with parameters and counts

If copying outputs to `/mnt/user-data/outputs/` for user access, copy individual files (not the entire directory) so users can preview them directly as Claude.ai artifacts.

### Workflow Steps

The script performs the following steps:

1. **Calculate QC metrics** - Count depth, gene detection, mitochondrial/ribosomal/hemoglobin content
2. **Apply MAD-based filtering** - Permissive outlier detection using MAD thresholds for counts/genes/MT%
3. **Apply hard MT% cutoff** - Supplementary hard threshold for mitochondrial content
4. **Filter genes** - Remove genes detected in few cells
5. **Generate visualizations** - Comprehensive before/after plots with threshold overlays
6. **Save summary JSON** - Machine-readable QC summary with parameters, counts, and retention rate

## Approach 2: Modular Building Blocks (For Custom Workflows)

For custom analysis workflows or non-standard requirements, use the modular utility functions from `scripts/qc_core.py` and `scripts/qc_plotting.py`:

```python
# Run from scripts/ directory, or add scripts/ to sys.path if needed
import anndata as ad
from qc_core import calculate_qc_metrics, detect_outliers_mad, filter_cells
from qc_plotting import plot_qc_distributions  # Only if visualization needed

adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)
# ... custom analysis logic here
```

**When to use this approach:**
- Different workflow needed (skip steps, change order, apply different thresholds to subsets)
- Conditional logic (e.g., filter neurons differently than other cells)
- Partial execution (only metrics/visualization, no filtering)
- Integration with other analysis steps in a larger pipeline
- Custom filtering criteria beyond what command-line params support
- Log1p transform control and tail-direction filtering for fine-grained outlier detection

**Available utility functions:**

From `qc_core.py` (core QC operations):
- `calculate_qc_metrics(adata, mt_pattern, ribo_pattern, hb_pattern, inplace=True)` - Calculate QC metrics and annotate adata
- `detect_outliers_mad(adata, metric, n_mads, transform=None, tail='both', verbose=True)` - MAD-based outlier detection with optional log1p transform and tail control (both/high/low), returns boolean mask
- `apply_hard_threshold(adata, metric, threshold, operator='>', verbose=True)` - Apply hard cutoffs, returns boolean mask
- `filter_cells(adata, mask, inplace=False)` - Apply boolean mask to filter cells
- `filter_genes(adata, min_cells=20, min_counts=None, inplace=True)` - Filter genes by detection
- `print_qc_summary(adata, label='')` - Print summary statistics
- `build_qc_masks(adata, mad_counts=5, mad_genes=5, mad_mt=3, mt_threshold=8, ...)` - Generate all QC outlier masks and combined pass/fail mask in one call

From `qc_plotting.py` (visualization):
- `plot_qc_distributions(adata, output_path, title)` - Generate comprehensive QC plots
- `plot_filtering_thresholds(adata, outlier_masks, thresholds, output_path)` - Visualize filtering thresholds
- `plot_qc_after_filtering(adata, output_path)` - Generate post-filtering plots

**Example custom workflows:**

**Example 1: Only calculate metrics and visualize, don't filter yet**
```python
adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)
plot_qc_distributions(adata, 'qc_before.png', title='Initial QC')
print_qc_summary(adata, label='Before filtering')
```

**Example 2: Apply only MT% filtering, keep other metrics permissive**
```python
adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)

# Only filter high MT% cells
high_mt = apply_hard_threshold(adata, 'pct_counts_mt', 10, operator='>')
adata_filtered = filter_cells(adata, ~high_mt)
adata_filtered.write('filtered.h5ad')
```

**Example 3: Different thresholds for different subsets**
```python
adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)

# Apply type-specific QC (assumes cell_type metadata exists)
neurons = adata.obs['cell_type'] == 'neuron'
other_cells = ~neurons

# Neurons tolerate higher MT%, other cells use stricter threshold
neuron_qc = apply_hard_threshold(adata[neurons], 'pct_counts_mt', 15, operator='>')
other_qc = apply_hard_threshold(adata[other_cells], 'pct_counts_mt', 8, operator='>')
```

## Workflow
1. Accept `.h5ad`, 10x `.h5`, or 10x directory inputs; set mitochondrial/ribosomal patterns as needed.
2. Run `qc_analysis.py` (CLI) or call `qc_core` helpers to compute metrics, apply MAD thresholds, and filter cells/genes.
3. Generate standard plots (metrics before/after, threshold overlays) plus filtered data artifacts.
4. Document parameters (mad_counts/genes/mt, mt_threshold, min_cells, log1p flag) inside the summary JSON.
5. Provide guidance on next steps (doublet detection, downstream analysis).

## Guardrails
- Adjust MT% expectations for tissue context; avoid over-filtering rare populations.
- This workflow is QC only -- doublet handling and batch correction stay separate.
- Keep reproducibility by storing command invocations and environment info.
- Be permissive with filtering -- Default thresholds intentionally retain most cells to avoid losing rare populations.
- Inspect visualizations -- Always review before/after plots to ensure filtering makes biological sense.
- Consider dataset-specific factors -- Some tissues naturally have higher mitochondrial content (e.g., neurons, cardiomyocytes).
- Check gene annotations -- Mitochondrial gene prefixes vary by species (mt- for mouse, MT- for human).
- Iterate if needed -- QC parameters may need adjustment based on the specific experiment or tissue type.

## Reference Materials

For detailed QC methodology, parameter rationale, and troubleshooting guidance, see `references/scverse_qc_guidelines.md`. This reference provides:
- Detailed explanations of each QC metric and why it matters
- Rationale for MAD-based thresholds and why they're better than fixed cutoffs
- Guidelines for interpreting QC visualizations (histograms, violin plots, scatter plots)
- Species-specific considerations for gene annotations
- When and how to adjust filtering parameters
- Advanced QC considerations (ambient RNA correction, doublet detection)

See also `README.md`, `qc_core.py`, `qc_analysis.py`, and `qc_plotting.py` for API usage and schema details.

Load this reference when users need deeper understanding of the methodology or when troubleshooting QC issues.

## Next Steps After QC

Typical downstream analysis steps:
- Ambient RNA correction (SoupX, CellBender)
- Doublet detection (scDblFinder)
- Normalization (log-normalize, scran)
- Feature selection and dimensionality reduction
- Clustering and cell type annotation
