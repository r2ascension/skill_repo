---
name: scientific-agent-skills
description: Broad router for scientific coding and research-computing skills. Trigger for MATLAB or Octave work, Matplotlib or Seaborn plotting, scientific visualization, signal processing, numerical analysis, and similar research scripting tasks when no narrower child skill is already obvious.
---

# scientific-agent-skills

Use this collection router when:
- the user wants help with MATLAB, Octave, Matplotlib, Seaborn, Plotly, or related scientific tooling
- the task is about research figures, scientific computing, signal processing, simulation, or analysis scripts
- the user names a K-Dense scientific skill pack or asks for a scientific coding skill without specifying the exact child skill

Routing guidance:
- Route to the closest child skill under `scientific-agent-skills/skills`, such as `matlab`, `matplotlib`, or `signal-processing`.
- Prefer a child skill over the collection wrapper once the exact tool or workflow is clear.
- Use this wrapper mainly as the entry point for scientific-computing tasks that need discovery.

Merge and precedence notes:
- `claude-scientific-skills` should be treated as an alias of this collection, not a separate pack.
- If both names appear, route into this collection once and then pick the best child skill.

Examples in this collection:
- scientific-agent-skills/matlab
- scientific-agent-skills/matplotlib
- scientific-agent-skills/seaborn
- help me make a research plot in Matplotlib
