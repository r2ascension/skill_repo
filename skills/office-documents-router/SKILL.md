---
name: office-documents-router
description: Top-level router for Office files, documents, slide decks, spreadsheets, PDFs, and related transformation tasks. Trigger when the user wants to create, edit, inspect, convert, or repurpose office-format artifacts and the exact format-specific skill is not yet obvious.
---

# office-documents-router

Use this router when:
- the task involves PowerPoint, Word, Excel, PDF, posters, or document conversion
- the user wants an office-format artifact created or edited but has not yet narrowed the exact file workflow

Routing guidance:
- Use pptx, docx, xlsx, and pdf skills for direct format work.
- Use academic-slides-router for academic talk decks and paper-dissemination-router for paper-derived assets.
- Use markitdown, pdf-processing, or format-specific tools for extraction and conversion workflows.
- Use latex-posters or pptx-posters when the deliverable is a poster rather than a normal document.

Examples:
- edit this PPTX
- convert this PDF into structured markdown
- build a poster or spreadsheet deliverable