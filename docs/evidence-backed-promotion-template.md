# Evidence-backed Promotion Candidate Template

本模板用于把 daily/runtime 中的观察转成 **候选晋升记录**。候选不等于长期事实；只有通过 shared governance 五门准入和 Hermes/人工复核后，才可写入 curated active claim。

```yaml
candidate_id: YYYYMMDD-agent-topic-slug
candidate_type: fact|project_state|workflow_rule|skill_candidate|open_question
source_agent: hermes|openclaw|future-agent|human
source_paths:
  - inbox/<agent>/daily/YYYY-MM-DD.md
evidence_refs:
  - inbox/<agent>/daily/YYYY-MM-DD.md#section
extracted_at: YYYY-MM-DDTHH:mm:ss+08:00
summary: 一句话候选
claim_draft:
  claim_id: kebab-case-id
  claim_type: fact|project_state|workflow_rule|user_preference|agent_system
  scope: user|project|workflow|agent-system|multi-agent
  lens: identity|world|pulse|journey
  topic: stable.topic.key
  confidence: 0.0
safety:
  sensitivity: low|medium|high
  secret_checked: true
  license_checked: true
  auto_apply_allowed: false
gates:
  long_term_value: pass|fail|unknown
  cross_agent_value: pass|fail|unknown
  evidence: pass|fail|unknown
  dedupe_conflict: pass|fail|unknown
  secret_check: pass|fail|unknown
decision:
  status: deferred|accepted|rejected|duplicate|disputed
  reviewer: hermes|human|openclaw
  notes: 决策理由
```

## 安全边界

- 每日学习、巡检、dreaming、reflect worker 默认只写 candidate。
- 不允许自动改 `curated/memory/facts/*.md` 为 active。
- 不允许自动改配置、provider、模型、cron、secret。
- 不确定证据必须标为 `unknown/deferred`。
