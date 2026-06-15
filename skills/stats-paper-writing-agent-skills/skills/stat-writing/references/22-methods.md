# Methods section guidance

## Goal
A strong Methods section lets a reader understand **what is being estimated**, **under what assumptions**, **how it is estimated**, and **how uncertainty is quantified**.

## Principle: intuition before notation
Start with a plain-language overview (what the method does, what problem it solves) before introducing full notation.

## Minimum elements checklist
1. **Problem setup & estimand**
   - Define the target quantity (estimand) in words.
2. **Assumptions**
   - State modeling or identification assumptions explicitly.
3. **Notation**
   - Define symbols once, keep consistent.
4. **Model / procedure**
   - Specify the model or algorithm steps.
5. **Inference / uncertainty**
   - Standard errors, confidence intervals, tests, or posterior summaries.
6. **Tuning / implementation details**
   - Only what is necessary to reproduce.

## Suggested paragraph outline
1. High-level method summary.
2. Notation and data structure.
3. Model/estimand.
4. Estimation procedure.
5. Uncertainty + inference.
6. Practical notes (computation, hyperparameters, diagnostics).

## Writing tips
- Keep each paragraph focused on one idea.
- If you introduce new notation, define it immediately.
- If you compare to existing methods, explicitly state what differs.

## Output format tips (LaTeX)
- Use `\subsection{Method}` etc.
- Put long derivations in an appendix.

## Placeholders
- `\todo{define estimand}`
- `\todo{state assumptions}`
- `\todo{add algorithm pseudo-code}`

Never invent theoretical guarantees.
