# 2026-08-27 GitHub 热门项目每日学习报告

- 执行器：**Hermes**。当前 OpenClaw runtime 不存在；本次没有调用、启动、模拟或向 OpenClaw 发送任务。
- 研究日期：2026-08-27（UTC+8）。
- 共享根：先执行 `python3 scripts/resolve_shared_root.py`，真实返回 `/home/vany/agent/shared`。
- 发现来源：2026-08-27T07:31–07:44+08:00 实际抓取 GitHub Trending daily 页面（解析出 16 个仓库），并用 GitHub repository API 逐仓核验速览项目；Stars、Forks、Language、License、updated/pushed 均来自 API 响应，不采用 README badge 数字。
- 深读固定提交：`tt-a1i/archify@8b542d60e5eb2c552a3bb5bc1651d076be312aec`；`browser-use/browser-use@28670f720f63cc5f525a2acd6d6072867689ab68`。
- 证据范围：每个深读项目均交叉读取 README、release、open issues/PR、关键源码和依赖清单，并运行本机聚焦验证。没有实际运行的浏览器/LLM/provider/cloud 路径均标为“待核验”。

## 今日结论

**今日主线是“确定性外壳必须覆盖最后一个副作用点”：Archify 已把 typed IR、结构化诊断、候选渲染、artifact checks、hash receipt 和同文件系统 rename 串成较完整的 verified-delivery 管线，但 CLI output 参数仍可把 HTML 成功覆盖到任意非 HTML 文件；Browser Use 已把浏览状态、LLM 决策、Pydantic action、EventBus/CDP、超时和页面变化保护分层，但 `data:`/`blob:` allowlist 绕过、步骤超时计数及文件写回真实性仍有 open gaps。对 Hermes/shared hub 可迁移的不是直接安装两个产品，而是 `typed proposal → deterministic validation → scoped effect gate → observed effect/readback → terminal receipt`，且 path、domain、secret、页面 revision 与持久化状态必须在最终 chokepoint 重验。**

## 研究范围与真实验证摘要

1. GitHub Trending daily 实际返回的候选包括 `tt-a1i/archify`、`anthropics/claude-plugins-official`、`basecamp/omarchy`、`rohitg00/ai-engineering-from-scratch`、`tinyhumansai/openhuman`、`browser-use/browser-use`、`K-Dense-AI/scientific-agent-skills`、`marin-community/marin` 等；本次选择 **Archify** 与 **Browser Use** 深读。
2. Archify repository API 快照：**17,833 Stars / 1,236 Forks / HTML / MIT**；`updated_at=2026-08-26T23:31:08Z`，`pushed_at=2026-08-26T14:10:32Z`，default branch `main`。浅克隆 HEAD 为 `8b542d60...`，提交时间 `2026-08-26T14:10:31Z`。
3. Archify 最新 GitHub release 是 `v2.15.0`（2026-08-17T15:50:19Z），而固定提交的 `archify/package.json` 是开发版 `2.16.0-dev.0`；**HEAD 不是 stable release**。
4. Archify 本机 `doctor` 全部标 `[ok]`；checked-in architecture example 的 showcase validation 真实返回 **9/9 checks、composition pass、0 errors、0 warnings**。
5. Archify 完整 `npm test` 真实汇总为 **728 tests / 709 pass / 3 fail / 16 skip**。3 个失败均由本机缺 `zip`/`unzip` 可执行文件触发，集中在 archive/onboarding gates；因此不能声称全绿。`npm audit --omit=dev` 为 0，但含 dev 依赖的 audit 有 **1 个 high**：`fast-uri` 的 host-confusion advisories。
6. Archify open issue #124 报告 CLI output path 可覆盖非 HTML 文件。本机在 `/tmp` 隔离目录使用 unchanged checked-in workflow 真实复现：`deliver ... /tmp/.../marker.env --json` **exit 0、receipt ok=true**，原 marker 被 713,856-byte HTML 替换。该结果只破坏隔离 fixture，没有触碰 shared、用户配置或凭据。
7. Browser Use repository API 快照：**110,949 Stars / 12,184 Forks / Python / MIT**；`updated_at=2026-08-26T23:30:09Z`，`pushed_at=2026-08-26T18:41:37Z`，default branch `main`。浅克隆 HEAD 为 `28670f720...`，也是 latest repository push，但 release `0.13.8` 发布于 2026-08-16；同样要区分 HEAD 与 release。
8. Browser Use 固定提交有 494 tracked files、167 个 `browser_use/**/*.py`、100 个测试文件；`python3 -m compileall -q browser_use` 成功。
9. Browser Use 仓库没有 checked-in `uv.lock`；第一次 `uv sync --frozen` 如实失败。随后仅在 runtime 浅克隆中运行 `uv sync`，解析 400 packages、安装 193 packages。清除本机继承的 HTTP/SOCKS proxy 环境后，action timeout + domain filtering 两组聚焦测试真实返回 **26 passed in 1.74s**；第一次未清 proxy 时 21 个 domain tests 因缺 `socksio` 在 session 构造阶段失败，这也说明测试/客户端初始化会受宿主环境污染。
10. Browser Use 当前环境 `pip-audit --path .venv/.../site-packages` 返回 exit 1：**21 个 vulnerability records / 6 packages**；含 runtime 路径上的 Click 8.3.1、cryptography 45.0.7、pydantic-settings 2.12.0、pypdf 6.14.2、Starlette 0.50.0，以及 dev-only pytest 9.0.2。requirements-level audit 因配置源无法取得 `portalocker==4.3.0` 而 blocked，所以不能声称 dependency closure 完整。
11. Browser Use open issue #4763 与固定源码一致：`SecurityWatchdog._is_url_allowed()` 在 domain policy 前无条件允许 `data:`/`blob:`；open issue #5513 与固定源码一致：timeout handler 的步数补偿条件可能双增，open PR #5521 正在修复。另有 #5527（失败文件写入污染内存状态）与 #5529（自动切换新 tab 失败仍报成功）。
12. Dependabot alerts：Archify 返回“disabled”403；Browser Use 返回 unauthorized 403。Repository advisories API：Archify 空数组；Browser Use 返回 1 条历史 critical advisory `GHSA-x39x-9qw5-ghrf/CVE-2025-47241`，受影响 `<=0.1.44`、patched `0.1.45`。空数组、403 或历史 advisory 已修复都不能证明当前依赖无漏洞。

## 项目速览

> 下表 Stars / Language / License / updated/pushed 均来自本次 GitHub repository API。Stars 是查询瞬时快照；License 是 GitHub 对仓库顶层 license 的识别，不覆盖依赖、模型、release assets、品牌素材或服务条款。

| 项目 | Stars | Language | License（GitHub API） | updated / pushed（UTC） | 今日判断 |
|---|---:|---|---|---|---|
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | 17,833 | HTML | MIT | 2026-08-26T23:31:08Z / 2026-08-26T14:10:32Z | **深读：typed IR、diagnostics、verified delivery 与 output path 缺口** |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 110,949 | Python | MIT | 2026-08-26T23:30:09Z / 2026-08-26T18:41:37Z | **深读：browser agent loop、typed actions、timeouts 与 domain/effect 边界** |
| [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) | 49,565 | Python | MIT | 2026-08-26T23:25:14Z / 2026-08-23T20:29:51Z | 教学型高热候选；需审内容 provenance 与可运行性 |
| [tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman) | 38,195 | Rust | GPL-3.0 | 2026-08-26T23:29:03Z / 2026-08-26T22:30:49Z | 机制已有 shared 项目跟踪；GPL 源码不复制 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 34,712 | Python | MIT | 2026-08-26T23:23:05Z / 2026-08-24T09:22:55Z | 科研 skill registry 候选；需逐 skill 审 authority/依赖 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 34,352 | Python | Apache-2.0 | 2026-08-26T23:30:40Z / 2026-08-26T07:40:55Z | 插件生态候选；不直接外推到 Hermes loader |
| [basecamp/omarchy](https://github.com/basecamp/omarchy) | 31,977 | Shell | MIT | 2026-08-26T23:29:39Z / 2026-08-26T21:56:34Z | 系统级安装 effect 面大，不适合无人值守尝试 |
| [freestylefly/awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) | 21,237 | JavaScript | MIT | 2026-08-26T23:26:15Z / 2026-08-26T08:54:32Z | 资源集合；需要逐素材/提示词来源审计 |
| [marin-community/marin](https://github.com/marin-community/marin) | 2,448 | Python | Apache-2.0 | 2026-08-26T23:30:54Z / 2026-08-26T23:22:19Z | 模型训练/数据流水线候选；基础设施成本高 |

## 深读项目

### 1. tt-a1i/archify

- **一句话判断**：Archify 值得学的是把 agent-authored diagram 从“直接生成 HTML”改造成 `typed JSON IR → deterministic diagnostics → candidate render → artifact checks → hash receipt → atomic commit`，但 CLI output 参数仍能成功覆盖非 HTML/越界路径，所以今天不能直接把完整 skill 放进 Hermes/shared；其 verified-delivery 思路只适合在修复 path/effect gate 后二次验证。
- **解决的问题**：替代让模型直接拼 SVG/HTML、依赖 Mermaid 默认布局、发生几何错误时全量重写，以及把“进程 exit 0”误当成可交付 artifact 的旧做法。Archify 用五种 schema、稳定 ID、结构化诊断、确定性 renderer、最后产物检查和 receipt 把模糊设计判断包进机械验证外壳。

#### 基本信息与可验证来源

- URL：https://github.com/tt-a1i/archify
- GitHub API：**Stars 17,833；Forks 1,236；Language HTML；License MIT**。
- API 时间字段：`updated_at=2026-08-26T23:31:08Z`，`pushed_at=2026-08-26T14:10:32Z`，`open_issues_count=30`（GitHub 该字段含 PR），default branch `main`。
- 固定提交：[`8b542d60e5eb2c552a3bb5bc1651d076be312aec`](https://github.com/tt-a1i/archify/commit/8b542d60e5eb2c552a3bb5bc1651d076be312aec)。
- Release：[`v2.15.0`](https://github.com/tt-a1i/archify/releases/tag/v2.15.0)，发布于 2026-08-17；固定提交 package version 是 `2.16.0-dev.0`，不可混称 stable `v2.16`。
- README/docs：README 说明五种 diagram、typed IR、atomic validation、last-good preview、source evidence；`archify/SKILL.md` 给出 artifact-first、validate/deliver contract；`DESIGN.md` 明确 authored facts 与 viewer-only state 的边界。
- Issues：GitHub Search API 返回 20 个 open issues（排除 PR）；本次重点核验 [#124](https://github.com/tt-a1i/archify/issues/124) CLI output overwrite、[#126](https://github.com/tt-a1i/archify/issues/126) workflow 非均匀列间距。
- 本机验证：doctor 通过；showcase example 9/9 checks；完整 suite 709 pass / 3 fail / 16 skip；隔离 `/tmp` fixture 复现 #124。

#### 架构 / 实现与数据流

```text
plain-language requirement / repository evidence
                     |
                     v
Agent reads one schema + one example
                     |
                     v
         typed JSON IR (stable IDs)
architecture | workflow | sequence | dataflow | lifecycle
                     |
                     v
     generated standalone validator
schema path + subject identity + supportedFixes
                     |
                     v
 renderer + geometry/layout/composition checks
                     |
             candidate HTML in
       target-adjacent staging directory
                     |
                     v
 check-render-output.mjs (9 showcase checks)
                     |
                     v
 SHA-256/bytes/validation/source-evidence receipt
                     |
                     v
 same-filesystem rename -> requested output
                     |
             optional visual-check
       containment/captures; review=pending
```

实现上应区分五层：

1. **Authoring contract**：`SKILL.md` 控制 agent 先写 candidate、每轮只修 diagnosed subject、最多聚焦修复；这是 prompt/skill 层，不是 hard security boundary。
2. **Typed IR**：`schemas/*.schema.json` 与 generated validators 约束字段、枚举、ID、placement；valid 只证明 shape，不证明架构事实真实。
3. **Renderer/composition**：每种 diagram 有独立 renderer，共享 geometry、legend、text-fit、diagnostics 与 viewer template；showcase profile 增加 clearances、crossing、corridor、readability gates。
4. **Delivery envelope**：冻结 specification bytes，在 target 同目录创建 candidate，render/check/readback/hash 后 rename；render/check 失败会保留旧 artifact。
5. **Truth boundary**：viewer search/reach/story/lens 复用 authored topology；Architecture Delta 明确只比较 authored IR，不推断 runtime impact、risk 或 mergeability。

关键缺口位于第 4 层的 **effect target**：`resolveOutputPath()` 对 authored `meta.output` 有更严格约束，但 issue #124 与本机复现证明 CLI `requestedOutput` 可指向 `.env` 及 cwd 外绝对路径。即使 content validation、candidate staging、hash、rename 都正确，只要最终 target authority 错了，整个 delivery 仍然不安全。

#### Repo tree 摘要（固定提交）

```text
archify/
├── archify/
│   ├── SKILL.md                     # Agent authoring/repair/delivery 契约
│   ├── schemas/                     # 五类 JSON Schema + common schema
│   ├── renderers/
│   │   ├── architecture|workflow|...# 五类 renderer
│   │   └── shared/                  # validator/geometry/diagnostics/path/legend
│   ├── bin/archify.mjs              # render/validate/deliver/compare/doctor CLI
│   ├── delta/architecture-delta.mjs # canonical diff + exact change receipt
│   ├── scripts/check-render-output.mjs
│   ├── examples/                    # authoritative JSON examples与rendered fixtures
│   ├── test/                        # Node test suite
│   └── package.json                 # Node >=18；runtime zero-dependency intent
├── scripts/                         # release/archive/gallery/test runners
├── docs/                            # project page、guide、cases、assets
├── examples/                        # delivered HTML examples
├── benchmarks/                      # ordinary-model-floor fixtures/results
├── integrations/                    # opt-in host bundles
├── experiments/                     # 非主线实验
├── archify.zip                      # checked-in distribution archive
├── README.md / DESIGN.md / ROADMAP.md
└── LICENSE                          # MIT
```

固定提交有 439 个 tracked files，其中 `archify/` 165、`docs/` 142、`experiments/` 51；136 个 `.mjs`，`archify/test/` 下 81 个 `*.test.mjs`。这些数量来自 `git ls-tree`，不代表所有 browser/OS/release lane 在本机通过。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `archify/renderers/shared/validator.mjs` | typed schema gate | 选择 generated validator；把 JSON pointer 补上最近 node id/label；输出 `code/subject/evidence/supportedFixes` |
| `archify/bin/archify.mjs` | CLI 与 verified delivery | freeze spec、render candidate、check、readback、hash receipt、rename；但 CLI output scope 当前过宽 |
| `archify/renderers/shared/output-path.mjs` | output target resolution | issue #124 指出 authored meta 与 CLI requested output 的约束不一致 |
| `archify/renderers/architecture/render-architecture.mjs` | architecture layout/render | component/boundary measurement、viewBox、readability、route/collision validation |
| `archify/delta/architecture-delta.mjs` | exact authored diff | canonicalize order/set-like fields；stable ID diff；proofLevel；明确 limitations |
| `archify/scripts/check-render-output.mjs` | final artifact gate | single SVG、finite geometry、orthogonal arrows、clearance/corridor/rhythm/legend 等检查 |
| `archify/bin/visual-check.mjs` | browser evidence sidecar | 多 viewport containment + screenshots；始终把 visual review 标 pending |
| `archify/package.json` | 依赖与测试入口 | dev dependencies：AJV、parse5、saxes、simple-icons；Node >=18 |

#### ⭐ 源码精读

**代码块 1：`validateSchema()`——让 deterministic error 指向可局部修复的 subject**  
来源：[`archify/renderers/shared/validator.mjs#L38-L85`](https://github.com/tt-a1i/archify/blob/8b542d60e5eb2c552a3bb5bc1651d076be312aec/archify/renderers/shared/validator.mjs#L38-L85)

```javascript
export function validateSchema(diagramType, data) {
  const validate = validators[diagramType];
  if (!validate) {
    throw new Error(`validateSchema: unknown diagram type "${diagramType}"`);
  }
  if (!validate(data)) {
    const diagnostics = validate.errors.map((error) => {
      const annotated = annotatedPath(error.instancePath, data);
      return {
        code: `schema/${error.keyword}`,
        severity: 'error',
        message: `${annotatePath(error.instancePath, data)} ${error.message}`,
        subject: {
          diagramType,
          path: annotated.path,
          ...(annotated.identity != null ? { identity: String(annotated.identity) } : {}),
        },
        evidence: { keyword: error.keyword, expected: error.schema, ...error.params },
        supportedFixes,
      };
    });
    throwDiagnosticError('schema validation failed', diagnostics);
  }
}
```

逻辑摘要：schema failure 不只回 AJV message；`annotatedPath()` 沿 JSON pointer 找最近 `id/label`，将错误绑定 diagram type、path、identity，并给可支持修法。对 Agent 的关键价值是“只改 named subject”，减少全量重写造成的新错。边界：schema valid 不验证 source evidence 的事实正确性，也不验证最终 output target 是否获授权。

**代码块 2：`commandDeliver()`——冻结 bytes、候选旁路、检查后才生成 receipt**  
来源：[`archify/bin/archify.mjs#L846-L920`](https://github.com/tt-a1i/archify/blob/8b542d60e5eb2c552a3bb5bc1651d076be312aec/archify/bin/archify.mjs#L846-L920)

```javascript
// candidate beside target => same-filesystem commit
stagingDirectory = fs.mkdtempSync(
  path.join(outputDirectory, '.archify-delivery-')
);
const candidatePath = path.join(stagingDirectory, path.basename(outputPath));
const specificationSnapshotPath = path.join(
  stagingDirectory, 'specification.snapshot.json'
);

fs.writeFileSync(specificationSnapshotPath, specification, { flag: 'wx' });
const render = runNode(
  [renderer, specificationSnapshotPath, candidatePath],
  { stdio: 'pipe', env: rendererEnv(quality, repoRoot, true) }
);
if (render.status !== 0) return reportDeliveryFailure(/* render */);

const check = runNode(
  [path.join(skillRoot, 'scripts/check-render-output.mjs'), candidatePath],
  { stdio: 'pipe' }
);
if (check.status !== 0) {
  return reportDeliveryFailure({
    stage: 'check',
    error: 'Final artifact check failed; the previous artifact was preserved.'
  });
}
```

逻辑摘要：先把输入 bytes 冻结为私有 snapshot，renderer 永远读 frozen bytes；candidate 与 target 同目录，render/check 失败不碰 last-good。这是可迁移的 verified publish envelope。边界：如果 `outputPath` 一开始就选错，即使 candidate 完全有效，最终成功 commit 仍是高质量的错误副作用。

**代码块 3：receipt + commit——content identity 完整，但 target authority 不完整**  
来源：[`archify/bin/archify.mjs#L1005-L1068`](https://github.com/tt-a1i/archify/blob/8b542d60e5eb2c552a3bb5bc1651d076be312aec/archify/bin/archify.mjs#L1005-L1068)

```javascript
const receipt = {
  schemaVersion: 1,
  ok: true,
  command: 'deliver',
  type,
  input: inputPath,
  output: outputPath,
  specification: {
    sha256: createHash('sha256').update(specification).digest('hex'),
    bytes: specification.byteLength,
  },
  artifact: {
    sha256: createHash('sha256').update(artifact).digest('hex'),
    bytes: artifact.byteLength,
  },
  validation: {
    checksPassed: result.checks.filter((item) => item.ok).length,
    checkCount: result.checks.length,
    compositionStatus: result.composition.status,
    errors: result.composition.summary.errors,
    warnings: result.composition.summary.warnings,
  },
};

// after a second path resolution check
fs.renameSync(candidatePath, outputPath);
```

逻辑摘要：receipt 能证明本次 specification/artifact bytes 与 validation summary；rename 是同文件系统单文件 commit。#124 的本机复现说明第二次 resolution 仍接受 CLI 指定的 `/tmp/.../marker.env`，所以 receipt 证明“写进去的 HTML 是哪份”，却不证明“允许覆盖这个目标”。迁移时必须给 receipt 再加 `canonical_target/target_type/allowed_root/previous_hash/effect_grant`。

**代码块 4：`compareArchitecture()`——只比较 authored IR，不冒充 runtime impact**  
来源：[`archify/delta/architecture-delta.mjs#L226-L317`](https://github.com/tt-a1i/archify/blob/8b542d60e5eb2c552a3bb5bc1651d076be312aec/archify/delta/architecture-delta.mjs#L226-L317)

```javascript
export function compareArchitecture(base, head, evidence = {}) {
  requireComparableShape(base, 'base');
  requireComparableShape(head, 'head');
  const baseComponents = stableIndex(base.components, 'components', 'base');
  const headComponents = stableIndex(head.components, 'components', 'head');
  const shared = sorted(
    [...baseComponents.keys()].filter((id) => headComponents.has(id))
  );
  if (!shared.length) {
    fail('delta/no-shared-component-id',
      'The snapshots share no component id...');
  }
  // components/connections/boundaries exact field classifications...
  return {
    schemaVersion: 1,
    ok: true,
    proofLevel,
    changes: { components, connections, boundaries },
    limitations: [
      'Authored Architecture IR only; no runtime impact, causality, risk, or mergeability is inferred.',
      'Boundary identity is conservatively derived from kind + label.',
    ],
  };
}
```

逻辑摘要：stable ID 不匹配会 fail closed；semantic/evidence/geometry/topology 分类分开；receipt 主动写 limitations。这个“projection 不冒充更强事实”的做法适合 shared derived views。边界：authored IR 仍可能由模型写错，revision-pinned source evidence也只验证引用，不自动证明所有架构关系完整。

#### 依赖分析与供应链风险

- `archify/package.json` 的 Node engine 是 `>=18`；运行时代码主要使用 Node built-ins，四个声明依赖全部是 devDependencies：`ajv ^8.17.1`、`parse5 7.3.0`、`saxes 6.0.0`、`simple-icons 16.28.0`。
- `npm audit --omit=dev` 真实返回 0 known advisories；这只说明当前 package 的 production dependency closure 极窄，不覆盖 checked-in ZIP、DSH bundle、Node runtime、browser、remote brand capture、GitHub Pages 或用户输入。
- 含 dev dependencies 的 `npm audit` 真实返回 1 high：transitive `fast-uri`（AJV lane）受 `GHSA-v2hh-gcrm-f6hx` 与 `GHSA-7p8r-x3mc-p8w7` 影响，fix available。它主要进入 schema build/dev lane，具体 runtime reachability 待核验；不能因为是 dev 就忽略 release generator/CI 风险。
- 完整 suite 的 3 个失败来自缺 `zip`/`unzip`，说明“zero-dependency skill runtime”与“完整 release/archive validation”是不同 prerequisite lane。
- remote brand capture 会访问 URL 并处理图片；源码/tests 展示 SSRF、digest、content type、防 SVG 等保护，但本次没有对真实互联网 icon 执行安全测试。相关网络/DNS TOCTOU 与 decompression 风险待核验。
- `archify.zip` 是 checked-in binary artifact；本次未重建并比对 archive digest，因为本机缺 zip/unzip，故 package reproducibility 待核验。

#### README / docs / release / issues / 源码交叉结论

- README 的“atomic validation before delivery”对 content/candidate 成立；issue #124 与真实复现证明它**不等于 arbitrary target safe**。必须区分 artifact integrity 与 effect authorization。
- `SKILL.md` 要求 `deliver` 作为 final acceptance，并明确 non-zero 不能称 success；本次危险路径恰恰返回 exit 0/ok=true，因此单靠 skill prose 无法挡住 target bug。
- README 与源码都强调 last-good preservation；issue #126 提醒：失败后马上跑 visual-check 可能检查的是旧 artifact。后续 receipt 应包含 candidate/committed generation identity，consumer 必须绑定本次 artifact hash。
- v2.15.0 release 包含 brand capture、DSH、quality flag 等变化；固定 HEAD 已到 2.16 dev 并新增更多校验。高频迭代要求 pin commit/tag，不能把 main behavior 当 stable contract。
- GitHub Actions 最近既有 success，也有 `action_required` 和 DSH integration failure；CI 列表不能简化成“全部绿色”。

#### 可复用经验

- 当生成器已经拥有 schema、diagnostics、hash 和 atomic rename 时，应优先继续在最终 commit 前验证 canonical target、extension、allowed root、existing target type 与 effect grant，因为 artifact 正确不能补救写错位置；边界是 path containment 还要防 symlink/replacement race。
- 当确定性校验失败时，应优先把错误绑定稳定 `code + subject + evidence + supportedFixes` 并只修局部对象，因为 Agent 全量重写会放大变化面；边界是 supported fix 不能删除有语义的信息来骗过几何 gate。
- 当 output 有 last-good preservation 时，应优先让后续 visual/audit 消费本次 receipt 中的 committed hash，而不是只看固定文件路径，因为失败后路径可能仍指向旧版本；边界是 hash 仍需和授权 target 绑定。
- 当 derived interaction 只能证明 authored topology 时，应优先在 receipt 中显式写“不推断 runtime impact/risk/mergeability”，因为 UI 的 reach/delta 很容易让读者误读为动态事实；边界是若要更强结论必须接独立 code/runtime evidence。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/scoped-artifact-delivery/` 做纯 Python/Node synthetic fixture，不复制上游 viewer：

1. 输入 `candidate bytes + requested relative path + allowed root + expected extension + prior hash`。
2. 在 allowed root 同文件系统 staging 中写候选，执行 content checker/readback/hash。
3. commit 前重新 `realpath` parent，拒绝绝对越界、symlink、directory、非目标扩展、未授权 existing file；已存在文件必须匹配 previous hash 或显式 create-only/replace grant。
4. 注入 `../marker.env`、absolute outside root、symlink swap、checker fail、readback mismatch、last-good exists、concurrent replacement fixtures。
5. 输出 `prepared|blocked|committed|failed` receipt，并验证下游只能消费本次 committed hash；不触碰 Hermes config、skills、cron、curated 或用户文件。

#### 风险边界

- **License**：GitHub API、`package.json`、`SKILL.md` 与根 `LICENSE` 均为 MIT；上游还注明 based on 一个 MIT 项目。品牌图标、remote icon、simple-icons、示例仓库和用户输入另有许可/商标边界。
- **维护活跃度**：API 显示查询前约 9 小时 pushed；latest release 约 10 天前；HEAD 是 dev version，变化快且近期 Actions 非全绿。
- **安全风险**：#124 的任意 output overwrite 已本机复现；remote brand capture 涉及 SSRF/content parsing；self-contained HTML 仍可能承载不受信 authored text；CLI/skill 可被 prompt injection 引导选择危险 path。
- **局限性**：本机缺 zip/unzip，完整 suite 3 fail；16 个 browser regressions skip；未做真实 Chrome visual review、Windows/macOS、DSH、remote brand、release archive reproducibility。
- **不适用场景**：不能把 Archify delta 当 runtime impact；不能让无人值守 Agent 自由指定 output；不能把 HTML/SVG artifact 直接当 curated fact；不能从漂亮图形推导 source coverage。
- **不能自动执行**：不安装 Archify skill，不修改 Hermes/OpenClaw skills/config，不在 shared 外写用户文件，不抓取未知品牌 URL，不把 candidate 写 curated active facts。

#### ⭐ Skill 升格判断

**暂不沉淀。** 完整 Archify skill 当前存在已真实复现的 CLI output target 缺口，且 release/archive lane未全绿，不应直接复制到 `capabilities/skills/`。更窄的 agent-neutral `scoped-artifact-delivery` 模式为 **需二次验证**：先做 target authority、generation hash、last-good 和 symlink fixtures，再与现有 verification-first / path-portability / completion receipt 能力去重。今天不创建 shared skill、不修改 manifest。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/scoped-artifact-delivery/{contract.json,gate.py,fixtures/,test_gate.py,README.md}`。
2. **Hermes 学习审计**：未来可让 `scripts/github_learning_orchestrator.py` 在复制 KB 前绑定 report source hash、destination allowed root、prior hash 与 copy readback；本次不改 orchestrator。
3. **shared 分层**：source report 仍在 `inbox/hermes/daily/`；diagram/HTML、candidate、screenshots、checks 均放 `runtime/hermes/`，不能进入 curated truth。
4. **路径可迁移**：contract 只记录 resolver 后的 shared-relative path；不得把 `/home/vany/...` 写进跨机器 skill/prefill。
5. **未来 OpenClaw adapter**：当前不存在且本次不实现；若未来接入，只复用 agent-neutral receipt schema，由 OpenClaw 自身 loader/effect gate 证明 allowed root 和 readback，不能共享 Hermes 的绝对路径或 grant。

### 2. browser-use/browser-use

- **一句话判断**：Browser Use 值得学的是把浏览器自动化拆成 state capture、LLM decision、typed action registry、EventBus/CDP effect、timeouts、page-change guards 与 history/judge，而不是把“浏览器控制”做成一个万能 tool；但固定 HEAD 仍有 domain-policy bypass、timeout step accounting、phantom file state 与 false tab-success 等 open gaps，所以完整产品/skill 暂不进入 Hermes/shared。
- **解决的问题**：替代仅用 HTTP 抓取无法处理交互页面、让模型直接生成脆弱 Playwright selector/script、一次模型调用规划整个长任务，以及把浏览器异常/页面变化吞成自然语言的旧做法。它每步重新采集 DOM/AX/screenshot，用 Pydantic action schema约束工具调用，再经 BrowserSession/EventBus/CDP执行并写 history。

#### 基本信息与可验证来源

- URL：https://github.com/browser-use/browser-use
- GitHub API：**Stars 110,949；Forks 12,184；Language Python；License MIT**。
- API 时间字段：`updated_at=2026-08-26T23:30:09Z`，`pushed_at=2026-08-26T18:41:37Z`，`open_issues_count=383`（含 PR），default branch `main`。
- 固定提交：[`28670f720f63cc5f525a2acd6d6072867689ab68`](https://github.com/browser-use/browser-use/commit/28670f720f63cc5f525a2acd6d6072867689ab68)，commit message `fix(deps): bump dependency versions (#5382)`。
- Release：[`0.13.8`](https://github.com/browser-use/browser-use/releases/tag/0.13.8)，发布于 2026-08-16T18:48:54Z；固定 HEAD 晚于 release。
- README/docs：README 区分 agent CLI 与 Python library，展示 `Agent(task,llm)`、custom tools、local/cloud；仓库 `AGENTS.md` 提供 development contract；`.github/SECURITY.md` 要求 private advisory。
- Issues/PR：[#4763](https://github.com/browser-use/browser-use/issues/4763)、[#5513](https://github.com/browser-use/browser-use/issues/5513)、[#5521](https://github.com/browser-use/browser-use/pull/5521)、[#5524](https://github.com/browser-use/browser-use/issues/5524)、[#5527](https://github.com/browser-use/browser-use/issues/5527)、[#5529](https://github.com/browser-use/browser-use/issues/5529)、[#5543](https://github.com/browser-use/browser-use/issues/5543)、[#5555](https://github.com/browser-use/browser-use/pull/5555) 查询时均 open。
- 本机验证：compileall 成功；清理 proxy env 后两个聚焦 test files 为 26 passed；没有启动 Chrome、没有调用任何 LLM/provider/cloud、没有使用真实 credential/profile。

#### 架构 / 实现与数据流

```text
user task + optional policy/skills/sensitive placeholders
                         |
                         v
Agent.run() starts BrowserSession + watchdogs + skill actions
                         |
                 per-step loop
                         |
       BrowserSession.get_browser_state_summary()
       DOM/AX snapshot + selector map + screenshot + tabs
                         |
                         v
 MessageManager: prior results + state + available actions
                         |
                         v
     LLM -> Pydantic AgentOutput[action[]]
                         |
                         v
 Agent.multi_act(): stop/pause + stale-page guards
                         |
                         v
 Tools.act() -- per-action asyncio timeout
                         |
                         v
 Registry.execute_action()
 params validation + injected BrowserSession/FileSystem/LLM context
                         |
                         v
 BrowserSession EventBus -> watchdogs -> CDP actions
 navigate/click/input/scroll/download/tab/etc.
                         |
                         v
 ActionResult -> history -> plan/loop detector/judge/terminal
```

核心模块分成七层：

1. **Agent loop**：每 step 做 prepare context、LLM output、multi-action execution、post-process、finalize；run loop管理 max steps、failures、callbacks、judge 与 cleanup。
2. **State plane**：BrowserSession 维护 target/session/focus/cache；DOM service合并 DOM snapshot、AX tree、iframes、visibility 和 clickable elements。
3. **Decision plane**：MessageManager 将 state、actions、history、skills、plan、budget/loop signals组成模型输入；LLM不直接持有 CDP client。
4. **Action contract**：Registry从函数签名生成 Pydantic param model，识别 special injected dependencies，domain-filter actions并标准化 sync/async函数。
5. **Effect plane**：Tools.act加 per-action timeout；BrowserSession/EventBus/watchdogs执行 CDP事件；multi_act在静态 `terminates_sequence` 与实际 URL/focus 变化后停止剩余 action。
6. **Security plane**：allowed/prohibited domains、IP blocking、domain-scoped secret replacement、file path availability、security watchdog。问题是这些局部规则还没有形成统一 effect/authority receipt。
7. **Observability/terminal**：ActionResult、history、telemetry、token cost、judge、callbacks；但 open issues证明“返回 success prose”与真实 effect/readback仍可能漂移。

#### Repo tree 摘要（固定提交）

```text
browser-use/
├── browser_use/
│   ├── agent/
│   │   ├── service.py                # Agent step/run/multi_act主循环
│   │   ├── message_manager/          # history/state/model messages
│   │   ├── prompts.py + system_prompts/
│   │   └── views.py                  # AgentOutput/ActionResult/history schemas
│   ├── browser/
│   │   ├── session.py                # target/session/EventBus/CDP lifecycle
│   │   ├── events.py                 # typed browser events
│   │   ├── profile.py                # domains/security/browser settings
│   │   └── watchdogs/                # DOM/security/download/crash/etc.
│   ├── dom/                          # snapshot、AX、serializer、clickable detection
│   ├── tools/
│   │   ├── service.py                # built-in tools + timeout + ActionResult
│   │   └── registry/                 # action registration/param validation/dispatch
│   ├── llm/                          # provider-neutral BaseChatModel + adapters
│   ├── filesystem/                   # Agent file state与disk sync
│   ├── skills/                       # browser-use skill service/bundle
│   ├── mcp/                          # MCP client/server/controller
│   ├── sandbox/ sync/ telemetry/     # cloud/sync/observability side planes
│   └── cli.py
├── tests/                             # 111 tracked paths；100 test files
├── examples/                          # 124 tracked examples
├── skills/                            # host-facing skill bundles
├── docker/ + Dockerfile*             # runtime images
├── pyproject.toml                     # exact dependency pins + optional groups
├── README.md / AGENTS.md / CLOUD.md
└── LICENSE                            # MIT
```

固定提交有 494 tracked files，`browser_use/` 184、`examples/` 124、`tests/` 111、`skills/` 27；这些统计不能证明 cloud、Chrome、各 LLM provider 与 host skill 均已实测。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `browser_use/agent/service.py` | Agent orchestration | step phases、LLM timeout、run loop、multi_action stale-page guards、history/judge |
| `browser_use/browser/session.py` | browser control plane | Pydantic profile/session、EventBus、CDP target/session、local/cloud兼容、reconnect |
| `browser_use/dom/service.py` | state extraction | DOM snapshot + AX + iframe + visibility + clickability；并发收集子 frame AX |
| `browser_use/tools/registry/service.py` | typed action registry | signature normalization、Pydantic model、special dependency injection、domain restriction |
| `browser_use/tools/service.py` | built-in actions/effect timeout | 180s action cap、ActionResult normalization、search/find JS safety injection |
| `browser_use/browser/watchdogs/security_watchdog.py` | URL policy enforcement | navigation前/redirect后/new-tab checks；但 data/blob 当前无条件 allow |
| `browser_use/filesystem/file_system.py` | Agent-visible file persistence | issue #5527 报告 sync失败后内存仍保留 phantom state |
| `browser_use/llm/*` | provider adapters | exact provider pins与参数序列化；#5543/#5555说明 substring classifier边界 |
| `pyproject.toml` | dependency/supply chain | 近 40 个 exact direct pins，包含 browser、MCP、PDF、LLM SDK、telemetry |

#### ⭐ 源码精读

**代码块 1：`Agent.step()`——每步重新取 state，再让 LLM 决策并执行**  
来源：[`browser_use/agent/service.py#L1027-L1079`](https://github.com/browser-use/browser-use/blob/28670f720f63cc5f525a2acd6d6072867689ab68/browser_use/agent/service.py#L1027-L1079)

```python
@observe(name='agent.step', ignore_output=True, ignore_input=True)
@time_execution_async('--step')
async def step(self, step_info: AgentStepInfo | None = None) -> None:
    self.step_start_time = time.time()
    browser_state_summary = None
    try:
        # Phase 0: optional captcha wait/result injection
        browser_state_summary = await self._prepare_context(step_info)

        # Clear stale previous-step state before this LLM/action phase
        self.state.last_model_output = None
        self.state.last_result = None

        await self._get_next_action(browser_state_summary)
        await self._execute_actions()
        await self._post_process()
    except Exception as e:
        await self._handle_step_error(e)
    finally:
        await self._finalize(browser_state_summary)
```

逻辑摘要：LLM 不一次规划完整 browser script；每 step 先重新 capture state，然后生成 action[]，执行后再 history/finalize。清掉 stale output/result 可避免当前 step timeout沿用上一轮假状态。边界：finally 与外层 timeout cancellation交互复杂，#5513 正说明 step counter不能靠推断式补偿。

**代码块 2：Registry——从函数签名生成 action schema，并在调用前验证 params**  
来源：[`browser_use/tools/registry/service.py#L291-L395`](https://github.com/browser-use/browser-use/blob/28670f720f63cc5f525a2acd6d6072867689ab68/browser_use/tools/registry/service.py#L291-L395)

```python
def action(self, description: str, param_model=None,
           domains=None, allowed_domains=None,
           terminates_sequence: bool = False):
    def decorator(func):
        if func.__name__ in self.exclude_actions:
            return func
        normalized_func, actual_param_model = (
            self._normalize_action_function_signature(
                func, description, param_model
            )
        )
        self.registry.actions[func.__name__] = RegisteredAction(
            name=func.__name__,
            description=description,
            function=normalized_func,
            param_model=actual_param_model,
            domains=final_domains,
            terminates_sequence=terminates_sequence,
        )
        return normalized_func
    return decorator

async def execute_action(self, action_name: str, params: dict, **context):
    action = self.registry.actions[action_name]
    validated_params = action.param_model(**params)
    special_context = {
        'browser_session': context.get('browser_session'),
        'page_extraction_llm': context.get('page_extraction_llm'),
        'file_system': context.get('file_system'),
        # ...
    }
    return await action.function(params=validated_params, **special_context)
```

逻辑摘要：action declaration 同时形成 param model、description、domain metadata、sequence effect；执行时模型参数先通过 Pydantic，BrowserSession/FileSystem等能力由 host 注入，不让模型自己构造。可迁移点是“typed proposal + host-injected authority”。边界：metadata/dependency injection仍需最终 effect gate；`terminates_sequence`是声明，不足以证明真实页面/文件效果。

**代码块 3：`Tools.act()`——给每个 effect 加 wall-clock terminal，统一 ActionResult**  
来源：[`browser_use/tools/service.py#L2168-L2255`](https://github.com/browser-use/browser-use/blob/28670f720f63cc5f525a2acd6d6072867689ab68/browser_use/tools/service.py#L2168-L2255)

```python
async def act(self, action: ActionModel, browser_session: BrowserSession,
              action_timeout: float | None = None, **context) -> ActionResult:
    timeout_s = _coerce_valid_action_timeout(action_timeout)
    for action_name, params in action.model_dump(exclude_unset=True).items():
        if params is not None:
            try:
                result = await asyncio.wait_for(
                    self.registry.execute_action(
                        action_name=action_name,
                        params=params,
                        browser_session=browser_session,
                        **context,
                    ),
                    timeout=timeout_s,
                )
            except BrowserError as e:
                result = handle_browser_error(e)
            except TimeoutError:
                result = ActionResult(
                    error=f'Action {action_name} timed out after {timeout_s:.0f}s.'
                )
            except Exception as e:
                result = ActionResult(error=str(e))

            if isinstance(result, str):
                return ActionResult(extracted_content=result)
            if isinstance(result, ActionResult):
                return result
            if result is None:
                return ActionResult()
            raise ValueError(f'Invalid action result type: {type(result)}')
```

逻辑摘要：inner CDP/event wait不一定都有 timeout，所以最外层每个 action 再加 hard cap；各种 handler output被规范化成 ActionResult。聚焦 tests 5 个 action-timeout case 实测通过。边界：timeout只保证“返回”，不能证明被 cancel 的副作用完全停止；对 click/download/file write等需 action-specific observation/readback/idempotency。

**代码块 4：`SecurityWatchdog._is_url_allowed()`——allowlist 前的 data/blob 例外形成 bypass**  
来源：[`browser_use/browser/watchdogs/security_watchdog.py#L176-L218`](https://github.com/browser-use/browser-use/blob/28670f720f63cc5f525a2acd6d6072867689ab68/browser_use/browser/watchdogs/security_watchdog.py#L176-L218)

```python
def _is_url_allowed(self, url: str) -> bool:
    if url in ['about:blank', 'chrome://new-tab-page/',
               'chrome://new-tab-page', 'chrome://newtab/']:
        return True

    parsed = urlparse(url)

    # Current fixed-commit behavior
    if parsed.scheme in ['data', 'blob']:
        return True

    host = parsed.hostname
    if not host:
        return False

    if self.browser_session.browser_profile.block_ip_addresses:
        if self._is_ip_address(host):
            return False

    if (not self.browser_session.browser_profile.allowed_domains
            and not self.browser_session.browser_profile.prohibited_domains):
        return True
    # then exact/glob allow/prohibit matching...
```

逻辑摘要：普通 URL 会做 hostname、IP 与 allow/prohibit checks，历史 HTTP-auth bypass也已有测试和 advisory fix；但 `data:`/`blob:` 在这些 checks 前直接 True。Issue #4763 给出 prompt-injection/exfiltration场景。即使后续 redirect event可能检测外域，`data:` 页面本身已能执行内容或诱导输入，不能视为安全 allowlist。边界：修复不能简单禁止所有 blob；同源 blob需要解析内嵌 origin并逐 effect 验证。

**代码块 5：`multi_act()`——静态 effect 声明之外再观察 URL/focus 变化**  
来源：[`browser_use/agent/service.py#L2731-L2831`](https://github.com/browser-use/browser-use/blob/28670f720f63cc5f525a2acd6d6072867689ab68/browser_use/agent/service.py#L2731-L2831)

```python
async def multi_act(self, actions: list[ActionModel]) -> list[ActionResult]:
    for i, action in enumerate(actions):
        pre_action_url = await self.browser_session.get_current_page_url()
        pre_action_focus = self.browser_session.agent_focus_target_id

        result = await self.tools.act(
            action=action,
            browser_session=self.browser_session,
            # host context injected here
        )
        results.append(result)
        if result.is_done or result.error or i == len(actions) - 1:
            break

        registered = self.tools.registry.registry.actions.get(action_name)
        if registered and registered.terminates_sequence:
            break

        post_url = await self.browser_session.get_current_page_url()
        post_focus = self.browser_session.agent_focus_target_id
        if post_url != pre_action_url or post_focus != pre_action_focus:
            break
```

逻辑摘要：一个 LLM step可给多个 action，但 navigation类声明会立即终止队列，且任何实际 URL/focus变化也会阻止继续用 stale DOM。模式是“declaration + observation 双层 guard”。边界：URL/focus不变不代表 DOM/revision没变；click后 AJAX rerender、permission dialog、download、文件写入仍需各自 revision/effect receipt。

#### 依赖分析与供应链风险

- `pyproject.toml` 要求 Python `>=3.11,<4.0`，对近 40 个 direct packages采用 exact pins。核心涉及 `aiohttp/httpx/requests`、`bubus`、`pydantic`、OpenAI/Anthropic/Google/Groq/Ollama SDK、MCP、CDP、PDF/Docx/reportlab/Pillow、telemetry、Google OAuth、TOTP 与 browser harness；authority/data surface远大于简单 Playwright wrapper。
- 固定 HEAD 已将 `mcp` 提升到 `1.28.1`，但 Click 仍是 `8.3.1`、pypdf仍是 `6.14.2`。Issue #5524 所列 Click 与 pypdf advisories仍与当前 pins相符。
- 本机 environment-level `pip-audit --path` 找到 21 records / 6 packages：Click、cryptography、pydantic-settings、pypdf、Starlette、pytest。重复 advisory records来自环境扫描输出；pytest是dev，其他包可在 runtime/transitive路径出现。可达性与升级兼容性待逐 lane核验。
- requirements-level audit 因 index 无法提供 `portalocker==4.3.0` 而 blocked，不能把 path audit当完整 reproducible closure；仓库无 checked-in lock也让每日 main resolution漂移。
- `uv sync` 解析 400 packages、当前平台安装 193 packages；大量 provider/OS markers与optional extras说明“只用本地 Chrome + 一个 LLM”也承受很大的 published dependency metadata。
- Dependabot API 403；repository advisory只返回项目自身历史 advisory，不覆盖所有 transitive advisories。
- Telemetry与cloud/browser sync是独立数据出口；本次未放入任何 key、cookie、profile或用户数据，也未验证 opt-out/retention。

#### README / docs / release / issues / 源码交叉结论

- README 宣称可给 Hermes/OpenClaw 等 agent 安装 skill；本次没有执行安装，因为安装会修改 agent 能力面，且当前任务明确禁止调用 OpenClaw。README兼容列表不等于当前 Hermes loader/security policy已验证。
- README 的 domain-scoped `sensitive_data` 模式有价值；#4763 与固定源码证明 allowed_domains 当前不是完整边界。带 secret 的浏览任务不应只依赖它。
- `Tools.act()` 与 tests证明 per-action timeout工作；#5513 与固定 `Agent._execute_step()` 说明 outer step timeout cancellation的 accounting仍可能双增。局部 timeout正确不等于整个 loop terminal正确。
- release 0.13.8 已修很多 DOM/MCP/security pins，并加入 first-party OpenClaw skill；固定 HEAD又有 dependency bump。快速演进意味着要 pin commit并复验 host adapter，不可按 README最新示例猜稳定 API。
- #5527 与 Archify #124 指向同一更广模式：文件/target副作用必须以 disk/readback为事实，内存 state/ok receipt若未绑定 observed effect会产生“幻影成功”。
- #5529 与 #5543 指向另一模式：自然语言 success和字符串 heuristic不应决定真实 control state；应读取 handler result与非空 validated pattern。
- GitHub Actions 最近 main commit的 CLI install与 dependency graph update显示 success，PR lint/test也有 success；但这不能覆盖真实 Chrome/LLM/provider、所有 OS、dependency advisories或上述 open issues。

#### 可复用经验

- 当 LLM action需要 BrowserSession/FileSystem/LLM client等高权能力时，应优先由 host按 typed schema注入最小 special context，而不是让模型构造连接或路径，因为 proposal与authority必须分离；边界是注入后仍要在最终 handler重验 scope/effect。
- 当一个 step批量执行多个 UI action时，应优先同时使用静态 `terminates_sequence` 和实际 URL/focus/DOM revision观察，因为声明可能漏标、页面也可能意外变化；边界是 URL不变的 SPA仍需 DOM generation guard。
- 当 action或step加 timeout时，应优先记录 start generation、cancellation outcome、observed effect与exactly-once counter update，因为“wait_for返回TimeoutError”不证明 cleanup没有推进状态；边界是外部网站副作用通常不可回滚。
- 当 browser policy依赖 domain allowlist时，应优先逐 scheme、每次 redirect/new-tab、DNS/IP与 opaque-origin URL重验，因为 `data:`/`blob:`/auth-userinfo等特殊 URL会绕开朴素 host判断；边界是同源 blob与下载 URL需单独策略。
- 当文件 API 返回 error时，应优先 rollback内存 candidate并从 disk readback最后持久状态，因为内存对象不应冒充已经写盘；边界是跨进程还需 revision/lock，单进程 rollback不够。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/action-effect-envelope/` 做不启动浏览器的纯 fixture：

1. 定义 action schema：`name/params/requested_effect/target_scope/start_revision/deadline`；host注入 grant，而非模型给 grant。
2. fake handler支持 URL navigation、SPA DOM revision、file write、new-tab switch、timeout cancellation；每个返回 `attempted/observed_effect/readback/terminal`。
3. 注入 `data:` URL、redirect外域、URL不变但DOM revision变化、timeout cleanup已计数、disk write fail但memory changed、tab switch no result。
4. gate要求 exactly-one terminal、counter只增一次、scope重验、success必须有 effect-specific readback；否则 `blocked|failed|partial`。
5. 只用 synthetic state，不连接 Chrome/provider/MCP，不读取 cookie/secret，不改 Hermes/OpenClaw配置。

#### 风险边界

- **License**：GitHub API、`pyproject.toml` 与根 `LICENSE` 均指向 MIT；browser binaries、LLM provider SDK/services、CDP、MCP、PDF/doc素材、cloud服务与 examples另有条款。
- **维护活跃度**：API 显示查询前约 5 小时 pushed；release 约 11 天前；open issue search有 112 个 issue、repository field有 383 issues+PRs，迭代快且未关闭 gaps较多。
- **安全风险**：prompt injection可驱动浏览器；#4763 domain bypass；真实 profile/cookie/secret输入；download/file upload；MCP/custom tools；cloud/browser sync；telemetry；PDF/doc parsing；provider内容出域。
- **依赖风险**：path audit 21 records/6 packages；requirements audit blocked；无 checked-in uv.lock；exact pins使 downstream难以自动选择 fixed versions。
- **局限性**：只跑 26 个聚焦 tests和compileall；没有运行完整 suite、Chrome、DOM真实站点、LLM、judge、cloud、proxy、captcha、MCP、file upload/download、Windows/macOS。
- **已知 open gaps**：#4763、#5513/#5521、#5527、#5529、#5543/#5555 均未在固定 HEAD合并关闭；不能用 main CI success覆盖。
- **不适用场景**：高价值账户交易、无人监督发布/删除、处理明文凭据、要求强浏览器隔离、多租户共享 profile、将网页内容直接写 curated truth。
- **不能自动执行**：不安装 browser-use skill，不连接用户 Chrome/profile，不设置任何 API key，不启动 cloud/MCP，不上传/download文件，不修改 Hermes/OpenClaw config/auth/env/skills/cron。

#### ⭐ Skill 升格判断

**暂不沉淀。** 完整 Browser Use skill涉及浏览器、secret、network、MCP、cloud与本地文件等高权面，且固定 HEAD仍有已核验的 open security/consistency gaps；不适合直接进入 shared skills。更窄的 `action-effect-envelope` 为 **需二次验证**：先用离线 fixtures验证 typed proposal、host grant、scheme/revision guard、timeout exactly-once与readback，再与现有 effect-scope / terminal contract / verification-first候选去重。今天不安装产品、不创建 shared skill。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/action-effect-envelope/{schema.json,engine.py,fixtures/,test_engine.py,README.md}`，只实现 agent-neutral contract。
2. **Hermes tools/audit**：未来给 network/file/browser-like tools统一补 `requested_effect + scoped grant + observed effect + terminal receipt`；不依赖 Browser Use runtime。
3. **shared memory**：网页/工具 raw evidence进入 `inbox/hermes/daily/` 或 `runtime/hermes/`；外部页面 prose不能直接生成 curated user fact。
4. **secrets**：只允许 secret placeholder name进入报告/receipt；真实值保留 Hermes本地 credentials，不进入 shared。
5. **未来 OpenClaw adapter**：当前不存在且本次不调用；未来若接入同一 schema，必须由其自身 browser/plugin loader证明 grant、scheme policy、DOM generation与readback，不能因为 Browser Use README列出 OpenClaw就默认兼容。

## 经验沉淀

1. 当 Agent 产生文件、网页操作、消息或其他副作用时，应优先把 `typed proposal` 与 `host-owned authority` 分开，并在最终 chokepoint重验 canonical target、scope、effect与revision，因为 schema-valid content仍可能写到错误对象；边界是 host policy本身也需 adversarial fixtures。
2. 当 pipeline已有 candidate、validation、hash与atomic rename时，应优先继续验证 target authorization和 prior state，而不是把 content integrity当成effect safety，因为 Archify #124证明“每个字节都正确”仍可安全地覆盖错误文件；边界是跨进程需要 lock/CAS，单文件 rename不够。
3. 当 action或step使用 timeout/cancellation时，应优先记录 start generation、cleanup是否推进、counter exactly-once和 observed effect，因为 timeout signal不等于副作用未发生；边界是外部不可逆效果必须设计幂等键或人工确认。
4. 当批量 UI actions共享一个页面快照时，应优先在每个 action后检查声明式 page-changing flag与实际 URL/focus/DOM revision，因为 stale selector会把后续合法 action施加到新页面；边界是复杂页面还需 frame/session generation。
5. 当 browser/network allowlist保护 secret时，应优先逐 scheme、redirect、new-tab、DNS/IP和 opaque origin 重验，因为 `data:`、`blob:`、userinfo与非标准 IP编码会绕开简单 hostname规则；边界是 allowlist只限制去向，不消除页面 prompt injection。
6. 当 handler报告 success或更新内存状态时，应优先要求 effect-specific readback（disk bytes、target id、current URL、artifact hash），因为自然语言 success、marker和内存对象都可能与真实世界漂移；边界是 readback也必须绑定同一 revision与权限。
7. 当 deterministic checker给 Agent修复建议时，应优先返回稳定 code、精确 subject、measured evidence与允许的局部修法，因为全量重写会扩大变化和幻觉；边界是不能为了过 gate删除真实语义或绕开 policy。
8. 当依赖审计只覆盖当前 environment、生产子集或可解析 requirements时，应优先同时报告 scope、blocked lane与dev/runtime区别，因为 0 advisory、403或 resolver失败都不是安全证明；边界是 advisory existence仍需可达性与兼容性分析。
9. 当上游仓库快速更新时，应优先固定 commit并区分 API snapshot、main HEAD、stable tag、release asset与host adapter，因为“最新”不是单一 artifact identity；边界是固定 commit也不保证依赖源长期可重现。

### 今日统一实验

优先实现 `runtime/hermes/github-learning-poc/scoped-effect-receipt/`，把 Archify 的 target-safe artifact commit 与 Browser Use 的 typed action/observed page change统一成最小 contract：

```text
proposal
  -> validate schema
  -> resolve canonical target
  -> authorize(scope,effect,revision)
  -> stage/execute with deadline
  -> observe/readback
  -> exactly-one terminal receipt
  -> only then project success
```

fixture至少覆盖错误扩展/越界path、symlink swap、last-good旧artifact、`data:` URL、redirect、DOM revision变化、timeout cleanup双计数、disk失败内存污染、tab switch无result。只使用 synthetic state，不连接浏览器/provider/MCP，不改配置/cron/skills/curated。

## Skill 升格总判断

- `tt-a1i/archify`：**暂不沉淀**完整 skill；其窄化 `scoped-artifact-delivery` 模式为**需二次验证**，先修复/绕开 target authority gap并完成 path fixtures。
- `browser-use/browser-use`：**暂不沉淀**完整 skill；其窄化 `action-effect-envelope` 模式为**需二次验证**，先完成 scheme/revision/timeout/readback fixtures。
- 统一候选 `scoped-effect-receipt` 可能跨 Hermes/future-agent复用，但与现有 verification-first、effect-scope、completion contract、path-portability高度重叠；优先更新既有能力而非新建重复 skill。
- 今日不创建 `capabilities/skills/`，不更新 shared skill manifest，不写 curated active facts。所有候选仅进入二轮治理输入。

## 明日继续

1. 用 30 分钟实现 `scoped-effect-receipt` synthetic POC，先覆盖 `../marker.env`、absolute outside root、data URL、timeout cleanup、disk readback fail 五个失败 fixture。
2. 追踪 Archify #124/#126 的 fix/PR；固定新 commit 后先重跑隔离 marker fixture，再跑 showcase validation与最窄 output-path regression，不测试用户文件。
3. 追踪 Browser Use #4763、#5513/#5521、#5527、#5529、#5543/#5555；只有 merged commit进入浅克隆后才重跑对应 tests，PR prose不算修复完成。
4. 对 Browser Use 生成仅当前平台/runtime依赖的可解析 export，在可信 index运行 audit；区分 direct/transitive/dev、可达性与升级阻塞，不因 portalocker resolver failure跳过。
5. 对 shared 现有 verification/effect/path/completion skills做只读去重，判断应更新哪个 contract；不自动升格、不改配置或 cron。

## 候选反哺

### Candidate Facts

- [ ] topic: verified artifact delivery必须同时证明 content identity 与 target authority | evidence: `tt-a1i/archify@8b542d60` 的 freeze/check/hash/rename实现 + #124 + 本机隔离 marker真实复现 | 建议: create candidate / 与verification、path-portability去重 | 安全级别: high
- [ ] topic: browser action success需要 typed proposal、host grant、observed effect与revision-bound readback | evidence: `browser-use/browser-use@28670f720` 的 Registry/Tools/multi_act + #5527/#5529 | 建议: create candidate | 安全级别: high
- [ ] topic: domain allowlist必须逐 scheme/redirect/opaque origin验证 | evidence:固定源码对 data/blob直接 True + open #4763 | 建议: update effect/network governance candidate | 安全级别: high
- [ ] topic: timeout completion必须 exactly-once accounting | evidence:固定 `Agent._execute_step` + #5513 + open PR #5521 | 建议: update terminal contract candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: scoped-effect-receipt | 可复用场景: artifact发布、browser action、文件写入、消息发送、知识库copy | 是否建议 shared: yes（仅二次验证并优先更新既有skill） | 原因: 跨Agent横切能力，但需target/scheme/revision/readback/terminal fixtures并避免重复建设
- [ ] 名称: archify-full-skill | 可复用场景: architecture diagram | 是否建议 shared: no（当前） | 原因: CLI arbitrary output overwrite已实测，release/archive lane未全绿
- [ ] 名称: browser-use-full-skill | 可复用场景: browser automation | 是否建议 shared: no（当前） | 原因: 高权面、domain bypass与一致性open gaps、依赖审计未闭合

### Candidate Open Questions

- [ ] 问题: Archify #124 修复后是否对 CLI/meta 两条 output source统一执行 extension、allowed root、symlink、existing target type与stable diagnostic？ | reason: gap | priority: high
- [ ] 问题: visual-check如何强绑定本次 deliver receipt/artifact hash，避免失败后检查 last-good旧文件？ | reason: adaptation | priority: high
- [ ] 问题: Browser Use #4763 对 data/blob 的最终策略如何兼顾 opaque origin、同源 blob、redirect与download？ | reason: security gap | priority: high
- [ ] 问题: #5521 合并后 step timeout在 cleanup-counted/cleanup-skipped两条lane是否都有 exactly-once terminal/counter evidence？ | reason: gap | priority: high
- [ ] 问题: shared hub现有哪个 skill应承载 target authority + observed effect + terminal receipt，能否避免再建一个同义 skill？ | reason: adaptation/dedup | priority: medium
- [ ] 问题: Browser Use 当前可重现 runtime-only dependency closure与 advisories修复版本是什么，exact pins升级会破坏哪些 provider/OS lane？ | reason: blocked | priority: medium

### 不应自动落地

- 不安装或启用 Archify/Browser Use，不运行第三方 pipe-to-shell/global installer，不连接 Chrome/profile/cloud/MCP/provider。
- 不调用 OpenClaw；当前 runtime 不存在。
- 不自动修改 Hermes/OpenClaw config、model、provider、auth、env、cron、plugins或skills。
- 不让 Agent自由选择 shared外 output path，不处理用户文件；#124 复现仅在 `/tmp` 隔离 fixture。
- 不读取、记录、上传 cookie、API key、TOTP seed、账号密码或 browser storage；报告仅使用变量名/类别。
- 不把网页/diagram/README prose直接写 curated active fact，不把 candidate skill视为已升格。
- 不把 Stars、README benchmark、GitHub Actions success、聚焦 tests、audit 0或历史 advisory已修复外推为生产安全。
