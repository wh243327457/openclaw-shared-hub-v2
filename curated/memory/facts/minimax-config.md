---
fact_id: minimax-provider-config
status: active
freshness_class: operational
scope: openclaw
subject: model.provider.minimax
attribute: api_config
value_summary: "Base URL https://api.minimax.chat/v1, API key via $MINIMAX_API_KEY"
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-08-25T02:58:05+08:00
last_verified_at: 2026-08-25T02:58:05+08:00
review_due_at: 2026-09-24
source_refs:
  - /home/vany/agent/.openclaw/openclaw.json
  - /home/vany/agent/.openclaw/.env
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

# MiniMax 配置事实

## 已确认的配置
- Provider: minimax
- Base URL: https://api.minimax.chat/v1
- API Key: 环境变量 `$MINIMAX_API_KEY`
- 配置文件: /home/vany/agent/.openclaw/openclaw.json
- .env 文件: /home/vany/agent/.openclaw/.env

## 可用模型
- MiniMax-M2.7: contextWindow 256k, maxTokens 8k
- MiniMax-Text-01: contextWindow 256k, maxTokens 8k

## 稳定约束
- 不将明文 API Key 写入 shared 或 git
- 使用 `${MINIMAX_API_KEY}` 占位符在配置文件中引用
