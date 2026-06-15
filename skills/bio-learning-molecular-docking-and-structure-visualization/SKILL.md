---
name: bio-learning-molecular-docking-and-structure-visualization
description: Cross-source learning skill for molecular docking, docking setup, and structure visualization with PyMOL or related tooling. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# bio-learning-molecular-docking-and-structure-visualization

Use this skill when the user wants a maintained learning map for molecular docking and structure visualization, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/bio-learning-molecular-docking-and-structure-visualization-catalog-latest.md](references/bio-learning-molecular-docking-and-structure-visualization-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: molecular docking and structure visualization
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

- [references/bio-learning-molecular-docking-and-structure-visualization-catalog-latest.md](references/bio-learning-molecular-docking-and-structure-visualization-catalog-latest.md)
  - current cross-source functional catalog
- `references/bio-learning-molecular-docking-and-structure-visualization-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和分子对接、PyMOL 结构可视化有关的学习内容
- 找适合分子对接流程学习的技能
