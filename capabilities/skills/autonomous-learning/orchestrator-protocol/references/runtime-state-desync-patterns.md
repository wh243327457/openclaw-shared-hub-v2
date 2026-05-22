# Runtime State Desync Patterns

2026-05-22 发现的运行时状态文件与真实系统状态脱节模式。

## Pattern: delivery-state vs health_alert.log desync

**症状**: `delivery-state.json` 显示 `status: normal` / `consecutive_delivery_failures: 0`，但 `health_alert.log` 记录连续 95 次失败，guard 进入 `push_guard_blocked`。

**根因**: delivery-state.json 由 node-10 的 `delivery-state.json` 初始化时写入，之后未被实际推送流程更新。它是"设计意图"而非"运行时真相"。

**检查方法**:
```bash
# 对比两个数据源
jq '.status, .consecutive_delivery_failures, .last_delivery_at' runtime/hermes/autonomous-learning/delivery-state.json
tail -3 runtime/hermes/health_alert.log
```

**检测规则**: 如果 health_alert.log 最近 5 条包含 `push_guard_blocked` 或 `consecutive_failures > 10`，但 delivery-state.json 显示 `status: normal`，即为 desync。

**影响**:
- cron guard 可能基于 delivery-state 做判断，导致误判推送健康
- 用户报告可能遗漏真实故障

**处理**:
- 不要自动 patch delivery-state.json（可能覆盖其他运行时写入）
- 在 Spec Review 中标记 desync，在通知报告的"需要你决策"中提出
- 长期方案：推送流程应直接写 delivery-state.json，而非依赖外部状态同步

## Pattern: state.json vs runtime artifacts staleness

**症状**: `state.json` 记录 node-12 (health-dashboard) 为 done，但引用的 artifact 路径或结构化文件缺失/过期。

**检查方法**:
```bash
# 验证 state.json 中声明的 artifact 是否存在
cat runtime/hermes/autonomous-learning/state.json | grep -o '"artifact": "[^"]*"' | while read line; do
  f=$(echo $line | cut -d'"' -f4)
  test -f "/home/vany/agent/shared/$f" && echo "OK: $f" || echo "MISSING: $f"
done
```

**影响**: 自动化脚本依赖 state.json 声明的 artifact 存在性做决策，缺失时行为未定义。

## Backlog dormancy pattern

**症状**: backlog items 标记为 `active_warning_only`，长期无人跟进。

**检测规则**: `updated_at` 距今 > 5 天 且 priority 含 `active_warning_only` 时，在巡检报告中单独列出。

**原因**: `active_warning_only` 语义模糊——"monitor but don't act" 容易被人遗忘。

**建议**:
- 改为 `weekly_review` 或 `needs_periodic_check` 以增加可见度
- 或在 cron guard 中加检测：如果 backlog 有 dormant warning items，降级通知频率

## Applicability

这些模式适用于任何有"状态文件 + 独立日志"双源的自治系统巡检。检查 desync 应成为 scheduled learning 的标准 preflight 延伸。
