# compat daily legacy entry

本目录是旧 OpenClaw `shared/memory/daily/` 的兼容入口，不是真相源。

## 规则

- 新的 OpenClaw 原始 daily 写入应使用：`inbox/openclaw/daily/`。
- 旧 daily 文件可在本地保留，用于兼容旧 workspace 读取。
- `dreaming/`、`.dreams`、cache、index、临时摘要等运行时产物不得纳入 Git 跟踪。
- `.dreams` 应指向：`../../runtime/openclaw/dreams`。
- 长期稳定事实必须晋升到：`curated/memory/`，并更新 `curated/memory/MEMORY.md`。

## Git 跟踪策略

Git 只跟踪本 README 和必要的兼容入口说明；历史 bulk 文件保留在本地运行目录，但不进入仓库快照。
