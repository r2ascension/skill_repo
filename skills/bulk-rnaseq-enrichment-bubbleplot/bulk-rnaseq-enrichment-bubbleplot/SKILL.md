---
name: bulk-rnaseq-enrichment-bubbleplot
description: Use when the user references `生信教程` 里的 `通路富集`、`自定义画气泡图`、`airway` 示例、`annotables_grch38` 注释表或 bulk 结果下游富集可视化。
---

# 生信教程 bulk 富集分析与气泡图

## Overview

这个 skill 覆盖教程中 bulk DEG 之后的通路富集、GSEA 风格输入、以及课堂自定义气泡图的可视化套路。

## Use This Skill When

- 用户提到 `通路富集`、`自定义画气泡图`、`GeneRatio` 解析、`airway` 练习数据。
- 需要复用课堂富集结果表去画 bubble plot。
- 需要按教程方式把 bulk 差异结果接到富集分析。

## Workflow

- 先从 `references/source-map.md` 选富集脚本还是气泡图脚本。
- 确认输入是 DEG gene list、富集结果表，还是课堂 `airway` 示例矩阵。
- 把 `read.table` / `read.csv` 的输入文件替换成用户现有结果，保留教程绘图参数结构。
- 如果上游 DEG 还没完成，先回到 `bulk-rnaseq-deg-design-visualization`。

## Boundaries

- 只负责 bulk 下游富集与气泡图表达。
- 单细胞富集和 GSVA/AUC 风格展示交给单细胞技能。

## Output Rules

- 返回富集分析或 bubble plot 代码。
- 指出依赖的注释表、`GeneRatio` 列格式和富集结果字段名。

## Adaptation Notes

- 课堂 `airway` 示例同时依赖 counts、metadata 和 annotables，多文件要一起迁移。
- 真实结果表的列名经常不同，不能假设一定叫 `GeneRatio` 或 `p.adjust`。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
