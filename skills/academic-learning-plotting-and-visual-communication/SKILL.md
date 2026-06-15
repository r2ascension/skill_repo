---
name: academic-learning-plotting-and-visual-communication
description: Cross-source learning skill for plotting, figure styling, and turning analysis into readable visual communication artifacts. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# academic-learning-plotting-and-visual-communication

Use this skill when the user wants a maintained learning map for plotting, figures, and visual communication, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/academic-learning-plotting-and-visual-communication-catalog-latest.md](references/academic-learning-plotting-and-visual-communication-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: plotting, figures, and visual communication
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
- Route broader follow-up questions into `scientific-computing-router`.

## Resources

- [references/academic-learning-plotting-and-visual-communication-catalog-latest.md](references/academic-learning-plotting-and-visual-communication-catalog-latest.md)
  - current cross-source functional catalog
- `references/academic-learning-plotting-and-visual-communication-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和绘图、可视化表达有关的学习内容
- 找适合科研作图和图形表达的技能
