# Self-healing agent scaffold session

Use this reference when the user asks to design or implement a global inspection / self-repair / self-improvement agent for Hermes + OpenClaw + shared-hub systems.

## Durable lesson

Do not implement self-repair as an immediate auto-fixer. The safe class-level pattern is:

```text
read-only baseline scan
  -> evidence-backed finding classification
  -> prioritized repair backlog
  -> minimal patch plan with rollback/verification
  -> safety review
  -> one low-risk canary repair
  -> verification and review
  -> only after repeated success, propose cron/automation
```

## User expectation

For self-healing / self-improvement agents, the user wants an overall landing plan first, not premature execution. Include:

- detailed state flow
- node inputs/actions/artifacts/acceptance criteria
- runtime-first scaffold
- clear safety boundaries
- approval gates for config/model/gateway/cron changes
- resumable state files and implementation plan

## Recommended shared-hub artifacts

Use a four-part runtime-first landing package:

- `curated/memory/projects/self-healing-agent.md` — stable project architecture and status
- `runtime/hermes/self-healing-agent/implementation-plan.md` — executable phased plan
- `runtime/hermes/self-healing-agent/state.json` — machine-readable state
- `runtime/hermes/self-healing-agent/templates/` — baseline scan, finding, patch-plan, safety-review, notification templates

Optional runtime directories:

- `runs/` — scan snapshots and canary run records
- `findings/` — normalized finding JSON/MD
- `repair-backlog.json` — prioritized repair queue
- `patch-plans/` — proposed fixes with rollback/verification
- `reviews/` — Hermes safety/quality verification
- `pending-approval/` — high-risk actions awaiting user approval

## Safety boundaries

Auto-allowed initially:

- read-only validation
- runtime snapshot writes
- finding/backlog/patch-plan writes
- runtime state updates

Require user approval:

- modifying Hermes/OpenClaw config
- switching models/providers
- restarting gateway/services
- creating/updating cron jobs
- promoting curated memory
- deleting files
- touching secrets/auth/env

## Finding taxonomy

| Category | Examples | Default handling |
|---|---|---|
| `config_drift` | target-system mixups, provider naming issues | patch plan only, approval required |
| `model_instability` | repeated APIConnectionError, fallback not firing | model test plan, no auto switch |
| `workflow_stall` | state says pending but artifacts exist | reconciliation plan |
| `quality_regression` | messy reports, missing review fields, repeated topics | template feedback + canary |
| `bridge_integrity` | symlink/MEMORY/verify_bridge issues | P0 plan and validation |
| `skill_drift` | stale commands, missing shared manifest entry | skill patch plan |
| `cron_noise` | noisy pushes, repeated failures without evidence | throttle/pause proposal, approval required |

## Verification pattern

After scaffold or low-risk changes, run:

```bash
cd <shared-root>
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/self-healing-agent')
for name in ['state.json', 'scan-policy.json', 'repair-backlog.json']:
    json.loads((base/name).read_text())
print('json ok')
PY
python3 scripts/promoter.py --dry-run
python3 scripts/promoter.py
python3 scripts/verify_bridge.py
```

## Reporting style

Use short conclusion first, then compact tables:

- current status
- what was created/changed
- verification result
- next recommended node
- decisions needed
- file paths last
