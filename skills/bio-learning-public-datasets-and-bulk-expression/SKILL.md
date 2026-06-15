---
name: bio-learning-public-datasets-and-bulk-expression
description: Cross-source learning skill for GEO, TCGA, microarray, bulk RNA-seq, and public-expression dataset mining workflows. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# bio-learning-public-datasets-and-bulk-expression

Use this skill when the user wants a maintained learning map for public datasets, GEO, TCGA, microarray, and bulk-expression workflows, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/bio-learning-public-datasets-and-bulk-expression-catalog-latest.md](references/bio-learning-public-datasets-and-bulk-expression-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: public datasets, GEO, TCGA, microarray, and bulk-expression workflows
- Prefer concrete operational items over broad channel or album summaries.
- If a source item is only title-derived, keep the note conservative and source-grounded.

## Workflow

1. Read the latest cross-source reference catalog in `references/`.
2. If the user asks for latest content, refresh the underlying source skills first.
3. Rebuild the functional skills from the refreshed source indexes.
4. Answer with a concise task-oriented checklist instead of a creator-by-creator dump.

## Reporting Rules

- State whether the answer comes from the cached functional catalog or a fresh rebuild.
- Mention when an item is grouped by title/summary evidence rather than full article or full video details.
- Route broader follow-up questions into `bulk-rnaseq-router`.

## Resources

- [references/bio-learning-public-datasets-and-bulk-expression-catalog-latest.md](references/bio-learning-public-datasets-and-bulk-expression-catalog-latest.md)
  - current cross-source functional catalog
- `references/bio-learning-public-datasets-and-bulk-expression-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和 GEO、TCGA、bulk RNA-seq 有关的学习内容
- 找适合公共数据挖掘和 bulk 表达分析的技能
