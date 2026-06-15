---
name: research-superpower
description: Router for literature discovery, citation traversal, screening, and research-question answering. Trigger when the user wants evidence gathering from papers, especially PubMed or citation-chain workflows, rather than full manuscript drafting.
---

# research-superpower

Use this collection router when:
- the user asks to find papers, traverse citations, screen studies, or answer a research question from the literature
- the task is search-first evidence gathering, especially in biomedical or scientific-paper corpora

Routing guidance:
- Route to `skills/research/searching-literature` for PubMed-style seed searches, `traversing-citations` for citation chaining, and related screening skills for triage.
- If the user already has the papers and needs a written review, route instead toward literature-review or survey-writing skills.

Merge and precedence notes:
- This pack overlaps with `research-skills/skills/literature-scout`; use this one when the emphasis is search and evidence retrieval rather than survey writing deliverables.

Examples in this collection:
- research-superpower/research/searching-literature
- research-superpower/research/traversing-citations
- research-superpower/research/answering-research-questions
