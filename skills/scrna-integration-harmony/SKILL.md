---
name: scrna-integration-harmony
description: Use when the user references `生信教程` 里多样本 10x 合并、`Harmony`、多目录 `Read10X`、第13-16课的整合脚本或单细胞批次整合流程。
---

# 生信教程 单细胞整合与 Harmony

## Overview

这个 skill 负责教程里多样本 Seurat 对象构建、合并、批次整合和 Harmony 驱动的主分析主线。

## Use This Skill When

- 用户提到 `harmony`、多样本整合、`CAFs.1` / `dapi1` 这类多目录输入、教程第13-16课代码。
- 需要把多个 10x 样本合并进统一对象并做整合。
- 需要保留教程里的样本命名、循环构建对象和整合习惯。

## Workflow

- 先读 `references/source-map.md`，确定用哪一版主流程代码。
- 确认样本目录列表、样本别名和要保留的元数据字段。
- 把循环读取、合并、整合和降维步骤改成当前项目的目录结构。
- 如果后续任务是 marker、比例图或下游通讯/CNV，再切换到后续单细胞 skill。

## Boundaries

- 这里只覆盖整合主线与 Harmony 级别批次处理。
- marker 注释、轨迹、SCENIC、通讯等在其他技能中处理。

## Output Rules

- 返回多样本整合与 Harmony 代码。
- 提示哪些 `.RData` 缓存或对象名是教程特有的，需要重建或重命名。

## Adaptation Notes

- 多份 `代码*.txt` 实际是同一条整合主线的不同拷贝，优先用 source map 中列出的代表版。
- 如果用户用的是 Seurat v5，需提醒 `Harmony` / assay API 可能略有不同。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
