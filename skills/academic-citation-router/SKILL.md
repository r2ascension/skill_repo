---
name: academic-citation-router
description: Top-level router for citation finding, validation, and formatting. Trigger when the user needs references attached to claims, metadata verified, or BibTeX or RIS generated and you need to choose between general citation management, Nature-style citation policy, or literature-search helpers.
---

# academic-citation-router

Use this router when:
- the user asks to add citations, find sources for a claim, verify metadata, or generate BibTeX or RIS
- the task is citation-focused and several literature skills could apply

Routing guidance:
- Use `citation-management` for DOI or PMID lookup, metadata correction, and BibTeX generation.
- Use `nature-citation` when the user explicitly wants Nature, Cell, or Science-family source policy or citation attachment in a high-impact-journal style.
- Use `literature-workflows-router` or its child search skills when the user first needs the paper set before citations can be formatted.

Examples:
- find citations for this paragraph
- convert these DOIs into clean BibTeX
- add Nature-style references to these claims
