---
name: bulk-network-wgcna
description: Use when the user references `生信教程` 的 `bulk.wgcna`、bulk 共表达网络构建、GEO 元数据整理和 WGCNA 模块-性状分析流程。
---

# 生信教程 bulk WGCNA

## Overview

这个 skill 负责教程里的 bulk WGCNA 路线，从 GEO 元数据整理到模块构建。

## Use This Skill When

- 用户提到 `bulk.wgcna`、`WGCNA`、模块与性状关联、教程第25课 bulk 网络。
- 需要把 GEO bulk 队列接到 WGCNA。
- 需要沿用教程对 metadata 的整理方式。

## Workflow

- 先看 `references/source-map.md` 的代表脚本。
- 确认 GEO 编号、表达矩阵格式和 traits 字段。
- 把课堂路径、`getGEO` 调用和 traits 构造改成当前项目数据。
- 如果任务是单细胞伪细胞 WGCNA，改用单细胞网络 skill。

## Boundaries

- 这里只做 bulk WGCNA。
- 单细胞 WGCNA 与 NMF 不在这里。

## Output Rules

- 返回 bulk WGCNA 准备与主线代码。
- 提示表达矩阵方向、traits 整理和软阈值选择仍需结合真实数据调整。

## Adaptation Notes

- 教程脚本里 GEO metadata 字段拆分很依赖原始 `characteristics_ch1` 格式。
- 换 GEO 数据集时 traits 提取逻辑通常需要重写。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
