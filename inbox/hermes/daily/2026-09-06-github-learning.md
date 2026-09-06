---
type: case
status: archived
created: 2026-09-06
updated: 2026-09-06
domain: learning
tags: [github-learning, retrieval, shell, lifecycle, verification]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
  - "[[03-学习/技术实践/00-技术实践索引]]"
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-09-05-GitHub热门项目学习日报]]"
---

# 2026-09-06 GitHub 热门项目学习报告

> 执行者：Hermes（OpenClaw 运行时不存在；本次未调用 OpenClaw）  
> 查询窗口：2026-09-06 07:30–07:42（UTC+08:00）  
> 发现方法：真实抓取 GitHub Trending daily HTML，解析出 16 个项目；项目速览的 Stars、Forks、Language、License、`updated_at`、`pushed_at` 均由 GitHub Repository API 逐仓核验。Trending 只用于发现，不把 “stars today” 当总 Stars。  
> 深读固定提交：`ruvnet/ruflo@277c7bc03ad192eef6d6f57e59ab7bab69a5728d`；`nvm-sh/nvm@ccb49e5cd07e3a73850a1e1d36e666297ced9018`。动态热度快照与固定源码 revision 分开记录。  
> 证据位置：`runtime/hermes/github-hot-project-learning/evidence/2026-09-06/`；源码浅克隆只在 `/tmp`，未写入 shared runtime。

## 今日结论

**今天最值得迁移的共同模式是“把隐含质量假设变成可拒绝、可降级、可复验的确定性边界”：Ruflo 的检索链将 embedding 只留在内部管道，以有限值/维度检查决定 cosine 或 lexical fallback，并用基准暴露 relevance-diversity trade-off；nvm 则用逐版本锁、完整 staging、目录替换和结构校验把并发安装与半安装从 happy-path 脚本升级为恢复协议。两者也共同证明：绿测试、README 宣称或仓库热度都不能替代供应链、制品与实际执行环境的证据。**

### 今日真实验证摘要

- `ruvnet/ruflo`：固定 HEAD 后 `npm ci --ignore-scripts` 安装 805 packages，因 `undici@8.10.0` 要求 Node `>=22.19.0` 而本机为 `v22.14.0`，npm 给出 `EBADENGINE`；安装仍完成。执行 `smart-retrieval.test.ts + mmr-benchmark.test.ts`，真实结果 **2 files / 18 tests passed / 0 failed**。
- Ruflo 基准在同一 18-doc / 6-topic synthetic corpus 上真实输出：默认 `lambda=0.7` 时 candidate 与 lexical baseline 的 Recall@6、nDCG@6 相同（1.0 / 0.777357），topic diversity 从 0.472222 提升至 0.666667，duplicate rate 从 0.288889 降至 0.2；但 `lambda=0.3/0.5` 时 candidate Recall@6 降到 0.333333。因此不能把 embedding MMR 写成无条件更优。
- Ruflo `npm audit --json` 命中 **12（9 high / 3 moderate）**；直接命中包含 `agentdb`、`agentic-flow`、`ajv`、`express`、`fast-uri`、`toml`。Repository security advisories API 返回 1 条公开 advisory：`GHSA-c4hm-4h84-2cf3 / CVE-2026-59726`，影响 `<3.16.3`；当前根 package `3.38.21` 高于 patched version，但仍须按实际安装树核验。
- `nvm-sh/nvm`：固定 HEAD 后 `bash -n nvm.sh install.sh nvm-exec` 成功；在正确测试工作目录直接执行三项 upstream fixture：`nvm_acquire_install_lock`、`nvm_install_binary_extract self-heals a broken version dir`、`nvm_validate_install`，均 exit 0。
- nvm 先尝试通过 Makefile/Urchin 执行定向测试，但初次因 dev tools 未安装而 blocked；`npm install --ignore-scripts` 后发现 Urchin 只接受目录，不接受单文件，故改为在测试目录直接执行原 fixture。依赖安装审计真实命中 **20（1 critical / 10 high / 9 moderate）**，全部属于 dev graph；随后删除 `node_modules` 与未跟踪 lockfile，浅克隆恢复 clean。
- nvm Security Advisories API 返回 3 条已披露 advisory：`CVE-2026-15921`（patched `v0.40.6`）、`CVE-2026-10796`（patched `0.40.5`）、`CVE-2026-1665`（patched `0.40.4`）；固定 HEAD/最新 release 版本均为 `0.40.7`。这不等于未知漏洞为零。
- 两仓 Dependabot alerts API 均返回 403（Ruflo disabled；nvm 无权）；不得据此声称没有未修依赖漏洞。Ruflo 的 source-only witness open issue #3189、nvm 的 source patch open issue #3114 均只作为边界证据，未把 issue 作者声明冒充本机复现。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | 252,547 | 21,314 | Shell | MIT | 2026-09-04T08:45:43Z | Trending；8 月 22 日已深读，避免重复 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 249,847 | 37,611 | JavaScript | MIT | 2026-09-05T21:47:27Z | 高热 Agent harness；8 月 19 日已深读 |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 241,982 | 49,715 | Python | MIT | 2026-09-05T23:31:18Z | 当前 Hermes 上游；历史已深读 |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | 204,664 | 26,699 | TypeScript | MIT | 2026-09-05T23:29:29Z | 8 月 25 日已深读 durable session/reconcile |
| [anthropics/skills](https://github.com/anthropics/skills) | 174,544 | 20,670 | Python | **NOASSERTION** | 2026-09-03T16:37:14Z | skill 参考；API 未识别仓库级 license，不复制 |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 127,893 | 6,842 | JavaScript | MIT | 2026-09-04T12:35:29Z | 昨日已深读 canonical adapter 与 session scope |
| [nvm-sh/nvm](https://github.com/nvm-sh/nvm) | 94,910 | 10,424 | Shell | MIT | 2026-09-04T22:40:55Z | **深读：逐版本锁、staging replacement、结构校验** |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | 70,686 | 8,413 | TypeScript | MIT | 2026-09-05T15:57:31Z | **深读：检索 MMR、内部 evidence、benchmark honesty** |
| [fmtlib/fmt](https://github.com/fmtlib/fmt) | 25,567 | 3,043 | C++ | MIT | 2026-09-05T22:40:31Z | 成熟库；与今日 Agent/恢复主线较弱 |
| [BraveOPotato/FckSignups](https://github.com/BraveOPotato/FckSignups) | 2,871 | 198 | TypeScript | GPL-3.0 | 2026-08-22T01:59:09Z | 高风险自动化且 GPL；不在无人 cron 执行 |

> API 查询时 Stars 是动态快照；License 是 repository API 识别的根 SPDX，不覆盖子目录、依赖、模型、数据或 release asset。`open_issues_count` 包含 PR，不能直接当 issue 数。速览只做元数据判断，未对非深读仓做源码能力声明。

## 深读项目

### 1. ruvnet/ruflo

- **一句话判断**：值得学的是它把一次 self-evolution 改动绑定到 frozen hypothesis、实际 production path、counterexample、参数 sweep 与诚实的负面结果；但仓库巨大、alpha 依赖多、公开安全/制品验证缺口仍在，不适合把整个框架直接引入 Hermes。
- **解决的问题**：替代“只按语义相关性返回同义重复”“把 embedding 用于初排后丢弃”“用 token overlap 代理语义去重”“只报告有利参数”“把内部向量顺手输出给 CLI/MCP”的旧做法。
- **URL / API 快照**：https://github.com/ruvnet/ruflo ；**Stars: 70,686 / Forks: 8,413 / Language: TypeScript / License: MIT**；`updated_at=2026-09-05T23:26:10Z`，`pushed_at=2026-09-05T15:57:31Z`，repository API `open_issues_count=929`（含 PR），default branch `main`。
- **固定提交**：[`277c7bc03ad192eef6d6f57e59ab7bab69a5728d`](https://github.com/ruvnet/ruflo/commit/277c7bc03ad192eef6d6f57e59ab7bab69a5728d)，committer time `2026-09-05T15:57:23Z`，提交为 `dream(memory): #3168 wire embedding-cosine into SmartRetrieval's MMR step (evaluated, ACCEPT) (#3169)`。
- **Release / issue 证据**：latest release [`v3.38.21`](https://github.com/ruvnet/ruflo/releases/tag/v3.38.21)，发布于 `2026-09-02T13:40:40Z`，修复 HTTP MCP bridge 重启后 memory path 不一致；release notes 同时明确 standalone `@claude-flow/mcp@3.0.0-alpha.10` 未发布这一 known gap。open issue [#3189](https://github.com/ruvnet/ruflo/issues/3189) 说明 source-only checkout 无 `dist/` 时 witness 验证全 missing；[#3208](https://github.com/ruvnet/ruflo/issues/3208) 记录一次 rerun 后 assertion evidence 丢失，具体 flake 根因仍是 hypothesis，**待核验**。
- **来源交叉核验**：README、`SECURITY.md`、latest release、issues #3189/#3208、固定源码、package manifests、GitHub advisories API、本机锁定安装、18 个定向 tests 和 npm audit。

#### 架构 / 实现与数据流

```text
query
  -> template expansions（最多约 3 个）
  -> caller-provided SearchFn（HNSW / AgentDB / sql.js / test fake）
  -> per-variant ranked candidates
  -> Reciprocal Rank Fusion（跨 variant 去重融合）
  -> recency boost（可关闭）
  -> bounded fanOut truncation
  -> MMR: relevance - semantic duplication
       embedding finite + same dimension -> cosine
       missing / empty / NaN / Infinity / mismatch -> token Jaccard fallback
  -> session round-robin
  -> final result + stage counts / duration

CLI memory-initializer:
query embedding -> RaBitQ shortlist -> SQLite exact vector -> cosine score
                -> internal SearchCandidate.embedding
                -> smartSearch/MMR
                -> CLI/MCP field whitelist（不输出 embedding）
```

`smart-retrieval.ts` 不拥有数据库或模型：`SearchFn` 注入 raw search，管道只处理排序；这是可测的 pure-ish decision layer。`memory-initializer.ts` 在本来就计算 exact cosine 的位置保留向量，避免为了 MMR 重算；输出 adapter 用字段白名单阻止 embedding 离开内部面。MMR 不是独立“分数修正”，而是逐项选择：首项取 top relevance，后续每轮在剩余项中最大化 `lambda * relevance - (1-lambda) * maxSimilarity(selected)`。

#### repo tree 摘要

固定 commit `git ls-files` 为 **5,628 tracked paths**；去掉 git 元数据与本机 `node_modules` 后实查主要文件分布为 `v3/ 3,494`、`plugins/ 623`、`ruflo/ 556`、`.claude/ 371`、`docs/ 195`、`.agents/ 144`、`scripts/ 108`：

```text
ruvnet/ruflo/
├── v3/
│   ├── @claude-flow/memory/       # retrieval、backend、benchmark、tests
│   ├── @claude-flow/cli/          # CLI/MCP adapters 与 memory-initializer
│   ├── @claude-flow/security/     # 输入、credential、安全模块
│   ├── @claude-flow/swarm/        # coordination/consensus
│   └── docs/adr/                  # 大量机制决策记录
├── plugins/                       # plugin surfaces 与 witness scripts
├── ruflo/                         # 发布/运行相关 package tree
├── .claude/ + .agents/            # host instruction/agent/skill 表面
├── docs/dream-cycle/              # 每轮假设、评测、接受/拒绝、风险记录
├── verification/                  # 跨平台 manifest/witness 验证层
├── package.json                   # root release package 与 overrides
├── package-lock.json              # npm 锁文件
├── pnpm-lock.yaml                 # v3 workspace 锁文件
└── SECURITY.md / LICENSE          # security policy / MIT
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `v3/@claude-flow/memory/src/smart-retrieval.ts` | 可插拔检索决策管道 | expansion → RRF → recency → bounded MMR → session diversity；返回逐阶段统计 |
| `v3/@claude-flow/cli/src/memory/memory-initializer.ts` | store adapter | RaBitQ shortlist 与 sql.js fallback 都可把已经消费的 embedding 传入内部 candidate |
| `v3/@claude-flow/memory/src/smart-retrieval.test.ts` | adversarial unit fixtures | 覆盖 embedding、缺失/维度不匹配、NaN/Infinity、空向量、确定性及 CLI/MCP 不泄漏 |
| `v3/@claude-flow/memory/src/mmr-benchmark.test.ts` | baseline/candidate benchmark | 18 docs / 6 topics，遍历 lambda 0.3/0.5/0.7/0.9，评估 recall、nDCG、diversity、duplicate、latency |
| `docs/dream-cycle/dream-gist-2026-09-05.md` | 自进化审计记录 | 公开 baseline/candidate、负面结果、reward-hack check、安全扫描与未处理 gap |
| `verification/README.md` | 制品 witness 契约 | 解释 unit test 与 fresh install/release surface 不同，并记录 witness 层用途 |
| `package.json` + `v3/package.json` | 依赖/工作区边界 | root release 3.38.21；v3 是 `3.0.0-alpha.1` monorepo，Node >=20，pnpm 8.15；多重 overrides |

#### ⭐ 源码精读

**代码块 1：`smartSearch()` 将每阶段显式化，并在 MMR 前约束候选量。**

```ts
export async function smartSearch(
  search: SearchFn,
  opts: SmartSearchOptions
): Promise<SmartSearchResult> {
  const limit = opts.limit ?? 10;
  const fanOutK = opts.fanOutK ?? Math.max(limit * 3, 20);
  const variants = opts.multiQuery !== false
    ? (opts.queryExpansions ?? defaultQueryExpansions)(opts.query)
    : [opts.query];

  const ranked: SearchCandidate[][] = [];
  for (const v of variants) {
    ranked.push((await search({ query: v, limit: fanOutK })).results);
  }
  let scored = ranked.length === 1
    ? ranked[0].map(candidate => ({ candidate, score: candidate.score }))
    : reciprocalRankFusion(ranked, opts.rrfK ?? 60);
  if (scored.length > fanOutK) scored = scored.slice(0, fanOutK);
  scored = mmrRerank(scored, opts.mmrLambda ?? 0.7,
    Math.min(limit * 2, scored.length));
  // sessionRoundRobin + stats + final slice
}
```

逻辑摘要：raw store 被接口隔离；每阶段可关闭、可统计，昂贵的二次排序只看 bounded fanout。边界：expansion 仍是英文模板/token 规则，跨语言效果没有在今日证据中验证；串行 fan-out 的延迟与失败语义也需另测。

**代码块 2：`mmrRerank()` 逐轮平衡相关性与已选集合最大相似度。**

```ts
function mmrRerank(scored: Scored[], lambda: number, limit: number): Scored[] {
  const selected: Scored[] = [];
  const remaining = [...scored];
  const first = remaining.shift()!;
  selected.push(first);

  while (selected.length < limit && remaining.length > 0) {
    let bestIdx = -1;
    let bestMmr = -Infinity;
    for (let i = 0; i < remaining.length; i++) {
      const cand = remaining[i];
      const maxOverlap = maxSimilarityAgainstSelected(cand, selected);
      const mmr = lambda * cand.score - (1 - lambda) * maxOverlap;
      if (mmr > bestMmr) { bestMmr = mmr; bestIdx = i; }
    }
    if (bestIdx < 0) break;
    selected.push(remaining.splice(bestIdx, 1)[0]);
  }
  return selected;
}
```

逻辑摘要：不是把 duplicate 标成 boolean，而是让每个候选和当前已选集合比较；lambda 是策略，不是普适常数。边界：上段为忠实压缩片段，真实源码用 `selectedTokens/selectedEmbeddings` 避免重复构建 selected 特征；复杂度仍近似 `O(limit * fanOut * selected)`，大 fanout 必须限额。

**代码块 3：`pairSimilarity()` 对无效向量降级，不让 NaN 毒化选择循环。**

```ts
function pairSimilarity(
  embA: number[] | undefined,
  embB: number[] | undefined,
  tokensA: Set<string>, tokensB: Set<string>
): number {
  if (isWellFormedEmbedding(embA) &&
      isWellFormedEmbedding(embB) &&
      embA.length === embB.length) {
    return cosineSimilarity(embA, embB);
  }
  return jaccard(tokensA, tokensB);
}

function isWellFormedEmbedding(emb: number[] | undefined): emb is number[] {
  return Array.isArray(emb) && emb.length > 0 &&
    emb.every(v => typeof v === 'number' && Number.isFinite(v));
}
```

逻辑摘要：缺向量、空数组、维度不一致、NaN/Infinity 都走 lexical fallback；这是显式 degraded path，而不是返回空结果或静默中断。边界：fallback 保可用，不保证跨语言/同义改写的去重质量；向量 model/revision 兼容性也未被这个函数检查。

**代码块 4：`searchEntries()` 复用已有向量，但把它声明为 internal plumbing。**

```ts
export async function searchEntries(options: {
  query: string; namespace?: string; limit?: number; threshold?: number;
  provenanceFilter?: string[];
}): Promise<{ success: boolean; results: Array<{
  id: string; key: string; content: string; score: number;
  namespace: string; provenanceType?: string; embedding?: number[];
}>; searchTime: number; error?: string }> {
  const queryEmbedding = (await generateEmbedding(options.query)).embedding;
  const rabitqCandidates = await searchRabitq(queryEmbedding, { k: limit * 2 });
  // 从 SQLite 取 embedding，算 exact cosine，并把 parsedEmbedding 留给内部 MMR
}
```

逻辑摘要：`provenanceFilter` 先做 enum 校验；RaBitQ 只负责 shortlist，SQLite 向量重算 exact cosine，且 embedding 不由此接口直接承诺给终端用户。边界：源码对 `JSON.parse` 失败只 skip；数据库加密、namespace/provenance authority 与 embedding model identity 属于更外层契约，今日未完整动态复现。

#### 依赖分析与供应链风险

- root `package.json` 直接依赖包含 `@claude-flow/*` alpha packages、`agentdb` alpha、`agentic-flow`、`@ruvector/rabitq-wasm`、`express`、`ws`、`zod`、`semver`；optional 包含 native/keyring/SQLite/ONNX 相关能力。`overrides` 面很大，说明 resolved graph 与单个 manifest 不等价。
- `v3/@claude-flow/memory/package.json` 的运行依赖为 `@claude-flow/security ^3.0.0-alpha.12`、`agentdb ^3.0.0-alpha.17`、`sql.js ^1.10.3`，optional `better-sqlite3 ^12.9.0`；其版本 `3.0.0-alpha.23`，发布 tag `v3alpha`。
- 本机锁图 `npm audit` 为 12 条；这是 advisory 命中，不证明每条可从今日 MMR 路径达到，但明确阻止“依赖安全”结论。依赖安装时还有 Node engine mismatch，完整 workspace/build 未运行。
- 最新 release notes 主动披露某 standalone alpha package 未发布；这说明 monorepo source install、npm end-user tarball 与 release tag 是三种不同制品面，不能互相代替验证。

#### 可复用经验

- 当检索结果充满同义重复时，应优先复用初排已经生成的 embedding 做 bounded MMR，并保留 lexical fallback，因为重新调用模型浪费成本、直接丢向量会让 diversity 退化；边界是必须按真实 corpus 调 lambda，不能默认“更分散就是更好”。
- 当数值 evidence 进入排序或决策时，应优先校验 finite、非空、维度和 model/revision compatibility，再选择明确 degraded path，因为 NaN 可让比较循环静默失效；边界是 fallback 只保证流程可继续，不保证质量等价。
- 当内部检索需要敏感/大体积特征而外部只需结果时，应优先在内部 schema 传递并由 CLI/MCP adapter 使用 allowlist projection，因为“接口当前没打印”不是不泄漏契约；边界是每个出口都要 conformance fixture。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/retrieval-diversity-gate-v0/` 做纯 Python 离线 fixture：用 6 条候选模拟“同义重复 + 不同主题”，实现 `finite/dimension/model_revision gate -> cosine MMR / lexical fallback`，遍历 lambda 0.3/0.7/0.9，并输出 `recall/diversity/duplicate/degraded_reason`。不读取真实 curated、不调用模型、不引入 Ruflo 源码；只有在默认 shared retrieval corpus 上同时满足 recall floor 与 duplicate 改善，才提出集成建议。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 MIT；只可抽象机制。第三方依赖、plugins、模型、数据与发布制品需独立审计。
- **维护活跃度**：10 个最近 commit 跨 `2026-08-30T13:47:11Z` 至 `2026-09-05T15:57:23Z`，当前活跃；高频改动、alpha 包和 929 aggregate open issue/PR 同时意味着稳定性成本高。
- **安全风险**：公开 advisory 记录旧版默认 Docker MCP bridge unauthenticated RCE；当前版本高于 patched version，但无人值守安装前仍要核实际 resolved version、绑定地址与 auth。Dependabot 不可读；npm audit 非零。
- **验证风险**：issue #3189 表明 source-only checkout 缺 built artifacts 时 witness 全 missing；unit test 通过不能证明 published artifact。今日只测 retrieval 两文件，不证明 5,628-path monorepo、swarm、MCP、plugins 或 release 安全。
- **不适用场景**：小型精确检索、没有可靠 embedding identity 的 corpus、必须保留同主题多证据的任务，不应盲目追求 diversity；Hermes 不需要引入完整 Ruflo runtime 才能采用这一窄模式。

#### ⭐ Skill 升格判断

**需二次验证。** 只提出 `retrieval-evidence-diversity-gate` candidate，不直接复制 Ruflo skill、代码或框架。原因：shared hub 已有 verification-first/governance 能力，新增点只是“内部 evidence + degraded retrieval + benchmark sweep”；必须先用本地 corpus 验证中文、跨日事实、provenance 与 recall floor，并和现有 shared-memory bridge 去重。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/retrieval-diversity-gate-v0/`，包含 `fixture.json`、`rerank.py`、`test_rerank.py`、`receipt.json`；只处理 synthetic candidates。
2. 若通过二次验证：优先更新现有 `capabilities/skills/foundation/shared-memory-bridge/SKILL.md` 的 retrieval contract，而非新建大 skill；可复用 decision core 放 `scripts/`，host adapter 只传 `candidate_id/score/provenance/embedding_revision`。
3. Hermes runtime：在 `runtime/hermes/` 的索引/检索实验层接入，不直接改 `curated/memory/`；输出必须含 `mode=cosine|lexical_fallback`、`degraded_reason`、`lambda`、coverage 和 corpus revision。
4. OpenClaw 当前不存在，本次不改其配置或 runtime；future adapter 只能消费同一纯 decision contract，不复制动态项目 ID、绝对路径或凭据。

---

### 2. nvm-sh/nvm

- **一句话判断**：nvm 值得学的不是 Node 切换命令，而是它在纯 shell、弱事务环境中把“同版本并发写”“旧半安装目录”“安装成功误判”拆成锁、staging replacement、结构校验三层；该模式可用于 Hermes 安装器/迁移器，但 nvm 自身仍是 per-shell 工具，不是生产镜像锁定系统。
- **解决的问题**：替代并发 `nvm install` 互删目录、把零字节 executable 当安装成功、在旧 `bin/lib` 上逐项 merge、binary 下载失败后意外长时间 source build、以及 profile 自动修改不可控的旧做法。
- **URL / API 快照**：https://github.com/nvm-sh/nvm ；**Stars: 94,910 / Forks: 10,424 / Language: Shell / License: MIT**；`updated_at=2026-09-05T23:25:54Z`，`pushed_at=2026-09-04T22:40:55Z`，repository API `open_issues_count=389`（含 PR），default branch `master`。
- **固定提交**：[`ccb49e5cd07e3a73850a1e1d36e666297ced9018`](https://github.com/nvm-sh/nvm/commit/ccb49e5cd07e3a73850a1e1d36e666297ced9018)，committer time `2026-09-04T21:08:01Z`，修复 stderr 被关闭时 `nvm_err` 导致工作流失败；对应 issue [#3906](https://github.com/nvm-sh/nvm/issues/3906) 已关闭。
- **Release / issue 证据**：latest release [`v0.40.7`](https://github.com/nvm-sh/nvm/releases/tag/v0.40.7)，`published_at=2026-08-18T06:22:50Z` 且 API `immutable=true`；release notes明确列出 same-version serialization、`NVM_NO_SOURCE_FALLBACK`、broken install reject、atomic replacement、installer download 去 `eval`。open issue [#3114](https://github.com/nvm-sh/nvm/issues/3114) 请求 source build 前应用用户 patch，说明 source fallback 的可定制性尚未内建。
- **来源交叉核验**：README、ROADMAP、v0.40.7 release、issues #3906/#3114、固定 `nvm.sh/install.sh/nvm-exec`、三项 upstream fixtures、GitHub advisories API 和 dev dependency audit。

#### 架构 / 实现与数据流

```text
shell sources nvm.sh
  -> resolve .nvmrc / alias / local or remote version
  -> nvm install
       -> per-version advisory lock (.cache/locks/<sanitized-version>)
       -> choose binary vs source（可用 NVM_NO_SOURCE_FALLBACK 限制）
       -> download + checksum
       -> extract into temp staging
       -> replace whole version directory (rename; cross-FS fallback)
       -> structural validate: non-empty executable node + resolvable npm symlink
       -> release lock
  -> nvm use
       -> rewrite current shell PATH
  -> nvm-exec
       -> source --no-use -> resolve NODE_VERSION/.nvmrc -> nvm use -> exec argv

install.sh
  -> decide NVM_DIR/XDG path + source + git/script method
  -> install pinned nvm version
  -> detect profile or respect PROFILE=/dev/null
  -> append source/completion only when absent
  -> optionally install NODE_VERSION
```

nvm 的 authority 是“当前 shell 环境 + 用户目录”，不是系统 daemon。安装事务也不是数据库 ACID：锁使用 atomic `mkdir`，内容先放 temp，再替换目标目录；校验的是 layout，不执行 Node，以免把“宿主 glibc 不兼容”误判成“安装树破损”。这体现了 failure taxonomy：broken artifact 与 incompatible runtime 是不同状态。

#### repo tree 摘要

固定 commit `git ls-files` 为 **448 tracked paths**；去除 git 元数据与临时依赖后实查主要文件为 `test/ 389`、`.github/ 25`，核心实现集中在少数 shell 文件：

```text
nvm-sh/nvm/
├── nvm.sh                 # 版本解析、download、install/use、lock、校验（约 171 KiB）
├── install.sh             # git/script installer、profile detection/mutation
├── nvm-exec               # .nvmrc/NODE_VERSION -> nvm use -> exec
├── bash_completion        # shell completion
├── test/
│   ├── fast/              # 函数与行为 fixtures
│   ├── slow/              # 命令流程
│   ├── install_script/    # installer/profile 行为
│   ├── installation_node/ # 实际 Node 安装路径
│   └── sourcing/          # source semantics
├── Makefile               # 多 shell + Urchin test orchestration
├── README.md              # install/use/offline/mirror/WSL contracts
├── ROADMAP.md             # RC/nightly/update/v1.0 未完成项
├── package.json           # 只含 devDependencies，无 runtime npm dependency
└── LICENSE.md             # MIT
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `nvm.sh:233-269` | `nvm_validate_install()` | 检查 version dir、non-empty executable node、npm symlink target；刻意不运行 node |
| `nvm.sh:2459-2522` | `nvm_install_binary_extract()` | 先完整解压到 TMPDIR，删除旧目标后单 rename；跨 filesystem 才逐项 fallback |
| `nvm.sh:3293-3365` | lock lifecycle | 版本名净化、atomic mkdir、timeout、opt-in stale steal、release |
| `nvm.sh:136-200` | downloader boundary | 参数作为 argv 传给 curl/wget，不再 eval；Authorization header allowlist sanitize |
| `install.sh:71-109` | source identity | 默认 `nvm-sh/nvm` + pinned version；非默认 repo 给醒目 warning |
| `install.sh:310-350,401-509` | profile mutation | `PROFILE=/dev/null` 时不修改；否则探测 profile 并避免重复 append |
| `nvm-exec:1-20` | subprocess adapter | 选择 NODE_VERSION 或 `.nvmrc`，版本未装则 exit 127，最后 `exec "$@"` |
| `test/fast/Unit tests/*` | recovery fixtures | 真实覆盖 lock、broken dir replacement、zero-byte node/dangling npm |

#### ⭐ 源码精读

**代码块 1：`nvm_acquire_install_lock()` 用 per-version atomic mkdir 串行化写者。**

```sh
nvm_acquire_install_lock() {
  VERSION="${1-}"
  [ -z "${VERSION}" ] && return 0
  LOCK_ROOT="$(nvm_cache_dir)/locks"
  command mkdir -p "${LOCK_ROOT}" 2>/dev/null || return 0
  LOCK="${LOCK_ROOT}/$(nvm_install_lock_name "${VERSION}")"
  TIMEOUT="${NVM_INSTALL_LOCK_TIMEOUT:-600}"
  STALE="${NVM_INSTALL_LOCK_STALE:-0}"
  WAITED=0
  while ! command mkdir "${LOCK}" 2>/dev/null; do
    # opt-in stale removal; timeout otherwise
    [ "${WAITED}" -ge "${TIMEOUT}" ] && return 1
    command sleep 1; WAITED=$((WAITED + 1))
  done
  NVM_INSTALL_LOCK="${LOCK}"
}
```

逻辑摘要：scope 是 sanitized version，同版本互斥、不同版本不被全局锁阻塞；默认永不偷 stale lock，只有显式 `NVM_INSTALL_LOCK_STALE` 才按 mtime 删除。边界：如果 lock root 创建失败，函数 **fail open** 返回成功；目录锁不记录 owner token/PID，因此 stale 判断依赖时间与人工策略，不是强租约。

**代码块 2：`nvm_install_binary_extract()` 把半安装恢复变成 staging + whole-tree replace。**

```sh
nvm_install_binary_extract() {
  NVM_OS="$1"; PREFIXED_VERSION="$2"; VERSION="$3"
  TARBALL="$4"; TMPDIR="$5"
  VERSION_PATH="$(nvm_version_path "${PREFIXED_VERSION}")" || return 1
  nvm_extract_tarball "${NVM_OS}" "${VERSION}" "${TARBALL}" "${TMPDIR}" || return 1
  command rm -rf "${VERSION_PATH}" || return 1
  command mkdir -p "$(dirname "${VERSION_PATH}")" || return 1
  if command mv "${TMPDIR}" "${VERSION_PATH}" 2>/dev/null; then return 0; fi
  command mkdir -p "${VERSION_PATH}" || return 1
  command mv "${TMPDIR}/"* "${VERSION_PATH}" || return 1
}
```

逻辑摘要：先完成 download/extract，才删旧 broken target；同 filesystem 用 rename 收口，避免旧文件与新文件 merge。上游 fixture 预置 stale `bin/npm`/`lib/STALEFILE` 且缺 node，执行后确认 stale 文件消失、新 node/npm 存在。边界：跨 filesystem fallback 是逐项 move，不再具有同等 whole-tree atomic visibility；删除目标到 move 完成之间也不是 rollback transaction。

**代码块 3：`nvm_validate_install()` 区分结构破损与宿主不兼容。**

```sh
nvm_validate_install() {
  VERSION="${1-}"
  VERSION_PATH="$(nvm_version_path "${VERSION}" 2>/dev/null)"
  [ -z "${VERSION_PATH}" ] || [ ! -d "${VERSION_PATH}" ] && return 1
  NVM_NODE_PATH="${VERSION_PATH}/bin/node"
  if [ ! -s "${NVM_NODE_PATH}" ] || [ ! -x "${NVM_NODE_PATH}" ]; then
    nvm_err "The installed node binary ... is missing or empty."
    return 1
  fi
  if [ -h "${VERSION_PATH}/bin/npm" ] && [ ! -e "${VERSION_PATH}/bin/npm" ]; then
    nvm_err "npm for ${VERSION} is a dangling symlink."
    return 1
  fi
}
```

逻辑摘要：`-x` 不足以拒绝 zero-byte 文件，因此结合 `-s`；dangling npm symlink 单独拒绝。fixture 还让 `bin/node` 执行时 exit 1，却要求 layout validation 通过，因为运行失败可能是 glibc/宿主 compatibility，而非 artifact tree broken。边界：结构校验不覆盖二进制签名、所有 bundled files、执行能力或 ABI；checksum 和 runtime smoke 属于其他阶段。

**代码块 4：`nvm_download()` 不再通过 eval 重解释远端影响的参数。**

```sh
nvm_download() {
  sanitized_header=''
  [ -n "${NVM_AUTH_HEADER:-}" ] &&
    sanitized_header="$(nvm_sanitize_auth_header "${NVM_AUTH_HEADER}")"
  if nvm_has_executable curl; then
    NVM_DOWNLOADER='curl'; set -- -q --fail "$@"
  elif nvm_has_executable wget; then
    NVM_DOWNLOADER='wget'
    # translate known curl flags into wget argv
  fi
  [ -n "${NVM_AUTH_HEADER:-}" ] &&
    set -- "$@" --header "Authorization: ${sanitized_header}"
  command "${NVM_DOWNLOADER}" "$@"
}
```

逻辑摘要：downloader 名和参数都作为 literal argv 执行，不让 mirror-supplied version string 被 shell 二次解析；这是 v0.40.7 release 的 robustness 项。边界：自定义 mirror/auth 仍是敏感 egress 面；header sanitize 不等于目标 host allowlist，用户不应在不可信 mirror 上发送凭据。

**代码块 5：`nvm-exec` 是薄 adapter，版本不可用时明确失败。**

```sh
DIR="$(command cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. "$DIR/nvm.sh" --no-use
if [ -n "$NODE_VERSION" ]; then
  nvm use "$NODE_VERSION" > /dev/null || exit 127
else
  NVM_RC_VERSION="$(nvm_rc_version 3>&1 1>&4)" &&
    nvm_ensure_version_installed "$NVM_RC_VERSION"
  nvm use >/dev/null 2>&1 || exit 127
fi
exec "$@"
```

逻辑摘要：adapter 不复制 version resolver；复用 canonical `nvm.sh`，成功后用 `exec` 保留目标程序的进程/exit semantics。边界：它继承当前目录 `.nvmrc` 的信任问题；对不可信仓库，版本文件只是请求，不应自动触发安装或 profile mutation。

#### 依赖分析与供应链风险

- `package.json` **没有 runtime npm dependencies**；nvm 运行依赖 POSIX shell 与系统工具。devDependencies 为 `dockerfile_lint`、`doctoc`、`eclint`、`markdown-link-check`、`replace`、`semver`、`urchin`。
- 本机临时安装 478 packages，npm audit 为 20 条（critical 1 / high 10 / moderate 9），直接命中包括 `dockerfile_lint`、`eclint`、`replace`；`urchin@0.0.5`、旧 `axios` 等还出现 deprecation/security warning。它们不进入 nvm runtime，但会影响贡献者 CI/docs/release tooling，不能忽略。
- README 推荐 `curl|bash`/`wget|bash` 一步安装；这对便利有效，但自动化环境应先下载固定 tag、校验来源/内容，再执行。GitHub release `immutable=true` 是平台元数据，不等于 tarball 独立签名。
- 三条已公开 nvm advisories 都在 0.40.7 之前修复；仍需禁止部署旧缓存版本，并独立核验 Node 下载 checksum、mirror identity 与 auth header 目标。

#### 可复用经验

- 当多个进程会写同一版本/资源目录时，应优先使用 resource-scoped lock + timeout，并让 stale reclaim 显式 opt-in，因为全局锁降低并发、无界抢锁会把活写者误删；边界是 lock directory 创建失败不能默默当安全成功。
- 当安装或迁移可能留下半目录时，应优先先在 staging 完整构建和校验，再以 whole-tree rename 提交，因为逐文件覆盖会混入旧状态；边界是跨 filesystem fallback 必须降级标记并补 receipt/rollback。
- 当验证“安装成功”时，应优先拆分 artifact integrity、layout validity 与 host runtime compatibility，因为 executable bit、checksum、真实执行分别回答不同问题；边界是任何单层绿色都不是完整完成证明。
- 当 installer 会修改 profile/config 时，应优先提供 `PROFILE=/dev/null` 这类明确 no-mutation mode，并让计划/执行/验证可分离，因为 unattended install 不应把自动探测当授权。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/scoped-staged-install-v0/` 用 Python + shell fixtures 建一个无网络 installer：两个并发进程争同一 artifact key；candidate 先写 staging，生成 file manifest/hash，故意 kill 一个 writer，再验证第二个不会合并 stale file；同 filesystem 走 atomic replace，模拟 cross-filesystem 时必须返回 `degraded_requires_verification`。不触碰 `~/.hermes`、profile、shared curated 或真实 Node 安装。

#### 风险边界

- **License**：GitHub API 与 `LICENSE.md` 为 MIT；可抽象机制。Node binaries、npm packages、mirror 与系统工具有独立许可。
- **维护活跃度**：最近 10 个 commit 覆盖 `2026-09-03T17:17:16Z` 至 `2026-09-04T21:08:01Z`；最新 release 为 2026-08-18，当前维护活跃。项目仍未到 1.0，ROADMAP 把 `nvm update`、RC/nightly 和 v1.0 列为未完成。
- **安全风险**：历史 mirror/version/env 注入与 path traversal advisories 说明远端元数据是攻击输入。README pipe-to-shell、profile mutation、custom mirror/auth 都需额外 gate；不能把当前 patched version 外推为配置安全。
- **局限性**：nvm 是 per-user/per-shell，PATH mutation 对 cron/non-interactive shell 必须显式 source；不适合作为容器/生产部署的唯一 immutable build provenance。Windows 原生不是主支持面，WSL/Git Bash/Cygwin 各有差异。
- **验证局限**：今日只执行三项定向 fixture和 bash syntax；未跑多 shell/full/slow/real Node installation。ShellCheck 未安装；完整静态检查 **blocked**。dev audit 非零，Makefile 路径初次 blocked 也已保留。

#### ⭐ Skill 升格判断

**需二次验证。** 不把 nvm 变成 shared skill；只把 `resource-scoped lock + staged whole-tree commit + layered validation + no-mutation install mode` 作为候选模式。它与现有 path-portability、bootstrap、verification-first 有重叠，应优先更新现有安装/迁移契约而不是新增重复 skill。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/scoped-staged-install-v0/`，只在临时目录运行并输出 `prepared/committed/degraded/blocked` receipt。
2. 若通过：把通用 staged commit helper 放在 shared `scripts/`，目标根始终由 `scripts/resolve_shared_root.py` 解析；禁止写死宿主绝对路径。
3. Hermes bridge/bootstrap 可采用 `--check/--apply` 分离：prepare 只列 source revision、target realpath、manifest/hash、预计 mutation；apply 需显式触发，完成后 read-back exact target。
4. shared skill 层优先更新 `capabilities/skills/foundation/path-portability/SKILL.md` 或相关 bootstrap 文档，加入 same-resource lock、cross-filesystem degraded state 和 no-config-mutation fixture；不自动修改 Hermes config/env/auth/cron。
5. OpenClaw 当前不存在，本次不操作；future agent 只复用中性的 staged-commit contract，不复用 nvm 的 profile、Node-specific alias 或本机路径。

## 经验沉淀

1. 当检索排序需要兼顾相关性与去重时，应优先把 relevance、diversity、recall floor 和参数 sweep 同时纳入验收，因为单一“更分散”指标会奖励遗漏；边界是 synthetic benchmark 不能替代真实 corpus。
2. 当内部 evidence（embedding、credential metadata、raw artifact）只用于决策时，应优先由 typed internal schema 传递并在每个 CLI/API adapter 用字段 allowlist，因为“当前没有输出”不是可测试的不泄漏契约。
3. 当数值向量、分数或统计量进入循环比较时，应优先拒绝/降级 NaN、Infinity、空值、维度和 revision 不匹配，因为异常数值可能让排序静默少返回；degraded path 必须带 reason。
4. 当多个进程修改同一 artifact 时，应优先 resource-scoped lock、staging、whole-tree commit 和 post-commit validation，因为 queue empty、exit 0 或部分文件存在都不证明目标一致。
5. 当验证安装/发布结果时，应优先分开下载来源、checksum、layout、runtime compatibility、published artifact 与 source checkout，因为每层绿色只覆盖自己的 failure class。
6. 当安装器会改 profile、配置或兼容入口时，应优先提供 prepare/check 与显式 apply/no-mutation mode，因为自动发现 target 不是修改授权。
7. 当 GitHub 项目有绿测试或 security advisory 已标 patched 时，应优先核 resolved dependency、真实版本和执行面，因为 repo HEAD、release tag、npm tarball、source checkout 与当前 host 不是同一个对象。
8. 当测试 runner 因 prerequisite 或调用方式未运行真实 fixture 时，应优先标 blocked 并换成可验证的正确入口，因为 runner 报错不能被记录为测试失败，更不能伪装成通过。

## 明日继续

1. **最小动作 A**：创建 `runtime/hermes/github-learning-poc/retrieval-diversity-gate-v0/`，先用中文 synthetic corpus 证明 `embedding_revision mismatch -> lexical fallback`、`lambda sweep` 与 `recall floor`；不接真实 curated。
2. **最小动作 B**：创建 `runtime/hermes/github-learning-poc/scoped-staged-install-v0/`，覆盖 same-key contention、kill mid-stage、stale lock、cross-filesystem degraded 和 final manifest read-back。
3. **继续核验**：Ruflo 的 source-only witness #3189 在完整 build artifact 上是否能通过；nvm 的跨 filesystem fallback 是否需要显式 degraded receipt。两项均不在无人 cron 自动安装上游软件。

## 候选反哺

### Candidate Facts

- [ ] topic: retrieval rerank 必须同时记录 relevance/recall/diversity/duplicate 与 degraded mode | evidence: `ruvnet/ruflo@277c7bc` 的 `smart-retrieval.ts`、`mmr-benchmark.test.ts` 和本机 18-test 输出 | 建议: create candidate only | 安全级别: low
- [ ] topic: artifact 安装完成应拆分 lock、staging commit、layout validation 与 runtime compatibility | evidence: `nvm-sh/nvm@ccb49e5` 的 `nvm_acquire_install_lock`、`nvm_install_binary_extract`、`nvm_validate_install` 及三项本机 fixture | 建议: create candidate only | 安全级别: low
- [ ] topic: source checkout、release tag、包管理器制品和实际 resolved graph 是不同证据对象 | evidence: Ruflo v3.38.21 release known package gap、#3189 与 nvm v0.40.7 immutable release/API | 建议: update existing verification candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: retrieval-evidence-diversity-gate | 可复用场景: shared memory / research result rerank | 是否建议 shared: yes-after-POC | 原因: 横切 Hermes/future agent，但需中文真实 corpus、provenance 与 embedding revision 二次验证，优先更新 shared-memory-bridge
- [ ] 名称: scoped-staged-artifact-commit | 可复用场景: bootstrap、bridge install、迁移、能力更新 | 是否建议 shared: yes-after-POC | 原因: 跨 agent 横切；需补 owner-token lock、cross-FS degraded、rollback/read-back，并与 path-portability 去重

### Candidate Open Questions

- [ ] 问题: shared hub 的检索 candidate 是否已持有可比较的 embedding model/revision 与 provenance？ | reason: adaptation | priority: high
- [ ] 问题: 当前 bootstrap/bridge 写入是否存在跨进程 same-target race 或 cross-filesystem rename？ | reason: gap | priority: high
- [ ] 问题: Ruflo witness 在按 release 所需步骤构建后能否核 published npm tarball，而不只是本地 dist？ | reason: gap | priority: medium
- [ ] 问题: nvm lock root 创建失败时 fail-open 是否会在受限 HOME/NFS 环境重新引入并发破坏？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动安装 Ruflo、nvm、plugin、MCP、模型或 Node 版本；不执行 README 的 pipe-to-shell 命令。
- 不自动改 Hermes/OpenClaw 配置、模型、provider、auth、env、cron、profile 或 shell startup files。
- 不直接写 curated active fact；以上只进入 Hermes 二轮审计候选，需证据、去重、脱敏和人工/总控审查。
- 不复制 license 不明/不兼容项目源码；不把 MIT 根许可外推到依赖、模型、数据或 release asset。
- 不把 assistant prose、GitHub issue hypothesis、Stars、audit clean/dirty 或 synthetic benchmark 单独当用户事实、生产授权或安全证明。
