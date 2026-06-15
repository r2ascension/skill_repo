---
name: genomics-sequencing-router
description: Second-level router for sequencing, alignment, genome, variant, and read-processing workflows. Trigger when the task is genomics or sequencing heavy and you need to choose among the large low-level bio file, alignment, variant, and genome skill families.
---

# genomics-sequencing-router

Use this router when:
- the request is about FASTQ, BAM, VCF, alignment, variant calling, reference handling, or genome assembly
- the task is genomics infrastructure or sequencing-file processing rather than downstream interpretation

Routing guidance:
- Use bio-alignment-*, bio-read-qc-*, bio-sequence-*, and bio-reference-* skills for file handling, QC, and alignment primitives.
- Use bio-variant-calling-* and bio-vcf-* skills for variant workflows.
- Use bio-learning-sequencing-and-data-submission when the user wants maintained learning content for FASTQ handling, data submission, or sequence-level onboarding rather than an immediate file-processing operation.
- Use bio-genome-assembly-*, bio-genome-annotation-*, or bio-genome-intervals-* when the task is assembly, annotation, or interval-centric.

Examples:
- route a FASTQ to BAM workflow
- which skill handles VCF filtering and variant calling
- I need the right genome assembly or annotation skill