# Input Detection False Negative — 2026-05-30 & 2026-06-01

## 2026-05-30 事件

2026-05-30 12:00 scheduled run 声称"无新日报输入"并降级为 runtime-only 巡检。
但实际数据：

- `inbox/openclaw/daily/2026-05-30.md`：mtime=08:33 UTC+8，内容为完整 GitHub 热门项目日报（10 个项目 + 深读分析）
- `inbox/hermes/daily/2026-05-30.md`：mtime=07:30 UTC+8，内容为 Hermes 健康状态

文件在 run 执行前 3.5 小时就已存在且非空。

**根因**：run 的输入检测逻辑只检查文件是否存在，没有验证 mtime 和非空。
**性质**：run 本身有 bug（文件已存在但漏检）。

## 2026-06-01 事件（跨 run 时序变体）

2026-06-01 00:05 run 声称"无新日报输入"——当时是正确的（openclaw daily 在 08:36 才写入）。
2026-06-01 12:00 run 做三步检测时发现 openclaw daily 已存在且有 312 行新鲜内容。

**关键区别**：
- 2026-05-30：文件在 run 之前存在，run 漏检 → run 有 bug
- 2026-06-01：文件在 run 之后才写入，run 当时无输入 → 时序正确但结论过期

**纠正措辞**：desync_findings 应写"00:05 run was correct AT THAT TIME (file didn't exist yet), but 12:00 run has fresh input"。不要写成"00:05 run 错误宣称"——当时确实没有。

**附加发现**：00:05 run 还声称"微信推送 85+ 次连续失败"，但 `weixin-push-guard.json` 显示 `last_rate_limited_at=2026-05-17`、`last_push_at=2026-05-30`，guard 状态健康。WeChat push guard 文件是 rate-limiting 的权威来源，优先于 run notes 中的推断。

## 正确的检测流程

```bash
# 1. 文件存在性
test -f "inbox/openclaw/daily/$(date +%Y-%m-%d).md" && echo EXISTS

# 2. mtime 在今天内（或在本轮 run 时间窗口内）
stat -c %Y "inbox/openclaw/daily/$(date +%Y-%m-%d).md"  # 与当前时间戳比较

# 3. 非空
test -s "inbox/openclaw/daily/$(date +%Y-%m-%d).md" && echo NON_EMPTY
```

三步全通过才能判定"有新输入"。任一步失败才可降级为"无新输入"。

## 跨 run 纠正的权威来源优先级

当 run notes 声称某状态（如 rate limiting、consecutive failures）但对应的状态文件显示不同数据时：
1. **状态文件是权威来源**（weixin-push-guard.json、delivery-state.json 等）
2. Run notes 是推断/观察，可能基于过期数据或间接证据
3. 如果两者矛盾，在 desync_findings 中列出并以状态文件为准

## 相关教训

- Lesson #22：三步验证要求
- Lesson #24：新 run 必须纠正前轮事实错误
- Lesson #28：跨 run 时序纠正措辞规范
