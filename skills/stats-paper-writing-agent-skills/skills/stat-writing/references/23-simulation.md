# Simulation study guidance (ADEMP)

Simulation sections are often where statistical papers fail: too many scenarios, unclear goals, or tables with no narrative.

Use **ADEMP** to structure the section:
- **A**im
- **D**ata generating mechanism
- **E**stimand
- **M**ethods compared
- **P**erformance measures

## ADEMP checklist
### Aim
- What do you want to learn? (robustness, finite-sample bias, CI coverage, power, runtime, etc.)

### Data generating mechanism
- Describe the generative model in words (and optionally compact notation).
- Give the parameter values, distributions, sample sizes, correlation structures, and missingness mechanisms.
- Keep scenarios limited and motivated.

### Estimand
- Define the target parameter for the simulation.
- If multiple estimands, say why.

### Methods
- List methods compared (baseline + competitors + your method).
- Make sure each is implemented fairly and tuned appropriately.

### Performance measures
- Bias, RMSE/MSE, coverage, type I error, power, interval width, runtime.
- Report Monte Carlo error where feasible (or at least number of replicates).

## Reporting tips
- State the number of Monte Carlo replications and any random seed policy.
- Use tables/figures, but also include narrative: highlight *the main pattern*.
- Don’t bury the key message in a 20×20 table.

## Common reviewer complaints
- “Unrealistic simulations.” → Motivate scenarios based on the application.
- “Too many scenarios, no story.” → Reduce and add narrative.
- “No competitors.” → Include the main baselines.

## Output format hints
- Use a short subsection structure: Setup → Results → Summary.
- Reference key tables/figures explicitly in the text.
