---
name: scrna-nmf-programs
description: Use when the user references `生信教程` 的 `nmf.signature`、`nmf(2).txt`、`nmf.降维`、恶性上皮 program 提取、AUCell 打分或 NMF 替代 PCA 的单细胞降维流程。
---

# 生信教程 单细胞 NMF 程序发现与 NMF 降维

## Overview

这个 skill 负责教程里所有 NMF 相关单细胞内容：signature 提取、program 聚类、AUCell 打分，以及把 NMF 结果塞回 Seurat reduction 做降维。

## Use This Skill When

- 用户提到 `NMF`、`nmf.signature`、`nmf.降维`、program discovery、AUCell 打分。
- 需要对恶性上皮或特定细胞群做 NMF program 提取。
- 需要比较 PCA 与 NMF 因子的解释性。

## Workflow

- 先读 `references/source-map.md`，区分是 program 提取脚本还是 NMF 降维脚本。
- 确认输入矩阵、抽取细胞群、`rank` 参数和内存预算。
- 把课堂里的缓存文件、样本命名和输出子目录统一到当前项目路径。
- 若用户还需要恶性细胞筛选，先配合 CNV/双细胞 skill 完成上游对象准备。

## Boundaries

- 这里只做 NMF 程序发现与 NMF-based 降维。
- ConsensusClusterPlus 的 bulk 代谢分型不在这里。

## Output Rules

- 返回 NMF program discovery 或 NMF reduction 代码。
- 提醒这条流程内存占用高、参数 `rank` / `topn` 需要结合数据规模调整。

## Adaptation Notes

- 教程里 `nmf(2).txt` 和 `nmf.signature.txt` 是同一条主线的不同拷贝，要统一使用。
- 如果用户对象不是恶性上皮子集，不能直接照抄课堂脚本的解释口径。

## Resources

- Read `references/source-map.md` first to locate the exact tutorial files that belong to this skill.
- Treat these files as source-specific overlays for `生信教程`; preserve the tutorial intent, but rewrite hard-coded paths, cached object names, and obsolete install steps to match the user's real environment.
