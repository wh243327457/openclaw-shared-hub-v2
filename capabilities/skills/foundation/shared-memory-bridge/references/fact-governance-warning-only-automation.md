# Shared v2 fact governance warning-only automation

## 适用场景

当 shared v2 已有 fact freshness / conflict-resolution 草案，用户要求“按计划让结构完整自主跑起来”时，优先落地 warning-only 自动化闭环，而不是直接开启 curated 自动写入。

## 最小闭环

1. `scripts/promoter.py --dry-run --scan-promote-candidates`
   - 扫描 inbox daily 候选。
   - 给出 `freshness_suggestion`、`stale_risk`、`possible_conflict`、`conflict_type_suggestion`、`recommended_state`、`evidence_needed`。
   - 只输出报告，不写 curated。

2. `scripts/verify_bridge.py`
   - 增加 `fact_governance` warning-only 检查。
   - 扫描 `curated/memory/facts/*.md` frontmatter。
   - 检查 `fact_id` 唯一性、`status`、`freshness_class`、`review_due_at`、`secret_checked`、`supersedes/superseded_by`、`disputed` 状态一致性。
   - 同 `scope + subject + attribute` 下多个 active 且 `value_summary` 不同时输出 `POSSIBLE_ACTIVE_FACT_CONFLICT` warning。
   - 旧 facts 缺 frontmatter 只输出 `LEGACY_FACT_METADATA_MISSING` warning，不让 bridge 失败。

3. `scripts/daily_maintenance.sh`
   - 在每日维护里加入 promotion governance dry-run scan。
   - 日志建议写到 `runtime/hermes/promotion-governance-cron.log`。
   - 保持 `curated_autopromotion_enabled=false`，由用户/总控审核后再晋升。

4. 模板与文档
   - 增加 `docs/fact-frontmatter-template.md`，统一 fact metadata 字段。
   - 更新 `docs/maintenance.md`，声明 governance scan 是 report-only。

5. 状态闭环
   - 更新 `runtime/hermes/autonomous-learning/state.json`：记录 `GOVERNANCE_WARNING_ONLY_AUTOMATION_ENABLED`、入口脚本、日志、测试路径、curated 写入禁用。
   - 更新 backlog 中相关治理项为 `warning_only_automation_wired`。

## TDD 验证建议

新增或维护 `tests/test_fact_governance.py`，至少覆盖：

- 过期 fact 输出 `STALE_FACT_REVIEW_NEEDED`。
- `status=disputed` 但 `conflict.status` 不匹配时输出 warning。
- 多个 active facts 同 `scope/subject/attribute` 且 value 不同输出 `POSSIBLE_ACTIVE_FACT_CONFLICT`。
- promoter candidate scan 输出 freshness/conflict 治理建议字段。

## 验证命令

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 tests/test_fact_governance.py -v
python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10 --max-candidates-per-file 5 > runtime/hermes/promotion-governance-final.json
python3 scripts/promoter.py --dry-run > runtime/hermes/promoter-final-dry-run.json
python3 scripts/verify_bridge.py > runtime/hermes/verify-final.json
python3 - <<'PY'
import json, pathlib
for name in ['promotion-governance-final.json','promoter-final-dry-run.json','verify-final.json']:
    payload = json.loads((pathlib.Path('runtime/hermes') / name).read_text())
    assert payload.get('ok') is True, name
print('final smoke json ok')
PY
DRY_RUN=1 SHARED_ONLY=1 RUN_GITHUB_LEARNING=0 scripts/daily_maintenance.sh
```

## Pitfalls

- 不要把 warning-only 检查变成自动 curated 晋升；自动化可以发现风险，但不能裁决事实为真。
- `review_due_at` 是复核提醒，不是删除 TTL。
- `stale` 不等于 false；只是需要复核。
- 旧 facts 缺 frontmatter 是兼容 warning，不应导致 `verify_bridge.py` exit 1。
- 如果用户明确说计划/目的已清晰并要求继续落地，不要继续停留在草案汇报；直接按既定安全边界实施、验证、更新状态。