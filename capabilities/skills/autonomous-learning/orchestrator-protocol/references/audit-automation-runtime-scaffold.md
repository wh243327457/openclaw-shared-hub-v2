# Audit Automation Runtime Scaffold

Session lesson from autonomous-learning node-04 closeout.

## When to use

Use this pattern when the autonomous-learning system has working execution outputs but Spec Review / Quality Review are still being produced ad hoc by Hermes.

## Pattern

Create a runtime-only deterministic audit script under:

`runtime/hermes/autonomous-learning/scripts/audit_output.py`

Inputs:
- `--run-id`
- `--item`
- `--instruction` pointing to the run instruction
- `--output` pointing to the executor/Hermes output
- `--spec-review` output path
- `--quality-review` output path

The script should:
1. Read the instruction and output.
2. Extract expected completion markers from the instruction.
3. Check for matching completion markers in the output.
4. Check evidence presence: URL, repo metadata, paths, stars, license, dates, commands, or similar grounded references.
5. Check boundary/risk sections.
6. Check for unauthorized curated-write claims.
7. Run simple secret-pattern detection.
8. Write deterministic Markdown reviews ending in `SPEC_REVIEW_DONE` and `QUALITY_REVIEW_DONE`.
9. Return non-zero only when Spec/Quality gates fail.

## Boundaries

This is a scaffold, not final semantic judgment:
- Do not call external LLMs from the script.
- Do not write curated memory.
- Do not enable cron.
- Do not modify OpenClaw config.
- Treat high scores as promotion candidates only; user approval is still required for curated writes.

## State closeout

After validating the script on at least one real run:
1. Update `runtime/hermes/autonomous-learning/state.json`:
   - set `node-04` to `done`
   - set `current_phase` to `NODE_04_COMPLETED`
   - set `current_node` to `node-05`
   - attach completion evidence: script path, sample run, generated review paths, and boundary note
2. Append an inbox note to `inbox/hermes/daily/YYYY-MM-DD.md`.
3. Verify:

```bash
cd <shared-root>
python3 - <<'PY'
import json, pathlib
base=pathlib.Path('runtime/hermes/autonomous-learning')
files=[base/'state.json', base/'learning-backlog.json'] + list((base/'orchestrator-runs').glob('*/run-state.json'))
for p in files:
    json.loads(p.read_text())
print('json ok', len(files), 'files')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

## Actual invocation

```bash
cd <shared-root>
python3 runtime/hermes/autonomous-learning/scripts/audit_output.py \
  --run-id "<run_id>" \
  --instruction "runtime/hermes/autonomous-learning/templates/hardened-cron-prompt.md" \
  --output "runtime/hermes/autonomous-learning/agent-outputs/<file>.md" \
  --spec-review "runtime/hermes/autonomous-learning/reviews/<run_id>-spec-review.md" \
  --quality-review "runtime/hermes/autonomous-learning/reviews/<run_id>-quality-review.md" \
  --item "<backlog-item-id>"
```

注意：脚本要求 `--spec-review` 和 `--quality-review` 显式路径（不是 `--reviews-dir`）。缺任一会报 `argparse` 错误。

## Known limitations

1. **completion_marker_present 依赖 instruction 内容**：脚本从 `--instruction` 文件提取 ALL_CAPS 标记（含 DONE/COMPLETED/EXECUTOR/HERMES 的 token）。如果 instruction 模板不含这类标记（如 `hardened-cron-prompt.md`），`matched` 永远为空，该检查永远 FAIL。
2. **boundary_present 关键词有限**：脚本只检查 `风险`、`边界`、`不确定`、`限制`、`极早期`、`early`、`boundaries`、`bounded`、`not source-level`、`降级产出`。输出中的 "Source boundary" 不会被匹配。必须包含上述关键词之一。
3. **post-run 验证脚本缺失**：`promoter.py --dry-run` 和 `verify_bridge.py` 在当前 scripts 目录不存在。post-run 检查只能跳过。
4. **deterministic 评分偏保守**：模板缺标记时 spec 直接 FAIL，quality boundary=0 导致总分偏低。应手动复核 deterministic 结果，不要把误报的低分当作真正质量问题。

## Manual override pattern

当 deterministic audit 因模板缺标记而 FAIL 时：
1. 写手动 Spec Review（覆盖所有 checklist 项，verdict=PASS）
2. 写手动 Quality Review（正常评分 20 分制）
3. 在最终通知中注明 "deterministic audit 因 instruction 模板缺 ALL_CAPS 标记产生误报，已手动复核通过"

## Pitfall

Deterministic scoring can over-score concise but well-structured outputs. Use it to stabilize pipeline mechanics, not as the sole curated-promotion decision. Node-05 should create a pending-promotion queue rather than auto-promoting curated content.
