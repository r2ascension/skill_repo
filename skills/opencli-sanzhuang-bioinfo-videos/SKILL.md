---
name: opencli-sanzhuang-bioinfo-videos
description: Curate, refresh, and summarize Bilibili videos from `散装生信散哥` that are about bioinformatics, single-cell, GEO, TCGA, RNA-seq, immune infiltration, survival analysis, and R-based omics visualization. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-sanzhuang-bioinfo-videos

Use this skill when the user wants a maintained map of `散装生信散哥` videos that are specifically relevant to bioinformatics, single-cell, GEO, TCGA, RNA-seq, immune infiltration, survival analysis, and R-based omics visualization.

## Quick Start

- Start from [references/sanzhuang-bioinfo-videos-video-map-2026-06-15.md](references/sanzhuang-bioinfo-videos-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 280749894 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep videos that directly teach bioinformatics analysis, especially single-cell, GEO or TCGA, enrichment, immune infiltration, survival modeling, or supporting R visualization code
- Use the category split below when summarizing results:
- `Single-Cell Workflow`: Covers single-cell data loading, Seurat workflow, clustering, scoring, or differential analysis.
- `GEO, TCGA, And RNA-Seq`: Focuses on public-dataset mining, RNA-seq processing, GEO or TCGA workflows, and related bulk-expression steps.
- `Immune, Enrichment, And Survival`: Explains immune infiltration, enrichment analysis, or survival-model workflow.
- Respect this boundary rule: include plotting or table-format tutorials only when they are clearly attached to a bioinformatics analysis workflow.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `散装生信散哥`
   - UID: `280749894`
   - space URL: `https://space.bilibili.com/280749894`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 280749894 --limit 50 --page N -f json`
4. Prefer a concise grouped checklist in the final answer:
   - title
   - date
   - BVID or URL
   - one short relevance note
5. When the user says `latest`, do a live refresh instead of trusting the cached snapshot.

## Reporting Rules

- State the snapshot date explicitly.
- Mention the channel scope used for inclusion.
- Say when an answer comes from the cached reference file versus a fresh refresh.
- If the user wants more depth on one video, inspect that BVID with `opencli bilibili video`, `summary`, or `subtitle`.

## Resources

- [references/sanzhuang-bioinfo-videos-video-map-2026-06-15.md](references/sanzhuang-bioinfo-videos-video-map-2026-06-15.md)
  - current curated snapshot
- `references/sanzhuang-bioinfo-videos-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理散装生信散哥所有关于生信的视频
- 列出散装生信散哥关于单细胞、GEO、TCGA、GSVA 和生存分析的视频
- refresh 散装生信散哥的最新生信实战视频清单
