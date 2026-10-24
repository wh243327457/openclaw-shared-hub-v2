---
type: case
status: draft
created: 2026-10-25
updated: 2026-10-25
domain: learning
tags: [github-learning, agent-sandbox, policy-prover, agent-plugins, supply-chain]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-10-22-GitHub热门项目学习日报]]"
---

# 2026-10-25 GitHub 热门项目学习报告

> 执行者：Hermes；按任务约束未调用 OpenClaw。  
> 查询时间：2026-10-25 06:30–07:34（宿主 UTC+09:00；GitHub API 时间按 UTC 原样记录）。发现入口是 `https://github.com/trending?since=daily` 的真实 HTML，随后用 GitHub Repository / License / Commit / Release / Issues / Checks / Security Advisories API 核验。  
> 深读固定提交：`NVIDIA/OpenShell@c4688aa8715ea75d6c39fe468361dbbc16c691fa`；`aws/agent-toolkit-for-aws@e8c630949189f03b3dd77388c86b06a7f2f911a9`。  
> 本次只读取 README、docs、release/issues、依赖声明和关键源码；**没有安装或执行两个项目**，所以 runtime enforcement、云端 API、SMT 求解结果与完整测试均标为待核验。

## 今日结论

**Agent 工程不能把“安全”寄托在提示词或自报声明上：高权执行应由宿主强制的 policy + fail-closed verifier 包住；跨 harness 分发的 skills/plugins 应由 canonical source、版本一致性、路径 containment 和真实副作用 gate 包住。**

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 108,001 | 14,805 | TypeScript | Apache-2.0 | 2026-10-24T01:15:52Z | 热度最高的 Agent CLI 候选；体量大，今日不扩散主题 |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 86,335 | 5,151 | Rust | Apache-2.0 | 2026-10-24T06:29:27Z | UI/设计能力；已有历史速览，避免重复深读 |
| [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) | 44,497 | 5,486 | Python | MIT | 2026-10-20T12:23:14Z | 使用指南集合；源码机制密度不如今日两项 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 32,063 | 1,646 | CSS | MIT | 2026-10-22T17:20:32Z | 前端生成方向；与今日安全控制面主线较远 |
| [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell) | 19,435 | 1,930 | Rust | Apache-2.0 | 2026-10-24T02:12:45Z | **深读：Agent sandbox、policy preview/prover、凭据句柄** |
| [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) | 10,939 | 1,405 | Rust | Apache-2.0 | 2026-10-24T09:37:44Z | 机器人方向活跃，但不是当前 shared hub 优先级 |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 4,052 | 582 | TypeScript | Apache-2.0 | 2026-10-24T22:33:05Z | 新近活跃；open issues 很多，后续再做稳定性筛选 |
| [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | 3,101 | 396 | Python | Apache-2.0 | 2026-10-23T15:00:22Z | **深读：canonical skills、跨 harness plugin manifests、验证与安全补丁** |

> API 快照说明：Stars 会继续变化；表内数字均是上述查询窗口的 Repository API 快照。`updated_at` 可能由元数据活动触发，因此维护判断使用 `pushed_at`、固定 commit、release、issues/checks。顶层 license 不能外推到依赖、云服务、模型、数据或 release 制品。

## 深读项目

### 1. NVIDIA/OpenShell

- **一句话判断**：值得学的不是“再加一个容器”，而是把 Agent 文件/进程/网络/凭据能力变成宿主可执行 policy，并在 policy 变更前同时生成同源 preview 与可机器判定的 prover 结果。
- **解决的问题**：替代“在当前宿主直接运行 Agent，再用 prompt 要求它不要越权”的旧做法；旧做法不能在 syscall、网络连接、secret 注入与动态 policy 更新处形成硬边界。
- **URL / API 快照**：https://github.com/NVIDIA/OpenShell ；**Stars: 19,435 / Forks: 1,930 / Language: Rust / License: Apache-2.0（Repository + License API）**；`created_at=2026-02-24T22:52:22Z`，`pushed_at=2026-10-24T02:12:45Z`，`updated_at=2026-10-24T22:32:20Z`，open issues/PR count `577`。
- **固定提交 / release**：[`c4688aa8715ea75d6c39fe468361dbbc16c691fa`](https://github.com/NVIDIA/OpenShell/commit/c4688aa8715ea75d6c39fe468361dbbc16c691fa)，commit time `2026-10-24T02:00:51Z`；latest stable release [`v0.1.5`](https://github.com/NVIDIA/OpenShell/releases/tag/v0.1.5)，published `2026-10-20T17:28:32Z`。
- **来源交叉核验**：README 的 sandbox/policy/provider/gateway 边界；Policy Prover docs；v0.1.5 release notes；最新 issues/PR；Cargo/pyproject；CLI policy update、prover policy/credential model、server credential runtime 源码；fixed-head Checks API。

#### 架构 / 实现与数据流

```text
Hermes/agent request
      |
      v
OpenShell CLI / SDK --------> Gateway control plane
      |                            |
      | policy mutation            | sandbox/provider/credential handles
      v                            v
build_policy_update_plan     policy store + credential drivers
  |              |
  |              +--> preview_operations --> local merge / human review
  +-----------------> merge_operations   --> gateway RPC
                                      |
                                      v
                           sandbox supervisor / driver
                 filesystem + process + network enforcement
                                      |
                       credential injected only at approved endpoint

candidate policy + boundary policy
                 |
                 v
       openshell-prover + Z3
 within_boundary | exceeds_boundary | unsupported | inconclusive | error
```

核心机制：

1. **控制面与执行面分离**：README 声明 gateway 管理 sandbox、policy 与 provider，supervisor/driver 承担运行时隔离；凭据不直接暴露给 Agent，而由受控链路解析/注入。该声明与 `CredentialRuntime` 的 handle/driver 设计一致，但真实 kernel enforcement 本次未运行，仍待核验。
2. **同源 preview / transport**：`build_policy_update_plan` 同时产出 wire `merge_operations` 和 local `preview_operations`，而 L7 target 只构建一次，降低“用户看到的 preview 与真正 RPC scope 不同”的风险。
3. **显式完整 scope**：L7 append 必须提供 rule name，并在 `--binary` 完整列表与 `--any-binary` 中二选一；混合 add-endpoint 与 append 被拒绝。这里用拒绝不完整表达，代替猜测目标规则。
4. **形式验证 fail-closed**：Policy Prover docs 把终态分成 0/1/2/3 exit code；只有 `within_boundary` 是通过。GraphQL/MCP/WebSocket 等未建模特性返回 `unsupported`，timeout/资源上限返回 `inconclusive`，而不是被静默忽略。
5. **凭据值与控制面引用分离**：provider 保存 `CredentialHandle`，runtime 按 driver 批量 resolve；未知、重复、缺失 request ID、过期值、未启用 driver 都会返回错误或 withholding。部分写入失败会尝试清理已成功项。

#### repo tree 摘要

```text
OpenShell/
├── README.md / SECURITY.md / LICENSE / THIRD-PARTY-NOTICES
├── Cargo.toml / Cargo.lock / deny.toml        # 38 个 Rust crates 与供应链策略
├── crates/
│   ├── openshell-cli/                         # CLI；policy update/preview
│   ├── openshell-policy[-schema]/             # policy 模型、解析、merge
│   ├── openshell-prover[-cli]/                # Z3 boundary / risk checks
│   ├── openshell-server/                      # gateway services、credential runtime
│   ├── openshell-supervisor-*                 # process/network/control/middleware
│   ├── openshell-driver-{docker,podman,vm,...}/
│   └── openshell-sdk / openshell-core         # 公共类型与协议
├── proto/ / sdk/{go,typescript}/ / python/    # 跨语言 SDK/protocol
├── docs/how-it-works/                         # policies/providers/sandbox 文档
├── deploy/helm/ / snap/                       # Kubernetes/packaging
├── tests/ / e2e/ / examples/                  # conformance 与场景 fixtures
└── skills/                                    # CLI/policy/debug skills
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/openshell-cli/src/policy_update.rs` | 构建 policy mutation | 一次构建 wire + preview；拒绝歧义 scope；解析 endpoint/L7/options |
| `crates/openshell-prover/src/policy.rs` | prover 投影模型 | 从有界 policy parser 投影 filesystem/network/L7；推断 access intent |
| `crates/openshell-prover/src/credentials.rs` | 凭据风险能力模型 | host/wildcard overlap、scope→action、write/destructive action 分类 |
| `crates/openshell-server/src/credentials.rs` | credential driver runtime | handle store/resolve/delete、批量响应完整性、expiry、partial rollback |
| `docs/how-it-works/policies/prover.mdx` | verifier 契约 | 五种结果、coverage、counterexample、unsupported/inconclusive 边界 |
| `Cargo.toml` / `crates/openshell-prover/Cargo.toml` | 依赖与 verifier backend | Tokio/Tonic/Axum/Rustls/SQLx/Kube/Z3 等核心依赖 |

#### ⭐ 源码精读

1. `build_policy_update_plan(...) -> Result<PolicyUpdatePlan>`：在生成任何 mutation 前先拒绝不完整或歧义 scope，并让 preview 与 RPC 使用同一个目标。

```rust
pub fn build_policy_update_plan(
    add_endpoints: &[String],
    remove_endpoints: &[String],
    add_deny: &[String],
    add_allow: &[String],
    remove_rules: &[String],
    binaries: &[String],
    rule_name: Option<&str>,
    any_binary: bool,
    endpoint_path: Option<&str>,
) -> Result<PolicyUpdatePlan> {
    let has_l7_append = !add_allow.is_empty() || !add_deny.is_empty();
    if any_binary && !binaries.is_empty() {
        return Err(miette!("--any-binary and --binary are mutually exclusive"));
    }
    if has_l7_append && binaries.is_empty() && !any_binary {
        return Err(miette!(
            "--add-allow and --add-deny require the complete --binary list or explicit --any-binary"
        ));
    }
    // ... push equivalent merge_operations and preview_operations ...
}
```

逻辑摘要：授权增量不是“加一个 URL”这么简单，binary identity、rule identity、endpoint path 与 L7 method/path 共同构成作用域。边界是 CLI validation 只是一层入口；其他 SDK/API 调用仍需 gateway/server 端再次验证，不能把 CLI parser 当最终 enforcement。

2. `Endpoint::intent(&self) -> PolicyIntent`：把 authored access preset 或规则集合投影成 prover 可比较的意图。

```rust
pub fn intent(&self) -> PolicyIntent {
    if !self.is_l7_enforced() {
        return PolicyIntent::L4Only;
    }
    match AccessPreset::parse(&self.access) {
        Some(AccessPreset::ReadOnly) => PolicyIntent::ReadOnly,
        Some(AccessPreset::ReadWrite) => PolicyIntent::ReadWrite,
        Some(AccessPreset::Full) => PolicyIntent::Full,
        None => {
            let methods: HashSet<String> =
                self.rules.iter().map(|r| r.method.to_uppercase()).collect();
            if methods.is_subset(&["GET", "HEAD", "OPTIONS"].into_iter().map(str::to_owned).collect()) {
                PolicyIntent::ReadOnly
            } else if !methods.contains("DELETE") {
                PolicyIntent::ReadWrite
            } else {
                PolicyIntent::Full
            }
        }
    }
}
```

逻辑摘要：prover 不直接拿 prose 判断风险，而把 endpoint 投影为有限模型。真正关键的是 docs 同时承认模型边界：未支持协议必须 `unsupported`；所以“证明通过”只对 coverage 声明内成立。上段为便于聚焦而按同一逻辑缩写的源码摘录；真实实现还显式处理 `rules.is_empty()`，并以预构造的 read-only 方法集合判定。

3. `CredentialRuntime::resolve_provider_handles(...)`：把 driver 当不可信协议对端，验证 response identity/completeness，并对过期 secret fail closed。

```rust
pub async fn resolve_provider_handles(
    &self,
    provider: &Provider,
    now_ms: i64,
) -> Result<ResolvedProviderCredentials, Status> {
    self.registry.validate_provider_handles(provider)?;
    // requests are grouped by driver and stamped with request_id
    let responses = driver.resolve_credentials(requests).await?;
    for response in responses {
        if !expected_request_ids.contains(&response.request_id) {
            return Err(Status::internal("credential driver returned unknown request_id"));
        }
        if !seen_responses.insert(response.request_id.clone()) {
            return Err(Status::internal("credential driver returned duplicate request_id"));
        }
        if effective_expires_at_ms.is_some_and(|expiry| expiry <= now_ms) {
            resolved.expired_keys.insert(credential_key);
            continue;
        }
        resolved.values.insert(credential_key, response.value);
    }
    // every request_id must receive exactly one response
}
```

逻辑摘要：handle 不是 secret 本身，也不是无条件授权；driver 必须返回 exactly-once response，effective expiry 取 provider/driver 两者更早值。边界是同一 gateway 进程、driver 进程、backend store 和 endpoint injection 仍需要 OS/transport 权限与日志脱敏。

4. `ApiCapability::destructive_actions_for_scopes(...)`：从 token scopes 映射出高风险 API 行为，供 proposal risk check 使用。

```rust
pub fn destructive_actions_for_scopes(&self, scopes: &[String]) -> Vec<&ApiAction> {
    self.actions_for_scopes(scopes)
        .into_iter()
        .filter(|action| {
            let risk = self.action_risk.get(&action.action).map(String::as_str);
            matches!(risk, Some("high" | "critical"))
        })
        .collect()
}
```

逻辑摘要：到达 credentialed host 不只是 network allow；还需要结合 scope 与 API action risk 看潜在影响。边界是 registry 质量、API 演进和自定义服务语义会决定判定是否完整。

#### 依赖分析与供应链风险

- Rust workspace 的核心依赖包括 `tokio 1.43`、`tonic/prost 0.14`、`axum 0.8`、`tower 0.5`、`rustls 0.23`、`reqwest 0.12.28`、`sqlx 0.9`、`kube 0.99`、`z3 0.21`、`aws-lc-rs 1.16`；Python SDK 依赖 `grpcio>=1.60`、`httpx>=0.27`、`protobuf>=4.25` 等，`Cargo.lock` 与 `uv.lock` 在仓库内。
- 供应链面较大：38 个 Rust crates、跨 Rust/Python/Go/TypeScript、容器/Helm/snap、Z3 与 native crypto。Apache-2.0 顶层许可不替代 `THIRD-PARTY-NOTICES`、lockfile、镜像、二进制与 release provenance 审查。
- v0.1.5 release notes 明确升级 `rustls 0.23.46` 处理多条 RUSTSEC，并承认临时接受 build-only `zip` advisories；这说明 release 说明比“advisories API 空数组”更有信息量。
- fixed-head Checks 中 Rust/Go/Python/JS CodeQL success，但 `Cargo Deny` 于 `2026-10-24T07:35:28Z` failure，API annotation 只有 exit 1，没有暴露根因；同时 combined status 的 Branch Checks/Helm Lint 为 success。**不能声称固定提交 CI 全绿**，Cargo Deny 根因待核验。
- Public Security Advisories API 返回空数组，只能说明当前公开 advisory 列表为空；Dependabot/私有发现、未知漏洞、runtime 配置风险仍不可见。

#### 可复用经验

- 当 Agent 需要文件、进程、网络或 secret 能力时，应优先把权限放进宿主 enforcement plane，并让 prompt 只描述意图，因为模型自律不能阻止 syscall/egress；边界是 sandbox runtime 本身仍需版本、配置和内核级验证。
- 当 policy 变更既要给人预览又要提交远端时，应优先从同一 typed target 同时派生 preview 与 wire operation，因为两套独立拼装会产生 scope drift；边界是服务端仍必须重验。
- 当 verifier 不能覆盖某个协议或路径语义时，应优先返回 `unsupported/inconclusive` 并披露 coverage，因为静默忽略会把“未证明”伪装成“安全”；边界是 fail-closed 会增加人工处理量。
- 当 secret 经 driver/sidecar 解析时，应优先使用 opaque handle + request identity + expiry + exactly-once response，而不是把明文环境变量交给 Agent；边界是 backend、transport 与最终注入点仍需独立最小权限。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/policy-preview-envelope-v0/` 做**纯离线 synthetic fixture**：输入 `{actor, task_id, effect, target, binary_scope, network_scope, credential_refs, current_revision}`，同一纯函数生成 `human_preview.json` 与 `enforcement_request.json`；测试 missing scope、preview/wire divergence、unsupported protocol、expired credential、stale revision 五种情况必须返回 `blocked`。不安装 OpenShell，不执行未知代码，不读取真实 secret，不改 Hermes 配置。

#### 风险边界

- **License**：仓库与 License API 为 Apache-2.0；第三方依赖、镜像、Z3、云服务与 release assets 另行审查，复制源码需保留 notice。
- **维护活跃度**：最后 push 2026-10-24，v0.1.2–v0.1.5 在近一个月连续发布，issues/PR 活跃；同时 open issues/PR count 577，README classifier 仍标 Alpha，接口变化风险高。
- **安全风险**：Agent sandbox/gateway/credential driver 都是高权 TCB；错误 wildcard、policy gap、provider injection、driver compromise、DNS/redirect/host-alias 语义都可能扩大权限。v0.1.5 仍在修 DNS binding、fail-closed broker 与 crypto dependency。
- **CI 风险**：固定提交 `Cargo Deny` 失败，根因未从 API annotation 得到；本次没有本机 build/test，不能把 CodeQL success 当完整验证。
- **局限性**：prover docs 明确 GraphQL/MCP/WebSocket 等边界检查不支持；filesystem path containment 会受 symlink/image 信息影响；通过 boundary 不证明 policy 最小、适合任务或运行时确实执行。
- **不适用场景**：只需低风险只读文本处理、无法运维 gateway/sandbox、宿主不支持其 runtime，或不能接受 Alpha 接口/额外 TCB 时，不应为“看起来安全”强行引入整个平台。
- **不能自动执行**：不运行 README 的 curl installer，不创建 sandbox/gateway，不导入 secret，不改 provider/config/cron，不自动应用 policy，不把候选直接写 curated active fact。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `typed effect scope → same-source preview/wire → fail-closed coverage result → credential handle/expiry` 协议，不是 OpenShell runtime 本体。它与 shared hub 既有 verification-first、effect-scope、orchestrator 四状态候选高度重叠；先扩展现有 workflow，不创建重复 shared skill。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/policy-preview-envelope-v0/`。
- 若 fixtures 通过，候选修改：
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：为高权 step 增加 `effect/target/scope/revision/coverage/terminal` envelope；
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：未知仓库执行必须有 sandbox capability receipt，否则只 source review；
  - `scripts/github_learning_orchestrator.py`：把 `unsupported/blocked/inconclusive` 与 audit_failed 分开，避免“未运行”被关键词分数覆盖。
- Hermes 当前落地只做 policy contract/fixture，不修改 `~/.hermes/config.yaml`；OpenClaw 当前不存在，不做 OpenClaw 安装或配置。

### 2. aws/agent-toolkit-for-aws

- **一句话判断**：值得学的是把庞大领域知识库分成 canonical skills、按 harness 打包的 plugins、版本化 manifests 和 CI validators，并把“Markdown 指令也能造成真实数据外泄”当成供应链代码处理。
- **解决的问题**：替代“每个 Agent/IDE 复制一套散落 prompt/MCP 配置”的旧做法；旧做法会造成 skill 漂移、manifest 不一致、路径逃逸、secret 插值、依赖/副作用不可审计。
- **URL / API 快照**：https://github.com/aws/agent-toolkit-for-aws ；**Stars: 3,101 / Forks: 396 / Language: Python / License: Apache-2.0（Repository + License API）**；`created_at=2026-04-23T12:44:08Z`，`pushed_at=2026-10-23T15:00:22Z`，`updated_at=2026-10-24T22:24:24Z`，open issues/PR count `64`。
- **固定提交 / release**：[`e8c630949189f03b3dd77388c86b06a7f2f911a9`](https://github.com/aws/agent-toolkit-for-aws/commit/e8c630949189f03b3dd77388c86b06a7f2f911a9)，commit time `2026-10-23T14:59:30Z`；Releases API 返回空数组，无仓库级 tag/release 可作为稳定锚点。
- **来源交叉核验**：README 的 skills/MCP/plugins 分层；最新 PR；`tools/validate.py`、`validate_spec.py`、`sync-plugin-skills.py`；三套 marketplace/plugin manifests；build workflow/mise；依赖声明；Public Security Advisory `GHSA-2px6-hhjp-3g5x / CVE-2026-87912`；修复后的 AWS Security Agent skills。

#### 架构 / 实现与数据流

```text
canonical skills/**/SKILL.md + references/assets/scripts
                       |
         build_canonical_index(name -> source)
                       |
          sync-plugin-skills.py --check
                       v
plugins/{aws-core,aws-agents,...}/skills/*
        |               |                |
 Claude manifest    Codex manifest   Cursor/Devin/root v1 manifest
        +---------------+----------------+
                        |
        validate.py + validate_spec.py
 schema | frontmatter | containment | symlink | MCP URL/header rules
                        |
                        v
      marketplace / agent install surface
                        |
     MCP/API/cloud side effects at runtime
```

核心机制：

1. **知识与工具分层**：README 明确 skills 可按需加载，不要求 MCP；MCP 提供实时 AWS API、文档与脚本执行；plugin 再把二者打包。这比把所有权限藏在一个 skill 中更容易审计 capability boundary。
2. **canonical→bundled parity**：`sync-plugin-skills.py` 按 skill 目录名建立 canonical index，逐文件 byte comparison；`--check` 只报告 drift，apply 才删除并复制 bundled tree。
3. **多 harness manifests 不是一份 JSON 改后缀**：Claude/Codex/Cursor/Devin/root Agent Plugins v1 各有 manifest；validator 检查 name/version/description parity、路径存在/containment、MCP transport 与 URL 规则。
4. **两层 validator**：stdlib `validate.py` 提供基础门禁；`validate_spec.py` 使用 vendored Agent Plugins v1 schema、真实 YAML parser、NFKC/name/allowed-fields/path/symlink/placeholder/HTTPS/header 检查，避免加载时联网取 schema。
5. **instruction supply chain 是真实攻击面**：公开 advisory 显示旧版 skill 用可预测 S3 bucket name，只检查 bucket 存在、不验证 owner，可能把含 `.env`/private keys/Terraform state 的 source archive 上传给第三方。修复版 1.1.0 在 every S3 operation 传 `ExpectedBucketOwner` 并把 foreign-owned bucket 视为 fatal。

#### repo tree 摘要

```text
agent-toolkit-for-aws/
├── README.md / LICENSE / NOTICE / SUPPORT.md
├── skills/                                 # canonical skill corpus（118 个 SKILL.md）
│   ├── specialized-skills/...              # 按 AWS domain 分类
│   └── .../references|assets|scripts
├── plugins/                                # 5 个产品包；77 个 bundled SKILL.md
│   ├── aws-core/
│   ├── aws-agents/
│   ├── aws-data-analytics/
│   ├── aws-agents-for-devsecops/
│   └── aws-startup-advisor/
│       ├── plugin.json                     # Agent Plugins v1 root manifest
│       ├── .claude-plugin/.codex-plugin/...
│       ├── skills/commands/hooks/.mcp.json
│       └── package/script dependencies
├── .claude-plugin/ .agents/ .cursor-plugin/# marketplace adapters
├── rules/ / setup-instructions/            # project rules 与接入说明
├── tools/
│   ├── validate.py                         # stdlib baseline validator
│   ├── validate_spec.py                    # v1 schema + semantic validator
│   ├── sync-plugin-skills.py               # canonical parity
│   └── schemas/1.0.0/                      # vendored schemas
└── .github/workflows/build.yml / mise.toml # lint/validation/gitleaks CI
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `tools/sync-plugin-skills.py` | canonical skill 同步 | name→source index、byte-for-byte tree parity、check/apply 分离 |
| `tools/validate.py` | 低依赖基础门禁 | manifests、frontmatter、cross-manifest parity、MCP type/url 校验 |
| `tools/validate_spec.py` | Agent Plugins v1 conformance | vendored JSON Schema、真实 YAML、路径 containment、symlink/placeholder/header rules |
| `.claude-plugin/marketplace.json` / `.agents/plugins/marketplace.json` | harness adapters | 同一 5-plugin catalogue 的不同宿主 schema |
| `plugins/aws-agents-for-devsecops/skills/setup-security-agent/SKILL.md` | 高权 workflow | IAM/S3 setup；ExpectedBucketOwner 与 foreign bucket fail-closed |
| `plugins/aws-agents-for-devsecops/skills/scanning-with-aws-security-agent/SKILL.md` | source upload/scan | source zip、S3 upload、scan/poll/findings；advisory 修复调用点 |

#### ⭐ 源码精读

1. `build_canonical_index() -> dict[str, Path]` 与 `trees_match(a, b)`：把 top-level skills 作为单一来源，plugin bundle 只做 materialized projection。

```python
def build_canonical_index() -> dict[str, Path]:
    skills_root = REPO_ROOT / "skills"
    index: dict[str, Path] = {}
    for skill_md in skills_root.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        index[skill_dir.name] = skill_dir
    return index

def trees_match(a: Path, b: Path) -> bool:
    a_files = {p.relative_to(a) for p in a.rglob("*") if p.is_file()}
    b_files = {p.relative_to(b) for p in b.rglob("*") if p.is_file()}
    return a_files == b_files and all(
        filecmp.cmp(a / f, b / f, shallow=False) for f in a_files
    )
```

逻辑摘要：不仅比较 `SKILL.md`，还比较 references/assets/scripts 整棵树，避免“主文档同步、附件漂移”。边界是 index 只按目录 basename，若 canonical corpus 出现同名 skill，后者会覆盖前者；shared hub 若借鉴必须把 canonical relative path/scope 也纳入 identity。

2. `check_containment(rel_path, label, plugin_dir)`：插件路径不是做字符串 `..` 检查就结束，还要解析 filesystem target。

```python
def check_containment(rel_path: str, label: str, plugin_dir: Path) -> None:
    if "\\" in rel_path:
        error(f"{label}: path must use '/' separators")
        return
    if not rel_path.startswith("./"):
        error(f"{label}: plugin-relative path must begin with './'")
        return
    if ".." in Path(rel_path).parts:
        error(f"{label}: path escapes the plugin root")
        return
    root = plugin_dir.resolve()
    target = (root / rel_path[2:]).resolve()
    if target != root and root not in target.parents:
        error(f"{label}: path resolves outside the plugin root")
```

逻辑摘要：lexical path 和 resolved target 都检查，且 `reject_symlinks()` 直接禁止 plugin tree 下 symlink，防止 validator 读到包外文件。边界是 TOCTOU、打包器行为和安装后的 filesystem 仍由宿主 loader 负责。

3. `validate_server(...)`：MCP manifest 字段会变成 subprocess 或网络连接，因此按 effect surface 检查，而不是只做 JSON shape。

```python
def validate_server(name: str, srv: dict, label: str, plugin_dir: Path) -> None:
    if srv.get("type") == "stdio":
        cmd = srv.get("command")
        if PLACEHOLDER_RE.search(cmd):
            error(f"{label}: command must not use placeholders")
        if not (cmd.startswith("./") or "/" not in cmd):
            error(f"{label}: command must be a bare name or './' path")
    elif srv.get("type") in ("streamable-http", "sse"):
        parsed = urlsplit(srv.get("url"))
        if parsed.scheme != "https" and parsed.hostname not in LOOPBACK_HOSTS:
            error(f"{label}: non-loopback url must use HTTPS")
        if any(h.lower() == "authorization" for h in (srv.get("headers") or {})):
            error(f"{label}: must not embed credentials in headers")
```

逻辑摘要：非 loopback 强制 HTTPS，URL/header 禁止 expansion/embedded authorization，stdio command 与 args/cwd 分别处理。边界是 bare executable 仍依赖 PATH provenance，HTTPS 也不证明 endpoint 可信；最终执行前还需 host-owned allowlist/consent。

4. 修复后的 `setup-security-agent` / `scanning-with-aws-security-agent`：把可预测 bucket identity 与 owner assertion 绑定到每次 S3 操作。

```bash
BUCKET="security-agent-scans-${ACCOUNT}-${REGION}"
aws s3api head-bucket \
  --bucket "$BUCKET" \
  --expected-bucket-owner "$ACCOUNT"

aws s3 cp /tmp/source.zip \
  "s3://$BUCKET/security-scans/source/$WORKSPACE_ID/source.zip" \
  --expected-bucket-owner "$ACCOUNT"
```

逻辑摘要：advisory `GHSA-2px6-hhjp-3g5x` 说明旧版 `<=1.0.0` 可把源码上传给抢注 bucket 的第三方；patched `1.1.0` 把 403/`BucketAlreadyExists` 视为 fatal。边界是当前顶层 `.claude-plugin/marketplace.json` 仍把 DevSecOps plugin 标为 `1.0.0`，而插件内部四份 manifests/root `plugin.json` 是 `1.1.0`；这是真实版本元数据漂移，安装器取哪个版本字段需核验。

#### 依赖分析与供应链风险

- 仓库主 validator 分两层：`validate.py` 是 Python stdlib；`validate_spec.py` 需要 `jsonschema` + `pyyaml`，CI 用 `uv run --with ...`，schema vendored 在 `tools/schemas/1.0.0/`。Markdown lint 用 Node 24 + `markdownlint-cli2 0.18`，secret scan 用 `gitleaks latest`。
- 这是内容型 monorepo，没有一个统一根 `pyproject.toml/package.json/lockfile`。子 skill/script 自带依赖，例如 Bedrock migration script 使用 `boto3/botocore/jsonschema/openai/aws-bedrock-token-generator` 的范围版本；Agents Pay requirements 精确锁定 22 个 Python 包，OpenClaw adapter package 精确依赖 `typebox 1.1.39` 与 TypeScript 7.0.2。
- 风险在于 118 个 canonical skills、77 个 plugin-bundled skills、3,541 tracked files 和跨 harness manifests 会扩大审查面；Markdown 内 shell/cloud 指令本身能读文件、打包源码、改 IAM、上传 S3，不能按“文档”降级审查。
- fixed-head check-runs 显示 build、CodeQL Python/Actions、Scorecard success；`build.yml` 默认 permissions 全 none、job 只开 `contents: read`，Actions SHA pinned。但本次未运行仓库 validators；Dependabot/完整 dependency audit 待核验。
- Public advisory **不是空**：`GHSA-2px6-hhjp-3g5x / CVE-2026-87912`，medium，CVSS v4 5.1，affected `<=1.0.0`，patched `1.1.0`。顶层 marketplace 版本漂移让“已修复”不能只靠仓库 HEAD 推断给所有安装路径。

#### 可复用经验

- 当同一 skill 要发布到多个 Agent/harness 时，应优先保留 canonical source，再把 bundle 当可重建 projection 并在 CI 做整树 parity，因为人工复制会让 references/scripts 与主文档漂移；边界是 skill basename 不能作为全局唯一 identity。
- 当 manifest 中的路径、command、URL 或 header 最终会触发文件/进程/网络行为时，应优先把它们当代码做 schema + semantic + resolved-path 校验，因为 JSON shape 合法不等于副作用安全；边界是 loader 最终还要重验实际 target。
- 当资源名由账号、region、tenant 等公开信息可预测时，应优先在每次读写操作绑定不可伪造 owner/account 条件，因为“对象存在”不证明“对象属于我”；边界是 owner check 不替代 archive secret exclusion 和最小上传范围。
- 当发布安全修复时，应优先让 advisory patched version、每个 plugin manifest、marketplace catalogue 与安装器解析结果保持一致，因为仓库源码已修不等于消费者一定拿到修复版；边界是 version parity 还需 artifact hash/provenance。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/shared-skill-parity-v0/` 写只读 checker，针对 shared hub 当前 `capabilities/skills/` 与 `capabilities/manifests/shared-skills.yaml` 生成 `{canonical_path, manifest_entry, content_hash, symlink_target, reference_count, secret_scan_state}` receipt；先用 synthetic duplicate-basename、missing manifest、out-of-root symlink、stale projection、version mismatch fixtures。只报告，不复制/删除 skill，不修改 Hermes/OpenClaw 配置。

#### 风险边界

- **License**：仓库/License API 为 Apache-2.0；个别子 package 可有自己的 license（例如所读 Agents Pay package 为 MIT-0），AWS 文档、云 API、第三方依赖和生成制品另行约束。
- **维护活跃度**：最后 push 2026-10-23，最新 PR 更新到 2026-10-24，fixed-head build/checks success；无 repository releases/tags，稳定版本主要散落在 plugin manifests，版本治理更重要。
- **安全风险**：公开 CVE 已证明 skill 文本可导致源码/secret 外泄；`zip` 排除列表没有列出所有可能 secret（例如任意命名证书、state、credentials），即使 owner check 修复也不应默认上传整个 workspace。
- **版本风险**：DevSecOps 内部 manifests 是 `1.1.0`，顶层 Claude marketplace 条目为 `1.0.0`；validator 所读逻辑检查 plugin 内 parity，但没有在所读函数中比较 marketplace version 与 plugin manifest version。
- **局限性**：stdlib frontmatter parser 是简化实现；spec validator 才用真实 YAML。两套门禁规则存在演进漂移可能；bare command 的 PATH provenance、MCP endpoint identity 与云端授权不由 schema 证明。
- **不适用场景**：没有 AWS 使用场景、不能接受云端处理源码、需要 provider-neutral 能力，或没有严格 IAM/CloudTrail/数据出口审批时，不应安装整套 AWS plugins。
- **不能自动执行**：不安装 marketplace/plugin，不配置 AWS/MCP，不读取凭据，不创建 IAM/S3/Agent Space，不上传源码，不运行 scan/pentest，不把上游 118 skills 批量复制进 shared。

#### ⭐ Skill 升格判断

**需二次验证**。`canonical skill → host projections → parity/schema/containment gate` 与 shared hub 的 `capabilities/skills + manifest + local symlink bridge` 高度相关，值得更新已有 shared-skill governance / bridge 能力；但 security upload workflows 是 AWS 专用且有公开 CVE，不直接迁移。今天不新增重复 skill。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/shared-skill-parity-v0/`。
- 候选修改：
  - `capabilities/skills/foundation/shared-memory-bridge/SKILL.md`：将 projection parity 从“路径存在”升级为 canonical relative path + content/hash/target receipt；
  - `docs/shared-skill-governance.md`：增加 multi-harness manifest version parity、resolved containment、no-out-of-root symlink 与 effect-surface review；
  - `scripts/verify_bridge.py` 或新增窄 validator：只读检查 manifest→skill path→local bridge，不自动复制；
  - `capabilities/manifests/shared-skills.yaml`：继续作为共享 capability truth source，不引入 AWS/OpenClaw 专属绝对路径。
- Hermes 安装面仍保持 `~/.hermes/skills` 本地桥；OpenClaw 当前不存在，本轮不操作任何 OpenClaw runtime/config。

## 经验沉淀

1. 当 Agent 将执行未知代码、访问网络或使用 secret 时，应优先把 effect/target/scope/revision 放进宿主可强制的 policy envelope，并在最后副作用点重验，因为 prompt 和早期计划都不是持续授权；边界是 enforcement runtime 仍是高权 TCB。
2. 当 verifier 只覆盖输入的一部分时，应优先公开 coverage 并将 unsupported/inconclusive 作为非成功终态，因为没有建模不能被解释为满足边界；边界是 fail-closed 需要明确人工恢复路径。
3. 当同一 skill 跨 Hermes、其他 CLI 或 future agent 分发时，应优先使用 canonical source + 可重建 projection + parity receipt，因为多份手工副本会漂移；边界是 canonical identity 必须包含相对路径/namespace，不能只靠 basename。
4. 当配置字段最终变成 path、subprocess、URL、header 或云资源操作时，应优先做 resolved containment、transport、placeholder、credential 与 owner 校验，因为 schema-valid 只证明形状；边界是实际 loader/执行器仍要再验。
5. 当资源名可从公开状态预测时，应优先在每次操作绑定 owner/account/tenant 条件并对 mismatch fail closed，因为 existence check 会遭遇 namespace squatting；边界是 owner 正确仍不代表 payload 已脱敏。
6. 当安全修复跨多个 manifest/marketplace/release 面发布时，应优先做版本与 artifact identity 的全链一致性审计，因为仓库 HEAD 已修不能证明所有消费者拿到补丁；边界是版本一致还需运行时配置验证。

## 风险边界总表

| 维度 | OpenShell | Agent Toolkit for AWS | 本轮动作 |
|---|---|---|---|
| License | Apache-2.0；第三方与制品另审 | Apache-2.0；子 package/云文档另审 | 只抽象机制，不复制源码 |
| 维护活跃度 | 2026-10-24 push；v0.1.5；Alpha/577 open | 2026-10-23 push；无 repo release；64 open | 固定 commit，保留待核验 |
| 安全 | 高权 sandbox/gateway/credential TCB；Cargo Deny failure | 已发布源码外泄 CVE；版本元数据漂移 | 不安装、不连接 secret/cloud |
| 局限 | prover coverage 不完整；本机未测试 | validators/host adapters 可能漂移；本机未测试 | 只做离线 synthetic POC 候选 |
| 不适用 | 低风险简单文本任务或无运维能力 | 非 AWS / 禁止源码出域场景 | 不升格产品依赖 |

## Skill 升格总判断

- **NVIDIA/OpenShell：需二次验证**。抽象 policy preview/verifier/credential handle 协议，优先更新既有 orchestrator/verification contract；不引入 runtime。
- **aws/agent-toolkit-for-aws：需二次验证**。抽象 canonical skill parity 与 manifest/effect validator，优先更新 `shared-memory-bridge` 和 shared skill governance；不复制 AWS skills。
- **今日不直接写 curated active fact、不新建 shared skill**：两个候选都与现有能力重叠，且分别存在未运行的 enforcement/CI 问题与已知 CVE/版本漂移，需要 fixture 和治理审查。

## Hermes / shared hub 落地路径

1. `runtime/hermes/github-learning-poc/policy-preview-envelope-v0/`：离线验证 same-source preview/wire、coverage 终态、stale revision、credential expiry。
2. `runtime/hermes/github-learning-poc/shared-skill-parity-v0/`：离线验证 canonical path、manifest parity、symlink containment、hash receipt、duplicate basename。
3. 通过后只更新既有：
   - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`
   - `capabilities/skills/foundation/shared-memory-bridge/SKILL.md`
   - `capabilities/skills/research/github-hot-project-learning/SKILL.md`
   - `docs/shared-skill-governance.md`
4. 脚本路径必须由 `scripts/resolve_shared_root.py` 解析；不硬编码宿主绝对路径，不改 Hermes/OpenClaw config/provider/cron/secret。

## 明日继续

- **最小动作 1**：读取 OpenShell `openshell-prover` 的 boundary comparison 核心和 tests，做 5 个 synthetic policy cases；目标不是安装 runtime，而是验证 `within/exceeds/unsupported/inconclusive/error` 是否能映射到 shared hub 四/五状态。
- **最小动作 2**：对 Agent Toolkit 写一个只读版本 parity fixture，复现 `marketplace 1.0.0 vs plugin 1.1.0`，确认现有 validator 是否漏报，并记录安装器实际取值为“待核验”。
- **停止条件**：若与现有 verification/effect-scope/shared-memory-bridge 规则重复且没有新 failure fixture，则只更新 reference，不新增 skill。

## 候选反哺

### Candidate Facts
- [ ] topic: Agent 高权执行需要 host-enforced policy + coverage-aware verifier | evidence: `NVIDIA/OpenShell@c4688aa...` README、prover docs、`policy_update.rs`、`credentials.rs` | 建议: update（与 verification/effect-scope 去重） | 安全级别: medium
- [ ] topic: 跨 harness skill 分发应由 canonical source + full-tree parity + semantic manifest validation 驱动 | evidence: `aws/agent-toolkit-for-aws@e8c6309...` 的三个 validators 与 manifests | 建议: update shared-skill governance | 安全级别: low
- [ ] topic: 可预测云资源名必须在每次操作断言 owner | evidence: `GHSA-2px6-hhjp-3g5x / CVE-2026-87912` 与 patched 1.1.0 skill | 建议: candidate，先做跨云抽象评审 | 安全级别: high

### Candidate Skills / Workflow
- [ ] 名称: policy-preview-envelope-v0 | 可复用场景: Agent 高权工具/网络/secret 请求的预览与执行一致性 | 是否建议 shared: no（先 POC） | 原因: 与 orchestrator/effect-scope 重叠，且未运行 enforcement
- [ ] 名称: shared-skill-parity-v0 | 可复用场景: shared canonical skills 到 Hermes/future-agent 本地桥的漂移检查 | 是否建议 shared: yes（验证后更新既有 skill） | 原因: 跨 agent 横切能力，但应更新 `shared-memory-bridge` 而非新建重复 skill

### Candidate Open Questions
- [ ] 问题: OpenShell fixed-head `Cargo Deny` failure 的真实依赖/许可根因是什么？ | reason: gap | priority: high
- [ ] 问题: Agent Toolkit 安装器在 marketplace `1.0.0` 与 plugin manifest `1.1.0` 冲突时采用哪个版本，是否会阻止 patched version 被识别？ | reason: conflict | priority: high
- [ ] 问题: shared hub 当前 local bridge 验证是否覆盖 content hash、resolved symlink target、manifest version 与 duplicate basename？ | reason: adaptation | priority: medium

### 不应自动落地
- 不运行 OpenShell installer/sandbox/gateway，不修改 Hermes 配置、provider、cron 或 secret。
- 不安装 AWS marketplace/MCP，不创建 IAM/S3/Agent Space，不上传本地 workspace，不运行 scan/pentest。
- 不批量复制上游 skills，不把 GitHub Stars、README 声明、空 advisory 或单次 CI check 写成长期事实。
- 不把候选直接晋升为 curated active fact；先完成 synthetic fixtures、去重、证据与人工/总控审查。
