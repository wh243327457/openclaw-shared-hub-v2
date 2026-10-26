# 2026-10-27 GitHub 热门项目学习日报

> 执行者：Hermes（未调用 OpenClaw）  
> 研究窗口：2026-10-27 07:00–07:40 JST  
> 热门候选来源：GitHub Trending 日榜 HTML；Stars、Forks、Language、License、更新时间均由 `gh api repos/{owner}/{repo}` 实时读取。  
> 深读固定源码：`NVIDIA/SkillSpector@d7338f58200a9ae2a24810cee08911ab68b107a7`、`nightly-labs/openbot@cc1a2fea6a6d689a0961acc242214701434c76a4`。

## 今日结论

Agent 系统真正可迁移的不是“多一个扫描器或桌面壳”，而是两层确定性外壳：安装前用 **输入解析→并行检查→coverage ledger→fail-closed verdict** 阻断不可信 Skill；执行时用 **durable queue→scope lane→hold reason→provider acceptance→terminal reconciliation** 管住长任务与不确定副作用。

## 项目速览

GitHub API 查询基准为本次运行；时间字段为 UTC。`NOASSERTION` 表示 GitHub License API 未识别，不等于“无许可证”。

| 项目 | Stars | Language | License（GitHub API） | pushed_at | 速览判断 |
|---|---:|---|---|---|---|
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 36,112 | CSS | MIT | 2026-10-22T17:20:32Z | 面向编码 Agent 的反 AI-slop 设计 Skill，热度高但今日不深挖。 |
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | 115,981 | Python | Apache-2.0 | 2026-10-16T21:38:46Z | 多 Agent 金融研究框架；高风险领域，不将演示结果外推为投资能力。 |
| [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | 2,818 | TypeScript | Apache-2.0 | 2026-10-26T22:27:59Z | IDE 自适应 Agent；已在昨日研究，今日避免重复。 |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 6,363 | TypeScript | Apache-2.0 | 2026-10-26T17:17:47Z | 开箱即用 Agent；已在昨日研究，今日避免重复。 |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | 22,122 | Python | Apache-2.0 | 2026-10-23T09:40:29Z | Skill 安装前安全扫描器，与 shared skill 治理直接相关，列为深读 1。 |
| [nightly-labs/openbot](https://github.com/nightly-labs/openbot) | 1,422 | TypeScript | NOASSERTION | 2026-10-26T22:11:47Z | 持久 Agent 队列与多 provider 工作台；执行状态机值得研究，列为深读 2。 |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 103,470 | Python | MIT | 2026-10-25T04:37:26Z | 多站点信息读取 CLI；涉及站点条款、登录态与反爬边界，今日不安装。 |

## 深读项目

### 1. NVIDIA/SkillSpector

- **链接**：https://github.com/NVIDIA/SkillSpector
- **固定源码提交**：`d7338f58200a9ae2a24810cee08911ab68b107a7`
- **GitHub API**：Stars **22,122**；Forks **1,931**；Language **Python**；License **Apache-2.0**；`updated_at=2026-10-26T22:31:25Z`；`pushed_at=2026-10-23T09:40:29Z`。
- **Release**：最新可见 release 为 `v2.13.1`，发布于 `2026-10-23T09:40:35Z`；但固定 `main` 提交的 `pyproject.toml` 仍写 `2.12.0`，因此 **main 源码版本、maintenance release 与安装制品不能混称同一对象**。
- **一句话判断**：值得学的不是 71 条规则本身，而是它把“不可信 Skill 扫描”组织成带资源上限、coverage ledger、静态/语义分层、SARIF 输出和 fail-closed 降级的可审计流水线。
- **解决的问题**：替代“读一遍 `SKILL.md`/README 就安装”与“只靠 LLM 判断恶意意图”的旧做法；它先确定性枚举输入和执行面，再可选地让 LLM 做语义补充。

#### 证据交叉核验

1. **README**：说明输入支持 repo/URL/zip/目录/单文件；静态分析 + 可选 LLM；JSON/Markdown/SARIF；100 MiB ingest cap、10,000 zip members、单文件 1 MiB 分析 cap；明确不会执行被扫 Skill。
2. **docs/DEVELOPMENT.md**：给出 LangGraph 数据流、state 字段、fan-out/fan-in 节点与 package layout。
3. **Release `v2.13.1`**：说明原子/拒绝 symlink 的报告与 baseline 写入、partial gap-fill fail-closed、静态解析误报修复。
4. **Issue #910**：公开 issue 报告 `uv.lock` 中 `anyio 4.14.1`、`certifi 2026.6.17`、`urllib3 2.7.0`、`langgraph-sdk 0.4.2` 存在已发布 advisories；本次已在固定 main 的 lockfile 核对这四个版本确实存在。advisory 可达性及修复落地仍需单独核验。
5. **关键源码**：直接读取 `graph.py`、`resolve_input.py`、`meta_analyzer.py`、`report.py`。

#### 架构 / 实现与数据流

```text
input_path / skill_path
        │
        ▼
resolve_input
  - Git/URL/zip/file/dir → 本地目录
  - 建立全图共享 resource budget
  - 记录 source identity 与 temp cleanup owner
        │
        ▼
build_context
  - inventory / manifest / file_cache / component metadata
  - inspection ledger / executable surface
        │
        ├──► static pattern analyzers
        ├──► behavioral AST / taint analyzers
        ├──► MCP least-privilege / poisoning analyzers
        └──► semantic analyzers（可选 LLM）
                    │ fan-in
                    ▼
              meta_analyzer
  - 按文件/批次语义复核
  - 批次缺失或模型失败时保留确定性 findings
                    │
                    ▼
       finalize_inspection_ledger
  - 计算 complete / partial / exclusions / failures
                    │
                    ▼
                 report
  - baseline suppression → risk score → verdict
  - Terminal / JSON / Markdown / SARIF projection
```

核心模块边界清楚：`InputHandler` 负责 materialize 输入，`build_context` 建 canonical scan context，analyzers 只产出 findings/ledger events，`finalize_inspection_ledger` 统一 coverage，`report` 再做评分和多格式投影。关键价值是 **finding 与 coverage 分开**：0 finding 只有在 coverage 完整时才可能被解释为低风险。

#### Repo tree 摘要

以下目录来自固定提交的 `git ls-tree`：

```text
SkillSpector/
├── .github/              # CI、release、Scorecard 等工作流
├── .opencode/            # OpenCode 适配资源
├── contrib/              # batch scanner 等扩展工具
├── docs/                 # 架构、资源边界、抑制、扩展说明
├── extensions/           # Pi / OpenCode 等集成面
├── scripts/              # 构建、release、维护脚本
├── skills/               # 项目随附 Skill 资源
├── src/
│   └── skillspector/
│       ├── nodes/        # graph nodes 与 analyzers
│       ├── providers/    # 各 LLM/provider adapter 与 model registry
│       └── yara_rules/   # YARA 规则
└── tests/                # unit / node / integration / provider / fixtures
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/skillspector/graph.py` | 工作流装配 | 注册 resolve/build/analyzers/meta/finalize/report；analyzer 可用性检查；fan-out/fan-in。 |
| `src/skillspector/nodes/resolve_input.py` | 输入归一化 | 统一 Git/URL/zip/file/dir；共享 deadline；异常时清理临时树；保留 source identity。 |
| `src/skillspector/nodes/build_context.py` | canonical scan context | 枚举组件、缓存文本、识别 manifest 与执行面、记录跳过/部分分析。 |
| `src/skillspector/nodes/meta_analyzer.py` | LLM 语义复核 | 按文件和 token budget 分批；找不到 batch result 时保留 finding 并标 review failed。 |
| `src/skillspector/nodes/finalize_inspection_ledger.py` | coverage 收口 | 将 analyzer event 汇总为 complete/partial/failed 与有效 finding IDs。 |
| `src/skillspector/nodes/report.py` | verdict 与投影 | baseline、去重、风险加权、coverage 降级、SARIF/JSON/Markdown/terminal。 |
| `src/skillspector/input_handler.py` | 远端与归档输入 | ingest cap、zip member cap、路径与临时目录生命周期。 |
| `src/skillspector/providers/_agent_cli.py` | CLI provider 边界 | stdin 传不可信文本、环境清理、超时与 fail-closed；README 明确 Codex CLI provider 当前禁用。 |

#### ⭐ 源码精读

**函数 1：`create_graph()`——analyzer registry 驱动的 fan-out/fan-in。**

```python
def create_graph():
    """Create and compile Skillspector workflow graph."""
    workflow = StateGraph(SkillspectorState)

    workflow.add_node("resolve_input", resolve_input)
    workflow.add_node("build_context", build_context)
    workflow.add_node("meta_analyzer", meta_analyzer)
    workflow.add_node("finalize_inspection_ledger", finalize_inspection_ledger)
    workflow.add_node("report", report)

    wired_analyzers = []
    for analyzer_id in ANALYZER_NODE_IDS:
        mod = ANALYZER_MODULES.get(analyzer_id)
        is_available = getattr(mod, "is_available", None)
        if callable(is_available) and not is_available():
            logger.warning("Skipping analyzer %s: is_available() returned False", analyzer_id)
            continue
        workflow.add_node(
            analyzer_id, guard_analyzer_node(analyzer_id, ANALYZER_NODES[analyzer_id])
        )
        wired_analyzers.append(analyzer_id)

    workflow.add_edge(START, "resolve_input")
    workflow.add_edge("resolve_input", "build_context")
    for analyzer_id in wired_analyzers:
        workflow.add_edge("build_context", analyzer_id)
        workflow.add_edge(analyzer_id, "meta_analyzer")
    workflow.add_edge("meta_analyzer", "finalize_inspection_ledger")
    workflow.add_edge("finalize_inspection_ledger", "report")
    workflow.add_edge("report", END)
    return workflow.compile()
```

逻辑摘要：新增 analyzer 通过 registry 接入，不需要手改每条 edge；`guard_analyzer_node` 将 analyzer 异常纳入统一 ledger，而不是让“某检查没跑”静默变成 clean。

**函数 2：`resolve_input()`——共享 deadline 与 cleanup ownership 从入口建立。**

```python
def resolve_input(state: SkillspectorState) -> dict[str, object]:
    input_path = state.get("input_path")
    skill_path = state.get("skill_path")
    workflow_budget = ensure_workflow_resource_budget(state)

    if input_path and isinstance(input_path, str) and input_path.strip():
        handler = InputHandler(
            transitive_budget=workflow_budget,
            allow_git_credentials=state.get("allow_git_credentials", True),
        )
        try:
            resolved, source_type = handler.resolve(input_path.strip())
            temp_dir = handler.temp_dir_for_cleanup()
            update: dict[str, object] = {
                "skill_path": str(resolved),
                "primary_file_path": handler.primary_file_path,
                "selected_source_identity": selected_source_identity_for_input(
                    input_path.strip(), source_type=source_type,
                    resolved_path=resolved, temp_dir=temp_dir,
                ),
                "workflow_resource_budget": workflow_budget,
            }
            update["temp_dir_for_cleanup"] = str(temp_dir) if temp_dir is not None else None
            return update
        except BaseException:
            handler.cleanup()
            raise
```

逻辑摘要：预算从下载/clone/解压前开始，而非进入 analyzer 后重置；即使 interrupt/cancel 落在临时目录创建后，也走 `BaseException` cleanup，明确资源 owner。

**函数 3：`meta_analyzer()`——模型失败不能删除确定性 finding。**

```python
def meta_analyzer(state: SkillspectorState) -> MetaAnalyzerResponse:
    findings: list[Finding] = state.get("findings", [])
    if not findings:
        return {
            "findings": [],
            "effective_finding_ids": [],
            "meta_review_required": False,
            "inspection_ledger": [],
            "analyzer_status_events": [
                analyzer_status_event(
                    analyzer_id="meta_analyzer",
                    status="not_applicable",
                    reason=LedgerReason.NO_APPLICABLE_FILES,
                )
            ],
        }

    if state.get("use_llm", True) is False:
        filtered = _fallback_filtered(findings)
        return {
            "findings": filtered,
            "effective_finding_ids": _effective_finding_ids(filtered),
            "meta_review_required": False,
            "inspection_ledger": [],
            "analyzer_status_events": [
                analyzer_status_event(
                    analyzer_id="meta_analyzer",
                    status="disabled",
                    reason=LedgerReason.DISABLED_BY_CONFIGURATION,
                )
            ],
        }
```

逻辑摘要：没有 finding 是 `not_applicable`，显式关闭 LLM 是 `disabled`；两者不是同一状态。更后面的异常分支使用 passthrough/default remediation，并把失败写入 ledger。

**函数 4：`_compute_risk_score()` 与 report fail-closed——风险分数和覆盖完整性分层。**

```python
def _compute_risk_score(
    findings: list[Finding],
    has_executable_scripts: bool,
    component_metadata: list[dict[str, object]] | None = None,
) -> tuple[int, str, str]:
    # 同一 rule 最多计前三次，权重 1.0 / 0.5 / 0.25；
    # finding confidence 参与贡献，执行文件 finding 可乘 1.3。
    # SC8/部分 SC9 等 closed proof 另设 blocking floor。
    final_score = min(100, max(score_floor, int(score)))
    severity_band, recommendation = risk_severity_and_recommendation(final_score)
    return final_score, severity_band, recommendation

# report() 中的 coverage 降级：
if (
    degraded
    or fatal_exception
    or entirely_uninspected > 0
    or incomplete
    or transitive_truncation_reasons
) and risk_recommendation == "SAFE":
    risk_recommendation = "CAUTION"
```

逻辑摘要：分数衡量“看见的 finding”，coverage 衡量“看了多少”；扫描不完整时即使分数低，也不能输出 SAFE。这比把“0 finding”硬解释为安全更适合 shared skill 安装 gate。

#### 依赖分析与供应链风险

`pyproject.toml` 要求 Python `>=3.12,<3.15`。核心依赖包括：

- 工作流/模型：`langgraph>=1.0.10`、`langchain-core>=1.2.17`、`langchain-openai>=1.1.10`、`langchain-anthropic>=1.4.5`、`langchain-aws>=0.2.0`、`openai>=2.25.0`；
- 网络/模型验证：`httpx>=0.28.0`、`pydantic>=2.12.0`、`pyyaml>=6.0.1`；
- 安全分析：`yara-python>=4.5.0`、`regex==2026.5.9`、`packaging>=24.0`；
- 云端：`boto3>=1.34.0`、`google-auth[requests]>=2.53.0`；
- CLI：`typer>=0.23.0,<0.24`、`rich>=14.3.0`；可选 MCP `mcp>=1.29.0,<2.0.0`。

供应链判断：

- `uv.lock` 是固定解析图，但 issue #910 报告的四个 advisory 版本在固定 main 中真实存在；**lock 提供可复现性，不自动提供安全性**。
- README 说明 LLM 模式会把 analyzer-eligible 文件内容发给配置 provider；即使 `--no-llm`，SC4 仍会把依赖坐标发给 OSV.dev。私有 Skill 必须先决定是否允许出域。
- YARA、LangGraph、多个云 SDK 与 provider adapter 扩大依赖面；应把 scanner 自身的 lock audit 与扫描结果分开报告。
- 本次 public repository security advisories API 返回 0 条，但 Dependabot vulnerability-alerts endpoint 为 404/不可读；不能据此声称“无漏洞”。

#### 本机验证

固定 main 提交上执行：

```bash
uv run --python 3.12 --all-extras python -m pytest -q \
  tests/unit/test_cli.py tests/nodes/test_report.py
# 561 passed, 1 skipped in 24.79s
```

随后执行静态最小 demo：

```bash
uv run --python 3.12 --all-extras python -m skillspector.cli scan \
  tests/fixtures/safe_skill --no-llm --format json \
  --output /tmp/skillspector-safe-2026-10-27.json
# exit=0
# risk_assessment: score=0, severity=LOW, recommendation=SAFE
# coverage: 1/1 components, 100%, complete=true, execution_successful=true
```

第一次直接调用 `uv run ... pytest` 时命中了宿主 Python 3.11 的 pytest 脚本，产生 2 个 collection import error；已改用 `python -m pytest` 绑定 uv 的 Python 3.12 后获得上述真实结果。此失败说明验证命令也需要绑定 interpreter identity。

#### 可复用经验

- 当第三方 Skill 将被装入高权 Agent 时，应优先执行 **immutable source identity + 本地静态扫描 + coverage gate + 人工 review**，因为 README、Stars 和 LLM “看起来安全”都不能证明全部执行面被检查；边界是静态 scanner 不是 sandbox。
- 当语义模型参与安全分析时，应优先让确定性 finding 保持 canonical、模型只做 enrich/dispute，并把未返回 batch 标为 partial，因为模型超时或拒答不能删除已有证据；边界是 deterministic 规则仍会误报。

#### 30 分钟可尝试实验

已完成最小实验：在隔离 clone 上，以 `--no-llm` 扫官方 safe fixture，读取 JSON 的 `risk_assessment`、`analysis_completeness` 与 exit code。下一步可用一个 synthetic malicious fixture 验证 shared gate 是否会同时阻断 `DO_NOT_INSTALL`、incomplete coverage 与 scanner internal failure。

#### 风险边界

- **License**：GitHub API 与仓库均为 Apache-2.0，可研究和按许可复用；仍需审第三方依赖许可证。
- **维护活跃度**：最新 release 为 2026-10-23，仓库 2026-10-23 有 push；活跃，但 main/release version 漂移必须 pin commit/tag。
- **安全风险**：open issue #910 指向 scanner 自身锁文件 advisories；LLM/OSV 有出域；MCP HTTP transport 无认证但限制 loopback；静态分析不执行目标也不隔离后续运行。
- **局限/不适用**：README 明确非英语、图片、加密/二进制、runtime behavior 覆盖有限；static-only SAFE 不是运行期安全证明。
- **未验证**：未运行完整 suite、provider live tests、Docker、MCP server、LLM 分析、真实 shared skills 扫描；v2.13.1 release asset 与 main 2.12.0 的差异未做二进制/源码对照。

#### ⭐ Skill 升格判断

**需二次验证。** 不复制 NVIDIA 的完整规则库为 shared skill；先把“安装前 gate contract”做成 agent-neutral POC，并验证 false positive、partial coverage、scanner failure、private-input egress 与 exact source pin。若收益成立，优先更新现有 `shared-skill-governance` / verification 流程，而不是创建重复大 Skill。

#### Hermes / shared hub 落地路径

仅提出路径，不自动改配置、cron 或 active skill：

1. POC：`runtime/hermes/github-learning-poc/skill-install-gate-v0/`。
2. 候选入口：`scripts/skill_security_gate.py`，输入必须为共享根相对路径或经过 `resolve_shared_root.py` 解析的目标、commit/hash、scan mode；输出 JSON/SARIF 到 `runtime/hermes/`。
3. Gate contract：`scanner_state + coverage + recommendation + exact artifact identity + reviewed_by`；`scanner_failed/partial/unknown` 不得投影为 allow。
4. Hermes adapter：在“复制进本地 `~/.hermes/skills` 或晋升 `capabilities/skills/`”之前调用；今天不修改 Hermes 配置。
5. Future-agent/OpenClaw adapter：将来只消费同一 canonical verdict，不复制规则；本次未调用 OpenClaw。
6. 通过 fixture 和治理审查后，才更新现有 `docs/shared-skill-governance.md` 或相邻 class-level skill，并同步 manifest；candidate 不直接写 curated active fact。

---

### 2. nightly-labs/openbot

- **链接**：https://github.com/nightly-labs/openbot
- **固定源码提交**：`cc1a2fea6a6d689a0961acc242214701434c76a4`
- **GitHub API**：Stars **1,422**；Forks **179**；Language **TypeScript**；License **NOASSERTION**；`updated_at=2026-10-26T22:31:37Z`；`pushed_at=2026-10-26T22:11:47Z`。
- **仓库许可证实读**：根 `LICENSE` 为 **PolyForm Noncommercial 1.0.0**；README 说明商业使用需另行许可，`<=0.1.11` 才保留 Apache-2.0。
- **Release**：最新 `v0.51.1`，发布于 `2026-10-26T16:26:20Z`；同日还有 `v0.51.0`，显示维护活跃但变化快。
- **一句话判断**：它的价值不在“再造一个 Agent 产品”，而在把 provider session、持久 mailbox、每任务 lane、hold reason、timeout-uncertain、恢复与终态 reconciliation 放进宿主拥有的状态机。
- **解决的问题**：替代“一个会话一个内存队列、进程退出即丢、busy 时靠模型自己等、provider timeout 就盲重试”的旧做法。

#### 证据交叉核验

1. **README**：明确 local-first、多 provider、每 Agent workspace、FIFO queue、crash-safe persistence、agent-to-agent messaging；同时警告 preview 默认 `danger-full-access`、`approvalPolicy: never`。
2. **docs/architecture/structure.md**：定义 renderer/contracts/preload/main/backend 依赖方向，SQLite `openbot.db` 为 agents/conversations/queues 等真相源。
3. **docs/architecture/agents.md**：说明 scheduler 启动前重读 routine、task lane、恢复、handoff、agent communication policy 与任务并发限制。
4. **Release `v0.51.1`**：包含 AppImage crash handler、worktree mobile build、provider/CPU limit 等修复。
5. **Issue #3330**：bot-to-bot message 当前不能 steer，说明多 Agent 交互控制面仍有已知缺口。
6. **关键源码**：直接读取 `src/backend/agent/drain-scheduler.ts` 与 `queue-controls.ts`。

#### 架构 / 实现与数据流

```text
Desktop / Web / Mobile / Automation input
                │
                ▼
       typed contract + IPC/API validation
                │
                ▼
           MailboxStore (SQLite)
  queued → starting → running → completed/failed/interrupted
                │ durable admission
                ▼
        DrainScheduler.scheduleDrain
                │
                ├─ lane: agent main chat
                └─ lane: each agent task
                │
                ▼
     hold composition / TurnSlots / limits
  active-turn, one-turn, task-limit, hidden, channel,
  compaction, routine, usage-limit, provider replacement…
                │ allowed
                ▼
 provider/session prepare → turn/start request
                │
        ┌───────┴────────┐
        ▼                ▼
 confirmed turn      timeout / refusal / failure
 mark running        uncertain wait / restore / terminal
        │                │
        └───────┬────────┘
                ▼
 TurnLifecycle + mailbox reconciliation + UI projection
```

关键设计是 admission、wake、drain、provider acceptance 与 terminal 分开：`scheduleDrain()` 只是 advisory wake；真正执行前 `#drainLane` 重验 holds；`turn/start` timeout 不盲重试，而把 delivery 留在 `starting` 并等待 lifecycle event，五分钟后仍无 turn 才 settle 为 interrupted。

#### Repo tree 摘要

固定提交有 6,139 个 tracked files；以下目录来自 `git ls-tree` 与架构文档：

```text
openbot/
├── apps/                   # auth-api、mobile、site-router、status 等应用
├── packages/
│   ├── contracts/          # 进程/网络边界类型与验证
│   ├── ui/                 # SolidJS 共享 UI
│   ├── team-client/        # Team/WebRTC 客户端与恢复
│   ├── logging/            # 脱敏日志
│   └── telemetry/          # bounded retry telemetry
├── remote/                 # Signal/coturn/消息 relay
├── resources/              # managed skills、import resources
├── scripts/                # 开发、E2E、release、package 验证
├── src/
│   ├── backend/
│   │   ├── agent/          # drain、turn、thread、provider runtime、queue controls
│   │   ├── database/       # SQLite core、projection、history store
│   │   ├── agent-tasks/    # task lifecycle
│   │   ├── workflows/      # workflow graph/run state
│   │   └── routine-flows/  # routine handoff state
│   ├── main/               # Electron lifecycle、可信 IPC、OS adapter
│   ├── preload/            # 窄 typed bridge
│   └── renderer/           # SolidJS UI
├── tools/                  # Biome/GritQL、UI/check tooling
├── vendor/                 # remote desktop patches 等 vendored surface
└── docs/                   # 架构、provider、security、运维说明
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/backend/agent/drain-scheduler.ts` | 队列执行核心 | lane identity、hold composition、turn slot、provider start、uncertain timeout 与 reconciliation。 |
| `src/backend/agent/queue-controls.ts` | 用户队列变更 | cancel/edit/update/reorder/steer；channel ownership 与 task thread 校验；失败后恢复 queued。 |
| `src/backend/mailbox-store.ts` | durable mailbox | delivery 状态、nextQueued、attachment verification、terminal 写入。 |
| `src/backend/agent/turn-lifecycle.ts` | provider turn 收口 | turn end、error、usage/failover 与后续 drain。 |
| `src/backend/agent/thread-lifecycle.ts` | provider session | start/resume/recovery/routine thread/handoff。 |
| `src/backend/database/database-core.ts` | SQLite 事务与事件 | append events、projection、command receipts、嵌套事务 owner。 |
| `src/backend/database/conversation-writer.ts` | 会话投影 | 高频 streaming 只更新变化 message，避免反复重写全历史。 |
| `packages/contracts/` | 稳定边界 | IPC/Team API/schema/limits；旧 protocol profile 冻结。 |

#### ⭐ 源码精读

**函数 1：`laneKey()` / `laneOf()`——主聊天与 task 使用稳定复合 lane identity。**

```typescript
function laneKey(lane: Lane): string {
  return lane.taskId === null ? lane.agentId : `${lane.agentId}\u0000${lane.taskId}`;
}

function laneOf(key: string): Lane {
  const separator = key.indexOf("\u0000");
  return separator < 0
    ? { agentId: key, taskId: null }
    : { agentId: key.slice(0, separator), taskId: key.slice(separator + 1) };
}

const mainLane = (agentId: string): Lane => ({ agentId, taskId: null });
```

逻辑摘要：主聊天保持原 agent ID 兼容旧 map，task 用不可见分隔符形成复合 key；lane 是 scheduler 并发、hold、turn model 与 drain receipt 的统一作用域。

**函数 2：`#heldBy()`——等待原因由宿主状态合成，而不是让模型猜。**

```typescript
#heldBy(lane: Lane): string | null {
  const { agentId, taskId } = lane;
  if (this.#settingsHolds.has(agentId)) return "session-settings";
  if (this.#laneTurnActive(lane)) return "active-turn";
  if (
    this.#tasks.oneTurnAtATime(agentId) &&
    this.#lanesOf(agentId).some((other) => other.taskId !== taskId && this.#laneRunning(other))
  ) return "one-turn";
  if (taskId !== null) {
    if (this.#tasks.threadId(taskId) === null) return "task-closed";
    const running = this.#tasks
      .openTaskIds(agentId)
      .filter((other) => other !== taskId && this.#laneRunning({ agentId, taskId: other })).length;
    if (running >= this.#tasks.limit(agentId)) return "task-limit";
  }
  if (agent?.hiddenAt !== undefined) return "hidden";
  if (taskId === null && !(this.#channels?.mayDrain(agentId) ?? true)) return "channel";
  if (!this.#profileSave.mayDrain(agentId)) return "profile-save";
  if (!this.#duplication.mayDrain(agentId)) return "duplication";
  if (!this.#compaction.mayDrain(agentId)) return "compaction";
  if (!this.#routines.mayDrain(agentId)) return "routine";
  if (!this.#usageLimits.mayDrain(agentId)) return "usage-limit";
  return null;
}
```

逻辑摘要：每个控制器拥有自己的 `mayDrain` 条款，scheduler 只组合；reason 是结构化状态，可用于日志/UI/retry policy。源码中 `agent` 的取得位于节选中间，以上为保留判定顺序的核心片段。

**函数 3：`#scheduleLane()`——wake 去重，真正执行前再次重验。**

```typescript
#scheduleLane(lane: Lane, followUsageLimit = true): boolean {
  const key = laneKey(lane);
  if (this.#hooks.isStopping() || this.#scheduledDrains.has(key)) return false;
  const hold =
    (!this.#providers.isReady() && "providers-not-ready") ||
    (this.#drainingLanes.has(key) && "drain-running") ||
    this.#heldBy(lane) ||
    (this.#heldByMachine(lane) && "machine");
  if (hold) this.#reportHold(lane, hold);
  if (followUsageLimit && (!hold || hold === "usage-limit") && this.#hooks.followUsageLimit(lane.agentId))
    return true;
  if (hold) return false;
  this.#scheduledDrains.add(key);
  const completion = Deferred.makeUnsafe<void, DeliveryStartFailed>();
  this.#drainTasks.set(key, completion);
  queueMicrotask(() => {
    Effect.runFork(
      Effect.gen({ self: this }, function* () {
        this.#scheduledDrains.delete(key);
        const exit = yield* Effect.exit(this.#hooks.isStopping() ? Effect.void : this.#drainLane(lane));
        yield* Deferred.done(completion, exit);
        if (this.#drainTasks.get(key) === completion) this.#drainTasks.delete(key);
      }),
    );
  });
  return false;
}
```

逻辑摘要：同 lane 的 scheduled wake 被集合去重，但不同 lane 可并发；发布 `drainTasks` 早于 microtask，使删除/关闭流程能等待尚未真正开始的 attempt。`#drainLane` 内再次检查 holds，防止 schedule→run 的竞态窗口。

**函数 4：`startDelivery()`——provider 接受与 mailbox running 分两步。**

```typescript
readonly startDelivery = Effect.fn("DrainScheduler.startDelivery")(function* (
  this: DrainScheduler,
  context: DeliveryContext,
) {
  const { delivery } = context;
  let confirmedTurnId: string | null = null;
  let turnMayRun = false;
  const releaseReservation = this.#memory.reserveTurn();

  yield* Effect.gen({ self: this }, function* () {
    for (const item of batch)
      yield* this.#mailbox.markStarting(item.delivery.id).pipe(toDeliveryStartFailed);
    this.#mailboxSync.emitQueue(delivery.recipientAgentId);
    yield* this.#mailbox.verifyDeliveryAttachments(delivery.id).pipe(toDeliveryStartFailed);

    const response = yield* startTurn(threadId);
    if (!this.#hooks.turnEnded(response.turn.id)) snapshot.activeTurnId = response.turn.id;
    confirmedTurnId = response.turn.id;
    for (const item of batch)
      yield* this.#mailbox.markRunning(item.delivery.id, response.turn.id).pipe(toDeliveryStartFailed);
  });
});
```

逻辑摘要：先 durable `starting`，验证 attachment，再请求 provider；收到权威 turn ID 后才进入 `running`。若 `turn/start` timeout，后续分支设置 `turnMayRun=true`，等待 lifecycle，而不是可能重复执行同一任务。

**函数 5：`QueueControls.steer()` 的失败恢复——副作用不成功时把 delivery 放回队列。**

```typescript
yield* client
  .request("turn/steer", { threadId: session, expectedTurnId: turnId, input: deliveryPromptInput(...) }, decodeRecordResponse)
  .pipe(
    toQueueOperationFailed,
    Effect.tapError(() =>
      this.#mailbox.restoreUnsteered(input.deliveryId, turnId).pipe(
        toQueueOperationFailed,
        Effect.andThen(queueStep(() => {
          this.#mailboxSync.syncMailboxMessages(snapshot);
          this.#mailboxSync.emitQueue(agent.id);
          this.#drain.scheduleDrain(agent.id);
        })),
      ),
    ),
  );
yield* this.#mailbox.markRunning(input.deliveryId, turnId).pipe(toQueueOperationFailed);
```

逻辑摘要：steer 必须绑定 `expectedTurnId`；请求失败后恢复 unsteered 并重新 schedule，成功后才把 queued delivery 关联到 running turn。Issue #3330 说明 bot-to-bot steer 仍未覆盖，不能把这一机制外推到所有消息类型。

#### 依赖分析与供应链风险

根 `package.json`：`bun@1.4.2`，Node `>=24.0.0`，monorepo workspaces 为 `apps/*`、`packages/*`、`remote/api`。核心依赖包括：

- Agent/provider：`@anthropic-ai/claude-agent-sdk@0.3.309`、`@anthropic-ai/sdk@0.137.0`、`@agentclientprotocol/sdk@1.9.0`、`@modelcontextprotocol/sdk@1.32.1`、`@muse-code/sdk@1.4.12`；
- UI/runtime：`solid-js@2.0.0-rc.18`、`effect@4.0.6`、`electron-updater@6.8.11`、`zod@4.6.7`、`ws@8.22.0`；
- 内容处理：`marked@18.1.1`、`mermaid@12.2.0`、`pdfjs-dist@6.4.299`；
- build/dev：`electron@44.9.3`、`electron-builder@26.18.0`、`vite@8.3.5`、`vitest@4.1.12`、`typescript@7.0.2`；
- `trustedDependencies`：`electron-winstaller`、`esbuild`、`workerd`；另有多个 patched dependencies 和 vendored remote-desktop patches。

供应链判断：

- exact pin 与 `bun.lock` 有利于复现，但 Electron、provider CLI 自动下载、native Computer Use/remote desktop、Cloudflare、mobile、patch/vendored code 形成很大的制品矩阵。
- README 说明部分 provider runtime 只靠 TLS（上游不提供 hash）；不同 CLI 又有 GitHub digest、npm integrity 或 manifest checksum，不能用单一“已 pin”概括。
- 本机没有 Bun，因此未执行 `bun install --frozen-lockfile`、test、typecheck、build 或 audit；不能把仓库的测试脚本数量外推为通过。
- public repository security advisories API 返回 0，Dependabot alerts endpoint 404/不可读；不能据此声称依赖安全。

#### 可复用经验

- 当 durable queue 的 wake、admission 与 effect execution 分离时，应优先把 wake 视为可合并提示、在 drain 前重验所有 hold，并在 provider 确认后才进入 running，因为 schedule 成功不等于任务已经执行；边界是跨进程仍需 lease/事务。
- 当 provider start 超时但副作用可能已发生时，应优先进入 `starting/outcome-uncertain`、等待 lifecycle/read-back 后再收口，而不是立即重试，因为 transport timeout 不证明 provider 没接单；边界是最终仍需有界 grace period 与人工恢复。

#### 30 分钟可尝试实验

设计一个不接 provider 的 SQLite/Python fixture：同一 agent 的 main lane 与两个 task lane 入队；注入 `task-limit`、`usage-limit`、`turn/start timeout`、late turn event；验证同 lane wake 合并、不同 lane 并发、timeout 不重复 dispatch、每个 delivery exactly-one terminal。由于本机 Bun 不可用，今日未运行上游实现测试，此实验只能验证抽象 contract，不能证明 OpenBot 本体。

#### 风险边界

- **License**：GitHub API 为 `NOASSERTION`；仓库根许可证实为 PolyForm Noncommercial 1.0.0，商业复用需要另行许可。禁止复制源码进 shared；只可独立抽象通用机制并保留证据。
- **维护活跃度**：2026-10-26 同日连续发 `v0.51.0`/`v0.51.1`，main 当日继续 push；活跃但 churn 高，接口需 pin commit。
- **安全风险**：README 明示 development preview，Agent 当前 `danger-full-access` 且 `approvalPolicy: never`，能读写宿主、运行命令、联网和控制浏览器；local-first 也不是 offline-only。
- **局限/不适用**：若需求只是 Hermes/shared hub 的调度 contract，引入完整 Electron/Cloudflare/mobile/native stack 明显过重；issue #3330 表明 bot-to-bot steering 尚不完整。
- **未验证**：无 Bun，未运行任何 OpenBot test/build/audit/Electron/provider/runtime；未动态验证 SQLite crash recovery、timeout late event、mobile/Team API、sandbox 或发布制品。

#### ⭐ Skill 升格判断

**暂不沉淀。** 完整产品与源码既受 noncommercial 许可证约束，又与当前 shared hub 的 cron/reflection/orchestrator 能力大面积重叠；只保留“durable lane + typed hold + uncertain-start reconciliation”作为 candidate workflow，待独立 fixture 验证后再判断是否更新既有 orchestrator protocol。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/durable-lane-reconciliation-v0/`，只用 synthetic SQLite events。
2. Canonical schema：`run_id / agent_id / lane_id / attempt / status / hold_reason / effect_certainty / terminal / evidence`；不从日志 prose 反解析状态。
3. Hermes adapter：未来可让 `github_learning_orchestrator.py`、reflection/long-task runner 使用同一 admission/terminal contract；先不改现有 cron。
4. shared hub：若 fixture 发现现有流程会 duplicate dispatch 或错误 completed，优先更新现有 `orchestrator-protocol`、verification-first、自我反思相关 skill，不新增产品同名 Skill。
5. Future-agent/OpenClaw：若未来接入，仅实现 thin adapter；本次 OpenClaw runtime 不存在且未调用。
6. 许可证边界：只写独立规范和测试，不复制 TypeScript 源码、UI、品牌、release assets 或 vendor patches。

## 经验沉淀

1. **当不可信 Skill 将进入 Agent 执行面时，应优先把输入 identity、确定性 findings、coverage ledger 与 verdict 分开，因为 0 finding 可能只是 scanner 没看完；边界是完整静态覆盖仍不等于运行期安全。**
2. **当 LLM 参与安全审计时，应优先让模型只 enrich/dispute，不能删除 canonical deterministic finding，因为 timeout、拒答与 schema failure 都不是负面证据；边界是确定性规则本身仍需误报基线和版本化。**
3. **当队列由多个事件唤醒时，应优先按 immutable lane 合并 wake、在 drain 前重验 hold，因为全局串行浪费吞吐、每请求独立 loop 又会破坏顺序；边界是跨进程必须再加 lease/事务。**
4. **当 provider 请求超时但可能已被接收时，应优先记录 outcome unknown 并等待 lifecycle/read-back，因为立即 retry 可能重复副作用；边界是等待必须有 deadline 和可见恢复动作。**
5. **当 GitHub API License 为 NOASSERTION 时，应优先直接读取仓库 LICENSE 并停止源码迁移，因为 API 未识别不代表无条款；边界是顶层许可证也不能覆盖全部依赖和 release assets。**
6. **当验证命令依赖指定 runtime 时，应优先通过该 runtime 的解释器调用 test module，因为 PATH 上的同名脚本可能绑定另一解释器；边界是定向测试只能证明所选文件与环境。**
7. **当 main、tag、release 与 package version 不一致时，应优先分别记录 commit/tag/artifact identity，因为“最新版本”不是单一对象；边界是 commit hash 也不能证明发布制品可复现。**

## 今日真实验证汇总

| 对象 | 实际执行 | 结果 | 可外推范围 |
|---|---|---|---|
| GitHub Trending + API | `curl` Trending；`gh api repos/...`、release/issues/license | 7 个候选元数据真实返回 | 仅查询时点，不代表未来数据 |
| SkillSpector 固定 main | Python 3.12 + `uv --all-extras` 定向 pytest | **561 passed / 1 skipped** | CLI/report 两个测试文件；非完整 suite/provider |
| SkillSpector safe fixture | `--no-llm --format json` | exit 0；score 0；coverage 1/1、100%、complete | 只证明该 fixture 的 static lane |
| OpenBot 固定 main | repo/docs/source/release/issues 静态读取 | 源码与契约已核验 | 无 Bun，build/test/runtime 全部待核验 |
| GitHub security endpoints | public advisories + vulnerability alerts | public advisories 均 0；alerts 均 404/不可读 | **不能**据此声称无漏洞 |

## 明日继续

1. 在 `runtime/hermes/github-learning-poc/skill-install-gate-v0/` 做 4 个 fixture：safe、malicious、partial coverage、scanner internal failure；验收点是 unknown/partial 绝不变 allow。
2. 在 `runtime/hermes/github-learning-poc/durable-lane-reconciliation-v0/` 做 timeout→late event 与 crash→startup reconcile；验收点是每个 delivery exactly-one terminal、无 duplicate dispatch。
3. 二者均先与现有 verification-first、orchestrator protocol、shared-skill-governance 去重；只有发现真实缺口再更新 class-level skill。

## 候选反哺

### Candidate Facts

- [ ] topic: Skill 安装 gate 必须把 finding 与 coverage 分开 | evidence: `SkillSpector@d7338f5` 的 ledger/report fail-closed；本机 561 passed/1 skipped + safe fixture complete | 建议: create candidate（非 active fact） | 安全级别: medium
- [ ] topic: durable queue 的 schedule/wake 不等于 effect started | evidence: `openbot@cc1a2fe` 的 `#scheduleLane`、`#drainLane`、`startDelivery` | 建议: create candidate，先做独立 fixture | 安全级别: medium
- [ ] topic: timeout 后 provider effect 可能 outcome unknown | evidence: OpenBot `TURN_START_GRACE_MS` 与 unconfirmed start 分支 | 建议: update 既有 completion/effect certainty candidate | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: skill-install-gate-v0 | 可复用场景: Hermes/future-agent/shared skill 安装或晋升前审计 | 是否建议 shared: no（当前） | 原因: 需验证 scanner 自身依赖、隐私出域、partial/false positive；成熟后优先更新已有治理 skill
- [ ] 名称: durable-lane-reconciliation-v0 | 可复用场景: cron、长任务、多 agent lane、provider timeout 恢复 | 是否建议 shared: no（当前） | 原因: 与现有 orchestrator/verification 候选重叠，先用 synthetic fixture 证明真实增益

### Candidate Open Questions

- [ ] 问题: SkillSpector `main` 的 `2.12.0` 与最新 maintenance release `v2.13.1` 应以哪个 artifact 做长期 gate？ | reason: conflict | priority: high
- [ ] 问题: issue #910 的四个 lock advisories 在当前 scanner 调用路径中的实际 reachability 与修复版本何时落地？ | reason: gap | priority: high
- [ ] 问题: Hermes 现有 cron/orchestrator 是否存在 provider ACK 丢失后重复 dispatch 的真实路径？ | reason: adaptation | priority: high
- [ ] 问题: OpenBot issue #3330 修复后，bot-to-bot steer 是否仍保持 expected turn identity 与失败恢复语义？ | reason: stale | priority: medium

### 不应自动落地

- 不自动安装 SkillSpector、OpenBot 或其 MCP/provider/runtime。
- 不自动修改 Hermes/OpenClaw 配置、model、provider、cron、secret 或本地 Skill。
- 不把候选直接写入 `curated/memory/` active facts；本报告保留在 Hermes inbox，POC 只进 runtime。
- 不复制 PolyForm Noncommercial 的 OpenBot 源码、UI、品牌或制品到 shared。
- 不把 static-only SAFE、public advisories=0、Stars、release 频率或定向测试外推为生产安全。
