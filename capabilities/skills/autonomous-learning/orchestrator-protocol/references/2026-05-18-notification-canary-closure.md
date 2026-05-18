# 2026-05-18 — Node 07/08 notification + canary closure

## 触发背景

自主学习全自动化推进到最后阶段：

- node-07 `notification-automation`：生成固定模板的可扫读通知。
- node-08 `canary-run`：跑通一次低风险全链路 canary。

本次不是新增一条窄技能，而是补充 `autonomous-learning/orchestrator-protocol` 这个类级技能的收口经验。

## Node 07：通知自动化的可复用做法

### 目标

把自主学习运行产物转换成微信/日报可读报告，并且可用 linter 防止退化成流水账。

### 建议脚本职责

`runtime/hermes/autonomous-learning/scripts/generate_readable_notification.py`

应保持以下边界：

- 只读 runtime 中的 run / output / reviews / pending queue。
- 只写 `runtime/hermes/autonomous-learning/notifications/<run-id>-readable-report.md`。
- 不发送消息。
- 不启用 cron。
- 不写 curated。

### Linter 最小检查

报告生成后必须自动检查：

1. 必备章节是否齐全：计划/执行/审计/沉淀/收获/下一步/决策/产出文件。
2. 决策块是否存在：无决策必须写“暂无需要你决策的事项”；有决策必须表格化。
3. 文件路径是否后置且限量：最多 5 条；超过只给目录入口。
4. 是否出现长段落：微信报告不应有密集大段解释。
5. 是否泄露内部机制：不要出现 send_message、cron 内部说明、Traceback、工具调用细节。

### 审计数据读取坑点

Spec review 可能写成不同格式：

- `verdict: PASS`
- `**结果: PASS**`
- `✅ PASS`

脚本不能只匹配一种格式，否则会把已通过的审计误报为 `UNKNOWN`。未来写解析器时应覆盖这三类常见表达。

## Node 08：低风险 canary 的验收口径

Node 08 不是必须重新联网跑一个高成本任务；如果最近已有低风险运行完整覆盖以下链路，可以复用该 run 作为 canary evidence：

1. 选题/路由存在 instruction 或 run-state。
2. 执行产物已落盘。
3. Spec review 与 Quality review 已落盘。
4. 晋升决策进入 runtime queue 或明确 runtime-only。
5. 通知报告已生成并通过 notification linter。
6. `state.json`、inbox 记录已更新。
7. JSON 检查、`promoter.py --dry-run`、`verify_bridge.py` 通过。

### 关键边界

- canary 通过不等于允许 cron。
- canary 通过不等于自动 curated 晋升。
- 18/20+ 高分项只能进入“待用户确认”，不能自己晋升。
- 最终汇报只说用户要知道的状态，不贴大段 verify 输出。

## 推荐最终汇报

使用小表格：

| 节点 | 状态 |
|---|---|
| node-07 | done |
| node-08 | done |
| node-09 | next |

然后用 3–5 条说明：跑通了什么、验证结果、下一步 node-09 做什么。

## 可复用教训

1. 通知自动化也需要测试/lint，否则模板会逐渐退化。
2. canary 验收应看“链路证据是否完整”，而不是机械要求重新执行昂贵任务。
3. 状态推进必须同步写 `state.json` 和 `inbox/hermes/daily/YYYY-MM-DD.md`，让后续 agent 可恢复。
4. 验证命令通过后，用户汇报里只保留结论和关键产物路径；完整 JSON 输出不要推给用户。
