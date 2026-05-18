# Orchestrator Run State Reconciliation

Use this reference when a long-running shared-hub/autonomous-learning task looks inconsistent across `state.json`, `run-state.json`, and actual artifacts.

## Trigger

User asks:
- “方案到什么地步了？”
- “能完整跑通了吗？”
- “继续确认”
- “状态是不是已经完成？”

## Core lesson

Do not trust one state file alone. Runtime state can lag behind actual artifacts. A run may already have:

- executor failure evidence saved
- fallback output written
- spec review completed
- quality review completed

while `run-state.json` still says `FALLBACK_OUTPUT_WRITTEN` or `PREPARED`.

## Audit order

From shared root:

```bash
cd /home/vany/openclaw-data/.openclaw/shared
```

Read:

1. `manifest.yaml`
2. `AGENTS.md`
3. `curated/memory/MEMORY.md`
4. `runtime/hermes/autonomous-learning/state.json`
5. `runtime/hermes/autonomous-learning/implementation-plan.md`
6. Target run:
   - `runtime/hermes/autonomous-learning/orchestrator-runs/<run_id>/run-state.json`
   - `runtime/hermes/autonomous-learning/agent-outputs/<executor>/<run_id>*.md`
   - `runtime/hermes/autonomous-learning/reviews/<run_id>-spec-review.md`
   - `runtime/hermes/autonomous-learning/reviews/<run_id>-quality-review.md`

## Reconciliation rule

If artifacts prove the run is reviewed but state lags:

1. Update only runtime state files:
   - target `run-state.json`
   - global `runtime/hermes/autonomous-learning/state.json`
   - optionally runtime backlog if the review explicitly recommends backlog items
2. Do not write curated memory.
3. Do not enable cron.
4. Do not create or update shared skills unless the user specifically asked for skill-library maintenance.
5. Keep fallback output explicitly labeled as fallback; never relabel it as executor success.

Suggested terminal states:

- `EXECUTOR_FAILED` when failure evidence exists but no fallback/review exists
- `FALLBACK_OUTPUT_WRITTEN` when fallback exists but reviews do not
- `AWAITING_USER_APPROVAL_BEFORE_AUTOMATION_OR_PROMOTION` when spec + quality reviews exist

## Minimal verification

```bash
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/autonomous-learning')
files = [
    base/'state.json',
    base/'learning-backlog.json',
]
files += list((base/'orchestrator-runs').glob('*/run-state.json'))
for path in files:
    json.loads(path.read_text())
print('json ok:', len(files), 'files')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

## Reporting language

Use this distinction clearly:

- “手动闭环已跑通” means prepare → execute/fail → evidence → fallback → review → runtime state closeout works.
- “自动化上线已跑通” requires cron/event execution and promotion policy to be enabled and verified; do not claim this when `automation_enabled=false` or `cron_allowed=false`.
