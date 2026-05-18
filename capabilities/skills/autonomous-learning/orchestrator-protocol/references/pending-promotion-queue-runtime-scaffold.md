# Pending Promotion Queue Runtime Scaffold

## Context

During the autonomous-learning iteration, node-05 needed to solve a recurring problem: high-quality learning outputs stayed buried in `runtime/` even after quality review, but automatic curated promotion was intentionally forbidden.

The durable pattern is a **runtime-only pending promotion queue**.

## What to build

Create a script under:

```text
runtime/hermes/autonomous-learning/scripts/build_pending_promotion_queue.py
```

It scans `runtime/hermes/autonomous-learning/reviews/*quality-review.md`, extracts quality scores and promotion recommendations, then writes:

```text
runtime/hermes/autonomous-learning/pending-promotion-queue.json
runtime/hermes/autonomous-learning/pending-promotion-queue.md
```

## Policy

- Score `18-20`: `awaiting_user_approval`
- Score `15-17`: `runtime_learning_only`
- Score `10-14`: `archive_for_reference`
- Score `<10`: `rejected_low_quality`
- Any sensitive risk: `blocked_sensitive_review_needed`

## Hard boundaries

- Do **not** write curated memory.
- Do **not** decide facts are true.
- Do **not** auto-accept or reject facts beyond queue status.
- Do **not** enable cron.
- The queue is visibility + decision support only.

## Important implementation detail

If both human review and deterministic auto review exist for the same candidate, prefer the human review. Deterministic review can over-score short or scaffolded outputs. Use grouping by canonical item id and choose non-`-auto-` review first.

## Verification

Run:

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 runtime/hermes/autonomous-learning/scripts/build_pending_promotion_queue.py --recent-limit 20 --min-score 15
python3 - <<'PY'
import json
json.load(open('runtime/hermes/autonomous-learning/pending-promotion-queue.json'))
print('pending promotion queue json ok')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

## State update

After validation, update only runtime state:

- `runtime/hermes/autonomous-learning/state.json`
- `inbox/hermes/daily/YYYY-MM-DD.md`

Mark node-05 done only when queue generation works and shared verification still passes.
