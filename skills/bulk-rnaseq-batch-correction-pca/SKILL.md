---
name: bulk-rnaseq-batch-correction-pca
description: Use when the user references `生信教程` 的 `批次矫正`、`batchPCA.R`、样本批次可视化、批次前后质控或课堂 PCA 检查流程。
---

# 生信教程 批次矫正与 PCA 质控

## Overview

这个 skill 处理 bulk 数据里的批次效应矫正与 PCA 观察，包括教程自带的 `batchPCA` 函数和多份批次矫正脚本。

## Use This Skill When

- 用户提到 `批次矫正`、`PCA`、`batchPCA`、样本聚类偏移或批次效应。
- 需要把课堂里的批次矫正流程改写到当前 bulk 矩阵。
- 需要解释教程里的 PCA 图函数如何使用。

## Workflow

- 先读 `references/source-map.md`，区分是函数工具还是完整批次矫正脚本。
- 确认输入矩阵方向、批次向量顺序和输出图目录。
- 把教程函数调用参数替换成当前数据对象与批次标签。
- 如果任务还涉及差异分析设计，配合 `bulk-rnaseq-deg-design-visualization` 使用。

## Boundaries

- 这里只聚焦批次效应与 PCA 观察。
- 分组设计、免疫浸润与通路富集不在这里。

## Output Rules

- 返回批次矫正 / PCA 绘图代码。
- 说明样本顺序与批次向量必须严格对齐。

## Adaptation Notes

- 教程自带 `batchPCA` 依赖 `ClassDiscovery`，如果环境没有需提前说明。
- 课堂脚本里目录和图名是固定值，迁移时要一并改掉。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
