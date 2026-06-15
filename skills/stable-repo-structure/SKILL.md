---
name: stable-repo-structure
description: Use when creating, moving, renaming, or packaging files for commit, push, or pull request in this repository; deciding where a new skill, instruction, prompt, agent, doc, tool, script, output, or log should live; or when the user asks for 目录结构统一, 路径规范, GitHub-ready layout, or “不要每次结构都不一样”.
---

# Stable Repo Structure

## Overview

当某个文件或目录**准备被提交、推送或放进 PR** 时，路径选择应当先服从仓库结构，而不是服从“这次聊天里顺手放哪儿”。

核心目标只有一个：**让相似的东西长期落到相似的位置**。

这意味着：

- 共享到 GitHub 的内容，默认进入仓库内稳定的语义目录；
- 个人专用内容，不要混进仓库共享目录；
- 临时产物不要冒充正式结构；
- 能复用已有目录时，优先复用，不再发明同义新目录。

## First split: personal vs GitHub-shared

先判断这个东西是不是要进入版本库。

| 情况 | 默认位置 | 说明 |
|---|---|---|
| 只给当前用户自己用，不准备推 GitHub | 用户级 prompts 目录或 `.copilot/skills/` | 这是个人层，不是 repo 共享层 |
| 团队共享、准备 commit / push / PR | 仓库内稳定目录 | 默认应可被 GitHub 跟踪 |

**重要规则：**

如果用户明确说“要推到 GitHub”“要放在仓库里”“要让以后默认按这个规则来”，那么默认不应放进 `.copilot/skills/` 这类个人目录，而应优先走仓库共享路径。

## Routing order

每次按下面顺序决定路径：

1. **它会不会被 commit / push？**
   - 不会：放个人目录或临时目录。
   - 会：继续往下判断。

2. **它是 customization，还是项目资产？**
   - customization（skill / instruction / prompt / agent / hook）→ `.github/`
   - 项目资产（docs / tools / scripts / outputs / logs）→ 对应业务目录

3. **仓库里是否已经有同一家族目录？**
   - 有：优先复用
   - 没有：再考虑新建

4. **选择稳定用途桶（purpose bucket）**
   - 不按“这次方便”命名
   - 按长期语义命名

5. **提交前做一次结构审计**
   - 有没有 stray root files？
   - 有没有同义目录并存？
   - 有没有把个人目录当共享目录？

## Canonical homes for GitHub-shared customizations

如果是**仓库共享的 Copilot / agent customization**，优先使用下面的固定位置：

| 内容类型 | 稳定位置 |
|---|---|
| shared skill | `.github/skills/<skill-name>/SKILL.md` |
| shared instruction | `.github/instructions/<topic>.instructions.md` |
| shared prompt | `.github/prompts/<name>.prompt.md` |
| shared agent | `.github/agents/<name>.agent.md` |
| shared hook | `.github/hooks/<name>.json` |
| repo-wide always-on guidance | `.github/copilot-instructions.md` |

### Default rule for skills

- **准备推 GitHub 的 skill** → `.github/skills/<name>/SKILL.md`
- **只打算自己本地用的 skill** → `.copilot/skills/<name>/SKILL.md`

不要在“其实想共享到仓库”的情况下，一会儿放 `.copilot/skills/`，一会儿又放 `.github/skills/`。默认共享就走 `.github/skills/`。

## More precise routing inside `.github/`

不要只知道“放进 `.github/`”；还要知道**放进 `.github/` 的哪一层**。

| 需求 | 稳定位置 | Use when |
|---|---|---|
| 仓库级默认行为说明 | `.github/copilot-instructions.md` | 规则短、广泛、应默认生效 |
| 多步骤或条件性工作流知识 | `.github/skills/<name>/SKILL.md` | 需要按需命中、内容较长、有判断逻辑 |
| 文件模式触发规则 | `.github/instructions/<topic>.instructions.md` | 需要 `applyTo` 自动触发 |
| 用户显式调用的聚焦任务 | `.github/prompts/<name>.prompt.md` | 更像一个可调用模板 |
| 上下文隔离的专门代理 | `.github/agents/<name>.agent.md` | 需要子代理行为或工具边界 |
| 硬性执行/拦截 | `.github/hooks/<name>.json` | 需要确定性校验或阻断 |

### Naming rules for shared customizations

- skill / prompt / agent / instruction 的**主题名**默认使用稳定语义名，不带日期；
- 目录或文件基名优先使用 `kebab-case` 或仓库既有命名习惯；
- 一个主题优先维护一个固定入口，不要为同一主题并排创建 `foo-rule`、`foo-guideline`、`foo-structure-v2` 这类近义副本；
- 只有内容职责明显不同，才拆成多个 customization 文件。

## Canonical homes inside `docs/`

`docs/` 不是一个大杂烩目录。

| 内容类型 | 稳定位置 | 不要误放成 |
|---|---|---|
| 实验过程、执行记录、结果追踪 | `docs/experiments/` | `docs/notes/`、根目录散落 markdown |
| 未来要做的计划、实施方案、任务拆解 | `docs/plans/` | `docs/experiments/` |
| 稳定方法说明、流程规范、长期约定 | `docs/methods/` | `docs/plans/` |
| 版本口径、迁移记录、变更说明 | `docs/versions/` | `docs/methods/` |

### Docs placement shortcuts

- **“记录今天做了什么”** → `docs/experiments/`
- **“接下来准备怎么做”** → `docs/plans/`
- **“以后都按这个方法做”** → `docs/methods/`
- **“这个版本和上个版本差在哪”** → `docs/versions/`

## Canonical homes inside `tools/`

`tools/` 只放**可复用的 repo 级工具**，不要把它当成“不会分类时的回收站”。

适合进入 `tools/` 的内容：

- 外部服务桥接器；
- repo 级启动脚本、包装器、守护脚本；
- 多项目复用的自动化工具；
- 与分析脚本分离的基础设施型 helper。

不适合进入 `tools/` 的内容：

- 某个谱系/项目专属分析脚本；
- 一次性的 notebook 导出脚本；
- 结果文件或运行日志；
- 为单一分析临时写的小探针。

### Quick rule for `tools/` vs `script/`

- **在回答“分析什么”** → 放 `script/`
- **在回答“怎么运行/怎么桥接/怎么自动化”** → 放 `tools/`

如果一个文件主要处理生物学分析流程、细胞类型、DE、trajectory、programs 等主题，它通常更应该去 `script/`，而不是 `tools/`。

## Canonical homes for repo assets

| 内容类型 | 稳定位置 | 说明 |
|---|---|---|
| 实验/工作日志 | `docs/experiments/` | 持久记录 |
| 计划/设计说明 | `docs/plans/` | 任务计划、实施方案 |
| 方法文档 | `docs/methods/` | 方法学、约定、说明 |
| 版本/变更说明 | `docs/versions/` | 版本口径、变更历史 |
| 可复用工具/脚本包装器 | `tools/<tool-or-domain>/` | repo 级工具 |
| 分析脚本 | `script/py/`、`script/R/`、`script/bash/` 下的稳定子目录 | 继续遵守 `analysis-script-routing` |
| Python 输出 | `data/py/<YYYYMMDD>/` | 结果产物 |
| R 输出 | `data/R/<YYYYMMDD>/` | 结果产物 |
| 运行日志 | `logs/<YYYYMMDD>/` | runtime logs |
| 临时探针/草稿 | `temp/` | 默认不作为最终 GitHub 结构 |

## Stable naming rules

### 1. 优先复用已有词汇

不要给同一种东西反复起不同目录名。

优先复用已有稳定词汇，例如：

- `skills`，不要再造 `abilities`
- `instructions`，不要再造 `rulesets`
- `tools`，不要再造 `utils_repo`
- `plans`，不要再造 `notes_for_later`
- `methods`，不要再造 `methodology_docs`
- `tests/smoke`、`tests/audit`、`tests/regression`，不要同级混用一堆近义词

### 2. 目录名用稳定语义，不带临时情绪

避免：

- `misc/`
- `tmp_final/`
- `new_stuff/`
- `final2/`
- `github_push_fix/`

优先用“长期还能看懂”的名字。

### 3. 日期/版本号不要进正式结构目录名

除非该目录本来就是时间序列产物：

- `data/py/<YYYYMMDD>/`
- `data/R/<YYYYMMDD>/`
- `logs/<YYYYMMDD>/`
- `docs/experiments/EXP-YYYYMMDD-.../`

除此以外，目录名默认不要带日期或版本号。

## Root-level whitelist for new shared additions

对**新的 GitHub-shared 顶层结构**要保守。

默认优先复用这些家族目录：

- `.github/`
- `docs/`
- `tools/`
- `script/`
- `data/`
- `logs/`
- `temp/`

这意味着：

- 新的共享文件，默认应先问“能不能放进现有家族目录”；
- 只有当现有家族目录都明显不适配时，才考虑创建新的顶层目录；
- 已存在的历史目录可以继续维护，但**不是**新内容默认落点。

### Special note on historical roots

仓库里已经存在一些历史根目录，例如 `output/`、`R/`、`int/`、`TOM/` 等。

处理原则是：

- 如果你是在**延续该目录已存在的同类内容**，可以继续沿用；
- 如果你是在**新增一类共享结构**，默认不要再把它们当成首选新家。

例如：

- 新分析产物优先考虑 `data/py/<YYYYMMDD>/` 或 `data/R/<YYYYMMDD>/`；
- 新 repo 文档优先考虑 `docs/`；
- 新共享 customization 优先考虑 `.github/`。

## Anti-drift rules

以下情况默认视为结构漂移，应避免：

- 为同类内容重复新建多个近义目录；
- 把应共享的内容放到个人目录；
- 把应临时存在的内容塞进正式共享目录；
- 为单个文件新建过深的目录迷宫；
- 在仓库根目录散落新文件，而已有家族目录完全可以接住它；
- 让 `temp/` 里的文件未经整理就直接变成最终提交结构。

## What should usually stay out of GitHub

以下内容默认不应因为“先跑通了”就直接进入共享结构：

- secrets、token、密钥相关文件；
- 机器本地环境目录、缓存、包安装目录；
- 临时下载物、浏览器状态、会话缓存；
- 中间结果堆、一次性 debug dump、未整理的 scratch exports；
- 仅当前用户本地有意义的 agent / IDE 状态文件；
- 纯粹为了短时验证创建、但没有沉淀为稳定入口的临时脚本。

如果这类文件确实需要被版本化，应该先完成一层“整理”：

- 去 secret；
- 去本机路径耦合；
- 放进正确家族目录；
- 明确它的长期角色。

## Relocate-before-commit rule

如果文件最初只是临时放置，但现在要进 GitHub，共享前应先**搬到最终结构**。

常见情况：

- `.copilot/skills/xxx/` 里的 skill 变成团队共享 → 搬到 `.github/skills/xxx/`
- `temp/` 里的临时 helper 变成长期工具 → 搬到 `tools/` 或 `script/.../tests/`
- 根目录里的草稿 markdown 变成正式文档 → 搬到 `docs/plans/`、`docs/methods/` 或 `docs/experiments/`

不要把“临时放哪儿”直接固化为“长期结构长哪样”。

## Pre-push structure checklist

在 commit / push / PR 前，至少检查：

- [ ] 新文件是否已经落到正确的家族目录
- [ ] 共享 customization 是否放在 `.github/` 而不是个人目录
- [ ] 仓库根目录是否出现了本可归类的 stray files
- [ ] 是否发明了一个现有目录就能替代的新同义目录
- [ ] 是否把临时目录当成了长期结构
- [ ] 若是脚本，是否已经同时遵守 `analysis-script-routing`
- [ ] 若是分析实质性改动，是否同时更新 `docs/experiments/`

## Quick examples

| 需求 | 应放位置 |
|---|---|
| 新建一个准备提交到仓库的 skill | `.github/skills/<name>/SKILL.md` |
| 新建一个只给自己用的本地 skill | `.copilot/skills/<name>/SKILL.md` |
| 新建 repo 共享 instruction | `.github/instructions/<topic>.instructions.md` |
| 新建任务计划文档 | `docs/plans/` |
| 新建方法说明 | `docs/methods/` |
| 新建 repo 共享工具脚本 | `tools/<tool-or-domain>/` |
| 新建分析脚本 | `script/<lang>/...` 下稳定子目录 |
| 运行结果文件 | `data/py/<YYYYMMDD>/` 或 `data/R/<YYYYMMDD>/` |
| 运行日志 | `logs/<YYYYMMDD>/` |
| 临时 smoke / probe 文件 | `temp/`，若需版本化则进 `script/.../tests/` |

## Final reminder

当用户说的是“以后默认按稳定结构来”，真正要稳定的是**路径决策规则**。

因此默认顺序应是：

1. 先判断是否 GitHub-shared；
2. 再选固定家族目录；
3. 再决定子目录；
4. 最后才写文件。

不要反过来先写出来，再事后硬找地方塞进去。

如果任务涉及分析脚本或分析产物路径，继续参考：

- `analysis-script-routing`
- `bioinformatics-experiment-journal`
