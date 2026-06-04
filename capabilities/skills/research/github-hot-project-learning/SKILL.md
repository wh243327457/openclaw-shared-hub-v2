---
name: github-hot-project-learning
description: 跨 Agent GitHub 热门项目每日学习流水线：OpenClaw 首轮学习，Hermes 质量审计，结果落盘 Obsidian 并生成每日推送。
version: 1.4.1
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

## 闭环学习系统（v2 架构）

> 2026-05-13 新增：Hermes 发指令 → OpenClaw 学习 → Hermes 审计 → 反馈改进模板

### 时间线

| 时间 | 任务 | Agent |
|------|------|-------|
| 07:30 | 生成今日学习指令 | Hermes cron |
| 08:30 | 按指令执行学习 | OpenClaw cron |
| 09:00 | 审计学习质量 + 反馈写入模板 | Hermes cron |
| 09:15 | 微信推送学习成果 | Hermes cron |

### 核心文件

- **闭环编排脚本**: `scripts/github_learning_orchestrator.py`（单一任务完成全部流程）
- **学习指令模板**: `templates/daily-instruction.md`（定义学什么、怎么学、产出什么）
- **执行计划文档**: `templates/daily-execution-plan.md`（完整流程定义 + 路径常量）
- **指令生成脚本**: `scripts/generate_daily_instruction.py`（读取审计反馈 → 生成强化指令）
- **审计反馈脚本**: `scripts/audit_feedback_writer.py`（审计失败 → 实时更新模板）
- **审计反馈数据**: `shared/runtime/hermes/github-hot-project-learning/audit-feedback.json`
- **每日生成指令**: `shared/runtime/hermes/github-hot-project-learning/instruction.md`
- **OpenClaw 集成指南**: `references/openclaw-integration.md`（修改学习任务提示词、手动触发等）
- **深挖学习与安全反哺模式**: `references/deep-learning-safe-feedback-pattern.md`（把高质量外部项目研究转成每日学习/巡检的 candidate-first 安全机制）

### 单一任务编排器模式（推荐）

用户希望一个 cron 任务完成整个闭环，而非多个分散任务。编排器读取 plan 文件，按步骤执行：

```
Step 1: 生成今日学习指令（generate_daily_instruction.py）
Step 2: 触发 OpenClaw 学习（docker exec openclaw openclaw cron run <job-id>）
Step 3: 等待完成 + 审计产出
Step 4A: 失败 → 反思 → 更新模板
Step 4B: 成功 → 更新知识库 → 推送微信
```

触发 OpenClaw 学习的关键命令：
```bash
docker exec openclaw openclaw cron run 7aa310ea-b264-40c8-b23a-ed655c565a69
```

### ⚠️ Orchestrator Shell Timeout 与 OpenClaw 调度时序死锁（2026-05-14 发现）

**问题**: `github_learning_orchestrator.py` 以 cron job 身份运行，shell timeout 为 300s，但其内部 `OPENCLAW_TIMEOUT = 1800s`。两个 timeout 完全不匹配，导致 orchestrator 被 SIGKILL 时 OpenClaw 工作实际还未开始。

**时序死锁**（关键根因）:

| 时间 | 事件 |
|------|------|
| 07:30 | `orchestrator.py` cron job 触发，docker exec 发送 `openclaw cron run 7aa310ea...` |
| 07:30 | OpenClaw cron schedule = `30 8 * * *`（08:30 才真正执行） |
| ~07:35 | orchestrator 被 shell timeout (300s) SIGKILL |
| 07:36 | OpenClaw job 实际仍可能在跑（或等待 08:30 调度） |
| 08:30 | OpenClaw cron 正常触发（与 orchestrator 完全无关） |

**现象**: cron `lastRunStatus: ok`（shell 返回码 0 是 SIGKILL 的默认行为），但 `inbox/openclaw/daily/YYYY-MM-DD.md` 未生成。

**修复方案**（推荐）:

**方案 A — 增大 cron job shell timeout**（最简单）
```bash
# 在创建 cron job 时指定 timeout >= 2000（大于 orchestrator 的 1800s OPENCLAW_TIMEOUT）
cronjob(action='create', prompt='...', schedule='...', timeout=2000)
```

**方案 B — 分离 trigger 和 wait**（更健壮，推荐生产环境）
```bash
# Cron job 1 (07:30): 只 trigger，不等待
python3 scripts/github_learning_orchestrator.py --skip-wait --date YYYY-MM-DD

# Cron job 2 (09:30): 只等待 + 审计 + 上报
python3 scripts/github_learning_orchestrator.py --trigger-only --date YYYY-MM-DD
```

**验证方法**:
```bash
# 检查 cron job 配置的 timeout
docker exec openclaw sh -lc 'openclaw cron list'

# 检查 orchestrator 是否在预期位置生成了 inbox
ls -la <shared-root>/inbox/openclaw/daily/YYYY-MM-DD.md
```

### ⚠️ OpenClaw 输出格式不匹配（2026-05-13 发现，2026-06-04 已修复）

**历史问题**: OpenClaw 的实际学习产出格式与 `audit_learning()` 的 regex 不匹配，导致审计假阴性（14/16，内容实际良好）。

**修复状态（2026-06-04）**：✅ 全部修复，审计从 14/16 升至 23/23。

**已修复的 regex**：
- 深读标题：新增 `r'^##\s+深读项目\s+'` 和 `r'^###\s+\d+\.\s+'` 匹配
- Stars 数据：新增表格 header + data row 联合匹配
- License：新增表格格式匹配
- 经验沉淀：新增「可复用经验」章节名兼容
- 明日继续：新增「明日建议」「下一步」「候选反哺」兼容
- 项目提取字段：兼容 `**一句话判断**：`（无 `- ` 前导）和全角/半角冒号

**调试技巧**: 用 `--skip-openclaw` 参数测试编排器流程：
```bash
python3 scripts/github_learning_orchestrator.py --skip-openclaw --date YYYY-MM-DD
```

### 自进化机制

1. 审计失败时，`audit_feedback_writer.py` 自动将失败点写入模板的「审计反馈区」
2. 次日 `generate_daily_instruction.py` 读取反馈，生成「强化指令」
3. OpenClaw 按强化指令执行，避免重复犯错
4. 积累 7 天反馈后自动分析高频失败点

### Plan 文件

完整 plan 位于: `shared/docs/plans/2026/05/2026-05-13-github-learning-closed-loop.md`

## 固定分工

1. **Hermes（主控）**：生成学习指令 → 触发 OpenClaw → 审计产出 → 推送微信。
2. **OpenClaw（执行）**：按指令学习、沉淀，不负责格式化。
3. **Obsidian**：保存通过审计的长期学习资产。
4. **shared hub**：保存跨 agent 可复用流程、skill 和运行状态。

## 闭环编排流程（单一 cron 任务）

```
07:30  Hermes 生成今日学习指令 → shared/runtime/hermes/github-hot-project-learning/instruction.md
       ↓
08:30  OpenClaw 按指令学习 → shared/inbox/openclaw/daily/YYYY-MM-DD.md
       ↓
09:00+ Hermes 审计产出 → 审计反馈写入 audit-feedback.json
       ↓
       审计成功 → 更新知识库 → 推送微信（精华摘要）
       审计失败 → 反思 → 更新模板强化指令
```

### 编排脚本

`shared/scripts/github_learning_orchestrator.py` — 单一脚本完成整个闭环。

### Cron 任务配置

- 任务名：`GitHub 学习：每日闭环执行`
- 时间：`30 7 * * *`
- prompt 中指示：执行编排脚本 → 读取推送文件 → 用 `send_message` 发送微信

### 关键脚本

| 脚本 | 用途 |
|------|------|
| `shared/scripts/github_learning_orchestrator.py` | 闭环编排器 |
| `shared/scripts/generate_daily_instruction.py` | 生成学习指令 |
| `shared/scripts/audit_feedback_writer.py` | 审计反馈写入 |
| `shared/scripts/generate_push_summary.py` | 生成推送摘要（个性版） |

### 关键文件路径

```
shared/
├── capabilities/skills/research/github-hot-project-learning/
│   ├── SKILL.md
│   └── templates/
│       ├── daily-instruction.md          # 学习指令模板
│       └── daily-execution-plan.md       # 执行计划文档
├── scripts/
│   ├── github_learning_orchestrator.py
│   ├── generate_daily_instruction.py
│   ├── audit_feedback_writer.py
│   └── generate_push_summary.py
├── runtime/hermes/github-hot-project-learning/
│   ├── instruction.md                    # 每日生成的学习指令
│   ├── audit-feedback.json               # 审计反馈历史
│   └── wechat-push-YYYY-MM-DD.txt        # 推送内容备份
└── inbox/openclaw/daily/
    └── YYYY-MM-DD.md                     # OpenClaw 学习产出
```

## 微信推送格式要求（v3，重要）

**用户确认 v3 方向可用：推送不是流程字段堆叠，而是一份早上能快速吸收的学习复盘。**

### v3 必须包含的章节

1. 🧭 今日一句话结论 — 先给学习主线和最值得关注的方向
2. 🔥 今日最值得看的项目 — **价值导向表格**
3. 🎯 计划 vs 实际 — Hermes 原计划、OpenClaw 实际产出、Hermes 主观评价
4. 💡 今天真正学到的东西 — 3 条可迁移经验，说明来源和应用方向
5. 🎉 可沉淀判断 — 立即沉淀 / 继续观察 / 暂不沉淀
6. ✅ Hermes 审计结果 — 来源、深度、迁移价值、风险和不足
7. 🧠 Hermes 主观复盘 — 判断、联想、批评或表扬
8. ➡️ 明日学习建议 — 基于今日结果给出继续追踪方向和最小动作
9. 📁 知识库 — 详细报告路径

### 项目表格格式（固定）

```
| 项目 | 为什么值得看 | Hermes 判断 | 可沉淀点 |
|---|---|---|---|
| owner/repo | 解决什么关键问题 | 和用户当前体系有什么关系 | 可复用模式 |
```

禁止退回旧格式：

```
| # | 项目 | 简介 | 亮点 |
```

### 情绪表达规则

情绪必须基于审计事实，不是机械套模板：

- 数量达标 + 内容深入 + 有可沉淀点 → “今天有点惊喜”
- 数量达标但内容浅 → “数量够了，但说实话有点浮”
- 数量少但质量高 → “虽然少，但质量不错”
- 缺关键源码/风险/可迁移经验 → “OpenClaw 今天有点糊弄，需要加压”
- 发现与用户长期系统相关的项目 → “这个值得单独拆一次”

### 排版规范

- 使用分隔线 `━━━━━━━━━━━━━━━━━━━━` 分隔章节
- 使用 `▸` 作为短列表符号
- 标题使用 emoji
- 每个章节之间有空行
- 优先突出最值得看的 2-3 个项目，不要所有项目等权展示

### 禁止事项

- ❌ 不要只说"详见知识库"
- ❌ 不要只列审计优点
- ❌ 不要把 OpenClaw 原文机械压缩
- ❌ 不要缺少 Hermes 主观复盘
- ❌ 不要把项目表格写回“简介/亮点”
- ❌ 不要没有情绪、没有判断
- ❌ 不要生成太长的项目背景介绍

完整模板见：`references/push-message-template.md`。

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
5. 可复用经验：至少一条"当……时，应优先……"格式规则。
6. 可尝试实验：一个 30 分钟内能做的最小 demo 或阅读任务。
7. 风险边界：license、维护活跃度、安全风险、适用/不适用场景。
8. skill 升格判断：是否值得升格；若值得，给出 skill 草案。
9. 候选反哺：按 candidate fact / candidate skill-workflow / open question / 不应自动落地 四类输出，供 Hermes 二轮审计。

### 深挖学习与安全反哺模式（2026-05-22 增强）

本流水线的学习质量标准从“热门项目摘要”升级为“深挖 → 机制抽象 → 反哺建议 → 安全边界”：

1. **深挖对象**：明确今日深挖的是项目、工具、机制还是故障案例；每个深读对象至少核验 README/docs/release/issues 中的 2 类来源。
2. **可验证证据**：给出 GitHub 链接、核心文件/目录、版本/提交或查询时间；不确定结论必须标注“待核验”。
3. **核心机制**：不只罗列功能，必须抽象为可迁移模式，优先使用 `当……时，应优先……，因为……，边界是……`。
4. **反哺判断**：判断是否可进入 shared curated memory、shared skill/workflow、Hermes 审计流程、OpenClaw 每日学习/巡检、runtime POC 或 open questions。
5. **安全边界**：OpenClaw 只产出 candidate；不得自动改配置、模型、provider、cron、secret；不得直接写 curated active fact；不得复制 license 不明或不兼容源码；巡检类结论只输出风险、证据、影响、建议动作，不自动修复。
6. **Hermes 二轮审计**：所有候选反哺必须由 Hermes 按 shared governance 五门准入复核后，才能进入 Obsidian / shared curated / shared skill。

## ⚠️ 防失败规则（来自历史审计教训）

> 以下规则基于 2026-04-28 ~ 2026-05-08 共 5 次审计经验总结，违反任一条将导致审计返工。

### FR-1. 深读项目必须有完整的 C1~C6 六节，不得截断

| 章节 | 必须包含的内容 | 常见错误 |
|------|--------------|---------|
| C1. 核心命令 | README 中的安装/运行命令，标注 OS 要求 | 只写一行安装命令 |
| C2. Repo Tree 摘要 | 目录结构 + 每层用途，用代码块展示 | 截断在某个子目录名处 |
| C3. 关键源码文件 | 列表形式，含文件路径、用途、关键内容摘要 | 缺少此节 |
| C4. 最小运行验证路径 | 5 步以内可完成的验证命令序列 | 只有安装命令，无验证步骤 |
| C5. 可迁移设计模式 | 至少 3 条可复用的工程模式，附落地路径 | 无此节或仅抄 README |
| C6. 风险边界 | 至少 3 条已知限制，需二次验证的点 | 无此节 |

**截断判定**：文件在 C2 之后出现 `…` 或戛然而止 → 直接不合格。

### FR-2. 候选表七列必须齐全，数字必须来自实时 API

```
# | owner/repo | source_url | stars | language | license | created_at | pushed_at | why_selected
```

- `stars`、`license`、`created_at`、`pushed_at` 必须是**实时 GitHub API 查询值**
- `license` 为 null 时必须标注"无license或proprietary"，不得留空
- `why_selected` 必须有**实质性判断**，禁止"很火""值得关注"等泛泛描述

### FR-3. 所有数字必须标注来源和查询时间

每份报告开头必须有抓取口径表：

```
| 查询类型 | URL（完整） | 抓取时间 (UTC) | 筛选算法 |
```

当无法确认数字时，**必须标注"未确认"**，不得凭感觉填充。

### FR-4. 禁止引用未经查询的数据（常见幻觉类型）

- **stars 增速夸张**：某项目"36天破100K stars"——必须注明来源且需二次验证
- **benchmark 数字**：README 声明的性能数字（如"96.6% R@5"）必须标注"来自 README 声明，未交叉验证"
- **skill/design-system 数量**：某项目自称"72 design systems"，需确认数字单位（可能是 design-systems + design-skills 之和）

### FR-5. 深读项目必须有 Skill 升格判断（三级分类）

格式：

```
## D. Skill 升格判断
**项目**：[owner/repo]
**判断**：[可直接迁移 / 需二次验证 / 暂不沉淀]

### 可直接迁移的部分：
1. [具体内容 + 为什么可直接迁移]

### 需要二次验证的部分：
1. [具体内容 + 需要什么验证]

### 暂不沉淀的部分：
1. [具体内容 + 为什么]
```

禁止：完全没有 D 节，或只有"建议进一步研究"这样的空话。

### FR-6. 每份报告必须有可落地章节

禁止只描述"这个项目是什么"，必须有"我们如何用"——说明需要哪些文件、修改哪些配置、影响哪些现有 workflow。

### FR-7. delivery 失败必须写入 inbox 并标注

当推送失败时：
1. 将报告完整内容写入 `shared/inbox/openclaw/daily/YYYY-MM-DD.md`
2. 在报告头部注明 `delivery_status: failed`
3. **不得**声称"已推送"或"发送成功"

### FR-8. 容器状态自检

开始学习前检查 OpenClaw 容器状态。如果容器处于 Exited/Stopping 状态，先 `docker start openclaw` 并等待 `health: healthy` 再执行学习。

### FR-9. 报告完整性自检清单（输出前逐项核对）

- [ ] 抓取口径表完整（URL + 时间 + 筛选算法）
- [ ] 候选表七列齐全，stars 等数字来自实时 API
- [ ] 深读项目 C1~C6 六节完整，无截断
- [ ] Skill 升格判断有实质性三级分类
- [ ] 至少 3 条可复用动作或落地路径
- [ ] 标注已知幻觉点和待验证项
- [ ] 无明文 secret
- [ ] delivery 失败时已写入 inbox 并标注

## Hermes 审计标准（v3，10 维 23 分制）

低于 16 分返工。审计失败自动重试 1 次（清除旧产出→重触发 OpenClaw→再审计）。

| # | 维度 | 分值 | 检查方式 |
|---|------|------|----------|
| 1 | 结构完整 | 4 | 五个必需章节逐一检查（兼容「可复用经验」「候选反哺」等变体章节名） |
| 2 | 深读数量 | 3 | `### 项目` / `### N.N` / `## 深读项目` 头计数，≥3 满分 |
| 3 | 源码深度 | 3 | repo tree/关键文件/架构/代码块 4 信号 |
| 4 | 源码精读 | 2 | 代码块计数：≥6 满分，≥3 半分 |
| 5 | API 数据 | 2 | stars 三路匹配（行内/表格 header/header+data）+ license 两路匹配 |
| 6 | 可迁移经验 | 3 | `当……时，应优先……` 格式 + 经验沉淀/可复用经验章节列表项 |
| 7 | 风险边界 | 2 | license/安全风险/局限性/维护活跃度 4 信号 |
| 8 | Skill 升格 | 2 | `skill 升格/升格判断/可沉淀/暂不沉淀/继续观察` |
| 9 | 落地路径 | 1 | `落地路径/复用路径/在 Hermes/在 OpenClaw` |
| 10 | 无幻觉 | 1 | 可疑 stars >500K 检测 |

PASS 阈值 16，MAX_SCORE=23。实现：`shared/scripts/github_learning_orchestrator.py::audit_learning()`。

## 落盘路径

Obsidian：

- 总览：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/00-总览索引.md`
- 每日学习：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/YYYY-MM-DD-GitHub热门项目学习日报.md`
- 项目卡片：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/项目卡片/owner-repo.md`
- 质量审计：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/质量审计/YYYY-MM-DD-质量审计.md`

shared：

- 计划：`<shared-root>/docs/plans/YYYY/MM/YYYY-MM-DD-github-hot-project-learning-pipeline.md`
- shared skill：`<shared-root>/capabilities/skills/research/github-hot-project-learning/`
- runtime：`<shared-root>/runtime/hermes/github-hot-project-learning/`

## 每日推送格式（v3 - 学习复盘型日报）

> 2026-05-14 用户确认：v3 示例方向可用。推送应从“流程字段堆叠”升级为“早上能快速吸收的学习复盘”。

### 核心要求

1. 第一屏先给价值：`🧭 今日一句话结论`，先说明今日主线和最值得关注的方向。
2. 项目表格固定为价值导向：`项目 / 为什么值得看 / Hermes 判断 / 可沉淀点`。
3. 必须有 Hermes 主观复盘：判断、联想、情绪、批评或表扬，不能机械压缩 OpenClaw 原文。
4. 可沉淀判断必须分级：`✅ 立即沉淀` / `🟡 继续观察` / `❌ 暂不沉淀`，并说明原因。
5. 审计结果必须解释“为什么”：来源完整、技术深度、可迁移价值、风险边界、不足/明日加压点。
6. 明日建议必须来自今日学习结果，包含继续追踪方向、原因和一个最小动作。

### 关键文件

- 完整消息模板：`references/push-message-template.md`
- 执行 plan：`templates/daily-execution-plan.md`
- 实际生成逻辑：`shared/scripts/github_learning_orchestrator.py::generate_push_summary()`

### 执行校验

改动推送模板后必须跑一次历史日报自测，避免“文档已升级但脚本仍旧格式”：

```bash
cd <shared-root>
python3 scripts/github_learning_orchestrator.py --skip-openclaw --date YYYY-MM-DD
cat runtime/hermes/github-hot-project-learning/wechat-push-YYYY-MM-DD.txt
```

检查点：
- [ ] 开头是 `📚 GitHub 热门项目学习日报 · v3`
- [ ] 包含 `🧭 今日一句话结论`
- [ ] 项目表格列为 `项目 / 为什么值得看 / Hermes 判断 / 可沉淀点`
- [ ] `计划 vs 实际` 中经验沉淀数量不是误解析为 0（除非源报告确实没有经验）
- [ ] 包含 `🧠 Hermes 主观复盘`
- [ ] 没有退回“详见知识库”“简介/亮点表格”等旧格式

### 禁止回退

- ❌ 不要恢复 v2 的“Hermes 学习计划 / OpenClaw 学习内容 / 是否符合预期”字段式模板。
- ❌ 不要把项目表格写回 `# / 项目 / 简介 / 亮点`。
- ❌ 不要只报审计分数；必须说明审计判断。
- ❌ 不要让用户自己打开知识库找重点。

### 实现方式

编排脚本 `generate_push_summary()` 从 OpenClaw 日报提取：
1. `今日结论` → 今日主线
2. `深读项目` → 价值导向项目表格
3. `经验沉淀` 或深读项目中的 `可复用经验` → 今天真正学到的东西 + 可沉淀判断
4. 审计得分/问题 → Hermes 审计结果 + 主观复盘 + 明日加压点

然后由 cron 任务读取生成的 `wechat-push-YYYY-MM-DD.txt` 并用 `hermes send -t weixin -f <file>` 发送（或 `cat file | hermes send -t weixin -f -`）。

## 微信主动推送限流保护

主动推送需考虑 iLink 频控，但计数器必须在 Hermes Weixin 平台发送层统一收口，不能由 GitHub 学习日报单独维护。平台层公共状态文件为 `/root/.hermes/weixin/weixin-push-guard.json`：连续 3 次主动推送且用户未回复时自动追加“回复任意内容刷新会话”提示；连续 4 次仍无回复时发送层追加更强提醒，业务层应避免继续推长消息、优先落盘或等用户回复；出现 `ret=-2` / `rate limited` 后记录 `last_rate_limited_at`，不得反复补发同一长内容。业务脚本只生成/落盘 `wechat-push-YYYY-MM-DD.txt`，不要实现局部计数器。微信平台层实现细节见 `hermes-wechat-push` skill 的 `references/weixin-push-guard.md`。

## 失败回退

- GitHub 限流：用 Trending HTML 或前日缓存。
- README 缺失：只放观察，不深读。
- **OpenClaw 容器不可用**：Hermes 用 delegate_task 子 agent 直接深读（见下方「Hermes 直接深读 fallback」）。
- OpenClaw 模型失败：按优先级尝试模型 `minimax/MiniMax-M3`（timeout≥1800s）> `self/gpt-5.4-mini` > `openai/gpt-5.2`。注意 `minimax/MiniMax-Text-01` 不能用于此任务（见下方陷阱）。如果所有模型都失败，走 Hermes fallback 路径。
- cron 推送失败：先写 runtime 日志，再由 Hermes 当前会话汇报。
- 微信未配置：不阻塞知识库落盘。
- 审计不通过：保留草稿到 runtime，不进入长期知识资产。审计失败自动重试 1 次（清除旧产出→重触发→再审计）。

### Hermes 直接深读 fallback（OpenClaw 不可用时）

当 OpenClaw 容器不可用时，Hermes 可独立完成完整深读闭环：

1. **delegate_task 采集 Trending**（web+terminal toolsets，600s 超时）
2. **筛选 3 个高价值项目**（优先 AI/Agent/DevOps/CLI 领域）
3. **并行 delegate_task 每个项目深读**（terminal+file toolsets）
   - 注意 `max_concurrent=1`，实际串行执行
   - 每个子 agent 约 120-300s，总耗时 10-15 分钟
4. **编译完整报告** → 写入 `inbox/openclaw/daily/YYYY-MM-DD-v3.md`
5. **走编排器** `--skip-openclaw` 审计 → 知识库 → 推送

实测 23/23 满分（2026-06-04）。

### 大仓库 clone 超时 fallback

当 `git clone --depth 1` 超时 60s 时，改用 GitHub REST API：

```bash
# 获取目录结构
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/" | jq -r '.[].name'

# 获取文件内容（base64 解码）
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/{path}" | jq -r '.content' | base64 -d

# 获取子目录
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/{dir}?ref=main"
```

未认证限额 60 次/小时。3 个项目各读 10 文件 = 30 次，足够。

## ⚠️ 审计评分体系（v3，2026-06-04 最终版）

旧审计只检查关键词存在性（"有就给分"），导致永远 16/20 通过、issues 永远"无"，反馈闭环断裂。

v3 审计 10 维 23 分制：

| # | 维度 | 分值 | 检查方式 |
|---|------|------|----------|
| 1 | 结构完整 | 4 | 五个必需章节逐一检查（兼容「可复用经验」「候选反哺」等变体章节名） |
| 2 | 深读数量 | 3 | `### 项目` / `### N.N` / `## 深读项目` 头计数，≥3 满分 |
| 3 | 源码深度 | 3 | repo tree/关键文件/架构/代码块 4 信号 |
| 4 | 源码精读 | 2 | 代码块计数：≥6 满分，≥3 半分（新增 v3） |
| 5 | API 数据 | 2 | stars 三路匹配（行内/表格 header/header+data）+ license 两路匹配 |
| 6 | 可迁移经验 | 3 | `当……时，应优先……` 格式 + 经验沉淀/可复用经验章节列表项 |
| 7 | 风险边界 | 2 | license/安全风险/局限性/维护活跃度 4 信号 |
| 8 | Skill 升格 | 2 | `skill 升格/升格判断/可沉淀/暂不沉淀/继续观察` |
| 9 | 落地路径 | 1 | `落地路径/复用路径/在 Hermes/在 OpenClaw`（新增 v3） |
| 10 | 无幻觉 | 1 | 可疑 stars >500K 检测 |

PASS 阈值 16，MAX_SCORE=23。审计失败自动重试 1 次。

实现：`shared/scripts/github_learning_orchestrator.py::audit_learning()` + `_count_pattern()`

## ⚠️ 反馈闭环断裂陷阱（2026-05-30 发现）

**问题**：`handle_success()` 硬编码 `'--issues', '无'`，导致即使审计发现了问题，feedback.json 也只记录"无"。强化指令永远是"今日无特殊要求"。

**根因**：`handle_success` 不接收 `issues` 参数。

**修复**：
1. `handle_success` 签名增加 `issues: list[str]` 参数
2. 调用处从 `handle_success(date, score, strengths, ...)` 改为 `handle_success(date, score, issues, strengths, ...)`
3. 写入 feedback 时过滤：`real_issues = [i for i in issues if i and i != '无']`

**同样修复**：`analyze_failures()` 旧版只看 `score < 16`，新版跟踪通过但有扣分项的情况。

## ⚠️ 关键陷阱

### 微信推送平台名称

**错误**: `send_message(target='wechat')` → `Unknown platform: wechat`
**错误**: `send_message(target='weixin')` → 工具在 cron/受限环境中不可用

**正确**: 使用 `hermes send` CLI（无需 LLM/agent loop，复用 gateway 平台凭证）：
```bash
cat wechat-push-YYYY-MM-DD.txt | hermes send -t weixin -f -
```

iLink Bot 的平台标识是 `weixin`，不是 `wechat`。

`hermes send` 是独立 CLI（`/root/.local/bin/hermes send`），通过 `-t weixin` 指定目标，`-f -` 从 stdin 读取。不依赖 `send_message` 工具，适合 cron job 和脚本调用。

### ⚠️ OpenClaw protocol mismatch 时的 Hermes fallback（2026-05-22 发现）

如果 `docker exec openclaw openclaw cron run <job-id>` 失败，错误包含：

```text
GatewayClientRequestError: protocol mismatch
GatewayTransportError: gateway closed (1002): protocol mismatch
```

不要直接声称闭环失败，也不要反复重启/重试到超时。先确认 `runtime/hermes/github-hot-project-learning/instruction.md` 已生成；如果 `inbox/openclaw/daily/YYYY-MM-DD.md` 尚不存在，可由 Hermes fallback executor/subagent 读取今日 instruction，代执行 GitHub 热门项目学习，并写入 OpenClaw 兼容产物：

```text
shared/inbox/openclaw/daily/YYYY-MM-DD.md
```

随后使用审计-only 路径收口：

```bash
cd /home/vany/agent/shared
python3 scripts/github_learning_orchestrator.py --skip-openclaw --date YYYY-MM-DD
```

最终汇报必须区分：
- OpenClaw 原定 cron 触发失败；
- Hermes fallback 已代执行学习；
- 审计与知识库是否完成；
- 微信是否实际发送。

详细案例：`references/2026-05-22-fallback-and-push-guard.md`。

Full session details: `references/2026-05-27-manual-retrigger-and-wechat-rate-limit.md`.

### ⚠️ OpenClaw 模型级联失败（2026-06-02 发现）

当 OpenClaw cron job 的模型从 allowlist 被移除或 provider key 失效时，逐个尝试模型会导致多次失败。不同模型的典型失败模式：

| 模型 | 典型错误 | 耗时 | 诊断 |
|------|---------|------|------|
| `minimax/MiniMax-M2.7` | `rejected by agents.defaults.models allowlist` | 24ms | 模型已从 allowlist 移除 |
| `minimax/MiniMax-M3` | 超时（600s 不够） | ~556s | 需要 `--timeout-seconds 1800` |
| `minimax/MiniMax-Text-01` | 完成但**不写文件** | ~52s | ⚠️ 该模型不使用工具，只返回推理文本 |
| `deepseek/deepseek-v4-flash` | `HTTP 401: Invalid API Key` | <1s | Provider API key 过期 |
| `mimo/MiMo-V2.5-Pro` | `HTTP 401: Invalid API Key` | <1s | Provider API key 过期 |
| `openai/gpt-5.2` | `hasBeforeToolCallPolicy is not a function` | ~11s | OpenClaw 版本兼容问题 |
| `self/gpt-5.4` | `403 Forbidden` | ~4s | 自托管模型权限问题 |

**诊断命令**：
```bash
# 查看最近一次 run 的错误
docker exec openclaw openclaw cron runs --id <job-id> --limit 1 2>&1 | grep -E '"error"|"status"|"durationMs"'

# 查看 allowlist 中可用的模型
docker exec openclaw openclaw config get agents.defaults.models 2>&1

# 改模型
docker exec openclaw openclaw cron edit <job-id> --model "minimax/MiniMax-M3" --timeout-seconds 1800

# 改完后重新触发
docker exec openclaw openclaw cron run <job-id>
```

**关键教训**：
- `minimax/MiniMax-Text-01` 虽然返回 `status: ok`，但**不调用任何工具**，不写文件。不要因为 cron run 成功就认为产出已生成，必须检查 inbox 文件是否实际存在。
- `minimax/MiniMax-M3` 需要至少 1800s timeout，原来的 600s 不够。
- 检查 cron run status 要用 `openclaw cron list`（实时状态）而不是 `cron runs`（历史记录可能缓存旧的 error）。

### ⚠️ Orchestrator timeout but instruction already exists: manual re-trigger recovery

When `github_learning_orchestrator.py` times out at shell timeout (300s), but the daily instruction was already generated (either by an earlier orchestrator step or by `generate_daily_instruction.py` directly), OpenClaw is healthy and just needs to be manually triggered. This is **simpler** than the fallback pattern — no need for Hermes to do the learning itself.

**Recovery steps:**

1. Confirm instruction exists: `ls -la <shared-root>/runtime/hermes/github-hot-project-learning/instruction.md`
2. Check OpenClaw is running: `docker inspect -f '{{.State.Status}}' openclaw`
3. Trigger manually: `docker exec openclaw openclaw cron run <job-id>`
   - If `"already-running"`, wait 30s and retry
   - If `"enqueued": true`, proceed to wait
4. Poll for output every 30s (15min max): `ls -la <shared-root>/inbox/openclaw/daily/YYYY-MM-DD.md`
   **Key timing**: When instruction already exists and container is healthy, OpenClaw typically completes in **~2 minutes**, not 10-15 min.
5. Once output exists, close with audit-only:
   ```bash
   cd /home/vany/agent/shared
   python3 scripts/github_learning_orchestrator.py --skip-openclaw --date YYYY-MM-DD
   ```

### ⚠️ OpenClaw gateway 1006 immediately after container auto-start: wait + manual cron run recovery

If `github_learning_orchestrator.py` starts the OpenClaw container and Step 2 fails with:

```text
GatewayTransportError: gateway closed (1006 abnormal closure)
Gateway target: ws://127.0.0.1:18789
```

Do not immediately declare the learning loop failed and do not jump straight to Hermes fallback. First treat this as a gateway readiness race:

1. Check/wait for the `openclaw` container to keep running and move past startup.
2. Manually enqueue the OpenClaw learning job:
   ```bash
   docker exec openclaw sh -lc 'openclaw cron run 7aa310ea-b264-40c8-b23a-ed655c565a69 --expect-final --timeout 600000'
   ```
3. Poll for today's report:
   ```bash
   test -s /home/vany/agent/shared/inbox/openclaw/daily/$(date +%F).md
   ```
4. Once the report exists, close the loop with audit-only mode:
   ```bash
   cd /home/vany/agent/shared
   python3 scripts/github_learning_orchestrator.py --skip-openclaw --date $(date +%F)
   ```
5. Only if the manual enqueue fails or the daily report never appears should Hermes fallback execute the learning task itself.

Final reporting must distinguish: initial orchestrator trigger failed, manual OpenClaw enqueue recovered the learning step, audit/knowledge-base status, and Weixin delivery status.

### ⚠️ `push_guard_active` / `ret=-2 rate limited` 不是发送成功

如果 `hermes send -t weixin -f -` 返回：

```text
Weixin send failed: push_guard_active
```

或：

```text
hermes send: Weixin send failed: iLink sendmessage rate limited: ret=-2 errcode=None errmsg=rate limited
```

这是 Hermes Weixin 平台层主动推送保护或 iLink 频控生效。不要绕过、不要连续补发、不要声称“微信已推送”。正确处理：

1. 保留 `runtime/hermes/github-hot-project-learning/wechat-push-YYYY-MM-DD.txt`。
2. 最终报告写清：推送内容已落盘，但微信未实际发出。
3. 在 `inbox/hermes/daily/YYYY-MM-DD.md` 追加一条执行记录，至少包含：
   - `pipeline: github-hot-project-learning`
   - `audit_status`
   - `knowledge_base_status`
   - `weixin_delivery_status: failed`
   - `delivery_error`
   - `push_file`
4. 追加记录后跑 `python3 scripts/verify_bridge.py` 做 shared 入口健康复核。

不要因为 cron prompt 写了 `send_message` 就尝试绕过平台层；cron/受限环境优先使用 `hermes send -t weixin -f -`，发送失败时按上面流程落盘和报告。


### Hermes cron 创建参数

**错误**: `cronjob(action='create', script='...')` → 缺少 prompt/skill
**正确**: `cronjob(action='create', prompt='...', schedule='...')`

Hermes cron 必须提供 `prompt` 或 `skill`，不支持直接 `script`。

### auth.json 重复条目

**问题**: 同一个 provider 可能在 `auth.json` 中出现多次（来自 env 变量和 config.yaml），导致模型列表显示多个组。

**排查**:
```bash
grep -A 10 "provider-name" /root/.hermes/auth.json
```

**解决**: 删除旧的 env 条目，保留 config.yaml 条目。

### MiMo API base_url 错误

**问题**: `tp-` 前缀的 API key 使用 `token-plan-cn.xiaomimimo.com`，不是 `api.xiaomimimo.com`。

**验证**:
```bash
curl -s -o /dev/null -w "%{http_code}" https://api.xiaomimimo.com/v1/models -H "Authorization: Bearer <key>"
# 返回 401 = 错误

curl -s https://token-plan-cn.xiaomimimo.com/v1/models -H "Authorization: Bearer <key>"
# 返回 200 = 正确
```

## 验证命令

```bash
cd <shared-root>
python3 scripts/verify_bridge.py
```

预期：`ok: true`。
