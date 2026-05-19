---
name: orchestrator-protocol
description: 自主学习系统编排协议 — 状态机驱动的多 agent 学习任务编排，含 review gates、fallback、approval 闸门
version: "1.0"
status: active
agents:
  - hermes
  - openclaw
  - future-agent
owner: shared-hub
category: autonomous-learning
---

# Orchestrator Protocol

自主学习系统的编排协议。将一个学习主题转化为可审计、可恢复、有审批闸门的 canary run。

## 适用场景

- 每日自主学习任务编排
- 跨 agent 调研任务（Claude Code 深读、OpenClaw 发现）
- 需要 Spec Review + Quality Review 双审的长期沉淀任务
- 新 agent 接入时的能力验证

## 前置条件

读取以下文件：
1. `shared/manifest.yaml`
2. `shared/AGENTS.md`
3. `shared/curated/memory/projects/autonomous-learning-system.md`
4. `shared/runtime/hermes/autonomous-learning/learning-weights.json`
5. `shared/runtime/hermes/autonomous-learning/learning-backlog.json`

## 状态机

```text
PREPARED
  → EXECUTION_READY
  → DISPATCHING
  → EXECUTOR_COMPLETED | EXECUTOR_FAILED
  → FALLBACK_OUTPUT_WRITTEN | REVIEW_READY
  → SPEC_REVIEWED
  → QUALITY_REVIEWED
  → AWAITING_USER_APPROVAL
  → PROMOTED | ARCHIVED
```

失败分支：
```text
EXECUTOR_FAILED
  → FAILURE_EVIDENCE_SAVED
  → FALLBACK_OUTPUT_WRITTEN（仅 allow_fallback=true）
  → REVIEW_READY
```

## 执行步骤

### Step 1：准备 run

```bash
cd <shared-root>
python3 runtime/hermes/autonomous-learning/scripts/manual_runtime_orchestrator.py \
  --run-id "$(date +%Y-%m-%d)-<topic-slug>" \
  --topic "<学习主题>" \
  --executor claude-code \
  --mode prepare-only \
  --source-url "<url1>" \
  --source-url "<url2>" \
  --allow-fallback
```

产出：
- `runtime/hermes/autonomous-learning/orchestrator-runs/<run_id>/run-state.json`
- `runtime/hermes/autonomous-learning/orchestrator-runs/<run_id>/instruction.md`

### Step 2：派发执行 agent

**Bounded subagent 预算（强制）：**

| 任务价值/复杂度 | 子 agent 数量 | 适用场景 | 禁止事项 |
|---|---:|---|---|
| 普通日报/小时学习 | 0–1 | 一个 GitHub 项 + 一个非 GitHub 轻量项 | 不为每个小问题开 agent |
| 高价值调研/源码 canary | 1–2 | 一个 discovery + 一个 deep-read/review | 不超过 2 个并行执行 agent |
| 重大架构/跨系统决策 | 2–3 | 独立证据面明显不同，且有用户明确收益 | 不开 4+ 个，不做无限搜索 |

派发前必须写清：`agent_goal`、`input evidence`、`output artifact`、`time budget`、`completion marker`、`fallback plan`。如果任一项说不清，先不派发。

高频 cron 默认只允许 1 个主要执行子 agent；另一个学习项应优先由 Hermes 轻量 fetch/fallback 完成。只有当任务满足“高价值 + 证据面独立 + 输出可审计”时，才允许 2 个子 agent。不得为了显得自动化而滥用 subagent。

**Claude Code / delegate_task 方式：**

```
delegate_task(
  goal="按照 instruction.md 完成深度分析，输出纯 Markdown",
  context="instruction 内容 + 源 URLs + 完成标记要求",
  toolsets=["web", "terminal", "file"]
)
```

**OpenClaw 方式：**
```bash
docker exec openclaw-main agent --local --agent main \
  -p "<discovery instruction>"
```

**关键规则：**
- Claude Code 失败时，Hermes 可以生成 fallback 产出，但必须标记 `fallback_executor`
- 执行 agent 不得自行宣布 APPROVED_FOR_PROMOTION
- max_turns 不少于 20（WebSearch + 分析场景）

### Step 3：Hermes Spec Review

检查清单：
- [ ] 覆盖 instruction 中所有必填字段
- [ ] 有明确完成标记
- [ ] 有证据路径/URL/命令输出
- [ ] 没有越权写入 curated
- [ ] 没有把 runtime/cache/secret 写入长期记忆

输出：`reviews/<run_id>-spec-review.md`

### Step 4：Hermes Quality Review

检查清单：
- [ ] 结论有证据
- [ ] 足够具体，避免空泛总结
- [ ] 能转化为行动/skill/项目规则
- [ ] 指出不确定性和适用边界
- [ ] 与用户目标相关

评分：满分 20（证据 5 + 深度 5 + 可复用 5 + 边界 5）

输出：`reviews/<run_id>-quality-review.md`

### Step 5：晋升决策

| 质量分 | 决策 |
|--------|------|
| 18-20 | 建议晋升 curated，需用户确认 |
| 15-17 | 晋升 runtime learning，不自动进 curated |
| 10-14 | 存档，供后续参考 |
| <10   | 标记为失败教训 |

### Step 6：通知用户

必须包含完整流程摘要，但微信/日报类自主学习报告必须采用“短结论 + 表格 + 后置文件清单”的可扫读格式，禁止长段流水账。核心目标是让用户 10 秒内看懂：学了什么、谁做的、审计是否通过、沉淀到哪里、是否需要拍板。

固定结构：
```text
📚 自主学习系统 — 本轮学习报告
时间 + 结论：✅ 正常 / ⚠️ 降级完成 / ❌ 失败

📋 今天/本轮学了什么
表格：类型 / 主题 / 为什么学

🤖 执行情况
表格：学习项 / 执行方 / 状态 / 备注

🔍 审计结果
表格：学习项 / Spec / Quality / 晋升

📊 结果沉淀
3 条以内：产出、决策、风险

💡 对用户有用的收获
3 条以内，每条为“短标题：一句可复用结论”

🎯 下一步
2 条以内，每条一行

需要你决策
无决策时必须写“暂无需要你决策的事项”；有决策时用表格：决策项 / 选项 / 影响 / 建议

产出文件
最多 5 条相对路径，超过写目录入口
```

排版硬规则：
- 不要把内部状态机、cron 机制、send_message 说明推给用户。
- 每个 bullet 尽量 1 行；不要写 5 行以上长段落。
- 文件路径统一后置，最多 5 条。
- 失败/降级要明确说明影响，但不要贴长状态机；用一句人话。
- 决策事项不能混在“下一步”或“收获”里。

对于高频 cron（例如每小时）运行：每轮应避免重复上一轮主题；优先选择新的 GitHub 增长项目或新的非 GitHub 学习角度。若上一轮留下高价值待决策事项，本轮可以转为复核、补证据或把决策表讲清楚，而不是机械重复采集。

## 硬规则

1. 默认 mode 是 prepare-only，不自动派发
2. 永远不自动启用 cron
3. 永远不自动晋升 curated（需用户确认）
4. 任何 executor 故障必须保存失败证据
5. fallback 产出必须标记 `fallback_executor`
6. 执行 agent 不得自行宣布 review 通过

## 关键文件

| 文件 | 用途 |
|------|------|
| `orchestrator-runs/<run_id>/run-state.json` | 运行状态机 |
| `orchestrator-runs/<run_id>/instruction.md` | 执行 agent 指令 |
| `agent-outputs/<executor>/<run_id>.md` | 执行产出 |
| `reviews/<run_id>-spec-review.md` | 规格审查 |
| `reviews/<run_id>-quality-review.md` | 质量审查 |
| `learning-weights.json` | 学习组合权重 |
| `learning-backlog.json` | 候选学习主题 |

## 教训记录

1. Claude Code 直接写 runtime 文件不稳定 → 改为 stdout-capture 或 delegate_task
2. Claude Code max_turns 6~12 不够做 WebSearch + 分析 → 至少 20
3. 执行 agent 会越权自称 review 通过 → 模板必须禁止
4. OpenClaw 容器路径映射问题 → 优先写容器 canonical 路径
5. 高频/每小时自主学习任务中，delegate_task 可能因网络或外部网页读取在 600s 内超时；这不是“静默失败”的理由。必须保存 `failure-evidence/<task_id>-delegate-timeout.md`，再由 Hermes 生成明确标注 `fallback_executor` 的降级产出，并在最终报告中写清“未源码级深读/未完整联网复核”等边界。
6. 子 agent 是高成本执行资源，不是默认并行复制人。普通日报/小时学习默认 0–1 个；高价值 canary 1–2 个；重大跨系统决策最多 2–3 个。超过 3 个或无法说明 output artifact/time budget/fallback plan 时，必须先拆任务或停止派发。
7. 当 cron 提示某个配置技能找不到（例如 `foundation/console-style-progress-report`）时，最终报告开头必须保留简短告警；不要把它埋进文件清单或审计表。
8. 高频学习报告如果出现 16–17/20 的 runtime learning 候选，不要自动晋升 curated；应用"需要你决策"表格把是否做 POC、是否允许补证据后晋升讲清楚。
9. 安全扫描环境禁止 `curl | python3` 管道；用 `execute_code` + `urllib.request` 做 GitHub API/README 抓取。详见 `references/github-discovery-fallback.md` 的 pitfall 节。
10. node-07 通知自动化应配套 linter：检查必备章节、决策块、文件路径限量、长段落和内部术语泄露；Spec review 解析要兼容 `verdict: PASS`、`结果: PASS`、`✅ PASS` 等常见格式，避免把已通过审计误判为 UNKNOWN。
11. pending promotion queue 要把“晋升”和“分流”分开处理：用户批准的候选才写 curated；未批准的高分候选可重新分类为 observation card/runtime-only/awaiting approval。相似候选（如同一项目跨日期重复出现）应合并成单一观察卡，避免重复长期事实。详见 `references/2026-05-18-promotion-candidate-triage.md`。
12. node-08 canary 验收看链路证据是否完整，不必机械重跑高成本联网任务；如果最近运行已覆盖选题/路由、执行产物、双审、晋升队列/边界、通知报告、状态回写、promoter dry-run 和 verify_bridge，即可作为低风险 canary evidence。canary 通过仍不代表允许 cron 或自动 curated 晋升。详见 `references/2026-05-18-notification-canary-closure.md`。
14. node-09 cron hardening closure：上线 autonomous-learning cron 前/同时必须有 runtime-only policy、preflight/prompt/postrun guard、hardened prompt、保守 schedule、最小 toolsets、Weixin 限流处理和人工晋升边界；更新现有 cron 优先于创建重复 job。详见 `references/2026-05-18-cron-hardening-closure.md`。
15. `audit_output.py` deterministic audit 的 `completion_marker_present` 检查从 instruction 文件中提取 ALL_CAPS 标记（DONE/COMPLETED/EXECUTOR/HERMES）；如果 instruction 模板（如 `hardened-cron-prompt.md`）不含这类标记，该检查永远 FAIL，连带 `boundary_present` 也可能因关键词不匹配而 FAIL。此时必须做手动 Spec/Quality review 覆盖 deterministic 结果，不要把 14/20 误判为真正低质量。同时 `promoter.py --dry-run` 和 `verify_bridge.py` 在当前 scripts 目录不存在，post-run 检查只能跳过这两步。详见 `references/audit-automation-runtime-scaffold.md`。

## 参考资料

- `references/audit-automation-runtime-scaffold.md` — node-04 审计自动化收口模式：runtime-only deterministic audit script 的输入/输出、边界、状态更新和验证命令；提醒确定性评分只能稳定流程，不可替代 curated 晋升判断。
- `references/pending-promotion-queue-runtime-scaffold.md` — node-05 晋升候选队列模式：从 quality reviews 扫描 18/20+ 候选，写 runtime-only pending queue，必须用户确认后才可进 curated；同项优先采用人工 review 而非 auto review。
- `references/failure-fallback-runtime-automation.md` — node-06 失败/回退自动化模式：executor 超时/失败后保存 failure evidence、fallback_executor 产出、blocked-tasks、agent-health，并对 fallback 做双审，禁止把 fallback 伪装成成功。
- `references/2026-05-17-hourly-learning-fallback.md` — 每小时自主学习 cron 中 delegate_task 超时后的 fallback、双审、报告排版经验。
- `references/2026-05-17-readable-autonomous-learning-reports.md` — 用户反馈微信推送"格式太乱"后的可扫读报告模板、文件清单后置、决策单列和 bounded subagent 预算修正。
- `references/github-discovery-fallback.md` — GitHub trending 页面超时时的 search API fallback 技巧（created:>7d + sort=stars）。
- `references/2026-05-18-notification-canary-closure.md` — node-07/08 收口经验：可扫读 notification 生成器与 linter 的最小检查、Spec review PASS 格式兼容、以及用完整链路证据验收低风险 canary 的标准。
- `references/2026-05-18-cron-hardening-closure.md` — node-09 收口经验：scheduled autonomous-learning 的 policy/guard/prompt 三件套、现有 cron 更新策略、Weixin 限流边界、preflight/postrun 验证清单。
- `references/2026-05-18-promotion-candidate-triage.md` — pending promotion queue 分流经验：批准项进 curated，未批准高分候选重新分类，重复主题合并观察卡，用户汇报只暴露需要拍板项。
- `references/2026-05-18-progress-review-status-sources.md` — 用户询问“最近自主学习进度”时的状态源优先级与汇报口径：以 `state.json` + `health-dashboard.json` 交叉验证真实阶段，识别 plan 文档滞后，并把 pending promotion 决策单独列出。

