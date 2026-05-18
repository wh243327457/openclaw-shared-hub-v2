# runtime retention 策略

共享中台 v2 的 runtime 层只保存运行时产物，不作为长期事实源。retention 的目标是控制体积和风险，但默认只报告，不自动删除。

## 适用范围

仅适用于：

- `runtime/hermes/`
- `runtime/openclaw/`
- `runtime/future-agent/`

不适用于：

- `curated/`
- `inbox/`
- `compat/`
- `capabilities/`
- `prefill/`

## 默认策略

- verify 只报告 runtime 各 agent 目录大小。
- daily maintenance 只记录 shared 总体大小。
- 默认不删除任何文件。

## 建议保留周期

- `logs/`：保留 30-90 天，视排障需要决定。
- `cache/`：可按大小上限清理，默认先人工确认。
- `tmp/`：可短期保留，建议 7-14 天后人工清理。
- `.dreams` / reflections：默认视为低置信运行时材料，不晋升 curated；需要人工摘录证据后再进入 inbox 或 curated。

## 清理前检查

清理 runtime 前必须确认：

1. 目标路径确实位于 `shared/runtime/<agent>/` 下。
2. 不包含 curated / inbox / compat / capabilities。
3. 无明文 secret 需要单独安全处理。
4. 清理命令先 dry-run 输出候选列表。
5. 用户确认后再删除。

## 推荐 dry-run 命令

```bash
cd <shared-root>
find runtime -type f -mtime +90 -print
```

## 禁止事项

- 禁止自动删除 curated 事实。
- 禁止自动删除 inbox 原始记录。
- 禁止把 runtime 内容直接当作 source of truth。
- 禁止在未确认路径的情况下执行递归删除。
