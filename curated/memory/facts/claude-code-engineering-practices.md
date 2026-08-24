---
fact_id: claude-code-engineering-practices
topic: Claude Code 工程实践模式提取
category: agent-engineering
status: active
source: autonomous-learning/pending-promotion
date: 2026-05-17
created_at: 2026-05-17
score: 18/20
fact_id: claude-code-engineering-practices
freshness_class: slow_changing
scope: cross-agent
subject: agent-engineering
attribute: engineering-practices
value_summary: "Claude Code 工程模式：验证优先、权限先于自主权、project rules 作为可执行上下文"
updated_at: 2026-08-24
last_verified_at: 2026-08-24
review_due_at: 2026-11-24
confidence: high
secret_checked: true
---

# Claude Code 工程实践模式提取

Claude Code 的核心理念是将 AI coding agent 从聊天助手转变为可配置、可验证、可自动化的工程执行环境。关键架构分层：上下文层（CLAUDE.md、memory、skills）、执行层（shell/CLI 工具、测试、截图、预期输出、非交互模式）、集成层（MCP、hooks、permissions）、自动化层（headless mode + JSON/streaming JSON）。

三个最高杠杆的工程模式：(1) Verification-first——先定义成功标准再行动，用测试/截图/预期输出做验证，是减少自动化幻觉和返工的最高杠杆动作；(2) Permissions-before-autonomy——先定义权限和危险门控再扩展自治度，对无人值守 cron agent 尤其关键；(3) Project rules 作为可执行上下文——在 CLAUDE.md 中写 agent 可读的项目规则，而非仅靠 system prompt。

可复用模式：探索优先于修改；将重复工作流打包为 skills/commands；hook 保持幂等和可观测；MCP 作为适配器边界而非 prompt stuffing。

## 证据来源
- 质量评审: `reviews/non-github-learning-2026-05-17-claude-code-engineering-practices-quality-review.md` (18/20)
- 原始链接: https://www.anthropic.com/engineering/claude-code-best-practices
