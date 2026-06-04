---
name: biomni
description: "Use when conducting multi-step biomedical research including CRISPR screening design, single-cell RNA-seq analysis, ADMET prediction, GWAS interpretation, rare disease diagnosis, or lab protocol optimization. Leverages LLM reasoning with code execution and integrated biomedical databases."
license: MIT
metadata:
  author: Stanford (Snap Lab)
  source: "https://github.com/snap-stanford/Biomni"
  version: "1.0.0"
compatibility:
  - system: Python 3.9+
allowed-tools:
  - Read
  - Bash
  - WebFetch
keywords:
  - biomni
  - automation
  - biomedical
  - reasoning
  - tools
  - multi-tool
  - know-how
  - tutorials
  - protocols
  - databases
measurable_outcome: Execute complex research tasks with >95% success rate and validated tool usage.
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

# Biomni

## Overview

Biomni is an open-source biomedical AI agent framework from Stanford's SNAP lab that autonomously executes complex research tasks across biomedical domains. Use this skill when working on multi-step biological reasoning tasks, analyzing biomedical data, or conducting research spanning genomics, drug discovery, molecular biology, and clinical analysis.

Biomni is a "General-Purpose" biomedical agent. Unlike specialized skills (e.g., just for folding proteins), Biomni acts as a high-level orchestrator that can break down complex open-ended research questions into solvable sub-tasks using a vast library of tools and databases.

## At-a-Glance
- **description (10-20 chars):** Omni bio agent
- **keywords:** multi-tool, know-how, tutorials, protocols, databases
- **measurable_outcome:** Execute a Biomni workflow that touches >=2 tool categories and returns a cited research summary or artifact within 15 minutes per request.

## Core Capabilities

Biomni excels at:

1. **Multi-step biological reasoning** - Autonomous task decomposition and planning for complex biomedical queries
2. **Code generation and execution** - Dynamic analysis pipeline creation for data processing
3. **Knowledge retrieval** - Access to ~11GB of integrated biomedical databases and literature
4. **Cross-domain problem solving** - Unified interface for genomics, proteomics, drug discovery, and clinical tasks
5. **Tool Use** - Access to 150+ tools, 105 software packages, and 59 databases
6. **Hypothesis Generation** - Can formulate scientific hypotheses and plan experiments to test them
7. **Plan & Execute** - Breaks down queries into a dependency graph of tasks
8. **Database QA** - High accuracy (74.4%) in querying biomedical databases

## When to Use This Skill

Use biomni for:
- **CRISPR screening** - Design screens, prioritize genes, analyze knockout effects
- **Single-cell RNA-seq** - Cell type annotation, differential expression, trajectory analysis
- **Drug discovery** - ADMET prediction, target identification, compound optimization
- **GWAS analysis** - Variant interpretation, causal gene identification, pathway enrichment
- **Clinical genomics** - Rare disease diagnosis, variant pathogenicity, phenotype-genotype mapping
- **Lab protocols** - Protocol optimization, literature synthesis, experimental design

## General Workflow

### Workflow A: Task-Oriented (A1 Agent)
1. **Query Parsing**: The agent analyzes the user's natural language request.
2. **Tool Selection**: It selects relevant tools (e.g., "Search GWAS Catalog", "Run GO Enrichment", "Fetch Uniprot Data").
3. **Execution Loop**:
   - Step 1: Get data.
   - Step 2: Analyze data.
   - Step 3: Refine plan based on intermediate results.
4. **Synthesis**: Combines all findings into a comprehensive answer.

### Workflow B: Environment-Oriented
1. **Environment:** `cd repo && pip install .` (or follow tutorials env set up). Activate the environment with required GPUs if using heavy models.
2. **Select mode:** Choose Standard (full stack), Light (API-only), or Commercial (license-safe) per task.
3. **Plan tools:** Query the Know-How library for relevant protocols/databases before executing.
4. **Execute notebooks/scripts:** Use `repo/tutorials` or CLI entrypoints to run pipelines; log tool versions.
5. **Summarize:** Provide outputs + citations pulled from the Know-How metadata.

## Quick Start

### Installation and Setup

Install Biomni and configure API keys for LLM providers:

```bash
uv pip install biomni --upgrade
```

Configure API keys (store in `.env` file or environment variables):
```bash
export ANTHROPIC_API_KEY="your-key-here"
# Optional: OpenAI, Azure, Google, Groq, AWS Bedrock keys
```

Use `scripts/setup_environment.py` for interactive setup assistance.

### Basic Usage Pattern

```python
from biomni.agent import A1

# Initialize agent with data path and LLM choice
agent = A1(path='./data', llm='claude-sonnet-4-20250514')

# Execute biomedical task autonomously
agent.go("Your biomedical research question or task")

# Save conversation history and results
agent.save_conversation_history("report.pdf")
```

## Working with Biomni

### 1. Agent Initialization

The A1 class is the primary interface for biomni:

```python
from biomni.agent import A1
from biomni.config import default_config

# Basic initialization
agent = A1(
    path='./data',  # Path to data lake (~11GB downloaded on first use)
    llm='claude-sonnet-4-20250514'  # LLM model selection
)

# Advanced configuration
default_config.llm = "gpt-4"
default_config.timeout_seconds = 1200
default_config.max_iterations = 50
```

**Supported LLM Providers:**
- Anthropic Claude (recommended): `claude-sonnet-4-20250514`, `claude-opus-4-20250514`
- OpenAI: `gpt-4`, `gpt-4-turbo`
- Azure OpenAI: via Azure configuration
- Google Gemini: `gemini-2.0-flash-exp`
- Groq: `llama-3.3-70b-versatile`
- AWS Bedrock: Various models via Bedrock API

See `references/llm_providers.md` for detailed LLM configuration instructions.

### 2. Task Execution Workflow

Biomni follows an autonomous agent workflow:

```python
# Step 1: Initialize agent
agent = A1(path='./data', llm='claude-sonnet-4-20250514')

# Step 2: Execute task with natural language query
result = agent.go("""
Design a CRISPR screen to identify genes regulating autophagy in
HEK293 cells. Prioritize genes based on essentiality and pathway
relevance.
""")

# Step 3: Review generated code and analysis
# Agent autonomously:
# - Decomposes task into sub-steps
# - Retrieves relevant biological knowledge
# - Generates and executes analysis code
# - Interprets results and provides insights

# Step 4: Save results
agent.save_conversation_history("autophagy_screen_report.pdf")
```

### 3. Common Task Patterns

#### CRISPR Screening Design
```python
agent.go("""
Design a genome-wide CRISPR knockout screen for identifying genes
affecting [phenotype] in [cell type]. Include:
1. sgRNA library design
2. Gene prioritization criteria
3. Expected hit genes based on pathway analysis
""")
```

#### Single-Cell RNA-seq Analysis
```python
agent.go("""
Analyze this single-cell RNA-seq dataset:
- Perform quality control and filtering
- Identify cell populations via clustering
- Annotate cell types using marker genes
- Conduct differential expression between conditions
File path: [path/to/data.h5ad]
""")
```

#### Drug ADMET Prediction
```python
agent.go("""
Predict ADMET properties for these drug candidates:
[SMILES strings or compound IDs]
Focus on:
- Absorption (Caco-2 permeability, HIA)
- Distribution (plasma protein binding, BBB penetration)
- Metabolism (CYP450 interaction)
- Excretion (clearance)
- Toxicity (hERG liability, hepatotoxicity)
""")
```

#### GWAS Variant Interpretation
```python
agent.go("""
Interpret GWAS results for [trait/disease]:
- Identify genome-wide significant variants
- Map variants to causal genes
- Perform pathway enrichment analysis
- Predict functional consequences
Summary statistics file: [path/to/gwas_summary.txt]
""")
```

See `references/use_cases.md` for comprehensive task examples across all biomedical domains.

### 4. Example Usage

**User**: "Identify genes associated with Type 2 Diabetes that are also expressed in the pancreas and have approved drugs."

**Agent Action**:
1. Tool: `OpenTargets` -> Get T2D associated genes.
2. Tool: `GTEx` -> Filter for high expression in Pancreas.
3. Tool: `DrugBank` -> Intersect with drug targets.
4. Result: Returns a list of genes (e.g., *GLP1R*, *DPP4*) and their drugs.

### 5. Data Integration

Biomni integrates ~11GB of biomedical knowledge sources:
- **Gene databases** - Ensembl, NCBI Gene, UniProt
- **Protein structures** - PDB, AlphaFold
- **Clinical datasets** - ClinVar, OMIM, HPO
- **Literature indices** - PubMed abstracts, biomedical ontologies
- **Pathway databases** - KEGG, Reactome, GO

Data is automatically downloaded to the specified `path` on first use.

### 6. MCP Server Integration

Extend biomni with external tools via Model Context Protocol:

```python
# MCP servers can provide:
# - FDA drug databases
# - Web search for literature
# - Custom biomedical APIs
# - Laboratory equipment interfaces

# Configure MCP servers in .biomni/mcp_config.json
```

### 7. Evaluation Framework

Benchmark agent performance on biomedical tasks:

```python
from biomni.eval import BiomniEval1

evaluator = BiomniEval1()

# Evaluate on specific task types
score = evaluator.evaluate(
    task_type='crispr_design',
    instance_id='test_001',
    answer=agent_output
)

# Access evaluation dataset
dataset = evaluator.load_dataset()
```

## Guardrails
- Respect tool/data licenses when selecting Light vs Commercial mode.
- Track provenance (tool versions, dataset snapshots) in final response.
- Keep workflows modular -- reuse Biomni recipes rather than ad-hoc scripts when possible.
- Run in isolated environments (Docker, VMs) for production.
- Avoid exposing sensitive credentials to LLM-generated code.

## Best Practices

### Task Formulation
- **Be specific** - Include biological context, organism, cell type, conditions
- **Specify outputs** - Clearly state desired analysis outputs and formats
- **Provide data paths** - Include file paths for datasets to analyze
- **Set constraints** - Mention time/computational limits if relevant

### Security Considerations
- **Important**: Biomni executes LLM-generated code with full system privileges. For production use:
  - Run in isolated environments (Docker, VMs)
  - Avoid exposing sensitive credentials
  - Review generated code before execution in sensitive contexts
  - Use sandboxed execution environments when possible

### Performance Optimization
- **Choose appropriate LLMs** - Claude Sonnet 4 recommended for balance of speed/quality
- **Set reasonable timeouts** - Adjust `default_config.timeout_seconds` for complex tasks
- **Monitor iterations** - Track `max_iterations` to prevent runaway loops
- **Cache data** - Reuse downloaded data lake across sessions

### Result Documentation
```python
# Always save conversation history for reproducibility
agent.save_conversation_history("results/project_name_YYYYMMDD.pdf")

# Include in reports:
# - Original task description
# - Generated analysis code
# - Results and interpretations
# - Data sources used
```

## Resources

### References
Detailed documentation available in the `references/` directory:

- **`api_reference.md`** - Complete API documentation for A1 class, configuration, and evaluation
- **`llm_providers.md`** - LLM provider setup (Anthropic, OpenAI, Azure, Google, Groq, AWS)
- **`use_cases.md`** - Comprehensive task examples for all biomedical domains

### Scripts
Helper scripts in the `scripts/` directory:

- **`setup_environment.py`** - Interactive environment and API key configuration
- **`generate_report.py`** - Enhanced PDF report generation with custom formatting

### External Resources
- **GitHub**: https://github.com/snap-stanford/biomni
- **Web Platform**: https://biomni.stanford.edu
- **Paper**: https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1
- **Model**: https://huggingface.co/biomni/Biomni-R0-32B-Preview
- **Evaluation Dataset**: https://huggingface.co/datasets/biomni/Eval1

## Troubleshooting

### Common Issues

**Data download fails**
```python
# Manually trigger data lake download
agent = A1(path='./data', llm='your-llm')
# First .go() call will download data
```

**API key errors**
```bash
# Verify environment variables
echo $ANTHROPIC_API_KEY
# Or check .env file in working directory
```

**Timeout on complex tasks**
```python
from biomni.config import default_config
default_config.timeout_seconds = 3600  # 1 hour
```

**Memory issues with large datasets**
- Use streaming for large files
- Process data in chunks
- Increase system memory allocation

### Getting Help

For issues or questions:
- GitHub Issues: https://github.com/snap-stanford/biomni/issues
- Documentation: Check `references/` files for detailed guidance
- Community: Stanford SNAP lab and biomni contributors
