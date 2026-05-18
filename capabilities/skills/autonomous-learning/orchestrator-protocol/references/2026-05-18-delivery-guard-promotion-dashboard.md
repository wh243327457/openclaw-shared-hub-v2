# 2026-05-18 Autonomous Learning Delivery Guard / Promotion Summary / Health Dashboard

## Session signal

A long-running autonomous-learning rollout needed three runtime-only operational closures after cron hardening:

1. Weixin delivery risk should not be handled only as prose policy; it needs a machine-readable runtime state and downgrade recommendation.
2. Pending promotion queues can grow too large for Weixin/chat reports; provide a compact top-candidate summary rather than dumping the full queue.
3. A health dashboard should combine runtime state, delivery state, pending-promotion counts, and shared-hub verification results.

## Durable pattern

For scheduled autonomous-learning systems, add a runtime-only operations layer:

- `delivery-state.json`: tracks delivery status, consecutive failures, recommended delivery target, and report compactness.
- `cron_hardening_guard.py --mode delivery`: reads delivery policy and non-secret platform guard counters, classifies state into `normal`, `compact_report_required`, or `local_only_recommended`.
- `pending-promotion-summary.md/json`: compresses `pending-promotion-queue.json` to a top-N decision table.
- `health-dashboard.md/json`: summarizes current phase, completed nodes, delivery state, pending-promotion counts, agent health, and runs `promoter.py --dry-run` + `verify_bridge.py`.

## Guardrails

- Runtime-only: do not write curated memory, do not send messages, do not create or modify cron jobs automatically.
- Do not store secrets or credentials in shared; if reading platform guard files, copy only non-secret counters/timestamps/errors.
- Weixin delivery downgrade is a recommendation/state gate, not a hidden side effect. The cron final report should respect it by becoming ultra-compact or local-only.
- Full pending-promotion queues belong in runtime files; user-facing messages should show only counts and top candidates.

## Verification checklist

```bash
cd /home/vany/agent/.openclaw/shared
python3 runtime/hermes/autonomous-learning/scripts/cron_hardening_guard.py --mode delivery --write-state
python3 runtime/hermes/autonomous-learning/scripts/build_pending_promotion_queue.py --recent-limit 20 --min-score 15
python3 runtime/hermes/autonomous-learning/scripts/build_pending_promotion_summary.py --limit 5
python3 runtime/hermes/autonomous-learning/scripts/generate_health_dashboard.py
python3 - <<'PY'
import json, pathlib
base=pathlib.Path('runtime/hermes/autonomous-learning')
for p in [base/'state.json', base/'delivery-state.json', base/'pending-promotion-summary.json', base/'health-dashboard.json']:
    json.loads(p.read_text())
print('json ok')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

## Reporting shape

Use a compact table:

| Item | Result |
|---|---|
| delivery_status | `normal` / `compact_report_required` / `local_only_recommended` |
| pending promotion | awaiting/runtime-only/blocked counts |
| health dashboard | OK/errors/warnings |
| verification | JSON/promoter/verify status |

Always keep `需要你决策` separate: promotion candidates require accept/defer/reject; no automatic curated write.
