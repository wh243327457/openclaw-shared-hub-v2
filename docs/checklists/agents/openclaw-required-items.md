# OpenClaw 必须项清单

- 创建时间: 2026-04-25
- Agent: OpenClaw
- 维护位置: `<shared-root>/docs/checklists/agents/openclaw-required-items.md`
- 状态规则: `[x]` = OpenClaw 已完成并有证据；`[ ]` = OpenClaw 未完成或待验证；`[~]` = OpenClaw 已部分完成但仍需审计/修复
- 边界: 这里只标记 OpenClaw 自己的完成状态，不替 Hermes / future-agent 标记。

## P0 必须项

| 状态 | OpenClaw 必须项 | 当前证据 / 路径 | 最近状态 |
|---|---|---|---|
| [x] | OpenClaw 可通过容器路径读取 shared | `/home/node/.openclaw/shared/` | 已定义 |
| [x] | OpenClaw 共享 skill 入口已接通 | `/home/node/.openclaw/shared/skills` | `verify_bridge.py` 通过 |
| [x] | OpenClaw 配置事实已沉淀且不含明文 secret | `curated/memory/facts/openclaw-config.md` | 已完成 |
| [x] | OpenClaw 旧 workspace 兼容入口可解析 | `memory/MEMORY.md`, `memory/daily`, workspace symlink | `verify_bridge.py` 通过 |
| [x] | OpenClaw 原始记录应进入自己的 inbox | `inbox/openclaw/daily/` | 已有 canonical 路径 |
| [x] | OpenClaw runtime 产物有独立目录 | `runtime/openclaw/`, `runtime/openclaw/dreams/` | 已完成 |
| [~] | OpenClaw 自身 API 请求流式策略 | 已审计 Docker 镜像；主模型出站链路为 `stream: true`，但 Kimi/Perplexity 辅助 `/chat/completions` 仍为非流式 JSON | 2026-04-28：部分完成，需修复 auxiliary 后才能标 [x] |
| [x] | OpenClaw 不把明文 secret 写入 shared | shared 中只记录环境变量名/占位符 | 已执行 |

## P1 必须项

| 状态 | OpenClaw 必须项 | 当前证据 / 路径 | 最近状态 |
|---|---|---|---|
| [x] | OpenClaw daily 兼容视图仍可访问 | `compat/daily/`, `memory/daily` | 已完成 |
| [ ] | OpenClaw 后续新增 workspace 时同步检查 shared symlink | `scripts/verify_bridge.py --workspace-name <name>` | 持续项 |

## 更新记录

### 2026-04-25
- 从混合总清单拆分出 OpenClaw 独立清单。
- 明确 OpenClaw 的流式策略不能由 Hermes 代标完成，需要 OpenClaw 自己审计后更新。

### 2026-04-28
- 已启动 `openclaw` Docker 容器并完成 MiniMax smoke test：容器内 local infer 返回 `ok: true`。
- 已审计 OpenClaw 镜像内流式策略：主模型 OpenAI-compatible completions 参数包含 `stream: true` 与 `stream_options.include_usage`。
- 已确认 inbound gateway 的 `/v1/chat/completions` 与 `/v1/responses` 使用 `Boolean(payload.stream)`，属于客户端兼容协商，不作为上游出站非流式证据。
- 发现 auxiliary 非流式路径：Kimi web search 与 Perplexity web search 都调用 `/chat/completions`，请求体未设置 `stream: true`，并使用 `await res.json()`。因此本项只能标为 `[~]`，不能标 `[x]`。
