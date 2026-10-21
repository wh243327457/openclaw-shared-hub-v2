---
type: case
status: draft
created: 2026-10-22
updated: 2026-10-22
domain: learning
tags: [github-learning, security-audit, context-compression, evidence-ledger, reversible-offload]
---

# 2026-10-22 GitHub 热门项目学习报告

> 执行者：Hermes；按任务约束未调用 OpenClaw。  
> 查询时间：2026-10-22 07:31–07:48（宿主 UTC+09:00；GitHub API 时间按 UTC 原样记录）。项目发现来自 `https://github.com/trending?since=daily` 的真实 HTML，再用 GitHub Repository API 逐项核验；Stars/Forks/Language/License/更新时间均来自当次 API 快照。  
> 深读固定提交：`cloudflare/security-audit-skill@c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`；`headroomlabs-ai/headroom@e995eb9f1dacac7ed548758406de6c1508caef95`。  
> 真实来源：GitHub Repository/Commit/Release/Issues/Checks/License/Public Security Advisories API、README、依赖声明、关键源码。Dependabot alerts 两仓均因当前 token 权限返回失败；公开 advisory 空数组不等于无漏洞。本次未安装或执行两项目代码，因此运行行为只作“源码核验”，不冒充本机实测。

## 今日结论

**今天两条主线共同指向同一个工程原则：Agent 的“压缩”和“审计”都不能只产出一段更短或更像真的 prose；必须保留冻结的 coverage denominator、结构化候选、独立验证、可回取原文/证据和 fail-closed 终态，才能把节省 token 与减少误报建立在可追溯、可恢复的基础上。**

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 171,488 | 9,335 | JavaScript | MIT | 2026-10-18T01:55:14Z | 热度极高；输出精简方向与既有研究重叠，今日不重复深读 |
| [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | 141,464 | 16,721 | Python | GPL-3.0 | 2026-10-21T21:59:02Z | 成熟节点式生成工作流；GPL 边界和体量不适合今日窄研究 |
| [supabase/supabase](https://github.com/supabase/supabase) | 112,948 | 16,913 | TypeScript | Apache-2.0 | 2026-10-21T22:27:54Z | 云后端平台；与今日 Agent 证据闭环主线较远 |
| [stablyai/orca](https://github.com/stablyai/orca) | 101,151 | 6,396 | TypeScript | MIT | 2026-10-21T22:31:55Z | 多 Agent worktree/IDE 候选；仓库 38,930 files，后续专题研究 |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 94,832 | 23,736 | Python | Apache-2.0 | 2026-10-21T22:17:04Z | 推理服务成熟项目；今日不重复深读 |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | 77,214 | 5,989 | Python | Apache-2.0 | 2026-10-21T20:02:55Z | **深读：内容路由、可逆 offload 与 live-zone 安全** |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) | 59,116 | 9,658 | TypeScript | NOASSERTION | 2026-10-21T20:45:04Z | License API 不明确；只观察，不复制源码 |
| [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | 42,793 | 7,067 | Python | MIT | 2026-04-13T12:38:49Z | 热榜出现但 `pushed_at` 相对陈旧，维护状态需另核 |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 36,185 | 2,261 | JavaScript | MIT | 2026-09-14T19:29:02Z | **深读：coverage-led audit + 独立反证 + typed findings** |
| [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory) | 12,278 | 869 | Rust | MIT | 2026-10-21T19:47:05Z | 与 shared hub 高相关，但既有项目卡已存在，今日只列速览 |

> API 快照说明：`updated_at` 是 GitHub 仓库元数据活动时间，不等同源码提交时间；维护判断优先使用 `pushed_at`、commit、release 和 issue。顶层 License 不覆盖依赖、模型、数据、品牌与 release 制品。

## 深读项目

### 1. cloudflare/security-audit-skill

- **一句话判断**：值得学的不是一组安全提示词，而是把“发现漏洞”拆成冻结 coverage、隔离 hunter、独立 verifier、typed verdict、record re-verification 与由 canonical record 生成报告的审计协议。
- **解决的问题**：替代单 Agent 读仓库后直接输出漏洞报告的旧做法；旧做法会把未覆盖范围当“安全”、把候选当 confirmed、让 finder 自证，并让 severity 先于可复现 impact。
- **URL / API 快照**：https://github.com/cloudflare/security-audit-skill ；**Stars: 36,185 / Forks: 2,261 / Language: JavaScript / License: MIT（GitHub API）**；`created_at=2026-06-18T14:08:44Z`，`pushed_at=2026-09-14T19:29:02Z`，`updated_at=2026-10-21T22:31:11Z`。
- **固定提交 / release**：[`c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`](https://github.com/cloudflare/security-audit-skill/commit/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8)，commit time `2026-09-14T19:28:54Z`；Releases API 为空，无可核验 release/tag。
- **来源交叉核验**：README 的六阶段流程和 sandbox 要求；`SKILL.md` / `VALIDATION-AND-REPORTING.md`；两份 validator、schema；最新 issues/PR；fixed-head check-runs。

#### 架构 / 实现与数据流

```text
repo + source revision + prior ledgers/findings
                    |
                    v
       reconnaissance / trust boundaries
                    |
          coverage-ledger.json
      (canonical IDs + status invariants)
                    |
          isolated hunter assignments
                    |
              candidate set
                    |
        fresh verifier tries to disprove
          /             |             \
 confirmed     needs_validation      rejected
          \             |             /
            findings.json + schema
                    |
    validate-findings.cjs (shape + semantics)
                    |
     fresh final record/source verification
                    |
 REPORT.md / FINDINGS-DETAIL.md / NEEDS-VALIDATION.md
```

核心机制：

1. coverage 不是“Agent 看过了”的 prose，而是 `surface × boundary × subsystem × attack_class × optional lifecycle` 的 canonical tuple；状态分别约束 owner、reviewed paths、local checks、fingerprints 与 unresolved。
2. finder 不拥有 confirmed 权限；fresh verifier 负责反证。`needs_validation` 禁止 severity，避免把未证实候选包装成高危结论。
3. `findings.json` 是 canonical record；Markdown 报告是从已验证记录和 ledger 派生的 projection，而不是反过来从报告抽事实。
4. validators 不只做 JSON shape：还限制文件大小/嵌套/数组/错误数，拒绝 symlink、非 regular file、不安全相对路径和控制字符，并检查 trace 首尾、severity 不超过 impact、状态字段互斥。
5. README 明确 target-controlled build/test/browser 必须在无外网、allowlisted env、有资源上限、仅 scratch 可写的 OS sandbox 内执行；否则只保留 `needs_validation`。

#### repo tree 摘要

```text
security-audit-skill/
├── README.md
├── LICENSE
└── skills/security-audit/
    ├── SKILL.md                         # 触发、总流程、角色与反模式
    ├── RECONNAISSANCE.md                # 架构/边界/coverage synthesis
    ├── HUNTING.md                       # ledger 驱动分派与 hunting
    ├── ATTACK-CLASSES.md                # 通用攻击类
    ├── AI-AND-LLM.md                    # prompt/tool/output handling
    ├── WEB-PROTOCOL-AND-AUTH.md         # HTTP/auth
    ├── SUPPLY-CHAIN-AND-RELEASE.md      # 供应链/CI/签名/更新
    ├── ...                              # cloud/data/IPC/resource 等 companion blocks
    ├── VALIDATION-AND-REPORTING.md       # 候选验证→报告
    ├── report-schema.json               # 三种 verdict canonical schema
    ├── validate-findings.cjs            # findings shape + semantic validator
    ├── validate-coverage-ledger.cjs      # coverage identity/state validator
    └── *.test.cjs                       # 两个 validator 的 fixtures
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `skills/security-audit/report-schema.json` | typed findings contract | 用 `oneOf + verdict const` 分隔 confirmed / needs_validation / rejected，字段互斥 |
| `skills/security-audit/validate-findings.cjs` | canonical finding gate | 预解析资源限制、safe read、schema interpreter、trace/severity/verdict semantic checks |
| `skills/security-audit/validate-coverage-ledger.cjs` | coverage gate | canonical coverage ID、状态机、fresh owner、artifact namespace、排序/唯一性 |
| `skills/security-audit/HUNTING.md` | finder orchestration | 按 ledger unit 分派隔离 hunter，不以空 findings 代替 coverage |
| `skills/security-audit/VALIDATION-AND-REPORTING.md` | independent verification | fresh agent 反证、final record verification、由 record 生成报告 |

#### ⭐ 源码精读

1. `canonicalCoverageId(refs)`：把 coverage 身份绑定到语义 tuple，而不是 Agent 自由命名；字段缺失或意外字段直接拒绝。

```javascript
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

逻辑摘要：`surface/boundary/subsystem/attack_class[/lifecycle]` 先验证可见文本、NFC 与控制字符，再做 UTF-8 percent encoding；同一语义只能对应一个 ID，并要求全 ledger 字典序排序。它冻结 denominator，但不证明每个 local check 真执行了目标行为。

2. `validateStateInvariants(unit, base, errors)`：终态决定什么证据必须存在，禁止 planned/covered/candidate 共享一个松散 schema。

```javascript
function validateStateInvariants(unit, base, errors) {
  if (unit.status !== "candidate") requireEmptyArray(unit, "result_fingerprints", base, errors);
  switch (unit.status) {
    case "planned":
      if (unit.agent_id !== null) errors.push(`${base}.agent_id: planned unit must be unassigned`);
      emptyEvidence();
      requireEmptyArray(unit, "unresolved", base, errors);
      break;
    case "covered":
      requireOwner();
      requireNonemptyArray(unit, "reviewed_paths", base, errors);
      requireNonemptyArray(unit, "local_checks", base, errors);
      requireEmptyArray(unit, "unresolved", base, errors);
      break;
    case "candidate":
      requireOwner();
      requireNonemptyArray(unit, "result_fingerprints", base, errors);
      break;
  }
}
```

逻辑摘要：`blocked` 必须有 unresolved，`covered` 必须无 unresolved，`candidate` 必须有 fingerprint；reassignment 还要求 fresh owner，旧 artifact 不能复用。边界：本次源码仍只验证 artifact path 属于 `agents/<id>/artifacts/`，没有在该函数内对 artifact 实体做 existence/hash read-back。

3. `collectFindingSemanticErrors(findings)`：在 JSON Schema 之后再做跨字段业务约束。

```javascript
if (verdict === "confirmed") {
  if (!finding.execution || !hasVisibleProse(finding.execution.observed_result))
    errors.push(`${base}: confirmed finding requires a visible execution observed_result`);
  const overall = finding.severity && finding.severity.overall_severity;
  const impact = finding.severity && finding.severity.impact && finding.severity.impact.score;
  if (SEVERITY_RANK.get(overall) > SEVERITY_RANK.get(impact))
    errors.push(`${base}.severity.overall_severity: cannot exceed demonstrated impact`);
} else if (verdict === "needs_validation") {
  if (hasOwn(finding, "severity"))
    errors.push(`${base}: needs_validation finding must not contain "severity"`);
}
```

逻辑摘要：confirmed 必须有 observed execution 与 remediation；`needs_validation` 禁止 severity/execution/remediation，且必须有具体 validation plan。价值在于“证据不足”不能写成“高危待验证”。

4. `readFileWithinLimit(file)`：validator 自己也按不可信输入处理，不跟随 symlink，先限制 regular file 和 5 MiB，再以 fatal UTF-8 解码。

```javascript
descriptor = fs.openSync(file,
  fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK);
const stat = fs.fstatSync(descriptor);
if (!stat.isFile()) throw new SafeInputError("input must be a regular file");
if (stat.size > LIMITS.inputBytes)
  throw new SafeInputError(`input exceeds ${LIMITS.inputBytes} byte limit`);
return UTF8_DECODER.decode(Buffer.concat(chunks, bytesRead));
```

逻辑摘要：避免 symlink/device/blocking input 与过大文档直接进入 JSON.parse；随后还有文本级 nesting/array preflight。边界是同目录 schema 文件的供应链身份仍依赖固定源码与仓库权限。

#### 依赖分析与供应链风险

- 仓库**没有 `package.json`、lockfile、go.mod 或 requirements**；两个生产 validator 仅使用 Node built-ins（`fs/path/util` 或 `node:*`）。这减少 runtime 依赖，但运行时 Node 本身、安装 CLI、Agent harness 与被审计目标依赖不在这张“零依赖”图内。
- 顶层 GitHub API 与根 `LICENSE` 均为 MIT。规则文档可抽象，但不能未经 review 整包复制到 shared；报告 schema/validator 源码也需保留许可与来源。
- fixed-head check-runs 显示 JavaScript/TypeScript CodeQL success；这不是两 validator 完整测试的替代。本次未执行 Node tests，运行结果**待核验**。
- Public Security Advisories API 为 0 条；Dependabot alerts 因 token 权限读取失败。两者均不能证明没有未知漏洞或目标执行风险。

#### 可复用经验

- 当审计范围是多维组合时，应优先先冻结 canonical coverage denominator，再启动 hunter，因为空 findings 只在“已覆盖”前提下才有意义；边界是 coverage record 仍需真实 artifact closure。
- 当 Agent 提交安全候选时，应优先让不同 owner 的 verifier 试图反证，并把未决事实保留为 `needs_validation`，因为 finder 自证会放大确认偏差；边界是角色分离不等于模型、权限或 OS 隔离。
- 当报告会被人或另一个 Agent 消费时，应优先由 typed canonical findings 单向生成 Markdown，并在 schema 后补 semantic checks，因为 shape-valid 不等于 verdict 合法；边界是 schema 版本与 source revision 要一起绑定。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/coverage-artifact-closure-v1/` 建立 synthetic ledger：加入 `covered-but-missing-artifact`、symlink、wrong-owner、hash mismatch、stale source revision、reassigned-owner-reuses-artifact` 六个 fixture；让 checker 输出 `covered|candidate|blocked|failed`，只有 exact source revision 下的 regular file + owner + hash read-back 才允许 covered。只处理 synthetic files，不审计真实用户仓库，不调用模型。

#### 风险边界

- **License**：MIT 仅覆盖仓库源码；被审计项目、PoC、fixtures、报告披露和第三方漏洞数据另行受约束。
- **维护活跃度**：最后 push 为 2026-09-14，但 2026-10-21 仍有活跃 PR/issue；无 release/tag，默认分支就是可核验交付面，稳定性需观察。
- **安全风险**：README 要求执行 target-controlled code 时必须 OS sandbox、无外网、清洁 allowlisted env、资源限额和 scratch-only write；当前 Hermes cron 任务未建立这种 sandbox，因此不得照 Skill 自动执行未知仓库代码。
- **局限**：此次没有本机运行 validator tests；coverage validator 的 local artifact path 没有在所读函数内做实体存在/hash closure；独立 Agent 可能仍共享同一模型偏差或权限面。
- **不适用场景**：小范围人工 code review、没有并行 subagent 的宿主，或无法提供隔离执行环境时，不应伪装成 full audit，只能 guidance/source-only review。
- **不能自动执行**：不安装该 Skill、不运行目标仓库构建/PoC、不扫描私有源码、不自动上报漏洞、不改 Hermes/OpenClaw 配置或 curated active facts。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `canonical coverage → isolated finder → fresh verifier → typed verdict → record verification → derived report`，而不是整包安全攻击类知识。该机制与现有 `research/github-hot-project-learning`、verification-first、self-reflection 和 2026-09-17 的 artifact-closure 候选重叠；先扩展既有 POC，不创建重复 shared skill。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/coverage-artifact-closure-v1/`。
- 若 fixtures 通过，优先更新：
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：加入 source matrix、coverage denominator 与 artifact read-back；
  - `capabilities/skills/autonomous-learning/self-reflection-engine/SKILL.md`：candidate/needs_validation/rejected 分态，未经独立验证不得晋升；
  - `scripts/github_learning_orchestrator.py`：审计 receipt 记录报告 hash、coverage 与 validator version，而不只记录 score/path。
- 不复用上游 agent ID、绝对路径或输出目录；host adapter 必须通过 shared root resolver 计算路径。

### 2. headroomlabs-ai/headroom

- **一句话判断**：值得学的是把内容压缩拆成 `detect → lossless reformat → bloat-gated reversible offload → CCR retrieval`，并用 live-zone、tool-pair atomicity 和 pass-through failure 保住 Agent 协议，而不是照搬其“节省比例”宣传数字。
- **解决的问题**：替代“把所有 tool output 统一截断/摘要”的旧做法；统一截断会误删 error、破坏 tool_use/tool_result 配对、使 provider KV-cache 失效，并让被丢原文无法复查。
- **URL / API 快照**：https://github.com/headroomlabs-ai/headroom ；**Stars: 77,214 / Forks: 5,989 / Language: Python / License: Apache-2.0（GitHub API）**；`created_at=2026-01-07T19:58:51Z`，`pushed_at=2026-10-21T20:02:55Z`，`updated_at=2026-10-21T22:30:17Z`。
- **固定提交 / release**：[`e995eb9f1dacac7ed548758406de6c1508caef95`](https://github.com/headroomlabs-ai/headroom/commit/e995eb9f1dacac7ed548758406de6c1508caef95)，commit time `2026-10-21T20:02:54Z`；latest releases API 前三项为 `v0.41.0`（2026-10-14）、`v0.40.0`（2026-10-06）、`v0.39.1`（2026-09-26）。
- **来源交叉核验**：README 架构/限制/telemetry；Rust core pipeline/traits/content detector/safety/config；`Cargo.toml` 与 `pyproject.toml`；release/issues/check-runs；Public Security Advisory。

#### 架构 / 实现与数据流

```text
agent tool output / logs / diff / JSON / code
                    |
             ContentDetector
  JSON | diff | HTML | git-status | search | log | code | text
                    |
       +------------+-------------+
       |                          |
 lossless reformat          per-domain bloat estimates
 serial, stop early          parallel via rayon::join
       +------------+-------------+
                    |
       threshold + fallback decision
                    |
     serial OffloadTransform chain
          |                   |
 compressed marker      original -> CcrStore
          |                   |
          +------ headroom_retrieve -----+
                    |
        model receives shorter live zone
```

核心机制：

1. detector 使用固定优先级和门槛路由：JSON → diff → HTML → git status → search → log → code → plain text；低 confidence 不强行路由。`ContentType` 同时支持稳定 tag 与 operator natural name。
2. pipeline 将 `ReformatTransform`（语义等价、无需 CCR）和 `OffloadTransform`（线上的字节减少、原文必须入 CCR）分开，用 trait 强制 offload 返回非 Optional `cache_key`。
3. reformat 与 per-offload bloat estimation 并行；真正 offload 串行执行并看到前一步输出。所有 transform error 都降级为 skip/pass-through，不让压缩热路径 panic。
4. 默认门槛是 `reformat_target_ratio=0.5`、`bloat_threshold=0.5`、`offload_fallback_ratio=0.85`，且配置注释明确这些是 conservative defaults，不是普适事实。
5. `tool_pair_indices` 同时识别 OpenAI `tool_calls.id ↔ tool_call_id` 与 Anthropic `tool_use.id ↔ tool_result.tool_use_id`，要求成对处理，避免压缩一边后产生 protocol 400。

#### repo tree 摘要

```text
headroom/
├── README.md / CHANGELOG.md / SECURITY.md
├── pyproject.toml / uv.lock             # Python wheel、extras 与锁图
├── Cargo.toml / Cargo.lock              # Rust workspace
├── crates/
│   ├── headroom-core/
│   │   ├── config/pipeline.toml         # conservative routing/offload defaults
│   │   └── src/
│   │       ├── transforms/              # detector、compressors、safety
│   │       ├── transforms/pipeline/     # traits/config/orchestrator/offloads/reformats
│   │       └── ccr/                     # in-memory/SQLite/Redis stores
│   ├── headroom-proxy/                  # Anthropic/OpenAI live-zone proxy
│   └── headroom-py/                     # PyO3/maturin bridge
├── headroom/                             # Python SDK/CLI/proxy/providers/memory
├── sdk/typescript/                       # TypeScript SDK
├── plugins/openclaw/                     # OpenClaw adapter（本任务未启用）
├── benchmarks/                           # seeded benchmark/eval scripts
├── tests/ + crates/*/tests/              # Python/Rust/parity/E2E fixtures
└── docs/content/docs/                    # architecture/CCR/limitations/security docs
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/headroom-core/src/transforms/content_detector.rs` | typed routing | 固定 detection order、confidence threshold、Python parity fixtures |
| `crates/headroom-core/src/transforms/pipeline/traits.rs` | transform contract | reformat/offload 分型，offload 强制 store + cache key |
| `crates/headroom-core/src/transforms/pipeline/orchestrator.rs` | hot-path orchestration | reformat 与 bloat 并行，offload gate，error pass-through |
| `crates/headroom-core/src/transforms/safety.rs` | tool pair safety | OpenAI/Anthropic pair extraction，去重 pair |
| `crates/headroom-core/config/pipeline.toml` | policy defaults | stop/threshold/fallback 与各 domain floor |
| `pyproject.toml` / `crates/headroom-core/Cargo.toml` | 依赖面 | Python+Rust+optional ML/proxy/native 供应链 |

#### ⭐ 源码精读

1. `detect_content_type(content: &str) -> DetectionResult`：明确有序 detector 与 confidence gate；低置信度回落 plain text，而不是强路由。

```rust
pub fn detect_content_type(content: &str) -> DetectionResult {
    if content.is_empty() || content.trim().is_empty() {
        return DetectionResult::plain_text(0.0);
    }
    if let Some(r) = try_detect_json(content) { return r; }
    if let Some(r) = try_detect_diff(content) {
        if r.confidence >= 0.7 { return r; }
    }
    if let Some(r) = try_detect_search(content) {
        if r.confidence >= 0.6 { return r; }
    }
    if let Some(r) = try_detect_log(content) {
        if r.confidence >= 0.5 { return r; }
    }
    DetectionResult::plain_text(0.5)
}
```

逻辑摘要：优先顺序本身是 policy；例如 search false positive 会误丢非匹配行，所以源码增加 path-shape guard。边界是 regex/heuristic 仍会漂移，必须绑定 detector version 与真实 corpus regression。

2. `CompressionPipeline::run(...) -> PipelineResult`：把 cheap decision 与 expensive transform 分离，且错误不传播到 Agent 主路径。

```rust
pub fn run(&self, content: &str, content_type: ContentType,
           ctx: &CompressionContext, store: &dyn CcrStore) -> PipelineResult {
    let (reformat_acc, bloat_scores) = rayon::join(
        || self.run_reformats(content, reformats),
        || self.estimate_bloats(content, offloads),
    );
    let reformat_ratio = current.len() as f64 / original_len as f64;
    for (offload, score) in offloads.iter().zip(bloat_scores.iter()) {
        let above = *score >= self.config.pipeline.bloat_threshold;
        let fallback = reformat_ratio > self.config.pipeline.offload_fallback_ratio && *score > 0.0;
        if !(above || fallback) { continue; }
        if let Ok(out) = offload.apply(&current, ctx, store) {
            if out.bytes_saved > 0 { current = out.output; cache_keys.push(out.cache_key); }
        }
    }
    PipelineResult { output: current, bytes_saved: total_saved,
                     steps_applied: steps, cache_keys }
}
```

逻辑摘要：bloat scores 保持与 offload registration order 对齐，offload 串行；失败时输出仍是原文/上一步结果。边界是 pass-through 保障可用性，不证明压缩质量或 retrieval 一定发生。

3. `OffloadTransform`：把“可恢复”变成类型契约，而不是 README 承诺。

```rust
pub trait OffloadTransform: Send + Sync {
    fn name(&self) -> &'static str;
    fn applies_to(&self) -> &[ContentType];
    fn estimate_bloat(&self, content: &str) -> f32;
    fn apply(&self, content: &str, ctx: &CompressionContext,
             store: &dyn CcrStore) -> Result<OffloadOutput, TransformError>;
    fn confidence(&self) -> f32;
}

pub struct OffloadOutput {
    pub output: String,
    pub bytes_saved: usize,
    pub cache_key: String,
}
```

逻辑摘要：`cache_key` 必填，trait 文档要求返回前先 `store.put`，并有测试要求 key 可 resolve。边界是 trait 无法独自保证 store durability、tenant scope、TTL 或模型真的调用 retrieve。

4. `tool_pair_indices(messages: &[Value]) -> Vec<ToolPair>`：协议结构是原子压缩单元。

```rust
pub fn tool_pair_indices(messages: &[Value]) -> Vec<ToolPair> {
    let mut announced: HashMap<String, usize> = HashMap::new();
    for (i, msg) in messages.iter().enumerate() {
        if msg.get("role").and_then(Value::as_str) == Some("assistant") {
            for id in collect_assistant_tool_call_ids(msg) { announced.insert(id, i); }
        }
    }
    // OpenAI tool_call_id and Anthropic tool_use_id both resolve to assistant index.
    // seen deduplicates multiple tool results in one message to one index pair.
    pairs
}
```

逻辑摘要：同一 assistant/user message 内多 tool blocks 最终去重成 message-index pair，保证 compression decision 同步。边界是 orphan response 只是不形成 pair；上层如何处置 orphan 仍需独立 fail-closed policy。

#### 依赖分析与供应链风险

- `pyproject.toml` core 直接依赖包括 `tiktoken`、`pydantic`、`litellm<2`、`click`、`rich`、`opentelemetry-api`、`ast-grep-cli!=0.44.1`、`pyyaml`、`tomlkit`、`truststore`、`hf-xet`；proxy/ML/memory/image 等 extras 再引入 FastAPI、httpx、OpenAI/MCP、ONNX Runtime、Transformers/Torch、sqlite-vec、OCR 等大图。
- `crates/headroom-core/Cargo.toml` 包含 serde、tokenizers/hf-hub、dashmap、regex、ICU segmenter、flate2、rayon、rusqlite bundled、可选 Redis、tree-sitter 多语言精确 pin、可选 fastembed/ORT/Magika。注释说明 ONNX/native/platform 与 parser parity 风险。
- Python production metadata 使用大量范围版本；`uv.lock` 可冻结仓库开发解析，但消费者 `pip install` 仍按当时索引解析。`[tool.uv].constraint-dependencies` 只对 uv 解析生效，不能自动等同所有 pip consumer 的全图硬 pin。
- fixed-head check-runs 中 Docker/init/CodeQL/gitleaks 和 npm audits 多项 success，但 `Rust advisories (cargo audit)` 与 `Dependency audit (pip-audit)` 均为 **failure**，很多普通 test/lint jobs 因变更路由而 skipped；因此不能写“CI 全绿”。失败根因本次未展开，标为**待核验**。
- Public Security Advisory API 返回 1 条 high：`GHSA-h46j-26q3-rggf / CVE-2026-71416`（Cross-Site WebSocket Hijacking），API 标 vulnerable `0.23.0`、patched `0.35.0`；当前 `pyproject.toml` 是 `0.41.0`，但实际部署版本仍须 read-back，不能因 main 新就假定已修。

#### 可复用经验

- 当上下文优化面对 JSON、日志、diff、代码等异构内容时，应优先先做 typed detection + confidence/abstain，再路由 domain transform，因为统一摘要会混淆不同 failure class；边界是 detector 必须有版本化 corpus 回归。
- 当压缩会删掉线上字节时，应优先先持久化 exact original 并返回必填 retrieval handle，再发布短视图，因为“短了”不等于可恢复；边界是 store 的 scope、TTL、加密、容量和删除覆盖需独立治理。
- 当 Agent 协议含 tool call/result 配对时，应优先把 pair 当原子单元，并在 live zone 之外保持 frozen prefix byte-identical，因为单边压缩会破坏协议和 provider cache；边界是 orphan/跨 turn 异常必须显式终态。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/reversible-context-route-v0/` 用 synthetic JSON/log/diff/tool-pair fixtures 实现纯 Python 原型：`detect → route → original store → marker → retrieve → byte equality`；加入 false-positive detector、store write failure、orphan tool result、TTL expired、tenant mismatch。验收要求任何不可恢复 lane pass-through 或 blocked，绝不 silent drop；不安装 Headroom、不改代理/provider/config。

#### 风险边界

- **License**：GitHub API、根 LICENSE 与 `pyproject.toml` 为 Apache-2.0；HuggingFace 模型、ONNX/native binaries、可选依赖、品牌和用户内容仍需逐项审查。
- **维护活跃度**：2026-10-21 有 push，10-14 发布 v0.41.0，issue/PR 同日活跃；更新快也意味着接口、依赖和 policy 变化频繁。
- **安全风险**：历史 high CSWSH advisory 已标 0.35.0 修复；fixed-head 两个 dependency audit jobs 当前失败；proxy 会接触 API key、prompt、tool output 和 loopback/admin surfaces，不能在未审配置下接入 Hermes。
- **隐私/telemetry**：README 声称 compression 本地执行，但 anonymous beacon 默认开启，发送 ratio/counters/provider/model/OS/arch；即便不传 prompt，也必须先按用户隐私策略评审并默认关闭 POC telemetry。
- **局限**：README benchmark 数字未在本机复现；短对话、密集 prose 可能无收益；模型可能不 retrieve；CCR store 故障/过期会让 marker 无法恢复；AVX2/ORT/model download/platform 有兼容边界。
- **不适用场景**：短会话、已经使用 provider-native compaction 且不需可逆检索、不能运行本地进程的 sandbox，或对额外 proxy/telemetry/存储面不接受的环境。
- **不能自动执行**：不把它插入当前 gateway，不运行 `headroom deploy/wrap`，不修改 `~/.hermes/config.yaml`、provider、model、cron 或 OpenClaw 插件，不下载模型/ONNX 制品，不上传私有上下文。

#### ⭐ Skill 升格判断

**需二次验证**。`typed detection + abstain + original-first reversible offload + pair atomicity + pass-through failure` 可迁移；完整 Headroom proxy/memory/learning 系统暂不沉淀。该候选与既有 context-pruning、canonical-derived、shared-memory、completion/receipt POC 重叠，应先做窄 fixture 并证明真实 Hermes token/quality 收益。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/reversible-context-route-v0/`。
- 若 fixture 与脱敏历史 replay 都通过，优先更新：
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：长 API/tree 输出先保留 runtime evidence，再生成带 truncation/retrieval pointer 的报告摘要；
  - `capabilities/skills/foundation/shared-memory-bridge/SKILL.md`：projection 必须带 canonical source identity、retrieval scope 与 expiry；
  - `runtime/hermes/github-hot-project-learning/`：只放 per-run evidence/cache，不把原始长输出晋升 curated。
- 真正接入 Hermes gateway 属配置变更，目标文件将是 `~/.hermes/config.yaml`；本次只提出候选，未经用户明确授权绝不写入。

## 跨项目机制对照

| 机制 | security-audit-skill | Headroom | 对 shared hub 的判断 |
|---|---|---|---|
| 冻结范围 | coverage canonical tuple | ContentType + detector order | denominator / routing policy 必须 host-owned 且版本化 |
| Agent 不确定性 | finder 只产 candidate | detector 有 confidence + fallback | uncertain 不得直接成为终态或 destructive transform |
| 可恢复证据 | ledger + findings + final verifier | original in CCR + retrieval key | 压缩/报告都要可回取 exact source |
| 独立收口 | fresh verifier / record verifier | tool-pair safety + store contract | verifier 与 producer 应分权，协议结构不可破坏 |
| 失败语义 | needs_validation / rejected / blocked | transform error → skip/pass-through | unknown/blocked 不能投影为 clean/completed |
| projection | canonical records → reports | original → compressed marker | prose/短视图只能是 derived artifact |

## 经验沉淀

1. 当 Agent 工作流要缩短上下文或扩大审计范围时，应优先冻结 canonical input identity、coverage denominator 与 policy version，因为“更短”或“没发现问题”都可能只是漏掉对象；边界是 identity/coverage 不证明结论正确。
2. 当模糊模型或 heuristic 提出候选分类、漏洞或压缩策略时，应优先限制它只产生 proposal，再由 deterministic host gate 检查 schema、scope、evidence closure 和 effect，因为置信度高不等于获准改变真相或丢弃原文。
3. 当任何 transform 会让模型看不到原字节时，应优先 original-first durable store + scoped retrieval handle + byte-equality read-back，因为不可回取的摘要无法审计误删；边界是存储本身会引入敏感数据、TTL、加密与删除治理。
4. 当结果有 `confirmed / needs_validation / rejected / blocked` 等不同状态时，应优先让 schema 与 semantic validator强制字段互斥，因为同一个松散对象会让 severity、remediation 与未决候选互相污染。
5. 当工具调用有 request/response、tool_use/tool_result 或 parent/child 配对时，应优先把关联单元原子处理，因为单边压缩、截断或恢复会破坏协议；边界是 orphan 必须显式标异常而非静默忽略。
6. 当外部仓库 CI 同时有 success、skipped 与 failed jobs 时，应优先逐 job 保留真实结论并标待核验根因，因为部分绿色不能覆盖 dependency audit failure，skipped 也不是通过。
7. 当热门项目提供自动 installer、proxy、hook 或 Skill 时，应优先只读源码和离线 fixtures，再决定是否安装，因为 License 合法、Stars 高和 README 安全声明都不是 effect authorization。

## Hermes / shared hub 统一落地建议

### Candidate POC A：coverage artifact closure v1

`runtime/hermes/github-learning-poc/coverage-artifact-closure-v1/`

```json
{
  "input_revision": "immutable-source-id",
  "coverage_id": "surface::boundary::subsystem::attack_class",
  "status": "planned|candidate|covered|blocked|failed",
  "owner": "runner-id",
  "artifact": {"path": "relative/path", "sha256": "...", "read_back": true},
  "verifier": {"owner": "different-runner-id", "version": "v1"},
  "unresolved": [],
  "terminal": "covered|needs_validation|blocked|failed"
}
```

### Candidate POC B：reversible context route v0

`runtime/hermes/github-learning-poc/reversible-context-route-v0/`

```json
{
  "input_hash": "sha256:...",
  "detector": {"version": "v0", "type": "json|log|diff|text", "confidence": 0.0},
  "policy": {"action": "pass|reformat|offload", "version": "v0"},
  "original_store": {"scope": "run-id", "key": "opaque-id", "verified": true},
  "projection_hash": "sha256:...",
  "retrieve_check": "byte-equal|blocked|expired",
  "terminal": "completed|pass_through|blocked|failed"
}
```

### 预期验收

- missing/symlink/wrong-owner/hash-mismatch artifact 不得成为 covered；
- finder 与 verifier owner 相同只能 `needs_validation`；
- original store write/read-back 失败时必须 pass-through 或 blocked，不能发布不可逆 marker；
- tool pair 单边进入 offload 时必须拒绝；
- detector false positive 要由 fixture 触发 fallback，并保留原始证据；
- 全部 POC 只在 runtime 使用 synthetic/脱敏 fixture，不改 config、provider、model、cron、shared skill 或 curated。

## Skill 升格总判断

- **今日不创建新 shared skill，不写 curated active fact。**
- security-audit-skill：**需二次验证**；只吸收 coverage/verdict/artifact-closure 协议，先更新既有 verification/GitHub-learning 候选，完整安全攻击 Skill 暂不沉淀。
- Headroom：**需二次验证**；只吸收 typed detection、reversible offload、pair atomicity 与 pass-through 原则，完整 proxy/memory/telemetry/runtime 暂不沉淀。
- 两项都必须先通过离线 POC、去重与治理审查；未经用户确认不落盘到 `capabilities/skills/` 或 `curated/memory/`。

## 明日继续

1. 建立 `coverage-artifact-closure-v1` 的 6 个 synthetic fixtures，并验证 source revision / owner / regular-file / hash / fresh verifier 全部参与 terminal。
2. 建立 `reversible-context-route-v0` 的 JSON/log/diff/tool-pair fixtures，加入 store write/read/TTL/tenant 失败和 detector false positive。
3. 展开 Headroom fixed-head `cargo audit` 与 `pip-audit` check failure 的日志，定位具体 advisory、依赖路径和是否只影响 dev/optional/runtime；未核验前不写安全结论。
4. 如 POC 捕获现有 orchestrator 的真实假绿或不可逆截断，再提交“更新已有 skill”的审核稿；否则仅保留 inbox/runtime 研究。

## 候选反哺

### Candidate Facts

- [ ] topic: coverage success 必须闭合到 exact artifact read-back | evidence: Cloudflare ledger 的 canonical/state invariants + 当前 local artifact 仅 path namespace 校验 | 建议: update 既有 artifact-closure POC，暂不写 active fact | 安全级别: medium
- [ ] topic: destructive context compression 必须 original-first 且 retrieval 可验证 | evidence: Headroom `OffloadTransform`/CCR contract + shared hub canonical/projection 分层 | 建议: create runtime fixture，POC 后评审 | 安全级别: medium
- [ ] topic: tool call/result 应作为原子上下文单元 | evidence: Headroom `tool_pair_indices` 对 OpenAI/Anthropic 的实现与 tests | 建议: update context-pruning candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: coverage-artifact-closure-v1 | 可复用场景: GitHub 学习、反思、巡检、安全审计 | 是否建议 shared: yes（仅 POC 后更新已有 skill） | 原因: 跨 agent 横切，但与 2026-09-17 候选重叠
- [ ] 名称: reversible-context-route-v0 | 可复用场景: 长 tool output、日报证据、Agent continuation | 是否建议 shared: yes（仅真实 replay 证明收益后） | 原因: 可补 truncation/retrieval contract，不应引入完整第三方 proxy

### Candidate Open Questions

- [ ] 问题: Headroom fixed-head 的 cargo-audit / pip-audit 失败具体命中哪些依赖与 execution path？ | reason: gap | priority: high
- [ ] 问题: 当前 GitHub-learning orchestrator 的 score 是否绑定 report content hash、source coverage 与 knowledge-base copy read-back？ | reason: gap | priority: high
- [ ] 问题: Hermes 长工具输出被截断时，是否存在可授权回取的 exact runtime evidence pointer 与 retention policy？ | reason: adaptation | priority: high
- [ ] 问题: Cloudflare coverage local artifact 是否已在待合并 PR 中增加 existence/hash closure？ | reason: stale | priority: medium

### 不应自动落地

- 不安装 Cloudflare Skill，不运行未知仓库代码、PoC、浏览器或目标服务。
- 不安装或接入 Headroom proxy/plugin，不下载模型/ONNX，不打开 telemetry。
- 不自动修改 Hermes/OpenClaw 配置、model、provider、gateway、cron、secret。
- 不把 public advisories 0、Dependabot 不可读、README benchmark 或 Stars 投影为安全/成熟事实。
- 不直接写 curated active fact，不复制整包上游源码到 shared skill。

## 知识库路径

审计通过后由 orchestrator 复制到 `03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-10-22-GitHub热门项目学习日报.md`；此处使用知识库根相对路径，避免把宿主绝对路径写入可迁移知识内容。
