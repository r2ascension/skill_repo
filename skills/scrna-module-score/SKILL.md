---
name: scrna-module-score
description: Use when the user references `生信教程` 的 `addscore.txt`、`AddModuleScore`、通路 signature 打分或把基因集映射到单细胞对象的流程。
---

# 生信教程 单细胞模块打分

## Overview

这个 skill 专门处理教程里的单细胞模块打分和通路 signature 映射。

## Use This Skill When

- 用户提到 `AddModuleScore`、`addscore`、module score、signature 打分。
- 需要把 `msigdbr` 基因集拆成 list 后打到 Seurat 对象。
- 需要沿用课堂里 `KEGG` 基因集示例。

## Workflow

- 先看 `references/source-map.md` 中的代表脚本。
- 确认基因集来源、物种、Seurat 对象和输出 metadata 列名。
- 替换教程里的固定 gene set 子集与对象名。
- 如果后续还要 NMF 程序发现或 GSVA 展示，再切到相邻技能。

## Boundaries

- 这里只做 module score。
- NMF、velocity、细胞通讯和恶性细胞识别不在这里。

## Output Rules

- 返回 `AddModuleScore` 代码和 gene set 整理代码。
- 提醒输出列名会自动附带编号后缀。

## Adaptation Notes

- 课堂脚本只抽了一个 KEGG 集合作示例，真实使用时通常要换成用户指定 signature。
- 模块打分之前要确认对象使用的是哪个 assay / slot。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
