# 2026-08-25 GitHub 热门项目每日学习报告

- 执行器：Hermes；本次没有调用、启动或模拟 OpenClaw。
- 研究日期：2026-08-25（UTC+8）。
- 共享根：先运行 `python3 scripts/resolve_shared_root.py`，真实返回 `/home/vany/agent/shared`。
- 元数据最终查询时间：2026-08-25T07:37:17+08:00。
- 发现来源：GitHub Search API，查询 `created:>2025-01-01 stars:>1000`、按 Stars 降序。另用 `curl -fsSL https://github.com/trending?since=daily` 保存页面，但本次 HTML 解析只得到导航链接，因此不把它作为候选或热度证据。
- 深读固定提交：`anomalyco/opencode@18b4cb6819d7de0b37927fef60d03927e678c9dd`；`ultraworkers/claw-code@08106b0c3771ef5b4a5aa176acccd460e88b7325`。
- 证据边界：Stars、Forks、Language、License、updated/pushed、default branch 来自本次 `gh api repos/{owner}/{repo}`；README、SECURITY、release、issues、Actions 来自 GitHub API 或固定提交浅克隆；代码结论来自固定提交文件；运行结论只使用本机真实命令输出。

## 今日结论

**今日主线是“先持久化意图，再用单资源串行 drain 推进副作用，并把权限提示与真正隔离分开”：OpenCode 的 V2 Session 把 prompt admission、advisory wake、Location-scoped runner 和 durable event projection拆开；Claw Code 则展示了更小的 Rust loop、workspace 绑定和权限分类，同时也用源码与项目自述暴露出纯 lexical/命令启发式边界的局限。对 Hermes/shared hub 可迁移的是 durable admission + scoped drain + terminal reconciliation 契约，不是引入另一个完整 Agent runtime。**

## 研究范围与真实验证摘要

1. GitHub Search API 返回的高 Stars 候选包括 `obra/superpowers`、`NousResearch/hermes-agent`、`mattpocock/skills`、`anomalyco/opencode`、`deepseek-ai/deepseek-harness`、`ultraworkers/claw-code` 等。Superpowers、Hermes、skills、DeepSeek Harness 已在近日深读，今日选择尚未在本任务历史中深读的 OpenCode 与 Claw Code。
2. OpenCode repository API 快照为 **201,029 Stars / 26,023 Forks / TypeScript / MIT**，`updated_at=2026-08-24T23:34:30Z`、`pushed_at=2026-08-24T23:33:13Z`、default branch `dev`。固定提交是查询时浅克隆 HEAD `18b4cb6...`。
3. OpenCode 最新 release `v1.18.22` 发布于 `2026-08-24T14:37:19Z`；release notes 涉及 device-login URL、OpenAI-compatible `textVerbosity` 和 Bedrock 兼容修复。Issue #44807 报告 crashed run 留下 zombie running session、steer inbox 不再投递和 ghost form，说明 durable input 与 process-local active state仍需要 reconciliation。
4. OpenCode 固定提交共有 6,527 个 tracked files、`packages/` 下 36 个 `package.json`。本机没有 Bun（真实返回 `bun: command not found`），因此未安装依赖、未运行 package tests/typecheck/build；Actions 查询时最新相关 run 仍有 `in_progress/pending`，不能外推为该提交 CI 已通过。
5. Claw Code repository API 快照为 **195,110 Stars / 108,951 Forks / Rust / MIT**，`updated_at=2026-08-24T22:53:06Z`、default branch `main`，但 `pushed_at=2026-08-16T06:18:45Z`。README 明确称它是“agent-managed exhibit”而非严肃生产项目，这是采纳判断中的强边界。
6. Claw Code 没有可由 `releases/latest` 返回的 GitHub release，tags API 也未列出 tag；不能把 README 的 workspace version `0.1.3` 当 release。固定提交有 395 个 tracked files与 11 个 Rust crates。
7. 本机没有 Cargo（真实返回 `cargo: command not found`），所以 Rust compile/test/clippy/cargo-audit 均待核验；但仓库的 Python companion/audit suite 可运行，`python3 -m unittest discover -s tests` 真实返回 **47 tests passed / 0 failed，5.603s**。这不证明 Rust `claw` binary、sandbox、provider、MCP 或 permission runtime 已通过。
8. 两仓 Dependabot alerts API 都返回 HTTP 403，不能据此声称无已知漏洞。OpenCode 的 SECURITY 明确说明默认无 sandbox、permission 是 UX；Claw Code 的 SECURITY 把 path traversal、permission bypass、sandbox misreporting、plugin/hook/MCP/provider secret leak 列为安全范围。

## 项目速览

> 下表 Stars / Language / License / updated/pushed 均来自本次 GitHub repository API；Stars 是瞬时快照。仓库级 MIT 不自动覆盖依赖、模型服务、制品、商标或用户数据。

| 项目 | Stars | Language | License | updated / pushed (UTC) | 今日判断 |
|---|---:|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 277,104 | Shell | MIT | 2026-08-24T23:30:13Z / 2026-08-19T17:33:23Z | 高热；近日已深读，不重复 |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 235,773 | Python | MIT | 2026-08-24T23:30:32Z / 2026-08-24T22:18:09Z | 当前 Hermes 上游；近日已深读 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 235,348 | Shell | MIT | 2026-08-24T23:24:42Z / 2026-08-24T14:20:17Z | skills registry；近日已深读 |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 201,029 | TypeScript | MIT | 2026-08-24T23:34:30Z / 2026-08-24T23:33:13Z | **深读：durable input、scoped runner、reconciliation** |
| [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code) | 195,110 | Rust | MIT | 2026-08-24T22:53:06Z / 2026-08-16T06:18:45Z | **深读：小型 loop、workspace/permission 边界与反例** |
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 191,885 | TypeScript | MIT | 2026-08-24T23:32:28Z / 2026-08-21T12:35:08Z | 昨日已深读，不重复 |

## 深读项目

### 1. anomalyco/opencode

- **一句话判断**：值得学的是 V2 Session 将“请求已接收”“当前进程开始 drain”“模型/工具执行”“durable projection”拆成不同事实，避免调用方把一次 HTTP 返回或内存 running flag误认作业务完成。
- **解决的问题**：替代“prompt API 直接进入内存 tool loop、并发请求各跑一套 loop、历史只从当前内存 transcript 获取”的旧做法；输入先 durable admission，再通过可合并的 wake 触发 Session-ID 串行 drain，Location 决定 runner/tool/filesystem/model作用域。

#### 基本信息与可验证来源

- URL：https://github.com/anomalyco/opencode
- GitHub API：**Stars 201,029；Forks 26,023；Language TypeScript；License MIT**。
- API 时间字段：`updated_at=2026-08-24T23:34:30Z`，`pushed_at=2026-08-24T23:33:13Z`，open issues `5,390`，default branch `dev`。
- 固定提交：[`18b4cb6819d7de0b37927fef60d03927e678c9dd`](https://github.com/anomalyco/opencode/commit/18b4cb6819d7de0b37927fef60d03927e678c9dd)。
- Release：[`v1.18.22`](https://github.com/anomalyco/opencode/releases/tag/v1.18.22)，发布于 2026-08-24T14:37:19Z。
- Issue：[#44807](https://github.com/anomalyco/opencode/issues/44807) 为查询时 open 的真实故障报告；它描述 crash 后 process registry 仍显示 running、inbox steer 不投递、form reply/cancel 404，恢复依赖 interrupt + 删除 stuck inbox item。
- README：说明 build/plan/general agents 和多种安装面；SECURITY：明确 **No Sandbox**，permission 只是 UX awareness，真隔离需要 Docker/VM；server mode 无密码时未认证。
- 本机运行：没有 Bun，未运行 TS tests/build/typecheck。所有运行行为除静态源码/官方 issue 证据外均标记待核验。

#### 架构 / 实现与数据流

```text
HTTP/SDK/TUI prompt
       |
       v
SessionV2.prompt (uninterruptible)
  get session -> resolve prompt -> SessionInput.admit
  -> exact retry equivalence / conflict
       |
       +-- resume=false: admit only
       +-- default: SessionExecution.wake(sessionID)
                            |
                            v
                process-global coordinator
           same session serialized/coalesced
           different sessions may run concurrently
                            |
                            v
              resolve session.location at drain
   Location-scoped runner/model/tools/permissions/filesystem
                            |
                            v
     promote steer/queue -> durable projected history
     -> exactly one llm.stream per provider turn
     -> tool settle/events -> continuation/next queue
```

核心不是“多一层队列”，而是四个分离的语义面：

1. **Admission plane**：`session_input` 是 durable intent；同 message ID 只允许精确 retry，冲突重用失败。
2. **Scheduling plane**：`wake` 是 advisory；可合并，不代表执行完成。`resume` 可 join 当前同 Session 运行。
3. **Placement/effect plane**：drain 时才读取 Session 与 Location；runner/model/tool registry/filesystem 位于 Location scope。
4. **Truth/recovery plane**：每轮重新从 durable event/projected history构造请求；但源码规则也明确 process crash 后 provider work 自动恢复仍需要独立设计。

#### Repo tree 摘要（固定提交）

```text
opencode/
├── packages/
│   ├── core/                    # V2 Session、runner、DB、tool/provider、Location
│   │   └── src/session/
│   │       ├── input.ts         # durable admission / promote / equivalent
│   │       ├── execution/       # process-global wake/resume/interrupt routing
│   │       ├── run-coordinator.ts # per-session local serialization/coalescing
│   │       ├── runner/          # LLM turn、tool settle、continuation
│   │       ├── event.ts         # durable Session event vocabulary
│   │       ├── history.ts       # event/projected model history
│   │       ├── store.ts         # session projection/store
│   │       └── sql.ts           # session_input/message/event tables
│   ├── opencode/                # CLI/TUI/server 与 core adapter
│   ├── server/ protocol/ schema/# HTTP/RPC/schema 层
│   ├── app/ desktop/ tui/       # 用户界面 projections
│   └── sdk/ plugin/             # SDK 与扩展接口
├── patches/                     # 上游依赖补丁
├── specs/                       # 设计/迁移规格
├── script/                      # 生成、发布、仓库工具
├── bun.lock                     # Bun 精确依赖图
├── package.json                 # workspace catalog、trusted/patched deps
└── SECURITY.md                  # no-sandbox 与 server trust boundary
```

固定提交真实统计为 6,527 个 tracked files、36 个 package manifests；统计只说明仓库规模，不等于这些 package 已在本机验证。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/core/src/session.ts` | Session service/API | `prompt` 先 durable admit；exact retry 做等价校验；默认只发 advisory wake |
| `packages/core/src/session/input.ts` | input lifecycle | 区分 `steer` / `queue`，记录 admitted/promoted sequence，并提供 promote/hasPending |
| `packages/core/src/session/execution/local.ts` | 当前进程执行路由 | coordinator 按 Session ID组织 active/run/wake/interrupt；drain 时按 Location provision runner |
| `packages/core/src/session/run-coordinator.ts` | 同 Session 并发控制 | 同 Session wake 合并、resume join；不同 Session 可并发；状态只在当前进程 |
| `packages/core/src/session/runner/llm.ts` | provider turn + tools | promote durable input、重载 history、单次 `llm.stream`、并发 settle tool、处理 continuation/queue |
| `packages/core/src/session/sql.ts` | durable schema | `session_input` 保存 prompt、delivery、admitted/promoted sequence |
| `packages/opencode/src/session/session.ts` | 产品层 adapter | 组装 Database、Event bridge、Location map 与 local SessionExecution |
| `SECURITY.md` | 权限边界 | 明确 permission 不是 sandbox，server/MCP/provider 各有独立 trust boundary |

#### ⭐ 源码精读

**代码块 1：`V2Session.prompt`——先 durable admit，再 advisory wake；冲突 ID 失败**  
来源：[`packages/core/src/session.ts#L360-L385`](https://github.com/anomalyco/opencode/blob/18b4cb6819d7de0b37927fef60d03927e678c9dd/packages/core/src/session.ts#L360-L385)

```typescript
prompt: Effect.fn("V2Session.prompt")((input) =>
  Effect.uninterruptible(
    Effect.gen(function* () {
      yield* result.get(input.sessionID)
      const prompt = resolvePrompt(input.prompt)
      const messageID = input.id ?? SessionMessage.ID.create()
      const delivery = input.delivery ?? "steer"
      const expected = { sessionID: input.sessionID, messageID, prompt, delivery }
      const admitted = yield* SessionInput.admit(db, events, {
        id: messageID,
        sessionID: input.sessionID,
        prompt,
        delivery,
      })
      if (!SessionInput.equivalent(admitted, expected))
        return yield* new PromptConflictError({ sessionID: input.sessionID, messageID })
      if (input.resume !== false) yield* execution.wake(admitted.sessionID)
      return admitted
    }),
  ),
)
```

逻辑摘要：admission 位于 uninterruptible 区；调用方可提供稳定 message ID用于精确重试，但 session/prompt/delivery 任一不一致都会冲突；`resume=false` 只落库不唤醒。返回 admitted 只证明已接收，不证明模型或工具完成。

**代码块 2：`SessionExecutionLocal.layer`——drain 时解析 Location，coordinator 只掌管当前进程**  
来源：[`packages/core/src/session/execution/local.ts#L10-L36`](https://github.com/anomalyco/opencode/blob/18b4cb6819d7de0b37927fef60d03927e678c9dd/packages/core/src/session/execution/local.ts#L10-L36)

```typescript
const layer = Layer.effect(
  SessionExecution.Service,
  Effect.gen(function* () {
    const store = yield* SessionStore.Service
    const locations = yield* LocationServiceMap.Service
    const coordinator = yield* SessionRunCoordinator.make({
      drain: Effect.fnUntraced(function* (sessionID, force) {
        const session = yield* store.get(sessionID)
        if (!session) return yield* Effect.die(`Session not found: ${sessionID}`)
        return yield* SessionRunner.Service.use((runner) => runner.run({ sessionID, force })).pipe(
          Effect.provide(locations.get(session.location)),
        )
      }),
    })
    return SessionExecution.Service.of({
      active: coordinator.active,
      interrupt: coordinator.interrupt,
      resume: coordinator.run,
      wake: coordinator.wake,
    })
  }),
)
```

逻辑摘要：Session ID不是 Location service key；每次开始 drain 才从 store 读取 placement，再 provision Location-scoped runner。优点是移动/远程 placement 有单一 seam；边界是 coordinator process-local，跨进程 lease、crash ownership 与 stale active reconciliation不由这段代码解决。

**代码块 3：`SessionRunner.run`——steer 优先、queue逐个推进、同轮工具 continuation 继续**  
来源：[`packages/core/src/session/runner/llm.ts#L390-L417`](https://github.com/anomalyco/opencode/blob/18b4cb6819d7de0b37927fef60d03927e678c9dd/packages/core/src/session/runner/llm.ts#L390-L417)

```typescript
const run = Effect.fn("SessionRunner.run")(function* (input: {
  readonly sessionID: SessionSchema.ID
  readonly force: boolean
}) {
  const hasSteer = yield* SessionInput.hasPending(db, input.sessionID, "steer")
  const hasQueue = hasSteer ? false : yield* SessionInput.hasPending(db, input.sessionID, "queue")
  if (!input.force && !hasSteer && !hasQueue) return
  yield* failInterruptedTools(input.sessionID)
  let promotion = hasSteer ? "steer" : hasQueue ? "queue" : undefined
  let shouldRun = input.force || hasSteer || hasQueue
  while (shouldRun) {
    let needsContinuation = true
    let step = 1
    while (needsContinuation) {
      const result = yield* runTurn(input.sessionID, promotion, step)
      needsContinuation = result.needsContinuation
      step = result.step + 1
      promotion = "steer"
      if (!needsContinuation)
        needsContinuation = yield* SessionInput.hasPending(db, input.sessionID, "steer")
    }
    shouldRun = yield* SessionInput.hasPending(db, input.sessionID, "queue")
    promotion = shouldRun ? "queue" : undefined
  }
})
```

逻辑摘要：进入 drain 时 steer 优先；tool call 或新 steer 可让当前 turn继续；当前工作收敛后逐个处理 queue。`failInterruptedTools` 先把遗留 running tools终结，避免 projection永久悬挂。边界：issue #44807 显示 process registry/form/inbox 跨故障面的实际 reconciliation仍可能缺失，不能只凭此 loop 声称 crash-safe。

#### 依赖分析与供应链风险

- 根 `package.json` 使用 `bun@1.3.14` workspace；root `postinstall` 会进入 `packages/core` 执行 `fix-node-pty`，安装不是纯数据操作。
- `packages/core/package.json` 的核心依赖包含多家 `@ai-sdk/*` provider、AWS credential providers、Effect beta、Drizzle、OpenTelemetry、PTY、filesystem watcher、HTML parser、Git/npm utilities和 workspace schema/plugin/LLM 包。
- 根 manifest 明示 `trustedDependencies`，含 `esbuild`、`node-pty`、tree-sitter、Electron等 native/build surface；同时维护多项 `patchedDependencies`。升级不能只看版本范围，必须验证 patch仍适用。
- `effect`、Drizzle相关版本含 beta/RC；稳定性风险与供应链漏洞风险是不同维度。
- 本机没有 Bun，未执行 install、audit、test 或 build；Dependabot API 403。无法核验依赖 advisory 状态，明确标记**待核验**。
- 多 provider、MCP、shell、web、server、desktop、PTY 使 authority/egress 面很宽。SECURITY 明确 no sandbox，因此 permission prompt不能作为隔离证明。

#### README / release / issue /源码交叉结论

- README 把 plan agent描述为 read-only、bash 需确认；SECURITY 同时明确 permission只用于 UX awareness，不是 security isolation。两者并不矛盾，但要求报告把“默认行为”和“强安全边界”分开。
- Release `v1.18.22` 修复 provider/device-login等问题，说明 provider兼容层保持高频变化；不能把固定 dev HEAD 与 release完全等同。
- Issue #44807 的 zombie running症状与 `SessionExecution` process-local contract形成直接警示：durable inbox存在不等于 wake/active/form状态能在 crash后自动收敛。
- 源码把 prompt admission、wake、Location provision、history reload拆开，支持本文机制抽象；真实 crash复现与修复版本仍待核验。

#### 可复用经验

- 当外部请求必须在进程崩溃后仍可解释时，应优先先记录 durable admission，再发送可合并的 advisory wake，因为“已接收”与“已执行”是不同事实；边界是还需 lease/reconciler 与 terminal receipt。
- 当同一资源可被并发唤醒时，应优先按 immutable resource ID串行 drain、允许 join/coalesce，并让不同资源并行，因为每个请求各跑 loop会破坏顺序；边界是 process-local coordinator不能提供跨进程互斥。
- 当 session 可以移动到不同 workspace/backend 时，应优先在 drain开始时解析 current Location，并把 model/tool/filesystem/permission绑定到该 scope，因为旧 location snapshot可能失效；边界是 placement解析不是 authorization。
- 当 crash可能留下 running tool/form/inbox状态时，应优先在启动、wake与投递前运行 reconciliation，并输出 stale→terminal evidence，因为 process memory不可作为 durable liveness；边界是外部 effect是否发生可能只能标记 `needs_verification`。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/durable-session-drain/` 做纯 Python synthetic fixture：

1. SQLite表保存 `input_id/session_id/prompt_hash/delivery/admitted_seq/promoted_seq/terminal`。
2. `admit()` 验证 exact retry；同 ID不同 payload返回 conflict。
3. 内存 coordinator对同 session合并 wake，对不同 session并发；执行器只写 synthetic event，不调用 provider/shell/network。
4. 模拟“admit后 crash”“promotion后 crash”“tool running后 crash”，reconciler输出 `queued/resumable/needs_verification/terminal`。
5. 验收不是 stdout，而是 DB readback：每个 input恰好一个 durable terminal或显式 needs_verification。

#### 风险边界

- **License**：GitHub API与根 LICENSE均为 MIT；依赖、provider SDK、desktop assets、模型服务与用户输入受各自许可/条款约束。
- **维护活跃度**：dev branch在查询前数小时仍 pushed，release也在当日，维护很活跃；同时 open issues 5,390、变更频率高，固定 adapter容易漂移。
- **安全风险**：官方 SECURITY明确 no sandbox；server无密码可未认证运行；shell/file/web/MCP/provider具备高权或数据出域能力。
- **局限性**：本机无 Bun，未验证 compile/test/typecheck/audit；最新 Actions查询时未全部结束；V2 Session源码和 issue都处于快速变化期。
- **不适用场景**：不能直接作为多租户强隔离、无人值守高权 shell、跨进程 exactly-once或已证明 crash recovery的依据。
- **不能自动执行**：不运行 README 的 `curl | bash`；不安装 OpenCode，不启动 server，不配置 provider/secret/MCP，不修改 Hermes config/model/cron。

#### ⭐ Skill 升格判断

**需二次验证。** 候选是 agent-neutral 的 `durable-session-drain-contract`，不是 OpenCode Skill：`admit → exact-retry check → scoped wake/coalesce → promote → effect → reconcile → exactly-one terminal/needs_verification`。源码和真实 issue足以形成 POC假设，但本机没有 Bun、未复现 #44807、跨进程恢复边界未闭合。先做离线 fixture，并与现有 verification-first、subagent四状态、completion receipt和reflection engine去重；今日不创建 shared skill、不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **Hermes runtime POC**：`runtime/hermes/github-learning-poc/durable-session-drain/{schema.sql,engine.py,reconcile.py,fixtures/,test_engine.py,README.md}`。
2. **Hermes cron contract**：未来可让 orchestrator先 durable记录 `run_id/input_hash/target_path`，再执行；状态必须区分 `admitted/running/needs_verification/completed/failed`，但本次不改 cron或配置。
3. **审计接点**：`scripts/github_learning_orchestrator.py` 后续候选增加 artifact readback与 terminal检查，不能让内容关键词分数覆盖未完成执行。
4. **shared hub分层**：raw研究在 `inbox/hermes/daily/`；fixture/log在 `runtime/hermes/`；通过评分、证据、去重、脱敏和治理审查后才候选进入 `curated/memory/facts/` 或 `capabilities/skills/`。
5. **OpenClaw边界**：当前 OpenClaw runtime不存在，本次不实现、不调用；未来只能共享 schema/fixtures，由其自身 adapter证明 durable store、wake、effect和terminal语义。

### 2. ultraworkers/claw-code

- **一句话判断**：它适合作为“可读的小型 Agent loop与安全边界反例库”，不适合作为生产 runtime候选；项目自己明确称其为 museum exhibit，且当前权限层的 lexical path和命令 allowlist仍有已记录缺口。
- **解决的问题**：提供一个公开 Rust `claw` CLI、session persistence、provider/tool loop、permission、hooks/plugins/MCP和 parity harness；相较巨型单体 CLI，它按 crates分离 runtime/API/tools/commands/plugins，并用 mock service与 companion audit验证部分契约。

#### 基本信息与可验证来源

- URL：https://github.com/ultraworkers/claw-code
- GitHub API：**Stars 195,110；Forks 108,951；Language Rust；License MIT**。
- API 时间字段：`updated_at=2026-08-24T22:53:06Z`，`pushed_at=2026-08-16T06:18:45Z`，open issues `44`，default branch `main`。
- 固定提交：[`08106b0c3771ef5b4a5aa176acccd460e88b7325`](https://github.com/ultraworkers/claw-code/commit/08106b0c3771ef5b4a5aa176acccd460e88b7325)。
- Release/tags：`releases/latest` 返回 404；tags API未列出 tag。README 的 workspace version不能替代 release provenance。
- README：明确“not the serious production project”“agent-managed exhibit”；`rust/` 是 canonical实现，`src/` 是 Python companion/parity workspace。
- Issues：[#3295](https://github.com/ultraworkers/claw-code/issues/3295) 报告 nested frontmatter覆盖 root Skill metadata；[#3259](https://github.com/ultraworkers/claw-code/issues/3259) 报告流式 Markdown换行问题。两者查询时均 open。
- Actions：最近查询到一个 `Rust CI` run success和一个 `Rust` run success（head `d1638ec...`），另一个 run为 `action_required`；它们不是本机固定提交测试证据。
- 本机运行：Python companion suite **47 pass / 0 fail**；Cargo不存在，Rust compile/test/clippy/cargo audit均**待核验**。

#### 架构 / 实现与数据流

```text
claw CLI (rusty-claude-cli)
        |
        +--> config/session/provider selection
        |
        v
ConversationRuntime<C: ApiClient, T: ToolExecutor>
  push user -> build ApiRequest from session -> stream provider
        |
        v
assistant blocks -> collect ToolUse
        |
        v
PreToolUse hook -> permission policy/prompter -> ToolExecutor
        |
        v
PostToolUse/Failure hook -> ToolResult -> persist Session
        |
        +--> next model iteration / no tools => TurnSummary

side planes:
Session JSON/JSONL + workspace_root + atomic write
PermissionEnforcer lexical path / bash heuristic
plugins/hooks/MCP/provider adapters
mock Anthropic parity + Python companion audits
```

它的价值与边界同时很明确：

1. 泛型 `ApiClient` / `ToolExecutor` 让 loop可离线测试。
2. assistant tool use、permission和tool result都进入 Session message序列，利于恢复与审计。
3. `workspace_root`随 session持久化，防止多个 workspace共享全局 store时写错 CWD。
4. 但 permission layer部分依赖 lexical normalization和shell字符串启发式；源码注释主动承认 `sed w/e`、`awk system()`等 residual gaps，不能视为 sandbox。

#### Repo tree 摘要（固定提交）

```text
claw-code/
├── rust/                         # canonical Cargo workspace
│   ├── crates/
│   │   ├── rusty-claude-cli/     # claw binary / CLI dispatch
│   │   ├── runtime/              # session、conversation、permission、MCP、hooks
│   │   ├── api/                  # Anthropic/OpenAI-compatible provider clients
│   │   ├── tools/                # model tool definitions/dispatch
│   │   ├── commands/             # slash commands
│   │   ├── plugins/              # plugin manifest/lifecycle
│   │   ├── telemetry/            # request/analytics sinks
│   │   ├── compat-harness/       # parity extraction
│   │   ├── mock-anthropic-service/# deterministic provider fixture
│   │   ├── claw-analog/          # lean alternate harness
│   │   └── claw-rag-service/     # optional RAG service
│   ├── Cargo.toml                # 11 crates、unsafe_code=forbid
│   └── Cargo.lock                # locked Rust dependency graph
├── src/                          # Python companion/reference workspace
├── tests/                        # Python unittest suite；本次 47 pass
├── docs/                         # gate maps、platform/security topics
├── scripts/                      # fmt/dogfood/roadmap helpers
├── README.md / USAGE.md          # product/exhibit定位与使用说明
└── SECURITY.md                   # vulnerability scope与secret边界
```

固定提交真实统计为 395 个 tracked files、11 个 crates。目录小于 OpenCode，但 `runtime/src`仍包含大型 flat modules；规模小不等于边界简单。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `rust/crates/runtime/src/conversation.rs` | 模型/工具 loop | provider stream、assistant append、hook→permission→execute→post hook→tool result、max iteration |
| `rust/crates/runtime/src/session.rs` | session persistence | version/id/messages/compaction/fork/workspace_root；JSON/JSONL load；push失败回滚；atomic save |
| `rust/crates/runtime/src/permission_enforcer.rs` | permission checks | mode、workspace lexical containment、bash read-only allowlist；源码明确 residual gaps |
| `rust/crates/runtime/src/permissions.rs` | permission policy | tool required mode与prompter授权逻辑 |
| `rust/crates/runtime/src/hooks.rs` | pre/post tool hooks | tool input改写、deny/cancel/failure与反馈 |
| `rust/crates/runtime/src/file_ops.rs` | filesystem effect | workspace-aware variants；仍需 symlink/TOCTOU实测 |
| `rust/crates/runtime/Cargo.toml` | runtime依赖 | sha2/glob/regex/serde/tokio/walkdir + internal plugins/telemetry |
| `rust/Cargo.lock` | transitive closure | 应作为 cargo audit与reproducible build输入；本机未审计 |

#### ⭐ 源码精读

**代码块 1：`PermissionEnforcer::check_file_write`——mode + lexical workspace containment**  
来源：[`rust/crates/runtime/src/permission_enforcer.rs#L107-L142`](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/runtime/src/permission_enforcer.rs#L107-L142)

```rust
pub fn check_file_write(&self, path: &str, workspace_root: &str) -> EnforcementResult {
    let mode = self.policy.active_mode();
    match mode {
        PermissionMode::ReadOnly => EnforcementResult::Denied { /* ... */ },
        PermissionMode::WorkspaceWrite => {
            if is_within_workspace(path, workspace_root) {
                EnforcementResult::Allowed
            } else {
                EnforcementResult::Denied {
                    tool: "write_file".to_owned(),
                    active_mode: mode.as_str().to_owned(),
                    required_mode: PermissionMode::DangerFullAccess.as_str().to_owned(),
                    reason: format!("path '{path}' is outside workspace root '{workspace_root}'"),
                }
            }
        }
        PermissionMode::Allow | PermissionMode::DangerFullAccess => EnforcementResult::Allowed,
        PermissionMode::Prompt => EnforcementResult::Denied { /* confirmation required */ },
    }
}
```

逻辑摘要：ReadOnly拒绝写；WorkspaceWrite调用 `is_within_workspace`；Prompt在无交互 enforcer路径拒绝；更高模式允许。`is_within_workspace` 会折叠 `.`/`..`，比字符串前缀更好，但它不访问文件系统，不能解析 symlink、mount、case/Windows path或最终 inode；源码注释也明确是 lexical normalization。

**代码块 2：`ConversationRuntime::run_turn`——hook决策后才进入 tool executor，结果回写 session**  
来源：[`rust/crates/runtime/src/conversation.rs#L324-L367`](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/runtime/src/conversation.rs#L324-L367) 与 [L418-L517](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/runtime/src/conversation.rs#L418-L517)

```rust
pub fn run_turn(
    &mut self,
    user_input: impl Into<String>,
    mut prompter: Option<&mut dyn PermissionPrompter>,
) -> Result<TurnSummary, RuntimeError> {
    self.session.push_user_text(user_input.into())?;
    let mut iterations = 0;
    loop {
        iterations += 1;
        if iterations > self.max_iterations {
            return Err(RuntimeError::new(
                "conversation loop exceeded the maximum number of iterations",
            ));
        }
        let request = ApiRequest {
            system_prompt: self.system_prompt.clone(),
            messages: self.session.messages.clone(),
        };
        let events = self.api_client.stream(request)?;
        // build assistant message, append it, collect pending ToolUse...
        // pre-hook -> permission authorize -> tool_executor.execute
        // post-hook -> ConversationMessage::tool_result -> session.push_message
    }
}
```

逻辑摘要：Session先接收 user message；每次 provider请求从 session克隆完整 message history；max iterations提供终止边界；每个 tool依次经过 pre hook、permission/prompter、executor、post/failure hook，再把结构化 ToolResult追加到 session。边界：工具按顺序执行且 `max_iterations`默认在构造中是 `usize::MAX`，真实 CLI是否总设置合理 cap需调用链核验；hook input rewrite后的权限和执行共用 `effective_input`是正确方向，但 hook/plugin本身仍是高权代码。

**代码块 3：`Session::push_message`——持久化失败时回滚内存 append**  
来源：[`rust/crates/runtime/src/session.rs#L279-L297`](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/runtime/src/session.rs#L279-L297)

```rust
pub fn push_message(&mut self, message: ConversationMessage) -> Result<(), SessionError> {
    self.touch();
    self.messages.push(message);
    let persist_result = {
        let message_ref = self.messages.last().ok_or_else(|| {
            SessionError::Format("message was just pushed but missing".to_string())
        })?;
        self.append_persisted_message(message_ref)
    };
    if let Err(error) = persist_result {
        self.messages.pop();
        return Err(error);
    }
    Ok(())
}

pub fn push_user_text(&mut self, text: impl Into<String>) -> Result<(), SessionError> {
    self.push_message(ConversationMessage::user_text(text))
}
```

逻辑摘要：内存 append与持久 append不是事务，但失败会回滚刚追加的 message，避免内存历史领先于文件。边界：`touch()` 对 timestamp的修改不会在此回滚；跨进程追加、rotate/write race、fsync durability与partial external effects需要更强 storage/locking验证。

#### 依赖分析与供应链风险

- Workspace使用 Rust 2021、resolver 2、`unsafe_code = "forbid"`、`publish=false`；这降低 unsafe面，但不代表所有依赖无 unsafe/native code。
- Runtime直接依赖 `sha2`、`glob`、internal `plugins`、`regex`、`serde`、`serde_json`、internal `telemetry`、Tokio、`walkdir`；dev dependency为 `tempfile`。
- CLI另依赖 `crossterm`、`pulldown-cmark`、`rustyline`、`syntect`、tools/commands/api/plugins/runtime；RAG service引入 Axum、Reqwest、Rusqlite bundled和optional Qdrant，不能把 runtime的较窄依赖外推到整个产品。
- `rust/Cargo.lock`存在，但本机没有 Cargo，未运行 `cargo audit`、`cargo deny`、build或tests；Dependabot API 403，因此 advisory与license closure均**待核验**。
- Plugin/hook/MCP/provider和telemetry是代码执行/网络/secret面。README还要求 API key；本次没有配置或读取任何 key。

#### README / issue / SECURITY /源码交叉结论

- README主动说项目不是严肃生产项目，这比 Stars更应影响采纳：高 Stars不构成维护承诺、release稳定性或安全证明。
- README把 `rust/` 定义为 canonical；因此本机 Python 47 pass只能证明 companion/audit工具，不能证明 Rust runtime。
- Issue #3295 指向 frontmatter parser将缩进键误认成顶层键，说明 Skill metadata是 untrusted structured input，不能只靠 trim+key match。
- SECURITY把 workspace traversal、permission bypass、sandbox misreporting、plugin/hook/MCP/provider secret leak列为 in scope；permission_enforcer源码中的 lexical/heuristic实现正是需要重点验证的边界。
- 最近 default branch pushed时间早于查询约九天；issues/Actions仍有活动，但没有 latest release/tag。维护活跃度低于 OpenCode且制品契约不清。

#### 可复用经验

- 当 session与全局 store可被多个 workspace共享时，应优先把 canonical workspace identity随 session持久化，并在最终文件副作用点重新解析 real target，因为 CWD不是稳定身份；边界是 lexical path不能解决 symlink/TOCTOU。
- 当权限判断涉及 shell时，应优先解析结构化 argv/AST并对未知形式 ask/deny，而不是维护“看起来只读”的首 token allowlist，因为 wrapper、interpreter、`sed`/`awk`脚本可产生副作用；边界是 parser仍不能替代 OS sandbox。
- 当工具有 pre/post hooks时，应优先让 hook改写后的 effective input参与同一次授权与执行，并把 deny/failure/cancel变成 ToolResult，因为对原 input授权会造成检查-执行偏差；边界是 hook来源与自身权限还要审计。
- 当内存状态需要落盘时，应优先在持久化失败时回滚内存 projection并保留 typed error，因为“内存已更新”不能冒充 durable完成；边界是时间戳、跨进程CAS和外部 effect仍需事务/receipt。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/workspace-effect-boundary/` 建纯 Python fixtures：

1. 输入 workspace root、relative/absolute path、symlink chain、missing target和expected effect。
2. 对比 lexical normalize与 `realpath(parent)+openat/no-follow`式决策结果；只在临时目录创建文件。
3. shell corpus覆盖 `cat`、pipe、redirect、subshell、`find -exec`、`sed w`、`awk system()`、解释器；unknown统一 `blocked`。
4. 输出 `requested_path/resolved_parent/inode_before/effect/decision/reason/terminal` receipt。
5. 不运行真实用户命令，不修改 Hermes config/cron/skills。

#### 风险边界

- **License**：GitHub API与workspace/root LICENSE为 MIT；依赖、上游兼容材料、模型服务和品牌资产仍需分别核验。
- **维护活跃度**：repository updated到 8月24，但 default branch最后 pushed为 8月16；无 latest release或tag；README明确 exhibit定位，不能期待生产 SLA。
- **安全风险**：permission是应用层规则；lexical containment不处理 symlink/TOCTOU；read-only shell heuristic有源码承认的 residual gaps；plugins/hooks/MCP/provider/telemetry扩大权限与secret面。
- **局限性**：本机无 Cargo，Rust binary完全未编译/运行；47个 Python tests不能外推；Actions是其他 head的上游信号，不是本机证据。
- **不适用场景**：生产高权 Agent、多租户隔离、Windows/Linux一致强文件边界、无人值守 secret/provider任务和要求稳定发布制品的系统。
- **不能自动执行**：不运行 `install.sh`，不设置 provider key，不启动 MCP/plugin/RAG，不复制源码到 shared，不把高 Stars当采纳授权。

#### ⭐ Skill 升格判断

**暂不沉淀。** 可学习的 workspace binding、effective-input authorization和persistence rollback已与现有 verification/effect-scope候选高度重叠；项目定位是 exhibit，本机Rust lane blocked，权限实现还有明确 heuristic gaps，且无 release/tag provenance。今日只保留 raw研究和 open question，不创建 Hermes本地 skill或 shared skill；若未来只抽象 `workspace-effect-boundary`，必须独立实现 fixtures而非复制上游代码。

#### Hermes / shared hub 落地路径

1. **仅 runtime实验**：候选目录 `runtime/hermes/github-learning-poc/workspace-effect-boundary/`；不进入 `~/.hermes/skills/` 或 `capabilities/skills/`。
2. **Hermes工具审计**：未来可对 file/shell工具增加 host-stamped `workspace_id/resolved_target/effect`和post-effect readback；模型不能声明自己是 read-only。
3. **shared hub路径**：本报告留在 `inbox/hermes/daily/`；实验日志留 `runtime/hermes/`；没有达到 curated或shared skill晋升条件。
4. **OpenClaw边界**：runtime不存在，本次完全不调用；未来若接入同一 agent-neutral fixture，也必须由独立 host adapter验证 realpath、permission和terminal，不共享本地配置或secret。

## 经验沉淀

1. 当请求接收与副作用执行之间存在排队、并发或故障窗口时，应优先拆分 durable admission、advisory wake、scoped drain、reconciliation和terminal receipt，因为任一单步成功都不能代表业务完成；边界是外部副作用不确定时必须进入 `needs_verification`。
2. 当同一 Session/任务会收到多个并发唤醒时，应优先按 immutable resource ID合并 wake并串行 drain，而让不同资源并行，因为全局串行浪费吞吐、每请求独立 loop破坏顺序；边界是跨进程仍需 lease/ownership。
3. 当 session/workflow可迁移 workspace或backend时，应优先在最终执行开始时解析 current location与canonical target，因为 admission时的 CWD/path可能已陈旧；边界是 location identity不能替代 effect authorization。
4. 当权限策略声称 read-only或 workspace-only时，应优先使用结构化 effect metadata、real target resolution和OS isolation，而不是 shell首 token或 lexical prefix，因为字符串启发式存在 wrapper、symlink和TOCTOU绕过；边界是 sandbox也要独立验证网络/credential挂载。
5. 当 crash可能留下 running tool、form、inbox或内存 active entry时，应优先提供启动/wake前reconciler与stale-to-terminal evidence，因为 durable input与process liveness属于不同事实面；边界是不能安全重试的effect只可park。
6. 当热门项目Stars极高但项目自述为 preview、exhibit或 no-sandbox时，应优先相信固定源码、release/issue/security边界和本机验证，而不是热度，因为Stars不证明稳定性、安全性或适用性。
7. 当某项目模式与既有shared候选重叠且本机关键toolchain blocked时，应优先保留raw/open question而暂不升格，因为重复skill会造成行为漂移；边界是后续新证据可重新评分。

### 今日可尝试的统一实验

优先实现 `runtime/hermes/github-learning-poc/durable-session-drain/`，只用 SQLite和synthetic events验证 admission/exact retry/coalesced wake/reconcile/terminal；第二个 workspace实验留作明日候选。任何实验都不接provider、MCP、真实shell，不改Hermes配置、模型、cron、auth或shared active skill。

## Skill 升格总判断

- `anomalyco/opencode`：**需二次验证**。只抽象 `durable-session-drain-contract`；先复现 admission/crash/reconcile fixtures并与现有 verification-first、subagent四状态、completion receipt去重。
- `ultraworkers/claw-code`：**暂不沉淀**。项目定位、无本机Rust验证、无release provenance和permission heuristic gaps不足以支持skill化。
- 今日不创建 `capabilities/skills/`，不更新 shared skill manifest，不写 curated active facts。候选必须经过评分、证据、去重、脱敏和治理审查。

## 明日继续

1. 用30分钟实现 `durable-session-drain`最小SQLite fixture，至少覆盖 exact retry conflict、admit后crash、同Session wake coalesce、tool running后reconcile、exactly-one terminal。
2. 继续追踪 OpenCode issue #44807 是否出现修复提交或reproduction test；固定新commit后只做源码diff，不安装产品。
3. 若环境获得Bun，先在 `packages/core` 按仓库规则运行最窄 Session tests/typecheck；若仍无Bun，保持 blocked，不拿Actions替代本机验证。
4. Claw Code仅在获得Cargo后考虑运行 `cargo test -p runtime permission_enforcer`等最窄测试；在此之前不晋升其模式。

## 候选反哺

### Candidate Facts

- [ ] topic: durable admission 与 process-local wake/active state必须分开，并需要 crash reconciliation | evidence: `anomalyco/opencode@18b4cb6` 的 `packages/core/src/session.ts`、`execution/local.ts`、`runner/llm.ts` 与 open issue #44807 | 建议: create candidate only | 安全级别: medium
- [ ] topic: workspace lexical containment和shell read-only allowlist不能作为强隔离 | evidence: `ultraworkers/claw-code@08106b0` 的 `permission_enforcer.rs` 源码注释、SECURITY范围 | 建议: create candidate only / 与effect-scope去重 | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: durable-session-drain-contract | 可复用场景: Hermes cron、长任务、跨会话队列、Agent tool continuation | 是否建议 shared: yes（仅二次验证后） | 原因: 跨agent可复用，但必须先有exact-retry/crash/reconcile/terminal fixtures和host adapter契约
- [ ] 名称: workspace-effect-boundary | 可复用场景: file/shell工具的workspace containment与effect receipt | 是否建议 shared: no（当前） | 原因: 与现有effect-scope/verification候选重叠，且本机Rust边界未验证

### Candidate Open Questions

- [ ] 问题: OpenCode #44807 的 zombie active/form/inbox状态分别由哪些store拥有，修复应放在wake、startup还是transport reconciliation？ | reason: gap | priority: high
- [ ] 问题: Hermes现有cron/session路径是否已经有durable admission与exact retry identity，还是只有最终status.json？ | reason: adaptation | priority: high
- [ ] 问题: Hermes file tools最终chokepoint是否能提供real target/inode/owner/effect receipt，而不只验证字符串路径？ | reason: gap | priority: medium
- [ ] 问题: Claw Code permission_enforcer在symlink、Windows path和shell adversarial corpus上的Rust tests实际结果是什么？ | reason: blocked | priority: low

### 不应自动落地

- 不安装或启动 OpenCode/Claw Code，不执行 `curl | bash` 或第三方 installer。
- 不调用OpenClaw；当前runtime不存在。
- 不自动改 Hermes/OpenClaw config、model、provider、cron、auth、env或secret。
- 不把candidate直接写成 curated active fact，不创建shared active skill，不复制第三方源码。
- 不把Stars、上游Actions、README声明、Python companion tests或schema-valid结果外推为生产安全/完成。
