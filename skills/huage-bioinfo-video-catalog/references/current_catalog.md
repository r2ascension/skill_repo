# 华哥生信AI 生信技术视频清单

- 更新时间: `2026-06-14 23:42:51`
- 来源: Bilibili `华哥生信官方` (uid `405009023`)，使用 `opencli bilibili user-videos` 实时抓取
- 总投稿数: `63`
- 纳入生信技术范围: `59`
- 排除的非技术/宣传视频: `4`

## 简要概览

- `入门与环境`: `4` 条
- `Bulk RNA-seq / 芯片 / 公共数据库`: `9` 条
- `单细胞基础`: `17` 条
- `单细胞进阶`: `14` 条
- `空间与多组学`: `3` 条
- `Nature复现与科研复盘`: `9` 条
- `专题案例与扩展课`: `3` 条

## 推荐学习顺序

- 先看 `入门与环境`，补齐 R / RStudio / Jupyter / Linux / Conda 基础。
- 再看 `Bulk RNA-seq / 芯片 / 公共数据库`，建立差异分析、富集分析、TCGA/GEO 思路。
- 之后进入 `单细胞基础`，按读入 -> 质控 -> 整合 -> 聚类 -> 注释 -> 可视化 顺序学习。
- 掌握基础后看 `单细胞进阶`，补轨迹、细胞通讯、调控网络、CNV、RNA velocity。
- 再进入 `空间与多组学`，理解空转、ATAC、联合分析和空间映射。
- 最后看 `Nature复现与科研复盘` 和 `专题案例与扩展课`，把方法串到真实论文与案例里。

## 排除项

- `人工智能体一： OpenClaw 龙虾介绍， AI Agent 实战`: AI agent demo rather than a bioinformatics technique lesson
- `生信千人培训计划`: program announcement rather than a concrete technique lesson
- `Nature复现：课程亮点`: course promotion rather than a concrete technique lesson
- `华哥生信来b站啦`: account introduction rather than a concrete technique lesson

## 分组清单

### 入门与环境

- `2026-05-19` | [12 WSL2 Linux、Miniconda与RStudio Server环境搭建](https://www.bilibili.com/video/BV1nNL76oEb2) | 播放 `154` | 偏环境与工具准备，主要讲WSL2 Linux、Miniconda与RStudio Server环境搭建。
- `2026-05-06` | [01 R语言基础与RStudio、R包安装使用入门](https://www.bilibili.com/video/BV1uSRsBtEdC) | 播放 `525` | 偏环境与工具准备，主要讲R语言基础与RStudio、R包安装使用入门。
- `2026-04-11` | [2.R语言基础知识讲解](https://www.bilibili.com/video/BV1b9QKBwEUc) | 播放 `219` | 偏环境与工具准备，主要讲R语言基础知识讲解。
- `2026-04-10` | [1.R语言基础与环境配置](https://www.bilibili.com/video/BV1X5QcBpEea) | 播放 `531` | 偏环境与工具准备，主要讲R语言基础与环境配置。

### Bulk RNA-seq / 芯片 / 公共数据库

- `2026-05-17` | [10 差异基因到GO、KEGG、DO富集分析实战)](https://www.bilibili.com/video/BV1mQLj6iEhd) | 播放 `951` | 重点讲差异基因到GO、KEGG、DO富集分析实战)。
- `2026-05-03` | [23.RNA-seq上游](https://www.bilibili.com/video/BV1hGoDBiEwN) | 播放 `197` | 重点讲RNA-seq上游。
- `2026-05-02` | [22.ChIP-seq下游分析](https://www.bilibili.com/video/BV1YMoDBuEPj) | 播放 `327` | 重点讲ChIP-seq下游分析。
- `2026-05-01` | [21.ChIP-seq全流程上游分析](https://www.bilibili.com/video/BV13MoDBuEmy) | 播放 `310` | 偏整套流程串讲，覆盖ChIP-seq全流程上游分析。
- `2026-04-18` | [8.芯片数据上游分析和蛋白互作（ppi网络）](https://www.bilibili.com/video/BV1d5d8BSEaJ) | 播放 `137` | 重点讲芯片数据上游分析和蛋白互作（ppi网络）。
- `2026-04-17` | [7.通路集富集分析](https://www.bilibili.com/video/BV1d5d8BSECC) | 播放 `400` | 重点讲通路集富集分析。
- `2026-04-16` | [6.RNA-seq差异分析](https://www.bilibili.com/video/BV1QWd8BCEa5) | 播放 `601` | 重点讲RNA-seq差异分析。
- `2026-04-13` | [4.芯片数据分析与常见作图](https://www.bilibili.com/video/BV1oHQuBSEy6) | 播放 `188` | 重点讲芯片数据分析与常见作图。
- `2026-04-12` | [3.生存曲线](https://www.bilibili.com/video/BV1oHQuBSE3Z) | 播放 `259` | 重点讲生存曲线。

### 单细胞基础

- `2026-05-21` | [14 Scanpy 3k PBMC预处理、质控与聚类分析](https://www.bilibili.com/video/BV1JML76RE38) | 播放 `84` | 重点讲Scanpy 3k PBMC预处理、质控与聚类分析。
- `2026-05-20` | [13 Jupyter Notebook基础与Scanpy入门](https://www.bilibili.com/video/BV1EgL76WExK) | 播放 `243` | 重点讲Jupyter Notebook基础与Scanpy入门。
- `2026-05-15` | [09 单细胞可视化美化、分组比较与marker图表绘制](https://www.bilibili.com/video/BV1guRsBdEwL) | 播放 `214` | 重点讲单细胞可视化美化、分组比较与marker图表绘制。
- `2026-05-13` | [08 Marker基因筛选、细胞类型注释与卵巢单细胞案例](https://www.bilibili.com/video/BV15kRsBAEWY) | 播放 `309` | 偏案例驱动，重点是Marker基因筛选、细胞类型注释与卵巢单细胞案例。
- `2026-05-12` | [07 DoubletFinder去双细胞与结直肠癌单细胞案例](https://www.bilibili.com/video/BV15kRsBAENL) | 播放 `103` | 偏案例驱动，重点是DoubletFinder去双细胞与结直肠癌单细胞案例。
- `2026-05-11` | [06 Seurat数据整合实战与细胞亚群注释)](https://www.bilibili.com/video/BV1dzRsBNE4T) | 播放 `111` | 重点讲Seurat数据整合实战与细胞亚群注释)。
- `2026-05-10` | [05 Seurat多样本整合、批次校正与SCTTransform流程](https://www.bilibili.com/video/BV1L6RsBeETC) | 播放 `108` | 重点讲Seurat多样本整合、批次校正与SCTTransform流程。
- `2026-05-09` | [04 单细胞质控过滤、去双细胞与PCA降](https://www.bilibili.com/video/BV1v6RsBeEbr) | 播放 `120` | 重点讲单细胞质控过滤、去双细胞与PCA降。
- `2026-05-08` | [03 单细胞数据结构、Cell Ranger报告与10x测序质控解读](https://www.bilibili.com/video/BV13mRsBfE8F) | 播放 `163` | 重点讲单细胞数据结构、Cell Ranger报告与10x测序质控解读。
- `2026-05-07` | [02 R语言数据结构与单细胞表达矩阵基础](https://www.bilibili.com/video/BV1SSRsBtEQx) | 播放 `143` | 重点讲R语言数据结构与单细胞表达矩阵基础。
- `2026-05-05` | [25单细胞进阶分析](https://www.bilibili.com/video/BV1gGoDBiE3d) | 播放 `339` | 重点讲单细胞进阶分析。
- `2026-04-24` | [14.marker基因展示](https://www.bilibili.com/video/BV1L1oEB9EsG) | 播放 `147` | 重点讲marker基因展示。
- `2026-04-24` | [13.单细胞可视化](https://www.bilibili.com/video/BV1fioEBfEEx) | 播放 `244` | 重点讲单细胞可视化。
- `2026-04-22` | [12.单细胞注释](https://www.bilibili.com/video/BV1hLdvBsEx5) | 播放 `443` | 重点讲单细胞注释。
- `2026-04-20` | [10.单细胞降维聚类与注释](https://www.bilibili.com/video/BV1ZwdvBPEN5) | 播放 `176` | 重点讲单细胞降维聚类与注释。
- `2026-04-19` | [9.单细胞数据读取与质控)](https://www.bilibili.com/video/BV1owdvBPEEx) | 播放 `285` | 重点讲单细胞数据读取与质控)。
- `2026-04-15` | [5.TCGA数据分析与可视化](https://www.bilibili.com/video/BV1bEQJBYEGu) | 播放 `237` | 重点讲TCGA数据分析与可视化。

### 单细胞进阶

- `2026-05-29` | [22 InferCNV拷贝数变异推断与CytoTRACE细胞干性](https://www.bilibili.com/video/BV1EbLj6pEmo) | 播放 `137` | 重点讲InferCNV拷贝数变异推断与CytoTRACE细胞干性。
- `2026-05-28` | [21 SCENIC单细胞转录因子调控网络分析](https://www.bilibili.com/video/BV1q8Lj6DE2h) | 播放 `155` | 重点讲SCENIC单细胞转录因子调控网络分析。
- `2026-05-27` | [20 细胞通讯分析、CellPhoneDB安装运行与CellChat可视化](https://www.bilibili.com/video/BV1q8Lj6DERk) | 播放 `153` | 重点讲细胞通讯分析、CellPhoneDB安装运行与CellChat可视化。
- `2026-05-26` | [19 Monocle拟时序轨迹分析与细胞命运推断](https://www.bilibili.com/video/BV1HwL76fEf1) | 播放 `129` | 重点讲Monocle拟时序轨迹分析与细胞命运推断。
- `2026-05-24` | [17 PHATE降维、细胞分化轨迹与亚群结构分析](https://www.bilibili.com/video/BV1HPL76tEw2) | 播放 `88` | 重点讲PHATE降维、细胞分化轨迹与亚群结构分析。
- `2026-05-23` | [16 velocyto.R与scVelo RNA velocity实战分析](https://www.bilibili.com/video/BV1WFL76cEZg) | 播放 `109` | 重点讲velocyto.R与scVelo RNA velocity实战分析。
- `2026-05-22` | [15 RNA velocity原理与scVelo分析环境准备](https://www.bilibili.com/video/BV1JML76REHK) | 播放 `139` | 重点讲RNA velocity原理与scVelo分析环境准备。
- `2026-05-18` | [11 GSVA通路活性评分与单细胞通路热图分析](https://www.bilibili.com/video/BV1JTL76xEYH) | 播放 `213` | 重点讲GSVA通路活性评分与单细胞通路热图分析。
- `2026-04-30` | [20.RNA velocity分析](https://www.bilibili.com/video/BV1RCoDB5Eyz) | 播放 `148` | 重点讲RNA velocity分析。
- `2026-04-29` | [19.CNV拷贝数变异分析](https://www.bilibili.com/video/BV1dCoDB5EwY) | 播放 `162` | 重点讲CNV拷贝数变异分析。
- `2026-04-28` | [18.细胞互作（细胞通讯）分析](https://www.bilibili.com/video/BV1ZBoDBmEEF) | 播放 `279` | 重点讲细胞互作（细胞通讯）分析。
- `2026-04-27` | [17.拟时间（轨迹分析）](https://www.bilibili.com/video/BV1i6oDB7EBS) | 播放 `192` | 重点讲拟时间（轨迹分析）。
- `2026-04-26` | [16.SCENIC转录调控分析](https://www.bilibili.com/video/BV1XDoEBJEYC) | 播放 `337` | 重点讲SCENIC转录调控分析。
- `2026-04-25` | [15.通路活性与功能富集分析](https://www.bilibili.com/video/BV1L1oEB9EJf) | 播放 `345` | 重点讲通路活性与功能富集分析。

### 空间与多组学

- `2026-05-30` | [23 空间转录组与单细胞RNA-seq联合解析组织结构](https://www.bilibili.com/video/BV1zbLj6HEjq) | 播放 `438` | 重点讲空间转录组与单细胞RNA-seq联合解析组织结构。
- `2026-05-25` | [18 Signac单细胞ATAC-seq质控、峰分析与多组学整合](https://www.bilibili.com/video/BV1HPL76tEFz) | 播放 `114` | 重点讲Signac单细胞ATAC-seq质控、峰分析与多组学整合。
- `2026-05-04` | [24.ATAC-seq全流程分析](https://www.bilibili.com/video/BV1gGoDBiEx6) | 播放 `612` | 偏整套流程串讲，覆盖ATAC-seq全流程分析。

### Nature复现与科研复盘

- `2026-03-31` | [Nature复现：QC、UMAP 和空间图一步一步跑通（实操继续）](https://www.bilibili.com/video/BV1HEXkBREXT) | 播放 `146` | 围绕顶刊复现，重点是QC、UMAP 和空间图一步一步跑通（实操继续）。
- `2026-03-25` | [Nature复现：环境、Spyder 和空转数据怎么顺利读进来（实操开始）](https://www.bilibili.com/video/BV1iVQUBbEhF) | 播放 `141` | 围绕顶刊复现，重点是环境、Spyder 和空转数据怎么顺利读进来（实操开始）。
- `2026-03-24` | [Nature复现：空间定位与共定位分析：关键亚群如何映射回组织空间](https://www.bilibili.com/video/BV1zhQBBTEuL) | 播放 `716` | 围绕顶刊复现，重点是空间定位与共定位分析：关键亚群如何映射回组织空间。
- `2026-03-22` | [Nature复现：经典 Cell 文章拆解：如何从单细胞中找到关键肿瘤亚群](https://www.bilibili.com/video/BV1BdA3zsECf) | 播放 `1960` | 围绕顶刊复现，重点是经典 Cell 文章拆解：如何从单细胞中找到关键肿瘤亚群。
- `2026-03-21` | [Nature复现：从 0 理解空间转录组，新手最该先懂的核心逻辑](https://www.bilibili.com/video/BV1owAAzbEH2) | 播放 `293` | 围绕顶刊复现，重点是从 0 理解空间转录组，新手最该先懂的核心逻辑。
- `2026-03-19` | [Nature复现：空转学习前的课前预热：AI、代码与学习方法怎么配合](https://www.bilibili.com/video/BV1NyAVzrERe) | 播放 `48` | 围绕顶刊复现，重点是空转学习前的课前预热：AI、代码与学习方法怎么配合。
- `2026-03-18` | [Nature复现：软件安装实操](https://www.bilibili.com/video/BV1GmwBzQEMZ) | 播放 `49` | 围绕顶刊复现，重点是软件安装实操。
- `2026-03-16` | [Nature复现：数据驱动科研与公开数据库发文思路](https://www.bilibili.com/video/BV179w2zSEN2) | 播放 `91` | 围绕顶刊复现，重点是数据驱动科研与公开数据库发文思路。
- `2026-03-15` | [Nature复现：AI辅助论文解读与科研思路](https://www.bilibili.com/video/BV1xTwuz4EoY) | 播放 `149` | 围绕顶刊复现，重点是AI辅助论文解读与科研思路。

### 专题案例与扩展课

- `2026-05-31` | [24 黑色素瘤脑转移单细胞图谱案例与通路特征分析](https://www.bilibili.com/video/BV1iYLj6UEt1) | 播放 `93` | 偏案例驱动，重点是黑色素瘤脑转移单细胞图谱案例与通路特征分析。
- `2026-04-21` | [11.多样本整合和批次分析](https://www.bilibili.com/video/BV1zfdeBKEFd) | 播放 `333` | 偏专题扩展，重点是多样本整合和批次分析。
- `2026-04-08` | [华哥新课：孟德尔+单细胞 纯生信公共数据库挖掘文章全文复现](https://www.bilibili.com/video/BV1CcDkBJExx) | 播放 `921` | 偏专题扩展，重点是华哥新课：孟德尔+单细胞 纯生信公共数据库挖掘文章全文复现。
