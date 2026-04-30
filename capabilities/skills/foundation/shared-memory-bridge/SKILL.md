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

## 维护收口实操

### 前置检查清单（批量执行前必做）

不要直接动手，先并行确认环境状态，避免做到一半发现网络/服务/工具不可用：

```bash
# 1. gateway 依赖与服务状态
/root/.hermes/hermes-agent/venv/bin/python3 -c "import websockets" 2>/dev/null && echo "websockets ok" || echo "websockets missing"
systemctl status hermes-gateway.service --no-pager 2>/dev/null | head -3

# 2. GitHub 网络与认证
curl -sI https://github.com | head -1
gh auth status 2>/dev/null | head -3

# 3. Claude Code 可用性（如需分派编码任务）
claude --version 2>/dev/null || echo "Claude Code unavailable"

# 4. shared 脚本完整性
ls scripts/promoter.py scripts/verify_bridge.py 2>/dev/null || echo "scripts missing"
```

### 本地 shared Git 状态判定口径

当用户问“共享中台有没有 Git / 远端 / 推送”时，必须区分两层，不要只检查 live shared 后就下绝对结论：

1. **live shared 运行目录**
   - 路径：`/home/vany/openclaw-data/.openclaw/shared`
   - 这是 OpenClaw / Hermes 实际读取和写入的共享中台目录
   - 可能不是 Git 仓库；若没有 `.git`、remote、branch，只能说明 live 目录没有直接 Git 化

2. **runtime staging Git 仓库**
   - 典型路径：`/home/vany/openclaw-data/.openclaw/shared/runtime/hermes/pr-staging/openclaw-shared-memory-v2/`
   - 这是把 shared 可审阅内容整理成 GitHub PR / 备份快照的 staging repo
   - 需要单独检查：`git -C <staging> remote -v`、branch、HEAD、PR 状态

判定模板：
- “live shared 目录当前没有直接 Git 化/自动 push”
- “但可能存在 staging repo + GitHub 远端，用于 shared-hub-v2 结构备份/审阅”
- “是否存在系统级自动同步，还需检查 crontab/systemd/Hermes cronjob”

已知历史状态示例：
- 远端：`https://github.com/wh243327457/openclaw-shared-hub-v2`
- staging：`runtime/hermes/pr-staging/openclaw-shared-memory-v2/`
- 曾创建并合并 PR：`https://github.com/wh243327457/openclaw-shared-hub-v2/pull/1`

### 本地 staging → GitHub PR 推送

当本地已准备好 staging repo 但无远程时，按以下顺序执行：

1. **创建远程仓库**（如不存在）
   ```bash
   gh repo create <repo-name> --public --description "..."
   ```
   - 若 GraphQL 超时，重试一次；API 波动常见，第二次通常成功
   - 废弃参数 `--confirm` 已移除，直接传参即可

2. **添加 remote 并推送**
   ```bash
   git remote add origin https://github.com/<user>/<repo>.git
   git push -u origin <branch>
   ```
   - 首次推送内容较多时，60s 可能超时，建议 `--timeout=180`
   - 若仓库为空，push 后无报错即成功

3. **创建 base main 分支**（首次推送必备）
   - 如果 staging repo 只有 feat 分支，PR 创建会报错 `Base ref must be a branch`
   - 从首个 commit 切出 main 并推送：
     ```bash
     git checkout -b main <first-commit-sha>
     git push -u origin main
     git checkout <feat-branch>
     ```

4. **创建 PR**
   ```bash
   gh pr create --title "..." --body "..." --base main
   ```

### OpenClaw inbox 切换到 canonical 路径

若 OpenClaw 仍在向兼容层 `compat/daily/` 写入，需平滑迁移到 `inbox/openclaw/daily/`：

1. **复制历史 daily 文件**
   ```bash
   cp shared/compat/daily/2026-*.md shared/inbox/openclaw/daily/
   ```

2. **修改 workspace/memory symlink**
   ```bash
   # 检查当前指向
   readlink /home/vany/openclaw-data/.openclaw/workspace/memory
   # 应该是 ../shared/memory/daily（即 compat/daily）

   # 更新到 inbox
   rm /home/vany/openclaw-data/.openclaw/workspace/memory
   ln -s ../shared/inbox/openclaw/daily /home/vany/openclaw-data/.openclaw/workspace/memory
   ```

3. **验证**
   - 新写入的 daily 应出现在 `inbox/openclaw/daily/`
   - 旧 daily 仍可通过 `compat/daily/` 访问，不会丢失

### Promoter 自动化

不要依赖手动执行，接入定时任务：

1. **创建维护脚本**
   ```bash
   cat > shared/scripts/daily_maintenance.sh << 'EOF'
   #!/bin/bash
   set -e
   cd /home/vany/openclaw-data/.openclaw/shared
   python3 scripts/promoter.py >> runtime/hermes/promoter-cron.log 2>&1 || true
   python3 scripts/verify_bridge.py >> runtime/hermes/verify-cron.log 2>&1 || true
   echo "[$(date -Iseconds)] daily maintenance done" >> runtime/hermes/cron.log
   EOF
   chmod +x shared/scripts/daily_maintenance.sh
   ```

2. **注册 cron**
   ```bash
   (crontab -l 2>/dev/null; echo "0 6 * * * /home/vany/openclaw-data/.openclaw/shared/scripts/daily_maintenance.sh") | crontab -
   ```

## 运行与验证

### 当用户要"按当前情况和进度重新整理一版"时

不要只做概念说明，按**现状审计 → 落盘沉淀 → 脚本复核**执行：

1. **先读真相源**
   - `shared/manifest.yaml`
   - `shared/AGENTS.md`
   - `shared/curated/memory/MEMORY.md`
2. **再审计真实文件状态**
   - 检查 canonical 目录是否齐全：`curated/`、`inbox/`、`runtime/`、`capabilities/`、`compat/`
   - 检查兼容入口及 symlink：`memory/MEMORY.md`、`memory/facts`、`memory/projects`、`memory/daily`、`skills`、`compat/daily/.dreams`
   - 同时确认 `scripts/promoter.py`、`scripts/verify_bridge.py` 是否存在
   - **检查各 agent inbox 写入状态**：`inbox/hermes/daily/`、`inbox/openclaw/daily/`、`inbox/future-agent/daily/` 是否有内容
   - **检查 facts/ 沉淀状态**：`curated/memory/facts/` 是否为空
3. **把结果分两层落盘**
   - 稳定项目状态写到 `shared/curated/memory/projects/<project>.md`
   - 本次会话原始记录写到 `shared/inbox/hermes/daily/YYYY-MM-DD.md`
4. **同步主索引**
   - 更新 `shared/curated/memory/MEMORY.md`，让它显式指向新项目条目
5. **最后跑脚本复核**
   - 先 `promoter.py --dry-run`
   - 再正式跑 `promoter.py`
   - 最后 `verify_bridge.py`

经验结论：这种场景下，**本地 shared 文件才是真相源**，不要把"是否还记得昨天聊过什么"误解成只能靠 session_search；如果聊天检索没有命中，也应回到本地 `manifest.yaml / AGENTS.md / curated/memory/MEMORY.md` 取证。

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
