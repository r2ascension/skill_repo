---
name: computational-research-router
description: Shared parent router for computational tasks. Trigger when the request is fundamentally code, analysis, automation, pipeline, modeling, or scientific computing work and you need to choose between software engineering, bioinformatics, scientific computing, or data science subrouters without narrowing too early.
---

# computational-research-router

Use this router when:
- the task is fundamentally computational, script-driven, pipeline-driven, or analysis-code driven
- the request could plausibly be handled as software engineering, bioinformatics, scientific computing, or data science
- you want a wide first pass for code and analysis work before choosing a narrower subrouter

Routing guidance:
- Use software-engineering-router when the main challenge is application code structure, frameworks, APIs, debugging, testing, or platform engineering.
- Use bioinformatics-router when the main challenge is omics workflow choice, biological analysis interpretation, or domain-specific computational biology tooling.
- Use scientific-computing-router when the task is numerical methods, simulation, plotting, or technical analysis without a strong app or omics framing.
- Use data-science-ml-router when the task is modeling, evaluation, machine learning, or AI workflow design.

Examples:
- this is a computational task but I am not sure if it is code engineering or bioinformatics
- route an analysis pipeline request without narrowing too early
- choose the right computational skill family first