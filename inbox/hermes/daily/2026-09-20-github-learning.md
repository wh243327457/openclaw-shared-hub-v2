---
type: case
status: archived
created: 2026-09-20
updated: 2026-09-20
domain: learning
tags: [github-learning, browser-agent, typed-action-space, design-ir, prompt-compilation, validation]
---

# 2026-09-20 GitHub 热门项目学习报告

> 执行者：Hermes；当前 OpenClaw runtime 不存在，本次未调用 OpenClaw。  
> 查询与验证时间：2026-09-20 07:31–07:51（UTC+08:00）。  
> 发现口径：GitHub Search API 查询 `created:>2026-08-20 sort:stars`；GitHub Repository / Commit / Checks / Issues / Releases API 核验动态元数据。Stars 是约 07:46 的快照，会继续变化。  
> 深读固定提交：`browser-use/jev-ultrafast@1231850a0bf1a0c0341fe408ef1668dbbfdfac46`；`lnkiai/m3e-canvas@dea74159d69b09fb6fc2e44ebebf5e62c043e1ce`。源码结论只绑定这些 revision。  
> 源码临时目录：`/tmp/github-learning-2026-09-20/`；未把 clone 写入 shared core。完整 raw 命令输出不晋升 curated。

## 今日结论

**今天的共同主线是：先把模糊意图编译成宿主拥有的窄类型中间表示，再允许执行或交付。Jev Ultrafast 用“动态 operation + compatible target heads + code-owned DOM identity”缩小浏览器 Agent 的动作空间；M3E Canvas 用 typed design document 把视觉草图编译成 prompt/share link。两者也共同暴露一个边界：shape-valid、model-DONE、share-link 可打开都不是语义/业务完成，必须继续做引用完整性、revision/effect 和权威结果验证。**

### 今日真实验证摘要

- `browser-use/jev-ultrafast`：锁定依赖后，受当前环境 `ALL_PROXY=socks5h://...` 且项目未声明 `httpx[socks]` 影响，首次 test collection 真实失败：缺 `socksio`。在临时 clone 的 `.venv` 额外安装 `socksio==1.0.0` 后，离线测试 **31 passed / 0 failed**；`ruff check .` 与 `uv build` 均 exit 0。此补包只是研究环境 workaround，没有改仓库 manifest，也说明“宿主代理环境”是未声明 prerequisite。
- Jev 生产依赖导出后执行 `pip-audit`：**No known vulnerabilities found**。这只覆盖已导出的 Python dependency/advisory，不覆盖 Browser Harness daemon、Chrome、TypeSafe 服务、模型端、未知漏洞或发布 provenance。
- Jev 最新 main checks 仅看到两个 CodeQL `Analyze` success；没有 release、没有 tag。issue #51、#55、#36 与 PR #39、#56 均仍 open，因此 Windows hidden-tab paint、预算契约、endpoint/key 配置和 about:blank race 尚不能写成已修复。
- `lnkiai/m3e-canvas`：`npm ci` 后 **22 test files / 722 tests passed**；`npm run typecheck`、`npm run build` 成功，静态导出 5 条 route；`npm audit --omit=dev` 为 **0 known vulnerabilities**。最新 main checks 的 deploy、typecheck/build 均 success。
- M3E Canvas 另跑一个临时、随后删除的回归 fixture：重复 frame/item ID 且 action 指向不存在 frame 的文档仍被 `isProject()` 接受，**1 passed**。这验证了当前 validator 是 shape checker，不是 referential-integrity checker；不能把 share/import 成功写成设计语义闭合。
- 两仓 GitHub API 公开 repository security advisories 都返回空数组；Jev Dependabot endpoint 因权限 403，M3E Dependabot 明确 disabled。公开 advisory 空和 audit 0 都不能外推为“无漏洞”。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) | 8,310 | 522 | Python | MIT | 2026-09-18T16:28:35Z | **深读：typed action-space 与 effect 前置验证** |
| [lnkiai/m3e-canvas](https://github.com/lnkiai/m3e-canvas) | 7,539 | 787 | TypeScript | MIT | 2026-09-16T10:57:11Z | **深读：design IR → prompt/share projection** |
| [sapientinc/PRAXIST](https://github.com/sapientinc/PRAXIST) | 6,186 | 682 | Python | **NOASSERTION** | 2026-09-18T07:48:40Z | 自主研究主题相关；license 未识别，今日不迁移源码 |
| [MengTo/threeui](https://github.com/MengTo/threeui) | 5,969 | 568 | HTML | MIT | 2026-09-03T05:36:26Z | UI component catalog，后续可观察 |
| [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter) | 5,927 | 449 | HTML | Unlicense | 2026-09-19T08:59:15Z | 内容型项目，不符合今日源码机制主线 |
| [rakanki911/DLSS5-Swapper](https://github.com/rakanki911/DLSS5-Swapper) | 5,926 | 316 | JavaScript | MIT | 2026-09-13T02:02:21Z | 高权游戏注入/替换工具，安全面较大 |
| [XiaoDuoYa/codex-with-chatgpt](https://github.com/XiaoDuoYa/codex-with-chatgpt) | 5,573 | 535 | TypeScript | MIT | 2026-09-13T03:22:46Z | 多模型 planning/execution 拆分，后续需身份与路由核验 |
| [bojieli/ai-infra-book](https://github.com/bojieli/ai-infra-book) | 4,514 | 319 | Python | Apache-2.0 | 2026-09-19T14:01:37Z | 系统书稿与计算工具，适合专题学习而非今日 runtime 深读 |

> 元数据均来自 GitHub API，不以 badge/README 数字为准。License 是 repository 根识别结果，不覆盖依赖、数据、模型、字体、网页内容、release asset 与商店制品。`pushed_at` 是任意 ref 更新时间，不必然等于 default branch commit 时间。速览项目除两个深读对象外只做发现与元数据筛选，不作安全/质量结论。

## 深读项目

### 1. browser-use/jev-ultrafast

- **一句话判断**：值得学的不是“7 秒跑完 Flights”这个单任务数字，而是它把开放式网页行为压成每轮动态生成的有限 operation/target 集合，并让 code-owned DOM identity、freshness guard 和执行器掌握最终 authority；但 model `DONE`、browser ACK 和单站 benchmark 仍不能证明业务完成或跨平台可靠。
- **解决的问题**：替代让模型自由生成 CSS/XPath/坐标/JavaScript、operation 与 target 串行多次调用、每次重读完整 accessibility tree、对 stale page 直接重放 mutation，以及把 Agent 自报 DONE 当完成证明的旧做法。
- **URL / API 快照**：https://github.com/browser-use/jev-ultrafast ；**Stars: 8,310 / Forks: 522 / Language: Python / License: MIT**；`created_at=2026-09-16T21:30:12Z`，`updated_at=2026-09-19T23:39:06Z`，`pushed_at=2026-09-18T16:28:35Z`，default branch `main`，API `open_issues_count=54`（含 PR）。
- **固定提交**：[`1231850a0bf1a0c0341fe408ef1668dbbfdfac46`](https://github.com/browser-use/jev-ultrafast/commit/1231850a0bf1a0c0341fe408ef1668dbbfdfac46)，committer time `2026-09-18T16:28:35Z`；该 commit 只改 README 的 Cloud waitlist，核心 runtime 来自此前提交。
- **Release / issue / checks**：releases API 与 tags API 均为空；main checks 看到 Python/JavaScript TypeScript 两个 CodeQL Analyze success。issue [#51](https://github.com/browser-use/jev-ultrafast/issues/51) 报告 Windows 后台 tab 菜单 paint 太慢导致 Flights BLOCKED；[#55](https://github.com/browser-use/jev-ultrafast/issues/55) 指出 60 actions / 120 decisions 预算缺文档与边界测试；[#36](https://github.com/browser-use/jev-ultrafast/issues/36) 指出缺 key 中途崩溃且默认 endpoint 与 `.env.example` 不一致。PR [#39](https://github.com/browser-use/jev-ultrafast/pull/39)、[#56](https://github.com/browser-use/jev-ultrafast/pull/56) 都 open，不能视为已进入 main。
- **来源交叉核验**：README、`docs/design.md`、`docs/performance.md`、固定源码、tests、pyproject/lock、GitHub repository/commit/checks/issues/releases API、本机离线 tests/lint/build/pip-audit。

#### 架构 / 实现与数据流

```text
natural-language goal
  -> Browser.observe()
      -> one Runtime.evaluate(snapshot.js)
          -> visible text + typed actions + code-owned node IDs + semantic marker/guards
  -> model.action_space()
      -> operation head: CLICK | TYPE_TEXT | SELECT | WAIT | DONE | BLOCKED
      -> per-operation compatible target heads
  -> one TypeSafe request for operation + speculative target heads
      -> validate probabilities / exact candidate IDs
      -> consume only selected operation's target head
  -> Agent.command("act")
      -> consume decision once
      -> recheck fingerprint / scoped semantic guard
      -> optional text helper returns exact {"text": ...}
      -> resolve current geometry + visibility + occlusion
      -> CDP input / select event
      -> log execution before post-action observation
  -> independent task-specific verification outside model DONE
```

核心机制是把 LLM 输出降权为“从 host-built finite set 中选择”。同一 DOM node 可同时支持 CLICK 与 TYPE_TEXT，但只有被选 operation 对应的 target head 能执行；selector、coordinate、shell、JS 都不由模型生成。执行前再检查 document/page key、目标附近语义、连接状态、可见性、disabled/readOnly、当前 geometry 与 hit-test。边界是它仍共享现有 Chrome profile，freshness 是启发式，CDP dispatch 后的业务效果没有统一 effect receipt。

#### repo tree 摘要

固定 commit 共 **40 tracked paths**：

```text
jev-ultrafast/
├── jev_ultrafast/
│   ├── agent.py          # run loop、预算、stale retry、terminal state
│   ├── model.py          # 动态 action-space、TypeSafe 请求、text helper
│   ├── browser.py        # Browser Harness/CDP、freshness、geometry、effect
│   ├── snapshot.js       # 原子 DOM 观察、node identity、guards
│   ├── questions.py      # operation/target/text helper 规则
│   ├── demo.py           # loopback inspector 服务
│   └── static/           # 本地 inspector UI
├── tests/test_agent.py   # 31 个离线 contract tests
├── examples/             # generic run + Flights 独立验证
├── scripts/              # smoke、local guards、record/render/measure
├── docs/                 # design、performance、measurement JSON、演示资产
├── pyproject.toml        # Python >=3.12，2 个 production direct deps
└── uv.lock               # 锁文件（48,798 bytes）
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `jev_ultrafast/model.py` | typed action-space 与 model adapter | 一 node 一 index；operation-specific target map；概率/choice 强校验；unused head 不可执行 |
| `jev_ultrafast/agent.py` | 状态机与预算 | decision 在 effect 前一次性消费；stale 后重观察；执行先记 history；60 action / 120 decision hard stop |
| `jev_ultrafast/browser.py` | effect chokepoint | scoped freshness、DOM ref、visibility/occlusion、current geometry、CDP input；select interruption 返回不确定错误 |
| `jev_ultrafast/snapshot.js` | 一次原子观察 | visible controls/text、actual node WeakMap/Map identity、semantic marker/guard |
| `jev_ultrafast/questions.py` | Agent policy contract | page text 声明为 untrusted；DONE 要可见 evidence；BLOCKED 表示无 supported progress |
| `examples/flights.py` | 外部 oracle | route/date/trip/results 等独立检查，不相信 model DONE |
| `tests/test_agent.py` | adverse contracts | invalid choice、stale consume、text cache identity、atomic observe、dropdown unknown、final verify |

#### ⭐ 源码精读

**代码块 1：`action_space()` 将一个观察节点投影为多个 operation-specific 候选集合。**

```python
def action_space(actions):
    elements, indices, targets, controls = [], {}, {}, {}
    operations = {"click": "CLICK", "fill": "TYPE_TEXT", "select": "SELECT"}
    for action in actions:
        kind = action["kind"]
        if kind not in operations:
            controls[action["id"].upper()] = action
            continue
        node = action["node"]
        if node not in indices:
            index = str(len(elements) + 1)
            indices[node] = index
            elements.append({"index": index, "label": action["label"].split(" → ")[0], "operations": []})
        operation = operations[kind]
        targets.setdefault(operation, {})[index] = action
    return elements, targets, controls
```

逻辑摘要：模型只能在观察后实时生成的 candidate set 中选；target head 按 operation 分区，CLICK 不可消费 TYPE_TEXT 候选。相比自由 selector/coordinate，这把 hallucinated action 拒绝在 deterministic adapter。边界：snapshot 漏掉 shadow root/frame/canvas/复杂 keyboard widget 时，可行操作根本不会进入集合；“有限集合安全”不等于“任务可完成”。

**代码块 2：`choose()` 一次请求 operation 与 speculative target heads，只验证并消费匹配 head。**

```python
def choose(state, goal, history):
    elements, targets, controls = action_space(state["actions"])
    questions = {"operation": {"type": "choice", "criteria": operations, ...}}
    for operation, candidates in targets.items():
        questions[operation.lower() + "_target"] = {
            "type": "choice",
            "criteria": {index: {...} for index, a in candidates.items()},
        }
    result = post_json("https://api.typesafe.ai/v1/systemone", key, body)
    operation_answer = validate_choice(result["answers"].get("operation", {}), operations)
    if operation in targets:
        target_answer = validate_choice(
            result["answers"].get(operation.lower() + "_target", {}), targets[operation]
        )
        choice = targets[operation][target_answer["choice"]]["id"]
```

逻辑摘要：operation 与各 target head共享同一 observed state，从而减少串行 network round trip；unused target head 即使无效也不能产生 action。`validate_choice()` 还要求 exact ID set、finite [0,1] probabilities、总和近 1、chosen 是最大项。边界：同一请求更快，但 token/input 仍可能很大；远端 TypeSafe 是外部依赖，其服务语义和完整成本未由本仓开源代码覆盖。

**代码块 3：`Agent.command("act")` 在任何 mutation/model text call 前消费 decision。**

```python
elif name == "act":
    decision, page = state["decision"], state["page"]
    if not decision or body.get("fingerprint") != page["fingerprint"]:
        raise ValueError("Observe and choose before acting")
    state["decision"] = None  # retry cannot double-click
    selected = decision["choice"]
    if selected in {"DONE", "BLOCKED"}:
        if not state["browser"].fresh(page):
            raise StalePage("Page changed since the decision. Choose again.")
    ...
    state["browser"].act(action, page, text=text)
    state["history"].append({...})  # before observing again
```

逻辑摘要：旧 decision 不能在异常后被再次提交；mutation 成功但 post-observe 因 navigation 失败时，history 仍保存 effect attempt，不会被错误擦除。边界：history 记录的是 dispatch/execution attempt，不是业务 postcondition；click ACK 丢失后的统一 `unknown` 状态仍未结构化。

**代码块 4：`browser_operation()` 在最终 input chokepoint 重验 code-owned node。**

```python
def browser_operation(request):
    if operation == "act":
        action = request["action"]
        target = evaluate("""(action => {
          const e=window.__jevFast?.nodes.get(action.node);
          if (!e?.isConnected || e.matches(':disabled') ||
              !e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return null;
          const r=e.getBoundingClientRect(), x=r.x+r.width/2, y=r.y+r.height/2;
          if (!e.contains(document.elementFromPoint(x,y))) return null;
          return {x,y};
        })(""" + json.dumps(action) + ")")
        if target is None:
            raise StalePage("Target changed or is covered. Observe again.")
```

逻辑摘要：执行器不信模型携带的 selector/coordinate，而从 snapshot 保存的 node identity 重新拿当前几何并 hit-test。select evaluation 被 navigation 中断时抛 `RuntimeError("...inspect before retrying")`，避免把可能已触发 change 的副作用当 retryable stale read。边界：click/input dispatch 后页面可能异步拒绝、弹出下载、导航或服务端失败，仍需 task-specific read-back。

#### 依赖分析与供应链风险

- `pyproject.toml` 生产 direct dependencies 只有 `browser-harness==0.1.13` 与 `httpx[http2]>=0.28,<1`；锁图还含 `cdp-use`、`fetch-use`、websockets、Pillow、HTTP/2 栈。`browser-harness` 被精确 pin，但网络、daemon、Chrome remote debugging 与 native/browser binary 不在单个 Python audit 的保证内。
- `uv.lock` 固定 48,798 bytes；`pip-audit` 对导出的 production Python graph返回 0 known findings。Dependabot API 403，公开 advisories 为空，不能证明未知漏洞为零。
- 首次测试在当前 SOCKS proxy 环境 collection 失败，因为 `httpx.Client(trust_env=True)` 自动读取 `ALL_PROXY=socks5h://...`，但项目没声明 socks extra。额外装 `socksio` 后 31 tests 通过；这说明 dependency graph 对代理环境有隐含分支，部署检查应显式探测 proxy scheme/prerequisite。
- 无 tag/release，main 只有 3 个 commit、contributors API 当前为 1；8k+ stars 与成熟度不能画等号。今日未下载/执行任何 release asset，也无 asset provenance 可核。

#### 可复用经验

- 当 Agent 要在网页或其他高权界面执行动作时，应优先由宿主从当前观察构造 typed finite action-space，并让模型只返回候选 ID，因为自由 selector/coordinate/JS 会把 hallucination 直接变成 effect；边界是观察器漏项会造成 capability false negative。
- 当一次调用想并行预测 operation 与 target 时，应优先隔离 target heads，并只验证/消费最终 operation 对应的 head，因为 speculative answer 不应获得副作用 authority；边界是请求大小、服务成本和 provider availability 仍需预算化。
- 当 effect 前后可能发生 navigation、stale 或 transport failure 时，应优先一次性消费 decision、在 chokepoint 重验 exact target，并把 post-dispatch unknown 与 pre-dispatch stale 分开，因为盲重试可能 double-click；边界是业务完成仍要独立 read-back。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/typed-action-envelope-v0/` 做纯 Python fixture：输入 `observation_revision`、`operation`、`target_candidates`、`selected_head`、`dispatch_phase`、`authoritative_readback`，输出 `rejected | stale | not_started | unknown | verified`。覆盖：(1) CLICK 不能消费 TYPE_TEXT target；(2) unknown ID 拒绝；(3) revision 变化 effect 前 stale；(4) dispatch 后 ACK 丢失为 unknown，禁止自动重试；(5) DONE 无独立 oracle 时只能 needs_verification。不连接浏览器/模型/provider。

#### 风险边界

- **License**：GitHub API、根 LICENSE、pyproject 均为 MIT；可抽象模式。Python dependencies、Chrome/Google 页面、Browser Harness、TypeSafe 服务、模型输出与用户数据需独立合规。
- **维护活跃度**：项目 09-16 创建，main 09-18 最新提交，09-19 有大量 open issue/PR；无 release/tag。快速增长不代表稳定 API、跨平台或供应链成熟。
- **安全风险**：existing Chrome profile、remote debugging、页面正文、输入字段、模型 API key、TypeSafe endpoint 和 local inspector 都是 authority/data surfaces；page text 虽在 prompt 声明 untrusted，但 prompt instruction 不是 hard sandbox。
- **配置风险**：固定源码中 `model.py` 默认 text endpoint 是 DeepSeek，`.env.example` 是 OpenRouter；issue #36 与 PR #39说明 half-config 可能把 key 指向错误 vendor。当前不能自动采用其默认配置。
- **局限性**：不完整 accessible-name 算法；不支持 shadow roots、frames、canvas、uploads、popup、新 tab、nested scrolling 与复杂 keyboard widgets；Windows background paint issue #51 open。
- **验证局限**：本机只跑 offline tests/lint/build/audit，未连接 TypeSafe/text model、未启动 Browser Harness/Chrome、未跑 Flights/Wikipedia live、未复验 Windows。README 的 7.073 s 与 25% 来自单任务 3 对 matched runs，不能外推通用 benchmark。

#### ⭐ Skill 升格判断

**需二次验证。** 不安装项目、不复制其 agent prompt，也不新增第二个 browser skill。typed candidate-set、selected-head isolation、single-consume decision 可作为现有 verification-first / effect-scope / completion receipt 的增量候选；先做 agent-neutral fixture，并与昨日 BrowserSkill 的 effect certainty 候选合并去重。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/typed-action-envelope-v0/`，只含 synthetic fixtures 与 JSON receipts。
2. Hermes tool adapter：在 browser/terminal/API adapter 中由 host 生成 `candidate_id + operation + target_revision + effect_class`；模型只能选择，不可覆写 target path/identity。
3. effect contract：统一 `decision_consumed_at`、`dispatch_state`、`effect_state`、`readback`；`unknown` 禁止 blind retry。
4. GitHub-learning audit：把“报告写了 DONE/通过”与 deterministic evidence/checker 拆开，沿用 requirements→evidence 思路。
5. 若 fixture 与真实 adapter conformance 通过，优先更新现有 shared verification/workflow skill；不自动改 Hermes/OpenClaw 配置、provider、cron 或 secret。

---

### 2. lnkiai/m3e-canvas

- **一句话判断**：值得学的是用一份可保存、可分享、可预览的 typed design document 作为 canonical IR，再确定性生成多语言 implementation prompt；它比“让模型直接写一大段 UI prose”更可编辑、可回滚、可投影，但当前 `isProject()` 只做浅 shape validation，重复 ID、dangling action target 与语义冲突仍能穿过 import/share gate。
- **解决的问题**：替代设计意图只存在截图/对话、AI coding prompt 与画布状态各自漂移、分享必须有后端账号、AI 直接改坐标/布局，以及多语言 prompt 分别手工维护的旧做法。
- **URL / API 快照**：https://github.com/lnkiai/m3e-canvas ；**Stars: 7,539 / Forks: 787 / Language: TypeScript / License: MIT**；`created_at=2026-09-02T04:36:34Z`，`updated_at=2026-09-19T23:38:16Z`，`pushed_at=2026-09-16T10:57:11Z`，default branch `main`，API `open_issues_count=9`（含 PR）。
- **固定提交**：[`dea74159d69b09fb6fc2e44ebebf5e62c043e1ce`](https://github.com/lnkiai/m3e-canvas/commit/dea74159d69b09fb6fc2e44ebebf5e62c043e1ce)，committer time `2026-09-16T10:56:58Z`；该提交改 prompt editor、screen panel、prompt marks 与相关 tests。
- **Release / issue / checks**：releases/tags 均为空；main 的 deploy、typecheck/build checks success。open issue [#441](https://github.com/lnkiai/m3e-canvas/issues/441) 报告 prompt 中 `rocket_launch` 被下游 AI 实装成相机，说明“设计 IR → prose prompt → coding model → platform asset”仍有语义漂移。issue #418 关于 JSON validation retry 已 closed，但关联 PR #413 `state=closed, merged_at=null`；当前固定 `lib/ai.ts` 也未含该 PR 描述的 continuation/retry，因此不能宣称该能力已进入 main。
- **来源交叉核验**：README、`public/agent.md`、SECURITY、固定源码、tests、package/lock、GitHub repository/commit/checks/issues/releases API、本机 tests/typecheck/build/audit 与自建 validator boundary fixture。

#### 架构 / 实现与数据流

```text
human canvas interactions OR AI draft OR imported project/share hash
  -> canonical Doc
      frames[] + groups[] + typed items + actions + theme + prompt options
  -> editor state + localStorage autosave + undo/draft-before
  -> multiple deterministic projections
      1) visual React canvas / tap preview
      2) buildPrompt(): multilingual implementation prose
      3) saveProject(): JSON file
      4) shareable() -> raw deflate -> base64url -> URL fragment
      5) PNG via html-to-image

optional AI helper
  -> fixed system/user prompt + whole-design context
  -> parse JSON object
  -> allowlisted string fields or isProject(document)
  -> human-visible draft with keep/undo
```

它的关键不是 UI 元件数量，而是 canonical IR 驱动多个 projection：同一个 Doc 生成画布、prompt、JSON、share hash 与 preview。share link 将 payload 放 URL fragment，因此静态服务器通常收不到 fragment；`shareable()` 先删除 local image data 与 AI rewrite history。边界是 fragment 仍会进入浏览器 history、截图、剪贴板、聊天/日志；import validator 未建立 max-size、unique ID、referential closure 和 semantic checker。

#### repo tree 摘要

固定 commit 共 **108 tracked paths**：

```text
m3e-canvas/
├── app/
│   ├── page.tsx             # client-only editor boot/skeleton
│   ├── Editor.tsx           # canonical editor state、autosave、import/share/AI draft
│   ├── layout.tsx / globals.css / manifest
├── components/              # canvas、part/frame/prompt/theme/layer/preview panels
├── lib/
│   ├── tokens.ts            # Doc/Frame/Group/Item 类型、M3 tokens 与几何
│   ├── project.ts           # JSON shape validation、save/read
│   ├── share.ts             # redaction、deflate/base64url、hash import
│   ├── prompt.ts            # 多语言 Doc -> implementation prompt compiler
│   ├── ai.ts                # BYOK provider adapters、JSON narrowing、AI draft/helper
│   ├── tidy.ts / rail.ts    # deterministic layout/constraint transforms
│   └── *.test.ts            # pure module/unit tests
├── public/agent.md           # Agent 生成设计文档的 wire spec
├── .github/workflows/        # read-only CI + GitHub Pages deploy
├── SECURITY.md / NOTICE      # 安全/第三方 attribution
├── package.json              # 5 production direct deps
└── package-lock.json         # lockfile v3，187 package entries
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `lib/project.ts` | import gate | 校验基础 shape、kind/variant/number/string；未校验唯一 ID、action target closure、size budget |
| `lib/share.ts` | portable projection | 去掉 note history/local image；deflate-raw + base64url 放 hash；decode 后复用 `isProject()` |
| `lib/prompt.ts` | prompt compiler | Doc/theme/layout/behavior/style/options 确定性生成 ja/en/zh/ko prompt；作者 note 进入 prose |
| `lib/ai.ts` | optional BYOK helper | HTTPS/local gate、provider-specific transport、JSON extraction、allowlisted strings、draft `isProject()` |
| `app/Editor.tsx` | canonical state owner | localStorage、share hash arrival、draft before/keep/undo、import、projection orchestration |
| `public/agent.md` | wire contract | JSON schema-like说明、parts/actions/navigation、link encoding；同时写了“不要 round-trip”边界 |
| `lib/share.test.ts` | share contract | Unicode round-trip、corruption rejection、local image/history removal、plain fallback |
| `.github/workflows/ci.yml` | verification | fork PR read-only permissions；npm ci/typecheck/test/build |

#### ⭐ 源码精读

**代码块 1：`isProject()` 是浅 shape checker，而不是完整 referential validator。**

```ts
export const isProject = (value: unknown): value is Doc =>
  isRecord(value) &&
  Array.isArray(value.groups) &&
  Array.isArray(value.frames) &&
  value.groups.every(validGroup) &&
  value.frames.every(validFrame) &&
  (value.platform === undefined || isPlatform(value.platform)) &&
  (value.promptOptions === undefined ||
    (Array.isArray(value.promptOptions) && value.promptOptions.every((o) => typeof o === "string")));
```

逻辑摘要：它能挡住非法 kind/variant、非数字坐标、空 group、坏 frame shape，但没有全局 symbol table。今日临时 fixture 已真实验证：两个 frame 使用同一 ID、两个 item 使用同一 ID、action 指向不存在 frame，`isProject()` 仍返回 true。边界：这不是代码执行漏洞结论；它是 semantic integrity gap，可能导致 preview/navigation/prompt 与用户意图不一致。

**代码块 2：`shareable()` 在生成 public projection 前做字段级 data minimization。**

```ts
export function shareable(doc: Doc): Doc {
  return {
    ...doc,
    frames: doc.frames.map(({ noteHistory: _h, ...f }) => f),
    groups: doc.groups.map((g) => ({
      ...g,
      items: g.items.map(({ src, noteHistory: _h, ...it }) =>
        src && /^https?:\/\//.test(src) ? { ...it, src } : it),
    })),
  };
}
```

逻辑摘要：分享不是直接序列化编辑态；AI rewrite history 与 data/blob/file/local path image source 被剥离，只保留 http(s) 图片地址和作者当前内容。tests 还验证 idempotence 与不复用原对象。边界：作者 note、labels、remote image URL 与整个设计仍在 link 中；公开 URL 是数据载体，不是 secret channel。

**代码块 3：`shareLink()` 与 `readShareHash()` 用无后端 fragment transport，但复用同一个窄 validator。**

```ts
export async function shareLink(doc: Doc, base: string): Promise<string> {
  const json = JSON.stringify(shareable(doc));
  if (typeof CompressionStream !== "undefined") {
    const packed = await pipe(new TextEncoder().encode(json), new CompressionStream("deflate-raw"));
    return `${base}#docz=${toBase64Url(packed)}`;
  }
  return `${base}#doc=${encodeURIComponent(json)}`;
}

export async function readShareHash(hash: string): Promise<Doc | null> {
  ...
  const value: unknown = JSON.parse(json);
  return isProject(value) ? value : null;
}
```

逻辑摘要：fragment 不随常规 HTTP request 发送到静态 server，能实现无账号/无数据库的 portable artifact；corrupt compressed input 不静默 fallback plain。边界：代码没有在 decode 前显式限制 compressed/decompressed bytes，`public/agent.md` 的“about 100 KB”只是 prose；untrusted oversized hash 的浏览器资源消耗待核验。

**代码块 4：`buildPrompt()` 从 canonical Doc 生成 deterministic projection，而非让 LLM重述画布。**

```ts
export function buildPrompt(doc: Doc, widths: Record<string, number>, onlyFrameId?: string, lang = getLang()): string {
  doc = { ...doc, groups: constrainModalRails(doc.groups) };
  const groups = doc.groups
    .filter((g) => !only || frameOfGroup(g, allFrames, widths)?.id === only.id)
    .flatMap((g) => explodeGroup(g, widths));
  ...
  frames.forEach((f) => {
    if (hasText(f.note)) lines.push(`${trimEnd(f.note!)}.`);
    lines.push(ph.screenHead(...));
    describeScreen(lines, byFrame.get(f.id) ?? [], frameRect(f), widths, lang);
  });
  for (const key of PROMPT_OPTIONS) if (chosen.includes(key)) lines.push(...);
  return lines.join("\n");
}
```

逻辑摘要：约束 rail、group、frame、theme、behavior、style 和交付选项后确定性生成 prompt，便于用户手改与测试。它体现“canonical typed IR → prose projection”，而不是“prose → 反解析 state”。边界：作者/模型 note 会原样进入下游 coding prompt；`rocket_launch` issue #441 证明 name-level intent 仍可能被下游模型错误映射为平台 asset。

**代码块 5：AI helper 只拿结构化结果的 allowlisted 字段，整份 draft 则通过 `isProject()`。**

```ts
function pickStrings(v: unknown, parts: Item[], max: number): Record<string, string> {
  const map = (v ?? {}) as Record<string, unknown>;
  const out: Record<string, string> = {};
  for (const it of parts) {
    const s = map[it.id];
    if (typeof s === "string" && s.trim()) out[it.id] = s.trim().slice(0, max);
  }
  return out;
}

export async function draftDesign(...): Promise<Doc> {
  const j = parseJsonObject(await complete(s, system, user, signal, 12000));
  if (!isProject(j)) throw new Error("json");
  return j;
}
```

逻辑摘要：behavior note 只能回填请求过的 item ID 且有长度上限；model 不直接触碰坐标的 helper 路径较窄。整份 draft 能写 Doc，但经 shape gate 后作为可 keep/undo draft 到达人类画布。边界：shape gate 的 referential gap 仍存在；AI key 与整份设计上下文直接发 provider，且 key 长期存在 localStorage。

#### 依赖分析与供应链风险

- production direct deps：Next 16.3.4、React/React DOM 19.2.8、motion 13.1.1、html-to-image 1.11.13；dev/build 面含 Tailwind、TypeScript 7、Vitest 5。lockfile v3 共 187 package entries，本机 `npm ls --depth=1` 解析成功；平台无关 optional package显示 unmet 属正常条件依赖，不等于安装失败。
- `npm audit --omit=dev` 返回 0 known vulnerabilities；Dependabot 明确 disabled，公开 advisories 空。CI action 使用 `actions/checkout@v7`、`setup-node@v7` 是 mutable major tag，不是 commit SHA pin。
- 静态站点无自有 backend/account，但 optional AI 直接从 browser 向 provider 发送 API key 与 generated whole-design description；`anthropic-dangerous-direct-browser-access: true` 明确启用浏览器直连。localStorage 不是 secret vault，同 origin XSS/恶意扩展/共享 browser profile 是风险面。
- README/NOTICE 声明 Loading shapes 和 Material Symbols 来源含 Apache-2.0；根项目 MIT 不自动覆盖字体、icons、remote image、AI provider terms 或用户设计内容。

#### 可复用经验

- 当同一对象需要 UI、JSON、share link、prompt 和 preview 多种视图时，应优先维护 typed canonical IR，再确定性生成 projections，因为从 prose/截图反解析 identity 与行为会漂移；边界是 canonical IR 自身必须版本化并做 semantic validation。
- 当要无后端分享富状态时，应优先先生成最小化 public projection，再把 payload 放 fragment 或文件，并明确 size/privacy 边界，因为“服务器通常收不到 hash”不等于链接内容保密；边界是 history、clipboard、chat 和浏览器扩展仍能看到。
- 当外部 Agent/模型生成结构化设计时，应优先同时做 shape、unique identity、referential closure、size budget 和 domain invariant 检查，因为 `isProject()==true` 只证明局部字段可解析；边界是 semantic checker 也不能证明下游实现视觉正确。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/referential-artifact-validator-v0/` 建 agent-neutral JSON checker：schema 为 `entities[] + edges[] + projections[]`；验证 unique IDs、edge targets exist、acyclic-required subset、compressed/decompressed size cap、public projection redaction。fixtures 包括 duplicate ID、dangling edge、oversized compressed payload、private history leak 与 valid round-trip。不安装 M3E Canvas，不处理真实用户设计。

#### 风险边界

- **License**：repository API 与根 LICENSE 为 MIT；NOTICE 列出 Apache-2.0 来源。依赖、字体、Material Symbols、图片、AI provider、用户内容需独立审计。
- **维护活跃度**：项目 09-02 创建，main 最新 commit 09-16；无 release/tag，contributors API 10。高 stars 与 722 tests 不代表 wire format 已稳定，`public/agent.md` 明确 beta。
- **安全风险**：share hash/imported JSON、remote image URLs、localStorage design/key、direct browser AI、HTML-to-image、external fonts 都是数据/资源面。当前未证明 XSS 或 SSRF；但 oversized decompression 与 semantic-invalid document 的处理待核验。
- **隐私风险**：share projection 会去 local images/history，但保留 design labels/notes/remote URLs；AI helper会发送 whole-design generated description 到选择的 provider。key 不进 prompt/export 不等于不会被 same-origin script/extension 读取。
- **局限性**：shape validator 不检查 ID 唯一与 action referential closure；prompt 是 lossy prose projection；下游 coding model 可能误解 icon/asset/behavior；mobile editor 是功能受限模式。
- **验证局限**：本机未用真实 browser 做 drag/tap/share UX E2E，未连接任何 AI provider，未测试跨浏览器 CompressionStream、超大/zip-bomb payload、remote image CORS、GitHub Pages真实部署或 Android output。issue #441 只证明 reporter 的下游实现错误，不证明所有模型都会复现。

#### ⭐ Skill 升格判断

**需二次验证。** 不复制 1,700+ 行 prompt compiler，不安装其 `public/agent.md` 为 skill。可迁移的是“canonical typed artifact → minimized public projection → deterministic human/Agent views → semantic validator”的 workflow；先与现有 shared-memory bridge、governance、verification-first、sealed artifact/evidence candidates 去重。

#### ⭐ Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/referential-artifact-validator-v0/`，纯 synthetic JSON fixtures。
2. GitHub-learning：未来把 API snapshot、source revision、tests、report path建成 canonical evidence manifest，再由它投影 Markdown/Obsidian；不要从报告 prose 反解析真相。
3. shared memory：candidate fact/skill promotion 先过 unique ID/source revision/referential closure/redaction checker；raw evidence仍留 inbox/runtime。
4. Hermes artifact sharing：输出 public projection 时显式 allowlist 字段与 byte budget；secret 永不进入 shared/hash。
5. 通过 POC/治理审查后优先更新现有 workflow/verification skill，不创建 `m3e-canvas` 专属 shared skill；不触碰 OpenClaw runtime。

## 经验沉淀

1. 当模型要驱动真实工具或生成可执行 artifact 时，应优先把模型限制在 host-owned typed IR / finite candidate set 中，因为自由 selector、坐标、路径和 prose 会把 hallucination扩散到 effect；边界是 IR builder 漏项和 schema 漏洞仍需独立验证。
2. 当一个 canonical object 需要生成 Markdown、prompt、URL、UI 或 audit view 时，应优先从 sealed typed state 做单向 projection，因为从 prose 反解析 identity、coverage 和 status 会漂移；边界是 projection 必须记录 source revision 与有损字段。
3. 当 validator 宣称 artifact valid 时，应优先区分 syntax、shape、referential closure、semantic invariant 与 business acceptance，因为 `isProject()`、model DONE、exit 0 和文件存在都只覆盖窄层；边界是最高层 acceptance 仍要权威 oracle。
4. 当 effect 可能在 timeout/navigation/transport failure 前后发生时，应优先一次性消费 decision，并用 `not_started | unknown | verified/rejected` 记录结果，因为把 post-dispatch unknown 当 stale 重试会重复副作用；边界是 read-back 要绑定 exact target/revision。
5. 当用 URL fragment 或本地存储实现“无后端”时，应优先做字段 allowlist、size budget、redaction 与 threat-path说明，因为 server 看不到 fragment 不代表 history、clipboard、extension、same-origin script 或接收方看不到。
6. 当宿主环境含 HTTP/SOCKS 代理时，应优先把 proxy scheme 对 optional dependencies 的影响纳入 prerequisite check，因为 Jev 在 current SOCKS env 中缺 `socksio` 会在 test collection 阶段失败；边界是临时补包不能代替项目 manifest 修复。
7. 当 repo 很新、stars 增长快但无 tag/release 时，应优先固定 commit、读 issues/PR 与本机执行 tests，而不是把热度当成熟度；边界是 unit/build 绿色仍不覆盖跨平台 browser E2E 和发布 provenance。

## 明日继续

1. 实现合并 POC `typed-referential-effect-envelope-v0`：candidate-set + reference closure + effect state，以 synthetic fixtures覆盖今日两个项目的共同边界。
2. 给 GitHub-learning evidence manifest 加 `source_revision / candidate_ids / references / checker / effect_state / projection_hash` 草案，先在 runtime，不改现有 orchestrator。
3. 追踪 Jev PR #39/#56 与 issue #51/#55 是否进入 main；若进入，固定新 commit 后只复验相关 tests，不把 PR 描述当事实。
4. 给 M3E Canvas validator 写不改上游的本地 differential fixture：shape-only vs semantic checker，并测试 byte budget；不加载真实用户设计。

## 候选反哺

### Candidate Facts

- [ ] topic: typed candidate-set 降低模型 effect authority | evidence: Jev `model.py::action_space/choose/validate_choice` + 31 offline tests | 建议: update verification/effect-scope fact | 安全级别: medium
- [ ] topic: shape-valid artifact 不等于 referentially valid | evidence: M3E `project.ts::isProject` + 今日 duplicate/dangling fixture 1 passed | 建议: create candidate, not active fact | 安全级别: low
- [ ] topic: canonical IR 应先最小化再生成 public projection | evidence: M3E `shareable/shareLink/buildPrompt` + share tests | 建议: update sealed artifact/governance pattern | 安全级别: medium
- [ ] topic: proxy scheme 可触发未声明 optional dependency | evidence: Jev 首次 collection 缺 socksio；临时补包后 31 passed | 建议: update prerequisite-check candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: typed-referential-effect-envelope | 可复用场景: browser/API tool selection、artifact graph、shared memory promotion | 是否建议 shared: yes（仅候选） | 原因: 跨 Hermes/future agent 可复用，但需先与 verification-first/effect-scope/completion receipt 去重并跑 fixtures
- [ ] 名称: public-projection-minimizer | 可复用场景: report/share link/evidence bundle/Obsidian projection | 是否建议 shared: yes（优先更新现有 workflow） | 原因: 规则稳定且横切，但应落在 deterministic script，不堆进大 SKILL.md

### Candidate Open Questions

- [ ] 问题: typed candidate-set 的最小跨工具 schema 如何同时表达 operation compatibility、target revision 与 effect class？ | reason: adaptation | priority: high
- [ ] 问题: artifact validator 的 referential closure/byte budget 应放在 producer、transport 还是 consumer，如何避免规则漂移？ | reason: adaptation | priority: high
- [ ] 问题: Jev PR #39/#56 是否会合并，Windows background paint issue #51 的跨平台修复是什么？ | reason: stale/gap | priority: medium
- [ ] 问题: URL fragment decompression 的安全 size cap 和浏览器兼容矩阵如何验证？ | reason: gap | priority: medium

### 不应自动落地

- 不自动安装或运行 Jev/M3E 产品，不连接 TypeSafe、text model、真实 Chrome profile、AI provider 或用户 API key。
- 不自动改 Hermes/OpenClaw 配置、model、provider、cron、skill 或 secret；当前 OpenClaw runtime 不存在且本次未调用。
- 不直接写 curated active fact、不创建 shared skill；本报告、runtime card 与 lessons 仍是候选/原始学习产物，需二轮治理、去重和人工审查。
- 不复制 MIT 源码或大段 prompt compiler进入 shared；只抽象机制。更不复制 license 为 NOASSERTION 的速览项目源码。
- 不把 0 audit findings、公开 advisory 空、CI success、unit tests通过、share link可解析、model DONE 或 stars 数量外推成完整安全/可靠/成熟证明。
