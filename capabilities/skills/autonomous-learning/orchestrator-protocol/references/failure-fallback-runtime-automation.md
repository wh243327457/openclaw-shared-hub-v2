# Failure/Fallback Runtime Automation Scaffold

## Context

During autonomous-learning node-06, the system needed a durable way to handle executor failures and timeouts without silent failure or inflated conclusions.

The durable pattern is a **runtime-only failure/fallback chain**.

## Required chain

When an executor times out, exits non-zero, is unavailable, fails audit, or produces missing evidence:

```text
executor failure
→ failure-evidence/<task>-<failure_type>.md
→ agent-outputs/fallback_executor/<task>.md   # only if fallback allowed
→ blocked-tasks.json
→ agent-health.json
→ fallback spec review
→ fallback quality review
```

## Script shape

Create a script under:

```text
runtime/hermes/autonomous-learning/scripts/handle_failure_fallback.py
```

Useful CLI shape:

```bash
python3 runtime/hermes/autonomous-learning/scripts/handle_failure_fallback.py \
  --run-id <run_id> \
  --task-id <task_id> \
  --executor <executor> \
  --failure-type timeout \
  --elapsed-seconds 600 \
  --summary '<what happened>' \
  --instruction runtime/hermes/autonomous-learning/orchestrator-runs/<run_id>/instruction.md \
  --evidence-text '<bounded evidence>' \
  --allow-fallback \
  --audit
```

## Fallback output requirements

Fallback output must explicitly say:

- `fallback_executor`
- `completed_with_fallback_executor`
- original executor did not complete
- confidence / evidence boundary
- no curated write
- no source-level/full audit claim unless evidence supports it

Good phrases:

- “降级产出”
- “未源码级深读”
- “bounded fallback”
- “README/API/design-doc level only”

## Audit behavior

Run normal Spec Review and Quality Review on fallback output. Low evidence fallback should usually receive archive/runtime-only scores, not promotion. A simulated timeout with little evidence scoring around 10-12/20 is expected and desirable; it proves the system is not exaggerating.

## Hard boundaries

- Do **not** relabel fallback as executor success.
- Do **not** write curated memory.
- Do **not** enable cron.
- Do **not** hide fallback status in report text.

## Verification

Run a simulated timeout canary:

```bash
cd <shared-root>
python3 runtime/hermes/autonomous-learning/scripts/handle_failure_fallback.py \
  --run-id 2026-05-18-node06-fallback-simulation \
  --task-id node06-simulated-delegate-timeout \
  --executor delegate_task \
  --failure-type timeout \
  --elapsed-seconds 600 \
  --summary 'Simulated delegate_task timeout for node-06 validation.' \
  --instruction runtime/hermes/autonomous-learning/orchestrator-runs/2026-05-18-daily-combo-learning-0000/instruction.md \
  --evidence-text 'timeout after 600s; no final executor output' \
  --allow-fallback \
  --audit
```

Then verify:

```bash
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/autonomous-learning')
for p in [base/'blocked-tasks.json', base/'agent-health.json']:
    json.loads(p.read_text())
print('fallback json ok')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

## State update

After validation, update only runtime state and inbox. Mark node-06 done only when evidence, fallback output, blocked task, agent health, and fallback reviews are all present.
