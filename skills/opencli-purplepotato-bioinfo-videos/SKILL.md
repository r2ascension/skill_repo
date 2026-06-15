---
name: opencli-purplepotato-bioinfo-videos
description: Curate, refresh, and summarize Bilibili videos from `小紫薯PurplePotato` that are about bioinformatics plus adjacent AI, R, and Linux foundations that directly support medical or bioinformatics beginners. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-purplepotato-bioinfo-videos

Use this skill when the user wants a maintained map of `小紫薯PurplePotato` videos that are specifically relevant to bioinformatics plus adjacent AI, R, and Linux foundations that directly support medical or bioinformatics beginners.

## Quick Start

- Start from [references/purplepotato-bioinfo-videos-video-map-2026-06-15.md](references/purplepotato-bioinfo-videos-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 361123190 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep videos that directly cover bioinformatics workflow or that clearly support bioinformatics onboarding through AI coding, R, RStudio, Linux, RNA-seq, or single-cell practice
- Use the category split below when summarizing results:
- `AI Workflow For Bioinformatics Beginners`: Explains how to use AI coding or knowledge-workflow tools to support bioinformatics or medical-research beginners.
- `R And Linux Foundations`: Covers the setup or basic workflow foundations that a bioinformatics beginner needs before analysis work.
- `RNA-Seq And Single-Cell Practice`: Directly teaches RNA-seq, transcriptomics, or single-cell analysis workflow.
- Respect this boundary rule: exclude general medical-research statistics or PhD-application videos unless they directly support the scoped bioinformatics workflow.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `小紫薯PurplePotato`
   - UID: `361123190`
   - space URL: `https://space.bilibili.com/361123190`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 361123190 --limit 50 --page N -f json`
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

- [references/purplepotato-bioinfo-videos-video-map-2026-06-15.md](references/purplepotato-bioinfo-videos-video-map-2026-06-15.md)
  - current curated snapshot
- `references/purplepotato-bioinfo-videos-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理小紫薯PurplePotato所有关于生信的视频
- 列出小紫薯PurplePotato关于 RNA-seq、单细胞、R 和 Linux 的视频
- refresh 小紫薯PurplePotato 里跟 AI 辅助生信学习相关的视频清单
