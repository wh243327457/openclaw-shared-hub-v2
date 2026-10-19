---
type: case
status: draft
created: 2026-10-19
updated: 2026-10-19
domain: learning
tags: [github-learning, agent-skill, verification, recursive-harness, resume-identity]
---

# 2026-10-19 GitHub 热门项目学习报告

> 执行者：Hermes；按任务约束未调用 OpenClaw。  
> 查询与验证时间：2026-10-19 08:31–08:39（工具环境 UTC+09:00；GitHub 时间按 UTC 原样记录）。发现口径包括 GitHub Search API `created:>2026-10-01 stars:>100 sort:stars` 与 `stars:>3000 pushed:>2026-10-10 sort:updated`。Stars/Forks/License/更新时间以 08:39:02 的 Repository API 快照为准。  
> 深读固定提交：`wheresryan22/anatomy@1482e8469b0a9e0d8cc18ea2740a01423d29ae80`；`google-research/harness2@1cfe254e8d25b15f37048c3730134686abe60335`。  
> 真实来源：GitHub Repository/Search/Commit/Release/Issues/Actions/License/Security Advisories API，README、SECURITY/docs、依赖声明、关键源码及本机定向测试。Dependabot vulnerability-alerts 对两仓均返回 HTTP 404，公开 repository advisories 均为 0；两者都不能外推为“无漏洞”。

## 今日结论

**Agent 能力若要可靠进化，不能把“写一份长 Skill”或“跑出一个更好答案”当完成：应把执行契约压到可编辑 surface，把候选改动与真实 probe 证据绑定，再用确定性 verifier、输入身份、原子 terminal marker 和可重建 projection 收口；视觉/报告等有损输出同样必须由 canonical model 单向生成，而不能从成品 prose/页面反推真相。**

### 今日真实验证摘要

- **Anatomy**：固定 `1482e846...`；按仓库 CI 同款临时依赖运行完整 Node 测试，实报 **289 passed / 1 failed**。唯一失败为 `drive-page-load.test.mjs` 在全套并发压力下读到 `loading false`；单独重跑该文件为 **1 passed / 0 failed**，因此标记为**疑似时序/负载 flaky，待上游复验**，不能写“全绿”。固定 head GitHub check `Rebuild the examples` 为 completed/success。
- **Harness²**：固定 `1cfe254e...`；`tests/test_workflow.py` 实报 **5 passed + 2 subtests passed**；Ruff 通过；credential-free `harness2-demo --k 2` 实报 **2 tasks completed / 0 failed、28 executions、32 editor calls**。
- Harness² 当前环境审计图的 `pip-audit` 为 0 known findings，但本项目本身因本地 editable package 被 scanner 标记 skipped，且 production `bridge` extras、下载 benchmark/runtime 与模型执行路径未纳入该次窄审计。
- 两仓都很新：Anatomy 创建于 2026-10-08，Harness² 创建于 2026-10-06；热度与短期活跃不等于成熟度。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 15,980 | 1,229 | JavaScript | MIT | 2026-10-18T20:20:24Z | **深读：Skill-as-workflow + deterministic visual verification** |
| [openai/math](https://github.com/openai/math) | 15,169 | 1,762 | Lean | Apache-2.0 | 2026-10-12T21:55:27Z | 形式化数学资产，非今日 Agent harness 主线 |
| [storytold/wordcraft](https://github.com/storytold/wordcraft) | 14,379 | 3,823 | Rust | Apache-2.0 | 2026-10-18T21:11:52Z | 新文档工具，和昨日同组织项目相邻，今日不重复深读 |
| [google-research/harness2](https://github.com/google-research/harness2) | 6,091 | 551 | Python | Apache-2.0 | 2026-10-14T02:22:51Z | **深读：Propose–Probe–Compose + persistent evidence library** |
| [storytold/cadcraft](https://github.com/storytold/cadcraft) | 5,770 | 2,574 | Rust | Apache-2.0 | 2026-10-18T18:33:14Z | CAD/Agent 工具候选，后续可核 effect boundary |
| [tangency-labs/solidcraft](https://github.com/tangency-labs/solidcraft) | 5,638 | 662 | Rust | Apache-2.0 | 2026-10-18T22:51:53Z | 高活跃 3D 候选，安全与成熟度待核验 |
| [zhongerxin/iPhone-use](https://github.com/zhongerxin/iPhone-use) | 4,167 | 415 | Python | MIT | 2026-10-16T08:47:41Z | 设备 Agent 候选，真实设备权限边界待核验 |
| [Niko1221/Strata](https://github.com/Niko1221/Strata) | 27,445 | 2,904 | C++ | MIT | 2026-10-17T06:50:46Z | 上月新项目高热，系统软件边界待后续核验 |

> 表中数据全部来自最后一轮 GitHub Repository API。`open_issues_count` 会包含 PR，不把它当纯 issue 数。顶层 License 不覆盖依赖、数据集、模型、字体/资产、第三方 runner、release 制品与商标。

## 深读项目

### 1. wheresryan22/anatomy

- **一句话判断**：最值得学的不是“让 Agent 画漂亮 SVG”，而是把一个高自由度创作任务约束成 **Skill 工作流 → canonical 几何/物理模型 → 多种 projection → 多层确定性检查 → 人眼 close-up** 的证据闭环。
- **解决的问题**：替代“模型直接写一页图、打开看起来差不多就交付”的旧做法；它要求真实数值先建模、几何只构建一次、动效和读数共用模型，并把 screenshot、line-end、碰撞、支撑、深度顺序、3D orbit、重建一致性拆成不同 verifier。
- **URL / API 快照**：https://github.com/wheresryan22/anatomy ；**Stars: 15,980 / Forks: 1,229 / Language: JavaScript / License: MIT（API）**；`created_at=2026-10-08T10:12:49Z`，`pushed_at=2026-10-18T20:20:24Z`，`updated_at=2026-10-18T23:38:25Z`，API `open_issues_count=50`（含 PR）。
- **固定提交 / release**：[`1482e8469b0a9e0d8cc18ea2740a01423d29ae80`](https://github.com/wheresryan22/anatomy/commit/1482e8469b0a9e0d8cc18ea2740a01423d29ae80)，verified commit，commit time `2026-10-18T20:20:24Z`；latest release [`v1.1.0`](https://github.com/wheresryan22/anatomy/releases/tag/v1.1.0)，published `2026-10-12T18:43:35Z`。
- **来源交叉核验**：Repository/Commit/Release/Issues/Actions/License/Security Advisories API；README 的 How it works/Limits；`SECURITY.md`；`SKILL.md`；`references/verify.md`；kit/scripts/tests/CI；本机 Node/Chrome 测试。

#### 架构 / 实现与数据流

```text
User concept + true numbers
          |
          v
      SKILL.md workflow
size -> truth -> object -> parts -> world plan
          |
          v
 canonical geometry / physical model
 kit/iso-kit + lathe + tube + audit recorder
       /          |             \
      v           v              v
 SVG/HTML      React view      WebGL/3D view
      \           |              /
       +------ live model -------+
                 |
       deterministic verification
 audit.mjs + lines.mjs + capture/drive + turn-check
                 |
        source-only publish plan
 build outputs removed -> figure.json -> gallery CI rebuild
```

核心机制：

1. `SKILL.md` 不是描述文件，而是有顺序、有质量门、有不适用边界的执行契约；它要求先确定 tier、真实模型和至少 40 个 purposeful parts，再允许进入几何。
2. `kit/iso-kit.*`、`lathe.mjs`、`tube.mjs` 形成 canonical geometry；静态 art、动效、读数和验证使用同一世界坐标与模型，降低 projection 漂移。
3. `kit/audit.mjs` 做模型级检查；`lines.mjs` 检查 audit 看不到的 SVG line markup；`capture.mjs`/`drive.mjs` 通过 Chrome DevTools Protocol 检查真实浏览器输出；不同 verifier 不互相冒充。
4. `scripts/publish.mjs` 只复制允许的 source 类型、拒绝 symlink 与未知外部依赖、在目标目录重建并预览，随后删除生成页面，只把 source + `figure.json` 交给 gallery CI。
5. 但 verifier 仍有边界：全套测试本机出现一个 page-load 时序失败，单测复跑通过；README 自己也明确“zero audit necessary, not sufficient”。

#### repo tree 摘要

```text
anatomy/
├── SKILL.md                     # Agent 触发条件、工作流、质量门与边界
├── kit/
│   ├── iso-kit.{mjs,ts}         # 相机、实体、SVG/card/page projection
│   ├── audit.mjs                # 碰撞/支撑/深度/覆盖等 model verifier
│   ├── lathe.mjs / tube.mjs     # 曲面与管线 canonical geometry
│   ├── turn*.mjs                # 3D runtime/build/audit
│   └── react/                   # React server-safe draw + client live hooks
├── scripts/
│   ├── capture.mjs / drive.mjs  # 真实 Chrome capture/action/eval
│   ├── lines.mjs                # line-end verifier
│   ├── turn-check.mjs           # 3D fidelity/order/pops/perf
│   ├── publish.mjs              # source-only staged publish/PR plan
│   └── *.test.mjs               # 290 个当前测试 case 的来源
├── references/                  # craft/motion/verify/WebGL/3D/print/publish
├── examples/                    # 8 个完整参考实现与提交后的 built pages
├── evals/evals.json             # Skill 评测 prompts/expectations
└── .github/workflows/ci.yml     # 临时 dev deps + tests + byte-stable rebuild
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `SKILL.md` | Agent contract | 先 truth/model，再 geometry；按 Figure/Hero/Epic 控预算；audit + line + browser + close-up 分层验收 |
| `kit/audit.mjs` | model-level verifier | `recorder/settle/audit/auditOrExit` 组合 geometry coverage、collision、support、depth-order 等检查 |
| `scripts/capture.mjs` | browser evidence | 临时 Chrome profile、动态 DevTools port、navigation/console/exception/screenshot read-back |
| `scripts/drive.mjs` | action/effect verifier | typed actions、参数 gate、真实 input event、until/shot/lines/orbit/sheet，与页面 readout/console evidence绑定 |
| `scripts/publish.mjs` | staged projection/publish | allowlisted sources、path rewrite、目标重建/预览、失败回滚、只提交目标目录 |
| `.github/workflows/ci.yml` | drift ratchet | 安装固定 test-only deps，跑 tests，重建全部 examples，要求 git diff/status 为空 |

#### ⭐ 源码精读

1. `auditOrExit`：build 的 `--audit` 不是文案约定，而是 terminal gate；任何 model-level problem 都转成非零退出。

```javascript
export function auditOrExit(
  R, P = R.P,
  { flag = "--audit", argv = process.argv, ...options } = {}
) {
  if (!argv.includes(flag)) return null;
  const result = audit(R, P, options);
  if (result.problems) process.exitCode = 1;
  return result;
}
```

逻辑摘要：真实函数还会输出各检查统计；`audit()` 汇合 clearance、terminal、support、depth、coverage 等。价值在于“Agent 自报完成”必须经过 deterministic terminal；边界是它只能检查 recorder 记录的形状，无法覆盖所有视觉语义。

2. `capture.main`：每次验证使用临时 profile 与 Chrome 分配的随机 DevTools port；先完成 navigation，再做真实页面 screenshot 与 console/exception采集。

```javascript
const profile = mkdtempSync(join(tmpdir(), "iso-capture-"));
const chrome = spawn(binary, [
  "--headless=new",
  ...(process.platform === "linux" ? ["--no-sandbox"] : []),
  "--remote-debugging-port=0",
  `--user-data-dir=${profile}`,
  "--allow-file-access-from-files",
  "--enable-unsafe-swiftshader",
  "about:blank",
]);
const port = await chromePort(chrome, profile);
```

逻辑摘要：随机端口避免固定端口冲突，throwaway profile 降低状态污染；但 Linux 明确使用 `--no-sandbox`，且 `SECURITY.md` 要求只指向可信页面，因此这不是不可信网页沙箱。

3. `drive.main` 的 action admission：执行 browser action 前先检查 action kind 和数值范围，避免空 orbit/sheet 被当成功。

```javascript
const kinds = new Set([
  "scroll", "wait", "move", "click", "drag", "key", "slow",
  "until", "eval", "shot", "lines", "turn", "orbit", "sheet"
]);
if (!Array.isArray(actions)) throw new Error("actions must be an array");
for (const action of actions) {
  if (!Array.isArray(action) || !kinds.has(action[0]))
    throw new Error(`unknown action ${Array.isArray(action) ? action[0] : action}`);
  if (action[0] === "orbit") {
    const [, , from, to, step] = action;
    if (![from, to, step].every(Number.isFinite) || step === 0 ||
        (step > 0 ? from > to : from < to)) throw new Error("invalid orbit");
  }
}
```

逻辑摘要：finite candidate set + typed shape 将自由文本动作压缩成 host 可验证 IR；但 `eval`/`preload` 仍可运行调用者提供的 JS，只能用于可信页面与测试代码。

4. `publish`：把发布拆成 staging、重建、preview、manifest 和 rollback；失败时恢复原目标。

```javascript
try {
  const all = listFiles(source);
  const typed = all.filter((file) => SOURCE_TYPES.includes(extname(file).toLowerCase()));
  // copy/rewrite source, rebuild declared pages, optionally capture preview
  writeFileSync(join(dest, "figure.json"), JSON.stringify(figure, null, 2) + "\n");
  if (replaced) rmSync(replaced, { recursive: true, force: true });
  return { dest, figure, skipped, linked, preview, measured };
} catch (error) {
  rmSync(dest, { recursive: true, force: true });
  if (replaced) renameSync(replaced, dest);
  throw error;
}
```

逻辑摘要：失败不会留下半个 replacement；PR plan 只 `git add -- <folder>`。边界是它没有跨进程 lock/CAS，且 issue #89 已证明 `--pages` 同主题 key collision 可静默丢页面。

#### 依赖分析与供应链风险

- 仓库**没有 `package.json` 或 lockfile**；核心宣称 Node built-ins only。CI 为 React 相关 tests 临时安装固定 `react@19.3.0`、`react-dom@19.3.0`、`typescript@5.9.3`、`esbuild@0.28.2`，但这些不属于提交的 production lock graph。
- 本机第一次直接跑 `node --test scripts/*.test.mjs` 得到 **264 pass / 6 fail**，6 个失败都因 `typescript`/`esbuild` 缺失；按 `.github/workflows/ci.yml` 安装同款临时依赖后得到 **289 pass / 1 fail**。这说明“zero dependencies”适用于核心运行，不等于所有 tests 无 dev prerequisites。
- GitHub fixed-head check 为 success；本机完整 suite 的唯一失败单独复跑通过，暂按 flaky/资源时序风险记录，不用上游绿 check 抹掉本机失败。
- repository advisories API 为 0；Dependabot endpoint 404。没有 lockfile 就无法给出稳定的完整依赖图，且发布时还会调用本机 `node`、Chrome、git、gh 与 gallery checkout。

#### 可复用经验

- 当 Agent 要生成图、报告、卡片或其他 projection 时，应优先先建立 canonical model，再单向生成各视图并分别验证，因为视觉上“像”不证明数值、身份和状态一致；边界是 canonical model 自身仍需真实来源与领域验收。
- 当自由度很高的 Skill 需要稳定复用时，应优先把流程写成有顺序的 contract，并为不同 failure class 配独立 deterministic verifier，因为一个总分或一次 screenshot 会掩盖 coverage gap；边界是 verifier 通过仍不能替代人眼/业务接受。
- 当把 Agent 生成物发布到共享仓库时，应优先 source allowlist → isolated rebuild → preview/read-back → scoped commit → rollback，而不是直接复制最终页面，因为 derived artifact 可陈旧且可能夹带环境状态；边界是并发发布仍需要 lock/CAS。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/canonical-projection-receipt-v0/` 做离线 fixture：定义 `CanonicalArtifact(id, source_hash, model, projections[])`，生成 Markdown 与 SVG 两个 projection；人为制造 stale source hash、缺页、same-key collision 和 verifier-not-run，断言 terminal 只能是 `verified|partial|blocked|failed`，不能因文件存在而 completed。只用 synthetic data，不安装 Anatomy、不启动外网、不改 shared skill/curated。

#### 风险边界

- **License**：GitHub API/License API 与根 `LICENSE` 均为 MIT；生成图、用户输入、引用资料、字体/图片、gallery 内容与品牌许可需单独审。
- **维护活跃度**：10-08 创建，10-12 发布 v1.1.0，10-18 仍 push；速度快但历史极短，3D 明示 beta，只支持 latest `main`。
- **安全**：`SECURITY.md` 明确 Chrome scripts 使用 throwaway profile、`--allow-file-access-from-files`，`drive.mjs` 可执行传入 JS；源码还在 Linux 使用 `--no-sandbox`。只可针对可信页面/代码运行。
- **局限**：本机完整 suite 非全绿；未运行所有 example byte-stable rebuild、Raptor 完整 audit、3D 15–20 分钟 full orbit、PDF print、真实 gallery PR。issue #89 的 page collision、#88 的 MiniMax agent whitelist drift 仍开放。
- **不能自动执行**：不全局安装该 Skill，不运行未知页面/JS，不自动发 PR，不复制其 33KB domain-specific `SKILL.md` 到 shared，不自动修改 Hermes/OpenClaw 配置或 shared active facts。

#### ⭐ Skill 升格判断

**需二次验证**。可迁移的是 `canonical model → projection → independent verifiers → staged publish receipt`，不是整套 isometric 视觉 Skill。它与现有 `research/github-hot-project-learning`、`foundation/shared-memory-bridge`、`autonomous-learning/orchestrator-protocol` 的 canonical/evidence/verification 原则重叠，应先做 fixture 和去重；完整 Anatomy Skill **暂不沉淀**。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/canonical-projection-receipt-v0/`。
- 若 fixture 捕获真实问题，优先更新既有能力：
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：报告/知识库 copy 前加入 canonical source hash、section coverage、projection read-back；
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：不同 failure class 不共享一个“通过”标志，增加 verifier coverage matrix；
  - `capabilities/skills/foundation/shared-memory-bridge/SKILL.md`：derived projection 必须可由 canonical truth 重建并记录 source identity。
- Hermes 本地候选：研究报告若生成图/卡片，只从 sealed report schema 投影；不要从卡片 prose 反解析候选事实。

### 2. google-research/harness2

- **一句话判断**：它把“改进 Agent”做成一个可执行实验：有限 editable surface、候选 harness、同任务 probe、证据驱动 compose、匿名 adoption 与跨任务 library；真正应迁移的是这条证据链及其失败边界，而不是递归次数本身。
- **解决的问题**：替代“读一次失败日志就直接改全局 prompt/skill”与“仅靠 benchmark 最终分数猜哪项改动有效”的旧做法；在 task-level 做 Propose–Probe–Compose，在 harnessing-level 只保存 adopted harness 和 evidence-supported lessons。
- **URL / API 快照**：https://github.com/google-research/harness2 ；**Stars: 6,091 / Forks: 551 / Language: Python / License: Apache-2.0（API）**；`created_at=2026-10-06T21:48:11Z`，`pushed_at=2026-10-14T02:22:51Z`，`updated_at=2026-10-18T23:38:59Z`，API `open_issues_count=68`（含 PR）。
- **固定提交 / release**：[`1cfe254e8d25b15f37048c3730134686abe60335`](https://github.com/google-research/harness2/commit/1cfe254e8d25b15f37048c3730134686abe60335)，verified commit，commit time `2026-10-14T02:22:49Z`；GitHub Releases 与 Tags API 均为空，**没有可核验 release/tag**。
- **来源交叉核验**：Repository/Commit/Issues/License/Security Advisories API；README；`docs/EXPERIMENTS.md`/SETUP/BENCHMARKS；`dependencies/README.md`；pyproject/config；core/substrate/tests；本机 tests/demo/lint/audit。

#### 架构 / 实现与数据流

```text
benchmark task + source + base harness
                |
          k base executions
                |
        +-------+--------+
        |                |
  parallel recursion   sequential recursion
  k INV + k DOM        round t: INV + DOM
  probe candidates     probe -> compose c_t
  k independent AGG    carry c_t forward
        |                |
        +--- final rollouts ---+
                              v
                 delivered-artifact filter
                 anonymized deterministic IDs
                 selector chooses one final
                              |
                 adopted harness + evidence
                              v
               task-local reflection/distil
                              |
            per-domain ordered experience library
                              |
                 next task reads earlier entries
```

核心机制：

1. `tree.SurfaceSpec` 将 system prompt、guardrails、memory、skills、scripts、subagents、plugins/hooks 压成明确 editable surface；off-surface files 被拒绝，proposal 不是任意 workspace 写权。
2. `run_parallel` 探索宽度，`run_sequential` 探索深度；两者都要求 ledger identity `R=4k/P=3k`，重复 label 会触发 `BudgetError`，避免覆盖后仍虚报候选数。
3. `_run_stage` 为 invalid proposal 提供一次带错误反馈的 repair；两次失败继承 fallback harness，并显式记录 `fell_back/error/attempts/usd`。
4. selection 只接受 delivered、非空 artifact，写匿名完整候选证据，选择失败时有受限 fallback；reflection 只在 adoption 后把 evidence-supported lesson 写 domain library。
5. resume marker 把 harness fingerprint 与正常 return 绑定，并用 temp + `os.replace` 原子发布；但 open issue #65 实证它**未绑定 task prompt/source identity**，可复用旧任务答案，这是不能照搬的关键缺口。

#### repo tree 摘要

```text
harness2/
├── harness2/
│   ├── core/
│   │   ├── recursion.py         # parallel/sequential Propose–Probe–Compose
│   │   ├── tree.py              # editable surface、validate、diff、diversity
│   │   ├── selection.py         # artifact filter、匿名 adoption、reflection
│   │   ├── ledger.py            # R=4k/P=3k identity 与 cost entries
│   │   ├── runmark.py           # atomic completion marker + harness fingerprint
│   │   ├── schedule.py          # namespace、stream order、resume、library ownership
│   │   └── context.py/spec.py   # task-local evidence 与 adapter contracts
│   ├── substrate/               # OpenCode / Codex adapters
│   ├── benchmarks/              # JobBench / LAB / WorkBuddy adapters
│   └── cli/                     # run/check/judge/report/setup/demo/bridge
├── docs/                        # setup、benchmarks、experiments/reproducibility
├── dependencies/                # pinned upstream identity/notices
├── third_party/                 # derived runners、patches、许可证/PROVENANCE
├── tests/test_workflow.py       # execution/evidence/adoption focused regressions
└── pyproject.toml               # core 零 runtime deps；render/bridge optional extras
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `harness2/core/recursion.py` | task-level recursion | stage retry/fallback、parallel width、sequential depth、probe evidence、stable ledger writes |
| `harness2/core/tree.py` | harness editable surface | path normalization、allowlist、Skill trigger repair、schema/compile validation、exact materialization |
| `harness2/core/selection.py` | adoption/reflection | drop non-delivered artifacts、deterministic anonymization、complete evidence files、selection fallback、lesson distillation |
| `harness2/core/runmark.py` | resume identity | harness tree hash、atomic completion marker、reuse check；缺 task/source identity |
| `harness2/core/ledger.py` | method/cost ledger | exact rollout/session counts、duplicate labels、attempts/usd projection |
| `harness2/substrate/codex.py` | host adapter | Codex surface/materialization/CLI flags；明确禁用 sandbox 和 approvals，是高风险边界 |

#### ⭐ 源码精读

1. `_run_stage`：proposal 只有两次合法化机会；每次都经过 tree/surface/adapter/grader-leak validation，失败后继承 fallback 而不是硬装成功。

```python
def _run_stage(*, label, dim, job, fallback, adapter, prop,
               ctx_dir, task_id, rollouts, harness_dir, library_dir,
               pool=(), decisions=None) -> Stage:
    # build evidence + mission
    for attempt in range(1, STAGE_ATTEMPTS + 1):
        reply = prop.call(
            mission + (f"\n# YOUR PREVIOUS ATTEMPT WAS REJECTED\n{err}" if err else ""),
            tree.root, f"{label}.a{attempt}", harvest="context/harness",
            max_attempts=TRANSPORT_ATTEMPTS,
        )
        new = harness_tree.read_tree(surface, reply.workspace, rejected=rejected)
        kept, err = _accept_tree(surface, adapter, new, fallback, label)
        if not err:
            return Stage(label=label, dim=dim, tree=new, attempts=spent_calls)
    return Stage(label=label, dim=dim, tree=dict(fallback),
                 fell_back=True, error=err[:400], attempts=spent_calls)
```

逻辑摘要：错误反馈参与 repair，但 acceptance 由 host validator 决定；边界是 fallback 后该 stage 仍会被 probe，消费者必须看 `fell_back`，不能只看有 tree。

2. `run_parallel`：INV/DOM proposals 并发生成、probe 后，AGG 读取完整 pool evidence 生成 k 个独立 compositions；ledger 在并发结束后按稳定顺序记账。

```python
specs = [(f"{d.lower()}{i}", d, i)
         for i in range(1, k + 1) for d in ("INV", "DOM")]
stages = list(pool_x.map(lambda s: _run_stage(
    label=s[0], dim=s[1], fallback=base_tree,
    rollouts=base, harness_dir=base_dir, library_dir=library_dir,
    job=prompts.propose(benchmark_prompts, s[1], surface, k=k, index=s[2]),
    adapter=adapter, prop=prop, ctx_dir=ctx_dir, task_id=task_id), specs))
result.rollouts.update(_roll_many(... [(s.label, s.tree) for s in stages] ...))
# then agg1..aggk compose from pool_ev and are probed again
ledger.assert_identity()
```

逻辑摘要：proposal 与 execution evidence 分离，compose 看到候选真实 rollout，而非只看 diff prose；边界是同任务 repeated probing 可能过拟合，公开 benchmark 还存在 rubric leakage 风险。

3. `Ledger.assert_identity`：不是只看总数；duplicate label 即使凑够 R/P 也失败，因为它意味着 run id 覆盖。

```python
def assert_identity(self) -> None:
    want_r, want_p = expected_rollouts(self.k), expected_sessions(self.k)
    rl, sl = self.labels("rollout"), self.labels("session")
    dupes = sorted(
        {label for label in rl if rl.count(label) > 1}
        | {label for label in sl if sl.count(label) > 1}
    )
    if not dupes and self.R == want_r and self.P == want_p:
        return
    raise BudgetError("...")
```

逻辑摘要：冻结 coverage denominator，防止并发覆盖后“计数看似正确”；边界是它约束方法次数，不是费用硬上限，issue #4 的 `--max-usd` 仍开放。

4. `mark_complete/is_complete`：只有 runner 正常返回后才能原子写 marker，并要求当前 harness fingerprint 相同。

```python
def mark_complete(where: Path, *, run_id: str,
                  harness_dir: Path | None = None, extra: dict | None = None) -> Path:
    payload = {"version": VERSION, "run_id": run_id, "at": time.time(),
               "harness": fingerprint(harness_dir), **(extra or {})}
    tmp = Path(where) / f"{MARK}.{os.getpid()}.tmp"
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
    final = Path(where) / MARK
    os.replace(tmp, final)
    return final

def is_complete(where: Path, *, harness_dir=None, match_harness=True) -> bool:
    m = read_mark(where)
    return bool(m and m.get("version") == VERSION and
                (not match_harness or m.get("harness") == fingerprint(harness_dir)))
```

逻辑摘要：artifact presence 不等于 finished；但 marker 没有 prompt/source hash，issue #65 已用本地 reproducer 证明 input 改变后仍复用旧 output。

#### 依赖分析与供应链风险

- `pyproject.toml`：core runtime `dependencies=[]`；`render` extras 为 `openpyxl>=3.1,<4`、`python-pptx>=1,<2`；`bridge` 精确固定 `litellm[proxy]==1.95.0`、`fastapi==0.139.2`、`google-auth==2.56.3`。
- 外部代码 pin 在 `config.DEPENDENCY_PINS`：JobBench、WorkBuddy、Harvey LAB、OpenCode 都固定 commit；Codex version 固定 `0.144.6`。优于 moving branch，但下载内容、patch、数据集 revision、容器/runtime 仍需 provenance/read-back。
- `dependencies/README.md` 明确 WorkBuddy custom Tencent license 含 EU territorial limitation；dataset license 与 software license 分离。因此 Apache-2.0 顶层许可不覆盖所有 benchmark 用法。
- 本机 `pip-audit` 对当前窄环境报 0 known findings，但 `harness2 0.1.0` 本地包被 skipped，未安装 render/bridge extras、benchmark dependencies、OpenCode/Codex runtime。不能外推 production graph 安全。
- GitHub repository advisories 为 0、Dependabot endpoint 404；无 release/tag，source main 是唯一可核验对象。

#### 可复用经验

- 当系统要让 Agent 自动改进 prompt/skill/harness 时，应优先把每次改动当候选，在同一 immutable task identity 上执行 probe 并保留对照证据，因为“编辑成功”不证明行为更好；边界是同任务证据可能过拟合，仍需 holdout/跨任务验证。
- 当并发候选要汇总和恢复时，应优先冻结 coverage denominator、使用稳定唯一 label、在 pool 完成后按确定顺序写 ledger，因为计数相同也可能是 run id 覆盖；边界是方法预算不等于成本硬限额。
- 当 resume/cache 决定跳过昂贵执行时，应优先绑定 **harness identity + task prompt/source identity + executor/model/policy identity + output integrity**，因为只绑定 harness 会复用旧输入结果；边界是 input 改变后还要级联失效 derived library/grade。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/harness-input-identity-v0/` 扩展 synthetic fixture：计算 `canonical_task_hash`（instructions + allowlisted source relative path/content hash）、`harness_hash`、`executor_identity`、`policy_version`；先完成一次 run，再改 instruction/source/harness/model 四类输入，断言 resume 分别 invalidated；同时模拟 grade/experience projection，要求 upstream identity 变化后 stale projection 不可复用。只用本地临时文件，不调用模型/benchmark/网络。

#### 风险边界

- **License**：核心 Apache-2.0；`third_party/`/benchmarks/datasets 保留上游许可，WorkBuddy 有 EU 限制，不能把顶层 license 外推全图。
- **维护活跃度**：10-06 创建、10-14 最后 push；无 release/tag、fixed head 无 check-runs，成熟度与发布流程待观察。
- **安全**：README/docs 明确 executor 网络未限制；Codex adapter 源码使用 `--dangerously-bypass-approvals-and-sandbox` 与 `--dangerously-bypass-hook-trust`。不得在含 secret/私有数据/生产权限的普通宿主直接运行。
- **正确性缺口**：open issue #65 证明 task source 变化后 resume/cache 可静默复用旧结果；#44 证明 re-run 后 judge 失败时可能保留旧 grade；#50 记录 interrupted rerun spend undercount；#4 费用 stop 尚未实现。
- **局限/未验证**：本机仅跑 focused workflow tests、credential-free demo 和 Ruff；未安装/运行 JobBench/LAB/WorkBuddy、真实 OpenCode/Codex executor、provider/judge、network restriction 或完整研究 benchmark。
- **不能自动执行**：不接真实 provider，不关闭 Hermes sandbox/approval，不下载 benchmark 数据，不采用 WorkBuddy 数据/runner，不自动改 global prompt/skills/cron/curated。

#### ⭐ Skill 升格判断

**需二次验证**。Propose–Probe–Compose 与现有 `autonomous-learning/orchestrator-protocol` / `self-reflection-engine` 高度重叠；其可迁移增量是“editable surface + probe evidence + input-bound resume + adoption 后才写 library”。鉴于 #65/#44，当前不能直接迁移完整 resume/adoption 逻辑，更不能自动启用 harness self-modification。

#### ⭐ Hermes / shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/harness-input-identity-v0/`。
- 若通过，优先更新已有：
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：候选修改必须绑定 base/input hash、probe artifact、selection decision 和 exact terminal；
  - `capabilities/skills/autonomous-learning/self-reflection-engine/SKILL.md`：reflection 只消费 adopted + independently verified evidence；
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：audit/知识库 reuse 绑定日报 source hash，不仅绑定日期/path。
- 脚本候选：在未来 runtime run-state 增加 `input_identity`、`harness_identity`、`executor_identity`、`derived_from`；identity mismatch 返回 `blocked/stale`，不得 silent resume。

## 跨项目机制对照

| 机制 | Anatomy | Harness² | 对 shared hub 的判断 |
|---|---|---|---|
| canonical source | geometry/physical model | editable harness tree + task evidence | raw/canonical/projection 必须分层 |
| Agent 自由度 | Skill 顺序与 finite browser actions | SurfaceSpec path allowlist + validator | proposal plane 必须窄于 effect plane |
| verification | geometry + lines + browser + human close-up | candidate rollout + artifact filter + selection | verifier 应按 failure class 分层 |
| completion/resume | CI rebuild/no diff；publish rollback | marker + harness hash | 还必须补 input/source/executor identity |
| learning | examples/references 固化 craft rules | adoption 后 reflection 入 domain library | 只允许 verified/adopted evidence 进入长期层 |
| 已知缺口 | flaky load test、page-key collision、browser no-sandbox | stale input cache、stale grade、无 spend stop | 候选不可直接升 active contract |

## 经验沉淀

1. 当 Agent 生成任何 Markdown、图、卡片、索引或网页 projection 时，应优先从 canonical typed state 单向生成，并绑定 source identity/coverage/read-back，因为输出存在和视觉完整不证明底层事实一致；边界是 canonical state 本身也需来源审查。
2. 当一个高自由度 Skill 要跨 agent 稳定复用时，应优先把它拆为 agent-neutral contract、确定性 engine/verifier 与 host adapter，而不是复制一份超长项目 Skill，因为不同宿主的 loader、browser、sandbox 与 effect 权限不等价。
3. 当 Agent 自动提出 prompt/skill/harness 改动时，应优先走 `proposal → validation → probe → contrast → adoption → reflection`，并把未经 probe 或未 adopted 的内容留在 runtime/inbox，因为生成候选不等于获得长期发布权。
4. 当 workflow 支持 resume/cache 时，应优先让 reuse identity 覆盖 task prompt/source、harness、executor/model、policy/version 与 output integrity，因为只看 path、日期、run id 或 harness hash 会复用旧输入结果。
5. 当并发候选共享 run namespace 时，应优先冻结 denominator、使用 immutable unique labels 并在并发完成后确定性记账，因为 duplicate label 可能在总数正确时仍覆盖真实 candidate。
6. 当 deterministic verifier 有多个 failure class 时，应优先保留每个 verifier 的 attempted/status/coverage，而不是压成一个绿色总分，因为 model audit、line check、browser E2E 和人工 review 互不替代。
7. 当外部项目为了 benchmark 关闭 sandbox、开放网络或运行第三方 hooks 时，应优先放入隔离 disposable environment，并在报告中把这种配置标成实验前提，而不是迁移到 Hermes/OpenClaw 默认运行时。
8. 当本机完整 suite 与上游 check 冲突时，应优先保留两面真实证据并做最小定向复跑；单测复跑通过只能标 flaky/待核验，不能把原始失败抹成全绿。

## Hermes / shared hub 统一落地建议

### Candidate POC A：canonical projection receipt

`runtime/hermes/github-learning-poc/canonical-projection-receipt-v0/`

```json
{
  "canonical_id": "immutable-id",
  "source_hash": "sha256:...",
  "schema_version": 1,
  "coverage": {"expected": 5, "verified": 5},
  "projections": [
    {"kind": "markdown", "path": "relative/path", "hash": "sha256:...", "status": "verified"},
    {"kind": "svg", "path": "relative/path", "hash": "sha256:...", "status": "partial"}
  ],
  "terminal": "verified|partial|blocked|failed"
}
```

### Candidate POC B：input-bound harness run

`runtime/hermes/github-learning-poc/harness-input-identity-v0/`

```json
{
  "run_id": "stable-id",
  "input_identity": "sha256(instructions + relative-source-paths + bytes)",
  "harness_identity": "sha256(contract tree)",
  "executor_identity": "runner+version+model+policy",
  "proposal_id": "candidate-id",
  "probe_receipts": ["artifact-hash", "verifier-status"],
  "adoption": "selected|rejected|needs_validation",
  "derived_from": ["exact-evidence-id"],
  "terminal": "completed|stale|blocked|failed"
}
```

### 预期验收

- source 改动但 path/date 不变时，两个 POC 都必须拒绝复用旧 projection/run；
- verifier 未运行、coverage 不满或 browser/test blocked 时，不得 completed；
- proposal rejected/fallback 不得写成 adopted lesson；
- derived grade/library/report 必须随 upstream identity 失效；
- 全部使用 synthetic fixture，不连接 provider/browser 外网、不改 config/cron/skills/curated。

## Skill 升格总判断

- **今日不创建新 shared skill，不写 curated active fact。**
- Anatomy：机制判断 **需二次验证**；完整视觉 Skill **暂不沉淀**。先抽象 canonical projection + independent verification，与 shared-memory/governance/GitHub-learning 去重。
- Harness²：**需二次验证**。先修正/验证 input-bound resume 与 stale derived artifact 失效，再考虑迭代现有 orchestrator/self-reflection skill；当前 #65/#44 阻止直接迁移。
- 若两个 POC 能在现有 GitHub-learning 或 autonomous-learning workflow 中真实发现 stale projection/cache 误判，再更新已有 class-level skill；否则只保留 runtime/inbox 研究。

## 明日继续

1. 建立 `harness-input-identity-v0` 的 6 个 synthetic fixtures：unchanged、instruction changed、source added/changed/removed、executor identity changed、stale grade/library。
2. 建立 `canonical-projection-receipt-v0` 的 5 个 fixtures：same-key page collision、missing projection、stale source hash、verifier blocked、read-back mismatch。
3. 复核 Anatomy full suite 的 page-load failure：在同 commit 连跑该单测与全套受控并发，确认是 fixture race、Chrome load event 竞争还是宿主负载；未复现前保持“待核验”。
4. 继续跟踪 Harness² #65/#44 是否进入 default branch，并固定修复 commit 后做本机 reproducer，不用 issue prose代替合并事实。

## 候选反哺

### Candidate Facts

- [ ] topic: derived projection 必须绑定 canonical source identity + coverage + read-back | evidence: Anatomy canonical geometry→多 verifier→publish rebuild；现有 shared raw/canonical/projection 分层 | 建议: update 既有 shared-memory/GitHub-learning contract（POC 后） | 安全级别: low
- [ ] topic: resume identity 必须覆盖 task source 而非仅 harness | evidence: Harness² `runmark.py` + open issue #65 的无凭证 reproducer | 建议: create candidate fixture，暂不写 active fact | 安全级别: medium
- [ ] topic: adoption 后 reflection 才可进入长期 library | evidence: Harness² `selection.py:reflect_adoption` 与 shared hub candidate-first governance | 建议: update 既有 autonomous-learning contract（去重后） | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: canonical-projection-receipt-v0 | 可复用场景: GitHub 日报、Obsidian copy、卡片/图/索引生成 | 是否建议 shared: yes（仅 POC 通过后更新已有 skill） | 原因: 跨 agent 横切，但与 shared-memory/GitHub-learning 重叠
- [ ] 名称: input-bound-harness-run-v0 | 可复用场景: 自主学习 resume/cache、candidate probe、grade/library projection | 是否建议 shared: yes（仅 POC 通过且 stale invalidation 完整后） | 原因: 可补现有 orchestrator 的 identity 缺口，不应创建 Harness² 专属 skill

### Candidate Open Questions

- [ ] 问题: 当前 GitHub-learning orchestrator 的知识库 copy 是否记录 report content hash，还是只按日期/path 判断？ | reason: gap | priority: high
- [ ] 问题: autonomous-learning run-state 的 resume identity 是否覆盖 instruction/source/agent/model/policy 版本？ | reason: gap | priority: high
- [ ] 问题: Anatomy full-suite page-load 失败是否为 Node test 并发导致的真实 race？ | reason: conflict | priority: medium
- [ ] 问题: Harness² #65/#44 的修复是否会级联失效 experience library 与旧 grade，而非只删 summary？ | reason: gap | priority: high

### 不应自动落地

- 不自动安装 Anatomy Skill，不把其 domain-specific 视觉规则整包复制进 shared。
- 不运行未知 HTML/JS，不用 `--no-sandbox` Chrome 处理不可信页面，不自动提交 gallery PR。
- 不运行 Harness² 真实 benchmark/provider，不关闭 Hermes approvals/sandbox，不开放 benchmark egress。
- 不把 GitHub advisory 空数组、Dependabot 404 或窄 pip-audit 0 findings 表述为“无漏洞”。
- 不把 issue reproducer 直接写成已修复事实；只在修复合并、固定 commit、本机复验后晋升。
- 不自动修改 Hermes/OpenClaw 配置、model、provider、cron、secret 或 curated active facts。

## 知识库路径

审计通过后由 orchestrator 复制到 `03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-10-19-GitHub热门项目学习日报.md`；此处使用知识库根相对路径，避免把宿主绝对路径写入可迁移知识内容。
