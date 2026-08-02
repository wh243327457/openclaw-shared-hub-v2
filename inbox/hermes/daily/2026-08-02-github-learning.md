# 2026-08-02 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> 研究时间：2026-08-01T23:31–23:40Z（北京时间 2026-08-02T07:31–07:40+08:00）  
> 发现来源：真实抓取 `https://github.com/trending?since=daily`，并用 GitHub Search API 查询 `created:>2026-07-01 stars:>200`；项目元数据均以 `gh api repos/{owner}/{repo}` 单仓复核。  
> 固定源码快照：`unicity-aos/aos-ce@1ffa80da3e19862bea2b5d3b3519a60ac5e12ea2`、`yc-software/qm@7f2c916360f1797a8ff2a77ce2ce40c5fabab087`。  
> 数据边界：Stars、forks、updated 会继续变化；本文数值只代表上述 API 查询窗口。GitHub repo-level License 不能替代依赖、数据、模型、商标和发布制品的独立审查。

## 今日结论

今天的主线是：**多 Agent 系统不能只靠 prompt 表达权限和共享语义；应把“身份/作用域解析、确定性 policy、最终副作用 chokepoint、结构化状态、审计和投影”分层，并明确每条 gate 在失败时究竟是 fail-closed、fail-open 还是退回更底层的硬边界。** `aos-ce` 展示了 capability PEP 之上的同源双平面 PDP、可信 ingress 与审批状态；`qm` 展示了 org floor + scope tightening、durable scoped workspace、外部内容筛查和 skill pack 同步。对 Hermes/shared hub 最有价值的不是安装两个新平台，而是抽象 **authority-plane map** 与 **scope-resolution conformance fixtures**。

## 证据与执行摘要

- **Trending**：`curl` 保存真实 HTML 到 `runtime/hermes/github-hot-project-learning/trending-2026-08-02.html`，文件为 632,588 bytes；解析到 `microsoft/AI-For-Beginners`、`github/copilot-sdk`、`github/gh-stack`、`iv-org/invidious`、`bytedance/deer-flow` 等候选。
- **增长项目补充发现**：GitHub Search API 的新仓库高星结果包含 `xai-org/grok-build`、`andrewyng/openworker`、`openai/codex-security`、`unicity-aos/aos-ce`、`yc-software/qm` 等。为避免连续重复，今日未再深读 7 月 28–30 日已经分析过的 grok-build/openworker/codex-security。
- **API 原始证据**：Trending 速览候选的 Repository API JSON 保存在 `runtime/hermes/github-hot-project-learning/api/2026-08-02/`；深读仓库又单独执行了 metadata、license、release、issues/pulls、commits API。
- **源码**：两个深读仓库均 `git clone --depth 1`，固定 commit 分别为 `1ffa80d...`、`7f2c916...`；tracked paths 分别为 360、1,264，写报告前工作树均干净。
- **交叉来源**：两个深读项目均核验 README、docs/SECURITY、release、issues/PR、依赖清单和关键源码，不以 README 单独支撑实现结论。
- **真实执行**：AOS 因本机没有 `cargo/rustc`，`cargo test -p aos-mcp-broker` 真实返回 exit 127，编译与 WASM/runtime 行为待核验。QM 执行 `npm ci` 后，以 `npx --yes node@24.15.0` 跑 4 个定向 test files，真实结果 **23 pass / 0 fail**；`npm audit --omit=dev --package-lock-only` 返回 **0 known vulnerabilities**，但不是安全证明。
- **权限边界**：Dependabot alerts API 对两个公开仓库均返回 403（当前 token 无权读取），所以 alert 状态明确标为**待核验**，不写“无漏洞”。

## 项目速览

### A. GitHub Trending daily（Repository API 复核）

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [microsoft/generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners) | 114,188 | 61,215 | Jupyter Notebook | MIT | 2026-08-01T23:38:54 / 08:23:49 | 高热教程，留给教程学习 lane |
| [microsoft/AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners) | 57,133 | 11,335 | Jupyter Notebook | MIT | 2026-08-01T23:40:43 / 2026-07-21T11:11:48 | 教程型，不替代源码机制深读 |
| [iv-org/invidious](https://github.com/iv-org/invidious) | 21,604 | 2,430 | Crystal | AGPL-3.0 | 2026-08-01T23:38:33 / 22:55:47 | 活跃但 AGPL 与代理服务边界高 |
| [paperswithbacktest/awesome-systematic-trading](https://github.com/paperswithbacktest/awesome-systematic-trading) | 12,227 | 1,514 | Python | NOASSERTION | 2026-08-01T23:41:12 / **2025-01-22T07:49:32** | awesome 列表，pushed 较旧且 license 未识别 |
| [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 11,872 | 1,795 | PowerShell | MIT | 2026-08-01T23:39:24 / 23:12:25 | 逆向/skill 攻防面高，不自动运行 |
| [abus-aikorea/voice-pro](https://github.com/abus-aikorea/voice-pro) | 11,729 | 1,716 | Python | GPL-3.0 | 2026-08-01T23:34:03 / 2026-07-13T01:28:10 | 模型/媒体/桌面依赖需专项审查 |
| [github/copilot-sdk](https://github.com/github/copilot-sdk) | 10,270 | 1,385 | Java | MIT | 2026-08-01T23:07:37 / 12:57:47 | 多语言 SDK 候选，今日不扩大范围 |
| [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech) | 10,192 | 1,248 | Python | Apache-2.0 | 2026-08-01T23:40:33 / 2026-07-31T23:14:20 | 实时语音链路，需 GPU/模型 license 验证 |
| [usekaneo/kaneo](https://github.com/usekaneo/kaneo) | 5,664 | 483 | TypeScript | MIT | 2026-08-01T23:33:07 / 2026-07-30T20:03:43 | 项目管理候选，和今日权限主线较弱 |
| [github/gh-stack](https://github.com/github/gh-stack) | 805 | 36 | Go | MIT | 2026-08-01T23:37:11 / 2026-07-31T00:36:50 | 小而活跃，适合后续 CLI 工作流研究 |

### B. 近期增长项目补充（深读对象）

| 项目 | Stars | Forks | Language | License（GitHub API） | Created / Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [unicity-aos/aos-ce](https://github.com/unicity-aos/aos-ce) | **8,577** | 16 | Rust | **Apache-2.0** | 2026-07-12 / 2026-08-01T15:51:59 / 2026-07-31T23:07:02 | **深读：双平面 policy、可信 ingress、approval/grant 状态** |
| [yc-software/qm](https://github.com/yc-software/qm) | **4,911** | 484 | TypeScript | **MIT** | 2026-07-29 / 2026-08-01T23:32:21 / 01:30:53 | **深读：scope resolution、security posture、skill pack 同步** |

说明：`aos-ce` 的 GitHub License API 返回 `Apache-2.0` 并指向 `LICENSE-APACHE`；仓库 README 和 workspace metadata 明确根代码是 `MIT OR Apache-2.0` 双许可证。本文同时保留 API 值与仓库自述，不把二者混成单值。Stars 不是安全性、成熟度或真实采用率证明。

## 深读项目

### 1. unicity-aos/aos-ce

**基本信息（GitHub API）**

- URL：https://github.com/unicity-aos/aos-ce
- Stars：**8,577**；Forks：**16**；Language：Rust；GitHub License API：**Apache-2.0**。
- 创建：2026-07-12T23:39:52Z；updated：2026-08-01T15:51:59Z；pushed：2026-07-31T23:07:02Z；`open_issues_count=26`（含 PR，不能解释为 26 个缺陷）。
- 固定 commit：[1ffa80da3e19](https://github.com/unicity-aos/aos-ce/commit/1ffa80da3e19862bea2b5d3b3519a60ac5e12ea2)，时间 2026-07-31T23:07:01Z，message `License AOS Community Edition (#79)`。
- 最新 GitHub Release：[2026.1.3](https://github.com/unicity-aos/aos-ce/releases/tag/2026.1.3)，published 2026-07-20T14:06:03Z；固定 commit 比 release 新。
- License API 还返回 `LICENSE-APACHE`；README/Cargo workspace 则声明 `MIT OR Apache-2.0`。这是仓库级双许可，依赖和分发制品仍需独立审查。

#### 一句话判断

值得学的不是“Agent OS”命名，而是它明确区分 **底层 capability PEP、MCP broker 进程内 PDP、native-tool hook PDP、可信 ingress、grant/approval pending 状态和 audit**；同一规则如何跨两个执行平面复用、哪个平面可绕过、失败时退到哪条硬边界，都写进代码和文档。

#### 解决的问题：替代了什么旧做法

它替代以下脆弱做法：

1. 只在 prompt 中说“不要运行危险工具”，没有最终执行点的确定性 gate。
2. MCP 工具和宿主 native tools 分别维护不同规则，导致一个 deny 在另一平面失效。
3. 将“调用来自已验证 principal”误当成“调用来自用户已同意的 ingress”，形成 confused deputy。
4. 把 `approval_required`、`grant_required`、`result` 和 `failed` 压成同一个错误字符串，无法正确恢复。
5. 把运行时 socket、PID、lock 和临时 token 一起迁移，导致新 daemon 继承旧协调状态。
6. 发布流程只跟 mutable latest/tag，不绑定 signed metadata、source commit、asset digest 与单调 generation。

边界是：AOS 的完整安全性依赖 Astrid Runtime、WASM sandbox、host capability enforcement 和发行配置；只读本仓库不能验证底层 runtime 的所有保证。

#### 架构 / 实现与数据流

```text
MCP client / Claude native tools
        │
        ├─ MCP tools/call ──> aos-mcp broker ──> trusted source_id gate
        │                              │
        │                              ├─ policy::evaluate(name,args)
        │                              ├─ capability grant / approval relay
        │                              └─ tool.v1.execute.<name> + result drain
        │
        └─ native Bash/Write/Edit ─> PreToolUse / hook-bridge
                                           │
                                           └─ same policy::evaluate

hard lower boundary: Astrid Runtime
  ├─ capability enforcement / WASM isolation
  ├─ principal-scoped KV and IPC attribution
  ├─ resource metering
  └─ audit
```

核心机制不是“所有 gate 都 fail-closed”。源码明确：

- 状态变更 MCP ingress 没有 caller context 时 fail-closed；未信任 `source_id` 时返回 consent-required，不 dispatch。
- broker 内的 argument-level policy deny 是 binding chokepoint；deny 后不 dispatch。
- native-tool settings-tier PreToolUse path 被文档明确称为 advisory/fail-open，硬边界仍是 host sandbox 与 `--disallowedTools`。
- policy 配置解析失败时退化为 capability PEP + loud audit，而不是 deny-all，以避免配置错误砖化所有 session；这是可用性/安全性的显式 trade-off。

#### Repo tree 摘要

```text
aos-ce/                                      # fixed commit tracked paths: 360
├── README.md / LICENSE-APACHE / LICENSE-MIT # 产品边界与双许可证
├── Cargo.toml / Cargo.lock                  # 24 workspace members、精确 runtime pins
├── crates/
│   ├── aos-mcp-broker/                      # MCP discovery、policy、ingress、approval、dispatch
│   └── unicity-aos-bootstrap/               # init/status/migrate/update/daemon 产品 CLI
├── capsules/                                # 22 个 first-party capsule 目录
│   ├── capsule-fs / capsule-http / capsule-shell
│   ├── capsule-memory / capsule-session / capsule-skills
│   ├── capsule-forge / capsule-meta-harness
│   └── capsule-hook-bridge / capsule-mcp / ...
├── distros/                                 # Community Edition manifest / release metadata
├── docs/
│   ├── meta-harness.md                      # user-space world 与扩展/评估模型
│   ├── runtime-migration.md                 # allowlist staging、receipt、recovery
│   └── release-channels.md                  # signed channels、generation、rollback
├── release/                                 # runtime compatibility 与 release readiness
├── scripts/                                 # build/install/release verification
└── .github/workflows/                       # release、promotion、nightly、CI
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/aos-mcp-broker/src/policy.rs` | 纯 PDP + rule loader | ordered first-match、JSON Pointer matcher、bounded glob、配置失败退到 PEP 并 audit |
| `crates/aos-mcp-broker/src/broker.rs` | MCP broker front door | req_id/topic gate、caller/source_id、可信 ingress、policy deny、approval/grant/result 状态整形 |
| `crates/aos-mcp-broker/src/hook_gate.rs` | native-tool 第二平面 | 同一 rule set 映射到 `ToolCallBefore {skip}`，deny-wins；明确 transport 边界 |
| `crates/aos-mcp-broker/src/execute.rs` | routed execute + drain | subscribe-before-publish、call_id matching、grant/approval multiplex、pending TTL/consumption |
| `crates/aos-mcp-broker/src/approval.rs` | 人类决策桥 | ingress、capability approval、grant respond 与 terminal reply |
| `crates/aos-mcp-broker/src/grant_decision.rs` | durable grant replay | recorded decision 驱动 auto-approve/deny/prompt，避免重复 elicitation |
| `docs/runtime-migration.md` | state migration contract | 显式 allowlist、排除 run state、private staging、hash receipt、锁与 rollback |
| `docs/release-channels.md` | release trust | signed immutable release + signed monotonic channel pointer，无 latest fallback |
| `docs/meta-harness.md` | 自我改进边界 | memory/skills/harness/capsule/trace 是 user-space world；capability 是硬上限 |

#### 源码精读（固定 commit）

**代码块 1：PDP 是纯函数，默认只收窄 capability PEP**  
来源：[`policy.rs#L157-L178`](https://github.com/unicity-aos/aos-ce/blob/1ffa80da3e19862bea2b5d3b3519a60ac5e12ea2/crates/aos-mcp-broker/src/policy.rs#L157-L178)

```rust
pub(crate) fn evaluate(rules: &[Rule], tool_name: &str, arguments: &Value) -> Decision {
    for rule in rules {
        if !glob_match(&rule.tool, tool_name) {
            continue;
        }
        if rule.when.iter().all(|m| matcher_holds(m, arguments)) {
            return match rule.effect {
                Effect::Deny => Decision::Deny {
                    reason: rule.id.clone(),
                },
                Effect::Allow => Decision::Allow,
            };
        }
    }
    Decision::Allow
}
```

逻辑：规则按顺序 first-match-wins；argument matcher 全部满足才命中；返回的 deny reason 是 operator rule id，不反射不可信 argument。`Allow` 只表示此 PDP 无异议，执行时 capability PEP 仍生效。边界是 early allow 可以短路 later deny，所以 rule order 本身是高权配置，必须 lint/test；默认 allow 也意味着 policy loader 失败不能被误报成 policy 已执行。

**代码块 2：native-tool 平面只做 veto，不用显式 allow 扩权**  
来源：[`hook_gate.rs#L119-L150`](https://github.com/unicity-aos/aos-ce/blob/1ffa80da3e19862bea2b5d3b3519a60ac5e12ea2/crates/aos-mcp-broker/src/hook_gate.rs#L119-L150)

```rust
fn verdict(tool_name: &str, tool_input: &Value) -> Value {
    let decision = crate::policy::evaluate(&crate::policy::load_rules(), tool_name, tool_input);
    if let crate::policy::Decision::Deny { reason } = &decision {
        let _ = ipc::publish_json(
            &crate::profile::audit_topic("pretooluse_deny"),
            &json!({ "tool": tool_name, "rule": reason }),
        );
    }
    verdict_body(&decision)
}

fn verdict_body(decision: &crate::policy::Decision) -> Value {
    match decision {
        crate::policy::Decision::Deny { reason } => json!({ "skip": true, "reason": reason }),
        crate::policy::Decision::Allow => json!({ "skip": false }),
    }
}
```

逻辑：同一 PDP 通过 hook transport 服务 native tools；`skip:false` 是 no-veto，不是授权。hook-bridge merge 语义为任意 `skip:true` 即阻断。边界是该 transport 的 failure path 多数保持 silent/no-op，以免 wedge fan-out；因此必须在 authority-plane map 中写明“此层是否为硬边界”，不能因为存在 hook 文件就宣称不可绕过。

**代码块 3：执行桥先订阅再发布，并区分四种终态**  
来源：[`execute.rs#L90-L119`](https://github.com/unicity-aos/aos-ce/blob/1ffa80da3e19862bea2b5d3b3519a60ac5e12ea2/crates/aos-mcp-broker/src/execute.rs#L90-L119) 与 [`#L139-L190`](https://github.com/unicity-aos/aos-ce/blob/1ffa80da3e19862bea2b5d3b3519a60ac5e12ea2/crates/aos-mcp-broker/src/execute.rs#L139-L190)

```rust
pub(crate) enum DispatchOutcome {
    Result(Value, bool),
    ApprovalRequired(ApprovalRequired),
    GrantRequired(GrantRequired),
    Failed(String),
}

pub(crate) fn dispatch_with_approval(
    tool_name: &str,
    call_id: &str,
    arguments: &Value,
) -> DispatchOutcome {
    if !is_valid_tool_name(tool_name) {
        return DispatchOutcome::Failed(format!(
            "{}: invalid tool name '{tool_name}'",
            crate::profile::log_tag()
        ));
    }
    let route_topic = format!("tool.v1.execute.{tool_name}");
    let result_topic = format!("tool.v1.execute.{tool_name}.result");
    let result_sub = match ipc::subscribe(&result_topic) {
        Ok(s) => s,
        Err(e) => return DispatchOutcome::Failed(format!("subscribe failed: {e}")),
    };
    let approval_sub = match ipc::subscribe(approval::APPROVAL_REQUEST_TOPIC) {
        Ok(s) => s,
        Err(e) => return DispatchOutcome::Failed(format!("approval subscribe failed: {e}")),
    };
    let forward = json!({
        "type": "tool_execute_request",
        "call_id": call_id,
        "tool_name": tool_name,
        "arguments": arguments,
    });
    if let Err(e) = ipc::publish_json(&route_topic, &forward) {
        return DispatchOutcome::Failed(format!("publish failed: {e}"));
    }
    // bounded drain loop follows; result is filtered by call_id
}
```

注：为压缩展示，两个 error string 缩短并省略后续 drain loop；签名、variant、subscribe-before-publish、forward schema 与控制流来自固定源码。逻辑：结果、工具中途 capability approval、kernel grant miss 和 transport failure 是不同状态；订阅发生在 publish 之前，避免 fast result/approval race。边界是 `astrid.v1.approval` 是共享广播 topic，源码把正确性建立在 capsule instance 的串行执行/store mutex 上；若未来并发模型变化，缺少 call_id 的 approval envelope 会成为相关性风险。

**代码块 4：迁移只复制持久状态，不复制 daemon coordination**  
来源：`docs/runtime-migration.md` 与 importer contract 的机制摘要（伪代码，不是上游源码原样复制）

```text
lock source run/system.lock
validate explicit top-level + etc allowlist
reject symlinks / overlapping roots / active socket / non-empty target
copy persistent state into private staging
exclude run/, COW worktrees, old runtime executables
record path + byte_length + blake3 digest receipt
fsync supported files/directories
atomic cutover, retain pre-import backup until receipt durable
```

这与 shared hub 路径迁移直接相关：持久事实/配置可以受控迁移，PID/socket/cache/current-session token 必须重建。边界是这段为 docs contract；本机没有构建或执行 importer，具体跨平台 fsync、Windows behavior 和 crash recovery 均待核验。

#### 依赖分析与供应链风险

- workspace 有 24 members：2 个 product crates + 22 个 first-party capsules；resolver 3、Rust edition 2024。
- 关键依赖精确 pin：`astrid-sdk = 0.7.1`、`astrid-core/types/uplink = 0.10.4`；其他核心包括 axum 0.8、blake3 1.8.5、clap 4.6、tokio 1、serde/json、uuid 1.22。
- 本地解析 `Cargo.lock`：212 packages，其中 188 个 registry source、0 个 git source、24 个 workspace/path package。没有 git dependency 降低 floating-revision 风险，但不代表 crates.io packages 或构建脚本安全。
- README 声明 release 提供 checksums、Sigstore bundles、GitHub provenance attestations 与 runtime compatibility；`docs/release-channels.md` 还规定无 `releases/latest` fallback、channel generation 单调递增。本文只核验了文档/源码结构，未下载并独立验证 release assets。
- 依赖的 Astrid Runtime 是独立的硬信任边界；AOS repo 的测试/许可证不能自动证明 runtime capability enforcement 正确。
- Dependabot alerts API 返回 403，公开 alert 状态待核验；没有把“无法读取”写成“无 alert”。

#### README / docs / release / issues 交叉核验

- README 的 workspace layout 与实际 `crates/`、`capsules/`、`distros/`、`docs/` 一致。
- `docs/meta-harness.md` 明确 AOS 不是 harness；hard boundary 是 Astrid Runtime 的 isolation/capability/IPC/metering/audit，agent initiative 只能在 granted capability 内发挥。
- 最新 release 2026.1.3 比固定源码旧；不能把当前 `main` 的 root license 修复等同于该 release 的所有 bytes。
- [issue #58](https://github.com/unicity-aos/aos-ce/issues/58) 报告 2026.1.3 x86_64 GNU binary 需要 GLIBC 2.39，RHEL/Oracle Linux 9 的 2.34 无法运行；说明签名验证成功不等于平台兼容。
- [PR #74](https://github.com/unicity-aos/aos-ce/pull/74) 提议 musl targets，截至查询为 open；不得写成已经发布。
- [PR #79](https://github.com/unicity-aos/aos-ce/pull/79) 于 2026-07-31 merged，才补上仓库 root MIT/Apache license；7 月 28/29 API 的 NOASSERTION 与今日 Apache-2.0 变化由真实 commit 解释。
- [PR #75](https://github.com/unicity-aos/aos-ce/pull/75) 提议 durable trace/evaluation archive，截至查询仍 open；不能把 roadmap 外推成现有能力。

#### 真实测试结果

```text
$ cargo test -p aos-mcp-broker
/usr/bin/bash: line 3: cargo: command not found
exit_code=127

$ rustc --version
/usr/bin/bash: line 3: rustc: command not found
```

准确结论：当前 WSL cron 环境缺 Rust toolchain，所以 **未编译、未运行 unit tests、未运行 AOS installer/daemon/MCP、未验证 Astrid capability enforcement**。源码中存在 tests 只能证明作者提供了测试代码，不能替代本机运行证据。

#### 可复用经验

- 当同一 policy 要覆盖 MCP 工具与宿主 native tools 时，应优先共享一个纯 PDP，再为每个执行平面建立独立 transport adapter 和 authority 声明，因为“共享规则”不等于“共享硬边界”；边界是 advisory hook 仍可能 fail-open。
- 当外部 client 能触发状态变更时，应优先用 host/kernel stamped `source_id` 绑定交互同意，而不是只检查 principal 是否 verified，因为 verified identity 不回答“哪个 ingress 代调用”；边界是 trust marker 的撤销和过期策略仍需独立设计。
- 当等待中的调用可能遇到 result、approval、grant 或 transport failure 时，应优先把它们建模为互斥结构化状态，并 subscribe-before-publish，因为错误字符串无法表达 resume 与 re-send 的差异；边界是共享 topic 必须有可靠 correlation 或严格串行前提。
- 当 policy 配置读取失败时，应优先显式记录 fallback target 与 audit severity，而不是笼统写 fail-open/fail-closed，因为退回 capability PEP 与退回 unrestricted execution 完全不同；边界是 operator 必须监控 loud audit。
- 当迁移 Agent runtime 时，应优先 allowlist 持久状态、排除 run coordination、用 staging+receipt+backup 切换，因为 PID/socket/token 不能跨实例继承；边界是 receipt integrity 不等于来源可信。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/authority-plane-map/` 做纯离线 fixture（今日只设计，不改生产）：

1. 定义 `Gate = {plane, actor_source, scope, effect, hard_boundary, failure_mode, fallback_boundary, audit_event}`。
2. fixtures 覆盖 MCP broker hard deny、native hook no-veto、policy load failure→capability PEP、missing caller→blocked、approval→park/resume、grant→drop/re-send。
3. validator 拒绝 `failure_mode=fail-open` 却没有 `fallback_boundary` 的 gate。
4. 用历史 Hermes 工具调用流程映射 prepare/terminal/audit/cron，找出只靠 prompt 的 effect path。
5. 全程不运行外部 tool effect，不修改 Hermes config/provider/auth/cron，不安装 AOS。

#### 风险边界

- **License**：GitHub API 为 Apache-2.0；仓库根声明 MIT OR Apache-2.0。依赖、Astrid Runtime、capsule assets 与发行包需另审；只抽象机制，不复制产品源码。
- **维护活跃度**：固定 commit 距查询不足 24 小时，release/PR 活跃；但仓库创建不足 1 个月、forks 仅 16、API open items 26，快速变化且成熟度有限。
- **安全风险**：MCP、native hooks、IPC topic、capability grants、approval、KV trust markers、installer、signed channels、migration secrets 都是高权边界。
- **显式弱点**：native PreToolUse path 被源码承认为 advisory/fail-open；policy loader 失败退到 PEP；approval 广播 topic 的 correlation 建立在串行前提上。
- **兼容性**：issue #58 的 GLIBC 2.39 问题仍 open；musl PR 尚未合并，不能假设企业 Linux 可运行。
- **运行局限**：本机无 Rust，所有 compile/runtime claims 待核验；未验证 release signature/assets 或 importer recovery。
- **不适用场景**：shared hub 不是 WASM Agent OS，不需要为了吸收 policy/迁移模式而整体改造成 AOS。
- **不可自动执行**：不运行 README 的 curl|sh installer，不初始化 `~/.aos`，不导入 secrets/runtime，不授予 capsule/ingress，不改本机 agent 配置。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`authority-plane map + fallback-boundary conformance`，可补强 Hermes 工具/cron/bridge 的权限描述和审计。
- **需验证**：先用 Hermes 自有 fixtures 证明每条 effect path 的 hard boundary、failure mode、fallback 和 audit 都可机器校验；再与 verification-first、effect-scope、config-target-routing、subagent 四状态去重。
- **暂不沉淀**：AOS installer、capsule format、Astrid IPC、native hook implementation、release pipeline和完整 meta-harness skill；当前无 Rust runtime 验证，且与现有 shared hub 架构不同。
- **今日动作**：只提 candidate；不写 curated active fact、不创建 shared skill、不更新 manifest。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/authority-plane-map/{schema.json,fixtures/,validate.py,test_gates.py,README.md}`。
2. **Hermes 审计候选**：为 terminal/tools/cron/gateway bridge 增加 `hard_boundary/failure_mode/fallback_boundary` 检查；不让“有 hook”自动等于“强制执行”。
3. **shared skill 候选更新**：验证后优先更新已有 verification/effect-scope 类 skill 的权限平面章节，不创建“AOS product integration”重复 skill。
4. **迁移规则候选**：扩展 `foundation/path-portability` 的 checklist：persistent allowlist、runtime exclusion、receipt、staging、backup、recovery；保持通过 shared-root resolver，不引入 AOS 路径。
5. **跨 Agent 复用**：future-agent 可消费中立 gate schema/fixtures；Agent-local transport adapter 各自实现。当前任务不调用或配置 OpenClaw。
6. **shared 分层**：API/stdout/clone 留 runtime；完整研究留 inbox；治理评分、证据、去重、脱敏与人工/总控审查后才可能进入 curated/capabilities。

---

### 2. yc-software/qm

**基本信息（GitHub API）**

- URL：https://github.com/yc-software/qm
- Stars：**4,911**；Forks：**484**；Language：TypeScript；License：**MIT**。
- 创建：2026-07-29T20:03:08Z；updated：2026-08-01T23:32:21Z；pushed：2026-08-01T01:30:53Z；`open_issues_count=63`（含 PR）。
- 固定 commit：[7f2c916360f1](https://github.com/yc-software/qm/commit/7f2c916360f1797a8ff2a77ce2ce40c5fabab087)，时间 2026-07-31T17:55:39Z，message `Use @latest in the qm init bootstrap instead of a version placeholder (#41)`。
- 最新 GitHub Release：[v0.1.4](https://github.com/yc-software/qm/releases/tag/v0.1.4)，published 2026-07-31T18:03:56Z；与固定 commit 时间接近。
- Repository license endpoint 返回根 `LICENSE`、SPDX MIT。

#### 一句话判断

QM 值得学的是它把多人/多房间 Agent 的共享问题拆成 **scope resolution、只读/可写 workspace layers、org floor + narrower scope、durable store、model/harness adapter、sandbox、surface plugin、skill pack import/sync 和显式安全局限**；这比“把所有 workspace 指向同一个 memory 目录”更接近可审计的持续上下文系统。

#### 解决的问题：替代了什么旧做法

它替代这些做法：

1. 全组织 Agent 共用一份无 scope memory/files/keychain，任何 channel 都能看到个人上下文。
2. 用 display name 或 Slack channel 文本决定资源身份，而不是 stable scope ID 与 audience entitlement。
3. lower-scope prompt 可以覆盖 organization policy，没有 tighten-only composition。
4. 让模型/沙箱自己做 authorization，core 只记录日志。
5. 将安全 posture 写成一句自然语言，不能解析成具体 screening/approval mechanism。
6. 把 skill git HEAD 更新直接自动提升为 org-wide skill，没有 pinned/tracked mode、admin gate 或 durable import state。
7. 把 UI/Slack/portal 业务写死进 agent core，难以切换 harness/model/surface。

边界是：QM 自己明确是 early experimental software，不是 hardened public/multi-tenant boundary；其 security controls 也有大量已知缺口。

#### 架构 / 实现与数据流

```text
Slack / Web / Portal / Cron
          │ authenticated surface + conversation/audience
          ▼
Headless core
  ├─ identity + ACL + scope resolution
  ├─ org floor + scope config + command/security policy
  ├─ session/run/queue/memory/audit (durable Postgres interfaces)
  ├─ harness router (Pi / OpenCode / Codex / Claude Code)
  └─ fixed tool surface
          │
          ▼
per-scope durable sandbox
  ├─ scope rw workspace
  ├─ org/team ro layers
  ├─ installed tools / skill packs
  └─ scoped credentials / logged-in services

optional surfaces/plugins consume core HTTP or direct service client;
canonical state stays in core stores, not in UI projection.
```

`src/resolution/resolution-service.ts` 是关键收口：DM 映射 personal scope，group/channel 映射对应 scope；workspace 层为 org `global` ro + 当前 scope rw，DM 可挂 team ro；org soul 和 lower-scope soul 分段，lower scope 不能 override；egress floor 按整个 audience 计算，granted handles 由 ACL 查询。

#### Repo tree 摘要

```text
qm/                                          # fixed commit tracked paths: 1,264
├── README.md / SECURITY.md / AGENTS.md      # 产品、威胁模型、工程约束
├── package.json / package-lock.json         # Node 24.15、npm 11.10、依赖与 overrides
├── src/
│   ├── core/ / harness/ / model/            # turn orchestration 与多 harness/model adapters
│   ├── resolution/ / acl/ / identity/       # scope、audience、grant、egress floor
│   ├── security/ / policy/ / auth/          # posture/screening、command policy、signed tokens
│   ├── memory/ / sessions/ / runs/ / tasks/ # durable scoped state 和 workers
│   ├── sandbox/ / credentials/              # per-scope computer、secret/materialization
│   ├── skills/                              # packs、normalize、ingest、sync、materialize
│   ├── cron/ / monitors/ / wake/            # background work
│   ├── api/ / slack/ / surfaces/            # control plane 和 surface adapters
│   └── wiring.ts                            # implementation composition root
├── plugins/{admin,auth,chassis,onboarding,portal,web-ui}/
├── cli/                                     # deployment directory interpreter
├── deploy/layers/                           # organization-specific isolated layer
├── aws/ / fly/ / local/                     # substrate backends
├── skills-seed/                             # first-party skills
├── test/                                    # unit/integration/conformance tests
├── docs/ / adrs/                            # deployment/security/design contracts
└── .github/workflows/                       # CI、release、security checks
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/resolution/resolution-service.ts` | conversation→scope composition root | scope ID、ro/rw layers、org/lower prompt、command/security policy、audience egress、ACL handles |
| `src/security/security-posture.ts` | posture contract | dangerous/auto/strict 映射；org floor + scope tighten-only；verdict/payload parsing |
| `src/security/security-screener.ts` | external classifier adapter | bounded chunks、overlap、2 concurrency、deadline、429 retry、response cap、strict-wins aggregation |
| `src/policy/command-policy.ts` | deterministic effect floor | org command floor 与 scope narrowing，和 model prompt 分离 |
| `src/skills/normalize.ts` | heterogeneous skill normalization | frontmatter、scope/private、capability/egress、credential refs、unknown metadata |
| `src/skills/skill-sync-engine.ts` | pack polling | tracked 自动 reconcile；pinned 只标 updateAvailable；leader lease；逐 pack 隔离失败 |
| `src/skills/pack-fetcher.ts` | git pack boundary | resolve/fetch revision 与 pack artifact |
| `src/persistence/leader-lease.ts` | multi-instance singleton work | sync/sweeper 等任务由 durable lease 收口 |
| `SECURITY.md` | honest threat model | command policy、browser、credentials、screening、egress、admin、retention 等已知限制 |
| `docs/deploy-directory.md` | portable deployment contract | no secret values、immutable pins、layer hash、plan/up/check/rollback、enforced/validated-only 表 |

#### 源码精读（固定 commit）

**代码块 1：security posture 用有序格保证 lower scope 只能收紧**  
来源：[`security-posture.ts#L14-L39`](https://github.com/yc-software/qm/blob/7f2c916360f1797a8ff2a77ce2ce40c5fabab087/src/security/security-posture.ts#L14-L39)

```typescript
const POSTURE_POLICIES: Record<SecurityPosture, ResolvedSecurityPolicy> = {
  dangerous: { inboundScreening: "off", toolApprovals: "none" },
  auto: { inboundScreening: "external", toolApprovals: "none" },
  strict: { inboundScreening: "off", toolApprovals: "all" },
};

const POSTURE_RANK: Record<SecurityPosture, number> = {
  dangerous: 0,
  auto: 1,
  strict: 2,
};

export function composeSecurityPosture(orgFloor: SecurityPosture, scope?: SecurityPosture | null): SecurityPosture {
  if (!scope || POSTURE_RANK[orgFloor] >= POSTURE_RANK[scope]) return orgFloor;
  return scope;
}
```

逻辑：scope 选择比 org 更严格的 posture 才生效；dangerous 也保留 predeclared hard denials/auth/scope/audit，只关闭 content screen/approval。边界是三个 posture 不是严格的单一安全强弱轴：`auto` 开 external screening，`strict` 反而关闭 screening、改成 every tool approval；rank 只编码产品定义的 control bundle，不证明 strict 在每个 threat 上都强于 auto。

**代码块 2：外部内容筛查分块有上限、overlap 和两路并发**  
来源：[`security-screener.ts#L55-L108`](https://github.com/yc-software/qm/blob/7f2c916360f1797a8ff2a77ce2ce40c5fabab087/src/security/security-screener.ts#L55-L108)

```typescript
function securityScreenChunks(text: string): string[] {
  const normalized = text.toWellFormed();
  if (normalized.length <= SECURITY_SCREEN_CHUNK_CHARS) return [normalized];
  const chunks: string[] = [];
  let start = 0;
  while (start < normalized.length) {
    let end = Math.min(start + SECURITY_SCREEN_CHUNK_CHARS, normalized.length);
    const endCode = normalized.charCodeAt(end);
    if (end < normalized.length && endCode >= 0xdc00 && endCode <= 0xdfff) end -= 1;
    chunks.push(normalized.slice(start, end));
    if (end === normalized.length) break;
    start = Math.max(end - SECURITY_SCREEN_CHUNK_OVERLAP_CHARS, start + 1);
    const startCode = normalized.charCodeAt(start);
    if (startCode >= 0xdc00 && startCode <= 0xdfff) start += 1;
  }
  return chunks;
}

async function classifyChunks<T>(
  chunks: string[],
  classify: (chunk: string, index: number, signal: AbortSignal) => Promise<T>,
  signal: AbortSignal,
): Promise<T[]> {
  // batches are sliced by two; first terminal failure aborts sibling work
  // fulfilled results are retained only when the batch had no failure
  return results;
}
```

注：`classifyChunks` body 用注释压缩，签名、两路 batch、abort 和结果语义来自固定源码。逻辑：16,000 字输入上限，1,600 字 chunk、256 字 overlap、Unicode surrogate 边界保护、每批最多两个请求；一个 terminal failure 会 abort sibling，避免 partial classification 被当 clean。边界是字符窗口可能切断语义，overlap 也不能保证跨多个 chunk 的组合攻击被识别；external classifier 看到完整被筛文本，存在数据披露边界。

**代码块 3：任何 strict chunk 赢，且 HTTP adapter 禁止 redirect**  
来源：[`security-screener.ts#L189-L267`](https://github.com/yc-software/qm/blob/7f2c916360f1797a8ff2a77ce2ce40c5fabab087/src/security/security-screener.ts#L189-L267)

```typescript
export function createSecurityScreenProxy(opts: {
  provider: string;
  endpoint: string;
  token: string;
  timeoutMs: number;
  shadow: boolean;
  fetch?: typeof fetch;
}): SecurityScreener {
  const request = opts.fetch ?? fetch;
  let activeShadow = 0;
  return {
    provider: opts.provider,
    shadow: opts.shadow,
    async classify(input) {
      if (input.payload.length > MAX_SECURITY_SCREEN_CHARS) {
        throw new Error("Security screen proxy payload exceeds the supported limit");
      }
      // each chunk POST uses redirect:"error", deadline and bounded 429 retry
      const classifications = await classifyChunks(/* ... */);
      return classifications.reduce((highest, current) => {
        if (current.verdict.decision !== highest.verdict.decision) {
          return current.verdict.decision === "strict" ? current : highest;
        }
        return current.score > highest.score ? current : highest;
      });
    },
  };
}
```

逻辑：任意 chunk 达到 threshold 即把整体降到 strict；同 verdict 取最高 score 作为诊断。response body 被限制 64 KiB；429 有 250/1000/4000ms fallback delay；invalid JSON/score/outcome/redirect 都失败。边界是 classifier 是 heuristic，不是 authorization；`SECURITY.md` 明确 command/background output、opaque/multimodal results、raw webhooks 等并未全覆盖，shadow mode 不掌权但仍披露数据。

**代码块 4：skill pack 的 tracked 与 pinned 具有不同副作用**  
来源：[`skill-sync-engine.ts#L23-L61`](https://github.com/yc-software/qm/blob/7f2c916360f1797a8ff2a77ce2ce40c5fabab087/src/skills/skill-sync-engine.ts#L23-L61)

```typescript
export function createSkillSyncEngine(deps: SkillSyncDeps): SkillSyncEngine {
  const leaderLease = deps.leaderLease ?? createNoopLeaderLease();

  async function syncOne(packId: string): Promise<void> {
    const pack = await deps.packs.get(packId);
    if (!pack) return;
    if (pack.syncMode === "tracked") {
      const head = await deps.fetcher.resolveRef(pack);
      if (pack.lastImport?.status === "ok" && head === pack.lastImport.commit) return;
      await deps.reconcile(packId);
    } else {
      const head = await deps.fetcher.resolveRef(pack);
      const available = pack.lastImport ? head !== pack.lastImport.commit : false;
      if (available !== Boolean(pack.updateAvailable)) {
        await deps.packs.update(packId, { updateAvailable: available });
      }
    }
  }

  const tick = async (): Promise<void> => {
    await leaderLease.hold("skills:sync:tick", syncAll);
  };
  return { tick, start: sweeper.start, stop: sweeper.stop };
}
```

逻辑：tracked pack 在 HEAD 变化时 reconcile；pinned pack 只更新 `updateAvailable`，不自动导入。全局 tick 由 leader lease 收口，每个 pack 的异常在 `syncAll` 内隔离，避免一个坏源阻断其他 packs。边界是 `resolveRef` 与 reconcile 之间仍有 revision race，安全导入还必须 pin 实际 fetched commit、验证内容、scope/visibility/credentials 并通过 admin promotion gate；leader lease 的默认 noop 只适用于单实例/测试 wiring。

#### scope-resolution 关键机制

`createResolutionService` 的实现给 shared hub 很直接的参考：

- DM → `personal:<actor>`；group/channel → 对应 conversation scope。
- org scope 以 `global` read-only mount 注入；current scope 是 root read-write；DM team layers 只读。
- org instructions 先出现，lower-scope instructions 被明确包在“可增加、不可覆盖”的 delimiter 中。
- command policy 由 org floor + scope policy compose；security posture 从 durable scoped config 解析。
- audience 的每个 principal/team 都进入 live config refresh；egress allow/deny floor 和 ACL handles 以完整 audience 计算。

这不是形式化 non-interference proof。`SECURITY.md` 明确 audience-floor filtering 的 origin labels 尚不完整，ambient Slack judge path 也未重复完整 internal-only check。

#### 依赖分析与供应链风险

- `package.json` 要求 Node `>=24.15.0`、npm `>=11.10.0`；本机默认 Node 22.14/npm 10.9 不满足，不能直接用默认 runtime 判定兼容。
- 主要 runtime dependencies：Claude Agent SDK、OpenAI Codex、OpenCode、Pi fork、Fastify、Slack Bolt/API、Postgres/pg-boss、AWS SDK、jose、zod、typebox、croner、tar-stream。
- `@earendil-works/pi-coding-agent` 来自 GitHub release `.tgz`，`package-lock.json` 有 SHA-512 integrity；非 registry artifact 增加发布账号、release asset 与 provenance 风险。
- `package.json` 有 dependency overrides（fast-uri、brace-expansion、protobufjs 等），说明维护者主动 pin transitive versions；但也会增加升级/兼容维护负担。
- `SECURITY.md` 声明 `.npmrc min-release-age=7`，用 7 天 cooldown 降低刚发布恶意包进入 lockfile 的概率；精确紧急安全更新可绕过窗口。cooldown 只降低时间窗口风险，不验证 maintainer 或旧版本安全。
- `npm audit --omit=dev --package-lock-only` 的 metadata 为 577 total（356 prod、162 dev、116 optional、16 peer，分类有重叠语义），0 known vulnerabilities；随后 `npm ci` 安装 616 packages、audit 618 packages，同样 0 known vulnerabilities。npm advisory coverage 不是完整供应链审计。
- Dependabot alerts API 返回 403，状态待核验；不能与 npm audit 0 合并成“无漏洞”。

#### README / SECURITY / release / PR 交叉核验

- README 的 central core + Postgres + per-scope sandbox + optional plugins 与 repo tree/wiring/interfaces一致。
- README 明确 Pi/OpenCode/Codex/Claude Code 可驱动同一 core；本文只核验 adapter 路径存在，没有调用真实模型或这些 harness。
- `SECURITY.md` 直接声明 early experimental、不是 hardened public/multi-tenant boundary，并列出 command policy 可绕过、browser 某些动作越过 core gates、sandbox credential 使用时为明文、screening 不完整、egress conditional、admin 可读敏感内容、artifact 无 expiry 等限制。
- 最新 release v0.1.4 发布于 2026-07-31；仓库创建于 7 月 29 日，版本和 API/contract 仍非常新。
- [PR #106](https://github.com/yc-software/qm/pull/106) 提议 scope write 的 claim/heartbeat/release convention，截至查询 open；它是 ADR proposal，不是现有 durable concurrency guarantee。
- [PR #78](https://github.com/yc-software/qm/pull/78) 提议 optional gbrain memory backend，截至查询 open；不能写成已支持。
- [PR #107](https://github.com/yc-software/qm/pull/107) 提议 doc-map drift guard，截至查询 open；说明 docs/code conformance 仍在快速补强。

#### 真实测试与审计结果

第一次直接使用系统 Node 22 跑 `.ts` test 真实失败（unknown `.ts` extension）；安装 lockfile 后使用要求的 Node 24.15 进行定向验证：

```text
$ npx --yes node@24.15.0 --test --experimental-test-module-mocks \
    test/security-posture.test.ts \
    test/security-screener.test.ts \
    test/skill-sync-engine.test.ts \
    test/skill-conformance.test.ts

ℹ tests 23
ℹ pass 23
ℹ fail 0
ℹ duration_ms 357.84863
```

覆盖：posture parse/compose、screen verdict/payload、proxy chunk/Unicode/retry/abort/response cap/shadow capacity、seed Skill conformance、tracked/pinned sync 与单 pack failure isolation。准确边界：

- 这是 4 个 test files 的 **23 项定向测试**，不是 1,264-path repo 的完整 suite。
- 没有启动 Postgres、Slack、web、sandbox、AWS/Fly、真实 model/harness、connector、cron 或 production deployment。
- `npm ci` 在默认 Node 22 下有 engine warnings，但最终 tests 用 Node 24.15 执行并通过。
- npm audit 0 findings 只代表当前 advisory DB 与 lockfile解析结果。

#### 可复用经验

- 当多 workspace 共享 org 事实又保留个人/房间状态时，应优先用 immutable scope ID + ro/rw layer composition，而不是共享同一可写目录，因为共享读取与共享写权限不是同一概念；边界是 filesystem mount 仍需 host ACL 和 path traversal 防护。
- 当 lower scope 可以自定义 Agent 时，应优先用有序 policy lattice 做 tighten-only composition，并把 org floor 与 lower prompt 分隔，因为自然语言“不得覆盖”不是唯一 enforcement；边界是不同 control bundle 未必能压成单调一维 rank。
- 当外部内容筛查会调用远端 classifier 时，应优先限制输入/响应、并发、deadline、redirect、retry，并让任何 strict chunk 赢，因为 partial clean 不能覆盖一段恶意内容；边界是 screening 不是 authorization，且会向 provider披露数据。
- 当 Skill 从 git pack 同步时，应优先区分 pinned 与 tracked，并由 leader lease/commit receipt/admin promotion 控制副作用，因为“发现更新”不等于“授权组织级生效”；边界是 resolve/fetch/reconcile 间仍需 immutable commit binding。
- 当系统声称 scoped security 时，应优先同时维护“已执行 controls”和“已知 limitations”的机器/文档映射，因为 audit log 或 approval 不等于预防；边界是 docs 也可能 stale，需要 conformance tests。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/scope-resolution-contract/` 做无网络 fixture（今日只设计）：

1. schema：`principal, audience, conversation, scope_id, layers[], policy_floor, scope_policy, egress_floor, grants[]`。
2. fixtures：personal DM、team member DM、internal channel、含外部参与者 channel、lower-scope weakens org、ACL store unavailable。
3. validator：org layer 必须 ro，current scope 才可 rw；lower policy 只能 tighten；audience entitlement failure 返回 blocked；display name 不得作为 storage key。
4. 再为 skill pack fixture 增加 `sync_mode=pinned|tracked`、resolved commit、imported commit、promotion state，验证 pinned 只提示更新。
5. 不连接 Slack/model/Postgres/git remote，不读取 secret，不修改现有 shared symlink/config/cron。

#### 风险边界

- **License**：repo MIT；npm dependencies、GitHub release tarball、provider SDK、sandbox image、plugins 和组织 deployment layer 各有独立 license/provenance。
- **维护活跃度**：更新距查询不足 24 小时、PR 非常活跃；但项目创建仅约 3 天、v0.1.4、open items 63（含 PR），接口稳定性和真实采用率无法由 stars 证明。
- **明确安全局限**：不是 hardened public/multi-tenant boundary；command policy 可被编码/脚本绕过；browser path、egress、screening、audience floor、provider gateway 均有缺口。
- **credential 风险**：sandbox process 在使用时可读明文 credential/token；purpose 是 instruction/audit field，不是强制用途约束。
- **数据保留**：session/memory/request capture 可持久化，file artifact 无 expiry/byte reclamation；需要独立 retention policy。
- **供应链**：616 installed packages、GitHub-hosted pi tarball、多个 SDK/provider；7-day cooldown 和 integrity 不能消除 compromise。
- **运行局限**：仅 23 个定向 tests；未运行数据库、surface、sandbox、deployment或真实 agent loop。
- **不适用场景**：shared hub 当前是跨 Agent 文件型真相/兼容层，不应直接引入 QM 的 Postgres/Slack/云部署复杂度。
- **不可自动执行**：不执行 `qm init/up`，不创建云资源/Slack app，不加载 credentials/model key，不改 Hermes/OpenClaw config/provider/tools/auth/env/cron。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`scope-resolution contract + tighten-only policy + pinned/tracked skill update semantics`，直接关联 shared hub 多 agent/workspace 共享。
- **需验证**：用 shared hub 自有 fixtures 检查 scope identity、ro/rw compatibility links、audience/agent entitlement、policy floor 与 skill promotion；再与 shared-memory-bridge、path-portability、shared-skill-governance 去重。
- **暂不沉淀**：QM 完整多人 harness、Slack/web plugins、Postgres stores、sandbox/cloud deployment、security screener provider；项目过新且高权 surface 未实测。
- **今日动作**：只提 candidate，不导入 repo skill、不新增 dependency、不更新 shared manifest/curated fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/scope-resolution-contract/{schema.json,fixtures/,resolve.py,test_resolution.py,README.md}`。
2. **shared hub 映射**：`curated/` 类比 org ro truth；`inbox/<agent>/` 与 `runtime/<agent>/` 是 agent-scoped writes；兼容 symlink 只提供稳定入口，不放宽 canonical write target。
3. **Hermes bridge 审计候选**：bridge check 输出 resolved agent/profile/scope、read layers、write targets 与 source-of-truth；禁止只显示一个 shared path。
4. **shared skill governance 候选**：manifest 增加/复核 `scope/reference_policy/future_agent_readable`；更新发现与实际 promotion 分离，promotion 仍需治理/人工 gate。
5. **portable conformance**：在 `bootstrap.py check` 或独立 read-only checker 中验证 org-like curated paths ro-by-policy、agent runtime/inbox writable、compat links 不成为新 truth source。
6. **跨 Agent 复用**：共享 schema/fixtures；Hermes/future-agent 各自 adapter。当前任务未调用 OpenClaw，也不改任何 agent 本地配置。

## 横向对照：权限与共享上下文不能只看一层

| 层次 | AOS CE | QM | Hermes/shared hub 候选 |
|---|---|---|---|
| 身份入口 | kernel-stamped source_id + principal | authenticated principal + conversation/audience | active Hermes profile + resolved shared root + agent lane |
| scope | per-principal KV/capability/capsule | personal/group/channel/team/org scope IDs | curated truth、inbox agent lane、runtime agent lane |
| policy | common PDP over MCP/native transports | org floor + scope tightening + posture bundle | governance/config target/effect policy，需 machine-readable map |
| 硬边界 | Astrid capability PEP/WASM sandbox | core ACL/effect gates + sandbox substrate | host tool API、filesystem permissions、cron manager、approval gate |
| 等待状态 | result/approval/grant/failed | runs/queue/signals/durable stores | completed/blocked/needs_user/failed + artifact receipt |
| 共享能力 | capsules/skills/Forge | scope-owned skills + packs + admin promotion | capabilities/skills + manifest + governance approval |
| 迁移/更新 | staging+receipt；signed monotonic release channels | pinned engine/layer/image + plan/check/rollback | root resolver + compat symlinks + bootstrap/check |
| 明确边界 | native hook advisory；policy load→PEP | early experimental；screen/egress/audience gaps | candidate 不直升 curated/skill；配置与 secrets 不自动改 |

## 经验沉淀

1. 当同一规则跨 MCP、native tool、browser 或其他 effect 平面时，应优先共享纯 decision core、分别声明 transport enforcement 和 fallback boundary，因为规则一致不等于不可绕过；边界是 advisory plane 不能替代 host hard gate。
2. 当外部入口能借 core 权限产生副作用时，应优先绑定 host-stamped ingress identity、actor、scope 与一次真实 consent，因为 verified principal 不证明 deputy 来源获准；边界是 standing trust 还需撤销、过期和审计。
3. 当调用可能进入 result、approval、grant、blocked 或 failed 时，应优先使用结构化状态和明确的 resume/re-send 语义，因为普通错误字符串会诱发错误重试或假完成；边界是每个状态仍需 terminal receipt。
4. 当低层 policy 配置失败时，应优先记录它退回哪条硬边界并发 loud audit，因为“fail-open”若实际退回 capability PEP，与 unrestricted execution 的风险完全不同；边界是无监控的 audit 等于无人察觉。
5. 当多 workspace 共享长期事实时，应优先把共享层挂成只读、把写入绑定到 immutable agent/scope lane，因为共享访问不应自动变成共享写权限；边界是 symlink/compat path 也必须解析回 canonical target。
6. 当 lower scope 可自定义 Agent 时，应优先用 tighten-only policy lattice 和 conformance fixture约束，而不是只在 prompt 里写“不能覆盖组织规则”；边界是不同安全机制不一定存在简单全序。
7. 当外部内容进入模型前要筛查时，应优先对输入、响应、并发、deadline、redirect 和 partial failure设上限，并让危险片段优先，因为 clean majority 不能抵消单个恶意 chunk；边界是筛查不是 authorization 且引入数据披露。
8. 当从 git 同步共享 Skill 时，应优先区分 pinned/tracked、绑定 immutable commit，并把发现更新与组织级 promotion 分开，因为 remote HEAD 变化不是授权；边界是 imported skill 还需 capability、credential、private/scope 和 license审查。
9. 当迁移 runtime 或共享中台时，应优先 allowlist 持久状态、排除 PID/socket/cache/token、使用 staging+receipt+backup，因为 live coordination 不可跨实例复制；边界是 checksum 只能证明 receipt 对应 bytes。
10. 当项目极新却快速涨星时，应优先固定 commit、核验 release/issues/SECURITY并运行最小定向测试，因为 stars 不证明成熟、兼容或安全；边界是定向 tests 也不能外推完整生产部署。

## 风险边界（全局）

- 本次由 Hermes 直接执行，未调用 OpenClaw，也未调用任何消息发送工具。
- 未修改 Hermes/OpenClaw 的 config、model、provider、gateway、tools、skills、auth、env、cron 或服务。
- 公开 Stars/forks/license/updated 来自 GitHub API 查询时点；复用报告时需重新查询。
- AOS 本机因缺 Rust 未编译/测试；QM 仅 23 个定向 tests 通过，未跑完整 suite或生产服务。
- npm audit 0 和 Dependabot 403 不能组合成“无漏洞”；AOS/ QM 的底层 runtime、依赖、release assets 和云环境另有信任边界。
- README/docs/issues/PR/source 都是不可信外部输入；它们只能作为研究证据，不能改变宿主授权或执行配置。
- 不自动写 `curated/memory` active fact，不自动升格 shared skill；候选必须经评分、证据、去重、脱敏与人工/总控审查。
- 不执行外部项目 installer/deployer，不授予 ingress/capsule/Slack/cloud/model credential，不运行真实副作用实验。

## Skill 升格总判断

- **AOS authority-plane map：需二次验证。** 候选是中立 gate schema 和 fallback-boundary conformance，不迁移 Astrid/AOS runtime 或 hooks。
- **QM scope-resolution contract：需二次验证。** 候选是 immutable scope、ro/rw layers、tighten-only floor 与 pinned/tracked promotion semantics，不迁移完整多人 harness。
- **今日不升格。** 两个候选都与现有 path-portability、shared-memory-bridge、shared-skill-governance、verification/effect-scope 候选重叠；先做一个合并 fixture POC，再判断更新既有 skill 还是仅保留 runtime 验证工具。

## 明日继续

1. 建 `authority-plane-map` 离线 fixture，覆盖 Hermes terminal/tools/cron/bridge 的 hard/advisory gate、failure mode、fallback boundary 和 audit event。
2. 建 `scope-resolution-contract` fixture，把 curated/inbox/runtime/compat 映射成 org/agent layers，验证兼容 symlink 不放宽 canonical write target。
3. 合并两套 fixture 为 `scoped-authority-conformance`，验证 `(actor, ingress, scope, effect, policy floor, terminal state, receipt)`。
4. 若受控环境有 Rust toolchain，再运行 AOS `cargo test -p aos-mcp-broker`；不为无人值守日报自动安装系统 Rust。
5. 对 QM 补跑 `resolution-service`、ACL/audience-floor 和 skill ingest/materialize 定向 tests；仍不启动 Slack/Postgres/云部署。
6. 跟进 AOS issue #58/PR #74/#75 与 QM PR #106/#78/#107；只在 merge commit/test/release 出现后更新事实。

## 候选反哺

### Candidate Facts

- [ ] topic: same-policy-across-planes-does-not-imply-same-enforcement | evidence: AOS `policy::evaluate`、broker binding gate、`hook_gate` no-veto、broker docs 的 advisory native path | 建议: create/update authority/effect fact after fixture | 安全级别: high
- [ ] topic: policy-failure-must-name-fallback-boundary | evidence: AOS `load_rules` parse/validation failure → empty rules + loud audit + capability PEP | 建议: update verification contract after Hermes mapping | 安全级别: high
- [ ] topic: shared-context-needs-ro-rw-scope-composition | evidence: QM `resolution-service.ts` org ro + scope rw + team ro、audience/ACL resolution | 建议: candidate，先对 shared symlink/canonical targets 做 fixture | 安全级别: medium
- [ ] topic: scope-policy-should-tighten-org-floor | evidence: QM `composeSecurityPosture`、tests、README admin model | 建议: candidate；不能直接复制三档 posture 全序 | 安全级别: medium
- [ ] topic: skill-update-discovery-must-be-separated-from-promotion | evidence: QM tracked reconcile vs pinned updateAvailable + leader lease | 建议: update shared-skill governance after immutable commit test | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: authority-plane-conformance | 可复用场景: Hermes tools/cron/bridge、future-agent effect gates | 是否建议 shared: yes（验证后更新既有 skill） | 原因: 防止把 advisory hook 冒充 hard enforcement；与 verification/effect-scope 合并而非新建产品 skill
- [ ] 名称: scoped-authority-conformance | 可复用场景: shared memory、多 workspace、兼容入口、agent lane 写入 | 是否建议 shared: yes（POC 和治理后） | 原因: immutable scope + ro/rw + policy floor 是跨 Agent 横切契约
- [ ] 名称: aos-product-integration | 可复用场景: WASM Agent OS | 是否建议 shared: no | 原因: 依赖 Astrid、installer/capabilities/IPC，当前本机无 Rust/runtime 证据
- [ ] 名称: qm-product-integration | 可复用场景: 组织级 Slack/Web Agent | 是否建议 shared: no | 原因: 项目极新、Postgres/cloud/credential/sandbox surface 过大，当前只抽象 scope contract

### Candidate Open Questions

- [ ] 问题: Hermes 每类 tool/terminal/cron/bridge 的最终 hard chokepoint 与 fallback boundary 分别在哪里？ | reason: adaptation/security | priority: high
- [ ] 问题: shared hub 的 compat symlink 应如何被 conformance checker 解析，才能证明它只兼容读取而不成为新写入真相源？ | reason: adaptation | priority: high
- [ ] 问题: org floor、Agent-local policy 与 task-specific approval 是否能形成偏序而不是粗糙单一 rank？ | reason: design | priority: high
- [ ] 问题: Skill tracked mode 怎样绑定 resolve/fetch/reconcile 同一个 immutable commit，避免 HEAD TOCTOU？ | reason: security/gap | priority: high
- [ ] 问题: AOS policy load failure 的 loud audit 在实际部署中是否有 mandatory health gate，还是仅日志？ | reason: runtime-gap | priority: medium
- [ ] 问题: QM audience-floor origin-label gaps 修复前，哪些 mixed-permission context 必须直接 blocked？ | reason: security/stale | priority: high

### 不应自动落地

- 不运行 AOS `curl|sh` installer、init/migrate/update/daemon，不创建 `~/.aos`，不授予 ingress/capsule。
- 不运行 QM init/up、Slack/Web/Postgres/AWS/Fly，不加载 model/provider/connector credentials。
- 不修改 Hermes/OpenClaw config、model、provider、tools、skills、auth、env、cron；不调用 OpenClaw。
- 不把今日 candidate 直接写入 curated active fact 或 shared manifest；先完成 runtime POC、治理评分、去重、脱敏与人工/总控审查。
