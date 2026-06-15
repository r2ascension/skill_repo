---
name: analysis-script-routing
description: Use when creating, moving, renaming, or refactoring Python, R, or bash scripts in this repository and deciding the target path under script/, especially for new workflows, helpers, tests, smoke checks, project bundles, lineage analyses, visualization scripts, or requests like “新建脚本放到哪个文件夹”.
---

# Analysis Script Routing

## Overview

在这个仓库里，新的脚本文件**不要只停留在** `script/py/`、`script/R/`、`script/bash/` 这一层。

默认思路应当是：

1. 先选语言根目录；
2. 再选**已有项目/工作流域**或**生物学谱系/主题域**；
3. 最后再按**方法/目的**放进合适子目录。

目标是让未来的脚本路径能表达三件事：

- 这是什么语言；
- 它属于哪个项目、谱系或主题；
- 它是干什么的（workflow / annotation / de / viz / tests 等）。

## Core rule

**优先复用已有目录，避免继续往语言根目录堆文件。**

只有在脚本满足以下任一条件时，才允许直接放在 `script/py/`、`script/R/` 或 `script/bash/` 根层：

- 它是明确的跨项目共享入口；
- 它是历史兼容桥接入口，且已有调用方依赖该路径；
- 它只是一个短期过渡包装器，后续会立即迁移到更清晰的位置。

如果以上都不满足，默认答案应是：**继续往下分目录。**

## Routing order

按下面顺序决定脚本路径：

1. **语言根目录**  
	`script/py/`、`script/R/`、`script/bash/`

2. **优先看是否属于已有项目/工作流目录**  
	例如：`non_unified_airway/`、`normal_airway_ml/`

3. **如果不是项目制任务，再看是否属于某个谱系或主题域**  
	例如：`bcell/`、`epithelial/`、`myeloid/`、`tnk/`、`stromal/`、`allcells/`

4. **如果它是跨谱系复用的方法模块，再放到方法模块目录**  
	例如：`modules/cnmf/`、`modules/scenic/`、`modules/cellchat/`

5. **最后按方法/目的选子目录**  
	例如：`workflow/`、`annotation/`、`communication/`、`trajectory/`、`de/`、`viz/`、`helpers/`、`tests/`

## Preferred path shapes

优先使用下面几种路径形态：

```text
script/
├── py/
│   ├── core/<purpose>/
│   ├── tests/<kind>/
│   ├── modules/<method>/<purpose>/
│   ├── <project>/<purpose>/
│   └── <lineage>/<purpose>/
├── R/
│   ├── core/<purpose>/
│   ├── tests/<kind>/
│   ├── modules/<method>/<purpose>/
│   ├── <project>/<purpose>/
│   └── <lineage>/<purpose>/
└── bash/
	 ├── core/
	 ├── tests/
	 └── <project>/
```

## Stable purpose buckets

| 子目录 | Use when | 典型内容 |
|---|---|---|
| `workflow/` | 端到端流程、顺序步骤脚本、编排入口 | `00_...`、`01_...`、主 pipeline |
| `integration/` | merge、桥接、导入导出、对象转换 | h5ad/RDS/metadata bridge |
| `model/` | scVI/scANVI/scArches/ML 训练、映射、推理 | train / map / retrain |
| `annotation/` | 自动注释、标签修订、cell type assignment | CellTypist / mLLM / label clean-up |
| `communication/` | 细胞通讯分析 | LIANA / CellPhoneDB / CellChat |
| `trajectory/` | 轨迹、伪时序、tradeSeq / slingshot / Monocle3 | trajectory / branch / pseudotime |
| `de/` | 差异表达、pseudobulk、对比统计 | DESeq2 / MAST / Wilcoxon |
| `programs/` | cNMF / WGCNA / regulon / gene programs | cNMF / SCENIC / hdWGCNA |
| `viz/` | 纯绘图、figure refresh、审稿图补画 | plot / figure / dotplot / heatmap |
| `helpers/` | 可复用函数、公共配置、adapter、registry | `common.py`、helper、bridge |
| `tests/smoke/` | 快速冒烟运行 | smoke / minimal run |
| `tests/audit/` | 结果审计、完整性检查 | audit / verify / inspect |
| `tests/regression/` | 回归测试、固定 bug 保护 | unit-ish / regression checks |

## Placement rules by situation

### 1. 已有项目目录存在时：先用项目目录

如果脚本明显属于某条已存在的工作流，就不要再新造同义目录。

**直接复用项目目录**，再按目的分层：

- `script/py/non_unified_airway/communication/...`
- `script/R/non_unified_airway/communication/...`
- `script/py/normal_airway_ml/model/...`
- `script/py/normal_airway_ml/tests/audit/...`

如果该项目目前脚本数量还不多，可以先放在项目根目录；但当第二类不同用途脚本出现时，应优先补出 `workflow/`、`helpers/`、`viz/` 等子目录，而不是继续平铺。

### 2. 谱系特异但不属于单独项目时：用谱系目录

对长期重复出现的谱系分析，优先采用：

- `script/py/bcell/model/...`
- `script/py/epithelial/viz/...`
- `script/R/myeloid/de/...`
- `script/R/tnk/trajectory/...`

这类目录适合替代未来继续在语言根目录下新增：

- `bcell_*`
- `epithelial_*`
- `myeloid_*`
- `stromal_*`
- `tnk_*`

### 3. 跨谱系复用的方法模块：用 `modules/<method>/`

当脚本的主语不是某个谱系，而是某种可复用方法时，使用：

- `script/py/modules/cnmf/workflow/...`
- `script/R/modules/scenic/workflow/...`
- `script/R/modules/bayesprism/workflow/...`
- `script/py/modules/scarches/helpers/...`

适用于：

- cNMF / SCENIC / BayesPrism / Milo / CellChat / CellPhoneDB / LIANA 等可在多个谱系或项目间复用的方法。

### 4. 跨项目共享逻辑：用 `core/`

如果脚本服务于多个项目/谱系，并且其职责主要是桥接、配置、公共辅助，而不是单一分析结果，优先放入：

- `script/py/core/helpers/...`
- `script/py/core/integration/...`
- `script/R/core/helpers/...`
- `script/bash/core/...`

这类内容通常包括：

- 公共 `common` / helper / registry / adapter；
- h5ad ↔ Seurat / metadata bridge；
- orchestrator / launcher / wrapper；
- 统一路径解析与参数校验逻辑。

### 5. 测试、审计、验证：永远不要混在生产脚本里

以下类型默认进入 `tests/`：

- `test_*`
- `smoke_*`
- `audit_*`
- `verify_*`
- 只用于 check / probe / validation 的脚本

推荐：

- `script/py/tests/smoke/...`
- `script/py/tests/audit/...`
- `script/py/tests/regression/...`
- `script/R/tests/smoke/...`

## Real repo examples

下面这些是真实存在的目录或脚本，可作为路由参考：

- 已有项目目录：
  - `script/py/non_unified_airway/`
  - `script/R/non_unified_airway/`
  - `script/py/normal_airway_ml/`

- 已有测试目录：
  - `script/py/tests/`
  - `script/R/tests/`

- 若今天新建，建议迁入更清晰目录的根层脚本示例：
  - `script/py/run_cnmf_by_l3_celltype_20260519.py` → 更适合 `script/py/modules/cnmf/workflow/`
  - `script/py/mllmcelltype_native_adapter_20260525.py` → 更适合 `script/py/core/helpers/annotation/` 或项目内 `helpers/`
  - `script/R/tissue_comparison_advanced_helper_20260408.R` → 更适合 `script/R/core/helpers/` 或相关项目内 `helpers/`
  - `script/py/normal_airway_ml_train_sample_level_20260527.py` → 更适合 `script/py/normal_airway_ml/model/`

## Naming rules for folders

- 文件夹名使用**稳定语义名**，不要带日期和版本号；
- 优先用 `snake_case`；
- 尽量复用同一套词：
  - 用 `helpers/`，不要在相邻目录里再造 `utils/`、`misc/`、`common_stuff/`；
  - 用 `viz/`，不要混用 `plot/`、`figures/`、`visualization/` 作为同级同义目录；
  - 用 `tests/smoke`、`tests/audit`、`tests/regression`，不要把测试分散回生产目录。

## Shallow-by-default rule

不要创建目录迷宫。

默认深度控制原则：

- 大多数脚本落在距离语言根目录 **2-3 层** 内；
- 只有当某个家族确实会继续增长时，才多加一层；
- 不要为了单个脚本就创建五层目录。

**好例子：**

- `script/py/non_unified_airway/communication/05c_run_cellphonedb_pairwise_L2_L3_20260530_v3.py`
- `script/R/bcell/de/tissue_comparison_20260530.R`
- `script/py/modules/cnmf/workflow/run_cnmf_by_l3_celltype_20260530.py`

**坏例子：**

- `script/py/bcell/single_cell/annotation/scanvi/model/training/final/`
- `script/R/methods/analysis/misc/final2/`

## Mirror Python and R when they belong together

如果 Python 和 R 分别承担同一项目的上下游步骤，尽量镜像目录结构。

例如：

- `script/py/non_unified_airway/communication/`
- `script/R/non_unified_airway/communication/`

这样比把 Python 放在项目目录、R 放回语言根目录更容易维护。

## What to do before creating a new folder

在新建目录前，先问自己：

1. 仓库里是否已经有等价项目目录？
2. 这个脚本是否其实应该归到某个已有谱系目录？
3. 它是不是测试/审计脚本，应该进入 `tests/`？
4. 它是不是跨项目 helper，应该进 `core/`？
5. 这个新目录未来至少还会接住 2-3 个兄弟脚本吗？

如果前四题有任何一个答案是“是”，优先复用已有结构；如果第五题是“否”，也要谨慎新增目录。

## Final checklist

在创建或重定位脚本前，确认：

- [ ] 已先选语言根目录
- [ ] 已检查是否存在可复用的项目目录
- [ ] 已检查是否属于谱系目录或方法模块
- [ ] 已按方法/目的选了稳定子目录
- [ ] 测试/审计脚本没有混入生产目录
- [ ] 目录深度没有失控
- [ ] 文件夹名没有日期/版本号
- [ ] 若涉及 Python/R 成对流程，路径尽量镜像

## Reminder

本 skill 负责**路径路由**，不替代实验日志要求。

只要是这个仓库中的实质性脚本创建/修改，仍需遵守 `bioinformatics-experiment-journal` 的记录要求，把变更写入 `docs/experiments/WORKLOG-YYYYMMDD.md` 或对应 `EXP-*` journal。
