---
name: bulk-rnaseq-tcga-gtex-analysis
description: Use when the user references `生信教程` 第5-7课附近的 TCGA/GTEx 联合分析、`TCGA-STAD`、临床表型与表达矩阵合并、肿瘤正常比较等 bulk 癌症队列步骤。
---

# 生信教程 TCGA / GTEx 联合表达分析

## Overview

这个 skill 聚焦教程中从 TCGA / GTEx 下载的临床表型、FPKM、probe map 整理，到课堂里的胃癌示例分析。

## Use This Skill When

- 用户提到 `TCGA`、`GTEx`、`TCGA-STAD`、癌症队列表达合并或教程第5课代码。
- 需要把教程的 bulk 癌症队列分析迁移到别的癌种或新目录。
- 需要处理 `phenotype.tsv.gz`、`htseq_fpkm.tsv.gz`、`probeMap` 这类输入。

## Workflow

- 先查 `references/source-map.md` 选用 TCGA/GTEx 主脚本或其后续讲义版。
- 确认癌种、样本筛选、临床字段与探针注释文件是否仍匹配。
- 把 `fread`、合并、列名处理和后续比较步骤改成当前项目路径。
- 如果后续要做富集、WGCNA 或亚型聚类，再切到对应 bulk skill。

## Boundaries

- 只覆盖 TCGA / GTEx 队列整理与表达主线。
- 不负责 GEO 微阵列原始读入或单细胞分析。

## Output Rules

- 返回适配当前癌种/目录的队列整理代码。
- 提醒下载文件命名、gzip 输入和样本 ID 对齐细节。

## Adaptation Notes

- 教程文件名用的是 STAD 示例，迁移时要系统替换癌种前缀。
- 如果用户只有 TPM / counts 而没有 FPKM，应该明确说明不能无脑照搬。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
