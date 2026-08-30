# 2026-08-30 GitHub 热门项目学习报告

> 执行者：Hermes（未调用 OpenClaw）  
> API/运行查询时间：2026-08-30T07:33:58+08:00 至 07:42:44+08:00  
> 发现方法：GitHub Search API 查询 `created:>=2026-08-01` 并按 Stars 降序；Stars、Forks、Language、License、更新时间均来自 GitHub repository API。  
> 深读固定提交：`deepseek-ai/deepseek-harness@cd5ef8148158c3a752a658978873241fdf8e2bbc`；`firecrawl/anydoc@261fc257d17c3eab0f673be31c408fd9fdc2171a`。

## 今日结论

今天两项深读共同指向一条主线：**当 Agent 或文档摄取系统需要可组合、可恢复且可审计时，应优先把模型可见事实、工具副作用和部分覆盖都变成宿主可验证的结构化状态；插件化、统一输出和高热度本身不能替代 durable truth、最终执行 gate、资源上限与显式降级。**

### 今日证据与实测摘要

- GitHub Search API 实际返回的新建热门候选包括 DeepSeek Harness、dsh-desktop、watermarks-remover、anydoc、awesome-dsh-plugin、arc-task-gen、kimi-k3-in-c、openGym 等；速览不使用 README badge 作为 Stars/License 真相源。
- DeepSeek Harness 在固定提交上完成锁文件安装（`--frozen-lockfile --ignore-scripts`），并真实运行 session/tools/agent-loop 四个定向测试文件：**322 passed / 0 failed**。宿主 Node `v22.14.0` 低于项目声明的 `^22.19.0 || >=24.0.0`，因此不能外推全仓或 production runtime。
- DeepSeek Harness 的 `pnpm audit --prod` 实报 **25 条 advisory 记录（12 high / 12 moderate / 1 low）**；报告路径含 E2B、MCP、LLM adapter、subagent 与 test-support workspace。是否在具体部署可达需二次核验，不能直接称为可利用漏洞，也不能称为安全。
- anydoc 本机没有 Cargo，`cargo test --lib` 真实返回 exit 127；Rust 编译、fuzz、Cargo 供应链审计均标记待核验。作为替代的真实发布物 smoke 使用 npm `@firecrawl/anydoc@0.2.4`：DOCX 转换 exit 0、输出 1,316 bytes；全扫描 PDF exit 3、stdout 0 bytes、stderr 为 `anydoc: all 2 pages need OCR`。
- anydoc npm registry 返回版本 `0.2.4` 与 integrity `sha512-rfJx...`；Node lock 的 `npm audit --omit=dev --package-lock-only` 返回 **0 known advisories**，但不覆盖 Rust/Cargo、预编译 native binary、未知漏洞或 hosted OCR 服务。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 203,376 | 23,462 | TypeScript | MIT | 2026-08-27T17:06:36Z | **深读：插件树、事件溯源 Session、工具执行 gate** |
| [anywhere-labs/dsh-desktop](https://github.com/anywhere-labs/dsh-desktop) | 21,842 | 1,068 | TypeScript | MIT | 2026-08-29T06:37:10Z | DeepSeek Harness 桌面面候选，今日不重复同生态深读 |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | 19,244 | 2,243 | Python | MIT | 2026-08-29T22:10:43Z | 图像处理候选；训练数据与误用边界需另审 |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 19,198 | 1,133 | Rust | MIT | 2026-08-28T02:13:16Z | **深读：content detection、共享模型、资源上限、typed errors** |
| [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | 13,540 | 2,329 | Python | CC0-1.0 | 2026-08-29T16:24:19Z | 插件目录候选；每个插件仍须独立审许可与 effect |
| [pathwaycom/arc-task-gen](https://github.com/pathwaycom/arc-task-gen) | 8,818 | 58 | Python | MIT | 2026-08-11T09:52:10Z | benchmark 生成候选；issue #1 指出训练/评测集重叠风险 |
| [FareedKhan-dev/kimi-k3-in-c](https://github.com/FareedKhan-dev/kimi-k3-in-c) | 6,720 | 1,096 | C | Apache-2.0 | 2026-08-26T07:36:53Z | 教学实现候选；不把演示代码外推生产推理能力 |
| [arvids-unavailable/openGym](https://github.com/arvids-unavailable/openGym) | 6,250 | 1,016 | JavaScript | AGPL-3.0 | 2026-08-03T19:19:38Z | 维护信号偏弱且 AGPL 边界高，只观察机制 |

> 注：Stars 是 2026-08-30 07:33:58+08:00 的 API 快照，会继续变化。源码结论绑定固定提交，不把动态热度与源码 revision 混为同一证据。

## 深读项目

### 1. deepseek-ai/deepseek-harness

- **一句话判断**：值得学的是它如何让“所有能力都是插件”仍受 append-only Session truth、scope、工具流水线与最终结果冻结约束，而不是再引入一套 Agent runtime。
- **解决的问题**：替代“模型 adapter、工具、Session、agent loop、UI 与配置紧耦合，扩展只能 patch core”的旧做法；Profile + Bundle + Cordis plugin tree 允许替换 provider/capability，同时用 durable events 和 host-owned execution pipeline 保持可重放边界。
- **URL / API 快照**：https://github.com/deepseek-ai/deepseek-harness ；**Stars 203,376 / Forks 23,462 / Language TypeScript / License MIT**；`updated_at=2026-08-29T23:25:23Z`，`pushed_at=2026-08-27T17:06:36Z`，default branch `master`。
- **固定提交**：[`cd5ef8148158c3a752a658978873241fdf8e2bbc`](https://github.com/deepseek-ai/deepseek-harness/commit/cd5ef8148158c3a752a658978873241fdf8e2bbc)，GitHub commit API 时间 `2026-08-27T16:57:43Z`，内容为 release `dsh@0.1.2-alpha.1`。
- **Release**：[`dsh-v0.1.2-alpha.1`](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-alpha.1)，发布于 `2026-08-27T17:06:37Z`。
- **来源交叉核验**：README、`docs/architecture.md`、`docs/tool-execution-pipeline.md`、`docs/subsystems/core.md`、`SAFETY.md`、release、关键源码、package manifests 与本机定向测试/audit。仓库 API 显示 `has_issues=false`，GitHub issue 搜索为 0，故今日没有 issue lane 可核验。

#### 架构/实现与数据流

1. 启动时，Profile 按顺序叠加 Bundles、profile patch、home patch 与命令行 patch，形成 Cordis plugin tree；model adapter、tool registry、session log、agent loop 都是可替换插件。
2. 一轮 turn 从 inbox claim 开始：组装 system prompt/tool schemas，进入 `agent/pre-step` waterfall，记录 `turn/start` / `step/start` / `user/message`，由 LLM stream 产生 chunk 与 assistant message。
3. Session 是 append-only event log；模型历史由 ordered surface 上的事件投影，而非另存一份可漂移 messages。源码将 event payload 做 lossless JSON snapshot、deep freeze、连续 seq 与 surface invariant 校验。
4. assistant message 中的 tool calls 进入 `pre-execute → monotonic guards → execute waterfall/body → post-execute → finalizeContent → tools/result`；审批缺失/不可路由时 fail closed。
5. 工具最终结果先被 schema 验证并 lossless materialize，随后冻结并通知 observer；observer 失败被 containment，不能回写已确定 outcome。
6. 若工具结果要求下一步，loop 将 additional context 放回 `next-step` inbox；否则写 `turn/end`。因此 durable log 是恢复、fork、UI replay 和模型可见历史的共同来源。

#### repo tree 摘要

```text
deepseek-harness/                         # 固定提交 8,953 tracked files
├── apps/cli/                             # 唯一 Node 应用启动入口 dsh
├── apps/web/                             # Web 客户端
├── packages/core/                        # session/system-prompt/tools/agent/agent-loop/scope
├── packages/{llm,fs,shell,sandbox,...}/  # 可替换 capability seams 与 providers
├── packages/{skill,subagent,workflow}/   # skill、子代理与 workflow 能力
├── packages/bundle/                      # base/web/headless/sdk/acp 组合层
├── docs/                                 # 架构、子系统、生成 catalog、开发契约
├── vendor/cordis/                        # plugin/context/effect 框架
├── native/landlock-run/                  # Linux 限制执行辅助
├── python/                               # Python SDK/runtime 分发
├── scripts/                              # build、gate、catalog、release 检查器
├── snapshots/                            # session/SDK/ACP 等回放快照
├── package.json / pnpm-lock.yaml         # 265 workspace projects 与锁定依赖
└── SAFETY.md                             # preview、未安全审计与隔离局限
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/core/agent-loop/src/agent.ts` | turn/step/stream/tool 主循环 | inbox claim、pre-step waterfall、durable boundaries、stream assembly、tool continuation、request header/context |
| `packages/core/session/src/index.ts` | append-only Session 与 store | lossless snapshot、deep freeze、连续 seq、surface 校验、derived message cache、restore boundary |
| `packages/core/session/src/surface.ts` | 模型可见 surface projection | append/replace 规则、provenance、tool-result rewrite 与 transcript projection |
| `packages/core/tools/src/index.ts` | tool registry 与执行流水线 | pre/guard/approval/around/body/post/finalize/result、cancellation、canonical JSON output |
| `docs/architecture.md` | 组合和数据流契约 | Profile/Bundle、事件分类、turn flow、capability seam 与扩展点 |
| `docs/tool-execution-pipeline.md` | tool policy graph | guard、approval、fs gate、post transform、frozen authoritative outcome |
| `SAFETY.md` | 安全边界 | developer preview、未安全审计、插件/命令/网络/凭据风险、sandbox 非唯一控制 |

#### ⭐ 源码精读

**1) `private async turn(): Promise<boolean>`：durable boundary 包住每个模型 step**

```ts
private async turn(): Promise<boolean> {
  const turn = phase.turn + 1
  this.session.append('turn/start', { turn })
  try {
    while (true) {
      const step = phase.step + 1
      const decision = await this.preStep(target, { turn, step })
      if (decision.kind === 'reject') return false
      this.session.append('step/start', { turn, step })
      try {
        for (const message of decision.messages) {
          this.session.append('user/message', message, { surfaceOp: 'append' })
        }
        turnEnds = await this.step(decision.assembly, decision.startsRequestSeries === true)
      } finally {
        this.session.append('step/end', { turn, step })
      }
    }
  } finally {
    this.session.append('turn/end', { turn, reason: turnEnds! })
  }
}
```

逻辑：先开 turn，再由 pre-step 决定是否进入 step；模型可见输入先写日志，step 无论正常/异常都写 `step/end`，turn 也在 finally 中有终态。值得迁移的是“边界事件与业务动作同一个 owner”，而不是照搬 TypeScript loop。边界：append-only 不能自动保证外部副作用幂等，tool crash 后仍需 reconciliation。

**2) `append<T extends SessionEventType>(...)`：接受时即验证、复制、冻结并提交**

```ts
append<T extends SessionEventType>(
  type: T,
  data: SessionEventMap[T],
  ...opts: T extends SurfaceEventType ? [opts: SurfaceIntent] : []
): SessionEvent<T> {
  const dataSnapshot = snapshotJsonValue(data)
  if (dataSnapshot === undefined) {
    throw new Error(`session event "${type}" carries non-JSON-serializable data`)
  }
  const event = deepFreeze({
    type, seq: this.log.length, time: Date.now(), data: dataSnapshot,
    ...surfaceMetadataSnapshot,
  })
  this.surfaceManager.validateNext(event)
  this.log.push(event)
  return event
}
```

逻辑：拒绝 BigInt、函数、循环引用、稀疏数组或 exotic object 等非 lossless JSON；seq 由 log length 决定；surface transition 在 push 前验证，observer 在 commit 后运行且错误被 containment。这减少“内存已变、持久化才失败”的漂移。边界：内存 append 与异步 persistence flush 之间仍有 crash window，durable backend 必须有 checkpoint/repair。

**3) `async execute(exec: ToolExecutionInput)` 与 staged scheduler：让 policy 和 body 可组合但不跳过最终归一化**

```ts
async execute(exec: ToolExecutionInput): Promise<ToolExecutionResult> {
  return this.prepareExecution(exec, prepared => this.completeScheduledExecution(prepared))
}

private async completeScheduledExecution(prepared: ScheduledToolPreparation) {
  switch (prepared.kind) {
    case 'dispatch': {
      const dispatched = await this.dispatchScheduledExecution(prepared.exec)
      return dispatched.kind === 'post-result'
        ? await this.finalizeScheduledExecution(prepared.exec, dispatched.result)
        : this.finishScheduledExecution(prepared.exec, dispatched.result)
    }
    case 'post-result':
      return await this.finalizeScheduledExecution(prepared.exec, prepared.result)
    case 'final-result':
      return this.finishScheduledExecution(prepared.exec, prepared.result)
  }
}
```

逻辑：pre-policy/guard 可以直接产生 post-result 或 final-result；实际 body 只是其中一条路径。所有路径最终都经过 materialization/finalizer/result notification，避免 denial、invalid args 或 wrapper error 形成“没有权威终态”的旁路。

**4) `private async dispatchToolBody(...)`：调用方取消信号不可被 wrapper 替换掉**

```ts
private async dispatchToolBody(exec: MutableToolRunContext): Promise<ToolExecutionResult> {
  const wrapperSignal = exec.signal
  const fused = fuseToolSignals(state.callerSignal, wrapperSignal)
  exec.signal = fused.signal
  try {
    const tool = this.resolveExecution(exec.name, exec.agent, exec.parent !== undefined)
    if (!tool) throw new ToolNotFoundError(exec.name)
    state.bodyInvoked = true
    const returned = await tool.execute(exec.arguments, exec)
    const result = this.createSuccessResult(exec, tool, returned)
    return isAborted(exec.signal) ? toolAbortedResult(result) : result
  } catch (error) {
    return toolErrorResult(error)
  } finally {
    fused.dispose()
    exec.signal = wrapperSignal
  }
}
```

逻辑：around wrapper 可换 signal，但 registry 把原调用方 signal 融回去；body 开始前后分别产生 `ABORTED_BEFORE_DISPATCH` / `ABORTED` 语义，且不会抛弃已启动 promise。边界：same-process code 只能 cooperative cancel，不能 hard kill；外部不可逆 effect 仍可能在取消前发生。

#### 依赖分析与供应链风险

- 根 `package.json` 固定 `pnpm@11.7.0`，要求 Node `^22.19.0 || >=24.0.0`；本机 Node 22.14 触发 unsupported-engine warning。
- `agent-loop` 依赖/peer seam：`dsh-agent`、`dsh-llm`、`dsh-session`、`dsh-session-persistence`、`dsh-system-prompt`、`dsh-tools`、Cordis、settings 与 Schemastery。
- `tools` 依赖/peer seam：agent、code-runtime、LLM、scope、session、system-prompt、approval、Cordis 与 Schemastery。
- monorepo 安装真实识别 **265 workspace projects、1,292 lock entries、1,011 packages**，并报告多个 cyclic workspace dependencies；`--ignore-scripts` 避免执行 postinstall/native 下载，但也意味着不能据此证明发布物或 CLI 可运行。
- `pnpm audit --prod` 实报 25 条记录，涉及 `brace-expansion`、`js-yaml`、`protobufjs`、`fast-uri`、`ip-address`、`undici`、`hono`、`@hono/node-server`、`postcss`、`nanoid` 等。部分路径在 E2B/MCP/LLM/subagent，部分标在 test-support workspace；需按实际 bundle、输入可控性和部署路径做 reachability review。
- 安装期间两个 optional platform tarball（Claude Agent SDK Linux x64、Codex Linux x64）下载重试后未明确安装为可用；又因未 build，两个 `dsh` bin link 报目标 `apps/cli/lib/bin.js` 不存在。这些是 `--ignore-scripts`/未 build 环境限制，不应误判为上游 runtime defect。

#### 真实验证

- `npx pnpm@11.7.0 install --frozen-lockfile --ignore-scripts`：exit 0；锁文件 supply-chain policy 检查通过，但有 engine/platform/cycle/bin warnings。
- 定向命令：`vitest run packages/core/session/tests/session.spec.ts packages/core/session/tests/surface.spec.ts packages/core/tools/tests/tools.spec.ts packages/core/agent-loop/tests/loop.spec.ts`。
- 真实结果：**4 test files passed，322 tests passed，0 failed，3.73s**。
- 未运行：全仓 `check:all`、build、Web、provider、真实模型、MCP、PTY、E2B、Landlock、Windows、Python SDK 或 release asset smoke，均待核验。

#### 可复用经验

- 当 Agent 的 prompt、tool、provider 和 loop 都可被插件替换时，应优先把 durable truth、scope resolution、monotonic guard 与 final-result materialization 留在宿主确定性外壳，因为可组合性不应产生绕过终态的旁路；边界是同进程插件仍不是 OS sandbox。
- 当模型历史要支持恢复、fork、压缩与 UI replay 时，应优先从 append-only typed events 投影，并让每个模型可见输入都可由日志重建，因为单独维护 messages cache 会与真实事件漂移；边界是 persistence flush 和外部 effect 仍需独立 receipt。
- 当 tool middleware 可以换超时、重试或 signal 时，应优先重新融合原调用方取消与 authority，并区分 body-before/body-after cancellation，因为 wrapper 不应扩大执行权；边界是 cooperative cancellation 不能撤销已发生副作用。

#### 可尝试实验（30 分钟内）

在 `runtime/hermes/github-learning-poc/durable-tool-projection-v0/` 建纯 Python fixture：输入 `call_id/scope/input_hash`，依次产生 `pre_decision/body_invoked/canonical_value/terminal`，同时追加 event log 并从 log 重建 model projection。测试 observer throws、invalid JSON、cancel-before-body、cancel-after-body、post-policy block、duplicate terminal 六类情况。只用 synthetic data，不连接 provider、shell、MCP 或真实配置。

#### 风险边界

- **License**：GitHub API、root/package manifests 均为 MIT；但 `THIRD_PARTY_NOTICES.md`、native binaries、模型服务、第三方 plugins 与各依赖许可仍需逐项审查。
- **维护活跃度**：8 月 27 日发布 alpha，固定提交即该 release；热度和发布活跃，但 README 明确 developer preview 与 compatibility-breaking changes。
- **安全风险**：`SAFETY.md` 明确项目未经过安全审计，可执行模型生成命令、加载第三方插件并访问文件/进程/网络/凭据；sandbox、审批、权限控制不保证隔离。
- **供应链风险**：锁图大、workspace 多、含 native/platform packages；本次 production audit 有 25 条记录，且 ignore-scripts lane 未验证安装脚本与发布制品。
- **测试局限**：本机 Node 低于支持 floor，只跑了 4 个 core 测试文件；322 green 不能外推到所有 adapters、sandbox 或 production deployment。
- **不适用**：要求稳定 API、经过独立安全审计、强多租户 OS 隔离、最小依赖闭包或不能接受 breaking changes 的生产场景。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `durable tool projection + final-result chokepoint`，不是 DeepSeek Harness runtime 或 Cordis 源码。shared hub 已有 verification-first、effect-scope、completion/receipt、shared-memory 和 GitHub-learning 候选，直接新建 skill 会重复；先完成 fixture 与去重，若有增量只更新现有研究/验证 contract。今日不修改 `capabilities/skills/`、manifest 或 curated active fact。

#### Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/durable-tool-projection-v0/{schema.json,engine.py,fixtures/,test_engine.py}`。
- Hermes workflow 候选：给 `scripts/github_learning_orchestrator.py` 的状态增加 canonical `research_input_hash/report_hash/audit_version/audit_dimensions/terminal`，不再只由 Markdown 关键词推断业务完成。
- Shared skill 候选：二次验证后优先更新 `capabilities/skills/research/github-hot-project-learning/SKILL.md` 或 verification 类能力，加入“canonical evidence → projections”与 observer containment；不要创建 Harness 专用大 skill。
- 分层：raw 研究留 `inbox/hermes/daily/`；fixture、安装和测试日志只留 `runtime/hermes/`；经治理评分、证据、去重、许可与安全审查后，才提出 `curated/memory/facts/` candidate。
- 不安装/启动 DeepSeek Harness，不改 Hermes model/provider/tools/config/cron/secret；本任务不存在 OpenClaw runtime，也未调用 OpenClaw。

### 2. firecrawl/anydoc

- **一句话判断**：值得学的是 content-based format identity、共享 Document model、固定资源上限与 typed incomplete terminal 如何共同阻止“有 Markdown 就算完整”的错觉。
- **解决的问题**：替代针对 Word/PPT/Excel/PDF 分别 shell out 到多个转换器、输出风格不一致且扫描页/损坏附件可能静默丢失的旧做法；大多数格式先进入统一 Document model，再由单一 GFM serializer 输出。
- **URL / API 快照**：https://github.com/firecrawl/anydoc ；**Stars 19,198 / Forks 1,133 / Language Rust / License MIT**；`updated_at=2026-08-29T23:13:00Z`，`pushed_at=2026-08-28T02:13:16Z`，default branch `main`。
- **固定提交**：[`261fc257d17c3eab0f673be31c408fd9fdc2171a`](https://github.com/firecrawl/anydoc/commit/261fc257d17c3eab0f673be31c408fd9fdc2171a)，GitHub commit API 时间 `2026-08-28T02:13:16Z`。
- **Release**：[`v0.2.4`](https://github.com/firecrawl/anydoc/releases/tag/v0.2.4)，发布于 `2026-08-27T19:14:19Z`；引入 scanned-page `NeedsOcr` typed failure 与 opt-in hosted OCR。
- **来源交叉核验**：README、v0.2.4 release、open issues [#144](https://github.com/firecrawl/anydoc/issues/144)、[#139](https://github.com/firecrawl/anydoc/issues/139)、[#146](https://github.com/firecrawl/anydoc/issues/146)、关键 Rust 源码、Cargo/Node manifests 与真实 npm CLI smoke。

#### 架构/实现与数据流

1. `Format::from_bytes` 先按 RTF magic、OLE stream、ZIP package identity、PDF header 判定；CSV 没有 signature，才依赖显式 format 或 extension。
2. 非 PDF 输入进入 per-format parser（doc/docx/ppt/pptx/xls/xlsx/ODF/RTF/EPUB/CSV），统一输出 `model::Document` 的 blocks/inlines/tables/notes/assets。
3. `document_to_markdown` 统一处理 heading、list、table、footnote、anchor、quote、code 与 math，避免每个 parser 各自发明 Markdown escaping。
4. PDF 是显式例外：`pdf-inspector` 直接输出 Markdown；遇到扫描/图像页，0.2.4 返回 `NeedsOcr` 而不是静默丢页。
5. ZIP/XML/binary 路径应用不可配置的 entry/total bytes、entry count、XML depth/nodes、grid expansion、asset total 与 record depth/count 上限；`ResourceLimit` 在 optional part 路径也不可吞掉。
6. Node/Python/Wasm bindings 暴露相近 API；Node/Python/CLI 的 hosted OCR 只在显式 opt-in 后发送整个需要 OCR 的文档，Rust core 不发网络请求。

#### repo tree 摘要

```text
anydoc/                                  # 固定提交 329 tracked files
├── src/lib.rs                           # Format API、to_markdown/to_document 总入口
├── src/formats/                         # detect 与各文档格式 parser
├── src/model/                           # 共享 Document/Block/Inline/Table/Asset 模型
├── src/render/markdown/                 # 单一 GFM serializer、escape/table/anchor
├── src/package/                         # ZIP/XML/path/relationship 与 hard limits
├── src/error.rs                         # typed ConvertError 与稳定 code
├── node/                                # N-API binding、CLI wrapper、package-lock
├── python/                              # PyO3/maturin binding
├── wasm/                                # browser WebAssembly binding
├── tests/fixtures/                      # 正常、malformed、abuse 文档 fixtures
├── tests/robustness.rs                  # mutation robustness
├── fuzz/                                # per-format cargo-fuzz targets
├── skills/convert-documents-to-markdown # 上游 Agent Skill
├── bench/                               # 质量/性能评测 harness
├── Cargo.toml / Cargo.lock              # Rust 1.88、直接和锁定依赖
└── .github/workflows/release.yml        # crate/npm/PyPI 多制品发布
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/lib.rs` | 公共入口与 parser routing | content-first detection、extension fallback、PDF direct path、Document → Markdown |
| `src/formats/detect.rs` | 内容身份判定 | RTF/OLE/ZIP/PDF，OPC rel/content type/root/path 多级 fallback |
| `src/model/*` | 统一中间模型 | 多格式共享 blocks、inlines、tables、notes、assets |
| `src/render/markdown/mod.rs` | GFM serializer | note order、escaping、block/list/table/math/code rendering |
| `src/package/limits.rs` | 固定安全下限 | decompression、XML、grid、expansion、asset、binary record caps |
| `src/package/archive.rs` | ZIP budget enforcement | declared size + capped reader、total budget、cache、fatal limit propagation |
| `src/error.rs` | typed terminal | `unsupported/needsOcr/malformed/encrypted/resourceLimit/missingPart/io` |
| `skills/convert-documents-to-markdown/SKILL.md` | Agent adapter 说明 | CLI 用法、exit 0/1/2/3、大文档落盘与 hosted OCR 规则 |

#### ⭐ 源码精读

**1) `pub fn to_markdown_bytes(...)`：共享模型为主，PDF direct path 是显式例外**

```rust
pub fn to_markdown_bytes(
    bytes: &[u8],
    format: impl Into<Option<Format>>,
) -> Result<String, ConvertError> {
    let format = resolve_format(bytes, format.into())?;
    if format == Format::Pdf {
        return formats::pdf::to_markdown(bytes);
    }
    Ok(document_to_markdown(&to_document(bytes, format)?))
}

pub fn to_document(
    bytes: &[u8],
    format: impl Into<Option<Format>>,
) -> Result<model::Document, ConvertError> {
    formats::parse(bytes, resolve_format(bytes, format.into())?)
}
```

逻辑：所有非 PDF parser 统一进入 Document model；PDF 因 `pdf-inspector` 已直接产生 Markdown，不伪装成支持 Document model。这个例外被类型/API 文档公开，优于暗中返回缺字段的假统一。边界：调用方若依赖 `Document.assets`，必须对 PDF 明确标 `unsupported`。

**2) `pub(crate) fn from_bytes(bytes: &[u8]) -> Option<Format>`：先容器身份，后 extension**

```rust
pub(crate) fn from_bytes(bytes: &[u8]) -> Option<Format> {
    if bytes.starts_with(b"{\\rtf") { return Some(Format::Rtf); }
    if bytes.starts_with(&OLE_MAGIC) { return detect_ole(bytes); }
    if bytes.starts_with(b"PK\x03\x04") { return detect_zip(bytes); }
    if bytes[..bytes.len().min(1024)].windows(5).any(|w| w == b"%PDF-") {
        return Some(Format::Pdf);
    }
    None
}
```

逻辑：ZIP 不等于 DOCX，而要继续读 ODF/EPUB mimetype 或 OPC relationship、content type、root element和 conventional part；OLE 读 mandated stream name。这样错误扩展名仍可识别，普通 ZIP 不会冒充文档。边界：CSV 没 signature；explicit format override 仍需 host policy 与 source receipt。

**3) `pub fn document_to_markdown(doc: &Document) -> String`：一次修复，多格式复用**

```rust
pub fn document_to_markdown(doc: &Document) -> String {
    let rc = Ctx { nums: number_notes(doc), anchors: resolve_anchors(doc) };
    let mut parts: Vec<String> = doc.blocks
        .iter()
        .filter_map(|b| render_block(b, &rc))
        .collect();
    // Footnotes are emitted in first-reference order; duplicate ids are dropped.
    let mut out = parts.join("\n\n");
    if !out.is_empty() { out.push('\n'); }
    out
}
```

逻辑：heading/list/table/footnote/code/math 等都由共享 renderer 处理；例如 table escaping 修复不必在 DOCX、RTF、ODT 各写一份。边界：统一 serializer 只统一输出规则，不保证每个 parser 都完整提取资产；issue #139 就显示 XLSX embedded image 在进入 Document 前已丢失。

**4) `pub fn part(&mut self, name: &str)`：declared size 不可信，再用 capped reader 验证**

```rust
pub fn part(&mut self, name: &str) -> Result<Option<Rc<[u8]>>, ConvertError> {
    let mut file = match self.zip.by_name(name.trim_start_matches('/')) { /* ... */ };
    if file.size() > limits::MAX_ENTRY_BYTES {
        return Err(ConvertError::ResourceLimit { limit: "max_entry_bytes", detail: /* ... */ });
    }
    let remaining_total = limits::MAX_TOTAL_BYTES.saturating_sub(self.total_read);
    let cap = limits::MAX_ENTRY_BYTES.min(remaining_total);
    let mut bytes = Vec::new();
    let read = (&mut file).take(cap + 1).read_to_end(&mut bytes)? as u64;
    if read > cap { return Err(/* max_total_bytes or max_entry_bytes */); }
    self.total_read += read;
    Ok(Some(Rc::from(bytes)))
}
```

逻辑：既检查 ZIP 声明的解压大小，也通过 `take(cap + 1)` 防声明欺骗；同 part cache 命中不重复计费，总预算为 512 MiB、单 entry 为 128 MiB。optional part 可以跳过普通损坏，但 `ResourceLimit` 永远传播。边界：内存 hard cap 仍不能替代进程 deadline、CPU budget、sandbox 与总输入大小 gate。

#### 依赖分析与供应链风险

- `Cargo.toml`：anydoc `0.2.4`、Rust edition 2024、`rust-version=1.88`。
- Rust 直接依赖：`cfb 0.14.0`（OLE）、`csv 1.4.0`、`flate2 1`、`encoding_rs 0.8.35`、`log 0.4`、`pdf-inspector 1.14.2`、`quick-xml 0.41.0`、`zip 8.6.0`（仅 deflate）。
- `Cargo.lock` 固定 transitive graph，但本机无 Cargo，未运行 `cargo audit`、Rust compile、unit tests 或 fuzz；这一 lane 为 **blocked/待核验**。
- Node CLI 通过 npm 下载平台预编译制品；`npm view` 返回 `0.2.4`、tarball URL 与 registry integrity。integrity 能校验下载内容与 registry metadata 一致，不是签名或可复现构建证明。
- Node lock `npm audit --omit=dev --package-lock-only` 为 0 known advisories，报告 production dependency 1、optional 58；不覆盖 Rust lock、native binary、hosted OCR API 或未知漏洞。
- hosted OCR 会把整个文档发送给 Firecrawl Parse；README 明确没有 page selection。它是隐私/合规/网络副作用，绝不能自动 fallback，也不能在 shared 中保存 key。

#### 真实验证

- `cargo test --lib`：`cargo: command not found`，exit 127；如实标记 Rust lane 待核验。
- `npx --yes @firecrawl/anydoc --version`：`0.2.4`。
- DOCX fixture `tests/fixtures/docx/text.docx`：exit 0，输出 1,316 bytes，实际包含 heading、bold/italic/strikethrough、nested lists、table、footnotes、Unicode、escaped Markdown 与 links。
- 全扫描 PDF fixture `tests/fixtures/pdf/handmade-scanned.pdf`：exit 3，stdout 0 bytes，stderr `anydoc: all 2 pages need OCR`，符合 v0.2.4 release contract。
- 未运行：PPT/XLS/ODF/EPUB 全格式矩阵、Wasm/Python binding、hosted OCR、benchmark、fuzz、Cargo tests/audit，均不可外推。

#### 可复用经验

- 当 Agent 摄取扩展名可伪造的复杂文件时，应优先使用 content/container identity，并把 declared extension、detected format 与 conflict 一起写 receipt，因为文件名不是可信类型；边界是无 signature 的 CSV 仍需显式声明。
- 当多个 parser 要产生一致输出时，应优先汇入共享 canonical model 再生成 Markdown/UI projection，因为输出修复可复用且便于验证；边界是 parser 未提取的资产不会被 serializer 自动补回。
- 当文档只部分可读时，应优先把 coverage 与 terminal 分开表达，禁止 partial silently masquerade as complete，因为“拒绝全部”与“静默缺页”都可能不适合调用方；边界是 partial 是否可接受必须由宿主 policy 决定。
- 当 ZIP/XML/binary parser 面对不可信输入时，应优先提供不可配置的安全下限，并在其上再加进程 deadline/sandbox，因为调用方漏配不应关闭最小防线；边界是 hard cap 不能防所有 CPU 算法复杂度攻击。

#### 可尝试实验（30 分钟内）

更新既有 `runtime/hermes/github-learning-poc/document-ingestion-receipt/` 设计为纯 wrapper fixture：记录 `source_hash/declared_extension/detected_format/converter_version/status/coverage/error_code/output_hash/output_bytes/network_used`；用公开 DOCX、scanned PDF、mixed PDF 和伪扩展 ZIP 验证 `complete/partial/needs_ocr/unsupported/blocked`。默认禁止 hosted OCR，不处理私有文件，不把转换全文写 curated。

#### 风险边界

- **License**：GitHub API、Cargo manifest 与 LICENSE 都是 MIT；依赖与 npm/native 发布物仍需各自 license review。
- **维护活跃度**：8 月 27 日发布 v0.2.4，8 月 28 日仍有 push，当前有 31 个 open issues；活跃不等于边缘格式已完整。
- **已知局限**：issue #144 指出 mixed PDF 中一个 image-only page 会让 0.2.4 丢弃其他可读页的全部输出；issue #139 报 XLSX embedded images 未进入 `Document.assets`；issue #146 请求 local OCR/image parser。上述是上游 issue 证据，本机仅实测全扫描 PDF，不声称本机复现 #139/#144。
- **安全风险**：复杂 ZIP/XML/OLE/binary parser 仍有 parser bug 与 CPU/memory attack surface；固定 cap 只是下限。`npx`/native binary 是供应链执行；hosted OCR 是整个文档外传。
- **完整性风险**：统一 Markdown 不等于完整内容。assets、mixed scanned pages、layout、图表、宏语义可能缺失；输出必须携带 coverage/error/provenance。
- **不适用**：要求本地 OCR、严格保留视觉布局/图片定位、加密文档、不能接受 native/npm 制品、或必须证明所有页面完整的高保证流程。

#### ⭐ Skill 升格判断

**需二次验证**。上游已自带 `skills/convert-documents-to-markdown/SKILL.md`，但不应直接复制/安装到 shared：Hermes 已能读取多类文档，且 shared 需要 network/effect/large-output/coverage 统一 contract。可迁移的是 `document-ingestion-receipt`，先更新 existing POC、加入 mixed/asset/hosted-OCR fixtures，再决定是否更新现有文件读取/研究 skill。今日不创建新 shared skill。

#### Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/document-ingestion-receipt/{schema.json,wrapper.py,fixtures/,test_wrapper.py}`；若已有目录则增量更新，不另建重复项目。
- Hermes adapter：先 content detection，再调用本地 converter；输出超过预算时落 `runtime/hermes/` 并返回 hash/bytes/truncated/pointer，不能把全文塞入 curated 或 prompt。
- 状态 contract：至少 `complete | partial | needs_ocr | unsupported | resource_limit | failed`，同时携带 detected format、converter version、source/output hash 与 network-used。
- hosted OCR：默认 disabled；若未来用户显式授权，只从 Hermes 本地 secret 变量读取 `$FIRECRAWL_API_KEY`，不得写 shared，且在发送前确认文档可外传。无人值守任务遇到 OCR 应返回 blocked/needs_ocr，而非自动联网。
- Shared skill：二次验证后优先更新已有研究/文件摄取能力的 reference 与 conformance fixture，不复制上游一页式 skill 作为新的 class-level 能力。

## 经验沉淀

1. 当 Agent 系统允许插件替换 prompt、tool、provider 或 loop 时，应优先把 append-only truth、scope、guard、canonical output 与 terminal 留在宿主确定性外壳，因为可组合性不能等于可绕过；边界是同进程外壳也不是 OS 隔离。
2. 当模型可见历史需要恢复、fork、压缩或多 UI projection 时，应优先从带连续 identity/provenance 的事件日志重建，而不是维护第二份可变 messages，因为缓存与真实执行会漂移；边界是 persistence flush 与外部副作用仍要 reconciliation。
3. 当 tool middleware 能替换 signal、重试或超时时，应优先融合原调用方取消并记录 `body_invoked`，因为取消前后语义不同；边界是 cooperative cancel 不能撤销已经提交的外部 effect。
4. 当 Agent 摄取 DOCX/PDF/ZIP 等复杂文件时，应优先使用 content/container identity、固定资源上限与 typed terminal，因为扩展名、exit 0 和非空 Markdown 都不能证明完整；边界是 parser 本身还要 deadline/sandbox。
5. 当多个格式共享一种输出时，应优先先构造 canonical model、再生成 Markdown/UI/索引 projection，因为格式修复可复用；边界是进入 canonical model 前的漏提取仍需 coverage tests。
6. 当输入部分可读、需要 OCR 或有资产缺失时，应优先分开 `terminal` 与 `coverage`，由宿主显式选择 refuse/partial/fallback，因为静默缺页和全量拒绝都不是普适答案；边界是 hosted fallback 还涉及隐私、费用与授权。
7. 当本机工具链低于上游要求或完全缺失时，应优先保留真实 warning/exit 并标 blocked/待核验，因为定向绿色 tests、README benchmark 或另一发布 binding 都不能证明全仓通过。
8. 当 production audit 返回 advisory 时，应优先记录 scanner、lock revision、dependency path、severity 与 reachability 待核验，不能把 finding 直接夸大成已利用漏洞，也不能用另一个生态的 0 findings 抵消它。

### 今日总 Skill 升格判断

- `durable-tool-projection-v0`：**需二次验证**；优先更新已有 verification/GitHub-learning contract，不引入 DeepSeek Harness runtime。
- `document-ingestion-receipt`：**需二次验证**；已有 POC/历史候选，先增量补 mixed PDF、asset coverage、network-used 与 typed terminal，不新建重复 skill。
- DeepSeek Harness 完整插件/runtime 与 anydoc 上游 Agent Skill：**暂不直接沉淀**；前者 authority/supply-chain surface 大，后者尚未满足 shared hub 的 coverage/privacy/effect contract。
- 今日不修改 `capabilities/skills/`、manifest、Hermes config/model/provider/cron/secret，也不写 curated active fact。

## 明日继续

1. 在现有 `runtime/hermes/github-learning-poc/document-ingestion-receipt/` 增加 mixed PDF 与 XLSX-asset fixture，验证 `terminal != coverage`，并确认输出 pointer/hash/bytes 的 readback。
2. 新建或合并 `durable-tool-projection-v0` synthetic fixture，覆盖 observer failure、invalid JSON、cancel-before/after-body、post block 与 duplicate terminal；先和 completion/effect-scope 候选去重。
3. 若环境升级到 Node 22.19+，固定同一 DeepSeek Harness commit 重跑 322 tests 和更广 core gate；当前 22.14 结果保留 incompatible warning。
4. 若后续获得 Cargo/Rust 1.88 环境，固定 anydoc commit 运行 `cargo test --locked` 与 cargo audit；未完成前 Rust/fuzz/供应链 lane保持待核验。
5. 复核 anydoc issue #144/#139 的修复与 release 状态；在 mixed PDF coverage 未解决前，禁止把 anydoc exit 0/3 压成单一 completed 布尔值。

## 候选反哺

### Candidate Facts

- [ ] topic: plugin-everything 架构仍需 host-owned durable truth 与 final-result chokepoint | evidence: DSH `docs/architecture.md`、`agent.ts`、`session/index.ts`、`tools/index.ts`、322 passed | 建议: update verification/effect-scope candidate | 安全级别: medium
- [ ] topic: 文档摄取的 terminal 与 coverage 必须分离 | evidence: anydoc v0.2.4 `NeedsOcr`、issue #144/#139、DOCX/PDF smoke | 建议: update document-ingestion candidate | 安全级别: medium
- [ ] topic: fixed parser limits 是最低防线而非完整 sandbox | evidence: anydoc `limits.rs`/`archive.rs` 与 blocked Cargo lane | 建议: update existing ingestion security candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: durable-tool-projection-v0 | 可复用场景: Hermes tool audit / GitHub learning / future-agent execution receipts | 是否建议 shared: yes-after-fixtures | 原因: 跨 Agent 横切，但需与 verification-first、completion/receipt、effect-scope 去重
- [ ] 名称: document-ingestion-receipt-v1 | 可复用场景: Office/PDF 输入、研究附件、知识库导入 | 是否建议 shared: yes-after-update | 原因: 已有候选，需加入 coverage、network-used、output pointer 与 mixed-format fixtures
- [ ] 名称: install-upstream-anydoc-skill | 可复用场景: 文档读取 | 是否建议 shared: no | 原因: 与现有 Hermes 文件读取重叠，且上游 skill 未覆盖 shared 的隐私/终态/大输出治理

### Candidate Open Questions

- [ ] 问题: DeepSeek Harness 的 post-commit async persistence 在 crash 后如何证明最后一个 tool/result 已 durable，repair 是否覆盖所有外部 effect uncertainty？ | reason: gap | priority: high
- [ ] 问题: DSH audit 的 25 条记录中，哪些在默认 web/headless/sdk bundle 可达，哪些仅为 workspace classification 假阳性？ | reason: adaptation | priority: high
- [ ] 问题: anydoc 是否会采用 issue #144 的 partial output + inline missing-page marker，还是继续 all-or-nothing？ | reason: stale | priority: high
- [ ] 问题: XLSX embedded assets 缺失是否在后续 release 修复，并加入跨 binding fixture？ | reason: gap | priority: medium

### 不应自动落地

- 不安装或启动 DeepSeek Harness，不加载第三方 plugins，不运行模型、shell、MCP、E2B、Landlock 或网络服务。
- 不自动安装 anydoc Agent Skill，不处理私有文档，不启用 `--ocr hosted`，不把任何 API key 写入 shared。
- 不自动修改 Hermes 配置、模型、provider、cron、secret；不调用 OpenClaw。
- 不把 322 个定向测试外推为全仓/生产安全，也不把 anydoc npm smoke 外推为 Rust/fuzz 全绿。
- 不把 audit finding 直接定性为可利用漏洞，不把 npm audit 0 外推为 Cargo/native/hosted OCR 安全。
- 不把今日候选直接写入 curated active fact；完整原始证据留在 Hermes inbox/runtime，等待二轮治理。
