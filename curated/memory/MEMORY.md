# friend-001 独立记忆入口

这是 friend-001 的独立长期记忆入口。

## 边界
- 只服务 friend-001 微信会话。
- 不写入 shared/curated/memory，避免污染 Hermes / OpenClaw main 的跨 agent 真相源。
- 稳定事实优先写入本 workspace 的 memory/。
- 运行时产物写入本 workspace 的 runtime/。
- 原始聊天摘要可写入本 workspace 的 inbox/。
- 不保存明文 API key、token、密码、cookie、二维码登录 token。

## 当前状态
- workspace 已初始化。
- 微信绑定与路由待完成。

<!-- SHARED-BRIDGE-STATE:START -->
## 自动生成的共享桥状态块

- 生成时间: `2026-04-30T06:00:02+08:00`
- 共享根目录: `/home/vany/openclaw-data/.openclaw/shared`
- runtime 位置提示: `/home/vany/openclaw-data/.openclaw/shared/runtime`
- facts 文件数: 6
- projects 文件数: 2
- 最近 daily 文件:
  - `inbox/hermes/daily/2026-04-29.md` (inbox/hermes/daily)
  - `compat/daily/dreaming/deep/2026-04-29.md` (compat/daily)
  - `compat/daily/dreaming/rem/2026-04-29.md` (compat/daily)
  - `compat/daily/dreaming/light/2026-04-29.md` (compat/daily)
  - `inbox/openclaw/daily/dreaming/deep/2026-04-29.md` (inbox/openclaw/daily)
- inbox 各 agent 文件计数:
  - `future-agent`: 0
  - `hermes`: 10
  - `openclaw`: 16
<!-- SHARED-BRIDGE-STATE:END -->
