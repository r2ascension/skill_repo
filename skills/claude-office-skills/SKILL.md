---
name: claude-office-skills
description: Router for Office-document workflows across DOCX, PPTX, PDF, and XLSX. Trigger when the user wants to create, edit, convert, inspect, or quality-check common Office files and the exact document type is not yet narrowed.
---

# claude-office-skills

Use this collection router when:
- the task mentions Word, PowerPoint, Excel, PDF, Office documents, or cross-format conversion
- the user needs OOXML-level editing, content extraction, or document QA across multiple Office formats
- the request is clearly office-document work but the best child skill is not yet obvious

Routing guidance:
- Route to `public/docx` for Word documents, `public/pptx` for presentations, `public/xlsx` for spreadsheets, and `public/pdf` for PDF-specific workflows.
- If the task is specifically an academic presentation, consider `academic-pptx-skill` or `thesis-defense-pptx` alongside `public/pptx`.

Merge and precedence notes:
- This collection remains general-purpose; use academic slide routers for research-talk structure.

Examples in this collection:
- claude-office-skills/docx
- claude-office-skills/pdf
- claude-office-skills/pptx
- claude-office-skills/xlsx
