---
name: bioskills-installer
description: "Use when setting up GPTomics bioSkills, installing bioinformatics skills, or when a bioinformatics task requires specialized skills that may not yet be installed."
---

# bioSkills Installer

Meta-skill that installs the full GPTomics bioSkills collection for bioinformatics analysis.

## Installation

Run the bundled install script to download and install all bioSkills:

```bash
bash scripts/install-bioskills.sh
```

Or install only specific categories:

```bash
bash scripts/install-bioskills.sh --categories "single-cell,variant-calling,differential-expression"
```

## What Gets Installed

The collection covers broad bioinformatics workflows including:

- Sequence and alignment analysis
- Read QC and read alignment
- RNA-seq, expression matrices, and differential expression
- Single-cell and spatial transcriptomics
- Variant calling, CNV analysis, and phasing/imputation
- ChIP-seq, ATAC-seq, methylation, and Hi-C
- Metagenomics and microbiome analysis
- Genome assembly, genome annotation, intervals, and engineering
- Gene regulatory networks, causal genomics, and RNA structure
- Immunoinformatics, clinical databases, and TCR/BCR analysis
- Proteomics, metabolomics, alternative splicing, chemoinformatics, and liquid biopsy
- Phylogenetics, population genetics, and comparative genomics
- Structural biology, systems biology, CRISPR screens, cytometry, reporting, and workflow management
- End-to-end workflow skills from FASTQ to final results

## After Installation

Once installed, skills are automatically triggered based on the task at hand. Example requests:

- "I have RNA-seq counts from treated vs control samples - find the differentially expressed genes"
- "Call variants from this whole genome sequencing BAM file"
- "Cluster my single-cell RNA-seq data and find marker genes"
- "Predict the structure of this protein sequence"
- "Run a metagenomics classification on these shotgun reads"

## Source

GitHub: https://github.com/GPTomics/bioSkills