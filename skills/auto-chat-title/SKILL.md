---
name: auto-chat-title
description: "Use when starting a new Copilot chat, when the chat title is generic or stale, or when the user asks to rename, retitle, update, or summarize a chat/conversation name."
---

# Auto Chat Title

## 核心原则

为当前 Copilot Chat 生成一个简短、稳定、可检索的中文标题；只有在工具或 VS Code API 明确确认成功时，才声称已经修改了聊天名称。

## 何时使用

- 新对话开始后，用户目标已经足够清楚时。
- 当前聊天名类似 `New Chat`、`Chat`、空标题，或明显与当前任务不符时。
- 用户说“更新 chat 名称”“重命名对话”“改一下聊天标题”“conversation title”等。

## 标题规则

- 6-18 个中文字符优先；必要时可用短英文术语。
- 用名词短语，不用完整句子：例如 `创建自动聊天标题技能`。
- 聚焦用户真实目标，而不是工具动作：例如 `修复 scVI 训练参数` 优于 `运行终端和改文件`。
- 避免泄露敏感信息：不要包含 API key、token、患者身份信息、完整文件路径、隐私数据。
- 多阶段任务可在意图变化后更新标题一次，但不要频繁抖动。

## 执行流程

1. 从用户请求与当前上下文提取主题。
2. 生成一个候选标题。
3. 如果环境提供可信的聊天标题工具、命令或 API（例如 `update_chat_title`、`rename_chat`、`set_conversation_title`、明确可用的 VS Code chat title command），立即调用它更新标题。
4. 如果没有可用能力，不要伪称已改名；在回复中简短写出 `建议聊天名：<标题>`，供用户手动采用。
5. 若工具调用失败，报告失败并给出建议标题，不要反复重试。

## 可用性边界

当前 VS Code/Copilot 稳定扩展 API 通常不暴露“修改当前聊天标题”的通用接口。这个 skill 的目标是：能自动改时自动改；不能自动改时，稳定地产生可复制的最佳标题，并诚实说明限制。

## 常见错误

| 错误 | 正确做法 |
|---|---|
| 声称标题已更新但没有工具确认 | 只说“建议聊天名” |
| 标题过长像摘要 | 压缩为一个名词短语 |
| 标题包含密钥、姓名、ID、完整路径 | 改为脱敏主题 |
| 每轮回复都换标题 | 只在任务目标首次明确或明显变化时更新 |