# 2026-07-29 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> GitHub API 核验时间：2026-07-29T07:30:55+08:00  
> 固定源码快照：`andrewyng/openworker@f96ad4c8e6865f0aec519681a3717b6bcdd81546`、`vercel-labs/scriptc@20c3a6c27da4807f607ebe496663842b67e87f0e`  
> 发现口径：GitHub Search API，查询 `created:>=2026-07-01 stars:>100`，按 stars 降序；深读仓库元数据再用 Repository API 单独核验。Stars 与更新时间会继续变化，本文数字只代表上述查询时点。

## 今日结论

今天的主线是**把“不确定或不完整能力”关进可验证的契约**：OpenWorker 把 autonomy、交互位置和授权拆开，并将持续授权绑定到 `tool + exact target + task`；scriptc 把可静态编译、显式动态岛和拒绝分成三层，用 typed IR、编号诊断和 differential oracle 防止静默误编译。对 Hermes/shared hub 的共同启示是：**能力声明只能是申请；宿主必须在最终边界按 scope/effect/capability 重验，并把拒绝、降级和已知差异做成可测试终态。**

## 证据与执行摘要

- GitHub API：用 `gh api` 查询发现列表，并逐仓库核验 stars、forks、language、license、created/updated/pushed、latest release 与 issues。
- 源码：对两个仓库执行 `git clone --depth 1`；固定 commit 后分别统计 **450** 与 **2,843** 个 tracked paths。
- OpenWorker：读取 README、CI、权限/风险/unattended/workspace trust 源码和测试、release `v0.1.6`、issue #302；使用 `uv` 创建隔离 venv 并安装 commit 固定的依赖，定向测试真实返回 **34 passed, 5 deselected**。
- scriptc：读取 README、How It Works、Limitations、CHANGELOG、CI、compiler pipeline、IR validator、differential harness、vendor 清单、release `v0.0.17`、issues #35/#40。`pnpm install --frozen-lockfile` 与 workspace build 真实成功，但环境只有 Node 22（仓库要求 Node ≥24），构建输出有 unsupported-engine warning。
- scriptc 定向测试：IR **5 passed**、diagnostics **100 passed**；C emitter 的 4 项因本机无 `clang` 全部 blocked。完整 differential corpus 实际枚举 **1,028** 项，但都因 `clang ENOENT` 或动态路径缺 `cmake` 失败，不能宣称 native equivalence 在本机通过。
- 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-07-29/`。浅克隆与依赖目录均属于 runtime 临时证据，不进入 curated。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | Created / Updated (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | 23,234 | 4,400 | Rust | Apache-2.0 | 2026-07-14 / 2026-07-28T23:20:57Z | 昨日已深读，今日只作热度参照 |
| [JustVugg/colibri](https://github.com/JustVugg/colibri) | 20,599 | 2,085 | C | Apache-2.0 | 2026-07-01 / 2026-07-28T23:28:54Z | 昨日已深读，今日只作热度参照 |
| [Fei-Away/Codex-Dream-Skin](https://github.com/Fei-Away/Codex-Dream-Skin) | 12,568 | 1,255 | JavaScript | NOASSERTION | 2026-07-15 / 2026-07-28T23:21:23Z | License 未识别，不复制源码 |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | **9,978** | 1,310 | Python | **MIT** | 2026-07-20 / 2026-07-28T23:30:21Z | **深读：scope/effect/approval** |
| [unicity-aos/aos-ce](https://github.com/unicity-aos/aos-ce) | 7,710 | 13 | Rust | NOASSERTION | 2026-07-12 / 2026-07-28T23:30:30Z | License 边界待核验 |
| [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) | 7,580 | 578 | Python | Apache-2.0 | 2026-07-15 / 2026-07-28T23:28:34Z | 候选：图像到程序的质量门控 |
| [elder-plinius/T3MP3ST](https://github.com/elder-plinius/T3MP3ST) | 5,274 | 1,092 | TypeScript | AGPL-3.0 | 2026-07-02 / 2026-07-28T22:02:03Z | 攻防与 AGPL 边界高，不自动运行 |
| [vercel-labs/scriptc](https://github.com/vercel-labs/scriptc) | **2,108** | 40 | TypeScript | **Apache-2.0** | 2026-07-22 / 2026-07-28T23:27:19Z | **深读：显式能力包络与差分验证** |

说明：`NOASSERTION` 仅表示 GitHub API 没有识别出 SPDX license，不等于无版权限制；未深读项目不做代码实现结论。Stars 不是质量、安全性或真实采用率证明。

## 深读项目

### 1. andrewyng/openworker

**基本信息（GitHub Repository API）**

- URL：https://github.com/andrewyng/openworker
- Stars：**9,978**；Forks：**1,310**；Language：Python；License：**MIT**。
- 创建：2026-07-20T01:52:32Z；updated：2026-07-28T23:30:21Z；pushed：2026-07-28T19:34:17Z；API `open_issues_count=270`（该字段包含 PR，不能等同于缺陷数）。
- 固定 commit：[f96ad4c8e686](https://github.com/andrewyng/openworker/commit/f96ad4c8e6865f0aec519681a3717b6bcdd81546)，commit 时间 2026-07-28T19:34:12Z。
- 最新 release：[v0.1.6](https://github.com/andrewyng/openworker/releases/tag/v0.1.6)，published 2026-07-23T15:59:36Z；release body 只有 compare 链接，不据此虚构功能清单。
- 活跃 issue：[#302](https://github.com/andrewyng/openworker/issues/302)，报告 macOS `Info.plist` 缺日历/提醒 usage description，导致 calendar MCP 工具无系统授权提示而静默失败；截至查询时仍 open。

#### 一句话判断

值得学的不是“桌面 Agent 又多一个”，而是它把**风险分类、模式上限、路径 scope、任务级 exact-target grant、unattended 交互路由和 audit citation**拆成独立层；这能直接检验 Hermes cron 在“无人在线”时是否错误地把不可询问当成可自动授权。

#### 解决的问题：替代了什么旧做法

它替代三类危险做法：

1. 仅按工具名授权，例如“这个任务总能用 `send_message`”，却不绑定具体 channel/recipient。
2. 把 unattended 误解成更高自治；实际它只改变“人在哪里回答”，需要审批的调用仍应挂起。
3. 仓库自带配置一出现就生效，或命令 allowlist 用字符串前缀，导致 workspace 内容自行扩大执行权。

源码中的约束组合为：risk 先归类；只读模式先拒绝 consequential effect；本地写入始终受 writable root 限制；持续授权只给 external risk、声明了 target argument 且 exact target 命中的调用；exec 永远不能生成 standing rule；shell allowlist 遇到 chaining/redirection/substitution 就拒绝自动放行；workspace 配置只有用户信任 canonical path 后才贡献 command allowances。

#### 架构 / 实现与数据流

```text
GUI / TUI / Slack / scheduled automation
                 │
                 ▼
        TurnEngine + ToolRegistry
                 │ proposed tool + args + metadata
                 ▼
      risk.classify() -> RiskClass
                 │
                 ▼
 PermissionEngine.evaluate(mode, roots, task_rules)
      │              │                 │
      │ allow        │ ask             │ hard deny
      ▼              ▼                 ▼
  executor      inline / Inbox      tool result
      │          (unattended)        blocked
      ▼
 TOOL_FINISHED + audit entry citing actual standing rule
```

关键不变量：

- `unattended` 只改变 approval/question 的到达位置，不提升 permission mode。
- standing rule 身份是 `(owning task, tool, exact target)`；read-only mode 仍优先拒绝。
- local write 由 canonical writable root 约束；external effect 用 target；exec 不得长期授权。
- permission declaration 与 enforcement 分开，`PermissionEngine` 决策后仍需 TurnEngine/执行器真正遵守。

#### Repo tree 摘要

```text
openworker/
├── README.md / LICENSE              # 产品边界与 MIT license
├── pyproject.toml                   # Python 运行时依赖；aisuite 固定 git commit
├── coworker/
│   ├── engine.py                    # turn/tool/approval lifecycle
│   ├── permissions.py               # mode、root、allowlist、task rule 决策
│   ├── risk.py                      # READ/WRITE_LOCAL/EXEC/EXTERNAL 分类
│   ├── unattended.py / inbox.py     # 无人值守标记与挂起审批
│   ├── workspace_trust.py           # 用户拥有的 canonical path trust
│   ├── automation/                  # schedule、task、run 与 standing grants
│   ├── connectors/ / mcp/           # 外部工具与 MCP 接入
│   └── providers/                   # provider-neutral 模型适配
├── surfaces/gui/                    # React + Tauri desktop；npm/Cargo lock
├── stt/                             # Rust speech-to-text sidecar
├── tests/                           # backend 权限、durable run、connector fixtures
└── .github/workflows/ci.yml         # Python、GUI unit、hermetic Playwright lanes
```

固定 commit 的 tracked paths 为 **450**。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `coworker/risk.py` | side-effect taxonomy | 内建写入/exec 按名归类，metadata approval 映射 external，其他默认 read |
| `coworker/permissions.py` | 最终授权决策 | read-only、root、mode、session allow、task exact-target rule、shell parser gate |
| `coworker/unattended.py` | per-session route flag | 只持久化交互位置，不改变 autonomy ceiling |
| `coworker/workspace_trust.py` | repo-provided allowance trust | canonical path、0600、temp+replace；信任绑定路径而非配置快照 |
| `tests/test_standing_approvals.py` | 授权生命周期 fixture | exec 不可 mint、target exact match、规则持久化/撤销、blocked run 不阻塞其他 task |
| `tests/test_tools_permissions.py` | permission gate fixture | traversal、plan、custom、auto、shell allowlist |
| `.github/workflows/ci.yml` | CI 证据 | Python 3.12 pytest；Node 20 GUI unit/e2e；actions 只 pin major tag |
| `pyproject.toml` | dependency truth | provider SDK、FastAPI、MCP、PDF、browser/messaging extras；无根 Python lockfile |

#### 源码精读（固定 commit）

**代码块 1：风险分类把 effect 变成宿主数据**  
来源：[`coworker/risk.py#L18-L53`](https://github.com/andrewyng/openworker/blob/f96ad4c8e6865f0aec519681a3717b6bcdd81546/coworker/risk.py#L18-L53)

```python
class RiskClass(str, Enum):
    READ = "read"
    WRITE_LOCAL = "write_local"
    EXEC = "exec"
    EXTERNAL = "external"

def classify(tool_name, metadata=None, overrides=None) -> RiskClass:
    if overrides is not None:
        ov = overrides(tool_name)
        if ov is not None:
            return ov
    base = _BASE.get(tool_name)
    if base is not None:
        return base
    if bool(getattr(metadata, "requires_approval", False)):
        return RiskClass.EXTERNAL
    return RiskClass.READ
```

逻辑：权限引擎不再散落硬编码“危险工具”，而消费统一 effect class。可迁移点是 schema；不可照搬的边界是未知工具默认 `READ` 偏乐观，尤其 MCP/插件 metadata 错误时会低估风险。Hermes 候选应让 unknown 默认为 `UNKNOWN/BLOCKED`，或要求 host registry 有已审计 effect declaration。

**代码块 2：授权顺序把模式上限和 writable root 放在 grant 之前**  
来源：[`coworker/permissions.py#L120-L178`](https://github.com/andrewyng/openworker/blob/f96ad4c8e6865f0aec519681a3717b6bcdd81546/coworker/permissions.py#L120-L178)

```python
def evaluate(self, tool_name, arguments, metadata=None) -> Decision:
    risk = classify(tool_name, metadata, self.risk_overrides)
    consequential = is_consequential(risk)

    if self.mode in READ_ONLY_MODES and consequential:
        return Decision(False, f"{self.mode.value} mode is read-only")

    if risk is RiskClass.WRITE_LOCAL:
        path = arguments.get("path")
        if path is not None and not self._under_writable_root(path):
            return Decision(False, f"path is not in a writable directory: {path}")

    if not consequential:
        return Decision(True, "low risk")
    if self.mode is Mode.AUTO:
        return Decision(True, "full access")
    # session/task/custom checks follow; otherwise needs_user=True
```

逻辑：read-only 是 ceiling；write path scope 在 AUTO 前检查，因此全自动也不能逃出 writable roots。边界是 write 工具若未提供 `path`，此处不会拒绝；effect schema 必须规定 scope-bearing 参数，不能让参数缺失意味着“全局”。

**代码块 3：standing grant 只绑定 external risk 的 exact target**  
来源：[`coworker/permissions.py#L62-L80`](https://github.com/andrewyng/openworker/blob/f96ad4c8e6865f0aec519681a3717b6bcdd81546/coworker/permissions.py#L62-L80) 与 [`#L160-L171`](https://github.com/andrewyng/openworker/blob/f96ad4c8e6865f0aec519681a3717b6bcdd81546/coworker/permissions.py#L160-L171)

```python
def standing_rule_candidate(tool_name, arguments, metadata=None, overrides=None):
    if classify(tool_name, metadata, overrides) is not RiskClass.EXTERNAL:
        return None
    arg = target_arg_for(tool_name)
    if arg is None:
        return None
    value = str((arguments or {}).get(arg) or "").strip()
    return value or None

if tool_name in self.task_rules:
    target = standing_rule_candidate(tool_name, arguments, metadata, self.risk_overrides)
    if target and target in self.task_rules[tool_name]:
        rule = f"{tool_name} → {target}"
        return Decision(True, f"allowed by standing rule: {rule}", rule=rule)
```

逻辑：exec/local write 不能通过 standing rule；external effect 要由 host registry 声明 target 参数，并 exact match。测试还确认 rule 只由 automation owner 持有、可以撤销，auto-allowed event 必须在 audit 中引用规则。边界是字符串 target 仍需 canonicalization/versioning；例如大小写、alias、重命名和跨 workspace 同名 channel 可能产生 identity drift。

**代码块 4：shell allowlist 不接受链式副作用**  
来源：[`coworker/permissions.py#L216-L238`](https://github.com/andrewyng/openworker/blob/f96ad4c8e6865f0aec519681a3717b6bcdd81546/coworker/permissions.py#L216-L238)

```python
def _command_allowed(self, command: str) -> bool:
    if _has_shell_operators(command):
        return False
    try:
        argv = shlex.split(command)
    except ValueError:
        return False
    if not argv:
        return False
    for allowed in self.allowed_commands:
        try:
            prefix = shlex.split(allowed)
        except ValueError:
            continue
        if prefix and argv[: len(prefix)] == prefix:
            return True
    return False
```

逻辑：先拒绝 `; & | > < backtick $(` 等 operator，再按 argv token prefix 匹配，避免 `git status && rm...` 与 `statusfoo`。边界是 `shlex` 不是所有平台 shell 的完整 parser，命令自身也可能有危险 flags/config/plugin hooks；这只能是 approval reducer，不能替代 OS sandbox。

#### 依赖分析与供应链风险

`pyproject.toml` 核心依赖包括 OpenAI/Anthropic/Google SDK、FastAPI/Uvicorn、Textual、Pydantic、MCP `>=1.1,<2`、HTTPX/WebSockets、DDGS、croniter、pypdf/pypdfium2；browser/messaging/Bedrock 是 extras。关键风险：

- 根 Python 依赖大多只有 lower bound，**没有根 lockfile**；今日 `uv` 实际解析到的是查询时最新集合，不等同于发布构建的可复现环境。
- `aisuite` 是固定 commit 的 git dependency，identity 较明确，但构建依赖 GitHub 可用性，且应继续审计该 commit 的 transitive graph。
- GUI 有 `package-lock.json`，Tauri/STT 有 `Cargo.lock`，但这是多个独立供应链，不应把“一个 lock 存在”外推为整仓可复现。
- CI 使用 `actions/checkout@v4`、`setup-python@v5` 等 major tags，而非 immutable SHA；应把 action supply-chain 也纳入 release provenance。
- README 称 Windows build 尚未 code-signed；自动更新、local secret store、OAuth broker 与 MCP/connector 都是高价值攻击面。
- issue #302 说明应用清单/OS capability 可让工具“无提示失败”；permission engine 通过不等于 OS effect 真正发生，completed 必须再检查 effect receipt。

#### 真实测试结果

在仓库 runtime 浅克隆中执行：

```text
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -e '.[dev]'
.venv/bin/pytest -q tests/test_tools_permissions.py \
  tests/test_standing_approvals.py tests/test_unattended.py tests/test_config.py \
  -k 'permission or shell or standing or unattended or workspace_trust or trusted'

34 passed, 5 deselected in 17.10s
```

这验证当前 Linux/Python 3.11 环境下的定向纯 fixture；不验证 GUI/Tauri、macOS EventKit、Windows signing、真实 MCP/provider/connector、网络发送或完整 270-open-items 范围。安装过程从公网下载依赖，但未使用任何用户 secret，未启动服务，也未发送外部消息。

#### 可复用经验

- 当 scheduled/unattended Agent 无法即时找到用户时，应优先**挂起需要审批的 effect 并把请求路由到 Inbox**，而不是把“没人回答”解释成批准；边界是 cron 还必须有 timeout/cancel/blocked 终态，不能无限悬挂。
- 当持续授权指向外部副作用时，应优先绑定 `(owner task, tool, immutable target, effect)` 并在每次执行点重验，因为仅按工具名会把一次授权扩大到所有接收者；边界是 target alias/rename 要 canonicalize 并保留 revision。
- 当 repository 可声明 command allowance 时，应优先把声明视为申请，由 user-owned trust store 对 canonical root 授权；边界是“长期信任路径”会接受未来配置变化，高风险环境还应绑定 config hash 或每次 diff。
- 当工具 metadata 不完整或来源不可信时，应优先归为 unknown/blocked，而不是默认 read，因为错误的 `READ` 分类会绕开 consequential gate；边界是 built-in vetted registry 可使用显式只读 allowlist。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/scoped-consequence-gate/` 建纯离线 fixture（**建议，今日未创建**）：定义 12 个调用，覆盖 exact-target hit/miss、target alias、missing target、write path escape、unknown tool、shell chain、unattended approval、revoked grant、mode downgrade、OS receipt missing。接口返回 `allowed/blocked/needs_user/failed` 与 `rule_id/scope/effect/reason`。不连接 provider/MCP，不执行 shell，不修改配置或 cron。

#### 风险边界

- **License**：first-party GitHub API 为 MIT；依赖、Tauri/Rust、PDFium、provider SDK 各自另算。不整仓复制到 shared skill。
- **维护活跃度**：commit 距查询约 4 小时、release 6 天内，活跃；但仓库仅创建 9 天、API open items 高，仍处 beta，稳定性不可外推。
- **安全风险**：terminal/files/connectors/MCP/secret/OAuth/update 全是高权面；unknown metadata 默认 read 偏乐观；AUTO 允许 exec；workspace trust 绑定 path 而非 config snapshot。
- **局限/不适用**：其 desktop product、aisuite provider layer 不适合直接接入 Hermes；只迁移窄权限契约。真实外部连接与 GUI 未测试。
- **已知故障**：issue #302 表明 OS manifest capability 缺失会静默失败；任何发送/日历类 completed 都应要求 effect receipt，而非只看工具函数返回。
- **不可自动执行**：不启用 OpenWorker、不迁移 provider/secret/connectors、不发送消息、不改 Hermes/OpenClaw 配置、auth、env、cron。

#### Skill 升格判断

**需二次验证。** 候选不是 `openworker` skill，而是对已有 `effect-scope-contract` / verification-first 候选的更新：补入 `unattended ≠ autonomy`、exact-target standing grant、unknown-effect blocked、effect receipt。与近一周 scoped authority 研究高度重叠，不新建重复 shared skill；先完成 adversarial fixture 和治理去重，再决定更新现有 shared skill。今天不直接写 active fact 或 manifest。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/scoped-consequence-gate/{README.md,schema.json,fixtures.json,test_gate.py}`。
2. **Hermes 审计候选接口**：`authorize(actor, run_id, tool_id, target_id, effect, path_scope, mode, grant_revision) -> Decision`；unknown effect、missing scope 或 authority store unavailable 返回 `blocked`。
3. **cron/status 对照**：无人值守遇到 `needs_user` 时，status 应是 `blocked` 并生成待审批 artifact；不能改为 completed，也不能自动修改 cron。
4. **shared hub 分层**：fixture/log 只在 `runtime/hermes/`；raw 结论在本 inbox；通过评分、证据、去重、脱敏与审查后，才更新现有 `curated/memory/facts/` 或 verification/effect shared skill。
5. **未来 OpenClaw/future-agent 复用**：只复用 schema/fixtures，不调用或修改其运行时；各宿主在自己的最终执行 chokepoint 实现 enforcement。

---

### 2. vercel-labs/scriptc

**基本信息（GitHub Repository API）**

- URL：https://github.com/vercel-labs/scriptc
- Stars：**2,108**；Forks：**40**；Language：TypeScript；License：**Apache-2.0**。
- 创建：2026-07-22T23:04:54Z；updated：2026-07-28T23:27:19Z；pushed：2026-07-28T23:27:40Z；API `open_issues_count=26`（包含 PR）。
- 固定 commit：[20c3a6c27da4](https://github.com/vercel-labs/scriptc/commit/20c3a6c27da4807f607ebe496663842b67e87f0e)，commit 时间 2026-07-27T03:27:03Z。
- 最新 release：[v0.0.17](https://github.com/vercel-labs/scriptc/releases/tag/v0.0.17)，published 2026-07-27T02:22:50Z；release 内容是 Windows CLI/path 修复。
- 活跃 issues：[#35](https://github.com/vercel-labs/scriptc/issues/35) 报告 dynamic island 的 `Buffer.from(<island call>)` 触发 SC9001 internal compiler error；[#40](https://github.com/vercel-labs/scriptc/issues/40) 报告每个 async function 分配 256 KiB fiber stack 导致内存快速耗尽。两项截至查询时均 open。

#### 一句话判断

值得学的不是把 Hermes TypeScript 编译成 native，而是其**显式 acceptance envelope**：静态支持就编译；需要动态能力必须显式 opt-in 并在边界验证；其余用稳定诊断拒绝；所有“等价”主张由 reference-vs-candidate differential fixture 证明，而不是依靠 README 或类型检查。

#### 解决的问题：替代了什么旧做法

传统 transpiler/compat layer 常见两个失败：不支持的构造在后端才崩溃，或者静默走 fallback 导致 artifact 体积、依赖和语义改变。scriptc 将流程拆成 preflight → lower → typed IR validation → backend → clang，并用三层策略替代：

1. 默认 static，只有显式 `--dynamic` 才嵌 QuickJS-ng；binary 不会无提示长出 JS engine。
2. unsupported construct 用 `SC` code、code frame 和 rewrite hint 拒绝；LLVM 显式 pin 时不 fallback，默认模式才披露后转 C。
3. corpus 同时跑 Node 和 native binary，比较 stdout/stderr/exit；ASan + refcount audit 单列为 memory-safety lane；已知不可相同处编号记录。

这不是“永不失败”：issue #35 证明 panic fence 仍有漏网路径，issue #40 证明语义相同不等于资源预算可接受。正确迁移的是**验证结构和诚实拒绝**，不是其完整编译器。

#### 架构 / 实现与数据流

```text
TypeScript / JavaScript
        │ real TypeScript parse + typecheck
        ▼
preflight diagnostics ─── failure ──► SC code + frame + hint
        │ clean
        ▼
lowering ──► typed IR ──► validateModule
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          LLVM emitter          C reference emitter
              │ refusal             │
              └── default fallback ─┘  (explicit --backend llvm fails)
                         │
                         ▼
                       clang
                         │
                         ▼
native artifact + optional IR / provenance / sidecar

Acceptance oracle: Node result ⇄ native result
                  stdout + stderr + exit + sanitizer audit
```

核心机制：

- Frontend 完成后立即 dispose，backend 只消费 validated IR。
- LLVM/C 共用同一个 in-memory module；fallback 不重跑 frontend。
- runtime feature link 由 IR predicate 决定，regex/net/TLS/dynamic 等按需拉入。
- `analyze()` 将 blocker 当数据并计算 coverage；`compile()` 对 preflight/lowering/validation fail closed。
- differential oracle cache 只缓存纯输入决定的结果；realtime/volatile-host case 强制 live run；cache identity 另有三遍验收脚本。

#### Repo tree 摘要

```text
scriptc/
├── README.md / CHANGELOG.md / LICENSE    # 声明、版本差异、Apache-2.0
├── package.json / pnpm-lock.yaml         # Node >=24；workspace dependency lock
├── packages/
│   ├── compiler/
│   │   ├── src/frontend/                 # tsc/tsgo program、provenance、lowering
│   │   ├── src/ir/                       # typed nodes、serialize、validator
│   │   ├── src/backend/                  # C/LLVM emit、clang driver、feature links
│   │   └── surface-manifest.json         # 版本化 capability surface
│   ├── runtime/
│   │   ├── src/                          # C runtime、event loop、net/TLS/dynamic island
│   │   └── vendor/                       # ryu、quickjs-ng、zlib、curl headers、mbedTLS
│   └── cli/                              # build/run/coverage 命令
├── tests/
│   ├── corpus/                           # Node-vs-native program corpus
│   ├── diagnostics/                      # 拒绝/提示 snapshots
│   ├── harness/                          # differential、cache、shard、server drivers
│   └── library-mode/                     # ABI/profile/sidecar fixtures
├── docs/                                 # how-it-works、limitations、dependencies、FFI
└── .github/workflows/ci.yml              # plain/san 分片 + Linux clang + Windows smoke
```

固定 commit 的 tracked paths 为 **2,843**；大量路径来自 tests 与 vendored C source，不能以 GitHub 主 license 自动概括全部 provenance。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/compiler/src/index.ts` | pipeline composition | analyze/compile/library；preflight、lower、validate、fallback、feature link |
| `packages/compiler/src/ir/validate.ts` | IR gate | 模块/函数结构不变量，validation error 转 internal diagnostic |
| `packages/compiler/src/frontend/lowering/*` | source → typed IR | 每个 construct 的 lowering 或 `SC` fence |
| `packages/compiler/src/backend/cc.ts` | native toolchain | clang/cmake/vendor archive/cache/target handling |
| `tests/harness/differential.test.ts` | semantic oracle | Node/native byte compare、exit、dynamic directives、volatile cache exclusion |
| `tests/harness/cache-identity.mjs` | cache acceptance | uncached/populate/cached 三遍测试，逐 test identity diff |
| `docs/src/app/limitations/page.mdx` | capability boundary | unsupported surface、编号 divergence、dynamic limits、tooling gaps |
| `packages/runtime/vendor/README.md` | supply-chain provenance | upstream version/commit/license/修改与 lazy build 说明 |

#### 源码精读（固定 commit）

**代码块 1：`analyze` 把不支持项当数据，但不把不可信 program 算成 coverage**  
来源：[`packages/compiler/src/index.ts#L541-L624`](https://github.com/vercel-labs/scriptc/blob/20c3a6c27da4807f607ebe496663842b67e87f0e/packages/compiler/src/index.ts#L541-L624)

```ts
export function analyze(entryPath: string, opts: AnalyzeOptions = {}): AnalyzeResult {
  const fe = runFrontend(entryPath, opts.npmStatic);
  try {
    const preflight = fe.preflight;
    const IMPORT_FENCES = new Set(["SC1010", "SC1012", "SC1013", "SC1014", "SC1015"]);
    if (preflight.some((d) => !IMPORT_FENCES.has(d.code))) {
      return { coverage: { /* zero stats */, diagnostics: preflight,
                           preflightFailed: true },
               sourceTexts: fe.sourceTexts() };
    }
    const lowered = fe.lower({ dynamic: opts.dynamic ?? false,
                               coverage: true,
                               targetPlatform: buildTargetPlatform() });
    return { coverage: { stats: lowered.stats,
                         diagnostics: [...preflight, ...lowered.diagnostics],
                         preflightFailed: false },
             sourceTexts: fe.sourceTexts() };
  } finally {
    fe.dispose();
  }
}
```

逻辑：import-form fence 仍可进入 blocker 报告，但类型错误、配置冲突、cycle 等让 program 不可信时直接标 `preflightFailed`，不伪造静态覆盖率。这适合 Hermes 审计：checker 未运行或输入无效应是 blocked，而不是空 findings/100%。

**代码块 2：`compile` 在 emit 前执行 preflight、panic fence 和 IR validation**  
来源：[`packages/compiler/src/index.ts#L627-L677`](https://github.com/vercel-labs/scriptc/blob/20c3a6c27da4807f607ebe496663842b67e87f0e/packages/compiler/src/index.ts#L627-L677)

```ts
export async function compile(entryPath: string, opts: CompileOptions): Promise<CompileResult> {
  const fe = runFrontend(entryPath, opts.npmStatic);
  try {
    const fail = (diagnostics: ScrDiagnostic[]): CompileResult => ({
      ok: false, diagnostics, sourceTexts: fe.sourceTexts(),
    });
    if (fe.preflight.length > 0) return fail(fe.preflight);
    try {
      lowered = fe.lower({ dynamic: opts.dynamic ?? false,
                           targetPlatform: buildTargetPlatform() });
    } catch (e) {
      if (!isCheckerPanic(e)) throw e;
      return fail([checkerPanicDiag(/* anchored at entry */)]);
    }
    if (lowered.module === null) return fail(lowered.diagnostics);
    const validation = validateModule(lowered.module);
    if (validation.length > 0)
      return fail(validation.map((v) => iceDiag(v.message, v.loc)));
  } finally {
    fe.dispose();
  }
  // emit and clang follow
}
```

逻辑：只有 validated IR 能进入 emitter；checker panic 被转换为 clean failed compile。边界是 #35 显示仍有内部错误可从其他路径暴露，panic containment 必须靠 fault corpus 持续补齐，不能靠一个 catch 宣称完备。

**代码块 3：backend fallback 有“自动”和“显式 pin”两种不同语义**  
来源：[`packages/compiler/src/index.ts#L681-L712`](https://github.com/vercel-labs/scriptc/blob/20c3a6c27da4807f607ebe496663842b67e87f0e/packages/compiler/src/index.ts#L681-L712)

```ts
let backend: "c" | "llvm" = "c";
if (opts.backend !== "c") {
  try {
    const ll = emitLlvmModule(lowered.module!);
    cPath = join(opts.outDir, `${stem}.ll`);
    await writeFile(cPath, ll);
    backend = "llvm";
  } catch (err) {
    if (!(err instanceof LlvmUnsupportedError)) throw err;
    if (opts.backend === "llvm") {
      return { ok: false,
               diagnostics: [llvmRefusalDiag(err, entryPath)], sourceTexts };
    }
    llvmRefusal = err.kind;
  }
}
if (backend === "c") await writeFile(cPath, emitModule(lowered.module!, entryText));
```

逻辑：默认可透明回到 reference C backend，并在结果携带 `llvmRefusal`；用户显式 pin LLVM 则 fail loudly。迁移到 Agent 的原则是：只有策略预先声明“可语义保持 fallback”时才降级；显式 provider/tool/backend 要求不应被静默替换。

**代码块 4：differential gate 比较 bytes 与 exit，不把 golden prose 当 oracle**  
来源：[`tests/harness/differential.test.ts#L365-L397`](https://github.com/vercel-labs/scriptc/blob/20c3a6c27da4807f607ebe496663842b67e87f0e/tests/harness/differential.test.ts#L365-L397)

```ts
test.for(files.map((f) => [f.slice(corpusDir.length + 1), f] as const))(
  "%s", { retry: 1 }, async ([, file]) => {
    const [nodeRes, nativeRes] = await Promise.all([runNode(file), compileAndRun(file)]);
    if (!nodeRes.stdout.equals(nativeRes.stdout)) {
      expect(nativeRes.stdout.toString("utf8")).toBe(nodeRes.stdout.toString("utf8"));
    }
    const expectedExit = expectedExitCode(file);
    if (expectedExit === 0) {
      const nativeErr = comparableStderr(nativeRes.stderr);
      if (!nodeRes.stderr.equals(nativeErr)) {
        expect(nativeErr.toString("utf8")).toBe(nodeRes.stderr.toString("utf8"));
      }
    }
    expect(nodeRes.exitCode).toBe(expectedExit);
    expect(nativeRes.exitCode).toBe(expectedExit);
  },
);
```

逻辑：reference 和 candidate 并行运行，stdout 按 bytes 比较，成功路径连 stderr 一起比较，双方 exit 都要符合声明。只有已编号 divergence 才窄化比较。边界是 Node oracle 也可能 nondeterministic，因此源码对 real-time/host-volatile cases 禁用 cache，并给 oracle-side hang 一次 retry；retry 不能掩盖确定性 mismatch。

#### 依赖分析与供应链风险

- 根 `package.json` 要求 **Node >=24**；dev 依赖 TypeScript 5.9.3、Vitest 3.2、tsx、ESLint，`pnpm-lock.yaml` 提供 integrity。compiler 同时依赖 TypeScript **7.0.2** 与别名 `typescript5@5.9.3`，双 compiler world 增加兼容与审计复杂度。
- first-party package 标 Apache-2.0；runtime vendored：Ryū（BSL-1.0 选择）、QuickJS-ng MIT、zlib license、curl headers/curl license、mbedTLS Apache-2.0。每个都在 `vendor/README.md` 记录版本/commit/修改，仍需 SBOM 和 CVE 更新流程。
- dynamic、TLS、cross compile 首次使用会 lazy-build vendored archive；构建过程执行 compiler/CMake/C source，不能把“pnpm install”视为纯数据读取。
- CI actions 大多 major-tag pin；`vercel-labs/setup-zig@v1` 也非 immutable SHA。release provenance/SLSA 签名本次未核验。
- cache key、oracle cache、generated native binary 都是执行面；源码已有 atomic publish 和 identity test，但 cache root 权限、poisoning 与跨用户 scope 仍需单独审计。
- issue #40 的 per-async 256 KiB stack 是可用性/DoS 风险；issue #35 是编译器 crash/诊断一致性风险。

#### 真实构建与测试结果

1. `npx --yes pnpm@11.0.0 install --frozen-lockfile`：成功安装 157 packages。
2. `npx --yes pnpm@11.0.0 build`：runtime/compiler/cli workspace build 均成功。
3. 环境偏差：本机 Node **v22.14.0**，仓库要求 >=24；输出明确 unsupported-engine warning。因此只能证明 TypeScript workspace 在 Node 22 上编译，不证明受支持运行矩阵。
4. 定向 Vitest：
   - `packages/compiler/test/ir.test.ts`：**5 passed**。
   - `tests/harness/diagnostics.test.ts`：**100 passed**。
   - `packages/compiler/test/emit-c.test.ts`：**4 failed**，统一原因为 `spawn clang ENOENT`。
5. 完整 `tests/harness/differential.test.ts`：枚举 **1,028 tests，1,028 failed**；static 路径被缺失 `clang` 阻塞，dynamic 路径还缺 `cmake`。这是本机 prerequisite blocker，不据此判断项目语义错误，也绝不改写成“测试通过”。

本次未安装系统 clang/cmake，未运行生成的 native binary，故 README 的 startup、size、RSS、byte-identical 与 800+（当前真实 corpus 已枚举 1,028）主张均未独立复现。上游 CI 文件显示 macOS plain/san 3 分片、Ubuntu host clang 与 Windows CLI lanes，但本次未查询每个 workflow run 的结论，状态**待核验**。

#### 可复用经验

- 当兼容层只支持输入语言/协议的子集时，应优先发布版本化 capability manifest，并让 unsupported surface 以稳定 code + location + remediation 拒绝，因为“能解析”不等于“能保持语义”；边界是 manifest 必须由同一实现/测试生成，不能手写漂移。
- 当新实现声称兼容参考实现时，应优先对同一 fixture 比较结构化结果、stdout/stderr、exit 和 artifact hash，并对 divergence 编号，因为普通单元测试容易把错误预期固化成 golden；边界是时间、网络、随机和 host state 必须隔离或显式标 volatile。
- 当 fallback 会改变 backend/provider/tool 或依赖体积时，应优先区分“策略允许的语义保持 fallback”和“用户显式 pin”，后者失败应 loud；边界是即便输出相同，成本、权限、隐私和 license 改变也可能禁止 fallback。
- 当 checker/build prerequisite 缺失时，应优先返回 `blocked` 并保留真实工具错误，而不是把 0 findings、未生成 artifact 或 README CI 宣称当作成功；边界是环境探测本身也要记录版本与 scope。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/differential-contract-gate/` 建纯 Python fixture（**建议，今日未创建**）：对 current/reference 两个 mock runner 输入 20 个 status/effect cases，比较 canonical JSON、stderr class、exit、artifact hash；允许的差异必须在 `divergences.yaml` 有 id、reason、expiry、owner。额外加入 checker-missing、timeout、volatile timestamp、fallback backend、schema version mismatch。只运行 fixture，不触碰生产脚本/config/cron。

#### 风险边界

- **License**：GitHub API 与 package 为 Apache-2.0，但 vendored 组件多 license；只抽象验证模式，不复制 compiler/runtime 源码到 shared。
- **维护活跃度**：commit/release/issue 均在两天内，活跃；但项目仅创建 6 天、版本 0.0.17、开放 compiler crash 与 fiber memory 问题，API/语义仍高速变化。
- **安全风险**：编译不可信 TS、C emitter、clang、CMake、FFI、dynamic engine、vendored TLS 都扩大执行面；构建生成物不能自动在宿主执行。
- **局限/不适用**：它不是 Agent runtime，也不能直接改善 Hermes；Node 语义、static subset、macOS primary 与 system toolchain 限制很强。
- **资源边界**：issue #40 暗示 async-heavy 服务可能因 fixed stack OOM；正确性 gate 不能替代 memory/CPU/binary-size budget。
- **本机待核验**：缺 clang/cmake、Node 版本低于要求，native、ASan、dynamic、Linux/Windows differential 均未通过本地验证。
- **不可自动执行**：不安装系统 toolchain、不运行不可信 native binary、不把 scriptc 接入 Hermes tools，不改 provider/model/config/cron。

#### Skill 升格判断

**需二次验证。** 可迁移的是 `differential acceptance gate` 与 `capability-envelope`，不是 scriptc 工具本身。它应先合并到既有 verification-first / toolchain migration candidate：加入 reference-vs-candidate、编号 divergence、prerequisite blocked、显式 fallback policy。因本机 native lane未完成且与现有事实高度重叠，今天不直接创建 shared skill；通过 Hermes 自有 fixture 与治理去重后再更新已有 skill/reference。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/differential-contract-gate/{README.md,cases.json,divergences.yaml,runner.py,test_gate.py}`。
2. **首个适配对象**：以 shared root resolver 或 cron manager 的纯 fixture 作为 reference/candidate，不触碰真实 config；比较 status、canonical path、stderr class、exit 与 artifact schema。
3. **能力清单候选**：为自动化 job 声明 `required_tools/required_versions/effects/output_schema/fallback_policy`；prerequisite 缺失写 `blocked`，不生成 clean/completed。
4. **审计接入候选**：completed 同时要求 runner terminal、artifact exists、schema valid、audit threshold；允许 divergence 必须有 id、证据与到期日。
5. **shared 治理**：raw stdout 与大型 fixture 留 runtime；稳定契约通过评审后更新现有 verification-first/shared governance 文档，不把一次性 test result 写进 class-level skill。

## 横向对照：授权包络与能力包络

| 维度 | OpenWorker | scriptc | 对 Hermes/shared hub 的启示 |
|---|---|---|---|
| 不确定输入 | LLM 提议 tool call | TS/JS program surface | 输入可开放，执行前必须进入 deterministic gate |
| 包络身份 | task + tool + exact target + path | source graph + compiler version + backend | scope/config/version 必须进入 evidence key |
| 允许 | mode/root/rule 命中 | static lowering + validated IR | declaration 只申请，host gate 决定实际能力 |
| 询问/降级 | inline/Inbox；不提升 autonomy | explicit dynamic；default backend fallback | 交互路由、权限和 fallback policy 必须分开 |
| 拒绝 | deny / needs_user | SC code + frame + hint | blocked/failed 是正常终态，不是“待包装成功” |
| 完成证据 | audit cites standing rule；仍需 effect receipt | output bytes/exit 与 oracle 相同 | completed 需要 artifact + actual path/effect receipt |
| 已知边界 | OS capability、metadata、shell parser | numbered divergence、toolchain、resource | 能力/差异清单要版本化并持续测试 |

## 经验沉淀

1. 当无人值守任务遇到需要人工授权的副作用时，应优先返回 `blocked/needs_user` 并将请求送入可恢复 Inbox，因为 unattended 只改变交互位置、不改变自治上限；边界是必须有 timeout/cancel 与后续 resume identity。
2. 当持续授权覆盖外部工具时，应优先绑定 owner、run/task、tool、immutable target、effect 与 grant revision，因为仅按工具名或 display name 会放大权限；边界是 alias/rename/canonicalization 和 authority-store failure 要 fail closed。
3. 当系统只支持输入空间的一部分时，应优先发布版本化 capability envelope，并对 unsupported case 给稳定 code、source location 和 remediation，因为“解析成功/发现工具”不是执行能力；边界是 envelope 必须由实现与 fixture 共同验证。
4. 当替换 parser、runner、provider、backend 或兼容入口时，应优先运行 reference-vs-candidate differential fixtures，比较 canonical output、stderr class、exit、artifact hash 与 effect receipt；边界是已知差异必须编号、解释、设 owner/expiry，不能用宽泛 normalization 隐藏回归。
5. 当 fallback 可能改变成本、隐私、license、权限或依赖体积时，应优先要求策略显式允许，并让用户 pin 的路径 fail loudly，因为“结果看似一样”不代表副作用等价；边界是 fallback receipt 必须披露实际 backend/provider/tool。
6. 当 prerequisite、checker 或 native toolchain 未运行时，应优先标 `blocked` 并保存真实错误，因为空 findings、README 的 CI 声明和源码里存在 tests 都不能证明当前 commit 在当前环境通过；边界是环境版本也要进入证据。
7. 当能力 gate 自身依赖 metadata 或 repo-provided config 时，应优先把 declaration 当申请，并由 user/host-owned registry 在最终 chokepoint 重验；边界是 unknown metadata 默认 read 过于乐观，高权系统应 unknown-deny。

## 风险边界（全局）

- 本次由 Hermes 直接执行；未调用 OpenClaw，未使用消息发送工具，未更改 Hermes/OpenClaw 的配置、model、provider、tools、auth、env 或 cron。
- 公开仓库的 stars/license/更新时间来自 GitHub API 查询时点；license 字段不覆盖依赖、vendored source、模型、数据、商标和 release artifact。
- 为真实测试在 runtime 浅克隆内下载了 Python/Node dependencies；没有把 secret 写入 shared，也没有启动服务、provider、MCP、connector 或外部 effect。
- OpenWorker 只完成定向纯 fixture；GUI、EventKit、Windows、真实连接和完整测试待核验。
- scriptc workspace build 与 pure diagnostics/IR tests有真实结果；native/dynamic/differential 因 clang/cmake 缺失被阻塞，不能宣称兼容性或 benchmark 通过。
- 不直接写 `curated/memory` active fact，不升格 shared skill；候选必须走评分、证据、去重、脱敏与人工/总控审查。

## Skill 升格总判断

- **OpenWorker 模式：需二次验证。** 更新现有 effect-scope/scoped-authority 候选，不新建产品型 skill。
- **scriptc 模式：需二次验证。** 更新 verification-first/toolchain migration 候选，先用 Hermes 自有 fixture 证明 differential gate。
- **今日动作：暂不升格。** 两者都能反哺 class-level 契约，但与已有候选重叠；且 effect receipt、unknown-default、native lane、resource budget 仍有关键缺口。

## 明日继续

1. 最小动作：建立 `scoped-consequence-gate` 离线 fixture，重点验证 unknown effect、missing target/path、revoked rule、unattended blocked、OS receipt missing。
2. 建立 `differential-contract-gate` 的 20-case mock corpus，并确认宽 normalization 不会吞掉 status/effect/schema 回归。
3. 跟进 OpenWorker issue #302：核验修复 commit 是否同时加入 plist capability、真实 macOS fixture 与 effect receipt；未修复前保持待核验。
4. 跟进 scriptc issues #35/#40：分别观察 clean diagnostic regression test 与 fiber stack/resource budget；不为了测试自动安装系统 toolchain。
5. 将两项 POC 与已有 verification-first、subagent 四状态、effect-scope、scoped-authority 候选做去重矩阵，再决定是更新 reference 还是建立窄 shared contract。

## 候选反哺

### Candidate Facts

- [ ] topic: unattended-does-not-raise-autonomy | evidence: OpenWorker `unattended.py` module contract、Inbox fixture、34 个定向 tests 通过 | 建议: update（并入既有 scoped-authority/subagent 状态事实） | 安全级别: low
- [ ] topic: standing-external-grant-needs-owner-tool-exact-target-effect | evidence: `permissions.py` + `test_standing_approvals.py` 固定 commit | 建议: update（补 grant revision/canonical target/unknown deny） | 安全级别: medium
- [ ] topic: explicit-capability-envelope-and-numbered-divergence | evidence: scriptc analyze/compile/differential/limitations 固定 commit；本机 diagnostics 100 passed | 建议: update verification-first，native equivalence pending | 安全级别: medium
- [ ] topic: semantic-correctness-does-not-cover-resource-budget | evidence: scriptc issue #40；上游尚未修复，本机未复现 | 建议: pending/dispute，不进入 active fact | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: scoped-consequence-gate-fixtures | 可复用场景: cron、tool call、connector、future-agent effect authorization | 是否建议 shared: yes（验证并去重后） | 原因: 跨 agent 通用，但应合并现有 effect-scope/scoped-authority skill 候选
- [ ] 名称: differential-contract-gate | 可复用场景: runner/provider/backend/路径迁移与兼容入口替换 | 是否建议 shared: yes（验证后） | 原因: verification-first 的可执行补充，不应包含 scriptc 源码或今日 stdout
- [ ] 名称: openworker-integration | 可复用场景: 桌面 coworker | 是否建议 shared: no | 原因: 产品/runtime/provider 过重，且不符合当前 Hermes/shared hub 最小集成边界

### Candidate Open Questions

- [ ] 问题: Hermes 的 unknown tool/effect 当前是 blocked、ask 还是 read，最终 enforcement chokepoint 在哪里？ | reason: adaptation | priority: high
- [ ] 问题: exact target 如何跨 alias、rename、workspace 与 connector revision canonicalize，同时保持 revoke 生效？ | reason: gap | priority: high
- [ ] 问题: effect function 返回 success 但 OS capability/manifest 阻止真实副作用时，receipt 如何判 failed？ | reason: adaptation | priority: high
- [ ] 问题: differential gate 应如何隔离 timestamp/network/random，又不使用过宽 normalization 隐藏回归？ | reason: adaptation | priority: high
- [ ] 问题: scriptc #35/#40 的修复是否进入 release、diagnostic corpus 和 memory budget gate？ | reason: stale | priority: medium

### 不应自动落地

- 不启用 OpenWorker、不连接 provider/MCP/connector、不发送消息、不迁移其 secret store、OAuth 或 auto-update。
- 不安装 scriptc 为 Hermes tool，不运行未知 native artifact，不自动安装 clang/cmake，不复制编译器/runtime 源码。
- 不修改 Hermes/OpenClaw 的配置、模型、provider、tools、auth、env、cron；未来 OpenClaw 只作为 schema 消费方候选，本任务未调用其运行时。
- 不把候选直接写入 `curated/memory` active fact 或 shared skill manifest；先完成 runtime POC、治理去重、评分与审查。
