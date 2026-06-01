# 2026-05-22 fallback: OpenClaw protocol mismatch + Weixin push guard

## Trigger

During the GitHub hot project daily learning closed loop, the orchestrator started the OpenClaw container and it eventually became `healthy`, but `openclaw cron run <job-id>` failed with:

```text
GatewayClientRequestError: protocol mismatch
GatewayTransportError: gateway closed (1002): protocol mismatch
```

The learning artifact for the day did not exist yet at `shared/inbox/openclaw/daily/YYYY-MM-DD.md`.

## Working fallback pattern

1. Keep the canonical shared root as `/home/vany/agent/shared`.
2. Confirm the daily instruction exists:
   - `runtime/hermes/github-hot-project-learning/instruction.md`
3. Use a Hermes subagent / fallback executor to perform the learning task from that instruction and write the OpenClaw-compatible artifact:
   - `inbox/openclaw/daily/YYYY-MM-DD.md`
4. Run the orchestrator in audit-only mode for that date:
   ```bash
   cd /home/vany/agent/shared
   python3 scripts/github_learning_orchestrator.py --skip-openclaw --date YYYY-MM-DD
   ```
5. Verify generated artifacts:
   - `inbox/openclaw/daily/YYYY-MM-DD.md`
   - knowledge base daily report under `/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/`
   - `runtime/hermes/github-hot-project-learning/wechat-push-YYYY-MM-DD.txt`

## Weixin push guard behavior

If the final send command fails with:

```text
hermes send: Weixin send failed: push_guard_active
```

Do **not** bypass or repeatedly resend. Treat this as a platform-level active push safety gate. The correct closeout is:

- report that learning/audit/knowledge-base update succeeded;
- report that Weixin delivery was blocked by `push_guard_active`;
- point to the saved push file;
- do not claim “微信已推送”.

The guard state can be inspected for diagnosis at `/root/.hermes/weixin/weixin-push-guard.json`, but do not edit it as part of this pipeline.

## Reporting wording

Use precise status separation:

- “学习、审计、知识库落盘已完成”
- “OpenClaw 原定 cron 触发失败，Hermes fallback 已代执行”
- “微信未实际发出，原因是 push_guard_active；推送内容已落盘”

This avoids overstating completion when delivery is blocked.
