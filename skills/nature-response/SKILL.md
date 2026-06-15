---
name: nature-response
description: "Draft, audit, or revise point-by-point reviewer response letters for Nature-family manuscript revisions. Use when the user explicitly wants Nature-style response packaging or is revising a Nature-family submission. For general reviewer responses across journals, prefer the academic review router and the more specialized domain writing skills."
version: 1.0.0
status: Beta
author: Community contribution, refactored into static/dynamic layers
---

# Nature Reviewer Response 鈥?Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (the default stance and red lines, and the response workflow with output format).
- A **dynamic layer** (this file plus `manifest.yaml`) that loads the core every time and reaches for the deeper response references only when a step needs them.

Do not try to apply the response logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

## Routing Note

Use this skill for Nature-family or explicitly Nature-style reviewer response letters.

Prefer other skills for:

- general reviewer-style critique before submission: `academic-review-router`
- statistics-manuscript response letters: `stats-paper-writing-agent-skills/skills/stat-writing`

Follow these four steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). Then read every file listed under `always_load`:

- `static/core/stance.md` 鈥?the editor-facing purpose, the default stance, the red lines, and the source hierarchy that apply to every response job.
- `static/core/workflow.md` 鈥?accepted inputs, the ten-step workflow, and the output package format.

### 2. No content axis 鈥?identify mode and language inline

Unlike nature-writing or nature-figure, nature-response has no fragment axis. Its variation is identified at runtime, not by loading different content bodies:

- **task mode** 鈥?`draft` / `audit` / `revise` / `triage-only` / `appeal-like`.
- **decision type** 鈥?minor revision, major revision, revise-and-resubmit, transfer after review, or unclear.
- **user language** 鈥?if the user writes Chinese, also produce the 涓枃鏍稿 block.

Use `references/intake-and-routing.md` to fix the task mode, minimum inputs, and readiness state before drafting. Route appeal-like cases separately; do not draft an appeal as the default path.

### 3. Run the workflow

Follow the ten-step workflow in `core/workflow.md`: identify mode and decision type, extract editor instructions (IDs `E.1`) then reviewer comments (`R1.1`, `R2.1`), classify each item, build a strategy summary, draft point-by-point responses from the preserved comments, map every claimed change to a manuscript location or an explicit placeholder, flag missing author input, run QA, and return the package with a readiness state.

Never invent experiments, citations, line numbers, figure panels, supplementary items, editor instructions, or manuscript changes. Mark anything the author must supply as `AUTHOR_INPUT_NEEDED`.

### 4. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest 鈥?for example `references/comment-taxonomy.md` to classify comments, `references/action-mapping.md` for tracker fields, `references/tone-and-stance.md` for disagreement wording, `references/difficult-cases.md` for impossible experiments / conflicting reviewers / appeal-like cases, `references/chinese-author-alignment.md` for Chinese author notes, and `references/qa-checklist.md` before finalizing.

## Why this split

- The static layer is versioned and reviewable; the core stays small for a normal response.
- The dynamic layer keeps each invocation cheap: the difficult-case, taxonomy, and QA depth load only when a step needs them.
- The router itself is short on purpose. Update fragments and references, not this file, when adding scope.
- This structure mirrors `nature-writing`, `nature-polishing`, `nature-reader`, `nature-paper2ppt`, `nature-figure`, and `nature-citation`.


