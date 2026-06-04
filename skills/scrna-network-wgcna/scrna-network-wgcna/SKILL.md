---
name: scrna-network-wgcna
description: Use when the user references `生信教程` 的 `sc.wgcna`、单细胞伪细胞 / metacell WGCNA、pseudocell 构建或单细胞网络模块分析流程。
---

# 生信教程 单细胞伪细胞 WGCNA

## Overview

这个 skill 汇总教程中把单细胞对象压缩成伪细胞后进行 WGCNA 的路线。

## Use This Skill When

- 用户提到 `sc.wgcna`、pseudocell、单细胞 WGCNA、模块网络。
- 需要把 Seurat 对象先做注释再生成伪细胞矩阵。
- 需要沿用教程的 pseudocell 聚合和变量基因筛选思路。

## Workflow

- 先读 `references/source-map.md` 确认完整脚本。
- 检查对象是否已有 celltype / cluster 注释，必要时先走自动注释 skill。
- 把课堂里的抽样、伪细胞大小、变量基因和输出目录改成当前任务需求。
- 确认用户是否接受 WGCNA 对样本量和计算资源的要求。

## Boundaries

- 这里只做单细胞伪细胞 WGCNA。
- bulk WGCNA、SCENIC、NMF 和 CNV 不是本 skill 范围。

## Output Rules

- 返回 pseudocell 构建与 WGCNA 主线代码。
- 提示伪细胞大小、过滤阈值和相关性方法要结合数据规模调参。

## Adaptation Notes

- 教程脚本里先用 SingleR 注释再做网络，这一步不要漏。
- 伪细胞构建部分对 cell 数很敏感，真实数据需重新看 `pseudocell.size`。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
