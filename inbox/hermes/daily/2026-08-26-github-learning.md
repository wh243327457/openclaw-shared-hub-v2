# 2026-08-26 GitHub 热门项目每日学习报告

- 执行器：Hermes；当前 OpenClaw runtime 不存在，本次没有调用、启动或模拟 OpenClaw。
- 研究日期：2026-08-26（UTC+8）。
- 共享根：先运行 `python3 scripts/resolve_shared_root.py`，真实返回 `/home/vany/agent/shared`。
- 发现来源：GitHub Search API，查询 `created:>2025-06-01 stars:>1000 archived:false`，按 Stars 降序；返回候选 30 个。
- GitHub repository API 快照时间：2026-08-26T07:39:32+08:00；Stars、Forks、Language、License、updated/pushed 均取自本次 API 输出。
- 深读固定提交：`Graphify-Labs/graphify@43d54acbfa9e731f7a592bb582c1f4b9d48ed73e`；`JuliusBrussee/caveman@81536f57b3303b7de7f5bc5b564cc344f9112d68`。
- 证据边界：README/docs/SECURITY/release/issues/Actions 来自固定提交或 GitHub API；源码判断来自浅克隆的固定提交；测试与审计结论只使用本机真实命令结果。无法覆盖的路径明确标为“待核验”。

## 今日结论

**今日主线是“有损加速不能冒充完整真相”：Graphify 通过可追溯的图 schema、置信标签、增量 cache 与原子导出减少重复读库，但 open issues 仍显示 partial extraction 可能污染 manifest/增量图；Caveman 通过类型检测、保守压缩和 CCR 原文恢复减少上下文，却也证明只有在原文已持久化、作用域/许可清楚、端到端 route 真正生效时，压缩结果才可安全使用。对 Hermes/shared hub 最值得迁移的是 `canonical source + derived projection + coverage/partial + recovery handle + fail-closed publish` 契约，而不是安装两个完整产品。**

## 研究范围与真实验证摘要

1. GitHub Search API 的当日高 Stars 候选包含 `openclaw/openclaw`、`obra/superpowers`、`affaan-m/ECC`、`NousResearch/hermes-agent`、`Graphify-Labs/graphify`、`JuliusBrussee/caveman`、`earendil-works/pi`、`thedotmack/claude-mem`、`ruvnet/RuView`、`paperclipai/paperclip` 等。为避免重复，今日选择尚未在本学习任务中建立项目卡的 Graphify 与 Caveman。
2. Graphify repository API 快照：**110,485 Stars / 10,758 Forks / Python / Apache-2.0**；default branch `v8`；`updated_at=2026-08-25T23:29:03Z`，`pushed_at=2026-08-25T17:43:30Z`。浅克隆 HEAD `43d54ac...` 正好有 tag `v0.9.50`。
3. Graphify 最新 release `v0.9.50` 发布于 `2026-08-25T17:43:31Z`。固定提交有 838 个 tracked files、337 个 Python files、228 个 `tests/test_*.py`。
4. Graphify 本机以 `uv run --frozen` 创建 Python 3.13.13 环境；五个聚焦测试文件真实返回 **101 passed in 7.12s**，另有 `compileall` 成功和 schema 正/反 fixture 实测。没有运行全套 228 个测试文件、LLM semantic pass、PDF/Office/media、MCP HTTP、Neo4j/FalkorDB、真实大型 repo 或 benchmark。
5. Graphify `uv run --frozen pip-audit` 真实返回 exit 1：当前安装环境中发现 **5 个记录（2 个 package）**，涉及 `pip 26.1.1` 的 `PYSEC-2026-196` / `PYSEC-2026-3721` 与 `setuptools 82.0.1` 的 `PYSEC-2026-3447`；重复记录来自依赖解析输出。可选 PDF extra 未安装，因此本次 audit 不覆盖 lock 中的 `pypdf 6.13.3`；open issue #2658 对该版本的 PDF text-extraction advisories另有报告，仍需在 all-extras/隔离 PDF lane复验。
6. Graphify open issue #3004 报告默认 dedup 的增量 merge 在 partial semantic re-extraction 时可能先删除旧节点再只恢复部分；#3093 报告 failed semantic chunk 仍被写入 manifest、以后不重试；#2781 报告文档 semantic pass缺少 outbound secret redaction。它们与源码的 partial marker、cache scope、shrink guard形成直接采纳边界，不能凭聚焦测试宣称已解决。
7. Caveman repository API 快照：**100,943 Stars / 5,860 Forks / Go / License `NOASSERTION`**；default branch `main`；`updated_at=2026-08-25T23:25:11Z`，`pushed_at=2026-08-24T23:31:25Z`。API 的 `NOASSERTION` 是准确快照；仓库自己的 `LICENSE` / `LICENSE.BSL` / `LICENSING.md` 则声明**按目录拆分 MIT + BSL-1.1**，不能简化成“MIT 项目”。
8. Caveman 最新 stable release `v2.3.1` 发布于 `2026-08-23T09:01:48Z`；浅克隆 HEAD `81536f5...` 晚于该 release，不是 tag。固定提交有 1,388 个 tracked files、528 个 Go files、318 个 JS/MJS/TS files、20 个 `skills/*/SKILL.md`。
9. Caveman 本机 Node `v22.14.0` / npm `10.9.2`；根 installer suite 真实返回 **175 passed / 0 failed / 92.50s**，包括 fake/isolated Hermes 安装、冲突备份、ownership journal、uninstall 与 dry-run。没有写当前 `~/.hermes`，没有调用 OpenClaw；测试自身使用临时目录覆盖了兼容 adapter。
10. 本机没有 Go；仓库 `go.mod` 要求 `go 1.26.5`，所以 Engine/CCR/contextwindow/cacheengine/proxy 的 compile/test/race/fuzz/cargo式依赖审计均**待核验**。根 `npm audit --omit=dev --package-lock-only` 实报 **0 known npm advisories**，但只覆盖根 installer 的很窄生产依赖（metadata 显示 prod 2），不能外推到 Go graph、release binaries、Chrome、provider、MCP 或 skill 行为。
11. Caveman open issue #908 报告 Claude subscription/OAuth traffic 即使显式经过 compress proxy也不进入 eligible compression，且 MCP recovery安装标记与 status/doctor不一致；#895 报告 `caveman-compress` 被 Hermes project-skill scanner判 dangerous；#544 报告压缩 skill 曾在验证前覆盖 live file。它们说明源码中的 CCR fail-closed contract不等于每个 host adapter/skill mutation path都满足该 contract。
12. 两仓 Dependabot alerts API均未给出可用结果：Graphify返回权限 403，Caveman返回“Dependabot alerts are disabled” 403；repository advisories API查询为空数组。空数组/403都不能证明无漏洞。

## 项目速览

> 下表 Stars / Language / License / updated/pushed 均来自本次 GitHub repository API。Stars 是查询瞬时快照；License 是 API 的仓库顶层识别，不覆盖依赖、模型、release asset、目录级例外或商标。

| 项目 | Stars | Language | License（GitHub API） | updated / pushed（UTC） | 今日判断 |
|---|---:|---|---|---|---|
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 110,485 | Python | Apache-2.0 | 2026-08-25T23:29:03Z / 2026-08-25T17:43:30Z | **深读：derived graph、coverage、partial/cache truth** |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 100,943 | Go | NOASSERTION（仓库内 split MIT+BSL） | 2026-08-25T23:25:11Z / 2026-08-24T23:31:25Z | **深读：fail-closed compression、CCR、host adapter边界** |
| [earendil-works/pi](https://github.com/earendil-works/pi) | 97,219 | TypeScript | MIT | 2026-08-25T23:01:35Z / 2026-08-25T22:50:18Z | 高热；此前报告已涉及其依赖/adapter，不重复深读 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 91,835 | JavaScript | Apache-2.0 | 2026-08-25T23:30:38Z / 2026-08-25T23:29:49Z | 持续记忆候选；需单独审 capture/privacy |
| [ruvnet/RuView](https://github.com/ruvnet/RuView) | 91,636 | Rust | MIT | 2026-08-25T23:12:04Z / 2026-08-25T18:11:45Z | Rust observability候选；本机无 Rust lane |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | 79,371 | TypeScript | MIT | 2026-08-25T23:12:42Z / 2026-08-25T23:12:04Z | 多 Agent控制面候选；此前报告已提及，不重复 |

## 深读项目

### 1. Graphify-Labs/graphify

- **一句话判断**：值得学的不是“用图替代 grep”这一口号，而是把 source-derived AST/semantic事实、confidence/provenance、portable identity、incremental cache 与 query projection显式化；但 open issues 显示 partial semantic extraction仍可能被过早投影为 current manifest/新图，所以它适合作为 coverage/derived-state实验对象，不适合直接成为 shared truth layer。
- **解决的问题**：替代每次让 Agent从头扫描整个 repo、让多个 Agent各自构建不可共享的文本摘要、用无 provenance 的向量近邻解释架构的旧做法。代码走本地 tree-sitter确定性抽取，文档/media走可选 semantic pass，最终统一成带 source/confidence 的 graph，再按 query预算遍历。

#### 基本信息与可验证来源

- URL：https://github.com/Graphify-Labs/graphify
- GitHub API：**Stars 110,485；Forks 10,758；Language Python；License Apache-2.0**。
- API时间字段：`updated_at=2026-08-25T23:29:03Z`，`pushed_at=2026-08-25T17:43:30Z`，open issues `1,108`，default branch `v8`。
- 固定提交：[`43d54acbfa9e731f7a592bb582c1f4b9d48ed73e`](https://github.com/Graphify-Labs/graphify/commit/43d54acbfa9e731f7a592bb582c1f4b9d48ed73e)，浅克隆上有 tag `v0.9.50`。
- Release：[`v0.9.50`](https://github.com/Graphify-Labs/graphify/releases/tag/v0.9.50)，发布于 2026-08-25T17:43:31Z；release notes包括 Ruby符号ID、qualified constant receiver、graph merge community offset、Windows BOM root marker、ignore matcher性能、enum member抽取等修复。
- Docs：`ARCHITECTURE.md` 给出 `detect → extract → build → cluster → analyze → report → export`；`docs/how-it-works.md` 划分本地 AST、本地音视频转录、可选文档/图片 semantic pass。
- Issues：[#3004](https://github.com/Graphify-Labs/graphify/issues/3004)、[#3093](https://github.com/Graphify-Labs/graphify/issues/3093)、[#2781](https://github.com/Graphify-Labs/graphify/issues/2781)、[#2658](https://github.com/Graphify-Labs/graphify/issues/2658) 查询时均 open。
- 本机验证：聚焦 tests `101 passed in 7.12s`；`compileall`成功；未连接任何 LLM backend、数据库、MCP HTTP或外部语料。

#### 架构 / 实现与数据流

```text
corpus / repository
       |
       v
detect(root)
  classify files + ignore rules + scan metadata
       |
       +---------------------------+
       |                           |
       v                           v
AST extract(paths, root=...)   optional semantic extraction
(tree-sitter, local)           docs/PDF/images -> configured backend
       |                           |
       +---- nodes/edges ----------+
               confidence/source_file/_origin
                       |
                       v
       validate_extraction -> build/build_merge
       tier-scoped replace + dedup + prune
                       |
                       v
       NetworkX graph -> cluster -> report/export
                       |
         graph.json + report/wiki/html
                       |
                       v
       query/path/explain/MCP bounded traversal
```

机制上有六个值得区分的事实面：

1. **Corpus discovery**：`detect()` 决定扫描范围，ignore/symlink/format支持决定 coverage，不是“目录存在就已读”。
2. **Producer tier**：AST与semantic是不同 producer；`_origin`与 tier-scoped replace避免一层更新删除另一层，但 partial producer coverage仍是风险。
3. **Evidence schema**：node带 `id/label/file_type/source_file`；edge带 `source/target/relation/confidence/source_file`，允许 EXTRACTED/INFERRED/AMBIGUOUS。
4. **Incremental identity/cache**：AST和semantic cache分 namespace，semantic cache还能绑定 prompt fingerprint、allowed source scope与 partial marker。
5. **Projection safety**：`to_json`比较旧/新节点数、拒绝覆盖 malformed/shrunken graph，并用原子写；但 issue #3004指出 default dedup/partial replace路径仍存在未覆盖窗口。
6. **Query projection**：query用 term scoring选择 seeds，再在 token budget内 BFS/DFS；输出标 graph path/node count，降低从错误 corpus回答的风险，但 query仍是 derived view而非 source truth。

#### Repo tree 摘要（固定提交）

```text
graphify/
├── graphify/
│   ├── detect.py                 # corpus扫描、类型识别、ignore与格式入口
│   ├── extract.py                # AST调度、并行抽取、跨文件解析、portable ID
│   ├── extractors/               # 分语言 tree-sitter/regex extractors
│   ├── validate.py               # node/edge schema与endpoint校验
│   ├── build.py                  # dedup、tier merge、prune、graph assembly
│   ├── cache.py                  # AST/semantic cache、prompt/partial/scope约束
│   ├── cluster.py                # Leiden/Louvain、hub排除、stable community IDs
│   ├── serve.py                  # query/path/explain与MCP stdio/HTTP
│   ├── export.py                 # graph.json/HTML/Obsidian/GraphML/Cypher
│   ├── security.py               # URL/path/label/input边界
│   └── cli.py                    # extract/update/watch/query命令编排
├── tests/                        # 228个 test_*.py；本次只跑5个聚焦文件
├── tools/skillgen/               # 多host skill/always-on生成与golden fixtures
├── docs/                         # how-it-works、协议、平台说明
├── worked/                       # worked corpus及图输出/review
├── pyproject.toml                # core + optional extras + dev dependency groups
├── uv.lock                       # 锁定依赖图
├── ARCHITECTURE.md / SECURITY.md # 架构与威胁模型
└── LICENSE / LICENSE-MIT / NOTICE
```

固定提交统计：838 tracked files、337 Python files、228 test files。规模与测试数量只说明覆盖面，不能证明所有格式/backend已在本机执行。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `graphify/extract.py` | AST核心与cross-file resolution | explicit `root`绑定portable identity；cache hit/uncached work分流；20+文件可进process pool；empty/error source不会被当正常cache hit |
| `graphify/validate.py` | extraction contract | 校验node/edge必需字段、file_type/confidence枚举、非hashable ID与dangling endpoint |
| `graphify/cache.py` | semantic cache | mode/prompt namespace；allowed-source write scope；partial entry按miss处理；legacy vintage发warning |
| `graphify/build.py` | merge/dedup/prune | AST/semantic tier-scoped replace；existing malformed graph拒绝覆盖；issue #3004指出partial replacement仍有缺口 |
| `graphify/export.py` | canonical projection | node/link排序、confidence默认分数、direction恢复、shrink guard与atomic JSON write |
| `graphify/cluster.py` | community projection | hub exclusion、isolate处理、oversized/low-cohesion二次切分、stable size+lexical reindex |
| `graphify/serve.py` | bounded query | query scoring、seed selection、BFS/DFS、token budget、graph identity header、ambiguous symbol guard |
| `graphify/security.py` |输入/输出安全 | SSRF/private address、fetch cap、graph path、label/input sanitization；semantic outbound secret仍见issue #2781 |

#### ⭐ 源码精读

**代码块 1：`extract()`——显式 root、cache分流、并行失败后只补未完成项**  
来源：[`graphify/extract.py#L5665-L5798`](https://github.com/Graphify-Labs/graphify/blob/43d54acbfa9e731f7a592bb582c1f4b9d48ed73e/graphify/extract.py#L5665-L5798)

```python
def extract(
    paths: list[Path],
    cache_root: Path | None = None,
    *,
    root: Path | None = None,
    parallel: bool = True,
    max_workers: int | None = None,
    resolution_context_nodes: list[dict] | None = None,
    resolution_context_edges: list[dict] | None = None,
) -> dict:
    paths = [Path(p) for p in paths]
    anchor_root = Path(root) if root is not None else None
    # ... load_cached -> uncached_work ...
    if uncached_work:
        ran_parallel = False
        if parallel and len(uncached_work) >= _PARALLEL_THRESHOLD:
            ran_parallel = _extract_parallel(
                uncached_work, per_file, root, max_workers, total, cache_location
            )
        if not ran_parallel:
            _extract_sequential(
                [(i, p) for (i, p) in uncached_work if per_file[i] is None],
                per_file, root, total, cache_location,
            )
```

逻辑摘要：输入 path与cache位置不是同一身份；`root`决定 source_file/node ID/resolution锚点，`cache_root`只决定缓存位置。pool中途失败时只补 `per_file[i] is None` 的项，避免重做已完成工作。后续还把error/zero-node source列入 failed sources，意图让下次重试。边界：这些AST级保护不能自动覆盖LLM semantic chunk的manifest lifecycle；#3093说明编排层仍可能把失败文件stamp为current。

**代码块 2：`validate_extraction()`——schema valid不是“有内容”，但至少阻止坏ID/坏枚举/悬空边**  
来源：[`graphify/validate.py#L10-L87`](https://github.com/Graphify-Labs/graphify/blob/43d54acbfa9e731f7a592bb582c1f4b9d48ed73e/graphify/validate.py#L10-L87)

```python
def validate_extraction(data: dict) -> list[str]:
    if not isinstance(data, dict):
        return ["Extraction must be a JSON object"]
    errors: list[str] = []
    node_ids: set = set()
    # ... collect and validate node ids ...
    edge_list = data.get("edges") if "edges" in data else data.get("links")
    for i, edge in enumerate(edge_list or []):
        if "confidence" in edge and edge["confidence"] not in VALID_CONFIDENCES:
            errors.append(f"Edge {i} has invalid confidence ...")
        for endpoint in ("source", "target"):
            val = edge[endpoint]
            if bool(node_ids) and val not in node_ids:
                errors.append(
                    f"Edge {i} {endpoint} '{val}' does not match any node id"
                )
    return errors
```

本机fixture：合法单node/零edge返回 `[]`；非法fixture真实返回3个错误（non-hashable ID、invalid file_type、invalid confidence）。逻辑摘要：validator保护形状与引用闭包，但“只抽出1个合法node”仍能schema-valid；因此还必须验证 dispatched files coverage、旧/新source identity overlap和partial terminal，不能用schema valid替代完整性。

**代码块 3：`to_json()`——旧图 shrink guard + canonical projection + atomic write**  
来源：[`graphify/export.py#L266-L321`](https://github.com/Graphify-Labs/graphify/blob/43d54acbfa9e731f7a592bb582c1f4b9d48ed73e/graphify/export.py#L266-L321) 与 [L323-L410](https://github.com/Graphify-Labs/graphify/blob/43d54acbfa9e731f7a592bb582c1f4b9d48ed73e/graphify/export.py#L323-L410)

```python
def to_json(G, communities, output_path, *, force=False,
            built_at_commit=None, community_labels=None) -> bool:
    existing_path = Path(output_path)
    if not force and existing_path.exists():
        # ... parse old graph; malformed non-empty input returns False ...
        new_n = G.number_of_nodes()
        if new_n < existing_n:
            print("[graphify] WARNING: new graph ... Refusing to overwrite.",
                  file=sys.stderr)
            return False
    # ... canonicalize/sort nodes and links ...
    from graphify.paths import write_json_atomic
    write_json_atomic(output_path, data, indent=2)
    return True
```

逻辑摘要：最终projection不是裸 `write_text`：先读取旧图、拒绝不可解释的缩小或malformed baseline，再排序字段/节点/链接，最后atomic write。这适合作为shared derived index的最低门槛。边界：count guard看不到“节点数相同但身份全换”；#3004还指出默认dedup与partial re-extract可能绕过或发生在更早阶段，所以需要 per-source coverage/hash/overlap gate，而不只比较总节点数。

#### 依赖分析与供应链风险

- `pyproject.toml` core依赖 NetworkX、NumPy、RapidFuzz、tree-sitter及大量语言grammar；这些grammar有窄版本上限，降低ABI漂移但增加升级协调成本。
- optional extras扩展到 MCP/Starlette、Neo4j、FalkorDB、pypdf、Office、Google、faster-whisper、yt-dlp、OpenAI/tiktoken、Boto3、Anthropic、SQL/Postgres及更多tree-sitter grammar；“core local”不能外推到 all-extras。
- dev group含 Bandit、Hypothesis、Nuitka、pip-audit、Pyright、Pytest、Ruff、build toolchain。README明确 Bandit/pip-audit CI为 advisory/`continue-on-error`，不是阻断gate。
- 本机聚焦环境安装86 packages。`pip-audit`发现当前环境的 pip/setuptools advisories并exit 1；生产core可达性与修复影响待核验，不能把它们等同Graphify runtime漏洞，也不能忽略。
- `uv.lock`锁定 `pypdf 6.13.3`，但本机没有安装PDF extra；issue #2658声称其 text-extraction path有多项DoS advisory。需在隔离all-extras环境用当前advisory DB和安全PDF corpus复验，不能在cron里处理未知PDF。
- semantic backends可能把docs/PDF/images内容发给第三方。README披露backend/data residency，但 issue #2781指出 outbound secret redaction缺口；对私有shared inbox/curated默认禁止semantic upload。

#### README / docs / release / issues / 源码交叉结论

- README强调code AST local/no LLM；docs同时明确docs/PDF/images会进入configured backend。结论必须按file lane区分，不能笼统说“Graphify完全本地”。
- `SECURITY.md`称graph analysis不网络、仅ingest网络，与README/semantic backend说明存在表述张力；issue #2781也指出该冲突。当前固定源码真实存在多backend依赖与LLM path，因此私有文档数据出口必须按调用链核验。
- Release v0.9.50显示维护高频且多语言/portable identity修复活跃；同时1,108 open issues与每日变更意味着adapter和图schema快速漂移。
- `cache.py`有partial marker、prompt fingerprint、scope-limited cache write；#3093仍报告编排层manifest过早stamp，说明单模块保护不等于pipeline terminal完整。
- `to_json`有总node shrink guard；#3004报告partial source replace可在总数/默认dedup下漏检，说明应升级为per-source identity/coverage比较。

#### 可复用经验

- 当 canonical source会生成图、索引、wiki或摘要时，应优先把每个derived item绑定 `source_file/source_hash/producer/version/confidence`，因为projection可重建且可能有损；边界是provenance不证明抽取完整。
- 当增量抽取可能partial时，应优先在merge前验证每个source的 `attempted/covered/failed/partial + old/new identity overlap`，而不是先删旧projection再看新结果，因为“一条合法node”可能是最危险的半成功；边界是合法删除需要显式tombstone/force。
- 当cache依赖prompt或extractor语义时，应优先把 prompt/config/schema/engine fingerprint纳入key并让partial entry强制miss，因为同内容hash不代表同提取语义；边界是legacy cache只能标unknown vintage。
- 当query从多个graph/workspace选择语料时，应优先在结果头返回canonical graph identity、node count与coverage，因为“回答看起来合理”无法暴露读错库；边界是显示identity仍需host确保用户获准读取。

#### 可尝试实验（30分钟最小demo）

在 `runtime/hermes/github-learning-poc/derived-index-publish-gate/` 做纯Python synthetic fixture：

1. 输入3个source，每个有 `source_id/content_hash/expected_units`；生成old projection。
2. 模拟新抽取的 `complete`、`zero-result`、`partial-one-node`、`same-count-different-id`、`deleted-with-tombstone`。
3. publish gate只有在每source terminal、coverage达到policy、identity churn可解释且artifact schema/hash readback通过时才replace；否则保留旧projection并写`blocked/partial` receipt。
4. 输出 `manifest.json`、`candidate.json`、`publish-receipt.json`；不处理真实私有文档、不调用LLM/backend/network。
5. 验收重点：partial-one-node不能删除旧图；same-count-different-id必须被捕获；显式tombstone可以合法减少。

#### 风险边界

- **License**：GitHub API与`pyproject.toml`识别Apache-2.0，根`LICENSE`是Apache-2.0；仓库另有`LICENSE-MIT`/NOTICE，具体第三方与文件级notice仍需保留。依赖、模型API、输入文档和export资产另行适用条款。
- **维护活跃度**：default branch与release在查询前约一天内更新，Actions近期成功；高活跃也意味着schema/CLI/skill integration持续变化，必须pin commit/tag。
- **安全风险**：semantic文档出域、prompt injection只能减缓、PDF解析DoS、MCP HTTP暴露、live Postgres introspection、URL ingest/SSRF与graph export都扩大authority/data surface。
- **局限性**：本机只跑101个聚焦tests；未跑全套、benchmark、LLM、PDF、media、DB、MCP HTTP、100k-node query、Windows native。README benchmark来自项目自有harness，未在本机复现。
- **已知open gaps**：#3004 partial merge、#3093 failed manifest、#2781 secret redaction、#2658 pypdf DoS均未由本次聚焦测试关闭。
- **不适用场景**：不能把graph.json直接当curated truth；不能无人值守上传私有shared docs；不能把confidence标签当事实真实性；不能用总node count证明coverage。
- **不能自动执行**：不运行`graphify install`，不写Hermes/OpenClaw config或skills，不设置provider key，不启动MCP/HTTP/DB，不扫描shared私有内容，不把候选写curated active fact。

#### ⭐ Skill 升格判断

**需二次验证。** 候选不是Graphify产品skill，而是更窄的agent-neutral `derived-index-publish-gate`：`source identity → attempt/coverage → candidate projection → old/new per-source diff → atomic publish → readback receipt`。源码与issues足够定义failure fixtures，本机101个tests也验证了部分组件，但partial semantic pipeline、secret出口、all-extras与既有governance/verification能力去重尚未完成。今日不创建shared skill、不复制Graphify源码、不写curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/derived-index-publish-gate/{schema.json,gate.py,fixtures/,test_gate.py,README.md}`。
2. **Hermes学习审计**：未来可让`scripts/github_learning_orchestrator.py`对report/project card/lessons/KB copy生成canonical artifact manifest，audit通过后readback hash；本次不改脚本或cron。
3. **shared层级**：`curated/memory/`保持canonical long-term truth；任何graph/wiki/index只放`runtime/hermes/`并标derived，不让Graphify输出覆盖curated。
4. **portable identity**：source用共享根resolver后的相对path + content hash，禁止把宿主绝对路径写进可迁移schema。
5. **OpenClaw边界**：当前runtime不存在，本次不实现、不调用；未来若接入同一agent-neutral fixture，必须由其自身adapter证明source scope、loader与publish readback。

### 2. JuliusBrussee/caveman

- **一句话判断**：值得学的是 Engine把“检测→压缩→计数→先存原文→再发布有损结果”做成确定性包络，并把估计明确标`inferred`；但仓库是split license、关键Go lane本机未编译、真实subscription adapter有open issue，因此不能把高压缩比或175个installer tests外推为Hermes生产可用。
- **解决的问题**：替代把整段log/JSON/search result/skill重复送入模型、只靠prompt要求“简洁”、有损截断后无法找回原文的旧做法。Engine按content type选择compressor，S4有损结果必须有CCR exact-original handle；context packer按BM25+recency+error+priority在token预算内选内容；host wrappers把不同Agent指向local proxy/skills。

#### 基本信息与可验证来源

- URL：https://github.com/JuliusBrussee/caveman
- GitHub API：**Stars 100,943；Forks 5,860；Language Go；License NOASSERTION**。
- 仓库内许可：根`LICENSE`作用域说明 + `LICENSE.BSL` + `LICENSING.md`定义split MIT/BSL-1.1；Engine/Proxy/CacheEngine/Rewriter/Browse/MCP/Shrink/Go mem/shared platform为BSL，skills/CLI/thin SDK/contracts/provider catalog等为MIT。
- API时间字段：`updated_at=2026-08-25T23:25:11Z`，`pushed_at=2026-08-24T23:31:25Z`，open issues `371`，default branch `main`。
- 固定提交：[`81536f57b3303b7de7f5bc5b564cc344f9112d68`](https://github.com/JuliusBrussee/caveman/commit/81536f57b3303b7de7f5bc5b564cc344f9112d68)，提交时间晚于最新stable release，不是release tag。
- Release：[`v2.3.1`](https://github.com/JuliusBrussee/caveman/releases/tag/v2.3.1)，发布于2026-08-23；release notes说明v2.3.0 installer shim仍pin旧版，v2.3.1补了跨bootstrap pin一致性测试。
- Docs：`SECURITY.md`披露proxy/provider/CCR/telemetry/data flow；`docs/WRAP-BENCHMARK.md`披露33.2%为`benchmark_counterfactual`且checkout不含raw harness；`docs/HONEST-NUMBERS.md`明确skill每turn增加约1–1.5k input tokens，短任务可能净负。
- Issues：[#908](https://github.com/JuliusBrussee/caveman/issues/908)、[#895](https://github.com/JuliusBrussee/caveman/issues/895)、[#544](https://github.com/JuliusBrussee/caveman/issues/544) 查询时open。
- 本机验证：Node installer suite 175/175通过；根npm production lock audit 0；本机无Go，Engine/CCR/proxy未编译运行。

#### 架构 / 实现与数据流

```text
Agent / SDK request or tool output
              |
              v
wrapper / local proxy / MCP / CLI
              |
              v
Engine.Detect(input)
json/log/code/diff/search/html/terminal/config/text
              |
              v
safety-classed Compressor
parse/transform -> token count -> smaller?
              |
       +------+------------------+
       | unsafe/no smaller/error | lossy S4
       v                         v
original pass-through       CCR.Store.Put(original)
                                  |
                         durable recovery handle?
                           | yes            | no
                           v                v
                    publish compressed    fail closed/error,
                    result + handle        original remains result

side planes:
- contextwindow.Pack: BM25 + recency + error + priority -> original order
- cacheengine: provider-specific cache metadata, malformed/unknown -> pass-through
- host installers: ownership journal/backups/dry-run/agent-specific payload
- telemetry/provider/CCR/license each有独立boundary
```

核心可迁移模式有五层：

1. **Proposal lane**：detector和compressor提出content type/transform；不确定输入回落到text或pass-through。
2. **Safety lane**：compressor声明safety class；unknown class fail closed，S4必须可recover。
3. **Truth lane**：CCR存exact original，handle content-addressed；压缩projection不是canonical truth。
4. **Accounting lane**：token count basis标`inferred`；project docs区分benchmark_counterfactual、provider-reported与verified。
5. **Adapter lane**：Hermes/Claude/OpenClaw等wrapper各自接config/env/hook/MCP；core contract通过不等于adapter真实route生效，#908正是反例。

#### Repo tree 摘要（固定提交）

```text
caveman/
├── engine/
│   ├── engine.go                 # Detect→Compress→CCR→Result稳定核心
│   ├── detect.go                 # deterministic content router
│   ├── safety/                   # S0-S4 registry与RequiresCCR
│   ├── compressors/              # JSON/log/code/diff/text等纯transform
│   ├── ccr/                      # SQLite/in-memory exact recovery store
│   ├── contextwindow/            # BM25+recency/error/priority packer
│   └── tokens/                   # 本地token counter与basis
├── cacheengine/                  # provider-native cache planner/wire compiler
├── proxy/                        # local gateway、provider adapter、store
├── rewriter/ mcp/ shrink/ mem/   # reflection/recovery/tool surfaces
├── packages/cli/ sdk/ shared/    # MIT adoption/client/contracts层
├── bin/                          # 多Agent installer与ownership journal
├── skills/                       # 20个Agent-facing SKILL.md
├── src/hooks/ plugins/ rules/    # host lifecycle/hook/plugin integration
├── tests/                        # installer/host compatibility tests
├── benchmarks/ evals/ docs/      # measurement与边界说明
├── go.mod / go.sum               # Go 1.26.5及Go dependency closure
├── package.json / package-lock.json
├── LICENSE / LICENSE.BSL / LICENSING.md
└── SECURITY.md
```

固定提交统计：1,388 tracked files、528 Go files、318 JS/MJS/TS files、20 top-level skill manifests。仓库同时包含产品core、installer、镜像与历史consumer copy；不能把一个目录的测试/许可外推到全部。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `engine/engine.go` | stable core API | `Compress/Retrieve/Detect/Stats`；有损先CCR，store失败不publish compressed fields；basis inferred |
| `engine/detect.go` | content routing | strict JSON→terminal→diff→HTML→tabular→code→log→search→config→text；低置信回text |
| `engine/ccr/store.go` | recovery schema | content-addressed handle、typed object、content hash、currentness/lifecycle、exact bytes |
| `engine/ccr/store_sqlite.go` | durable store | 0600、symlink/non-regular拒绝、canonical parent、budget、single writer connection、exact Get |
| `engine/contextwindow/contextwindow.go` | budget pack | BM25 + priority + exponential recency + error boost + pin；按score选、按原顺序返回 |
| `cacheengine/native.go` | provider wire compiler | malformed/record/non-PAYG/caller-managed/profile mismatch/unknown path均保留原bytes |
| `bin/install.js`及`bin/lib/*` | host integration | Hermes等安装、conflict/backup/ownership/uninstall；本次installer suite覆盖 |
| `LICENSING.md` / `SECURITY.md` |采纳边界 | per-directory license；proxy/CCR/telemetry/provider/data flow与保留策略 |

#### ⭐ 源码精读

**代码块 1：`Engine.Compress`——有损结果先存CCR，成功后才publish transform metadata**  
来源：[`engine/engine.go#L63-L139`](https://github.com/JuliusBrussee/caveman/blob/81536f57b3303b7de7f5bc5b564cc344f9112d68/engine/engine.go#L63-L139)

```go
func (e *Engine) Compress(input []byte, opts Options) (Result, error) {
    body, wrappers := unwrapInput(input)
    ct := opts.Type
    if ct == "" { ct = e.Detect(body) }
    before := e.counter.Count(input)
    res := Result{Output: input, ContentType: ct,
        TokensBefore: before, TokensAfter: before,
        TokenCountBasis: e.counter.Name(), Basis: BasisInferred}

    comp, ok := e.registry.For(ct)
    if !ok { return res, nil }
    info, known := safety.Lookup(comp.SafetyClass())
    if !known { return res, nil }
    if info.RequiresCCR && e.store == nil && !opts.ExternalRecovery {
        return res, nil
    }
    out, meta, ok := compressWith(comp, body, opts.Query)
    if !ok || out == nil { return res, nil }
    out = wrappers.rewrap(out)
    after := e.counter.Count(out)
    if after >= before || bytes.Equal(out, input) { return res, nil }

    if info.RequiresCCR && !opts.ExternalRecovery {
        handle, err := e.store.Put(ccr.Recovery{Original: append([]byte(nil), input...)})
        if err != nil { return res, err }
        res.RecoveryHandle = handle
    }
    res.Output, res.TokensAfter, res.Method = out, after, meta.Method
    return res, nil
}
```

逻辑摘要：`res`从完整input初始化，所有未知/失败路径都返回原bytes；只有output更小且S4 original已进入CCR后，才覆盖`res.Output`。这是“canonical先于derived publish”的强示例。边界：`ExternalRecovery=true`把保证委托给host；host若虚报恢复能力就可绕开本地store，必须有adapter conformance test与真实retrieve readback。

**代码块 2：`contextwindow.Pack`——按价值选，按原时序返回**  
来源：[`engine/contextwindow/contextwindow.go#L66-L155`](https://github.com/JuliusBrussee/caveman/blob/81536f57b3303b7de7f5bc5b564cc344f9112d68/engine/contextwindow/contextwindow.go#L66-L155)

```go
func Pack(query string, items []Item, opts Options) Result {
    budget := opts.MaxTokens - opts.ReserveTokens
    bm25 := bm25Scores(query, normalized)
    candidates := make([]candidate, len(normalized))
    for i, item := range normalized {
        score := bm25[i] + item.Priority
        score += opts.RecencyWeight * math.Exp(
            -float64(age)/float64(opts.RecencyHalfLife))
        if errorSignalRe.MatchString(item.Text) { score += opts.ErrorBoost }
        if item.Pin { score += 1_000_000 }
        candidates[i] = candidate{index: i, item: item, score: score}
    }
    sort.SliceStable(candidates, func(i, j int) bool {
        return candidates[i].score > candidates[j].score
    })
    // fit by budget ...
    sort.SliceStable(selected, func(i, j int) bool {
        return selected[i].index < selected[j].index
    })
    return Result{Items: out, TokensUsed: used,
        TokensBefore: tokensBefore, TokensSaved: max(0, tokensBefore-used),
        DeferredCount: len(items)-len(out)}
}
```

逻辑摘要：selection order与presentation order分开：先用BM25/priority/recency/error/pin找高价值项，装入token预算后按原index恢复时序。这比“直接截最后N条”更适合Agent上下文。边界：英文style stopwords、heuristic error regex、greedy knapsack与token counter basis会影响结果；`DeferredCount`不描述被省略的关键coverage，仍需保留可恢复ID和reason。

**代码块 3：`Store.Put`——content-addressed exact original + budget-before-publish**  
来源：[`engine/ccr/store_sqlite.go#L351-L389`](https://github.com/JuliusBrussee/caveman/blob/81536f57b3303b7de7f5bc5b564cc344f9112d68/engine/ccr/store_sqlite.go#L351-L389)

```go
func (s *Store) Put(rec Recovery) (string, error) {
    handle := Handle(rec.Original)
    unchanged, err := s.recoveryUnchanged(handle, rec)
    if err != nil { return "", fmt.Errorf("ccr put: %w", err) }
    if unchanged { return handle, nil }
    if err := s.checkRecoveryBudget(
        handle, int64(len(rec.Original)+len(rec.Metadata))); err != nil {
        return "", fmt.Errorf("ccr put: %w", err)
    }
    _, err = s.db.Exec(`INSERT INTO recoveries ... ON CONFLICT(handle) DO UPDATE ...`,
        handle, time.Now().UTC().Format(time.RFC3339Nano),
        rec.ContentType, rec.Compressor, rec.TokensBefore,
        rec.TokensAfter, rec.Original, rec.Metadata)
    if err != nil {
        if isFull(err) { return "", fmt.Errorf("ccr put: %w", ErrBudgetExceeded) }
        return "", fmt.Errorf("ccr put: %w", err)
    }
    return handle, nil
}
```

逻辑摘要：handle由original SHA-256截取形成，重复内容幂等；先算逻辑retained-byte budget，再写SQLite；budget/DB失败返回error，让上层保持原文。store open还会resolve parent、拒绝symlink/non-regular、chmod 0600并限制单writer connection。边界：本地文件权限不是加密，同一OS account可读；handle截断哈希用于identity而非签名；没有Go toolchain，本次未运行并发/race/budget fixtures。

#### 依赖分析与供应链风险

- 根`go.mod`要求**Go 1.26.5**；直接依赖包括chromedp/CDP、pgx、MinIO、SQLite、tree-sitter、tokenizer、x/crypto/net/sys、yaml等，覆盖browser/database/object-store/native parsing/network，authority surface很宽。
- modernc SQLite、tree-sitter、chromedp、compression与provider proxy需要分别审compile flags、platform制品与transitive license；`go.sum`锁hash不等于advisory clean。
- 根npm installer `package.json`本身为MIT，Node>=18，唯一声明dependency是`@caveman-ai/cli ^1.1.0`；`npm audit --omit=dev --package-lock-only`返回0，但metadata只显示很窄的prod closure，不能覆盖Go runtime。
- release notes另pin `bin-v1.1.3` companions和CLI 1.2.4；源HEAD、stable tag、npm range与36个binary assets不是同一artifact identity，采用时必须逐项digest/signature/readback。
- split license是第一优先边界：Engine/CCR/contextwindow等本文深读模式位于BSL区域。可以独立抽象工程原则，但不得复制到shared并误称MIT；第三方hosted/managed/embedded use需要商业许可，具体法律适用仍需专业核验。
- Dependabot disabled/403；未运行`govulncheck`、Go tests/race/fuzz或binary SBOM，Go dependency advisories全部待核验。

#### README / docs / release / issues / 源码交叉结论

- `engine.go`明确CCR失败不publish有损结果；SECURITY也称lossy transform在durable recovery不可用时pass-through。这个core契约很强。
- Issue #908显示Claude subscription/OAuth adapter即使proxy可达也不进入eligible compression，MCP marker与doctor判断不一致；说明core正确不等于真实host route有效，必须测请求计数、eligible、recovery与retrieve。
- `docs/WRAP-BENCHMARK.md`给出33.2% provider-reported input reduction与18/18 exact checks，但同文明确checkout没有raw harness/run artifacts，无法从当前repo独立复现；HTML case还是-9.9%。因此只可称pinned benchmark report，不是通用收益。
- `docs/HONEST-NUMBERS.md`明确纯response skill增加约1–1.5k input tokens/turn，短/本就简洁的任务可能净负；不能把Engine input compression与skill output style混为一个数字。
- Release v2.3.1本身修的是v2.3.0 installer pin drift，说明source、shim、package、binary版本一致性必须由test保护；“文档写v2.3.0”不代表实际pipe-to-shell安装该版本。
- Issue #895表明Hermes skill scanner可能隔离`caveman-compress`；本机installer tests通过“文件落在fake Hermes目录”不代表当前Hermes loader会信任并加载该skill。
- Issue #544指出一个skill mutation path曾在validate前覆盖live file；即便Engine core先CCR，Agent-facing文件rewrite仍需独立staging/atomic replace contract。

#### 可复用经验

- 当任何压缩/摘要会删除原始细节时，应优先先持久化exact original并验证retrieve handle，再发布derived output，因为“模型大概率不需要”不是不可逆删除授权；边界是store必须有scope、retention、encryption与budget策略。
- 当detector或compressor不确定、解析失败或结果不更小时，应优先返回原bytes并声明no-op，而不是强行生成看似更短的结果，因为错误压缩成本高于未节省token；边界是pass-through仍会消耗预算。
- 当按相关性装配上下文时，应优先把selection ranking与chronological presentation分开，并返回deferred count/recovery IDs，因为按score重排会破坏事件顺序；边界是greedy ranking仍可能漏关键依赖。
- 当跨Agent wrapper声称能力可用时，应优先验证真实request route、eligible decision、artifact/store readback和retrieve，而不是只检查installer marker或status prose，因为#908展示了“安装成功但数据面没生效”；边界是测试必须不泄露provider credential。
- 当GitHub API license为NOASSERTION且仓库按目录split license时，应优先以per-directory canonical license map决定可复制范围，因为根badge或package.json不能覆盖Engine-linked code；边界是法律判断需人工/专业审查。

#### 可尝试实验（30分钟最小demo）

在 `runtime/hermes/github-learning-poc/recoverable-projection-envelope/` 写零第三方依赖Python fixture，不复制BSL源码：

1. `propose(raw)`只产生synthetic shortened view、method与omitted unit IDs。
2. host用SHA-256 content ID把raw写到temp SQLite/JSON store，readback bytes/hash一致后才publish projection。
3. 注入`store_missing/store_full/write_error/not_smaller/unknown_type/retrieve_miss`，预期均pass-through或blocked，绝不发布无recoverable handle的derived view。
4. `pack()`使用简单fixture score选择，但最终按原sequence输出，receipt列selected/deferred IDs与coverage。
5. 不使用Caveman代码，不连接proxy/provider/MCP，不安装skill，不改Hermes config。

#### 风险边界

- **License**：GitHub API为NOASSERTION；仓库实际split MIT + BSL-1.1。本文深读的Engine/CCR/contextwindow/cacheengine是BSL范围；只抽象原则，不复制实现。依赖、binary assets、font、商标另有notice。
- **维护活跃度**：main在查询前约一天内pushed；latest stable release早两天。更新快，但HEAD不等stable artifact，且371 open issues。
- **安全风险**：local proxy转发provider credential/content；CCR可能存prompts/credentials/tool results且未加密；telemetry默认opt-out；MCP/browser/hooks/plugins/installers扩大network/config/effect面。
- **局限性**：本机无Go，核心Engine完全未编译运行；175 pass只证明installer/host fixtures，不证明compression、CCR、proxy或provider traffic；npm audit只覆盖窄root package。
- **真实adapter gap**：#908报告subscription/OAuth不eligible与MCP recovery状态漂移；#895报告Hermes quarantine；#544报告live-file mutation window。不能把源码contract外推为当前Hermes可用。
- **收益边界**：pinned benchmark不可从checkout独立复现，包含负收益HTML case；skill固定prompt overhead可能净负；所有inferred token saving都不是provider invoice。
- **不适用场景**：多租户remote proxy、第三方managed/embedded服务、需要强加密retention、无人值守改写shared truth、只按marker判断成功的工作流。
- **不能自动执行**：不运行`curl|bash`、不`npm install -g`、不下载release binary、不启动proxy/MCP/browser、不读取provider credential、不修改Hermes或OpenClaw config/skills/cron/auth/env。

#### ⭐ Skill 升格判断

**暂不沉淀。** `recoverable-projection-envelope`的抽象有价值，但与现有verification-first、completion receipt、source-outcome、canonical-derived layer候选高度重叠；关键实现位于BSL区域，本机Go lane blocked，Hermes loader与subscription adapter还有open gaps。优先做独立无依赖fixture并评估“更新既有verification workflow”而非新建skill。今日不安装Caveman、不创建Hermes local skill/shared skill、不复制上游源码。

#### Hermes / shared hub 落地路径

1. **仅runtime实验**：`runtime/hermes/github-learning-poc/recoverable-projection-envelope/`，schema和实现必须独立、agent-neutral、无BSL代码复制。
2. **Hermes工具输出**：候选给长stdout/report projection附`raw_artifact_id/raw_hash/method/coverage/truncated/recoverable/terminal`；model不能自行声明recoverable，host必须readback。
3. **shared hub分层**：canonical raw研究在`inbox/hermes/daily/`；大raw/cache/POC留`runtime/hermes/`；只有治理审查后的稳定原则才可进入curated或shared skill。
4. **知识库projection**：KB copy是derived human view，未来可附source report hash；KB存在不反向证明inbox源完整。
5. **OpenClaw边界**：runtime不存在，本次不调用；未来adapter若复用schema，必须自行验证loader、route、store、retrieve、license与secret隔离。

## 经验沉淀

1. 当canonical source要生成图、摘要、压缩视图或知识库副本时，应优先让derived artifact绑定source identity/hash、producer/version、coverage和terminal receipt，因为projection随时可能partial或stale；边界是可追溯不等于事实正确。
2. 当增量更新会替换旧projection时，应优先先验证per-source coverage、old/new identity overlap与显式tombstone，再atomic publish，因为总node count相同也可能全部换成错误身份；边界是合法大重构需要人工或policy override。
3. 当有损压缩、截断或context packing发生时，应优先先持久化exact original并验证retrieve，再展示short view，因为没有恢复路径的“节省”是不可逆数据损失；边界是原文store含敏感数据，必须做scope/retention/encryption治理。
4. 当cache依赖prompt、schema、extractor或policy时，应优先把这些fingerprint纳入key，并让partial/unknown-vintage cache强制miss或告警，因为content hash只证明输入字节没变；边界是重算成本需显式预算。
5. 当跨host installer或adapter报告success时，应优先验证数据面route、effect/readback、ownership journal与uninstall receipt，因为marker/config写入成功不证明能力真正加载；边界是测试必须使用fake home或隔离scope。
6. 当开源仓库顶层license是NOASSERTION或按目录split时，应优先逐文件/目录读取canonical license map，只抽象机制而不复制高风险实现，因为README badge和GitHub API都可能不足；边界是最终合规需人工/专业审查。
7. 当本机只跑了窄测试或缺关键toolchain时，应优先明确“该lane待核验”，不能用上游Actions、README benchmark或另一语言的绿色suite替代；边界是blocked仍应给最小复验命令与固定commit。
8. 当私有docs、logs或memory可能送往semantic backend时，应优先默认local-only/deny，并在明确consent后才允许按file lane出域，因为secret redaction只能降低已知泄漏而不能保证无敏感内容；边界是图片/压缩包/未知格式更难可靠redact。

### 今日可尝试的统一实验

优先实现`runtime/hermes/github-learning-poc/derived-index-publish-gate/`，把Graphify的per-source coverage问题与Caveman的“先存canonical再publish derived”原则合并：candidate projection只在source terminal、coverage/identity gate、atomic write和readback全部通过后替换旧projection；失败保留旧版本并输出`blocked/partial/needs_verification`。实验只用synthetic fixtures，不连接provider/MCP/DB server，不改config/cron/skills/curated。

## Skill 升格总判断

- `Graphify-Labs/graphify`：**需二次验证**。只抽象`derived-index-publish-gate`，先做per-source partial/same-count-churn/tombstone fixtures，并与shared governance、verification-first、path-portability去重。
- `JuliusBrussee/caveman`：**暂不沉淀**。split BSL、Go lane blocked、Hermes quarantine与真实adapter issue使其不足以直接skill化；只在runtime独立验证recoverable projection原则。
- 今日不创建`capabilities/skills/`，不更新shared skill manifest，不写curated active facts。候选反哺不代表已落库。

## 明日继续

1. 用30分钟实现`derived-index-publish-gate` synthetic POC，至少覆盖complete、zero、partial-one-node、same-count-different-id、explicit tombstone、atomic write failure与readback mismatch。
2. 追踪Graphify #3004/#3093是否出现merged fix/test；固定新commit后做源码diff与最窄regression fixture，不处理私有语料。
3. 在隔离Graphify all-extras export上运行requirements-level audit，核验`pypdf 6.13.3`与当前fix版本；不打开未知PDF，不将安全issue正文当本机复现。
4. 若环境获得Go 1.26.5，先运行Caveman最窄`engine/ccr`、`engine/contextwindow`与`cacheengine`tests/race；在此之前保持core runtime待核验。
5. 对当前Hermes loader只做read-only能力盘点，判断是否已有canonical/derived/recovery receipt契约；不自动安装Caveman/Graphify或改Hermes配置。

## 候选反哺

### Candidate Facts

- [ ] topic: derived graph/index不能替代canonical source，publish必须绑定per-source coverage与identity churn | evidence: `Graphify-Labs/graphify@43d54ac`的`extract.py/cache.py/build.py/export.py`与open issues #3004/#3093 | 建议: create candidate only | 安全级别: medium
- [ ] topic: 有损projection必须先存exact original并验证recovery，再publish short view | evidence: `JuliusBrussee/caveman@81536f5`的`engine/engine.go`与`engine/ccr/store_sqlite.go` | 建议: create candidate only / 与verification候选去重 | 安全级别: high
- [ ] topic: GitHub API NOASSERTION必须下钻per-directory license map | evidence: Caveman API license NOASSERTION与`LICENSE`/`LICENSE.BSL`/`LICENSING.md` split scope | 建议: update governance candidate | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: derived-index-publish-gate | 可复用场景: shared runtime index、memory graph、learning KB projection、artifact summary | 是否建议 shared: yes（仅二次验证后） | 原因: 跨Agent可复用，但需per-source fixtures、portable identity与atomic/readback契约
- [ ] 名称: recoverable-projection-envelope | 可复用场景: tool output truncation、context packing、摘要/压缩 | 是否建议 shared: no（当前） | 原因: 与verification/completion/canonical-derived候选重叠，且上游参考实现为BSL、关键lane未实测

### Candidate Open Questions

- [ ] 问题: Graphify #3004/#3093在v0.9.50后分别由哪个pipeline owner修复，是否已有per-source terminal/manifest regression test？ | reason: gap | priority: high
- [ ] 问题: shared hub当前哪些runtime projection已有source hash、coverage、old/new identity diff和atomic publish receipt？ | reason: adaptation | priority: high
- [ ] 问题: Hermes现有工具是否能为truncated output提供host-stamped raw artifact ID与readback，而不只返回文本pointer？ | reason: gap | priority: high
- [ ] 问题: Caveman #908的adapter route/MCP marker状态是否已在later commit修复，Hermes wrapper是否有独立conformance fixture？ | reason: stale/gap | priority: medium
- [ ] 问题: Graphify all-extras当前advisory closure及PDF subprocess/resource-cap结果是什么？ | reason: blocked | priority: medium

### 不应自动落地

- 不安装、启动或配置Graphify/Caveman，不运行第三方`curl|bash`、global npm installer、release binary、proxy、MCP、browser或DB integration。
- 不调用OpenClaw；当前runtime不存在。
- 不自动改Hermes/OpenClaw config、model、provider、cron、auth、env、skills或secret。
- 不扫描/上传shared私有docs、curated memory或用户文件到semantic backend。
- 不复制Caveman BSL实现，不把NOASSERTION简写为MIT，不把候选直接写成curated active fact。
- 不把Stars、上游Actions、README benchmark、聚焦tests、npm audit 0或schema-valid结果外推为生产安全/完整/高收益。
