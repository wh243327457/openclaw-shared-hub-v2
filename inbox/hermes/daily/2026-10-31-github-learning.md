---
type: case
status: draft
created: 2026-10-31
updated: 2026-10-31
domain: learning
tags: [github-learning, llm-inference, agent-harness, verification, hermes]
---

# 2026-10-31 GitHub 热门项目学习报告

> 执行者：Hermes；未调用 OpenClaw。  
> 查询与验证时间：2026-10-31 06:31–07:33（工具环境 UTC+09:00；GitHub 时间按 UTC 原样记录）。发现口径：GitHub Search API `created:>2026-10-01 stars:>100 sort:stars`；Stars/Forks/License/更新时间以 Repository API 快照为准。认证 `gh api` 命中限流后改用 GitHub REST API 的未认证 `curl`，真实响应已保存到 `runtime/hermes/github-hot-project-learning/evidence/2026-10-31/`。  
> 深读固定提交：`deepseek-ai/DeepInfer@553741557a57df44a46fb3ab72b6aafeaf945337`；`google-research/harness2@1cfe254e8d25b15f37048c3730134686abe60335`。  
> 证据范围：Repository/Search/Release/Issues API，README、docs、依赖声明、关键源码、本机 compile/test/demo。未运行 DeepInfer native build/GPU 推理；相关性能与生产数字只作为上游声明，标注待核验。

## 今日结论

**高吞吐推理与 Agent 自我改进表面不同，工程主线却一致：把异步流水线、可编辑 surface、预算、失败与完成态变成宿主可验证的显式状态；候选或请求只有经过 probe/执行证据、terminal flush、read-back 与边界审查后，才可进入 adoption、长期经验或对外结果。**

### 今日真实验证摘要

- **DeepInfer**：固定 `553741557...`；使用项目要求的 Python 3.12 执行 `compileall` 成功。宿主默认 Python 3.11 对 PEP 695 泛型语法真实报错，证明 runtime floor 不是文档装饰。未安装 CUDA 13 / Torch 2.13 CUDA / native vendor submodules，未跑 GPU、C++ scheduler、性能与模型推理。
- **Harness²**：固定 `1cfe254e...`；隔离 Python 3.12 venv 安装 `.[render]` 成功；`unittest discover` 实报 **5 tests passed / 0 failed**；credential-free demo `--k 1` 实报 **2 tasks completed / 0 failed、14 executions、16 editor calls**。
- 两仓 Releases API 与 `git ls-remote --tags` 都为空：没有可核验 release/tag。两仓历史很短，Stars 高不能替代稳定 release、跨平台 E2E 或生产验证。

## 项目速览

| 项目 | Stars | Forks | Language | License（GitHub API） | pushed_at（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 46,652 | 5,758 | Python | NOASSERTION | 2026-10-30T18:31:57Z | 高热但许可未识别，今日不迁移源码 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 24,487 | 2,953 | Python | Apache-2.0 | 2026-10-26T05:30:52Z | **深读：异步推理流水线与 request-local failure** |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 22,995 | 1,892 | JavaScript | MIT | 2026-10-18T20:20:24Z | canonical projection 工作流，10-19 已深读，不重复 |
| [google-research/harness2](https://github.com/google-research/harness2) | 21,502 | 2,134 | Python | Apache-2.0 | 2026-10-14T02:22:51Z | **深读：证据驱动 harness 递归与 Hermes substrate 缺口** |
| [openai/math](https://github.com/openai/math) | 17,135 | 1,929 | Lean | Apache-2.0 | 2026-10-30T00:35:38Z | 形式化数学资产，非今日主线 |
| [storytold/wordcraft](https://github.com/storytold/wordcraft) | 16,743 | 4,586 | Rust | Apache-2.0 | 2026-10-30T17:07:12Z | 文档工具候选，开放事项很多，待后续核验 |
| [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) | 13,469 | 1,321 | C | 未识别/None | 2026-10-29T02:30:54Z | 高权 GPU 修改面且许可不明，不自动运行 |

> 表中数值来自同一轮 Search API 快照；两项深读项目又用 Repository API 单独复核。`open_issues_count` 包含 PR，未当成纯 issue 数。顶层 License 不覆盖依赖、模型权重、数据集、第三方代码和发布制品。

## 深读项目

### 1. deepseek-ai/DeepInfer

- **一句话判断**：值得学的不是把 DeepSeek 专用 GPU runtime 搬进 Hermes，而是其 `schedule → forward → sample → delayed post-process → explicit flush` 异步状态机、request-local 失败隔离与严格配置 admission。
- **解决的问题**：替代同步 decode 中 GPU 等待 CPU scheduling/post-process 的空泡；并把 structured-output 编译、多模态失败、KV/state 延迟释放与 speculative decode 放到明确的 request/step lifecycle 中。
- **URL / API 快照**：https://github.com/deepseek-ai/DeepInfer ；**Stars: 24,487 / Forks: 2,953 / Language: Python / License: Apache-2.0**；`created_at=2026-10-16T07:47:23Z`，`updated_at=2026-10-30T22:13:05Z`，`pushed_at=2026-10-26T05:30:52Z`，API `open_issues_count=229`（含 PR）。
- **固定提交 / release**：`553741557a57df44a46fb3ab72b6aafeaf945337`，commit time `2026-10-25T19:59:27+08:00`；Releases 与 Tags 都为空。
- **来源交叉核验**：Repository/Release/Issues API；README；`doc/inference_deployment_qa.md`；requirements/pyproject/setup；entrypoint/engine/worker/model runner 源码；本机 Python 3.12 compileall。

#### 架构 / 实现与数据流

```text
prompts / token ids / sampling params
              |
      entrypoints/llm.py
      validate + enqueue Sequence
              |
       C++ Scheduler.schedule()
              |
   seq metadata + cache/state plan
              |
      worker.execute_model_step()
     /           |              \
forward(N)  post-process(N-1)  sample(N)
     \           |              /
      ZOS: retain WorkerStepState
              |
 next forward overlaps prior post-process
              |
 scheduler.process_outputs + RequestOutputPool
              |
 has work -> next step / no work -> flush_inflight_reqs
```

核心模块与依赖关系：

1. `entrypoints/llm.py` 是离线 API：把字符串/token IDs 变成 `Sequence`，循环 `LLMEngine.step()`，最后对 ZOS 在途结果调用 `flush_inflight_reqs()`。
2. `engine/llm_engine.py` 持有 tokenizer、C++ `Scheduler`、block/state managers、worker 与 deferred-release；每 step 先 schedule/clone，再异步执行模型与输出处理。
3. `worker/worker.py` 是流水线核心：当前 step 做 forward，随后收口前一步，再 sample 当前步；ZOS decode 把当前状态留到下一步，实现 CPU/GPU overlap。
4. `worker/model_runner.py` 把 input preparation、CUDA graph replay、forward、sampling 分开；`forbid_cuda_sync()` 明确禁止热路径意外同步。
5. README 明示本次开源只提供 offline inference；完整在线服务还缺 KV cache system、VE/Prefill/Decode disaggregation 与 DP load balancing。不能把公开 engine 外推为完整生产栈。

#### repo tree 摘要

```text
DeepInfer/
├── deepinfer/
│   ├── entrypoints/llm.py        # 离线批处理 API、enqueue、step/flush
│   ├── engine/llm_engine.py      # 请求、调度、cache/state、worker 生命周期
│   ├── worker/
│   │   ├── worker.py             # forward/post-process/sample 异步流水线
│   │   ├── model_runner.py       # input、CUDA graph、model forward、sample
│   │   └── cache_engine.py       # KV/state cache 设备层
│   ├── model_executor/           # 模型、MoE、并行、sampling、TileLang kernels
│   ├── structure_output/         # grammar 编译、matcher、mask
│   ├── ve/                       # 多模态处理
│   └── distributed/              # 分布式执行辅助
├── csrc/engine/                  # C++ scheduler、Sequence、输出池、ZOS
├── vendor/                       # DeepEP/DeepGEMM/FlashMLA 等 git submodules
├── examples/                     # offline inference、benchmark、sweep、SO
├── eval/                         # AIME/GPQA/HLE 评测脚本
├── tests/                        # engine/model/distributed/worker/VE tests
├── doc/inference_deployment_qa.md# EPD、LB、KV、async、SO 设计说明
└── requirements*.txt/setup.py    # 平台依赖与 native extension build
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `deepinfer/entrypoints/llm.py` | 离线入口 | 自动 batching；请求 ID；clone pooled output；无未完成请求后显式 flush ZOS |
| `deepinfer/engine/llm_engine.py` | engine 状态机 | C++ scheduler、KV/state block manager、deferred release、request-local SO/VE 状态、step/flush |
| `deepinfer/worker/worker.py` | 异步流水线 | `forward current → post previous → sample current`；ZOS decode 延迟 post-process |
| `deepinfer/worker/model_runner.py` | GPU 执行边界 | input metadata、CUDA graph、forward/sample 严禁同步、profile path |
| `deepinfer/structure_output/so_matcher_builder.py` | SO admission | 异步 grammar 编译；完成后再 enqueue，失败只终止对应 request |
| `requirements*.txt` / `setup.py` | 供应链与构建 | Python 3.12、Torch 2.13 平台轮、CUDA/NPU C++ extension、vendored kernels |

#### ⭐ 源码精读

1. `LLM.generate` 与 `_run_engine`：入口只负责规范化和提交，完成条件同时包含 scheduler 与在途 ZOS flush。

```python
def generate(
    self,
    prompts: str | list[str] | None = None,
    sampling_params: SamplingParams | list[SamplingParams] | None = None,
    prompt_token_ids: list[list[int]] | list[np.ndarray[np.int32]] | None = None,
    use_tqdm: bool = True,
    multi_modal_data: dict | list[dict] | None = None,
) -> list[list[RequestOutput] | str]:
    # normalize -> _add_request(...) for every input
    return self._run_engine(use_tqdm)

def _run_engine(self, use_tqdm: bool):
    while True:
        unfinished = self.llm_engine.has_unfinished_requests()
        step_outputs = (
            self.llm_engine.step()
            if unfinished
            else self.llm_engine.flush_inflight_reqs()
        )
        # clone pooled outputs before next step releases them
        if not unfinished:
            break
```

逻辑摘要：`scheduler empty` 不是完成证据；ZOS 可能仍持有前一步 `WorkerStepState`，所以必须 flush。`RequestOutputPool` 对象下一 step 会释放，调用方需要 clone。这一模式可迁移到 Agent 异步 tool/result pipeline，但 durability 仍需另做。

2. `LLMEngine.add_request`：统一做 request admission，并将 optional SO 编译变成“编译完成后 enqueue”的 request-local 状态。

```python
def add_request(
    self, /, user_id: str, request_id: str,
    sampling_params: dict | SamplingParams | None,
    prompt_token_ids: np.ndarray[np.int32],
    multi_modal_data: dict | None = None,
    arrival_time: float | None = None,
    extra: dict | None = None,
    enqueue: bool = True,
    chunk_checkpoints: list[int] | None = None,
) -> Sequence | None:
    # validate prompt/token range, build Sequence
    if sampling_params.so_args is not None:
        so_pending = True
    if enqueue:
        if so_pending:
            self.so_matcher_builder.submit(seq, sampling_params.so_args, _enqueue)
        else:
            _enqueue(seq)
    return seq
```

逻辑摘要：空 prompt/非法 token 会在 admission 被拒；SO 编译与主调度解耦。回调 `_enqueue` 会把 matcher abort 映射到 `FINISHED_SO_FAILED`，而不是拖垮全 engine。可迁移点是 `pending prerequisite → request-local terminal → only-ready enqueue`。

3. `LLMEngine.step`：调度、state clone、模型执行与输出处理被切成可计时的明确阶段。

```python
def step(self) -> np.ndarray[np.uint64]:
    with cpu_timer.record("schedule"):
        seq_metadata_list, scheduler_outputs = self.scheduler.schedule(
            self.sequence_metadata_pool
        )
        # clone/zero state and blocks, then post_schedule(...)
    request_outputs = self._execute_model_async_step(
        seq_metadata_list, scheduler_outputs
    )
    self.generate_step += 1
    return request_outputs

def flush_inflight_reqs(self) -> np.ndarray[np.uint64]:
    request_outputs = self._run_workers("flush_inflight_reqs")
    self.deferred_release.collect_request_outputs(request_outputs)
    self.process_output(request_outputs)
    return request_outputs
```

逻辑摘要：热路径不把“调用 worker 返回”直接当全部完成；在途 output 还要进入 deferred release 与 engine-specific process。Agent 工作流可复用 phase/step/flush 契约，但外部副作用还需 `outcome_unknown` 与 read-back。

4. `Worker.execute_model_step`：真正的 zero-overhead scheduling 是 typed previous-step state，而不是“加线程”。

```python
@torch.inference_mode()
def execute_model_step(
    self, is_prompt: bool, is_placeholder: bool,
    seq_metadata_list=None, scheduler_outputs=None,
) -> np.ndarray[np.uint64]:
    main_model_output = self.model_runner.execute_main_model(...)
    request_outputs = self._post_process_step(self.prev_step_state)
    sampler_output = self.model_runner.execute_sample(...)
    curr_step_state = WorkerStepState(...)
    if is_prompt or not envs.DEEPINFER_ZERO_OVERHEAD_SCHEDULING:
        request_outputs = np.concatenate([
            request_outputs, self._post_process_step(curr_step_state)
        ])
        self.prev_step_state = None
    else:
        self.prev_step_state = curr_step_state
    return request_outputs
```

逻辑摘要：当前 forward 与上一步 post-process 交叠；prompt/non-ZOS 当步收口，ZOS decode 显式保留状态。边界是状态只在进程内，crash 后没有 durable reconciliation。

#### 依赖分析与供应链风险

- `requirements.txt` 固定 `numpy==2.3.5`、`transformers==4.50.0`、`tilelang==0.1.15`、`tile-kernels==2.1.0`、`xgrammar==0.2.2` 等 21 个 Python 包；平台文件固定 `torch==2.13.0+cu132` + `flash-attn-4==4.0.0b34`，或 CPU Torch + `torch-npu==2.13.0rc1`。
- `setup.py` 构建 `deepinfer._C`，要求 C++20、CXX11 ABI、CUDA/NPU toolchain；`vendor/` 是 6 个未初始化的 git submodule（DeepEP/DeepGEMM/DeepSelect/FlashMLA 等）。仅 Python compileall 不覆盖这些 native bytes。
- 构建系统 `pyproject.toml` 要求 `torch>=2.7`，而平台 requirements 固定预发布/未来平台轮；环境与硬件兼容风险高。README 限定 Linux、GCC≥13、Python 3.12、CUDA 13 或 CANN 9.2，且硬件仅列 NVIDIA SM100 / Ascend 950。
- 本次没有执行 lockfile/advisory 审计；仓库没有统一 lockfile。不能声明“依赖安全”或“可复现构建”。

#### 可复用经验

- 当异步 pipeline 把当前计算与前一步收口重叠时，应优先保留 typed step/generation state 与 explicit flush，因为 queue/scheduler empty 不证明在途结果已完成；边界是进程崩溃仍需 durable reconciliation。
- 当可选编译、解析或预处理是主执行的前置条件时，应优先采用 request-local pending/failed terminal，并只把 ready 对象 enqueue，因为一条坏输入不应拖垮整批；边界是失败必须进入 coverage，不能静默 drop。
- 当热路径性能依赖“没有同步”时，应优先把 no-sync 约束做成代码级 guard 和定向测试，而不是注释，因为一个意外 device sync 会破坏整条 overlap；边界是 guard 不覆盖 native library 内部同步。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/async-step-flush-contract-v0/` 做纯 Python fixture：模拟 `forward(N) / finalize(N-1)`、pending prerequisites、request-local failed、queue empty 但 inflight 非空、显式 flush 与 crash-before-terminal，断言只有 `inflight==0 && terminal_receipts==admitted` 才能 completed。只用 synthetic state，不接模型/GPU/provider，不改 config/cron/skills/curated。

#### 风险边界

- **License**：GitHub API、`pyproject.toml` 与根 `LICENSE` 均为 Apache-2.0；衍生自 vLLM 的文件有 SPDX/derived 注记。模型权重、vendor submodules、CUDA/CANN、benchmark 数据与运行制品仍需逐项审查。
- **维护活跃度**：仓库 2026-10-16 创建，固定 head 2026-10-25；2026-10-30 仍有 PR 活动，但无 tag/release，稳定升级与回滚面不足。
- **安全风险**：`trust_remote_code` 是可配置项；首次运行可下载 Hugging Face 模型；native extension、GPU kernels、共享内存、ZeroMQ、HTTP profile server 都扩大执行面。不要在默认 Hermes runtime 自动安装或运行。
- **局限/不适用**：仅支持 DeepSeek-V4.1-Flash 与两类新硬件；公开版本是 offline core，不含完整在线 KV/cache/LB/EPD 服务；上游文档中的 155T tokens/day、$/GPU-hour 和吞吐收益本机均**待核验**。
- **本机覆盖**：Python 3.12 compileall 通过；native build、submodule、GPU/NPU、distributed、model download、performance、structured-output runtime 均待核验。

#### ⭐ Skill 升格判断

**需二次验证**。只抽象 `typed step state + pending admission + request-local terminal + explicit flush`，不迁移 DeepInfer runtime、kernels、模型或部署参数。该模式与既有 completion/receipt、orchestrator protocol、verification-first 候选高度重叠，应更新已有 class-level contract 而非新建 DeepInfer 专属 Skill。

#### ⭐ Hermes / shared hub 落地路径

- Hermes runtime POC：`runtime/hermes/github-learning-poc/async-step-flush-contract-v0/`。
- POC 若能复现当前 orchestrator 假完成，再提议更新：
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：增加 `admitted/pending/inflight/flushed/terminal` invariant；
  - `capabilities/skills/foundation/verification-first/SKILL.md`（若现有 canonical 路径确认存在）：增加 queue-empty ≠ completed fixture；
  - `scripts/github_learning_orchestrator.py`：status 写入前核报告、知识库 projection 与 audit terminal receipt。
- 不自动改 Hermes provider/model/config，不把 GPU 环境变量写进 shared，不把 DeepInfer 源码复制进 skill。

### 2. google-research/harness2

- **一句话判断**：Harness² 将“改 Agent”限制为 `proposal → validation → probe → contrast → adoption → reflection`，而当前 open issue #117 又直接给出 Hermes substrate 草案，因此最有价值的是建立 Hermes adapter 的 conformance gate，而不是自动开启递归自修改。
- **解决的问题**：替代“读失败日志后直接改全局 prompt/skill”的旧做法；task-level 同任务探测候选，harnessing-level 只保存 adopted harness 与 evidence-supported lesson，并让任务按 domain 顺序读取早期经验。
- **URL / API 快照**：https://github.com/google-research/harness2 ；**Stars: 21,502 / Forks: 2,134 / Language: Python / License: Apache-2.0**；`created_at=2026-10-06T21:48:11Z`，`updated_at=2026-10-30T22:23:54Z`，`pushed_at=2026-10-14T02:22:51Z`，API `open_issues_count=146`（含 PR）。
- **固定提交 / release**：`1cfe254e8d25b15f37048c3730134686abe60335`，commit time `2026-10-13T21:22:49-05:00`；Releases 与 Tags 都为空。
- **来源交叉核验**：Repository/Release/Issues API；README；`docs/EXPERIMENTS.md`；`dependencies/PINNED.md`/README；core/substrate/tests；本机隔离安装、完整仓库现有 test module 与 demo。

#### 架构 / 实现与数据流

```text
benchmark task + source + base harness
                 |
           k reference executions
                 |
       +---------+----------+
       |                    |
 parallel recursion    sequential recursion
 k INV + k DOM         each round: INV + DOM
 candidate probes      probe -> compose c_t
 k compositions        carry evidence/harness
       |                    |
       +------ final rollouts -----+
                                  v
                    delivered-artifact filter
                    deterministic anonymous IDs
                                  |
                          final adoption
                                  |
                   evidence-bound reflection
                                  |
               per-domain ordered Library.add()
                                  |
                     later tasks read earlier only
```

核心模块与状态流：

1. `tree.SurfaceSpec` 将可编辑面参数化：always-on、skills、scripts、subagents、plugins/hooks；off-surface path、未触发 skill、坏 frontmatter、超长 always-on 与缺脚本引用都会被 deterministic validate 拒绝。
2. `recursion._run_stage` 建 evidence、调用 proposer、最多修复一次 invalid proposal；失败继承 fallback harness，同时记录 `fell_back/error/attempts/usd`。
3. parallel 模式探索宽度；sequential 模式探索深度。`Ledger.assert_identity()` 强制 `R=4k/P=3k` 且先检查 duplicate labels，避免覆盖候选后仍虚报预算完整。
4. `selection` 只纳入 delivered、可渲染 artifact；匿名 ID 由 task/k/mode 稳定生成。adoption 后才 `_distil`；`Library.add()` 只有 `cue/lesson/evidence` 完整才保存经验。
5. README/docs 明示 executor 网络不受限、Codex sandbox disabled；公开 benchmark rubric 可被联网 executor 获取，必须用宿主网络策略隔离，不能靠 prompt。

#### repo tree 摘要

```text
harness2/
├── harness2/
│   ├── core/
│   │   ├── recursion.py       # parallel/sequential proposal-probe-compose
│   │   ├── tree.py            # editable SurfaceSpec、validate、diff、diversity
│   │   ├── selection.py       # artifact filter、匿名 adoption、reflection
│   │   ├── library.py         # per-domain adopted harness + evidence lesson
│   │   ├── ledger.py          # R=4k/P=3k budget identity
│   │   ├── schedule.py        # task/domain ordering、resume orchestration
│   │   └── context.py/spec.py # evidence layout 与 benchmark adapter protocol
│   ├── substrate/             # OpenCode / Codex adapters；Hermes 尚未合入
│   ├── benchmarks/            # JobBench / LAB / WorkBuddy adapters
│   └── cli/                   # run/judge/report/setup/check/demo/bridge
├── docs/                      # benchmark、setup、experiment/reproducibility
├── dependencies/              # immutable upstream pins 与 dataset说明
├── third_party/               # runners、patches、licenses、provenance
├── tests/test_workflow.py     # resume/budget/evidence/library regression
└── pyproject.toml             # core 零依赖；render/bridge optional extras
```

#### 关键源码文件

| 路径 | 用途 | 关键内容摘要 |
|---|---|---|
| `harness2/core/recursion.py` | 候选实验 | evidence build、proposal repair、parallel/sequential probes、fallback 与 deterministic ledger order |
| `harness2/core/tree.py` | editable surface gate | path containment、allowed files、skill/subagent/hooks/scripts validation、diff/diversity |
| `harness2/core/selection.py` | adoption/reflection | dropped artifact、匿名 ID、选择、adoption evidence、experience distillation |
| `harness2/core/library.py` | 持续经验 | 只接收完整 evidence lesson；保存 adopted full tree；per-domain ordered context |
| `harness2/core/ledger.py` | 预算闭包 | 固定 rollout/session identity，duplicate label 先于数量检查 |
| `harness2/substrate/{base,codex,opencode}.py` | host adapter | SurfaceSpec、materialise、execute、trajectory；Hermes adapter 仍是 issue #117 草案 |

#### ⭐ 源码精读

1. `_run_stage`：模型只提出 candidate；确定性 validator 决定是否接受，非法候选只有一次有证据的修复机会。

```python
def _run_stage(
    *, label: str, dim: str, job: str,
    fallback: harness_tree.Tree,
    adapter: BenchmarkAdapter, prop: Proposer,
    ctx_dir: Path, task_id: str,
    rollouts: Sequence[RunView],
    harness_dir: Path | None,
    library_dir: Path | None,
    pool=(), decisions=None,
) -> Stage:
    # context.build(...) -> mission
    for attempt in range(1, STAGE_ATTEMPTS + 1):
        reply = prop.call(..., harvest="context/harness")
        new = harness_tree.read_tree(surface, reply.workspace, rejected=rejected)
        kept, err = _accept_tree(surface, adapter, new, fallback, label)
        if not err:
            return Stage(label=label, tree=new, ...)
    return Stage(label=label, tree=dict(fallback), fell_back=True, error=err[:400])
```

逻辑摘要：proposal 与 activation 分离；off-surface 文件、空 tree、adapter invariant、grader leakage 都可拒绝。边界是 proposer session 仍有其 substrate 权限，隔离要由宿主实施。

2. `run_parallel` / `run_sequential`：宽度与深度是两种不同 evidence topology，但都以真实 rollout 收口。

```python
def run_parallel(task_id: str, k: int, base, *, adapter, prop, work_dir, ...):
    specs = [(f"{d.lower()}{i}", d, i)
             for i in range(1, k + 1) for d in ("INV", "DOM")]
    stages = parallel_map(_run_stage, specs)
    candidate_rollouts = _roll_many(...)
    aggs = parallel_map(_run_stage, [f"agg{i}" for i in range(1, k + 1)])
    result.finals = [stage.label for stage in aggs]
    ledger.assert_identity()
    return result

def run_sequential(...):
    for t in range(1, k + 1):
        # propose INV/DOM from current harness + accumulated history
        # probe both, compose c_t, then carry c_t to next round
        current_harness = comp.tree
    ledger.assert_identity()
    return result
```

逻辑摘要：parallel 候选共享 base evidence 后独立 compose；sequential 把前轮 harness/evidence 带入后轮。两者都不是“模型说改好了”就完成，而是 proposal 和 rollout 成对出现。

3. `Ledger.assert_identity`：预算不只是计数，还必须防 label overwrite。

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
    raise BudgetError(...)
```

逻辑摘要：重复 label 即使让 R/P 数量“正确”，也会因实际 candidate 被覆盖而失败。可迁移到多 Agent fan-out：冻结 denominator 后，还要验证 immutable unique identity。

4. `Library.add`：只有 adopted 且 evidence 完整的经验能进入后续任务上下文。

```python
def add(
    self, task_id: str, harness: harness_tree.Tree, *,
    why: str = "", label: str = "", run_id: str = "",
    experience: dict | None = None,
) -> Path | None:
    if not has_experience(experience):
        return None
    context.assert_tree_has_no_grader_verdicts(harness)
    harness_tree.write_tree(self.surface, harness, d / "harness", stubs=False)
    (d / "EXPERIENCE.md").write_text(...)
    self.rebuild_index()
    return d
```

逻辑摘要：完整条件是 `cue + lesson + evidence`，不是非空 prose；保存 full adopted tree 而非只存摘要。边界是 Library 是实验 run 内经验，不等于 shared curated truth。

#### 依赖分析与供应链风险

- core `dependencies=[]`，Python 要求 `>=3.12,<3.14`；optional `render` 使用 `openpyxl`/`python-pptx`，`bridge` 固定 `litellm[proxy]==1.95.0`、`fastapi==0.139.2`、`google-auth==2.56.3`。
- `dependencies/PINNED.md` 固定 JobBench、WorkBuddy、LAB、OpenCode commits，并分发 patches/derived runners；这比 moving branch 好，但同时扩大到 Node/Bun、Docker、GCloud、benchmark datasets 与模型凭据。
- WorkBuddy 采用 custom Tencent license，并有 EU territorial limitation；顶层 Apache-2.0 不能覆盖 third_party、benchmark 或 dataset。
- 本机只安装 `.[render]`，没有安装/审计 `bridge`、benchmark download、Node/Bun、Docker、GCloud 或模型/provider graph；不能声称完整供应链安全。

#### 可复用经验

- 当 Agent 要自动改 prompt、memory、skill 或 scripts 时，应优先执行 `proposal → deterministic validation → task-local probe → contrast → adoption → reflection`，因为生成候选不等于获得发布权；边界是 probe 任务必须代表真实 workload。
- 当并发候选共享 namespace 与预算时，应优先冻结 denominator、使用 immutable unique labels，并在并发结束后确定性记账，因为 duplicate label 可在总数正确时覆盖真实候选。
- 当经验准备进入后续任务或共享层时，应优先要求 cue、lesson、evidence、adoption identity 与完整 source tree，再经过治理 promotion，因为非空总结与一次高分不是长期事实。
- 当 benchmark executor 能访问公网或关闭 sandbox 时，应优先在宿主 egress/OS 层限制访问并隔离凭据，因为 prompt 中的“不要看答案”不是 enforcement；边界是网络限制也不消除本地数据泄漏。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/hermes-surface-conformance-v0/` 建 fake `HERMES_HOME` fixture，只验证 issue #117 草案的 `SOUL.md / skills/<name>/SKILL.md / scripts/` materialise、off-surface rejection、skill name/trigger、trajectory JSONL parser 与 no-secret environment allowlist；不执行 paid benchmark、不调用 provider、不安装 OpenCode/Codex、不写 `~/.hermes`。

#### 风险边界

- **License**：顶层 Apache-2.0；third-party 与 dataset 各自许可，WorkBuddy 有 custom/EU 限制。不可把整个依赖树当 Apache-2.0。
- **维护活跃度**：仓库 2026-10-06 创建，固定源码 2026-10-14，2026-10-30 仍有 PR/issue 更新，但无 release/tag；快速增长不等于稳定 API。
- **安全风险**：README 明示 executor 网络 unrestricted，Codex sandbox disabled；公开 benchmark rubric 可在线获取。模型凭据、GCloud ADC、Docker 和下载 patches 都是高权面。
- **局限/不适用**：当前正式 substrate 只有 OpenCode/Codex；Hermes 支持仍是 open issue #117 的提案，草案声称“unit-tested but 未跑 paid benchmark”，本次未取得其 draft code，真实实现**待核验**。
- **本机覆盖**：现有 5 个 workflow tests 与 credential-free demo 通过；未运行真实模型、benchmark、judge、bridge、Docker、跨平台与付费 rollout。

#### ⭐ Skill 升格判断

**需二次验证**。Propose–Probe–Compose 与 evidence-bound adoption 可直接作为既有 autonomous-learning workflow 的候选增量；Hermes substrate 不能直接升格，因为 #117 尚未合入且 paid benchmark 未验证。完整 Harness² runtime **暂不沉淀**，不自动启用 self-modification。

#### ⭐ Hermes / shared hub 落地路径

- runtime POC：`runtime/hermes/github-learning-poc/hermes-surface-conformance-v0/`。
- 若 conformance fixture 通过并完成真实 Hermes isolated rollout，再提议更新：
  - `capabilities/skills/autonomous-learning/orchestrator-protocol/SKILL.md`：加入 proposal/probe/adoption/release 分层；
  - `capabilities/skills/autonomous-learning/self-reflection-engine/SKILL.md`：只反思 adopted + evidence-closed candidate；
  - `capabilities/skills/research/github-hot-project-learning/SKILL.md`：候选 Skill 先 runtime probe，再进入 shared governance。
- Hermes adapter 应保持薄层：`SurfaceSpec`、fake-home materialise、JSONL trajectory、preflight；共享逻辑放 agent-neutral deterministic core。禁止把 OpenCode/Codex 路径或凭据写死进 shared。

## 经验沉淀

1. **当异步 pipeline 把当前工作与前一步收口重叠时，应优先使用 typed generation/step state、active/inflight count 与 explicit flush，因为 queue empty、scheduler 返回或进程 exit 都不能证明在途结果完成；边界是 crash 后还需 durable reconciliation。**
2. **当模型要修改 prompt、memory、skill、script 或其他行为面时，应优先把输出当 proposal，经过确定性 surface validation、真实 probe、contrast 与 adoption 才允许发布，因为候选质量与发布权限是两件事；边界是 probe coverage 必须公开。**
3. **当多个候选并发探索时，应优先冻结 coverage denominator、使用不可重复 identity 并在 barrier 后确定性记账，因为总数正确仍可能掩盖 label overwrite、静默 drop 与 fallback；边界是跨进程还需 lock/lease。**
4. **当可选编译、解析或预处理失败时，应优先给单对象 typed terminal 并只让 ready 对象进入主队列，因为一条坏输入不应拖垮整批，也不能被静默忽略；边界是失败必须计入最终 coverage。**
5. **当经验要进入后续任务或跨 Agent shared 层时，应优先要求 adopted identity、cue、lesson、evidence 与 source pointer，再走评分/去重/脱敏/审查，因为一次实验总结不是长期真相。**
6. **当 benchmark 或 Agent executor 可联网、持有凭据或关闭 sandbox 时，应优先使用宿主 egress、OS 隔离与 include-only environment，因为 prompt/Skill prose 不是安全 enforcement。**

## Hermes/shared hub 落地总表

| 候选 | 首个落点 | 目标能力 | 当前判断 | 自动执行边界 |
|---|---|---|---|---|
| async step/flush contract | `runtime/hermes/github-learning-poc/async-step-flush-contract-v0/` | orchestrator/completion receipt | 需二次验证 | 不接 GPU/provider，不改 cron/config |
| Hermes surface conformance | `runtime/hermes/github-learning-poc/hermes-surface-conformance-v0/` | thin host adapter + deterministic core | 需二次验证 | fake HOME；不写 `~/.hermes`，不跑 paid benchmark |
| evidence-bound adoption | 先更新既有 autonomous-learning POC | proposal/probe/adoption/promotion | 可抽象，仍需治理 | 不自动写 curated，不自动发布 Skill |

## 明日继续

1. **最小动作**：实现 `async-step-flush-contract-v0` 的 synthetic fixture，先复现“queue empty 但 inflight 未 flush”与“request prerequisite failed 但总任务误 completed”两类错误。
2. 核验 Harness² issue #117 后续是否出现 PR/commit；若仍只有 prose，继续保持“待核验”，不自行把草案当上游实现。
3. 对当前 GitHub learning orchestrator 做只读差距检查：报告 audit 通过后，知识库 copy 是否验证 exact hash/frontmatter/index；只出修订建议，不自动改 cron/provider/config。

## 候选反哺

### Candidate Facts

- [ ] topic: 异步流水线必须显式 flush 在途状态后才能 completed | evidence: `DeepInfer@5537415` 的 `LLM._run_engine`、`Worker.prev_step_state`、`flush_inflight_reqs` 与本机 Python 3.12 compileall | 建议: create candidate / 与 completion-receipt 去重 | 安全级别: low
- [ ] topic: evidence-bound Agent harness adoption | evidence: `harness2@1cfe254e` 的 recursion/selection/library/ledger + 本机 5 tests 与 demo 2/2 | 建议: update autonomous-learning candidate | 安全级别: medium
- [ ] topic: Harness² Hermes substrate 仍未进入固定源码 | evidence: open issue #117（2026-10-30 API 快照）与固定 repo tree 只有 codex/opencode | 建议: stale/open-question tracking，不创建 active fact | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: async-step-flush-contract-v0 | 可复用场景: cron、subagent、tool pipeline、provider callback 收口 | 是否建议 shared: yes-after-fixture | 原因: agent-neutral 且与 completion/orchestrator 横切；先更新既有 skill，避免重复
- [ ] 名称: hermes-surface-conformance-v0 | 可复用场景: Hermes host adapter、Skill/脚本 materialise 与 first-turn behavior | 是否建议 shared: no-now | 原因: 上游实现未合入，先留 Hermes runtime POC
- [ ] 名称: evidence-bound-adoption | 可复用场景: prompt/skill/harness 自动优化 | 是否建议 shared: yes-after-governance | 原因: 高权自修改面，必须有 proposal/probe/adoption/release 与人工/策略门禁

### Candidate Open Questions

- [ ] 问题: DeepInfer 的 ZOS/pending/flush 契约在进程崩溃后如何恢复？ | reason: gap | priority: high
- [ ] 问题: Harness² issue #117 的 Hermes adapter 是否已有可公开 PR、conformance tests 与 credential-isolation 结果？ | reason: gap/stale | priority: high
- [ ] 问题: GitHub learning 知识库 projection 是否应绑定 inbox report hash、frontmatter gate 与 index read-back？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动修改 Hermes/OpenClaw 配置、模型、provider、cron、secret 或网络策略。
- 不安装 DeepInfer、模型权重、CUDA/NPU vendor runtime，不运行 GPU benchmark。
- 不运行 Harness² paid benchmark，不关闭 sandbox，不向 executor 暴露宿主凭据。
- 不直接写 curated active fact；本节只是二轮审计候选。
- 不复制许可未识别项目源码，也不把顶层 Apache-2.0 外推到第三方依赖/数据集。
