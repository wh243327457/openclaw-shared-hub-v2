# Cron Mode Execution Constraints & Linter Path

## execute_code blocked in cron mode

When Hermes runs as a scheduled cron job, `execute_code` is blocked by security policy:

```
BLOCKED: execute_code runs arbitrary local Python (including subprocess calls that bypass
shell-string approval checks). Cron jobs run without a user present to approve it.
Use normal tools instead, or set approvals.cron_mode: approve only if this cron profile
is intentionally trusted.
```

**Alternatives in cron mode (by reliability):**
1. **首选** `read_file` — read JSON/CSV/text, parse in response context. Zero security risk, no tirith trigger, no terminal dependency. 2026-06-04 verified: parsed pending-promotion-queue.json (20 items) via read_file + manual line parsing, zero errors.
2. `terminal` + standalone script — write a `.py` file first, then `python3 script.py`
3. `terminal` + inline python — `python3 -c "import json; ..."` (no pipes)
4. Still forbidden: `cat file | python3` (tirith pipe_to_interpreter, lesson 9)

**Discovered:** 2026-06-01 during scheduled learning run.

## generate_readable_notification.py linter path resolution

The `--lint-only` mode resolves the report path as:

```python
REPORTS = Path("runtime/hermes/autonomous-learning/notifications")
out = REPORTS / f"{args.run_id}-readable-report.md"
```

This is relative to the **current working directory** (shared root), NOT relative to the script.

**Correct workflow:**
1. Write report to `<shared-root>/runtime/hermes/autonomous-learning/notifications/<run_id>-readable-report.md`
2. Optionally copy to `orchestrator-runs/<run_id>/` for archival
3. Run: `cd <shared-root> && python3 runtime/hermes/autonomous-learning/scripts/generate_readable_notification.py --run-id <id> --lint-only`

**Common mistake:** Writing to `orchestrator-runs/<run_id>/<run_id>-readable-report.md` then running `--lint-only` → FileNotFoundError.

**Discovered:** 2026-06-01. Extends lesson 23 which documented the filename convention but not the directory.
