---
name: tabular-results-llm-bridge
description: "Use when wiring LLM APIs to bioinformatics analysis result tables in this repository, especially when users ask to interpret DEG, enrichment, ssGSEA, pathway-map, or tissue-comparison CSV/TSV outputs, or to build reusable wrappers around those tabular summaries."
---

# Tabular Results LLM Bridge

## 核心目标

把本仓库中的分析结果表（尤其是 `csv` / `tsv`）安全、可追溯、可批量地接到 LLM API 上，产出**结构化解释**，而不是把大表一股脑倒进 prompt 里然后祈祷奇迹发生。

这个 skill 的重点不是“随便调用一个大模型”，而是复用当前仓库已经成熟的三层范式：

1. **证据标准化**：把 DEG / enrichment / ssGSEA / gene-pathway map 压缩成紧凑证据块。
2. **结构化输出**：强制 JSON schema，而不是接受自由散文。
3. **失败可恢复**：JSON 解析失败时保留 raw text，并走 fallback / standardization，而不是直接把非结构化返回当成功。

## 何时使用

当用户要做下面这些事情时使用本 skill：

- “把某个分析结果 `csv/tsv` 接到 LLM 做解释”
- “给 `DESeq2_results.csv` / enrichment 结果 / ssGSEA 结果生成机制说明”
- “设计一个 LLM wrapper，把不同分析表统一转成结构化解释输出”
- “把多数据库富集结果整理后喂给模型，而不是逐数据库分开瞎讲”
- “批量读取对比目录里的结果表，输出标准化的 LLM 结果文件”
- “仿照 `interpret()` / `interpret_agent()` 写一个适配本仓库表格结果的 helper / script / workflow”

### 何时不使用

下面这些情况不要优先使用本 skill：

- 你手里已经是 R 内存中的 `enrichResult` / `gseaResult` / `compareClusterResult`，而且用户只是想直接解释对象；这时优先走 `interpret()` / `interpret_agent()`。
- 用户只是想读某一个结果表、做人工总结或生成一次性说明，而不是搭一个可复用的 LLM 接口层。
- 输入只有汇总主表（如 `all_lineages_tissue_deg_llm_master.tsv`），但没有准备回捞 contrast 级证据；这时先做筛选和定位，不要直接做机制推断。
- 用户问题本质上是 plotting / visualization / report layout，而不是“结果表 → LLM 结构化解释”。

## 先看这几个现成参考，不要重新发明轮子

### 一手参考实现

- `script/R/interpret.R`
  - `process_enrichment_input()`：输入标准化
  - `construct_interpretation_prompt()` / `construct_annotation_prompt()` / `construct_phenotype_prompt()`：prompt 模板
  - `call_llm_fanyi()`：LLM API 调用 + JSON 解析
  - `interpret()` / `interpret_agent()`：单阶段与多代理入口

- `script/R/interpret_agent_hotfix.R`
  - `.ensure_list()`：防守式 list 校验
  - hotfix `interpret_agent()`：非 JSON / character 返回的 fallback 包装

### 仓库里更贴近“CSV/TSV → LLM”的参考

- `script/R/bcell_tissue_comparison_v2_6_20260406.R`
  - `prepare_llm_enrichment_bundle()`：从多数据库结果挑代表对象 + 组装 evidence
  - `build_multi_db_context_text()`：多数据库富集表压缩为文本证据
  - `build_gene_pathway_map()`：从 enrichment + fold change 提取保守的 gene→pathway 映射
  - `format_gene_pathway_map_text()`：将 gene-pathway map 转成 prompt 证据行
  - `build_integrated_directional_enrichment_text()`：把 up/down + 多数据库证据合并成单一判断上下文
  - `standardize_result_with_llm()`：强制统一 JSON schema 的后标准化层

- `script/R/tissue_deg_llm_crosslineage_summary_20260525.R`
  - 展示了仓库里**现有表格产物如何被再次消费**：
    - `DESeq2_results.csv`
    - `interpret_agent_integrated_up_down_structured.rds`
    - `llm_multi_db_evidence_integrated_up_down.csv`
    - `validated_gene_pathway_map_integrated_up_down.csv`
    - `all_lineages_tissue_deg_llm_master.tsv`

## 输入表的优先级与用途

| 输入类型 | 典型文件 | 主要用途 | 是否适合直接做机制推断 |
|---|---|---|---|
| DEG 表 | `DESeq2_results.csv` | 提供 top DEG、方向性和 `log2FC/padj` | 可以做基础判断，但机制证据有限 |
| 多数据库富集证据表 | `llm_multi_db_evidence_integrated_up_down.csv` | 作为**主证据表**，提供方向、数据库、term、geneID、padj、Count | **最适合** |
| 验证过的基因-通路映射 | `validated_gene_pathway_map_integrated_up_down.csv` | 限制 gene→pathway claim，防止模型乱连线 | **必须优先用于精确机制表述** |
| 单对象/列表 enrichment 结果 | `enrichResult` / `gseaResult` / list | 适合在 R 内直接走 `interpret()` / `interpret_agent()` | **最适合对象态工作流** |
| 汇总主表 | `all_lineages_tissue_deg_llm_master.tsv` | 汇总、交付、QA、横向筛查 | **不适合当原始机制证据** |
| 已结构化 LLM 结果 | `*_structured.rds` | 再汇总、再展平、报告化 | 不应用作第一轮推断证据 |

## 针对当前仓库的推荐工作流

### 场景 A：手里是 R enrichment 对象

优先复用：

1. `process_enrichment_input()`
2. `construct_*_prompt()`
3. `call_llm_fanyi()`
4. 必要时套 `interpret_agent_hotfix.R`

不要先导出成 `csv` 再绕一圈读回来，除非用户明确要求做可复用的表格接口层。

### 场景 B：手里是 `csv/tsv` 结果表

优先按下面顺序压缩证据：

1. **比较/群组切分**：先按 `comparison`、`cluster`、`celltype`、`direction` 分组。
2. **DEG 摘要**：提取 top up / top down / top |log2FC| 基因。
3. **富集证据摘要**：
   - 多数据库时优先用 `build_multi_db_context_text()` 或 `build_integrated_directional_enrichment_text()` 思路。
   - 不要逐数据库各写一段互相打架的解释。
4. **gene-pathway map**：
   - 若有 `validated_gene_pathway_map*.csv`，只允许根据它做 gene→pathway 直连表述。
   - 若没有，就把基因和通路分开说，不要脑补一条虚构边。
5. **标准化输出**：
   - 第一轮可以允许 richer schema。
   - 最终扁平落盘时，优先模仿 `standardize_result_with_llm()` 的 schema。

### 场景 C：手里是主汇总 `tsv`

把它当成：

- 交付总表
- QA 面板
- 候选 contrast 筛选器
- 二次报告输入

不要把 `all_lineages_tissue_deg_llm_master.tsv` 当成“主要生物学证据来源”。
它应该告诉你**去哪一个 contrast 目录回捞真正证据**，而不是自己承担第一轮机制判断。

## 推荐的 schema：优先用扁平标准化版本

对于“结果表 → LLM → 可下游汇总”的任务，优先使用下面这组固定键：

- `overview`
- `key_mechanisms`
- `hypothesis`
- `narrative`
- `key_drivers`
- `evidence`
- `limitations`

原因：

- 便于落成一行一条记录的 `csv/tsv`
- 便于跨 lineage / cell type 汇总
- 比 `interpret_agent()` 的 richer network schema 更适合批量结果管理

### 什么时候再加 richer 字段

只有在输入里真的有足够网络级证据时，才增加：

- `refined_network`
- `network_evidence`
- `functional_modules`
- `regulatory_drivers`（rich object 版）

否则保持扁平 schema，别给未来自己制造解析灾难。

## API 层设计约定

### 1. 最小 wrapper 接口骨架

如果后续要把这个 skill 落成真正可运行的 R helper，优先从一个**最小而稳定**的接口开始：

- 输入：
  - `deg_path = NULL`
  - `enrichment_path = NULL`
  - `gene_pathway_map_path = NULL`
  - `result_scope`（如 `celltype/comparison/direction`）
  - `model`
  - `api_key = NULL`
  - `output_prefix`
- 过程：
  - 读取表格
  - 压缩 evidence text
  - 调用 LLM
  - 解析 JSON
  - 失败时保留 raw text 并 fallback
  - 输出 structured + tabular artifacts
- 返回值最少应包含：
  - `status`
  - `raw_text`
  - `parsed`
  - `warnings`
  - `output_files`

重点是先把“输入路径 / evidence builder / LLM call / parse / outputs”这五段边界钉死，再考虑 richer network schema、批量调度和多代理扩展。

### 2. 把 API 调用层与 prompt 层分开

无论用：

- `fanyi::chat_request()`
- 自定义 `httr2` / `httr` 调用
- 未来其他兼容 API

都尽量维持类似接口：

- 输入：`prompt`, `model`, `api_key = NULL`
- 输出：原始文本

然后把 JSON 解析、fallback、重试放在上层 helper 里。

### 3. 当前仓库的首选仿照对象

优先仿照 `call_llm_fanyi()` 的职责边界：

- 负责 API 调用
- 尝试解析 JSON
- 解析失败时保留 raw text 并报警告

### 4. 密钥处理规则

- 不要硬编码 API key。
- 不要把 key 打进日志、message、warning、输出表。
- 优先接受 `api_key` 参数；若为 `NULL` 再去 option / env 中找。
- 如果需要 `.env`，只检查变量是否存在，不在对话里回显其内容。

## Prompt 设计规则

### 一定要做的事

1. **明确角色**：如解释器、标注器、标准化器。
2. **明确输入来源**：DEG、multi-db enrichment、validated gene-pathway map。
3. **明确 JSON schema**：固定键名，固定值类型。
4. **明确 grounding**：每个结论必须来自输入表里的 term / gene / direction。
5. **明确限制**：
   - 证据弱时要保守
   - 没有验证过的 gene→pathway 映射时不能硬连
   - 多数据库结果要综合，不要只盯第一行

### 一定不要做的事

- 不要把整张超大 `tsv` 原样塞进 prompt。
- 不要让模型对一个数据库的单个术语过拟合。
- 不要从 `master.tsv` 直接推机制。
- 不要在没有 `validated_gene_pathway_map` 的情况下编造 gene→pathway 连接。
- 不要在 JSON parse 失败后把流程默默当成功。

## 针对本仓库最有用的三种输入模板

### 1. DEG-only 模式

适用：只有 `DESeq2_results.csv`

最低要求列：

- `gene` / `symbol`
- `log2FoldChange` / `avg_log2FC`
- 可选 `padj` / `p_val_adj`

输出重点：

- `overview`
- `key_mechanisms`
- `evidence`
- `limitations`

此模式下要主动承认：机制链条弱，更多是状态判断和候选假说。

### 2. Enrichment + gene-pathway map 模式

适用：

- `llm_multi_db_evidence_integrated_up_down.csv`
- `validated_gene_pathway_map_integrated_up_down.csv`

这是当前仓库最推荐的**表格接口 → LLM**模式。

输出时应优先：

- 综合 up/down
- 综合多个数据库
- 在 `key_mechanisms` 中只使用已验证的 gene→pathway 对

### 3. 汇总报告模式

适用：`all_lineages_tissue_deg_llm_master.tsv`

目标不是首轮解释，而是：

- 选出高价值 contrast
- 汇总各 lineage 结论
- 发现缺失文件 / 空 LLM 输出 / evidence rows 为 0 的异常项

## 建议的落盘产物

如果本 skill 被用于编写新脚本或 helper，优先沿用当前仓库产物命名：

- 原始模型文本：`*_raw.txt`
- 结构化对象：`*_structured.rds`
- 富集证据表：`llm_multi_db_evidence_<tag>.csv`
- 基因-通路映射：`validated_gene_pathway_map_<tag>.csv`
- 扁平汇总表：`*.tsv`

### 放置位置

- 新 R 脚本：`script/R/`
- 运行产物：`data/R/<YYYYMMDD>/...` 或已有 comparison 输出目录
- 日志：`logs/<YYYYMMDD>/`
- 实验记录：`docs/experiments/WORKLOG-YYYYMMDD.md` 或 `EXP-YYYYMMDD-<slug>/README.md`

## 批量处理时的拆分原则

一条 prompt 最好对应一个最小生物学单元，例如：

- 一个 `celltype x comparison`
- 一个 `cluster`
- 一个 `tissue x cell type` 组合
- 一个 `direction-integrated contrast`

不要把一整个 lineage 的几百行 contrast 直接混在一起。那不是“上下文丰富”，那是“模型失去人生方向”。

## 最低验证要求

使用本 skill 完成任务后，至少检查：

1. JSON 是否真的可解析。
2. 解析失败时 raw text 是否被保留。
3. 输出字段是否齐全。
4. `evidence` 是否真的引用了输入表中的 term / gene。
5. 若写了 gene→pathway，是否来自 `validated_gene_pathway_map`。
6. 扁平汇总表中的 `status` / `error` / `warnings` 是否可用于下游 QA。

## 在本仓库里，优先采用的设计结论

### 优先级 1：对象态解释

如果你在 R 会话里直接拿到 enrichment 对象，先看 `interpret()` / `interpret_agent()`。

### 优先级 2：表格态标准化

如果你要做复用性更强的 pipeline、批处理、跨 lineage 汇总、或用户明确给你 `csv/tsv`，优先看：

- `prepare_llm_enrichment_bundle()`
- `build_multi_db_context_text()`
- `build_gene_pathway_map()`
- `build_integrated_directional_enrichment_text()`
- `standardize_result_with_llm()`

### 优先级 3：热修复容错

如果 LLM 经常返回：

- 非 JSON
- 截断 JSON
- 纯文本散文
- 混合 markdown code fence

直接参考：

- `call_llm_fanyi()` 的解析清洗逻辑
- `interpret_agent_hotfix.R` 的 `.ensure_list()` + 非结构化 fallback 包装

## 你在实际工作中应该产出的内容

使用本 skill 时，目标通常不是只给一段聊天建议，而是产出以下一种或多种成果：

- 一个新的 R helper / script，把 `csv/tsv` 结果表接到 LLM
- 一个固定 JSON schema
- 一套 evidence text builder
- 一套 raw + structured 双落盘机制
- 一个可汇总的平面结果表
- 必要时补实验日志，说明输入、输出、参数、验证情况

如果这些都没有落地，只是“给模型喂了张表然后说了一段感想”，那还不算真正用好了这个 skill。
