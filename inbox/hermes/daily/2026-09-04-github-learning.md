---
type: case
status: archived
created: 2026-09-04
updated: 2026-09-04
domain: learning
tags: [github-learning, agent-engineering, research-orchestration, effect-safety]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
  - "[[03-学习/技术实践/00-技术实践索引]]"
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-09-03-GitHub热门项目学习日报]]"
---

# 2026-09-04 GitHub 热门项目学习报告

> 执行者：Hermes（当前 OpenClaw 运行时不存在；本次未调用 OpenClaw）  
> 查询时间：2026-09-04T12:28:21+08:00 至 12:36:40+08:00  
> 发现方法：GitHub Search API 查询 `created:>=2026-08-20 stars:>20`，按 Stars 降序；项目速览的 Stars、Forks、Language、License、`pushed_at`、`updated_at` 均来自 GitHub repository/license API。  
> 深读固定提交：`sapientinc/PRAXIST@afba7a9cbe7071666c96a02c976b16ec518e0ae2`；`anthropics/commerce-agents@fd4d59224ab96b43c6dc6888207c67b3bd5a24cf`。动态热度快照与固定源码 revision 分开记录。

## 今日结论

今天的共同主线是：**长期 Agent 系统必须把“可读信号、可继承事实、模型建议、获准副作用”分成不同语义层，并在最终提交点重新验证。** PRAXIST 用 canonical/validation/derived/partial 角色和 generation boundary 控制“下一代能继承什么”；commerce-agents 用同一个 executor、provenance gate、当前 guardrail 和 host approval 控制“模型建议何时能变成业务写入”。但两仓也同时证明：设计文档、类型和绿色 CI 都不能替代端到端控制——PRAXIST 的开放 issue 显示 budget grant 仍可能只是事后记账、run artifact 仍可能泄漏 provider credential。

### 今日真实验证摘要

- PRAXIST：固定 HEAD `afba7a9...`；`python3 -m compileall -q praxist` 成功；运行 `tests.unit.test_artifact_semantics_contracts` 与 `tests.unit.test_run_lifecycle_contracts`，真实结果 **32 tests / OK**。固定提交的 GitHub check-runs 为 7/7 success，但只作为上游补充证据。
- commerce-agents：固定 HEAD `fd4d592...`；三个 Python package 树 `compileall` 成功；运行 `commerce-common/tests/test_execution.py` 与 `merchant-agent/core/tests/test_gates.py`，真实结果 **15 passed in 2.58s**。固定提交 GitHub CI checks 为 success。
- 供应链：`uvx pip-audit -r` 对两仓 requirements 均返回 **No known vulnerabilities found**；commerce 的 7 个本地 editable packages 因未注册 PyPI 被明确 skip；其 examples lock 的 `npm audit --omit=dev --package-lock-only` 返回 0 findings（118 dependency records）。这些只覆盖已解析清单和当前 advisory 数据库，不证明未知漏洞、源码逻辑或可达性安全。
- 两仓 latest release API 都返回 404，`SECURITY.md` contents API 都返回 404；Dependabot alerts API 因当前 token 缺 `admin:repo_hook` scope 不可读取。公开 repository security-advisories API 返回空数组，不能据此声称“无漏洞”。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [sapientinc/PRAXIST](https://github.com/sapientinc/PRAXIST) | 6,944 | 519 | Python | NOASSERTION | 2026-09-03T21:05:41Z | **深读：canonical evidence、generation commit、预算与恢复边界** |
| [MengTo/threeui](https://github.com/MengTo/threeui) | 5,075 | 501 | HTML | MIT | 2026-09-03T05:36:26Z | 交互组件目录，偏 UI 展示，不符合今日控制面主线 |
| [crmne/fastpotify](https://github.com/crmne/fastpotify) | 2,854 | 118 | Rust | MIT | 2026-09-03T21:30:36Z | 本地播放器候选；与 Agent/共享中台关联弱 |
| [XiaoDuoYa/codex-with-chatgpt](https://github.com/XiaoDuoYa/codex-with-chatgpt) | 2,420 | 251 | TypeScript | MIT | 2026-09-03T13:54:28Z | 规划/执行拆分候选；需先审 auth 与工具权限 |
| [tobi/walgit](https://github.com/tobi/walgit) | 2,416 | 132 | Rust | MIT | 2026-08-27T01:50:20Z | WAL + Git 数据机制候选；留待数据层专题 |
| [duty1g/x64dbg-mcp-server](https://github.com/duty1g/x64dbg-mcp-server) | 1,863 | 190 | Zig | MIT | 2026-09-02T20:34:21Z | 高权 debugger MCP；无人值守任务不安装、不连接 |
| [anthropics/commerce-agents](https://github.com/anthropics/commerce-agents) | 1,649 | 266 | Python | Apache-2.0 | 2026-09-01T20:41:14Z | **深读：共享 executor、provenance/approval/effect gate** |
| [ApodexAI/FrontierAgent](https://github.com/ApodexAI/FrontierAgent) | 1,596 | 135 | Python | Apache-2.0 | 2026-09-04T04:29:13Z | ReAct/Agent Team/TUI 候选；当天仍高频变动 |
| [N4darae/anti-mage](https://github.com/N4darae/anti-mage) | 1,419 | 54 | Go | MIT | 2026-09-02T10:01:40Z | 2026-09-01 已深读，今日避免重复 |

> 注：Stars 会继续变化；commerce-agents 的 API 快照在任务期间由 1,647 增至 1,649，表中采用 12:36:40+08:00 的最后一次真实快照。GitHub `open_issues_count` 包含 PR；License API 也不能替代依赖、数据、模型、品牌和发布物的完整合规审查。

## 深读项目

### 1. sapientinc/PRAXIST

- **一句话判断**：值得学的是它把连续研究从“多轮聊天”提升为“冻结配置 → 并行实验 → 分层证据 → 有序 generation commit → 可恢复继承”的控制面；更值得警惕的是，其公开 issue 显示声明的 budget/credential 边界尚未全部落到最终执行点。
- **解决的问题**：替代让 Agent 直接凭 transcript、leaderboard 或任意结果文件规划下一轮的旧做法；把任务事实留给 task project，把调度、证据、预算、回放和生命周期留给 task-agnostic core。
- **URL / API 快照**：https://github.com/sapientinc/PRAXIST ；**Stars 6,944 / Forks 519 / Language Python / License NOASSERTION**；`updated_at=2026-09-04T04:24:56Z`，`pushed_at=2026-09-03T21:05:41Z`，repository API `open_issues_count=10`，default branch `main`。
- **固定提交**：[`afba7a9cbe7071666c96a02c976b16ec518e0ae2`](https://github.com/sapientinc/PRAXIST/commit/afba7a9cbe7071666c96a02c976b16ec518e0ae2)，commit API 时间 `2026-09-03T15:58:09Z`；tag `0.5.0` 指向较早提交 `92b7853...`，不能把 main 的测试与发布包等同。
- **Release / issue 证据**：latest release API 404；仓库存在 tag `0.5.0`。开放 issue [#84](https://github.com/sapientinc/PRAXIST/issues/84) 报告 peer runtime shell snapshot 把 provider API key 写进 run artifact；[#81](https://github.com/sapientinc/PRAXIST/issues/81) 报告 grant 500k tokens 的 run 实际约 6M tokens（issue 作者复现，**本机未复现，待核验**）；[#83](https://github.com/sapientinc/PRAXIST/issues/83) 报告 CPU-only host 上 GPU job 0 admitted 却继续烧 token；[#43](https://github.com/sapientinc/PRAXIST/issues/43) 记录 resume public surface 与部分 startup 边界仍不一致；[#189](https://github.com/sapientinc/PRAXIST/issues/189) 报告示例 frozen hash 漂移。本机真实计算 `examples/rocket_booster_recovery/src/plant_adapter.py` SHA-256 为 `b6a68c67...`，而两个 evaluator 仍含 issue 所述 `63f543e2...` pin，确认固定 HEAD 存在该 mismatch 代码状态，但本机未跑完整 canary。
- **来源交叉核验**：README、`docs/concepts/architecture.md`、`runtime-model.md`、research-loop/budget docs、GitHub API/check-runs/issues、核心源码与本机 32 个定向 tests。

#### 架构/实现与数据流

1. CLI/resolver 读取 task project、plugins、provider/runtime 和 baseline，先写 run-local frozen configuration。
2. `GenerationLoop` 为每代组装 task prompt、角色、agenda、frontier/incubator/Gems、negative evidence、peer memory 和 evaluator contract。
3. peer 只在独立 variant 下实现假设，经 task-owned evaluator 产出 result；materializer 把可用摘要转换为 finding。
4. artifact 被显式分为 `canonical_state`、`validation_signal`、`derived_view`、`audit_snapshot`、`partial_output`；只有符合 runtime fact 语义的 committed state 能驱动恢复与下一代。
5. 一代结束按固定顺序 ingest/refresh/update/synthesize，最后写 `gen_N/generation_boundary.json`；无 contiguous marker 的结果仍是 pending boundary work。
6. runtime request 把 model profile、tool permission、env policy、credential ref、budget grant、artifact scope、timeout、cache policy 标准化；plugin adapter 负责具体 provider/runtime。
7. budget guard 在高成本动作前可要求 active grant，在结束后记录 exact/partial/unknown usage；然而 issue #81 说明累计 token ceiling 未必在每个最终 model-call chokepoint 强制执行，故不能把 grant 类型或 ledger 当硬限额。

```text
task project (objective + evaluator + constraints)
  -> resolver / frozen run config
  -> GenerationLoop
      -> parallel peer variants
      -> task evaluator -> results
      -> materialize -> findings / frontier / validation signals
      -> PI/Chair synthesis -> next agenda
  -> ordered close -> generation_boundary.json
  -> next generation / resume only from eligible committed state
```

#### repo tree 摘要

```text
PRAXIST/
├── praxist/core/                    # 稳定协议：runtime、budget、artifact、storage、replay、registry
├── praxist/plugins/                 # runtime/provider/tool/workflow/budget/topology 等可替换实现
├── praxist/cli/                     # setup/start/status/stop/resume/takeover/doctor
├── tests/{unit,integration,...}/    # contract、hardening、adversarial、migration tests
├── docs/concepts/                   # ownership、state/replay、runtime model
├── docs/guides/                     # research loop、budget、scheduler、provider、skills
├── skills/                          # Codex/Claude 操作 runbook；不是 task truth
├── templates/tasks/                 # task harness 模板
├── examples/                        # Python/Rust rocket-booster 完整示例；占 tracked files 大头
├── services/product_usage/          # 可选 usage collector
├── pyproject.toml                   # core/optional/dev 依赖与 packaging
├── requirements.txt                 # 旧式宽范围依赖清单，无版本 pin
└── LICENSE.md                       # Fair Source License Agreement 1.0
```

> `git ls-files` 实查 4,547 个 tracked paths，其中 examples 3,742、`praxist/` 306、tests 192、templates 176；因此“仓库很大”主要受示例及 Rust vendoring 影响，不能等同于 Python core 体量。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `praxist/core/protocol.py` | runtime-neutral 协议 | `AgentRunRequest/Result`、tool/env/cache/sandbox intent、budget request/decision；把 provider wire object 隔离在 adapter 外 |
| `praxist/core/storage.py` | artifact 与 ledger 写入 | payload redaction、atomic replace、content hash、artifact role/status/source refs、artifact index |
| `praxist/core/trajectory.py` | append-only event truth | thread lock + POSIX file lock、递增 event id、redaction、flush+fsync |
| `praxist/plugins/workflow_stages/research_loop/backend/resume_state.py` | generation commit / resume identity | canonical boundary marker、evidence cutoff、task/model identity mismatch 拒绝 |
| `praxist/core/execution_guards.py` | 高成本 action budget envelope | grant preflight、usage/unknown records、late accounting warning |
| `tests/unit/test_artifact_semantics_contracts.py` | 语义回归 gate | derived/partial 不得覆盖 canonical，boundary marker 才是 runtime fact |
| `tests/unit/test_run_lifecycle_contracts.py` | stop/resume 路径 gate | malformed stop signal fail-safe、run-local path/symlink 限制、wall-clock stop |

#### ⭐ 源码精读

**代码块 1：`ArtifactWriter.persist_json()` 先 redaction 和 canonical serialization，再交给统一 artifact writer。**

```python
def persist_json(self, artifact_type: str, logical_path: str,
                 payload: dict[str, Any], *, schema_ref: str | None,
                 producer: dict[str, str], artifact_role: str | None = None,
                 artifact_status: str | None = None,
                 runtime_fact_source: bool | None = None, ...) -> dict[str, Any]:
    redacted_payload, hits = redact_json(payload)
    payload_bytes = (
        json.dumps(redacted_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return self._persist_payload(..., payload_bytes=payload_bytes,
        redaction_hits=hits, artifact_role=artifact_role,
        artifact_status=artifact_status, runtime_fact_source=runtime_fact_source)
```

逻辑摘要：同一 writer 生成 payload、SHA-256、metadata、artifact index 和 `artifact.persisted` trajectory event；`artifact_role/status/runtime_fact_source` 让 reader 不必从文件名或 prose 猜权威性。边界是 redactor 的 coverage 仍需测试，issue #84 正说明另一条 shell-snapshot 写入路径可绕过统一 writer。

**代码块 2：`TrajectoryWriter.emit()` 在 scope/actor/payload 全部 redaction 后，以锁、递增序号和 fsync 追加 event。**

```python
def emit(self, kind: str, *, severity: str = "info",
         scope: dict[str, str] | None = None,
         actor: dict[str, str] | None = None,
         payload: dict[str, Any] | None = None, ...) -> dict[str, Any]:
    redacted_payload, payload_hits = redact_json(payload or {})
    with _TRAJECTORY_THREAD_LOCK, self.path.open("a+b") as handle:
        _lock_file(handle)
        self._seq = max(self._seq, _latest_trajectory_seq(handle)) + 1
        event = {"seq": self._seq, "event_id": f"evt_{self._seq:06d}",
                 "kind": kind, "scope": redacted_scope,
                 "actor": redacted_actor, "payload": redacted_payload}
        handle.write((json.dumps(event, sort_keys=True) + "\n").encode())
        handle.flush(); os.fsync(handle.fileno())
        return event
```

逻辑摘要：事件顺序由 host writer 产生，不信任 agent 自报；file lock 解决 POSIX 同文件并发追加。边界是 Windows 分支不执行 `fcntl`，且 append-only + fsync 不等于签名、防回滚或跨多文件事务。

**代码块 3：`write_boundary_marker()` 把一代是否完成收口为 canonical marker，并只引用 committed Gems。**

```python
def write_boundary_marker(run_dir: Path, *, gen_id: int,
                          promoted_count: int, pi_status: str, ...) -> None:
    canonical_sources = [
        f"gen_{gen_id}/generation_results.json",
        "frontier/frontier_manifest.json",
    ]
    if is_committed_runtime_fact_file(run_dir / "gems" / "gems_state.json"):
        canonical_sources.append("gems/gems_state.json")
    payload = {
        "artifact_semantics": artifact_semantics(
            role=CANONICAL_STATE, status=COMMITTED,
            stage="generation_boundary", generation_id=gen_id,
            runtime_fact_source=True, canonical_sources=canonical_sources),
        "generation_id": gen_id, "promoted_count": promoted_count,
        "pi_status": pi_status,
    }
    atomic_write_json(run_dir / f"gen_{gen_id}" / BOUNDARY_MARKER_FILENAME, payload)
```

逻辑摘要：结果/leaderboard 文件存在不表示代已提交；marker 在 ordered close 最后写，resume 可据此区分 committed 与 pending。边界是 marker 依赖前序检查正确；它记录 sources 但不是整个外部 effect 世界的事务 commit。

**代码块 4：`BudgetedActionGuard.start()/finish()` 区分 admission gate 与 late accounting。**

```python
def start(self) -> None:
    if self.require_budget_grant and not self.budget_grant_id:
        self._emit_event("resource.action_denied", severity="error",
                         payload={"reason": "missing_budget_grant", **self.metadata})
        raise ResourceBudgetError(f"{self.action_type} requires an approved budget grant")
    if self.budget_grant_id and self.run_dir is not None:
        BudgetLedger(self.run_dir, self.run_id).require_active_grant(self.budget_grant_id)
    self._emit_event("resource.action_started", payload=self.metadata)

def finish(self, *, actual_usage=None, expected_units=(), status="succeeded", ...):
    # 只把 finite/nonnegative 且 grant 已批准的 unit 写入 ledger；缺失 unit 写 usage_unknown
    # late accounting exception 只产生 warning，尽量保留已有研究结果
```

逻辑摘要：这正确表达了“没有 grant 可拒绝启动”“计量缺失不得写 0”“事后记账失败不应抹去科学结果”。但 issue #81 的关键是：active grant preflight 不等于累计剩余额度在每次模型调用前被强制扣减，故 shared hub 不能只复制这个 API 形状。

#### 依赖分析与供应链风险

- `pyproject.toml` core 仅声明 `pyyaml>=6.0`、`jinja2>=3.1`、`pydantic>=2.7,<3`；optional `agents/codex/storage/product-usage-server/docs` 扩展会引入 Anthropic/OpenAI/MCP、OCR/PDF、AWS、FastAPI/Postgres 等更大网络与解析面。
- `claude-agent-sdk==0.2.136`、`openai-codex==0.147.0`、`codex-relay==0.5.5` 有精确 pin，但大量其他依赖为范围版本；仓库根没有 `uv.lock/poetry.lock/Pipfile.lock`，`requirements.txt` 又是无版本宽清单。固定 git commit 不足以复现 Python dependency graph。
- Rust 示例有 `Cargo.lock` 且 CI 用 `--locked --offline`，但 vendored tree 占 3,742 个 example paths 中的大部分，扩大 review/更新负担。
- 本机 `uvx pip-audit -r requirements.txt` 返回 0 known vulnerabilities；这是按当前无 pin resolver 解析出的图，不是 release `0.5.0` 的 immutable SBOM。Dependabot alerts 不可读。
- Actions 中 `actions/checkout@v4`、`astral-sh/setup-uv@v3` 使用可移动 major tag 而非 commit SHA；CI 供应链 pinning 弱于 commerce-agents。

#### 可复用经验

- 当长期任务同时产生报告、prompt、leaderboard、partial result 与可继承事实时，应优先为 artifact 声明 `role + status + runtime_fact_source + source identity`，并只让 committed canonical state 驱动恢复；因为“文件存在”不说明它有权成为下一轮真相，边界是 schema 仍需 writer/reader conformance tests。
- 当一个阶段的完成会改变下游规划时，应优先最后写一个 generation/phase boundary marker，并让无连续 marker 的数据停留在 pending；因为多文件流程无法靠任一中间文件证明整体提交，边界是 marker 不是跨外部系统事务。
- 当预算是安全上限而非观测指标时，应优先在每个昂贵 call/admission chokepoint 校验剩余额度并停止新工作，而不是只验证 grant 存在或事后写 overrun；因为 ledger 准确不等于控制有效，边界是 in-flight call 仍需 drain 与不确定 usage 处理。
- 当所有 artifact 理论上都会 redaction 时，应优先做“secret canary 扫描整个 run tree”的端到端 fixture，因为绕过统一 writer 的 snapshot/log 路径会泄漏，边界是 regex canary 不能证明所有 secret 类型都被覆盖。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/canonical-boundary-budget-gate-v0/` 做纯 Python fixture：

1. 构造 `canonical_state/validation_signal/derived_view/partial_output` 四类 artifact；
2. 证明 resume reader 只接收 `committed + runtime_fact_source=true + matching run/revision`；
3. 模拟两个昂贵 calls，第二次 admission 发现 remaining budget 不足后 `blocked`，而不是运行后只记 overrun；
4. 向 fake env/snapshot/log 注入 secret canary，扫描整个 run tree，不仅扫描 canonical writer；
5. 输出 exactly-one terminal：`completed|blocked|needs_verification|failed`。不调用 provider，不安装 PRAXIST，不改 Hermes 配置/cron/skills/curated。

#### 风险边界

- **License**：GitHub API 为 `NOASSERTION`；仓库 `LICENSE.md` 是 Fair Source License Agreement 1.0，并非 OSI 开源许可。年总收入达到 US$1M 后需协商 commercial license；第三方分发、输出公开 attribution 等另有限制。只抽象机制，不复制代码/skills/templates 到 shared。
- **维护活跃度**：main 最后提交 2026-09-03，固定 commit 7 个 check-runs success；10 个 open non-PR issues，说明维护活跃但产品边界快速变化。latest release API 404，tag 0.5.0 与 main 不同 revision。
- **安全风险**：issue #84 报告明文 provider key 进入 run artifact；本机未复现真实 provider run，但其影响与 shared 目录禁写 secret 规则直接相关。`SECURITY.md` API 404，公开 advisories 空不能作为安全证明。
- **成本/资源风险**：issue #81/#83 指向 token budget 不硬拦截、无可满足 GPU job 时仍运行的组合风险；这些是 issue 作者数据，未本机 E2E 复现，必须标“待核验”，但在验证前不能把系统用于无人值守高预算研究。
- **恢复局限**：#43 指向 resume surface 与部分 startup 边界仍不完整；本机 32 个 tests 只证明两个 contract files 在当前 Python 环境通过，不证明真实 crash、多进程、provider、GPU 或跨平台恢复。
- **供应链局限**：Python graph 无根 lock；requirements 无 pin；optional SDK/OCR/cloud 面较大。pip-audit 0 findings 只覆盖当前解析，不证明未来 resolver 或可达路径。
- **不适用**：不应把 PRAXIST 整个 runtime 引入 Hermes/shared hub，也不应在未解决 credential/budget/resource preflight 前让它接管现有 cron。

#### ⭐ Skill 升格判断

**暂不沉淀 PRAXIST skill；机制需二次验证。** `canonical artifact role + phase boundary + resume identity` 与现有 shared hub 分层、verification-first、completion receipt、orchestrator-protocol 高度重叠，适合先更新既有 contract；hard budget chokepoint 与 whole-run secret canary 是新补强点，但必须先完成 fixture。由于 Fair Source license、#84、#81、#83 未闭环，禁止复制上游源码、skills、templates 或安装 runtime。

#### ⭐ Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/canonical-boundary-budget-gate-v0/`。
- 现有入口优先：增量更新 `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md` 的 phase boundary、remaining-budget admission、whole-run secret canary 条款；不新建重复 skill。
- 审计候选：给 `scripts/github_learning_orchestrator.py` 的 completed 判定增加 `report hash + knowledge-base copy hash + status readback`；当前只提 candidate，不修改生产脚本。
- shared 分层映射：raw evidence 仍进 `inbox/hermes/daily/`，实验进 `runtime/hermes/`，curated 只接收多日验证后事实。
- OpenClaw 当前不存在；未来 adapter 只能消费 agent-neutral artifact/terminal schema，不能把 OpenClaw 路径写入 canonical contract。

---

### 2. anthropics/commerce-agents

- **一句话判断**：值得学的是它把三种运行方式都收敛到同一 tool executor，并把第三方文本、ID provenance、当前 guardrail、host approval 与 backend effect 串成一条确定性路径；这比在 prompt 里要求“谨慎操作”可靠得多。
- **解决的问题**：替代为 Messages API、Agent SDK、Managed Agents 各写一套规则的旧做法；也替代“模型输出了一个合法 ID/说用户已批准，所以直接写业务系统”的错误授权模型。
- **URL / API 快照**：https://github.com/anthropics/commerce-agents ；**Stars 1,649 / Forks 266 / Language Python / License Apache-2.0**；`updated_at=2026-09-04T04:34:25Z`，`pushed_at=2026-09-01T20:41:14Z`，repository API `open_issues_count=3`（包含 PR），default branch `main`。查询 open issues 并剔除 PR 后为 0。
- **固定提交**：[`fd4d59224ab96b43c6dc6888207c67b3bd5a24cf`](https://github.com/anthropics/commerce-agents/commit/fd4d59224ab96b43c6dc6888207c67b3bd5a24cf)，commit API 时间 `2026-08-31T22:48:58Z`。
- **Release / issue 证据**：latest release API 404；tags API 返回空；README 明确写明“reference implementation; it is not maintained and does not accept contributions”。固定提交 CI 的 Python 3.11/3.12、web、no-PyPI-fallback checks success，但仓库本身不承诺持续维护。
- **来源交叉核验**：README、`docs/safety.md`、fixed commit CI、requirements/lock、common/merchant 核心源码与本机 15 个定向 tests。

#### 架构/实现与数据流

1. shopping/merchant 各自定义 prompt、skills、tool contracts、role gates 和 backend interface；`commerce-common` 持有 config、fencing、memory、grounding、presentation、executor、events。
2. Messages API runtime、Agent SDK toolset、Managed Agent MCP server 最终都调用同一 role executor，避免安全规则按 transport 漂移。
3. 外部 catalog/order/merchant text 先 NFKC normalize、移除 invisible/control/forged tags，再包进 source-literal fence 并做长度 cap；dynamic context 位于 cache breakpoint 后。
4. 某些问题形状通过 deterministic grounding rule 强制首个 read tool；返回 ID 被记入 session provenance。
5. merchant write 先校验 model args、session provenance/record-read、options、change guardrails，再由 backend stage；preview 不授予批准。
6. apply 时重新读取 current config 检查 guardrail，并要求 host-owned `approved_change_ids`；通过后才调用 backend effect，再把 applied change 更新给 host。
7. memory extraction 只读最新 user/assistant text、不读 tool result；candidate fact 经过 length/category/filter/dedup，且 extraction 运行期间若 purge generation 改变则整批放弃。
8. tool error 返回 structured outcome 而不结束 turn；loop/size/delegate/search limits 有显式上限。

```text
user turn
  -> deterministic grounding rule -> server-side read
  -> external payload sanitize + source-literal fence
  -> shared BaseToolExecutor
      -> schema validation
      -> provenance / option / guardrail gate
      -> backend stage -> preview only
host approval mark
  -> apply_change
      -> provenance recheck
      -> current-config guardrail recheck
      -> host approval check
      -> backend effect -> change_update
```

#### repo tree 摘要

```text
commerce-agents/
├── commerce-common/                 # 两角色共享 executor、fence、memory、grounding、turn/event
├── shopping-agent/
│   ├── core/                        # storefront backend、tool/gate/prompt/types
│   ├── runtime-messages-api/        # Messages API loop
│   ├── runtime-agent-sdk/           # Agent SDK adapter
│   ├── managed-agents/              # manifest + loopback MCP server
│   └── skills/                      # shopping flows
├── merchant-agent/                  # 同结构；增加 staged changes、approval、analysis
├── examples/                        # retail/travel/telecom/entertainment + 8 web apps
├── plugins/commerce-builder/        # Claude Code scaffold/review plugin
├── docs/{safety,backends,deployment}.md
├── tests/                           # cross-package seams/consumption tests
├── requirements.txt                 # 7 个 editable package + 完整 pin 的第三方 runtime graph
├── requirements-dev.txt             # pytest/ruff 精确 pin
└── LICENSE                          # Apache-2.0
```

> `git ls-files` 实查 571 个 tracked paths，其中 examples 387、merchant-agent 60、shopping-agent 50、commerce-common 34。README 所称“四个 vertical、八个 web apps”与 repo tree 一致。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `commerce-common/commerce_common/execution.py` | 三运行面的公共 tool chokepoint | status 剥离、schema parse、tool allowlist、delegate cap、统一 failure ladder |
| `commerce-common/commerce_common/fencing.py` | untrusted text data plane | NFKC、invisible/control/tag/turn marker 清理、固定 label fence、cap |
| `commerce-common/commerce_common/grounding.py` | deterministic first-read routing | ordered rules 返回首个强制 tool；lexicon/config 与 matcher 分离 |
| `commerce-common/commerce_common/turn.py` | streaming/compaction/exact-once dispatch | eager tool overlap、malformed stream salvage、history result clearing、usage/log hygiene |
| `commerce-common/commerce_common/memory.py` | bounded personal memory | fact validation/filter/dedup/retention、purge generation race guard |
| `merchant-agent/core/merchant_agent/gates.py` | apply authorization | seen change、current guardrail、host approval 三门 |
| `merchant-agent/core/merchant_agent/changes.py` | staged change lifecycle | stage/apply 都运行 guardrail；applied/discarded 留审计轨迹 |
| `merchant-agent/core/merchant_agent/executor.py` | role effect adapter | 所有 stage/apply/discard 都经过 shared executor 和 gates |

#### ⭐ 源码精读

**代码块 1：`BaseToolExecutor.execute()/dispatch()` 将错误分类与真实 dispatch 分开，未知/关闭 tool 不会穿透。**

```python
async def execute(self, name: str, tool_input: dict[str, Any] | None) -> ToolOutcome:
    try:
        return await self.dispatch(name, dict(tool_input or {}))
    except InvalidArguments as invalid:
        return ToolOutcome.error(invalid_arguments_text(name, invalid.invalid))
    except Exception as error:
        if (outcome := self.domain_error(error)) is not None:
            return outcome
        logger.warning("tool %s failed and is reported as unavailable", name, exc_info=True)
        return ToolOutcome.error(self.unavailable_text.format(name=name))

async def dispatch(self, name: str, tool_input: dict[str, Any]) -> ToolOutcome:
    tool_input, _status = self.split_status(name, tool_input)
    if name in self._absent: return ToolOutcome.error(...)
    if (handler := self._handlers.get(name)) is None:
        return ToolOutcome.error(f"Unknown tool: {name}")
    return await handler(tool_input)
```

逻辑摘要：模型生成的 `status` 只给 host 展示，进入 validation/gate/backend 前被剥离；argument error、domain refusal、backend failure 有不同 outcome。边界是 executor 内统一不等于 backend 内授权完整，部署方仍负责真实 identity、credential、业务规则和 effect readback。

**代码块 2：`Fence.sanitize_text()/fence_payload()` 防止不可信业务文本伪造角色、tool tag 或 fence boundary。**

```python
def sanitize_text(self, text: str, max_chars: int | None = None) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = _INVISIBLE.sub("", text)
    text = _CONTROL.sub(" ", text)
    marker = _marker_pattern(self.label)
    while True:
        stripped = _SPECIAL_TOKEN.sub("[removed]", marker.sub("[removed]", text))
        if stripped == text: break
        text = stripped
    text = _TURN_INDICATOR.sub(r"\1\2 -", text)
    return bounded(text, max_chars)

def fence_payload(self, payload: Any, max_chars: int = MAX_FENCED_CHARS) -> str:
    body = serialize(self.sanitize_value(payload))
    return f"{self.open}\n{bounded(body, max_chars)}\n{self.close}"
```

逻辑摘要：label 是源码字面量，运行时文本不能选择边界；fixpoint removal 防止嵌套 marker 删除后重组。边界是 fencing 降低 prompt-injection 表达面，不提供 authorization；真正写入仍必须经过后续 provenance/approval gate。

**代码块 3：`check_apply_change()` 在最终 effect 前重验来源、当前 policy 与 host approval。**

```python
def check_apply_change(state: MerchantSessionState,
                       config: MerchantAgentConfig,
                       change_id: str) -> ToolOutcome | None:
    known = state.seen_changes.get(change_id)
    if known is None:
        return ToolOutcome.held(PROVENANCE_GATE, "...not staged or listed...")
    if violations := check_guardrails(known.kind, known.items, config):
        return ToolOutcome.held(GUARDRAIL_GATE, apply_guardrail_message(violations))
    if config.require_host_approval and change_id not in state.approved_change_ids:
        return ToolOutcome.held(APPROVAL_GATE, "...not approved through host surface...")
    return None
```

逻辑摘要：模型在聊天里声称“用户同意”或展示 preview 都不改变 `approved_change_ids`；并且 policy 可能在 stage 后收紧，所以 apply 要重新计算 guardrail。边界是 state 里的 approval mark 仍由部署 host 正确认证与写入；代码只证明 mark 存在，不证明谁有权设置它。

**代码块 4：`MerchantToolExecutor._apply_change()` 让 backend effect 只能位于 gate 后。**

```python
async def _apply_change(self, tool_input: dict[str, Any]) -> ToolOutcome:
    change_id = str(tool_input.get("change_id", ""))
    if held := check_apply_change(self._state, self._config, change_id):
        return held
    try:
        applied = await self._backend.apply_change(self._session, change_id)
    except GuardrailViolation as violation:
        return ToolOutcome.held(GUARDRAIL_GATE,
                                apply_guardrail_message(violation.violations))
    self._state.remember_change(applied)
    return ToolOutcome(applied_confirmation(...),
                       [AgentEvent.change_update(_record(applied))])
```

逻辑摘要：role-level gate 后，backend 还可以执行更严格业务校验；成功后才发布 applied confirmation/change update。边界是方法未展示 effect-specific external readback 或 idempotency key；网络断开时“backend 是否已应用”仍需要部署层 reconciliation。

**代码块 5：`extract_and_store()` 用 purge generation 避免删除期间的慢模型结果把个人数据写回来。**

```python
async def extract_and_store(store: MemoryStore, subject_id: str, client, model,
                            transcript: str, **policy) -> list[MemoryFact]:
    generation = await store.purge_generation(subject_id)
    existing = await store.get_facts(subject_id)
    new_facts = await extract_facts(client, model, transcript, existing, **policy)
    if not new_facts or await store.purge_generation(subject_id) != generation:
        return []
    await store.upsert_facts(subject_id, new_facts)
    return new_facts
```

逻辑摘要：慢 extraction 开始后若用户执行 purge，旧 generation 的 candidate batch 被丢弃，避免 resurrection。边界是 read-generation-check-upsert 不是跨进程原子 CAS；JsonFile store 的 read/write 也未显示跨进程 lock，生产 store 必须提供事务语义。

#### 依赖分析与供应链风险

- 根 `requirements.txt` 明确 pin 第三方 runtime graph：`anthropic==0.122.0`、`claude-agent-sdk==0.2.139`、`mcp==1.29.0`、`pydantic==2.13.4`、`fastapi==0.141.1`、`cryptography==50.0.0` 等；7 个仓库本地 package 通过 editable path 安装。
- 各 package `pyproject.toml` 使用较宽 ranges，但 README/CI 的 canonical 安装路径走 pinned root requirements；CI 另有 `no-pypi-fallback` job，先确认内部包名未注册，再验证孤立安装因 sibling pin 不存在而 fail loudly，降低 dependency-confusion 风险。
- GitHub Actions 的 checkout/setup-python 都 pin 到完整 commit SHA；比移动 major tag 更稳。examples 有 `package-lock.json`，web CI 用 `npm ci`。
- 本机 pip-audit 对第三方 pin 返回 0 known vulnerabilities，但 7 个 editable internal packages被 skip；npm production lock audit 为 0 findings。公开 advisories 空、Dependabot alerts 不可读，不能外推整个系统安全。
- 高权 supply chain 还包括 Claude Code plugin、Agent SDK、MCP、8 个 Next.js apps 和部署脚本；本日未执行 install/plugin/MCP/web build/live model。

#### 可复用经验

- 当同一 tool contract 要跨 Messages API、SDK、MCP 等 transport 复用时，应优先让所有路径委托给单一 deterministic executor，并对每个 adapter 做 conformance test；因为复制 gate 会形成安全漂移，边界是 shared executor 不能替代 transport auth 和 OS sandbox。
- 当模型要引用外部记录 ID 触发写入时，应优先只接受本 session 由权威 read/stage 返回的 ID，并在 final effect 前重验 object/policy；因为 schema-valid ID 仍可能是猜测或跨用户对象，边界是 provenance 不是业务授权。
- 当用户批准发生在聊天外的 host surface 时，应优先让 host 写不可由模型参数设置的 approval mark，并让 preview/chat confirmation 零授权；因为模型可误述“已批准”，边界是 host route 本身必须认证、授权和防 replay。
- 当个人记忆写入依赖慢模型 extraction 时，应优先绑定 purge generation，并要求 transactional compare-and-write；因为删除与异步 extraction 竞态会复活已删除事实，边界是单进程 generation check 不等于跨进程 CAS。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/transport-shared-effect-gate-v0/` 做纯 fixture：

1. 定义一个 shared `execute(tool, args, host_context)`，分别接 CLI/MCP/fake-SDK adapters；
2. fixtures 覆盖 unknown tool、forged external ID、policy tightened after stage、chat-only approval、valid host approval、backend success-but-timeout；
3. 所有 transport 必须得到同一 canonical outcome code/hash；
4. success-but-timeout 进入 `needs_verification`，只允许 readback reconciliation，不自动 replay；
5. 不连接真实 commerce backend/provider，不安装 plugin，不处理真实个人数据。

#### 风险边界

- **License**：GitHub API 与仓库 LICENSE 均为 Apache-2.0；依赖、Claude/Anthropic 品牌、模型服务条款、示例素材和部署环境仍需分别审查。
- **维护活跃度**：固定 HEAD/唯一 commit 为 2026-08-31；README 明确“不维护、不接受贡献”。虽然 CI green、热度增长快，但不能期待安全修复或兼容升级。
- **安全风险**：示例 route 无认证；MCP server 只以 loopback 为默认边界，到达 server 的连接都可调用；deployment 必须补 auth/authz/rate limit/credential isolation/business rules。
- **隐私风险**：memory 是个人数据；DEBUG model logs 包含 injected facts 和整车 cart。reference 的 filter/retention 不是合规制度，生产必须有访问、删除、retention 与日志控制。
- **prompt injection 局限**：fencing/sanitize 只降低伪造 marker/role 的能力，不证明模型不会受业务文本影响；安全性来自写工具仍经过 hard gates。
- **副作用局限**：apply path 展示 gate 与 backend return，但未在本次精读范围看到通用 external idempotency/readback receipt；backend timeout 后是否已写入需部署层处理。
- **运行局限**：本机仅跑 15 个定向 tests 与 compileall；未安装 pinned full graph、未运行完整 pytest、8 个 web builds、live model、MCP、Managed Agents 或真实 backend。
- **不适用**：不能直接部署 examples 到公网，也不能把 demo guardrail 数值当实际业务政策。

#### ⭐ Skill 升格判断

**需二次验证。** 不升格完整 commerce skill；可迁移的是 agent-neutral 的 `transport-shared-executor + session provenance + host approval + effect-time policy revalidation + uncertain-effect reconciliation`。前四项与现有 effect-scope、verification-first、orchestrator/subagent terminal 契约有明显重叠，应优先更新既有 class-level skill；“backend success-but-timeout → needs_verification/readback”需 fixture 后补齐。上游 Apache-2.0 允许复用，但本日只抽象机制，不复制项目源码或领域 prompts。

#### ⭐ Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/transport-shared-effect-gate-v0/`。
- deterministic core：候选模块 `runtime/hermes/.../gate.py` 输出 `allowed|blocked|needs_verification|failed`，输入包含 `run/session/target/revision/effect/policy_revision/approval_revision`。
- Hermes adapter：仅在真实 tool dispatch 前调用 gate；模型不可提交 `approved=true`，approval 必须来自 host state。
- shared skill：验证后优先更新 `autonomous-learning/orchestrator-protocol` 或现有 verification/effect contract，不新增 commerce 专属 skill。
- shared memory：本日只保留 candidate；不得把 assistant prose 直接写 curated user fact。
- OpenClaw 当前不存在；未来只做 adapter conformance，不修改其配置或复制任何 ID/credential/path。

## 经验沉淀

1. **当系统同时产生 raw output、audit snapshot、derived report、validation signal 与长期真相时，应优先给每个 artifact 声明角色、状态、来源 revision 与是否可驱动 runtime；因为文件存在/格式正确不代表有权成为下一步输入，边界是 reader 与 writer 都要做 conformance。**
2. **当多文件或多阶段流程的完成会触发下游动作时，应优先按固定顺序收口并最后写 canonical boundary marker；因为中间 artifact、exit 0 或绿色日志都不能证明整体已提交，边界是 marker 仍不能提交外部不可逆 effect。**
3. **当同一工具要跨 CLI、SDK、MCP 或多个 agent runtime 复用时，应优先共享一个 deterministic executor/gate，再分别验证 transport adapter；因为复制规则会产生安全漂移，边界是单一 executor 不提供 transport auth 或 OS 隔离。**
4. **当模型提交外部对象 ID 或 change request 时，应优先把它当 proposal，只接受由本 session 权威 read/stage 产生的 provenance，并在最终 effect 前重验 target、policy 与 approval；因为合法 ID 和自然语言确认都不是授权，边界是 provenance 仍需业务 ACL。**
5. **当预算被称为硬上限时，应优先在每个昂贵 admission/call 前检查 remaining budget，并为 in-flight work 设计 drain；因为 active grant 与事后 overrun ledger 都不能限制消费，边界是 provider usage 延迟需要保守 reserve。**
6. **当异步 extraction、worker 或 snapshot 可能绕过统一写入器时，应优先用 generation/CAS 和 whole-tree canary scan 验证删除与 secret 边界；因为局部 redaction/filter 不能覆盖旁路，边界是 canary 只证明测试的 secret class。**
7. **当上游 README、类型、CI 与公开 issue 的控制能力冲突时，应优先相信固定源码、issue 复现证据和本机定向 test，并把未复现数据标为待核验；因为设计意图不等于 end-to-end enforcement。**

### 跨项目机制对比

| 问题 | PRAXIST | commerce-agents | shared hub 可取部分 |
|---|---|---|---|
| 什么是可继承事实 | canonical role + committed boundary | session/backend state，不信 model prose | curated/raw/runtime + terminal receipt |
| 什么可以执行 | normalized request + grant/guard | provenance + current guardrail + host approval | proposal/effect 分离 + final chokepoint |
| 恢复如何判定 | generation marker + resume identity | turn repair、purge generation | immutable run/revision + needs_verification |
| 最大已知缺口 | issue 显示 secret/budget/resource enforcement 漏洞 | demo 无 auth，effect uncertainty/readback 由 deployment 承担 | 必须做端到端 fixture，不只抄类型 |

## 明日继续

1. 创建 `runtime/hermes/github-learning-poc/canonical-boundary-budget-gate-v0/`，用 synthetic fixtures 验证 artifact eligibility、remaining-budget admission 与 whole-tree secret canary。
2. 创建 `runtime/hermes/github-learning-poc/transport-shared-effect-gate-v0/`，验证 CLI/MCP/fake-SDK 三 adapter outcome 等价，以及 effect timeout 后只读 reconciliation。
3. 继续观察 PRAXIST issues #84/#81/#83/#189 是否有 maintainer 修复与回归测试；任何 issue 数字在本机复现前继续标待核验。
4. 若 fixture 通过，先提出对现有 `orchestrator-protocol` / GitHub-learning skill 的增量 diff 审核稿；不自动更新 shared skill 或 curated。
5. 对 commerce-agents 如需加深，只运行完整离线 pytest 与 repo consistency check；不启动 demo、不填 provider key、不连接 MCP/backend。

## 候选反哺

### Candidate Facts

- [ ] topic: committed artifact eligibility requires explicit role/status/source and final boundary | evidence: PRAXIST `architecture.md`、`resume_state.py`、本机 32 tests | 建议: update existing autonomous-learning fact after POC/de-dup | 安全级别: low
- [ ] topic: budget grant existence is not equivalent to hard remaining-budget enforcement | evidence: PRAXIST `execution_guards.py` + issue #81（issue 数据未本机复现） | 建议: create open question first | 安全级别: high
- [ ] topic: shared executor reduces cross-transport gate drift | evidence: commerce `execution.py`、`executor.py`、docs/safety.md、本机 15 tests | 建议: update existing effect/verification candidate after adapter fixture | 安全级别: medium
- [ ] topic: purge generation prevents stale async memory extraction resurrection only with atomic compare-and-write | evidence: commerce `memory.py::extract_and_store`；文件 store 无跨进程事务验证 | 建议: open question / synthetic race POC | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: `canonical-boundary-budget-gate` | 可复用场景: cron、长任务、学习代际、阶段发布 | 是否建议 shared: no（当前） | 原因: 与 orchestrator/verification/completion 高度重叠，先 fixture 后更新既有 skill
- [ ] 名称: `transport-shared-effect-gate` | 可复用场景: 同一工具跨 Hermes/future-agent/CLI/MCP adapter | 是否建议 shared: no（当前） | 原因: 先证明三 adapter conformance 与 uncertain effect reconciliation
- [ ] 名称: `whole-run-secret-canary` | 可复用场景: run artifact、snapshot、log、runtime 发布前检查 | 是否建议 shared: no（当前） | 原因: 需要定义 allowlist/redaction scope，避免扫描真实 secret 或误报

### Candidate Open Questions

- [ ] 问题: PRAXIST #84 的 shell snapshot 路径在 `afba7a9...` 是否仍能用无效 canary secret 本机复现，是否已有未合并修复？ | reason: security verification gap | priority: high
- [ ] 问题: PRAXIST #81 的 remaining-token enforcement 是否在 adapter/model-call 层存在但 issue 环境绕过，还是确实只有事后记账？ | reason: conflict/gap | priority: high
- [ ] 问题: commerce backend 在 apply 请求 timeout 时如何区分未执行、已执行但 ACK 丢失、部分执行？ | reason: effect uncertainty | priority: high
- [ ] 问题: commerce `JsonFileMemoryStore` 的 purge-generation check 与 upsert 在多进程下如何原子化？ | reason: concurrency gap | priority: medium
- [ ] 问题: commerce reference 明确不维护后，依赖 pin/advisory 与新 SDK 兼容性由谁承担？ | reason: stale risk | priority: medium

### 不应自动落地

- 不安装、启动或接管 PRAXIST runtime；不执行其 agent-managed `codex --yolo` 路径，不调用 provider/GPU/S3/product-usage 服务。
- 不把 PRAXIST Fair Source 源码、skills、templates 复制进 shared；只保留独立机制分析。
- 不启动 commerce demos、MCP、Managed Agents、Claude plugin 或真实 backend；不填写任何 API key。
- 不自动修改 Hermes/OpenClaw 配置、模型、provider、cron、auth、skills 或 secrets；OpenClaw 当前不存在。
- 不把公开 issue 的 token/cost/security 声明、本机窄测试或 advisory 0 findings直接写入 curated active fact。
- 不用审计关键词、compileall、定向 tests 或 GitHub check-runs冒充真实生产 E2E、安全证明或完整维护承诺。
