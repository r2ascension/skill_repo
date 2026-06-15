---
name: codex-operation-worklog
description: Keep a durable repository-level worklog for substantive local Codex operations. Use when Codex is modifying files, changing prompts/configuration/skills, running commands that affect the workspace, creating or updating runbooks, or making decisions that should be recoverable later. Prefer an existing task-specific worklog when one already governs the active thread; otherwise maintain a root `WORKLOG.md` in the repository.
---

# Codex Operation Worklog

## Overview

Use this skill to make local Codex work replayable in the same way SSH-side experiment logs are replayable.

Treat worklog updates as part of the task, not as optional cleanup at the end.

## Choose the journal target

Select the most specific existing journal that already owns the work:

1. Reuse an active task worklog if the repository already has one for the same thread.
2. Otherwise use the repository root `WORKLOG.md`.
3. Create a new dedicated worklog only when the user explicitly asks for a separate journal or the repository already has a stronger convention.

Do not fork the provenance trail across multiple new files unless there is a clear reason.

## Required loop

For every substantive operation:

1. Identify the journal target before the first meaningful edit or command batch finishes.
2. Ensure the target file exists.
3. Append a timestamped entry for each meaningful step instead of rewriting history.
4. Record failures, retries, and reversals, not only successful actions.
5. Update the journal again before finishing if the plan, files, or verification changed.

Substantive operations include:

- editing files
- creating or updating local skills
- changing `AGENTS.md`, prompts, config, or routing behavior
- running workspace-affecting commands
- introducing or removing automation scripts
- making decisions that change how future sessions should behave

If the task is purely explanatory and no files, commands, outputs, or durable decisions are produced, skipping is acceptable.

## Entry content

Use concise factual bullets. Prefer this shape:

````md
### 2026-06-15T22:50:47+08:00 | short_step_name

- Operation:
- Goal:
- Process:
- Modified files:
- Commands:
  ```bash
  ...
  ```
- Decisions:
- Verification:
- Result:
- Next step:
- Time:
  - 2026-06-15T22:50:47+08:00
- Author:
  - Codex
````

Use real paths, commands, and outcomes. Link to artifacts instead of pasting long terminal dumps.

## Root `WORKLOG.md` default

When no stronger journal exists, maintain a root `WORKLOG.md` with a short header plus appended entries.

The header should explain that:

- the file is a repository-level provenance log
- task-specific worklogs still win when they are clearly active
- the log should be append-only for history, except for tiny typo fixes

## Helper script

Use `scripts/ensure_worklog.py` when a root `WORKLOG.md` is missing or when you want a fresh entry scaffold:

- create the file if needed
- print or append a timestamped markdown stub
- keep the format consistent without inventing content

Typical usage:

```bash
python scripts/ensure_worklog.py --repo-root . --step create-skill --append
```

After the scaffold exists, fill in the actual details from the work that happened.
