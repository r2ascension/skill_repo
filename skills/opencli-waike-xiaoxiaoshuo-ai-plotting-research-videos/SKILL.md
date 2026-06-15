---
name: opencli-waike-xiaoxiaoshuo-ai-plotting-research-videos
description: Curate, refresh, and summarize Bilibili videos from `外科小小硕` that are about plotting, AI-assisted medical research workflow, Codex or ClaudeR usage, clinical prediction-model methods, and research-process tutorials. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-waike-xiaoxiaoshuo-ai-plotting-research-videos

Use this skill when the user wants a maintained map of `外科小小硕` videos that are specifically relevant to plotting, AI-assisted medical research workflow, Codex or ClaudeR usage, clinical prediction-model methods, and research-process tutorials.

## Quick Start

- Start from [references/waike-xiaoxiaoshuo-ai-plotting-research-videos-video-map-2026-06-15.md](references/waike-xiaoxiaoshuo-ai-plotting-research-videos-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 277408458 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep videos about plotting, AI tools for analysis or writing, Codex or ClaudeR workflow, prediction-model methodology, or broader research-method execution
- Use the category split below when summarizing results:
- `AI Workflow And Coding Agents`: Explains how AI tools, coding agents, or model-assisted workflow can support medical research execution.
- `Plotting And Visualization`: Focuses on figure making, layout, beautification, or other research-visualization workflow.
- `Research Methods And Writing`: Covers research-method execution, reporting guidance, journal-formatting, or model-building workflow.
- Respect this boundary rule: exclude casual commentary unless it contains concrete reusable workflow guidance for AI, plotting, or research methods.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `外科小小硕`
   - UID: `277408458`
   - space URL: `https://space.bilibili.com/277408458`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 277408458 --limit 50 --page N -f json`
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

- [references/waike-xiaoxiaoshuo-ai-plotting-research-videos-video-map-2026-06-15.md](references/waike-xiaoxiaoshuo-ai-plotting-research-videos-video-map-2026-06-15.md)
  - current curated snapshot
- `references/waike-xiaoxiaoshuo-ai-plotting-research-videos-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理外科小小硕所有关于绘图、AI、研究方法的视频
- 列出外科小小硕关于 Codex、ClaudeR、预测模型写作和科研绘图的视频
- refresh 外科小小硕最新的 AI 医学科研工作流视频清单
