---
fact_id: anthropic-multi-agent-research-patterns
status: active
freshness_class: slow_changing
scope: cross-agent
subject: multi-agent / orchestration
attribute: production-patterns
value_summary: "Anthropic 官方多 Agent 研究系统的 7 个生产级模式：token scaling、并行工具调用、委托模板、搜索策略、工具描述自优化、LLM-as-judge、Rainbow 部署"
created_at: 2026-05-17
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://www.anthropic.com/engineering/built-multi-agent-research-system
  - runtime/hermes/autonomous-learning/agent-outputs/hermes/2026-05-17-anthropic-multi-agent-research.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# Anthropic 多 Agent 研究系统 — 生产级模式

## 关键发现

1. **Token scaling 是主要性能驱动**：95% 性能方差由 token 用量(80%) + 工具调用 + 模型选择解释
2. **多 agent 擅长广度优先查询**：比单 agent Opus 4 提升 90.2%
3. **并行工具调用**：lead agent 并行 3-5 subagent + subagent 并行 3+ 工具 → 90% 研究时间缩减
4. **工具设计 = UI 设计**：差的工具描述会让 agent 走错路
5. **Agent 自优化**：Claude 4 能诊断失败并重写工具描述 → 40% 任务时间缩减
6. **LLM-as-judge**：单次 LLM 调用 + rubric 评分最稳定
7. **Rainbow 部署**：有状态 agent 需要特殊部署策略

## 对我们系统的启发

- bounded subagent 预算策略正确（普通 0-1，高价值 1-2，重大 2-3）
- delegate_task 模板应包含 agent_goal/input/output/time/fallback
- 工具描述优化是低成本高收益的改进点
