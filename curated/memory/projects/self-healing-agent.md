# Self-Healing Agent / 全局巡查与自我修复 Agent

- 项目：Self-Healing Agent
- 版本：v0.1
- 状态：RUNTIME_SCAFFOLD_CREATED
- 更新时间：`2026-05-17T22:48:47+08:00`
- 真相源路径：`shared/curated/memory/projects/self-healing-agent.md`
- runtime 工作区：`shared/runtime/hermes/self-healing-agent/`
- 关联系统：`autonomous-learning-system`、`shared-hub-v2`、Hermes runtime、OpenClaw runtime、future-agent 接入槽

## 1. 定位

这个 agent 不是“再做一个学习 agent”，而是全局巡查、自我纠错、自我修复迭代的总控机制。

它负责定期或按需检查：

1. 自主学习链路是否跑偏、重复、低质量或卡在半途中。
2. shared 中台是否出现路径、索引、symlink、metadata、promoter/verify 规则漂移。
3. Hermes/OpenClaw/future-agent 的配置、模型、工具、skills、cron、gateway 是否出现异常迹象。
4. 已有失败记录是否被归因、归档、转成 patch plan，而不是散落在日志中。
5. 模板、skill、路由策略、fallback 策略是否因为历史失败需要更新。

## 2. 与自主学习系统的关系

自主学习系统解决“主动学什么、怎么学、怎么沉淀”。

Self-Healing Agent 解决“系统哪里坏了、哪里在退化、怎么安全修复、怎么防止同类错误再次出现”。

二者关系：

```text
Autonomous Learning
  -> 产生 outputs / reviews / failures / backlog / health
  -> Self-Healing Agent 巡查这些证据
  -> 生成 findings / patch plans / canary repair runs
  -> 经 Hermes review + 用户审批后
  -> 更新模板 / skill / runtime 策略 / blocked tasks / agent health
  -> 反哺 Autonomous Learning
```

## 3. 设计边界

- 默认只做“巡查 + 诊断 + patch plan”，不直接改高风险配置。
- 不自动写 curated；稳定结论必须经 Hermes review，必要时等用户确认。
- 不写 secret；只能引用环境变量名或脱敏状态。
- 不直接重启 gateway、改模型组、启用 cron；这些属于需要明确授权的动作。
- 可自动执行低风险只读检查和 runtime 写入，例如 JSON 解析、promoter dry-run、verify_bridge、日志摘要、finding 记录。
- 执行 agent 可以提出修复建议，但不能自行宣布修复通过；Hermes 拥有最终 review 权。

## 4. 状态流转

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

## 5. 节点输入、动作、产物、验收

| 节点 | 输入 | 动作 | 产物 | 验收 |
|---|---|---|---|---|
| COLLECT_SIGNALS | runtime 状态、reviews、failure-evidence、logs、verify 输出 | 只读采集 | signal snapshot | 证据路径完整，不含 secret |
| CLASSIFY_FINDINGS | signal snapshot | 按故障类型归因 | findings/*.json | 每条 finding 有 severity/category/evidence |
| PRIORITIZE_BACKLOG | findings、用户目标、系统风险 | P0/P1/P2 排序 | repair-backlog.json | P0 不超过 3 条，能解释优先级 |
| PLAN_REPAIR | repair-backlog | 生成最小修复计划 | patch-plans/*.md | 每个计划含文件、动作、回滚、验证 |
| SAFETY_REVIEW | patch plan | 判断是否可自动执行 | safety review | 高风险必须 pending approval |
| CANARY_REPAIR | 低风险 patch plan | 小范围试修 | canary run | 只改 runtime 或模板局部，不碰 secret |
| VERIFY_REPAIR | canary 结果 | 跑测试/校验/对比 | reviews/* | 验证命令明确通过或失败 |
| RETROSPECT_AND_UPDATE_RULES | 修复结果 | 提炼预防规则 | skill patch / template feedback | 同类错误有预防入口 |

## 6. Finding 分类

| 类别 | 示例 | 默认处置 |
|---|---|---|
| config_drift | Hermes/OpenClaw/shared 目标混用、provider 命名异常 | 生成只读诊断和 patch plan，写入 pending approval |
| model_instability | APIConnectionError、超时、fallback 未触发、模型工具调用差 | 触发模型能力测试计划，不自动切主模型 |
| workflow_stall | state.json 停在旧节点但产物已完成 | reconciliation patch plan |
| quality_regression | 报告格式乱、review 缺字段、重复主题 | 模板反馈 + 小流量 canary |
| bridge_integrity | symlink、manifest、MEMORY 索引、verify_bridge 异常 | P0，先 runtime 修复计划，再验证 |
| skill_drift | skill 失效、命令过时、共享 skill 未登记 | patch skill + 更新 manifest |
| cron_noise | 高频通知无实质内容、重复推送、失败无证据 | 暂停建议/节流建议，需要审批 |

## 7. 初始落地策略

v0.1 只创建 runtime 脚手架与模板，不启用定时任务。

推荐下一步：

1. 先跑一次只读 baseline scan。
2. 将发现写入 `runtime/hermes/self-healing-agent/findings/`。
3. 生成 `repair-backlog.json`，只挑一个低风险问题做 canary。
4. Hermes 做 Safety Review + Quality Review。
5. 通过后再决定是否创建 cron 或共享 skill。

## 8. 当前状态

- 已创建 runtime 工作区和基础配置。
- 已登记到 shared MEMORY 主索引。
- 当前未启用 cron，未执行自动修复。
- 下一步是生成并运行 baseline scanner（只读）。
