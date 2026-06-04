---
name: biomamba-multimir-mirna
description: "Use only when the user mentions Biomamba, multiMiR, microRNA-靶标相互作用及疾病和药物关联分析, the provided HTML notes, or asks to reproduce that tutorial's query, filtering, network, or Sankey code. For generic small RNA-seq or miRNA target prediction prefer existing small-RNA skills."
---

# Biomamba multiMiR miRNA

## Scope

Use this skill for multiMiR database queries and visualization of miRNA target, disease, and drug associations.

Do not use it for small RNA-seq preprocessing, miRNA quantification, or differential miRNA expression. Those are separate sequencing workflows.

## Repository Fit

When using multiMiR inside `/home/h2048`:

- Keep reusable query or plotting code in `script/R` and save tables/plots under `data/R/<YYYYMMDD>/...`.
- Record the organism, database scope, and filtering decisions in `docs/experiments/WORKLOG-YYYYMMDD.md`, because those choices strongly affect interpretation.
- If the multiMiR output is only a downstream annotation step for bulk or scRNA results, keep the upstream DEG/marker workflow in its own skill and use this one only for the miRNA association layer.

## Workflow

1. Define whether the query starts from miRNAs, target genes, disease terms, or drug terms.
2. Choose validated, predicted, disease/drug, or all multiMiR table categories.
3. Run `get_multimir` or `get.multimir` with the correct organism.
4. Filter predictions by table, score, support count, or database source.
5. Export tables for review.
6. Visualize miRNA-target-disease-drug relationships with network, Sankey, or summary plots.

## References

Read `references/workflow.md` for query and visualization patterns.
Read `references/source-map.md` for source provenance.
