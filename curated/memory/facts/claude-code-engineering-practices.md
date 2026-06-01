---
fact_id: claude-code-engineering-practices
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-workflow / engineering-practices
attribute: best-practices
value_summary: "Claude Code 官方工程实践的 8 个可迁移模式：项目级 CLAUDE.md、验证优先、先探索后修改、技能封装、headless 自动化、MCP 适配层、幂等 hooks、渐进授权"
created_at: 2026-05-17
updated_at: 2026-05-31
last_verified_at: 2026-05-31
review_due_at: 2026-06-30
source_refs:
  - https://www.anthropic.com/engineering/claude-code-best-practices
  - https://docs.anthropic.com/en/docs/claude-code/overview
  - runtime/hermes/autonomous-learning/agent-outputs/non-github-learning-2026-05-17-claude-code-engineering-practices.md
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# Claude Code 官方工程实践 — 可迁移模式

## 核心模式

1. **项目级 CLAUDE.md**：agent 可读的项目规则文件，区分稳定规则/项目状态/笔记/日志
2. **验证优先**：定义成功标准（tests/screenshots/expected outputs）再行动
3. **先探索后修改**：explore first, modify second
4. **技能封装**：可复用工作流打包为 skills/commands
5. **Headless 自动化**：非交互模式 + JSON/streaming JSON 用于 CI 和定时任务
6. **MCP 适配层**：MCP 作为集成边界，不是 prompt stuffing
7. **幂等 hooks**：生命周期自动化但需日志和关闭开关
8. **渐进授权**：先定义权限和危险门，再扩大自治

## 与我们系统的关联

- Hermes 的 SKILL.md ≈ Claude Code 的 skills
- shared hub 的 AGENTS.md ≈ 项目级 CLAUDE.md
- self-healing-agent 的先 plan 再 apply ≈ 验证优先
- cron jobs ≈ headless 自动化
