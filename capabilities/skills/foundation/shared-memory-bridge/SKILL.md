---
name: shared-memory-bridge
description: 跨 Hermes / OpenClaw / future agent 的共享中台 v2 入口
version: "2.0"
agent: hermes, openclaw, future
---

# shared-memory-bridge

跨 agent 共享记忆与共享能力的统一入口 skill。

## 共享根目录

- 宿主：`<shared-root>/`
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
- 若该 skill 会被 Hermes / OpenClaw / future-agent 复用，或属于共享中台、共享记忆、进度汇报、调研协作、配置目标识别等横切能力，则同步到 `shared/capabilities/skills/`
- 升格到 shared 时，除了复制完整 skill 目录（`SKILL.md`、`templates/`、`references/`、`scripts/`、`assets/`），还要更新 `shared/capabilities/manifests/shared-skills.yaml`
- 若明确只保留本地，也要在结论里写清楚：当前仅本地长期，不是 shared 长期能力
- `inbox/**/daily/dreaming/`、`inbox/**/daily/.dreams/` 等 raw/runtime-like 资料只做本地保留；如果已进 Git，用 `git rm --cached -r` 清出主线，并在 `docs/promote-protocol.md` / `docs/maintenance.md` 写清不得自动删除或自动晋升。

### shared governance standard

共享中台的筛选总结必须按 `docs/shared-governance-standard.md` 执行：

- `references/shared-governance-standard.md` condenses the standard into a concise reference for future screening, scoring, promotion, and compression work.

- **状态流**：`RAW_CAPTURED -> CANDIDATE_EXTRACTED -> SCREENED -> DECIDED_* -> CURATED_WRITTEN/LEFT_IN_INBOX -> VERIFIED`。
- **五门准入**：长期价值、跨 agent 价值、可验证证据、去重/冲突、脱敏安全；任一失败不得写入 curated active fact。
- **决策表**：单次 PR/commit/任务进度默认不进长期记忆；日志/cache/.dreams 默认只做 runtime 证据；项目状态压缩写 projects；跨 agent 工作流写 shared skill。
- **节奏**：daily 只做每日总结和候选池；weekly 是常规内容晋升核心记忆的唯一触发点；monthly 只做 MEMORY、runtime、skill references、tracked raw bulk 结构体检和瘦身。
  - 细节见 `references/weekly-core-memory-promotion.md`：把“每周总结复盘到核心记忆”落实为 daily summary → weekly core-memory promotion → monthly health review。
- **验收**：治理改动后跑 `python3 -m unittest tests/test_fact_governance.py`、`python3 scripts/promoter.py --dry-run`、`python3 scripts/verify_bridge.py`、`git diff --check`。

机制解释见 `docs/governance-summary-mechanism.md`；强制口径以标准文档为准。

### shared hub slimming workflow

当 shared 目录开始变重时，优先按阶段瘦身，而不是一次性大改：

1. 先加 `.gitignore` 和治理文本，阻止新的 bulk 进入主线。
2. 再把 `compat/` 收缩成薄兼容入口，历史 bulk 用 `git rm --cached` 从 index 移除，保留本地文件。
3. 再把 `curated/memory/MEMORY.md` 缩成“入口索引 + 当前状态 + archive 链接”，把 promoted 历史迁到单独 archive。
4. 最后再收口 `inbox/` raw 的 Git 跟踪边界，明确 raw 可保留、可统计，但不自动晋升 curated。
5. 每完成一阶段，更新计划文件里的 phase 状态，再跑 `git diff --check`、`scripts/promoter.py --dry-run`、`scripts/verify_bridge.py` 做收口验证。

### Pitfalls

- 不要把 `compat/` 当成真实数据仓库；它只负责兼容旧入口。
- 不要把 `MEMORY.md` 重新写成历史流水账；promoted 明细应进 archive。
- 不要把 raw bulk 的本地保留误当成 Git 跟踪；`git rm --cached` 的目标是移出主线，不是物理删除。
- 不要让 `promoter.py` 继续向主索引追加历史 promoted 明细；它应只刷新状态块和摘要统计。


配置类任务（配置、模型、provider、模型列表、gateway、tools、skills、auth、env、cron、streaming、fallback、profile、重启服务等）属于跨 agent 高风险任务，必须先识别目标系统，避免把 Hermes / OpenClaw / shared 中台混用。

### 强制路由规则（必须遵守，违反即算错误）

- 用户说"你 / 当前 agent / Hermes / 这个 agent / 当前 CLI / 当前网关"时，默认目标是 **Hermes**，优先操作 `~/.hermes/config.yaml`、`~/.hermes/.env`、`~/.hermes/auth.json` 等 Hermes 路径。**即使记忆中 OpenClaw 配置路径更显眼，也不能作为默认操作 OpenClaw 的理由。**
- 只有用户**明确**说 OpenClaw，或提供 `/home/vany/agent/.openclaw/`、`/home/node/.openclaw/` 等 OpenClaw 路径时，才操作 OpenClaw 配置。
- 用户提到"共享中台 / shared / 跨 agent / 共享记忆"时，才进入 shared 层，先读 `manifest.yaml`、`AGENTS.md`、`curated/memory/MEMORY.md`。
- **如果目标不明确，必须先问："这是改 Hermes 还是 OpenClaw？如果是当前这个 agent，我会按 Hermes 处理。"**
- 禁止因为历史记忆或某个 agent 的已知配置路径更显眼，就默认改错系统。
- 配置写入前必须声明目标系统和目标文件路径。

### 配置写入前强制自检清单

在读取或修改任何配置文件之前，先在回复中声明：

```
[配置目标识别]
目标系统：Hermes / OpenClaw / shared
目标文件：<实际路径>
操作方式：读取 / 写入 / 修改
```

如果没做这一步就动手修改配置，属于流程违规，需要重新核对。

### 常见触发词与预期目标

| 用户说 | 默认目标 | 正确文件 |
|---|---|---|
| “你 / Hermes / 当前 agent / 这个 agent / 当前 CLI” | Hermes | `~/.hermes/config.yaml` |
| “你 / Hermes 的模型 / 你用的模型” | Hermes | `~/.hermes/config.yaml` |
| “Hermes gateway / 你的 gateway” | Hermes | `~/.hermes/hermes-agent/` |
| “OpenClaw / openclaw 的配置” | OpenClaw | `/home/vany/agent/.openclaw/openclaw.json` |
| “shared / 共享中台 / 跨 agent” | shared 层 | `shared/` 根目录 |
| 只有“改配置”且无上下文 | 必须先问 | — |

共享版流程已沉淀到：`shared/capabilities/skills/foundation/config-target-routing/SKILL.md`，并登记在 `shared/capabilities/manifests/shared-skills.yaml`。

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
   - 路径：`<shared-root>`
   - 这是 OpenClaw / Hermes 实际读取和写入的共享中台目录
   - 可能不是 Git 仓库；若没有 `.git`、remote、branch，只能说明 live 目录没有直接 Git 化
   - 若它本身已经是 Git 仓库，用户说“提交一下本次修改”时可直接在 live shared 仓库内提交；先做 `git diff --check`、差异范围复核和 secret 关键词扫描，提交后汇报 hash、分支、工作区状态、是否已 push。详见 `references/shared-live-commit-checklist.md`。

2. **runtime staging Git 仓库**
   - 典型路径：`<shared-root>/runtime/hermes/pr-staging/openclaw-shared-memory-v2/`
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
   readlink /home/vany/agent/.openclaw/workspace/memory
   # 应该是 ../shared/memory/daily（即 compat/daily）

   # 更新到 inbox
   rm /home/vany/agent/.openclaw/workspace/memory
   ln -s ../shared/inbox/openclaw/daily /home/vany/agent/.openclaw/workspace/memory
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
   cd <shared-root>
   python3 scripts/promoter.py >> runtime/hermes/promoter-cron.log 2>&1 || true
   python3 scripts/verify_bridge.py >> runtime/hermes/verify-cron.log 2>&1 || true
   echo "[$(date -Iseconds)] daily maintenance done" >> runtime/hermes/cron.log
   EOF
   chmod +x shared/scripts/daily_maintenance.sh
   ```

2. **注册 cron**
   ```bash
   (crontab -l 2>/dev/null; echo "0 6 * * * <shared-root>/scripts/daily_maintenance.sh") | crontab -
   ```

## 运行与验证

### 外部机制类项目本地化

当用户要深度学习一个外部项目/文章并判断能否集成到系统中时，若结论是“机制值得借鉴，但不应直接依赖其源码/服务”，优先落成三层产物，而不是只输出调研报告：

1. `curated/memory/projects/<project>.md`：跨 agent 真相源，写机制、边界、接入价值、禁止事项。
2. `runtime/<agent>/<project>/`：实施计划、状态、架构、POC 模板和可恢复执行记录。
3. Obsidian 风格知识库：面向人类的学习入口和分章节文档。

边界：GPL/外部项目只作为机制样板时，不复制源码进核心；runtime/cache/sqlite/chunks 不晋升 curated；需要 Hermes review 后再把结论写入 curated。参考会话细节见 `references/openhuman-mechanism-localization-session.md`。

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

### 长任务落地的推荐文件组合

当要把一个长期系统从讨论推进到可落地骨架时，优先采用四件套：

- `curated/memory/projects/<project>.md`：正式架构和长期状态
- `runtime/<agent>/<project>/implementation-plan.md`：执行计划和阶段状态
- `runtime/<agent>/<project>/state.json`：机器可读状态机
- `runtime/<agent>/<project>/templates/`：instruction / review / handoff 模板

推荐顺序：
1. 先建 plan，再建正式架构。
2. 先写配置骨架，再写模板。
3. 每完成一步，立刻更新 plan 的 status。
4. 验证时固定跑：`json 解析 -> promoter --dry-run -> promoter -> verify_bridge`。
5. 如果项目会跨会话延续，必须在 `curated/memory/MEMORY.md` 里加索引入口。

Continue-from-plan iteration detail is captured in `references/continue-from-plan-iteration.md`: when a user says “继续” after a plan exists, read plan/state, execute the next pending step, update persisted plan/state, verify, and report compactly instead of asking which branch to continue.

### 长任务状态复核：不要只信 state.json

当用户问“方案到什么地步 / 能否跑通 / 继续确认”时，除了读取 `state.json` 和 `implementation-plan.md`，还必须交叉检查实际产物目录：

- `orchestrator-runs/<run_id>/run-state.json`
- `agent-outputs/<executor>/<run_id>*.md`
- `reviews/<run_id>-spec-review.md`
- `reviews/<run_id>-quality-review.md`

常见情况：真实产物已经完成 fallback + 双审，但 run-state 仍停在 `FALLBACK_OUTPUT_WRITTEN` 或 `PREPARED`。这种状态不一致时，先按产物事实判断，再只更新 runtime 状态文件收口；不得顺手写 curated、启用 cron 或升格 shared skill。

收口后至少验证：

```bash
python3 - <<'PY'
import json, pathlib
base = pathlib.Path('<shared-root>/runtime/hermes/autonomous-learning')
for p in [base/'state.json', base/'learning-backlog.json'] + list((base/'orchestrator-runs').glob('*/run-state.json')):
    json.loads(p.read_text())
print('json ok')
PY
cd <shared-root>
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

更多 rollout 细节见：`references/autonomous-learning-rollout.md`。其中包含 Phase A/B/C、canary 目录结构、dry-run 边界、Claude Code stdout 捕获模式、执行 agent 禁止自审批等经验。

状态不一致收口细节见：`references/orchestrator-state-reconciliation.md`。其中包含 run-state 与实际产物不一致时的审计顺序、只更新 runtime 的边界和最小验证命令。

落地优先级与 runtime-only 脚手架经验见：`references/landing-prioritization-runtime-scaffold.md`。其中包含如何区分 learned vs landed、按共享治理→现有流水线→自主学习→新采集系统→本地代码探索能力的落地顺序，以及新系统最小 runtime 文件包与 CodeGraph shared 候选判断口径。

CodeGraph / 本地代码上下文索引候选规则见：`references/codegraph-context-index-candidate.md`。要点：先把代码结构索引成 runtime 图谱，再让 agent 通过自然语言/MCP 查询 symbol/file/edge；缓存不进 curated；本地 POC 通过前不要升格 shared skill。

Claim / evidence / runtime-only governance rollout pattern is captured in `references/claim-evidence-runtime-rollout.md`: baseline first, schema as target not migration, evidence-backed candidates, warning-only checkers, text recall before vector, open questions in runtime, reflect workers candidate-only, and dashboard-based manual review.



Semi-auto discovery execution detail is captured in `references/autonomous-learning-semi-auto-discovery-execution.md`: how to execute exactly one approved low-risk OpenClaw discovery run from a plan-only candidate, preserve runtime/inbox-only boundaries, save stdout/stderr evidence, run Hermes spec/quality review, and avoid treating transient GitHub fetch failures as durable tool limitations.

Effect-check run pattern is captured in `references/autonomous-learning-semi-auto-effect-check.md`: when the user asks to “run one version and see effect”, generate a runtime-only semi-auto candidate bundle with explicit gates, three bounded draft runs, validation commands, and report language that does not imply full automation.

Self-healing / global inspection agent scaffolding is captured in `references/self-healing-agent-scaffold.md`: runtime-first plan shape, safety gates, finding taxonomy, approval boundaries, and verification commands for building a self-repair loop without premature auto-fixing.

### 运行与验证

完成迁移或修复后，至少执行：

```bash
python3 <shared-root>/scripts/promoter.py --dry-run
python3 <shared-root>/scripts/promoter.py
python3 <shared-root>/scripts/verify_bridge.py
```


- `promoter.py` 能更新 `shared/curated/memory/MEMORY.md` 中的自动状态块
- `verify_bridge.py` 返回 exit code 0，且 JSON 中 `ok: true`
- Hermes 仍引用 `shared/skills` 与 `shared/prefill/hermes-shared-memory.json`
- OpenClaw 仍引用 `/home/node/.openclaw/shared/skills`
- 各 workspace 的 `memory` / `MEMORY.md` / `shared` 入口仍可解析

## 新增：Warning 观察期与全局待办收口

当 claim schema、recall helper、reflect candidate 等能力刚落地时，`warning-only` 结果通常不是故障，而是结构过渡信号。处理这类阶段性 warning 时：

1. 先按类型分群：
   - **结构缺口**：缺 frontmatter / claim 字段 / evidence_refs
   - **状态枚举漂移**：旧 project 状态值不在新枚举里
   - **少量例外项**：个别条目已升级、但字段还没补齐
2. 先补少量高价值条目，不做批量迁移；优先 shared 基础结构和高频 operational facts。
3. 把“观察期问题”写进持续可见的全局待办/计划，而不是只留在聊天里，避免跨天遗忘。
4. 每次补强后重新跑 `check_curated_claims.py` / `shared_memory_dashboard.py` / `verify_bridge.py`，观察 warning 是否真实下降。
5. 仍保持 warning-only 边界：不自动写 active curated fact、不启用新 cron、不上 vector 作为默认下一步。

观察期分析细节可参考 `references/claim-warning-observation.md`。

## Secrets 安全规范

- **默认不要**将任何明文 secret（API key、token、密码等）写入 shared
- 如需引用 secret，用变量名占位（如 `$OPENCLAW_API_KEY`）
- 各 agent 的 `.env` / credential 文件保持在各自 agentDir 下
