---
topic: antirez/ds4 DeepSeek V4 Flash 本地推理引擎
category: inference-engineering
status: active
source: autonomous-learning/pending-promotion
date: 2026-05-17
score: 20/20
---

# antirez/ds4 DeepSeek V4 Flash 本地推理引擎

ds4 是 Redis 创始人 antirez 开发的专为 DeepSeek V4 Flash 打造的自包含本地推理引擎。Metal 路径实现 whole-model GPU graph inference（17 个 .metal compute kernels），CUDA 路径含 IQ2 量化专用查找表。128GB Mac 上可运行 284B MoE 模型做 coding agent。

三个关键可复用模式：(1) Disk KV Cache 作为一等公民——SHA1(rendered_text) 做 key，序列化到磁盘，解决 agent 持续上下文跨 session/restart 的 prefix 复用问题；(2) Tool-call exact replay——radix tree 存储 tool_id → DSML text 精确映射，解决 multi-turn tool-calling 的 KV prefix 失配问题；(3) 不对称 MoE 量化——只量化 MoE routed experts，shared experts 保持原始精度。

"单一模型深度绑定"模式值得关注——为特定模型做 end-to-end 最优，比通用抽象性能更好。

## 证据来源
- 质量评审: `reviews/2026-05-17-ds4-quality-review.md` (20/20)
- 项目链接: https://github.com/antirez/ds4 (MIT, 10K+ stars)
