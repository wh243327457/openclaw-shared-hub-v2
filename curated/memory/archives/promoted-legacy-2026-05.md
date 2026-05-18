# Promoted legacy archive — 2026-05

本文件从 `curated/memory/MEMORY.md` 迁出旧的自动 promoted 明细，保留历史可追溯性。

- 迁出日期：2026-05-18
- 来源：`curated/memory/MEMORY.md` 中的 `Promoted From Short-Term Memory` 历史块
- 原因：主索引应回归入口索引 + 当前状态块；score/source/raw 摘要不应长期堆在主索引。
- 处理原则：本文件仅归档，不作为新的真相源；稳定事实应进入 `curated/memory/facts/` 或 `curated/memory/projects/`。

---

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
