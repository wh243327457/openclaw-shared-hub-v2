---
topic: Anthropic 多 Agent 研究系统的工程实践
category: industry-trends
status: active
source: autonomous-learning/pending-promotion
date: 2026-05-17
score: 18/20
---

# Anthropic 多 Agent 研究系统的工程实践

Anthropic 的 Research 功能采用 orchestrator-worker 多 agent 架构：LeadResearcher agent 分解用户查询为子任务，并行 spawn 多个 Subagent（Claude Sonnet 4），每个拥有独立上下文窗口和搜索工具。核心发现是 token 使用量解释了 95% 的 BrowseComp 评估性能方差（其中 80% 来自 token 用量本身），multi-agent 模式消耗约 15x tokens。

生产验证的 prompt 工程原则：(1) 教 orchestrator 如何 delegate——详细任务描述包含目标、输出格式、工具、边界；(2) 按查询复杂度缩放投入——简单 1 agent/3-10 次调用，复杂 10+ subagents；(3) 先宽后窄搜索策略；(4) 让 agent 自我改进——Claude 4 能诊断失败并重写工具描述，减少 40% 任务时间。

对 Hermes 系统的启示：当前 delegate_task 模板与 Anthropic 的显式 delegation 模式一致；需在 instruction.md 中添加"搜索策略"指导和 `tool_call_budget` 字段；quality review 可形式化为 LLM-as-judge rubric。

## 证据来源
- 来源文件: `agent-outputs/hermes/2026-05-17-anthropic-multi-agent-research.md`
- 原始链接: https://www.anthropic.com/engineering/built-multi-agent-research-system
