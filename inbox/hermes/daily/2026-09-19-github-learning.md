---
type: case
status: archived
created: 2026-09-19
updated: 2026-09-19
domain: learning
tags: [github-learning, browser-automation, spec-driven-development, effect-verification, artifact-graph]
---

# 2026-09-19 GitHub 热门项目学习报告

> 执行者：Hermes；本次未调用 OpenClaw。  
> 查询时间：2026-09-19 07:31–07:45（UTC+08:00）。  
> 发现方式：真实抓取 GitHub Trending daily HTML，并用 GitHub Repository API 核验 Stars、Forks、Language、License、`updated_at` 与 `pushed_at`；Trending 只作发现入口。  
> 深读固定提交：`Tencent/BrowserSkill@fa953dc6fcd868827b93164e3bea26198e691224`；`Fission-AI/OpenSpec@bae58cf61479986431bb798acbe5a688a591c18c`。动态元数据与固定源码 revision 分开记录。  
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-09-19/`；源码浅克隆仅位于 `/tmp/github-learning-2026-09-19/`，没有写入 shared 的 core 层。

## 今日结论

**今天两项深读共同证明：Agent 系统不能把“命令返回成功”或“文件已经存在”直接投影成业务完成；应把副作用前置条件、结果确定性、语义验证和可恢复终态分别建模。BrowserSkill 用输入 readiness、session ownership 与 `effect_state` 降低浏览器静默假成功；OpenSpec 用 artifact DAG 和 archive merge builder 约束规划流，但当前 `validate` 仍可把 archive blocker 仅作为 INFO 并返回 0，说明 workflow 还需要 requirements→artifact→semantic checker→effect receipt 的闭环。**

### 今日真实验证摘要

- `Tencent/BrowserSkill`：根 Node 脚本与 browser eval harness 测试为 **22 passed / 0 failed**；执行 `wxt prepare` 后，extension 的 input-readiness/background-execution 定向测试为 **96 passed / 0 failed**。未启动真实 Chrome/Edge、未借用登录态 tab、未运行远程 gateway。
- BrowserSkill issue [#242](https://github.com/Tencent/BrowserSkill/issues/242) 报告 v0.2.1 后台窗口 click “exit 0 但页面无事件”；PR [#261](https://github.com/Tencent/BrowserSkill/pull/261) 已合并，v0.3.0 与当前源码新增 hidden-page readiness、paint flush、document revision 重验和 `effect_state`。issue 仍 open，评论也明确缺 Windows E2E 复验，因此“跨平台完全修复”仍**待核验**。
- `Fission-AI/OpenSpec`：锁定 pnpm 安装成功；artifact graph / archive preflight / requirement near-miss 定向测试为 **250 passed / 0 failed**；production `pnpm audit` 为 **0 known vulnerabilities**。
- OpenSpec 全仓测试真实结果为 **197 files passed / 1 file failed；5,743 tests passed / 1 failed / 1 skipped**。唯一失败是 root 环境可读取 `chmod` 后文件，导致权限 fixture 前置断言不成立；不能写成“全仓全绿”。
- 我在当前固定提交复现 issue [#1918](https://github.com/Fission-AI/OpenSpec/issues/1918) 的关键边界：不存在于 baseline 的 `MODIFIED` header，普通与 `--strict` 均输出 `Change 'fix-widgets' is valid`、exit 0，同时附一条 `INFO: Archive would refuse ... not found`。与 issue 所述旧版不同，当前 archive builder 已拒绝该操作，不再静默当 ADDED；但 validate verdict 仍会假绿给只看 exit code 的自动化。
- 两仓 Dependabot alerts endpoint 对当前 token 均返回 404；这不证明没有依赖漏洞。两仓公开 repository security advisories API 返回空数组，也不能覆盖依赖、未公开漏洞、release asset 或浏览器扩展商店制品。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 262,029 | 39,206 | JavaScript | MIT | 2026-09-18T22:59:58Z | 高热 skill 集合；今日不重复深读 |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | 146,271 | 23,783 | TypeScript | **NOASSERTION** | 2026-09-18T23:33:15Z | License API 未识别，不迁移源码 |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 96,380 | 10,189 | JavaScript | MIT | 2026-09-18T03:32:22Z | 技能集合，先做治理去重 |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | 69,328 | 4,750 | TypeScript | MIT | 2026-09-18T23:23:30Z | **深读：artifact DAG 与语义验证边界** |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 36,626 | 2,609 | Go | Apache-2.0 | 2026-09-18T14:24:55Z | 已于 09-17 深读，今日不重复 |
| [rustfs/rustfs](https://github.com/rustfs/rustfs) | 33,146 | 1,482 | Rust | Apache-2.0 | 2026-09-18T20:00:40Z | 对象存储，后续可观察 |
| [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) | 30,254 | 2,640 | TypeScript | MIT | 2026-09-18T22:02:30Z | 记忆系统，历史主题重叠 |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 13,578 | 727 | JavaScript | MIT | 2026-09-14T19:29:02Z | 已于 09-17 深读 |
| [Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill) | 5,266 | 365 | TypeScript | MIT | 2026-09-18T15:01:25Z | **深读：浏览器 authority 与 effect certainty** |
| [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | 3,942 | 405 | Python | MIT | 2026-09-18T22:21:53Z | 多用户多 Agent，自托管面较大 |

> Stars/Forks 是约 07:33 的 GitHub API 快照，会继续变化；License 仅是 repository API 根 SPDX，不覆盖依赖、模型、数据、扩展商店包和 release asset。`pushed_at` 表示任意 ref 更新，不等于 default branch 最新 commit 时间。未深读项目只作元数据筛选，不作能力或安全结论。

## 深读项目

### 1. Tencent/BrowserSkill

- **一句话判断**：值得学的不是“让 Agent 控制浏览器”，而是它把真实登录态浏览器建模为有 owner、session、borrow/return 生命周期、串行 effect queue 与不确定结果的高权资源；但浏览器/扩展/daemon/CLI 多版本组合、真实登录态和后台输入仍不能只靠 unit tests 宣告安全。
- **解决的问题**：替代让 Agent 直接共享整个浏览器 profile、依赖焦点窗口、把 CDP ACK 当业务成功、timeout 后盲重试，以及多 session 并发操作同一 tab 的旧做法。
- **URL / API 快照**：https://github.com/Tencent/BrowserSkill ；**Stars: 5,266 / Forks: 365 / Language: TypeScript / License: MIT**；`updated_at=2026-09-18T23:30:35Z`，`pushed_at=2026-09-18T15:01:25Z`，API `open_issues_count=52`（含 PR），default branch `main`。
- **固定提交**：[`fa953dc6fcd868827b93164e3bea26198e691224`](https://github.com/Tencent/BrowserSkill/commit/fa953dc6fcd868827b93164e3bea26198e691224)，committer time `2026-09-18T13:17:44Z`，`fix(bsk): support full-page screenshots of controlled background tabs` 合并提交。
- **Release / issue / checks 证据**：latest release [`cli-v0.3.0`](https://github.com/Tencent/BrowserSkill/releases/tag/cli-v0.3.0)，`published_at=2026-09-17T02:22:24Z`、`immutable=false`，6 个 assets 均有 GitHub API SHA-256 digest。固定 commit 的 5 个 checks 全为 success。issue #242 仍 open；PR #261 已于 09-16 合并，release notes列出 input readiness 修复。
- **来源交叉核验**：README、`docs/architecture.md`、`docs/operation-audit.md`、release API、issue #242、PR #261、固定源码、checks、pnpm/Cargo manifests、本机定向 tests。

#### 架构 / 实现与数据流

```text
Hermes / shell-capable harness
  -> bsk CLI
      -> JSONL over UDS / Windows named pipe
          -> local or server-mode daemon
              -> per-session queue + browser/session registries
                  -> WebSocket RPC to MV3 extension
                      -> ToolDispatcher
                          -> SessionManager + ref-store + BrowserDriver/CDP
                              -> dedicated Agent Window
                              -> explicitly borrowed user tab only

native input path
  -> resolve exact session-owned target
  -> acquire background execution
  -> read visibility + remember document revision
  -> hidden: enable focus emulation + force compositor surface
  -> recheck document revision
  -> resolve geometry + mark input sent + dispatch CDP input
  -> finally disable temporary focus emulation
  -> return effect_state: none | unknown | committed/confirmed result
```

关键区别是“窗口不抢焦点”不是“跳过 readiness”。target 由 session/tab ownership 决定，不由当前 UI focus 决定；hidden page 在 dispatch 前临时进入输入可用状态。timeout/cancel 若发生在输入发送前可报 `effect_state=none`，发送后丢 ACK 则必须保留 `unknown`，不能自动重试点击、上传或下载。

#### repo tree 摘要

固定 commit 有 **764 tracked paths**：

```text
BrowserSkill/
├── crates/
│   ├── bsk-cli/                    # Rust CLI、daemon、IPC、session queue、更新/安装
│   └── bsk-protocol/               # Rust wire types 与生成的 JSON Schemas
├── apps/extension/                 # WXT/MV3 扩展、CDP driver、tools、session manager
├── packages/
│   ├── dsh-plugin-browserskill/    # DeepSeek Harness adapter
│   ├── vom/                        # visual observation model/render layer
│   ├── i18n/ 与 ui/                # 公共 UI/i18n
├── evals/browser/                  # agent-neutral deterministic browser fixtures/oracles
├── skill/SKILL.md                  # shell-capable harness 的使用契约
├── docs/                           # architecture、audit、sandbox、remote、transfer
├── Cargo.toml / Cargo.lock         # Rust workspace，rust-version 1.85
├── package.json / pnpm-lock.yaml   # pnpm 10.17 workspace
└── install.sh / install.ps1        # release binary 安装面
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `apps/extension/src/tools/input-readiness.ts` | hidden-page 输入前置与结果分级 | visibility、focus emulation、surface flush、revision 重验、`effect_state` 与 cleanup |
| `apps/extension/src/tools/background-execution.ts` | page tool 前统一 target/control gate | 只为 exact session-owned Agent Window tab 准备后台执行；失败显式 `cdp_failed` |
| `crates/bsk-cli/src/daemon/queue.rs` | per-session 串行与 cancellation reconciliation | stop 前关闭 admission；request/cancel wire order；deadline 后 bounded cleanup |
| `crates/bsk-protocol/src/tools/tabs.rs` | borrow/return wire contract | user/agent/all scope；原 window/index；browser setting 是确认 authority |
| `apps/extension/src/tools/__tests__/interaction.test.ts` | input readiness adversarial tests | hidden/visible、cancel、paint failure、document replacement、cleanup failure |
| `docs/operation-audit.md` | 审计语义边界 | session ended 不等于业务完成；unknown/partial/interrupted 不得推断 success |
| `evals/browser/lib/oracle.mjs` | 外部 effect oracle | 将 adapter transcript 与页面真实状态验证分开 |

#### ⭐ 源码精读

**代码块 1：`withInputReady()` 把 input readiness 和 effect certainty 包在一次 action 外。**

```ts
export async function withInputReady<T extends object>(
  ctx: SessionContext,
  tabId: number,
  deps: InputReadinessDeps,
  action: (input: ReadyInput) => Promise<T | RpcError>,
): Promise<T | RpcError> {
  const documentRevision = ctx.refStore.documentRevision(tabId);
  let restoreFocus = false;
  let inputSent = false;
  // ... visibility/readiness ...
  if (ctx.refStore.documentRevision(tabId) !== documentRevision) {
    result = { code: "not_found", message: "Document changed while preparing input; observe again",
      data: { reason: "ref_not_found", effect_state: "none" } };
  } else {
    result = await action({ hidden: restoreFocus, markSent: () => { inputSent = true; } });
  }
}
```

逻辑摘要：先绑定 document revision，再准备 renderer，最后在 effect 之前复核；`markSent()` 将错误语义从“确定没发生”切到“可能发生”。这比只返回 click coordinate 或 CDP command ACK 更接近真实副作用语义。边界：页面业务逻辑可能异步拒绝 click，仍需 DOM/server read-back；`effect_state` 不是目标完成证明。

**代码块 2：hidden page readiness 使用 focus emulation + surface capture，而不抢用户前台窗口。**

```ts
if (visibility.result.value === "hidden") {
  attachmentId = deps.cdp.getAttachmentId?.(tabId);
  restoreFocus = true;
  await deps.cdp.send(tabId, "Emulation.setFocusEmulationEnabled", { enabled: true });
  await flushInputRendering(deps.cdp, tabId, deps.signal, deps.deadline);
}
// finally: only clear the override on the same attachment
await deps.cdp.send(tabId, "Emulation.setFocusEmulationEnabled", { enabled: false });
```

逻辑摘要：它不通过 `Page.bringToFront` 抢用户焦点，而是临时启用 focus emulation，并读取 surface 强制 compositor frame；cleanup 前检查 attachment identity，避免 navigation/replacement 后误改新 target。边界：本机只跑 mock/happy-dom tests，没有 Windows + Chromium + DPR 1.5 真实 E2E，因此 issue #242 的跨平台闭环待核验。

**代码块 3：`dispatch_after_closing()` 让 session stop 成为队列最后一个受控 effect。**

```rust
pub async fn dispatch_after_closing(
    &self, sid: &SessionId, method: Method, params: Value,
    timeout: Duration, cancel: Option<AbortToken>,
) -> Result<Value, DispatchError> {
    let (sender, state) = {
        let mut guard = self.queues.lock().expect("tool queue registry poisoned");
        let entry = guard.get_mut(sid).ok_or(DispatchError::SessionNotFound)?;
        if !entry.accepting { return Err(DispatchError::SessionStopping); }
        entry.accepting = false;
        (entry.sender.clone(), Arc::clone(&entry.state))
    };
    dispatch_with_sender(sender, state, sid.clone(), method, params,
                         timeout, true, None, cancel, timeout).await
}
```

逻辑摘要：session stop 先停止新 admission，再排到已接收操作之后，避免 teardown 与 snapshot/get_html 等 in-flight 工具竞争。deadline/cancel 还会保留 bounded compensation window。边界：这是进程内 session 队列，不是跨 daemon 的分布式事务；browser crash 或 transport loss 仍会产生 unknown/interrupted。

**代码块 4：tab borrow contract 保存原位置，并拒绝由 CLI legacy flag 覆盖浏览器侧策略。**

```rust
pub struct TabBorrowParams {
    pub confirmation_timeout_ms: Option<u32>,
    pub tab_id: i64,
    pub session_id: String,
    /// Legacy input, ignored. Browser settings decide whether confirmation is required.
    pub confirm: Option<bool>,
}

pub struct TabBorrowResult {
    pub tab_id: i64,
    pub original_window_id: i64,
    pub original_index: i32,
    pub agent_window_id: i64,
}
```

逻辑摘要：borrow 是显式 lease，不是“看到 tab 就拥有”；返回结果保留 recovery 所需原 window/index。用户浏览器设置才是确认 authority，deprecated CLI 参数不能降权。边界：用户关闭确认后仍必须依赖上层 task authorization；同 OS account 下恶意进程也不是安全隔离边界。

#### 依赖分析与供应链风险

- Rust workspace 有 3 个 Cargo manifests；关键依赖含 Tokio、tokio-tungstenite、Serde/Schemars、Reqwest(rustls)、Clap、Nix、zip/tar/flate2、SHA-2。协议、网络、压缩包、更新器与本地 IPC 都是供应链/解析攻击面。
- pnpm workspace 有 6 个 package manifests、约 57 组声明依赖；extension 生产依赖含 React 19、内部 i18n/ui/vom；构建面含 WXT、Vite、Vitest、Tailwind、Biome、Stylelint。`pnpm audit --prod` 今日为 0 known vulnerabilities，但只覆盖锁文件可识别的 npm advisory。
- `pnpm-lock.yaml` 已固定；release API 6 个 assets 都有 digest，但 release `immutable=false`。今日未下载/执行 release binary，也未验证商店 extension bytes 与源码对应关系。
- 本机 Cargo/Rustc 当前不可用，Rust build/test blocked；只验证了 Node/eval 与 extension 定向 tests。公开 advisories 空、Dependabot 404 都不能补足 RustSec、浏览器扩展权限和 release provenance。

#### 可复用经验

- 当 Agent 要操作真实登录态 browser/tab 时，应优先把 tab 绑定到 session owner，并使用显式 borrow/return lease，因为“用户已登录”不是对整个 profile 的持续授权；边界是浏览器设置也不能替代任务级授权。
- 当 timeout/cancel 可能发生在副作用 dispatch 前后时，应优先返回 `none | unknown | committed/confirmed` 并对 unknown 做 read-only reconcile，因为 ACK 丢失后盲重试会重复 click/upload/download；边界是 read-back 必须读取业务权威状态而非同一 adapter 的缓存。
- 当后台页面输入不应打断用户时，应优先建立 renderer readiness、document identity 与 cleanup，而不是依赖当前窗口 focus 或强制 bring-to-front；边界是不同 browser/OS/DPR 必须做真实 E2E matrix。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/effect-certainty-envelope-v0/` 建纯 Python synthetic state machine：输入 `target_revision`、`dispatch_phase`、`ack`、`authoritative_readback`，输出 `not_started | unknown | committed | rejected` 与 `retry_allowed`。fixture 覆盖：(1) dispatch 前 timeout 可重试；(2) dispatch 后 ACK 丢失禁止重试；(3) target revision 变化先 blocked；(4) read-back 证实 effect 后 committed。只使用 synthetic browser records，不安装 BrowserSkill、不读取 cookie、不启动 daemon。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 MIT；可抽象机制。依赖、Chrome/Edge APIs、商店制品、release binary 与用户页面内容需独立审计。
- **维护活跃度**：固定 commit 是 09-18 的提交；latest release 09-17，main 与 release 已有差异。高频更新意味着 protocol/CLI/extension staggered version 风险高。
- **安全风险**：真实登录态、页面正文、下载/上传、remote WSS、device pairing、daemon、安装器和 skill 都是 authority surfaces。loopback 不等于授权；remote pairing 不等于每次 task consent。
- **隐私风险**：官方 audit 默认关闭且声明不保存正文/输入值，但 daemon logs、页面 provider、远程 gateway、extension permissions 和用户导出的 audit JSON 仍需单独治理。
- **局限性**：session 隔离是 BrowserSkill runtime 内的 ownership，不是 OS/browser-profile 强隔离；audit 状态“已结束”不代表用户业务目标完成。
- **验证局限**：未跑 Rust tests、真实 browser E2E、remote gateway、file transfer、borrow approval、商店 extension 或 release binary。issue #242 虽代码与定向 tests显示已修，reporter 复验仍待核验。

#### ⭐ Skill 升格判断

**需二次验证。** 不直接安装上游 `skill/SKILL.md`，不创建第二套 browser skill。只提出 agent-neutral `effect-certainty-envelope` 候选，并与现有 verification-first、effect-scope、completion receipt、BrowserSkill/Hermes 原生能力去重；先通过 synthetic fixture 与真实 browser adapter conformance，才考虑更新 shared skill。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/effect-certainty-envelope-v0/`，输出 `attempt.json`、`effect-receipt.json`、`reconcile.json`。
2. Hermes tool adapter：在 browser/terminal 等有副作用工具的宿主 adapter 统一记录 `target_revision`、`dispatch_state`、`effect_state`、`readback`，模型 prose 不得覆盖状态。
3. shared workflow：若 POC 通过，优先迭代现有 verification/completion contract，加入 `unknown => no blind retry`；共享根仍通过 `scripts/resolve_shared_root.py` 解析。
4. 审计：将“工具 success”与“业务 postcondition read-back”拆成两条证据；无 read-back 时只能 partial/needs_verification。
5. 不修改 Hermes/OpenClaw 配置、provider、cron 或 secret；当前 OpenClaw runtime 不存在，本次没有调用或写入其 runtime。

---

### 2. Fission-AI/OpenSpec

- **一句话判断**：OpenSpec 值得学的是把需求规划拆成 schema-driven artifact DAG，并用确定性 CLI 给 Agent 返回 ready/blocked/done 与路径；但当前“文件存在即 artifact done”和“archive blocker 只是 validate INFO”揭示了结构完成、语义有效与可执行完成仍是三个不同状态。
- **解决的问题**：替代需求只存在 chat history、一次生成全部文档、硬编码 workflow、不同 Agent 各复制一套 prompt，以及实施过程中无法回改 spec 的旧做法。
- **URL / API 快照**：https://github.com/Fission-AI/OpenSpec ；**Stars: 69,328 / Forks: 4,750 / Language: TypeScript / License: MIT**；`updated_at=2026-09-18T23:31:08Z`，`pushed_at=2026-09-18T23:23:30Z`，API `open_issues_count=234`（含 PR），default branch `main`。
- **固定提交**：[`bae58cf61479986431bb798acbe5a688a591c18c`](https://github.com/Fission-AI/OpenSpec/commit/bae58cf61479986431bb798acbe5a688a591c18c)，committer time `2026-09-17T06:31:19Z`，`docs: fix Docslab links to unfinished pages (#1903)`。
- **Release / issue / checks 证据**：latest release [`v1.13.1`](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.13.1)，`published_at=2026-09-17T01:11:07Z`、`immutable=false`、0 assets，target commit `634c557...`。固定 commit checks 中 Linux/macOS/Windows、lint/typecheck 和 CodeQL 已成功；部分 job 因矩阵/路径条件 skipped，cloud scan neutral。issue #1918 仍 open，无评论。
- **来源交叉核验**：README、`docs/opsx.md`、release API、issue #1918、artifact graph / resolver / state / output / validator / merge builder 源码、tests、checks、本机 CLI reproduction 与 tests。

#### 架构 / 实现与数据流

```text
project config / change metadata / CLI --schema
  -> resolve schema precedence
      project openspec/schemas > user data schemas > package schemas
  -> parse schema.yaml
      artifacts: id + requires + generates + template
  -> ArtifactGraph
      deterministic topological order + ready/blocked calculation
  -> loadChangeContext
      detect outputs on filesystem -> completed set
      optional skip_specs -> explicit skipped set
  -> generateInstructions
      context + per-artifact rules + template + dependency paths
  -> Agent writes proposal/specs/design/tasks
  -> validate
      shape/semantic checks + advisory archive-builder dry run
  -> apply/update/sync/archive
      merge delta into canonical main specs
```

Artifact DAG 是 enablement，不是强制线性 phase：proposal 完成后 specs/design 可并行 ready，tasks 依赖两者；Agent 可 update 既有 artifact。可靠性核心在 CLI 结构化状态，而不是 slash command prose。但 `detectCompleted()` 只检测至少一个 output file 存在，后续 semantic validation 是独立层；自动化若只看 status 或 validate exit 0，仍会假完成。

#### repo tree 摘要

固定 commit 有 **1,221 tracked paths**：

```text
OpenSpec/
├── src/
│   ├── core/artifact-graph/        # schema、DAG、state、output、instruction loader
│   ├── core/validation/            # spec/change validators 与 findings
│   ├── core/parsers/               # Markdown/delta/change parsers
│   ├── core/specs-apply.ts         # delta -> canonical spec merge truth
│   ├── commands/                   # validate/status/archive/store/schema/workflow CLI
│   └── telemetry/                  # opt-out 与匿名 command/version stats
├── schemas/                        # built-in workflow schemas/templates
├── skills/ + .agents/              # 30+ harness 的生成/通用入口
├── openspec/                       # 本项目自己的 specs 与 changes
├── test/                           # 198 files，含 security/path/adapter/e2e fixtures
├── docs/ + website/                # OPSX、stores、tool support 文档站
├── bin/openspec.js                 # CLI entry
├── package.json / pnpm-lock.yaml   # Node >=20.19，pnpm 10.34.5
└── LICENSE                         # MIT
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/core/artifact-graph/graph.ts` | DAG engine | Kahn sort、declaration-order tie break、ready/blocked/complete |
| `src/core/artifact-graph/state.ts` | artifact completion detector | output path/glob 只要存在文件即 completed |
| `src/core/artifact-graph/outputs.ts` | output path boundary | canonical containment、symlink traversal/cycle guard、deterministic matches |
| `src/core/artifact-graph/resolver.ts` | schema resolution | project > user > package；拒绝绝对/遍历名；支持安全 symlink dir |
| `src/core/artifact-graph/instruction-loader.ts` | Agent-facing structured context | schema + completed + skipped + context/rules/template + dependencies |
| `src/core/specs-apply.ts` | archive merge semantic truth | exact MODIFIED match、near-miss、scenario loss、ADDED collision、early sync |
| `src/core/validation/validator.ts` | validate verdict | 结构检查后复用 merge builder，但 archive blockers 当前仅 INFO |
| `test/core/validation.archive-preflight.test.ts` | validate/archive parity fixtures | 明确测试 blocker 是 INFO 且不改变 verdict |

#### ⭐ 源码精读

**代码块 1：`ArtifactGraph.getBuildOrder()` 用 declaration order 解决合法 DAG 的稳定 tie。**

```ts
getBuildOrder(): string[] {
  const inDegree = new Map<string, number>();
  const dependents = new Map<string, string[]>();
  for (const artifact of this.artifacts.values()) {
    inDegree.set(artifact.id, artifact.requires.length);
    dependents.set(artifact.id, []);
  }
  const queue = [...this.artifacts.keys()]
    .filter(id => inDegree.get(id) === 0)
    .sort((a, b) => this.compareByDeclarationOrder(a, b));
  // Kahn: each newly ready node joins queue, then whole queue re-sorts
  return result;
}
```

逻辑摘要：同层 `specs`/`design` 都依赖 proposal 时，字母排序会违背 schema 作者声明顺序；代码用声明位置做稳定 tie-break。可迁移点是“DAG 给可行集合，policy 给稳定建议顺序”。边界：拓扑顺序不代表 artifact 内容有效，也不自动防 cycle；schema parser 的 cycle validation需独立存在。

**代码块 2：`detectCompleted()` 明确显示“存在性”只是一个窄状态。**

```ts
export function detectCompleted(graph: ArtifactGraph, changeDir: string): CompletedSet {
  const completed = new Set<string>();
  if (!fs.existsSync(changeDir)) return completed;
  for (const artifact of graph.getAllArtifacts()) {
    if (isArtifactComplete(artifact.generates, changeDir)) completed.add(artifact.id);
  }
  return completed;
}

function isArtifactComplete(generates: string, changeDir: string): boolean {
  return artifactOutputExists(changeDir, generates);
}
```

逻辑摘要：状态检测可快速恢复，不维护易漂移数据库；`outputs.ts` 还做 canonical containment 和 symlink cycle guard。关键边界是空壳、语义错误、过期文件也会被视为 done，所以 downstream apply 前必须有 validator/coverage gate；不能把 DAG done 直接映射 completed。

**代码块 3：archive merge builder 对 MODIFIED 做 exact baseline lookup。**

```ts
for (const mod of plan.modified) {
  const key = normalizeRequirementName(mod.name);
  const currentBlock = nameToBlock.get(key);
  if (!currentBlock) {
    throw new Error(
      `${specName} MODIFIED failed for header "### Requirement: ${mod.name}" - not found`
    );
  }
  const missingScenarios = findMissingCurrentScenarios(currentBlock, mod);
  if (missingScenarios.length > 0) throw new Error(/* refuse scenario loss */);
  nameToBlock.set(key, mod);
}
```

逻辑摘要：当前 main 已不会把 typoed MODIFIED 静默当新增；它还拒绝 scenario loss。与 issue #1918 的 v1.5.0 描述相比，这是实质改进。边界：这段抛错只在调用者把它升级为 hard verdict 时才有效；当前 validate adapter 将该错误降成 INFO。

**代码块 4：`findArchiveBlockers()` 复用了 truth function，却有意不改变 validate verdict。**

```ts
try {
  await buildUpdatedSpec(update, changeName, { silent: true });
} catch (error) {
  if ((error as NodeJS.ErrnoException)?.code !== undefined) continue;
  issues.push({
    level: 'INFO',
    path: entryPath,
    message: `Archive would refuse this delta: ${error instanceof Error ? error.message : String(error)}`,
  });
}
```

逻辑摘要：好处是 validation 与 archive 不复制 merge rules；filesystem error 不冒充 semantic conflict。问题是 deterministic blocker 也只记 INFO，而 `createReport()` 在普通和 strict mode 都不让 INFO 影响 `valid`，因此 CLI exit 0。今日当前源码复现为 `valid + INFO + RC 0`。边界：可能存在 sibling unarchived change，所以直接 hard-fail 需引入显式 baseline/dependency marker，而不是粗暴把所有 INFO 变 ERROR。

#### 依赖分析与供应链风险

- 根 `package.json` 要求 Node `>=20.19.0`、pnpm `10.34.5`；生产依赖是 Inquirer、Chalk、Commander、cross-spawn、diff、fast-glob、Ora、YAML、Zod。关键风险面是 shell/process、glob/path、YAML/schema、全局安装和生成各 harness skills。
- 锁定安装解析 237 packages；`pnpm audit --prod` 为 0 known vulnerabilities。完整测试安装/生成会写大量临时目录与 harness fixtures，但今日未全局安装 OpenSpec、未在 shared hub 执行 init/update/archive。
- release `v1.13.1` 无二进制 assets，npm package 是主要发布面；release `immutable=false`。今日验证的是 source checkout + lockfile，不是 npm registry tarball 的 provenance/签名。
- full suite 唯一失败是 root 可绕过 DAC 导致 unreadable fixture 失真；这不是已证实产品 regression，但证明权限测试必须覆盖 root/non-root。Dependabot 404 和公开 advisory 空不能证明无未知漏洞。

#### 可复用经验

- 当 workflow 用文件存在性恢复进度时，应优先把 `present`、`schema_valid`、`semantically_valid`、`verified_against_baseline` 分开，因为一个 Markdown 文件存在只证明 artifact path 有对象；边界是每层 checker 都要固定 revision 与覆盖范围。
- 当 validate 与最终 apply/archive 使用不同规则时，应优先复用同一个 sans-I/O truth function，并明确 blocker 的 verdict 映射，因为“复用逻辑但降成 INFO”仍会让只看 exit code 的自动化假绿；边界是 concurrent baseline 要用 dependency/revision 表达。
- 当 DAG 有多个 ready 节点时，应优先用 schema declaration order 提供确定性建议，同时保留 ready set，因为 deterministic UX 不应把建议顺序误写成强制 phase；边界是最终业务依赖仍需 acceptance coverage。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/artifact-semantic-state-v0/` 用 4 个 synthetic artifacts 实现 `missing | present | invalid | verified | stale`；DAG readiness 只接受依赖为 `verified`，并模拟 baseline revision 变化将 verified 降为 stale。验证：(1) 空文件不是 done；(2) validator INFO blocker 不可投影为 completed；(3) sibling change 缺 dependency marker 时返回 needs_validation；(4) projection 从 canonical state 生成。无需安装 OpenSpec，不修改 shared core。

#### 风险边界

- **License**：GitHub API、package manifest 与根 LICENSE 均为 MIT；可抽象机制。npm 依赖、community schema、生成的第三方 harness adapter 和用户 specs 内容需独立合规。
- **维护活跃度**：latest release 与固定 commit 都在 09-17；API pushed_at 09-18 可能来自其他 ref。快速演进且 stores 仍 beta，schema/CLI/skill contract 可能变化。
- **安全风险**：project-local schema/config/template 是 authority surface，可影响 Agent instructions 和输出路径；global install/update、cross-spawn、community schemas 与 generated skills 都需 pin/dry-run/diff/read-back。
- **隐私风险**：README 声明 telemetry 仅 command/version、CI 自动关闭，可通过 `OPENSPEC_TELEMETRY=0`/DNT 关闭；今日未抓包验证，仍不能外推为绝无元数据泄漏。
- **局限性**：artifact file presence 不等于内容有效；validation INFO 不改变 exit code；spec 与实现一致性仍依赖 Agent/human verify；DAG 不能替代 requirement coverage 或真实 E2E。
- **验证局限**：未验证 npm tarball、全局安装、30+ real harnesses、stores remote、Nix、Windows/macOS 本机。全仓在 root 下 1 个权限 fixture失败；non-root 复验待核验。

#### ⭐ Skill 升格判断

**需二次验证。** Artifact DAG / declaration-order / validator-archive parity 可迁移，但不安装完整 OpenSpec，也不复制其 generated skills。候选应先与现有 autonomous-learning plan、verification-first、shared skill governance 和 completion receipt 去重；更可能是更新现有 workflow/checker，而不是创建 `openspec` 专属 shared skill。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/artifact-semantic-state-v0/`；canonical JSON 包含 `artifact_id/source_revision/presence/schema/semantic/baseline/terminal`。
2. GitHub learning orchestrator：把当前 Markdown keyword audit 升级为 requirements→evidence manifest，报告存在只算 present；API evidence、源码路径、测试 receipt 分别验证。
3. shared plans：长任务 plan 的 step 状态拆为 `ready/in_progress/blocked/present/verified/stale/completed`，只有 verified acceptance 可以解锁最终 completed。
4. deterministic checker：finalize 前复用实际 apply/merge truth function；若 checker 只给 INFO，必须在状态中保留 `needs_validation`，禁止自动投影 completed。
5. 所有新增 runtime 路径通过 shared root resolver 拼接；不自动执行 `openspec init/update`，不覆盖 Hermes skills，不改 OpenClaw 或 future-agent workspace。

## 经验沉淀

1. 当 Agent 工具会产生不可安全重放的副作用时，应优先在 dispatch 前后切换 `none/unknown/committed` 并用权威 read-back 收口，因为 exit 0、RPC ACK 或 coordinate 只证明 transport/dispatch；边界是 read-back 也必须绑定 exact target revision。
2. 当 workflow 以 artifact 文件恢复进度时，应优先把 presence、schema、semantic、baseline verification 和 business acceptance 分层，因为文件存在既不能证明内容正确，也不能证明实现完成；边界是状态转换应由 checker 而不是 Agent prose授权。
3. 当 validator 与最终 apply/archive 有共同语义时，应优先复用一个 truth function，并审计 adapter 如何映射 severity/exit/status，因为共享函数仍可能被上层降级成假绿 INFO；边界是并行 change 需要显式 dependency/revision。
4. 当多个任务共享浏览器、workspace 或 artifact graph 时，应优先使用 immutable session/change identity、owner 与 scoped queue/lock，因为 focus、路径、display name 或当前进程都不是稳定 authority；边界是进程内隔离不是 OS 安全边界。
5. 当真实效果难以在 unit test 中验证时，应优先把 synthetic/unit、browser E2E、cross-platform、release artifact 与 user read-back 分开报告，因为一层绿色不能覆盖另一层未知；边界是 open issue/reporter confirmation 仍是外部证据，不可伪造。
6. 当 DAG 允许多个 ready 项时，应优先同时返回 ready set 与 deterministic recommendation，因为并行能力和可预测 UX可以共存；边界是 declaration order 是 policy，不是依赖事实。

## 明日继续

1. 在 runtime 创建一个合并实验 `verified-artifact-effect-envelope-v0`：artifact 状态到 effect receipt 的纯 fixture，不连接 browser/provider。
2. 给 GitHub-learning audit 设计 requirements→evidence manifest 草案：每个硬性要求绑定 evidence type、source revision、checker 和 terminal，不再仅扫描关键词。
3. 若可获得非 root shell，复验 OpenSpec 唯一权限 fixture；若有隔离 Chromium，再复验 BrowserSkill hidden click，但禁止读取真实 cookie/账号。
4. 继续跟踪 OpenSpec #1918 的 verdict 设计和 BrowserSkill #242 reporter 在 v0.3.0 的复测，不把 issue open/close 单独当修复证明。

## 候选反哺

### Candidate Facts

- [ ] topic: effect certainty 必须区分 dispatch 前后 | evidence: BrowserSkill `input-readiness.ts`、`queue.rs`、96 定向 tests、issue #242/PR #261 | 建议: update verification/completion fact | 安全级别: medium
- [ ] topic: artifact presence 不等于 semantic completion | evidence: OpenSpec `state.ts`、`outputs.ts`、当前 CLI #1918 reproduction | 建议: update autonomous-learning/project workflow | 安全级别: low
- [ ] topic: shared truth function 仍需审计 verdict adapter | evidence: `buildUpdatedSpec()` hard reject vs `findArchiveBlockers()` INFO + exit 0 | 建议: create candidate, not active fact | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: verified-artifact-effect-envelope | 可复用场景: browser/tool effects、长任务 artifact、审计闭环 | 是否建议 shared: yes（仅候选） | 原因: 跨 Hermes/future agent 可复用，但需先与 verification-first/completion receipt 去重并跑 fixtures
- [ ] 名称: github-learning requirements-evidence manifest | 可复用场景: 每日研究审计 | 是否建议 shared: yes（优先更新现有 workflow） | 原因: 当前审计偏关键词，无法证明来源、revision 与代码块的真实绑定

### Candidate Open Questions

- [ ] 问题: `effect_state=unknown` 的最小跨工具 read-back 接口是什么？ | reason: adaptation | priority: high
- [ ] 问题: 并行 change 未归档时，OpenSpec archive blocker 应何时从 INFO 升为 hard failure？ | reason: conflict | priority: medium
- [ ] 问题: BrowserSkill v0.3.0 在 Windows + DPR 1.5 + hidden Agent Window 是否真实修复？ | reason: gap | priority: high
- [ ] 问题: 如何让 artifact DAG 只由 verified artifact 解锁，同时不牺牲轻量恢复？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动安装 BrowserSkill/OpenSpec，不下载或执行 release assets，不加载真实 browser profile。
- 不自动改 Hermes/OpenClaw 配置、model、provider、cron、skills 或 secret；当前 OpenClaw runtime 不存在且本次未调用。
- 不直接写 curated active fact 或创建 shared skill；本报告与候选需二轮治理、去重和人工审查。
- 不把 GitHub API License、公开 advisories 空、npm audit 0、CI success 或 unit tests外推成完整供应链/部署安全。
- 不把 BrowserSkill operation audit 的“已结束”、OpenSpec artifact 的“done”或 validate exit 0 当业务完成。
