---
name: scrna-rna-velocity
description: Use when the user references `生信教程` 的 `velocity.txt`、`velocyto.R`、`SeuratWrappers`、速度场分析或从 loom / spliced-unspliced 结果出发的单细胞动态流程。
---

# 生信教程 单细胞 RNA Velocity

## Overview

这个 skill 负责教程里的 RNA velocity 相关依赖、对象转换和运行框架。

## Use This Skill When

- 用户提到 `velocity`、`velocyto.R`、`SeuratWrappers`、单细胞速度场。
- 需要把教程里的 velocity 依赖装起来并接到 Seurat 对象上。
- 需要解释为什么 velocity 依赖额外的 spliced / unspliced 输入。

## Workflow

- 先读 `references/source-map.md` 的 velocity 脚本。
- 确认是否已有 loom、spliced/unspliced 矩阵或 velocyto 输出。
- 把教程中的安装命令、对象名和 reduction 调用改成当前环境。
- 如果用户其实只需要轨迹分析，优先改用 Monocle skill。

## Boundaries

- 这里只做 RNA velocity。
- Monocle 轨迹和 NMF 程序发现不在这里。

## Output Rules

- 返回 velocity 依赖安装和基础分析代码。
- 明确列出额外所需输入文件类型。

## Adaptation Notes

- 教程脚本主要是依赖和入口说明，不代表单靠现有 `.RData` 就能跑完整 velocity。
- 如果没有 spliced/unspliced 数据，必须先告诉用户这一点。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
