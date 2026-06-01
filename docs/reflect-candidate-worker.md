# Reflect Candidate Worker Template

用途：从 curated/runtime 中发现“可能需要补证据、复核、退休、冲突裁决”的候选项。

## 关键原则

- candidate-only：只写 `runtime/hermes/reflect-candidates/*.jsonl`。
- 不自动修改 `curated/memory/facts/` 或 `projects/`。
- 不自动修改配置、provider、模型、cron、secret。
- 每条 candidate 必须包含 `auto_apply_allowed: false`。
- Hermes/人工按 shared governance 五门准入复核后，才可决定是否更新 curated。

## 命令

```bash
cd <shared-root>
python3 scripts/reflect_candidate_worker.py --json
```

## 输出类型

- `metadata_gap`：缺 claim metadata / evidence_refs。
- `stale_review`：超过 review_after。
- `possible_conflict`：同 topic 多个 active claim。
- `retire_candidate`：可能已过期的 pulse/journey 类信息。

当前落地版本先实现 `metadata_gap`，其余类型保持模板能力，不启用自动判断。
