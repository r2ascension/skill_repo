---
name: scrna-literature-method-figure-patterns
description: Use when the user references `deep-research-report (5).md`, the checked single-cell literature inside it, or asks to write `Methods` / figure logic by imitating these literature-derived scRNA-seq study patterns.
---

# Deep Report 单细胞文献方法与图表套路

## Overview

这个 skill 不是通用 Seurat 教程，而是把 `deep-research-report (5).md` 里那批代表论文的研究设计、分析链路和图表逻辑整理成一个 source-specific overlay。

## Use This Skill When

- 用户提到 `deep-research-report (5).md`、这批单细胞文献、或“按这些论文写 methods”。
- 需要把结果图反推成方法学段落。
- 需要按 atlas / 新亚群 / 单基因通路 / 轨迹 / 免疫微环境 / 空间整合 这些论文套路组织单细胞分析。

## Workflow

- 先读 `references/source-map.md`，确认要参考的报告和核对过的原始论文。
- 再读 `references/literature-method-summary.md`，先选最接近的论文 archetype。
- 按固定槽位写方法，不要直接照抄论文：
  - 样本与分组
  - 测序/多组学平台
  - 质控、归一化、降维与聚类
  - 细胞注释与 marker 验证
  - 主题特异分析
  - 外部验证或空间/实验验证
- 如果用户要“按图写方法”，先从图类型回推分析链：
  - `UMAP/TSNE + marker heatmap/dotplot` -> 聚类、注释、marker 筛选
  - `比例柱图/堆积图` -> composition / abundance comparison
  - `FeaturePlot/Violin/Boxplot` -> 基因或 signature scoring
  - `trajectory` -> pseudotime / lineage inference
  - `network/chord/cell-cell communication` -> ligand-receptor analysis
  - `spatial map` -> scRNA 与 Visium / Slide-seq 映射

## Archetype Routing

- `atlas`：适合大样本、多组织或多阶段景观图谱。
- `single-gene-or-pathway`：适合靶基因、通路、干性或预后相关主线。
- `new-subcluster`：适合恶性亚群、免疫亚群、巨噬细胞亚型等发现。
- `trajectory`：适合疾病进展、分化、恶性转化连续体。
- `immune-communication`：适合 TME、配体受体和免疫状态比较。
- `spatial-integration`：适合 Visium、Slide-seq 或空间验证。
- `clinical-multiomic-atlas`：适合临床队列、多条件刺激、CAR-T 等多组学场景。

## Boundaries

- 这个 skill 负责“文献套路”和“methods 写法”。
- 具体 Seurat/Harmony/Monocle/CellChat 执行代码，优先交给已有单细胞技能。
- 如果用户要的是通用入门流程，不要被这份报告绑死。

## Output Rules

- 输出应优先给出一版可直接放进手稿的 `Methods` 骨架。
- 明确哪些步骤来自文献共性，哪些是针对当前项目的改写。
- 如果报告里的作者名、年份或标题简称和原文不一致，按核对后的论文信息写。

## Adaptation Notes

- 这批论文的方法高度重复，优先抽象共通骨架，再补主题特异步骤。
- 不要机械复述细胞数、样本数或软件版本，除非用户明确要复现某一篇。
- 写法上保留“论文味”，但要替换成当前项目真实样本、分组、对象名和验证方式。

## Resources

- Read `references/source-map.md` first to locate the local report and the verified paper list.
- Read `references/literature-method-summary.md` for the checked bibliography, report corrections, and per-archetype method templates.
