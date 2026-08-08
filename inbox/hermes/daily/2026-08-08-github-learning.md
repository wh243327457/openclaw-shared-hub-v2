# 2026-08-08 GitHub 热门项目学习日报

> 执行器：Hermes（当前 OpenClaw runtime 不存在；本任务未调用、启动或模拟 OpenClaw）。  
> 研究时间：2026-08-08T07:31–08:10+08:00；GitHub API 查询窗口约 2026-08-07T23:31–23:36Z。  
> 发现来源：真实抓取 [`github.com/trending?since=daily`](https://github.com/trending?since=daily)，并用 GitHub Search API 补充 2026-07-01 后新仓；逐仓用 Repository API 核验元数据。  
> 固定源码快照：`openai/codex-security@8c40d7a0061488fedcd7e24a825c332f82d45483`；`denoland/celld@553ae73f83c87c3f7c7a5f73c32c2211d9d7341f`。  
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-08/`；clone：`runtime/hermes/github-hot-project-learning/repos/2026-08-08/`。  
> 数据边界：Stars、forks、updated/pushed 是查询时动态值；issue 内容是报告者陈述，除本报告列出的本机测试与静态交叉核验外，不视为已独立复现。

## 今日结论

今天的主线是：**Agent/自动化系统的“完成”与“仍有权执行”都必须由确定性外壳证明，不能从正文、进程存活、CAS 成功或一次时间读取推断。** `codex-security` 把语义结果、覆盖率和 sealed artifact 分开，明确 `partial/unknown` 不是 complete；`celld` 把对象所有权写成 object-store CAS 与 epoch，却被 open issue #132 指出：如果 takeover 用远端 wall clock、旧 owner 的 self-fence 用本地 monotonic clock，CAS 能保证“新记录唯一”却不能自动撤销旧进程的本地 authority。对 Hermes/shared hub 最值得迁移的窄原则是：**业务终态必须绑定 immutable input、coverage 与 artifact hash；时效授权必须绑定 owner generation、store revision、单调截止点和 effect-time revalidation。**

## 证据与执行摘要

- 先真实运行 `scripts/resolve_shared_root.py`，解析到 `/home/vany/agent/shared`，并读取 `manifest.yaml`、`AGENTS.md`、`curated/memory/MEMORY.md`；今日原始研究只写 Hermes inbox/runtime，没有直接写 curated。
- Trending HTML 保存为 `runtime/hermes/github-hot-project-learning/trending-2026-08-08.html`，真实大小 **640,804 bytes**；解析到 17 个仓库。9 个候选的 Repository API 原始响应写入 `project-overview-api.json`。
- 两个深读仓均 `git clone --depth 1` 并固定 HEAD；repo、commit、release、issues 原始 API JSON保存在 evidence 目录。
- `codex-security`：用锁定的 `pnpm@11.9.0 install --frozen-lockfile` 安装 **95 packages**；`pnpm run types` 通过；Bun 1.3.13 定向运行 comparison/contract/trusted-executable/multiscan 共 **86 passed / 1 skipped / 0 failed**。未登录、未调用模型、未扫描用户仓库。`pnpm audit --prod --audit-level high` **失败并实报 1 个 high**：`pdfjs-dist 5.6.205` 命中 `GHSA-hq66-cqwq-w95j / CVE-2026-16633`；其在本项目 Node 文本提取路径是否可达任意脚本执行尚未复现，不能降格为“无影响”。
- `celld`：临时为本机安装 Rust 1.97.1 toolchain（未写共享配置）；`cargo test --workspace --locked` 真实通过 **176 tests / 0 failed**。`cargo audit` 扫描锁文件 347 dependencies，**失败并实报 3 vulnerabilities + 2 unmaintained warnings**：`quick-xml 0.37.5` 两个 high、`rsa 0.9.10` 一个 medium、`paste`/`rustls-pemfile` 两个维护警告。未连接 S3、未启动 fleet/V8 runtime、未做网络或时钟偏移故障注入。
- 两仓 Dependabot alerts API 都返回 403 unauthorized；公开 repository security advisories API 当前返回空数组，但这不能替代 npm/RustSec 审计或私有 advisory。
- 未修改 Hermes/OpenClaw 配置、provider、模型、auth、env、cron 或 secret；未复制上游源码到 shared capabilities/curated。

## 项目速览

下表 Stars/Forks/Language/License/Updated/Pushed 来自约 2026-08-07T23:31–23:36Z 的 GitHub Repository API。`NOASSERTION` 表示 API 未识别仓库级 License，不等于“确认无 License”。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [jdx/mise](https://github.com/jdx/mise) | 32,061 | 1,332 | Rust | MIT | 2026-08-07T23:26:45 / 2026-08-07T23:27:25 | 成熟工具版本管理；今日与 authority/completion 主线较弱 |
| [xai-org/grok-build](https://github.com/xai-org/grok-build) | 24,392 | 4,633 | Rust | Apache-2.0 | 2026-08-07T23:04:07 / 2026-08-07T16:56:15 | 热门 coding agent；近期已多次深读，避免重复追热 |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | 13,576 | 1,832 | Python | MIT | 2026-08-07T23:32:10 / 2026-08-01T18:51:09 | 07-29 已深读 unattended/effect gate，不重复结论 |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 10,946 | 510 | Rust | MIT | 2026-08-07T23:31:48 / 2026-08-07T09:20:18 | 新文档解析候选；安全输入面很大，留待后续 |
| [openai/codex-security](https://github.com/openai/codex-security) | **9,264** | **638** | TypeScript | **Apache-2.0** | 2026-08-07T23:23:18 / 2026-08-07T23:31:27 | **深读：coverage-aware completion、sealed contract、restricted semantic reconciliation** |
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | 6,409 | 513 | TypeScript | MIT | 2026-08-07T23:31:28 / 2026-08-07T23:24:27 | RLM/continual harness 候选；高权 Python REPL，不因热度自动安装 |
| [semantica-agi/semantica](https://github.com/semantica-agi/semantica) | 2,332 | 305 | Python | MIT | 2026-08-07T23:32:08 / 2026-08-07T11:19:25 | 语义知识工程候选；今日不扩展 memory store |
| [denoland/celld](https://github.com/denoland/celld) | **2,191** | **60** | Rust | **Apache-2.0** | 2026-08-07T23:36:46 / 2026-08-05T13:43:16 | **深读：S3 CAS ownership、epoch fencing、wake durability、clock-skew authority gap** |
| [unclebob/swarm-forge](https://github.com/unclebob/swarm-forge) | 1,820 | 199 | Clojure | **NOASSERTION** | 2026-08-07T23:25:42 / 2026-08-07T20:22:31 | 多 Agent workflow 候选；许可未核验，不复制源码 |

Stars 只是发现信号，不是安全、维护质量、许可证兼容或生产成熟度证明。今天实际深读 `openai/codex-security` 与 `denoland/celld`；其他项目只做 API/README 层筛选。

## 深读项目

### 1. openai/codex-security

- **URL**：https://github.com/openai/codex-security
- **Stars / Forks / Language / License（GitHub API）**：**9,264 / 638 / TypeScript / Apache-2.0**。
- **updated / pushed**：2026-08-07T23:23:18Z / 2026-08-07T23:31:27Z。
- **API open_issues_count**：137（GitHub 该字段含 open PR，不等于纯 issue 数）。
- **固定 commit**：[`8c40d7a00614`](https://github.com/openai/codex-security/commit/8c40d7a0061488fedcd7e24a825c332f82d45483)，author/committer 2026-08-07T21:47:25Z，message `release: bump Codex Security to 0.1.8 (#315)`。
- **最新 Release**：[`npm-v0.1.8`](https://github.com/openai/codex-security/releases/tag/npm-v0.1.8)，published 2026-08-07T22:00:28Z；固定 clone 的 package version 为 0.1.8。

#### 一句话判断

值得学的不是“让模型找漏洞”，而是它用 **target snapshot → canonical manifest/findings/coverage → local validator → sealed artifact hashes → deterministic Markdown/SARIF projection → resumable campaign receipt** 把不确定扫描包进可审计外壳；同时 open issues 与今日真实 npm advisory 证明：外壳再严格，也不能把工具自身的 dependency risk、platform gap 或 completion/save mismatch抹去。

#### 解决的问题：替代了什么旧做法

1. 替代从 Markdown 反解析 finding identity：`findingId/occurrenceId/fingerprint` 由 target、rule、semantic anchor、scan ID 确定性派生。
2. 替代“扫描退出 0/生成报告 = 完成”：canonical contract要求 manifest/findings/coverage ID、scope、expectation、artifact SHA-256 与 seal 对齐。
3. 替代“没有 finding = 安全”：coverage 显式区分 `complete / partial / unknown`，并记录 surface disposition、exclusion、deferred、receipt refs。
4. 替代把 incomplete 当失败后盲目重跑：multiscan 保留 sealed incomplete bundle，标 `completed_with_incomplete_coverage`，避免重复费用；业务 gate仍可 fail-closed。
5. 替代让 LLM 自由匹配前后 findings：comparison thread 关闭 network/web/shell/plugins/multi-agent，强制 schema；本地再拒绝 invented/duplicate IDs。
6. 替代直接信任 repo 内 `git` shim、scope 与 output path：解析 trusted executable、清理 Git环境、要求 full immutable SHA、realpath containment、private non-symlink output。

边界：这些机制证明 artifact 一致性、requested scope 对齐和状态分类，不证明漏洞 finding 语义正确，也不证明扫描覆盖了工具未识别的攻击面。

#### 架构 / 实现与数据流

```text
repository/path/ref + requested mode
             │
             ▼
target normalization / immutable revision / trusted git
             │
             ▼
Codex Security scan + bundled plugin/workbench
  ├─ discovery / threat model / validation
  ├─ scan-manifest.json
  ├─ findings.json
  └─ coverage.json (complete|partial|unknown + receipts)
             │
             ▼
SDK contract loader
  ├─ bounded JSON/schema + canonical identity
  ├─ scope/expectation/cross-document checks
  ├─ non-symlink path + root inode/device checks
  └─ sealed artifact SHA-256 verification
             │
             ├─ deterministic report.md / SARIF projections
             ├─ scan history + semantic comparison
             └─ multiscan results.jsonl receipts + resume
```

核心不对称很重要：canonical JSON 与 receipt 是语义输入；`report.md` 是可再生 projection。Mutable workflow annotations 不应写回 sealed bundle。`multiscan` 的 incomplete 是“产出存在但覆盖不足”，不是 operational failed，也不是 complete。

#### Repo tree 摘要

```text
codex-security/
├── sdk/typescript/
│   ├── src/
│   │   ├── api.ts / cli.ts / config.ts          # SDK/CLI composition
│   │   ├── targets.ts / trusted-executable.ts   # target、Git 与 PATH 边界
│   │   ├── contract.ts / models.ts / result.ts  # canonical contract + validator
│   │   ├── multiscan.ts / scan-comparison.ts    # campaign resume + restricted reconciliation
│   │   ├── knowledge-base.ts / auth.ts           # imported docs 与 credential surface
│   │   └── runtime.ts / cost.ts                  # state、subprocess、telemetry
│   ├── _bundled_plugin/
│   │   ├── schemas/ / references/ / skills/     # scan contract 与 model workflows
│   │   ├── scripts/ / mcp/                      # Python workbench + MCP runtime
│   │   └── examples/completed-scan/             # canonical bundle fixture
│   ├── tests-ts/                                 # contract/multiscan/auth/CLI/recovery tests
│   ├── package.json / pnpm-lock.yaml             # pinned npm surface
│   └── README.md
├── docker/ / Dockerfile / compose*.yaml          # bulk scan container + AppArmor/seccomp
├── SECURITY.md                                   # explicit trust/security boundary
└── .github/workflows/                            # npm/container release and CI
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `sdk/typescript/src/contract.ts` | canonical bundle loader | 文档/Schema大小与深度、scope path、derived IDs、seal hash、receipt、root identity/权限检查 |
| `sdk/typescript/src/multiscan.ts` | 批量扫描与恢复 | immutable SHA inventory、checkout containment、durable JSONL receipt、lease-like supervisor lock、incomplete terminal |
| `sdk/typescript/src/scan-comparison.ts` | finding semantic reconciliation | read-only/no-network/no-tool model turn、strict schema、allowed occurrence IDs 与唯一性验证 |
| `sdk/typescript/src/trusted-executable.ts` | executable trust | 丢弃相对 PATH、repo-contained shim 与 unsafe entries，返回清洗环境 |
| `sdk/typescript/src/knowledge-base.ts` | 外部文档输入 | no-follow 读取、扩展名约束、PDF/DOCX extract、private temp；今日 advisory 的实际依赖入口 |
| `sdk/typescript/_bundled_plugin/schemas/coverage.schema.json` | completion schema | completeness、surfaces、exclusions、deferred；complete 禁止 deferred/needs_follow_up |
| `sdk/typescript/_bundled_plugin/references/scan-contract.md` | 语义规范 | canonical/projection 分层、target snapshot、finding identity、coverage semantics |
| `SECURITY.md` | 产品边界 | same OS account 非多租户；repo/Git/env 不是 sandbox；非 Codex secret 可能被 subprocess 继承 |

#### 源码精读（固定 commit）

**代码块 1：semantic comparison 把 LLM 放入最小能力、结构化输出通路**  
来源：[`sdk/typescript/src/scan-comparison.ts#L75-L131`](https://github.com/openai/codex-security/blob/8c40d7a0061488fedcd7e24a825c332f82d45483/sdk/typescript/src/scan-comparison.ts#L75-L131)

```ts
export async function matchScanFindings(
  input: ScanComparisonInput,
  options: ScanComparisonOptions = {},
): Promise<ScanComparisonResult> {
  const codex = options.codex ?? new Codex({
    config: {
      "features.multi_agent": false,
      "features.plugins": false,
      "features.shell_tool": false,
      "features.unified_exec": false,
      shell_environment_policy: {
        inherit: "core",
        exclude: ["CODEX_HOME", "*KEY*", "*SECRET*", "*TOKEN*"],
      },
    },
  });
  const thread = codex.startThread({
    sandboxMode: "read-only",
    approvalPolicy: "never",
    networkAccessEnabled: false,
    webSearchMode: "disabled",
    skipGitRepoCheck: true,
  });
  const turn = await thread.run(comparisonPrompt(input), {
    outputSchema: z.toJSONSchema(comparisonSchema, { target: "openapi-3.0" }),
  });
  return validateComparison(input, JSON.parse(turn.finalResponse), false);
}
```

逻辑：LLM 只做“是否同一 root cause”模糊判断，不获 shell/network/plugin能力；最终 `validateComparison` 只允许输入集合已有 occurrence ID，拒绝同一 ID 多次 confirmed、重复 uncertain 和不合法交叉。边界是 hosted model 仍接收 finding JSON；是否允许外发应由宿主数据策略决定，blacklist 环境变量也不是通用 secret证明。

**代码块 2：multiscan 把 coverage 不完整建模为独立终态**  
来源：[`sdk/typescript/src/multiscan.ts#L224-L281`](https://github.com/openai/codex-security/blob/8c40d7a0061488fedcd7e24a825c332f82d45483/sdk/typescript/src/multiscan.ts#L224-L281)

```ts
const result = await security.run(checkout, {
  mode: task.mode,
  outputDir: scanDir,
  ...(task.scope === undefined ? {} : { target: [task.scope] }),
});
coverage = result.coverage.completeness;
if (coverage !== "complete") {
  if (!(await hasArtifacts(scanDir))) {
    throw new Error("Multiscan scan output is missing required artifacts.");
  }
  warning = `Scan coverage is ${coverage}; results may be incomplete.`;
}
const status = failure !== undefined
  ? "failed"
  : warning === undefined
    ? "completed"
    : "completed_with_incomplete_coverage";
await appendReceipt(ledger, `${JSON.stringify({
  ...task, status, attempt, outputDir: scanDir, coverage, cost,
})}\n`);
```

逻辑：sealed partial/unknown 已产生有价值且可能昂贵的 artifact，不应按 transient failure 重试；但状态绝不伪装为 completed。`appendReceipt` 使用 0600、append、`sync()`，resume 又联合核验 computed attempt path 与 required artifacts。边界是 JSONL append + fsync 不是跨文件数据库事务；artifact语义完整性由下游 contract loader负责。

**代码块 3：contract loader不只验 Schema，还绑定 scope、ID 与 seal**  
来源：[`sdk/typescript/src/contract.ts#L92-L200`](https://github.com/openai/codex-security/blob/8c40d7a0061488fedcd7e24a825c332f82d45483/sdk/typescript/src/contract.ts#L92-L200)

```ts
export async function loadContract(scanDirectory: string, options: ...)
: Promise<LoadedContract> {
  const scanRoot = await requireScanRoot(scanDirectory, options.signal);
  const documentDigests = new Map<string, string>();
  const payloads = {
    "scan-manifest.json": await readScanJson(...),
    "findings.json": await readScanJson(...),
    "coverage.json": await readScanJson(...),
  };
  // bounded JSON Schemas are compiled and each payload validated
  if (findings.scanId !== manifest.scan.id || coverage.scanId !== manifest.scan.id)
    throw new ContractValidationError("Canonical contract scan IDs do not match.");
  if (!sameArray(coverage.includePaths, manifest.scan.scope.includePaths))
    throw new ContractValidationError("Coverage include paths do not match...");
  validateCanonicalContract(manifest, findings);
  await validateSeal(scanDir, manifest, findings, coverage, documentDigests, ...);
  if (options.expectation !== undefined)
    validateExpectation(manifest, coverage, options.expectation, ...);
  await verifyScanRoot(scanRoot, options.signal);
  return { manifest, findings, coverage };
}
```

逻辑：它先把 canonical files限定为 regular non-symlink files，做 bounded read和 schema复杂度限制，再校验 cross-document identity、derived finding IDs、requested target/mode/revision、artifact hash和 root device/inode。最后再验 root，降低读期间 replacement race。边界是本地同 OS account 可改进程/内存的攻击者不在其多租户边界内；SHA-256 也不是外部签名。

**代码块 4：coverage schema让 complete 与 deferred互斥**  
来源：[`coverage.schema.json#L190-L225`](https://github.com/openai/codex-security/blob/8c40d7a0061488fedcd7e24a825c332f82d45483/sdk/typescript/_bundled_plugin/schemas/coverage.schema.json#L190-L225)

```json
{
  "if": {
    "properties": { "completeness": { "const": "complete" } },
    "required": ["completeness"]
  },
  "then": {
    "properties": {
      "deferred": { "contains": {}, "minContains": 0, "maxContains": 0 },
      "surfaces": {
        "contains": {
          "properties": { "disposition": { "const": "needs_follow_up" } },
          "required": ["disposition"]
        },
        "minContains": 0,
        "maxContains": 0
      }
    }
  }
}
```

逻辑：不是靠 prose 声明 complete；只要有 deferred 或 needs_follow_up，schema 就拒绝 complete。边界是 producer 仍可能漏建 deferred unit，故 inventory strategy、receipt与独立 expectation同样必要。

#### 依赖分析与供应链风险

- package：`@openai/codex-security@0.1.8`，Node `^22.13 || ^24 || ^26`，package manager pin 为 `pnpm@11.9.0`。
- direct runtime dependencies：`@openai/codex`/`codex-sdk 0.144.6`、Ajv 8.20.0、Octokit 7.0.6、Inquirer 8.3.0、PapaParse 5.5.3、`pdfjs-dist 5.6.205`、fflate/extract-zip、incur、smol-toml。
- `pnpm install --frozen-lockfile` 输出 lockfile policy verified、安装 95 packages；只说明 lock 可解析与 policy通过。
- **真实 advisory**：`pnpm audit --prod --audit-level high` 返回 exit 1：`pdfjs-dist >=5.6.83 <6.2.108` 命中 `GHSA-hq66-cqwq-w95j / CVE-2026-16633`，修复版本 `>=6.2.108`。`knowledge-base.ts` 确实用 `pdfjs-dist/legacy/build/pdf.mjs` 解析 operator-selected PDF，并设置 `isEvalSupported:false`，但没有显式 `enableScripting:false`。该 Node extraction 形态是否满足 advisory 的 exploit前提仍**待核验**；在核验前不应无人值守导入不可信 PDF。
- Dependabot endpoint 403，公开 repo advisories空；这两项不能抵消本机 audit。
- bundled plugin含 Python scripts、MCP server、skills、schemas；Docker surface另有 Ubuntu packages/AppArmor/seccomp；模型/provider和 Trusted Access条款也不由 Apache-2.0 repo license覆盖。

#### README / docs / release / issues / source 交叉核验

- README 的 scan/SDK/container/resumable history 主线与 `api.ts`、`multiscan.ts`、`contract.ts`、Docker配置对应。
- `scan-contract.md` 明确 canonical JSON是 source of truth、Markdown/SARIF是 projection、bundle不是 mutable workflow DB；源码 `loadContract()` 与 schema落实了大部分约束。
- v0.1.8 release 声明新增 custom scan prompts，修复 container restart lock与“sealed incomplete bulk scans不再重试”；固定源码 `multiscan.ts` 和 tests存在对应逻辑，本机 multiscan定向测试通过。
- open issue [#299](https://github.com/openai/codex-security/issues/299) 报 v0.1.7 `scan --diff` 完成分析后因缺 `snapshotDigest` 保存失败；[#53](https://github.com/openai/codex-security/issues/53) 是相邻历史报告。固定 v0.1.8是否已修复真实 diff E2E **待核验**；本机未登录、未运行真实 scan。
- open issue [#302](https://github.com/openai/codex-security/issues/302) 报 Windows deep inventory输出反斜杠、下游只接受POSIX path；Linux定向测试无法证明 Windows修复。
- open issue [#292](https://github.com/openai/codex-security/issues/292) 报 standard scan完成后 manifest scan ID 与 workbench不匹配；[#290](https://github.com/openai/codex-security/issues/290) 报 deep scan把字面量 `$CODEX_SECURITY_SCAN_ID` 传给MCP；这些是报告者陈述，未独立复现。
- open issue [#291](https://github.com/openai/codex-security/issues/291) 报 telemetry读取 >1 MiB session event可在扫描完成后 abort；它说明辅助观测不能成为业务 artifact 的单点 fatal gate，但固定 v0.1.8状态待核验。

#### 真实测试结果

```text
$ npx --yes pnpm@11.9.0 install --frozen-lockfile
Lockfile is up to date ... Packages: +95 ... Done

$ npx --yes pnpm@11.9.0 run types
$ pnpm run generate:models:check && tsc --noEmit
# exit 0

$ npx --yes bun@1.3.13 test ... scan-comparison contract trusted-executable
50 pass / 1 skip / 0 fail

$ npx --yes bun@1.3.13 test ... multiscan
36 pass / 0 fail
```

准确结论：当前固定源码的类型检查、contract/comparison/trusted executable/multiscan定向 tests 通过。未运行 full 243-file surface、真实 provider/model、standard/deep/diff scan、Windows、container、AppArmor/seccomp、private repo、SARIF上传、release attestation。

#### 可复用经验

- 当不确定 Agent 只需比较结构化记录时，应优先关闭 shell/network/plugin/multi-agent并强制 schema，再由宿主验证 allowed IDs，因为 prompt injection声明不能替代 capability removal；边界是 hosted model仍是数据出口。
- 当任务产生完整但覆盖不足的 artifact时，应优先使用 `completed_with_incomplete_coverage` 并保留成本/receipt，而不是重试或冒充 complete；边界是消费者仍可把该状态视为发布失败。
- 当报告需要被人和机器同时消费时，应优先以 sealed canonical data为真相、从中生成 Markdown/SARIF projection，因为反解析 prose会丢 identity/coverage；边界是 seal不等于外部签名。
- 当高权工具导入 PDF/DOCX/zip等复杂格式时，应优先在执行前做版本/advisory与 parser capability gate，因为“用户选择了文件”不证明解析器安全；边界是版本命中不自动证明漏洞可达。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/terminal-evidence-bundle/` 做纯本地 fixture：

1. schema：`input_revision, instruction_sha256, report_sha256, coverage(completeness/surfaces/deferred), artifacts[], runner, audit_score, terminal_status`。
2. fixtures：complete、partial+artifact、unknown、deferred却声称complete、report被篡改、输出路径不匹配、retry attempt路径漂移。
3. validator：只有 immutable input + complete coverage + matching hashes + audit pass可投影为 completed；partial/unknown保留但不得完成。
4. 不安装/调用 Codex Security产品，不连接 provider，不扫描用户仓库，不导入PDF，不修改现有orchestrator。

#### 风险边界

- **License**：repo API、root LICENSE、package manifest均 Apache-2.0；Codex runtime、npm/Python/container依赖、模型/provider、扫描目标与生成patch分别审查。
- **维护活跃度**：固定 commit与release在查询日前数小时，更新很活跃；API `open_issues_count=137` 且多个completion/platform issue当日活跃，意味着协议 churn与回归面也大。
- **安全风险**：真实 high PDF.js advisory；复杂 PDF/DOCX/zip parser；scan可读源码/写workspace和state；环境可能向subprocess暴露非Codex cloud token；Git hooks/filter/helper/PATH不构成sandbox。
- **准确性局限**：LLM scanner有漏报/误报；complete只表示声明scope已处理，不表示无漏洞；semantic comparison的high confidence仍是模型判断。
- **一致性风险**：open #299/#292/#290/#291显示分析完成、artifact finalization、workbench identity和telemetry之间可能失配；定向 unit/integration tests不等于E2E。
- **供应链风险**：pnpm audit实报1 high；Dependabot不可见；bundled Codex binary/plugin/Python/container/release provenance未完整审计。
- **不适用场景**：把它当恶意repo sandbox、多租户扫描服务、无需授权的第三方安全测试、把0 findings当安全证书。
- **不可自动执行**：不安装产品、不登录、不设置API key、不扫描私有/第三方仓库、不应用patch、不上传SARIF/报告、不修改Hermes/OpenClaw配置/provider/cron。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`terminal-evidence-bundle`——canonical input/coverage/artifact hash/terminal status；以及 restricted semantic reconciliation 的“最小能力 + allowed IDs”契约。
- **需验证**：用当前 GitHub-learning历史日报与synthetic partial/unknown/篡改fixture跑通；与已有 `sealed-research-receipt-v2`、completion/source-outcome candidates去重。
- **暂不沉淀**：Codex Security产品、bundled security skills/MCP/Python workbench、PDF importer、provider/model/auth、Docker runtime。
- **今日动作**：更新 runtime project card/lessons/candidate；不创建 shared skill，不直接写 curated active fact。

#### Hermes / shared hub 落地路径

1. runtime POC：`runtime/hermes/github-learning-poc/terminal-evidence-bundle/{schema.json,fixtures/,validate.py,test_contract.py,README.md}`。
2. orchestrator proposal：未来给 `scripts/github_learning_orchestrator.py` 的 `status.json` 增加 `input_revision/report_sha256/coverage/artifact_receipt`，审计时从文件真实计算；本日不修改。
3. existing skill：POC通过后优先更新 `capabilities/skills/research/github-hot-project-learning/` 的 completion/evidence contract，不新建重叠skill。
4. 分层：raw API/test stdout留 `runtime/hermes/`；完整日报留 `inbox/hermes/daily/`；只有治理审查通过的窄原则才进入 `curated/memory/facts/`。
5. OpenClaw runtime不存在；不创建、不调用OpenClaw adapter，只保持schema agent-neutral/future-agent-readable。

---

### 2. denoland/celld

- **URL**：https://github.com/denoland/celld
- **Stars / Forks / Language / License（GitHub API）**：**2,191 / 60 / Rust / Apache-2.0**。
- **updated / pushed**：2026-08-07T23:36:46Z / 2026-08-05T13:43:16Z。
- **API open_issues_count**：14（含 open PR）。
- **固定 commit**：[`553ae73f83c8`](https://github.com/denoland/celld/commit/553ae73f83c87c3f7c7a5f73c32c2211d9d7341f)，author/committer 2026-08-05T13:27:25Z，message `v0.1.0`。
- **最新 Release**：[`v0.1.0`](https://github.com/denoland/celld/releases/tag/v0.1.0)，published 2026-08-05T13:43:13Z；固定 HEAD即 release target commit。

#### 一句话判断

值得学的是它把分布式 Durable Object 拆成 **无依赖 sans-I/O decision core + S3 conditional-write effect adapter + epoch fencing + per-cell SQLite/LTX replication + authenticated peer protocol**，从而能在fixture里验证顺序不变量；但 open issue #132 指出一个关键边界：object-store CAS只线性化owner record，若新owner的wall-clock expiry判断和旧owner的monotonic self-fence没有共享安全裕量，两个epoch仍可能同时在本地接受工作。

#### 解决的问题：替代了什么旧做法

1. 替代中心化control plane/consensus membership：S3-compatible bucket保存deployment、cell state、owner/node lease和wake records。
2. 替代共享大数据库：每个Durable Object拥有独立SQLite，按对象天然分片，LTX持续复制到bucket。
3. 替代I/O与决策混写：`celld-logic`无async/I/O/clock/random/lock/dependency，production executor只执行Effect；同一transition可被deterministic harness驱动。
4. 替代last-writer-wins ownership：owner object使用ETag CAS与monotonic epoch；release也只针对自己读到的exact record。
5. 替代alarm只留本地timer：wake entry必须在ack前durable PUT；move按put-before-delete；consume commit未复制前禁止删除entry。
6. 替代“内网HTTP无需认证”：peer request绑定protocol/method/path/body hash/source/target/timestamp/nonce的HMAC，并有clock/replay cap。

边界：没有consensus并不等于没有分布式时序问题。Bucket CAS提供对象级条件写，但lease expiration、旧owner fencing、replication durability、peer network和clock contract仍必须独立证明。

#### 架构 / 实现与数据流

```text
HTTP request / alarm / deployment
             │
             ▼
celld-logic::State::on_event(event)       # pure/sans-I/O decisions
  ├─ ownership/node-lease/epoch state
  ├─ route/activate/restore/evict/wake
  └─ emits typed Effect
             │
             ▼
crates/celld effect executor
  ├─ S3 owner/node lease CAS
  ├─ V8 Worker / Durable Object runtime
  ├─ per-cell SQLite + LTX replication
  ├─ signed peer HTTP / WebSocket tunnel
  └─ wake/deploy/diagnose/pressure adapters
             │
             ▼
S3-compatible bucket (durable authority)
  ├─ cells/<cell>/own.json (node, epoch, ETag)
  ├─ nodes/<node>.json (lease, addr, generation, load)
  ├─ wake/<minute>/<cell>
  ├─ deployments + current pointer
  └─ replicated cell state + fleet peer secret
```

关键不变量分两层：store CAS决定“谁能写新owner record”；local authority gate决定“旧进程是否还可执行”。二者必须共同满足single-writer。Release docs声称ownership epoch fences lost owner，但固定源码的remote lease takeover主要以`lease.expires_ms > now_ms`判断；issue #132的clock-skew序列与该静态结构一致，运行复现仍待核验。

#### Repo tree 摘要

```text
celld/
├── crates/
│   ├── logic/
│   │   ├── lib.rs                         # event/effect state machine、ownership/routing
│   │   ├── wake.rs / alarm.rs             # durable wake ordering与alarm decisions
│   │   ├── restore.rs / sqlite.rs          # epoch-aware restore与transaction rules
│   │   ├── routing.rs / peer.rs            # retry/protocol pure decisions
│   │   └── pressure.rs / cache.rs          # admission、shedding、cache policy
│   ├── celld/
│   │   ├── main.rs / runtime.rs / js.rs    # CLI、V8、Workers/DO host
│   │   ├── ownership_store.rs              # S3 CAS effect adapter
│   │   ├── peer_auth.rs / peer_probe.rs    # HMAC/version/replay/direct probe
│   │   ├── replication.rs / wake.rs        # LTX replication与wake executor
│   │   ├── deploy.rs / protocol.rs         # deployment object protocol
│   │   └── bucket.rs / storage.rs          # object store/SQLite effects
│   └── ltx/                                # Litestream-compatible WAL/LTX pipeline
├── docs/                                   # security、limitations、compatibility、operations
├── examples/                               # Worker/Durable Object fixtures
├── Cargo.toml / Cargo.lock                 # 3-crate workspace + lock
└── Dockerfile / .github/                   # image、release与CI
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `crates/logic/lib.rs` | 核心state machine | typed Event/Effect、node lease、owner CAS、epoch、routing、activation/fencing；remote lease按wall time判断 |
| `crates/logic/wake.rs` | alarm durability | ack前PUT、stale-early覆盖、put-before-delete、consume durability gate、in-flight delete race handling |
| `crates/celld/ownership_store.rs` | object-store adapter | owner/node lease wire、ETag CAS、ambiguous-vs-rejected语义、load sampling、release exact owner |
| `crates/celld/peer_auth.rs` | peer auth | protocol v2、HMAC canonical request、body hash、30s clock window、nonce replay cache |
| `crates/ltx/src/db.rs` / `replica.rs` / `leaser.rs` | SQLite durability | WAL capture、LTX chain、restore、conditional-write lease、resilience tests |
| `docs/security.md` / `docs/limitations.md` | trust boundary | bucket即admin authority；peer无TLS；alpha非hostile multi-tenant；one deployment/fleet |
| `Cargo.toml` / `Cargo.lock` | dependency truth | V8/Axum/object_store/rusqlite/crypto/LTX；RustSec今日实报3项漏洞 |

#### 源码精读（固定 commit）

**代码块 1：WakeCore把“ack前durable entry”做成状态机决策**  
来源：[`crates/logic/wake.rs#L106-L148`](https://github.com/denoland/celld/blob/553ae73f83c87c3f7c7a5f73c32c2211d9d7341f/crates/logic/wake.rs#L106-L148)

```rust
pub fn arm(&mut self, cell: &str, next_alarm_ms: Ms) -> Option<Op> {
    if next_alarm_ms < 0 { return None; }
    let want = entry_key(next_alarm_ms, cell);
    match self.flushed.get_mut(cell) {
        Some(e) if e.deleting => Some(Op::Put {
            key: want, due_ms: next_alarm_ms,
        }),
        Some(e) if e.verified && e.key <= want && e.delete_pending => {
            e.delete_pending = false;
            if e.key == want { None } else {
                Some(Op::Put { key: want, due_ms: next_alarm_ms })
            }
        }
        Some(e) if e.verified && e.key <= want => None,
        _ => Some(Op::Put { key: want, due_ms: next_alarm_ms }),
    }
}
```

逻辑：更早minute的verified entry可以覆盖更晚alarm，最多导致spurious wake、不丢wake；delete已上wire则必须重新PUT；尚未发出的delete可被新arm取消。边界是`verified`只代表executor报告PUT成功；object store错误分类、读取一致性和bucket权限仍属于adapter/部署边界。

**代码块 2：Reconcile把put-before-delete和失败短路固化，executor不能跳过**  
来源：[`crates/logic/wake.rs#L339-L384`](https://github.com/denoland/celld/blob/553ae73f83c87c3f7c7a5f73c32c2211d9d7341f/crates/logic/wake.rs#L339-L384)

```rust
pub fn next(&mut self, core: &mut WakeCore) -> Option<Step> {
    while let Some(op) = self.steps.pop_front() {
        match op {
            Op::Put { key, due_ms } => return Some(Step::Put {
                body: format!("{{\"cell\":{cell:?},\"due_ms\":{due_ms}}}"),
                key, due_ms,
            }),
            Op::Delete { key } => {
                if core.take_delete(&self.cell, &key) {
                    return Some(Step::Delete { key });
                }
            }
        }
    }
    None
}
pub fn put_failed(&mut self) {
    self.steps.clear();
}
```

逻辑：若replacement PUT失败，清空后续delete，避免armed alarm进入entryless状态；真正发DELETE前再次询问core，吸收异步窗口的新arm。边界是单个reconcile内顺序正确不等于跨进程/跨对象事务；crash可能保留额外entry，设计选择是at-least-one wake而非exactly-once。

**代码块 3：owner release/CAS绑定exact ETag与epoch**  
来源：[`crates/celld/ownership_store.rs#L271-L311`](https://github.com/denoland/celld/blob/553ae73f83c87c3f7c7a5f73c32c2211d9d7341f/crates/celld/ownership_store.rs#L271-L311)

```rust
pub async fn release_owner(&self, cell: &str, epoch: u64)
    -> anyhow::Result<CasOutcome> {
    let Some(current) = self.read_owner(cell).await? else {
        return Ok(CasOutcome::Rejected);
    };
    if current.node.as_deref() != Some(self.node.as_str())
        || current.epoch != epoch {
        return Ok(CasOutcome::Rejected);
    }
    let body = serde_json::to_vec(&OwnerWire { node: "", epoch })?;
    match self.bucket.put_cas(&key, body, Some(&current.etag)).await? {
        Some(_) => Ok(CasOutcome::Applied),
        None => Ok(CasOutcome::Rejected),
    }
}
```

逻辑：release不能覆盖并发takeover后的owner；保留epoch而把node置空，下一次claim再递增。边界是CAS线性化record write，不会向旧进程发送撤权中断；旧runtime是否停止仍依赖node lease/self-fence/effect-time checks。

**代码块 4：remote lease expiry只根据读取方wall clock决定takeover**  
来源：[`crates/logic/lib.rs#L3023-L3082`](https://github.com/denoland/celld/blob/553ae73f83c87c3f7c7a5f73c32c2211d9d7341f/crates/logic/lib.rs#L3023-L3082)

```rust
fn apply_node_lease_result(
    &mut self,
    id: &str,
    cell: &mut Cell,
    record: OwnerRecord,
    now_ms: u64,
    result: Result<Option<NodeLeaseRecord>, Failure>,
    effects: &mut Vec<Effect>,
) {
    match result {
        Ok(Some(lease))
            if lease.expires_ms > now_ms
                && !lease.addr.is_empty()
                && record.node.as_deref() == Some(lease.node.as_str())
                && lease.peer_protocol == self.config.peer_protocol => {
            // route Remote to existing owner/epoch
        }
        Ok(_) => {
            let epoch = record.epoch.saturating_add(1);
            self.activate_or_wait(id, cell, Activation::Claim(Claim {
                guard: CasGuard::Match(record.etag),
                epoch, takeover: true, reconciles: 0,
            }), effects);
        }
        Err(_) => { /* fail request */ }
    }
}
```

逻辑：foreign owner lease只要在observer的`now_ms`看来不再live，就进入owner CAS takeover。`Event::NodeLeaseRead`本身不携带`now_mono_ms`；issue #132所述“B wall clock ahead，而A monotonic self-fence尚未到期”的双local窗口与此结构一致。边界：本报告未把issue regression test移入固定仓运行，也未启动双node故障注入；因此是**高可信静态风险 + 上游公开复现声明，独立运行复现待核验**。

#### 依赖分析与供应链风险

- workspace三包：`celld 0.1.0`（43 direct dependency entries）、`celld-logic 0.1.0`（**0 dependencies**）、`celld-ltx 0.0.0`（16 entries）；均声明 Apache-2.0。
- core/system surface：V8 152、Axum/Hyper/Tokio、object_store 0.11、rusqlite 0.31、reqwest/rustls、LTX；crypto含AES-GCM、Ed25519、P-256、RSA、HMAC/SHA。
- `cargo test --workspace --locked`真实通过176 tests；它不覆盖真实S3 fleet、多node时钟偏移、V8应用兼容全表、长期soak或hostile multi-tenancy。
- `cargo audit`实报：
  - `quick-xml 0.37.5`：`RUSTSEC-2026-0194` quadratic duplicate-attribute check（high 7.5）和`RUSTSEC-2026-0195` namespace allocation DoS（high 7.5），修复`>=0.41.0`；`cargo tree -i`确认经`object_store 0.11.2`进入`celld`与`celld-ltx`。是否可由恶意S3-compatible XML响应触达需进一步测试。
  - `rsa 0.9.10`：`RUSTSEC-2023-0071` Marvin timing sidechannel（medium 5.9），无fixed upgrade；它是`celld` direct dependency，`js.rs`实际用于RSA key generate/decrypt。远程可观测性与key recovery条件待核验。
  - `paste 1.0.15`、`rustls-pemfile 2.2.0`为unmaintained warnings；前者由V8引入，后者在当前host feature tree的可达路径未完全确认。
- Dependabot alerts 403；公开repo advisory为空不能抵消RustSec结果。

#### README / docs / release / issues / source 交叉核验

- README声称S3 CAS owner、per-cell SQLite、bucket durability、peer HMAC/replay和无control plane；路径可在`ownership_store.rs`、`ltx/`、`peer_auth.rs`与`logic/`核验。
- `docs/security.md`明确bucket credential即fleet admin；peer只认证不加密；alpha不适用于hostile multi-tenant。`docs/limitations.md`还说明one deployment/fleet、无managed ingress/global placement、WebSocket跨owner测试较薄。
- v0.1.0 release重点是pressure shedding、streaming proxy、replicator seed、macOS memory与Apache-2.0 relicensing；固定commit就是release target。本报告不把README“release前有deterministic simulation”外推为本机已运行的隐藏release suite。
- open issue [#132](https://github.com/denoland/celld/issues/132) 给出具体TTL/clock-skew序列、`State::on_event` regression test和Quint model链接，报告两个owner epochs可同时`Route::Local`。固定源码expiry/takeover路径支持其机制判断；本机未独立运行fork test，修复方案仍**待核验**。
- open issue [#135](https://github.com/denoland/celld/issues/135)讨论signed identity token替代static endpoint，引用的是外部fork路径；不能当本仓已实现功能。
- README贡献方式关闭PR、要求email patch并含权利转让/许可条款；这不影响只读研究，但任何贡献需单独遵守。

#### 真实测试结果

```text
$ rustc --version && cargo --version
rustc 1.97.1 (8bab26f4f 2026-07-14)
cargo 1.97.1 (c980f4866 2026-06-30)

$ cargo test --workspace --locked
# 汇总各 test binary：176 passed / 0 failed
# 其中 celld-ltx lib 122、differential 5、fault 7、fuzz 7、
# integration/file/minio/resilience 各3、helpers 24、property 1、celld lib 1

$ cargo audit
Scanning Cargo.lock for vulnerabilities (347 crate dependencies)
error: 3 vulnerabilities found!
warning: 2 allowed warnings found
```

准确结论：固定release commit在Rust 1.97.1上完整公开workspace test命令通过；RustSec audit失败。未运行真实S3/R2/MinIO外部服务（测试名不等于外部部署证明）、双节点、clock skew、network partition、V8 Worker corpus、Docker、load/soak、release attestation。

#### 可复用经验

- 当分布式owner由lease expiry决定时，应优先同时定义wall-clock skew contract与local monotonic self-fence，并在每个effect boundary重验authority，因为CAS只能更新记录、不能撤销旧进程内存中的授权；边界是最安全方案需模型/故障注入验证。
- 当replace操作可能在中途crash时，应优先把操作顺序设计为安全偏置，例如put-before-delete让失败留下重复而不是丢失；边界是重复必须有幂等消费/GC。
- 当生产I/O复杂而不变量可纯化时，应优先抽取sans-I/O decision core并让executor逐step报告outcome，因为同一规则可被deterministic simulation和production复用；边界是adapter错误分类与时钟采样仍需contract tests。
- 当peer协议没有TLS时，应优先把authentication/integrity与confidentiality分开声明，因为HMAC/replay保护不加密源码或状态；边界是私网也需要真实网络隔离。

#### 30 分钟最小实验

在`runtime/hermes/github-learning-poc/lease-authority-model/`做纯Python离线state machine：

1. state：`owner, epoch, generation, store_revision, lease_expires_wall, local_deadline_mono, authority_state`。
2. fixture：无skew、B +1000ms、renew ambiguous、CAS rejection、old owner late effect、generation restart、clock jump back/forward。
3. invariant：任意real-time step最多一个generation可执行effect；CAS success但old generation未fence时必须`blocked`而非local。
4. 比较三种policy：wall-only、bounded-skew grace、observe-unchanged-revision-for-monotonic-TTL；只输出counterexample，不连接对象存储。

#### 风险边界

- **License**：repo API、root/workspace manifest为Apache-2.0；V8、Litestream-derived LTX、Rust dependencies、Worker bundles和container base分别审查。贡献另有README中的assignment条款。
- **维护活跃度**：v0.1.0三天内发布，issues当日活跃；但这是明确alpha、open_issues_count 14、协议/pressure/identity快速变化，不应当稳定基础设施。
- **安全风险**：clock-skew double-authority issue #132；peer HTTP无TLS；bucket credential是fleet admin；application ingress auth/TLS由operator负责；alpha非hostile multi-tenant。
- **供应链风险**：cargo audit实报2 high + 1 medium vulnerability及2 maintenance warnings；V8/native/build surface大；Dependabot不可见。
- **一致性风险**：owner CAS、node lease、local monotonic fence、LTX replication和wake entries跨多个对象/进程，不是单一事务；ambiguous I/O与clock skew需故障模型。
- **运行局限**：176公开tests通过，但`celld-logic`自身lib test binary为0 tests，许多decision-core验证可能在非公开release simulation或其他harness；#132未进入固定仓回归。
- **不适用场景**：hostile multi-tenant、没有私网/加密overlay、不能接受S3作为root authority、强一致跨对象事务、Windows、把alpha当托管control plane。
- **不可自动执行**：不部署fleet、不写bucket credential、不打开public peer port、不运行installer、不导入shared状态、不修改Hermes/OpenClaw cron/config。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`lease-authority-model`中的wall/monotonic/generation/effect-time revalidation，以及sans-I/O decision core + typed effect/outcome模式。
- **需验证**：先复现#132 counterexample并证明候选policy不会双authorise；再与已有effect-scope、scoped-authority、completion/lease候选去重。
- **暂不沉淀**：celld产品、S3 ownership protocol、V8 runtime、LTX implementation、peer HMAC code；shared hub当前不是分布式object-store runtime。
- **今日动作**：只写runtime project card/lessons/candidate；不创建shared skill，不写curated active fact。

#### Hermes / shared hub 落地路径

1. runtime POC：`runtime/hermes/github-learning-poc/lease-authority-model/{model.py,fixtures/clock-skew.json,test_invariants.py,README.md}`。
2. future scheduler contract：若shared cron/learning未来支持跨host claim，proposal字段为`job_id, owner_agent, owner_generation, lease_revision, observed_wall, local_deadline_mono, effect_scope`；每次写报告/状态前重验。当前`config/cron-jobs.json`仍是truth，不自动引入lease。
3. reflection/agent workflows：复用“pure decision → typed effect → reported outcome”作为候选测试结构，优先更新已有verification/self-reflection能力，不复制Rust实现。
4. 分层：counterexample traces留`runtime/hermes/`；研究正文留`inbox/hermes/daily/`；只有跨Agent反复验证后的最小不变量才考虑curated/shared skill。
5. OpenClaw runtime不存在；不创建分布式adapter，不把未来兼容描述成已落地。

## 经验沉淀

1. **当业务结果可能是完整、部分、未知、阻塞或失败时，应优先把coverage与terminal分开建模，并绑定immutable input和artifact hash，因为“有报告/退出0”不能证明完成；边界是complete也不证明结论无误。**
2. **当LLM只需做模糊匹配或归并时，应优先移除shell/network/plugin等能力、强制schema并验证allowed IDs，因为输入内的指令不能获得副作用权；边界是模型调用本身仍需数据出口授权。**
3. **当所有权依赖过期时间时，应优先同时使用wall-clock skew policy、local monotonic deadline、owner generation和effect-time revalidation，因为CAS只线性化store record、不自动撤销旧runtime；边界是policy必须经故障模型验证。**
4. **当replace流程不能跨对象事务时，应优先选择失败安全的顺序（例如put-before-delete），让crash产生可清理重复而非不可恢复缺失；边界是重复消费与GC必须幂等、有界。**
5. **当生产adapter包含网络、时钟、存储和进程副作用时，应优先抽取sans-I/O pure decision core和typed effect/outcome，因为simulation与production才能共享规则；边界是adapter的错误分类、采样和side effect仍需独立测试。**
6. **当高权工具支持PDF、DOCX、archive或复杂repo输入时，应优先在执行前结合锁文件、实时advisory与实际调用路径做gate，因为parser存在且版本固定不等于安全；边界是版本命中也不自动证明漏洞可达。**
7. **当认证协议运行在明文transport上时，应优先把integrity/authentication与confidentiality分开评估，因为HMAC、nonce和replay cache不能隐藏内容；边界是private network本身也需验证。**
8. **当上游issue给出复现和模型时，应优先交叉核验固定源码并明确“上游复现声明/本机复现”层级，因为issue可信度高于猜测但仍不是本机证据；边界是静态一致不等于已触发。**

### 跨项目机制抽象

| 维度 | Codex Security | celld | 对 Hermes/shared hub 的窄迁移 |
|---|---|---|---|
| 输入身份 | targetId + immutable revision/snapshot | cell + node generation + owner epoch/ETag | job/report ID + runner generation + immutable input hash |
| 完成/授权 | completeness + seal + expectation | live lease + local fence + owner CAS | terminal status与effect authority分别验证 |
| 不确定状态 | partial / unknown / deferred | ambiguous I/O / expired observation / CAS rejected | blocked/partial/unknown不得投影completed |
| 确定性外壳 | schema、derived IDs、hash、path checks | sans-I/O state machine、typed Effect | pure validator + typed side-effect receipt |
| 恢复 | JSONL attempt receipt + required artifacts | epoch/LTX/wake put-before-delete | resume绑定attempt/revision/artifact identity |
| 风险 | model/parser/dependency/platform gaps | clock/network/object-store/dependency gaps | 不自动改配置/cron/secret，不自动晋升curated |

## 明日继续

1. 实现`runtime/hermes/github-learning-poc/lease-authority-model/`的clock-skew counterexample，先证明wall-only takeover违反single-authority invariant，再比较bounded grace与monotonic observation方案。
2. 将今日`terminal-evidence-bundle`与已有`sealed-research-receipt-v2`、`source-outcome-contract`、`attempt-evidence-envelope-v0`去重，形成一个现有GitHub-learning skill的窄patch proposal，不新建第五套receipt。
3. 对Codex Security PDF.js advisory做只读reachability分析：确认Node legacy `getDocument`中scripting路径是否启用；不打开恶意PDF、不调用provider。
4. 若时间允许，用上游#132公开test思路写独立synthetic fixture（不复制fork实现），固定v0.1.0比较owner routes；不部署双节点或S3。

## 候选反哺

### Candidate Facts

- [ ] topic: coverage-aware terminal evidence：partial/unknown artifact不可冒充completed | evidence: `codex-security@8c40d7a`的`coverage.schema.json`、`contract.ts`、`multiscan.ts` + 本机86 tests | 建议: update/merge existing completion fact，避免重复 | 安全级别: low
- [ ] topic: store CAS不自动撤销旧runtime authority | evidence: `celld@553ae73` `apply_node_lease_result` + `ownership_store.rs` + open #132；本机未复现clock-skew序列 | 建议: create candidate after synthetic counterexample | 安全级别: medium
- [ ] topic: high权文档导入前需锁文件+实时advisory gate | evidence: Codex `knowledge-base.ts`实际引用`pdfjs-dist 5.6.205`；pnpm audit命中GHSA/CVE | 建议: compare/update existing ingestion safety fact | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: terminal-evidence-bundle | 可复用场景: Hermes cron学习、审计、future-agent handoff | 是否建议 shared: yes（验证后更新既有GitHub-learning skill） | 原因: 跨Agent横切，但必须与4个既有receipt/envelope候选去重
- [ ] 名称: lease-authority-model | 可复用场景: future跨host scheduler/claim/effect gate | 是否建议 shared: no（当前仅Hermes runtime POC） | 原因: #132尚未本机复现，shared cron当前无分布式lease需求
- [ ] 名称: Codex Security/celld product integration | 可复用场景: security scan或distributed DO runtime | 是否建议 shared: no | 原因: dependency advisory、高权输入/网络/存储面与当前需求不匹配

### Candidate Open Questions

- [ ] 问题: `pdfjs-dist` GHSA在Codex Security的Node legacy text extraction（`isEvalSupported:false`但未设`enableScripting:false`）是否实际可达？ | reason: security/reachability gap | priority: high
- [ ] 问题: celld v0.1.0能否用最小`State::on_event` fixture稳定复现#132双`Route::Local`，哪种skew/fence policy可证明修复？ | reason: distributed safety gap | priority: high
- [ ] 问题: Codex #299/#292的“analysis complete但final save失败”在v0.1.8是否已修复？ | reason: stale/E2E gap | priority: medium
- [ ] 问题: `quick-xml`两个high是否能由celld配置的S3-compatible endpoint响应触达，升级object_store/quick-xml会否改变协议兼容？ | reason: supply-chain reachability | priority: high
- [ ] 问题: 现有GitHub-learning orchestrator是否应以report hash+coverage receipt而非仅file existence+keyword audit写completed？ | reason: adaptation | priority: high

### 不应自动落地

- 不自动安装、登录或调用Codex Security，不扫描任何用户/第三方仓库，不打开未知PDF/DOCX，不应用或发布安全finding。
- 不部署celld、不创建bucket、credential、fleet secret或peer端口，不执行clock/network fault到真实环境。
- 不自动修改Hermes/OpenClaw config、provider、模型、auth、env、cron或secret；当前OpenClaw runtime不存在。
- 不把候选直接写入curated active fact，不从README/issue/assistant prose生成用户事实；先fixture、去重、证据评分与治理审查。
- 不复制上游源码到shared capabilities；只抽象agent-neutral contract，并分别遵守Apache-2.0、dependency license与贡献条款。
- 不把Codex 86 tests、celld 176 tests、empty public advisories或Repository API热度解释为完整产品安全；真实npm/RustSec advisory必须保留。
