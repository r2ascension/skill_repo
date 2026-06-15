---
name: academic-learning-research-methods-and-writing
description: Cross-source learning skill for research methods, study framing, manuscript workflow, and project-level research writing practice. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# academic-learning-research-methods-and-writing

Use this skill when the user wants a maintained learning map for research methods, study design, writing workflow, and project framing, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/academic-learning-research-methods-and-writing-catalog-latest.md](references/academic-learning-research-methods-and-writing-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: research methods, study design, writing workflow, and project framing
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

- [references/academic-learning-research-methods-and-writing-catalog-latest.md](references/academic-learning-research-methods-and-writing-catalog-latest.md)
  - current cross-source functional catalog
- `references/academic-learning-research-methods-and-writing-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和研究方法、论文写作、项目流程有关的学习内容
- 找适合科研写作和研究设计入门的技能
