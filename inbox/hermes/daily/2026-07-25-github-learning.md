# 2026-07-25 GitHub 热门项目学习日报（Hermes）

> 执行器：Hermes（未调用 OpenClaw）  
> GitHub Trending 抓取时间：2026-07-25 07:30 CST  
> 项目元数据最终查询时间：2026-07-25 07:37 CST  
> 元数据来源：`gh api repos/{owner}/{repo}`；趋势来源：`https://github.com/trending?since=daily`  
> 深读快照：`block/buzz@264a56a2260ac87350bfe1f5d3ec3d89615eb47c`、`likec4/likec4@f9700621c2bd8cc6c002d54b813a4d251e3f7bd8`、`Automattic/harper@efa59c33b2915108f52c385ce1e3311a3cfa1439`

## 今日结论

**今日主线是“把 Agent 系统的可信性做在边界与中间表示里”：Buzz 在投递 chokepoint 重验租户/成员权限并用规范化 hash chain 留证；LikeC4 把架构文本变成分阶段模型并隔离 dev RPC；Harper 把自然语言质量检查拆成可缓存、可测试、离线的确定性规则。** 三者都提示：不能只靠提示词约束，必须把 scope、stage、effect、cache key 和失败状态编码进结构与代码。

## 研究方法与证据边界

- 真实执行了 GitHub API、Trending HTML 抓取、README/release/issues API 查询、三个仓库的浅克隆和固定 commit 源码读取。
- Stars、Forks、Language、License、更新时间均来自 2026-07-25 当次 GitHub API；数字会随时间变化，不把本报告数字当永久事实。
- 源码结论只针对上方固定 commit；未运行三个上游仓库的完整构建/测试，因此运行时行为仍需 POC 二次验证。
- README、docs、release、issue 是项目方声明或当前状态证据；性能宣传不等同于本机 benchmark。
- 本轮没有改配置、模型、provider、cron、secret，也没有写入 curated active fact；只写 Hermes inbox 与 runtime 学习产物。

## 项目速览

下表全部来自 2026-07-25 07:37 CST 的 GitHub Repository API；`Pushed At` 是代码最近推送时间。`NOASSERTION` 表示 API 未给出可核验 SPDX license，**不等于无版权限制**。

| 项目 | Stars | Forks | Language | License | Pushed At (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [block/buzz](https://github.com/block/buzz) | 9,882 | 766 | Rust | Apache-2.0 | 2026-07-24T23:35:59Z | 深读：多租户事件投递、Agent 身份与审计链值得迁移 |
| [likec4/likec4](https://github.com/likec4/likec4) | 5,010 | 334 | TypeScript | MIT | 2026-07-24T17:24:03Z | 深读：架构模型 stage、虚拟模块与 dev RPC 边界清晰 |
| [Automattic/harper](https://github.com/Automattic/harper) | 13,020 | 481 | Rust | Apache-2.0 | 2026-07-24T04:09:59Z | 深读：离线确定性文本检查、规则 DSL 与分块缓存 |
| [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | 73,235 | 10,980 | TypeScript | NOASSERTION | 2026-07-24T21:00:41Z | 热度高，但 license 未由 API 核验，本轮不迁移源码 |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 70,031 | 7,900 | Python | NOASSERTION | 2026-07-24T07:48:01Z | 适合发现候选，不应把聚合清单当可信 skill registry |
| [Pumpkin-MC/Pumpkin](https://github.com/Pumpkin-MC/Pumpkin) | 9,324 | 632 | Rust | GPL-3.0 | 2026-07-24T18:25:58Z | 高性能服务端值得后续看，但 GPL 边界需先评估 |
| [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | 33,473 | 5,677 | Python | MIT | 2026-04-13T12:38:49Z | 金融模型热度高，代码推送距查询日较远，先观察维护节奏 |
| [yorukot/superfile](https://github.com/yorukot/superfile) | 19,556 | 596 | Go | MIT | 2026-07-24T17:41:57Z | TUI/文件操作体验可参考，但与 shared hub 主线较弱 |

---

## 深读项目

### 项目 1. block/buzz

- **链接**：https://github.com/block/buzz
- **API 基本信息**：Stars: **9,882**；Forks: **766**；License: **Apache-2.0**；Language: Rust；API `updated_at`: 2026-07-24T23:37:04Z；`pushed_at`: 2026-07-24T23:35:59Z。
- **固定快照**：[`264a56a`](https://github.com/block/buzz/commit/264a56a2260ac87350bfe1f5d3ec3d89615eb47c)，提交时间 2026-07-24T23:28:39Z。
- **Release / Issues**：最新 release [`v0.4.25`](https://github.com/block/buzz/releases/tag/v0.4.25)，发布于 2026-07-24T23:04:14Z；查询到的近期 open issue 包括 [#2787 model picker 缺少 claude-opus-5 显式条目](https://github.com/block/buzz/issues/2787) 和 [#1 Dependency Dashboard](https://github.com/block/buzz/issues/1)。
- **一句话判断**：它值得学的不是“又一个协作 UI”，而是把人、Agent、workflow、Git 活动统一成签名事件，同时在真正发送数据的 chokepoint 重新验证 tenant/access，并为每个 community 建独立审计链。
- **解决的问题**：替代聊天、Agent bot、代码托管、工作流、搜索和审计各自维护身份与记录的旧做法；更关键的是，避免“订阅建立时有权限，之后权限变化但 stale subscription 继续泄漏”的 TOCTOU 风险。

#### 架构 / 实现与数据流

README 和 `ARCHITECTURE.md` 描述的是 Nostr-first relay：客户端（Desktop / Agent ACP / CLI）经 WebSocket/窄 HTTP 面进入 `buzz-relay`，持久事件写入 Postgres，Redis 做跨 pod pub/sub，S3/MinIO 保存媒体。源码显示持久事件的关键流为：

1. 事件在 ingest seam 完成验证和持久化；
2. `dispatch_persistent_event` 先等待 bounded audit enqueue，再把 Redis publish、local fan-out、workflow side effects 放入 post-commit task；
3. `filter_fanout_by_access` 在发送前按 `community_id`、author-only、channel visibility、current membership fail-closed 重验；
4. `buzz-audit` 按 community 获取 Postgres advisory lock，读当前 chain head、规范化时间、计算 SHA-256，再在事务中 append；
5. 跨 pod 收到 Redis 事件时以 `(community_id, event_id)` 去重，仍经过同一访问过滤逻辑。

这不是“订阅授权一次后永远相信”，而是“subscription 只决定候选，delivery 才做最终授权”。

#### Repo tree 摘要

```text
block/buzz/
├── crates/
│   ├── buzz-core/          # 事件、kind、filter、验证、tenant 类型
│   ├── buzz-relay/         # Axum WebSocket/HTTP relay 与最终投递边界
│   ├── buzz-db/            # Postgres 事件存储
│   ├── buzz-auth/          # NIP-42/98 认证、rate limit
│   ├── buzz-pubsub/        # Redis fan-out / presence
│   ├── buzz-audit/         # per-community append-only hash chain
│   ├── buzz-acp/           # ACP Agent harness
│   ├── buzz-cli/           # 面向 Agent 的 JSON-in/JSON-out CLI
│   ├── buzz-workflow/      # YAML workflow engine
│   └── buzz-dev-mcp/       # shell / file edit MCP 工具面
├── desktop/                # Tauri 2 + React 19
├── web/                    # relay 服务的浏览器客户端
├── mobile/                 # Flutter 客户端
├── migrations/             # 启动时执行的 SQL migrations
├── Cargo.toml              # Rust workspace 与依赖版本
└── AGENTS.md               # crate map、边界、质量门禁
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/buzz-relay/src/handlers/event.rs` | local / Redis / persistent fan-out | `filter_fanout_by_access` 是发送前授权 chokepoint；不可把注册 subscription 当授权证明 |
| `crates/buzz-relay/src/admission.rs` | 共享 rate-limit admission | limiter 出错时返回 `Unavailable`，即 fail-closed；5 秒 burst 保持平均速率 |
| `crates/buzz-audit/src/service.rs` | 每租户审计链 append/verify | community-scoped advisory lock + transaction；跨 relay process 串行同一租户，租户间并行 |
| `crates/buzz-audit/src/hash.rs` | hash preimage 规范化 | tenant id、seq、时间、字段 presence、canonical JSON、prev hash 都进入 SHA-256 |
| `Cargo.toml` | workspace 依赖与供应链入口 | Axum/Tokio/SQLx/Redis/Nostr；含一个固定 git rev 的 `aws-creds` patch |

#### ⭐ 源码精读 1：共享 admission 故障时拒绝，而不是降级放行

固定源码：[`crates/buzz-relay/src/admission.rs`](https://github.com/block/buzz/blob/264a56a2260ac87350bfe1f5d3ec3d89615eb47c/crates/buzz-relay/src/admission.rs#L17-L37)

```rust
pub(crate) async fn check_principal<L: RateLimiter>(
    limiter: &L,
    tenant: &TenantContext,
    pubkey: &PublicKey,
    limit_type: LimitType,
    window_secs: u64,
    limit: u64,
) -> Result<(), AdmissionError> {
    match limiter
        .check_and_increment(tenant, pubkey, limit_type, window_secs, limit)
        .await
    {
        Ok(result) if result.allowed => Ok(()),
        Ok(result) => Err(AdmissionError::Exceeded {
            reset_in_secs: result.reset_in_secs,
        }),
        Err(error) => {
            tracing::warn!(error = %error, "shared rate-limit admission unavailable");
            Err(AdmissionError::Unavailable)
        }
    }
}
```

逻辑摘要：限流器不仅使用 `tenant + pubkey + limit_type`，共享计数器不可用也不会 silently allow。对有资源滥用风险的 Agent 工具网关，这个失败语义比“Redis 挂了先放行”更安全。

#### ⭐ 源码精读 2：候选订阅者在发送时重新校验 tenant 和成员资格

固定源码：[`crates/buzz-relay/src/handlers/event.rs`](https://github.com/block/buzz/blob/264a56a2260ac87350bfe1f5d3ec3d89615eb47c/crates/buzz-relay/src/handlers/event.rs#L115-L199)

```rust
pub async fn filter_fanout_by_access(
    state: &AppState,
    community_id: CommunityId,
    stored_event: &StoredEvent,
    matches: Vec<(crate::subscription::ConnId, crate::subscription::SubId)>,
    threaded: Option<&crate::state::ThreadedChannelVisibility>,
) -> Vec<(crate::subscription::ConnId, crate::subscription::SubId)> {
    let matches: Vec<_> = matches
        .into_iter()
        .filter(|(conn_id, _)| {
            state.conn_manager.community_for_conn(*conn_id) == Some(community_id)
        })
        .collect();
    // ... author-only gate ...
    let Some(channel_id) = stored_event.channel_id else {
        return matches;
    };
    // visibility lookup failure returns an empty recipient set (fail closed)
    // private channels then re-check current membership per recipient
}
```

逻辑摘要：先把连接绑定的 community 与事件标签比较；再处理 author-only；有 channel 时验证 visibility，读失败直接空集；private channel 逐连接读取认证 pubkey 并检查最新 membership。`threaded` 快照只有 scope 完全匹配才复用，避免把别的 channel 结果误当当前授权。

#### ⭐ 源码精读 3：按 community 串行 append 审计链

固定源码：[`crates/buzz-audit/src/service.rs`](https://github.com/block/buzz/blob/264a56a2260ac87350bfe1f5d3ec3d89615eb47c/crates/buzz-audit/src/service.rs#L41-L80)

```rust
pub async fn log(&self, entry: NewAuditEntry) -> Result<AuditEntry, AuditError> {
    let mut conn = self.pool.acquire().await?;
    let lock_key = format!("{AUDIT_LOCK_NAMESPACE}{}", entry.community_id);
    sqlx::query("SELECT pg_advisory_lock(hashtextextended($1, 0))")
        .bind(&lock_key)
        .execute(&mut *conn)
        .await?;

    let result = std::panic::AssertUnwindSafe(self.log_inner(&mut conn, entry))
        .catch_unwind()
        .await;

    let _ = sqlx::query("SELECT pg_advisory_unlock(hashtextextended($1, 0))")
        .bind(&lock_key)
        .execute(&mut *conn)
        .await;
    // return or resume panic
}
```

逻辑摘要：lock key 含 community id，所以同租户链 head 的竞争被串行，不同租户不互相阻塞；panic 也尽力释放 session advisory lock。这解决了多 relay process 同时读同一 head、生成重复 seq/错误 prev hash 的竞态。

#### ⭐ 源码精读 4：hash 输入必须与存储 round-trip 一致

固定源码：[`crates/buzz-audit/src/hash.rs`](https://github.com/block/buzz/blob/264a56a2260ac87350bfe1f5d3ec3d89615eb47c/crates/buzz-audit/src/hash.rs#L22-L72)

```rust
pub fn to_storage_precision(created_at: DateTime<Utc>) -> DateTime<Utc> {
    created_at.trunc_subsecs(6)
}

pub fn compute_hash(entry: &AuditEntry) -> Result<[u8; 32], AuditError> {
    let mut hasher = Sha256::new();
    hasher.update(entry.community_id.as_bytes());
    hasher.update(entry.seq.to_be_bytes());
    hasher.update(to_storage_precision(entry.created_at).to_rfc3339().as_bytes());
    hasher.update(entry.action.as_str().as_bytes());
    // actor/object presence tags + canonical JSON detail + prev hash
    Ok(hasher.finalize().into())
}
```

逻辑摘要：最新 commit 正是在修 `Utc::now()` 纳秒精度与 Postgres `TIMESTAMPTZ` 微秒精度不一致导致的永久 `HashMismatch`。经验不是“用了 SHA-256 就可信”，而是 **hash preimage 必须先按持久层实际 round-trip 规范化**。旧行本来就不可验证，提交说明明确要求运营者 re-anchor。

#### 依赖分析与供应链风险

- 核心：Tokio 1、Axum 0.8、Tower 0.5、SQLx 0.9、Redis 1.0、Nostr 0.44、Serde、OpenTelemetry、Reqwest、SHA-2、HMAC。
- `Cargo.toml` 将 `aws-creds` patch 到 `https://github.com/tlongwell-block/rust-s3` 的固定 rev `c9fce...`；固定 rev 优于浮动 branch，但绕开 crates.io 发布链，需要单独审计 fork、持续追踪 upstream 合并。
- `buzz-relay` dev-dependencies 包含以 tag 固定的 Mesh-LLM GitHub 依赖；虽是 dev-only，CI/test 构建仍会拉取外部 git 源。
- 大型 monorepo 同时覆盖 relay、Git、media、workflow、Agent shell/MCP、桌面与移动端，攻击面和依赖图都很大；不可因 Apache-2.0 就直接整体引入。

#### 可复用经验

- **当订阅、session 或缓存权限可能在建立后变化时，应优先在最终发送/执行 chokepoint 重验 tenant、resource 与当前 membership，因为 subscription 只是候选匹配，不是持续授权；边界是额外读放大会影响延迟，需要 scoped cache 且读取失败必须 fail-closed。**
- **当多进程要追加同一条证据链时，应优先使用 scope-derived lock + transaction 串行 chain head，而不是只靠进程内 mutex；边界是数据库 advisory lock 的 session 生命周期和超时必须监控。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/scoped-delivery-gate/` 做纯 Python fixture：输入 `event_scope / connection_scope / visibility / membership_lookup_result`，输出 `allowed|denied|blocked`；至少覆盖 wrong tenant、private non-member、membership backend failure、matching public scope。只验证协议，不启动 Buzz、不接真实消息系统。

#### 风险边界

- **License**：Apache-2.0 可用于模式研究和合规复用，但复制代码仍需保留 notice 并做依赖 license 扫描。
- **维护活跃度**：查询日有当天 push 和 release，活跃；但 API open issues count 为 604，且最新 commit 修复的是会让真实审计链全部验证失败的基础问题，说明高活跃不等于成熟稳定。
- **安全风险**：无密钥 SHA-256 hash chain 能检出未同步重算的篡改，不能阻止拥有数据库写权限的攻击者重写整条链；需要外部锚定/签名/只写介质才能增强对强攻击者的保证。
- **局限 / 不适用**：shared hub 是文件治理中台，不需要复制完整 Nostr relay、Redis、Postgres 和协作 UI；若数据量小，数据库级链与实时 pubsub 可能过度设计。
- **运行核验**：未启动 Postgres/Redis，也未运行 Buzz tests；所有运行结论待本地 fixture/集成环境核验。

#### Skill 升格判断与 Hermes/shared hub 落地路径

- **Skill 升格判断：需二次验证。** 可迁移的是“final-boundary scoped authorization + tenant-bound evidence”契约，不是 Buzz 平台本身。先验证四状态、cache scope、fail-closed 和 evidence canonicalization，再决定是否合并到现有治理/审计 skill；现在不新建 shared skill，避免与既有 verification-first、治理标准重复。
- **Hermes/shared hub 落地路径**：
  1. POC：`runtime/hermes/github-learning-poc/scoped-delivery-gate/`；
  2. 若 POC 通过，在 `scripts/` 新增通用 evidence verifier 时必须通过 `scripts/resolve_shared_root.py` 定位根；
  3. 候选契约写入 inbox 报告，审查后才可更新 `capabilities/skills/autonomous-learning/self-reflection-engine/` 或新建 narrowly-scoped shared skill；
  4. 任何 Agent 的最终写入/推送操作以 `(agent, job/run, resource/path)` 复合 scope 重新授权，并把 canonical payload hash、source、status 写 runtime evidence；
  5. 不自动改 Hermes/OpenClaw 配置、cron 或 secret。

---

### 项目 2. likec4/likec4

- **链接**：https://github.com/likec4/likec4
- **API 基本信息**：Stars: **5,010**；Forks: **334**；License: **MIT**；Language: TypeScript；API `updated_at`: 2026-07-24T23:33:04Z；`pushed_at`: 2026-07-24T17:24:03Z。
- **固定快照**：[`f970062`](https://github.com/likec4/likec4/commit/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8)，提交时间 2026-07-22T18:45:37Z。
- **Release / Issues**：最新 release [`v1.59.2`](https://github.com/likec4/likec4/releases/tag/v1.59.2)，发布于 2026-07-22T18:58:22Z，修复 imported element dynamic view、metadata keyword 和 MCP `npx` runtime dependencies；近期 issue [#2017 Dependency Dashboard](https://github.com/likec4/likec4/issues/2017) 于查询日前仍更新。
- **一句话判断**：LikeC4 值得学的是把可编辑 DSL 变成 `parsed → computed → layouted` 的显式模型阶段，再用 Vite virtual module/HMR 给 UI 供数、用 birpc 把“读模型”和“改模型”隔开。
- **解决的问题**：替代手工维护易过期图和每个消费者各自解析文本的旧做法；同时避免 diagram UI 直接依赖 language server、把 transport/存储/模型计算混成一层。

#### 架构 / 实现与数据流

源码和仓库 `AGENTS.md` 给出的 dev 数据流是：

`*.c4 DSL → language-server / language-services → Parsed model → computeLikeC4Model → layout → vite-plugin virtual module → likec4-spa nanostore → diagram`。

开发期 mutation 走 `SPA → likec4:rpc (birpc over Vite HMR) → vite-plugin → language-services → updated virtual model → HMR`。生产 `likec4 build` 不带 RPC，虚拟模块内联静态 JSON并只读。该分层把 UI contract (`diagram`)、host (`likec4-spa`) 和 data/RPC bridge (`vite-plugin`) 分开。

#### Repo tree 摘要

```text
likec4/likec4/
├── apps/
│   ├── docs/                    # 文档站
│   └── playground/              # 在线试验
├── packages/
│   ├── core/                    # model types、builder、compute-view
│   ├── language-server/         # Langium DSL parser / LSP
│   ├── language-services/       # Browser/Node 服务初始化
│   ├── layouts/                 # Graphviz layout
│   ├── vite-plugin/             # virtual modules + dev RPC bridge
│   ├── likec4-spa/              # UI host / nanostore / HMR
│   ├── diagram/                 # React/ReactFlow renderer
│   ├── generators/              # Mermaid/PlantUML/D2/LikeC4 export
│   ├── mcp/                     # MCP package
│   └── likec4/                  # CLI / static site / SDK entry
├── examples/                    # 示例模型
├── skills/                      # 上游 Agent skills（不直接导入 shared）
├── e2e/                         # Playwright tests
└── package.json                 # pnpm 11 + turbo monorepo
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/core/src/types/model-data.ts` | stage 数据契约 | Parsed/Computed/Layouted 模型的共享字段与差异 |
| `packages/core/src/compute-view/compute-view.ts` | parsed → computed | 对每个 parsed view 执行 `unsafeComputeView`，返回 stage 标记为 computed 的模型 |
| `packages/core/src/builder/Builder.ts` | typed builder 与 runtime compatibility | phantom type ledger；`assertSpecificationCompatible` 给 typed cast 加运行时 guard |
| `packages/vite-plugin/src/virtuals/model.ts` | 模型虚拟模块 | layouted model 序列化为 JS atom，HMR 时更新 store |
| `packages/vite-plugin/src/rpc/rpc.ts` | dev mutation bridge | 只注册明确的 update/calc/layout 三个 RPC，错误去重后回传 client |
| `package.json` | monorepo toolchain | Node >=22.22.3、pnpm 11.15、Turbo、Vitest、oxlint、dprint |

#### ⭐ 源码精读 1：显式从 Parsed 计算为 Computed

固定源码：[`packages/core/src/compute-view/compute-view.ts`](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/packages/core/src/compute-view/compute-view.ts#L70-L90)

```ts
export function computeLikeC4Model<
  A extends AnyAux,
  B extends aux.toComputed<A> = aux.toComputed<A>
>(parsed: ParsedLikeC4ModelData<A>): LikeC4Model<B> {
  return LikeC4Model.create(computeParsedModelData<A, B>(parsed))
}
```

`computeParsedModelData` 去掉输入 `_stage`，对 `views` 逐项计算，再返回 `[_stage]: 'computed'`。逻辑摘要：stage 不只是文档概念，而是类型参数与数据字段共同表达，消费者可要求 Computed/Layouted，而不误拿 Parsed view 当最终图。

#### ⭐ 源码精读 2：虚拟模块把 layouted model 变成可热更新 atom

固定源码：[`packages/vite-plugin/src/virtuals/model.ts`](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/packages/vite-plugin/src/virtuals/model.ts#L6-L44)

```ts
const projectModelCode = (model: LikeC4Model.Layouted) => `
import { createHooksForModel, atom } from 'likec4/vite-plugin/internal'
export let $likec4data = atom(${JSON5.stringify(model.$data)})
export let { updateModel, $likec4model, useLikeC4Model } =
  createHooksForModel($likec4data)
if (import.meta.hot) {
  import.meta.hot.accept(md => {
    const update = md.$likec4data?.get()
    if (update) import.meta.hot.data.$update(update)
    else import.meta.hot.invalidate()
  })
}
`
```

逻辑摘要：plugin 读取 `layoutedModel(project.id)`，生成模块代码；SPA 只消费 virtual module contract，不知道 LSP 如何读取文件。HMR 有 update 就替换 atom，无 update 才 invalidate。这适合把 shared hub 的 curated facts 编译成只读 query snapshot，而不是让每个 UI/Agent直接扫描 Markdown。

#### ⭐ 源码精读 3：dev RPC 只暴露显式方法并集中错误处理

固定源码：[`packages/vite-plugin/src/rpc/rpc.ts`](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/packages/vite-plugin/src/rpc/rpc.ts#L15-L47)

```ts
export function enablePluginRPC(
  this: MinimalPluginContextWithoutEnvironment,
  params: PluginRPCParams,
) {
  const functions: LikeC4VitePluginRpc = {
    updateView: (data) => updateView(params, data),
    calcAdhocView: (data) => calcAdhocView(params, data),
    applySemanticLayout: (data) => applySemanticLayout(params, data),
  }
  createBirpc(functions, {
    on: fn => params.server.hot.on('likec4:rpc', fn),
    post: data => params.server.hot.send('likec4:rpc', data),
    onFunctionError: (error, functionName) => { /* log + send deduped error */ },
  })
}
```

逻辑摘要：调用面不是任意 command，而是三个 typed function；transport 被封装在 Vite HMR channel。可迁移时还需补 effect metadata、鉴权和 path scope，不能把“方法清单有限”误当完整安全边界。

#### ⭐ 源码精读 4：typed cast 前做 runtime specification guard

固定源码：[`packages/core/src/builder/Builder.ts`](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/packages/core/src/builder/Builder.ts#L368-L392)

```ts
export function assertSpecificationCompatible(
  declared: BuilderSpecification,
  loaded: SpecificationShape,
): void {
  const missing: string[] = []
  // compare declared element/deployment/relationship kinds, tags, metadata keys
  if (missing.length > 0) {
    throw new Error(
      `Specification mismatch — declared but not present in the loaded model:\n` +
      `  - ${missing.join('\n  - ')}`,
    )
  }
}
```

逻辑摘要：TypeScript 类型在 runtime 不存在，因此对“我声明模型有这些 kind/tag”的 typed cast 再做真实加载模型的 subset 检查。它不能证明样式与语义完全一致，但能防止最危险的“类型说存在、数据其实没有”。

#### 依赖分析与供应链风险

- 根工程：Node >=22.22.3、pnpm 11.15.0、Turbo、TypeScript、Vitest、oxlint、dprint、Husky。
- `@likec4/core` runtime 依赖 `immer`、`type-fest`、`zod`；开发/构建依赖 Graphology、Remeda、Markdown/HTML sanitize 链等。
- `@likec4/vite-plugin` 依赖多个 workspace package、Langium、JSON5、Zod、WebSocket，并把 React/Vite/TanStack AI providers 声明为 peer/optional 组合。
- 大量 `catalog:` 和 `workspace:*` 提高版本统一性，但实际解析依赖由 lockfile 和 workspace catalog 决定；审计单个 `package.json` 不足，必须同时固定 `pnpm-lock.yaml`。
- v1.59.2 专门修复 MCP `npx` 安装缺 runtime dependencies，证明 monorepo 内可用不代表发布包完整；包产物必须做 clean-install smoke test。

#### 可复用经验

- **当同一事实要被 UI、Agent、CLI 与审计共同消费时，应优先生成带 `stage` 和 schema 的中间模型，再由各 consumer 读取 snapshot，因为重复解析原始 Markdown 会产生语义漂移；边界是 stage 转换必须公开有损字段和 source location。**
- **当开发期需要写回而生产期只需读取时，应优先把 mutation RPC 与静态数据模块分开，并在生产构建移除 RPC；边界是 dev RPC 仍需鉴权、effect 标注、输入验证和 workspace path 限制。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/shared-memory-model/` 写一个只读脚本：将 2 个 fixture fact Markdown 编译为 `parsed.json`，再计算 `computed.json`（去重 topic、补 source path、标 `stage`），查询端只接受 `stage=computed`。加入一个缺 source 的 fixture，预期状态为 `blocked`，而非输出“空结果”。

#### 风险边界

- **License**：MIT 宽松，但上游仓库有 `THIRD-PARTY-NOTICES.txt`，实际分发仍需检查第三方依赖与 Graphviz/layout 相关组件。
- **维护活跃度**：查询日前 3 天发布 v1.59.2、查询日有 push，维护活跃；API open issues count 为 170。
- **安全风险**：dev RPC 经 Vite HMR 传输，源码片段本身未展示 auth；不应暴露在不可信网络。虚拟模块将模型数据嵌入 JS，涉及内部架构时要限制构建产物和日志可见性。
- **局限 / 不适用**：DSL writeback 在仓库说明中明确有损，不保留 comments/source positions/original formatting；不能把 generated DSL 覆盖原文当无损 round-trip。小型静态项目也可能不值得引入完整 LSP/Vite/Graphviz monorepo。
- **运行核验**：本轮未安装 Node 22/pnpm 11 依赖，也未运行 LikeC4 tests；build、HMR 与 RPC 行为待 POC 核验。

#### Skill 升格判断与 Hermes/shared hub 落地路径

- **Skill 升格判断：需二次验证。** “stage-aware architecture evidence model”可能成为共享能力，但昨日已有相近 candidate；今天不重复新建 skill。先验证 source location、schema migration、invalid/blocked 状态和 snapshot freshness，再由治理审查决定更新既有 candidate 还是关闭重复项。
- **Hermes/shared hub 落地路径**：
  1. 原始 Markdown 仍在 `curated/memory/` 与 `inbox/`，不直接让 runtime index 反写真相源；
  2. 编译产物放 `runtime/hermes/shared-memory-model/`，字段至少含 `schema_version / stage / source_path / source_hash / generated_at / diagnostics`；
  3. 查询接口在 `scripts/` 中通过 root resolver 取根，不硬编码宿主路径；
  4. 只读查询可供 Hermes/future agent 使用，任何 writeback 输出 patch 到 inbox 候选，不能自动覆盖 curated；
  5. 若升格为 shared skill，再更新 `capabilities/manifests/shared-skills.yaml`，并明确 effect=`read-only` 与 invalid/blocked/error 四状态。

---

### 项目 3. Automattic/harper

- **链接**：https://github.com/Automattic/harper
- **API 基本信息**：Stars: **13,020**；Forks: **481**；License: **Apache-2.0**；Language: Rust；API `updated_at`: 2026-07-24T23:31:27Z；`pushed_at`: 2026-07-24T04:09:59Z。
- **固定快照**：[`efa59c3`](https://github.com/Automattic/harper/commit/efa59c33b2915108f52c385ce1e3311a3cfa1439)，提交时间 2026-07-23T19:44:06Z。
- **Release / Issues**：最新 release [`v2.6.0`](https://github.com/Automattic/harper/releases/tag/v2.6.0)，发布于 2026-06-24T16:01:05Z；近期 issues 包括 [#3874 Memory Leak](https://github.com/Automattic/harper/issues/3874)、[#3875 dictionary entries and `'s`](https://github.com/Automattic/harper/issues/3875)、[#3868 Firefox highlight offset](https://github.com/Automattic/harper/issues/3868)。
- **一句话判断**：Harper 展示了怎样把“文本质量”从云端 LLM 主观改写拆成离线 parser → annotated Document → deterministic linters → spans/suggestions，并用 Weir DSL 让规则和测试一起交付。
- **解决的问题**：替代把私有文本发送到云端 grammar service、依赖巨大 n-gram 数据集，或仅靠 LLM prose 判断“看起来没问题”的旧做法；它给出可定位 span、可配置 rule、可重复执行的结果。

#### 架构 / 实现与数据流

官方 architecture docs 把核心类型压缩为 `Document / Parser / Linter`：

1. Parser 从 Markdown、plain text、代码等输入提取可检查 token；
2. `Document::new_from_chars` 执行 parser，应用 token fixups，再调用 Brill tagger 和 chunker，并从 dictionary 补 metadata；
3. `LintGroup` 聚合普通 Linter、chunk ExprLinter、sentence ExprLinter，以稳定有序 map 管理，按 chunk/sentence 与 config hash 缓存；
4. 每个 Linter 返回 `Lint { span, kind, suggestions, message, priority }`；
5. `harper-ls` 包装 core 给编辑器，`harper-wasm` / `harper.js` 给浏览器和 JS 集成，CLI/各编辑器插件复用同一 core；
6. Weir 规则先 lex/parse/optimize 为 AST，解析结果有上限为 10,000 的 LRU cache；规则内可携带 test，`run_tests` 有最大 suggestion transformation depth 防无限搜索。

#### Repo tree 摘要

```text
Automattic/harper/
├── harper-core/              # tokenizer、Document、dictionary、linters、Weir
├── harper-ls/                # Language Server
├── harper-wasm/              # Rust → WebAssembly
├── harper-cli/               # CLI
├── harper-tree-sitter/       # 代码语言文本提取
├── harper-brill/             # POS tagging / chunking
├── harper-*/                 # HTML/Typst/TeX/Asciidoc 等 parser 或 integration
├── packages/
│   ├── harper.js/            # JS/WASM API
│   ├── vscode-plugin/        # VS Code
│   ├── obsidian-plugin/      # Obsidian
│   ├── chrome-plugin/        # 浏览器插件
│   └── web/                  # 文档与网站
├── harper-desktop/           # Desktop app
├── Cargo.toml                # Rust workspace / release profile
└── AGENT_POLICY.md           # 上游 AI-generated code policy
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `harper-core/src/document.rs` | 文本中间表示 | parser tokenization、fixups、Brill tag/chunk、dictionary metadata |
| `harper-core/src/linting/mod.rs` | `Linter` contract | mutable self 只为 cache，输出结构化 `Vec<Lint>` |
| `harper-core/src/linting/lint_group/mod.rs` | 规则注册与增量 cache | chunk/sentence 分层，cache key 含 unit/config hash，rule name 稳定排序 |
| `harper-core/src/weir/mod.rs` | Weir DSL → Linter | `main/message/description/becomes/scope` 解析，规则内 tests |
| `harper-core/src/weir/parsing/stmt.rs` | Weir parser cache | `(source, optimizer flag)` 为 key 的 bounded LRU；lex/parse/optimize |
| `harper-core/Cargo.toml` | core 依赖 | FST、Brill、regex、LRU、ammonia、pulldown-cmark、zip 等 |

#### ⭐ 源码精读 1：构造 Document 时把文本变成可查询的带注解 token

固定源码：[`harper-core/src/document.rs`](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/harper-core/src/document.rs#L52-L81)

```rust
pub fn new_from_chars(
    source: Lrc<[char]>,
    parser: &impl Parser,
    dictionary: &impl Dictionary,
) -> Self {
    let tokens = parser.parse(&source);
    let mut document = Self { source, tokens };
    document.parse(dictionary);
    document
}
```

`parse` 先 `apply_fixups()`，再对 sentence 运行 `brill_tagger()` 与 `burn_chunker()`，并把词典 metadata、POS tag、nominal phrase flag 写回 token。逻辑摘要：规则不是每次重读原始字符串，而是共享同一个含 span/词法/句法 metadata 的中间表示。

#### ⭐ 源码精读 2：Linter contract 保持简单，聚合层负责缓存

固定源码：[`harper-core/src/linting/mod.rs`](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/harper-core/src/linting/mod.rs#L334-L353)

```rust
pub const MAX_SUGGESTION_TRANSFORMATION_DEPTH: usize = 100;

pub trait Linter: LSend {
    fn lint(&mut self, document: &Document) -> Vec<Lint>;
    fn description(&self) -> &str;
}
```

逻辑摘要：`lint` 的输入输出确定且结构化，`&mut self` 明确用于 caching；多步 suggestion 搜索有 100 层硬上限。迁移到 Agent 质量门禁时，应保持 checker 接口简单，把并发、cache、预算与 aggregation 放外壳。

#### ⭐ 源码精读 3：Weir DSL 在构造时强制解析核心字段

固定源码：[`harper-core/src/weir/mod.rs`](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/harper-core/src/weir/mod.rs#L68-L164)

```rust
pub fn new(weir_code: &str) -> Result<WeirLinter, Error> {
    let ast = parse_str(weir_code, true)?;
    let resolved = resolve_exprs(&ast)?;
    let expr = resolved.get("main").ok_or(Error::ExpectedVariableUndefined)?;
    let description = ast.get_variable_value("description")
        .ok_or(Error::ExpectedVariableUndefined)?
        .as_string().ok_or(Error::ExpectedDifferentVariableType)?;
    let message = ast.get_variable_value("message")
        .ok_or(Error::ExpectedVariableUndefined)?
        .as_string().ok_or(Error::ExpectedDifferentVariableType)?;
    // parse becomes / strategy / kind / scope, then construct the linter
    Ok(linter)
}
```

逻辑摘要：规则不是自由 prose；缺 `main/description/message/becomes` 或类型错误都会构造失败。`scope` 限定 chunk/sentence，replacement strategy 限定 exact/match-case。规则契约比提示词“请检查这些问题”更可审计。

#### ⭐ 源码精读 4：规则源码与 optimizer flag 共同组成 bounded cache key

固定源码：[`harper-core/src/weir/parsing/stmt.rs`](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/harper-core/src/weir/parsing/stmt.rs#L16-L57)

```rust
pub fn parse_str(weir_code: &str, use_optimizer: bool) -> Result<Arc<Ast>, Error> {
    type ParseStrParams = (Arc<String>, bool);
    static PARSE_CACHE: LazyLock<RwLock<LruCache<ParseStrParams, Arc<Ast>>>> =
        LazyLock::new(|| RwLock::new(LruCache::new(NonZeroUsize::new(10000).unwrap())));
    // hit: clone Arc<Ast>; miss: lex → parse_stmt_list → optimize → cache
}
```

逻辑摘要：cache key 包含所有影响 AST 的参数，容量有界；缺 optimizer flag 会让同一规则的不同语义错误复用。对于 shared hub checker，应进一步把 engine version、rule pack hash、input hash 都纳入 evidence key。

#### 依赖分析与供应链风险

- `harper-core` 直接依赖 FST、Hashbrown、Itertools、SmallVec、regex、LRU、cached、ammonia、pulldown-cmark、Brill、可选 thesaurus，以及 `zip 8.6.0`（只启用 deflate）。
- Rust workspace 覆盖 LS、WASM、Python、desktop、浏览器/编辑器插件等多种发布面；每个 integration 有不同依赖和更新节奏，不能把 core 审计结论外推到所有插件。
- `ammonia` 说明 Markdown description 转 HTML 需要 sanitize；任何把 lint message/description 显示到 Web UI 的复用也要保留输出编码边界。
- 规则/词典更新非常频繁，deterministic 不等于永远正确；rule pack version 必须进入结果证据，且允许 disable/waiver。

#### 可复用经验

- **当质量要求可以确定性表达时，应优先把规则做成结构化 checker + fixture tests，再让 LLM 解释或修订，因为 deterministic finding 可复现、可定位、可缓存；边界是自然语言规则会有误报，必须允许配置和人工 waiver。**
- **当对大文档或频繁编辑做检查时，应优先按稳定 unit（chunk/sentence/file）和 config hash 缓存，而不是仅按全文路径缓存；边界是 cache 必须有容量、engine/rule version 和输入 content hash。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/local-report-quality-gate/` 对两个 fixture Markdown 做只读检查：标题章节完整、URL 格式、`待核验` 标记、禁止 secret-like pattern；输出 JSON `findings/status/rule_pack_hash/input_hash`。状态必须区分 `clean / findings / blocked / failed`，不安装 Harper 也能先验证 gate contract；之后才比较 Harper CLI/WASM 集成价值。

#### 风险边界

- **License**：仓库和 core 为 Apache-2.0；复制规则、字典或代码仍需 notice 和依赖 license 检查。
- **维护活跃度**：查询日前一天有 commit，最近 release 距查询日约一个月，活跃；API open issues count 为 687。
- **安全风险**：离线处理降低内容外泄，但插件/更新/词典下载链仍有供应链风险；Web 展示 lint description/message 时仍需 sanitize。近期 #3874 报告 memory leak，长驻 Hermes 守护进程集成前必须做 soak/resource test。
- **局限 / 不适用**：README 明确当前只支持 English；不能用它评价中文报告主体。Grammar lint 也不能证明技术事实、引用或安全结论正确。
- **性能声明边界**：README 声称毫秒级、低于 LanguageTool 1/50 内存，但本轮未 benchmark，故本机性能为**待核验**。

#### Skill 升格判断与 Hermes/shared hub 落地路径

- **Skill 升格判断：需二次验证。** “local deterministic report quality gate”跨 Agent 可复用，但今天仍只是 candidate；需先验证中文报告不会被误处理、blocked/failed 不会伪装 clean、资源上限和 waiver/evidence 契约，再判断是否升格。
- **Hermes/shared hub 落地路径**：
  1. POC 放 `runtime/hermes/github-learning-poc/local-report-quality-gate/`，只检查 fixture，不扫描 secret 文件；
  2. 首期规则用 Python/JSON 自有契约验证，若需要英文 grammar 再以独立 subprocess 包装 Harper，设置 timeout/memory limit；
  3. 结果写 `runtime/hermes/...`，报告只引用摘要；不把 cache/findings 全文写 curated；
  4. 若稳定，再候选新建 `capabilities/skills/quality/local-report-gate/` 并登记 manifest；skill 只写规则契约、验证命令与 pitfalls，不放每日输出；
  5. 自动门禁只阻止发布或提示人工审查，不自动改用户原文、配置、cron 或 secret。

---

## 横向对照

| 维度 | Buzz | LikeC4 | Harper | 对 shared hub 的启示 |
|---|---|---|---|---|
| 核心中间表示 | signed event + tenant/channel | parsed/computed/layouted model | Document + annotated Tokens + Lints | 原始 Markdown 之上应有带 schema/source/stage 的 runtime snapshot |
| 最终边界 | delivery chokepoint 重验 access | dev mutation RPC 与 production static model 分离 | Linter contract + bounded aggregation | 写入/发送前重验 scope/effect；查询与 mutation 分离 |
| 缓存身份 | `(community_id,event_id)` | project/stage/HMR module | unit hash + config hash；rule source + optimizer | cache key 必须含 agent/run/resource/schema/config/engine |
| 证据 | per-community canonical hash chain | source model + stage transitions | spans/suggestions/rule tests | evidence 要 canonical、可定位、带版本，不用 prose 自证 |
| 主要边界 | hash chain 非签名锚；系统面大 | writeback 有损；dev RPC 需安全外壳 | 英文限定；误报与 memory leak | candidate 先 POC，不自动进入 curated/shared skill |

## 经验沉淀

1. **当授权可能随时间变化时，应优先在最终发送或副作用执行点重验 `(actor, tenant/run, resource, effect)`，因为早期订阅/计划只能证明当时匹配；边界是查询失败必须 blocked/denied，不能默认放行。**
2. **当多个进程或 Agent 追加同一状态链时，应优先用 scope-derived serialization 与事务保护 head，再把 scope 编入 evidence hash；边界是 hash chain 若没有外部签名/锚定，只能检出部分篡改。**
3. **当数据会经历解析、计算、布局、摘要或治理时，应优先显式标注 stage/schema/source，而不是让 consumer 猜当前成熟度；边界是每个转换必须披露有损字段与 freshness。**
4. **当开发环境需要写回、生产或跨 Agent 消费只需查询时，应优先拆分 read snapshot 与 mutation RPC，并给每个工具声明 effect；边界是“方法有限”不等于已鉴权。**
5. **当规则可确定性表达时，应优先使用可测试 checker 做质量外壳，让 LLM 只处理模糊判断与解释；边界是 checker 失败必须返回 failed/blocked，空 findings 不能冒充 clean。**
6. **当结果需要缓存时，应优先让 key 覆盖 input content hash、scope、config/rule hash、engine/schema version，并设置容量与 deadline；边界是 path/name 不是内容身份。**
7. **当热门项目 license 为 `NOASSERTION`、GPL 或依赖图未审计时，应优先只抽象机制而不复制源码；边界是 GitHub API 的 license 字段也不能替代完整依赖 license review。**

## 可实践总实验

把三个项目的共同模式合并成一个不触碰真实配置的 30 分钟 fixture POC：

```text
runtime/hermes/github-learning-poc/trusted-check-pipeline/
├── fixtures/
│   ├── valid.md
│   ├── wrong-scope.md
│   └── invalid-schema.md
├── compile_model.py       # raw → parsed → computed，保留 source/hash
├── check_rules.py         # deterministic findings + four-state status
├── authorize_effect.py    # 在最终 output action 前重验 scope/effect
└── expected/
    ├── valid.json
    ├── wrong-scope.json
    └── invalid-schema.json
```

只生成 runtime JSON，不发送消息、不写 curated、不改 cron。验收点：wrong scope 必须 denied；invalid schema 必须 blocked；checker crash 必须 failed；只有 valid 且无 findings 才 clean；evidence key 含 input/rule/schema/scope hash。

## Skill 升格总判断

- **本日三个候选均为“需二次验证”，没有直接升格 shared skill。**
- 原因：Buzz 模式可能与现有 verification/governance 契约重叠；LikeC4 和 Harper 已在前一日报出现相近 candidate，需要先去重；三个项目均未在本机跑完整依赖/测试。
- 本轮只形成 candidate workflow：`trusted-check-pipeline`。完成 fixture POC、资源/副作用测试、治理去重后，才决定：
  - 更新已有 shared skill；
  - 新建 narrowly scoped skill 并更新 `capabilities/manifests/shared-skills.yaml`；或
  - 保留为 Hermes 本地 runtime 能力，不升格 shared。

## 明日继续

1. **最小动作**：实现 `runtime/hermes/github-learning-poc/trusted-check-pipeline/` 的 3 个 fixture 与 expected JSON，并真实运行；不接生产 inbox/curated。
2. 对 Buzz 模式补验证：测试 fail-closed、cross-scope cache poison、evidence canonicalization 与 timestamp round-trip。
3. 对 LikeC4 模式补验证：定义 `parsed/computed` JSON schema 和 stale snapshot 行为，记录 source location 与 transform diagnostics。
4. 对 Harper 模式补验证：先做自有 deterministic gate，再决定是否安装 CLI；重点复现 blocked/failed 与资源上限，不以“无 findings”掩盖工具未运行。
5. 若 POC 通过，运行 shared skill 去重审查；若未通过，保留 runtime 失败证据，不晋升。

## 候选反哺

### Candidate Facts

- [ ] topic: 最终副作用边界重验 scope 可减少 stale authorization 泄漏 | evidence: `block/buzz@264a56a` `handlers/event.rs::filter_fanout_by_access` | 建议: create | 安全级别: medium
- [ ] topic: hash preimage 必须先规范化为持久层 round-trip 精度 | evidence: `block/buzz@264a56a` `buzz-audit/src/hash.rs` 与修复提交说明 | 建议: create（先用本地 fixture 复现） | 安全级别: medium
- [ ] topic: 显式 parsed/computed/layouted stage 可防 consumer 误用未成熟模型 | evidence: `likec4/likec4@f970062` core model/compute-view | 建议: update 既有 architecture evidence candidate，避免重复 | 安全级别: low
- [ ] topic: deterministic checker 需要 input/config/rule/engine identity 与 bounded cache | evidence: `Automattic/harper@efa59c3` `LintGroup` / Weir parser cache | 建议: update 既有 local quality gate candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: trusted-check-pipeline | 可复用场景: GitHub 学习审计、共享记忆候选校验、未来 Agent 产物门禁 | 是否建议 shared: yes（仅 POC 通过后） | 原因: 融合 stage-aware model、deterministic checker、final effect authorization，避免三个重复小 skill
- [ ] 名称: scoped-delivery-gate | 可复用场景: 发送消息、写 curated、改配置前的最终 scope/effect 重验 | 是否建议 shared: no（当前） | 原因: 先验证与现有 config routing / governance skill 是否重复

### Candidate Open Questions

- [ ] 问题: shared hub 的 evidence 是否需要 HMAC/签名或外部 anchor，而不只是 SHA-256 chain？ | reason: adaptation | priority: high
- [ ] 问题: runtime compiled model 如何定义 stale、schema migration 和 source deletion？ | reason: gap | priority: high
- [ ] 问题: 中文报告只做结构/事实 gate、英文片段才交给 Harper，边界怎样自动且可解释地判定？ | reason: adaptation | priority: medium
- [ ] 问题: Buzz 旧审计行 re-anchor 的运营流程与证据连续性如何处理？ | reason: gap | priority: medium

### 不应自动落地

- 不自动修改 Hermes/OpenClaw 配置、provider、模型、cron、auth 或 secret。
- 不自动把本报告写为 curated active fact；Candidate Facts 必须经过评分、证据、去重、脱敏和治理审查。
- 不复制 `NOASSERTION` 或 GPL 项目源码进入 shared；Apache/MIT 源码也不因许可证宽松而跳过 notice/依赖审计。
- 不把 hash chain 宣称为不可伪造日志，不把 LikeC4 图宣称为真实架构本身，不把 Harper clean 宣称为事实正确。
- 不在未运行 checker、依赖安装失败或 schema invalid 时输出 clean；必须使用 blocked/failed。

## 产物索引

- 完整报告：`inbox/hermes/daily/2026-07-25-github-learning.md`
- 原始 API / README / release / issues 证据：`runtime/hermes/github-hot-project-learning/api/`
- 固定快照：`runtime/hermes/github-hot-project-learning/research/{buzz,likec4,harper}/`
- 项目卡片：`runtime/hermes/github-learning/projects/{block-buzz,likec4-likec4,Automattic-harper}.md`
- 累积经验：`runtime/hermes/github-learning/lessons.md`
