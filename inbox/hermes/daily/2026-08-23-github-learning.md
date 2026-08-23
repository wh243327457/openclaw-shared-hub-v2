# 2026-08-23 GitHub 热门项目每日学习报告

- 执行器：Hermes
- 研究日期：2026-08-23
- 发现/核验时间：2026-08-23（WSL；GitHub API 查询与本地浅克隆均为本次真实执行）
- 共享根解析：先运行 `python3 scripts/resolve_shared_root.py`，返回 `/home/vany/agent/shared`
- 研究边界：OpenClaw 运行时不存在；本次没有调用、启动、模拟或写入 OpenClaw，也没有修改 Hermes 配置、模型、provider、auth、env、cron 或现有 skills。
- 证据方式：热门候选由 `gh api search/repositories` 发现；Stars、Forks、Language、License、更新时间由 `gh api repos/{owner}/{repo}` 核验；README 由 GitHub API 内容接口读取；源码由 `git clone --depth=1` 后读取；release/issues 由 GitHub API 读取。
- 深读固定版本：`CopilotKit/OpenBot@6826e11afd52f03c30af2d873203792acad95f63`；`wang2122/sprix-sage-router@aed97852abc0bbd1dfccd8851b31290bc1b3f507`。

## 今日结论

**今日主线是“先把权限与约束放在执行边界，再让路由根据进度和证据调整”：OpenBot 将浏览器、文件、MCP、shell 等动作统一经过 server gateway 的 resolve → policy → audit → act 链路；Sprix SAGE 则把 SELF/COLLABORATE/HANDOFF 的选择约束在权限、预算、时限和任务 DAG 之内，并用执行结果更新局部可靠性。对 Hermes/shared hub 最值得迁移的是窄契约——结构化决策、硬约束优先、可审计 receipt、失败后的重新规划——而不是直接复制两个项目的产品或源码。**

## 研究范围与证据摘要

1. `gh api -X GET search/repositories -f q='created:>2026-08-15 stars:>1000' -f sort=stars -f order=desc -f per_page=10` 返回了本日新项目候选；下方速览只写入该命令真实返回的字段。
2. OpenBot 的 GitHub API 元数据显示 2,315 Stars、MIT、TypeScript、`pushed_at=2026-08-22T21:48:01Z`；API 的 releases 返回最新 `v0.0.4`，issues 返回 #193/#192/#190。README 明确标注 Alpha/active development，并描述 gateway、CEL policy、audit 与 per-Bot computer。
3. SAGE 的 GitHub API 元数据显示 1,243 Stars、MIT、Python、`pushed_at=2026-08-21T08:45:27Z`；API 的 releases 返回 `v0.1.0`。README、`ALGORITHM.md`、`SECURITY.md` 与源码交叉核验；README 明确称其为 early-stage research preview，且当前 reference implementation 不认证 agent、不传输 A2A task、不隔离执行、不 enforce network policy。
4. SAGE 在本次真实执行中运行 `python -m unittest -v`：**12 tests / 12 passed / 0 failed**；`python demo.py` 返回 `COLLABORATE`，成功概率 `0.814`，成本 `0.176`，延迟 `1122 ms`。`python benchmark.py` 返回 2,500 tasks、5 seeds 的 synthetic benchmark；learned_sage 为 quality `0.634+/-0.006`、utility `0.487+/-0.006`、deadline miss `0.2%`。这些不是现实生产效果证据。
5. OpenBot 本地浅克隆成功，但环境中 `bun` 不存在（真实输出：`/usr/bin/bash: bun: command not found`），因此没有声称 OpenBot 的本地 Bun tests/typecheck 通过。其代码结论来自固定 commit 的源码与测试文件读取；运行验证状态为 **待在 Bun 1.3.14 环境复验**。

## 项目速览

> Stars / Language / License 均来自本次 GitHub API 输出；Stars 是查询时快照，不是永久值；`NOASSERTION` 或空值不等于许可证已确认。

| 项目 | Stars | Language | License | 本次判断 |
|---|---:|---|---|---|
| [s1dashu/ip-as-logo-skill](https://github.com/s1dashu/ip-as-logo-skill) | 3,773 | 待标注（API 空值） | MIT | 新近 Agent Skill，适合观察技能资产化，不作源码深读 |
| [yetone/cumora](https://github.com/yetone/cumora) | 2,900 | TypeScript | MIT | Agent-first team chat 候选，不作今日深读 |
| [CopilotKit/OpenBot](https://github.com/CopilotKit/OpenBot) | 2,315 | TypeScript | MIT | **深读：统一动作网关、策略、审计和 per-Bot computer** |
| [MengTo/threeui](https://github.com/MengTo/threeui) | 1,836 | HTML | MIT | UI 组件目录候选，不作今日机制深读 |
| [wang2122/sprix-sage-router](https://github.com/wang2122/sprix-sage-router) | 1,243 | Python | MIT | **深读：状态感知三模式 agent 路由与 DAG 调度** |
| [cinderline/northcinder](https://github.com/cinderline/northcinder) | 1,205 | JavaScript | MIT | MCP 产品比较服务候选，安全边界需另行研究 |
| [vvxw/deploy-vercel](https://github.com/vvxw/deploy-vercel) | 1,114 | JavaScript | API License 为空，待核验 | 仅 API 速览，不复制或迁移 |
| [Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report](https://github.com/Tiger3807861189/DeepSeek-V4-J-Space-Capability-Realization-Report) | 1,039 | 待标注（API 空值） | NOASSERTION | 研究报告型仓库，license 待核验，不作源码深读 |

## 深读项目

# 1. CopilotKit/OpenBot

### 基本信息与核验来源

- URL：https://github.com/CopilotKit/OpenBot
- GitHub API：**2,315 Stars / 266 Forks / TypeScript / MIT**。
- API 时间：`created_at=2026-08-17T00:44:59Z`，`updated_at=2026-08-22T23:09:07Z`，`pushed_at=2026-08-22T21:48:01Z`，open issues `29`，default branch `main`。
- 固定源码 commit：`6826e11afd52f03c30af2d873203792acad95f63`。
- Release API：最新 `v0.0.4`，`published_at=2026-08-22T21:48:02Z`。
- Issue API：#193 “Routines: let a Bot work on a schedule with nobody watching”；#192 “Bot-to-bot messaging”；#190 “live screen is tracked per Bot rather than per socket”。这些是开放 issue 的真实标题，不代表已修复或已实现。
- README 交叉核验：项目状态为 Alpha/active development；README 描述 Docker Compose、PostgreSQL、AG-UI、CEL policy、gateway、audit、per-Bot browser/files/workspace 与 human take-the-wheel。
- 运行状态：本次 WSL 无 `bun`，没有执行 OpenBot 的 Bun test/typecheck；该部分标为待复验，不能把源码测试文件当作已运行结果。

### 一句话判断：为什么值得学

**值得学的不是“给 agent 一台电脑”这个产品包装，而是把每个高影响动作收敛到一个可验证的 server-side gateway：解析服务端持有的 snapshot ref，策略先决策，审计先落行，最后才把动作发给 computer。**

### 解决的问题：替代了什么旧做法

1. 替代模型直接拥有浏览器/文件/shell 权限：所有 computer action 经 gateway；README 的架构说明和 `server/src/computer/gateway.ts` 的 `govern` 一致。
2. 替代按模型自报的元素名称做策略判断：gateway 以服务端 snapshot 中的 opaque `ref` 解析真实元素；测试明确加入伪造 `name: "Continue"` 仍应被 `Submit` deny 规则拒绝的 counterexample。
3. 替代只记录成功：gateway 先写 `computer.action_allowed`/`computer.action_refused`，动作失败后再写 `computer.action_failed`；测试检查允许但失败的动作产生两条记录。
4. 替代把 secrets、typed text、file contents 混进 transcript/audit：测试检查 typed text 与 file body 不在 audit payload；shell 返回 output 也不作为 audit row 的内容。
5. 替代“策略没配置就默认允许”：`evaluateActionPolicy` 的契约是 absent policy denies；deny 优先于 allow，broken policy fail closed。
6. 替代所有 Bot 共用隐式环境：README 与 `agent-computer/src/shell.ts` 说明每个 Bot 可有独立 computer/workspace；shell 使用环境变量 allow-list、workspace 作为 HOME、超时和输出上限。

### 架构 / 实现与数据流

```text
User / UI / AG-UI agent
          |
          v
      OpenBot server
          |
          +--> resolve bot -> computer address / session
          +--> load server-side snapshot(ref, generation)
          +--> build PolicyContext(element/page/file/command/intent)
          +--> evaluate CEL policy (deny > allow; absent/broken => deny)
          +--> write audit decision row
          |
          +--> if forward: computer gateway -> per-Bot browser/files/shell/MCP
          +--> if effect fails: write action_failed row
          |
          +--> transcript/admin audit projection
```

关键边界是“决策所依据的对象”与“执行所到达的对象”都要绑定 Bot、snapshot generation/session 和 target address；README 还说明 computer 直接端口应保持私有，不能绕过 gateway。

### Repo tree 摘要（固定 commit）

```text
OpenBot/
├── server/src/
│   ├── computer/gateway.ts       # resolve -> policy -> audit -> act
│   ├── computer/policy.ts        # CEL context、deny/allow、fail-closed
│   ├── computer/snapshot-store.ts# ref/generation 的跨 replica 存储抽象
│   ├── audit.ts                  # audit event types 与敏感字段处理
│   └── agents/ plugins/ channels/# agent、MCP、会话和路由
├── agent-computer/src/
│   ├── authorisation.ts          # computer token 与 health open path
│   ├── shell.ts                  # bounded shell、环境 allow-list、workspace
│   ├── egress.ts                 # per-Bot proxy/egress identity
│   └── workspace.ts/profiles.ts  # workspace/profile 边界
├── agent-bot/ / agent-langgraph/ # AG-UI agent examples
├── app/src/                     # UI、admin boundaries、audit、channels
├── supervisor/                   # 创建/管理 per-Bot computer
├── docs/                        # architecture/configuration/deployment 等文档
├── .github/workflows/            # CI、release、zizmor security workflow
├── package.json                 # Bun 1.3.14、workspace scripts
├── server/package.json           # Hono/CEL/Drizzle/Postgres 等
├── agent-computer/package.json  # Playwright、SPIFFE、YAML
└── LICENSE / README.md          # MIT 与 Alpha 产品边界
```

### 关键源码文件

| 文件 | 用途 | 本次核验摘要 |
|---|---|---|
| `server/src/computer/gateway.ts` | computer action 的唯一治理面 | `govern` 从 snapshot store 解析 ref，构造 context，写 decision audit，拒绝则不 forward，执行失败再写 failure |
| `server/src/computer/policy.ts` | 规则求值 | CEL `contains`/`matches` helper；deny 优先；缺少 policy、表达式抛错或非 boolean 结果走 fail-closed |
| `server/src/computer/snapshot-store.ts` | 跨 replica 的 ref 映射 | snapshot ID、elements、URL、session/generation 由 server 保存；旧 generation 不解析为当前元素 |
| `agent-computer/src/authorisation.ts` | computer 端 token | `matchesToken` 做等长字符比较；health 是唯一 unauthenticated open path；stream token 走 query 参数 |
| `agent-computer/src/shell.ts` | 受限 shell 执行 | `/bin/bash -c` 在 workspace cwd、独立 process group；timeout 1–600 秒；stdout/stderr 64 KiB 上限；环境使用 allow-list |
| `server/src/audit.ts` | 审计事件与敏感字段 | 事件区分 allowed/refused/failed、MCP callback refused 等；敏感 key 包含 token、password、result、content 等 |

### ⭐ 源码精读

**代码块 1：`matchesToken(expected, offered)`——没有 secret 时 fail closed，并避免简单前缀比较**

来源：`agent-computer/src/authorisation.ts:17-25`，固定 commit `6826e11...`。

```typescript
export function matchesToken(expected: string, offered: string): boolean {
  if (expected.length === 0) return false;
  if (offered.length !== expected.length) return false;
  let difference = 0;
  for (let index = 0; index < offered.length; index += 1) {
    difference |= offered.charCodeAt(index) ^ expected.charCodeAt(index);
  }
  return difference === 0;
}
```

逻辑摘要：空 expected 不会开放 computer；长度先拒绝，等长 token 逐字符 XOR 聚合差异。源码注释明确长度仍可能泄露，但 token 内容不通过前缀 timing 暴露。边界：这只是 computer port 的 token 认证，不是用户身份、授权策略、网络隔离或完整 session 证明。

**代码块 2：`govern(...)`——policy decision 必须先于 action effect**

来源：`server/src/computer/gateway.ts:468-483`。

```typescript
const decision = evaluateActionPolicy(options.policy(), context);
await write(auditStore, {
  toolName,
  botId,
  actor,
  element,
  ref,
  ...(subject.key ? { key: subject.key } : {}),
  ...(subject.command ? { command: subject.command } : {}),
  filePath,
  pageUrl,
  decision,
});
if (!decision.forward) {
  throw new ActionRefusedError(decision.reason, decision.matched);
}
```

逻辑摘要：先以服务端解析出的 `element`、目标 page、file path、command 和 intent 生成 policy context；不论允许还是拒绝，先写 decision audit；`forward=false` 立即抛出，因此拒绝动作不会到达 computer。源码后续 `try/catch` 还会在被允许但执行失败时写第二条 failure row。边界：审计 row 不是 effect receipt；“允许后失败”仍需区分部分副作用，computer/container 自身也必须提供边界。

**代码块 3：`environmentForCommand(...)`——shell 采用 allow-list，而不是 deployment env deny-list**

来源：`agent-computer/src/shell.ts:82-117`。

```typescript
export function environmentForCommand(
  source: NodeJS.ProcessEnv,
  workspaceDir: string,
): Record<string, string> {
  const env: Record<string, string> = {};
  const copy = (name: string) => {
    const value = source[name];
    if (value !== undefined) env[name] = value;
  };
  const copyProxy = (name: string) => {
    const value = source[name];
    if (value !== undefined) env[name] = withoutUserinfo(value);
  };
  for (const name of PATH_NAMES) copy(name);
  for (const name of LOCALE_NAMES) copy(name);
  for (const name of TERMINAL_NAMES) copy(name);
  for (const name of PROXY_NAMES) copyProxy(name);
  for (const name of extraShellEnvNames(source.COMPUTER_SHELL_ENV)) copy(name);
  env.HOME = workspaceDir;
  if (env.DEBIAN_FRONTEND === undefined) env.DEBIAN_FRONTEND = "noninteractive";
  return env;
}
```

逻辑摘要：默认不把 `process.env` 全量交给 agent shell；PATH、locale、terminal、proxy 和显式额外变量才进入子进程，proxy userinfo 会被剥离，HOME 指向 workspace。该文件还拒绝 `BASH_ENV`、`LD_PRELOAD` 等 hook 型环境变量。边界：源码注释明确“安全不是这个文件单独提供的”：shell 仍可执行任意命令，内容 policy 不能替代 container isolation；部署侧必须决定每 Bot 独立 computer、网络和权限。

### 依赖分析与供应链风险

- 根 `package.json` 声明 `bun@1.3.14`；root dependencies 为空，workspace 包分别声明依赖。
- `server/package.json` 的核心依赖：`@ag-ui/client 0.0.57`、`@copilotkit/runtime 1.68.3`、`@modelcontextprotocol/sdk ^1.30.0`、`better-auth ^1.7.1`、`cel-js ^0.8.2`、`drizzle-orm ^0.45.2`、`hono ^4.10.0`、`postgres ^3.4.9`、`rxjs 7.8.1`、`yaml ^2.9.0`、`zod ^4.4.3`。
- `agent-computer/package.json` 的核心依赖：`playwright 1.62.1`、`spiffe ^0.5.1`、`yaml ^2.9.0`；浏览器自动化、网络、容器/identity 和 MCP 都是高权限供应链面。
- 本地未安装 Bun，故未运行 `bun test`、`bun run typecheck` 或 Docker integration；不能把 GitHub 上的 test 文件视为本地通过结果。需要在 Bun 1.3.14 和项目要求的 Docker/PostgreSQL/Chromium 条件下复验。
- `README` 依赖 CopilotKit Intelligence、模型 key、PostgreSQL，并支持 Docker image；外部 SaaS、模型 provider、Docker image、Playwright browser 与 MCP server 的 license/update/security 均不由根 MIT 自动覆盖。
- `.github/workflows/security_zizmor.yml` 存在，但这不等于运行环境或 agent action surface 已安全；不能据 workflow 名称推断无漏洞。

### README / release / issues / source 交叉核验

- README 的 “one gateway decides and records it” 与 `gateway.ts` 的 `resolve -> evaluate -> write -> forward` 顺序一致。
- README 的 “CEL policy, fail closed” 与 `policy.ts` 的 absent policy、deny precedence、broken expression handling 一致。
- README 的 “secrets never enter transcript” 与 `computer-gateway.test.ts` 对 typed text、file contents、shell output 的断言一致。
- Release API 的 v0.0.4 与 `pushed_at` 接近，说明项目处于快速迭代阶段；README 自己标注 Alpha，不能按稳定平台处理。
- Issue #193/#192/#190 显示定时工作、Bot-to-Bot messaging、per-Bot screen tracking 仍在活跃讨论；不能把这些 issue 当作已完成能力。

### 可复用经验

- **当 agent 可以触发浏览器、shell、文件或 MCP 副作用时，应优先把“服务端解析真实 target → policy → audit → effect”做成唯一入口，因为模型自报的名称和客户端路径都可被绕过；边界是 gateway 不能替代 container、network 和 identity isolation。**
- **当动作引用来自动态页面时，应优先使用服务端持有的 opaque ref + snapshot generation/session，而不是接受模型传回的 label，因为旧 ref 不能被重新解释成当前元素；边界是 snapshot freshness 仍需和 computer 端状态一起校验。**
- **当审计要支持事故分析时，应优先分开“policy allowed/refused”和“effect succeeded/failed”，因为允许不代表执行成功；边界是审计日志本身不能证明第三方副作用是否已回滚。**
- **当 shell 运行在带有部署 secret 的进程旁边时，应优先使用环境变量 allow-list、workspace HOME、超时、process group 和输出上限，而不是只维护一个不断过期的 secret deny-list；边界是任意 shell 仍须放进隔离 computer/container。**

### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/openbot-governance-envelope/` 做离线 Python fixture，不安装 OpenBot、不启动 browser：

1. 定义 `ActionRequest(bot_id, snapshot_id, ref, intent, target, command)`、`PolicyDecision`、`AuditReceipt` 三个 JSON schema。
2. 写一个纯函数实现 `resolve -> deny/allow -> decision receipt -> effect stub`；规则至少覆盖缺少 policy、ref generation mismatch、敏感 path、`run_command` 禁止和 allowed-but-failed。
3. 断言：拒绝请求不调用 effect stub；允许后 stub 失败产生 `allowed` 与 `failed` 两条 receipt；typed text/file contents 不进入 receipt。
4. 输出进入 `runtime/hermes/`；不改 Hermes 配置，不写 secret，不进入 curated。

### 风险边界

- **License**：根仓库 API license 为 MIT；第三方 Bun/npm 包、CopilotKit Intelligence、Docker/base image、Playwright browser、MCP server 和模型服务各自需要独立 license/供应链审核，不能把它们都视为 MIT。
- **维护活跃度**：API `pushed_at=2026-08-22T21:48:01Z`，最新 release v0.0.4 于 `2026-08-22T21:48:02Z`，很活跃但也很早期；README 明确 Alpha/active development。
- **安全**：gateway 是主要治理点；直连 agent-computer 服务端口、绕过 gateway 或把 supervisor token 暴露给 Bot 都会破坏模型。shell command 文本匹配只是 filter，不是 sandbox；README 也要求私有 computer endpoints。
- **身份/部署**：`.env.example` 的 `OPENBOT_SINGLE_USER=true` 适合本地启动但不适合多人部署；README 要求在其他人可访问前配置 sign-in。不能在 Hermes 中自动采纳该默认值。
- **可用性**：当前没有 Bun，OpenBot test/typecheck/CI 状态待核验；项目依赖 Docker、PostgreSQL、Chromium/Playwright、CopilotKit Intelligence 与模型 key，完整 E2E 不在本次环境完成。
- **不适用场景**：不能直接用于高风险金融/生产写入、分布式 exactly-once、跨租户强隔离或无人工审批的 credential/secret 操作；必须另外设计 fencing、approval、rollback 和独立审计。
- **不能自动执行**：不 clone/install/start OpenBot product，不配置 provider/token，不启动 Docker/浏览器，不把任何源码复制进 shared skill。

### ⭐ Skill 升格判断

**需二次验证。** 可候选化的是 agent-neutral 的 `governed-action-receipt` 工作流（服务端 target resolution、policy decision receipt、effect outcome、sensitive payload redaction），不是 OpenBot 本身，也不是其 TypeScript 源码。原因：模式与 Hermes 的审计/verification-first/shared-memory 方向有复用价值，但 OpenBot 本地 Bun/多服务集成未在本机运行，且 action semantics、identity、container boundary 还需和 Hermes tool executor 对齐。今日不创建 shared skill，不写 curated active fact。

### Hermes / shared hub 落地路径

1. **Hermes runtime POC**：`runtime/hermes/github-learning-poc/openbot-governance-envelope/{schema.json,checker.py,fixtures/,README.md}`；只实现离线 receipt，不调用 provider/tool。
2. **Hermes tool 接点**：未来在 host-owned tool executor 增加 `target_ref/target_generation/policy_decision/effect_status/receipt_id`；模型 prose 不能成为授权证据，配置仍由 `~/.hermes/config.yaml` 等正式入口管理。
3. **审计接点**：GitHub learning orchestrator 的 `status.json`/audit 只采信 artifact readback、命令 exit code、hash/coverage；不要把模型报告中的“已完成”当作执行 receipt。
4. **shared hub 接点**：本日报和后续原始 evidence 继续写 `inbox/hermes/daily/`；fixture/log 写 `runtime/hermes/`；经评分、证据、去重、脱敏与人工/总控审查后，才考虑候选进入 `curated/memory/facts/` 或共享 skill。
5. **OpenClaw 边界**：当前不存在，不实施 OpenClaw adapter；未来只消费 agent-neutral receipt schema，并独立验证其 tool/session authority。

# 2. wang2122/sprix-sage-router

### 基本信息与核验来源

- URL：https://github.com/wang2122/sprix-sage-router
- GitHub API：**1,243 Stars / 12 Forks / Python / MIT**。
- API 时间：`created_at=2026-08-18T04:08:11Z`，`updated_at=2026-08-22T16:02:27Z`，`pushed_at=2026-08-21T08:45:27Z`，open issues `0`，default branch `main`。
- 固定源码 commit：`aed97852abc0bbd1dfccd8851b31290bc1b3f507`。
- Release API：`v0.1.0`，`published_at=2026-08-18T04:25:55Z`。
- README / `ALGORITHM.md`：项目将 SAGE 定义为 A2A discovery 与执行之间的 state-aware decision layer，支持 SELF、COLLABORATE、HANDOFF、requirement DAG、beam search、contextual trust、bid fidelity 和 evidence-aware credit。
- `pyproject.toml`：包版本声明 `0.2.0`、Python `>=3.10`、MIT、`py-modules=["sprix_sage"]`；GitHub release tag 为 v0.1.0。该版本差异是本次观察到的仓库状态，不能推断发布流程原因。
- 真实运行：`python -m unittest -v` 返回 **Ran 12 tests ... OK**；`python demo.py` 返回 `mode=collaborate`、`p(success)=0.814`、`cost=0.176`、`latency=1122 ms`；`python benchmark.py` 返回 2,500 tasks synthetic benchmark。

### 一句话判断：为什么值得学

**SAGE 值得学的是将“是否继续自己做”从静态 skill ranking 提升为受权限、预算、deadline、DAG 进度、context transfer loss 和 observed evidence 共同约束的三模式决策；它是可嵌入的研究原型，不是生产 A2A runtime。**

### 解决的问题：替代了什么旧做法

1. 替代只按 agent advertised skill 选一个人：先做 permission-first eligibility，再比较 SELF、COLLABORATE、HANDOFF。
2. 替代开工后不能调整：`ExecutionState` 保存 active agents、completed requirements、progress、failed agents 和 transferable context，失败后可以重新 route。
3. 替代把团队能力简单相加：按 requirement 做 noisy-OR coverage、DAG assignment 和 critical-path latency；互补能力而非 agent 名气进入判断。
4. 替代单一 global reputation：global reliability 与 requirement-conditioned reliability 分开，coding 的成功不会完全转移成 research 能力。
5. 替代把团队最终 outcome 等额归因给每个成员：`record_outcome` 优先使用 agent score、requirement score、weak team-only evidence，并为 pair synergy 使用 residual credit。
6. 替代不可解释的 winner：`RouteDecision` 具有 mode、agents、assignments、topology、utility、risk、cost、latency、explanation 和 diagnostics。
7. 替代无约束的全组合搜索：collaboration 使用 bounded beam search；但 `ALGORITHM.md` 明确这只是 bounded approximation，不声称全局最优。

### 架构 / 实现与数据流

```text
Agent metadata / A2A AgentCard mapping / bids
                  |
                  v
Task(requirement DAG, permissions, budget, deadline, progress)
                  |
                  v
Eligibility filter (availability + permission + cost + deadline)
                  |
                  +--> SELF: incumbent alone
                  +--> HANDOFF: one peer owns task
                  +--> COLLABORATE: bounded beam teams
                                  |
                                  v
        requirement coverage + DAG assignment + topology/schedule
                                  |
                                  v
        contextual trust + online success model + utility ranking
                                  |
                                  v
RouteDecision(mode, assignments, rationale, diagnostics)
                  |
                  v
ExecutionOutcome(success, per-agent/per-requirement scores, actual cost/latency)
                  |
                  v
reliability / skill reliability / synergy / bid fidelity / model updates
```

它本身只返回 routing decision，README 明确不传输 A2A tasks；真正的 `message/send`、streaming、polling、cancellation、authentication 和 execution recovery 需要外部 adapter。

### Repo tree 摘要（固定 commit）

```text
sprix-sage-router/
├── sprix_sage.py       # dataclasses、SAGERouter、DAG、beam search、online update
├── ALGORITHM.md        # 目标函数、eligibility、coverage、utility、credit 与局限
├── demo.py             # 端到端可读示例
├── benchmark.py        # 外部 nonlinear synthetic simulator 与 baseline
├── test_sprix_sage.py  # 12 个行为测试
├── pyproject.toml      # Python >=3.10、包 metadata、MIT
├── README.md           # 使用、A2A mapping、benchmark、roadmap
├── SECURITY.md         # 明确 reference implementation 的安全缺口
├── CITATION.cff        # 引用信息
├── docs/assets/        # routing system、policy map、benchmark 图
└── .github/workflows/tests.yml # CI
```

### 关键源码文件

| 文件 | 用途 | 本次核验摘要 |
|---|---|---|
| `sprix_sage.py` | 全部 reference router | `Requirement`/`Task` 验证 DAG；`Agent`/`Bid` 描述能力与报价；`SAGERouter.route` 过滤和比较三模式；`record_outcome` 更新证据模型 |
| `ALGORITHM.md` | 机制契约 | 说明 permission-first、contextual calibration、coverage、DAG schedule、online logistic model、bounded beam 与非生产限制 |
| `test_sprix_sage.py` | 行为边界 | 覆盖 self、handoff、collaboration、permission hard filter、DAG、deadline、skill isolation、partial credit、failed incumbent replan |
| `benchmark.py` | 外部评估 | 使用与 SAGE 预测模型不同的 nonlinear simulator，比较 self/skill_solo/oracle/static/learned；仍是 synthetic |
| `SECURITY.md` | 安全范围 | 明确不认证 agent、不签 Agent Card、不传输 task、不隔离执行、不存 credential、不 enforce network policy |
| `pyproject.toml` | 依赖/发布元数据 | Python >=3.10、runtime module 单文件；没有 requirements.txt，项目声明无 runtime dependencies |

### ⭐ 源码精读

**代码块 1：`BetaBelief.update(score, weight)`——把执行证据变成加权 posterior，而不是无条件全员记功**

来源：`sprix_sage.py:169-193`。

```python
@dataclass
class BetaBelief:
    alpha: float = 2.0
    beta: float = 2.0

    def update(self, score: float | bool, weight: float = 1.0) -> None:
        value = float(score)
        if not 0 <= value <= 1:
            raise ValueError("belief update score must be in [0, 1]")
        if weight <= 0:
            raise ValueError("belief update weight must be positive")
        self.alpha += weight * value
        self.beta += weight * (1.0 - value)
```

逻辑摘要：`score` 在 0–1，`weight` 必须为正；成功/失败或 partial score 以加权方式更新 Beta belief。`ALGORITHM.md` 进一步规定 explicit agent score 权重最高，requirement score 是 partial credit，只有 team-only outcome 时权重更弱。边界：这是在线统计更新，不是 causal credit assignment；项目自己要求 production 增加 logged propensities、randomized exploration 和 doubly robust off-policy evaluation。

**代码块 2：`SAGERouter.route(...)`——先 eligibility，再三模式比较，禁止高分越过硬约束**

来源：`sprix_sage.py:315-353`。

```python
def route(
    self,
    task: Task,
    bids: Iterable[Bid] | None = None,
    state: ExecutionState | None = None,
) -> RouteDecision:
    state = state or ExecutionState()
    self._validate_state(task, state)
    bid_map = self._prepare_bids(task, bids)
    eligible = [
        agent_id
        for agent_id, agent in self.agents.items()
        if agent_id not in state.failed_agents
        and self._eligible(agent, task, bid_map[agent_id])
    ]
    if not eligible:
        raise RuntimeError("no eligible agent satisfies permissions, budget, and deadline")
    decisions: list[RouteDecision] = []
    if self.incumbent_id in eligible:
        self_decision = self._evaluate(Mode.SELF, (self.incumbent_id,), task, bid_map, state)
        if self._team_feasible(self_decision, task):
            decisions.append(self_decision)
        decisions.extend(self._beam_collaboration_decisions(task, eligible, bid_map, state))
    for agent_id in eligible:
        if agent_id == self.incumbent_id:
            continue
        decision = self._evaluate(Mode.HANDOFF, (agent_id,), task, bid_map, state)
        if self._team_feasible(decision, task):
            decisions.append(decision)
    best = max(decisions, key=lambda decision: decision.utility)
    return replace(best, switch_recommended=bool(state.active_agents) and (...))
```

逻辑摘要：源码先排除 failed/unavailable/unauthorized/不满足预算和时限的 agent，再评估 SELF、bounded collaboration 和 HANDOFF；随后 `_team_feasible` 还会做 team-level budget/deadline 检查。测试真实验证了 permission hard filter、互补能力 collaboration 和 tight DAG deadline。代码块末尾的 `...` 是本报告为压缩展示的 `switched` 判断省略，不是声称源码存在省略号；固定源码完整逻辑为根据 active mode/agents 判断是否推荐切换。边界：`utility` 仍依赖先验和 synthetic/online model，不能替代真实执行授权。

**代码块 3：`record_outcome(...)`——按证据强度更新 agent、skill、pair 和 success model**

来源：`sprix_sage.py:355-406`。

```python
def record_outcome(self, decision: RouteDecision,
                   outcome: ExecutionOutcome | float | bool) -> None:
    evidence = outcome if isinstance(outcome, ExecutionOutcome) else ExecutionOutcome(outcome)
    unknown_agents = set(evidence.agent_scores) - set(decision.agents)
    unknown_requirements = set(evidence.requirement_scores) - set(decision.assignments)
    if unknown_agents or unknown_requirements:
        raise ValueError("outcome contains evidence outside the selected route")
    overall = _clip(float(evidence.success))
    self.success_model.update(decision.model_features, overall)
    # explicit agent score > assigned requirement scores > weak team-only credit
    for agent_id in decision.agents:
        explicit = evidence.agent_scores.get(agent_id)
        assigned_scores = [...]
        if explicit is not None:
            credit, weight = explicit, 1.0
        elif assigned_scores:
            credit, weight = sum(assigned_scores) / len(assigned_scores), 0.85
        else:
            credit, weight = overall, 0.35
        self.reliability[agent_id].update(credit, weight)
```

逻辑摘要：输入 evidence 不能引用未选中的 agent/requirement；全局 success 更新在线 logistic model；agent credit 按 explicit → requirement-derived → weak team-only 降级；随后源码还对 requirement skill reliability、pair synergy residual、actual cost/latency fidelity 做更新。边界：这里的“evidence”仍是调用方提交的观测，生产系统必须把它绑定到真实 execution receipt、身份、任务结果和不可抵赖的 telemetry，不能直接信任模型自报。

### 依赖分析与供应链风险

- `pyproject.toml` 声明 Python `>=3.10`，build backend `setuptools>=68`；`sprix_sage.py` 模块文档与 README 均说明无 third-party runtime dependencies。
- 仓库没有 `requirements.txt`；本次没有安装额外 runtime package，测试直接使用系统 Python。
- 依赖面相对窄，但 `setuptools`/Python build chain、CI action、未来 A2A adapter、Agent Card 输入和 marketplace bids 都会成为供应链/信任面。
- 当前实现不认证 agent、不签 Agent Card、不传输 A2A task、不隔离执行、不保存 credential、不执行 network policy；因此低依赖不等于可安全部署。
- `benchmark.py` 的 2,500-task 结果来自外部 nonlinear synthetic simulator；README 和 `ALGORITHM.md` 都警告这不是 real-world superiority，也不构成 peer-reviewed production evidence。
- package version `0.2.0` 与 GitHub latest release `v0.1.0` 同时存在；集成前应固定 commit/tag，避免把 main 上未发布接口当稳定 API。

### README / docs / release / issues / source 交叉核验

- README 的 A2A mapping（AgentCard skills → capability vector、security requirements → hard permissions、task status/artifacts/failures → ExecutionState）与 `sprix_sage.py` 的 data model 和 `ALGORITHM.md` 一致。
- README 的 “prototype returns a routing decision; it intentionally does not transmit tasks” 与 `SECURITY.md` 的 implementation scope 一致；所以本项目不能被误读成完整 A2A transport/runtime。
- `test_sprix_sage.py` 的 12 个测试真实通过，覆盖关键纯函数/路由行为，但没有证明真实 agent 网络、身份、恶意 bid、网络策略或分布式恢复安全。
- API release `v0.1.0` 与源码 `pyproject` version `0.2.0` 的差异被保留为待核验发布治理问题；没有依据声称它是 bug 或已发布版本。
- API open issues 为 0；这只表示当时公开 issue 列表没有开放 issue，不代表没有风险或没有外部反馈。

### 可复用经验

- **当多 agent 系统要在执行中途选择继续、协作或交接时，应优先先做 permission/availability/budget/deadline hard filter，再做质量 utility ranking，因为高分不能覆盖越权和不可行路线；边界是 eligibility 元数据必须认证且不可由 agent 自报。**
- **当任务含有多个依赖步骤时，应优先用 requirement DAG + assignment + critical-path 检查，而不是只按平均 skill 分数组队，因为互补能力可能被顺序、通信和 deadline 抵消；边界是 DAG 仍需由可信任务定义方提供。**
- **当执行反馈可区分到 agent 或 requirement 时，应优先使用 evidence-aware partial credit，并把 team-only outcome 降权，因为给每个成员同一成功分会污染可靠性和协作 synergy；边界是 receipt 必须来自真实执行，不能接受未经验证的模型总结。**
- **当 agent/模型声称的 capability 会影响未来路由时，应优先使用 requirement-conditioned trust，而不是把一个领域的 success 全局传播，因为跨领域泛化通常未经证明；边界是冷启动、样本偏差和探索成本仍要单独评估。**
- **当路由模型只有 synthetic benchmark 时，应优先把它当机制回归测试而不是生产排名依据，因为 benchmark 的外部 simulator 仍不能代表真实任务、攻击和成本；边界是上线前要做 trace replay、校准、adversarial 和 human approval 验证。**

### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/state-aware-route/` 做不接外部 agent 的纯 Python demo：

1. 把 Hermes 可用执行器抽象成 `Agent(id, capabilities, permissions, cost, deadline)`，任务使用 2–3 个 requirement 和一个依赖 DAG。
2. 先运行 permission-first eligibility，再输出 SELF/COLLABORATE/HANDOFF 三种候选及其 reason；禁止高质量但无权限的候选进入排序。
3. 运行一轮 `ExecutionOutcome` fixture，分别提供 requirement score、agent score 和 team-only score，检查三种证据对后验更新的权重不同。
4. 使用 `resolve_shared_root.py` 找到路径；只写 `runtime/hermes/`，不修改 Hermes config/provider/cron，不写 shared curated。

### 风险边界

- **License**：GitHub API 与 `pyproject.toml` 均为 MIT；若未来接入 A2A SDK、Agent Card parser、模型或 marketplace connector，需逐项审核，不把新增依赖自动视为 MIT。
- **维护活跃度**：API `pushed_at=2026-08-21T08:45:27Z`，项目创建于 2026-08-18，更新很新；但 README/pyproject/release 状态显示 research/alpha 过渡，不能当稳定 SLA。
- **安全**：`SECURITY.md` 明确 reference implementation 没有 authentication、signed Agent Cards、task transport、execution isolation、credential storage 或 network policy。它只能作为本地算法参考。
- **学习风险**：online model 会受错误、偏置或伪造 outcome 影响；没有 causal/off-policy 评估时，不应自动用其结果调高权限或 provider 信任。
- **性能/正确性**：bounded beam search 不是全局最优；DAG 和 utility 复杂度随候选、requirement、team size 增长；模型只能作决策建议，不能自动执行 handoff。
- **版本**：GitHub latest release v0.1.0 与 checkout 的 `pyproject` 0.2.0 不同；集成要 pin commit 并做 contract test。
- **不适用场景**：不适合直接管理真实资金、生产数据库写入、密钥操作、多租户 A2A marketplace 或无审批的 agent-to-agent handoff。
- **不能自动执行**：不接真实 A2A endpoint、不发送 task、不导入未知 Agent Card、不改变 Hermes provider/model/fallback/cron，不把 benchmark 结果写成 curated fact。

### ⭐ Skill 升格判断

**需二次验证。** 可候选化的是 `permission-first-progress-aware-routing` 的窄 workflow：hard eligibility → explicit route alternatives → auditable rationale → execution receipt → evidence-aware update。不能直接迁移 `sprix_sage.py` 或其 learned weights。原因：纯 Python 测试已通过且机制与多 agent 编排相关，但其 security scope 明确不生产，A2A transport/identity/receipt 都缺失。先在 Hermes runtime POC 做 contract test，再与 shared 已有 autonomous-learning、多 agent orchestration、verification-first 事实去重；今日不创建 shared skill，不写 curated active fact。

### Hermes / shared hub 落地路径

1. **POC 文件**：`runtime/hermes/github-learning-poc/state-aware-route/{schema.py,fixtures/,checker.py,README.md}`；把 route decision 作为建议对象，不直接 dispatch。
2. **Hermes 编排接点**：在未来多 agent task planner 之前插入 `EligibilityGate`；接口输入仅使用已注册 agent capability/permission、任务约束和可信 runtime state，输出 `RouteDecision` + reason + constraints。
3. **receipt 接点**：路由结果必须绑定 `run_id/task_id/selected_agents/requirements`，完成后只能从 host/tool receipts 生成 `ExecutionOutcome`；模型报告不能直接回写 reliability。
4. **shared hub 接点**：候选方法论保持在本日报和 `runtime/hermes/`；经过治理评分、证据、去重、脱敏与审查后，才考虑放入 `curated/memory/facts/` 或 shared skill manifest。不要复制原项目源码。
5. **Hermes audit 接点**：把 route reason、hard-filter rejection、artifact readback 和 audit score 分开记录；audit score 不能覆盖 missing artifact。
6. **OpenClaw 边界**：当前 OpenClaw 不存在；未来仅共享 agent-neutral route schema，并要求 OpenClaw 自己验证 task/session authority。

## 经验沉淀

1. **当 agent 工具具有外部副作用时，应优先采用“server-owned target + hard policy + pre-effect audit + post-effect outcome”的四段式契约，因为客户端/模型输入、允许和成功是不同事实；边界是还需要 container/network/identity 证明。**
2. **当任务路由会受到权限、预算、时限影响时，应优先先过滤不可行候选，再按质量与成本排序，因为 utility 不能覆盖硬约束；边界是输入元数据必须来自可信注册表。**
3. **当执行结果可细分到 requirement 时，应优先做 requirement-conditioned、evidence-aware 更新，而不是给团队成员统一成功分，因为后者会把协作相关性误写成个人能力；边界是 evidence 必须绑定真实 receipt。**
4. **当项目文档声称有安全边界时，应优先读取关键源码与 counterexample tests，再决定是否升格 skill，因为 prose contract、regex hook 和默认配置都可能与 enforcement 不同；边界是本次 OpenBot 因 Bun 缺失仍有本地运行空白。**
5. **当共享中台沉淀跨 agent 方法论时，应优先把原始日报写入 `inbox/hermes/daily/`、POC 写入 `runtime/hermes/`，经过证据/评分/去重/脱敏/审查后再晋升 curated，因为 raw 日志不是跨 agent 真相源。**

## 风险边界与安全反哺

- 不自动改配置、模型、provider、auth、env、cron 或 secret。
- 不自动启动 OpenBot、A2A endpoint、browser、Docker 或任何外部 agent runtime。
- 不把模型输出、benchmark 数字或本日报直接写入 `curated/memory/`；本次只提出 candidate。
- 不复制 license 不明、API 返回 `NOASSERTION` 或未完成兼容审查的仓库源码。
- OpenBot 的 MIT 只覆盖其仓库代码，不覆盖依赖、服务、模型、Docker image、browser 和 MCP vendor。
- SAGE 的测试与 benchmark 证明的是当前纯 Python 机制/模拟器行为，不证明生产安全、真实路由优势或不可篡改的 outcome。
- 巡检/审计建议只输出风险、证据、影响、建议动作；不自动修复。

## Skill 升格总判断

今日两个深读项目的共同模式**暂不直接升格为 shared skill**，结论均为“需二次验证”：

- OpenBot：候选是 governed action receipt，不是 OpenBot product/source；需要 Bun/E2E、Hermes tool executor 接口、identity 和 container boundary 复验。
- SAGE：候选是 permission-first progress-aware routing，不是其 learned weights/source；需要 Hermes runtime POC、真实 receipts、离线回放和安全评审。
- 升格前必须复制完整 skill 目录、更新 `capabilities/manifests/shared-skills.yaml` 的 `scope/reference_policy/future_agent_readable`，并与现有 shared facts/skills 去重；本次未执行这些写入。

## 明日继续

**最小下一步：在 `runtime/hermes/github-learning-poc/` 完成一个不接 provider 的 `governed-action-receipt + permission-first-route` 联合 fixture，至少覆盖 stale target、absent policy、unauthorized candidate、budget/deadline rejection、allowed-but-failed、partial outcome 六类反例，然后用真实测试输出决定是否进入 candidate queue。**

## 候选反哺

### Candidate Facts

- [ ] topic: OpenBot 的服务端 target resolution → policy → audit → effect 顺序是可迁移治理模式 | evidence: `server/src/computer/gateway.ts` fixed commit `6826e11...`、README、`computer-gateway.test.ts` | 建议: create candidate fact after Hermes POC and review | 安全级别: medium
- [ ] topic: SAGE 的 permission-first tri-mode routing 与 evidence-aware update | evidence: `sprix_sage.py`、`ALGORITHM.md`、12 tests passed、`SECURITY.md` | 建议: create candidate fact only after receipt-bound replay | 安全级别: medium
- [ ] topic: OpenBot root requires Bun 1.3.14 but current WSL lacks Bun | evidence: root `package.json` and real command output `bun: command not found` | 建议: create operational open question, not curated engineering fact | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: governed-action-receipt | 可复用场景: Hermes tool execution、GitHub learning audit、未来 agent tool gateway | 是否建议 shared: yes, after second validation | 原因: Hermes/OpenClaw/future-agent 都可能需要把授权、执行和审计分开；当前只做 runtime POC，不复制 OpenBot
- [ ] 名称: permission-first-progress-aware-routing | 可复用场景: 多 agent task planner 的 self/collaborate/handoff 建议 | 是否建议 shared: yes, after receipt-bound replay | 原因: 与 shared autonomous-learning/multi-agent orchestration 横切相关，但当前参考实现缺 identity/transport/isolation

### Candidate Open Questions

- [ ] 问题: Hermes 当前 tool executor 的真实 effect receipt 是否能提供 stable `run_id/operation_id/target_generation`？ | reason: gap | priority: high
- [ ] 问题: 当前环境何时提供 Bun 1.3.14、Docker、PostgreSQL 与 Chromium，以复验 OpenBot test/typecheck/E2E？ | reason: gap | priority: medium
- [ ] 问题: SAGE `pyproject` 0.2.0 与 GitHub latest release v0.1.0 的发布治理差异是什么？ | reason: stale/conflict | priority: low
- [ ] 问题: 未来多 agent 路由如何绑定注册 capability、权限和人类审批，而不是信任 AgentCard 自报？ | reason: adaptation | priority: high

### 不应自动落地

- 不自动安装或启动 OpenBot，不自动安装 Bun/Docker，不向任何 provider 或 A2A endpoint 发送请求。
- 不自动把 SAGE 的 learned weights、synthetic benchmark 或 route choice 变成 Hermes 权限、provider fallback 或 cron 决策。
- 不把 candidate facts/skills 直接写入 `curated/memory/` 或 `capabilities/skills/`；须经过评分、证据、去重、脱敏与审查。
- 不写入明文 API key、token、password、模型 credential 或任何 OpenClaw/Hermes secret。

## 证据路径与完整产物

- 本日报：`inbox/hermes/daily/2026-08-23-github-learning.md`
- POC 预留目录：`runtime/hermes/github-learning-poc/`（本次未创建代码，避免以 stub 冒充已验证 artifact）
- 项目卡片：`runtime/hermes/github-learning/projects/CopilotKit-OpenBot.md`、`runtime/hermes/github-learning/projects/wang2122-sprix-sage-router.md`
- 经验追加：`runtime/hermes/github-learning/lessons.md`
- 审计状态：由 `python3 scripts/github_learning_orchestrator.py --runner hermes --audit-only` 更新 `runtime/hermes/github-hot-project-learning/status.json`
