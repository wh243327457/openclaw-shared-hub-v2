---
type: case
status: archived
created: 2026-09-05
updated: 2026-09-05
domain: learning
tags: [github-learning, local-inference, lifecycle, cross-agent-skills, verification]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
  - "[[03-学习/技术实践/00-技术实践索引]]"
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-09-04-GitHub热门项目学习日报]]"
---

# 2026-09-05 GitHub 热门项目学习报告

> 执行者：Hermes（OpenClaw 运行时不存在；本次未调用 OpenClaw）  
> 查询时间：2026-09-05T07:31:08+08:00 至 07:38:12+08:00  
> 发现方法：真实读取 GitHub Trending daily，并用 GitHub repository/license/commit/release/issues/check-runs API 核验；项目速览中的 Stars、Forks、Language、License、`updated_at`、`pushed_at` 均以 07:38:12+08:00 API 快照为准。  
> 深读固定提交：`magnitudedev/magnitude@0851902d63b8698618aa8dbc78e6ac0f996a7b7e`；`DietrichGebert/ponytail@974d940a1c5344210874150b98ff0d2c861fab6a`。动态热度快照与固定源码 revision 分开记录。

## 今日结论

**Agent 工程里真正可迁移的不是“自动化更多”，而是把 authority、identity、终态、适配层和验证边界显式化：Magnitude 用精确进程身份、单一 owner fact、纯 convergence decision 与 at-most-once ambiguity 控制本地 daemon；Ponytail 用 canonical skill、薄 host adapter、drift checker 与行为 benchmark 控制跨 Agent 规则，但两者当前都存在“文档/测试看似完整，真实边界仍有洞”的反例。**

### 今日真实验证摘要

- Magnitude：固定 HEAD `0851902...`，通过 `npx -y bun@1.3.14 install --frozen-lockfile --ignore-scripts` 安装 1,046 packages；5 个核心测试文件真实结果 **27 pass / 0 fail**。先运行 `dev:version` 后，`packages/sdk` 与 `packages/providers` typecheck 均成功。`packages/utils` typecheck 真实失败，与开放 issue #74 所述旧 `packages/protocol` 导入一致，另含项目刻意保留的 schema compile-error fixtures。
- Magnitude 供应链：`bun audit` 真实返回 **25 vulnerabilities（1 critical / 14 high / 7 moderate / 3 low）**，涉及 `tar`、`fast-uri`、`toml`、`dompurify`、`qs`、`@tootallnate/once`；这是 lockfile 级命中，不代表每条均可达，但足以阻止“无已知漏洞”的结论。
- Ponytail：初次根 `npm test` 因本机缺 pandas 导致唯一 CSV correctness fixture 失败（**83 pass / 1 fail**）；在隔离 venv 安装 pandas 后重跑，根 suite **84/84**、pi extension **23/23**、MCP **3/3**，全部成功。另行执行 canonical rule-copy checker 成功，4 个核心 adapter files **28/28**。
- Ponytail 供应链：根仓没有 lockfile、根 package 没有 runtime dependencies；MCP 子包使用临时 lock 解析后 `npm audit --omit=dev` 为 **0 known vulnerabilities**。这不覆盖未锁定的 future resolution、宿主 Agent、外部模型、复制到其他 host 的脚本或未知漏洞。
- 两仓 `SECURITY.md` contents API 都返回 404，公开 repository security-advisories API 都返回空数组；不能据此声称安全。Magnitude 固定提交 check-runs 只有 `version=success`、Mintlify skipped；Ponytail 固定提交上游 `test=success`，本机结果仍单独记录。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | 250,306 | 21,152 | Shell | MIT | 2026-09-04T08:45:43Z | 今日 Trending；近期已多次研究，避免重复 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 248,477 | 37,450 | JavaScript | MIT | 2026-09-04T19:02:58Z | Agent harness 候选；历史已有学习记录 |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 241,472 | 49,551 | Python | MIT | 2026-09-04T23:35:26Z | 当前 Hermes 上游；历史已深读，今日不重复 |
| [anthropics/skills](https://github.com/anthropics/skills) | 174,117 | 20,639 | Python | NOASSERTION | 2026-09-03T16:37:14Z | 跨 Agent skill 参考；license 需逐目录核验 |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 125,905 | 6,762 | JavaScript | MIT | 2026-09-04T12:35:29Z | **深读：canonical rule、薄 adapter、漂移测试与 session-state 反例** |
| [blader/humanizer](https://github.com/blader/humanizer) | 42,676 | 3,606 | Python | MIT | 2026-08-19T05:58:53Z | 风格治理候选；与今日 authority 主线关联较弱 |
| [fmtlib/fmt](https://github.com/fmtlib/fmt) | 25,459 | 3,035 | C++ | MIT | 2026-09-04T23:27:22Z | 成熟格式化库；不作为 Agent 架构深读 |
| [magnitudedev/magnitude](https://github.com/magnitudedev/magnitude) | 2,448 | 174 | TypeScript | Apache-2.0 | 2026-09-04T21:36:23Z | **深读：JIT daemon 收敛、恢复语义、本地模型 evidence** |

> 注：Stars 会继续变化，表中是同一时间窗口的 repository API 总量，不使用 Trending 页的 “stars today”。GitHub `open_issues_count` 包含 PR：另行筛选后 Magnitude 为 14 个开放 issue、Ponytail 为 33 个开放 issue。License API 只核验仓库根许可，不能替代依赖、模型权重、数据、release asset 与宿主平台条款审查。

## 深读项目

### 1. magnitudedev/magnitude

- **一句话判断**：值得学的不是“又一个本地模型服务器”，而是它把 daemon replacement、模型 evidence、mutation acknowledgement 和 transport ambiguity 拆成有明确 authority 的协议；但当前供应链审计、高权本地 dashboard 与 monorepo typecheck 仍不满足无人值守生产接入条件。
- **解决的问题**：替代“Agent 猜硬件、猜量化、手工下载模型、按 PID/端口判断 daemon 可用、断线后一律重试”的旧做法；其目标是统一 profile → recommend → acquire → assess → serve，并允许 Hermes 等 harness 通过 provider/CLI 接入。
- **URL / API 快照**：https://github.com/magnitudedev/magnitude ；**Stars: 2,448 / Forks: 174 / Language: TypeScript / License: Apache-2.0**；`created_at=2026-06-12T09:06:26Z`，`updated_at=2026-09-04T23:35:53Z`，`pushed_at=2026-09-04T21:36:23Z`，repository API `open_issues_count=19`，default branch `main`。
- **固定提交**：[`0851902d63b8698618aa8dbc78e6ac0f996a7b7e`](https://github.com/magnitudedev/magnitude/commit/0851902d63b8698618aa8dbc78e6ac0f996a7b7e)，commit API 时间 `2026-09-04T18:42:23Z`；该提交修复 OpenAI image body total limit 与 per-image limit 冲突。
- **Release / issue 证据**：latest release 为 `@magnitudedev/cli@0.0.11`，发布于 `2026-09-02T05:57:36Z`。开放 issue [#66](https://github.com/magnitudedev/magnitude/issues/66) 报告本地 dashboard 的 wildcard CORS + 无鉴权 `POST /api/acns/kill-all` 可被网页触发；固定源码静态核验确认 `127.0.0.1:4886`、`Access-Control-Allow-Origin: *` 与无额外 gate 的 kill route 同时存在。issue #74 报告 rename 后旧 import，本机 typecheck 复现。issue #62 的长推理 502/worker drop 本机未复现，**待核验**。
- **来源交叉核验**：README、docs、4 份 design contracts、fixed source、GitHub API/release/issues/check-runs、本机 lock 安装、27 个定向 tests、两个 package typechecks 与 `bun audit`。

#### 架构/实现与数据流

1. CLI/desktop/web 作为 client；`packages/sdk` 持有连接、JIT daemon 管理与 query/mutation client；ACN（agent control node）是 Agent/模型管理 authority；ICN/native inference 负责物理模型实例与硬件事实。
2. 多个 host client 共享同一 data root 时，不使用常驻 coordinator；SQLite singleton owner row 只保存精确 `pid + processStartIdentity + port`，revision 来自活进程 health，不被持久化为选举权威。
3. `AcnOwnerObserver` 读取 owner/process/health，纯 `AcnConvergenceDecider` 决定 wait/prepare/launch/shutdown/confirm/fail，`AcnEnsuranceCoordinator` 只执行决定；启动、停止、观察权限彼此分离。
4. candidate 在 admission 前只绑定 health/shutdown endpoint，不启动应用或 inference；CAS 风格 `replaceOwner(expected,candidate)` 成功后才获得 authority。ready adoption 还会再次确认 owner 与精确进程发生实例。
5. RPC transport 根据 operation recovery policy 区分可重放与 at-most-once mutation。若 transport 失败可能发生在 dispatch 之后，返回 typed `RpcOutcomeUnknown`，调用者必须从 authoritative state reconcile，不可自动 replay。
6. 模型 catalog 将 API schema 解码、capability/property 分类与 5 分钟 cache 分开；模型“适合当前硬件”必须来自 native assessment 的 `Fits` evidence，不以 authored metadata 或 cache 单独授权加载，admission 再以当前资源复验 memory fit。
7. 用户侧 mutation、resource query、presentation state 分开：mutation success 代表 owner commit/admission，不等于 physical model Ready；query cache 只影响成本/延迟，不改变语义。

```text
Hermes / CLI / desktop / web
  -> SDK connection + Effect Query
  -> JIT ensure(target revision)
       -> observe owner row + exact process + health
       -> pure convergence decision
       -> prepare / launch / fenced replace / confirm ready
  -> ACN (agent & product state owner)
       -> ICN (hardware + physical model instance owner)
       -> native inference worker
  -> OpenAI-compatible/provider stream
```

#### repo tree 摘要

```text
magnitude/                              # 2,269 tracked paths
├── cli/                                # TUI client、onboarding、provider/model interaction（301）
├── desktop/                            # Electron host
├── web/                                # React UI（124）
├── packages/                           # TS monorepo core（1,478）
│   ├── sdk/                            # JIT ACN、recovering RPC、Effect Query client
│   ├── acn + acn-protocol/             # Agent/control authority 与跨版本协议
│   ├── icn + icn-protocol/             # 本地模型/硬件/worker control
│   ├── providers + ai/                 # provider、catalog、model capability contract
│   ├── agent + harness + skills/       # Agent loop、tools、roles、skills
│   └── storage/event-core/vcs/...      # state、event、Git 等支撑层
├── inference/                          # Rust native inference workspace（204；87 个 .rs）
├── design/                             # 69 份 architecture/domain contracts
├── docs/                               # 面向用户的 onboarding/models/reference 文档
├── bun.lock                            # JS/TS 锁文件
└── inference/Cargo.lock                # Rust 锁文件
```

> `git ls-files` 实查 2,269 个 tracked paths、1,773 个 `.ts/.tsx`、87 个 `.rs`、408 个 test paths/signals。仓库不是一个可直接嵌入 Hermes 的小 provider package，而是带 CLI、desktop、web、ACN、ICN 和 native backend 的完整产品面。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `design/acn/lifecycle/cross-version-coordination-protocol.md` | 跨版本稳定面 | durable fact 只保留 singleton owner；replace 是短事务；health/精确进程共同决定 authority |
| `packages/sdk/src/acn-jit/acn-convergence-decider.ts` | sans-I/O 收敛策略 | 将 observation/candidate/time 映射成 typed action；health/start/stop 有固定 deadline |
| `packages/sdk/src/acn-jit/acn-ensurance-coordinator.ts` | decision executor | 观察、更新连续性时间、协调 candidate、执行 prepare/launch/shutdown/confirm |
| `packages/sdk/src/jit-rpc/recovering-protocol.ts` | transport recovery | stream 重连、endpoint retirement、at-most-once ambiguity、typed protocol violation |
| `packages/sdk/src/mutation-outcome.ts` | 不确定副作用识别 | 将 `RpcOutcomeUnknown` 暴露给 caller 进行 authoritative reconcile |
| `packages/providers/src/magnitude/catalog.ts` | 模型清单投影 | schema decode、capability/property 映射、TTL cache、refresh/get |
| `design/model-management/assessment-and-ranking.md` | 模型 evidence authority | Fits/DoesNotFit/Incompatible 为终态；缺证据不填 0；cache 不授权 admission |
| `packages/acn-dashboard/src/server.ts` | 本地调试 dashboard | loopback server、ACN introspection、kill-all route；当前 #66 高权边界缺陷所在 |

#### ⭐ 源码精读

**代码块 1：`decideAcnConvergence()` 是纯决策核，未知健康不会立刻抢 ownership。**

```ts
export const decideAcnConvergence = (
  snapshot: AcnConvergenceSnapshot,
): AcnConvergenceDecision => {
  const { candidate, observation, now } = snapshot
  if (candidate._tag === "Failed")
    return { _tag: "FailCandidate", failure: candidate.failure }
  if (observation._tag === "AcnRecordedOwnerAbsent")
    return candidate._tag === "NotLaunched"
      ? { _tag: "LaunchCandidate" }
      : { _tag: "Wait" }
  if (observation._tag === "AcnRecordedOwnerLiveWithoutHealth")
    return now - snapshot.healthStateObservedAt >= Duration.toMillis(HEALTH_GRACE)
      ? shutdown(observation.owner, "HealthUnavailable")
      : { _tag: "Wait" }
  // revision / Ready / Starting / Stopping 分支继续返回 typed decision
}
```

逻辑摘要：owner absent、process-group survivor、health unavailable、lower revision、starting timeout 与 ready confirmation 都是不同输入状态；30 秒 health grace、5 分钟 startup ceiling、5 秒 stopping grace 是显式策略。边界是纯函数只保证 decision 可测，observer 的 OS/process/health 证据和 executor 的 effect 正确性仍需各自验证。

**代码块 2：`makeAcnEnsuranceCoordinator()` 只协调窄 authority，并在 ConfirmReady 时再次确认。**

```ts
export const makeAcnEnsuranceCoordinator = (
  options: MakeAcnEnsuranceCoordinatorOptions,
): Effect.Effect<AcnEnsuranceCoordinator> => Effect.gen(function* () {
  const prepared = yield* Ref.make(Option.none<AcnDaemonLaunchCommand>())
  const coordinate = Effect.gen(function* () {
    while (true) {
      const observation = yield* options.ownerObserver.observe
      const candidate = yield* options.candidateSupervisor.reconcile(
        liveObservationOwner(observation),
      )
      const decision = AcnConvergenceDecider.decide({ /* snapshot */ })
      switch (decision._tag) {
        case "LaunchCandidate":
          yield* options.candidateSupervisor.launch((yield* prepare).command)
          break
        case "ConfirmReady": {
          const ready = yield* options.ownerObserver.confirmReady(
            decision.owner, decision.observed,
          )
          if (Option.isSome(ready)) return ready.value
          break
        }
      }
    }
  })
  return AcnEnsuranceCoordinator.of({ run: coordinate.pipe(Effect.timeoutFail(/* 10m */)) })
})
```

逻辑摘要：coordinator 不直接实现 process observation、shutdown 或 launch policy；ready 不是一次 HTTP 200 就采用，而是交给 observer 做 final confirmation。边界是完整可靠性还依赖 SQLite transaction、process-start identity、shutdown escalation 与 candidate finalizer，不应只复制 coordinator 外形。

**代码块 3：`makeRecoveringProtocol()` 对 at-most-once RPC 的模糊结果停止 replay。**

```ts
const definitelyNotDispatched = failure._tag === "BadResponseStatus" &&
  (failure.status === 409 || failure.status === 503)
if (!isStream && policy === "AtMostOnce" && !definitelyNotDispatched) {
  yield* options.recover(endpoint).pipe(Effect.ignore, Effect.forkIn(protocolScope))
  return yield* toRpcClientError(new RpcOutcomeUnknown({ tag: request.tag }))
}
yield* options.recover(endpoint).pipe(
  Effect.mapError(options.classifyInfraError),
)
```

逻辑摘要：如果 409/503 明确表示未 dispatch，可以恢复后再发；否则 mutation 可能已经到达 daemon，transport 层只恢复 endpoint 并返回 outcome unknown。边界是 caller 必须有 authoritative query 与 idempotency/reconciliation 逻辑；仅抛 typed error 不会自动消除重复 effect。

**代码块 4：`createMagnitudeCatalog()` 的 cache 只是投影，不是 availability authority。**

```ts
export function createMagnitudeCatalog(
  config: MagnitudeCatalogConfig,
): ModelCatalog<MagnitudeModelInfo> {
  let cache: readonly MagnitudeModelInfo[] | null = null
  let fetchedAt = 0
  const list = Effect.gen(function* () {
    if (cache && Date.now() - fetchedAt < (config.ttlMs ?? 300_000)) return cache
    const models = yield* fetchModels
    cache = models
    fetchedAt = Date.now()
    return models
  })
  const refresh = Effect.gen(function* () {
    const models = yield* fetchModels
    cache = models
    fetchedAt = Date.now()
    return models
  })
  return { list, get, refresh }
}
```

逻辑摘要：API response 经 schema 解码后才进入 cache，family classification 是 metadata 而非 availability gate。`assessment-and-ranking.md` 进一步规定 loading 只能消费完成 assessment，并在 admission 重验当前 memory fit。边界是今日没有下载模型或运行 native assessment，因此“推荐速度/适配质量”仍**待核验**。

**代码块 5：固定 HEAD 的 dashboard kill route 静态确认 #66 所述组合。**

```ts
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
}
const server = Bun.serve({
  port: Number(process.env.ACN_DASH_API_PORT ?? 4886),
  hostname: '127.0.0.1',
  async fetch(req) {
    if (path === '/api/acns/kill-all' && req.method === 'POST') {
      return json({ results: await killAllAcns(), timestamp: Date.now() })
    }
  },
})
```

逻辑摘要：loopback 只限制网络可达位置，不阻止浏览器从任意网页发 simple POST；wildcard CORS 又扩大读响应能力。项目方已在 issue 中承诺补 safeguard，但固定 commit 尚无 header/token/origin gate。本机未启动 server、未实际杀进程；漏洞触发链依 issue + 源码静态一致性确认，动态 exploit **未执行**。

#### 依赖分析与供应链风险

- 根 `package.json` 使用 Bun workspace + Turbo；核心 TS 依赖以 Effect 生态为主：`effect ^3.21.2`、`@effect/platform ^0.96.0`、`@effect/rpc 0.75.1`、Effect Atom、OpenTelemetry。CLI/UI 还含 React 19、Electron、Monaco、Svelte、Shadcn；native inference 为 Rust/Cargo workspace。
- `bun.lock` 与 `inference/Cargo.lock` 存在，但 package manifests 大量使用 caret ranges；lock 能固定当前 install，不代表未来更新安全。`packages/markdown-cst` 甚至对 micromark 依赖使用 `*`，需要额外 review。
- 本机 `bun audit` 返回 25 advisories；其中 `tar` 链含 critical/high 路径，`fast-uri` 含 SSRF/host confusion，`dompurify` 含 XSS/配置污染。是否可达取决于 desktop archive、web content、tooling 等实际调用路径，本日未做 reachability analysis，故逐条标为“已知 advisory 命中，利用性待核验”。
- `npx bun install --frozen-lockfile --ignore-scripts` 成功，降低 install-script effect，但不等于 release installer/download/native artifact 安全；本日未执行 bootstrap、setup、模型下载、release acquisition 或 native worker。
- `packages/sdk/providers` typecheck 需先生成 `version.generated`；直接 typecheck 会失败，先跑 `dev:version` 后两者成功。`packages/utils` 仍真实 fail，说明固定 HEAD 不是全 monorepo 绿色状态。
- GitHub Actions/check-runs 在固定 HEAD 只显示 version success 和 docs skipped，不能用来外推完整 build/test/security。

#### 可复用经验

- 当多个 client 可能同时启动或替换同一 daemon 时，应优先用“最小 durable owner fact + 精确进程发生身份 + CAS replacement + lifetime monitor”，因为 PID/端口/HTTP 200 单独都可能陈旧；边界是 OS identity 和 store transaction 必须真实可靠。
- 当 daemon RPC 可能已经 dispatch 但 ACK 丢失时，应优先返回 `outcome_unknown/needs_verification` 并从权威状态 reconcile，而不是自动 replay at-most-once mutation；因为恢复连接不等于恢复 effect 确定性，边界是 query 也必须能绑定同一 operation/target identity。
- 当硬件建议决定模型下载或加载时，应优先把 authored catalog、native assessment、当前 resource admission 分成三层 evidence，因为 metadata/cached Fits 不能证明此刻仍可加载；边界是 assessment 本身需固定模型 artifact 与硬件 revision。
- 当本地服务提供 destructive debug endpoint 时，应优先把 loopback 当网络范围而非授权，并增加 origin/action-token/CSRF-style gate 与权限测试；因为恶意网页可访问 loopback，边界是 token 仍需保密、轮换和最小权限。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/exact-owner-outcome-unknown-v0/` 做纯 Python/TypeScript synthetic fixture：

1. 定义 owner `(pid, process_start_identity, endpoint, revision)` 与 observation snapshots；
2. 证明 PID reuse、stale owner、inconclusive health、lower/newer revision 不会被误 adopt；
3. 对 replay-safe query 与 at-most-once mutation 注入“dispatch 后断线”，后者只能进入 `needs_verification`；
4. reconciliation 必须读取匹配 `operation_id + target_id + revision` 的 authoritative state；
5. 输出 exactly-one terminal：`completed|blocked|needs_verification|failed`。不安装 Magnitude、不下载模型、不启动 dashboard/daemon、不修改 Hermes/provider/config/cron。

#### 风险边界

- **License**：GitHub API/license endpoint 与仓库 LICENSE 均为 Apache-2.0；依赖、模型权重、Hugging Face artifact、数据集、Electron/native binaries 与 release bundles 仍需单独审查。
- **维护活跃度**：固定 commit 为 2026-09-04，latest release 距查询约 3 天；14 个开放 non-PR issues，说明快速开发且仍在收边界。快速更新不等于稳定兼容。
- **安全风险**：#66 的无鉴权 wildcard-CORS kill-all route 在固定源码成立；`bun audit` 25 条已知 advisory。无 `SECURITY.md`，公开 advisory 空不能抵消源码与本机 audit。
- **正确性风险**：本机只跑 27 个核心 tests；未跑完整 408 test paths、Rust workspace、Electron/web、release installer、真实 daemon crash/upgrade、GPU/MLX/CUDA 或模型推理。#62 推理长请求故障待核验。
- **构建风险**：`packages/utils` typecheck fail；sdk/providers 依赖 generated version 前置步骤。不能把局部绿色测试投影成 monorepo 可发布。
- **隐私/资源风险**：README 的“offline/private”适用于本地路径目标，但 repo 仍包含 cloud endpoint、web search、usage 与模型下载能力；实际配置、网络调用、telemetry 和模型来源必须逐项核验。
- **不适用**：当前 Hermes 的服务端模型统一由既有 gateway 路由到 `ox-alpha`；本任务不得自行把 Magnitude 设为 provider、下载模型或切换当前模型。OpenClaw 不存在，也不创建其兼容配置。

#### ⭐ Skill 升格判断

**需二次验证，暂不升格 Magnitude 专属 skill。** 可迁移的是 `exact-owner convergence + at-most-once outcome_unknown + evidence-separated model admission`，与现有 `autonomous-learning/orchestrator-protocol`、verification-first、four-state terminal/effect-scope 候选高度重叠；先完成 synthetic fixture，再以增量条款更新既有 contract。上游 Apache-2.0 允许依法复用，但本日不复制其 Effect/Bun/Rust runtime。

#### ⭐ Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/exact-owner-outcome-unknown-v0/`。
- 候选 schema：`owner_identity.json`、`operation_receipt.json`，字段含 `scope/run/operation/target/revision/effect/terminal/evidence_hash`；只在 POC 使用，不直接写 curated。
- 验证后优先更新 `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：补 exact occurrence identity、outcome unknown、authority readback；不新增 Magnitude 专属共享 skill。
- Hermes adapter 只能在用户明确配置时接入 OpenAI-compatible endpoint，且遵守 stream=true；本任务不修改 `~/.hermes/config.yaml`。
- future agent 只消费 agent-neutral receipt/convergence contract；不得把某台宿主绝对路径、PID、端口或 Magnitude data root 写入 canonical shared 文档。

---

### 2. DietrichGebert/ponytail

- **一句话判断**：值得学的是它把一条行为准则做成 canonical skill + 多 host 薄 adapter + drift/behavior tests，而不是散落复制；更值得警惕的是其 shared mode flag、hook stdout dialect 与 benchmark prerequisite 证明“有 adapter 和绿色 CI”仍不等于 session/host 语义正确。
- **解决的问题**：替代 Agent 无条件加依赖、造抽象和自定义组件的习惯，也替代为每个 host 手工维护一份不同 prompt 的做法；其 ladder 先判断“不做/复用/stdlib/native/installed dependency”，最后才写最小代码，并明确不能削掉安全、validation、data-loss handling、accessibility 和用户要求。
- **URL / API 快照**：https://github.com/DietrichGebert/ponytail ；**Stars: 125,905 / Forks: 6,762 / Language: JavaScript / License: MIT**；`created_at=2026-06-12T00:52:37Z`，`updated_at=2026-09-04T23:37:10Z`，`pushed_at=2026-09-04T12:35:29Z`，repository API `open_issues_count=210`，default branch `main`。
- **固定提交**：[`974d940a1c5344210874150b98ff0d2c861fab6a`](https://github.com/DietrichGebert/ponytail/commit/974d940a1c5344210874150b98ff0d2c861fab6a)，commit API 时间 `2026-09-04T12:35:29Z`。
- **Release / issue 证据**：latest release `v4.9.0` 发布于 `2026-08-07T21:15:11Z`；main 已继续变化近一个月，不能把固定 main test 等同 release package。开放 issue [#809](https://github.com/DietrichGebert/ponytail/issues/809) 指出 Claude 多 session 共用 `~/.claude/.ponytail-active`；固定源码的 `statePath` 确实不含 `session_id`，静态一致。[#798](https://github.com/DietrichGebert/ponytail/issues/798) 指出未知兼容 host 将 raw stdout 当 JSON 时丢 context；[#790](https://github.com/DietrichGebert/ponytail/issues/790) 指出 Windows EOF fallback 的 unref timer 仍可能等外部 timeout；本机 Linux 定向测试未复现 Windows 情况，**待核验**。[#804](https://github.com/DietrichGebert/ponytail/issues/804) 报告网站写 medians、repo report 写 means；网站源码不在该 repo，本日只确认 repo report 明确使用 means。
- **来源交叉核验**：README、agent portability docs、agentic benchmark report、release/issues、canonical skill/adapters/hooks/tests、本机完整 suites 与临时供应链 audit。

#### 架构/实现与数据流

1. `skills/*/SKILL.md` 是 rich behavior source；`AGENTS.md` 是 compact instruction fallback；Cursor/Windsurf/Cline/Qoder/Copilot/Kiro 等复制体由 `check-rule-copies.js` 与 AGENTS canonical body 做 byte-equivalent 检查。
2. 支持完整插件的 host 使用薄 adapter：Hermes 根 `plugin.yaml + __init__.py` 注册 skills、`pre_llm_call`、gateway rewrite 与 slash commands；Claude/Codex/Copilot/Qoder 共用 Node hooks；Pi/OpenCode/MCP 各自适配 host API。
3. instruction builder 去 frontmatter，按 lite/full/ultra 只保留当前 intensity row/example；skill 文件缺失时退到 built-in fallback，防止 host 完全无规则。
4. lifecycle hook 在 session start 设置 mode 并注入；prompt hook解析 `/ponytail` 切换；subagent hook为子 Agent 再注入，并可按 regex scope。
5. Hermes adapter 不使用 Node shared flag，而是 Python 模块内 `_current_mode` + XDG config default；gateway command 先调用 Hermes slash access checker，授权后才 rewrite 成 skill prompt。
6. benchmark 分为 agentic feature tasks 与 deterministic safety tasks，以 git diff added LOC、tokens/cost/time 和 adversarial execution scoring；报告主动披露旧 baseline contamination bug、均值、n=4、单模型等限制。
7. distribution 通过 manifest/version/skill inventory/adapters tests 和 generated OpenClaw skill equality 防 drift；但 issue #809 表明“文件一致性”不能替代 state-scope conformance。

```text
canonical behavior
  skills/ponytail/SKILL.md
      +-> Hermes adapter (__init__.py + plugin.yaml)
      +-> shared Node hooks -> Claude/Codex/Copilot/Qoder
      +-> Pi / OpenCode / MCP adapters
      +-> generated/copied host rule views
  AGENTS.md compact body
      +-> byte-aligned instruction-only copies
  tests + benchmark
      +-> manifest/drift/behavior/correctness/safety checks
```

#### repo tree 摘要

```text
ponytail/                               # 159 tracked paths
├── skills/                             # 6 canonical skill contracts
├── AGENTS.md                           # compact cross-agent fallback
├── plugin.yaml + __init__.py           # Hermes native plugin adapter
├── hooks/                              # 11 shared lifecycle/config/instruction files
├── commands/                           # slash command definitions
├── .opencode/ .openclaw/ .qoder/ ...   # generated/copied host views/adapters
├── pi-extension/                       # Pi host adapter + tests
├── ponytail-mcp/                       # MCP prompt/tool adapter + 2 deps
├── scripts/                            # drift/version/generation/uninstall helpers
├── tests/                              # 15 root test files
├── benchmarks/                         # 35 files，agentic/correctness/safety evidence
├── docs/agent-portability.md           # canonical-to-adapter mapping
├── package.json                        # root package 无 runtime dependency
└── LICENSE                             # MIT
```

> `git ls-files` 实查 159 paths：35 benchmark、15 root tests、12 examples、11 hooks、6 skills、约 27 个常见 host adapter/view paths。小仓库的主要复杂度不是业务代码，而是跨 host 分发与一致性矩阵。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `skills/ponytail/SKILL.md` | rich canonical behavior | ladder、intensity、安全 carve-outs、one runnable check、debt comment |
| `AGENTS.md` | compact canonical fallback | instruction-only hosts 的统一正文 |
| `scripts/check-rule-copies.js` | deterministic drift gate | 7 个 copy 对 AGENTS body 比较；9 条 invariant 同时存在于 SKILL/AGENTS |
| `hooks/ponytail-instructions.js` | mode-aware projection | 去 frontmatter、filter mode row/example、fallback instructions |
| `hooks/ponytail-runtime.js` | Node host dialect/state | host detection、state path、raw/JSON output shape；#809 scope 缺口所在 |
| `hooks/ponytail-mode-tracker.js` | prompt command state | mode/default/off 解析、Qoder fallback、stdin 1 秒退出机制 |
| `hooks/ponytail-subagent.js` | subagent context | matcher scope、unknown fail-open injection、不同 host 输出 |
| `__init__.py` | Hermes native adapter | 注册 skills/hooks/commands、access-controlled gateway rewrite、process-local mode |
| `benchmarks/results/2026-06-18-agentic.md` | effect evidence | 同 agent baseline、git diff LOC、adversarial safety、污染复盘与限制 |

#### ⭐ 源码精读

**代码块 1：`filterSkillBodyForMode()` 从 canonical skill 投影当前 mode，而不是维护三份 prompt。**

```js
function filterSkillBodyForMode(body, mode) {
  const effectiveMode = normalizeMode(mode) || DEFAULT_MODE;
  const withoutFrontmatter = String(body || '').replace(/^---[\s\S]*?---\s*/, '');
  return withoutFrontmatter.split(/\r?\n/).filter((line) => {
    const tableLabel = line.match(/^\|\s*\*\*(.+?)\*\*\s*\|/);
    if (tableLabel) {
      const labelMode = normalizeMode(tableLabel[1].trim());
      if (labelMode) return labelMode === effectiveMode;
    }
    const exampleLabel = line.match(/^-\s*([^:]+):\s*"/);
    if (exampleLabel) {
      const labelMode = normalizeMode(exampleLabel[1].trim());
      if (labelMode) return labelMode === effectiveMode;
    }
    return true;
  }).join('\n');
}
```

逻辑摘要：mode-specific 数据通过结构化行识别，普通以 “Full:” 开头的规则不会被误删；测试专门覆盖这个回归。边界是这是启发式文本投影，不是完整 Markdown AST，规则格式变化仍可能漏筛或误筛，需 invariant/behavior tests 托底。

**代码块 2：`check-rule-copies.js` 把 copy drift 和 load-bearing invariants 分开检查。**

```js
for (const [relPath, normalize] of copies) {
  const actual = normalize(read(relPath));
  if (actual !== canonical) {
    console.error(`${relPath} drifted from AGENTS.md`);
    failed = true;
  }
}
const INVARIANTS = [
  'in this codebase', 'naive heuristic', 'ONE runnable check',
  'input validation at trust boundaries', 'prevents data loss',
  'security', 'accessibility',
];
for (const phrase of INVARIANTS)
  for (const [label, text] of sources)
    if (!text.includes(phrase)) failed = true;
```

逻辑摘要：compact copies 可 byte compare；rich SKILL 与 compact AGENTS 不能全文相等，所以只 pin 关键 safety/verification phrases。边界是 phrase canary 只能证明字符串存在，不能证明 host 实际加载、语义位置正确或模型遵循；因此还需要 adapter registration 和 first-turn behavior tests。

**代码块 3：Hermes `register()` 复用 canonical skills，并将 gateway access gate 放在 rewrite 前。**

```python
def rewrite_gateway_command(event=None, gateway=None, **_):
    text = str(getattr(event, "text", "") or "").strip()
    head, _, rest = text[1:].partition(" ")
    command = head.replace("_", "-").lower()
    if command not in SKILL_COMMANDS:
        return None
    if _slash_access_denied(event, gateway, command):
        return None
    return {"action": "rewrite", "text": _skill_prompt(command, rest)}

def register(ctx):
    for child in sorted(SKILLS_DIR.iterdir()):
        if (child / "SKILL.md").exists():
            ctx.register_skill(child.name, child / "SKILL.md")
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    ctx.register_hook("pre_gateway_dispatch", rewrite_gateway_command)
```

逻辑摘要：插件不复制每个 skill 内容到 Python；Hermes loader 注册真实 `SKILL.md`，hook 负责上下文，slash command 先检查 access。边界是本机 test 使用 fake context/gateway；本日没有安装或重启当前 Hermes，也没有做真实多用户 gateway E2E。

**代码块 4：Node `statePath` 未包含 session identity，静态解释 #809。**

```js
let stateDir = getClaudeDir();
if (isCodex) stateDir = process.env.PLUGIN_DATA;
if (isCopilot) stateDir = process.env.COPILOT_PLUGIN_DATA || getClaudeDir();
if (isQoder) stateDir = path.join(os.homedir(), '.qoder');
const statePath = path.join(stateDir, '.ponytail-active');

function setMode(mode) {
  fs.mkdirSync(path.dirname(statePath), { recursive: true });
  fs.writeFileSync(statePath, mode);
}
function readMode() {
  try { return fs.readFileSync(statePath, 'utf8').trim() || null; }
  catch { return null; }
}
```

逻辑摘要：Codex/Copilot 可能由宿主提供 per-plugin data scope；native Claude 默认是 config-dir singleton，未消费 hook payload 的 `session_id`。因此一个 pane 的 review/off 可影响另一 pane subagent。边界是 Hermes Python adapter使用 process-local `_current_mode`，不应把 Claude 的该缺陷直接外推为 Hermes 已受影响；但多会话/多 worker 的 scope acceptance test 仍值得补。

**代码块 5：`ponytail-subagent.js` 对未知 matcher 输入选择 fail-open 注入。**

```js
function finish() {
  let agentType = '';
  try {
    agentType = String(JSON.parse(input.replace(/^\uFEFF/, '')).agent_type || '').trim();
  } catch {}
  if (agentType && !matcherRe.test(agentType)) process.exit(0);
  inject();
}
process.stdin.on('end', finish);
process.stdin.on('error', () => { finish(); process.exit(0); });
setTimeout(() => { finish(); process.exit(0); }, 1000).unref();
```

逻辑摘要：明确 mismatch 才跳过；缺字段、坏 JSON、坏 regex 都注入，以免 persona 在 subagent 中静默丢失。边界是对低权限/只读 agent 而言，fail-open 会增加上下文税或行为干扰；若规则本身带 effect 权限，策略必须反过来 fail-closed。#790 还指出 Windows 某种 stdin handle 下 unref fallback 可能不按预期触发，本机 Linux test 只能证明普通条件约 1 秒退出。

#### 依赖分析与供应链风险

- 根 `package.json` 没有 dependencies/devDependencies；主要 runtime 是 Node built-ins + Python stdlib Hermes adapter，供应链面相对小。
- `ponytail-mcp/package.json` 依赖 `@modelcontextprotocol/sdk ^1.26.0` 与 `zod ^3.23.0`；仓库没有提交 lockfile。本机临时生成 lock 后解析 95 packages，production audit 为 0 known vulnerabilities；删除临时 lock 后仓库保持 clean。
- 没有 lockfile 意味着相同 `v4.9.0` 源码在未来可能解析到不同 MCP/Zod transitive graph；CI green 不能证明未来安装可复现。
- 真实安装仍涉及 Agent plugin marketplace、hooks、全局 config、skill copies、MCP 或 host runtime。MIT 许可与 0 advisory 不会验证这些 authority surfaces。
- 根 `npm test` 隐式依赖系统 Python + pandas 才能让 CSV fixture 通过，而 pandas 不在 package manifest；本机首次 83/84 失败，安装隔离 venv 后 84/84。这是 prerequisite discovery 缺口，不是项目代码回归，但意味着 fresh environment 的 test contract 不自足。

#### 可复用经验

- 当一个 skill 要跨多个 Agent/harness 分发时，应优先保留一个 rich canonical contract、一个 compact fallback，并让 host adapter 只处理 loader/hook/command dialect；因为复制业务规则会漂移，边界是 thin adapter 仍要做真实 first-turn/subagent/command conformance。
- 当 canonical 与 projections 不能全文相等时，应优先组合“可 byte-compare 的 copy drift + load-bearing invariant canary + behavior test”，而不是只搜索关键词；因为字符串存在不证明 host 加载和行为，边界是 behavior test 也需覆盖真实 host version。
- 当 mode/state 被称为 session-scoped 时，应优先把 session identity 写入 state key 并做两个并发 session 的隔离 fixture；因为 config-dir singleton 会产生跨 pane 污染，边界是 process-local state 也可能在共享 gateway worker 内跨用户复用。
- 当 benchmark 依赖外部 runtime/package 时，应优先在入口 preflight、声明版本并将 missing prerequisite 标为 blocked；因为“唯一测试失败”可能是工具没装而不是产品回归，边界是补装后绿色仍不证明 benchmark 外部有效性。
- 当规则以“尽量少写”为目标时，应优先把 trust-boundary validation、安全、data-loss handling、accessibility 与一个 runnable check 写成不可删 carve-out；因为单纯 YAGNI/one-liner 会把 guard 一起削掉，边界是当前 100% safety 只来自单模型、小样本 fixture。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/canonical-adapter-session-scope-v0/` 做纯 fixture：

1. 定义一个 canonical markdown contract 和两个 adapter projection；故意制造 copy drift，checker 必须 fail；
2. 用两个 `session_id` 并发切换 full/review/off，证明 state 不串线；
3. 模拟 raw stdout / JSON hook dialect mismatch，必须返回 `blocked(adapter_incompatible)` 而非静默成功；
4. 删除 prerequisite（如 pandas），benchmark preflight 应返回 blocked；补齐后再执行 behavior checks；
5. 不安装 Ponytail、不改 `~/.hermes/`、不复制其 skill 到 shared、不调用 OpenClaw。

#### 风险边界

- **License**：GitHub API/license endpoint 与根 package 均为 MIT；benchmark 的目标 repo、模型服务、host plugins、外部 assets 与 transitive dependencies 仍需分别核验。
- **维护活跃度**：main 最后提交 2026-09-04，33 个开放 non-PR issues；latest release v4.9.0 为 2026-08-07，main 与 release 已明显分叉。热度和 commit 频率高，也意味着 adapter compatibility 快速变化。
- **安全风险**：插件能在每轮注入上下文、改全局/host state、注册 gateway command；这些是 authority surfaces。Hermes adapter有 slash access check，但真实共享 gateway E2E 未跑。无 `SECURITY.md`。
- **状态隔离风险**：#809 与固定源码证明 native Claude state path 不含 session key；跨 pane 污染是明确设计缺口。Hermes 当前实现 process-local，不等于跨用户安全，需结合 Hermes worker 生命周期核验。
- **兼容风险**：#798 指向 hook stdout dialect；#790 指向 Windows stdin/timer；本机 WSL/Linux tests 不能覆盖 ZCode/Windows/各 host 新版本。
- **benchmark 局限**：报告使用 Haiku 4.5、n=4、12 feature + 6 safety tasks；作者已披露旧 baseline contamination。网站 mean/median 文案冲突仍 open。本机没有重跑真实 Claude agentic benchmark，只跑 deterministic tests，因此 54%/20%/27% 等效果数据均属于上游实验结果，**本机待核验**。
- **供应链局限**：MCP 无提交 lock，临时 audit 0 findings 只覆盖当前解析；fresh root tests 又隐式需要 pandas。
- **不适用**：不应全局安装或默认启用第三方 persona 来替代当前 AGENTS/skills 治理；它会增加每轮上下文并可能与用户要求冲突。OpenClaw 当前不存在，本日不操作其路径。

#### ⭐ Skill 升格判断

**暂不沉淀 Ponytail skill；机制需二次验证。** “YAGNI + reuse/native-first + safety carve-outs”适合作为代码评审原则，但 shared hub 已有 path/config/orchestrator/research 等 class-level skills，不能因热门就复制一整套 persona/commands。真正值得反哺的是 `canonical contract → thin adapter → drift + behavior matrix → session-scope isolation`，应先更新现有 shared-skill governance 或 GitHub-learning verification 条款；上游 MIT 允许复用，但本日不复制源码或 skill 文本。

#### ⭐ Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/canonical-adapter-session-scope-v0/`。
- shared skill governance 候选：在现有 `docs/shared-skill-governance.md` 或 `research/github-hot-project-learning` 中增加 `canonical source / generated view / adapter / drift test / first-turn behavior / state scope` 检查矩阵；先出审核稿，不直接改。
- Hermes 本地如未来试用，必须用户明确同意后操作 `~/.hermes/plugins/`，先审 `plugin.yaml`、`__init__.py`、access control 与 token/context overhead；本任务未安装。
- shared hub 不保存 `.ponytail-active`、PID、host config 或其他 runtime state；跨 agent canonical 只保留中性 contract，宿主 adapter 保留本地。
- future agent 接入时只编写薄 adapter 并跑 canonical/adapter conformance；不把 OpenClaw、Claude 或 Hermes 路径写死在共享真相层。

## 经验沉淀

1. **当多个 client、进程或 Agent 要竞争同一服务/任务 authority 时，应优先绑定精确 occurrence identity、最小 durable owner fact、CAS replacement 与 lifetime monitor；因为 PID、端口、文件存在或 HTTP 200 都可能陈旧，边界是 OS/store 证据本身仍需验证。**
2. **当副作用请求可能已经 dispatch 但 ACK 丢失时，应优先返回 `needs_verification/outcome_unknown` 并读取权威状态，而不是自动重试；因为连接恢复不等于 effect 未发生，边界是 readback 必须关联同一 operation/target/revision。**
3. **当一个 skill/规则跨多个 host 分发时，应优先使用 canonical contract + 薄 adapter + deterministic drift gate + first-turn/subagent behavior matrix；因为文件一致不等于宿主加载和会话语义正确，边界是每个 host version 都可能改变 hook dialect。**
4. **当状态宣称 session-scoped、run-scoped 或 tenant-scoped 时，应优先把该 immutable scope 写入 key 并做并发隔离 fixture；因为 machine-global flag/process singleton 会产生跨 pane/用户污染，边界是清理与 TTL 也必须 scope-aware。**
5. **当 recommendation/cache 将触发下载、加载或调度时，应优先分开 authored metadata、measured assessment 与 effect-time admission；因为缓存建议不是当前资源事实，边界是 measurement 必须绑定 artifact/hardware revision。**
6. **当本地 loopback 服务提供高权 mutation 时，应优先把 loopback 仅视为网络范围，再补 host-owned authorization、origin/CSRF 防护和 destructive-route tests；因为浏览器与本机低权进程仍可触达，边界是 token 本身也需保护。**
7. **当测试/benchmark 依赖未声明的系统工具或 Python 包时，应优先 preflight 并返回 blocked，而不是把缺依赖当产品失败或悄悄跳过；因为测试是否执行与测试是否通过是两类事实，边界是补齐 prerequisite 后仍需披露环境版本。**
8. **当供应链扫描命中 advisory 时，应优先报告 lockfile 命中与 reachability 分开，不把 audit 非零直接写成已利用漏洞，也不把 audit clean 写成安全；因为依赖存在、调用可达、可利用和已修复是不同层，边界是未知漏洞永远不在 advisory 数据库里。**

### 跨项目机制对比

| 问题 | Magnitude | Ponytail | shared hub 可取部分 |
|---|---|---|---|
| canonical authority | SQLite exact owner + live health/process evidence | SKILL/AGENTS canonical behavior | curated truth / canonical skill / runtime 分层 |
| derived/projection | query cache、catalog/model projection | host rule copies、mode-filtered prompt | projection 必须可重建、有 source/version |
| adapter | SDK/ACN/ICN/provider boundaries | Hermes/Node/Pi/OpenCode/MCP host adapters | agent-neutral contract + thin host adapters |
| uncertain result | typed `RpcOutcomeUnknown` | 当前多数 hook silent fail，部分兼容问题会静默丢 context | unknown/blocked 必须显式 terminal，禁止假成功 |
| 已知反例 | dashboard kill-all、audit 25、utils typecheck fail | machine-global flag、hook dialect、隐式 pandas prerequisite | audit 必须覆盖 authority/state scope/prerequisite，不只关键词 |

## 明日继续

1. 创建 `runtime/hermes/github-learning-poc/exact-owner-outcome-unknown-v0/`，用 synthetic process/transport fixtures 验证 stale identity、CAS replacement 与 at-most-once reconciliation。
2. 创建 `runtime/hermes/github-learning-poc/canonical-adapter-session-scope-v0/`，验证 copy drift、两个 session 隔离、hook dialect mismatch 与 prerequisite-blocked。
3. 观察 Magnitude #66/#74 是否合并修复，并固定新 commit 重跑 route source、utils typecheck 与定向 tests；不启动 destructive endpoint。
4. 观察 Ponytail #809/#798/#790/#804；只有 session-keyed state 与 cross-host acceptance fixtures落地后，才考虑吸收 adapter-state 条款。
5. 若 POC 通过，先在聊天中给 `orchestrator-protocol` / `github-hot-project-learning` / shared-skill governance 的增量审核稿；不自动修改 shared skill 或 curated。

## 候选反哺

### Candidate Facts

- [ ] topic: exact occurrence identity + owner CAS is safer than PID/endpoint-only daemon coordination | evidence: Magnitude cross-version protocol、convergence source、本机 27 tests | 建议: update existing orchestration/verification fact after POC/de-dup | 安全级别: medium
- [ ] topic: at-most-once transport ambiguity must terminalize as needs_verification and authoritative readback | evidence: `recovering-protocol.ts`、`mutation-outcome.ts`、对应 tests | 建议: update existing effect-scope/terminal fact after fixture | 安全级别: high
- [ ] topic: cross-agent skill distribution requires canonical source, thin adapters, drift tests, behavior tests and scope isolation | evidence: Ponytail portability docs/checker/Hermes adapter + issue #809 | 建议: update shared-skill governance after two-host fixture | 安全级别: medium
- [ ] topic: dependency/test prerequisite absence must be represented separately from product failure | evidence: Ponytail first run 83/84 due missing pandas, venv rerun 84/84 + 23/23 + 3/3 | 建议: update GitHub-learning verification workflow | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: `exact-owner-outcome-unknown` | 可复用场景: daemon、cron worker、Agent job replacement、不可重复副作用 | 是否建议 shared: no（当前） | 原因: 与 orchestrator/verification/effect-scope 重叠，先做 fixture 后增量更新
- [ ] 名称: `canonical-adapter-conformance` | 可复用场景: shared skill 跨 Hermes/future-agent/CLI/hook 分发 | 是否建议 shared: no（当前） | 原因: 先验证 state scope、first-turn/subagent 与 dialect matrix，再更新治理标准
- [ ] 名称: `prerequisite-aware-test-receipt` | 可复用场景: cron 学习、benchmark、build/audit | 是否建议 shared: no（当前） | 原因: 应并入现有 GitHub-learning/verification contract，避免重复 skill

### Candidate Open Questions

- [ ] 问题: Magnitude #66 的修复是否同时覆盖 Origin、simple request、auth token、read routes 和 destructive route tests，而不是只改 CORS header？ | reason: security gap | priority: high
- [ ] 问题: Magnitude 的 25 个 lockfile advisories 哪些真实可达 release/install/web/desktop 路径，修复是否需要 breaking update？ | reason: supply-chain reachability | priority: high
- [ ] 问题: `RpcOutcomeUnknown` 的上层 mutation 是否均实现 operation-correlated authoritative reconciliation？ | reason: effect uncertainty | priority: high
- [ ] 问题: Ponytail native Claude mode 如何 session-keyed 且在 hook cleanup/abandoned session 时有界回收？ | reason: scope isolation | priority: high
- [ ] 问题: Ponytail 各 host 的 hook stdout/event capability 能否通过 versioned adapter capability matrix 自动发现，而不是 env heuristic？ | reason: adapter drift | priority: medium
- [ ] 问题: benchmark 网站的 median/mean 文案何时统一，真实多模型重跑是否仍支持 headline？ | reason: evidence conflict/stale | priority: medium

### 不应自动落地

- 不安装、启动或配置 Magnitude；不下载模型/权重，不启动 ACN/ICN/dashboard，不执行 kill-all，不修改当前 Hermes provider/model/gateway。
- 不安装或启用 Ponytail Hermes 插件，不修改 `~/.hermes/config.yaml`、plugins、skills、cron 或 auth；不调用不存在的 OpenClaw。
- 不复制 Ponytail skill/persona 或 Magnitude Effect/Bun/Rust 源码到 shared；只提出独立机制候选。
- 不把 Stars、issue 声明、上游 benchmark、audit 0 findings、局部 tests 或静态漏洞链直接写入 curated active fact。
- 不把 machine-specific PID、端口、absolute repo checkout、session flag 或 dependency cache 写入 curated/capabilities。
- 不自动修改 config、模型、provider、cron、secret；任何未来接入先声明目标系统与目标文件、dry-run、审计、再由用户明确批准。
