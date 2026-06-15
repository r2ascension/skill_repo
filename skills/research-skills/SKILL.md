---
name: research-skills
description: Router for general research workflows spanning literature scouting, survey writing, research proposals, paper slide decks, and medical imaging review. Trigger when the task is about managing a research workflow rather than only coding or editing a single document file.
---

# research-skills

Use this collection router when:
- the user wants literature scouting, proposal drafting, survey support, or paper-to-slide workflows
- the request is broad research-process support and the exact specialized child skill is not yet clear

Routing guidance:
- Route to `paper-slide-deck` for image-first slide generation from papers or markdown content.
- Route to `research-proposal` for proposal-specific structure, and `skills/literature-scout` or `skills/survey-writer` for literature-heavy tasks.
- If the task is a formal editable academic PPTX rather than slide images, prefer `thesis-defense-pptx` or Office/PPTX skills instead.

Merge and precedence notes:
- This collection is broader than literature search alone; do not let it swallow specialized manuscript-writing or editable-PPTX workflows.

Examples in this collection:
- research-skills/paper-slide-deck
- research-skills/research-proposal
- research-skills/skills/literature-scout
