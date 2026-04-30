---
name: github-hot-project-learning
description: 跨 Agent GitHub 热门项目每日学习流水线：OpenClaw 首轮学习，Hermes 质量审计，结果落盘 Obsidian 并生成每日推送。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, research, openclaw, hermes-review, obsidian, daily-learning]
    related_skills: [foundation/shared-memory-bridge, foundation/console-style-progress-report]
---

# GitHub 热门项目学习流水线

## 触发场景

当用户要求：
- 学习 GitHub 热门项目
- 把热门项目总结为技能、经验、尝试
- OpenClaw 先学习，Hermes 再审计
- 每日推送学习成长
- 将学习成果落盘到 Obsidian / shared hub

## 固定分工

1. OpenClaw：负责首轮候选发现、阅读和学习总结。
2. Hermes：负责审计事实、结构、可复用价值、安全和许可证。
3. Obsidian：保存通过审计的长期学习资产。
4. shared hub：保存跨 agent 可复用流程、skill 和运行状态。

## 输入源

优先级从高到低：

1. GitHub Trending：当天热门项目。
2. GitHub Search API：按 stars、pushed、language、topic 补充候选。
3. Releases：近期重大版本发布。
4. 社区讨论：Hacker News、Reddit、X、博客，只作为热度真实性补充。

## 筛选规则

硬门槛：

- 有明确 license。
- README 不为空且能说明用途。
- 最近 30 天有 commit、release 或 issue 活动。
- 不是纯 awesome 列表、资源目录或营销页。
- 没有明显恶意、盗版、凭据泄露或高危操作诱导。

评分维度：

| 维度 | 权重 |
|---|---:|
| 热度真实性 | 20 |
| 工程活跃度 | 20 |
| 文档可读性 | 15 |
| 学习新意 | 20 |
| 可复用性 | 15 |
| 安全与合规 | 10 |

低于 70 分只放速览，不做深读。

## OpenClaw 首轮输出格式

每个深读项目必须输出：

1. 仓库链接、license、主要语言、star/fork/watch、最近更新时间。
2. 一句话判断：这个项目为什么值得学。
3. 解决的问题：它替代了什么旧做法，或补齐了什么能力。
4. 架构/实现：核心模块、数据流、关键依赖。
5. 可复用经验：至少一条“当……时，应优先……”格式规则。
6. 可尝试实验：一个 30 分钟内能做的最小 demo 或阅读任务。
7. 风险边界：license、维护活跃度、安全风险、适用/不适用场景。
8. skill 升格判断：是否值得升格；若值得，给出 skill 草案。

## Hermes 审计标准

按 20 分制审计，低于 16 分返工。

| 项 | 满分要求 |
|---|---|
| 来源完整 | 仓库、README/docs/release/issue 链接齐全 |
| 事实准确 | 关键事实可追溯，不臆测 |
| 中心判断 | 明确说明为什么值得学 |
| 技术深度 | 讲清实现思路和边界 |
| 可复用动作 | 有条件-动作规则或 checklist |
| 安全合规 | 明确 license、安全、数据风险 |
| 反宣传能力 | 能指出局限和不适用场景 |
| Obsidian 结构 | frontmatter 和目录符合知识库规范 |
| Skill 升格判断 | 明确是否升格及原因 |
| 每日推送质量 | 3-5 条高密度行动信息 |

## 落盘路径

Obsidian：

- 总览：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/00-总览索引.md`
- 每日学习：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/YYYY-MM-DD-GitHub热门项目学习日报.md`
- 项目卡片：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/项目卡片/owner-repo.md`
- 质量审计：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/质量审计/YYYY-MM-DD-质量审计.md`

shared：

- 计划：`/home/vany/openclaw-data/.openclaw/shared/docs/plans/YYYY/MM/YYYY-MM-DD-github-hot-project-learning-pipeline.md`
- shared skill：`/home/vany/openclaw-data/.openclaw/shared/capabilities/skills/research/github-hot-project-learning/`
- runtime：`/home/vany/openclaw-data/.openclaw/shared/runtime/hermes/github-hot-project-learning/`

## 每日推送格式

只推 5 段以内：

1. 今日结论：一句话。
2. 值得深读：1-3 个项目和理由。
3. 学到的经验：1-3 条条件-动作规则。
4. 已沉淀资产：知识库文件或 shared skill。
5. 明日继续：下一步最小动作。

## 失败回退

- GitHub 限流：用 Trending HTML 或前日缓存。
- README 缺失：只放观察，不深读。
- OpenClaw 模型失败：切换到已验证模型 `minimax/MiniMax-M2.7`。
- cron 推送失败：先写 runtime 日志，再由 Hermes 当前会话汇报。
- 微信未配置：不阻塞知识库落盘。
- 审计不通过：保留草稿到 runtime，不进入长期知识资产。

## 验证命令

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 scripts/verify_bridge.py
```

预期：`ok: true`。
