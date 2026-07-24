# 2026-07-24 GitHub 热门项目学习日报（Hermes）

> 执行器：Hermes（本任务未调用 OpenClaw）  
> 调研时间：2026-07-24 07:30–07:35 CST  
> 热门入口：`https://github.com/trending?since=daily`（2026-07-24 07:31 CST 真实抓取，共解析到 15 个仓库）  
> 元数据来源：GitHub REST API（`gh api repos/{owner}/{repo}`）；Stars、Forks、License、更新时间均为查询时快照，不是永久值。  
> 深读代码固定到：`likec4/likec4@f9700621c2bd8cc6c002d54b813a4d251e3f7bd8`、`Automattic/harper@efa59c33b2915108f52c385ce1e3311a3cfa1439`。  
> 验证边界：两个仓库均已真实 clone 并 checkout 到上述提交；读取了 README、官方架构/贡献文档、release、open issue、GitHub check-runs 与关键源码。当前 WSL 有 Node `v22.14.0`，但缺少 `pnpm`、`cargo`、`rustc`；LikeC4 还要求 Node `>=22.22.3`，所以未伪造本地构建或测试通过，动态行为结论标注为“源码核验，运行待核验”。

## 今日结论

今天最值得迁移的主线是：**先建立可查询、分阶段、带作用域的确定性语义模型，再把 Agent 或规则引擎放在模型之上；同时，工具的真实副作用必须由机器可检验的权限元数据表达，不能只靠说明文字。** LikeC4 展示了 `parsed → computed → layouted` 的架构模型与批量图查询，但其 MCP 文本宣称“全部只读”与 `apply-semantic-layout` 实际写入 snapshot 存在源码级冲突；Harper 展示了本地 `Parser → Document → LintGroup → integration` 的确定性质量门，并用配置哈希缓存和只导出忽略项哈希降低隐私成本。两项都适合先进入 Hermes runtime POC，不应直接改配置、cron 或 curated active fact。

## 项目速览

以下项目都出现在 07:31 CST 抓取的 GitHub Trending 日榜。Stars、Language、License、`pushed_at` 来自随后真实 GitHub API 查询。`NOASSERTION` 表示 API 无法给出 SPDX 结论，不等于允许任意使用。

| 项目 | Stars（API） | Language | License（API） | API `pushed_at` | 今日判断 |
|---|---:|---|---|---|---|
| [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | 71,506 | TypeScript | NOASSERTION | 2026-07-23T21:31:47Z | 情报聚合面板；License 未判定，不复制源码 |
| [jellyfin/jellyfin](https://github.com/jellyfin/jellyfin) | 54,720 | C# | GPL-2.0 | 2026-07-22T17:46:57Z | 成熟媒体系统；GPL 组合边界需单独评估 |
| [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | 33,029 | Python | MIT | 2026-04-13T12:38:49Z | 金融基础模型；热度高但 API push 距今较久 |
| [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | 27,109 | TypeScript | MIT | 2026-07-23T23:14:06Z | 多模型路由；provider/密钥面不自动接入 |
| [Automattic/harper](https://github.com/Automattic/harper) | **12,254** | Rust | **Apache-2.0** | 2026-07-23T20:25:16Z | **深读**：本地确定性英文质量门与多前端复用 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 11,473 | Go | Apache-2.0 | 2026-07-23T14:43:51Z | 昨日已深读，今日不重复占深读名额 |
| [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | 9,962 | JavaScript | MIT | 2026-07-11T00:26:42Z | 文本到 CAD；执行生成代码需沙箱 |
| [Pumpkin-MC/Pumpkin](https://github.com/Pumpkin-MC/Pumpkin) | 8,889 | Rust | GPL-3.0 | 2026-07-20T09:55:57Z | Rust 服务端；GPL 代码不混入 shared capability |
| [block/buzz](https://github.com/block/buzz) | 6,793 | Rust | Apache-2.0 | 2026-07-23T23:30:26Z | 昨日已深读；今日只保留趋势观察 |
| [likec4/likec4](https://github.com/likec4/likec4) | **4,675** | TypeScript | **MIT** | 2026-07-23T18:04:06Z | **深读**：架构即代码、阶段模型与 Agent 图查询 |

> 数据复核：深读项目 API 快照分别为 LikeC4 4,675 Stars / 318 Forks、Harper 12,254 Stars / 456 Forks；完整候选快照位于 `runtime/hermes/github-hot-project-learning/evidence/2026-07-24/repos.jsonl`。

## 深读项目

### 项目 1：likec4/likec4

- 仓库：[https://github.com/likec4/likec4](https://github.com/likec4/likec4)
- 固定提交：[`f9700621c2bd8cc6c002d54b813a4d251e3f7bd8`](https://github.com/likec4/likec4/commit/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8)，commit API 时间 2026-07-22T18:45:37Z
- API 快照：Stars **4,675**；Forks **318**；Language **TypeScript**；License **MIT**；open issues **168**；updated_at 2026-07-23T23:28:38Z；pushed_at 2026-07-23T18:04:06Z
- 最新 release：[`v1.59.2`](https://github.com/likec4/likec4/releases/tag/v1.59.2)，发布于 2026-07-22T18:58:22Z
- 一句话判断：**值得学的不是自动画图，而是把架构从易漂移的图片提升为可解析、可计算、可布局、可查询、可追溯到源码位置的分阶段模型。**

#### 解决的问题：替代了什么旧做法

README 将 LikeC4 定义为受 C4 Model / Structurizr DSL 启发、但允许自定义 notation、element type 与任意嵌套层级的 architecture-as-code 工具。它替代的是“手动画图 + 文档中重复维护组件清单 + Agent 反复全文扫描”的旧做法：DSL 是输入，Langium language server 负责解析与诊断，core 计算 view，Graphviz 布局，React/SPA 渲染；MCP 则把 resolved model 暴露为 graph query、批量读取、关系路径和 subgraph summary。

这并不等于“架构永远自动保持正确”。模型仍需人或生成流程维护；`toDSL()` 官方注释明确 round-trip 会丢失 comments、source positions 与原格式。因此应把模型生成、可视化和查询看作受控派生链，而不是无损编辑器。

#### 架构 / 实现与数据流

依据 `AGENTS.md`、`packages/language-services/src/common/LikeC4.ts`、`packages/core/src/compute-view/compute-view.ts`、`packages/mcp/` 交叉核验：

1. `.c4` DSL 由 `packages/language-server` 的 Langium grammar / LSP 解析并产生 diagnostics。
2. `LikeC4.parsedModel()` 返回 `LikeC4Model.Parsed`；这是 elements、relations、views、deployments、globals、imports 的原始结构。
3. `computeParsedModelData()` 建立 parsed `LikeC4Model`，按 view 类型分发到 element/deployment/dynamic 计算器，并把 `_stage` 改为 `computed`。
4. `layoutedModel()` 在 computed view 上应用 Graphviz/manual layout，得到可渲染的 `Layouted` stage。
5. 开发模式中，SPA 经 `likec4:rpc` / birpc / Vite HMR 调 language services，模型更新后通过虚拟模块和 nanostores 触发图重绘；production build 则把虚拟模块内联为静态 JSON，图为只读。
6. MCP server 复用同一 language services，提供 project、element、view、relationship、incomer/outgoer、metadata/tag、batch read 与 subgraph 等查询。
7. `subgraph-summary` 在 computed model 上做 BFS，响应最多 200 个 descendant，深度最多 20，并显式返回 `truncated` / `truncatedByDepth`。
8. 重要反例：MCP 顶层 instructions 写着“All tools are read-only and idempotent”，但同一 server 注册了 `apply-semantic-layout`；该工具通过 sampling 生成 hints，最终调用 `languageServices.editor.applyChange({ op: 'save-view-snapshot' })`。因此**文字契约和真实副作用不一致**。

#### Repo tree 摘要

```text
likec4/
├── apps/                       # docs、playground 等用户应用
├── packages/
│   ├── core/                   # 模型类型、Builder、view compute、模型遍历
│   ├── language-server/        # Langium DSL parser、LSP、workspace 服务
│   ├── language-services/      # 浏览器/Node 统一入口，封装 parser/compute/layout
│   ├── layouts/                # Graphviz 与 semantic layout
│   ├── diagram/                # React/ReactFlow 图渲染契约
│   ├── likec4-spa/             # SPA host、nanostores、HMR model context
│   ├── vite-plugin/            # 虚拟模块与 SPA↔LSP RPC bridge
│   ├── mcp/                    # Agent 可调用的模型查询与 semantic layout 工具
│   ├── generators/             # Mermaid / PlantUML / D2 / LikeC4 DSL 输出
│   ├── likec4/                 # CLI 与静态站生成入口
│   └── vscode/                 # VS Code extension
├── skills/likec4-dsl/          # 上游自己的 Agent skill；本任务不直接复制
├── examples/                   # 示例模型与多项目 fixture
├── e2e/ + tests/               # Playwright / Vitest 测试
├── pnpm-workspace.yaml         # catalog、build allowlist、patched dependency
└── pnpm-lock.yaml              # 锁定依赖图
```

#### 关键源码文件

| 文件 | 用途 | 本次核验到的关键内容 |
|---|---|---|
| `packages/language-services/src/common/LikeC4.ts` | SDK / service facade | `parsedModel`、`computedModel`、`layoutedModel` 明确分阶段；`toTypedBuilder` 做 subset compatibility；`toDSL` 明确有损 |
| `packages/core/src/compute-view/compute-view.ts` | view 计算入口 | 用类型 guard 分发 element/deployment/dynamic view；安全版本把异常转为 tagged result |
| `packages/core/src/model/LikeC4Model.ts` | resolved model / graph index | 构造 element、parent/children、incoming/outgoing/internal、view、tag 等索引；stage guard 区分 parsed/computed/layouted |
| `packages/mcp/src/server/createMCPServer.ts` | MCP registry | 注册查询工具并开启 strict capabilities；文字 instructions 声称所有工具只读 |
| `packages/mcp/src/tools/subgraph-summary.ts` | 批量子图摘要 | bounded response + depth；BFS；metadata filter；返回截断信号 |
| `packages/mcp/src/tools/apply-semantic-layout.ts` | AI 布局写入 | 发起 MCP sampling，调用 layout，再以 `save-view-snapshot` 写入 editor change |
| `packages/mcp/src/utils.ts` | 工具统一 adapter | Zod schema、structuredContent、异常转 `isError`；未在此统一强制只读策略 |
| `pnpm-workspace.yaml` | 供应链策略 | pnpm catalog；`allowBuilds` 明确允许/拒绝 install scripts；patch `chroma-js@3.2.0` |

#### ⭐ 源码精读 1：阶段转换是类型与数据的共同契约

`packages/core/src/compute-view/compute-view.ts:67-90`：

```ts
export function computeParsedModelData<A extends AnyParsed>(
  parsed: ParsedLikeC4ModelData<A>,
): ComputedLikeC4ModelData<aux.toComputed<A>> {
  const likec4model = LikeC4Model.create(parsed)
  const { views: _views, _stage: __omitted, ...rest } = parsed
  const views = mapValues(_views, v => unsafeComputeView(v, likec4model))
  return {
    [_stage]: 'computed',
    ...rest,
    views,
  }
}
```

逻辑摘要：计算不是“给对象附加几个字段”，而是显式消费 parsed data、用 parsed model 做查询上下文、重建全部 view 并写入新 stage。这样调用方可用 `isParsed/isComputed/isLayouted` 做状态窄化，避免把尚未布局的数据误交给 renderer。边界是 `unsafeComputeView` 会抛异常；需要用户态容错时应调用返回 tagged result 的 `computeView`。

#### ⭐ 源码精读 2：批量图查询用 BFS + 输出截断信号

`packages/mcp/src/tools/subgraph-summary.ts:121-183`：

```ts
const MAX_RESULTS = 200

const rootElement = model.findElement(args.elementId)
invariant(rootElement, `Element "${args.elementId}" not found`)

const queue = [...rootElement.children()]
  .map(element => ({ element, depth: 1 }))

while (queue.length > 0) {
  const { element, depth } = queue.shift()!
  if (depth > args.maxDepth) {
    truncatedByDepth = true
    continue
  }
  totalDescendants++
  const children = [...element.children()]
  if (descendants.length < MAX_RESULTS) {
    descendants.push(/* compact fields + counts */)
  } else {
    truncated = true
  }
  for (const child of children) queue.push({ element: child, depth: depth + 1 })
}
```

逻辑摘要：工具避免 Agent 对每个节点重复 `read-element`，同时以 compact schema 限制响应体，并明确告诉调用方结果是否被截断。这是降低 tool round-trip/token 的有效模式。边界是 `MAX_RESULTS` 只限制响应数组，不限制 BFS 实际遍历总节点数；极大模型仍可能产生 CPU/内存压力，应在复用时增加 `maxVisited` / deadline / cancellation 检查。

#### ⭐ 源码精读 3：工具文字“只读”不等于实现只读

`packages/mcp/src/tools/apply-semantic-layout.ts:104-116`：

```ts
const result = await languageServices.views.layouter.aiLayout(
  { view: view.$view, styles: model.$styles },
  hints,
)

const change = await languageServices.editor.applyChange({
  change: {
    op: 'save-view-snapshot',
    layout: result.diagram,
  },
  viewId: view.id,
  projectId,
})
```

逻辑摘要：该工具先通过 MCP sampling 把 diagram 交给模型生成 layout hints，再写回 view snapshot。它与 `createMCPServer.ts` instructions 中“All tools are read-only and idempotent”不相符，而且没有像查询工具那样声明 `readOnlyHint: true`。这不是对项目安全性的全面判定，但足以证明：**权限决策不能从自然语言总说明推导，必须逐工具读取可机检 metadata 与实际调用链。**

#### ⭐ 源码精读 4：DSL round-trip 主动声明有损

`packages/language-services/src/common/LikeC4.ts:248-251`：

```ts
async toDSL(project?: string): Promise<string> {
  const parsed = await this.parsedModel(project)
  return generateLikeC4Source(
    parsed.$data as Parameters<typeof generateLikeC4Source>[0],
  )
}
```

逻辑摘要：实现本身很短，但其接口注释明确 output 不保留 comments、source positions、original formatting。可迁移教训是：模型到文本的 emitter 必须把 lossiness 放进契约，生成前保存 source/hash/diff，不能把 regenerate 当作无损 patch。

#### 依赖分析与供应链风险

根 `package.json` 指定版本 **1.59.2**、`pnpm@11.15.0`、Node **>=22.22.3**；本机 Node `22.14.0` 低于要求且没有 pnpm，因此没有执行本地 build/test。核心依赖与风险如下：

- `langium 3.5.0` + VS Code LSP packages：DSL/LSP 基座；parser 生成物与 runtime 版本必须同步。
- `@hpcc-js/wasm-graphviz 1.22.2`：布局依赖 WASM；资源占用、平台构建与恶意模型复杂度要单独限额。
- `@modelcontextprotocol/sdk ^1.29.0`、Hono：扩大到 stdio/HTTP Agent 工具面；必须区分 read/write 工具并配置 workspace scope。
- `zod ^4.4.3`，MCP 部分从 `zod/v3` 导入：schema 可检验是优点，但双 API 兼容面需关注。
- `esbuild 0.28.1`、`sharp 0.35.0`、`workerd`、`oxlint` 等含构建/原生面；`pnpm-workspace.yaml` 用 `allowBuilds` 明确控制 install scripts，是积极信号。
- `patchedDependencies` 固定了 `chroma-js@3.2.0` 的本地 patch；升级必须重新评估 patch 是否仍适用。
- `pnpm-lock.yaml` 存在；release v1.59.2 专门修复了 MCP 包未发布 runtime dependencies 导致 `npx` 安装的问题，说明“源码构建成功”不等于“发布包可运行”。

GitHub check-runs 快照：固定提交共有 30 条，6 success、21 skipped、3 failure；3 条 failure 都名为 Dependabot。不能据此宣称该提交“全绿”，也不能仅凭 Dependabot failure 推断运行代码失败，具体 job 原因本次未继续展开，标记**待核验**。

#### 可复用经验

- **当同一事实需要被 UI、CLI 和 Agent 复用时，应优先建立 `parsed → computed → layouted` 这类显式阶段模型，并让各入口消费相同 resolved model，因为重复解析文本会产生语义漂移；边界是 stage 转换与 emitter 的有损字段必须公开。**
- **当 Agent 需要读取大图或层级树时，应优先提供 bounded batch query + `truncated` 信号，而不是让 Agent 循环单节点工具，因为可减少 round-trip 和 token；边界是响应上限之外还要限制总遍历量与执行时间。**
- **当工具说明声称“只读”时，应优先依据逐工具权限 metadata 和真实调用链做授权，而不是相信 server 级自然语言，因为注册表可能同时包含写操作；边界是 metadata 也需测试防止与实现漂移。**
- **当结构化模型需要重新生成 source 时，应优先声明 lossiness 并输出 diff/backup，而不是原地覆盖，因为 comments、positions 和格式可能不可逆；边界是完全由外部 catalogue 生成的文件可以整体替换，但仍需 provenance。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/architecture-evidence-model/` 建一个**不安装 LikeC4、不调用外部模型**的 Python POC：

1. 从 `manifest.yaml` 与一个 fixture project markdown 提取 nodes / edges / source path。
2. 产出 `{stage: parsed}`，运行 validator 后产出 `{stage: computed}`，禁止未 computed 数据进入 query。
3. 实现 `subgraph_summary(root, max_depth, max_results, max_visited)`，返回 `truncated_by_depth`、`truncated_by_results`、`truncated_by_visit_budget`。
4. 注册两个 mock tools：`query_graph(readOnly=true)` 与 `save_snapshot(readOnly=false)`。
5. 审计器对照 metadata 和实际 effect fixture；若 server 总说明写“全部只读”但存在 write tool，必须失败。

成功标准：非法 stage 被拒；10,000 节点 fixture 在 visit budget 内停止；写工具不能进入只读 allowlist；所有输出携带 source path 和 evidence hash。产物只写 runtime，不改 Hermes 配置或 cron。

#### 风险边界

- **License**：MIT，机制参考与改编相对宽松，但仍需保留版权/许可文本；不直接复制上游完整 skill 或产品代码。
- **工具安全**：MCP 可经 stdio 或 HTTP 暴露 workspace model；`apply-semantic-layout` 会调用 sampling 并写 snapshot。任何真实接入都要拆分 read-only profile 与 explicit write approval，禁止默认开放 HTTP 写工具。
- **数据外发**：semantic layout 的 `sampling/createMessage` 把 prompt + diagram 交给 MCP client 选择的模型路径；架构图可能包含内部系统名与关系，需脱敏/授权。
- **资源风险**：Graphviz/WASM、文件 watch、递归图查询可能在大 workspace 消耗 CPU/内存；`subgraph-summary` 当前只限制响应数，不限制总 visited nodes。
- **有损写回**：`toDSL` 不保留 comments/source positions/格式；不能作为无备份的 source patch。
- **维护活跃度**：API `pushed_at` 为 2026-07-23，v1.59.0–v1.59.2 在四天内连续发布，活跃但升级速度快。
- **已知 issue**：open issue [#3141](https://github.com/likec4/likec4/issues/3141) 报告 VS Code extension 在特定 macOS/arm64 环境随机冻结 10 秒到 1 分钟；这是单个用户报告，根因与普遍性**待核验**。
- **CI 边界**：固定提交 check-runs 并非全绿；本机 Node 版本不满足声明且无 pnpm，未执行本地测试。
- **不适用场景**：只有几个静态组件、没有架构查询/漂移问题的小项目，不值得引入完整 DSL + LSP + Graphviz + SPA/MCP 栈。

#### Skill 升格判断

**结论：需二次验证。**

不直接迁移上游 `skills/likec4-dsl/`，也不把完整 LikeC4 作为 shared skill。候选是更窄的 `architecture-evidence-query-contract`：显式 stage、source location、bounded batch query、truncation、effect metadata。它预计可被 Hermes / future agent 复用，但必须先通过 stage misuse、超大图、metadata/side-effect drift、敏感路径脱敏 fixture。通过后才考虑进入 `capabilities/skills/foundation/` 并更新 `capabilities/manifests/shared-skills.yaml`；当前只提出 candidate。

#### Hermes / shared hub 落地路径

1. **Runtime POC**：`runtime/hermes/github-learning-poc/architecture-evidence-model/`；仅存 fixture、临时 index 和审计结果。
2. **模型输入**：通过 `scripts/resolve_shared_root.py` 获取根，不硬编码宿主路径；只读 `manifest.yaml` 与经 allowlist 的 `curated/memory/projects/*.md`，默认排除 inbox/runtime raw 文本中的 secret。
3. **Hermes 接口候选**：`scripts/architecture_evidence.py {build,validate,query}`，输出 `{stage, project_id, nodes, edges, source_locations, evidence_hash, truncation}`。
4. **工具权限表**：候选 `runtime/hermes/architecture-evidence/tool-effects.json` 为每个工具声明 `read_only / writes_runtime / writes_curated / network`；审计实现调用与声明是否一致。
5. **共享能力候选**：若 POC 跨项目稳定，再创建 `capabilities/skills/foundation/architecture-evidence-query-contract/`，更新 shared skill manifest；Skill 只保留契约/流程/验证命令，raw graph 留 runtime。
6. **治理**：不直接写 curated active fact；候选先过评分、证据、去重、脱敏和审查。

---

### 项目 2：Automattic/harper

- 仓库：[https://github.com/Automattic/harper](https://github.com/Automattic/harper)
- 固定提交：[`efa59c33b2915108f52c385ce1e3311a3cfa1439`](https://github.com/Automattic/harper/commit/efa59c33b2915108f52c385ce1e3311a3cfa1439)，commit API 时间 2026-07-23T19:44:06Z
- API 快照：Stars **12,254**；Forks **456**；Language **Rust**；License **Apache-2.0**；open issues **683**；updated_at 2026-07-23T23:28:36Z；pushed_at 2026-07-23T20:25:16Z
- 最新 release：[`v2.6.0`](https://github.com/Automattic/harper/releases/tag/v2.6.0)，发布于 2026-06-24T16:01:05Z
- 一句话判断：**Harper 值得学的是把“文本质量”做成离线、确定性、可配置、跨 CLI/LSP/WASM 复用的 core engine，而不是把每次校对都交给远端 LLM。**

#### 解决的问题：替代了什么旧做法

README 对比了两类旧做法：远端语法服务存在文本外发与网络往返；大型本地工具可能占用大量内存/数据集。Harper 选择 Rust core + curated dictionary + rule linters，通过 CLI、language server、WASM/JavaScript、浏览器、Obsidian、VS Code 和 desktop 复用同一核心。

项目方声称 lint 只需毫秒、内存少于 LanguageTool 的 1/50；本次没有独立 benchmark，**性能数字待核验**。可以源码确认的是：core 不依赖远端模型；但官方 testing strategy 也写明，当用户主动报告错误 suggestion 时会 POST 到 `writewithharper.com` 进行 tally。因此“core 可完全本地运行”和“所有集成永不联网”必须区分，不能把 README 宣传语扩大为每条产品路径的事实。

#### 架构 / 实现与数据流

依据官方 architecture/testing docs、`harper-core`、`harper-cli`、`harper-wasm` 交叉核验：

1. 不同 `Parser` 从 plain text / Markdown / code comments / Typst 等输入提取 English tokens，并保留字符 span。
2. `Document::new_from_chars` 先调用 parser，再执行 fixups、Brill POS tagging、noun-phrase chunking 与 dictionary metadata annotation。
3. `Linter` 是接收 `Document`、返回 `Vec<Lint>` 的窄 trait；mutable receiver 明确用于缓存。
4. `LintGroup` 组合普通 rules、chunk Expr linters 与 sentence Expr linters；`FlatConfig` 控制每条规则是否启用。
5. chunk/sentence 模式以 `(content_hash, config_hash)` 为 cache key；cache hit 后把相对 span 推回 document-space。
6. `harper-wasm::Linter` 复用 curated + user + Weirpack dictionaries，按 language / regex mask / isolate English 建 parser，执行 group、移除 ignored lints、可选去重，然后映射为 WASM `Lint`。
7. `harper-cli` 支持 directory batch；多个 input job 用 Rayon 并行，最后确定性汇总 JSON/compact/rich report；发现 lints 时返回错误状态，适合作为 CI quality gate。
8. `harper-ls` 与 JS/WASM/desktop/browser integrations 位于 core 之外，避免编辑器协议和 UI 逻辑污染规则引擎。

#### Repo tree 摘要

```text
harper/
├── harper-core/                # Document、Parser、dictionary、rules、LintGroup、cache
├── harper-cli/                 # 文件/目录/stdin lint，JSON/compact/rich 输出
├── harper-ls/                  # Language Server，供多种编辑器调用
├── harper-wasm/                # Rust core 的 WASM binding
├── harper-comments/            # 从多种编程语言注释提取英文
├── harper-tree-sitter/         # tree-sitter 解析适配
├── harper-{html,typst,tex,...} # 各输入格式 parser / adapter
├── harper-brill/               # POS tagger / chunker
├── harper-stats/               # 本地统计结构
├── harper-desktop/             # Tauri desktop 与 overlay highlighter
├── packages/
│   ├── harper.js/              # WASM loader、Local/Worker Linter
│   ├── chrome-plugin/          # 浏览器集成
│   ├── obsidian-plugin/        # Obsidian 集成
│   ├── vscode-plugin/          # VS Code client
│   ├── lint-framework/         # Web 文本读取/高亮/建议 UI
│   └── web/                    # 官网、文档、demo
├── Cargo.toml                  # 21 个 Rust workspace members
├── Cargo.lock                  # Rust 依赖锁
└── pnpm-lock.yaml              # Web/JS 依赖锁
```

#### 关键源码文件

| 文件 | 用途 | 本次核验到的关键内容 |
|---|---|---|
| `harper-core/src/document.rs` | 文本中间表示 | parser tokenization、fixups、Brill tag/chunk、dictionary metadata；span 始终基于 char |
| `harper-core/src/linting/mod.rs` | rule contract | `Linter::lint(&mut self, &Document)`；mutable 只为 cache，规则语义保持无外部 I/O |
| `harper-core/src/linting/lint_group/mod.rs` | rule 编排与 cache | 普通/chunk/sentence 三类规则；BTreeMap 稳定顺序；content+config hash cache |
| `harper-wasm/src/lib.rs` | 浏览器/JS facade | parser 装饰、curated config、ignored hashes、dictionary sync、去 overlap |
| `harper-cli/src/lint.rs` | CI/批量入口 | 多输入 Rayon 并行、JSON schema、每文件 dictionary、lint 后非零退出 |
| `packages/web/src/routes/docs/contributors/architecture/+page.md` | 官方架构地图 | core / LS / JS 的职责分层 |
| `packages/web/src/routes/docs/contributors/testing-strategy/+page.md` | 质量与隐私边界 | unit/integration/manual/production feedback；用户报告 suggestion 时可 POST |
| `AGENT_POLICY.md` | Agent contribution policy | 小 PR、以人类价值/issue 为依据、披露 LLM 使用 |

#### ⭐ 源码精读 1：Document 把 parser 输出变成可复用语义中间层

`harper-core/src/document.rs:70-80,175-219`：

```rust
pub fn new_from_chars(
    source: Lrc<[char]>,
    parser: &impl Parser,
    dictionary: &impl Dictionary,
) -> Self {
    let tokens = parser.parse(&source);
    let mut document = Self { source, tokens };
    document.parse(dictionary);
    document
}

fn parse(&mut self, dictionary: &impl Dictionary) {
    self.apply_fixups();
    let chunker = burn_chunker();
    let tagger = brill_tagger();
    // sentence POS tagging + noun-phrase chunking + dictionary metadata
}
```

逻辑摘要：输入格式差异被隔离在 `Parser`，后续所有规则消费统一 `Document`。span 使用字符下标而非 UTF-8 byte offset，CLI JSON 也明确输出 `char_start/char_end`，减少跨 Rust/JS/编辑器定位错位。边界是构建 Document 会执行 tag/chunk 和 dictionary lookup，不是零成本；大文档仍需预算与增量策略。

#### ⭐ 源码精读 2：Linter 是窄契约，缓存是被允许的内部状态

`harper-core/src/linting/mod.rs:341-353`：

```rust
pub trait Linter: LSend {
    /// Analyzes a document and produces zero or more Lints.
    /// We pass `self` mutably for caching purposes.
    fn lint(&mut self, document: &Document) -> Vec<Lint>;

    /// A user-facing description of the rule.
    fn description(&self) -> &str;
}
```

逻辑摘要：规则输入只有 immutable Document，输出只有 lints；`&mut self` 的用途被注释限定为 caching。这样的 contract 便于 unit test、WASM/LSP/CLI 复用和 rule-by-rule 配置。边界是 Rust 类型本身没有禁止实现者执行 I/O；项目约定与 code review 仍要守住纯规则边界。

#### ⭐ 源码精读 3：缓存键同时绑定文本内容与配置

`harper-core/src/linting/lint_group/mod.rs:935-987`：

```rust
for chunk in document.iter_chunks() {
    let chunk_chars = document.get_span_content(&chunk_span);
    let config_hash = self.hasher_builder.hash_one(&self.config);
    let char_hash = self.hasher_builder.hash_one(chunk_chars);
    let cache_key = (char_hash, config_hash);

    let chunk_results = if let Some(hit) = self.chunk_expr_cache.get(&cache_key) {
        hit.clone()
    } else {
        let pattern_lints = run_enabled_chunk_rules(/* ... */);
        self.chunk_expr_cache.put(cache_key, pattern_lints.clone());
        pattern_lints
    };
    // cached relative spans are shifted back into document-space
}
```

逻辑摘要：只按文本缓存会在规则开关改变后返回旧结果，因此 key 包含 config hash；缓存内部保存 chunk-relative spans，复用到文档时恢复 offset。这个模式适用于 Hermes 对稳定段落重复做确定性校验。边界是 hash collision 虽概率低但并非形式证明，cache 容量/淘汰策略会影响长期驻留内存，且当前 desktop memory issue 的根因不能据此猜测。

#### ⭐ 源码精读 4：WASM facade 组合 parser 装饰器并显式去重

`harper-wasm/src/lib.rs:397-425`：

```rust
pub fn lint(
    &mut self,
    text: String,
    language: Language,
    all_headings: bool,
    regex_mask: Option<String>,
    dedup: bool,
    isolate_english: bool,
) -> Vec<Lint> {
    let Some(parser) = self.create_lint_parser(
        language, all_headings, regex_mask, isolate_english,
    ) else { return vec![]; };

    let document = Document::new_from_chars(source.clone(), &parser, &self.dictionary);
    let mut lints = self.with_curated_config(|group| group.lint(&document));
    self.ignored_lints.remove_ignored(&mut lints, &document);
    if dedup { remove_overlaps(&mut lints); }
    lints.into_iter().map(/* WASM output */).collect()
}
```

逻辑摘要：WASM 层不重写规则，只负责 parser policy、配置、忽略项、overlap 和序列化。无效 regex mask 返回空结果并发 warning；复用时这类“配置错误→看似 clean”应改为结构化 error，否则质量门可能 fail open。

#### 依赖分析与供应链风险

根 Cargo workspace 真实解析到 **21** 个 member，release profile 使用 `panic="abort"` 与 fat LTO。`harper-core/Cargo.toml` 版本 **2.6.0**、edition 2024、License Apache-2.0，关键依赖包括：

- `fst 0.4.7`、`trie-rs 0.4.2`、`levenshtein_automata 0.2.1`：词典与拼写候选核心；字典数据/构建产物需纳入 provenance。
- `harper-brill` path dependency：POS tagging / chunking；内部 crate 版本与 workspace release 要同步。
- `pulldown-cmark 0.13.3`：Markdown parsing；恶意/极端 markup 应做性能 fixture。
- `cached 0.59.0`、`lru 0.18.0`：缓存能力；长期服务和 desktop 必须监控容量与生命周期。
- `regex 1.12.3`：mask / rule path；无效配置的 fail-open 行为要在调用层修正。
- `zip 8.6.0` 关闭默认 feature，只启用 deflate：减小 feature 面，但仍需把 archive input 当不可信数据处理。
- `serde` / `serde_json`：WASM、CLI JSON、config 边界；schema/version 应稳定。
- `Cargo.lock` 与 `pnpm-lock.yaml` 都存在；Rust + Web + Tauri + browser extensions 构成较大的多生态供应链。

GitHub check-runs 快照：固定提交共 30 条，28 success、2 failure；两条 failure 都名为 Dependabot。包括 `just test-rust`、`just check-desktop`、web build 与多平台 harper-cli/harper-ls binary jobs在 API 快照中显示 success，但这只是 GitHub 对该提交的 check 状态，不替代本地复现。两条 Dependabot failure 原因仍**待核验**。

#### 可复用经验

- **当多个前端需要相同质量判断时，应优先把 parser、语义中间层和 rule engine 放入无 UI 的 core，再让 CLI/LSP/WASM 做薄 adapter，因为这样同一规则可被一致测试；边界是各 adapter 的 mask、ignore、offset 与 fail-open 行为仍需契约测试。**
- **当缓存结果受配置影响时，应优先把内容哈希和配置哈希共同纳入 key，而不是只按输入文本缓存，因为规则开关变化会使旧结果失效；边界是还要设置容量、淘汰和可观测指标。**
- **当处理用户私有文本时，应优先在本地执行确定性检查，并只持久化必要的 hash/统计，而不是默认上传原文，因为质量门不需要把全部上下文交给远端；边界是用户主动报告与某些集成的网络行为必须单独披露。**
- **当质量工具遇到无效配置时，应优先返回结构化 `blocked/invalid_config`，而不是空结果，因为“没有发现问题”和“检查根本没运行”不能共用 clean 状态；边界是交互式 UI 可降级，但 CI 必须 fail closed。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/local-writing-quality-gate/` 做两阶段 POC：

1. 不改现有报告，先准备 5 个英文 Markdown fixture：clean、拼写错误、code fence、专有名词、invalid regex mask。
2. 在隔离环境下载/校验官方 `harper-cli` artifact 或使用可复现 Cargo build（本机当前无 Rust 工具链，故本轮不执行）。
3. 运行 JSON 输出，wrapper 统一映射为 `completed_clean / completed_with_findings / blocked / failed`。
4. 对 raw inbox 只在本地 lint；产物只保留 rule、span、message、artifact version/hash，不复制全文到新的 runtime log。
5. 将 invalid mask 明确映射为 `blocked`，验证不能伪装成 clean。

成功标准：相同 fixture 重复得到稳定 JSON；字符 span 能定位 Unicode 文本；invalid config 非零/blocked；无网络调用；artifact hash 可追溯。本轮仅设计，不安装依赖、不修改 cron。

#### 风险边界

- **License**：Apache-2.0，允许改编/再分发但需履行版权、LICENSE/NOTICE 等义务；如只调用官方 binary，也要记录版本和 provenance。
- **语言局限**：README 明确当前只支持 English；不能把它作为中文日报的通用文风裁判。
- **准确性局限**：rule-based grammar checker 会有 false positive/false negative；项目官方也通过用户报告寻找高误报 linter。不能自动应用 suggestion 到 curated memory 或用户原文。
- **隐私边界**：core/CLI 可本地运行，但 testing docs 写明用户主动报告错误 suggestion 时会 POST 到官网；接入前需关闭/隔离任何 telemetry/reporting path并抓包验证。
- **资源风险**：open issues [#3874](https://github.com/Automattic/harper/issues/3874) 与 [#3714](https://github.com/Automattic/harper/issues/3714) 分别报告 desktop 长时间运行后约 41GB、21.3GB 内存占用；均是用户报告，根因与是否来自 core cache**待核验**，但足以要求 long-run RSS test。
- **配置风险**：WASM 的无效 regex mask 返回空 lint；wrapper 若不区分，会 fail open。
- **维护活跃度**：API pushed_at 为当天；固定提交当天产生，最近 release v2.6.0 为一个月内，维护活跃。683 个 open issues 表明生态面广，不能只凭活跃度推断稳定性。
- **构建验证缺口**：本机没有 cargo/rustc；没有声称本地 tests pass。GitHub check-runs 也有 2 条 Dependabot failure。
- **不适用场景**：中文、多语种、需要深层事实一致性或领域术语语义审查时，Harper 不能替代人工/LLM review；它更适合作为英文机械质量的第一道本地门。

#### Skill 升格判断

**结论：需二次验证。**

不复制 Harper 规则源码到 shared skill。候选是 `local-writing-quality-gate` workflow：选择受支持语言、固定 artifact、JSON schema、四状态、字符 span、invalid-config fail closed、只建议不自动修改。它具有跨 agent 复用价值，但必须先验证 artifact provenance、无网络、Unicode span、RSS 长跑、false-positive golden set 和 License 义务。验证通过后才考虑 shared skill；当前不自动升格。

#### Hermes / shared hub 落地路径

1. **Runtime POC**：`runtime/hermes/github-learning-poc/local-writing-quality-gate/`；fixture、binary metadata、JSON 结果只留 runtime。
2. **Hermes wrapper 候选**：`scripts/local_writing_quality_gate.py --input <path> --language english --format json`，输出四状态与 evidence hash，不自动改文件。
3. **学习闭环候选接点**：在 `scripts/github_learning_orchestrator.py --audit-only` 现有结构审计之后，以 optional gate 检查英文摘要/代码注释；工具缺失时标记 blocked，不降低事实审计结果、不伪装 clean。
4. **数据最小化**：只处理显式 allowlist 文件；不把 raw inbox 内容上传，不复制完整原文到 runtime 诊断；只保存 span/rule/version/hash。
5. **共享 Skill 候选**：验证后可建 `capabilities/skills/foundation/local-writing-quality-gate/` 并更新 manifest；Skill 只描述调用契约、状态、安全边界和验证命令。
6. **治理**：不自动接受 suggestion，不写 curated active fact，不修改模型/provider/auth/env/cron。

## 经验沉淀

1. **当多个消费者需要同一事实时，应优先构建分阶段、可查询、带 source location 的语义模型，而不是让每个 Agent 重读文本，因为统一模型能减少语义漂移；边界是 stage 转换与有损字段必须可见。**
2. **当 Agent 面对层级树或依赖图时，应优先提供有 visit budget 的批量查询和显式截断信号，而不是循环调用单节点工具，因为可控的 incomplete 比无界遍历或悄悄截断更可靠；边界是 response cap 不等于 compute cap。**
3. **当工具注册表同时包含查询和写入时，应优先用逐工具 effect metadata + 实现审计决定授权，而不是相信 server 级“全部只读”说明，因为自然语言与调用链会漂移；边界是 metadata 本身也要通过 contract test。**
4. **当确定性检查结果受用户配置影响时，应优先用 `content_hash + config_hash + engine_version` 形成 cache/evidence key，而不是只按输入缓存，因为规则或引擎升级会改变结论；边界是还要限制 cache 容量。**
5. **当质量工具因依赖、配置或 parser 错误没有真正运行时，应优先输出 `blocked/failed`，而不是空 findings，因为 clean 和 not-run 是不同状态；边界是下游必须拒绝把 blocked 汇总成 passed。**
6. **当处理用户文本或内部架构时，应优先本地执行、最小化持久化并明确任何外发路径，因为 prompt、diagram 和原文都可能包含敏感信息；边界是用户明确授权的报告/模型调用仍需独立证据。**

## 风险边界（跨项目）

- 不自动安装、启动或接入热门项目；不自动开放 MCP HTTP，不调用任何 OpenClaw 运行时。
- 不修改 Hermes/OpenClaw 配置、model、provider、auth、env、cron 或 secret。
- 不把 GitHub Stars 当质量评分；Stars 只是 07:31–07:35 CST 的 API 快照。
- 不直接写 curated active fact；候选反哺只作为后续治理输入。
- `NOASSERTION` 仓库不复制源码；GPL 代码不混入 shared capability，除非先完成合规/隔离评审。
- 不把 README 性能/隐私宣传、单个 issue 报告或 GitHub check-run 改写成“本地已复现”。
- 两个项目的固定提交 check-runs 都含 Dependabot failure；本机又缺满足条件的完整 toolchain，因此运行层仍有待核验项。
- 任何“写 snapshot”“应用 suggestion”“改 architecture source”动作都必须显式审批并产出 diff；巡检/质量门默认只报告。

## Skill 升格总判断

- `likec4/likec4` → **需二次验证**：候选为 `architecture-evidence-query-contract`，不是完整 LikeC4 或上游 skill。
- `Automattic/harper` → **需二次验证**：候选为 `local-writing-quality-gate` workflow，不复制规则源码。
- 今日不修改 `capabilities/skills/` 或 manifest：两个候选都缺少 runtime fixture POC、资源/隐私验证和跨项目适配证据，尚不满足 shared class-level 能力门槛。

## 明日继续

1. 最小动作：实现 `architecture-evidence-model` 的 4 个 fixture：illegal stage、10,000-node traversal budget、truncated result、read-only declaration vs write effect drift。
2. 在隔离环境为 Harper 获取官方 artifact provenance，并用 5 个 English/Unicode fixture验证 JSON、exit code、invalid mask 与无网络；若无法验证则继续标记 blocked。
3. 对 LikeC4 release package 做 `npm pack`/runtime dependency smoke test（需先提供满足 Node `>=22.22.3` 的隔离环境），复核 v1.59.2 的 npx 修复。
4. 复核 LikeC4 `apply-semantic-layout` 是否在 MCP 客户端 UI 中被正确标注为写操作；如果没有，形成 upstream issue candidate，而不是本地默默绕过。
5. 为 Harper desktop memory issue 设计 8 小时 RSS fixture；没有复现前不归因 core cache。

## 候选反哺

### Candidate Facts

- [ ] topic: explicit-model-stages-prevent-agent-querying-unready-data | evidence: `likec4/likec4@f9700621` 的 `LikeC4.ts`、`compute-view.ts`、`LikeC4Model.ts` | 建议: create（POC 通过后） | 安全级别: low
- [ ] topic: tool-effect-metadata-must-match-implementation | evidence: LikeC4 `createMCPServer.ts` 的“All tools are read-only”与 `apply-semantic-layout.ts` 的 `save-view-snapshot` 调用链冲突 | 建议: create 或 update verification-first fact | 安全级别: high
- [ ] topic: deterministic-local-quality-core-with-thin-adapters | evidence: `Automattic/harper@efa59c33` 的 architecture docs、`Document`、`Linter`、`LintGroup`、CLI/WASM adapter | 建议: create（fixture 后） | 安全级别: medium
- [ ] topic: cache-keys-must-bind-content-config-and-engine-version | evidence: Harper chunk/sentence cache 使用 content+config hash；engine version 为本地适配补充要求 | 建议: update existing verification/caching guidance | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: architecture-evidence-query-contract | 可复用场景: Hermes/future agent 查询 shared hub 项目关系与证据位置 | 是否建议 shared: yes（需二次验证） | 原因: stage、bounded traversal、truncation、effect metadata 是跨 Agent 稳定契约
- [ ] 名称: local-writing-quality-gate | 可复用场景: 英文日报/文档/代码注释的本地机械质量门 | 是否建议 shared: yes（需二次验证） | 原因: 可减少外发，且四状态/JSON/span/provenance 可统一多个 agent
- [ ] 名称: likec4-full-platform-or-upstream-dsl-skill | 可复用场景: 完整 architecture-as-code 产品 | 是否建议 shared: no | 原因: 产品特定、依赖重、含写工具与大量 references，不应整包复制为 shared skill
- [ ] 名称: harper-rule-source-copy | 可复用场景: 英文规则库 | 是否建议 shared: no | 原因: License/更新/字典/测试成本，应优先调用固定 artifact 而非 fork 源码

### Candidate Open Questions

- [ ] 问题: shared hub 的项目索引是否需要 `parsed/computed/layouted` 三阶段，还是 `raw/validated/indexed` 更贴合现有治理？ | reason: adaptation | priority: high
- [ ] 问题: Hermes 工具系统能否强制校验 effect metadata 与实际文件/network side effects，而不只依赖说明？ | reason: gap | priority: high
- [ ] 问题: LikeC4 `subgraph-summary` 对超大模型是否需要 `maxVisited`，当前是否已有上层 cancellation 保证？ | reason: gap | priority: medium
- [ ] 问题: Harper CLI 的无效 mask 路径是否同 WASM 一样返回空结果，wrapper 如何统一 fail closed？ | reason: gap | priority: high
- [ ] 问题: Harper desktop #3874/#3714 的内存增长来自 overlay、integration、cache 还是其他路径？ | reason: gap | priority: medium
- [ ] 问题: 本地英文质量门的 false-positive golden set 应来自哪些经用户确认的 shared 文档？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动改 Hermes/OpenClaw 配置、模型、provider、auth、env、cron 或 secret。
- 不调用、启动或修改 OpenClaw 运行时。
- 不直接写 `curated/memory/facts/`、active project 状态或 shared skill manifest。
- 不默认启用 LikeC4 MCP HTTP、`apply-semantic-layout` 或任何 workspace 写工具。
- 不自动应用 Harper suggestion，不上传 inbox/curated 原文，不把 empty lint 当 clean。
- 不复制 License 未判定/GPL 仓库源码；不整包复制 LikeC4 upstream skill 或 Harper rules。

## 证据索引

- Trending 原页：`runtime/hermes/github-hot-project-learning/evidence/2026-07-24/trending.html`
- 候选 API 快照：`runtime/hermes/github-hot-project-learning/evidence/2026-07-24/repos.jsonl`
- LikeC4 API/release/issue/checks：`runtime/hermes/github-hot-project-learning/evidence/2026-07-24/api/likec4-likec4/`
- Harper API/release/issues/checks：`runtime/hermes/github-hot-project-learning/evidence/2026-07-24/api/Automattic-harper/`
- 固定提交 checkout：
  - `runtime/hermes/github-hot-project-learning/evidence/2026-07-24/likec4/`
  - `runtime/hermes/github-hot-project-learning/evidence/2026-07-24/harper/`
- 核心链接：
  - [LikeC4 README](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/README.md)
  - [LikeC4 v1.59.2](https://github.com/likec4/likec4/releases/tag/v1.59.2)
  - [LikeC4 issue #3141](https://github.com/likec4/likec4/issues/3141)
  - [LikeC4 MCP registry](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/packages/mcp/src/server/createMCPServer.ts)
  - [LikeC4 semantic layout tool](https://github.com/likec4/likec4/blob/f9700621c2bd8cc6c002d54b813a4d251e3f7bd8/packages/mcp/src/tools/apply-semantic-layout.ts)
  - [Harper README](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/README.md)
  - [Harper architecture docs](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/packages/web/src/routes/docs/contributors/architecture/%2Bpage.md)
  - [Harper testing strategy](https://github.com/Automattic/harper/blob/efa59c33b2915108f52c385ce1e3311a3cfa1439/packages/web/src/routes/docs/contributors/testing-strategy/%2Bpage.md)
  - [Harper v2.6.0](https://github.com/Automattic/harper/releases/tag/v2.6.0)
  - [Harper issue #3874](https://github.com/Automattic/harper/issues/3874)
  - [Harper issue #3714](https://github.com/Automattic/harper/issues/3714)
