---
type: case
status: draft
created: 2026-10-18
updated: 2026-10-18
domain: learning
tags: [github-learning, agent-tools, capability-filesystem, effect-receipt, rust]
---

# 2026-10-18 GitHub 热门项目学习报告

> 执行者：Hermes；当前 OpenClaw runtime 不存在，本次未调用 OpenClaw。  
> 查询与验证时间：2026-10-18 07:30–08:40（UTC+08:00）。发现口径包括 GitHub Search API `created:>2026-09-01 sort:stars` 与 `stars:>1000 pushed:>2026-10-01 sort:stars`；Stars 是 08:39:58（+09 工具环境，即 07:39:58 UTC+08）附近的 Repository API 快照。  
> 深读固定提交：`storytold/photocraft@ead6d2197f5d0b82d70f3fddb70e472fc27ce577`；`storytold/pdfcraft@4f6d16380a13e6d584bba369d7118ba6e60b608a`。PdfCraft 在研究期间 main 前进到 `3f5a784c2cb5934ed429ee52a07c4abeb180138b`，因此源码结论只绑定 clone 的 `4f6d163...`，最新维护状态另行记录。  
> 真实来源：GitHub Repository/Search/Commit/Release/Issues/Actions/License/Security Advisories API，README、SECURITY/docs（存在时）、Cargo manifests/lockfile、关键源码，以及本机锁定依赖的定向 Cargo tests 与 `cargo audit`。Dependabot Alerts API 对两仓均为 HTTP 403，未把不可见结果写成“无漏洞”。

## 今日结论

**Agent 工具的安全边界不能只做参数 schema：应把 capability-based 文件句柄、读写 authority 分离、host-owned 命令门禁、effect certainty（未发送/结果未知/确定失败）、原子发布与 read-back receipt 串成同一条确定性外壳；同时把“无约束模式”和“仅字符串 canonicalize 的 TOCTOU 窗口”明确视为降级状态。**

### 今日真实验证摘要

- **PhotoCraft**：固定 `ead6d219...`；本机 `cargo test -p photocraft-automation --locked --lib workspace::tests` 实报 **21 passed / 0 failed**。测试覆盖读写 authority 分离、路径/设备名拒绝、symlink escape、ambient filesystem command fail-closed、原子替换和异常清理。
- **PdfCraft**：固定 `4f6d163...`；本机 `cargo test -p pdfcraft-automation --locked --lib file_access::tests` 实报 **7 passed / 0 failed**。覆盖 read/write root、component containment、parent traversal、symlink/dangling link、以及“所有工具文件 I/O 必须先 resolve”的源码 ratchet。
- 两仓最新 release 分别为 `PhotoCraft v0.9.0`（2026-10-14）和 `PdfCraft v0.8.0`（2026-10-14）。截至最后 API 查询，PhotoCraft 固定 head checks 为 4 success、3 in progress、2 queued、1 skipped；PdfCraft 最新 head `3f5a784...` 为 6 success、1 in progress、1 skipped，均不能写成“全绿”。
- 本机 `cargo audit`：PhotoCraft lockfile 836 dependencies，**4 vulnerabilities + 7 unmaintained + 1 yanked**；PdfCraft 773 dependencies，**1 vulnerability + 4 unmaintained**。详情见各项目风险边界。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [storytold/photocraft](https://github.com/storytold/photocraft) | 66,409 | 11,604 | Rust | Apache-2.0 | 2026-10-17T23:21:00Z | **深读：capability filesystem + command/effect boundary** |
| [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | 33,273 | 2,985 | Python | Apache-2.0 | 2026-10-17T16:58:09Z | typed classifier/router，历史已深读 |
| [Niko1221/Strata](https://github.com/Niko1221/Strata) | 26,897 | 2,829 | C++ | MIT | 2026-10-17T06:50:46Z | 新项目高热，系统软件边界待后续核验 |
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 23,167 | 1,722 | Python | MIT | 2026-09-30T01:24:38Z | finite candidate typed action，历史已深读 |
| [robbietilton/Compositor](https://github.com/robbietilton/Compositor) | 17,302 | 1,688 | Swift | MIT | 2026-10-15T01:43:33Z | UI/compositor 候选观察 |
| [storytold/pdfcraft](https://github.com/storytold/pdfcraft) | 15,494 | 5,959 | Rust | Apache-2.0 | 2026-10-18T00:03:39Z | **深读：schema tool table + root policy + atomic publish** |
| [openai/math](https://github.com/openai/math) | 15,104 | 1,749 | Lean | Apache-2.0 | 2026-10-12T21:55:27Z | 形式化数学资产，非今日 Agent 工具主线 |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 15,105 | 1,157 | JavaScript | MIT | 2026-10-15T14:14:32Z | 新项目候选，成熟度待核验 |

> 表中 Stars/Forks/Language/License/时间均来自最后一轮 GitHub Repository API；License API 识别两深读仓的 `LICENSE-APACHE` 为 Apache-2.0，但两个 README 和根 `Cargo.toml` 均声明 `MIT OR Apache-2.0`。因此表格忠实保留 API 值，合规说明使用“仓库声明双许可、API 只选中 Apache 文件”。顶层许可不覆盖依赖、字体/图标/模型、release assets 与商标。

## 深读项目

### 1. storytold/photocraft

- **一句话判断**：值得学的不是 500+ 图像命令本身，而是把同一引擎暴露给 UI/CLI/JSON/MCP 时，仍用 capability directory handle、host authorization gate、预算与不确定结果语义守住 effect 边界。
- **解决的问题**：替代“Agent 拿到任意宿主路径 + 所有 engine command 都可直调 + socket 断线自动重试”的旧做法；文件 I/O 经独立 read/write capability，未迁移的 ambient-path command 先 fail-closed，发送后丢 ACK 的 mutation 不自动重放。
- **URL / API 快照**：https://github.com/storytold/photocraft ；**Stars: 66,409 / Forks: 11,604 / Language: Rust / License: Apache-2.0（API）**；`created_at=2026-09-30T13:37:48Z`，`pushed_at=2026-10-17T23:21:00Z`，`updated_at=2026-10-18T00:39:04Z`，API `open_issues_count=2772`（含 PR）。
- **固定提交 / release**：[`ead6d2197f5d0b82d70f3fddb70e472fc27ce577`](https://github.com/storytold/photocraft/commit/ead6d2197f5d0b82d70f3fddb70e472fc27ce577)，commit time `2026-10-17T23:20:33Z`；release [`v0.9.0`](https://github.com/storytold/photocraft/releases/tag/v0.9.0)，published `2026-10-14T16:36:26Z`。
- **来源交叉核验**：Repository/Commit/Release/Issues/Actions/License/Security Advisories API；README 的 Built for agents/Under the hood；`SECURITY.md`；`book/src/automation/`、`book/src/security/`；Cargo manifests/lock；automation/engine 源码；本机定向 tests/audit。

#### 架构 / 实现与数据流

```text
UI / photocraft-cli / JSON-lines / MCP
        |
        v
bounded transport + auth (TCP only) + schema/param checks
        |
        v
Headless::handle / Session::dispatch
        |                         \
        | engine command           \ doc.open/save/render/place
        v                           v
host authorize gate          AuthorizedWorkspace
  - deny ambient path          read Dir capability
  - validate params            write Dir capability
  - precondition/admit          relative handle-based I/O
        |                           |
        +--------> pure-data document/session <--------+
                         |
                         v
                  journal / history / job
                         |
            atomic stage + fsync + rename
                         |
                         v
              canonical result / inspect/read-back
```

关键层次：

1. `crates/engine` 持有 pure-data document、统一 command registry 与 journal；UI 不拥有第二套编辑语义。
2. `crates/automation` 将传输、MCP、headless RPC 和 filesystem authority 包在 engine 外。`AuthorizedWorkspace` 使用 `cap_std::fs::Dir` 句柄相对打开，而不是“先 canonicalize 字符串、再 ambient open”。
3. 对尚未改造成 capability I/O 的 engine 命令，`authorize_engine_command` 按 command id、参数与 preference surface fail-closed；安全不是由 tool description 宣称。
4. `BridgeClient` 把 failure 分成 `NotSent`、`Transport`、`TimedOut`、`Definite`：只有 caller 明确声明 read 的 `call_read` 才可在 transport failure 后重试；mutation 进入“可能已完成，先 inspect”。
5. 写入采用同目录 temporary file、sync、rename；结果仍须由上层 inspect/revision/artifact read-back 收口。

#### repo tree 摘要

```text
photocraft/
├── apps/
│   ├── photocraft/             # desktop app、control server、平台集成
│   ├── photocraft-cli/         # headless CLI/serve/MCP 入口
│   └── photocraft-web*/        # WebAssembly 前端
├── crates/
│   ├── engine/                 # command registry、session、journal、jobs、precheck
│   ├── automation/             # workspace capabilities、RPC、MCP、bridge、budgets
│   ├── doc|ops|compose|io/     # document model、操作、渲染/编解码
│   ├── codecs|psd|raw/         # 不可信格式解析面
│   └── ui-egui|gpu|plugins/    # UI/GPU/WASM plugin adapters
├── book/src/automation/        # CLI/MCP/control 与 security model
├── book/src/security/          # threat model、parser/file/release hardening
├── Cargo.toml / Cargo.lock     # workspace graph 与固定解析
└── SECURITY.md                 # 当前已实现边界与明确缺口
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/automation/src/workspace.rs` | 文件 capability 与 engine command gate | read/write authority 分离；拒绝 `..`、反斜杠、prefix/device；cap-std handle I/O；ambient path commands fail-closed |
| `crates/automation/src/bridge.rs` | GUI bridge effect certainty | 仅 loopback；55s timeout；read 可重试，mutation reply 丢失返回 outcome unknown |
| `crates/automation/src/rpc.rs` | JSON-lines RPC / batch | request/batch/reply budget、panic guard、unknown method 明确失败、TCP token/connection limit |
| `crates/automation/src/server/transport.rs` | MCP admission | 完整读取有界 frame 后才交给 rmcp，避免“合法前缀已执行、超长后缀才拒绝” |
| `crates/engine/src/jobs.rs` | command dispatch | command lookup、param validation、host gate、precondition、panic containment、journal/job terminal |
| `crates/engine/src/lib.rs` | Session API | `execute`、`precheck`、`admit`，统一同步/后台命令行为 |

#### ⭐ 源码精读

1. `AuthorizedWorkspace::read`：请求路径先转为 capability-relative path；缺 read authority 直接拒绝；打开后再确认 regular file，并按已观察长度有界读取。

```rust
pub fn read(&self, path: &str) -> Result<Vec<u8>, AutomationError> {
    let relative = request_path(path, self.read.as_ref())?;
    let root = self.read.as_ref().ok_or_else(||
        AutomationError::BadRequest(format!("{DENIED}: read authority is absent")))?;
    let mut file = root.dir.open(&relative)
        .map_err(|e| file_error("read", path, e))?;
    let metadata = file.metadata().map_err(|e| file_error("read", path, e))?;
    if !metadata.is_file() {
        return Err(AutomationError::BadRequest(
            format!("automation read path is not a regular file: `{path}`")));
    }
    read_to_observed_length(&mut file, metadata.len())
}
```

2. `Session::dispatch`：每个 command（包括 nested command）都经过 host gate；参数验证与 precondition 在 effect 前完成；panic 转成 typed error，并依靠 copy-on-edit 保持文档不变。

```rust
pub(crate) fn dispatch(
    &mut self, id: &str, params: Value, background: bool
) -> Result<Started> {
    let spec = crate::commands::find(id)
        .ok_or_else(|| EngineError::UnknownCommand(id.to_string()))?;
    if !(params.is_object() || params.is_null()) {
        return Err(EngineError::BadParams {
            cmd: id.to_string(), msg: "params must be a JSON object".into()
        });
    }
    if let Some(gate) = self.authorize { gate(id, &params)?; }
    crate::param_check::check(spec, &params)?;
    crate::filters::validate_params(id, &params)?;
    let run_params = self.admit(id, spec, &params)?;
    let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(||
        (spec.run)(self, &run_params)
    ));
    // ... typed error / background Job / Done + journal
}
```

3. `BridgeClient::dispatch`：retry policy 不是网络库默认值，而是 effect-aware；只有 read 才会在 not-sent/transport failure 后做一次 fresh attempt。

```rust
async fn dispatch(
    &self, method: &str, params: &Value, read: bool
) -> Result<Value, AutomationError> {
    match self.attempt(method, params).await {
        Ok(v) => Ok(v),
        Err(Failure::NotSent(_)) | Err(Failure::Transport(_)) if read => {
            match self.attempt(method, params).await {
                Ok(v) => Ok(v),
                Err(retry) => Err(self.failure(method, retry, read)),
            }
        }
        Err(f) => Err(self.failure(method, f, read)),
    }
}
```

4. `bounded_line`：先聚合完整、大小合规、UTF-8 合规的一行，再转发给 MCP SDK；这把“admission 通过”绑定到完整 frame，而不是流式前缀。

```rust
async fn bounded_line<R: tokio::io::AsyncRead + Unpin>(
    source: &mut BufReader<R>, maximum: usize
) -> std::io::Result<Option<String>> {
    let mut bytes = Vec::new();
    loop {
        let available = source.fill_buf().await?;
        let newline = available.iter().position(|&byte| byte == b'\n');
        let length = newline.map_or(available.len(), |at| at + 1);
        if length > maximum.saturating_sub(bytes.len()) {
            return Err(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                format!("request exceeds {maximum} bytes"),
            ));
        }
        // ... only complete accepted line is returned to dispatch
    }
}
```

#### 依赖分析与供应链风险

- 根 `Cargo.toml`：workspace dependency 共 **46** 项，其中 **25 local path / 3 git-rev pinned / 18 registry**。关键 automation 依赖 `cap-std 4`、`rmcp 3.5`、`tokio 1`、`serde_json`；engine 依赖大量本地 image/document crates、`rayon`、`blake3`。
- 三个 git dependencies 都固定 `rev`，比 moving branch 好；但仍需核 repository identity、commit availability 与 release reproducibility。`Cargo.lock` 只固定解析，不证明来源未被替换。
- 本机 `cargo audit`（database updated `2026-10-17T17:23:59+02:00`）扫描 836 lock dependencies，实报：
  - `rustls 0.23.45`：`RUSTSEC-2026-0346/0347/0348/0349` 四条；是否从 PhotoCraft 实际可达待按 ECH/Debug/certificate-compression/session-resumption 路径核验，不能直接写成已利用。
  - 7 个 unmaintained warnings（含 `paste`、`proc-macro-error`、`rustybuzz`、`ttf-parser`、zbus/zvariant 家族）和 yanked `yoke-derive 0.8.3`。
- GitHub repository advisories API 返回空；Dependabot 403。因此本机 advisory findings 优先保留，空 API 不可抵消它们。

#### 可复用经验

- 当 Agent 需要文件读写时，应优先把 root 打开为 directory capability 并相对句柄执行 I/O，而不是只做 path string canonicalization，因为后者仍留 check→open TOCTOU；边界是同 root 内的恶意协作进程、挂载与 OS sandbox 仍需另行治理。
- 当 RPC mutation 的 ACK 丢失或 timeout 时，应优先返回 `outcome_unknown/needs_verification` 并读取 revision/artifact/world state，而不是自动重试，因为请求可能已提交；边界是 read 的重试资格也应由 host registry 而非 caller prose 声明。
- 当同一 engine 同时暴露 CLI/MCP/UI 时，应优先让所有路径汇入同一 host authorization/param/precondition chokepoint，因为 transport schema 与 tool annotations 不是 enforcement；边界是 authenticated client 仍可能拥有过宽 tool surface。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/capability-effect-receipt-v0/` 做纯 Python fixture：

1. `OperationSpec(effect=read|write, scope, target, replayability)`；
2. fake directory capability 只接受 component-safe relative path；
3. 模拟 `not_sent / reply_lost_after_commit / definite_error`；
4. 断言 write reply-lost 不重试，进入 `needs_verification`；read 才允许一次 retry；
5. 成功 write 必须 read-back content hash/revision 才 terminal `completed`。

只使用临时目录和 synthetic bytes，不连接 MCP/provider，不修改 Hermes config/cron/skills/curated。

#### 风险边界

- **License**：GitHub API/License API 识别 Apache-2.0；README、根 manifest 同时声明 `MIT OR Apache-2.0`。资产在 `ATTRIBUTION.md`，brand/trademark 不随代码许可；依赖许可证需单独审。
- **维护活跃度**：仓库 2026-09-30 创建、10-14 发布 v0.9.0、10-17 仍 push；高速迭代但 README 明示 early alpha。最后观测 head checks 尚有 in-progress/queued，不能写全绿。
- **安全**：本机 audit 有 4 vulnerabilities；`SECURITY.md` 明确缺少 JSON-depth、render/document-memory、command-duration、client identity、encryption、audit controls；TCP token 不提供 per-client/per-tool capability。
- **局限/不适用**：本机只验证 automation workspace 21 tests，未跑 1,700+ 全仓、GUI/GPU/Web/PSD corpus、真实 MCP/loopback control、release binary/signature。open issues 包括启动/崩溃和大量 action round-trip 问题。
- **不能自动执行**：不安装 release、不启 MCP/control server、不导入用户图片、不自动改 Hermes/OpenClaw 配置、provider、cron 或 secret。

#### ⭐ Skill 升格判断

**需二次验证**。能力模式与现有 `research/github-hot-project-learning`、`foundation/path-portability`、`foundation/shared-memory-bridge` 及历史 effect/verification 候选高度重叠；应先做 capability/effect receipt fixture 并证明能捕获真实 Hermes 回归，再更新已有 class-level contract，不能创建 PhotoCraft 专属 shared skill。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/capability-effect-receipt-v0/`。
- 若 fixture 通过，优先更新：
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：外部工具“发送成功 ≠ effect 完成”，要求 certainty + read-back；
  - `capabilities/skills/foundation/path-portability/SKILL.md`：高权 I/O 除 root resolution 外增加 component containment、no-follow/capability handle 注意事项；
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：terminal receipt 增加 `not_sent|unknown|verified`。
- Hermes adapter 候选：在未来高权工具 registry 增加 `effect/read_only/replayable/requires_readback` host-owned metadata；本日报只提出 candidate，不写 active skill/config。

### 2. storytold/pdfcraft

- **一句话判断**：值得学的是“一个 schema tool table 驱动 library/CLI/MCP + 分离 read/write roots + atomic publication + compact discovery”，同时它也诚实展示了 canonicalize-check 再 ambient-open 仍存在 TOCTOU 的边界。
- **解决的问题**：替代 CLI、MCP 与 library 各复制一份 PDF 操作逻辑，和“文件存在/exit 0 就算保存完成”的旧做法；所有 tool 先由 schema registry 校验，再进入 `Automation::call`，保存先 validate bytes、原子写、最后 mark_saved。
- **URL / API 快照**：https://github.com/storytold/pdfcraft ；**Stars: 15,494 / Forks: 5,959 / Language: Rust / License: Apache-2.0（API）**；`created_at=2026-09-30T13:39:37Z`，最后 `pushed_at=2026-10-18T00:03:39Z`，`updated_at=2026-10-18T00:34:20Z`，API `open_issues_count=1527`（含 PR）。
- **固定提交 / release**：源码 clone 固定 [`4f6d16380a13e6d584bba369d7118ba6e60b608a`](https://github.com/storytold/pdfcraft/commit/4f6d16380a13e6d584bba369d7118ba6e60b608a)，commit time `2026-10-17T23:11:26Z`；研究期间 main 前进至 [`3f5a784c2cb5934ed429ee52a07c4abeb180138b`](https://github.com/storytold/pdfcraft/commit/3f5a784c2cb5934ed429ee52a07c4abeb180138b)，commit time `2026-10-18T00:03:38Z`。release [`v0.8.0`](https://github.com/storytold/pdfcraft/releases/tag/v0.8.0)，published `2026-10-14T15:21:59Z`。
- **来源交叉核验**：Repository/Commit/Release/Issues/Actions/License/Security Advisories API；README 的 Built for agents/How it's built/What's next；Cargo manifests/lock；automation/engine 源码；本机定向 tests/audit。固定 head 没有根 `SECURITY.md`（Contents API 404），故不编造安全政策。

#### 架构 / 实现与数据流

```text
pdfcraft-cli run | pdfcraft-cli mcp | Rust embedder
                     |
                     v
             one ToolDef schema table
       name + input_schema + read_only/destructive
                     |
                     v
             Automation::call(name,args)
         schema check -> tool dispatch -> Session/Edit
              |                        |
              | read/write path        | in-memory edit/undo
              v                        v
      resolve root policy        canonical document state
      (read != write)                   |
              |                 check_save(candidate bytes)
              |                        |
              +----------> atomic stage/sync/rename
                                       |
                                 mark_saved only after write
                                       |
                                structured JSON / MCP result
```

可迁移点不是 PDF domain，而是 control/data plane：

1. `tools.rs` 的 canonical schema 同时服务 native call 与 MCP；`mcp.rs` 只做 transport/projection，并给 compact mode 提供 `tool_search + tool_call`，降低工具列表上下文税。
2. `Automation::call` 先拒绝非 object args、unknown tool、schema mismatch，再进入集中 dispatch；mutations 经 `Session::apply`，不是由 MCP adapter直接改文件。
3. `AutomationRoots` 分离 read/write，symlink 和 component boundary 可测试；但源码注释明确“check 后再 open”可被本机另一进程换 link，不能把它称作 capability-safe。
4. `doc_save` 的状态顺序是 candidate bytes → `check_save` → atomic write → `mark_saved`；写失败不会把内存 document 假标为 clean。
5. batch 先有界 discovery，再逐文件重验 path/link；publish 用 `persist_noclobber`，避免并发覆盖已有文件。

#### repo tree 摘要

```text
pdfcraft/
├── apps/
│   ├── pdfcraft/                # native desktop
│   ├── pdfcraft-cli/            # run/mcp/ui control、root flags
│   └── pdfcraft-web/            # WebAssembly frontend
├── crates/
│   ├── automation/              # canonical tools、MCP、batch、file policy
│   ├── engine/                  # Session、Document、Edit、export façade
│   ├── cos|filters|crypt/       # PDF object/filter/security handler
│   ├── render|content|fonts/    # rendering/text/font pipeline
│   ├── organize|annot|forms/    # domain edits
│   └── redact|sign|ocr|js/      # 高风险复杂功能面
├── vendor/                      # patched hayro/lopdf/winit 等
├── Cargo.toml / Cargo.lock      # workspace、patch graph、固定解析
└── xtask/                       # corpus/gates/release helpers
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/automation/src/lib.rs` | canonical tool executor | `Automation::call`、集中 schema check/dispatch、save validate→write→mark_saved、path resolve |
| `crates/automation/src/tools.rs` | ToolDef 真相源 | name/title/schema/read_only/destructive，供 CLI/MCP 共用 |
| `crates/automation/src/mcp.rs` | MCP thin adapter | stdio only、compact discovery、tool annotations、structuredContent、panic guard |
| `crates/automation/src/file_access.rs` | read/write root policy | canonicalize nearest ancestor、component containment、symlink/dangling/device handling；明确 TOCTOU 边界 |
| `crates/automation/src/batch.rs` | bounded batch publication | 10k entries/64 depth/512 MiB caps、先 discovery、执行前重验、noclobber publish |
| `apps/pdfcraft-cli/src/automation_args.rs` | root admission | duplicate flag/empty operand fail closed，避免 malformed args 静默取消 confinement |

#### ⭐ 源码精读

1. `Automation::call`：canonical tool table 先做 shape/schema 校验；adapter 无权跳过。`ToolError` 区分 unknown/invalid/failed，避免把模型调用错误混成产品失败。

```rust
pub fn call(&mut self, name: &str, args: &Value) -> Result<Vec<Content>> {
    let empty = json!({});
    let args = if args.is_null() { &empty } else { args };
    if !args.is_object() {
        return Err(ToolError::InvalidArgs(
            "arguments must be a JSON object".into()
        ));
    }
    let def = tools::find(name)
        .ok_or_else(|| ToolError::UnknownTool(name.into()))?;
    tools::check_args(def, args)?;
    let a = Args(args);
    let out = match name {
        "doc_open" => self.doc_open(&a)?,
        "doc_save" => self.doc_save(&a)?,
        // ... all tools converge here
        _ => return Err(ToolError::UnknownTool(name.into())),
    };
    Ok(vec![Content::Json(out)])
}
```

2. `AutomationRoots::check_path`：read/write authority 独立缺省拒绝，真实 path 与 root 按 component 比较，避免 `/work2` 字符串前缀冒充 `/work`。

```rust
pub fn check_path(
    &self, shown: &str, target: &Path, access: Access
) -> Result<(), String> {
    let root = match access {
        Access::Read => self.read.as_ref(),
        Access::Write => self.write.as_ref(),
    };
    let Some(Root { resolved: folder, shown: root_shown }) = root else {
        return Err(format!(
            "automation filesystem access is not granted: {access:?} authority is absent: {shown}"
        ));
    };
    if inside(&resolve(shown, target)?, folder) { return Ok(()); }
    Err(format!("automation path rejected: outside the root {}: {shown}",
        root_shown.display()))
}
```

3. `publish_save`：先验证 candidate，再 publish，再更新内存 saved state。顺序本身就是 completion contract；任何前置绿色都不能提前 terminal completed。

```rust
fn publish_save(
    &mut self,
    id: DocId,
    target: &Path,
    bytes: Arc<Vec<u8>>,
    incremental: bool,
    write: impl FnOnce(&Path, &[u8]) -> Result<()>,
) -> Result<Value> {
    self.session.check_save(id, &bytes).map_err(failed)?;
    write(target, &bytes)?;
    let path = target.to_string_lossy().into_owned();
    self.session.mark_saved(id, bytes.clone(), Some(path.clone()))
        .map_err(failed)?;
    let doc = self.session.get(id)
        .ok_or_else(|| failed("the saved document is no longer open"))?;
    Ok(json!({"path": path, "bytes": bytes.len(),
              "incremental": incremental, "document": summary(doc)}))
}
```

4. `doc_batch` 的执行前重验：discovery 不是持续授权；每个 item 在 process 前再次 resolve 并比对 immutable real path，publish 不覆盖已有名称。

```rust
let current = self.resolve(
    path.to_str().ok_or_else(|| failed("input path is not UTF-8"))?,
    false,
)?;
if linked(&path.symlink_metadata().map_err(failed)?)
    || absolute(&current)? != path
{
    return Err(failed("input path changed after discovery"));
}
let (bytes, log) = recipe.process(&current)?;
let target = self.resolve(target_str, true)?;
if !target.starts_with(&out) {
    return Err(failed("output path leaves out_dir"));
}
let output = publish(&target, &bytes)?;
```

#### 依赖分析与供应链风险

- 根 `Cargo.toml`：workspace dependency 共 **53** 项，其中 **33 local path / 4 git-rev pinned / 16 registry**。核心 PDF 路径含 `hayro 0.7.1`、`hayro-syntax 0.7.2`、`lopdf 0.45`；automation 直接依赖 `sha2 0.11`、`tempfile 3.27`、`png 0.18`、`serde_json`，MCP feature 引入 `base64`。
- `[patch.crates-io]` 本地 vendor/patch `hayro*`、`lopdf`、`winit`、`egui-wgpu`、`vello_common`。优点是修复可审计、构建不依赖 moving patch branch；风险是上游 CVE/bug 修复不会自动进入，必须维护 patch provenance 与 differential tests。
- 四个 `craft-libs` git dependencies 固定 commit rev。仍需 release provenance 与重现构建；Git commit pin 不等于签名。
- 本机 `cargo audit` 扫描 773 lock dependencies，实报 `rsa 0.10.0-rc.18` 的 **RUSTSEC-2023-0071 Marvin timing sidechannel**，以及 4 个 unmaintained warnings（`proc-macro-error`、zbus/zvariant 家族）。`rsa` 位于签名功能图；实际可达性、密钥类型与部署暴露待核验，不能写成已被利用。
- repository advisories API 空、Dependabot 403，不代表无漏洞。固定 commit 缺根 `SECURITY.md`，私密报告流程待核验。

#### 可复用经验

- 当一个工具要同时服务 native API、CLI 与 MCP 时，应优先建立 canonical ToolDef/schema/executor，再让 transport 只做 projection，因为复制 schema/dispatch 会产生参数与安全漂移；边界是 annotation 必须和实现做 ratchet test。
- 当保存会改变内存 dirty state或触发下游完成时，应优先执行 `validate candidate → atomic publish → authoritative read-back/mark_saved → receipt`，因为 candidate 合法和 write return 都不是完整业务完成；边界是 rename 后、mark 前 crash 仍需启动 reconciliation。
- 当批量任务会遍历不可信目录时，应优先先做有界 discovery，再逐 item effect-time 重验 path identity，并采用 noclobber/幂等 publish，因为早期扫描结果会陈旧；边界是 canonicalize-check 与 ambient open 之间仍存在 TOCTOU。

#### 可尝试实验（30 分钟）

扩展同一 `capability-effect-receipt-v0` fixture：建立一个 canonical `ToolDef(name, input_schema, effect, replayable, requires_readback)`，生成两个 adapters（CLI JSON 与 fake MCP）；运行 conformance corpus，断言 unknown key、缺 write authority、symlink swap、reply lost、publish collision 在两个 adapters 得到相同 typed terminal。只测试 synthetic temp files，不运行 PDF parser/JS/OCR/signing。

#### 风险边界

- **License**：GitHub API/License API 为 Apache-2.0；README/root manifest 声明 MIT OR Apache-2.0；`ATTRIBUTION.md` 和 vendor license 需一并审，ArtCraft brand/trademark 不在代码许可内。
- **维护活跃度**：仓库 2026-09-30 创建，v0.8.0 于 10-14 发布，10-18 仍推进 main；README 明示 alpha，hardening 仍会从 hostile files 找到 crash/hang。研究结束时最新 head checks 尚有 1 in-progress。
- **安全**：本机 audit 有 1 vulnerability；file policy 源码明确有 check→open race；MCP 本身 stdio only 是优点，但 tool surface 含 JS、OCR、signing、redaction 等复杂输入/crypto 功能。
- **局限/不适用**：本机只跑 file_access 7 tests，完整 automation/all-workspace、PDF corpus、qpdf/hayro/poppler oracle、GUI/print/web/release binary 未跑。公开 issues #3117/#3118 显示 redaction audit 对多种绘制语义存在 false clean/false positive，安全判断不可直接依赖单一 audit tool。
- **不能自动执行**：不处理私有 PDF，不启 MCP，不调用打印/JS/OCR/签名，不安装 release，不自动修改 Hermes/OpenClaw 配置、cron、provider 或 shared active facts。

#### ⭐ Skill 升格判断

**需二次验证**。canonical ToolDef + adapter conformance 与现有 shared-skill governance/verification/orchestrator 方法高度相关，但 PdfCraft 的 root 实现仍明确存在 TOCTOU；只抽象 contract，不迁移 PDF runtime，也不创建项目专属 skill。

#### ⭐ Hermes / shared hub 落地路径

- POC 与 PhotoCraft 合并：`runtime/hermes/github-learning-poc/capability-effect-receipt-v0/`，避免每日项目各造一个 skill。
- 优先更新已有 `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：增加 canonical operation registry、adapter conformance、validate→publish→read-back→terminal 顺序。
- 在 `capabilities/skills/research/github-hot-project-learning/SKILL.md` 增加供应链结论约束：GitHub advisory empty/Dependabot 403 不得覆盖本机 lockfile audit。
- 若未来 Hermes 引入大量 MCP tools，再在 Hermes 本地 adapter 层实现 compact `tool_search + tool_call`；必须保留 effect metadata，不能因 compact mode 把 mutation 伪装为 read-only。

## 跨项目机制对照

| 机制 | PhotoCraft | PdfCraft | 对 shared hub 的判断 |
|---|---|---|---|
| canonical execution | engine command registry | ToolDef + `Automation::call` | 可抽象为 host-owned operation registry |
| filesystem isolation | cap-std directory handle，强于字符串检查 | canonicalize/component check，有 TOCTOU 注释 | shared contract 应把两者区分为 `capability_enforced` / `checked_only` |
| effect certainty | explicit not-sent/transport/timed-out/definite | MCP/tool errors结构化，但 crash recovery receipt较弱 | 增加 `unknown` terminal 与 read-back |
| publish | temp+sync+rename | validate+atomic write+mark_saved；batch noclobber | 可形成统一 completion sequence |
| compact tools | MCP registry/commands filtering | `tool_search + tool_call` | 适合工具多时降上下文税，但 metadata 不得丢 |
| dependency state | audit 4 vuln | audit 1 vuln | security status 必须绑定 lock + scanner DB time |

## 经验沉淀

1. 当 Agent 工具涉及文件或其他宿主资源时，应优先使用 capability handle 与 read/write authority 分离，并把仅 canonicalize-check 的实现标成较弱 enforcement，因为路径通过检查不代表 effect-time 对象未被替换；边界是 capability 仍不等于完整 OS sandbox。
2. 当 mutation 请求出现 timeout、断线或 ACK 丢失时，应优先进入 `outcome_unknown/needs_verification` 并做权威 read-back，而不是自动重试，因为 transport failure 不证明 effect 未发生；边界是 read-only 身份必须由 host registry 决定。
3. 当同一能力跨 CLI、MCP、UI 或 future agent adapter 暴露时，应优先维护 canonical schema/executor/effect metadata 和 adapter conformance ratchet，因为复制实现会漂移；边界是 schema-valid 不等于获得 authorization。
4. 当保存/发布会驱动 completed 状态时，应优先执行 `candidate validation → atomic publish → read-back/mark → terminal receipt`，因为 artifact 存在、rename 成功或内存 flag 都只覆盖一层；边界是 publish 与 mark 间 crash 仍需 reconciliation。
5. 当 batch 先扫描后执行时，应优先冻结 coverage denominator、设置 entries/depth/bytes 上限，并在每个 effect 前重验 identity，因为 discovery result 会陈旧；边界是本机协作进程仍可制造 TOCTOU。
6. 当 GitHub Security Advisories 为空或 Dependabot API 返回 403 时，应优先保留 scanner 名称、lock revision、advisory DB 时间和真实 findings，而不是写“无漏洞”；边界是 audit 命中还需 reachability 分析，audit clean 也不是安全证明。
7. 当新项目方法与已有 shared skill/POC 高度重叠时，应优先合并到已有 class-level contract 并做 fixture，而不是按 repo 创建新 skill；边界是确有独立触发条件、输入输出契约和验证面时才升格。

## Hermes / shared hub 统一落地建议

### Candidate POC

`runtime/hermes/github-learning-poc/capability-effect-receipt-v0/`

最小 schema：

```json
{
  "operation_id": "immutable-id",
  "effect": "read|write|external",
  "scope": "agent/run/resource",
  "target_identity": "canonical target",
  "enforcement": "capability_enforced|checked_only|none",
  "replayable": false,
  "dispatch_state": "not_sent|sent|unknown|acknowledged",
  "readback": {"required": true, "status": "pending|verified|mismatch"},
  "terminal": "completed|blocked|failed|needs_verification"
}
```

### 预期验收

- 两个 adapters 对同一 fixture 产生相同 terminal；
- write reply lost 永不自动 retry；
- `checked_only` 的 symlink swap fixture 不得投影为安全完成；
- publish 后 read-back mismatch 必须 failed/needs_verification；
- 不读 private data、不连接 provider/MCP、不改 config/cron/skills/curated。

## Skill 升格总判断

- **今日不创建新 shared skill，不写 curated active fact。**
- 两项目都判定 **需二次验证**；先完成统一 POC，并与 `research/github-hot-project-learning`、`autonomous-learning/orchestrator-protocol`、`foundation/path-portability`、`foundation/shared-memory-bridge` 去重。
- 若 POC 能真实发现至少一个现有 workflow 的误判，再优先迭代已有 skill；若只复述既有 verification/effect 经验，则保留在 inbox/runtime，不升格。

## 明日继续

1. 在 runtime 创建 `capability-effect-receipt-v0` 的 8 个 synthetic fixtures：read retry、write reply-lost、symlink swap、missing authority、unknown key、publish collision、read-back mismatch、crash-after-publish-before-mark。
2. 固定 PhotoCraft/PdfCraft 后续 head，检查上述 supply-chain advisories 是否在 lockfile 更新中消失，并区分 direct/transitive/reachable；不等待 README 自报。
3. 继续深读一个“使用真实 descriptor-relative I/O + operation receipt”的非图像项目，验证今天模式不是同一组织代码风格造成的单源偏差。

## 候选反哺

### Candidate Facts

- [ ] topic: capability filesystem 强度应与 canonicalize-check 分级 | evidence: `photocraft/workspace.rs` 使用 cap-std directory handle；`pdfcraft/file_access.rs` 明示 check→open race | 建议: create（待 POC/第三源验证） | 安全级别: medium
- [ ] topic: mutation transport failure 必须保留 outcome unknown | evidence: `photocraft/bridge.rs` 的 `NotSent/Transport/TimedOut/Definite` 与 read-only retry | 建议: update 既有 completion/effect 候选 | 安全级别: medium
- [ ] topic: security API empty 不得覆盖 lockfile audit findings | evidence: 两仓 advisories empty、Dependabot 403；本机 cargo audit 分别 4/1 vulnerabilities | 建议: update GitHub-learning workflow | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: capability-effect-receipt-v0 | 可复用场景: Hermes/future-agent 高权 tool、MCP adapter、文件发布与恢复 | 是否建议 shared: yes（仅 POC 通过后更新既有 skill） | 原因: 跨 agent 横切，但与现有 orchestrator/verification/path 能力重叠，必须先去重
- [ ] 名称: canonical-tool-adapter-conformance | 可复用场景: CLI/MCP/UI 多 adapter | 是否建议 shared: yes（合并入 orchestrator protocol） | 原因: 可防 schema/effect metadata 漂移，不应创建项目专属 skill

### Candidate Open Questions

- [ ] 问题: Hermes 当前 tool registry 是否有 host-owned read_only/replayable/requires_readback metadata，而非只靠 prompt/tool name？ | reason: gap | priority: high
- [ ] 问题: capability directory handle 在 WSL、Windows mount、容器 bind mount 和 network filesystem 上的 no-follow/rename 语义是否一致？ | reason: adaptation | priority: high
- [ ] 问题: PhotoCraft rustls advisories与 PdfCraft rsa advisory 在各自 release artifact 中是否真实可达？ | reason: gap | priority: medium
- [ ] 问题: crash-after-publish-before-mark 应由启动 reconciler、journal 还是 content-addressed receipt 收口？ | reason: adaptation | priority: high

### 不应自动落地

- 不自动安装或运行两个产品的 release/MCP/control server，不处理用户图片/PDF。
- 不自动改 Hermes/OpenClaw 配置、provider、model、cron、secret 或全局 tool 权限。
- 不复制上游源码到 shared skill；只抽象机制，并保留 MIT/Apache、资产、商标与依赖许可边界。
- 不把本日报候选直接写入 curated active facts；需评分、证据、去重、脱敏、POC 和总控/人工审查。
- 不把 cargo-audit finding 直接表述为已利用漏洞，也不把 GitHub advisories 空数组表述为无漏洞。

## 知识库路径

审计通过后由 orchestrator 复制到 `03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-10-18-GitHub热门项目学习日报.md`；此处使用知识库根相对路径，避免写死宿主绝对路径。
