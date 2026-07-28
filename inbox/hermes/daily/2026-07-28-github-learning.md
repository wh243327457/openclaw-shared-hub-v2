# 2026-07-28 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> API 核验时间：2026-07-28T07:34:25+08:00  
> 固定源码快照：`xai-org/grok-build@02d9359435d0e9c20a20945679389cdce441e431`、`JustVugg/colibri@1b8b62ee75e33685508c26d10424460f857cd85d`  
> 发现口径：GitHub Search API，查询 `created:>=2026-07-01 stars:>100`，按 stars 降序；元数据再用各仓库 API 单独复核。Stars、更新时间会继续变化，本文数字只代表上述查询时点。

## 今日结论

今天的主线不是“再找一个更大的 Agent”或“把大模型硬塞进内存”，而是研究两种可迁移的**确定性外壳**：Grok Build 用类型化流协议、策略优先级和 OS sandbox 约束 Agent 工具副作用；Colibrì 用可测量的热度、确定性分流、分层驻留和失败降级把稀疏 MoE 权重当作可调度数据。两者共同提示：**LLM/路由器负责选择，宿主必须负责身份、终态、预算、权限和退化语义。**

## 证据与执行摘要

- GitHub API：逐仓库核验 stars、forks、language、license、created/updated/pushed。
- 源码：对两个仓库做 `git clone --depth 1`，固定到上面的 commit；GitHub recursive tree 分别统计到 2,918 与 240 个 blob。
- README/docs/issues/releases：
  - Grok Build：读取 README、sandbox/headless/permissions/skills 文档；GitHub `releases/latest` 返回 404，仓库 API 的 open issues 为 0，故用最近同步 commit 作为活跃性补证，不虚构 release。
  - Colibrì：读取 README、构建/CI、源码、最新 release `v1.1.1`（2026-07-22 发布）及 issue #653。
- 真实运行：Colibrì 的 `make test-c` 在本机成功退出 0，覆盖 25 个 C 测试二进制；编译时出现 `test_int3.c` 的 `t.gs` “used uninitialized” warning 与 `test_e8_kernel.c` 的未使用全局 warning，测试本身全部通过。
- 运行阻塞：Grok Build 的 `cargo test -p xai-tool-runtime` 未执行，真实返回 `/usr/bin/bash: cargo: command not found`（exit 127）；因此其编译/测试结论标记为**待核验**，只做静态源码分析。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | Created / Updated (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | 22,998 | 4,345 | Rust | Apache-2.0 | 2026-07-14 / 2026-07-27T23:32:31Z | 深读：Agent 工具运行时、权限、sandbox |
| [JustVugg/colibri](https://github.com/JustVugg/colibri) | 20,160 | 2,023 | C | Apache-2.0 | 2026-07-01 / 2026-07-27T23:33:57Z | 深读：MoE 权重分层与可测退化 |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | 8,636 | 1,124 | Python | MIT | 2026-07-20 / 2026-07-27T23:34:08Z | 候选：worker 运行时，今日未深读 |
| [unicity-aos/aos-ce](https://github.com/unicity-aos/aos-ce) | 7,612 | 12 | Rust | NOASSERTION | 2026-07-12 / 2026-07-27T22:57:46Z | License 未由 API 识别，暂不复制源码 |
| [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) | 6,890 | 523 | Python | Apache-2.0 | 2026-07-15 / 2026-07-27T23:24:38Z | 候选：质量门控的图像到程序模型 |
| [oso95/scroll-world](https://github.com/oso95/scroll-world) | 5,507 | 631 | JavaScript | MIT | 2026-07-06 / 2026-07-27T23:30:41Z | 候选：skill 产物，今日未核验实现 |
| [elder-plinius/T3MP3ST](https://github.com/elder-plinius/T3MP3ST) | 5,263 | 1,088 | TypeScript | AGPL-3.0 | 2026-07-02 / 2026-07-27T22:32:10Z | 攻防与 AGPL 边界较高，不自动运行 |
| [withmarbleapp/os-taxonomy](https://github.com/withmarbleapp/os-taxonomy) | 3,694 | 640 | JavaScript | ODbL-1.0 | 2026-07-08 / 2026-07-27T15:57:02Z | 数据库权利/署名边界需单独核验 |

说明：`NOASSERTION` 仅表示 GitHub API 未识别出 SPDX license，不等价于“无版权限制”。未深读项目不做代码结论。

## 深读项目

### 1. xai-org/grok-build

**基本信息（GitHub API）**

- URL：https://github.com/xai-org/grok-build
- Stars：**22,998**；Forks：**4,345**；Language：Rust；License：**Apache-2.0**。
- 创建：2026-07-14T20:04:23Z；updated：2026-07-27T23:32:31Z；pushed：2026-07-27T17:54:39Z。
- 固定 commit：[02d9359435d0](https://github.com/xai-org/grok-build/commit/02d9359435d0e9c20a20945679389cdce441e431)，commit 时间 2026-07-27T17:54:34Z；根 `SOURCE_REV` 为 `1adcd1f477870e4a97bacbd6be78c8a3bfbac46d`。
- GitHub `releases/latest`：404；API `open_issues_count=0`。这两项只按 API 原样记录，不推断“无缺陷”或“已稳定”。

#### 一句话判断

值得学的不是 TUI 外观，而是它把“工具的类型化实现、JSON wire、流式进度、唯一终态、权限策略、OS sandbox”拆成多个可审计层；这与 Hermes/shared hub 需要的 verification-first 与 effect scope 非常接近。

#### 解决的问题：替代了什么旧做法

它替代了三类脆弱做法：

1. 工具只返回一坨自由 JSON，调用方无法知道 schema、进度和终态。
2. 把“模型说这是只读”或单个 allow 前缀当作最终授权。
3. 只在工具 wrapper 内做路径检查，shell、子进程、subagent 可绕过同一边界。

Grok Build 的策略是：具体工具实现保持类型化；在 `ToolDyn` 边界完成 JSON 解码/编码；流必须以一个 `Terminal` 结束；策略按 deny > ask > allow；不确定 shell 解析 fail closed 到 Ask；需要强隔离时再由 Landlock/Seatbelt/bubblewrap 约束整个进程。

#### 架构 / 实现与数据流

```text
Prompt / TUI / headless / ACP
        │
        ▼
xai-grok-shell + xai-grok-agent
        │  list/route tool, lifecycle, session
        ▼
xai-tool-runtime::ToolDyn / ToolDispatch
        │  JSON Args -> typed Args; typed Output -> JSON + model_output
        ▼
concrete xai-grok-tools implementation
        │
        ├─ Progress* ───────────────► UI / streaming-json
        └─ exactly one Terminal ────► result / error / receipt

Before effect:
PreToolUse hook -> compiled permission rules -> grants/default mode
                                        │
                                        └─ process-wide sandbox (optional)
```

核心模块与依赖关系：

- `xai-tool-protocol`：ToolId、能力、wire frame。
- `xai-tool-runtime`：类型化 `Tool`、对象安全 `ToolDyn`/`ToolDispatch`、流 invariant、error taxonomy。
- `xai-grok-tools`：terminal、file edit、search 等具体工具。
- `xai-grok-workspace`：FS/VCS/执行/checkpoint/permission/sandbox 对接。
- `xai-grok-shell`：Agent runtime、leader/stdio/headless。
- `xai-grok-pager`：TUI；`xai-grok-pager-bin` 是 composition root。

#### Repo tree 摘要

```text
grok-build/
├── Cargo.toml / Cargo.lock        # 生成的 workspace 根与锁文件
├── rust-toolchain.toml            # 固定 Rust 1.92.0 + clippy/rustfmt
├── SOURCE_REV                     # 上游 monorepo revision
├── crates/
│   ├── common/
│   │   ├── xai-tool-protocol/     # wire IDs、frames、handshake
│   │   ├── xai-tool-runtime/      # Tool/ToolDyn/dispatch/stream/error
│   │   └── xai-circuit-breaker/   # 失败窗口与 breaker
│   └── codegen/
│       ├── xai-grok-agent/        # Agent、plugin/skill registry
│       ├── xai-grok-shell/        # 主运行时与 headless/stdio
│       ├── xai-grok-tools/        # 工具实现
│       ├── xai-grok-workspace/    # FS/VCS/permission/checkpoint/sandbox
│       └── xai-grok-pager*/       # TUI、render、binary composition
├── prod/mc/                       # proxy/shared types
└── third_party/                   # Mermaid/graph layout 等 vendored source
```

GitHub recursive tree 对固定 commit 返回 **2,918 个 blob**。README 明确根 `Cargo.toml` 由生成器产生，应视为只读并优先改 per-crate manifest。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/common/xai-tool-runtime/src/tool.rs` | 工具主契约 | typed Args/Output、`Progress* + Terminal`、type erasure |
| `crates/common/xai-tool-runtime/src/dispatch.rs` | 对象安全 dispatch | `call_terminal` 排空 progress；无 Terminal 明确报协议错误 |
| `crates/codegen/xai-grok-workspace/src/permission/policy.rs` | permission policy | deny > ask > allow；shell 链拆分、wrapper peel、`bash -c` 递归、失败 Ask |
| `crates/codegen/xai-grok-pager/docs/user-guide/18-sandbox.md` | OS sandbox 契约 | Linux Landlock/bwrap/seccomp，macOS Seatbelt，deny glob 平台差异 |
| `crates/codegen/xai-grok-pager/docs/user-guide/14-headless-mode.md` | 自动化协议 | JSON/streaming-json、tool filter、max turns、最后 `end` 事件 |
| `crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md` | 权限顺序与陷阱 | hook/rule/grant/mode 顺序，链式 shell 与 allow 前缀边界 |
| `Cargo.toml` / `Cargo.lock` | 供应链真相 | 大型 workspace、git/path/crates.io 依赖与锁定结果 |

#### 源码精读（固定 commit）

**代码块 1：`Tool::execute` 给简单工具一个终态 wrapper**  
来源：[`tool.rs#L79-L111`](https://github.com/xai-org/grok-build/blob/02d9359435d0e9c20a20945679389cdce441e431/crates/common/xai-tool-runtime/src/tool.rs#L79-L111)

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

fn run(
    &self,
    _ctx: ToolCallContext,
    _args: Self::Args,
) -> impl Future<Output = Result<Self::Output, ToolError>> + Send {
    async move {
        Err(ToolError::not_implemented(
            "Tool must implement either `run` or `execute`",
        ))
    }
}
```

逻辑：简单工具只实现 `run`；默认 `execute` 把结果包装为唯一 Terminal。两者都不实现时不是空成功，而是显式 `NotImplemented`。这让 blocking 与 streaming 工具共享同一消费协议。

**代码块 2：`with_progress` 构造 Progress* + Terminal**  
来源：[`tool.rs#L202-L227`](https://github.com/xai-org/grok-build/blob/02d9359435d0e9c20a20945679389cdce441e431/crates/common/xai-tool-runtime/src/tool.rs#L202-L227)

```rust
pub fn with_progress<T, P, F>(progress: P, terminal: F) -> ToolStream<T>
where
    T: Send + 'static,
    P: Stream<Item = ToolProgress> + Send + 'static,
    F: Future<Output = Result<T, ToolError>> + Send + 'static,
{
    let progress = progress.map(ToolStreamItem::Progress);
    let tail = stream::once(async move {
        ToolStreamItem::Terminal(terminal.await)
    });
    Box::pin(progress.chain(tail))
}
```

逻辑：progress 完全排空后才 await terminal future，避免两条消费者同时拉同一个 upstream；协议构造器天然把 Terminal 放在尾部。但“exactly one”仍是实现契约，恶意/错误的自定义 stream 需要消费者校验。

**代码块 3：`call_terminal` 不把无终态 stream 当成功**  
来源：[`dispatch.rs#L42-L67`](https://github.com/xai-org/grok-build/blob/02d9359435d0e9c20a20945679389cdce441e431/crates/common/xai-tool-runtime/src/dispatch.rs#L42-L67)

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

逻辑：只关心最终结果的调用者可丢弃 progress；第一条 Terminal 立即返回；EOF 无 Terminal 被识别为协议违规，而不是“没有报错所以成功”。这正适合 cron/audit 的 completed 判定。

**代码块 4：权限决策优先级独立于规则顺序**  
来源：[`policy.rs#L220-L277`](https://github.com/xai-org/grok-build/blob/02d9359435d0e9c20a20945679389cdce441e431/crates/codegen/xai-grok-workspace/src/permission/policy.rs#L220-L277)

```rust
pub fn evaluate(&self, access: &AccessKind) -> Option<Decision> {
    let mut matched_ask = false;
    let mut matched_allow = false;
    for (rule, matcher) in self.config.rules.iter().zip(&self.matchers) {
        if !tool_filter_matches(access, &rule.tool) { continue; }
        if !pattern_matches(access, &CompiledRule { rule, matcher: matcher.as_ref() }) {
            continue;
        }
        match rule.action {
            RuleAction::Deny => return Some(Decision::Reject(/* reason */)),
            RuleAction::Ask => matched_ask = true,
            RuleAction::Allow => matched_allow = true,
        }
    }
    if matched_ask { return Some(Decision::Ask); }
    /* Bash allow additionally requires every peeled segment to be allowed. */
    if matched_allow { return Some(Decision::Allow); }
    None
}
```

逻辑：deny 立即返回，ask 压过 allow。实际源码还对 Bash 使用 `bash_chain_fully_allowed`，要求拆出的每个 segment 都满足 allow；对无法分解、wrapper 耗尽、动态 `-c` 等情况提升到 Ask。注意 docs 还披露一个边界：普通 `Bash(git *)` 的全串前缀匹配可能覆盖 `git status && rm ...`，因此必须配合 segment deny/ask 或 `dontAsk`/sandbox，不能只看 allow 文本。

#### 依赖分析与供应链风险

`xai-tool-runtime/Cargo.toml` 的核心依赖为 `async-trait`、`futures`、`schemars`、`serde(_json)`、`tokio-util` 与三个内部 protocol/types crate。更大的 workspace 还依赖 Tokio、Axum、Reqwest、Tonic、OpenTelemetry、Ratatui、Git/SQLite、tree-sitter 等。

核验到的供应链特征：

- 根有 `Cargo.lock`，Rust 固定到 `1.92.0`；这是可复现基础，但不等于已做漏洞/license 审计。
- `async-openai` 被 patch 到 `our-forks/async-openai` 的完整 git rev；`nucleo` 也是 git rev；git dependency 会增加上游可用性与审计负担。
- `third_party/` 内 vendored Mermaid/graph stack；README 指向 `THIRD-PARTY-NOTICES`，Apache-2.0 不能自动覆盖所有 vendored 代码原 license。
- 构建要求 DotSlash 下载/运行 hermetic tools（如 protoc）；任何“构建即执行”的 binary、`build.rs`、proc macro 都应在隔离环境审计。
- 仓库由 monorepo 定期同步，外部贡献不接受；公开 tree 与内部 monorepo revision 的差异需要持续跟踪。
- 本机没有 Cargo，**未真实编译**；不能据源码存在测试就宣称当前 commit 通过。

#### 可复用经验

- 当工具既要支持简单阻塞返回又要支持长任务进度时，应优先统一为 `Progress* + exactly-one Terminal` 协议，并让无 Terminal 明确失败；边界是还需为 cancel、duplicate Terminal、超时与 receipt 建 fixture。
- 当工具实现需要类型安全但 wire/registry 需要对象安全时，应优先在单一 adapter 做 typed Args/Output 与 JSON 的转换，并保留 model-facing output；边界是 schema 声明仍不能替代运行时 effect enforcement。
- 当 shell 命令可含链、wrapper 或 `bash -c` 时，应优先拆分后逐段执行 deny/ask，解析不确定时 fail closed；边界是 OS、shell 方言和 symlink 仍需 kernel sandbox 或更强执行器。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/tool-terminal-contract/` 做纯 Python fixture（**建议，今日未创建**）：输入四条模拟流：正常 Terminal、Progress+Terminal、EOF 无 Terminal、双 Terminal；输出 `completed/failed/blocked/protocol_error`，再把相同 fixture 对照现有 cron `status.json` completed 规则。全程不调用真实 provider、不执行 shell、不改 Hermes 配置。

#### 风险边界

- **License**：first-party Apache-2.0；vendored/in-tree ports 必须继续看 notices，不整仓复制到 shared skill。
- **维护活跃度**：固定 commit 距查询不足一天；但仓库仅创建两周、无 GitHub release，长期 API/兼容稳定性待核验。
- **安全**：sandbox 默认 off；Linux 与 macOS 网络/deny glob 语义不同，Linux 对启动后新建且匹配 glob 的文件只 best-effort。built-in HTTP 工具不受 child-network seccomp 限制。
- **局限/不适用**：体量大（2,918 blobs）、monorepo 同步、Grok-specific；不适合直接成为 Hermes 依赖。Cargo 未安装导致本机测试待核验。
- **不可自动执行**：不安装 Grok、不执行其 install script、不更改 Hermes provider/tools/cron/secret，不把其默认权限策略直接套到生产。

#### Skill 升格判断

**需二次验证。** 候选不是“Grok Build skill”，而是窄化的 `terminal-tool-contract` / `effect-policy-fixtures`。它与已有 verification-first、subagent 四状态和近几日 effect-scope candidate 高度重叠，应优先更新既有候选/POC，不新建重复 shared skill。完成 cancel/timeout/duplicate-terminal、shell ambiguity、scope/effect fixture 与治理审查后，才考虑更新 `capabilities/skills/autonomous-learning/...`；今天只保留 raw 报告和 runtime POC 建议。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/tool-terminal-contract/{README.md,schema.json,fixtures.json,test_contract.py}`。
2. **Hermes 审计接入候选**：让学习/cron status 的 completed 同时要求“唯一终态 + artifact exists + audit threshold”，但先在副本 fixture 验证，不能直接改 cron。
3. **共享候选**：通过后把协议步骤合并到现有 verification-first / self-reflection shared skill 的 `SKILL.md` 和少量 reference；不要复制 Grok Rust 源码。
4. **治理路径**：候选先写 inbox/runtime，经 evidence、去重、脱敏与 review 后才可进入 `curated/memory/facts/`；本次未写 active fact。

---

### 2. JustVugg/colibri

**基本信息（GitHub API）**

- URL：https://github.com/JustVugg/colibri
- Stars：**20,160**；Forks：**2,023**；Language：C；License：**Apache-2.0**。
- 创建：2026-07-01T12:27:49Z；updated：2026-07-27T23:33:57Z；pushed：2026-07-27T23:33:17Z。
- 固定 commit：[1b8b62ee75e3](https://github.com/JustVugg/colibri/commit/1b8b62ee75e33685508c26d10424460f857cd85d)，commit 时间 2026-07-26T22:50:49Z。
- 最新 release：[v1.1.1](https://github.com/JustVugg/colibri/releases/tag/v1.1.1)，published 2026-07-22T22:03:15Z。
- 活跃 issue：[#653](https://github.com/JustVugg/colibri/issues/653)，2026-07-27 创建并更新，报告 GB10 unified memory 自动预算使用分层分配前快照，导致 OOM kill。

#### 一句话判断

值得学的是“把稀疏权重视作可调度工作集”而不是其 744B 宣传数字：确定性路由、coalesced read、LRU/LFRU 热驻留、批内去重、lookahead、镜像失败回落，都能抽象成大工件/索引/缓存的宿主调度原则。

#### 解决的问题：替代了什么旧做法

传统本地推理要求所有权重驻留 RAM/VRAM，容量不足就不能运行，或通过悄悄降低精度/改变路由换速度。Colibrì 把 dense 部分常驻，把 routed experts 跨 VRAM/RAM/NVMe 分层；placement 只决定速度，默认不静默改变 router 与 precision。它还用批内 expert union、三矩阵相邻的一次 `pread`、异步加载、下一层预测与双 SSD 确定性分流减少重复 I/O。

注意：README 的 744B、约 25GB RAM、速度与 71.6% 可预测性属于上游测量声明；本次没有 372GB 模型和对应硬件，**未独立复现实机推理/benchmark**。

#### 架构 / 实现与数据流

```text
prompt tokens
    │
    ▼
attention + router (dense, resident)
    │ top-K expert IDs per token
    ▼
batch-union unique experts
    │
    ├─ hit: VRAM pinned / RAM pinned / per-layer cache
    └─ miss: deterministic primary/mirror fd
               │ prefetch / io_uring / worker pool
               ▼
        coalesced expert slab (gate + up + down)
               │
               ▼
      CPU/CUDA/HIP/Metal expert matmul
               │
               ▼
      usage heat + recency update -> later repin
```

核心不变量：

- 同一 `(layer,eid)` 的 prefetch 与 demand read 必须去同一副本，否则 page cache 重复且 miss 行为漂移。
- Mirror 读失败回 primary，不改变 token；partial mirror 可用。
- batch 内同一 expert 只加载一次。
- 热度主要、最近性次要，并有 25%+4 hysteresis，避免驻留 slot 抖动。
- speculative/prefetch 失败不应杀死主服务；demand/fatal 路径保持诚实失败。

#### Repo tree 摘要

```text
colibri/
├── Makefile                     # 委托到 c/ 的统一入口
├── pyproject.toml               # `coli` Python launcher；可选 convert/oracle/bench
├── c/
│   ├── colibri.c                # GLM 主引擎（当前实际文件；README tree 仍写 glm.c）
│   ├── olmoe.c                  # OLMoE 路径
│   ├── tier.h                   # 热驻留/LFRU 选择
│   ├── st.h / quant.h / tok.h   # tensor container/量化/tokenizer
│   ├── backend_cuda.cu          # CUDA/HIP 单源 backend
│   ├── backend_loader.c         # Windows CUDA DLL 动态加载
│   ├── openai_server.py         # OpenAI-compatible gateway
│   ├── tools/                   # 转换、oracle、benchmark、诊断
│   └── tests/                   # C/Python/CUDA/Metal fixtures
├── docs/                        # tuning/API/CUDA/Metal/bench/实验
├── web/                         # React/Vite dashboard
├── desktop/                     # Tauri shell
└── .github/workflows/ci.yml     # CPU/CUDA/HIP/Windows/Web/Python checks
```

GitHub recursive tree 对固定 commit 返回 **240 个 blob**。一个值得记录的文档漂移是：README 第 92、314 行称核心文件 `c/glm.c`，固定 commit 实际主文件是 `c/colibri.c`；这不是推理缺陷，但说明文件路径必须从真实 tree 再核验，不能只抄 README。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `c/colibri.c` | 主推理与调度 | expert 路由、镜像 read、cache、MoE union、attention、speculation |
| `c/tier.h` | 热驻留策略 | frequency 主导、recency tie-break、hysteresis、decay |
| `c/backend_cuda.cu` | CUDA/HIP backend | 同一 source 适配两 vendor；硬件执行仍需实机 |
| `c/backend_loader.c` | 动态 backend | Windows DLL capability 探测，缺失时回 CPU |
| `c/Makefile` | 平台构建 | compiler target triple、OpenMP、CUDA/HIP/portable arch |
| `.github/workflows/ci.yml` | 质量覆盖 | CPU tests、CUDA/HIP syntax、Windows MSVC CUDA build、web/Python |
| `docs/tuning.md` / `docs/benchmarks.md` | 性能证据 | 参数、测量边界；本次只作为上游文档，不外推到本机 |
| `c/resource_plan.py` | 资源预算 | issue #653 指向 unified-memory 预算边界，尚待上游修复核验 |

#### 源码精读（固定 commit）

**代码块 1：双盘副本路由必须确定性**  
来源：[`colibri.c#L1340-L1349`](https://github.com/JustVugg/colibri/blob/1b8b62ee75e33685508c26d10424460f857cd85d/c/colibri.c#L1340-L1349)

```c
static inline int expert_route(int layer,int eid){
    if(!g_mirror) return 0;
    uint32_t h=(uint32_t)layer*2654435761u ^ (uint32_t)eid*0x9E3779B9u;
    h^=h>>16; h*=0x45d9f3bu; h^=h>>16;
    return (int)(h&255) < g_mir_share;
}
```

逻辑：只用稳定 `(layer,eid)` 与份额阈值选盘。这样 lookahead/prefetch 与最终 demand read 会命中同一 fd/page cache；不能用每次随机负载均衡，否则会把同一 expert 缓存两次并破坏可解释性。

**代码块 2：镜像错误只降速，不杀主路径**  
来源：[`colibri.c#L1358-L1377`](https://github.com/JustVugg/colibri/blob/1b8b62ee75e33685508c26d10424460f857cd85d/c/colibri.c#L1358-L1377)

```c
static ssize_t mir_pread(shards *S,int fd,int rep,void *buf,
                         int64_t n,int64_t off,const char *tag){
    int rfd = st_fd_rep(S,fd,rep);
    int used = rep && rfd>=0;
    if(rfd<0) rfd=fd;
    int rc=pread_full(rfd,buf,n,off,tag);
    if(rc && used){
        static _Atomic int warned;
        if(!atomic_exchange(&warned,1))
            fprintf(stderr,"[MIRROR] read error ... falling back ...\n");
        used=0; rc=pread_full(fd,buf,n,off,tag);
    }
    if(!rc) atomic_fetch_add_explicit(&g_mir_bytes[used],n,memory_order_relaxed);
    return rc;
}
```

逻辑：mirror shard 不存在或读取失败时回 primary；warning 只发一次；成功后按实际盘记账。它区分“冗余加速层失败”和“唯一真相源失败”。边界是 primary 同样损坏时仍必须诚实失败，不能伪造输出。

**代码块 3：LFRU 让频率主导、最近性只打破接近值**  
来源：[`tier.h#L27-L54`](https://github.com/JustVugg/colibri/blob/1b8b62ee75e33685508c26d10424460f857cd85d/c/tier.h#L27-L54)

```c
static uint64_t tier_lfru_score(uint32_t heat, uint32_t last, uint32_t clock){
    uint32_t age=clock-last, recent=age<255?255-age:0;
    return ((uint64_t)heat<<8)|recent;
}

/* ... choose cold resident and hot non-resident ... */
if(hs<=cs+(cs>>2)+(4u<<8)) return 0;
*slot=cold; *eid=hot; *gain=(long)((hs-cs)>>8);
```

逻辑：一次 frequency 等于 256 分，recency 最多 255，因此“刚访问一次”不能挤掉真正热点；替换还需超过旧 slot 的 25% + 4 frequency hysteresis。这个模式适合防止 cache/skill prefill 高频抖动，但需要溢出、decay 与 workload shift 测试。

**代码块 4：MoE 先全批路由，再构造 expert union**  
来源：[`colibri.c#L2704-L2718`](https://github.com/JustVugg/colibri/blob/1b8b62ee75e33685508c26d10424460f857cd85d/c/colibri.c#L2704-L2718) 与 [`#L2939-L2945`](https://github.com/JustVugg/colibri/blob/1b8b62ee75e33685508c26d10424460f857cd85d/c/colibri.c#L2939-L2945)

```c
/* BATCH-UNION: each unique expert is loaded once for all positions. */
static void moe(Model *m, Layer *l, int layer,
                float *x, int S, float *out, int with_shared){
    /* FASE A computes idxs/weights for all S positions ... */
    int *uniq=malloc((size_t)E*sizeof(int)); int nu=0;
    unsigned char seen[E]; memset(seen,0,(size_t)E);
    for(int s=0;s<S;s++) for(int kk=0;kk<keff[s];kk++){
        int e=idxs[(int64_t)s*K+kk];
        if(!seen[e]){ seen[e]=1; uniq[nu++]=e; }
    }
}
```

逻辑：把 S 个 token 的 top-K 先合成 unique expert 集，随后一次加载可服务多个 position。这是“同 scope 请求先 union 再取大工件”的典型 I/O 优化。边界是 union 可能放大瞬时工作集，所以源码后续还有 miss-aware `EXPERT_BUDGET`；不能无界 batch。

#### 依赖分析与供应链风险

核心 C CPU 路径使用 libc、pthread、OpenMP 与 `libm`，不是整个仓库“零依赖”：

- `pyproject.toml`：launcher 本体无必需 Python dependency，但 `convert` 可选 `numpy/huggingface_hub`，`oracle` 有 `torch/transformers/safetensors`，`bench` 有 `tokenizers/datasets`。
- `web/package.json`：React 18、Vite/Vitest、Tailwind 等；有 `package-lock.json`。
- Desktop 有 Tauri/Cargo.lock；GPU 可选 CUDA/HIP/Metal toolchain。
- CI actions 多数只按 major tag（如 `actions/checkout@v4`），`Jimver/cuda-toolkit@v0.2.19` 相对更窄；仍需 action SHA pin/SBOM 审查。
- 模型文件约 372GB，来自外部 Hugging Face；README 声称 GLM-5.2 weights 为 MIT，但本次未独立审计模型卡、转换产物 provenance、pickle/unsafe loader 风险，不能把代码 Apache-2.0 外推到权重与数据。
- `make test-c` 真实通过，但 `test_int3.c` 有 `t.gs` 未初始化 warning；这是测试编译静态诊断，需上游确认是否仅测试 fixture 初始化缺失。

#### 真实测试结果

执行：`make test-c`（目录 `c/`），exit code **0**。关键终态包括：

- `tier tests: ok`
- `decode batch helper tests: ok`
- `test_topp: 123 cases run, 0 failure(s)`
- `test_dsa_select: 129 cases run, 0 failure(s)`
- `test_uring: ok`

这验证了当前主机上的 CPU fixture，不验证 744B 模型正确性、CUDA/HIP/Metal、Windows、双 NVMe、性能数字或 issue #653 的 GB10 场景。

#### 可复用经验

- 当大工件只有稀疏子集被请求时，应优先把工件当可分层调度数据，并让 placement 只改变性能、不静默改变语义；边界是预算必须按共享物理资源而非逻辑 tier 分别计算。
- 当 prefetch 与 demand 会访问同一只读副本时，应优先用稳定 resource identity 做确定性分流，并记录实际 fallback；边界是副本内容必须在使用前验证一致性。
- 当批内请求共享昂贵依赖时，应优先先 union 去重再加载，并设置 distinct-item budget；边界是 append-only evidence、用户隔离数据和不同授权 scope 不能跨界合并。
- 当 workload 热点变化但频繁换入代价很高时，应优先用频率主导、最近性 tie-break 与 hysteresis；边界是需要 decay、冷启动、概念漂移与上限测试。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/tiered-artifact-cache/` 做**纯合成** fixture（建议，今日未创建）：生成 256 个 artifact IDs 与 1000 次访问，比较 LRU 与 LFRU+hysteresis 的 swap 次数和 hit rate；再模拟 mirror 20% 失败，验证 fallback 不改变返回 hash。禁止下载 372GB 模型、禁止访问 secret、禁止改系统 cache/config。

#### 风险边界

- **License**：代码 API 为 Apache-2.0；模型权重/数据/依赖另算。只抽象机制，不复制大段 C 源码到 shared。
- **维护活跃度**：最新 release 6 天内、commit/issue 1 天内，活跃；但仓库创建不足一个月，接口与文件名已出现 README/真实 tree 漂移。
- **安全**：外部 372GB 模型、转换链、Python gateway、GPU backend 都扩大攻击面；不要自动下载/加载未知容器。issue #653 表明预算错误会 OOM-kill。
- **局限/不适用**：磁盘 streaming 极慢时只有“能跑”不等于可用；README 自述 25GB 冷 decode 仅 0.05–0.1 tok/s。本任务未复现性能/质量。
- **资源预算**：unified memory 不能把 VRAM 与 RAM 当两个独立池；issue #653 建议重新读取可用内存或扣除实际 tier bytes，修复状态待核验。
- **不可自动执行**：不下载模型、不启服务、不开放 API port、不安装 CUDA/HIP、不改 Hermes 模型/provider/cache/cron。

#### Skill 升格判断

**需二次验证。** “tiered artifact cache”可作为 runtime POC，但当前更像跨项目事实/工程模式，不足以直接成为 shared skill；必须先证明对 Hermes 大 artifact、索引或 skill cache 有真实收益，并验证 scope isolation、hash equality、预算、fallback receipt。若仅用于本地推理，则保留 Hermes 本地长期能力，不升 shared；只有形成跨 agent 的稳定 cache contract 才考虑 `capabilities/skills/`。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/tiered-artifact-cache/`，只用 synthetic IDs/hashes。
2. **可复用接口候选**：`get(scope, artifact_id, expected_hash) -> {value,tier,source,fallbacks,status}`；cache key 必含 scope + immutable identity + content hash。
3. **shared 适配边界**：可用于 runtime 索引/大附件缓存，不能把 runtime cache 写到 curated；`curated/memory` 只接收审查后的模式摘要。
4. **治理**：先与现有 cache/evidence key、scoped authority、path portability 经验去重；通过后才更新 project/fact 或 shared skill manifest。

## 横向对照：两类“确定性外壳”

| 维度 | Grok Build | Colibrì | 对 Hermes/shared hub 的启示 |
|---|---|---|---|
| 模糊选择 | LLM 选工具 | router 选 experts | 选择可模糊，执行契约必须确定 |
| 身份 | ToolId + typed Args | `(layer,eid)` | cache/effect 必须绑定 immutable scoped ID |
| 中间态 | Progress | prefetch/cache tier | 中间态不能冒充完成 |
| 终态 | exactly one Terminal | demand load 成功或诚实失败 | completed 需终态 + artifact/receipt |
| 权限/预算 | deny/ask/allow + sandbox | VRAM/RAM/NVMe budget | 逻辑层必须映射真实物理/授权边界 |
| 降级 | stream_no_terminal 报错 | mirror -> primary | 降级可减速，不能静默改变语义 |
| 证据 | typed output / status | bytes、hit、tier、warning | receipt 要披露实际路径与 fallback |

## 经验沉淀

1. 当不确定组件负责选择而宿主负责副作用时，应优先把身份、schema、预算、权限和终态放进确定性外壳，因为“模型/路由器选对了”不等于“执行安全完成”；边界是外壳本身必须有 adversarial fixture。
2. 当任务能产生进度、重试、取消或后台工作时，应优先使用 `Progress* + exactly-one Terminal + receipt`，因为 EOF、queue empty 或最后一行 stdout 都不能证明完成；边界是 timeout/cancel 也必须成为显式终态。
3. 当同一逻辑资源可从多个副本或 tier 获取时，应优先用 scoped immutable ID 做确定性路由并核验 content hash，因为随机分流会制造重复缓存和证据漂移；边界是跨 tenant/user 的数据不得为提高 hit rate 而合并。
4. 当 shell 或自动化规则可以嵌套 wrapper、链式命令与解释器时，应优先逐段验证 deny/ask 并在解析不确定时 fail closed，因为宽 allow prefix 很容易包住额外副作用；边界是 kernel sandbox 的平台能力也需真实探测。
5. 当缓存换入代价高且访问分布有热点时，应优先采用频率主导、最近性辅助和 hysteresis 的替换策略，因为纯 recency 容易被扫描流量污染；边界是必须加入 decay、容量、概念漂移和 overflow 测试。
6. 当逻辑 tier 共享同一物理资源时，应优先按物理池统一记账并在分配后重采样，因为分别计算 VRAM/RAM 预算会重复承诺同一内存；边界是不同硬件（discrete/unified）需要显式 capability 分支。
7. 当上游 README、tree、release 或代码彼此不一致时，应优先固定 commit 并直接核验路径、函数和工具输出，因为文档路径和实时 stars 都会漂移；边界是未编译/未复现的部分必须标注待核验。

## 风险边界（全局）

- 本次只读取公开 GitHub 数据和本地浅克隆；未调用 OpenClaw，未发送消息，未更改 Hermes 配置/provider/model/tools/auth/env/cron。
- 不把 GitHub stars 当质量或安全证明；项目都很新，star 增长真实性与长期维护性未做社会层审计。
- GitHub API license 只覆盖仓库识别结果，不覆盖依赖、vendored source、模型权重、数据与商标。
- 不执行仓库安装脚本，不运行未知模型/服务；仅 Colibrì 的本地 C fixture 被实际编译执行。
- 不直接写 `curated/memory` active fact，不创建/升格 shared skill；下面只有候选。
- Grok Build 编译因本机缺 Cargo 阻塞；Colibrì 全模型、GPU、双盘、性能、质量和 GB10 issue 均待硬件复现。

## Skill 升格总判断

- **Grok Build 模式：需二次验证。** 合并到既有 verification/effect-scope 候选，避免重复造 `tool protocol` skill。
- **Colibrì 模式：需二次验证。** 先做 synthetic tier/cache POC；若只服务本地推理则不升 shared。
- **今日动作：不直接升格。** 原因是两个模式都尚未通过 Hermes fixture、治理去重与跨 agent 适用性验证；shared skill 需要 class-level 稳定契约，不应收纳今日 stdout、stars 或一次性源码快照。

## 明日继续

1. 最小动作：补装隔离 Rust toolchain 或使用临时容器（需安全审查后）执行 `cargo test -p xai-tool-runtime`，记录真实 commit、依赖下载与测试终态；若无法安全安装，继续标记 blocked，不伪造。
2. 建立 `tool-terminal-contract` 纯 fixture，验证无 Terminal、双 Terminal、cancel、timeout 与 artifact-missing 五类失败；与当前 `status.json overall_status=completed` 规则对照。
3. 建立 256 synthetic artifact 的 LRU vs LFRU+hysteresis 实验，输出 hit/swap/fallback/hash-equality；不下载模型。
4. 跟进 Colibrì issue #653 的修复 commit/release，核验 unified-memory capability 与预算重采样是否进入源码和测试。

## 候选反哺

### Candidate Facts

- [ ] topic: terminal-stream-completion-contract | evidence: `xai-tool-runtime/src/tool.rs` 与 `dispatch.rs` 固定 commit；无 Terminal 明确 `stream_no_terminal` | 建议: update（并入既有 verification/subagent 四状态事实，不新建重复条目） | 安全级别: low
- [ ] topic: deterministic-replica-routing-with-semantic-preserving-fallback | evidence: Colibrì `expert_route` + `mir_pread` 固定 commit，`make test-c` 通过 mirror fixtures | 建议: create candidate，先做 hash fixture | 安全级别: medium
- [ ] topic: unified-resource-budget-must-follow-physical-pool | evidence: Colibrì issue #653 的 GB10 OOM 报告；上游修复尚未核验 | 建议: dispute/pending，不进入 active fact | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: tool-terminal-contract-fixtures | 可复用场景: cron、subagent、长工具、audit completed 判定 | 是否建议 shared: yes（验证后） | 原因: Hermes/future agent 都需要，但先与 verification-first/self-reflection 去重
- [ ] 名称: tiered-artifact-cache-poc | 可复用场景: 大附件、索引、只读 artifact cache | 是否建议 shared: no（当前） | 原因: 尚无 Hermes 真实收益和 scope isolation 证据，先留 runtime POC

### Candidate Open Questions

- [ ] 问题: `Progress* + Terminal` 如何统一表达 cancel、timeout、partial artifact 与后台 drain receipt？ | reason: adaptation | priority: high
- [ ] 问题: Grok Build 的 public monorepo sync 是否有可复现 release/tag/SBOM，以及当前 commit 能否在隔离环境通过目标 crate tests？ | reason: gap | priority: high
- [ ] 问题: Colibrì issue #653 将如何区分 discrete 与 unified memory，并如何为分配后预算重采样加测试？ | reason: stale | priority: high
- [ ] 问题: LFRU+hysteresis 对 shared hub 的哪类真实 artifact 优于现有简单 cache，且不会跨 scope 泄漏？ | reason: adaptation | priority: medium

### 不应自动落地

- 不安装或运行 Grok Build，不执行 `curl | bash`，不修改 Hermes/OpenClaw 配置、模型、provider、tools、auth、env、cron 或 secret。
- 不下载/转换/运行 GLM-5.2 372GB 权重，不启动 Colibrì API，不开放端口，不安装 GPU backend。
- 不复制上游 Rust/C 源码进入 shared skill；只抽象经过验证的契约。
- 不把候选直接写成 `curated/memory` active fact；必须经过 evidence、去重、脱敏、评分和人工/总控审查。
