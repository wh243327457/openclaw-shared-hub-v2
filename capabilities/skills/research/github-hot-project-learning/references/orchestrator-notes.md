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

## 已知 Bug（2026-05-21）

### Bug 1：审计得分比较类型错误

**文件**: `scripts/github_learning_orchestrator.py`，约 L527

**问题**: `PASS_SCORE` 从配置读取时为字符串（`"16"`），但与整数比较时未转换。

```python
# 错误（PASS_SCORE 是 str，score 是 int）
if score >= PASS_SCORE:

# 正确
if score >= int(PASS_SCORE):
```

**影响**: 审计判定永远失败（`"16" >= 16` 在 Python 中为 `False`），即使得分满分 16，审计也被判定为失败，导致知识库更新和微信推送被跳过。

**症状**: orchestrator 输出显示 `audit_score=16` 但 `audit_pass=False`。

**修复**: 在 `load_config()` 中将 `pass_score` 转换为 int，或在比较处强制转换。

### Bug 2：来源表 key 不匹配

**文件**: `scripts/github_learning_orchestrator.py`，约 L447

**问题**: YAML frontmatter 用 `source`（单数），但 `get_source()` 查询时用 `sources`（复数）。

```python
# frontmatter（单数）
source: xxx

# 代码（复数）
sources = get_source(row["sources"])  # 查不到，返回 "unknown"
```

**影响**: 微信推送消息中所有项目的来源列都显示为 `unknown`，即使来源已正确记录在 frontmatter 中。

**修复**: 统一为 `source`（单数）或 `sources`（复数）。

### Bug 3：PASS_SCORE 空值防御

**文件**: 同上，`load_config()` 函数

**问题**: 如果 `config.yaml` 中 `pass_score` 字段为空或不存在，`config.get("pass_score", 16)` 返回 `None`，后续 `int(None)` 会抛 `TypeError`。

**修复**:
```python
pass_score = config.get("pass_score", 16)
PASS_SCORE = int(pass_score) if pass_score is not None else 16
```

## 微信推送注意事项

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
