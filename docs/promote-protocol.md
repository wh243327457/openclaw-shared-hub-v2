# inbox → curated 晋升协议

本文定义共享中台 v2 中“原始记录如何晋升为跨 Agent 真相源”的最小治理流程。

## 目标

- `inbox/<agent>/daily/` 保存各 Agent 的原始记录，不直接等同于长期记忆。
- `curated/memory/` 是跨 Agent 真相源，必须经过筛选、去重、脱敏和审核。
- 自动脚本只能生成候选与状态报告，默认不直接写入 curated。
- 详细治理总结机制见 `docs/governance-summary-mechanism.md`：raw 宽进、curated 严出，候选需经过评分、证据、去重、脱敏、人工/总控审查后才能晋升。
- 强制执行标准见 `docs/shared-governance-standard.md`：定义五门准入、标准状态流、决策表、质量阈值和 daily/weekly/monthly 节奏。

## 分层职责

| 区域 | 职责 | 写入者 | 可信度 |
|---|---|---|---|
| `inbox/<agent>/daily/` | 原始记录、观察、草稿、运行摘要 | 各 Agent | 低到中 |
| `curated/memory/facts/` | 稳定事实 | 总控/人工审核后写入 | 高 |
| `curated/memory/projects/` | 项目状态、决策、长期计划 | 总控/人工审核后写入 | 高 |
| `runtime/<agent>/` | 缓存、日志、临时产物 | 各 Agent / 脚本 | 不作为记忆 |

## 晋升状态

候选记录必须处于以下状态之一：

- `candidate`: 候选，等待复核。
- `accepted`: 已采纳，写入 curated。
- `rejected`: 明确拒绝，不进入 curated。
- `deferred`: 暂缓，证据不足或还不稳定。
- `duplicate`: 重复，已有 curated 事实覆盖。

## 候选筛选规则

优先晋升：

- 稳定路径、目录结构、兼容入口。
- 已验证的工具行为、脚本行为、运行方式。
- 用户明确偏好、跨 Agent 协作协议、长期项目状态。
- 已落地的治理规则、验收标准、接入契约。

默认不晋升：

- light sleep、dreams、reflection、未经验证的自我推断。
- 单次执行日志、临时错误、缓存摘要。
- 只对当前会话有效的任务进度。
- 含明文 secret、token、password、API key、连接串的内容。

## 脱敏规则

写入 curated 前必须检查：

- API key / token / password / secret / cookie / private key。
- URL 中的凭证片段。
- 本地配置文件中的敏感字段。

如必须引用，统一写为 `[REDACTED]` 或环境变量名，不写真实值。

## 推荐晋升流程

1. 运行候选扫描：
   - `python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10`
2. 读取候选清单，逐项判断状态。
3. 对 `accepted` 项选择目标文件：
   - 稳定事实 → `curated/memory/facts/*.md`
   - 项目状态 → `curated/memory/projects/*.md`
4. 写入 curated 后更新 `curated/memory/MEMORY.md` 索引或运行 promoter 刷新状态块。
5. 保留晋升日志，格式见 `docs/promote-log-template.md`。
6. 运行验证：
   - `python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10`
   - `python3 scripts/verify_bridge.py`

## Raw 保留与 Git 跟踪边界

`inbox/<agent>/daily/` 是 raw 写入入口，不等于 Git 主线审查面。

- `inbox/**/daily/dreaming/`、`inbox/**/daily/.dreams/`、cache、index、临时摘要默认只保留在本地运行目录，不进入 Git 主线。
- 对已经误入 Git 的 raw bulk，优先使用 `git rm --cached -r <path>` 从 Git index 移除，同时保留本地文件。
- 如 raw 中有长期价值，先提炼摘要或稳定事实，再写入 `curated/memory/facts/` 或 `curated/memory/projects/`。
- 不把整段 raw、score/source 噪声或单次运行日志直接追加到 `curated/memory/MEMORY.md`。

## 自动化边界

`promoter.py` 可以：

- 统计 inbox backlog。
- 扫描候选条目。
- 标记可能的敏感内容风险。
- 给出建议目标路径。
- 刷新 MEMORY.md 自动状态块。

`promoter.py` 不应默认：

- 自动决定事实为真。
- 自动删除 inbox。
- 自动把候选写入 curated。
- 自动覆盖人工维护内容。

## OpenClaw reflection 特别规则

OpenClaw 的 reflection / dreams / light sleep 内容默认只作为灵感或候选，不作为事实。

只有满足以下条件才可晋升：

- 有外部文件、命令输出或人工确认作为证据。
- 内容不含 secret。
- 与现有 curated 事实不冲突。
- 目标文件明确。
