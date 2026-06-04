---
name: 'clinical-nlp-extractor'
description: "Use when extracting medical entities from unstructured clinical notes AND patient messages. Extracts diseases, medications, procedures, symptoms, lab values, vitals, temporal data, and action items using regex, rules, or LLM wrappers."
measurable_outcome: Execute skill workflow successfully with valid output within 15 minutes.
allowed-tools:
  - Read
  - Bash
---

<!--
# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

-->

# Clinical NLP Entity Extractor

The **Clinical NLP Skill** converts free-text clinical notes into structured data. It identifies key medical entities like problems/diagnoses, medications, and procedures.

## When to Use This Skill

*   When analyzing unstructured EHR notes.
*   When extracting entities from patient messages (symptoms, medications, lab values, diagnoses).
*   To populate a patient's problem list or medication reconciliation.
*   To de-identify text (phi-removal) - *Basic version*.

## Core Capabilities

1.  **NER (Named Entity Recognition)**: Extracts Problems, Drugs, Procedures.
2.  **Negation Detection**: (Basic) Checks if a finding is denied ("No fever").
3.  **Structuring**: Returns JSON format compatible with FHIR/USDL.

## Workflow

1.  **Input**: A string of clinical text or a text file.
2.  **Process**: Tokenizes and matches against patterns/dictionaries.
3.  **Output**: JSON list of entities with spans and types.

## Example Usage

**User**: "Extract entities from this note."

**Agent Action**:
```bash
python3 Skills/Clinical/Clinical_NLP/entity_extractor.py \
    --text "Patient has diabetes type 2. Prescribed Metformin 500mg. No chest pain." \
    --output entities.json
```

```

## Patient Message Entity Extraction

Extract structured medical information from unstructured patient messages in addition to clinical notes. This supports triage, prior authorization, and clinical decision support workflows.

### Entity Types for Patient Messages

**Symptoms**
- Name, severity (mild/moderate/severe), duration, onset, progression (improving/stable/worsening)

**Medications**
- Name, dosage, frequency, route, context (new/existing/stopped)

**Lab Values**
- Type (BP, glucose, cholesterol, etc.), value, unit, timestamp, normal range

**Diagnoses**
- Name, context (confirmed/suspected/ruled out)

**Vital Signs**
- Temperature, heart rate, respiratory rate, oxygen saturation, blood pressure

**Action Items**
- Type (appointment, refill, question, callback), urgency, reason

### Temporal Extraction
Captures when symptoms started, duration, and progression timeline from free-text temporal expressions ("since yesterday", "for the past week").

### Medical Terminology Handling
Recognizes:
- Common abbreviations (BP, HR, RR, O2 sat)
- Brand and generic medication names
- Lay terms for medical conditions ("sugar" -> diabetes, "heart attack" -> MI)
- Temporal expressions ("since yesterday", "for the past week")

### Input Format (Patient Messages)
```json
[
  {
    "id": "msg-123",
    "priority_score": 78,
    "priority_bucket": "P1",
    "subject": "Medication side effects",
    "from": "patient@example.com",
    "date": "2026-02-27T10:30:00Z",
    "body": "I've been feeling dizzy since starting the new blood pressure medication (Lisinopril 10mg) three days ago."
  }
]
```

### Output Format
```json
[
  {
    "id": "msg-123",
    "entities": {
      "symptoms": [
        {"name": "dizziness", "severity": "moderate", "duration": "3 days", "onset": "since starting new medication"}
      ],
      "medications": [
        {"name": "Lisinopril", "dosage": "10mg", "context": "new medication"}
      ],
      "action_items": [
        {"type": "medication_review", "reason": "possible side effect (dizziness)"}
      ]
    },
    "summary": "Patient reports dizziness after starting Lisinopril 10mg 3 days ago."
  }
]
```

<!-- AUTHOR_SIGNATURE: 9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE -->