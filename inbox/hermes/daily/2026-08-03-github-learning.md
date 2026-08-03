# 2026-08-03 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> 研究时间：2026-08-03T07:31–07:42+08:00（GitHub API 数据最终复核约 2026-08-02T23:37Z）  
> 发现来源：真实抓取 `https://github.com/trending?since=daily`，并用 GitHub Search API 查询近期高星仓库；所有速览项目再以 `gh api repos/{owner}/{repo}` 单仓复核。  
> 固定源码快照：`kvcache-ai/AgentENV@1a39ba507272a891b749ccb141121c2dbfab0890`、`QoderAI/better-harness@8fa92b1613d69c94d62239ef5893318c179272a7`。  
> 数据边界：Stars、forks、updated/pushed 会继续变化；GitHub Repository API 的 license 只代表仓库级识别结果，不能替代依赖、模型、数据、镜像和发行制品审查。

## 今日结论

今天的主线是：**Agent 系统的“环境隔离”和“学习闭环”都必须把生命周期、证据身份、失败恢复与最终发布收进确定性外壳。** `AgentENV` 用显式 sandbox 状态、pause/resume rollback、内容寻址 artifact 与可禁用传输层承载大规模隔离环境；`better-harness` 用 episode/evidence contract、缺失证据状态、canonical source 与 staging→validate→publish 承载跨 coding-agent 的持续改进。对 Hermes/shared hub 最值得吸收的不是安装两个产品，而是把现有每日学习升级为 **evidence-bound learning episode + staged knowledge publication**：raw/runtime 可以宽进，只有绑定固定 revision、coverage、validation receipt 和目标 scope 的候选才能进入治理队列。

## 证据与执行摘要

- **Trending 真实抓取**：HTML 保存为 `runtime/hermes/github-hot-project-learning/trending-2026-08-03.html`，640,727 bytes；解析到 `microsoft/AI-For-Beginners`、`usekaneo/kaneo`、`lyogavin/airllm`、`iv-org/invidious`、`codecrafters-io/build-your-own-x`、`zhaoxuya520/reverse-skill`、`different-ai/openwork` 等。
- **增长项目补充**：GitHub Search API 查询 `created:>2026-07-15 stars:>100`，结果包含 `kvcache-ai/AgentENV`、`QoderAI/better-harness` 等；今日选它们深读，是因为一个覆盖隔离执行/快照/分布式 artifact，另一个直接覆盖多 host Agent 学习闭环，且与前一日 AOS/QM 不重复。
- **API 原始证据**：Repository、License、Releases、Issues、Pulls、Commits JSON 保存在 `runtime/hermes/github-hot-project-learning/api/2026-08-03/`。
- **源码**：两个仓库均真实 `git clone --depth 1`；tracked paths 分别为 **685** 和 **549**，写报告前工作树均干净。
- **交叉来源**：AgentENV 核验 README、`SECURITY.md`、architecture docs、release、issues/PR、Cargo/Go 依赖与关键 Rust 源码；Better Harness 核验 README、architecture/skill docs、PR、package lock、tests 与关键 JavaScript 源码。两者均未只依赖 README。
- **真实执行**：当前 WSL 无 Cargo/Rustc/Go、无 `/dev/kvm`、无 `/dev/ublk-control`，所以 AgentENV build/runtime 测试明确为 **blocked/待核验**；Better Harness 使用满足仓库 engine 的临时 Node 22.20.0 跑 6 个定向 test files，真实结果 **121 pass / 0 fail**，CLI help exit 0。
- **供应链检查**：Better Harness `npm ci` 安装 2 个依赖，`npm audit --omit=dev --package-lock-only` 返回 0 known vulnerabilities；本机默认 Node/npm 低于仓库最低版本并产生 EBADENGINE warning，测试改用 Node 22.20.0。两个仓库的 Dependabot alerts API 均返回 403，状态**待核验**，不能据此声称“无漏洞”。

## 项目速览

### A. GitHub Trending daily（Repository API 复核）

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 534,803 | 50,552 | Markdown | NOASSERTION | 2026-08-02T23:36:09 / 2026-07-14T19:25:58 | 超高星索引，但许可证未识别且不是源码机制主线 |
| [microsoft/generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners) | 114,748 | 61,282 | Jupyter Notebook | MIT | 2026-08-02T23:28:28 / 2026-08-01T08:23:49 | 高热教程，留给课程学习 lane |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 64,666 | 5,345 | Python | MIT | 2026-08-02T23:30:47 / 2026-07-25T10:20:07 | Agent 接入面大，今日不扩高权 surface |
| [microsoft/AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners) | 58,967 | 11,597 | Jupyter Notebook | MIT | 2026-08-02T23:37:04 / 2026-07-21T11:11:48 | Trending 首位，教程型而非运行时源码型 |
| [lyogavin/airllm](https://github.com/lyogavin/airllm) | 25,615 | 2,881 | Jupyter Notebook | Apache-2.0 | 2026-08-02T23:24:25 / 2026-07-29T01:08:32 | 分层推理候选，需 GPU/模型 license 专项复现 |
| [iv-org/invidious](https://github.com/iv-org/invidious) | 21,967 | 2,455 | Crystal | AGPL-3.0 | 2026-08-02T23:35:23 / 2026-08-02T22:26:07 | 活跃代理服务，AGPL/网络/内容边界高 |
| [different-ai/openwork](https://github.com/different-ai/openwork) | 20,294 | 2,087 | TypeScript | NOASSERTION | 2026-08-02T23:35:04 / 2026-08-02T21:48:27 | 热门 Agent workspace，但 license 未识别 |
| [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 13,309 | 1,993 | PowerShell | MIT | 2026-08-02T23:36:51 / 2026-08-02T15:45:28 | 逆向/Skill 攻防面高，不自动运行 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | 10,974 | 1,040 | TypeScript | NOASSERTION | 2026-08-02T23:36:22 / 2026-07-29T15:59:52 | 记忆候选，但 license 未识别且 open items 多 |
| [usekaneo/kaneo](https://github.com/usekaneo/kaneo) | 6,119 | 515 | TypeScript | MIT | 2026-08-02T23:28:10 / 2026-08-02T07:13:12 | 项目管理工具，和今日学习闭环主线较弱 |

### B. 近期增长项目补充（深读对象）

| 项目 | Stars | Forks | Language | License（GitHub API） | Created / Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [kvcache-ai/AgentENV](https://github.com/kvcache-ai/AgentENV) | **2,773** | 216 | Rust | **MIT** | 2026-07-23 / 2026-08-02T23:11:20 / 2026-08-01T07:10:12 | **深读：状态化 sandbox、快照恢复、内容寻址 artifact、可选 P2P** |
| [QoderAI/better-harness](https://github.com/QoderAI/better-harness) | **1,450** | 118 | JavaScript | **MIT** | 2026-07-21 / 2026-08-02T23:36:25 / 2026-08-02T04:33:45 | **深读：evidence episode、缺失证据、跨 host adapter、staged publish** |

说明：`pushed_at` 是仓库级活动字段，可能由非默认分支/PR 更新，不能替代固定 `main` commit；Stars 不是成熟度、采用率或安全证明。

## 深读项目

### 1. kvcache-ai/AgentENV

**基本信息（GitHub API）**

- URL：https://github.com/kvcache-ai/AgentENV
- Stars：**2,773**；Forks：**216**；Language：Rust；License：**MIT**。
- 创建：2026-07-23T02:48:07Z；updated：2026-08-02T23:11:20Z；pushed：2026-08-01T07:10:12Z；`open_issues_count=52`（含 PR，不能解释为 52 个缺陷）。
- 固定 default-branch commit：[1a39ba507272](https://github.com/kvcache-ai/AgentENV/commit/1a39ba507272a891b749ccb141121c2dbfab0890)，commit time 2026-08-01T07:01:58Z，message `fix(sandbox): isolate envd bootstrap connections across generations`。
- 最新 GitHub Release：[v0.1.0](https://github.com/kvcache-ai/AgentENV/releases/tag/v0.1.0)，published 2026-07-25T11:20:12Z；固定源码比 release 新。
- Repository/License API 均识别根许可证为 MIT；依赖、Firecracker/OverlayBD、OCI 镜像、工具镜像和部署物仍需另审。

#### 一句话判断

AgentENV 值得学的不是“50ms resume”这个 README 指标，而是它把 **VM lifecycle、持久 paused state、层叠 filesystem/memory snapshot、exact-range artifact transport、node heartbeat/binding 和明确部署安全缺口**放进同一套可审计架构；这为长任务 Agent 的环境 checkpoint/continuation 提供了状态与证据层面的参考。

#### 解决的问题：替代了什么旧做法

1. 替代每次 Agent 任务都从容器冷启动、重装工具和重建环境的做法。
2. 替代“pause 只是一个布尔字段”的做法，用 `Creating/Running/Pausing/Paused/Resuming/...` 明确中间状态和并发 join。
3. 替代把文件快照和内存快照都塞进单个巨大镜像的做法：rootfs 使用 overlaybd 层，内存 diff 也形成独立只读层并可共享 page cache。
4. 替代在 scheduler 中转储 artifact bytes/locator 的做法：scheduler 只给 peer hint，artifact catalog 与 bytes 保持 node-to-node。
5. 替代“optional backend 不存在也返回成功数据”的做法：disabled P2P 的 discovery 是 no result、fetch 是明确错误，只有 best-effort publish 是 no-op success。
6. 替代 crash 后盲目恢复中间态的做法：持久 record 区分 paused/resuming；启动时遗留 `Resuming` 被视为不安全记录并清理。

边界：AgentENV 是高权宿主基础设施，需要 KVM、ublk、network namespaces、iptables、mount 与 privileged DaemonSet；它自己明确**没有内置 API authorization**，不能因为使用 Firecracker 就推断整个控制面安全。

#### 架构 / 实现与数据流

```text
Client / E2B-compatible API
        │
        ▼
Axum API ──> per-node Orchestrator ──> Sandbox lifecycle state machine
                                       │
                                       ├─ Firecracker VM + envd
                                       ├─ NetworkManager / namespaces / policy
                                       └─ UblkDeviceManager
                                              │ Unix socket RPC
                                              ▼
                                      uvm-ublk-daemon
                                      ├─ rootfs / extra drive ublk
                                      └─ memory snapshot ublk
                                              │
                                              ▼
                                      overlaybd layer stack
                                      ├─ immutable lower layers
                                      ├─ writable upper
                                      └─ local/registry/tar backend

optional distributed plane:
Gateway ──gRPC──> Scheduler (node/binding hints) ──> AgentENV nodes
                                           └────── P2P peer discovery only
Artifacts: node catalog/P2P/object store; scheduler does not proxy bytes
```

核心数据流：API 调用先由 orchestrator CAS-like transition 到中间状态；pause 先保护 runtime image refs、detach route/handle、分配 artifact root、调用 backend snapshot、持久化 paused record，最后停止 VM；resume 则把 paused record 标为 resuming，重建 backend，失败时回滚内存 store 与 durable lifecycle。Storage 侧 overlaybd 把 immutable lower + writable upper 暴露成 ublk；内存 diff snapshot 同样变成只读 ublk 层，多个同源 resume 复用 page cache。

#### Repo tree 摘要

```text
AgentENV/                                      # fixed commit tracked paths: 685
├── README.md / SECURITY.md / LICENSE         # 产品边界、部署警告、MIT
├── Cargo.toml / Cargo.lock                   # 19 workspace members、Rust 主依赖图
├── src/
│   ├── api/                                  # Axum/OpenAPI 与 proxy endpoints
│   ├── orchestrator/                         # lifecycle、store、persistence、metrics
│   ├── sandbox/                              # Firecracker、network、ublk、envd
│   ├── snapshot/ / template/                 # committed artifacts 与 user-facing builder
│   ├── p2p/                                  # disabled/iroh transport、peer discovery
│   └── observability/                        # node identity、heartbeat、metrics projection
├── storage/
│   ├── overlaybd/                            # LSMT layers、backend、compression、snapshot
│   ├── ublk/ / ublk-daemon/                  # block device server 与 daemon RPC
│   ├── util/                                 # io_uring worker、ID allocator
│   └── uffd-core/                            # 参考实现，未进 workspace build
├── services/                                 # Go prototype gateway + scheduler
├── crates/                                   # CLI、benchmark、warm pool、observability 等
├── thirdparty/                               # generated Firecracker/envd clients
├── config/ / deploy/ / scripts/              # 依赖 manifest 与部署/构建
├── docs/src/internals/architecture.md        # 真实模块和数据流说明
└── tests/                                    # unit/integration/orchestrator tests
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/orchestrator/types.rs` | lifecycle vocabulary | 8 个显式状态与 lifecycle event type，避免 pause/resume 被压成布尔值 |
| `src/orchestrator/service.rs` | 最终 lifecycle chokepoint | conditional transition、并发 pause join、artifact pin、detach/restore、persist/resume rollback |
| `src/orchestrator/persistence/file_backed.rs` | durable paused record | versioned record、Paused/Resuming lifecycle、RocksDB durability、orphan cleanup |
| `src/digest.rs` | artifact identity | 同一 stream 同时计算 byte count + SHA-256，避免 size/hash 来自不同读取 |
| `src/p2p/transport.rs` | optional acceleration contract | lookup/fetch/range/publish/unpublish；short range 不可 silent success；disabled semantics |
| `storage/overlaybd/src/image/image_file.rs` | layered block image | upper/lower read-write、snapshot and restack 的高层入口 |
| `src/sandbox/ublk/device.rs` | device lifecycle bridge | node 侧 singleton 通过 daemon client 管理 ublk devices |
| `services/scheduler/` | prototype placement/bindings | heartbeat roster、TTL、node lookup；binding 仍是内存态 |
| `SECURITY.md` | threat/deployment boundary | 明确无 built-in API auth，要求 trusted network 或 auth proxy |

#### 源码精读（固定 commit）

**代码块 1：状态枚举把执行中间态暴露为一等语义**  
来源：[`src/orchestrator/types.rs#L56-L66`](https://github.com/kvcache-ai/AgentENV/blob/1a39ba507272a891b749ccb141121c2dbfab0890/src/orchestrator/types.rs#L56-L66)

```rust
#[derive(Clone, Debug, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SandboxState {
    Creating,
    Resuming,
    Running,
    Snapshotting,
    Forking,
    Pausing,
    Paused,
    Killing,
}
```

逻辑：`Pausing`、`Snapshotting`、`Resuming` 与 `Killing` 不是日志字符串，而是 store 中可做 transition conflict 判断的状态。`pause_sandbox` 遇到另一个 `Pausing` 会 join，而不是重复执行。边界是 enum 本身不保证所有 side effect 都事务化；源码仍有跨 store、route、VM、artifact root 的补偿路径。

**代码块 2：pause 先做条件 transition，并区分并发 join 与非法状态**  
来源：[`src/orchestrator/service.rs#L978-L1018`](https://github.com/kvcache-ai/AgentENV/blob/1a39ba507272a891b749ccb141121c2dbfab0890/src/orchestrator/service.rs#L978-L1018)

```rust
pub async fn pause_sandbox(self: &Arc<Self>, sandbox_id: SandboxId) -> Result<()> {
    let this = Arc::clone(self);
    self.run_lifecycle_operation("pause", sandbox_id, async move {
        this.pause_sandbox_inner(sandbox_id).await
    }).await
}

async fn pause_sandbox_inner(self: &Arc<Self>, sandbox_id: SandboxId) -> Result<()> {
    match self.store
        .update_state_if_state(
            &sandbox_id,
            SandboxState::Pausing,
            &[SandboxState::Running],
        ).await
    {
        Ok(_) => {}
        Err(StoreError::StateConflict { actual_state, .. }) => {
            return match actual_state {
                SandboxState::Pausing => self.join_concurrent_pause(sandbox_id).await,
                SandboxState::Paused => Ok(()),
                SandboxState::Killing => Err(OrchestratorError::SandboxNotFound(sandbox_id)),
                _ => Err(OrchestratorError::InvalidSandboxState {
                    sandbox_id,
                    state: actual_state,
                }),
            };
        }
        Err(err) => return Err(OrchestratorError::from(err)),
    }
    // protect refs, detach route, allocate artifact root, pause, persist, stop follow
}
```

逻辑：状态变更先于昂贵 snapshot；同一 sandbox 的 concurrent pause 被合流；已 paused 是幂等 success；正在 kill 返回 not found。边界是后续 artifact allocation、backend pause、persistence、stop 跨多个资源，依赖补偿而非单数据库事务；[issue #99](https://github.com/kvcache-ai/AgentENV/issues/99) 与 open [PR #100](https://github.com/kvcache-ai/AgentENV/pull/100) 正在修复 allocation failure 后留在 `Pausing` 的问题，说明状态机设计仍有真实缺口，不能写成已解决。

**代码块 3：持久态给 resume 加 intent marker，crash 后不盲目复用**  
来源：[`src/orchestrator/persistence/file_backed.rs#L21-L55`](https://github.com/kvcache-ai/AgentENV/blob/1a39ba507272a891b749ccb141121c2dbfab0890/src/orchestrator/persistence/file_backed.rs#L21-L55) 与 `#L263-L267`

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
enum PersistedPausedLifecycle {
    Paused,
    Resuming,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct PersistedPausedRecord {
    version: u32,
    lifecycle: PersistedPausedLifecycle,
    metadata: SandboxMetadata,
    artifact_root: PathBuf,
    state: Value,
}

// During load_all:
if record.lifecycle == PersistedPausedLifecycle::Resuming {
    self.cleanup_invalid_record(&sandbox_id).await?;
    continue;
}
```

逻辑：durable record 除 metadata/state 外还带 schema version 与 resume intent；进程在 resume 中崩溃后，下一次启动不把可能已部分消费/变异的 paused artifact 当安全 continuation，而是清理。正常 launch rollback 会调用 `rollback_resuming`。边界是这是一种保守 at-most-once 恢复策略，可能牺牲可恢复工作；cleanup 本身失败也需要被视为 operation failure。

**代码块 4：optional P2P 的每个操作有不同 disabled 语义**  
来源：[`src/p2p/transport.rs#L14-L69`](https://github.com/kvcache-ai/AgentENV/blob/1a39ba507272a891b749ccb141121c2dbfab0890/src/p2p/transport.rs#L14-L69) 与 `#L75-L109`

```rust
#[async_trait]
pub trait P2pTransport: Send + Sync {
    async fn lookup_with_hints(
        &self,
        key: &P2pArtifactKey,
        hints: &[P2pArtifactProviderHint],
    ) -> Result<Option<P2pArtifactDescriptor>>;

    async fn fetch(&self, descriptor: &P2pArtifactDescriptor, destination: &Path)
        -> Result<u64>;

    async fn fetch_byte_range(
        &self,
        descriptor: &P2pArtifactDescriptor,
        offset: u64,
        len: usize,
    ) -> Result<P2pByteStream>;

    async fn publish(&self, request: &P2pPublishRequest) -> Result<()>;
}
```

逻辑：lookup、whole-file fetch、in-memory fetch、exact range、publish 都是独立 contract；range 必须产出恰好 `len`，short read 必须 error。Disabled backend 的 lookup 返回 `None`、fetch 返回 `TransportDisabled`、publish 返回 `Ok(())`，因为 publishing 只是 acceleration。边界是 no-op success 仅适用于 best-effort advertise，绝不能推广到 required fetch/validation；P2P provider hints 也不是内容完整性，仍需 key/digest 验证。

#### 依赖分析与供应链风险

- 根 Rust workspace 声明 **19 members**；`Cargo.lock` 解析出 **842 packages**：821 registry、1 git source、20 workspace/path。
- 根 `Cargo.toml` 有 67 个 direct dependencies，核心包括 Tokio、Axum、Reqwest、OpenDAL S3、RocksDB、tonic/prost、nix/netlink、io-uring、overlaybd、ublk、iroh/iroh-blobs。
- 唯一 git dependency 是 `libublk-rs-sys 0.1.0`，固定到 commit `c6a3e069...`。Pin 降低 floating HEAD 风险，但 commit 来源、构建脚本和上游账号仍需审查。
- `services/go.mod` 要求 Go 1.25.0；直接依赖 gRPC/protobuf、Prometheus、Redis、Kubernetes client-go 等。Rust 与 Go 双生态扩大 CVE/license/build provenance 面。
- `thirdparty/` 含生成 client；`config/deps_manifest.toml`、工具镜像、Firecracker、OverlayBD、`regctl`、`umoci` 与 OCI registry 都进入供应链。
- Dependabot API 403，alerts 状态待核验；没有把 lockfile 固定或 release 存在等同于无漏洞。

#### README / docs / release / issues 交叉核验

- README 的 Firecracker + overlaybd + ublk + snapshot/fork 结构与 `docs/src/internals/architecture.md`、repo tree 和代码路径一致。
- README/SECURITY 都明确当前无 API authorization，要求 trusted network 或外部 auth proxy；这是部署硬边界，不是“未来可能有”的小缺点。
- v0.1.0 早于固定 commit；默认分支已包含 release 后修复，不能把 main 的行为外推给 release binary。
- [issue #102](https://github.com/kvcache-ai/AgentENV/issues/102) 描述 sandbox generation 间复用 envd bootstrap connection 可导致 snapshot restore stall；固定 commit 对应 [PR #103](https://github.com/kvcache-ai/AgentENV/pull/103) 已 merged，说明 generation isolation 是真实修复。
- [issue #99](https://github.com/kvcache-ai/AgentENV/issues/99) 指出 allocation failure 可留在 Pausing；[PR #100](https://github.com/kvcache-ai/AgentENV/pull/100) 截至查询仍 open，不得写成已修复。
- [issue #97](https://github.com/kvcache-ai/AgentENV/issues/97) 指出 malformed OverlayBD index metadata 在 allocation 前缺 bounds validation；[PR #98](https://github.com/kvcache-ai/AgentENV/pull/98) 仍 open，说明 hostile/corrupt image metadata 是现实 DoS/内存风险。
- [PR #104](https://github.com/kvcache-ai/AgentENV/pull/104) 提议 snapshot commit marker 写失败应返回 error 而非 panic，截至查询仍 open。

#### 真实测试结果

```text
$ cargo --version
cargo: command not found
$ rustc --version
rustc: command not found
$ go version
go: command not found
$ test -e /dev/kvm; echo $?
1
$ test -e /dev/ublk-control; echo $?
1
```

准确结论：当前 cron WSL 环境**无法编译 Rust/Go workspace，也无法运行 Firecracker、ublk、network namespace、pause/resume、snapshot、P2P 或 distributed control plane**。源码存在 tests、上游 CI badge 或 README benchmark 都不能替代本机运行证据；性能与隔离声明均待受控硬件环境复现。

#### 可复用经验

- 当长任务 Agent 需要 pause/resume 时，应优先把中间态、intent marker、并发 join、terminal failure 与 rollback 分开，因为布尔 `paused` 无法表达“正在暂停时谁拥有副作用”；边界是跨 VM/store/filesystem 的恢复仍需补偿测试。
- 当 runtime artifact 可从 object store、P2P 或本地 cache 获取时，应优先用稳定 logical key + byte length + content digest，并让 exact-range short read 失败，因为 locator/peer hint 不是内容身份；边界是无签名 digest 不证明发布者可信。
- 当某 backend 只是加速层时，应优先逐操作声明 disabled semantics，而不是统一 fail-open 或 fail-closed，因为 discovery miss、required fetch 与 best-effort publish 的正确结果不同；边界是 required path 不可被 no-op success 掩盖。
- 当 crash 发生在 continuation 恢复中间时，应优先保守标记并拒绝盲目重放可能被消费的 snapshot，因为“存在 record”不等于“状态仍一致”；边界是保守清理可能损失可恢复工作，需要 retention/forensics receipt。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/evidence-bound-continuation/` 做纯 Python 离线 fixture（今日只设计，不接 KVM）：

1. schema：`run_id, state, intent, artifact_key, size, digest, generation, owner, transition_revision, fallback_state`。
2. fixtures：Running→Pausing→Paused、concurrent pause join、artifact allocation fail→Running、Paused→Resuming crash→Blocked、range short read→Failed、optional publish disabled→Completed-without-acceleration。
3. validator 拒绝 transition 没有 expected previous state、required artifact 没有 size+digest、resuming crash 仍直接 completed。
4. 把 GitHub learning prepare/report/audit/KB copy 映射为类似状态，验证 report 写入和 KB 发布不是同一个 terminal receipt。
5. 不安装 Rust/Firecracker，不改 Hermes config/provider/auth/cron，不调用 OpenClaw。

#### 风险边界

- **License**：repo MIT；Rust/Go dependencies、Firecracker、OverlayBD、tools/OCI image、generated clients 与部署物另审。
- **维护活跃度**：固定 main commit 距查询约两天，issues/PR 活跃；但仓库创建约 11 天、仅 v0.1.0、open items 52，接口和恢复语义仍快速变化。
- **安全风险**：项目控制 KVM、ublk、network namespace、iptables、mount、registry/object-store/P2P credentials；任一输入验证缺口都接近宿主边界。
- **明确缺口**：没有内置 API auth；scheduler bindings 在内存中；open issue/PR 暴露 Pausing rollback、OverlayBD bounds、snapshot panic 等未完成修复。
- **隔离边界**：Firecracker 降低 guest→host 风险，不自动解决 API authorization、cross-sandbox artifact identity、page-cache exposure、registry provenance 或 DoS。
- **运行局限**：本机无 toolchain/KVM/ublk，未复现任何 benchmark、snapshot、fork、warm pool、P2P 或 cluster behavior。
- **不适用场景**：shared hub 是文件型知识/能力中台，不应为了吸收 lifecycle contract 而引入 privileged microVM 集群。
- **不可自动执行**：不运行 install script、不 `--setup-host`、不改 sysctl/iptables/groups/systemd、不下载未知镜像、不暴露 API、不创建集群。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`evidence-bound continuation state + optional acceleration semantics`，可补强 Hermes 长任务/cron/artifact 的状态和 receipt。
- **需验证**：先以纯离线 fixtures 验证 transition revision、expected prior state、generation、artifact size/digest、rollback 和 terminal receipt；再与现有 subagent 四状态、completion contract、scoped authority/effect-scope 候选去重。
- **暂不沉淀**：AgentENV 产品安装、Firecracker/ublk/overlaybd/P2P implementation、性能参数与部署脚本；本机没有 runtime 证据且高权依赖过重。
- **今日动作**：只提 candidate；不创建 shared skill，不写 curated active fact，不导入上游源码。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/evidence-bound-continuation/{schema.json,fixtures/,validate.py,test_transitions.py,README.md}`。
2. **GitHub learning status 候选**：扩展 runtime status 为 `prepared → researching → report_written → audited → published`，每步带 `attempt, input_revision, artifact_path, artifact_hash, terminal_state`；不是只靠 `overall_status`。
3. **shared 分层映射**：clone/API/stdout 留 runtime；完整研究留 inbox；KB copy 是 projection；curated/skill promotion 是另一条人工/治理 gated transition。
4. **Hermes cron 候选**：遇到依赖/审批缺失时返回 blocked + resume condition，不把无人值守任务提升到更高自治。
5. **共享能力候选**：若 POC 通过，优先更新既有 completion/subagent-state/verification 类 skill，不创建 AgentENV 产品集成 skill。
6. **跨 Agent**：共享中立 schema/fixtures；各 agent 只实现自己的 adapter。当前任务不调用 OpenClaw，也不修改任何 agent 配置。

---

### 2. QoderAI/better-harness

**基本信息（GitHub API）**

- URL：https://github.com/QoderAI/better-harness
- Stars：**1,450**；Forks：**118**；Language：JavaScript；License：**MIT**。
- 创建：2026-07-21T12:30:35Z；updated：2026-08-02T23:36:25Z；pushed：2026-08-02T04:33:45Z；`open_issues_count=4`（含 PR）。
- 固定 default-branch commit：[8fa92b1613d6](https://github.com/QoderAI/better-harness/commit/8fa92b1613d69c94d62239ef5893318c179272a7)，commit time 2026-08-01T14:54:11Z，message `Merge pull request #50 from QoderAI/fix/asset-inventory-designated-user-home`。
- GitHub Releases API 返回空数组：**暂无 GitHub Release**；`package.json` version 为 0.4.0，不能把 package version 等同于已核验 release。
- Repository/License API 与 `package.json` 均为 MIT；npm tarball、host plugin package 和依赖仍需独立验证。

#### 一句话判断

Better Harness 值得学的不是它的评分模板，而是它把跨 coding-agent 的观察拆成 **provider-labelled evidence bundle、task episode、evidence ref、coverage/unknown、lead-only reconciliation、canonical report source、deterministic projection、staging validation 与原子 publication**；这正是每日学习从“写一篇长文”走向可验证闭环所缺的中间契约。

#### 解决的问题：替代了什么旧做法

1. 替代把不同 host 的 raw session、项目状态和 Agent assets 混成一个 prompt 的做法，改为三个独立 evidence lanes。
2. 替代从“同一 session 跑过 test”推断“此次 edit 已验证”的做法，要求 episode、顺序和 reviewed relevance。
3. 替代缺失证据时填 0 分或猜测 clean 的做法，保留 partial/unavailable/unobserved/unknown。
4. 替代直接从 AI prose 生成多种展示物的做法：canonical source/findings 先冻结，再 deterministic projection 到 HTML/Markdown/Canvas。
5. 替代直接写最终目录的做法：先写 staging、验证 expected artifact set，再 rename publish，失败保留/恢复旧版本。
6. 替代每个 host 自己复制业务判断的做法：host shells/adapters 薄，product judgment 留在 skill/scripts/models/templates canonical owners。

边界：项目极新、没有 GitHub release；它能检查证据契约和报告一致性，但不能自动证明用户目标正确、测试全面、生产部署安全或一次 intervention 已产生长期效果。

#### 架构 / 实现与数据流

```text
Qoder / Claude / Codex / Cursor / Qwen / Copilot host
                         │ thin adapter / plugin metadata
                         ▼
              evidence-bundle / session-analysis
         ┌───────────────┼──────────────────┐
         ▼               ▼                  ▼
  Session Evidence  Project Harness   Agent Customize
  task episodes      repo evidence     assets/integrity
         └───────────────┼──────────────────┘
                         ▼
               Lead reconciliation only
         findings + score + evidence boundary
                         ▼
             canonical report source/findings
                         ▼
             deterministic render/projection
       Markdown / HTML / Qoder Canvas / Cursor Canvas
                         ▼
            stage → validate → atomic publish
```

关键机制：session events 只有在 stable invocation id + lifecycle phase 下才合并；validation 必须发生在 edit 后且被 reviewed 为 relevant 才能关闭 episode；report source 把 delivery evidence 分级；renderer 固定 target/topology、检查 artifact set、在临时目录生成和验证，然后 rename 到最终 run dir。

#### Repo tree 摘要

```text
better-harness/                                # fixed commit tracked paths: 549
├── README.md / LICENSE / AGENTS.md            # 产品入口、MIT、工程规则
├── package.json / package-lock.json           # Node/npm engine、2 个 runtime deps
├── skills/better-harness/
│   ├── SKILL.md                               # 五步 evidence/reconcile/render 契约
│   └── references/                            # lane、finding、support、fix contracts
├── scripts/
│   ├── better-harness.mjs                     # thin root CLI facade
│   ├── session-analysis/                      # events、episodes、facets、privacy、providers
│   ├── harness-analysis/                      # source、quality、render、review、projection
│   ├── workspace-topology/                    # frozen target/package scope
│   ├── coding-agent-practices/                # asset inventory/integrity
│   └── packaging/ / npm-package/              # host/package validation
├── models/                                    # Agent Work Loop 与 harness model
├── templates/                                 # canonical report/style contracts
├── hooks/                                     # lifecycle adapter templates
├── .{claude,codex,cursor,qoder}-plugin/        # thin host shells
├── docs/ARCHITECTURE.md / adrs/ / specs/      # ownership和 contract decisions
└── test/                                      # 80+ test files；今日定向跑 6 个
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `scripts/session-analysis/episode-contract.mjs` | event→episode semantic model | lifecycle dedupe、task key、edit/validation relevance、closure、repair candidate |
| `scripts/session-analysis/privacy-safe-text.mjs` | evidence minimization | 去 injected context、secret/path/id redaction、bounded summaries |
| `scripts/harness-analysis/report-source/source.mjs` | canonical report schema/validation | evidence levels、coverage states、permission summaries、safe target/output contracts |
| `scripts/harness-analysis/render-report.mjs` | deterministic projection chokepoint | frozen topology、output scope、staging、artifact set validation、atomic publish/rollback |
| `scripts/harness-analysis/report-quality.mjs` | evidence-aware quality gate | required sections、static-only score cap、unverified/session boundary、repair/schedule gates |
| `scripts/workspace-topology/` | target identity | requested workspace 与 package/member route freeze，阻止 output 绑定错目标 |
| `skills/better-harness/SKILL.md` | workflow contract | 三 independent lanes、lead-only final judgement、durable report authorization boundary |
| `docs/ARCHITECTURE.md` | ownership map | capability-owned module、thin facade、machine-safe CLI、plan-before-mutation |

#### 源码精读（固定 commit）

**代码块 1：lifecycle event 只有 stable invocation id 才可合并**  
来源：[`episode-contract.mjs#L148-L194`](https://github.com/QoderAI/better-harness/blob/8fa92b1613d69c94d62239ef5893318c179272a7/scripts/session-analysis/episode-contract.mjs#L148-L194)

```javascript
export function deduplicateLifecycleEvents(events = []) {
  const groups = new Map();
  const ungrouped = [];

  for (const event of deduplicatePromptSubmissionEvents(events)) {
    const invocation = event?.toolInvocationId ?? event?.requestId ?? event?.callId ?? null;
    const phase = event?.lifecyclePhase ?? null;
    if (!invocation || !phase || !["pre", "request", "post", "result"].includes(phase)) {
      ungrouped.push(event);
      continue;
    }
    const key = `${event.sessionId ?? "unknown"}:${invocation}`;
    const group = groups.get(key) ?? [];
    group.push(event);
    groups.set(key, group);
  }
  // choose result > post > first; preserve request fields and all evidence refs
  return [...ungrouped, ...merged].sort(compareEvents);
}
```

逻辑：时间接近、工具名相同都不足以合并；必须有 session-scoped invocation identity 和 recognized phase。合并时最终 result/post 提供 outcome，request/pre 补充 target/command，evidence refs 保留。边界是来自 host 的 invocation id 仍需可信 adapter；没有 id 的事件宁可不 dedupe，会保守重复计数而不是错误压缩。

**代码块 2：同一 session 的 test 不自动关闭 edit episode**  
来源：[`episode-contract.mjs#L348-L357`](https://github.com/QoderAI/better-harness/blob/8fa92b1613d69c94d62239ef5893318c179272a7/scripts/session-analysis/episode-contract.mjs#L348-L357) 与 `#L428-L450`

```javascript
function validationIsRelevant(change, validation) {
  if (validation?.reviewedAssociation === true || validation?.relevance === "relevant") return true;
  return false;
}

function closureFor(episode, changeSets, validationSets) {
  if (changeSets.length === 0) {
    return { status: "not-applicable", reason: "no-edit-observed", relevantValidationCount: 0 };
  }
  const latestChange = changeSets.at(-1);
  const relevant = validationSets.filter((validation) => {
    if (!validationOccursAfterChange(latestChange, validation)) return false;
    return validationIsRelevant({ affectedPaths: latestChange.paths }, validation._event);
  });
  if (relevant.length === 0) {
    return { status: "unobserved", reason: "no-relevant-validation-observed", relevantValidationCount: 0 };
  }
  const passed = relevant.filter((validation) => validation.status === "passed");
  return { status: passed.length > 0 ? "closed" : "observed-without-pass" };
}
```

逻辑：验证必须在 latest change 之后，并且显式 reviewed relevant，才进入 closure；没有证据返回 `unobserved`，不是 failed 也不是 passed。测试 `episode contract does not turn an unrelated same-session test into closure` 今日真实通过。边界是人工/adapter relevance 标记本身可能错，需要路径、check identity 和 reviewer evidence继续约束。

**代码块 3：renderer 固定 target/topology，再在 staging 中验证并发布**  
来源：[`render-report.mjs#L350-L415`](https://github.com/QoderAI/better-harness/blob/8fa92b1613d69c94d62239ef5893318c179272a7/scripts/harness-analysis/render-report.mjs#L350-L415) 与 `#L437-L471`

```javascript
export async function renderReport(options) {
  const inputCount = [options.findings, options.source, options.sourceData]
    .filter((value) => value !== undefined && value !== null).length;
  if (inputCount !== 1) throw Object.assign(
    new Error("provide exactly one of --source or --findings"),
    { code: "INVALID_RENDER_INPUT" },
  );

  const topology = options.topology
    ?? (options.target ? (await resolveWorkspaceTopology({ workspace: options.target })).topology : undefined);
  // realpath target must match frozen topology; structured package findings require complete topology

  stageDir = await mkdtemp(path.join(parentDir, `.${path.basename(runDir)}.staging-`));
  await writeArtifacts({ reportData, artifactDir: stageDir, runDir });
  validation = options.validate ? await validateArtifacts(/* ... */) : null;
  if (validation?.status === "fail") throw validationError(validation);
  await publishStagedRun(stageDir, runDir);
}
```

逻辑：恰好一个 canonical input；有 structured target 时要求 target；realpath 必须匹配 frozen topology；输出先进入同 parent staging，validator 检查 expected/missing/unexpected artifacts 和内容，再 rename 发布。若已有 run dir，publish 会先移到 backup；rename 失败时尝试 rollback。边界是 rename atomicity 只在同 filesystem/正常 FS 语义下成立；删除 backup 的 best-effort failure 可能留垃圾，需要 cleanup/receipt，但不能因此把 publish 报成未发生。

**代码块 4：私有文本先去注入块，再做 secrets/path/ID 最小化**  
来源：[`privacy-safe-text.mjs#L52-L80`](https://github.com/QoderAI/better-harness/blob/8fa92b1613d69c94d62239ef5893318c179272a7/scripts/session-analysis/privacy-safe-text.mjs#L52-L80)

```javascript
export function sanitizePrivateReviewText(value, { limit = 800 } = {}) {
  if (!value) return null;
  const maximum = Math.max(24, Number(limit) || 800);
  const text = String(value)
    .replace(MARKDOWN_IMAGE_RE, " ")
    .replace(MARKDOWN_LINK_RE, "$1")
    .replace(/\b(?:authorization\s*:\s*)?bearer\s+[A-Za-z0-9._~+\/-]{8,}\b/giu, "Bearer <redacted>")
    .replace(/\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+/giu, "$1=<redacted>")
    .replace(/\b(?:sk|ghp|github_pat|xox[abprs])[-_][A-Za-z0-9_-]{8,}\b/giu, "<secret>")
    .replace(/(^|[^\p{L}\p{N}_])\/(?:Users|home|var|private|tmp|opt)\/[^\s"'`<>]+/gmu, "$1<path>")
    .replace(/\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/giu, "<id>")
    .replace(/\s+/gu, " ").trim();
  if (!text) return null;
  return [...text].length <= maximum ? text : `${[...text].slice(0, maximum).join("")}…`;
}
```

逻辑：只输出 bounded review summary，剥离图片目标、链接 URL、常见 bearer/key/token、绝对路径和 UUID；`prepareTaskInput` 还会移除 injected environment/skill/tool context，防止把系统上下文误当用户事实。边界是 regex redaction 永远不完备，未知 secret 格式、自然语言 PII、base64/blob 仍可能泄露；因此最安全的默认仍是不要加载 raw session/body。

#### 依赖分析与供应链风险

- `package.json` version 0.4.0；Node engine `>=22.20.0 <25.0.0`，npm `>=10.9.3 <12.0.0`。
- runtime dependencies 只有 `@vscode/tree-sitter-wasm 0.3.1` 与 `esbuild-wasm 0.28.1`；lockfile 共 3 package entries（含 root），两个 tarball 均来自 npm registry 且有 integrity。
- `publishConfig.provenance=true` 是发布意图，但本次没有 GitHub Release，也未下载 npm published tarball 验证 attestation，因此发布 provenance **待核验**。
- 多 host plugin metadata、Skill、hook、HTML/Canvas render 会被多个 harness 读取；低依赖不等于低权限，安装后的 prompt/skill/hook 本身就是 supply-chain surface。
- `npm ci` 在默认 Node 22.14/npm 10.9.2 下成功但有 EBADENGINE；不能据此声称默认环境受支持。定向 tests 使用临时 Node 22.20.0。
- `npm audit` 0 findings 只覆盖当前 npm advisory DB/lockfile，不覆盖 prompt injection、host adapter、WASM parser、generated HTML 或非 npm assets。Dependabot API 403，状态待核验。

#### README / docs / PR 交叉核验

- README 声称不是 one universal entrypoint，而是 host-specific adapters；repo 确有多个 plugin roots，`docs/ARCHITECTURE.md` 要求 host shell 薄、business logic 留 capability owner。
- `skills/better-harness/SKILL.md` 要求三条 independent evidence pass、lead-only severity/score、缺 lane 在 normal mode 阻断；`report-source/source.mjs` 的 schema/coverage validator与此一致。
- [PR #50](https://github.com/QoderAI/better-harness/pull/50) 于 2026-08-01 merged，对应固定 main commit，修复 Claude designated config workspace inventory。
- [PR #49](https://github.com/QoderAI/better-harness/pull/49) merged，新增 Cursor Canvas route；repo 中确有 `.cursor-plugin` 和 Cursor renderer/test。
- [PR #48](https://github.com/QoderAI/better-harness/pull/48) merged，加入 recurring-correction candidate；源码中存在 learning capture/episode mechanisms。
- [PR #44](https://github.com/QoderAI/better-harness/pull/44) “read-only lifecycle control plane” 截至查询 open，不得写成已发布能力。
- [PR #51](https://github.com/QoderAI/better-harness/pull/51) 与 [PR #52](https://github.com/QoderAI/better-harness/pull/52) 仍 open；safe aliases/Grok adapter 都不能外推为当前 main 支持。
- 仓库没有 `SECURITY.md`；这不证明无安全政策，也不证明不安全，只能记录为 repo-level dedicated policy 未发现，漏洞报告/支持边界待核验。

#### 真实测试与审计结果

```text
$ npm ci
added 2 packages, and audited 3 packages in 4s
found 0 vulnerabilities
# 同时出现 EBADENGINE：系统 Node 22.14.0/npm 10.9.2 低于仓库最低版本

$ npx --yes node@22.20.0 --test \
    test/session-episode-contract.test.mjs \
    test/harness-report-run.test.mjs \
    test/harness-report-quality.test.mjs \
    test/session-analysis-time.test.mjs \
    test/learning-loop-contract.test.mjs \
    test/better-harness-skill.test.mjs

# tests 121
# pass 121
# fail 0
# duration_ms 1575.544699

$ npx --yes node@22.20.0 scripts/better-harness.mjs --help
exit=0
```

覆盖：Skill 主契约、episode relevance/dedupe、report analyze 不写入、report quality、Learning Capture states、session timestamp。准确边界：

- 只跑 6 个 test files 的 121 tests，不是整个 549-path repo 的完整 `npm test`。
- 没有运行真实 Qoder/Codex/Claude/Cursor session collection，没有读取用户 home/memory/raw transcripts。
- 没有运行 HTML/Canvas preview/playwright、host plugin install、npm pack/publish、provenance 或真实 report mutation。
- npm audit 0 不是完整供应链或 prompt/hook 安全证明。

#### 可复用经验

- 当多个 Agent/host 提供 session evidence 时，应优先用 provider-labelled versioned lane 与 stable invocation/task identity，再做 lead reconciliation，因为时间邻近和相似 prose 不能证明同一事件；边界是 adapter identity 仍需 conformance tests。
- 当 edit 之后出现任意 test 时，应优先要求 episode 内顺序 + reviewed relevance + pass receipt，不能把 same-session test 当 closure，因为测试可能针对无关路径；边界是 relevance review 也需要 bounded evidence。
- 当报告要投影为 Markdown/HTML/Canvas/知识库时，应优先冻结 canonical source，再在 staging 生成、验证 expected artifact set 后原子发布，因为直接多写目标会产生半新半旧状态；边界是跨 filesystem/外部 API 发布需更强 transaction/receipt。
- 当 session evidence 不完整时，应优先保留 unavailable/partial/unobserved 与 coverage，而不是补零或猜 clean，因为 absence of observation 不是 negative observation；边界是状态太多也要有清晰 machine contract。
- 当证据可能包含用户 prompt、secret、路径和 ID 时，应优先不读取 raw body；必须摘要时才做最小化、redaction 和长度上限，因为 regex sanitization 不是完整 DLP；边界是未知格式仍可能漏出。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/learning-episode-envelope/` 构建离线 parser（今日只设计）：

1. 将 GitHub 调研工具事件规范化为 `source_attempt, repo, revision, event_id, phase, artifact_ref, result_state`。
2. episode 以 `(date, runner, repo, revision)` 绑定，API metadata、clone、docs、source、test 分成独立 evidence lanes。
3. closure 只有在报告写入后、audit 针对同一路径/日期且 score receipt 存在时才为 completed；KB copy 是后续 projection receipt。
4. fixtures 覆盖 API 403、clone success/test blocked、report stale revision、audit unrelated file、KB copy failure、raw evidence redaction。
5. 全程使用 synthetic/historical records，不读取真实 secret/session，不修改 cron/config/curated。

#### 风险边界

- **License**：repo MIT；npm dependencies、WASM assets、host plugin packages、templates 与 generated report assets另审。
- **维护活跃度**：固定 main commit 很新，多个 PR 于 8 月 1 日 merged；但仓库创建约 13 天、无 GitHub release、open PR 仍改变 host/alias/control-plane contract。
- **安全风险**：Skill/prompt/hook/plugin 会影响 coding-agent 行为；session evidence、memory metadata、user home 与 report output 都可能含隐私或改变工作区。
- **证据风险**：deterministic validator 只能验证已编码 contract，不能判断遗漏的业务目标、隐藏 production failure 或恶意 evidence provider。
- **redaction 局限**：regex 不覆盖所有 secret/PII；摘要仍可能泄露语义，默认不应采集未授权 raw session/memory body。
- **发布局限**：staging+rename 是本地 FS contract，不等于 remote publish transaction；cleanup/backup residue 和 concurrent writer 仍需 lock/revision。
- **运行局限**：只跑 121 个定向 tests；未运行完整 suite、真实 host、Canvas/HTML preview、package publish。
- **不适用场景**：shared hub 已有 reflection/audit/governance，不应复制整个 Better Harness product/评分体系形成第二套真相源。
- **不可自动执行**：不安装 plugin/skill/hook，不扫描用户 session/home/memory，不生成生产报告，不执行 finding fix，不修改 Hermes/OpenClaw 配置或 cron。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`learning episode envelope + canonical-source staged publication + explicit evidence coverage`，直接适用于 GitHub learning/reflection/governance。
- **需验证**：先在当前日报历史上做 read-only fixtures，证明日期/runner/repo/revision/audit path/KB projection identity 一致；再与现有 GitHub learning、self-reflection、verification-first、governance skills 去重。
- **暂不沉淀**：Better Harness 整个 Skill、host plugins、Canvas render、评分模型、session collectors 与 repair workflow；它们的 scope/authority 和本地系统不一致。
- **今日动作**：只提 candidate，不复制 `SKILL.md`/源码，不更新 shared skill manifest，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/learning-episode-envelope/{schema.json,fixtures/,normalize.py,validate.py,test_episode.py,README.md}`。
2. **orchestrator adapter**：`scripts/github_learning_orchestrator.py` 后续可生成 machine-readable `evidence-manifest.json`，记录每源 attempted/state/items/detail/fixed revision；报告仍由 Hermes 撰写。
3. **审计绑定**：audit receipt 至少带 `date, runner, report_path, report_hash, score, issues, audited_at`，防止无关/旧报告被误认完成。
4. **KB projection**：知识库 copy 带 source hash 与 destination receipt；projection 失败不能改写 report/audit 成功，但 overall publication 状态应可区分。
5. **shared governance**：完整 evidence/raw 留 runtime/inbox；candidate 只进入 pending review；经过评分、证据、去重、脱敏、人工/总控 gate 后才写 curated/capabilities。
6. **跨 Agent adapter**：中立 schema 可给 future-agent；每个 host 只负责 evidence adapter。当前任务不调用 OpenClaw；未来若存在也必须独立授权与测试。

## 横向对照：隔离执行与学习闭环共享同一种可靠性骨架

| 层次 | AgentENV | Better Harness | Hermes/shared hub 候选 |
|---|---|---|---|
| identity | SandboxId + generation + node | provider/session/invocation/task/target | date + runner + repo + fixed revision + report path |
| lifecycle | Creating/Running/Pausing/Paused/Resuming/Killing | event phases、task episode、coverage states | prepared/researching/report_written/audited/published/blocked |
| artifact | overlaybd/snapshot/P2P key + digest + size | evidence refs + canonical source + expected artifact set | API JSON/clone/report/audit/KB receipt + hash |
| optional path | P2P publish best-effort，fetch required | partial lane lowers confidence/blocks normal mode | source 403/blocked 不冒充 clean；optional discovery 与 required audit 分开 |
| publication | persisted paused record / snapshot commit | stage→validate→rename，backup rollback | inbox report→audit receipt→KB projection→governance candidate |
| crash handling | resuming intent record，遗留中间态保守清理 | staging cleanup / old run backup restore | interrupted step 保留 attempt/error/resume condition，不直接 completed |
| hard boundary | host/KVM/ublk/network + missing API auth | evidence/authority contract，不能证明生产正确 | tool API、filesystem、cron manager、governance/approval gate |

## 经验沉淀

1. 当任务可以 pause、resume、retry 或 crash 时，应优先把中间态、owner、intent、expected prior state 与 rollback 写入结构化状态，因为一个 `running/completed` 布尔值无法表达谁拥有副作用；边界是状态枚举仍需跨资源补偿测试。
2. 当多个来源或 host 描述同一事件时，应优先用 stable invocation/task/revision identity 合并，并保留 source refs，因为时间接近、工具名相同或 prose 相似不能证明同一事实；边界是 source adapter 自己也要被验证。
3. 当 artifact 经 cache、P2P、object store 或知识库 projection 传播时，应优先绑定 logical key、byte size、content hash 与 scope，因为 locator 和路径只说明“去哪里找”；边界是无签名 hash 不证明发布者身份。
4. 当验证出现在 edit 之后时，应优先检查是否属于同一 episode、同一 target 且显式 relevant，再决定 closure，因为 same-session pass 可能完全无关；边界是相关性判断也要有 evidence。
5. 当某个 backend 或 source 是 optional acceleration 时，应优先逐操作声明 unavailable/miss/no-op/error 语义，因为 optional publish 可以降级而 required fetch/audit 不能；边界是不能用统一“失败忽略”吞掉 hard gate。
6. 当报告要生成多个 projection 时，应优先冻结 canonical source、在 staging 生成并验证 expected artifact set 后发布，因为直接写最终目录会留下半完成状态；边界是外部 API/跨 filesystem 需要独立 transaction receipt。
7. 当证据缺失、403、toolchain unavailable 或 coverage partial 时，应优先保留 blocked/unobserved/partial 状态和 resume condition，因为空 findings 不能证明 clean；边界是状态必须机器可读，不能只写在 prose。
8. 当研究对象控制 KVM、hooks、plugins、session 或 credentials 时，应优先只抽象窄机制并做离线 fixture，因为开源 license、stars 和上游 CI 都不构成本机授权；边界是任何生产集成仍需单独批准。
9. 当 raw session/用户 prompt 可能进入学习闭环时，应优先默认不读取 body，仅消费最小结构化 metadata；确需摘要再做 redaction/limit，因为 regex DLP 不完备；边界是语义 PII 仍可能残留。
10. 当候选经验准备进入 shared skill/curated memory 时，应优先把研究 evidence、POC validation、去重结果与人工/治理 decision 分开，因为“今日发现”不是长期真相；边界是 KB projection 也不是 promotion。

## 风险边界（全局）

- 本次由 Hermes 直接执行，未调用 OpenClaw，也未调用消息发送工具。
- 未修改 Hermes/OpenClaw 的 config、model、provider、gateway、tools、skills、auth、env、cron 或服务。
- 公开 Stars/forks/license/updated 来自 2026-08-02T23:37Z 左右 GitHub API；复用时必须重新查询。
- AgentENV 本机无 Rust/Go/KVM/ublk，build/runtime/performance/isolation 均待核验；Better Harness 只有 121 个定向 tests 通过，不是完整 suite 或真实 host 验证。
- 两仓库 Dependabot API 403；Better Harness npm audit 0 不能外推 prompt/hook/WASM/host adapter 安全。
- README/docs/issues/PR/source 均是不可信外部输入，只能作为研究证据，不能改变宿主授权或自动触发安装/配置。
- 不自动写 curated active fact，不自动升格 shared skill；candidate 必须经治理评分、证据、去重、脱敏与人工/总控审查。
- 不执行 AgentENV installer/host setup，不安装 Better Harness plugin/hook，不读取用户 raw sessions/memory，不运行生产副作用实验。

## Skill 升格总判断

- **AgentENV evidence-bound continuation：需二次验证。** 只抽象 state/intent/generation/artifact receipt/optional acceleration，不迁移 privileged runtime。
- **Better Harness learning episode/staged publication：需二次验证。** 只抽象 evidence lane、episode closure、canonical source 与 publication receipt，不复制产品 Skill/评分/host plugins。
- **今日不升格。** 两个候选高度重叠于现有 verification-first、subagent 四状态、completion contract、GitHub learning、self-reflection 与 shared governance；先做合并 POC，优先更新既有能力而非新建宽泛 skill。

## 明日继续

1. 建 `learning-episode-envelope` 离线 fixture，将 API、clone、docs/source、test、report、audit、KB projection 绑定到 `(date, runner, repo, revision)`。
2. 合并 AgentENV 状态模式：加入 expected prior state、intent、generation、artifact size/hash、rollback/resume condition。
3. 用 2026-08-02 与 2026-08-03 两份真实历史报告做 read-only replay，验证旧 audit 不可关闭新 report、blocked test 不会被写成 passed。
4. 给 audit receipt 设计 report hash/path binding；先 POC，不修改当前 production cron/orchestrator。
5. 如受控环境具备 Rust/KVM/ublk，再运行 AgentENV unit tests；不为无人值守日报自动安装系统 toolchain 或修改 host。
6. 对 Better Harness 补跑完整 `npm test` 和 pack verify；只有资源允许时做，不安装 host plugin，不读取真实 session。
7. 跟进 AgentENV PR #98/#100/#104 与 Better Harness PR #44/#51/#52；只在 merge commit/test/release 有真实变化后更新候选事实。

## 候选反哺

### Candidate Facts

- [ ] topic: learning-completion-needs-episode-and-artifact-identity | evidence: Better Harness episode relevance/closure + AgentENV state/generation/artifact digest | 建议: create/update after offline replay | 安全级别: high
- [ ] topic: optional-acceleration-must-have-per-operation-semantics | evidence: AgentENV disabled P2P lookup/fetch/publish 不同结果 | 建议: update completion/source-outcome contract after fixture | 安全级别: medium
- [ ] topic: canonical-source-should-precede-multiple-projections | evidence: Better Harness report source + staging/expected artifact set/rename publish | 建议: candidate for KB/governance projection | 安全级别: medium
- [ ] topic: validation-must-be-bound-to-change-episode | evidence: Better Harness `closureFor` + 真实 test `unrelated same-session test` 通过 | 建议: update verification fact after Hermes mapping | 安全级别: high
- [ ] topic: continuation-crash-needs-intent-marker | evidence: AgentENV Paused/Resuming persisted lifecycle + startup conservative cleanup | 建议: candidate，先验证 Hermes interrupted run semantics | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: evidence-bound-learning-episode | 可复用场景: GitHub learning、调研、reflection、audit、KB projection | 是否建议 shared: yes（验证后更新既有 skill） | 原因: 跨 Agent 横切，但应合并现有 GitHub learning/verification，不新建重复宽 skill
- [ ] 名称: staged-knowledge-publication | 可复用场景: inbox→audit→KB→curated/skill promotion | 是否建议 shared: yes（治理与 POC 后） | 原因: canonical source/receipt/rollback 可减少半完成和错误晋升
- [ ] 名称: agentenv-product-integration | 可复用场景: microVM Agent sandbox | 是否建议 shared: no | 原因: privileged/KVM/ublk/network surface，本机无 runtime evidence
- [ ] 名称: better-harness-product-integration | 可复用场景: coding-agent workflow audit | 是否建议 shared: no | 原因: 与本地 reflection/governance 重叠，host/session authority 不一致

### Candidate Open Questions

- [ ] 问题: 当前 `github_learning_orchestrator.py` 如何把 audit receipt 绑定到 report hash，而不破坏兼容路径？ | reason: adaptation/security | priority: high
- [ ] 问题: KB copy 失败时 overall status 应是 audit-completed/publish-partial 还是整体 failed？ | reason: state-model | priority: high
- [ ] 问题: API source 403、README unavailable、test blocked 分别是 optional lane 还是 required lane，规则应由谁声明？ | reason: governance | priority: high
- [ ] 问题: shared hub 在不记录 raw session 的情况下，能否用最小 event envelope证明“同一 change episode 的 relevant validation”？ | reason: privacy/adaptation | priority: high
- [ ] 问题: AgentENV 遗留 Resuming record 直接清理的 at-most-once 选择，对高价值长任务是否需要 quarantine 而非 delete？ | reason: recovery trade-off | priority: medium
- [ ] 问题: staging+rename 遇到跨文件系统知识库路径时，需要 manifest commit 还是双写 receipt？ | reason: portability/atomicity | priority: high

### 不应自动落地

- 不运行 AgentENV install/setup-host/server，不修改 KVM/ublk/sysctl/iptables/systemd/group，不暴露其无 auth API。
- 不安装 Better Harness Skill/plugin/hook，不读取真实 Qoder/Codex/Claude/Cursor session、用户 home 或 memory body。
- 不修改 Hermes/OpenClaw config、model、provider、tools、skills、auth、env、cron；不调用 OpenClaw。
- 不把今日 candidate 直接写入 curated active fact 或 shared manifest；先做 runtime POC、历史 replay、治理评分、去重、脱敏与人工/总控审查。
