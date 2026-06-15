---
name: academic-slides-router
description: Top-level router for academic presentation work. Trigger when the user wants thesis defense slides, seminar or conference decks, paper presentations, or other research-slide deliverables and you need to choose among editable PPTX generation, academic slide-structure guidance, or image-first deck generation.
---

# academic-slides-router

Use this router when:
- the task is a thesis defense, dissertation talk, seminar, conference talk, paper presentation, or research presentation deck
- the user asks to make academic slides but the best slide workflow is not yet clear

Routing guidance:
- Use `thesis-defense-pptx` for editable Windows PowerPoint decks generated from thesis PDF or LaTeX with template preservation and QA.
- Use `academic-pptx-skill` for academic argument structure, slide norms, and defense-specific content decisions.
- Use `scientific-slides` for general research-talk structure, timing, and Beamer-or-PowerPoint oral presentation guidance.
- Use `nature-paper2ppt` when the user explicitly wants a Nature-style or Chinese story-first paper presentation rather than template-preserving slides.
- Use `claude-office-skills/public/pptx` for generic PPTX creation or OOXML editing.
- Use `research-skills/paper-slide-deck` when the deliverable is an image-first deck or slide-image batch generated from papers or markdown.

Examples:
- turn my paper into conference slides
- make a thesis defense deck from this LaTeX project
- edit this existing PPTX for my seminar talk
