---
name: opencli-omics-lecture-hall-bioinfo-videos
description: Curate, refresh, and summarize Bilibili videos from the creator `组学大讲堂` that are about bioinformatics, omics data handling, sequencing-data workflow, R statistics or visualization, Linux foundations for bioinformatics, GEO or SRA submission, WGCNA, gene-family analysis, and related practical tutorials. Use when Codex needs a current checklist of this creator's bioinformatics videos through `opencli bilibili`, or when the result should be preserved as a reusable skill instead of a one-off chat list.
---

# opencli-omics-lecture-hall-bioinfo-videos

Use this skill when the user wants a working map of `组学大讲堂` videos that are relevant to bioinformatics, not just a single ad hoc recommendation.

## Quick Start

- Start from [references/omics-lecture-hall-bioinfo-video-map-latest.md](references/omics-lecture-hall-bioinfo-video-map-latest.md) for the current curated snapshot.
- Refresh the snapshot with `scripts/refresh_index.py` when the user asks for the latest or all current videos.
- Use `opencli bilibili search "组学大讲堂" --type user -f json` to verify the channel identity if needed.
- Use `opencli bilibili user-videos 1181501194 --limit 50 --page N -f json` as the reliable live source on this machine.
- If the user needs a deeper dive on one specific video and `opencli bilibili video` or `summary` works in the current environment, use it as a follow-up. If those commands hang, keep the title-derived summary and say so explicitly.

## Scope Rules

- Include videos that directly teach one or more of these:
  - bioinformatics analysis methods such as `WGCNA`, BLAST, FASTA processing, phylogenetic tree work, gene-family analysis, enrichment analysis, or protein-interaction networks
  - sequencing-data workflow such as `SRA` download, `GEO` upload, `16S` upload, FASTQ interpretation, checksum validation, or sequencing-principle primers
  - R-based statistics or visualization that are clearly positioned as bioinformatics workflow support
  - Linux, VS Code, or spreadsheet usage when the lesson is framed as support for bioinformatics work
  - literature walkthroughs that explain the analysis logic of a bioinformatics paper or omics case
- Treat this channel as bioinformatics-adjacent by default. Prefer splitting results into buckets rather than aggressively excluding videos.
- Only exclude videos if a future refresh adds clearly off-topic material.

## Workflow

1. Confirm local `opencli` availability with `opencli --help`.
2. Confirm the channel identity once if needed:
   - user name: `组学大讲堂`
   - UID: `1181501194`
   - space URL: `https://space.bilibili.com/1181501194`
3. Refresh the channel list with:
   - `python scripts/refresh_index.py`
   - or raw `opencli bilibili user-videos 1181501194 --limit 50 --page N -f json`
4. Use the generated reference file to answer quickly:
   - separate `核心生信分析`
   - `测序与数据提交`
   - `R语言与可视化`
   - `科研案例与基础支撑`
5. For the final answer, prefer a concise grouped checklist:
   - title
   - date
   - BVID or URL
   - why it matters
   - one short content summary
6. When the user says `latest`, rerun the script instead of trusting the existing snapshot.

## Reporting Rules

- State the snapshot date explicitly.
- Mention the total video count and bucket counts.
- Be clear that the current per-video content summaries are title-derived from the live `user-videos` list unless a video was further inspected.
- Separate core analysis videos from tool or environment foundations so the user can skim quickly.
- If `opencli bilibili video` or `summary` is unreliable on this machine for a specific run, say that the list is still live-refreshed but the fine-grained summary remained heuristic.

## Resources

- [references/omics-lecture-hall-bioinfo-video-map-latest.md](references/omics-lecture-hall-bioinfo-video-map-latest.md)
  - stable pointer to the latest generated snapshot
- `references/omics-lecture-hall-bioinfo-videos-latest.json`
  - machine-readable latest snapshot
- `scripts/refresh_index.py`
  - refreshes the channel list through `opencli`
  - classifies videos into reusable buckets
  - writes dated plus stable JSON and Markdown outputs

## Example Prompts

- organize all `组学大讲堂` bioinformatics videos and give me a short categorized checklist
- refresh the latest `组学大讲堂` channel and summarize all bioinfo-related videos
- list `组学大讲堂` videos about `WGCNA`, `GEO`, `SRA`, `R` plotting, and Linux foundations
