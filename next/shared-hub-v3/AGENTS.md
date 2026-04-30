这是 shared-hub-v3 stage3 seed 的接入说明。

## 设计前提

- v3 采用 protocol-first / manifest-first 思路
- 最小内核固定为：`agents/`、`registry/`、`truth/`、`sandbox/`
- `truth/` 是唯一跨 agent 真相源
- `sandbox/` 是默认写入入口
- 兼容性属于后续 adapter / shim，不属于 v3 存储层

## 角色约束

1. Hermes：orchestrator，负责 verify / promote / register 的编排
2. OpenClaw：worker，默认不能直接写 `truth/`
3. future-agent：supervisor-or-worker，默认也不能直接写 `truth/`

## Stage3 promote 路径

1. worker 把候选内容写入 `sandbox/<agent>/submissions/`
2. Hermes 在 `sandbox/hermes/promote-requests/` 准备“已审批 promote record”
3. `tools/promote_executor.py` 执行 `sandbox/` -> `truth/`
4. 审计记录写入 `truth/promote-logs/`
5. `truth/memory/MEMORY.md` 的受托管区块刷新最近 promote 索引

## 推荐读取顺序

1. `manifest.yaml`
2. `agents/manifest.yaml`
3. `schema/agent.schema.yaml`
4. `truth/memory/MEMORY.md`
5. `registry/manifest.yaml`
6. `registry/capabilities/manifest.yaml`
7. `policy/write-rules.yaml`
8. `protocol/promote-protocol.md`
9. `tools/promote_executor.py`

## 明确禁止

- 不要把 `compat/`、`memory/`、`skills/` 建到 v3 根目录
- 不要把明文 secret 写进 seed
- 不要让 worker agent 直接改写 `truth/`
- 不要把审批决策逻辑和执行器混在一起；stage3 只实现已审批执行器
