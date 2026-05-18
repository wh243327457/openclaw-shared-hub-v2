# Autonomous Learning Semi-Auto Effect Check Pattern

Use this when the user says to "run one version and see the effect" for the autonomous-learning system, but full cron/unattended execution has not been explicitly approved.

## Trigger

- User asks to try the autonomous-learning capability / run a version / see effect.
- Current system is in semi-auto or plan-only mode.
- Cron, curated auto-promotion, and external notification are still gated.

## Safe default

Create a runtime-only semi-auto candidate packet. Do not execute OpenClaw or Claude Code automatically unless the user explicitly approves that next execution step.

Required gates in every generated candidate/run draft:

```json
{
  "execution_allowed": false,
  "cron_allowed": false,
  "curated_promotion_allowed": false,
  "external_notification_allowed": false,
  "shared_skill_update_allowed": false
}
```

## File shape

Under `runtime/hermes/autonomous-learning/` create:

- `semi-auto-candidates/<candidate_id>/approval-packet.md`
- `semi-auto-candidates/<candidate_id>/draft-runs-index.json`
- For each proposed run:
  - `orchestrator-runs/<run_id>/run-state.json`
  - `orchestrator-runs/<run_id>/instruction.md`
  - `orchestrator-runs/<run_id>/orchestrator-report.md`

Set run status to `PREPARED_FOR_USER_REVIEW`.

## Recommended first effect-check bundle

A good first plan-only bundle contains three bounded drafts:

1. **GitHub / technical project discovery plan**
   - executor: `openclaw`
   - goal: discover up to 3 candidate projects or sources
   - no deep analysis yet
2. **Shared-memory governance warning scan plan**
   - executor: `hermes-controller`
   - goal: inspect fact freshness / conflict warning policies in warning-only mode
   - no curated edits
3. **Autonomous-learning effect review plan**
   - executor: `hermes-controller`
   - goal: define how to judge whether the semi-auto cycle is useful before execution/cron

Recommend executing only the first low-risk discovery run if the user approves the next step.

## Validation

After runtime-only changes, run at minimum:

```bash
cd <shared-root>
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/autonomous-learning')
paths = [
    base/'agent-capabilities.json',
    base/'learning-backlog.json',
    base/'learning-weights.json',
    base/'failover-policy.json',
    base/'state.json',
]
paths += sorted((base/'semi-auto-candidates').glob('*/draft-runs-index.json'))[-1:]
paths += sorted((base/'orchestrator-runs').glob('*/run-state.json'))
for p in paths:
    json.loads(p.read_text())
print(f'json ok: {len(paths)} files')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

Expected report language:

- "半自动候选计划生成成功，验证通过"
- Explicitly say what did **not** happen: no OpenClaw/Claude execution, no cron, no curated writes, no external notification, no shared skill update.
- Give one recommended next step, usually approving the first low-risk discovery run.

## Pitfalls

- Do not imply autonomous learning is fully live because plan drafts validated.
- Do not silently move from plan-only to execution.
- Do not write curated memory from an effect-check run.
- Do not create cron as part of the effect check.
