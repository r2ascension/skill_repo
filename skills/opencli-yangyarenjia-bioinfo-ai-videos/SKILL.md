---
name: opencli-yangyarenjia-bioinfo-ai-videos
description: Curate, refresh, and summarize Bilibili videos from `养鸭人家` that are about AI-enabled research workflow, DeepSeek, AI-assisted data analysis, scientific writing, and broader bioinformatics-adjacent research productivity. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-yangyarenjia-bioinfo-ai-videos

Use this skill when the user wants a maintained map of `养鸭人家` videos that are specifically relevant to AI-enabled research workflow, DeepSeek, AI-assisted data analysis, scientific writing, and broader bioinformatics-adjacent research productivity.

## Quick Start

- Start from [references/yangyarenjia-bioinfo-ai-videos-video-map-2026-06-15.md](references/yangyarenjia-bioinfo-ai-videos-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 631273618 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep videos that directly teach AI tools for data analysis, scientific research, writing, project management, DeepSeek practice, or adjacent open-science workflow; keep any explicit bioinformatics items that appear in future refreshes
- Use the category split below when summarizing results:
- `AI Tools And Practical Workflow`: Focuses on concrete AI tools, practical workflow, coding, or data-analysis enablement.
- `Research Writing And Project Workflow`: Explains how AI supports paper writing, research design, project management, or full research workflow.
- `Productivity, Editing, And AI Literacy`: Covers productivity, publishing, information service, editing, or AI literacy for research-adjacent work.
- Respect this boundary rule: this channel skews broader than strict bioinformatics; keep the AI-for-research core and note explicitly when a kept video is bioinformatics-adjacent rather than a wet-lab or omics tutorial.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `养鸭人家`
   - UID: `631273618`
   - space URL: `https://space.bilibili.com/631273618`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 631273618 --limit 50 --page N -f json`
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

- [references/yangyarenjia-bioinfo-ai-videos-video-map-2026-06-15.md](references/yangyarenjia-bioinfo-ai-videos-video-map-2026-06-15.md)
  - current curated snapshot
- `references/yangyarenjia-bioinfo-ai-videos-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理养鸭人家所有关于生信、AI的视频
- 列出养鸭人家关于 DeepSeek、AI 编程、AI 科研写作和数据分析的视频
- refresh 养鸭人家最新的 AI for research 视频清单
