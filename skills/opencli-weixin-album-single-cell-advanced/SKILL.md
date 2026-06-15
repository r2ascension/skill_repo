---
name: opencli-weixin-album-single-cell-advanced
description: Curate, refresh, and summarize the Weixin album `` from `` that is about advanced single-cell practice, multiplexing, sample hashing, comparative group design, integration, and deeper single-cell analysis tactics. Use when Codex needs the current article catalog for this specific Weixin album, wants a concise reading checklist, or wants the result preserved as a reusable local skill instead of a one-off chat answer.
---

# opencli-weixin-album-single-cell-advanced

Use this skill when the user wants a maintained map of the Weixin album `` from ``.

## Quick Start

- Start from [references/weixin-album-single-cell-advanced-album-map-2026-06-15.md](references/weixin-album-single-cell-advanced-album-map-2026-06-15.md) for the latest curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest album state.
- Use `opencli weixin download --url <article-url>` when the user wants full article Markdown for a specific entry.

## Scope Rules

- Keep the album within this scope: keep the full album because 单细胞进阶 is already a curated advanced single-cell collection from 生信技能树
- Use these buckets when summarizing the article list:
- `Experimental Design And Multiplexing`: Focuses on single-cell experimental design, multiplexing, and sample-handling tactics.
- `Comparison And Visualization`: Covers comparative analysis and visualization tactics across groups or cell subtypes.
- `Advanced Workflow Notes`: Captures advanced single-cell workflows and deeper analysis notes not covered by a narrower bucket.

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

- [references/weixin-album-single-cell-advanced-album-map-2026-06-15.md](references/weixin-album-single-cell-advanced-album-map-2026-06-15.md)
  - current curated snapshot
- `references/weixin-album-single-cell-advanced-articles-latest.json`
  - machine-readable latest article catalog
- `scripts/refresh_index.py`
  - refreshes the album metadata and article list
