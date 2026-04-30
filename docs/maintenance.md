# 共享中台维护说明

本文定义 `scripts/daily_maintenance.sh` 的执行边界，避免共享中台自检与外部知识库同步互相影响。

## 默认行为

```bash
cd /home/vany/openclaw-data/.openclaw/shared
scripts/daily_maintenance.sh
```

默认执行：

1. `scripts/promoter.py` 刷新 `curated/memory/MEMORY.md` 自动状态块。
2. `scripts/verify_bridge.py` 执行桥接健康检查。
3. 记录磁盘使用、shared 目录大小、inbox backlog。
4. 如未显式禁用，执行 `scripts/kb_git_sync.sh` 做本地知识库同步。

## 推荐模式

### 只检查 shared，不触发知识库同步

```bash
SHARED_ONLY=1 scripts/daily_maintenance.sh
```

### 干跑模式

```bash
DRY_RUN=1 scripts/daily_maintenance.sh
```

干跑模式只做无副作用检查：

- promoter 使用 `--dry-run`
- verify 正常读取检查
- 不执行 KB git sync

### 关闭 KB sync

```bash
RUN_KB_SYNC=0 scripts/daily_maintenance.sh
```

## 日志位置

- 主日志：`runtime/hermes/cron.log`
- promoter 日志：`runtime/hermes/promoter-cron.log`
- verify 日志：`runtime/hermes/verify-cron.log`
- KB sync 日志：`runtime/hermes/kb_sync.log`

## 失败策略

- promoter / verify / KB sync 的失败会写入主日志。
- 单项失败不应阻止后续监控信息写入。
- verify 失败代表共享中台健康度下降，应优先排查。

## 安全边界

- 维护脚本不应写入明文 secret。
- 维护脚本不应自动修改 curated 中的人工事实内容。
- 自动晋升长期记忆必须保持关闭；晋升只通过 `docs/promote-protocol.md` 的人工 / 总控审核流程。
