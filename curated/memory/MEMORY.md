# MEMORY.md

这是 **共享中台 v2** 的跨 agent 长期记忆主索引。

## 根路径

- 宿主：`/home/vany/openclaw-data/.openclaw/shared`
- 容器：`/home/node/.openclaw/shared`

## 作用范围

`curated/memory/` 是 **跨 agent 真相源**，只保留稳定、重要、后续大概率还会复用的信息。

- 事实片段：`curated/memory/facts/`
- 项目状态：`curated/memory/projects/`
- 兼容入口：`shared/memory/MEMORY.md`（symlink 到本文件）

## 目录索引

- **长期记忆主索引**：`curated/memory/MEMORY.md`
- **稳定事实**：`curated/memory/facts/`
- **项目状态目录**：`curated/memory/projects/`
- **当前项目条目**：`curated/memory/projects/shared-hub-v2.md`
- **共享技能清单**：`capabilities/manifests/shared-skills.yaml`
- **旧 OpenClaw daily 兼容视图**：`compat/daily/`（可通过 `memory/daily/` 访问）
- **agent 原始写入**：`inbox/<agent>/daily/`
- **运行时产物**：`runtime/<agent>/`

## 写入规则

- 只有经过整理和验证的长期信息才进入 `curated/memory/`
- agent 原始记录默认进入 `inbox/<agent>/daily/`
- `.dreams`、cache、index、临时摘要等运行时产物进入 `runtime/<agent>/`
- 避免在本文件中写入明文 secret

## 当前状态

- `shared-hub-v2` 项目状态已沉淀到 `curated/memory/projects/shared-hub-v2.md`
- `capabilities/manifests/shared-skills.yaml` 已建立，用于声明常驻 shared 的共享技能
- `curated/memory/facts/` 目前仍为空，后续可按需补充稳定事实条目
- 后续新增长期记忆时，请同时更新本索引

<!-- SHARED-BRIDGE-STATE:START -->
## 自动生成的共享桥状态块

- 生成时间: `2026-04-15T11:01:41+08:00`
- 共享根目录: `/home/vany/openclaw-data/.openclaw/shared`
- runtime 位置提示: `/home/vany/openclaw-data/.openclaw/shared/runtime`
- facts 文件数: 0
- projects 文件数: 1
- 最近 daily 文件:
  - `inbox/hermes/daily/2026-04-15.md` (inbox/hermes/daily)
  - `compat/daily/2026-04-15.md` (compat/daily)
  - `compat/daily/2026-04-14.md` (compat/daily)
- inbox 各 agent 文件计数:
  - `future-agent`: 0
  - `hermes`: 1
  - `openclaw`: 0
<!-- SHARED-BRIDGE-STATE:END -->
