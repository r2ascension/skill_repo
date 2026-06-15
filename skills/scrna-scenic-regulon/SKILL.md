---
name: scrna-scenic-regulon
description: Use when the user references `生信教程` 第16课附近的 `scenic.txt`、SCENIC、AUCell / RcisTarget、motif feather 文件或单细胞调控网络分析流程。
---

# 生信教程 SCENIC 调控网络

## Overview

这个 skill 聚焦教程里的 SCENIC 调控网络流程及其重型依赖，包括 motif feather 文件和相关 Bioconductor 包。

## Use This Skill When

- 用户提到 `SCENIC`、`AUCell`、`RcisTarget`、motif feather 文件、教程第16课。
- 需要从单细胞表达对象进入 regulon 推断或活性打分。
- 需要确认教程附带的 `.feather` 资源如何组织。

## Workflow

- 先读 `references/source-map.md`，确认要用哪份 `scenic.txt` 和哪些 motif 资源。
- 检查当前环境是否具备足够内存、`arrow`、`AUCell`、`RcisTarget` 等依赖。
- 把课堂路径、feather 文件位置和对象名统一到当前项目目录。
- 如果只需要 downstream regulon 可视化，也要先说明上游 SCENIC 依赖重。

## Boundaries

- 这里只做 SCENIC / regulon 流程。
- 单细胞整合、轨迹和细胞通讯不在这里。

## Output Rules

- 返回 SCENIC 主流程或依赖检查代码。
- 列出必须和脚本同路径或可配置路径的 `.feather` 资源。

## Adaptation Notes

- 教程里附带的 motif `.feather` 文件非常大，迁移时不要复制错物种版本。
- 如果用户只有人类或小鼠数据，要明确选择对应 reference 文件。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
