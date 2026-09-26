---
type: case
status: archived
created: 2026-09-26
updated: 2026-09-26
domain: learning
tags: [github-learning, sandbox, capability-boundary, continual-learning, candidate-publication]
---

# 2026-09-26 GitHub 热门项目学习报告

> 执行者：Hermes；本次未调用 OpenClaw。  
> 查询与验证时间：2026-09-26 07:41–07:55（UTC+08:00）。发现口径包括 GitHub Search API `created:>=2026-08-26 archived:false stars:>500 sort:stars` 与 `stars:>5000 pushed:>=2026-09-19 archived:false sort:updated`；Stars 是查询时快照。  
> 深读固定提交：`pydantic/monty@dd5307d15e80a57ba4fceecfe6ea472e6b5f4a85`（release `v1.0.0`）；`Human-Agent-Society/reef@ecec4e20b29e7dcbd96150d4b4f1a80b146e120d`（release `v0.1.1`）。源码结论只绑定这些 revision。  
> 真实来源：GitHub Repository/Search/Commit/Release/Issues/Actions/License/Security Advisories API，README、docs、lockfiles/manifests、关键源码与本机定向 tests/lint。clone 位于 shared runtime，完整 API 快照与测试日志也仅留 runtime。

## 今日结论

**安全的 Agent 自我改进不能把“生成候选”直接等同于“获得执行权”：不可信代码应在 capability-deny-by-default 的解释器边界暂停并由宿主显式恢复；不可信经验应先成为带稳定身份的 candidate，再经版本化 evaluator/selector、不可变发布链与人工门禁，最后才进入可服务状态。**

### 今日真实验证摘要

- `pydantic/monty`：固定 main commit；本机 `cargo test -p monty --lib` 实报 **45 passed / 0 failed**。固定 commit 的 GitHub check-runs 共 69 条，Rust/Python/JS/WASM、Miri、fuzz、lint 等主要 checks success，3 个 release jobs skipped。
- Monty 最新 release `v1.0.0` 发布于 `2026-09-25T08:27:46Z`。其安全文档明确它是 **language-level sandbox，不是 OS-level sandbox**；Python/JS 本地 API 以 worker subprocess 加 crash isolation，但 Rust `monty` crate 可 in-process，远端 WebSocket peer 的隔离属性也不能由客户端假定。
- Monty issue #939 在 `v1.0.0` 后报告 `cargo install monty-runtime` 因 `salsa` 解析漂移编译失败；本机用提交内 `Cargo.lock` 的 workspace test 成功，不等于 registry 安装问题已解决。issue #872 记录 type-check context 与解释器 namespace 在异常/import 后可能漂移。
- `Human-Agent-Society/reef`：固定 main commit；创建 Python 3.12 venv 并按仓库依赖安装后，定向运行 artifact、candidate-evaluation、records 三组测试，实报 **51 passed / 0 failed**；关键四文件 `ruff check` 返回 **All checks passed**。
- Reef 固定 commit 的 GitHub check-runs 共 13 条：source/package/sandbox tests、lint、docs、build、PyPI 与 GitHub release success，1 个 wake job skipped。release `v0.1.1` 与 main head 同日，仓库仍处在 `0.1.x` 高速演进期。
- 两仓库公开 Security Advisories API 均返回空数组；Dependabot alerts API 因当前 token 无管理权限返回 **HTTP 403**，所以不能声称“无依赖漏洞”。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) | 34,981 | 3,010 | Go | Apache-2.0 | 2026-09-25T22:50:14Z | 高活跃分布式存储，后续可读一致性/故障恢复 |
| [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | 24,624 | 2,123 | Python | Apache-2.0 | 2026-09-25T11:35:32Z | typed decision，历史已深读 |
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 20,239 | 1,371 | Python | MIT | 2026-09-25T04:06:12Z | 快速决策模型，历史已深读 |
| [pydantic/monty](https://github.com/pydantic/monty) | 8,299 | 422 | Rust | MIT | 2026-09-25T11:22:52Z | **深读：capability sandbox / suspension boundary** |
| [jaredpalmer/kev](https://github.com/jaredpalmer/kev) | 7,014 | 414 | Python | Apache-2.0 | 2026-09-25T23:53:07Z | 自托管 typed decision 家族，候选观察 |
| [zai-org/ZCode](https://github.com/zai-org/ZCode) | 6,770 | 2,029 | TypeScript | Apache-2.0 | 2026-09-24T06:49:55Z | durable workflow，昨日已深读 |
| [Human-Agent-Society/reef](https://github.com/Human-Agent-Society/reef) | 5,155 | 452 | Python | Apache-2.0 | 2026-09-25T16:53:44Z | **深读：候选评估、版本发布与持续改进闭环** |
| [NVlabs/SoL-Pi](https://github.com/NVlabs/SoL-Pi) | 3,078 | 241 | TypeScript | MIT | 2026-09-25T23:24:25Z | auto-research loop，后续候选 |

> 表中 Stars、Forks、Language、License、时间均来自 2026-09-26 GitHub Repository API。License 是仓库根识别结果，不覆盖依赖、数据、模型、远端服务、release assets 或商标；Stars 与近期 push 也不等于生产成熟度。

## 深读项目

### 1. pydantic/monty

- **一句话判断**：值得学的是“无 ambient authority 的语言解释器 + typed suspension + host-owned capability dispatch + subprocess crash boundary”，而不是把任意 Python、宿主回调或远端 worker 笼统称为安全沙箱。
- **解决的问题**：替代“每次 LLM 代码都启动容器”或“在宿主 CPython 中用禁用 builtins 黑名单”的旧做法；将 Python 子集解析/编译/执行放入 Rust VM，文件、网络、环境与外部函数默认不存在，只有宿主显式提供 capability 才能触达。
- **URL / API 快照**：https://github.com/pydantic/monty ；**Stars: 8,299 / Forks: 422 / Language: Rust / License: MIT**；`created_at=2023-05-28T11:13:38Z`，`updated_at=2026-09-25T23:02:44Z`，`pushed_at=2026-09-25T11:22:52Z`，API `open_issues_count=120`（含 PR）。
- **固定提交 / release**：[`dd5307d15e80a57ba4fceecfe6ea472e6b5f4a85`](https://github.com/pydantic/monty/commit/dd5307d15e80a57ba4fceecfe6ea472e6b5f4a85)，commit time `2026-09-25T10:28:32Z`；release [`v1.0.0`](https://github.com/pydantic/monty/releases/tag/v1.0.0) published `2026-09-25T08:27:46Z`。
- **来源交叉核验**：Repository/Commit/Release/Issues/Checks/License/Security Advisories API；README；`docs/security.md`；Cargo/Python manifests 与 lockfiles；`run.rs`、`run_progress.rs`、resource、mount table 源码；本机 Cargo test。

#### 架构 / 实现与数据流

```text
untrusted Python source
  -> Ruff parser / Monty compiler
      source nesting cap + bytecode + intern tables
  -> MontyRun / VM
      no ambient fs/env/socket/process capability
      + ResourceTracker(time/memory/recursion)
  -> RunProgress
      Complete
      FunctionCall | OsCall | NameLookup | ResolveFutures
          -> serialize/suspend snapshot
          -> host validates typed request + scope + limits
          -> optional MountTable(cap-std descriptor / mode / quota)
          -> host returns value/error/pending future
          -> resume VM
  -> Python/JS local pool
      worker subprocess + empty environment + untrusted wire decoder
  -> result / trusted snapshot store
```

核心不是“拦截危险 Python API”，而是解释器根本不实现 ambient authority。VM 遇到外部函数、OS call 或 future 时返回带 snapshot 的 typed `RunProgress`；真正有权限的宿主在边界上验证请求并决定 resume。文件系统单独放在 host-side `monty-fs`，mount 根目录先打开成 capability descriptor，后续操作相对该 descriptor 执行，而不是仅靠字符串 `..` 检查。

#### repo tree 摘要

固定 commit 共 **1,409 tracked files**：

```text
monty/
├── crates/
│   ├── monty/                # parser/compiler/bytecode VM/heap/run/snapshot
│   ├── monty-types/          # wire object、OS call、resource/exception contracts
│   ├── monty-fs/             # host-side capability mounts / overlay / path policy
│   ├── monty-pool/           # worker pool、subprocess/remote transport
│   ├── monty-proto/          # parent-child protocol与allocation budget
│   ├── monty-python/         # Python bindings/client/session驱动
│   ├── monty-js/             # Node/browser bindings
│   ├── monty-runtime/        # worker/CLI runtime
│   ├── monty-type-checking/  # ty/Ruff-based type checking
│   └── monty-wasm-runtime/   # browser/Node worker runtime
├── packages/pydantic-monty/  # Python metapackage，exact pin client/runtime 1.0.0
├── docs/                     # security、limits、snapshots、quickstarts
├── examples/                 # web scraper / SQL / class wrapper demos
├── Cargo.toml / Cargo.lock   # Rust workspace + resolved graph
├── pyproject.toml / uv.lock  # Python tooling + resolved graph
└── README.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/monty/src/run.rs` | VM 公共执行入口 | `MontyRun::new/run/start`；编译后创建 heap/VM，执行到完成或 suspension；OS policy/cwd 显式注入 |
| `crates/monty/src/run_progress.rs` | capability suspension 协议 | typed `FunctionCall/OsCall/ResolveFutures/NameLookup/Complete`；每种状态只暴露匹配的 resume API |
| `crates/monty-types/src/resource.rs` | 资源预算 | feed/turn execution time、memory、recursion、suspension、sleep；明确哪些是 host-enforced |
| `crates/monty-fs/src/mount_table.rs` | 文件系统 capability router | longest-prefix mount、host directory descriptor、交叠 mount 拒绝、rename 同 mount 限制、写入/memory quota |
| `crates/monty-fs/src/lib.rs` | trust boundary 声明 | `monty` interpreter 不依赖真实 fs；sandbox 只能请求，host 才执行 |
| `docs/security.md` | 权威安全边界 | language-level vs OS-level、callbacks/remote/snapshot/resource 的弱化点与安全要求 |
| `packages/pydantic-monty/pyproject.toml` | Python 发行边界 | client/runtime exact pin `1.0.0`；Python 3.10–3.14；MIT |

#### ⭐ 源码精读

**代码块 1：`MontyRun::start()` 只运行到 typed suspension/complete，再将 VM 状态封装为进度。**

```rust
pub fn start(
    self,
    inputs: Vec<MontyObject>,
    resource_tracker: ResourceTracker,
    print: PrintWriter<'_>,
) -> Result<RunProgress, MontyException> {
    let mut executor = self.executor;
    let mut heap = Heap::new(executor.namespace_size(), resource_tracker);
    let globals = executor.empty_globals();
    let (converted, vm_state) = HeapReader::with(
        &mut heap,
        &mut (&mut executor, print),
        |reader, (executor, print)| {
            let mut vm = VM::new(globals, &mut executor.tables,
                &executor.program, reader, print.reborrow());
            populate_inputs(inputs, &mut vm)?;
            let vm_result = vm.run_external();
            let converted = convert_frame_exit(vm_result, &mut vm);
            let vm_state = check_snapshot_from_converted(&converted, vm);
            Ok((converted, vm_state))
        },
    )?;
    build_run_progress(converted, vm_state, executor, heap)
}
```

逻辑摘要：执行权与外部 authority 被拆开；VM 自己只跑 bytecode，遇到外部边界就返回进度和 snapshot，宿主决定下一步。边界：直接用 Rust `monty` crate 是 in-process，语言级隔离仍在，但 native crash isolation 不在；生产更推荐 `monty-pool`。

**代码块 2：`RunProgress` 把暂停原因建模为封闭 variant，而不是字符串工具调用。**

```rust
pub enum RunProgress {
    FunctionCall(FunctionCall),
    OsCall(OsCall),
    ResolveFutures(ResolveFutures),
    NameLookup(NameLookup),
    Complete(MontyObject),
}

pub fn resume(
    self,
    result: impl Into<ExtFunctionResult>,
    print: PrintWriter<'_>,
) -> Result<RunProgress, MontyException> {
    self.snapshot.run(result, print)
}
```

逻辑摘要：每种 suspension 持有执行 snapshot，并只暴露匹配的 resume 操作；`call_id`、typed args、source position 可供宿主做 correlation/audit。边界：typed call 不自动安全；宿主函数与 `os=` callback 在 host process 中拥有完整权限，必须按不可信参数验证。

**代码块 3：资源限制区分 VM 可执行预算与必须由宿主执行的预算。**

```rust
pub struct ResourceLimits {
    pub max_feed_duration: Option<Duration>,
    pub max_turn_duration: Option<Duration>,
    pub max_memory: Option<usize>,
    pub gc_interval: Option<usize>,
    pub max_recursion_depth: usize,
    pub max_suspensions: usize,
    pub max_total_sleep: Option<Duration>,
}

pub fn max_memory(mut self, limit: usize) -> Self {
    self.max_memory = Some(limit);
    self
}
```

逻辑摘要：feed time 跨一次 feed 的多个 turn 累积；turn time 每次 resume 重置；host suspension 时间不计入 execution clock；recursion/suspension 默认有界。边界：`max_memory` 只有安装并 arm `monty-alloc` 才生效，否则源码明确会 silent not enforced；suspension 与 total sleep 也要求 host enforcement，触发 memory/time 后 session 应丢弃。

**代码块 4：mount 在插入时拒绝同一 host tree 的交叠 capability，并按 longest prefix 路由。**

```rust
pub fn push_mount(&mut self, mount: Mount) -> Result<(), MountError> {
    if let Some(existing) = self.mounts.iter()
        .find(|existing| mounts_overlap(existing, &mount)) {
        return Err(MountError::OverlappingMounts { /* identities */ });
    }
    let insert_at = self.mounts.partition_point(
        |existing| existing.virtual_path().len() > mount.virtual_path().len()
    );
    self.mounts.insert(insert_at, mount);
    Ok(())
}
```

逻辑摘要：不允许把同一 host directory tree 以不同 mode 暴露而形成弱权限旁路；nested virtual paths 只有在 host directories 不交叠时允许。每个 mount 用 `cap_std::fs::Dir` 固定根 descriptor。边界：配置 mount 的宿主本身是可信方；hard link/bind mount 等恶意 host state 不在 sandbox 对抗边界内。

#### 依赖分析与供应链风险

- workspace 要求 Rust `1.96`、edition 2024，版本 `1.0.0`；`Cargo.lock`、`uv.lock`、JS `package-lock.json` 均已提交。核心 `monty` 的直接依赖包括 Ruff parser/AST/codegen `0.0.14`、Serde、postcard/CBOR、hashbrown/indexmap、bigint、regex、chrono/jiff、jiter、sha2 等。
- workspace 明确把 Ruff/ty 系列统一 pin 到 `0.0.14`，但 `salsa = 0.28.2` 是 semver 范围；issue #939 显示 registry 安装解析到 `salsa 0.28.5` 时与 `ruff_python_ast 0.0.14` 不兼容。这说明 lockfile 保护 checkout 构建，不一定保护 `cargo install` 的独立解析。
- Python metapackage exact pin `pydantic-monty-client==1.0.0` 与 `pydantic-monty-runtime==1.0.0`，优于松散组合；但 runtime 仍含预编译 worker binary，需校验来源并显式 pin path，不能让不可信 `PATH` 决定沙箱 binary。
- GitHub 公开 advisories 为空；Dependabot alerts 因 403 无法核验。空 advisories 不是无漏洞证明，本次也没有运行 `cargo audit` 或对 release wheels/npm assets 做 SBOM/签名验证。
- 本机只跑 core lib 单元测试 45/45；未跑完整 workspace、Miri/fuzz、Python/JS/WASM bindings、mount adversarial tests、remote worker、release wheel/npm/crate 安装。上游 fixed commit checks success只能作为补充证据。

#### 可复用经验

- 当执行 LLM 生成代码时，应优先让高权能力在语言里“根本不存在”，再通过 typed suspension 逐项授予，因为黑名单式禁用 builtins 很难覆盖反射、FFI 与新 API；边界是宿主 callbacks 仍拥有完整 authority。
- 当沙箱需要文件访问时，应优先把 mount 根固化为 capability descriptor 并拒绝交叠 host tree，而不是只做字符串路径归一化，因为 rename/symlink/TOCTOU 会绕过词法检查；边界是恶意宿主与预存 bind/hard-link state 仍在信任侧。
- 当资源限制跨 VM 与宿主时，应优先逐项声明 enforcement owner 和 hard backstop，因为配置字段存在不代表实际生效；特别是 memory allocator、suspensions、sleep、request deadline 必须分别验证。
- 当持久化执行 snapshot 时，应优先验证 producer、version 与 MAC/signature 后再恢复，因为成功 decode 不能证明状态安全；边界是受信 producer 运行不可信 Python 产生的 snapshot 可以保存，但 bytes 不能被篡改。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/typed-capability-suspension-v0/` 建纯 Python fake VM，不安装 Monty：输入脚本只会返回 `Complete | FunctionCall | FsCall | Blocked`；host registry 对每个 capability 校验 `run_scope / effect / args_schema / budget / target`。覆盖：(1)未注册 function blocked；(2)read-only mount 拒绝 write；(3)跨 mount rename blocked；(4)超过 suspension budget terminal；(5)snapshot hash/version 不匹配 blocked；(6)callback exception 显式 failed。实验不执行真实 shell/network/filesystem effect。

#### 风险边界

- **License**：仓库和 GitHub License API 为 MIT；第三方 Rust/Python/JS dependencies、typeshed 数据、release binaries 与商业 Full Monty 分别核验。OSS license 不覆盖商业 server 条款。
- **维护活跃度**：固定 commit、release v1.0.0 与大量 CI checks 都在查询日前一日更新；但刚进入 1.0，issue #939 已暴露 registry dependency resolution 问题，issue #872 仍报告 type-check/session state drift。
- **安全风险**：它是 language-level sandbox；Rust in-process crash、JS worker process-wide OOM、宿主 callback、remote peer、未认证 snapshot、错误 worker PATH、未 arm memory allocator 都会弱化边界。
- **局限性**：只实现 Python 子集；clock/entropy 默认有例外能力；执行时间不含 host waiting；没有 session lifetime budget；触发 resource error 后继续 session 不保证 heap 正确。
- **验证局限**：本机未运行完整跨语言/跨平台/对抗套件，未复现 escape bounty 测试、registry install issue、remote transport、release assets 与真实宿主 callback policy。
- **不适用场景**：需要完整 CPython/native extension、必须依赖 OS kernel isolation、跨信任域远端 worker 无证明、或宿主无法封装所有 callbacks/mounts 的场景。

#### ⭐ Skill 升格判断

**需二次验证。** 可迁移的是 `deny-by-absence capability + typed suspension + host-owned dispatch + explicit enforcement owner + snapshot provenance`；不迁移 Monty 源码、Python 子集、商业服务或其产品配置。先完成 fake capability fixture，并与现有 effect-scope、verification-first、subagent 四状态和 policy-action identity 候选去重；当前不创建 shared skill。

#### ⭐ Hermes / shared hub 落地路径

1. 在 `runtime/hermes/github-learning-poc/typed-capability-suspension-v0/` 放 agent-neutral schema、fake VM 与 adversarial fixtures；不安装到 Hermes tools。
2. 若 fixture 稳定，在现有工具审计/执行 wrapper 的最终 dispatch 前增加 `capability_id / scope / effect / args_hash / budget / enforcement_owner / terminal` receipt；模型只提出 call，不拥有 capability。
3. 对可执行代码默认使用无 network/fs/env/process 的 runner；需要 capability 时通过 host adapter 明确 allowlist，不通过 prompt 约束权限。
4. 原始证据留 `runtime/hermes/`，候选总结留 `inbox/hermes/daily/`；经治理评分、去重、脱敏与人工审查后，优先更新既有 verification/effect-scope skill，而不是新建 Monty 专属 skill。
5. 不自动改 `~/.hermes/config.yaml`、tools、provider、cron 或 secret；OpenClaw 当前不存在，本轮不调用也不提供其配置写入。

---

### 2. Human-Agent-Society/reef

- **一句话判断**：值得学的是把持续改进拆成 durable record → candidate → evaluator → versioned selection decision → immutable release → activation/rollback，并让训练状态只在 durable commit settled 后可见；不能直接采用的是默认 `AlwaysSelect` 或让 agent 自己发布 code-bearing harness mutation。
- **解决的问题**：替代“把反馈拼进 prompt”“训练完立刻覆盖线上权重/skill”“没有候选身份、评估版本、拒绝记录和回滚链”的旧做法；统一 model weight 与 harness 两种改进面，同时保持服务、记录、训练、发布分层。
- **URL / API 快照**：https://github.com/Human-Agent-Society/reef ；**Stars: 5,155 / Forks: 452 / Language: Python / License: Apache-2.0**；`created_at=2026-08-31T01:39:18Z`，`updated_at=2026-09-25T22:55:46Z`，`pushed_at=2026-09-25T16:53:44Z`，API `open_issues_count=105`（含 PR）。
- **固定提交 / release**：[`ecec4e20b29e7dcbd96150d4b4f1a80b146e120d`](https://github.com/Human-Agent-Society/reef/commit/ecec4e20b29e7dcbd96150d4b4f1a80b146e120d)，commit time `2026-09-25T16:42:42Z`；release [`v0.1.1`](https://github.com/Human-Agent-Society/reef/releases/tag/v0.1.1) published `2026-09-25T16:51:26Z`。
- **Roadmap / release / checks**：roadmap issue #25 将可靠学习服务、可替换基础设施、artifact activate/rollback 与 safe harness evolution 列为重点；v0.1.1 release 包含记录容量淘汰、runtime placement、harness/session 修复等。fixed commit 的 source/package/sandbox tests、lint/docs/build/release checks success。
- **来源交叉核验**：Repository/Commit/Release/Issues/Checks/License/Security Advisories API；README/architecture；developer/state/security docs；`pyproject.toml`、`uv.lock`；records/evaluation/trainer/release-chain/dispatcher 源码；本机定向 pytest/ruff。

#### 架构 / 实现与数据流

```text
agent inference request
  -> service / inference runtime
  -> AgentRecord + stable receipt
  -> RecordStore durable append
  -> feedback/report references existing inference receipt
  -> processor eligibility + TrainingBatch reservation
  -> CandidateBackend.prepare_step()
  -> UpdateCandidate(candidate_id, metadata)
  -> CandidateEvaluator.evaluate()
  -> CandidateSelector.decide()
      SelectionDecision(select|reject, policy/version/reason/evaluation)
  -> backend.settle_step()
  -> ArtifactReleaseChain stage/publish(expected parent)
  -> scenario durable commit log
  -> loader/activator + serving head
  -> trainer.commit(prepared) only after durable commit settles
  -> version history / rollback / later feedback
```

核心分离了 measurement 与 authority：evaluator 只产生带版本的测量，selector 产生可解释的 durable decision，artifact repository 维护 parent/head，scenario/committer 决定事务顺序。记录先 durable append，才唤醒 trainer；trainer 的 state 和 consumed record IDs 也要等 scenario commit settled 后才对进程可见。

#### repo tree 摘要

固定 commit 共 **1,798 tracked files**：

```text
reef/
├── reef/
│   ├── service/             # HTTP routes、profiles、部署/dispatcher入口
│   ├── inference/           # provider/runtime adapters与request capture
│   ├── storage/             # AgentRecord、SQLite/Postgres、receipt、commit log
│   ├── train/               # processor、candidate backend、evaluation、runtime
│   ├── artifact/            # immutable artifact/ref/repository/release chain
│   ├── surface/             # artifact validate/load/activate/serving adapters
│   ├── scenario/            # commit ordering、recovery、rollback、multi-component
│   ├── harness/             # harness composition、native runner、sandbox enforcer
│   └── core/                # shared evaluation/report/batch contracts
├── recipes/                 # SAO/GEPA/TTT/OpenClawRL/SkillClaw/Reefine cookbook
├── tests/reef_service/      # storage/evaluation/artifact/commit/recovery contracts
├── docs/                    # state model、surface、executor、harness safety
├── third_party/             # reviewed integrations/subtrees
├── pyproject.toml / uv.lock # Python package + resolved environment
└── README.md / SECURITY.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `reef/core/evaluation.py` | agent-neutral candidate contract | stable `candidate_id`；versioned evaluator/policy；select/reject + reason + metrics |
| `reef/train/trainer.py` | candidate lifecycle 与 state exposure | evaluate/decide/settle；异常 abort；prepare commit 后才 durable commit；stale candidate re-evaluate |
| `reef/train/evaluation/evaluators.py` | 内置 selection policy | `AlwaysSelect` 默认；`RegressionCheck` 按历史 best + margin 拒绝退化 |
| `reef/storage/records.py` | record/consumption contract | durable sequence、audit/replay、idempotent consumption receipt，body 保留可审计 |
| `reef/dispatcher.py` | ingest/commit orchestration | report references必须指向同 scenario inference；append durable 后才消费；commit/experiment correlation |
| `reef/artifact/release_chain.py` | immutable release chain facade | stage/publish/advance/checkpoint，`expected_parent` 防 stale head |
| `docs/developer-guide/write-a-harness-method.rst` | harness evolution 安全契约 | untrusted tagging、credential screening、code-bearing mutation human review |
| `docs/advanced_topics/state-model.rst` | authoritative ordering | durable bytes、store commit、head install、backend sync、trainer state 的顺序 |

#### ⭐ 源码精读

**代码块 1：candidate、evaluation 与 selection 都有稳定身份和版本化解释。**

```python
@dataclass(frozen=True)
class UpdateCandidate:
    candidate_id: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class SelectionDecision:
    outcome: Literal["select", "reject"]
    policy: str
    policy_version: str
    reason: str
    evaluation: EvaluationResult
    metrics: Mapping[str, Any] = field(default_factory=dict)
```

逻辑摘要：candidate ID 是 idempotency/audit key；测量记录 evaluator/version，决定记录 policy/version/reason，不靠一段不可重放 prose。边界：ID 和结构不保证评估集独立、指标可信或 policy 安全；这些仍需要数据 provenance 和 evaluator fixtures。

**代码块 2：trainer 在 backend settle 异常时显式 abort candidate，且要求 decide 保留同一个 evaluation object。**

```python
def settle_candidate(self, backend, prepared, candidate) -> StepExecution:
    try:
        decision = self._evaluate_candidate(candidate)
        return StepExecution("commit", backend.settle_step(prepared, decision), prepared=prepared)
    except BaseException:
        backend.abort_step(prepared)
        raise

def _evaluate_candidate(self, candidate: UpdateCandidate) -> SelectionDecision:
    evaluation = self._candidate_evaluator.evaluate(candidate)
    decision = self._candidate_evaluator.decide(candidate, evaluation)
    if decision.evaluation is not evaluation:
        raise ValueError("candidate evaluator must retain the evaluation result supplied by Reef")
    return decision
```

逻辑摘要：prepare/evaluate/settle 是一个明确 lifecycle；selector 不能悄悄换掉测量对象，失败走 abort 而不是把半成品留作 commit。边界：`BaseException` abort 是 backend hook，真实远端训练/文件清理是否完成仍要后端 read-back。

**代码块 3：训练状态只在 scenario durable commit settled 后暴露。**

```python
def prepare_commit(self, result: TrainStepResult | None) -> PreparedCommit:
    # pending result、consumed IDs、high-water marks、metrics 被封成 PreparedCommit
    ...

def commit(self, prepared: PreparedCommit) -> None:
    """Expose one prepared state after its scenario commit has settled."""
    with self._lock:
        if self._pending.prepared_commit is not prepared:
            raise RuntimeError("prepared commit does not match the pending training step")
        self._processor.release_records(prepared.released_ids)
        self._state = dict(prepared.algorithm_state)
        self.consumed_record_ids.update(prepared.consumed_ids)
        self._pending = None
```

逻辑摘要：prepare 会触碰 processor 的 batch bookkeeping，但 algorithm state/pending reservation 不提前切换；外层先发布 artifact + 写 durable commit，再调用 `commit` 暴露状态，降低 crash 后重复消费/状态漂移。边界：跨 artifact/store/runtime 的真正原子性靠 scenario committer/recovery 协议，不是 Python lock。

**代码块 4：report ingestion 强制 reference 指向同 scenario 已存在 inference，record durable 后才唤醒学习。**

```python
for reference in item.references:
    source = preceding.get(reference)
    if source is None:
        stored = current.records.get_for_audit(item.scenario, reference)
        source = stored.item if stored is not None else None
    if source is None or source.request_type is not RequestType.INFERENCE:
        raise ReportValidationError(...)

appended = current.records.append_result(item)
if appended.inserted:
    self.process_accepted_records(current)
```

逻辑摘要：feedback 不能引用不存在、跨 scenario 或非 inference 的对象；相同重试通过 existing receipt 幂等；只有 append 成功才启动 processor/training。边界：合法 reference 只证明关联存在，不证明 feedback 来源可信、无注入或评价正确。

**代码块 5：默认 selector 会接受所有成功评估 candidate，安全部署必须显式替换。**

```python
class AlwaysSelectMixin(CandidateEvaluationPlugin):
    def decide(self, candidate, evaluation) -> SelectionDecision:
        return SelectionDecision(
            outcome="select",
            policy="always",
            policy_version="1",
            reason="the method selects every successfully evaluated candidate",
            evaluation=evaluation,
        )
```

逻辑摘要：默认保持兼容的自动发布行为；另有 regression check，可按 best score 与 margin 拒绝退化。边界：对 skill/rules/native tool 等高权 mutation，“成功评估”不等于可安全发布；文档明确 code-bearing mutation 应进入 `review_kinds` 人工审查。

#### 依赖分析与供应链风险

- root package `reef-infra` 需要 Python `>=3.12`。base dependencies 为 `aiohttp>=3.14`、`alembic>=1.13,<2`、`huggingface_hub`、`pyyaml`、`reef-client>=0.2.0`、`reef-eval[harbor]>=0.1.1`、`sqlalchemy>=2,<3`、`tomli-w`；基础包刻意不带 GPU/training stack。
- optional `slime/sglang/tinker/e2b/wandb/opentelemetry/postgres` 可显著扩大网络、GPU、cloud sandbox 与 telemetry 信任面；runtime group 直接 pin `THUDM/slime` 到 commit `41014d1f...`，有复现性但不是 registry provenance，升级需复审。
- `uv.lock` 已提交，开发安装实测成功；但依赖 `reef-client`、`reef-eval`、Harbor、HF、SQLAlchemy/Alembic，完整部署还可能引入 Ray、SGLang、Torch、Transformers、E2B、W&B。core 的 51 个测试通过不能覆盖 optional graph。
- 本机首次 pytest 因 source suite 要求 import repository cookbook package，而 editable installs 未让 repo root 进入 `sys.path`，真实返回 `ModuleNotFoundError: recipes`；补充 `PYTHONPATH=.` 后指定三组测试 51/51。这个环境修正只匹配仓库 source-suite 约定，不应掩盖 packaging/runtime 的其他路径。
- GitHub public advisories 为空，Dependabot API 403；本次未做 `pip-audit`、容器/GPU image、Git LFS artifact、model weights、remote provider 或 license transitive audit。

#### 可复用经验

- 当系统从交互反馈自动产生 skill/model/harness 更新时，应优先把 source record、candidate、evaluation、selection decision 与 release 分成不同持久对象，因为“训练成功”或“生成了文件”不能直接成为发布授权。
- 当候选评估与发布分层时，应优先记录 evaluator/policy version、reason、metrics 和 incumbent/base release，因为同一分数在不同数据集或阈值下没有稳定语义；边界是 evaluator 本身也需治理。
- 当记录会被训练消费时，应优先先 durable append，再唤醒 consumer，并为 consumption 建幂等 receipt，因为进程崩溃不能让同一反馈重复训练或已提交更新丢失消费进度。
- 当多组件或并发 trainer 可能移动 release head 时，应优先用 expected parent/base revision 检测 stale candidate，再重评或拒绝，而不是覆盖最新 head。
- 当 mutation 包含 code、native tool、hook、配置或 secret surface 时，应优先要求人工 review + credential scan + sandbox evaluation，不能采用默认 `AlwaysSelect`；边界是 review 也要绑定确切 candidate identity。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/candidate-promotion-ledger-v0/` 建不依赖 Reef 的纯 Python fixture：输入 3 条历史 cron report，生成 candidate `{candidate_id, base_revision, diff_hash}`；两个 evaluator 返回 deterministic metrics；selector 产出 `{select|reject, policy_version, reason}`；repository 只允许 expected-parent publish。覆盖：(1)相同 receipt 幂等；(2)跨 scope feedback rejected；(3)base revision stale 需 re-evaluate；(4)regression rejected；(5)code-bearing mutation 无 human grant blocked；(6)artifact 写成但 read-back/hash 不匹配仍 failed。仅 runtime POC，不改真实 skill/curated/config。

#### 风险边界

- **License**：仓库与 GitHub License API 为 Apache-2.0；third-party Cordis/reef-client、recipes、models、datasets、GPU images、provider SDK 与云服务条款另审。
- **维护活跃度**：仓库创建不足一个月，v0.1.1 与 fixed head 同日；checks 活跃，但 API、schema、recipes 与部署面仍高速变化，不能把 5k Stars 外推成稳定生产平台。
- **安全风险**：默认 selector 是 `AlwaysSelect`；harness evolution 可生成 skill/rules/native tool/hook，若禁用 sandbox 或漏配 `review_kinds` 会放大代码执行风险。反馈文本、评估任务与发布 artifact 也可能携 credential/prompt injection。
- **局限性**：base install 不是完整训练栈；持续学习质量取决于 feedback、evaluator、holdout、selection policy 与数据漂移。一个合法 receipt 不代表真实人类评价；artifact commit 不等于外部 runtime 已正确 serving，仍需 activation/read-back。
- **验证局限**：只跑 51 个定向 CPU tests 与 4 文件 lint；未跑完整 suite、sandbox/bwrap 本机 lane、Postgres、Git LFS、SGLang/Slime/Tinker/E2B、GPU、真实 provider、multi-node、长时间 crash/recovery。
- **不适用场景**：缺少可测 objective/holdout、无法保留 immutable release/rollback、不能隔离 code-bearing candidate、反馈身份不可信、或团队不愿承担训练/serving 运维复杂度的场景。

#### ⭐ Skill 升格判断

**需二次验证。** `record → candidate → evaluation → selection → immutable release → activate/read-back → rollback` 与 shared hub 自主学习/治理目标高度相关，但当前系统已有 reflection engine、governance、verification-first 和 skill promotion 机制。应先用历史报告做离线 ledger POC并去重，再更新现有 shared workflow；当前不安装 Reef、不创建 Reef 专属 skill、不直接写 curated active fact。

#### ⭐ Hermes / shared hub 落地路径

1. 在 `runtime/hermes/github-learning-poc/candidate-promotion-ledger-v0/` 实现中性 schema：`source_receipts / candidate_id / base_revision / diff_hash / evaluator_version / policy_version / decision / grant / artifact_hash / readback_state`。
2. 将 `scripts/reflection_engine.py` 的建议输出视为 candidate，而非直接 evolution；由现有治理评分、去重、脱敏、安全级别和人工审查产生 selection decision。
3. 对 shared skill 更新复用 `capabilities/manifests/shared-skills.yaml` 与现有治理门禁；code/script/config/cron 变更默认 requires-human，纯文档候选也不自动进入 curated。
4. publish 时必须校验 shared skill/fact 当前 revision；stale candidate 重新审计，避免覆盖其他 agent 已提交更新。写入后再 read-back 文件 hash/manifest/测试结果，不能只看 commit/exit 0。
5. Hermes 作为总控维护 candidate/decision/receipt；future agent 只消费 agent-neutral schema。OpenClaw 当前不存在，本轮不调用、不写其配置或状态。

## 经验沉淀

1. 当执行不可信 Agent 代码时，应优先采用 capability-deny-by-absence + typed suspension + host-owned dispatch，因为黑名单无法稳定覆盖反射、FFI 与新 API；边界是宿主 callback、mount 和远端 worker 仍需独立授权与隔离。
2. 当能力配置跨解释器与宿主时，应优先逐项记录 enforcement owner、hard backstop 与真实验证结果，因为 `max_memory`、sleep、suspension、deadline 等字段存在不等于生效。
3. 当恢复序列化执行状态时，应优先验证 producer、版本、scope 与 MAC/signature，因为 decode 成功不能证明 snapshot 安全或兼容。
4. 当反馈驱动 Agent 自我改进时，应优先把 durable source record、candidate、evaluation、selection decision、release 与 activation 分开，因为“生成/训练成功”不等于“获得发布权”。
5. 当候选涉及代码、native tool、hook、配置、cron 或 secret surface 时，应优先 fail closed 到人工 review，并把批准绑定 exact candidate identity/base revision；默认 auto-select 只适合低风险实验。
6. 当多个 trainer/agent 会更新同一能力时，应优先用 expected parent/base revision 做 stale detection，并在 head 变化后重评候选，因为 last-write-wins 会绕过原评估前提。
7. 当记录被训练消费时，应优先先 durable append、再唤醒 consumer，并用幂等 consumption receipt 记录消费，因为 crash/retry 不能重复训练或丢失进度。
8. 当 GitHub 上游声称安全/CI 通过时，应优先固定 commit、核验 checks/issues/lockfile 并运行本机定向测试，因为空 advisories、Stars、README 或 checkout lockfile 不能覆盖 registry install、optional graph 与 release assets。

## 明日继续

1. 实现 `typed-capability-suspension-v0`：覆盖未授权 function、read-only/write、cross-mount rename、suspension budget、snapshot identity 与 callback failure。
2. 实现 `candidate-promotion-ledger-v0`：用历史 GitHub-learning/cron reports 做 record→candidate→decision→publish/read-back 离线闭环。
3. 对 Monty 用 `cargo install monty-runtime --version 1.0.0 --locked` 与不带 `--locked` 分别复现 issue #939；若修复 release 出现，再核验 registry dependency resolution。
4. 对 Reef 深读 `scenario/committer.py` 和 state model 的 publish/store/head/activate 顺序，补 crash point matrix；不启动 provider/GPU/外部服务。
5. 深读 `NVlabs/SoL-Pi` 的 auto-research candidate/evaluation loop，与 Reef 的 durable publication authority 对比。

## 候选反哺

### Candidate Facts

- [ ] topic: Agent code sandbox 应把外部能力表示为 host-owned typed suspension，而不是 sandbox 内黑名单 | evidence: Monty `RunProgress`、`run.rs`、`docs/security.md`、45 unit tests | 建议: create candidate after fixture | 安全级别: high
- [ ] topic: 资源限制必须记录 enforcement owner，配置存在不等于生效 | evidence: Monty `ResourceLimits` 对 allocator/suspension/sleep 的显式 host obligation | 建议: update effect-scope/verification candidate | 安全级别: high
- [ ] topic: 自我改进应以 versioned candidate/evaluation/selection/release 链取代直接改 active skill | evidence: Reef `core/evaluation.py`、trainer prepare/commit、artifact release chain、51 tests | 建议: update autonomous-learning project candidate | 安全级别: high
- [ ] topic: feedback 先 durable append、消费用幂等 receipt | evidence: Reef dispatcher/RecordStore contracts | 建议: update completion receipt candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: typed-capability-suspension（更新既有 effect-scope / verification workflow） | 可复用场景: code runner、tools、MCP、sandbox callbacks | 是否建议 shared: yes（仅候选） | 原因: 跨 agent 横切，但需 host adapter fixtures 与 enforcement proof
- [ ] 名称: candidate-promotion-ledger（更新既有 autonomous-learning / governance workflow） | 可复用场景: skill、fact、prompt、cron、model/harness 改进 | 是否建议 shared: yes（仅候选） | 原因: 可阻止 suggestion 直接变 active；需与现有 governance 去重

### Candidate Open Questions

- [ ] 问题: Hermes 当前哪些 tool/code execution path 已有统一 host dispatch seam，可挂 capability receipt 而不改 provider/config？ | reason: gap | priority: high
- [ ] 问题: shared hub 现有 reflection 建议如何获得稳定 candidate_id/base_revision/diff_hash？ | reason: adaptation | priority: high
- [ ] 问题: skill/fact promotion 的 evaluator 与 selector version 应记录在哪个现有 schema，避免新建平行 ledger？ | reason: adaptation | priority: high
- [ ] 问题: Monty registry install 的 salsa 漂移在下一 patch release 是否已锁定？ | reason: stale | priority: medium
- [ ] 问题: Reef 默认 AlwaysSelect 在哪些 shipped profiles 被显式替换或叠加 human review？ | reason: gap | priority: high

### 不应自动落地

- 不自动安装或接入 Monty/Reef，不运行不可信 Agent 代码、真实训练、provider、GPU、E2B、远端 worker 或外部副作用。
- 不自动改 Hermes/OpenClaw config、model、provider、tools、auth、cron 或 secret；本轮不调用 OpenClaw。
- 不直接写 `curated/memory/` active fact、不创建新 shared skill；候选必须经评分、去重、脱敏、fixture、安全审查和人工确认。
- 不把 language-level sandbox 当 OS isolation，不把 typed call 当安全 callback，不把 snapshot checksum 当认证，不把 resource config 当 enforcement proof。
- 不把 feedback receipt 当可信评价，不把 evaluator score 当发布授权，不把 default AlwaysSelect 用于高权 mutation，不把 artifact commit 当 runtime serving 已验证。
- 不把 GitHub Stars、空 advisories、CI success、定向 tests 或 lockfile checkout 外推为全依赖、全平台、registry install、release assets 与生产安全已验证。
