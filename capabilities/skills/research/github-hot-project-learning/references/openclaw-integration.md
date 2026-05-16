# OpenClaw 集成模式

## 修改 OpenClaw 学习任务提示词

OpenClaw 的 cron 任务提示词存储在容器内的 `/home/node/.openclaw/cron/jobs.json`。

### 查看当前任务配置

```bash
docker exec openclaw cat /home/node/.openclaw/cron/jobs.json 2>/dev/null | head -100
```

### 修改任务提示词

```bash
docker exec openclaw openclaw cron edit <job-id> --message '新的提示词内容'
```

示例（GitHub 学习任务）：
```bash
docker exec openclaw openclaw cron edit 7aa310ea-b264-40c8-b23a-ed655c565a69 --message '请按照 Hermes 生成的学习指令执行...'
```

### 手动触发任务执行

```bash
docker exec openclaw openclaw cron run <job-id>
```

### 查看任务执行状态

```bash
docker exec openclaw openclaw cron list 2>/dev/null
```

状态说明：
- `ok`: 执行成功
- `error`: 执行失败
- `running`: 执行中

## OpenClaw 学习任务 ID

| 任务 | ID |
|------|-----|
| GitHub 热门项目每日学习 | `7aa310ea-b264-40c8-b23a-ed655c565a69` |

## 用户核心偏好

**"Hermes 安排学习，OpenClaw 只做学习和沉淀"**

- Hermes 负责：生成指令、定义格式、审计质量、反馈改进
- OpenClaw 负责：按指令执行学习、按格式输出

## 测试技巧

使用 `--skip-openclaw` 参数测试编排器流程，避免等待 30 分钟：

```bash
python3 scripts/github_learning_orchestrator.py --skip-openclaw
```

## 微信推送集成

### 发送消息

使用 `send_message` 工具，平台名称为 `weixin`（不是 `wechat`）：

```python
send_message(action='send', target='weixin', message='推送内容')
```

可用 target 列表：`send_message(action='list')` 返回 `weixin:o9cq801zk7qTYT_A2Z9JkDumupX8@im.wechat (dm)`

### 限流处理

iLink sendmessage 可返回 `ret=-2 errcode=None errmsg=rate limited`。
- 间隔 5-10 分钟再发
- 或写入 `shared/runtime/hermes/github-hot-project-learning/wechat-push-YYYY-MM-DD.txt` 备用

### CLI 方式（不可用）

`hermes send` 命令不存在，不要使用。只能通过 `send_message` 工具或 cron delivery 推送。

## Hermes Cron 创建

创建 cron 任务时必须提供 `prompt` 或 `skill`，不支持 `script`：

```python
cronjob(action='create', name='任务名', schedule='30 7 * * *', prompt='执行步骤...')
```

## 常见问题

### OpenClaw 学习超时

**症状**: 任务状态为 `error`，日志显示 `timeout`

**原因**: 网络问题导致 web_fetch 失败，模型超时

**解决**: 
1. 检查网络连接
2. 检查 OpenClaw 容器日志: `docker logs openclaw --tail 50`
3. 如果持续失败，考虑增加 timeoutSeconds

### OpenClaw 输出格式不匹配

**症状**: 审计时因格式不匹配被判定为缺失章节

**原因**: OpenClaw 的实际输出格式与模板期望格式不同

**解决**: 
1. 修改 OpenClaw 学习任务提示词，明确指定输出格式
2. 在提示词中列出所有必需章节
