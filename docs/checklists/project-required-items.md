# 项目必须项清单总览

- 创建时间: 2026-04-25
- 适用项目: shared-hub-v2 / 跨 Agent 共享中台
- 维护位置: `<shared-root>/docs/checklists/project-required-items.md`
- 作用: 只做“必须项定义 + 各 agent 清单入口”，不在这里混写 Hermes / OpenClaw / future-agent 的完成标记。
- 状态规则: 本总览不承载 agent 完成状态；完成状态必须写入对应 agent 自己的清单。
- 安全边界: 禁止写入明文 secret；只记录变量名、路径、验证命令和状态。

## 分账规则

1. 共享总览只维护：必须项定义、agent 清单入口、通用验收口径。
2. Hermes 只更新 Hermes 自己的清单：`docs/checklists/agents/hermes-required-items.md`。
3. OpenClaw 只更新 OpenClaw 自己的清单：`docs/checklists/agents/openclaw-required-items.md`。
4. future-agent 只更新 future-agent 自己的清单：`docs/checklists/agents/future-agent-required-items.md`。
5. 不允许某个 agent 在总览里把全局状态直接标成完成；总览最多写“定义存在 / 清单入口存在”。
6. 同一个必须项可以在不同 agent 清单里有不同状态，例如 Hermes 已完成、OpenClaw 待验证。

## Agent 清单入口

| Agent | 清单路径 | 说明 |
|---|---|---|
| Hermes | `docs/checklists/agents/hermes-required-items.md` | Hermes 本地配置、Hermes 请求链路、Hermes inbox/runtime 等状态 |
| OpenClaw | `docs/checklists/agents/openclaw-required-items.md` | OpenClaw 配置、OpenClaw workspace、OpenClaw 容器路径等状态 |
| future-agent | `docs/checklists/agents/future-agent-required-items.md` | future-agent 接入包与 smoke note 状态 |

## 通用必须项定义

这些是所有 agent 可以复用的“要求定义”，但状态必须回到各自 agent 清单里标记。

### P0

- shared v2 canonical 分层可读
- legacy 兼容入口按需可读
- 共享 skills 入口按 agent 配置接通
- 关键配置事实沉淀且不含明文 secret
- OpenAI-compatible API 请求必须使用 `stream=true`，包括主链路与辅助链路
- inbox → curated 晋升协议可用
- agent 自己的原始记录只写入对应 `inbox/<agent>/daily/`
- agent 自己的运行时产物只写入对应 `runtime/<agent>/`

### P1

- 项目状态字段遵守 `docs/status-schema.md`
- 新共享 skill 升格后同步 `capabilities/manifests/shared-skills.yaml`
- 完成一项必须项后，更新对应 agent 清单的状态、证据路径、验证结果

## 更新记录

### 2026-04-25
- 根据用户校准，将原来的混合状态清单改为“总览 + 每 agent 独立清单”。
- 总览不再承载 Hermes / OpenClaw / future-agent 的完成标记。
