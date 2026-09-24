---
type: case
status: archived
created: 2026-09-24
updated: 2026-09-24
domain: learning
tags: [github-learning, system-one, decision-routing, context-compaction, agent-context]
---

# 2026-09-24 GitHub 热门项目学习报告

> 执行者：Hermes；本次未调用 OpenClaw。  
> 查询与验证时间：2026-09-24 07:31–07:53（UTC+08:00）。发现口径为 GitHub Search API `created:>=2026-08-24 stars:>20 sort:stars`；Stars 是查询时快照，会继续变化。  
> 深读固定提交：`NandhaKishorM/laya@1e28ac20c0896b1c37a744cd11f740eb98f8b178`（tag/release `v0.3.11`）；`tamaratran/fast-jev-compaction@e3f262a7f4d42bd8dd32ced30d26176f7cb545b0`。源码结论只绑定这些 revision。  
> 证据来源：GitHub Repository/Search/Commit/Release/Tags/Issues/Actions/Security Advisories API，README、docs、manifests、lockfile、tests 与关键源码；clone/evidence 位于 `runtime/hermes/github-learning/evidence/2026-09-24/`。

## 今日结论

**Agent 上下文治理不应继续依赖“让大模型生成一段摘要”：高频、结构化判断可下沉到有界 typed decision plane，历史压缩则应使用“固定保留区 + call/result 分级 + 完整性不变量 + fallback”；但模型置信度、token 估算和宿主恢复语义都必须经真实 corpus 与生命周期验证，不能把快速概率直接当删除授权。**

### 今日真实验证摘要

- `NandhaKishorM/laya`：固定 `v0.3.11` commit 的 GitHub CI、Docker、Security workflows 均为 success；本机 `compileall` 成功，纯路由 smoke 正确区分英文/阿拉伯文/default，`tests/test_lang_guess.py` 为 **52 passed / 0 failed**。pytest collection 因当前 Python 环境缺 `torch` 失败，模型 forward、完整 tests、README latency/accuracy 均未在本机复现。
- Laya release `v0.3.11` 于 2026-09-23 发布，包含 routed batch、prediction hooks、server request limits 与 timing-safe auth。issue #285 明确指出 README/BENCHMARKS 数字可能随推理路径和 checkpoint 变化而漂移，release 前自动刷新尚未闭环；issue #290 表明 LangChain 的“只取最新 user message”与“完整会话”契约仍待明确。
- `tamaratran/fast-jev-compaction`：`npm ci`、typecheck、build 全部成功；Vitest **2 files / 29 tests passed / 0 failed**。`npm audit --omit=dev` 为 0 findings；完整 dev graph 为 **5 findings（3 moderate / 1 high / 1 critical）**，均落在 Vitest/Vite/esbuild 测试工具链，仍应升级并复验。
- fast-jev-compaction 没有 GitHub tag/release/Actions run；package manifest 为 `0.2.0`，plugin manifest 为 `0.3.0`，发布身份存在双版本。开放 issue #89 给出 `--resume` 后压缩效果丢失的真实上游测量，issue #97 给出包含 shell/SQL/path 文本时被 Cloudflare WAF 返回 HTML 403 的复现；本次未调用 TypeSafe API，线上行为只标为“上游 issue 已核验，当前环境待复现”。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | 20,354 | 1,727 | Python | Apache-2.0 | 2026-09-23T18:05:00Z | **深读：本地 typed System-1 decision plane** |
| [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter) | 13,005 | 877 | HTML | Unlicense | 2026-09-23T00:23:40Z | 循证内容型项目，不进入今日 Agent 主线 |
| [lnkiai/m3e-canvas](https://github.com/lnkiai/m3e-canvas) | 8,083 | 846 | TypeScript | MIT | 2026-09-22T03:07:57Z | 已于 09-20 深读，不重复 |
| [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) | 6,565 | 380 | TypeScript | MIT | 2026-09-18T04:45:31Z | **深读：verbatim tool-history pruning** |
| [zai-org/ZCode](https://github.com/zai-org/ZCode) | 6,531 | 1,935 | TypeScript | Apache-2.0 | 2026-09-23T13:25:04Z | 新 coding harness，列入后续候选 |
| [XiaoDuoYa/codex-with-chatgpt](https://github.com/XiaoDuoYa/codex-with-chatgpt) | 6,522 | 589 | TypeScript | MIT | 2026-09-13T03:22:46Z | planner/worker 分层候选，今日不展开 |
| [rakanki911/DLSS5-Swapper](https://github.com/rakanki911/DLSS5-Swapper) | 6,462 | 342 | JavaScript | MIT | 2026-09-13T02:02:21Z | 游戏图形工具，非当前共享中台主线 |
| [jaredpalmer/kev](https://github.com/jaredpalmer/kev) | 5,958 | 325 | Python | Apache-2.0 | 2026-09-23T23:34:11Z | 自托管 Jev-like 模型，明日对照 Laya |

> 表中 Stars、Forks、Language、License、时间均来自 GitHub Repository API。License 是仓库根识别结果，不覆盖依赖、模型权重、训练数据、远端服务条款或 release assets；`pushed_at` 也不等于生产成熟度。

## 深读项目

### 1. NandhaKishorM/laya

- **一句话判断**：值得学的是把 choice/score/yes-no 这类高频 Agent 判断做成 typed、可路由、可 hook、可批处理的独立 decision plane；不值得直接照搬的是把未经本域校准的概率当作自动执行或删除授权。
- **解决的问题**：替代用自回归 LLM 生成 JSON、再解析自由文本来做路由/审核/优先级判断的旧做法；同时用 checkpoint router 避免一个英文模型在非英文输入上“高置信错误”。
- **URL / API 快照**：https://github.com/NandhaKishorM/laya ；**Stars: 20,354 / Forks: 1,727 / Language: Python / License: Apache-2.0**；`created_at=2026-09-18T04:46:33Z`，`updated_at=2026-09-23T23:34:53Z`，`pushed_at=2026-09-23T18:05:00Z`，default branch `main`，API `open_issues_count=75`（含 PR）。
- **固定提交 / release**：[`1e28ac20c0896b1c37a744cd11f740eb98f8b178`](https://github.com/NandhaKishorM/laya/commit/1e28ac20c0896b1c37a744cd11f740eb98f8b178)，commit time `2026-09-23T18:04:56Z`，GitHub verification=false；tag/release `v0.3.11` published `2026-09-23T18:06:39Z`。
- **Release / issue / checks**：固定 commit 的 GitHub CI、Docker、Security run 均 success。release notes核到 routed batches、prediction hooks、malformed JSON 400、atomic tokenizer config rewrite、request limits/timing-safe auth 等改动。issue [#285](https://github.com/NandhaKishorM/laya/issues/285) 要求按 release 刷新 benchmark，说明当前 headline 数据可能 stale；issue [#290](https://github.com/NandhaKishorM/laya/issues/290) 仍在讨论完整会话提取契约。
- **来源交叉核验**：README、release `v0.3.11`、issues #285/#290、`pyproject.toml`、Router/Agent/hooks/server/fast path 源码、router/lang/server tests、GitHub Actions、本机 compile + pure-router test。

#### 架构 / 实现与数据流

```text
state + typed questions
  -> Router._route()
      explicit model > task > opt-in workflow > lang > lang_guess > script/language > default
  -> Router.load()
      checkpoint cache + LRU + optional preload/attach
  -> Agent.predict_batch()
      validate questions once
      -> serialize/tokenize state per question
      -> collate rows into bounded batches
      -> encoder + decision head in one forward pass
      -> temperature scaling + typed decode
  -> answers + confidence + usage + routing metadata
  -> optional hooks
      audit / redact / cache / gate / trace / on_error
  -> optional adapters
      Jev-compatible HTTP / MCP / LangChain / ONNX / TypeScript
```

这个设计把“决定什么”和“执行什么”分开：Laya只返回 typed probabilities，真正副作用仍应由宿主 policy gate 执行。Router 在模型加载前完成显式优先级和语言分流；Agent 把同一 questions 下多个 states 合并为 shared forward；hooks 是 observation/transformation seam，不是自动安全边界。HTTP 层进一步限制 body/state/question 数量并把同步推理移出 event loop。

#### repo tree 摘要

固定 commit（排除 `.git`）扫描到 **230 个文件**：

```text
laya/
├── laya/
│   ├── router.py            # checkpoint 选择、LRU、heterogeneous batch
│   ├── agent.py             # checkpoint 加载、验证、encode/forward/decode
│   ├── common.py            # sequence/model/temperature 公共逻辑
│   ├── hooks.py             # lifecycle context 与 dispatch
│   ├── serve.py             # Jev-compatible FastAPI endpoint
│   ├── fast.py              # TileLang + CUDA Graph fast path
│   ├── onnx_agent.py        # ONNX runtime adapter
│   ├── integrations/        # LangChain/LangGraph
│   └── mcp/                 # MCP tools/server
├── laya-ts/                 # Node/browser 实现与 parity tests
├── tests/                   # router/batch/hooks/server/onnx/security regressions
├── research/                # eval、benchmark scripts 与结果
├── benchmarks/              # fast/parity 复现入口
├── docs/                    # hooks、Docker、LangChain、fine-tuning
├── pyproject.toml           # Python 依赖与 extras
└── README.md / BENCHMARKS.md
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `laya/router.py` | 决策前路由与 resident cache | 明确 precedence；语言 hint 可 abstain；模型按 LRU 管理；批请求先按 checkpoint、再按 questions 分组 |
| `laya/agent.py` | 核心 inference runtime | checkpoint allow-pattern 下载、权重/shape 验证、问题 schema 验证、batch encode/forward/decode、OOM CPU fallback |
| `laya/hooks.py` | 可观测/变换 seam | `PredictContext`、6 个 lifecycle events、skip/cache、并发与错误策略 |
| `laya/serve.py` | Jev-compatible HTTP adapter | request/body/question 上限、timing-safe bearer 比较、单 worker offload、安全错误映射 |
| `laya/fast.py` | CUDA fast path | bf16 resident weights、TileLang fused kernels、shape bucket 与 CUDA graph replay |
| `tests/test_lang_guess.py` | 路由 regression | 52 个纯 Python assertions；覆盖 hint、abstain、precedence、predict forwarding |
| `tests/test_router_batch.py` | heterogeneous batch contract | 输入预验证、checkpoint/questions 分组、原序恢复、并发 load 去重 |
| `tests/test_serve.py` | HTTP adapter contract | malformed JSON、auth、known model、event-loop offload 与 health 并发 |

#### ⭐ 源码精读

**代码块 1：`Router._route()` 把显式意图放在 heuristic 前，并允许 language hint abstain。**

```python
def _route(self, state, questions=None, model=None, task=None,
           lang=None, lang_guess=None) -> RouteDecision:
    if model is not None:
        key = normalise_name(model)
        return RouteDecision(model=key, repo=_repo_str(self.models[key]),
                             reason="explicit model=%r" % model,
                             detection=None, workflow=None)
    if task is not None:
        key = normalise_name(
            "typed-decisions"
            if str(task).lower().replace("-", "_") == "typed_decisions"
            else task
        )
        return RouteDecision(model=key, repo=_repo_str(self.models[key]),
                             reason="explicit task=%r" % task,
                             detection=None, workflow=None)
    for source, hint in (("lang_guess", lang_guess),
                         ("Router(lang_guess=...)", self.lang_guess)):
        resolved = self._resolve_hint(hint, state)
        if resolved is not None:
            key = "english" if resolved else "multilingual"
            return RouteDecision(model=key, repo=_repo_str(self.models[key]),
                                 reason=f"{source}: caller hint",
                                 detection=None, workflow=workflow)
```

逻辑摘要：显式 `model/task/lang` 是 caller-owned authority，heuristic 只在缺少显式信息时参与；hint 返回 `None` 时继续内建检测，不会强行选模型。本机运行 `Router(default='multilingual').route()`，英文进入 `english`，阿拉伯文进入 `multilingual`，短葡萄牙语因 undecided 使用配置的 default。边界：纯 heuristic 路由正确不证明下游 checkpoint 判断正确，且短 Latin 文本仍依赖 default/LID。

**代码块 2：`Router.predict_batch()` 先固定 denominator，再按 checkpoint 与 question schema 分组。**

```python
def predict_batch(self, requests, batch_size=None):
    decisions = self.route_batch(requests)
    if not decisions:
        return []
    groups = {}
    for i, decision in enumerate(decisions):
        groups.setdefault(decision.model, []).append(i)
    results = [None] * len(requests)
    for model_name, indices in groups.items():
        agent = self.load(model_name)
        question_groups = []
        for i in indices:
            questions = requests[i]["questions"]
            for group in question_groups:
                if group["questions"] == questions:
                    group["indices"].append(i)
                    break
            else:
                question_groups.append({"questions": questions, "indices": [i]})
```

逻辑摘要：所有 request 在 load 前先完成 validation/routing，随后只优化执行顺序，最后恢复原始 index。这种“先冻结完整输入集合，再做性能分组”的模式适合 Agent 审计与批量学习；优化器不能让某个 item 从 denominator 消失。边界：questions 用 dict equality 线性分组，大批异构 schema 的复杂度和 canonical schema hash 尚需压测。

**代码块 3：`Agent.predict_batch()` 只验证一次 schema，再以 state chunks 共享 forward。**

```python
@torch.no_grad()
def predict_batch(self, states, questions, batch_size=None, **kwargs):
    ids = list(questions.keys())
    if not ids:
        return [{"model": "laya-rl-agent", "answers": {},
                 "usage": {"input_tokens": 0, "output_tokens": 0}}
                for _ in states]
    for qid in ids:
        self._check_question(qid, questions[qid])
    internal = {qid: self._to_internal(questions[qid]) for qid in ids}
    chunk = batch_size if (batch_size and batch_size > 0) else len(states)
    results = []
    for start in range(0, len(states), chunk):
        part = states[start:start + chunk]
        per_state_items = [self._encode_state(st, ids, internal)
                           for st in part]
        b = collate_items(per_state_items, self.tok.pad_token_id)
        logits, act = self._forward(b)
```

逻辑摘要：question schema 是 batch invariant，validation/normalization 不重复；state×question rows 被 collate 后共享 forward，最后逐 state decode。空问题直接返回零 usage，不触发 tokenizer/model。边界：README声称的 GPU 9–10×吞吐、33ms 和概率 parity 本机未跑；当前环境缺 `torch`，pytest在 collection 阶段失败，不能写成模型 tests 通过。

**代码块 4：HTTP adapter 在 tokenization 前限制攻击面，并把同步推理移出 event loop。**

```python
def _check_request_limits(state: Any, questions: Any) -> None:
    if not isinstance(questions, dict):
        raise HTTPException(status_code=400, detail="'questions' must be an object")
    if len(questions) > MAX_QUESTIONS:
        raise HTTPException(status_code=413, detail="too many questions")
    state_len = len(state) if isinstance(state, str) else len(str(state))
    if state_len > MAX_STATE_CHARS:
        raise HTTPException(status_code=413, detail="state too large")

async with gate:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        pool, lambda: router.predict(state, questions, model=model))
```

逻辑摘要：body 2MiB、state 50k chars、questions 64 的静态上限先于模型内存分配；single-worker pool避免 CPU/GPU forward堵塞 FastAPI event loop。边界：`len(str(dict))` 不是 canonical serialized byte size；单 worker保护设备但也形成队头阻塞，生产部署仍需 ingress queue/deadline/metrics。

#### 依赖分析与供应链风险

- `pyproject.toml` 要求 Python >=3.10；核心依赖：`torch>=2.0.0`、`transformers>=4.48.0`、`safetensors>=0.4.0`、`huggingface_hub>=0.20.0`、`numpy>=1.20.0`。没有锁文件，范围依赖意味着同一 commit 在不同日期可能解析出不同 graph。
- 可选 extras：FastAPI/Uvicorn/python-multipart、TileLang、MCP、ONNX/onnxruntime、LangChain/LangGraph。每个 adapter 扩大独立供应链和攻击面，不能用 core license/CI 替代它们的审计。
- checkpoint 通过 Hugging Face `snapshot_download` 拉取，源码用 allow-pattern 收窄文件集合，并用 safetensors + architecture/shape strict checks；但本次未验证模型制品 digest、签名、训练数据许可或恶意权重之外的 tokenizer/config 风险。
- GitHub Security Advisories API 返回空数组；vulnerability-alerts endpoint 404，不能据此声称无漏洞。本机未安装完整依赖，也没有可信的 `pip-audit` resolved graph。
- 固定 release 的 Actions 绿色是有价值证据，但 issue #285 已由维护者指出 benchmark artifacts 与代码/checkpoint 漂移风险，README 速度/准确率只能记为上游测量，不能直接进入 shared active fact。

#### 可复用经验

- 当 Agent 只需做有限 choice/score/boolean 判断时，应优先使用 typed decision plane，并让宿主保留 effect authority，因为结构化概率比自由文本更易验证，但它仍只是 proposal；边界是本域 calibration 与 false-positive cost 必须实测。
- 当多个 checkpoint 各自只覆盖部分输入分布时，应优先在 forward 前用显式 override + 可 abstain router 分流，因为错误 checkpoint 可能高置信失败；边界是 router heuristic 也必须有 unknown/default 与真实 corpus regression。
- 当批量优化可能改变执行顺序时，应优先先冻结完整 denominator 和 per-item decision，再按兼容 schema 分组并恢复原序，因为性能层不能改变覆盖面；边界是异常时必须能标出未执行 items。
- 当第三方 classifier 提供 hooks 时，应优先把 hooks 用于审计、cache、redaction 和 soft gate，不要把 hook declaration 当宿主硬授权，因为 plugin code 与 host policy 的 authority 不同。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/typed-decision-shadow-gate-v0/` 建立纯离线 shadow fixture：输入 30 条历史 cron/audit case，仅问 `route / risk / needs_review`，输出 typed proposal；与现有确定性规则比较 confusion matrix、abstain、coverage、pinned errors。第一轮只用 fake scorer 验证 schema/threshold/receipt，不下载 checkpoint、不修改 Hermes/OpenClaw 配置、不触发任何副作用；真实模型实验必须在独立 venv 并记录 checkpoint revision。

#### 风险边界

- **License**：仓库与 GitHub API 为 Apache-2.0；模型权重、训练数据、Hugging Face制品、TileLang/ONNX/LangChain/MCP 依赖和 benchmark datasets需独立核验。
- **维护活跃度**：仓库仅创建约 6 天，但已到 v0.3.11，09-23 单日连续发布多个版本；高活跃也意味着 API、checkpoint 与 benchmark 快速变化。
- **安全风险**：classifier 可被 adversarial text、distribution shift、label wording和校准漂移影响；remote model download 是供应链入口；HTTP bearer 只覆盖应用层身份，不是租户配额、请求隐私或 OS sandbox。
- **局限性**：README自己披露 50+ labels、ordinal score、多语言位置偏差、`noul` label sensitivity、raw calibration等限制；base checkpoint 在 typed-decisions 零样本表现接近/低于 majority baseline，价值主要来自 fine-tuning。
- **验证局限**：本机没有 `torch`，完整 pytest/model forward/HTTP tests均未运行；只完成 compile、Router无权重 smoke 与 52 条纯路由 assertions。README latency、accuracy、calibration 与自托管兼容性待独立复验。
- **不适用场景**：开放式生成、需要长链推理、高基数未调优分类、不可容忍误删/误执行且无人工或确定性 fallback 的场景。

#### ⭐ Skill 升格判断

**需二次验证。** 可抽象迁移的是 `typed proposal + explicit router precedence + abstain/default + frozen denominator + host effect gate`；不直接安装 Laya、不把模型概率接入自动修改/删除、不复制其 preset 为 shared truth。先完成 shadow corpus、校准、checkpoint pin、资源与隐私评估，再决定是否更新现有 autonomous-learning/verification workflow；当前不新建 shared skill。

#### ⭐ Hermes / shared hub 落地路径

1. 在 `runtime/hermes/github-learning-poc/typed-decision-shadow-gate-v0/` 定义 agent-neutral input/output schema，状态只允许 `proposed | abstained | blocked | failed`，不包含执行权限。
2. 在现有 `scripts/github_learning_orchestrator.py` 或反思引擎旁增加可选 shadow adapter，而不是改 provider/config；原确定性 audit 仍是 authority。
3. evidence 写 `runtime/hermes/`，候选经验写 `inbox/hermes/daily/`；真实收益经治理审查前不进入 `curated/memory/`。
4. 如果后续复用到其他 Agent，只共享 decision contract/fixtures 到现有 workflow skill；每个 host 保留自己的 adapter、资源预算与最终 effect gate。
5. 不自动改 Hermes/OpenClaw model、provider、auth、cron 或 secret；本轮未调用、未配置 OpenClaw。

---

### 2. tamaratran/fast-jev-compaction

- **一句话判断**：值得学的是“不改写用户/助手文本，只对 tool call/result 做 pair-preserving、三级动作的 verbatim pruning”；不能直接采用的是把远端 classifier 结果当删除授权，以及把 session 内压缩成功误当跨 resume 持久成功。
- **解决的问题**：替代 LLM 把旧对话重写成 lossy summary，避免 exact path、error、command、constraint 被摘要吞掉；通过 `keep / drop_result / drop_call` 比全留或全删多一个中间层。
- **URL / API 快照**：https://github.com/tamaratran/fast-jev-compaction ；**Stars: 6,565 / Forks: 380 / Language: TypeScript / License: MIT**；`created_at=2026-09-17T05:57:20Z`，`updated_at=2026-09-23T23:31:29Z`，`pushed_at=2026-09-18T04:45:31Z`，default branch `main`，API `open_issues_count=79`（含 PR）。
- **固定提交 / release**：[`e3f262a7f4d42bd8dd32ced30d26176f7cb545b0`](https://github.com/tamaratran/fast-jev-compaction/commit/e3f262a7f4d42bd8dd32ced30d26176f7cb545b0)，commit time `2026-09-17T22:29:18Z`，GitHub verified=true。Tags API 与 Releases API 均为空；`package.json` version `0.2.0`，`.claude-plugin/plugin.json` version `0.3.0`，版本身份不一致。
- **Release / issue / checks**：无 GitHub Actions runs。issue [#89](https://github.com/tamaratran/fast-jev-compaction/issues/89) 报告 plugin 压缩在当前 session 有效，但 `--resume` 回载接近完整历史；其 discriminator 指向缺少 `compactMetadata.preservedSegment/preservedMessages` 与 message handle/parent chain。issue [#97](https://github.com/tamaratran/fast-jev-compaction/issues/97) 报告真实 coding transcript 中 shell/SQL/path 文本触发 Cloudflare HTML 403，导致 fallback。两者均是上游复现，当前环境未连接 TypeSafe/Claude Code E2E。
- **来源交叉核验**：README、hooks README、plugin manifest、package manifest/lock、`src/compact.ts`、`src/state.ts`、`src/request.ts`、hook adapter、tests、GitHub issues/API、本机 install/typecheck/test/build/audit。

#### 架构 / 实现与数据流

```text
session messages
  -> collectToolCalls()
      pair tool_use <-> tool_result by tool_use_id
      pin first + newest N messages
  -> fitState()
      keep user/assistant text; replace tool outputs with notes
      staged fitting: input caps -> text abridge -> collapse -> compact calls -> omit/merge
  -> batchCalls()
      same full state + bounded question batches
  -> JevAsker.ask()
      2 noul questions per candidate: keepCall / keepResult
  -> decideCall()
      keepResult >= threshold -> keep pair
      else keepCall >= threshold -> keep call + truncate result
      else -> remove call + result
  -> applyDecisions()
      preserve order, pair integrity, untouched object identity
  -> plugin adapter
      minimum reduction gate -> return messages
      any failure/low reduction -> built-in compaction fallback
```

核心不是“压缩文本”，而是对 history 中可重取的工具证据做 selection。它把调用存在性与完整结果内容分开判断，且以 `tool_use_id` 保证 call/result成对变化；first/recent messages pinned。输出不重写普通 user/assistant text。边界是状态送往远端 Jev，完整 state 会随每个 question batch 重发；classifier决定删除什么，但没有证明跨宿主 resume、隐私、WAF或真实任务成功率。

#### repo tree 摘要

固定 commit（排除 `.git`、安装生成的 `node_modules/dist`）扫描到 **26 个源文件**：

```text
fast-jev-compaction/
├── src/
│   ├── compact.ts       # options、questions、batch、decision、rebuild、orchestration
│   ├── state.ts         # pair、pin、token estimate、staged state fitting
│   ├── request.ts       # Jev request/response contract
│   ├── client.ts        # fetch transport
│   ├── messages.ts      # compactMessages convenience API
│   ├── types.ts         # typed transcript/decision/result schema
│   └── index.ts         # public exports
├── hooks/
│   ├── fast-jev.ts      # Claude Code session.compact / turn.complete adapter
│   ├── hooks.json       # registration metadata
│   └── README.md        # host/version/fallback contract
├── tests/
│   ├── fast-jev-compaction.test.ts
│   └── hook.test.ts
├── .claude-plugin/      # plugin + marketplace manifests
├── types/               # Claude Code 2.1.274 generated declarations
├── package.json
├── package-lock.json
└── README.md / LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/state.ts` | state projection 与预算 | pair call/result、固定 first/recent、启发式 token estimator、按阶段有损缩减 classifier 输入 |
| `src/compact.ts` | 核心 sans-I/O engine | 两问 schema、request batching、三级 decision、pair-safe rebuild、stats |
| `src/request.ts` | transport contract | System One request、HTTP/JSON/answer validation；错误 body 截前 200 chars |
| `src/client.ts` | 网络 adapter | API key/env、injectable fetch、无 key fail closed |
| `hooks/fast-jev.ts` | Claude Code adapter | plugin config、session object mapping、minimum reduction fallback、auto-compact in-flight guard |
| `tests/fast-jev-compaction.test.ts` | core contract | fitting stages、pairing、threshold、rebuild、batch merge、malformed response |
| `tests/hook.test.ts` | adapter contract | hook config、identity mapping、fallback 和 plugin behavior |

#### ⭐ 源码精读

**代码块 1：`decideCall()` 明确了三态，而不是单一 keep/delete。**

```ts
export function decideCall(
  call: Pick<ToolCall, 'id' | 'tool' | 'pinned'>,
  answer: CallAnswer,
  options: Pick<ResolvedCompactOptions, 'keepThreshold'>,
): CallDecision {
  const base = { id: call.id, tool: call.tool, ...answer };
  if (call.pinned) return { ...base, action: 'keep', reason: 'pinned' };
  if (answer.keepResult >= options.keepThreshold) {
    return { ...base, action: 'keep', reason: 'kept' };
  }
  if (answer.keepCall >= options.keepThreshold) {
    return { ...base, action: 'drop_result', reason: 'result_dropped' };
  }
  return { ...base, action: 'drop_call', reason: 'call_dropped' };
}
```

逻辑摘要：保留完整结果的要求最高；结果不重要但“做过什么”仍重要时，只截断 result；调用本身也不重要才删 pair。pinned 是 deterministic override，不让 classifier 删除最近/首消息中的工具证据。边界：同一阈值作用于不同 tool/effect/result cost，未按 destructive effect、不可重放性、错误结果、secret/PII 等风险分级。

**代码块 2：`compact()` 先冻结候选和 state，再并发问答并重建。**

```ts
export async function compact(messages, asker, options = {}) {
  const resolved = resolveOptions(options);
  const calls = collectToolCalls(messages, resolved.preserveRecentMessages);
  const candidates = calls.filter((call) => !call.pinned);
  const answers = new Map<string, CallAnswer>();
  if (candidates.length > 0) {
    const state = fitState(messages, calls, resolved);
    const batches = batchCalls(candidates, state.tokens, resolved);
    const answered = await Promise.all(
      batches.map((batch) => askBatch(asker, state.state, batch)),
    );
    for (const map of answered) {
      for (const [id, answer] of map) answers.set(id, answer);
    }
  }
  const decisions = calls.map((call) =>
    decideCall(call, answers.get(call.id) ?? { keepCall: 1, keepResult: 1 }, resolved),
  );
  return { messages: applyDecisions(messages, decisions, calls,
                                     resolved.truncateHeadChars), decisions };
}
```

逻辑摘要：候选集合由 deterministic pairing/pinning 产生，Jev只填每个已有 ID 的概率；缺答案默认 keep，不会静默删除。所有 batches 共享同一个 fitted state，回答后一次性 rebuild。边界：并发请求无显式 timeout/retry/cancel limit；完整 state 重发会放大费用和隐私暴露；`Promise.all` 任一失败使整轮 fallback，安全但可用性脆弱。

**代码块 3：`fitState()` 逐阶段压缩“给 classifier 看的 state”，并保留最终 fail-closed。**

```ts
rebuild(INPUT_CHARS[0]);
if (fits()) return fitted(history, tokens, 'full');
for (const limit of INPUT_CHARS.slice(1)) {
  rebuild(limit);
  if (fits()) return fitted(history, tokens, `inputs<=${limit}`);
}
for (const index of order) {
  const entry = history[index]!;
  if (entry.text.length <= TEXT_HEAD + TEXT_TAIL + 40) continue;
  shrink(index, (e) => { e.text = abridge(e.text, TEXT_HEAD, TEXT_TAIL); });
  if (fits()) return fitted(history, tokens, 'texts abridged');
}
// 后续：old messages collapsed -> old calls compacted -> left out -> merged
throw new Error(
  `history too large for Jev (~${tokens} tokens after truncation, limit ${options.maxStateTokens})`,
);
```

逻辑摘要：首先压 tool inputs，然后才动文本；旧且非 pinned 优先缩减。每一步带 `stateStage`，超过预算最终抛错，不发送超大 request。边界：估算器不是 tokenizer；被压缩的是 classifier evidence，越往后 classifier越可能因缺证据误删输出，当前只有 stage 标签，没有按 stage 自动提高 keepThreshold或强制 fallback。

**代码块 4：plugin adapter 将“减少不够”与所有异常统一退回宿主内建 compaction。**

```ts
on('session.compact', async ($, event, next) => {
  try {
    const { result, messages } = await compactSession(
      event.messages, config, fetchFn,
    );
    if (reductionRatio(result) < config.minReductionRatio) {
      notify($, `fallback to built-in summary (below minimum)`);
      return next(event);
    }
    notify($, `kept ${messages.length}/${event.messages.length} messages, no summary`);
    return { messages };
  } catch (error) {
    notify($, `fallback to built-in summary (${String(error)})`);
    return next(event);
  }
});
```

逻辑摘要：网络失败、malformed answer、state fit失败、无 key与低收益均不返回半成品，而是调用 host fallback；`turn.complete` 还有 `compacting` in-flight guard。边界：fallback 是内建 lossy summary，不是“保持原历史”；issue #89 显示 session内 `{messages}` 返回成功也未必形成可 resume 的 durable boundary，必须把跨重启 read-back纳入完成条件。

#### 依赖分析与供应链风险

- package runtime 没有第三方 `dependencies`；Node >=18，核心只依赖 native `fetch`。devDependencies 为 TypeScript、tsx、Vitest、`@types/node`，并提交 `package-lock.json`。
- 本机 `npm ci` 安装后，typecheck（含 hook）、29 tests、build均通过。`npm audit --omit=dev` 为 **0 known findings**；完整 graph 为 5 findings：Vitest critical、Vite high，以及 3 moderate transitive findings。它们当前属于 dev/test graph，不应描述为 production exploit 已可达，但升级是合理 action。
- 安装时 npm 还提示两个 esbuild install scripts 未在 allowScripts 覆盖；本次工具链最终成功，但第三方 install scripts仍是供应链 effect surface。
- 没有 tag/release/Actions，package `0.2.0` 与 plugin `0.3.0` 分叉；用户很难仅靠仓库版本判断实际 adapter contract。generated Claude Code types固定在 2.1.274，hooks README明确 function hooks 为 early access。
- GitHub Security Advisories API为空，vulnerability-alerts endpoint因前一个仓库调用404而未形成两仓可靠 enablement结论；不能声称无漏洞。

#### 可复用经验

- 当上下文压缩的首要目标是保留 exact constraints/errors/paths 时，应优先对可重取工具证据做 selection，而不是重写全部文本，因为 verbatim retention更可审计；边界是 selection本身仍会丢信息。
- 当 tool call 与 result 具有引用关系时，应优先以 stable pair identity做原子 keep/truncate/drop，因为孤立 result 或孤立 call 会破坏会话结构；边界是宿主持久化还可能依赖额外 parent/handle metadata。
- 当 classifier evidence 为了预算经历 staged loss 时，应优先记录 stage、coverage与估算误差，并随 loss程度收紧删除策略，因为“请求 fit”不等于“判断仍有足够证据”；边界是启发式 token估算必须对目标模型真实校准。
- 当压缩声称成功时，应优先在新进程/新会话 resume 后读取实际 token/history并验证 boundary metadata，因为 session内 message减少不证明 durable transcript已缩减。
- 当远端 classifier处理真实 coding transcript时，应优先评估数据出域、WAF、deadline与可替换 transport，因为 shell/path/SQL正是正常内容；边界是 base64绕 WAF会破坏语义且不是安全修复。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/context-pruning-contract-v0/` 建一个无网络 TypeScript/Python fixture：10 条 transcript覆盖 read、write、failed shell、不可重放 external effect、secret placeholder、最近消息；fake scorer输出 keep/drop probabilities。验证：(1) call/result永不孤立；(2)首条/最近 N 条 pinned；(3)destructive/unknown effect默认 keep；(4)缺答案/exception fail closed；(5)压缩后 serialize→reload→reconstruct一致；(6)只有通过 fresh-process resume read-back才记 completed。该实验不安装 Claude Code plugin、不连接 Jev、不修改任何 agent配置。

#### 风险边界

- **License**：仓库与 GitHub API为 MIT；TypeSafe/Jev远端服务、Claude Code function hooks、transcript内容与依赖许可需独立核验。
- **维护活跃度**：仓库创建、最后 commit和 push都集中在 09-17/18，之后开放 issues增长到79但 main无新 commit；没有 tag/release/CI，热度与 issue活跃不能替代维护响应。
- **安全/隐私风险**：完整对话 state被发送到远端，每个 batch重复发送；可能包含源码、路径、shell、错误、内部业务和PII。项目不做通用 secret redaction，也没有 egress allowlist/retention证明。
- **持久化风险**：issue #89 表明当前宿主版本中 session内成功不等于 resume成功；返回原 message object handles可能使 parent walk跨越 compaction boundary。
- **可用性风险**：issue #97 的 HTML 403 表明正常 coding文本可被边缘 WAF阻断；client目前错误只截前200字符，plugin未暴露 `baseUrl`，只能 fallback。
- **决策风险**：一个全局 threshold同时处理可重放 read和不可重放 effect；概率不是删除证明。token estimator与state abridgement会改变 classifier所见证据。
- **验证局限**：本机只验证 core/hook unit contract、type/build与audit；未持有/使用 TypeSafe key，未运行Claude Code function hook，未复现 #89/#97，也未测真实任务成功率或token savings。
- **不适用场景**：审计/合规要求完整日志、工具结果不可重取、effect结果决定后续安全状态、禁止源码/对话出域、宿主不支持稳定 compaction boundary 的场景。

#### ⭐ Skill 升格判断

**需二次验证。** `pair-preserving tri-state pruning + pinned window + fail-closed fallback + fresh-resume verification` 值得作为 context-governance candidate；但不安装该 Claude Code plugin、不调用远端 Jev、不复制其 host专属 hook，不把它升格为 shared active skill。先在 Hermes runtime完成纯 fixture、真实历史 replay、secret/egress policy和跨进程恢复验证，并与既有 shared-memory/verification/completion contract去重。

#### ⭐ Hermes / shared hub 落地路径

1. 只在 `runtime/hermes/github-learning-poc/context-pruning-contract-v0/` 实现 sans-I/O transcript normalizer、pair validator、pin policy和fake scorer，不接任何生产 session。
2. 定义 agent-neutral `ContextItem`：`stable_id / kind / source_pointer / replayability / effect_certainty / pinned / decision / reason`；宿主 adapter负责映射，不共享Claude Code handle。
3. 压缩状态写入 runtime receipt：`input_hash / policy_version / coverage / estimated_tokens / output_hash / pair_integrity / reload_verified / terminal`；`reload_verified=false` 不得投影为 completed。
4. 若真实回放证明收益，优先更新现有 verification/completion/shared-memory workflow，不新建 fast-jev专属 shared skill；Hermes与其他Agent分别实现host adapter。
5. 不把原始 transcript、secret或完整tool output写入 `curated/`；候选事实只进入 inbox审查。本轮不改配置、provider、cron、auth，不调用OpenClaw。

## 经验沉淀

1. 当 Agent 的任务是有限集合判断而非开放生成时，应优先采用 typed proposal plane，并让宿主在最终 effect chokepoint重验，因为可解析概率不等于授权；边界是本域 calibration、abstain与fallback必须实测。
2. 当性能优化要对请求重排或分组时，应优先先冻结 coverage denominator与per-item identity，再按兼容 schema执行并恢复原序，因为优化层不能静默改变审计范围。
3. 当长上下文压缩要避免摘要失真时，应优先保留普通文本原文，只对可重取工具证据做 pair-preserving keep/truncate/drop，因为 exact constraint/path/error更可审计；边界是不可重放 effect默认不得删。
4. 当 classifier所见 state经历截断、折叠或省略时，应优先把 loss stage与coverage写入decision receipt，并随证据减少提高保守度，因为fit进窗口不代表判断依据完整。
5. 当压缩或迁移宣称完成时，应优先在fresh process/session中read-back并验证实际恢复状态，因为session内结果、exit 0或toast都不能证明durable continuation。
6. 当远端服务处理代码、shell、SQL和路径时，应优先把WAF、隐私、重复传输、deadline和替代transport纳入prerequisite，而不是把这些正常payload误判为异常边角。
7. 当README给出latency、accuracy、token saving或校准数字时，应优先绑定checkpoint/code/hardware/environment/raw artifact，并检查维护者是否报告benchmark drift，因为最新release不自动刷新历史测量。
8. 当项目同时有package、plugin、host types与远端model版本时，应优先建立artifact-level identity matrix，因为仓库commit、package version、plugin version、host版本和服务端模型并不是同一个对象。

## 明日继续

1. 深读 `jaredpalmer/kev`，与 Laya 对比：decision schema、模型/数据license、calibration、self-host路径、真实checkpoint identity与benchmark可复现性。
2. 建 `context-pruning-contract-v0` 最小fixture，优先验证 pair integrity、不可重放effect默认keep、缺答案fail closed和serialize→fresh reload。
3. 为 typed decision shadow实验准备30条已脱敏历史case，只比较proposal与现有deterministic verdict；不接生产effect、不自动调threshold。
4. 追踪 Laya issue #285、fast-jev issues #89/#97；只有fixed commit进入目标release并完成本机复验后，才更新对应风险判断。

## 候选反哺

### Candidate Facts

- [ ] topic: typed decision模型适合作为Agent proposal plane而非effect authority | evidence: Laya Router/Agent/hooks源码 + 本机52条router assertions + README公开限制 | 建议: create candidate, not active fact | 安全级别: medium
- [ ] topic: context pruning完成态必须包含fresh-resume read-back | evidence: fast-jev issue #89 + hook只返回session messages的源码路径 | 建议: update completion receipt candidate | 安全级别: high
- [ ] topic: pair-preserving tri-state pruning比全文摘要更可审计 | evidence: `collectToolCalls/decideCall/applyDecisions` + 本机29 tests | 建议: POC then review | 安全级别: medium
- [ ] topic: staged evidence loss应进入decision receipt | evidence: `fitState()`阶段化缩减 + heuristic token estimator | 建议: create candidate | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: typed-decision-shadow-gate（更新现有verification/autonomous-learning workflow） | 可复用场景: routing、risk、needs_review等低延迟proposal | 是否建议shared: yes（仅候选） | 原因: 跨Agent可复用，但需真实corpus/calibration/resource/privacy验证
- [ ] 名称: context-pruning-completion-contract（优先更新既有completion/shared-memory workflow） | 可复用场景: compaction、memory projection、session resume | 是否建议shared: yes（仅候选） | 原因: pair integrity与fresh-resume receipt为横切不变量，但host adapter必须分离

### Candidate Open Questions

- [ ] 问题: shared hub中哪些tool result可标为replayable，谁拥有最终标注authority？ | reason: adaptation | priority: high
- [ ] 问题: classifier state进入abridged/collapsed阶段后，threshold应如何动态收紧，何时直接fallback？ | reason: gap | priority: high
- [ ] 问题: Laya checkpoint/model artifact如何pin revision与digest，且如何在WSL CPU/GPU环境做可重复calibration？ | reason: gap | priority: medium
- [ ] 问题: 不同host的session handle/parent chain如何映射为agent-neutral continuation receipt而不丢宿主语义？ | reason: adaptation | priority: high

### 不应自动落地

- 不自动安装或启用 Laya / fast-jev-compaction，不下载checkpoint，不调用TypeSafe/Jev，不连接真实Claude Code/OpenClaw session。
- 不自动改 Hermes/OpenClaw config、model、provider、auth、cron或secret；本次未调用OpenClaw。
- 不直接写 `curated/memory/` active fact，不创建新shared skill；报告、project cards与lessons仍是raw/candidate，需评分、去重、脱敏和审查。
- 不让probability直接授权删除、执行、配置修改或长期记忆晋升；不可重放/unknown effect默认keep或blocked。
- 不把GitHub Actions、unit tests、空advisory、Stars或README benchmark外推为生产安全、跨平台稳定、校准可靠或真实任务成功。
