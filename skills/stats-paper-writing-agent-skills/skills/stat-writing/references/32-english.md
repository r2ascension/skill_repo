# English usage pitfalls (common in statistical writing)

## Tense
- Use **present tense** for general statements and paper structure (“Section 2 describes …”).
- Use **past tense** for what you did (data collection, experiments) (“We collected …”, “We simulated …”).

## “significant”
Use “(statistically) significant” only when you mean statistical significance.
If you mean “large/important”, consider:
- substantial, pronounced, considerable, meaningful (context-dependent)

## “data”
In many scientific styles, “data” is treated as plural:
- “the data are …”, “these data show …”

## Clarity
- Prefer active voice when it improves clarity.
- Avoid long noun stacks (“high-dimensional sparse penalized regression estimator ...”).
- Define acronyms once, then reuse.

## Script check
`scripts/check_tex.py` flags:
- “data is/was/has”
- “significant” without “statistically” nearby
