---
name: bioinformatics-experiment-journal
description: "Use when doing 生信分析、单细胞/scRNA-seq 分析、pipeline 运行、脚本修改、参数调整、结果生成、实验记录、工作日志、reproducibility tasks. Keeps a persistent experiment journal updated for every substantive operation in this repository."
---

# Bioinformatics Experiment Journal

## Overview

This skill makes analysis work durable.

In this repository, every **substantive operation** should leave a persistent record under `docs/experiments/`. A substantive operation is any step that changes code, parameters, commands, outputs, decisions, or execution state.

Tiny read-only exploration can be grouped into one planning note or skipped if it produces **no durable change**. Everything else should be journaled.

## Repo-optimized rule: journal separately, do not relocate the whole repository

Do **not** force a generic top-level `experiments/` output tree unless the user explicitly asks for a standalone scaffold.

This repository already has stable homes:

- analysis scripts: `script/py/`, `script/R/`, `script/bash/`
- Python outputs: `data/py/<YYYYMMDD>/...`
- R outputs: `data/R/<YYYYMMDD>/...`
- runtime logs: `logs/<YYYYMMDD>/...`
- scratch / temporary work: `temp/`
- persistent experiment journals: `docs/experiments/`

The journal should point to **real paths** instead of inventing a parallel directory tree.

## Choose the record type

### 1. Scoped experiment

Use `docs/experiments/EXP-YYYYMMDD-<slug>/` when the work is:

- multi-step
- result-bearing
- parameter-sensitive
- likely to continue across turns or days
- important enough that it should have its own metadata

Expected files:

- `docs/experiments/EXP-YYYYMMDD-<slug>/README.md`
- `docs/experiments/EXP-YYYYMMDD-<slug>/metadata.yaml`

### 2. Daily worklog

Use `docs/experiments/WORKLOG-YYYYMMDD.md` for:

- quick fixes
- one-off maintenance
- small refactors
- short exploratory sessions
- several small tasks that do not need a dedicated experiment folder

### Reuse before creating

If a matching active experiment or today's worklog already exists, **append to it**. Avoid duplicate journals for the same thread of work.

## Required behavior

For every substantive operation:

1. Identify the active journal path.
2. If no suitable journal exists, create one before finishing the first substantial batch of work.
3. Append entries; do not rewrite history unless the user explicitly asks for cleanup.
4. Record failures, dead ends, and reversals — not only success.
5. Use real commands, real paths, and real parameter values.
6. Link to log files or output folders instead of pasting huge terminal transcripts.
7. Before declaring the task done, ensure the journal reflects the latest status.

## Required entry fields

Every entry should include:

- `操作`
- `目标`
- `过程`
- `修改文件`
- `命令`
- `输入文件`
- `输出文件`
- `参数/决策`
- `验证`
- `结果`
- `时间戳`
- `作者`
- `备注/下一步`

## Entry template

````md
### 2026-05-26T18:30:00+08:00 | short_step_name

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

## Metadata minimum

A scoped experiment's `metadata.yaml` should minimally track:

```yaml
exp_id: EXP-YYYYMMDD-slug
title: Short human-readable title
mode: experiment
status: planned  # planned | in_progress | blocked | completed
created_at: 2026-05-26T18:30:00+08:00
updated_at: 2026-05-26T18:30:00+08:00
owner: GitHub Copilot
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

## When to create or update a journal automatically

Journaling is expected when you:

- create or modify analysis scripts
- change thresholds, model settings, or pipeline parameters
- run a command expected to produce outputs or logs
- move or rename output locations
- interpret a result in a way that changes the next action
- fix a bug that changes analysis behavior or reproducibility
- create a new helper script, config, or workflow for analysis execution

## When skipping is acceptable

Skipping journal creation is acceptable only when **all** of the following are true:

- the task is purely explanatory or advisory
- no files are created or modified
- no commands are run
- no outputs, logs, or decisions are persisted

If in doubt, add a short worklog entry. Small notes beat missing history.

## Anti-patterns

Avoid these:

- code changes with no journal update
- claiming outputs exist when they were not created
- inventing command lines or parameters after the fact
- dumping raw terminal output instead of referencing logs
- creating a new `EXP-...` folder when an existing active journal is sufficient
- storing secrets in the journal
- rewriting earlier entries to hide a failed attempt

## Closing checklist

Before saying work is complete, check:

- [ ] The active journal file was created or updated
- [ ] The journal points to real script/output/log paths
- [ ] Parameter choices and decisions are written down
- [ ] Verification or failure status is recorded
- [ ] Next step is recorded, or closure is stated explicitly

## Practical default for this repository

If the user gives no explicit experiment ID:

- prefer an existing relevant `EXP-...` journal if one already exists
- otherwise use today's `WORKLOG-YYYYMMDD.md` for small work
- create a new `EXP-YYYYMMDD-<slug>` only when the task is clearly multi-step or result-bearing

This keeps journaling strict without forcing unnecessary folder sprawl.
