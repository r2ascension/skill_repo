---
name: bulk-rnaseq-microarray-affy-preprocess
description: Use when the user references `生信教程` 里的 `芯片测序原始数据分析`、`affy`、CEL 文件读取、平台注释合并或课堂 microarray 原始预处理流程。
---

# 生信教程 芯片原始数据与 Affy 预处理

## Overview

这个 skill 负责教程中的 Affymetrix / 芯片原始数据读取与表达矩阵生成流程，适合从 CEL 或类似原始平台文件出发的场景。

## Use This Skill When

- 用户提到 `芯片测序原始数据分析`、`affy`、`CEL` 文件、平台注释或 microarray 原始预处理。
- 需要把教程的原始芯片输入流程改成当前样本目录。
- 需要从原始文件而不是现成表达矩阵开始。

## Workflow

- 先看 `references/source-map.md` 里的代表脚本，确认是 raw CEL 还是已导出的矩阵。
- 保留教程使用 `affy` / `GEOquery` / `tidyverse` 的基本顺序。
- 把课堂路径、样本文件夹和平台文件名改写为当前数据实际位置。
- 如果下游进入免疫浸润、差异分析或批次矫正，再切换到更专门的 skill。

## Boundaries

- 这里只做 microarray 原始读入与初步整理。
- 不覆盖 TCGA/GTEx、单细胞或 ChIP-seq 流程。

## Output Rules

- 返回 raw 芯片数据读取与基本清洗代码。
- 说明所需平台文件、CEL 目录结构和潜在内存需求。

## Adaptation Notes

- 课堂脚本里把 `affy` 安装写成注释，实际落地时要根据环境补安装。
- 如果数据不是 Affymetrix，应该明确指出教程脚本只能部分借鉴。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
