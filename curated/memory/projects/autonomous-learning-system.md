# 自主学习系统正式架构方案

- 项目：Autonomous Learning System
- 版本：v0.1
- 状态：IMPLEMENTATION_STARTED
- 更新时间：`2026-05-15T01:08:17+08:00`
- 真相源路径：`shared/curated/memory/projects/autonomous-learning-system.md`
- runtime 工作区：`shared/runtime/hermes/autonomous-learning/`

## 1. 设计目标

本系统不是单一的 GitHub Trending 总结器，而是一个长期运行的“自主学习组合调度系统”。

核心目标：

1. 让系统每天主动学习，不只等待用户提问。
2. 让学习内容覆盖 GitHub 项目、书籍、教程、理论/论文、行业资讯、问题复盘、工具工作流、用户关注领域。
3. 让 Hermes、OpenClaw、Claude Code、future-agent 按能力分工，而不是做重复劳动。
4. 通过 shared-hub-v2 保持跨 agent 持续上下文。
5. 通过状态机、模板、审计、证据等级、回滚和审批闸门，避免新模型或低级模型接手后跑偏。
6. 让输出不只是“读了什么”，而是能沉淀为用户可复用的认知、方案、skills、项目状态和行动建议。

## 2. 总体原则

- Hermes 做总控，不亲自承担主要执行：负责计划、路由、调度、审计、沉淀、通知、模板改进。
- 执行层优先 Claude Code：适合源码深读、复杂推理、结构分析、代码级判断。
- OpenClaw 负责浏览器型与轻量采集：网页巡检、趋势发现、网页摘要、可视化上下文收集。
- future-agent 作为能力扩展槽：未来接入专项模型、检索器、评测器或本地工具。
- curated/memory 是跨 agent 真相源；runtime 只放运行时产物；inbox 只放原始记录。
- 任何长期沉淀都必须经过审计，不允许原始摘要直接晋升为真相。
- 失败默认保守：证据不足、输出缺字段、任务阻塞时，不晋升、不通知夸大结论，只记录阻塞并反馈上游。

## 3. 系统角色分工

| 角色 | 定位 | 适合任务 | 不适合任务 | 主要写入位置 |
|---|---|---|---|---|
| Hermes | 总控、审计、沉淀、通知 | 计划生成、任务路由、结果复核、长期记忆晋升、模板更新 | 大量网页浏览、长源码逐文件阅读 | curated、runtime/hermes、inbox/hermes |
| Claude Code | 深度执行 agent | 源码分析、架构拆解、复杂问题推理、代码验证 | 跨平台消息推送、共享记忆治理决策 | 由 Hermes 汇总后写入 shared |
| OpenClaw | 采集和轻量执行 agent | 网页采集、浏览器操作、趋势发现、初筛摘要 | 最终审计、长期记忆晋升决策 | inbox/openclaw、runtime/openclaw |
| future-agent | 扩展能力槽 | 专项检索、评测、领域模型、外部系统执行 | 未注册能力外任务 | inbox/future-agent、runtime/future-agent |
| shared-hub-v2 | 持续上下文层 | 真相源、原始记录、运行时状态、共享 skills | 执行业务逻辑 | curated/inbox/runtime/capabilities |

## 4. 双闭环模型

### 4.1 知识学习闭环

```text
学习需求/权重
  -> Hermes 生成 daily learning plan
  -> 按能力路由到 OpenClaw / Claude Code / future-agent
  -> 执行 agent 产出原始结果与证据
  -> Hermes 审计：完整性、证据、可复用性、用户价值
  -> 晋升：curated memory / project note / skill / backlog
  -> 通知用户：计划、执行、审计、结果、收获
```

### 4.2 系统自我改进闭环

```text
执行失败/审计失败/低质量输出
  -> 失败分类
  -> 写入 template-feedback
  -> 同类失败累计
  -> 生成 template-patch-plan 或 agent 能力调整建议
  -> Canary 小流量试运行
  -> 通过后更新模板/能力注册表/路由策略
```

## 5. 主流程状态机

```text
IDLE
  -> PLAN_DAILY_LEARNING
  -> ROUTE_TASKS
  -> DISPATCH_EXECUTION
  -> COLLECT_RESULTS
  -> SPEC_REVIEW
  -> QUALITY_REVIEW
  -> PROMOTION_DECISION
  -> WRITE_SHARED_MEMORY
  -> NOTIFY_USER
  -> RETROSPECT_AND_ADJUST
  -> IDLE
```

### 5.1 状态输入、动作、产物、验收

| 状态 | 输入 | 动作 | 产物 | 验收 |
|---|---|---|---|---|
| PLAN_DAILY_LEARNING | learning-weights、backlog、上次状态 | 生成当日组合学习计划 | daily-plan JSON/MD | 必含 GitHub 主线和至少一个非 GitHub 学习项 |
| ROUTE_TASKS | daily-plan、agent-capabilities | 选择 agent 和模板 | dispatch plan | 每个任务有 agent、原因、超时、fallback |
| DISPATCH_EXECUTION | dispatch plan | 下发 instruction | agent raw outputs | 输出有证据、状态、完成标记 |
| COLLECT_RESULTS | raw outputs | 汇总并检查缺项 | collection report | 缺失项进入 blocked-tasks |
| SPEC_REVIEW | 原始需求、输出 | 检查是否满足任务规格 | spec review | PASS 才能进质量审计 |
| QUALITY_REVIEW | spec-pass 输出 | 检查深度、准确性、可复用性 | quality review | APPROVED 才可晋升 |
| PROMOTION_DECISION | review 结果 | 判断沉淀位置 | promotion plan | 明确 curated/inbox/runtime/skill/backlog |
| WRITE_SHARED_MEMORY | promotion plan | 写入 shared | curated/project/fact/skill | 不含 secret，路径正确 |
| NOTIFY_USER | 审计后摘要 | 推送/输出完整流程摘要 | notification | 包含计划→执行→审计→结果→收获 |
| RETROSPECT_AND_ADJUST | 成败记录 | 更新权重、模板反馈、健康状态 | health/report/feedback | 可解释的调整记录 |

## 6. 学习组合策略

初始权重：

| 类别 | 权重 | 节奏 | 说明 |
|---|---:|---|---|
| github_growth_learning | 0.30 | 每日必做 | GitHub 增长项目、热门项目、源码机制学习 |
| books_and_long_term_theory | 0.20 | 每周/隔日 | 经典书籍、长期理论、底层知识体系 |
| tutorials_and_skill_training | 0.15 | 每周多次 | 高质量教程、工具链训练、实践路径 |
| problem_postmortem | 0.15 | 按需/每周 | 用户问题、系统失败、项目事故复盘 |
| industry_trends | 0.10 | 每日轻量 | AI/工程/产品趋势和资讯过滤 |
| system_self_improvement | 0.10 | 每日轻量 | 模板、agent 能力、共享中台、自动化改进 |

硬规则：GitHub 增长项目每日必做，但不是全部；系统每天至少保留一个非 GitHub 学习项，以避免认知单一化。

## 7. 多学习源 DAG 示例

### 7.1 GitHub 增长项目 DAG

```text
OpenClaw 趋势发现
  -> Hermes 初筛与任务定义
  -> Claude Code 源码/架构深读
  -> Hermes 审计与可复用模式提炼
  -> Obsidian/curated 沉淀 + 微信/终端摘要
```

输出：项目卡片、架构图、关键机制、可复用模式、风险与适用场景。

### 7.2 书籍章节学习 DAG

```text
Hermes 选择章节/主题
  -> Claude Code/专用阅读 agent 提炼结构
  -> Hermes 联系用户当前项目和问题
  -> 生成章节笔记、概念卡、行动建议
  -> 晋升到知识库或 backlog
```

输出：章节摘要、核心概念、反例、应用场景、待实践任务。

### 7.3 教程学习 DAG

```text
OpenClaw/检索 agent 找教程
  -> Hermes 过滤质量与时效
  -> Claude Code 复现实验或检查代码
  -> Hermes 生成最短实践路径
  -> 沉淀为 skill 或操作手册
```

输出：教程可信度、最短路径、坑点、可复制命令、是否适合升格 skill。

### 7.4 理论/论文学习 DAG

```text
检索/候选论文
  -> Hermes 定义阅读问题
  -> Claude Code/研究 agent 结构化阅读
  -> Hermes 做二次复核与类比解释
  -> 生成概念图、局限性、工程启发
```

输出：问题背景、方法、贡献、限制、可迁移实践。

### 7.5 问题复盘 DAG

```text
失败/bug/阻塞记录
  -> Hermes 归因分类
  -> Claude Code 深挖根因
  -> Hermes 提炼预防规则
  -> 更新模板、skill、checklist 或 blocked-tasks
```

输出：根因、证据、修复、预防规则、是否需要模板 patch。

## 8. 审计与晋升规则

### 8.1 Spec Review

检查输出是否满足任务规格：

- 是否覆盖 instruction 中所有必填字段。
- 是否有明确完成标记。
- 是否有证据路径、URL、命令输出或代码定位。
- 是否没有越权写入 curated。
- 是否没有把 runtime/cache/secret 写入长期记忆。

### 8.2 Quality Review

检查输出是否值得长期复用：

- 结论是否有证据。
- 是否足够具体，避免空泛总结。
- 是否能转化为行动、skill、项目规则或认知卡片。
- 是否指出不确定性和适用边界。
- 是否与用户目标相关。

### 8.3 晋升去向

| 内容类型 | 默认去向 | 晋升条件 |
|---|---|---|
| 原始执行记录 | inbox/<agent>/daily | 仅作为原始记录，不直接成为真相 |
| 临时状态/心跳/快照 | runtime/<agent> | 不晋升，除非总结为稳定事实 |
| 稳定事实 | curated/memory/facts | 经审计、有证据、跨 agent 可复用 |
| 项目状态 | curated/memory/projects | 会持续推进、有明确状态和下一步 |
| 操作流程 | capabilities/skills 或本地 skill | 复用价值高，能指导未来执行 |
| 待学习主题 | learning-backlog | 暂不学习但有价值 |

## 9. 防跑偏机制

新模型或低级模型接手前必须读取：

1. `shared/manifest.yaml`
2. `shared/AGENTS.md`
3. `shared/curated/memory/MEMORY.md`
4. `shared/curated/memory/projects/autonomous-learning-system.md`
5. `shared/runtime/hermes/autonomous-learning/implementation-plan.md`
6. 当前任务相关配置和 state 文件

接手必须先回答：

```text
当前系统目标是什么？
当前运行阶段是什么？
哪些文件是只读真相源？
哪些目录允许写 runtime？
当前任务输入是什么？
预期输出是什么？
完成标记是什么？
失败时写到哪里？
是否需要用户审批？
下一步最小动作是什么？
```

未能回答清楚，不允许执行写入或通知。

## 10. 故障转移与阻塞处理

每个任务必须有：

- primary_agent
- fallback_agent
- timeout_minutes
- max_retries
- blocked_output_path
- escalation_policy

默认策略：

```text
agent 超时/不可用
  -> 记录 agent-health
  -> 将任务写入 blocked-tasks
  -> 若有 fallback，降级执行
  -> 若无 fallback，等待 Hermes 重新规划或用户审批
```

失败不能静默吞掉，也不能把部分结果当成完整结果通知。

## 11. 人类审批闸门

以下操作需要用户审批或至少进入 pending-approval：

- 修改长期权重策略且影响每日计划。
- 升格新的 shared skill。
- 删除或覆盖 curated 真相源。
- 将失败模板改动推广到所有 agent。
- 对外发送长消息或高频消息。
- 执行有明显副作用的外部操作。

## 12. 健康度指标

每日/每周应统计：

- planned_tasks
- completed_tasks
- blocked_tasks
- audit_pass_rate
- promotion_count
- duplicate_rate
- stale_backlog_count
- agent_timeout_count
- user_value_score
- template_failure_count

健康报告只放 runtime；稳定趋势才可总结进 curated。

## 13. 通知格式要求

所有推送或长任务结果必须包含完整流程摘要：

```text
计划：今天原计划学什么/做什么
执行：哪些 agent 做了什么
审计：哪些通过、哪些失败、证据是什么
结果：沉淀到哪里，产物路径是什么
收获：对用户认知/项目/系统能力有什么帮助
下一步：明天或下一轮建议
```

禁止只说“详见知识库”。

## 14. 当前落地边界

v0.1 先做“可恢复、可审计、可配置”的骨架，不立即做完全自动执行：

- 先建立正式架构、implementation plan、关键 JSON 配置、模板骨架。
- 再做一次手动触发的 dry-run。
- dry-run 通过后，再考虑 cron 化或事件触发。
- 任何自动化上线前必须保留人工审批闸门和回滚快照。

## 15. 相关文件

- 架构跟踪 plan：`shared/runtime/hermes/autonomous-learning/architecture-design-plan.md`
- 实施 plan：`shared/runtime/hermes/autonomous-learning/implementation-plan.md`
- Agent 能力注册表：`shared/runtime/hermes/autonomous-learning/agent-capabilities.json`
- 学习权重：`shared/runtime/hermes/autonomous-learning/learning-weights.json`
- 学习 backlog：`shared/runtime/hermes/autonomous-learning/learning-backlog.json`
- 故障转移策略：`shared/runtime/hermes/autonomous-learning/failover-policy.json`
- Agent 健康状态：`shared/runtime/hermes/autonomous-learning/agent-health.json`
- 阻塞任务：`shared/runtime/hermes/autonomous-learning/blocked-tasks.json`
- 模板目录：`shared/runtime/hermes/autonomous-learning/templates/`
