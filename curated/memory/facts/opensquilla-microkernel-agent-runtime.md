---
fact_id: opensquilla-microkernel-agent-runtime
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-runtime / model-routing
attribute: architecture-comparison
value_summary: "OpenSquilla 微内核 agent runtime 的可借鉴模式：TurnRunner 统一入口、ML 模型路由、Dream 记忆压缩、SKILL.md 多源加载"
created_at: 2026-05-17
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://github.com/opensquilla/opensquilla
  - runtime/hermes/autonomous-learning/agent-outputs/delegate-task/opensquilla-deep-read-2026-05-17.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# opensquilla/opensquilla — 微内核 Agent Runtime

## 核心架构

1. **TurnRunner 统一入口**：所有入口（Web/CLI/Channel）汇聚到单核心执行器
2. **ML 模型路由 SquillaRouter V4**：根据任务特征自动选择最优 provider
3. **Dream 记忆压缩**：睡眠时自动整理/压缩/遗忘，保持上下文窗口效率
4. **SKILL.md 多源加载**：GitHub / ClawHub / bundled 三源 skill hub
5. **沙箱三后端**：seatbelt / bubblewrap / noop 按安全级别选择

## 与 Hermes 的对比

- TurnRunner ≈ Hermes 的 gateway 主循环
- SquillaRouter ≈ 我们可借鉴的模型路由层
- Dream memory ≈ 我们 runtime/dreams 的参考
- Skill hub ≈ 我们 shared/capabilities/skills 的参考

## 风险

- 单文件巨型 runtime (4268 行)
- 复杂 ML 依赖
- Apache 2.0 但社区尚小
