# 2026-06-02 OpenClaw 模型级联失败完整记录

## 概要

2026-06-02 GitHub 热门项目每日学习闭环因 OpenClaw cron job 模型问题未能完成。Hermes cron job（`github_learning_orchestrator.py`）首次运行在 300s 内超时（Step 1 成功，Step 2 OpenClaw 等待超时）。随后手动分步执行，依次尝试 6+ 个模型，最终 `minimax/MiniMax-M3`（timeout=1800s）和 `minimax/MiniMax-Text-01`（timeout=1800s）均未能成功产出文件。

## 时间线（CST / UTC+8）

| 时间 | 事件 | 结果 |
|------|------|------|
| 07:35 | Hermes cron 触发 `github_learning_orchestrator.py` | Step 1 ✅ (指令已生成), Step 2 等待超时 |
| 07:36 | `--skip-openclaw` 模式重跑，指令生成成功 | 审计失败（无产出文件） |
| 07:36 | 确认 OpenClaw 容器 running | OK |
| 07:36 | 手动触发 `openclaw cron run`（原始模型 MiniMax-M2.7） | ❌ 模型不在 allowlist |
| 07:37 | 改模型为 `minimax/MiniMax-M3`，timeout=600s | ❌ 超时 556s |
| 07:38 | 改模型为 `deepseek/deepseek-v4-flash` | ❌ 401 API key 无效 |
| 07:39 | 改模型为 `mimo/MiMo-V2.5-Pro` | ❌ 401 API key 无效 |
| 07:40 | 改模型为 `openai/gpt-5.2` | ❌ `hasBeforeToolCallPolicy is not a function` |
| 07:41 | 改模型为 `self/gpt-5.4` | ❌ 403 Forbidden |
| 07:42 | 改模型为 `minimax/MiniMax-Text-01`，timeout=1800s | ⚠️ status: ok 但未写入文件 |
| 07:44 | 改模型为 `minimax/MiniMax-M3`，timeout=1800s | 运行中（最后状态） |

## 详细错误分析

### 1. `minimax/MiniMax-M2.7` — Allowlist 移除

```
cron payload.model 'minimax/MiniMax-M2.7' rejected by agents.defaults.models allowlist:
minimax/MiniMax-M2.7 is not in [deepseek/deepseek-v4-flash, deepseek/deepseek-v4-pro,
mimo/MiMo-V2-Pro, mimo/MiMo-V2.5, mimo/MiMo-V2.5-Pro, minimax/MiniMax-M3,
minimax/MiniMax-Text-01, openai/codex-mini-latest, openai/gpt-5-codex,
openai/gpt-5.1-codex, openai/gpt-5.1-codex-max, openai/gpt-5.1-codex-mini,
openai/gpt-5.2, openai/gpt-5.2-codex, openai/gpt-5.3-codex, self/gpt-5.4,
self/gpt-5.4-mini]
```

**影响**：这是之前唯一成功完成过此任务的模型（2026-06-01 成功，耗时 424s）。

### 2. `minimax/MiniMax-M3` — 超时（600s 不够）

```
cron: job execution timed out (last phase: model-call-started)
durationMs: 555968 (~9.3 min)
```

**修复**：`--timeout-seconds 1800`。

### 3. `minimax/MiniMax-Text-01` — 成功但不使用工具

```
status: ok
durationMs: 52248 (~52s)
output_tokens: 2185
```

**诊断**：agent 完成了推理（"Step 1: Read the Learning Instructions"、"Step 2: Execute Learning"），但只返回了文本摘要，没有实际调用 write_file 工具写入 `inbox/openclaw/daily/2026-06-02.md`。该模型可能不支持或未正确配置工具调用。

**教训**：cron run `status: ok` 不代表产出已写入文件。必须检查 inbox 文件是否存在。

### 4. `deepseek/deepseek-v4-flash` — API key 失效

```
FailoverError: HTTP 401: Authentication Fails, Your api key: ****755d is invalid
```

### 5. `mimo/MiMo-V2.5-Pro` — API key 失效

```
FailoverError: HTTP 401: Invalid API Key
```

### 6. `openai/gpt-5.2` — OpenClaw 内部错误

```
TypeError: (0 , _agentHarnessRuntime.hasBeforeToolCallPolicy) is not a function
```

可能与 OpenClaw 版本 `2026.5.12` 的兼容性有关。

### 7. `self/gpt-5.4` — 自托管模型 403

```
FailoverError: 403 status code (no body)
```

## 根因总结

1. **MiniMax-M2.7 从 allowlist 移除** — 配置变更未同步到 cron job
2. **DeepSeek / MiMo API key 过期** — 多个 provider 同时不可用
3. **MiniMax-Text-01 不支持工具调用** — 可用但不适合需要工具的任务
4. **OpenAI 版本兼容问题** — `hasBeforeToolCallPolicy` 错误

## 修复措施

1. 将 cron job 模型改为 `minimax/MiniMax-M3`
2. 将 timeout 从 600s 增加到 1800s
3. 需要用户更新 DeepSeek / MiMo API key
4. 可能需要更新 OpenClaw 版本以修复 OpenAI 兼容问题

## 诊断命令速查

```bash
# 查看 cron job 当前配置
docker exec openclaw openclaw cron list

# 查看最近运行历史
docker exec openclaw openclaw cron runs --id <job-id> --limit 3

# 查看 allowlist
docker exec openclaw openclaw config get agents.defaults.models

# 修改模型和超时
docker exec openclaw openclaw cron edit <job-id> --model "minimax/MiniMax-M3" --timeout-seconds 1800

# 手动触发
docker exec openclaw openclaw cron run <job-id>

# 检查产出文件
ls -la /home/vany/agent/shared/inbox/openclaw/daily/YYYY-MM-DD.md
# 容器内路径：
docker exec openclaw ls -la /home/node/.openclaw/shared/inbox/openclaw/daily/YYYY-MM-DD.md
```
