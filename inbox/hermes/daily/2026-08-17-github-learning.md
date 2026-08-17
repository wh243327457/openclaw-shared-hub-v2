# 2026-08-17 GitHub 热门项目学习日报

> 执行器：Hermes。当前 OpenClaw runtime 不存在；本次未调用、启动、模拟或写入 OpenClaw。
> 研究窗口：2026-08-17 07:31-07:47（UTC+08:00）。Trending 由 `curl` 抓取；仓库元数据、license、commit、release、issues、PR 由 `gh api` 读取；源码由 `git clone --depth 1` 固定。
> 固定源码：`cordiverse/cordis@8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4`；`basecamp/omarchy@30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec`。
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-17/`。Trending HTML 为 538,645 bytes，SHA-256 `491430ec2f7bbe0f46932a57f23d931e101b317d4324f2f8be371cf77bcd6756`。
> 数据边界：Stars、forks、updated/pushed 是查询时动态值；release/issue 中的运行现象属于上游报告。本文只把明确列出的命令结果称为本机验证。

## 今日结论

今天的主线是：**生命周期隔离与升级可靠性都不能只靠“有一个 scope”或“命令成功”。Cordis 证明 service identity、effect ownership、cleanup ownership 是三件事；Omarchy 证明 update lock、阶段顺序、migration marker、snapshot receipt、pending transition 也必须分别建模。对 Hermes/shared hub 最有价值的反哺是 `scope-owned effects + prepare/apply/verify/commit receipt + explicit partial/blocked terminal`，而不是直接引入第三方 runtime 或自动修改配置。**

## 研究边界与真实验证

- **发现源**：`https://github.com/trending?since=daily` 的真实 HTML 解析出 7 个候选：`cordiverse/cordis`、`basecamp/omarchy`、`unslothai/unsloth`、`OpenCut-app/OpenCut`、`public-apis/public-apis`、`ToolJet/ToolJet`、`cactus-compute/needle`。Trending 只用于发现，数值均由 Repository API 二次核验。
- **筛选**：`needle` 昨日已深读；`public-apis` 偏资源清单；`unsloth`、`ToolJet` 的依赖/部署面超出当天验证预算；OpenCut README 明确默认分支处于从头重写阶段，当前线上仍是 classic。最终选择能形成 README/docs + issue/PR + source + 本机测试闭环的 Cordis 与 Omarchy。
- **Cordis 本机验证**：Yarn 4.14.1 成功解析 455 packages（约 170 MiB），定向 `core loader` 为 **15 files / 108 tests passed**；最终全仓为 **19 files / 163 tests passed**。中间一次全仓重跑出现 HMR config fixture `expected initial, received v3`，为 **162 passed / 1 failed**；随后 HMR 单独重跑 **26/26 passed**，最终全仓再跑 **163/163 passed**，因此标记为真实 flaky/时序风险而非稳定全绿。另在同一 commit 直接复现 issue #72：isolate 无 `Symbol.dispose`，调用共享 `fiber.dispose()` 后父、子 listener 一起被清除。
- **Cordis 供应链验证**：仓库无 committed lockfile。npm 首次解析因 forked `tsx@4.19.3-fix.3` 与 Vite 的 peer range 冲突而拒绝；使用仓库声明的 Yarn 4.14.1 可安装。production audit 返回 `No audit suggestions`；含 dev dependencies 的全量 audit 返回 3 条 `minimatch@9.0.3` high ReDoS advisory及若干 deprecated/unmaintained 工具链提示。
- **Omarchy 本机验证**：只运行所有高权命令均被 stub 的 4 个安全 shell test files，共 **20 个断言通过**：update sequence 3、migration 5、snapshot 4、update lock/ownership 6；6 个关键脚本 `bash -n` 通过。未执行 pacman、sudo/pkexec、Snapper、systemd、Quickshell、Hyprland、PAM、真实迁移或重启。
- **安全边界**：不自动修改 Hermes config/model/provider/auth/env/cron/skills；不执行 Omarchy 更新/迁移；不加载 Cordis plugin；不把 candidate 直接写入 `curated/memory/`。

## 项目速览

下表来自 2026-08-17 07:31-07:47（UTC+08:00）的真实 `gh api repos/{owner}/{repo}` 输出。Stars 会变化；License 是 GitHub Repository API 的仓库级 SPDX 识别，不覆盖依赖、发布制品、模型或数据。

| 项目 | Stars | Forks | Language | License | Updated / Pushed（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | 461,688 | 50,997 | Python | MIT | 2026-08-16T23:37:53Z / 2026-08-16T19:26:55Z | 高热资源清单，源码机制不适合今日深读 |
| [OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) | 83,862 | 8,280 | TypeScript | MIT | 2026-08-16T23:40:27Z / 2026-08-10T16:38:36Z | 默认分支重写中，线上仍用 classic |
| [unslothai/unsloth](https://github.com/unslothai/unsloth) | 72,546 | 6,542 | Python | Apache-2.0 | 2026-08-16T23:36:30Z / 2026-08-16T22:19:14Z | GPU/模型/依赖矩阵过大，留候选 |
| [ToolJet/ToolJet](https://github.com/ToolJet/ToolJet) | 40,002 | 5,329 | JavaScript | AGPL-3.0 | 2026-08-16T23:34:16Z / 2026-08-14T14:11:22Z | 大型平台，AGPL 与部署边界重 |
| [basecamp/omarchy](https://github.com/basecamp/omarchy) | 25,355 | 2,588 | Shell | MIT | 2026-08-16T23:34:36Z / 2026-08-16T18:29:44Z | **深读：更新阶段、marker、snapshot、lock transition** |
| [cactus-compute/needle](https://github.com/cactus-compute/needle) | 6,544 | 431 | Python | MIT | 2026-08-16T23:36:14Z / 2026-08-15T16:03:14Z | 昨日已深读，不重复 |
| [cordiverse/cordis](https://github.com/cordiverse/cordis) | 4,701 | 245 | TypeScript | MIT | 2026-08-16T23:39:47Z / 2026-08-13T13:48:22Z | **深读：effect/fiber/service identity 与 cleanup 缺口** |

### 筛选说明

- Cordis 仓库很小，固定 commit 只有 112 tracked files，但 packages/core、loader、HMR 已具备可核验的 effect/fiber/service/reload 状态机；同时 README 明示 API 未稳定，issues 正好暴露 isolate cleanup 与子 Agent terminal propagation 的边界。
- Omarchy v4.0.0 于 2026-08-14 发布，固定 HEAD 比 release tag commit `f0020448...` ahead 21 commits；它把更新、迁移、snapshot、并发锁、交互冲突和登录通知拆开，适合研究无人值守任务的 durable terminal。但 v4 刚发布且 open issues 739，不能把快速修复等同成熟。
- 两仓 Repository/License API 均返回 MIT；这只覆盖仓库源码。Cordis 的 npm transitive packages、Omarchy 的 Arch/AUR packages、主题/plugin、ISO 与外部工具仍需独立许可/供应链审查。

## 深读项目

### 项目 1：cordiverse/cordis

- **URL**：https://github.com/cordiverse/cordis
- **Stars / Forks / Language / License（GitHub API）**：**4,701 / 245 / TypeScript / MIT**。
- **查询时 updated / pushed**：2026-08-16T23:39:47Z / 2026-08-13T13:48:22Z。
- **固定源码版本**：`8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4`；commit `chore: update readme (#45)`，GitHub verification 为 verified。
- **release / issues / PR 证据**：Repository API 无 tags、无 GitHub Releases；core package 声明 `4.0.0-rc.8`。Open issue #72 报告 isolate cleanup 误伤父 context，本机已复现；#76 报告 Cordis-based DSH 的 child `ask_user_question` 被当普通 retryable error，最终烧到 max tokens，但 issue 正文明确根因在 DSH packages，不是 Cordis core。所谓修复 PR #73 仍 open，而且实际 diff 只改 `.editorconfig` 并把 `associate.spec.ts` 198 行测试替换成一行注释，**没有实现其描述的 cleanup fix**。

#### 一句话判断：为什么值得学

Cordis 值得学习的是把 plugin effect、依赖可用性、service identity 与 unload/reload 串成显式 Fiber 状态机；更值得警惕的是：**`Context.isolate()` 只改变 service identity 映射，并不自动拥有独立 cleanup fiber，更不是权限/进程沙箱。**

#### 解决的问题：替代了什么旧做法

1. 替代 plugin 随手注册资源、无法统一回收：`ctx.effect()` 收集 disposer，并按逆序释放。
2. 替代缺依赖时直接崩溃或不断轮询：Fiber 根据 injected implementation UID 计算 epoch，在依赖出现/消失时串行 reload/unload。
3. 替代单全局 service registry：`Context.isolate(name, label)` 用 symbol identity 选择同名 service 的可见实现；共享 label 可让多个 context 共享 realm。
4. 替代 config 改动直接覆盖 live state：`Fiber.update()` 先 schema validate，再经过 `internal/update` waterfall，最后重启 effect。
5. 替代每个 plugin 自写生命周期：Registry 归一化 function/class/object plugin 并创建 runtime + Fiber。
6. 但它没有解决 scope-owned cleanup：isolate 通过 prototype extension 复用父 fiber，导致 disposal authority 与 identity scope 不一致。

#### 架构 / 实现与数据流

```text
Context (Proxy + root Fiber)
  ├─ RegistryService.plugin(plugin, config)
  │    └─ Plugin.Runtime + child Fiber
  ├─ ReflectService
  │    └─ service implementation store / notify
  ├─ EventsService
  │    └─ hooks registered as current Fiber effects
  └─ isolate(service, label)
       └─ derived Context + changed service symbol map
          (注意：默认仍共享 parent/root fiber)

Fiber lane
  inject names → resolve visible Impl UID → epoch
      ├─ missing → PENDING / UNLOADING → dispose effects
      ├─ available/new UID → LOADING → execute plugin → ACTIVE
      └─ apply/config error → FAILED

loader lane
  YAML entry → local/global Realm labels → patch context maps
             → reload affected fiber → transfer implementation → notify
```

核心是两个正交维度：space 由 service symbol identity 决定，time 由 Fiber epoch/state/effects 决定。当前 bug 正来自两维未在 `isolate()` 上同时分离。

#### Repo tree 摘要

固定 commit 共 **112 tracked files**，其中 packages 96：

```text
cordis/
├── packages/core/
│   ├── src/context.ts       # derived context、isolate/intercept
│   ├── src/fiber.ts         # effect、epoch、reload/unload、terminal state
│   ├── src/registry.ts      # plugin normalize、runtime、Fiber 创建
│   ├── src/service.ts       # service provide/filter/config merge
│   ├── src/events.ts        # hooks、dispatch mode、effect-owned disposer
│   └── tests/               # 12 spec files
├── packages/loader/
│   ├── src/config/          # tree/group/isolate/entry
│   └── tests/               # 3 spec files
├── packages/hmr/            # watch、stash、reload/rollback
├── packages/include/        # config include/patch
├── packages/timer/          # timer service
├── packages/logger-console/ # console logger
├── package.json             # Yarn 4.14.1 workspace；无 committed lockfile
├── vitest.config.ts / yakumo.yml
└── README.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `packages/core/src/context.ts` | Context 派生/isolate | prototype-based extend；isolate 只覆盖 service→symbol map |
| `packages/core/src/fiber.ts` | 生命周期核心 | effect/disposer、epoch、state、reload/unload、config update |
| `packages/core/src/registry.ts` | plugin 入口 | resolve callback、runtime 去重、Fiber 实例化、thenable wrapper |
| `packages/core/src/service.ts` | service scope | service filter 比较当前 context 与 provider 的 isolate symbol |
| `packages/core/src/events.ts` | event/effect 集成 | listener 注册到 `this.ctx.fiber.effect()`，因此 cleanup owner 取决于 fiber |
| `packages/loader/src/config/isolate.ts` | 配置化 realm | local/global realm、service diff、fiber reload、realm GC |
| `packages/core/tests/fiber.spec.ts` | 时序回归 | inertia lock、FAILED、dispose error、update/restart |
| `packages/core/tests/isolate.spec.ts` | identity 隔离 | independent/shared label 与 event visibility；未覆盖 isolate-owned cleanup |

#### 源码精读

**代码块 1：`Context.isolate()` 只派生 symbol map，没有创建 Fiber**  
来源：[`packages/core/src/context.ts#L55-L69`](https://github.com/cordiverse/cordis/blob/8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4/packages/core/src/context.ts#L55-L69)

```typescript
extend(meta = {}): this {
  const shadow = Reflect.getOwnPropertyDescriptor(this, symbols.shadow)?.value
  const self = Object.create(getTraceable(this, this))
  for (const prop of Reflect.ownKeys(meta)) {
    Object.defineProperty(self, prop, Reflect.getOwnPropertyDescriptor(meta, prop)!)
  }
  if (!shadow) return self
  return Object.assign(Object.create(self), { [symbols.shadow]: shadow })
}

isolate(name: string, label?: symbol) {
  const shadow = Object.create(this[symbols.isolate])
  shadow[name] = label ?? Symbol(name)
  return this.extend({ [symbols.isolate]: shadow })
}
```

逻辑摘要：新 context 继承父 context，只有 isolate map 被替换；没有新 fiber/disposable list。它能分开同名 service 的 identity，却不能保证该 context 注册的 effects 归独立 owner。

**代码块 2：service 可见性由两侧 isolate symbol 相等决定**  
来源：[`packages/core/src/service.ts#L37-L39`](https://github.com/cordiverse/cordis/blob/8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4/packages/core/src/service.ts#L37-L39)

```typescript
protected [symbols.filter](ctx: Context) {
  return ctx[symbols.isolate][this.name] === this.ctx[symbols.isolate][this.name]
}
```

逻辑摘要：这是 service routing predicate，不是 ACL、sandbox 或 resource ownership check。相同 label 的 context 可共享 service；不同 label 隔离可见性。若 service 本身有文件/网络权限，这个比较不会限制其 effect。

**代码块 3：`Fiber.effect()` 收集 disposer 并逆序执行**  
来源：[`packages/core/src/fiber.ts#L275-L339`](https://github.com/cordiverse/cordis/blob/8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4/packages/core/src/fiber.ts#L275-L339)

```typescript
effect(execute: () => Effect, label = 'anonymous'): any {
  this.assertActive()
  const disposables: Disposable[] = []
  const dispose = () => {
    let task!: void | Promise<void>
    for (const dispose of disposables.splice(0).reverse()) {
      if (task) task = task.then(dispose)
      else task = dispose() as any
    }
    return task
  }
  const runner = {
    execute,
    epoch: true,
    collect: (dispose) => {
      disposables.push(dispose)
      this._disposables.delete(dispose)
    },
    getOuterStack: buildOuterStack(),
  }
  const task = this._execute(runner)
  // ... wrapper makes disposal idempotent and awaitable
}
```

逻辑摘要：真实源码还记录 effect metadata 并捕获 rejection。LIFO 适合“先 acquire A，再 acquire B，先 release B”；但所有权绑定调用时的 `this.fiber`。isolate 共享 fiber 时，LIFO 正确也无法避免跨 scope over-clean。

**代码块 4：依赖 UID 组成 epoch，变化触发串行 unload/reload**  
来源：[`packages/core/src/fiber.ts#L385-L413`](https://github.com/cordiverse/cordis/blob/8cc9e33fab69e2d0476d126baaf2acb24e6a6ab4/packages/core/src/fiber.ts#L385-L413)

```typescript
_refresh() {
  let epoch: string | boolean = ''
  for (const name of Object.keys(this.inject)) {
    const impl = this._store[name]
    if (!impl) {
      epoch = INACTIVE
      break
    }
    epoch += ':' + impl.fiber.uid
  }
  this._setEpoch(epoch)
}

private _setEpoch(epoch: string) {
  const oldEpoch = this._runner.epoch
  if (epoch === oldEpoch) return
  this._runner.epoch = epoch
  if (this.inertia) return
  this._updateState(() => {
    if (epoch !== INACTIVE && oldEpoch === INACTIVE) {
      this.inertia = this._reload()
      return FiberState.LOADING
    }
    this.inertia = this._unload()
    return FiberState.UNLOADING
  })
}
```

逻辑摘要：UID 避免只凭 service name 判断同一实现；`inertia` 防止 reload/unload 重叠。边界是 epoch 是进程内 transient identity，不是 durable run revision；process crash 后不能据此 resume。

#### 本机 issue #72 复现

在固定 commit、Yarn 安装环境执行真实 `Context`：

```text
baseline {"internal/listener":1,"internal/update":1,"test-ev":1}
mounted {"internal/listener":1,"internal/update":1,"test-ev":1,"cand-ev":1}
symbol_dispose undefined
disposed {"internal/listener":1,"internal/update":1}
```

这证明 parent `test-ev` 与 isolate `cand-ev` 都由共享 fiber 持有。该结果只证明当前 API 的 cleanup 缺口，不证明其他 Cordis-based 产品一定同样调用错误 API。

#### 依赖分析与供应链风险

- core runtime 直接依赖：`@standard-schema/spec^1.1.0`、`cosmokit^1.8.1`；optional peers 为 loader/include。
- loader 直接依赖 `cosmokit^1.8.1`，peer `cordis^4.0.0-rc.8`，optional peer `node-addon-require-builtin^0.1.0`。
- dev toolchain：forked `tsx`、TypeScript、Vite/Vitest、esbuild、Yakumo、ESLint；版本多为 caret ranges，且仓库 **没有 lockfile**。
- npm 严格解析真实拒绝 forked `tsx` 的 peer range；Yarn 4.14.1 安装成功但报告 peer warning，且 build scripts 被禁用。不同 package manager 产生不同可安装结论。
- production audit 没有建议；全量 dev audit 报 `minimatch@9.0.3` 的 3 个 high ReDoS advisories，以及 ESLint 8、glob 7、inflight、rimraf 3、tsconfck 等 deprecated/unmaintained 提示。production clean 不能覆盖测试/build 输入风险。
- Dependabot API 返回 403（仓库未启用/当前 token无权），public repository advisories 为 0；两者都不能证明无漏洞。

#### README / docs / issues / source 交叉核验

- README 只有 10 行，明确 API 未稳定，并链接 paper 与 Cordis primer；primer 的 lifecycle/effect说明与 `Fiber.effect()` 大体一致。
- `Context.isolate()`、`Service.filter` 与 isolate tests 一致地证明 identity isolation；源码没有独立 cleanup owner。
- issue #72 的输出在本机同 commit 精确复现；评论还有第二个上游用户确认。
- PR #73 的 prose 声称已修复，但真实 files diff 没有实现代码，反而删除 198 行 association tests；因此禁止仅凭 PR 标题/正文标记已解决。
- issue #76 明确将根因定位在 DSH packages：child 继承工具、denial 被映射为普通 retryable error、无 terminal/retry cap。Cordis 只能提供更好的 parent/child lifecycle primitive，不能替 DSH 修复 tool policy。

#### 可复用经验

- 当框架提供 `isolate/scope/context` 时，应优先分别验证 identity visibility、effect ownership、cleanup ownership 与 authority enforcement，因为名称上的隔离不等于资源或权限隔离；边界是进程内 context 仍共享 OS 权限。
- 当 dependency availability 驱动 plugin reload 时，应优先使用 immutable implementation generation + serialized unload/reload + explicit state，因为同名 service 可能已换代；边界是进程内 generation 不能作为 durable resume token。
- 当 child Agent 调用不可用的人机交互工具时，应优先在 tool discovery 排除它，或把 denial 映射为 non-retryable `blocked/needs_parent` terminal，因为 prompt 中“不要重试”不能阻止 token spin；边界是 parent relay 仍需用户可达性。
- 当 PR 声称修复安全/生命周期 bug 时，应优先核对 files diff、tests 和 merge state，因为标题与正文可以和实现完全不一致；边界是 diff 静态一致仍需运行验证。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/scoped-effect-owner/` 做纯 Python/TypeScript fixture，不加载 Cordis product：

1. 定义 `Scope{id,parent,generation,state}` 与 `EffectReceipt{scope_id,effect_id,dispose_state}`。
2. parent 注册 A，child 注册 B；child dispose 后必须只剩 A。
3. child 缺 capability 时返回 `blocked/needs_parent`，同 operation 重试计数必须保持 0。
4. parent generation 更换时，旧 child effect 无权 commit；返回 `stale_generation`。
5. 用 property tests 验证 LIFO、idempotent dispose、parent survival、exactly-one terminal。

#### 风险边界

- **License**：Repository/License API 与根 LICENSE 为 MIT；npm transitive dependencies、Cordis-based forks/products分别审查。
- **维护活跃度**：pushed 2026-08-13；无 tags/releases；core 为 `4.0.0-rc.8`，README明示API随时变化。42 open issues/PR aggregate表明活跃，但不是稳定性证明。
- **正确性风险**：本机复现 isolate over-clean；修复 PR #73 无有效实现；全仓曾出现一次 HMR fixture flaky，虽随后定向和全仓通过。
- **安全风险**：plugin callback 是同进程代码；isolate不是sandbox；HMR/include/loader可加载/重载代码与配置；service visibility不是effect authorization。
- **供应链风险**：无 lockfile、caret ranges、forked tsx、npm/Yarn解析差异、dev audit high advisories。
- **不适用场景**：把不可信 plugin 放在同进程并期待强隔离；跨进程 durable workflow；需要稳定 API 的生产核心；仅凭 scope label授权文件/网络/secret。
- **不能自动执行**：不安装为 Hermes runtime，不加载未知 plugin，不把 child tool registry交给第三方框架，不自动应用 open PR。

#### Skill 升格判断

**需二次验证**；effect owner/terminal contract 值得抽象，Cordis runtime 暂不沉淀。

- **可迁移候选**：generation-bound dependency、serialized lifecycle、LIFO disposer、scope-owned cleanup、non-retryable child terminal。
- **需二次验证**：先完成 `scoped-effect-owner` adversarial fixture，并与现有 verification-first、subagent 四状态、effect-scope candidates 去重。
- **暂不沉淀**：不复制 Cordis源码、loader/HMR、paper术语或 PR #73 到 shared skill。
- **升格结论**：优先更新已有 `research/github-hot-project-learning` 的验证契约，不新建 Cordis-specific skill；今日仅 Hermes raw candidate。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/scoped-effect-owner/{schema.json,model.py,fixtures/,test_contract.py,README.md}`。
2. **Hermes orchestrator**：未来在 `scripts/github_learning_orchestrator.py` 的 task receipt 中加入 `scope_id/owner_generation/effects/terminal/retryability`，但先 sidecar，不直接改生产流程。
3. **shared skill**：fixture通过后更新 `capabilities/skills/research/github-hot-project-learning/` 的 source/PR verification 条款，并在 manifest bump version；禁止新建项目专属 skill。
4. **分层**：API JSON、clone、test stdout留 runtime；完整日报留 inbox；稳定 invariant 经评分、去重、脱敏与治理审查后才进入 curated。
5. **OpenClaw边界**：当前不存在且未调用；未来只复用 agent-neutral schema，必须在其真实 runtime 单独验证 tool denial/terminal mapping。

### 项目 2：basecamp/omarchy

- **URL**：https://github.com/basecamp/omarchy
- **Stars / Forks / Language / License（GitHub API）**：**25,355 / 2,588 / Shell / MIT**。
- **查询时 updated / pushed**：2026-08-16T23:34:36Z / 2026-08-16T18:29:44Z。
- **固定源码版本**：`30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec`；commit `Update tokyo-night winding-road background (#7057)`，GitHub verification 为 verified。
- **release / issues / PR 证据**：latest release `v4.0.0` 发布于 2026-08-14T16:35:40Z，tag commit `f0020448...`；固定 HEAD ahead 21 commits。Open issue #6995 报告 lock transition 期间新 idle cycle 启动第二个 screensaver；open PR #7131 给出 in-process `lockInFlight` fix，但未 merge。Issue #6976 报告旧 MacBook v4 性能回退，未给可量化 profile，故性能原因待核验。

#### 一句话判断：为什么值得学

Omarchy 值得学习的不是“用 Shell 做发行版”，而是它把高风险系统更新拆成**并发锁、前置预算、可辨识 snapshot、package transaction、成功后 marker、post-update、restart**；同时它也暴露两个边界：snapshot 失败会告警但更新继续，异步 lock command 与 lock service 状态之间仍可能有 transition gap。

#### 解决的问题：替代了什么旧做法

1. 替代用户直接 `pacman -Syu` 绕过 migration/snapshot：ALPM PreTransaction guard 引导进入 blessed update path，并保留显式 bypass。
2. 替代两个更新重叠：per-user flock fd 从 wrapper 继承到整条 pipeline。
3. 替代“脚本存在就算 migration 完成”：migration 只有 `bash -euo pipefail` 成功后才 touch per-user marker。
4. 替代“snapshot 命令 exit 0 但没配置”：Snapper installed/unconfigured 明确 exit 1；Snapper absent 用 127 表示 deliberate skip。
5. 替代 package failure 后仍继续 migration：`set -e` + 固定顺序保证 package transaction失败时后续不运行。
6. 替代 unattended 流程盲等 prompt：`-y` 导出 `OMARCHY_UPDATE_UNATTENDED=1`，冲突需要人回答时显式失败。
7. 但它不是事务：snapshot 失败时仍可继续；`/home` 不一定被 root snapshot覆盖；AUR/mise/orphans位于主 package/migration之后，整个流程没有跨系统 rollback。

#### 架构 / 实现与数据流

```text
omarchy update
  ├─ script(1) transcript → /tmp/omarchy-update.log
  ├─ per-user flock (update lock)
  ├─ free-space preflight (10 GiB, explicit force bypass)
  ├─ confirm / unattended policy
  ├─ prune package cache
  ├─ snapshot attempt
  │    ├─ snapper absent → 127 deliberate skip
  │    └─ configured/error → success or loud degraded continuation
  ├─ stay-awake owner
  ├─ dev checkout → keyring → pacman transaction
  ├─ pending migrations
  │    └─ run success → per-user marker commit
  ├─ post-update hook → AUR → mise → orphan handling
  ├─ log analysis / update status
  └─ release inhibitor → restart/reboot checks

bypass lane
  direct pacman → ALPM guard abort or explicit bypass
                → next login checks per-user pending markers
                → notify only; never silently migrate
```

这是一条可恢复但非原子 workflow。每个 stage 的 terminal/owner不同，不能由最后一个 exit 0 概括全部 coverage。

#### Repo tree 摘要

固定 commit 共 **1,622 tracked files**：

```text
omarchy/
├── bin/                  # 425 CLI scripts；update/migrate/snapshot/lock helpers
├── shell/                # 175 Quickshell files；长驻 desktop shell/plugins/services
├── test/                 # 201 tracked files；181 shell *-test.sh + fixtures/runners
├── themes/               # 249 theme assets/configs
├── default/              # packaged defaults、systemd、ALPM hooks、Hyprland等
├── install/              # ISO/user/hardware provisioning；147 core + 59 other packages
├── migrations/           # 79 one-time per-user repair scripts
├── manual/               # end-user docs
├── docs/                 # architecture/update/testing references
├── agents/skills/        # repo-local contributor procedures
├── config/ / etc/ / applications/
├── version               # checkout显示 4.0.0.alpha；runtime版本实际由pacman/dev hash派生
└── README.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `bin/omarchy-update` | blessed orchestrator | transcript、lock、budget、snapshot、packages、migrations、hooks、restart |
| `bin/omarchy-update-lock` | concurrency owner | fd path/ancestry验证、nonblocking flock、fd继承 |
| `bin/omarchy-migrate` | durable step runner | pending枚举、pacman wait、成功后marker、per-user state |
| `bin/omarchy-snapshot` | recovery evidence | absent/unconfigured/configured三态，逐config create+cleanup |
| `bin/omarchy-update-system-pkgs` | package transaction | parseable stderr、single retry handoff、owned update env |
| `bin/omarchy-update-system-pkgs-when-conflicted` | conflict recovery | quarantine unowned files、restore-on-failure、interactive package conflict |
| `default/libalpm/hooks/00-omarchy-update-guard.hook` | entrypoint enforcement | Upgrade PreTransaction + AbortOnFail |
| `shell/plugins/services/idle/Service.qml` | idle/lock timing | 当前 HEAD仍有 shell-out fail-open window；PR #7131待合并 |
| `docs/update-process.md` | intended contract | state files、stage order、bypass lane、remaining pacnew concern |

#### 源码精读

**代码块 1：`omarchy-update` 把 package success 放在 migration 之前**  
来源：[`bin/omarchy-update#L28-L55`](https://github.com/basecamp/omarchy/blob/30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec/bin/omarchy-update#L28-L55)

```bash
if [[ ${1:-} == "-y" ]] || omarchy-update-confirm; then
  omarchy-update-pkg-prune
  omarchy-snapshot create || (($? == 127)) ||
    echo -e "\e[33mContinuing the update without a snapshot.\e[0m" >&2
  omarchy-update-stay-awake start
  omarchy-update-dev
  omarchy-update-keyring
  omarchy-update-system-pkgs
  omarchy-migrate
  omarchy-hook post-update
  omarchy-update-aur-pkgs
  omarchy-update-mise
  omarchy-update-orphan-pkgs
  omarchy-update-analyze-logs
  omarchy-update-status
fi
```

逻辑摘要：顶层 `set -e` 使 package失败阻断migration；本机 sequence test验证这条 invariant。关键边界是 snapshot 被定义为 degraded-but-continue，不能把更新完成写成“可回滚已保证”。

**代码块 2：migration marker 是成功后的 commit point**  
来源：[`bin/omarchy-migrate#L88-L97`](https://github.com/basecamp/omarchy/blob/30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec/bin/omarchy-migrate#L88-L97)

```bash
while IFS=$'\t' read -r name file marker; do
  [[ -n $name ]] || continue
  if [[ ! -f $marker ]]; then
    echo -e "\e[32m\nRunning migration (${name%.sh})\e[0m"
    OMARCHY_PATH="$OMARCHY_PATH" bash -euo pipefail "$file"
    mkdir -p "$(dirname "$marker")"
    touch "$marker"
  fi
done < <(migration_entries)
```

逻辑摘要：失败脚本不会获得 marker，下次可重试。边界是 marker只证明脚本exit 0，不证明外部effect readback；migration规范要求idempotent，但没有通用事务、hash或版本绑定。

**代码块 3：update lock 验证 inherited fd 确实指向 canonical lock path**  
来源：[`bin/omarchy-update-lock#L12-L41`](https://github.com/basecamp/omarchy/blob/30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec/bin/omarchy-update-lock#L12-L41)

```bash
lock_is_held() {
  local lock_fd_path=""
  [[ -n ${OMARCHY_UPDATE_LOCK_FD:-} &&
     -e /proc/$$/fd/$OMARCHY_UPDATE_LOCK_FD ]] || return 1
  lock_fd_path=$(readlink -f "/proc/$$/fd/$OMARCHY_UPDATE_LOCK_FD" 2>/dev/null || true)
  [[ $lock_fd_path == "$(readlink -m "$lock_path")" ]] &&
    flock -n "$OMARCHY_UPDATE_LOCK_FD"
}

exec {OMARCHY_UPDATE_LOCK_FD}>"$lock_path"
if ! flock -n "$OMARCHY_UPDATE_LOCK_FD"; then
  echo "An Omarchy update is already running."
  exit 1
fi
export OMARCHY_UPDATE_LOCK_FD
exec "$@"
```

逻辑摘要：不仅信环境变量中的 fd number，还检查 `/proc/$$/fd` resolved path；test覆盖第二个更新进不了snapshot。边界是它是per-user/process lock，不是跨机器 lease；`/tmp` fallback与多用户 ownership另有文档限制。

**代码块 4：snapshot 的 absent/unconfigured/configured 终态明确分开**  
来源：[`bin/omarchy-snapshot#L16-L42`](https://github.com/basecamp/omarchy/blob/30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec/bin/omarchy-snapshot#L16-L42)

```bash
if omarchy-cmd-missing snapper; then
  exit 127
fi
mapfile -t CONFIGS < <(sudo snapper --csvout list-configs |
  awk -F, 'NR>1 {print $1}')
if (( ${#CONFIGS[@]} == 0 )); then
  echo "No Snapper configs found, so no snapshot was created." >&2
  exit 1
fi
for config in "${CONFIGS[@]}"; do
  sudo snapper -c "$config" create -c number -d "$DESC"
  sudo snapper -c "$config" cleanup number
done
```

逻辑摘要：127是明确 capability absent，1是“工具存在但没有产物”，0才是逐config命令成功。边界是没有读取新snapshot ID并验证subvolume coverage，且manual明确root snapshot不恢复`/home`。

**代码块 5：当前 idle path 的 shell-out guard可能在 transition/IPC failure时 fail open**  
来源：[`shell/plugins/services/idle/Service.qml#L65-L98`](https://github.com/basecamp/omarchy/blob/30f7a06090dc20dd1a4a8d0c99bfb8e2370df2ec/shell/plugins/services/idle/Service.qml#L65-L98)

```qml
function launchScreensaver() {
  root.screensaverStartedThisCycle = true
  screensaverLaunchGraceTimer.restart()
  runProcess(screensaverProcess, "screensaver",
    "[[ $(omarchy-shell lock isLocked 2>/dev/null) == \"true\" ]] || omarchy-launch-screensaver")
}

function lockSystem(reason) {
  // timers/reset omitted
  root.idledThisCycle = false
  runProcess(lockProcess, "lock", "omarchy-system-lock")
}

function startIdleCycle() {
  if (root.idledThisCycle) return
  root.idledThisCycle = true
  if (root.screensaverDelaySeconds === 0) launchScreensaver()
}
```

逻辑摘要：`lockSystem()`在异步command真正抵达lock service前清空cycle；IPC空输出不是`true`，`||`于是执行screensaver。PR #7131拟在同进程读lock service，并从command spawn开始维护bounded `lockInFlight`，但截至查询时仍open。

#### 依赖分析与供应链风险

- 不是 npm/pip 项目；没有单一 package lock。`install/omarchy-base.packages` 有 **147** 个非注释唯一package，`omarchy-other.packages` 有 **59** 个；实际版本由当前Arch/Omarchy channel仓库决定。
- 核心面含 kernel、firmware、Hyprland、Quickshell git package、Docker、Chromium、ffmpeg、PAM/systemd/NetworkManager、AUR/yay、mise工具，供应链与native/system authority面远大于脚本本身。
- package transaction允许 `--overwrite '/usr/share/omarchy/*'`；unowned conflict会移到 `/var/lib/omarchy/replaced`，失败时restore。该逻辑需要root并操作live system，今日未执行。
- theme/plugin支持git来源；v4 release notes还说明多个过去的theme code-execution path被修复。MIT仓库license不覆盖所有packages/plugins/themes的许可。
- Dependabot API 403；public repository advisories为0。没有在Arch环境运行 `pacman -Q`、`arch-audit` 或ISO SBOM，漏洞状态**待核验**。

#### README / docs / release / issues / source 交叉核验

- `manual/30-updates.md`称正常更新包含snapshot、migration与config；`docs/update-process.md`与源码给出更精确顺序和degraded路径。
- v4.0.0 release称“snapshot预期缺失时不再假称成功”，与 `omarchy-snapshot` 三态及本机4个snapshot断言一致。
- release称新shell整合为长驻Quickshell plugin process；issue #6995与源码说明这种整合带来in-process state可读，但当前idle仍通过shell-out查询lock。
- issue #6995的原始timeline与源码transition gap一致；维护者在评论中纠正部分后续报告的推断，并给PR #7131。PR仍open，不能标记stable已修复。
- `version` 文件显示 `4.0.0.alpha`，而docs说明package-backed runtime没有version file，真实版本由pacman或dev hash派生；因此不能用checkout该文件声称安装版本。
- docs列出的remaining concern包括`.pacnew/.pacsave`处理缺失，说明package-backed迁移仍有未闭环配置面。

#### 可复用经验

- 当升级包含多个高权阶段时，应优先把 `preflight → backup attempt → apply → migrate → verify → commit marker → restart` 分开并记录每阶段terminal，因为最终exit 0不能证明snapshot或所有post-step完成；边界是分阶段仍不是跨系统事务。
- 当一个恢复点是可选能力时，应优先区分 `unsupported`、`configured-but-no-artifact`、`created+verified`，因为静默no-op会制造虚假可恢复性；边界是created还需coverage/readback。
- 当异步command触发另一个service的状态变化时，应优先在command spawn时建立pending state，并在同一authority plane读取状态，因为等待下游“最终locked”会留下transition window；边界是pending需要timeout、generation和late completion处理。
- 当无人值守模式遇到package conflict或用户决策时，应优先返回non-retryable `blocked/needs_user`，因为默认回答或隐藏prompt可能破坏用户选择；边界是必须保存resume point与原始冲突证据。
- 当migration用marker实现at-most-once表象时，应优先在成功后写marker，并使effect idempotent/readbackable，因为crash可能发生在effect成功与marker写入之间；边界是marker文件不提供exactly-once effect。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/staged-upgrade-receipt/` 做离线fixture，不调用系统工具：

1. 定义 stages：`preflight, backup, apply, migrate, verify, commit`。
2. 每阶段输出 `attempted/status/artifact_id/coverage/retryable/detail`。
3. 构造 backup unsupported、backup failed-but-policy-allows、apply failed、effect succeeded-marker missing、pending timeout/late ACK 五类fixture。
4. `completed` 必须要求policy允许的coverage；backup degraded必须保留在overall receipt，不能被后续成功覆盖。
5. crash/replay时按operation ID去重；marker missing必须先readback effect再决定重跑。

#### 风险边界

- **License**：Repository/License API与根LICENSE为MIT；206个package entries、AUR、plugins、themes、ISO assets分别审查。
- **维护活跃度**：pushed 2026-08-16；v4.0.0发布两天；HEAD比tag ahead 21 commits。高活跃也意味着migration、shell与依赖快速漂移。
- **安全风险**：pacman/AUR、sudo/pkexec、PAM、systemd、boot/kernel、theme/plugin git、browser prefs、hooks和migration均是高权effect面；不适合在非Omarchy WSL cron尝试。
- **正确性风险**：snapshot失败仍继续；root snapshot不保证`/home`；marker不含hash/readback；pacnew/pacsave未处理；issue #6995修复未合并。
- **性能风险**：v4把大量组件合并到单长驻shell；issue #6976报告旧硬件变慢，但无本机profile，原因与普遍性待核验。
- **测试边界**：20个stubbed断言只证明shell控制流；没有Arch VM、真实package transaction、reboot、snapshot restore、PAM/lock视觉E2E。
- **不适用场景**：需要跨机器协调的升级、必须原子回滚`/home+root+external services`、无人值守中自动解决语义冲突。
- **不能自动执行**：不运行Omarchy installer/update/migration，不修改当前WSL systemd/pacman/boot，不clone plugin到用户环境，不自动应用PR。

#### Skill 升格判断

**需二次验证**；staged receipt与pending transition模式可抽象，Omarchy脚本/skill暂不沉淀。

- **可迁移候选**：lock-before-backup、stage ordering、success-after-marker、capability三态、unattended blocked、spawn-time pending。
- **需二次验证**：先完成 `staged-upgrade-receipt` fixture，并用最近GitHub-learning历史audit模拟 crash/replay。
- **暂不沉淀**：不复制Omarchy shell scripts、repo-local agent skills、migration、package lists或阈值进shared skill。
- **升格结论**：与现有 orchestrator/verification/reflection/path-portability 去重后，优先更新现有 skill；今日仅Hermes raw candidate。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/staged-upgrade-receipt/{schema.json,policy.yaml,fixtures/,runner.py,replay.py,test_contract.py}`。
2. **Hermes learning pipeline**：未来让 `scripts/github_learning_orchestrator.py` 写 `prepare/research/audit/knowledge-copy` 各阶段 receipt；`overall_status=completed` 需验证expected artifact和audit score，而不只命令exit。
3. **shared workflow**：POC通过后更新 `capabilities/skills/research/github-hot-project-learning/`，加入 `unsupported/degraded/blocked/failed/completed`投影规则；manifest版本随契约升级。
4. **迁移类复用**：任何shared hub迁移必须先通过 `scripts/resolve_shared_root.py`，再做dry-run inventory、backup/readback、apply、verify；不复用Omarchy宿主路径或pacman假设。
5. **OpenClaw边界**：当前不存在且禁止调用；未来若接入，只消费portable receipt schema，不假设其lock/marker/runtime语义等同Hermes。

## 经验沉淀

1. 当系统声称提供scope/isolation时，应优先把identity、effect owner、cleanup owner、authority四层分别测试，因为共享fiber或同进程权限会让“隔离”只剩routing语义；边界是测试通过也不等于OS sandbox。
2. 当异步操作在命令发出到权威状态可见之间有窗口时，应优先从spawn时记录bounded pending generation，并在最终effect前重验，因为只看最终state会在transition gap中fail open；边界是late completion必须按generation丢弃或reconcile。
3. 当长流程依赖backup/snapshot时，应优先输出unsupported、failed、created、verified及coverage，而不是一个snapshot exit；边界是artifact存在不代表可恢复全部数据。
4. 当migration或Agent step用marker表示完成时，应优先采用`effect → readback → marker/receipt`，并为effect成功但marker缺失设计replay，因为marker-after-success仍有crash window；边界是外部非幂等effect可能需要人工reconcile。
5. 当child Agent没有权限完成人机交互或高权effect时，应优先从capability discovery排除工具，或返回non-retryable blocked并向parent转交结构化问题，因为普通tool error会诱发模型重试；边界是parent也可能无人可问。
6. 当PR/issue/release声称修复时，应优先核对merge state、真实files diff、测试与固定commit，因为prose可能与实现相反；边界是merged也不代表用户已安装对应artifact。
7. 当仓库没有lockfile且依赖使用范围版本时，应优先记录resolver、解析时间、resolved graph与audit环境，因为同一commit可以得到不同依赖与测试结果；边界是临时生成lock不能冒充上游release lock。

## 明日继续

1. 检查 Cordis #72 / PR #73 是否出现真正实现与回归测试；若仍只有prose或删测试，保持blocked，不追随PR标题。
2. 检查 Omarchy #6995 / PR #7131 是否merge，并核对是否增加真实state transition test，而不只正则扫描QML文本。
3. 建立 `runtime/hermes/github-learning-poc/scoped-lifecycle-upgrade-receipt/` 的合并fixture：parent/child disposer、spawn pending、backup degraded、effect-success-marker-missing、late ACK 五类状态。
4. 用两天历史learning报告做offline replay，比较当前单一audit score与stage/coverage receipt是否会产生不同overall terminal；不改生产orchestrator。

## 候选反哺

### Candidate Facts

- [ ] topic: scope identity 不等于 cleanup/authority isolation | evidence: Cordis `context.ts`、`events.ts`、本机 #72 复现、PR #73真实diff | 建议: create | 安全级别: medium
- [ ] topic: staged workflow completed 必须保留 degraded backup/coverage | evidence: Omarchy update/snapshot/migrate源码与20个本机断言 | 建议: create | 安全级别: low
- [ ] topic: async command必须从spawn建立bounded pending generation | evidence: Omarchy #6995、当前idle源码、open PR #7131 | 建议: create（待merge/fixture） | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: scoped lifecycle receipt | 可复用场景: subagent/plugin/tool effect所有权与回收 | 是否建议 shared: yes（验证后） | 原因: Hermes/future agent均需，先与effect-scope/subagent四状态去重
- [ ] 名称: staged upgrade/audit receipt | 可复用场景: research、migration、cron、知识库复制的阶段终态 | 是否建议 shared: yes（验证后） | 原因: 能避免exit 0或最终分数覆盖degraded/blocked stage
- [ ] 名称: Cordis integration | 可复用场景: 第三方plugin runtime | 是否建议 shared: no | 原因: RC API、cleanup bug、无lockfile、当前无产品接入需求
- [ ] 名称: Omarchy update integration | 可复用场景: Arch桌面更新 | 是否建议 shared: no | 原因: 宿主特定且高权，不适合shared hub通用能力

### Candidate Open Questions

- [ ] 问题: Cordis应让derived context拥有独立fiber，还是新增显式scope/disposable owner？ | reason: gap | priority: high
- [ ] 问题: GitHub-learning `overall_status=completed` 是否应要求stage coverage receipt，而非只要求audit score？ | reason: adaptation | priority: high
- [ ] 问题: snapshot/backup degraded时哪些cron允许继续，哪些必须blocked？ | reason: adaptation | priority: high
- [ ] 问题: Omarchy PR #7131的15秒pending timeout遇到late lock completion如何按generation reconcile？ | reason: gap | priority: medium
- [ ] 问题: Cordis HMR config fixture为何一次残留`v3`，是watcher teardown还是test isolation问题？ | reason: conflict | priority: medium

### 不应自动落地

- 不自动修改Hermes/OpenClaw配置、model、provider、auth、env、cron或本地skills。
- 不自动写curated active fact；以上只进入Hermes inbox/runtime候选，等待评分、去重、脱敏和治理审查。
- 不安装Cordis runtime/plugin，不执行Omarchy installer/update/migration，不应用未合并PR。
- 不把MIT仓库许可外推到npm依赖、Arch/AUR packages、ISO、plugins、themes或第三方发布物。
- 不把全仓测试通过外推为cleanup bug已修复，也不把stubbed shell tests外推为系统升级/恢复E2E通过。
