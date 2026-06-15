---
name: bioagents-geoagent-router
description: Route between bio-xyz/BioAgents and JiekaiLab/GEOAgent. Use when the user names either repository or when the task sits between open-ended biology research assistance and GEO-first dataset discovery, metadata curation, or preprocessing orchestration.
---

# bioagents-geoagent-router

Use this router when:
- the user explicitly mentions `BioAgents`, `bio-xyz/BioAgents`, `GEOAgent`, or `JiekaiLab/GEOAgent`
- it is unclear whether the job is open-ended scientific research support or GEO-centric dataset curation
- the request mixes literature questions with GEO accessions, sample metadata, or preprocessing handoff needs

Routing guidance:
- Use `bioagents-agentkit` for conversational biology research loops that combine literature synthesis, uploaded datasets, analysis planning, hypothesis generation, reflection, and iterative deep research.
- Use `geoagent-geo-discovery` for GEO accession search, GSE or GSM metadata cleanup, omics and platform identification, sample renaming, multi-omics pairing, ChIP-seq Input or IP matching, and bioStream-oriented preprocessing handoff.
- If GEO cohorts have already been curated and the remaining job is standard downstream analysis, hand off into narrower bulk, single-cell, workflow, or visualization skills.
- If the work shifts from analysis support into manuscript writing, citation work, or review, hand off into the academic or literature routers after the repository choice is settled.

Examples:
- should I use BioAgents or GEOAgent for this task
- find GEO cohorts and prepare a preprocessing handoff
- combine papers, uploaded matrices, and hypotheses around this disease question
