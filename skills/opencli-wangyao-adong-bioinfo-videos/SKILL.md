---
name: opencli-wangyao-adong-bioinfo-videos
description: Curate, refresh, and summarize Bilibili videos from `网药阿东` that are about bioinformatics, network pharmacology, enrichment analysis, PPI-network construction, Cytoscape workflow, and molecular docking. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-wangyao-adong-bioinfo-videos

Use this skill when the user wants a maintained map of `网药阿东` videos that are specifically relevant to bioinformatics, network pharmacology, enrichment analysis, PPI-network construction, Cytoscape workflow, and molecular docking.

## Quick Start

- Start from [references/wangyao-adong-bioinfo-videos-video-map-2026-06-15.md](references/wangyao-adong-bioinfo-videos-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 3546805061028473 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep the full current channel because the uploaded series is already a tightly scoped network-pharmacology and bioinformatics tutorial line
- Use the category split below when summarizing results:
- `Active Components And Databases`: Focuses on how to retrieve active components, map disease or target resources, or use the relevant network-pharmacology databases.
- `PPI And Cytoscape`: Covers target-network construction, Cytoscape setup, STRING or PPI workflow, and related graph-building steps.
- `Enrichment And Visualization`: Explains GO or KEGG enrichment analysis, enrichment visualization, or related pathway-interpretation workflow.
- `Molecular Docking`: Covers docking environment setup, docking execution, and PyMOL or related structural visualization.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `网药阿东`
   - UID: `3546805061028473`
   - space URL: `https://space.bilibili.com/3546805061028473`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 3546805061028473 --limit 50 --page N -f json`
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

- [references/wangyao-adong-bioinfo-videos-video-map-2026-06-15.md](references/wangyao-adong-bioinfo-videos-video-map-2026-06-15.md)
  - current curated snapshot
- `references/wangyao-adong-bioinfo-videos-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理网药阿东所有关于生信和网络药理的视频
- refresh 网药阿东的最新网络药理和分子对接视频清单
- 列出网药阿东关于 Cytoscape、PPI、GO/KEGG 和分子对接的视频
