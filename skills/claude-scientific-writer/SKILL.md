---
name: claude-scientific-writer
description: Router for scientific-writing workflows such as literature review, peer review, scholar evaluation, and paper-to-web conversion. Trigger when the user wants research-writing support beyond raw Office editing, especially for review, critique, or scholar-facing deliverables.
---

# claude-scientific-writer

Use this collection router when:
- the task is literature review writing, peer review, rebuttal support, scholar evaluation, or converting a paper into another reader-facing format
- the user wants a scientist-oriented writing helper but not necessarily a full end-to-end paper drafting workflow

Routing guidance:
- Route to `literature-review` for survey prose, `peer-review` for review workflows, `scholar-evaluation` for evaluating researchers or papers, and `paper-2-web` for paper-to-web conversions.
- Use the more specialized paper-writing routers when the main job is drafting a full manuscript from scratch.

Merge and precedence notes:
- This pack overlaps with paper-writing collections but is better treated as review and transformation oriented.

Examples in this collection:
- claude-scientific-writer/scholar-evaluation
- claude-scientific-writer/peer-review
- claude-scientific-writer/paper-2-web
