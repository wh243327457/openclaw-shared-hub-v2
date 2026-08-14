# 2026-08-10 GitHub 热门项目学习日报

> 执行器：Hermes（当前 OpenClaw runtime 不存在；本任务未调用、启动或模拟 OpenClaw）。  
> GitHub Repository API 元数据查询时间：`2026-08-10T12:22:46+08:00`；动态 Stars/更新时间以该次真实响应为准。  
> 发现来源：真实抓取 [`github.com/trending?since=daily`](https://github.com/trending?since=daily)，并用 GitHub Search API 补充 2026-08-01 后新仓；逐仓使用 Repository API 核验。  
> 固定源码快照：`PrimeIntellect-ai/prime-agent@a18809e00ea30638584d87b3afea7285a9d7296c`；`disler/super-simple-software-factory@de31374882e7a4e3e5b7bb9bd09e69dc2f779356`。  
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-10/`；clone：`runtime/hermes/github-hot-project-learning/repos/2026-08-10/`。  
> 数据边界：GitHub issue 是报告者陈述；只有本报告明确列出的本机测试/fixture 才算独立复现。README、release 和 CI 状态不是本机验证。

## 今日结论

今天的主线是：**把控制面从 prompt 移到确定性代码，只是可靠 Agent 的起点；控制面的“看见了什么、验证了什么、允许改什么、何时算完成”也必须有可核验覆盖率。** `prime-agent` 已把 long-running session、goal、autonomous gate、local/global continual harness 和 baseline-aware refinement 做成宿主机制，但固定源码仍存在“system prompt 只显示每类前 6 条、kernel 默认读取 child-local 空 store”的可见性断层，且 goal completion 与 skill availability 可能失配；SSSF 把 phase、typed envelope、gate、write allowlist 和 trace 都放入 Python，却被本机 fixture 证明 `diff_matches_claims()` 根本不读 diff，而且 permission snapshot 只存 numstat，在预先 dirty 文件前后增删行数相同的情况下看不见内容被替换。对 Hermes/shared hub 最值得迁移的窄原则是：**任何确定性控制面都要同时披露 input identity、context visibility/coverage、实际 effect set、gate evidence 与 terminal acceptance；“代码拥有循环”不等于“代码已经验证了真实世界”。**

## 证据与执行摘要

- 先运行 `scripts/resolve_shared_root.py`，解析到 `/home/vany/agent/shared`，并依次读取 `manifest.yaml`、`AGENTS.md`、`curated/memory/MEMORY.md`；本日原始研究只写 Hermes inbox/runtime，没有直接写 curated。
- Trending HTML 真实保存为 `runtime/hermes/github-hot-project-learning/evidence/2026-08-10/trending.html`，大小 **589,826 bytes**，解析到 12 个 daily trending 仓库；8 个候选的 Repository API 原始响应写入 `project-overview-api.json`。
- 两个深读仓均执行 `git clone --depth 1` 并固定 HEAD；repo、commit、release、issues 的 API JSON保存在 evidence 目录。
- `prime-agent`：`npm ci --ignore-scripts` 安装 **353 packages**；定向执行 refinement、goal、autonomous 三个 test files，真实结果 **124 passed / 0 failed**。`npm audit --omit=dev` 返回 exit 1，汇总为 **3 high + 2 moderate** vulnerability nodes；没有调用 provider、模型、IPython Agent、daemon 或外部 skill。
- SSSF：fresh throwaway repo 中 `install.py` 首次 stamp **44** 项，第二次 **0** 项（43 template files 被跳过），`compileall` 通过；离线 `adw_quality.py` 确实返回 exit 0，但四个 quality command 全是明确的 `PLACEHOLDER ... echo`，所以只证明 trace/phase/exit 通路，不证明任何项目质量。
- SSSF 独立 fixture 证明：`diff_matches_claims()` 对从未修改的已存在文件返回 passed；read-only Agent 新建 untracked 文件会被 `PermissionBreach` 检出并删除；但预先 dirty tracked file 在 Agent 修改前后 numstat 同为 `1,1` 时 `changed_paths=[]`，内容已改变而 enforcement 无信号。
- 两仓 Dependabot alerts API 均为 403（Prime 未授权；SSSF alerts disabled），公开 repository security advisories API 均返回空数组；这不能替代本机 lockfile audit，也不能证明无未知漏洞。
- 未修改 Hermes/OpenClaw 配置、模型、provider、auth、env、cron 或 secret；未安装上游产品到 Hermes；未复制上游 skill/源码到 shared capabilities。

## 项目速览

下表 Stars/Forks/Language/License/Updated/Pushed 均来自 `2026-08-10T12:22:46+08:00` 附近的 GitHub Repository API。`NOASSERTION` 表示 API 未识别仓库级 License，不等于已确认无 License。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | **11,614** | **1,185** | TypeScript | **MIT** | 2026-08-10T04:19:54 / 2026-08-10T04:14:58 | **深读：RLM long-running control plane、autonomous gate、continual harness 可见性断层** |
| [vitali87/code-graph-rag](https://github.com/vitali87/code-graph-rag) | 3,136 | 527 | Python | MIT | 2026-08-10T04:19:41 / 2026-08-10T00:59:12 | 结构化代码检索；与 08-07 graph-context 主线相邻，避免重复深读 |
| [google-deepmind/weathernext](https://github.com/google-deepmind/weathernext) | 7,135 | 941 | Python | Apache-2.0 | 2026-08-10T04:20:34 / 2026-08-07T10:10:42 | 天气模型研究；价值高但与今日 Agent 控制面主线较远 |
| [google/skills](https://github.com/google/skills) | 17,326 | 1,398 | Python | Apache-2.0 | 2026-08-10T04:20:11 / 2026-08-07T22:50:54 | 第三方 skills 集；不能把热度当执行授权，不批量安装 |
| [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | 17,730 | 4,019 | TypeScript | MIT | 2026-08-10T04:19:39 / 2026-08-10T04:12:30 | 近期已研究 scoped authority，不重复追热 |
| [disler/super-simple-software-factory](https://github.com/disler/super-simple-software-factory) | **546** | **128** | Python | **MIT** | 2026-08-10T03:38:12 / 2026-08-04T13:43:58 | **深读：deterministic phases、typed envelopes、gate/permission 真实性缺口** |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 12,819 | 639 | Rust | MIT | 2026-08-10T04:21:39 / 2026-08-07T09:20:18 | 文档解析输入面大；供应链与 parser 安全留待专项 |
| [Accio-org/RealReplicaBench](https://github.com/Accio-org/RealReplicaBench) | 1,042 | 80 | HTML | Apache-2.0 | 2026-08-10T04:13:25 / 2026-08-10T04:13:21 | 长时 Agent benchmark 候选；新仓，先观察可复现性 |

Stars 只用于发现，不是成熟度、安全、正确性或许可证兼容证明。今天实际深读 `PrimeIntellect-ai/prime-agent` 与 `disler/super-simple-software-factory`；其余项目只做 API/README 层筛选。

## 深读项目

### 1. PrimeIntellect-ai/prime-agent

- **URL**：https://github.com/PrimeIntellect-ai/prime-agent
- **Stars / Forks / Language / License（GitHub API）**：**11,614 / 1,185 / TypeScript / MIT**。
- **updated / pushed**：2026-08-10T04:19:54Z / 2026-08-10T04:14:58Z。
- **API open_issues_count**：456（GitHub 该字段含 open PR，不等于纯 issue 数）。
- **固定 default-branch commit**：[`a18809e00ea3`](https://github.com/PrimeIntellect-ai/prime-agent/commit/a18809e00ea30638584d87b3afea7285a9d7296c)，author/committer 2026-08-07T23:23:00Z，message `add privacy-safe agent analytics (#521)`；`git ls-remote origin refs/heads/main` 与 Repository commit API 都返回同一 SHA。
- **最新稳定 Release**：[`v0.7.1`](https://github.com/PrimeIntellect-ai/prime-agent/releases/tag/v0.7.1)，published 2026-08-07T18:39:08Z，target `95afd319…`；固定 main 与 release target 不同，不能把 main 的全部行为外推到 v0.7.1 artifact。

#### 一句话判断

值得学的不是“持久 Python REPL”本身，而是它把 **client detach → daemon supervisor → resident worker → AgentSession → IPython/RLM children → goal/autonomous policy → local/global harness → transcript/artifacts** 做成宿主拥有的长时控制面；更值得警惕的是，控制面已经很丰富仍会因 **goal skill 不可用、harness overflow 无可达检索、child-local 默认空视图、daemon drain 卡住、release bundle 漏文件** 产生“状态存在但执行者看不见/用不了”的断层。

#### 解决的问题：替代了什么旧做法

1. 替代把所有工具平铺成 model tool：模型默认在持久 IPython 中把文件、shell、skill、child agent 当程序接口组合；provider/session/credential authority 留在 TypeScript host。
2. 替代终端进程即任务所有者：supervisor/worker 保有 session、kernel、children、schedule 与 queue；UI detach 不等于停止。
3. 替代“模型说继续就无限继续”：autonomous mode 由宿主计算 continuation/turn/token/time budget，并先执行 quality gate。
4. 替代“同一个目标每轮靠对话记住”：goal 作为持久状态，区分 active/paused/budget_limited/complete/error，并要求显式 `goal.complete()`。
5. 替代一次性 prompt tweak：continual harness 把 prompt/memory/skill/subagent 拆成 local/global entries，refinement proposal 有 baseline conflict check、history 与 rollback信息。
6. 替代 child call 阻塞等待：`rlm(...)` 只返回 admission handle，结果走 agent message/files，child registry可跨 compaction/restore。

边界：进程隔离用于 lifecycle/failure containment，不是安全 sandbox；IPython、skills 和项目命令仍以用户 OS 权限执行。宿主 gate只证明命令退出状态，不能证明命令与用户真实 acceptance 完全一致。

#### 架构 / 实现与数据流

```text
TUI / print / JSON / RPC client
              │ versioned local protocol
              ▼
daemon supervisor ── catalog / routing / attach / recovery / messages
              │
              ▼
session worker (one root session tree)
  ├─ AgentSessionRuntime + prompt queue
  ├─ root AgentSession ── model provider
  ├─ scheduler / heartbeat / cron prompt
  ├─ persistent goal + autonomous continuation policy
  ├─ persistent IPython kernel ── Python skills / host_request
  └─ RLM child sessions + optional child kernels
              │
              ├─ session JSONL / artifacts / local harness
              └─ global harness + refinement history
```

核心不对称是正确的：模型负责程序化决策，TypeScript host 负责 provider、session、goal、schedule、message 和持久化 authority。但“host-owned”不自动等于“完整”：harness prompt投影是有界 projection，kernel直接读取又默认 local；goal context要求模型调用 skill，`--no-skills` 却可能移除该调用面；这些组合约束必须在构造时验证。

#### Repo tree 摘要

```text
prime-agent/
├── packages/
│   ├── coding-agent/
│   │   ├── src/core/                    # AgentSession、autonomous、goal、refinement、kernel
│   │   ├── src/modes/daemon/            # supervisor/worker/protocol/recovery/ownership
│   │   ├── src/modes/{rpc,acp,...}/     # headless/client adapters
│   │   ├── docs/                        # architecture、RLM、long-running、skills
│   │   ├── skills/                      # bundled Agent/Python skills
│   │   └── test/                        # unit + faux-provider integration/regression
│   ├── agent/ / ai/ / tui/              # model loop、provider abstraction、terminal UI
│   └── examples/                        # extension/provider/sandbox examples
├── prime-agent-runtime/src/rlm/         # kernel-side Python bridge、harness、skills
├── scripts/                             # release、binary、installer、bench/profile
├── package.json / package-lock.json     # npm workspace + lock
├── AGENTS.md                            # development/protocol/dependency rules
└── README.md / LICENSE                  # product/trust boundary + MIT
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/coding-agent/src/core/autonomous.ts` | bounded autonomous policy | limits、quality commands、worktree snapshot、failure continuation、process timeout/tree kill |
| `packages/coding-agent/src/core/goals.ts` | durable objective | goal状态、budget accounting、continuation/budget prompt、显式 completion语义 |
| `packages/coding-agent/src/core/refinement/refinement.ts` | continual harness refinement | local/global merge、bounded prompt projection、proposal validation、baseline conflict、atomic rename |
| `prime-agent-runtime/src/rlm/harness.py` | kernel harness API | local/global store解析、CRUD、mtime sync、overview、skill reference contract |
| `packages/coding-agent/docs/architecture.md` | process truth map | client/supervisor/worker/session/kernel/storage边界 |
| `packages/coding-agent/docs/long-running-agents.md` | lifecycle contract | detach、messages、heartbeat/schedule、goal、autonomous、compaction |
| `packages/coding-agent/test/refinement.test.ts` | refinement fixtures | merge、projection、proposal、rollback等定向验证 |
| `package.json` / `package-lock.json` | dependency truth | npm workspaces、353-package install、生产 audit 的 advisory来源 |

#### 源码精读（固定 commit）

**代码块 1：Autonomous 是否继续由宿主 gate 和 limits 决定**  
来源：[`packages/coding-agent/src/core/autonomous.ts#L227-L251`](https://github.com/PrimeIntellect-ai/prime-agent/blob/a18809e00ea30638584d87b3afea7285a9d7296c/packages/coding-agent/src/core/autonomous.ts#L227-L251)

```ts
export async function shouldAutonomouslyContinue(
  state: AutonomousRuntimeState,
  message: AssistantMessage,
  options: AutonomousOperationOptions = {},
  now = Date.now(),
): Promise<AutonomousDecision> {
  if (!state.enabled || message.stopReason === "error" || message.stopReason === "aborted")
    return { shouldContinue: false, reason: "not_needed" };
  const gateResult = await refreshAutonomousQualityGates(state, options);
  if (gateResult) {
    if (gateResult === "passed") return { shouldContinue: false, reason: "not_needed" };
    if (gateResult === "retry_exhausted" || autonomousLimitReason(state, now))
      return { shouldContinue: false, reason: "limit_reached" };
    return { shouldContinue: true, reason: "gate_failed" };
  }
  if (autonomousLimitReason(state, now))
    return { shouldContinue: false, reason: "limit_reached" };
  return { shouldContinue: true, reason: "missing_terminal_evidence" };
}
```

逻辑：assistant正常停下不是 terminal evidence；有 gate 时先运行 gate，失败且尚有 budget才继续，无 gate则继续到 host limit。边界是“gate passed”只证明配置命令 exit 0；如果 gate 是 placeholder、范围不完整或未绑定 immutable input，宿主仍会过早结束。

**代码块 2：失败 gate 在工作树未改变时不盲目重跑**  
来源：[`packages/coding-agent/src/core/autonomous.ts#L293-L343`](https://github.com/PrimeIntellect-ai/prime-agent/blob/a18809e00ea30638584d87b3afea7285a9d7296c/packages/coding-agent/src/core/autonomous.ts#L293-L343)

```ts
for (const command of state.gates.commands) {
  const currentSnapshot = await captureGitWorktreeSnapshot(cwd, signal);
  if (
    state.lastGateFailure?.command === command &&
    state.lastGateFailureSnapshot &&
    gitWorktreeSnapshotsEqual(currentSnapshot, state.lastGateFailureSnapshot)
  ) {
    const attempt = (state.gateAttempts[command] ?? state.lastGateFailure.attempt) + 1;
    state.gateAttempts[command] = attempt;
    state.lastGateFailure = {
      ...state.lastGateFailure,
      attempt,
      exitText: "not rerun: workspace unchanged since previous failed gate",
      output: "The autonomous gate was not rerun because the workspace has not changed...",
    };
    return attempt > state.gates.maxRetries ? "retry_exhausted" : "failed";
  }
  const result = await runChildProcess(command, [], { cwd, shell: true, ... });
  const postRunSnapshot = await captureGitWorktreeSnapshot(cwd, signal);
  if (result.status === 0 && !result.error && !result.timedOut) continue;
  // bounded failure evidence + post-failure snapshot
}
```

逻辑：失败后若 source/test/blocker artifact无变化，不再浪费一次相同命令；tracked diff与untracked file content hash都进入 snapshot。本机对应 tests覆盖“unchanged不重跑”和“untracked内容变化后重跑”。边界是 pathspec显式排除若干目录，且 snapshot变化仍不证明修复相关；gate command本身也可能产生副作用。

**代码块 3：Harness prompt projection默认每类只显示 6 条，并按 path/title/id 字典序取头部**  
来源：[`packages/coding-agent/src/core/refinement/refinement.ts#L429-L501`](https://github.com/PrimeIntellect-ai/prime-agent/blob/a18809e00ea30638584d87b3afea7285a9d7296c/packages/coding-agent/src/core/refinement/refinement.ts#L429-L501)

```ts
export function formatHarnessStateForPrompt(state: HarnessState, options = {}): string {
  const maxEntriesPerKind = options.maxEntriesPerKind ?? DEFAULT_OVERVIEW_ENTRY_LIMIT; // 6
  const maxContentLength = options.maxContentLength ?? DEFAULT_OVERVIEW_CONTENT_LIMIT; // 180
  // ...
  for (const kind of Object.keys(state.entries) as RefinementKind[]) {
    const entries = Object.values(state.entries[kind]).sort((a, b) =>
      [a.path, a.title, a.id].join("\0").localeCompare([b.path, b.title, b.id].join("\0")),
    );
    for (const entry of entries.slice(0, maxEntriesPerKind)) {
      // compact summary projection
    }
    const overflow = entries.length - Math.min(entries.length, maxEntriesPerKind);
    if (overflow > 0) lines.push(`- +${overflow} more ${kind} entries`);
  }
}
```

逻辑：projection明确显示overflow，不是静默丢失；但selection不看更新时间、版本或相关性。open issue [#819](https://github.com/PrimeIntellect-ai/prime-agent/issues/819)进一步指出：child kernel 的 `rlm.harness` 默认解析 session-local store，新 child可显示 `memory: 0`，即使system prompt来自global+local merged state；`global_=True`可读，但默认输出未提示。本报告读取的 `harness.py` 也确认 `_state_file(..., global_=False)`优先 child local dir。issue有完整fixture，但本机未运行其40-entry child环境，故“实际child矛盾视图”仍标 **上游复现声明 + 固定源码一致，独立E2E待核验**。

**代码块 4：Refinement apply 用 baseline 拒绝规划期间被并发改动的 entry**  
来源：[`packages/coding-agent/src/core/refinement/refinement.ts#L707-L779`](https://github.com/PrimeIntellect-ai/prime-agent/blob/a18809e00ea30638584d87b3afea7285a9d7296c/packages/coding-agent/src/core/refinement/refinement.ts#L707-L779)

```ts
export function applyRefinementProposal(state, proposal, options): RefinementResult {
  const appliedEdits: AppliedRefinementEdit[] = [];
  const proposalModifiedKeys = new Set<string>();
  for (const edit of proposal.edits) {
    const id = edit.id ?? (edit.action === "create" ? slug(edit.title ?? edit.kind, edit.kind) : "");
    const records = state.entries[edit.kind];
    const before = cloneEntry(records[id]);
    const entryKey = `${edit.kind}:${id}`;
    const baseline = cloneEntry(options.baselineState?.entries[edit.kind][id]);
    if (options.baselineState && !proposalModifiedKeys.has(entryKey) &&
        JSON.stringify(before) !== JSON.stringify(baseline)) {
      appliedEdits.push({ ...edit, id, before, applied: false,
                          error: "entry changed during refinement planning" });
      continue;
    }
    // validate create/update/delete, preserve before/after, bump version
    records[id] = after;
    appliedEdits.push({ ...edit, id, before, after: cloneEntry(after), applied: true });
  }
}
```

逻辑：LLM proposal生成期间若目标 entry变化，不以旧观察覆盖新状态；create/update/delete也分别验证存在性。边界是最终 `saveHarnessState()`使用temp+rename，但源码未显示跨进程文件锁或directory fsync；baseline check与save之间的跨进程race是否可导致last-writer-wins **待核验**，不能从单进程test外推为事务数据库。

#### 依赖分析与供应链风险

- 根 package `prime-agent@0.7.1`，Node engine `>=22.8.0`，npm workspace包含 `ai/agent/coding-agent/tui` 与extension examples；kernel runtime另有 `ipykernel`、`nest-asyncio`、`tyro` 三个未锁版本的Python依赖声明。
- coding-agent runtime核心依赖包括 ACP SDK、内部 agent/ai/tui包、ZeroMQ、Undici、YAML、TypeBox、proper-lockfile、glob/minimatch、file/archive处理；这说明真实攻击面不只模型API，还包括本地IPC、extension、archive与HTTP。
- `npm ci --ignore-scripts --no-audit --no-fund`真实安装353 packages；跳过 lifecycle scripts是为只读研究降权，因此未验证postinstall、bundle、binary或installer。
- `npm audit --omit=dev`真实返回：metadata汇总 **3 high + 2 moderate**，vulnerability nodes为：
  - direct `undici 7.28.0`：high node，包含cache parsing/info disclosure、retry desync、CRLF/cookie相关GHSA，audit建议升级到`>=7.29.0`；
  - transitive `brace-expansion`：high DoS；
  - transitive `ip-address`：high node，含特殊地址误分类/SSRF boundary问题；
  - transitive `protobufjs`：moderate `.proto` option parse DoS；
  - direct workspace link `@earendil-works/pi-coding-agent`：moderate `GHSA-mqxh-6gq7-558m`（project-local extension未经批准加载），audit显示无自动fix。当前固定源码/配置是否仍满足advisory全部前提需专项核验，但不能忽略。
- Dependabot 403；公开repo advisories为空。两项都不能抵消本机audit，也不覆盖Python、release archive、native ZeroMQ/clipboard、provider SDK或用户安装skills。

#### README / docs / release / issues / source 交叉核验

- README的RLM、continual harness、background daemon、goal、autonomous、skills主线与`docs/architecture.md`、`docs/rlm.md`、`docs/long-running-agents.md`及上述源码对应。
- v0.7.1 release只列websearch配置引导与`retry_worker` recovery修复；固定 main SHA不同，因此今日tests验证的是main，不是稳定release asset。
- open issue [#819](https://github.com/PrimeIntellect-ai/prime-agent/issues/819) 的“6-entry alphabetical head + child local空store”与固定源码一致；child完整复现待核验。
- open issue [#1111](https://github.com/PrimeIntellect-ai/prime-agent/issues/1111) 报 `--goal --no-skills`移除必需goal skill后，目标完成仍可能继续autonomous。`goals.ts`确实要求模型调用`goal.complete()`；本机未启动daemon/provider复现组合CLI，故是上游复现声明。
- open issue [#1072](https://github.com/PrimeIntellect-ai/prime-agent/issues/1072) 报v0.7.1 daemon idle-eviction mutation drain timeout、closing/executing卡住；本机未运行长驻daemon soak。
- open issue [#751](https://github.com/PrimeIntellect-ai/prime-agent/issues/751) 针对v0.7.0 release tarball漏`amazon-bedrock.js`；不能外推v0.7.1或main仍受影响，release artifact验证待核验。
- GitHub Actions最近记录包含success、failure、action_required与in-progress PR runs；只说明仓库活跃，不能把某次PR CI当固定main全绿证明。

#### 真实测试结果

```text
$ npm ci --ignore-scripts --no-audit --no-fund
added 353 packages

$ cd packages/coding-agent
$ npx tsx ../../node_modules/vitest/dist/cli.js --run \
    test/refinement.test.ts \
    test/suite/agent-session-autonomous.test.ts \
    test/suite/agent-session-goal.test.ts
Test Files  3 passed (3)
Tests       124 passed (124)
Duration    13.38s

$ npm audit --omit=dev --json
# exit 1
3 high + 2 moderate vulnerability nodes
```

准确结论：固定main的refinement、goal、autonomous定向fixtures通过；未运行完整test suite、daemon process tests、real provider、RLM child、IPython kernel、installer、binary/release artifact、Windows/macOS、long-running soak、network或external skill。

#### 可复用经验

- 当目标完成依赖某个skill/tool调用时，应优先在构造时验证“目标协议所需能力 ⊆ 实际加载能力”，因为prompt要求`goal.complete()`不能弥补`--no-skills`移除调用面；边界是能力存在也不证明模型会正确调用。
- 当长期记忆投影有条数/字符预算时，应优先同时提供selection policy、coverage/overflow和可达的detail retrieval路径，因为“+N more”若指向默认空store仍是不可用证据；边界是扩大prompt会增加cache/context成本。
- 当自动循环由质量命令终止时，应优先绑定immutable input/worktree evidence并保存命令、attempt、output和snapshot，因为exit 0只证明该命令；边界是命令覆盖率必须另审。
- 当Agent自我修改harness时，应优先保留before/after、baseline revision和rollback，并在最终save重验，因为planning-time evidence会过期；边界是文件rename不等于跨进程事务。

#### 30 分钟最小实验

在`runtime/hermes/github-learning-poc/harness-visibility-contract/`做纯离线fixture：

1. 构造global 20 entries、parent-local 3 entries、child-local 0 entries，固定`updated_at/version/path`。
2. 输出`visible_in_system_prompt`、`visible_via_default_kernel`、`visible_via_explicit_global`、`overflow_count`和`retrieval_hint`。
3. validator要求：任何prompt overflow都必须有Agent实际可调用的detail path；goal protocol所需skill缺失时启动前blocked；不得把空child-local解释为全局无记忆。
4. 不安装/启动Prime Agent，不连接provider，不改Hermes config，不读取真实用户harness。

#### 风险边界

- **License**：GitHub API、root LICENSE和package manifest为MIT；dependencies、models/providers、用户skills、release binaries、Python packages分别审查。
- **维护活跃度**：main/repo在查询时数小时内有活动，v0.7.1三天内发布，issue/PR很活跃；但456个API open items、快速release与daemon/harness回归意味着协议churn大。
- **安全风险**：README明确model-generated Python/commands使用用户权限且不是sandbox；npm audit实报3 high+2 moderate；extensions/skills、project code、archive、HTTP与ZeroMQ扩大输入/执行面。
- **一致性风险**：local/global harness可见性、goal skill依赖、daemon mutation drain和release artifact与source可能错位；process/session存在不等于任务authority或completion完整。
- **准确性局限**：quality gate命令由operator定义；模型/child结果仍可能错误；124个定向tests不覆盖全runtime。
- **供应链风险**：npm + Python + native/binary + provider多生态；Dependabot不可见；stable release和fixed main不是同一commit。
- **不适用场景**：把它当恶意repo sandbox、hostile多租户服务、无需gate的无限自治、仅凭harness summary认定全部memory已读。
- **不可自动执行**：不安装Prime Agent、不运行curl installer、不登录provider、不加载第三方skill、不启动daemon/schedule、不改Hermes/OpenClaw配置、provider或cron。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`harness-visibility-contract`（投影coverage + overflow + resolvable retrieval）与“protocol-required capability preflight”。
- **需验证**：用synthetic global/parent-local/child-local fixtures复现#819可见性断层；与shared-memory-bridge、verification-first、completion/terminal evidence候选去重。
- **暂不沉淀**：Prime Agent产品、RLM kernel、daemon、provider、auto-refine实现、bundled skills和安装器；Hermes已有自己的runtime/skills/memory边界。
- **今日动作**：只写runtime project card/lessons/candidate，不创建shared skill，不写curated active fact。

#### Hermes / shared hub 落地路径

1. runtime POC：`runtime/hermes/github-learning-poc/harness-visibility-contract/{model.py,fixtures/,validate.py,test_contract.py,README.md}`。
2. Hermes学习审计proposal：未来给`runtime/hermes/github-hot-project-learning/status.json`增加`input_revision/report_sha256/evidence_coverage`，并在orchestrator完成前真实计算；本日不改脚本。
3. shared memory读取proposal：在已有`capabilities/skills/foundation/shared-memory-bridge/`验证“summary overflow → canonical path可读取”，不新建重叠memory skill。
4. 分层：fixture与原始stdout留`runtime/hermes/`；本日报告留`inbox/hermes/daily/`；只有经多Agent验证、去重、治理审查的窄事实才考虑`curated/memory/facts/`。
5. OpenClaw runtime不存在；不创建或调用OpenClaw adapter，只保持fixture agent-neutral、future-agent-readable。

---

### 2. disler/super-simple-software-factory

- **URL**：https://github.com/disler/super-simple-software-factory
- **Stars / Forks / Language / License（GitHub API）**：**546 / 128 / Python / MIT**。
- **updated / pushed**：2026-08-10T03:38:12Z / 2026-08-04T13:43:58Z。
- **API open_issues_count**：10（含open PR）。
- **固定 commit**：[`de31374882e7`](https://github.com/disler/super-simple-software-factory/commit/de31374882e7a4e3e5b7bb9bd09e69dc2f779356)，author/committer 2026-08-02T17:57:38Z，message `🚀`；`git ls-remote`与Commit API返回同一SHA。
- **Release**：GitHub Releases API 返回空数组，**无可核验release/tag artifact**；只能研究固定main snapshot。

#### 一句话判断

值得学的是它把 **deterministic phase graph、typed envelope、same-session correction、code quality phase、post-hoc write allowlist、SQLite trace、single finish acceptance** 收敛成一个可stamp的skill；更值得学习的是反例：名称叫`diff_matches_claims`的gate只验文件存在，placeholder quality会完整绿灯，numstat permission fingerprint对预dirty同增删行数变化无感——说明**确定性代码必须验证真实predicate，而不是仅把LLM声明换成函数名**。

#### 解决的问题：替代了什么旧做法

1. 替代把整个SDLC塞给一个Agent：Python ADW拥有phase顺序、retry、acceptance，Agent只在named phase中工作。
2. 替代自然语言handoff：每次Agent final response解析为Pydantic `EnvelopeBase`子类，JSON parse/gate失败继续同一session而非冷启动。
3. 替代让Agent浪费token运行已知命令：test/lint/typecheck/build作为`kind="code"`的确定性phase，失败通过envelope回给builder。
4. 替代“reviewer说自己只读”：`tools`只算capability申请，`writes`和`protected_files`在call后比较Git working tree并尝试rollback。
5. 替代transcript小说式审计：phase/event/envelope/gate/process写SQLite WAL和raw files，UI/CLI从同一DB读取。
6. 替代“所有phase没抛异常就是成功”：`run.finish(accepted=...)`联合phase status与业务acceptance，统一DB/banner/exit code。

边界：post-hoc enforcement不是sandbox，越权写已经发生；rollback无法恢复Agent删掉的预先未提交内容。当前版本还直接在当前branch运行，无branch-per-run、sandbox、merge或human approval phase。

#### 架构 / 实现与数据流

```text
engineer request
      │
      ▼
ADW Python script (deterministic graph owner)
  ├─ run.phase(engineer|agent|code)
  ├─ agent identity from sssf.config.yaml
  ├─ known commands in quality.py
  └─ run.finish(phases_ok && accepted)
      │
      ├─ agent phase → Pi session
      │    ├─ typed final JSON → Pydantic envelope
      │    ├─ gate(envelope, run) → GateReport
      │    ├─ violation → same-session correction
      │    └─ permission snapshot/enforce/rollback
      │
      ├─ code phase → tests/lint/build/git
      └─ trace → raw_output/envelope/files + SQLite WAL
```

三类truth必须分开：Agent envelope是claim；gate report是某个predicate的evidence；Git/tree/test/runtime才是world state。SSSF的设计语言明确知道这一区别，但固定实现的`diff_matches_claims` predicate与名称不一致，permission fingerprint又不是content identity，因此“green deterministic gate”仍可能是假绿。

#### Repo tree 摘要

```text
super-simple-software-factory/
├── .claude/skills/sssf/
│   ├── SKILL.md                         # hard rules + lazy cookbook routing
│   ├── cookbooks/                       # install/create/update/run playbooks
│   ├── references/                      # config/handoff/observability specs
│   ├── scripts/
│   │   ├── install.py                   # idempotent template stamping
│   │   ├── make_adw.py / make_config.py # generators
│   ├── templates/
│   │   ├── adws/adw_*.py                # 12 thin starter workflows
│   │   ├── adws/adw_modules/             # runner、agents、gates、permissions、trace
│   │   ├── prompt_engineering/           # per-agent system/user prompt
│   │   ├── harness_engineering/          # Pi extension examples
│   │   ├── sssf.config.yaml / justfile   # roster、permissions、entrypoints
│   │   └── env.sample                    # provider variable placeholders
│   └── apps/visualizer/                  # optional Bun/Vue/Vite read-only UI
├── images/                               # architecture illustrations
├── README.md
└── LICENSE                               # MIT
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `templates/adws/adw_modules/runner.py` | single phase/terminal primitive | phase fail-by-default、exception finalization、`finish(accepted)`统一终态 |
| `templates/adws/adw_modules/agents.py` | Agent call orchestration | prompt render、same-session JSON/gate retry、permission enforcement、envelope/trace |
| `templates/adws/adw_modules/gates.py` | mechanical validation | artifact/file/JSON/verdict/test checks；`diff_matches_claims`当前只验existence |
| `templates/adws/adw_modules/permissions.py` | post-hoc write boundary | Git numstat/untracked fingerprint、allowlist/protected path、rollback |
| `templates/adws/adw_modules/data_types.py` | typed contract | phase/envelope/gate/quality/change/config/event/Pi result models |
| `templates/adws/adw_modules/quality.py` | deterministic command lane | command evidence与结果adapter；starter命令是placeholder |
| `templates/adws/adw_modules/tracer.py` | observability truth | SQLite WAL sessions/phases/events/envelopes/gates/processes |
| `scripts/install.py` | skill stamping | skip-existing idempotency、`--force`覆盖、gitignore写入 |

#### 源码精读（固定 commit）

**代码块 1：Phase clean exit与业务acceptance是两个问题**  
来源：[`runner.py#L73-L142`](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/templates/adws/adw_modules/runner.py#L73-L142)

```python
@contextmanager
def phase(self, params: PhaseParams):
    phase = Phase(..., status="running", started_at=now_iso())
    try:
        yield PhaseHandle(self, phase)
    except BaseException as error:
        phase.status = "fail"
        self.tracer.session_finish(self.adw_id, ok=False)
        raise
    else:
        phase.status = "success"
        self.tracer.phase_upsert(phase)

def finish(self, accepted: bool = True, reason: str = "") -> int:
    phases_ok = bool(self.phases) and all(p.status == "success" for p in self.phases)
    ok = phases_ok and accepted
    self.tracer.session_finish(self.adw_id, ok=ok)
    self.console.session_finished(ok, self.tokens, self.cost, self.cfg.observability.db)
    return 0 if ok else 1
```

逻辑：test phase可成功执行一个红suite，因此phase成功不等于run accepted；一个`finish()`同时决定DB、banner和exit。边界是caller若把错误predicate传给`accepted`，一致地记录错误仍是错误；terminal consistency不等于semantic correctness。

**代码块 2：Gate失败回到同一Agent session，permission在接受envelope前检查**  
来源：[`agents.py#L139-L192`](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/templates/adws/adw_modules/agents.py#L139-L192)

```python
tree_before = permissions.snapshot(run)
result = send(user_text)
envelope, attempt = _parse_with_retries(run, phase, call, result, send)

for gate_attempt in range(1, max(1, phase.params.retries + 1) + 1):
    violations = []
    for gate in call.gates:
        report = _as_report(gate(envelope, run))
        violations.extend(report.violations)
    if not violations:
        break
    if gate_attempt > phase.params.retries:
        raise GateFailure(...)
    result = send("Your previous response failed validation... Fix ...")
    envelope, attempt = _parse_with_retries(run, phase, call, result, send)

# after all sends, before accepting the envelope
paths_touched = permissions.enforce(run, phase, agent, tree_before)
```

逻辑：parse/gate问题适合用同一context correction；越权write已经发生，不允许re-prompt“纠正”，而是rollback+abort。边界是tree snapshot只在整段多次send之前/之后各一次，无法归因哪一send改变了什么；外部并发进程变化也可能被误算给Agent。

**代码块 3：`diff_matches_claims`名称承诺diff，实际只查路径存在**  
来源：[`gates.py#L61-L68`](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/templates/adws/adw_modules/gates.py#L61-L68)

```python
def diff_matches_claims(envelope: EnvelopeBase, run) -> GateReport:
    """Every file claimed changed must exist on disk."""
    report = GateReport()
    for f in getattr(envelope, "changed_files", []):
        p = Path(f)
        report.check(f, p.exists(),
                     f"exists, {_size(p)}" if p.exists()
                     else "claimed changed file does not exist")
    return report
```

本机throwaway repo中`existing.txt`已commit且从未修改，envelope却claim其changed；函数真实返回`passed=True`。open issue [#6](https://github.com/disler/super-simple-software-factory/issues/6)也报告claimed-but-unchanged与changed-but-unclaimed，并指出后续`commit_all()`会提交整个working tree。边界：这是本机独立复现，不是仅复述issue；但本机没有运行真实Agent造成5,222-file commit。

**代码块 4：Permission snapshot把tracked内容压成numstat计数，不是content fingerprint**  
来源：[`permissions.py#L50-L74`](https://github.com/disler/super-simple-software-factory/blob/de31374882e7a4e3e5b7bb9bd09e69dc2f779356/.claude/skills/sssf/templates/adws/adw_modules/permissions.py#L50-L74)

```python
def snapshot(run) -> dict[str, str]:
    fingerprints: dict[str, str] = {}
    for line in _git(["diff", "HEAD", "--numstat"], run.repo_root).splitlines():
        fields = line.split("\t")
        if len(fields) >= 3:
            path = fields[-1].strip()
            fingerprints[path] = f"{fields[0]},{fields[1]}"
    for path in _git(["ls-files", "--others", "--exclude-standard"],
                     run.repo_root).splitlines():
        fingerprints[path.strip()] = "untracked"
    return fingerprints

def changed_paths(before, after) -> list[str]:
    return sorted({p for p in set(before) | set(after)
                   if before.get(p) != after.get(p)})
```

本机独立fixture：base为`base\n`；engineer先改成一行`engineer dirty\n`，snapshot为`{'tracked.txt':'1,1'}`；模拟Agent再改成一行`agent changed same numstat\n`，after仍为`{'tracked.txt':'1,1'}`，`changed_paths=[]`，当前内容已改变。也就是说注释所称“已dirty文件再次编辑仍会注册”只在numstat计数变化时成立。边界：对clean tracked文件或新untracked文件仍能检测；本机另一个fixture确认read-only Agent新增`forbidden.tmp`会触发`PermissionBreach`并删除。

#### 依赖分析与供应链风险

- 12个ADW脚本各自用PEP 723声明`pydantic`、`python-dotenv`、`pyyaml`、`rich`，**均无版本pin**；仓库没有`pyproject.toml`、requirements或Python lock。`uv run`首次会按当时registry解析，重现性与供应链审计弱于锁文件。
- 外部必需/可选工具包括`uv`、Pi coding agent、SQLite CLI、provider credentials；visualizer另有Bun/Vue/Vite/TypeScript/Oxlint依赖与`bun.lock`。Python控制面与optional UI是两个供应链。
- starter roster默认跨OpenRouter/Fireworks/OpenAI三provider；`agents.validate()`只验证model字符串/文件，不验证key或endpoint可用，失败会在链中途出现。
- fresh install没有执行网络Agent；`uv run adw_quality.py`自动解析并安装11个Python packages到uv环境后运行。该命令的成功只证明依赖当时可解析。
- Dependabot alerts disabled/403；公开repo advisories为空。仓库无Python lock可交给通用audit重放，本报告没有为optional visualizer运行`bun install/audit`，因此完整依赖漏洞状态 **待核验**。

#### README / docs / release / issues / source 交叉核验

- README的“code owns sequencing/retries/acceptance、Agent owns bounded phase、typed envelope、SQLite trace”与`runner.py`、`agents.py`、`data_types.py`、`tracer.py`对应。
- README自己诚实披露placeholder quality、当前branch、无sandbox/branch-per-run/merge、Pi-only、`--force`覆盖；本机quality probe逐行确认四个placeholder echo均绿色。
- Releases API为空；没有tag/release artifact/semantic version可验证，固定main就是唯一源码快照。
- open issue [#6](https://github.com/disler/super-simple-software-factory/issues/6) 的diff gate问题本机已独立复现。
- open issue [#5](https://github.com/disler/super-simple-software-factory/issues/5) 报fresh Pi环境缺`models.json`时`context_window()`在fallback前崩溃；本机未安装Pi、未复现。
- open issue #1报告Agent未输出valid JSON；固定源码确有最多2次JSON correction，超过即fail，这是bounded而非保证成功。
- GitHub Actions API最近没有可列出的runs；无CI信号不能解释为测试通过。仓库也没有项目级test目录；本机只能做compile、fixture与offline path probe。

#### 真实测试结果

```text
$ python3 scripts/install.py        # fresh throwaway git repo
stamped: 44 file(s)

$ python3 scripts/install.py        # second run
stamped: 0 file(s)
skipped: 43

$ python3 -m compileall -q adws
compileall=passed

$ uv run adws/adw_quality.py "offline placeholder quality probe"
quality test: PLACEHOLDER ... passed (exit 0)
quality lint: PLACEHOLDER ... passed (exit 0)
quality typecheck: PLACEHOLDER ... passed (exit 0)
quality build: PLACEHOLDER ... passed (exit 0)
ADW complete; phases 2/2; quality_exit=0
```

```text
# independent gate/permission fixtures
claimed existing-but-unchanged file:
  diff_gate_passed_for_unchanged=True

read-only agent creates new untracked path:
  PermissionBreach ... forbidden.tmp — deleted
  forbidden_exists_after=False

pre-dirty file changed with same numstat:
  before={'tracked.txt':'1,1'}
  after ={'tracked.txt':'1,1'}
  changed_paths=[]
  current_content='agent changed same numstat'
```

准确结论：installer idempotency、Python syntax、offline phase/trace/finish通路和两个permission/gate behaviors已运行；没有provider key、Pi binary或sqlite3 CLI，未运行真实Agent chain、visualizer、commit phase、Windows、并发writer、branch/merge、sandbox或外部network。

#### 可复用经验

- 当gate名称声称“diff与claims一致”时，应优先做双向集合核验（claimed⊆actual且actual⊆claimed）并固定base revision，因为路径存在既不证明changed，也不披露unclaimed变化；边界是generated/ignored文件需要显式policy。
- 当post-hoc权限依赖工作树snapshot时，应优先hash内容或保存可恢复blob/patch，并拒绝预dirty高风险路径，因为numstat不是fingerprint；边界是content hash仍不能阻止write先发生。
- 当已知测试命令尚未配置时，应优先让quality phase返回`blocked/unconfigured`，不能让placeholder exit 0投影成green；边界是模板可提供demo mode，但状态必须与production acceptance分开。
- 当Agent correction可复用同一session时，应优先区分“可纠正claim错误”和“不可撤销effect breach”，因为后者不能靠再prompt恢复；边界是rollback也可能损坏预先未提交工作。

#### 30 分钟最小实验

在`runtime/hermes/github-learning-poc/worktree-claim-reconciliation/`做纯Git fixture：

1. fixtures：exact match、claimed unchanged、unclaimed tracked、unclaimed untracked、rename、deleted file、pre-dirty same-numstat、gitignored generated、external concurrent write。
2. schema：`base_commit, before_hashes, after_hashes, claimed_paths, actual_paths, ignored_paths, violations, rollback_capability`。
3. validator：双向set reconciliation；pre-dirty默认blocked或要求stash/blob backup；quality command为placeholder/unconfigured时terminal不得completed。
4. 不调用Agent/provider，不commit shared工作树，不应用上游patch，不修改现有orchestrator。

#### 风险边界

- **License**：GitHub API与root LICENSE为MIT；Pi、Python/Bun/npm dependencies、models/providers、stamped用户代码分别审查。
- **维护活跃度**：仓库创建于2026-08-02、固定main同日仅一个极简commit、查询时updated较新但pushed停在08-04；546 stars不弥补无release、无CI/test suite和早期open issues。
- **安全风险**：Agent拥有bash/write且当前branch运行；post-hoc permission不是sandbox；provider keys进入进程环境；`commit_all`可收集unclaimed tree；visualizer/server增加本地HTTP面。
- **验证风险**：`diff_matches_claims`本机已证明假绿；placeholder quality本机已证明假绿；permission numstat本机已证明预dirty同计数blind spot。
- **恢复风险**：越权修改预dirty内容时源码明确承认无法重建；`--force`覆盖config/prompts；SIGKILL/host crash仍可能绕过Python signal finalization。
- **供应链风险**：Python依赖不pin、无统一lock；Pi/provider/visualizer外部surface未audit；Dependabot disabled。
- **不适用场景**：一次性小任务、恶意repo、hostile多租户、必须保护未提交工作、要求branch isolation/human approval、把placeholder demo当CI。
- **不可自动执行**：不stamp到shared/Hermes配置、不写provider key、不运行真实Pi/Agent、不commit/push、不启动visualizer、不复制整个上游skill到capabilities。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：single `finish(accepted)` terminal primitive、typed gate evidence、same-session correction，以及本报告提出的bidirectional worktree claim/content-hash fixture。
- **需验证**：先修复/绕开diff false-positive、pre-dirty fingerprint和placeholder green；再与现有self-reflection-engine、GitHub-learning audit、verification-first和subagent四状态能力去重。
- **暂不沉淀**：SSSF skill整体、Pi adapter、starter roster/prompts、provider配置、current-branch commit workflow、visualizer。
- **今日动作**：只写runtime project card/lessons/candidate，不创建shared skill，不修改manifest/prefill/curated。

#### Hermes / shared hub 落地路径

1. runtime POC：`runtime/hermes/github-learning-poc/worktree-claim-reconciliation/{model.py,fixtures/,validate.py,test_contract.py,README.md}`。
2. GitHub-learning audit proposal：给`scripts/github_learning_orchestrator.py`未来增加report content hash、evidence path existence和actual-vs-declared project set；未配置checker应`blocked`，不以keyword计complete。本日不修改。
3. existing skill：POC通过后优先更新`capabilities/skills/research/github-hot-project-learning/`或现有verification能力的gate contract，不复制SSSF整体、不新建重叠factory skill。
4. shared分层：fixture/raw output留`runtime/hermes/`；本日报告留`inbox/hermes/daily/`；跨Agent稳定原则经治理后才进入curated。
5. OpenClaw runtime不存在；不创建OpenClaw job/adapter，只把schema设计成runner-neutral。

## 经验沉淀

1. **当Agent协议依赖某个skill/tool完成终态时，应优先在启动前验证required capabilities与实际loader配置一致，因为prompt要求不能创造不存在的调用面；边界是能力存在仍需真实completion evidence。**
2. **当长期记忆被压缩成prompt摘要时，应优先同时记录selection policy、coverage/overflow和可实际调用的detail retrieval，因为隐藏条目与空local store会造成“记了但用不到”；边界是扩大可见性必须受context/privacy预算。**
3. **当自动循环用命令exit决定终止时，应优先绑定immutable input、命令identity、worktree/artifact hash和coverage，因为placeholder或窄命令也能exit 0；边界是任何gate只证明它检查的predicate。**
4. **当gate声称reconcile Agent claims与实际效果时，应优先做双向集合核验并披露base revision，因为只查claimed path存在会同时漏掉虚假claim和未声明副作用；边界是generated/ignored路径需版本化policy。**
5. **当权限检查发生在Agent执行后时，应优先保护pre-dirty状态、使用content identity并保留可恢复backup，因为numstat计数不是内容fingerprint；边界是post-hoc检测本身不能阻止首次写入。**
6. **当模板尚未配置真实测试、lint或build命令时，应优先返回blocked/unconfigured而不是绿色demo，因为完整trace与一致exit也可能一致地记录假成功；边界是demo状态可单独保留。**
7. **当模型输出可通过同一session修正时，应优先把schema/gate violation与authority/effect breach分流，因为前者可re-prompt，后者必须停止、审计和恢复；边界是恢复失败需明确人工处理。**
8. **当项目快速活跃但release、main、artifact不同步时，应优先固定commit并分别核验source、tag、release asset和issues，因为最新stars/CI不能证明当前安装制品；边界是定向tests不能外推整个平台。**

### 跨项目机制抽象

| 维度 | Prime Agent | SSSF | 对 Hermes/shared hub 的窄迁移 |
|---|---|---|---|
| 循环所有者 | TypeScript host autonomous/goal policy | Python ADW phase graph | 让orchestrator拥有终态，不信Agent prose |
| 上下文handoff | session/global/local harness + child/files/messages | typed envelope + context_handoff | 每个handoff携带scope/revision/coverage |
| 完成 | quality gates、limits、goal.complete | phase status + `finish(accepted)` | gate evidence与业务acceptance分开 |
| 副作用 | host request/session/tool runtime | tools + post-hoc writes enforcement | 最终effect set必须与declaration双向核验 |
| 可恢复性 | daemon/worker/session artifacts/refinement history | same Pi session + SQLite/raw files | resume绑定immutable input与attempt identity |
| 今日暴露缺口 | memory不可见、skill依赖、daemon/release drift | false gate、placeholder green、numstat blind spot | 控制面也需要coverage与adversarial fixtures |

## 明日继续

1. 实现`runtime/hermes/github-learning-poc/worktree-claim-reconciliation/`最小fixture，先固定重现claimed-unchanged、unclaimed-change和pre-dirty same-numstat三个反例，再比较content hash与Git blob/patch方案。
2. 实现`runtime/hermes/github-learning-poc/harness-visibility-contract/`，验证global/parent-local/child-local三层visibility与overflow retrieval，不安装Prime Agent。
3. 将两项与已有`terminal-evidence-bundle`、`source-outcome-contract`、`attempt-evidence-envelope`和shared-memory-bridge候选去重，形成一个窄patch proposal，不新建第三套completion/receipt skill。
4. 若时间允许，只读检查Prime issue #1111所需capability preflight调用链，以及SSSF `git_helper.changed_files()/commit_all()` rename和whole-tree语义；不运行provider、不commit真实repo。

## 候选反哺

### Candidate Facts

- [ ] topic: deterministic control plane也必须披露visibility/effect/gate coverage | evidence: `prime-agent@a18809e` harness projection/local default + SSSF两个本机反例 | 建议: merge/update existing verification/completion fact，避免重复 | 安全级别: low
- [ ] topic: Agent协议required capability应在构造时验证 | evidence: Prime `goals.ts`显式要求`goal.complete()` + open #1111；本机E2E未复现 | 建议: create candidate after loader fixture | 安全级别: medium
- [ ] topic: Git numstat不能作为pre-dirty内容fingerprint | evidence: SSSF `permissions.py` + 本机before/after均`1,1`且内容改变 | 建议: create narrow verification candidate | 安全级别: medium
- [ ] topic: claim-vs-effect gate必须双向reconcile | evidence: SSSF `diff_matches_claims`源码 + 本机claimed unchanged仍passed + open #6 | 建议: update verification-first candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: harness-visibility-contract | 可复用场景: Hermes/shared memory、future-agent handoff、bounded prompt projection | 是否建议 shared: yes（fixture通过后更新既有shared-memory-bridge） | 原因: 跨Agent横切，但先解决scope/privacy与重复能力
- [ ] 名称: worktree-claim-reconciliation | 可复用场景: coding/research Agent副作用审计 | 是否建议 shared: no（当前仅Hermes runtime POC） | 原因: pre-dirty/rename/generated/concurrency policy尚未验证
- [ ] 名称: Prime Agent / SSSF product integration | 可复用场景: long-running Agent或software factory | 是否建议 shared: no | 原因: 与现有Hermes控制面重叠，且存在advisory、false gate、loader/daemon与sandbox边界

### Candidate Open Questions

- [ ] 问题: Prime Agent固定main能否在无provider的kernel fixture中稳定复现#819 child-local空store与prompt merged视图冲突？ | reason: visibility gap | priority: high
- [ ] 问题: `--goal --no-skills`是否应构造时blocked，其他protocol-required skills是否存在同类组合缺口？ | reason: capability contract | priority: high
- [ ] 问题: SSSF permission如何在不丢失engineer预dirty工作时证明Agent未改同numstat内容？ | reason: recovery/authority gap | priority: high
- [ ] 问题: 双向diff gate如何处理rename、generated lockfile、ignored artifact、concurrent human edit和whole-tree commit？ | reason: adaptation | priority: high
- [ ] 问题: Prime npm audit的5个nodes在真实daemon/provider/extension路径中的reachability与fixed version是什么？ | reason: supply-chain | priority: high
- [ ] 问题: GitHub-learning orchestrator是否应把keyword score与artifact/content/evidence hash审计分离？ | reason: audit integrity | priority: medium

### 不应自动落地

- 不自动安装、登录或运行Prime Agent，不启动daemon、schedule、provider、RLM child、IPython或第三方skills。
- 不把SSSF stamp进shared/Hermes，不写provider key，不运行真实Agent chain，不commit/push，不启动visualizer。
- 不自动修改Hermes/OpenClaw config、provider、模型、auth、env、cron或secret；当前OpenClaw runtime不存在。
- 不直接写curated active fact，不从README/issue/assistant prose生成用户事实；候选先fixture、去重、评分和治理审查。
- 不复制上游完整源码/skill到shared capabilities；只保留必要的MIT源码短片段作为研究证据并抽象agent-neutral contract。
- 不把Prime 124 tests、SSSF compileall/placeholder green、空public advisories或Stars解释为产品安全/生产成熟度证明。
