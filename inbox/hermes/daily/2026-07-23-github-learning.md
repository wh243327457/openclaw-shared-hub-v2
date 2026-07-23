# 2026-07-23 GitHub 热门项目学习日报（Hermes）

> 执行器：Hermes（本次未调用 OpenClaw）  
> 调研时间：2026-07-23 21:51–22:04 CST  
> 热门入口：`https://github.com/trending`（21:51 CST 真实抓取）  
> 元数据来源：GitHub REST API（`gh api repos/{owner}/{repo}`）；Stars 是查询时快照，不是永久值。  
> 深读代码固定到：`alibaba/open-code-review@cf3bf706e842a26b256a82d2d3a3c31de9bbf144`、`block/buzz@acfbb1bb6af54cb29cb152496ff43b8285dcb8cf`。  
> 本地验证边界：仓库已真实 shallow clone 并逐文件读取；当前 WSL 没有 `go`、`rustc`，所以 Go/Rust 测试未能本地执行，相关动态行为均标注为“源码核验，运行待核验”。

## 今日结论

今天的主线不是“再给 Agent 加更多自由度”，而是把**不可错的边界交给确定性工程**：OpenCodeReview 用文件筛选、并发隔离、行号重定位和结果过滤约束 LLM；Buzz 用租户绑定、签名事件、权限门和哈希链约束人类/Agent 共用的事件系统。对 Hermes/shared hub 最值得反哺的是“确定性外壳 + Agent 判断”和“证据与租户身份进入数据主键”，但两者都应先进入 runtime POC，不应直接改配置、cron 或 curated active fact。

## 项目速览

以下项目均来自今日抓取的 GitHub Trending 页面；Stars、License、Language 来自随后真实 GitHub API 查询（快照约 21:51–21:57 CST）。`NOASSERTION` 表示 API 当时没有可判定 SPDX License，不等于“允许任意使用”。

| 项目 | Stars | Language | License（API） | API pushed_at | 今日判断 |
|---|---:|---|---|---|---|
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 11,145 | Go | Apache-2.0 | 2026-07-23T13:48:21Z | **深读**：确定性流水线约束 LLM code review |
| [block/buzz](https://github.com/block/buzz) | 5,525 | Rust | Apache-2.0 | 2026-07-23T12:37:00Z | **深读**：签名事件、租户隔离与审计链的人机协作底座 |
| [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | 70,752 | TypeScript | NOASSERTION | 2026-07-23T13:12:40Z | 实时情报聚合面板；License 未判定，不复制源码 |
| [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | 32,864 | Python | MIT | 2026-04-13T12:38:49Z | 金融市场基础模型，热度高但更新距今较久 |
| [Pumpkin-MC/Pumpkin](https://github.com/Pumpkin-MC/Pumpkin) | 8,710 | Rust | GPL-3.0 | 2026-07-20T09:55:57Z | Rust Minecraft 服务端；GPL 边界需隔离评估 |
| [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | 1,309 | JavaScript | MIT | 2026-07-23T11:54:29Z | 人与 Agent 并行浏览器，项目较新 |
| [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | 26,412 | TypeScript | MIT | 2026-07-23T13:05:31Z | 多模型网关；provider/密钥面风险高，不自动接入 |
| [likec4/likec4](https://github.com/likec4/likec4) | 4,558 | TypeScript | MIT | 2026-07-23T13:00:01Z | 从代码维护架构图，适合后续评估 shared hub 可视化 |
| [Automattic/harper](https://github.com/Automattic/harper) | 11,917 | Rust | Apache-2.0 | 2026-07-23T10:42:01Z | 离线隐私优先语法检查，适合本地质量门候选 |

> 复核说明：深读项目在 21:57 CST 再次调用 API，得到上表 11,145 / 5,525 Stars；其他项目使用 21:51 后的首轮 API 快照。完整原始证据位于 `runtime/hermes/github-hot-project-learning/evidence/2026-07-23/`。

## 深读项目

### 项目 1：alibaba/open-code-review

- 仓库：[https://github.com/alibaba/open-code-review](https://github.com/alibaba/open-code-review)
- 固定提交：[`cf3bf706e842a26b256a82d2d3a3c31de9bbf144`](https://github.com/alibaba/open-code-review/commit/cf3bf706e842a26b256a82d2d3a3c31de9bbf144)，提交时间 2026-07-23T13:45:14Z
- API 快照：Stars **11,145**；Forks **777**；Language **Go**；License **Apache-2.0**；open issues **38**；updated_at 2026-07-23T13:55:32Z
- 最新 release：[`v1.7.15`](https://github.com/alibaba/open-code-review/releases/tag/v1.7.15)，2026-07-22T13:00:44Z
- 一句话判断：**值得学的不是“让 LLM 看 diff”，而是把选择、预算、并发、定位、过滤和持久化做成确定性控制面。**

#### 解决的问题：替代了什么旧做法

README 明确指出通用 coding agent + 自然语言 Skill 容易出现大变更覆盖不全、评论位置漂移、轻微提示词变化导致质量波动。该项目替代的是“一段 prompt + 一个通用 Agent 自己决定看哪些文件”的软约束做法：Git 负责形成 diff，过滤器决定可审文件，模板规则按路径匹配，每个文件隔离子任务，LLM 仅在动态判断与上下文检索上发挥作用，评论再经过行号解析与 review filter。

README 宣称其 benchmark 在同模型下拥有更高 Precision/F1、约 1/9 token，但这是项目方 benchmark 结论；本次没有复现实验，**独立效果待核验**。

#### 架构 / 实现与数据流

从 `pages/src/content/docs/en/architecture.md`、`internal/agent/agent.go` 与 `internal/llmloop/loop.go` 交叉核验，主数据流为：

1. CLI 启动并解析 provider/model/template/tools/rules。
2. `internal/diff` 通过 workspace / commit / range 三种模式生成 `[]model.Diff`；未跟踪文件作为整文件新增。
3. 过滤层丢弃 binary、用户排除、非支持扩展与默认测试路径；用户显式 include 可越过后两门。
4. 每个文件一个并发子任务；大 diff 可先做无工具的 plan，再进入带工具的 LLM loop。
5. `llmloop.Runner` 最多运行配置的工具轮次，要求显式 `task_done`；连续三轮没有有效工具结果会停止。
6. `code_comment` 强制覆盖为当前文件路径，先做确定性行号匹配，失败时可调用 re-location；异步 worker 以文件 key 隔离等待。
7. 文件主循环结束后，`REVIEW_FILTER_TASK` 删除可证明错误的评论；顶层再做第二遍行号解析。
8. 会话按 JSONL 追加到本地 session 目录，便于复盘而不引入数据库。

#### Repo tree 摘要

```text
open-code-review/
├── cmd/opencodereview/   # CLI 分发：review / scan / config / delegate / viewer
├── internal/
│   ├── agent/            # diff review 编排、按文件并发、plan/filter
│   ├── scan/             # 全文件 scan、batch、预算、去重、项目摘要
│   ├── llmloop/          # 共享工具循环、token 统计、三段式压缩、worker pool
│   ├── diff/             # Git diff、hunk 解析、行号定位/重定位
│   ├── llm/              # OpenAI/Anthropic 协议、provider/endpoint 解析
│   ├── tool/             # code_search/file_read/code_comment/task_done 等
│   ├── config/           # prompt template、系统 rules、文件 allowlist
│   ├── session/          # append-only JSONL 会话记录与 resume
│   ├── mcp/              # 外部 MCP 客户端扩展
│   ├── telemetry/        # OTel 指标与 spans
│   └── viewer/           # 本地 session 浏览器
├── skills/               # Agent skill 入口
├── plugins/              # Claude Code/Codex/Cursor 插件包装
├── extensions/vscode/    # VS Code 集成
├── npm/ + bin/           # 六个平台 native 包及 npm launcher
└── pages/                # 文档站与架构文档
```

#### 关键源码文件

| 文件 | 用途 | 本次核验到的关键内容 |
|---|---|---|
| `internal/agent/agent.go` | diff review 总编排 | 加载全部 diff 后注入只读 DiffMap；按文件 semaphore 并发；plan/main/filter 分段；panic 与单文件失败隔离 |
| `internal/llmloop/loop.go` | 通用 LLM 工具循环 | `RunPerFile` 要求工具调用；最多 3 次空结果；token 聚合；当前路径覆盖；60%/80% 压缩门 |
| `internal/llmloop/pool.go` | 评论后处理 worker pool | `SubmitFor/AwaitKey` 按文件 drain，避免全局 WaitGroup 与其他文件提交并发竞态 |
| `internal/diff/resolver.go` | 评论行号确定性解析 | 优先匹配 hunk 新侧，再旧侧，最后扫描完整新文件；忽略空白行并返回绝对行号 |
| `internal/tool/comment_collector.go` | 并发安全结果存储 | mutex 保护，支持按路径读取、snapshot/since、batch dedup 后替换 |
| `internal/scan/agent.go` | 全仓扫描 | 文件枚举、过滤、按语言/策略 batch、per-file token 预算前瞻、best-effort 去重与项目摘要 |
| `pages/src/content/docs/en/architecture.md` | 官方实现说明 | 与源码交叉验证 pipeline、过滤门、压缩、session 与已知边界 |

#### ⭐ 源码精读 1：`Runner.RunPerFile` 把“结束”变成协议而不是猜测

源码签名与关键控制流（`internal/llmloop/loop.go:143-268`）：

```go
func (r *Runner) RunPerFile(
    ctx context.Context,
    messages []llm.Message,
    newPath string,
) (bool, error) {
    toolReqCount := r.deps.Template.MaxToolRequestTimes
    const maxConsecutiveEmptyRounds = 3
    consecutiveEmptyRounds := 0
    // ...
    for toolReqCount > 0 {
        // 调 LLM、解析 tool calls
        if len(calls) == 0 {
            messages = append(messages, llm.NewTextMessage(
                "user",
                "You did not successfully call any tools. Please try again or use task_done if finished.",
            ))
            continue
        }
        // ... task_done => return true
    }
    return false, nil
}
```

逻辑摘要：函数返回的 `bool` 只在模型明确调用 `task_done` 时为真；“模型输出了一段自然语言”不等于完成。没有工具调用时追加纠偏消息；有调用但没有有效结果时累计空轮次，三次后停止。这使上层能区分“显式完成”和“因预算/异常退出”。

#### ⭐ 源码精读 2：评论目标路径由运行时覆盖

`internal/llmloop/loop.go:325-329`：

```go
// Always inject the current file path for code_comment.
// The model sometimes hallucinates a path, so we override it.
if t == tool.CodeComment && newPath != "" {
    args["path"] = newPath
}
```

逻辑摘要：模型提供的 `path` 不作为权威数据，运行时以当前审查单元 `newPath` 覆盖。这是典型“Agent 提建议、控制面绑定作用域”的实现，可防止评论被写到幻觉文件或跨文件目标。

#### ⭐ 源码精读 3：行号定位先确定性匹配，再容错回退

`internal/diff/resolver.go:57-70`：

```go
func ResolveComment(cm *model.LlmComment, d *model.Diff) bool {
    if cm.StartLine > 0 || cm.EndLine > 0 {
        return true
    }
    if cm.ExistingCode == "" {
        return false
    }
    if resolveFromHunk(d, cm) {
        return true
    }
    return resolveFromFileContent(d, cm)
}
```

逻辑摘要：评论携带 `existing_code`，系统不信任模型给出的行号；先在 diff hunk 的新/旧侧做连续归一化匹配，再扫描新文件。只有确定性路径失败后，调用方才可能启用 LLM re-location。这比要求模型直接返回行号更稳。

#### ⭐ 源码精读 4：按文件等待异步评论，避免全局并发竞态

`internal/llmloop/pool.go:65-85,132-147`：

```go
func (p *CommentWorkerPool) SubmitFor(
    key string,
    f func() ([]model.LlmComment, error),
) {
    // 为 key 建立独立 WaitGroup 后提交
}

func (p *CommentWorkerPool) AwaitKey(key string) {
    p.keysMu.Lock()
    kwg := p.keys[key]
    p.keysMu.Unlock()
    if kwg != nil {
        kwg.Wait()
    }
}
```

逻辑摘要：文件 A 的 review filter 只等待 A 的评论后处理，不调用 pool-wide `Await`，因此不会与文件 B 仍在发生的 `Submit` 形成 WaitGroup 误用。最新 `v1.7.15` release notes 也明确列出 “drain per-file comment work without racing pool submissions (#449)” 修复，源码与 release 证据一致。

#### 依赖分析与供应链风险

`go.mod` 指定 Go **1.25.5**，核心直接依赖包括：

- `github.com/openai/openai-go/v3 v3.41.0`、`github.com/anthropics/anthropic-sdk-go v1.55.1`：双 LLM 协议面；上游 API 行为与日志策略会影响代码机密性。
- `github.com/modelcontextprotocol/go-sdk v1.6.1`：MCP 扩展扩大工具执行边界，必须显式 allowlist。
- `go.opentelemetry.io/otel v1.44.0` 及 exporter：可观测性强，但 endpoint/属性配置错误可能外发元数据。
- `github.com/pkoukk/tiktoken-go v0.1.8`：本地 token 估算；模型 tokenizer 差异可能导致预算误差。
- Bubble Tea / Bubbles / Lip Gloss：交互式配置面，依赖数量随之增加。
- npm meta package 通过六个 optional native platform packages 分发二进制；属于“JS launcher + native artifact”供应链面。

积极信号：`SECURITY.md` 声明 release binaries/checksums 使用 GitHub Artifact Attestations，tag 使用签名，并提供 `gh attestation verify`；`v1.7.15` 修复了 VS Code 依赖中的 5 个 high-severity 漏洞。边界：本次没有下载 release artifact，也没有实际执行 attestation verify，**具体 artifact provenance 待核验**。

#### 可复用经验

- **当 LLM 输出必须绑定到具体文件/资源时，应优先由控制面注入权威作用域，而不是相信模型回传的 path，因为 prompt 约束不能消除幻觉目标；边界是控制面自身必须先正确解析工作单元。**
- **当并发子任务各有异步后处理时，应优先按任务 key 建立局部 drain/barrier，而不是在热路径调用全局 Wait，因为全局等待既增加耦合又可能违反并发原语契约；边界是同 key 的提交必须在等待前完成。**
- **当 Agent 要判断“任务完成”时，应优先使用显式终止工具或结构化状态，而不是从自然语言推断完成，因为预算耗尽、空工具结果与真正完成是不同状态；边界是上层仍需处理未完成结果。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/deterministic-review-envelope/` 做一个**不调用外部 LLM**的最小 POC：

1. 对一个测试 Git 仓库运行 `git diff --name-only --diff-filter=ACMR`。
2. 用可配置 include/exclude 形成确定性 review manifest（文件、commit、diff hash）。
3. 模拟 Agent 返回两条 comment，其中一条故意给错 path。
4. wrapper 强制把 path 绑定到当前 manifest item，并用 `existing_code` 在 diff 中定位行号。
5. 输出 `completed / incomplete / blocked / failed` 四状态和 JSON 证据。

成功标准：错 path 被覆盖；不存在的 snippet 标为 unanchored 而非伪造行号；同一输入重复运行 manifest hash 一致。此实验不改 Hermes 配置、provider、cron 或 secret。

#### 风险边界

- **License**：Apache-2.0，允许改编和再分发但要保留版权/NOTICE 等义务；不能把项目自身的 benchmark 宣称当作本地已验证事实。
- **安全风险**：审查私有代码时会把 diff/上下文发送到配置的 LLM endpoint；自定义 MCP 工具进一步扩大读取与执行面。代码、prompt、session JSONL 与 telemetry 都需按敏感数据处理。
- **局限/不适用**：默认按文件隔离，跨文件推理依赖工具检索而不是共享上下文；默认过滤测试路径，可能漏掉测试回归；Precision 优先意味着 Recall 可能较低；极大文件受 80% token 门过滤。
- **维护活跃度**：API pushed_at 为当天，最近三版 v1.7.13–v1.7.15 连续三天发布；活跃度高也意味着接口和内部架构变化快。
- **已知 issue**：[#461](https://github.com/alibaba/open-code-review/issues/461) 请求允许 CLI 覆盖 `REVIEW_FILTER_TASK` timeout，本地/慢模型高并发下可能超时。
- **验证缺口**：WSL 没有 `go`，本地 `go test` 返回 `go: command not found`；上述行为来自固定提交源码、docs、release 与 issue 的交叉核验，运行结果待有工具链环境后复验。

#### Skill 升格判断

**结论：需二次验证。**

可抽象的是“deterministic review envelope”工作流，不是直接复制该仓库 `skills/`。它跨 Hermes / future agent / 其他 workspace 都有价值，但需要先验证：不同语言 diff、rename/binary、大文件、并发 barrier、敏感代码不外发以及四状态输出。验证通过后才考虑在 `capabilities/skills/autonomous-learning/` 新建共享 Skill，并同步更新 `capabilities/manifests/shared-skills.yaml`；当前日报只提出 candidate，不自动升格。

#### Hermes / shared hub 落地路径

1. **Runtime POC**：`runtime/hermes/github-learning-poc/deterministic-review-envelope/`，只放 manifest、测试 fixture 与临时输出。
2. **Hermes 审计接口**：候选脚本接收 `{repo_root, base, head, include, exclude}`，输出 `{items, evidence_hash, states, comments}`；不得读取 repo_root 外文件。
3. **共享契约候选**：若 POC 通过，Skill 的 `SKILL.md` 只保留触发条件、流程、四状态协议、验证命令与 pitfalls；raw diff/session 仍留 runtime，不进入 Skill references。
4. **治理**：稳定事实先作为 Candidate Fact 送审；不直接写 `curated/memory/`，不自动改 Hermes provider/model/cron。
5. **跨 Agent 使用**：未来其他 agent 只经 shared skill/manifest 读取同一契约；本任务不调用或修改 OpenClaw 运行时。

---

### 项目 2：block/buzz

- 仓库：[https://github.com/block/buzz](https://github.com/block/buzz)
- 固定提交：[`acfbb1bb6af54cb29cb152496ff43b8285dcb8cf`](https://github.com/block/buzz/commit/acfbb1bb6af54cb29cb152496ff43b8285dcb8cf)，提交时间 2026-07-22T23:16:56Z
- API 快照：Stars **5,525**；Forks **426**；Language **Rust**；License **Apache-2.0**；open issues **408**；updated_at 2026-07-23T13:57:54Z
- 最新 release：[`v0.4.23`](https://github.com/block/buzz/releases/tag/v0.4.23)，2026-07-22T23:17:33Z
- 一句话判断：**Buzz 值得学的是把人、Agent、workflow、git 都表达成同一类签名事件，同时让 host-derived community、权限门和审计链成为不可绕过的控制边界。**

#### 解决的问题：替代了什么旧做法

Buzz 试图替代“聊天、机器人、CI、代码托管、搜索、Agent 各有身份/日志/权限，再用 webhook 粘起来”的碎片化方式。其统一抽象是 Nostr event：消息、reaction、workflow、git、Agent job 都是签名事件，relay 是单一真相源；客户端、人和 Agent 共用协议，但各自持有身份和审计轨迹。

这不意味着“所有能力已完成”。README 把功能分为 works today / being wired up / pending code；本次重点分析可迁移的**事件入口、租户隔离和审计机制**，不评价产品体验。

#### 架构 / 实现与数据流

从 `README.md`、`ARCHITECTURE.md`、`crates/buzz-relay/src/handlers/event.rs`、`crates/buzz-audit/` 与 release/issue 交叉核验：

1. 请求 host 首先解析为 `TenantContext`；未知 host fail closed。community 是服务端来源，不由事件 tag 覆盖。
2. WebSocket 连接先做 NIP-42 challenge；HTTP bridge 用 NIP-98。认证后才能进入 EVENT/REQ。
3. `handle_event` 读取连接身份，检查 event pubkey 与认证身份（gift wrap 例外），拒绝 AUTH event 经普通 EVENT 提交。
4. ephemeral 事件验证签名后走 Redis/fan-out，但不入 Postgres；persistent 事件委托共享 ingest seam。
5. relay 编排 db、pubsub、search、audit、workflow；服务 crate 彼此隔离，跨子系统协调只在 relay。
6. audit service 为每个 community 建独立 SHA-256 链，使用 Postgres advisory lock 串行化该 community 的 append；不同 community 不互相阻塞。
7. workflow 的 cache key、DB 查询、run creation 都携带 `community_id`；执行事件种类会被排除以避免递归触发。
8. 最近 `v0.4.23` 加入 per `(agent, community)` harness；但当天 issue #2515 报告同名 Agent 在多 community 的 membership/mention/profile 路径仍可能串扰，说明“服务端边界正确”不代表所有客户端缓存/解析路径都正确。

#### Repo tree 摘要

```text
buzz/
├── crates/
│   ├── buzz-core/          # 零 I/O 类型、事件验证、kind、tenant/network 工具
│   ├── buzz-relay/         # Axum WS/HTTP 入口与跨子系统编排
│   ├── buzz-db/            # Postgres event/channel/workflow 等数据层
│   ├── buzz-auth/          # NIP-42/NIP-98、scope、replay/rate-limit 接口
│   ├── buzz-pubsub/        # Redis fan-out、presence、typing
│   ├── buzz-search/        # Postgres FTS 候选检索
│   ├── buzz-audit/         # per-community append-only hash chain
│   ├── buzz-workflow/      # YAML workflow、trigger/action/scheduler
│   ├── buzz-acp/           # relay @mention ↔ Agent ACP/JSON-RPC harness
│   ├── buzz-cli/           # 面向 Agent 的 JSON I/O CLI
│   ├── buzz-dev-mcp/       # shell/file MCP 工具
│   └── ...                 # media/sdk/admin/pairing/mesh/test 等
├── desktop/                # Tauri + React 桌面端
├── web/                    # 浏览器端 / repo browser
├── mobile/                 # Flutter 客户端
├── migrations/ + schema/   # Postgres schema 与迁移
├── deploy/                 # 部署资产
├── docs/                   # 协议、运维、安全文档
├── examples/               # 示例 bot
└── Cargo.toml              # 28 个 workspace members 与统一依赖
```

#### 关键源码文件

| 文件 | 用途 | 本次核验到的关键内容 |
|---|---|---|
| `crates/buzz-relay/src/handlers/event.rs` | WebSocket EVENT 边界 | 认证、pubkey match、AUTH event 拒绝、ephemeral 分流、persistent ingest、错误脱敏 |
| `crates/buzz-relay/src/router.rs` | HTTP/WS 路由与 body limit | WS/NIP-11、HTTP bridge、media、git、workflow hook、health；普通 API 1 MiB body 限制 |
| `crates/buzz-core/src/tenant.rs` | 租户上下文 | host 归一化、relay authority、`TenantContext` 类型化来源 |
| `crates/buzz-audit/src/service.rs` | 审计链 append/verify | per-community advisory lock、transaction append、按 community 读取与校验 |
| `crates/buzz-audit/src/hash.rs` | 稳定 hash 定义 | community_id 领先、固定字段序、presence tag、canonical JSON、prev/genesis hash |
| `crates/buzz-workflow/src/lib.rs` | event/cron workflow 编排 | cache 与 run 全程 community-scoped；执行事件防循环；durable schedule claim |
| `Cargo.toml` | workspace/依赖边界 | Axum/Tokio/SQLx/Redis/Nostr/OTel；git patch pin 与 RC 依赖 |
| `SECURITY.md` | 安全边界说明 | hash chain 是 tamper-evident 而非 tamper-resistant；TLS 由部署层终止；keyring fallback |

#### ⭐ 源码精读 1：EVENT 入口先绑定认证身份，再分流

`crates/buzz-relay/src/handlers/event.rs:585-705` 的关键签名与门控：

```rust
pub async fn handle_event(
    event: Event,
    conn: Arc<ConnectionState>,
    state: Arc<AppState>,
) {
    // ... read AuthState::Authenticated(ctx)
    let is_gift_wrap = kind_u32 == KIND_GIFT_WRAP;
    if event.pubkey != auth_pubkey && !is_gift_wrap {
        // reject: event identity != authenticated identity
        return;
    }
    if kind_u32 == buzz_core::kind::KIND_AUTH {
        // AUTH events cannot enter the normal EVENT pipeline
        return;
    }
    // ephemeral -> dedicated path; persistent -> ingest_event(...)
}
```

逻辑摘要：签名验证之前仍先做已认证连接的身份匹配和 event kind 分流，避免普通 client 借 event 字段冒充其他主体；内部错误返回 WS 前会被脱敏。gift wrap 是协议特例，不可把例外扩张成通用代理权限。

#### ⭐ 源码精读 2：审计 append 用 community 级锁，而非全局锁

`crates/buzz-audit/src/service.rs:38-70`：

```rust
pub async fn log(&self, entry: NewAuditEntry) -> Result<AuditEntry, AuditError> {
    let mut conn = self.pool.acquire().await?;
    let lock_key = format!("{AUDIT_LOCK_NAMESPACE}{}", entry.community_id);
    sqlx::query("SELECT pg_advisory_lock(hashtextextended($1, 0))")
        .bind(&lock_key)
        .execute(&mut *conn)
        .await?;

    let result = AssertUnwindSafe(self.log_inner(&mut conn, entry))
        .catch_unwind()
        .await;
    // release advisory lock on success/error/panic path
    // ...
}
```

逻辑摘要：每个 community 的链必须单写者排序，但不同 community 不应互相串行，因此 lock key 绑定 community。`catch_unwind` 保证 panic 时先尝试释放 session-level advisory lock，再恢复 unwind，避免连接回池后携带锁。

#### ⭐ 源码精读 3：hash 把租户身份与“字段是否存在”都编码进去

`crates/buzz-audit/src/hash.rs:19-45`：

```rust
pub fn compute_hash(entry: &AuditEntry) -> Result<[u8; 32], AuditError> {
    let mut hasher = Sha256::new();
    hasher.update(entry.community_id.as_bytes());
    hasher.update(entry.seq.to_be_bytes());
    hasher.update(entry.created_at.to_rfc3339().as_bytes());
    hasher.update(entry.action.as_str().as_bytes());
    match &entry.actor_pubkey {
        Some(pk) => { hasher.update([1u8]); hasher.update(pk); }
        None => hasher.update([0u8]),
    }
    // object_id + canonical detail + prev_hash / GENESIS_HASH
    Ok(hasher.finalize().into())
}
```

逻辑摘要：`community_id` 首字段使同一逻辑记录不能直接搬到另一个租户链；`Some(empty)` 与 `None` 通过 presence tag 区分；JSON object key 用 BTreeMap 排序后递归序列化，确保跨进程重算稳定。

#### ⭐ 源码精读 4：workflow trigger 全程携带 community

`crates/buzz-workflow/src/lib.rs:276-378`：

```rust
pub async fn on_event(
    self: &Arc<Self>,
    community_id: CommunityId,
    event: &buzz_core::StoredEvent,
) -> Result<(), WorkflowError> {
    let Some(channel_id) = event.channel_id else { return Ok(()); };
    if is_workflow_execution_kind(event_kind_u32(&event.event)) {
        return Ok(());
    }
    let cache_key = (community_id, channel_id);
    // DB lookup and create_workflow_run both receive community_id
    // spawned execute_run also receives community_id
    Ok(())
}
```

逻辑摘要：channel UUID 本身不足以作为隔离键；cache、查询、run 和异步执行均携带 community。执行类 event 被提前排除，避免 workflow 自己产生 event 后无限触发自己。

#### 依赖分析与供应链风险

workspace `Cargo.toml` 显示 28 个 member，核心依赖包括：

- `tokio 1`、`axum 0.8`、`tower/tower-http`：异步网络入口与中间件。
- `sqlx 0.9`（Postgres）、`redis 1.0` / `deadpool-redis`：持久层、fan-out、presence。
- `nostr 0.44`：签名 event 与 NIP 支持，是身份/协议核心依赖。
- `opentelemetry 0.32`、Prometheus metrics：可观测面，需限制 tenant/高基数标签。
- `reqwest 0.13`：workflow webhook；源码还需 SSRF、redirect 与 response-size 门共同约束。
- `rmcp 1.1.0`：Agent MCP 工具面。
- `iroh 1.0.0-rc.0`：mesh transport 使用 RC 版本，稳定性与升级风险高于稳定版。
- `[patch.crates-io] aws-creds` 固定到 git repo 的具体 rev `c9fce...`：虽然 pin 到 commit 好于浮动 branch，但偏离 crates.io release，需单独审查与更新治理。
- `buzz-relay` dev-dependencies 还从 git tag 引入 `mesh-llm`；虽为 dev 依赖，CI/开发供应链仍需关注。
- `Cargo.lock`、`pnpm-lock.yaml` 均存在；前端 workspace 使用 `pnpm@11.4.0`。

积极信号：`SECURITY.md` 声明 CI 运行 `cargo audit`、全 crate 禁止 unsafe；边界是本次未读取 CI 实际运行日志，也没有本地 cargo 工具链，**具体提交的构建与 audit 结果待核验**。

#### 可复用经验

- **当同一资源 ID 可能在多个 workspace/tenant 重复时，应优先把 tenant identity 放进 cache key、数据库查询、审计 hash 和异步任务参数，而不是只在 API 入口检查一次，因为后续任一层丢失 tenant 都会重新引入串扰；边界是客户端本地缓存也必须遵守同一复合键。**
- **当需要可审计但又不能引入密钥管理复杂度时，应优先使用 canonical serialization + hash chain 做 tamper-evidence，并明确它不能抵抗拥有数据库写权限的攻击者；边界是高保证审计仍需外部锚定或签名。**
- **当事件会触发自动化并由自动化继续产生事件时，应优先用明确 kind/origin 标记切断递归触发，而不是依赖 prompt 要求 Agent 不自触发；边界是新增 kind 时必须同步维护排除规则。**

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/tenant-bound-evidence/` 做纯 Python、无网络 POC：

1. 定义事件 `{agent, pipeline, date, action, object_id, detail, prev_hash}`。
2. canonical JSON 使用排序 key；hash 输入先加入 `agent` 与 `pipeline` 复合 scope。
3. 为 `hermes/github-learning` 与 `future-agent/github-learning` 生成相同 payload，验证 hash 不同。
4. 修改链中间一条 detail，验证后续校验失败。
5. 模拟同名 agent 的两条记录，验证查询必须使用 immutable agent id + scope，不能只按 display name。

成功标准：跨 scope replay 失败；中间篡改可检出；同名不冲突；产物只写 runtime。实验不启服务、不改 auth/env/cron。

#### 风险边界

- **License**：Apache-2.0；可参考机制，但复制代码仍需遵守 NOTICE/版权要求。项目名、协议与完整产品代码不应直接并入 shared skill。
- **安全风险**：relay 暴露 WS、HTTP bridge、media、git、webhook、Agent MCP 等广攻击面；TLS 依赖反向代理/部署层。Agent 私钥虽优先 OS keyring，headless fallback 是 0600 文件，环境变量又有最高优先级。
- **审计局限**：`SECURITY.md` 明确 hash chain 只是 tamper-evident，不是 tamper-resistant；DB 写权限攻击者可重算整条链。当前 event handler 代码还显示 audit channel 关闭时会记录 “entry lost”，所以不能把业务 event 成功等同于审计必达。
- **租户局限**：当天 open issue [#2515](https://github.com/block/buzz/issues/2515) 报告同名 Agent 的 membership/mention/profile 在多 community 场景串扰；release v0.4.23 虽按 `(agent, community)` 启动 harness，客户端与缓存路径仍有缺口。
- **维护活跃度**：当天 pushed，v0.4.21–v0.4.23 三天连续发布；活跃但仍是 pre-1.0，`SECURITY.md` 只对 main 积极支持，历史版本 best effort。
- **不适用场景**：单机脚本/简单 cron 不需要整套 Nostr + Postgres + Redis + S3；对 shared hub 而言应迁移“作用域键/事件 envelope/审计链”机制，不应引入整个 Buzz 平台。
- **验证缺口**：WSL 没有 `rustc`，本地 cargo test 返回 `rustc: command not found`；架构文档可能滞后于高速迭代，关键结论因此以固定提交源码优先，运行行为待核验。

#### Skill 升格判断

**结论：暂不沉淀（完整 Buzz 能力）；其中“tenant-bound evidence envelope”需二次验证。**

Buzz 是产品级平台，不适合作为 shared skill 搬运。可复用的是窄机制：复合 scope key、canonical evidence hash、明确的 event origin/loop guard。先做 runtime POC，并用同名 agent、跨 profile、链篡改、并发 append 等 fixture 验证；没有 POC 与治理评审前不创建 shared skill。

#### Hermes / shared hub 落地路径

1. **证据 envelope POC**：`runtime/hermes/github-learning-poc/tenant-bound-evidence/`。
2. **状态键**：候选将当前学习闭环记录从隐含“日期”提升为 `{runner, pipeline, date, run_id}`；所有 runtime index/cache 使用完整复合键。
3. **审计证据**：候选新增 `runtime/hermes/github-hot-project-learning/audit-evidence.jsonl`，每条含 source URL、commit、artifact hash、previous hash；这是 runtime 证据，不是 curated truth。
4. **治理入口**：通过 POC 后只提出 Candidate Fact；由 `docs/shared-governance-standard.md` 评分、去重、脱敏和审查后再决定是否进入 `curated/memory/facts/`。
5. **共享 Skill 候选**：若多个 agent 都需要同一证据协议，再建立 `capabilities/skills/foundation/tenant-bound-evidence/` 并更新 manifest；当前不自动创建。
6. **运行边界**：不调用 OpenClaw、不改 Hermes/OpenClaw 配置、模型、provider、auth、env、cron，不写任何 secret。

## 经验沉淀

1. **当任务包含“不可错”的选择、作用域、预算、定位或终止条件时，应优先把它们实现为确定性代码和结构化协议，再让 LLM 处理模糊判断，因为语言约束不能替代控制面；边界是确定性规则也要有版本与测试。**
2. **当并发 Agent/worker 需要收敛结果时，应优先使用按任务 key 的局部 barrier 和隔离 collector，而不是一个全局等待点，因为后者既拖慢无关任务又容易造成并发竞态；边界是 key 本身必须包含 tenant/run scope。**
3. **当系统支持多 agent、多 workspace 或多 tenant 时，应优先用 immutable id + scope 作为所有 cache/query/event 的复合身份，而不是 display name 或单一资源 UUID，因为名称会重名、缓存会跨上下文残留；边界是 UI 也要显示并持久化确切选择。**
4. **当需要长期证据链时，应优先 canonicalize 后再 hash，并把 scope 与字段 presence 编入 hash，因为“同值不同语义”和跨 tenant replay 都会破坏证据可信度；边界是无密钥 hash 链只能检出篡改，不能阻止重算。**
5. **当读取热门项目结论时，应优先固定 commit 并交叉读取 README/docs/release/issues/源码，而不是只看 Trending 和 README，因为高活跃仓库的文档、release 与 main 可能快速分叉；边界是本地缺工具链时必须明确运行待核验。**

## 风险边界（跨项目）

- 不自动安装或执行热门项目，不自动接入 provider/MCP，不写入任何 API key。
- 不把 GitHub Stars 当质量评分；Stars 只记录查询快照。
- `NOASSERTION` 项目不复制源码；GPL 项目在没有隔离/合规评审前不进入 shared code。
- 不直接写 curated active fact；本报告的“候选反哺”只是二轮治理输入。
- 不把项目方 benchmark、README 的“生产验证”或安全声明改写成本地已复现实验。
- 本机缺 Go/Rust 工具链，因此没有伪造 test pass；源码结论有固定 commit 证据，动态性能、兼容性和构建状态仍待核验。

## Skill 升格总判断

- `alibaba/open-code-review` → **需二次验证**：候选机制为 deterministic review envelope；先 runtime POC，再决定 shared skill。
- `block/buzz` → **暂不沉淀完整项目**：窄机制 tenant-bound evidence envelope **需二次验证**。
- 今日不直接创建/修改 `capabilities/skills/`，原因是尚未完成跨语言、跨 agent、并发与安全 fixture 验证；避免把一次性研究误升格为 class-level 能力。

## 明日继续

1. 最小动作：为 OpenCodeReview POC 写 4 个 fixture（wrong path、rename、binary、missing snippet），只验证确定性 manifest/定位与四状态，不调用 LLM。
2. 为 Buzz 机制写 3 个 fixture（same display name/different immutable id、same object/different scope、middle-chain tamper）。
3. 在具备 Go/Rust 工具链的隔离环境分别运行：
   - `go test ./internal/diff ./internal/llmloop ./internal/agent`
   - `cargo test -p buzz-audit hash::tests --lib`
4. 复核 GitHub Actions/check-runs 与 artifact attestation；如果无法验证，继续保留“待核验”。
5. 根据 POC 结果决定 candidate 是 create、update 现有 verification-first fact，还是 retire。

## 候选反哺

### Candidate Facts

- [ ] topic: deterministic-control-plane-around-llm-review | evidence: `alibaba/open-code-review@cf3bf706` 的 `internal/agent/agent.go`、`internal/llmloop/loop.go`、`internal/diff/resolver.go` 与 v1.7.15 release | 建议: create（POC 通过后） | 安全级别: medium
- [ ] topic: tenant-identity-must-propagate-through-cache-db-async-and-hash | evidence: `block/buzz@acfbb1bb` 的 `tenant.rs`、`buzz-audit/service.rs`、`hash.rs`、`buzz-workflow/lib.rs`，以及反例 issue #2515 | 建议: create 或 update 现有多 agent 编排事实（治理去重后） | 安全级别: medium
- [ ] topic: hash-chain-is-tamper-evident-not-tamper-resistant | evidence: Buzz `SECURITY.md:67-74` + `buzz-audit/src/hash.rs` | 建议: create（若现有 facts 无重复） | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: deterministic-review-envelope | 可复用场景: Hermes/future agent 的代码审查与学习报告证据绑定 | 是否建议 shared: yes（仅在 fixture POC 通过后） | 原因: 作用域注入、显式完成、行号确定性解析是跨 Agent 稳定契约
- [ ] 名称: tenant-bound-evidence-envelope | 可复用场景: 多 agent runtime 证据、audit JSONL、候选晋升链 | 是否建议 shared: yes（需二次验证） | 原因: 避免同名/同日期/同资源跨 scope 冲突，并使证据可重算
- [ ] 名称: block-buzz-platform | 可复用场景: 完整协作平台 | 是否建议 shared: no | 原因: 过重、产品特定、运行依赖多，不应把平台当 Skill

### Candidate Open Questions

- [ ] 问题: OpenCodeReview 默认排除测试文件在不同仓库是否会造成不可接受的 Recall 损失？ | reason: adaptation | priority: high
- [ ] 问题: `REVIEW_FILTER_TASK` 是提升 precision 还是会误删真实发现；如何构造本地 golden set？ | reason: gap | priority: high
- [ ] 问题: shared hub 的证据链应只做本地 tamper-evidence，还是需要外部签名/锚定？ | reason: adaptation | priority: medium
- [ ] 问题: Buzz issue #2515 的根因在 Desktop cache、membership reconciliation 还是 mention resolver？ | reason: gap | priority: medium
- [ ] 问题: 当前 orchestrator status 是否需要从单一日期状态升级为 `{runner,pipeline,date,run_id}`？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动改 Hermes/OpenClaw 配置、模型、provider、auth、env、cron 或 secret。
- 不直接写 `curated/memory/facts/` 或更新 active project 状态。
- 不复制 License 未判定项目源码，不把 GPL 代码混入 shared capability。
- 不启动 Buzz relay，不连接任何 OpenClaw 运行时，不安装 OCR 的 npm/native binary。
- 不从 README benchmark 或 assistant 总结生成“已本地验证”的事实。

## 证据索引

- Trending 原页快照：`runtime/hermes/github-hot-project-learning/evidence/2026-07-23/trending.html`
- 全部候选 API 快照：`runtime/hermes/github-hot-project-learning/evidence/2026-07-23/repos.jsonl`
- 深读 repo API：
  - `runtime/hermes/github-hot-project-learning/evidence/2026-07-23/api/alibaba-open-code-review/`
  - `runtime/hermes/github-hot-project-learning/evidence/2026-07-23/api/block-buzz/`
- 固定提交 shallow clone：
  - `runtime/hermes/github-hot-project-learning/evidence/2026-07-23/open-code-review/`
  - `runtime/hermes/github-hot-project-learning/evidence/2026-07-23/buzz/`
- 核心来源链接：
  - [OpenCodeReview README](https://github.com/alibaba/open-code-review/blob/cf3bf706e842a26b256a82d2d3a3c31de9bbf144/README.md)
  - [OpenCodeReview architecture docs](https://github.com/alibaba/open-code-review/blob/cf3bf706e842a26b256a82d2d3a3c31de9bbf144/pages/src/content/docs/en/architecture.md)
  - [OpenCodeReview v1.7.15](https://github.com/alibaba/open-code-review/releases/tag/v1.7.15)
  - [OpenCodeReview issue #461](https://github.com/alibaba/open-code-review/issues/461)
  - [Buzz README](https://github.com/block/buzz/blob/acfbb1bb6af54cb29cb152496ff43b8285dcb8cf/README.md)
  - [Buzz architecture](https://github.com/block/buzz/blob/acfbb1bb6af54cb29cb152496ff43b8285dcb8cf/ARCHITECTURE.md)
  - [Buzz security](https://github.com/block/buzz/blob/acfbb1bb6af54cb29cb152496ff43b8285dcb8cf/SECURITY.md)
  - [Buzz v0.4.23](https://github.com/block/buzz/releases/tag/v0.4.23)
  - [Buzz issue #2515](https://github.com/block/buzz/issues/2515)
