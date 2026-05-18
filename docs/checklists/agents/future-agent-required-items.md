# future-agent 必须项清单

- 创建时间: 2026-04-25
- Agent: future-agent
- 维护位置: `<shared-root>/docs/checklists/agents/future-agent-required-items.md`
- 状态规则: `[x]` = future-agent 已完成并有证据；`[ ]` = future-agent 未完成或待验证；`[~]` = future-agent 已部分完成但仍需审计/修复
- 边界: 这里只标记 future-agent 自己的完成状态，不替 Hermes / OpenClaw 标记。

## P0 必须项

| 状态 | future-agent 必须项 | 当前证据 / 路径 | 最近状态 |
|---|---|---|---|
| [x] | future-agent 最小接入包存在 | `inbox/future-agent/README.md`, `runtime/future-agent/README.md`, `prefill/future-agent-shared-memory.json` | 接入包已准备 |
| [ ] | future-agent 实际读取 shared v2 canonical 分层 | 待 future-agent 实际接入后验证 | 未开始 |
| [ ] | future-agent 原始记录写入自己的 inbox | `inbox/future-agent/daily/YYYY-MM-DD.md` | 等实际接入 |
| [ ] | future-agent runtime 产物写入自己的 runtime | `runtime/future-agent/` | 等实际接入 |
| [ ] | future-agent API 请求流式策略 | 待 future-agent 实际实现后审计 | 未开始 |
| [x] | future-agent 接入要求不包含明文 secret | prefill 只写路径/规则，不写 secret | 已完成 |

## P1 必须项

| 状态 | future-agent 必须项 | 当前证据 / 路径 | 最近状态 |
|---|---|---|---|
| [ ] | future-agent 生成 smoke note | `inbox/future-agent/daily/YYYY-MM-DD.md` | 等实际接入 |
| [ ] | future-agent 接入后运行 verify_bridge.py 复核 | `scripts/verify_bridge.py` | 等实际接入 |

## 更新记录

### 2026-04-25
- 从混合总清单拆分出 future-agent 独立清单。
- 接入包已完成，但实际 agent 状态仍保持未完成/待接入。
