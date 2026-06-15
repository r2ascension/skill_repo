---
name: scrna-annotation-automation
description: Use when the user references `生信教程` 中 `三种注释软件使用`、`SingleR`、`Garnett`、`CelliD`、`txt文件读取`、自动细胞类型注释或第12、19课的注释工具流程。
---

# 生信教程 单细胞自动注释工具箱

## Overview

这个 skill 汇总教程中的自动注释路线：SingleR 参考数据映射、Garnett 输入准备、CelliD 方案，以及相关支持读取脚本。

## Use This Skill When

- 用户提到 `三种注释软件使用`、`SingleR`、`Garnett`、`CelliD`、`自动注释`。
- 需要把参考数据集或 marker-based 注释工具接到现有 Seurat 对象上。
- 需要复用教程里从 `txt` 或参考对象构建注释输入的代码。

## Workflow

- 先从 `references/source-map.md` 里确认要走 SingleR、Garnett 还是 CelliD。
- 明确测试对象、参考对象和细胞标签字段。
- 把课堂路径、参考数据文件和输出列名替换成当前项目版本。
- 如果用户要求最终人工校正或 marker 复核，再交给手动注释相关 skill。

## Boundaries

- 这里只做自动或半自动注释工具链。
- Harmony 整合、marker 热图和手工细胞类型命名不在这里。

## Output Rules

- 返回自动注释脚本和参考对象要求。
- 提醒参考数据格式、`logcounts` 槽位和元数据字段依赖。

## Adaptation Notes

- 教程中 `SingleR` 和 `CelliD` 分布在多节课，落地时要先统一对象名。
- 如果没有参考对象或 marker 词典，需要先和用户确认可用资源。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
