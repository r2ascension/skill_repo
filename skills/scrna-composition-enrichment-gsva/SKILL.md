---
name: scrna-composition-enrichment-gsva
description: Use when the user references `生信教程` 的单细胞 `比例图`、单细胞差异后 `富集分析`、`GSVA` / `AUC` / 火山图可视化或课件里的下游展示代码。
---

# 生信教程 单细胞比例图、富集与 GSVA/AUC 可视化

## Overview

这个 skill 汇总教程里围绕单细胞 celltype 组成、对比富集、GSVA/AUC 风格展示的下游可视化代码。

## Use This Skill When

- 用户提到 `比例图`、单细胞 `富集分析`、`可视化-火山图-gsva-auc`。
- 需要比较不同样本中 celltype 组成比例。
- 需要从单细胞 DEG 或打分结果画出下游展示图。

## Workflow

- 先读 `references/source-map.md` 选择比例图、富集还是 GSVA/AUC 展示脚本。
- 确认对象中的 `celltype`、`orig.ident` 与分组字段是否齐全。
- 把课堂里的比较对象、颜色向量和 GMT/geneset 文件改成当前项目版本。
- 若缺少 marker 或 celltype 注释，先回到前序单细胞技能准备对象。

## Boundaries

- 这里只负责单细胞下游展示。
- bulk 富集、自动注释、SCENIC、轨迹和细胞通讯分别归其他技能。

## Output Rules

- 返回比例图、GSEA/GSVA/AUC 展示代码。
- 说明依赖的 metadata 字段、gene set 文件和比较组定义。

## Adaptation Notes

- 教程中同一份富集代码在 15、17 节课重复出现，优先保持一个统一版本。
- 如果用户明确说 `ssGSEA` 不可靠，要把展示改为更合适的替代方案，而不是硬套课堂脚本。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
