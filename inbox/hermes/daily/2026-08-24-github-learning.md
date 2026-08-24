# 2026-08-24 GitHub 热门项目每日学习报告

- 执行器：Hermes（本次没有调用、启动或模拟 OpenClaw）
- 研究日期：2026-08-24
- 共享根解析：先运行 `python3 scripts/resolve_shared_root.py`，真实返回 `/home/vany/agent/shared`
- GitHub 元数据最终核验时间：`2026-08-24T07:41:54+08:00`
- 候选来源：GitHub Search API（`created:>2026-07-01` 按 Stars 降序）与 GitHub Trending daily 页面
- 深读固定版本：`deepseek-ai/deepseek-harness@b150a551b8d465e31e418e1b2eaf5e79bbb7d28e`（tag `dsh-v0.1.1-rc.2`）；`firecrawl/anydoc@bf3d33e61731580d1ee1c6a85e56093d715a21a6`（tag `v0.2.3`）
- 证据边界：Stars、Forks、Language、License、更新时间来自本次 `gh api repos/{owner}/{repo}`；README/docs/release/issues/Actions 来自 GitHub API 或固定提交的浅克隆；代码结论来自固定提交文件；运行结论只记录本机真实命令输出。

## 今日结论

**今日学习主线是“把不可信输入收敛到可替换但不可绕过的确定性边界”：DeepSeek Harness 用 scoped plugin composition、append-only session log 和 pre/guard/execute/post/result 工具流水线把 Agent 扩展性与执行约束分开；anydoc 用 content-based detection、统一 Document model、固定资源上限和 typed errors 把多格式文档摄取收敛到一个本地转换边界。对 Hermes/shared hub 最值得反哺的是窄契约与验收 fixture，而不是直接引入另一套 Agent runtime 或自动安装第三方 Skill。**

## 研究范围与真实验证摘要

1. GitHub Search API 返回的新近高 Stars 候选包括 `deepseek-ai/deepseek-harness`、`xai-org/grok-build`、`firecrawl/anydoc`、`andrewyng/openworker`、`yc-software/qm` 等；GitHub Trending daily 页面还真实返回 `openai/codex`、`mattpocock/skills`、`basecamp/omarchy`、`NousResearch/hermes-agent` 等。本日报不把 Trending 的 “stars today” 当仓库总 Stars，项目速览的总 Stars 统一使用 repository API。
2. DeepSeek Harness API 最终快照为 **187,904 Stars / 20,909 Forks / TypeScript / MIT**，`pushed_at=2026-08-21T12:35:08Z`；最新 release 是 prerelease `dsh-v0.1.1-rc.2`，发布时间 `2026-08-21T12:35:08Z`。README 明确标注 developer preview 和 compatibility-breaking changes。
3. DeepSeek Harness 本机使用 `npx -y pnpm@11.7.0 install --frozen-lockfile --ignore-scripts` 完成依赖解析；因本机 Node `v22.14.0` 低于仓库 engine `^22.19.0 || >=24.0.0`，pnpm 给出 unsupported engine 警告。随后定向运行 6 个测试文件，真实结果为 **6 files passed / 208 tests passed / 0 failed**。这不能外推为全仓、真实 provider、PTY、sandbox、MCP、Web UI 或 E2E 通过。
4. DeepSeek Harness 的 `pnpm audit --prod --audit-level=low` 真实失败：**25 vulnerabilities（12 high / 12 moderate / 1 low）**，报告涉及 `js-yaml`、`fast-uri`、`ip-address`、`undici`、`brace-expansion`、`hono` 等路径。GitHub repository advisories API 返回 0，但 Dependabot API 返回 403（仓库禁用或当前 token 无权）；这些结果不能互相抵消。
5. anydoc API 最终快照为 **18,068 Stars / 1,042 Forks / Rust / MIT**，`pushed_at=2026-08-20T23:51:46Z`；release `v0.2.3` 为正式 release。固定提交对应的 CI、Release、Pages 三个 GitHub Actions run 均为 `success`。
6. anydoc 本机没有 Cargo/Rustc，因此没有编译 Rust 源码、运行 `cargo test` 或 fuzz。改用 release API 给出的 Linux x86_64 Python wheel：下载后 SHA-256 为 `d945165080917c7206273d9bc4eeda19b549b765d7ed7612e06f279bab791d6a`，与 GitHub release asset digest 完全一致；隔离 venv 中运行上游 Python binding tests，真实结果 **9 tests passed / 0 failed**。
7. anydoc 额外 smoke：DOCX、PPTX、XLSX、text PDF 均转换成功；encrypted ODT 返回 `EncryptedError`；zip-bomb fixture 返回 `ResourceLimitError(max_entry_bytes)`。`node/package-lock.json` 的 `npm audit --omit=dev --package-lock-only` 返回 **0 known vulnerabilities**，但本机未做 Cargo dependency audit，不能据此声称完整供应链安全。

## 项目速览

> 下表 Stars / Language / License / 更新时间均来自本次 GitHub repository API；Stars 是查询时快照。顶层 MIT/Apache-2.0 不代表依赖、模型、制品、服务或品牌资产自动同许可。

| 项目 | Stars | Language | License | pushed_at | 今日判断 |
|---|---:|---|---|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 187,904 | TypeScript | MIT | 2026-08-21T12:35:08Z | **深读：plugin composition、session truth、guarded tool pipeline** |
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | 25,940 | Rust | Apache-2.0 | 2026-08-23T10:49:04Z | 近期已研究，今日不重复深读 |
| [anywhere-labs/deepseek-harness-desktop](https://github.com/anywhere-labs/deepseek-harness-desktop) | 18,915 | TypeScript | MIT | 2026-08-23T09:27:44Z | DSH 桌面生态候选，权限面更大，暂不安装 |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 18,068 | Rust | MIT | 2026-08-20T23:51:46Z | **深读：多格式本地摄取、统一模型、资源上限** |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | 17,431 | Python | MIT | 2026-08-23T13:37:35Z | provenance 移除涉及合规边界，不作为今日迁移对象 |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | 14,970 | Python | MIT | 2026-08-23T20:10:41Z | unattended worker 候选，近期已有同主题研究 |
| [yc-software/qm](https://github.com/yc-software/qm) | 14,106 | TypeScript | MIT | 2026-08-22T00:39:05Z | 多人 Agent harness，近期已研究 scope/policy |
| [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) | 13,011 | Python | Apache-2.0 | 2026-08-23T15:22:32Z | image-to-3D 流程候选，与当前 shared hub 主线较远 |

## 深读项目

### 1. deepseek-ai/deepseek-harness

- **一句话判断**：值得学习的不是“Everything is a Plugin”口号，而是它让 prompt、tool、session、agent loop 都可组合，同时把真实执行重新收敛到 scoped registry、monotonic guard、canonical output 和 durable session event，避免“可替换”退化成“可绕过”。
- **解决的问题**：替代把 provider、工具、记忆、UI、审批和 loop 写死在一个 Agent core 中的做法；同时替代仅靠 prompt 声明工具限制、把 UI transcript 当 durable truth、把 approval 缺失当隐式允许、把插件生命周期脚本全部默认放行的做法。

#### 基本信息与核验来源

- URL：https://github.com/deepseek-ai/deepseek-harness
- GitHub API：**187,904 Stars / 20,909 Forks / TypeScript / MIT**。
- API 时间字段：`created_at=2026-08-13T11:56:32Z`，`updated_at=2026-08-23T23:34:44Z`，`pushed_at=2026-08-21T12:35:08Z`，open issues count `0`，default branch `master`。
- 固定 commit/tag：`b150a551b8d465e31e418e1b2eaf5e79bbb7d28e` / `dsh-v0.1.1-rc.2`。
- Release API：`dsh-v0.1.1-rc.2`，prerelease `true`，发布时间 `2026-08-21T12:35:08Z`；release notes 是 DeepSeek Files API 图片上传/复用与图片预处理改进；release 没有 GitHub assets。
- README/docs：README 明确 developer preview 与 breaking changes；`docs/architecture.md` 描述 Cordis、profiles/bundles、session events、turn flow 和 capability seams；`docs/tool-execution-pipeline.md` 给出工具执行图。
- 本地版本：Node `v22.14.0`，低于仓库 `package.json` 的 Node `^22.19.0 || >=24.0.0`；pnpm 使用 `11.7.0`。
- 真实定向测试：`system-prompt/tool-order`、`tools/execution-mode`、`tools/scoped`、`tools/tools`、`tool-terminal/tools`、`tool-terminal/render` 共 **6 files / 208 tests passed**。
- 未验证：全仓 tests/typecheck/build、postinstall、native binaries、PTY E2E、Landlock、Web UI、DeepSeek Files API、真实模型请求、MCP、E2B、subagent provider 与 Windows behavior 均待核验。

#### 架构 / 实现与数据流

```text
profile + bundles + user/home/--patch layers
                    |
                    v
             Cordis plugin tree
  (service definitions/providers/consumers + reversible effects)
                    |
       +------------+-------------+
       |            |             |
       v            v             v
 SystemPrompt   ToolRuntime     Session append-only log
 sections/ctx   scoped view     durable events + projections
 tools/vars     restrictions               |
       |        guards/policy               v
       +-----------> AgentLoop <----- deriveMessages()
                         |
                         v
 agent/pre-step -> request -> llm stream -> tool/call
                         |
                         v
 pre-execute -> monotonic guards -> approval -> execute/body
     -> post-execute -> canonical JSON/output schema -> finalizeContent
     -> frozen tools/result -> durable tool/result -> next step/turn end
```

关键设计不是“插件越多越好”，而是把不同事实放在不同平面：

1. **composition plane**：profile/bundle/patch 决定装载什么；注册是可逆 effect。
2. **scope plane**：global、preset、agent scope 通过 chain 和 shadowing 决定某个 Agent 看见的 prompt/tool/provider；scope presence 不是授权证明。
3. **truth plane**：模型可见输入必须能由 append-only session log 重建；UI/transcript 是 projection。
4. **effect plane**：工具调用经过 pre/guard/approval/execute/post/finalize/result；工具 body 的 canonical value 先做 lossless JSON snapshot 和 output schema validation。
5. **lifecycle plane**：agent handle、driver quiescence、disposer 与 scoped effect unwind 分开，避免 session/agent/plugin teardown 次序漂移。

#### Repo tree 摘要（固定 commit）

```text
deepseek-harness/
├── apps/                         # CLI/Web 等产品入口
├── packages/                     # 234 个 package.json 的能力/产品包层
│   ├── core/
│   │   ├── session/              # append-only SessionEvent 真相与 projection
│   │   ├── system-prompt/        # prompt/context/tool schema 组装
│   │   ├── tools/                # scoped registry + guarded execution pipeline
│   │   ├── agent/                # Agent contract、registry、scope/owner
│   │   └── agent-loop/           # 默认 turn/step driver
│   ├── credentials/              # secret reference/provider/authorization seams
│   ├── terminal/ shell/ fs/      # 高权 effect capability 与工具适配
│   ├── sandbox/ subprocess/      # 执行环境与进程边界
│   ├── subagent/ mcp/ workflow/  # 外部/子 Agent 与复合工作流
│   └── client/                   # UI projection 与 Host/Client 分层
├── native/landlock-run/          # Linux 原生隔离 launcher；本次未构建
├── vendor/                       # Cordis 等 vendored source + upstream manifest
├── python/sdk/                   # stdio JSON-RPC Python client
├── python/sdk-runtime/           # bundled runtime carrier
├── docs/                         # architecture/subsystems/generated catalogs
├── scripts/                      # build/gates/catalog/notices/release 工具
├── examples/                     # agent spine、ACP、JSON-RPC 示例
├── pnpm-workspace.yaml           # workspace、allowBuilds、patched deps
├── pnpm-lock.yaml                # 精确 transitive dependency graph
├── THIRD_PARTY_NOTICES.md        # 直接依赖、vendored 与特殊 payload 许可说明
└── package.json                  # pnpm 11.7、Node engine、build/test/gate 入口
```

本次 `git ls-files` 统计真实返回 7,903 个 tracked files、234 个 `packages/*/*/package.json`、232 个 `packages/*/*/src/index.ts`、689 个匹配的 package tests；这些数字只是仓库规模证据，不代表全部 package 均已运行。

#### 关键源码文件

| 文件 | 用途 | 本次源码结论 |
|---|---|---|
| `docs/architecture.md` | 系统地图 | plugins 提供 services/events/reversible effects；session、system-prompt、tools、agent、agent-loop 是可替换 packages |
| `packages/core/system-prompt/src/index.ts` | prompt/context/tool schema assembly | global + scope chain 合并；scoped 同名覆盖 global；未知 tool order、重复 complete section、未知变量均 loud failure |
| `packages/core/tools/src/index.ts` | 工具 registry 和 effect chokepoint | 参数先 lossless snapshot/freeze；pre decision 后有 monotonic guards；canonical output 校验后才形成 authoritative result |
| `packages/core/agent/src/index.ts` 与 `docs/subsystems/core.md` | Agent ownership/lifecycle | Agent/session 共用 branded identity；handle disposer 是 capability；ambient initiator 仅因果归因，不是 authorization |
| `packages/terminal/tool-terminal/src/index.ts` | persistent PTY tools | owner 取自 initiating Agent；输出有 byte cap；idle/timeout 不等于进程退出；close 等待 owned process tree |
| `packages/credentials/credentials/src/index.ts` | secret reference seam | config/UI 保存 reference 与 presence/source/writable，不读取 value；consumer 每 operation re-resolve，避免重启与长期缓存 |
| `pnpm-workspace.yaml` | install-script policy | `strictDepBuilds` 语义下显式 allow/deny lifecycle scripts；`node-pty`、`koffi` 等 allow，部分无用脚本 deny |
| `THIRD_PARTY_NOTICES.md` | 许可边界 | 根 MIT 之外，运行依赖含 Apache/BSD/ISC；Claude payload 声明 `SEE LICENSE`；锁文件才是完整 transitive closure |

#### ⭐ 源码精读

**代码块 1：`SystemPrompt.assemble(...)`——scope merge、known-name validation 与 complete prompt 约束在一次 assembly 中完成**

来源：`packages/core/system-prompt/src/index.ts:467-541`。

```typescript
async assemble(context: AssembleContext = {}): Promise<PromptAssembly> {
  const scope = context.scope
  const scopeLayers = this.layers.chainLayers(scope)
  const variables: Record<string, string | undefined> = {}
  for (const [name, provider] of this.layers.global.variables.entries()) {
    variables[name] = provider(context)
  }
  for (const layer of scopeLayers) {
    for (const [name, provider] of layer.variables.entries()) {
      variables[name] = provider(context)
    }
  }
  const sectionByName = this.layers.merge(scope, layer => layer.sections)
  const contextByName = this.layers.merge(scope, layer => layer.contexts)
  // ... collect schemas and pre-restriction knownNames ...
  const completeSections = sectionDefinitions.filter(section => section.complete === true)
  if (completeSections.length > 1) {
    throw new Error(`multiple complete prompt sections are active: ...`)
  }
  // ... canonical ordering, waterfall, complete-section restoration ...
}
```

逻辑摘要：scope chain 由远到近覆盖变量；sections/contexts 通过同一 scope resolver 合并；tool schema 和 known names 分开，让被 restriction 隐藏的已知 tool 不被误判为配置不存在；多个 complete prompt 直接失败。边界：prompt assembly 只控制模型可见内容，不构成真实 tool authorization；真正 effect 仍须在 ToolRuntime chokepoint 重验。

**代码块 2：`ToolRuntime.execute(...)` 与 `prepareExecution(...)`——extensible policy 之后仍有不可反转的 monotonic guard**

来源：`packages/core/tools/src/index.ts:1342-1506`。

```typescript
async execute(exec: ToolExecutionInput): Promise<ToolExecutionResult> {
  return this.prepareExecution(exec, prepared => this.completeScheduledExecution(prepared))
}

private async prepareExecution<T>(input: ToolExecutionInput, next: ...): Promise<T> {
  const created = this.createExecution(input)
  if (created.kind !== 'ready') return next(created)
  const exec = created.exec
  const gate = await this.ctx.waterfall(
    scopeTarget(this, exec.agent), 'tools/pre-execute', exec,
    () => Promise.resolve<PreToolDecision>({ kind: 'allow' }),
  )
  const { decision } = gate.kind === 'ask'
    ? await this.serviceAsk(exec, gate)
    : { decision: gate, approvalCancelled: false }
  const denialReason = decision.kind === 'allow'
    ? this.guardReason(exec)
    : decision.reason
  if (denialReason !== undefined) return await next({ kind: 'post-result', exec, result: ... })
  if (this.callerCancelled(exec)) return await next({ kind: 'post-result', exec, result: ... })
  return await next({ kind: 'dispatch', exec })
}
```

逻辑摘要：调用参数先在 `createExecution` 中做 lossless JSON materialization 与 freeze；pre-execute waterfall 可 allow/deny/ask；ask 必须通过 approval seam；然后 monotonic guard 只能 deny/abstain，不存在后置 allow 覆盖 denial；caller cancellation 在 dispatch 前再次检查。边界：插件代码与 tool body 仍处于同一进程时，pipeline 不能提供 OS 级隔离；sandbox/provider 的真实 enforcement 需独立验证。

**代码块 3：`createSuccessResult(...)`——canonical value 与 model/UI projection 分开，schema 不匹配变成 typed failure**

来源：`packages/core/tools/src/index.ts:1792-1822`。

```typescript
private createSuccessResult(
  exec: ToolExecution,
  tool: ToolDefinition,
  candidate: unknown,
): ToolExecutionSuccess {
  const detached = snapshotToolValue(tool.name, candidate)
  const violations = validateJsonSchemaValue(tool.output.schema, detached, 'value')
  if (violations.length > 0) throw new ToolOutputError(tool.name, violations)
  const value = deepFreeze(detached)
  const content = snapshotProjection(
    tool.name, 'render', tool.output.render(exec.arguments, value),
  )
  let meta: JsonValue | undefined
  if (exec.parent === undefined && tool.output.presentationMeta !== undefined) {
    meta = snapshotProjection(
      tool.name, 'presentationMeta', tool.output.presentationMeta(exec.arguments, value),
    )
  }
  return this.markCanonical(exec, this.materializeFinalResult({
    isError: false, value, content, ...(meta !== undefined ? { meta } : {}),
  }) as ToolExecutionSuccess)
}
```

逻辑摘要：body 返回值不能直接成为“成功”；先必须是 lossless JSON，再满足工具声明的 output schema，再分别生成模型 content 与 top-level UI meta，所有 projection 也重新 snapshot。复合工具的 nested call 不生成 presentation meta。边界：schema-valid 只能证明形状，不证明外部 effect、业务结果或数据真实性；Hermes 审计仍需 artifact readback/hash/exit/coverage。

**代码块 4：`CredentialProvider.resolve(...)` 契约——配置面只保存 reference，值在每个 operation 重新解析**

来源：`packages/credentials/credentials/src/index.ts:177-208`。

```typescript
export abstract class CredentialProvider extends Service {
  abstract resolve(ref: CredentialRef): Promise<ResolvedCredential | undefined>
  abstract describe(ref: CredentialRef): Promise<CredentialInfo>
  abstract set(ref: CredentialRef, value: string): Promise<void>
  abstract unset(ref: CredentialRef): Promise<void>
}
```

该抽象类上方的源码契约明确：consumer 每次 operation 重新 `resolve`，不得跨 operation 缓存；`describe` 只暴露 configured/source/writable，不暴露 value；空 stored value 视为 absent。边界：reference grammar 和 provider interface 不等于 storage 加密、进程隔离或 secret redaction 全部完成，具体 provider/telemetry/subprocess 仍需逐层审计。

#### 依赖分析与供应链风险

- 根 `package.json`：版本 `0.1.1-rc.2`、package manager `pnpm@11.7.0`、Node engine `^22.19.0 || >=24.0.0`；本机 Node 22.14 不满足支持范围。
- 核心 package 采用 workspace peer dependencies：`dsh-tools` 依赖 Cordis、scope、session、system-prompt、agent、approval、code-runtime 等 seam；`dsh-agent-loop` 依赖 session/persistence/system-prompt/tools/settings；terminal tool 依赖 terminal/jobs/tools/output-retention。
- `pnpm-workspace.yaml` 显式 `allowBuilds`：默认阻断未审查 lifecycle scripts；允许 `esbuild`、`lefthook`、`node-pty`、`koffi` 和一个 workspace postinstall，明确 deny `@google/genai`/`protobufjs` 等不需要的 scripts。本次使用 `--ignore-scripts`，因此没有验证这些脚本或 native package。
- `THIRD_PARTY_NOTICES.md` 只声明 direct dependencies 与特殊 payload；完整 npm closure 在 `pnpm-lock.yaml`，Python closure在 `python/sdk/uv.lock`。运行面含 MCP、Claude SDK、Codex、E2B、OpenTelemetry、PTY、Sharp 等高权限/原生/网络依赖。
- 本次 production audit 真实报告 **25 vulnerabilities：12 high、12 moderate、1 low**。至少包括：`js-yaml` quadratic CPU、`fast-uri` host confusion、`ip-address` SSRF classification、`undici` cache/CRLF、`brace-expansion` DoS、`hono` ReDoS/SSR disclosure。是否在默认 profile 可达需逐 path 复核，但在修复/隔离前不能称为安全基线。
- repository advisories API 的 0 只表示公开 repository advisories endpoint 当时为空；Dependabot endpoint 为 403，且 audit 已有具体 advisory，不能用“0 advisories”覆盖本机扫描。

#### README / docs / release / tests 交叉核验

- README “everything is a plugin” 与 `docs/architecture.md` 的 session/system-prompt/tools/agent-loop package 分层一致；但 docs 同时把 session log 称为模型上下文 source of truth，说明插件化不等于事实来源任意化。
- `docs/tool-execution-pipeline.md` 的 pre → guard → approval → execute → post → finalize → result 顺序与 `ToolRuntime` 源码一致。
- `tools.spec.ts` 真实覆盖：schemas 不暴露 host callbacks/timeout、output schema mismatch、pre deny、approval missing/agentless fail-closed、post block、cancellation、hostile thrown value 等；本次其中 136 tests 全部通过。
- `system-prompt/tool-order.spec.ts`、`tools/scoped.spec.ts` 与源码的 unknown tool fail-loud、scope restriction/shadowing 对应；本次定向通过。
- Release 是 RC/developer preview；没有 GitHub release assets，不能把 source tag 等同于已验证的所有平台制品。
- GitHub API open issues count 为 0，但仓库引导用户使用 Discussions；0 open issues 不代表无缺陷。

#### 可复用经验

- 当 Agent framework 追求“everything is a plugin”时，应优先同时定义不可绕过的 host-owned registry、scope resolver、durable truth 和 final effect chokepoint，因为可替换能力不应让 prompt、UI 或插件声明自行获得授权；边界是同进程插件仍需 OS sandbox 和供应链审计。
- 当多个 policy listener 可以改写决策时，应优先在可扩展 waterfall 后追加只可 deny/abstain 的 monotonic guard，因为 listener 排序不应把 owner/security denial 重新变成 allow；边界是 guard 输入身份和 scope 必须由 host 注入。
- 当工具结果要同时服务模型、UI 和审计时，应优先保留 canonical structured value，并从它生成 model content/UI meta/durable event，而不是从 prose 反解析成功，因为 projection 可以有损；边界是 schema-valid 不证明 effect 成功。
- 当 prompt/tool 配置按 workspace 或 Agent 覆盖时，应优先用 scope chain、同名 shadowing、重复/未知项 loud failure 和 disposal contract，因为隐式 merge 容易产生 capability drift；边界是 scope 只是组合身份，不是权限证明。
- 当 credential 会轮换且配置 UI 不应看见 secret 时，应优先保存 reference/presence/source/writable，并在每个 operation 重新 resolve，因为跨 operation 缓存会产生 stale secret；边界是 provider storage、subprocess env 与 telemetry 仍需独立最小化。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/scoped-canonical-tool-envelope/` 做纯 Python、无 provider 的 fixture：

1. 定义 `ToolDefinition(name, input_schema, output_schema, effect, concurrency)`、`Scope(global/preset/agent)`、`Decision(allow/deny/ask)`、`ToolReceipt`。
2. fixture 覆盖：agent scope 隐藏 global tool、unknown configured name fail-loud、pre allow 但 monotonic guard deny、approval unavailable deny、body value schema mismatch、model projection 截断但 canonical value 保留。
3. 输出 `prepare/dispatch/post/terminal` 四阶段 receipt；禁止调用真实 shell/network/provider。
4. 与 Hermes 当前 tool API 只做 adapter contract 对照，不修改 `~/.hermes/config.yaml`、provider、auth、cron 或 shared skill。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 MIT；`THIRD_PARTY_NOTICES.md` 明确依赖有 Apache/BSD/ISC、LGPL/MPL 开发工具和 `SEE LICENSE` 的 Claude payload，不能把整个运行闭包都称为 MIT。
- **维护活跃度**：固定 commit/release 在 2026-08-21，repository API 于 2026-08-23 仍更新，短期很活跃；但 README 明确 developer preview、breaking changes，稳定性不足。
- **安全风险**：本机 audit 有 25 个已知 advisory；MCP、E2B、subagent、PTY、filesystem、sandbox、Git hooks、postinstall 和 provider 都是 authority surface。没有完成可达性与 patch 验证前不部署为 Hermes 替代 runtime。
- **运行局限**：本机 Node 低于支持 floor；安装跳过 lifecycle scripts；仅跑 208 个定向 tests，没有全仓 build/typecheck/E2E/native/real API。
- **架构局限**：同进程 plugin/effect 可逆不等于强隔离；append-only log 不自动防篡改；approval seam 不等于身份认证；scope attribution 不等于 authorization。
- **不适用场景**：不直接用于生产 credential 操作、无人工审批的高权 shell/MCP、多租户强隔离或要求稳定 API/SLA 的系统。
- **不能自动执行**：不安装/启动 DSH 产品，不修改 Hermes provider/model/cron/secret，不加载其 plugin 或执行 postinstall/native payload，不复制 DSH 源码进 shared skill。

#### ⭐ Skill 升格判断

**需二次验证。** 候选不是“DeepSeek Harness Skill”，而是 agent-neutral 的 `scoped-canonical-tool-envelope`：composition scope → model-visible schema → pre decision → monotonic guard → canonical structured result → projections/receipt。理由是源码与 208 个定向测试已支持该机制，但运行环境不满足 Node floor、全仓/E2E 未跑且 audit 有 25 个 advisory。先做 Hermes 离线 fixture，并与 shared 现有 verification-first、effect-scope、subagent 四状态、shared-skill-governance 去重；今日不创建 shared skill，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **Hermes runtime POC**：`runtime/hermes/github-learning-poc/scoped-canonical-tool-envelope/{schema.py,engine.py,fixtures/,test_engine.py,README.md}`。
2. **Hermes tool adapter**：未来在 host-owned executor 外层定义 `scope_id/call_id/tool_name/input_hash/pre_decision/guard_decision/body_invoked/output_schema/terminal`；模型只能提出 call，不能设置 scope/guard result。
3. **Hermes audit**：`scripts/github_learning_orchestrator.py` 后续可把结构审计与 artifact receipt 分开，`audit_score` 不得覆盖 missing artifact、blocked prerequisite 或依赖 audit failure。
4. **shared hub**：原始研究继续在 `inbox/hermes/daily/`；fixture/log 在 `runtime/hermes/`；通过证据、评分、去重、脱敏、治理审查后才考虑 `curated/memory/facts/` 或 `capabilities/skills/`。
5. **OpenClaw 边界**：当前运行时不存在，不实现或调用 adapter；未来仅共享 agent-neutral schema，并要求其自身验证 loader、scope、effect 和 terminal receipt。

### 2. firecrawl/anydoc

- **一句话判断**：值得学的不是“文档转 Markdown”这个功能本身，而是把 content detection、format-specific parser、统一 Document model、单一 renderer、typed failure 和不可配置的资源上限组合成一个可离线验收的摄取边界。
- **解决的问题**：替代按扩展名盲选 parser、每种 Office 格式各自拼 Markdown、遇到 malformed/加密/zip bomb 只返回模糊失败、为了读文档默认发送 hosted OCR，以及 Agent Skill 直接把无限输出塞进上下文的做法。

#### 基本信息与核验来源

- URL：https://github.com/firecrawl/anydoc
- GitHub API：**18,068 Stars / 1,042 Forks / Rust / MIT**。
- API 时间字段：`created_at=2026-08-03T16:36:14Z`，`updated_at=2026-08-23T23:16:19Z`，`pushed_at=2026-08-20T23:51:46Z`，open issues count `63`，default branch `main`。
- 固定 commit/tag：`bf3d33e61731580d1ee1c6a85e56093d715a21a6` / `v0.2.3`。
- Release API：`v0.2.3`，正式 release，发布时间 `2026-08-20T23:56:40Z`；主题为 spreadsheet checkbox；release assets 对 Node/Python 多平台制品提供 SHA-256 digest。
- Issue API：#128 请求 `.eml/.msg`；#127 报告少量 EPUB title page 丢失。它们是 open issues，不代表已修复。
- Actions API（固定 commit）：CI、Release、Pages 三个 run 均 `completed/success`。
- 本机无 Cargo/Rustc；因此 Rust compile/test/fuzz **待核验**。
- 真实制品验证：下载 `firecrawl_anydoc-0.2.3-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`，本机 hash 与 release digest 均为 `d945165080917c7206273d9bc4eeda19b549b765d7ed7612e06f279bab791d6a`。
- Python binding tests：**9 passed / 0 failed**；`pip check` 返回 `No broken requirements found`。

#### 架构 / 实现与数据流

```text
path / bytes / optional explicit format
                 |
                 v
 content-based detector
 PDF | RTF | OLE stream | ZIP package identity | CSV explicit/path fallback
                 |
                 v
 format parser (doc/docx/ppt/pptx/xls/xlsx/odf/rtf/epub/csv)
                 |
        +--------+---------+
        |                  |
        v                  v
 shared Document model    PDF direct path via pdf-inspector
 blocks/inlines/table/          |
 notes/assets/styles            |
        |                       |
        +----------+------------+
                   v
          one GFM Markdown renderer
                   |
                   v
 success String OR typed ConvertError
 Unsupported/Malformed/Encrypted/ResourceLimit/MissingPart/Io
```

其关键机制有四个：

1. **identity before parser**：先看 PDF/RTF/OLE/ZIP 标识；CSV 无签名才需要 extension/explicit format。
2. **many parsers, one model/renderer**：多数格式统一进入 Document model，再由一个 Markdown renderer 处理 escaping/table/list/math；PDF 是文档中明确披露的例外，直接输出 Markdown。
3. **fixed limits**：archive entry、total decompression、entry count、XML depth/nodes、grid、expansion text、assets、binary records 都有固定上限，超限总是 `ResourceLimit`。
4. **binding parity**：Rust core 通过 napi/PyO3/wasm 暴露 Node、Python、browser API；release workflow 对 crate/npm/PyPI 版本做联动。

#### Repo tree 摘要（固定 commit）

```text
anydoc/
├── src/
│   ├── lib.rs                    # 公共 API、format resolve、Document/Markdown 路由
│   ├── formats/
│   │   ├── detect.rs             # content-based PDF/RTF/OLE/ZIP detection
│   │   ├── doc*/ ppt*/ sheet/    # format-specific parsers
│   │   ├── odf/ rtf/ epub/ csv/  # 其他 parser
│   │   └── pdf.rs                # pdf-inspector direct Markdown path
│   ├── model/                    # blocks/inlines/table/assets/style 统一模型
│   ├── render/markdown/          # 单一 GFM renderer
│   ├── package/                  # limited ZIP、XML、path、relationship
│   └── shared/                   # Office shared primitives/math/list/grid
├── tests/
│   ├── fixtures/                 # 72 个 tracked fixtures，含 malformed/abuse
│   ├── snapshots.rs              # 多格式 snapshot output
│   └── robustness.rs             # deterministic mutation smoke
├── fuzz/                         # 12 个 format fuzz targets + seeds
├── node/                         # napi binding、CLI、package-lock
├── python/                       # PyO3/maturin binding、typed stubs、9 tests
├── wasm/                         # browser binding 和 demo
├── bench/                        # speed/quality harness；corpus 不随 repo 分发
├── skills/convert-documents-to-markdown/SKILL.md
├── Cargo.toml / Cargo.lock       # Rust 1.88 floor 与精确 dependency graph
├── .github/workflows/            # Rust/Node/Python/Wasm CI、release/pages
└── LICENSE / README.md           # MIT、能力、限制和上游 benchmark
```

本次 `git ls-files` 统计真实返回 322 tracked files、74 个 `src/**/*.rs`、72 个 tracked fixture files、12 个 fuzz targets；仓库约 5.2 MiB。数字不代表 fixture 覆盖全部现实格式变体。

#### 关键源码文件

| 文件 | 用途 | 本次源码结论 |
|---|---|---|
| `src/lib.rs` | 公共转换 API | path 模式先读 bytes，content detection 优先，extension fallback；PDF direct path，其他格式进 Document + renderer |
| `src/formats/detect.rs` | format identity | RTF/OLE/ZIP 优先于 1 KiB 内 PDF header；OLE 看 stream name；ZIP 看 mimetype、rels/content type/root/path fallback |
| `src/formats/mod.rs` | parser dispatch | 每个 Format 显式分发；扩展名为 doc 但 bytes 是 RTF 时路由 RTF；PDF 禁止 Document model API |
| `src/package/limits.rs` | hard resource caps | caps 不可配置；越界统一 ResourceLimit，降低 deployment 漏配风险 |
| `src/package/archive.rs` | limited ZIP reader | 检查 declared size，再用 `take(cap+1)` 防虚假大小；相同 part cache/Rc，避免重复计费和复制 |
| `tests/robustness.rs` | mutation smoke | 每个非 abuse fixture 做 25 轮 deterministic byte mutation/truncation；允许 typed error，不允许 panic/hang/OOM |
| `python/tests/test_anydoc.py` | binding contract | API、content detection、Document model/assets、typed subclasses、zip bomb、stub parity 共 9 tests |
| `skills/convert-documents-to-markdown/SKILL.md` | Agent-facing wrapper | 建议大文件输出到文件分段读取，明确 scanned PDF 需 OCR；但默认 `npx -y` 是网络下载/执行 authority surface |

#### ⭐ 源码精读

**代码块 1：`formats::detect::from_bytes(...)`——容器 identity 优先，CSV 不做内容猜测**

来源：`src/formats/detect.rs:34-48`。

```rust
pub(crate) fn from_bytes(bytes: &[u8]) -> Option<Format> {
    if bytes.starts_with(b"{\\rtf") {
        return Some(Format::Rtf);
    }
    if bytes.starts_with(&OLE_MAGIC) {
        return detect_ole(bytes);
    }
    if bytes.starts_with(b"PK\x03\x04") {
        return detect_zip(bytes);
    }
    if bytes[..bytes.len().min(1024)].windows(5).any(|w| w == b"%PDF-") {
        return Some(Format::Pdf);
    }
    None
}
```

逻辑摘要：RTF、OLE、ZIP container 在前，PDF header 可位于前 1 KiB；纯文本 CSV 返回 None。测试还有“ZIP 内嵌 early PDF 不应把整个包判为 PDF”的反例。边界：明确 format 参数可以绕过 detection 直接选 parser，因此 host adapter 仍应记录 `detected_format/selected_format/source`，并对冲突做 policy。

**代码块 2：`to_markdown_bytes(...)`——PDF 例外显式披露，其余格式统一 Document → Markdown**

来源：`src/lib.rs:115-137`。

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

逻辑摘要：公共 API 先 resolve format；PDF 由 `pdf-inspector` 直接生成 Markdown，不能调用 Document model；其他格式通过 parser 得到统一 Document，再进入一个 renderer。边界：所谓“one consistent output”对 PDF 有显式架构例外；scanned/image-only PDF 不支持 OCR，不能把 unsupported 当空文本成功。

**代码块 3：`Package::part(...)`——同时验证声明大小与实际读取量，且总预算按解压字节累计**

来源：`src/package/archive.rs:39-89`。

```rust
pub fn part(&mut self, name: &str) -> Result<Option<Rc<[u8]>>, ConvertError> {
    let name = name.trim_start_matches('/');
    if let Some(bytes) = self.cache.get(name) {
        return Ok(Some(Rc::clone(bytes)));
    }
    let mut file = match self.zip.by_name(name) {
        Ok(f) => f,
        Err(zip::result::ZipError::FileNotFound) => return Ok(None),
        Err(e) => return Err(ConvertError::Malformed { part: Some(name.to_string()), detail: e.to_string() }),
    };
    if file.size() > limits::MAX_ENTRY_BYTES {
        return Err(ConvertError::ResourceLimit { limit: "max_entry_bytes", detail: ... });
    }
    let remaining_total = limits::MAX_TOTAL_BYTES.saturating_sub(self.total_read);
    let cap = limits::MAX_ENTRY_BYTES.min(remaining_total);
    let mut bytes = Vec::new();
    let read = (&mut file).take(cap + 1).read_to_end(&mut bytes)? as u64;
    if read > cap { return Err(...); }
    self.total_read += read;
    let bytes: Rc<[u8]> = Rc::from(bytes);
    self.cache.insert(name.to_string(), Rc::clone(&bytes));
    Ok(Some(bytes))
}
```

逻辑摘要：先检查 ZIP declared size，再用 capped reader 防止 header 欺骗；cap 取单 entry 与 archive remaining budget 的较小值；重复读取同 part 用 Rc cache，不重复解压、复制或计费。边界：这是进程内 memory/decompression 防线，不是 CPU deadline、进程 sandbox、文件输入大小、输出大小、并发总预算或恶意 native dependency 的完整防线。

**代码块 4：`mutated_fixtures_never_panic()`——把 malformed 输入视为正常 typed-error surface**

来源：`tests/robustness.rs:24-56`。

```rust
#[test]
fn mutated_fixtures_never_panic() {
    let root = fixture_root();
    let mut files = Vec::new();
    walk(&root, &mut files);
    let mut rng = Rng(0x5EED_1234_5678_9ABC);
    for path in files {
        // ... skip dedicated abuse fixtures, resolve format ...
        for _ in 0..25 {
            let mut bytes = original.clone();
            for _ in 0..1 + (rng.next() % 8) {
                let pos = (rng.next() as usize) % bytes.len();
                bytes[pos] = rng.next() as u8;
            }
            if rng.next().is_multiple_of(4) { bytes.truncate(cut.max(1)); }
            let _ = anydoc::to_markdown_bytes(&bytes, format);
        }
    }
}
```

逻辑摘要：固定 seed 保证跨运行可重放；每个 fixture 做 burst mutation 和偶发 truncation；允许 `Err`，测试目标是“不 panic/hang/exhaust memory”。边界：本机无 Cargo，没有运行该测试或 fuzz；这里只能确认源码机制，运行状态待有 Rust 1.88+ 环境复验。

#### 依赖分析与供应链风险

- 根 `Cargo.toml`：Rust edition 2024、`rust-version=1.88`、版本 0.2.3；core direct dependencies 是 `cfb 0.14.0`、`csv 1.4.0`、`flate2 1`、`encoding_rs 0.8.35`、`log 0.4`、`pdf-inspector 1.14.2`、`quick-xml 0.41.0`、`zip 8.6.0`。
- `Cargo.lock` 固定 transitive crates 与 checksums；Python binding 用 PyO3/maturin，Node binding 用 napi，Wasm 用 wasm-bindgen/serde。根 MIT 不替代所有 crate/native artifact 的逐项 license/advisory 审查。
- Python wheel 是本次真实 release artifact，hash 与 GitHub API digest一致；hash 只证明下载字节对应 release 声明，不能证明 build provenance、源码可复现或无恶意代码。
- Node package 需要 Node >=20，release 以 native `.node` artifact 分平台发布；其 npm package `files` 不包含源码。调用 `npx` 会下载并运行平台 binary，因此必须 pin 版本/hash/cache，不能在无人值守高权 Agent 中每次取 latest。
- `npm audit --omit=dev --package-lock-only` 对 Node binding lock 返回 0 known vulnerabilities；本机没有 Cargo，未运行 `cargo audit`，也未对 wheel 做 SBOM/签名/可复现构建验证。
- README 的 speed/quality benchmark 由上游 100 个非再分发 corpus、Claude Sonnet 5 judge 与指定硬件产生；本次没有复现，不能把 4.4ms/81 score 当本机实测。

#### README / release / issues / source / artifact 交叉核验

- README “content-based detection” 与 `detect.rs` 的 signature/container identity 一致；CSV 的例外在 README、源码与 Python test 三处一致。
- README “one shared model/renderer” 与 `src/formats/mod.rs`、`src/model/`、`src/render/markdown/` 一致；PDF direct path 例外也在源码/JSDoc 明确披露。
- README 的 fixed safety limits 与 `limits.rs`/`archive.rs`/abuse fixtures 对应；本机 wheel test 真实将 zip bomb 转为 `ResourceLimitError(max_entry_bytes)`。
- Release v0.2.3 的 checkbox model 与 `.github/releases/v0.2.3.md` 一致；固定 commit CI/Release/Pages success，但本机没有复跑 Rust/Wasm/Node binding build。
- Issue #127 说明 EPUB title page 在少量输入仍可能丢失；#128 说明 email format 尚不支持。故不应把“14 formats”外推为所有文件类型或所有 edge cases 完整。
- Wheel smoke 真实成功转换 DOCX/PPTX/XLSX/text PDF；这是 fixture-level 证据，不是私有/现实 corpus 的完整 fidelity 证明。

#### 可复用经验

- 当 Agent 摄取用户上传的 Office/EPUB/PDF 时，应优先按内容/container identity 检测格式并记录 extension conflict，而不是只信文件名，因为扩展名可错、可伪造；边界是 explicit override 仍须 host policy 和证据字段。
- 当多种 parser 要输出同一种知识表示时，应优先使用共享中间模型加单一 renderer，因为 escaping/table/link/math 修复可以一次覆盖多格式；边界是 PDF/OCR 等例外必须在 schema 中显式标记，不能伪装成统一路径。
- 当解析 ZIP/XML/binary 等不可信复杂格式时，应优先使用不可由调用方放大的 hard caps、typed ResourceLimit、mutation fixtures 和 fuzz targets，因为默认配置遗漏不应关闭安全下限；边界是仍需进程级 CPU/memory/deadline/egress 隔离。
- 当 release 提供 native wheel/node artifact 时，应优先 pin tag、校验 release digest、隔离安装并运行 binding contract tests，因为“来自官方 GitHub”不能证明实际字节或 ABI；边界是 hash 不是签名和可复现构建证明。
- 当转换结果要进入 LLM/context/shared memory 时，应优先保留 `source_hash/format/detector/converter_version/terminal/truncated/output_hash`，并把 Markdown 当 derived projection，因为转换可能丢失标题、布局、隐藏内容或 OCR；边界是成功转换不等于事实可信。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/document-ingestion-receipt/` 做本地 fixture，不处理用户私有文件：

1. 输入 4 个公开测试 fixture（DOCX、XLSX、text PDF、zip bomb），计算 input hash。
2. 用已校验 wheel 的隔离 venv 调用 Python API，输出 `detected_format/selected_format/converter_version/status/error_code/output_path/output_hash/truncated`。
3. 强制 output 写文件并设置 byte cap；unsupported/encrypted/resource-limit 分别为不同 terminal，不能变成空 Markdown success。
4. 只写 `runtime/hermes/`；不自动安装 Agent Skill，不上传 hosted OCR，不修改 Hermes tools/config/provider/cron。

#### 风险边界

- **License**：GitHub API、Cargo/Python/Node metadata 和 LICENSE 均为 MIT；crate、napi/PyO3、pdf-inspector、zip、release artifact 与 hosted Firecrawl API 仍需分别审核。
- **维护活跃度**：固定 release/commit 在 2026-08-20，open issues 63，近期持续 release；项目创建时间很短，接口与 fidelity 仍可能快速变化。
- **安全风险**：解析复杂二进制格式是高风险输入面。代码有 hard caps、mutation tests、fuzz targets，但本机没有运行 Rust tests/fuzz/cargo audit；native wheel 也不是 sandbox。
- **数据风险**：本地 library 与 browser Wasm 可避免上传，但 Agent Skill 默认 `npx -y` 会联网取制品；hosted API/OCR 是另一数据出口，不能自动 fallback。
- **输出局限**：image-only PDF unsupported；issue #127 表明 EPUB title page 有 edge case；格式转换天然丢失版式、宏、OLE 行为、隐藏内容等，Markdown 不应替代原件。
- **benchmark 局限**：4.4ms/81 quality 来自上游指定 corpus/judge/hardware，未在本机复现；不能作为 Hermes SLA。
- **不适用场景**：不直接用于法律证据保真、恶意文档高权进程、需要 OCR/布局坐标/宏执行/完整电子邮件解析的工作流。
- **不能自动执行**：不运行 `npx skills add`，不安装到 Hermes/shared skills，不处理用户私有 corpus，不上传 Firecrawl Parse，不把转换 Markdown 自动晋升 curated truth。

#### ⭐ Skill 升格判断

**需二次验证。** `document-ingestion-receipt` 工作流具有跨 Agent 价值，但不能直接复制上游 `SKILL.md` 并默认执行 `npx -y`。原因：已完成 release digest、9 binding tests 和 6 个 smoke/error fixture；但 Rust/fuzz/cargo audit 未运行，Hermes 目前已有文件读取/Office 提取能力，需先做 capability overlap、隐私出口、output cap、typed terminal 和 artifact provenance 对比。今日不创建 shared skill，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **Runtime POC**：`runtime/hermes/github-learning-poc/document-ingestion-receipt/{schema.json,convert.py,fixtures.json,test_convert.py,README.md}`；使用固定 wheel digest或现有受控 parser，不从 latest 动态安装。
2. **Hermes tool contract**：输入 `source_path/source_hash/declared_extension/privacy_label/max_output_bytes`；输出 `detected_format/converter/version/status/error/output_hash/truncated`；原文件保持 canonical，Markdown 是 derived artifact。
3. **shared-memory gate**：转换结果先进入 `inbox/hermes/daily/` 或 runtime evidence，不直接进 curated；候选 fact 必须回链原文位置、source hash 和转换 receipt。
4. **Hermes audit**：文档摄取失败按 `unsupported/encrypted/resource_limit/malformed/blocked` 分开；0 字符或 truncated 不得标 completed。
5. **future/OpenClaw adapter**：当前 OpenClaw 不存在，不实施；未来只消费相同 receipt schema，并独立验证其 parser binary、privacy、path scope 和 output limits。

## 经验沉淀

1. **当系统允许插件替换 prompt、tool、provider 或 loop 时，应优先把 scope resolution、durable truth、monotonic guard 和 final effect chokepoint 留在 host-owned 确定性外壳中，因为“可组合”不应等于“可绕过”；边界是同进程插件仍不构成 OS 隔离。**
2. **当工具输出同时供模型、UI、审计和恢复使用时，应优先保留 schema-validated canonical value，再生成各 projection，因为 prose/卡片/日志都可能截断或有损；边界是形状正确仍不证明外部 effect 已成功。**
3. **当 Agent 摄取扩展名可伪造的复杂文件时，应优先使用 content/container identity、显式 conflict、typed terminal 和原件 hash，因为文件名与空 Markdown 都不是可信完成证据；边界是 explicit override 也必须受 host policy。**
4. **当 parser 面对 ZIP/XML/binary 放大输入时，应优先使用不可配置的安全下限加进程级预算，并用 abuse/mutation/fuzz fixture 验证，因为调用方漏配不能关闭最小防线；边界是 hard cap 不能替代 CPU deadline 与 sandbox。**
5. **当无人值守任务要使用 native/npm/wheel 制品时，应优先 pin immutable tag、核验 release digest、隔离安装并运行 contract tests，因为官方 repo、HTTPS 和顶层 license 不能证明运行字节；边界是 digest 不是签名或可复现构建证明。**
6. **当依赖审计与 GitHub advisory 页面结论冲突时，应优先保留每个扫描器的真实状态、路径和时间，而不是用“0 advisories”覆盖本机 25 个 findings，因为 endpoint 权限/配置/数据库覆盖不同；边界是 finding 仍需做可达性与版本复核。**
7. **当 shared hub 要吸收跨 Agent 方法论时，应优先把 raw 研究写 inbox、POC/日志写 runtime、candidate 经评分/证据/去重/脱敏/审查后再进 curated/skill，因为候选反哺不等于长期真相。**

## 风险边界与安全反哺

- 不自动改 Hermes 配置、模型、provider、auth、env、cron、tools 或现有 skills。
- 不调用、启动、模拟或写入 OpenClaw；当前运行时不存在。
- 不把报告、上游 benchmark、GitHub Stars 或模型生成 prose 直接写 `curated/memory/`。
- 不自动执行 DSH plugin/postinstall/native payload，不运行真实 provider/MCP/E2B/subagent/sandbox/PTY。
- 不自动执行 anydoc 的 `npx skills add`，不上传 hosted OCR/Firecrawl Parse，不处理私有文件。
- 顶层 MIT 不覆盖所有依赖、native artifact、模型服务、hosted API 或 `SEE LICENSE` payload。
- DeepSeek Harness 定向 tests 通过不能抵消 unsupported Node engine 与 25 个 audit findings；anydoc wheel tests 通过不能替代 Rust/fuzz/cargo audit。
- 巡检和审计只输出证据、影响、建议与候选动作，不自动修复依赖、配置或权限。

## Skill 升格总判断

- `deepseek-ai/deepseek-harness`：**需二次验证**。候选是 `scoped-canonical-tool-envelope`，不迁移 DSH runtime/source；先完成 Hermes 离线 fixture，并处理 Node floor、全仓覆盖和 25 个 dependency findings。
- `firecrawl/anydoc`：**需二次验证**。候选是 `document-ingestion-receipt`，不直接复制其 Agent Skill；先对比 Hermes 现有读取能力并完成 privacy/output cap/Rust audit/typed terminal 验收。
- 今日不新建 `capabilities/skills/` 目录，不更新 shared skill manifest，不写 curated active fact。若二次验证通过，必须按 shared-skill-governance 提交完整 `SKILL.md + templates/references/scripts/assets`、manifest 的 `scope/reference_policy/future_agent_readable`，并与现有能力去重。

## 明日继续

**最小下一步：在 `runtime/hermes/github-learning-poc/` 实现一个联合的 `ingest → canonical artifact → scoped proposal → guard → terminal receipt` 离线 fixture，至少覆盖 extension/content conflict、zip-bomb resource limit、truncated projection、unknown tool、approval unavailable、guard deny、invalid output schema 七类反例；不接 provider、network、shell、MCP 或私有文件。**

## 候选反哺

### Candidate Facts

- [ ] topic: scoped plugin composition 必须由 host-owned effect chokepoint 与 monotonic guard 收口 | evidence: DSH fixed commit `b150a551...` 的 `packages/core/tools/src/index.ts`、`docs/tool-execution-pipeline.md`、本机 208 targeted tests | 建议: create candidate after Hermes fixture and dependency-risk review | 安全级别: medium
- [ ] topic: canonical structured tool result 应先于 model/UI/audit projection | evidence: DSH `createSuccessResult`/`materializeFinalResult` 与 `tools.spec.ts` | 建议: update existing verification/completion candidate after dedupe | 安全级别: low
- [ ] topic: 多格式文档摄取应绑定 content identity、hard resource caps 与 typed terminal | evidence: anydoc `detect.rs`/`limits.rs`/`archive.rs`、release wheel hash、9 tests、zip-bomb smoke | 建议: create candidate only after Hermes capability overlap review | 安全级别: medium
- [ ] topic: DeepSeek Harness fixed lock currently reports 25 dependency advisories | evidence: real `pnpm audit --prod --audit-level=low` on fixed commit | 建议: runtime risk record only, not timeless curated fact | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: scoped-canonical-tool-envelope | 可复用场景: Hermes tool execution、subagent adapter、审计 receipt | 是否建议 shared: yes, after second validation | 原因: 跨 Agent 横切，但必须先与 verification-first/effect-scope/subagent 四状态去重且不复制 DSH runtime
- [ ] 名称: document-ingestion-receipt | 可复用场景: Office/PDF/EPUB 到 Markdown 的 provenance、terminal、output cap | 是否建议 shared: yes, after second validation | 原因: 多 Agent 都需文档摄取，但必须证明隐私、现有能力 overlap、binary pin 与 error contract

### Candidate Open Questions

- [ ] 问题: Hermes 当前工具执行结果是否已有 canonical value 与 model projection 分离的稳定接口？ | reason: gap/adaptation | priority: high
- [ ] 问题: 如何把 monotonic guard 加在所有高权 Hermes tool 的最终 chokepoint，而不是只写在 prompt/Skill？ | reason: gap | priority: high
- [ ] 问题: DeepSeek Harness 25 个 audit findings 哪些可达默认 base/web/headless profile，哪些只在可选/test package？ | reason: security gap | priority: high
- [ ] 问题: Hermes read_file 对 DOCX/XLSX/PDF 的现有 parser、资源上限、隐私出口与 provenance contract 能否覆盖 anydoc 候选？ | reason: conflict/dedupe | priority: high
- [ ] 问题: anydoc issue #127 的 EPUB title-page 丢失能否由公开 fixture 复现，且如何表达 partial conversion？ | reason: gap | priority: medium
- [ ] 问题: 在 Rust 1.88+ 环境运行 anydoc `cargo test --locked`、fuzz smoke 与 cargo audit 的结果是什么？ | reason: blocked prerequisite | priority: medium

### 不应自动落地

- 不把 DeepSeek Harness 安装为 Hermes/OpenClaw 替代 runtime，不导入其 plugins、provider、credential 或 sandbox 配置。
- 不自动修复或升级 DSH dependency graph；audit findings 先做可达性、兼容性和 lockfile 审查。
- 不运行 `npx skills add firecrawl/anydoc`，不把 third-party SKILL.md 直接复制进 shared skills。
- 不把 anydoc 转换输出视为原件或 curated fact，不自动上传 OCR/hosted API。
- 不写明文 API key、token、password 或模型 credential；只允许变量名占位符。

## 证据与产物路径

- 本日报：`inbox/hermes/daily/2026-08-24-github-learning.md`
- 项目卡片：`runtime/hermes/github-learning/projects/deepseek-ai-deepseek-harness.md`、`runtime/hermes/github-learning/projects/firecrawl-anydoc.md`
- 经验累计：`runtime/hermes/github-learning/lessons.md`
- 审计状态：`runtime/hermes/github-hot-project-learning/status.json`
- 知识库目标：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-08-24-GitHub热门项目学习日报.md`
