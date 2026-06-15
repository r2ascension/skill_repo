---
name: scrna-sctransform-qc
description: Use when the user references `生信教程` 里的 `sct.txt`、SCTransform 前后基础处理、计数矩阵抽取、Seurat QC 起步或第12-14课相关标准化片段。
---

# 生信教程 单细胞 SCT 标准化与基础 QC

## Overview

这个 skill 负责教程中围绕 `sct.txt` 的单细胞标准化前处理与基础 QC 脚本。

## Use This Skill When

- 用户提到 `sct`、`SCTransform`、单细胞标准化、课上 `sct.txt`。
- 需要从 Seurat 对象的 counts 出发做后续 SCT 风格分析准备。
- 需要保留课堂里针对 `BC21` 等目录的处理框架。

## Workflow

- 先读 `references/source-map.md` 选择最完整的 `sct` 脚本。
- 确认输入是 10x 目录还是已存在的 Seurat 对象。
- 将课堂路径和样本项目名改成当前任务的真实值。
- 如果任务目标是整合或注释，完成基础标准化后切换到相邻 skill。

## Boundaries

- 只做 SCT 相关前处理与基础 QC。
- 整合、注释和 marker 展示不在这里。

## Output Rules

- 返回单细胞标准化起步代码。
- 标出最依赖数据路径和样本名的几行设置。

## Adaptation Notes

- 教程文件名叫 `sct`，但实际落地时可能是 `SCTransform` 或标准 NormalizeData 流程，需按用户要求调整。
- 不要默认课堂中的 `BC21` 仍然存在。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
