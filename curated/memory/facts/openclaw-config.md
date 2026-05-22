---
fact_id: openclaw-core-config
claim_id: openclaw-core-config
claim_type: agent_system
status: active
freshness_class: operational
scope: openclaw
lens: world
subject: openclaw.config
attribute: core_model_config
value_summary: "Base URL https://aixj.vip/v1, default model gpt-5.4 + xhigh thinking"
topic: openclaw.config.core_model
source_agent: hermes
source_paths:
  - /home/vany/agent/.openclaw/openclaw.json
evidence_refs:
  - /home/vany/agent/.openclaw/openclaw.json
sensitivity: low
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-05-16T02:58:05+08:00
last_verified_at: 2026-05-16T02:58:05+08:00
review_due_at: 2026-06-16T02:58:05+08:00
source_refs:
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

# OpenClaw 配置事实

## 已确认的配置
- Base URL: https://aixj.vip/v1
- API Key: 环境变量 `$OPENCLAW_API_KEY`
- 默认模型: gpt-5.4 + xhigh thinking
- 配置文件: /home/vany/agent/.openclaw/openclaw.json
- 后台地址: http://localhost:18789

## 稳定约束
- 不将明文 API Key 写入 shared
- 查询配置时需先确认是 Hermes 配置还是 OpenClaw 配置
