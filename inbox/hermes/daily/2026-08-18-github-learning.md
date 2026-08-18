# 2026-08-18 GitHub 热门项目学习日报

> 执行器：Hermes。当前 OpenClaw runtime 不存在；本次未调用、启动、模拟或写入 OpenClaw。
> 研究窗口：2026-08-18 07:30-07:38（UTC+08:00；GitHub API 返回 UTC 时间）。Trending 由 `curl` 真实抓取；stars/license/updated/pushed、release/issues/tags 由 GitHub REST API 读取；源码由 `git clone --depth 1` 固定。
> 固定源码：`akitaonrails/ai-memory@7f052990991aa541022a4bd015b58d1f5a9e8bf5`（恰为 tag `v1.28.0`）；`AlexsJones/llmfit@acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe`（比 tag `v1.1.10` ahead 1 commit，该 commit 只更新 GitHub Action）。
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-18/`。Trending HTML 为 582,715 bytes，SHA-256 `c1bc4629253fcb462164dd984e680117de93c07516db91d1dfb352d985ab2cc9`。
> 数据边界：stars/forks/updated/pushed 是查询时动态值；GitHub API 的 repository license 只覆盖仓库级识别，不覆盖依赖、模型、数据、release asset。当前宿主无 Cargo/Rustc/Rustup，源码编译与 Rust tests 明确标为待核验；为避免用 README 代替运行，本次另下载、校验并执行官方 release 二进制。

## 今日结论

**今天的主线是“长期事实与实时估计都必须分层”：ai-memory 用 Markdown 真相源 + SQLite 派生索引 + typed sanitizer + bounded retrieval 把历史证据变成可恢复记忆；llmfit 用硬件事实 + 估计 basis + 本机/同硬件 measured calibration 把启发式建议变成可核验输出。对 Hermes/shared hub 最有价值的不是直接接入两个产品，而是补强 `canonical truth / derived projection / coverage / estimate provenance / live readback` 契约。**

## 研究边界与真实验证

- **发现源**：`https://github.com/trending?since=daily` 真实 HTML 解析出 11 个候选：`harry0703/MoneyPrinterTurbo`、`usestrix/strix`、`nautechsystems/nautilus_trader`、`akitaonrails/ai-memory`、`mukul975/Anthropic-Cybersecurity-Skills`、`AlexsJones/llmfit`、`santifer/career-ops`、`jundot/omlx`、`immich-app/immich`、`cordiverse/cordis`、`agalwood/Motrix`。Trending 只负责发现；表中数值全部由 Repository API 二次核验。
- **筛选**：Cordis 昨日已深读；Immich/MoneyPrinterTurbo/Strix 体量与运行依赖超出当天安全验证预算；Motrix 的 GitHub license 为 `NOASSERTION`；skills 清单不适合做今日 core source 深读。最终选择直接对应 shared memory 与 Hermes 本地模型决策的 ai-memory、llmfit。
- **GitHub API 限流事实**：认证 `gh api search/repositories` 因脚本误用了 `--paginate`，在输出大量结果后真实触发 403 rate limit；随后对候选元数据使用非认证 GitHub Repository API 并将原始 JSON保存到 evidence。报告不使用被截断搜索结果作排名结论。
- **ai-memory release 实测**：下载 `v1.28.0` Linux x86_64 官方 asset，SHA-256 校验为 `f564f08d8d91035d8000341b72287b7671cc77b4848f214cd78dceb86898e15f`；`ai-memory 1.28.0`。在隔离 `/tmp` data dir 成功 `init`，启动 loopback HTTP server；初始 `/admin/status` 为 0 sessions/0 observations，POST 一个 Hermes `user-prompt` hook 返回 `queued`，1 秒后 status 为 **1 session / 1 observation / 1 observations_fts row**。canary 原文含 `MY_INTERNAL_API_KEY=aaaaaaaaaaaa`，对隔离 data dir 做 byte scan 未发现 raw canary，证明该 fixture 的 sanitizer 路径真实生效。未开启 LLM/embedder、未接真实 Hermes hook、未触碰 `~/.hermes`。
- **ai-memory CLI 边界**：在 server 未启动时 `status` 真实返回 connection refused，而不是假健康；启动日志明确 `LLM/embedding disabled`、FTS5+entity+graph 可用。本机无 Cargo，源码 tests/compile 待核验。
- **llmfit release 实测**：下载 `v1.1.10` Linux x86_64 GNU 官方 asset，SHA-256 `c5d3f119160c7fe362d43847cf58b918e3b0f37a7f7d19ec15450581a7bbdb8c` 与 sidecar 一致；`llmfit 1.1.10`。真实运行 `doctor` 与 `recommend --json`：检测到 WSL **5.79 GiB total / 3.96 GiB available / 8 cores / Intel i5-10400 / no GPU / CpuX86**；recommend 返回 5 个模型，全部使用 `estimate_basis.method=cpu_constant`、`efficiency=0.55`、`local_calibration=null`。这只是估计，不是实际推理 benchmark。
- **安全边界**：不自动修改 Hermes config/model/provider/auth/env/cron/skills；不安装 ai-memory hook/MCP；不下载或运行模型；不提交 llmfit benchmark；不把 candidate 直接写入 `curated/memory/`。

## 项目速览

下表来自 2026-08-18 07:31-07:38（UTC+08:00）的真实 `GET /repos/{owner}/{repo}` JSON。Stars 会变化；License 是 GitHub Repository API 返回的 SPDX 标识。

| 项目 | Stars | Forks | Language | License | Updated / Pushed（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [immich-app/immich](https://github.com/immich-app/immich) | 111,131 | 6,574 | TypeScript | AGPL-3.0 | 2026-08-17T23:30:50Z / 2026-08-17T23:14:41Z | 高热大型图库，AGPL/媒体/部署面重 |
| [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 105,944 | 16,104 | Python | MIT | 2026-08-17T23:31:03Z / 2026-08-17T11:12:12Z | 多媒体生成，外部服务与内容风险较高 |
| [santifer/career-ops](https://github.com/santifer/career-ops) | 64,596 | 12,650 | JavaScript | MIT | 2026-08-17T23:31:42Z / 2026-08-17T22:24:43Z | 高热，但领域模式与 shared hub 较远 |
| [usestrix/strix](https://github.com/usestrix/strix) | 54,115 | 5,793 | Python | Apache-2.0 | 2026-08-17T23:31:10Z / 2026-08-17T20:55:28Z | 安全自动化，高权攻击面不进今日运行 lane |
| [agalwood/Motrix](https://github.com/agalwood/Motrix) | 53,046 | 4,927 | TypeScript | NOASSERTION | 2026-08-17T23:25:34Z / 2026-08-17T22:49:49Z | License 待核验，不迁移源码 |
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | 32,234 | 1,998 | Rust | MIT | 2026-08-17T23:26:49Z / 2026-08-17T07:35:58Z | **深读：事实→估计→测量校准→provenance** |
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | 28,391 | 3,447 | Python | Apache-2.0 | 2026-08-17T23:30:47Z / 2026-08-08T14:55:19Z | skills 集合，需逐 skill authority review |
| [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | 25,896 | 3,372 | Rust | LGPL-3.0 | 2026-08-17T23:31:48Z / 2026-08-17T21:55:40Z | 金融交易核心，高风险且领域较远 |
| [jundot/omlx](https://github.com/jundot/omlx) | 18,974 | 1,644 | Python | Apache-2.0 | 2026-08-17T23:26:59Z / 2026-08-17T18:22:23Z | 本地模型候选，运行/硬件面较大 |
| [cordiverse/cordis](https://github.com/cordiverse/cordis) | 5,558 | 295 | TypeScript | MIT | 2026-08-17T23:29:40Z / 2026-08-13T13:48:22Z | 昨日已深读，不重复 |
| [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) | 2,015 | 192 | Rust | MIT | 2026-08-17T23:29:08Z / 2026-08-17T02:39:12Z | **深读：可审计真相源、派生检索、hook 安全边界** |

### 筛选说明

- ai-memory stars 低于大多数候选，但它在 Trending 当日出现，且主题与 shared hub v2 直接重合；价值在架构可比性，不在绝对热度。
- llmfit 的 release、docs、source、issues 与可直接执行的 read-only binary 形成完整验证链；尤其适合检验“估计值如何携带 basis、如何被 measured data 校准”。
- 两仓 Repository API 均返回 MIT；ai-memory 的 Cargo transitive dependencies、llmfit 的 Cargo/npm/Python/Nix 依赖与模型 license 必须独立审计。公开 repository security advisories endpoint 两仓均返回空数组；这**不证明无漏洞**。

## 深读项目

### 项目 1：akitaonrails/ai-memory

- **URL**：https://github.com/akitaonrails/ai-memory
- **Stars / Forks / Language / License（GitHub API）**：**2,015 / 192 / Rust / MIT**。
- **查询时 updated / pushed / open issues**：2026-08-17T23:29:08Z / 2026-08-17T02:39:12Z / 6。
- **固定源码版本**：`7f052990991aa541022a4bd015b58d1f5a9e8bf5`，commit `release: v1.28.0`；该 HEAD 等于 tag `v1.28.0`。
- **release / issues / PR 证据**：latest release `v1.28.0` 发布于 2026-08-17T02:52:48Z，提供 Linux/macOS/Windows assets 与 checksums。Open issue #407 报告 standalone Docker `upgrade` 不能安全重建手工容器，且升级后的非 loopback 无 auth fail-closed 造成 restart loop；#406 追踪 Pi/OMP config-home path 是否误装；#387 要求按 session UUID 跨所有 retained layers 强删除，关联 PR #399 仍 open。PR #408 扩充 token sanitizer 仍 open，故当前 release 不包含其新 pattern。

#### 一句话判断：为什么值得学

ai-memory 值得学的是把**人类可审计 Markdown 真相、可重建 SQLite projection、自动但有界的 hook capture、typed sanitizer、四流检索和显式 handoff**拆开；更值得警惕的是，多副本删除、Docker 升级、session routing 与“清洗即安全”都仍有真实边界。

#### 解决的问题：替代了什么旧做法

1. 替代每个 Agent 手工写 note：lifecycle hooks 自动采集 bounded observations。
2. 替代把 opaque DB 当唯一事实：Markdown wiki + git 是 source of truth，SQLite 是 derived index。
3. 替代纯向量召回：FTS5、entity、graph、optional vector 用 RRF 合并，再做 bounded authority adjustment。
4. 替代历史 prose 直接变指令：检索内容明确标记为 untrusted historical evidence。
5. 替代 session 结束后无 baton：typed handoff 携带 summary/open questions/files/next steps。
6. 替代 hook 网络阻塞：single hook 用 try-acquire + spawn 后返回 202，拥塞返回 429；native spool 用 idempotency key 重放。
7. 但它没有自动解决 complete erasure：issue #387 明确 page 删除后，observations、handoff、backup、git checkpoint、spool 仍可保留内容。

#### 架构 / 实现与数据流

```text
Agent lifecycle hook / generated extension
  -> client capture policy (recognized file tools only)
  -> bounded body + local spool/idempotency key
  -> POST /hook
  -> raw assistant backstop / subagent policy / semaphore / source rate limit
  -> typed Sanitized<NewObservation>
  -> single-writer SQLite actor
       |- sessions / observations / FTS / handoffs / audit
       `- SessionEnd generation watermark
  -> Wiki mutation layer
       |- atomic markdown write
       |- git checkpoint
       `- watcher/reindex reconciliation

memory_query
  FTS5 rank + entity rank + optional vector rank
       -> graph neighbors from seed set
       -> RRF(k=60)
       -> bounded authority multiplier
       -> deterministic path tie-break
       -> result + optional provenance
```

核心是把 canonical durable knowledge、operational observations、derived indexes、portable transcript ledger 分开。它允许 SQLite 重建，却也承认 filesystem + DB 无真正跨资源事务，只能 best-effort rollback + reindex convergence。

#### Repo tree 摘要

固定 commit 共 **560 tracked files**，其中 `crates/` 294；仓库包含 committed `Cargo.lock`：

```text
ai-memory/
├── crates/
│   ├── ai-memory-core/        # domain ID/type、Sanitized boundary
│   ├── ai-memory-store/       # SQLite writer actor、reader、RRF、decay
│   ├── ai-memory-wiki/        # markdown、atomic write、git、watcher
│   ├── ai-memory-hooks/       # hook schema/router/capture policy
│   ├── ai-memory-mcp/         # MCP tool handlers / auth / scope
│   ├── ai-memory-llm/         # typed provider/auth traits
│   ├── ai-memory-consolidate/ # summarize/lint/forget/auto-improve
│   ├── ai-memory-workstream/  # native transcript read-only adapters
│   ├── ai-memory-web/         # read-only browser/API
│   └── ai-memory-cli/         # single binary / admin commands
├── hooks/                     # Claude/Codex/Kimi/Grok/... shell & PowerShell hooks
├── docs/                      # architecture/security/deploy/workstream specs
├── packaging/ / docker/       # systemd/AUR/container packaging
├── evals/                     # recall fixtures / A-B harness
├── Cargo.toml / Cargo.lock    # Rust 1.95, resolver 3, workspace deps
└── README.md / LICENSE / AGENTS.md
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/ai-memory-core/src/sanitize.rs` | typed privacy boundary | regex compile-once；scrub title/body；UTF-8 bounded body；`Sanitized<T>` wrapper |
| `crates/ai-memory-hooks/src/router.rs` | hook ingress | assistant field backstop、capture drop、subagent drop、try semaphore、per-source limit、202/429 |
| `crates/ai-memory-store/src/reader.rs` | retrieval | FTS/entity/vector seeds、graph neighbors、RRF k=60、authority adjustment、stable tie-break |
| `crates/ai-memory-store/src/writer.rs` | write serialization | one connection/actor owns SQLite mutations，避免 `database is locked` |
| `crates/ai-memory-wiki/src/lib.rs` | canonical file mutation | atomic files、git commit、store reconciliation |
| `crates/ai-memory-hooks/src/native.rs` | client spool | keyed retry、bounded drain 与 delivery |
| `crates/ai-memory-consolidate/src/auto_improve.rs` | learning review | proposal/validation/pending approval，不应绕过 canonical write path |
| `docs/ARCHITECTURE.md` | operational contract | source-of-truth、dataflow、schema、cross-cutting invariants |

#### 源码精读

**代码块 1：`Sanitized<NewObservation>::new` 把 redaction 与 durable cap 固化在类型构造边界**  
来源：[`crates/ai-memory-core/src/sanitize.rs#L196-L204`](https://github.com/akitaonrails/ai-memory/blob/7f052990991aa541022a4bd015b58d1f5a9e8bf5/crates/ai-memory-core/src/sanitize.rs#L196-L204)

```rust
impl Sanitized<NewObservation> {
    #[must_use]
    pub fn new(mut obs: NewObservation, sanitizer: &Sanitizer) -> Self {
        obs.title = sanitizer.scrub(&obs.title);
        obs.body = truncate_utf8_bytes(
            &sanitizer.scrub(&obs.body),
            OBSERVATION_BODY_MAX_BYTES,
        );
        Self(obs)
    }
}
```

逻辑摘要：store API 可以要求 `Sanitized<NewObservation>`，减少调用方忘记 scrub 的路径；cap 在 redaction 后执行并保证 UTF-8 边界。本机 hook canary 未在 data dir byte scan 中出现，支持该具体 fixture。边界是 regex DLP 只能覆盖已知 pattern，allowlist/alias/encoded secrets 仍可能漏过；PR #408 正说明 pattern 集合持续变化。

**代码块 2：单条 hook 对 capture、容量和 source rate 做 fail-fast，再异步处理**  
来源：[`crates/ai-memory-hooks/src/router.rs#L584-L646`](https://github.com/akitaonrails/ai-memory/blob/7f052990991aa541022a4bd015b58d1f5a9e8bf5/crates/ai-memory-hooks/src/router.rs#L584-L646)

```rust
async fn handle_hook(/* ... */, Json(mut body): Json<serde_json::Value>) -> impl IntoResponse {
    strip_assistant_message_raw(&mut body);
    let mut env = HookEnvelope::from_query_and_body(query, body);
    apply_assistant_backstop(&mut env, state.capture_assistant_enabled);
    let Some(env) = inspect_capture_envelope(env) else {
        return (StatusCode::ACCEPTED, "capture policy dropped");
    };
    if should_drop_subagent(&state, &env).await {
        return (StatusCode::ACCEPTED, "subagent capture dropped");
    }
    let Ok(permit) = state.ingest_semaphore.clone().try_acquire_owned() else {
        return (StatusCode::TOO_MANY_REQUESTS, "hook queue full");
    };
    if !state.ingest_rate.lock().await.try_take(&rate_key, Instant::now()) {
        return (StatusCode::TOO_MANY_REQUESTS, "hook source rate limited");
    }
    tokio::spawn(async move { let _permit = permit; process_envelope(/* ... */).await; });
    (StatusCode::ACCEPTED, "queued")
}
```

逻辑摘要：policy drop 返回 202，表示客户端可清 spool；真实过载返回 429，要求重试。返回 `queued` 不是 durable receipt，真正可靠性依赖 native spool/idempotency completion marker；普通 curl client 若收到 202 后 server crash，不能凭 202 证明所有下游 effects 已完成。

**代码块 3：检索不是把不同 score 直接相加，而是按 rank 做 RRF**  
来源：[`crates/ai-memory-store/src/reader.rs#L3648-L3710`](https://github.com/akitaonrails/ai-memory/blob/7f052990991aa541022a4bd015b58d1f5a9e8bf5/crates/ai-memory-store/src/reader.rs#L3648-L3710)

```rust
// score(d) = Σ 1/(k + rank_i(d))
let k = 60.0_f64;
for (rank, h) in fts_hits.iter().enumerate() {
    let contrib = 1.0 / (k + (rank + 1) as f64);
    fused.entry(h.id).or_insert_with(/* ... */).score += contrib;
}
for (rank, (id, path, cosine)) in vec_hits.iter().enumerate() {
    let contrib = 1.0 / (k + (rank + 1) as f64);
    fused.entry(*id).or_insert_with(/* ... */).score += contrib;
}
for (rank, e) in entity_hits.iter().enumerate() {
    let contrib = 1.0 / (k + (rank + 1) as f64);
    fused.entry(e.hit.id).or_insert_with(/* ... */).score += contrib;
}
```

逻辑摘要：FTS BM25、cosine、entity weight 的尺度不同，rank fusion 避免直接混加不可比 raw scores；graph 作为第四流加入。边界是 RRF k、candidate limit 与 authority multiplier 都是 policy；必须保留 scorer/config version 与 explain provenance，不能把排序当事实正确性。

**代码块 4：最终排序使用 authority adjustment 和 deterministic path tie-break**  
来源：[`crates/ai-memory-store/src/reader.rs#L3751-L3779`](https://github.com/akitaonrails/ai-memory/blob/7f052990991aa541022a4bd015b58d1f5a9e8bf5/crates/ai-memory-store/src/reader.rs#L3751-L3779)

```rust
for (hit, explain) in &mut out {
    if let Some(authority) = authorities.get(&hit.id) {
        hit.rank = authority.adjust_rank(hit.rank);
        if let Some(details) = explain {
            details.authority = Some(authority.factor);
        }
    }
}
out.sort_by(|a, b| {
    a.0.rank
        .partial_cmp(&b.0.rank)
        .unwrap_or(Ordering::Equal)
        .then_with(|| a.0.path.as_str().cmp(b.0.path.as_str()))
});
```

逻辑摘要：canonical/rule/decision 等仅是 bounded ranking signal，不提升为指令 authority；相同分数按 path 确定性收敛。shared hub 可借鉴的是 projection explainability，而不是把 path/tier 当绝对真伪标签。

#### 依赖分析与供应链风险

- workspace Rust 1.95 / edition 2024 / resolver 3，9 个 shipped crates + eval；committed `Cargo.lock`。
- 核心直接依赖：`tokio`、`rusqlite` bundled+backup、`refinery`、`rmcp`、`axum`/tower、`git2` vendored-libgit2、`notify`、`reqwest` rustls、`regex`、`sysinfo`、`secrecy`、`schemars`。
- native surface 包含 SQLite、libgit2、TLS、filesystem watcher、tar/gzip、process inspection；单 binary 不等于小供应链。
- release asset 有独立 SHA-256，本机真实通过；但 checksum 与 asset 同在同一 GitHub release authority，不能抵御上游账号/发布流水线同时被攻破。未核验签名或 SLSA provenance。
- 当前宿主无 Cargo，无法执行 `cargo test --workspace --locked`、`cargo deny`、`cargo audit`；源码编译和 transitive advisory 状态**待核验**。公开 repository advisories 空数组不能替代 lockfile audit。
- hooks/installer 会写 Agent 配置与执行 shell/PowerShell；任何接入都必须逐 client dry-run、backup、scope/uninstall review，不能因 MIT 或 checksum 自动信任。

#### README / docs / release / issues / source / 运行交叉核验

- README 宣称 Markdown-in-git 是真相、SQLite 是 derived index；`ARCHITECTURE.md`、crate layout 与 status 输出一致。
- release asset version 与 tag/workspace version 均为 1.28.0；HEAD 与 tag 完全一致，不存在 main/tag drift。
- 本机 loopback server status、hook queue、session/observation/FTS count 变化与 dataflow 一致；未验证 LLM consolidation、handoff、watcher、backup/restore、multi-user 或 managed workstream。
- issue #407 与 `serve --help` 的 non-loopback guard一致：CLI明确要求 auth 或 dangerous override；但 upgrade 如何重建 standalone container 尚未本机复现，属于上游报告。
- issue #387 说明强删除必须跨 wiki/DB/log/git/raw/spool/backup；PR #399 仍 open，不能声称 v1.28.0 已满足“忘记此 session”。
- README 把 Hermes 标为 Community，明确无 first-party installer且 Hermes session-start stdout 不可用；因此本次不安装第三方 Hermes plugin。

#### 可复用经验

- 当同一知识同时存在 canonical document、DB index、cache、ledger 与 projection 时，应优先明确唯一 truth source、每个 derived layer 的重建/删除/coverage contract，因为“删页面”或“重建索引”不代表全层语义一致；边界是 filesystem+DB仍无跨资源原子事务。
- 当 hook 位于 Agent 热路径时，应优先 client-side bounded spool + idempotency key + server backpressure + completion marker，因为 202 queued 只证明接收而非 durable downstream completion；边界是 at-least-once effect 仍需幂等或 reconcile。
- 当检索混合 BM25、cosine、entity 与 graph 时，应优先按 rank fusion并输出 per-stream provenance，因为 raw score 尺度不可直接比较；边界是 rank policy 不能提升历史文本的指令 authority。
- 当 sanitizer 声称保护 secret 时，应优先在 capture 前最小化、typed boundary、server backstop 与 canary tests并用，因为 regex redaction 不能证明未知/编码 secret 不泄漏；边界是最安全的数据仍是未采集的数据。
- 当实现“忘记某 session”时，应优先先做 retained-layer inventory 和 exact immutable session ID scope，再输出 per-layer deletion receipt，因为 wiki、FTS、raw observation、git、backup、spool 都可能各自保留；边界是已外部复制的数据无法由本地 purge 撤回。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/canonical-derived-memory-receipt/` 做纯 Python 离线 fixture，不安装 ai-memory：

1. canonical markdown、derived JSON index、raw inbox、runtime cache 四层各写同一 canary ID。
2. 定义 `LayerReceipt{role, source_revision, attempted, status, coverage, artifact_hash}`。
3. 只删 canonical 时 overall 必须为 `partial`，不能为 `forgotten`。
4. derived hash 不匹配时必须 `stale_projection`，允许从 canonical 重建；canonical 不存在时禁止从 cache 反升格。
5. fixture 覆盖 crash-after-file-before-index、duplicate hook、missing completion marker、exact-ID purge 与 backup-out-of-scope。

#### 风险边界

- **License**：Repository/License API、Cargo workspace 与根 LICENSE 为 MIT；transitive crates、containers、hook dependencies、第三方 plugins分别审查。
- **维护活跃度**：pushed 2026-08-17；连续多个 releases，v1.28.0 当日发布；高频发布也意味着 schema/client matrix/upgrade 行为快速漂移。
- **安全风险**：自动采集 prompt/tool 生命周期可接触源码、路径和 secret；regex sanitizer不完整；remote HTTP bearer需TLS；multi-user没有 per-page RBAC；hooks/installers是配置与执行 authority surface。
- **正确性风险**：202只是queued；filesystem+SQLite无真实跨资源事务；at-least-once下游 effect 可重复；unknown client events会归一为`other`；static MCP client不能自动传真实session ID。
- **删除/合规风险**：#387 强删除仍在进行；git、backup、spool与外部复制使“删除”必须定义覆盖范围。
- **升级风险**：#407 报告 standalone Docker升级可导致服务停机/迁移失败；不能自动执行 upgrade。
- **测试边界**：release binary smoke真实通过；源码 compile/test/cargo audit 因无工具链待核验；未跑真实 Hermes plugin、LLM、embedder、multi-machine、restore或load test。
- **不适用场景**：把未信任多租户数据当RBAC隔离；要求强删除外部备份；把检索结果视为当前指令；把Regex DLP当完整secret防护。
- **不能自动执行**：不安装MCP/hooks/plugin，不写`~/.hermes`，不导入shared历史，不启动长期server，不配置token/provider。

#### Skill 升格判断

**需二次验证**；`canonical-derived memory receipt` 值得抽象，ai-memory 产品与 hook installer 暂不沉淀。

- **可迁移候选**：truth/derived分层、projection stale detection、rank provenance、capture-before-minimize、retained-layer purge receipt。
- **需二次验证**：先完成离线 fixture，并与现有 `shared-memory-bridge`、governance、path-portability、completion/receipt、OpenHuman localization 去重。
- **暂不沉淀**：不复制 ai-memory Rust 源码、hooks、installer、MCP tool surface 或 retention公式到 shared skill。
- **升格结论**：优先补充既有 shared-memory/governance 契约；今日仅写 Hermes raw candidate，不创建新 shared skill，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/canonical-derived-memory-receipt/{schema.json,fixtures/,checker.py,test_contract.py,README.md}`。
2. **shared truth**：继续保持 `curated/memory/` 为唯一跨 Agent 真相，`inbox/<agent>/daily/` 为 raw，`runtime/<agent>/` 为 derived/bulk；禁止 cache 或历史 retrieval 反写 curated。
3. **bridge verification**：未来给 `scripts/verify_bridge.py` sidecar receipt 增加 `canonical_target/resolved_target/source_hash/projection_hash/stale/coverage`，先 dry-run，不改生产 bridge。
4. **governance**：候选事实仍经评分、证据、去重、脱敏、人工/总控审查；不采用 ai-memory 默认 auto-approve 策略替换本地规则。
5. **Hermes adapter**：若未来评估 ai-memory，只允许先做本地 loopback、临时 profile、read-only inventory；第三方 community plugin单独审计，明确 uninstall/secret/session attribution，再由用户批准。
6. **OpenClaw 边界**：当前不存在且禁止调用；未来仅消费 agent-neutral layer receipt，不假设其 plugin/hook/session stdout 与 Hermes 相同。

### 项目 2：AlexsJones/llmfit

- **URL**：https://github.com/AlexsJones/llmfit
- **Stars / Forks / Language / License（GitHub API）**：**32,234 / 1,998 / Rust / MIT**。
- **查询时 updated / pushed / open issues**：2026-08-17T23:26:49Z / 2026-08-17T07:35:58Z / 63。
- **固定源码版本**：`acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe`，commit `chore(deps): bump actions/setup-python from 6 to 7 (#824)`；比 release tag `v1.1.10@b0875c2...` ahead 1 commit。
- **release / issues / PR 证据**：latest release `v1.1.10` 发布于 2026-08-17T07:12:24Z；新增 RamaLama discovery、Qwen3.8 family，修复 Ollama family installed marker 与 MLX mapping。Open issue #887 来自 v1.1.9 的 Qwen3.8缺失，release notes显示 v1.1.10已加入，但本机没有模型/provider，未做用户原场景E2E。#791 报 GGUF被同时识别为MLX；#869指出两个 MLX quant suffix stripper覆盖分裂，open PR #895拟统一，故当前 HEAD 仍有重复实现。

#### 一句话判断：为什么值得学

llmfit 值得学的不是“一条模型推荐命令”，而是把**硬件探测事实、运行路径、动态量化、估计公式、估计 basis、本机/同硬件实测校准和 read-only machine output**放在同一 core；更值得警惕的是，模型目录、provider 名称归一化与 heuristic 会快速过时或分叉。

#### 解决的问题：替代了什么旧做法

1. 替代凭模型参数或显存拍脑袋：检测 RAM/CPU/GPU/backend，并区分 unified/discrete/multi-GPU。
2. 替代固定 Q4 假设：按 runtime quant hierarchy 选最高质量且能放入预算的 quant。
3. 替代“fit=true”单布尔：FitLevel 与 RunMode正交，另输出 memory required/available/utilization/usable context。
4. 替代无 provenance 的 tok/s：`EstimateBasis`披露 method、bandwidth、efficiency、context、local calibration。
5. 替代同一算法多处复制：`plan.rs` 委托 `fit::estimate_tps`；源码注释记录旧重复实现曾漏 MoE 修复并低估约4倍。
6. 替代只信启发式：本机 bench、community same-hardware、preset measured data 按优先级覆盖/校准估计。
7. 但它没有消除数据漂移：catalog embedded在 binary；更新靠新 release，provider normalized names还有 open divergence bug。

#### 架构 / 实现与数据流

```text
SystemSpecs::detect()
  sysinfo RAM/CPU
  + NVIDIA/AMD/Intel/Apple/Ascend/Vulkan probes
  -> discrete/unified/multi-GPU normalization

ModelDatabase::new()
  embedded HF / ONNX / Docker catalogs
  + custom models / update cache
  -> backend-compatible models

build_model_fits()
  -> ModelFit::analyze_with_forced_runtime()
       |- execution path (GPU/MoE/CPU offload/CPU/TP)
       |- runtime-specific best quant under memory budget
       |- fit level + usable context
       |- estimate_tps single source of truth
       `- score components
  -> measured sources priority:
       local bench > same-hardware community > measured preset
  -> median calibration factor [0.05, 3.0]
  -> CLI/TUI/Web/MCP/Desktop projections
```

关键不是“预测一定准”，而是让每个预测携带假设和验证命令，并允许真实 measured data逐步替代估计。

#### Repo tree 摘要

固定 commit 共 **218 tracked files**；`llmfit-core/` 85，`llmfit-tui/` 15；存在 Cargo/npm/uv/Nix locks：

```text
llmfit/
├── llmfit-core/
│   ├── src/hardware.rs    # RAM/CPU/GPU/backend探测
│   ├── src/models.rs      # model schema/catalog/quant/memory
│   ├── src/fit.rs         # path/fit/quant/TPS/score核心
│   ├── src/analysis.rs    # all-model flow + measured calibration
│   ├── src/bench*.rs      # live bench/community/preset
│   ├── src/providers.rs   # Ollama/MLX/llama.cpp/... detection
│   └── data/              # embedded model/benchmark/community JSON
├── llmfit-tui/            # CLI/TUI/Web/API/MCP main binary
├── llmfit-desktop/        # Tauri desktop
├── llmfit-web/            # React/Vite dashboard + package-lock
├── llmfit-python/         # binary wrapper + uv.lock
├── scripts/               # model scrape/verify/update
├── skills/llmfit-advisor/ # repo-shipped advisor skill
├── docs/                  # formulas/providers/benchmark/OpenClaw docs
├── Cargo.toml / Cargo.lock / flake.lock
└── README.md / LICENSE / AGENTS.md
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `llmfit-core/src/hardware.rs` | hardware truth | 多 vendor probe、dedup、unified/discrete、VRAM sum、backend |
| `llmfit-core/src/models.rs` | model facts | model metadata、quant hierarchy、memory/KV estimates、MoE fields |
| `llmfit-core/src/fit.rs` | decision core | RunMode/FitLevel、dynamic quant、TPS basis、usable context、score |
| `llmfit-core/src/analysis.rs` | full pipeline | provider compatibility、installed mark、measured source priority、calibration |
| `llmfit-core/src/providers.rs` | runtime detection | model/tag normalization；当前MLX suffix逻辑重复 |
| `llmfit-core/src/bench.rs` | active measurement | live provider bench、tok/s与TTFT、target discovery |
| `llmfit-tui/src/mcp_server.rs` | Agent interface | hardware/model/plan tools返回JSON |
| `docs/how-it-works.md` | intended model | detection、scoring、bandwidth公式、fit levels |
| `docs/benchmarking.md` | estimate→measure loop | 3 passes、local-first、optional PR sharing |

#### 源码精读

**代码块 1：`SystemSpecs::detect()` 将事实采集与路径 normalization 集中**  
来源：[`llmfit-core/src/hardware.rs#L72-L156`](https://github.com/AlexsJones/llmfit/blob/acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe/llmfit-core/src/hardware.rs#L72-L156)

```rust
pub fn detect() -> Self {
    let mut sys = System::new_all();
    sys.refresh_all();
    let total_ram_gb = sys.total_memory() as f64 / 1024_f64.powi(3);
    let available_ram_gb = /* sysinfo or platform fallback */;
    let cpu_name = Self::detect_cpu_name(&sys);
    let gpus = Self::detect_all_gpus(total_ram_gb, &cpu_name);
    let primary = gpus.first();
    let total_gpu_vram_gb = {
        let sum: f64 = gpus.iter()
            .filter_map(|g| g.vram_gb.map(|v| v * g.count as f64))
            .sum();
        (sum > 0.0).then_some(sum)
    };
    SystemSpecs { /* primary display + aggregate fit pool + backend */ }
}
```

逻辑摘要：primary GPU 用于显示/带宽 identity，总 VRAM 用于 fit pool；vendor-specific probes不是互斥 cascade。边界是聚合 VRAM 只证明容量总和，实际 runtime 是否支持 mixed GPU/tensor split仍取决于 backend/topology；本机无GPU，只验证了CPU fallback。

**代码块 2：`ModelFit::analyze_inner()`先选运行路径，再在对应预算内选 quant**  
来源：[`llmfit-core/src/fit.rs#L306-L395`](https://github.com/AlexsJones/llmfit/blob/acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe/llmfit-core/src/fit.rs#L306-L395)

```rust
fn analyze_inner(
    model: &LlmModel,
    system: &SystemSpecs,
    context_limit: Option<u32>,
    force_runtime: Option<InferenceRuntime>,
    config: Option<CalcConfig>,
) -> Self {
    let config = config.unwrap_or_default();
    let estimation_ctx = context_limit
        .unwrap_or(model.context_length.min(DEFAULT_ESTIMATION_CTX))
        .min(model.context_length);
    let runtime = if let Some(forced) = force_runtime { forced }
        else if system.cluster_mode { InferenceRuntime::Vllm }
        else if model.is_prequantized() { InferenceRuntime::Vllm }
        else if system.backend == GpuBackend::Metal && system.unified_memory { InferenceRuntime::Mlx }
        else { InferenceRuntime::LlamaCpp };
    let choose_quant = |budget| {
        best_quant_for_runtime_budget(model, runtime, budget, estimation_ctx)
    };
    // then choose GPU / MoE-offload / CPU-offload / CPU / tensor-parallel path
}
```

逻辑摘要：context cap避免用模型宣传的超长窗口夸大KV cache；runtime决定 quant hierarchy。边界是默认 cap 与 runtime policy是版本化 heuristic，用户场景若需要完整 context必须显式 override并检查`usable_context`。

**代码块 3：`estimate_tps` 是共享 single source，且输出 basis**  
来源：[`llmfit-core/src/fit.rs#L1168-L1223`](https://github.com/AlexsJones/llmfit/blob/acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe/llmfit-core/src/fit.rs#L1168-L1223)

```rust
pub(crate) fn estimate_tps(
    model: &LlmModel,
    quant: &str,
    system: &SystemSpecs,
    run_mode: RunMode,
    runtime: InferenceRuntime,
    config: &CalcConfig,
) -> f64 {
    let params = model.active_parameters
        .filter(|_| model.is_moe)
        .map(|p| p as f64 / 1_000_000_000.0)
        .unwrap_or_else(|| model.params_b())
        .max(0.1);
    if run_mode != RunMode::CpuOnly
        && let Some(bw) = gpu_memory_bandwidth_gbps(system.gpu_name.as_deref().unwrap_or(""))
    {
        let active_gb = params * models::quant_bytes_per_param(quant);
        let efficiency = config.efficiency;
        // dense/MoE/run-mode-specific branches
        return ((bw / active_gb) * efficiency * mode_factor).max(0.1);
    }
    // backend constants only when bandwidth is unknown
}
```

逻辑摘要：known GPU走bandwidth roofline；MoE再区分 DDR expert offload、GPU two-component、VRAM pressure；unknown hardware才回退backend constants。`EstimateBasis`另保存method/bandwidth/efficiency/context/calibration。本机真实输出走`cpu_constant`，因此报告绝不把184.8 tok/s写成测量值。

**代码块 4：真实测量按来源优先级覆盖，并用中位比率校准所有估计**  
来源：[`llmfit-core/src/analysis.rs#L156-L205`](https://github.com/AlexsJones/llmfit/blob/acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe/llmfit-core/src/analysis.rs#L156-L205)

```rust
pub fn build_model_fits(/* ... */) -> Vec<ModelFit> {
    let local_index = LocalBenchIndex::load(specs);
    let community_index = CommunityBenchIndex::for_specs(specs);
    let measured_index = MeasuredTpsIndex::for_specs(specs);
    let mut fits = db.get_all_models().iter()
        .filter(|m| backend_compatible(m, specs))
        .map(|m| {
            let mut fit = ModelFit::analyze_with_forced_runtime(/* ... */);
            fit.measured_tps = local_index.as_ref().and_then(|x| x.lookup(&m.name))
                .or_else(|| community_index.as_ref().and_then(|x| x.lookup(&m.name)))
                .or_else(|| measured_index.as_ref().and_then(|x| x.lookup(&m.name, &fit.best_quant)));
            fit
        }).collect();
    apply_local_calibration(&mut fits);
    fits
}
```

逻辑摘要：source priority是 local exact hardware > community same hardware > broader measured preset；calibration只用>=1B dense trustworthy anchors，中位 measured/estimated ratio clamp在 `[0.05,3.0]`。边界是相同hardware name不等于driver/runtime/context完全相同，community data仍需provenance与acceleration flags。

**代码块 5：当前 HEAD 仍有两个不同 MLX suffix normalization 实现**  
来源：[`llmfit-core/src/providers.rs#L3280-L3285`](https://github.com/AlexsJones/llmfit/blob/acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe/llmfit-core/src/providers.rs#L3280-L3285) 与 [`#L3531-L3546`](https://github.com/AlexsJones/llmfit/blob/acc7e40c3a0afbd36510a92f2f8f3d5177cfc0fe/llmfit-core/src/providers.rs#L3531-L3546)

```rust
pub fn strip_mlx_quant_suffix(stem: &str) -> Option<String> {
    for pat in ["-mxfp4-q4", "-mxfp4", "-fp16"] { /* plus N-bit variants */ }
    // ...
}

fn strip_trailing_quant_suffix(name: &str) -> String {
    for suffix in ["-4bit", "-6bit", "-8bit"] { /* narrower */ }
    name.to_string()
}
fn normalize_mlx_repo_base(repo_lower: &str) -> String {
    let without_quant = strip_trailing_quant_suffix(repo_lower);
    without_quant.strip_suffix("-mlx").unwrap_or(&without_quant).to_string()
}
```

逻辑摘要：issue #869真实列出双向coverage差异，PR #895仍open；因此不能把`installed=true`当绝对事实，尤其MLX/GGUF name mapping。最重要的模式是：同一canonicalization只能有一个pure implementation与shared differential fixtures。

#### 依赖分析与供应链风险

- Rust workspace `llmfit-core`、`llmfit-tui`、`llmfit-desktop`，edition 2024，committed `Cargo.lock`；另有 React `package-lock.json`、Python `uv.lock`、Nix `flake.lock`。
- core直接依赖较窄：`sysinfo`、`serde(_json)`、`regex`、`ureq`、`which`、`dirs`、`yaml_serde`，macOS另有`objc2-metal`。但TUI/MCP/Web/Desktop扩展依赖面更大，包括ratatui/crossterm/axum/rmcp/Tauri/npm。
- model catalog、community benchmark JSON和runtime provider detection都是数据供应链；仓库MIT不覆盖每个模型的license。真实recommend JSON里有一项`license=null`，说明必须允许unknown而非默认可用。
- release asset sidecar checksum真实通过；同样未核验独立签名/provenance。README说明Windows artifacts由SignPath签名，但本次Linux asset不据此声称签名。
- 当前宿主无Cargo，无法跑`cargo test --workspace --locked`/`cargo audit`；公开 repository advisories 空数组不能证明依赖安全。
- README给出`curl | sh`安装，今日未执行；应优先下载、校验、检查后运行，不能直接pipe远端脚本。

#### README / docs / release / issues / source / 运行交叉核验

- README/`docs/how-it-works.md`对 four-dimensional scoring、bandwidth formula、dynamic quant 的描述与 `fit.rs`一致。
- release v1.1.10 说明新增Qwen3.8；issue #887的诊断是v1.1.9，故“当前仍缺失”不能直接成立，但真实provider/catalog E2E未做，标待核验。
- issue #869关于双stripper分裂与当前源码完全一致；PR #895 open，不能声称已统一。
- 本机官方binary真实检测 no GPU，输出5项 recommendations与 basis；没有运行任何模型或live provider，因此 tok/s、fit与score都是工具计算结果，不是本机实测质量/吞吐。
- `recommend --help`明确 side effects None 与 exit codes；本机JSON可解析。`doctor`把缺失nvidia-smi/rocm-smi/lspci/vulkaninfo/npu-smi逐项写为not available，而不是静默当GPU不存在的唯一证据。
- HEAD比release只ahead一个Action dependency commit；核心源码与实际运行binary接近，但严格源码片段对应HEAD、运行结果对应tag v1.1.10，已分开声明。

#### 可复用经验

- 当工具输出预测、评分或推荐时，应优先返回 `method + inputs + assumptions + calibration + verify command`，因为一个高分或tok/s数字无法区分测量、模型、fallback与默认常数；边界是provenance完整仍不保证公式正确。
- 当同一业务判断出现在CLI/TUI/Web/MCP/plan时，应优先集中到 sans-I/O core 并让所有projection委托它，因为复制公式会漏掉MoE或bug修复；边界是各adapter仍需验证schema、filter和side effects。
- 当模型/runtime名称需要canonicalization时，应优先只有一个pure normalizer和真实corpus differential fixtures，因为两个看似相似的stripper会产生installed/benchmark mapping冲突；边界是upstream naming仍会漂移，需要unknown终态。
- 当估计可被真实测量校准时，应优先保存未校准值、measurement source、hardware/runtime identity和bounded factor，因为直接覆盖会丢失模型误差证据；边界是同硬件不代表同driver/context/acceleration。
- 当硬件有unified、discrete、mixed或cluster路径时，应优先分开logical fit pool和physical execution capability，因为容量求和不证明runtime能高效利用；边界是拓扑/互联/driver需要实测。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/provenanced-estimate-envelope/` 做离线fixture，不下载模型：

1. 定义 `Estimate{value,unit,method,input_hash,assumptions,coverage,source_revision,calibration,verify_command,terminal}`。
2. 构造 `measured`、`formula`、`fallback_constant`、`unknown_prerequisite` 四类结果。
3. projection禁止把`formula/fallback`显示成“实测”；missing basis时overall为`partial`。
4. 两个normalizer对同一fixture输出不一致时gate失败并保存counterexample。
5. 用今日真实llmfit JSON作只读fixture，验证 `cpu_constant + local_calibration=null` 必须展示为“估计、未校准”。

#### 风险边界

- **License**：Repository/License API与根License为MIT；transitive crates/npm/Python packages、model weights/datasets、benchmark submissions分别审查。
- **维护活跃度**：pushed 2026-08-17，release v1.1.10同日；63 open issues/PR aggregate与高频catalog更新说明活跃，也说明数据/normalizer持续漂移。
- **安全风险**：provider discovery会读取本机runtime/cache；benchmark会连接live endpoint；download/share可写cache、发GitHub PR并涉及token。今日只运行read-only doctor/recommend。
- **正确性风险**：estimate依赖GPU bandwidth表、efficiency、context cap、quant metadata、provider normalization；#791/#869说明installed detection可误分类。
- **数据风险**：embedded catalog随binary release更新；用户可能把旧binary数据当最新；community benchmark可能受runtime/driver/acceleration差异影响。
- **隐私风险**：doctor报告含hardware/driver identity；share benchmark会出域。应先预览并授权。
- **测试边界**：release binary doctor/recommend真实成功；没有Cargo，源码compile/tests/audit待核验；没有GPU、model、Ollama/MLX/llama.cpp live server，未验证真实TPS、TTFT、quality、download/share。
- **不适用场景**：要求SLA级性能预测、未知硬件/自定义kernel、受限model license自动安装、把CPU heuristic当真实bench、跨机器无同一identity校准。
- **不能自动执行**：不安装llmfit skill，不改Hermes模型列表/provider，不下载模型，不运行bench/share，不设置GitHub token。

#### Skill 升格判断

**需二次验证**；provenanced estimate envelope 可迁移，llmfit advisor skill和模型推荐产品暂不沉淀。

- **可迁移候选**：estimate basis、measured-vs-estimated label、single decision core、多projection、calibration receipt、normalizer differential tests。
- **需二次验证**：先用Hermes模型/provider inventory的只读synthetic data做fixture，并与verification-first、model routing/config-target-routing去重。
- **暂不沉淀**：不复制上游 `skills/llmfit-advisor`、模型目录、bandwidth常数或provider mappings到shared。
- **升格结论**：若POC稳定，优先扩展既有 verification/research skill；今日只保留Hermes raw candidate。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/provenanced-estimate-envelope/{schema.json,fixtures/llmfit-cpu.json,normalizers.py,checker.py,test_contract.py}`。
2. **Hermes只读诊断**：未来如需模型适配建议，读取live system + `~/.hermes/config.yaml`前必须明确目标Hermes；输出candidate list与basis，不自动写config/provider/model。
3. **shared contract**：在现有research/verification skill中加入 `measured|estimated|fallback|unknown`标签与source revision；不把动态硬件/模型排名写入curated。
4. **runtime evidence**：doctor、recommend JSON、asset hash、benchmark stdout留`runtime/hermes/`；只有稳定方法论经审查后进入shared skill/fact。
5. **normalizer gate**：任何provider/model canonicalization变更先跑old-vs-new corpus differential，并对unmapped返回reason，不静默猜同一模型。
6. **OpenClaw边界**：当前不存在且未调用；上游repo虽有OpenClaw文档/installer，本次禁止安装。未来若存在，只复用agent-neutral estimate schema并独立验证其真实model/provider surface。

## 经验沉淀

1. 当系统同时保留canonical、raw、index、cache、ledger与backup时，应优先为每层声明role、source revision、重建与删除coverage，因为单层成功不能投影为整体一致或彻底忘记；边界是外部副本不可由本地receipt保证删除。
2. 当自动capture位于Agent热路径时，应优先用client spool、idempotency key、bounded ingress、429 backpressure与completion receipt，因为202 queued只是接收承诺；边界是at-least-once effect仍需幂等和reconcile。
3. 当混合不同检索或评分来源时，应优先使用rank/source-aware fusion并保留per-stream provenance，因为BM25、cosine、entity、启发式分数和实测值尺度不可比；边界是排序永远不是authority。
4. 当输出为估计或推荐时，应优先披露method、inputs、assumptions、coverage、calibration与verify command，因为裸数字最容易被误当实测；边界是完整basis也不能替代真实benchmark。
5. 当同一算法服务多个interface时，应优先抽出single sans-I/O decision core并让adapter委托，因为复制逻辑会形成修复漂移；边界是transport与projection仍需独立conformance test。
6. 当同一identity有多个normalizer时，应优先合并为一个pure function并运行真实corpus differential fixtures，因为看似等价的suffix/alias规则会双向漏配；边界是unknown必须显式保留而不是强行映射。
7. 当secret可能进入capture时，应优先“不采集”与path/tool policy，其次才是typed sanitizer与server backstop，因为regex只能降低已知泄漏；边界是canary通过不证明全类secret安全。
8. 当第三方release可直接运行时，应优先校验sidecar hash并在隔离目录做最小read-only/synthetic smoke；仍需明确asset/tag/source/provenance差异，不能用binary成功替代源码tests或安全审计。

## 明日继续

1. 跟踪 ai-memory #387 / PR #399：核对是否真正覆盖sessions、observations、handoffs、FTS、wiki、git、raw/spool/backups，并是否输出per-layer receipt。
2. 跟踪 ai-memory #407：检查是否增加standalone Docker inspect/recreate dry-run和auth migration preflight；不在当前宿主执行upgrade。
3. 跟踪 llmfit #869 / PR #895：若merge，固定新commit并跑normalizer corpus differential，核对installed/benchmark两条路径是否共用一个实现。
4. 建立 `runtime/hermes/github-learning-poc/truth-estimate-provenance/` 合并fixture：stale projection、partial purge、queued-not-complete、fallback estimate、normalizer conflict五类状态。
5. 若宿主后续具备Cargo，再在固定commit运行两仓`cargo test --workspace --locked`与可用audit工具；在此之前保持源码lane“待核验”。

## 候选反哺

### Candidate Facts

- [ ] topic: canonical truth 与derived index必须有source revision、rebuild与deletion coverage | evidence: ai-memory ARCHITECTURE/store/wiki源码、本机hook/status smoke、#387 | 建议: create（治理去重后） | 安全级别: medium
- [ ] topic: retrieval/estimate projection必须保留source/method/assumptions/calibration provenance | evidence: ai-memory reader RRF explain；llmfit EstimateBasis/analysis源码与本机JSON | 建议: create | 安全级别: low
- [ ] topic: identity canonicalization应只有一个pure implementation并做differential corpus gate | evidence: llmfit #869、当前providers.rs双stripper、open PR #895 | 建议: create（待merge验证） | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: canonical-derived layer receipt | 可复用场景: shared memory、index/cache、migration、purge | 是否建议 shared: yes（验证后） | 原因: Hermes/future agent共享中台都需，先与shared-memory/governance/receipt去重
- [ ] 名称: provenanced estimate envelope | 可复用场景: model selection、audit score、capacity/performance recommendation | 是否建议 shared: yes（验证后） | 原因: 防止估计/实测/fallback混淆，优先扩展既有verification skill
- [ ] 名称: ai-memory integration | 可复用场景: third-party cross-agent memory | 是否建议 shared: no | 原因: 与现有shared hub重叠，hook/secret/erase/upgrade边界未验证，Hermes仅community支持
- [ ] 名称: llmfit advisor install | 可复用场景: local model recommendation | 是否建议 shared: no | 原因: 动态catalog与宿主硬件特定，且不得自动改Hermes模型/provider配置

### Candidate Open Questions

- [ ] 问题: shared hub的删除/retire receipt应覆盖哪些inbox/runtime/git/backup层，哪些明确out-of-scope？ | reason: adaptation | priority: high
- [ ] 问题: GitHub-learning的audit score是否也应像EstimateBasis一样输出scorer version/coverage/method，而不只是总分？ | reason: adaptation | priority: high
- [ ] 问题: 202 queued阶段怎样与overall_status completed建立可验证completion marker，而不扩大orchestrator复杂度？ | reason: gap | priority: high
- [ ] 问题: llmfit PR #895合并后是否所有MLX installed/bench/download路径真正共享同一normalizer？ | reason: gap | priority: medium
- [ ] 问题: ai-memory strong purge如何处理git remote、已导出backup和客户端spool这类不可撤回副本？ | reason: gap | priority: high

### 不应自动落地

- 不自动修改Hermes/OpenClaw配置、model、provider、auth、env、cron、skills；当前OpenClaw不存在且本次未调用。
- 不自动写curated active fact；以上只进入Hermes inbox/runtime候选，等待评分、去重、脱敏与治理审查。
- 不安装ai-memory MCP/hooks/community Hermes plugin，不启动长期服务，不导入shared历史。
- 不安装llmfit advisor skill，不下载/运行模型，不bench、不share PR，不用doctor/recommend改变模型配置。
- 不把MIT repository license外推到Cargo/npm/Python依赖、Docker image、模型、数据、benchmark或release provenance。
- 不把release binary smoke外推为源码tests通过；本机无Cargo/Rustc，两个Rust源码lane均保持待核验。
