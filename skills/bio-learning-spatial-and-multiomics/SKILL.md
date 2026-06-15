---
name: bio-learning-spatial-and-multiomics
description: Cross-source learning skill for spatial transcriptomics, multiomics integration, scATAC, velocity-adjacent, and multimodal analysis learning. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# bio-learning-spatial-and-multiomics

Use this skill when the user wants a maintained learning map for spatial transcriptomics, multiomics, and multimodal analysis, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/bio-learning-spatial-and-multiomics-catalog-latest.md](references/bio-learning-spatial-and-multiomics-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: spatial transcriptomics, multiomics, and multimodal analysis
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
- Route broader follow-up questions into `bioinformatics-router`.

## Resources

- [references/bio-learning-spatial-and-multiomics-catalog-latest.md](references/bio-learning-spatial-and-multiomics-catalog-latest.md)
  - current cross-source functional catalog
- `references/bio-learning-spatial-and-multiomics-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和空间转录组、多组学、多模态有关的学习内容
- 找适合空间和多组学分析学习的技能
