---
name: opencli-weixin-album-bioinfo-software-series
description: Curate, refresh, and summarize the Weixin album `` from `` that is about bioinformatics software tutorials, single-cell or multi-omics tools, RNA velocity, scATAC, and practical analysis software walkthroughs. Use when Codex needs the current article catalog for this specific Weixin album, wants a concise reading checklist, or wants the result preserved as a reusable local skill instead of a one-off chat answer.
---

# opencli-weixin-album-bioinfo-software-series

Use this skill when the user wants a maintained map of the Weixin album `` from ``.

## Quick Start

- Start from [references/weixin-album-bioinfo-software-series-album-map-2026-06-15.md](references/weixin-album-bioinfo-software-series-album-map-2026-06-15.md) for the latest curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest album state.
- Use `opencli weixin download --url <article-url>` when the user wants full article Markdown for a specific entry.

## Scope Rules

- Keep the album within this scope: treat the whole album as in-scope because the album itself is already a curated software series from 生信宝库
- Use these buckets when summarizing the article list:
- `Single-Cell And Multi-Omics Software`: Focuses on single-cell or multi-omics software workflows, especially analysis tool introductions and hands-on tutorials.
- `Drug Discovery And Screening Tools`: Highlights practical tools or workflows for drug screening, drug discovery, or related computational pipelines.
- `Method And General Software Tutorials`: Covers method-oriented software introductions and practical walkthroughs that do not fit a narrower bucket.

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

- [references/weixin-album-bioinfo-software-series-album-map-2026-06-15.md](references/weixin-album-bioinfo-software-series-album-map-2026-06-15.md)
  - current curated snapshot
- `references/weixin-album-bioinfo-software-series-articles-latest.json`
  - machine-readable latest article catalog
- `scripts/refresh_index.py`
  - refreshes the album metadata and article list
