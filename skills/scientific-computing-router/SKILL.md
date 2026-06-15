---
name: scientific-computing-router
description: Top-level router for scientific computing, plotting, simulation, and numerical analysis. Trigger when the user wants technical analysis or scientific scripting and the best tool family could be MATLAB, Python plotting, numerical methods, or simulation, especially when the work is computational but not strongly app-engineering or bio-omics specific.
---

# scientific-computing-router

Use this router when:
- the task is scientific programming, technical plotting, simulation, or numerical analysis
- the request mentions MATLAB, Matplotlib, Plotly, Seaborn, scientific visualization, or equations
- the user needs a scientific coding skill but not specifically a bioinformatics one

Routing guidance:
- Use scientific-agent-skills, matlab, matplotlib, plotly, or scientific-visualization for concrete tool workflows.
- Use academic-learning-plotting-and-visual-communication when the user wants maintained learning content for plotting, figure communication, or reusable figure design patterns rather than immediate code execution.
- Use numerical and simulation skills for ODEs, solvers, time stepping, stability, or simulation orchestration.
- Use data-science-ml-router when the job shifts from scientific scripting into machine learning or model-building workflows.
- Use software-engineering-router when the core problem becomes packaging, framework integration, testing, or productionization.
- Use bioinformatics-router when the same computational pattern becomes tied to omics-specific biological interpretation.

Examples:
- make a publication-quality Matplotlib figure
- help with MATLAB analysis
- simulate this system and analyze the result