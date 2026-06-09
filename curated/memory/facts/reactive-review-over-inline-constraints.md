---
fact_id: reactive-review-over-inline-constraints
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-code-review
attribute: design-pattern
value_summary: "给 Agent 加质量门禁应优先用 reactive review（事后审查）而非 inline constraints（行内约束），不干扰生成过程且捕获率更高"
created_at: 2026-06-09
updated_at: 2026-06-09
last_verified_at: 2026-06-09
review_due_at: 2026-07-09
source_refs:
  - https://github.com/amElnagdy/guard-skills
  - https://github.com/JimLiu/baoyu-design
  - daily-report: 2026-06-09-GitHub热门项目学习日报.md
conflict: null
supersedes: null
superseded_by: null
confidence: medium
authority: hermes-autonomous-learning
secret_checked: true
---

# Reactive Review > Inline Constraints

## 核心内容

当需要给编码 Agent 加质量门禁时，应优先用 **reactive review**（事后审查）而非 **inline constraints**（行内约束）：

### 为什么事后审查更好

1. **不干扰生成过程**：Agent 可以自由发挥创造力，审查在完成后独立进行
2. **可以引用已发表的研究**：如 AI 6 大失败模式、SOLID 原则、DRY/KISS/YAGNI
3. **审查规则可独立更新**：不依赖 Agent 的 prompt 或配置
4. **可组合**：多个 guard skill 按需组合（code + test + docs）

### 实现模式

```
Agent 完成工作（生成代码/文档/测试）
  → 加载独立 guard skill
  → 在 diff 上运行审查规则
  → 输出问题列表和修复建议
  → Agent 根据建议修改
```

### Guard Skill 架构

- `SKILL.md` — 审查入口和流程编排
- `references/` — 详细规则（如 ai-failure-modes.md、solid.md）
- `agents/` — 平台特定元数据

## 边界

- 双项目验证（guard-skills + baoyu-design），confidence: medium-high
- 需要 Agent 支持 skill 加载机制
- 审查质量依赖规则准确性，需持续维护

## 适用场景

- Hermes requesting-code-review skill 改进
- 任何需要 Agent 输出质量保证的工作流
- 多领域审查（代码、测试、文档、安全）

## 来源

- guard-skills (⭐467, MIT) + baoyu-design (⭐519, MIT)
- 2026-06-09 GitHub 热门项目学习日报深读
