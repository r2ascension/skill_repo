---
name: opencli-ai-ghost-lab-ai-skills
description: Curate, refresh, and summarize Bilibili videos from `AI-Ghost-Lab` that are about AI skills, prompts, AGENTS.md, Codex, subagents, project evolution, AI coding workflow, and reusable engineering practice. Use when Codex needs the current scoped video list through `opencli bilibili`, wants a concise learning checklist, or wants the result preserved as a reusable local skill instead of a one-off answer.
---

# opencli-ai-ghost-lab-ai-skills

Use this skill when the user wants a maintained map of `AI-Ghost-Lab` videos that are specifically relevant to AI skills, prompts, AGENTS.md, Codex, subagents, project evolution, AI coding workflow, and reusable engineering practice.

## Quick Start

- Start from [references/ai-ghost-lab-ai-skills-video-map-2026-06-15.md](references/ai-ghost-lab-ai-skills-video-map-2026-06-15.md) for the current curated snapshot.
- Refresh with `python scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili user-videos 1731330412 --limit 50 --page N -f json` as the live source on this machine.

## Scope Rules

- Keep videos that directly match the requested scope: keep videos that teach AI workflow, prompt strategy, skills, Codex or ChatGPT usage, subagent collaboration, architecture iteration, evaluation, or leverage through AI coding
- Use the category split below when summarizing results:
- `Skills, Prompts, And Collaboration`: Focuses on skills, prompt design, collaboration modes, AGENTS conventions, or subagent usage patterns.
- `AI Coding Workflow`: Explains AI coding pipelines, validation, testing, delivery flow, or operational execution design.
- `Architecture And Project Evolution`: Reflects on architecture, project evolution, or how to scale engineering leverage with AI assistance.
- Respect this boundary rule: exclude the older security, Hack The Box, CVE, or personal-life videos unless the user explicitly asks for the whole channel history.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `AI-Ghost-Lab`
   - UID: `1731330412`
   - space URL: `https://space.bilibili.com/1731330412`
3. Refresh the list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 1731330412 --limit 50 --page N -f json`
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

- [references/ai-ghost-lab-ai-skills-video-map-2026-06-15.md](references/ai-ghost-lab-ai-skills-video-map-2026-06-15.md)
  - current curated snapshot
- `references/ai-ghost-lab-ai-skills-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - rewrites the latest Markdown and JSON outputs

## Example Prompts

- 整理 AI-Ghost-Lab 所有关于 AI 技巧及技能的视频
- 列出 AI-Ghost-Lab 关于 Codex、AGENTS、prompt 和 subagent 的视频
- refresh AI-Ghost-Lab 的最新 AI coding workflow 视频清单
