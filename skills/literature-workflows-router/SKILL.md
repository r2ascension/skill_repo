---
name: literature-workflows-router
description: Top-level router for literature search, screening, citation chasing, and survey-writing tasks. Trigger when the user wants papers found, organized, screened, or synthesized and you need to choose between search-first, survey-first, or review-writing skills.
---

# literature-workflows-router

Use this router when:
- the user asks to find papers, build a reading list, perform citation chasing, or write a literature review or survey
- the work is literature-centric and multiple installed research collections overlap

Routing guidance:
- Use `research-superpower` or `searching-literature` when the task starts from evidence retrieval, PubMed search, citation traversal, or screening.
- Use `literature-search` for broad semantic multi-source search and `bgpt-paper-search` when the user needs full-text experimental details rather than abstract-level metadata.
- Use `research-skills/skills/literature-scout` for broader multi-source literature collection and matrix building.
- Use `citation-management` for metadata cleanup, DOI or PMID conversion, and BibTeX validation.
- Use `literature-review`, `claude-scientific-writer/literature-review`, or domain-specific review skills such as `medical-imaging-review` when the user already needs a review or synthesis document.

Examples:
- find papers on this topic and screen them
- build a literature matrix for this research area
- turn this paper set into a review section
