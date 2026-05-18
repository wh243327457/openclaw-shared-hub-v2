---
type: plan
status: validated
created: 2026-04-28
updated: 2026-04-29
domain: ai-agent-learning
tags: [github, openclaw, hermes, daily-learning, shared-hub]
related:
  - "[[GitHub 热门项目学习档案/00-总览索引]]"
---

# GitHub 热门项目学习流水线实施计划

> 目标：让 OpenClaw 每日学习 GitHub 热门项目，产出项目卡片、经验规则、可复用 skill 草案；Hermes 负责质量审计和升格判断；最终沉淀到 Obsidian 知识库，并形成每日推送内容。

> 2026-04-29 收口状态：OpenClaw 提示词已收紧并二次 run 通过；Hermes 已配置每日审计与微信推送链路。微信侧重新绑定后，`getupdates`、最小测试消息、GitHub 学习摘要手动推送均验证成功；后续进入每日稳定性观察。

## 1. 分工

| 角色 | 职责 | 产物 |
|---|---|---|
| OpenClaw | 抓取候选项目、阅读 README/docs/examples、生成初版学习总结 | 原始日报、项目卡片草稿、skill 草案 |
| Hermes | 审计事实、结构、复用价值、安全与许可证，决定是否通过或返工 | 审计报告、升格建议、知识库最终稿 |
| shared hub | 保存跨 agent 规则、skill、运行状态 | shared skill、计划、运行日志 |
| Obsidian 知识库 | 保存长期学习资产 | 总览索引、每日学习、项目卡片、质量审计 |

## 2. 每日流水线

1. 候选发现
   - GitHub Trending：按日维度获取热门项目。
   - GitHub Search API：补充 `stars:>500 pushed:>YYYY-MM-DD`、topic/language 条件。
   - GitHub Releases：优先关注近期发布重大版本的项目。
   - 技术社区信号：Hacker News、Reddit、X/博客只作为补充，不作为唯一依据。

2. 候选筛选
   - 硬门槛：有 license、README 不为空、最近 30 天有活动、不是纯 awesome 列表、不是明显营销页。
   - 学习价值：能解释一个技术趋势、架构模式、工程实践或工具链变化。
   - 复用价值：能转成经验、规则、模板、skill 或可运行实验。

3. OpenClaw 初学
   - 对 Top 3 深读：README、docs、examples、核心目录、release、issues。
   - 对 Top 10 速览：一句话用途、技术栈、为什么火、是否值得深读。
   - 每个项目必须保留引用来源和原仓库链接。

4. Hermes 审计
   - 检查事实是否可追溯到链接。
   - 检查是否有“学到了什么”和“下次怎么用”。
   - 检查是否误把宣传语当结论。
   - 检查许可证、安全风险、不可复现结论。
   - 对不合格产物给出返工问题清单，再让 OpenClaw 重跑。

5. 落盘与推送
   - 通过审计的内容落入 Obsidian：`03-学习/技术实践/GitHub 热门项目学习档案/`。
   - 跨 agent 复用流程沉淀到 shared skill：`shared/capabilities/skills/research/github-hot-project-learning/`。
   - 每日推送只发“今日学到什么、值得深读什么、沉淀了什么能力、明天继续什么”。

## 3. 筛选评分

总分 100，低于 70 不深读。

| 维度 | 权重 | 通过标准 |
|---|---:|---|
| 热度真实性 | 20 | star/fork/watch 增长与讨论来源一致，不是单点刷量 |
| 工程活跃度 | 20 | 最近 30 天有 commit/release/issue 互动 |
| 文档可读性 | 15 | README 能说明用途、安装、示例、边界 |
| 学习新意 | 20 | 能提供新模式、新工具链、新工程经验 |
| 可复用性 | 15 | 能转成规则、模板、skill 或实践 checklist |
| 安全与合规 | 10 | license 清晰，无明显恶意/侵权/危险指令 |

## 4. 质量审计 Rubric

每份 OpenClaw 初稿必须按 0-2 分评分，总分 20，低于 16 返工。

| 项 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| 来源完整 | 无链接 | 只有仓库链接 | 仓库、README/docs/release/issue 链接齐全 |
| 事实准确 | 明显臆测 | 大体正确但缺引用 | 关键事实可追溯 |
| 中心判断 | 只有摘要 | 有判断但泛 | 明确说明为什么值得学 |
| 技术深度 | 只讲用途 | 提到架构/模块 | 讲清实现思路和边界 |
| 可复用动作 | 无 | 有建议但不可执行 | 有条件-动作规则或 checklist |
| 安全合规 | 未检查 | 简单提 license | 明确 license、安全、数据风险 |
| 反宣传能力 | 照抄 slogan | 有少量辨别 | 能指出局限和不适用场景 |
| Obsidian 结构 | 无 frontmatter | frontmatter 不完整 | 符合知识库规范 |
| Skill 升格判断 | 乱升格 | 有草案但边界不清 | 明确是否升格及原因 |
| 每日推送质量 | 冗长流水账 | 有摘要 | 3-5 条高密度行动信息 |

## 5. 目录结构

```text
03-学习/技术实践/GitHub 热门项目学习档案/
├── 00-总览索引.md
├── 每日学习/
│   └── 2026-04-28-GitHub热门项目学习日报.md
├── 项目卡片/
│   └── owner-repo.md
└── 质量审计/
    └── 2026-04-28-质量审计.md
```

## 6. 最小闭环验收标准

- [x] OpenClaw agent 能用 `minimax/MiniMax-M2.7` 返回正常文本。
- [x] 能生成至少 1 份项目学习卡片/日报。
- [x] Hermes 完成审计并给出通过/返工判断。
- [x] 知识库中存在总览索引、日报、审计报告；项目卡片目录已预留。
- [x] shared skill manifest 已登记 `research/github-hot-project-learning`。
- [x] OpenClaw cron 中存在每日学习任务，且已手动 run 两次，状态 `ok`。
- [x] OpenClaw 提示词已收紧，必填 `source_url`、抓取口径、时间窗口、`owner/repo`、`created_at`、`pushed_at`、`license`、`stars`。
- [x] Hermes cron 已创建：`2a82c752d86a`，每日 09:10 读取知识库日报/审计报告并尝试微信推送。
- [x] 微信送达：微信侧已重新绑定到新会话，`getupdates` 返回正常；最小测试消息和 GitHub 学习摘要均已通过 `send_weixin_direct` 发送成功。

### 2026-04-28 验证记录

- Cron job：`7aa310ea-b264-40c8-b23a-ed655c565a69`
- 手动 run：`status=ok`，耗时约 173 秒。
- 模型：`minimax/MiniMax-M2.7`。
- 生成内容检查：包含 GitHub API、候选表、深读项目卡片、skill 判断。
- Hermes 抽样事实审计：`nexu-io/open-design`、`freeCodeCamp/freeCodeCamp`、`Dhravya/webpull` 等项目元数据可由 GitHub API 佐证；部分品牌组合可能被误识别为 repo，需要下一轮修正。
- Delivery：未送达，错误为未配置明确 channel。

### 2026-04-29 收口验证记录

- OpenClaw cron 提示词已更新，要求输出 `source_url`、抓取口径、时间窗口、`owner/repo`、`created_at`、`pushed_at`、`license`、`stars`，且禁止编造未知事实。
- 二次手动 run：`status=ok`，耗时约 169 秒，输出包含必填字段；Hermes 检查未发现必填字段缺失。
- 新增知识库文件：`每日学习/2026-04-29-GitHub热门项目学习日报.md` 与 `质量审计/2026-04-29-质量审计.md`。
- Hermes 推送调度：已创建 cron job `2a82c752d86a`，计划每日 09:10 执行。
- 微信送达验证：重新绑定微信会话后，`getupdates` 正常，最小测试消息已由用户确认收到；GitHub 学习摘要手动推送返回 `success=true`、`chat_id_matches_user=true`。

## 7. 失败回退

| 失败点 | 回退策略 |
|---|---|
| GitHub API 限流 | 使用 Trending HTML 或缓存候选列表 |
| README 缺失 | 不深读，只列入观察 |
| OpenClaw 模型失败 | 切换到已验证模型 `minimax/MiniMax-M2.7` |
| cron 发送失败 | 先落盘 runtime 日志，再由 Hermes 推送摘要 |
| 微信未配置 | 不阻塞知识库落盘，推送改为本地 cron/当前会话报告 |
| 审计不通过 | 保留草稿到 inbox/runtime，不进入 curated 知识资产 |
