# 2026-11-02 GitHub 热门项目学习日报

> 执行者：Hermes；本次未调用 OpenClaw。
>
> 发现入口：2026-11-02 06:43–07:39 JST 真实读取 `https://github.com/trending?since=daily`，随后使用 GitHub Repository / License / Commit / Release / Issues / Checks / Security Advisories API 交叉核验。
>
> 深读固定源码：`thedotmack/claude-mem@c239a048a8a07607148f4c1f26b258ccfb28b80d`；`lightpanda-io/browser@c3b9247c4f979a75b61947925b8584b79bd25c1f`。Stars 是 07:39 JST 前后 Repository API 快照，会继续变化。
>
> 验证边界：本次只在 `/tmp` 浅克隆源码；未安装 claude-mem、未改 Hermes 配置。实际运行了 claude-mem Hermes adapter 的定向测试与纯函数 smoke；实际下载并运行 Lightpanda 1.0.2 Linux release，完成网页 fetch 和 MCP session 复现。未运行两个仓库的完整构建/全量测试，未完成全部依赖 license / reachability 审计。

## 今日结论

**持续上下文与浏览器自动化的共同难点不是“功能能跑”，而是 scope、隐私、终态和可回收性：记忆必须把采集、脱敏、检索、注入与发布分层；共享浏览器必须把每个 Agent 的 session identity、生命周期 tombstone、网络入口和最终效果验证做成宿主强制契约。**

## 项目速览

API 查询窗口：2026-11-02 07:32–07:39 JST。`NOASSERTION` 只表示 GitHub License API 未识别，不等于没有许可。

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | 494,509 | 55,198 | Python | MIT | 2026-11-01T18:22:08Z | Trending 高热清单仓；信息密度偏目录，不做源码深读 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 109,140 | 9,559 | TypeScript | Apache-2.0 | 2026-11-01T21:01:59Z | **深读：跨 Agent capture→compress→retrieve→inject 与 Hermes adapter** |
| [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | 45,314 | 7,493 | Python | MIT | 2026-04-13T12:38:49Z | 金融模型；最后 push 较早，和 shared hub 主线较远 |
| [lightpanda-io/browser](https://github.com/lightpanda-io/browser) | 40,045 | 1,959 | Zig | AGPL-3.0 | 2026-11-01T09:35:11Z | **深读：Agent-native browser、MCP session isolation 与 lifecycle 缺口** |
| [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | 37,757 | 8,899 | TypeScript | MIT | 2026-11-01T22:23:20Z | 高活跃 coding UI；open issue/PR 计数 3,876，范围过大 |
| [cjpais/Handy](https://github.com/cjpais/Handy) | 36,476 | 3,447 | Rust | MIT | 2026-10-27T09:23:19Z | 离线语音转写，后续可审隐私与 native model 供应链 |
| [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | 10,463 | 1,448 | TypeScript | Apache-2.0 | 2026-11-01T19:48:30Z | VM 型 Bot，权限面大；本轮不安装、不执行 |

> 速览数据均来自真实 Repository API。顶层 license 不覆盖依赖、模型、训练数据、网页内容、商标或 release assets。

## 深读项目

### 1. thedotmack/claude-mem

- **链接**：https://github.com/thedotmack/claude-mem
- **固定源码提交**：[`c239a048a8a07607148f4c1f26b258ccfb28b80d`](https://github.com/thedotmack/claude-mem/commit/c239a048a8a07607148f4c1f26b258ccfb28b80d)，commit time `2026-11-01T21:01:57Z`；GitHub verification 为 `unsigned`。
- **GitHub API**：**Stars: 109,140**；Forks `9,559`；Language `TypeScript`；**License: Apache-2.0**（License API 路径 `LICENSE`）；`created_at=2025-08-31T20:50:03Z`，`updated_at=2026-11-01T22:37:59Z`，`pushed_at=2026-11-01T21:01:59Z`，API `open_issues_count=171`（含 PR）。
- **latest release**：[`v15.8.1`](https://github.com/thedotmack/claude-mem/releases/tag/v15.8.1)，published `2026-11-01T20:04:20Z`。Release 说明该版本主要清理 repo，npm 包内容不变。
- **一句话判断**：值得学的是把多 harness 的事件采集、低权压缩、progressive recall、context injection 和 fail-soft host adapter 串成闭环；不应直接照搬其“自动采集全部活动”的产品默认到 shared hub。
- **解决的问题**：替代“每轮把全部聊天塞回 prompt”或“只靠 Agent 自己手写 MEMORY.md”的旧做法；前者上下文成本高，后者遗漏大且难以跨 Agent 检索。
- **来源交叉核验**：README 的 How It Works / MCP Search Tools；Hermes adapter README；`package.json`；`.github/SECURITY.md`；v15.8.1 release；Issues #5260/#5262；固定提交源码；GitHub Checks API；本机定向测试。

#### repo tree 摘要

固定提交浅克隆共 `2,852` 个非 `.git` 文件，其中 `.ts=1,852`、`.tsx=102`、`.md=158`、`.json=152`。

```text
claude-mem/
├── src/
│   ├── cli/                 # hook CLI、session init、deliverables capture
│   ├── services/worker/     # capture queue、provider、session/observer 生命周期
│   ├── storage/             # SQLite/Postgres memory 与 event repositories
│   ├── servers/             # MCP stdio/HTTP 与 progressive search tools
│   ├── sdk/                 # observation/summary prompt 与低权 SDK options
│   └── shared/              # hook I/O、path、context cache、search 公共契约
├── hermes/claude-mem/       # Hermes memory provider（Python 标准库）
├── openclaw/                # 另一宿主 adapter；本次未调用、未运行
├── plugin/                  # hooks、modes、skills、SQLite/native bundle
├── services/                # sync-api / sync-hub / viewer-host
├── tests/hermes/            # Hermes provider contract tests
├── docs/                    # API、privacy、capture、架构说明
└── package.json             # monorepo 脚本、Node/Bun 版本与依赖
```

#### 架构 / 数据流

```text
Hermes lifecycle / hooks
  ├─ on_turn_start → prompt event
  ├─ post_tool_call → bounded tool observation
  ├─ on_session_end → summary request
  └─ prefetch / system_prompt_block ← recall
                 │
                 v
        bounded async client queue
                 │
        local Worker HTTP / hosted /v1
                 │
    raw events → Observer compression → observations
                 │
        SQLite/Postgres + FTS/vector index
                 │
 search(index) → timeline → selected full observations
                 │
          low-authority context injection
```

核心分层成立，但必须区分两类事实：

1. **capture truth**：prompt、tool input/output、session summary 等原始事件；
2. **generated observation**：Observer/模型压缩出的派生记忆，不应自动升级成用户事实或 shared curated truth。

Hermes adapter 的 README 映射了 `on_turn_start`、`post_tool_call`、`prefetch`、`system_prompt_block`、`on_memory_write` 和 session end；本次源码同时确认 scheduled agent 的写入会被关掉，但仍可 recall。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `hermes/claude-mem/client.py` | Hermes→worker/server transport | 标准库 HTTP、递归 privacy tag stripping、后台有界队列、3 次失败后 30 秒 breaker、读写 timeout |
| `hermes/claude-mem/__init__.py` | Hermes provider adapter | 生命周期映射、scheduled agent read-only、按 session 路由 tool hook、低权 memory injection label |
| `src/sdk/hardened-options.ts` | Observer/KnowledgeAgent capability lockdown | `tools=[]`、空 MCP/settings、`dontAsk`、最终 `canUseTool` deny + audit |
| `src/servers/mcp-server.ts` | progressive recall / context injection | `search → timeline → get_observations`，session context 委托 worker；读写工具 metadata 分开 |
| `src/storage/sqlite/memory-items.ts` | memory item + FTS search | project scope、64 distinct term cap、CJK/未分词脚本 substring fallback、parameterized SQL |
| `src/services/sqlite/SessionStore.ts` | observation durable store | content hash dedup、FTS trigger/schema migrations、storeObservation seam |
| `.github/SECURITY.md` | security / privacy contract | 最新版支持策略、私密标签、命令执行安全规范；文档声明的 path 规则仍需实现级复核 |

#### ⭐ 源码精读 1：Observer 工具能力 fail-closed

签名：`buildHardenedSdkOptions(input: HardenedSdkOptionsInput): Options`

```ts
export function buildHardenedSdkOptions(input: HardenedSdkOptionsInput): Options {
  const canUseTool: Options['canUseTool'] = async (toolName, toolInput) => {
    recordObserverToolAttempt({
      source: input.source,
      sessionDbId: input.sessionDbId,
      contentSessionId: input.contentSessionId,
      project: input.project,
      tool_name: toolName,
      tool_input: toolInput,
      result: 'denied',
    });
    return {
      behavior: 'deny',
      message: `${input.source} is forbidden from tool use (claude-mem hard lockdown).`,
    };
  };
```

逻辑不是只写“Observer 不应调用工具”，而是同时移除默认工具、MCP、settings inheritance 和额外目录，并保留最终 deny callback。这种 belt-and-suspenders 外壳值得迁移：**压缩器只处理提供给它的文本，不应获得文件、网络或宿主工具权限。**

```ts
  return {
    model: input.model,
    cwd: input.cwd ?? ensureObserverSessionsDir(),
    env: input.env,
    tools: [],
    allowedTools: [],
    disallowedTools: [...OBSERVER_DISALLOWED_TOOLS],
    permissionMode: 'dontAsk',
    canUseTool,
    additionalDirectories: [],
    mcpServers: {},
    settingSources: [],
    strictMcpConfig: true,
  };
}
```

边界：这是 SDK 配置层 defense-in-depth，不是 OS sandbox；`env` 内容、模型 endpoint、宿主进程权限和数据出域仍需独立控制。

#### ⭐ 源码精读 2：context injection 先强制 project scope

签名：`handleSessionStartContext(args: SessionStartContextArgs)`

```ts
async function handleSessionStartContext(
  args: SessionStartContextArgs,
): Promise<{ content: Array<{ type: 'text'; text: string }>; isError?: boolean }> {
  const projects = normalizeProjectsArg(args);
  if (projects.length === 0) {
    return {
      content: [{ type: 'text', text: 'session_start_context: "project" or "projects" is required' }],
      isError: true,
    };
  }

  return callWorker('/api/context/inject', {
    query: {
      projects: projects.join(','),
      ...(args.platformSource !== undefined ? { platformSource: normalizeMcpPlatformSource(args.platformSource) } : {}),
      ...(args.full !== undefined ? { full: args.full } : {}),
      ...(args.colors !== undefined ? { colors: args.colors } : {}),
    },
    text: true,
  });
}
```

这避免“无 scope 默认搜全库”。但 project string 的 canonical identity、ACL、跨 worktree 规则仍取决于下游；shared hub 不能把 display name 直接当跨 Agent 权威身份。

#### ⭐ 源码精读 3：检索先 compact index，再按 ID 展开

签名：`MemoryItemsRepository.search(projectId, query, limit)`

```ts
search(projectId: string, query: string, limit = 20): MemoryItem[] {
  const { words, symbols, substrings } = buildSearchQuery(query);
  if (!words && symbols.length === 0 && substrings.length === 0) return [];

  const conditions = ['memory_items.project_id = ?'];
  const parameters: Array<string | number> = [projectId];
  const ftsCondition = `memory_items.id IN (
    SELECT memory_item_id FROM memory_items_fts
    WHERE project_id = ? AND memory_items_fts MATCH ?
  )`;
```

其查询构造对 distinct term 做 `64` 上限，普通词走 FTS，Han/Hiragana/Katakana/Hangul/Thai 等未分词脚本额外走 literal substring；所有动态值使用参数，不拼进 SQL。最后按 `updated_at_epoch DESC` 有界返回。

```ts
  const rows = this.db.prepare(`
    SELECT memory_items.*
    FROM memory_items
    WHERE ${conditions.join(' AND ')}
    ORDER BY memory_items.updated_at_epoch DESC
    LIMIT ?
  `).all(...parameters) as MemoryItemRow[];
  return rows.map(mapMemoryItemRow);
}
```

值得迁移的是 README 与 MCP 工具共同表达的三层 recall：`search` 返回紧凑索引，`timeline` 看邻近上下文，`get_observations(ids)` 只展开选中的全文。README 声称约 10× token saving；**该数字本次未独立 benchmark，标记待核验**。

#### ⭐ 源码精读 4：Hermes 写入 fail-soft，但队列满会丢最新写入

签名：`ClaudeMemClient._enqueue(job)` / `_run()`

```python
def _run(self) -> None:
    while True:
        job = self._queue.get()
        try:
            if job is None:
                return
            job()
        except Exception:
            pass
        finally:
            self._queue.task_done()

def _enqueue(self, job: Callable[[], None]) -> None:
    try:
        self._queue.put_nowait(job)
    except self._queue_full:
        pass
```

好处是 memory worker 挂掉不阻塞 Hermes 主任务；代价是队列满时 newest write 静默丢失，且 `_run` 吞掉异常。产品上这是 availability-first，不是 durable capture。若 shared hub 采用类似模式，必须补 `dropped_count / last_error / drain receipt / replay spool`，否则“没有记忆”无法区分无事件与丢事件。

#### 依赖分析与供应链风险

`package.json` 要求 Node `^20.19.0 || >=22.12.0`、Bun `>=1.1.31`。运行依赖直接列出 `better-auth`、`@better-auth/api-key`、`sharp`；dev 图包含 Anthropic SDK、MCP SDK、Express、Postgres/Redis 客户端、React、DOMPurify、Zod、TypeBox 和多语言 tree-sitter grammar。`plugin/bun.lock`、各 service 的 `bun.lock`、viewer `package-lock.json` 分散存在，但根目录没有单一全仓 lock。

风险判断：

- `sharp/libvips`、tree-sitter grammars、Bun compiled binary、SQLite/Chroma/uv 让安装面远大于“一个 TypeScript plugin”。
- 自动 installer 会修改宿主配置并注册 MCP；本次未执行。
- GitHub Checks API 对固定 HEAD 返回 `17` 个 check runs：`13 success / 3 skipped / 1 failure`。失败 job 是 Windows installed decoder；日志显示 media binary 实际输出 `mediaRuntime=ok` 后，清理临时 exe 遇到 `EBUSY unlink`，所以是 packaging/cleanup 风险，不可改写成“核心功能失败”或“全绿”。
- Public Security Advisories API 当前返回空数组，只能写“仓库未发布 advisory”，不能写“无漏洞”。

#### 真实验证结果

1. GitHub Contents API 下载的 `hermes/claude-mem/client.py` 与固定 clone 文件 SHA-256 完全一致：`5ea5b1d8...e13093`。
2. 本机纯函数 smoke：recursive privacy tag stripping + 3-failure circuit breaker **PASS**。
3. `python3 -m unittest tests.hermes.test_claude_mem_provider`：**38 tests，32 pass，6 fail**。六个失败都表现为当前 Hermes 环境的 `agent.runtime_cwd.resolve_agent_cwd()` 返回 `/root`，覆盖测试传入的临时 `cwd`，导致 scope / exclusion / hosted project 断言失败。源码明确设计 runtime cwd 优先；因此这是**宿主环境耦合/测试隔离风险证据**，不能直接定性为上游回归。需在 disposable venv、没有当前 Hermes import path 的环境再次运行。
4. 未运行 npm/Bun 全量测试：本机 `bun` 不存在；未将 prerequisite 缺失伪装为通过。

#### 可复用经验

- **当自动记忆压缩器只需把事件转成结构化 observation 时，应优先移除 tools/MCP/settings/additional directories，并在最终 callback deny + audit，因为 prompt 里的“不要调用工具”不是能力边界；边界是 SDK lockdown 仍不等于 OS sandbox。**
- **当长期上下文可能很大时，应优先采用 compact search → timeline → selected full records 的 progressive disclosure，因为先展开全部正文会放大 token 与隐私面；边界是排序相关性不能提升记忆 authority。**
- **当 capture 位于 Agent 热路径时，应优先 fail-soft 但同时持久化 dropped/error/drain receipt，因为静默丢最新写入会把“没有发生”与“记录失败”混为一谈；边界是 durable spool 也必须有 TTL、脱敏和容量上限。**

#### 可尝试实验（30 分钟）

在 `<shared-root>/runtime/hermes/github-hot-project-learning/poc/progressive-recall/` 建一个**不读取真实用户内容**的 synthetic JSONL：20 条假 observation，先返回 `id/title/type/time/source` 索引，再按选中的 ID 展开正文；测量 full dump 与 progressive flow 的字符数、漏召回和 source label。只做 runtime POC，不改 Hermes memory provider，不写 curated。

#### 风险边界

- **License**：仓库和 GitHub API 均为 Apache-2.0；依赖、服务端能力、模型和外部数据仍需逐项审查。
- **隐私**：项目目标就是 capture prompt/tool/session；privacy tag 是减害，不是完整 secret/PII detector。默认不得把真实 shared inbox、secret、用户 prompt 送入第三方模型。
- **Prompt injection / memory poisoning**：README/adapter 把 recalled text 标为“recorded data, not instructions”，但文本标签不是硬隔离；最终 effect 仍须 host policy。
- **维护活跃度**：固定 HEAD 在 2026-11-01 有提交，v15.8.1 同日发布，活跃；同时 churn 高，adapter/version contract 易漂移。
- **可靠性**：有界队列满时静默 drop，worker failure 被吞；适合“不阻塞主任务”，不适合宣称 exactly-once capture。
- **本机验证局限**：没有 Bun，未跑全量 suite；定向测试受当前 Hermes import/runtime cwd 污染，需干净环境复验。
- **不适用场景**：高合规审计、必须不丢事件、要求强 tenant isolation、禁止模型读取原始会话的环境。

#### ⭐ Skill 升格判断

**判断：需二次验证，暂不新增 shared skill。**

原因：progressive recall、低权 injection、raw/derived 分层、adapter fail-soft 与现有 `foundation/shared-memory-bridge`、治理标准和 shared hub 分层高度重叠；新建 `claude-mem` 专属 skill 会重复。应先把可复用契约作为 existing skill 的 candidate iteration，经 synthetic POC、干净 Hermes adapter test 和隐私 review 后再决定更新。

#### Hermes / shared hub 落地路径

不安装第三方插件、不修改 `~/.hermes/config.yaml`。候选落地：

1. 在 `<shared-root>/runtime/hermes/github-hot-project-learning/poc/progressive-recall/` 做 synthetic POC；接口只接 `search_index(query, scope, limit)`、`timeline(anchor)`、`get_selected(ids)`。
2. 在 `<shared-root>/capabilities/skills/foundation/shared-memory-bridge/SKILL.md` 的未来迭代中加入候选契约：recalled content 必须携带 `source/layer/agent/scope/revision/coverage`，并明确“data, not instruction”。本次不直接写 skill。
3. 若 POC 通过，再新增 host-neutral checker 到 `<shared-root>/scripts/`：验证 raw 只进 `inbox/<agent>`、cache/index 只进 `runtime/<agent>`、candidate 不直写 curated。
4. Hermes adapter 如需试验，应在隔离 profile/fake HOME 内完成，不自动改当前 provider、MCP、cron 或 secrets。

---

### 2. lightpanda-io/browser

- **链接**：https://github.com/lightpanda-io/browser
- **固定源码提交**：[`c3b9247c4f979a75b61947925b8584b79bd25c1f`](https://github.com/lightpanda-io/browser/commit/c3b9247c4f979a75b61947925b8584b79bd25c1f)，commit time `2026-11-01T08:37:05Z`；GitHub verification `verified=true`。
- **GitHub API**：**Stars: 40,045**；Forks `1,959`；Language `Zig`；**License: AGPL-3.0**（仓库 `LICENSING.md` 进一步写明默认 `AGPL-3.0-only`）；`created_at=2023-02-07T15:19:34Z`，`updated_at=2026-11-01T22:39:06Z`，`pushed_at=2026-11-01T09:35:11Z`，API `open_issues_count=103`（含 PR）。
- **latest release**：[`1.0.2`](https://github.com/lightpanda-io/browser/releases/tag/1.0.2)，published `2026-10-23T09:01:02Z`。
- **一句话判断**：值得学的不是“换一个更快的浏览器”口号，而是一个进程内为多个 Agent 提供独立浏览上下文、typed MCP tools、CDP/BiDi 与 deterministic script replay 的结构；当前 session termination 语义仍有可真实复现的生命周期漏洞。
- **解决的问题**：替代“每个 Agent 启一个完整 Chrome，或多个 Agent 共享同一个 page/cookie/focus”的旧做法；HTTP MCP 为每个 session 维护独立 worker/browser context，同 ID 可显式共享。
- **来源交叉核验**：README Quick start / Native MCP / Status；1.0.2 release；`SECURITY.md`、`LICENSING.md`；Issues #4350/#4348；Security Advisories API；固定源码 `src/mcp`、`src/lightpanda.zig`、`src/App.zig`、`build.zig.zon`；release asset 实测。

#### repo tree 摘要

固定提交浅克隆共 `1,467` 个 tracked/non-git 文件，其中 `.zig=689`、`.js=112`、`.md=10`。

```text
browser/
├── src/
│   ├── browser/             # DOM/Web APIs、frame/page/session、XPath/selector
│   ├── network/             # HTTP、CORS、robots、IP filter、rate limit、cache
│   ├── server/cdp/          # Chrome DevTools Protocol adapter
│   ├── server/bidi/         # WebDriver BiDi adapter
│   ├── mcp/                 # JSON-RPC router、tools、stdio/HTTP transports
│   ├── script/              # PandaScript runtime / recorder / schema
│   ├── storage/             # SQLite storage
│   ├── lightpanda.zig       # fetch orchestration 与结果写出
│   └── App.zig              # V8/platform/network/telemetry/watchdog 初始化
├── build.zig / build.zig.zon # Zig build 与 pinned source dependencies
├── orderfile/               # binary ordering/performance tooling
├── nix/ / flake.lock        # reproducible environment lane
├── LICENSE / LICENSING.md   # AGPL-3.0-only default
└── README.md / SECURITY.md
```

#### 架构 / 数据流

```text
Agent / MCP client
   │ JSON-RPC over stdio or Streamable HTTP
   v
MCP router → typed tool table → browser_tools / script runtime
   │
   ├─ default session
   └─ HTTP Mcp-Session-Id → per-session Worker thread/queue
                              │
                              v
                   Browser Session / Page / Cookie / Storage
                              │
                  DOM + V8 + Network + CDP/BiDi
                              │
                 structured result / page status / image
```

HTTP transport 的重要语义：

- `initialize` 无 session ID 时 mint `s1/s2/...`；同 ID 复用同一浏览上下文。
- 每个 worker 串行消费自己的 queue，不同 session 可并行。
- idle reaper 把 ID 放进 tombstone，后续请求返回 404；但 explicit DELETE 的当前实现没有同样 tombstone，本机已复现“已终止 session 被同 ID 复活”。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/mcp/HttpServer.zig` | 多 session MCP HTTP server | per-ID worker、mint/reap/tombstone、Host/Origin/content-type gate、DELETE/POST routing |
| `src/mcp/router.zig` | MCP JSON-RPC dispatch | parse error、method allowlist、initialize/tools/resources 分派 |
| `src/mcp/tools.zig` | typed tool registry | browser tools + `run/save/session_new/list/close`，tool annotations 与 error mapping |
| `src/lightpanda.zig` | multi-URL fetch | fresh session、每 URL page、wait budget、per-page errors、全部写出后返回首类失败 |
| `src/App.zig` | runtime bootstrap | V8 platform/snapshot、regex、fonts、watchdog、network、telemetry、arena pool 初始化与逆序释放 |
| `build.zig.zon` | dependency pins | V8 fork、brotli、zlib/zstd、nghttp2、BoringSSL、curl、SQLite、PCRE2 等 URL+hash/pinned commit |

#### ⭐ 源码精读 1：multi-URL fetch 保留 per-page failure

签名：`pub fn fetch(app: *App, browser: *Browser, urls, opts) !void`

```zig
pub fn fetch(app: *App, browser: *Browser, urls: []const [:0]const u8, opts: FetchOpts) !void {
    const notification = try Notification.init(app.allocator);
    defer notification.deinit();

    var session = try browser.newSession(notification);
    defer browser.closeSession();

    var pages: std.ArrayList(Session.PageHandle) = try .initCapacity(
        session.arena.allocator(), urls.len,
    );
    for (urls) |url| {
        const page = try session.createPage();
        const frame = page.frame().?;
        const encoded_url = try URL.resolveNavigation(frame.call_arena, url, .{});
        _ = try frame.navigate(encoded_url, navigateOpts(opts));
        pages.appendAssumeCapacity(page);
    }
```

每个 URL 有自己的 page handle；wait selector/script 错误记录在对应 slot，不因一页失败停止其他页。完成后先 `writeResults`，再按失败返回 `error.PageFailed`。

```zig
    try writeResults(app, opts, pages.items, errors, alternates);

    var failed = false;
    for (urls, pages.items, errors) |url, page, err| {
        if (err) |e| {
            failed = true;
            log.err(.app, "page failed", .{ .url = url, .err = e });
            continue;
        }
        // optional HTTP status handling follows
    }
    if (failed) return error.PageFailed;
}
```

可迁移点是“对象级 terminal + batch-level failure”，而不是 fail-fast 丢掉剩余 coverage。

#### ⭐ 源码精读 2：每个 MCP session 有独立 worker，但 ID 生命周期分两条路径

签名：`createSession` / `findOrSpawnLocked` / `closeSession`

```zig
fn findOrSpawnLocked(self: *HttpServer, id: ?[]const u8) !*Worker {
    if (id) |name| {
        if (self.workers.get(name)) |worker| return worker;
        if (self.reaped.contains(name)) return error.SessionExpired;
        return self.spawnLocked(name, null);
    }
    var buf: [16]u8 = undefined;
    while (true) {
        self.session_seq += 1;
        const candidate = std.fmt.bufPrint(&buf, "s{d}", .{self.session_seq}) catch unreachable;
        if (!self.workers.contains(candidate) and !self.reaped.contains(candidate)) {
            return self.spawnLocked(candidate, null);
        }
    }
}
```

`reap()` 会先记 tombstone，防止 expired ID 自动复活；但显式 close 只 remove worker：

```zig
pub fn closeSession(self: *HttpServer, id: []const u8) bool {
    if (Server.isDefault(id)) return false;
    self.workers_mutex.lockUncancelable(lp.io);
    defer self.workers_mutex.unlock(lp.io);
    if (self.forgetReapedLocked(id)) return true;
    const worker = self.workers.get(id) orelse return false;
    self.removeLocked(worker);
    return true;
}
```

这正是 Issue #4350 的根因。生命周期 terminal 不能只释放资源，还要留下“该 identity 已终止”的可判定记录。

#### ⭐ 源码精读 3：HTTP 入口做 content type + Origin + Host gate

签名：`serve(...)` / `checkHeaders(...)`

```zig
if (method == .POST and !isJsonContentType(request.head.content_type)) {
    return request.respond("", .{ .status = .unsupported_media_type, .keep_alive = false });
}

const session_id = checkHeaders(arena, request) catch |err| switch (err) {
    error.ForbiddenOrigin => return request.respond(
        "Origin not allowed\n", .{ .status = .forbidden, .keep_alive = false },
    ),
    error.ForbiddenHost => return request.respond(
        "Host not allowed, connect to the MCP endpoint by IP address or localhost\n",
        .{ .status = .forbidden, .keep_alive = false },
    ),
    else => return err,
};
```

`checkHeaders` 拒绝任何带 `Origin` 的请求，Host 只接受 literal IP 或 `localhost:<port>`。这能缩小 browser-origin / DNS rebinding 面，但不是 client authentication；阅读到的该 HTTP 路径未见 bearer/token 校验，远程部署需反向代理认证或 network policy，仍待完整调用链核验。

```zig
if (method == .DELETE) {
    if (session_id) |sid| _ = self.closeSession(sid);
    return request.respond("", .{ .status = .accepted, .keep_alive = keep_alive });
}

var job: Job = .{ .body = body, .out = out };
const routed = self.submit(arena, target(arena, session_id, body), &job) catch |err| switch (err) {
    error.SessionExpired => return request.respond(
        "Session expired, start a new one\n", .{ .status = .not_found, .keep_alive = keep_alive },
    ),
    else => return request.respond("", .{ .status = .internal_server_error, .keep_alive = false }),
};
```

#### ⭐ 源码精读 4：MCP router 使用有限 method map

签名：`pub fn handleMessage(server, arena, msg) !void`

```zig
pub fn handleMessage(server: anytype, arena: std.mem.Allocator, msg: []const u8) !void {
    const req = std.json.parseFromSliceLeaky(protocol.Request, arena, msg, .{
        .ignore_unknown_fields = true,
    }) catch {
        try server.sendError(.null, .ParseError, "Parse error");
        return;
    };

    const method = method_map.get(req.method) orelse {
        if (req.id != null) try server.sendError(req.id.?, .MethodNotFound, "Method not found");
        return;
    };
```

有限 method table 比任意反射 dispatch 更易审计；tool 调用仍进入更大的 typed registry，`run` 能执行 PandaScript，属于高权 effect，不能因协议 typed 就默认安全。

#### 依赖分析与供应链风险

`build.zig.zon` pin 了 V8 fork commit/tar hash、Brotli 1.2.1、zlib 1.3.2、zstd 1.5.7、nghttp2 1.70.0、BoringSSL wrapper commit、curl 8.23.0、SQLite 3.53.2、ZenAI、PCRE2 等；另有 `src/rust/Cargo.lock` 和 `flake.lock`。优点是多数 dependency source 有 hash/commit，缺点是浏览器本身是巨大 native attack surface，V8/HTML parser/network/crypto 任一层都需持续更新。

风险判断：

- GitHub Security Advisories API 返回 10 条历史 advisory（8 high、2 critical）；公开 vulnerable ranges 都是 `<0.4.1` 或更早，**未命中本次 1.0.2 asset**。这不等于 1.0.2 安全。
- 1.0.2 release notes包含 UAF 修复、CORS/cookie/CDP/Origin 行为变化，说明兼容性和安全边界仍快速演进。
- release API 未给资产 checksum/signature；本次自算 Linux x86_64 asset SHA-256 `ae7d01d261efb9e480e18ce3424533332883863bcf70b12a4321b5733f37e19e`，只作为本次下载 identity，不是上游签名。
- AGPL-3.0-only 与 shared hub 当前代码许可/分发策略需专业审查；本次只抽象机制，不复制源码。

#### 真实验证结果

1. 固定 HEAD GitHub Checks API：`30/30 success`，包括 `zig test`、debug V8 tests、MCP smoke、browser fetch、agent deterministic replay、release build；这是上游 CI 外部证据。
2. GitHub Contents API 的 `src/mcp/HttpServer.zig` 与本地固定 clone SHA-256 完全一致：`d60be906...ef33fc`。
3. 下载 release `lightpanda-x86_64-linux`：`76,408,136 bytes`；`lightpanda version` 返回 `1.0.2`。
4. `lightpanda fetch --dump html https://example.com`：exit `0`，输出 `1,990` bytes，含 `Example Domain` HTML，真实 fetch smoke **PASS**。
5. 启动 `lightpanda mcp --host 127.0.0.1 --port 19223`，实际完成 `initialize→s1`、`goto→200`、`DELETE→202`、再次用 `s1 goto→200`；**Issue #4350 在 1.0.2 release 本机复现**，预期终止后应 404。复现后已终止临时进程。
6. 未从源码构建：本机没有 Zig 0.17.0；不以 release binary smoke 替代源码全量测试。

#### 可复用经验

- **当多个 Agent 共享一个 browser service 时，应优先用不可混淆的 session identity + per-session serialized queue + 独立 cookie/storage/page，因为进程共享不应等于上下文共享；边界是同进程 session isolation 不是 OS sandbox。**
- **当 session 被 close/expire/revoke 时，应优先留下 tombstone/generation 并让旧 ID 稳定返回终态，因为只释放 worker 会让同一 ID 静默复活成新上下文；边界是 tombstone 需要 TTL、容量和显式 reuse policy。**
- **当 batch 中单页/单对象失败时，应优先保存每对象 terminal 并继续收集剩余 coverage，最后再给 batch 失败，因为 fail-fast 会丢失可用结果；边界是任何 partial output 都不能被投影为 complete。**

#### 可尝试实验（30 分钟）

在 `<shared-root>/runtime/hermes/github-hot-project-learning/poc/browser-session-contract/` 写一个**仅对本地 synthetic server**的协议 fixture，不接真实账户：

1. initialize 得到 session ID；
2. 两个 ID 各写 cookie，确认互不污染；
3. DELETE A 后重放 A，要求 404；
4. B 仍正常；
5. 输出 machine-readable `isolation_pass / termination_pass / cleanup_pass`。

当前 1.0.2 的第 3 项会失败，这正是 POC 的有效 counterexample；不应为了绿色而放宽验收。

#### 风险边界

- **License**：GitHub API 为 AGPL-3.0，`LICENSING.md` 写默认 AGPL-3.0-only；不复制源码到 shared core，不在未审合规前形成衍生集成。
- **安全风险**：浏览器处理不可信网页、JS、网络、cookie、下载与脚本；MCP `run` 可执行 PandaScript。必须隔离 filesystem、network、env、credential 与 process。
- **session correctness**：1.0.2 explicit DELETE 可复活旧 ID，已本机复现；多 Agent workflow 不能把 DELETE 视为可靠撤销证明。
- **网络入口**：Host/Origin/content-type gate 不是认证；服务只应默认 loopback，远程 bind 前需独立 auth/TLS/network policy。
- **维护活跃度**：2026-11-01 有 verified commit，1.0.2 发布于 10-23，活跃；同时 Web API/安全语义快速 churn。
- **telemetry/core dump**：README 写 telemetry 默认开启，可用 `LIGHTPANDA_DISABLE_TELEMETRY=true` 关闭；core dump 也需显式控制，生产 secret 场景必须审查。
- **不适用场景**：需要完整 Chrome extension ecosystem、强浏览器兼容保证、强多租户 OS isolation、许可证不兼容或不能接受快速行为变化的系统。

#### ⭐ Skill 升格判断

**判断：需二次验证；暂不沉淀项目专属 shared skill。**

可迁移的是 agent-neutral 的 browser session contract（isolation、termination tombstone、effect read-back、partial coverage），不是 Lightpanda 的 AGPL 实现。现有 shared skills 中没有 browser 专项，但在未建立至少两个 backend 的 differential fixture 前直接升格，会把单项目语义误当通用契约。

#### Hermes / shared hub 落地路径

1. 只在 `<shared-root>/runtime/hermes/github-hot-project-learning/poc/browser-session-contract/` 建 synthetic contract fixture；不自动注册 MCP，不修改 Hermes config。
2. contract schema 建议包含：`backend/version/artifact_hash/session_id/generation/operation/terminal/http_status/page_url/cookie_probe/cleanup_readback`。
3. 先对 Lightpanda 1.0.2 记录真实 counterexample，再选第二个 backend 做 differential；只有共同 invariant 稳定后，才评审是否新增 `capabilities/skills/browser/session-lifecycle-contract/`。
4. 若未来 Hermes 使用 browser MCP，应由 Hermes host adapter 强制 loopback/auth、每任务新 session、finally cleanup、DELETE 后 read-back；不能仅信 tool description。

## 经验沉淀

1. **当自动记忆或检索结果将进入 Agent prompt 时，应优先携带 source/layer/scope/revision/coverage 并明确低 authority，因为相关文本不等于真实指令；边界是最终副作用仍需 host-owned policy。**
2. **当 Agent 热路径的辅助系统需要 fail-soft 时，应优先同时保留 durable drop/error/drain evidence，因为“不阻塞”不能以静默丢失为代价；边界是 spool 本身必须限容、脱敏和可删除。**
3. **当多个 Agent 共享浏览器或其他有状态服务时，应优先为每个 scope 建独立 session/generation/queue，并对 close/expire 留 tombstone，因为资源释放不等于旧 identity 已失效。**
4. **当本机测试运行在当前 Agent 自身环境中时，应优先隔离 import path、HOME 和 runtime context，因为已安装 host module 会覆盖 fixture 并制造真假难辨的失败；边界是隔离测试还需真实宿主 integration lane。**
5. **当 release binary smoke、上游 CI、源码静态检查和本机全量测试覆盖不同层时，应优先并列报告各自状态，因为任一绿色都不能替代另一层；边界是公开 advisory 为空也不是安全证明。**
6. **当第三方实现 license 或供应链边界较重时，应优先抽象协议/不变量并用 clean-room fixture 验证，而不是复制源码或自动安装；边界是机制抽象也不能规避商标、专利或服务条款审查。**

## Hermes / shared hub 综合落地优先级

| 优先级 | 候选 | 当前动作 | 进入 shared 的条件 |
|---|---|---|---|
| P0 | browser session termination contract | runtime synthetic POC，保留 1.0.2 counterexample | 至少两个 backend differential + cleanup/read-back fixture |
| P0 | memory raw/derived authority labels | 对照现有 shared-memory-bridge 做设计评审 | synthetic recall POC + governance 去重 + 隐私 review |
| P1 | progressive recall 三层接口 | runtime synthetic index/timeline/detail 测量 | 明确 scope/coverage/token 指标，且不读取真实 secret |
| P1 | fail-soft capture receipt | 仅形成 candidate schema | drop/error/drain/replay 的 bounded durability 实测 |
| 禁止自动 | 安装 claude-mem / 注册 Lightpanda MCP | 不执行 | 必须用户明确授权、配置目标识别、隔离与合规审查 |

## 明日继续

1. 最小动作：在 runtime 写 `browser-session-contract` 的 backend-neutral schema 与 4 步 synthetic fixture，先把 1.0.2 的 `termination_pass=false` 固化为证据。
2. 在 disposable Python 环境复跑 claude-mem 的 `tests/hermes`，隔离当前 Hermes `agent.runtime_cwd`，判断 6 个失败是 host pollution 还是 adapter scope bug。
3. 不改当前 Hermes/OpenClaw 配置，不写 curated；POC 有两个 backend 的稳定证据后再提交 shared skill 评审稿。

## 候选反哺

### Candidate Facts

- [ ] topic: Agent memory 应区分 raw event、model-generated observation、retrieval projection 与 curated truth | evidence: claude-mem 固定提交的 capture/storage/injection 链 + shared hub 现有分层 | 建议: update | 安全级别: medium
- [ ] topic: session termination 必须留下 tombstone/generation，不能只释放 worker | evidence: Lightpanda 1.0.2 本机 `DELETE 202 → same ID POST 200` + Issue #4350 + `HttpServer.zig` | 建议: create | 安全级别: low
- [ ] topic: fail-soft capture 需要 dropped/error/drain receipt | evidence: `ClaudeMemClient._enqueue` queue full 静默 drop，sender 吞异常 | 建议: create | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: browser-session-lifecycle-contract | 可复用场景: Hermes/future agent 的 browser MCP、多 Agent browser pool | 是否建议 shared: no（当前） | 原因: 仅一个 backend 有本机 counterexample，需第二 backend differential 后评审
- [ ] 名称: shared-memory-bridge progressive recall iteration | 可复用场景: shared inbox/runtime/curated 的按需检索 | 是否建议 shared: yes（候选更新现有 skill，不新建） | 原因: 与现有分层高度重叠，应先 POC 和去重
- [ ] 名称: host-adapter isolation test lane | 可复用场景: 第三方 adapter 在当前 Hermes 环境中的 contract test | 是否建议 shared: no（当前） | 原因: 先在 runtime 证明 fake HOME/import isolation 方法稳定

### Candidate Open Questions

- [ ] 问题: claude-mem 的 6 个 Hermes test 失败在完全隔离环境是否消失？ | reason: adaptation | priority: high
- [ ] 问题: Lightpanda 修复 #4350 后，DELETE、idle reap、explicit `session_close` 是否共享同一 terminal/tombstone 语义？ | reason: gap | priority: high
- [ ] 问题: progressive recall 在中文/CJK shared corpus 上的 token saving、召回率与 source leakage 如何？ | reason: gap | priority: medium
- [ ] 问题: Lightpanda HTTP MCP 除 Host/Origin 外是否有可配置 application auth，或必须由外部 proxy 提供？ | reason: gap | priority: high

### 不应自动落地

- 不自动安装 claude-mem、Lightpanda 或其 skills/plugins/MCP。
- 不自动修改 Hermes/OpenClaw 配置、provider、模型、cron、env 或 secret。
- 不把模型生成的 observation 直接写 `curated/memory`；只保留 candidate。
- 不复制 AGPL-3.0-only 的 Lightpanda 源码到 shared core。
- 不把 release smoke、上游 Checks 或空 advisory 列表写成“完整测试通过/无漏洞”。
- 不读取或外发真实用户 prompt、shared inbox 正文、credential 或生产浏览器 cookie 做 POC。
