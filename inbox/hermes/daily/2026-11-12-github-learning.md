---
type: github-learning-daily
status: raw-research
created: 2026-11-12
updated: 2026-11-12
runner: hermes
---

# 2026-11-12 GitHub 热门项目学习日报

> 查询时间：2026-11-12 07:31–07:36 CST。Stars、Forks、License、更新时间均取自 GitHub Repository API；源码结论固定到下述 commit。证据缓存位于 `runtime/hermes/github-hot-project-learning/evidence/2026-11-12/`。本报告是 Hermes inbox 原始研究，不是 curated 事实。

## 今日结论

Agent 系统最值得复用的不是“更主动”，而是把 **授权门（proposal ≠ authority）→ 单写者事务核心 → commit 后 durable effects → typed terminal/read-back** 做成宿主强制的确定性外壳；高性能异步推理同样证明 queue empty 不等于 completed，必须显式 flush 在途结果。

## 项目速览

以下七项均由 2026-11-12 GitHub API 实时核验；“最近更新”是 repository `updated_at`，并非发布版本。

| 项目 | Stars | Language | License（API） | 最近更新 UTC | 判断 |
|---|---:|---|---|---|---|
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 56,514 | Python | NOASSERTION | 2026-11-11T23:26:21Z | 热度高但许可识别不清，只观察，不迁移源码 |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 28,335 | Rust | Apache-2.0 | 2026-11-11T23:31:58Z | 多媒体生成工具链候选，今日不深读 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 25,865 | Python | Apache-2.0 | 2026-11-11T23:26:46Z | 深读：异步调度与显式 flush |
| [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) | 22,482 | TypeScript | MIT | 2026-11-11T23:09:19Z | 深读：授权、事务核心、durable effects |
| [seedds/nxnative](https://github.com/seedds/nxnative) | 14,808 | Python | MIT | 2026-11-11T23:26:36Z | issue 数较高，继续观察维护压力 |
| [heydamir/unslop](https://github.com/heydamir/unslop) | 14,519 | JavaScript | CC-BY-4.0 | 2026-11-11T23:28:17Z | 内容许可不宜直接外推到软件复用 |
| [amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness) | 8,736 | TypeScript | AGPL-3.0 | 2026-11-11T23:24:31Z | 学习 harness 值得后续看，网络服务复用需 AGPL 审查 |

## 深读项目

### 项目 1. deepseek-ai/dsh-superagent-prototype

- **GitHub**：https://github.com/deepseek-ai/dsh-superagent-prototype
- **固定提交**：`8c32a9dc5d72c033816c6a8110b37f40cf94fba4`（提交时间 2026-10-31T20:06:31+08:00）
- **API 基本信息**：Stars 22,482；Forks 2,730；Language TypeScript；License MIT；`updated_at=2026-11-11T23:09:19Z`；`pushed_at=2026-11-03T09:29:14Z`。
- **Release / issue / checks**：GitHub API 返回 0 releases、0 tags、0 issues、0 check-runs。这里的“0”只表示这些 API 列表没有条目，不能解释为无缺陷或 CI 通过。
- **一句话判断**：值得学的是“低注意力主动 Agent”的确定性控制面，而不是把 prototype 直接装入 Hermes。
- **解决的问题**：它替代“消息一来就由大模型自由决定并直接执行”的松散做法：Source 先把外部事件转成 Trigger；Policy gate 判断 explicit/inferred/not-admitted；主 Session 只做候选 assessment/routing；Engine 才是 Trigger、Decision、Ticket、Assignment 的唯一写者；外部副作用在事务内入 durable queue、commit 后执行。

#### 架构 / 实现与数据流

固定源码与 `docs/002-authorization.md`、`docs/007-architecture.md` 互证后的主流：

```text
GitHub / Feishu Source
  -> SourceRegistry / SourceContext
  -> Engine.receive(Trigger)
  -> Intake -> Eval candidate
  -> Policy.gate + MasterAssessor proposal
  -> Engine.decide()
  -> Ticket + Mandate + Assignment（同一事务）
  -> Effects.enqueue(kind,key,payload)（事务内）
  -> commit
  -> Effects dispatcher -> DshExecutor / Outbox / Sessions
  -> report/read-back -> Engine facts -> terminal / attention
```

`Runtime` 是 composition root；`src/core` 不做 I/O。Engine 将写模型拆成 Intake、Evals、Tickets、Assignments、Replies，依赖单向流动。Store 用 SQLite 持久化；Effects 将 assessment、launch、delivery、relay、notice、reply 建成按 kind/key 去重的队列。Policy 让内容只能形成 proposal，授权来自 Source policy、allowed list、admission table、accept mode 与 Mandate revalidation。

#### Repo tree 摘要

```text
dsh-superagent-prototype/
├── src/core/       # 无 I/O 的领域核心；Engine 是 Trigger/Ticket/Decision/Assignment 单写者
├── src/app/        # Runtime、SQLite Store、Effects、Settings、Prompts、HTTP 与 views
├── src/sources/    # GitHub/Feishu adapter，外部事件 <-> Trigger/Channel
├── src/executor/   # 每 Ticket 独立 Session/目录、worker slots、恢复与报告
├── src/client/     # 管理面板
├── docs/           # 哲学、领域、授权、执行、架构与部署说明
├── prompts/        # 主/worker/交接/assessment prompts
├── skills/         # GitHub 与 Feishu 的 DSH 专用 skills
├── tests/          # core/effects/policy/runtime/concurrency/panel 等 contract tests
├── package.json    # Node/DSH 版本、依赖、check 命令
└── pnpm-lock.yaml  # 锁定 npm 解析图
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/core/engine.ts` | 领域命令入口 | 所有 mutation 都包在 `repo.atomic`；对 caller 暴露 role-scoped Pick，而非整台 Engine |
| `src/policy.ts` | authorization / admission | `off/observe/auto`、规则全覆盖 assessment、Mandate revalidation、policy version |
| `src/app/effects.ts` | durable side-effect queue | kind/key upsert、generation、ordered lane、并发 limit、指数退避、Later 不计失败 |
| `src/app/store.ts` | SQLite 真相与事务 | domain repository、effect/outbox/kv；`afterCommit` 避免 rollback 后执行副作用 |
| `src/app/runtime.ts` | composition root | 加锁 state dir、构造部件、setup、恢复中断 Assignment、graceful shutdown |
| `src/executor/dsh.ts` | Ticket 执行适配 | 一 Ticket 一 Session/目录；launch/delivery 走 Effects；恢复与 worker slot |
| `docs/002-authorization.md` | 授权证据 | 外部文本只影响 decision，不能改变 permission；follow-up ownership 与 revalidation |
| `docs/007-architecture.md` | 实现索引 | 单写者、依赖规则、持久化表、effect backoff 与测试映射 |

#### 源码精读

**1）`Engine.receive`：外部事件只能通过单一事务入口进入领域真相。**

```ts
receive(trigger: Trigger): ReceiveResult {
  return this.repo.atomic(() => this.intake.receive(trigger))
}
```

函数签名很短，但边界很硬：Source adapter 不直接写 Ticket/Decision；Intake 在事务中完成去重、Thread 关联、fan-out 与 Eval 排队。这样 adapter 的网络重试不会变成多套写规则。

**2）`assessmentOutcome`：模型 assessment 是有 schema 的 proposal，accept 还需确定方向、规则命中和证据。**

```ts
export function assessmentOutcome(
  assessment: Assessment,
  settings: Pick<Settings, 'policy' | 'eval'>,
  strength: Strength,
): AssessmentOutcome {
  const enabled = settings.policy.rules.filter(rule => rule.enabled)
  const judged = assessment.rule_assessments
  if (judged.length !== enabled.length ||
      enabled.some(rule => !new Set(judged.map(x => x.rule_id)).has(rule.id))) {
    throw new Error('Exactly one assessment for every enabled rule is required')
  }
  if (!directionAllowed(assessment.direction))
    return { kind: 'ignore', audit: {}, reason: { code: 'directionUnsettled' } }
  if (strength === 'inferred' && settings.eval.mode !== 'auto')
    return { kind: 'ignore', audit: { would_accept: true }, reason: { code: 'observed' } }
  // 满足 matched rule + intent evidence 后才形成 accept
}
```

关键不是让模型给一个“accept”，而是冻结 enabled-rule denominator，要求每条规则恰好判断一次；`observe` 下即使模型认为应接也只记录 `would_accept`，不会启动工作。

**3）`Effects.enqueue`：副作用先与业务 mutation 一起 durable，再在 commit 后 dispatch。**

```ts
enqueue<K extends EffectKind>(kind: K, key: string, payload: EffectPayloads[K]): void {
  this.store.db.prepare(`INSERT INTO effect (kind, key, value, seq, due, since)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(kind, key) DO UPDATE
    SET value = excluded.value, generation = generation + 1,
        attempts = 0, error = '', due = excluded.due`)
    .run(kind, key, JSON.stringify(payload), ++this.seq,
         this.now(), new Date(this.now()).toISOString())
  this.kick()
}
```

同 kind/key 的 waiting effect 合并 payload，却保留原排队位置；generation 避免正在运行的旧 attempt 删除新 payload。它解决“数据库已提交但消息/worker 未启动”以及“网络重试造成重复副作用”两类常见故障窗。

**4）`Effects.attempt`：成功、Later、失败、shutdown 分开建模。**

```ts
private async attempt(kind: EffectKind, handler: Handler<never>, row: Row): Promise<void> {
  let failure: { error: unknown } | undefined
  try { await handler.run(JSON.parse(row.value) as never, row.key) }
  catch (error) { failure = { error } }
  const own = 'kind = ? AND key = ? AND seq = ? AND generation = ?'
  if (!failure) this.store.db.prepare(`DELETE FROM effect WHERE ${own}`).run(...ownRow)
  else if (this.stopped) return
  else if (failure.error instanceof Later)
    this.store.db.prepare(`UPDATE effect SET due = ? WHERE ${own}`).run(this.now() + handler.retry[0], ...ownRow)
  else
    this.store.db.prepare(`UPDATE effect SET attempts = attempts + 1, error = ?, due = ? WHERE ${own}`)
      .run(String(failure.error).slice(0, 1000), this.now() + delay, ...ownRow)
}
```

`Later` 表示“现在没有 worker slot / 被 pause”，不污染 failure count；普通错误做有界指数退避；shutdown 时保留行，下一次启动重试。这里仍没有外部副作用的通用 read-back，所以不能把“行删除”外推为所有业务效果都已验证。

#### 依赖分析与供应链风险

- `package.json`：直接 runtime 依赖只有 `proper-lockfile@4.1.2`、`zod@4.4.3`；但 peer/dev 图依赖大量 `@deepseek-ai/dsh-* 0.2.1-alpha.2`、`cordis 4.0.5-alpha.1`，并要求 Node `^22.19.0 || >=24`、DSH `^0.2.1-alpha.2`、pnpm 11.7.0。
- 供应链边界：核心并不是可独立运行的小库，实际行为依赖 alpha harness、Session、permission preset、webserver 与 UI packages；顶层 MIT 不替代这些 package 的逐件许可与制品 provenance 审计。
- 本机验证：`node --version` 为 v22.14.0，低于项目要求的 22.19；`pnpm install --frozen-lockfile` 在 corepack 拉取 `https://registry.npmjs.org/pnpm` 时失败，所以 typecheck/test/build **未运行，状态为 blocked/待核验**。不能拿仓库有测试或 0 check-runs 冒充本机通过。

#### 可复用经验

- **当外部消息可能启动长期工作时，应优先让模型只提交 typed proposal，再由宿主冻结规则集合、重验 authorization 与 policy revision，因为内容相关不等于有权执行；边界是 policy/store 本身必须是可信控制面。**
- **当事务提交后还需启动 worker、发消息或调用 API 时，应优先把 side effect 与 mutation 一起写入 durable generation-aware queue，再由 commit 后 dispatcher 执行，因为同步调用会留下不可恢复故障窗；边界是外部效果仍需 idempotency/read-back。**

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/transactional-effects-contract-v0/` 做纯 Python/SQLite 最小 POC：一个 `task` 表、一个 `(kind,key,generation)` 唯一的 `effect` 表；在同一事务创建 task+effect；注入三类故障（commit 前 crash、commit 后 handler crash、运行中同 key 更新）；验证不丢 effect、旧 generation 不删除新 effect、完成必须有 handler receipt。只用 synthetic 数据，不接消息、secret 或真实配置。

#### 风险边界

- **License**：仓库根与 API 为 MIT；依赖和 DSH 发布物仍需逐件审查。
- **维护活跃度**：repository 最近 push 为 2026-11-03，但无 release/tag/check-run；项目 README 明示 research prototype、非官方产品、可能有 bug，且公开版与内部实现/文章不完全相同。
- **安全风险**：可读 GitHub/飞书、启动 coding worker、执行 shell/prepare 命令并持有账号，属于高权 authority surface；loopback panel、policy 与 command shim 不能自动等价 OS sandbox。
- **局限 / 不适用**：依赖 DeepSeek Harness alpha 生态；记录“nothing deletes old records yet”，SQLite 历史无界增长；Source-specific GitHub/Feishu 耦合仍存在；没有本机构建/测试证据。

#### Skill 升格判断

**需二次验证。** “proposal/authority 分离”和“transactional durable effects”与现有 shared 自主学习/verification-first 规则高度重叠，今日不新建 repo 专属 Skill。先做 runtime POC，并与现有 `autonomous-learning/orchestrator-protocol`、`self-reflection-engine`、完成/receipt 约束去重；只有 conformance fixture 证明跨 Hermes/future-agent 均适用，才更新既有 class-level skill。

#### Hermes / shared hub 落地路径

1. 原始报告保留 `inbox/hermes/daily/2026-11-12-github-learning.md`；证据和 POC 只放 `runtime/hermes/`。
2. POC 建议接口：`admit(proposal, policy_revision) -> accepted|observe|denied`；`enqueue(kind,key,payload,generation)`；`dispatch() -> committed|retry|later|outcome_unknown`；`reconcile(effect_id) -> verified|needs_user`。
3. 若验证通过，更新既有 shared skill 的 contract / fixture，不复制 DSH 源码，不写 OpenClaw runtime；future-agent 只通过 agent-neutral schema 接入。
4. 任何配置、provider、cron、secret 或消息发送仍必须由目标 agent 自己的 adapter 与权限层处理，不能由 shared workflow 自动修改。

---

### 项目 2. deepseek-ai/DeepInfer

- **GitHub**：https://github.com/deepseek-ai/DeepInfer
- **固定提交**：`a679bb86ce36e883a98a97733492b686e5b9a08e`（提交时间 2026-11-03T15:31:40+08:00）
- **API 基本信息**：Stars 25,865；Forks 3,169；Language Python；License Apache-2.0；`updated_at=2026-11-11T23:26:46Z`；`pushed_at=2026-11-03T07:31:59Z`。
- **Release / tags / checks / issues**：0 releases、0 tags；固定 commit API 显示 4 个 CodeQL check-runs 均 success（Python/C++，2026-11-03 与 2026-11-08）。最近 issues API 返回的是活跃 PR，例如 #220 Trainium 支持、#104/#105/#106 修复；这证明仍在变动，不证明当前部署稳定。
- **一句话判断**：值得学的是异步 pipeline 的 pending/inflight/flush 与 request-local failure；GPU/NPU 推理 runtime 本身不适合直接接入 Hermes。
- **解决的问题**：相比同步 batch 推理，DeepInfer 把 CPU scheduling 与 device execution 重叠，并为 structured-output compile、多模态、MTP、KV cache 与多个并行策略建了明确状态；同时在 scheduler “没有 unfinished request”之后显式 flush 在途 ZOS 结果，避免 queue empty 被误判为 completed。

#### 架构 / 实现与数据流

```text
LLM.generate(prompts)
  -> tokenize / SamplingParams deepcopy
  -> LLMEngine.add_request()
     -> validate token/multimodal/SO
     -> SO pending compile（完成后才 enqueue）
     -> Scheduler waiting queue
  -> while has_unfinished_requests():
       LLMEngine.step()
       -> scheduler.schedule()
       -> Worker.execute_model_step()
       -> post-process previous async step
  -> scheduler empty
  -> flush_inflight_reqs()
  -> clone RequestOutput -> restore request order -> optional decode
```

公开版是 offline inference core；README 明确完整在线服务还需要 KV cache system、VE/Prefill/Decode disaggregation、DP replica load balancing。核心优化依赖 FlashMLA、DeepGEMM、DeepEP、TileKernels/TileLang 等 vendor/native components。

#### Repo tree 摘要

```text
DeepInfer/
├── deepinfer/entrypoints/ # LLM 用户入口
├── deepinfer/engine/      # LLMEngine、scheduler orchestration、profile server
├── deepinfer/worker/      # model runner、cache、CUDA graph、async step state
├── deepinfer/model_executor/ # 模型、采样、并行、TileLang/CUDA/Ascend kernels
├── deepinfer/structure_output/ # regex/JSON schema/EBNF matcher 编译与 mask
├── deepinfer/ve/          # 视觉 encoder / multimodal preprocess
├── deep_cluster/          # GPU/NPU/CPU 拓扑与部署辅助
├── csrc/                  # C++/CUDA 扩展
├── vendor/                # 6 个 git submodule，浅 clone 未初始化
├── examples/              # offline inference、benchmark、sweep、structured output
├── eval/                  # AIME/GPQA/HLE 评测
├── tests/                 # engine/model/worker/distributed/VE tests
└── requirements*.txt      # common / NVIDIA / Ascend 依赖
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `deepinfer/entrypoints/llm.py` | offline API | 批量加入请求、step 循环、显式 flush、按 request id 恢复顺序 |
| `deepinfer/engine/llm_engine.py` | 调度核心 | request admission、SO pending、scheduler step、worker dispatch、post-process/flush |
| `deepinfer/worker/worker.py` | 异步 worker | 当前 forward 与前一步 post-process 重叠，维护 step state |
| `deepinfer/sequence.py` | request state | Sequence / status / sampling 相关状态与输出生命周期 |
| `deepinfer/structure_output/so_matcher_builder.py` | 异步 grammar compile | 编译完成才让 request 进入 scheduler；失败局部终止 |
| `requirements.txt` / `requirements-nvidia.txt` | 供应链入口 | exact pins；NVIDIA lane 引入 torch 2.13.0+cu132、flash-attn-4 beta |
| `README.md` | 能力与缺口 | 只支持 V4.1-Flash、SM100/Ascend 950，且完整在线服务组件未包含 |

#### 源码精读

**1）`LLM.generate`：统一 admission 后由 engine 自行批处理。**

```python
def generate(
    self,
    prompts: str | list[str] | None = None,
    sampling_params: SamplingParams | list[SamplingParams] | None = None,
    prompt_token_ids: list[list[int]] | list[np.ndarray[np.int32]] | None = None,
    use_tqdm: bool = True,
    multi_modal_data: dict | list[dict] | None = None,
) -> list[list[RequestOutput] | str]:
    if prompts is None and prompt_token_ids is None:
        raise ValueError("Either prompts or prompt_token_ids must be provided.")
    for i in range(num_requests):
        self._add_request(prompt, sampling_params, token_ids, multi_modal_data)
    return self._run_engine(use_tqdm)
```

入口拒绝无 prompt；共享 SamplingParams 在 `_add_request` 里 deepcopy，避免不同 request 互相污染；所有请求先入 engine，让 scheduler 在显存约束下统一批处理。

**2）`LLMEngine.add_request`：pending 编译成功前不进入 ready queue。**

```python
def add_request(
    self, /, user_id: str, request_id: str,
    sampling_params: dict | SamplingParams | None,
    prompt_token_ids: np.ndarray[np.int32],
    multi_modal_data: dict | None = None,
    enqueue: bool = True,
) -> Sequence | None:
    if prompt_token_ids.size == 0:
        raise ValueError("prompt must not be empty")
    seq = Sequence(prompt_token_ids=prompt_token_ids, **sequence_args)
    so_pending = sampling_params.so_args is not None
    if so_pending:
        self.so_matcher_builder.submit(seq, sampling_params.so_args, _enqueue)
    elif enqueue:
        _enqueue(seq)
    return seq
```

Structured output matcher 可能昂贵或失败，所以 request 先是 pending；只有 callback `_enqueue` 才进入 scheduler。`get_num_unfinished_requests()` 还会把 matcher builder pending 数计入，防止 scheduler empty 时遗漏未完成 admission。

**3）`LLMEngine.step`：schedule 与 worker 执行分层，输出生命周期显式。**

```python
def step(self) -> np.ndarray[np.uint64]:
    with cpu_timer.record("schedule"):
        seq_metadata_list, scheduler_outputs = self.scheduler.schedule(
            self.sequence_metadata_pool
        )
        self.post_schedule(scheduler_outputs)
    request_outputs = self._execute_model_async_step(
        seq_metadata_list, scheduler_outputs
    )
    self.generate_step += 1
    return request_outputs
```

scheduler 产出 typed metadata / outputs；worker 执行后，输出由 deferred-release 管理。docstring 明确下一次 step 会自动释放 output，调用方要跨 step 保留必须 clone，这是一种清晰的 ownership contract。

**4）`LLM._run_engine` + `flush_inflight_reqs`：queue empty 后仍收口在途结果。**

```python
while True:
    unfinished = self.llm_engine.has_unfinished_requests()
    step_outputs = (
        self.llm_engine.step()
        if unfinished
        else self.llm_engine.flush_inflight_reqs()
    )
    for raw_output in step_outputs:
        output = RequestOutput.clone(raw_output)
        outputs[output.request_id].append(output)
    if not unfinished:
        break

def flush_inflight_reqs(self) -> np.ndarray[np.uint64]:
    request_outputs = self._run_workers("flush_inflight_reqs")
    self.deferred_release.collect_request_outputs(request_outputs)
    self.process_output(request_outputs)
    return request_outputs
```

`has_unfinished_requests()==False` 只说明 scheduler/SO pending 已空，不说明异步 worker 的上一步 post-process 已经吐完；所以还要走一次 flush。这一机制可直接抽象为 Agent workflow 的 `ready queue empty -> drain inflight -> verify terminal receipts`。

#### 依赖分析与供应链风险

- Common exact pins：`transformers==4.50.0`、`tokenizers==0.21.4`、`xgrammar==0.2.2`、`tilelang==0.1.15`、`tile-kernels==2.1.0`、`numpy==2.3.5`、`scipy==1.17.0`、`safetensors==0.8.0` 等。
- NVIDIA lane：`torch==2.13.0+cu132`（自定义 find-links）与 `flash-attn-4==4.0.0b34`；另有 6 个 git submodules（DeepEP/DeepGEMM/DeepSelect/FlashMLA 及 Ascend variants）。浅 clone 中 submodule 未初始化，不能把源码 checkout 当完整可构建 artifact。
- 供应链边界：native extension、CUDA 13/CANN 9.2、vendor commit、wheel index、GPU 架构共同决定运行制品；顶层 Apache-2.0 不能覆盖每个依赖与模型权重。
- 本机验证：系统 Python 是 3.11.15，而项目要求 Python 3.12；`python3 -m compileall` 在 PEP 695 `class EnvVar[T]` / `class Movable[T]` 处真实失败。这是**环境不兼容 / blocked**，不是上游 regression。未运行 build、pytest、模型或 benchmark。

#### 可复用经验

- **当异步 pipeline 将当前计算与前一步收口重叠时，应优先维护 typed step/generation state、把 pending 与 ready 分开，并在 ready queue 为空后显式 flush inflight，因为 queue empty 不等于业务 completed；边界是 crash 后仍需 durable reconciliation。**
- **当单请求需要 schema compile、图片预处理或其他可失败 admission 时，应优先让失败成为 request-local terminal 并计入 batch coverage，而不是拖垮整批或静默 drop；边界是局部失败仍必须可见和可重试。**

#### 可尝试实验（30 分钟）

复用项目 1 的 POC，增加 `pending -> ready -> inflight -> terminal` 四态与 `flush()`：投递 5 个 synthetic task，其中一个 compile_failed、两个在 queue empty 时仍 inflight；断言最终 coverage=5、每 task exactly-one terminal、未 flush 时 overall 不得 completed。无需 GPU、模型或第三方代码。

#### 风险边界

- **License**：顶层 Apache-2.0；vendor、wheel、模型权重与发布制品仍需分别核验。
- **维护活跃度**：2026-11-03 有 push，2026-11-11 仍有多个活跃 PR；固定 commit 有 4 个 CodeQL success，但没有 release/tag，不能视为稳定发布。
- **安全风险**：native CUDA/C++/NPU 构建、外部 wheel index、自动下载 Hugging Face checkpoint，具有高供应链、资源消耗和模型数据边界；不得在 Hermes cron 自动安装/下载。
- **局限 / 不适用**：只支持 DeepSeek-V4.1-Flash 与 NVIDIA SM100 / Ascend 950；公开版缺完整在线服务组件；README 的 4/64 GPU benchmark 本机待核验；当前主机 Python/HW 不满足运行条件。

#### Skill 升格判断

**暂不沉淀新 Skill。** pending/inflight/flush 模式已在既有 `deepseek-ai/DeepInfer` 项目卡与完成/receipt 类经验中出现；今天的新证据是更新 commit 与更明确的 request-local admission。应先合并到同一个 runtime POC / 既有 contract，避免重复 Skill。若 POC 对 cron、delegate_task、knowledge projection 三类 workflow 都通过，才考虑更新既有 shared class-level skill。

#### Hermes / shared hub 落地路径

- 在 `runtime/hermes/github-learning-poc/transactional-effects-contract-v0/` 与项目 1 合并验证，不引入 DeepInfer 依赖。
- 给 orchestrator status 增加 `coverage_total / pending / ready / inflight / terminal / flush_receipt`；`overall_status=completed` 仅在 terminal==coverage_total 且 inflight==0 时成立。
- 将 verifier 绑定到 `scripts/github_learning_orchestrator.py` 或通用 workflow engine 的 canonical status，而不是从 Markdown 关键词反推完成态。
- 验证后更新 existing shared skill/fixture；不复制 kernel、不安装模型、不改 provider/config/cron，不把 runtime 输出写 curated。

## 经验沉淀

1. **当外部内容可能触发 Agent 长期工作时，应优先把模型输出限制为 proposal，并由宿主按完整规则、scope、policy revision 和 final effect gate 授权，因为“模型认为该做”不是 authority；边界是规则本身也要版本化与测试。**
2. **当业务事务之后还有消息、worker 或 API 副作用时，应优先使用同事务 durable effect + generation + 幂等 key + commit 后 dispatcher，因为同步执行会形成 commit/effect 裂缝；边界是效果未知时必须 read-back 或 `needs_verification`。**
3. **当异步系统的 ready queue 为空时，应优先继续 drain/flush inflight 并核对 exactly-one terminal receipt，因为 scheduler 空、进程退出或 handler ACK 都不能证明业务完成；边界是 crash recovery 需要 durable state。**
4. **当单对象预处理或 schema compile 可失败时，应优先保留对象级 typed terminal 并继续其余 coverage，因为 fail-fast 会丢证据、静默 drop 会制造假完成；边界是 partial batch 不能投影为 completed。**
5. **当热门项目没有 release/tag、依赖 alpha/native runtime 或本机 prerequisite 不满足时，应优先固定 commit、保留 blocked 证据并只抽象机制，因为 Stars、README、CodeQL 或源码里存在 tests 都不是本机可运行证明。**

## 明日继续

1. 在 `runtime/hermes/github-learning-poc/transactional-effects-contract-v0/` 实现不依赖第三方包的 SQLite POC，覆盖 commit 前/后 crash、same-key generation replacement、Later、outcome_unknown、flush 与 exactly-one terminal。
2. 先搜索现有 shared skills 中 completion/receipt/orchestrator 规则并做去重矩阵；只有 POC 与三类 workflow fixture 都通过才提 shared skill 更新审核稿。
3. 对 dsh-superagent 在满足 Node >=22.19 且 registry 可达的隔离环境运行 `pnpm check`；当前保持 blocked，不自动修代理、不安装到 Hermes。

## 候选反哺

### Candidate Facts
- [ ] topic: Agent 主动工作应采用 proposal/authority 分离与 policy revision revalidation | evidence: `dsh-superagent-prototype@8c32a9d` 的 `src/policy.ts`、`src/core/engine.ts`、`docs/002-authorization.md` | 建议: update（先与现有 verification-first 去重） | 安全级别: medium
- [ ] topic: durable effect 应与 mutation 同事务写入并带 generation | evidence: `src/app/effects.ts` enqueue/attempt 与 `docs/007-architecture.md` | 建议: create candidate，需 POC | 安全级别: medium
- [ ] topic: async workflow queue empty 之后仍需 flush inflight | evidence: `DeepInfer@a679bb8` 的 `LLM._run_engine` / `LLMEngine.flush_inflight_reqs` | 建议: update 既有 pending/flush fact，不新建重复条目 | 安全级别: low

### Candidate Skills / Workflow
- [ ] 名称: transactional-effects-and-terminal-receipts（优先更新既有 orchestrator/verification contract） | 可复用场景: cron、delegate_task、知识库 projection、消息/API side effect | 是否建议 shared: yes-after-POC | 原因: 跨 agent 横切，但今日仅有上游源码证据，缺本地 conformance fixture
- [ ] 名称: request-local-admission-and-flush fixture | 可复用场景: parser/compile/OCR/LLM batch | 是否建议 shared: no-now | 原因: 先作为 runtime synthetic fixture，确认不与既有 completion contract 重复

### Candidate Open Questions
- [ ] 问题: 如何把 effect 的 `committed / outcome_unknown / verified` 与现有 reflection/orchestrator status 统一，而不让 Markdown 审计成为权威？ | reason: adaptation | priority: high
- [ ] 问题: dsh-superagent 的 effect row 成功删除后，各 Source 是否都有业务 read-back / idempotency 保证？ | reason: gap | priority: high
- [ ] 问题: DeepInfer 在真实 Python 3.12 + SM100/Ascend 950 上的 flush 与 SO failure fixture 是否通过？ | reason: gap | priority: medium

### 不应自动落地
- 不自动安装 dsh-superagent/DeepInfer，不下载模型或 native wheel，不运行第三方 prepare/hook。
- 不自动修改 Hermes/OpenClaw 配置、模型、provider、cron、secret 或消息渠道。
- 不复制 alpha/native 项目源码到 shared skill；不把本报告直接晋升 curated active fact。
- 不把 API 的 0 issues/releases/checks、CodeQL success 或 README benchmark解释为“无风险/生产可用”。
