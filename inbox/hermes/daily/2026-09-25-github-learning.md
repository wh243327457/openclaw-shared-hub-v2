---
type: case
status: archived
created: 2026-09-25
updated: 2026-09-25
domain: learning
tags: [github-learning, durable-workflow, replay, policy-enforcement, approval-identity]
---

# 2026-09-25 GitHub 热门项目学习报告

> 执行者：Hermes；本次未调用 OpenClaw。  
> 查询与验证时间：2026-09-25 07:31–07:49（UTC+08:00）。发现口径包括 GitHub Search API `created:>=2026-08-25 archived:false sort:stars` 与 `stars:>5000 pushed:>=2026-09-18 archived:false sort:updated`；Stars 是查询时快照。  
> 深读固定提交：`zai-org/ZCode@29628c9acdb81b703bbd4080c207a0e7ce5e276e`（tag/release `v3.14.3`）；`microsoft/agent-governance-toolkit@2ca7094ffec53df6610b7181446e78d264bd781c`。源码结论只绑定这些 revision。  
> 证据来源：GitHub Repository/Search/Commit/Release/Issues/Actions/License/Security Advisories API，README、docs、package manifests/lockfiles、关键源码与本机定向 build/lint/typecheck/tests。clone 位于 `runtime/hermes/github-hot-project-learning/repos/`。

## 今日结论

**可恢复 Agent 系统应把“执行”拆成两道互补的确定性边界：工作流层用稳定实例身份、输入哈希、journal 与首生结算次序保证 replay；副作用层在最终调用前用 fail-closed verdict、变换后 action identity 与审批重验保证授权——任何一层的 `completed/allow` 都不能替代外部结果 read-back。**

### 今日真实验证摘要

- `zai-org/ZCode`：固定 `v3.14.3` commit；`@zcode/dynamic-workflow` 在本机 Node `22.14.0`（上游要求 Node `24.14.0`）完成 typecheck、build、lint，lint 为 **0 warnings / 0 errors（94 files）**。README 所列 `pnpm test` 在当前 tag 实际没有匹配的 test files，手工 `vitest run` 返回 **No test files found / exit 1**，因此不能声称该 workflow core 测试通过。
- ZCode release `v3.14.3` 明确包含“运行中修改并发上限、优化修改后重启复用、降低 workflow 上下文占用”。GitHub Actions/check-runs API 对该 commit 返回空；仓库 API `has_issues=false`，所以 `open_issues_count=11` 不能作为可访问 issue 证据。
- ZCode 完整 workspace 的 `pnpm audit --prod --json` 实报 **182 vulnerability findings：21 low / 101 moderate / 59 high / 1 critical**；critical 为 `apps/zcode-cli/packages/tui > react-devtools-core > shell-quote@1.8.3` 的 GHSA-w7jw-789q-3m8p。它不在纯 `dynamic-workflow` 包的直接运行依赖中，是否进入具体发行物仍待 reachability / bundle 核验。
- `microsoft/agent-governance-toolkit`（AGT）：固定 main commit 的 `ci-complete` 与 CI 成功；本机更新到 Rust `1.98.1` 后，policy-engine Rust SDK 的 conformance corpus **3 passed / 0 failed**，fail-closed error parity **1 passed / 0 failed**。
- AGT release 最新为 `v4.1.0`（2026-06-09），而当前 core package manifest 已为 `5.0.0`、Rust SDK `0.4.0-beta.0`，main 与 release 存在明显版本差；issue #4048 仍记录 Python SDK reason/approval 等小正确性问题，issue #3349 的完整 evidence-led red-team benchmark 尚未闭环。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) | 34,957 | 3,007 | Go | Apache-2.0 | 2026-09-24T23:39:29Z | 高活跃分布式存储，后续可读一致性与故障恢复 |
| [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | 22,994 | 1,976 | Python | Apache-2.0 | 2026-09-24T17:22:53Z | 昨日已深读，今日不重复 |
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 19,814 | 1,322 | Python | MIT | 2026-09-18T16:28:35Z | typed decision 候选，已有历史深读 |
| [openai/codex-security](https://github.com/openai/codex-security) | 10,841 | 816 | TypeScript | Apache-2.0 | 2026-09-24T23:33:41Z | 安全证据 bundle 候选，已有历史深读 |
| [pydantic/monty](https://github.com/pydantic/monty) | 8,272 | 419 | Rust | MIT | 2026-09-24T23:29:57Z | AI 用安全 Python interpreter，后续候选 |
| [zai-org/ZCode](https://github.com/zai-org/ZCode) | 6,707 | 2,003 | TypeScript | Apache-2.0 | 2026-09-24T06:49:55Z | **深读：durable deterministic workflow/replay** |
| [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) | 6,331 | 1,127 | Python | MIT | 2026-09-24T23:48:40Z | **深读：fail-closed policy/approval chokepoint** |

> 表中 Stars、Forks、Language、License、时间均来自 2026-09-25 GitHub Repository API。License 只表示仓库根识别结果，不覆盖依赖、远端服务、模型、数据、release assets 或商标；Stars 与 push 活跃也不等于生产成熟度。

## 深读项目

### 1. zai-org/ZCode

- **一句话判断**：值得学的是把 Agent workflow 做成“纯编译/分析核心 + 窄 driver port + journal replay + sandbox harness”，并用输入哈希和首生结算次序恢复确定性；不应直接照搬整个产品或把 replay cache 当外部副作用已幂等。
- **解决的问题**：替代靠 prompt/prose 保存步骤、进程内 Promise 代表完成、崩溃后整段重跑的旧做法；把脚本 typecheck、site identity、typed ask schema、调度、journal、resume 与 app adapter 分层。
- **URL / API 快照**：https://github.com/zai-org/ZCode ；**Stars: 6,707 / Forks: 2,003 / Language: TypeScript / License: Apache-2.0**；`created_at=2026-09-20T12:01:16Z`，`updated_at=2026-09-24T23:40:09Z`，`pushed_at=2026-09-24T06:49:55Z`，default branch `main`，API `open_issues_count=11`，但 `has_issues=false`。
- **固定提交 / release**：[`29628c9acdb81b703bbd4080c207a0e7ce5e276e`](https://github.com/zai-org/ZCode/commit/29628c9acdb81b703bbd4080c207a0e7ce5e276e)，commit time `2026-09-24T06:49:06Z`；tag/release `v3.14.3` published `2026-09-24T10:54:12Z`。
- **Release / docs / checks**：release notes 核到运行中调并发、修改后重启复用、large workflow status 与 context token 优化。README 明确 Desktop/Web/CLI、SSH/WSL 本地上传链与 `dynamic-workflow` 包边界；`NOTICE.md` 明确默认不提供 OS sandbox、Hook/MCP/CLI 模式与凭据/日志风险。GitHub checks API为空，不能写 CI 通过。
- **来源交叉核验**：Repository/Commit/Release/Tags/License API、README、`apps/zcode-cli/packages/dynamic-workflow/README.md`、runtime README、NOTICE、root/dynamic-workflow package manifests、lockfile、engine/scheduler/journal/hash/settlement 源码与本机 build/typecheck/lint/audit。

#### 架构 / 实现与数据流

```text
workflow script
  -> compiler / analyzer
      typecheck + ask<T> JSON Schema + dependency/site graph + stable site id
  -> lowering
      facade calls -> __host calls
  -> sandbox child (vm context)
      ES intrinsics + __host only; NDJSON bridge
  -> parent WorkflowEngine (pure core)
      site ordinal + inputHash + AskScheduler + caps + settlement
  -> JournalStorePort
      run / actor / node / event; production adapter = SQLite
  -> WorkflowDriver
      actor session / model turn / world operation / cancel
  -> event projection + durable settlement
  -> resume/amend
      same script hash + recorded node + first-birth settle order + import cache gate
```

核心把 determinism 约束放在 host boundary：脚本不能直接读时钟、随机数、网络或磁盘；所有时间/外部结果都必须经 host 调用并 journal。`siteId@ordinal` 标识实例，`inputHash` 防止同一位置输入漂移，per-actor FIFO 保证准入，`ReplaySettleOrder` 恢复跨 actor 的首生完成顺序。纯 ask 可在工作区变更后继续复用；可能读取/修改世界的 cache 在第一笔 mutating effect 前关闭。

#### repo tree 摘要

固定 commit 共 **7,060 tracked files**，其中 `apps/zcode-cli/packages/dynamic-workflow/**` 为 **102 tracked files**；其核心树为：

```text
ZCode/
├── apps/zcode-cli/
│   ├── packages/dynamic-workflow/
│   │   ├── src/compiler/       # 虚拟 TS host、typecheck、纯度约束
│   │   ├── src/analysis/       # site/因果/flow/actor graph 与诊断
│   │   ├── src/schema/         # ask<T> -> JSON Schema 与 subset validator
│   │   ├── src/lowering/       # facade -> __host，注入 site id
│   │   ├── src/engine/         # WorkflowEngine、scheduler、journal、replay
│   │   └── package.json        # TypeScript-only pure package
│   ├── packages/dynamic-workflow-runtime/
│   │   └── src/                # child vm + NDJSON bridge + timeout/abort
│   ├── packages/core/          # Agent/tool/workflow product runtime
│   └── packages/bootstrap/     # production driver、SQLite/session wiring
├── packages/server|ui|desktop  # Web/桌面/共享 UI 与服务
├── pnpm-lock.yaml              # monorepo resolved graph
├── package.json                # v3.14.3 / Node >=24 / pnpm 10.33.2
└── README.md / NOTICE.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `apps/zcode-cli/packages/dynamic-workflow/src/engine/engine.ts` | 确定性 run 状态机 | 统一铸造 ordinal；script hash mismatch loud fail；恢复 usage/artifact/settle order；动态并发持久化 |
| `.../engine/scheduler.ts` | ask 准入、派发与结算 | per-actor FIFO；recorded node 先验输入哈希校验；running 重派、completed/failed 短路；cache purity gate |
| `.../engine/journal-memory.ts` | JournalStorePort 参考实现 | run/actor/node/event 分桶；深拷贝模拟存储边界；严格 sequence cursor；生产实现为 SQLite |
| `.../engine/hash.ts` | replay 输入一致性 | canonical JSON + FNV-1a 32-bit；明确仅防御性检查，不是密码学证明 |
| `.../engine/engine-settlement.ts` | run 终态 | first-wins；完成时取消未 await ask；终态与 artifact 同步落 journal；dispose 一次 |
| `.../dynamic-workflow-runtime/src/harness.ts` | sandbox bridge | 子进程/vm、NDJSON、timeout/abort，将 `__host` 调用映射到 engine |
| `apps/zcode-cli/packages/dynamic-workflow/README.md` | 边界契约 | 声明 pure core、site identity、compiler/lowering/runtime 分层与 test 命令 |

#### ⭐ 源码精读

**代码块 1：`WorkflowEngine` 恢复时拒绝脚本身份漂移，并从 journal 恢复顺序与累计状态。**

```ts
const existing = this.journal.getRun(this.runId);
if (existing === undefined) {
  this.journal.createRun({ runId: this.runId, caps: this.caps,
    spentTokens: this.spentTokens, status: "running", ... });
} else {
  if (existing.scriptHash !== undefined &&
      config.scriptHash !== undefined &&
      existing.scriptHash !== config.scriptHash) {
    throw new WorkflowError("ScriptHashMismatch",
      `Cannot resume run ${this.runId}: its script changed ...`);
  }
  const nodes = this.journal.listNodes(this.runId);
  this.replaySettleOrder = recoverSettleOrder(this.journal, this.runId, nodes);
  this.reportCount = nodes.filter((n) => n.kind === "report").length;
  this.spentTokens = existing.spentTokens;
  this.journal.updateRunStatus(this.runId, "running");
}
```

逻辑摘要：resume 只接受 byte-identical script；节点、报告数、artifact version、用量和首生 settle order 都从 durable state 恢复，而不是相信新进程内存。边界：`scriptHash` 两侧任一缺失时不拒绝；journal 本身的锁、事务、tamper evidence 与外部 effect idempotency 仍由 adapter/宿主负责。

**代码块 2：`AskScheduler.admitAsk()` 用 `(siteId, ordinal) + inputHash + actorSeq` 区分 replay、resume 与 fresh。**

```ts
const ordinal = this.host.nextOrdinal(siteId);
const instance = { siteId, ordinal };
const hash = inputHash(instructions);
const recorded = this.journal.getNode(this.host.runId, siteId, ordinal);
if (recorded !== undefined) {
  if (recorded.inputHash !== hash) {
    const err = hashMismatch(instance, recorded.inputHash, hash);
    this.host.failRun(err);
    return Promise.reject(err);
  }
  const seq = recorded.actorSeq ?? 0;
  if (recorded.status === "running") {
    actor.pendingRecorded.set(seq, () =>
      this.admitLive(instance, actor, seq, instructions, hash, spec, deferred, true));
  } else {
    actor.pendingRecorded.set(seq, () =>
      this.releaseCachedAsk(instance, recorded, deferred));
  }
}
```

逻辑摘要：已完成与已失败结果都按原 rejection/value 短路重放；崩溃时仍 running 的节点按原 actorSeq 重派。边界：`inputHash` 是 32-bit FNV-1a，源码自己说明不具抗碰撞性；安全/跨信任域 receipt 不能复用它，需 SHA-256/签名与 scope。

**代码块 3：`setMaxConcurrency()` 将 live retune 同步投影到内存、journal、事件，再主动 pump。**

```ts
setMaxConcurrency(maxConcurrency: number): boolean {
  if (this.runSettled) return false;
  if (!Number.isFinite(maxConcurrency)) return false;
  const previous = this.caps;
  const next = Math.max(1, Math.floor(maxConcurrency));
  if (next === previous.maxConcurrency) return false;
  const caps = { maxConcurrency: next };
  this.caps = caps;
  this.journal.updateRunCaps(this.runId, caps);
  this.record({ type: "run-caps-changed", runId: this.runId, caps, previous });
  if (next > previous.maxConcurrency) this.scheduler.pumpAll();
  return true;
}
```

逻辑摘要：同一个同步步骤完成 truth 更新与 event receipt，升高后立即重新扫描等待队列；降低不撤回已在飞 ask。边界：宿主仍负责机器级 ceiling、跨 run/provider 的全局配额和持久层原子性；单 run cap 不是全局资源安全。

**代码块 4：完成态先封口再取消未被 await 的分支，避免“run 完成但后台仍烧 token”。**

```ts
export function settleCompleted(state: EngineState, artifact: unknown): void {
  if (state.isRunSettled()) return;
  state.markSettled();
  state.abortInFlight(
    new WorkflowError("Cancelled",
      "Run completed; in-flight subagent tasks were abandoned."),
    true,
  );
  finishRun(state, "completed", { result: artifact });
  state.resolveSettled({ status: "completed", artifact });
}
```

逻辑摘要：terminal first-wins；`Promise.race` 输家或忘记 await 的 ask 被取消并补 terminal event，artifact 与 completed 同一 settlement 写入。边界：`driver.cancelAsk()` 仍可能只是合作式取消；已产生的文件/网络 effect 不会被撤销，必须另做 effect receipt/read-back/compensation。

#### 依赖分析与供应链风险

- root `package.json` 为 ZCode `3.14.3`，要求 Node `>=24.0.0`，README/mise 精确到 Node `24.14.0`、pnpm `10.33.2`；当前本机 Node `22.14.0`，所以 build/typecheck/lint 只能算兼容性实测，不等于支持矩阵通过。
- `@zcode/dynamic-workflow` 自身运行依赖只有 `typescript ^5.9.0`，dev 为 `@types/node`；纯 core 依赖面窄。整个 monorepo 有 33 workspace，lockfile 含 AI SDK、MCP、Electron、Playwright、native bindings 等，产品供应链远大于 core。
- `pnpm-lock.yaml` 固定 resolved versions，并对 `@ai-sdk/anthropic`、`@ai-sdk/openai-compatible`、`@arms/rum-electron` 使用本地 patches；patch hash 有助复现，但也意味着升级时需独立维护、复审补丁。
- 本机 frozen install 成功；dynamic-workflow typecheck/build/lint 成功，lint 0/0。README 宣称有 fixtures/tests，但 tag 中 `git ls-files .../tests/**` 为 0，`vitest run` 实际 exit 1，因此测试发布完整性存在明显断层。
- 完整 workspace production audit 为 182 findings；critical `shell-quote@1.8.3` 路径位于 TUI 的 `react-devtools-core`。不能把全仓 findings 全写成 dynamic-workflow 可达漏洞，但也不能把 pure core 的窄依赖外推成产品安全。

#### 可复用经验

- 当工作流需要 crash resume 时，应优先将每次 host 调用绑定稳定 instance identity、canonical input hash、durable terminal 与首生 settle order，因为“同一代码位置”不能恢复异步完成顺序；边界是 hash/journal 还需 scope、事务和 tamper 保护。
- 当 revision 可能复用前驱结果时，应优先按真实 effect purity 关闭缓存，而不是按 wall-clock 或“第一个 miss”关闭，因为并发兄弟之间未必存在依赖；边界是 purity 必须由宿主观测真实工具 effect，不能由模型自报。
- 当运行中需要调整并发时，应优先让 live truth、durable state、event receipt 与 scheduler rescan 在一个同步步骤收口，因为只改 UI/配置会在 resume 或排队时漂移；边界是单 run cap 不能替代全局 provider/CPU 配额。
- 当 run 进入 terminal 时，应优先主动结算/取消所有未完成分支并保证 exactly-one terminal，因为脚本顶层 return 不代表后台 Promise、进程或外部 effect 已停止。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/durable-run-replay-contract-v0/` 建一个纯 Python fixture：两个 actor 并发产生乱序完成；journal 记录 `run_scope/site_id/ordinal/actor_seq/input_sha256/status/result_hash/settle_seq`。模拟在一条 running、一条 completed 时 crash，fresh process replay 后验证：(1) completed 不重跑；(2) running 重试携同一 operation_id；(3) input 变化 loud fail；(4) settlement 顺序一致；(5) terminal 后无 live nodes；(6)外部 fake effect 必须 read-back 才从 `unknown` 转 `verified`。不连接 provider，不改 cron/config。

#### 风险边界

- **License**：仓库与 GitHub License API 为 Apache-2.0；第三方依赖、字体/图标/native assets、远端服务条款与商标需独立核验，`THIRD-PARTY-NOTICES.md` 不能被根 license 替代。
- **维护活跃度**：仓库创建 5 天即 6.7k Stars、2k Forks，但 Git 历史只有“open source”与 v3.14.3 两个公开提交路径；公开历史浅且 issues 被关闭，无法从 GitHub 常规 issue 流观察缺陷处理。
- **安全风险**：NOTICE 明确共享 Agent adapter 默认不提供 OS sandbox；Hook、MCP、shell、login shell、installer、凭据同步与模型日志都是 authority/data surface。完整 production graph audit 有大量已知 findings。
- **局限性**：纯 workflow core 的 deterministic replay 不证明 driver、SQLite、child kill、provider cancel 或外部 effect exactly-once；FNV hash不是安全 identity；cache purity依赖 host stats/observations准确。
- **验证局限**：本机 Node 版本低于项目要求；只完成 core typecheck/build/lint。测试目录在当前 tag 缺失，Vitest无 tests；未运行 Desktop/Web/CLI E2E、SQLite resume、真实子代理、远程 workspace 或 release asset。
- **不适用场景**：需要硬实时、跨信任域不可抵赖证明、不可幂等外部 effect 且没有 operation id/read-back、无 durable journal 或不允许 child process/sandbox 的场景。

#### ⭐ Skill 升格判断

**需二次验证。** 可迁移的是 `stable instance + input identity + journaled terminal + first-birth settle order + effect-aware cache gate + terminal drain`；不迁移 ZCode 产品、脚本 DSL、UI、provider 或公开仓库的绝对路径。先做离线 replay/effect fixture，并与现有 verification-first、completion receipt、subagent 四状态与 autonomous-learning workflow 去重；当前不创建 shared skill。

#### ⭐ Hermes / shared hub 落地路径

1. 在 `runtime/hermes/github-learning-poc/durable-run-replay-contract-v0/` 实现 agent-neutral journal schema 与 fake driver；runtime 只放实验产物。
2. 若 fixture 稳定，优先扩展现有 `scripts/github_learning_orchestrator.py` / reflection receipt：为每个阶段记录 `input_revision / operation_id / attempt / terminal / artifact_hash / readback_verified`，而非引入第二套 workflow engine。
3. Hermes adapter 只负责调用本地命令与状态写回；未来 agent 用各自 adapter，共享的只是真实 schema、fixtures 与 invariants。
4. 候选先写 `inbox/hermes/daily/`；经评分、去重、脱敏和人工审查后，才考虑更新既有 shared workflow skill 或 `curated/memory/facts/`。
5. 不自动改 Hermes/OpenClaw model、provider、auth、cron 或 secret；本轮不调用 OpenClaw。

---

### 2. microsoft/agent-governance-toolkit

- **一句话判断**：值得学的是把 policy engine 的纯 verdict 与 host 的 effect authority 分开，并让 transform、approval、identity re-derive、fail-closed reason 都在最终执行 seam 收口；不能直接采用的是把 application middleware 宣称成 OS 隔离、结果证明或完整合规。
- **解决的问题**：替代 prompt 里“请遵守规则”、OAuth/IAM 只管能否连服务却不管本次动作、以及审批只绑定易变 prose 的旧做法；通过 intervention point、canonical policy input、verdict 与 enforced identity 控制实际 tool/model/output effect。
- **URL / API 快照**：https://github.com/microsoft/agent-governance-toolkit ；**Stars: 6,331 / Forks: 1,127 / Language: Python / License: MIT**；`created_at=2026-03-02T22:11:47Z`，`updated_at=2026-09-24T23:30:40Z`，`pushed_at=2026-09-24T23:48:40Z`，default branch `main`，API `open_issues_count=104`（含 PR）。
- **固定提交 / release**：[`2ca7094ffec53df6610b7181446e78d264bd781c`](https://github.com/microsoft/agent-governance-toolkit/commit/2ca7094ffec53df6610b7181446e78d264bd781c)，commit time `2026-09-24T23:30:35Z`；最新 release `v4.1.0` published `2026-06-09T23:11:52Z`，不等于当前 main。
- **Release / issue / checks**：固定 commit GitHub `ci-complete` 最终 success；License Header、workflow lint、generation check 也 success。issue [#4048](https://github.com/microsoft/agent-governance-toolkit/issues/4048) 记录 Python SDK reason code、approval reason、warning 与 schema parity 问题；issue [#3349](https://github.com/microsoft/agent-governance-toolkit/issues/3349) 说明 action-level red-team benchmark只有初始 deterministic smoke phase 完成，4 个 follow-up 尚未 filed。
- **来源交叉核验**：Repository/Commit/Release/Issues/Actions/License API、README、ACS Specification、Known Limitations、Cargo/pyproject manifests、host evaluation/snapshot/approval 源码、conformance tests与本机 Cargo tests。

#### 架构 / 实现与数据流

```text
agent host action
  -> host assembles complete snapshot
  -> intervention point
      startup / input / pre|post model / pre|post tool / output / shutdown
  -> ACS runtime (stateless, deterministic)
      resolve policy target + project tool + collect annotations
      -> policy dispatcher (Rego / Cedar / custom)
      -> normalize allow | deny | transform
      -> fail closed on runtime error
  -> HostEvaluation
      transform validation/application + snapshot limit recheck
      canonical input_identity / enforced_identity
  -> enforce seam
      allow/transform -> execute effective target
      deny -> block
      liftable deny -> approval resolver
          rederive enforced_identity -> allow / deny / suspend
  -> telemetry/audit metadata
  -> application executes action and separately verifies outcome
```

重要分层：engine 只返回 verdict，不执行 effect；host 必须应用 transform、阻止 deny，并在审批时绑定“实际将执行的 action identity”。`evaluate_only` 仍验证 transform，但不应用，以便 shadow mode 提前暴露 enforce 时会 fail-closed 的配置。规范明确 runtime stateless，跨 turn label/provenance、外部结果与 outcome verification 都是 host obligation。

#### repo tree 摘要

固定 commit 共 **4,930 tracked files**，其中 `policy-engine/**` 为 **566 tracked files**：

```text
agent-governance-toolkit/
├── policy-engine/
│   ├── core/                 # 对 agent-control-spec 的兼容 shim 与 AGT 扩展
│   ├── sdk/rust/             # HostEvaluation、approval、FFI、conformance
│   ├── sdk/python|node/      # 语言绑定
│   ├── integrations/         # MCP / OpenAI / Rig / annotators / OTEL
│   ├── spec/                 # RFC 2119 runtime semantics + schemas
│   ├── tests/conformance/    # shared executable corpus / fail-closed fixtures
│   └── Cargo.lock            # Rust resolved graph
├── agent-governance-python/  # Agent OS/Mesh/Runtime/SRE/Compliance packages
├── agent-governance-typescript|rust|golang|dotnet/
├── docs/LIMITATIONS.md       # action/outcome/isolation/credential 等边界
├── examples/                 # governed framework integration
└── README.md / LICENSE / SECURITY.md
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `policy-engine/spec/SPECIFICATION.md` | 权威 runtime/host contract | stateless/deterministic/fail-closed、8 intervention points、canonical input、transform、approval与 telemetry |
| `policy-engine/sdk/rust/src/host/evaluation.rs` | engine result 到 host effect | transform point/path/limit 验证；enforce/evaluate-only分流；canonical SHA-256 identities |
| `policy-engine/sdk/rust/src/host/snapshot.rs` | 最终 enforcement seam | deny/block；liftable deny走resolver；审批身份三方一致；effective target选择 |
| `policy-engine/sdk/rust/src/host/approval.rs` | 审批返回契约 | `Allow / Deny / Suspend`，allow/suspend必须携 action identity |
| `policy-engine/sdk/rust/src/host/mod.rs` | SDK 主入口 | evaluate、enforce、startup/shutdown/tool/session wrappers |
| `policy-engine/sdk/rust/tests/conformance_corpus.rs` | executable spec | schema、coverage map、evaluate/approval fixtures与 expected verdict |
| `policy-engine/sdk/rust/tests/fail_closed_error_parity.rs` | reserved reason parity | 12 个 runtime reasons 全覆盖，errors 都必须转 deny |
| `docs/LIMITATIONS.md` | 诚实边界 | 不管 reasoning/outcome、非 OS kernel、跨 session chain、无政策默认 allow等 |

#### ⭐ 源码精读

**代码块 1：`HostEvaluation::from_engine_with_limits()` 在 host 应用 transform 前后都做边界校验。**

```rust
if verdict.decision == Decision::Transform && !point.transform_permitted() {
    return Err((HostError::TransformTargetForbidden,
        format!("a transform is not permitted at interception point {point}")));
}
let transformed_policy_target = match verdict.decision {
    Decision::Transform => {
        let applied = agent_hooks::apply_transform_path(
            target, &transform.path, transform.value.clone())?;
        let snapshot = snapshot_with_transformed_target(input, &applied)?;
        limits.validate_snapshot(&snapshot).map_err(|error| (...))?;
        if mode == EnforcementMode::Enforce { Some(applied) } else { None }
    }
    _ => None,
};
```

逻辑摘要：transform不能越出允许 intervention point，也不能让完整 snapshot 超预算；shadow/evaluate-only 虽不应用，也必须验证，从而避免 promotion hazard。边界：engine信任 host组装的 snapshot；snapshot错误或漏字段会导致 policy 在错误事实上确定性运行。

**代码块 2：identity 对 canonical policy input 取 SHA-256，区分 policy 看见的与最终执行的 action。**

```rust
pub fn identity(value: &JsonValue) -> Result<String, serde_json::Error> {
    let canonical = agent_control_spec::canonical_json(value)?;
    let digest = Sha256::digest(canonical.as_bytes());
    let mut hex = String::with_capacity(71);
    hex.push_str("sha256:");
    for byte in digest {
        write!(&mut hex, "{byte:02x}").expect("writing to String cannot fail");
    }
    Ok(hex)
}
```

逻辑摘要：`input_identity`覆盖原始 canonical policy input；若 enforce transform，`enforced_identity`覆盖变换后的目标。它可作为审批/audit correlation key。边界：无密钥 hash不是签名；若 host能伪造 snapshot或重写审计记录，digest不能提供外部不可抵赖。

**代码块 3：审批允许前重算 current identity，并要求 original/current/approved 三者全等。**

```rust
let original_identity = result.enforced_identity.clone()
    .or_else(|| result.action_identity.clone());
let resolution = resolver(intervention_point, result);
let current_identity = current_enforced_identity(result);
match resolution.outcome {
    ApprovalOutcome::Allow if approved_identity_matches(
        original_identity.as_deref(), current_identity.as_deref(),
        resolution.action_identity.as_deref()) => Ok(()),
    ApprovalOutcome::Suspend if approved_identity_matches(...) =>
        Err(AgentControlInterruption::Suspended(...)),
    _ => Err(blocked(intervention_point, &approval_action_mismatch_result())),
}
```

逻辑摘要：审批不是“点过同意”布尔值，而是对确切 canonical action 的授权；resolver panic、缺resolver、identity mismatch都 fail closed。边界：resolver同步执行；审批者看到的展示若不是同一 canonical object 的可信 projection，仍可能发生 human-readable mismatch。

**代码块 4：`enforce()` 只在 enforce mode 阻断，deny 与 liftable deny明确分流。**

```rust
if mode != EnforcementMode::Enforce { return Ok(()); }
match result.verdict.decision {
    Decision::Allow | Decision::Transform => Ok(()),
    Decision::Deny if result.verdict.approval.is_none() =>
        Err(blocked(intervention_point, result)),
    Decision::Deny => {
        let Some(resolver) = resolver else {
            return Err(blocked(intervention_point, &approval_unresolved_result()));
        };
        // resolver -> allow / deny / suspend; every mismatch blocks
    }
}
```

逻辑摘要：policy decision与host execution authority分开；evaluate-only只观察，不能被误报成 enforced。边界：只拦截经过 adapter/intervention point 的调用；绕过 adapter 的工具、shell、network仍在 trust boundary之外。

#### 依赖分析与供应链风险

- `policy-engine/Cargo.lock` 已提交；Rust SDK将 `agent-control-spec` 精确 pin 为 `0.4.0-alpha.3`、`agent-hooks-sdk` pin为 `0.1.0-alpha.5`，但规范状态仍 Draft/alpha，接口与安全语义仍可能破坏性变化。
- Rust SDK feature 默认关闭 bundled annotator dispatchers，并在 `Cargo.toml` 注释中披露 remote manifest→environment credential 与 OPA inherited environment风险；这是有价值的显式安全 gate，但也说明 manifest/policy dispatcher必须按高权代码对待。
- Python consolidated core `5.0.0` 依赖 ACS、Pydantic、PyYAML、cryptography、PyNaCl、HTTPX、aiohttp、structlog、jsonschema等，optional full/server/storage/MCP会显著扩大 graph；`migrate` extra 注释还指出 `agt-policies>=5.1.0` 当前不可解析（issue #4019）。
- 本机只编译并运行 Rust policy-engine两个定向 suites：conformance 3/3、fail-closed parity 1/1；没有安装/运行 Python full stack、MCP、OPA binary、Cedar external policy、云集成或多 SDK parity。
- 固定 commit CI 最终 success是上游证据，但部分 jobs显示 skipped，不能外推为每个语言/feature组合都已执行。公开 Security Advisories API返回空也不能证明无已知/未知依赖漏洞。

#### 可复用经验

- 当 policy engine 与真实副作用分属不同组件时，应优先把 engine限定为 verdict producer，并在host最终 chokepoint明确实现deny/transform/approval，因为“计算正确”不等于“执行方遵守”；边界是所有旁路都必须同样经过PEP。
- 当审批覆盖可变参数或transform后动作时，应优先对canonical enforced action identity授权，并在执行前重算，因为只绑定prompt、按钮或旧对象会留下TOCTOU；边界是审批UI必须从同一canonical对象生成。
- 当上线前使用shadow/evaluate-only时，应优先执行与enforce相同的schema、transform path和resource-limit验证，只跳过effect，因为宽松shadow会把promotion failure隐藏到生产首请求。
- 当审计记录只覆盖attempt/verdict时，应优先另设external outcome read-back与effect certainty，因为allowed/executed日志不能证明API、文件或业务目标真实成功。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/policy-action-identity-gate-v0/` 写纯 Python sans-I/O fixture：canonicalize `{agent,scope,tool,args,policy_revision}` 后取 SHA-256；policy返回 allow/deny/transform/needs_approval；fake approval只接受 exact enforced identity。覆盖：(1)批准后args变化必须blocked；(2)transform越界blocked；(3)shadow验证失败也blocked/not-promotable；(4)resolver异常blocked；(5)allow后fake external effect进入unknown，read-back匹配后才verified。不安装AGT、不改生产tool wrapper。

#### 风险边界

- **License**：仓库与GitHub License API为MIT；依赖、OPA/Cedar、云服务、示例框架和商标另审。license允许使用不等于默认安全或合规认证。
- **维护活跃度**：当前main于查询时仍持续push，固定commit CI成功；但最新release停在v4.1.0，main的Python core已5.0.0、Rust SDK beta，release/main/package identity明显漂移。
- **安全风险**：它是application middleware，不是OS kernel/sandbox；dispatcher以host trust运行。源码注释明确bundled dispatcher/OPA可能继承环境secret，remote manifest与policy必须视为高权输入。
- **局限性**：Known Limitations明确不管reasoning、外部outcome、跨动作恶意序列、knowledge provenance、credential lifecycle或物理/streaming安全；无policies或permissive default可能实际全放行。
- **验证局限**：只跑Rust定向conformance；未复现issue #4048 Python SDK问题，未跑full workspace、real OPA/Cedar/MCP、container isolation、multi-SDK互操作与red-team live tier。
- **不适用场景**：把middleware当硬隔离、需要token级stream enforcement、需要跨session全链路信息流但host不传播labels、无法封住旁路工具、或需要审批异步持久恢复而没有host状态机的场景。

#### ⭐ Skill 升格判断

**需二次验证。** `verdict producer / host effect gate / canonical enforced identity / approval revalidation / shadow validation / fail-closed reason` 与现有 verification-first、effect-scope、config-target-routing高度相关，应先以fixture验证并更新现有能力，而不是新建AGT专属skill。当前不安装AGT、不复制其MIT源码、不直接写curated active fact。

#### ⭐ Hermes / shared hub 落地路径

1. 在 `runtime/hermes/github-learning-poc/policy-action-identity-gate-v0/` 建纯decision core与fake effect adapter，schema中显式记录`policy_revision / input_identity / enforced_identity / verdict / effect_state / readback`。
2. 在Hermes工具执行包装层的最终dispatch前做host-owned effect/scope gate；如果当前Hermes没有统一wrapper，先只做shadow audit，不改`~/.hermes/config.yaml`、provider或tools配置。
3. 对cron/config/curated promotion等高权操作复用现有确定性规则；LLM/外部classifier只产proposal，不拥有最终authority。
4. evidence写`runtime/hermes/`，研究结论写`inbox/hermes/daily/`；通过治理审查后优先更新既有verification/governance skill，避免复制AGT整套平台。
5. future agent只读取agent-neutral contract；每个host分别证明所有真实effect path都经过gate。OpenClaw当前不存在，本轮不调用、不配置。

## 经验沉淀

1. 当工作流需要跨崩溃恢复时，应优先持久化稳定实例身份、canonical输入identity、明确terminal与首生结算顺序，因为重新执行同一脚本无法自动恢复异步因果；边界是journal还需scope、事务与外部effect幂等。
2. 当revision尝试复用前驱结果时，应优先由host按真实tool effect/replayability关闭cache，而不是按时间或第一个miss关闭，因为并发兄弟可能仍独立；边界是unknown effect默认不得复用。
3. 当policy与副作用执行分层时，应优先在最终host chokepoint重验verdict、scope、target与policy revision，因为prompt/engine返回值不会自动约束旁路；边界是没有统一PEP时只能shadow不能宣称enforced。
4. 当审批对象会被transform或随后变化时，应优先绑定canonical enforced action identity，并在执行前重新派生比较，因为按钮同意或旧参数会产生TOCTOU。
5. 当shadow/evaluate-only用于上线前评估时，应优先运行与enforce相同的transform/schema/resource校验，只跳过真实effect，因为宽松shadow会制造假安全。
6. 当run或policy记录`completed/allow/executed`时，应优先再做外部world-state read-back并把`unknown`保留为独立状态，因为attempt/verdict/transport ACK都不能证明业务结果。
7. 当上游package README声明tests但tag中缺fixture/test files时，应优先相信固定revision的tree与真实命令结果，并把发布完整性列为风险；文档不是测试产物。
8. 当monorepo的窄core依赖很小但完整产品graph很大时，应优先分别审core、adapter、runtime、installer与release bundle，因为一个package的低风险不能覆盖整个产品。

## 明日继续

1. 建 `durable-run-replay-contract-v0`：模拟并发乱序、crash、running重试、completed短路、input drift与terminal drain。
2. 建 `policy-action-identity-gate-v0`：覆盖transform、shadow、approval identity mismatch、resolver failure与effect read-back。
3. 深读 `pydantic/monty` 的resource/capability boundary，与AGT application gate对比“解释器级限制 vs middleware policy”。
4. 追踪AGT issue #4048/#3349；ZCode若发布包含tests的新tag，再用Node 24.14复跑fixture、runtime与resume E2E。

## 候选反哺

### Candidate Facts

- [ ] topic: durable Agent replay必须恢复首生settle order而不只恢复节点结果 | evidence: ZCode `recoverSettleOrder`、scheduler hold、fixed v3.14.3源码 | 建议: create candidate after fixture | 安全级别: medium
- [ ] topic: approval应绑定transform后的canonical action identity并在执行前重算 | evidence: AGT `HostEvaluation` + `snapshot::enforce` + conformance tests | 建议: update effect-scope candidate | 安全级别: high
- [ ] topic: completed/allow与external outcome必须分层 | evidence: ZCode settlement只能取消runtime task；AGT LIMITATIONS明确audit只记attempt | 建议: update completion receipt candidate | 安全级别: high
- [ ] topic: shadow mode必须验证未来enforce会执行的transform与limits | evidence: AGT `from_engine_with_limits`在两种mode都验证 | 建议: create/update verification candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: durable-run-replay-contract（更新现有completion/autonomous-learning workflow） | 可复用场景: cron、长任务、多agent fan-out、崩溃恢复 | 是否建议shared: yes（仅候选） | 原因: 跨agent横切，但先证明journal/settle/effect fixtures
- [ ] 名称: canonical-effect-approval-gate（更新现有verification/effect-scope workflow） | 可复用场景: 配置、发送、发布、删除、curated promotion | 是否建议shared: yes（仅候选） | 原因: canonical identity与effect-time revalidation可跨host复用，host adapter必须分离

### Candidate Open Questions

- [ ] 问题: shared hub现有reflection/cron状态能否在不引入第二engine的前提下表达settle_seq与running resume？ | reason: adaptation | priority: high
- [ ] 问题: 哪些Hermes tool path已有统一dispatch chokepoint，可安全做shadow policy而不改配置？ | reason: gap | priority: high
- [ ] 问题: ZCode dynamic-workflow tests为何在v3.14.3公开tree缺失，后续tag是否补齐？ | reason: conflict | priority: medium
- [ ] 问题: AGT main 5.0.0与latest release 4.1.0之间哪些contracts已稳定、哪些仍alpha/draft？ | reason: stale | priority: medium
- [ ] 问题: ZCode全仓audit的182 findings中哪些进入Linux CLI/Desktop release bundle且实际可达？ | reason: gap | priority: high

### 不应自动落地

- 不自动安装或启用ZCode/AGT，不把其workflow engine或policy runtime接入生产Hermes，不调用OpenClaw。
- 不自动改Hermes/OpenClaw config、model、provider、tools、auth、cron或secret；不从研究结论产生真实审批/副作用。
- 不直接写`curated/memory/` active fact、不创建新shared skill；candidate需经评分、去重、脱敏、fixture和人工审查。
- 不把replay cache当external effect exactly-once，不把policy allow当业务outcome，不把hash当签名，不把application middleware当OS sandbox。
- 不把GitHub Stars、空advisories、CI success、build/lint或定向tests外推为生产安全、全平台兼容、完整license审计或发行物已验证。
