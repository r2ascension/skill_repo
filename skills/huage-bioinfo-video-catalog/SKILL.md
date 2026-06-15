---
name: huage-bioinfo-video-catalog
description: Curated catalog and refresh workflow for Bilibili uploader `华哥生信AI` / `华哥生信官方` bioinformatics technique videos. Use when the user asks to list, group, summarize, compare, or recommend a learning order from this uploader's B站生信技术课程, wants the current video snapshot refreshed with `opencli`, or needs these videos organized into a reusable Codex skill.
---

# Huage Bioinfo Video Catalog

## Overview

- Use this skill to answer questions about `华哥生信AI` bioinformatics technique videos on Bilibili.
- Treat `references/current_catalog.md` as the cached snapshot.
- Refresh with `scripts/refresh_catalog.py` whenever the user asks for the latest/current list or when the cached snapshot is stale for the current session.

## Workflow

1. Read `references/current_catalog.md` first for the latest generated grouped catalog.
2. If the user asks for current/latest content, run:

```powershell
python scripts/refresh_catalog.py --profile <opencli-profile>
```

3. If `opencli` reports multiple Browser Bridge profiles, run `opencli profile list`, choose one connected profile, and re-run with `--profile`.
4. Default scope is "生信技术视频":
   - include workflow, environment, analysis, visualization, multi-omics, or article-reproduction content,
   - exclude obvious promo/account-intro uploads unless the user asks for all uploads.
5. When responding, prefer:
   - a compact grouped list first,
   - then a learning route from easy to advanced,
   - then task-matched recommendations for the user's goal.

## Output Rules

- State the snapshot date.
- Say whether the answer comes from the cached catalog or from a fresh `opencli` refresh.
- If non-technical videos were excluded, say so explicitly.

## Resources

- `references/current_catalog.md`: latest human-readable grouped catalog
- `references/current_catalog.json`: latest machine-readable snapshot
- `scripts/refresh_catalog.py`: refreshes the catalog from Bilibili with `opencli`
