---
name: scrna-manual-annotation-markers
description: Use when the user references `生信教程` 的 `手动注释`、`FindAllMarkers`、热图、marker 基因展示、细胞类型人工命名或第14-17课 marker 相关脚本。
---

# 生信教程 单细胞手动注释与 marker 展示

## Overview

这个 skill 负责教程里人工细胞类型命名、marker 提取、热图/UMAP 展示，以及承接整合对象后的人工注释步骤。

## Use This Skill When

- 用户提到 `手动注释`、`marker基因的展示`、`FindAllMarkers`、`DoHeatmap`。
- 需要从整合后的 `scRNA1` 或类似对象做人手注释与 marker 导出。
- 需要按教程风格出热图或按 celltype 上色的 UMAP。

## Workflow

- 先从 `references/source-map.md` 里确认是 marker 筛选、热图展示还是手动命名。
- 检查当前对象是否已有聚类结果和基础 celltype 字段。
- 改写教程里的 `load("scRNA1.Rdata")`、颜色向量和输出文件路径。
- 如果用户想继续做比例图或富集分析，可切到相邻技能。

## Boundaries

- 这里只做手工注释、marker 热图和 marker 导出。
- 自动注释工具链和 Harmony 整合不在这里。

## Output Rules

- 返回 marker 提取、热图和 celltype 标注代码。
- 提示依赖的对象名、聚类字段和输出文件位置。

## Adaptation Notes

- 教程里 `scRNA1.Rdata` 是缓存对象，不保证用户当前环境存在；必要时要回推到整合主线重建。
- 如果 celltype 水平和教程不一致，颜色向量与因子顺序都要同步改写。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
