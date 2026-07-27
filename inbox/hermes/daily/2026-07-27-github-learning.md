# 2026-07-27 GitHub 热门项目学习日报

> 执行者：Hermes（OpenClaw 未运行、未调用）  
> 查询时间：2026-07-27T07:30–08:05+08:00  
> 发现入口：<https://github.com/trending?since=daily>；仓库元数据：`gh api repos/{owner}/{repo}`  
> 深读固定快照：`pingdotgg/t3code@a17cbc3b4022b824cda9b199e4c53a8c9a608923`、`CoreBunch/Instatic@d97cac231e759d5ca445617193e53243d970b629`。Stars 是查询快照，会继续变化。

## 今日结论

今日主线是：**Agent 系统不能把“异步工作完成”“插件获准联网”“外部 Agent 获准写入”留作模糊约定；应把它们收束为可等待的局部 completion barrier、最终副作用点的 authority 重验，以及每个网络跳转都重新执行的 fail-closed guard。** T3 Code 展示了 queue/active/pending 三态和 keyed drain；Instatic 展示了 QuickJS 隔离、`grantedPermissions` 中央检查、SSRF hop-by-hop 重验及连接能力不被浏览器 cookie 放大。

## 研究方法与可验证证据

1. 真实下载 GitHub Trending daily HTML，并对 17 个候选逐仓运行 GitHub REST API；速览表中的 Stars、Forks、Language、License、`updated_at`、`pushed_at` 均来自该响应。
2. 两个深读项目均 `git clone --depth=1 --filter=blob:none`，固定到上方 commit；读取 README、architecture/plugin/MCP docs、release、issues/PR、依赖清单、关键源码和测试。
3. Release / issue 交叉来源：
   - T3 Code 最新 API 返回 release 为预发布 `v0.0.29-nightly.20260725.899`（2026-07-25）；issue [#4596](https://github.com/pingdotgg/t3code/issues/4596) 暴露逐 delta replay 的超线性成本，[#4595](https://github.com/pingdotgg/t3code/issues/4595) 暴露把 base64 图像重复内联到事件/活动记录造成慢链路失败。
   - Instatic 最新 release `v0.0.13`（2026-07-24）；PR [#275](https://github.com/CoreBunch/Instatic/pull/275) 修复 URL scheme 解析绕过并说明随 0.0.14 交付，PR [#281](https://github.com/CoreBunch/Instatic/pull/281) 补齐 MCP browser tool 的 open-workspace precondition；issue [#284](https://github.com/CoreBunch/Instatic/issues/284) 报告 Windows 上 247/6283 tests fail，主因 DB handle 未关闭。
4. 动态验证：
   - T3 Code：本机 Node 22.14.0 不满足根 `package.json` 的 Node ^24.13.1，且无 pnpm；未伪称完整测试通过。使用 Node experimental type stripping 直接执行 `threadSettled.ts` 纯函数 fixture，真实结果 **3 assertions passed**。
   - Instatic：临时下载 Bun 1.3.14（满足 `>=1.3.0 <1.4.0`），执行 frozen lock 安装，再运行 4 个 focused test files，真实结果 **26 passed / 0 failed / 103 expect calls**，覆盖 MCP 行级授权、registry 能力过滤、SSRF redirect/DNS rebinding 和 sandbox architecture gates。
5. 全部原始 API/HTML/clone/issue/release 证据位于 `runtime/hermes/github-hot-project-learning/evidence/2026-07-27/`；它们是 runtime 产物，不晋升 curated。

## 项目速览

> 下表数据来自 2026-07-27 查询时的 GitHub API；`License（API）` 只表示仓库级 SPDX 识别，不是 transitive dependency license 审计；`updated_at` 不是最后提交时间。

| 项目 | Stars | Forks | Language | License（API） | API updated_at | API pushed_at | 今日判断 |
|---|---:|---:|---|---|---|---|---|
| [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | **15,033** | 3,309 | TypeScript | MIT | 2026-07-26T23:30:12Z | 2026-07-26T23:13:05Z | **深读**：可 drain 队列、按 key 合并、typed event/read model |
| [CoreBunch/Instatic](https://github.com/CoreBunch/Instatic) | **5,636** | 520 | TypeScript | MIT | 2026-07-26T23:30:28Z | 2026-07-25T18:47:54Z | **深读**：插件 sandbox、capability kernel、SSRF/MCP 授权 |
| [permissionlesstech/bitchat](https://github.com/permissionlesstech/bitchat) | 30,228 | 4,700 | Swift | Unlicense | 2026-07-26T23:28:06Z | 2026-07-26T22:45:21Z | 高热 P2P 通讯；协议/密码学面大，暂只观察 |
| [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | 4,441 | 220 | JavaScript | MIT | 2026-07-26T23:29:03Z | 2026-07-26T11:41:18Z | 昨日已深读；继续观察 ownership/handoff |
| [block/buzz](https://github.com/block/buzz) | 13,204 | 1,083 | Rust | Apache-2.0 | 2026-07-26T23:30:43Z | 2026-07-26T23:18:00Z | 近期已深读；继续观察 scoped evidence |
| [yorukot/superfile](https://github.com/yorukot/superfile) | 20,197 | 639 | Go | MIT | 2026-07-26T23:29:12Z | 2026-07-26T00:37:14Z | TUI 文件管理，候选但与今日主线较弱 |
| [nodejs/node](https://github.com/nodejs/node) | 118,455 | 36,175 | JavaScript | NOASSERTION | 2026-07-26T23:28:07Z | 2026-07-26T18:10:12Z | API 无可判定 license，且仓库过大；不仓促深读 |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 50,626 | 2,984 | JavaScript | Apache-2.0 | 2026-07-26T23:31:17Z | 2026-07-26T17:17:21Z | UI 设计 Agent 能力；后续单独审 prompt/skill injection 面 |
| [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | 34,154 | 5,752 | Python | MIT | 2026-07-26T23:27:45Z | 2026-04-13T12:38:49Z | 热度高但 pushed 时间较旧；模型结论需独立复现 |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 50,210 | 5,918 | Jupyter Notebook | MIT | 2026-07-26T23:29:16Z | 2026-07-23T17:32:41Z | 示例价值高，但今日优先实现型仓库 |

---

## 深读项目

### 项目 1. pingdotgg/t3code

- **仓库**：<https://github.com/pingdotgg/t3code>
- **API 基本信息**：Stars: **15,033**；Forks: **3,309**；License: **MIT**；Language: TypeScript；`updated_at`: 2026-07-26T23:30:12Z；`pushed_at`: 2026-07-26T23:13:05Z；open issues/PR count: 827。
- **License 文件**：根 `LICENSE` 是 MIT，copyright 2026 T3 Tools Inc.
- **固定快照**：[`a17cbc3`](https://github.com/pingdotgg/t3code/commit/a17cbc3b4022b824cda9b199e4c53a8c9a608923)，commit time 2026-07-26T22:26:59Z。
- **Release / Issues**：[`v0.0.29-nightly.20260725.899`](https://github.com/pingdotgg/t3code/releases/tag/v0.0.29-nightly.20260725.899) 是 prerelease；[#4596](https://github.com/pingdotgg/t3code/issues/4596) 报告 streaming delta backlog 逐事件 replay 导致超线性 UI 工作；[#4595](https://github.com/pingdotgg/t3code/issues/4595) 报告 base64 图像在活动/事件中重复内联造成慢链路无法打开 thread。
- **一句话判断**：值得学的不是又一个 coding UI，而是如何把 provider-native stream 变成 **typed command/event/read model + ordered worker + explicit drain/receipt + snapshot fallback**，从而让测试和用户态都能区分“请求返回”与“异步副作用真正静止”。
- **解决的问题**：替代“WebSocket 直接透传 provider JSON、多个 reactor 靠 sleep/poll 猜完成、同 key 高频更新全部排队、历史大对象全塞首帧”的旧做法。

#### 架构/实现与数据流

```text
pingdotgg/t3code/
├── apps/server/
│   ├── src/server.ts                              # runtime layer graph / WebSocket+HTTP 入口
│   ├── src/provider/                              # Codex/Claude/OpenCode 等 provider session
│   ├── src/orchestration/Layers/                  # engine、ingestion、command/checkpoint reactors
│   ├── src/persistence/                           # event store、projection/read model、receipts
│   └── src/terminal/Manager.ts                    # terminal I/O 与 keyed history persistence
├── apps/web/                                      # React/Vite 客户端
├── packages/contracts/src/orchestration.ts        # wire schema、command/event/read model SSOT
├── packages/shared/src/
│   ├── DrainableWorker.ts                         # 全局有序队列 + 可等待 quiescence
│   └── KeyedCoalescingWorker.ts                   # 每 key 最新值合并 + drainKey
├── packages/client-runtime/src/state/
│   ├── threadSnapshotHttp.ts                      # 大 snapshot 走 gzip-able HTTP，socket fallback
│   └── threadSettled.ts                           # pending/queued/live 的 settle/snooze 不变量
└── docs/architecture/overview.md                  # 生命周期与 completion receipt 说明
```

数据流：`Browser typed request -> wsServer schema decode -> ProviderService -> provider JSON-RPC/ACP -> ProviderRuntimeIngestion normalization -> OrchestrationEngine append/projection -> queue-backed reactors -> RuntimeReceiptBus milestone -> ServerPushBus ordered push -> client read model`。thread 首开时优先 `HTTP snapshot (6s bound)`，失败后回退 WebSocket subscription；这是 payload transport 优化，不改变 socket 对 thread existence 的权威性。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `docs/architecture/overview.md` | 官方数据流 | provider event 规范化、queue-backed worker、typed receipt、ordered push |
| `packages/shared/src/DrainableWorker.ts` | completion barrier | `outstanding` 与 enqueue 同一事务更新；process 成败都在 `ensuring` 减计数；`drain` 用 transactional retry |
| `packages/shared/src/KeyedCoalescingWorker.ts` | 热 key 背压 | `latestByKey / queuedKeys / activeKeys`；active 时只合并 latest；失败后重排 pending |
| `packages/client-runtime/src/state/threadSnapshotHttp.ts` | 大状态传输 | 6s timeout；HTTP 可 gzip；404/网络失败回退 socket snapshot |
| `packages/client-runtime/src/state/threadSettled.ts` | UI/状态不变量 | approval/input/running/queued turn 均阻止 settle；clock skew 与 grace window 明确处理 |
| `packages/contracts/src/orchestration.ts` | schema/compat | typed WS methods；legacy model selection 只在 decode transform 吸收；输入/附件上限 |

#### 源码精读 1：drain 等的是“队列空且当前 item 完成”

固定源码：[`DrainableWorker.ts#L40-L69`](https://github.com/pingdotgg/t3code/blob/a17cbc3b4022b824cda9b199e4c53a8c9a608923/packages/shared/src/DrainableWorker.ts#L40-L69)

```ts
export const makeDrainableWorker = <A, E, R>(process: (item: A) => Effect.Effect<void, E, R>) =>
  Effect.gen(function* () {
    const queue = yield* Effect.acquireRelease(TxQueue.unbounded<A>(), TxQueue.shutdown);
    const outstanding = yield* TxRef.make(0);
    yield* TxQueue.take(queue).pipe(
      Effect.tap((a) => Effect.ensuring(process(a), TxRef.update(outstanding, (n) => n - 1))),
      Effect.forever,
      Effect.forkScoped,
    );
    const drain = TxRef.get(outstanding).pipe(
      Effect.tap((n) => (n > 0 ? Effect.txRetry : Effect.void)), Effect.tx,
    );
    const enqueue = (element: A) => TxQueue.offer(queue, element).pipe(
      Effect.tap(() => TxRef.update(outstanding, (n) => n + 1)), Effect.tx,
    );
    return { enqueue, drain };
  });
```

逻辑摘要：不是读取 queue size 再 sleep，而是 `offer + outstanding++` 原子发生；当前 item 的 processing 也包含在 outstanding 中，并用 `ensuring` 保证失败/中断路径减计数。测试中 first active 时启动 drain、再 enqueue second，drain 必须等 second 完成。这是可验证 quiescence；边界是 unbounded queue 没有容量背压，错误语义也由外围 `process...Safely` 决定。

#### 源码精读 2：同 key 高频写只排一个 key，并保留 active 期间 latest

固定源码：[`KeyedCoalescingWorker.ts#L26-L57`](https://github.com/pingdotgg/t3code/blob/a17cbc3b4022b824cda9b199e4c53a8c9a608923/packages/shared/src/KeyedCoalescingWorker.ts#L26-L57) 与 [`#L111-L139`](https://github.com/pingdotgg/t3code/blob/a17cbc3b4022b824cda9b199e4c53a8c9a608923/packages/shared/src/KeyedCoalescingWorker.ts#L111-L139)

```ts
const enqueue = (key: K, value: V) =>
  TxRef.modify(stateRef, (state) => {
    const latestByKey = new Map(state.latestByKey);
    const existing = latestByKey.get(key);
    latestByKey.set(key, existing === undefined ? value : options.merge(existing, value));
    if (state.queuedKeys.has(key) || state.activeKeys.has(key)) {
      return [false, { ...state, latestByKey }] as const;
    }
    const queuedKeys = new Set(state.queuedKeys);
    queuedKeys.add(key);
    return [true, { ...state, latestByKey, queuedKeys }] as const;
  }).pipe(
    Effect.flatMap((shouldOffer) => shouldOffer ? TxQueue.offer(queue, key) : Effect.void),
    Effect.tx,
  );
```

逻辑摘要：queue 里存 key，不存每个 update；active/queued 时新值合并到 `latestByKey`。当前 process 完成后递归取一次最新值；若 process 失败，`cleanupFailedKey` 会把仍 pending 的 key 重排。`drainKey` 同时检查 latest/queued/active，而不是看到 queue 中没有 key 就提前返回。迁移时必须先判断 workload 是否允许合并；审计 append、用户消息、money movement 不能 latest-wins。

#### 源码精读 3：大 snapshot 从 socket 首帧拆出，但保留有界 fallback

固定源码：[`threadSnapshotHttp.ts#L19-L59`](https://github.com/pingdotgg/t3code/blob/a17cbc3b4022b824cda9b199e4c53a8c9a608923/packages/client-runtime/src/state/threadSnapshotHttp.ts#L19-L59) 与 [`#L92-L117`](https://github.com/pingdotgg/t3code/blob/a17cbc3b4022b824cda9b199e4c53a8c9a608923/packages/client-runtime/src/state/threadSnapshotHttp.ts#L92-L117)

```ts
const DEFAULT_THREAD_SNAPSHOT_TIMEOUT_MS = 6_000;

export const fetchEnvironmentThreadSnapshot = Effect.fn("fetchEnvironmentThreadSnapshot")(
  function* ({ prepared, threadId, signer, timeoutMs }) {
    const requestUrl = environmentEndpointUrl(
      prepared.httpBaseUrl, `/api/orchestration/threads/${threadId}`,
    );
    const headers = yield* buildEnvironmentAuthHeaders(
      prepared.httpAuthorization, "GET", requestUrl, signer,
    );
    return yield* executeEnvironmentHttpRequest(
      requestUrl, timeoutMs ?? DEFAULT_THREAD_SNAPSHOT_TIMEOUT_MS,
      withEnvironmentCredentials(/* typed API request */),
    );
  },
);
```

```ts
load: (prepared, threadId) =>
  fetchEnvironmentThreadSnapshot({ prepared, threadId, signer }).pipe(
    Effect.map(Option.some),
    Effect.catchTags({
      EnvironmentResourceNotFoundError: () => Effect.as(
        Effect.logDebug("snapshot not found; defer to socket"), Option.none(),
      ),
    }),
    Effect.catchCause((cause) => Effect.as(
      Effect.logWarning("HTTP snapshot failed; use socket snapshot", cause), Option.none(),
    )),
  )
```

逻辑摘要：多 KB snapshot 走可压缩 HTTP，避免污染 WebSocket first frame；6 秒 deadline 保证慢 HTTP 不长期阻止 socket fallback；404 不直接判 thread 消失，因为 socket subscription 才是 existence truth。issue #4595/#4596 证明边界仍存在：如果 payload 本身重复内联 base64，或 replay 仍逐 delta 应用，换 transport 不会消除状态/复杂度债务。

#### 依赖分析与供应链风险

- 根工具链：Node `^24.13.1`、pnpm 11.10.0、vite-plus 0.2.2、TypeScript native preview；本机 Node 22.14.0 不满足根约束。
- `packages/shared`：Effect `4.0.0-beta.78`、jose 6.2.2、`@noble/{curves,hashes}` 1.9.1/1.8.0、yaml ^2.9.0；lock 中 Effect 带 patch hash，`prepare` 还执行 `effect-tsgo patch`。
- `apps/server`：Claude Agent SDK `^0.3.170`、OpenCode SDK `^1.3.15`、Effect platform/sql、native `node-pty`；provider/runtime/terminal 权限面明显大于纯 UI。
- 风险：beta Effect + patch 增加升级耦合；catalog/workspace monorepo 和 native pty 增加构建/发布矩阵；provider SDK 可访问 credentials、shell/worktree；夜版 prerelease 更新快。只抽象协议，不把其完整 runtime 或依赖图引入 Hermes。

#### 可复用经验、实验与落地路径

- **当**请求返回后仍有 checkpoint、projection、index 或通知等异步副作用**时，应优先**提供可等待的 completion receipt / drain barrier，而不是 `sleep` 或轮询；因为 queue empty 不等于 active item 完成，边界是 worker 必须对失败/取消做终态计数。
- **可尝试实验（30 分钟）**：在 `runtime/hermes/github-learning-poc/scoped-drain-contract/` 写 Python fixture worker，状态为 `{pending,active,latest_by_key,failed}`，验证：active 时 enqueue 不提前 drain、不同 date/run key 不互相阻塞、processor fail 后 pending 仍可见；不接入真实 cron/provider。
- **Skill 升格判断：需二次验证。** `scoped completion barrier + typed receipt` 能反哺 cron/reflection/audit，但不能照搬 Effect/TypeScript 实现；先验证 Python orchestrator 在 crash/cancel/rerun 下的语义，并与既有 verification-first/self-reflection skill 去重。
- **Hermes/shared hub 落地路径**：
  1. runtime POC：`runtime/hermes/github-learning-poc/scoped-drain-contract/`；
  2. portable 接口：`enqueue(scope_key, revision, payload)`、`drain(scope_key, through_revision)`、`receipt={status,scope,revision,evidence_refs}`；
  3. Hermes 候选接点：`scripts/github_learning_orchestrator.py` 的 prepare/report/audit 阶段仅记录 receipt，不改 cron/provider；
  4. raw queue/receipt/log 放 `runtime/hermes/`，日报放 `inbox/hermes/daily/`，不把 replay/event bulk 写 curated；
  5. fixture 与真实失败恢复通过后，优先更新 `autonomous-learning/self-reflection-engine` 或 verification 相关 shared skill，而不是新建重复 worker skill。

#### 风险边界

- **License**：API 与根 LICENSE 为 MIT；仍需审 provider SDK、Effect、node-pty 等 transitive license。
- **维护活跃度**：固定 commit 与查询相差不到一天，nightly 2026-07-25，活跃但变化极快；nightly 不是稳定发布承诺。
- **安全风险**：server 管 provider credentials、terminal、git/worktrees、remote connections；schema 与 approval mode 不能替代 OS sandbox、secret redaction 和最小权限。
- **局限/不适用**：unbounded worker 不适合无上限 producer；coalescing 只适合 supersedable state，不适合 append-only evidence；snapshot HTTP fallback 不解决重复 base64、逐 delta replay 或超线性 render。
- **动态验证局限**：未按仓库要求跑 vp focused test，因为本机 Node/pnpm 不满足；只运行了不依赖外包的 `threadSettled.ts` 3-assert fixture，完整 worker/runtime 运行待核验。

---

### 项目 2. CoreBunch/Instatic

- **仓库**：<https://github.com/CoreBunch/Instatic>
- **API 基本信息**：Stars: **5,636**；Forks: **520**；License: **MIT**；Language: TypeScript；`updated_at`: 2026-07-26T23:30:28Z；`pushed_at`: 2026-07-25T18:47:54Z；open issues/PR count: 52。
- **License 文件**：根 `LICENSE` 是 MIT，copyright 2026 David Babinec。
- **固定快照**：[`d97cac2`](https://github.com/CoreBunch/Instatic/commit/d97cac231e759d5ca445617193e53243d970b629)，commit time 2026-07-25T18:01:04Z。
- **Release / Issues**：最新 release [`v0.0.13`](https://github.com/CoreBunch/Instatic/releases/tag/v0.0.13) 在 2026-07-24；固定 commit 的 PR [#275](https://github.com/CoreBunch/Instatic/pull/275) 是 scheme parser security fix；[#281](https://github.com/CoreBunch/Instatic/pull/281) 指出 MCP tool discovery 未声明 open-workspace 前置条件会诱发无效重试；[#284](https://github.com/CoreBunch/Instatic/issues/284) 说明 Windows test teardown 尚有跨平台缺口。
- **一句话判断**：Instatic 值得学的是一条完整的**不可信扩展/外部 Agent 权限收窄链**：manifest declared permissions → owner granted permissions → central host dispatch enforcement → per-resource authorization → network host/IP/redirect revalidation → explicit publish。
- **解决的问题**：替代 host 直接动态 import 插件、相信 declared permission、allowlisted hostname 即可联网、MCP bearer 借浏览器高权限 cookie 越权、headless 与 live editor 两条写路径互相覆盖的旧做法。

#### 架构/实现与数据流

```text
CoreBunch/Instatic/
├── server/
│   ├── index.ts / router.ts                  # 单 Bun process 的 HTTP 路由
│   ├── plugins/
│   │   ├── pluginWorker.ts                   # 每 active plugin 一个 Bun.Worker
│   │   ├── quickjs/vm.ts                     # QuickJS-WASM security sandbox
│   │   ├── host/apiDispatch.ts               # target→permission 中央 enforcement
│   │   ├── host/network.ts                   # allowlist + DNS/IP + redirect SSRF guard
│   │   └── protocol/                         # schema、target、wire/body encoding
│   ├── ai/mcp/
│   │   ├── auth.ts / connectors/ / oauth/    # hashed token、PKCE、grant/capability
│   │   ├── registry.ts                       # capability-filtered tools
│   │   ├── contentAuthorization.ts           # own-vs-any target row 重验
│   │   └── editorBridge.ts                   # user+scope live workspace bridge
│   └── publish/                              # atomic static slots / cache / explicit publish
├── src/core/plugins/manifest.ts              # manifest schema/permission coherence
├── src/core/plugin-sdk/                      # authoring API + build/lint scan
├── src/__tests__/architecture/               # sandbox/import/permission structural gates
├── docs/features/{plugin-system,mcp-connectors}.md
└── package.json / bun.lock                    # Bun 1.3、QuickJS、TypeBox、MCP 等依赖
```

插件数据流：`zip/plugin.json -> parse/coherence/forbidden literal scan -> owner grants subset -> per-plugin Bun.Worker -> QuickJS bootstrap -> validated api-call -> host apiDispatch -> TARGET_PERMISSIONS + grantedPermissions -> handler/resource checks -> DB/network`。网络每一跳执行 `protocol + host allowlist + DNS resolution + blocked IP`。

MCP 数据流：`OAuth/PAT bearer -> hashed token lookup -> connector {userId, capabilities} -> capability-filtered tool registry -> per-row own/any authorization -> headless read/publish OR user+scope editor bridge -> draft flush -> optional explicit site_publish`。关键是 bridge 中 admin cookie 不能扩大 connector grant。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `server/plugins/quickjs/vm.ts` | sandbox lifecycle | per-VM memory/stack/deadline；固定 dispatcher handles；deferred host promises；dispose 后丢弃 late results |
| `server/plugins/host/apiDispatch.ts` | authority chokepoint | validated target 的完整 handler table；`TARGET_PERMISSIONS`；只读 `grantedPermissions`；结构化错误关联 |
| `server/plugins/host/network.ts` | SSRF kernel | http(s) only、exact/single-label wildcard、DNS all-address check、manual redirects、每跳重验、5-hop cap |
| `server/ai/mcp/registry.ts` | tool surface | headless/browser 分类；去重；capability filtering；不提供第二条 headless page-tree mutation |
| `server/ai/mcp/contentAuthorization.ts` | delegated authority | 在 relay 前按 target row 重验 own-vs-any，防 cookie privilege widening |
| `src/__tests__/architecture/plugin-sandbox-invariants.test.ts` | executable architecture | 禁 dynamic import 回退、锁 sandbox resource limits、中央 permission map 与 accepted target set |

#### 源码精读 1：权限只信 grant，并在 host dispatcher 中央执行

固定源码：[`apiDispatch.ts#L61-L73`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/plugins/host/apiDispatch.ts#L61-L73) 与 [`#L122-L151`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/plugins/host/apiDispatch.ts#L122-L151)

```ts
type HostApiHandlerTable = {
  [Target in AllowedApiTarget]: HostApiHandler<Target>
};

const apiHandlers = {
  'cms.routes.register': handleRoutesRegister,
  'network.fetch': handleNetworkFetch,
  'cms.content.tree.mutate': handleContentTreeMutate,
  // ... every schema target exactly once
} satisfies HostApiHandlerTable;
```

```ts
export async function dispatchApiCall(msg: ValidatedApiCall): Promise<void> {
  const entry = hostPlugins.get(msg.pluginId);
  if (!entry) return replyApiError(msg.pluginId, msg.correlationId, 'not loaded');
  try {
    const required = TARGET_PERMISSIONS[msg.target as keyof typeof TARGET_PERMISSIONS];
    if (required) assertHostPluginPermission(entry, required);
    const handler = apiHandlers[msg.target] as AnyHostApiHandler;
    await handler(msg, entry, db);
  } catch (err) {
    replyApiError(msg.pluginId, msg.correlationId, String(err));
  }
}
```

逻辑摘要：`AllowedApiTarget` 源自 schema keys，缺 handler 是编译错误；所有通用 permission 在调用 handler 前统一检查，authority 是 owner 实际批准的 `grantedPermissions`，不是 plugin 自报 `permissions`。条件式 public route / per-table access 留给 handler。VM bootstrap 同一 map 只是 defense-in-depth，host 才是 kernel。

#### 源码精读 2：allowlist 不是一次 URL 检查，每个 redirect 都重验 DNS/IP

固定源码：[`network.ts#L126-L159`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/plugins/host/network.ts#L126-L159) 与 [`#L202-L245`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/plugins/host/network.ts#L202-L245)

```ts
async function assertOutboundAllowed(manifest, urlString, resolveHost): Promise<URL> {
  const parsed = new URL(urlString);
  if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') throw new Error('unsupported');
  if (!hostMatchesAllowlist(parsed.host, manifest.networkAllowedHosts ?? [])) {
    throw new Error('host not in allowlist');
  }
  const addresses = isIP(parsed.hostname) ? [parsed.hostname] : await resolveHost(parsed.hostname);
  if (addresses.length === 0) throw new Error('host did not resolve');
  for (const address of addresses) {
    if (isBlockedAddress(address)) throw new Error(`blocked address ${address}`);
  }
  return parsed;
}
```

```ts
for (let hop = 0; ; hop++) {
  await assertOutboundAllowed(manifest, currentUrl, resolveHost);
  const response = await fetchImpl(currentUrl, {
    method, headers, body, signal: controller.signal, redirect: 'manual',
  });
  const location = response.headers.get('location');
  if (REDIRECT_STATUSES.has(response.status) && location) {
    if (hop >= MAX_REDIRECTS) throw new Error('redirect limit');
    currentUrl = new URL(location, currentUrl).toString();
    continue;
  }
  return serialize(response);
}
```

逻辑摘要：hostname 即使 allowlisted，只要解析到 loopback/private/link-local/CGNAT/ULA/metadata 就拒绝；Bun 禁止透明 follow，301/302/303/307/308 每跳重走 guard，最多 5 次。focused tests 真实覆盖 DNS rebinding、metadata redirect、非 allowlist redirect、public redirect 和 cap。剩余边界：DNS validation 与实际 socket connect 之间仍可能有 TOCTOU；源码未显示把已验证 IP pin 到连接（待核验），所以不能把它描述成完整消灭 DNS rebinding。

#### 源码精读 3：连接 token 不能借 owner browser cookie 扩权

固定源码：[`contentAuthorization.ts#L43-L69`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/ai/mcp/contentAuthorization.ts#L43-L69)

```ts
export async function authorizeMcpContentTool(
  db, userId, capabilities, toolName, input,
): Promise<void> {
  const checksEdit = DOCUMENT_EDIT_TOOLS.has(toolName);
  const checksPublish = DOCUMENT_PUBLISH_TOOLS.has(toolName);
  if (!checksEdit && !checksPublish) return;
  const row = await getDataRow(db, inputDocumentId(input));
  if (!row) throw new Error('not found');
  if (checksEdit) {
    if (capabilities.includes('content.edit.any') || capabilities.includes('content.manage')) return;
    if (capabilities.includes('content.edit.own') && ownsDocument(row, userId)) return;
  }
  if (checksPublish) {
    if (capabilities.includes('content.publish.any')) return;
    if (capabilities.includes('content.publish.own') && ownsDocument(row, userId)) return;
  }
  throw new Error(`Tool ${toolName} is not permitted for document`);
}
```

逻辑摘要：MCP browser tool 最终由 owner 的浏览器 session/cookie 执行，而该 cookie 可能比 connector grant 强；因此 relay 前必须以 `{connector userId, connector capabilities, target row}` 再验 own/any。真实 test 验证 own-only connector 不能借 owner browser 的 any-row authority。这个模式直接适用于 delegated Agent、subagent 与 workspace bridge。

#### 源码精读 4：sandbox 同时限制资源、固定 dispatch handle、处理 late async result

固定源码：[`quickjs/vm.ts#L93-L123`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/plugins/quickjs/vm.ts#L93-L123) 与 [`#L195-L239`](https://github.com/CoreBunch/Instatic/blob/d97cac231e759d5ca445617193e53243d970b629/server/plugins/quickjs/vm.ts#L195-L239)

```ts
export async function createPluginVm({ pluginSource, env, evalTimeoutMs }) {
  const ctx = (await getWasmModule()).newContext();
  ctx.runtime.setMemoryLimit(DEFAULT_MEMORY_LIMIT_BYTES);
  ctx.runtime.setMaxStackSize(DEFAULT_STACK_SIZE_BYTES);
  // bootstrap 后、plugin 前保存 persistent dispatcher handles，
  // 防 plugin 重写 globalThis.__runRoute 截获 host dispatch。
  const dispatcherHandles = new Map<DispatcherName, QuickJSHandle>();
  // ...
}
```

```ts
const hostCallHandle = ctx.newFunction('__hostCall', (targetHandle, argsHandle) => {
  const deferred = ctx.newPromise();
  pendingDeferreds.add(deferred);
  env.hostCall(target, ctx.dump(argsHandle)).then(
    (value) => {
      if (vmDisposed || !deferred.alive) return pendingDeferreds.delete(deferred);
      deferred.resolve(jsToHandle(ctx, value));
      pumpPendingJobs();
      pendingDeferreds.delete(deferred);
    },
    (err) => { /* reject + deadline-bounded pending-job pump */ },
  );
  return deferred.handle;
});
```

逻辑摘要：Bun.Worker 负责 crash 隔离，QuickJS 才是代码安全边界；memory/stack/deadline 在 plugin code 前设置；bootstrap dispatcher handle 在 plugin 运行前固定，避免 global overwrite；host async result 回来时若 VM 已 dispose 就丢弃，避免 use-after-free。边界是 editor entrypoint/app-kind admin code 文档明确**不在 sandbox**，它拥有 admin window/cookie/DOM 权限，必须作为不同信任级别。

#### 依赖分析与供应链风险

`package.json` 固定 Bun `>=1.3.0 <1.4.0`；核心运行依赖包括 TypeBox 0.34.49、MCP SDK 1.29.0、quickjs-emscripten 0.32.0、DOMPurify 3.4.2、happy-dom 20.9.0、sharp 0.35.3、esbuild 0.28.0、React 19.2.5、Vite 8.0.10、TypeScript 6.0.3。`bun.lock` 存在且 frozen install 成功。

风险：QuickJS-WASM、sharp/esbuild native/WASM surface、MCP/OAuth、DOM sanitization 都是高价值供应链/安全边界；Bun 小版本约束与 issue #284 显示跨 OS teardown 仍有差异；plugin zip 与 unsandboxed `editor.code` 扩大攻击面。focused `bun test` 通过只证明选中 contracts，不证明无 sandbox escape、无 OAuth 漏洞或全平台兼容。

#### 可复用经验、实验与落地路径

- **当**不可信扩展或外部 Agent 声明自己需要权限**时，应优先**把 declaration 与 authority 分开，并只在最终 host dispatcher 使用 owner 实际 grant；因为 manifest 是请求不是授权，边界是 resource-level 条件还需在 handler/chokepoint 重验。
- **当**允许插件/工具访问外网**时，应优先**对初始 URL 和每个 redirect hop 重验 scheme、host allowlist、全部 DNS 地址与 private/metadata ranges，并 fail-closed；因为首跳安全不代表重定向目标安全，边界是还需考虑 DNS-connect TOCTOU、响应体大小和 egress 审计。
- **可尝试实验（30 分钟）**：在 `runtime/hermes/github-learning-poc/delegated-authority-gate/` 建纯 fixture：`declared_effects / granted_effects / actor_scope / resource_owner / target_url / redirect_chain`，覆盖 declared-but-not-granted、owner-cookie-wider-than-token、allowlisted→metadata redirect、missing workspace；只输出 allow/deny/blocked evidence，不联网。
- **Skill 升格判断：需二次验证。** “declaration ≠ grant + final chokepoint revalidation + redirect-hop guard”跨 Hermes/OpenClaw/future-agent 可复用，但 shared 已有 config routing、verification-first 和 subagent 四状态规则；先做窄 POC 与查重，不复制 Instatic plugin SDK/QuickJS 源码。
- **Hermes/shared hub 落地路径**：
  1. runtime POC：`runtime/hermes/github-learning-poc/delegated-authority-gate/`；
  2. schema：`request={actor,delegation,scope,resource,effect,network_chain}`，`decision={allowed|denied|blocked|failed,reasons,evidence}`；
  3. Hermes 工具 wrapper 候选在执行 write/network/exec/config 前读取实际 grant，不把 skill description 当 authority；
  4. shared skill 候选只保留 portable contract、fixtures、验证命令和 pitfalls；不绑定 Bun/QuickJS/MCP SDK；
  5. 不接入 OpenClaw runtime；未来仅让其消费同一 schema。配置、cron、secret 和 publish 仍需显式用户授权。

#### 风险边界

- **License**：API、`package.json` 与根 LICENSE 都是 MIT；第三方依赖另审，MIT 不自动批准把实现复制到 shared。
- **维护活跃度**：commit 2026-07-25，release 2026-07-24，活跃；但项目 pre-1.0，`SECURITY.md` 明确“不建议未经仔细 operator review 用于 hostile multi-user environment”。
- **安全风险**：unsandboxed `editor.code` 与 admin app bundles 继承 admin cookie/DOM；QuickJS sandbox 不是浏览器代码隔离；OAuth/MCP token、plugin network、publish 都是高副作用面。
- **局限/不适用**：Instatic 定位 self-hosted single-site，不是多租户 SaaS 参考实现；live editor 作为 draft SSOT 要求 workspace 在线，不适合完全 headless 自动化；PR #281 证明只在失败信息里暴露前置条件会诱发 Agent 重试，应在 tool discovery 中声明。
- **验证局限**：26 focused tests 通过；未跑 6,283-test 全套、E2E 或 Windows。issue #284 的 247 Windows failures 仍是明确剩余风险。

---

## 经验沉淀

1. **当请求完成后仍有异步 reactor/checkpoint/index 工作时，应优先提供 scope-aware drain/receipt，而不是 sleep 或全局 polling；因为 queue empty 不等于 active work 完成，边界是 crash/cancel 必须产出终态。**
2. **当多个高频更新指向同一可覆盖资源时，应优先按 immutable scope key 合并 latest 并提供 `drainKey`；因为重复排队会放大延迟，边界是 append-only evidence、消息和交易绝不能 latest-wins。**
3. **当状态快照很大且已有 event stream 时，应优先把 snapshot 与 incremental events 分离，并给 snapshot load 有界 fallback；因为 transport 拆分能改善首帧，边界是仍需去重/压缩 payload 和 batch replay。**
4. **当扩展或 Agent 自报 capability/effect 时，应优先把 declaration 视为申请，在最终 host chokepoint 只信实际 grant；因为描述文本不是 authority，边界是 per-resource own/any 仍需二次检查。**
5. **当低权限 token 的调用最终由更高权限 session/cookie 代执行时，应优先在 relay 前以 token identity、scope、resource 重验，不能继承 executor 的更大权限；因为 delegation 不能自动 privilege widening。**
6. **当允许外网并支持 redirect 时，应优先每跳重验 scheme、allowlist、DNS/IP 与 redirect cap；因为 allowlisted 首跳可以跳向 metadata/private host，边界是 DNS-connect TOCTOU 与响应大小仍需独立防护。**
7. **当安全规则是架构不变量时，应优先写 architecture gate 锁定禁止 import、resource limits、target set 和 permission map；因为 prose 会漂移，边界是 grep-style gate 不能替代运行时攻击测试。**
8. **当前置条件（如必须打开 workspace）不是 Agent 可自行满足时，应优先在 tool discovery/schema 中声明并返回 non-retryable blocked，而不是等调用失败后才提示；因为盲重试会烧 token，边界是 precondition freshness 仍需调用时重验。**

### 今日最小综合实验

建议在 `runtime/hermes/github-learning-poc/scoped-authority-receipt/` 合并两个项目的机制，建立不联网、无配置写入的 fixture runner：

```text
input:  {run_scope,key,revision,actor,delegation,effect,resource,preconditions,network_hops}
check:  authoritative_grant -> resource_scope -> preconditions -> operation -> postcondition
output: {status: completed|blocked|denied|failed, through_revision, reasons, evidence_refs}
```

Fixtures 至少包括：active worker 期间 enqueue、不同 run scope 隔离、processor fail 留存 pending、declaration 未获 grant、low-priv token 借 high-priv cookie、workspace missing、allowlisted redirect 到 metadata。该 POC 不连接 provider、MCP、browser、network，不修改 Hermes/OpenClaw 配置。

## 风险边界（跨项目）

- GitHub Stars、License、更新时间是 API 查询快照；仓库 license 不是 transitive license/SBOM 审计。
- 不自动安装或接入 T3 Code/Instatic runtime 到 Hermes；不自动启用 provider、terminal、MCP、plugin、browser、network、publish。
- 不自动修改 Hermes/OpenClaw 配置、模型、auth、env、tools、skills、cron 或 secret；本任务未调用 OpenClaw。
- 不把 Agent/tool 自报 effect 当 authority，不把 admin cookie 权限继承给 connector/subagent，不把首跳 allowlist 当整条 redirect chain 授权。
- 不将 candidate 直接写入 curated active fact，不创建/修改 shared skill；raw clone、API、tests 和 issue evidence 留 runtime，完整分析留 inbox。
- T3 完整 worker tests 因 Node/pnpm prerequisites 未运行；Instatic 只跑 focused Linux tests，Windows issue #284、全量 E2E、QuickJS escape 与 DNS pinning 仍待核验。

## Skill 升格总判断

- `pingdotgg/t3code`：**需二次验证**。候选是 scope-aware completion receipt / keyed drain contract；不迁移 Effect beta、provider runtime 或 UI。
- `CoreBunch/Instatic`：**需二次验证**。候选是 declaration-vs-grant、delegated authority recheck、hop-by-hop network guard；不复制 plugin SDK/QuickJS/MCP 实现。
- 今日没有“可直接迁移”：两项都触及并发状态、授权或网络安全，必须有本地 fixture、失败恢复、existing-skill 去重和治理审查。

## Hermes/shared hub 落地路径

1. **实验层**：仅在 `runtime/hermes/github-learning-poc/scoped-authority-receipt/` 创建 fixtures/results；不进 curated/Git core。
2. **接口层**：用 JSON schema 定义 `scope_key / revision / actor / actual_grants / resource / effect / preconditions / receipts`，status 固定为 `completed|blocked|denied|failed`。
3. **Hermes 候选接点**：先用于 `scripts/github_learning_orchestrator.py` 的 prepare/report/audit completion evidence；不改 provider、tools 或 cron。
4. **shared 查重**：对照 `capabilities/manifests/shared-skills.yaml`、verification-first、subagent 四状态、self-reflection-engine；优先更新现有窄契约，避免新建宽泛 `agent-security`。
5. **分层落盘**：raw events/test logs/runtime state → `runtime/hermes/`；当日研究 → `inbox/hermes/daily/`；只有跨日、跨 Agent、经评分去重脱敏审查的稳定模式才候选进入 `curated/memory/facts/`。
6. **future agent 可移植性**：只消费 schema/fixture，不依赖 TypeScript/Effect/Bun/QuickJS；路径始终经 `scripts/resolve_shared_root.py`，不硬编码宿主路径。

## 明日继续

1. 实现 `scoped-authority-receipt` fixture runner，并真实验证 7 类完成/拒绝/阻塞/失败 case；这是下一步最小动作。
2. 在满足仓库 Node 24 + pnpm 11 prerequisites 的隔离环境中，运行 T3 Code `DrainableWorker.test.ts` 与 `KeyedCoalescingWorker.test.ts` focused tests；不跑全 workspace。
3. 研究 T3 issue #4596 的 batch/coalesced replay 修复进展，验证 batch apply 是否保持 sequence、approval/tool ordering 与 exactly-once projection。
4. 检查 Instatic network connect 是否 pin 已验证 IP 或仍存在 DNS-check/connect TOCTOU；在没有源码/测试证据前保持“待核验”。
5. 跟踪 Instatic #281 是否 merge，并把“不可自行满足的 precondition 在 discovery 中声明”做成 fixture，而不是关键词规则。
6. 跟踪 #284 的 DbClient close 设计与 Windows CI；不要把 Linux focused pass 外推为跨平台 clean。

## 候选反哺

### Candidate Facts

- [ ] topic: completion means scoped queue+active+pending quiescence, not request return or queue empty | evidence: T3 `DrainableWorker` / `KeyedCoalescingWorker` + focused source tests | 建议: update verification-first fact after local POC | 安全级别: low
- [ ] topic: delegated execution must retain delegator authority even when executor session is stronger | evidence: Instatic `contentAuthorization.ts` + 2 passing authorization tests | 建议: create after existing subagent fact dedup | 安全级别: medium
- [ ] topic: network allowlist must be revalidated on every redirect hop and resolved address | evidence: Instatic `network.ts` + 9 passing SSRF tests | 建议: update tool/network safety fact after DNS TOCTOU review | 安全级别: high
- [ ] topic: non-self-satisfiable tool preconditions belong in discovery and must still be rechecked at invocation | evidence: Instatic PR #281 description and registry architecture | 建议: create only after PR merge/fixture | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: scoped-authority-receipt fixture workflow | 可复用场景: cron、reflection、subagent、tool relay、network actions | 是否建议 shared: yes（POC 后） | 原因: 跨 Agent 的 completion+authority 合同，但须先与 verification/subagent/self-reflection 能力去重
- [ ] 名称: redirect-hop egress gate | 可复用场景: browser fetch、plugin/tool network、research downloader | 是否建议 shared: no（当前） | 原因: 还需 DNS pinning、response budget、proxy 行为与实际 Hermes tool boundary 核验
- [ ] 名称: tool precondition discovery auditor | 可复用场景: workspace/session/login/approval 前置条件 | 是否建议 shared: yes（先本地） | 原因: 能减少不可恢复调用和 token 重试，但需结构化 schema，不能只扫 description 关键词

### Candidate Open Questions

- [ ] 问题: T3 keyed coalescing 在 process 持续失败且 enqueue 持续到来时的重试/丢弃/告警策略是什么，是否可能 key starvation？ | reason: gap | priority: high
- [ ] 问题: T3 #4596 修复应在 event persistence、server replay batching、client batch apply 还是 markdown render memoization哪层完成，如何保持 sequence evidence？ | reason: adaptation | priority: high
- [ ] 问题: Instatic DNS 检查与实际 fetch connect 是否绑定同一已验证地址？ | reason: gap | priority: high
- [ ] 问题: Instatic #281 discovery hint merge 后，MCP client 是否真正减少不可满足工具的重试？ | reason: adaptation | priority: medium
- [ ] 问题: shared 现有哪个 skill 最适合承载 scoped completion + delegated authority，而不形成新宽泛 safety skill？ | reason: conflict | priority: medium

### 不应自动落地

- 不安装/启用 T3 Code 或 Instatic，不启动 provider、terminal、MCP、plugin、浏览器登录态、外网 fetch 或 publish。
- 不自动修改 Hermes/OpenClaw 配置、模型、auth、tools、skills、cron、secret；不调用 OpenClaw。
- 不把 candidate 写 curated active fact，不复制上游 runtime 源码，不把 runtime clone/node_modules/test logs 提交 Git。
- 不把 T3 的 3 个纯函数断言写成完整测试通过；不把 Instatic 26 focused Linux tests 写成全量/Windows/E2E 通过。
