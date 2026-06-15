---
name: thesis-defense-pptx-skill
description: Router alias for editable thesis-defense PowerPoint generation on Windows. Trigger when the user wants a defense PPTX generated from thesis PDF or LaTeX, preserved against an existing PowerPoint template, exported to PNG, or checked for text overflow.
---

# thesis-defense-pptx-skill

Use this collection router when:
- the task is specifically about thesis or dissertation defense slides rather than generic presentation design
- the user wants an editable PPTX built from thesis PDF, LaTeX, or a local manuscript project
- the workflow needs template-preserving PowerPoint automation, slide image export, or overflow QA on Windows

Routing guidance:
- Prefer the installed `thesis-defense-pptx` skill for the real deck generation workflow.
- Combine with `academic-pptx-skill` when the content structure and argument arc of the talk need improvement.
- Use generic Office or PPTX skills only for follow-up edits that are not defense-specific.

Merge and precedence notes:
- This wrapper is intentionally an alias, not a separate slide methodology.

Examples in this collection:
- thesis-defense-pptx
- turn my thesis PDF into an editable defense PPTX
- keep this university template and regenerate the defense deck from LaTeX
