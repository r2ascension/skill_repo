# SSH Handoff Template

Use this as the default skeleton for SSH-side execution notes in `E:\AI\codex`.

Keep the wording concrete. Replace every placeholder with real paths, real commands, and real output names.

## 1. Goal

- State the exact task to finish on the SSH side.
- State the stop condition in one sentence.
- State whether the SSH side is generating new outputs, validating existing outputs, or writing back results.

## 2. Local Input Inventory

List every local artifact the SSH-side agent depends on.

Use this shape:

```md
- `E:\AI\codex\path\to\file.ext`
  - role: what this file is for
  - remote target: `/remote/path/file.ext`
  - method: `copy` | `run` | `read-only reference`
```

If a local script is executed remotely, name the exact entrypoint and the exact destination path after sync.

## 3. Remote Target Tree

Name the exact remote root first, then list the required subpaths.

Use this shape:

```md
- remote root: `/home/h2048/docs/experiments/example_run_20260615`
- required directories:
  - `/home/h2048/docs/experiments/example_run_20260615/docs`
  - `/home/h2048/docs/experiments/example_run_20260615/scripts`
  - `/home/h2048/docs/experiments/example_run_20260615/results`
```

Do not say "use an appropriate directory".

## 4. File-to-Method Mapping

Map each important file to one primary action.

Use this shape:

```md
| Artifact | Location | Method | Result |
| --- | --- | --- | --- |
| input manifest | `E:\AI\codex\example.tsv` | `copy` | remote copy exists |
| plotting script | `/remote/root/scripts/run_plot.py` | `run` | writes `results/panel.svg` |
| result summary | `/remote/root/results/summary.tsv` | `return` | copied back to local repo |
```

This section is where you remove ambiguity around "which file does what".

## 5. Ordered Execution Steps

Write steps in the exact order they should be executed.

For each step, include:

- the exact working directory
- the exact command
- the expected output path
- the condition for moving to the next step

Use this shape:

```md
1. Create the remote directories.
   - command:
     ```bash
     mkdir -p /remote/root/docs /remote/root/scripts /remote/root/results
     ```
   - success check: all three directories exist

2. Sync the local inputs.
   - command:
     ```bash
     scp E:/AI/codex/example.tsv user@host:/remote/root/docs/example.tsv
     ```
   - success check: `/remote/root/docs/example.tsv` exists and file size is non-zero
```

Do not compress multiple fragile actions into one vague step.

## 6. Expected Outputs

Name the exact output files or directories the SSH-side agent should produce.

Use this shape:

```md
- `/remote/root/results/panel.svg`
- `/remote/root/results/summary.tsv`
- `/remote/root/logs/run_plot.log`
```

If an output is optional, state the decision rule that makes it optional.

## 7. Validation

Provide both the command and the success condition.

Use this shape:

```md
- command:
  ```bash
  test -s /remote/root/results/summary.tsv
  ```
  success: file exists and is non-empty

- command:
  ```bash
  grep -n "ERROR" /remote/root/logs/run_plot.log
  ```
  success: no matches
```

If visual inspection is required, say which file to inspect and what property must be true.

## 8. Write-Back to Local Repo

State exactly what should come back to `E:\AI\codex`.

Use this shape:

```md
- copy `/remote/root/results/summary.tsv` back to `E:\AI\codex\artifacts\summary_20260615.tsv`
- copy `/remote/root/results/panel.svg` back to `E:\AI\codex\artifacts\panel_20260615.svg`
- append a brief completion note to `E:\AI\codex\WORKLOG.md` only if the run actually changed tracked artifacts
```

Do not end with "return the results" without naming files.

## 9. Failure Recovery

Cover the first likely failure modes explicitly.

Minimum set:

- missing remote directory
- missing synced file
- command exits non-zero
- output file missing or empty
- result generated but write-back failed

Use this shape:

```md
- if `/remote/root/scripts/run_plot.py` is missing, re-run the sync step only for that file before any compute step
- if `summary.tsv` is empty, inspect `logs/run_plot.log`, fix the input path, and rerun only step 4
```

## 10. Final Checklist

Do not ship the handoff until all are true:

- every referenced file path is explicit
- every directory path is explicit
- every step has a command or an explicit method
- every expected output is named
- every validation step has a success condition
- every write-back artifact is named with a local destination
- every fallback tells the SSH-side agent what to retry first
