# Hermes 必须项清单

- 创建时间: 2026-04-25
- Agent: Hermes
- 维护位置: `/home/vany/openclaw-data/.openclaw/shared/docs/checklists/agents/hermes-required-items.md`
- 状态规则: `[x]` = Hermes 已完成并有证据；`[ ]` = Hermes 未完成或待验证；`[~]` = Hermes 已部分完成但仍需审计/修复
- 边界: 这里只标记 Hermes 自己的完成状态，不替 OpenClaw / future-agent 标记。

## P0 必须项

| 状态 | Hermes 必须项 | 当前证据 / 路径 | 最近状态 |
|---|---|---|---|
| [x] | Hermes 可读取 shared v2 canonical 分层 | `manifest.yaml`, `AGENTS.md`, `curated/`, `inbox/hermes/`, `runtime/hermes/` | 已验证 |
| [x] | Hermes 共享 skill 入口已接通 | Hermes 配置引用 `shared/skills` | `verify_bridge.py` 通过 |
| [x] | Hermes prefill 入口存在 | `prefill/hermes-shared-memory.json` | 已完成 |
| [x] | Hermes 原始记录默认进入自己的 inbox | `inbox/hermes/daily/` | 已存在 daily 记录 |
| [x] | Hermes runtime 产物有独立目录 | `runtime/hermes/` | 已存在 |
| [x] | Hermes / OpenAI-compatible API 请求必须全部使用流式 `stream=true` | `/root/.hermes/hermes-agent`: `agent/auxiliary_client.py`, `trajectory_compressor.py`, `run_agent.py`, `mini_swe_runner.py`, `tools/mixture_of_agents_tool.py`; 回归测试 `tests/test_openai_stream_enforcement.py`, `tests/agent/test_stream_collection.py` | 2026-04-26 已专项审计并修复辅助/回退链路；`venv/bin/python -m pytest ...` 144 passed |
| [x] | Hermes 不把明文 secret 写入 shared | shared 中只记录变量名/占位符 | 已执行 |

## P1 必须项

| 状态 | Hermes 必须项 | 当前证据 / 路径 | 最近状态 |
|---|---|---|---|
| [x] | Hermes 共享中台维护脚本日志进入 runtime/hermes | `runtime/hermes/cron.log` 等 | 已完成 |
| [x] | Hermes 侧 promoter / verify 可运行 | `scripts/promoter.py`, `scripts/verify_bridge.py` | 已通过 |

## 更新记录

### 2026-04-26
- Hermes 流式请求硬性要求已从 `[~]` 收口为 `[x]`。
- 已覆盖主链路、`auxiliary_client` 同步/异步请求、max_tokens retry、auth refresh、payment/connection fallback、trajectory compressor、mini_swe_runner、mixture_of_agents 工具等 OpenAI-compatible 请求点。
- 验证命令：`cd /root/.hermes/hermes-agent && venv/bin/python -m pytest tests/agent/test_auxiliary_client.py tests/agent/test_stream_collection.py tests/test_openai_stream_enforcement.py tests/test_trajectory_compressor.py tests/test_trajectory_compressor_async.py tests/test_mini_swe_runner.py tests/tools/test_mixture_of_agents_tool.py -q`；结果：144 passed。

### 2026-04-25
- 从混合总清单拆分出 Hermes 独立清单。
- Hermes 的流式请求硬性要求保留为 `[~]`，等待专项审计/修复。
