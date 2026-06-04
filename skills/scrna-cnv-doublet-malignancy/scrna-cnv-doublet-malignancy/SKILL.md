---
name: scrna-cnv-doublet-malignancy
description: Use when the user references `生信教程` 中 `copykat`、`infercnv`、`cell.cnv`、`science.cnv`、`DoubletFinder`、双细胞识别或恶性细胞推断流程。
---

# 生信教程 单细胞 CNV、双细胞与恶性细胞识别

## Overview

这个 skill 负责教程里和恶性细胞识别相关的单细胞下游：CNV 推断、copykat / infercnv / 自定义 genome-position 方案，以及双细胞过滤。

## Use This Skill When

- 用户提到 `copykat`、`infercnv`、`DoubletFinder`、`双细胞`、`恶性细胞`、`CNV`。
- 需要根据教程脚本对肿瘤单细胞对象做恶性细胞识别。
- 需要使用教程附带的基因组位置文件。

## Workflow

- 先读 `references/source-map.md`，确定是 copykat、infercnv、DoubletFinder 还是自定义 CNV 路线。
- 确认输入对象、参考细胞群、物种和基因位置文件。
- 把课堂里的 `.RData`、`human.gene.positions` 和参考数据路径改成当前目录。
- 如果用户只需模块打分或 velocity，不要混进这一套恶性细胞流程。

## Boundaries

- 这里只覆盖 CNV / 双细胞 / 恶性细胞识别。
- 细胞通讯、轨迹和 NMF 程序发现不在这里。

## Output Rules

- 返回恶性细胞识别脚本。
- 指出所需参考对象、位置文件和样本前提。

## Adaptation Notes

- `human.gene...positions` 是 inferCNV / 自定义 CNV 的关键支持文件，不要漏映射。
- 教程部分脚本默认已经筛出上皮/恶性细胞，真实使用前要先确认对象范围。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
