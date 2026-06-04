---
name: chipseq-pipeline-and-annotation
description: Use when the user references `生信教程` 第21-23课附近的 `chipseq` conda 环境、SRA 下载、`parallel-fastq-dump`、`ChIPseeker`、deepTools、peak 注释与 TSS 热图流程。
---

# 生信教程 ChIP-seq 环境、下载与 peak 注释

## Overview

这个 skill 把教程里的 ChIP-seq 代码整理成一条完整链路：环境准备、SRA 数据下载、基础文件处理、peak 注释与 TSS 可视化。

## Use This Skill When

- 用户提到 `chipseq`、`parallel-fastq-dump`、`ChIPseeker`、`deepTools`、`bamCoverage`、`computeMatrix`。
- 需要从公开 SRA 数据开始搭一条 ChIP-seq 教程式流程。
- 需要对已得到的 peak 文件做注释、TSS 热图或 profile 图。

## Workflow

- 先读 `references/source-map.md`，区分是环境/下载部分还是注释/可视化部分。
- 确认目标系统是否为 Linux shell，conda 环境名和工具版本是否需要更新。
- 把课堂里的 SRA 编号、目录名、索引文件和 peak 文件名改成当前任务版本。
- 如果用户只需要 peak 注释，直接跳过下载部分，走 `ChIPseeker` / deepTools 子流程。

## Boundaries

- 这里只处理 ChIP-seq / peak 注释主线。
- bulk RNA、单细胞和 WGCNA 不在这里。

## Output Rules

- 返回 shell / R 混合的 ChIP-seq 流程代码。
- 明确哪些步骤依赖 Linux、conda、samtools 索引、bigWig 或 GTF 文件。

## Adaptation Notes

- 教程里有 `apt-get`、`sudo mv`、`wget` 等 Linux 命令，Windows 环境不能直接照抄。
- `第22节课.txt` 同时覆盖 ChIPseeker、deepTools 和 intervene，落地时按用户需求裁剪。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
