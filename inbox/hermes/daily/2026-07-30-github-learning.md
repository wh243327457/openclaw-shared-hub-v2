# 2026-07-30 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> GitHub Repository API 最终核验时间：2026-07-29T23:34:14Z（北京时间 2026-07-30T07:34:14+08:00）  
> 固定源码快照：`xai-org/grok-build@500129c714ad1b10e6095481f4a8387a2ec52649`、`openai/codex-security@1a9fc9bed3cbdbffad04ba03f50ff483f06c5516`  
> 发现口径：GitHub Search API，查询 `created:>2026-07-01 stars:>100`，按 stars 降序；候选元数据随后用 Repository API 单独复核。Stars、forks、updated 会变化，本文数字只代表上述最终查询时点。

## 今日结论

今天的主线是：**Agent 的“完成”不能只是自然语言或进程退出，而应由宿主拥有的阶段边界、唯一终态和可验证 canonical artifact 共同证明。** Grok Build 在工具层使用 `Progress* + exactly-one Terminal`，在长上下文层对压缩触发、结果有效性和控制 token 做确定性校验；Codex Security 则把 discovery、validation、attack path、canonical JSON、seal 和 report projection 分开，并明确 incomplete coverage 不能冒充通过。对 Hermes/shared hub 最值得反哺的不是迁移两个产品，而是建立一个跨 workflow 的 **phase/terminal/artifact/coverage completion contract**。

## 证据与执行摘要

- **发现与元数据**：真实执行 `gh api /search/repositories` 与逐仓库 `gh api repos/{owner}/{repo}`；最终速览数据见下表。
- **源码**：对两个深读仓库执行 `git clone --depth 1`，分别固定到 `500129c7...` 与 `1a9fc9b...`；tracked paths 分别为 **2,937** 与 **177**。
- **来源交叉**：Grok Build 读取 README、内置 sandbox/permissions docs、SECURITY、Cargo manifests 和关键 Rust 源码；Codex Security 读取根/package README、SECURITY、scan contract、deep-scan skill、issue #109、package/lockfile 和关键 TypeScript 源码。
- **release/tags**：两个仓库的 GitHub `releases/latest` API 均返回 404。Grok Build 查询时未列出 tag；Codex Security 有 `npm-v0.1.0` 至 `npm-v0.1.3` tags，package 当前版本为 `0.1.3`。不得把 tag 自动说成 GitHub Release。
- **真实验证——Grok Build**：尝试 `cargo test -p xai-tool-runtime --lib`，本机真实返回 `/usr/bin/bash: cargo: command not found`（exit 127）；因此 Rust 编译、测试和运行行为均标记**待核验**，不借用上游测试文件冒充本机通过。
- **真实验证——Codex Security**：Node 为 `v22.14.0`，满足 package 的 `>=22`。首次 `pnpm test` 因本机无 `bun` 真实失败；随后用临时 `npm exec bun@latest` 运行：package **build 成功**、TypeScript **lint 成功**、测试 **425 pass / 4 skip / 0 fail**。4 个 skip 包括 real Codex integration 与 Windows-only 边界，因此不宣称真实模型扫描或完整跨平台验证通过。
- **runtime 证据**：浅克隆与依赖安装位于 `runtime/hermes/github-hot-project-learning/repos/`，属于机器本地临时证据，不进入 curated。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | **23,416** | 4,451 | Rust | **Apache-2.0** | 2026-07-29T22:31:27Z / 17:17:58Z | **深读：终态协议、压缩有效性、安全分层** |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | 10,596 | 1,386 | Python | MIT | 2026-07-29T23:32:57Z / 2026-07-28T19:34:17Z | 昨日已深读，今日作热度参照 |
| [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) | 8,127 | 618 | Python | Apache-2.0 | 2026-07-29T23:31:01Z / 17:25:09Z | 候选：procedural model quality gate |
| [oso95/scroll-world](https://github.com/oso95/scroll-world) | 5,742 | 661 | JavaScript | MIT | 2026-07-29T23:14:09Z / 04:44:56Z | 速览；偏前端 skill，不做实现结论 |
| [openai/codex-security](https://github.com/openai/codex-security) | **4,854** | 295 | TypeScript | **Apache-2.0** | 2026-07-29T23:32:33Z / 23:27:39Z | **深读：隔离 runtime、sealed artifacts、coverage truth** |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | 3,441 | 271 | Python | MIT | 2026-07-29T23:27:10Z / 2026-07-27T01:45:22Z | 候选：确定性文本质量规则 |
| [nyblnet/bento](https://github.com/nyblnet/bento) | 3,019 | 190 | TypeScript | MIT | 2026-07-29T23:15:57Z / 2026-07-28T18:09:26Z | 单文件办公套件，今日不深读 |
| [synthetic-sciences/openscience](https://github.com/synthetic-sciences/openscience) | 2,927 | 404 | TypeScript | Apache-2.0 | 2026-07-29T23:08:45Z / 17:10:43Z | 科研工作台候选，数据治理待核验 |

说明：Stars 不是代码质量、安全性、采用率或项目真实性证明；GitHub API 的 repo-level License 也不覆盖依赖、vendored code、模型、数据、商标与发布制品。

## 深读项目

### 1. xai-org/grok-build

**基本信息（GitHub Repository API）**

- URL：https://github.com/xai-org/grok-build
- Stars：**23,416**；Forks：**4,451**；Language：Rust；License：**Apache-2.0**。
- 创建：2026-07-14T20:04:23Z；updated：2026-07-29T22:31:27Z；pushed：2026-07-29T17:17:58Z。
- 固定 commit：[500129c714ad](https://github.com/xai-org/grok-build/commit/500129c714ad1b10e6095481f4a8387a2ec52649)，commit 时间 2026-07-29T17:17:54Z，message 为 `Synced from monorepo`。
- GitHub API 查询时 `open_issues_count=0`；这只说明公开仓库当时没有 API 计数的 open item，不证明内部 monorepo 无缺陷。
- `releases/latest` 返回 404，查询时未列出 tags；README 指向站外 changelog，因此公开仓库无法提供可复核的 GitHub release lineage。

#### 一句话判断

值得继续深读的不是 TUI 外观，而是它把**类型化工具、流式进度、唯一终态、压缩策略、压缩输出校验、权限规则和 OS sandbox**分成多个可测试层；这为 Hermes 的长任务、subagent、cron 和 shared artifact 审计提供了更具体的 completion contract。

#### 解决的问题：替代了什么旧做法

它替代了三类脆弱做法：

1. 把 stdout 最后一行、流 EOF 或“模型说完成”当作工具成功。
2. 上下文快满时直接截断历史，或接受空/畸形摘要并继续运行。
3. 仅用 prompt 约束危险命令，却没有工具级 deny、进程级 filesystem/network 限制和 environment secret filtering 的独立层。

关键边界是：这些层不是同一种安全保证。工具协议能发现缺终态，compaction validator 能拒绝某些无效摘要，permission rules 控制模型请求，kernel sandbox 控制进程实际可达范围；任何一层都不能替代其他层。

#### 架构 / 实现与数据流

```text
TUI / headless / ACP
        │
        ▼
xai-grok-shell / agent runtime
        │ typed tool call
        ▼
xai-tool-runtime::Tool / ToolDyn / ToolDispatch
        │
        ├── Progress* ───────────────► UI / event consumer
        └── exactly one Terminal ────► typed result or ToolError
                                         │
                                         ▼
                                   session history
                                         │ token pressure
                                         ▼
                     xai-grok-compaction::should_compact
                                         │
                              select → sample → validate
                                         │
                            cleaned continuation carrier
```

安全控制是旁路约束而非同一 pipeline：permission rules/hook 在请求层授权；sandbox 在整个进程生命周期内施加 Landlock/Seatbelt/bubblewrap/seccomp；shell environment policy 决定子进程继承哪些变量。

#### Repo tree 摘要

```text
grok-build/
├── README.md / SECURITY.md / LICENSE       # 产品说明、漏洞报告、Apache-2.0
├── Cargo.toml / Cargo.lock                 # 生成的 workspace root 与锁文件
├── .cargo/ / rust-toolchain.toml           # 构建配置与固定 Rust 工具链
├── crates/
│   ├── codegen/
│   │   ├── xai-grok-pager[-bin]/           # TUI 与 composition root
│   │   ├── xai-grok-shell/                 # agent/session/headless runtime
│   │   ├── xai-grok-tools/                 # terminal/edit/search 等工具
│   │   ├── xai-grok-workspace/             # filesystem/VCS/checkpoint
│   │   ├── xai-grok-sandbox/               # OS sandbox
│   │   └── ...                             # auth/config/MCP/memory/hooks/ACP
│   └── common/
│       ├── xai-tool-protocol/               # wire IDs/envelopes/capabilities
│       ├── xai-tool-runtime/                # typed Tool、stream、dispatch
│       ├── xai-grok-compaction/             # trigger/sample/validate/format
│       └── xai-circuit-breaker/...          # shared leaf crates
├── prod/mc/                                 # proxy/shared production types
└── third_party/                             # Mermaid graph stack vendored source
```

固定 commit 的 tracked paths 为 **2,937**；其中 `crates/codegen/*` 2,659 个、`crates/common/*` 172 个。root workspace 列出 80 余个成员，不能把“小型 CLI”当作简单依赖面。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/common/xai-tool-runtime/src/tool.rs` | typed tool + stream contract | blocking `run` 自动包装为 terminal-only stream；stream 形状为 `Progress* + Terminal`；`ToolDyn` 在单一边界做 JSON type erasure |
| `crates/common/xai-tool-runtime/src/dispatch.rs` | object-safe dispatch | `call_terminal` 丢弃 progress、接受首个 terminal；EOF 无 terminal 转稳定 `stream_no_terminal` 错误 |
| `crates/common/xai-grok-compaction/src/intra_compaction/trigger.rs` | token-pressure policy | enabled/context/step/mode/threshold 全部用纯函数决定，边界值有测试 |
| `crates/common/xai-grok-compaction/src/history/validate.rs` | compaction validity gate | 空文本拒绝；DivideAndConquer 的 `<chunk_summary>` 开闭数不平衡拒绝 |
| `crates/common/xai-grok-compaction/src/code_compaction/summary.rs` | continuation carrier 清洗 | 去 leading scratchpad、保护正文、neutralize echoed control tokens、退化摘要检测 |
| `crates/codegen/xai-grok-pager/docs/user-guide/18-sandbox.md` | OS enforcement contract | built-in/custom profiles、deny glob、Linux/macOS 差异、fail-open/fail-closed 条件 |
| `crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md` | authorization semantics | deny > ask > allow、shell segment caveats、always-approve 与 sandbox 分层 |
| `THIRD-PARTY-NOTICES` | supply-chain provenance | 18,898 行 notices；first-party license 不可覆盖全部依赖与 in-tree port |

#### 源码精读（固定 commit）

**代码块 1：blocking tool 自动进入统一 streaming 入口**  
来源：`crates/common/xai-tool-runtime/src/tool.rs:87-95`

```rust
fn execute(
    &self,
    ctx: ToolCallContext,
    args: Self::Args,
) -> impl Future<Output = ToolStream<Self::Output>> + Send {
    async move {
        let result = self.run(ctx, args).await;
        terminal_only(result)
    }
}
```

逻辑：runtime 永远调用 `execute`；简单工具只实现 `run`，框架将其转换为单一 terminal item。这样 blocking/streaming 工具共享同一 consumer protocol，不需要两套完成判定。边界是 helper 只能构造良好流；自定义 `execute` 仍可能违反 invariant，宿主 consumer 必须检测 EOF、重复 terminal 和 terminal 后事件。

**代码块 2：EOF 无 Terminal 明确成为协议错误**  
来源：`crates/common/xai-tool-runtime/src/dispatch.rs:50-67`

```rust
async fn call_terminal(
    &self,
    tool_id: ToolId,
    args: Value,
    ctx: ToolCallContext,
) -> Result<TypedToolOutput, ToolError> {
    let mut stream = self.call(tool_id, args, ctx).await;
    while let Some(item) = stream.next().await {
        match item {
            ToolStreamItem::Progress(_) => continue,
            ToolStreamItem::Terminal(result) => return result,
        }
    }
    Err(ToolError::custom(
        "stream_no_terminal",
        "dispatch stream ended without a terminal item",
    ))
}
```

逻辑：progress 不是成功；只有 terminal 才能结束。EOF 被分类为稳定协议错误，而不是 `None = done`。对 Hermes 最直接的迁移点是：background process/subagent/cron 的 `process exited` 还不够，必须有 terminal receipt 与 expected artifact。

**代码块 3：压缩触发是可测的纯策略函数**  
来源：`crates/common/xai-grok-compaction/src/intra_compaction/trigger.rs:117-148`

```rust
pub fn should_compact(
    policy: &IntraCompactionConfig,
    last_prompt_tokens: u32,
    context_window: u32,
    current_step: u32,
) -> Option<IntraCompactionTrigger> {
    if !policy.enabled || context_window == 0 {
        return None;
    }
    if policy.mode != IntraCompactionMode::FullReplace
        && current_step < policy.min_steps_before_compact
    {
        return None;
    }
    let threshold =
        (context_window as u64 * policy.trigger_threshold_percent as u64 / 100) as u32;
    if last_prompt_tokens <= threshold {
        return None;
    }
    let percent = (last_prompt_tokens as u64 * 100 / context_window as u64).min(100) as u8;
    Some(IntraCompactionTrigger {
        last_prompt_tokens, context_window, percent, step: current_step,
    })
}
```

逻辑：是否压缩与如何压缩分离；FullReplace 明确忽略 min-step，而 partial modes 要满足 step gate；等于 threshold 不触发。可迁移点是把 memory compaction 的 policy/version/input 指标放进 receipt，而不是让模型自行决定“该总结了”。边界是 token count/summary quality 的来源仍需核验，纯函数正确不代表采样结果有用。

**代码块 4：压缩输出在持久化前有最小有效性检查**  
来源：`crates/common/xai-grok-compaction/src/history/validate.rs:43-64`

```rust
pub fn validate_compaction_text(
    text_content: &str,
    strategy: &CompactionStrategy,
) -> Result<(), CompactionValidationError> {
    if text_content.trim().is_empty() {
        return Err(CompactionValidationError::EmptyContent);
    }
    if matches!(strategy, CompactionStrategy::DivideAndConquer) {
        let open_count = text_content.matches("<chunk_summary").count();
        let close_count = text_content.matches("</chunk_summary>").count();
        if open_count != close_count {
            return Err(CompactionValidationError::UnbalancedChunkTags {
                open: open_count,
                close: close_count,
            });
        }
    }
    Ok(())
}
```

逻辑：空摘要会在 hydration 时被跳过却可能阻挡未来 trigger，因此直接拒绝；DnC 标签失衡被视为截断/畸形。边界是“标签平衡”不证明事实完整、无 prompt injection、无敏感数据或包含任务关键状态；Hermes 需要再加 required sections、source refs、redaction 和 information-loss fixtures。

#### 依赖分析与供应链风险

- root `Cargo.toml` 是 generated/read-only workspace，使用 Rust edition 2024；`Cargo.lock` 存在，工具链由 `rust-toolchain.toml` 固定。
- 核心依赖包括 `agent-client-protocol 0.10.4`、Tokio、Axum、Reqwest/Rustls、Ratatui、Serde、SQLite、MCP、OAuth、OpenTelemetry、Git/Gix、image/PDF 与 platform bindings。
- `async-openai` 通过 git patch 固定到 commit `95b52e...`，`nucleo` 也使用 git revision；identity 较明确，但 registry+git+vendored source 混合增加 provenance/CVE 维护面。
- `xai-grok-shell` 明确把 `rusqlite` 升至 0.37 并启用 bundled SQLite，以处理注释中列出的 CVE；这是风险意识证据，不代表当前整图无 advisory。
- `THIRD-PARTY-NOTICES` 约 762 KB、18,898 行，另有 crate-local notices 与 `third_party/NOTICE`；README 还声明包含从 Codex/OpenCode 移植的 in-tree implementations。任何迁移都要逐段保留 notice，不能只看 Apache-2.0。
- 构建依赖 DotSlash 下载 hermetic `protoc`，`xai-grok-shell/build.rs` release build 还会处理 ripgrep；构建不是纯离线解析，需网络/制品 hash 与构建沙箱。

#### 真实测试结果

```text
cargo test -p xai-tool-runtime --lib && cargo test -p xai-grok-compaction should_compact
/usr/bin/bash: line 3: cargo: command not found
exit_code: 127
```

这只证明当前 WSL job 环境缺 `cargo`，不证明项目测试失败。源码中的 unit tests、README 的 build 命令和上游实现均已读取，但本次**没有编译、没有执行二进制、没有验证 sandbox kernel behavior**。为了完成日报不自动安装 Rust toolchain。

#### 可复用经验

- 当工具能产生进度或长时间运行时，应优先使用 `Progress* + exactly-one Terminal`，因为 EOF、process exit 与最后一条 progress 都不能证明业务完成；边界是 consumer 还必须拒绝双 terminal、terminal 后事件和缺 artifact。
- 当长上下文接近上限时，应优先把 compaction trigger 做成版本化纯策略，并在持久化前校验输出，因为“模型愿意总结”不是可复现策略；边界是结构有效不等于语义完整，仍需 required-state 与 source-evidence 测试。
- 当 prompt 中存在控制标签或 summarization instructions 时，应优先在 continuation carrier 层 neutralize live control tokens，因为原样回灌可能诱导下一轮重复控制行为；边界是字符替换不是完整 injection defense，外部数据仍应按 data 处理。
- 当安全要求跨模型工具和子进程时，应优先组合 permission rule、environment filtering 与 OS sandbox，因为任一层只能覆盖部分边界；边界是 Grok built-in sandbox 默认 `off`，且 Linux/macOS network/glob enforcement 不完全相同。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/completion-contract/` 建离线 fixture（今日只设计，未改生产逻辑）：

1. 定义 `Event = progress | terminal` 与 `Receipt = {run_id, scope, status, artifact_paths, schema_version}`。
2. 覆盖正常、EOF 无 terminal、双 terminal、terminal 后 progress、cancel、timeout、artifact missing、schema invalid。
3. 再加入 compaction fixture：empty summary、missing required state、unbalanced marker、control-token echo、source ref missing。
4. 只对 synthetic JSON/Markdown 运行，不连接 provider、不执行真实 tool、不改 config/cron。

#### 风险边界

- **License**：first-party 为 Apache-2.0；第三方 notices、vendored source 和 in-tree ports 必须另审，不整仓复制到 shared skill。
- **维护活跃度**：固定 commit 距查询约 6 小时，活跃；但仓库只创建约 16 天、来自内部 monorepo 周期同步、不接受外部贡献、无公开 release，公共治理透明度有限。
- **安全风险**：terminal/edit/web/MCP/hooks/plugins/custom models 都是高权面；sandbox 默认 off。built-in profile apply 失败可 warning 后继续，custom deny profile 才在特定错误下 fail closed。
- **平台差异**：Linux child network 可用 seccomp 阻断，macOS 文档明确为 no-op；Linux deny glob只覆盖启动时已存在文件，macOS runtime regex 更强。
- **摘要局限**：空/标签失衡检查很窄；事实遗漏、过期、source mismatch、secret 与恶意指令仍可能通过。
- **本机待核验**：缺 Cargo，因此 compile、unit tests、Landlock/bubblewrap/Seatbelt、ACP/headless runtime 全部待核验。
- **不可自动执行**：不安装/启用 Grok Build，不迁移其 provider/auth/hooks/plugins，不改 Hermes 模型、配置、tools、auth、env 或 cron。

#### Skill 升格判断

**需二次验证。** 可迁移的是 `completion-contract + compaction-validity` 模式，不是 Grok 产品或 Rust runtime。昨日已有 `tool-terminal-contract` candidate，今日应**更新并扩充**而不是新建重复 skill：加入 compaction receipt、required-state validation、control-token fixture 和 terminal/artifact 联合条件。当前本机 Rust lane blocked，且与 verification-first/subagent 四状态高度重叠，今天不直接升格 shared skill。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/completion-contract/{schema.json,events.jsonl,fixtures.json,test_contract.py,README.md}`。
2. **Hermes runner 候选接口**：`validate_completion(events, expected_artifacts, schema_version, scope) -> completed|failed|blocked|canceled`；process exit 0 只作 evidence，不单独决定 completed。
3. **GitHub 学习闭环适配候选**：把 `audit_score >= threshold`、报告存在、status schema 有效合并为最终 terminal guard；不改现有 cron，先用历史日报 fixture。
4. **memory compaction 候选**：raw 摘要留 `runtime/hermes/`；必须通过 required sections、source path、redaction、size/reduction 与 control-token tests 后才可成为 continuation artifact。
5. **shared hub 分层**：今日源码/stdout 留 runtime，本报告留 Hermes inbox；通过治理去重和人工/总控审查后，才更新 verification-first 事实或 `research/github-hot-project-learning` reference。
6. **future agent / OpenClaw 复用**：只共享 schema、fixtures、状态语义；本任务没有调用 OpenClaw，各 agent 在自己的最终 chokepoint 实现 enforcement。

---

### 2. openai/codex-security

**基本信息（GitHub Repository API）**

- URL：https://github.com/openai/codex-security
- Stars：**4,854**；Forks：**295**；Language：TypeScript；License：**Apache-2.0**。
- 创建：2026-07-13T22:00:13Z；updated：2026-07-29T23:32:33Z；pushed：2026-07-29T23:27:39Z；`open_issues_count=60`（含 PR，不能当作缺陷数）。
- 固定 commit：[1a9fc9bed3cb](https://github.com/openai/codex-security/commit/1a9fc9bed3cbdbffad04ba03f50ff483f06c5516)，commit 时间 2026-07-29T22:58:17Z，修正文档中的 CLI help 与 deep-scan configuration。
- package 版本：`0.1.3`；tags 有 `npm-v0.1.0` 至 `npm-v0.1.3`，但 GitHub `releases/latest` 返回 404。
- 活跃 issue：[#109](https://github.com/openai/codex-security/issues/109)（2026-07-29 open）报告共享可写 parent 下 scan output 在 completion 前可被替换；prepare 时的 0700/owner 检查没有在 registration/completion/contract load 重验。

#### 一句话判断

值得学的不是把 Codex Security 直接接入 Hermes，而是它将**输入预检、隔离 runtime、scan registration、重复 discovery、集中 validation、canonical artifacts、seal、projection、coverage 与 mutable triage**分离；这提供了“审计结果如何成为可长期比较事实”的完整反例与正例。

#### 解决的问题：替代了什么旧做法

它替代以下做法：

1. 扫描器直接写一份 Markdown，然后下游从 prose 反向解析 findings。
2. 发现一次就直接出报告，或把多个 worker 的复现次数当作漏洞成立证明。
3. 没扫完却因 findings 为空而 CI 通过。
4. 在目标 repository 内写 scan state/report，混淆被扫描输入与扫描器输出。
5. 批量扫描跟随 branch 名，重跑时目标已漂移；或失败后无法安全 resume。

其 contract 明确：canonical truth 是 `scan-manifest.json`、`findings.json`、`coverage.json`；`report.md` 和 SARIF 是 projection。mutable false-positive、external links、retention 与 sync state 要放到独立 workbench，而不能改写 sealed observation。

#### 架构 / 实现与数据流

```text
CLI / TypeScript SDK
        │
        ▼
preflight: repo + target + mode + output + auth selection
        │
        ▼
isolated CODEX_HOME + private state/output + bundled plugin
        │
        ▼
workbench register scan ──► target contract + scan_id + snapshot/revision
        │
        ▼
Codex thread (approvalPolicy="never", fixed permission profile)
        │
        ├── standard discovery
        └── deep repeated discovery ──► terminal discovery manifest
                                           │ hard phase boundary
                                           ▼
                          centralized validation + attack-path analysis
                                           │
                                           ▼
                 scan-manifest.json + findings.json + coverage.json
                                           │ validate + seal
                                           ▼
                         generated report.md / SARIF / CSV projections
                                           │
                                           ▼
                     separate mutable workbench triage and scan history
```

批量扫描是外层 supervisor：CSV 中每个 target 必须使用完整 immutable Git SHA；worker 将 checkout、artifact attempt 与 JSONL receipt 分离，完整 artifact bundle 才允许 resume 时 skip。

#### Repo tree 摘要

```text
codex-security/
├── README.md / SECURITY.md / LICENSE       # quickstart、threat model、Apache-2.0
├── Dockerfile / compose.yaml / docker/     # container workflow、seccomp、credentials
├── .github/workflows/                      # Node/container CI 与发布流程
└── sdk/typescript/
    ├── package.json / pnpm-lock.yaml        # ESM package、Node >=22、锁文件
    ├── src/
    │   ├── api.ts                           # CodexSecurity lifecycle 与 scan orchestration
    │   ├── runtime.ts                       # isolated home、output、plugin ZIP/Python boundary
    │   ├── targets.ts                       # target/path/diff normalization
    │   ├── multiscan.ts                     # pinned checkout、ledger、retry/resume
    │   ├── contract.ts / result.ts          # canonical artifact load/validation
    │   └── cli.ts / config.ts / auth.ts     # CLI、固定配置与凭据选择
    ├── _bundled_plugin/
    │   ├── skills/                          # discovery/validation/attack path/writeup/fix
    │   ├── references/                      # scan contract/final report/security rules
    │   ├── schemas/                         # manifest/findings/coverage JSON Schema
    │   ├── scripts/                         # Python workbench/finalizer/rank/validation
    │   └── examples/                        # completed-scan contract fixture
    └── tests-ts/                            # API/CLI/runtime/multiscan/security boundary tests
```

固定 commit 的 tracked paths 为 **177**：`sdk/typescript/src/*` 20 个、`tests-ts/*` 33 个、bundled plugin 95 个。仓库不大，但 package 同时携带 TypeScript、Python scripts、schemas、skills 与压缩的 MCP app assets，供应链不止 Node。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `sdk/typescript/src/api.ts` | scan lifecycle composition root | local validation 先于 runtime；isolated home/auth/output；scan registration；event loop；completion/failure；cleanup |
| `sdk/typescript/src/runtime.ts` | trust boundary | 0700 output、0600 auth、workbench secret filtering、plugin ZIP traversal/symlink/size/CRC checks、trusted Python |
| `sdk/typescript/src/multiscan.ts` | durable batch supervisor | full SHA inventory、scoped checkout、JSONL receipt+fsync、retry/resume、stale lock、artifact completeness |
| `sdk/typescript/src/targets.ts` | target identity | repository/path/diff normalization、trusted git executable、unsafe Git env rejection |
| `_bundled_plugin/references/scan-contract.md` | canonical semantics | immutable bundle、target snapshot、finding identity、coverage、seal 与 report projection |
| `_bundled_plugin/skills/deep-security-scan/SKILL.md` | phase ownership | repeated discovery 只负责 discovery；parent 集中 validation/attack path/finalization；terminal manifest 不是最终报告 |
| `sdk/typescript/package.json` | direct dependencies | Codex SDK/runtime、Ajv、Octokit、ZIP/PDF/TOML/CSV/CLI dependencies |
| `SECURITY.md` |真实边界 | local OS account 不是多租户；subprocess 可继承其他 credentials；prompt injection 本身不等于越界 |

#### 源码精读（固定 commit）

**代码块 1：preflight 只验证本地输入，不偷偷启动 runtime**  
来源：`sdk/typescript/src/api.ts:250-290`

```ts
public async preflight(
  repository: string,
  options: ScanOptions = {},
): Promise<ScanPreflight> {
  this.#requireOpen();
  const inputs = await this.#validateLocalInputs(
    repository,
    options,
    options.signal,
  );
  requireOutputOutsideRepository(
    inputs.protectedRoot,
    await realpath(tmpdir()),
    "temporary",
  );
  const configuration = await mergedCodexConfig(this.config);
  const model = scanModelConfiguration(configuration);
  validateScanCostLimit(options.maxCostUsd, model.model);
  // assemble plan; no scan runtime is started here
  return {
    repository: inputs.repository,
    target: inputs.target,
    mode: inputs.mode,
    outputDir: inputs.outputDir,
    authentication: scanAuthentication(this.#dependencies.environment, options.auth),
    ...model,
  };
}
```

逻辑：repository/target/mode/output/cost/auth selection 可以先成为 plan；README 明确 preflight 不初始化 runtime、不加载 credentials、不探测 plugin Python。可迁移点是 Hermes cron 在执行前输出 capability/effect/output plan。边界是 authentication 的 `verified:false` 表示选择来源而非验证可用，preflight success 不能直接升级为 runnable/completed。

**代码块 2：workbench 子进程显式去掉两类模型 key，但不是全环境净化**  
来源：`sdk/typescript/src/runtime.ts:121-148`

```ts
({ stdout } = await execFile(
  options.python,
  ["-I", "-B", join(options.pluginRoot, "scripts", "workbench_db.py"), ...args],
  {
    env: Object.fromEntries(
      Object.entries(options.environment).filter(
        ([name]) =>
          name.toUpperCase() !== "OPENAI_API_KEY" &&
          name.toUpperCase() !== "CODEX_API_KEY",
      ),
    ),
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
    windowsHide: true,
    signal: options.signal,
  },
));
```

逻辑：Python 使用 `-I -B`，不加载普通 user site/bytecode，并从 workbench env 去掉两个 API key。SECURITY 同时诚实说明其他 `GITHUB_TOKEN`、AWS 凭据仍可能继承。迁移原则不是复制 blacklist，而是对每类 subprocess 使用 include-only 环境 schema；边界是某些工具需要 credential，需按 effect/target 显式授予。

**代码块 3：plugin ZIP 在解压边界校验数量、路径、symlink、膨胀量和 CRC**  
来源：`sdk/typescript/src/runtime.ts:469-539`

```ts
export async function extractPluginZip(
  archive: string,
  destination: string,
  signal?: AbortSignal,
): Promise<string> {
  const staging = await realpath(
    await mkdtemp(join(dirname(destination), ".codex-security-plugin-")),
  );
  let expandedSize = 0;
  const paths = new Set<string>();
  const checksums: Array<{ path: string; checksum: number }> = [];
  await extractZip(archivePath, {
    dir: staging,
    onEntry(entry, archive) {
      if (archive.entryCount > MAX_ZIP_ENTRIES) throw new PluginBootstrapError(/*...*/);
      const path = safeArchivePath(entry.fileName);
      if (paths.has(path.toLowerCase())) throw new PluginBootstrapError(/*...*/);
      if (((entry.externalFileAttributes >>> 16) & 0o170000) === 0o120000)
        throw new PluginBootstrapError(/*...*/);
      if (entry.uncompressedSize > MAX_ZIP_ENTRY_SIZE)
        throw new PluginBootstrapError(/*...*/);
      expandedSize += entry.uncompressedSize;
      if (expandedSize > MAX_ZIP_EXPANDED_SIZE)
        throw new PluginBootstrapError(/*...*/);
      checksums.push({ path, checksum: entry.crc32 >>> 0 });
    },
  });
  // each extracted regular file is re-read and checked against recorded CRC
```

注：`/*...*/` 仅省略源码中的错误字符串，分支与限制来自固定文件。逻辑：解压先进入 private staging；大小写 collision、symlink、单项/总膨胀、backslash 路径、CRC 都有独立 gate。边界是 CRC-32 只检出传输损坏，不提供发布者真实性；仍需 package integrity、signature/provenance 和 trust policy。

**代码块 4：multiscan 只有 canonical artifacts 完整才允许 resume skip**  
来源：`sdk/typescript/src/multiscan.ts:105-133`

```ts
const ledger = join(output, "results.jsonl");
await ensureOutputDirectory(join(output, "checkouts"));
await ensureOutputDirectory(join(output, "artifacts"));
await ensureManifest(join(output, "manifest.json"), tasks);
const receipts = await readReceipts(ledger);
const pending: MultiscanTask[] = [];
let completed = 0;
for (const task of tasks) {
  const receipt = receipts.get(task.id.toLowerCase());
  if (
    receipt?.status === "completed" &&
    receipt.outputDir ===
      join(output, "artifacts", task.id, `attempt-${receipt.attempt}`) &&
    (await hasArtifacts(receipt.outputDir))
  ) {
    completed += 1;
  } else {
    pending.push(task);
  }
}
```

逻辑：JSONL receipt 写了 `completed` 仍不够；outputDir 必须等于 supervisor 计算出的 scoped path，而且四个 required artifacts 必须存在。输入 inventory 还要求完整 40/64 hex Git SHA；checkout 后再次核验 HEAD。边界是 `hasArtifacts` 当前只查文件存在，不在这里核验 seal/hash；真正消费 canonical bundle 还需 contract loader。issue #109 进一步表明 path 在时间上可能被替换，ownership/mode/object identity 要在最终 chokepoint 重验。

#### Canonical contract 的关键机制

`_bundled_plugin/references/scan-contract.md` 明确：

- canonical documents 是 `scan-manifest.json`（最大 16 MiB）、`findings.json`（128 MiB）、`coverage.json`（32 MiB）；oversize 在 seal 前拒绝。
- `report.md`、SARIF、CSV 是 projection，不是语义真相源；report 由 canonical JSON 确定性生成，producer 不应手写后再反解析。
- target kind 按实际 reviewed content 选择；clean revision、dirty worktree、diff、directory snapshot 使用不同 identity/digest 字段。
- finding identity 避免 line number，使用 stable rule family + semantic anchor + optional instance；fingerprint 只是 reconciliation signal，不是等价证明。
- coverage 区分 `complete / partial / unknown`，明确 included/excluded/deferred；`not observed` 不能冒充 `not scanned`。
- sealed observation 与 mutable triage 分开；false-positive、external links、retention 与 sync state不修改 canonical bundle。

Deep Security Scan skill 又增加硬 phase boundary：repeated discovery 只产生 terminal discovery manifest；parent 必须再执行统一 threat model、central validation、attack-path analysis、canonical JSON assembly 和 completion。候选多次出现只是 search evidence，不是 reportability proof。

#### 依赖分析与供应链风险

- package `@openai/codex-security` 版本 0.1.3、ESM-only、Node `>=22`，使用 pnpm 11.9.0；`pnpm-lock.yaml` 对 registry packages 含 integrity。
- direct runtime dependencies：`@openai/codex`/`@openai/codex-sdk 0.144.6`、Ajv 8.20.0、Octokit 7.0.6、Inquirer、Incur、extract-zip、fflate、PapaParse、pdfjs-dist、smol-toml。
- package 同时执行 bundled Python scripts；Python 3.10 还需 tomli。TypeScript lockfile不能覆盖 Python runtime、Codex native platform package、Docker base image与模型服务。
- plugin ZIP 具备 bounded extraction/CRC/manifest TOCTOU 防护；但真实性仍依赖 npm integrity、发布账户和所选 `pluginPath` trust。
- CI workflow/tag 与 release provenance 本次只读取文件和 tags，未核验 npm provenance、签名/SBOM 或每个 GitHub Actions run，均为**待核验**。
- issue #109 是当前明确未闭合的 local filesystem race：0700 scan dir 放在无 sticky bit 的共享可写 parent 下可被 rename+replacement。使用 private home 或 sticky `/tmp` 是已知缓解，但最终修复应在每次 resolution 重验 owner/mode/object identity。

#### 真实构建与测试结果

第一次按 package script 运行：

```text
npm exec --yes pnpm@11.9.0 -- test
$ bun test --timeout 30000 ./tests-ts
sh: 1: bun: not found
ELIFECYCLE Test failed
```

随后不修改项目源码，使用临时下载的 Bun 运行完整 package lane：

```text
npm exec --yes pnpm@11.9.0 -- run build
npm exec --yes pnpm@11.9.0 -- run lint
npm exec --yes bun@latest -- test --timeout 30000 ./tests-ts

425 pass
4 skip
0 fail
4128 expect() calls
Ran 429 tests across 29 files. [87.92s]
```

build 与 lint 之所以可判成功，是 shell 使用 `&&`，后续测试实际启动并最终 exit 0。四项 skip 是：real Codex/unchanged-plugin integration、一个 Windows login pipe fallback、一个 Windows trusted executable、一个 Windows canonical paths case。因此本次只验证 Node/Bun/fixture/Python workbench 的本地测试范围；**没有登录、没有读取或打印 API key、没有调用模型、没有扫描第三方目标、没有验证 Windows/macOS 与真实 Codex runtime**。

#### 可复用经验

- 当多个阶段共同产出最终报告时，应优先让每个阶段有唯一 owner 和硬 handoff manifest，因为 discovery 结束不等于 validation/report 完成；边界是 handoff artifact 本身还要 schema、path、scope 与 terminal reason 校验。
- 当报告要长期比较或导出多种格式时，应优先保存 sealed canonical JSON，把 Markdown/SARIF/CSV 当 projection，因为从 prose 反解析会丢 identity、coverage 与 evidence；边界是 mutable triage 必须另存，不能重写历史观察。
- 当扫描/审计可能未覆盖完整 scope 时，应优先将 coverage completeness 作为 success gate，因为 0 findings 可能只是没有扫描；边界是 complete 仍不证明无漏洞，只证明声明范围按 receipt 完成。
- 当批量任务需要 resume 时，应优先固定 immutable revision，并同时校验 receipt、computed output scope 与 required artifacts，因为 branch/单一状态字段都会漂移；边界是存在性还不够，最终消费还应验 seal/hash 与对象身份。
- 当 subprocess 处理高敏输入时，应优先使用 isolated runtime、private output 和 environment include-only policy，因为只过滤两个已知 key 会遗漏其他 cloud/token 凭据；边界是需要的 credential 应按 task/effect 最小授予。
- 当路径在高权流程中跨越时间窗口时，应优先在最终 completion/load chokepoint 重验 canonical path、owner、mode 与对象 identity，因为 prepare-time 检查会遭遇 rename/replacement race；边界是同一 OS account 不是该项目承诺的多租户边界。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/sealed-learning-bundle/` 建纯离线 POC（今日只设计）：

1. `run-manifest.json`：date、runner、input query、fixed commits、phase receipts、artifact hashes。
2. `projects.json`：项目元数据与 evidence paths；`coverage.json`：README/docs/issues/source/tests 各自 complete/partial/blocked。
3. Markdown 日报只从两份 canonical JSON 投影生成；mutable audit feedback 与 candidate review 单独保存。
4. fixture 覆盖 discovery-only、audit blocked、report replaced、hash mismatch、partial coverage、retry attempt drift。
5. 不调用真实 provider/安全扫描器，不改现有 orchestrator/config/cron。

#### 风险边界

- **License**：repo/package 为 Apache-2.0；Codex native runtime、transitive packages、Python runtime、模型服务和扫描目标各有独立条款。只抽象 contract，不复制整个 bundled security workflow 到 shared。
- **维护活跃度**：commit/issue 在查询前一小时内，活跃；但项目仅创建约 17 天、package 0.1.3、open items 60（含 PR），public API 在 1.0 前可变。
- **安全模型**：`approvalPolicy:"never"` 不等于只读；文档说明 profile 可读本地 filesystem、写 workspace roots/state，subprocess 可继承其他 credentials。只扫描受信且获授权的 repo。
- **已知 issue #109**：共享 parent replacement race 尚 open；不要在 group/world-writable 无 sticky parent 下放 scan output。
- **报告局限**：LLM-based security scanner 可漏报/误报；重复 discovery 不证明漏洞成立；central validation 也不能替代人工审查与真实测试。
- **测试局限**：425 pass 很强但 real Codex 与 Windows-only 4 项 skip；没有真实模型访问、网络授权、host sandbox 或发布制品验证。
- **适用边界**：Hermes/shared hub 当前不是 Codex plugin host；不应把其 deep-security skill 直接当 Hermes skill 运行。
- **不可自动执行**：不安装/登录 Codex Security、不读取环境 secret、不扫描用户仓库、不自动修复漏洞、不改模型/provider/config/auth/env/cron。

#### Skill 升格判断

**需二次验证。** 可迁移的是 `sealed canonical bundle + coverage truth + phase ownership`，不是 Codex Security 产品。该模式与 shared hub 现有 curated/raw/runtime 分层、verification-first 与 orchestrator protocol 高度一致，优先更新既有契约，不新建“Codex Security”产品型 shared skill。issue #109 说明 path revalidation 尚有缺口；在 Hermes 自有 artifact fixture 通过前不直接升格。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/sealed-learning-bundle/{run-manifest.schema.json,projects.schema.json,coverage.schema.json,fixtures/,project_report.py,test_bundle.py}`。
2. **现有 orchestrator 适配候选**：prepare/research/audit/knowledge-copy 四阶段各写 terminal receipt；`overall_status=completed` 同时要求 audit threshold、报告 schema、expected knowledge-base projection 与 hash。
3. **路径防替换候选**：在 final load/copy 前重验 resolved path 位于 expected root、不是 symlink、owner/mode 符合策略，并用 open file descriptor/stat identity 减少 check/use race；先做 fixture，不自动修改生产脚本。
4. **shared 分层映射**：inbox 报告=raw observation；runtime manifest/coverage/test stdout=机器证据；curated fact=经过治理审查的机制摘要；Obsidian 日报=projection，不反向成为事实真相源。
5. **Hermes 审计接口候选**：`complete = phase_terminal && artifacts_sealed && coverage != incomplete && audit_score >= threshold`；空 findings/空 issues 不单独代表 clean。
6. **跨 agent**：future-agent/OpenClaw 只消费 versioned schema 与 projection；每个 agent 的 mutable review 独立，不改写 sealed run。当前任务没有调用 OpenClaw。

## 横向对照：完成协议的四个层次

| 层次 | Grok Build | Codex Security | Hermes/shared hub 候选 |
|---|---|---|---|
| 事件终态 | `Progress* + Terminal`；EOF 无 terminal 是 error | scan event stream + completion/failure | 每个 runner/phase 恰好一个 terminal receipt |
| 阶段边界 | tool dispatch、compaction trigger/sample/validate | discovery manifest 后仍须 central tail | prepare/research/audit/project/knowledge 分 owner 与 handoff |
| artifact 真相 | typed output、cleaned continuation carrier | 3 个 sealed canonical JSON；report 是 projection | run manifest + project/evidence + coverage；日报是 projection/raw |
| 完整性 | empty/unbalanced compaction 拒绝 | incomplete coverage exit 2，不能冒充 pass | artifact exists + schema/hash + coverage + audit threshold |
| 安全边界 | permissions/env/sandbox 各层独立 | isolated home/output、fixed permission profile、path issue #109 | final chokepoint 重验 scope/effect/path/object identity |
| mutable 状态 | session/runtime 独立于工具结果 | triage/workbench 与 sealed observation 分开 | candidate review/反馈不修改历史 evidence bundle |

## 经验沉淀

1. 当工具或阶段能产生进度、重试或后台工作时，应优先使用 `Progress* + exactly-one Terminal + receipt`，因为 EOF、exit 0 和最后一条日志都不能证明业务完成；边界是还要拒绝重复终态并核验 expected artifacts。
2. 当长上下文需要压缩时，应优先把 trigger、selection、validation 和 continuation carrier 分开，并记录 policy/version/source，因为“摘要非空”不等于任务状态完整；边界是结构校验仍需 required facts、脱敏与 source evidence。
3. 当多个 worker 或阶段共同形成结论时，应优先明确 phase owner 与 hard handoff manifest，因为 discovery 完成、候选复现或 worker exit 都不是最终 validation；边界是 handoff 本身必须 schema-valid、scope-bound、terminal。
4. 当同一事实需要 Markdown、SARIF、CSV 或 Obsidian 展示时，应优先从 sealed canonical data 生成 projection，因为反向解析 prose 会丢 identity、coverage 和证据；边界是 projection 不应覆盖 canonical source。
5. 当审计或扫描可能只覆盖部分范围时，应优先把 coverage completeness 纳入 success gate，因为 0 findings 可能只是没有检查；边界是 complete 只证明声明流程完成，不证明目标无缺陷。
6. 当批量任务需要可恢复执行时，应优先固定 immutable revision 并联合校验 receipt、attempt、computed path、artifact seal，因为 branch、display name 和单一 completed flag 都可能漂移；边界是同一 revision 的外部依赖仍可能变化。
7. 当高权路径从 prepare 跨到 final completion 时，应优先在最终 chokepoint 重验 canonical path、owner、mode、scope 与对象 identity，因为 prepare-time 检查会遭遇替换竞态；边界是 shared OS account 本身通常不是强隔离边界。
8. 当 subprocess 可能继承 secret 时，应优先使用 include-only environment schema 与按 effect 最小授权，因为已知-key blacklist 会漏掉其他 provider/cloud token；边界是运行所需 credential 必须有显式来源与不落盘规则。

## 风险边界（全局）

- 本次由 Hermes 直接执行，未调用 OpenClaw，也未调用任何消息发送工具。
- 未修改 Hermes/OpenClaw 的模型、provider、tools、skills、auth、env、cron 或服务配置。
- 公开仓库元数据来自 GitHub API 查询时点；数字以后变化不构成报告错误，复用时应重新查询。
- 为验证 Codex Security 在 runtime clone 内下载 Node dependencies 与临时 Bun；没有调用真实 Codex、模型、MCP、安全扫描或外部副作用。
- Grok Build 因本机缺 Cargo 未编译/测试；不能把源码测试或 README 命令写成本机通过。
- Codex Security 的 425 pass 不覆盖 4 skip、真实模型扫描、Windows/macOS、npm release provenance 与 issue #109 修复。
- 不自动写 `curated/memory` active fact，不升格 shared skill；所有候选先走评分、证据、去重、脱敏与人工/总控审查。

## Skill 升格总判断

- **Grok Build completion/compaction 模式：需二次验证。** 更新昨日 `tool-terminal-contract` candidate，补 phase/artifact/compaction validity，不新建重复产品型 skill。
- **Codex Security sealed bundle/coverage 模式：需二次验证。** 优先更新 verification-first、orchestrator protocol 或 GitHub learning workflow reference；不迁移完整安全扫描器。
- **今日动作：暂不升格。** 两个模式共同支持 `phase-terminal-artifact-coverage contract`，但 Grok 本机测试 blocked，Codex 路径 replacement 仍有 open issue，且与既有 shared 能力重叠；先完成统一离线 POC 和去重矩阵。

## 明日继续

1. 建立统一 `completion-contract` synthetic fixture：EOF/no terminal、double terminal、terminal-after-progress、artifact missing/schema invalid/hash mismatch、partial coverage。
2. 在历史 GitHub learning status/report 上做 read-only adapter，验证 `overall_status=completed` 是否真的同时对应报告、audit、knowledge projection；不修改 cron。
3. 为 compaction 加 required-state 与 source-ref fixtures，验证空/短/标签平衡但语义缺失的摘要不会被错误接受。
4. 跟进 Codex Security issue #109：只在出现修复 commit/test 后更新判断；关注是否在 registration/completion/load 全部重验 parent/owner/mode/object identity。
5. 若环境已有受控 Rust toolchain，再定向运行 Grok `xai-tool-runtime` 与 `xai-grok-compaction` tests；不为日报自动改系统工具链。
6. 将候选与 `autonomous-learning/orchestrator-protocol`、verification-first fact、subagent 四状态和 GitHub learning skill 做去重，决定更新 reference 还是创建窄 shared contract。

## 候选反哺

### Candidate Facts

- [ ] topic: completion-requires-terminal-plus-artifact-plus-coverage | evidence: Grok `ToolDispatch::call_terminal`、Codex scan contract/multiscan、Codex 425 pass | 建议: update verification-first / orchestrator facts | 安全级别: low
- [ ] topic: compaction-output-needs-semantic-receipt-not-just-nonempty-text | evidence: Grok trigger/validate/summary fixed commit；本机 Cargo blocked | 建议: candidate，先做 Hermes fixture | 安全级别: medium
- [ ] topic: sealed-canonical-observation-separate-from-projection-and-mutable-triage | evidence: Codex `scan-contract.md` + schema/workbench architecture | 建议: update shared governance after de-dup | 安全级别: low
- [ ] topic: final-path-revalidation-after-prepare | evidence: Codex issue #109（open，尚未修复） | 建议: pending/open question，不写 active fact as solved | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: phase-terminal-artifact-coverage-contract | 可复用场景: cron、subagent、研究、巡检、批处理、future-agent | 是否建议 shared: yes（验证并去重后） | 原因: 横跨 agent；应优先并入 existing orchestrator/verification capability
- [ ] 名称: sealed-learning-bundle | 可复用场景: GitHub/教程/安全研究日报及 Obsidian projection | 是否建议 shared: yes（POC 后） | 原因: 避免 prose 反解析；需先证明维护成本和 path safety
- [ ] 名称: grok-build-integration | 可复用场景: coding agent | 是否建议 shared: no | 原因: runtime/依赖/权限面过大，与 Hermes 当前目标不符
- [ ] 名称: codex-security-integration | 可复用场景:真实安全扫描 | 是否建议 shared: no | 原因: 需要独立授权、credential、扫描目标与产品运行时；本任务只抽象 workflow contract

### Candidate Open Questions

- [ ] 问题: Hermes 当前哪个 chokepoint 能统一拒绝 no-terminal、double-terminal、artifact-missing 与 partial-coverage？ | reason: adaptation | priority: high
- [ ] 问题: shared hub 的 inbox 日报与 Obsidian 副本是否需要 content hash/manifest，谁是 projection、谁是 raw source？ | reason: adaptation | priority: high
- [ ] 问题: compaction 如何验证 required task state、source evidence 与 secret redaction，而不把格式模板误当语义质量？ | reason: gap | priority: high
- [ ] 问题: issue #109 的修复能否在不依赖 path-string race 的情况下绑定 open directory/file identity？ | reason: stale/security | priority: high
- [ ] 问题: canonical bundle seal 应由 job runner、audit stage 还是 independent finalizer 持有，避免同一进程自证？ | reason: design | priority: medium

### 不应自动落地

- 不安装或启用 Grok Build，不复制其 Rust runtime、hooks、plugins、providers 或 sandbox 配置。
- 不登录或运行 Codex Security，不读取 secret，不扫描用户或第三方 repository，不自动修漏洞。
- 不修改 Hermes/OpenClaw 的 config、model、provider、tools、skills、auth、env、cron；本任务未调用 OpenClaw。
- 不把今日 candidate 直接写入 `curated/memory` active fact 或 shared skill manifest；先完成 runtime POC、治理评分、去重、脱敏和审查。
