# Autonomous Learning Semi-Auto Candidate Lessons

Context: shared-hub v2 autonomous-learning moved from manual canary to a semi-auto candidate stage. The durable lesson is the workflow shape, not the specific date/run ids.

## Pattern: plan-only semi-auto before cron

Before enabling any cron or unattended execution, prepare a semi-auto candidate packet under runtime only:

- Generate `semi-auto-candidates/<candidate_id>/approval-packet.md`.
- Generate a `draft-runs-index.json` listing proposed run drafts.
- Generate each proposed `orchestrator-runs/<run_id>/run-state.json`, `instruction.md`, and `orchestrator-report.md`.
- Keep every run in `PREPARED_FOR_USER_REVIEW` or equivalent.
- Set gates explicitly false: `execution_allowed`, `cron_allowed`, `curated_promotion_allowed`, `external_notification_allowed`, `shared_skill_update_allowed`.

Allowed in this stage:

- plan drafts
- orchestrator run drafts
- runtime backlog items
- JSON/promoter dry-run/verify_bridge validation
- human approval packet

Forbidden in this stage:

- executing Claude Code/OpenClaw automatically
- creating or enabling cron
- writing curated memory
- sending external notifications
- updating shared skills as part of the semi-auto candidate

## Pattern: Claude Code deep-dive granularity guard

When Claude Code hits `max_turns_exhausted` repeatedly on research/deep-dive tasks, do not keep increasing turn budget. Treat it as a task-shape problem.

For future deep-analysis instructions, split so a single Claude Code task covers at most:

- 1 repository or product
- 3 source files or doc sections
- 1 architecture question
- 1 output artifact

Suggested sub-run sequence:

1. discovery-summary
2. source-file-pass-1
3. mechanism-map
4. final-synthesis

Default turn budgets:

- quick source check: 4
- bounded deep read: 8
- synthesis from prior outputs: 6

After two `max_turns_exhausted` attempts in the same run family, save failure evidence, then split the task or produce an explicitly labelled controller fallback. Do not mark fallback output as executor output, and do not promote fallback output to curated by default.

## Required validation after runtime-only changes

```bash
cd <shared-root>
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/autonomous-learning')
for path in [
    'agent-capabilities.json',
    'learning-backlog.json',
    'failover-policy.json',
    'state.json',
]:
    json.loads((base / path).read_text())
print('json ok')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

## Status language

Report this as “manual or semi-auto candidate green” unless cron/unattended execution has actually been enabled and verified. Do not imply full automation is live just because plan-only drafts and validation pass.
