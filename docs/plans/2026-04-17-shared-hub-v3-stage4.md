# shared-hub-v3 stage4 migration layer 实施计划

> For Hermes: use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 在不回流 v2 storage layout 到 v3 根目录的前提下，为 `next/shared-hub-v3/` 增加一个最小可执行的 `v2 -> v3 migration layer`，先把 v2 的长期真相源安全导入到 v3 `truth/`。

**Architecture:** stage4 不改造现有 `/home/vany/openclaw-data/.openclaw/shared`，也不把 `compat/`、`memory/`、`skills/` 重新带回 v3。新增一个仅由 Hermes 触发的 migration executor，读取 v2 `manifest.yaml + AGENTS.md + curated/memory/`，经过 preflight 后把稳定内容复制到 v3 `truth/memory/`，并写入独立的 `truth/migration-logs/` 审计记录与 `truth/memory/MEMORY.md` 的受托管迁移索引块。

**Tech Stack:** Python 3 标准库、Markdown frontmatter、现有 `scripts/verify_v3.sh` / `tools/shared_v3_verify.py` 校验链路。

---

状态：planning / migration-layer
日期：2026-04-17
优先级：高（作为 stage3 promote 之后、stage5 adapter 之前的桥接批次）

## 现在什么情况

1. v2 已经有稳定 canonical truth：`curated/memory/`，并保留 `memory/`、`skills/`、`compat/` 兼容入口。
2. v3 stage3 已经跑通 `sandbox/` -> `truth/` 的 promote 执行链路，但明确还没有 migration / adapter。
3. 当前最缺的不是新的协议，而是一个“把现有 v2 长期真相迁入 v3 truth”的最小迁移层。
4. 这个迁移层必须坚持 v3 的核心约束：compatibility belongs to adapters, not storage。

## Stage4 最小完成定义

满足以下 6 条，才算 stage4 完成：

1. 存在 `tools/v2_migration_executor.py`，可对一个 v2 shared root 执行 dry-run / apply。
2. migration executor 只允许读取 v2 canonical truth，不读取旧兼容视图作为输入真相源。
3. 第一批仅迁移：
   - `v2 curated/memory/facts/*.md` -> `v3 truth/memory/facts/`
   - `v2 curated/memory/projects/*.md` -> `v3 truth/memory/projects/`
4. 执行器具备幂等语义：重复执行不会重复写脏数据；未变化文件显示为 `unchanged` 或 `skipped`。
5. 执行器会写独立审计日志到 `truth/migration-logs/`，并刷新 `truth/memory/MEMORY.md` 的受托管迁移区块。
6. `tools/shared_v3_verify.py` 能跑 demo fixture，覆盖 dry-run、apply、idempotent re-run 三段验证。

## In Scope

### 迁移输入（只读）
- `v2-root/manifest.yaml`
- `v2-root/AGENTS.md`
- `v2-root/curated/memory/MEMORY.md`
- `v2-root/curated/memory/facts/*.md`
- `v2-root/curated/memory/projects/*.md`

### 迁移输出（v3）
- `next/shared-hub-v3/truth/memory/facts/*.md`
- `next/shared-hub-v3/truth/memory/projects/*.md`
- `next/shared-hub-v3/truth/migration-logs/*.md`
- `next/shared-hub-v3/truth/memory/MEMORY.md` 的受托管 migration block

### 必须新增
- migration protocol 文档
- migration log template
- 自包含 v2 demo fixture
- verifier 对 migration layer 的最小回归校验

## Out of Scope

1. 不迁移 `compat/`、`memory/`、`skills/` 兼容目录本身。
2. 不迁移 `inbox/`、`runtime/`、`prefill/`、workspace symlink、agent 本地配置。
3. 不迁移 `.dreams`、cache、index、临时摘要。
4. 不把 `capabilities/skills/` 自动转换成 v3 capability registry。
5. 不实现持续双写、实时同步、文件监听器。
6. 不做 destructive sync：stage4 不删除 v3 已有 truth 文件。
7. 不自动处理 secrets；发现疑似 secrets 时只失败并提示，不做净化修复。

## 关键设计决策

### 1. 真相源只认 v2 curated

虽然 v2 暴露了 `memory/` 兼容入口，但 stage4 迁移只认：
- `curated/memory/facts/`
- `curated/memory/projects/`

原因：
- `memory/` 是兼容视图，不是 canonical truth
- `compat/daily/` 与 `.dreams` 明确属于 legacy/runtime 兼容链路
- 迁移层不能把 v2 的兼容结构误升格为 v3 truth

### 2. migration 是 Hermes 专属 authority，不走 worker promote

stage3 promote 解决的是 `sandbox/` 提交审批后进入 `truth/`；
stage4 migration 解决的是“历史 canonical truth 的一次性/分批导入”。

因此 stage4 设计为：
- 仅 orchestrator/Hermes 触发
- 不要求构造 fake sandbox submissions
- 审计日志独立写到 `truth/migration-logs/`
- 不复用 `truth/promote-logs/`，避免把历史导入和新提交 promote 混淆

### 3. 幂等优先，默认不覆盖冲突

第一批策略：
- 目标不存在：`copied`
- 目标已存在且 SHA256 相同：`unchanged`
- 目标已存在且 SHA256 不同：默认 `conflict` 并返回非 0

不做默认覆盖，避免把 stage3 之后在 v3 产生的新真相被历史导入静默踩掉。
后续若需要覆盖，单独再加显式参数，不放进 stage4 最小批次。

### 4. MEMORY.md 只维护索引，不复制 v2 MEMORY 正文

`v2 curated/memory/MEMORY.md` 只作为：
- 迁移输入存在性检查
- 审计来源之一

stage4 不把它原文复制到 `v3 truth/memory/MEMORY.md`。
相反，v3 MEMORY 只新增一个托管块，例如：
- `<!-- SHARED-V3-V2-MIGRATION:START -->`
- `<!-- SHARED-V3-V2-MIGRATION:END -->`

区块中仅列出最近 migration run 的：
- run_id
- source_root
- copied / unchanged / conflicts 统计
- 最近导入目标路径

## 文件计划

### 新增文件
- `next/shared-hub-v3/tools/v2_migration_executor.py`
- `next/shared-hub-v3/protocol/v2-migration-protocol.md`
- `next/shared-hub-v3/protocol/v2-migration-log-template.md`
- `next/shared-hub-v3/truth/migration-logs/.gitkeep`
- `next/shared-hub-v3/fixtures/v2-demo-shared/manifest.yaml`
- `next/shared-hub-v3/fixtures/v2-demo-shared/AGENTS.md`
- `next/shared-hub-v3/fixtures/v2-demo-shared/curated/memory/MEMORY.md`
- `next/shared-hub-v3/fixtures/v2-demo-shared/curated/memory/facts/demo-imported-fact.md`
- `next/shared-hub-v3/fixtures/v2-demo-shared/curated/memory/projects/demo-imported-project.md`

### 修改文件
- `next/shared-hub-v3/README.md`
- `next/shared-hub-v3/AGENTS.md`
- `next/shared-hub-v3/manifest.yaml`
- `next/shared-hub-v3/truth/memory/MEMORY.md`
- `next/shared-hub-v3/tools/shared_v3_verify.py`
- `next/shared-hub-v3/scripts/verify_v3.sh`

## 数据映射规则

### v2 -> v3 path mapping
- `curated/memory/facts/<name>.md` -> `truth/memory/facts/<name>.md`
- `curated/memory/projects/<name>.md` -> `truth/memory/projects/<name>.md`

### 明确不映射
- `memory/` -> 无
- `compat/` -> 无
- `skills/` -> 无
- `inbox/` -> 无
- `runtime/` -> 无
- `prefill/` -> 无

## migration executor 设计草案

### CLI 形式

```bash
python3 next/shared-hub-v3/tools/v2_migration_executor.py \
  --v2-root next/shared-hub-v3/fixtures/v2-demo-shared \
  --dry-run

python3 next/shared-hub-v3/tools/v2_migration_executor.py \
  --v2-root next/shared-hub-v3/fixtures/v2-demo-shared
```

### 输入
- `--v2-root <path>`：v2 shared 根目录
- `--dry-run`：只做 preflight 与执行计划输出，不写文件

### preflight 必查项
1. `manifest.yaml` 存在且 `version: 2`
2. `curated/memory/MEMORY.md` 存在
3. `curated/memory/facts/`、`curated/memory/projects/` 目录存在
4. 待导入文件全部位于 `curated/memory/` 下
5. 文件扩展名限制为 `.md`
6. 文件内容中若命中明显 secret 模式则 fail fast

### 输出摘要（stdout）
建议输出单行 summary + JSON 明细，例如：
- `DRY-RUN copied=2 unchanged=0 conflicts=0`
- `SUCCESS copied=2 unchanged=0 conflicts=0 log=truth/migration-logs/migration-20260417-demo001.md`

JSON 明细至少包含：
- `run_id`
- `v2_root`
- `copied`
- `unchanged`
- `conflicts`
- `items[]`（source / target / status / sha256）

### 审计日志
审计日志写入：
- `truth/migration-logs/migration-<run_id>.md`

frontmatter 至少包含：
- `run_id`
- `source_root`
- `executed_by`
- `executed_at`
- `copied_count`
- `unchanged_count`
- `conflict_count`

正文至少包含：
- 本次导入文件清单
- source -> target 映射
- 每个条目的 source_sha256 / target_sha256
- 失败或冲突列表

### 失败与回滚
stage4 不做复杂回滚系统，采用“两段式安全策略”：
1. 先完整 preflight，任何 conflict / invalid input 直接拒绝 apply
2. 只有 preflight 全绿才开始 copy

由于 stage4 默认不覆盖已有目标，因此失败场景只可能发生在“部分新文件已创建”。
对这种情况，执行器应：
- 先把计划内写入目标收集在内存中
- copy 前确保父目录已存在
- 任一 copy 失败时返回非 0，并在日志中记录 partial failure

## 任务拆解

### Task 1: 写 migration protocol 与模板

**Objective:** 把 stage4 语义、边界和审计格式定死，避免实现时漂移。

**Files:**
- Create: `next/shared-hub-v3/protocol/v2-migration-protocol.md`
- Create: `next/shared-hub-v3/protocol/v2-migration-log-template.md`
- Modify: `next/shared-hub-v3/README.md`
- Modify: `next/shared-hub-v3/AGENTS.md`
- Modify: `next/shared-hub-v3/manifest.yaml`

**Implementation notes:**
- manifest 增加 migration protocol / executor 引用
- README/AGENTS 明确：migration layer 读取 v2 canonical truth，但不把 compat 当 storage
- protocol 文档写清楚 in-scope / out-of-scope / idempotency / conflict policy

**Verification:**
- `python3 next/shared-hub-v3/tools/shared_v3_verify.py`
- 预期：先失败，提示缺少 migration executor / fixture / verify 逻辑（这是正常的阶段性失败）

### Task 2: 建自包含 v2 demo fixture

**Objective:** 让 verifier 不依赖真实本机 `/home/vany/openclaw-data/.openclaw/shared`，可在 staging repo 内自测。

**Files:**
- Create: `next/shared-hub-v3/fixtures/v2-demo-shared/manifest.yaml`
- Create: `next/shared-hub-v3/fixtures/v2-demo-shared/AGENTS.md`
- Create: `next/shared-hub-v3/fixtures/v2-demo-shared/curated/memory/MEMORY.md`
- Create: `next/shared-hub-v3/fixtures/v2-demo-shared/curated/memory/facts/demo-imported-fact.md`
- Create: `next/shared-hub-v3/fixtures/v2-demo-shared/curated/memory/projects/demo-imported-project.md`

**Implementation notes:**
- fixture 只保留最小 v2 canonical truth，不创建 compat / runtime / skills
- fixture 内容要明显标记 `demo-imported-*`，避免和 stage3 promote fixture 混淆

**Verification:**
- `python3 next/shared-hub-v3/tools/v2_migration_executor.py --v2-root next/shared-hub-v3/fixtures/v2-demo-shared --dry-run`
- 预期：命令存在后能列出 2 个待导入对象

### Task 3: 实现 migration executor

**Objective:** 提供可执行、幂等、默认不覆盖的 v2 -> v3 导入器。

**Files:**
- Create: `next/shared-hub-v3/tools/v2_migration_executor.py`
- Modify: `next/shared-hub-v3/truth/memory/MEMORY.md`
- Create: `next/shared-hub-v3/truth/migration-logs/.gitkeep`

**Implementation notes:**
- 继续保持 Python 标准库实现
- 复用 stage3 executor 的一些做法：sha256、frontmatter、managed block
- 但不要复用 promote log 路径与 block marker
- managed block 建议单独使用 `SHARED-V3-V2-MIGRATION`

**Verification:**
- dry-run：`python3 next/shared-hub-v3/tools/v2_migration_executor.py --v2-root next/shared-hub-v3/fixtures/v2-demo-shared --dry-run`
- apply：`python3 next/shared-hub-v3/tools/v2_migration_executor.py --v2-root next/shared-hub-v3/fixtures/v2-demo-shared`
- rerun：再次执行 apply
- 预期：第一次 `copied=2`；第二次 `unchanged=2`

### Task 4: 扩展 verifier

**Objective:** 把 migration layer 纳入 stage4 的本地回归链路。

**Files:**
- Modify: `next/shared-hub-v3/tools/shared_v3_verify.py`
- Modify: `next/shared-hub-v3/scripts/verify_v3.sh`

**Implementation notes:**
- verifier 新增 stage4 常量：demo fixture root、demo migration targets、demo log path
- 校验前先清理 demo migration 输出，避免脏状态影响结果
- 校验顺序：required files -> manifest refs -> migration dry-run -> migration apply -> migration rerun -> managed block / log assertions

**Verification:**
- `bash next/shared-hub-v3/scripts/verify_v3.sh`
- 预期：输出 `PASS` 与 `wrapper=PASS`

### Task 5: 文档收口

**Objective:** 让 stage4 的边界、操作方式和后续 stage5 方向都可读可交接。

**Files:**
- Modify: `next/shared-hub-v3/README.md`
- Modify: `next/shared-hub-v3/AGENTS.md`
- Modify: `docs/plans/2026-04-17-shared-hub-v3-stage4.md`

**Implementation notes:**
- README 解释 stage3 与 stage4 的职责差异
- AGENTS 强调 migration layer 只读取 v2 canonical truth
- 计划文件若实施中发生偏差，及时回填实际路径与命令

## 验收命令

```bash
python3 next/shared-hub-v3/tools/v2_migration_executor.py \
  --v2-root next/shared-hub-v3/fixtures/v2-demo-shared \
  --dry-run

python3 next/shared-hub-v3/tools/v2_migration_executor.py \
  --v2-root next/shared-hub-v3/fixtures/v2-demo-shared

python3 next/shared-hub-v3/tools/v2_migration_executor.py \
  --v2-root next/shared-hub-v3/fixtures/v2-demo-shared

bash next/shared-hub-v3/scripts/verify_v3.sh
```

预期：
- dry-run 成功且不落任何 truth 写入
- 第一次 apply 导入 2 个 demo 文件
- 第二次 apply 不重复导入，显示 `unchanged=2`
- 审计日志进入 `truth/migration-logs/`
- `truth/memory/MEMORY.md` 出现 stage4 托管迁移区块
- verifier 总体输出 `PASS`

## Stage4 完成后再考虑的下一步

1. Stage5 再讨论 adapter / shim，把 Hermes/OpenClaw 如何消费 v3 接口正式化。
2. 评估是否把 `capabilities/manifests/shared-skills.yaml` 映射到 v3 registry，但这不属于 stage4。
3. 如果后续要支持更新覆盖或双向同步，必须单独开新阶段，不要混进当前批次。

## 一句话结论

stage4 不是把 v2 的 compat 结构搬进 v3，而是补上一条“只从 v2 canonical truth 安全导入到 v3 truth”的最小迁移层。