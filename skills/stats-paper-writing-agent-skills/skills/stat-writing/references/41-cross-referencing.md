# Labels and cross-referencing guidance

## Label conventions

Use prefix conventions consistently:

- `sec:` for sections
- `fig:` for figures
- `tab:` for tables
- `eq:` for equations
- `alg:` for algorithms
- `app:` for appendix items

Examples:

- `\\label{sec:methods}`
- `\\label{fig:simulation-rmse}`

## Placement rules

- Put `\\label{...}` after `\\caption{...}` for figures/tables.
- Keep labels unique across the project.

## Referencing in prose

- Use `Figure~\\ref{fig:...}`, `Table~\\ref{tab:...}`, `Section~\\ref{sec:...}`.
- Use `\\eqref{eq:...}` for equations.
- Avoid hard-coded references like "Figure 2" or "Table 3".

## Review-time checks

- Undefined references.
- Duplicate labels.
- Defined-but-unused labels.
- Prefix convention violations.

## Script

`python scripts/check_tex.py path/to/main.tex` flags these issues.
