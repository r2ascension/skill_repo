---
name: agent-memory-budget
description: "Use when starting, resizing, or coordinating multiple background agents, subagents, async terminals, or long-running parallel workflows where their combined memory must stay below a fixed cap such as 600G."
---

# Agent Memory Budget

## 核心规则

所有后台 agent 共享一个总内存池，不按“每个 agent 各自独立”处理。

- **硬上限：600G** — 所有后台 agent / subagent / async terminal / 常驻 worker 的合计预算 **绝不能超过 600G**
- **软上限：540G** — 超过后默认 **不再新开** agent，优先缩容、复用、排队
- **缓冲区：60G** — 把硬上限中的最后 60G 当作峰值缓冲，不当作日常可随便分配的额度
- **单 agent 默认上限：180G** — 超过需要明确理由，并同步压缩其他 agent

## 何时使用

- 同时启动 2 个或更多后台 agent
- 并行跑长任务、索引、分析、推理或批处理
- 需要决定“继续并行、缩容已有 agent，还是排队”
- 任何可能把上下文、模型或数据常驻在内存里的后台工作

## 动态分配流程

每次启动或扩容前，先计算：

- `reserved_total = 所有运行中 agent 的已分配预算之和`
- `safe_remaining = 540G - reserved_total`
- `hard_remaining = 600G - reserved_total`

然后按任务级别先估一个目标值：

| 任务级别 | 默认预算 |
|---|---:|
| 轻量检索/简单脚本 | 8-16G |
| 常规编码/分析 | 16-32G |
| 中型数据任务 | 32-64G |
| 重型任务 | 64-128G |
| 特大型任务 | 128-180G |

其中：

- `requested = 当前任务按上表估出的目标预算`
- `minimum_viable_budget = 当前任务可接受的最低档预算`，默认取该档位下限（如常规任务 16G、重型任务 64G）

分配规则：

1. **先核算，再启动**；禁止跳过现有 agent 直接新开。
2. 若 `safe_remaining <= 0`，**不要新开**；先缩容、回收、排队或复用已有 agent。
3. 若 `0 < safe_remaining < requested`，只在任务可以降配运行时给较小额度；否则排队。
4. 若 `hard_remaining < minimum_viable_budget`，直接拒绝启动新 agent。
5. 不确定真实内存需求时，**按更高一级估算**，不要乐观下注。

## 优先级与回收顺序

保留顺序：

1. 当前用户主任务相关 agent
2. 已经运行较久且高价值的重任务
3. 轻量但仍活跃的辅助 agent

回收顺序：

1. 空闲或等待中的 agent
2. 低优先级后台 agent
3. 最新启动且收益最低的重型 agent

## 快速例子

如果当前已经有 4 个后台 agent，预算分别是 `140G + 96G + 64G + 24G = 324G`：

- `safe_remaining = 540G - 324G = 216G`
- 一个新重型 agent 申请 `128G`：**可以启动**，新总额变成 `452G`

如果当前总额已经是 `500G`：

- `safe_remaining = 40G`
- 新 agent 申请 `64G`：**默认不批**；只能降配到可行低档，或直接排队
- 无论如何，**总额都不能超过 600G**

## 默认决策

- 接近 **540G**：停止扩张，先整理存量
- 接近 **600G**：立即执行缩容/回收，不再争取并发
- 拿不准时：**少开 agent，而不是多开 agent**
- 与其开很多吃不饱的小 agent，不如保留更少但真正能完成任务的 agent

## 常见错误

| 错误 | 正确做法 |
|---|---|
| 只看新 agent，不看已运行 agent | 每次都先算 `reserved_total` |
| 把 600G 当作日常目标值 | 540G 才是默认运行上限 |
| 让单个 agent 无限膨胀 | 给单 agent 明确封顶 |
| 内存不够时继续并行 | 改为缩容、排队或复用 |
| 需求不确定时按最低值下注 | 不确定就按更高档估算 |
