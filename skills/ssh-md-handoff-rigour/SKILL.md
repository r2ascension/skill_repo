---
name: ssh-md-handoff-rigour
description: Detailed Markdown handoff and runbook discipline for SSH-side execution from `E:\AI\codex`. Use when Codex is delegating remote analysis, plotting, exports, evidence collection, figure reruns, worklog sweeps, or other SSH-side work and the `.md` must specify exact local files, remote target paths, methods, commands, expected outputs, verification, and fallback steps.
---

# SSH MD Handoff Rigour

## Overview

Use this skill to turn an SSH-side handoff into a low-ambiguity execution document.

Assume vague wording causes errors, reruns, or wrong file placement. Prefer one explicit path, one explicit method, and one explicit validation rule over open-ended guidance.

## Workflow

1. Decide whether the work should be delegated to SSH.
2. Inventory every artifact before writing: local source files, local scripts, remote target directories, remote output files, and expected write-back files.
3. Assign exactly one method to each artifact: `copy`, `run`, `edit`, `generate`, `validate`, or `return`.
4. Write the handoff in Chinese first unless the user asked for another language.
5. Follow `references/handoff-template.md` and keep its section order unless the task is truly tiny.

In `E:\AI\codex`, prefer an execution-ready `.md` handoff when the SSH side can reasonably do the work and the user did not explicitly ask Codex to perform the remote actions itself.

## Non-Negotiable Detail Rules

- Name exact local files with absolute Windows paths such as `E:\AI\codex\...`.
- Name exact remote paths. If the remote path is not known yet, choose one concrete path to create and state it explicitly.
- State the method for each file or directory, not only the existence of the file.
- Expand commands fully instead of saying "run the script" or "execute the pipeline".
- Name the entry script or notebook and the key arguments that matter.
- Name the exact expected output files or directories after each major step.
- Define validation commands and success criteria.
- Define the first fallback action for each likely failure mode.
- Repeat critical paths inside the execution steps; do not force the SSH-side agent to scroll back and infer them.
- Split one broad plan into multiple `.md` runbooks when unrelated scientific purposes, figures, or method families would otherwise compete in one file.

## Banned Vague Phrases

- Avoid vague wording such as `related files`, `corresponding directory`, `adjust as needed`, `if necessary`, `run it`, `check the result`, or `return the processed output` unless followed immediately by exact files, exact commands, or an explicit decision rule.
- Do not ask the SSH-side agent to infer which file, which directory, which script, which parameter, or which order.
- Do not give parallel alternatives without telling the SSH-side agent which one to choose and why.

## Required Sections

Every SSH handoff `.md` should include:

- goal and stop condition
- local input inventory
- remote destination tree
- per-file method mapping
- ordered execution steps
- expected outputs
- validation and acceptance checks
- write-back instructions to the local repository
- failure recovery and resume point

## Quick Sanity Check

Before finishing the handoff, verify these questions can each be answered without guesswork:

- Which exact local files must be read or copied?
- Which exact remote directory must exist first?
- Which exact command generates each expected artifact?
- Which exact files prove success?
- If one step fails, what should be retried or skipped first?

If any answer is missing, the handoff is not ready.

## Resource

Read `references/handoff-template.md` before drafting the final `.md`. Reuse its section headers and checklist instead of inventing a looser format.
