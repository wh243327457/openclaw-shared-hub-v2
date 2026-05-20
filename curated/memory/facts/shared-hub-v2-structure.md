---
fact_id: shared-hub-v2-structure
status: active
freshness_class: static
scope: shared-hub
subject: shared-hub.v2
attribute: directory_structure
value_summary: "curated, inbox, runtime, capabilities, compat, memory and skills compatibility layers"
created_at: 2026-05-16T02:58:05+08:00
updated_at: 2026-05-16T02:58:05+08:00
last_verified_at: 2026-05-16T02:58:05+08:00
review_due_at: 2026-08-16T02:58:05+08:00
source_refs:
  - /home/vany/agent/shared/manifest.yaml
  - /home/vany/agent/shared/AGENTS.md
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
authority: hermes-controller
secret_checked: true
---

# 共享中台 v2 结构事实

## 核心分层
- curated/memory/ = 跨 agent 真相源
- inbox/<agent>/daily/ = agent 原始写入
- runtime/<agent>/ = 运行时产物
- capabilities/skills/ = 共享 skills
- compat/daily/ = 旧 OpenClaw daily 兼容

## 兼容链路
- shared/skills -> capabilities/skills
- shared/memory/MEMORY.md -> curated/memory/MEMORY.md
- shared/memory/daily -> compat/daily
- compat/daily/.dreams -> runtime/openclaw/dreams

## 治理规则
- 禁止明文 secret 写入 shared
- 新 skill 需判断是否升格为跨 agent 共享
