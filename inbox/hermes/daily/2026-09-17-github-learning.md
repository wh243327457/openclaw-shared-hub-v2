---
type: case
status: archived
created: 2026-09-17
updated: 2026-09-17
domain: learning
tags: [github-learning, code-review, security-audit, coverage, verification]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
  - "[[03-学习/技术实践/00-技术实践索引]]"
---

# 2026-09-17 GitHub 热门项目学习报告

> 执行者：Hermes（当前 OpenClaw 运行时不存在；本次未调用 OpenClaw）  
> 查询时间：2026-09-17 14:40–14:55（UTC+08:00）  
> 发现方法：真实抓取 GitHub Trending daily HTML，再用 GitHub Repository API 核验速览项目的 Stars、Forks、Language、License、`updated_at` 与 `pushed_at`。Trending 只用于发现，不把页面排名或 “stars today” 当总 Stars。  
> 深读固定提交：`alibaba/open-code-review@75d7bc9b4e6a24246a0593940d37410c4299a598`；`cloudflare/security-audit-skill@c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`。动态 Stars 快照与固定源码 revision 分开记录。  
> 证据：`runtime/hermes/github-hot-project-learning/evidence/2026-09-17/`；源码浅克隆仅在 `/tmp/github-learning-2026-09-17/`，未把源码或依赖缓存写入 shared。

## 今日结论

**今天最值得迁移的共同主线是：先把“要检查什么、覆盖了什么、输入究竟是哪一版”封进宿主可验证的确定性证据层，再让 Agent 处理语义判断；但 schema/路径校验不能冒充 artifact 真实存在，LLM 分组也不能改变 coverage denominator。OpenCodeReview 展示了 `sealed input → deterministic selection → coverage seal → bounded semantic grouping → typed terminal manifest`，Cloudflare security-audit-skill 展示了 `canonical coverage units → 独立 hunt/verify → typed verdict → schema validator`，二者的公开 issue 又共同证明：没有 read-back 的证据引用仍可假绿。**

### 今日真实验证摘要

- `alibaba/open-code-review`：本机起始 Go 为 `1.22.2`，`go.mod` 要求 `1.25.5`；使用 Go 官方 `GOTOOLCHAIN=auto` 下载匹配工具链后，`go test -json ./...` 真实结果为 **23 packages passed / 4,623 tests passed / 6 skipped / 0 failed**。未调用任何 LLM/provider，也未执行真实代码审查。
- OpenCodeReview 固定 commit 的 GitHub checks 在查询时并非全绿：9 个 check 中，`test` 已 **failure**、`windows` 仍 **queued**，其余已列出的 build/deploy/cross-compile 成功。本机全仓测试绿色不能覆盖上游 CI 的 OS/race/coverage 差异，CI 失败根因**待核验**。
- OpenCodeReview Repository Security Advisories API 返回公开 `GHSA-wwg6-qfxw-xffj`（medium，CVSS 5.3，受影响 `<1.11.1`，patched `1.11.1`）：不可信仓库 `rule.json` 曾可把任意本地文本读入 LLM prompt；今日源码与 latest release `v1.12.4` 高于 patched version，但 resolved binary/package 路径仍应独立核验。
- `cloudflare/security-audit-skill`：零依赖 Node validators 的两个测试文件真实结果为 **65 passed / 0 failed**。测试覆盖输入字节/深度/数组预算、UTF-8、symlink/FIFO、canonical ID、typed verdict、severity 上界与路径安全。
- 我又按 open issue #21 真实构造一个 `local_checks[].artifact` 指向不存在文件的 ledger：`validate-coverage-ledger.cjs` 输出 **`PASS: 1 coverage units valid`**，而 read-back 为 **`artifact_exists=no`**。这证明当前 validator 只校验 artifact 路径形状/owner prefix，不校验证据对象存在性；issue 声明在本机得到复现。
- 两仓 Dependabot vulnerability-alerts endpoint 对当前 token 均返回 404；这只表示 endpoint 不可用/无权，不能声称没有依赖漏洞。OpenCodeReview 共解析 152 个 Go modules（含 main；无 replace、无 retracted 标记），没有运行 `govulncheck`；security-audit-skill 无 package manifest/runtime 依赖，但 Node 运行时与安装器仍是独立供应链面。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [supabase/supabase](https://github.com/supabase/supabase) | 109,892 | 14,066 | TypeScript | Apache-2.0 | 2026-09-17T06:51:05Z | 高活跃平台，今日不扩散主线 |
| [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | 78,043 | 8,634 | Java | Apache-2.0 | 2026-09-15T16:02:22Z | 成熟逆向工程平台，范围过大 |
| [cline/cline](https://github.com/cline/cline) | 68,475 | 7,394 | TypeScript | Apache-2.0 | 2026-09-17T06:28:41Z | Agent 热门项目，历史模式重叠 |
| [roboflow/supervision](https://github.com/roboflow/supervision) | 50,684 | 4,815 | Python | MIT | 2026-09-16T20:26:40Z | 视觉工具库，与今日证据主线较弱 |
| [JustVugg/colibri](https://github.com/JustVugg/colibri) | 35,222 | 3,702 | C | Apache-2.0 | 2026-09-15T21:33:15Z | 本地推理值得后续观察 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 32,809 | 2,321 | Go | Apache-2.0 | 2026-09-17T06:27:36Z | **深读：sealed input、coverage manifest、确定性/Agent 混合** |
| [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | 25,678 | 3,509 | Go | **NOASSERTION** | 2026-09-17T06:51:20Z | License API 未识别；不复制源码 |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | 24,372 | 2,926 | Python | Apache-2.0 | 2026-09-17T00:17:25Z | plugins/skills 生态，先避免重复研究 |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 8,029 | 451 | JavaScript | MIT | 2026-09-14T19:29:02Z | **深读：coverage ledger、独立验证、schema 与 artifact gap** |
| [rlaope/oh-my-hermes](https://github.com/rlaope/oh-my-hermes) | 2,629 | 189 | Python | MIT | 2026-09-17T06:09:25Z | Hermes 生态观察；不因同名自动接入 |

> 上表 Stars 是 14:52 左右的 API 动态快照，后续会变化；License 是 repository API 的根 SPDX，不覆盖依赖、子目录、模型、数据、plugins 或 release asset。`open_issues_count` 含 PR。速览仓只作元数据筛选，不对未深读仓作代码能力结论。

## 深读项目

### 1. alibaba/open-code-review

- **一句话判断**：值得学的不是“再做一个 AI code reviewer”，而是它把 moving Git refs、文件选择、预算、覆盖分母、每组终态和 session persistence 放在 Agent 外的确定性控制面；但其规则文件历史漏洞、动态 CI failure 与高频 release 说明不能把 README 的 assurance 宣称当成现状证明。
- **解决的问题**：替代“把整个 diff 丢给通用 Agent、靠 prompt 自觉覆盖、模型自己报行号、失败时只看 stdout/exit 0、resume 时重新解析 moving ref”的旧做法。
- **URL / API 快照**：https://github.com/alibaba/open-code-review ；**Stars: 32,809 / Forks: 2,321 / Language: Go / License: Apache-2.0**；`updated_at=2026-09-17T06:51:45Z`，`pushed_at=2026-09-17T06:27:36Z`，API `open_issues_count=178`（含 PR），default branch `main`。
- **固定提交**：[`75d7bc9b4e6a24246a0593940d37410c4299a598`](https://github.com/alibaba/open-code-review/commit/75d7bc9b4e6a24246a0593940d37410c4299a598)，committer time `2026-09-17T06:27:36Z`，`feat(pages): standardize web crawler policy (#939)`。
- **Release / issue / advisory 证据**：latest release [`v1.12.4`](https://github.com/alibaba/open-code-review/releases/tag/v1.12.4)，`published_at=2026-09-16T10:12:20Z`、API `immutable=false`，6 平台 binaries 与 `sha256sum.txt` 都有 API digest；release notes含 workspace binary/untracked oversized fixes。open issue [#1316](https://github.com/alibaba/open-code-review/issues/1316) 询问 spec-aware review，说明外部需求到具体模块的绑定仍缺清晰官方入口。公开 advisory [`GHSA-wwg6-qfxw-xffj`](https://github.com/alibaba/open-code-review/security/advisories/GHSA-wwg6-qfxw-xffj) 说明旧版仓库规则路径可越界读取宿主文本并送往 LLM。
- **来源交叉核验**：README、architecture docs、`ASSURANCE_CASE.md`、release API/assets、issue #1316、security advisory、固定源码、Go manifests、GitHub check-runs 与本机 full Go test。

#### 架构 / 实现与数据流

```text
ocr review
  -> ResolveIdentity: moving commit/range refs -> immutable commit SHAs
  -> git diff provider -> []model.Diff
  -> selectFiles（pure）
       binary -> secret path -> user exclude/include -> extension/default path
       -> deletion -> per-file token limit
  -> registerCoverage(selected) + seal denominator
  -> resume: only reuse manifest-settled fingerprinted items
  -> grouping
       small set -> deterministic local grouping
       large set -> LLM sees metadata only, not diff body
       parse/error/truncation -> per-file fallback
       max 10 files + prompt token valve
  -> bounded concurrent group subtasks
       optional plan -> tool loop -> code_comment/task_done
       budget/timeout/panic/error -> typed per-file outcome
  -> line resolution + review filter + second resolution
  -> wait background compression
  -> immutable run manifest + session_end + JSON/text/SARIF projection
```

关键点不是“LLM 参与分组”，而是 LLM 只做 best-effort optimization：输入只有文件 metadata，未知/重复 index 被忽略，遗漏文件自动单列，解析失败退化 per-file，分组后仍受文件数/token limit 限制。真正的 coverage denominator 在 grouping 前已冻结，所以模型不能通过“没分到组”让文件从分母消失。

#### repo tree 摘要

固定 commit `git ls-files` 为 **830 tracked paths**；根目录实际包含：

```text
open-code-review/
├── cmd/opencodereview/             # CLI、flags、JSON/SARIF 输出、resume admission
├── internal/
│   ├── agent/                      # selection、sealed identity、grouping、dispatch、manifest
│   ├── diff/                       # workspace/commit/range diff、hunk 与 line resolve
│   ├── llmloop/                    # tool loop、budget、compression、terminal
│   ├── config/                     # template/rules/allowlist/provider config
│   ├── session/                    # JSONL events、resume、run manifest
│   ├── tool/                       # read/search/comment/task_done 等工具
│   ├── llm/                        # OpenAI/Anthropic client 与 token accounting
│   ├── telemetry/                  # spans/metrics，不附 prompt/response content
│   └── viewer/                     # 本地 session viewer
├── skills/ + plugins/              # portable skill 与各 host adapter
├── pages/                          # docs/site frontend
├── npm/ + bin/ + scripts/          # 多平台 npm launcher/install/release
├── .github/workflows/              # vet/govulncheck/race/full tests/release
├── go.mod / go.sum                 # Go 1.25.5；锁定 module graph
├── package.json                    # npm launcher；postinstall 获取 binary
├── ASSURANCE_CASE.md               # threat model 与安全声明
└── LICENSE                         # Apache-2.0
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `internal/agent/identity.go` | preflight sealed identity | 在创建新 session 前固定 commit/range，重跑相同 selection 后计算 source/rule/repository identity |
| `internal/agent/selection.go` | 单一纯 selection primitive | preview 与真实 run 共用；secret path 位于 user include 之前；size gate 只在配置 limit 时计数 |
| `internal/agent/grouping.go` | semantic grouping + fallback | metadata-only LLM call；index 响应；遗漏补回；max 10；token 超限拆回单文件 |
| `internal/agent/agent.go` | pipeline 与 coverage terminal | grouping 前 register/seal coverage；budget pre-admission；per-file completed/failed；background join 后 finalize |
| `internal/llmloop/loop.go` | tool-use main loop | session-scoped cache key；typed `task_done DONE/FAILED`；3 empty rounds；max-round grace call |
| `internal/llmloop/compression.go` | 三段式上下文压缩 | frozen/compress/active；60% async、80% sync；conversation-local compression ownership |
| `internal/session/` | durable evidence | JSONL event、manifest、resume lineage、terminal coverage projection |
| `internal/config/rules/` | 规则解析与 hash | rule text/config 进入 run identity；历史 advisory 提醒 repo config 是 authority surface |
| `.github/workflows/ci.yml` | CI policy | `go vet ./...`、`govulncheck ./...`、Linux race/full tests、Windows tests |

#### ⭐ 源码精读

**代码块 1：`ResolveIdentity()` 在 session 创建前重现真实 selection 并封存 moving ref。**

```go
func ResolveIdentity(ctx context.Context, args Args) (*SealedInput, error) {
    defer stdout.Quiet()()
    resolution, err := resolveInputBeforeDiff(ctx, args)
    if err != nil { return nil, err }
    if resolution != nil { args.SealedInput = resolution }

    a := &Agent{args: args}
    if err := a.loadDiffs(ctx); err != nil {
        return nil, fmt.Errorf("load diffs: %w", err)
    }
    a.diffs, _ = summarizeSelection(a.selectFiles(a.diffs))
    return &SealedInput{Identity: a.runIdentity(), Resolution: a.inputResolution}, nil
}
```

逻辑摘要：resume admission 先固定 `commit/range` 的实际 SHA，再用和 real run 相同的 diff + selection 计算 identity；拒绝 resume 时不会先写新 session 痕迹。边界：workspace dirty state 仍是动态对象，identity/hash 不能代替 effect-time worktree/repository authority。

**代码块 2：`selectFiles()` 与 `whyExcluded()` 把文件覆盖入口变成 pure deterministic gate。**

```go
func (a *Agent) selectFiles(diffs []model.Diff) []fileDecision {
    limit := llmloop.PromptTokenLimit(a.args.Template.MaxTokens)
    decisions := make([]fileDecision, 0, len(diffs))
    for _, d := range diffs {
        dec := fileDecision{Diff: d, Reason: a.whyExcluded(d)}
        switch {
        case dec.Reason != ExcludeNone:
        case d.IsDeleted:
            dec.Reason = ExcludeDeleted
        case limit > 0:
            dec.DiffTokens = llm.CountTokens(d.Diff)
            if dec.DiffTokens > limit { dec.Reason = ExcludeTooLarge }
        }
        decisions = append(decisions, dec)
    }
    return decisions
}

func (a *Agent) whyExcluded(d model.Diff) ExcludeReason {
    if d.IsBinary { return ExcludeBinary }
    if allowedext.IsSecretPath(d.OldPath) || allowedext.IsSecretPath(d.NewPath) {
        return ExcludeSecret
    }
    // user exclude/include -> extension allowlist -> default path
    return ExcludeNone
}
```

逻辑摘要：preview 与真实 run 共享一个无 I/O/无 LLM 的 selection primitive；credential path 在 user include 前拒绝，避免 include 把高风险输入重新纳入。边界：静态 secret path 规则只能降低已知风险，不能识别源码正文中的全部 secret；被 filter 的相关 diff 可被只读 context tool 查询，仍要约束外发面。

**代码块 3：`groupDiffs()` 把 LLM 限定为可失败的优化器。**

```go
func groupDiffs(ctx context.Context, diffs []model.Diff, client llm.LLMClient,
    modelName string, tpl template.Template, tokenLimit int,
    sessOpts *groupingSessionOpts) groupDiffsResult {
    if len(diffs) <= 1 { return groupDiffsResult{groups: toSingleFileGroups(diffs)} }
    totalChanged, _ := diffsChurn(diffs)
    if strategy := tpl.GroupingPlan(len(diffs), totalChanged); strategy != template.GroupingViaLLM {
        return groupDiffsResult{groups: groupWithoutLLM(ctx, diffs, strategy, tpl, totalChanged, tokenLimit)}
    }
    groups, usage, err := callGroupingLLM(/* metadata only */)
    if err != nil { return groupDiffsResult{groups: toSingleFileGroups(diffs), usage: usage} }
    groups = enforceGroupTokenBudget(groups, tokenLimit)
    return groupDiffsResult{groups: groups, usage: usage}
}
```

逻辑摘要：小 change set 本地决策，大 change set 才调用 LLM；失败不阻断 review，而是回到 one-file-per-group。`parseGroupingResponse()` 还会去重 index、补回遗漏文件并按 10 文件切块。边界：语义 grouping 仍会改变跨文件 context、成本和并发；fallback 保覆盖，不保证同等发现质量。

**代码块 4：`dispatchSubtasks()` 在并发前冻结 coverage，并在 admission 前做预算判断。**

```go
func (a *Agent) dispatchSubtasks(ctx context.Context) ([]model.LlmComment, error) {
    if err := a.registerCoverage(a.diffs); err != nil {
        a.recordWarning("manifest_error", "", err.Error())
    }
    toDispatch := a.applyResume(a.diffs)
    groups := groupDiffs(/* ... */).groups

    for _, group := range groups {
        if a.args.MaxTokensBudget > 0 {
            projected := a.runner.TotalTokensUsed() + estimateGroup(group)
            if projected > a.args.MaxTokensBudget {
                a.budgetExceeded.Store(true)
                // pending failure cause; undispatched items become failed(budget)
                break
            }
        }
        // bounded goroutine; per-file completed/failed/reused outcome
    }
}
```

逻辑摘要：coverage denominator 在 resume/grouping/dispatch 前登记；aggregate budget 是 dispatch admission gate，不把“受控截断”伪装成 run crash；group 内部分文件已有 comments 时可 completed，其余 failed。边界：in-flight groups 可造成最多约 concurrency 数量的预算 overrun；估算也不是真实计费。

**代码块 5：`RunMainTask()` 要求显式 terminal，并为用尽预算提供窄 grace round。**

```go
func (r *Runner) RunMainTask(ctx context.Context, messages []llm.Message,
    taskKey string) (bool, MainLoopStop, error) {
    toolReqCount := r.deps.Template.MaxToolRequestTimes
    const maxConsecutiveEmptyRounds = 3
    for toolReqCount > 0 {
        resp, err := r.deps.LLMClient.CompletionsWithCtx(/* tools + session key */)
        if err != nil { return false, StopNone, err }
        calls := resp.ToolCalls()
        if len(calls) == 0 { /* nudge */; continue }
        for _, call := range calls {
            cp := r.executeToolCall(ctx, taskKey, call, rec, thinking)
            if cp.Failed { return false, StopNone, fmt.Errorf("task failed: %s", cp.Data) }
            if cp.Completed { taskCompleted = true }
        }
        if taskCompleted { return true, StopNone, nil }
        // empty-result counter + compression gate
    }
    r.runGraceRound(ctx, messages, taskKey, sessionID)
    return false, StopMaxRounds, nil
}
```

逻辑摘要：模型 prose 或无 tool call 不等于完成；`task_done` 可显式 `DONE/FAILED`，连续 3 次空结果和 max rounds 是不同终止原因；grace round 只开放 `code_comment`/`task_done`，不再继续探索。边界：模型调用 `DONE` 仍只是 subtask claim，最终 coverage/manifest 与 comments read-back 才是宿主完成证据。

#### 依赖分析与供应链风险

- `go.mod` 要求 Go `1.25.5`，直接依赖包括 Bubble Tea/Lipgloss、Anthropic SDK、OpenAI SDK、AWS SDK config、MCP Go SDK、Cobra、tiktoken 与 OpenTelemetry；`go list -m all` 解析 **152 modules（含 main）**，无 replace、无 retracted 标记。依赖范围广，尤其 provider/MCP/telemetry/grpc 是网络与数据出口面。
- 根 `package.json` 是 launcher，不含普通 dependencies，但有 6 个 platform optional packages，且 `postinstall` 执行 `scripts/install.js`；source checkout、npm wrapper、platform package、GitHub release binary 是不同制品面。
- `v1.12.4` API `immutable=false`；assets 有 GitHub digest 与 `sha256sum.txt`，但今日未下载/执行 binary，也未核签名或可复现构建。digest 证明平台记录的 bytes identity，不证明 source correspondence。
- 本机 `go test ./...` 全绿；没有运行 `go vet`、`-race`、`govulncheck`、Node/pages tests 或 release smoke。GitHub check 的 `test` failure 说明不能将本机窄环境外推为上游全绿。
- Dependabot endpoint 404；公开 advisory 只覆盖已披露记录。`ASSURANCE_CASE.md` 的 “Dependabot/govulncheck” 是流程声明，不是今日实际扫描结果。

#### 可复用经验

- 当 resume、缓存或审计依赖 Git ref/workspace 输入时，应优先在创建新 run 前固定 immutable revision，并用真实 selection 重算 identity，因为 moving ref 与 preview/run 漂移会让旧证据错配；边界是 identity 不替代权限与 dirty worktree effect-time 重验。
- 当 Agent 只负责语义 grouping/ranking 时，应优先先冻结确定性 coverage denominator，再把 Agent 输出当可失败优化，并补回遗漏/冲突项，因为模型分组不能定义“哪些对象不存在”；边界是 fallback 仍可能降低跨文件发现质量。
- 当预算、timeout、panic 或部分结果会截断并发任务时，应优先逐 item 记录 completed/reused/failed(reason) 并从 manifest 推导 terminal，因为 group error、exit 0 或有 comments 都不是完整 coverage；边界是 manifest builder 自身也需 fixture 与持久化 read-back。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/sealed-selection-coverage-v0/` 做纯 Python fixture：输入 6 个 synthetic file records 和 moving-ref A/B；实现 `seal ref -> pure selection -> coverage set -> untrusted grouping proposal -> omission/duplicate repair -> budget stop -> manifest`。验证：(1) grouping 漏项不改变 denominator；(2) ref 在 admission 后变化不会改变已封存 source hash；(3) budget stop 产生 partial 而不是 completed；(4) terminal manifest read-back hash 一致。不调用 provider、不读取真实 repo secret、不改 Hermes/shared 配置。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 Apache-2.0；可抽象机制。依赖、npm platform packages、plugins、LLM SDK、模型输出与 release assets需独立审计。
- **维护活跃度**：最近 10 个 commit 横跨 2026-09-16 至 09-17；5 个最新 release 集中在 09-12 至 09-16，极活跃也意味着接口/制品 churn 高。今日 main check 非全绿。
- **安全风险**：历史 rule path traversal/local-file exfiltration advisory 直接说明“repo config 是 authority surface”；MCP、自定义 endpoint、shell/key commands、viewer、telemetry 与 session logs 都需独立 gate。当前版本高于 patch，不等于所有入口安全。
- **隐私风险**：代码/diff/rules 会进入配置的 LLM provider；architecture docs称 telemetry 不附内容，但 provider 出域仍是核心边界。不能默认把私有仓库交给任意 endpoint。
- **局限性**：README 自报 benchmark 未在今日复现；Agent review 的 precision/recall 与特定 model/provider/template 绑定。issue #1316 所问的 external spec-to-module contract 仍待官方确认。
- **验证局限**：本机未执行真实 review、provider、MCP、viewer、npm launcher、release binary、race/vet/govulncheck；上游 `test` failure 原因待核验。

#### ⭐ Skill 升格判断

**需二次验证。** 不安装或迁移完整 OpenCodeReview skill/runtime。只提出 `sealed-input-selection-coverage-contract` 候选；它与现有 verification-first、completion receipt、effect-scope、GitHub-learning orchestrator 高度重叠，应优先更新现有 class-level workflow，而不是再建一个 code-review 大 skill。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/sealed-selection-coverage-v0/`；输入 synthetic manifest，输出 `sealed-input.json`、`selection.json`、`coverage-manifest.json`、`receipt.json`。
2. Hermes orchestrator：在 prepare 后保存 discovery query/API timestamp 与候选 revision；研究报告 audit 前计算 requirements→evidence coverage，不能只扫 Markdown 关键词。
3. shared scripts：若 POC 通过，将 pure checker 作为现有 GitHub-learning/verification helper；共享根必须由 `scripts/resolve_shared_root.py` 解析，不硬编码宿主路径。
4. shared skill：优先迭代现有 verification/self-reflection 或 GitHub learning 契约，加入 `selection denominator sealed before LLM optimization` 与 typed per-item terminal。
5. OpenClaw 当前不存在，本次不修改其配置/runtime；future agent 只复用 neutral manifest contract，不复制 provider key、repo ID、绝对路径或上游代码。

---

### 2. cloudflare/security-audit-skill

- **一句话判断**：它最值得学的是把安全审计从“Agent 写一篇看似专业的报告”改成 coverage-led、independent verification、typed verdict、schema-validated records；但本机已证实 ledger validator 可接受不存在的 artifact，因此“schema valid”必须和“evidence object verified/read back”分开。
- **解决的问题**：替代单 Agent checklist 扫描、hunter 自证、把 blocked hypothesis 赋 severity、prose 报告与 JSON 漂移、一次 run 暗示完整覆盖、target-controlled build 直接继承 host 环境的旧做法。
- **URL / API 快照**：https://github.com/cloudflare/security-audit-skill ；**Stars: 8,029 / Forks: 451 / Language: JavaScript / License: MIT**；`updated_at=2026-09-17T06:52:29Z`，`pushed_at=2026-09-14T19:29:02Z`，API `open_issues_count=15`（含 PR），default branch `main`。
- **固定提交**：[`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`](https://github.com/cloudflare/security-audit-skill/commit/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8)，committer time `2026-09-14T19:28:54Z`，`Clarify guidance and full audit modes`。
- **Release / issue 证据**：latest release API 为 404，tags API 返回空列表，当前没有可核验 release/tag 版本面。open issue [#20](https://github.com/cloudflare/security-audit-skill/issues/20) 报告一个外部 blind seeded comparison 的覆盖/成本 gap；这些数字是 issue 作者声明，今日未独立复现实验，**待核验**。open issue [#21](https://github.com/cloudflare/security-audit-skill/issues/21) 报告 validator 接受 nonexistent artifact；今日已本机复现。
- **来源交叉核验**：README、`SKILL.md`、11 类 companion docs、schema、两个 validators/tests、issues #20/#21、固定源码、GitHub checks 与本机 Node tests。

#### 架构 / 实现与数据流

```text
explicit full audit request
  -> parent resolves target/source_ref/profile/scope/budget/output ownership
  -> run-metadata.json (in_progress)
  -> Phase 1 reconnaissance
       architecture.md
       canonical coverage-ledger.json
  -> Phase 2 hunter waves
       one isolated agent root each
       source/static or sandboxed local checks
       parent-only ledger updates + coverage critics
  -> Phase 3 fresh verifier per candidate
       finder != verifier
       try to disprove / exact blocker
  -> Phase 4 findings.json
       confirmed | needs_validation | rejected
       validate-findings.cjs + validate-coverage-ledger.cjs
  -> Phase 5 fresh final record verification
       material replacement -> another verifier
  -> Phase 6 reports derived from records/ledger
       REPORT.md / FINDINGS-DETAIL.md / NEEDS-VALIDATION.md
  -> terminal: all artifacts + both validators pass OR incomplete(exact reason)
```

其能力不是 runtime library，而是 agent-neutral contract + deterministic validators。parent 独占 shared run files，hunter/verifier 各有独立 scratch/artifacts；target code 必须 no network、empty allowlisted env、read-only target、resource limits。找不到 OS-enforced sandbox 时不运行目标代码，保留 `needs_validation`。

#### repo tree 摘要

固定 commit `git ls-files` 为 **22 tracked paths**，根目录只有 `skills/` 与文档/license：

```text
security-audit-skill/
├── README.md
├── LICENSE                              # MIT
└── skills/security-audit/
    ├── SKILL.md                         # modes、safety、budget、6 phases、terminal
    ├── RECONNAISSANCE.md                # trust boundary 与 ledger seed
    ├── HUNTING.md                       # hunters、critics、candidate protocol
    ├── VALIDATION-AND-REPORTING.md       # verifier、records、derived reports
    ├── ATTACK-CLASSES.md                # core attack taxonomy
    ├── AI-AND-LLM.md                    # prompt/tool/output classes
    ├── WEB-PROTOCOL-AND-AUTH.md         # HTTP/auth classes
    ├── CLIENT-SIDE.md                   # DOM/message/UI classes
    ├── SUPPLY-CHAIN-AND-RELEASE.md      # dependency/CI/update/plugin classes
    ├── CLOUD-AND-DEPLOYMENT.md          # IAM/IaC/container/serverless
    ├── PROTOCOLS-RPC-AND-MESSAGING.md   # RPC/queue/webhook/stream
    ├── RESOURCE-EXHAUSTION-AND-AVAILABILITY.md
    ├── DATA-ISOLATION-AND-LIFECYCLE.md
    ├── DESKTOP-MOBILE-AND-LOCAL-IPC.md
    ├── MEMORY-SAFETY-AND-BINARY.md
    ├── report-schema.json               # 3 verdict contract
    ├── validate-findings.cjs            # schema + semantic validator
    ├── validate-findings.test.cjs
    ├── validate-coverage-ledger.cjs     # canonical coverage/state validator
    └── validate-coverage-ledger.test.cjs
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `skills/security-audit/SKILL.md` | 权威 workflow contract | guidance/full mode 分离；parent ownership；sandbox；budget reserves；6 phases；exact terminal |
| `report-schema.json` | typed finding truth | `confirmed`/`needs_validation`/`rejected` 三分；只有 confirmed 有 severity；字段额外项拒绝 |
| `validate-findings.cjs` | findings gate | 5 MiB、64 depth、1,000 items、100 errors；safe input open；schema interpreter + semantic checks |
| `validate-coverage-ledger.cjs` | coverage gate | canonical tuple/ID、排序、owner、state/evidence invariants、attempt archive、path checks |
| `validate-findings.test.cjs` | adversarial fixtures | Unicode/control、FIFO/symlink、oversize/deep JSON、duplicate、severity 与 path fixtures |
| `validate-coverage-ledger.test.cjs` | ledger fixtures | canonical collision、state evidence、reassignment、artifact owner-prefix；没有存在性 read-back fixture |
| `HUNTING.md` | isolation/handoff | hunter output 与 shared state 写入分离；critic 负责 gap wave |
| `VALIDATION-AND-REPORTING.md` | independent verifier | final prose 从 verified records 派生，避免 report/JSON 双真相 |

#### ⭐ 源码精读

**代码块 1：`canonicalCoverageId()` 从精确 UTF-8 refs 生成稳定 ID，而不是从 display prose 猜 slug。**

```js
function canonicalCoverageId(refs) {
  if (!isObject(refs)) throw new TypeError("canonical_refs must be an object");
  const fields = hasOwn(refs, "lifecycle") ? [...REF_FIELDS, "lifecycle"] : REF_FIELDS;
  if (Object.keys(refs).length !== fields.length ||
      fields.some((field) => !hasOwn(refs, field))) {
    throw new TypeError("canonical_refs has missing or unexpected fields");
  }
  return fields.map((field) => encodeCanonicalRef(refs[field])).join("::");
}
```

逻辑摘要：coverage identity 由 `surface/boundary/subsystem/attack_class[/lifecycle]` 精确编码；validator 还拒绝 duplicate ID、不同语义 collision、同语义 alias，并要求 lexical sort。边界：canonical ID 保身份一致，不证明 unit 真被检查或 evidence 存在。

**代码块 2：`validateChecks()` 约束 source/local evidence 与 agent owner，但只验证路径语义。**

```js
function validateChecks(value, location, errors) {
  value.forEach((check, index) => {
    const base = `${location}[${index}]`;
    if (!isSafeAgentId(check.agent_id)) errors.push(/* ... */);
    validateStringArray(check.reviewed_paths, `${base}.reviewed_paths`, errors,
                        { allowEmpty: false, pathValue: true });
    if (check.method === "source" && check.artifact !== null) {
      errors.push(`${base}.artifact: source-only check must use null`);
    } else if (check.method === "local") {
      if (!isOwnedArtifactPath(check.artifact, check.agent_id)) {
        errors.push(`${base}.artifact: local check requires an artifact owned by agent ...`);
      }
    }
  });
}
```

逻辑摘要：source-only evidence 必须 `artifact=null`；local evidence 必须指向 `agents/<agent>/artifacts/...`，防止 cross-agent path claim。关键边界：函数没有 output root，也没有 `open/fstat/hash`；因此合法字符串可以引用不存在对象。今日 reproduction 得到 `PASS` + `artifact_exists=no`。

**代码块 3：`readFileWithinLimit()` 对 validator 输入本身采用 no-follow、nonblocking、regular-file、size 与 strict UTF-8 gate。**

```js
function readFileWithinLimit(file) {
  const noFollow = fs.constants.O_NOFOLLOW;
  const nonBlock = fs.constants.O_NONBLOCK;
  if (!Number.isInteger(noFollow) || !Number.isInteger(nonBlock)) {
    throw new SafeInputError("OS no-follow and nonblocking input protection is unavailable");
  }
  const descriptor = fs.openSync(file, fs.constants.O_RDONLY | noFollow | nonBlock);
  try {
    const stat = fs.fstatSync(descriptor);
    if (!stat.isFile()) throw new SafeInputError("input must be a regular file");
    if (stat.size > MAX_INPUT_BYTES) throw new SafeInputError("input exceeds byte limit");
    // bounded read -> fatal UTF-8 TextDecoder
  } finally { fs.closeSync(descriptor); }
}
```

逻辑摘要：拒绝 symlink、FIFO/device、超 5 MiB 与 invalid UTF-8；平台无法提供 no-follow/nonblocking 时 fail closed。这是“安全读取声明文件”的好范式。边界：输入 fd 安全不等于声明中引用的所有 evidence/artifacts 安全。

**代码块 4：`validateDocument()` 把 coverage unit 的 schema、identity、semantic alias 与排序集中到单一 gate。**

```js
function validateDocument(ledger) {
  const errors = createErrorList();
  if (!Array.isArray(ledger)) return ["$: expected a top-level array"];
  errors.push(...preflightDocument(ledger));
  const ids = new Map(), semantics = new Map();
  let previousId = null;
  for (let index = 0; index < ledger.length; index++) {
    const unit = ledger[index];
    errors.push(...collectUnitErrors(unit, index));
    // reject duplicate/collision/semantic alias
    if (previousId !== null && previousId > unit.coverage_id) {
      errors.push(`$[${index}].coverage_id: units must be sorted lexicographically`);
    }
    previousId = unit.coverage_id;
  }
  return errors;
}
```

逻辑摘要：validator 不只查 JSON shape，还查状态和证据 ownership、attempt archive、current owner freshness 与 canonical order；错误输出上限 100，避免恶意输入放大。边界：它验证 document coherence，不验证 audit completeness、source truth、artifact bytes 或 external deployment fact。

**代码块 5：`run()` 将 input parse、schema/semantic validation 和 terminal exit 明确分开。**

```js
function run(file) {
  if (!file) return 1;
  let contents;
  try { contents = readFileWithinLimit(file); }
  catch (error) { console.error("Failed to read coverage ledger: ..."); return 1; }

  try { preflightJsonText(contents); }
  catch (error) { console.error("Failed to parse coverage ledger: ..."); return 1; }

  const ledger = JSON.parse(contents);
  const errors = validateDocument(ledger);
  if (errors.length > 0) { console.error(`FAIL: ${errors.length} ...`); return 1; }
  console.log(`PASS: ${ledger.length} coverage units valid`);
  return 0;
}
```

逻辑摘要：read/parse/validation failures 都有 non-zero terminal；不把异常或空 findings 当 clean。边界：`PASS` 的准确语义只能是“这个 ledger 文档通过当前 validator”，不能写成“审计证据齐全”或“目标安全”。

**代码块 6：`report-schema.json` 强制把 certainty 与 severity 分离。**

```json
{
  "oneOf": [
    { "properties": { "verdict": { "const": "confirmed" },
      "severity": { "type": "object" } },
    { "properties": { "verdict": { "const": "needs_validation" },
      "blockers": { "type": "array", "minItems": 1 },
      "validation_plan": { "type": "object" } },
    { "properties": { "verdict": { "const": "rejected" },
      "reason": { "type": "string" } }
  ]
}
```

逻辑摘要：confirmed 需要 source trace、observed result、remediation、severity/confidence；needs_validation 只有 exact blockers/plan，不能偷带 severity；rejected 保留被推翻 claim，防止重复浪费。边界：schema 可确保字段纪律，不能确保 verifier 真独立、观察值真实或 severity calibration 正确。

#### 依赖分析与供应链风险

- 仓库无 `package.json`/lockfile；两个 validators 只用 Node built-ins（`fs/path/util/child_process/node:test`），运行时第三方 package surface 很小。Node runtime 本身仍须固定版本/来源。
- README 推荐 `npx skills add https://github.com/...`，这是外部 installer + moving repo URL；无人值守接入应固定 immutable commit、先 inventory/dry-run、核 license/hash/owner/conflict，不直接安装 main。
- 无 GitHub Releases、无 tags；source commit 是当前唯一可固定对象。没有 release artifact/signature/SBOM 证据。
- GitHub fixed commit 只有一个 CodeQL check，且 success；仓库自身没有 `.github/workflows` test workflow。今日 `node --test ...` 的 65 tests 是本机证据，不能外推不同 Node/OS。
- GitHub advisories API 空数组、Dependabot endpoint 404；零 npm runtime dependency 降低某类风险，但不证明 skill prompt、安全方法、Node runtime、installer 或 target execution 无风险。

#### 可复用经验

- 当审计输出引用本地 artifact 时，应优先在 terminal gate 中对 exact target 做 no-follow regular-file open、size/hash/owner read-back，而不是只校验相对路径字符串，因为 schema-valid reference 可以指向不存在对象；边界是 read-back 仍需绑定 source ref 与 producer identity。
- 当 Agent 安全审计存在 finder bias 时，应优先把 coverage unit、hunter、candidate verifier、final record verifier 分离，并让 parent 独占 canonical state，因为同一 Agent 自找自证容易把 checklist deviation 升成漏洞；边界是“fresh agent”不自动保证不同模型偏差或真实隔离。
- 当外部事实、sandbox 或 budget 不足时，应优先保留 `needs_validation/blocked/deferred/incomplete(exact reason)`，禁止用 severity、空 findings 或 prose clean 替代，因为不可观测不是负面证据；边界是 blocked backlog 仍需 owner、优先级与后续验证路径。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/evidence-artifact-closure-v0/` 实现一个不依赖上游代码的 Python checker：读取 synthetic ledger 后，从受信 output-root fd 逐层 no-follow 打开 `agents/<id>/artifacts/<file>`，要求 regular、link count 1、owner prefix 匹配、bounded size，并把 SHA-256 写入 terminal receipt。fixtures 覆盖 missing、symlink、FIFO、wrong owner、changed-size 与 valid regular file。只用临时目录，不审计真实项目、不运行目标代码。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 MIT；可抽象机制。安装器、目标代码、测试工具链与审计产物许可证需独立审查。
- **维护活跃度**：最近 commit 为 2026-09-14；前一批大改在 09-10，仓库较新且 validator contract 快速变化。无 release/tag，稳定版本边界弱。
- **安全风险**：full audit 要求 subagents、target builds/tests、浏览器/fuzzer；若 host 不能提供 OS sandbox，skill 明确应停在 needs_validation。prompt 规则不能创造 OS isolation。
- **证据完整性风险**：issue #21 已本机复现；当前 coverage PASS 不关闭 artifact existence。还需核 hash、producer/source revision、promotion race、retention 与 report→record correspondence。
- **覆盖/成本风险**：issue #20 的 benchmark 数字来自第三方单目标 n=3，今日未复现，不可泛化；它提出的 CVE external grounding、taxonomy gap、quick malformed-return recovery 值得作为 open questions。
- **不适用场景**：没有 subagent independence、没有 sandbox、预算不足以保留 critics/verifiers、需要 live production probing 的场景，不应称为 full audit completed。
- **验证局限**：今日只跑 validators tests 与 missing-artifact reproduction；未运行完整 6-phase audit、target sandbox、multi-agent independence 或真实 vulnerability discovery。

#### ⭐ Skill 升格判断

**需二次验证。** 完整 security-audit skill **暂不直接迁移**：它体量大、要求真实 subagent/sandbox，且 artifact closure 有已复现缺口。只提出 `evidence-artifact-closure` candidate；shared hub 已有 verification-first/governance/self-reflection，优先把“引用 artifact 必须 read-back”增量并入现有 contract，避免复制 20+ references 形成上下文税。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/evidence-artifact-closure-v0/`，只处理 synthetic ledger/output root，输出 machine-readable receipt。
2. GitHub-learning 审计：报告中的 test result/API/evidence path 应生成 evidence manifest；audit 先查文件存在/regular/size/hash，再打内容分，而不是只数关键词。
3. shared workflow：若 POC 通过，优先更新现有 verification-first 或 self-reflection skill 的 completion gate；新增字段 `artifact_state=verified|missing|changed|blocked`、`sha256`、`source_revision`。
4. shared governance：candidate 仍只写 inbox/runtime；不因 validator PASS 自动晋升 curated fact。promotion 必须再经去重、脱敏、来源与人工/总控审查。
5. Hermes/future adapter：contract 保持 agent-neutral；Hermes adapter 只负责解析本地 output root。OpenClaw 当前不存在，本次不调用、不写其 runtime/config。

## 经验沉淀

1. 当 moving ref、workspace 或 mutable config 会决定任务输入时，应优先在 run 创建和 resume admission 前封存 immutable revision 与 canonical input hash，因为执行中再发现漂移会留下错误 session/evidence；边界是 hash 不替代权限与 effect-time target revalidation。
2. 当 Agent 参与 grouping、ranking、routing 或摘要时，应优先先冻结 host-owned coverage denominator，并把 Agent 输出当可失败 optimization，因为模型漏项不能让对象从审计范围消失；边界是 fallback 要披露质量/成本退化。
3. 当结果以 ledger/schema/manifest 形式引用 artifact 时，应优先对 exact artifact 做 existence、regular-file、no-follow、size/hash 和 owner read-back，因为路径合法只证明字符串，不证明证据存在。
4. 当任务可能 partial、blocked、deferred、rejected 或 needs_validation 时，应优先使用 typed terminal + exact reason，并从 canonical state 生成 prose，因为 exit 0、空 findings、DONE tool call 或报告存在都不能证明完整成功。
5. 当 security/code-review workflow 引入 subagents 时，应优先分离 finder、verifier、final record owner 与 shared-state writer，因为独立角色能降低自证和并发污染；边界是角色名不同不等于 OS/模型/权限真正独立。
6. 当预算是硬边界时，应优先在 dispatch/admission 前做 reserve/check，并把 in-flight overrun 上界和未覆盖 items 写入 manifest，因为事后 ledger 只能记账不能限额。
7. 当仓库 README、assurance case、CI、本机测试和公开 issue 冲突时，应优先固定 commit 并并列保留各证据面的真实状态，因为任一单面绿色都不能覆盖另一面的失败或未知。
8. 当第三方 skill 通过 moving URL/installer 分发时，应优先 pin commit、dry-run inventory、验证 owner/conflict/uninstall 与 first-turn behavior，而不是因官方组织、Stars 或 MIT/Apache 许可直接安装。

## 明日继续

1. **最小动作 A**：创建 `runtime/hermes/github-learning-poc/evidence-artifact-closure-v0/`，先复现 missing/symlink/FIFO/wrong-owner/changed-size/valid-file 六个 fixtures，并输出 SHA-256 receipt。
2. **最小动作 B**：创建 `runtime/hermes/github-learning-poc/sealed-selection-coverage-v0/`，验证 moving ref、group omission、budget partial 与 manifest read-back。
3. **继续核验**：OpenCodeReview 固定 main check 的 `test` failure 根因；security-audit-skill issue #21 后续是否修复并加入 output-root artifact validation。均不在无人 cron 自动安装上游 skill/runtime。

## 候选反哺

### Candidate Facts

- [ ] topic: LLM grouping 必须位于 sealed coverage denominator 之后 | evidence: `alibaba/open-code-review@75d7bc9` 的 `registerCoverage`、`groupDiffs`、omission fallback 与本机 4,623-test 结果 | 建议: update existing verification/orchestrator candidate | 安全级别: low
- [ ] topic: schema-valid artifact reference 不等于 artifact 存在 | evidence: `cloudflare/security-audit-skill@c1c8a8c` 的 `validateChecks()`、issue #21、本机 `PASS: 1 coverage units valid` + `artifact_exists=no` | 建议: create candidate only | 安全级别: medium
- [ ] topic: mutable Git refs 应在 resume admission 前封存 | evidence: `internal/agent/identity.go` 的 `ResolveIdentity/resolveInputBeforeDiff` 与 fixed source tests | 建议: update existing path/verification fact candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: evidence-artifact-closure | 可复用场景: GitHub learning、reflection、security audit、knowledge projection completion | 是否建议 shared: yes-after-POC | 原因: 横切多 agent，但需先完成 no-follow/read-back/hash fixtures，并优先更新现有 verification skill
- [ ] 名称: sealed-input-selection-coverage-contract | 可复用场景: research orchestration、code review、batch audit、resume | 是否建议 shared: yes-after-POC | 原因: 与现有 verification/completion 能力高度相关，应增量合并而非新建重复大 skill

### Candidate Open Questions

- [ ] 问题: 当前 GitHub-learning audit 是否只验证报告文本关键词，而没有 evidence path/hash closure？ | reason: gap | priority: high
- [ ] 问题: OpenCodeReview main 的 `test` check 为什么 failure，而同 commit 本机 full Go tests 全绿？ | reason: conflict | priority: medium
- [ ] 问题: security-audit-skill 是否会为 issue #21 增加 trusted output-root 与 artifact existence/hash validation？ | reason: stale/gap | priority: high
- [ ] 问题: shared hub 现有 verification-first skill 是否已有可复用的 no-follow fd/read-back receipt，避免重复实现？ | reason: adaptation | priority: high

### 不应自动落地

- 不自动安装、运行或接入 OpenCodeReview/security-audit-skill，不执行 `npx skills add`，不连接真实 LLM/provider/MCP，不扫描用户仓库或生产系统。
- 不自动修改 Hermes/OpenClaw 的配置、模型、provider、auth、env、cron、skills；OpenClaw 当前不存在且本任务明确禁止调用。
- 不直接写 curated active fact；以上只进入 Hermes 二轮审计候选，需评分、证据、去重、脱敏与人工/总控审查。
- 不复制 NOASSERTION/GPL/未知依赖许可代码；不把 Apache-2.0/MIT 根许可外推到依赖、模型、数据、plugins、installer 或 release asset。
- 不把 README benchmark、issue #20 作者数字、CI badge、Stars、schema PASS、test green 或 assistant prose单独当作安全证明、完整覆盖、用户事实或生产授权。
