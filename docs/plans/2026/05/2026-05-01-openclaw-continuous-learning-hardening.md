# OpenClaw 持续学习流水线加固 Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 把 GitHub 热门项目每日学习从“OpenClaw cron 能生成，但下游偶发断链”升级为“OpenClaw 原始产物稳定落盘、Hermes 只消费当天 inbox、缺失自动告警、Obsidian/共享中台状态可验收”的持续学习闭环。

**Architecture:** 保留 OpenClaw 08:30 作为首轮学习生成器，不依赖 OpenClaw delivery 作为关键路径。新增 Hermes/shared 侧桥接脚本读取 OpenClaw cron run/session，将当天 summary 写入 `shared/inbox/openclaw/daily/YYYY-MM-DD.md` 和 runtime 状态；Hermes 审计/推送任务再从 canonical inbox 读取，生成 Obsidian 日报、质量审计和状态摘要。

**Tech Stack:** Python 3 stdlib、Hermes cronjob、OpenClaw cron JSONL、shared hub v2、Obsidian Markdown、Weixin push via existing Hermes channel.

---

## 0. 当前审计结论

### 已确认事实

- OpenClaw 已有每日学习 cron：`GitHub 热门项目每日学习`。
- OpenClaw 任务 ID：`7aa310ea-b264-40c8-b23a-ed655c565a69`。
- 计划时间：`30 8 * * *`，时区 `Asia/Shanghai`。
- 2026-05-01 08:30 已运行，OpenClaw 状态为 `ok`。
- 2026-05-01 运行 summary 存在于：
  - `/home/vany/openclaw-data/.openclaw/cron/runs/7aa310ea-b264-40c8-b23a-ed655c565a69.jsonl`
  - 对应 session：`/home/vany/openclaw-data/.openclaw/agents/main/sessions/927091d0-e03d-42b2-8d70-127ac7e5a244.jsonl`
- 但当天没有生成这些规范文件：
  - `shared/inbox/openclaw/daily/2026-05-01.md`
  - `GitHub 热门项目学习档案/每日学习/2026-05-01-GitHub热门项目学习日报.md`
  - `GitHub 热门项目学习档案/质量审计/2026-05-01-质量审计.md`

### 根因判断

OpenClaw **生成成功**，但输出只停留在 OpenClaw cron/session 内部，没有稳定桥接到 shared inbox；Hermes 审计/推送链路随后回退到了旧 Obsidian 日报，导致“任务跑了但知识库当天无产物”。

---

## 1. 必须项清单

### Hermes 侧必须项

- [ ] 新增桥接脚本：OpenClaw cron run → `shared/inbox/openclaw/daily/YYYY-MM-DD.md`。
- [ ] 新增状态面板：`shared/runtime/hermes/github-hot-project-learning/status.json`。
- [ ] 新增健康检查：检查 OpenClaw run、OpenClaw inbox、Obsidian daily、Obsidian audit 四项。
- [ ] Hermes 09:10 审计任务优先读取当天 `shared/inbox/openclaw/daily/YYYY-MM-DD.md`，不得静默回退到旧日报。
- [ ] 缺失当天 OpenClaw inbox 时必须写失败记录，并在推送内容里明确失败原因。
- [ ] 不写入任何明文 secret；如需引用只写变量名或 `[REDACTED]`。

### OpenClaw 侧必须项

- [ ] 保持现有 08:30 cron 继续运行。
- [ ] OpenClaw delivery 仅视为 best-effort，不作为闭环成功条件。
- [ ] OpenClaw 原始输出必须能通过桥接脚本进入 canonical inbox。
- [ ] 后续如能修改 OpenClaw prompt，应要求“最终报告不含过程语句，且包含 source_url、抓取口径、时间窗口、owner/repo、license、stars、pushed_at”。

### 共享中台必须项

- [ ] 运行时产物只写 `shared/runtime/<agent>/`。
- [ ] OpenClaw 原始日报只写 `shared/inbox/openclaw/daily/`。
- [ ] 稳定项目状态写 `shared/curated/memory/projects/github-hot-project-learning.md`。
- [ ] 更新 `shared/curated/memory/MEMORY.md` 自动/人工状态块。
- [ ] 通过 `scripts/verify_bridge.py`。

### Obsidian 必须项

- [ ] 每日学习文件存在：`每日学习/YYYY-MM-DD-GitHub热门项目学习日报.md`。
- [ ] 质量审计文件存在：`质量审计/YYYY-MM-DD-质量审计.md`。
- [ ] `00-总览索引.md` 至少包含最新日报和审计入口。
- [ ] 审计为红时，不进入长期项目卡片或 shared facts。

---

## 2. 目标文件布局

### 新增/修改文件

- Create: `/home/vany/openclaw-data/.openclaw/shared/scripts/openclaw_github_learning_bridge.py`
- Create: `/home/vany/openclaw-data/.openclaw/shared/scripts/github_learning_healthcheck.py`
- Modify: `/home/vany/openclaw-data/.openclaw/shared/scripts/daily_maintenance.sh`
- Modify: Hermes cron job `2a82c752d86a` prompt or wrapper behavior
- Modify: Hermes cron job `c489f1a5dfde` prompt or wrapper behavior if needed
- Modify: `/home/vany/openclaw-data/.openclaw/shared/curated/memory/projects/github-hot-project-learning.md`
- Modify: `/home/vany/openclaw-data/.openclaw/shared/curated/memory/MEMORY.md`

### 运行时文件

- Create/Update: `/home/vany/openclaw-data/.openclaw/shared/runtime/hermes/github-hot-project-learning/status.json`
- Create/Update: `/home/vany/openclaw-data/.openclaw/shared/runtime/hermes/github-hot-project-learning/healthcheck-YYYY-MM-DD.json`
- Append log: `/home/vany/openclaw-data/.openclaw/shared/runtime/hermes/github-hot-project-learning/bridge.log`

### 产物文件

- Create/Update: `/home/vany/openclaw-data/.openclaw/shared/inbox/openclaw/daily/YYYY-MM-DD.md`
- Create/Update: `/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/YYYY-MM-DD-GitHub热门项目学习日报.md`
- Create/Update: `/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/质量审计/YYYY-MM-DD-质量审计.md`

---

## 3. 分阶段实施计划

## Phase 1：补上 OpenClaw run → shared inbox 桥

### Task 1.1：创建桥接脚本骨架

**Objective:** 创建可重复运行、无外部依赖的 Python 脚本。

**Files:**
- Create: `shared/scripts/openclaw_github_learning_bridge.py`

**Implementation requirements:**

脚本必须支持：

```bash
python3 scripts/openclaw_github_learning_bridge.py --date 2026-05-01 --dry-run
python3 scripts/openclaw_github_learning_bridge.py --date 2026-05-01
python3 scripts/openclaw_github_learning_bridge.py
```

常量默认值：

```python
SHARED_ROOT = Path('/home/vany/openclaw-data/.openclaw/shared')
OPENCLAW_ROOT = Path('/home/vany/openclaw-data/.openclaw')
JOB_ID = '7aa310ea-b264-40c8-b23a-ed655c565a69'
RUNS_FILE = OPENCLAW_ROOT / 'cron' / 'runs' / f'{JOB_ID}.jsonl'
STATE_FILE = OPENCLAW_ROOT / 'cron' / 'jobs-state.json'
```

**Verification:**

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 scripts/openclaw_github_learning_bridge.py --date 2026-05-01 --dry-run
```

Expected:
- exit code 0
- 输出将要写入的 inbox 路径
- 不修改文件

---

### Task 1.2：实现 JSONL run 解析

**Objective:** 从 OpenClaw run JSONL 找到指定日期最后一条 `status=ok` 且含 summary 的记录。

**Files:**
- Modify: `shared/scripts/openclaw_github_learning_bridge.py`

**Parsing rules:**

- 逐行读取 JSONL。
- 忽略 JSON parse 失败行，但记录 warning。
- 日期匹配字段优先级：`endedAt`、`finishedAt`、`updatedAt`、`startedAt`、`createdAt`、`ts`、`timestamp`。
- 若无时间字段，但 summary 标题含 `YYYY-MM-DD`，也可匹配。
- 只接受 `status == 'ok'` 或 `lastRunStatus == 'ok'`。
- summary 字段可为 `summary`、`result`、`output`、`message` 中第一个非空字符串。

**Verification:**

```bash
python3 scripts/openclaw_github_learning_bridge.py --date 2026-05-01 --dry-run
```

Expected:
- 能定位到 2026-05-01 OpenClaw summary。
- 若无记录，输出明确错误，exit code 非 0。

---

### Task 1.3：写入 canonical OpenClaw inbox

**Objective:** 将 OpenClaw 当天原始 summary 写入 shared inbox。

**Files:**
- Modify: `shared/scripts/openclaw_github_learning_bridge.py`
- Output: `shared/inbox/openclaw/daily/YYYY-MM-DD.md`

**Markdown format:**

```markdown
# YYYY-MM-DD — GitHub 热门项目每日学习（OpenClaw 原始输出）

---
source: openclaw-cron
job_id: 7aa310ea-b264-40c8-b23a-ed655c565a69
run_status: ok
run_ts: '<timestamp>'
needs_hermes_audit: true
---

## 桥接说明

- 本文件由 Hermes/shared 桥接脚本从 OpenClaw cron run 提取。
- 这是 OpenClaw 原始输出，不是最终审计结论。

## OpenClaw 原始报告

<summary>
```

**Safety:**

- 写入前对内容做 secret redaction：匹配 `sk-...`、`token=...`、`api_key=...` 等常见模式替换为 `[REDACTED]`。
- 不覆盖非桥接脚本生成且含人工编辑标记的文件，除非传 `--force`。

**Verification:**

```bash
python3 scripts/openclaw_github_learning_bridge.py --date 2026-05-01
test -s inbox/openclaw/daily/2026-05-01.md
```

---

### Task 1.4：写入 runtime status.json

**Objective:** 让当前流水线状态机器可读。

**Files:**
- Modify: `shared/scripts/openclaw_github_learning_bridge.py`
- Output: `shared/runtime/hermes/github-hot-project-learning/status.json`

**Status schema:**

```json
{
  "date": "YYYY-MM-DD",
  "pipeline": "github-hot-project-learning",
  "openclaw": {
    "job_id": "...",
    "run_found": true,
    "run_status": "ok",
    "run_ts": "...",
    "inbox_path": "...",
    "inbox_written": true
  },
  "hermes": {
    "audit_path": null,
    "push_status": "pending"
  },
  "obsidian": {
    "daily_path": null,
    "audit_path": null
  },
  "overall_status": "openclaw_inbox_ready",
  "updated_at": "ISO-8601"
}
```

**Verification:**

```bash
python3 -m json.tool runtime/hermes/github-hot-project-learning/status.json
```

---

## Phase 2：修复 Hermes 下游消费与健康检查

### Task 2.1：创建健康检查脚本

**Objective:** 检查当天四段链路是否齐全，并输出 JSON 和人类可读摘要。

**Files:**
- Create: `shared/scripts/github_learning_healthcheck.py`

**Checks:**

1. OpenClaw run 是否存在且 `ok`。
2. OpenClaw inbox 是否存在。
3. Obsidian daily 是否存在。
4. Obsidian audit 是否存在。
5. 质量审计是否引用当天日报，而不是旧日期。
6. `00-总览索引.md` 是否包含当天入口。

**CLI:**

```bash
python3 scripts/github_learning_healthcheck.py --date 2026-05-01 --json
python3 scripts/github_learning_healthcheck.py --date 2026-05-01
```

**Exit code:**

- 全绿：0
- 黄/缺少非关键项：1
- 红/缺少 OpenClaw run 或 inbox：2

---

### Task 2.2：将桥接加入 daily_maintenance.sh 或单独 Hermes cron

**Objective:** 08:30 OpenClaw 运行后，自动在 08:35-08:40 之间生成 shared inbox。

**Preferred:** 新建 Hermes cron job，时间 `35 8 * * *`。

**Fallback:** 若不创建 Hermes cron，则在 `daily_maintenance.sh` 中加入“补桥接最近一天”的幂等步骤，但这只能每天 06:00 修复昨天/历史，不适合当天实时推送。

**Recommended command:**

```bash
cd /home/vany/openclaw-data/.openclaw/shared && python3 scripts/openclaw_github_learning_bridge.py >> runtime/hermes/github-hot-project-learning/bridge.log 2>&1
```

**Verification:**

```bash
# Hermes cron list should show 08:35 bridge job enabled, or crontab/daily_maintenance contains fallback.
```

---

### Task 2.3：更新 Hermes 08:45/09:10 任务口径

**Objective:** 禁止使用旧 Obsidian 日报冒充当天结果。

**Files:**
- Modify: Hermes cron job prompts via cronjob update, or document exact manual update if tool API unsuitable.

**Required behavior:**

- 08:45 微信摘要：优先读取 `shared/inbox/openclaw/daily/YYYY-MM-DD.md`；若不存在，推送“今日 OpenClaw 原始日报缺失/等待桥接”，不回退旧日报。
- 09:10 审计：只审计当天 `shared/inbox/openclaw/daily/YYYY-MM-DD.md`；若不存在，写失败审计到 runtime，不生成 Obsidian daily。
- 审计后写入 Obsidian daily/audit，并更新 status.json。

---

## Phase 3：补救 2026-05-01 当天产物

### Task 3.1：桥接 2026-05-01 OpenClaw 原始输出

**Objective:** 从已存在 OpenClaw run 中补写当天 inbox。

**Command:**

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 scripts/openclaw_github_learning_bridge.py --date 2026-05-01
```

**Verification:**

```bash
test -s inbox/openclaw/daily/2026-05-01.md
```

---

### Task 3.2：生成 2026-05-01 Hermes 审计文件

**Objective:** 对当天 OpenClaw 原始输出做质量审计，至少生成质量审计；若质量达标，再生成 Obsidian 日报。

**Files:**
- Read: `shared/inbox/openclaw/daily/2026-05-01.md`
- Create: `.../质量审计/2026-05-01-质量审计.md`
- Create if yellow/green: `.../每日学习/2026-05-01-GitHub热门项目学习日报.md`

**Audit rules:**

- 明确标记抓取口径偏差：GitHub Trending 失败后改用 Search API，并非严格“今日 Trending”。
- 对无法核验的 stars/license/pushed_at 标黄。
- 若发现 repo 不存在或字段明显幻觉，评级红，不生成正式日报。

---

### Task 3.3：更新总览索引

**Objective:** 让 Obsidian 首页能看到 2026-05-01 状态。

**Files:**
- Modify: `/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/00-总览索引.md`

**Verification:**

```bash
grep -n "2026-05-01" "/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/00-总览索引.md"
```

---

## Phase 4：更新共享状态与验收

### Task 4.1：更新项目状态文件

**Objective:** 把项目状态从过期的“绿/暂无阻塞”改成真实状态。

**Files:**
- Modify: `shared/curated/memory/projects/github-hot-project-learning.md`

**Required content:**

- 状态：黄 / OpenClaw 生成正常，shared inbox 桥接已补强中。
- 当前阶段：修复 run → inbox → audit → Obsidian → push 的当天闭环。
- 已知问题：2026-05-01 OpenClaw ok 但未自动落盘；Hermes 曾回退旧日报；OpenClaw delivery 不作为关键路径。
- 下一步：观察 2026-05-02 自动桥接和推送是否连续成功。

---

### Task 4.2：运行 shared 验证

**Objective:** 确认没有破坏共享中台结构。

**Commands:**

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 scripts/promoter.py --dry-run
python3 scripts/promoter.py
python3 scripts/verify_bridge.py
```

**Expected:**

- `verify_bridge.py` exit code 0。
- JSON 中 `ok: true`。

---

### Task 4.3：最终健康检查

**Objective:** 输出今日流水线验收结论。

**Commands:**

```bash
cd /home/vany/openclaw-data/.openclaw/shared
python3 scripts/github_learning_healthcheck.py --date 2026-05-01 --json
python3 scripts/github_learning_healthcheck.py --date 2026-05-01
```

**Expected:**

- OpenClaw run：绿。
- OpenClaw inbox：绿。
- Obsidian daily：绿或黄，取决于审计质量。
- Obsidian audit：绿。
- overall：至少黄，不能红。

---

## 4. 验收标准

### 最小验收

- [ ] `scripts/openclaw_github_learning_bridge.py --date 2026-05-01` 能从 OpenClaw run 生成 `inbox/openclaw/daily/2026-05-01.md`。
- [ ] `runtime/hermes/github-hot-project-learning/status.json` 存在且 JSON 合法。
- [ ] `scripts/github_learning_healthcheck.py --date 2026-05-01` 能准确报告缺失项。
- [ ] shared `verify_bridge.py` 通过。
- [ ] 没有新增明文 secret。

### 完整验收

- [ ] 08:35 桥接任务已注册。
- [ ] 08:45 推送任务不再回退旧日报。
- [ ] 09:10 审计任务只消费当天 OpenClaw inbox。
- [ ] 2026-05-01 日报/审计已补齐或明确标红并写明原因。
- [ ] 项目状态文件已更新为真实状态。
- [ ] 明天 2026-05-02 自动链路可观察。

---

## 5. 风险控制

- 不修改 OpenClaw credential / provider / token 配置。
- 不输出 OpenClaw 配置中的任何 secret。
- 不删除 OpenClaw cron 历史 run/session。
- 不让健康检查自动改写知识库，只报告状态。
- 桥接脚本必须幂等：重复运行不应制造重复块。
- 审计不通过时，不把内容升格到 shared facts 或 shared skills。

---

## 6. 执行优先级

1. **P0:** Task 1.1-1.4，先把 OpenClaw run 稳定桥接到 inbox。
2. **P0:** Task 2.1，健康检查能看见断点。
3. **P0:** Task 3.1，补救 2026-05-01 原始 inbox。
4. **P1:** Task 2.2-2.3，注册自动桥接并修正 Hermes 任务口径。
5. **P1:** Task 3.2-3.3，补齐知识库当天产物。
6. **P1:** Task 4.1-4.3，更新共享状态并验收。
