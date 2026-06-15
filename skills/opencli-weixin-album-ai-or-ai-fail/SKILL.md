---
name: opencli-weixin-album-ai-or-ai-fail
description: Curate, refresh, and summarize the Weixin album `` from `` that is about practical AI-assisted coding for research work, automation pitfalls, large-scale data handling, and how to keep AI from producing low-quality outputs. Use when Codex needs the current article catalog for this specific Weixin album, wants a concise reading checklist, or wants the result preserved as a reusable local skill instead of a one-off chat answer.
---

# opencli-weixin-album-ai-or-ai-fail

Use this skill when the user wants a maintained map of the Weixin album `` from ``.

## Quick Start

- Start from [references/weixin-album-ai-or-ai-fail-album-map-2026-06-15.md](references/weixin-album-ai-or-ai-fail-album-map-2026-06-15.md) for the latest curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest album state.
- Use `opencli weixin download --url <article-url>` when the user wants full article Markdown for a specific entry.

## Scope Rules

- Keep the album within this scope: keep the whole album because it is already curated as a practical AI-for-research series by 生信菜鸟团
- Use these buckets when summarizing the article list:
- `AI Coding Practice`: Focuses on hands-on AI coding practice, code-generation issues, and practical implementation workflow.
- `Data Handling And Scale`: Covers AI or workflow discussions tied to large data handling, scaling, or bioinformatics datasets.
- `Prompting And AI Usage Pitfalls`: Highlights prompting, failure modes, and usage patterns for making AI outputs more reliable.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Use `scripts/refresh_index.py` to re-fetch the album article list.
3. Read the generated Markdown reference for the grouped catalog.
4. If the user wants full content for one article, download only that article with `opencli weixin download`.
5. Prefer a concise grouped checklist in the final answer: title, date, URL, and one short relevance note.

## Reporting Rules

- State the snapshot date explicitly.
- Say whether the answer comes from the cached snapshot or a live refresh.
- If an article body was not downloaded, keep the summary title-derived and say so when needed.

## Resources

- [references/weixin-album-ai-or-ai-fail-album-map-2026-06-15.md](references/weixin-album-ai-or-ai-fail-album-map-2026-06-15.md)
  - current curated snapshot
- `references/weixin-album-ai-or-ai-fail-articles-latest.json`
  - machine-readable latest article catalog
- `scripts/refresh_index.py`
  - refreshes the album metadata and article list
