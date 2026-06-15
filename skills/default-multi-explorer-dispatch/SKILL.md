---
name: default-multi-explorer-dispatch
description: Use by default at the start of complex agent tasks that need repository context, debugging, planning, or validation; dispatch three parallel read-only Explore subagents for context, patterns, and risks before the main agent acts.
---

# Default Multi-Explorer Dispatch

Use this skill to make complex agent work start with parallel, read-only reconnaissance. The controller agent remains responsible for synthesis, decisions, edits, commands, validation, and the final user-facing answer.

**Core principle:** for non-trivial work, first split the unknowns across three fresh `Explore` subagents, then synthesize before acting.

## When to Use

Use this skill by default when a task is complex enough that a single linear inspection would likely miss context.

Good triggers:

- Debugging an error with an unknown root cause.
- Modifying code that touches multiple files, notebooks, environments, or data objects.
- Planning a non-trivial workflow before implementation.
- Validating scientific or operational assumptions.
- Working in a repository with important local conventions, memory notes, or historical scripts.
- Any request where the user says to use an agent, specialist agent, or subagents and the task is not a simple one-shot answer.

Skip this skill when:

- The user explicitly asks for a fast direct answer.
- The task is a small explanation that needs no workspace context.
- The answer is already certain from the visible prompt.
- Dispatching subagents would be slower than reading one short file.
- The task is unsafe or disallowed; refuse or redirect instead of dispatching.

## Default Dispatch

Dispatch exactly three `Explore` subagents in parallel unless the user asks for a different number.

### 1. Context Explorer

Goal: locate the concrete workspace context.

Ask this subagent to find:

- Relevant scripts, notebooks, configs, task definitions, and entry points.
- Data object names, file paths, assay/layer keys, model paths, and environment names.
- The smallest set of files the controller should read before acting.
- Any obvious current-state facts that constrain the solution.

### 2. Pattern Explorer

Goal: find reusable local patterns and precedents.

Ask this subagent to find:

- Similar prior scripts, helper functions, wrappers, recovery scripts, or task files.
- Repository memory, docs, plans, or version notes that establish conventions.
- Related skills that should be read or invoked before implementation, such as domain, visualization, data-export, or LLM-integration skills.
- Existing command patterns, environment setup patterns, and output naming conventions.
- Places where the same problem was already solved.

### 3. Risk Explorer

Goal: identify pitfalls before the controller edits or runs anything.

Ask this subagent to find:

- Likely failure modes, hidden assumptions, and dependency/environment risks.
- Scientific/data-integrity risks such as label vocabularies, batch categories, layers, raw counts, or file-format semantics.
- Minimal validation commands, smoke tests, or non-destructive checks.
- What should not be changed unless explicitly requested.

## Controller Protocol

1. Before editing or executing non-trivial commands, dispatch the three `Explore` subagents in parallel.
2. Give each subagent a self-contained prompt: include the user request, known paths, relevant constraints, expected output, and a strict read-only instruction.
3. Tell subagents not to modify files, install packages, run long jobs, or perform destructive actions.
4. After they return, synthesize the results before acting:
   - Deduplicate repeated findings.
   - Resolve disagreements by reading the primary files yourself.
   - Mark high-confidence facts versus hypotheses.
   - Convert findings into a concrete plan or implementation step.
5. Continue as the controller: make edits, run validations, update todos, and report results to the user.

## Memory, Repository, and Related Skill Awareness

Before implementation, the controller should use the Explorer reports to decide which memory files, repository conventions, and domain skills are relevant.

- Consult user memory and repository memory for environment pitfalls, helper APIs, previous migrations, output schemas, and validated commands.
- Prefer existing repository helpers and tests over inventing parallel implementations.
- If a domain-specific skill applies, read that skill before making domain decisions.
- If the task involves figures, tables, reports, enrichment, single-cell objects, or LLM review, explicitly check for relevant visualization, data-export, single-cell, GeneAgent, or LLM integration skills and local conventions.
- Keep the final implementation aligned with repository naming, logging, output-directory, and test conventions.

## Script Creation and Naming Convention

When implementing analysis, visualization, recovery, comparison, or LLM-review workflows, default to creating a new script instead of modifying an older analysis script.

- Treat existing dated scripts as provenance. Read and reuse their patterns, but do not mutate them unless the user explicitly asks to patch that exact file.
- New scripts should use the filename stem format `celltype_tool_purpose_YYYYMMDD`.
- Use lowercase snake_case components when practical; keep `purpose` short but specific.
- Preserve the language extension after the required stem, such as `.py`, `.R`, `.sh`, or `.ipynb`.
- Examples: `bcell_cnmf_program_review_20260506.py`, `tnk_scanvi_label_transfer_20260506.py`, `epithelial_choir_recovery_20260506.R`.
- If the exact same filename already exists, do not overwrite it; refine the purpose component or append a small suffix after the date only when necessary.
- It is still acceptable to modify shared helpers, tests, documentation, or configuration files when the task is explicitly about maintaining shared code rather than producing a new analysis run script.

## Figure, CSV, and LLM Artifact Contract

When the downstream task produces figures, LLM comparisons, or reviewer-facing summaries, the controller should treat plots and machine-readable data as paired artifacts.

- Every generated figure should have a corresponding CSV/TSV whenever practical.
- The CSV should contain the exact data used for plotting, not a manually reconstructed approximation.
- If a figure summarizes LLM-supported interpretation, also write a comparison CSV that links the plotted item to the LLM output.
- Include stable identifiers where available, such as `plot_id`, `panel`, `dataset`, `sample`, `cell_type`, `cluster`, `gene`, `program`, `pathway`, `metric`, `value`, `method`, `llm_model`, `llm_prompt_id`, `llm_label`, `llm_score`, `llm_rationale`, and `source_file`.
- Preserve enough provenance for reruns: input file paths, parameters, model names, prompt/template versions, timestamps when useful, and script version or git context when available.
- Keep figure filenames and CSV filenames paired by stem, for example `*_plot.pdf` with `*_plot_data.csv` and `*_llm_comparison.csv`.

## LLM Integration Guardrails

When implementation touches an LLM API or local LLM helper:

- Reuse existing repository LLM wrappers when present instead of adding another client layer.
- Do not hard-code API keys, base URLs, deployment names, or model names.
- Check whether the repository already expects `.env` variables or helper-specific configuration before adding new variables.
- If new secrets are required, ensure placeholder environment variables are documented or added to a local `.env` only as placeholders.
- Support configurable base URL, model/deployment, timeout, retry behavior, and dry-run or mock-test paths when feasible.
- Record the LLM model and prompt/template identifier in any LLM comparison CSV or reviewer bundle.
- Prefer deterministic, schema-checked LLM outputs for downstream plots or comparisons.
- Validate LLM plumbing with a lightweight test or mock before launching expensive analysis.

## Prompt Template

Use this shape for each `Explore` subagent prompt.

```markdown
You are the [Context|Pattern|Risk] Explorer for this task.

User request:
[paste the user's request]

Known context:
[workspace path, active file, known scripts, error snippets, relevant constraints]

Your scope:
[specific explorer role]

Rules:
- Read-only investigation only.
- Do not edit files.
- Do not install packages.
- Do not run long or destructive commands.
- Prefer concise findings with exact paths and line references when available.
- Check relevant memory, repository conventions, and applicable skills for this focus area.
- Check whether a new script should be created using `celltype_tool_purpose_YYYYMMDD` rather than modifying an old dated script.

Return:
1. Key findings.
2. Files or symbols the controller should inspect.
3. Risks, assumptions, or open questions.
4. Recommended next action for the controller.
```

## Synthesis Format

After all three subagents return, the controller should summarize internally or to the user when useful:

- `Context:` concrete files, data objects, commands, and current state.
- `Reusable patterns:` prior implementations or conventions to follow.
- `Risks:` pitfalls and guardrails.
- `Next action:` the smallest safe implementation or validation step.

## Failure Handling

- If one subagent fails, continue with the other results and fill the missing role yourself using targeted reads/searches.
- If subagents disagree, read primary sources directly before editing.
- If all subagents fail, fall back to normal manual investigation and tell the user briefly.
- Never present subagent output as verified fact until the controller has checked critical claims.

## Red Flags

Do not use this skill as an excuse to over-dispatch. Three `Explore` subagents are the default for complex tasks; simple tasks should stay simple. Tiny nails do not need a three-hammer orchestra.

Never let read-only exploration replace final validation. The controller must still run or propose the relevant checks after implementation.