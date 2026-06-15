---
name: opencli-weixin-album-bioinfo-analysis
description: Curate, refresh, and summarize the Weixin album `` from `` that is about bioinformatics analysis practice, especially single-cell analysis, bulk RNA-seq, GSEA, GO or KEGG enrichment, and machine-learning workflow scripts. Use when Codex needs the current article catalog for this specific Weixin album, wants a concise reading checklist, or wants the result preserved as a reusable local skill instead of a one-off chat answer.
---

# opencli-weixin-album-bioinfo-analysis

Use this skill when the user wants a maintained map of the Weixin album `` from ``.

## Quick Start

- Start from [references/weixin-album-bioinfo-analysis-album-map-2026-06-15.md](references/weixin-album-bioinfo-analysis-album-map-2026-06-15.md) for the latest curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest album state.
- Use `opencli weixin download --url <article-url>` when the user wants full article Markdown for a specific entry.

## Scope Rules

- Keep the album within this scope: keep the whole album because 生信分析 is already a dedicated bioinformatics-analysis collection
- Use these buckets when summarizing the article list:
- `Single-Cell Analysis`: Covers single-cell analysis, cell-group comparisons, and practical visualization or interpretation work.
- `Bulk RNA-Seq And GSEA`: Focuses on bulk RNA-seq, single-gene GSEA, and related transcriptome workflows.
- `Enrichment And Machine Learning`: Highlights enrichment analysis and machine-learning or automated-model workflow.
- Respect this boundary rule: the album includes paid items; keep them listed as catalog entries but do not assume their full body can always be downloaded anonymously.

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

- [references/weixin-album-bioinfo-analysis-album-map-2026-06-15.md](references/weixin-album-bioinfo-analysis-album-map-2026-06-15.md)
  - current curated snapshot
- `references/weixin-album-bioinfo-analysis-articles-latest.json`
  - machine-readable latest article catalog
- `scripts/refresh_index.py`
  - refreshes the album metadata and article list
