---
name: clinical-health-router
description: Top-level router for clinical, health, diagnostic, and protocol-focused skills. Trigger when the task is patient-oriented, protocol-oriented, or medically framed and the best skill family could be clinical reasoning, documentation, trial, regulatory, or health analysis.
---

# clinical-health-router

Use this router when:
- the request is medical, clinical, diagnostic, protocol, payer, lab, or health-behavior related
- the user needs a clinical-domain skill but not yet a single precise specialty skill

Routing guidance:
- Use clinical note, diagnostic, FHIR, lab, or protocol skills for documentation and clinical workflows.
- Use trial, regulatory, or prior-authorization skills for study operations and payer-facing tasks.
- Use bioinformatics-router instead when the main task is omics analysis rather than patient-facing or clinical interpretation.

Examples:
- route this clinical documentation task
- which medical skill should handle this request
- I need a health or protocol workflow