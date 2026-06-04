---
name: bulk-rnaseq-expression-matrix-import
description: Use when the user references `生信教程` 里网页下载表达矩阵、`fread` 读入 `series_matrix` / `phe.txt`、手动整理 phenotype 与表达矩阵列名的步骤。
---

# 生信教程 GEO 表达矩阵网页下载读取

## Overview

这个 skill 处理教程中直接从网页下载文本表达矩阵并用 `data.table::fread` 整理样本注释、表达矩阵和表头的套路。

## Use This Skill When

- 用户提到 `网页下载的表达矩阵读取`、`series_matrix` 手动读入、`phe.txt`、`fread`。
- 需要处理 GEO 网页下载得到的表达矩阵文本，而不是直接用 `getGEO`。
- 需要把课堂里拆行、转置、清洗 phenotype 的逻辑改成当前项目版本。

## Workflow

- 先读 `references/source-map.md`，锁定最接近的网页矩阵读取脚本。
- 确认样本注释文件、表达矩阵文件、跳过表头行数等细节。
- 把转置、去首行、列名修复等步骤改成当前文件的真实结构。
- 如果后续进入差异分析，转到 `bulk-rnaseq-deg-design-visualization`。

## Boundaries

- 只处理网页文本表达矩阵与 phenotype 读取整理。
- 芯片原始 CEL 级预处理不在这里。

## Output Rules

- 返回能直接读取当前矩阵文件的 R 代码。
- 提醒哪些步骤依赖文件头格式、分隔符或平台注释文件。

## Adaptation Notes

- 教程里 `fread` 参数较死板，真实文件经常要调整 `skip`、`header`、`sep`。
- 如果用户手头是 gzip / tsv / csv，不要机械照抄课堂文件名。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
