---
name: scrna-cell-communication
description: Use when the user references `生信教程` 的 `CellChat`、`iTALK`、`NicheNet`、`CellPhoneDB`、配体受体网络 `.rds` 文件或细胞互作分析流程。
---

# 生信教程 单细胞细胞通讯分析

## Overview

这个 skill 汇总教程里的细胞通讯路线：CellChat、iTALK、NicheNet、CellPhoneDB 及其配套网络资源文件。

## Use This Skill When

- 用户提到 `CellChat`、`CellPhoneDB`、`iTALK`、`NicheNet`、`细胞互作`。
- 需要从已有 Seurat 对象出发构造通讯分析输入。
- 需要处理教程自带的 ligand-target / network `.rds` 辅助文件。

## Workflow

- 先查 `references/source-map.md`，确定要走哪条通讯工具链。
- 确认表达矩阵、细胞类型标签、样本分组和所需支持网络文件。
- 将课堂里的抽样、对象名、支持文件路径改写成当前项目设置。
- 如果细胞类型还没注释好，应先回到注释相关 skill。

## Boundaries

- 这里只做细胞通讯工具链。
- CNV、轨迹、SCENIC 与 module score 归其他单细胞技能。

## Output Rules

- 返回对应工具的可执行代码和输入格式说明。
- 列出依赖的 `.rds` 网络资源与 celltype 字段。

## Adaptation Notes

- NicheNet / CellChat 依赖较多，落地时要先检查安装来源和版本。
- 教程里有随机抽样步骤，若用户要求复现性，要补 `set.seed`。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
