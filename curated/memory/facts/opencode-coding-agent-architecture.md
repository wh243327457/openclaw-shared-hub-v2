---
fact_id: opencode-coding-agent-architecture
status: active
freshness_class: slow_changing
scope: cross-agent
subject: coding-agent / architecture
attribute: engineering-patterns
value_summary: "anomalyco/opencode 的 5 个工程模式：client/server 分离、provider-neutral LLM 层、角色化 agent、统一工具注册、上下文压缩一级子系统"
created_at: 2026-05-17
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://github.com/anomalyco/opencode
  - runtime/hermes/autonomous-learning/agent-outputs/github-growth-2026-05-17-opencode.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# anomalyco/opencode — Coding Agent 工程体系

## 核心模式

1. **Client/server 分离**：TUI 只是客户端之一，统一 API 供多端调用
2. **Provider-neutral LLM 层**：adapter/transform 隔离 provider 差异，业务层只看统一 schema
3. **角色化 agent**：build(可执行)/plan(只读)/general(搜索)，代码级过滤而非 prompt 约束
4. **统一工具注册**：shell/read/write/edit/grep/glob/websearch/lsp 集中管理，按 agent mode 过滤
5. **上下文压缩一级子系统**：compaction/overflow/summary 模板显式处理长对话膨胀

## 可迁移模式

- 共享中台应把 skills/policies/roles 做成清晰 registry
- 自主学习 executor/reviewer/promoter 分层可借鉴 role separation
- 长任务必须显式 compaction，避免 inbox/runtime 膨胀后不可审计
