# 自主学习进度复核：状态源优先级与汇报口径（2026-05-18）

## 触发场景

用户问“最近自主学习进度怎么样 / 继续 / 到什么阶段了”时，不要只按聊天记忆或单个 plan 文件回答；必须做 shared runtime + curated 的交叉复核。

## 推荐读取顺序

1. `shared/manifest.yaml`、`shared/AGENTS.md`、`shared/curated/memory/MEMORY.md`：确认 shared 根、分层与项目索引。
2. `shared/curated/memory/projects/autonomous-learning-system.md`：确认已晋升的长期事实、未晋升候选、架构观察卡。
3. `shared/runtime/hermes/autonomous-learning/state.json`：确认节点总数、done 数、current phase。
4. `shared/runtime/hermes/autonomous-learning/health-dashboard.json`：确认 cron、delivery、blocked task、pending promotion 的汇总口径。
5. `shared/runtime/hermes/autonomous-learning/pending-promotion-summary.json` 与 `pending-promotion-queue.json`：确认等待用户决策的候选。
6. `shared/runtime/hermes/autonomous-learning/orchestrator-runs/*/run-state.json`：确认最近真实 run 的状态。
7. `shared/runtime/hermes/autonomous-learning/auto-full-automation-plan.md` / `implementation-plan.md`：只作为计划叙述，不作为唯一状态源。

## 状态冲突处理

若 plan 文档的“当前状态”滞后，而 `state.json` 与 `health-dashboard.json` 显示更晚阶段：

- 以 `state.json` + `health-dashboard.json` 为当前运行状态；
- 在汇报中明确说“计划文档某段落滞后”；
- 不要因为 plan 旧状态而降级真实进度；
- 不要顺手改 curated 或启用/关闭 cron，除非用户明确要求。

## 汇报形状

进度汇报应优先让用户 10 秒看懂：

- 总体结论：一句话说明是方案阶段、半自动阶段、cron hardened 阶段，还是阻塞阶段。
- 状态表：节点完成数、cron、auto curated write、用户审批、阻塞任务、健康状态。
- 最近完成：选题、路由、执行协议、双审、fallback、通知、pending queue、cron hardening。
- 学到什么：列已晋升长期模式和重要观察卡，不要只汇报基础设施。
- 需要用户决策：列高分未晋升候选，给出 accept/defer/reject 建议。
- 产出文件：最多 5 条，路径后置。

## 典型结论模板

```text
自主学习系统已经从“方案/半自动”推进到“节点收口 + hardened cron”。
当前主要不是缺执行链路，而是 pending promotion 队列里哪些高分候选允许进入 curated。
```

## Pitfalls

- 不要把旧 plan 的“Node 2/Node 3”当成真实状态，必须用 runtime 状态交叉验证。
- 不要只说“共享中台整理好了”；用户问自主学习进度时，还要说明学到了什么、晋升了什么、还等什么决策。
- 不要把 internal cron/job 细节堆给用户；需要时只报频率、是否启用、是否自动晋升。
