---
fact_id: shared-model-availability
claim_id: shared-model-availability
claim_type: agent_system
status: active
freshness_class: static
scope: shared-hub
lens: world
subject: model.availability
attribute: configured_models
value_summary: "gpt-5.4, kimi-for-coding, MiniMax-M2.7, gpt5.5"
topic: shared.models.available
source_agent: hermes
source_paths:
  - /root/.hermes/config.yaml
  - /home/vany/agent/.openclaw/openclaw.json
evidence_refs:
  - /root/.hermes/config.yaml
  - /home/vany/agent/.openclaw/openclaw.json
sensitivity: low
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-08-25T14:15:00+08:00
last_verified_at: 2026-08-25T14:15:00+08:00
review_due_at: 2027-02-21
source_refs:
  - /root/.hermes/config.yaml
  - /home/vany/agent/.openclaw/openclaw.json
review_status: approved
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

4. **gpt5.5** (FastAI / api.fastapi.ai) ← 新增
   - Provider: `fastai`
   - Base URL: https://api.fastapi.ai/v1
   - 默认模型: gpt5.5
   - API Key: 环境变量 `$FASTAI_API_KEY`
   - 模型列表: 待通过接口获取补全

## 模型切换策略
- 代码/编程任务: 优先 kimi-for-coding
- 一般任务/调研: 优先 gpt-5.4
- 中文内容/长上下文: 可尝试 MiniMax-M2.7
- 接口限制时: 自动切换到可用模型

## 稳定约束
- 不在 shared 中存储明文 key
- 配置文件使用环境变量占位符
