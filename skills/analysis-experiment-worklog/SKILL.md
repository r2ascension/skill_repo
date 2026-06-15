---
name: analysis-experiment-worklog
description: "Use when the user asks to 写实验记录, 更新实验记录, 写工作日志, 更新 WORKLOG, 记录分析步骤, 记录参数/命令/输出, or maintain docs/experiments style journals for bioinformatics or scRNA analysis repositories. Follows the same journaling principles as the existing bioinformatics experiment journal skill, but is optimized for Chinese-facing worklog updates in repositories using docs/experiments, script/*, data/py/<date>, data/R/<date>, and logs/<date>."
---

# Analysis Experiment Worklog

## Purpose

This skill keeps analysis work durable and easy to resume.

Use it when the user wants us to:

- write or append 实验记录
- update `WORKLOG-YYYYMMDD.md`
- create or continue `EXP-YYYYMMDD-<slug>/`
- summarize what was done in a reproducible journal entry
- record commands, parameters, outputs, failures, and next steps after real analysis work

## Repository convention

Prefer the repository's real structure instead of inventing a parallel tree:

- journals: `docs/experiments/`
- scripts: `script/py/`, `script/R/`, `script/bash/`
- Python outputs: `data/py/<YYYYMMDD>/...`
- R outputs: `data/R/<YYYYMMDD>/...`
- logs: `logs/<YYYYMMDD>/...`
- temporary files: `temp/`

The journal should point to real paths that were actually used.

## Choose the journal target

### `EXP-YYYYMMDD-<slug>/`

Use a dedicated experiment folder when the work is:

- multi-step
- result-bearing
- parameter-sensitive
- expected to continue later
- important enough to track with its own metadata

Expected files:

- `docs/experiments/EXP-YYYYMMDD-<slug>/README.md`
- `docs/experiments/EXP-YYYYMMDD-<slug>/metadata.yaml`

### `WORKLOG-YYYYMMDD.md`

Use the daily worklog when the work is:

- a quick fix
- a short exploratory check
- a small maintenance task
- a one-off command run
- several small related tasks that do not need a dedicated experiment folder

## Reuse before creating

Before creating a new journal target:

1. Look for a matching active `EXP-...` folder.
2. If the work is small, prefer today's `WORKLOG-YYYYMMDD.md`.
3. Append to the existing relevant record when possible.

Avoid creating duplicate journals for the same thread of work.

## Required behavior

For every substantive operation:

1. Identify the active journal path.
2. Create the journal target before finishing the first substantial batch of work if none exists.
3. Append entries instead of rewriting history.
4. Record failures, dead ends, retries, and reversals, not only successes.
5. Use real commands, real parameters, real paths, and real outputs.
6. Link to logs and output directories instead of pasting long terminal transcripts.
7. Before finishing, ensure the journal reflects the latest state and next step.

Substantive operations include:

- modifying scripts or configs
- running commands that generate outputs or logs
- changing thresholds or model settings
- moving output locations
- making an interpretation that changes the next action
- debugging an analysis behavior change

## Entry template

Use this structure unless the existing journal already uses a close variant:

````md
### 2026-06-02T22:30:00+08:00 | short_step_name

- 操作:
- 目标:
- 过程:
- 修改文件:
- 命令:
  ```bash
  ...
  ```
- 输入文件:
- 输出文件:
- 参数/决策:
- 验证:
- 结果:
- 时间戳:
- 作者:
- 备注/下一步:
````

## Writing rules

- Keep entries factual and concise.
- Prefer one entry per meaningful step.
- Use bullet lists, not long prose paragraphs.
- Mention why a decision was made when it affects reproducibility.
- If a command failed, say it failed and note the useful symptom.
- Do not invent outputs, command lines, or parameters after the fact.
- Do not store secrets in the journal.

## Encoding and remote sync guardrail

When the journal contains Chinese or other non-ASCII text and needs to be synced to SSH/remote Linux:

- Treat UTF-8 preservation as part of correctness, not as a formatting detail.
- Do **not** assume a successful shell command means the remote file is text-safe.
- Avoid text-mode pipelines that can silently replace Chinese characters with `?`, especially patterns like PowerShell `Get-Content -Raw | ssh "cat > file"` when locale/encoding is uncertain.
- Prefer binary-safe transfer:
  - `scp` of the original file when it is reliable, or
  - base64 encode locally, transfer ASCII safely, then decode remotely back to bytes.
- After syncing, verify the remote file, not just the command exit code.

Minimum verification for Chinese markdown synced to SSH:

1. Confirm the remote file decodes as UTF-8.
2. Check that suspicious replacement patterns are absent, especially large runs of `?`.
3. Prefer a byte-level check such as local/remote `SHA256` equality when possible.

If terminal output still shows `?` after verification, distinguish display-locale issues from file corruption before rewriting the file.

## Metadata minimum

For dedicated `EXP-...` folders, keep `metadata.yaml` minimally aligned with:

```yaml
exp_id: EXP-YYYYMMDD-slug
title: Short human-readable title
mode: experiment
status: planned
created_at: 2026-06-02T22:30:00+08:00
updated_at: 2026-06-02T22:30:00+08:00
owner: Codex
journal_root: docs/experiments
script_roots:
  - script/py
  - script/R
  - script/bash
output_roots:
  python: data/py/YYYYMMDD
  r: data/R/YYYYMMDD
log_root: logs/YYYYMMDD
```

## When skipping is acceptable

Skipping a journal update is acceptable only when all are true:

- the task is purely explanatory
- no files are created or modified
- no commands are run
- no outputs, logs, or durable decisions are produced

If unsure, add a short worklog entry.

## Practical default

If the user asks to “记一下”, “写个实验记录”, or “补一下 worklog” without specifying a target:

1. Prefer an existing relevant `EXP-...` record.
2. Otherwise use today's `WORKLOG-YYYYMMDD.md`.
3. Create a new `EXP-...` folder only when the task is clearly multi-step or will continue.
