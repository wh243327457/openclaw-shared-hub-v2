---
fact_id: agent-skill-architecture-four-part-pattern
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-engineering
attribute: architecture-pattern
value_summary: "Agent Skill 标准四件套架构：SKILL.md 入口 + system-prompt.md 方法论 + references/ 平台映射 + built-in-skills/ 专项能力"
created_at: 2026-06-09
updated_at: 2026-08-25
last_verified_at: 2026-08-25
review_due_at: 2026-11-23
source_refs:
  - https://github.com/JimLiu/baoyu-design
  - daily-report: 2026-06-09-GitHub热门项目学习日报.md
conflict: null
supersedes: null
superseded_by: null
confidence: medium
authority: hermes-autonomous-learning
secret_checked: true
---

# Agent Skill 架构四件套模式

## 核心内容

当需要封装一个复杂能力为 Agent Skill 时，应优先用四件套结构：

1. **SKILL.md** — 入口文件，编排整个流程，保持精简（降低 token 消耗）
2. **system-prompt.md**（或核心方法论文档）— 工艺标准、质量要求、设计哲学
3. **references/** — 平台特定工具映射（如 claude.md、cursor.md、codex.md）
4. **built-in-skills/** — 专项能力子 skill（按需加载）

### 设计原则

- **Progressive disclosure**：SKILL.md 精简，深入内容按需加载
- **Harness-adaptive**：skill 检测运行环境，加载对应的 references/ 映射文件
- **核心逻辑平台无关**：每个平台只需一个映射文件

### 边界

- 单项目验证（baoyu-design），confidence: medium
- 依赖 Agent 支持 skill 加载机制
- references/ 映射文件需随平台 API 变化更新

## 适用场景

- Hermes/OpenClaw skill 设计规范
- 需要支持多 Agent 平台的能力封装
- 复杂工作流的 skill 化

## 来源

- baoyu-design (⭐519, MIT) — 把 Claude Design 封装为本地 Agent Skill
- 2026-06-09 GitHub 热门项目学习日报深读
