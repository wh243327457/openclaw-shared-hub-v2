# Shared skill governance

共享 skill 是跨 agent 的 class-level 能力契约，不是单次会话记录库。

## 升格准入

新 skill 进入 `capabilities/skills/` 前，至少满足一项：

1. Hermes / OpenClaw / future-agent 中两个以上 agent 会复用。
2. 属于横切治理能力：共享中台、共享记忆、配置目标识别、进度汇报、调研协作、自动化编排等。
3. 不共享会导致不同 agent 行为漂移、重复造轮子或长期规则不一致。
4. 它描述的是稳定工作流，而不是一次性任务复盘。

如果只对当前 agent 有用，应保留在该 agent 本地 skill，并在汇报中说明“当前仅本地长期，不是 shared 长期能力”。

## shared skill 内容边界

`SKILL.md` 应保留：

- 触发条件。
- 标准流程。
- 输入 / 输出契约。
- 验证命令。
- 关键 pitfalls。
- 指向少量 class-level references 的链接。

`SKILL.md` 不应堆放：

- 单次会话完整流水账。
- 原始日志、stdout、score/source 明细。
- 大段 raw 调研材料。
- 可过期的一次性任务状态。

## references 治理

`references/` 用来保存可复用经验，不是 session dump。

推荐形态：

- 一个主题一个 class-level reference，例如 `shared-hub-slimming-iteration.md`。
- 多次会话经验合并进同一个主题文档，保留“规则 / 坑点 / 验证命令”，删除流水账式细节。
- 如果 reference 只服务一次任务，应优先放到 `runtime/<agent>/<project>/` 或 `docs/plans/`，不要进入 shared skill。

告警阈值：

- 单个 shared skill 的 `references/` 文件数 > 15 时，应触发 review。
- review 动作优先是合并同主题 reference，而不是删除仍有价值的依据。
- 删除 reference 前必须确认其中稳定规则已被吸收进 `SKILL.md` 或 class-level reference。

## manifest 元数据

`capabilities/manifests/shared-skills.yaml` 中每个条目应包含：

- `scope`: 能力范围，使用 `cross-agent`、`workflow`、`governance`、`research-pipeline` 等。
- `reference_policy`: reference 治理策略，例如 `class-level-only` 或 `bounded-class-level`。
- `future_agent_readable`: future-agent 是否可直接读取。

## 审查清单

新增或更新 shared skill 时检查：

1. 是否真的跨 agent 复用？
2. 是否已登记 manifest？
3. 是否有明确 owner / status / last_reviewed？
4. 是否没有写入 secret？
5. references 是否是可复用主题文档，而非单次任务日志？
6. 如 reference 数量增长，是否更新或合并了 class-level 文档？
