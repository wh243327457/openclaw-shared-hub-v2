---
fact_id: zero-language-for-agents
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-tooling / programming-language
attribute: design-patterns
value_summary: "Vercel Labs Zero 语言的 5 个 agent-first 设计模式：结构化编译器输出、能力对象、Agent 自修复、自举编译器、诊断码分类"
created_at: 2026-05-17
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://github.com/vercel-labs/zero
  - runtime/hermes/autonomous-learning/agent-outputs/delegate-task/2026-05-17-zero-deep-analysis.md
  - runtime/hermes/autonomous-learning/agent-outputs/github-growth-2026-05-18-zero.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# vercel-labs/zero — 面向 Agent 的系统级编程语言

## 核心设计

1. **结构化编译器输出**：所有 CLI 命令 `--json`，agent 不需解析人类可读日志
2. **能力对象 World**：没有全局 singleton，所有 I/O 通过显式能力对象传递
3. **Agent 自修复**：`zero fix --plan --json` 先方案再执行，编译器生成 agent 可消费的修复计划
4. **自举编译器**：Zero 写 Zero，降低外部 toolchain 依赖
5. **诊断码分类**：TYP*/NAM*/BOR*/MEM*/MET* 标准化码，agent 可精确修复决策

## 可迁移模式

- 我们的 agent 工具链应优先 JSON 输出
- self-healing-agent 借鉴 fix --plan 模式
- 错误/审计结果可用结构化码便于聚合分析

## 风险

- 极早期（3 天项目），语言未稳定
- 适用场景窄：定位 small native tools
