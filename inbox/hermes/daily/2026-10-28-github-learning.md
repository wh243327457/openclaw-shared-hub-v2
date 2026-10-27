# 2026-10-28 GitHub 热门项目学习日报

> 执行者：Hermes（未调用 OpenClaw）  
> 研究窗口：2026-10-28 06:30–07:43 JST  
> 热门候选来源：GitHub Trending 日榜 HTML（`https://github.com/trending?since=daily`）；Stars、Forks、Language、License、更新时间由 `gh api repos/{owner}/{repo}` 实时读取。  
> 深读固定源码：`pbakaus/impeccable@d34c87e1a00989ae8dbdd7f6b30b70f23319e860`、`HKUDS/DeepTutor@a31d82624c27d75f4e771d4fcb78dce16470b383`。

## 今日结论

今天两类热门项目给出同一条工程主线：**跨 Agent 能力与多 workspace 数据都不能靠“复制文件 + prompt 约定”维持正确性，而应由宿主建立 canonical core、scope identity、host adapter、deterministic gate，以及 snapshot → verify → commit → recover 的状态闭环。**

## 项目速览

GitHub API 查询时间为本次运行；时间字段均为 UTC。`NOASSERTION` 表示 GitHub License API 未识别，不等于“无许可证”。

| 项目 | Stars | Language | License（GitHub API） | pushed_at | 速览判断 |
|---|---:|---|---|---|---|
| [elayadesign/ai-design-skills](https://github.com/elayadesign/ai-design-skills) | 9,193 | 未标注 | MIT | 2026-10-27T16:02:10Z | 设计 Skill 合集，今日只列入候选，不执行其安装器。 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 38,875 | CSS | MIT | 2026-10-27T15:05:53Z | 反 AI-slop 设计 Skill，与昨日候选重复，今日不深挖。 |
| [nightly-labs/openbot](https://github.com/nightly-labs/openbot) | 2,355 | TypeScript | NOASSERTION | 2026-10-27T22:30:08Z | 昨日已深读，今日避免重复。 |
| [obra/superpowers](https://github.com/obra/superpowers) | 306,372 | Shell | MIT | 2026-10-23T03:48:57Z | 多 Agent 开发工作流；已有项目卡，今日不重复。 |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 90,423 | Rust | Apache-2.0 | 2026-10-27T16:28:34Z | 一份 canonical Skill 跨 harness 编译，detector core 跨 native/HTML/browser/WASM 复用，列为深读 1。 |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 7,422 | TypeScript | Apache-2.0 | 2026-10-27T22:26:20Z | 已在 10 月 26 日研究，今日避免重复。 |
| [gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | 39,288 | TypeScript | AGPL-3.0 | 2026-10-24T18:27:21Z | 社交发布平台；AGPL 与外部平台权限面需单独审查。 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 290,818 | JavaScript | MIT | 2026-10-26T04:56:56Z | Agent 编码工作流集合；已有项目卡，今日不重复。 |
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | 45,748 | Python | Apache-2.0 | 2026-10-27T18:37:55Z | workspace 隔离、资源收窄、可恢复迁移与 shared hub 直接相关，列为深读 2。 |
| [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | 3,917 | TypeScript | Apache-2.0 | 2026-10-27T22:12:09Z | 已在 10 月 26 日研究，今日避免重复。 |
| [togg53192-cmd/jailbreaks](https://github.com/togg53192-cmd/jailbreaks) | 5,425 | 未标注 | NOASSERTION | 2026-10-25T15:21:20Z | 内容与许可都需谨慎；不读取、不执行其中 jailbreak 文本。 |

## 深读项目

### 1. pbakaus/impeccable

- **链接**：https://github.com/pbakaus/impeccable
- **固定源码提交**：`d34c87e1a00989ae8dbdd7f6b30b70f23319e860`
- **GitHub API**：Stars **90,423**；Forks **5,371**；Language **Rust**；License **Apache-2.0**；`updated_at=2026-10-27T22:30:57Z`；`pushed_at=2026-10-27T16:28:34Z`。
- **Release**：最近可见 release 包含 `skill-v4.8.0`、`cli-v4.8.0`、`engine-v0.1.18`，均发布于 2026-10-26；仓库 `package.json=4.8.0`、Cargo workspace `0.1.18`，说明 skill/CLI 与 engine 使用独立版本线。
- **一句话判断**：真正值得迁移的不是 24 条设计命令，而是“**一份 agent-neutral Skill 源 → 多 harness projection；一份 detector core → native/HTML/browser/WASM adapter；oracle 固化行为契约**”的分层方式。
- **解决的问题**：替代“给每个 Agent 手工维护一份 Skill、给 CLI/浏览器各写一套规则、靠 README 声明兼容”的旧做法；它把规则、宿主能力矩阵、构建投影、运行引擎、hook 与 release identity 分开。

#### 证据交叉核验

1. **README**：说明一份 `impeccable` Skill、24 个命令、62 条 deterministic detector；支持 Hermes 等多 harness；Hermes 无 hook surface，因此只装 Skill，不应假装 hook 可用。
2. **docs/ENGINE.md**：Rust workspace 是统一 runtime；`CLI-CONTRACT.md` 定义 observable behavior，`tests/oracle/` 做 byte-for-byte gate；同一 core 可编译成 native/WASM 并由 HTML/browser adapter 调用。
3. **docs/HARNESSES.md**：明确 provider frontmatter、skill path、hook、subagent、placeholder 能力不同，强调 point-in-time，不能把一个 harness 的能力外推到另一个。
4. **Releases/API**：skill/CLI v4.8.0 与 engine v0.1.18 分线发布，最近仍在快速变化。
5. **Issues**：#1202 报告 hook finding identity/缓存重复；#1190 报告 global install 仍写 project hook；#813 质疑二进制下载与校验 provenance。它们说明跨 harness 安装、cache identity、release provenance 仍是活跃风险面。
6. **关键源码**：直接读取 `crates/detect/src/cli.rs`、`detect_text.rs`、`engines.rs`、`crates/bundle/src/lib.rs` 及 Cargo/package manifests。

#### 架构 / 实现与数据流

```text
canonical skill/agents/reference + provider capability table
                          │
                          ▼ build transformer
 .claude/.agents/.hermes/.grok/... provider projections
                          │
                          ▼ launcher
                pinned Rust engine binary
                          │
          ┌───────────────┼─────────────────┐
          ▼               ▼                 ▼
     file/text scan   static HTML scan   browser/CDP scan
          │               │                 │
          └───────────────┼─────────────────┘
                          ▼
        impeccable-core rules + optional RulePack
                          │
        ┌─────────────────┴────────────────┐
        ▼                                  ▼
 native CLI findings              WASM/browser bundle
        │                                  │
        └────────── canonical registry ────┘
                          │
                  text/JSON/GitHub output
```

核心边界：`detect` crate 负责 target 枚举、配置、失败分类和输出；`HtmlEngine` / `UrlEngine` 是 adapter seam；`core` 保存确定性规则；`bundle` 确保 WASM 与 browser artifact 确定性构建；Skill build 再按 harness 能力做 projection。**共享的是 contract/core，不是假设所有宿主能力相同。**

#### Repo tree 摘要

固定提交有 4,422 个 tracked files；以下来自 `git ls-tree`/本地 clone 与 `docs/ENGINE.md`：

```text
impeccable/
├── skill/                  # canonical SKILL 源、agents、reference、launcher
├── scripts/                # 多 provider 构建、release、校验工具
├── crates/
│   ├── cli/                # Rust 命令路由与 exit code
│   ├── detect/             # 文件枚举、配置、text scan、CLI 输出
│   ├── foundation/         # finding、registry、Dom trait、共享类型
│   ├── core/               # 规则实现与 RulePack seam
│   ├── html/               # static HTML/cascade adapter
│   ├── browser/            # Chrome/CDP/snapshot adapter
│   ├── hook/               # provider hook 与 cache
│   ├── wasm/               # core 的 wasm-bindgen exports
│   └── bundle/             # deterministic browser/extension artifact
├── browser-bundle/         # page probe / overlay JS，不承载规则真相
├── tests/oracle/           # 跨实现行为向量与 byte contract
├── tests/skill-*           # skill activation/workflow/behavior
├── .hermes/.agents/...     # 当前仓库内 provider projection/fixture
└── docs/                   # engine、harness、release、CLI contract
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/detect/src/cli.rs` | CLI 编排 | 解析 scope/viewport/CDP；枚举 targets；记录 unreadable/engine failure；共享 browser session。 |
| `crates/detect/src/engines.rs` | adapter seam | `ScanOptions`、`HtmlEngine`、`UrlEngine`、`SharedBrowser`；缺 engine 时显式失败。 |
| `crates/detect/src/detect_text.rs` | text detector | regex/style/CSS-in-JS/page analyzer → dedupe → optional RulePack → inline ignore。 |
| `crates/core/src/rule_pack.rs` | 扩展契约 | process-lifetime RulePack；规则 pack 不可覆盖 built-in identity。 |
| `crates/bundle/src/lib.rs` | artifact 构建 | JS/WASM 固定顺序拼装、registry 生成、capture contract drift 检查。 |
| `tests/oracle/` | 兼容验证 | 固化 CLI/函数 observable behavior，防止 provider/runtime 迁移静默漂移。 |
| `scripts/lib/transformers/providers.js` | harness projection | 根据 capability matrix 生成各 provider Skill/agent/hook 形状。 |
| `docs/HARNESSES.md` | point-in-time 能力证据 | 明示 Hermes 无 hook/per-skill ACL，未知 frontmatter 会被忽略。 |

#### ⭐ 源码精读

**函数 1：`run_detect()` / `detect_cli()`——宿主先规范请求，再进入 scanner。**

```rust
pub fn run_detect(args: &[String], io: &mut Io, engines: &Engines) -> i32 {
    match detect_cli(args, io, engines) {
        Ok(code) => code,
        Err(Exit(code)) => code,
    }
}

fn detect_cli(args_in: &[String], io: &mut Io, engines: &Engines) -> Result<i32, Exit> {
    let mut args: Vec<String> = args_in.iter().map(|a| match a.as_str() {
        "-json" => "--json".to_string(),
        "-fast" => "--fast".to_string(),
        _ => a.clone(),
    }).collect();
    // 后续验证 scope / viewport / CDP 组合，构造唯一 ScanOptions。
```

逻辑摘要：兼容旧 flag 但不让 alias 泄漏进 core；非法 scope、viewport、CDP/target 组合在 scan 前失败。配置解析属于 host-owned envelope，不交给规则或模型猜。

**函数 2：`scan_targets()`——枚举失败不能静默变成 clean。**

```rust
fn scan_targets(ctx: &mut Ctx, paths: &[String], shared: Option<&dyn SharedBrowser>,
                browser_setup_failed: bool, all: &mut Vec<Finding>) -> Result<(), Exit> {
    for target in paths {
        // URL 走 shared/single browser adapter。
        let resolved = jsp::resolve(&ctx.cwd, &[target]);
        let Ok(stat) = std::fs::metadata(&resolved) else {
            ctx.had_operational_failure = true;
            ctx.io.err(&format!("Warning: cannot access {target}\n"));
            continue;
        };
        // unreadable directory/file 都调用 report_local_scan_failure，最终强制 exit 1。
    }
    Ok(())
}
```

逻辑摘要：目录 walk、文件读取、browser launch、单 target engine error 都单独保留；0 finding 与“目标没读到”不会混成同一状态。这一点可直接反哺 Hermes 审计器的 coverage/terminal 分层。

**函数 3：`detect_text()`——built-in canonical，pack 只追加并共享 waiver。**

```rust
pub fn detect_text(content: &str, file_path: &str, options: &TextOptions) -> Vec<Finding> {
    let mut findings: Vec<Finding> = Vec::new();
    findings.extend(run_regex_matchers(/* source */));
    // style blocks / CSS-in-JS / page analyzers / design-system checks ...

    let mut deduped: Vec<Finding> = Vec::new();
    for f in findings {
        let is_dupe = deduped.iter().any(|d| d.antipattern == f.antipattern
            && d.snippet == f.snippet && (d.line - f.line).abs() <= 2.0);
        if !is_dupe { deduped.push(f); }
    }
    if let Some(pack) = options.rule_pack {
        deduped.extend(pack.check_text(content, file_path, &ext));
    }
```

逻辑摘要：扩展规则在 built-in 与 dedupe 后追加、inline ignores 前进入，因此 pack 可复用同一 waiver，但没有 pack 时 built-in 输出 byte-identical。边界是 issue #1202 说明 finding cache identity 仍可能因行号漂移重复提示。

**函数 4：`ScanOptions` + engine traits——共享 contract，不共享宿主实现。**

```rust
pub struct ScanOptions {
    pub inline_ignores: bool,
    pub design_system: Option<Rc<DesignSystem>>,
    pub viewport: Option<(u32, u32)>,
    pub rule_pack: Option<&'static dyn RulePack>,
    pub keep_consent_banners: bool,
    pub keep_overlays: bool,
    pub unreported_rules: Vec<String>,
}

pub trait HtmlEngine {
    fn detect_html(&self, path: &str, options: &ScanOptions,
                   stderr: &mut dyn std::io::Write) -> Result<Vec<Finding>, EngineError>;
}
```

逻辑摘要：规则输入、浏览器 UI 处理、忽略策略都显式入参；HTML/browser 是 adapter，不把 Puppeteer/CDP 依赖塞进 text core。Hermes 不支持 hook 时必须降级为显式 CLI/审计步骤，不能伪装等价。

#### 依赖分析与供应链风险

- Rust workspace 核心依赖包括 `serde`、`serde_json`、`regex`、`once_cell`、`thiserror`，具体 browser/image/HTTP 依赖分布在各 crate；`Cargo.lock` 固定 209 个依赖节点。
- npm package 主要是 installer/shim，runtime engine 走可选 platform packages `@impeccable/cli-* 0.1.18`；dev graph含 Playwright、Puppeteer、AI SDK、Claude Agent SDK、Svelte、Zod。
- release 设计有 engine checksums、`.sha256` sidecar、签名 Skill ZIP；但 issue #813 仍质疑 hash provenance 与 tagged source 对齐，因此“有 checksum”不能自动证明独立来源可信。
- 本机固定 commit 执行 `cargo audit --json`：**9 个 RustSec vulnerability hits**，集中于 `rustls`、`rustls-webpki`、`webpki-roots`、`zip`；版本命中不等于代码可达，但不允许声称依赖 clean。
- Public repository security advisories API 返回 0 条；Dependabot endpoint 返回 403（token 缺 `admin:repo_hook`），两者均不能抵消本机 lock audit。

#### 本机验证

```bash
cargo test -p impeccable-detect --lib
# 87 passed; 0 failed; 0 ignored; finished in 0.34s
```

GitHub fixed-head checks 共 21 个：Rust、Rust Windows、oracle、Node 22/24、CLI shim、launcher 等为 success；部分 live/skill E2E 为 skipped。**success 与 skipped 分开，不外推为全路径通过。**

#### 可复用经验

- 当同一 Skill 要跨 Hermes / future agent / 其他 harness 分发时，应优先维护 **agent-neutral contract + deterministic core + host capability manifest + generated projection**，因为复制目录会漂移；边界是每个 host 仍需 acceptance fixture。
- 当 scanner 覆盖多个 target/adapter 时，应优先把 **finding、coverage、operational failure、projection** 分开，因为 unreadable target 和 clean target 不是同一结果；边界是 complete scan 也不证明没有未知规则缺口。

#### 30 分钟可尝试实验

建立一个仅含 synthetic Skill 的 projection parity fixture：canonical `SKILL.md` → Hermes/future-agent 两个 adapter；验证 frontmatter 保留/剥离、相对路径、内容 hash 与不支持能力的显式 `degraded`。不安装 Impeccable、不运行 hook、不下载 release binary。

#### 风险边界

- **License**：GitHub API、Cargo、package 与根 LICENSE 均为 Apache-2.0；可研究并按条款复用，第三方依赖许可仍需另审。
- **维护活跃度**：2026-10-27 有 push、2026-10-26 有三条 release，活跃但快速变化；必须 pin commit/artifact。
- **安全风险**：hook 可独立于模型审批执行并可能首次下载 engine；#1190 表明 scope 语义可能出错；#813 指向 provenance；本机 Cargo audit 命中 9 条 advisories。
- **局限/不适用**：设计 detector 是启发式 lint，不是通用 UI 质量证明；Hermes 无 hook，不应照搬 hook workflow；browser/live 模式扩大 Chrome/CDP/网络面。
- **未验证**：未运行完整 workspace suite、oracle、本地 browser/live/extension、release binary/hash/signature 对照、真实 Hermes 安装；RustSec 可达性待核验。

#### ⭐ Skill 升格判断

**需二次验证。** 不直接迁移 Impeccable Skill、规则或安装器。只抽象“canonical skill → host adapters → parity receipt”模式，先与现有 `shared-skill-governance`、`path-portability`、GitHub learning/verification 能力去重。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/host-capability-projection-v0/`。
2. Canonical fixture：`canonical/example-skill/SKILL.md`；adapter 输出仅落 runtime，不写 `capabilities/skills/`。
3. Capability schema：`host`, `skill_frontmatter`, `hooks`, `subagents`, `tool_acl`, `project_trust`, `degraded_reasons`, `verified_at`。
4. Verifier：`scripts/verify_skill_projection.py` 候选，读取 shared root 必须经 `resolve_shared_root.py`；比较 source hash、projection hash、遗漏能力与 unsupported fields。
5. Hermes adapter 只验证 `.hermes/skills` 形状和 trust 语义；future-agent adapter 消费同一 canonical contract；**本次不配置或调用 OpenClaw**。
6. fixture 通过且与现有能力去重后，优先迭代已有 shared-skill governance，而不是创建重复 Skill。

---

### 2. HKUDS/DeepTutor

- **链接**：https://github.com/HKUDS/DeepTutor
- **固定源码提交**：`a31d82624c27d75f4e771d4fcb78dce16470b383`
- **GitHub API**：Stars **45,748**；Forks **5,739**；Language **Python**；License **Apache-2.0**；`updated_at=2026-10-27T22:30:07Z`；`pushed_at=2026-10-27T18:37:55Z`。
- **Release**：最新可见 `v1.6.15`，发布于 2026-10-18T20:13:23Z；README 标示 2026-10-19 发布说明。固定 main 提交与该 tag 同 SHA 仍需单独比较，本文只研究固定 commit。
- **一句话判断**：它最值得 shared hub 学习的是把“workspace”拆成 **scope identity、content root、private state、account-global state、resource ceiling、background-job pinning 与 recoverable migration**，而不是只给目录换个名字。
- **解决的问题**：替代“UI 切换当前目录、后台任务跟随全局变量、Skill/MCP 全账号暴露、迁移直接 copy+delete”的旧做法；每个任务在 admission 时固定 scope，资源选择只能收窄，迁移先快照校验再 commit/cleanup。

#### 证据交叉核验

1. **README**：content workspace 与 private runtime home 分开；custom workspace 的私有数据放 `.deeptutor/data/`，可见产物放 `outputs/`；外部写入需 exact source/destination 的 Allow once。
2. **docs-for-user/workspaces.md**：账号级 settings/credentials/memory 与 workspace 数据分层；running task 保持启动时 scope；Skill/MCP/KB assignment 引用资源但不复制凭据；workspace-specific Skill 可覆盖共享版本。
3. **workspace-isolation-implementation.md**：列出 ownership 与 scope 独立检查、WebSocket 固定 scope、SQLite backup/WAL、迁移 journal/recovery，以及 application-level partitioning 边界。
4. **Release v1.6.15**：宣称 bounded tutoring memory、reliable chat recovery、reviewed learning-path changes；只是上游 release 说明，不替代本机验证。
5. **Issue #2074**：archived workspace 仍被 navigation index 读取，说明 lifecycle status 必须进入每个 reader，而不能只在 UI 隐藏。
6. **关键源码**：直接读取 `context.py`、`service.py`、`resources.py`、`data_migration.py`、`migration.py`。

#### 架构 / 实现与数据流

```text
authenticated account + requested workspace id
                  │ independent checks
                  ▼
        resolve_workspace_scope()
  owner/kind/archive/root → immutable WorkspaceScope
                  │ ContextVar pin at admission
                  ▼
        WorkspacePathService projection
  ├─ workspace-local: sessions/material/progress/cache/.deeptutor/data
  ├─ visible outputs: content_root/outputs
  └─ account-global: settings/credentials/memory/catalog
                  │
                  ├─ resource ceiling: Skills / MCP / KB
                  │       └─ turn selection can only intersect, never widen
                  │
                  └─ background task inherits original ContextVar scope

migration:
preview dependency closure + blockers
  → exclusive activity lease
  → SQLite backup / file hash snapshot
  → journal cleanup intent
  → copy + destination hash/read-back
  → session/resource rebind
  → committed marker
  → source cleanup
  → completed / recovery_required / cleanup_required
```

核心机制不是“目录隔离”四个字，而是 identity、authority、storage、lifecycle 分层：workspace ID 与 content root 绑定；认证切换清 scope；移动后 current root 必须 read-back；turn resource selection 只能做集合交集；迁移状态在 destructive cleanup 前持久化。

#### Repo tree 摘要

固定提交有 3,875 个 tracked files；以下来自 clone tree：

```text
DeepTutor/
├── deeptutor/
│   ├── agents/                  # chat/loop/learning agents
│   ├── capabilities/            # capability runtime
│   ├── services/
│   │   ├── workspace/           # scope/catalog/resources/migration/navigation
│   │   ├── session/             # session/turn durable runtime
│   │   ├── skill/               # built-in/account/workspace skill resolution
│   │   ├── mcp/                 # MCP config/manager
│   │   ├── rag/                 # 多 RAG pipeline
│   │   └── sandbox/             # system/best-effort execution boundary
│   ├── runtime/                 # worker/coordination/memory probe
│   └── tools/                   # agent tool surfaces
├── deeptutor_cli/               # Typer CLI / SDK-facing commands
├── web/                         # Next.js 16 / React 19 UI
├── tests/                       # backend, workspace, runtime, frontend/E2E
├── docs-for-user/               # workspace/security/setup contract
├── pyproject.toml               # Python core + large optional dependency graph
└── compose*.yaml / Dockerfile   # deployment surfaces
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `deeptutor/services/workspace/context.py` | scope identity | `WorkspaceScope`、ContextVar、账号切换清 scope、private/global path projection、移动后 root 重验。 |
| `deeptutor/services/workspace/service.py` | path/effect gate | stable workspace/item IDs、relative path normalize、allowed roots、`outputs/` write ceiling、runtime context。 |
| `deeptutor/services/workspace/resources.py` | resource authority | Pydantic strict schema；workspace allowlist；turn selection 只能 intersect；credential 不进 assignment。 |
| `deeptutor/services/workspace/data_migration.py` | 可恢复数据迁移 | dependency closure、active-turn blocker、SQLite backup/WAL、hash verification、journal、commit/recovery。 |
| `deeptutor/services/workspace/migration.py` | workspace root relocation | staging sibling、manifest before/after、atomic rename、catalog `BEGIN IMMEDIATE`、previous paths。 |
| `deeptutor/services/workspace/navigation.py` | 跨 workspace 聚合 | account navigation index；issue #2074 显示 archived lifecycle filtering 缺口。 |
| `tests/services/workspace/test_data_migration.py` | failure-path fixtures | 冲突、partial copy、session transfer、restore/recovery 等迁移约束。 |
| `docs-for-user/workspaces.md` | 用户级 scope contract | 哪些数据 workspace-local、哪些 account-global、迁移与资源分配边界。 |

#### ⭐ 源码精读

**函数 1：`resolve_workspace_scope()`——身份、kind、owner 与物理根一起解析。**

```python
def resolve_workspace_scope(workspace_id: str | None = None) -> WorkspaceScope:
    base = get_account_path_service()
    service = get_content_workspace_service()
    service.assert_available()
    workspace_id = str(workspace_id or "").strip()
    if not workspace_id or workspace_id == service._builtin_id("general"):
        return WorkspaceScope("", base.workspace_root, base.get_workspace_dir())
    binding = service.validate_chat_binding(workspace_id, existing=True)
    row = next(row for row in service._catalog() if row["workspace_id"] == workspace_id)
    if row["kind"] != "workspace":
        raise WorkspaceError("This workspace cannot contain learning data.")
    return WorkspaceScope(workspace_id, base.workspace_root, binding.root, bool(row["archived"]))
```

逻辑摘要：ID 不是权限；仍要验证 catalog owner/kind/root。`ContextVar` 让 async task 和 `to_thread` 继承 admission 时的 immutable scope，UI 后续切换不改正在运行的任务。

**函数 2：`scoped_path_service()`——保存的 scope 也要在 effect 前重验 current root。**

```python
def scoped_path_service(account: PathService) -> PathService:
    scope = _scope.get()
    if scope is None or not scope.workspace_id:
        return account
    if account.workspace_root != scope.account_root:
        raise WorkspaceError("The workspace belongs to a different account context.")
    current = get_content_workspace_service().binding_by_id(scope.workspace_id)
    if current.root != scope.content_root:
        raise WorkspaceError("Workspace storage moved. Reload before continuing.")
    return WorkspacePathService(account, scope)
```

逻辑摘要：既防跨账号继承，又防 workspace 在任务期间被移动后旧任务继续写旧根；这比只在请求入口查一次 path 更接近 effect-time revalidation。

**函数 3：`_narrow_to_turn()`——对话选择只能收窄 workspace ceiling。**

```python
def _narrow_to_turn(resources: WorkspaceResources) -> WorkspaceResources:
    selection = _turn_selection.get()
    if not selection:
        return resources
    data = resources.model_dump()
    for kind, picked in selection.items():
        allowed = data.get(kind)
        data[kind] = picked if allowed is None else [v for v in picked if v in set(allowed)]
    return WorkspaceResources.model_validate(data)
```

逻辑摘要：`None` 是 workspace 继承全部账号可用资源；显式 allowlist 是 ceiling；turn picker 只能做 intersection。MCP/Skill assignment 保存 ID 引用，不保存 secret，也不能扩大管理员 grant。

**函数 4：`migrate_data()`——先留恢复证据，再碰 destination/source。**

```python
def migrate_data(source_id: str, target_id: str, features: list[str], *, session_ids=None) -> dict:
    with data_activity(exclusive=True):
        assert_no_pending_recovery(reject_unreadable=True)
        plan = preview(source_id, target_id, features, session_ids=session_ids)
        if plan["blockers"]:
            raise WorkspaceError(" ".join(plan["blockers"]))
        result = {"status": "preparing", "plan": plan, ...}
        atomic_write_json(journal, result)
        # snapshot SQLite through backup API / files through SHA-256
        result["status"] = "copying"; atomic_write_json(journal, result)
        # journal installed_paths BEFORE copy; verify destination hashes
        result["status"] = "transferring"; atomic_write_json(journal, result)
        # transfer sessions / rebind references
        result["status"] = "committed"; atomic_write_json(journal, result)
        # only now clean source; finally mark completed
```

逻辑摘要：状态用于恢复语义而非进度装饰；`preparing/copying/transferring/committed/completed/recovery_required/cleanup_required` 对应不同可逆边界。source cleanup 发生在 durable `committed` 后。

#### 依赖分析与供应链风险

- Python `>=3.11,<3.15`；核心 graph 很大：OpenAI/Anthropic、HTTP、Pydantic、MCP、LlamaIndex、FAISS、文档解析、FastAPI/WebSocket、PocketBase/Redis、JWT/crypto 等；optional extras 又包含 GraphRAG、LightRAG、Docling、Matrix、Partner channels、Manim。
- Frontend 是 Next.js 16 + React 19，含 Mermaid、PDF.js、ExcelJS、EPUB、DOCX preview、KaTeX 等复杂内容解析面。
- 本机对固定 `web/package-lock.json` 执行 `npm audit --omit=dev --package-lock-only --json`：**14 个 vulnerability nodes：1 critical、5 high、4 moderate、4 low**。其中直接依赖包括 Next、Mermaid、ExcelJS、rehype-katex、remark-math；Next 命中多条 RCE/SSRF/cache/DoS advisories。版本命中不自动证明 DeepTutor 路径可达，但当前 lock 不能称为 clean。
- Public repository advisories API 返回 0；Dependabot endpoint 403，不等于无漏洞。
- GitHub fixed-head check-runs 返回大量重复 workflow runs，其中存在 `Test Summary`、`Web Node Tests`、部分 Python 3.11/3.13 failure；因此不能用其他 success jobs 覆盖 fixed-head CI failure。

#### 本机验证

```bash
cargo # 不适用于本项目；Python workspace 采用隔离 venv。
python3 -m compileall -q deeptutor/services/workspace deeptutor/runtime
# exit 0

PYTHONPATH=. /tmp/deeptutor-testenv/bin/python -m pytest -q \
  tests/services/workspace/test_data_migration.py
# 29 passed（与同批 test_data_scope 首次运行合计 33 passed / 1 blocked-by-missing-dependency）

PYTHONPATH=. /tmp/deeptutor-testenv/bin/python -m pytest -q \
  tests/services/workspace/test_data_scope.py
# 补齐隔离测试依赖 defusedxml 后：5 passed
```

最初用裸系统 Python 运行 workspace glob，collection 因缺 `loguru` 失败；随后 `uv run` 又因项目 extras 跨 Python marker 的 resolver conflict 失败；改用独立 Python 3.11 venv 和定向依赖后获得上述真实结果。`test_content_workspace.py` 仍因完整 app dependency graph 缺 `json_repair` 未执行，明确标 **待核验**，不继续无界补装。

#### 可复用经验

- 当长任务可跨 UI 切换 workspace 时，应优先在 admission 时固定 **workspace ID + account root + content root**，并在最终 path/effect 前重验 current binding，因为“当前选择”是 UI 状态，不是运行任务的 authority；边界是 application scope 不等于 OS sandbox。
- 当 workspace 可分配 Skill/MCP/知识库时，应优先让 workspace policy 成为 ceiling、turn selection 只做 intersection，因为对话层选择不应扩大管理员/账号 grant；边界是外部 MCP 自身权限仍需独立限制。
- 当迁移包含 SQLite、文件、引用和后台任务时，应优先采用 **dependency preview → exclusive lease → verified snapshot → journaled install → commit → cleanup/recovery**，因为 copy 成功和 DB 文件存在都不证明 WAL/引用/跨表一致；边界是外部绕过 lease 的 writer 仍会破坏假设。

#### 30 分钟可尝试实验

为 shared hub 做一个纯 synthetic 的 `scope-bound-migration-receipt` fixture：两份 runtime 临时树、一个 SQLite WAL 数据库、一个 symlink、一个 interrupted-copy fault。验证：active writer 阻断、symlink 拒绝、snapshot hash、commit 前 rollback、commit 后 cleanup resume。只落 `runtime/hermes/`，不迁移真实 shared 数据。

#### 风险边界

- **License**：GitHub API、`pyproject.toml` 与根 LICENSE 均为 Apache-2.0；第三方模型、RAG engine、文档解析器与前端依赖另有许可。
- **维护活跃度**：2026-10-27 有 push，v1.6.15 发布于 2026-10-18，活跃；但 3,875 tracked files、160 个 fixed-head check-runs 与快速 release 节奏增加漂移面。
- **安全风险**：巨大 Python/Node/可选插件/MCP/CLI app surface；npm audit 真实命中 critical/high；content parser、Mermaid/Next、外部 MCP、local runner 都是高权输入面。
- **局限/不适用**：workspace partition 是 application-level organization，官方文档明确 memory/settings/admin resources 可保持全局；best-effort subprocess 不是强隔离。
- **已知 issue**：#2074 表明 archived lifecycle 没进入 navigation reader；这说明“archive 阻止新写入”不自动意味着所有聚合查询已正确过滤。
- **未验证**：完整 Python suite、frontend tests/build、Docker、WebSocket live QA、PocketBase live service、真实 migration crash injection、全部 optional RAG/Partner/MCP paths 均待核验。

#### ⭐ Skill 升格判断

**需二次验证。** 只抽象 scope identity、resource intersection 与 recoverable migration receipt；不迁移 DeepTutor 产品/Skill、账号系统或依赖图。该模式与现有 `path-portability`、`shared-memory-bridge`、governance/verification 能力高度重叠，应先做 POC 和去重。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/scope-bound-migration-receipt-v0/`。
2. Scope schema：`agent`, `layer`, `logical_root`, `resolved_root`, `owner`, `source_revision`, `lifecycle`, `effect_ceiling`；所有路径从 `resolve_shared_root.py` 拼接，不硬编码宿主绝对路径。
3. Shared hub 对应关系：`curated/` 是稳定 truth、`inbox/<agent>/` 是 raw、`runtime/<agent>/` 是可删 projection；resource selection 只能缩窄 agent 的 writes，不允许 runtime 反写 curated。
4. 候选迁移器：只对 synthetic runtime tree 做 `preview.json → snapshot/manifest.json → operation.json → read-back`；默认 dry-run，symlink/special file/active writer/unknown owner 均 blocked。
5. Hermes adapter 负责执行和审计；future-agent 只消费同一 receipt schema。本任务不调用 OpenClaw，也不修改任何 agent 配置、cron 或 secret。
6. 如果 POC 能抓到真实 shared migration regression，再更新现有 path-portability/shared-memory/governance Skill；否则保留 Hermes runtime candidate。

## 经验沉淀

1. 当一份能力跨多个 Agent/harness 发布时，应优先维护 canonical contract、host capability manifest 和可重建 projection，并用 hash/parity fixture 验证，因为手工复制会漂移；边界是 projection 一致仍不证明各宿主运行语义一致。
2. 当 scan/audit 有多个 adapter 或文件目标时，应优先将 finding、coverage、operational failure 与最终 verdict 分开，因为 unreadable/unsupported 不是 clean；边界是 complete coverage 仍只覆盖已建模规则。
3. 当长任务跨 workspace/UI 生命周期运行时，应优先在 admission 固定 scope 并在 effect-time 重验 owner/root/revision，因为当前 UI 选择不能作为持续授权；边界是应用级重验不替代 OS sandbox。
4. 当 workspace/对话选择 Skill、MCP 或知识库时，应优先采用 `account/admin grant ∩ workspace allowlist ∩ turn selection`，因为下层选择只能收窄不能提权；边界是远端服务内部授权仍需另验。
5. 当迁移包含数据库、文件与引用时，应优先执行依赖闭包预览、exclusive lease、SQLite backup/hash snapshot、journaled copy、read-back、commit 后 cleanup，因为 copy/exit 0 不证明一致完成；边界是外部 writer 与跨系统事务仍需额外协调。
6. 当安全扫描返回公开 advisories 为空但本机 lock audit 命中时，应优先保留两面证据并以 lock audit 为当前 artifact 风险输入，因为 repository advisories 不是依赖图证明；边界是版本命中还需 reachability 分析。

## 明日继续

1. 最小动作：创建 `runtime/hermes/github-learning-poc/host-capability-projection-v0/` 的 synthetic fixture，仅验证 canonical Skill 到 Hermes/future-agent projection 的 hash/parity/degraded reason；不安装第三方 Skill。
2. 并行准备 `scope-bound-migration-receipt-v0` 的设计稿，优先复用现有 path-portability/verification 脚本；若只是重复既有契约则停止新增。
3. 继续核验 Impeccable #813 的 release provenance 与 DeepTutor npm critical advisories 的实际 reachable surfaces；无法核验则保持待核验。

## 候选反哺

### Candidate Facts

- [ ] topic: 跨 harness Skill 应拆为 canonical contract、host capability manifest、generated projection 与 parity receipt | evidence: `pbakaus/impeccable@d34c87e...` 的 `skill/`、`docs/HARNESSES.md`、transformers、oracle | 建议: update（优先现有 shared-skill governance） | 安全级别: medium
- [ ] topic: 多 workspace 正确性需要 admission scope pin + effect-time binding revalidation + resource intersection | evidence: `HKUDS/DeepTutor@a31d826...` 的 `context.py`、`resources.py`、`service.py` | 建议: candidate/update | 安全级别: medium
- [ ] topic: 数据迁移 receipt 应区分 preparing/copying/transferring/committed/completed/recovery_required | evidence: DeepTutor `data_migration.py` + 定向 34 tests 通过 | 建议: candidate/update verification workflow | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: host-capability-projection parity | 可复用场景: Hermes/future-agent/shared Skill 分发 | 是否建议 shared: yes（验证后更新既有能力） | 原因: 横切多 agent，但当前仅源码模式，尚未有本地 POC
- [ ] 名称: scope-bound migration receipt | 可复用场景: shared hub 路径迁移/runtime relocation/跨 workspace 搬运 | 是否建议 shared: yes（验证后合并到 path-portability） | 原因: 稳定横切契约；必须避免创建重复 Skill

### Candidate Open Questions

- [ ] 问题: shared hub 当前 bridge/bootstrap/migration 是否有 source scope、destination scope、commit marker 与 recovery receipt 的统一 schema？ | reason: gap/adaptation | priority: high
- [ ] 问题: Hermes project-local Skill trust、external_dirs 与 active profile 在 projection verifier 中应如何作为可机读 capability？ | reason: adaptation | priority: medium
- [ ] 问题: Impeccable release checksum 的 trust root 是否能独立绑定 tag source 与构建 provenance？ | reason: conflict/gap（issue #813） | priority: high
- [ ] 问题: DeepTutor fixed lock 的 Next/Mermaid/DOMPurify advisories 哪些路径实际可由不可信学习内容触达？ | reason: gap | priority: high

### 不应自动落地

- 不安装 Impeccable/DeepTutor，不运行其 hook、browser extension、provider、MCP、unknown CLI app 或 release binary。
- 不修改 Hermes/OpenClaw/future-agent 配置、模型、provider、cron、secret；本次明确未调用 OpenClaw。
- 不把候选直接写入 curated active fact，不复制第三方规则、Skill 或大段源码到 shared。
- 不因 87/34/5 个定向测试通过而宣称完整项目安全；不因 public advisories 为 0 而宣称无漏洞。
