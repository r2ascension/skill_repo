---
name: academic-learning-postgraduate-application-and-interview-prep
description: Cross-source learning skill for postgraduate application, mentor selection, personal statements, interview preparation, and related academic progression planning. Use this when the user wants content organized by concrete function rather than by creator or album source.
---

# academic-learning-postgraduate-application-and-interview-prep

Use this skill when the user wants a maintained learning map for postgraduate application, interview preparation, and academic progression planning, aggregated across multiple opencli-derived sources.

## Quick Start

- Start from [references/academic-learning-postgraduate-application-and-interview-prep-catalog-latest.md](references/academic-learning-postgraduate-application-and-interview-prep-catalog-latest.md) for the current cross-source skill map.
- Refresh source-specific indexes first when needed, then rebuild this functional skill with `python E:\AI\codex\build_opencli_functional_skills.py`.

## Scope Rules

- Keep the skill tightly scoped to this function: postgraduate application, interview preparation, and academic progression planning
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

- [references/academic-learning-postgraduate-application-and-interview-prep-catalog-latest.md](references/academic-learning-postgraduate-application-and-interview-prep-catalog-latest.md)
  - current cross-source functional catalog
- `references/academic-learning-postgraduate-application-and-interview-prep-items-latest.json`
  - machine-readable item list and source evidence

## Example Prompts

- 整理和考研复试、个人陈述、选导师有关的学习内容
- 找适合保研直博和复试准备的技能
