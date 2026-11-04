# 2026-11-04 GitHub 热门项目学习日报

> 执行者：Hermes；本次未调用 OpenClaw。
>
> 发现与核验窗口：2026-11-04 07:30–07:49 CST。发现入口为 GitHub Search API：`created:>=2026-10-01 stars:>100` 按 stars 降序；逐仓使用 Repository / License / Commit / Release / Issues / Checks / Security Advisories API 核验。Stars 是窗口内快照，会继续变化。
>
> 深读固定源码：`deepseek-ai/dsh-superagent-prototype@8c32a9dc5d72c033816c6a8110b37f40cf94fba4`；`storytold/wordcraft@969df57ea2e10342e4d17db87c83fff395482dac`。源码仅浅克隆到 `/tmp`，未复制进 shared。
>
> 本机验证：dsh-superagent 定向 4 个 suite **469 passed**；完整 `pnpm check` 为 **49 files passed / 10 failed，1152 tests passed / 38 failed / 7 skipped**，且 build 单独失败于缺少 `unrun`；WordCraft `cargo test -p wordcraft-mcp --lib` **25 passed**，CLI 实报 **651** 个命令。未部署 dsh-superagent、未启动 WordCraft 桌面控制口、未运行两仓完整生产场景。

## 今日结论

**今天两类项目给出同一条主线：Agent 自动化应让模型只做候选判断，把授权、命令身份、状态转换、持久副作用、文件边界和结果验收收口到宿主的确定性 chokepoint；但“有策略/有 MCP/有 tests”仍不等于可生产采用，依赖漏洞、构建缺口和宿主权限边界必须独立过闸。**

## 项目速览

API 查询时间：2026-11-04 07:30–07:32 CST。`NOASSERTION` 表示 GitHub API 未识别 license，不等于没有许可证；顶层 license 不覆盖依赖、模型、数据和 release assets。

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 51,323 | 6,488 | Python | NOASSERTION | 2026-11-03T16:09:44Z | 热度最高但许可未识别；不复制、不执行 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 25,218 | 3,071 | Python | Apache-2.0 | 2026-11-03T07:31:59Z | 已于 10-29 / 10-31 深读，今日避免重复 |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 24,441 | 2,038 | JavaScript | MIT | 2026-10-18T20:20:24Z | 已于 10-19 深读，最后 push 较旧 |
| [google-research/harness2](https://github.com/google-research/harness2) | 22,431 | 2,233 | Python | Apache-2.0 | 2026-11-02T02:17:27Z | 已于 10-19 / 10-31 深读，今日不重复 |
| [openai/math](https://github.com/openai/math) | 17,308 | 1,953 | Lean | Apache-2.0 | 2026-10-30T00:35:38Z | 形式化数学资产，与今日 Agent 控制面主线较远 |
| [storytold/wordcraft](https://github.com/storytold/wordcraft) | 17,199 | 4,728 | Rust | Apache-2.0（仓库声明双许可） | 2026-11-03T23:12:23Z | **深读：统一 command core、MCP 验收、automation roots** |
| [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) | 16,649 | 1,803 | TypeScript | MIT | 2026-11-03T09:29:14Z | **深读：Mandate、事务 core、durable effects、恢复** |
| [tangency-labs/solidcraft](https://github.com/tangency-labs/solidcraft) | 13,396 | 1,774 | Rust | Apache-2.0 | 2026-11-03T23:16:04Z | 高活跃 3D 编辑器；API issue/PR 计数 5,539，范围过大 |

## 深读项目

### 1. deepseek-ai/dsh-superagent-prototype

- **链接**：https://github.com/deepseek-ai/dsh-superagent-prototype
- **固定提交**：[`8c32a9dc5d72c033816c6a8110b37f40cf94fba4`](https://github.com/deepseek-ai/dsh-superagent-prototype/commit/8c32a9dc5d72c033816c6a8110b37f40cf94fba4)，commit time `2026-10-31T12:06:31Z`，GitHub verification 为 `unsigned`。
- **GitHub API**：**Stars: 16,649**；Forks `1,803`；Language `TypeScript`；**License: MIT**；`created_at=2026-10-31T09:32:46Z`，`updated_at=2026-11-03T23:30:55Z`，`pushed_at=2026-11-03T09:29:14Z`，API `open_issues_count=0`（含 PR）。
- **release / issue**：Releases API 与 Issues API 均返回空数组；仓库只有一个可见 commit。README 明确写明它是 research prototype、非 DeepSeek 正式产品、非 production-ready，并且论文部分设计尚未实现。
- **一句话判断**：值得学的不是“主动替团队写代码”，而是用 Mandate + role-scoped core + durable effect queue 把跨 GitHub/飞书的长期 Agent 工作约束为可审计状态机；但单提交、alpha peer runtime、构建缺依赖和真实高权执行模型使其只能作为机制样本。
- **解决的问题**：替代“一个聊天 Session 同时接消息、判断授权、跑命令、发回复”的旧做法；将 Trigger→Eval→Decision→Ticket→Assignment→Report→Reply 分层，使入站事实、工作授权、执行状态和外部副作用可分别恢复与审计。
- **来源交叉核验**：README；`docs/002-authorization.md`；`docs/003-execution.md`；`docs/007-architecture.md`；`package.json` / `pnpm-lock.yaml`；固定提交源码；Repository / Commit / Release / Issues / Security Advisories API；本机 typecheck、定向测试、全量测试与 build。

#### repo tree 摘要

固定提交浅克隆含 `216` 个非 `.git` 文件，约 `2.60 MB`。

```text
dsh-superagent-prototype/
├── src/core/                  # Trigger/Thread/Decision/Ticket/Assignment 纯领域与 role ports
├── src/app/                   # SQLite store、effects、sessions、delivery、HTTP、view/tool adapters
├── src/sources/               # GitHub / Feishu intake、poll、read、trigger、channel adapters
├── src/executor/              # DSH worker 生命周期、prepare、background work、recovery
├── src/client/                # 人工 overview / ticket / settings panel
├── prompts/                   # orchestrator / worker / admission / delivery 行为契约
├── skills/                    # GitHub 与飞书宿主侧 skill 入口
├── docs/                      # philosophy→domain→authorization→execution→architecture
├── tests/                     # 59 个 spec 文件及 host/deployment fixtures
├── cordis.patch.yml           # DSH bundle 组合与运行时注入
├── package.json               # Node/DSH 版本、scripts、direct/peer deps
└── pnpm-lock.yaml             # 289 package records，lockfileVersion 9.0
```

#### 架构 / 实现与数据流

```text
GitHub / Feishu Source
  → normalize Trigger + actor/thread/scope
  → Policy.gate（explicit / inferred / not admitted）
  → Eval + complete rule assessment
  → Decision(accept/ignore/unavailable)
  → Ticket + immutable-ish Mandate(policy version + basis + scope)
  → Assignment / isolated Session / work directory
  → Worker Report(waiting/ready/blocked/failed/dropped)
  → Reply / launch / delivery / relay 先写 SQLite effect
  → commit 后 dispatcher 执行、重试、恢复、health report
```

关键分离：

1. `Engine` 是唯一事务 mutation 入口，并用 `Pick<Engine, ...>` 给 Source、main Session、People、Settings、Executor 不同能力面；
2. 模型 assessment 不是 authority：`assessmentOutcome()` 要求覆盖每条 enabled rule、方向已定、至少一条规则命中和 intent evidence，inferred 只有 `auto` 才可 accept；
3. Ticket 的 Mandate 在 resume 时重验 source scope、sender、mode 和 matched rules；
4. 外部副作用不在 command transaction 内直接执行，而先写 durable queue；effect 的 `(kind,key)` 既是 coalescing key，又用 `seq+generation` 防运行中旧 attempt 删除新版 payload；
5. Session delivery 用稳定 message ID，并从 live events、持久历史和 pending inbox 三处去重，flush 后才向 producer 确认。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/core/engine.ts` | 单一领域 mutation 入口 | 每个 mutation 包在 `repo.atomic()`；对不同 caller 只暴露 role-scoped `Pick` |
| `src/policy.ts` | admission / assessment / Mandate revalidation | Zod strict schema、exact rule coverage、policy hash、explicit/inferred 分流、resume revalidate |
| `src/app/effects.ts` | durable side-effect outbox | SQLite queue、per-kind concurrency、ordered lane、指数退避、generation-aware delete、drain |
| `src/app/delivery.ts` | Session 消息幂等交付 | `requestId→MessageId`，扫描 persistent history + inbox，authorize 后送达，flush 后 ACK |
| `src/core/assignments.ts` | worker report 状态转换 | waiting / ready / blocked / failed / dropped 与 input read/terminal 语义 |
| `src/executor/dsh.ts` | DSH host adapter | worker launch、prepare、background、permission preset、recovery；高权执行面 |
| `docs/002-authorization.md` | 授权契约 | subscription 只给 context 不给 authority；Mandate 的创建、stop、resume 重验 |
| `docs/003-execution.md` | 执行与恢复契约 | worker slot、持久工作、failure、source/channel retry、pause 语义 |

#### ⭐ 源码精读 1：所有领域 mutation 经单一事务入口

签名：`receive(trigger: Trigger): ReceiveResult`、`decide(triggerId: string, outcome: Outcome): Decision`、`report(ticketId: string, report: WorkerReport): Ticket`

```ts
receive(trigger: Trigger): ReceiveResult {
  return this.repo.atomic(() => this.intake.receive(trigger))
}

decide(triggerId: string, outcome: Outcome): Decision {
  return this.repo.atomic(() => this.evals.decide(triggerId, outcome))
}

report(ticketId: string, report: WorkerReport): Ticket {
  return this.repo.atomic(() => this.assignments.report(ticketId, report))
}
```

`Engine` 构造时组合 Intake/Evals/Tickets/Assignments/Replies；外部并不拿到完整对象，而是得到 `EngineForSources`、`EngineForPeople`、`EngineForExecutor` 等 `Pick`。这让“谁可调用哪种状态转换”成为 TypeScript 接口的一部分，而不是只靠 prompt。边界：TypeScript 类型不构成进程级安全；拿到 store/host 对象的恶意插件仍可绕开 core。

#### ⭐ 源码精读 2：accept 需要完整规则覆盖与确定方向

签名：`assessmentOutcome(assessment, settings, strength): AssessmentOutcome`

```ts
const enabled = settings.policy.rules.filter(rule => rule.enabled)
const judged = assessment.rule_assessments
const ids = new Set(judged.map(item => item.rule_id))
if (judged.length !== enabled.length || ids.size !== judged.length
    || enabled.some(rule => !ids.has(rule.id))) {
  throw new Error('Exactly one assessment for every enabled rule is required')
}
if (assessment.decision !== 'accept')
  return { kind: assessment.decision, reason: assessment.reason, audit }
if (!directionAllowed(assessment.direction))
  return { kind: 'ignore', audit, reason: { code: 'directionUnsettled' } }
if (!matches.length)
  return { kind: 'ignore', audit, reason: { code: 'noRuleMatched' } }
```

这不是让模型输出一个 `accept=true` 就开工：缺规则、重复规则、方向未定、无匹配、无 intent evidence 都会被确定性代码拒绝；inferred 在非 `auto` 模式只记录 `would_accept`。边界：rule 文本本身仍可能设计不良，且 `auto` 是高风险开关，不能从此实现推导“自动执行安全”。

#### ⭐ 源码精读 3：durable effect 使用 generation 防旧 attempt 覆盖新工作

签名：`enqueue<K>()`、`attempt(kind, handler, row): Promise<void>`

```ts
enqueue<K extends EffectKind>(kind: K, key: string, payload: EffectPayloads[K]): void {
  this.store.db.prepare(`INSERT INTO effect ... ON CONFLICT(kind, key) DO UPDATE
    SET value = excluded.value, generation = generation + 1,
        attempts = 0, error = '', due = excluded.due`)
    .run(kind, key, JSON.stringify(payload), ++this.seq, this.now(), new Date(this.now()).toISOString())
  this.kick()
}
```

```ts
const own = 'kind = ? AND key = ? AND seq = ? AND generation = ?'
const ownRow = [kind, row.key, row.seq, row.generation] as const
if (!failure) this.store.db.prepare(`DELETE FROM effect WHERE ${own}`).run(...ownRow)
else if (failure.error instanceof Later) {
  this.store.db.prepare(`UPDATE effect SET due = ? WHERE ${own}`)
    .run(this.now() + handler.retry[0], ...ownRow)
}
```

effect 在业务事务中先入库，commit 后再 dispatch。运行期间同 key payload 更新会提升 generation，旧 attempt 完成时因 compare 条件不再匹配，不能删除新版任务。边界：`idle()` 只表示当前没有 runnable task，不代表所有 future-due rows 完成；业务 completed 仍需 ticket/receipt gate。

#### ⭐ 源码精读 4：消息交付去重后 flush，再确认 producer

签名：`AgentDelivery.send(agent, requestId, text, mode, signal, authorize?, accepted?)`

```ts
const seen = await this.history(agent)
if (this.ctx.agents.get(agent.id) !== agent) throw new Error('Delivery target was disposed')
authorize?.()
const id = messageId(requestId)
const pending = [...agent.inbox.nextTurn, ...agent.inbox.nextStep]
  .some(message => deliveryId(message) === id)
if (!seen.ids.has(id) && !pending) {
  const message = freezeMessage({ id, role: 'user', content: [{ type: 'text', text }], source })
  mode === 'steer' ? agent.steer(message) : agent.followup(message)
}
accepted?.()
await this.ctx.sessionPersistence.flush()
```

源码实际是 `accepted?.()` 在 `flush()` **之前** 调用；注释写“flush before acknowledging producer”，两者语义可能依赖 accepted callback 的实际定义，存在文档/实现歧义，列为待核验。可靠点是 stable message ID、历史与 pending 双查、target identity 和 effect-time authorize；不应把回调命名自动解释为 durable ACK。

#### 依赖分析与供应链风险

- `package.json` runtime direct deps 只有 `proper-lockfile 4.1.2` 与 `zod 4.4.3`，但有 23 个 `@deepseek-ai/*` alpha peer dependencies；Node 要求 `^22.19.0 || >=24.0.0`，DSH 要求 `^0.2.1-alpha.2`。
- `pnpm-lock.yaml` 有 289 package records；`npx pnpm@11.7.0 install --frozen-lockfile` 成功，但本机 Node `22.14.0` 低于声明 floor，产生 engine warning。
- `pnpm audit --prod` 实报 **1 high**：`zod 4.4.3` 命中 `GHSA-mrhx-c7xc-m3w5`（oversized constrained collections 可耗尽内存），修复线 `>=4.6.6`。是否被外部不可信超大 collection 真实触达需 reachability 复核，但不能上线前忽略。
- `pnpm check`：typecheck 通过，测试阶段 **1152 passed / 38 failed / 7 skipped**；多数失败为 WSL/本机 5 秒 timeout，但 `commands.spec.ts` 还有非 timeout assertion failure。由于 test 失败，script 未到 build；单独 build 又真实失败：`tsdown` 无法 import 未声明的 `unrun`。因此不能声称仓库当前可完整构建。
- 定向 `core-engine / policy / effects / delivery` 4 suites 实报 **469 passed**，只证明本文精读的窄机制在当前 fixture 下通过，不覆盖部署、source polling、migration、完整 runtime 和 build。

#### 可复用经验

- **当长期 Agent 能跨消息、线程和重启继续工作时，应优先把一次授权固化为带 actor/source/scope/policy-version 的 Mandate，并在 resume 与最终副作用前重验，因为旧聊天上下文不是永久授权；边界是 live task 是否立即撤销仍需单独 enforcement。**
- **当业务事务会触发外部副作用时，应优先 transaction 内写 durable effect、commit 后 dispatch，并用 scope key + generation 防旧 attempt 覆盖新 payload，因为直接 API 调用既难恢复又会重复；边界是 queue idle 不能冒充业务 terminal。**

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/mandate-effect-envelope-v0/` 做纯 Python fixture：定义 `Mandate(actor, scope, policy_rev, allowed_effects)`、`Effect(kind,key,generation,payload)`，模拟 policy change、同 key payload 更新、crash-before-send、resume 和 final revalidation；断言旧 generation 不能 ACK 新 payload、policy rev 变化必须 blocked。只用 synthetic state，不接 provider/GitHub/飞书，不改 config/cron/skill/curated。

#### 风险边界

- **License**：MIT 允许机制学习；依赖、DSH alpha packages 与运行环境仍需各自 license review。
- **维护活跃度**：API 显示 2026-11-03 有 push，但公开仓仅一个 commit、无 release、无 issue/PR；“活跃”不等于维护成熟。
- **安全风险**：worker 以 operator OS user 无审批执行；文档明确 blocked command 和目录只是 defaults，不是安全边界，绝对路径可绕 command name block。另有 Zod high advisory。
- **局限 / 不适用**：依赖 DeepSeek Harness alpha peer surface；公开版本与内部/论文实现不同；全量 check 未通过，build 缺 `unrun`；不适合直接接入当前 Hermes 或无人值守生产执行。
- GitHub Security Advisories API 返回 0 条 published advisory，只说明仓库级公开记录为空，不代表没有漏洞。

#### ⭐ Skill 升格判断

**需二次验证。** `Mandate + policy revision + durable effects + generation-aware retry` 与现有 `autonomous-learning/orchestrator-protocol`、verification/completion 经验高度重叠，先做 runtime POC 和去重，不新建 dsh 专属 shared Skill；构建、漏洞、effect-time revocation 和 accepted/flush 语义补证后，最多更新现有 class-level contract。

#### ⭐ Hermes / shared hub 落地路径

1. runtime POC：`runtime/hermes/github-learning-poc/mandate-effect-envelope-v0/`，实现纯数据结构与 fixtures；
2. 若验证通过，更新 `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：新增 `authorization_basis`、`policy_revision`、`effect_receipt`、`generation`、resume revalidation，不复制上游源码；
3. 在 `scripts/github_learning_orchestrator.py` 的后续设计中，将“报告生成”和“知识库 copy / push artifact”建模为分开的 durable effects；本任务只提出 candidate，不改脚本；
4. Hermes 只使用本地 `~/.hermes` 配置，任何 provider/model/cron/secret 变更都不自动执行；OpenClaw 本任务不调用、不修改。

### 2. storytold/wordcraft

- **链接**：https://github.com/storytold/wordcraft
- **固定提交**：[`969df57ea2e10342e4d17db87c83fff395482dac`](https://github.com/storytold/wordcraft/commit/969df57ea2e10342e4d17db87c83fff395482dac)，commit time `2026-11-03T23:12:07Z`，GitHub verification `verified=true / valid`。
- **GitHub API**：**Stars: 17,199**；Forks `4,728`；Language `Rust`；**License: Apache-2.0（API）**；仓库实际有 `LICENSE-APACHE` 与 `LICENSE-MIT`，workspace 声明 `MIT OR Apache-2.0`；`created_at=2026-10-07T08:34:24Z`，`updated_at=2026-11-03T23:31:51Z`，`pushed_at=2026-11-03T23:12:23Z`，API `open_issues_count=2,602`（含 PR）。
- **latest release**：[`v0.15.0`](https://github.com/storytold/wordcraft/releases/tag/v0.15.0)，published `2026-11-03T00:53:40Z`。浅克隆没有 tags 是 `--depth 1` clone 行为，不能据此说仓库无 tag。
- **一句话判断**：值得学的是把 UI、CLI、MCP 和 control channel 全部收口到同一 command registry，并以结构化 inspect/render、路径 confine、undo/rollback 做 Agent 可验证编辑；但复杂文档解析面和当前依赖 advisory 使其不能未经修复处理不可信文档。
- **解决的问题**：替代“Agent 模拟点击某个编辑器、靠截图猜结果”以及“CLI/MCP/UI 各自实现一套业务语义”的旧做法；同一 command core 同时服务人和 Agent，并允许 inspect document 做结构化 read-back。
- **来源交叉核验**：README；`docs/mcp.md`；`docs/control-protocol.md`；`SECURITY.md`；`Cargo.toml` / `Cargo.lock`；固定提交关键源码；v0.15.0 release；Issues API；Checks API；本机 cargo metadata、MCP tests、CLI commands 与 cargo-audit。

#### repo tree 摘要

固定提交浅克隆含 `951` 个非 `.git` 文件，约 `27.38 MB`；其中 `.rs=791`。Cargo workspace 有 `19` 个 packages。

```text
wordcraft/
├── crates/doc/                # 文档模型、selection、styles、track changes
├── crates/layout/             # line break、pagination、table/notes/hit testing
├── crates/docx|formats|pdf/   # OOXML 与多格式 import/export/render
├── crates/engine/             # Session、command registry、undo、file access、inspection
├── crates/mcp/                # stdio JSON-RPC、tool schemas、Headless/Remote backend
├── crates/control-key/        # desktop loopback control key
├── crates/ui-egui/            # 可替换桌面 UI
├── apps/wordcraft-cli/        # convert / inspect / run / mcp CLI
├── apps/wordcraft/            # desktop app + control channel
├── apps/wordcraft-web/        # WebAssembly app
├── docs/                      # MCP、control、recovery、architecture、parity
├── Cargo.toml / Cargo.lock    # workspace contract；702 locked packages
└── SECURITY.md                # crafted docs / MCP / control / network 均在威胁范围
```

#### 架构 / 实现与数据流

```text
Human UI / CLI script / MCP tool / JSON control request
  → stable command id + JSON params
  → Session::run(command, params)
  → enabled/protection check
  → snapshot + panic guard + command dispatch
  → success: undo/dirty/revision 更新
     failure: restore document/session state
  → structured inspect / text / render read-back
  → save/export（可受 AutomationRoots 限制）
```

Agent-facing 分两条 backend：

- `Headless`：同进程 `Session`，可使用 read/write roots 限制文件；
- `Remote`：MCP bridge 连接桌面 app 的 loopback control channel，可 screenshot/click/key，但 docs 明确 desktop app **没有等价 roots 限制**，因此不能把 headless 的边界外推到 remote。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/engine/src/lib.rs` | command contract | `CommandSpec{id, params, mutates, enabled, run}`；Registry 给所有入口共用 |
| `crates/engine/src/session/run.rs` | command transaction shell | enable/protection、snapshot、panic→error、失败 rollback、undo/dirty/revision |
| `crates/engine/src/file_access.rs` | automation filesystem gate | read/write root 分离、canonical path、whole-component containment、symlink checks |
| `crates/mcp/src/lib.rs` | Headless/Remote backend | doc routing、engine.execute、inspect/render、roots 在 backend call 外围生效 |
| `crates/mcp/src/tools.rs` | MCP tool surface | JSON schemas、readOnlyHint、batch stop-on-error、inspect/render/save adapters |
| `crates/mcp/src/server.rs` | bounded stdio JSON-RPC | request line cap、initialize/tools/resources、protocol stdout/stderr 分离 |
| `docs/control-protocol.md` | desktop control authority | 127.0.0.1 + 256-bit key、1 MiB line cap、queued input 需 read-back |
| `docs/mcp.md` | Agent 使用与边界 | file roots、TOCTOU、headless vs remote、inspect/render 验收流程 |

#### ⭐ 源码精读 1：同一 CommandSpec 驱动所有入口

签名：`CommandSpec::new(...)`、`Registry::describe()`

```rust
pub struct CommandSpec {
    pub id: &'static str,
    pub label: &'static str,
    pub location: &'static str,
    pub shortcut: &'static str,
    pub params: &'static str,
    pub mutates: bool,
    pub enabled: fn(&Session) -> Option<&'static str>,
    pub run: fn(&mut Session, &Value) -> CmdResult,
}

pub fn describe(&self) -> Value {
    Value::Array(self.specs.iter().map(|s| serde_json::json!({
        "id": s.id, "label": s.label, "location": s.location,
        "shortcut": s.shortcut, "params": s.params, "mutates": s.mutates
    })).collect())
}
```

本机 `cargo run -p wordcraft-cli -- commands --json` 实报 **651 个 command**，高于 README 的“422”和 docs/mcp 的“over 270”，说明文档数字已漂移；可靠做法是运行时 discovery，而非硬编码命令数量。边界：`params` 当前是描述字符串，不是完整 machine-enforced JSON Schema；未知字段可能被部分命令忽略。

#### ⭐ 源码精读 2：Session::run 提供 rollback 与 panic containment

签名：`pub fn run(&mut self, id: &str, params: &Value) -> Result<Value, CmdError>`

```rust
let Some(spec) = reg.get(id) else {
    return Err(CmdError::Unknown(id.to_string()))
};
if let Some(why) = (spec.enabled)(self) {
    return Err(CmdError::Disabled(format!("{id}: {why}")));
}
let guard = if spec.mutates {
    crate::cmd::protect::check_before(self, id, params)?
} else { false };
let before_doc = if spec.mutates {
    Some((self.doc.clone(), self.sel.clone(), self.history.clone(), self.redo.clone(),
          self.typing_open, self.undo_evicted, self.column.clone()))
} else { None };
```

```rust
let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(||
    crate::cmd::column::dispatch(self, id, mutates, run, params)
));
let mut result = match result {
    Ok(r) => r,
    Err(p) => Err(CmdError::Failed(format!("{id} panicked: {msg}"))),
};
if result.is_ok() && guard && !crate::cmd::protect::outside_unchanged(...) {
    result = Err(CmdError::Disabled(format!("{id}: only the editable regions ... can change")));
}
```

它把 UI/CLI/MCP 的 mutation 语义统一为“失败不留下文档变化”，并将 panic 转成 tool error。边界：clone-based snapshot 对超大文档的内存/延迟成本需实际 benchmark；panic containment 也不能捕获 abort、OOM 或原生库进程崩溃。

#### ⭐ 源码精读 3：文件 authority 采用 read/write 分离并解析 symlink

签名：`AutomationRoots::new()`、`AutomationRoots::check(path, access)`

```rust
pub fn new(read: Option<&Path>, write: Option<&Path>)
    -> Result<Option<Arc<Self>>, String> {
    if read.is_none() && write.is_none() { return Ok(None); }
    let read = read.map(|p| Root::open(p, Access::Read)).transpose()?;
    let write = write.map(|p| Root::open(p, Access::Write)).transpose()?;
    Ok(Some(Arc::new(Self { read, write })))
}
```

```rust
if inside(&resolve(path)?, folder) && entry_inside()? {
    return Ok(());
}
match access {
    Access::Read => Err(format!("automation path rejected: outside the read root {root}: {path}")),
    Access::Write => Err(format!("automation path rejected: outside the write root {root}: {path}")),
}
```

它不仅核验 symlink 最终目标，write 还核验将被 replace/remove 的 directory entry 本身，避免“root 外 symlink 指向 root 内”被用来改外部 entry。源码和 docs 都诚实说明 check→open 存在 TOCTOU；同 OS 上可换 link 的进程仍能赢竞态。

#### ⭐ 源码精读 4：MCP tools 显式区分 read-only，batch 对错误有结构化终态

签名：`tool_definitions()`、`call_tool(b, name, a): ToolResult`

```rust
fn tool(name: &str, title: &str, desc: &str, schema: Value, ro: bool) -> Value {
    json!({"name": name, "title": title, "description": desc,
      "inputSchema": schema,
      "annotations": {"title": title, "readOnlyHint": ro, "openWorldHint": false}})
}
```

```rust
for c in a.get("commands").and_then(Value::as_array).cloned().unwrap_or_default() {
    let r = exec(b, id, params, doc);
    let failed = r.is_err();
    out.push(match r {
        Ok(v) => json!({"command": id, "ok": true, "result": v}),
        Err(e) => json!({"command": id, "ok": false, "error": e}),
    });
    if failed && !keep { return ToolResult { content: ..., is_error: true }; }
}
```

MCP surface 只暴露较小工具集，再通过 command discovery 访问长尾能力；每个 batch item 保留 command identity 和 ok/error。边界：`readOnlyHint` 是声明，不是 authorization；`execute` 可触达 651 个命令，实际 effect 仍必须依据 command registry 和 host gate，不可只信 MCP 注解。

#### 依赖分析与供应链风险

- Workspace Rust `1.95` / edition 2024，`Cargo.lock` 锁定 `702` packages；核心依赖包括 `serde`、`image`、`quick-xml`、`zip`、`cfb`、RustCrypto、egui，以及多个固定 revision 的 `storytold/craft-libs` / egui / winit Git dependencies。
- fixed Git revision 优于浮动 branch，但扩大 provenance 与 license review 面；`[patch.crates-io]` 使上游 crate 名可能实际来自 fork，SBOM 需记录 source URL + rev，不能只记 semver。
- `cargo audit` 实报 **4 vulnerabilities**，全部落在 `zip 3.0.0`：`RUSTSEC-2026-0367`、`0368`、`0369`、`0429`，涉及 SUID/SGID、symlink 越界/权限和 panic，修复线均为 `>=9.0.0`。另外有 `tokio 1.53.2` unsound warning、4 个 unmaintained warnings 和 1 个 yanked package。
- WordCraft 明确处理 docx/odt 等 archive/container 格式，`zip` 漏洞与输入面具有潜在相关性；具体是否调用受影响的 `extract()` 路径仍需 reachability 核验，不能直接断言可利用，也不能因 MCP tests 通过而忽略。
- 本机 `cargo test -p wordcraft-mcp --lib` 实报 **25 passed / 0 failed**；首次 build 约 4m42s，复跑 19s。只覆盖 MCP library fixtures，不覆盖完整 workspace、desktop UI、所有 parser、wasm、network pack 或恶意文档。
- GitHub fixed-head Checks：`gate`、4 个 tests、print 三平台、nix eval 为 success；SonarCloud Scan 为 failure。上游 CI 是补充证据，不替代本机/生产验证。

#### 可复用经验

- **当 UI、CLI、MCP 和自动化脚本要操作同一业务对象时，应优先共用稳定 command registry 和单一 mutation primitive，再从运行时生成 capability discovery，因为复制实现会造成语义漂移；边界是命令 metadata 必须由实现和 contract tests 校验。**
- **当 Agent 产出富文档或其他可结构化对象时，应优先执行 mutation→结构化 inspect→必要时 render→save/read-back，而不是只凭 tool success 或截图，因为可验证 artifact 比动作回执更接近业务完成；边界是 parser/render 仍可能共享同一缺陷。**

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/command-inspect-envelope-v0/` 做不依赖 WordCraft 的 JSON fixture：定义 `CommandSpec(id,effect,input_schema)`，执行 synthetic document mutation，生成 `before_hash / after_hash / inspect / expected assertions / save receipt`；加入 unknown command、invalid params、partial batch、read-only mislabel 测试。目标是验证 Hermes 工具结果能从“exit 0”升级为 artifact closure，不安装 MCP server、不处理用户真实文档。

#### 风险边界

- **License**：GitHub API 返回 Apache-2.0，但仓库是 `MIT OR Apache-2.0`；第三方 fonts/assets、craft-i18n、Git forks 和输入文档内容需分别审核。
- **维护活跃度**：v0.15.0 刚于 11-03 发布，fixed head 当日仍有 commit；API open issue/PR 计数 `2,602`，高速开发也意味着接口漂移和 backlog 风险。
- **安全风险**：复杂文档/图片/XML/ZIP parser 面大；cargo-audit 有 4 个 zip advisories；desktop remote control 虽为 loopback + 256-bit key，但 remote backend 没有 headless automation roots。
- **局限 / 不适用**：read/write roots 有 check-open TOCTOU；`readOnlyHint` 不构成 enforcement；UI queued input 只代表入队，docs 要求 inspect 后再继续；命令数字在 README/docs/运行时不一致。
- Security Advisories API 返回 0 条 published advisory，不代表 dependency advisory 为 0；SECURITY.md 也明确 crafted document、MCP、control 和 network response 属于安全范围。

#### ⭐ Skill 升格判断

**需二次验证。** “统一 command core + inspect/render 验收 + automation read/write roots”可迁移，但当前 shared 已有 verification-first、orchestrator 和 tool effect 经验。先做 synthetic POC，并确认是否只更新现有 `orchestrator-protocol` / `github-hot-project-learning` 的验收条款；不新建 WordCraft 专属 Skill，不复制 Rust 源码。

#### ⭐ Hermes / shared hub 落地路径

1. runtime POC：`runtime/hermes/github-learning-poc/command-inspect-envelope-v0/`；
2. 对 Hermes 工具适配器定义 `tool_id / effect / target_scope / input_hash / artifact_hash / inspect_assertions / terminal`；这只是 candidate schema，不修改当前 tools 配置；
3. 若 POC 通过，在 `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md` 增补 artifact inspect/read-back gate；在 `capabilities/skills/research/github-hot-project-learning/SKILL.md` 增补运行时 capability discovery，不硬编码 README 的命令数量；
4. 任何后续真实文档 MCP 试验都必须限定独立 read/write root、使用非敏感 fixture，并在 zip advisories 修复或 reachability 风险接受前禁止处理不可信 archive 文档；
5. 本任务不改 Hermes tools/provider/model/config/cron，不接入 OpenClaw。

## 跨项目机制对照

| 维度 | dsh-superagent | WordCraft | 对 Hermes/shared hub 的候选启示 |
|---|---|---|---|
| 模型职责 | assessment / routing / worker reasoning | 选择稳定 command 与 params | 模型提议，宿主 gate 与 executor 决定 authority/effect |
| 单一入口 | `Engine` + role-scoped `Pick` | `Session::run` + command registry | 状态 mutation 不应散落在 prompt/adapters |
| 权限 | Mandate + policy version + resume revalidate | read/write AutomationRoots + protection checks | scope、effect、revision 在最终 chokepoint 重验 |
| 副作用 | SQLite durable Effects + generation | command snapshot/rollback + save | command success 与 durable artifact receipt 分开 |
| 验证 | reports / replies / stored effects | inspect_document / render / save | completed 需要结构化 read-back，不只 exit 0 |
| 当前阻断 | Zod high、全量 tests/build 不绿、alpha runtime | 4 个 zip advisory、TOCTOU、remote 无 roots | 只抽象模式，暂不接生产依赖 |

## 经验沉淀

1. **当模型输出会触发长期工作时，应优先把它降格为候选，并由宿主用完整规则覆盖、scope、policy revision 和 final effect gate 决定是否执行，因为模型判断不是 authority；边界是 rule/config 本身也要版本化和测试。**
2. **当事务提交后还要发消息、启动 worker、复制报告或调用外部 API 时，应优先把副作用写成 durable、幂等、generation-aware 的 effect，再由 dispatcher 执行，因为同步 side effect 无法可靠恢复；边界是 effect queue 空不等于业务完成。**
3. **当多个入口共享业务能力时，应优先收口到同一个 typed command/mutation core，并从实现动态生成 capability 清单，因为 README 数字和手写 adapter 会漂移；边界是 metadata 必须经过实现级 contract test。**
4. **当 Agent 修改文件或富文档时，应优先使用最小 read/write root、结构化 inspect、artifact hash 与 save read-back，因为“调用成功/queued/截图看起来对”都不能证明目标状态；边界是 check-open TOCTOU 和同源 verifier 缺陷仍需独立对抗测试。**
5. **当热门仓库测试很多且上游 CI 大多绿色时，应优先在当前 commit 与当前宿主运行窄测试、完整 check 和依赖 advisory 扫描，因为 469/25 个 passing tests 仍可与 build failure、38 个全量失败和高危依赖同时存在；边界是 advisory 命中还需 reachability 判断。**

## Skill 升格总判断

- **dsh-superagent：需二次验证**；候选更新现有 `orchestrator-protocol`，不建项目专属 Skill。
- **WordCraft：需二次验证**；候选补强 command discovery + artifact inspect/read-back，先 runtime synthetic POC。
- **今日不直接迁移 / 不自动晋升**：两个模式均与既有 verification/completion/orchestration 经验重叠，且各自存在真实供应链或构建阻断。候选只能进入二轮审计，不写 curated active fact。

## 明日继续

1. 复核 dsh `accepted?.()` 与 `flush()` 的 producer ACK 真实调用链，并用 Node 22.19+/24 在非 WSL 或放宽 test timeout 的隔离环境重跑 build/full check，区分环境慢与实现失败。
2. 对 WordCraft `zip 3.0.0` 做调用路径 reachability：搜索 `ZipArchive::extract` / stream extraction 是否用于不可信 docx/pack；不运行恶意样本，不在 root 权限下解压。
3. 若两项补证通过，再只做一个合并 POC：`Mandate → command → durable effect → inspect/hash receipt → terminal`，避免创建两个重复 Skill。

## 候选反哺

### Candidate Facts

- [ ] topic: 长期 Agent 授权应绑定 actor/source/scope/policy revision，并在 resume/final effect 重验 | evidence: `dsh-superagent@8c32a9d` 的 `policy.ts`、`docs/002-authorization.md`、`Engine` role ports | 建议: update existing autonomous-learning orchestration fact after POC | 安全级别: medium
- [ ] topic: 多入口能力应共用 command registry，完成态需 inspect/read-back | evidence: `wordcraft@969df57` 的 `CommandSpec`、`Session::run`、MCP tests 25 passed、CLI 651 commands | 建议: update existing verification-first fact after dedupe | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: Mandate + generation-aware effect envelope | 可复用场景: cron/subagent/外部 API 的可恢复副作用 | 是否建议 shared: yes（仅更新现有 orchestrator-protocol） | 原因: 跨 Agent 通用，但需先验证 ACK 与 policy-change race
- [ ] 名称: Command → inspect → artifact receipt gate | 可复用场景: 文档/文件/构建产物型工具 | 是否建议 shared: yes（更新现有 verification contract） | 原因: 能减少 exit-0 假完成，但需避免 project-specific API

### Candidate Open Questions

- [ ] 问题: dsh `accepted?.()` 在 persistence `flush()` 前调用是否会提前 ACK producer？ | reason: conflict（注释与调用顺序） | priority: high
- [ ] 问题: dsh build 缺 `unrun` 是 tsdown 0.22.14 packaging regression、lockfile policy副作用还是仓库漏声明？ | reason: gap | priority: high
- [ ] 问题: WordCraft 是否实际调用受影响的 `zip::extract` API 处理用户文档/语言包？ | reason: security reachability | priority: high
- [ ] 问题: WordCraft command params 字符串如何演进为 machine-enforced schema，同时兼容 651 个命令？ | reason: adaptation | priority: medium

### 不应自动落地

- 不安装或部署 dsh-superagent，不创建 GitHub/飞书 listener，不启用 `auto` accept，不让 worker 以当前 OS 用户无审批执行。
- 不把 Zod/ZIP advisory 写成“已证实可利用”；只记录真实扫描命中，reachability 待核验。
- 不启动 WordCraft desktop control port，不读取用户真实文档，不处理不可信 DOCX/ZIP，不把 control key/secret 写入 shared。
- 不自动改 Hermes/OpenClaw 配置、模型、provider、tools、cron 或 secret；不调用 OpenClaw。
- 不把本日报候选直接写入 curated，不复制上游源码到 shared Skill。

## 证据与知识库路径

- 共享原始报告：`inbox/hermes/daily/2026-11-04-github-learning.md`
- API / test / audit 证据：`runtime/hermes/github-hot-project-learning/evidence/2026-11-04/`
- 项目卡片：`runtime/hermes/github-learning/deepseek-ai-dsh-superagent-prototype.md`、`runtime/hermes/github-learning/storytold-wordcraft.md`
- 经验追加：`runtime/hermes/github-learning/lessons.md`
- 通过 orchestrator 审计后同步的人类知识库目标：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-11-04-GitHub热门项目学习日报.md`
