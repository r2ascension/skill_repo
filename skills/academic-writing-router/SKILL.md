---
name: academic-writing-router
description: Top-level router for academic manuscript work. Trigger when the user wants to plan, draft, revise, audit, review, or respond to reviews for a paper and you need to choose among general paper-writing, strategy, statistics-writing, or ML-paper-writing skills.
---

# academic-writing-router

Use this router when:
- the user wants to write or revise an academic paper, section, abstract, rebuttal, response letter, or review
- the task is manuscript-focused but multiple writing skill families plausibly apply

Routing guidance:
- Use `paper-writing-skill` for general manuscript drafting and revision workflows rooted in SNL editorial practice.
- Use `scientific-writing` for IMRAD-style scientific manuscripts that should stay in full-paragraph prose and often need reporting-guideline-aware structure.
- Use `nature-writing` when the user explicitly wants Nature/CNS or high-impact-journal style framing, especially from Chinese notes or drafts.
- Use `academic-paper-skills/strategist` for outline and originality planning, and `academic-paper-skills/composer` for plan-to-manuscript execution.
- Use `stats-paper-writing-agent-skills/skills/stat-writing` for statistics-heavy or journal-style LaTeX manuscripts, audits, reviewer reports, and response letters.
- Use `AI-Research-SKILLs/20-ml-paper-writing/ml-paper-writing` for ML or AI conference papers.
- Use `claude-scientific-writer` child skills when the task is literature review, peer review, scholar evaluation, or paper transformation rather than full-paper drafting.

Examples:
- help me rewrite the introduction of my paper
- plan a paper outline before drafting
- draft a response to reviewers for this manuscript
- write an ML conference paper from this repo
