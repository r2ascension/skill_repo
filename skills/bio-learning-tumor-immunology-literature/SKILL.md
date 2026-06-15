---
name: bio-learning-tumor-immunology-literature
description: Cross-source learning skill for tumor immunology paper reading, interpretation, and single-cell-informed immunology study digestion. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# bio-learning-tumor-immunology-literature

Use this skill when the user wants a maintained learning map for tumor immunology literature reading and interpretation, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/bio-learning-tumor-immunology-literature-catalog-latest.md](references/bio-learning-tumor-immunology-literature-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: tumor immunology literature reading and interpretation
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
- Route broader follow-up questions into `literature-workflows-router`.

## Resources

- [references/bio-learning-tumor-immunology-literature-catalog-latest.md](references/bio-learning-tumor-immunology-literature-catalog-latest.md)
  - current cross-source functional catalog
- `references/bio-learning-tumor-immunology-literature-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和肿瘤免疫论文阅读有关的学习内容
- 找适合肿瘤免疫单细胞文献消化的技能
