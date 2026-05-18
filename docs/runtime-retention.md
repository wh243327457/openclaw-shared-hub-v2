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
- Git 主线默认不继续新增 runtime / dreams / cache / index / log 等 bulk 文件；如需长期保留，应先摘录成 curated facts/projects 或 docs 摘要。

## Git 跟踪边界

`runtime/` 是本地运行态，默认永不进入 Git 主线；`inbox/` 是 raw 写入入口，默认也不应承载无限增长的 dreaming/raw bulk；`compat/` 是兼容视图，默认只保留薄入口和说明。

允许进入 Git 主线的内容：

- `curated/` 下经过验证的长期事实与项目状态。
- `capabilities/` 下跨 agent 共享 skill 与 manifest。
- 核心 `docs/`、`scripts/`、`tests/`。
- 必要的 symlink 兼容入口与 `prefill/`。

不应继续新增进入 Git 主线的内容：

- `runtime/**`
- `inbox/**/daily/dreaming/**`
- `inbox/**/daily/.dreams/**`
- `compat/daily/dreaming/**`
- `compat/daily/.dreams/**`

历史上已经被跟踪的 bulk 文件在瘦身迭代中分阶段处理：先加 ignore 防新增，再单独 PR 用 `git rm --cached` 从跟踪层移除并保留本地文件。

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
