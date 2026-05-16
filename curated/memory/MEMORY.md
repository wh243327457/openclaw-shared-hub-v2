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
- **共享技能清单**：`capabilities/manifests/shared-skills.yaml`
- **配置目标识别规则**：`capabilities/skills/foundation/config-target-routing/SKILL.md`
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
- `curated/memory/facts/` 目前仍为空，后续可按需补充稳定事实条目
- 后续新增长期记忆时，请同时更新本索引
- `autonomous-learning-system` 已进入 v0.1 骨架落地阶段，正式架构在 `curated/memory/projects/autonomous-learning-system.md`，runtime 配置与模板在 `runtime/hermes/autonomous-learning/`

<!-- SHARED-BRIDGE-STATE:START -->
## 自动生成的共享桥状态块

- 生成时间: `2026-05-16T10:53:15+08:00`
- 共享根目录: `/home/vany/openclaw-data/.openclaw/shared`
- runtime 位置提示: `/home/vany/openclaw-data/.openclaw/shared/runtime`
- facts 文件数: 6
- projects 文件数: 3
- 最近 daily 文件:
  - `inbox/hermes/daily/2026-05-16.md` (inbox/hermes/daily)
  - `inbox/openclaw/daily/2026-05-16.md` (inbox/openclaw/daily)
  - `inbox/openclaw/daily/2026-05-15.md` (inbox/openclaw/daily)
  - `inbox/hermes/daily/2026-05-15.md` (inbox/hermes/daily)
  - `compat/daily/dreaming/deep/2026-05-15.md` (compat/daily)
- inbox 各 agent 文件计数:
  - `future-agent`: 0
  - `hermes`: 23
  - `openclaw`: 68
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







