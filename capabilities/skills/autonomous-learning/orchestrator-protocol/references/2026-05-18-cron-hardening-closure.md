# 2026-05-18 — node-09 cron hardening closure

## Trigger

Autonomous-learning reached node-09 after node-07 notification automation and node-08 canary closure. The remaining risk was that a scheduled learning job could run without explicit guardrails: repeated Weixin pushes, recursive cron changes, too many executor agents, or accidental curated promotion.

## Reusable pattern

For autonomous-learning cron hardening, add three runtime-only artifacts before treating a scheduled job as production-ready:

1. **Policy JSON** — `runtime/hermes/autonomous-learning/cron-hardening-policy.json`
   - schedule frequency and minimum interval
   - max executor/subagent budget
   - delivery constraints and Weixin rate-limit handling
   - approval gates for curated promotion, faster schedules, new cron jobs, fan-out, and config/secret changes
   - preflight and post-run checklists

2. **Guard script** — `runtime/hermes/autonomous-learning/scripts/cron_hardening_guard.py`
   - `--mode preflight`: validate JSON state, policy, notification template/script, and approval gates
   - `--mode prompt --prompt-file ...`: lint cron prompt for mandatory safety/readability terms
   - `--mode postrun --report-file ...`: run report lint plus `promoter.py --dry-run` and `verify_bridge.py`

3. **Hardened prompt template** — `runtime/hermes/autonomous-learning/templates/hardened-cron-prompt.md`
   - first run preflight
   - no curated writes / no recursive cron scheduling / no secrets
   - no `send_message` inside cron; scheduler final response handles delivery
   - max 1 primary executor for high-frequency learning by default
   - failure evidence required for timeout/failure
   - final Weixin report must be short, table-based, and put file paths last

## Cron update pattern

For an existing autonomous-learning cron job, update rather than duplicate it:

- Keep schedule conservative: `0 */12 * * *` unless user approves faster cadence.
- Set `workdir` to `/home/vany/agent/.openclaw/shared` so relative runtime paths and AGENTS context resolve correctly.
- Restrict toolsets to the minimum needed: `terminal`, `file`, `skills`, `web`, `delegation`.
- Attach only the governing class skill: `autonomous-learning/orchestrator-protocol`.
- Preserve Weixin delivery if that is the intended channel, but require compact report format.

## Weixin rate-limit boundary

If previous delivery has `ret=-2` / rate-limited:

- Do not claim a fixed official threshold.
- Do not keep pushing long reports.
- Harden the prompt/report first: compact under ~3000 chars, table-based, no internal logs.
- If consecutive delivery failures occur, pause the job or switch delivery to `local` until user replies or approves resume.

## Validation checklist

Before marking node-09 done:

```bash
cd /home/vany/agent/.openclaw/shared
python3 - <<'PY'
import json, pathlib
base=pathlib.Path('runtime/hermes/autonomous-learning')
for p in [base/'state.json', base/'learning-backlog.json', base/'cron-hardening-policy.json', base/'pending-promotion-queue.json']:
    json.loads(p.read_text())
print('json ok')
PY
python3 runtime/hermes/autonomous-learning/scripts/cron_hardening_guard.py --mode preflight
python3 runtime/hermes/autonomous-learning/scripts/cron_hardening_guard.py --mode prompt --prompt-file runtime/hermes/autonomous-learning/templates/hardened-cron-prompt.md
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

All should exit 0. Then update `state.json` with `NODE_09_COMPLETED`, `current_node=maintenance`, and record cron job id/name/schedule/workdir/toolsets in completion evidence.

## Pitfalls

- Do not create a second autonomous-learning cron job when the existing job can be updated; duplication makes rate limits and state ownership worse.
- Do not let cron prompts recursively create/update cron jobs.
- Do not let cron runs auto-promote curated facts; 18+/20 stays `awaiting_user_approval`.
- Do not bury delivery-rate warnings in a file list; mention them briefly in status and encode guardrails in policy/prompt.
- Prompt lint should treat missing safety/readability terms as at least warnings; fix the prompt until warnings are zero before updating the live job.

## Outcome shape

A completed node-09 means the system is in maintenance/running state, not unrestricted autonomy:

- scheduled job can run
- preflight/postrun checks exist
- compact Weixin reports are enforced
- high-risk writes still require user approval
- operator can pause/switch delivery if Weixin rate limits recur
