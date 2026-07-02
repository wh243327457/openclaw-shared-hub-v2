# MEMORY.md

这是 **共享中台 v2** 的跨 agent 长期记忆主索引。

## 根路径

- 宿主：`/home/vany/agent/shared`
- 容器：`/home/node/.openclaw/shared`

## 作用范围

`curated/memory/` 是 **跨 agent 真相源**，只保留稳定、重要、后续大概率还会复用的信息。

- 事实片段：`curated/memory/facts/`
- 项目状态：`curated/memory/projects/`
- 兼容入口：`shared/memory/MEMORY.md`（symlink 到本文件）

## 目录索引

- **长期记忆主索引**：`curated/memory/MEMORY.md`
- **稳定事实**：`curated/memory/facts/`
- **项目状态目录**：`curated/memory/projects/`
- **当前项目条目**：`curated/memory/projects/shared-hub-v2.md`
- **自主学习系统**：`curated/memory/projects/autonomous-learning-system.md`
- **OpenHuman 机制本地化**：`curated/memory/projects/openhuman-mechanism-localization.md`
- **OpenClaw 网页/公众号采集系统**：`curated/memory/projects/openclaw-web-watch.md`
- **Self-Healing Agent / 全局巡查自我修复**：`curated/memory/projects/self-healing-agent.md`
- **Elephant Agent 机制研究与 shared hub v2 反哺**：`curated/memory/projects/elephant-agent-mechanism-study.md`
- **共享技能清单**：`capabilities/manifests/shared-skills.yaml`
- **治理总结标准**：`docs/shared-governance-standard.md`
- **治理总结机制**：`docs/governance-summary-mechanism.md`
- **配置目标识别规则**：`capabilities/skills/foundation/config-target-routing/SKILL.md`
- **自主学习多 agent 编排模式**：`curated/memory/facts/autonomous-learning-multi-agent-orchestration-patterns.md`
- **Skill-as-contract / Subagent 四状态协议**：`curated/memory/facts/autonomous-learning-skill-as-contract-pattern.md`
- **Agent 工程 Verification-first 实践**：`curated/memory/facts/agent-engineering-verification-first-practices.md`
- **工具链迁移兼容优先原则**：`curated/memory/facts/toolchain-migration-compat-first.md`
- **ds4 推理优化长期事实**：`curated/memory/facts/autonomous-learning-ds4-inference-patterns.md`
- **旧 OpenClaw daily 兼容视图**：`compat/daily/`（可通过 `memory/daily/` 访问）
- **agent 原始写入**：`inbox/<agent>/daily/`
- **运行时产物**：`runtime/<agent>/`

## 写入规则

- 只有经过整理和验证的长期信息才进入 `curated/memory/`
- agent 原始记录默认进入 `inbox/<agent>/daily/`
- `.dreams`、cache、index、临时摘要等运行时产物进入 `runtime/<agent>/`
- 避免在本文件中写入明文 secret

## 当前状态

- `shared-hub-v2` 项目状态已沉淀到 `curated/memory/projects/shared-hub-v2.md`
- `capabilities/manifests/shared-skills.yaml` 已建立，用于声明常驻 shared 的共享技能
- `docs/shared-governance-standard.md` 已建立，作为 shared hub 长期筛选、总结、晋升、压缩、淘汰的强制执行标准
- `docs/governance-summary-mechanism.md` 已建立，作为 shared hub 治理总结机制说明入口
- `foundation/config-target-routing` 已升格为共享 skill，用于约束 Hermes / OpenClaw / future-agent 在配置类任务前先识别目标系统，避免混改配置
- `curated/memory/facts/` 已包含自主学习、多 agent 编排、agent 工程与配置治理等稳定事实条目
- 后续新增长期记忆时，请同时更新本索引
- `autonomous-learning-system` 已进入 v0.1 骨架落地阶段，正式架构在 `curated/memory/projects/autonomous-learning-system.md`，runtime 配置与模板在 `runtime/hermes/autonomous-learning/`
- 已按用户确认晋升 3 条自主学习长期模式：多 agent 编排、skill-as-contract/subagent 四状态、verification-first agent 工程实践。
- `openhuman-mechanism-localization` 已进入 planned 阶段：将 OpenHuman 的 Memory Tree / Obsidian Wiki / Auto-fetch sync_state / Trigger triage / Token compression 思路本地化到 Hermes + OpenClaw + shared hub v2 + Obsidian 工作流；不依赖 OpenHuman 后端，不复用 GPL 源码，先做 runtime/实验区 POC。
- `self-healing-agent` 已创建 v0.1 runtime 脚手架：定位为全局巡查、自我纠错、自我修复迭代机制；当前只做手动 baseline 和 runtime 产物，不启用 cron、不自动改配置。
- `autonomous-learning-system` 继续吸纳架构参考：OpenSquilla 的 TurnRunner / provider-neutral / skill loader / memory snapshot / sandbox 分层已作为长期观察卡记入项目说明。
- `autonomous-learning-system` 已开始集成 2026-05-19 晋升建议：兼容旧入口优先、本地工具简单入口、HTML 输出面 POC、多数据源统一抽象进入 backlog。

<!-- SHARED-BRIDGE-STATE:START -->
## 自动生成的共享桥状态块

- 生成时间: `2026-07-03T06:00:10+08:00`
- 共享根目录: `/home/vany/agent/shared`
- runtime 位置提示: `/home/vany/agent/shared/runtime`
- facts 文件数: 26
- projects 文件数: 11
- 最近 daily 文件:
  - `inbox/hermes/daily/2026-07-02.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-07-02-tutorial-learning.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-07-01.md` (inbox/hermes/daily)
  - `inbox/hermes/daily/2026-06-26.md` (inbox/hermes/daily)
  - `inbox/openclaw/daily/2026-06-26.md` (inbox/openclaw/daily)
- inbox 各 agent 文件计数:
  - `future-agent`: 0
  - `hermes`: 62
  - `openclaw`: 78
<!-- SHARED-BRIDGE-STATE:END -->

## 历史 promoted 归档

- 旧自动 promoted 明细已迁出：`curated/memory/archives/promoted-legacy-2026-05.md`
- 主索引只保留稳定入口和当前状态；长期事实请沉淀到 `facts/` 或 `projects/`。



## Promoted From Short-Term Memory (2026-05-19)

<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:30:33 -->
- | 项目 | 值 | |------|---| | **主要来源** | `https://github.com/trending` — 今日所有语言 | | **补充来源** | `https://api.github.com/search/repositories?q=stars:>1000+created:>2025-05-01&sort=stars` | [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-13.md:30-33]
<!-- openclaw-memory-promotion:memory:memory/2026-05-14.md:3:4 -->
- > 数据来源: GitHub API，查询时间 2026-05-14T23:35 UTC > 说明: 实际执行日期为 2026-05-14（cron 调度时使用 2026-05-14 作为日期标签） [score=0.868 recalls=0 avg=0.620 source=memory/2026-05-14.md:3-4]
<!-- openclaw-memory-promotion:memory:memory/2026-05-14.md:8:8 -->
- 深读了两个 AI 基础设施项目（ollama 本地 LLM 运行平台、everything-claude-code AI Agent 优化系统）和一个工作流自动化平台（n8n），提炼出 3 条可复用工程经验，并设计了 1 个可尝试的实验。 [score=0.868 recalls=0 avg=0.620 source=memory/2026-05-14.md:8-8]
<!-- openclaw-memory-promotion:memory:memory/2026-05-14.md:12:15 -->
- | 项目 | Stars | Forks | 语言 | 描述 | |------|-------|-------|------|------| | openclaw/openclaw | 371,883 | 76,985 | TypeScript | OpenClaw AI 助手主仓库 | | public-apis/public-apis | 435,034 | 47,667 | Python | 免费 API 集合列表 | [score=0.868 recalls=0 avg=0.620 source=memory/2026-05-14.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-05-14.md:16:19 -->
- | sindresorhus/awesome | 466,375 | 34,974 | - | 各类优质主题列表合集 | | freeCodeCamp/freeCodeCamp | 444,736 | 44,565 | TypeScript | 免费编程学习平台 | | EbookFoundation/free-programming-books | 388,301 | 66,300 | Python | 免费编程书籍列表 | [score=0.868 recalls=0 avg=0.620 source=memory/2026-05-14.md:16-18]
<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:2:5 -->
- source: openclaw-cron pipeline: github-hot-project-learning job_id: 7aa310ea-b264-40c8-b23a-ed655c565a69 run_status: ok [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-13.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:20:20 -->
- 现在我已经获取了足够的结构化数据，以下是完整的流水线输出： [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-13.md:20-20]






## Promoted From Short-Term Memory (2026-05-20)

<!-- openclaw-memory-promotion:memory:memory/2026-05-14.md:20:23 -->
- | n8n-io/n8n | 187,864 | 57,628 | TypeScript | 流程自动化平台（含 AI） | | everything-claude-code/affaan-m | 182,217 | 28,071 | JavaScript | AI Agent 性能优化系统 | | ollama/ollama | 171,404 | 16,117 | Go | 本地 LLM 运行平台 | [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-14.md:20-22]
<!-- openclaw-memory-promotion:memory:memory/2026-05-14.md:24:27 -->
- | Significant-Gravitas/AutoGPT | 184,302 | 46,234 | Python | AI Agent 框架 | | avelino/awesome-go | 172,658 | 13,208 | Go | Go 语言优质资源列表 | | rustdesk/rustdesk | 114,194 | 17,155 | Rust | 开源远程桌面 | | denoland/deno | 106,696 | 6,058 | Rust | 现代 JS/TS 运行时 | [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-14.md:24-27]
<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:6:7 -->
- run_ts: '1778670620846' needs_hermes_audit: true [score=0.860 recalls=0 avg=0.620 source=memory/2026-05-13.md:6-7]



## Promoted From Short-Term Memory (2026-05-21)

<!-- openclaw-memory-promotion:memory:memory/2026-05-15.md:2:5 -->
- source: openclaw-cron pipeline: github-hot-project-learning job_id: 7aa310ea-b264-40c8-b23a-ed655c565a69 run_status: ok [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-15.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-15.md:20:20 -->
- ✅ **今日学习完成** [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-15.md:20-20]
<!-- openclaw-memory-promotion:memory:memory/2026-05-15.md:26:29 -->
- | 文件 | 状态 | 说明 | |------|------|------| | `shared/inbox/openclaw/daily/2026-05-15.md` | ✅ 170行 | 完整日报，含5个章节 | | `shared/runtime/openclaw/github-learning/projects/rohitg00-agentmemory.md` | ✅ | 项目卡片 | [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-15.md:26-29]
<!-- openclaw-memory-promotion:memory:memory/2026-05-15.md:6:7 -->
- run_ts: '1778805284053' needs_hermes_audit: true [score=0.832 recalls=0 avg=0.620 source=memory/2026-05-15.md:6-7]
<!-- openclaw-memory-promotion:memory:memory/2026-05-15.md:22:22 -->
- 已按指令完成所有产出： [score=0.812 recalls=0 avg=0.620 source=memory/2026-05-15.md:22-22]




## Promoted From Short-Term Memory (2026-05-22)

<!-- openclaw-memory-promotion:memory:memory/2026-05-16.md:2:5 -->
- source: openclaw-cron pipeline: github-hot-project-learning job_id: 7aa310ea-b264-40c8-b23a-ed655c565a69 run_status: ok [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-16.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-16.md:20:20 -->
- 已完成今日 GitHub 热门项目学习，产出文件如下： [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-16.md:20-20]
<!-- openclaw-memory-promotion:memory:memory/2026-05-16.md:22:22 -->
- **✅ 已完成产出** [score=0.842 recalls=0 avg=0.620 source=memory/2026-05-16.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-05-16.md:6:7 -->
- run_ts: '1778891706299' needs_hermes_audit: true [score=0.832 recalls=0 avg=0.620 source=memory/2026-05-16.md:6-7]

## Promoted From Pending Queue (2026-06-04)

- **opensquilla-agent-runtime-architecture**: Hermes 竞品 OpenSquilla 的微内核架构分析，含 ML 模型路由、Dream 记忆压缩、per-session 锁。→ `facts/opensquilla-agent-runtime-architecture.md`
- **anthropic-multi-agent-engineering**: Anthropic 多 agent 研究系统工程实践，token 用量 15x 换质量，验证 orchestrator-worker 模式。→ `facts/anthropic-multi-agent-engineering.md`
- **antirez-ds4-local-inference**: antirez 的 ds4 本地推理引擎，Disk KV Cache 跨 session 复用 + 不对称 MoE 量化。→ `facts/antirez-ds4-local-inference.md`
- **claude-code-engineering-practices**: Claude Code 工程模式：验证优先、权限先于自主权、project rules 作为可执行上下文。→ `facts/claude-code-engineering-practices.md`






































