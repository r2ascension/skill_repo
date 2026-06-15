---
name: opencli-weixin-album-router
description: Router for opencli-backed Weixin album skills. Use when the user provides one or more Weixin album links or asks for a maintained catalog of article collections from specific Weixin albums and you need to choose the right album-specific skill.
---

# opencli-weixin-album-router

Use this router when the task is about one of the maintained Weixin article albums rather than a single standalone article.

## Album Skills

- `opencli-weixin-album-bioinfo-software-series`
- `opencli-weixin-album-ai-frontier-bioinfo-ai`
- `opencli-weixin-album-ai-or-ai-fail`
- `opencli-weixin-album-bioinfo-analysis`
- `opencli-weixin-album-monthly-single-cell`
- `opencli-weixin-album-biomuse-tumor-immunity-notes`
- `opencli-weixin-album-single-cell-advanced`

## Routing guidance

- Use `opencli-weixin-album-ai-frontier-bioinfo-ai` for AI frontier, RAG, MCP, Biomni, agent systems, or AI-for-science articles.
- Use `opencli-weixin-album-ai-or-ai-fail` for practical AI-coding, prompt engineering, and automation pitfall articles.
- Use `opencli-weixin-album-bioinfo-analysis`, `opencli-weixin-album-monthly-single-cell`, or `opencli-weixin-album-single-cell-advanced` for bioinformatics and single-cell tutorial collections.
- Use `opencli-weixin-album-biomuse-tumor-immunity-notes` for tumor-immunity and paper-note collections.
- Use `opencli-weixin-album-bioinfo-software-series` when the album is software-oriented and tool-heavy.
- Use `opencli-learning-content-router` as the broader parent entry when the user has not yet decided between Bilibili and Weixin source collections.

## Maintenance

- Refresh a leaf skill with its own `scripts/refresh_index.py`.
- Use `opencli weixin download --url <article-url>` only for the specific articles whose full Markdown is needed.
