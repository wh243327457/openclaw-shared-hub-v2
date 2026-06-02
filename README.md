# OpenClaw / Hermes 共享中台 v2

> 让 Hermes、OpenClaw workspaces、未来 agent 共享同一套能力层，同时把“长期真相 / 原始写入 / 运行时产物”分层隔离。

## 统一存放目录规范

共享中台本体推荐统一放在每台宿主机的：

```text
~/agent/shared
```

也就是：

```bash
mkdir -p ~/agent
git clone <repo> ~/agent/shared
export SHARED_HUB_ROOT="$HOME/agent/shared"
```

重要边界：共享中台本体不应该放在 `runtime/` 目录里。`runtime/` 是共享根内部的机器本地临时产物层，用来放 cache、dreams、index、运行中间文件；共享中心根目录应是 `~/agent/shared` 这种稳定目录。

如果某台机器无法使用 `~/agent/shared`，可以把 shared hub clone 到任意目录，但必须显式设置：

```bash
export SHARED_HUB_ROOT=/your/custom/shared/path
```

解析顺序与最小保留集见 `manifest.yaml: deployment` 段与 `capabilities/skills/foundation/path-portability/SKILL.md`。

## 新机器快速接入

```bash
mkdir -p ~/agent
git clone https://github.com/wh243327457/openclaw-shared-hub-v2.git ~/agent/shared
cd ~/agent/shared
python3 scripts/bootstrap_shared_root.py
python3 scripts/resolve_shared_root.py --check
python3 scripts/verify_bridge.py --portable-only
python3 scripts/audit_portability.py
```

建议把下面两行加入 shell rc：

```bash
export SHARED_HUB_ROOT="$HOME/agent/shared"
export AGENTS_SHARED_ROOT="$SHARED_HUB_ROOT"
```

## 关键目录

| 路径 | 用途 |
|---|---|
| `curated/memory/` | 跨 agent 真相源，只放稳定记忆 |
| `inbox/<agent>/daily/` | agent 原始写入、草稿、待整理上下文 |
| `runtime/<agent>/` | 机器本地运行时产物，如 dreams / cache / index；不是共享根 |
| `capabilities/skills/` | 共享 skills 实际存放位置 |
| `compat/daily/` | 旧 OpenClaw 日志兼容视图 |
| `memory/` | legacy memory 入口，保留旧路径兼容 |
| `skills/` | legacy skills 入口，实际链接到 `capabilities/skills/` |
| `prefill/` | 各 agent 的预填充消息 |

## 兼容性

当前配置无需修改：
- Hermes 仍可从 `shared/skills/` 加载共享 skills
- Hermes 仍可从 `shared/prefill/hermes-shared-memory.json` 读取预填充
- 旧 OpenClaw workspace 仍可通过 `shared/memory/MEMORY.md`、`shared/memory/daily/`、`shared/skills/` 访问共享层

其中：
- `shared/skills -> capabilities/skills`
- `shared/memory/MEMORY.md -> curated/memory/MEMORY.md`
- `shared/memory/facts -> curated/memory/facts`
- `shared/memory/projects -> curated/memory/projects`
- `shared/memory/daily -> compat/daily`
- `shared/memory/daily/.dreams -> runtime/openclaw/dreams`（经由 `compat/daily/.dreams`）

## 读写建议

### 读取
1. 先用 `python3 scripts/resolve_shared_root.py` 获取共享根
2. 再读 `<root>/manifest.yaml`
3. 再读 `<root>/AGENTS.md`
4. 再读 `<root>/curated/memory/MEMORY.md`
5. 按需读 `<root>/curated/memory/facts/`、`<root>/curated/memory/projects/`
6. 兼容旧 OpenClaw 日志时，再读 `<root>/memory/daily/`
7. 查看 agent 原始记录时，读 `<root>/inbox/<agent>/daily/`

### 写入
- 稳定事实 / 项目状态：写 `curated/memory/`
- agent 原始写入：写 `inbox/<agent>/daily/`
- 运行时产物：写 `runtime/<agent>/`
- 不要把 `.dreams`、cache、索引、临时摘要留在 curated 或 compat 的真实目录里

## 共享 skill 治理

- 跨 agent 会重复复用的 skill，不要只留在单个 agent 本地目录
- 共享 skill 的真实目录是 `capabilities/skills/`，兼容入口仍可从 `skills/` 读取
- 升格为 shared skill 时，除了复制 skill 目录本身，还要更新 `capabilities/manifests/shared-skills.yaml`
- 若某 skill 明确只服务当前 agent，本地保留即可，但应在产出里说明“未进入共享层”

## 安全规则

- 默认禁止把明文 secrets 写入 shared
- 如需引用 secret，请只写环境变量名或占位符

## 跨机器迁移

shared hub v2 已被设计为可在不同机器之间搬运。最小保留集与逐步迁移清单见：

- `manifest.yaml: deployment.portable.must_preserve`
- `capabilities/skills/foundation/path-portability/references/migration-checklist.md`
