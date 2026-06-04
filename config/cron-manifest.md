# Cron 自动化任务管理

## 真相源

**唯一权威**: `shared/config/cron-jobs.json`

所有自动化任务的定义都在这个文件里。Hermes 启动时从这里读取。

## 文件结构

```
shared/config/
├── cron-jobs.json        ← 唯一真相源，所有 job 定义在这里
├── cron-manifest.md      ← 本文件，说明文档
└── cron-templates/       ← job 模板（可选）
```

## 自定义 Job 路径

用户自定义的 job 在 `cron-jobs.json` 中标记 `"owner": "user"`。

系统内置 job 标记 `"owner": "system"`。

新增自定义 job：用 `cron_manager.py add` 或直接编辑 `cron-jobs.json`。
删除 job：必须用 `cron_manager.py remove`（需要确认）。

## Job 定义格式

```json
{
  "id": "唯一ID",
  "name": "任务名称",
  "schedule": "cron 表达式或间隔（如 '0 9 * * *' 或 '30m'）",
  "prompt": "任务指令",
  "deliver": "local,weixin",
  "enabled": true,
  "owner": "user|system",
  "skills": [],
  "script": "",
  "no_agent": false,
  "workdir": "",
  "description": "一句话说明这个 job 做什么"
}
```

## 管理工具

```bash
# 列出所有 job
python3 scripts/cron_manager.py list

# 添加 job
python3 scripts/cron_manager.py add --name "任务名" --schedule "0 9 * * *" --prompt "做某事"

# 删除 job（需要确认）
python3 scripts/cron_manager.py remove --id <job_id>

# 同步到 Hermes（自动）
python3 scripts/cron_manager.py sync

# 检查 Hermes 与 shared hub 的差异
python3 scripts/cron_manager.py diff
```

## 同步协议

1. **新增**: 写入 `cron-jobs.json` → `sync` 自动推送到 Hermes
2. **修改**: 编辑 `cron-jobs.json` → `sync` 自动更新 Hermes
3. **删除**: `remove` 命令需用户确认 → 更新 `cron-jobs.json` → `sync` 自动移除 Hermes job
4. **冲突**: 以 `cron-jobs.json` 为准，Hermes 本地的未同步 job 会提醒用户处理
