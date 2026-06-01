# 2026-05-27 Manual OpenClaw re-trigger + WeChat rate limit

## Scenario

Orchestrator cron timed out at 300s. The instruction was already generated (`instruction.md` at 07:31), but OpenClaw's cron hadn't been triggered for today's date. The last completed OpenClaw run was for yesterday (2026-05-26).

## What worked: manual re-trigger (NOT fallback)

This is **not** the "Hermes fallback" pattern (where OpenClaw has protocol errors and Hermes must do the learning itself). This is the simpler case where OpenClaw is healthy but just wasn't triggered in time.

### Steps performed

1. Confirmed instruction exists: `instruction.md` (07:31)
2. Checked OpenClaw container: `docker inspect -f '{{.State.Status}}' openclaw` → `running`
3. Triggered cron manually: `docker exec openclaw openclaw cron run 7aa310ea-...`
4. First attempt returned `"already-running"` (the timed-out orchestrator had triggered it)
5. Second attempt succeeded: `"enqueued": true`
6. Polled for output file every 30s — **found at 120s** (much faster than expected)
7. Ran audit on the output (16/16, all sections passed)
8. Updated knowledge base (copy to Obsidian daily learning dir)
9. Attempted WeChat push → rate limited

### Key timing insight

When the instruction already exists and the container is healthy, OpenClaw completes in **~2 minutes**, not the 10-15 minutes the orchestrator typically waits. The orchestrator's 1800s timeout is overly conservative for the "instruction already generated" case.

## WeChat rate limit details

### Error

```
SEND_FAIL:{'error': 'Weixin send failed: iLink sendmessage rate limited: ret=-2 errcode=None errmsg=rate limited'}
```

### Guard state

```json
{
  "consecutive_push_without_user_reply": 8,
  "last_push_at": "2026-05-26T05:16:28",
  "last_rate_limited_at": "2026-05-27T07:50:48"
}
```

- Guard at **8/10** consecutive pushes without user reply
- Cooldown: **600 seconds** after rate limit
- Last successful push was yesterday (May 26)
- The push guard lives in the Hermes Weixin platform layer, not in this pipeline

### Correct handling

1. Save push content to `wechat-push-YYYY-MM-DD.txt` ✅
2. Do NOT claim "已推送" or "发送成功"
3. Report: "推送内容已落盘，微信因 rate limit 未实际发出"
4. Wait for user reply (resets guard) or cooldown to expire
5. Update `status.json` with `push_status: "rate_limited"` and error details

### `send_weixin_direct` via execute_code

The gateway venv Python approach works (no network isolation issues on this host):

```python
hermes_python = "/root/.hermes/hermes-agent/venv/bin/python3"
hermes_src = "/root/.hermes/hermes-agent/src"
# ... (see hermes-wechat-push skill for full template)
```

The rate limit is a platform-level iLink constraint, not a code bug.

## Recovery playbook for "instruction exists but OpenClaw not triggered"

```
1. Verify instruction exists
   ls -la <shared-root>/runtime/hermes/github-hot-project-learning/instruction.md

2. Check OpenClaw is running
   docker inspect -f '{{.State.Status}}' openclaw

3. Trigger manually
   docker exec openclaw openclaw cron run <job-id>

4. If "already-running", wait 30s and retry

5. Poll for output (30s intervals, 15min max)
   ls -la <shared-root>/inbox/openclaw/daily/YYYY-MM-DD.md

6. Once output exists, run audit-only:
   python3 scripts/github_learning_orchestrator.py --skip-openclaw --date YYYY-MM-DD

   OR do manual audit + knowledge base + push (as in this session)
```

## Status JSON update

After manual recovery, update `status.json`:

```json
{
  "overall_status": "pipeline_ok_wechat_rate_limited",
  "hermes": {
    "push_status": "rate_limited",
    "push_error": "iLink rate limited (ret=-2), guard at 8/10, cooldown ~600s"
  }
}
```
