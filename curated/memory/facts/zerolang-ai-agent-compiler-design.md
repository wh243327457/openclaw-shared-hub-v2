---
fact_id: zerolang-ai-agent-compiler-design
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-tooling / compiler-design
attribute: design-principles
value_summary: "Zero 语言的 agent-first 编译器设计原则：结构化输出、能力对象、Agent 修复闭环、自举、诊断码标准化"
created_at: 2026-05-18
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://github.com/vercel-labs/zero
  - runtime/hermes/autonomous-learning/agent-outputs/github-growth-2026-05-18-zero.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# Zero 语言 — Agent-First 编译器设计原则

## 设计原则

1. **编程语言开始为 agent 优化**：不只为人类开发者，也为 AI agent 优化
2. **结构化编译器输出**：agent 不需要解析人类可读日志
3. **能力对象显式传递**：agent 生成的代码天然具备效果边界
4. **编译器生成修复计划**：不只是报错，还要 agent 可消费的修复方案
5. **诊断码标准化**：TYP001/NAM002 等便于 agent 聚合分析

## 趋势判断

Zero 代表了"编程语言为 agent 优化"的趋势。虽然极早期，但设计方向值得关注。

## 与 zerolang 的关系

此 fact 与 zero-language-for-agents 互补：后者关注具体模式，此 fact 关注设计原则和趋势判断。
