---
name: bulk-rnaseq-immune-infiltration
description: Use when the user references `生信教程` 的 `estimate`、`免疫浸润`、`CIBERSORT.R`、`LM22` 签名矩阵或 bulk 肿瘤微环境估计流程。
---

# 生信教程 bulk 免疫浸润与 ESTIMATE / CIBERSORT

## Overview

这个 skill 管理教程里的免疫浸润估计代码，包括 ESTIMATE、CIBERSORT 和其配套的 `LM22` 支持文件。

## Use This Skill When

- 用户提到 `estimate`、`CIBERSORT`、`LM22`、`免疫浸润` 或肿瘤微环境评分。
- 需要把课堂里的 bulk 浸润分析迁移到当前表达矩阵。
- 需要确认 CIBERSORT 辅助文件如何组织。

## Workflow

- 先查看 `references/source-map.md`，确认是 ESTIMATE、CIBERSORT 还是两者串联。
- 明确输入矩阵格式是否已转成基因行为、样本列的表达矩阵。
- 对 `LM22`、公共函数脚本和工作目录做真实路径替换。
- 如果前面的矩阵清洗未完成，先切回相应 bulk skill。

## Boundaries

- 只负责 bulk 免疫浸润和微环境评分。
- 不承担单细胞细胞通讯或单细胞 marker 打分。

## Output Rules

- 返回可执行的 ESTIMATE / CIBERSORT 脚本。
- 列出需要额外下载或同目录放置的支持文件。

## Adaptation Notes

- `LM22.txt` 是配套签名矩阵，不要遗漏。
- `CIBERSORT.R` 来自第三方脚本，落地时要保留其独立调用方式。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
