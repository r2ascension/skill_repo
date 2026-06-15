---
name: opencli-onekeyai-bioinfo-videos
description: Curate, refresh, and summarize OnekeyAI Bilibili videos that are relevant to bioinformatics-adjacent workflows, especially traditional omics, multi-omics, structured or tabular modeling, survival analysis, batch correction, cross-validation, clustering, and feature-fusion topics. Use when Codex needs to organize OnekeyAI's video library via `opencli bilibili`, produce a concise categorized checklist, or maintain a reusable skill-backed reference instead of a one-off list.
---

# opencli-onekeyai-bioinfo-videos

Use this skill when the user wants a working map of OnekeyAI videos that are close to bioinformatics or omics workflows, not the entire channel.

## Quick Start

- Start from [references/onekeyai-bioinfo-video-map-2026-06-14.md](references/onekeyai-bioinfo-video-map-2026-06-14.md) for the current curated snapshot.
- Refresh the candidate list with `scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili video <bvid> -f yaml` for per-video detail.
- If `video` metadata is sparse or suspicious, fall back to `opencli bilibili subtitle <bvid> -f yaml`.

## Scope Rules

- Keep the strict core list focused on videos that explicitly mention one or more of these themes in the title or content:
  - traditional omics or multi-omics
  - structured data, survival, or Cox modeling
  - Combat or batch correction
  - cross-validation, multiclass evaluation, or clustering
  - text modality when it is presented as a new omics-like modality
- Keep an extended bucket for foundation or helper videos that materially support the core workflow, such as:
  - older `OnekeyComp` traditional-omics overview videos
  - clustering or feature utility videos
  - multi-omics positioning or differentiation talks
- Exclude by default:
  - pure hardware or computer-buying advice
  - pure segmentation or ROI drawing tutorials
  - generic grant-trend or AIGC trend talks that are not tied back to omics workflow execution
  - pure Q and A videos unless they are specifically about a core omics component

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `OnekeyAI`
   - UID: `1948639457`
   - space URL: `https://space.bilibili.com/1948639457`
3. Pull the channel list with either:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 1948639457 --limit 50 --page N -f json`
4. Apply the scope rules above and split results into:
   - `core`
   - `extended`
5. For the final answer, prefer a concise categorized checklist:
   - title
   - date
   - BVID or URL
   - why it is relevant
   - one short content summary
6. When the user says `latest`, do a live refresh instead of trusting the snapshot.

## Reporting Rules

- State the snapshot date explicitly when using the reference file.
- Say when a video was included as a strict core item versus an extended or boundary item.
- Be careful with older Bilibili AI descriptions: some are noisy or generic. If the description looks wrong, trust the title, duration, chronology, and subtitle more than the generated blurb.
- If the user wants a truly exhaustive update, rerun the script and then spot-check new candidate videos with `video` and `subtitle`.

## Resources

- [references/onekeyai-bioinfo-video-map-2026-06-14.md](references/onekeyai-bioinfo-video-map-2026-06-14.md)
  - curated snapshot collected on `2026-06-14`
  - use for fast answers and continuity
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - writes candidate JSON and Markdown outputs for re-curation

## Example Prompts

- organize all OnekeyAI videos that are really about omics or bioinformatics
- refresh the latest OnekeyAI bioinfo-related videos and give me a short categorized checklist
- find the OnekeyAI videos about survival analysis, batch correction, and structured data, then summarize them
