---
name: scrna-seurat-basics
description: Use when the user references `生信教程` 第9-11课附近的单细胞基础、10x 读取、`CreateSeuratObject`、课堂 R/Seurat 入门和最基本对象创建流程。
---

# 生信教程 单细胞 Seurat 基础入门

## Overview

这个 skill 是教程单细胞部分的入门层，负责 10x 数据读取、Seurat 对象创建、基础依赖安装和对象结构理解。

## Use This Skill When

- 用户提到 `单细胞基础`、`Read10X`、`CreateSeuratObject`、`生信教程` 第9-11课。
- 需要从 10x 目录开始搭起最基础的 Seurat 对象。
- 需要保留教程里的课堂入门节奏，而不是直接跳到更现代框架。

## Workflow

- 先看 `references/source-map.md`，确认是纯基础说明还是含实际对象构建的版本。
- 把教程里的 10x 输入目录替换成当前数据路径。
- 保留 `Seurat` / `patchwork` / `tidyverse` 的基础包结构，并根据当前 Seurat 版本做兼容提醒。
- 如果任务进入标准化、注释、整合或轨迹分析，切换到后续单细胞技能。

## Boundaries

- 这里只做单细胞入门与对象创建。
- SCT、Harmony、注释、SCENIC、轨迹等各自有专门 skill。

## Output Rules

- 返回最小可运行的 Seurat 入门代码。
- 提示 10x 目录结构、最小基因/细胞阈值和对象命名规则。

## Adaptation Notes

- 教程里的包安装写法偏课堂化，实际运行时要根据当前 Seurat 版本检查兼容性。
- 不要把这里和 SCT / Harmony 代码混在一起，先保住基础对象可用。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
