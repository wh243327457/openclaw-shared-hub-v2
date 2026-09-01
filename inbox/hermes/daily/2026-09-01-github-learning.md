---
type: case
status: archived
created: 2026-09-01
updated: 2026-09-01
domain: learning
tags: [github-learning, agent-engineering, lifecycle, benchmark]
related:
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/00-每日学习索引]]"
  - "[[03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-08-31-GitHub热门项目学习日报]]"
---

# 2026-09-01 GitHub 热门项目学习报告

> 执行者：Hermes（当前 OpenClaw 运行时不存在；本次未调用 OpenClaw）  
> 查询时间：2026-09-01T07:30:35+08:00 至 07:34:14+08:00  
> 发现方法：GitHub Search API 查询 `created:>=2026-08-01` 并按 Stars 降序；所有 Stars、Forks、Language、License、updated/pushed 时间取 GitHub repository/license API。  
> 深读固定提交：`anywhere-labs/dsh-desktop@e71a9ef0b168763d422042835a8c3b7d6d809800`；`pathwaycom/arc-task-gen@20b2203064b09f60f7925a191d75c11d72277f35`。动态热度快照与固定源码 revision 分开记录。

## 今日结论

今天深挖的是两种“**生成与变更都必须保留分布/生命周期约束**”的实现：DSH Desktop 用不可变 startup generation 统一拥有 Host 与本地资源，并用短期 preview、generation revalidation 和幂等 release 约束恢复副作用；arc-task-gen 用 joint slot、slot recycling、合并 novelty loop 和显式 `converged/stalled` 状态约束生成集。共同原则是：**当系统会恢复、重试或再生成时，应优先固定权威 identity/slot，先验证再变更，并把“停止了”和“满足目标”分成不同终态。**

### 今日真实验证摘要

- DSH Desktop：固定 HEAD `e71a9ef...`；在未安装全仓依赖的情况下运行 dependency-free architecture gate，真实结果 `2 passed / 0 failed`。未运行 Yarn `check`、Electron、Windows/macOS 打包或真实恢复流程，这些均待核验。
- arc-task-gen：固定 HEAD `20b2203...`；对 5 个 Python 脚本执行 `python3 -m py_compile`，exit 0。未配置模型/embedding API，未生成任务，也未复现 README 的 400-task 数据；生成质量与 benchmark 声明待核验。
- 两仓 GitHub `SECURITY.md` contents API 均返回 404；Dependabot vulnerability-alerts endpoint 对当前凭据也返回 404。因此不能声称“无已知漏洞”。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 206,425 | 23,962 | TypeScript | MIT | 2026-08-31T16:03:39Z | 前两日已深读；今日避免重复 |
| [anywhere-labs/dsh-desktop](https://github.com/anywhere-labs/dsh-desktop) | 22,448 | 1,102 | TypeScript | MIT | 2026-08-30T14:54:54Z | **深读：generation ownership、恢复预览与副作用重验** |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | 19,671 | 2,288 | Python | MIT | 2026-08-31T23:31:36Z | 图像真实性与误用边界高，不在无人值守任务安装 |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 19,666 | 1,175 | Rust | MIT | 2026-08-28T02:13:16Z | 已深读；继续观察 mixed-page coverage |
| [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | 13,890 | 2,419 | Python | CC0-1.0 | 2026-08-31T13:19:38Z | 目录许可不覆盖每个第三方插件的 license/effect |
| [pathwaycom/arc-task-gen](https://github.com/pathwaycom/arc-task-gen) | 9,398 | 62 | Python | MIT | 2026-08-11T09:52:10Z | **深读：联合约束采样、slot recycling、收敛与 benchmark contamination** |
| [yjh051108/dsh-routing-suite](https://github.com/yjh051108/dsh-routing-suite) | 6,998 | 141 | JavaScript | MIT | 2026-08-28T19:03:44Z | 路由候选；本日不展开 |
| [FareedKhan-dev/kimi-k3-in-c](https://github.com/FareedKhan-dev/kimi-k3-in-c) | 6,909 | 1,117 | C | Apache-2.0 | 2026-08-26T07:36:53Z | 低层实现候选；模型/权重许可需另审 |
| [sapientinc/PRAXIST](https://github.com/sapientinc/PRAXIST) | 5,447 | 474 | Python | NOASSERTION | 2026-08-31T06:44:10Z | 顶层许可未断言，只观察不迁移源码 |
| [tobi/walgit](https://github.com/tobi/walgit) | 2,362 | 129 | Rust | MIT | 2026-08-27T01:50:20Z | WAL/Git 数据工具候选；本日不展开 |

> 注：Stars 是 2026-09-01 07:30–07:32 +08:00 的 API 快照，会继续变化；GitHub 顶层 License 不能替代依赖、数据、模型、发布物和品牌的完整合规审查。

## 深读项目

### 1. anywhere-labs/dsh-desktop

- **一句话判断**：值得学的不是 Electron 外壳本身，而是“每次启动都是一个不可变 generation；资源、Host、恢复授权和 profile 均不得跨 generation 漂移”的生命周期外壳。
- **解决的问题**：替代把窗口、托盘、Host、subprocess 与恢复操作散落在全局 singleton 中的旧做法；也替代“用户在 UI 点过确认，所以稍后仍可执行”的长效授权假设。
- **URL / API 快照**：https://github.com/anywhere-labs/dsh-desktop ；**Stars 22,448 / Forks 1,102 / Language TypeScript / License MIT**；`updated_at=2026-08-31T23:16:01Z`，`pushed_at=2026-08-30T14:54:54Z`，repository API `open_issues_count=301`，default branch `master`。
- **固定提交**：[`e71a9ef0b168763d422042835a8c3b7d6d809800`](https://github.com/anywhere-labs/dsh-desktop/commit/e71a9ef0b168763d422042835a8c3b7d6d809800)，提交时间 `2026-08-30T14:07:52Z`。
- **Release / issue 证据**：[`v2.0.4`](https://github.com/anywhere-labs/dsh-desktop/releases/tag/v2.0.4) 发布于 `2026-08-28T17:54:51Z`，明确提示上游 `v0.1.2-alpha.1` 有破坏性更新；查询时 issue [#737](https://github.com/anywhere-labs/dsh-desktop/issues/737) 报告升级后插件导致无法启动，[#732](https://github.com/anywhere-labs/dsh-desktop/issues/732) 报告解析到全局旧版 runtime。说明 pinning 与 recovery 不是装饰性设计。
- **来源交叉核验**：README、`docs/architecture.md`、release v2.0.4、issues #737/#732、`upstream.json`、源码、tests 目录、package manifests 与本机定向 architecture test。

#### 架构/实现与数据流

1. Electron main 获取单实例锁并选定 profile；launcher 创建一个 startup generation。
2. generation 绑定唯一 Cordis Host，并用 `own(release)` 收集窗口、托盘、listener、subprocess 等本地资源的幂等释放回调。
3. Host 提供 HTTP/WebSocket carrier，sandboxed renderer 只访问同源 Web surface，不直接得到 Electron API。
4. profile/mode 切换先 dispose 当前 generation，再创建下一代；旧 generation 的 service/window/handle 不得复用。
5. 恢复操作先读取当前 generation/profile 的快照，生成 5 分钟有效的一次性 preview；执行时重新验证 generation、target、snapshot identity 和可变性，再调用官方 plugin/remove 或 checkpoint restore 流程。
6. 恢复变更前若 Host 不能在超时内 quiesce，则 mutation unavailable；这避免在活跃 Host 持有文件/进程时并发改 profile。

```text
用户 -> Electron main / profile launcher
     -> DesktopStartupGeneration (generation id + resource owner)
     -> Cordis Host -> HTTP/WebSocket carrier -> sandboxed renderer
                   -> upstream services + desktop-owned plugins + third-party plugins
恢复 UI -> preview(profile, generation, target, snapshot, expiry)
       -> execute-time revalidation -> quiesce Host -> mutation -> readback
```

#### repo tree 摘要

```text
dsh-desktop/
├── deepseek-harness/                   # 固定上游 Git submodule；不在桌面分支修改
├── vendor/dsh-runtime/0.1.2-alpha.1/  # 打包 runtime tgz + manifest/sha256
├── dsh-plugin-desktop/
│   ├── src/                            # Electron host、profile、startup/recovery、network、update
│   ├── src/client/                     # Desktop Web client 插件面
│   ├── src/native-ui/                  # setup/recovery/dialog/profile 原生窗口 UI
│   ├── tests/                          # 生命周期、恢复、打包、网络、secret mask 等测试
│   └── scripts/                        # release、runtime closure、license、package verification
├── dsh-community-market/              # catalog contract、adapters、受限 HTTP、安装服务
├── dsh-community-fabric/              # 插件 schema/RFC/兼容层文档
├── scripts/                            # repo 级 architecture/layout/vendor gates
├── patches/                            # 显式 package patches
├── docs/architecture.md                # Host/client/native runtime 边界
├── upstream.json                       # 上游 commit/version/runtime manifest pointer
├── package.json / yarn.lock            # Yarn 4 workspace 与锁文件
└── LICENSE                             # MIT
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `dsh-plugin-desktop/src/startup-generation.ts` | 一代启动资源 owner | 唯一 Host、幂等 `own/release`、逆序释放、恢复前限时 quiesce |
| `dsh-plugin-desktop/src/startup-recovery-controller.ts` | 恢复授权控制面 | generation/profile 绑定、5 分钟 preview、one-shot token、execute-time target/snapshot revalidation |
| `dsh-plugin-desktop/src/workspace-admission.ts` | workspace 进入门 | 并发目录选择合并；Windows volume allow/confirm/block 策略在持久化前执行 |
| `docs/architecture.md` | 权威架构说明 | Host/Web carrier/sandboxed renderer、generation 与 platform adapter 边界 |
| `upstream.json` | 上游 provenance | 固定上游 commit `cd5ef814...`、source/runtime version `0.1.2-alpha.1` |
| `vendor/dsh-runtime/0.1.2-alpha.1/manifest.json` | 运行时制品清单 | 每个 tgz 的 name/version/size/SHA-256；这是 byte provenance，不是签名 |
| `scripts/market-dependency-direction.mjs` | 架构依赖 gate | 拒绝 Market source import Desktop implementation；本机定向测试 2/2 通过 |

#### ⭐ 源码精读

**代码块 1：`DesktopStartupGeneration.own()` 把每个 effect 转成幂等 release，并由 generation 统一持有。**

```ts
own(release: () => void): () => void {
  this.assertActive()
  let active = true
  const releaseOnce = (): void => {
    if (!active) return
    active = false
    release()
  }
  this.releases.push(releaseOnce)
  return releaseOnce
}
```

逻辑摘要：调用方可以把同一个 `releaseOnce` 同时注册为 Host effect 和最终 shutdown cleanup；无论哪条路径先触发，底层资源最多释放一次。边界是 `release()` 自身若不是同步幂等或抛错，仍需上层收集 failure。

**代码块 2：`quiesceForRecovery()` 用真实 Host dispose 与超时竞速，失败时拒绝恢复 mutation。**

```ts
async quiesceForRecovery(): Promise<boolean> {
  if (this.released) return false
  if (this.host === undefined) return true
  this.hostDisposeTask ??= this.disposeHostForRecovery()
  const timedOut = new Promise<false>(resolve => {
    timeout = setTimeout(() => {
      this.options.logger.error(
        `${BIN_NAME}: plugin Host did not stop in time; mutating recovery actions are unavailable`,
      )
      resolve(false)
    }, this.quiesceTimeoutMs)
  })
  return await Promise.race([this.hostDisposeTask, timedOut])
}
```

逻辑摘要：恢复不是“弹窗确认后直接改文件”，而是先证明当前 generation 的 Host 已安静；超时返回 false，不把未知活跃状态当成功。边界是 Promise timeout 不会强制杀死卡住的 dispose，后续仍需人工/进程级恢复。

**代码块 3：恢复执行重新绑定 preview 的 profile、generation、有效期，并在调用副作用前再次授权。**

```ts
async executeUninstall(previewId: string): Promise<DesktopStartupRecoveryUninstallResult> {
  this.assertCurrentGeneration()
  if (!UNINSTALL_PREVIEW_ID_PATTERN.test(previewId)) throw this.expiredPreview()
  this.assertOperationAvailable()
  const preview = this.uninstallPreviews.get(previewId)
  this.uninstallPreviews.delete(previewId)
  if (preview === undefined || preview.expiresAt <= this.now()
    || preview.profileName !== this.profileName || preview.generationId !== this.generationId) {
    throw this.expiredPreview()
  }
  this.operationActive = true
  try {
    this.authorizeUninstall(preview.packageName)
    await this.options.uninstallPlugin(preview.packageName)
    this.assertCurrentGeneration()
    // readback: inventory 中仍存在则 operation-failed
  } finally {
    this.operationActive = false
  }
}
```

逻辑摘要：preview 是一次性且短期有效的 proposal，不是持续授权；执行前重新读 inventory 验证 target 仍可卸载，执行后又检查 generation 与 inventory readback。

**代码块 4：workspace admission 把平台存储风险留在 host-owned gate。**

```ts
async validateDirectory(path: string): Promise<boolean> {
  const decision = evaluateWindowsWorkspaceVolume(
    this.options.platform, path, this.options.volumeQuery,
  )
  if (decision.action === 'allow') return true
  if (decision.action === 'confirm') {
    const result = await this.options.showMessageBox(/* removable NTFS/ReFS warning */)
    return result.response === 0
  }
  await this.options.showMessageBox(/* block exFAT/FAT32/network/uninspectable */)
  return false
}
```

逻辑摘要：renderer/插件只能请求选择；真实平台检查和最终允许/拒绝由 Electron host 执行。此 gate 处理 durability/compatibility，不等于对 workspace 内容完成安全扫描。

#### 依赖分析与供应链风险

- 根 workspace：Yarn `4.18.0`，Node `^22.19.0 || >=24.0.0`；workspaces 为 desktop/fabric/market。
- 关键运行依赖：`electron 43.3.0`（peer/dev）、Cordis packages、固定 `@deepseek-ai/dsh 0.1.2-alpha.1` 系列、`pnpm 11.8.0`、`koffi 3.1.5`、`selfsigned 5.5.0`、`yaml`、`semver`、React。
- 供应链优点：`yarn.lock`；上游 commit/version 指针；vendored tgz manifest 带 size/SHA-256；package patch 显式入库；有 `verify:licenses`、runtime closure 与 packaged-runtime gates。
- 供应链风险：大量 alpha 版本的 DSH package；Electron/native modules（koffi、node-pty、sharp 等）与打包链扩大 attack/ABI surface；仓库内有大量 vendored tgz 和 patches，升级需重新核验；SHA-256 证明 bytes 与 manifest 一致，不证明发布者身份或 reproducible build。
- 本机未执行 `yarn install --immutable` 或 production dependency audit，原因是本任务不应在无人值守研究中安装庞大高权 Electron/runtime 依赖；漏洞可达性待核验。

#### 可复用经验

- 当 profile/runtime 切换会让旧句柄失效时，应优先以不可变 generation 统一拥有资源，并禁止跨代缓存，因为 display name 或当前 path 不能证明仍是同一运行实例；边界是进程内 generation 不等于 OS sandbox。
- 当恢复操作先展示影响、后执行副作用时，应优先使用短期 one-shot preview，并在执行点重验 scope/target/revision，因为早期确认会随状态变化而过期；边界是不可逆外部 effect 还需幂等键与人工恢复。
- 当宿主准备修改插件/profile 状态时，应优先先 quiesce 当前 Host 并在超时后 fail closed，因为活跃进程树可能仍持有文件和缓存；边界是 cooperative dispose 不能终止失控进程。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/generation-preview-gate-v0/` 做纯 Python/JSON fixture，不运行 Electron/DSH：

1. 建 `generation_id/profile/target/revision/expires_at/used` preview schema；
2. 覆盖 stale generation、expired、replayed、target changed、quiesce blocked、effect succeeded but readback failed；
3. 要求 exactly-one terminal：`completed|blocked|needs_verification|failed`；
4. 所有 effect 用 fake adapter，不改 Hermes 配置、cron、skills 或 curated。

#### 风险边界

- **License**：GitHub license API 与仓库 LICENSE 均为 MIT；但依赖、DeepSeek 商标、vendored tgz、第三方插件和发布 assets 仍需单独合规审查。
- **维护活跃度**：固定 HEAD 是 2026-08-30，近 5 个 commit 覆盖 recovery report、PTY relay 与 version header；repository API 有 301 open issues，说明活跃但仍在快速变化。
- **安全风险**：Electron host、shell/terminal、插件安装、局域网入口、update、native modules 都是高权面；README 当前还提示 LAN 无鉴权，而 v2.0.4 release 写 HTTPS + system-generated token，文档与 release 语义存在 drift，**待核验实际固定 HEAD 行为**。
- **稳定性/局限**：v2.0.4 release 明确上游 breaking changes；issues #737/#732 显示插件和全局旧 runtime 可导致启动/解析失败。今日只跑 2 个 architecture unit tests，不能外推全仓、安装包或真实恢复稳定。
- **不适用**：不建议直接把桌面 runtime 引入 Hermes/shared hub；共享中台需要的是窄生命周期契约，不是第二个 Host/插件市场/更新器。

#### ⭐ Skill 升格判断

**需二次验证。** 可候选迁移的是 `generation-bound-preview-effect-gate` 契约；不能直接迁移 DSH Desktop skill/runtime。先与已有 `verification-first`、effect-scope、completion receipt、self-healing 和 config-target-routing 能力去重，并完成 stale/replay/readback fixtures 后再决定是否更新现有 shared skill；今日不创建 shared skill、不写 curated active fact。

#### ⭐ Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/generation-preview-gate-v0/`。
- schema：`preview.json` 包含 `agent/run/generation/profile/canonical_target/revision/effect/expires_at/used`。
- engine：纯函数 `prepare_preview(state, request)` 与 `authorize_execute(state, preview)`；adapter 只接 fake effect。
- 审计接入候选：给 `scripts/github_learning_orchestrator.py` 的产物发布阶段增加 generation/report hash/readback，而不是自动修改 Hermes config。
- 若跨 agent 稳定：更新现有 verification/effect contract skill；只有去重后确有独立语义才在 `capabilities/skills/` 新建目录并同步 manifest。
- OpenClaw 路径仅作为未来 adapter 候选；当前运行时不存在，本日不调用、不写其配置。

---

### 2. pathwaycom/arc-task-gen

- **一句话判断**：值得学的不是“让 LLM 造 benchmark”，而是它把分布约束抽成可回收 slot，并将结构校验、集合内去重、公共评测相似度过滤合并进一个明确的 convergence loop。
- **解决的问题**：替代直接在公开 ARC-AGI-1 上反复评测、无法区分能力与记忆的旧做法；也替代独立采样 rows/colors/pair count 导致不自然组合，以及 sequential one-pass filters 相互破坏保证的实现。
- **URL / API 快照**：https://github.com/pathwaycom/arc-task-gen ；**Stars 9,398 / Forks 62 / Language Python / License MIT**；`updated_at=2026-08-31T23:27:59Z`，`pushed_at=2026-08-11T09:52:10Z`，repository API `open_issues_count=1`，default branch `main`。
- **固定提交**：[`20b2203064b09f60f7925a191d75c11d72277f35`](https://github.com/pathwaycom/arc-task-gen/commit/20b2203064b09f60f7925a191d75c11d72277f35)，提交时间 `2026-08-11T09:52:10Z`。
- **Release / issue 证据**：latest release API 返回 404（查询时没有 GitHub release）；唯一 open issue [#1](https://github.com/pathwaycom/arc-task-gen/issues/1) 声称在一组变换下 ARC-AGI-1 eval 的 375/400 可在 ARC-AGI-2 public training 中找到，并给出外部复现仓库。**该 375/400 数字是 issue 作者声明，本机未运行其复现，待核验**；它仍足以提示 content hash 不覆盖语义等价变换。
- **来源交叉核验**：README、`instructions.md`、issue #1、关键源码、`pixi.toml/pixi.lock`、GitHub API 与本机 py_compile。

#### 架构/实现与数据流

1. 首次运行下载 ARC-AGI-1 eval 作为参考分布并缓存；生成任务不把 eval grids/rule descriptions 送入普通 generation prompt。
2. `sample_joint_slots` 从单个 anchor task 整体读取 input dimensions、非背景颜色数、train/test 数，保留自然 covariance。
3. 每个 API call 只生成 1 个任务；parser 解析严格 JSON，结构 validator 检查 train/test、二维矩形网格与 cell 0–9。
4. transformation description 被 embedding；集合内矩阵找 near-duplicate，另一个矩阵找与 eval descriptions 过近的任务。
5. 两类 novelty filter 与 malformed check 在同一轮取 union；被删除任务的原 slot 被回收，避免 replacement 重新抽样导致幸存分布偏移。
6. 循环只有在无删除且数量达到 N 时标 `converged`；连续 3 轮 removal 不下降标 `stalled`，达到轮数上限也只 warning，不应把“脚本 exit 0”外推为 clean benchmark。
7. stratified wrapper 复用 base loop，只替换 slot plan 和 prompt；支持 category/mechanic plan 与 `--dry-run-plan`。

```text
public ARC eval -> joint slot/profile (不把 grid/rule 放进 generation prompt)
                -> one task per model call -> strict JSON parse
                -> structural validation
                -> intra-set description similarity ┐
                -> eval-description similarity      ├-> union remove
                -> malformed                         ┘
                -> recycle original slot -> regenerate
                -> converged | stalled | round-ceiling
                -> tasks.json + separated/ + sanity_check.json
```

#### repo tree 摘要

```text
arc-task-gen/
├── generate_tasks.py             # base generator、joint slots、validation、novelty convergence
├── generate_tasks_stratified.py  # category/mechanic plan；复用 base engine
├── label_eval_tasks.py           # 从 train pairs 生成 category/mechanic labels
├── describe_eval_tasks.py        # 为 eval 构造 rule descriptions，启用 cross-sim filter
├── visualize_tasks.py            # 任务可视化
├── instructions.md               # 安装、输出、方法与 caveats
├── README.md                     # 项目/论文入口与 benchmark 声明
├── pixi.toml / pixi.lock         # Python >=3.12 与锁定环境
├── assets/                       # 结果图
└── LICENSE                       # MIT
```

> tree 中没有 committed `data/`：README 明确 eval cache、labels、generated sets 不提交，以避免新任务公开后被抓入训练集。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `generate_tasks.py` | 主生成与收敛 engine | joint slot、embedding filters、structural validation、slot recycling、stall detection、sanity artifact |
| `generate_tasks_stratified.py` | 分层实验 wrapper | anchor profile、category/mechanic plan、dry-run plan；monkey-patch base sampler/generator |
| `label_eval_tasks.py` | 评测任务标签器 | 只看最多 3 个 train pairs；闭集 category/mechanic；unknown mechanic 回落 `other` |
| `instructions.md` | 方法/风险说明 | 公开集污染动机、输出、 measured claim、solvability/wording/id leakage caveats |
| `pixi.toml` | 依赖入口 | Python >=3.12、numpy/httpx/openai/matplotlib |

#### ⭐ 源码精读

**代码块 1：`sample_joint_slots()` 以单个 anchor 整体抽样约束，而不是独立拼接边际。**

```python
def sample_joint_slots(eval_tasks: dict, n: int) -> list:
    task_ids = list(eval_tasks.keys())
    slots = []
    for _ in range(n):
        anchor_id = random.choice(task_ids)
        task = eval_tasks[anchor_id]
        input_grids, colors = [], set()
        for pair in task["train"] + task["test"]:
            for field in ("input", "output"):
                g = pair.get(field)
                if field == "input":
                    input_grids.append((len(g), len(g[0])))
                for row in g:
                    colors.update(v for v in row if v != 0)
        rows, cols = random.choice(input_grids)
        slots.append({"rows": rows, "cols": cols, "colors": len(colors),
                      "n_train": len(task["train"]), "n_test": len(task["test"]),
                      "anchor": anchor_id})
    return slots
```

逻辑摘要：slot 保留 size/color/pair-count covariance，避免 2×2 grid + 9 colors 等不自然组合。边界是它只匹配可量化表面分布，不证明认知难度或规则分布一致。

**代码块 2：`find_duplicate_clusters()` 先单位化 embedding，再用矩阵乘法和 union-find 构造 cluster。**

```python
def find_duplicate_clusters(descriptions: dict, threshold: float = DEDUP_THRESHOLD) -> list:
    task_ids = list(descriptions.keys())
    if len(task_ids) < 2:
        return []
    m = _embed([descriptions[tid] or "no description" for tid in task_ids])
    sim = m @ m.T
    pairs = np.argwhere(np.triu(sim, k=1) >= threshold)
    parent = list(range(len(task_ids)))
    # union matched pairs, then return groups of size >= 2
```

逻辑摘要：避免纯 Python 重复求 norm；transitive union 把 A≈B、B≈C 归成一组。边界是相似度依赖模型与文字描述，机制相同但表述不同可漏检；cluster 中保留第一项也是任意策略。

**代码块 3：`validate_tasks()` 只证明结构可评分，不证明规则可解。**

```python
def validate_tasks(tasks: dict) -> list:
    errors = []
    for task_id, task in tasks.items():
        if "train" not in task or "test" not in task:
            errors.append(f"{task_id}: missing 'train' or 'test' key")
            continue
        if len(task["train"]) < 2:
            errors.append(f"{task_id}: fewer than 2 training pairs")
        for split in ("train", "test"):
            for i, pair in enumerate(task[split]):
                for field in ("input", "output"):
                    grid = pair.get(field)
                    # 2-D, non-empty, rectangular, integer cells 0..9
    return errors
```

逻辑摘要：它保护 downstream harness 不被 ragged/out-of-range task 拖垮，但没有执行 transformation rule，也没有盲测 inferability。README 也明确 solvability 未程序化验证。

**代码块 4：合并收敛循环取三类失败的 union，并回收原 slot。**

```python
for dedup_round in range(1, MAX_DEDUP_ROUNDS + 1):
    clusters = find_duplicate_clusters(all_descriptions, DEDUP_THRESHOLD)
    flagged = find_eval_similar(all_descriptions, eval_descriptions,
                                EVAL_SIMILARITY_THRESHOLD)
    malformed = invalid_task_ids(all_tasks)
    to_remove = set()
    for group in clusters:
        to_remove.update(group[1:])
    to_remove.update(flagged.keys())
    to_remove.update(malformed)
    if not to_remove and len(all_tasks) >= N:
        converged = True
        break
    slots = [slot_by_task[tid] for tid in to_remove if tid in slot_by_task]
    # regenerate replacements with recycled slots + avoidance descriptions
```

逻辑摘要：一个 replacement 必须在下一轮同时通过所有 filters；slot recycling 维持第一轮分布计划。边界是 convergence 只相对于当前 detectors/thresholds，不能证明真正原创、无污染或可解。

**代码块 5：stratified plan 在真正调用 API 前可 dry-run 并落下完整 slot plan。**

```python
def main(argv: list[str] | None = None) -> int:
    profiles = load_anchor_profiles()
    if args.mechanics is not None:
        _PLAN = build_mechanic_plan(profiles, args.per_mechanic, args.seed, requested)
    else:
        _PLAN = build_category_plan(profiles, args.n, args.seed, args.anchor_mode)
    write_plan(_PLAN, args.plan_output)
    if args.dry_run_plan:
        return 0
    base = import_base_generator()
    base.sample_joint_slots = sample_plan_slots
    base.generate_one = make_generate_one(base)
    return int(base.main())
```

逻辑摘要：昂贵 generation 前先暴露 experiment design，使 category/mechanic counts、shape relation 和 borrowed pools 可审查。边界是 monkey-patching base globals 增加耦合，base API 变化可能静默破坏 wrapper，缺少自动 tests 是风险。

#### 依赖分析与供应链风险

- `pixi.toml`：Python `>=3.12`，`numpy >=1.24`、`httpx >=0.24`、`openai >=1.0`、`matplotlib >=3.11.1,<4`；存在 `pixi.lock`。
- 运行还访问 GitHub codeload（下载 fchollet/ARC-AGI master tarball）和 OpenAI-compatible chat/embedding endpoint；默认 generation model 与 embedding model 均可由 env 改写。
- 供应链优点：依赖锁；公开 ARC 数据仅缓存不提交；标准 ARC output；env 支持本地 endpoint。
- 风险：`DATASET_TARBALL` 指向 `refs/heads/master` 而非 immutable commit，参考集可漂移；下载后未见 digest/signature 验证；模型 endpoint 会接收生成 prompt/已有 descriptions；大量并发（默认 64）有费用、rate-limit 和 partial failure 风险；embedding model/threshold 更换会改变 detector 语义。
- 今日只做 `py_compile`，未创建 pixi 环境、未做依赖漏洞扫描；Dependabot endpoint 不可用，安全状态待核验。

#### 可复用经验

- 当生成结果必须匹配多个相关约束时，应优先从同一真实样本整体抽取 slot，而不是独立抽边际，因为独立组合会破坏 covariance；边界是匹配表面统计不等于匹配语义难度。
- 当多个 filter 会对 replacement 再产生影响时，应优先放进同一个迭代收敛循环并每轮验证全部 invariant，因为 sequential one-pass 会让后一阶段撤销前一阶段保证；边界是 detector 盲区仍会被稳定地“收敛”。
- 当过滤与 slot 属性相关时，应优先回收被删对象的原 slot 再生成，因为重新随机抽样会让幸存者选择偏差改变目标分布；边界是反复失败的 slot 需要 stall/人工审查，不能无限烧预算。
- 当程序因 stall 或上限停止时，应优先把 `converged` 与 `stopped` 分开，并让下游拒绝把 exit 0 当 clean benchmark；边界是 converged 也只代表已实现 checks 通过。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/convergence-slot-recycling-v0/` 做无需模型的 synthetic experiment：

1. 生成 20 个带 `slot={size,class}` 的候选，其中某 class 更易被 filter 删除；
2. 比较 fresh redraw 与 slot recycling 后的目标分布偏差；
3. 加两个互相干扰的 deterministic filters，证明 sequential one-pass 可留下 violation，而 merged loop 会重新检查；
4. 输出 `converged|stalled|ceiling|blocked`、round history 和 final coverage；不调用 provider，不复制 ARC 数据。

#### 风险边界

- **License**：GitHub license API 与仓库 LICENSE 均为 MIT；下载的 fchollet/ARC-AGI 在源码注释/README 标为 Apache-2.0。生成数据的权利、模型 provider 条款和论文/品牌不由顶层 MIT 自动覆盖。
- **维护活跃度**：固定 HEAD/最后 push 是 2026-08-11，latest release API 404；只有 1 个 open issue。热度高但 commit 历史短，维护持续性待观察。
- **安全/隐私**：prompt 会送往配置的 chat endpoint，descriptions 会送 embedding endpoint；私有 benchmark description 若外送可能提前泄露 benchmark。API key 只允许 env 注入，不能写 shared。
- **benchmark contamination**：issue #1 的 375/400 是未在本机复现的第三方声明，不能当已验证事实；但它揭示 canonical content hash 对 reorder/D4/color permutation 等等价变换可能失效。当前 description embedding 也不保证发现结构同构。
- **质量局限**：结构 validator 不检查 solvability；README 自述 blind sample 20 中 19 solvable 是项目方数据，本机未复现。task id 可能泄露规则，sanity file 含 intended rule；对 human blind test 必须重编号和隔离答案。
- **运行局限**：默认 64 并发与模型调用成本高；partial calls、rate limit、parse failure、stall 均可能出现。今天未生成任何 task，不能证明默认模型或阈值有效。
- **不适用**：不能直接用 LLM 生成集作为高风险评测、发布排行或训练数据治理的唯一依据；至少需要 blind human solvability sample、deterministic leakage checks、held-out policy 与版本化 receipts。

#### ⭐ Skill 升格判断

**需二次验证。** 可迁移的是通用的 `constraint-slot + merged convergence + slot recycling + explicit terminal` 工作流，不是 ARC generator 或其 prompts。先用 synthetic fixtures 证明 selection bias、filter interference 和 stall semantics，并与现有 orchestrator、verification-first、source-outcome 与 self-reflection skills 去重；今日不创建 shared skill、不写 curated active fact。

#### ⭐ Hermes/shared hub 落地路径

- POC：`runtime/hermes/github-learning-poc/convergence-slot-recycling-v0/`。
- 可先用于 GitHub 日学选题：把每天的技术栈/领域/新旧项目配额作为 slots；若项目因重复/许可/证据不足被过滤，补位时回收同类 slot，而不是任意选热门项目。
- 在 `scripts/github_learning_orchestrator.py` 的未来版本中，审计状态应区分 `completed/converged`、`stalled`、`ceiling`、`blocked`，并保存 round history；本日不改生产 orchestrator。
- raw report 继续写 `inbox/hermes/daily/`，实验写 `runtime/hermes/`；只有多日证据、去重与审查后才提出 curated fact。
- 若稳定跨 agent，优先更新现有 autonomous-learning/orchestrator skill contract；future-agent adapter 只消费 agent-neutral slot/terminal schema。OpenClaw 当前不存在，不执行适配。

## 经验沉淀

1. **当资源、授权或句柄会随重启/切换失效时，应优先用 immutable generation 统一标识和拥有，并在最终 effect 前重验 current generation；因为“同名 profile/同一路径”不能证明仍是同一运行实例，边界是进程内 generation 不提供 OS 隔离。**
2. **当危险变更需要先预览后执行时，应优先使用短期 one-shot preview + execute-time target/revision revalidation + effect readback；因为早期确认会过期，边界是不可逆外部 effect 仍需幂等键和人工恢复。**
3. **当生成对象必须满足多个相关约束时，应优先从同一 anchor 整体抽 slot，并在 replacement 时回收原 slot；因为独立抽边际或重新抽样会破坏 covariance/目标分布，边界是统计匹配不证明语义等价。**
4. **当多个检查会互相影响 replacement 时，应优先用 merged convergence loop 每轮重验全部 invariant；因为 sequential one-pass 会让后一阶段撤销前一阶段保证，边界是 detector 盲区仍可能收敛。**
5. **当循环因 stall、timeout 或轮数上限停止时，应优先输出显式非成功终态和 coverage，而不是依赖 exit 0；因为“停止运行”不等于“目标已满足”，边界是 completed/converged 也只覆盖已实现检查。**
6. **当依赖/数据来自 moving branch、vendored archive 或模型 endpoint 时，应优先固定 immutable revision、digest、provider/model 和 policy version；因为 lockfile/sha256 只覆盖部分供应链，边界是 digest 不是签名或可复现构建。**

### 今日与既有经验的关系

- generation-bound preview 是 2026-08-27 `scoped-effect-receipt` 与 2026-08-31 host-owned challenge 的具体生命周期证据，不宜另造宽泛 shared skill。
- merged convergence + slot recycling 为现有 GitHub-learning/orchestrator 补上“补位不得改变研究配额”和“audit stop != converge”的新候选语义，需 synthetic POC 后再评审。

## 明日继续

1. 建 `runtime/hermes/github-learning-poc/generation-preview-gate-v0/` 的 6 个纯 fixture：stale/expired/replay/target-changed/quiesce-blocked/readback-failed。
2. 建 `runtime/hermes/github-learning-poc/convergence-slot-recycling-v0/`，定量比较 redraw 与 recycle 的 slot distribution drift，并复现 two-filter interference。
3. 对 DSH Desktop 只在满足 Node `>=22.19`、隔离安装预算和无副作用前提时运行更窄 recovery tests；不启动 Electron、不安装插件。
4. 对 arc-task-gen 先运行 `--dry-run-plan` 所需的离线 prerequisite 检查；如缺 labels，返回 blocked，不调用模型；benchmark reproduction 继续待核验。
5. 继续观察 DSH issue #737/#732 与 arc-task-gen issue #1 是否有维护者证据、修复或复现结果。

## 候选反哺

### Candidate Facts

- [ ] topic: generation-bound preview/effect gate | evidence: `dsh-plugin-desktop/src/startup-generation.ts`、`startup-recovery-controller.ts`、固定提交 `e71a9ef...` | 建议: create candidate / 与 scoped-effect-receipt 去重 | 安全级别: medium
- [ ] topic: slot recycling preserves planned constraint distribution under selective filtering | evidence: `generate_tasks.py` convergence loop 与源码注释；尚未本地定量 POC | 建议: create candidate after fixture | 安全级别: low
- [ ] topic: benchmark contamination can evade byte/JSON hash under semantic transformations | evidence: arc-task-gen issue #1（第三方声明，未本机复现） | 建议: open question，禁止直接晋升 fact | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: `generation-preview-effect-gate` | 可复用场景: 恢复、插件变更、配置变更、人工确认后延迟执行 | 是否建议 shared: no（当前） | 原因: 与 effect-scope/completion/scoped-effect-receipt 重叠，先做 fixture 和去重
- [ ] 名称: `constraint-slot-convergence-loop` | 可复用场景: GitHub 选题补位、研究采样、合成数据、候选筛选 | 是否建议 shared: no（当前） | 原因: 需证明 redraw bias、filter interference、terminal semantics 后优先更新现有 orchestrator skill

### Candidate Open Questions

- [ ] 问题: DSH v2.0.4 固定 HEAD 的 LAN 实际是 README 所述“无鉴权”还是 release 所述“HTTPS + generated token”？ | reason: conflict | priority: high
- [ ] 问题: DSH recovery preview 在 Host quiesce timeout 后的底层 dispose task 如何最终回收，是否有进程级 kill/reconcile？ | reason: gap | priority: medium
- [ ] 问题: arc-task-gen issue #1 的 375/400 是否能在固定 dataset commits 上独立复现？ | reason: verification gap | priority: high
- [ ] 问题: description embedding detector 对 D4/color permutation/example reorder 的 recall 如何，阈值在模型变更后如何校准？ | reason: adaptation | priority: high
- [ ] 问题: merged loop hit stall/ceiling 时，CLI 是否应非零退出而不是只 warning？ | reason: contract gap | priority: medium

### 不应自动落地

- 不自动安装或运行 DSH Desktop、Electron、插件市场、第三方插件、update 或 LAN 服务。
- 不自动调用 arc-task-gen 的 chat/embedding provider，不生成或发布 private benchmark，不写任何明文 API key。
- 不自动修改 Hermes/OpenClaw 配置、模型、provider、cron、auth、skills 或 secrets；OpenClaw 当前不存在。
- 不复制 DSH vendored tgz/patches 或 ARC 数据到 shared core；clone、cache、POC 只留 `runtime/hermes/`。
- 不把 issue #1 的 375/400、README benchmark 或本日源码推断直接写入 curated active fact。
- 不用 audit keyword、exit 0、py_compile 或 2 个 unit tests冒充完整功能、安全或 benchmark 验证。
