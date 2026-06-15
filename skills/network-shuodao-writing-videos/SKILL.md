---
name: network-shuodao-writing-videos
description: Collect, regroup, and summarize Bilibili videos from the UP 主 `网络硕导` that relate to thesis writing, literature review, topic selection, proposal writing, formatting, citations, AIGC reduction, questionnaires or interview outlines, and defense PPTs. Use when Codex needs to audit this UP's writing-course inventory, answer what a given video covers, refresh the current list via `opencli`, or turn these videos into a reusable checklist or report.
---

# Network Shuodao Writing Videos

## Overview

Use this skill to turn `opencli bilibili` output into a usable writing-course inventory for the UP 主 `网络硕导`. Prefer it when the user wants a current grouped list, a quick topic map, or a refreshable local snapshot rather than one-off manual browsing.

## Quick Start

- Confirm `opencli` is callable with `opencli --help`.
- If `opencli` reports `Pre-navigation ... This operation was aborted`, run `opencli daemon status` and then `opencli daemon restart` before retrying.
- Refresh the snapshot with:

```powershell
E:\ProgramData\anaconda3\python.exe -X utf8 `
  C:\Users\simon\.codex\skills\network-shuodao-writing-videos\scripts\refresh_catalog.py `
  --max-pages 3 `
  --max-detailed-topics 12 `
  --reference-dir C:\Users\simon\.codex\skills\network-shuodao-writing-videos\references
```

- The generated working files land in `E:\codex\network-shuodao-writing-videos\`.
- The skill-local copies land in `references/network_shuodao_writing_catalog.md` and `references/network_shuodao_writing_catalog.json`.

## Workflow

1. Resolve the creator.
   Use `opencli bilibili search "网络硕导" --type user`.
   The current UID in this snapshot is `189717004`.
2. Pull the video inventory.
   Use `opencli bilibili user-videos 189717004 --page <n> --limit 50`.
   Current data fit within pages `1-3`.
3. Keep only writing-related items.
   Include thesis-writing course videos, beginner formatting/citation videos, questionnaire/interview videos, writing tools, and defense-PPT videos.
4. Regroup the list by theme.
   Prefer the buckets in `references/curated_overview.md`: 主线课程, 案例写法拓展, 小白扫盲与格式规范, 工具与答辩, 论文反诈与避坑.
5. Prefer stronger evidence when available.
   If a video has B 站 AI 总结, use `opencli bilibili summary <bvid>`.
   If not, summarize from the title and, when necessary, the subtitle opening via `opencli bilibili subtitle <bvid>`.
6. State confidence clearly.
   Mark whether a note is based on AI summary, subtitle opening, or title-level inference.

## References

- Read `references/curated_overview.md` first when the user wants a human-readable guide.
- Read `references/network_shuodao_writing_catalog.md` when the user wants the full grouped checklist.
- Read `references/network_shuodao_writing_catalog.json` when the user wants structured exports or regrouping.
- Read `references/notes.md` for the local file roles.

## Guardrails

- Treat the catalog as a dated snapshot, not a timeless truth. Mention the snapshot date when answering.
- Keep "all videos" separate from "grouped topics": this UP has repeated dry-run, 碎碎念, and重制 versions for the same lesson.
- Do not overclaim the contents of videos that lack AI summary. Use wording such as "based on the title/course position" or "from subtitle opening".
- Default report output stays under `E:\codex\`.
