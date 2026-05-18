# GitHub 热门项目学习闭环系统 Plan

**创建日期**: 2026-05-13
**状态**: 进行中

---

## 目标

建立一个 **Hermes 发指令 → OpenClaw 学习 → Hermes 审计 → 反馈改进模板** 的闭环学习系统。

## 时间线

| 时间 | 任务 | 说明 |
|------|------|------|
| 07:30 | Hermes 生成今日学习指令 | 基于模板 + 审计反馈 + 昨日遗留 |
| 08:30 | OpenClaw 按指令执行学习 | 按照 instruction.md 执行 |
| 09:00 | Hermes 审计学习质量 | 评分 + 反馈 |
| 09:15 | 微信推送学习成果 | 高质量摘要 |

---

## 阶段一：创建学习指令模板

### Step 1.1: 创建学习指令模板

**文件**: `shared/capabilities/skills/research/github-hot-project-learning/templates/daily-instruction.md`

**内容要求**:
- 明确今日学习目标
- 指定学习范围（技术栈、领域）
- 产出要求（格式、数量、深度）
- 质量标准
- 审计反馈区（Hermes 审计后自动更新）

**验证**: OpenClaw 能读取并理解指令

### Step 1.2: 创建指令生成脚本

**文件**: `shared/scripts/generate_daily_instruction.py`

**功能**:
- 读取历史审计反馈
- 分析昨日失败点
- 生成今日强化指令
- 写入 `shared/runtime/hermes/github-hot-project-learning/instruction.md`

**验证**: 脚本能生成指令文件

---

## 阶段二：调整 Cron 任务

### Step 2.1: 删除旧任务

**操作**: 删除任务 9（审计）和任务 10（推送）

**验证**: cron list 确认删除

### Step 2.2: 创建新任务

**任务 A: 学习指令生成** (07:30)
- Cron: `30 7 * * *`
- 触发: `generate_daily_instruction.py`
- 输出: 写入 `shared/runtime/hermes/github-hot-project-learning/instruction.md`

**任务 B: 学习质量审计** (09:00)
- Cron: `0 9 * * *`
- 触发: 审计 OpenClaw 学习结果
- 输出: 写入审计报告 + 更新模板

**任务 C: 微信推送** (09:15)
- Cron: `15 9 * * *`
- 触发: 推送学习成果到微信

**验证**: cron list 显示三个任务，时间正确

---

## 阶段三：创建审计反馈机制

### Step 3.1: 审计结果实时写入模板

**机制**:
- 审计失败时，自动提取失败原因
- 写入 `templates/daily-instruction.md` 的「审计反馈区」
- 生成「今日强化指令」

**示例**:
```markdown
## 审计反馈（自动生成）

### 2026-05-13 失败点
- 问题：深读项目缺少 C5 可迁移设计模式
- 强化：今日深读项目必须包含至少 3 条可迁移模式

### 强化指令
- 重点检查：C5 可迁移设计模式
- 必须输出：每条模式附带落地路径
```

**验证**: 审计失败后，模板自动更新

### Step 3.2: 模板自动进化

**机制**:
- 积累 7 天反馈后，生成「周度优化建议」
- 定期清理过期反馈（保留最近 14 天）
- 季度模板大版本更新

**验证**: 模板有版本号和更新记录

---

## 阶段四：OpenClaw 适配

### Step 4.1: 修改 OpenClaw 学习 cron

**操作**: 修改 OpenClaw 的学习任务，读取 `shared/runtime/hermes/github-hot-project-learning/instruction.md`

**验证**: OpenClaw 执行时使用指令文件

### Step 4.2: OpenClaw 产出规范化

**产出要求**:
- 学习报告: `shared/inbox/openclaw/daily/YYYY-MM-DD.md`
- 项目卡片: `shared/runtime/openclaw/github-learning/projects/`
- 经验沉淀: `shared/runtime/openclaw/github-learning/lessons.md`

**验证**: 文件格式正确，数量达标

---

## 阶段五：监控与优化

### Step 5.1: 创建监控脚本

**文件**: `shared/scripts/learning_pipeline_monitor.py`

**功能**:
- 检查每个步骤是否执行
- 检查产出质量
- 异常告警

**验证**: 脚本能检测失败

### Step 5.2: 月度优化

**操作**: 每月 1 号回顾学习效果，优化模板

---

## 文件清单

```
shared/
├── capabilities/skills/research/github-hot-project-learning/
│   ├── SKILL.md (已有，需更新)
│   └── templates/
│       └── daily-instruction.md (新建)
├── scripts/
│   ├── generate_daily_instruction.py (新建)
│   └── learning_pipeline_monitor.py (新建)
├── runtime/hermes/github-hot-project-learning/
│   ├── instruction.md (每日生成)
│   ├── audit-feedback.json (审计反馈)
│   └── bridge.log (已有)
└── docs/plans/2026/05/
    └── 2026-05-13-github-learning-closed-loop.md (本文件)
```

---

## 验收标准

- [ ] 学习指令模板创建完成
- [ ] Cron 任务时间调整正确
- [ ] 审计失败能实时反馈到模板
- [ ] OpenClaw 能读取并执行指令
- [ ] 每日推送内容正确
- [ ] 监控脚本能检测异常

---

## 风险

1. **OpenClaw 不读指令**: 需要确认 OpenClaw 学习任务会读取 `instruction.md`
2. **审计太严格**: 初期可以适当放宽，逐步提高标准
3. **模板过于复杂**: 保持简洁，OpenClaw 能理解

---

## 变更记录

| 日期 | 变更 | 状态 |
|------|------|------|
| 2026-05-13 | 创建 plan | ✅ 完成 |
| 2026-05-13 | 创建学习指令模板 | ✅ 完成 |
| 2026-05-13 | 创建指令生成脚本 | ✅ 完成 |
| 2026-05-13 | 创建审计反馈脚本 | ✅ 完成 |
| 2026-05-13 | 调整 Cron 任务时间 | ✅ 完成 |
| 2026-05-13 | 创建执行计划文档 | ✅ 完成 |
| 2026-05-13 | 创建单一编排脚本 | ✅ 完成 |
| 2026-05-13 | 创建单一 Cron 任务 | ✅ 完成 |
| 2026-05-14 | 首次闭环测试 | 待执行 |
