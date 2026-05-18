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

## Pitfall

Deterministic scoring can over-score concise but well-structured outputs. Use it to stabilize pipeline mechanics, not as the sole curated-promotion decision. Node-05 should create a pending-promotion queue rather than auto-promoting curated content.
