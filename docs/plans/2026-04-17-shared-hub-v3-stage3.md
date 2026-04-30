# shared-hub-v3 stage3 计划

状态：implementation / promote-executor
日期：2026-04-17

## 目标

1. 把 stage2 的 promote 协议草案变成可执行的最小执行链路。
2. 保持 v3 的 protocol-first 约束：worker 只提交到 `sandbox/`，Hermes 依据已审批记录执行 promote。
3. 为 stage3 增加可复现实例与本地校验，证明 `sandbox/` -> `truth/` 已经跑通。

## 本批次范围

- 新增 `tools/promote_executor.py`，继续保持 Python 标准库实现。
- 约定 Hermes 读取“已审批 promote record”后执行，不在本批次实现自动审批器。
- 为 `memory-fact` / `memory-project` 建立最小目标映射规则：
  - `memory-fact` -> `truth/memory/facts/`
  - `memory-project` -> `truth/memory/projects/`
- 新增 stage3 demo：至少一条 worker 提交内容 + 一条 Hermes 已审批 promote record。
- 扩展 `tools/shared_v3_verify.py`，加入 stage3 结构检查与 promote dry-run / apply 验证。
- 更新 `README.md`、`AGENTS.md`、`manifest.yaml`、`protocol/promote-protocol.md`、`truth/memory/MEMORY.md`，把执行语义写清楚。

## 非目标

1. 不实现 v2 -> v3 migration adapter。
2. 不把审批决策自动化到 `policy/write-rules.yaml`。
3. 不引入复杂队列、数据库或多 workspace federation。
4. 不让 worker agent 直接写 `truth/`。

## 设计落点

### 1. 决策边界

- promote record 的 `decision` 必须已经是 `approved`。
- stage3 执行器只做“已审批记录的执行器”，不负责生成审批结论。
- 最终 promote authority 仍然只属于 Hermes。

### 2. 审计落点

- 已执行 promote 的审计记录落入 `truth/promote-logs/`。
- promote log 保留 record 核心字段，并补充执行时生成的 `source_sha256` / `target_sha256` / `executed_at`。

### 3. MEMORY 索引更新

- `truth/memory/MEMORY.md` 增加一个受托管的 stage3 区块。
- 每次 promote 成功后，执行器刷新该区块，至少展示最近 promote 的 target 与 record_id。
- 只维护简短索引，不在 `MEMORY.md` 里复制正文内容。

## 计划改动文件

- 新增：`next/shared-hub-v3/tools/promote_executor.py`
- 新增：`next/shared-hub-v3/sandbox/openclaw/submissions/demo-fact.md`
- 新增：`next/shared-hub-v3/sandbox/hermes/promote-requests/demo-fact.md`
- 新增：`next/shared-hub-v3/truth/promote-logs/.gitkeep`
- 修改：`next/shared-hub-v3/README.md`
- 修改：`next/shared-hub-v3/AGENTS.md`
- 修改：`next/shared-hub-v3/manifest.yaml`
- 修改：`next/shared-hub-v3/protocol/promote-protocol.md`
- 修改：`next/shared-hub-v3/protocol/promote-log-template.md`
- 修改：`next/shared-hub-v3/truth/memory/MEMORY.md`
- 修改：`next/shared-hub-v3/tools/shared_v3_verify.py`

## 验证命令

```bash
bash next/shared-hub-v3/scripts/verify_v3.sh
```

预期：
- 输出 `PASS` 与 `wrapper=PASS`
- verifier 能确认 stage3 所需文件齐全
- verifier 能调用 promote executor 完成 demo promote
- demo 结果进入 `truth/memory/facts/` 与 `truth/promote-logs/`
- `truth/memory/MEMORY.md` 的托管区块被刷新
