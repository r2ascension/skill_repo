# Checked Literature and Method Archetypes

## 1. What Was Checked

The local report `E:\idm\deep-research-report (5).md` was cross-checked against journal or publisher pages for the representative papers it cites.

## 2. Quick Corrections to the Report

- The thyroid atlas entry is the npj Precision Oncology 2025 paper `Comprehensive single-cell RNA analysis reveals intertumoral microenvironment heterogeneity and hub niche of carcinogenesis in thyroid cancer`, not a generic `Liu et al.` shorthand.
- The kidney atlas entry is best anchored by the paper title `An atlas of healthy and injured cell states and niches in the human kidney` in `Nature` (2023); the report's author shorthand is not stable enough to reuse blindly.
- The CAR-T atlas with `695,819` cells is the `Nature` paper `Single-cell CAR T atlas reveals type 2 function in 8-year leukaemia remission`, published in 2024 rather than 2025.

## 3. Verified Representative Papers

### Atlas / landscape papers

1. `A single-cell atlas enables mapping of homeostatic cellular shifts in the adult human breast`
   - Journal: `Nature Genetics` (2024)
   - Signal from paper: single-cell RNA-seq from `55 donors`, `>800,000 cells`, atlas-style epithelial / immune / stromal subclustering.
   - Method signature: multi-donor atlas -> clustering -> subcluster annotation -> compare composition and state shifts across donor covariates.
   - URL: <https://www.nature.com/articles/s41588-024-01688-9>

2. `Comprehensive single-cell RNA analysis reveals intertumoral microenvironment heterogeneity and hub niche of carcinogenesis in thyroid cancer`
   - Journal: `npj Precision Oncology` (2025)
   - Signal from paper: `405,077` cells from `50` thyroid cancer samples plus `14` normal tissues; unbiased clustering; cell-cell communication; `NicheNet`; multiplex IHC validation.
   - Method signature: tumor atlas -> cell subset annotation -> niche/crosstalk analysis -> spatial or tissue-level validation.
   - URL: <https://www.nature.com/articles/s41698-025-00924-7>

3. `An atlas of healthy and injured cell states and niches in the human kidney`
   - Journal: `Nature` (2023)
   - Signal from paper: multimodal atlas integrating transcriptomic, epigenomic, imaging, `Slide-seq2`, and `Visium`; RNA data aligned by joint UMAP; Visium normalized with `SCTransform` and processed in `Seurat`.
   - Method signature: multi-assay atlas -> joint embedding -> state annotation -> spatial localization and niche mapping.
   - URL: <https://www.nature.com/articles/s41586-023-05769-3>

4. `Single-cell atlas of human lung aging identifies cell type dyssynchrony and increased transcriptional entropy`
   - Journal: `Nature Communications` (2026)
   - Signal from paper: scRNA-seq on `32` lungs plus integration with `28` control lungs; `199,400` cells from `60` donors; bulk-RNA validation; WGCNA; somatic mutation calling.
   - Method signature: age-focused atlas -> integration of in-house and reference cohorts -> cell proportion / DEG analysis -> orthogonal validation and advanced secondary analyses.
   - URL: <https://www.nature.com/articles/s41467-026-68810-9>

5. `Single-cell CAR T atlas reveals type 2 function in 8-year leukaemia remission`
   - Journal: `Nature` (2024)
   - Signal from paper: single-cell multi-omics atlas of `695,819` pre-infusion CAR-T cells from `82` pediatric patients plus `6` donors, basal and CAR-stimulated conditions.
   - Method signature: clinical multi-condition cohort -> single-cell multi-omics -> persistence-group comparison -> state program discovery.
   - URL: <https://www.nature.com/articles/s41586-024-07762-w>

### Focused mechanism / progression papers

6. `Single-cell and bulk transcriptomics uncovers PRKD2-driven tumor stemness and progression in multiple myeloma`
   - Journal: `Scientific Reports` (2025)
   - Signal from paper: integrated single-cell plus bulk transcriptomics; pseudotime; WGCNA; enrichment; immune deconvolution; drug sensitivity; knockdown / overexpression validation.
   - Method signature: nominate target gene -> show single-cell expression pattern -> relate to trajectory / stemness / immune context -> validate with orthogonal data and experiments.
   - URL: <https://www.nature.com/articles/s41598-025-20615-4>

7. `Single cell deciphering of progression trajectories of the tumor ecosystem in head and neck cancer`
   - Journal: `Nature Communications` (2024)
   - Signal from paper: scRNA-seq across normal, precancer, early-stage, advanced-stage, recurrent, and lymph-node samples; malignant epithelial trajectory; TFDP1-regulated tumorigenic subcluster.
   - Method signature: staged disease sampling -> trajectory inference across states -> malignant subcluster discovery -> TME co-evolution analysis.
   - URL: <https://www.nature.com/articles/s41467-024-46912-6>

8. `Comprehensive analysis of the tumor immune microenvironment in gastric cancer and peritoneal metastasis based on single-cell RNA sequencing analysis`
   - Journal: `Scientific Reports` (2025)
   - Signal from paper: scRNA-seq dissection of gastric cancer and peritoneal metastasis TME; highlighted `TAMs`, mast cells, and `CCL5-CCR1`.
   - Method signature: immune-focused reclustering -> abundance/state comparison -> communication axis prioritization -> survival association.
   - URL: <https://www.nature.com/articles/s41598-025-13892-6>

9. `Single-cell characterization of macrophages in uveal melanoma uncovers transcriptionally heterogeneous subsets conferring poor prognosis and aggressive behavior`
   - Journal: `Experimental & Molecular Medicine` (2023)
   - Signal from paper: `63,264` single-cell transcriptomes from `11` patients; four macrophage subsets; multicenter bulk and single-cell cohorts; RNA-seq and immunofluorescence validation.
   - Method signature: isolate one lineage -> recluster -> define subtype markers and programs -> connect subsets to prognosis and cohort-level phenotypes.
   - URL: <https://www.nature.com/articles/s12276-023-01115-9>

10. `Anaplastic transformation in thyroid cancer revealed by single-cell transcriptomics`
    - Journal: `JCI`
    - Signal from paper: combined single-cell transcriptomes, bulk transcriptomes, and targeted mutation data; `10X Genomics` 3' scRNA-seq for PTC, ATC, and adjacent normal tissues; transformation continuum and phenotype scoring.
    - Method signature: combine single-cell with bulk and mutation data -> build malignant continuum -> define phenotype scores -> compare immune and epithelial states along transformation.
    - URL: <https://www.jci.org/articles/view/169653>

## 4. Cross-Paper Common Method Skeleton

Most papers in the report can be rewritten with the same seven-slot structure:

1. `Samples and cohorts`
   - disease types, clinical groups, controls, metastatic or recurrent lesions, stimulation conditions, donor counts
2. `Assays`
   - scRNA-seq or single-cell multi-omics; sometimes spatial transcriptomics, imaging, bulk RNA-seq, mutation panels
3. `Preprocessing`
   - quality control, normalization, variable-gene selection, PCA, batch integration when needed
4. `Clustering and annotation`
   - UMAP/tSNE, graph clustering, marker-based annotation, focused reclustering for target compartments
5. `Theme-specific downstream analysis`
   - atlas: composition / diversity / subtype landscape
   - trajectory: pseudotime / lineage continuum
   - pathway: DEG, enrichment, module scoring, stemness / phenotype score
   - immune: checkpoint / state scoring, ligand-receptor analysis
   - spatial: mapping cell states to tissue coordinates
6. `Comparative statistics`
   - group-wise abundance shifts, score comparisons, survival / prognosis links, regression or correlation
7. `Validation`
   - bulk cohort replication, IHC / IF / mIHC, spatial confirmation, perturbation experiments, drug response

## 5. Archetype Templates for Writing Methods

### A. Atlas paper

Use when the figure logic is `global UMAP -> marker heatmap/dotplot -> composition bars -> optional spatial validation`.

Template cues:

- Collect multi-sample single-cell data across tissues, stages, or donor covariates.
- Perform QC, normalization, PCA, batch correction/integration if datasets come from multiple sources.
- Cluster cells on a joint embedding and annotate major compartments, then subcluster selected compartments.
- Quantify cell-type proportions, diversity, or state shifts across clinical or demographic groups.
- If available, validate with spatial transcriptomics, imaging, or orthogonal bulk data.

### B. Single-gene / pathway paper

Use when the figure logic is `FeaturePlot/Violin/heatmap -> correlation or score -> communication or pathway diagram`.

Template cues:

- Identify a candidate gene or pathway from differential or integrative analysis.
- Show cell-type or cluster-specific expression using FeaturePlot, violin, boxplot, or heatmap.
- Estimate functional scores such as stemness, differentiation, checkpoint, or pathway activity.
- Relate target expression to pseudotime, prognosis, drug sensitivity, or immune fractions.
- Add ligand-receptor or enrichment analysis if the claim extends from expression to mechanism.

### C. New subcluster discovery paper

Use when the figure logic is `recluster target lineage -> marker dotplot/heatmap -> fraction comparison`.

Template cues:

- Restrict to a lineage of interest such as malignant epithelial cells, macrophages, or T cells.
- Re-run dimensionality reduction and clustering within that lineage.
- Define subtype markers and state programs.
- Compare subtype abundance across stages, lesions, or outcomes.
- Link subclusters to prognosis, metastasis, or transition states.

### D. Trajectory paper

Use when the figure logic is `staged sampling -> pseudotime tree/continuum -> branch genes`.

Template cues:

- Order cells along a developmental, malignant, or treatment-response continuum.
- Infer branch structure and identify branch- or pseudotime-associated genes.
- Combine trajectory placement with phenotype or pathway scores.
- Interpret specific subclusters as transition or endpoint states.

### E. Immune microenvironment / communication paper

Use when the figure logic is `immune UMAP -> abundance change -> ligand-receptor or checkpoint readout`.

Template cues:

- Separate immune lineages or TME components after global annotation.
- Compare immune-cell abundance, exhaustion, activation, macrophage polarization, or mast-cell enrichment across groups.
- Run ligand-receptor tools such as `CellChat`, `NicheNet`, `CellPhoneDB`, or equivalent logic.
- Prioritize signaling axes by both interaction strength and clinical relevance.

### F. Spatial integration paper

Use when the figure logic is `global atlas + tissue map`.

Template cues:

- Build a single-cell reference first.
- Map annotated cell states onto Visium or Slide-seq coordinates.
- Use spatial plots to confirm niche localization, injured states, or microenvironment interactions.
- Keep assay-specific preprocessing explicit, because spatial workflows are usually version-sensitive.

### G. Clinical multi-omic atlas paper

Use when the figure logic is `clinical grouping + multi-condition single-cell profile + outcome association`.

Template cues:

- Define the cohort and pre-analytic grouping clearly.
- Model multiple assay conditions together, such as basal vs stimulated or transcriptome plus protein / accessibility.
- Compare states linked to persistence, response, relapse, or long-term remission.
- Avoid collapsing this route into a plain scRNA pipeline; the cohort design is part of the method.

## 6. Figure-to-Method Reverse Mapping

When the user only gives figure ideas, infer the minimum method chain:

| Figure type | Usually implies |
|---|---|
| UMAP / tSNE clusters | QC -> normalized expression matrix -> PCA/integration -> graph clustering |
| Marker heatmap / dotplot | differential marker testing and annotation |
| Violin / boxplot of genes or scores | score calculation or expression extraction plus group comparison |
| Stacked bar / composition plot | per-sample cell-type fractions and statistical comparison |
| Pseudotime curve / tree | lineage inference and dynamic gene analysis |
| Chord / network / bubble communication plot | ligand-receptor database-based communication analysis |
| Spatial spot map | spatial assay preprocessing plus label transfer or mapping |

## 7. Writing Rules for This Skill

- Prefer literature-grounded wording such as `single-cell atlas`, `trajectory inference`, `cell-cell communication analysis`, `spatial mapping`, and `orthogonal validation`.
- Only include software names and versions when the user wants a reproducible protocol or when the assay is especially tool-sensitive.
- If the request is for a manuscript section, convert the chosen archetype into a tight paragraph rather than a tool list.
- If the request is for a methods plan, keep the seven-slot skeleton explicit.
