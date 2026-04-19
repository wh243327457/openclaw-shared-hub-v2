# MEMORY.md

这是 shared-hub-v3 stage3 seed 的长期记忆入口。

## 规则

- `truth/` 是 v3 唯一的跨 agent 真相源
- 稳定事实进入 `truth/memory/facts/`
- 项目状态进入 `truth/memory/projects/`
- worker agent 不直接写 truth，默认先进入 sandbox 后再由 orchestrator promote
- promote 审计日志进入 `truth/promote-logs/`

## Recent Promote Entries

<!-- SHARED-V3-PROMOTE-ENTRIES:START -->
- 2026-04-17T09:20:13Z | promote-20260417-demo001 | memory-fact | truth/memory/facts/demo-fact.md
<!-- SHARED-V3-PROMOTE-ENTRIES:END -->
