---
name: scientific-figure-decision
description: "Use when deciding or reviewing scientific figures (作图、审图) before plotting or revising manuscript, poster, lab-meeting, or talk visuals, especially bioinformatics figures such as volcano plots, heatmaps, PCA/UMAP, and enrichment plots where communication clarity matters more than raw statistical output."
---

# Scientific Figure Decision

## Overview

Good scientific figures are not just statistical output rendered as graphics. They are communication design. Use this skill **before** `scientific-visualization`, `nature-figure`, or `bizard` when you need to decide what a figure should say, how complex it should be, and whether it should even be a figure.

The governing question is:

> **这张图要让谁在几秒（或几分钟）内看懂什么？**

If you cannot answer that in one sentence, do not start drawing yet.

## When to Use

Use this skill when:
- You have results and need to decide **what plot to make**
- A draft figure feels technically correct but hard to understand
- The same result must be adapted for a **paper, poster, lab meeting, or talk**
- An auto-generated or AI-generated figure looks generic or overloaded
- You are unsure whether a **figure, table, or figure+table** is best
- You are reviewing bioinformatics visuals such as **volcano plots, heatmaps, PCA/UMAP, enrichment plots, Manhattan plots, or multi-panel omics figures**

Do **not** use this skill for low-level plotting syntax, journal export settings, or package-specific code generation. After the figure logic is settled, hand off to `scientific-visualization`, `nature-figure`, or `bizard`.

## First Move: write the figure contract

Before choosing any chart type, write one sentence in this format:

> This figure should help **[audience]** understand **[main message]** in **[time available]** during **[paper/poster/talk/meeting/interactive tool]**.

Examples:
- This figure should help **reviewers** understand **that interferon signaling is the main cross-tissue response** in **20-40 seconds** during **paper reading**.
- This figure should help **talk audience members** understand **that cluster separation is mostly batch, not biology** in **5 seconds** during **a live presentation**.
- This figure should help **poster viewers** understand **which 3 pathways matter most** in **15-30 seconds** during **a conference poster session**.

## The 5-step decision framework

### 1. Define the key message first

One figure should carry **one main conclusion**.

Ask:
- What should a reader say after the first glance?
- Which comparison, pattern, or uncertainty matters most?
- What can be removed without changing the conclusion?

Rules:
- Do not treat “all statistically significant outputs” as the message.
- Do not let software defaults decide the story.
- If multiple conclusions compete, split the figure.

**Bad:** “This heatmap shows the top 100 DE genes.”  
**Better:** “This heatmap shows that immune activation, not metabolism, separates responders from non-responders.”

### 2. Match complexity to time + interaction

Figure complexity should depend on how long the audience has and whether they can ask questions.

| Context | Time available | Interaction | Design implication |
|---|---|---|---|
| Paper | Medium to long | Low live interaction, high re-readability | Can include richer detail, but structure must be clean and layered |
| Lab meeting | Medium | High | Can show method choices, edge cases, and rawer views |
| Poster | Medium | Medium to high | Keep main panel simple; add details that can be explained verbally |
| Talk / public lecture | Short | Low | One message, large text, direct labels, minimal clutter |
| Interactive dashboard | Variable | High | Use overview first, then progressive disclosure for detail |

Practical rule:
- **Short time + low interaction = simplify aggressively**
- **Longer time and/or interaction = allow deeper detail**

### 3. Choose chart type and color by data structure, not habit

Pick a figure because it matches the structure of the information, not because it is common in the field.

#### Common decisions

| Communication goal | Usually prefer | Often avoid when | Why |
|---|---|---|---|
| Show distribution across samples | Dot plot, jitter, box plot, violin plot | Bar chart | Bars hide spread, outliers, and sample size |
| Show effect size / model estimate | Point + confidence interval | Bar chart | Point+CI better communicates uncertainty |
| Show trend over time | Line plot with uncertainty | Dense multi-line spaghetti without emphasis | Trend should stay readable |
| Show matrix-like patterns | Focused heatmap with grouped labels | Giant heatmap with everything | Too much matrix = too little message |
| Show set overlap | UpSet plot | Complex multi-set Venn | Venns fail quickly beyond a few sets |
| Show precise ranking with a few items | Lollipop plot or table | Bubble plot with too many encodings | Too many visual channels overload readers |

#### Color rules

Use color functionally:
- **Categorical palette** for distinct groups
- **Sequential palette** for ordered magnitude
- **Diverging palette** for deviation around a meaningful baseline

Avoid:
- Red-green as the only contrast
- Rainbow palettes for ordered values
- Decorative colors that do not encode information

Add backup encoding when needed:
- shape
- linetype
- annotation
- texture or pattern

### 4. Reduce cognitive load

The goal is not to maximize information volume. The goal is to maximize **useful signal per glance**.

Prefer:
- Direct labels instead of distant legends
- A small number of emphasized comparisons
- Muted non-essential elements
- Consistent encodings across panels

Reduce or remove:
- Unnecessary grid lines
- Heavy backgrounds and decorative shading
- Too many categories/colors
- Overlapping labels
- Panels that repeat the same message
- Exact numeric detail that belongs in a table

A strong figure often becomes stronger after deletion.

Useful review prompt:
> If I remove this element, does the main message become less clear? If not, delete or weaken it.

### 5. Ask whether a figure is necessary at all

Not every result deserves a figure.

Prefer a **table** when the priority is:
- exact values
- baseline characteristics
- model coefficients
- top hits with precise statistics
- parameter lists
- reference lookup

Prefer a **figure** when the priority is:
- pattern recognition
- distribution
- trend
- relationship
- comparison structure
- uncertainty at a glance

Prefer **figure + table** when:
- the figure gives the fast pattern
- the table provides exact values, transparency, or auditability

## Bioinformatics quick audit

Use this section when reviewing common omics figures.

| Figure type | Common weak version | Better version |
|---|---|---|
| Volcano plot | All genes shown, no labeling, threshold lines dominate | Highlight a small set of biologically central genes or modules; add direct labels; pair with DEG table if exact values matter |
| Heatmap | Top N DE genes chosen by software output only | Use genes/modules that support the biological story; group rows/columns meaningfully; reduce to focused panels when needed |
| PCA / UMAP | Separation shown without interpretation | State what likely drives separation (batch, tissue, treatment, biology); add variance explained or supporting annotation where relevant |
| Enrichment bubble plot | Many pathways with size/color/FDR/count all encoded at once | Keep only the pathways needed for the main claim; group themes; sort for readability; use bar/table if precision matters more |
| Expression bar chart | Mean-only bars for heterogeneous samples | Show sample-level variation with dots/box/violin when distribution matters |
| Large composite figure | Every panel equally sized and equally loud | Use a hero panel plus supporting panels; let panel importance follow argument importance |

## AI and auto-plotting warning

Auto-generated figures, including those produced by generative AI, are often good at turning data fields into chart primitives. They are much less reliable at modeling:
- communication intent
- audience context
- reading time
- interaction level
- cognitive load
- whether a table would be clearer

Treat automated plotting as a **draft generator**, not as the final figure strategist.

## Fast pre-flight checklist

Before you finalize any scientific figure, check:

- [ ] I wrote the main message in one sentence
- [ ] I know who the audience is
- [ ] I estimated how much time they have
- [ ] I estimated how interactive the setting is
- [ ] The chart type matches the data structure
- [ ] Color is encoding meaning, not decoration
- [ ] Non-essential clutter has been removed
- [ ] Direct labels are used where possible
- [ ] I considered whether a table would be clearer
- [ ] A non-expert or cross-background colleague could still read the main point

## Common failure modes

### “The plot is correct, so the figure is good.”
Correct is necessary, not sufficient. A correct figure can still communicate poorly.

### “Top N output = narrative.”
Software-ranked output is not the same thing as a scientific message.

### “I’ll use the same figure for paper and talk.”
Different time and interaction conditions require different complexity.

### “More detail = more rigorous.”
Sometimes more detail only means more noise.

### “A fancy plot is always better than a table.”
When exact lookup is the job, tables win.

## Hand-off

After the figure decision is clear:
- use `scientific-visualization` for plotting standards and export
- use `nature-figure` for submission-grade manuscript figure workflows
- use `bizard` for chart-type examples and biomedical plotting recipes

This skill answers **what the figure should do**. The other skills answer **how to draw it well**.
