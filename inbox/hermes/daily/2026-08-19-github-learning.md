# GitHub 热门项目每日学习报告

- 日期：2026-08-19
- 执行器：Hermes
- 研究时间：2026-08-19 07:31-07:38 +08:00
- 数据查询：GitHub API / `gh api`；源码核验为各仓库当日浅克隆的 commit
- 研究边界：OpenClaw 运行时不存在，本报告未调用 OpenClaw，也未把未核验内容写成事实

## 今日结论

今日主线是：把 Agent 的“会做事”拆成可验证的工作流外壳、项目作用域学习和副作用门控，再以 Hermes 的已有 bundle、memory provider 与分段工具执行接口承接，而不是直接复制上游仓库。

## 项目速览

以下 Stars、License、更新时间均来自 GitHub API 查询；查询时间约为 2026-08-19 07:31-07:35 +08:00。

| 项目 | Stars | Language | License | updated_at | 选择理由 |
|---|---:|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 273,669 | Shell | MIT | 2026-08-18T23:31:10Z | 可组合 skills 与强制工作流 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 240,961 | JavaScript | MIT | 2026-08-18T23:13:22Z | hooks、项目级 continuous learning、安全 guard |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 232,530 | Python | MIT | 2026-08-18T23:31:10Z | 当前 Hermes 上游，直接核验运行时机制 |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | 201,117 | TypeScript | NOASSERTION | 2026-08-18T22:58:44Z | 工作流编排候选；License 待进一步核验 |
| [ollama/ollama](https://github.com/ollama/ollama) | 178,901 | Go | MIT | 2026-08-18T23:04:29Z | 本地模型服务与简化入口 |
| [astral-sh/uv](https://github.com/astral-sh/uv) | 88,857 | Rust | Apache-2.0 | 2026-08-18T23:36:04Z | 依赖/运行环境的快速、可复现管理 |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) | 124,579 | Go | Apache-2.0 | 2026-08-18T23:15:59Z | 控制面与 reconciliation 机制参考 |

速览项目未进行本日报要求的源码深读；除 API 字段外，n8n 的 License 为 `NOASSERTION`，不要据此自动复制其代码或得出许可证兼容结论。

## 深读项目

### 项目 1. obra/superpowers

#### 基本信息与证据

- 链接：https://github.com/obra/superpowers
- API：Stars `273,669`，Forks `24,488`，主语言 `Shell`，License `MIT`，`pushed_at=2026-08-13T00:36:31Z`，`updated_at=2026-08-18T23:31:10Z`，open issues `324`。
- 源码 commit：`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`，default branch `main`。
- README 证据：项目描述为可组合 skills 加启动指令；基本工作流依次覆盖 brainstorming、worktree、plan、subagent、TDD、review、finish；README 明确列出 Hermes plugin 安装路径。
- Release/issue 证据：最近 release `v6.3.0`，发布时间 `2026-08-12T16:58:30Z`；开放 PR/issue 示例包括 `#2174 docs: add Freebuff integration guide`、`#2173 fix: add hooks.json at plugin root for Devin CLI/Desktop SessionStart bootstrap`、`#2172` shellcheck 修复，更新时间均为 2026-08-18。

#### 一句话判断

值得学的不是某个 prompt，而是把设计、实现、测试、审查和完成验证串成有明确触发条件的 skill contract。

#### 解决的问题

它替代“用户一句话后 Agent 直接改代码”的不可重复做法：先细化设计，再建立计划，再用 TDD 和分阶段 review 执行。它把跨 harness 的安装入口也纳入插件层，而不是要求每个会话手工粘贴长规则。

#### 架构/实现与数据流

1. `skills/` 是过程能力目录，包含 brainstorming、writing-plans、TDD、systematic-debugging、subagent-driven-development、verification-before-completion 等 skill。
2. 启动层由 `hooks/session-start` 或具体 harness plugin 注入 bootstrap；OpenCode plugin 通过 config hook 注册 skills 路径，再通过 message transform 注入第一条 user message。
3. 运行时数据流为：会话启动 -> 加载 `using-superpowers` -> 根据任务触发 skill -> 生成设计/计划 -> 执行与审查 -> 完成前再次验证。
4. 关键依赖很少：`package.json` 仅声明 package 元数据、ES module、Pi extensions 与 skills 目录；没有运行时 npm dependencies。

#### repo tree 摘要

```text
obra/superpowers/
├── skills/                  # 可组合的流程 skills
│   ├── brainstorming/       # 需求澄清与设计
│   ├── test-driven-development/ # RED-GREEN-REFACTOR
│   ├── systematic-debugging/     # 根因定位与防御性修复
│   ├── subagent-driven-development/ # task + review loop
│   └── verification-before-completion/ # 完成前证据门
├── hooks/session-start      # 启动时注入 bootstrap
├── .opencode/plugins/       # OpenCode config/message transform 适配器
├── .hermes-plugin/          # Hermes 插件清单
├── tests/                   # harness 与 skill 行为测试
├── package.json             # package/ Pi 元数据
└── LICENSE                  # MIT
```

#### 关键源码文件

- `skills/using-superpowers/SKILL.md`：把“发现相关 skill 并先调用”设为会话入口规则，并要求根据 harness 读取工具映射。
- `skills/subagent-driven-development/SKILL.md`：定义 implementer -> task review -> fix loop -> final review 的状态机，并要求每轮有 diff/review artifact。
- `skills/verification-before-completion/SKILL.md`：要求在声明完成前执行新鲜验证，不能用“应该可以”代替命令输出。
- `.opencode/plugins/superpowers.js`：实现路径解析、bootstrap 缓存、技能目录注册和幂等 message transform。
- `hooks/session-start`：按平台输出不同 JSON context 字段，避免重复注入。

#### ⭐ 源码精读

1. `extractAndStripFrontmatter(content)`：先用 frontmatter 分隔线拆出 body，再以首个冒号拆 key/value；无 frontmatter 时返回原文。这是低依赖的启动路径解析器，适合 bootstrap，但不应当替代通用 YAML 解析器。

```javascript
const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };
  const frontmatter = {};
  for (const line of match[1].split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }
  return { frontmatter, content: match[2] };
};
```

2. `getBootstrapContent()`：模块级 `_bootstrapCache` 使用 `undefined` 表示未加载、`null` 表示文件不存在；同一会话避免重复磁盘读取和正则解析。这个 cache 只缓存静态 skill，不缓存用户事实。

```javascript
let _bootstrapCache = undefined;
const getBootstrapContent = () => {
  if (_bootstrapCache !== undefined) return _bootstrapCache;
  const skillPath = path.join(superpowersSkillsDir, 'using-superpowers', 'SKILL.md');
  if (!fs.existsSync(skillPath)) {
    _bootstrapCache = null;
    return null;
  }
  const fullContent = fs.readFileSync(skillPath, 'utf8');
  const { content } = extractAndStripFrontmatter(fullContent);
  _bootstrapCache = `<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n${content}\n</EXTREMELY_IMPORTANT>`;
  return _bootstrapCache;
};
```

3. `experimental.chat.messages.transform`：只找第一条 user message，检测已有 `EXTREMELY_IMPORTANT` 后才 unshift bootstrap，形成幂等注入；技能路径通过 config hook 加入运行时配置，不修改用户配置文件。

```javascript
'config': async (config) => {
  config.skills = config.skills || {};
  config.skills.paths = config.skills.paths || [];
  if (!config.skills.paths.includes(superpowersSkillsDir)) {
    config.skills.paths.push(superpowersSkillsDir);
  }
},
'experimental.chat.messages.transform': async (_input, output) => {
  const bootstrap = getBootstrapContent();
  if (!bootstrap || !output.messages.length) return;
  const firstUser = output.messages.find(m => m.info.role === 'user');
  if (!firstUser || !firstUser.parts.length) return;
  if (firstUser.parts.some(p => p.type === 'text' && p.text.includes('EXTREMELY_IMPORTANT'))) return;
  firstUser.parts.unshift({ ...firstUser.parts[0], type: 'text', text: bootstrap });
}
```

`hooks/session-start` 的 `escape_for_json()` 也体现同一思路：先转义反斜杠、引号、换行、回车和 tab，再按 Cursor、Claude 或 Copilot 输出各自 context schema，避免一份 JSON 同时写入两个字段导致重复注入。

#### 依赖分析与供应链风险

- `package.json`：无 `dependencies`；`type=module`；Pi 扩展为 `.pi/extensions/superpowers.ts`；skills 目录作为 Pi skills 入口；主入口为 `.opencode/plugins/superpowers.js`。
- 供应链优势：运行时依赖小，主要风险转移到 harness plugin API、远程安装来源和 skill 文本本身。
- 风险：README 仍建议从 GitHub plugin marketplace/仓库安装；安装时应固定 commit 或受信任 release，不应让未知 fork 直接修改 Hermes plugin。可选 visual companion 会请求项目外部 telemetry 资源，README 说明可用 `SUPERPOWERS_DISABLE_TELEMETRY` 关闭；本次未运行该功能。
- MIT 允许机制重写，但不能把上游 skill 原文或商标/telemetry 逻辑不加审查复制到 shared。

#### 可复用经验

- 当 Agent 任务有稳定的先后阶段时，应优先把阶段写成可触发、可 review、可验证的 skill contract，因为单一 system prompt 很难保证每轮都遵守；边界是不同 harness 的 hook/skill 能力不等价。
- 当启动上下文会在多步或重放中重复注入时，应优先使用内容 cache 加幂等 sentinel；边界是 cache 只适合静态内容，用户事实和权限不能靠 cache 记忆。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/superpowers-bootstrap/` 做离线 fixture：模拟 0/1/2 次 session bootstrap，验证输出只含一份 sentinel；再模拟 missing skill、Windows-like path 和不同 harness schema，要求失败返回可识别状态，不改 `~/.hermes`。

#### 风险边界

- License：GitHub API 与 `LICENSE` 均为 MIT；可抽象机制，但复制源码仍需保留版权和逐文件审查。
- 安全：bootstrap 文本可影响 Agent 行为；外部 plugin 安装与 optional telemetry 是供应链/隐私边界；不自动安装、不自动修改 Hermes 配置。
- 维护活跃度：API 的 `pushed_at` 为 2026-08-13，`updated_at` 为 2026-08-18；release `v6.3.0` 在 2026-08-12，活跃度较高但开放 issue/PR 仍需持续观察。
- 不适用：不能把 Claude/OpenCode 的 hook 语义直接推断为 Hermes 语义；不能用 message 注入替代 host-owned tool permission。

#### ⭐ Skill 升格判断

**需二次验证**。可提取“静态 bootstrap + 幂等 sentinel + harness adapter”机制，但当前 shared hub 已有 path portability、verification-first 和 skill contract 规则；应先做 Hermes fixture，确认不会重复加载已有 Hermes skills，也不会越过当前 profile 的权限边界。暂不复制上游 SKILL.md 原文。

#### ⭐ Hermes/shared hub 落地路径

- Hermes 本地实验：`runtime/hermes/github-learning-poc/superpowers-bootstrap/` 放 fixture、输出和验证日志。
- 若通过验证，再建本地 skill：`~/.hermes/skills/superpowers-bootstrap/SKILL.md`，只写触发条件、sentinel 规则、harness mapping 和测试命令。
- 若确认 Hermes/OpenClaw/future-agent 都需要，升格到 `capabilities/skills/foundation/skill-bootstrap-contract/`，在 `capabilities/manifests/shared-skills.yaml` 增加 `scope`、`reference_policy`、`future_agent_readable`；不写入 `curated/memory` active fact。
- Hermes 使用现有 `agent/skill_commands.py` 或 skill loader 接口；OpenClaw 运行时不存在，不能本日实施其配置改动。

### 项目 2. affaan-m/ECC

#### 基本信息与证据

- 链接：https://github.com/affaan-m/ECC
- API：Stars `240,961`，Forks `36,544`，主语言 `JavaScript`，License `MIT`，`pushed_at=2026-08-18T20:07:38Z`，`updated_at=2026-08-18T23:13:22Z`，open issues `137`。
- 源码 commit：`06c5e118c4d3e6c3b7f9445f973a2194c82de193`，default branch `main`。
- README 证据：项目把工作流写成 `plan -> test -> implement -> review -> verify -> remember -> improve`，同时强调各 harness 只选一种安装方法，避免重复 skills/hooks/config。
- Release/issue 证据：最近 release `v2.1.0`，发布时间 `2026-07-27T18:10:46Z`；`#2818` selective install state merge 修复、`#2817` npm 12 pack output 修复、`#2816` npm 12 导致的测试失败问题均在 2026-08-18 更新，说明安装/打包兼容是当前维护面。

#### 一句话判断

值得学的是“观察先于总结、项目作用域优先、候选 instinct 需要证据与 promotion gate”的持续学习闭环；它不是把所有会话内容直接写入全局记忆。

#### 解决的问题

它替代了全局、无作用域、无 TTL 的“从每次会话自动抽取永久规则”做法：先把 tool start/complete 记录到 project-scoped observations，再由 observer 聚类成 project instinct，达到跨项目和置信度门槛后才 promotion 到 global。

#### 架构/实现与数据流

1. `hooks/hooks.json` 把 PreToolUse、PostToolUse、SessionStart、PreCompact、Stop 等生命周期接到统一 dispatcher。
2. `skills/continuous-learning-v2/hooks/observe.sh` 读取 JSONL hook 输入，识别 git project，写入 project observations，并带有 automated session、secret scrub、文件大小和 observer liveness guard。
3. `scripts/observe-runner.js` 解析 plugin root、阻止 path traversal、选择 shell、执行 observe.sh，并在 runtime 失败时 passthrough 原始 hook 输入。
4. `scripts/continuous-learning-v2/instinct-cli.py` 维护 project/global 目录、confidence、promotion、import URL 校验和 pending TTL。

#### repo tree 摘要

```text
affaan-m/ECC/
├── hooks/                  # 生命周期 hook graph 与安装说明
├── scripts/hooks/          # dispatcher、observe runner、session persistence
├── skills/continuous-learning-v2/
│   ├── hooks/observe.sh    # project-scoped observation writer
│   ├── agents/observer.md  # pattern -> instinct 规则
│   ├── scripts/instinct-cli.py # import/evolve/promote/prune
│   └── config.json         # observer 默认关闭、间隔与阈值
├── agents/ commands/ rules/ # harness 内容与规则
├── .codex/ .hermes/ .openclaw/ # 各 harness 适配入口
├── package.json             # ecc-universal 依赖与脚本
└── LICENSE                  # MIT
```

#### 关键源码文件

- `scripts/hooks/observe-runner.js`：跨平台 runner，统一 root/path/shell/timeout，并确保 observer 失败不阻断主 hook。
- `skills/continuous-learning-v2/hooks/observe.sh`：把 tool event 变成带 `project_id`、`project_name` 的 observation；有 secret scrub 和非人工会话过滤。
- `skills/continuous-learning-v2/scripts/instinct-cli.py`：project hash、remote import SSRF 防护、promotion/confidence、pending TTL。
- `hooks/hooks.json`：把 observe runner 挂到 `PreToolUse`/`PostToolUse`，并挂接 config protection、GateGuard、session persistence 等安全面。
- `package.json`：版本 `2.2.0`，运行时依赖 `@iarna/toml`、`ajv`、`js-yaml`、`sql.js`，Node `>=18`。

#### ⭐ 源码精读

1. `run(raw, options={})`：从 hook id 推断 pre/post；解析 plugin root 后将目标限制在 root 内；找不到 shell 或脚本时返回 warning + exit 0，避免学习 hook 破坏主流程。

```javascript
function resolveTarget(rootDir, relPath) {
  const resolvedRoot = path.resolve(rootDir);
  const resolvedTarget = path.resolve(rootDir, relPath);
  if (resolvedTarget !== resolvedRoot &&
      !resolvedTarget.startsWith(resolvedRoot + path.sep)) {
    throw new Error(`Path traversal rejected: ${relPath}`);
  }
  return resolvedTarget;
}

function getPhaseFromHookId(hookId) {
  const prefix = String(hookId || process.env.ECC_HOOK_ID || '').split(':')[0];
  return prefix === 'pre' || prefix === 'post' ? prefix : null;
}
```

2. `emitHookResult(raw, output)`：若 child 有 stdout 就透传 child 输出，否则在 exit 0 时透传原始 hook 输入；这使 observer 可以作为非破坏性 adapter，失败不丢主事件。

```javascript
function emitHookResult(raw, output) {
  if (output && typeof output === 'object') {
    if (output.stderr) process.stderr.write(String(output.stderr));
    if (Object.prototype.hasOwnProperty.call(output, 'stdout')) {
      process.stdout.write(String(output.stdout ?? ''));
    } else if (!Number.isInteger(output.exitCode) || output.exitCode === 0) {
      process.stdout.write(raw);
    }
    return Number.isInteger(output.exitCode) ? output.exitCode : 0;
  }
  process.stdout.write(raw);
  return 0;
}
```

3. `detect_project()` / `_normalize_remote_url()` 的机制：优先显式 `CLAUDE_PROJECT_DIR`，再 git root，再 global；有 remote 时对 remote URL 做 credential strip、协议归一化和 `.git` 去除，再 SHA-256 截短形成 portable project id。这个顺序使同一远程项目跨机器更容易复用，但无 remote 的 path fallback 仍是机器相关。

```python
def _project_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]

# project id source: normalized remote URL, otherwise project root
hash_input = normalized_remote or remote_url or fallback_root
project_id = _project_hash(hash_input)
```

4. `observe.sh` 的安全边界另外值得保留：它过滤 `agent_id`、`ECC_SKIP_OBSERVE=1` 和 observer path，观察数据写入前对 token/secret/password 等模式做 scrub；observer 默认配置 `enabled=false`，阈值为 20 条 observation。该结论来自 `config.json`、`observer.md` 和 `observe.sh`。

#### 依赖分析与供应链风险

- `package.json` runtime dependencies：`@iarna/toml=2.2.5`、`ajv=8.20.0`、`js-yaml=4.3.1`、`sql.js=1.14.1`；Node engine `>=18`；大量行为由自有 JS/Shell/Python 实现。
- 供应链优势：`package.json` 明确发布 files；README 警告只从官方 GitHub/npm/GitHub App 来源安装；脚本中有 supply-chain IOC/advisory 检查入口。
- 供应链风险：hook graph 复杂，安装脚本会接触 harness 配置、MCP 和生命周期；错误的重复安装会造成重复 hook/skill；npm 12 的 pack 变化已有 issue，安装路径必须跟 release/测试一起核验。
- MIT 允许机制抽象；不要复制 ECC 的全量 rules、hooks 或品牌资产进入 shared。远程 instinct import 即便使用 HTTPS，也必须保留其 allowlist、DNS/IP、大小和 content-type 校验边界。

#### 可复用经验

- 当持续学习跨多个项目时，应优先用 project-scoped observation 和稳定 project id，再以证据/置信度/跨项目门槛 promotion；边界是 remote-less path hash 不具备跨机器稳定性。
- 当 hook 是辅助观察而不是主业务副作用时，应优先 fail-open passthrough 原始输入并单独记录 warning；边界是安全 hard gate、配置保护和 secret 写入不能套用 fail-open。
- 当远程内容要进入 instinct/skill 生成流程时，应优先先验证 HTTPS、DNS/IP、大小、类型和 TTL，再解析内容；边界是 SSRF 防护不等于内容可信，仍需人工/治理审查。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/project-scoped-instinct/` 用 3 个本地 JSONL fixture 模拟两个项目各产生相同 workflow：验证 project id 不串、单项目不 promotion、两项目达到阈值才生成 candidate；再用一个 `staged=true` 和一个含 `$API_KEY` 的 fixture 验证不写 active fact、不持久化明文 secret。

#### 风险边界

- License：GitHub API 和仓库 `LICENSE` 为 MIT；仍需分别审查依赖 license，不能只看顶层字段。
- 安全：hook 解析 shell、MCP、配置和项目观察，拥有较大本地可见面；`hooks.json` 的 matcher/dispatcher 必须在 Hermes 侧重写，不能原样安装。观察数据会接触工具输入/输出，scrub 不是形式化保密保证。
- 维护活跃度：API `pushed_at` 和 `updated_at` 都在 2026-08-18；但 release 仍可能落后于 main，必须 pin release/commit 并运行 adapter tests。
- 不适用：ECC 的 Claude hook schema、`CLAUDE_PROJECT_DIR` 和 `~/.local/share/ecc-homunculus` 不能直接当 Hermes/shared hub 的路径真相源。

#### ⭐ Skill 升格判断

**需二次验证**。只候选化“project-scoped observations -> candidate -> promotion gate”这一窄机制；shared 现有治理已经规定 raw/inbox、curated 严出和不自动写 active fact，必须先做去重与 fixture。不要直接把 ECC 的 continuous-learning-v2 全量复制到 `capabilities/skills/`。

#### ⭐ Hermes/shared hub 落地路径

- Hermes raw：把候选观察写 `inbox/hermes/daily/`，运行时索引/fixture 写 `runtime/hermes/github-learning-poc/project-scoped-instinct/`。
- project identity：复用 `scripts/resolve_shared_root.py` 解析 shared root；对 shared hub 使用显式 `agent=hermes` 和项目/任务 scope，不能使用 ECC 的 `CLAUDE_PROJECT_DIR` 作为唯一身份。
- promotion：候选先进入日报 `Candidate Facts/Skills`，经 `docs/shared-governance-standard.md` 的证据、评分、去重、脱敏、审查后，才可能写 `curated/memory/facts/` 或 `capabilities/skills/`。
- 审计接点：扩展 `scripts/github_learning_orchestrator.py` 的 artifact audit，只记录 score/issues/strengths；不由 hook 自动改 provider、model、cron 或 secret。
- OpenClaw 接点：当前运行时不存在，仅记录未来适配接口，不执行 OpenClaw 安装或配置。

### 项目 3. NousResearch/hermes-agent

#### 基本信息与证据

- 链接：https://github.com/NousResearch/hermes-agent
- API：Stars `232,530`，Forks `46,412`，主语言 `Python`，License `MIT`，`pushed_at=2026-08-18T23:27:35Z`，`updated_at=2026-08-18T23:31:10Z`，open issues `33,223`。
- 源码 commit：`210cdb0ed35d4f7ef0957182312baaaa9e19bfbc`，default branch `main`。
- README 证据：项目描述 closed learning loop、skills、FTS5 session search、cron、delegation、多 terminal backend、MCP 与 memory；同时列出 CLI `hermes model/tools/config/gateway` 和官方文档入口。
- Release/issue 证据：最近 release `v2026.8.18`（Hermes Agent `v0.20.4`），发布时间 `2026-08-18T07:26:46Z`；近期 issue/PR 示例为 `#89551` desktop、`#89550` TUI toolset resolution 和 `#89549` video generation，均于 2026-08-18 更新。

#### 一句话判断

这是今日最应直接反哺的项目：它把 bundle、memory provider、tool executor 等复杂运行时边界落在 host-owned Python 接口上，适合作为 Hermes/shared hub 的实现参照，但不能把当前源码假设成稳定公共 API。

#### 解决的问题

它替代把所有工具调用、记忆同步、技能加载和 session rotation 塞在一个主循环里的做法：工具执行被抽为 sequential/concurrent/segmented 模块，记忆通过 MemoryManager/provider contract 进入，bundle 通过 YAML 目录和 cache 注册。

#### 架构/实现与数据流

1. 用户/cron 输入进入 conversation loop，产生 model tool calls。
2. `agent/tool_executor.py` 解析参数、按 effect/安全边界切成 parallel 与 barrier segment，再执行并按 tool_call_id 写回消息；全批次最后做 budget 和 steer。
3. `agent/memory_manager.py` 以 provider 列表承接 prefetch/sync/session switch；memory tool 只有真实 committed write 才通知外部 provider，并保留 per-op metadata。
4. `agent/skill_bundles.py` 读取 `~/.hermes/skill-bundles/*.yaml`，按 mtime cache；调用 bundle 时重新检查 disabled skills、去重、missing，并生成带加载清单的 user message。
5. 工具结果会经过 session DB flush、预算、风险 metadata 和 UI projection；关键结果不只依赖 stdout。

#### repo tree 摘要

```text
NousResearch/hermes-agent/
├── agent/
│   ├── conversation_loop.py  # 一轮对话与状态推进
│   ├── tool_executor.py      # sequential/concurrent/segmented tool calls
│   ├── memory_manager.py     # provider bridge、session/memory lifecycle
│   └── skill_bundles.py      # YAML bundle scan/cache/invocation
├── tools/                    # terminal、approval、registry、memory tool
├── skills/                   # agentskills-compatible skill surface
├── gateway/ cron/            # messaging 与 scheduled automation
├── hermes_cli/ providers/    # CLI/config/provider adapters
├── tests/                    # Python/JS 单元与集成测试
├── pyproject.toml uv.lock    # Python constraints and pinned deps
└── LICENSE                   # MIT
```

#### 关键源码文件

- `agent/skill_bundles.py`：bundle YAML 解析、mtime cache、disabled/missing 处理、message assembly 和 file-level CRUD。
- `agent/memory_manager.py`：provider contract、session switch、memory write mirror、shutdown drain。
- `agent/tool_executor.py`：参数 fail-closed、concurrent timeout、tool result persistence、segmented execution。
- `agent/conversation_loop.py`：模型调用、压缩、tool dispatch、retry 与 turn finalization 的总编排。
- `pyproject.toml`：Python `>=3.11,<3.14`、核心 direct dependency exact pins 与安全注释。

#### ⭐ 源码精读

1. `_parse_tool_arguments(raw_arguments)`：只接受 JSON object；无效 JSON 或非 dict 不执行工具，而返回结构化错误。这是模型输出到副作用之间的第一道确定性边界。

```python
def _parse_tool_arguments(raw_arguments: Any) -> tuple[dict, Optional[str]]:
    """Parse model-emitted arguments without repairing or coercing them."""
    try:
        arguments = json.loads(raw_arguments)
    except (json.JSONDecodeError, TypeError):
        arguments = None
    if isinstance(arguments, dict):
        return arguments, None
    return {}, json.dumps({
        "error": "Invalid tool arguments",
        "message": "Tool arguments must be a valid JSON object; tool was not executed.",
    }, ensure_ascii=False)
```

2. `_memory_tool_result_succeeded(result)`：把字符串先 JSON parse，再要求 dict 中 `success is True` 且 `staged is not True`；否则拒绝通知外部 provider，避免 staged/failed write 污染共享记忆。

```python
@staticmethod
def _memory_tool_result_succeeded(result: Any) -> bool:
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except Exception:
            return False
    if not isinstance(result, dict):
        return False
    return result.get("success") is True and result.get("staged") is not True
```

3. `notify_memory_tool_write(tool_result, tool_args, build_metadata=None)`：只处理 `add/replace/remove`；支持单操作和 batch operations；每个 op 单独生成 metadata，并把 `old_text` 作为 provenance 保留。

```python
def notify_memory_tool_write(
    self, tool_result: Any, tool_args: Dict[str, Any], *,
    build_metadata: Optional[Callable[[], Dict[str, Any]]] = None,
) -> None:
    if not self._memory_tool_result_succeeded(tool_result):
        return
    operations = tool_args.get("operations")
    raw_operations = operations if isinstance(operations, list) and operations else [{
        "action": tool_args.get("action"),
        "content": tool_args.get("content"),
        "old_text": tool_args.get("old_text"),
    }]
    for op in raw_operations:
        action = str(op.get("action") or "") if isinstance(op, dict) else ""
        if action not in self._MIRRORED_MEMORY_ACTIONS:
            continue
        metadata = dict(build_metadata() if build_metadata else {})
        if op.get("old_text"):
            metadata["old_text"] = str(op["old_text"])
        self.on_memory_write(action, target, str(op.get("content") or ""), metadata=metadata)
```

4. `execute_tool_calls_segmented(...)`：把最大连续 parallel-safe calls 和 barrier calls 分段；每段以 `finalize=False` 执行，最后整个 batch 只做一次 budget enforcement 与 steer 注入，避免分段后重复预算/截断。

```python
def execute_tool_calls_segmented(agent, assistant_message, messages: list,
                                 effective_task_id: str, api_call_count: int = 0,
                                 segments=None) -> None:
    if segments is None:
        segments = _plan_tool_batch_segments(assistant_message.tool_calls,
                                             execution_cwd=_exec_cwd)
    for kind, calls in segments:
        segment_message = SimpleNamespace(tool_calls=list(calls))
        if kind == "parallel":
            execute_tool_calls_concurrent(agent, segment_message, messages,
                                          effective_task_id, api_call_count,
                                          finalize=False)
        else:
            execute_tool_calls_sequential(agent, segment_message, messages,
                                          effective_task_id, api_call_count,
                                          finalize=False)
    total_tools = len(assistant_message.tool_calls)
    if total_tools > 0:
        enforce_turn_budget(messages[-total_tools:], env=get_active_env(effective_task_id),
                             config=_budget_for_agent(agent))
        agent._apply_pending_steer_to_tool_results(messages, total_tools)
```

5. `on_session_switch(new_session_id, ..., rewound=False)`：只有 `rewound=True` 才把该 kwarg 传给 provider，避免普通 `/new`、`/resume`、压缩路径污染 provider 参数；session boundary 的 end -> switch 则提交到单一 FIFO background worker。

#### 依赖分析与供应链风险

- `pyproject.toml`：Python `>=3.11,<3.14`；核心 direct pins 包括 `openai==2.24.0`、`certifi==2026.5.20`、`python-dotenv==1.2.2`、`fire==0.7.1`、`httpx[socks]==0.28.1`、`rich==14.3.3`、`tenacity==9.1.4`、`pyyaml==6.0.3`、`ruamel.yaml==0.18.17`、`requests==2.33.0`、`jinja2==3.1.6`、`pydantic==2.13.4`、`prompt_toolkit==3.0.52`、`croniter==6.0.0`、`packaging==26.0`、`Markdown==3.10.2`、`PyJWT[crypto]==2.13.0`、`cryptography==50.0.0`。
- 供应链优势：核心 direct dependencies 强调 exact pin，并把 provider-specific 重依赖放入 extras/lazy install，降低每个 Hermes session 的 blast radius；有 `uv.lock`。
- 供应链风险：Hermes 支持大量 provider、gateway、voice、MCP 和 terminal backend；extras 仍会扩大安装面。exact pin 不能替代 hash/signature、镜像来源和 lockfile review；本次未执行完整 install 或供应链扫描。
- MIT license 来自 GitHub API 与仓库 `LICENSE`；上游代码可作实现参照，但不要把上游源码整段复制到 shared skill。

#### 可复用经验

- 当模型输出将触发工具或记忆副作用时，应优先在 host-owned chokepoint 做结构化解析、effect 检查和 committed gate；边界是工具本身仍需独立授权、参数和路径校验。
- 当同一轮工具调用既有可并行查询又有状态 barrier 时，应优先用 ordered segments，并在全 batch 末尾统一预算和终态处理；边界是并行安全性必须有逐工具 metadata，不能只按名字猜。
- 当外部记忆需要镜像内置写入时，应优先只镜像成功且非 staged 的 mutation，并保存 old_text、session/task/tool provenance；边界是 candidate/raw 仍不能绕过 shared governance 直接写 curated。
- 当 session rotation 与后台 memory extraction 同时发生时，应优先用单一 FIFO worker 串行 end -> switch，并设置 bounded shutdown drain；边界是 drain timeout 后必须显式记录 abandoned work。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/hermes-boundaries/` 写纯 Python fixture：测试 invalid JSON 不执行、`success=false`/`staged=true` 不镜像、batch operations 只处理三种 mutation、parallel/barrier/parallel 只在 barrier 前后分段；不连接真实 provider，不写 `~/.hermes` 或 curated。

#### 风险边界

- License：MIT；依赖与 extras 的许可证必须另审，不能因顶层 MIT 就自动兼容。
- 安全：工具执行涉及 shell、文件、网络、MCP、provider 和配置；`_parse_tool_arguments`、memory committed gate、segmented dispatch 只是部分边界，不能替代最终 tool policy 和 user approval。
- 维护活跃度：API `pushed_at` 与 `updated_at` 均为 2026-08-18；release `v2026.8.18` 与 issue/PR 同日活跃，但 open issues `33,223` 很多，升级应固定版本并跑目标测试。
- 不适用：不能从源码当前结构推断长期稳定插件 API；不能在无人值守 cron 中自动改模型/provider/auth/secret/cron；不能把 assistant prose 当用户事实。

#### ⭐ Skill 升格判断

**可直接迁移（仅限窄契约，非上游源码）**：`committed non-staged memory mirror`、`invalid tool args fail-closed`、`segmented execution finalization` 与现有 Hermes/shared hub 的 verification-first 方向高度一致，且可做离线 fixture。实际写 shared skill 仍需先与现有 `foundation/shared-memory-bridge`、`autonomous-learning/self-reflection-engine` 去重并通过治理审查。

#### ⭐ Hermes/shared hub 落地路径

- Hermes runtime POC：`runtime/hermes/github-learning-poc/hermes-boundaries/`，输入只用 synthetic fixtures。
- 若形成稳定能力，优先更新当前 Hermes 本地 skill 或共享 `capabilities/skills/foundation/verification-first-tool-boundaries/`，保留函数契约、状态、验证命令与 pitfalls，不复制上游实现。
- 共享记忆接点：所有原始日报和 candidate 写 `inbox/hermes/daily/`；只有人工/总控审查后的稳定事实进入 `curated/memory/facts/`，索引同步 `curated/memory/MEMORY.md`。
- 审计接点：把 orchestrator 的学习报告视为 raw artifact；`audit-only` 只更新 runtime status/feedback，不自动晋升 candidate。
- Hermes 本地接口可参考 `agent/skill_bundles.py`、`agent/memory_manager.py`、`agent/tool_executor.py`；不改动这些上游文件，也不改 Hermes profile 配置。
- OpenClaw 路径只保留未来 adapter 设计，当前不调用、不安装、不写配置。

## 经验沉淀

1. 当 Agent 工作流需要跨 harness 复用时，应优先拆成 skill contract、确定性 engine 和 host adapter，因为不同 harness 的 hook、路径和权限语义不等价；边界是先做逐 host fixture，再决定 shared。
2. 当持续学习跨多个 workspace 时，应优先用 immutable project/agent/task scope、raw inbox 和 candidate promotion gate，而不是把 observation 直接写 curated；边界是 scope identity 必须能解释来源且处理无 remote 的 fallback。
3. 当工具/记忆调用可能产生副作用时，应优先采用 fail-closed 参数解析、committed/non-staged gate、逐操作 provenance 和 exactly-once terminal 处理；边界是这些机制不能替代最终授权和人工 approval。
4. 当一轮任务混合并发查询与状态修改时，应优先按 effect metadata 建 ordered segments，并只在 whole batch 结束做 budget/steer/receipt；边界是 barrier 的识别必须由 host-owned registry 支持。
5. 当上游仓库 API 顶层 License 为 `NOASSERTION` 或依赖未审计时，应优先只抽象机制并标注待核验，不复制源码、安装包或品牌资产；边界是顶层许可证不等于完整依赖合规。

### 今日实验设计

- 名称：`runtime/hermes/github-learning-poc/2026-08-19-boundary-fixtures/`
- 30 分钟范围：invalid JSON、staged memory result、batch memory operations、parallel/barrier/parallel、重复 bootstrap 五类离线 fixture。
- 成功条件：每个 fixture 输出 `pass|blocked|failed`，有输入 hash、scope、预期 artifact 和 receipt；不能以空 findings 代替未执行。
- 安全边界：不连接 provider/MCP/browser/network，不改 `~/.hermes`、model、provider、auth、env、cron 或 secret，不写 curated active fact。

## 明日继续

1. 最小动作：创建上述离线 fixture 的目录和测试矩阵，先实现 5 个输入/输出样例，不安装任何上游项目。
2. 重点核验：shared 已有 `foundation/shared-memory-bridge`、verification-first 和 self-reflection skill 是否与今日候选重复。
3. 继续研究：选择一个带明确依赖/License 的本地模型或工具链项目，补做 release asset 与 lockfile 级供应链核验。
4. 完成条件：fixture 有真实运行输出，候选经过证据、去重、脱敏和 scope 审查后，才决定是否升格；仍不得自动改配置或 cron。

## 候选反哺

### Candidate Facts

- [ ] topic: project-scoped learning should remain raw until cross-project evidence and promotion threshold | evidence: ECC `observe.sh`/`instinct-cli.py`/`observer.md`，项目默认 scope=project、promotion 需 2+ projects 与 confidence threshold | 建议: create candidate only | 安全级别: medium
- [ ] topic: Hermes memory mirror must gate on committed non-staged success and preserve per-op provenance | evidence: Hermes commit `210cdb0...`, `agent/memory_manager.py:1105-1178` | 建议: create/update candidate after fixture | 安全级别: medium
- [ ] topic: ordered tool segments allow parallel-safe runs around barrier calls while finalizing budget once | evidence: Hermes commit `210cdb0...`, `agent/tool_executor.py:2698-2755` | 建议: create candidate and compare existing verification skill | 安全级别: medium
- [ ] topic: NOASSERTION top-level license is insufficient for copying or dependency compliance | evidence: GitHub API n8n `license=NOASSERTION`; daily quality standard requires license/security boundary | 建议: create candidate governance reminder | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: project-scoped-learning-candidate-gate | 可复用场景: Hermes GitHub learning、共享记忆候选、未来多 workspace 观察 | 是否建议 shared: yes, after fixture | 原因: 属于跨 agent 学习治理横切流程，但必须与现有 reflection/governance skills 去重
- [ ] 名称: committed-memory-mirror-contract | 可复用场景: built-in memory 到外部 provider/shared inbox 的安全镜像 | 是否建议 shared: yes, after interface review | 原因: Hermes/OpenClaw/future-agent 可能复用，但具体 adapter 和路径必须 host-owned
- [ ] 名称: ordered-effect-segment-executor | 可复用场景: 并发查询与写入混合的工具批次 | 是否建议 shared: no for now | 原因: 当前更像 Hermes runtime contract，跨 agent 复用前需要 effect registry 和适配器
- [ ] 名称: idempotent-skill-bootstrap | 可复用场景: 启动时注入共享 skills、避免重复 context | 是否建议 shared: yes, after harness fixtures | 原因: 跨 harness 横切，但不同 host 的 injection schema 不同

### Candidate Open Questions

- [ ] 问题: Hermes shared-memory-bridge 是否已经覆盖 committed/non-staged/provider provenance 门控？ | reason: gap/duplication | priority: high
- [ ] 问题: shared hub 的 project identity 是否应由 remote URL hash、workspace path、agent lane 还是复合 scope 组成？ | reason: adaptation | priority: high
- [ ] 问题: ECC 的 observer/scrub 逻辑在 Hermes cron 输入上是否会误把研究数据视为 secrets 或遗漏新凭据模式？ | reason: adaptation/security | priority: high
- [ ] 问题: n8n `NOASSERTION` 的实际 LICENSE 与主要依赖许可证是什么？ | reason: stale/gap | priority: medium
- [ ] 问题: Superpowers v6.3.0 Hermes plugin 与当前 Hermes v0.20.4 的 post-compaction/skill loading 行为是否完全兼容？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动安装 Superpowers、ECC 或其他 GitHub 项目，不自动写 `~/.hermes` 配置。
- 不自动改变 Hermes model、provider、auth、env、tools、skills、cron 或 gateway。
- 不把 candidate 直接写入 `curated/memory/` 或 `capabilities/skills/`；需要证据、去重、脱敏和总控/人工审查。
- 不复制 License 未明确、依赖未审计或 `NOASSERTION` 项目的源码、包、规则和品牌资产。
- 不把 assistant-authored prose 生成用户事实；不把 OpenClaw 不存在时的运行状态写成已验证。
- 不运行真实 provider/MCP/browser/外网实验，不发送消息；本任务交付由 cron 自动处理。

## 研究证据索引

- GitHub API metadata：`gh api repos/{owner}/{repo}`，查询时间 2026-08-19 07:31-07:35 +08:00。
- Trending-like discovery：`gh api search/repositories?q=stars:>50000&sort=stars&order=desc&per_page=20`；用于项目发现，不替代 repo metadata。
- Superpowers commit/tree/source：`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`，README、`skills/*/SKILL.md`、`.opencode/plugins/superpowers.js`、`hooks/session-start`、`package.json`。
- ECC commit/tree/source：`06c5e118c4d3e6c3b7f9445f973a2194c82de193`，README、`scripts/hooks/observe-runner.js`、`skills/continuous-learning-v2/*`、`hooks/hooks.json`、`package.json`。
- Hermes commit/tree/source：`210cdb0ed35d4f7ef0957182312baaaa9e19bfbc`，README、`agent/skill_bundles.py`、`agent/memory_manager.py`、`agent/tool_executor.py`、`pyproject.toml`。
- 不能由本次读取确认的内容统一标注为“待核验”，尤其是速览项目 n8n 的实际 license/依赖合规、上游完整测试结果以及未执行的真实 provider 行为。
