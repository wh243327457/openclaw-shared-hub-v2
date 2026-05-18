# Skill-as-Contract 与 Subagent 四状态协议

- 晋升时间：`2026-05-18T12:07:05+08:00`
- 来源：`runtime/hermes/autonomous-learning/agent-outputs/hermes-delegate/2026-05-17-superpowers-deep-analysis.md`
- 审计：`runtime/hermes/autonomous-learning/reviews/2026-05-17-superpowers-deep-analysis-quality-review.md`，18/20
- 状态：accepted_by_user

## 稳定结论

`obra/superpowers` 的核心价值不是具体实现，而是把 Markdown skill 当成 **行为契约**：skill 不是“建议文档”，而是带 hard gate、触发条件和验收标准的执行协议。这个模式适合用于 shared skills、自主学习模板和跨 agent handoff。

## 可复用规则

1. **Skill-as-Behavioral-Contract**：共享 skill 要写成可执行约束，包含触发条件、必须动作、禁止事项、验收标准。
2. **强标签用于关键流程**：可在高风险流程使用 `<HARD-GATE>`、`<SUBAGENT-STOP>`、`<EXTREMELY-IMPORTANT>` 风格的显式边界，但不要滥用。
3. **Subagent 四状态**：执行 agent 汇报应限制为 `DONE`、`DONE_WITH_CONCERNS`、`NEEDS_CONTEXT`、`BLOCKED`，避免自称 review/promotion 已通过。
4. **两阶段 review**：controller 收到执行产物后先做 spec compliance，再做 quality review；执行 agent 不得自审通过。
5. **CSO 描述优化**：skill description 应以触发条件和关键词为主，少写流程长摘要，方便 agent 检索命中。

## 约束与风险

- 纯 prompt 约束不是安全边界，不能替代权限控制和验证脚本。
- hard gate 会增加 token 与流程成本，探索性任务不宜过度流程化。
- shared skill 需要版本化和回滚，否则会把坏流程长期固化。

## 对当前系统的落地

- `autonomous-learning/orchestrator-protocol` 的子 agent 状态与 review gate 继续保持强约束。
- 新 shared skill 升格前应补齐 description 触发条件、硬边界和验证命令。
- 未来可以用 “TDD for skills” 对关键 workflow skill 做 pressure test。
