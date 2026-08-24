---
fact_id: agent-engineering-verification-first-practices
status: active
freshness_class: slow_changing
scope: cross-agent
subject: agent-engineering
attribute: engineering-practice-patterns
value_summary: "Agent 工程应采用 Verification-first：先定义可验证成功标准再实现，验证产物而非意图"
created_at: 2026-05-18
updated_at: 2026-08-24
last_verified_at: 2026-08-24
review_due_at: 2026-11-24
source_refs:
  - runtime/hermes/autonomous-learning/agent-outputs/
conflict: null
supersedes: null
superseded_by: null
confidence: high
authority: hermes-autonomous-learning
secret_checked: true
---

# Agent 工程 Verification-first 实践

- 晋升时间：`2026-05-18T12:07:05+08:00`
- 来源：`runtime/hermes/autonomous-learning/agent-outputs/non-github-learning-2026-05-17-claude-code-engineering-practices.md`
- 审计：`runtime/hermes/autonomous-learning/reviews/non-github-learning-2026-05-17-claude-code-engineering-practices-quality-review.md`，18/20
- 状态：accepted_by_user

## 稳定结论

Claude Code 工程实践可抽象为通用 agent 工程规范：先提供项目级上下文和成功标准，再让 agent 执行；执行后必须用测试、截图、预期输出、lint/build 或结构化报告验证。自治能力必须建立在权限边界、可观测 hooks、可回滚 skills 之上。

## 可复用规则

1. **Project rules first**：执行前读取项目规则/AGENTS/CLAUDE/skill，而不是直接改文件。
2. **Success criteria before action**：先定义验收标准，再执行实现或调研。
3. **Explore first, modify second**：先审计结构与现状，再写入或改配置。
4. **Verification-first**：每次改动后尽量跑 JSON 解析、lint、测试、dry-run、health check 或 read-back。
5. **Permissions-before-autonomy**：headless/cron/自动修复前先定义权限、危险动作 gate、日志和禁用开关。
6. **MCP/工具作为 adapter boundary**：不要把所有上下文塞进 prompt；工具接口要有清楚输入输出和权限。
7. **Hooks 必须幂等可观测**：自动化 hook 需要日志、错误处理和禁用路径。

## 约束与风险

- 上下文文件会膨胀，需分层：稳定规则进 curated/skills，运行状态进 runtime，原始记录进 inbox。
- 弱测试会制造假闭环；没有验证证据时不能报告“已完成”。
- headless 模式不适合不确定或高风险任务，必须保留人工审批。

## 对当前系统的落地

- 自主学习 cron 保持 hardened prompt + preflight/postrun guard。
- 配置/secret/cron/curated 写入继续要求显式审批或明确目标识别。
- 复杂工程任务继续采用“先读规则与计划 → 执行 → 验证 → 写 inbox/curated”的闭环。
