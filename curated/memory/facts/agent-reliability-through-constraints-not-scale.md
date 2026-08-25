---
fact_id: agent-reliability-through-constraints-not-scale
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-engineering
attribute: engineering-principle
value_summary: "Agent 可靠性应通过约束（guardrails、状态机、分阶段工具空间）提升，而非依赖更大模型"
created_at: 2026-06-09
updated_at: 2026-08-25
last_verified_at: 2026-08-25
review_due_at: 2026-11-23
source_refs:
  - https://github.com/antoinezambelli/forge
  - https://github.com/statewright/statewright
  - https://news.ycombinator.com/item?id=44289083
  - tutorial-card: 2026-06-09
conflict: null
supersedes: null
superseded_by: null
confidence: medium
authority: hermes-autonomous-learning
secret_checked: true
---

# Agent 可靠性通过约束而非更大模型

## 核心内容

两个独立项目（Forge 和 Statewright）用不同方法验证了同一原则：**给 agent 加约束层比换更大模型更经济有效**。

### 证据 1：Forge — Tool-calling Guardrails

自托管 LLM 的 reliability layer：
- 8B 本地模型：无 guardrails 个位数成功率 → **有 guardrails 84%**
- Sonnet 4.6：85% → **98%**
- 方法：rescue parsing + retry nudges + response validation

### 证据 2：Statewright — 状态机 Guardrails

用状态机约束 agent 每个阶段可用的工具：
- 20B 本地模型：无约束 2/10 → **有约束 10/10**
- 方法：planning 只读 → implementing 可编辑 → testing 只测试

### 核心洞察

> "Instead of making the model bigger, make the problem smaller."
> — Statewright

- **分阶段约束工具空间**：planning 阶段只给只读工具，implementing 阶段解锁编辑，testing 阶段只给测试命令
- **Guardrails 不替代模型能力，而是放大模型能力**：同样的模型，加约束层后表现提升数倍
- **适用于 frontier 和 local 模型**：效果对小模型更显著，但大模型也有提升

## 对 Hermes 的意义

1. **Hermes agent 编排**可以引入分阶段工具约束，而非给 agent 全部工具
2. **requesting-code-review** 已有类似理念（分步审查），可推广到更多工作流
3. **本地模型链路**可以在 sub2api 和模型之间加 Forge proxy 做 guardrails
4. **成本优化**：用小模型 + guardrails 替代大模型的场景值得评估

## 边界

- 两个项目都是 2026 年的新项目，长期维护不确定
- Forge eval 是自有 26 场景，非标准 benchmark
- Statewright 依赖 SaaS key，本地部署可行性待验证
- 约束层增加了系统复杂度，简单场景可能不需要
- 13GB 以下模型即使有 guardrails 效果也有限（模型本身能力不足）

## 来源

- Forge (⭐2043, MIT) — HN 687pts
- Statewright (⭐398) — HN 126pts
- 2026-06-09 教程学习深读
