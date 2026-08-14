# 2026-08-14 GitHub 热门项目学习日报

> 执行器：Hermes。OpenClaw runtime 不存在；本次未调用、启动或模拟 OpenClaw。  
> 共享根：由 `python3 scripts/resolve_shared_root.py` 真实解析为当前 shared 根；本报告只写 Hermes inbox，未写 `curated/memory/`。  
> 研究窗口：2026-08-14 14:07–14:17（UTC+08:00）；GitHub API 查询通过 `gh api` 完成，Trending 页面通过 `curl` 保存。  
> 发现证据：`runtime/hermes/github-hot-project-learning/evidence/2026-08-14/trending.html`（真实抓取大小 647,345 bytes）及同目录 JSON。  
> 源码证据：`runtime/hermes/github-hot-project-learning/evidence/2026-08-14/`；Superpowers 的 API main commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`，pdf-inspector 的 API main commit `4bee4f993ba28bd6a3334fa55e699b318663fba3`。  
> 数据边界：Stars、更新时间、pushed 时间是查询时动态值；README benchmark、上游 release 中的测试数字均标为上游声明，未外推为本机通过。Cargo/Rust 不在本机 PATH，pdf-inspector 的本机编译测试因此为“待核验”。

## 今日结论

今天的主线是：**Agent 能力接入必须同时有“宿主确定性引导”和“输入/输出证据边界”：Superpowers 把技能注册、首轮 bootstrap、Hermes tool mapping 与工作流审查串起来；pdf-inspector 把 PDF 级判断拆为 per-page classification、confidence、OCR reason 和布局/Markdown 阶段。对 Hermes/shared hub 最值得反哺的不是复制上游代码，而是建立一个窄的、可验证的 `capability + source + stage + reason + coverage + terminal` 契约；缺工具链、缺权限或只完成部分阶段时必须明确 blocked/待核验，不能投影为成功。**

## 研究边界与证据摘要

- **真实发现**：`curl https://github.com/trending?since=daily` 成功保存页面；页面解析到当日热门候选，包括 `cathrynlavery/diagram-design`、`anthropics/skills`、`cactus-compute/needle`、`macro-inc/macro`、`NVIDIA-NeMo/Switchyard`、`Lightricks/LTX-2`、`infiniflow/ragflow` 等。Trending 页面本身只作为发现源，项目关键元数据再用 GitHub Repository API 核验。
- **深读对象**：`obra/superpowers`（Agent skills/workflow/plugin bootstrap）与 `firecrawl/pdf-inspector`（本地 PDF classification/extraction/routing）。两者均交叉核验了 README、源码和 release/issues 至少两类来源。
- **Superpowers 真实验证**：浅层 shell syntax check 通过；`hooks/session-start` 在 `COPILOT_CLI=1` 下真实输出可解析 JSON，`context_chars=3321`。未安装到当前 Hermes、未写 `~/.hermes`、未运行 Hermes live plugin test；上游仓库存在 19 项 Hermes 测试的 release/commit 说明，但本机未复制上游测试结果。
- **pdf-inspector 真实验证**：源码、Cargo/Python manifest、README、release v1.14.2、open issues 已读取；本机 `cargo test --manifest-path ... --lib` 返回 exit 127（`cargo: command not found`），所以 build/test/benchmark/runtime 行为均为**待核验**，不把上游 PR 的测试报告当成本机结果。
- **安全边界**：不安装未知 plugin，不执行一键 installer，不修改 Hermes/OpenClaw provider、模型、auth、env、cron、hooks 或 secret；不复制 license 不明项目源码；不把本日报候选直接晋升为 curated active fact。

## 项目速览

下表均来自本次 `gh api repos/{owner}/{repo}` 的真实 Repository API 响应，查询窗口约为 2026-08-14 14:07–14:17 +08:00。`NOASSERTION` 是 GitHub API 的仓库级 license 未识别，不等于“无许可证”。Stars 会随时间变化。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed（UTC） | 今日用途判断 |
|---|---:|---:|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 169,192 | 20,142 | Python | NOASSERTION | 2026-08-14T06:16:26Z / 2026-08-13T18:09:56Z | 高热 skills 集合；只作候选来源，不能把 stars 当授权 |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 88,140 | 10,363 | Go | Apache-2.0 | 2026-08-14T06:15:38Z / 2026-08-14T05:45:14Z | RAG/检索系统候选，今天不展开全栈安全面 |
| [3b1b/manim](https://github.com/3b1b/manim) | 90,981 | 7,541 | Python | MIT | 2026-08-14T06:16:28Z / 2026-08-11T14:41:19Z | 可视化工程成熟项目，与今日 Agent 接入主线较弱 |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 15,422 | 931 | HTML | MIT | 2026-08-14T06:16:48Z / 2026-08-14T02:34:14Z | Agent 生成图示的展示面候选，未深读 |
| [cactus-compute/needle](https://github.com/cactus-compute/needle) | 5,105 | 336 | Python | MIT | 2026-08-14T06:16:22Z / 2026-08-13T23:26:11Z | 本地检索候选，需单独核验索引/ACL边界 |
| [NVIDIA-NeMo/Switchyard](https://github.com/NVIDIA-NeMo/Switchyard) | 1,305 | 115 | Rust | Apache-2.0 | 2026-08-14T06:12:46Z / 2026-08-14T05:34:07Z | Rust/Agent infra 候选，热度新但证据面不足 |
| [Lightricks/LTX-2](https://github.com/Lightricks/LTX-2) | 8,963 | 1,412 | Python | NOASSERTION | 2026-08-14T05:49:06Z / 2026-08-12T08:29:34Z | 生成模型候选，license 待核验，禁止复制源码 |
| [obra/superpowers](https://github.com/obra/superpowers) | 271,867 | 24,312 | Shell | MIT | 2026-08-14T06:07:44Z / 2026-08-13T00:36:31Z | **深读：skills、plugin bootstrap、workflow gate、Hermes 适配** |
| [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) | 15,408 | 1,063 | Rust | MIT | 2026-08-14T06:07:14Z / 2026-08-13T21:23:18Z | **深读：per-page routing、OCR reason、单次加载、资源边界** |

### 候选筛选说明

- `obra/superpowers` 的 GitHub API 返回 license `MIT`，最新列出的 release 为 `v6.3.0`，发布于 2026-08-12T16:58:30Z；当前 main pushed 于 2026-08-13T00:36:31Z，不能把任意 HEAD 行为都等同于 release 制品。
- `firecrawl/pdf-inspector` 的 GitHub API 返回 license `MIT`，最新 release `v1.14.2` 发布于 2026-08-13T21:23:19Z；release body 声称由 source checkpoint `4bee4f9` 构建，并列出资源上限修复。这个 release 说明是上游声明，本机未构建制品。
- `anthropics/skills` 与 `Lightricks/LTX-2` 的仓库级 license 为 `NOASSERTION`，因此本日报只记录为候选，不复制其源码或将其作为 shared skill 来源。

## 深读项目

### 项目 1：obra/superpowers

- **URL**：https://github.com/obra/superpowers
- **Stars / Forks / Language / License（GitHub API）**：**271,867 / 24,312 / Shell / MIT**。
- **查询时 updated / pushed**：2026-08-14T06:07:44Z / 2026-08-13T00:36:31Z。
- **固定源码版本**：GitHub API `commits/main` 返回 `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`，commit message 为 `Release v6.3.0: Devin CLI and Hermes Agent support...`。
- **release / issues 证据**：`v6.3.0` release 真实存在；open issue #2146 讨论 TDD RED 可能因 missing export 而“假失败”，open PR #2148 讨论 named implementer idle 后的报告请求。两项都说明这不是只靠 README 的静态技能集合，而是持续通过行为评估修订 workflow。

#### 一句话判断：为什么值得学

值得学的不是把一堆 Markdown skills 复制到 Hermes，而是它把**首轮 bootstrap、原生 skill 注册、工作流分阶段、子 agent 复核和“不要把 exit/表面通过当成行为验证”**连接成一个宿主可执行的契约；其中 Hermes 适配是当前仓库的一等入口，但仍需在本机 Hermes 环境做安装与 live acceptance test。

#### 解决的问题：替代了什么旧做法

1. 替代“用户说要写代码，Agent 立即改文件”：先通过 `brainstorming` 形成可审阅的 spec，再进入 plan、TDD、implementation、review。
2. 替代“skill 文件放在磁盘就会生效”：`.hermes-plugin/__init__.py` 在注册时枚举 `skills/*/SKILL.md`，调用 `ctx.register_skill(name, Path(...))`，并通过 `pre_llm_call` 首轮返回 bootstrap context。
3. 替代“所有 harness 共用一套隐式工具名”：`using-superpowers/references/hermes-tools.md` 显式映射 `read_file/write_file/patch/terminal/search_files/delegate_task/skill_view` 等 Hermes 工具。
4. 替代“subagent 完成即可信”：`subagent-driven-development` 的契约是每个任务独立 implementer、task review、修复轮次和最终 whole-branch review；这是流程要求，不等于本次已运行那些 subagent。
5. 替代“测试 RED 只要变红就算验证”：open issue #2146 明确指出 missing import/export 可能让 RED 通过错误原因，应该验证断言确实能区分 buggy/correct behavior。

#### 架构 / 实现与数据流

```text
Hermes plugin loader
        │ register(ctx)
        ├── locate repo-clone or flattened skills/ tree
        ├── build using-superpowers bootstrap
        ├── register every skills/*/SKILL.md via native loader
        └── register pre_llm_call hook
                 │
                 ├── first turn only → {"context": bootstrap}
                 └── later turns → None

Hermes Agent turn
        │
        ▼
using-superpowers → brainstorming → writing-plans
        │                         │ approval gate
        ▼                         ▼
TDD / implementation → subagent-driven-development
        │                         │ task review / re-review
        ▼                         ▼
verification-before-completion → final review / durable artifact
```

关键实现点是：插件只在首轮注入 bootstrap，其他 skill 通过 Hermes 原生 loader 按需读取；因此“首轮上下文”与“长期 skill catalog”是两个不同的面。仓库 README 同时明确 Hermes 安装命令为 `hermes plugins install obra/superpowers --enable`，并提醒 Hermes 没有 post-compaction hook；这意味着长会话压缩后 bootstrap 可能丢失，fresh session 是上游给出的恢复方式。

#### Repo tree 摘要

```text
superpowers/
├── .hermes-plugin/
│   ├── __init__.py       # Hermes plugin register、skill loader、pre_llm_call
│   └── plugin.yaml       # name/version/description/provides_hooks
├── hooks/
│   ├── session-start     # 多 harness 启动注入与 JSON schema 分支
│   └── hooks*.json       # 平台 hook 声明
├── skills/
│   ├── using-superpowers # bootstrap、平台适配与 skill_view 约定
│   ├── brainstorming     # 需求澄清与设计批准
│   ├── writing-plans     # 可执行计划
│   ├── test-driven-development
│   ├── subagent-driven-development
│   ├── systematic-debugging
│   └── verification-before-completion 等
├── tests/                # 上游行为/平台测试；本次未从远端完整 clone 验证
├── docs/                 # porting/eval/workflow 文档
├── scripts/              # shell packaging、sync、lint 工具
├── package.json          # Pi/Node package metadata；无 dependencies 字段
└── README.md / RELEASE-NOTES.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `.hermes-plugin/__init__.py` | Hermes 入口 | `_skills_dir()` 支持 git-clone/flattened 两种布局；`register()` 注册技能与 `pre_llm_call` |
| `.hermes-plugin/plugin.yaml` | 插件 manifest | `name: superpowers`、`version: 6.3.0`、声明 `pre_llm_call` hook |
| `skills/using-superpowers/SKILL.md` | 行为入口 | 要求 skill 在任何 action/澄清前触发，并指向 Hermes tool mapping |
| `skills/subagent-driven-development/SKILL.md` | 多阶段执行 | implementer → task review → fix/re-review → final review，强调 ledger 与不无故停滞 |
| `hooks/session-start` | shell hook | 读取 bootstrap，按 Cursor/Claude/Copilot/unknown 平台输出不同 JSON 字段 |
| `skills/using-superpowers/references/hermes-tools.md` | Hermes 适配 | 将 skill 动词绑定到当前 Hermes 工具，而非假设通用工具名 |
| `README.md` / `RELEASE-NOTES.md` | 文档与版本证据 | Hermes 安装、compaction 限制、跨 harness 支持与 v6.3.0 变更 |

#### ⭐ 源码精读（固定 API main commit）

**代码块 1：跨安装布局定位 skills，找不到时 loud failure**  
来源：[`__init__.py#L8-L32`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.hermes-plugin/__init__.py#L8-L32)

```python
# .hermes-plugin/__init__.py

def _skills_dir() -> str:
    here = os.path.dirname(os.path.realpath(__file__))
    candidates = (
        os.path.realpath(os.path.join(here, "..", "skills")),
        os.path.realpath(os.path.join(here, "skills")),
    )
    for cand in candidates:
        if os.path.isfile(os.path.join(cand, "using-superpowers", "SKILL.md")):
            return cand
    raise RuntimeError(
        "superpowers plugin: cannot find the skills/ tree "
        f"(looked at {candidates}). Reinstall with "
        "`hermes plugins install obra/superpowers`."
    )
```

逻辑摘要：优先支持仓库 clone 布局，再支持 flattened plugin 布局；只要找不到 `using-superpowers/SKILL.md` 就抛错，不静默地启动一个没有 skills 的“半工作”插件。边界是路径检查证明文件存在，不证明 skill 内容安全、版本已 pin 或 Hermes runtime API 兼容。

**代码块 2：原生注册全部 skills，并把 bootstrap 限定为首轮 pre-LLM context**  
来源：[`__init__.py#L74-L105`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/.hermes-plugin/__init__.py#L74-L105)

```python
# .hermes-plugin/__init__.py

def register(ctx):
    skills_dir = _skills_dir()
    bootstrap = _build_bootstrap(skills_dir)

    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, name, "SKILL.md")
        if os.path.isfile(skill_md):
            ctx.register_skill(name, Path(skill_md))

    def pre_llm_call(
        session_id=None, user_message=None, conversation_history=None,
        is_first_turn=None, model=None, platform=None, **kwargs
    ):
        if is_first_turn:
            return {"context": bootstrap}
        return None

    ctx.register_hook("pre_llm_call", pre_llm_call)
```

逻辑摘要：`register_skill` 接收 `pathlib.Path`；每个首轮只返回一次 context，后续返回 `None`。这把“skill catalog”与“首轮引导”分离，降低每轮重复注入，但也产生 compaction 后恢复问题。边界是这段代码依赖真实 Hermes plugin API；本次没有在当前 Hermes 中安装或 live 验证。

**代码块 3：shell 启动 hook 按平台选择 JSON context 字段**  
来源：[`hooks/session-start#L26-L47`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/hooks/session-start#L26-L47)

```bash
# hooks/session-start
using_superpowers_escaped=$(escape_for_json "$using_superpowers_content")
session_context="<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n...\n${using_superpowers_escaped}\n</EXTREMELY_IMPORTANT>"

if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
  printf '{\n  "additional_context": "%s"\n}\n' "$session_context"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -z "${COPILOT_CLI:-}" ]; then
  printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$session_context"
else
  printf '{\n  "additionalContext": "%s"\n}\n' "$session_context"
fi
```

逻辑摘要：先对换行、反斜杠和引号做 JSON escaping，再为 Cursor、Claude Code、Copilot/unknown 输出不同的字段形状。本机真实执行了 unknown/Copilot 分支并以 Python JSON parser 验证；没有声称 Cursor/Claude live harness 已通过。边界是 JSON escaping 不是权限控制，hook 进程仍会读取并注入整个 skill bootstrap。

#### 依赖分析与供应链风险

- 根 `package.json` 的 `dependencies`/`devDependencies` 均未声明；它的核心形态是 Markdown skills、Python plugin entry 和 shell hooks，而不是一个锁定的 Node runtime。
- 这不等于无供应链风险：Hermes plugin loader 会执行 `.hermes-plugin/__init__.py`，hook 会执行 shell 并读取仓库内容；安装整个仓库约 195 个 tracked files，写入面/启动面明显大于一个只读文档包。
- `README.md` 提供 `hermes plugins install obra/superpowers --enable`；在 Hermes/shared hub 中应先审核固定 commit、manifest、hook effect、skills 目录和版本，再决定是否安装。禁止无人值守执行上游 installer 或把第三方 skills 批量复制进 `capabilities/skills/`。
- MIT 只覆盖该仓库许可，不自动覆盖 Hermes 本体、插件 API、外部 harness、shell runtime 或用户从 skill 中触发的工具 effect；依赖/平台 license 仍需逐项核验。

#### README / docs / release / issues / source 交叉核验

- README 的核心 workflow（brainstorm → spec approval → plan → TDD → subagent-driven development）与 `skills/using-superpowers`、`skills/subagent-driven-development` 和 plugin registration 路径一致。
- README 的 Hermes 安装段落明确安装命令与“没有 post-compaction hook”的限制；`.hermes-plugin/__init__.py` 的首轮 `pre_llm_call` 实现解释了该限制的来源。
- `v6.3.0` release 与 API main commit 都包含 Hermes support，但 release commit 与未来 main 行为不能混同；本次使用 API main commit 作为源码引用锚点。
- open issue #2146 对 TDD RED 的 falsifiability 提出具体反例，说明 workflow 文本仍在演进；open PR #2148 的“idle implementer report”主题说明 subagent lifecycle 需要真实状态回收，不应只依据 child process exit。
- 本机只验证 hook shell syntax 与 JSON 输出；没有验证 Hermes plugin registration、native `skill_view` catalog、真实首轮 context 或 post-compaction 恢复。

#### 可复用经验

- 当 Agent 依赖一组可插拔 skills 时，应优先把 **loader、路径布局、版本、required capability 与 missing-state** 做成宿主可验证契约，因为“文件在磁盘”不等于“模型能调用”；边界是 loader 检查仍需行为 acceptance test。
- 当 workflow 需要在首轮注入较大 bootstrap 时，应优先将首轮 context 与按需 skill retrieval 分离，并为 compaction/新 session 设计恢复路径；边界是 bootstrap 仍会消耗首轮上下文预算。
- 当多个 harness 共享同一行为契约时，应优先维护 agent-neutral core、逐 harness adapter 和真实 schema fixture，而不是复制一份看似相同的工具映射；边界是每个 harness 仍可能有不同的 hook timing/permission semantics。
- 当 TDD 的 RED 可能由 import/export、编译或拼写错误触发时，应优先要求断言对错误行为产生可见差异，再修复并复跑；边界是行为测试也不能替代完整集成覆盖。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/superpowers-bootstrap-contract/` 做不安装插件的离线 fixture：

1. 用临时目录构造 git-clone 与 flattened 两种 `skills/using-superpowers/SKILL.md` 布局。
2. mock `ctx.register_skill` 与 `ctx.register_hook`，验证每个 `SKILL.md` 都被注册为 `Path`，缺文件时返回明确 blocked/failure。
3. 对 `is_first_turn=True/False` 验证 context exactly-once；对 shell hook 的三种环境变量组合验证 JSON schema。
4. 记录 `bootstrap_bytes`、registered skill names、hook schema、test status；不调用真实 Hermes、不写 `.hermes` 配置。

#### 风险边界

- **License**：仓库 API license 为 MIT；外部 harness、Hermes plugin API 与依赖环境不随 MIT 自动授权。
- **维护活跃度**：查询时 pushed 为 2026-08-13T00:36:31Z，最新 release 为 v6.3.0；活跃也意味着 contract 变化快，必须固定 commit/ref。
- **安全风险**：插件入口与 shell hooks 是执行面；skill 文本是行为面，可能诱导调用 `terminal`、写文件、创建 subagent 或修改 workflow。安装/启用不能等同于只读导入。
- **维护/一致性风险**：README、release 与 main 可能不同步；Hermes no post-compaction hook 是已披露限制；`skill_view`、`register_skill` 的 API 兼容性需本机验证。
- **供应链风险**：根 package 没有 Node dependencies 不能证明 shell/Python/plugin source 无风险；还需审查 commit provenance、hooks、skills、安装器和平台分发渠道。
- **不适用场景**：只想读取单个方法、没有人审阅的 unattended install、需要强租户隔离的高权工具链、或没有完整 plugin API/acceptance test 的 harness。
- **不能自动执行**：不运行 `hermes plugins install`，不启用第三方 plugin，不把上游 skill 复制进 shared，不修改 provider/auth/env/cron/hooks。

#### ⭐ Skill 升格判断

**需二次验证**，不是“可直接迁移”。

- **可直接抽象的窄机制**：`plugin-capability-preflight`（required skill names、loader registration、hook schema、version/ref、first-turn budget）可作为 runtime POC 候选。
- **需二次验证**：先完成上面的 offline fixture，再在隔离 Hermes profile 中做真实 native registration、首轮 trigger、compaction/restart 与 permission/effect review。
- **暂不沉淀**：不复制 Superpowers 全部 skills、hooks、installer、subagent workflow 文案；当前 shared hub 已有 foundation/shared-memory-bridge、verification-first 与多 agent 编排能力，整包引入会造成行为漂移和重复控制面。
- **升格结论**：如果 fixture 和隔离 profile 通过，优先**更新现有 research/GitHub-learning shared skill 的 capability/evidence contract**，而不是新建一个同名 workflow skill；今日不创建 shared skill，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **Hermes 本地验证面**：在隔离 profile 的 plugin staging 目录检验 `plugin.yaml`、`__init__.py`、hooks 与固定 commit；仅在人工批准后才考虑 `~/.hermes/plugins/` 的实际安装，当前不执行。
2. **shared 能力面**：若 POC 通过，候选契约写入现有共享研究能力的 `SKILL.md`/references：要求 `required_capabilities`、`loader_state`、`source_ref`、`bootstrap_bytes`、`hook_schema`、`terminal`；具体上游源码仍留 runtime evidence。
3. **研究编排面**：在 `scripts/github_learning_orchestrator.py` 的未来 audit contract 中增加“研究使用了哪些真实工具/依赖/是否 blocked”的 receipt，而不是通过报告关键字推断。
4. **共享分层**：原始 clone/API/hook 输出留在 `runtime/hermes/github-hot-project-learning/evidence/`；当日报留 `inbox/hermes/daily/`；候选经评分、证据、去重、脱敏和治理审查后才可能进 `curated/memory/`。
5. **OpenClaw 边界**：OpenClaw runtime 不存在，不创建 adapter、不调用 OpenClaw；若未来接入，复用 agent-neutral contract，另做其 hook/skill loader conformance，不共享未经验证的本地 plugin 状态。

### 项目 2：firecrawl/pdf-inspector

- **URL**：https://github.com/firecrawl/pdf-inspector
- **Stars / Forks / Language / License（GitHub API）**：**15,408 / 1,063 / Rust / MIT**。
- **查询时 updated / pushed**：2026-08-14T06:07:14Z / 2026-08-13T21:23:18Z。
- **固定源码版本**：GitHub API `commits/main` 返回 `4bee4f993ba28bd6a3334fa55e699b318663fba3`，commit message 为 `chore(release): bump package versions to 1.14.2 (#382)`。
- **release / issues 证据**：release `v1.14.2` 于 2026-08-13T21:23:19Z 发布，body 列出 Form XObject、CID range、CMap、content stream、detector lookback、rect clustering 等资源上限；open PR #378 讨论 visual-order Hebrew，open PR #377 讨论重复 text-paint 去重及其测试声明。上游测试声明不等于本机测试。

#### 一句话判断：为什么值得学

值得学的是**单文档单次加载、detector → extractor → layout/Markdown 的阶段分离，以及每页 `needs_ocr + reason` 的路由输出**；这正好可抽象到 Agent ingestion/研究 evidence，但不能把 PDF 的启发式阈值直接当成 Hermes 的通用事实判断器。

#### 解决的问题：替代了什么旧做法

1. 替代所有 PDF 都直接走昂贵 OCR：先采样内容流，区分 TextBased/Scanned/ImageBased/Mixed，再给出每页 OCR 列表。
2. 替代 detect 和 extract 各自重复加载：`process_pdf_with_options` 加载一次 `Document`，把同一个对象交给后续 `process_document`。
3. 替代只输出一段 Markdown：`PdfProcessResult` 暴露 page count、confidence、layout、encoding issue、OCR reason；调用者可以按页切换 direct extraction/OCR。
4. 替代单一 text-operator 计数：detector 同时考虑 image dominance、unique/alphanumeric chars、vector text、Type3/font/CID signal、sample strategy。
5. 替代只在 happy path 约束 parser：v1.14.2 release 将 Form/CMap/content stream/rect clustering 资源上限列为修复目标，说明不可信 PDF 输入本身是安全边界。

#### 架构 / 实现与数据流

```text
PDF path/bytes
     │ validate + load once (password redacted in Debug)
     ▼
Document
     │ detector: sample/full/pages strategy
     ├── PdfType + pages_sampled + confidence
     ├── pages_needing_ocr + reason codes
     └── title / image / vector / encoding signals
              │
              ├── TextBased → text extraction
              ├── Mixed → per-page direct/OCR routing
              └── Scanned/ImageBased → OCR lane

TextItems + PdfRect/PdfLine + structure tree
              │
              ▼
layout / table / column analysis
              │
              ▼
position-aware Markdown projection
              │
              ▼
PdfProcessResult + layout/encoding/OCR receipt
```

默认 detector 使用 `ScanStrategy::Sample(8)`、每页至少 3 个 text operators（含图像页时 effective minimum 至少 10）和 0.6 text-page ratio；这是项目内部可调 heuristic，不是语义正确性证明。Markdown 层把 table/image 作为 positioned blocks，与 TextLine 按页面几何顺序合并；复杂布局、字体编码和 RTL 仍可能需要 OCR/人工核验。

#### Repo tree 摘要

```text
pdf-inspector/
├── src/lib.rs                 # public API、PdfOptions、single-load pipeline、result types
├── src/detector.rs            # PDF type、page sampling、image/vector/font/OCR reasons
├── src/extractor/
│   ├── content_stream.rs      # Tj/TJ/Td/Tm/q/Q 等操作状态机
│   ├── fonts.rs / layout.rs   # font/CMap、列检测、布局
│   └── mod.rs                 # extraction orchestrator
├── src/markdown/
│   ├── convert.rs             # TextLine + positioned block → Markdown
│   ├── analysis.rs / classify.rs
│   └── preprocess.rs / postprocess.rs
├── src/tables/                # rect/line/heuristic/structured table detection
├── src/tounicode.rs / external/bcmaps/ # CMap、CID、字体编码
├── src/types.rs               # TextItem、TextLine、PdfRect、LayoutComplexity
├── tests/fixtures/             # PDF fixture corpus and Rust integration tests
├── napi/ / wasm/ / python.rs   # Node, WebAssembly, Python surfaces
├── Cargo.toml / pyproject.toml # Rust + maturin package metadata
├── docs/                      # Python/Rust API、benchmarking/debugging/publishing
└── SECURITY.md / .github/     # security guidance and CI/publish workflows
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/lib.rs` | public API/pipeline | `PdfOptions`、password Debug redaction、`process_pdf_with_options` single-load、`classify_pdf_mem` |
| `src/detector.rs` | classification | ScanStrategy、sample pages、text/image/vector/font signals、per-page OCR reason |
| `src/process_mode.rs` | stage contract | DetectOnly、Analyze、Full 三种 pipeline mode |
| `src/extractor/content_stream.rs` | parser state machine | PDF text operators与矩阵/字体状态 |
| `src/extractor/layout.rs` | geometry | histogram/column/newspaper/tabular layout |
| `src/markdown/convert.rs` | projection | positioned table/image blocks、TextLine ordering、structure heading suppression |
| `src/types.rs` | typed result pieces | `TextItem`、`PdfLine`、`PdfRect`、`LayoutComplexity` |
| `Cargo.toml` / `pyproject.toml` | dependency/package truth | lopdf、pyo3 optional、Rust/Python package surfaces |

#### ⭐ 源码精读（固定 API main commit）

**代码块 1：PdfOptions 在 Debug 输出中主动隐藏 password，主流程只加载一次**  
来源：[`src/lib.rs#L176-L200`](https://github.com/firecrawl/pdf-inspector/blob/4bee4f993ba28bd6a3334fa55e699b318663fba3/src/lib.rs#L176-L200)、[`src/lib.rs#L280-L295`](https://github.com/firecrawl/pdf-inspector/blob/4bee4f993ba28bd6a3334fa55e699b318663fba3/src/lib.rs#L280-L295)

```rust
// src/lib.rs
impl std::fmt::Debug for PdfOptions {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PdfOptions")
            .field("mode", &self.mode)
            .field("detection", &self.detection)
            .field("markdown", &self.markdown)
            .field("page_filter", &self.page_filter)
            .field("password", &self.password.as_ref().map(|_| "[REDACTED]"))
            .finish()
    }
}

pub fn process_pdf_with_options<P: AsRef<Path>>(
    path: P,
    options: PdfOptions,
) -> Result<PdfProcessResult, PdfError> {
    let start = ProcessingTimer::start();
    validate_pdf_file(&path)?;
    let (doc, page_count) =
        load_document_from_path_with_password(&path, options.password.as_deref())?;
    process_document(doc, page_count, options, start)
}
```

逻辑摘要：配置对象的 Debug 实现不把 password 原文带入日志；处理入口先 validate，再一次 load，后续检测和提取共享 doc。边界是 password 仍会进入实际 parser，日志 redaction 不是 secret lifecycle；单次加载也不等于 parser 对恶意 PDF 的资源安全。

**代码块 2：默认 sampler 与图像页的更高 text-op 门槛**  
来源：[`src/detector.rs#L69-L88`](https://github.com/firecrawl/pdf-inspector/blob/4bee4f993ba28bd6a3334fa55e699b318663fba3/src/detector.rs#L69-L88)、[`src/detector.rs#L221-L248`](https://github.com/firecrawl/pdf-inspector/blob/4bee4f993ba28bd6a3334fa55e699b318663fba3/src/detector.rs#L221-L248)

```rust
// src/detector.rs
impl Default for DetectionConfig {
    fn default() -> Self {
        Self {
            strategy: ScanStrategy::Sample(8),
            min_text_ops_per_page: 3,
            text_page_ratio_threshold: 0.6,
        }
    }
}

let is_image_dominated = analysis.image_count > 10
    && analysis.image_count > analysis.text_operator_count * 3;
let effective_min_ops = if analysis.has_images || analysis.image_count > 0 {
    config.min_text_ops_per_page.max(10)
} else {
    config.min_text_ops_per_page
};
if analysis.text_operator_count >= effective_min_ops
    && !is_image_dominated
    && analysis.unique_text_chars >= 5
    && !analysis.has_vector_text
    && !analysis.has_only_type3_fonts
{
    pages_with_text += 1;
}
```

逻辑摘要：默认只均匀采样最多 8 页，带图片页面提高最低 text operator 门槛，并额外排除图像主导、vector text、Type3-only 等信号。边界是采样/阈值可能漏掉局部异常；必须把 strategy、阈值、sampled pages 和 reason 写入 receipt，不能只记 `TextBased=true`。

**代码块 3：Mixed 文档生成 per-page OCR 列表和机器可读 reason**  
来源：[`src/detector.rs#L379-L417`](https://github.com/firecrawl/pdf-inspector/blob/4bee4f993ba28bd6a3334fa55e699b318663fba3/src/detector.rs#L379-L417)

```rust
// src/detector.rs
let mut pages_needing_ocr = match pdf_type {
    PdfType::TextBased => Vec::new(),
    PdfType::Scanned | PdfType::ImageBased => (1..=total_pages).collect(),
    PdfType::Mixed => {
        let mut ocr_pages = Vec::new();
        for page_num in 1..=total_pages {
            let analysis = analysis_cache.get(&page_num)
                .cloned()
                .unwrap_or_else(|| analyze_page_content(doc, pages[&page_num]));
            let looks_like_scan = analysis.image_count <= 1
                && analysis.text_operator_count < 50
                && analysis.unique_alphanum_chars < 10;
            if (analysis.has_template_image && looks_like_scan)
                || analysis.has_vector_text
                || (analysis.text_operator_count < config.min_text_ops_per_page
                    && analysis.has_images)
            {
                ocr_pages.push(page_num);
            }
        }
        ocr_pages.sort();
        ocr_pages.dedup();
        ocr_pages
    }
};
```

逻辑摘要：Mixed 不把整个 PDF 送进一个 lane，而是逐页计算 OCR candidates；后续 `ocr_reasons_by_page` 以 `scanned/no_text/vector_text/suspected_garbled_text` 等 code 解释为什么。边界是 heuristic 误判仍可能发生，且本机没有 Cargo 来运行 fixture/regression；使用者必须保留原 PDF、版本、策略和 fallback outcome。

**代码块 4：内存分类 API 明确 1-index → 0-index 的 caller contract**  
来源：[`src/lib.rs#L376-L401`](https://github.com/firecrawl/pdf-inspector/blob/4bee4f993ba28bd6a3334fa55e699b318663fba3/src/lib.rs#L376-L401)

```rust
// src/lib.rs
pub fn classify_pdf_mem(buffer: &[u8]) -> Result<PdfClassification, PdfError> {
    validate_pdf_bytes(buffer)?;
    let (doc, page_count) = load_document_from_mem(buffer)?;
    let detection = detector::detect_from_document(
        &doc, page_count, &DetectionConfig::default()
    )?;
    Ok(PdfClassification {
        pdf_type: detection.pdf_type,
        page_count,
        // Convert from 1-indexed to 0-indexed for caller convenience
        pages_needing_ocr: detection.pages_needing_ocr.iter().map(|&p| p - 1).collect(),
        confidence: detection.confidence,
    })
}
```

逻辑摘要：库内部的 OCR reason/page 结构使用 1-indexed，而这个轻量 caller API 转成 0-indexed；这是一个必须写进 adapter contract 的边界，否则会把错误页送进 OCR。边界是此函数使用默认 DetectionConfig，若产品需要可控策略，应调用带 config 的 API 并把配置 hash 纳入 evidence。

#### 依赖分析与供应链风险

- `Cargo.toml` 核心依赖：`lopdf = 0.42.0`（native 开 rayon、WASM 使用 wasm_js）、`thiserror 2.0`、`log 0.4`、`regex 1.10`、`once_cell 1.19`、`unicode-normalization 0.1`、`ttf-parser 0.25`；native 还有 `rayon 1.10`、`env_logger 0.11`；可选 Python binding 为 `pyo3 0.25`。
- `pyproject.toml` 使用 `maturin>=1.0,<2.0`，Python package `pdf-inspector` 1.14.2，Python >=3.8，license text MIT；NAPI/WASM 另有独立 package surface。Rust crate manifest 的版本约束不等于本机已经解析出的完整 dependency graph。
- 供应链面包含 native Rust crate、bundled CMaps、Python wheel、Node native platform packages、WASM 与发布 workflow；不能因为核心 crate MIT/“single dependency on lopdf”的 README 描述就忽略 transitive/native release risks。
- Release v1.14.2 的 resource bounds 是积极安全信号，但本机没有 Rust toolchain，无法验证 bounds、fuzz、integration tests 或 benchmark。Dependabot 状态未作为“无漏洞”证据使用；当前研究没有成功获取一份完整 advisory 清单。

#### README / docs / release / issues / source 交叉核验

- README 的“detect scanned/text-based → position-aware extraction → Markdown、Python/Node/WASM bindings、single document load”与 `src/lib.rs`、`src/detector.rs`、`src/markdown/convert.rs` 的真实导出和结构吻合。
- README benchmark 声称在 200 PDFs 上跑出 `pdf-inspector 0.875 overall / 0.470s` 等结果；这是上游 benchmark 声明，本机未下载 corpus、未构建或复跑，不能作为今日验证结果。
- v1.14.2 release body 明确列出 crafted PDF 资源边界修复（Form XObject、CID `/W`、CMap、content-stream decode、detector lookback、rect clustering），与当前源码的 parser/detector/tables 分层一致；release asset 制品未下载验证。
- open PR #378 指出 visual-order Hebrew 可能在正文和表格中反转缺失，且提出“document-level decision、ambiguous input 不乱翻”的模型；这说明 RTL coverage 仍在演进，不能把 `is_rtl_char` 的存在当成完整正确性。
- open PR #377 的 body 声称 double-draw text dedup 测试通过，同时坦白该 branch 的完整 integration target 仍有 10 个 fixture/snapshot failures；本机没有 Rust，不能独立复现或替上游确认。

#### 可复用经验

- 当输入可能在不同处理 lane 之间分流时，应优先输出 per-unit `class + confidence + reason + fallback lane`，而不是整个输入一个布尔值；边界是阈值必须版本化，并保留原始输入与 replay fixture。
- 当解析/提取出现“非空但可能错误”的输出时，应优先把 encoding、coverage、garbage、stage 和 OCR/人工 fallback 状态分开记录；边界是保守 gate 会误杀，必须给出可恢复的原始输入。
- 当一个资源会经历 detect、extract、layout、projection 多阶段时，应优先只加载/读取一次并共享 typed intermediate result，同时为每个阶段写 outcome；边界是单次加载不等于每阶段成功。
- 当处理来自用户或网络的不可信 PDF/archive/repo 时，应优先在 parser 前后设置 resource budget、deadline、size cap 和依赖审计；边界是版本命中不自动证明漏洞可达，audit clean 也不证明未知漏洞不存在。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/reason-coded-ingestion-routing/` 做纯 Python fixture，不安装 Rust crate、不读取真实私有 PDF：

1. 定义 `InputUnit`、`StageResult`、`RoutingDecision`：字段含 `input_hash/source_ref/stage/class/confidence/reasons/coverage/fallback/terminal`。
2. 构造 `text`、`mixed`、`scanned`、`garbled`、`blocked-toolchain` 五个 synthetic fixture。
3. 验证 mixed 只能把有 reason 的 unit 路由到 OCR/人工 lane；`unknown/blocked/partial` 不得被汇总为 completed。
4. 验证 1-index/0-index adapter、重复处理 hash、budget exceed 与 missing dependency 都有显式输出。
5. 将结果写 runtime evidence，不写 curated，不调用 OCR/provider，不修改 Hermes/OpenClaw 配置。

#### 风险边界

- **License**：GitHub API 与 `Cargo.toml`/`pyproject.toml` 均为 MIT；bundled CMaps、lopdf/transitive crates、Python/Node/WASM 发布物与调用方 license 仍需逐项审查。
- **维护活跃度**：查询时 pushed 为 2026-08-13T21:23:18Z，最新 release v1.14.2 在 2026-08-13 发布；高频修复说明活跃，但也意味着 parser contract 漂移快，必须 pin source/release。
- **安全风险**：PDF 是复杂、可构造输入；Form/CMap/content stream/rect expansion 可能造成 CPU/内存压力。不能把 parser 放进高权、无 deadline 的工具调用；密码只在 Debug 中 redacted 不代表输入可安全长期保存。
- **正确性风险**：OCR reason 和 classification 是启发式；RTL、vector text、Type3/CID、tables、multi-column、reading order 仍有 open PR/回归面；confidence 不是事实正确率。
- **供应链风险**：Rust native dependency、Python maturin wheel、NAPI platform packages、WASM/CMaps 与发布 workflow 扩大供应链；本机没有 Cargo，当前未完成编译/测试/审计。
- **维护/验证边界**：本机 `cargo test --lib` 为 exit 127；上游 README/release/PR 的测试和 benchmark均不能代替当前环境结果，所有 build/test/benchmark/runtime 结论标为待核验。
- **不适用场景**：需要 OCR/视觉模型理解扫描页、需要编译器级文档语义正确性、处理超大/恶意 PDF 而没有沙箱和预算、或将 non-empty Markdown 直接当 trusted evidence。
- **不能自动执行**：不下载/执行第三方 PDF、不开启云 OCR、不给 Hermes 工具增加 parser effect、不修改 provider/auth/env/cron，不把 parser 输出直接写 curated fact。

#### ⭐ Skill 升格判断

**需二次验证**，只抽象机制，不迁移 parser。

- **可迁移候选**：`reason-coded-ingestion-routing`，定义 per-unit result、stage、confidence、reason、coverage、fallback 与 terminal。
- **需二次验证**：先用 synthetic fixture 验证 mixed/partial/unknown/blocked 语义，再用公开、无敏感的 PDF fixtures 在具备 Cargo 的隔离环境做 differential check；比较 canonical output、reason、page index、artifact hash。
- **暂不沉淀**：不复制 `src/`、启发式阈值、CMap、parser、NAPI/WASM packaging，不把 README benchmark 写入 curated。
- **升格结论**：如果 POC 通过，优先更新现有 `capabilities/skills/research/github-hot-project-learning/` 或 verification/evidence contract；当前不创建新 shared skill、不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/reason-coded-ingestion-routing/{schema.json,fixtures/,validate.py,test_contract.py,README.md}`；只处理 synthetic input 和上游 evidence metadata。
2. **Hermes research adapter**：未来在 GitHub learning report 的 evidence sidecar 增加 `source_ref/source_hash/stage/items_attempted/items_read/failures/coverage/fallback/terminal`；不改现有 `read_file/search_files` 的权限。
3. **shared skill**：若 fixture 通过，修改现有 research skill 的输出契约，要求“工具链缺失=blocked、部分读取=partial、未复现 benchmark=unverified”，而不是引入第二套 ingest skill。
4. **知识库分层**：PDF/parser 原始源码与测试错误留在 `runtime/hermes/`；研究正文写 `inbox/hermes/daily/`；稳定的 agent-neutral routing invariant 只能作为 candidate，经过治理后才进入 `curated/memory/facts/`。
5. **OpenClaw 边界**：OpenClaw runtime 仍不存在；不写 OpenClaw workspace，不创建 adapter。未来若复用，只共享 schema/fixture，不共享本机 native dependency 或缓存。

## 经验沉淀

- 当 Agent 依赖外部 plugin/skill loader 时，应优先验证 `required capability → actual loader registration → first-turn behavior → post-compaction/restart recovery` 的完整链路，因为存在文件、存在 manifest 和能被模型调用是三个不同状态；边界是行为测试不能替代人工审核第三方 effect。
- 当输入可进入 direct、fallback、OCR、人工或 blocked lane 时，应优先采用 per-unit `class + confidence + reason + coverage + terminal`，因为单一 success flag 会把 mixed/partial 错投为 completed；边界是 reason code 仍需版本化、去重和 replay fixture。
- 当 workflow 或 parser 的中间结果会被 Agent 继续消费时，应优先保留 `source_ref/source_hash/stage/config/version`，并把“上游声明、本机复现、待核验、工具链阻塞”分开；边界是 provenance 不是正确性证明。
- 当第三方仓库包含 hooks、plugin entry、shell、native binding 或自动 installer 时，应优先把它们视为 authority surface，先做 manifest/路径/effect/权限审计，再决定是否安装；边界是 license 合法不等于运行时安全。
- 当本机缺少 Cargo、provider、OCR 或其他 prerequisite 时，应优先输出 `blocked/待核验` 和真实 exit/error，而不是用 README、CI 或源码中存在 tests 代替实测；边界是 blocked 也应保留下一步最小复现命令。
- 当共享中台接收跨 agent 学习结果时，应优先 raw→candidate→治理→curated 分层，原始 clone/stdout/cache 留 runtime/inbox；边界是候选反哺不代表已落库，也不能携带明文 credential。

### 后续实验汇总

- `runtime/hermes/github-learning-poc/superpowers-bootstrap-contract/`：离线验证 plugin loader、skill registration、hook JSON、first-turn exactly-once。
- `runtime/hermes/github-learning-poc/reason-coded-ingestion-routing/`：离线验证 direct/OCR/manual/blocked 的 per-unit reason and terminal contract。
- 两个实验都不安装上游项目、不连接 provider/OCR/MCP、不扫描私有仓库、不改 config/provider/auth/env/cron、不写 curated active fact。

## 风险边界（跨项目）

1. **来源边界**：Stars/license/updated/pushed 只来自本次 GitHub Repository API；README benchmark、release test numbers、issue reproductions 分别标注为上游声明或待核验。
2. **安装边界**：没有执行 `hermes plugins install`，没有复制 Superpowers skills，没有安装 Rust/Python/Node package，没有改变当前 Hermes profile。
3. **权限边界**：不自动改模型、provider、auth、env、cron、hooks、secret；不把 skill 文案当用户事实，不从第三方 instruction 生成 curated memory。
4. **工具链边界**：Superpowers 只做了 shell/JSON 层验证；pdf-inspector 的 Cargo lane blocked。不能把“审计报告完成”误投影为“两个项目已成功运行”。
5. **数据边界**：不处理私有 PDF、不上传源码/文档、不启用 cloud embedding/OCR；证据仅来自公开 GitHub 与本地项目文件。
6. **长期记忆边界**：本日报是 Hermes inbox raw research；候选 facts/skills 需经评分、证据、去重、脱敏与总控/人工审查，今日不主动写 `curated/memory/`。

## 明日继续

**最小动作**：先在隔离的、具备 Hermes plugin API 的 profile 中跑一个 10 分钟 Superpowers bootstrap conformance，再在具备 Cargo 的隔离环境只跑 pdf-inspector 的 `cargo test --lib` 与 3 个公开 fixtures；两项均先保存 terminal/coverage/artifact receipt，再决定是否更新现有 research skill。

1. Superpowers：验证真实 `ctx.register_skill(Path)`、`pre_llm_call(is_first_turn)`、`skill_view` namespace、restart/compaction 恢复；若失败只记录 adapter gap，不安装替代 shim。
2. pdf-inspector：安装隔离 toolchain 后固定 `4bee4f9`，跑 `cargo test --lib`、`cargo clippy -- -D warnings` 和 detect/pdf2md 的窄 fixture；对 mixed/RTL/garbled 记录 expected vs actual，不跑不受控的全量生产 PDF。
3. 共同审计：将 `blocked/partial/unknown/completed` 加入 GitHub learning evidence contract，并为每个 external source 记录 attempted/result/items/evidence。
4. 继续候选：如果今天主线延展，优先深读 `cactus-compute/needle` 的检索/ACL边界或 `NVIDIA-NeMo/Switchyard` 的 Rust runtime；先核验 README、tree、release、issues 与 license，再决定深读对象。

## 候选反哺

### Candidate Facts

- [ ] topic: external agent skill/plugin 接入需要 loader registration、hook schema、required capability、source ref 与 first-turn/recovery receipt | evidence: `obra/superpowers/.hermes-plugin/__init__.py`、`plugin.yaml`、`hooks/session-start`、README Hermes 段落；固定 main `b36e0829c6d...` | 建议: create/update candidate only | 安全级别: medium
- [ ] topic: untrusted document ingestion 应输出 per-unit class/confidence/reason/fallback/coverage，而不是 document-level boolean | evidence: `firecrawl/pdf-inspector/src/detector.rs`、`src/lib.rs`、release v1.14.2 resource-bound notes；固定 main `4bee4f993ba...` | 建议: create/update candidate only | 安全级别: high
- [ ] topic: 2026-08-14 本机 pdf-inspector Rust verification blocked | evidence: real `cargo test --manifest-path ... --lib` exit 127, `cargo: command not found` | 建议: create candidate execution note, do not promote as project quality fact | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: `plugin-capability-preflight` | 可复用场景: Hermes/shared skill/plugin 引入前检查 manifest、loader、hook、版本/ref、effect、recovery | 是否建议 shared: yes, after fixture | 原因: Hermes/OpenClaw/future-agent 都可能引入跨 harness 能力，但要与现有 config-target-routing、verification-first 去重
- [ ] 名称: `reason-coded-ingestion-routing` | 可复用场景: GitHub evidence、PDF、文档或多阶段研究输入的 direct/fallback/manual/blocked 分流 | 是否建议 shared: yes, after fixture | 原因: 属于跨 agent 的 source/evidence/coverage 横切契约，不应复制 pdf-inspector parser
- [ ] 名称: `external-repo-study-evidence-receipt` | 可复用场景: 固定 commit、记录 API/README/release/issues/source、保存真实 toolchain exit 与审计结论 | 是否建议 shared: yes, likely update existing skill | 原因: 与每日 GitHub 学习和 verification-first 直接重合，优先更新现有 shared skill，不新建重叠 skill

### Candidate Open Questions

- [ ] 问题: 当前 Hermes 版本/插件 API 是否能在隔离 profile 真实注册 Superpowers 的 `pathlib.Path` skills 并触发 namespaced `skill_view`？ | reason: gap | priority: high
- [ ] 问题: Hermes 长会话 compaction 后是否有现行 bootstrap recovery 机制，还是必须 fresh session？ | reason: adaptation | priority: high
- [ ] 问题: pdf-inspector v1.14.2 的 resource bounds、mixed/RTL reason 和 release artifact 能否在具备 Cargo 的环境中复现？ | reason: gap | priority: high
- [ ] 问题: shared hub 的 evidence contract 应将 `blocked` 与 `unverified` 如何映射到现有 orchestrator status，才能避免 audit 关键字投机？ | reason: adaptation | priority: medium

### 不应自动落地

- 不运行 `hermes plugins install obra/superpowers --enable`，不写 `~/.hermes` 配置，不启用第三方 plugin。
- 不复制 Superpowers 全部 skills/hooks，不复制 pdf-inspector parser/CMap/native bindings，不把 `NOASSERTION` 项目作为 shared skill 来源。
- 不把上游 README benchmark、release body 测试数字或 open issue 的复现声明写成“本机已通过”。
- 不自动修改 provider/model/auth/env/cron/secret，不从 assistant-authored prose 生成用户事实。
- 不把 candidate facts/skills 写入 `curated/memory/`；本报告只作为 Hermes 二轮审计与后续治理输入。

## 报告与证据路径

- **Hermes inbox 报告**：`inbox/hermes/daily/2026-08-14-github-learning.md`
- **运行证据**：`runtime/hermes/github-hot-project-learning/evidence/2026-08-14/`
- **项目卡片**：`runtime/hermes/github-learning/projects/obra-superpowers.md`、`runtime/hermes/github-learning/projects/firecrawl-pdf-inspector.md`
- **经验追加**：`runtime/hermes/github-learning/lessons.md`
- **知识库 projection（audit 通过后由 orchestrator 复制）**：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-08-14-GitHub热门项目学习日报.md`
- **审计状态**：`runtime/hermes/github-hot-project-learning/status.json`
