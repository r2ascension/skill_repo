---
name: opencli-mango-bioinfo-videos
description: Curate, refresh, and summarize Bilibili videos from `芒果大学Mango` that are about bioinformatics, GEO or TCGA mining, single-cell workflow, online analysis platforms, enrichment, limma, and practical omics tutorials. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-mango-bioinfo-videos

Use this skill when the user wants a maintained map of `芒果大学Mango` videos that are specifically relevant to bioinformatics, GEO or TCGA mining, single-cell workflow, online analysis platforms, enrichment, limma, and practical omics tutorials.

## Quick Start

- Start from [references/mango-bioinfo-videos-video-map-2026-06-15.md](references/mango-bioinfo-videos-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 630252799 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep videos that explicitly teach bioinformatics analysis, online omics platforms, single-cell practice, GEO or TCGA workflows, Linux mapping, or practical data-analysis strategy
- Use the category split below when summarizing results:
- `Bioinformatics Strategy And Practice`: Focuses on bioinformatics learning strategy, practical project framing, or integrated omics-analysis workflow.
- `GEO And TCGA Workflows`: Covers public-dataset mining, chip or bulk-expression processing, TCGA access, or downstream GEO/TCGA workflow.
- `Single-Cell And Online Platforms`: Explains single-cell analysis, database-driven online exploration, or the supporting platform workflow around those tasks.
- `Practical Omics Foundations`: Covers foundational practical steps such as mapping, enrichment, or immunology-oriented omics analysis.
- Respect this boundary rule: exclude wet-lab-only experimental reports and general pathology lectures unless they are clearly tied back to a bioinformatics workflow or online analysis platform.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `芒果大学Mango`
   - UID: `630252799`
   - space URL: `https://space.bilibili.com/630252799`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 630252799 --limit 50 --page N -f json`
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

- [references/mango-bioinfo-videos-video-map-2026-06-15.md](references/mango-bioinfo-videos-video-map-2026-06-15.md)
  - current curated snapshot
- `references/mango-bioinfo-videos-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理芒果大学Mango所有关于生信的视频
- 列出芒果大学Mango里关于 GEO、TCGA、单细胞、Seurat 和 TIMER 的视频
- refresh 芒果大学Mango 的最新生信实战视频清单
