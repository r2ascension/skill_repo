# BibTeX, natbib, and compilation workflow

## Citation commands (natbib)

- `\\citep{KEY}`: parenthetical citation.
- `\\citet{KEY}`: textual citation.
- `\\citep[see][p.~26]{KEY}`: citation with notes.

Use citation commands consistently. Do not manually type author-year text.

## Build order

- Recommended: `latexmk -pdf main.tex`
- Manual sequence: `pdflatex -> bibtex -> pdflatex -> pdflatex`

## BibTeX hygiene checklist

- Stable key naming convention.
- No duplicate keys.
- Protect capitalization with braces for acronyms/proper nouns.
- Use page ranges with double dash (`110--118`).
- Fill required fields by type (`@article` volume/pages; `@book` publisher/address when style requires).
- Avoid literal `et al.` in author fields.
- Avoid duplicate DOI values across unrelated entries.

## JDS-aligned checklist

- Clean and minimal bibliography with only cited references.
- No noisy or malformed entries in submitted `.bib`.
- Ensure references can compile without manual edits.

## Script

Run:

```bash
python scripts/check_bib.py --tex main.tex --bib refs.bib
```

The script reports missing citations, unused entries, and hygiene warnings.

## Guardrail

Never invent citations. If a citation is needed but unknown, use `\\todo{add citation}`.
