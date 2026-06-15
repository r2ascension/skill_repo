---
name: agent-memory-budget
description: "Use when starting, resizing, or coordinating multiple background agents, subagents, async terminals, or long-running parallel workflows where their combined memory must stay below a fixed cap such as 600G."
---

# Agent Memory Budget

## 核心规则

所有后台 agent 共享一个总内存池，不按“每个 agent 各自独立”处理。

- **硬上限：600G** — 所有后台 agent / subagent / async terminal / 常驻 worker 的合计预算 **绝不能超过 600G**。
- **软上限：540G** — 超过后默认 **不再新开** agent，优先缩容、复用、排队。
- **缓冲区：60G** — 把硬上限中的最后 60G 当作峰值缓冲，不当作日常可随便分配的额度。
- **单 agent 默认上限：180G** — 超过需要明确理由，并同步压缩其他 agent。

## 何时使用

- 同时启动 2 个或更多后台 agent。
- 并行跑长任务、索引、分析、推理或批处理。
- 需要决定“继续并行、缩容已有 agent，还是排队”。
- 任何可能把上下文、模型或数据常驻在内存里的后台工作。

## 目标

这个 skill 的目标不是只做“账面预算”，而是尽量把预算和真实主机内存约束对齐：

- 能做 **操作系统级硬限制** 时，优先做硬限制。
- 做不到硬限制时，要明确说这是 **admission control（入场控制）**，不是“已经物理封顶”。
- 不能把远程/托管推理、没有本地进程句柄的任务，误说成可被本地 OS 强制限制。

## 强制模式

每个计划都必须归类为以下三种之一：

- `hard-cgroup`：存在真实的 OS / container / cgroup 限制，例如 Linux cgroup v2 或 `systemd-run --scope -p MemoryMax=`。
- `hard-rlimit`：使用 `prlimit` 或 `ulimit` 之类的每进程限制；仅在 cgroup 不可用时作为后备，语义较弱、兼容性也更差。
- `soft-admission-only`：没有可用的本地进程边界，只能限制并发和预算预留，不能保证硬性物理上限。

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

再补充两个量：

- `requested = 当前任务按上表估出的目标预算`
- `minimum_viable_budget = 当前任务可接受的最低档预算`，默认取该档位下限（如常规任务 16G、重型任务 64G）

决策步骤：

1. 列出所有活动作业及其预算。
2. 给每个作业标记强制模式：`hard-cgroup` / `hard-rlimit` / `soft-admission-only`。
3. 估算新作业的 `requested` 与 `minimum_viable_budget`。
4. 计算 `active_total + requested_total + buffer`，并同时跟踪其中 **真正硬限制** 的部分和 **仅软预留** 的部分。
5. 若 `hard_remaining < minimum_viable_budget`，直接拒绝启动新 agent。
6. 若估算不确定，**按更高一级估算**，不要乐观下注。
7. 给出批准 / 改配 / 排队 / 拒绝结论。

## 物理意义规则

- 除非操作系统或运行时实际上会强制执行内存上限，否则不要称计划为“硬限制”。
- 对于本地后台进程，优先考虑 Linux 上的 `hard-cgroup`。如果你声明了硬上限，也必须同时说明 **强制机制**。
- 对于 600G 的机器预算，默认至少保留 `max(32G, 10%)` 给 OS / 编辑器 / shell / 文件缓存。也就是说，**600G 是绝对上限，540G 才是默认可调度工作预算**。
- 如果只能使用 `soft-admission-only`，请更保守：减少并行数、提高估算值、保留更大的缓冲，而不是假装“系统会自动挡住”。
- 不要在没有说明的情况下混合硬预留和软预留。必须分别报告：
	- `hard_limited_total`
	- `soft_reserved_total`
- 对于异步终端、守护进程、工作者或其他本地作业，优先选择“**启动时就带限制**”的方式，而不是“先跑起来再观察”。

## 优先级与回收顺序

保留顺序：

1. 当前用户主任务直接相关的 agent。
2. 已经运行较久、且高价值的重任务。
3. 可以明显复用已有上下文的 agent。

优先回收顺序：

1. 空闲或等待中的 agent。
2. 低优先级后台 agent。
3. 最新启动且收益最低的重型 agent。

## 升级建议

如果请求装不下：

- 序列化启动。
- 降低模型 / 上下文大小。
- 减少 worker 数量。
- 把工作流拆成多个阶段。
- 能用 cgroup 或 `systemd-run --scope -p MemoryMax=` 时优先使用。
- 只有在 cgroup 不可用时，才退回 `prlimit` / `ulimit`，并明确说明这是较弱的硬限制形式。
- 询问用户哪些工作负载优先级最高。

## 输出格式

始终报告：

- 活动作业及每个作业的内存估算。
- 新申请作业及每个作业的内存估算。
- 安全缓冲区。
- 启动后的总计。
- 剩余余量。
- 每个作业的强制模式（`hard-cgroup` / `hard-rlimit` / `soft-admission-only`）。
- `hard_limited_total` 与 `soft_reserved_total`。
- 决策：批准 / 批准但改配 / 拒绝。
- 具体启动顺序。

## 快速例子

如果当前总额已经是 `500G`：

- `safe_remaining = 40G`
- 新 agent 申请 `64G`：**默认不批**；只能降配到可行低档，或直接排队。
- 无论如何，**总额都不能超过 600G**。

示例表述：

- “批准 3 个每个 120G 的本地工作者，全部使用 `hard-cgroup`，保留 80G 余量，拒绝第 4 个，直到一个完成。”
- “拒绝当前计划：5 × 140G 会超过 600G。先运行 2 个，再运行 2 个，最后运行 1 个。”
- “批准但改配：两个作业只有 `soft-admission-only`，因此降低并行度并增加缓冲，而不是声称已经做了硬 600G 限制。”

## 常见错误

| 错误 | 正确做法 |
|---|---|
| 只看新 agent，不看已运行 agent | 每次都先算 `reserved_total` |
| 把 600G 当作日常目标值 | 540G 才是默认运行上限 |
| 让单个 agent 无限膨胀 | 给单 agent 明确封顶 |
| 内存不够时继续并行 | 改为缩容、排队或复用 |
| 需求不确定时按最低值下注 | 不确定就按更高档估算 |
| 只有账面预算，却说成“硬限制” | 明确区分 `hard-*` 和 `soft-admission-only` |
