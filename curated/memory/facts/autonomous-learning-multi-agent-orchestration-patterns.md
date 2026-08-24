---
fact_id: autonomous-learning-multi-agent-orchestration-patterns
claim_id: autonomous-learning-multi-agent-orchestration-patterns
claim_type: workflow_rule
status: active
confidence: 0.9
freshness_class: slow_changing
scope: agent-system
lens: world
topic: autonomous_learning.multi_agent.orchestration
source_agent: hermes
source_paths:
  - runtime/hermes/autonomous-learning/agent-outputs/hermes/2026-05-17-anthropic-multi-agent-research.md
evidence_refs:
  - runtime/hermes/autonomous-learning/agent-outputs/hermes/2026-05-17-anthropic-multi-agent-research.md
  - runtime/hermes/autonomous-learning/reviews/2026-05-17-anthropic-multi-agent-research-quality-review.md
sensitivity: low
secret_checked: true
created_at: 2026-05-18T12:07:05+08:00
updated_at: 2026-06-04T22:53:21+08:00
last_verified_at: 2026-06-04T22:53:21+08:00
review_due_at: 2026-09-04
review_status: approved
review_after: 2026-09-04
supersedes: []
superseded_by: []
---

# 自主学习多 Agent 编排模式

- 晋升时间：`2026-05-18T12:07:05+08:00`
- 来源：`runtime/hermes/autonomous-learning/agent-outputs/hermes/2026-05-17-anthropic-multi-agent-research.md`
- 审计：`runtime/hermes/autonomous-learning/reviews/2026-05-17-anthropic-multi-agent-research-quality-review.md`，18/20
- 状态：accepted_by_user

## 稳定结论

Anthropic 多 agent research 系统验证了当前自主学习系统的主控/执行/审计分层方向：主控 agent 负责拆解、派发、综合和判断是否继续探索；执行 subagent 保持独立上下文；最终用 end-state quality review 评估结果，而不是只看每一步过程是否完成。

## 可复用规则

1. **显式派发模板**：每个执行任务必须写清 objective、output format、tools、boundaries、time budget、completion marker、fallback plan。
2. **按任务复杂度缩放预算**：普通日报/高频学习默认 0–1 个执行 agent；高价值 deep-read 可 1–2 个；重大架构决策才考虑更多，但必须有独立证据面。
3. **先宽后窄**：发现阶段先广泛搜索/筛选，再选 1–2 个对象深读，避免一开始陷入过窄方向。
4. **外部记忆与文件交接**：长上下文不要全部塞给 subagent；优先用 runtime 文件作为 handoff，再由 Hermes 汇总进 curated。
5. **终态评估优先**：审计看结果是否有证据、可复用、边界清楚，而不是盯每个中间步骤。

## 约束与风险

- 多 agent 成本高；Anthropic 案例显示 token 成本可显著放大，因此高频 cron 不能默认 fan-out。
- 同步 subagent 会形成慢任务阻塞，超时必须写 failure evidence 并降级。
- 工具说明质量会强烈影响 agent 行为；工具/skill description 要按触发条件和边界优化。

## 对当前系统的落地

- 保留 `bounded subagent budget`：高频学习最多 1 个主要执行 agent。
- 在 instruction 模板中持续要求 search strategy / tool_call_budget / fallback plan。
- 继续用 Hermes Spec Review + Quality Review 作为晋升前 gate。
