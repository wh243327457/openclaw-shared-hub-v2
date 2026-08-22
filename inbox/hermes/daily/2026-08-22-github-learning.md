# 2026-08-22 GitHub 热门项目每日学习报告

- 执行器：Hermes
- 研究窗口：2026-08-22 07:31:39–07:42:35（UTC+08:00）
- 发现源：GitHub Trending daily HTML；仓库元数据由 GitHub Repository API 重新核验
- 固定源码：`apache/maka@d62857a8357e9160926726a2a13096bc2dc2b91d`；`mattpocock/skills@5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-22/`
- 执行边界：OpenClaw 运行时不存在，本次没有调用、启动、模拟或写入 OpenClaw；未修改 Hermes 配置、模型、provider、auth、env、cron 或现有 skills

## 今日结论

**今日主线是“声明必须由执行层证据约束”：Maka 把 Agent 历史、工具副作用与恢复做成 canonical event、durable boundary 和 fail-closed continuation；mattpocock/skills 把工程流程做成小型可组合 skill、显式 invocation policy 与 registry conformance，但其 git guardrail 实测证明，写在 skill 里的安全承诺如果没有依赖 preflight、结构化解析和绕过 fixture，仍会静默失效。**

## 研究边界与真实验证

1. `curl` 真实抓取 `https://github.com/trending?since=daily`，得到 17 个仓库；HTML 为约 636 KiB，SHA-256 为 `c420493f7ff8226055a28c950283389bc3e4ddc7160f0c1cfae44a6533438472`。Trending 只用于发现，Stars、Forks、Language、License、updated/pushed 均重新读取 `GET /repos/{owner}/{repo}`。
2. 选择 `apache/maka` 是因为它是当日 Trending 中直接处理 Agent runtime event log、tool recovery 与 continuation authority 的本地优先工作区；选择 `mattpocock/skills` 是因为它把 36 个 skill 分层、注册、路由和 invocation policy 做成可检查的仓库结构。`obra/superpowers`、`affaan-m/ECC` 已于 2026-08-19 深读，今日不重复。
3. Maka 固定 commit 后运行 `npm ci --ignore-scripts`，安装 898 packages；使用 `--ignore-scripts` 是为了不触发根 `postinstall` 的 dependency patch 和 Electron 下载。宿主 Node `v22.14.0` 低于仓库要求 `>=22.19.0`，npm 明确报 `EBADENGINE`，因此所有失败均保留环境边界。
4. Maka `@maka/core` 完整测试真实返回 **588 pass / 0 fail**；`@maka/runtime` 构建成功，`runtime-commit-sink` 与 `runtime-resume` 两个定向文件真实返回 **28 pass / 0 fail**。
5. Maka `@maka/storage` 完整测试真实返回 **547 pass / 253 fail / 17 skip**，主要可见错误包含 `cannot start a transaction within a transaction`，另有 root 下只读目录 fixture 失真。由于 Node 版本不满足仓库 engine，不能把这批失败直接定性为上游回归，也不能声称 storage 通过；正确状态是 **blocked/incompatible environment，待用 Node >=22.19 复验**。
6. Maka lockfile 级 `npm audit --package-lock-only --omit=dev` 返回 **0 known vulnerabilities / 398 prod dependencies**。这只说明 npm 当前已知 advisory 未命中，不证明 native、Electron、release asset、模型/provider 或未知漏洞安全。公开 repository security advisories 为 0；Dependabot API 因权限不足返回 403。
7. skills 固定 commit 后 `npm ci --ignore-scripts` 安装 111 packages；`check-plugin-version` 通过。独立 checker 核验：promoted `engineering + productivity` 共 **25** 个，和 `.claude-plugin/plugin.json` 完全一致；全仓 **36** 个 `SKILL.md` 的 Claude frontmatter 与 `agents/openai.yaml` invocation policy 一致。
8. skills 的 `scripts/link-skills.sh` 在隔离 fake HOME 连跑两次：`~/.claude/skills` 与 `~/.agents/skills` 各 **36 symlinks、0 broken**。注意它是 maintainer dev script，且会链接 `misc`/`in-progress`，不同于插件只发布 25 个 promoted skills；不得当生产 installer 自动运行。
9. skills 的 git guardrail 做了真实 counterexample：本机没有 `jq` 时，危险的 `git push origin main` 返回 **0（fail open）**；注入最小 jq fixture 后直接 `git push` 返回 **2（blocked）**，但 `git -C /tmp push origin main` 仍返回 **0**。这与 open issue [#898](https://github.com/mattpocock/skills/issues/898) 完全一致，不是推测。
10. skills lockfile 级生产 audit 返回 **0 known vulnerabilities**；但 production count 仅 1，dev graph 为 111，真正风险主体是 skill prose、shell 模板、hook/installer 行为和远程自动更新，而不是 npm runtime dependencies。

## 项目速览

下表 Stars / Language / License 来自 2026-08-22 07:31–07:36（UTC+08:00）的 GitHub Repository API；Stars 是查询时快照，License 是 API 识别的仓库级 SPDX，不覆盖依赖、模型、数据和发布资产。

| 项目 | Stars | Language | License | 今日判断 |
|---|---:|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 275,641 | Shell | MIT | 高热；8 月 19 日已深读，今日不重复 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 241,775 | JavaScript | MIT | 高热；8 月 19 日已深读，今日不重复 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 229,404 | Shell | MIT | **深读：skill 分层、router、invocation 与 conformance** |
| [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 113,870 | Python | MIT | 多媒体生成，外部模型与内容风险较大 |
| [microsoft/TypeScript](https://github.com/microsoft/TypeScript) | 110,371 | Go | Apache-2.0 | 新实现迁移活跃，但今日与 Agent 闭环主线较远 |
| [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) | 71,763 | C++ | NOASSERTION | License 待核验，不迁移源码 |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 68,633 | TypeScript | MIT | 多 Agent meta-harness，体量与能力面超出今日预算 |
| [santifer/career-ops](https://github.com/santifer/career-ops) | 67,425 | JavaScript | MIT | Agent 工作流候选，但领域专用 |
| [TryGhost/Ghost](https://github.com/TryGhost/Ghost) | 54,870 | JavaScript | MIT | 大型发布平台，非今日 Agent runtime 主线 |
| [apache/maka](https://github.com/apache/maka) | 2,001 | TypeScript | Apache-2.0 | **深读：canonical runtime event 与 fail-closed resume** |

补充发现但未列入十项表：PostHog（38,279，Python，NOASSERTION）、modular（28,673，Mojo，NOASSERTION）、onnxruntime（21,430，C++，MIT）、OpenLogi（12,885，Rust，Apache-2.0）、OBLITERATUS（7,768，Python，AGPL-3.0）、cursor/plugins（4,388，TypeScript，API license 空）、google-timeline-visualizer（2,206，Kotlin，MIT）。这些项目只完成 API 速览，不作源码结论。

## 深读项目

### 项目 1：apache/maka

#### 基本信息与证据

- URL：https://github.com/apache/maka
- GitHub API：**2,001 Stars / 240 Forks / TypeScript / Apache-2.0**；`updated_at=2026-08-21T23:05:51Z`，`pushed_at=2026-08-21T20:07:03Z`，open issues/PR aggregate `282`，default branch `main`。
- 固定 commit：`d62857a8357e9160926726a2a13096bc2dc2b91d`。
- 最近 release：`v0.1.11`，发布于 `2026-08-18T14:22:55Z`；另有 CLI `cli-v0.1.0-beta.1` 同日发布。
- issue 证据：[#3279](https://github.com/apache/maka/issues/3279) 报告 Windows 从 0.1.9 升级到 0.1.11 并复用旧 profile 时，Runtime Host 间歇性 startup timeout；[#3409](https://github.com/apache/maka/issues/3409) 记录 hardcoded OpenCode Free model set 漂移，后已关闭，但本次未连接 provider 复验。
- README 明确：数据格式、CLI 和实验能力仍可变化；macOS arm64 是早期 public release，Windows unsigned preview，Linux desktop package 尚不支持。

#### 一句话判断：为什么值得学

Maka 值得学习的是将“对话看起来发生过”升级为“不可变 runtime facts 可以被严格编码、重放、封口和恢复”，并在任何副作用状态不确定时选择 park，而不是自动重试。

#### 解决的问题：替代了什么旧做法

1. 替代把 UI message list 当运行真相：model message、tool call、tool result、terminal fact 进入 Runtime Event Log，UI/context/recovery 都是 projection。
2. 替代把 context compaction 当历史删除：context pruning 只改变下一次 provider 输入，不修改 canonical history。
3. 替代工具调用后仅凭 stdout/exception 判断副作用：`operationId + canonicalArgsHash + prepared/outcome commit` 把调用身份与结果边界写入 host-owned ledger。
4. 替代 crash 后盲目续跑：resume 先核验 terminal、tool pairing、permission、workspace identity、tool catalog、background settlement、high-water 和 provider boundary；任一不确定就 park。
5. 替代多个前端各持一个 runtime：Desktop/TUI/CLI/Eval 都通过 Runtime Host；Eval 只拥有 experiment/cell/attempt 语义，不构造第二个 Maka runtime。

#### 架构 / 实现与数据流

```text
Desktop / TUI / CLI / Bot / Eval client
                   |
                   v
              Runtime Host                 # 唯一执行 authority
                   |
          SessionManager + AgentRun
          /          |            \
   Model adapter  Tool Runtime    Agent Graph
          \          |            /
             Runtime Event Log             # canonical immutable facts
                     |
    Context / Session / UI / Recovery projections

Tool side effect:
function_call -> durable dispatch(T1, operationId, args hash)
              -> implementation
              -> durable outcome(T2, function_response)
              -> provider projection / terminal fact

Resume:
immutable prefix + terminal/header agreement + host safety facts
              -> safe_replay / blocked
              -> fresh invocation/run/turn + durable continuation-start
              -> provider call（不重复原 user message）
```

`ARCHITECTURE.md` 与源码边界一致：`packages/core` 放纯 contract，`packages/storage` 放 SQLite authority，`packages/runtime` 放 SessionManager/tools/context/recovery，`packages/runtime-host` 是唯一 hosted authority；`packages/eval` 只管理 experiment/cell/immutable attempts。

#### Repo tree 摘要

固定 commit 共 **2,747 tracked files**；其中 core 231、storage 220、runtime 497、runtime-host 352、eval 62：

```text
apache/maka/
├── packages/core/          # RuntimeEvent、permission、session、capability 纯契约
├── packages/storage/       # runtime.sqlite、authority writers、backup、bounded reads
├── packages/runtime/       # model/tool runtime、resume、recovery、context、graph
├── packages/runtime-host/  # 唯一 hosted execution authority 与 client protocol
├── packages/eval/          # Experiment -> Cell -> immutable Attempt -> Result
├── packages/cli/           # TUI、maka run、eval route
├── packages/ui/            # conversation / tool activity / artifact projections
├── apps/desktop/           # Electron main/preload/renderer composition
├── docs/architecture/      # runtime/resume/graph/compaction contracts
├── scripts/                # build、release、Windows、computer-use verification
├── package.json            # npm workspaces、Node >=22.19、postinstall authority surface
├── package-lock.json       # 约 493 KiB lockfile
├── LICENSE / NOTICE        # Apache-2.0 与 attribution
└── README.md / ARCHITECTURE.md
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/core/src/canonical-runtime-event.ts` | canonical encoding | decode → normalize allowed undefined → stable strict JSON → parse/decode → deep-equal round trip；不无损则拒绝 |
| `packages/core/src/tool-args-identity.ts` | tool args identity | strict JSON canonicalization；拒绝 accessor、custom prototype、hole、BigInt、非有限数；维持 v1 hash bytes |
| `packages/core/src/runtime-event-store.ts` | event store contract | canonical/best-effort durability、sealed run、durable terminal、immutable prefix、continuation claim |
| `packages/runtime/src/runtime-commit-sink.ts` | T1/T2 commit identity | 用 invocation ID + provider tool call ID 生成 operation ID；prepared/outcome 分开 |
| `packages/runtime/src/runtime-resume.ts` | crash/resume planner | P0–P11 failpoints、tool recovery projection、safe/blocked、workspace/tool/permission gates |
| `packages/storage/src/runtime-event-persistence.ts` | SQLite composition | read/write persistence 分开；read-only surface 只暴露查询 |
| `packages/storage/src/runtime-event-authority.ts` | reserved authority | 普通 writer 禁止写 workspace facts 或占 reserved stream |
| `packages/storage/src/bounded-evidence.ts` | bounded reads | record 与 byte 双预算；超限返回 `limit_exceeded`，不投影为 complete |
| `packages/storage/src/write-queue.ts` | per-key serialization | 同 key promise chain；错误返回 caller，同时维持后续队列并自动清 Map |

#### ⭐ 源码精读

**代码块 1：`encodeCanonicalRuntimeEvent(value)` 要求 immutable fact 真正无损 round trip**  
来源：`packages/core/src/canonical-runtime-event.ts:20-33`

```typescript
export function encodeCanonicalRuntimeEvent(value: unknown): CanonicalRuntimeEventEncoding {
  const decoded = normalizeRuntimeEventEnvelope(decodeRuntimeEvent(value));
  let json: string;
  try {
    json = stableJsonStringify(decoded);
  } catch (cause) {
    throw new Error('RuntimeEvent is not losslessly serializable', { cause });
  }
  const event = decodeRuntimeEvent(JSON.parse(json));
  if (!nodeUtil.isDeepStrictEqual(decoded, event)) {
    throw new Error('RuntimeEvent is not losslessly serializable');
  }
  return { event, json };
}
```

逻辑摘要：schema valid 不等于 persistence safe。函数在写入前验证 strict JSON canonical form，再把实际 bytes 读回来重新 decode 和 deep compare。这样 `undefined`、getter、prototype、sparse array 或 `toJSON` 不能在写入时偷偷改语义。边界是 canonical encoding 只保证表示一致，不保证事件陈述真实，也不提供签名或外部防篡改。

**代码块 2：`buildToolOperationId(input)` 将工具 operation 绑定到 invocation 与 provider call identity**  
来源：`packages/runtime/src/runtime-commit-sink.ts:43-52`

```typescript
export function buildToolOperationId(input: ToolOperationIdInput): string {
  if (!input.invocationId || !input.providerToolCallId) {
    throw new Error('Tool operation identity requires invocationId and providerToolCallId');
  }
  const digest = createHash('sha256')
    .update(JSON.stringify([input.invocationId, input.providerToolCallId]))
    .digest('hex')
    .slice(0, 32);
  return `toolop_${digest}`;
}
```

逻辑摘要：operation ID 不从模型 prose、tool name 或 argument text 猜测，而从 host 已知 invocation + provider call tuple 派生；tuple JSON encoding 也避免简单字符串拼接歧义。参数内容另由 `canonicalToolArgsHash(toolName,args)` 绑定。边界是无密钥 SHA-256 是确定性 identity，不是授权、签名或不可伪造证明。

**代码块 3：`buildResumePlanFromRuntimeEvents(events, options)` 对不确定副作用 fail closed**  
来源：`packages/runtime/src/runtime-resume.ts:869-900`

```typescript
export function buildResumePlanFromRuntimeEvents(
  events: readonly RuntimeEvent[],
  options: BuildResumePlanOptions = {},
): ResumePlan {
  const recovery = resolveRuntimeRecovery(events);
  const operations = projectToolOperations(events, recovery);
  const sourceRuntimeEventHighWater = events.length;
  const diagnostics = collectResumeDiagnostics(events, operations, options, recovery);
  const rejectionReasons = deriveRejectionReasons(diagnostics);
  const requiresVerification =
    operations.some((operation) => operation.status === 'indeterminate') ||
    hasHiddenIndeterminateOperation(events, recovery);
  const disposition =
    rejectionReasons.length === 0 && !requiresVerification && !recovery.hasCorruption
      ? 'safe_replay'
      : 'blocked';
  return { disposition, operations, diagnostics, rejectionReasons,
           requiresVerification, sourceRuntimeEventHighWater,
           runtimeEvents: [...events],
           replayRuntimeEvents: buildResumeReplayRuntimeEvents(events) };
}
```

逻辑摘要：resume 不是“程序重启后再跑一次”。任何 unmatched result、tool name mismatch、corrupt semantic lane、indeterminate hidden nested operation 或 high-water mismatch 都进入 diagnostics/rejection；只有无拒绝、无 verification、无 corruption 才是 `safe_replay`。边界是 planner 仍依赖 host 提供 workspace identity、tool catalog 与 background settlement；planning 不是 lease，执行前必须重验。

**代码块 4：`buildSafeBoundaryContinuationPlan(events, facts)` 的最终 gate**  
来源：`packages/runtime/src/runtime-resume.ts:928-1175`（摘录）

```typescript
export function buildSafeBoundaryContinuationPlan(
  events: readonly RuntimeEvent[],
  facts: SafeBoundaryContinuationFacts,
): SafeBoundaryContinuationPlan {
  // ... validate ledger identity, terminal repair, permission and high-water ...
  if (facts.sourceWorkspaceIdentity !== facts.currentWorkspaceIdentity) {
    phaseOneRejectionReasons.push('workspace_identity_mismatch');
  }
  if (!facts.backgroundOperationsSettled) {
    phaseOneRejectionReasons.push('background_operation_pending');
  }
  // ... require historical tools and provider user/tool boundaries ...
  if (phaseOneRejectionReasons.length > 0 || !source) {
    return { disposition: 'park', rejectionReasons: phaseOneRejectionReasons,
             diagnostics: phaseOneDiagnostics };
  }
  return { disposition: 'continue', rejectionReasons: [],
           diagnostics: phaseOneDiagnostics, continuation: { /* fresh IDs + snapshot */ } };
}
```

逻辑摘要：cwd 位置变化只记 diagnostic，但 stable workspace identity 变化会 park；background operation 未 settled、历史工具缺失、pending permission、terminal/header 不一致或 provider boundary 非法也会 park。这个区分适合路径迁移：位置不是身份，身份也不能只靠路径。

#### 依赖分析与供应链风险

- 根要求 Node `>=22.19.0`、`npm@11.19.0`；本机 Node `22.14.0`/npm `10.9.2` 不满足，已真实触发 `EBADENGINE`。这正是 storage suite 不能外推的边界。
- 根 `postinstall` 会执行 `scripts/apply-dependency-patches.mjs` 和 Electron installer；今日使用 `--ignore-scripts`，没有下载 Electron binary，也没有应用仓库 patches。
- `@maka/runtime` 直接依赖包括多家 AI SDK、`@openai/agents-core`、Slack/Lark/WeCom SDK、`node-pty`、`undici`、`ws`、`ajv`、`zod`、`linkedom`、proxy packages。它不是“小依赖 core”；模型、网络、bot、PTY、MCP 都扩大 authority surface。
- `@maka/storage` 直接依赖很小（`@maka/core`、`fs-native-extensions`），但 native filesystem 与 Node experimental SQLite 让平台/runtime version 非常关键。
- lockfile audit：398 prod / 640 dev / 178 optional / total 1,045 dependency entries，0 known npm advisory。0 不等于无漏洞；native 二进制、Electron、GitHub release、provider 数据、patch 文件与第三方 notices 必须独立审。
- API/root manifest/LICENSE 均为 Apache-2.0；第三方依赖仍按各自 license。不要把 Maka 源码整段复制进 shared skill。

#### README / docs / release / issues / source / 运行交叉核验

- README 的“Log is the Runtime”与 `RuntimeEventStore`、strict canonical encoder、SQLite persistence 和 resume projection 对齐。
- `runtime-resume-phase1-safe-boundary-contract.md` 说 missing/contradictory fact 应 park；`buildSafeBoundaryContinuationPlan` 源码和 28 个定向 tests 支持该结论。
- 定向 tests 真正覆盖 operation identity、P0–P11 catalog、unmatched result、hidden nested tool、workspace identity、background pending、tool catalog mismatch 等；但没有运行完整 runtime suite、Runtime Host、Desktop、real provider 或 Windows upgrade。
- #3279 是上游 Windows upgrade lifecycle 的真实报告，本机 WSL 没有复现；不能声称 0.1.11 在本机命中或已修复。
- #3409 说明静态 provider model pin 会漂移；issue 已关闭，但本次未连接 OpenCode Free，故“当前 E2E 已恢复”待核验。

#### 可复用经验

- 当 Agent 历史将用于重放、恢复或审计时，应优先使用 strict canonical event + immutable prefix + high-water，而不是 UI transcript，因为 presentation、context compaction 和 durable fact 是不同层；边界是 canonical bytes 仍不证明事实真实。
- 当工具可能已产生副作用但结果未提交时，应优先 park 并要求 read-only reconciliation，不应自动 retry，因为重试可能重复支付、写入或删除；边界是每个工具仍需声明自己的 recovery mode。
- 当 workspace 路径可以搬迁时，应优先把 path 当 location diagnostic，把稳定 workspace identity 当恢复 gate，因为同一项目可换路径、同一路径也可换内容；边界是 stable identity 不能替代当前 authorization。
- 当一个运行面被 Desktop/TUI/CLI/Eval 共同使用时，应优先保留唯一执行 authority 和多个 projection/client，因为多 runtime 会产生权限、session 与 ledger 分叉；边界是单一 authority 也需要高可用与 protocol versioning。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/canonical-tool-resume-envelope/` 做纯 Python/JSON 离线 fixture：

1. 定义 `Event{scope,id,seq,kind,operation_id,args_hash,terminal}` 与 `Resume{safe|park,reasons,coverage}`。
2. 覆盖 canonical key reorder、`undefined` 等价模拟、duplicate event ID、call 无 result、result tool mismatch、terminal 后 late event、workspace path 变但 ID 相同、workspace ID 变化八种输入。
3. 只有 event prefix 完整、tool pair 一致、terminal 在末尾、identity 匹配时输出 `safe`；其余必须 `park`，并有 stable reason。
4. 不接 provider、不执行真实 shell effect、不写 Hermes 配置或 curated。

#### 风险边界

- **License**：Apache-2.0；第三方依赖/notices/patch/native/release asset 分别审查。
- **维护活跃度**：pushed 2026-08-21，v0.1.11 于 2026-08-18 发布，活跃；同时 README 明确 data formats/CLI/experimental capabilities 可变化。
- **安全**：README 明确 `credential-vault.json` 是 OS account boundary 下的本地明文（目录 0700、文件 0600）；这不是加密 secret store。Renderer 不拿 plaintext credential，但 OS account compromise 仍可读取。
- **恢复**：Phase 3 对 indeterminate tool effects 尚未完全实现；ambiguous outcome 会 park。不要把 safe-boundary planner 当 exactly-once effect guarantee。
- **升级**：旧 JSONL/history 与旧 safeStorage credential 不自动迁移；README 明确可能出现历史空 thread、需要重新认证。#3279 又显示 Windows profile upgrade 有 startup 风险。
- **测试**：core 588 pass、runtime focused 28 pass；storage 253 fail，且 Node engine 不兼容。不得声称全仓通过。
- **不适用**：分布式 fencing、多租户强隔离、外部备份强删除、SLA 级恢复、未知 tool effect 自动重试。
- **不能自动执行**：不安装 Maka、不启动 Runtime Host、不配置 provider/token，不运行 Electron postinstall，不迁移现有 Hermes/shared 数据。

#### ⭐ Skill 升格判断

**需二次验证。** 可候选化的是窄契约 `canonical event -> tool boundary -> park/reconcile -> fresh continuation identity`，不是 Maka 产品或 TypeScript 实现。先与 shared 现有 verification-first、subagent 四状态、self-reflection、shared-memory-bridge 和 completion/receipt 候选去重；storage suite 还必须在 Node >=22.19 环境复验。今日不创建 shared skill，不写 curated active fact。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/canonical-tool-resume-envelope/{schema.json,fixtures/,checker.py,test_contract.py,README.md}`。
2. Hermes runtime 接点：未来只在 host-owned tool executor/receipt 层引入 `operation_id + args_hash + effect status + terminal`；不要从模型 prose 生成 effect receipt。
3. GitHub learning 接点：给 orchestrator status 增加可解释的 `expected_artifact/hash/coverage/reasons`，audit score 仍不能替代 artifact readback。
4. shared hub 接点：raw report 继续进 `inbox/hermes/daily/`，fixture/log 进 `runtime/hermes/`；只有经过评分、证据、去重、脱敏和审查的方法论才进入 `curated/memory/facts/` 或现有 shared skill。
5. 路径迁移接点：复用 `scripts/resolve_shared_root.py`，将 shared root path 与 shared hub identity/revision 分开；不得硬编码当前宿主绝对路径到新 script/skill/prefill。
6. OpenClaw：当前不存在，不实施 adapter；未来只消费 agent-neutral receipt schema，独立验证其真实 tool/session authority。

---

### 项目 2：mattpocock/skills

#### 基本信息与证据

- URL：https://github.com/mattpocock/skills
- GitHub API：**229,404 Stars / 19,605 Forks / Shell / MIT**；`updated_at=2026-08-21T23:31:51Z`，`pushed_at=2026-08-21T10:56:48Z`，open issues/PR aggregate `374`。
- 固定 commit：`5b15a47f2d7150f545fbcacbfe381787fc0230dc`。
- 最近 release：`v1.2.3`，发布于 `2026-08-06T14:05:28Z`。
- issue 证据：[#898](https://github.com/mattpocock/skills/issues/898) 报告 git guardrail 缺 jq 时 fail open，且 `git -C ... push` 等合法 spelling 绕过；本机 fixture 真实复现。[#924](https://github.com/mattpocock/skills/issues/924) 报告 `/to-tickets` 可在大 PRD 分解中孤立/遗漏 invariant，说明 tracer ticket 仍需 coverage matrix。
- 仓库自身 `AGENTS.md` 规定 promoted buckets 必须同时出现在 README、docs 和 plugin manifest；misc/in-progress/deprecated 不得进入 plugin。

#### 一句话判断：为什么值得学

该仓库最值得学的是把 skill 当成“可分层、可路由、可声明 invocation、可做 registry conformance 的工程资产”；最值得警惕的是，prose contract 和 regex hook 不是安全 enforcement，且 skill 分解本身可能丢失全局需求覆盖。

#### 解决的问题：替代了什么旧做法

1. 替代一个超大“万能开发 prompt”：engineering、productivity、misc、in-progress 分桶，单 skill 小而可组合。
2. 替代模型自由猜工作流：`ask-matt` 给 idea → grill → spec → tickets → implement → TDD/review 的显式路由与 phase boundary。
3. 替代所有 skill 都能被模型自动触发：user-invoked 与 model-invoked 双 harness policy 对齐。
4. 替代只按 layer 拆任务：`to-tickets` 要求 end-to-end tracer bullet、blocking edges 与 context-window size。
5. 替代把 code review 合成一个总分：standards 与 spec 两轴平行 review，不互相掩盖。
6. 但它没有自动保证安全 hook 真正 enforcement，也没有自动证明 spec 的每个 requirement 被某 ticket 覆盖；#898/#924 是明确边界。

#### 架构 / 实现与数据流

```text
skills/
  engineering + productivity  -> promoted registry -> plugin.json -> managed bundle
  misc + in-progress          -> visible source/dev link, not plugin publication
  deprecated                  -> excluded

Human request
  -> user-invoked router/orchestrator（ask-matt / to-tickets / implement）
  -> model-invoked discipline（research / tdd / code-review / domain-modeling）
  -> repo artifacts（CONTEXT.md / ADR / spec / ticket / review）

Conformance
  package.json version -> sync-plugin-version.mjs -> plugin.json
  promoted SKILL dirs  -> README/docs/plugin lists
  SKILL frontmatter    <-> agents/openai.yaml invocation policy

Local maintainer link
  repo skills/*/*/SKILL.md -> ~/.claude/skills + ~/.agents/skills symlinks
```

重要分层：plugin 只发布 25 个 promoted skills；maintainer `link-skills.sh` 会链接 36 个非 deprecated skills，包括 misc/in-progress。这不是同一 distribution policy，必须在报告和安装计划中区分。

#### Repo tree 摘要

固定 commit 共 **162 tracked files**，36 个 `SKILL.md`：engineering 18、productivity 7、misc 4、in-progress 7、deprecated 0。

```text
mattpocock/skills/
├── skills/
│   ├── engineering/       # 18：spec/tickets/TDD/review/research/router
│   ├── productivity/      # 7：grilling/handoff/teach/writing
│   ├── misc/              # 4：保留但不 promoted，含 git guardrail
│   ├── in-progress/       # 7：公开 beta，不进 plugin
│   └── deprecated/        # 已下线能力说明
├── docs/                  # promoted skill 的 human-facing pages
├── .claude-plugin/
│   ├── plugin.json        # 25 个 promoted skills registry
│   └── marketplace.json
├── .agents/
│   ├── invocation.md      # user/model invocation 双 harness 契约
│   ├── writing-docs.md
│   └── adr/               # distribution 决策
├── scripts/
│   ├── link-skills.sh     # maintainer fake/local symlink installer
│   ├── sync-plugin-version.mjs
│   └── list-skills.sh
├── package.json / package-lock.json
├── AGENTS.md / CONTEXT.md / CHANGELOG.md
└── LICENSE                # MIT
```

#### 关键源码/契约文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `skills/engineering/ask-matt/SKILL.md` | flow router | idea→ship、on-ramps、phase boundary、user/model invoked 关系 |
| `skills/engineering/to-tickets/SKILL.md` | work graph | tracer slices、blocking edges、expand-contract、tracker projection |
| `skills/engineering/code-review/SKILL.md` | two-axis review | pin fixed point；standards/spec 并行且不 rerank |
| `skills/engineering/research/SKILL.md` | primary-source research | background agent、primary sources、single cited Markdown artifact |
| `.agents/invocation.md` | cross-harness invocation | Claude frontmatter 与 OpenAI YAML 必须同向；user skill 不可被另一个 skill 隐式调用 |
| `.claude-plugin/plugin.json` | promoted registry | 当前 25 个 engineering/productivity skills |
| `scripts/sync-plugin-version.mjs` | manifest conformance | package/plugin version readback；`--check` drift 时 exit 1 |
| `scripts/link-skills.sh` | local maintainer linking | 两个 destination、symlink recursion guard、idempotent `ln -sfn` |
| `skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh` | regex hook | jq 提取命令并按 pattern 拦截；实测存在 fail-open 与 spelling bypass |
| `skills/engineering/wizard/template.sh` | human effect adapter | browser/manual step、env/GitHub secret 写入；高权且必须人工触发与审查 |

#### ⭐ 源码精读

**代码块 1：`sync-plugin-version.mjs` 把版本 drift 变成 deterministic check**  
来源：`scripts/sync-plugin-version.mjs:10-27`

```javascript
const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const pluginPath = join(repo, ".claude-plugin", "plugin.json");
const { version } = JSON.parse(readFileSync(join(repo, "package.json"), "utf8"));
const source = readFileSync(pluginPath, "utf8");
const plugin = JSON.parse(source);

if (plugin.version === version) process.exit(0);
if (process.argv.includes("--check")) {
  console.error(`plugin.json version is ${plugin.version}, package.json is ${version}.`);
  process.exit(1);
}
```

逻辑摘要：一个版本字段做 source，另一个 manifest 是 projection；CI 用 `--check` 不修改文件，release/version 命令才更新。今日真实返回 `plugin.json version is 1.2.3 (already in sync)`。边界是版本一致只证明字段同步，不证明 skill registry、README、docs 或行为一致；所以还需要独立 registry checker。

**代码块 2：`link-skills.sh` 的 collection + recursion boundary**  
来源：`scripts/link-skills.sh:15-39,44-55`

```bash
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/deprecated/*' -print0)

if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST")"
  case "$resolved" in "$REPO"|"$REPO"/*) exit 1 ;; esac
fi
ln -sfn "$src" "$target"
```

逻辑摘要：使用 NUL-delimited find 避免空格路径问题；若整个 destination 是指回 repo 的 symlink，则拒绝，避免在 source tree 里反向创建 per-skill links。fake HOME 连跑两次得到两个 destination 各 36 links、0 broken。边界：如果 `target` 已存在且不是 symlink，源码会 `rm -rf "$target"`；它也链接 misc/in-progress。因此只能视为 maintainer dev script，不能无人值守写真实 Hermes profile。

**代码块 3：`write_env()` 是幂等 upsert，但仍是明文 secret effect**  
来源：`skills/engineering/wizard/template.sh:130-139`

```bash
write_env() {
  local key="$1" value="$2" tmp
  touch "$ENV_FILE"
  tmp=$(mktemp)
  grep -vE "^${key}=" "$ENV_FILE" > "$tmp" || true
  printf '%s=%s\n' "$key" "$value" >> "$tmp"
  mv "$tmp" "$ENV_FILE"
  WRITTEN_ENV+=("$key")
  printf '  %s✓ wrote%s %s → %s\n' "$GREEN" "$RESET" "$key" "$ENV_FILE"
}
```

逻辑摘要：重跑会替换同 key 而不是追加重复行，并用 temp + mv 发布。但它没有检查 symlink、owner/mode、ancestor、value newline 或 ENV_FILE containment，模板示例还会把 `STRIPE_SECRET_KEY` 写入 `.env`。这必须由用户主动触发并在受控目录执行，不能由 cron 或 shared skill 自动运行。

**代码块 4：`set_secret()` 将 GitHub mutation 限制在 gh 已认证时，但没有 target receipt**  
来源：`skills/engineering/wizard/template.sh:143-154`

```bash
set_secret() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if printf '%s' "$value" | gh secret set "$name" >/dev/null 2>&1; then
      WRITTEN_SECRET+=("$name")
      return
    fi
  fi
  SKIPPED+=("GitHub secret $name (set it manually: gh secret set $name)")
  warn "skipped GitHub secret $name: gh not ready; set it later"
}
```

逻辑摘要：无 gh/未认证/写失败时降级为 skipped，不伪报完成；secret 通过 stdin 传入而非命令行参数。边界是没有绑定 repo/owner/ref，也没有 readback 验证目标，仅将 command exit 当成功；当前 scheduled Hermes 更不能运行这种 human-only effect。

**代码块 5：git guardrail 的 fail-open 实现与真实 counterexample**  
来源：`skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh:3-23`

```bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')
DANGEROUS_PATTERNS=("git push" "git reset --hard" "git clean -fd" ...)
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    exit 2
  fi
done
exit 0
```

真实结果：

```text
without jq:  git push origin main          -> rc 0 (allowed; stderr jq not found)
with jq:     git push origin main          -> rc 2 (blocked)
with jq:     git -C /tmp push origin main  -> rc 0 (allowed)
```

逻辑摘要：脚本没有 `set -e`，也没有检查 jq/parse status；依赖失败后 `COMMAND` 为空并最终 exit 0。字符串 regex 也不能正确解析 git global options/subcommands。该 hook 位于 `misc`，不在 promoted plugin registry；#898 当前 open。它不能作为 Hermes 的 hard permission gate。

#### 依赖分析与供应链风险

- `package.json` 无 runtime dependencies；dev dependencies 只有 `@changesets/changelog-github` 与 `@changesets/cli`，package manager `npm@10.9.4`。
- lockfile audit：1 prod / 111 dev / total 111，0 known advisories。依赖面较小，但这几乎不衡量 skill 仓库的真实风险。
- 真正供应链入口：Claude managed plugin 自动更新、`npx skills@latest` installer、symlink dev installer、shell templates、GitHub `gh` mutations、第三方 skill prose 对模型行为的影响。
- README 明确 managed plugin 与 editable copy 二选一；同时安装会产生重复 skill。shared hub 也应坚持唯一 owner/source，不应同时链接和复制同名能力。
- 根 License/API/package manifest 均为 MIT；复制 skill 原文仍要保留许可/版权并做 prompt authority review。今日不复制。

#### README / docs / release / issues / source / 运行交叉核验

- README 说 skills 小型、可组合；tree 中 36 个独立 skill 与 router/primitive 分离支持该结论。
- `AGENTS.md` 规定 promoted set = README + plugin；本机 checker 得到 actual 25 = plugin 25，且 non-promoted leak 0。
- `.agents/invocation.md` 规定 Claude frontmatter 与 OpenAI YAML 同步；本机 checker 遍历 36 个 skill，全部 PASS。
- README 把 plugin 和 editable installer 定义为二选一；本次没有运行远程 `npx skills@latest`，也没有安装到真实 HOME。
- #898 的两个问题本机都复现；不能因 skill 名叫 guardrail 就把它当 hard gate。
- #924 是上游用户报告，本次未复现 85-story PRD；但现有 `to-tickets` 源码只要求 breakdown/edges/approval，没有 machine-checkable requirement→ticket coverage matrix，机制 gap 与 issue 一致。

#### 可复用经验

- 当 skill 数量增长时，应优先把 source bucket、promotion registry、human docs、invocation policy 做成可执行 conformance，而不是依靠 README 人工同步；边界是 registry 一致仍不证明行为正确。
- 当一个工作流同时包含 user-only orchestrator 与 model-invoked primitives 时，应优先把 invocation authority 写进每个 harness 的原生 metadata 并做双向 checker，因为 prose 中写“只能用户调用”不等于 loader enforcement；边界是 host loader 仍需 acceptance test。
- 当 spec 被拆成多张 tracer tickets 时，应优先维护 requirement→ticket→acceptance→verification coverage matrix，因为每张 ticket 自洽仍可能遗漏全局 invariant；边界是 coverage 完整也不证明实现正确。
- 当安全 hook 依赖外部 parser 或 command spelling 时，应优先 prerequisite fail-closed + structured argv parser + adversarial corpus，而不是 raw substring regex，因为缺依赖和合法变体都会绕过；边界是 parser 仍不能替代 OS sandbox/host authorization。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/skill-registry-coverage-conformance/` 做离线 checker：

1. 输入 synthetic skill tree、manifest、invocation metadata、requirements/tickets JSON。
2. 检查 promoted skill 是否同时出现在 manifest/docs/index；user/model invocation 是否跨 adapter 一致；duplicate owner/source 是否出现。
3. 检查每个 requirement 至少映射一 ticket，每 ticket 有 blocker closure 与 acceptance；孤立 requirement 输出 `partial`，不能 completed。
4. 加 guardrail corpus：missing parser、`git push`、`git -C /tmp push`、`command git push`、quoted/chained command；未知 parse 必须 `blocked`，不是 allowed。
5. 只使用 fake tree/fake HOME，不安装上游 skill、不执行 git mutation、不写真实 `~/.hermes`。

#### 风险边界

- **License**：MIT；shell/template/引用内容仍需逐文件与第三方 attribution 审查。
- **维护活跃度**：pushed 2026-08-21，最近 release 2026-08-06，活跃；374 open issue/PR aggregate 也表示 behavior 仍在快速调整。
- **安全**：skills 能改变 Agent 行为；wizard 可写 `.env` 和 GitHub secret，link script 可删除同名非 symlink 目录，git guardrail 实测 fail open。不能把 model guidance 当 host security boundary。
- **正确性**：router/flow 是经验性 policy；“smart zone ~150k”是项目文本中的 heuristic，本次未独立核验，不应成为硬 runtime 阈值。
- **分解风险**：#924 表明 ticket graph 可完整执行但遗漏 PRD invariant；需要 coverage matrix 和最终全局 spec review。
- **发布风险**：managed plugin 自动更新与 editable copy 语义不同；双装会重复；symlink 跟随 `git pull` 变化，缺 immutable pin。
- **测试边界**：registry/invocation/link/version/audit fixture 通过；没有运行 Claude/Codex/Hermes 真正 loader acceptance，也没有运行全部 skill E2E。
- **不适用**：把 regex hook 当 shell sandbox；在无人值守 cron 中执行 wizard；把所有 36 个 skill 一次性装入 shared；跨 agent 无 adapter 测试直接共享。
- **不能自动执行**：不运行 `npx skills@latest`、不安装 plugin、不修改真实 HOME/skills/config、不写 `.env`/GitHub secrets。

#### ⭐ Skill 升格判断

**需二次验证。** 可候选化的是 `skill registry + invocation + requirement coverage conformance`，不是整套 mattpocock skills。shared hub 已有 shared-skill governance、manifest、future-agent-readable 和 local/shared scope 规则，应优先扩展现有治理/checker，而不是新增平行 skill。git guardrail 当前为 **暂不沉淀**：已证实 fail open，不可迁移。今日不创建 shared skill，不复制上游 SKILL.md。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/skill-registry-coverage-conformance/{fixtures/,checker.py,test_checker.py,schema.json}`。
2. shared skill registry：对 `capabilities/manifests/shared-skills.yaml` 与 `capabilities/skills/*/SKILL.md` 做双向核验；继续要求 `scope`、`reference_policy`、`future_agent_readable`。
3. invocation adapter：agent-neutral contract 只声明 `user_only|model_allowed`；Hermes/OpenClaw/future agent 各自 adapter 映射并跑 loader fixture。当前 OpenClaw 不存在，不实现其 adapter。
4. GitHub learning：在报告审计中加入 requirement coverage，不再只检测关键词；每个“深读项目”要求 tree/files/code blocks/license/risk/skill/landing 都有对应 evidence pointer。
5. 安装边界：任何第三方 skill 先落 `runtime/hermes/` fake-home inventory，固定 commit/hash，做 conflict/owner/uninstall plan；用户批准后才可能写 `~/.hermes/skills/`。
6. shared 晋升：若 POC 通过，优先更新现有 `docs/shared-skill-governance.md` 或相关 governance skill；完整目录、manifest、prefill/curated 影响仍须审查。

## 经验沉淀

1. 当 Agent 的执行历史将用于恢复或审计时，应优先构造 strict canonical facts、immutable high-water 与 terminal seal，因为 UI transcript、context projection 和 durable truth 不同；边界是 canonicalization 不提供真实性或授权。
2. 当工具结果在 crash 时可能不确定，应优先输出 `park/needs_verification` 并使用 read-only reconciliation，因为自动重试会把“不知道是否发生”放大为重复副作用；边界是 recovery mode 必须逐工具声明。
3. 当项目或 shared root 可以迁移路径时，应优先分开 stable identity 与 current location，并在最终 effect/resume 点重验，因为路径相同不代表对象相同、对象相同也可换路径；边界是 identity 仍不能替代权限。
4. 当 skill 需要跨 harness 共享时，应优先拆成 agent-neutral contract、deterministic conformance checker 与 host adapter，因为 invocation metadata、tool surface 和权限语义不同；边界是 adapter 声明必须由真实 loader acceptance test 证明。
5. 当一个大 spec 被拆成 ticket DAG 时，应优先维护 requirement→ticket→acceptance→verification coverage，因为 blockers-first 全部完成仍可能漏掉全局 invariant；边界是 100% mapping 仍需最终行为 E2E。
6. 当 guardrail 依赖 jq、regex 或 shell command string 时，应优先缺依赖 fail-closed、结构化解析和 adversarial spelling corpus，因为 raw substring 在普通合法语法下就可绕过；边界是任何 parser 都不能替代 host/OS sandbox。
7. 当安装脚本会链接、覆盖或删除 skill 目录时，应优先用 fake HOME、dry-run inventory、immutable source、owner/conflict/uninstall receipt，因为幂等重跑不代表不会覆盖用户文件；边界是 symlink 随 upstream checkout 变化。
8. 当测试环境不满足上游 engine 时，应优先报告真实 pass/fail 与 `blocked/incompatible`，不应把失败定性为上游 regression，也不应拿部分绿色外推全仓；边界是复验必须固定 commit、engine、lockfile 和命令。

### 今日实验设计

- 名称：`runtime/hermes/github-learning-poc/canonical-skill-effect-contract/`
- 范围：把 Maka 的 `canonical/terminal/park` 与 skills 的 `registry/invocation/coverage` 合并成 synthetic fixture。
- 成功条件：每个输入有 immutable hash、scope、coverage、terminal；missing dependency、missing requirement mapping、indeterminate tool、manifest drift 都必须非 completed。
- 安全：不连接 provider/MCP/browser，不执行真实 git/secret effect，不安装 skill，不修改 config/model/provider/auth/env/cron，不写 curated。

## 明日继续

1. 在 Node `>=22.19.0` 的隔离环境复跑 Maka `@maka/storage`，记录 engine、SQLite version、root/non-root 与完整 summary；在此之前保持 storage lane blocked。
2. 跟踪 Maka #3279，核验是否形成旧 profile startup inventory、bounded timeout evidence 和升级回滚/repair receipt；不在当前 WSL 执行 Windows installer。
3. 跟踪 skills #898，若修复则固定新 commit，跑 missing jq、invalid JSON、`git -C`、`command git`、chained/quoted corpus；unknown parse 必须 fail closed。
4. 跟踪 skills #924，设计最小 requirement coverage fixture，验证一个“被某 ticket 明确排除但没有后继 ticket”的 invariant 能让 overall 变 partial。
5. 将两个 POC 候选与已有 verification-first、completion/receipt、shared-skill-governance、path-portability、self-reflection 去重，再决定更新已有 skill 还是仅保留 Hermes runtime 工具。

## 候选反哺

### Candidate Facts

- [ ] topic: Agent continuation 必须由 immutable event prefix、tool-pair completeness、terminal/header agreement 与 host safety facts共同 gate | evidence: Maka commit `d62857a...` 的 `runtime-resume.ts`、Phase 1 contract、28 pass 定向 tests | 建议: create candidate after existing verification fact dedup | 安全级别: medium
- [ ] topic: strict schema validation 之外还需要 lossless persistence round-trip | evidence: Maka `canonical-runtime-event.ts`、core 588 pass | 建议: update verification-first candidate | 安全级别: low
- [ ] topic: skill registry/invocation metadata 可以做双向 conformance，但不证明运行时安全 | evidence: skills commit `5b15a47...`，25 registry/36 invocation checker PASS，#898 counterexample | 建议: create candidate after governance dedup | 安全级别: low
- [ ] topic: ticket DAG 需要 requirement coverage，局部 ticket review 不能证明全局 spec 完整 | evidence: skills #924 + `to-tickets/SKILL.md` 当前无 machine-checkable coverage matrix | 建议: create as open candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: canonical-tool-resume-envelope | 可复用场景: Hermes tool execution、cron completion、memory mirror、future agent recovery | 是否建议 shared: yes after fixture | 原因: 跨 Agent 横切，但先与 verification/completion/subagent 四状态去重
- [ ] 名称: skill-registry-coverage-conformance | 可复用场景: shared skill manifest、Hermes/local adapter、future-agent 接入、GitHub-learning audit | 是否建议 shared: yes after fake-tree tests | 原因: shared hub 已有 manifest/governance，可优先扩展而不是新建平行系统
- [ ] 名称: regex-git-guardrail | 可复用场景: shell safety | 是否建议 shared: no | 原因: missing jq 与 `git -C` 已真实绕过；prose/regex hook 不能作 hard gate
- [ ] 名称: Maka runtime integration | 可复用场景: 本地 Agent workspace | 是否建议 shared: no | 原因: 与 Hermes runtime/shared hub 重叠，storage 测试 blocked，产品/data migration/credential boundary 不适合直接接入

### Candidate Open Questions

- [ ] 问题: Hermes 当前 tool executor 是否已有 operation ID、canonical args identity、indeterminate terminal 与 resume park contract？ | reason: gap/duplication | priority: high
- [ ] 问题: GitHub learning audit 如何记录 scorer version、coverage 与 artifact hash，而不把关键词命中当质量？ | reason: adaptation | priority: high
- [ ] 问题: shared skill manifest 与各 host 的 user-only/model-allowed invocation 应如何表达和做真实 loader acceptance？ | reason: adaptation | priority: high
- [ ] 问题: ticket/spec coverage 是否应成为 autonomous-learning/reflection 的硬 gate，怎样避免纯数量覆盖骗分？ | reason: adaptation | priority: high
- [ ] 问题: Maka storage suite 在受支持 Node 和非 root 环境下是否全绿？ | reason: blocked environment | priority: medium
- [ ] 问题: Maka #3279 的旧 profile startup failure 是锁、schema migration、credential 还是 runtime-host lifecycle？ | reason: gap | priority: medium

### 不应自动落地

- 不自动修改 Hermes/OpenClaw 配置、model、provider、auth、env、cron、skills；当前 OpenClaw 不存在且未调用。
- 不把 Candidate Facts 直接写入 `curated/memory/`，不创建或修改 shared active skill；候选需评分、证据、去重、脱敏与人工/总控审查。
- 不安装 Maka、mattpocock plugin 或 `npx skills@latest`；不运行第三方 postinstall、Electron、provider 或 Runtime Host。
- 不执行 wizard 的 `.env`/GitHub secret mutation，不把 regex git guardrail 当安全 enforcement。
- 不把 npm audit 0 外推为 native、Electron、release、provider、模型、shell template 或未知漏洞安全。
- 不把 Maka core/focused tests 外推为全仓通过；storage 253 failures 保持 blocked/incompatible，待受支持 Node 复验。
- 不复制上游 TypeScript、Shell 或 SKILL.md 原文到 shared；只候选化机制与本地重写契约。

## 研究证据索引

- Trending：`runtime/hermes/github-hot-project-learning/evidence/2026-08-22/trending.html` 与 `trending.sha256`。
- API metadata：`evidence/2026-08-22/api/*.json` 与 `repo-metadata.jsonl`。
- release/issues：`evidence/2026-08-22/releases/`、`issues/`；Maka #3279/#3409，skills #898/#924 有独立 JSON。
- 固定源码：`runtime/hermes/github-hot-project-learning/repos/2026-08-22/apache__maka/`、`.../mattpocock__skills/`。
- Maka tests：`apache__maka-core-test.log`、`apache__maka-storage-test.log`、`apache__maka-runtime-focused-tests.log`、`apache__maka-test-rc.txt`。
- skills fixtures：`mattpocock__skills-registry-check.log`、`mattpocock__skills-version-check.log`、`mattpocock__skills-link-fake-home-check.log`、`guardrail-fixture-rc.txt`、`guardrail-with-jq-rc.txt`。
- audits：`apache__maka-npm-audit-prod.json`、`mattpocock__skills-npm-audit-prod.json`。
- 所有无法由上述运行确认的内容均标为“待核验”或 blocked，尤其是 Maka storage 在受支持 Node 的结果、Windows upgrade、真实 provider、完整 loader E2E 与 OpenClaw adapter。
