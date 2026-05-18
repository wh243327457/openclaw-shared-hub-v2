# Self-Healing Agent rollout pattern

Use this when the user wants a global inspection / self-correction / self-repair mechanism for Hermes + OpenClaw + shared-hub systems.

## Core lesson

Do not start with an auto-repair cron. Start runtime-first and read-only:

1. Create a curated project entry and runtime workspace.
2. Define state, scan policy, repair backlog, and templates.
3. Implement a read-only baseline scanner.
4. Classify findings into actionable backlog and observations.
5. Generate approval-gated patch plans.
6. Only apply low-risk runtime canaries after safety review.
7. Consider cron only after repeated successful manual/canary runs.

## Recommended files

- `curated/memory/projects/self-healing-agent.md`
- `runtime/hermes/self-healing-agent/state.json`
- `runtime/hermes/self-healing-agent/scan-policy.json`
- `runtime/hermes/self-healing-agent/repair-backlog.json`
- `runtime/hermes/self-healing-agent/scripts/baseline_scan.py`
- `runtime/hermes/self-healing-agent/scripts/classify_findings.py`
- `runtime/hermes/self-healing-agent/findings/*.json`
- `runtime/hermes/self-healing-agent/patch-plans/*.md`
- `runtime/hermes/self-healing-agent/reviews/*.md`
- `runtime/hermes/self-healing-agent/templates/*.md`

## State flow

```text
IDLE
  -> COLLECT_SIGNALS
  -> CLASSIFY_FINDINGS
  -> PRIORITIZE_BACKLOG
  -> PLAN_REPAIR
  -> SAFETY_REVIEW
  -> CANARY_REPAIR
  -> VERIFY_REPAIR
  -> HUMAN_APPROVAL_REQUIRED | RUNTIME_PATCH_APPLIED
  -> RETROSPECT_AND_UPDATE_RULES
  -> IDLE
```

## Finding classes

- `config_drift`: target-system confusion, provider naming drift, model/fallback config mismatch.
- `model_instability`: repeated API errors, fallback not triggering, tool-use regressions.
- `workflow_stall`: state files lag behind real artifacts, unfinished review/fallback chains.
- `quality_regression`: report format drift, missing review fields, repeated low-quality outputs.
- `bridge_integrity`: manifest, symlink, MEMORY index, promoter/verify failures.
- `skill_drift`: shared skill missing from manifest, outdated commands, stale metadata.
- `cron_noise`: high-frequency notifications without substance, silent failures, repeated topics.

## Safety rules

- Baseline scanner is read-only.
- No Hermes/OpenClaw config writes without explicit target declaration and approval.
- No model/provider/fallback changes without approval.
- No gateway restart or cron enablement without approval.
- No curated promotion without Hermes review, and often user approval.
- No plaintext secrets in shared.
- Execution agents may propose repairs; Hermes owns final review.

## Implementation pitfalls

- Path math matters. If scripts live under `shared/runtime/hermes/self-healing-agent/scripts/`, then `SELF_HEALING_ROOT = Path(__file__).resolve().parents[1]` and `SHARED_ROOT = SELF_HEALING_ROOT.parents[2]`. An off-by-one parent can make the scanner falsely report missing `manifest.yaml`, `AGENTS.md`, and `curated/memory/MEMORY.md`.
- Treat a clean baseline as useful evidence, not as proof there is nothing to improve. The classifier can still emit observations such as recent failure evidence or current autonomous-learning node state.
- Keep `repair-backlog.json` small and actionable: separate `items` from `observations`.
- Use `verify_bridge.py` and JSON parsing after each stage.

## Minimal verification

```bash
cd /home/vany/agent/.openclaw/shared
python3 runtime/hermes/self-healing-agent/scripts/baseline_scan.py
python3 runtime/hermes/self-healing-agent/scripts/classify_findings.py
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/self-healing-agent')
for p in [base/'state.json', base/'repair-backlog.json'] + list((base/'findings').glob('*.json')):
    json.loads(p.read_text())
print('json ok')
PY
python3 scripts/verify_bridge.py
```
