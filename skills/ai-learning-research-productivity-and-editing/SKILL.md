---
name: ai-learning-research-productivity-and-editing
description: Cross-source learning skill for editing, office productivity, and AI-assisted everyday research workflow. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# ai-learning-research-productivity-and-editing

Use this skill when the user wants a maintained learning map for editing, office productivity, and AI-assisted research workflow, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/ai-learning-research-productivity-and-editing-catalog-latest.md](references/ai-learning-research-productivity-and-editing-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: editing, office productivity, and AI-assisted research workflow
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
- Route broader follow-up questions into `academic-writing-router`.

## Resources

- [references/ai-learning-research-productivity-and-editing-catalog-latest.md](references/ai-learning-research-productivity-and-editing-catalog-latest.md)
  - current cross-source functional catalog
- `references/ai-learning-research-productivity-and-editing-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和 AI 提效、编辑、办公流有关的学习内容
- 找适合科研生产力工具的技能
