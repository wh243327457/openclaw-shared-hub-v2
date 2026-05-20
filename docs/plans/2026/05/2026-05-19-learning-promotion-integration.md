# 2026-05-19 学习晋升建议系统集成计划

> 目标：把 2026-05-19 GitHub 热门项目学习日报里的晋升建议，从“推送里的明日建议”落到 shared hub / autonomous-learning 的可执行系统状态里。

## 当前阶段

- 阶段：第一轮落地完成，A 线 runtime 子计划已建，等待执行 POC
- 创建时间：`2026-05-19T12:30:00+08:00`
- 真相源：`shared/docs/plans/2026/05/2026-05-19-learning-promotion-integration.md`
- 关联日报：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-05-19-GitHub热门项目学习日报.md`

## 晋升输入

今日日报提到的可迁移范式：

1. Agent 要靠显式记忆长期成长。
2. 工具链替换要先兼容旧入口。
3. 本地模型/本地工具能力要封装成简单入口。
4. agent 输出面可以从 Markdown 扩展到 HTML / 多 surface。
5. 跨数据源访问可先建统一抽象层，再逐个挂载。

## 集成原则

- 不复制外部项目源码，只沉淀机制与系统改造步骤。
- runtime 先承载实验与状态，curated 只写稳定事实/项目状态。
- Hermes 做总控与审计；执行型 POC 后续再交给 Claude Code / OpenClaw。
- shared skill 升格前必须先经过可复用性判断与验证。

## 步骤状态

| Step | 状态 | 动作 | 产物 | 验收 |
|---|---|---|---|---|
| 1 | ✅ 已完成 | 建立本计划 | 本文件 | 计划可被后续 agent 接手 |
| 2 | ✅ 已完成 | 把“兼容旧入口优先”沉淀为稳定工程事实 | `curated/memory/facts/toolchain-migration-compat-first.md` | 有来源、适用场景、边界 |
| 3 | ✅ 已完成 | 更新 autonomous-learning 项目状态 | `curated/memory/projects/autonomous-learning-system.md` | 新增 2026-05-19 集成章节 |
| 4 | ✅ 已完成 | 把下一轮学习主题写入 backlog | `runtime/hermes/autonomous-learning/learning-backlog.json` | JSON 可解析，含 owner/next_action |
| 5 | ✅ 已完成 | 建立 runtime 执行状态 | `runtime/hermes/autonomous-learning/promotion-integration/2026-05-19-state.json` | JSON 可解析 |
| 6 | ✅ 已完成 | 写入 Hermes 原始记录 | `inbox/hermes/daily/2026-05-19.md` | 原始记录不冒充 curated 真相 |
| 7 | ✅ 已完成 | 跑 promoter / verify 收口 | `promoter.py`、`verify_bridge.py` 输出 | `verify.ok == true`；仅剩 3 条历史 fact metadata warning，与本轮新增无关 |
| 8 | ✅ 已完成 | 建立 A 线 runtime 子计划 | `runtime/hermes/autonomous-learning/agent-memory-skill-evolution/2026-05-19-plan.md` | 子计划可恢复、可继续分派 |

## 后续迭代队列

### A. Agent 记忆 / skill 自进化

- 下一动作：先走 runtime 子计划，收窄 source scope，再发 Claude Code bounded deep read。
- 目标产物：`runtime/hermes/autonomous-learning/agent-memory-skill-evolution/2026-05-19-claude-output.md`
- 晋升门槛：能形成稳定流程、能降低重复提醒、可转成 shared skill 或模板 patch。

### A.1 runtime 子计划

- `runtime/hermes/autonomous-learning/agent-memory-skill-evolution/2026-05-19-plan.md`
- `runtime/hermes/autonomous-learning/agent-memory-skill-evolution/2026-05-19-state.json`
- `runtime/hermes/autonomous-learning/agent-memory-skill-evolution/2026-05-19-source-scope.md`

### B. 工具链迁移 / 兼容旧入口

- 下一动作：对 shared hub 自身做一次“兼容入口清单”审计，确认 legacy 入口仍可用，同时新写入走 canonical。
- 目标产物：兼容入口检查报告 + 必须项清单。
- 晋升门槛：发现可复用迁移规则时再扩展 shared skill。

### C. html-anything 输出面实验

- 下一动作：先做 runtime-only HTML 推送模板 POC，不改现有微信日报正式格式。
- 目标产物：`runtime/hermes/autonomous-learning/html-surface-poc/`
- 晋升门槛：微信/Obsidian 两端可读性明显提升，且不增加推送失败率。

### D. mirage 虚拟文件系统观察

- 下一动作：先做设计评估，不直接接入 OAuth / 外部账号。
- 目标产物：shared hub “多数据源挂载层”候选设计。
- 晋升门槛：能证明比现有 file/search/session_search 更省心。

## 验证命令

```bash
cd /home/vany/agent/shared
python3 -m json.tool runtime/hermes/autonomous-learning/learning-backlog.json >/dev/null
python3 -m json.tool runtime/hermes/autonomous-learning/promotion-integration/2026-05-19-state.json >/dev/null
python3 scripts/promoter.py --dry-run
python3 scripts/promoter.py
python3 scripts/verify_bridge.py
```
