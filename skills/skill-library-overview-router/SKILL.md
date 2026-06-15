---
name: skill-library-overview-router
description: Top-level router for the local skill library. Trigger when the task is broad or the best skill family is not yet clear and you need to route the user into a major domain such as academic writing, computational workflows, office documents, or clinical work.
---

# skill-library-overview-router

Use this router when:
- the request is broad and could map to several unrelated skill families
- the user asks what skills exist or which major skill family to use
- you want a top-level entry point before drilling into a domain router

Routing guidance:
- Use academic-writing-router, literature-workflows-router, academic-review-router, academic-citation-router, academic-slides-router, or paper-dissemination-router for paper and research communication work.
- Use computational-research-router first for coding, bioinformatics, scientific computing, data science, pipeline automation, or analysis engineering tasks.
- Use office-documents-router for PPTX, DOCX, XLSX, PDF, posters, and document transformations.
- Use clinical-health-router for clinical, diagnostic, protocol, or health-focused tasks.

Examples:
- which local skill family should handle this task
- show me the main skill categories
- route this request before choosing a concrete skill