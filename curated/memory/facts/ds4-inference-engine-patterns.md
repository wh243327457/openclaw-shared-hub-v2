---
fact_id: ds4-inference-engine-patterns
status: active
freshness_class: slow_changing
scope: cross-agent
subject: local-inference / model-serving
attribute: reusable-engineering-patterns
value_summary: "antirez/ds4 的 5 个可复用推理工程模式：非对称 MoE 量化、磁盘 KV Cache、Tool-call exact replay、单一模型深度绑定、AI辅助+人类主导"
created_at: 2026-05-17
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://github.com/antirez/ds4
  - runtime/hermes/autonomous-learning/agent-outputs/2026-05-17-antirez-ds4-analysis.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# antirez/ds4 — 本地推理引擎可复用模式

## 核心模式

1. **非对称 MoE 量化**：只量化 routed experts（占参数量大头），shared experts/attention 保持 Q8/F16 — 2-bit 质量显著提升
2. **磁盘 KV Cache 持久化**：SHA1(rendered_text) 做 key + binary payload 序列化到磁盘，重启后不用重新 prefill 100K+ 上下文
3. **Tool-call exact replay**：radix tree 存储 tool_id → DSML text 精确映射，解决 multi-turn tool-calling 的 KV prefix 失配
4. **单一模型深度绑定**：为特定模型做 end-to-end 最优，比通用抽象性能更好
5. **AI 辅助 + 人类主导**：明确声明 AI 写代码，人类把关架构和正确性

## 适用边界

- alpha 质量，仅支持 DeepSeek V4 Flash
- 单 worker 串行推理，无 batching
- macOS CPU 路径存在 kernel VM bug

## 与我们系统的关联

- Disk KV Cache 可参考用于跨 agent 共享推理状态
- Tool-call exact replay 可解决多 agent 协作中的 tool call 一致性
- 非对称量化可直接用于 llama.cpp 的 Mixtral/Qwen MoE 推理
