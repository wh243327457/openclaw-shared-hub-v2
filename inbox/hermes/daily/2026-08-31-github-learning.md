# 2026-08-31 GitHub 热门项目学习报告

> 执行者：Hermes（当前 OpenClaw 运行时不存在；本次未调用 OpenClaw）  
> GitHub API / 运行查询窗口：2026-08-31T07:31:41+08:00 至 07:51:33+08:00  
> 发现方法：GitHub Search API 查询 `created:>=2026-08-01 stars:>200`、`created:>=2026-08-20 stars:>50` 及 `pushed:>=2026-08-29 stars:>5000 archived:false`；Stars、Forks、Language、License、更新时间均取 GitHub repository API。  
> 深读固定提交：`Tracer-Cloud/opensre@e40e8d912c8614d308dc3644663570db8988c2a9`；`N4darae/anti-mage@a9bc8e2e7b5adb4f6b7c1a3121546f588eac2f22`。动态热度快照与固定源码 revision 分开记录。

## 今日结论

今天深挖的是两种“证据不能越权”的机制：**OpenSRE 把工具 raw output 通过工具自带 mapper 提升成可引用证据，并用 coverage ratchet 防止新增工具静默漏映射；anti-mage 则只让宿主选择、且经真实观测标为 `Verified` 的参照进入确定性评分。共同原则是：当结论会被 Agent、审计或策略消费时，应优先让证据携带来源、覆盖、验证状态和明确的 unknown/insufficient 终态，而不是把“工具调用过”“输入非空”“0 分”投影成已证明。**

### 今日真实验证摘要

- OpenSRE：固定 HEAD 安装使用锁文件（Python 3.12、`uv sync --frozen`）；`opensre --help` exit 0；evidence mapper coverage、VictoriaLogs mapper、SessionGoal host evaluator 的 4 个定向测试文件 **60 passed / 0 failed**。`pip-audit --path .venv/.../site-packages` 扫描 151 个已安装 distribution，返回 **0 known vulnerabilities**；这不覆盖未知漏洞、未安装 extras、外部 SaaS、release binary 或可达性分析。
- OpenSRE HEAD 的 GitHub CI、Synthetic Deterministic Tests、Interactive Shell Live、benchmark-image build 均为 success；查询时 CodeQL 和 Release 仍 `in_progress`，不得写成全绿。公开 issue #5872 仍指出 `astream_investigation` 对 `BaseException` 和 thread-liveness 的终态缺口。
- anti-mage：宿主无 Go，因此改用固定镜像 `golang:1.25.1@sha256:d7098379...`；`go test -json ./...` 实数为 **416 passed / 0 failed / 0 skipped**（5 个有测试 package 通过，2 个无测试 package）；`go vet ./...`、`gofmt -l` 均通过；`go list -m all` 只有本 module，和 `go.mod` 的零外部 module dependency 一致。
- anti-mage 真实本地 API smoke：`GET /api/bootstrap` 返回 v1、32 字符 nonce、6 个随机 font controls、8 个 offset samples；用该 nonce POST 空 probes 返回 `not-evaluated`、score 0，而不是“coherent”。没有真实受测浏览器 corpus，因此 README 的 800-browser 结果未在本机复现，标记待核验。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 204,669 | 23,692 | TypeScript | MIT | 2026-08-30T13:52:13Z | 超高热度，前两日已深读；今日避免重复 |
| [anywhere-labs/dsh-desktop](https://github.com/anywhere-labs/dsh-desktop) | 22,079 | 1,082 | TypeScript | MIT | 2026-08-30T14:54:54Z | Harness 桌面面候选，authority surface 大 |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | 19,469 | 2,266 | Python | MIT | 2026-08-30T15:13:00Z | 训练数据、误用和图像真实性边界需专项审查 |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 19,402 | 1,154 | Rust | MIT | 2026-08-28T02:13:16Z | 前两日已深读，继续观察 mixed-page coverage |
| [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | 13,709 | 2,369 | Python | CC0-1.0 | 2026-08-30T15:50:30Z | 目录许可不代表每个插件许可/effect 已审 |
| [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre) | 10,970 | 1,599 | Python | Apache-2.0 | 2026-08-30T23:31:36Z | **深读：工具本地 mapper、citeable evidence、coverage ratchet** |
| [pathwaycom/arc-task-gen](https://github.com/pathwaycom/arc-task-gen) | 9,055 | 60 | Python | MIT | 2026-08-11T09:52:10Z | benchmark 生成候选，数据泄漏仍是主风险 |
| [sapientinc/PRAXIST](https://github.com/sapientinc/PRAXIST) | 4,526 | 365 | Python | NOASSERTION | 2026-08-30T08:58:12Z | 许可未断言，只观察不迁移源码 |
| [tobi/walgit](https://github.com/tobi/walgit) | 2,349 | 127 | Rust | MIT | 2026-08-27T01:50:20Z | 新 Rust 数据工具候选，今日不展开 |
| [N4darae/anti-mage](https://github.com/N4darae/anti-mage) | 1,256 | 36 | Go | MIT | 2026-08-30T14:46:13Z | **深读：宿主选 challenge、Verified 参考表、单调评分与 abstention** |

> 注：表内 Stars 是 2026-08-31 07:31–07:33 +08:00 的 API 快照，会继续变化；License 只代表 GitHub 顶层识别，不等价于依赖、数据集、模型或发布物的完整合规审查。

## 深读项目

### 1. Tracer-Cloud/opensre

- **一句话判断**：值得学的不是再引入一个 SRE Agent，而是“工具输出默认只是 raw，只有工具本地 mapper 才能提升为可引用 evidence；registry coverage 测试让未做映射决策的新增工具 fail loudly”。
- **解决的问题**：替代在中央 investigation stage 写不断扩张的 vendor `if/elif`，也替代“工具调用成功就自然出现在报告”的假设。固定提交正是 PR #5634 / issue #5594 的 VictoriaLogs mapper 落地：工具定义携带 mapper，stage 保持 vendor-neutral，coverage baseline 作为迁移 ratchet。
- **URL / GitHub API 快照**：https://github.com/Tracer-Cloud/opensre ；**Stars 10,970 / Forks 1,599 / Language Python / License Apache-2.0**；`updated_at=2026-08-30T23:31:47Z`，`pushed_at=2026-08-30T23:31:36Z`，283 open issues（repository API 字段），default branch `main`。
- **固定提交**：[`e40e8d912c8614d308dc3644663570db8988c2a9`](https://github.com/Tracer-Cloud/opensre/commit/e40e8d912c8614d308dc3644663570db8988c2a9)，commit API 时间 `2026-08-30T23:31:35Z`，变更 4 个路径：VictoriaLogs tool、`_evidence.py`、测试及 baseline。
- **Release**：[`v0.1.2026.8.30`](https://github.com/Tracer-Cloud/opensre/releases/tag/v0.1.2026.8.30)，发布于 `2026-08-30T01:18:01Z`，target commit `10d935c...`；它早于今日固定 HEAD，不能把 HEAD mapper 结论冒充该 release 已含。
- **来源交叉核验**：README、`docs/adding-tools-and-integrations.md`、release、issue [#5594](https://github.com/Tracer-Cloud/opensre/issues/5594)、open bug [#5872](https://github.com/Tracer-Cloud/opensre/issues/5872)、关键源码、tests、`pyproject.toml`/`uv.lock`、GitHub Actions 和本机定向验证。

#### 架构/实现与数据流

1. `integrations/<vendor>/tools/` 拥有 vendor client、tool metadata、raw output normalization 和 `evidence_mapper`，而不是把 vendor 知识塞入 shared stage。
2. 调查执行把 tool name/input/output 交给 `merge_tool_evidence`；函数先保存 raw output 和 redacted `tool_outputs`，仅对 dict output 查 registry mapper。
3. mapper 通过 `record_evidence_entry` 追加最小的 `source/label/summary/url/snippet` 到 `catalog_entries`；report catalog 后续赋予 `E1...` display id。raw payload、模型/报告可见摘要是不同层。
4. `test_no_new_unmapped_tool` 比较 `registered - mapped` 与显式 known-gap baseline；新增 tool 若没有 mapper，也没承认是 gap，就失败。`test_backfilled_tools_leave_the_baseline` 防“已修但 baseline 永久腐烂”。
5. VictoriaLogs mapper 空 rows 不产 evidence，非空只记录行数与 query 的前 200 字符，不把日志全文复制进 context；这是 context budget 和敏感数据最小化的初级边界。
6. 独立的 `SessionGoal` evaluator 把模型的 `session_goal:achieved` 当 claim；普通 handoff goal 还要求成功工具 evidence，长 checklist 不能被单次 claim 全部完成。这展示“citeable data”与“业务完成 proof”应分别有 host gate。

#### repo tree 摘要

```text
opensre/                                      # 固定提交 5,173 tracked files
├── bootstrap/                                # process profiles、adapter registration
├── config/                                   # settings、constants、credential resolution
├── core/                                     # Agent harness、domain types、state、LLM/tool contracts
│   ├── domain/types/evidence.py              # EvidenceMapper 与 catalog entry primitive
│   └── agent_harness/session_goal/           # host-owned completion evaluator/persistence
├── integrations/<vendor>/                    # vendor config/client/verifier/tools/mapper ownership
│   └── victoria_logs/tools/                  # 今日固定提交的 query tool + mapper
├── tools/investigation/                      # pipeline、gather、report catalog/projection
├── surfaces/                                 # CLI/Web/交互入口
├── gateway/                                  # 独立 gateway surface
├── infrastructure/                           # persistence、telemetry、safety、delivery adapters
├── tests/                                    # unit/integration/synthetic/e2e，1,191 test_*.py
├── docs/                                     # tool/integration definition of done、用户文档
└── pyproject.toml / uv.lock                  # Python >=3.12；42 direct deps；214 lock packages
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `core/domain/types/evidence.py` | evidence mapper 公共契约 | vendor-open `EvidenceSource=str`、mapper callable、`record_evidence_entry` 最小 citeable schema |
| `core/tool/contracts.py` | tool registration contract | `BaseTool.evidence_mapper` 和 registered tool metadata 携带 mapper |
| `tools/investigation/stages/gather_evidence/tools.py` | raw→canonical 提升点 | raw output 永久保留；只在 dict + registered mapper 时生成 canonical evidence |
| `integrations/victoria_logs/tools/__init__.py` | VictoriaLogs tool | surfaces、inputs、outputs、run 及 class-level mapper 绑定 |
| `integrations/victoria_logs/tools/_evidence.py` | vendor-local projection | non-empty rows → 一条最小 catalog entry；query 截断 200 字符 |
| `tests/tools/investigation/stages/gather_evidence/test_evidence_mapper_coverage.py` | registry coverage ratchet | 新 unmapped 工具必须加 mapper 或显式进入 gap；回填后必须离开 baseline |
| `core/agent_harness/session_goal/evaluate.py` | 模型 claim 的 host evaluator | tool success、checklist、dispatch、host-owned rule 与 typed status/reason |
| `tools/investigation/capability.py` | sync/async investigation API | background thread → queue → async stream；issue #5872 指出 BaseException/liveness 缺口 |

#### ⭐ 源码精读

**1) `record_evidence_entry(...)`：mapper 只能铸造最小 citeable projection**

```python
def record_evidence_entry(
    evidence: dict[str, Any], *, source: str, label: str,
    summary: str | None = None, url: str | None = None,
    snippet: str | None = None,
) -> None:
    entries = evidence.setdefault(CATALOG_ENTRIES_KEY, [])
    if not isinstance(entries, list):
        return
    entries.append({
        "source": source, "label": label, "summary": summary,
        "url": url, "snippet": snippet,
    })
```

逻辑：core 不枚举 vendor，只定义开放字符串 source 与最小 entry schema；display id 由 catalog 后置分配。优点是每个 integration 可独立演进，且 report 不必内联 raw payload。边界：schema 没有 `input_hash/tool_call_id/timestamp/coverage/output_hash`，也没有 mapper exception containment；它能建立可引用性，尚不能单独证明完整性、真实性或执行授权。

**2) `merge_tool_evidence(...)`：先保留 raw，再按 registry mapper 显式提升**

```python
def merge_tool_evidence(evidence, tool_name, output, tool_input, *, redacted=None):
    evidence[tool_name] = output
    view = redacted if redacted is not None else redact_tool_view(tool_input, output)
    evidence.setdefault("tool_outputs", []).append({
        "tool_name": tool_name,
        "tool_args": view.tool_input,
        "data": view.output,
    })
    if not isinstance(output, dict):
        return
    tool = get_registered_tool(tool_name)
    mapper = tool.evidence_mapper if tool is not None else None
    if mapper is not None:
        mapper(evidence, output, tool_input)
```

逻辑：raw truth 与 report projection 并存；未知/非 dict output 不凭空生成 canonical key。mapper 从真实 registry 解析，stage 无 vendor 分支。边界：raw `evidence[tool_name]` 与 redacted `tool_outputs` 的敏感度不同，后续任何 consumer 必须知道自己读哪一层；mapper 抛异常当前会向上冒泡，需明确是否应 fail investigation、记录 blocked，或 containment。

**3) `map_victoria_logs_query(...)`：空结果不是 evidence，摘要有长度预算**

```python
def map_victoria_logs_query(evidence, output, tool_input) -> None:
    rows = output.get("rows", [])
    if not isinstance(rows, list) or not rows:
        return
    query = output.get("query") or tool_input.get("query")
    query_text = str(query).strip() if query else ""
    row_label = "log entry" if len(rows) == 1 else "log entries"
    record_evidence_entry(
        evidence,
        source="victoria_logs_query",
        label="VictoriaLogs Logs",
        summary=f"{len(rows)} {row_label}",
        snippet=query_text[:200] or None,
    )
```

逻辑：工具的完整 rows 仍在 raw 层；catalog 只获得 cardinality + bounded query。空 rows 不制造“0 logs”噪声。边界：`len(rows)` 可能只是 limit 后数量，不等于查询全集 coverage；entry 没有 `truncated/limit/start/fetch_error`，所以“2 log entries”不能被 Agent 外推为只存在 2 条。

**4) coverage ratchet：只允许已知缺口收缩，不允许无声增长**

```python
def test_no_new_unmapped_tool(self) -> None:
    registered, mapped = _registered_and_mapped()
    unmapped = registered - mapped
    assert unmapped <= _known_gaps(), (
        "New investigation tool(s) with no evidence mapper: "
        f"{sorted(unmapped - _known_gaps())}"
    )

def test_backfilled_tools_leave_the_baseline(self) -> None:
    _registered, mapped = _registered_and_mapped()
    assert not (_known_gaps() & mapped)
```

逻辑：baseline 是技术债预算而不是目标真相。由于 optional dependency 缺失可能让 registry 缩小，使用 subset 而非 equality；但任何新增 unmapped tool 都扩大差集并失败。边界：若模块 import 失败，工具可能根本不在 registered set，subset 测试看不到；需要另有 discovery coverage/blocked diagnostics。

**5) `turn_has_session_goal_evidence(...)`：模型“已完成”不能替代实际成功工具**

```python
def turn_has_session_goal_evidence(result: Any) -> bool:
    if turn_dispatched_investigation(result):
        return False
    action = getattr(result, "action_result", None)
    action_succeeded = 0
    if action is not None:
        try:
            action_succeeded = int(getattr(action, "executed_success_count", 0) or 0)
        except (TypeError, ValueError):
            action_succeeded = 0
    return action_succeeded > 0
```

逻辑：执行失败和仅 dispatch investigation 都不能作为完成证据；evaluator 再结合 checklist 和 host ownership 产出 typed status/reason。边界：`executed_success_count > 0` 仍只证明“某工具成功”，不天然绑定 goal requirement、输入 revision 或 artifact hash；高保证流程还需 requirement→evidence mapping。

#### 依赖分析与供应链风险

- `pyproject.toml` 要求 Python `>=3.12`；42 个直接 dependency，包含 Anthropic/OpenAI/LiteLLM、MCP、Pydantic、Kubernetes、FastAPI/Uvicorn、HTTP clients、crypto、AWS、Slack/Discord、数据库 clients、OpenTelemetry、Sentry 等。锁文件解析出 214 packages，生产安装再加 dev 后本机 `.venv` 为 588 MiB。
- 高权/高面依赖包括 LLM SDK、MCP、Kubernetes、cloud SDK、数据库 drivers、HTTP/network server、telemetry。即使 mapper 模式本身很窄，完整 OpenSRE runtime 的 credential/network/tool surface 很大，不能作为 shared hub 的普通库直接引入。
- `uv sync --frozen` 成功，`opensre --help` exit 0。`pip-audit --path` 对当前已安装 151 个 distribution 为 0 known vulnerabilities；不覆盖 lock 中未安装 platform/extras、PyInstaller release、外部 services、未知漏洞或 exploitability。
- Dependabot alerts API 对当前 token返回 403（未授权），GitHub repository advisories 列表为空不能抵消本机 audit，也不能证明安全。
- README 明示 public alpha、API/integrations 可变化；PostHog/Sentry telemetry 默认 opt-out，而非默认关闭。不能在无人值守 Hermes 任务中直接安装、配置 provider 或接入生产 observability。

#### 真实验证

- `uv sync --frozen`：exit 0；使用锁文件构建 editable `opensre@e40e8d...`。
- `uv run --frozen opensre --help`：exit 0，输出 3,271 bytes。
- 定向命令：VictoriaLogs evidence mapper、mapper coverage、SessionGoal evaluate + predicates 共 4 个 test files；真实结果 **60 passed / 0 failed，3.75s**。
- 目标源码 `compileall`：exit 0。
- HEAD Actions 查询：CI、Synthetic Deterministic、Interactive Shell Live、benchmark image success；CodeQL/Release 查询时仍 in progress。
- 未运行：全仓 1,191 test files、真实 LLM、VictoriaLogs credential/E2E、Kubernetes/cloud/gateway、release binary、telemetry 或生产 incident。issue #5594 要求的真实 credential report grep 今日未执行，端到端 citeability仍待核验。

#### 可复用经验

- 当插件/工具输出需要进入 Agent 报告时，应优先让 mapper 随工具定义同行，并由 shared stage 只执行统一契约，因为 vendor schema 应由 vendor owner 维护；边界是 mapper 仍须 schema、异常与敏感数据测试。
- 当 capability registry 会持续新增时，应优先使用“已知缺口 baseline + 只减不增 ratchet”，因为 review checklist 很容易漏掉新工具的 evidence decision；边界是 import 失败导致的未注册项需另一条 discovery gate。
- 当 raw output 要投影到模型、报告或知识库时，应优先保留 raw/canonical/projection 分层并限制摘要长度，因为可引用不等于应复制全文；边界是 projection 必须携带 coverage、hash 与 source revision 才能高保证重建。
- 当模型声称 goal 完成时，应优先由宿主根据 requirement、tool success、artifact/readback 和 terminal reason 独立判断，因为 tag/prose 是 claim；边界是成功计数仍需绑定具体 requirement。

#### 可尝试实验（30 分钟内）

在 `runtime/hermes/github-learning-poc/evidence-promotion-ratchet-v0/` 建纯 Python synthetic registry：三个 source adapter 分别返回 `complete/partial/blocked`；mapper 生成 `source/input_hash/output_hash/coverage/truncated/summary`；测试新增 unmapped adapter、mapper exception、empty output、oversized summary、optional adapter import blocked、raw 与 redacted projection 分离。只使用 synthetic payload，不连接 provider、observability、MCP、OpenSRE 或任何 secret。

#### 风险边界

- **License**：GitHub API、`LICENSE` 与 `pyproject.toml` 均为 Apache-2.0；依赖、容器、release binary、LLM/provider 和第三方 integrations 仍需独立合规审查。
- **维护活跃度**：固定提交距查询不足 10 分钟；repository API 有 283 open issues，且 daily release 活跃。高活跃与 public alpha 同时意味着改动快、compatibility 风险高。
- **安全风险**：完整项目连接 cloud、Kubernetes、logs、databases、MCP、消息系统和 LLM；README 的 remediation 可选执行意味着 effect/approval/credential 边界必须逐工具核验。Telemetry 默认为 opt-out。
- **已知局限**：open issue #5872 指出 async stream 对 `BaseException` 可能静默结束，且 queue drain 缺 thread-liveness check；源码固定提交仍是 `except Exception` + sentinel + 无 liveness gate，机制与 issue 一致，本机未注入复现，因此标“上游复现/静态核验，待本机复现”。
- **证据局限**：VictoriaLogs entry 未写 coverage/limit/start/output hash；有 citation 不等于查询完整或 root cause 正确。35 个 open evidence-mapper issue 表明迁移仍未完成。
- **测试局限**：60 个定向 tests 和 HEAD CI success 不能外推到全部 5,173 files、所有 integrations、生产 incident 或 release artifact。
- **不适用**：只需要轻量离线审计、禁止外网/telemetry、要求稳定 API、最小依赖闭包或强制 independent security audit 的环境，不适合引入完整 OpenSRE。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `evidence-promotion-ratchet` 契约，不是 OpenSRE runtime、SRE prompt 或 vendor integration 源码。shared hub 已有 GitHub-learning、verification-first、completion/receipt、shared-memory/governance 能力，直接创建大 skill 会重复。先做 synthetic fixture，证明 coverage、redaction、hash、blocked adapter 与 mapper failure semantics，再决定更新既有 research/verification skill。今日不修改 `capabilities/skills/`、manifest 或 curated active fact。

#### Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/evidence-promotion-ratchet-v0/{registry.py,schema.json,baseline.txt,fixtures/,test_registry.py}`。
- Hermes orchestrator 候选：给研究 source 建结构化 registry，每个 adapter 声明 `mapper/version/effect/network/coverage`；报告生成前 gate `registered - mapped - declared_gap == ∅`。
- 报告 receipt：建议在 `runtime/hermes/github-hot-project-learning/status.json` 未来增加 `source_revision/report_hash/evidence_coverage/audit_dimensions/terminal_reason`，不要只靠 Markdown 关键词完成。
- Shared skill 候选：二次验证后优先更新 `capabilities/skills/research/github-hot-project-learning/SKILL.md` 与 verification 类 reference，加入“raw → canonical evidence → bounded projection”和 coverage ratchet；不创建 OpenSRE 专用 skill。
- 分层：raw 报告在 `inbox/hermes/daily/`；clone、venv、audit JSON、fixtures 在 `runtime/hermes/`；治理评分、证据、去重、脱敏和人工审查后才能形成 curated candidate。
- 不安装 OpenSRE 到 Hermes 本体，不执行 setup，不修改 Hermes model/provider/tools/config/cron/secret，不连接生产日志或 observability；本次未调用 OpenClaw。

### 2. N4darae/anti-mage

- **一句话判断**：值得学的是它如何把“被测环境自报的数据”限制为 observation，而把 challenge、clock、reference provenance 和是否可作为证据的 `Verified` 状态留给宿主，再用 `not-evaluated/insufficient` 阻止 0 分冒充可信。
- **解决的问题**：替代只查已知 automation signature、单个 fingerprint 或由客户端自己选择挑战/时间的旧做法；它检查浏览器多个 surface 自洽性，并用 server-issued nonce/随机 controls/offset dates 把 measurement 绑定到一次宿主选择的 scan。
- **URL / GitHub API 快照**：https://github.com/N4darae/anti-mage ；**Stars 1,256 / Forks 36 / Language Go / License MIT**；`updated_at=2026-08-30T22:35:35Z`，`pushed_at=2026-08-30T14:46:13Z`，0 issues，default branch `main`。
- **固定提交**：[`a9bc8e2e7b5adb4f6b7c1a3121546f588eac2f22`](https://github.com/N4darae/anti-mage/commit/a9bc8e2e7b5adb4f6b7c1a3121546f588eac2f22)，commit API 时间 `2026-08-30T14:46:09Z`；该 HEAD 仅修改 README。源码 tree 共 87 tracked files。
- **Release/CI**：GitHub Releases 和 tags 均为空；HEAD status 为 pending/0 contexts，check-runs 为 0，仓库没有 Actions runs。不能称上游 CI 通过。
- **来源交叉核验**：README、closed PR [#1](https://github.com/N4darae/anti-mage/pull/1)/[#2](https://github.com/N4darae/anti-mage/pull/2)、关键源码、reference tables/tests、`go.mod`、本机 Docker 固定 Go 镜像测试和 API smoke。仓库没有 issue，故没有 issue lane 可交叉核验。

#### 架构/实现与数据流

1. `server.issuer.issue` 用 crypto/rand 生成 128-bit hex nonce、6 个虚构 font family control 和 8 个历史 offset instants；保存最多 4,096 个 live challenge，TTL 30 分钟。
2. 浏览器 client 收到 bootstrap 后采集 `probes`；POST 时 `assess.Decode` 只接收 nonce 与 observations/probes，不允许客户端注入 server-owned dates、font controls、clock 或 Findings。
3. server 根据 nonce（或 legacy control match fallback）恢复 issued inputs，计算 server elapsed time，再构造 `assess.Environment` 调用 pure `Evaluate`。
4. `internal/scan` 固定顺序运行 22 个 section，输出 `consistent/contradiction/inconclusive/unverified/instrumented`；未识别 determination 被 normalize 为 inconclusive。
5. reference 表每行带 `Source{Origin,Checked}` 与 `Verified`；engine version、GPU decode、fonts 等路径明确跳过或返回 unverified，而不把“文档里看到过但没真实观察”用于强结论。
6. summary 只让 contradiction/instrumented 增加 bot-likeness，使用独立权重的互补概率组合、10 分量化、90 cap；缺失 feature 不降低 score。无 determined section 返回 `not-evaluated`，覆盖不足返回 `insufficient`。
7. HTTP server 强制 loopback 地址、1 MiB body、30 秒 read/write timeout、no-store/nosniff/referrer headers；但可选 `-dump` 会将原 payload 以 0644 写盘，属于显式隐私风险。

#### repo tree 摘要

```text
anti-mage/                              # 固定提交 87 tracked files；76 *.go
├── main.go                             # embed web、flags、loopback server lifecycle
├── assess/                             # public Environment/Assessment、Decode、Evaluate
├── internal/scan/                      # 22 section evaluators、band/score、payload helpers
├── reference/                          # Source/Checked/Verified tables + table tests
├── osfont/                             # resolved font family floor evaluator
├── server/                             # challenge issuer、HTTP API、limits、optional dump
├── web/                                # bootstrap consumer、browser probes、report UI
├── tools/debugscan/                    # debug/replay helper
├── go.mod                              # Go 1.24；无 require，零外部 module dependency
├── Makefile                            # gofmt + go vet + go test
└── LICENSE / NOTICE / readme.md        # MIT、使用和边界说明
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `server/bootstrap.go` | server-owned challenge | nonce、随机 controls/dates、TTL、容量、elapsed 计算 |
| `server/server.go` | HTTP boundary | loopback、body/time limits、decode、host-owned input overlay、headers、optional dump |
| `assess/decode.go` | trust boundary decoder | 只读取 nonce 与 probes/observations；忽略 client 的 Findings/clock/reference fields |
| `assess/assess.go` | public pure API | Environment → scan request/inputs → typed Assessment；score clamp、sorted supplied IDs |
| `internal/scan/scan.go` | deterministic section runner | 固定 22 section 顺序、normalise、summary |
| `internal/scan/band.go` | evidence aggregation | monotonic weights、10 分量化、not-evaluated/insufficient/coherent/discrepant/instrumented |
| `reference/reference.go` + tables | provenance gate | Origin、Checked、Verified；未验证 reference 不进强 evidence |
| `internal/scan/sec_engineversion.go` | reference consumer | 只遍历 Verified features；later capability 才形成 contradiction |
| `osfont/osfont.go` | coverage/verification-aware floor | 空输入→inconclusive，表未验证→unverified，部分匹配→inconclusive |

#### ⭐ 源码精读

**1) `Decode(b []byte)`：被测 client 只能提交 observations 与 nonce**

```go
func Decode(b []byte) (Environment, error) {
    var top map[string]json.RawMessage
    if err := json.Unmarshal(b, &top); err != nil { /* typed error */ }
    env := Environment{}
    if raw, ok := top["nonce"]; ok {
        var s string
        if json.Unmarshal(raw, &s) == nil { env.Nonce = s }
    }
    obs := map[string]Observation{}
    for _, field := range []string{"probes", "observations"} {
        // invalid entries are skipped; only id/status/value enters env
    }
    env.Observations = obs
    return env, nil
}
```

逻辑：即使 wire JSON 包含 `offsetDates/fontControls/elapsedMs/findings`，此 decoder 也不导入；server 随后用 issuer state overlay。这把不可信 measurement 与 host-owned challenge/policy 分开。边界：invalid observation 被逐项跳过而不是返回 coverage errors，调用方必须依靠 `supplied` 与 determination 判断缺失，不能把 HTTP 200 当完整。

**2) `issuer.issue(now)`：challenge 有 entropy、TTL 与容量上限**

```go
func (i *issuer) issue(now time.Time) (Bootstrap, error) {
    nonce, _ := randomHex(16)
    controls, _ := inventedFamilies(6)
    samples, _ := offsetInstants(now, 8)
    i.mu.Lock()
    for k, v := range i.live {
        if now.After(v.expires) { delete(i.live, k) }
    }
    for len(i.live) >= 4096 { delete(i.live, oldestKey(i.live)) }
    i.live[nonce] = issued{at: now, inputs: scanInputs{
        Nonce: nonce, OffsetDates: dates, FontControls: controls,
    }, expires: now.Add(30 * time.Minute)}
    i.mu.Unlock()
    return bootstrap, nil
}
```

逻辑摘要基于真实源码：challenge 不由被测环境预先选择；live map 有 mutex、TTL 和 max capacity，避免无限增长；elapsed 由 server 的 issued time 计算。边界：`resolve` 不消费 nonce，同一 challenge 在 TTL 内可 replay；fallback `resolveByControls` 允许无 nonce 匹配 controls。它提供 measurement binding，不是认证、防重放或 anti-fraud 完整协议。

**3) `Evaluate(env Environment)`：pure decision core 与 typed abstention**

```go
func Evaluate(env Environment) Assessment {
    req := scan.Request{V: 1, Mode: "public", Nonce: env.Nonce, Probes: probesOf(env)}
    in := scan.Inputs{
        Nonce: env.Nonce, OffsetDates: env.OffsetDates,
        FontControls: env.FontControls, ElapsedMS: elapsedOf(env),
    }
    rep := scan.AnalyzeWith(req, in, suppliedSections(env.Findings))
    a := Assessment{V: 1, Score: clampScore(rep.Summary.BotLikeness), Supplied: suppliedIDs(env.Observations)}
    a.Determination = determinationOf(rep.Summary.Band)
    if a.Determination == NotEvaluated { a.Score = 0 }
    a.Statement = statements[a.Determination]
    return a
}
```

逻辑：核心无 clock/filesystem/network/global mutation；排序 supplied IDs，未知 band 映射为 not-evaluated，并附人类可读 statement。真实空 probes smoke 返回 `not-evaluated/0`。边界：public `Environment.Findings` 允许 in-process trusted caller注入外部 verdict；若 adapter 错把 client data 放入 Findings，仍可污染评分，宿主 adapter 必须保持 trust boundary。

**4) `sectionEngineVersion(...)`：reference 没 Verified 就不能用于 contradiction**

```go
for _, fe := range reference.EngineFeatures {
    if !fe.Verified { continue }
    if fe.ShipsInMajor <= claimed { continue }
    present, known := boolean(features, fe.ID)
    if !known { continue }
    applicable++
    if present { laterPresent = append(laterPresent, rowFor(fe)) }
}
if applicable == 0 { return Unverified }
if len(laterPresent) > 0 { return Contradiction }
return Consistent
```

逻辑：表中 Chrome 150 的两个 feature 虽有 release-note source，但 `Verified:false`，不会形成结论；只有 exact observed 的 151 features可用。未知输入和未观察 reference 保留 unverified。边界：`Verified` 是仓库维护者的布尔声明，不是签名或双人审查；source freshness、browser/platform matrix 和撤销仍需治理。

**5) `combineWeights` / `summarise`：只有 evidence 增加 score，缺失不奖励**

```go
func combineWeights(ws []findingWeight) int {
    unaccounted := 1.0
    for _, w := range ws {
        unaccounted *= 1 - float64(w)/100
    }
    n := round10(int(math.Round(100 * (1 - unaccounted))))
    if n > 90 { return 90 }
    return n
}

switch {
case determined == 0: band = BandNotEvaluated
case deliberate > 0: band = BandInstrumented
case flagged >= 2: band = BandInstrumented
case flagged == 1: band = BandDiscrepant
case determined*2 >= candidates: band = BandCoherent
default: band = BandInsufficient
}
```

逻辑：多个独立 evidence body 以 diminishing-return 组合并量化到 10；缺失/unverified 不降低 bot score，也不制造“安全”。真实 API 空 probes 展示了 not-evaluated，而不是 coherent。边界：section independence 是设计假设；若多个 section 共享同一根因，组合会重复计权，README 的校准结果仍需独立 corpus 复现。

#### 依赖分析与供应链风险

- `go.mod` 只有 module path 和 `go 1.24`，无 `require`；固定 Go 1.25.1 容器内 `go list -m all` 只返回项目 module。零外部 module dependency 显著缩小依赖图，但不等于零供应链：仍有 Go toolchain/container base、浏览器 runtime、embedded JS/CSS/data 和 reference data provenance。
- 测试镜像真实 digest：`golang:1.25.1@sha256:d7098379b7da665ab25b99795465ec320b1ca9d4addb9f77409c4827dc904211`；镜像 digest 固定下载内容，不证明镜像无漏洞或构建可复现。
- repository advisories endpoint 返回空数组；Dependabot alerts 被仓库禁用（403）。由于无第三方 Go module，典型 dependency audit 面很小，但 Go stdlib/toolchain CVE、Docker base 和 web/browser attack surface仍需跟踪。
- `-dump` 可把整个 browser observation payload写成 mode 0644；即使 loopback，也可能包含高熵 fingerprint 和设备信息，默认不应开启，若开启需私有目录、权限、retention 和 consent。

#### 真实验证

- 宿主 `go` 缺失时，`go test ./...` 真实先返回 exit 127；没有用 README/CI 代替。
- 使用固定 Go 1.25.1 container：`go test -json ./...` **416 tests passed / 0 failed / 0 skipped**；5 个有测试 packages pass，root/debugscan 两个 packages 显示 `[no test files]`。
- `go vet ./...` exit 0；`gofmt -l .` 无输出；`go list -m all` 仅本 module。
- API smoke 在同一隔离 container 内 build/run：bootstrap `v=1`、nonce length 32、6 controls、8 offsets；空 probes POST 返回 `not-evaluated`, score 0, supplied `[]`。
- 未运行：真实 Chrome/Firefox/Edge/Brave/anti-detect browser、800 samples、Windows/font/GPU/media capability matrix、对抗绕过、race detector、fuzz、跨平台 build。README benchmark 数字均为上游声明，今日不作为本机复现事实。

#### 可复用经验

- 当输入方可能从测试内容获益时，应优先由宿主随机选择 challenge、保存 issuance state 并在评估前覆盖 client-owned policy fields，因为被测对象不应定义自己的考题和计时；边界是 challenge binding 不是身份认证。
- 当 reference table 驱动自动判断时，应优先把 `origin/checked/observed/verified` 做成可执行 gate，让未核验行返回 unknown 而不是参与评分，因为文档存在不等于真实配置已观察；边界是布尔 Verified 还需 review、freshness 和撤销机制。
- 当 score 为 0 时，应优先同时输出 `not-evaluated/insufficient/coherent` 等 coverage-aware terminal，因为“没有发现矛盾”与“没有测到东西”完全不同；边界是 coherent 也不是未修改证明。
- 当多个 detector 可能相关时，应优先按 evidence body 分组、单调累积并限制 cap，而不是逐 check 简单相加或用缺失项减分，因为同源重复和 unsupported 会扭曲置信；边界是独立性假设必须用真实 corpus 校准。

#### 可尝试实验（30 分钟内）

在 `runtime/hermes/github-learning-poc/verified-reference-gate-v0/` 做纯 Python fixture：host 生成 nonce + random question ids，adapter 只解析 observations；reference row 为 `source/checked/observed/verified/revision`；decision core 输出 `not_evaluated/insufficient/coherent/discrepant` 和 coverage。测试 client 注入 clock/reference、expired/replayed nonce、unverified match、partial observations、同源重复 evidence、zero-score abstention。只用 synthetic data，不采集真实浏览器 fingerprint。

#### 风险边界

- **License**：GitHub API 与 LICENSE 均为 MIT；NOTICE 存在。reference 数据的来源与可再分发边界仍需逐源审查，不能因代码 MIT 就假定数据集完全同许可。
- **维护活跃度**：项目 2026-08-22 创建，固定 HEAD 8 月 30 更新；只有 2 个 closed PR、0 issues、0 releases/tags、无 Actions checks。新且活跃，但 bus factor、长期维护和 release provenance 很弱。
- **隐私/安全**：浏览器 probes 涉及 fonts、GPU、media、canvas、audio、WebRTC 等 fingerprint surface；即使目标是 consistency，也可能形成隐私数据。loopback 降低网络暴露，不消除同机恶意页面、dump 文件或浏览器扩展读取风险。
- **对抗边界**：README 明确技术会被 reverse-engineer；nonce 和随机 controls 增加预适配成本，但未一次性消费、无认证、无远端 attestation。高级伪装可统一篡改多个 surface，consistent 不等于 genuine。
- **误判边界**：privacy/accessibility/content-blocking 也会修改 surface；项目只说 environment appears modified，不应推断“是 bot/恶意用户/某 vendor”。将分数作为封禁唯一依据会产生公平性和合规风险。
- **校准边界**：README 的 stock 0、anti-detect median 60+ 为上游 100 samples/browser 声明；没有公开 raw corpus/runner receipt供今日复验，故 benchmark、false-positive 和泛化结论均待核验。
- **测试边界**：416 unit tests 和空-probes API smoke 没有跑真实 browser collection、Windows reference、GPU 设备或 adversarial evasion；不能外推检测效果。
- **不适用**：身份认证、强 bot attestation、无 fingerprint consent 的终端用户追踪、单分数自动封禁、需要经过独立公平/隐私审计的高风险决策。

#### ⭐ Skill 升格判断

**暂不沉淀（完整浏览器检测能力） / 需二次验证（verified-reference gate 抽象）**。反 bot/browser fingerprint 不是当前 Hermes/shared hub 的核心能力，且有隐私、公平性与对抗风险，不能迁移采集代码或 reference data。可抽象的窄模式是“host-owned challenge + verified reference + abstention”，与 verification-first/source-outcome/effect-scope 既有候选高度重叠；先做 synthetic fixture 和去重，今日不新建 shared skill。

#### Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/verified-reference-gate-v0/{issuer.py,adapter.py,decision.py,references.json,fixtures/,test_contract.py}`，仅 synthetic evidence。
- Hermes research：source adapter 不得从被研究项目 prose 自动提升 `verified=true`；验证状态只能来自真实 tool output、固定 revision、test receipt 和 reviewer/policy。
- GitHub learning 候选：候选事实 schema增加 `source_revision/checked_at/observed_by/verified/coverage`；unverified 结论留 inbox/runtime，不能进入 curated active fact。
- Shared skill：若 fixture证明跨 agent 可复用，优先更新 verification/governance reference；不复制 anti-mage browser probes，不创建“反机器人”skill，不收集用户浏览器 fingerprint。
- 安全边界：不运行真实受测 browser，不把扫描器接入登录/风控，不保存 fingerprint，不自动改 Hermes/OpenClaw 配置、工具、cron 或 secret；本次未调用 OpenClaw。

## 经验沉淀

1. 当工具输出要被 Agent 当作报告证据时，应优先由工具本地 mapper 生成 bounded canonical entry，并由 shared stage 只执行统一 contract，因为 vendor schema 不应渗入中央流水线；边界是 mapper 还需 coverage/hash/redaction/error contract。
2. 当 registry、skills 或 adapters 会持续新增时，应优先维护“known gaps + no-new-gap ratchet”，因为一次性迁移无法阻止未来 silent drift；边界是 discovery/import blocked 必须有独立可见状态。
3. 当 raw truth 要生成报告、模型上下文或知识库投影时，应优先分开 raw/canonical/projection 并记录 revision、coverage、hash 与 truncation，因为可引用摘要仍可能不完整；边界是 hash 只证明内容绑定，不证明事实真实性。
4. 当模型或 worker 声称任务完成时，应优先由宿主按 requirement→evidence、成功 effect/readback 和 typed terminal 独立判定，因为 prose/tag/成功计数只是 claim；边界是 verifier 本身也需固定版本和 fixture。
5. 当不可信输入方可能选择测量问题、时钟或 reference 时，应优先由宿主生成 challenge、持久化 issuance 并在最终评价前覆盖 client fields，因为被测对象不能定义自己的证据门槛；边界是 challenge 不是 authorization 或 identity。
6. 当 reference data 参与自动结论时，应优先要求 source、checked time、真实 observation 和 explicit verified gate，因为“有来源”不等于“在目标配置上成立”；边界是 verified 还需要 freshness、review 和撤销。
7. 当分数为 0 或 findings 为空时，应优先区分 `not_evaluated/insufficient/coherent/blocked` 并披露 coverage，因为没有观测不能投影成 negative evidence；边界是 coherent 也不能证明安全、真实或未修改。
8. 当多个 checks 共享根因时，应优先按 evidence body 分组、做单调有界聚合并验证独立性，因为逐 check 简单加分会重复计权；边界是任何评分都需真实 corpus calibration，不能直接成为高风险自动决策。
9. 当上游项目没有 release、CI 或公开复现 corpus 时，应优先固定 commit、运行本地 contract tests 并明确待核验 lane，因为 Stars、新鲜提交和 0 issues 都不是成熟度证明。

### 今日总 Skill 升格判断

- `evidence-promotion-ratchet-v0`：**需二次验证**；跨 Agent 横切，但先与 GitHub-learning、verification-first、completion/receipt、shared-governance 去重。
- `verified-reference-gate-v0`：**需二次验证**；只抽象 host-owned challenge/verified/abstention，不迁移浏览器 fingerprint 代码或数据。
- OpenSRE 完整 runtime：**暂不沉淀**；public alpha、依赖与 authority surface 大、open stream bug、配置和生产数据风险高。
- anti-mage 完整检测能力：**暂不沉淀**；非当前核心，隐私/公平性/对抗和校准边界未过审。
- 今日不修改 `capabilities/skills/`、manifest、curated active facts、Hermes config/model/provider/tools/cron/secret。

## 明日继续

1. 建立 `evidence-promotion-ratchet-v0` synthetic fixture，至少覆盖新增 unmapped source、mapper exception、partial/truncated evidence、optional adapter import blocked、raw/redacted mismatch。
2. 在同一 fixture 增加 requirement→evidence binding，证明“成功工具数 > 0”不能让错误 requirement 完成，并输出 exactly-one terminal reason。
3. 建立 `verified-reference-gate-v0`，验证 client 注入 host fields、unverified source、expired/replayed challenge、zero-score abstention；不采真实 browser data。
4. 复核 OpenSRE issue #5872 是否有修复 PR；若修复，固定新 commit 运行 BaseException + worker-death fixtures，不能只看 issue closed。
5. 若继续评估 anti-mage 校准，先寻找可公开复现 corpus、采集脚本、许可与 consent；没有这些前，不引用 README 的 false-positive/median 为稳定事实。

## 候选反哺

### Candidate Facts

- [ ] topic: registry evidence mapper 应采用 known-gap ratchet 防 silent drift | evidence: OpenSRE `merge_tool_evidence`、coverage tests、issue #5519/#5594、60 tests passed | 建议: update verification/GitHub-learning candidate | 安全级别: medium
- [ ] topic: citeable projection 必须与 raw truth 分层并携带 coverage/hash | evidence: OpenSRE `record_evidence_entry` 仅 summary/snippet，VictoriaLogs limit/coverage 缺口 | 建议: create candidate POC，不直接晋升 | 安全级别: medium
- [ ] topic: reference provenance 应以 executable verified gate 控制结论 | evidence: anti-mage `reference.*`、`sec_engineversion.go`、416 tests passed | 建议: update verification candidate | 安全级别: medium
- [ ] topic: zero score 必须配合 abstention/coverage terminal | evidence: anti-mage `summarise` 与真实空 probes API smoke `not-evaluated/0` | 建议: update source-outcome candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: evidence-promotion-ratchet-v0 | 可复用场景: Hermes research sources / shared memory promotion / future-agent tool evidence | 是否建议 shared: yes-after-fixtures | 原因: 横切能力，但需补 coverage/hash/redaction/blocked semantics 并与既有能力去重
- [ ] 名称: verified-reference-gate-v0 | 可复用场景: curated candidate review / benchmarks / compatibility matrices | 是否建议 shared: yes-after-fixtures | 原因: 可复用的是验证门，不是 anti-mage 实现；需 reviewer/freshness/revocation contract
- [ ] 名称: anti-mage-browser-detection | 可复用场景: browser bot scoring | 是否建议 shared: no | 原因: 非当前核心，涉及 fingerprint、隐私、公平、对抗与校准风险
- [ ] 名称: install-opensre-runtime | 可复用场景: SRE incident automation | 是否建议 shared: no | 原因: authority/credential/network/telemetry surface 大，不能由学习 cron 自动接入

### Candidate Open Questions

- [ ] 问题: OpenSRE mapper exception 应 fail investigation、记录 partial，还是 containment 后继续？如何保证 exactly-one terminal？ | reason: gap | priority: high
- [ ] 问题: VictoriaLogs evidence 如何携带 query window、limit、truncated、fetch coverage 与 output hash，而不增加上下文泄漏？ | reason: adaptation | priority: high
- [ ] 问题: OpenSRE issue #5872 的 BaseException/thread-death 修复如何与 queue sentinel、cancel 和 partial stream receipt统一？ | reason: gap | priority: high
- [ ] 问题: anti-mage Verified 由谁审、多久过期、如何撤销，reference 数据许可如何治理？ | reason: gap | priority: high
- [ ] 问题: anti-mage 多 section 权重的独立性与 README 800-sample结果是否有可复现 raw corpus？ | reason: gap | priority: high
- [ ] 问题: nonce 是否应一次性消费；`resolveByControls` fallback 在对抗环境中是否扩大 replay/collision 风险？ | reason: adaptation | priority: medium

### 不应自动落地

- 不安装、setup 或启动 OpenSRE 产品，不连接生产 observability、cloud、Kubernetes、MCP、LLM 或 telemetry。
- 不复制 OpenSRE vendor integrations 或 anti-mage browser probes/reference 数据到 shared；顶层 license 不替代数据/依赖合规审查。
- 不采集真实用户 browser fingerprint，不启用 anti-mage `-dump`，不把 detector score用于封禁、身份或高风险决策。
- 不把 60 个 OpenSRE定向 tests / 416 个 anti-mage unit tests 外推为生产安全、检测有效或全仓 E2E 完成。
- 不把 pip-audit 0、repository advisories 空、Dependabot 403/disabled 外推为无漏洞。
- 不把今日候选直接写入 curated active fact；raw 研究和工具产物留 Hermes inbox/runtime，等待二轮治理。
- 不自动修改 Hermes 配置、模型、provider、tools、cron、secret；本任务禁止且未调用 OpenClaw。
