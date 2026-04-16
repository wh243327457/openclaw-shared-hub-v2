---
name: shared-memory-bridge
description: 跨 Hermes / OpenClaw / future agent 的共享中台 v2 入口
version: "2.0"
agent: hermes, openclaw, future
---

# shared-memory-bridge

跨 agent 共享记忆与共享能力的统一入口 skill。

## 共享根目录

- 宿主：`/home/vany/openclaw-data/.openclaw/shared/`
- 容器：`/home/node/.openclaw/shared/`

## 新分层

```text
shared/
├── curated/memory/           # 跨 agent 真相源
├── inbox/<agent>/daily/      # agent 原始写入
├── runtime/<agent>/          # 运行时产物
├── capabilities/skills/      # 共享 skills 实际位置
├── compat/daily/             # 旧 OpenClaw daily 兼容层
├── memory/                   # legacy memory 入口
├── skills/                   # legacy skills 入口
└── prefill/                  # 预填充消息
```

## 读取顺序建议

1. **先读 manifest** → `shared/manifest.yaml`
2. **再读共享治理** → `shared/AGENTS.md`
3. **再读长期真相** → `shared/curated/memory/MEMORY.md`
4. **按需读稳定事实** → `shared/curated/memory/facts/`
5. **按需读项目状态** → `shared/curated/memory/projects/`
6. **兼容旧 OpenClaw 日志** → `shared/memory/daily/`（实际为 `shared/compat/daily/`）
7. **查看 agent 原始写入** → `shared/inbox/<agent>/daily/`
8. **仅调试时读取 runtime** → `shared/runtime/<agent>/`

## 写入规范

### Curated（长期稳定）
经过验证、需要跨 agent 共享的长期信息，写入：
- `shared/curated/memory/facts/`
- `shared/curated/memory/projects/`
- 并同步更新 `shared/curated/memory/MEMORY.md`

### Inbox（原始写入）
默认新的 agent 原始记录写入：
- `shared/inbox/hermes/daily/YYYY-MM-DD.md`
- `shared/inbox/openclaw/daily/YYYY-MM-DD.md`
- `shared/inbox/future-agent/daily/YYYY-MM-DD.md`

### Runtime（运行时产物）
`.dreams`、cache、index、临时摘要等运行时产物必须写入：
- `shared/runtime/hermes/`
- `shared/runtime/openclaw/`
- `shared/runtime/future-agent/`

OpenClaw 旧路径兼容保留：
- `shared/memory/daily/.dreams` 会通过兼容链路落到 `shared/runtime/openclaw/dreams/`
- 不要把 `.dreams` 再留在 curated 或 compat 的真实目录中

## 共享 skill 升格规则

- 新沉淀的 skill，先判断它是“当前 agent 本地长期能力”还是“跨 agent 共享能力”
- 若该 skill 会被 Hermes / OpenClaw / future-agent 复用，或属于共享中台、共享记忆、进度汇报、调研协作等横切能力，则同步到 `shared/capabilities/skills/`
- 升格到 shared 时，除了复制完整 skill 目录（`SKILL.md`、`templates/`、`references/`、`scripts/`、`assets/`），还要更新 `shared/capabilities/manifests/shared-skills.yaml`
- 若明确只保留本地，也要在结论里写清楚：当前仅本地长期，不是 shared 长期能力

## 兼容入口

| 旧入口 | 实际目标 |
|---|---|
| `shared/skills/` | `shared/capabilities/skills/` |
| `shared/memory/MEMORY.md` | `shared/curated/memory/MEMORY.md` |
| `shared/memory/facts/` | `shared/curated/memory/facts/` |
| `shared/memory/projects/` | `shared/curated/memory/projects/` |
| `shared/memory/daily/` | `shared/compat/daily/` |

重要实现细节：
- `shared/memory/` **本身保留为真实目录**，不要把整个 `memory/` 做成 symlink
- 兼容性通过目录内关键入口的 symlink 实现：`MEMORY.md`、`facts/`、`projects/`、`daily/`
- `shared/compat/daily/.dreams` 应 symlink 到 `shared/runtime/openclaw/dreams/`
- 校验脚本也应按这个模型检查；不要误要求 `shared/memory` 整体必须是 symlink

## 运行与验证

### 当用户要“按当前情况和进度重新整理一版”时

不要只做概念说明，按**现状审计 → 落盘沉淀 → 脚本复核**执行：

1. **先读真相源**
   - `shared/manifest.yaml`
   - `shared/AGENTS.md`
   - `shared/curated/memory/MEMORY.md`
2. **再审计真实文件状态**
   - 检查 canonical 目录是否齐全：`curated/`、`inbox/`、`runtime/`、`capabilities/`、`compat/`
   - 检查兼容入口及 symlink：`memory/MEMORY.md`、`memory/facts`、`memory/projects`、`memory/daily`、`skills`、`compat/daily/.dreams`
   - 同时确认 `scripts/promoter.py`、`scripts/verify_bridge.py` 是否存在
3. **把结果分两层落盘**
   - 稳定项目状态写到 `shared/curated/memory/projects/<project>.md`
   - 本次会话原始记录写到 `shared/inbox/hermes/daily/YYYY-MM-DD.md`
4. **同步主索引**
   - 更新 `shared/curated/memory/MEMORY.md`，让它显式指向新项目条目
5. **最后跑脚本复核**
   - 先 `promoter.py --dry-run`
   - 再正式跑 `promoter.py`
   - 最后 `verify_bridge.py`

经验结论：这种场景下，**本地 shared 文件才是真相源**，不要把“是否还记得昨天聊过什么”误解成只能靠 session_search；如果聊天检索没有命中，也应回到本地 `manifest.yaml / AGENTS.md / curated/memory/MEMORY.md` 取证。

完成迁移或修复后，至少执行：

```bash
python3 /home/vany/openclaw-data/.openclaw/shared/scripts/promoter.py --dry-run
python3 /home/vany/openclaw-data/.openclaw/shared/scripts/promoter.py
python3 /home/vany/openclaw-data/.openclaw/shared/scripts/verify_bridge.py
```

期望结果：
- `promoter.py` 能更新 `shared/curated/memory/MEMORY.md` 中的自动状态块
- `verify_bridge.py` 返回 exit code 0，且 JSON 中 `ok: true`
- Hermes 仍引用 `shared/skills` 与 `shared/prefill/hermes-shared-memory.json`
- OpenClaw 仍引用 `/home/node/.openclaw/shared/skills`
- 各 workspace 的 `memory` / `MEMORY.md` / `shared` 入口仍可解析

## Secrets 安全规范

- **默认不要**将任何明文 secret（API key、token、密码等）写入 shared
- 如需引用 secret，用变量名占位（如 `$OPENCLAW_API_KEY`）
- 各 agent 的 `.env` / credential 文件保持在各自 agentDir 下
