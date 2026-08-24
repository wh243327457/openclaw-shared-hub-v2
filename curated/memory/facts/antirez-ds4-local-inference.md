---
fact_id: antirez-ds4-local-inference
claim_id: antirez-ds4-local-inference
claim_type: technical_pattern
status: active
confidence: 0.95
freshness_class: slow_changing
scope: mlops
lens: world
subject: antirez.ds4
attribute: local_inference_patterns
value_summary: "ds4 demonstrates model-specific local inference optimization, disk KV cache, exact tool-call replay, and asymmetric MoE quantization patterns."
topic: mlops.inference.ds4
source_agent: hermes
source_paths:
  - reviews/2026-05-17-ds4-quality-review.md
evidence_refs:
  - reviews/2026-05-17-ds4-quality-review.md
  - https://github.com/antirez/ds4
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

# antirez/ds4 DeepSeek V4 Flash 本地推理引擎

ds4 是 Redis 创始人 antirez 开发的专为 DeepSeek V4 Flash 打造的自包含本地推理引擎。Metal 路径实现 whole-model GPU graph inference（17 个 .metal compute kernels），CUDA 路径含 IQ2 量化专用查找表。128GB Mac 上可运行 284B MoE 模型做 coding agent。

三个关键可复用模式：(1) Disk KV Cache 作为一等公民——SHA1(rendered_text) 做 key，序列化到磁盘，解决 agent 持续上下文跨 session/restart 的 prefix 复用问题；(2) Tool-call exact replay——radix tree 存储 tool_id → DSML text 精确映射，解决 multi-turn tool-calling 的 KV prefix 失配问题；(3) 不对称 MoE 量化——只量化 MoE routed experts，shared experts 保持原始精度。

"单一模型深度绑定"模式值得关注——为特定模型做 end-to-end 最优，比通用抽象性能更好。

## 证据来源
- 质量评审: `reviews/2026-05-17-ds4-quality-review.md` (20/20)
- 项目链接: https://github.com/antirez/ds4 (MIT, 10K+ stars)
