---
name: academic-review-router
description: Top-level router for peer review, mock review, rebuttal, and reviewer-response tasks. Trigger when the user wants a reviewer-style critique, pre-submission review, or a point-by-point response letter and you need to choose among general review, Nature-style mock review, or response-letter skills.
---

# academic-review-router

Use this router when:
- the user asks for peer review, reviewer-style critique, pre-submission assessment, rebuttal drafting, or response to reviewers
- the task is review-cycle focused and multiple review-related skills overlap

Routing guidance:
- Use `peer-review` for general cross-disciplinary manuscript or grant review.
- Use `nature-reviewer` when the user explicitly wants a Nature-style reviewer simulation or high-impact-journal referee framing.
- Use `nature-response` for point-by-point reviewer response letters, especially Nature-family style responses.
- Use `stats-paper-writing-agent-skills/skills/stat-writing` when the response letter is tightly coupled to a statistics manuscript workflow.

Examples:
- review this manuscript like a referee
- draft a response to reviewers
- give me a Nature-style mock review before submission
