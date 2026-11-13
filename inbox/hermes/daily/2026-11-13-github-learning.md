---
type: github-learning-daily
status: raw-research
created: 2026-11-13
updated: 2026-11-13
runner: hermes
---

# 2026-11-13 GitHub 热门项目学习日报

> 查询时间：2026-11-13 07:31–07:38 CST。Stars、Forks、License、更新时间均来自 GitHub Repository API；release/issues 来自对应 GitHub API；源码结论固定到下述 commit。真实 clone、API JSON 与测试输出位于 `runtime/hermes/github-hot-project-learning/evidence/2026-11-13/`。本报告属于 Hermes inbox 原始研究，不是 curated 长期事实。

## 今日结论

今天最值得迁移的共同主线是：**把 Agent 结论变成可核验的 evidence contract，再以 immutable input hash 选择最小 differential harness，并用 sequence cursor / coverage / limitations 明确“看了什么、没看什么、是否真的完成”**；热门度、README 自述和单次绿色测试都不能替代这个确定性外壳。

## 项目速览

下表八个项目均由 2026-11-13 GitHub Repository API 核验；“最近更新”是 repository `updated_at`，不是 release 时间。

| 项目 | Stars | Language | License（API） | 最近更新 UTC | 判断 |
|---|---:|---|---|---|---|
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 57,007 | Python | NOASSERTION | 2026-11-12T23:31:48Z | 热度最高但许可未识别；不复制、不安装，只观察 |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 29,794 | Rust | Apache-2.0 | 2026-11-12T23:31:46Z | **深读**：证据契约、coverage、approval 分类、CLI/MCP 共核 |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 26,934 | JavaScript | MIT | 2026-11-12T23:17:12Z | 视觉 Skill 热门，但今日不做高自由度生成能力迁移 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 25,904 | Python | Apache-2.0 | 2026-11-12T22:55:32Z | 昨日已深读；pending/inflight/flush 模式不重复拆解 |
| [google-research/harness2](https://github.com/google-research/harness2) | 23,547 | Python | Apache-2.0 | 2026-11-12T23:00:49Z | 已有项目卡；今日优先研究不同证据面的工程实现 |
| [horizon-rust/horizon](https://github.com/horizon-rust/horizon) | 9,096 | Rust | MIT | 2026-11-12T23:32:25Z | **深读**：按依赖选择 differential harness、事件游标、统计判决 |
| [amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness) | 9,013 | TypeScript | AGPL-3.0 | 2026-11-12T23:30:57Z | 学习 harness 有关，但网络服务复用需 AGPL 审查 |
| [l0ng-ai/openidea](https://github.com/l0ng-ai/openidea) | 8,751 | TypeScript | Apache-2.0 | 2026-11-12T23:15:37Z | Rust IDE 壳活跃；今日不展开，后续关注增量索引 |

## 深读项目

### 项目 1. storytold/craft-anything

- **GitHub**：https://github.com/storytold/craft-anything
- **固定提交**：`52f1daa668021a84e8c72f2564cf3dfe36ccec67`（提交时间 2026-11-13T01:11:05+07:00）
- **API 基本信息**：Stars 29,794；Forks 6,060；Language Rust；License API 为 Apache-2.0；`updated_at=2026-11-12T23:31:46Z`；`pushed_at=2026-11-12T19:50:17Z`；open issues/PR count 350。
- **许可补充**：根 `Cargo.toml` 与 README 声明 `MIT OR Apache-2.0` 双许可，GitHub API 只识别为 Apache-2.0；仓库品牌文件另受商标条款约束，第三方资产保留各自许可。
- **Release / issue 证据**：最近 release 为 `v0.6.1`，发布于 2026-11-12T01:41:22Z；API 最近活跃项包括 issue #1806（手机/电视 ADB target 提案）、#1695（Codex/OpenCode 的 Just ask 支持）和 PR #1804（Qwen Code 经 ACP 并使 approvals 生效）。这些只证明项目快速变化，不证明所有 adapter 已稳定。
- **一句话判断**：值得学的不是“自动复刻软件”，而是统一的 **Evidence + Coverage + Limitation + Authority** 数据契约，以及 CLI/MCP/UI 共用一个 typed tool registry 和按 effect 分类的 approval gate。
- **解决的问题**：它替代“工具输出一段自然语言、Agent 自己猜可信度/完整度/是否能执行”的旧做法；同时把研究结果和生命周期值分开，将 inferred/partial/unknown 显式化，并把 publish/system/delete 等动作从普通分析工具中分离授权。

#### 架构 / 实现与数据流

```text
Target / Website / App / Binary
  -> apps/craft-anything | craft-anything-cli | MCP
  -> crates/engine::ToolSpec（同一 registry、schema、effect metadata）
  -> formats / disasm / js / analysis / engines
  -> ToolOutput::Evidence | ToolOutput::Value
  -> Session.record()
  -> project evidence store + in-memory bounded ledger
  -> evidence id / coverage / limitations / unknowns
  -> Study -> Build -> Check -> Ready
  -> action approval（allow / ask / refuse）
```

核心并不是让每个入口各写一套逻辑：`ToolSpec` 统一 id、schema、effects、requires 和函数指针；`ToolOutput` 明确 evidence 与非 evidence lifecycle value；`Session.record` 同时落项目 store 和有序 ledger；Evidence 的 identity 由 canonical JSON 的 SHA-256 生成，并把 display-only 字段排除；ActionKind 则把 web、commands、outside_files、publish、delete_outside、system、other_tools 分开决策。

#### Repo tree 摘要

```text
craft-anything/
├── apps/
│   ├── craft-anything/       # egui 桌面应用
│   ├── craft-anything-cli/   # 与 engine 同源的 CLI / MCP 入口
│   └── craft-anything-web/   # WASM 浏览器查看器
├── crates/
│   ├── evidence/             # Evidence、confidence、coverage、limitation、unknown、canonical id
│   ├── engine/               # Session、Workspace、ToolSpec、approval、jobs、project workflow
│   ├── formats/              # archive/binary/document/game 等格式读取器
│   ├── analysis/             # 图、diff、应用与源码分析
│   ├── disasm/ / js/         # 反汇编与 JavaScript 分析
│   ├── engines/              # 外部引擎/WASM plugin adapter
│   ├── mcp/ / setup/         # MCP 暴露与宿主接入
│   ├── platform/ / ui-egui/  # 平台能力与 UI
│   └── testkit/              # fixtures / 测试工具
├── docs/                     # STATUS、ROADMAP、工具与 agent adapter 文档
├── examples/                 # WASM plugin 示例
├── vendor/wgpu-hal/          # 临时 vendored patch
├── packaging/                # 多平台发布脚本
├── Cargo.toml / Cargo.lock   # workspace 与锁定依赖图
└── deny.toml                 # 供应链/许可检查配置入口
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/evidence/src/lib.rs` | canonical evidence contract | `Confidence`、`Authority`、`Coverage`、`Limitation`、`Evidence`、content-derived id 与 tamper check |
| `crates/engine/src/tool.rs` | 统一工具注册和输出 | `ToolOutput::Evidence/Value`；`ToolSpec` 同时携带 schema、effects、requires、run |
| `crates/engine/src/session.rs` | evidence ledger | 项目 store + bounded in-memory ledger；按 id 更新并保留展示顺序 |
| `crates/engine/src/workspace.rs` | project manifest 与 action policy | `ActionKind` 七类 effect；auto/manual 默认矩阵；project override |
| `crates/engine/src/project.rs` | 项目持久层 | project meta、evidence/unknown 存取与完整性入口 |
| `docs/STATUS.md` | 可核验能力矩阵 | 逐能力说明状态、如何验证、未验证平台/场景，而非只列 feature |
| `README.md` | 工作流和安全边界 | clean room 不是 OS sandbox；安装依赖会执行代码；early alpha |
| `Cargo.toml` / `Cargo.lock` | 依赖与构建边界 | Rust 1.97、819 个锁定 package、1 个 pinned git source、vendored patch |

#### 源码精读

**1）`Evidence::compute_id`：对 canonical 内容做 identity，而不是对展示文本或路径做 identity。**

```rust
pub fn compute_id(&self) -> Result<String, ToolError> {
    let mut v = serde_json::to_value(self)
        .map_err(|e| ToolError::internal(format!("serialising evidence: {e}")))?;
    if let Value::Object(map) = &mut v {
        map.remove("id");
        map.remove("summary");
        map.remove("carries_target_content");
        if let Some(Value::Object(subject)) = map.get_mut("subject") {
            subject.remove("name");
        }
    }
    Ok(format!("ev_{}", sha256_hex(canonical_json(&v).as_bytes())))
}
```

`summary`、`subject.name` 和 target-content 展示标记不改变 id；params、result、confidence、authority、environment、coverage、limitations、links 等语义字段会改变 id。`verify()` 重新计算并比较，能检测存储内容被改动；但这是无密钥 hash，不能证明发布者身份，也不能阻止攻击者改内容后重算 id。

**2）`Session::record`：先持久化项目 evidence，再维护当前 session 的有序 ledger。**

```rust
pub fn record(&mut self, ev: Evidence) -> Result<(), ToolError> {
    if let Some(project) = &self.project {
        project.store_evidence(&ev)?;
    }
    if !self.ledger.contains_key(&ev.id) {
        self.order.push(ev.id.clone());
    }
    self.ledger.insert(ev.id.clone(), ev);
    Ok(())
}
```

相同 id 更新 map 时不会重复追加 order；项目打开时只把最新 evidence 按记录数/字节预算载入内存，其他记录留盘并可按 id resolve。这里的“bounded recall + durable exact record”比把所有证据塞入 prompt 更稳，但 `store_evidence` 与内存更新之间仍不是跨多个外部 artifact 的通用事务。

**3）`ToolOutput` / `ToolSpec`：区分可审计 evidence 与普通状态值，并让所有表面共用一个执行描述。**

```rust
pub enum ToolOutput {
    Evidence(Box<Evidence>),
    Value(Value),
}

pub struct ToolSpec {
    pub id: &'static str,
    pub title: &'static str,
    pub summary: &'static str,
    pub beginner: &'static str,
    pub toolset: Toolset,
    pub effects: Effects,
    pub requires: Requires,
    pub input_schema: fn() -> Value,
    pub run: ToolFn,
}
```

Evidence 会进入 session ledger；lifecycle/status result 不冒充 evidence。`ToolSpec` 把 tool id、schema、effect 和 prerequisite 放在同一 registry，CLI 名由 id 确定性转换；这适合生成 adapter，而不是维护多份手写能力清单。边界是 metadata 仍需与真实实现做 contract test，不能因声明 read-only 就默认可信。

**4）`ActionKind::default_in` / `Manifest::approval`：auto mode 不是“全放行”，publish/system 等默认拒绝。**

```rust
pub fn default_in(self, auto_mode: bool) -> Approval {
    self.row().map_or(
        Approval::Ask,
        |r| if auto_mode { r.auto } else { r.manual },
    )
}

pub fn approval(&self, kind: ActionKind, auto_mode: bool) -> Approval {
    self.approvals
        .get(&kind)
        .copied()
        .unwrap_or_else(|| kind.default_in(auto_mode))
}
```

源码矩阵显示：Web 在 auto/manual 都 Allow；Commands 和 OutsideFiles 在 auto Allow、manual Ask；Publish、DeleteOutside、System、OtherTools 在 auto Refuse、manual Ask。这个策略对“可撤销”的定义仍偏应用级，不能直接复制到 Hermes；尤其 commands/outside_files 自动允许并不适合作为共享中台默认安全策略。

#### 依赖分析与供应链风险

- workspace 要求 Rust `1.97`，版本 `0.6.1`；根依赖包括 `serde/serde_json/schemars`、`sha2`、`egui/eframe`、`oxc_*`、`object`、`iced-x86`、`wasmparser/wasmprinter` 等。
- `craft-anything-evidence` 的直接依赖较窄：`serde`、`serde_json`、`sha2`、`hex`、`thiserror`；适合单独验证 evidence contract，而不是编译整套 UI/格式引擎。
- `Cargo.lock` 实测 819 个 package，含 1 个固定 revision 的 git source：`storytold/craft-libs@6ac2a6a...`；根 `[patch.crates-io]` 将 `wgpu-hal` 指到 `vendor/wgpu-hal`。commit pin 降低 moving-ref 风险，但 vendored patch 与发布制品仍要独立 provenance/许可审查。
- 本机真实执行 `cargo test --locked -p craft-anything-evidence`：**15 passed, 0 failed**，doc-tests 0；执行时真实更新 crates.io index 并拉取 pinned git repository。这只验证 evidence crate，不覆盖 engine、CLI/MCP、桌面 UI、adapter、installer、release asset 或 clean-room 行为。

#### 可复用经验

- **当工具输出要进入 Agent 推理、审计和恢复时，应优先使用 `subject + operation + params + result + confidence + authority + coverage + limitations + links` 的 canonical evidence，而不是只保存 Markdown 摘要，因为摘要无法区分观察、推导、猜测与未覆盖范围；边界是 hash identity 不证明来源真实性。**
- **当同一能力要从 CLI、MCP、UI 和 future agent adapter 暴露时，应优先共用一个 typed ToolSpec / executor，再从 registry 生成各表面，因为手写多份清单会发生 schema/effect 漂移；边界是 adapter transport auth 与真实 effect 仍需分别验证。**
- **当无人值守模式遇到 publish、delete、system 或未分类工具时，应优先拒绝或进入 `needs_user`，而不是把 auto mode 理解为全授权，因为自动化程度不能提升 authority；边界是当前项目对 commands/outside_files 的 auto 默认不能原样迁移。**

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/evidence-contract-v0/` 用 Python 标准库做一个无副作用 fixture：定义 3 条 synthetic evidence（observed/derived/inferred），固定 canonical JSON，生成 content id；改变 summary 应保持 id，改变 coverage/limitation 必须改变 id；再生成一份 Markdown projection，并断言 projection 不能反向成为 canonical truth。无需安装 Craft Anything，不读取 secret，不改配置/cron。

#### 风险边界

- **License**：API 为 Apache-2.0，仓库根为 MIT OR Apache-2.0；第三方资产、字体、icons、vendor 与品牌另有条款，顶层许可不能外推到全部 bundle。
- **维护活跃度**：固定提交与 `v0.6.1` 均在近 24 小时内，issue/PR 活跃；但 README 明示 early alpha，adapter 支持有的只是“built, not yet run live”。快速变化意味着 schema/路径可能继续漂移。
- **安全风险**：可启动 coding agent、执行命令、安装依赖、读取 target、联网、使用外部 engine；README 明确 clean room 不是 OS sandbox，依赖安装脚本会在本机执行。不得在 cron 自动安装或运行重建工作流。
- **局限 / 不适用**：本次只运行 evidence crate 15 个测试；未验证 923-test baseline、全 workspace clippy、MCP/CLI parity、Hermes ACP adapter、Windows/macOS、真实 app rebuild。README 的测试数量和能力矩阵是上游证据，不是本机完整复现。

#### Skill 升格判断

**需二次验证。** Evidence schema 与 typed tool registry 对 shared hub 有明显价值，但与现有 `autonomous-learning/orchestrator-protocol` 的 completion/evidence/coverage 约束高度重叠。今日不创建 repo 专属 Skill；先做 runtime fixture、与现有 contract 去重，并验证 raw inbox、audit artifact、knowledge projection 三类数据都能保持 identity/coverage 后，再提交“更新既有 Skill”的审核稿。

#### Hermes / shared hub 落地路径

1. 原始研究继续放 `inbox/hermes/daily/2026-11-13-github-learning.md`；clone、API JSON、stdout 与 POC 只放 `runtime/hermes/`。
2. POC 建议 schema：`EvidenceRecord(subject, operation, input_hash, result_ref, confidence, authority, coverage, limitations, producer, revision)`；`to_markdown()` 只能做 projection，不能反向写 truth。
3. 在 `scripts/github_learning_orchestrator.py` 的后续候选版本中，让 auditor 读取结构化 sidecar，而不是只靠 Markdown 关键词计分；但今天不改 orchestrator，先保留为 candidate。
4. 若 fixture 通过，优先更新 `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md` 的既有 evidence contract 和 tests，不复制上游 Rust 源码；future-agent 通过中性 schema 接入。
5. 不自动修改 Hermes 配置、模型、provider、cron 或 secret；不调用当前不存在的 OpenClaw runtime。

---

### 项目 2. horizon-rust/horizon

- **GitHub**：https://github.com/horizon-rust/horizon
- **固定提交**：`7c1a43138c8e6d1b5102231facb7bdfff2f2ab37`（提交时间 2026-11-12T22:43:08+00:00）
- **API 基本信息**：Stars 9,096；Forks 1,498；Language Rust；License MIT；`updated_at=2026-11-12T23:32:25Z`；`pushed_at=2026-11-12T22:43:09Z`；open issues/PR count 688。
- **Release / issue 证据**：最近 API releases 为 launcher `0.2.62`、`0.2.61`、`0.2.60`，其中 `0.2.62` 发布于 2026-11-12T16:37:22Z；最近活跃项主要是 PR，例如 #15728（处理非有限 benchmark 样本）、#15817（刷新自动 loot/warden parity captures）。高频 release/PR 证明活跃，不等于完整游戏/跨平台稳定。
- **一句话判断**：最值得学的不是 Minecraft 重写，而是 **依赖追踪驱动的 differential harness 选择、content-addressed pass reuse、事件 cursor 防丢与统计判决的 measurement floor**。
- **解决的问题**：它替代“每次改动都跑全套”与“只跑几个手选测试”两种极端：harness 真实记录 Python/Java/Rust/fixture 依赖，输入与 toolchain hash 不变就复用 pass；变化时只跑 affected harness，同时用 vanilla oracle 做差分。Agent 控制面则以 seq/cursor、wait condition 和 typed timeout 避免轮询与事件竞态。

#### 架构 / 实现与数据流

```text
Source change / branch diff
  -> tools/parity.py discovers test_*_parity.py
  -> previous trace dependencies + Cargo .d dep-info + oracle inputs
  -> environment_key(rustc/java/javac/profile/research-lock/Cargo.lock/prepared data)
  -> content key(dependency path + SHA-256)
  -> affected harness selection
  -> vanilla oracle + Horizon probe
  -> deterministic comparison
  -> pass/fail/flaky/blocked records + logs
  -> shared content-addressed pass reuse across worktrees

Agent command
  -> horizon-ctl / MCP
  -> local authenticated control endpoint
  -> Game command/action
  -> event snapshot diff
  -> seq-numbered bounded event log
  -> events --since / wait-for --since
  -> JSON outcome / typed timeout
```

`tools/parity.py` 从真实执行 trace 中收集 Python modules、Java oracle sources、其他 repo files 和 Cargo dep-info；`environment_key` 还绑定 Rust/JDK、build profile、`research-lock.json`、`Cargo.lock` 和 prepared manifest。`docs/parity-workflow.md` 说明 oracle output 可缓存，但失败时会 fresh rerun。Agent event loop 每轮比较快照，事件带 `seq/tick`，wait 默认从当前 seq 开始；调用方若要防止“动作太快导致错过”，先读 last，再传 `--since`。

#### Repo tree 摘要

```text
horizon/
├── crates/
│   ├── horizon-client*       # 游戏循环、输入、渲染、CLI control
│   ├── horizon-world         # 世界、实体、物理、存储与大量 probe
│   ├── horizon-protocol      # 网络协议、版本 adapter、mod list
│   ├── horizon-server*       # 独立服务、事件/API/管理
│   ├── horizon-perf*         # capture、diff、统计与 benchmark
│   ├── horizon-mcp           # MCP schema/transport 共用层
│   └── horizon-prepare       # 从用户自有游戏文件准备私有资源
├── tools/
│   ├── parity.py             # differential harness runner / trace / cache / scheduling
│   ├── parity_reach.py       # item-level Rust reachability 近似
│   ├── pr_ready.py           # 变更驱动的 PR gate
│   ├── test_*_parity.py      # 数百个差分 harness
│   └── ci/                   # release/runner/triage 工具
├── tests/                    # Python 工具与治理测试
├── docs/                     # parity、agent control、架构、发布与安全边界
├── third_party/              # wgpu-hal、naga、libmimalloc-sys 固定修补
├── launcher/                 # 独立 launcher workspace
├── mods/                     # vanilla oracle/mod fixtures
├── research-lock.json        # 官方资源/研究工具 pin
├── Cargo.toml / Cargo.lock   # 50+ workspace crates与锁图
└── THIRD_PARTY_NOTICES.md    # 逐项来源、许可、历史清理记录
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `tools/parity.py` | 增量 differential harness runner | harness discovery、trace dependency、content/environment key、cache、远端/本地资源调度、flaky policy |
| `tools/parity_reach.py` | 变更影响近似 | 从 probe item 到 Rust source 的保守 reachability，超预算时回退全依赖 |
| `tools/pr_ready.py` | PR gate | 变更→crate/tests/clippy/parity 计划；公开 skip/left-to-main 状态 |
| `docs/parity-workflow.md` | 机制契约 | oracle replay、依赖追踪、worktree pass sharing、资源预算、边界与误差 |
| `crates/horizon-client/src/game/events.rs` | Agent event stream | snapshot diff、seq/tick、events cursor、wait-for、typed timeout |
| `crates/horizon-server/src/events.rs` | 管理 API/SSE event stream | bounded replay、Last-Event-ID、type filter、keepalive |
| `crates/horizon-perf/src/stats.rs` | 性能判决 | Hodges-Lehmann effect、exact Mann-Whitney interval、measurement floor、drift |
| `crates/horizon-protocol/src/mod_list.rs` | 兼容 diff | id/version/hash/side 的确定性 missing/changed/extra 分类 |
| `THIRD_PARTY_NOTICES.md` | 许可与来源审计 | 记录曾误用的 GPL/LGPL 源码及清理、vendored patch、外部制品条款 |

#### 源码精读

**1）`environment_key` + `key`：pass reuse 绑定依赖内容和执行环境，不绑定 worktree 路径。**

```python
def environment_key(hasher):
    parts = [version(["rustc", "-V"]), version(["java", "-version"]),
             version(["javac", "-version"]), json.dumps(PROFILE, sort_keys=True),
             hasher(ROOT / "research-lock.json"), hasher(ROOT / "Cargo.lock"),
             hasher(version_dir / "prepared.json"),
             hasher(version_dir / "manifest.json")]
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()

def key(record, hasher, environment):
    digest = hashlib.sha256(environment.encode())
    for path in sorted(record["dependencies"]):
        digest.update(f"{path}\0{hasher(ROOT / path)}\n".encode())
    return digest.hexdigest()
```

缓存 identity 覆盖 toolchain、profile、研究锁、Cargo 锁和准备数据，再覆盖每个真实 dependency path/content。这样相同内容可跨 worktree 复用，路径变化不会天然让测试失效；但 trace 若漏依赖仍会产生 stale pass，所以 scope narrowing 是保守优化，闭包不成立时回退全部 source。

**2）`Events::push` / `since`：事件有 dense seq，bounded replay 被明确化。**

```rust
fn push(&mut self, tick: u64, mut event: Value) {
    self.seq += 1;
    event["seq"] = self.seq.into();
    event["tick"] = tick.into();
    if self.log.len() == KEPT {
        self.log.pop_front();
    }
    self.log.push_back(event);
}

fn since(&self, seq: u64) -> impl Iterator<Item = &Value> {
    self.log.iter().filter(move |e| e["seq"].as_u64() > Some(seq))
}
```

client event log 只保留 256 条，server 管理 API 保留 2,000 条；seq 继续递增，调用方可以知道自己从哪个 cursor 继续。当前 `since` 不返回显式 gap/oldest sequence，若 cursor 早于已淘汰窗口，调用方可能只能从第一条 retained event 推断缺口；这正是不能直接复制而应在 shared POC 加 `oldest_seq/truncated` 的原因。

**3）`events_command` 的 `wait-for`：默认从注册时当前 seq 开始，避免旧事件误命中。**

```rust
"wait-for" => {
    let (condition, timeout, since) = parse_wait(&words[1..])?;
    self.events.waits.push(Wait {
        condition,
        since: since.unwrap_or(self.events.seq),
        started: Instant::now(),
        timeout,
        reply: reply.clone(),
    });
    Ok(Some(None))
}
```

`watch_events` 每轮检查 screen/widget/loaded/chat/event 条件；成功返回 `ok=true`，超时返回 `kind=timeout`，未完成就保留 waiter。对于“先动作、再 wait”的调用，文档要求动作前先读 `events.last` 并在 wait 中传 `--since`，避免快速事件发生在注册前。这是 Agent 工具比 `sleep && poll` 更可靠的具体协议。

**4）`stats::compare`：统计显著不等于工程上重要，先判断噪声和 measurement floor。**

```rust
pub fn compare(a: &[f64], b: &[f64]) -> Option<Comparison> {
    let (a, b) = (last_blocks(a), last_blocks(b));
    let (median_a, median_b) = (median(a)?, median(b)?);
    let mut diffs: Vec<f64> = a.iter()
        .flat_map(|&x| b.iter().map(move |&y| y - x)).collect();
    diffs.sort_by(f64::total_cmp);
    let effect = median_sorted(&diffs);
    let verdict = match interval {
        _ if a.len() < MIN_BLOCKS || b.len() < MIN_BLOCKS => Verdict::TooFewBlocks,
        Some(([lo, hi], ..)) if lo <= 0.0 && 0.0 <= hi => Verdict::WithinNoise,
        Some(_) if effect.abs() < NEGLIGIBLE_MS.max(NEGLIGIBLE_SHARE * median_a) => Verdict::Negligible,
        Some(([lo, _], ..)) if lo > 0.0 => Verdict::Slower,
        Some(_) => Verdict::Faster,
        None => Verdict::TooFewBlocks,
    };
    // 返回 median、effect、CI、confidence、verdict
}
```

至少六个 block 才判方向；CI 覆盖 0 为 WithinNoise；效果虽显著但低于 1 ms 或基线 2%（取更大者）则为 Negligible。这个模式可迁移到 Agent quality/latency 对比：不能把单次快 100 ms 或一个均值变化直接写成“优化成功”。

#### 依赖分析与供应链风险

- workspace `Cargo.toml` 列出 50+ crates，要求 Rust 1.95；`horizon-client` 直接依赖大量内部 crate，以及 `wgpu 30.0.1`、`winit 0.30.13`、`naga 30.0.1`、`zip 9.1.3`、`ureq 2` 等图形、压缩和网络组件。
- `Cargo.lock` 实测 610 个 package，0 个 git source；但 `third_party/wgpu-hal`、`third_party/naga`、`third_party/libmimalloc-sys` 通过 `[patch.crates-io]` 替换 registry crate，仍属于 vendored supply chain。
- `THIRD_PARTY_NOTICES.md` 公开记录曾错误纳入 LGPL/GPL 来源实现并已移除/clean-room replacement；这说明 license provenance 是活跃风险，不应因顶层 MIT 就复制实现。另有 DXC release asset、Microsoft 条款、Minecraft EULA/商标与用户自有游戏资源边界。
- 本机真实执行：`cargo test --locked -p horizon-perf --lib stats::tests` 为 **11 passed, 0 failed**；`python3 -m unittest tests.test_parity_reach` 为 **9 passed**。第一次误用模块路径 `tools.test_parity_reach` 得到真实 `ModuleNotFoundError`，随后定位到 `tests/test_parity_reach.py` 并用正确入口通过；原始错误没有伪装成产品失败。
- 未执行全量 `parity.py --all`：它需要用户自有 Minecraft 26.3、server jar、JDK 25、prepared `.local` 和大量时间/硬件。README 的 hundreds of differential tests、性能数字与“0 player-visible gaps”属于上游声明，本机未全量复现。

#### 可复用经验

- **当测试套件很大且输入依赖可追踪时，应优先用“真实执行 trace + toolchain/config/data hash”选择 affected differential harness，并让 cache key 绑定内容而不是 worktree 路径，因为全量重跑浪费资源、手选测试容易漏回归；边界是 trace 漏依赖必须由保守回退和定期全量审计兜底。**
- **当 Agent 需要等待异步世界状态时，应优先使用 dense sequence cursor、bounded event replay 和 typed wait timeout，而不是 sleep/poll，因为动作可能快于 waiter 注册且旧事件可能误命中；边界是 replay 截断必须显式返回 oldest/truncated，不能让调用方猜。**
- **当质量或性能比较要驱动结论时，应优先同时设置 sample floor、effect size、confidence interval 和 negligible threshold，因为统计显著、单次变化与工程价值不是一回事；边界是阈值必须按本系统真实语料校准。**

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/differential-harness-selection-v0/` 创建 4 个 synthetic task 与 3 个 verifier：记录每个 verifier 读取的文件；key 绑定 Python 版本、policy version、输入 hash 与 dependency hash；只改一个输入时断言只选择受影响 verifier；再模拟 cursor 早于 retained window，要求返回 `truncated=true, oldest_seq, next_seq`。纯 Python 标准库，不执行第三方游戏、不联网、不写 shared curated。

#### 风险边界

- **License**：原创代码为 MIT，但 Minecraft code/assets 受 Mojang/Microsoft 权利与 EULA 约束；third-party patches、DXC、字体/icons 与历史 clean-room replacement 分别受不同许可。不得复制 game/oracle/decompiled source 到 shared。
- **维护活跃度**：API 显示同日 push 和 launcher 0.2.62 release，近期 PR 密集；高活跃也意味着 API、资源 pin 和实现频繁变化，固定提交之外的结论待核验。
- **安全风险**：launcher/prepare 会处理用户账号、私有游戏资源、JDK、native GPU stack、mods、network server 和本地 control socket；`horizon-ctl` 的动作能力高，不能接入 Hermes cron。远端 parity host 文档还明确不可发送 secret/token。
- **局限 / 不适用**：本机只跑 11 个统计单测与 9 个 reachability 单测；未跑游戏、GPU、JDK oracle、完整 parity、release asset、agent-control E2E。content-hash cache 依赖 trace 完整性；bounded events 在过旧 cursor 上缺少显式 gap 字段。

#### Skill 升格判断

**需二次验证。** “dependency-traced differential harness selection”和“cursor-aware event wait”都是跨 Agent 可复用模式，但前者需要验证 Hermes workflow 的依赖是否能可靠追踪，后者需先补显式 truncation/gap contract。今天不新建 Horizon 专属 Skill；先在 runtime 做 synthetic POC，再判断是否更新现有 `autonomous-learning/orchestrator-protocol` 和 `research/github-hot-project-learning` 的 verifier 章节。

#### Hermes / shared hub 落地路径

1. 建议 POC 路径：`runtime/hermes/github-learning-poc/differential-harness-selection-v0/`，状态只服务当前 Hermes 验证，不进 curated。
2. 建议接口：`record_reads(verifier_id) -> dependency_set`；`cache_key(input_hash, dependency_hashes, toolchain, policy_revision)`；`affected(changed_hashes) -> verifier_ids`；`events_since(cursor) -> {events, oldest_seq, next_seq, truncated}`。
3. 若通过，再让 `scripts/github_learning_orchestrator.py` 的 checker 以报告 input hash、审计器版本和 evidence sidecar 决定是否复用；每日/周期性 full audit 兜底 trace 漏项。
4. shared 层只沉淀中性的 contract/fixture，不复制 Minecraft 源码、游戏资源、Horizon 实现或机器路径；future agent 各自实现 adapter。
5. 不自动修改 Hermes 配置、cron 或工具权限；不启动当前不存在的 OpenClaw runtime。

## 经验沉淀

1. **当工具输出要进入 Agent 推理、审计或长期恢复时，应优先保存 canonical evidence（identity、authority、confidence、coverage、limitations、source links），再生成 Markdown/卡片 projection，因为自然语言摘要无法可靠承担 truth；边界是 content hash 不证明发布者和事实真实性。**
2. **当同一能力要跨 CLI、MCP、UI 与 future agent 暴露时，应优先共用 typed registry/executor 并从中生成 adapter，因为手写多份 schema/effect 清单会漂移；边界是 transport auth、host policy 和真实副作用仍需逐 adapter 验证。**
3. **当大型 workflow 只需重跑受影响验证时，应优先记录真实 dependency trace，并让 reuse key 覆盖 input、dependency、toolchain、config/policy 与 oracle revision，因为路径、日期和“上次通过”不是稳定身份；边界是定期全量审计要兜底漏依赖。**
4. **当 Agent 等待异步状态或事件时，应优先先取得 cursor，再执行动作并按 `since` 等待 typed event，因为 sleep/poll 会漏掉快事件或消费旧事件；边界是 bounded log 截断必须返回 gap/truncated。**
5. **当性能或质量数据要触发“更好/更差”结论时，应优先同时要求 sample floor、effect size、interval 与 negligible threshold，因为一次变化或统计显著不等于工程价值；边界是阈值要用本域历史数据校准。**
6. **当无人值守任务遇到 publish、delete、system、secret 或未知 effect 时，应优先拒绝或返回 `needs_user`，因为 auto mode 不能扩大权限；边界是 project-local commands 也不能仅凭文本分类自动放行。**
7. **当上游项目极新、release/PR 高频且 stars 快速增长时，应优先固定 commit、保存 API snapshot、运行窄测试并明确未覆盖 lane，因为热度与活跃度不证明成熟、安全或跨平台可用。**

## 明日继续

1. 实现 `runtime/hermes/github-learning-poc/evidence-contract-v0/`：验证 canonical id、display-only 字段、coverage/limitation identity、projection 单向性。
2. 实现 `runtime/hermes/github-learning-poc/differential-harness-selection-v0/`：验证 dependency hash 选择、policy/toolchain 失效、cursor gap/truncated。
3. 搜索并做去重矩阵：对照现有 `autonomous-learning/orchestrator-protocol` 与 `research/github-hot-project-learning`，只提交既有 Skill 的更新审核稿，不自动落盘 shared Skill。
4. 若继续研究上游，优先读取 Craft Anything engine/tool dispatch 的 effect enforcement tests 与 Horizon event-gap/affected-harness failure cases；不自动安装 app、模型、agent adapter 或游戏资源。

## 候选反哺

### Candidate Facts

- [ ] topic: Agent 工具结果应采用 authority/confidence/coverage/limitations 完整 evidence contract | evidence: `storytold/craft-anything@52f1daa` 的 `crates/evidence/src/lib.rs`，本机 evidence crate 15 tests passed | 建议: update 既有 verification/evidence fact，先 POC 与去重 | 安全级别: medium
- [ ] topic: 大型验证可用真实依赖 trace + environment/content hash 选择 differential harness | evidence: `horizon-rust/horizon@7c1a431` 的 `tools/parity.py`、`docs/parity-workflow.md`，本机 parity_reach 9 tests passed | 建议: create candidate，需 Hermes synthetic POC | 安全级别: medium
- [ ] topic: Agent event wait 应绑定 sequence cursor 并显式披露 replay gap | evidence: `crates/horizon-client/src/game/events.rs` 的 seq/since/wait；上游当前 bounded log 未显式返回 oldest/truncated | 建议: create candidate with adaptation，不直接复制 | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: canonical-evidence-contract（优先更新既有 orchestrator protocol） | 可复用场景: GitHub 学习、巡检、研究、知识库 projection、future agent handoff | 是否建议 shared: yes-after-POC | 原因: 横切价值高，但需与现有 completion/evidence contract 去重并验证 projection 边界
- [ ] 名称: dependency-traced-differential-verification | 可复用场景: 大型 cron/workflow 的增量 audit、受影响测试选择、跨 workspace pass reuse | 是否建议 shared: yes-after-POC | 原因: 可明显降低重跑成本，但漏依赖会制造 stale green，必须有 full-audit ratchet
- [ ] 名称: cursor-aware-event-wait fixture | 可复用场景: delegate、浏览器、消息、后台任务的异步等待 | 是否建议 shared: no-now | 原因: 先在 runtime 验证 gap/truncation/timeout/cancel，再并入既有 terminal/receipt contract

### Candidate Open Questions

- [ ] 问题: 如何让 GitHub 学习审计从 Markdown 关键词评分迁移为 canonical sidecar，同时保持人类可读报告？ | reason: adaptation | priority: high
- [ ] 问题: Hermes workflow 能否低成本、可靠地记录 verifier 实际读取的依赖，而不引入不完整 trace 的假绿？ | reason: gap | priority: high
- [ ] 问题: bounded event log 的 cursor 早于 oldest retained event 时，统一 contract 应返回 `truncated`、gap range 还是直接 blocked？ | reason: adaptation | priority: high
- [ ] 问题: Craft Anything 的 effect metadata 与 action approval 在 CLI/MCP/ACP adapter 上是否都有不可绕过的最终 enforcement？ | reason: gap | priority: medium

### 不应自动落地

- 不自动安装或运行 Craft Anything/Horizon，不启动 coding agent、游戏、MCP server、JDK oracle、native GPU 工具或第三方 installer。
- 不自动修改 Hermes/OpenClaw 配置、模型、provider、cron、secret 或消息渠道；当前 OpenClaw runtime 不存在且本任务未调用。
- 不复制上游源码、Minecraft/品牌资产、decompiled/oracle data 或 vendored native code到 shared Skill。
- 不把本报告或 Candidate Facts 直接晋升 curated active fact；必须先 POC、证据评分、去重、脱敏和治理/人工审查。
- 不把 15/11/9 个定向测试、上游 release 活跃或 README benchmark外推为全仓、跨平台或生产可用。
