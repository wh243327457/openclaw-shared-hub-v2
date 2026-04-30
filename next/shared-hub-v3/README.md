# shared-hub-v3

这是放在当前 repo 内的 v3 stage3 seed。

它的目的不是接管现有 v2，而是把 v3 的最小内核推进成一个“可执行、可校验、可继续扩展”的协议骨架。

## 当前范围

- 最小内核：`agents/`、`registry/`、`truth/`、`sandbox/`
- 声明式入口：`manifest.yaml`
- capability registry：`registry/capabilities/`
- agent schema：`schema/agent.schema.yaml`
- promote 协议 + 已审批执行器：`protocol/` + `tools/promote_executor.py`
- 本地校验：`tools/shared_v3_verify.py` + `scripts/verify_v3.sh`

## Stage3 新增

- 可执行 promote 链路：`tools/promote_executor.py`
- content_kind 默认目标约束：
  - `memory-fact` -> `truth/memory/facts/`
  - `memory-project` -> `truth/memory/projects/`
- 审计日志：`truth/promote-logs/`
- MEMORY.md 受托管区块：自动记录最近 promote 条目
- Demo fixtures：`sandbox/openclaw/submissions/`、`sandbox/hermes/promote-requests/`

## 明确不做

- 不在 v3 根目录保留 `compat/`、`memory/`、`skills/`
- 不复用 v2 的 storage layout 作为 v3 真相源
- 不在本批次实现迁移或 adapter
- 不实现自动审批器

## 校验

```bash
bash next/shared-hub-v3/scripts/verify_v3.sh
```
