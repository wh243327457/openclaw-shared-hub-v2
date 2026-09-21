---
type: case
status: archived
created: 2026-09-21
updated: 2026-09-21
domain: learning
tags: [github-learning, agent-memory, provenance, deterministic-retrieval, memory-security]
---

# 2026-09-21 GitHub 热门项目学习报告

> 执行者：Hermes；当前 OpenClaw runtime 不存在，本次未调用 OpenClaw。  
> 查询与验证时间：2026-09-21 07:31–08:27（UTC+08:00）。发现口径为 GitHub Search API `created:>2026-08-21 stars:>500 sort:stars` 与 agent-memory topic 查询；Stars 是 08:27 API 快照，会继续变化。  
> 深读固定提交：`tigerless-labs/agent-memory@34d12a2f8678d5561aba27bd8ff73c5ae4b6a258`；`okf-memory/okf-agent-memory@9413d7780714165dcb8e82fff73b9f966feb653a`（tag `v0.4.2`）。源码结论只绑定这些 revision。  
> 证据来源：GitHub Repository/Commit/Release/Tags/Issues/Pulls/Checks/Advisories API，README、docs、security policy、lock/module manifests、关键源码与本机 tests/build/validator。临时 clone 位于 `/tmp/github-learning-2026-09-21/`，未写入 shared core。

## 今日结论

**长期记忆不是“把更多文本塞进 prompt”，而是把 push 型不变量、pull 型知识、append-only raw evidence、可重建索引、受限写入与语义/安全 gate 分层；但 file-first 只有在 import/path、并发 ledger、scope 边界和 derived-index 一致性都经过确定性验证时，才真正可迁移。**

### 今日真实验证摘要

- `tigerless-labs/agent-memory`：固定 main commit 的 GitHub CI success；本机 `ruff check .` 与 `mypy` 成功，5 个关键 test files（poisoning/concurrency/recall/storage/supersede）**43 passed / 0 failed**。更宽的受限 suite 实际为 **235 passed / 1 failed / 60 deselected**；失败 `test_paths_are_data_not_defaults` 是 root 环境下测试把用户名 `root` 当禁止子串，误命中源码参数名 `root`，不能写成全绿。两次完整/宽 pytest 超过 420 秒被工具终止，未取得完整 suite 终态。
- agent-memory 固定 main 真实复现两个仍开放边界：恶意 export 的 `../escaped.md` 被 `import_into()` 写到 store 外；`scope=preference/user` 同时返回 `preference/user-notes/leak.md`。对应 issue #18（critical）、#17（high）及修复 PR #15/#38 均仍 open；decision ledger 非原子 issue #19、PR #36 也仍 open。
- `okf-memory/okf-agent-memory`：Go 1.26.0 自动工具链；`go test ./...`、`go vet ./...`、build 全部成功，5 个 package 测试 lane 0 fail；本机构建 binary 对 `knowledge/` 执行 strict+drift 得到 **20 concepts / 0 errors / 0 warnings / 0 broken links / 0 orphans / conformant**，并真实返回 `pkg/okf/types.go` 的 constraint。
- OKF 固定 commit/tag 的 GitHub Build/Test/Validate 与 Release checks success，13 个 tags/releases，公开 repository advisories API 均为空；但 PR #34（跨平台 absolute-path hardening）仍 open，公开 advisory 空也不能证明未知漏洞或依赖可达风险为零。
- 两仓 GitHub vulnerability-alerts endpoint 当前均返回 404，无法据此判断 Dependabot 是否启用；因此不写“无依赖漏洞”。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 11,752 | 733 | Python | MIT | 2026-09-18T16:28:35Z | 昨日已深读；热度继续上涨，不重复分析 |
| [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter) | 8,510 | 593 | HTML | Unlicense | 2026-09-20T13:23:50Z | 内容型仓库，不进入今日 memory runtime 主线 |
| [lnkiai/m3e-canvas](https://github.com/lnkiai/m3e-canvas) | 7,775 | 811 | TypeScript | MIT | 2026-09-16T10:57:11Z | 昨日已深读；今日不重复 |
| [sapientinc/PRAXIST](https://github.com/sapientinc/PRAXIST) | 6,367 | 699 | Python | NOASSERTION | 2026-09-18T07:48:40Z | 已研究且 license 仍未识别，不迁移源码 |
| [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) | 5,161 | 283 | TypeScript | MIT | 2026-09-18T04:45:31Z | compaction 候选，后续与长期记忆 loss contract 对照 |
| [crmne/spotifast](https://github.com/crmne/spotifast) | 4,466 | 203 | Rust | MIT | 2026-09-20T15:01:44Z | 高活跃 Rust 客户端，非今日主线 |
| [ApodexAI/FrontierAgent](https://github.com/ApodexAI/FrontierAgent) | 4,214 | 212 | Python | Apache-2.0 | 2026-09-20T22:25:40Z | Agent 候选，后续需独立固定 revision |
| [Human-Agent-Society/reef](https://github.com/Human-Agent-Society/reef) | 3,780 | 312 | Python | Apache-2.0 | 2026-09-21T00:21:13Z | 活跃多 Agent 项目，后续观察 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | 959 | 61 | Python | MIT | 2026-09-18T17:27:13Z | **深读：evidence-linked file truth + host-triggered distillation** |
| [okf-memory/okf-agent-memory](https://github.com/okf-memory/okf-agent-memory) | 707 | 52 | Go | MIT | 2026-09-20T04:52:54Z | **深读：push codex + pull knowledge + deterministic gate** |

> 表中元数据来自 GitHub API，不采用 README badges。前 8 项为发现/筛选，不作源码、安全或成熟度结论。License 仅是 repository 根识别值，不覆盖依赖、模型、数据、release asset 与服务条款；`pushed_at` 可由任意 ref 推动，不必然等于 default branch HEAD 时间。

## 深读项目

### 1. tigerless-labs/agent-memory

- **一句话判断**：值得学的是“raw archive → evidence-linked memory files → rebuildable cache → progressive recall → reversible manage”闭环，而不是再造一个向量数据库；但固定 main 仍有可本机复现的 import path traversal、scope prefix leak 与开放并发 ledger 问题，现阶段不能接管 shared hub 写路径。
- **解决的问题**：替代把全部历史塞进 prompt、只在向量库保存 opaque chunks、让每个 host 自己判断何时记忆、把 index/cache 当唯一真相，以及无人值守 consolidation 直接物理删除的旧做法。
- **URL / API 快照**：https://github.com/tigerless-labs/agent-memory ；**Stars: 959 / Forks: 61 / Language: Python / License: MIT**；`created_at=2026-09-01T21:52:29Z`，`updated_at=2026-09-20T21:30:07Z`，`pushed_at=2026-09-18T17:27:13Z`，default branch `main`，API `open_issues_count=21`（含 PR），contributors API 当前一页计数 1。
- **固定提交**：[`34d12a2f8678d5561aba27bd8ff73c5ae4b6a258`](https://github.com/tigerless-labs/agent-memory/commit/34d12a2f8678d5561aba27bd8ff73c5ae4b6a258)，committer time `2026-09-09T13:11:30Z`，verified commit；main 此后未包含远端 feature branches 的新实现。
- **Release / issue / checks**：releases/tags API 均为空；README version 0.1.0 不是可下载 release。固定 HEAD 的 CI check success。issue [#18](https://github.com/tigerless-labs/agent-memory/issues/18) 标 critical import traversal、[#17](https://github.com/tigerless-labs/agent-memory/issues/17) 标 high scope prefix、[#19](https://github.com/tigerless-labs/agent-memory/issues/19) 标 medium ledger lost update；PR [#15](https://github.com/tigerless-labs/agent-memory/pull/15)、[#38](https://github.com/tigerless-labs/agent-memory/pull/38)、[#36](https://github.com/tigerless-labs/agent-memory/pull/36) 均 open，不能把其修复描述当 main 事实。
- **来源交叉核验**：README、`CLAUDE.md` invariants、Skill、固定源码、red-team/concurrency tests、各 package manifest/uv.lock、GitHub API、本机 lint/typecheck/pytest 与两个独立 boundary reproducer。

#### 架构 / 实现与数据流

```text
host session / transcript
  -> host dialect maps SessionStart | Stop | PreCompact ... to inject/pause/evict
  -> boundary capture
      -> append exact message increment to archive/sessions
      -> advance watermark
      -> launch distill asynchronously
  -> distill core
      -> retrieve existing candidates into reconcile sheet
      -> external Ask/Executor proposes JSON-line operations
      -> handle/provenance/date/schema checks
      -> one Store.record_many() write path under flock
      -> Markdown truth + MEMORY.md/SQLite projections
  -> read
      -> bounded MEMORY.md injection
      -> BM25 active/history recall (+ optional raw fallback)
      -> read abstract | outline | full | trace provenance
  -> sleep/manage
      -> reversible updates/supersede/proposals/dream report
      -> physical gc remains human-only
```

核心分层是：Markdown memory file 是 truth；raw session/provenance append-only；SQLite FTS/access log 与 `MEMORY.md` 是 derived projection；LLM/host judgement 通过 `Ask: str -> str` 注入 core 外部。`reconcile.Sheet` 只给模型有限 handles，模型不能任意命名已有 memory 来 update/supersede。边界是 fixed main 的 file write 使用 `Path.write_text`，并非 temp+fsync+rename；single flock 覆盖主要 store pipeline，但 `correct()` 先在锁外 find/read，ledger 也不走同锁。

#### repo tree 摘要

固定 commit 共 **120 tracked paths**：

```text
agent-memory/
├── packages/
│   ├── core/          # schema、store、archive、recall、reconcile、distill、manage、index
│   ├── adapters/      # host dialect、hook capture、transcript/setup
│   ├── executor/      # host CLI / endpoint reasoner 与 credentials
│   ├── cli/           # universal shell entry
│   ├── mcp/           # agent-facing MCP adapter
│   └── harness/       # LongMemEval / cross-host evaluation
├── skills/agent-memory/SKILL.md   # recall-before-write 与 supersede discipline
├── tests/
│   ├── unit/          # store/recall/schema/manage/config 等 contract
│   ├── system/        # CLI/MCP/interop/concurrency/sleep stores
│   └── redteam/       # poisoning、traversal、captured reasoner boundaries
├── pyproject.toml     # uv workspace；Python >=3.12
├── uv.lock            # 22 package records，含 7 个 workspace packages
└── .github/workflows/ci.yml
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/core/.../store.py` | single write path | batch 共用 flock/projection；update 不允许悄改事实；supersede 保留 predecessor |
| `packages/core/.../reconcile.py` | LLM 写入权限收窄 | 只允许 sheet handles 被 update/supersede；provenance 默认绑定消息范围 |
| `packages/core/.../distill.py` | boundary consolidation | batch→sheet→negotiate→check→record；失败可 repair 后进入 pending |
| `packages/core/.../recall.py` | active/history/raw 检索 | eligibility 先于 ranking；score = relevance × weight × recency；scope 当前仅 prefix |
| `packages/core/.../injection.py` | resident push view | 只注入 `MEMORY.md` byte-prefix，不调用模型重摘要 |
| `packages/adapters/.../capture.py` | exact raw capture | archive increment 后推进 watermark；distillation 与 capture 分离 |
| `packages/adapters/.../hook_entry.py` | host boundary adapter | hook 始终 exit 0；capture 后异步 `mem distill` |
| `packages/core/.../portability.py` | export/import | fixed main 未做 target containment，本机已复现 store escape |
| `packages/core/.../ledger.py` | proposal decision truth | read-modify-write 无共享 lock，issue #19/PR #36 open |

#### ⭐ 源码精读

**代码块 1：`record_many()` 让所有正常写入共享 lock 与 projection。**

```python
def record_many(self, specs: list[dict[str, object]]) -> BatchResult:
    written, rejected = [], []
    if not specs:
        return BatchResult(written=written, rejected=rejected)
    with store_lock(self.layout):
        for index, spec in enumerate(specs):
            try:
                written.append(self._write_one(_known_fields(spec)))
            except ValidationError as error:
                rejected.append(Rejected(index=index, errors=list(error.errors)))
        self._project()
    return BatchResult(written=written, rejected=rejected)
```

逻辑摘要：CLI/MCP/Manage 最终复用同一入口；batch 中坏 item 被逐项拒绝，其他 item 仍落盘；所有 accepted writes 完成后统一 sync index 和重写 `MEMORY.md`。可迁移点是“write truth 与 derived projection 同一 chokepoint”；边界是多个文件加 index 不是跨文件事务，直接 `write_text()` 在 crash 时仍可能留下 truth/projection drift。

**代码块 2：`reconcile.check()` 只允许模型触碰宿主给出的 handles。**

```python
def check(spec: dict[str, object], sheet: Sheet) -> list[FieldError]:
    op = operation_of(spec)
    handle = str(spec.get(KEY_HANDLE) or spec.get(KEY_SUPERSEDES) or "")
    if op in (OP_SUPERSEDE, OP_UPDATE):
        if not handle:
            errors.append(FieldError(KEY_HANDLE, f"{op} names an existing memory"))
        elif handle not in sheet.handle_names():
            errors.append(FieldError(KEY_HANDLE, f"{handle} is not on the reconcile sheet"))
    if op == OP_NEW and handle and handle in sheet.handle_names():
        errors.append(FieldError(KEY_HANDLE, f"{handle} exists; use update or supersede"))
    return errors
```

逻辑摘要：模型输出是 proposal，不拥有任意 record identity；existing memory 的更新权来自 host-built sheet。`to_record_spec()` 还把 provenance 默认绑定当前 batch pointer。边界是候选召回漏掉旧事实时，模型可创建语义重复的新文件；handle gate 限制 authority，不自动解决 semantic dedupe。

**代码块 3：`distill()` 先 reconcile，再把失败留到 repair/pending，而不是吞掉。**

```python
def distill(store: Store, session: str, messages: list[Message], ask: Ask) -> DistillReport:
    for batch in batching.batches(messages, config.max_distill_input_chars):
        sheet = reconcile.build(store, session, batch)
        outcome = agentic.negotiate(store, sheet, prompt, ask, config)
        specs = queue.drain(session) + outcome.specs
        result, leftovers = _apply(store, sheet, specs, outcome.errors)
        for _ in range(config.repair_rounds):
            if not leftovers:
                break
            retry, errors = reconcile.parse_operations(ask(prompts.repair(...)))
            result_more, leftovers = _apply(store, sheet, retry, errors)
        queued = queue.append(session, [spec for spec, _ in leftovers])
        watermark.settle(session, distilled)
```

逻辑摘要：raw archive/watermark 与 curated write 是两个状态面；解析/校验失败的 operation 可修一次，再进入 pending。边界是 watermark settle 与 pending/store 的 crash atomicity需单独验证；远端 endpoint reasoner失败返回空字符串，当前报告未做真实 provider E2E。

**代码块 4：`Recall.recall()` 先 eligibility，再 ranking，但 `_in_scope` 存在真实 prefix 边界缺口。**

```python
def recall(self, query: str, scope: str | None = None, as_of: str | None = None, ...):
    candidates = index.match(query, pool, SURFACE_ACTIVE)
    if as_of is not None:
        candidates += index.match(query, pool, SURFACE_HISTORY)
    eligible = self._eligible(index.rows(), scope=scope, as_of=as_of)
    hits = self._rank(candidates, eligible, as_of=as_of)
    return hits[:limit]

def _in_scope(self, path: str, scope: str) -> bool:
    return path.startswith(scope.strip("/"))
```

逻辑摘要：inactive/as-of/scope 先过滤，随后 `relevance * weight * recency` 排序；比“先全库 top-k 后 ACL filter”更可靠。但 fixed main 没要求目录 separator。本机创建 `preference/user/exact.md` 与 `preference/user-notes/leak.md` 后，scope `preference/user` 真实返回两条，证明 scope 不是安全边界。

**代码块 5：`import_into()` 信任 payload path，本机已复现写出 store。**

```python
def import_into(store: Store, payload: dict[str, object]) -> int:
    store.layout.ensure()
    files = payload.get(KEY_FILES)
    for entry in files if isinstance(files, list) else []:
        target = store.root / str(entry[KEY_PATH])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(entry[KEY_TEXT]), encoding="utf-8")
    store.rebuild_index()
```

逻辑摘要：迁移 payload 没做 `resolve()` + `is_relative_to(root)`、reserved path 或 symlink containment。今日 synthetic payload `../escaped.md` 返回 `imported=1` 且 `/tmp/.../escaped.md` 真实存在，内容为 `escaped`。这不是“待核验”，而是固定 main 的本机复现；PR #15 尚未合并，因此严禁把不可信 export 交给该入口。

#### 依赖分析与供应链风险

- core manifest runtime dependencies 为 **0**；CLI/adapters/MCP/executor/harness 只声明 workspace packages。`uv.lock` 共 22 package records，其中 7 个 workspace；外部 records主要是 pytest/coverage/mypy/ruff 等 dev toolchain。源码 executor 使用 Python stdlib `urllib`，不是第三方 SDK。
- `.github/workflows/ci.yml` 使用 `actions/checkout@v4`、`astral-sh/setup-uv@v5` mutable major tags，不是 commit SHA pin；CI 安装 Python 3.12 后执行 ruff/mypy/pytest coverage >=85。
- 没有 PyPI release、GitHub release 或 tag；只能从 checkout 安装。main HEAD 09-09，但仓库 `pushed_at` 09-18 来自多条未合并 feature branch；不能把 branch 活跃当 main 已修复。
- public repository security advisories API 返回空数组；vulnerability-alerts endpoint 404。未跑出可信 `pip-audit` 生产图（core 本身零外部 runtime deps）；不能据此写“项目无漏洞”。
- 固定 main 的明确风险比依赖 advisory 更优先：import traversal 可越界写、scope prefix 可跨 group 泄漏、ledger RMW 可丢 decision、`fcntl`/`SIGALRM` 是 Unix-specific，Windows portability 未在本机验证。

#### 可复用经验

- 当多 Agent 共享长期记忆时，应优先把 Markdown/typed files 设为可审查 truth、把 FTS/vector/MEMORY.md 设为可重建 projection，因为缓存损坏不应等于知识丢失；边界是 truth write 与多 projection 仍需 crash-consistency gate。
- 当模型要更新或 supersede 已有记忆时，应优先由宿主提供有限 handles 和 evidence pointers，并只允许这些 identity 被修改，因为模型自由命名会扩大 poisoning/误改面；边界是 recall 漏项仍可能制造重复。
- 当 capture/distill/manage 异步分离时，应优先先 append exact raw evidence、再推进 watermark，并为 failed/pending 留 durable lane，因为 distiller 漏提取不能等于 raw 消失；边界是含 PII/secret 的 raw archive 必须有采集前 policy、scope、retention 与删除覆盖。
- 当 import/export、scope filter 或 ledger 被称为 portability/governance 边界时，应优先用 adversarial fixture 验证 containment、path-component 与 concurrent append，因为“文件可读/有锁”不能证明所有写入口都受保护。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/memory-promotion-gate-v0/` 设计纯 fixture（今日只提案，不自动落地）：输入 `raw_pointer / candidate_fact / existing_handles / target_layer / path / actor / source_revision`，输出 `new | update | supersede | duplicate | reject`；必须覆盖：(1) raw 永不直接 promotion；(2) update/supersede 仅接受候选 handles；(3) `../`、absolute、symlink escape 拒绝；(4) scope 以 path component 匹配；(5) concurrent decision append 不丢失；(6) projection 删除后从 truth 重建结果相同。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 MIT；可抽象机制。依赖、host CLI、模型 endpoint、用户 transcript 与 benchmark dataset 需独立合规。
- **维护活跃度**：09-01 创建，main HEAD 09-09，1 contributor page count，无 tag/release；大量 feature branches/PR 活跃但尚未进入 main。959 Stars 不证明 release/Windows/upgrade stability。
- **安全风险**：fixed main import path traversal 已复现；scope prefix leak 已复现；ledger lost update 有源码证据但本机并发复现未做；raw archive 可能持久化 prompt injection、secret、PII。poisoning tests 证明部分入口把内容当 data，不代表所有消费者都安全。
- **一致性风险**：truth、archive、SQLite、MEMORY.md、watermark、pending、ledger、dream report 是多个文件；主要 writes 有 flock，但没有完整 multi-file transaction/recovery receipt。
- **局限性**：默认 FTS/BM25 是 lexical；optional vector 当前在未合并 branch；`fcntl`、`SIGALRM` 对 Windows 不可移植；MCP 没覆盖 context/sleep/proposal ledger；hook failure 被设计为静默 exit 0，需外部 health signal 才不会长期无记忆。
- **验证局限**：未连接 Gemini/Vertex/host CLI、不跑 LongMemEval、不执行 sleep reasoner、不验证 Windows；完整 pytest 两次超时，宽 suite 有 1 个 root-sensitive false-positive，不能称全仓测试通过。

#### ⭐ Skill 升格判断

**需二次验证。** 不安装该 runtime、不复制其 skill、不替换 shared hub。可迁移的是 evidence-linked candidate write、finite-handle reconciliation、raw-before-derived 与 rebuildable projection；但必须先修/规避 path containment、scope component、ledger locking、crash receipt，并与现有 `shared-memory-bridge`、governance、verification-first 去重。

#### ⭐ Hermes / shared hub 落地路径

1. raw 保持现状：Hermes 原始观察进 `inbox/hermes/daily/`，运行 evidence/index 进 `runtime/hermes/`；不把 transcript 自动直写 `curated/`。
2. promotion gate：在现有治理脚本前增加 agent-neutral candidate manifest：`source_pointer / source_revision / candidate_type / target_path / existing_handles / operation`。
3. deterministic checks：复用 `scripts/resolve_shared_root.py`，对 candidate target 做 canonical root containment、reserved layer、agent lane 与 symlink 检查；scope 用 path components，不能 prefix。
4. projection：`curated/memory/` 仍是 truth，prefill/index/Obsidian 均为 derived projection，记录 source revision/coverage/hash；任何 projection 可删除重建。
5. shared skill：POC、真实 corpus differential 与治理审查通过后，只更新现有 `foundation/shared-memory-bridge`/governance contract，不创建 `agent-memory` 专属重复 skill；不自动改 Hermes/OpenClaw config、cron 或 secret。

---

### 2. okf-memory/okf-agent-memory

- **一句话判断**：值得学的是把必须常驻的行为规则压成 push codex，把事实/决策/约束留在按需 pull 的 typed Markdown graph，并用 `code_refs + governance + strict validator` 把“改哪个文件前应读什么”变成确定性查询；但 AAG 的 token/compliance 宣称与远程 zero-knowledge sync 不能未经独立测量就移植。
- **解决的问题**：替代超大 `AGENTS.md` prompt monolith、把 operational rules 放进语义检索导致永远搜不到的 RAG blindspot、每个 Agent 各有一份漂移文档、只靠 grep 找项目约束、以及知识文件与 source path 没有机器可检验关系的旧做法。
- **URL / API 快照**：https://github.com/okf-memory/okf-agent-memory ；**Stars: 707 / Forks: 52 / Language: Go / License: MIT**；`created_at=2026-09-05T21:26:04Z`，`updated_at=2026-09-20T20:35:21Z`，`pushed_at=2026-09-20T04:52:54Z`，default branch `develop`，API `open_issues_count=2`（含 PR），contributors API 一页计数 6。
- **固定提交 / release**：[`9413d7780714165dcb8e82fff73b9f966feb653a`](https://github.com/okf-memory/okf-agent-memory/commit/9413d7780714165dcb8e82fff73b9f966feb653a)，tag/release `v0.4.2`，committer time `2026-09-19T13:03:25Z`；GitHub Release published `2026-09-19T13:06:24Z`。API 返回 13 个 tags 与 13 个 releases（v0.1.0–v0.4.2）。
- **Release / issue / checks**：固定 commit 的 CI 与 Build & Publish Release checks success。v0.4.2 notes 声明 MCP size limits、copy-on-write、Unicode/BiDi、frontmatter smuggling 与 backslash traversal hardening；源码/tests 与本机构建交叉核验。PR [#34](https://github.com/okf-memory/okf-agent-memory/pull/34) 为进一步跨平台 absolute path hardening，state=open、merged_at=null，说明 tag v0.4.2 不能宣称覆盖该 PR。
- **来源交叉核验**：README、DMAA RFC、SECURITY 与 v0.4.2 release notes、fixed tag 源码、Go manifests、security/crash/sync tests、GitHub API、本机 go test/vet/build/strict validator/search。

#### 架构 / 实现与数据流

```text
session start
  -> Layer 1: compact AGENTS.md / AAG codex (push invariants + memory triggers)
user task / target source path
  -> okf search(query) OR search --for-path(target)
  -> LoadBundle()
      -> parse Markdown + frontmatter
      -> build outbound/inbound graph + broken links + orphans
  -> deterministic BM25-ish lexical rank
      -> title/tags/description/id/body weights
      -> for-path: governance hold > constraint > context
  -> okf show exact concept
  -> agent acts under retrieved constraint/context
candidate write
  -> ValidateConceptID + root/symlink/reserved-path checks
  -> sanitize metadata/frontmatter
  -> atomic concept write
  -> update parent index + append log
  -> strict/drift/stale validation gate
optional sync
  -> client-side Argon2id key + AES-256-GCM envelopes
  -> CAS blobs/tree/commit + expected-head update
  -> 3-way reconcile / explicit conflict-local file
```

它把两类“记忆”拆开：不能依赖检索命中的 behavioral invariant 常驻 push；大量 domain knowledge 以 OKF Markdown graph pull。`code_refs` 把知识条目绑定 source path，`SearchForPath()` 先按 governance rank，再按 lexical relevance/specificity 排序。边界是 AAG 仍是 prompt discipline，不是 host hard authorization；Go tool 的 strict validator也只是知识 bundle gate，不是用户意图或事实真实性证明。

#### repo tree 摘要

固定 commit 共 **206 tracked paths**：

```text
okf-agent-memory/
├── cmd/
│   ├── okf/              # CLI + stdio MCP + tool schemas
│   └── okf-benchmark/    # progressive-disclosure benchmark runner
├── pkg/
│   ├── okf/              # parser/bundle/search/mutate/validator/bootstrap/AAG
│   ├── sync/             # Hub client、CAS push/pull、3-way reconcile
│   └── vault/            # Argon2id、AES-GCM envelope、tree/commit
├── knowledge/            # 项目自身 dogfood：typed concepts/index/log
├── .agents/skills/       # OKF memory skill contract
├── docs/
│   ├── spec/             # DMAA、AAG、OKF compatibility RFC
│   ├── guides/           # CLI/MCP/instruction usage
│   ├── security/         # threat/data-governance/audit
│   └── releases/         # v0.1.0–v0.4.2 release notes
├── benchmarks/           # fixtures 与多模型结果（README claims 需独立复验）
├── examples/             # software/coaching/books bundles
├── go.mod / go.sum       # Go 1.26；x/crypto + x/sys
└── .github/workflows/    # CI + release
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `pkg/okf/bundle.go` | canonical bundle load/graph | root resolution、symlink containment、concept/index/log 分类、broken/orphan graph |
| `pkg/okf/parser.go` | OKF Markdown codec | frontmatter parse、unknown metadata round-trip、safe YAML quoting |
| `pkg/okf/search.go` | lexical retrieval/governance query | bounded query/results、field weights、Unicode tokens、`--for-path` authority rank |
| `pkg/okf/mutate.go` | mutation chokepoint | concept ID/path validation、frontmatter smuggling guard、atomic file write、index/log bookkeeping |
| `pkg/okf/validator.go` | conformance/drift gate | provenance/trust/lifecycle/code_refs/link/orphan/stale checks |
| `pkg/okf/aag/linter.go` | push codex linter | token estimate、ASCII/modal/tool signature/Mermaid assertions |
| `pkg/vault/envelope.go` / `kdf.go` | zero-knowledge client crypto | random nonce AES-256-GCM、version AAD、Argon2id 64MB/3/4 |
| `pkg/sync/reconcile.go` | file manifest 3-way merge | disjoint merge、same-file conflicts、remote primary + local conflict fork |
| `pkg/sync/engine.go` | CAS sync orchestration | missing-only upload、encrypted tree/commit、expected-head retry/reconcile |

#### ⭐ 源码精读

**代码块 1：`Bundle.Search()` 有界解析 query，并按字段加权做确定性 lexical ranking。**

```go
func (b *Bundle) Search(query string, limit int) []SearchResult {
    if len(query) > MaxQueryLength {
        runes := []rune(query)
        if len(runes) > MaxQueryLength { query = string(runes[:MaxQueryLength]) }
    }
    qTokens := tokenize(query)
    if len(qTokens) > 50 { qTokens = qTokens[:50] }
    if limit <= 0 { limit = 10 } else if limit > MaxSearchLimit { limit = MaxSearchLimit }
    // title 4.0, tags 3.5, description 2.5, id 2.0, body capped at 5 occurrences
    ...
    sort.Slice(results, func(i, j int) bool {
        if results[i].Score == results[j].Score { return results[i].ConceptID < results[j].ConceptID }
        return results[i].Score > results[j].Score
    })
}
```

逻辑摘要：无网络/embedding，query 1000、token 50、results 100 上限；stable ConceptID tie-break。字段权重让 concise title/tags/description 比大 body 更重要。边界：实现注释称 BM25/TF-IDF，但代码是自定义 weighted TF×IDF，不含文档长度归一化/k1/b；不能把 README benchmark 外推为标准 BM25 质量。

**代码块 2：`SearchForPath()` 让 source path 先命中 code_refs，再让 hold/constraint/context 决定 authority rank。**

```go
func (b *Bundle) SearchForPath(targetPath, query string, limit int) []SearchResult {
    for _, c := range b.Concepts {
        for _, ref := range c.CodeRefs {
            if matchCodeRef(ref, targetPath) {
                matchedCandidates = append(matchedCandidates, candidate{concept: c, ...})
                break
            }
        }
    }
    for _, cand := range matchedCandidates {
        gov := cand.concept.EffectiveGovernance()
        score := float64(governanceRank(gov) * 10)
        if cand.exactMatch { score += 2.0 }
        if tr, exists := textScores[c.ID]; exists { score += tr.Score }
        ...
    }
}
```

逻辑摘要：模型不必“想起”要用哪些关键字找 subsystem constraint；宿主可按将修改的真实 path 拉出 constraints/holds。本机执行 `search --for-path pkg/okf/types.go knowledge` 返回 `architecture/governance-model [constraint] score 22.00`。边界：`code_refs` 由作者维护，会 stale 或覆盖过宽；drift validator只检查非 glob path existence，不能证明 glob semantics 或 governance内容正确。

**代码块 3：`SaveConcept()` 在写入前做 ID/path/metadata gate，再 atomic replace。**

```go
func SaveConcept(bundleDir string, c *Concept, isNew, autoLog, autoIndex bool, actor string) error {
    if err := ValidateConceptID(c.ID); err != nil { return fmt.Errorf("invalid concept ID: %w", err) }
    fullPath, err := resolveInBundle(bundleDir, c.Path)
    if err != nil { return err }
    c.Generated = &Generated{By: actor, At: time.Now().UTC().Format(time.RFC3339)}
    if err := sanitizeConceptMetadata(c); err != nil { return err }
    raw := SerializeConcept(c)
    if err := atomicWriteFile(fullPath, []byte(raw), 0o644); err != nil { return err }
    if autoIndex { if err := UpdateParentIndex(bundleDir, c); err != nil { return err } }
    if autoLog { if err := AppendLogEntry(bundleDir, entryType, desc); err != nil { return err } }
    return nil
}
```

逻辑摘要：concept ID 拒绝 traversal/absolute/hidden/control/BiDi/reserved/depth>8；`resolveInBundle` 检查 symlink containment 与 `.md` target；metadata 拒绝 newline/frontmatter smuggling；文件本身 temp+Sync+Rename。边界：concept、parent index 与 log 是三个 sequential atomic writes，不是一个事务；`crash_consistency_test.go` 明确证明 concept 可以已存在而 index/log未更新，strict+drift 负责发现而非原子避免。

**代码块 4：`Validate()` 区分 conformance、warnings、gate findings 与 strict gate。**

```go
func Validate(b *Bundle, opts ValidateOptions) *ValidationResult {
    res := &ValidationResult{ConceptCount: len(b.Concepts), BrokenLinks: b.BrokenLinks, Orphans: b.Orphans}
    // validate source IDs, generated/verified actors & time, governance,
    // code_refs boundaries, lifecycle, index description drift and parent listing
    res.IsConformant = len(res.Errors) == 0
    gateFailure := (opts.Strict && (len(b.BrokenLinks) > 0 || len(b.Orphans) > 0)) ||
        (opts.Strict && isV2 && len(res.GateFindings) > 0) ||
        (opts.Stale && res.StaleCount > 0)
    res.GatePassed = res.IsConformant && !gateFailure
    return res
}
```

逻辑摘要：语法/结构 conformance 与 strict governance gate 不混成一个 bool；broken/orphan、legacy field、bad governance 在 strict 时阻断。本机固定 tag strict+drift 为 20 concepts、全 0、conformant。边界：warnings 默认不阻断；事实内容的真实性、人工 verified 的真实身份、source URL freshness 都不由本函数证明。

**代码块 5：remote sync 用 client-side authenticated envelope + CAS/expected head。**

```go
func EncryptPayload(plaintext, key []byte) ([]byte, error) {
    if len(key) != 32 { return nil, ErrInvalidKeyLength }
    block, _ := aes.NewCipher(key)
    gcm, _ := cipher.NewGCM(block)
    nonce := make([]byte, NonceLength)
    io.ReadFull(rand.Reader, nonce)
    sealed := gcm.Seal(nil, nonce, plaintext, []byte{EnvelopeVersionV1})
    return append(append([]byte{EnvelopeVersionV1}, nonce...), sealed...), nil
}

func (e *Engine) Push(ctx context.Context, author vault.CommitAuthor, message string) (*PushResult, error) {
    files, _ := e.ScanBundle()
    // plaintext hash detects local change; encrypted envelope hash is CAS key
    // upload missing blobs -> encrypted tree -> encrypted commit
    resp, err := e.Client.Commit(ctx, e.VaultID, commitBlobHash, expectedHead)
    ...
}
```

逻辑摘要：key 由 password + 128-bit secret salt 经 Argon2id（64MB、3 passes、4 lanes）导出；AES-GCM version byte进入 AAD；remote只见 encrypted blobs/tree/commit 与 hashes，head 用 expected value推进。冲突时 3-way reconcile，不能合并的 local copy另存 `.conflict-local.md`。边界：今日只跑 unit/integration tests，未连接真实 Hub、未审 server/auth/traffic metadata；“zero-knowledge”不代表隐藏 blob sizes、访问时序、vault identity，也不代表 endpoint 可用性。

#### 依赖分析与供应链风险

- `go.mod` 声明 Go 1.26.0；direct dependency `golang.org/x/crypto v0.57.0`，indirect `x/sys v0.48.0`。`go list -m all` 还显示 `x/net v0.58.0`、`x/term v0.46.0`、`x/text v0.42.0` 为 module graph indirect entries。
- 本机构建 binary metadata只嵌入 `x/crypto` 与 `x/sys`；`vcs.revision=9413d...`、`vcs.modified=false`。这比只看 go.mod 更接近实际 artifact，但仍不是可复现构建或签名证明。
- CI 使用 `actions/checkout@v7`、`actions/setup-go@v7` mutable tags，不是 commit SHA pin；release workflow与 Homebrew/asset provenance 未做本机 digest/签名验证。
- v0.4.2 在 09-19 发布，13 releases 在约两周内快速迭代；活跃度高也意味着 schema/CLI/sync contract 仍可能快速变动。
- public advisories API 空、vulnerability-alerts endpoint 404；本次没有独立 `govulncheck` 结果，因此不声明依赖无已知漏洞。

#### 可复用经验

- 当长期规则必须每轮遵守、领域事实只在相关任务需要时，应优先拆分 compact push invariant 与 on-demand pull knowledge，因为把两者都塞 prompt 或都丢进 RAG 会分别导致 context bloat 与 retrieval blindspot；边界是 push 规则仍需 host hard gate 才能约束高权 effect。
- 当修改 source file 前需要找对应约束时，应优先用 `code_refs + governance rank` 做 path-driven retrieval，因为自然语言 query 不一定提到 subsystem 名；边界是 refs 需 drift 检查且真实 target 要 canonicalize。
- 当 canonical Markdown 同时维护 index/log/graph 时，应优先让单文件原子写、post-write strict validator 和可重建 index共同收口，因为跨文件事务缺失时 crash 会留下可发现而非静默的 drift；边界是发现不等于自动安全修复。
- 当远程同步私有知识时，应优先把 encryption、CAS identity、expected-head concurrency 与 conflict preservation分开验证，因为“加密成功”不等于不丢更新，“同步成功”也不等于 server 看不到 metadata。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/path-bound-governance-query-v0/` 做只读 synthetic fixture：3 个 facts 分别绑定 `scripts/**`、`capabilities/skills/**`、`curated/memory/**`，governance 为 context/constraint/hold。输入 candidate target realpath，输出 ordered applicable constraints + broken/stale refs + source revision。覆盖 exact/prefix/glob/backslash/`../`/symlink 与 hold-first；只比较 Hermes 现有 `rg/frontmatter` baseline，不改 AGENTS/prefill/curated。

#### 风险边界

- **License**：GitHub API、根 LICENSE 与 release repo均 MIT；OKF spec引用、Go dependencies、benchmark prompts/models、Homebrew/release assets与远程 Hub terms 需独立审查。
- **维护活跃度**：09-05 创建、09-19 v0.4.2、09-20 pushed；13 个 releases、6 contributor page count。迭代非常快，不能把版本数量等同长期稳定。
- **安全风险**：knowledge 是持久 prompt-injection/data-poisoning surface；AAG/AGENTS 是 prompt层，不是 OS policy。remote sync 涉及 password/secret key/token、server availability 与 conflict writes；PR #34 尚未合并，tag 后跨平台 absolute-path边界仍在加固。
- **一致性风险**：concept → parent index → log 是 sequential writes；crash fixture证明 derived index可 stale。strict validator能发现部分 drift，但不会原子 rollback。
- **隐私风险**：git-native plaintext 在 remote sync 前仍存在本地磁盘/工作树/history；误提交 secret 后需要 history rewrite。AES-GCM sync 不能隐藏所有 metadata，也不能替代 local access control/backup deletion。
- **局限性**：自定义 lexical scorer不是标准 BM25；token estimator 只是 max(chars/4, words×1.2)；AAG ASCII-only/Mermaid断言带项目偏好，不是通用 memory 标准；`verified.by` 只是格式校验，不验证签名/真实 human identity。
- **验证局限**：未复现 README `<300µs`、4ms、78–85% token、模型 compliance benchmark；未连接 Hub/MCP client/真实多 Agent；未执行 release asset checksum 或 `govulncheck`。

#### ⭐ Skill 升格判断

**需二次验证。** DMAA 的“push invariant + pull facts”、path-bound governance query、strict drift gate 可直接进入 POC；但不复制 AAG syntax/Skill、不替换 shared hub 目录，不把 README benchmark 当事实。需与现有 `shared-memory-bridge`、path-portability、config-target-routing 与 governance去重后再决定更新哪个 shared skill。

#### ⭐ Hermes / shared hub 落地路径

1. push 层：保留 `AGENTS.md`/prefill 中最小、跨任务必须遵守的不变量，不把 daily/facts 全部展开进系统 prompt。
2. pull 层：`curated/memory/` 仍为稳定 truth；为 facts/projects增加可选 `applies_to`（相对 glob）候选 schema，先在 runtime parser POC，不改现有 frontmatter。
3. query：新增只读 `scripts/query_applicable_context.py` 候选，输入 resolved shared-relative target，输出 `hold/constraint/context + evidence path + revision`；错误/越界 fail closed。
4. gate：扩展现有 governance checker，检查 broken refs、orphan、stale/review_due、index drift；只输出风险与候选，不自动修改 curated。
5. projection：Obsidian/README/prefill从 canonical facts生成，不从 prose反向写 truth；所有 derived view带 source revision/coverage。
6. 如 POC与真实任务回放证明收益，优先更新现有 shared-memory/governance/path skill；不自动部署 OKF MCP/Hub，不改 Hermes/OpenClaw provider、auth、cron或 secret。

## 经验沉淀

1. 当长期规则必须无条件常驻、事实只在相关任务需要时，应优先采用“compact push invariants + on-demand pull knowledge”，因为全塞 prompt会膨胀、全靠 RAG会漏 operational rules；边界是高权 effect 仍要 deterministic host gate。
2. 当模型参与长期记忆写入时，应优先把它限制为 candidate operation，并由宿主提供 existing handles、source pointer、target layer 与 path scope，因为自由 update identity 会放大 poisoning 和误覆盖；边界是 semantic duplicate 仍需独立 checker。
3. 当 raw、curated、index、prefill、Obsidian 与 archive 共存时，应优先声明每层 truth/projection/retention/delete coverage，并让 projection可重建，因为“文件存在”不能证明层间一致；边界是外部 backup/history需单独删除证明。
4. 当 path 被用于 import、scope、governance 或写入时，应优先 canonicalize 后做 root containment、component matching、symlink/reserved-path检查，因为字符串 prefix与 `root / relative` 都不是安全边界；边界是 TOCTOU仍需最终 effect点重验。
5. 当多进程写同一 memory/ledger/index 时，应优先让所有 truth mutation共用 resource-scoped lock、staging/atomic replace与 post-write validation，因为部分有锁会让未覆盖入口成为一致性缺口；边界是单文件原子不等于跨文件事务。
6. 当 GitHub issue/PR声称修复安全问题时，应优先核 state、merged_at、base branch、fixed commit与本机 reproducer，因为 open PR代码不属于 default branch；边界是 merged也需确认release/artifact包含该 commit。
7. 当 README给出 latency、accuracy、token saving或“zero knowledge”时，应优先区分源码机制、本机可复现实验与未核验宣称，因为 architecture plausibility 不能替代 benchmark/threat-model证据。

## 明日继续

1. 实现合并 POC `memory-promotion-and-path-governance-v0`：candidate handles + raw pointer + path containment + component scope + applicable constraints，仅 synthetic fixtures。
2. 给 shared governance候选 schema草拟 `applies_to / governance / source_revision / review_due`，先做 parser/validator differential，不改 curated active facts。
3. 对 agent-memory PR #15/#36/#38 与 OKF PR #34追踪 merge；只有进入目标 branch/tag 后才固定新 commit复验对应 adversarial tests。
4. 为两类系统定义统一 memory completion receipt：`truth_written / projection_updated / validated / source_pointer_recoverable / deletion_coverage`，避免单一 success。

## 候选反哺

### Candidate Facts

- [ ] topic: 长期记忆应分 push invariant 与 pull knowledge | evidence: OKF DMAA RFC + 本机 `search --for-path`；agent-memory MEMORY.md injection/recall split | 建议: update shared-memory architecture candidate | 安全级别: medium
- [ ] topic: model memory write 应使用 finite handles 与 evidence pointers | evidence: agent-memory `reconcile.py::check/to_record_spec` + targeted tests 43 pass | 建议: create candidate, not active fact | 安全级别: medium
- [ ] topic: file-first 不自动等于安全可迁移 | evidence: agent-memory main import escape + scope prefix本机复现；OKF crash consistency fixture | 建议: update path-portability/governance candidate | 安全级别: high
- [ ] topic: path-bound governance 可降低语义检索 blindspot | evidence: OKF `SearchForPath` + 本机 `pkg/okf/types.go` constraint output | 建议: POC then review | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: memory-promotion-gate（更新现有 shared-memory/governance workflow） | 可复用场景: inbox→curated、Agent候选写入、facts更新/替换 | 是否建议 shared: yes（仅候选） | 原因: Hermes/future-agent横切，但需先完成 path/concurrency/provenance fixtures并去重
- [ ] 名称: path-bound-context-query（优先做 deterministic script，不新建大 skill） | 可复用场景: 修改 script/skill/fact 前拉取适用约束 | 是否建议 shared: yes（仅候选） | 原因: 可减少规则漏检，但 frontmatter schema与 glob semantics需二次验证

### Candidate Open Questions

- [ ] 问题: shared hub 如何定义跨 curated/inbox/runtime/prefill/Obsidian 的 deletion coverage 与 supersede chain？ | reason: adaptation | priority: high
- [ ] 问题: promotion gate 的 existing handles 应来自 lexical recall、exact key、path scope还是多源 union，如何保证 denominator不被模型漏掉？ | reason: gap | priority: high
- [ ] 问题: path-bound governance 的 hold/constraint/context 是否适用于非代码 facts，如何避免过宽 glob造成误阻断？ | reason: adaptation | priority: medium
- [ ] 问题: agent-memory open安全 PR 与 OKF PR #34 何时进入 release，release artifact如何做 source revision/digest closure？ | reason: stale/gap | priority: medium

### 不应自动落地

- 不自动安装或接管 agent-memory/OKF runtime，不启动 MCP/Hub/endpoint，不读取或写入任何真实 token/password/secret key。
- 不自动改 Hermes/OpenClaw config、provider、cron、auth或 skills；当前 OpenClaw runtime不存在且本次未调用。
- 不直接写 curated active fact、不创建新 shared skill；本报告、project cards、lessons均是 raw/candidate，需要二轮评分、证据、去重、脱敏和审查。
- 不导入不可信 agent-memory export；fixed main的越界写已真实复现。也不把 scope参数当 ACL。
- 不把 GitHub CI、本机定向 tests、公开 advisory空、strict validator绿色、Stars或README benchmark外推为完整安全、可靠、跨平台或生产成熟证明。
