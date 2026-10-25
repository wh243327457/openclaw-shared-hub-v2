---
type: case
status: draft
created: 2026-10-26
updated: 2026-10-26
domain: learning
tags: [github-learning, living-spec, headless-agent, provenance, verification]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
---

# 2026-10-26 GitHub 热门项目学习报告

> 执行者：Hermes；按任务约束未调用 OpenClaw。  
> 查询窗口：2026-10-26 06:30–07:38（宿主 UTC+09:00）；最终项目元数据快照为 `2026-10-25T22:37:51Z`。发现入口是 GitHub Trending daily 的真实 HTML，随后用 GitHub Repository / License / Commit / Release / Issues / Checks / Actions / Security Advisories API 核验。  
> 深读固定提交：`JetBrains/thinkrail@d299f20d2ba014f382ddbcc9b49f2aa63fada132`；`makecindy/cindy@7c5bd270c956417127e12a74934d0ecdb97ba55d`。  
> 本次真实读取 README、架构/模块 docs、release/issues、依赖声明、CI 与关键源码；本机成功浅克隆两仓库，但 **Bun 未安装**，本机 ThinkRail 测试命令返回 `bun: command not found`。因此运行语义不以本机测试背书；仓库 Actions 结果与源码静态分析分开陈述。

## 抓取口径

| 查询类型 | URL / 命令入口 | 抓取时间（UTC） | 用途与筛选算法 |
|---|---|---|---|
| GitHub Trending | `https://github.com/trending?since=daily` | 2026-10-25 21:30 后 | 从页面 `<article>` 项目链接提取 11 个候选；只深读与 Agent/持续上下文/工程验证强相关者 |
| Repository + License API | `gh api repos/{owner}/{repo}`、`gh api repos/{owner}/{repo}/license` | 最终快照 2026-10-25T22:37:51Z | stars、forks、语言、license、created/pushed/updated；两条 license API 相互核对 |
| Commit / Release / Issues | `commits/main`、`releases`、`issues?sort=updated` | 2026-10-25 21:34–22:38Z | 固定源码版本；检查发布节奏、当前维护问题，不把 `updated_at` 单独当代码活跃证据 |
| Checks / Actions / Advisories | fixed-head check-runs、actions runs/jobs、security-advisories | 2026-10-25 21:34–22:38Z | 核验 CI 与公开安全公告；空 advisory 仅表示没有公开仓库 advisory，不等于无漏洞 |
| 源码 | `git clone --depth 1` + 本地文件读取 | 2026-10-25 21:32–22:38Z | tree、函数签名、依赖与 tests；结论锚定上述固定 commit |

> 证据快照：`runtime/hermes/github-hot-project-learning/evidence/2026-10-26/`。Stars 会继续变化；表内数值是最终 API 快照，不是增长率。GitHub Repository API 的 `open_issues_count` 混合 issue 与 PR，不解读为纯 issue 数。

## 今日结论

**可持续 Agent 系统的关键不是把更多上下文塞进 prompt，而是把知识、运行配置和执行结果分别做成“可验证的图 / 冻结输入 / 带来源与完整度的证据”：ThinkRail 展示了 living specs + 派生图索引，Cindy Headless 展示了 profile digest + runtime receipt。**

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | 114,525 | 22,123 | Python | Apache-2.0 | 2026-10-16T21:38:46Z | 多 Agent 金融协作；金融结论与数据风险高，今日不扩散主题 |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 87,599 | 5,235 | Rust | Apache-2.0 | 2026-10-25T18:04:24Z | 设计 skill + deterministic detectors；已有连续速览，避免重复深读 |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | 86,664 | 9,598 | Python | AGPL-3.0 | 2026-10-25T22:27:08Z | 大型本地语音栈；AGPL 与模型/数据 license 面广，另题处理 |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 46,752 | 2,898 | JavaScript | MIT | 2026-09-14T19:29:02Z | 安全审计 skill；2026-10-22 已深读，今日去重 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 33,625 | 1,752 | CSS | MIT | 2026-10-22T17:20:32Z | 分层 UI gates + fresh-context review；可后续与 Impeccable 对照 |
| [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) | 11,584 | 1,479 | Rust | Apache-2.0 | 2026-10-25T13:23:00Z | 机器人方向活跃，与 shared hub 当前优先级较远 |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 4,794 | 660 | TypeScript | Apache-2.0 | 2026-10-25T20:26:51Z | **深读：多 harness headless profile、输入冻结、证据工件与完整度** |
| [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | 1,591 | 100 | TypeScript | Apache-2.0 | 2026-10-25T21:32:26Z | **深读：living spec 图、派生索引、worktree 隔离与 hydrate-then-stream** |

## 深读项目

### 1. JetBrains/thinkrail

- **一句话判断**：值得学的是让“架构说明”成为带稳定 ID 和显式边的 living spec 图，同时坚持 Markdown 文件为真相源、索引只是可丢弃派生物；这比无限追加一份线性 `MEMORY.md` 更能治理长期 Agent 上下文。
- **解决的问题**：替代“README、架构文档、任务计划和 Agent prompt 各自维护一份关系”的旧做法；旧做法容易出现重复 ID、断链、环、过期索引和不同工作任务互相污染。
- **URL / API 快照**：https://github.com/JetBrains/thinkrail ；**Stars: 1,591 / Forks: 100 / Language: TypeScript / License: Apache-2.0（Repository API + License API）**；`created_at=2026-07-08T07:40:43Z`，`pushed_at=2026-10-25T21:32:26Z`，`updated_at=2026-10-25T22:36:33Z`，Repository API open issues/PR count `198`。
- **固定提交 / release**：[`d299f20d2ba014f382ddbcc9b49f2aa63fada132`](https://github.com/JetBrains/thinkrail/commit/d299f20d2ba014f382ddbcc9b49f2aa63fada132)，commit time `2026-10-25T13:39:01Z`；latest release [`v0.3.0-nightly.6`](https://github.com/JetBrains/thinkrail/releases/tag/v0.3.0-nightly.6)，published `2026-10-25T06:49:25Z`，明确是 prerelease/nightly。
- **来源交叉核验**：README；`architecture.md`；`packages/spec-graph/{SPEC.md,core/*}`；`packages/server/src/workspaces/{SPEC.md,workspaces.ts}`；release notes；最新 issues；root/package manifests；CI workflow、Actions jobs 与 fixed-head Checks。

#### 架构 / 实现与数据流

```text
Markdown specs（文件真相源）
  frontmatter: id/type/parent/depends-on/references/implements
                 |
                 v
        SpecIndex.scan()
  stable traversal + mtime/size parse cache
                 |
                 v
 buildGraph() --> nodes / typed edges / forward / reverse / duplicateIds
                 |
      +----------+-----------+
      |                      |
      v                      v
spec_* Agent tools      host Specs viewer
      |                      |
      +------ same pi-free core ------+

project repo
   |
   +--> Default workspace（用户 repo，不回收）
   +--> managed git worktree（独立 branch/cwd）
   +--> attached external worktree（用户拥有，不改名/回收）
                 |
        chats / files / terminals
                 |
       host authoritative state
                 v
       clients hydrate, then stream deltas
```

核心机制：

1. **真相与索引分离**：`packages/spec-graph/SPEC.md` 明确 filesystem 是 source of truth，图是内存只读派生物。每次读取重扫文件集合，仅对 `(mtimeMs,size)` 变化项重解析；文件新增、删除或改变 spec 身份都会进入下一次结果。
2. **一个关系模型给 Agent 和 UI 共用**：portable package 给 pi 提供 7 个 `spec_*` tools；host 的 Specs viewer 直接 value-import 无 pi 依赖的 `core`。因此 Agent 与人看到同一 parser / is-a-spec rule / graph，而不是两个实现。
3. **路径门同时检查词法与文件系统语义**：`resolveSpecPath` 拒绝 absolute、`..`、Windows drive/stream、ignored dir 和路径中的 symlink，并返回索引真正会报告的 canonical spelling；不存在或无法列目录时 fail closed。
4. **图错误显式化**：`validateGraph` 输出 dangling links、duplicate IDs、parent cycles。`buildGraph` 对重复 ID 采用稳定遍历下“首文件暂时赢”，但同时保留所有重复路径，验证器不会把它当成功。
5. **工作隔离用 git primitive，不用 prompt 约定**：`createWorkspace` 创建独立 branch + worktree；managed/default/external 三类有不同所有权。默认项目目录和外部 worktree 禁止被回收；scratch dir 检查真实目录与 symlink 后才写入自忽略 `.gitignore`。
6. **客户端不是第二真相源**：`architecture.md` 的 hydrate-then-stream 要求客户端先读取 host 当前 projects/workspaces/sessions/transcripts，再订阅 delta；断线重连通过读模型修复漏掉的事件。

#### repo tree 摘要

```text
thinkrail/
├── README.md / architecture.md / goal-and-requirements.md
├── apps/
│   ├── cli/                      # browser launcher
│   ├── desktop/                  # Electrobun 本地主机 launcher
│   └── web/                      # React client，只有 wire 依赖
├── packages/
│   ├── contracts/                # typed/versioned wire
│   ├── server/                   # host、workspace/session/persistence/git
│   ├── spec-graph/               # portable living-spec graph + 7 tools + skill
│   ├── shared/                   # host-side shared primitives
│   ├── pi-delegation|pi-subagents|pi-dag/
│   └── artifact-tests/           # source/artifact 边界验证
├── pi-extensions/                # 可在 vanilla pi 运行的 packages
├── thinkrail-extensions/         # pi + server + web 三段式扩展
├── e2e/ / scripts/ / patches/   # gates、artifact/E2E、受控补丁
└── package.json / bun.lock       # Bun workspace；核心版本集中 exact-pin
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/spec-graph/core/store.ts` | 文件索引与路径边界 | 稳定遍历、忽略目录、mtime/size cache、symlink/path containment、按需 graph cache |
| `packages/spec-graph/core/graph.ts` | 图投影 | 从 frontmatter 生成 node/typed edge、forward/reverse adjacency、duplicate ID 清单 |
| `packages/spec-graph/core/validate.ts` | 完整性 gate | dangling link、duplicate ID、parent cycle 三类验证 |
| `packages/spec-graph/core/core.test.ts` | 机制回归测试 | 外部增删改、CRLF/BOM、Windows namespace、Unicode/case、symlink escape 等 fixtures |
| `packages/server/src/workspaces/workspaces.ts` | worktree 生命周期 | managed/default/external ownership、ref validation、persist-then-publish、scratch hardening |
| `architecture.md` | 全局边界 | host/wire/client 三环、hydrate-then-stream、domain/view state、exact pin、portable packages |
| `.github/workflows/ci.yml` | conformance gates | deps/boundaries/spec surface、unit、vanilla-pi parity、artifact smoke/E2E、Windows paths |

#### ⭐ 源码精读

1. `resolveSpecPath(root, path) -> SpecPathResolution`：在“文件尚未创建”时也计算 index-compatible canonical path，并拒绝路径逃逸与 symlink。

```ts
export function resolveSpecPath(root: string, path: string): SpecPathResolution {
  if (path.trim() === "") return { error: "Path must not be empty." };
  if (isAbsolute(path)) return { error: `Path must be root-relative, not absolute: ${path}` };
  if (process.platform === "win32" && hasWindowsNamespaceSyntax(path)) {
    return { error: `Path must not use Windows drive or stream syntax: ${path}` };
  }
  const segments = normalize(path).split(sep);
  if (segments.includes("..")) return { error: `Path must stay inside the project root: ${path}` };
  // ... resolve each segment against directory entries ...
  if (isSymlink(walked)) {
    return { error: `Path passes through a symlink, which the index never follows: ${path}` };
  }
  if (!isPathInsideRoot(root, walked)) return { error: `Path must stay inside the project root: ${path}` };
  return { rel: canonical.join("/"), abs: walked };
}
```

逻辑摘要：不是只做 `path.includes("..")`；它还区分 Windows namespace、父目录可列性、on-disk spelling 和 symlink。边界是 `SpecIndex` 的缓存仍只看 mtime+size，文档承认“同一 mtime tick 且同长度”的理论漏检；严格场景需 content hash。

2. `SpecIndex.scan() / graph()`：把图当可重建 read model，不把 cache 提升为权威状态。

```ts
private scan(): SpecFileRecord[] {
  const seen = new Set<string>();
  const specs: SpecFileRecord[] = [];
  let changed = false;
  for (const abs of this.walk(this.root)) {
    seen.add(abs);
    const stat = statSync(abs);
    let entry = this.cache.get(abs);
    if (!entry || entry.mtimeMs !== stat.mtimeMs || entry.size !== stat.size) {
      const content = readFileSync(abs, "utf8");
      const { frontmatter } = parseFile(content);
      entry = { rel: toRel(this.root, abs), mtimeMs: stat.mtimeMs, size: stat.size,
        content: isSpec(frontmatter) ? content : "", frontmatter };
      this.cache.set(abs, entry);
      changed = true;
    }
    if (isSpec(entry.frontmatter)) specs.push({ abs, rel: entry.rel, content: entry.content, frontmatter: entry.frontmatter });
  }
  for (const abs of [...this.cache.keys()]) if (!seen.has(abs)) { this.cache.delete(abs); changed = true; }
  if (changed) this.graphCache = null;
  return specs;
}

graph(): SpecGraph {
  const specs = this.scan();
  if (this.graphCache === null) this.graphCache = buildGraph(specs.map(r => ({ path: r.rel, frontmatter: r.frontmatter })));
  return this.graphCache;
}
```

逻辑摘要：read 时重扫集合，cache 只节省 parse/build；外部工具改文件也能被下一次 read 看到。边界是同步 filesystem API 面对极大树可能阻塞；当前实现通过 ignore 与 cache 降成本，不等于无限规模索引。

3. `buildGraph(entries) -> SpecGraph` 与 `validateGraph(graph)`：先投影所有关系，再用单独 gate 判定图是否可接受。

```ts
export function buildGraph(entries: SpecFileEntry[]): SpecGraph {
  const nodes = new Map<string, SpecNode>();
  const pathsById = new Map<string, string[]>();
  for (const entry of entries) {
    const id = scalar(entry.frontmatter, FIELDS.id);
    const type = scalar(entry.frontmatter, FIELDS.type);
    if (id === undefined || type === undefined) continue;
    push(pathsById, id, entry.path);
    if (!nodes.has(id)) nodes.set(id, { id, type, title: scalar(entry.frontmatter, FIELDS.title), path: entry.path, frontmatter: entry.frontmatter });
  }
  // ... produce typed forward/reverse edges ...
  const duplicateIds = new Map([...pathsById].filter(([, paths]) => paths.length > 1));
  return { nodes, edges, forward, reverse, duplicateIds };
}

export function validateGraph(graph: SpecGraph): ValidationReport {
  // every typed target must exist
  // duplicateIds are surfaced, not silently discarded
  return { danglingLinks, duplicateIds, parentCycles: findParentCycles(graph) };
}
```

逻辑摘要：查询模型可以在存在错误时仍给出诊断，但 `isValid` 只有三类错误都为零才通过。边界是它验证的是结构一致性，不证明 prose 正确、事实新鲜或 link 语义合理。

4. `createWorkspace(...) -> Promise<Workspace>`：把并行任务映射到 git 可审计隔离单元。

```ts
export async function createWorkspace(projectId: string, name?: string, baseRef?: string): Promise<Workspace> {
  const project = openProjectById(projectId);
  const branch = name ? uniqueBranch(project, toBranch(name)) : nextAutoBranch(project);
  const baseBranch = baseRef?.trim() || currentBranch(project.path);
  assertSafeRef(baseBranch);
  // missing remote ref may be fetched asynchronously, then the ref is re-checked
  const worktreePath = join(dataDir(), "worktrees", project.slug, branch);
  const added = git(project.path, ["worktree", "add", worktreePath, "-b", branch,
    "--no-track", "--end-of-options", remoteBase ?? baseBranch]);
  if (!added.ok) throw new Error(`git worktree add failed: ${added.err}`);
  const workspace = { id: randomUUID(), projectId, name: name ?? branch, branch,
    worktreePath, baseBranch, initialTerminalPending: true, lastActiveAt: Date.now() };
  ensureWorkspaceScratchDir(workspace);
  const all = loadWorkspaces(); // awaited work 后重读，避免 stale snapshot 覆盖并发写
  all.push(workspace); saveWorkspaces(all); emit({ kind: "created", workspace });
  return workspace;
}
```

逻辑摘要：隔离、branch identity、base provenance、状态持久化和 lifecycle event 形成一份 workspace receipt。边界是 worktree 隔离不是 OS sandbox；工作区内恶意代码仍需独立进程/网络/secret policy。

#### 依赖分析与供应链风险

- root 固定 `bun@1.4.4`，catalog 集中 exact-pin `@earendil-works/pi-* 1.2.0`、`typebox 1.3.27`、`typescript 6.0.3`、`turbo 2.9.18`、`@playwright/test 1.61.0` 等；`pi-spec-graph` runtime 只依赖 `yaml 2.9.0`，pi/typebox 是 peer dependencies。
- 仓库有 `bun.lock`、`patchedDependencies` 与 `trustedDependencies`；CI 的 `check:deps` 拒绝浮动 ranges/catalog drift，`check:boundaries`、`check:spec-surface` 和 vanilla-pi under Node parity 强化边界。
- **供应链缺口**：所读 `ci.yml` 使用 `actions/checkout@v5`、`oven-sh/setup-bun@v2` 等 tag，而非完整 commit SHA；仓库顶层没有 `.github/dependabot.yml`，是否由组织级策略补足待核验。顶层 Apache-2.0 不替代 npm transitive、Electrobun、release binaries 与 patches 的逐项审查。
- fixed-head Checks API 为 **17/17 success**。主分支 push 只出现 `CI cache`；最近 PR CI run `40235978911` 的 Unit Tests、Lint & Typecheck、no-agent E2E、Windows binary smoke、Pi package parity 与 `CI passed` success，但该 run 是另一 head SHA，不把它冒充 fixed-head 全套验证。
- 本机 `bun test packages/spec-graph` 没有执行：系统不存在 Bun，真实输出为 `bun: command not found`。因此源码测试结果只引用 upstream Actions，不写成本地通过。
- Public Security Advisories API 返回 `[]`；只能说明未查询到公开 advisory。仓库根没有 `SECURITY.md`，私密披露入口/响应 SLA 待核验。

#### 可复用经验

- 当长期知识同时被 Agent 与人读取时，应优先保留可审查文本为 source of truth、图/索引为可重建 projection，因为缓存或数据库一旦成为第二真相源就会产生漂移；边界是大规模树需要 hash/incremental backend。
- 当知识条目之间存在 parent/dependency/reference 关系时，应优先用稳定 ID + typed edge + dangling/duplicate/cycle validator，因为“相关链接列表”不能机器判定结构完整性；边界是结构通过不证明内容真实。
- 当多个 Agent 任务会并行修改同一 repo 时，应优先用 git worktree/branch/cwd 做隔离，而不是靠 prompt 约定“不碰别人文件”；边界是 worktree 不隔离进程、网络和 secret。
- 当客户端可能断线或多端并发时，应优先 hydrate authoritative reads 再 stream deltas，因为仅靠事件见证无法修复漏包与重启；边界是 read/delta 必须有一致 identity/version contract。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/shared-memory-graph-validator-v0/` 做**只读 synthetic fixture**：扫描 5 个假的 curated facts/projects frontmatter，构建 `{id,type,parent,related,path}` 图；验证 duplicate ID、dangling link、parent cycle、symlink path 四类错误，并生成 `report.json`。不更改现有 curated，不建立第二真相源，不引入 ThinkRail/pi 依赖。

#### 风险边界

- **License**：Repository + License API 均为 Apache-2.0；依赖、Electrobun、icons/fonts、补丁与发布制品另审，复制代码要保留 notice。
- **维护活跃度**：固定提交为 2026-10-25，nightly.6 同日发布、issues 当日更新、fixed-head checks 全 success；但 latest 是 nightly prerelease，接口/存储/wire 仍可能快速变化。
- **安全风险**：Agent 在 host 内 in-process 运行，`architecture.md` 明确“no crash isolation”；git worktree 不是 sandbox。workspace path/ref/scratch 虽有 hardening，未知 repo 的 build/tool 仍可访问宿主能力。
- **供应链风险**：Actions 未全 SHA pin；没有仓库级 Dependabot 文件和根 `SECURITY.md`（组织级能力待核验）；portable package peer deps 由 host 提供，兼容性依赖 conformance gate。
- **局限性**：SpecIndex 用 mtime+size，存在极窄的同 tick 同长度漏检；graph validator 不验证 prose；同步扫描大树成本待压测；spec schema 偏 ThinkRail，需要映射 shared hub 现有 frontmatter，而不是照搬。
- **不适用场景**：只有几份无关系静态文档、没有多任务并发、或不能接受 Bun/pi/桌面整体栈时，不应引入 ThinkRail 产品；最多迁移图验证机制。
- **不能自动执行**：不安装 ThinkRail、不运行未知项目、不改 shared schema/curated、不自动创建 worktree/cron/config，不把 GitHub 数据直接晋升为长期事实。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `text truth → derived graph → structural validator → bounded read` 机制，以及 worktree 的“所有权分类 + persist-then-publish”协议；不是 ThinkRail 产品或 pi extension。它与现有 `foundation/shared-memory-bridge`、shared governance 和 path portability 重叠，应先做 runtime POC，若通过则更新既有 skill/reference，不新建重复 skill。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/shared-memory-graph-validator-v0/`。
- 候选接口：`scripts/validate_memory_graph.py --root <resolved-shared-root> --report runtime/hermes/.../report.json`，仅报告不写源文件。
- 候选输入：`curated/memory/facts/*.md`、`curated/memory/projects/*.md` 的已有 frontmatter；identity 使用 canonical relative path + 显式 `id`（先审查现有 schema，不猜字段）。
- 通过 fixtures 后候选更新：
  - `capabilities/skills/foundation/shared-memory-bridge/SKILL.md`：加入 derived-index-not-truth、duplicate/dangling/cycle gate；
  - `docs/shared-governance-standard.md`：候选晋升前增加 graph consistency receipt；
  - `scripts/verify_bridge.py`：只引用 validator 结果，不把 runtime cache 写入 curated。
- 所有路径通过 `scripts/resolve_shared_root.py`；Hermes 当前只做 validator/receipt，不修改 `~/.hermes/config.yaml`。OpenClaw runtime 不存在，本轮不做其接入或配置。

### 2. makecindy/cindy（聚焦 `apps/cindy-headless`）

- **一句话判断**：值得学的是把 Agent 一次运行的“我用了什么”变成可核验工件：冻结 profile、prompt/binary/source digest、actual identity 的 evidence label、usage completeness 和 terminal result 分类，而不是只保存最终回答。
- **解决的问题**：替代“同一个任务大概用了同一个模型/配置，成功或失败看 stdout，缺失用量按 0 算”的旧做法；旧做法无法复现实验，也会把 provider 故障、Agent 失败、超时与未知成本混在一起。
- **URL / API 快照**：https://github.com/makecindy/cindy ；**Stars: 4,794 / Forks: 660 / Language: TypeScript / License: Apache-2.0（Repository API + License API）**；`created_at=2026-07-22T17:49:34Z`，`pushed_at=2026-10-25T20:26:51Z`，`updated_at=2026-10-25T22:31:10Z`，Repository API open issues/PR count `1,913`。
- **固定提交 / release**：[`7c5bd270c956417127e12a74934d0ecdb97ba55d`](https://github.com/makecindy/cindy/commit/7c5bd270c956417127e12a74934d0ecdb97ba55d)，commit time `2026-10-25T20:26:51Z`；latest stable release [`v0.1.115`](https://github.com/makecindy/cindy/releases/tag/v0.1.115)，published `2026-10-23T02:46:16Z`。
- **重要版本边界**：仓库 HEAD 是 `7c5bd270...`，但 `apps/cindy-headless/package.json` 与 `compatibility.ts` 自报 Headless `0.4.3` 基于 Cindy upstream `fa3fc88d...`。因此今日源码分析的是仓库 HEAD 中的 Headless 实现，但不能声称现成正式 bundle 已验证 HEAD 全部新变化。
- **来源交叉核验**：README；Headless README / feature parity docs；release notes；最新 issues；`profile.ts`、`host.ts`、`project-context.ts`、`memory-provider.ts`、tests；root/headless manifests；CI/CodeQL Actions 与 advisory API。

#### 架构 / 实现与数据流

```text
profile.json + optional profile.lock.json
  agent backend/binary/version/model/permissions/memory/context/MCP
                 |
      validateProfile + profileDigest + prompt digest
                 |
                 v
 runTask() -> clean temporary HOME + isolated stateDir
                 |
       project-context TOC (optional, digest)
                 |
       Maker session over one native harness
 Claude SDK | Codex app-server JSON-RPC | Pi RPC JSONL
                 |
      raw AgentEvent[] + session snapshot
                 |
     normalizeTraceEvents / extractProviderUsage
                 |
                 v
identity.json / config.json / trace.raw.jsonl / trace.jsonl
usage.json / result.json / stderr.log
  provenance       completeness       terminal class
```

核心机制：

1. **执行输入冻结**：profile 明确 backend、binary path/version、supported exact model IDs、requested model、permission mode、memory/project context、MCP、BYOM 等；canonical JSON 计算 digest。可选 `profile.lock.json` 再绑定原始文件 SHA、canonical digest、binary version、upstream commit、prompt digest。
2. **能力存在不等于已暴露**：`CINDY_FEATURE_PARITY.md` 把 Available、Core-present-but-not-exposed、Host-specific excluded 分开；“源代码里有”不会自动成为 Headless benchmark capability。
3. **安全策略 fail closed**：`bypassPermissions` 默认必须 `containerSandbox=true`，除非显式 unsafe override；remote endpoint 只允许 HTTPS 或 loopback HTTP，URL 禁嵌 credentials；secret 只以 env var 名出现在 profile。
4. **项目上下文有来源与摘要**：只读 `.cindy/project-knowledge/TOC.md`，记录 injected/reason/path/digest；prompt 包裹在 `<project-context-toc>` 中，缺失与空文件可区分。
5. **结果不压成一个布尔值**：`classifyFailure` 区分 valid completed/agent error/deadline 与 agent setup/auth/request/route/provider/signal 等 infra 类；`standardResult` 再映射标准结果。
6. **用量缺失不是 0**：usage 标记 `COMPLETE/PARTIAL/MISSING` 和 `exact/lower-bound/incomplete`；timeout/interruption 只保留观察到的下界。report 遇到未知 cost 可 fail closed 为 `cost-unknown`。
7. **自报身份披露证据等级**：`identityEvidence` 区分 provider-event、configured、operator-asserted、unknown，并把 `gatewayAttested` 固定为 false，除非未来有 request-ID lookup 或签名账单；这避免把配置名误当实际底层模型证明。

#### repo tree 摘要

```text
cindy/
├── README.md / SECURITY.md / LICENSE / LICENSE-NOTICE.md
├── apps/
│   ├── desktop/ / mobile/             # 主产品与设备宿主
│   └── cindy-headless/
│       ├── README.md / CINDY_FEATURE_PARITY.md
│       ├── capability-registry.json / harbor-compatibility.json
│       ├── profiles/                   # frozen backend/model profiles + locks
│       ├── scripts/                    # build/bundle/distribution verification
│       └── src/                        # profile、host、artifacts、benchmark、bridges
├── packages/
│   ├── maker-core/                     # Agent/session/memory substrate
│   ├── project-context/                # 项目知识发现与 TOC
│   ├── responses-* / model-compat/     # provider protocol bridges
│   └── remote-* / protocol packages   # 跨端与能力协议
├── tools/                              # pinned harness update metadata
├── .github/workflows/                  # client CI、CodeQL、release gates
└── package.json / pnpm-lock.yaml       # pnpm monorepo 与 overrides/patches
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `apps/cindy-headless/src/profile.ts` | profile schema / digest / doctor | backend-specific validation、lock verification、safe endpoint、binary/version/auth checks |
| `apps/cindy-headless/src/host.ts` | 执行与工件 | isolated HOME、session terminal、failure classification、usage normalization、7 类 artifacts |
| `apps/cindy-headless/src/project-context.ts` | context receipt | TOC 注入、缺失原因、SHA-256 digest |
| `apps/cindy-headless/src/memory-provider.ts` | Memory adapter | 复用 Maker Memory MCP，不另造 headless memory 实现 |
| `apps/cindy-headless/src/compatibility.ts` | 能力/安全报告 | registry validation、SUPPORTED/DETECTED_BUT_UNSUPPORTED、safeForUntrustedWorkloads |
| `apps/cindy-headless/CINDY_FEATURE_PARITY.md` | capability boundary | available / not exposed / excluded 分类与每次 upstream sync audit |
| `apps/cindy-headless/src/{profile,host,usage,compatibility}.test.ts` | contract tests | lock tamper、permission、infra classification、usage completeness 等 |

#### ⭐ 源码精读

1. `validateProfile(profile) -> HeadlessProfile`：把配置当执行契约，而不是宽松 options bag。

```ts
export function validateProfile(profile: unknown): HeadlessProfile {
  // ... shape and exact ID checks ...
  if (!value.supportedModelIds.includes(value.model.requestedId)) {
    throw new Error(`model ${value.model.requestedId} is not supported by this profile`);
  }
  if (value.agentBackend === 'pi' && value.permissionMode !== 'bypassPermissions') {
    throw new Error('headless pi requires bypassPermissions because no interactive approval channel is available');
  }
  if (value.unsafeAllowUnsandboxedBypass && value.permissionMode !== 'bypassPermissions') {
    throw new Error('unsafeAllowUnsandboxedBypass requires bypassPermissions');
  }
  // MCP: HTTPS/loopback HTTP, secret only via validated env-var names
  // project skill roots: workspace-relative, no parent traversal
  return value as HeadlessProfile;
}
```

逻辑摘要：backend、permission、model、MCP、project skill roots 都做组合约束，拒绝“字段各自合法但整体不可执行”的 profile。边界是 schema validation 不能证明 gateway 真提供该 model，也不能证明 container runtime 正确配置。

2. `readProfile(profilePath, bundleRoot?) -> ResolvedProfile`：把 profile、prompt、binary 与 upstream revision 绑成可复核输入。

```ts
export async function readProfile(profilePath: string, bundleRoot?: string): Promise<ResolvedProfile> {
  const rawProfile = await readFile(path.resolve(profilePath), 'utf8');
  const profile = validateProfile(JSON.parse(rawProfile));
  const canonicalProfileDigest = profileDigest(profile);
  const lock = await readOptionalLock(path.dirname(profilePath));
  if (lock?.profileFile === path.basename(profilePath)) {
    if (lock.profileFileSha256 !== sha256(rawProfile)) throw new Error('profile file does not match profile.lock.json');
    if (lock.profileDigest !== canonicalProfileDigest) throw new Error('profile digest does not match profile.lock.json');
    if (lock.agentBinaryVersion !== profile.agentBinaryVersion) throw new Error('profile Agent version does not match profile.lock.json');
    if (lock.cindyUpstreamCommit !== CINDY_UPSTREAM_COMMIT) throw new Error('profile lock Cindy upstream commit is stale');
  }
  // resolve relocatable bundle resources and verify optional systemPrompt digest
  return { profile, profilePath: path.resolve(profilePath), systemPrompt, profileDigest: canonicalProfileDigest, systemPromptDigest };
}
```

逻辑摘要：同时校验“文件原始字节”和“canonical semantic digest”，并把 prompt 与 upstream commit 纳入锁。边界是 lock 与 bundle 的签名/provenance 仍需外部发行链；本地写权限被攻破时 hash 不能替代签名。

3. `assertSafeExecutionProfile(profile)`：危险权限只有在明确隔离或明确 unsafe override 时才放行。

```ts
export function assertSafeExecutionProfile(profile: HeadlessProfile): void {
  if (
    profile.permissionMode === 'bypassPermissions'
    && profile.containerSandbox !== true
    && profile.unsafeAllowUnsandboxedBypass !== true
    && process.env.CINDY_HEADLESS_ALLOW_UNSANDBOXED_BYPASS !== '1'
  ) {
    throw new Error(
      'bypassPermissions requires containerSandbox=true; set CINDY_HEADLESS_ALLOW_UNSANDBOXED_BYPASS=1 only in a controlled environment'
    );
  }
}
```

逻辑摘要：不能因为 headless 没有交互审批就静默把 bypass 变默认裸奔。边界是 `containerSandbox: true` 仍是 profile 声明；需要外部 runtime attestation 才能独立证明容器确实隔离。

4. `classifyFailure(...)` 与 `standardResult(...)`：基础设施失败不算 Agent 能力失败。

```ts
export function classifyFailure(error: string | undefined, terminalError: AgentEvent | undefined, deadlineKilled: boolean): string {
  if (deadlineKilled) return 'valid-deadline-killed';
  if (error?.startsWith('HEADLESS_TERMINATED_')) return 'infra-terminated-signal';
  if (!error && !terminalError) return 'valid-completed';
  const text = `${error ?? ''} ${terminalError ? JSON.stringify(terminalError.data) : ''}`.toLowerCase();
  if (/native binary not found|enoent/.test(text)) return 'infra-agent-setup';
  if (/auth|api.?key|unauthorized|401/.test(text)) return 'infra-invalid-auth';
  if (/model.*(not found|unsupported)|route/.test(text)) return 'infra-invalid-route';
  if (/5\d\d|rate.?limit|provider|network|timeout|stream disconnected/.test(text)) return 'infra-invalid-provider';
  return 'valid-agent-error';
}
```

逻辑摘要：对 benchmark/cron 特别重要：provider 502、401、binary 缺失与模型本身答错不能混成一个失败率。边界是 regex 分类会受错误文本变化影响；长期应优先使用 typed upstream errors，regex 作为 fallback。

5. `runTaskWithIsolatedEnvironment(...)` 的 artifact write：每次运行输出 identity/config/raw+normalized trace/usage/result。

```ts
await Promise.all([
  writeFile(join(outputDir, 'identity.json'), JSON.stringify(identity, null, 2) + '\n'),
  writeFile(join(outputDir, 'config.json'), JSON.stringify(configReceipt, null, 2) + '\n'),
  writeFile(join(outputDir, 'trace.raw.jsonl'), rawEvents),
  writeFile(join(outputDir, 'trace.jsonl'), normalizedEvents),
  writeFile(join(outputDir, 'usage.json'), JSON.stringify(createUsageArtifact({
    usageStatus, usageCompleteness, usageSource, missingFields,
    termination, observedTokenTotal
  }), null, 2) + '\n'),
  writeFile(join(outputDir, 'result.json'), JSON.stringify(result, null, 2) + '\n'),
]);
```

逻辑摘要：raw trace 保证可追溯，normalized trace 避免 delta+final 重复计数；identity evidence 不声称 gateway attestation；usage unknown 不伪装成零。边界是 artifacts 本身可能含敏感 tool/event payload，保存位置、保留期和脱敏策略必须由 host 管理。

#### 依赖分析与供应链风险

- root 要求 Node `>=22.12`、pnpm `>=10.7 <11`，`packageManager` 固定到带完整 integrity 的 `pnpm@10.33.2...`；有 `pnpm-lock.yaml`、9 个 overrides、14 个 patched dependencies，native/build deps 包括 Electron、better-sqlite3、node-pty、sharp。
- `apps/cindy-headless` runtime 依赖 workspace 内 `@cindy/maker-core`、`@cindy/mcps` 与 `@modelcontextprotocol/sdk ^1.29.0`；dev dependencies `esbuild ^0.28.1`、TypeScript `^5.7.0`、Vitest `^3.2.4`。虽然 lockfile 冻结实际图，manifest 仍用 ranges，升级审查依赖 lock diff 与 Dependabot。
- `.github/dependabot.yml` 每周巡检 GitHub Actions 与 root npm，open PR 上限 5。CI 使用 SHA-pinned `pnpm/action-setup@0977...`，但其他 Actions 是否全 SHA pinned 本次未穷举。
- fixed-head Checks API 为 **20/20 success**；Actions run `40230808942` 的 Linux/Windows unit shards、Git integration、runner/database checks 全 success；`40230808230` 的 CodeQL actions/javascript-typescript/python/go/rust/c-cpp/csharp 全 success。
- Public Security Advisories API 返回 `[]`；不代表无漏洞。`SECURITY.md` 提供 GitHub private advisory / email 渠道、5 工作日确认和 90 天协调披露窗口。
- Headless 正式 bundle 包含三种 Agent runtime 时供应链/体积显著增大；README 要求 manifest 记录 source/upstream/prompt/binary digest 并在 scored run 前验证。**本次没有构建 bundle、没有真实 provider run，也没有验证 formal archive**。
- HEAD 与 Headless frozen upstream baseline 不同：若直接拿 HEAD 源码配旧 bundle，会违反其自身 maintenance rule；此项是高优先级版本漂移风险。

#### 可复用经验

- 当 Agent 运行结果要用于审计、评测或自动化决策时，应优先保存 input digest + actual identity evidence + raw/normalized trace + terminal class，而不是只保存最终文本，因为没有运行 receipt 就无法区分配置漂移和模型行为；边界是 receipt 也需可信存储/签名。
- 当某能力只存在于共享 core、但当前 runner 没有稳定入口时，应优先标记 `present-but-not-exposed/unsupported`，因为“代码存在”不等于当前执行面可用；边界是 capability registry 必须随 upstream diff 持续维护。
- 当 usage/cost 只观察到一部分时，应优先用 `PARTIAL/lower-bound` 或 `MISSING/incomplete`，而不是补 0，因为 0 会污染成本预算与模型比较；边界是完整度仍依赖 provider event contract。
- 当高权 headless runner 没有交互审批时，应优先要求真实 sandbox 并 fail closed，而不是为了不挂起就默认裸 `bypassPermissions`；边界是 config flag 不是隔离证明，需要 runtime attestation。
- 当 gateway 中请求模型名、实际 route 与底层模型可能不同，应优先分别记录 requested/observed/operator-asserted/gateway-attested 字段，因为配置名不能证明实际模型；边界是没有签名账单/request lookup 时应明确 `gatewayAttested=false`。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/run-receipt-envelope-v0/` 用**纯 synthetic 数据**定义：

```json
{
  "input": {"task_digest":"...","instruction_digest":"...","config_digest":"..."},
  "identity": {"requested_model":"...","observed_model":null,"evidence":"configured","gateway_attested":false},
  "result": {"terminal":"completed|agent_failed|infra_failed|blocked|inconclusive"},
  "usage": {"status":"complete|partial|missing","completeness":"exact|lower-bound|incomplete"},
  "artifacts": ["stdout.log","report.md","audit.json"]
}
```

写 6 个 fixture 覆盖 401、502、timeout、有结果无 usage、requested/observed 不同、config digest 漂移；checker 禁止把 unknown cost 当 0。只写 runtime，不读真实 secret、不改模型/provider/config/cron。

#### 风险边界

- **License**：Repository + License API 均为 Apache-2.0；`LICENSE-NOTICE.md`、子包、模型/语音数据、Electron/native binaries、Agent harness 和第三方服务许可需另审。
- **维护活跃度**：fixed commit 2026-10-25、latest stable v0.1.115 于 2026-10-23、HEAD CI/CodeQL success、issues/PR 当日活跃；但仓库变化极快、open issues/PR count 1,913，兼容面和回归面很大。
- **安全风险**：产品横跨桌面/移动/远程/MCP/provider/voice/credentials；Headless 的 bypass、remote MCP、BYOM 和 project skills 都是高权输入。Profile flag、digest 和 clean HOME 降低漂移，但不等于容器/网络/secret 强隔离。
- **版本风险**：Headless 0.4.3 frozen upstream `fa3fc88...` 落后于仓库 HEAD `7c5bd270...`；必须重做 parity audit、tests、bundle verify 和 smoke 才能声称覆盖 HEAD。
- **身份风险**：`actualModelId` 可来自 provider event 或 operator assertion，`gatewayAttested=false`；不能把它升级成底层模型独立证明。尤其经过自建 gateway 时，应保留请求名、路由名和可验证上游证据的区别。
- **数据风险**：raw trace/stderr/config receipt 可能包含文件路径、tool arguments、remote URLs 或用户内容；必须限定 runtime、脱敏和保留期，不能自动进入 curated/shared skill references。
- **局限性**：failure 分类部分依赖 regex；formal bundle 与 live model 本次未执行；Security Advisory API 只覆盖公开项；README 的能力声明不能替代 runtime test。
- **不适用场景**：普通一次性本地聊天无需整套 benchmark artifacts；若没有 sandbox、不能管理三 harness 供应链，或不需要跨 runner 对照，不应引入 Cindy Headless 本体。
- **不能自动执行**：不安装 Cindy、不下载 Agent binaries、不连接 gateway/MCP、不读取 API key、不运行 unknown benchmark、不修改 Hermes profile/provider/config/cron，不把 artifacts 写入 curated。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `frozen input profile → execution receipt → provenance labels → completeness-aware audit`，与现有 `autonomous-learning/orchestrator-protocol`、reflection engine、GitHub learning audit 重叠。应先用 synthetic fixtures 验证，再更新已有 shared skill；不引入 Cindy runtime，不创建“第二套 orchestrator”新 skill。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/run-receipt-envelope-v0/`。
- 候选 schema：`runtime/hermes/<workflow>/runs/<run-id>/{identity.json,config.json,result.json,usage.json,evidence-index.json}`；runtime only，不进 Git main/curated。
- 候选修改：
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：增加 `input_digest/config_digest/runner/evidence/terminal/completeness`；
  - `scripts/github_learning_orchestrator.py`：status 增加 evidence path、audit issues 与 knowledge-base copy receipt；unknown 不等于 zero/success；
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：区分本机验证、upstream CI、README 声明与待核验；
  - `scripts/reflection_engine.py`：infra failure 与 content/audit failure 分桶，避免错误经验进入反思统计。
- Hermes 可复用的是通用 receipt，不读取或改写 `~/.hermes/config.yaml`。OpenClaw runtime 不存在，本轮不操作其配置；future agent 可读取同一中性 schema。

## 经验沉淀

1. 当共享知识从线性文档增长为多项目、多事实、多依赖时，应优先保留文本真相源并派生 typed graph + validator，因为第二份权威数据库会漂移；边界是图只证明结构，不证明事实。
2. 当缓存或索引用于持续上下文时，应优先设计为可删除、可重建、带输入摘要的 projection，因为 runtime 产物不应反向污染 curated；边界是大规模性能要另做压测。
3. 当多个 Agent 并行工作时，应优先用 worktree/branch/cwd 隔离写面并显式标注 managed/user-owned 资源，因为生命周期操作若不区分所有权会误删用户目录；边界是工作区隔离不替代 sandbox。
4. 当 cron、评测或审计依赖 Agent 结果时，应优先保存 frozen input digest、terminal class 与 evidence index，因为仅有“命令返回 0”无法说明任务真正完成；边界是 receipt 需要防篡改和保留策略。
5. 当 provider/model 身份经过网关时，应优先把 requested、observed、operator-asserted、gateway-attested 分层记录，因为模型名映射不等于底层身份；边界是没有独立 attestation 就必须保持 unknown/false。
6. 当 usage、cost 或 source coverage 不完整时，应优先保留 `partial/missing/inconclusive` 状态，而不是填 0 或默认成功，因为未知值会污染预算、排名和反思；边界是下游必须真正支持这些终态。
7. 当上游 monorepo 的子系统宣称固定在旧 upstream commit 时，应优先核对 source HEAD、subsystem baseline、bundle manifest 和 smoke evidence 四者一致，因为仓库活跃不等于当前制品覆盖最新代码；边界是 rebuild 也不替代 live integration test。

## 风险边界总表

| 维度 | JetBrains/thinkrail | makecindy/cindy Headless | 本轮动作 |
|---|---|---|---|
| License | Apache-2.0；依赖/桌面制品另审 | Apache-2.0；子包/模型/Agent binaries 另审 | 只抽象模式，不复制代码 |
| 维护活跃度 | 2026-10-25 push；nightly prerelease；198 open count | 2026-10-25 push；stable v0.1.115；1,913 open count | 固定 commit，API 快照 |
| CI | fixed-head 17 checks success；本机无 Bun | fixed-head 20 checks success + client CI/CodeQL success | 不声称本机项目测试通过 |
| 安全 | in-process Agent、worktree 非 sandbox；无根 SECURITY.md | 高权多协议；Headless bypass 依赖 sandbox 声明 | 不安装、不接 secret/provider |
| 数据 | spec prose 真实性不由图保证 | raw trace/artifacts 可能含敏感上下文 | runtime-only + 脱敏候选 |
| 版本 | nightly/API 快速变动 | Headless frozen baseline 与 repo HEAD 不同 | 标记待 parity/build/smoke |
| 不适用 | 小型无关系文档 / 无并发任务 | 普通聊天 / 无 sandbox / 不做评测 | 只做 synthetic POC 候选 |

## Skill 升格总判断

- **JetBrains/thinkrail：需二次验证**。先做 shared-memory graph validator；若通过，只更新 `foundation/shared-memory-bridge` / governance，不引入 ThinkRail/pi。
- **makecindy/cindy Headless：需二次验证**。先做 run receipt envelope fixtures；若通过，只更新 `autonomous-learning/orchestrator-protocol` 与 GitHub learning audit，不引入 Cindy runtime。
- **今日不直接写 curated active fact、不新建 shared skill**：两个模式都有明显跨 agent 价值，但与既有 shared skills 重叠；应遵守“先 runtime fixture、再去重审查、后更新现有 class-level skill”。

## Hermes / shared hub 落地路径

1. `runtime/hermes/github-learning-poc/shared-memory-graph-validator-v0/`：5 个 synthetic docs，验证 duplicate/dangling/cycle/symlink；输出只读 report。
2. `runtime/hermes/github-learning-poc/run-receipt-envelope-v0/`：6 个 synthetic run fixtures，验证 infra/content failure、identity evidence、usage completeness、digest drift。
3. POC 均通过后，再候选更新：
   - `capabilities/skills/foundation/shared-memory-bridge/SKILL.md`
   - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`
   - `capabilities/skills/research/github-hot-project-learning/SKILL.md`
   - `docs/shared-governance-standard.md`
4. 不新增重复 skill；不把 runtime report 复制进 references；路径均由 `scripts/resolve_shared_root.py` 解析。
5. 本轮不改 Hermes/OpenClaw/future-agent 配置、模型、provider、cron、auth 或 secret。

## 明日继续

- **最小动作 1**：实现 `shared-memory-graph-validator-v0` 的纯 Python synthetic checker，限定 30 分钟；停止条件是只证明 structural receipt，不自动修改任何 Markdown。
- **最小动作 2**：实现 `run-receipt-envelope-v0` JSON Schema + 6 fixtures，明确 `completed ≠ evidence_complete`、`unknown_cost ≠ 0`、`configured_model ≠ attested_model`。
- **最小动作 3**：核验 ThinkRail spec graph 在大目录下的扫描开销与 content-hash escalation；核验 Cindy Headless `fa3fc88... → 7c5bd270...` 是否已有正式 parity/bundle smoke。
- **停止条件**：若 POC 与现有 shared-memory bridge / orchestrator protocol 完全重复且无新增 failure fixture，则只补 reference 或不落地，不新建能力。

## 候选反哺

### Candidate Facts

- [ ] topic: 长期 Agent 上下文应采用 text truth + derived typed graph + structural receipt | evidence: `JetBrains/thinkrail@d299f20...` 的 `spec-graph/{SPEC.md,core/*}` 与 tests | 建议: update（与 shared-memory bridge 去重） | 安全级别: low
- [ ] topic: Agent 自动化结果需同时记录 frozen input、identity evidence、terminal class 与 completeness | evidence: `makecindy/cindy@7c5bd270...` 的 Headless `profile.ts/host.ts/compatibility.ts` | 建议: update orchestrator protocol | 安全级别: medium
- [ ] topic: requested model / observed model / operator assertion / gateway attestation 必须分层 | evidence: Cindy Headless `identityEvidence` 与 README 的 `gatewayAttested:false` 边界 | 建议: candidate，结合现有 gateway 事实治理审查 | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: shared-memory-graph-validator-v0 | 可复用场景: curated facts/projects 与 future-agent 知识图一致性 | 是否建议 shared: yes（验证后更新既有 skill） | 原因: 跨 agent 横切，但不应新建重复 skill
- [ ] 名称: run-receipt-envelope-v0 | 可复用场景: cron / 调研 / 巡检 / benchmark 的可恢复、可审计状态 | 是否建议 shared: yes（验证后更新既有 orchestrator protocol） | 原因: 能区分结果、证据、身份和完整度

### Candidate Open Questions

- [ ] 问题: shared 当前 facts/projects frontmatter 是否已有稳定 `id/parent/related` 契约，还是只能先以 canonical path 为 identity？ | reason: adaptation | priority: high
- [ ] 问题: ThinkRail mtime+size cache 在 WSL/跨文件系统下是否会出现可复现同 tick 同长度 stale read？ | reason: gap | priority: medium
- [ ] 问题: Cindy Headless frozen upstream `fa3fc88...` 到 repo HEAD `7c5bd270...` 的正式 parity audit、bundle verify、live smoke 是否已完成？ | reason: stale | priority: high
- [ ] 问题: Hermes cron 的 status.json 是否应区分 `execution_completed`、`evidence_complete`、`knowledge_base_copied` 与 `delivery_pending`？ | reason: adaptation | priority: high

### 不应自动落地

- 不安装或运行 ThinkRail/Cindy 产品，不下载 Agent binaries，不连接 gateway/MCP，不读取凭据。
- 不改 Hermes/OpenClaw config、provider、model、cron、auth；OpenClaw runtime 本轮不存在且未调用。
- 不把 GitHub stars、README 声明、空 advisory、CI success 或模型自报身份晋升为长期事实。
- 不把 runtime evidence/trace/raw logs 写入 curated 或 shared skill references；只在 fixtures、治理评分和人工/总控审查通过后更新 class-level 契约。
