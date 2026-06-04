---
name: bulk-rnaseq-consensus-metabolic-subtyping
description: Use when the user references `生信教程` 第24/27课的 `ConsensusClusterPlus`、代谢亚型、糖酵解 / 胆固醇生物合成四象限分型或 bulk 队列亚型聚类流程。
---

# 生信教程 bulk 代谢亚型 ConsensusClusterPlus

## Overview

这个 skill 聚焦教程后段基于代谢基因集的 bulk 样本亚型聚类与四象限分型绘图。

## Use This Skill When

- 用户提到 `ConsensusClusterPlus`、代谢亚型、`glycolytic` / `cholesterogenic` 四象限。
- 需要根据 bulk 表达矩阵做样本聚类与亚型划分。
- 需要沿用教程里的 `stad.exp.rdata` 示例结构。

## Workflow

- 先读 `references/source-map.md` 确认代表脚本。
- 检查表达矩阵、基因集和抽样列范围是否与当前数据一致。
- 替换课堂里的 `stad.exp.rdata`、样本索引和颜色设置。
- 如果任务其实是单细胞 NMF，不要误用本 skill。

## Boundaries

- 这里只做 bulk 代谢亚型聚类。
- NMF 单细胞 program discovery 和 bulk WGCNA 不在这里。

## Output Rules

- 返回 ConsensusClusterPlus 聚类和四象限分型绘图代码。
- 标出需要人工复核 cluster 编号与亚型命名的步骤。

## Adaptation Notes

- 教程里某些 cluster 与亚型对应关系写在注释里，换数据后必须重新确认。
- 脚本默认样本列截取范围固定，迁移时应改成按元数据筛选而不是硬编码列号。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
