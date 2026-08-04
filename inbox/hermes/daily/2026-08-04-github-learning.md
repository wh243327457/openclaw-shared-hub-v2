# 2026-08-04 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> 研究时间：2026-08-04T07:31–07:40+08:00；GitHub API 最终复核约 2026-08-03T23:39:58–23:40:03Z。  
> 发现来源：真实抓取 `https://github.com/trending?since=daily`，并以 GitHub Search API 查询近期高星项目；速览元数据再逐仓用 `gh api repos/{owner}/{repo}` 复核。  
> 固定源码快照：`xai-org/grok-build@e5478eff1e4050558e12e1328b85e6616632efb6`（`SOURCE_REV=27d2088ae3b3f25e9ddab462caa18a07005ada9a`）、`openai/codex-security@7b7e031df81d712db4e8a309728f975229628114`。  
> 数据边界：Stars、forks、updated/pushed 会继续变化；GitHub Repository API 的 license 只代表仓库级识别结果，不能替代依赖、模型、数据、镜像和发行制品审查。

## 今日结论

今天的主线是：**高权限 Agent 不能只靠“提示词提醒安全”，而要让宿主同时拥有输入身份、权限求值、可恢复执行记录和可验证完成证据。** Grok Build 把 repository-controlled config 纳入 folder-trust gate，把 shell 链逐段授权，把 deterministic request hash 与 dense journal 用于可恢复 workflow；Codex Security 把 target canonicalization、restricted comparison、coverage、sealed canonical artifacts、私有输出目录与凭据锁收进 SDK 外壳。对 Hermes/shared hub 最值得吸收的不是安装两个产品，而是把现有每日学习 POC 进一步收敛为 **authority-before-execution + evidence-before-completion**：研究输入绑定固定 revision，执行前校验 scope/effect，完成时校验 canonical artifact、coverage、hash 和 audit receipt。

## 证据与执行摘要

- **Trending 真实抓取**：HTML 保存为 `runtime/hermes/github-hot-project-learning/trending-2026-08-04.html`，651,956 bytes；解析到 `lyogavin/airllm`、`zhaoxuya520/reverse-skill`、`firecrawl/pdf-inspector`、`esengine/DeepSeek-Reasonix`、`TencentCloud/TencentDB-Agent-Memory`、`antirez/ds4`、`livekit/agents`、`usekaneo/kaneo`、`jamiepine/voicebox` 等 16 个项目。
- **近期增长补充**：GitHub Search API 查询 `created:>2026-07-01 stars:>100`，结果包含 `xai-org/grok-build`、`openai/codex-security` 等。今日筛出 5 个值得进一步读的对象：Grok Build、Codex Security、pdf-inspector、DeepSeek-Reasonix、livekit/agents；受时间与深度要求限制，只对前两项完成源码级深读。
- **API 原始证据**：两个深读仓库的 Repository、License、Releases、Issues/PR 和 Commits JSON 保存于 `runtime/hermes/github-hot-project-learning/api/2026-08-04/`。Dependabot alerts endpoint 对当前 token 返回 HTTP 404，状态标记为**待核验**，不能写成“没有漏洞”。
- **源码证据**：两个仓库均真实 `git clone --depth 1`；固定快照 tracked paths 分别为 **3,024** 和 **192**，研究后两个工作树均无 tracked 修改。
- **来源交叉**：Grok Build 核验 README、permissions/folder trust 文档、SECURITY、commit history、Cargo manifests、journal/workflow/permission/folder-trust 源码；仓库关闭公开 issues，Releases 与 tags API 均为空。Codex Security 核验 README、SECURITY、completed-scan contract、GitHub Release、公开 issues/PR、package/lockfile、target/comparison/contract/runtime 源码与 tests。
- **真实执行——Grok Build**：本机没有 Cargo、Rustc 和 DotSlash，未安装工具链；因此 Rust 编译、单测、TUI、ACP、sandbox、workflow resume 和 permission enforcement 均为**待核验**。只报告源码静态结论，不借上游 tests 冒充本机通过。
- **真实执行——Codex Security**：在 `sdk/typescript/` 用锁定的 `pnpm@11.9.0` 安装成功（lockfile policy 检查通过，安装 95 个 package）；`pnpm run build`、`pnpm run lint`、`pnpm audit --prod --audit-level high` 均成功，后者返回 `No known vulnerabilities found`。首次调用 repo test command 因 `bun` 不存在失败；随后临时执行 `bun@1.3.13` 的 5 个定向 test files，真实结果 **81 pass / 0 fail**，耗时 63.30s。
- **安全边界**：没有登录 Codex Security、没有提供 API key、没有扫描真实仓库、没有调用模型、没有安装 Grok Build、没有修改 Hermes/OpenClaw 配置或 cron，也没有把候选直接写入 curated/skills。

## 项目速览

下表数字均来自 2026-08-03T23:39:58–23:40:03Z 左右逐仓 Repository API；`open_issues_count` 未列出，因为它包含 PR 且不能解释为缺陷数。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [jamiepine/voicebox](https://github.com/jamiepine/voicebox) | 48,645 | 5,990 | TypeScript | MIT | 2026-08-03T23:37:45 / 2026-07-28T02:20:57 | 热门语音工作台；模型、音频隐私和 GPU 边界需专项研究 |
| [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | 29,885 | 1,918 | Go | MIT | 2026-08-03T23:35:08 / 2026-08-03T18:29:05 | 值得继续：围绕 prefix-cache stability 的长驻 coding agent |
| [lyogavin/airllm](https://github.com/lyogavin/airllm) | 27,025 | 2,965 | Jupyter Notebook | Apache-2.0 | 2026-08-03T23:39:54 / 2026-07-29T01:08:32 | 分层本地推理候选；性能、模型 license 和 GPU 需复现 |
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | **24,023** | 4,547 | Rust | **Apache-2.0** | 2026-08-03T23:35:46 / 2026-08-03T17:33:39 | **深读：folder trust、逐段权限、journal resume、输出可恢复性** |
| [antirez/ds4](https://github.com/antirez/ds4) | 20,342 | 1,798 | C | MIT | 2026-08-03T23:39:31 / 2026-08-03T17:26:53 | 已有长期事实；今日只作持续活跃参照，不重复深读 |
| [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 15,674 | 2,213 | PowerShell | MIT | 2026-08-03T23:39:50 / 2026-08-03T13:57:57 | 安全工具路由面高权，不在无人值守 cron 中运行 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | 12,039 | 1,139 | TypeScript | NOASSERTION | 2026-08-03T23:35:22 / 2026-08-03T12:49:18 | 与 shared hub 相关，但 API 未识别 license，禁止复制源码 |
| [livekit/agents](https://github.com/livekit/agents) | 11,961 | 3,456 | Python | Apache-2.0 | 2026-08-03T23:39:57 / 2026-08-03T23:00:02 | 值得继续：实时 voice agent lifecycle 与多模态 transport |
| [openai/codex-security](https://github.com/openai/codex-security) | **8,370** | 571 | TypeScript | **Apache-2.0** | 2026-08-03T23:40:03 / 2026-08-03T23:39:59 | **深读：target identity、restricted comparison、sealed contract、private state** |
| [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) | 8,106 | 538 | Rust | MIT | 2026-08-03T23:39:54 / 2026-08-03T23:35:52 | 值得继续：PDF 分类后确定性路由，需恶意 PDF 资源预算测试 |

说明：Stars 不是成熟度、采用率、安全性或真实性证明；`updated_at` 可能由元数据活动推动，`pushed_at` 也可能来自非默认分支。深读结论始终绑定上方固定 commit。

## 深读项目

### 1. xai-org/grok-build

**基本信息（GitHub API）**

- URL：https://github.com/xai-org/grok-build
- Stars：**24,023**；Forks：**4,547**；Language：Rust；License：**Apache-2.0**。
- 创建：2026-07-14T20:04:23Z；updated：2026-08-03T23:35:46Z；pushed：2026-08-03T17:33:39Z。
- 固定 default-branch commit：[e5478eff1e40](https://github.com/xai-org/grok-build/commit/e5478eff1e4050558e12e1328b85e6616632efb6)，commit time 2026-08-03T17:33:32Z，message `Synced from monorepo`；根 `SOURCE_REV` 指向内部 revision `27d2088ae3b3f25e9ddab462caa18a07005ada9a`。
- Repository API：`has_issues=false`、`open_issues_count=0`；Releases 与 tags API 返回空数组，pulls endpoint 返回 404。这里的“0”只表示公共镜像关闭 issues，不证明内部 monorepo 无缺陷。
- README 与 License API 识别 first-party code 为 Apache-2.0；README 明确 third-party/vendored code 保留原许可证，并指向 `THIRD-PARTY-NOTICES`、crate-local notices 与 `third_party/NOTICE`。

#### 一句话判断

Grok Build 值得学的不是全屏 TUI，而是它把 **repo-controlled configuration 的信任、逐段 tool authorization、deterministic workflow replay、后台输出的可恢复 delivery**分别做成宿主层契约；这比单纯在 system prompt 里写“不要执行危险命令”更接近可验证的 Agent runtime。

#### 解决的问题：替代了什么旧做法

1. 替代“只看到 MCP/hook 才提示 trust”的窄 gate：项目内 permission、plugin paths、`.envrc`、Claude settings、agents、roles/personas/workflows 也能改变执行或提示语义。
2. 替代把整条 shell 文本只看第一个 prefix 的做法：allow 必须覆盖每个可解析 segment；wrapper、inline `-c` 和不确定解析有独立 fail-closed/Ask 路径。
3. 替代 resume 时按“第 N 个调用”盲目复用结果的做法：journal 还比较 `kind + canonical request hash`，脚本或参数变化触发 divergence。
4. 替代把 torn journal tail 或超大 journal 当正常状态的做法：限制 64 MiB、要求 dense sequence、拒绝 symlink，并只截断无法解析的最后半行。
5. 替代把长后台输出直接塞进 prompt 或静默截断的做法：有 polling tool 时给可拉取指针；bash inline preview 截断时保留 full-log disk pointer。
6. 替代“always approve 就什么都绕过”的模糊说法：文档列出 hook、deny、ask、remembered grant、built-in readonly 与 prompt policy 的顺序，并明确 OS sandbox 是另一层。

边界：permission parser、folder trust 与 sandbox 都是复杂安全代码；静态阅读不能证明所有 shell grammar、symlink、平台或 config source 都被覆盖。README 也明确该仓库由内部 monorepo 同步且不接受外部贡献，公共镜像不是完整治理面。

#### 架构 / 实现与数据流

```text
TUI / headless CLI / ACP client
              │
              ▼
      xai-grok-pager-bin          # composition root
              │
              ▼
       xai-grok-shell             # session / agent / background lifecycle
        ├───────────────┬──────────────────────┐
        ▼               ▼                      ▼
 xai-grok-tools   xai-grok-workspace      xai-workflow
 typed tools      FS/Git/permission       Rhai deterministic script
        │          /folder trust          + budget/cancel/pause
        │               │                      │
        ▼               ▼                      ▼
 tool runtime      permission policy       host calls
 progress/result   + optional sandbox      + JSONL journal
        │                                      │
        └──────── completion reminders ────────┘
                 preview / polling / disk pointer
```

一次 repo session 启动时，folder-trust scanner 先查找能执行代码或改变授权的 repo-local surfaces；工具调用进入 permission policy，deny/ask/allow 与 mode 按确定顺序求值，shell 链还需要 segment 级检查。Workflow DSL 不直接持有副作用实现，而通过 host channel 调 Agent、scratch、Git 等；每个 result-bearing host call 用 sequence 与 request hash 写 journal，恢复时重放已匹配结果。后台任务完成后，renderer 根据可用 tool 决定“给 polling pointer”还是 inline；有 disk-backed bash log 时，preview 可截断但必须提示完整输出位置。

#### Repo tree 摘要

```text
grok-build/                                      # fixed commit tracked paths: 3,024
├── README.md / SECURITY.md / LICENSE            # 产品入口、HackerOne、first-party Apache-2.0
├── SOURCE_REV                                   # 公共镜像对应的内部 monorepo revision
├── Cargo.toml / Cargo.lock                      # generated workspace、固定依赖图
├── rust-toolchain.toml / .cargo/                # Rust 1.93.0、构建配置
├── bin/                                         # DotSlash/protoc 等 hermetic tool 描述
├── crates/
│   ├── codegen/
│   │   ├── xai-grok-pager[-bin]/                # TUI、用户文档、composition root
│   │   ├── xai-grok-shell/                      # session、agent、headless/leader runtime
│   │   ├── xai-grok-tools/                      # bash/edit/search/background tools
│   │   ├── xai-grok-workspace/                  # FS、VCS、permission、folder trust
│   │   ├── xai-grok-sandbox/                    # OS-level enforcement
│   │   └── xai-workflow/                        # deterministic workflow、journal、validation
│   └── common/
│       ├── xai-tool-runtime/                    # typed tool dispatch/stream/terminal
│       ├── xai-tool-protocol/                   # wire protocol 与 identity
│       └── xai-grok-compaction/                 # context compaction stages
├── prod/mc/                                     # shared production-facing types
└── third_party/                                 # Mermaid graph stack 等 vendored source
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/codegen/xai-grok-workspace/src/folder_trust.rs` | repository trust gate | 用同一 scanner 发现 MCP、permission、plugin paths、envrc、Claude config、hooks、agents/workflows，headless 遇配置默认 untrusted |
| `crates/codegen/xai-grok-workspace/src/permission/policy.rs` | tool authorization | deny > ask > allow；shell allow 每段覆盖；不确定脚本 Ask；path lexical normalization + cwd forms |
| `crates/codegen/xai-workflow/src/engine.rs` | deterministic orchestration | Rhai resource limits、禁用时间/sleep/eval、host-call replay/record、budget/cancel/pause terminal |
| `crates/codegen/xai-workflow/src/journal.rs` | resume evidence | dense seq、kind/request hash、64 MiB cap、torn-tail handling、symlink rejection、sync append |
| `crates/codegen/xai-grok-tools/src/reminders/task_completion.rs` | output delivery | polling tool、inline preview、full-log pointer、session ownership、重复 completion 抑制 |
| `crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md` | public authorization contract | mode、规则来源、执行顺序、known caveats、sandbox 组合建议 |
| `Cargo.toml` / `Cargo.lock` | dependency truth | 81 workspace members、244 workspace dependencies、1,303 locked packages、git pins 与 vendored crates |
| `THIRD-PARTY-NOTICES` | license provenance | first-party Apache-2.0 之外的 registry/git/in-tree port 义务入口 |

#### 源码精读（固定 commit）

**代码块 1：repo-local permission/plugin/env/agent 也属于 trust surface**  
来源：[`folder_trust.rs#L305-L438`](https://github.com/xai-org/grok-build/blob/e5478eff1e4050558e12e1328b85e6616632efb6/crates/codegen/xai-grok-workspace/src/folder_trust.rs#L305-L438)

```rust
fn collect_repo_config_kinds(cwd: &Path, first_only: bool) -> Vec<&'static str> {
    let chain = xai_grok_agent::repo::RepoDirChain::resolve(cwd);
    let mut kinds: Vec<&'static str> = Vec::new();

    for path in crate::project_config::find_project_configs_in(&chain.dirs) {
        let Ok(root) = xai_grok_config::load_config_file(&path) else {
            continue;
        };
        let has_mcp_servers = root.get("mcp_servers")
            .and_then(|v| v.as_table()).is_some_and(|t| !t.is_empty());
        let has_plugin_paths = root.get("plugins")
            .and_then(|v| v.get("paths"))
            .and_then(|v| v.as_array()).is_some_and(|a| !a.is_empty());
        let has_permission = root.get("permission")
            .is_some_and(config_toml_permission_contributes);
        // each hit is recorded as mcp / plugins / permission
    }
    // Same scanner also checks .envrc, Claude settings, hooks, agents,
    // roles, personas, workflows and project-scoped MCP.
    kinds
}
```

逻辑：trust gate 不是只找可执行二进制；任何能加载 server/plugin/hook、注入环境、shadow subagent 或自动 allow/deny tool 的 repository-owned config 都是 authority surface。scanner 复用和 loader 相同的 cwd→git-root 路径，减少“loader 看得到、gate 看不到”的漂移。边界是 `decide()` 对无法记录 trust key 的 home/fs-root 情形有兼容选择，且 feature flag/build stamp 也影响 gate；因此不能只复制 marker 列表就宣称获得同等保护。

**代码块 2：Bash allow 必须覆盖每个可解析 segment**  
来源：[`permission/policy.rs#L223-L343`](https://github.com/xai-org/grok-build/blob/e5478eff1e4050558e12e1328b85e6616632efb6/crates/codegen/xai-grok-workspace/src/permission/policy.rs#L223-L343)

```rust
pub fn evaluate_with_cwd(
    &self,
    access: &AccessKind,
    cwd: Option<&Path>,
) -> Option<Decision> {
    let mut matched_ask = false;
    let mut matched_allow = false;
    for (rule, matcher) in self.config.rules.iter().zip(&self.matchers) {
        if !tool_filter_matches(access, &rule.tool) { continue; }
        if !pattern_matches(access, &CompiledRule { rule, matcher: matcher.as_ref() }, cwd) {
            continue;
        }
        match rule.action {
            RuleAction::Deny => return Some(Decision::Reject(/* provenance */)),
            RuleAction::Ask => matched_ask = true,
            RuleAction::Allow => matched_allow = true,
        }
    }
    if matched_ask { return Some(Decision::Ask); }
    if let AccessKind::Bash(cmd) = access {
        if self.has_bash_allow_rules
            && self.bash_chain_fully_allowed(cmd, MAX_INLINE_SHELL_DEPTH)
        {
            return Some(Decision::Allow);
        }
        return None;
    }
    matched_allow.then_some(Decision::Allow)
}
```

逻辑：deny 立即胜出，ask 高于 allow；Bash 即使整体文本匹配某个 allow，也必须进入 `bash_chain_fully_allowed`，逐段剥离可识别 wrapper，并递归检查 literal `shell -c`。解析 exhausted/ambiguous、`env -S` split string 或未知 inline 形状不进入 allow。边界是 shell 是开放语法，文档仍明确 hooks fail open、read-only command list 只是 convenience、direct tool path 与 shell-level symlink checks 不完全相同；必须再叠 OS sandbox。

**代码块 3：journal replay 同时绑定 sequence、kind 和 request hash**  
来源：[`xai-workflow/src/journal.rs#L170-L224`](https://github.com/xai-org/grok-build/blob/e5478eff1e4050558e12e1328b85e6616632efb6/crates/codegen/xai-workflow/src/journal.rs#L170-L224)

```rust
pub fn replay(
    &self,
    seq: u64,
    kind: &str,
    req_hash: &str,
) -> Result<Option<serde_json::Value>, JournalError> {
    let Some(entry) = usize::try_from(seq).ok()
        .and_then(|seq| self.entries.get(seq)) else {
        return Ok(None);
    };
    if entry.seq != seq || entry.kind != kind || entry.req_hash != req_hash {
        return Err(JournalError::Divergence { seq, kind: kind.to_string() });
    }
    Ok(Some(entry.result.clone()))
}

pub fn record(&mut self, seq: u64, kind: &str, req_hash: String,
              result: serde_json::Value) -> Result<(), JournalError> {
    validate_sequence(&self.entries, &entry)?;
    if self.bytes.saturating_add(line.len() as u64) > MAX_JOURNAL_BYTES {
        return Err(JournalError::Full { seq, limit: MAX_JOURNAL_BYTES });
    }
    append_line(path, &line)?;
    self.entries.push(entry);
    Ok(())
}
```

逻辑：resume 只有在调用顺序、调用类别与 canonicalized payload hash 都一致时才复用旧 result；脚本改动或输入改变会得到 `Divergence`，不是把旧响应注入新调用。record 在写磁盘成功后才推进内存，并把超 cap 视为 fatal，避免产出一个之后无法 restore 的 journal。边界是 request hash 截取 SHA-256 前 16 bytes，journal 没有外部签名，也不自动绑定 script/repo identity；有写权限者仍可能改写完整 journal，跨进程 writer 的互斥也需宿主保证。

**代码块 4：workflow engine 主动移除破坏 deterministic resume 的能力**  
来源：[`xai-workflow/src/engine.rs#L103-L187`](https://github.com/xai-org/grok-build/blob/e5478eff1e4050558e12e1328b85e6616632efb6/crates/codegen/xai-workflow/src/engine.rs#L103-L187)

```rust
pub fn run_workflow(params: WorkflowRunParams) -> WorkflowOutcome {
    let mut engine = rhai::Engine::new();
    engine.set_max_operations(max_ops);
    engine.set_max_call_levels(64);
    engine.set_max_expr_depths(128, 64);
    engine.set_max_string_size(16 * 1024 * 1024);
    engine.set_max_array_size(65_536);
    engine.set_module_resolver(rhai::module_resolvers::DummyModuleResolver::new());
    engine.disable_symbol("eval");
    engine.register_fn("timestamp", || -> ScriptResult<()> {
        Err(runtime_error("timestamp() is unavailable: workflow scripts must be deterministic"))
    });
    // sleep() and exit() are similarly rejected; completion uses typed control tokens.
    register_host_fns(&mut engine, &ctx);
    // compile + run -> Completed / Paused / BudgetExceeded / Cancelled / Failed
}
```

逻辑：脚本只能消费显式 `args`，不能读 wall-clock timestamp、任意 eval 或用 sleep 模拟 host lifecycle；CPU/recursion/string/array/map/host-call 有上限，副作用通过 host functions。边界是 deterministic DSL 只能保证已建模操作；host implementation、Agent output、filesystem、Git、网络和 journal storage 仍可能非确定，必须靠 receipt/identity/timeout 补强。

#### 依赖分析与供应链风险

- root `Cargo.toml` 列出 **81 workspace members** 与 **244 workspace dependencies**；`Cargo.lock` 有 **1,303 packages**：1,218 registry、81 workspace/path、4 git。
- git source 包括 `async-openai`/`async-openai-macros` 固定 revision `95b52e...`，`nucleo`/`nucleo-matcher` 固定 revision `5b74652...`。Pin 避免 floating HEAD，但 fork 账号、build script、commit provenance 仍需审核。
- 核心依赖横跨 Tokio/Axum/Reqwest/Rustls、Ratatui、Git/Gix、OAuth、MCP/ACP、OpenTelemetry、SQLite、PDF/image、平台 API、sandbox/process controls，依赖面远大于一个普通 CLI。
- 根 workspace 与多个 Cargo manifest 是 generated mirror；公开 commit 又对应内部 `SOURCE_REV`。GitHub commit 是本研究可固定的快照，但发布 binary 与内部 build pipeline 的完整 lineage**待核验**。
- `third_party/` 含 vendored Mermaid stack，README 还声明 tools 有 Codex/OpenCode in-tree source ports；整仓复制会带来 notice/变更声明和后续同步负担。
- 构建需要 Rust 1.93.0、DotSlash/protoc；当前环境三者均无，因此没有执行任何 build.rs、proc macro 或 fetched tool。Dependabot API 404，不能声称依赖图无 advisory。

#### README / docs / commits 交叉核验

- README 的 crate 分层与实际 repo tree 一致；根 `Cargo.toml` 也将 pager、shell、tools、workspace、sandbox、workflow、tool runtime 拆为独立 members。
- permissions 文档说明 deny > ask > allow、always-approve 的真实短路点和 sandbox 分层；`policy.rs` 的 deny/ask/allow 与 chain coverage 能在源码找到。
- 2026-08-03 固定 commit 的同步说明包括“skip nested checkouts in file watching”“count model-side skill reads”“state real size when short output only part of log”；本报告只对已定位到的 output/folder-trust/journal/permission 源码做结论，未定位到的 telemetry/file-watch 细节不外推。
- 前一同步 commit `780d138...` 的说明包括 permission path lexical normalization 与 vendor MCP kill switch；当前 `policy.rs` 确有 lexical normalization，但 commit message 不是独立安全审计。
- 公共 issues 关闭、PR API 404、Releases/tags 为空，SECURITY 仅指向 HackerOne；因此维护活跃可由频繁 sync commit 证明，但公开缺陷透明度有限。

#### 真实测试结果

```text
$ command -v cargo; command -v rustc; command -v dotslash
# 三者均无输出

$ git rev-parse HEAD
 e5478eff1e4050558e12e1328b85e6616632efb6

$ git ls-files | wc -l
3024
```

准确结论：本机未编译任何 crate，也未运行 workflow/permission/sandbox/TUI/ACP 测试。源码中存在大量 tests、固定 toolchain 与上游同步活动都不能替代本机运行证据；特别是 shell parsing、cross-platform process cleanup 和 OS sandbox 行为均待核验。

#### 可复用经验

- 当 repository 能提供 permission、plugin、hook、agent、workflow 或环境配置时，应优先把所有“会改变 authority/effect”的入口放进同一个 trust-surface registry，因为只 gate 可执行文件会漏掉配置型提权；边界是 registry 必须与真实 loader 共源并做 drift tests。
- 当 shell allow rule 面向链式命令时，应优先要求每个可解析 segment 都独立匹配，并让不确定 grammar 降级 Ask/Blocked，因为只匹配整串 prefix 可能放过后续副作用；边界是 OS sandbox 仍不可省。
- 当 workflow 支持 crash resume 时，应优先用 dense sequence + operation kind + canonical request hash 重放结果，因为同一个“第 N 步”在脚本或输入变化后不再是同一个调用；边界是 journal 还需 run/script identity、lock 和 tamper evidence。
- 当长输出无法全部进入模型上下文时，应优先把 preview、`bytes_seen/truncated` 和可恢复 full-output pointer 一起交付，因为无标记截断会让 Agent把片段当全量；边界是 pointer 的访问权限和 retention 也必须校验。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/authority-and-resume-envelope/` 做纯 Python 离线 fixture（今日只设计，不改 production）：

1. `authority_surface.json` 枚举 `config/skill/hook/plugin/cron/env/tool`，每项带 `source_scope, loader, effect, trust_state`。
2. `operation.jsonl` 记录 `seq, kind, canonical_request_hash, run_id, script_hash, result_state, receipt_ref`。
3. fixtures 覆盖：repo permission-only surface、`git status && rm`、wrapper/inline shell ambiguity、旧 journal + 新参数 divergence、torn final line、preview truncated but pointer missing。
4. validator 要求 unknown authority surface blocked；allow chain 必须全段覆盖；replay 必须匹配 run/script/request identity；truncated output 必须有 bytes_seen 与授权 pointer。
5. 不安装 Grok、不执行 shell payload、不改 Hermes config/model/provider/cron，不调用 OpenClaw。

#### 风险边界

- **License**：first-party Apache-2.0；registry/git dependencies、vendored Mermaid、in-tree ports、themes/assets、预编译 binary 和站外 installer 另审。
- **维护活跃度**：固定 commit 在查询前约 6 小时同步，活动非常新；但仓库创建约 3 周、由 monorepo 镜像同步、关闭公开 issues/PR、无 GitHub release/tag，公开治理与 release lineage有限。
- **安全风险**：terminal/edit/web/MCP/hooks/plugins/custom models、project config、credentials 和 sandbox 都接近宿主权限；任何 parser、trust gate 或 path normalization缺口都可能放大为本地副作用。
- **文档边界**：permissions 文档明确 hooks fail open，read-only list 不是 security boundary，always-approve 仍是高风险 mode；不能把 policy UX 当 OS enforcement。
- **恢复边界**：journal hash 不是签名，append+sync 不是多文件事务，host side effect 可能在 result record 前完成；exactly-once 仍待外部 idempotency key/receipt。
- **运行局限**：本机无 Rust/DotSlash，所有编译、测试、性能、sandbox 和平台差异均待核验。
- **不适用场景**：shared hub 不需要迁移 81-crate TUI/runtime；应只吸收窄 contract 和离线 fixtures。
- **不可自动执行**：不运行 `curl | bash` installer、不登录、不启用 always-approve、不加载 repo hooks/plugins/MCP、不修改 sandbox/系统权限。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`authority-surface registry + request-bound journal replay + recoverable truncation contract`，适用于 Hermes cron、subagent、tool output 和 shared-hub governance。
- **需验证**：先用离线 fixtures 证明 loader/gate 共源、segment coverage、run/script/request identity、torn-tail 与 pointer authorization；再与既有 orchestrator protocol、verification-first、completion-contract、effect-scope 候选去重。
- **暂不沉淀**：Grok 产品集成、permission parser Rust 实现、TUI/ACP、OS sandbox、always-approve mode、monorepo build/release流程；本机无 runtime 证据且依赖/权限面过大。
- **今日动作**：只更新 project card 与 runtime lessons，提出 candidate；不新建 shared skill，不写 curated active fact，不复制上游源码。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/authority-and-resume-envelope/{schema.json,fixtures/,validate.py,test_contract.py,README.md}`。
2. **现有学习编排器候选**：在 `scripts/github_learning_orchestrator.py` 的 status/audit receipt 旁增加 `run_id, report_hash, instruction_hash, attempt, terminal_state`；先 POC，不直接改生产脚本。
3. **现有 shared skill 候选**：若 fixtures 通过，优先更新 `capabilities/skills/research/github-hot-project-learning/` 和 `capabilities/skills/autonomous-learning/orchestrator-protocol/`，不创建名为 Grok 的产品 skill。
4. **shared 分层**：clone/API/stdout 留 `runtime/hermes/`；完整日报留 `inbox/hermes/daily/`；候选晋升仍走治理评分、去重、脱敏与人工/总控 gate。
5. **跨 Agent 中立层**：只共享 authority/operation/receipt schema；未来 agent 各自实现 loader adapter。当前 OpenClaw runtime 不存在，本任务不创建或调用 OpenClaw adapter。

---

### 2. openai/codex-security

**基本信息（GitHub API）**

- URL：https://github.com/openai/codex-security
- Stars：**8,370**；Forks：**571**；Language：TypeScript；License：**Apache-2.0**。
- 创建：2026-07-13T22:00:13Z；updated：2026-08-03T23:40:03Z；pushed：2026-08-03T23:39:59Z；`open_issues_count=111`（含 PR，不能解释为 111 个缺陷）。
- 固定 default-branch commit：[7b7e031df81d](https://github.com/openai/codex-security/commit/7b7e031df81d712db4e8a309728f975229628114)，commit time 2026-08-03T23:08:12Z，message `feat: add verbose security scan diagnostics (#63)`。
- 最新 GitHub Release：[npm-v0.1.5](https://github.com/openai/codex-security/releases/tag/npm-v0.1.5)，published 2026-07-31T16:08:45Z；release asset `openai-codex-security-0.1.5.tgz` 有 GitHub API digest `sha256:173e8a22...559a4`、size 997,638 bytes。本次没有下载 asset 或独立验签。
- 当前 main `package.json` 仍是 0.1.5，但 main commit 晚于 release tag commit `66778d0d...`，因此本报告源码结论不能外推为 release artifact 行为。

#### 一句话判断

Codex Security 值得学的不是“让 LLM 找漏洞”，而是它把 **target canonicalization、untrusted finding comparison 的工具剥离、canonical scan contract、coverage truth、artifact seal、私有 output/state 与 credential lock**做成产品 SDK 的确定性外壳；这为 shared hub 的研究报告、审计和知识库 projection 提供了更完整的证据契约参考。

#### 解决的问题：替代了什么旧做法

1. 替代按用户字符串直接扫描路径的做法：repository 先 realpath，path target 必须存在且 canonical path 留在 repo 内；Git refs 用 `rev-parse --verify --end-of-options` 固定 commit。
2. 替代让环境中的 `GIT_DIR/GIT_WORK_TREE/...` 偷换 target 的做法：公开校验拒绝这些变量，内部 Git 调用删除所有 `GIT_*` 并解析 trusted executable。
3. 替代让模型比较历史 findings 时继续读文件、联网或调用 shell 的做法：comparison thread read-only、approval never、network/web/tools/plugins/multi-agent 全关，输入明确标注 untrusted JSON。
4. 替代从 Markdown report 反解析事实的做法：`scan-manifest.json`、`findings.json`、`coverage.json` 是 canonical documents，report/SARIF 是 projection。
5. 替代“0 findings 就 complete”的做法：coverage 独立记录 included/excluded paths、surfaces、receipt refs、deferred work 和 complete/partial/unknown。
6. 替代只校验 JSON schema 的做法：SDK 还重算 finding identity、检查 scan ID/scope一致性、artifact digest、regular non-symlink file、root identity 与 expectation。
7. 替代把 credential/output 放在 repo 任意目录的做法：private mode/owner/ancestry、symlink replacement checks、per-process lock token 与 stale lock quarantine。

边界：Codex Security 自己的 SECURITY.md 明确它不是多用户/多租户隔离边界；扫描 subprocess 仍可能继承 `GITHUB_TOKEN`、`AWS_SECRET_ACCESS_KEY` 等非 OpenAI credentials；`approvalPolicy: never` 也不等于只读。LLM 扫描仍可能漏报、误报或被输入影响。

#### 架构 / 实现与数据流

```text
CLI / TypeScript SDK
        │
        ├─ normalizeRepository / normalizeTarget
        │    ├─ realpath + repo containment
        │    └─ trusted git + immutable revisions
        │
        ├─ state + credential runtime
        │    ├─ private output ancestry
        │    ├─ isolated Codex home
        │    └─ lock owner token / stale quarantine
        │
        ▼
Bundled Codex Security plugin + workbench (Python, SQLite)
        │
        ├─ inventory / discovery / validation / coverage
        └─ artifacts + detailed receipts
        │
        ▼
canonical semantic bundle
  ├─ scan-manifest.json
  ├─ findings.json
  └─ coverage.json
        │ schema + semantic + seal + expectation validation
        ▼
SDK result / deterministic projections
  ├─ report.md
  ├─ SARIF / CSV
  └─ saved scan history / comparison
```

Target 层先把 path/ref 变成 canonical scope；runtime 准备 private scan/credential roots 与 bundled plugin；scan 产出 artifacts、findings、coverage 后由 finalization 构造 canonical bundle。SDK `loadContract` 不只 parse，还校验 schema complexity、document size、cross-document identity、derived fingerprints、artifact seal、receipt path 和 requested target expectation。历史比较只把 canonical findings 给一个被剥离工具和网络的模型 turn，随后本地 validator 拒绝 invented/duplicated occurrence IDs。

#### Repo tree 摘要

```text
codex-security/                                  # fixed commit tracked paths: 192
├── README.md / SECURITY.md / LICENSE            # 产品入口、真实 threat model、Apache-2.0
├── .github/workflows/                           # Node/container CI 与 release cut
├── Dockerfile / compose*.yaml
├── docker/                                      # entrypoint、seccomp、AppArmor、release verify
└── sdk/typescript/
    ├── package.json / pnpm-lock.yaml            # CLI/SDK 与 110-entry lock graph
    ├── bin/codex-security.mjs                   # CLI launcher
    ├── src/
    │   ├── targets.ts                           # repository/path/ref canonicalization
    │   ├── runtime.ts                           # state/output/plugin/credential安全边界
    │   ├── contract.ts                          # canonical contract + seal validation
    │   ├── scan-comparison.ts                   # restricted finding reconciliation
    │   ├── api.ts / result.ts / cli.ts          # scan orchestration 与 public surface
    │   └── multiscan.ts / bulk-scan-discovery.ts# batch/resume/discovery
    ├── _bundled_plugin/
    │   ├── schemas/                             # manifest/findings/coverage JSON schemas
    │   ├── references/scan-contract.md          # canonical semantics
    │   ├── scripts/                             # Python workbench/finalization/projection
    │   └── skills/                              # scan/validation/attack-path/writeup workflows
    └── tests-ts/                                # 30+ TypeScript test files
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `sdk/typescript/src/targets.ts` | target identity | realpath、repo containment、ref→commit、GIT env isolation、trusted executable |
| `sdk/typescript/src/scan-comparison.ts` | restricted model reconciliation | tools/network/plugins/multi-agent off；JSON schema；本地 ID uniqueness/invention check |
| `sdk/typescript/src/contract.ts` | completion verifier | bounded JSON/schema、cross-document consistency、fingerprints、seal/hash、path/symlink/root identity、expectation |
| `sdk/typescript/src/runtime.ts` | local state boundary | private credential/output root、ancestry、lock、stale quarantine、safe ZIP extraction、trusted Python/workbench |
| `sdk/typescript/_bundled_plugin/references/scan-contract.md` | semantic SSOT | canonical docs、target snapshot、finding identity、coverage、projection 分离 |
| `sdk/typescript/plugin-files.json` | shipped asset allowlist | 明确 bundled plugin 的 schemas/scripts/skills/assets inventory |
| `sdk/typescript/package.json` / `pnpm-lock.yaml` | dependency truth | Node engine、pnpm pin、12 runtime deps、package/release scripts |
| `SECURITY.md` | actual threat model | same-OS-user 非隔离、env 继承、authorized target/output、prompt injection 与 false positive 的边界 |

#### 源码精读（固定 commit）

**代码块 1：path target 必须 realpath 后仍在 repository 内**  
来源：[`targets.ts#L158-L274`](https://github.com/openai/codex-security/blob/7b7e031df81d712db4e8a309728f975229628114/sdk/typescript/src/targets.ts#L158-L274)

```typescript
export async function normalizeTarget(
  repository: string,
  target: ScanTarget,
  signal?: AbortSignal,
): Promise<NormalizedTarget> {
  const root = await normalizeRepository(repository, signal);
  if (target === "repository") return { kind: "repository", paths: [] };

  // DiffTarget resolves base/head to immutable commits.
  if (target instanceof DiffTarget) {
    await requireGitRepository(root, signal);
    const base = await resolveGitRef(root, target.base, signal);
    // refs/working_tree return resolved base/head plus original ref names
  }

  const paths: string[] = [];
  for (const value of target) {
    const candidate = isAbsolute(expandHome(value))
      ? resolve(expandHome(value)) : resolve(root, expandHome(value));
    const canonical = await realpath(candidate);
    const relativePath = relative(root, canonical);
    if (relativePath === ".." || relativePath.startsWith(`..${sep}`)
        || isAbsolute(relativePath)) {
      throw new InvalidTargetError(`Path target is outside the repository: ${value}`);
    }
    paths.push(relativePath.split(sep).join("/") || ".");
  }
  return { kind: "paths", paths };
}
```

逻辑：target identity 不是 display path；repository 与每个 path 都 canonicalize，symlink escape 会在 `relative(root, canonical)` 后被拒绝。DiffTarget 要求传入的 repository 本身就是 worktree root，base/head 再固定为 commit SHA。边界是 SECURITY 明确正常 Git 操作仍可使用 repo config/hooks/filters/credential helpers；canonical path 解决 scope identity，不等于 Git execution sandbox。

**代码块 2：历史 finding comparison 主动关闭工具、网络和高权 feature**  
来源：[`scan-comparison.ts#L75-L131`](https://github.com/openai/codex-security/blob/7b7e031df81d712db4e8a309728f975229628114/sdk/typescript/src/scan-comparison.ts#L75-L131)

```typescript
export async function matchScanFindings(input, options = {}) {
  const codex = options.codex ?? new Codex({
    env: await comparisonEnvironment(options.environment, accountStatus, options.signal),
    config: {
      allow_login_shell: false,
      "features.apps": false,
      "features.code_mode": false,
      "features.multi_agent": false,
      "features.plugins": false,
      "features.shell_tool": false,
      "features.unified_exec": false,
      shell_environment_policy: {
        inherit: "core",
        exclude: ["CODEX_HOME", "*KEY*", "*SECRET*", "*TOKEN*"],
      },
    },
  });
  const thread = codex.startThread({
    sandboxMode: "read-only",
    approvalPolicy: "never",
    networkAccessEnabled: false,
    webSearchMode: "disabled",
    skipGitRepoCheck: true,
  });
  const turn = await thread.run(comparisonPrompt(input), { outputSchema: /* strict schema */ });
  return validateComparison(input, JSON.parse(turn.finalResponse), false);
}
```

逻辑：比较只是对 before/after semantic records 做 root-cause reconciliation，不需要读取 workspace 或联网；prompt 还明确 JSON 是 untrusted data。模型只可输出 high-confidence groups 与 uncertain pairs，本地 `validateComparison` 再拒绝 unknown ID、重复 match、重复 uncertain pair。边界是 credentials 仍用于模型调用，known-name exclude 不是完整 secret DLP；模型相似性判断也不是等价证明，所以 contract 明确 ambiguous 仍 unresolved。

**代码块 3：completed contract 不只过 schema，还要过 cross-document 和 seal 校验**  
来源：[`contract.ts#L92-L200`](https://github.com/openai/codex-security/blob/7b7e031df81d712db4e8a309728f975229628114/sdk/typescript/src/contract.ts#L92-L200)

```typescript
export async function loadContract(scanDirectory: string, options): Promise<LoadedContract> {
  const scanRoot = await requireScanRoot(scanDirectory, options.signal);
  const documentDigests = new Map<string, string>();
  const payloads = {
    "scan-manifest.json": await readScanJson(scanRoot.path, "scan-manifest.json", documentDigests),
    "findings.json": await readScanJson(scanRoot.path, "findings.json", documentDigests),
    "coverage.json": await readScanJson(scanRoot.path, "coverage.json", documentDigests),
  };
  for (const [filename, schemaName] of Object.entries(DOCUMENTS)) {
    const schema = await readJson(join(options.pluginRoot, "schemas", schemaName));
    requireSchemaComplexity(schema, schemaName);
    if (!createValidator().compile(schema)(payloads[filename])) throw schemaError(/*...*/);
  }
  if (findings.scanId !== manifest.scan.id || coverage.scanId !== manifest.scan.id)
    throw new ContractValidationError("Canonical contract scan IDs do not match.");
  validateCanonicalContract(manifest, findings);
  await validateSeal(scanRoot.path, manifest, findings, coverage, documentDigests, options.signal, scanRoot);
  if (options.expectation) validateExpectation(manifest, coverage, options.expectation);
  await verifyScanRoot(scanRoot, options.signal);
  return { manifest, findings, coverage };
}
```

逻辑：文档先做 byte/depth/schema complexity 上限，再验证 scan ID 与 include/exclude scope 一致；本地重算 finding fingerprint/findingId/occurrenceId，检查 remote URL、safe relative paths、sealed artifact SHA-256、coverage receipt 和 root inode/device。边界是截至固定 commit，[issue #230](https://github.com/openai/codex-security/issues/230) 称 finding writeups/hardening portfolio 被引用但未纳入 seal；[PR #240](https://github.com/openai/codex-security/pull/240) 仍 open，所以不能声称所有 derived files 已被 seal 覆盖。

**代码块 4：credential-home lock 绑定目录 identity 与随机 owner token**  
来源：[`runtime.ts#L312-L447`](https://github.com/openai/codex-security/blob/7b7e031df81d712db4e8a309728f975229628114/sdk/typescript/src/runtime.ts#L312-L447)

```typescript
export async function acquireCodexSecurityCredentialHomeLock(
  codexHome: string,
  signal?: AbortSignal,
): Promise<() => Promise<void>> {
  const homeMetadata = await requireSecureCredentialHome(codexHome);
  const expectedDevice = homeMetadata.dev;
  const expectedInode = homeMetadata.ino;
  const lock = join(codexHome, ".codex-security-scan.lock");
  const ownerPath = join(lock, "owner.json");
  const token = randomUUID();

  while (true) {
    await requireSecureCredentialHome(codexHome, { expectedDevice, expectedInode });
    if (await recoverStaleCredentialHomeLock(lock)) continue;
    await mkdir(lock, { mode: 0o700 });
    await writeFile(ownerPath, `${JSON.stringify({ pid: process.pid, token })}\n`,
                    { encoding: "utf8", flag: "wx", mode: 0o600 });
    return async () => {
      const owner = JSON.parse(await readFile(ownerPath, "utf8"));
      if (owner.token !== token) throw new PluginBootstrapError("lock is no longer owned");
      await rm(lock, { recursive: true, force: true });
    };
  }
}
```

逻辑：每次使用前重验 credential home 是 private non-symlink directory，且 device/inode 未被替换；lock dir 以原子 mkdir 竞争，owner file 用 `wx`，release 前再校验随机 token。stale owner 的 PID 不存在时先 rename 到 quarantine 再删。边界是同 OS account 不是 adversarial tenant boundary，PID reuse/平台 ACL/进程崩溃都需测试；当前 open [PR #229](https://github.com/openai/codex-security/pull/229) 还在改进 owner-name/no-process 的 stale reclaim，不能外推为已合并。

#### 依赖分析与供应链风险

- `package.json` version 0.1.5；Node engine `^22.13.0 || ^24.0.0 || ^26.0.0`，package manager 固定 `pnpm@11.9.0` 及其 integrity。
- 12 个 runtime direct dependencies：`@inquirer/prompts`、`@octokit/core`、`@openai/codex`、`@openai/codex-sdk`、Ajv、extract-zip、fast-uri、fflate、incur、papaparse、pdfjs-dist、smol-toml。
- `pnpm-lock.yaml` 解析为 110 packages / 110 snapshots / 1 importer；真实安装输出为 `+95` packages。Codex runtime、PDF/ZIP/CSV parsers、CLI prompts 与 schema validator 都是可处理不可信输入的供应链面。
- `plugin-files.json` 列出 90+ shipped schemas/scripts/skills/references/assets；低层 TS SDK 会装载 Python workbench 与 bundled plugin，package 不是纯 TypeScript library。
- `pnpm audit --prod --audit-level high` 返回 0 known vulnerabilities，只覆盖当前 pnpm advisory/lock graph；不覆盖 prompt injection、Python stdlib/SQLite、Codex binary、container base image、model service 或未入库漏洞。Dependabot API 404，状态待核验。
- GitHub Release asset有 API digest，但本次未下载、未核对 npm registry tarball、Sigstore/attestation 或 container manifest；package provenance 只在定向 tests 中验证逻辑，真实 release provenance 待核验。

#### README / SECURITY / release / issues 交叉核验

- README 的 repository/path/diff scan、history compare、container bulk scan 与实际 targets/comparison/multiscan 文件一致。
- `scan-contract.md` 明确 canonical JSON 与 Markdown/SARIF projection 分离，coverage 防止把 not scanned 当 no issue；`contract.ts` 实际验证这些文档与 seal。
- SECURITY 明确 only trusted/authorized repositories、same OS account 不隔离、Git/config/env 不是独立边界、非 OpenAI credentials 可能继承；本报告据此不把 `approvalPolicy: never` 描述成安全沙箱。
- release `npm-v0.1.5` 早于固定 main；release notes提到 private output、release hardening 和 scan recovery，但 main 新增了后续 diagnostics/fixes，不能混用版本。
- [issue #231](https://github.com/openai/codex-security/issues/231) 报告 target remote 的 tab/newline/CR 可能被 `new URL()` strip；[PR #233](https://github.com/openai/codex-security/pull/233) 仍 open。固定 `contract.ts` 没有显式 control-character reject，因此状态是**待修复/待核验**。
- [issue #230](https://github.com/openai/codex-security/issues/230) 与 open PR #240 说明 writeup/hardening seal 仍在演进。
- open [PR #241](https://github.com/openai/codex-security/pull/241) 提议为 committed diff target记录 content digest；说明 commit ref 之外，reviewed diff bytes identity 仍是活跃改进点。
- open [PR #208](https://github.com/openai/codex-security/pull/208) 收紧 submodule recursion/credentials；不能把其能力写成当前 main 已实现。

#### 真实测试与审计结果

```text
$ npx --yes pnpm@11.9.0 install --frozen-lockfile
✓ Lockfile passes supply-chain policies (110 entries in 4.4s)
Packages: +95
Done in 5.7s using pnpm v11.9.0

$ npx --yes pnpm@11.9.0 run build
$ node --run clean && tsc -p tsconfig.build.json

$ npx --yes pnpm@11.9.0 run lint
$ tsc --noEmit

$ npx --yes pnpm@11.9.0 run audit:prod
No known vulnerabilities found
```

```text
$ npx --yes pnpm@11.9.0 exec bun test ...
[ERR_PNPM_RECURSIVE_EXEC_FIRST_FAIL] Command "bun" not found

$ npx --yes bun@1.3.13 test --timeout 30000 \
  ./tests-ts/targets.test.ts \
  ./tests-ts/contract.test.ts \
  ./tests-ts/scan-comparison.test.ts \
  ./tests-ts/scan-recovery.test.ts \
  ./tests-ts/package-provenance.test.ts

81 pass
0 fail
364 expect() calls
Ran 81 tests across 5 files. [63.30s]
```

覆盖：target canonicalization/trusted Git、contract size/schema/path/seal/expectation、restricted scan comparison ID validation、malformed scan recovery、package provenance逻辑。准确边界：

- 只跑 5 个 test files 的 81 tests，不是整个仓库 test suite。
- 没有运行真实 Codex/model scan、login/auth、API integration、container、bulk scan、Windows ACL、SARIF/export、release download 或 npm publish。
- build/lint/audit 与 tests 使用当前 main source，不证明 npm-v0.1.5 release asset完全一致。
- `pnpm audit` 0 findings 不等于无 supply-chain 或产品安全风险。

#### 可复用经验

- 当用户给出 workspace/path/ref 作为高权任务 target 时，应优先 canonicalize、固定 immutable revision 并验证 containment，因为 display path、symlink 和 Git env 都可能改变真实对象；边界是 target identity 不替代执行 sandbox。
- 当 LLM 只需比较已结构化记录时，应优先关闭文件、shell、plugin、network 和 multi-agent能力，并在返回后本地验证 allowed IDs，因为不必要工具只会扩大 prompt injection 与 secret surface；边界是模型调用本身仍需最小凭据和数据政策。
- 当报告要作为“完成”证据时，应优先以 canonical semantic documents + coverage + sealed artifact hashes 为真相，再生成 Markdown/SARIF projection，因为 prose 不能稳定承载 identity 与 completeness；边界是 seal 必须覆盖所有被信任的 derived artifact。
- 当本地 state 含 credential 或敏感结果时，应优先校验 private mode、owner、ancestry、symlink/device/inode 和 lock owner token，因为 chmod 700 单点检查不足以防 parent replacement；边界是同 OS account 不构成租户隔离。
- 当安全扫描返回 0 findings 时，应优先检查 coverage 是 complete/partial/unknown 和 deferred units，因为“没发现”可能只是“没检查”；边界是 complete coverage 仍不证明没有漏洞。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/sealed-research-receipt-v2/` 构建离线 validator（今日只设计）：

1. canonical docs：`run-manifest.json`、`projects.json`、`coverage.json`；Markdown 日报只作 projection。
2. target contract：`date, runner, instruction_hash, repo, fixed_revision, report_path, report_hash`。
3. artifacts：API snapshot、repo tree、source excerpts、test receipt、audit receipt；每项有 size/hash/state。
4. fixtures：symlink report、stale revision、API missing、test blocked、partial coverage + 0 findings、writeup referenced but unsealed、audit hash mismatch。
5. validator 只读历史日报/runtime fixture；不调用模型、不扫描用户仓库、不读取 credential、不改 production orchestrator/config/cron。

#### 风险边界

- **License**：repo/package Apache-2.0；npm dependencies、Codex binary/runtime、bundled plugin assets、Python workbench、container image/base、模型服务条款另审。
- **维护活跃度**：固定 main commit 查询前约 32 分钟，PR/commit 高活跃；但仓库创建约 3 周、版本 0.1.5、open items 很多，target/seal/lock/release contract 正快速变化。
- **安全风险**：工具会读取源码、调用模型、运行 Git/Python/workbench、持久化 findings/credentials；SECURITY 明确其他环境 credentials 可被 subprocess 继承。
- **scope 风险**：realpath/commit binding 很强，但 repo Git config/hooks/filter/credential helper 不被视为独立边界；扫描未经授权或恶意仓库仍危险。
- **completion 缺口**：open issue #230/#231 与 PR #240/#241 显示 remote sanitization、derived artifact seal、diff content identity 尚在演进。
- **LLM 局限**：comparison/scan 的 schema 和 local validator只约束输出形状与 identity，不能证明 semantic judgement 正确；false negative/positive 仍存在。
- **运行局限**：只有定向 81 tests；无真实模型、auth、container、Windows、full suite 和 release provenance验证。
- **不适用场景**：shared hub 已有 governance/reflection/audit，不应复制 Codex Security 的整个扫描产品、评分或 credential home。
- **不可自动执行**：不 `npm install -g`、不 login、不传 API key、不扫描任何私有/第三方 repo、不应用 patch、不上传 findings、不修改用户凭据或配置。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`target-bound sealed research receipt + coverage-aware completion + restricted semantic comparison`，与 GitHub learning、research audit、知识库 projection 高度相关。
- **需验证**：离线历史 replay 必须证明 target/report/audit hash 一致、partial coverage 不完成、unsealed derived artifact 被拒绝、comparison adapter 只能使用 allowlisted IDs；再与现有 GitHub learning/verification/governance skills 去重。
- **暂不沉淀**：Codex Security 产品集成、bundled security skills、model scan、credential runtime、workbench、container/release workflow；高权且与本地系统重叠。
- **今日动作**：只更新既有 project card/lessons 与日报 candidate；不复制上游 skill/scripts，不创建 shared skill，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/sealed-research-receipt-v2/{schemas/,fixtures/,validate.py,test_receipt.py,README.md}`。
2. **研究证据 manifest 候选**：由 `scripts/github_learning_orchestrator.py` 未来生成 `runtime/hermes/github-hot-project-learning/evidence-manifest.json`，记录 source state、fixed commit、artifact hash、coverage 与 audit report hash；先做 sidecar，不破坏兼容路径。
3. **知识库 projection**：inbox report 是 source artifact，`/mnt/d/.../每日学习/...` 是 projection；copy 后记录 source/destination hash。projection失败不冒充整体 published。
4. **现有 shared skill 候选**：验证后优先更新 `capabilities/skills/research/github-hot-project-learning/` 的 evidence/coverage/receipt 条款，并与 shared governance 去重；不引入 Codex Security 产品 skill。
5. **未来跨 Agent**：共享 canonical schema/fixtures，agent adapter 只负责采集。当前 OpenClaw runtime 不存在，本任务未创建、调用或修改 OpenClaw。

## 横向对照：authority 与 completion 必须形成闭环

| 层次 | Grok Build | Codex Security | Hermes/shared hub 候选 |
|---|---|---|---|
| target identity | cwd/git-root、tool path、session owner | canonical repo/path、resolved commit、target snapshot | date + runner + repo + revision + report path/hash |
| authority input | repo config/plugin/hook/env/agent trust surfaces | authorized target/output、trusted executables、restricted model turn | config/skill/cron/tool/source surface registry |
| effect gate | deny/ask/allow、chain segment、sandbox | read/write/output/state boundaries、approval never | operation effect/scope policy at final tool chokepoint |
| resume identity | seq + kind + canonical request hash | scan ID、target snapshot、saved workbench state | run/script/instruction hash + operation request hash |
| completion evidence | typed terminal、journal result、recoverable output pointer | canonical docs + coverage + seal + expectation | report + evidence manifest + audit receipt + KB projection receipt |
| uncertain state | AskFailClosed / Paused / Budget / Cancelled | partial/unknown/deferred/uncertain | blocked/partial/unobserved/failed/completed |
| hard boundary | host process, project trust, optional OS sandbox | same OS account、env/Git/model/service trust | Hermes tools + filesystem scope + governance/approval gate |

## 经验沉淀

1. 当 repository/config/skill/hook/plugin 能改变执行或授权时，应优先把它们统一登记为 authority surfaces，并让 gate 与真实 loader 共用发现逻辑，因为配置型入口同样能提权；边界是 registry 仍需 drift/adversarial tests。
2. 当 shell 或复合工具请求包含多个 segment/wrapper/inline interpreter 时，应优先逐段授权并对不确定解析 fail closed/Ask，因为整串 prefix allow 可能掩盖后续副作用；边界是 parser 不能替代 OS sandbox。
3. 当可恢复 workflow 重放旧结果时，应优先绑定 run/script identity、dense sequence、operation kind 与 canonical request hash，因为调用位置相同不代表语义相同；边界是 journal 还需 lock、idempotency 和 tamper evidence。
4. 当用户指定 path/ref/workspace 作为高权目标时，应优先 realpath、containment check 与 immutable revision，因为 symlink、相对路径和 Git environment 能改变真实对象；边界是固定 target 不等于授权执行任意 Git hook。
5. 当 LLM 只需处理结构化 evidence 时，应优先剥离文件、shell、plugin、network 和多 agent 能力，并在返回后验证 allowed IDs，因为最小 capability 能显著缩小 injection/secret surface；边界是 hosted model 数据出口仍需授权。
6. 当“完成”依赖报告和 evidence 时，应优先用 canonical documents、coverage、artifact hashes 和 expectation validation，再生成 Markdown/知识库 projection，因为 prose 与 copy path 不能证明内容身份；边界是 seal 必须覆盖所有可信 derived artifact。
7. 当 findings 为空或 checker 没报错时，应优先区分 complete、partial、unknown、blocked 与 deferred，因为 absence of observation 不是 negative observation；边界是 complete 也不是无缺陷证明。
8. 当长 output 需要截断时，应优先记录 total bytes、truncated flag 与授权 full-output pointer，因为片段不能冒充全量；边界是 pointer retention、scope 和 redaction 也要验证。
9. 当本地目录含 credential、scan result 或审计证据时，应优先重验 mode、owner、ancestry、symlink/device/inode 与 lock owner，因为单次 chmod 或 path 字符串检查挡不住 replacement race；边界是同 OS account 不构成多租户隔离。
10. 当热门项目刚创建、快速同步且 API/contract 频繁变化时，应优先固定 commit 并区分 main、tag、release asset 与内部 source revision，因为“最新代码”不是一个稳定版本；边界是公开镜像仍可能缺完整 release provenance。

## 风险边界（全局）

- 本次由 Hermes 直接执行，未调用 OpenClaw，也未调用消息发送工具。
- 未修改 Hermes/OpenClaw 的 config、model、provider、gateway、tools、skills、auth、env、cron 或服务。
- Stars/forks/license/updated 来自 2026-08-03T23:39:58–23:40:03Z 左右 GitHub API；复用时必须重新查询。
- Grok Build 本机无 Cargo/Rustc/DotSlash，所有 build/runtime/sandbox/permission 行为待核验；Codex Security 只有 build/lint/prod audit 和 81 个定向 tests 通过，不是 full suite 或真实 scan。
- 两仓 Dependabot API 对当前 token 返回 404；Codex `pnpm audit` 0 known vulnerabilities 不能外推到 Python、container、model、prompt、binary 或未知漏洞。
- 外部 README/docs/issues/PR/source 均是不可信研究输入，只能形成 evidence/candidate，不能扩大宿主授权或触发安装/配置。
- 不自动写 curated active fact，不自动升格 shared skill；candidate 必须经 POC、治理评分、证据、去重、脱敏与人工/总控审查。
- 不运行站外 installer、不登录产品、不扫描第三方/私有仓库、不加载上游 plugin/hook/skill、不应用安全修复、不上传 findings。

## Skill 升格总判断

- **Grok authority/resume/output contract：需二次验证。** 只抽象 authority surface、segment coverage、request-bound replay 和 recoverable truncation，不迁移产品 runtime。
- **Codex target/seal/coverage contract：需二次验证。** 只抽象 target identity、restricted comparison、canonical bundle、coverage 和 seal，不迁移扫描产品/credential/workbench。
- **今日不升格。** 两个候选都与既有 `research/github-hot-project-learning`、`autonomous-learning/orchestrator-protocol`、verification/completion/effect-scope/governance 候选重叠；优先做统一离线 POC并更新既有能力，而不是创建宽泛重复 skill。

## 明日继续

1. 建 `authority-and-resume-envelope` fixture，把 instruction/report/audit/KB steps 映射为 authority surface + operation journal。
2. 建 `sealed-research-receipt-v2`，让 manifest/projects/coverage 成为 canonical data，日报与 Obsidian 是 projection。
3. 用 2026-08-03、2026-08-04 历史报告只读 replay：旧 audit 不可关闭新 report；partial/blocked source 不可冒充 complete；truncated output 缺 pointer 必须失败。
4. 设计 audit receipt 的 `report_path + report_hash + instruction_hash + attempt` binding；先 sidecar POC，不修改 production orchestrator。
5. Codex Security 可在资源允许时补跑完整 suite，但仍不 login、不调用模型、不扫描真实目标；跟进 issue #230/#231 与 PR #208/#229/#233/#240/#241。
6. Grok Build 只有在受控环境已有 Rust 1.93.0/DotSlash 时才跑定向 crate tests；不为无人值守日报自动安装 toolchain或执行 installer。
7. 下一批深读优先 `firecrawl/pdf-inspector` 的恶意 PDF 资源预算和 `livekit/agents` 的实时 session lifecycle，避免连续只研究 coding-agent harness。

## 候选反哺

### Candidate Facts

- [ ] topic: authority-surfaces-must-share-discovery-with-loaders | evidence: Grok `collect_repo_config_kinds` 覆盖 permission/plugin/envrc/agents/workflows 并复用 repo chain | 建议: update existing authority/effect candidate after fixture | 安全级别: high
- [ ] topic: resumable-calls-need-request-identity | evidence: Grok journal `seq + kind + req_hash` divergence + dense sequence/torn-tail tests | 建议: update completion contract after Hermes replay | 安全级别: high
- [ ] topic: canonical-research-bundle-needs-coverage-and-seal | evidence: Codex canonical manifest/findings/coverage + `loadContract` seal/expectation validation | 建议: candidate for GitHub-learning workflow | 安全级别: high
- [ ] topic: structured-LLM-comparison-should-be-capability-minimized | evidence: Codex comparison disables network/web/shell/plugins/multi-agent and validates IDs | 建议: create narrow pattern only after local adapter fixture | 安全级别: medium
- [ ] topic: truncation-needs-recoverable-full-output-reference | evidence: Grok completion delivery preview + polling/disk pointer | 建议: update tool terminal/completion candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: authority-and-evidence-completion-envelope | 可复用场景: cron、subagent、GitHub learning、research audit、KB projection | 是否建议 shared: yes（验证后更新既有 skills） | 原因: 跨 Agent 横切，但与 orchestrator/verification/completion 高度重叠，不应新建宽 skill
- [ ] 名称: sealed-research-receipt-v2 | 可复用场景: API/source/test/report/audit/knowledge projection | 是否建议 shared: yes（POC + governance 后） | 原因: 可让 coverage/identity/receipt machine-readable
- [ ] 名称: grok-build-product-integration | 可复用场景: coding agent TUI/runtime | 是否建议 shared: no | 原因: 81-crate、高权限、无本机编译/runtime证据
- [ ] 名称: codex-security-product-integration | 可复用场景: LLM 安全扫描 | 是否建议 shared: no | 原因: credential/model/repo scan 高权，与本地治理任务无直接授权

### Candidate Open Questions

- [ ] 问题: `github_learning_orchestrator.py` 如何兼容地绑定 instruction/report/audit/KB hash，同时保留现有 status.json 消费者？ | reason: adaptation/compatibility | priority: high
- [ ] 问题: API、README、source、test 各 lane 哪些是 required，谁声明 coverage complete/partial/blocked？ | reason: governance | priority: high
- [ ] 问题: report/KB projection 以 source hash 还是 canonical bundle ID 做 identity，跨文件系统 copy 如何出 receipt？ | reason: portability/atomicity | priority: high
- [ ] 问题: request journal 是否要加入 script hash、agent profile、tool schema version 与 effect policy revision？ | reason: replay correctness | priority: high
- [ ] 问题: truncated subagent output 没有 disk file 时，应强制 artifact store 还是允许 bounded inline + explicit loss？ | reason: evidence/retention | priority: medium
- [ ] 问题: Codex issue #230/#231 与相关 PR merge/release 后，main 和 release asset 的 contract 是否一致？ | reason: stale/security | priority: medium

### 不应自动落地

- 不安装或运行 Grok Build，不执行站外 installer，不加载其 plugin/hook/MCP/config，不启用 always-approve 或修改系统 sandbox。
- 不安装全局 Codex Security、不登录、不传 API key、不扫描任何真实第三方/私有仓库、不上传或应用 findings/patch。
- 不修改 Hermes/OpenClaw config、model、provider、tools、skills、auth、env、cron；当前任务不调用 OpenClaw。
- 不把今日 candidate 直接写入 curated active fact 或 shared skill manifest；先做 runtime POC、历史 replay、去重、治理评分、脱敏与人工/总控审查。
