# Curated Fact Claim Schema

本文件定义 shared hub v2 的 claim-like curated memory frontmatter 规范。它是 **新增与后续迁移的目标格式**，不是立即强制旧文件全部迁移的破坏性规则。

## 目标

把 `curated/memory/facts/` 与关键 `curated/memory/projects/` 从“普通 Markdown 记录”升级为可治理的长期 claim：

- 有生命周期状态。
- 有证据引用。
- 有来源 agent。
- 有适用范围与主题。
- 可被 recall helper 按强/弱/无匹配检索。
- 可被后续 reflect candidate worker 提出 update / retire / dispute 建议。

## 标准 frontmatter

```yaml
---
claim_id: kebab-case-id
claim_type: fact|project_state|workflow_rule|user_preference|agent_system
status: active|retired|disputed|superseded|deleted
confidence: 0.0-1.0
scope: user|project|workflow|agent-system|multi-agent
lens: identity|world|pulse|journey
topic: stable.topic.key
source_agent: hermes|openclaw|future-agent|human
source_paths:
  - inbox/hermes/daily/YYYY-MM-DD.md
evidence_refs:
  - inbox/hermes/daily/YYYY-MM-DD.md#section
sensitivity: low|medium|high
created_at: YYYY-MM-DDTHH:mm:ss+08:00
updated_at: YYYY-MM-DDTHH:mm:ss+08:00
review_status: draft|reviewed|approved
review_after: YYYY-MM-DD
supersedes: []
superseded_by: []
---
```

## 字段说明

| 字段 | 含义 | 规则 |
|---|---|---|
| `claim_id` | 稳定 ID | kebab-case，尽量与文件名一致 |
| `claim_type` | claim 类型 | fact/project_state/workflow_rule/user_preference/agent_system |
| `status` | 生命周期 | active 表示当前可用；retired/superseded/disputed 不应默认召回为强事实 |
| `confidence` | 置信度 | 0.0-1.0；无证据时不得高于 0.6 |
| `scope` | 适用范围 | 区分 user/project/workflow/agent-system/multi-agent |
| `lens` | Personal Model 映射 | identity/world/pulse/journey |
| `topic` | 稳定主题键 | 用于去重、召回、open questions 聚合 |
| `source_agent` | 产生来源 | hermes/openclaw/future-agent/human |
| `source_paths` | 原始来源路径 | 指向 inbox/runtime/外部引用，不复制全文 |
| `evidence_refs` | 可核验证据 | Phase 2 后新增事实推荐必填；旧事实 warning-only |
| `sensitivity` | 敏感级别 | high 不得自动写入或推送 |
| `review_status` | 审核状态 | approved 才可作为强事实 |
| `review_after` | 复核日期 | volatile/pulse 类 claim 必填 |
| `supersedes` / `superseded_by` | 替代关系 | 不删除历史，用状态治理 |

## 与既有标准的兼容

旧标准中的字段仍兼容：

- `fact_id` 可视为 `claim_id`。
- `freshness_class` 可辅助决定 `review_after`。
- `last_verified_at` 可映射为 `updated_at` 或证据时间。
- `source` 可作为 `source_paths` / `evidence_refs` 的过渡来源。

## 状态语义

| status | 召回行为 | 写入规则 |
|---|---|---|
| active | 可作为 strong/weak match 候选 | 必须有审核和证据 |
| retired | 默认不作为当前事实 | 保留历史，不删除 |
| disputed | 只能作为冲突提示 | 需要人工裁决 |
| superseded | 默认返回新 claim | 必须写 superseded_by |
| deleted | 默认不召回 | 仅保留最小 tombstone |

## 写入与迁移策略

1. 新增 curated fact 应尽量采用本 schema。
2. 旧 facts 不立即强制迁移；缺字段先 warning-only。
3. `evidence_refs` 初期只作为治理 warning，不作为 verify 阻断。
4. 不从 assistant-authored prose 直接生成用户事实。
5. secret、token、cookie、private key 等不得写入 `source_paths` 或正文。
6. runtime/cache/log 可作为 evidence path，但不晋升为 curated 正文。

## 最小示例

```yaml
---
claim_id: shared-hub-v2-structure
claim_type: agent_system
status: active
confidence: 0.95
scope: agent-system
lens: world
topic: shared.structure.v2
source_agent: hermes
source_paths:
  - manifest.yaml
  - AGENTS.md
evidence_refs:
  - manifest.yaml
sensitivity: low
created_at: 2026-05-22T00:00:00+08:00
updated_at: 2026-05-22T00:00:00+08:00
review_status: approved
review_after: 2026-06-22
supersedes: []
superseded_by: []
---
```

## 验收

- 新 schema 文档存在。
- `scripts/check_curated_claims.py` 能 warning-only 扫描缺失字段。
- `scripts/shared_recall.py` 能读取本 schema 字段。
- `verify_bridge.py` 保持 ok=true。
