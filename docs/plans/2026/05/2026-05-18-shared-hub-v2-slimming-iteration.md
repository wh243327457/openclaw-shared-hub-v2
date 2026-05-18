# 共享中台 v2 瘦身治理迭代 Plan

> **For Hermes:** 这是共享中台 v2 的可恢复瘦身计划。执行时按阶段逐步推进，每一步先验证、再小提交、再 PR 审查；不要一次性大改结构。

**Goal:** 降低 shared hub v2 的认知复杂度和 Git 膨胀风险，同时保持 Hermes / OpenClaw / future-agent 的兼容入口可用。

**Architecture:** 保留现有 v2 分层，不推倒重来；把共享中台重新压缩成三层心智模型：core 真相层、edge 兼容层、bulk 原始/运行层。每次迭代只收口一个膨胀源，确保 `verify_bridge.py` 和 `promoter.py --dry-run` 持续通过。

**Tech Stack:** Markdown governance docs, Git, shared hub scripts (`promoter.py`, `verify_bridge.py`), symlink compatibility entries.

---

## 当前审计基线（2026-05-18）

共享根目录：`/home/vany/agent/.openclaw/shared`，legacy 入口：`/home/vany/openclaw-data/.openclaw/shared`。

### 规模基线

| 区域 | 当前规模 | 判断 |
|---|---:|---|
| `curated/` | 约 128K / 17 文件 | 健康，是真相源 |
| `capabilities/` | 约 400K / 52 文件 | 可接受，但 references 有膨胀趋势 |
| `scripts/` | 约 356K / 13 文件 | 可接受，应保持少数稳定脚本 |
| `docs/` | 约 148K / 20 文件 | 可接受，有历史 plan 沉积 |
| `inbox/` | 约 2.0M / 129 文件 | 明显膨胀，尤其 OpenClaw dreaming |
| `runtime/` | 约 6.7M / 518 文件 | 最大本地膨胀源，不应进入 Git 审查面 |
| `compat/` | 约 272K / 61 文件 | 作为兼容层偏重 |
| `.git/` | 约 3.8M | 暂可接受，但不宜继续跟踪 raw/bulk |

### 已确认问题

1. `runtime/` 本地运行产物很多，虽然 `.gitignore` 已忽略，但会干扰审计。
2. `inbox/openclaw/daily/dreaming/` 与 `compat/daily/dreaming/` 像原始日志库，不适合长期进入 main 审查面。
3. `compat/` 从“薄兼容入口”变成了数据承载层。
4. `curated/memory/MEMORY.md` 混入 `Promoted From Short-Term Memory` 历史噪声。
5. shared skills references 越来越像会话记录库，需要升格/沉淀门槛。

### 当前健康点

必须保持：

- `manifest.yaml`
- `AGENTS.md`
- `curated/memory/`
- `capabilities/manifests/shared-skills.yaml`
- `capabilities/skills/`
- `scripts/promoter.py`
- `scripts/verify_bridge.py`
- `prefill/`
- `memory/` symlink 兼容入口
- `skills -> capabilities/skills`

---

## 总体原则

### 三层心智模型

```text
core/真相层：curated + capabilities + manifest + AGENTS +核心 scripts
edge/兼容层：memory + skills + compat，只保留薄入口和说明
bulk/原始与运行层：inbox + runtime，默认不进主审查，不长期堆在 Git
```

### 瘦身红线

- 不破坏 Hermes / OpenClaw 现有读取入口。
- 不删除未归档的唯一数据；先统计、再迁移/归档、再从 Git 跟踪层移除。
- 不把 `.dreams`、cache、index、log、临时摘要写入 curated。
- 不把明文 secret 写入 shared。
- 每一步必须能用命令验证，且应独立提交、独立 PR 审查。

### 每步固定验证命令

```bash
cd /home/vany/agent/.openclaw/shared
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
git diff --check
```

如果涉及 symlink 或兼容入口，再额外验证：

```bash
readlink memory/MEMORY.md
readlink memory/facts
readlink memory/projects
readlink memory/daily
readlink skills
readlink compat/daily/.dreams
```

---

## 迭代路线图

| 阶段 | 目标 | 风险 | 状态 |
|---|---|---:|---|
| Phase 0 | 建立瘦身计划与基线 | 低 | ✅ 已完成 |
| Phase 1 | Git 跟踪边界收口：raw/runtime 不再扩大 | 中 | ✅ 已完成 |
| Phase 2 | compat 薄化：只做兼容入口 | 中 | ✅ 已完成 |
| Phase 3 | MEMORY.md 瘦身：主索引回归索引 | 中 | ✅ 已完成 |
| Phase 4 | inbox/raw 归档与摘要晋升机制 | 中 | ⏳ 待开始 |
| Phase 5 | shared skills references 合并与升格门槛 | 低-中 | ⏳ 待开始 |
| Phase 6 | 自动化守护：verify 增加膨胀告警 | 中 | ⏳ 待开始 |
| Phase 7 | 收口 PR、删除已合并分支、更新长期状态 | 低 | ⏳ 待开始 |

---

## Phase 0：建立瘦身计划与基线

**Objective:** 只落盘计划，不移动、不删除、不改兼容入口。

**Files:**
- Create: `docs/plans/2026/05/2026-05-18-shared-hub-v2-slimming-iteration.md`

**Step 0.1：记录当前审计结论**

- 写入规模基线、问题判断、健康点。
- 明确本轮不是推倒重来，而是迭代瘦身。

**Step 0.2：创建计划分支**

```bash
git checkout -B plan/shared-hub-slimming-iteration origin/live/shared-sync
```

**Step 0.3：验证计划文件**

```bash
git diff --check
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
```

**Acceptance:**

- 计划文件存在。
- 没有结构性改动。
- 验证命令通过。

**Commit:**

```bash
git add docs/plans/2026/05/2026-05-18-shared-hub-v2-slimming-iteration.md
git commit -m "制定共享中台瘦身迭代计划"
```

---

## Phase 1：Git 跟踪边界收口

**Objective:** 明确哪些目录不应继续扩大 Git 历史，先防止新增 bulk 进入主线。

**Files:**
- Modify: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `docs/runtime-retention.md`
- Optional Modify: `scripts/verify_bridge.py`

**Step 1.1：确认当前已跟踪 bulk 清单**

```bash
git ls-files inbox compat runtime | sort > /tmp/shared-tracked-bulk.txt
wc -l /tmp/shared-tracked-bulk.txt
```

**Step 1.2：增强 `.gitignore` 新增防线**

候选规则：

```gitignore
# Raw / bulk histories should not grow in Git by default
inbox/**/daily/dreaming/
compat/daily/dreaming/
inbox/**/daily/.dreams/
compat/daily/.dreams/
```

注意：这不会自动移除已跟踪文件，只防止新增未跟踪 bulk 误入 Git。

**Step 1.3：在 AGENTS.md 写清 Git 边界**

新增原则：

- `curated/`、`capabilities/`、核心 `docs/`、核心 `scripts/` 可进入 main。
- `inbox/` 是 raw，不默认进 main；需要审查时只提交摘要或索引。
- `runtime/` 永不进入 main。
- `compat/` 只做薄兼容入口，不承载新增数据。

**Step 1.4：verify 增加 report-only warning（可选）**

如果时间允许，让 `verify_bridge.py` 输出：

- tracked bulk 文件数；
- `inbox/**/dreaming` tracked 数；
- `compat/daily/dreaming` tracked 数；
- 默认 warning，不 fail。

**Acceptance:**

- 新增 raw/dreaming 不会被 `git status` 默认显示为待提交。
- 现有兼容入口不变。
- `verify_bridge.py` 通过。

**执行记录（2026-05-18）：**

- 当前 `inbox` / `compat` / `runtime` 已被 Git 跟踪的历史文件数：167。
- 已确认 `compat/daily/dreaming/**` 与 `inbox/openclaw/daily/dreaming/**` 是主要 tracked bulk 来源。
- 已修改 `.gitignore`，防止新增 `inbox/**/daily/dreaming/`、`compat/daily/dreaming/`、`inbox/**/daily/.dreams/`、`compat/daily/.dreams/` 进入待提交面。
- 已在 `AGENTS.md` 增加 Git 跟踪边界：core 可审查，bulk 默认不进 main。
- 已在 `docs/runtime-retention.md` 增加 Git 主线边界与后续 `git rm --cached` 分阶段处理口径。
- 本阶段不删除、不移动、不 `git rm --cached` 任何历史 bulk；历史 tracked bulk 留到 Phase 2 / Phase 4 单独 PR 处理。

---

## Phase 2：compat 薄化

**Objective:** 让 `compat/` 回归兼容视图，不再像真实数据仓库。

**Files:**
- Modify/Create: `compat/daily/README.md`
- Modify: `AGENTS.md`
- Modify: `manifest.yaml`
- Modify: `scripts/verify_bridge.py`
- Potential Git operation: `git rm --cached compat/daily/dreaming/**` 或迁移到 archive 分支/目录

**Step 2.1：确认 compat 下真实内容来源**

```bash
find compat/daily -maxdepth 4 -type f | sort
find compat/daily -maxdepth 4 -type l -printf '%p -> %l\n'
```

**Step 2.2：定义 compat 最小形态**

目标：

```text
compat/daily/
├── README.md
└── .dreams -> ../../runtime/openclaw/dreams
```

**Step 2.3：处理历史 `compat/daily/dreaming/`**

优先方案：从 Git 跟踪移除，但保留本地文件：

```bash
git rm --cached -r compat/daily/dreaming
```

如果需要保留可审阅历史，先生成摘要：

```text
docs/archives/compat-daily-dreaming-summary-2026-05.md
```

**Step 2.4：verify 检查 compat 不再承载大量真实文件**

新增 warning：`compat/daily` 下除 README 与 symlink 外出现大量文件时提示。

**Acceptance:**

- `memory/daily` 仍可解析。
- `compat/daily/.dreams` 仍指向 runtime dreams。
- OpenClaw 旧入口不被破坏。
- Git 主线不再承载 compat dreaming bulk。

**执行记录（2026-05-18）：**

- 已确认 `compat/daily/` 中 Git 跟踪 bulk 包括 54 个 `dreaming/**` 文件与 5 个旧 daily snapshot。
- 已执行 `git rm --cached -r compat/daily/dreaming`，并对 5 个旧 daily snapshot 执行 `git rm --cached`；本地文件保留，兼容读取不受影响。
- 已更新 `compat/daily/README.md`，明确其只是 legacy entry，不是真相源。
- 已在 `.gitignore` 增加 `compat/daily/20*.md`，避免旧 daily snapshot 被再次误加。
- 验证后 Git 跟踪的 compat 入口只剩：`compat/daily/.dreams` 与 `compat/daily/README.md`。
- 本地 legacy 仍存在：5 个旧 daily 文件、54 个 dreaming 文件；这些只作本地兼容，不进入主线快照。
- 已验证 `compat/daily/.dreams -> ../../runtime/openclaw/dreams`，`memory/daily` 仍由 `verify_bridge.py` 判定正常。
- 已运行 `git diff --check`、`python3 scripts/promoter.py --dry-run`、`python3 scripts/verify_bridge.py`；结构验证 `ok: true`。

---

## Phase 3：MEMORY.md 主索引瘦身

**Objective:** 让 `curated/memory/MEMORY.md` 回归“索引 + 状态块”，移走自动 promoted 噪声。

**Files:**
- Modify: `curated/memory/MEMORY.md`
- Create: `curated/memory/archives/promoted-legacy-2026-05.md` 或 `docs/archives/promoted-legacy-2026-05.md`
- Modify: `scripts/promoter.py`（如其继续写入噪声）

**Step 3.1：切分主索引内容**

保留：

- 根路径；
- 作用范围；
- 目录索引；
- 写入规则；
- 当前状态；
- 自动生成状态块。

迁出：

- `Promoted From Short-Term Memory (...)` 全部历史块；
- score/source 元数据；
- GitHub daily 表格型历史明细。

**Step 3.2：创建 legacy promoted archive**

如果还需要保留历史可追溯性，迁到：

```text
curated/memory/archives/promoted-legacy-2026-05.md
```

并在 `MEMORY.md` 只留一行链接。

**Step 3.3：检查 promoter 行为**

确认 `scripts/promoter.py` 未来不会继续把大量 promoted 明细追加进主索引。若会，改为：

- 主索引只更新状态块；
- 候选/晋升日志写到 `runtime/` 或 `docs/promote-log-template.md` 指定位置；
- 长期事实必须进入 facts/projects 文件。

**Acceptance:**

- `MEMORY.md` 行数显著下降。
- 读取前 100 行即可获得共享中台真实入口。
- promoted 历史如需保留，有 archive 链接。
- promoter dry-run 通过。

**执行记录（2026-05-18）：**

- 审计前 `curated/memory/MEMORY.md` 共 184 行，其中 78 行以后为 7 个 `Promoted From Short-Term Memory` 历史块。
- 已确认 `scripts/promoter.py` 只替换 `<!-- SHARED-BRIDGE-STATE:START/END -->` 标记块，不会继续自动追加 promoted 明细。
- 已将旧 promoted 明细迁到：`curated/memory/archives/promoted-legacy-2026-05.md`。
- 主索引只保留一段“历史 promoted 归档”链接说明，长期事实仍要求进入 `facts/` 或 `projects/`。
- 迁移后 `MEMORY.md` 降至 81 行；前 100 行即可读完共享中台入口、状态块和归档指针。

---

## Phase 4：inbox/raw 归档与摘要晋升机制

**Objective:** 让 inbox 继续作为 raw 写入入口，但不再无限进入 main。

**Files:**
- Modify: `docs/promote-protocol.md`
- Modify: `docs/maintenance.md`
- Modify: `scripts/promoter.py`
- Optional Create: `docs/archives/inbox-retention-policy.md`

**Step 4.1：定义 inbox 保留窗口**

建议：

- main 中只保留最近 7 天或关键手工挑选 raw；
- 旧 raw 不进 main，只保留本地或外部归档；
- 晋升后的长期信息写入 `curated/memory/facts/` 或 `projects/`。

**Step 4.2：promoter 输出 backlog 摘要，而非搬运全文**

`promoter.py --dry-run` 应优先输出：

- 候选 source；
- 建议目标；
- 是否重复；
- 是否过期；
- 不直接把 raw 全量写入 `MEMORY.md`。

**Step 4.3：Git 跟踪移除大批 dreaming raw**

优先对这类目录执行 `git rm --cached`：

```text
inbox/openclaw/daily/dreaming/
inbox/openclaw/daily/.dreams/
```

保留本地 raw，不作为 main 审查面。

**Acceptance:**

- inbox 仍可写入。
- main 不再因 dreaming raw 快速膨胀。
- curated 中有必要摘要，不丢关键长期事实。

---

## Phase 5：shared skills references 合并与升格门槛

**Objective:** 防止 shared skills 变成会话记录库。

**Files:**
- Modify: `AGENTS.md`
- Modify: `capabilities/manifests/shared-skills.yaml`
- Modify: selected `capabilities/skills/**/SKILL.md`
- Potential Create: `docs/shared-skill-governance.md`

**Step 5.1：定义 shared skill 升格四条件**

必须满足至少一项：

- 两个以上 agent 会复用；
- 属于横切治理能力；
- 不共享会导致行为漂移；
- 是稳定工作流，而不是单次任务复盘。

**Step 5.2：合并重复 references**

对同一主题的多个 reference，合并成较少的 class-level 文档，例如：

```text
references/autonomous-learning-operations.md
references/shared-hub-maintenance.md
references/config-routing-governance.md
```

**Step 5.3：manifest 增加 review 状态**

为每个 shared skill 标注：

- owner；
- last_reviewed；
- status；
- scope；
- 是否允许 future-agent 读取。

**Acceptance:**

- shared skill 数量和 reference 数量不再无序增长。
- 新 skill 是否进 shared 有明确判断口径。

---

## Phase 6：自动化守护与膨胀告警

**Objective:** 让复杂度不再靠人工记忆维护。

**Files:**
- Modify: `scripts/verify_bridge.py`
- Modify: `docs/runtime-retention.md`
- Modify: `docs/maintenance.md`
- Test: `tests/test_fact_governance.py` 或新增 `tests/test_shared_slimming_policy.py`

**Step 6.1：verify 输出 size/bulk metrics**

新增报告项：

- top-level 文件数；
- top-level bytes；
- tracked inbox count；
- tracked compat dreaming count；
- runtime size；
- MEMORY.md 行数。

**Step 6.2：warning 阈值**

建议 warning，不直接 fail：

- `curated/memory/MEMORY.md` > 150 行；
- tracked `inbox/**/dreaming` > 0；
- tracked `compat/daily/dreaming` > 0；
- runtime > 100MB；
- shared skill reference 单 skill > 15 个。

**Step 6.3：测试 warning 输出**

新增测试确保 warning 不会误判核心 symlink。

**Acceptance:**

- `verify_bridge.py` 可以一眼看出膨胀源。
- 默认 report/warning，不自动删除。
- CI 或人工审查可用。

---

## Phase 7：收口 PR 与分支清理

**Objective:** 在 main 合并后清理临时/已合并分支，更新项目状态。

**Files:**
- Modify: `curated/memory/projects/shared-hub-v2.md`
- Modify: `curated/memory/MEMORY.md` 状态块或索引
- GitHub branch cleanup

**Step 7.1：确认 PR 合并状态**

```bash
gh pr list --state all --limit 20 --json number,title,state,baseRefName,headRefName,url
```

**Step 7.2：删除已合并远端分支**

仅在确认 PR 已合并后执行：

```bash
git push origin --delete docs/shared-live-commit-checklist || true
git push origin --delete feat/shared-memory-v2 || true
# live/shared-sync 只有在 main 已确认承载最新状态后再删
git push origin --delete live/shared-sync || true
```

**Step 7.3：本地同步**

```bash
git fetch origin --prune
git checkout main
git pull origin main
```

**Acceptance:**

- main 承载最新审查通过内容。
- 已合并临时分支删除。
- shared-hub-v2 项目状态更新。

---

## 推荐执行顺序

1. 先完成 Phase 0，提交计划 PR。
2. 等 PR #4 合并或确认如何处理后，再做 Phase 1。
3. Phase 1 只加规则和 warning，不移除历史文件。
4. Phase 2/4 再处理 `compat` 与 `inbox` 的 tracked bulk。
5. Phase 3 单独处理 `MEMORY.md`，避免和 bulk 清理混在一起。
6. Phase 5/6 做治理自动化。
7. Phase 7 收口分支。

---

## 风险与回滚

| 风险 | 缓解 |
|---|---|
| OpenClaw 旧 workspace 入口断裂 | 每步验证 `memory/daily`、`MEMORY.md`、`.dreams` symlink |
| raw 历史误删 | 优先 `git rm --cached`，保留本地；必要时先生成 archive 摘要 |
| promoter 继续污染 MEMORY.md | Phase 3 检查并修改 promoter 写入策略 |
| PR 太大难审 | 每个 phase 独立提交/PR |
| shared skill 规则过严影响沉淀 | 允许先本地 skill，满足跨 agent 条件后再升格 |

---

## 当前状态更新规则

每完成一个 Phase，必须更新本文件：

- 将阶段状态从 `⏳ 待开始` 改为 `⏳ 进行中` 或 `✅ 已完成`。
- 填写实际改动文件。
- 填写验证命令和结果。
- 若发现计划不合理，先修改本 plan，再执行实现。

