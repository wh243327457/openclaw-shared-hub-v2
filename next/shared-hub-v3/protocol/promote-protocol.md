# Promote Protocol

状态：stage3-executable
范围：定义并执行 `sandbox/` -> `truth/` 的最小 promote 链路。

## Trigger

以下场景可以触发 promote：

1. worker agent 已把候选内容写入自己的 `sandbox/<agent>/submissions/`
2. Hermes 已完成 verify / review / policy 检查
3. Hermes 已在 `sandbox/hermes/promote-requests/` 准备好一条 `decision=approved` 的 promote record
4. 目标 truth 路径已经明确，且不违反 `policy/write-rules.yaml`

## Flow

1. submitter 把候选内容写入 `sandbox/<agent>/submissions/`
2. Hermes 读取候选内容并决定是否 promote
3. 若通过，Hermes 生成已审批 promote record
4. `tools/promote_executor.py` 校验 record 并执行复制：`sandbox/` -> `truth/`
5. promote executor 写入 `truth/promote-logs/`
6. promote executor 刷新 `truth/memory/MEMORY.md` 的受托管索引区块

## Record-Format

每次 promote record 应至少记录以下字段：

- `record_id`: promote 记录唯一 ID
- `submitter_agent`: 原始提交 agent
- `source_path`: sandbox 内源路径
- `target_path`: truth 内目标路径
- `content_kind`: `memory-fact` / `memory-project` / `other`
- `promoted_by`: 默认是 Hermes
- `decision`: `approved` / `rejected`
- `promoted_at`: 审批时间戳
- `notes`: 人类可读说明

## Default Target Constraints

- `memory-fact` 必须进入 `truth/memory/facts/`
- `memory-project` 必须进入 `truth/memory/projects/`
- `other` 必须仍然落在 `truth/` 下，但本批次不扩展更多默认映射

## Constraints

- 只有 orchestrator 可以做最终 promote 决策。
- worker agent 不得直接写 `truth/`。
- promote 目标必须位于 `truth/` 下。
- 不得把明文 secret 写入 promote record。
- stage3 只实现“已审批执行器”，不实现自动审批器。
