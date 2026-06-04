---
name: bulk-rnaseq-geo-download-survival
description: Use when the user references `生信教程` 第3课附近的 GEO 下载、生存曲线起步、`getGEO`、`getGPL`、`series_matrix` 获取和课堂示例 `GSE12417` / `gset` 保存流程。
---

# 生信教程 GEO 下载与生存分析入门

## Overview

这个 skill 覆盖教程里从 GEO 拉取表达矩阵、保存中间对象 `gset`、并衔接到基础生存分析输入准备的部分。

## Use This Skill When

- 用户点名 `生信教程` 第3课、`geo第三节课`、`生存曲线`、`getGEO` 或 `getGPL`。
- 需要把 GEO 下载脚本改写成适配当前数据编号或缓存路径的版本。
- 需要复用教程里 `gset` / `ExpressionSet` 的处理方式。

## Workflow

- 从 `references/source-map.md` 中选最接近的 GEO 示例脚本。
- 确认 GEO 编号、是否下载 GPL 注释、是否需要保存 `.rdata` 中间结果。
- 把教程里的 `destdir`、`setwd`、缓存文件名替换成当前项目目录。
- 如果任务进一步进入矩阵清洗、探针注释或差异分析，切换到对应 bulk skill。

## Boundaries

- 重点是 GEO 下载、缓存与基础生存分析输入准备。
- 表达矩阵网页文件读取不在这里，交给 `bulk-rnaseq-expression-matrix-import`。

## Output Rules

- 产出可执行的 GEO 下载 / 缓存脚本。
- 说明 `ExpressionSet`、`exprs`、`pData` 这些对象后面如何接下游流程。

## Adaptation Notes

- 教程脚本里 `getGPL = F/T` 是课堂演示重点，改写时不要丢。
- 如果用户网络不稳，优先保留教程中“先下载网页文件再本地读取”的替代路径。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
