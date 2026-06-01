# pending-promotion-queue.json Schema

## 顶层结构

```json
{
  "version": "0.1",
  "generated_at": "2026-05-19T12:02:00+08:00",
  "policy": { ... },
  "summary": {
    "total": 20,
    "awaiting_user_approval": 7,
    "runtime_learning_only": 13,
    "blocked_sensitive_review_needed": 0
  },
  "items": [ ... ]
}
```

**注意**: 候选列表的 key 是 `items`，不是 `candidates`。

## items[] 单项结构

```json
{
  "candidate_id": "github-growth-2026-05-18-zero",
  "status": "awaiting_user_approval",
  "score": 19,
  "recommendation": "建议晋升 curated（待用户确认）",
  "quality_review": "runtime/hermes/autonomous-learning/reviews/...-quality-review.md",
  "output": "runtime/hermes/autonomous-learning/agent-outputs/...md",
  "target_hint": "curated/memory/projects/..."
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `candidate_id` | string | 唯一标识，格式通常为 `<type>-<date>-<slug>` |
| `status` | string | `awaiting_user_approval` 或 `runtime_learning_only` |
| `score` | number | 质量评分（满分 20） |
| `recommendation` | string | 晋升建议文本 |
| `quality_review` | string | quality review 文件的相对路径 |
| `output` | string\|null | 执行产出文件路径，可能为 null |
| `target_hint` | string | 晋升目标路径提示 |

## 常见误读

- ❌ `data.get('candidates')` → ✅ `data.get('items')`
- ❌ `item.get('topic')` → ✅ `item.get('candidate_id')`
- ❌ `item.get('quality_score')` → ✅ `item.get('score')`
- ❌ `item.get('source_run')` → ✅ 无此字段，用 `quality_review` 路径反推

## summary vs items 计数

summary.total 可能与 len(items) 不一致（summary 可能包含已归档项）。以 summary 为准做报告，以 items 为准做逐项处理。
