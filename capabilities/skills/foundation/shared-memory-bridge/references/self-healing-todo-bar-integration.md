# Self-healing todo bar integration pattern

Use this when scheduled inspection tasks need a durable todo source that the cron/healthcheck process can read and update.

## Key lesson

Do not replace the existing self-healing / inspection pipeline with a new todo workflow. Treat the todo bar as an embedded runtime sublayer inside the existing inspection flow.

## Recommended shape

```text
runtime/hermes/self-healing-agent/todo/
├── todo-list.json      # machine-readable truth source
├── todo-list.md        # human-readable rendered view
├── README.md           # rules for scheduled tasks
└── todo_manager.py     # list/add/update/complete/cancel/render CLI
```

Each todo item should include at least:

- `id`
- `title`
- `status`: `pending | scheduled | in_progress | blocked | done | cancelled`
- `priority`
- `due_at`
- `owner`
- `executor`
- `source`
- `notes`

## Integration points

1. `baseline_scan.py`
   - Read `todo/todo-list.json` during normal signal collection.
   - Validate that the todo JSON is parseable.
   - Add a `todo_bar_readable` check.
   - Add a compact `signals.todo_bar` summary with counts, open items, and overdue items.

2. `trial_cron_runner.py`
   - Keep the original baseline/classify/plan flow unchanged.
   - Add a final `todo_render` step that runs `todo_manager.py render`.
   - Validate `todo-list.json` and `todo-list.md` alongside state/backlog/snapshot validation.
   - Include a compact Todo Bar section in the trial report.

## Boundary rules

- Runtime-only writes are allowed for todo JSON/MD and cron reports.
- Do not treat todo items as user preferences or memory notes.
- Do not silently delete finished items; close them with `done` or `cancelled`.
- Do not auto-promote todo contents into curated memory.
- Do not create a new cron or restructure the inspection pipeline unless the user explicitly asks.

## Pitfalls

- Avoid adding todo handling as a separate workflow: the user explicitly prefers it as a sublayer inside the original inspection process.
- If patching repeatedly fails due to fuzzy anchor mismatch, stop using repeated patch attempts and rewrite the small target file or use a deterministic script, then run syntax/JSON validation.
- If a snapshot references a variable computed in another function, recompute it locally or pass it explicitly; do not rely on cross-function scope.

## Minimal verification

```bash
cd /home/vany/agent/shared
python3 runtime/hermes/self-healing-agent/scripts/baseline_scan.py
python3 runtime/hermes/self-healing-agent/scripts/classify_findings.py
python3 runtime/hermes/self-healing-agent/scripts/trial_cron_runner.py
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('runtime/hermes/self-healing-agent')
for rel in ['todo/todo-list.json', 'repair-backlog.json', 'state.json']:
    json.loads((base / rel).read_text())
assert (base / 'todo/todo-list.md').exists()
print('self-healing todo integration ok')
PY
```
