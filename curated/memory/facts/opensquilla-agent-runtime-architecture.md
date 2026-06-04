---
fact_id: opensquilla-agent-runtime-architecture
claim_id: opensquilla-agent-runtime-architecture
claim_type: agent_system
status: active
confidence: 0.9
freshness_class: slow_changing
scope: agent-system
lens: world
subject: opensquilla
attribute: runtime_architecture
value_summary: "OpenSquilla offers TurnRunner, provider-neutral routing, skill hub, memory snapshots, optional vector recall, and sandbox tool-envelope patterns relevant to Hermes/shared hub design."
topic: agent_runtime.opensquilla
source_agent: hermes
source_paths:
  - agent-outputs/delegate-task/opensquilla-deep-read-2026-05-17.md
evidence_refs:
  - agent-outputs/delegate-task/opensquilla-deep-read-2026-05-17.md
  - https://github.com/opensquilla/opensquilla
sensitivity: low
secret_checked: true
created_at: 2026-05-17T00:00:00+08:00
updated_at: 2026-06-04T23:53:40+08:00
last_verified_at: 2026-06-04T23:53:40+08:00
review_due_at: 2026-09-04
review_status: approved
review_after: 2026-09-04
supersedes: []
superseded_by: []
---

# OpenSquilla 微内核 AI Agent 运行时架构分析

OpenSquilla 是一个 token 效率优先的微内核 AI agent 运行时，定位为 Hermes Agent 的"同级竞争对手"。核心设计是所有入口（Web UI / CLI / 聊天频道）汇聚到统一的 `TurnRunner`，通过可插拔 provider 层对接约 20 个 LLM 提供商。其最具差异化的组件是 SquillaRouter V4 ML 模型路由——使用 LightGBM + MLP ONNX 模型做四层 tier 路由（t0 fast → t3 top），配合 complaint upgrade 机制（用户投诉后自动升级模型 tier）。

关键可复用模式包括：(1) TurnRunner per-session 锁注入机制，消除内部死锁风险——Hermes 可参考替代当前内置锁 dict；(2) Memory Snapshot + Bootstrap Snapshot——turn 开始时冻结 MEMORY.md/USER.md/AGENTS.md，防止 mid-turn 上下文不一致；(3) SKILL.md frontmatter schema + 三源 Hub（bundled / GitHub / ClawHub）——完整的 skill 分发机制；(4) sqlite-vec 混合向量索引（FTS5 + BGE ONNX embedding）；(5) 工具信封三状态设计（ok/error/denied）配合 deny-by-default 沙箱策略。

风险边界：runtime.py 4268 行单文件过大；SquillaRouter 模型依赖 Git LFS 分发，再训练需重发包；sqlite-vec 为可选依赖，失败回退 FTS-only。

## 证据来源
- 来源文件: `agent-outputs/delegate-task/opensquilla-deep-read-2026-05-17.md`
- 项目链接: https://github.com/opensquilla/opensquilla (Apache 2.0)
