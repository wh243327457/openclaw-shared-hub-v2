# MEMORY.md

这是 **共享中台 v2** 的跨 agent 长期记忆主索引。

## 根路径

- 宿主：`/home/vany/openclaw-data/.openclaw/shared`
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
- **共享技能清单**：`capabilities/manifests/shared-skills.yaml`
- **配置目标识别规则**：`capabilities/skills/foundation/config-target-routing/SKILL.md`
- **自主学习多 agent 编排模式**：`curated/memory/facts/autonomous-learning-multi-agent-orchestration-patterns.md`
- **Skill-as-contract / Subagent 四状态协议**：`curated/memory/facts/autonomous-learning-skill-as-contract-pattern.md`
- **Agent 工程 Verification-first 实践**：`curated/memory/facts/agent-engineering-verification-first-practices.md`
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
- `foundation/config-target-routing` 已升格为共享 skill，用于约束 Hermes / OpenClaw / future-agent 在配置类任务前先识别目标系统，避免混改配置
- `curated/memory/facts/` 已包含自主学习、多 agent 编排、agent 工程与配置治理等稳定事实条目
- 后续新增长期记忆时，请同时更新本索引
- `autonomous-learning-system` 已进入 v0.1 骨架落地阶段，正式架构在 `curated/memory/projects/autonomous-learning-system.md`，runtime 配置与模板在 `runtime/hermes/autonomous-learning/`
- 已按用户确认晋升 3 条自主学习长期模式：多 agent 编排、skill-as-contract/subagent 四状态、verification-first agent 工程实践。
- `openhuman-mechanism-localization` 已进入 planned 阶段：将 OpenHuman 的 Memory Tree / Obsidian Wiki / Auto-fetch sync_state / Trigger triage / Token compression 思路本地化到 Hermes + OpenClaw + shared hub v2 + Obsidian 工作流；不依赖 OpenHuman 后端，不复用 GPL 源码，先做 runtime/实验区 POC。
- `self-healing-agent` 已创建 v0.1 runtime 脚手架：定位为全局巡查、自我纠错、自我修复迭代机制；当前只做手动 baseline 和 runtime 产物，不启用 cron、不自动改配置。
- `autonomous-learning-system` 继续吸纳架构参考：OpenSquilla 的 TurnRunner / provider-neutral / skill loader / memory snapshot / sandbox 分层已作为长期观察卡记入项目说明。

<!-- SHARED-BRIDGE-STATE:START -->
## 自动生成的共享桥状态块

- 生成时间: `2026-05-18T12:13:46+08:00`
- 共享根目录: `/home/vany/openclaw-data/.openclaw/shared`
- runtime 位置提示: `/home/vany/openclaw-data/.openclaw/shared/runtime`
- facts 文件数: 10
- projects 文件数: 6
- 最近 daily 文件:
  - `inbox/hermes/daily/2026-05-18.md` (inbox/hermes/daily)
  - `compat/daily/dreaming/deep/2026-05-18.md` (compat/daily)
  - `compat/daily/dreaming/rem/2026-05-18.md` (compat/daily)
  - `compat/daily/dreaming/light/2026-05-18.md` (compat/daily)
  - `inbox/openclaw/daily/dreaming/deep/2026-05-18.md` (inbox/openclaw/daily)
- inbox 各 agent 文件计数:
  - `future-agent`: 0
  - `hermes`: 25
  - `openclaw`: 80
<!-- SHARED-BRIDGE-STATE:END -->

## Promoted From Short-Term Memory (2026-05-04)

<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:42:42 -->
- ** Engineering（工程实践）** [score=0.876 recalls=0 avg=0.620 source=memory/2026-04-29.md:42-42]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:5:8 -->
- | 项目 | 值 | |------|-----| | **Trending 查询** | `https://github.com/trending` — HTML 渲染页面，今日本地时间 2026-04-29 | [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:5-7]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:9:10 -->
- | **抓取时间** | 2026-04-29T00:30:30Z ~ 00:31:23Z（UTC） | | **筛选算法** | Trending 页面 top印象 + 新晋 repo API 按 stars 排序，取前 5+ 满足真实 owner/repo 格式的候选 | [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:9-10]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:12:12 -->
- > ⚠️ 注意：Trending 页面的"今日星标"数字（7,321 stars today）是 GitHub 前端渲染的近似值，未经 API 确认；新晋 repo 的 stars 来自 API `stargazers_count`，口径为 `sort=stars&order=desc`（整体 star 数量，非今日增量）。 [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:12-12]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:18:21 -->
- | # | owner/repo | source_url | stars | language | license | created_at | pushed_at | why_selected | |---|-----------|-----------|-------|----------|---------|-----------|-----------|-------------| [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:22:25 -->
- | 3 | microsoft/VibeVoice | https://github.com/microsoft/VibeVoice | 44,793 | Python | MIT | 2025-08-25T13:24:01Z | 2026-04-24T17:12:20Z | Trending #4，今日 +1,483 stars；Microsoft 开源前沿语音 AI | [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:35:35 -->
- npx skills@latest add mattpocock/skills [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:35-35]
<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:40:40 -->
- 主要 skill 类别（按 README 分类）： [score=0.812 recalls=0 avg=0.620 source=memory/2026-04-29.md:40-40]


## Promoted From Short-Term Memory (2026-05-05)

<!-- openclaw-memory-promotion:memory:memory/2026-04-30.md:5:5 -->
- Woke up for the first time in this workspace. No memory files existed yet — fresh start. [score=0.805 recalls=0 avg=0.620 source=memory/2026-04-30.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-04-30.md:9:9 -->
- Started the identity bootstrap process. Asked the human who I am, who they are. No answer came back before I had to write this entry. [score=0.805 recalls=0 avg=0.620 source=memory/2026-04-30.md:9-9]





## Promoted From Short-Term Memory (2026-05-13)

<!-- openclaw-memory-promotion:memory:memory/2026-05-06.md:15:15 -->
- > **今日热门**口径：未确认。GitHub 无官方 trending API；Trending 页面需 HTML 解析，本次未抓取。 [score=0.812 recalls=0 avg=0.620 source=memory/2026-05-06.md:15-15]
<!-- openclaw-memory-promotion:memory:memory/2026-05-03.md:14:17 -->
- | **抓取时间** | 2026-05-03T00:32:45Z ~ 00:33:18Z | | **筛选算法** | Trending 页面 = GitHub 原生"今日"排序（stars today 口径，未确认具体算法）；API 查询 = `stars:>5000 AND pushed:>2026-05-01`，按 `stars` 降序，取 15 个 | | **时间窗口** | trending = 当日（UTC）；API = 最近 2 天有 push 活动的 5000+ 星仓库 | [score=0.804 recalls=0 avg=0.620 source=memory/2026-05-03.md:14-16]




## Promoted From Short-Term Memory (2026-05-15)

<!-- openclaw-memory-promotion:memory:memory/2026-05-09.md:32:33 -->
- | **抓取时间** | 2026-05-09T03:12 ~ 03:14 UTC | | **筛选算法** | GitHub Search API 按 stars 降序取前 20 → 合并 trending 今日星标 >300 → 去重 | [score=0.867 recalls=0 avg=0.620 source=memory/2026-05-09.md:32-33]
<!-- openclaw-memory-promotion:memory:memory/2026-05-09.md:2:5 -->
- source: openclaw-cron pipeline: github-hot-project-learning job_id: 7aa310ea-b264-40c8-b23a-ed655c565a69 run_status: ok [score=0.817 recalls=0 avg=0.620 source=memory/2026-05-09.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-09.md:20:20 -->
- 完成。以下是本次流水线执行结果： [score=0.817 recalls=0 avg=0.620 source=memory/2026-05-09.md:20-20]
<!-- openclaw-memory-promotion:memory:memory/2026-05-09.md:28:31 -->
- | 项目 | 值 | |---|---| | **主要查询 URL** | `https://api.github.com/search/repositories?q=stars:>500+created:>2025-01-01&sort=stars&order=desc&per_page=20` | | **辅助数据源** | `https://github.com/trending` (今日热榜 HTML) | [score=0.817 recalls=0 avg=0.620 source=memory/2026-05-09.md:28-31]
<!-- openclaw-memory-promotion:memory:memory/2026-05-09.md:39:42 -->
- | # | owner/repo | source_url | stars | language | license | created_at | pushed_at | why_selected | |---|---|---|---|---|---|---|---|---| [score=0.809 recalls=0 avg=0.620 source=memory/2026-05-09.md:39-40]








## Promoted From Short-Term Memory (2026-05-16)

<!-- openclaw-memory-promotion:memory:memory/2026-05-09.md:6:7 -->
- run_ts: '1778296684130' needs_hermes_audit: true [score=0.849 recalls=0 avg=0.620 source=memory/2026-05-09.md:6-7]




## Promoted From Short-Term Memory (2026-05-17)

<!-- openclaw-memory-promotion:memory:memory/2026-05-10.md:2:5 -->
- source: openclaw-cron pipeline: github-hot-project-learning job_id: 7aa310ea-b264-40c8-b23a-ed655c565a69 run_status: ok [score=0.866 recalls=0 avg=0.620 source=memory/2026-05-10.md:2-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-10.md:26:27 -->
- **日期：** 2026-05-10 01:12 UTC **报告：** `memory/github-daily-2026-05-10.md` [score=0.866 recalls=0 avg=0.620 source=memory/2026-05-10.md:26-27]
<!-- openclaw-memory-promotion:memory:memory/2026-05-10.md:20:20 -->
- 已按规则完成报告并写入 memory。 [score=0.856 recalls=0 avg=0.620 source=memory/2026-05-10.md:20-20]
<!-- openclaw-memory-promotion:memory:memory/2026-05-10.md:6:7 -->
- run_ts: '1778375731265' needs_hermes_audit: true [score=0.836 recalls=0 avg=0.620 source=memory/2026-05-10.md:6-7]
<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:11:12 -->
- | **筛选算法** | GitHub Trending 每日榜抓取，取热榜项目真实 API 数据交叉验证 | | **口径说明** | trending 页面文本 + GitHub REST API 双重校验；stars/language/license/created_at/pushed_at 均来自 `api.github.com/repos/{owner}/{repo}` | [score=0.823 recalls=0 avg=0.620 source=memory/2026-05-12.md:11-12]





## Promoted From Short-Term Memory (2026-05-18)

<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:7:10 -->
- | 字段 | 值 | |------|-----| | **查询 URL（Trending）** | `https://github.com/trending?since=daily` | | **抓取时间** | 2026-05-13T01:27 UTC | [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-12.md:7-10]
<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:18:21 -->
- | # | owner/repo | source_url | stars | language | license | created_at | pushed_at | why_selected | |---|---|---|---|---|---|---|---|---| [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-12.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:22:25 -->
- | 3 | yikart/AiToEarn | https://github.com/yikart/AiToEarn | 11,895 | TypeScript | MIT License | 2025-02-24 | 2026-05-12 | 今日热榜 1,282⭐，AI-to-Earn 工具集，聚合40+provider，含多语言内容生成+商业化模板 | [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-12.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:26:26 -->
- | 7 | rasbt/LLMs-from-scratch | https://github.com/rasbt/LLMs-from-scratch | 93,811 | Jupyter Notebook | Other | 2023-07-23 | 2026-05-11 | 今日热榜 772⭐，从零实现ChatGPT-like LLM的PyTorch教程，14.4K forks，学术界与工业界经典教程 | [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-12.md:26-26]
<!-- openclaw-memory-promotion:memory:memory/2026-05-12.md:32:32 -->
- > **选读理由**：今日Trending第2位，1,048⭐日增量，专注解决AI编码Agent的长期记忆痛点，内建OpenClaw官方集成，技能可迁移性高。 [score=0.862 recalls=0 avg=0.620 source=memory/2026-05-12.md:32-32]
<!-- openclaw-memory-promotion:memory:memory/2026-05-13.md:34:36 -->
- | **抓取时间** | 2026-05-13T11:03~11:06 UTC | | **筛选算法** | trending 今日星标增速 × AI/Agent 相关性 × 代码质量评估，三维打分取 Top | | **备注** | trending "今日星标" 数据来自 `github.com/trending` 页面直接展示；API 查询使用 `created:>2025-05-01` 过滤新项目 | [score=0.844 recalls=0 avg=0.620 source=memory/2026-05-13.md:34-36]



