# 2026-10-29 GitHub 热门项目学习日报

> 执行者：Hermes（本任务未调用 OpenClaw）  
> 研究窗口：2026-10-29 07:30–07:36 JST；GitHub 时间字段按 UTC 原样记录。  
> 发现口径：GitHub Trending 日榜 HTML（15 个条目）+ Search API `created:>=2026-10-01 stars:>100 sort:stars`；Stars、Forks、License、时间和提交均由 `gh api` 实时读取。  
> 深读固定源码：`deepseek-ai/DeepInfer@553741557a57df44a46fb3ab72b6aafeaf945337`、`Jakeschincariol/replica-skill@77c9436fb3d18c3d58169efb8caf4fe906b0dc51`。

## 今日结论

今天两类项目共同说明：**性能调度和 Agent Skill 工作流都不应把“更快/更多自动化”直接当成正确性；应把可变策略包在严格配置解析、canonical artifact、可执行 gate、失败终态与真实 read-back 之内。** DeepInfer 的可迁移点是异步流水线仍保留 step identity、flush 和 fail-local terminal；Replica 的可迁移点是把长 prompt 流程落为稳定中间件与确定性检查器，但其“宣称的安全边界”还没有被所有 parser/effect path 强制。

## 项目速览

API 查询基准：2026-10-29 07:30–07:36 JST。`NOASSERTION` 表示 GitHub License API 未识别，不等于无许可。

| 项目 | Stars | Language | License（GitHub API） | pushed_at | 速览判断 |
|---|---:|---|---|---|---|
| [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | 4,983 | TypeScript | Apache-2.0 | 2026-10-28T20:06:59Z | 今日 Trending；10 月 26 日已深读，不重复。 |
| [elayadesign/ai-design-skills](https://github.com/elayadesign/ai-design-skills) | 11,030 | 未标注 | MIT | 2026-10-27T16:02:10Z | Skill 合集，只列候选，不执行安装器。 |
| [obra/superpowers](https://github.com/obra/superpowers) | 307,386 | Shell | MIT | 2026-10-23T03:48:57Z | 已有项目卡，避免重复。 |
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | 47,869 | Python | Apache-2.0 | 2026-10-28T18:01:08Z | 昨日已深读；更新很快，结论需固定提交。 |
| [macro-inc/macro](https://github.com/macro-inc/macro) | 5,384 | Rust | AGPL-3.0 | 2026-10-28T22:33:15Z | 今日 Trending；AGPL 和快速 churn 需专项审查。 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 40,625 | CSS | MIT | 2026-10-28T14:52:03Z | 设计 Skill，今日不安装。 |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 92,494 | Rust | Apache-2.0 | 2026-10-28T22:23:28Z | 昨日已深读，避免重复。 |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 8,040 | TypeScript | Apache-2.0 | 2026-10-28T18:56:38Z | 10 月 26 日已深读，避免重复。 |
| [nightly-labs/openbot](https://github.com/nightly-labs/openbot) | 3,186 | TypeScript | NOASSERTION | 2026-10-28T22:34:19Z | 10 月 27 日已深读；实际根许可曾核为 noncommercial。 |
| [expo/skills](https://github.com/expo/skills) | 3,541 | Shell | MIT | 2026-10-28T20:08:40Z | Skill 分发候选；今日不安装。 |
| [ruvnet/RuView](https://github.com/ruvnet/RuView) | 100,974 | Rust | MIT | 2026-10-28T18:14:24Z | 今日 Trending；无线感知涉及隐私与误用面。 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 23,901 | Python | Apache-2.0 | 2026-10-26T05:30:52Z | Search API 高热新仓；异步推理调度、结构化输出和配置 gate，深读 1。 |
| [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) | 6,264 | Python | MIT | 2026-10-03T12:07:53Z | Skill-as-workflow + deterministic gates；法律/安全承诺与实现差距值得核验，深读 2。 |

## 深读项目

### 1. deepseek-ai/DeepInfer

- **链接**：https://github.com/deepseek-ai/DeepInfer
- **固定源码提交**：`553741557a57df44a46fb3ab72b6aafeaf945337`（verified commit；2026-10-25T11:59:27Z）。
- **GitHub API**：Stars **23,901**；Forks **2,842**；Language **Python**；License **Apache-2.0**；`created_at=2026-10-16T07:47:23Z`；`updated_at=2026-10-28T22:26:05Z`；`pushed_at=2026-10-26T05:30:52Z`；API `open_issues_count=220`（含 PR）。
- **Release / tags**：Releases API 与 Tags API 均为空，**没有可核验 release/tag**；项目版本文件为 `pyproject.toml 0.1.0`，不能把 main 当稳定发行版。
- **一句话判断**：值得学的不是面向特定加速器的 kernel，而是“**host admission 严格化 + CPU/GPU 双流水线 + pending/flush/failed request 终态 + 结构化输出异步编译边界**”。
- **解决的问题**：替代同步 `schedule → forward → sample → post-process` 中 GPU 等 CPU 的空洞，以及宽松环境变量、同步 grammar 编译、无请求级失败隔离造成的隐性错误；但开源版只提供 offline inference core，不包含完整在线服务、KV cache system 与跨副本 load balancer。

#### 证据交叉核验

1. **README**：明确支持异步 scheduling、batch-invariant、deterministic sampling、structured outputs；只支持 DeepSeek-V4.1-Flash、NVIDIA SM100 / Ascend 950；完整服务仍缺 KV cache、VE/P/D disaggregation 和 DP load balancing。
2. **部署 Q&A**：解释 zero-overhead pipeline、结构化输出的异步 compile/runtime split、Wide-EP、KV storage 与真实生产架构；其中 155T tokens/day、US$38/GPU-hour 等是上游声明，本机未复现，标 **待核验**。
3. **源码**：直接读取 `entrypoints/llm.py`、`engine/llm_engine.py`、`worker/worker.py`、`environ.py`、`structure_output/compiler.py`、`matcher.py` 与 C++ scheduler。
4. **PR #218 / fixed commit**：合并 strict boolean parsing；本机 Python 3.12 probe 验证 `TRUE/FALSE` 可解析，`yes/2` 明确报错。
5. **Actions / checks**：固定 head 有 4 个 CodeQL check-runs success；main 的 Push/Scheduled workflows success。它们是静态分析面，不等于 GPU build/test/benchmark 全绿。
6. **Security endpoints**：public repository advisories 返回 0；Dependabot endpoint 404/不可读，不能推导无漏洞。

#### 架构 / 实现与数据流

```text
LLM.generate(prompts, SamplingParams)
        │ tokenize + deepcopy per request
        ▼
LLMEngine.add_request
  strict token/range checks
  structured-output compile pending ─────┐
        │ ready callback                  │ async CPU pool
        ▼                                 │ timeout/abort → request-local failed
C++ Scheduler waiting/running/block mgr ◄─┘
        │ schedule(N+1)
        ▼
Worker.execute_model_step
  forward(current)
  post_process(previous)   # ZOS decode: overlap CPU/GPU
  sample(current)
  pre_sampler_sync / deferred release
        │
        ├─ prompt/non-ZOS → post-process now
        └─ ZOS decode     → retain WorkerStepState for next step
        ▼
LLM._run_engine clones pooled outputs
        │ no unfinished scheduler/SO work
        └─ flush_inflight_reqs() → decode same request order
```

关键边界：scheduler 与 model runner 不靠 prose 表达状态；`SequenceStatus`、pending grammar future、pooled output ownership 与 `flush_inflight_reqs()` 都是显式对象。异步只改变阶段重叠，不应改变请求身份与最终输出排序。结构化输出编译失败只判死本请求，不应拖垮整个 batch。

#### Repo tree 摘要

固定提交有 **348 个 tracked files**；根目录与 tracked tree 真实读取如下：

```text
DeepInfer/
├── deepinfer/
│   ├── entrypoints/             # offline LLM 高层入口
│   ├── engine/                  # admission、scheduler 编排、stats/profile
│   ├── worker/                  # GPU step、ZOS pipeline、cache/runtime
│   ├── model_executor/          # model/layers/sampler/TileLang kernels
│   ├── structure_output/        # xgrammar compile/matcher/mask/rollback
│   ├── ve/                      # 多模态处理与 shared pool
│   ├── distributed/             # shared-memory broadcast
│   └── hugging_face/            # config/tokenizer/weights adapter
├── csrc/engine/                 # C++ Scheduler、Sequence、BlockManager、pybind
├── deep_cluster/                # accelerator discovery / NUMA binding
├── vendor/                      # DeepEP/DeepGEMM/FlashMLA 等 git submodules
├── examples/                    # offline、benchmark、sweep、YOCO equivalence
├── eval/                        # AIME/GPQA/HLE evaluation
├── tests/                       # engine/worker/distributed/model tests
├── doc/                         # 部署 Q&A 与架构/性能图
└── requirements*.txt/setup.py   # 平台依赖与 native build surface
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `deepinfer/entrypoints/llm.py` | offline host wrapper | 批量 admission、per-request deep copy、engine loop、pool clone、最终按 request ID 排序。 |
| `deepinfer/engine/llm_engine.py` | 核心编排 | worker/cache/scheduler 初始化；request 校验；SO pending；schedule/execute/process/flush。 |
| `deepinfer/worker/worker.py` | 异步 step runtime | `forward(current) → post(previous) → sample(current)`；ZOS 延后一轮 post-process。 |
| `csrc/engine/scheduler.hpp` | C++ 调度核心 | waiting/running/finished、block/state 管理、prompt/decode scheduling 与 metadata。 |
| `deepinfer/environ.py` | 配置真相层 | lazy typed descriptors；strict bool/choice/int；`rearm` 支持按 engine type 重解析。 |
| `deepinfer/structure_output/compiler.py` | grammar compile | JSON/regex/EBNF 分派、cache 上限、异常归类；记录 CVE-2025-32381 风险说明。 |
| `deepinfer/structure_output/matcher.py` | grammar runtime | KMP trigger、bound token、rollback history、timeout future、aborted matcher。 |
| `deepinfer/sampling_params.py` | 请求级 sampling contract | 参数边界、uint64 `seq_seed`、structured output args。 |
| `requirements*.txt` | 平台依赖矩阵 | common pins + NVIDIA/Ascend 的 torch/native graph；无 lockfile/hash。 |

#### ⭐ 源码精读

**函数 1：`LLM.generate()` / `_run_engine()`——自动 batch，但终态要 drain 在途 step。**

```python
def generate(self, prompts=None, sampling_params=None, prompt_token_ids=None,
             use_tqdm=True, multi_modal_data=None):
    if prompts is None and prompt_token_ids is None:
        raise ValueError("Either prompts or prompt_token_ids must be provided.")
    # 每个 request 进入 _add_request；其中 deepcopy SamplingParams。
    for i in range(num_requests):
        self._add_request(prompt, sampling_params, token_ids, multi_modal_data)
    return self._run_engine(use_tqdm)

def _run_engine(self, use_tqdm):
    while True:
        unfinished = self.llm_engine.has_unfinished_requests()
        step_outputs = (self.llm_engine.step() if unfinished
                        else self.llm_engine.flush_inflight_reqs())
        # clone pooled output，直到 scheduler + SO pending 均结束。
        if not unfinished:
            break
```

逻辑摘要：`has_unfinished_requests()` 同时汇总 scheduler 与 structured-output builder；“waiting 为空”不能跳过 ZOS 在途结果，最后必须 `flush_inflight_reqs()`。这可反哺 Hermes 的 completion contract：queue empty、process exit、stdout EOF 都不等于 active stage 已 drain。

**函数 2：`Worker.execute_model_step()`——当前 forward 与前一步 post-process 重叠。**

```python
@torch.inference_mode()
def execute_model_step(self, is_prompt, is_placeholder,
                       seq_metadata_list=None, scheduler_outputs=None):
    main_model_output = self.model_runner.execute_main_model(...)
    request_outputs = self._post_process_step(self.prev_step_state)
    sampler_output = self.model_runner.execute_sample(...)
    self.engine_callbacks.pre_sampler_sync_fn(scheduler_outputs)
    curr_step_state = WorkerStepState(..., sampler_output=sampler_output)
    if is_prompt or not envs.DEEPINFER_ZERO_OVERHEAD_SCHEDULING:
        request_outputs = np.concatenate(
            [request_outputs, self._post_process_step(curr_step_state)])
        self.prev_step_state = None
    else:
        self.prev_step_state = curr_step_state
    return request_outputs
```

逻辑摘要：ZOS 把 decode 当前 step 的 post-process 延到下一步，形成 `forward(N+1)` 与 `post(N)` 重叠；保存的是 typed `WorkerStepState`，不是推测日志。边界是 cooperative pipeline 仍依赖 CUDA event、同一 worker lifecycle 和最终 flush，进程崩溃不自动可恢复。

**函数 3：`EnvVar.__get__()` / `_bool()`——lazy config 也必须 strict、带字段名失败。**

```python
def _bool(v: str | None, default: str = "0") -> bool:
    value = (v if v is not None else default).lower()
    if value in {"0", "", "false"}:
        return False
    if value in {"1", "true"}:
        return True
    raise ValueError("expected one of '0', '1', 'false', 'true' (case-insensitive)")

class EnvVar[T]:
    def __get__(self, instance, owner):
        with self.lock:
            cached = owner.__dict__.get(self.name, self)
            if cached is not self:
                return cached
            try:
                value = self.init(os.getenv(self.name))
            except Exception as e:
                raise type(e)(f"{self.name}: {e}") from e
            setattr(owner, self.name, value)
            return value
```

逻辑摘要：值第一次访问才解析并缓存，异常前缀包含具体变量名；`rearm()` 允许 `EngineArgs` 设置默认后重新解析。PR #218 修复了非法值静默启用功能的问题。本机 Python 3.12 probe 真实得到 `TRUE→True`、`FALSE→False`、`yes/2→ValueError`。

**函数 4：`LLMEngine.add_request()`——SO compile pending 与 request-local failure。**

```python
def add_request(..., enqueue: bool = True, ...):
    if prompt_token_ids.size == 0:
        raise ValueError("prompt must not be empty")
    if min_token_id < 0 or max_token_id >= max_valid_token_id:
        return None
    seq = Sequence(...)
    if sampling_params.so_args is not None:
        if not enqueue:
            seq.so_matcher = self.so_matcher_builder.build(so_args).result()
        else:
            so_pending = True
    if enqueue:
        def _enqueue(s):
            if s.so_matcher is not None and s.so_matcher.is_aborted():
                s.status = SequenceStatus.FINISHED_SO_FAILED
            self.scheduler.add_sequence(s)
        self.so_matcher_builder.submit(seq, sampling_params.so_args, _enqueue)
    return seq
```

逻辑摘要：grammar compile 可与其他工作并行；完成/timeout/异常被投影成 matcher 状态，失败仅终止该 sequence。边界是 invalid token 当前写日志并 `return None`，调用方必须把 drop 纳入 admission receipt，不能只凭 add loop 完成声称所有请求已接收。

**函数 5：`XGrammarMatcher.accept_token()` / `rollback()`——trigger 与投机回滚共享同一状态机。**

```python
def accept_token(self, token: int) -> bool:
    if self._trigger_pending():
        if self._bound_fired():
            if token != self.trigger_tokens[self.trigger_progress]:
                return False
            self.trigger_progress += 1
        else:
            progress = self.trigger_progress
            while progress > 0 and token != self.trigger_tokens[progress]:
                progress = self._trigger_failure[progress - 1]
            if token == self.trigger_tokens[progress]:
                progress += 1
            self.trigger_progress = progress
        return True
    return self.inner_matcher.accept_token(token, debug_print=DEBUG_PRINT)

def rollback(self, steps: int) -> None:
    # 先撤 EOS，再撤 grammar，最后恢复 trigger progress；超 retained history 明确失败。
    if steps > len(self._progress_history):
        raise RuntimeError("rollback ... exceeds retained trigger progress history")
```

逻辑摘要：KMP 避免每 token 重扫 trigger；bound 后只能强制完成 trigger，投机解码拒绝后按有限 history 回滚。边界是 `MAX_ROLLBACK_TOKENS` 与 next-N 设置绑定，改变投机窗口必须同步验证 rollback contract。

#### 依赖分析与供应链风险

- `pyproject.toml`：Python `>=3.12`，build 依赖 `torch>=2.7`、setuptools、ninja；项目版本 `0.1.0`，Development Status 为 Beta。
- `requirements.txt` 精确 pin 21 项：`transformers 4.50.0`、`xgrammar 0.2.2`、`tilelang 0.1.15`、`tile-kernels 2.1.0`、`pillow 11.3.0`、`requests 2.32.5`、NumPy/SciPy 等。
- NVIDIA graph 另 pin `torch 2.13.0+cu132`、`flash-attn-4 4.0.0b34`；Ascend graph pin `torch 2.13.0+cpu`、`torch-npu 2.13.0rc1`。六个 vendor git submodule固定 commit，但 shallow clone 未 materialize，未审其独立 license/build。
- 无 committed lockfile/hash；`setup.py` native build 需要 C++20、CUDA/CANN、虚拟环境，且运行期首次可从 Hugging Face 下载 checkpoint。
- 本机对 common `requirements.txt` 执行 `pip-audit --no-deps --disable-pip`：报告 **109 vulnerability records / 3 packages**（Pillow、Requests、Transformers）。重复/未来 advisory 与实际可达性需复核，不能直接称 109 个可利用漏洞；但固定 pins 当前不可称 clean。
- 平台 requirements 的单独 audit 显示 PyPI 已知项为 0，但 `torch 2.13.0+cu132/+cpu` 因不在 PyPI被 **skipped**，Ascend 的 `torch-npu` 也未形成完整解析证明；因此不能写平台 graph 安全。

#### 本机验证

```bash
uv run --python 3.12 --no-project python -m compileall -q deepinfer deep_cluster tests
# exit 0
```

系统 `python3=3.11.15` 首次 compileall 对 PEP 695 `class EnvVar[T]` / `class Movable[T]` 报 SyntaxError；按项目声明切换到 Python 3.12.3 后成功。这是 runtime prerequisite mismatch，不是上游语法 bug。

```bash
uv run --python 3.12 --no-project python strict_bool_probe.py
# 'FALSE' -> False; 'TRUE' -> True
# 'yes' / '2' -> ValueError
```

本机没有 `nvidia-smi`，也没有 SM100 / Ascend 950、CUDA 13/CANN 9.2、模型权重与 vendor build，因此 **未运行 DeepInfer pytest、native build、offline inference、benchmark、structured-output GPU runtime 或多机调度**。GitHub fixed-head 4 个 CodeQL success 只能作为补充证据。

#### 可复用经验

- 当 CPU/GPU 或多阶段 pipeline 要重叠时，应优先保存 **typed step state + immutable request identity + explicit flush**，因为异步重叠不能让 queue empty 冒充所有在途结果已完成；边界是进程级 crash 仍需 durable replay/receipt。
- 当环境变量控制高成本或行为改变功能时，应优先采用 **strict typed parser + field-named failure + tested defaults**，因为未知字符串默认为 truthy 会静默改变执行；边界是类型正确仍需跨字段 invariant。
- 当可选编译/预处理会阻塞主 engine 时，应优先异步 admission 并把 timeout/error 投影为 request-local terminal，因为一条坏 schema 不应拖垮全 batch；边界是失败必须进入最终 coverage，不可静默 drop。

#### 30 分钟可尝试实验

在 `runtime/hermes/github-learning-poc/pending-flush-config-gate-v0/` 做纯 Python synthetic pipeline：3 个 request，其中一个预处理 pending、一个非法配置、一个已有在途 result；验证 `queue_empty != completed`、invalid config 在 admission 前失败、最终 flush 后每个 request exactly-one terminal。**不安装 DeepInfer、不下载模型、不调用 GPU。**

#### 风险边界

- **License**：GitHub API、`pyproject.toml`、根 LICENSE 均为 Apache-2.0；vendored submodule、模型权重、CUDA/CANN/Torch wheel 和外部 kernel 需分别审查。
- **维护活跃度**：2026-10-16 创建、10 月 25/26 仍有 push，短期 23,901 Stars，变化快；无 tag/release，必须 pin commit。
- **安全风险**：native C++/CUDA/NPU、shared memory、multiprocessing、HTTP profiling、远端 checkpoint、六个 submodule 与大规模 distributed runtime；common pins 的 audit 命中 109 records。
- **局限/不适用**：开源版是 offline core，只支持单一模型族和特定新硬件；不包含完整 online serving、KV cache system、P/D/VE disaggregation 与 replica load balancing；不能直接替换 Hermes 的模型网关。
- **未验证**：GPU/NPU build、pytest、kernel 正确性、benchmark、batch invariance、deterministic sampling、SO runtime、vendor submodule、模型/权重许可、Q&A 生产数字均待核验。

#### ⭐ Skill 升格判断

**需二次验证。** 不迁移 DeepInfer 代码、kernel 或部署配置。只将“pending preprocessing + typed step state + explicit drain/flush + strict config admission”作为 Hermes runtime workflow candidate，并先与已有 completion/receipt、orchestrator protocol、verification-first 去重。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/pending-flush-config-gate-v0/`。
2. Canonical schema：`run_id/request_id/stage/generation/status/pending_owner/inflight/effect_certainty/terminal/evidence`。
3. Config parser candidate：只处理 POC 的 synthetic bool/choice/int，不改 `~/.hermes/config.yaml`；非法值在 dispatch 前 `blocked`。
4. Orchestrator adapter：未来让 `github_learning_orchestrator.py` 把 pending background/audit/KB copy 分开，`completed` 必须在所有 required stages drain/read-back 后写入。
5. Shared hub 路径全部经 `scripts/resolve_shared_root.py`；POC 仅写 runtime，不改 curated、cron、provider、model 或 secret。
6. 只有 fixture 抓到现有 orchestrator 的真实假完成路径后，才更新既有 shared workflow/skill，不新建项目同名 Skill。

---

### 2. Jakeschincariol/replica-skill

- **链接**：https://github.com/Jakeschincariol/replica-skill
- **固定源码提交**：`77c9436fb3d18c3d58169efb8caf4fe906b0dc51`（2026-10-03T12:07:14Z；commit verification=false）。
- **GitHub API**：Stars **6,264**；Forks **1,108**；Language **Python**；License **MIT**；`created_at=2026-10-03T12:07:49Z`；`updated_at=2026-10-28T22:36:03Z`；`pushed_at=2026-10-03T12:07:53Z`；API `open_issues_count=15`（含 PR）。
- **Release / tags / Actions**：Releases 与 Tags API 均为空；固定 head check-runs=0，Actions runs 为空；`.claude-plugin/plugin.json` 自报 `1.0.0`，这不是签名 release artifact。
- **一句话判断**：它值得学的是“**多阶段 Skill 以稳定中间件串联，并把模糊工作交给 Agent、可判定边界交给标准库 checker/exit code**”；不值得照搬的是“clone any app”这个高风险目标与未完全强制的安全承诺。
- **解决的问题**：替代单个超长 prompt 从调研直接跳部署的做法：11 个 Skill 通过 `replica/` artifact 串成 recon→architect→design→build→backend→test→diff→entrepreneur→brand→launch→deploy；六个 Python 工具为 parity、视觉差异、review provenance、对比度、品牌残留和 store listing 提供 deterministic gate。

#### 证据交叉核验

1. **README**：11 个 Skill、六个标准库工具、共享 `replica/` 中间件、clean-room/only-own-account/always-rebrand 声明。
2. **SKILL.md**：`replica-recon` 规定 public/own-account、人类速度、不读 JS bundle/private APIs；`replica-deploy` 规定 user go、preflight failure stop、用户自行购买/输入 secret。
3. **源码与 tests**：读取 `parity.py`、`imgdiff.py`、`reviews.py`、`sweep.py`、`contrast.py`、`listing.py` 与其全部 tests；本机完整 `unittest` 为 57/57 通过。
4. **Issue #10**：报告 malformed/truncated IHDR 导致 raw `struct.error`；本机固定 commit 真实复现 exit 1 + traceback，证明 parser 错误终态不完整。
5. **GitHub API**：无 tags/releases/checks/actions；`updated_at` 主要可由 Stars/issues 等活动改变，源码 `pushed_at` 自 10 月 3 日未更新，不能用 updated_at 冒充维护提交。
6. **Security endpoints**：public advisories 0、Dependabot 404/不可读；项目虽无第三方 runtime dependencies，Skill 本身可驱动 browser/shell/deploy，仍是高权 authority surface。

#### 架构 / 实现与数据流

```text
public sources + user's own account + user scope
        │
        ▼
replica-recon → recon.md / features.csv / reference screenshots
        │ stable IDs Sxx/Fxx + evidence/confidence
        ▼
architect → design → build → backend
        │ shared project artifacts, not hidden chat memory
        ▼
test → diff → entrepreneur → brand → launch
        │
        ├─ parity.py      feature denominator / must-have gate
        ├─ imgdiff.py     layout/pixel measurement
        ├─ reviews.py     source-linked complaint evidence
        ├─ contrast.py    WCAG threshold gate
        ├─ sweep.py       original brand residue gate
        └─ listing.py     store constraints / copycat warnings
        ▼
replica-deploy preflight
        │ any failure stop; user go required by prose contract
        ▼
external host / DNS / OAuth / payments / stores
```

真正的核心是“artifact handoff + deterministic checker”，不是 11 个角色名。当前边界仍不完整：Skill 文本是模型行为契约，不是 host enforcement；没有统一 orchestrator manifest、artifact hash、stage terminal、source scope 或 final effect receipt。

#### Repo tree 摘要

固定提交只有 **39 个 tracked files**：

```text
replica-skill/
├── .claude-plugin/          # Claude Code plugin/marketplace manifest
├── replica-recon/           # sources/screens/flows/data model/features matrix
├── replica-architect/       # stack/schema/API plan
├── replica-design/          # tokens + WCAG contrast checker
├── replica-build/           # screen-by-screen build workflow
├── replica-backend/         # auth/database/payment/integration workflow
├── replica-test/            # test plan/bug report/Playwright example
├── replica-diff/            # feature parity + PNG layout/pixel checker
├── replica-entrepreneur/    # source-linked review theme ranker
├── replica-brand/           # rebrand workflow + residue sweep
├── replica-launch/          # landing/store listing + listing checker
├── replica-deploy/          # preflight and explicit user-go contract
└── tests/                   # 57 standard-library unit/contract tests
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `replica-recon/SKILL.md` | discovery contract | sources first、stable screen/flow IDs、evidence/confidence、out-of-scope、clean-room rules。 |
| `replica-diff/parity.py` | feature gate | `must/should/could=3/2/1`；partial=0.5；skip/extras 不进 denominator；must 未完显式 not shippable。 |
| `replica-diff/imgdiff.py` | image checker | stdlib PNG decode；layout edge-density grid；pixel mode；region/height delta；malformed IHDR bug。 |
| `replica-entrepreneur/reviews.py` | evidence ranker | 无 URL/text 丢弃、文本去重、rating/age weight、多来源 thin 标记、verbatim quote + URL。 |
| `replica-brand/sweep.py` | deploy blocker | 扫 name/domain/color/path；忽略 deps/build/binary/`replica/`；hits→exit 1。 |
| `replica-design/contrast.py` | accessibility gate | token flatten、WCAG luminance/ratio、AA/AAA/UI threshold、failure exit 1。 |
| `replica-launch/listing.py` | store metadata gate | Unicode approximate length、字段上限、original name、claims/emoji/keyword waste。 |
| `replica-deploy/SKILL.md` | final workflow | tests/parity/sweep/listing/build preflight；失败 stop；用户 go 与 credential boundary。 |
| `.claude-plugin/plugin.json` | host adapter | 11 个 root Skill 的 Claude Code plugin projection；无 Hermes capability manifest。 |

#### ⭐ 源码精读

**函数 1：`parity.score()`——冻结 denominator，skip 和 extras 不骗分。**

```python
def score(rows):
    counted, skipped, extras, problems = [], [], [], []
    for row in rows:
        if row.get("original", "yes").lower() in ("no", "n", "false"):
            extras.append(row); continue
        if row.get("clone", "").lower() == "skip":
            skipped.append(row); continue
        w = WEIGHT.get(row.get("priority", "").lower(), 1)
        c = CREDIT.get(row.get("clone", "").lower(), 0.0)
        counted.append(dict(row, weight=w, credit=c))
    total = sum(r["weight"] for r in counted)
    got = sum(r["weight"] * r["credit"] for r in counted)
    feature_score = 100.0 * got / total if total else 0.0
```

逻辑摘要：新增自家功能不提高 parity，主动 out-of-scope 不进入分母，unknown value 被记 problem 并按保守值计算；must-have 完成数独立于总体分。边界是 `skip` 只靠 CSV 文本，缺少独立批准与 evidence，模型仍可能把难项标 skip 来改变分母。

**函数 2：`reviews.load_reviews()` / `analyse()`——没有 source 就没有 claim。**

```python
def load_reviews(path):
    for raw in csv.DictReader(fh):
        url, text = row.get("url", ""), row.get("text", "")
        if not url or not text or not re.match(r"^https?://", url):
            dropped += 1; continue
        key = re.sub(r"\W+", " ", text.lower()).strip()
        if key in seen:
            dupes += 1; continue
        kept.append({"source": ..., "url": url, "text": text, ...})

def analyse(reviews, themes, request_patterns, today=None, months=18):
    for rv in reviews:
        hit = next((p for p in theme["patterns"] if p.search(rv["text"])), None)
        if hit:
            result["reviews"].append({"rv": rv,
                                      "quote": snippet(rv["text"], hit)})
    # <3 reviews or <2 sources => thin
```

逻辑摘要：算法只重排输入，不生成 review；quote 保持原文子串和 URL，低评分但未匹配主题的条目单独交给人工。边界是 URL 格式不证明网页真实存在/内容一致，regex theme 也会漏配与误配；公开评论采集仍受站点条款约束。

**函数 3：`sweep.sweep()`——确定性 preflight 可以阻断，但 coverage 必须公开。**

```python
def sweep(root, avoid=(), domains=(), colors=(), include_replica=False,
          max_size=2_000_000):
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(root)):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn in SKIP_FILES: continue
            if os.path.getsize(path) > max_size or is_binary(path): continue
            for i, line in enumerate(open(path, errors="replace"), 1):
                # name/domain regex + normalized hex matches
                ...
    return hits

# CLI: return 1 if hits else 0
```

逻辑摘要：path/content 同扫、name 可跨空格/下划线/连字符、颜色 short/long normalization；标准 exit code 可进入 deploy gate。边界是默认跳过 binary、lock、build、>2MB 文件和 planning folder，不能把 0 hits 写成“全部品牌资产已清除”；symlink/TOCTOU/生成制品也未建模。

**函数 4：`imgdiff.compare()`——layout 与 pixel 两种目标分离。**

```python
def compare(img_a, img_b, mode="layout", width=480, cols=12,
            tolerance=24, edge_threshold=40):
    a, b = to_width(img_a, target), to_width(img_b, target)
    h = min(a[1], b[1])
    if mode == "pixel":
        score = 100.0 * (1 - changed / float(w * h or 1))
    else:
        ea, eb = edges(gray(a[2][:h]), edge_threshold), edges(gray(b[2][:h]), edge_threshold)
        # 每个非空 grid cell 比较 edge density；sim < 0.6 标 region。
        score = 100.0 * sum(sims) / len(sims) if sims else 100.0
    return report, diff
```

逻辑摘要：rebrand 不应被 exact pixel 相似度惩罚，因此 layout 用 edge-density；自己的 regression 才用 pixel。边界是当前度量不比较真实组件语义、可访问性、交互与 OCR 文本；两张空图可能得到 100，必须与 feature/behavior gate 联合。

**函数 5：`read_png()` 的 malformed-IHDR 缺口——宣称的 clean terminal 未覆盖所有 parser path。**

```python
def read_png(path):
    # ... chunk loop ...
    if ctype == b"IHDR":
        ihdr = struct.unpack(">IIBBBBB", chunk)  # 未先验证 len(chunk) == 13

# main 只捕获：
except (PngError, OSError, zlib.error) as exc:
    print("imgdiff: %s" % exc, file=sys.stderr)
    return 2
```

逻辑摘要：`struct.error` 未捕获。按 issue #10 构造 12-byte IHDR，本机真实得到 exit **1** 与 raw traceback，不是预期的 exit 2 + 单行错误。这说明 deterministic gate 也必须有 malformed/fuzz corpus，不能因 57 tests 全绿就外推 parser fail-closed。

#### 依赖分析与供应链风险

- 六个工具都只用 Python 标准库，要求 Python 3.8+；仓库无 `requirements.txt`、package lock 或 native dependency，运行依赖面较小。
- 但真正的 Skill workflow 会引导浏览器读取站点、生成代码、运行 Playwright/npm build、设置生产数据库/DNS/OAuth/Stripe/store 发布；**authority/effect surface 远大于 Python package graph**。
- `.claude-plugin` 是 Claude Code adapter；没有 Hermes loader/conformance manifest。README 的“粘贴 URL install skill”不应在无人值守环境执行。
- 无 tag/release/Actions/checks，固定源码只有一个 root commit；commit 未 verified。API public advisories=0 和标准库-only 都不能证明 prompt workflow、browser/deploy 行为安全。
- 顶层 MIT 只覆盖仓库源码；目标 App 的商标、trade dress、内容、数据、服务条款与第三方集成许可不因 MIT 自动解决。

#### 本机验证

```bash
python3 -m unittest discover -s tests -v
# Ran 57 tests in 0.989s
# OK
```

测试真实覆盖 repo structure/frontmatter、parity、reviews provenance、PNG filters/layout、contrast、listing、brand sweep；没有真实 browser、Playwright、第三方 App、部署、支付、DNS 或 store review。

```bash
python3 replica-diff/imgdiff.py /tmp/replica-malformed-ihdr.png /tmp/replica-malformed-ihdr.png
# exit 1
# struct.error: unpack requires a buffer of 13 bytes
```

这是 issue #10 的本机复现。没有修改上游源码；修复与回归测试仍待上游落地。

#### 可复用经验

- 当长 Agent 流程跨调研、设计、实现、验证与发布时，应优先用 **stable artifact IDs + canonical handoff files + per-stage acceptance**，因为只靠聊天上下文会丢失 scope 和证据；边界是 artifact 存在不等于语义合格。
- 当规则能被确定性表达时，应优先写成 **stdlib checker + machine-readable output + meaningful exit code**，因为 prompt 约束不能稳定阻断发布；边界是 checker 必须披露 skip/coverage，并有 malformed/adversarial fixtures。
- 当自动分数影响 ship/no-ship 时，应优先冻结 denominator、把 skip/extras/partial 分开并独立检查 hard must-have，因为单一总分容易被新增项或排除项操纵；边界是 skip 本身需要 evidence/approval。
- 当 workflow 触及竞品、商标、登录态或部署时，应优先把合法来源、用户所有权、外部 effect 与最终 user-go 放在 host-owned gate，而不是只写进 Skill prose；边界是此类判断需要人工/法律审查。

#### 30 分钟可尝试实验

建立 `runtime/hermes/github-learning-poc/artifact-stage-gate-v0/`：synthetic `sources.csv → features.csv → report.md → preflight.json`，用 4 个 fixture 验证 missing source、unauthorized skip、checker crash、effect requires user-go；每阶段输出 `ready/blocked/failed/completed` 和 coverage。不复制 Replica Skill，不访问真实 App，不运行 deploy。

#### 风险边界

- **License**：仓库 GitHub API、根 LICENSE、plugin manifest 均为 MIT；但目标 App 的条款、商标、trade dress、数据、内容和第三方 API 不在该许可内。
- **维护活跃度**：源码只在 2026-10-03 push，之后没有 commit/tag/release/checks；API updated_at 到 10 月 28 不能证明代码维护。Issue #10 自 10 月 18 仍 open。
- **安全风险**：Skill 可建议 browser、copy directories、shell、Playwright、生产环境、支付、OAuth、DNS 和 store publish；用户 go 只是文本约束，宿主若无 hard gate 仍可被绕过。
- **局限/不适用**：不适合受监管、高 IP 风险、需强 OS sandbox 或无法合法观察目标的项目；edge-density 不是视觉/行为等价证明，regex sweep 也不证明 clean-room。
- **已知缺陷**：malformed IHDR 会 raw traceback/exit 1；`sweep` 默认跳过多类文件；`parity skip` 无独立批准；review URL 未做 live read-back。
- **未验证**：真实 Claude/Hermes invocation、全 11 阶段顺序与 resume、browser source limits、Playwright、deploy、Stripe/OAuth/DNS、store acceptance、legal claims 均待核验。

#### ⭐ Skill 升格判断

**暂不沉淀。** 不将 11 个“clone app” Skills 复制进 shared，也不安装 plugin。只保留“artifact-stage gate + source-linked evidence + deterministic preflight”作为候选 workflow；它与现有 orchestrator protocol、verification-first、shared-skill governance 高度重叠，必须先去重和做 synthetic fixture。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/artifact-stage-gate-v0/`。
2. Stage manifest：`stage/id/inputs/source_scope/expected_artifacts/checker/coverage/terminal/next/effect_class`。
3. Hermes 只做 host-owned orchestrator；所有写入限制在 synthetic runtime，外部发布/effect 固定为 `blocked/needs_user`。
4. 候选 checker：source URL presence、denominator/skip approval、artifact hash/read-back、exactly-one terminal；checker crash 必须 `failed`，不能空结果继续。
5. Shared hub 若吸收，只更新既有 autonomous-learning/orchestrator/verification Skill；不建立 “Replica” 产品同名 Skill，不复制第三方模板。
6. 本次不修改 Hermes/OpenClaw/future-agent 配置、cron、provider、model 或 secret，且明确未调用 OpenClaw。

## 经验沉淀

1. **当异步 pipeline 把当前计算与前一步收口重叠时，应优先保留 typed generation/step state、active count 与 explicit flush，因为 queue empty、schedule 成功和进程仍活着都不能证明全部结果已完成；边界是进程崩溃仍需 durable reconciliation。**
2. **当环境变量控制高成本、并行度或行为开关时，应优先严格解析允许值并把字段名写进错误，因为未知字符串 truthy 会静默启用功能；边界是单字段合法还需跨字段 invariant。**
3. **当可选 schema compile、文档解析或预处理失败时，应优先给单对象 request-local terminal，并把失败计入 coverage，因为一条坏输入不应拖垮整批，也不能被静默 drop；边界是 fail-local 不等于忽略失败。**
4. **当多阶段 Agent 工作流需要持续上下文时，应优先用 stable IDs、canonical artifacts 和 stage manifest 交接，因为纯聊天记忆不能稳定承载 scope、source 与 acceptance；边界是文件存在仍需 schema/semantic/read-back。**
5. **当确定性 checker 被用作发布 gate 时，应优先公开 skip/coverage、返回 machine-readable status，并加入 malformed/adversarial fixtures，因为 57 个绿色测试也可能漏掉一个未捕获 parser exception；边界是 checker 完整也不替代 OS/host authorization。**
6. **当自动分数决定是否发布时，应优先冻结 denominator，并把 skipped、extras、partial 与 hard must-have 分开，因为总分可被排除项和新增项扭曲；边界是 skip 需要独立 evidence 与 approval。**
7. **当 Skill 触及登录态、竞品、支付、DNS 或生产发布时，应优先由宿主强制 source/effect/user-go gate，因为 Skill prose 中的“不要做”不是 enforcement；边界是法律与服务条款仍需人工审查。**
8. **当项目要求特定 runtime 时，应优先用项目声明的解释器执行验证，因为系统 Python 3.11 对 Python 3.12 语法失败不能记为上游 regression；边界是 compileall 成功也不代表 native/GPU runtime 成功。**

## 今日真实验证汇总

| 对象 | 实际执行 | 结果 | 不可外推范围 |
|---|---|---|---|
| GitHub Trending/Search/API | `curl` + `gh api` repository/commit/release/tag/issues/checks/advisories | 候选与两仓元数据真实返回；固定 commit | API 查询时点，不代表未来热度/维护 |
| DeepInfer Python 3.12 | `compileall deepinfer deep_cluster tests` | exit 0 | 不含 import/native build/GPU tests |
| DeepInfer strict bool | fixed commit `_bool()` probe | TRUE/FALSE 正确；yes/2 ValueError | 不证明所有 config invariant |
| DeepInfer dependency audit | common pins `pip-audit --no-deps` | 109 records / 3 packages | 需去重、reachability；平台 torch 被 skip |
| Replica完整 suite | `python3 -m unittest discover -s tests -v` | **57 passed / 0 failed** | 不含 browser/deploy/external services |
| Replica issue #10 | synthetic 12-byte IHDR | **exit 1 + raw struct.error，已复现** | 仅该 malformed path，不外推其他 parser |
| GitHub security API | public advisories + vulnerability alerts | 两仓 advisories 0；Dependabot 404/不可读 | 不能声称无漏洞 |

## 明日继续

1. 最小动作：创建 `runtime/hermes/github-learning-poc/pending-flush-config-gate-v0/`，用三个 synthetic request 验证 pending、invalid-config、inflight flush 与 exactly-one terminal。
2. 再建立 `artifact-stage-gate-v0` 的四个 fixture：missing source、unauthorized skip、checker crash、effect needs_user；不执行真实外部 effect。
3. 深挖 DeepInfer `Scheduler::schedule/process_outputs` 的 prompt/decode collective 边界，以及 Replica checker 的 coverage schema；如果只重复已有 completion/verification contract，则停止新增。
4. Replica issue #10 只跟踪上游修复，不在 shared 复制/打补丁；DeepInfer audit records 做去重和调用路径 reachability 后再判断风险。

## 候选反哺

### Candidate Facts

- [ ] topic: 异步 stage 需要 pending/inflight/flush 分层，queue empty 不等于 completed | evidence: `DeepInfer@5537415` 的 `Worker.execute_model_step`、`LLM._run_engine`、`flush_inflight_reqs` | 建议: update existing completion/orchestrator candidate | 安全级别: medium
- [ ] topic: Agent workflow 的 canonical artifact handoff 应与 deterministic checker 联动 | evidence: `replica-skill@77c9436` 的 11-stage `replica/` artifacts + six stdlib gates + 本机 57 tests | 建议: candidate/update existing workflow | 安全级别: medium
- [ ] topic: checker 绿色 suite 不代表 malformed terminal 完整 | evidence: Replica issue #10 + 本机 12-byte IHDR 复现 exit 1/raw traceback | 建议: update verification-first malformed corpus guidance | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: pending-flush-config-gate-v0 | 可复用场景: Hermes cron/orchestrator/background preprocess/audit | 是否建议 shared: no（当前） | 原因: 与 completion/receipt 高度重叠，先做 fixture 证明现有假完成缺口
- [ ] 名称: artifact-stage-gate-v0 | 可复用场景: 多阶段研究/生成/审计/发布 | 是否建议 shared: no（当前） | 原因: 先与 autonomous-learning、verification-first、shared-skill governance 去重；不迁移 Replica 产品语义

### Candidate Open Questions

- [ ] 问题: `github_learning_orchestrator.py` 的 audit success 后 KB copy / push artifact 是否有 required-stage drain 与 read-back receipt？ | reason: adaptation/gap | priority: high
- [ ] 问题: DeepInfer invalid token 的 `return None` 在上层是否始终形成可见 rejection，而非 admission coverage 丢失？ | reason: gap | priority: medium
- [ ] 问题: Replica 的 `skip` denominator 变更应如何绑定 source/evidence/user approval，避免 Agent 自行降分母？ | reason: adaptation | priority: high
- [ ] 问题: issue #10 修复后是否加入 truncated chunk/CRC/oversized PNG 的统一 malformed corpus？ | reason: stale/gap | priority: medium

### 不应自动落地

- 不安装 DeepInfer、模型、Torch/CUDA/CANN、vendor submodule、Replica plugin 或 11 个第三方 Skills。
- 不执行真实 App recon、登录态浏览、复制、支付、DNS、OAuth、store publish 或生产 deploy。
- 不修改 Hermes/OpenClaw/future-agent 配置、model、provider、cron、secret；本任务未调用 OpenClaw。
- 不把候选直接写入 curated active facts，不复制第三方代码/模板进 shared capabilities。
- 不把 common pins 的 109 audit records说成 109 个已利用漏洞；不把 57 tests/CodeQL success 外推为完整安全或生产可用。
