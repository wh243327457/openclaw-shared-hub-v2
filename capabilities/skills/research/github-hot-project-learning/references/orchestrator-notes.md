# 闭环编排器实战经验

## 架构决策

### 单一任务 vs 多任务

用户明确要求单一 cron 任务完成整个闭环，而非多个分散任务。

**原因**:
- 更容易理解和维护
- 每次执行读取 plan 文件，步骤明确
- 失败时可以从断点继续

**实现**: `github_learning_orchestrator.py` 按顺序执行 4 个步骤。

### OpenClaw 触发方式

```bash
docker exec openclaw openclaw cron run <job-id>
```

- 使用 `openclaw cron run` 而非 `openclaw cron add` 重新创建任务
- 任务 ID 固定：`7aa310ea-b264-40c8-b23a-ed655c565a69`
- 需要检查 OpenClaw 容器状态，未运行时先 `docker start openclaw`

### 等待机制

轮询检查产出文件：
```python
while time.time() - start_time < timeout:
    if output_file.exists() and output_file.stat().st_size > 0:
        return True
    time.sleep(30)
```

超时默认 30 分钟（`OPENCLAW_TIMEOUT = 1800`）。

## 已知问题

### ~~OpenClaw 输出格式不匹配~~（已解决 2026-05-13）

**解决方案**: 修改 OpenClaw 学习任务提示词，要求读取 `instruction.md` 并按模板输出。

```bash
docker exec openclaw openclaw cron edit 7aa310ea-b264-40c8-b23a-ed655c565a69 \
  --message '请按照 Hermes 生成的学习指令执行每日 GitHub 热门项目学习。
## 执行流程
### 第一步：读取学习指令
读取文件：/home/node/.openclaw/shared/runtime/hermes/github-hot-project-learning/instruction.md
### 第二步：执行学习
按照 instruction.md 中的要求执行学习。
### 第三步：按模板输出
严格按照 instruction.md 中「产出要求」的格式输出...'
```

**验证**: 2026-05-13 测试通过，审计得分 16/16，包含所有必需章节。

### 审计评分逻辑

当前使用简单的关键词匹配评分：
- 检查必须章节是否存在
- 检查深读项目数量
- 检查可迁移经验、风险边界等关键词

**待优化**: 应该适配 OpenClaw 的 A/B/C 格式进行评分。

## 测试技巧

```bash
# 只测试指令生成和审计流程（跳过 OpenClaw 学习）
python3 scripts/github_learning_orchestrator.py --skip-openclaw

# 完整测试（需要等待 OpenClaw 学习完成）
python3 scripts/github_learning_orchestrator.py

# 干跑模式
python3 scripts/github_learning_orchestrator.py --dry-run
```

## 微信推送注意事项

- 平台名称: `weixin`（不是 `wechat`）
- 限流间隔: 5-10 分钟
- 备用方案: 写入 `wechat-push-YYYY-MM-DD.txt`
- 详见 `openclaw-integration.md` 的「微信推送集成」章节
