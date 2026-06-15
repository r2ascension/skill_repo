---
name: bulk-rnaseq-geo-r-basics
description: Use when the user references `生信教程` 第1-2课的 R 基础、包安装、GEOquery 入门、工作目录设置，或想按教程风格快速搭好 bulk RNA / GEO 的 R 运行环境。
---

# 生信教程 GEO / R 基础入门

## Overview

这是 `生信教程` 前两课的源材料型 skill，聚焦 R 环境初始化、常见包安装方式、GEOquery 基本加载习惯，以及教程里反复出现的开场模板。

## Use This Skill When

- 用户提到 `生信教程` 第1课、第2课、`geo的第一二课`、`R基础`、`GEOquery 入门`。
- 需要复用教程里的 `Sys.setenv` / `options(stringsAsFactors = FALSE)` / `rm(list = ls())` 开场模板。
- 需要把教程中的包安装与工作目录设置改写成当前机器可运行的版本。

## Workflow

- 先读 `references/source-map.md`，确认要沿用哪一份基础脚本。
- 保留教程的初始化顺序，但把硬编码 `setwd(...)` 改成用户当前真实路径。
- 把过时或注释掉的安装命令补成今天可运行的写法，但不要擅自改掉教程分析意图。
- 如果后续任务进入 GEO 下载、表达矩阵读取或差异分析，切换到对应更专门的 skill。

## Boundaries

- 只负责基础 R / GEO 启动模板与安装习惯。
- GEO 下载、生存分析、表达矩阵读取、差异分析分别交给相邻的 bulk skills。

## Output Rules

- 产出可直接运行的 R 启动脚本或安装脚本。
- 显式标出需要用户替换的数据目录、GEO 编号或包版本。

## Adaptation Notes

- 教程里大量 `setwd("C:/shangke/..." )` 只是课堂路径占位符，落地时必须替换。
- 如果用户环境里没有 `BiocManager`、`devtools` 或 `remotes`，要先补安装步骤。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
