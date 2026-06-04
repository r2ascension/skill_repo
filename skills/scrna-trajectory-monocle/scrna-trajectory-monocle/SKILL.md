---
name: scrna-trajectory-monocle
description: Use when the user references `生信教程` 第17-19课的 `monocle2`、`monocle3`、伪时序、轨迹重建或从 Seurat 对象转到 Monocle 分析的流程。
---

# 生信教程 单细胞轨迹分析（Monocle2 / Monocle3）

## Overview

这个 skill 覆盖教程中的 Monocle2 / Monocle3 轨迹分析路线，包括从 Seurat counts 和 metadata 构造轨迹对象。

## Use This Skill When

- 用户提到 `monocle2`、`monocle3`、`轨迹`、`伪时序`、第17课细胞轨迹。
- 需要把 Seurat 对象转换成 Monocle 输入结构。
- 需要复用课堂里针对特定 cluster 子集的轨迹分析代码。

## Workflow

- 先从 `references/source-map.md` 选 Monocle2 还是 Monocle3 版本。
- 确认输入对象、子集细胞、特征基因和元数据字段。
- 把课堂里的 `load(...)`、`subset(...)`、对象名替换成当前项目版本。
- 如果用户还要 RNA velocity，请转到专门的 velocity skill。

## Boundaries

- 这里只做 Monocle 轨迹分析。
- velocity、CellChat、CNV 与手动注释不在这里。

## Output Rules

- 返回 Monocle2 / Monocle3 轨迹代码。
- 说明从 Seurat 到 Monocle 需要哪些槽位与元数据字段。

## Adaptation Notes

- Monocle2 和 Monocle3 API 不同，不能混写。
- 教程里部分脚本默认已有整合对象，需要先确认上游对象准备好。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
