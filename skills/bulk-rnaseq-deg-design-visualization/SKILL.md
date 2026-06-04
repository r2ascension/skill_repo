---
name: bulk-rnaseq-deg-design-visualization
description: Use when the user references `生信教程` 里的 `差异分析`、`差异分析+可视化`、分组矩阵设计、`design=model.matrix(...)` 或 bulk DEG 的课堂可视化步骤。
---

# 生信教程 差异分析设计矩阵与可视化

## Overview

这个 skill 覆盖 bulk 转录组差异分析里的分组设计、设计矩阵构造、课堂讲解文本，以及差异结果的基础可视化套路。

## Use This Skill When

- 用户提到 `差异分析`、`分组矩阵`、`design matrix`、`limma` 风格设计。
- 需要按教程风格构建对照组 / 多组比较设计矩阵。
- 需要把课堂差异分析脚本改到当前表达矩阵上。

## Workflow

- 先从 `references/source-map.md` 里确定是理论讲解、设计矩阵，还是完整差异分析脚本。
- 明确输入矩阵、分组向量和比较设计，再改写 `model.matrix` 与分组标签。
- 保留教程里的可视化和统计顺序，但用用户当前样本名与比较关系替换课堂样例。
- 如需上游表达矩阵整理或下游通路富集，切换到邻近 skill。

## Boundaries

- 负责 DEG 设计矩阵与差异分析主线。
- 通路富集 / 气泡图、免疫浸润、批次矫正分别归其他技能。

## Output Rules

- 返回可运行的 DEG 脚本和分组矩阵构造代码。
- 指出哪些比较关系、对照水平和样本顺序必须显式确认。

## Adaptation Notes

- 教程里的讲义文本解释很多，真正落地时要提炼成简洁可跑代码。
- 如果用户组别数量和教程不同，要重写 `group_list` 而不是硬套样本数。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
