# Tooling for statistical paper workflows

## Build and compile

Preferred command:

```bash
latexmk -pdf main.tex
```

Optional Makefile:

```make
paper:
	latexmk -pdf main.tex
clean:
	latexmk -C
```

## Review-ready manuscript checks

Before submission or revision:

- Enable line numbers in review draft.
- Ensure figures are vector when appropriate.
- Verify all labels/refs compile cleanly.
- Verify bibliography compiles cleanly.

## Reproducibility expectations

- Include code and data availability statement when possible.
- Provide supplement or repository instructions.
- Record random seeds and environment assumptions.
- Keep figure/table generation scripts versioned.

## Version control

- Use git from the start.
- Commit in small, meaningful units.
- Tag submission and revision states.

## Skill scripts

This skill includes:

- `scripts/check_tex.py` for manuscript heuristics.
- `scripts/check_bib.py` for citation/BibTeX consistency.
- `scripts/audit_paper.py` for combined audit.

Suggested run:

```bash
python scripts/audit_paper.py --tex main.tex --bib refs.bib
```

Fix HIGH findings first, then MED, then LOW.
