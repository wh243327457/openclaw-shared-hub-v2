---
fact_id: shared-model-availability
status: active
freshness_class: static
scope: shared-hub
subject: model.availability
attribute: configured_models
value_summary: "gpt-5.4, kimi-for-coding, MiniMax-M2.7"
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-05-16T02:58:05+08:00
last_verified_at: 2026-05-16T02:58:05+08:00
review_due_at: 2026-06-16T02:58:05+08:00
source_refs:
  - /root/.hermes/config.yaml
  - /home/vany/agent/.openclaw/openclaw.json
conflict:
  status: none
  type: null
  conflicting_fact_ids: []
  conflicting_candidate_refs: []
  resolution: null
  resolved_by: null
  resolved_at: null
supersedes: []
superseded_by: null
confidence: high
authority: filesystem
secret_checked: true
---

# 当前环境可用模型事实

## 已配置模型
1. **gpt-5.4** (Aixj.vip / custom)
   - 当前主力模型
   - 思考模式: xhigh thinking
   - Base URL: https://aixj.vip/v1

2. **kimi-for-coding** (Kimi For Coding)
   - 代码/长上下文场景
   - 通过 Kimi 提供商切换

3. **MiniMax-M2.7** (MiniMax / minimaxi.com)
   - 新增模型
   - Base URL: https://api.minimax.chat/v1
   - contextWindow: 256k, maxTokens: 8k
   - 适用于中文场景和中长文本处理

## 模型切换策略
- 代码/编程任务: 优先 kimi-for-coding
- 一般任务/调研: 优先 gpt-5.4
- 中文内容/长上下文: 可尝试 MiniMax-M2.7
- 接口限制时: 自动切换到可用模型

## 稳定约束
- 不在 shared 中存储明文 key
- 配置文件使用环境变量占位符
