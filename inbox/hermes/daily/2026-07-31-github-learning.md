# 2026-07-31 GitHub 热门项目学习日报

> 执行器：Hermes（本次未调用 OpenClaw）  
> GitHub Trending HTML 抓取时间：2026-07-30T23:30:50Z（北京时间 2026-07-31T07:30:50+08:00）  
> GitHub Repository API 核验时间：2026-07-30T23:31:38Z（北京时间 2026-07-31T07:31:38+08:00）  
> 固定源码快照：`mvanhorn/last30days-skill@57f8d2c87a8d5463f58307168ac1070f104daa77`、`agavra/tuicr@567528413e2600c69579f8ec37330b1c0933cf52`  
> 发现口径：真实抓取 `https://github.com/trending?since=daily`，得到 14 个仓库；随后对 10 个候选逐仓库执行 `gh api repos/{owner}/{repo}`。Stars、forks、updated/pushed 会变化，本文数字只代表上述查询时点。

## 今日结论

今天的主线是：**把 Agent 的模糊研究或人工反馈变成可组合工作流时，应将“意图/计划、来源执行结果、canonical state、投影输出和副作用”分层；空结果不能吞掉 transport failure，界面或 Markdown 也不应成为唯一真相源。** `last30days-skill` 展示了 plan → 并发多源检索 → 归一化 → weighted RRF → rerank → cluster → versioned report，并用 `SourceOutcome` 保留真实失败；`tuicr` 则用统一 `ReviewSession/ReviewStore` 同时服务 TUI、人类、CLI 与 Agent，再在提交前把 comments 映射为 forge-specific effect。对 Hermes/shared hub 最值得反哺的是 **source-outcome-aware research contract** 与 **human-review canonical session adapter**，不是直接安装两个完整产品。

## 证据与执行摘要

- **Trending 发现**：真实保存 GitHub Trending daily HTML 到 `runtime/hermes/github-hot-project-learning/trending-2026-07-31.html`，解析到 14 个仓库，包括 `mvanhorn/last30days-skill`、`agavra/tuicr`、`different-ai/openwork` 等。
- **API 元数据**：10 个候选的 Repository API 原始 JSON 保存在 `runtime/hermes/github-hot-project-learning/api/2026-07-31/`。API 查询时 core rate limit 为 5,000，使用后剩余 4,992。
- **源码**：对两个深读项目执行 `git clone --depth 1`；tracked paths 分别为 **436** 与 **171**，工作树干净。
- **来源交叉**：两个项目均读取 README、docs、latest release、open issue、依赖清单和关键源码；结论没有只复述 README。
- **last30days 真实测试**：在源码快照中以 `uv run pytest` 执行完整 suite，真实结果为 **3,576 passed / 7 skipped / 48 subtests passed / 1 failed**，耗时 260.98 秒。唯一失败为 `test_unwritable_target_returns_false`：cron 以 root 执行，root 可在 mode `0500` 目录下创建子目录，导致测试期望 `False`、实际 `True`。这说明完整 suite 在本环境**未通过**；非 root 是否通过未成功复现，标记待核验。
- **tuicr 真实测试**：尝试 `cargo test --lib`，环境真实返回 `cargo: command not found`（exit 127）；因此编译、测试、TUI 与 forge 行为均标记**待核验**，不把上游源码中的 tests 当成本机通过。
- **运行时证据边界**：浅克隆、API JSON、HTML 与 test log 都位于 `runtime/hermes/`，不进入 curated；本报告位于 Hermes inbox。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | Created / Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 236,194 | 35,926 | JavaScript | MIT | 2026-01-18 / 2026-07-30T23:30:39 / 2026-07-29T18:11:01 | 高热度 Agent 资源，今日不重复做产品清单式深读 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | **55,522** | 4,786 | Python | **MIT** | 2026-01-23 / 2026-07-30T23:30:13 / 2026-07-30T19:17:51 | **深读：多源 research contract 与 honest source outcomes** |
| [microsoft/AI-For-Beginners](https://github.com/microsoft/AI-For-Beginners) | 53,855 | 10,943 | Jupyter Notebook | MIT | 2021-03-03 / 2026-07-30T23:31:32 / 2026-07-21T11:11:48 | 教程型项目，留给教程学习 lane |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 48,026 | 3,258 | TypeScript | Apache-2.0 | 2025-09-11 / 2026-07-30T23:29:57 / 2026-07-30T19:41:47 | 高权 browser/MCP 候选，需单独授权与安全研究 |
| [pascalorg/editor](https://github.com/pascalorg/editor) | 20,092 | 2,620 | TypeScript | MIT | 2025-10-16 / 2026-07-30T23:26:47 / 2026-07-30T10:44:33 | AI 文档编辑器，当前与 shared hub 主线较远 |
| [different-ai/openwork](https://github.com/different-ai/openwork) | 18,687 | 1,904 | TypeScript | **NOASSERTION** | 2026-01-14 / 2026-07-30T23:30:20 / 2026-07-30T19:30:46 | 活跃但 repo-level license 无法断言；只观察，不迁移源码 |
| [paperswithbacktest/awesome-systematic-trading](https://github.com/paperswithbacktest/awesome-systematic-trading) | 11,007 | 1,411 | Python | **null** | 2022-02-05 / 2026-07-30T23:27:36 / **2025-01-22T07:49:32** | awesome 列表且 pushed 已久，不做深读 |
| [WhiskeySockets/Baileys](https://github.com/WhiskeySockets/Baileys) | 10,428 | 3,251 | JavaScript | MIT | 2022-01-12 / 2026-07-30T23:29:53 / 2026-07-29T12:53:12 | WhatsApp 高风险集成面，非今日学习目标 |
| [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech) | 8,738 | 1,086 | Python | Apache-2.0 | 2024-08-07 / 2026-07-30T23:30:54 / 2026-07-30T16:41:20 | 实时语音链路候选，需 GPU/模型 license 专项核验 |
| [agavra/tuicr](https://github.com/agavra/tuicr) | **1,837** | 157 | Rust | **MIT** | 2026-01-08 / 2026-07-30T23:27:16 / 2026-07-30T04:49:45 | **深读：human review canonical session 与 forge effect adapter** |

说明：Stars 不是安全、质量、采用率或项目真实性证明；GitHub API 的 repo-level License 也不能覆盖依赖、模型、数据、vendored code、商标与发布制品。

## 深读项目

### 1. mvanhorn/last30days-skill

**基本信息（GitHub Repository API）**

- URL：https://github.com/mvanhorn/last30days-skill
- Stars：**55,522**；Forks：**4,786**；Language：Python；License：**MIT**。
- 创建：2026-01-23T20:37:37Z；updated：2026-07-30T23:30:13Z；pushed：2026-07-30T19:17:51Z。
- API 查询时 `open_issues_count=77`，该字段可能包含 PR，不能解释成 77 个缺陷；subscribers 为 204。
- 固定 commit：[57f8d2c87a8](https://github.com/mvanhorn/last30days-skill/commit/57f8d2c87a8d5463f58307168ac1070f104daa77)，commit 时间 2026-07-30T19:17:50Z，message 为 `fix(reddit): report keyless 429/403 as transport failures, not no-results (#900)`。
- latest GitHub Release 为 [v3.18.4](https://github.com/mvanhorn/last30days-skill/releases/tag/v3.18.4)，发布于 2026-07-28T20:56:59Z；固定 commit 比该 release 更新，本文源码结论对应 commit，不等同于 release binary/package 行为。

#### 一句话判断

值得学的不是“抓更多网站”，而是它把 **agent-facing Skill contract、deterministic engine、plan、source adapters、observed SourceOutcome、融合/重排、versioned export 与 host adapters**分离；尤其适合校正 Hermes 每日调研中“某来源失败却被写成无结果”的问题。

#### 解决的问题：替代了什么旧做法

它替代五类脆弱做法：

1. Agent 临时拼 `curl` 并从不同来源直接堆结果，没有统一 schema、date window 或 provenance。
2. 用一个关键词搜所有来源，忽略来源能力、intent、subquery weight 与每源 fetch budget。
3. 将 HTTP 403/429、auth failure、timeout 或 schema drift 吞成空列表，最后写“没有相关内容”。
4. 让 LLM 直接给全局排序，而没有 deterministic normalization、dedupe、RRF 与 fallback entity grounding。
5. 把 Markdown 当唯一产物；跨 host、MCP、cron、library feed 与后续 Agent 只能重新解析 prose。

边界是：更复杂的 pipeline 也会带来更大攻击面、配置面和维护成本；“来源多”不自动等于可信，engagement 也不是事实正确性。

#### 架构 / 实现与数据流

```text
User / host harness
        │
        ▼
SKILL.md agent-facing contract
        │ intent translated to explicit flags / external plan
        ▼
last30days.py CLI / host adapter / MCP tool
        │
        ▼
pipeline.run
  ├─ date window + available source gate
  ├─ planner.plan_query / validate_external_plan
  ├─ ThreadPoolExecutor → source adapters
  ├─ normalize + date filter + signal score + dedupe
  ├─ RetrievalBundle + SourceOutcome
  ├─ weighted RRF + per-author/source diversification
  ├─ deterministic/remote rerank + clustering
  └─ Report(schema) + warnings + artifacts
        │
        ├─ Markdown/compact/HTML projection
        ├─ versioned agent JSON
        ├─ local library/store/watchlist
        └─ MCP/host-specific surface
```

核心分工是：Skill 告诉 host model 怎样调用；Engine 负责可执行机制；Harness 负责加载和工具权限。`CONCEPTS.md` 明确 Skill 是分发单元，Engine 是实现，Harness 是运行宿主。这个区分与 shared hub 的 class-level skill / runtime artifact 分层相容。

#### Repo tree 摘要

```text
last30days-skill/                         # 固定 commit tracked paths: 436
├── README.md / README.zh-CN.md           # 产品、安装、来源、用户工作流
├── AGENTS.md / CONCEPTS.md               # 贡献规则与精确定义的领域词汇
├── CONFIGURATION.md / HERMES_SETUP.md    # 配置矩阵与 Hermes 安装说明
├── pyproject.toml / uv.lock              # Python 3.12、dev/test lock
├── skills/last30days/
│   ├── SKILL.md                           # agent-facing canonical contract
│   ├── scripts/last30days.py              # CLI composition root
│   ├── scripts/lib/                       # 87 个 Python source/planner/fusion/render 模块
│   ├── scripts/lib/vendor/bird-search/    # vendored Node X search subset
│   └── references/ / assets/ / agents/    # host references、媒体、metadata
├── mcp/
│   ├── cmd/last30days-pp-mcp/             # Go MCP entry
│   └── internal/{engine,tools,manifest}/  # embedded engine 与 tool bridge
├── tests/                                 # 187 个 Python test files（git path 口径）
├── docs/                                  # 架构、eval、release、故障经验
├── fixtures/                              # source/eval replay fixtures
├── hooks/                                 # host setup/config hook
├── changelog.d/                           # towncrier change/security fragments
└── .github/workflows/                     # validate/release/CodeQL/OSV/Scorecard
```

`SKILL.md` 在固定 commit 为 **2,255 行 / 222,241 bytes**。这同时是完整 contract 的证据与上下文税风险；open issue #910 也把其称为 multi-host compliance risk，而不是可无限增长的优点。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `skills/last30days/scripts/lib/pipeline.py` | 研究 composition root | source gating、planner、并发 fetch、retry、SourceOutcome、RRF/rerank/cluster/report |
| `skills/last30days/scripts/lib/schema.py` | canonical in-memory/export model | `SourceItem`、`Candidate`、`SourceOutcome`、`RetrievalBundle`、`Report` 与 versioned exports |
| `skills/last30days/scripts/lib/planner.py` | intent → query/source plan | external plan validation、LLM/deterministic fallback、source/subquery weights |
| `skills/last30days/scripts/lib/fusion.py` | global candidate fusion | URL canonicalization、weighted RRF、同源/作者上限与 source diversity |
| `skills/last30days/scripts/lib/rerank.py` | final scoring | provider rerank 与 deterministic fallback、entity grounding、engagement/freshness |
| `skills/last30days/scripts/lib/render.py` | report projection | source outcomes/coverage、compact/Markdown sections 与 URL safety |
| `skills/last30days/scripts/lib/discovery_handoff.py` | multi-leg discovery checkpoint | bundle id、TTL、mock/real provenance、resume handoff |
| `skills/last30days/scripts/lib/setup_wizard.py` | local setup + secret file write | consent后的工具/配置动作、0600 env append；本机 suite 唯一失败发生于其权限测试 |
| `docs/how-search-works.md` | architecture docs | 并行检索、normalize/filter/score/dedupe 与 error handling 说明 |
| `changelog.d/899.fixed.md` | failure truth evidence | Reddit 429/403 不再伪装 `no-results`，严格模式可 exit 3 |
| `changelog.d/+sessionstart-env-rce.security.md` | security fix evidence | 拒绝非 identifier `.env` keys，project config 改为显式 trust |

#### 源码精读（固定 commit）

**代码块 1：observed source result 是一等结构，而不是日志字符串**  
来源：`skills/last30days/scripts/lib/schema.py:179-213`

```python
@dataclass
class SourceOutcome:
    source: str
    state: RunOutcomeState
    items_returned: int = 0
    attempted: bool = True
    detail: str | None = None
    at: str = field(default_factory=_utc_now)
    fix_hint: str | None = None

    def __post_init__(self) -> None:
        valid_states = {
            health.OK, health.TIMEOUT, health.ERROR, NO_RESULTS, PARTIAL,
            RATE_LIMITED, AUTH_FAILED, UNREACHABLE, SCHEMA_DRIFT,
            SKIPPED_UNCONFIGURED,
        }
        if self.state not in valid_states:
            raise ValueError(f"Unknown source outcome state: {self.state}")
        if self.items_returned < 0:
            raise ValueError("items_returned cannot be negative")
```

逻辑：configured/attempted/result count/failure class 被写进 report schema；`no-results` 与 `rate-limited`、`auth-failed`、`partial` 不是同义词。对 Hermes 的迁移点是每个 evidence lane 都要产出 observed receipt，最终摘要不能只看 items。边界是 dataclass validation 只验证枚举和非负计数，不能证明 adapter 正确分类，也不证明来源内容真实。

**代码块 2：并发 source fetch 的失败被保留，partial 不会被清洗成 clean**  
来源：`skills/last30days/scripts/lib/pipeline.py:2257-2320`

```python
for future in as_completed(futures):
    subquery, source = futures[future]
    try:
        raw_items, artifact = future.result()
    except Exception as exc:
        if _is_rate_limit_error(exc):
            with rate_limit_lock:
                rate_limited_sources.add(source)
            bundle.errors_by_source[source] = str(exc)
            state, attempted = _classify_source_failure(exc)
            bundle.record_failure(source, state, str(exc), attempted=attempted)
            continue
        if _is_transient_error(exc):
            time.sleep(3)
            # retry once; second failure is recorded with both errors
        else:
            bundle.errors_by_source[source] = str(exc)
            state, attempted = _classify_source_failure(exc)
            bundle.record_failure(source, state, str(exc), attempted=attempted)
            continue
    normalized = _normalize_score_dedupe(
        source, raw_items, from_date, to_date,
        freshness_mode=plan.freshness_mode,
        ranking_query=subquery.ranking_query,
    )
    bundle.add_items(subquery.label, source, normalized)
```

逻辑：rate limit 会给 pending workers 提供共享信号，transient error 只重试一次；成功返回的数据仍进入统一 normalize path。后续代码把“部分 subquery 失败但已有 items”的 source 标记 degraded/partial，而不是删除错误。边界是线程池没有让来源变可信；sleep retry、source-specific cap 与第三方 WAF 仍可能造成 coverage 偏差。

**代码块 3：weighted RRF 只融合 rank/evidence，不让某个来源或作者垄断 pool**  
来源：`skills/last30days/scripts/lib/fusion.py:110-159,162-207`

```python
def weighted_rrf(
    streams: dict[tuple[str, str], list[schema.SourceItem]],
    plan: schema.QueryPlan,
    *,
    pool_limit: int,
) -> list[schema.Candidate]:
    subqueries = {subquery.label: subquery for subquery in plan.subqueries}
    candidates: dict[str, schema.Candidate] = {}
    for (label, source), items in streams.items():
        subquery = subqueries[label]
        weight = subquery.weight * plan.source_weights.get(source, 1.0)
        for rank, item in enumerate(items, start=1):
            key = candidate_key(item)
            score = weight / (RRF_K + rank)
            if key not in candidates:
                candidates[key] = schema.Candidate(
                    candidate_id=key,
                    item_id=item.item_id,
                    source=item.source,
                    title=item.title,
                    url=item.url,
                    rrf_score=score,
                    sources=[item.source],
                    source_items=[item],
                )
                continue
            candidates[key].rrf_score += score
            # merge provenance, sources, ranks and best primary representation
    fused = sorted(candidates.values(), key=_candidate_sort_key)
    fused = _apply_per_author_cap(fused)
    return _diversify_pool(fused, pool_limit)
```

逻辑：同 URL/identity 的 evidence 从多个 `(subquery, source)` stream 累积分数和 provenance；之后执行作者上限与 source diversity。它避免直接比较不同平台不可比的绝对 score。边界是 source/subquery weights 仍是 policy；RRF 只说“多个 ranked lists 同意”，不证明事实正确，也可能把同一原始消息的转载误当跨源 corroboration。

**代码块 4：private corpus 不进入 remote reranker**  
来源：`skills/last30days/scripts/lib/pipeline.py:2401-2437`

```python
private_candidates = [
    candidate
    for candidate in candidates
    if candidate.source == "corpus"
    or any(item.source == "corpus" for item in candidate.source_items)
]
public_candidates = [
    candidate for candidate in candidates
    if id(candidate) not in {id(c) for c in private_candidates}
]
ranked_public = rerank.rerank_candidates(
    topic=topic, plan=plan, candidates=public_candidates,
    provider=None if mock else reasoning_provider,
    model=None if mock else runtime.rerank_model,
    shortlist_size=settings["rerank_limit"],
)
ranked_private = rerank.rerank_candidates(
    topic=topic, plan=plan, candidates=private_candidates,
    provider=None, model=None,
    shortlist_size=settings["rerank_limit"],
)
```

逻辑：任何带 corpus evidence 的 candidate 强制走 deterministic fallback，避免私有标题/摘要进入 hosted reasoning prompt。对 shared hub 的启示是 privacy label 必须随 candidate 合并传播，不能只看 primary source。边界是代码注释承诺只覆盖该 rerank path；其他输出、HTML publish、logs、adapter 和 config 仍需逐出口验证。

#### 依赖分析与供应链风险

- root `pyproject.toml` 要求 Python `>=3.12`，**runtime dependencies 为空**；dev group 为 pytest、pytest-cov、PyYAML、towncrier，`uv.lock` 存在。
- 空 Python dependency list 不代表无依赖：source adapters 会使用系统/外部工具、网络 API、browser cookies 与 optional CLIs；README 列出 yt-dlp、Node 和 ScrapeCreators 等路径。
- `mcp/go.mod` 要求 Go 1.25.5，直接依赖 `github.com/mark3labs/mcp-go v0.56.0`，另有 JSON Schema、UUID、cast、URI template 与 `x/text` 间接依赖。
- vendored `bird-search` package 自报版本 0.8.0、Node `>=22`、MIT，并标注基于 `@steipete/bird`；vendored code 必须保留 attribution，不能只看 root MIT。
- `.github/workflows/` 包含 CodeQL、OSV Scanner、Scorecard、dependency review 与 attestation；这是维护者的安全投入证据，不证明当前 commit/每个 release/用户环境无漏洞。
- GitHub repository security advisories API 查询没有返回公开 advisory；这只说明查询时列表为空，不能解释成“没有安全问题”。仓库自己的 security changelog 已记录 URL rendering 与 `.env` hook 问题。
- `SKILL.md` 约 222 KB，engine 87 个 Python lib 模块，且跨 Python/Node/Go/MCP/API/browser/host：供应链和权限面远大于 `dependencies=[]` 给人的第一印象。

#### README / release / issue 交叉核验

- README 声明 current v3 pipeline 的 source of truth 是 `skills/last30days/SKILL.md`，与 repo tree 一致。
- latest release v3.18.4 包含 YouTube comparison timeout 与 CI dependency fixes；固定 commit 又加入 Reddit 429/403 outcome 修复。
- issue [#910](https://github.com/mvanhorn/last30days-skill/issues/910)（open）报告 Grok host path 仍是 Claude-first：2,255 行 Skill contract、host detection、hook variables 与 tool names 存在跨 host gap。
- issue [#909](https://github.com/mvanhorn/last30days-skill/issues/909)（open）报告 Truth Social 默认 User-Agent 被 Cloudflare 403；它证明 source adapter 的“无结果”必须携带 transport classification，而不是静默成功。
- `changelog.d/899.fixed.md` 明确 Reddit 403/429 已从 clean `no-results` 改为 `rate-limited/auth-failed`，并让 strict exit 返回 3；这与固定 commit message 和源码 `SourceOutcome` 相互印证。

#### 真实测试结果

```text
uv run pytest

1 failed, 3576 passed, 7 skipped, 48 subtests passed in 260.98s (0:04:20)
FAILED tests/test_setup_wizard.py::TestWriteApiKey::test_unwritable_target_returns_false
assert True is False
```

失败 fixture 在 mode `0500` 的目录下调用 `write_api_key(ro_dir / "sub" / ".env", ...)`，预期捕获 `OSError` 返回 false；本 cron 为 root，root 实际成功创建目录并写文件。定向重跑仍失败。尝试以非 root 复现时被 WSL 路径/解释器 execute permission 阻塞，没有得到有效测试结果。因此：

- 不能宣称 suite 通过；准确结论是 **3,576 pass + 1 environment-sensitive failure**。
- 该失败不证明生产 secret write 已安全，也不证明业务 pipeline 错误；测试若要跨 root CI，应显式 mock `mkdir/os.open` 的 permission error，或在 test precondition 中 skip root，并另保留真实 non-root integration lane。
- 本次没有调用真实研究 provider、browser cookies、付费 API、MCP server、HTML publish 或 watchlist webhook。

#### 可复用经验

- 当研究流程包含多个外部来源时，应优先为每个来源保存 `attempted/state/items/detail/fix_hint` 的 observed receipt，因为 403、429、timeout 和 0 items 有完全不同的语义；边界是 adapter classification 仍需 fixture 和 postmortem 校验。
- 当多个来源的原生分数不可直接比较时，应优先先做 per-stream ranking，再以 weighted RRF 和 provenance 融合，因为平台 engagement 单位不同；边界是 weights 不是事实真值，转载也不等于独立 corroboration。
- 当私有 corpus 与公开 web evidence 在同一 pipeline 合并时，应优先让 privacy label 随 candidate 传播，并把 hosted reranker 放在显式出口 gate 之后；边界是还要审计 render、publish、log 和 adapter 的所有出站路径。
- 当 Skill 要跨多个 agent harness 分发时，应优先保持 Skill contract、engine 和 harness adapter 分离，并对每个 host 做 contract fixtures；边界是单个 222 KB SKILL.md 已形成上下文与行为漂移风险。
- 当测试依赖 Unix mode bits 时，应优先显式覆盖 root/non-root 语义或 mock syscall error，因为 root 的 DAC bypass 会让“不可写目录”fixture失真；边界是 mock 不能替代至少一条真实 non-root integration test。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/source-outcome-contract/` 建纯离线 POC（今日只设计，不改生产 orchestrator）：

1. 定义 `SourceOutcome = {source, attempted, state, items, detail, evidence_paths, checked_at}`。
2. 用 synthetic adapters 覆盖 `ok-with-items`、`ok-no-results`、`rate-limited`、`auth-failed`、`timeout`、`partial`、`schema-drift`。
3. 让 summary gate 拒绝把 degraded/blocked source 写成“没有内容”，并输出 coverage matrix。
4. 用两个 ranked fixture 验证 deterministic RRF、duplicate URL、same-origin repost 与 source diversity。
5. 不连接真实 provider/API/browser，不读取 secret，不改 Hermes config/cron。

#### 风险边界

- **License**：root 为 MIT；vendored Bird、Go modules、optional CLIs、API terms、平台内容、cookies 与生成报告各有独立义务。不要整仓复制进 shared skill。
- **维护活跃度**：固定 commit/updated 距查询不足 5 小时，活跃；但仓库创建约 6 个月、open items 77（含 PR），变更快且 multi-host contract 尚有 open gap。
- **安全风险**：Skill 涉及 API keys、browser cookies、subprocess、network、HTML publish、webhook、MCP 与大量外部内容；prompt injection、credential leakage、stored XSS、WAF/ToS 变化和 malicious source 都是现实边界。
- **来源质量**：engagement 可被操纵；social consensus 不是事实；同一新闻的跨平台转载不是独立证据；Polymarket odds 也不是确定事实。
- **运行局限**：本机 suite 1 fail；未运行真实 provider/cookie/API/MCP/publish；issue #909/#910 仍 open；非 root permission fixture 待核验。
- **适用边界**：shared hub 已有 GitHub learning skill 与治理流程，不需要复制一个通用 social research 产品才能获得 source-outcome 模式。
- **不可自动执行**：不安装 last30days 到 Hermes，不运行 setup wizard，不读取 cookies/keychain/.env，不调用付费来源，不发布 HTML/webhook，不修改 provider/tools/auth/env/cron。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`SourceOutcome + RetrievalBundle + coverage-aware summary`；它能直接补强 Hermes 的 GitHub/教程/巡检研究 receipts。
- **需验证**：在历史日报与 synthetic failure fixtures 上证明 `403/429/timeout != no-results`；再与现有 `research/github-hot-project-learning`、verification-first 和 orchestrator protocol 去重。
- **暂不沉淀**：完整 `last30days` product skill、222 KB contract、source scrapers、cookie/setup/provider logic；权限与供应链面太大，且本机 suite 未全绿。
- **今日动作**：只提 candidate，不写 curated active fact，不安装本地 skill，不更新 shared manifest。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/source-outcome-contract/{schema.json,fixtures/,validate.py,test_outcomes.py,README.md}`。
2. **GitHub 学习 workflow 候选**：为 Trending、Repository API、README/docs/issues/source/tests 各写 outcome；`audit_score` 之外增加 `coverage_status`，禁止“README blocked”被总结成“项目没有文档”。
3. **共享 skill 候选更新**：验证后优先更新 `capabilities/skills/research/github-hot-project-learning/SKILL.md` 的 source receipts 与 degraded wording，不创建重复的“last30days”产品型 skill。
4. **orchestrator 候选接口**：`finalize_research(outcomes, expected_sources) -> completed|degraded|blocked|failed`；completed 仍要求 report artifact、audit threshold 与 knowledge projection。
5. **shared 分层**：raw API/stdout/test log 留 runtime；完整日报留 `inbox/hermes/daily/`；通过治理评分、证据、去重、脱敏与人工/总控审查后才更新 curated。
6. **跨 Agent 复用**：future-agent/OpenClaw 只消费 versioned schema、state semantics 与 fixtures；当前任务未调用 OpenClaw，也不修改任何 agent 本地配置。

---

### 2. agavra/tuicr

**基本信息（GitHub Repository API）**

- URL：https://github.com/agavra/tuicr
- Stars：**1,837**；Forks：**157**；Language：Rust；License：**MIT**。
- 创建：2026-01-08T04:55:34Z；updated：2026-07-30T23:27:16Z；pushed：2026-07-30T04:49:45Z。
- API 查询时 `open_issues_count=90`，可能包含 PR；subscribers 为 11。
- 固定 commit：[567528413e26](https://github.com/agavra/tuicr/commit/567528413e2600c69579f8ec37330b1c0933cf52)，commit 时间 2026-07-30T04:49:45Z，message 为 `fix(jj): remove ANSI escape sequences by disabling revision ids coloring (#510)`。
- latest GitHub Release 为 [v0.19.1](https://github.com/agavra/tuicr/releases/tag/v0.19.1)，发布于 2026-07-13T22:53:08Z；固定 commit 比 release 新。

#### 一句话判断

值得学的不是 TUI 皮肤，而是它把**人类交互界面、Agent CLI、Rust library、持久化 review session 与 GitHub/GitLab submission adapter**统一到同一 canonical review model；这能避免 Hermes 从 clipboard/Markdown 反向猜测用户反馈。

#### 解决的问题：替代了什么旧做法

它替代以下做法：

1. 人类在 terminal 看 diff，却必须回 GitHub 网页逐行评论。
2. Agent 只能读取用户粘贴的一段 Markdown，无法查询 active review、稳定 comment ID、line side 与 lifecycle state。
3. TUI、CLI 与 library 各自实现 comment mutation，导致验证与持久化语义漂移。
4. 直接把本地 line number 发到 forge，而不验证该行仍在 diff、属于 old/new side、binary/too-large 或 mixed-side range。
5. 并发的 TUI/Agent write 用 read-modify-write 覆盖彼此，没有锁、atomic replace、manifest identity 与 active session signal。

边界是：active session 仍依赖 PID、path、12 小时 freshness；same-user filesystem 不是多租户隔离；最终提交会产生真实 GitHub/GitLab 副作用，必须由用户明确触发。

#### 架构 / 实现与数据流

```text
Git / jj / hg checkout     GitHub PR / GitLab MR
          │                         │
          └──── VcsBackend / ForgeBackend ────┐
                                               ▼
                                     parsed DiffFile/Hunk/Line
                                               │
                        ┌──────────────────────┴─────────────────────┐
                        ▼                                            ▼
                  TUI App/Input/UI                          review CLI / Rust API
                        │                                            │
                        └──── add_comment_to_session ────────────────┘
                                               │
                                               ▼
                                  ReviewSession + ReviewStore
                                               │
                            lock + atomic JSON + manifest + active map
                                               │
                          ┌────────────────────┴────────────────────┐
                          ▼                                         ▼
                 Markdown/stdout projection                 submit preflight/map
                                                                    │
                                                Inline | Unmappable → resolver/body
                                                                    │ confirm
                                                                    ▼
                                                         gh/glab side effect
```

关键模式是 UI 与 Agent 不交换无结构 prose，而是共享 session identity 和 comment schema；forge submission 是 canonical local draft 的 effect adapter，不反过来定义本地真相。

#### Repo tree 摘要

```text
tuicr/                                      # 固定 commit tracked paths: 171
├── README.md / AGENTS.md / PLAN.md         # 产品、架构、计划
├── Cargo.toml / Cargo.lock                 # Rust 2024、依赖与锁文件
├── src/                                    # 127 tracked paths
│   ├── app/                                # session state、navigation、submit、tests
│   ├── ui/                                 # diff/file/comment/status rendering
│   ├── input/                              # keybindings 与 modes
│   ├── model/                              # DiffFile、Comment、ReviewSession
│   ├── vcs/{git,jj,hg}/                    # VcsBackend implementations
│   ├── forge/{github,gitlab}/              # PR/MR open、comment mapping、submission
│   ├── persistence/                        # atomic session/manifest/active-session store
│   ├── review_store.rs / review_cli.rs     # Agent/library canonical interface
│   ├── output/                             # Markdown/clipboard projection
│   ├── update/                             # verified release update
│   └── main.rs / lib.rs / cli.rs           # TUI, library and CLI surfaces
├── tests/fixtures/                         # PR refresh patches
├── docs/{REVIEW_CLI,GITLAB,CONFIG,...}.md  # machine interface、forge、配置
├── skills/tuicr/                           # agent workflow + tmux/Zellij/Herdr wrappers
├── scripts/demo/                           # demo fixtures/driver
└── .github/workflows/                      # CI/release/Nix build
```

源码模块数显示 `app` 34 paths、`forge` 19、`ui` 18、`vcs` 15、`update` 7；它不是“一个 diff renderer”，而是 local state + multi-VCS + multi-forge + updater 的组合。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/vcs/traits.rs` / `src/vcs/mod.rs` | VCS abstraction | `VcsBackend` 统一 Git/jj/hg；按 jj → git → hg 检测，避免 jj 的 Git backing 误判 |
| `src/model/review.rs` / `src/model/comment.rs` | canonical review model | files/reviewed hunks/comments、line side/range、lifecycle 与 author |
| `src/review_store.rs` | shared mutation facade | TUI/CLI/library 共用 `add_comment_to_session`，拒绝 empty/unknown file |
| `src/persistence/storage.rs` | durable state | slug-derived path、manifest、lock、atomic replace、active PID/path/freshness |
| `src/review_cli.rs` | Agent machine surface | list/comments/add，JSON input/output 与 slug/path resolution |
| `src/forge/submit.rs` | effect-neutral mapping | comment anchor → inline/unmappable；binary、too-large、side/range edge cases |
| `src/forge/github/submit.rs` | GitHub payload projection | commit/body/event/comments；draft 省略 event |
| `src/forge/gitlab/glab.rs` | GitLab adapter | glab CLI、MR diff/header normalization、discussion submission |
| `docs/REVIEW_CLI.md` | machine contract | active signal、slug kinds、JSON schema 与 CLI behavior |
| `skills/tuicr/SKILL.md` | agent workflow | 区分 user-led 与 agent-led review；禁止冒充用户 comment |

#### 源码精读（固定 commit）

**代码块 1：VCS 自动检测优先识别 jj，避免被 Git backing 抢先**  
来源：`src/vcs/mod.rs:324-348`

```rust
pub fn detect_vcs(
    git_backend_preference: GitBackendPreference,
    whitespace_mode: DiffWhitespaceMode,
) -> Result<Box<dyn VcsBackend>> {
    if let Ok(backend) = JjBackend::discover(whitespace_mode) {
        return Ok(Box::new(backend));
    }
    if let Ok(backend) = GitBackend::discover(git_backend_preference, whitespace_mode) {
        return Ok(Box::new(backend));
    }
    if let Ok(backend) = HgBackend::discover(whitespace_mode) {
        return Ok(Box::new(backend));
    }
    Err(TuicrError::NotARepository)
}
```

逻辑：capability detection 不是任意 first-success；因为 jj repo 可能 Git-backed，必须先试更具体的 backend。对 Hermes 工具路由的启示是 capability overlap 时应使用 specificity order 或 explicit preference。边界是 `discover` 失败被吞成下一 backend，诊断可能丢失；最终 `NotARepository` 不说明每个尝试为何失败。

**代码块 2：TUI 与 Agent 共用唯一 comment mutation primitive**  
来源：`src/review_store.rs:209-264`

```rust
pub fn add_comment_to_session(
    session: &mut ReviewSession,
    request: AddCommentRequest,
) -> Result<Comment> {
    let content = request.content.trim().to_string();
    if content.is_empty() {
        return Err(TuicrError::InvalidInput("comment cannot be empty".to_string()));
    }
    let comment = match request.target {
        CommentTarget::Review => {
            let comment = Comment::new(content, request.comment_type, None)
                .with_author(request.author);
            session.review_comments.push(comment.clone());
            comment
        }
        CommentTarget::File { path } => {
            let review = file_review_mut(session, &path)?;
            let comment = Comment::new(content, request.comment_type, None)
                .with_author(request.author);
            review.add_file_comment(comment.clone());
            comment
        }
        CommentTarget::Line { path, line, side } => {
            let review = file_review_mut(session, &path)?;
            let comment = Comment::new(content, request.comment_type, Some(side))
                .with_author(request.author);
            review.add_line_comment(line, comment.clone());
            comment
        }
        CommentTarget::LineRange { path, range, side } => {
            let review = file_review_mut(session, &path)?;
            let comment = Comment::new_with_range(
                content, request.comment_type, Some(side), range,
            ).with_author(request.author);
            review.add_line_comment(range.end, comment.clone());
            comment
        }
    };
    session.updated_at = Utc::now();
    Ok(comment)
}
```

逻辑：review/file/line/range target 都落同一 model；unknown file 在 `file_review_mut` 被拒绝；TUI 与 `ReviewStore` 不各写一套 mutation。对 shared hub 的迁移点是 human/agent feedback 应共用 typed operation，并保留 author/lifecycle，而不是把 Agent 建议伪装为用户事实。边界是该函数不验证 line 是否在当前 diff；effect submission 仍需后置 map/preflight。

**代码块 3：session 更新由锁内 read-modify-atomic-write 完成**  
来源：`src/persistence/storage.rs:69-80,334-375`

```rust
pub(crate) fn update_session_in_dir<T>(
    session_ref: &Path,
    reviews_dir: &Path,
    update: impl FnOnce(&mut ReviewSession) -> Result<T>,
) -> Result<(ReviewSession, T)> {
    maybe_migrate(reviews_dir)?;
    with_reviews_dir_lock(reviews_dir, || {
        let mut session = load_session(session_ref)?;
        let output = update(&mut session)?;
        save_session_in_dir_unlocked(&session, reviews_dir)?;
        Ok((session, output))
    })
}

fn write_atomic(path: &Path, bytes: &[u8]) -> Result<()> {
    let parent = path.parent().ok_or_else(/* invalid input */)?;
    fs::create_dir_all(parent)?;
    let tmp_path = parent.join(format!(".session.{}.tmp", uuid::Uuid::new_v4()));
    {
        let mut tmp = fs::File::create(&tmp_path)?;
        tmp.write_all(bytes)?;
        tmp.sync_all().ok();
    }
    fs::rename(&tmp_path, path)?;
    Ok(())
}
```

注：第二段将真实 `file_name` formatting 简化为 `.session.<uuid>.tmp`，只为压缩展示；锁内 read/update/save 与 temp-write/rename 逻辑来自固定源码。逻辑：同一 reviews dir 的并发 mutations 串行；session JSON 和 manifest 通过 scoped save 路径更新。边界是这不是数据库事务：session rename 成功、manifest save 失败时可能产生不一致；`sync_all().ok()` 忽略 fsync error，且未见 parent directory fsync，断电 durability 不应过度宣称。

**代码块 4：提交前将无法安全定位的评论显式分类，不静默丢弃**  
来源：`src/forge/submit.rs:187-216`

```rust
pub fn map_comment(
    comment: &Comment,
    anchor: CommentAnchor,
    file: &DiffFile,
    config: &ForgeConfig,
) -> MappedComment {
    let path = file.display_path().clone();
    if file.is_binary {
        return MappedComment::Unmappable {
            comment: comment.clone(),
            file: path,
            reason: UnmappableReason::BinaryFile,
        };
    }
    if file.is_too_large {
        return MappedComment::Unmappable {
            comment: comment.clone(),
            file: path,
            reason: UnmappableReason::TooLargeFile,
        };
    }
    let old_path = renamed_old_path(file);
    match anchor {
        CommentAnchor::FileLevel => match file.first_valid_line(LineSide::New) {
            Some(line) => { /* build Inline with counterpart when present */ }
            None => { /* return Unmappable::FileLevelNoAnchor */ }
        },
        CommentAnchor::Line { line, side } => { /* validate/map side */ }
        CommentAnchor::Range => { /* validate same-side range */ }
    }
}
```

逻辑：binary、too-large、无 anchor、mixed-side range 与 line not in diff 都有结构化 reason；上层可让用户选择移到 summary，而不是假装 inline 已提交。边界是 map success 仍不证明远端 revision 未变、actor 有权限或 API 成功；必须在最终 effect point 重新核验 target revision、auth 与 user confirmation。

#### Canonical session 与 Agent workflow 的关键机制

`docs/REVIEW_CLI.md` 和 `skills/tuicr/SKILL.md` 共同说明：

- TUI 一旦 review target active 就创建 session；空 session 在退出时清理。
- `active_sessions.json` 保存 PID、slug、path 与 last-seen；list 输出 `active: true/false`，Agent 不必猜最近 mtime。
- session 参数可以是 local slug、self-contained PR slug 或 JSON path；machine output 默认 JSON/RFC3339。
- user-led review 与 agent-led review 是不同权限语义：user-led 时 Agent 只读用户 comments，不能预写、冒充或把自己的 finding 当用户反馈。
- `Comment` 有 ID、path、line/range、side、type、lifecycle、author；Markdown/clipboard 只是 projection。
- open issue [#410](https://github.com/agavra/tuicr/issues/410)（2026-07-30 更新）说明现有系统还不能 reply/resolve existing PR threads；所以 canonical local draft 并不等同于完整远端 thread state。

#### 依赖分析与供应链风险

- `Cargo.toml` package 版本 0.19.1、edition 2024、MIT，`Cargo.lock` 存在。
- TUI：`ratatui 0.30` 使用 unstable rendered-line-info feature，`crossterm 0.29`；comment editor 为 `edtui 0.11` 且关闭 default features。
- VCS：`git2 0.20`、系统 `git/jj/hg` CLI paths；forge 还依赖外部已认证 `gh` / `glab`，Cargo lock 无法覆盖这些二进制与 credential store。
- 状态/CLI：serde/json/toml、chrono、clap、directories、uuid、ignore、tracing。
- UI/文件：arboard（Wayland data control）、syntect/two-face、terminal-colorsaurus；clipboard 与 syntax stack 会引入平台差异。
- updater：ureq、self-replace、tempfile、semver、sha2、flate2/tar/zip。README 声称 direct binary update 校验 SHA-256；hash 只能校验指定 digest，digest/provenance 的信任来源仍需审计。
- `git2` 关闭 default features 会改变 TLS/SSH 能力边界；实际 GitHub/GitLab 操作主要通过 `gh/glab`，需分别审计 command args、PATH executable trust 和 auth scope。
- GitHub security advisories API 未返回公开 advisory；这不证明没有 bug。当前 issue #410 是功能缺口，不是 security advisory。

#### README / release / issue 交叉核验

- README 的“review CLI + Rust library + TUI”与 `review_store.rs`、`review_cli.rs`、`lib.rs` 和 docs 路径一致。
- latest release v0.19.1 修复 binary detection、fork PR edit、inline commit-range reload 等；这与 mapper/diff boundary 的复杂度相符。
- 固定 commit 是 release 后的 jj ANSI fix，说明多-VCS adapter 仍在快速迭代。
- issue #410 明确 existing remote threads 只能显示/新建 top-level comments，不能 reply/resolve；不要把“支持 PR review”外推成完整 review-thread lifecycle。
- `docs/GITLAB.md` 明确所有 GitLab 操作 shell out 到 `glab`，tuicr 自己不存 token；request changes 需要 actor 是 assigned reviewer，失败应原样 surfaced。

#### 真实测试结果

```text
CARGO=
RUSTC=
ATTEMPT
/usr/bin/bash: line 9: cargo: command not found
EXIT=127 COMMAND_DISCOVERY cargo=1 rustc=1
```

这只证明当前 WSL cron 环境缺 Rust toolchain，不证明 tuicr 上游测试失败。本次**没有编译、没有运行 TUI、没有写 review session、没有调用 gh/glab submit、没有更新二进制**。源码中的 unit tests 与 fixtures 已阅读，但行为待受控 Rust lane 核验。

#### 可复用经验

- 当人类和 Agent 要协作修改同一审查状态时，应优先使用带 stable session/comment ID、author、lifecycle 与 typed target 的 canonical store，因为 clipboard prose 会丢 identity 和并发语义；边界是 user comment 与 agent comment 必须保持不同 author/authority。
- 当多个后端 capability 重叠时，应优先按 specificity 或显式 preference 做检测，例如 jj 必须先于 Git，因为 jj repo 可能 Git-backed；边界是 fallback 还应保留每个探测失败原因。
- 当 TUI、CLI 和 library 都能写状态时，应优先让它们共用唯一 mutation primitive，并在 scoped lock 内 read-modify-atomic-write，因为独立写法容易覆盖或行为漂移；边界是文件锁/rename 不是完整数据库事务与崩溃一致性证明。
- 当本地 comment 要变成 GitHub/GitLab 副作用时，应优先先映射为 `Inline|Unmappable(reason)`，再由用户处理 unplaced comments 与确认 effect，因为 line/side/range 可能已失效；边界是 mapping 后仍要重验 remote revision 和 actor permission。
- 当 active resource 用 PID/path/mtime 表示时，应优先把它视为 convenience signal 并验证 scope/session identity，因为 PID 会复用、path 会变化、12 小时 freshness 不等于当前用户意图。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/human-review-session/` 建纯离线 JSON fixture（今日只设计）：

1. `review-session.schema.json`：`session_id, scope, revision, status, comments[]`。
2. comment 必须带 `comment_id, author_kind(user|agent), author_id, target, lifecycle, content, created_at`。
3. 写 `add_comment.py`，拒绝 empty、unknown file、out-of-scope path、stale revision；只做 atomic local JSON，不调用 forge。
4. fixture 覆盖并发 revision mismatch、user/agent author 混淆、binary/too-large/unmappable、session stale、duplicate ID。
5. 输出 Markdown projection；再从 projection 反向解析并故意证明 identity/lifecycle 丢失，从而固定 canonical-vs-projection 边界。

#### 风险边界

- **License**：repo 为 MIT；Rust transitive crates、themes、release archives、gh/glab 与远端平台条款需另审。抽象 schema，不复制整个 TUI。
- **维护活跃度**：commit 距查询约 19 小时，issue #410 在约 3 小时前更新，活跃；但版本 0.19.1、open items 90（含 PR），接口与存储 schema 仍可能变化。
- **安全风险**：review content 与 diff 均是不可信文本；TUI/clipboard/editor、PATH 中 git/jj/hg/gh/glab、自更新、archive extraction、session JSON 都是边界。
- **并发/durability**：lock 有 stale removal 与 12h reuse guard；atomic rename 不等于 session+manifest 双文件事务，fsync error 被忽略。
- **身份/权限**：`active:true` 是 PID/path/freshness signal，不是用户授权；same account 上的进程可读写相同 state；远端 submit 必须单独授权。
- **功能局限**：issue #410 尚未支持 reply/resolve existing thread；remote-only GitLab commit-range diff 文档标记 not supported。
- **本机待核验**：缺 Cargo，compile/tests/TUI/Windows/macOS/Wayland/gh/glab behavior 全部待核验。
- **不可自动执行**：不安装或启动 tuicr，不打开 multiplexer，不写用户 review，不调用 `:submit`、gh/glab mutation 或 updater，不把 Agent comment 伪装成用户 comment。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`canonical review session + typed author/lifecycle + effect adapter`，可用于 Hermes 产物验收与用户反馈闭环。
- **需验证**：在 shared hub 自有 JSON fixture 上验证 scoped identity、concurrent revision、user/agent authority 与 projection loss；再与 orchestrator approval gate、verification-first、shared memory candidate review 去重。
- **暂不沉淀**：完整 tuicr TUI skill、tmux/Zellij/Herdr wrappers、gh/glab submit、自更新器；当前 Hermes cron 无用户在场，且 Rust tests blocked。
- **今日动作**：不安装、不升格，只创建 candidate/open question。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/human-review-session/{review-session.schema.json,fixtures/,add_comment.py,project_markdown.py,test_session.py}`。
2. **候选接口**：`add_review_comment(session_id, expected_revision, author, target, content) -> accepted|conflict|blocked`；author 必须由 host 注入，不能让模型自称 user。
3. **candidate queue 映射**：Hermes 生成 candidate；用户/总控 comment 作为独立 review record；approval 后 promoter 消费 canonical record，Markdown 只作展示。
4. **orchestrator 映射**：prepare/research/spec/quality/promotion 各有 immutable run scope；用户 comment 不能改写原始 executor artifact，只能形成 review decision。
5. **shared hub 分层**：review runtime state 留 `runtime/hermes/`；raw agent report 留 inbox；approved stable fact 才进入 curated；projection/notification 不反向成为 source of truth。
6. **future-agent 复用**：共享 schema、authority/lifecycle 与 fixtures；Agent-local UI/CLI adapter 独立实现。当前任务没有调用 OpenClaw。

## 横向对照：从模糊输入到可审计状态

| 层次 | last30days-skill | tuicr | Hermes/shared hub 候选 |
|---|---|---|---|
| 意图入口 | SKILL.md 把自然语言转 plan/flags | skill 区分 user-led / agent-led review | host-owned task/review intent，author authority 明确 |
| canonical state | `RetrievalBundle`、`Report`、`SourceOutcome` | `ReviewSession`、Comment ID/lifecycle、manifest | versioned research bundle + review session |
| 执行边界 | source adapters + fetch budget + retry | VCS/forge adapters + submit mapper | tool/source effect metadata + scoped receipt |
| honest failure | rate-limited/auth/partial/no-results 分离 | Inline/Unmappable(reason)、CLI errors | blocked/degraded/failed 不冒充空结果/完成 |
| 融合/变更 | weighted RRF + rerank + cluster | lock 内 typed mutation | deterministic candidate merge + revision check |
| projection | Markdown/HTML/JSON/library | TUI/Markdown/stdout/GitHub/GitLab | inbox/Obsidian/notification 都是 projection/raw layer |
| 人类权限 | host 负责 consent/setup | user comments 与 agent comments 分离 | user approval 独立于 agent proposal，不从 prose 猜 authority |

## 经验沉淀

1. 当多个外部来源共同支撑研究结论时，应优先为每个来源记录 `attempted/state/items/detail/evidence`，因为 `no-results`、403、429、timeout 与 schema drift 的语义不同；边界是分类器本身也需要 fixtures。
2. 当不同来源的原生 engagement/score 不可比时，应优先以 per-stream rank + weighted RRF 融合并保存 provenance，因为直接比较 likes、stars、points 会制造伪精度；边界是同源转载不能自动算独立 corroboration。
3. 当 private corpus 与 public web evidence 合并时，应优先让 privacy label 随 candidate 传播，并在 hosted model、publish、log 等每个出口做 gate；边界是只在主 reranker 分流不等于全链路无泄漏。
4. 当一个 Skill 跨多个 harness 时，应优先拆分 agent contract、deterministic engine 与 host adapter，并做逐 host contract fixtures；边界是 contract 无限增长会反过来造成上下文税和行为漂移。
5. 当测试依赖权限位时，应优先显式覆盖 root/non-root 或 mock syscall failure，因为 root 可绕过普通 DAC；边界是 mock 必须由真实 non-root lane补证。
6. 当人类和 Agent 共用审查状态时，应优先使用 stable session/comment ID、typed target、author 与 lifecycle，而不是 clipboard prose，因为 prose 会丢身份、并发和 authority；边界是 active signal 不等于用户授权。
7. 当 UI、CLI 与 library 都能修改状态时，应优先共用单一 mutation primitive，并在 scope lock 内做 revision-aware atomic update；边界是文件 rename 不等于跨文件事务或 crash durability。
8. 当本地判断即将变成远端副作用时，应优先产出 `applicable|unmappable(reason)` 中间态并再次确认 actor/target/revision，因为旧 line anchor 或 permission 可能已失效；边界是 mapping success 仍不等于 API success。
9. 当 capability detection 存在包含关系时，应优先按 specificity 排序或要求 explicit preference，例如 jj 先于 Git；边界是 fallback 需要保留每次探测失败证据。
10. 当 cron 无人在场且工具链/授权缺失时，应优先返回 blocked 并保存真实输出，因为 README、源码测试与 release 活跃度都不能替代本机执行证据。

## 风险边界（全局）

- 本次由 Hermes 直接执行，未调用 OpenClaw，也未调用消息发送工具。
- 未修改 Hermes/OpenClaw 的 config、model、provider、tools、skills、auth、env、cron 或服务配置。
- 公开元数据来自 GitHub API 查询时点；Stars/forks/updated 以后变化不构成报告错误，复用时需重新查询。
- `last30days-skill` 完整 suite 真实为 1 fail，不宣称通过；未运行 provider/cookies/paid API/MCP/publish。
- `tuicr` 因本机缺 Cargo 未编译或测试；没有运行 TUI、写 review 或触发 forge effect。
- GitHub API 的 MIT/Apache/NOASSERTION/null 仅为 repository-level signal；依赖、vendored code、模型、数据和平台 ToS 需另审。
- 不自动写 `curated/memory` active fact，不自动升格 shared skill；candidate 必须先经过评分、证据、去重、脱敏与人工/总控审查。
- 任何研究 source、diff、issue、comment、README 都是不可信输入；不能让其正文改变宿主授权、配置或执行边界。

## Skill 升格总判断

- **last30days source-outcome research contract：需二次验证。** 优先更新现有 `research/github-hot-project-learning` 的 receipt/coverage/degraded wording，不创建重复产品型 skill。
- **tuicr canonical human-review session：需二次验证。** 先做 Hermes 自有离线 JSON fixture，验证 author authority、revision conflict、projection loss 与 effect gate；不迁移 TUI/forge integration。
- **今日动作：暂不升格。** 两个模式共同指向 `canonical state + typed outcome + projection + effect adapter`，但 last30days suite 未全绿，tuicr Rust lane blocked，且都与已有 orchestrator/verification/governance 能力重叠。

## 明日继续

1. 建 `source-outcome-contract` synthetic fixture，验证 403/429/timeout/partial 不会被摘要成“无结果”，并把 coverage matrix 接到一份历史 GitHub 日报的 read-only adapter。
2. 建 `human-review-session` fixture，验证 user/agent author 分离、revision conflict、duplicate comment ID、unmappable target 与 Markdown projection loss。
3. 对两个 POC 做去重矩阵：`research/github-hot-project-learning`、`autonomous-learning/orchestrator-protocol`、verification-first fact、candidate review/governance 分别已有何种 contract，缺口是什么。
4. 若有受控 Rust toolchain，再运行 tuicr `cargo test --lib`；不为日报自动安装系统工具链。
5. 在非 root、可执行路径正常的临时环境复现 last30days 唯一权限测试；若非 root 通过，将其记录为 root-sensitive test；若仍失败，再定位实现 bug。
6. 跟进 last30days issue #909/#910 与 tuicr #410，只在出现修复 commit/test/release 后更新事实，不把 open proposal 写成已实现。

## 候选反哺

### Candidate Facts

- [ ] topic: research-source-outcome-must-distinguish-no-results-from-transport-failure | evidence: last30days `SourceOutcome`、`RetrievalBundle.record_failure`、commit `57f8d2c...`、full suite 3576 pass/1 fail | 建议: update verification/research contract after fixtures | 安全级别: low
- [ ] topic: private-evidence-label-must-propagate-through-fused-candidate | evidence: last30days `pipeline.py:2401-2437` private/public rerank split | 建议: candidate，审计所有出口后再 create/update | 安全级别: medium
- [ ] topic: human-and-agent-review-should-share-canonical-session-but-not-authority | evidence: tuicr `ReviewStore`、`add_comment_to_session`、review CLI JSON、Skill user-led/agent-led split | 建议: candidate，先做 Hermes fixture | 安全级别: medium
- [ ] topic: active-session-pid-path-freshness-is-convenience-not-authorization | evidence: tuicr `active_sessions.json` implementation + 12h freshness | 建议: update scoped-authority candidate after validation | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: source-outcome-aware-research | 可复用场景: GitHub/教程/网页/安全调研、巡检、future-agent | 是否建议 shared: yes（验证后更新现有 skill） | 原因: 防止 blocked source 冒充 clean；应并入 `research/github-hot-project-learning`
- [ ] 名称: human-review-session-adapter | 可复用场景: 用户验收 Agent 产物、candidate promotion、代码/文档 review | 是否建议 shared: yes（POC 与授权审计后） | 原因: 横跨 agent，但必须 host 注入 author/authority
- [ ] 名称: last30days-product-integration | 可复用场景: social/web research | 是否建议 shared: no | 原因: 222 KB contract、cookies/keys/network/provider/MCP 权限面过大，且本机 suite 未全绿
- [ ] 名称: tuicr-product-integration | 可复用场景: interactive code review | 是否建议 shared: no | 原因: 需要 Cargo/TUI/multiplexer/gh/glab/user presence；当前只抽象 canonical session

### Candidate Open Questions

- [ ] 问题: GitHub learning orchestrator 应在哪个 chokepoint 汇总 source outcomes，并怎样让 `overall_status=completed` 同时表达 coverage/degraded？ | reason: adaptation | priority: high
- [ ] 问题: 同一原始消息在 Reddit/X/YouTube 转述时，如何证明 independent corroboration 而不是多平台转载？ | reason: gap | priority: high
- [ ] 问题: private label 应如何跨 dedupe/merge/cluster/projection 保持 taint，并被哪些 outbound surfaces 强制执行？ | reason: security/adaptation | priority: high
- [ ] 问题: shared hub 的 user review record 应由哪个 host-owned接口写 author/authority，避免模型自称 user？ | reason: security/design | priority: high
- [ ] 问题: 文件型 review session 如何实现 session JSON + manifest 的 crash-consistent transaction，或是否应直接使用 SQLite？ | reason: adaptation | priority: medium
- [ ] 问题: last30days permission fixture 在真实 non-root WSL lane 是否通过，root CI 应 mock 还是 skip？ | reason: environment-gap | priority: medium

### 不应自动落地

- 不安装/运行 last30days，不读取 browser cookies、keychain、`.env` 或 secret，不调用付费 API、MCP、publish、webhook。
- 不安装/运行 tuicr，不打开 TUI/multiplexer，不写或提交用户 review，不调用 gh/glab mutation/self-update。
- 不修改 Hermes/OpenClaw config、model、provider、tools、skills、auth、env、cron；本任务未调用 OpenClaw。
- 不把 today candidate 直接写入 `curated/memory` active fact 或 shared manifest；先完成 runtime POC、治理评分、去重、脱敏与人工/总控审查。
