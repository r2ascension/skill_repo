# Data section guidance

## Goal
Describe the data well enough that a reader understands:
- where the data came from,
- what population/time period it covers,
- what variables/outcomes are used,
- what preprocessing was done,
- and why the data are appropriate for the research question.

## Minimum contents checklist
1. **Source**: dataset name, owner, collection mechanism.
2. **Units and sample size**: number of subjects/rows/events, inclusion/exclusion criteria.
3. **Time/space coverage**: dates, geography, follow-up time.
4. **Outcomes and covariates**: define key variables.
5. **Missingness and filtering**: how much missing data, how handled.
6. **Ethics**: IRB/consent/de-identification if relevant.
7. **Exploratory summary**: key summary stats/plots that motivate the modeling.

## Writing tips
- Use **past tense** for data collection (what you did), present tense for general facts.
- Prefer a small number of informative figures/tables over long prose lists.
- If you transform variables, state the transformation and rationale.

## Output format hints (LaTeX)
- Use `\subsection{Data}` (or template section).
- Reference figures/tables in text (e.g., `Figure~\ref{fig:eda}`).

## Placeholders (if info missing)
If some details are unknown, insert:
- `\todo{report sample size}`
- `\todo{describe inclusion criteria}`

Never invent data details.
