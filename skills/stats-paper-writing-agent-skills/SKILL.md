---
name: stats-paper-writing-agent-skills
description: Router for statistical manuscript writing and review workflows in LaTeX, including abstract drafting, section expansion, manuscript audits, reviewer reports, and response letters. Trigger when the paper is statistics-heavy, journal-oriented, or explicitly framed as statistical writing.
---

# stats-paper-writing-agent-skills

Use this collection router when:
- the manuscript is in statistics, biostatistics, or JDS-style journal writing
- the task is a reviewer report, response letter, or structured manuscript audit for a statistical paper
- the user wants LaTeX-first statistical writing help instead of general academic prose advice

Routing guidance:
- Route to `skills/stat-writing` as the main workbench for statistical papers.
- Prefer this collection over generic paper-writing skills when the writing task is statistics-specific.

Merge and precedence notes:
- This collection should take precedence over generic paper-writing wrappers for statistics manuscripts.

Examples in this collection:
- stats-paper-writing-agent-skills/stat-writing
- write a response letter for my statistics paper
- audit this JDS manuscript in LaTeX
