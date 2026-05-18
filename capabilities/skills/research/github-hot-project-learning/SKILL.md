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

### ⚠️ OpenClaw 输出格式不匹配（2026-05-13 发现）

**问题**: OpenClaw 的实际学习产出格式（A/B/C 章节结构）与 `daily-instruction.md` 模板定义的格式不同。

OpenClaw 实际输出结构：
- A. 抓取口径（查询 URL、抓取时间、筛选算法）
- B. 候选表（7 列：owner/repo、stars、language、license 等）
- C. 深读项目（README 核心命令、源码分析等）

模板期望的结构：
- 今日结论、项目速览、深读项目、经验沉淀、明日继续

**影响**: 审计时因格式不匹配被判定为缺失章节，导致不必要的扣分。

**调试技巧**: 用 `--skip-openclaw` 参数测试编排器流程，避免每次等 30 分钟：
```bash
python3 scripts/github_learning_orchestrator.py --skip-openclaw
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

然后由 cron 任务读取生成的 `wechat-push-YYYY-MM-DD.txt` 并用 `send_message(target='weixin')` 发送。

## 微信主动推送限流保护

主动推送需考虑 iLink 频控，但计数器必须在 Hermes Weixin 平台发送层统一收口，不能由 GitHub 学习日报单独维护。平台层公共状态文件为 `/root/.hermes/weixin/weixin-push-guard.json`：连续 3 次主动推送且用户未回复时自动追加“回复任意内容刷新会话”提示；连续 4 次仍无回复时发送层追加更强提醒，业务层应避免继续推长消息、优先落盘或等用户回复；出现 `ret=-2` / `rate limited` 后记录 `last_rate_limited_at`，不得反复补发同一长内容。业务脚本只生成/落盘 `wechat-push-YYYY-MM-DD.txt`，不要实现局部计数器。微信平台层实现细节见 `hermes-wechat-push` skill 的 `references/weixin-push-guard.md`。

## 失败回退

- GitHub 限流：用 Trending HTML 或前日缓存。
- README 缺失：只放观察，不深读。
- OpenClaw 模型失败：切换到已验证模型 `minimax/MiniMax-M2.7`。
- cron 推送失败：先写 runtime 日志，再由 Hermes 当前会话汇报。
- 微信未配置：不阻塞知识库落盘。
- 审计不通过：保留草稿到 runtime，不进入长期知识资产。

## ⚠️ 关键陷阱

### 微信推送平台名称

**错误**: `send_message(target='wechat')` → `Unknown platform: wechat`
**正确**: `send_message(target='weixin')`

iLink Bot 的平台标识是 `weixin`，不是 `wechat`。

### 微信限流

iLink sendmessage 可返回 `ret=-2 errcode=None errmsg=rate limited`。
间隔 5-10 分钟再发，或写入文件备用。

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
