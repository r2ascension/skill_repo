---
name: fangyangren-paper-writing-index
description: Source-specific index and digest for the Bilibili creator Fangyangren. Use when the user wants to organize, recall, filter, summarize, or locate this creator's paper-writing videos, or wants creator-specific advice on literature review, introduction, abstract, methodology, results and discussion, innovation points, topic selection, proposal writing, thesis revision, peer review, journal selection, or AI-assisted writing. Prefer this skill for source-grounded recall and indexing; if the task shifts to drafting a new manuscript, route to `scientific-writing` or `nature-writing`.
---

# Fangyangren Paper Writing Index

## Overview

Use this skill as a source-grounded index for Fangyangren rather than as a generic manuscript-writing guide. The underlying index was captured on 2026-06-14 with `opencli` from Bilibili UID `508455218`.

## Quick Start

- Start with `references/video-index.md` to find the relevant theme, date, and BV id.
- Read `references/topic-digest.md` for the merged recurring advice across repeated videos.
- Read `references/all-video-details.md` when the user wants per-video detail across the full corpus.
- Use `references/representative-summaries.md` when a shorter representative set is enough.

## Workflow

1. Identify the request shape:
   - theme overview
   - brief checklist
   - exact video lookup
   - detailed source-grounded summary
2. For theme overviews or list requests:
   - scan `references/video-index.md`
   - group the answer by theme
   - preserve `date + BV id + title` when possible
3. For detailed-content requests:
   - check `references/all-video-details.md`
   - merge repeated points across nearby videos into one consolidated summary
   - cite representative BV ids instead of repeating every overlapping title
4. If the exact video is not covered well enough in the local detail files, refresh it live with `opencli`:

```powershell
opencli bilibili user-videos 508455218 --limit 100 --page 1 -f json
opencli bilibili summary <BV> -f yaml
opencli bilibili subtitle <BV> -f yaml
opencli bilibili video <BV> -f yaml
```

5. Use the fallback order:
   - `summary`
   - `subtitle`
   - `video` metadata plus title-only inference

## Reference Map

- `references/video-index.md`: full curated writing-video index grouped by theme
- `references/topic-digest.md`: merged recurring lessons and practical takeaways
- `references/all-video-details.md`: 154 writing-related videos with summary or subtitle fallback
- `references/representative-summaries.md`: 39 representative videos for faster review

## Output Rules

- Separate the video list from the core takeaways.
- Prefer repeated cross-video advice over one-off marketing or testimonial framing.
- Mark weak evidence explicitly when only title or metadata was available.
- Preserve the creator-specific framing instead of silently rewriting it into generic academic advice.

## Guardrails

- Do not treat this as a universal best-practice writing manual; it is a creator-specific corpus.
- Do not overclaim precision for videos that had no official AI summary and no usable subtitle.
- If the user wants to actually draft, revise, or submit a manuscript, hand off after retrieval to `scientific-writing`, `nature-writing`, or another appropriate writing skill.
