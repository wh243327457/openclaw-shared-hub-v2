# 2026-05-14 Orchestrator 超时诊断记录

## 问题

`github_learning_orchestrator.py` 作为 cron job 运行，shell timeout = 300s，内部 `OPENCLAW_TIMEOUT` = 1800s。两者不匹配导致 orchestrator 被 SIGKILL 时 OpenClaw 实际还未开始工作。

## 关键数据

### cron job state（超时后）

```json
{
  "7aa310ea-b264-40c8-b23a-ed655c565a69": {
    "lastRunAtMs": 1778715059038,    // 07:30:59 CST
    "lastRunStatus": "ok",
    "lastDurationMs": 340310          // 340s > 300s shell timeout
  }
}
```

注意：`lastRunStatus: ok` 是 SIGKILL 返回码 0 的误判，并非 orchestrator 正常完成。

### 时序

| 时间 | 事件 |
|------|------|
| 07:30 | orchestrator cron job 触发 |
| 07:30 | docker exec → openclaw cron run（OpenClaw schedule = 08:30 CST） |
| ~07:35 | shell timeout (300s) 杀死 orchestrator |
| 08:30 | OpenClaw cron 正常 scheduled 触发（与 orchestrator 无关） |

### inbox 状态

- `inbox/openclaw/daily/2026-05-13.md` ✅ 已存在（51行，来自 bridge 06:00）
- `inbox/openclaw/daily/2026-05-14.md` ❌ 不存在

## 修复

**方案 A（推荐）**：cron job timeout >= 2000s（大于 orchestrator OPENCLAW_TIMEOUT=1800s）

**方案 B**：分离 trigger / wait 为两个独立 cron job
