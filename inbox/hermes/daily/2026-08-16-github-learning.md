# 2026-08-16 GitHub 热门项目学习日报

> 执行器：Hermes。当前 OpenClaw runtime 不存在；本次未调用、启动、模拟或写入 OpenClaw。  
> 共享根：先运行 `python3 scripts/resolve_shared_root.py`，真实解析为当前 shared 根。  
> 研究窗口：2026-08-16 07:30–07:36（UTC+08:00）；Trending 用 `curl` 真实抓取，仓库元数据、commit、release、issues 和 license 用 `gh api` 读取，源码用 `git clone --depth 1` 固定。  
> 固定源码：`MakazhanAlpamys/Soup@33cce1a4ca8954110f2ff365d59dbd65f2912844`；`citrolabs/ego-lite@c46a439e7fbad90ad33dbea6c6af329b6009809f`。  
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-16/`。Trending HTML 为 604,316 bytes，SHA-256 `ed2d63111a66200fad5c7fcb49f6e2f6ce7271a41edee6d805d4d44e054c96cc`。  
> 数据边界：Stars、forks、updated/pushed 是查询时动态值；README/release/issue 的 benchmark 与运行报告属于上游声明。只有本文明确列出的本机命令结果是本机验证。

## 今日结论

今天的主线是：**自动化系统的可靠边界不能只靠一个“通过”布尔值。Soup 把模型发布判断拆为 task win、回归轴、noise floor、provenance 和不同 exit code；ego-lite 把浏览器自动化拆为 task-space ownership、stable error code、session/ref 生命周期与 hard stop。对 Hermes/shared hub 最值得反哺的是统一的 `scope identity + measurement coverage + ownership/authorization + terminal reason + receipt` 契约，而不是自动安装训练栈或复用用户登录态的浏览器。**

## 研究边界与真实验证

- **发现源**：`https://github.com/trending?since=daily` 的真实 HTML 解析出 `cordiverse/cordis`、`cathrynlavery/diagram-design`、`cursor/plugins`、`cactus-compute/needle`、`unslothai/unsloth`、`public-apis/public-apis`、`MakazhanAlpamys/Soup`、`github/spec-kit`、`citrolabs/ego-lite` 等候选；Trending 只作发现，元数据由 Repository API 二次核验。
- **Soup 本机验证**：浅 clone 固定 main commit；`python3 -m compileall -q src` 返回 exit 0。第一次 `uv run --with pytest --with-editable .` 因 uv 跨支持 Python split 同时解析 `all` 与 `mlx`，暴露 `mlx-lm>=0.31.3` 要求 `transformers>=5`、而 train extra 要求 `<5` 的真实解析冲突，exit 1。随后在独立 `.venv-min` 只安装 core editable + pytest，`tests/test_v07302.py` **175 passed in 3.16s**。没有安装 train extra、没有下载模型、没有 GPU、没有运行训练/ship live gate，因此 4GB、tok/s、VRAM 和模型质量均为**待核验/上游测量**。
- **ego-lite 本机验证**：浅 clone 固定 GitHub API main commit；Node `v22.14.0`、npm `10.9.2`。`npm ci --ignore-scripts` 安装 29 packages，npm audit 报 0 vulnerabilities；`npm test` 完成 build、TypeScript typecheck 和 Node tests，**299 passed / 0 failed，596.94 ms**。构建真实警告 `src/state.ts -> src/browser-runtime.ts -> src/state.ts` circular dependency。没有 ego browser app/global binding，未执行真实浏览器 E2E、未迁移 Chrome 数据、未读取登录 cookie。
- **安全边界**：不自动修改 Hermes config/model/provider/auth/env/cron/skills；不安装 ego-lite DMG/skill，不调用浏览器；不下载模型或执行训练；不把 candidate 直接写入 `curated/memory/`。

## 项目速览

下表均来自 2026-08-16 07:31–07:36（UTC+08:00）期间真实 `gh api repos/{owner}/{repo}` 输出。`NOASSERTION` 表示 GitHub API 未识别仓库级许可，不等于无许可；Stars 会变化。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | 460,127 | 50,852 | Python | MIT | 2026-08-15T23:31:28Z / 2026-08-13T21:07:34Z | 资源清单，热度高但源码机制较弱 |
| [github/spec-kit](https://github.com/github/spec-kit) | 129,174 | 11,548 | Python | MIT | 2026-08-15T23:29:42Z / 2026-08-14T16:44:52Z | 前一日已深读，今日不重复 |
| [unslothai/unsloth](https://github.com/unslothai/unsloth) | 72,027 | 6,492 | Python | Apache-2.0 | 2026-08-15T23:25:15Z / 2026-08-15T16:49:07Z | 大型训练栈，依赖/GPU 面超出今日范围 |
| [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | 47,333 | 4,392 | Python | Apache-2.0 | 2026-08-15T23:23:47Z / 2026-08-13T04:30:15Z | CLI/Agent 候选，今日先读新项目 |
| [ToolJet/ToolJet](https://github.com/ToolJet/ToolJet) | 39,517 | 5,293 | JavaScript | AGPL-3.0 | 2026-08-15T23:29:53Z / 2026-08-14T14:11:22Z | 部署面大、AGPL 边界重 |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 18,571 | 1,114 | HTML | MIT | 2026-08-15T23:30:33Z / 2026-08-14T21:28:44Z | 图示 skill，需防 prompt/template 直接搬运 |
| [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | 10,944 | 557 | JavaScript | MIT | 2026-08-15T23:32:28Z / 2026-08-15T09:56:46Z | **深读：浏览器 ownership、hard stop、CDP/session/ref** |
| [cactus-compute/needle](https://github.com/cactus-compute/needle) | 6,054 | 402 | Python | MIT | 2026-08-15T23:31:22Z / 2026-08-15T16:03:14Z | 前一日已深读，今日不重复 |
| [cordiverse/cordis](https://github.com/cordiverse/cordis) | 4,044 | 198 | TypeScript | MIT | 2026-08-15T23:22:17Z / 2026-08-13T13:48:22Z | 时空组合框架；README 明示 API 未稳定 |
| [MakazhanAlpamys/Soup](https://github.com/MakazhanAlpamys/Soup) | 1,638 | 261 | Python | Apache-2.0 | 2026-08-15T23:32:00Z / 2026-08-15T18:54:34Z | **深读：双腿发布 gate、noise floor、evidence/provenance、layer streaming** |

### 筛选说明

- Soup 的 v0.73.2 release 就在查询日前一日发布，直接记录“scorer 错误会让 gate 在两种方向撒谎”；它可用于检验 shared hub 的审计分数是否也把测量噪声、工具失败、覆盖缺失误投为结论。
- ego-lite 是当日 Trending，且仓库 topics 明确含 `hermes-agent`；但 README 同时说明开源仓库只含 harness/skill，浏览器 app 是单独下载，正适合研究“开源 adapter 与闭源 authority surface”的边界。
- 两项目的 GitHub License API 及 `repos/{repo}/license` API 分别返回 Apache-2.0 与 MIT；这不自动覆盖模型权重、数据集、浏览器 app、登录数据、site skills 或 transitive dependencies。

## 深读项目

### 项目 1：MakazhanAlpamys/Soup

- **URL**：https://github.com/MakazhanAlpamys/Soup
- **Stars / Forks / Language / License（GitHub API）**：**1,638 / 261 / Python / Apache-2.0**。
- **查询时 updated / pushed**：2026-08-15T23:32:00Z / 2026-08-15T18:54:34Z。
- **固定源码版本**：`33cce1a4ca8954110f2ff365d59dbd65f2912844`；commit message `docs(contributors): Amir Fathi's fourth merge (#414)`。
- **release / issues 证据**：latest release `v0.73.2` 发布于 2026-08-15T09:04:49Z；open issue #406 说明新增 `--noise-floor` 尚不能写进 `eval.ship` 配置；#372 说明 `--no-reexec` 打印的 launch command 会丢用户 flags；#371 说明 reward-hack controller 某些 mode/ladder 尚无有效机械验证。

#### 一句话判断：为什么值得学

Soup 值得学的不是“一份 YAML 就能在 4GB GPU 训练 8B”这句宣传，而是它把**测量仪器本身也当成待验证对象**：task win 与 regression 分腿、scorer 版本变化显式告警、noise floor 只覆盖实际测量的轴、evidence 可离线 replay、配置/数据 provenance 独立记录、工具错误与模型退化使用不同 exit semantics。

#### 解决的问题：替代了什么旧做法

1. 替代“微调 loss 下降就发布”：`soup ship` 要求任务轴获胜，同时 general suites 不发生超过 threshold/noise floor 的回归。
2. 替代“单次 greedy 输出就是确定测量”：`--noise-floor N` 重跑 base，按每轴 max-min 建可分辨下限；上游明确它只 sizes effect，不校准阈值。
3. 替代“evidence JSON 一次性输出”：`verdict_to_evidence`/`--emit-evidence` 使输出可重新成为 `--evidence` 输入，并在读取时保留 stored floor。
4. 替代“配置改了但旧证据继续绿”：semantic `config_sha` 检查 recipe drift；源码也明确 unkeyed hash 只做 staleness，不做防伪。
5. 替代“用公式猜显存适配”：layer streaming 先限制 resident weights，再可选真实 synthetic step probe；probe 失败/oom/refusal 都显式分流。
6. 但它没有消除测量边界：judge mode 的 leg-1 noise 未测、v0.73.2 scorer 与旧 baseline 不同尺度、open issue #406 说明 noise floor policy 还不能完整 config-as-code。

#### 架构 / 实现与数据流

```text
soup.yaml / CLI flags
       │ Pydantic schema + CLI > config > default
       ▼
train lane
  dataset → tokenizer/collator → resident model OR layer-streamed runtime
  layer streaming: meta skeleton → shard index → RAM/NVMe source
                   → one-layer GPU buffers → optional measured VRAM probe
                   → trainer → adapter/artifact

release lane (`soup ship`)
  base + tuned/adapter + task eval
       ├── leg 1: metric / judge_score / pairwise task win
       ├── leg 2: bundled suites + optional lm-eval benchmarks
       ├── optional base repeats → per-axis noise floor
       └── task win + deltas + threshold/floor → SHIP / DON'T SHIP
                    │
                    ├── verdict JSON / distinct exit code
                    └── replayable evidence + config/data provenance
```

核心机制不是单个模型算法，而是“产生 artifact 的训练面”和“决定 artifact 能否发布的测量面”分开。`ship.py` 再把 live generation、offline evidence、baseline、noise floor、provenance 与 terminal rendering 分开；这比一个通用 `success=true` 更适合审计。

#### Repo tree 摘要

固定 commit 共 **966 tracked files**，其中 `src/` 527、`tests/` 366：

```text
Soup/
├── src/soup_cli/
│   ├── cli.py / commands/       # train、ship、eval、serve、data、MCP 等 CLI effects
│   ├── config/schema.py         # Pydantic v2 单一配置真相源与兼容 gate
│   ├── trainer/                 # SFT/DPO/KTO/SimPO 等 wrapper；stream_setup mixin
│   ├── eval/                    # gate、bundled suites、judge、forgetting/scorers
│   ├── utils/                   # ship verdict、layer shard/stream/runtime、provenance
│   └── data/                    # fixtures、traces、split/quality pipelines
├── tests/                       # 366 tracked files；版本化回归、CLI、安全/平台测试
├── benchmarks/                  # 保留撤回读数、硬件/仪器/边界的 measurement records
├── docs/ / examples/ / notebooks/
├── pyproject.toml               # core + 大量 optional extras；Python >=3.10,<3.13
├── SECURITY.md
└── LICENSE / NOTICE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/soup_cli/commands/ship.py` | 发布决策入口 | live/offline 两路、CLI/config precedence、safe evidence read、noise floor、provenance、exit taxonomy |
| `src/soup_cli/utils/ship_verdict.py` | 纯 verdict moat | task win、benchmark deltas、noise floor、SHIP/DON'T SHIP 决策和 evidence projection |
| `src/soup_cli/eval/gate.py` | 通用 suite gate | task 逐项评分；异常变 score=None 且绝不静默 pass |
| `src/soup_cli/eval/gate_suites.py` | bundled scorer | MCQ/tool-call/JSON/safety/over-refusal 等离线 suites |
| `src/soup_cli/trainer/stream_setup.py` | layer streaming | meta skeleton、RAM/NVMe tier、量化 shard、VRAM forecast/probe、cleanup |
| `src/soup_cli/config/schema.py` | 配置真相源 | 互斥、范围、bool-as-int、stream compatibility 等早拒绝 |
| `benchmarks/gate-v0.73.2-leg2-scoring.md` | 测量档案 | RED baseline、撤回读数、live run、evidence round-trip、已知未建立结论 |
| `tests/test_v07302.py` | v0.73.2 回归 | 本机 minimal core 环境真实运行 175 tests 全过 |

#### ⭐ 源码精读

**代码块 1：`_safe_read_text()` 把 evidence/config 文件读取限制在 cwd、非 symlink、有限大小**  
来源：[`src/soup_cli/commands/ship.py#L204-L222`](https://github.com/MakazhanAlpamys/Soup/blob/33cce1a4ca8954110f2ff365d59dbd65f2912844/src/soup_cli/commands/ship.py#L204-L222)

```python
def _safe_read_text(path: str, field: str, max_bytes: int) -> str:
    enforce_under_cwd_and_no_symlink(path, field)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"{field} unreadable: {type(exc).__name__}") from exc
    with os.fdopen(fd, "r", encoding="utf-8") as handle:
        if os.fstat(handle.fileno()).st_size > max_bytes:
            raise ValueError(f"{field} exceeds {max_bytes} bytes")
        return handle.read()
```

逻辑摘要：先做路径 containment 与 symlink policy，再用 `O_NOFOLLOW` 打开并对已打开 fd 做 `fstat`，避免检查后替换的常见 TOCTOU 路径；evidence cap 16 MiB、config cap 4 MiB。边界是 Windows/平台对 `O_NOFOLLOW` 的支持不同，且“文件来自 cwd”不证明里面分数可信。

**代码块 2：`_verdict_from_evidence()` 必须保留 stored noise floor，才能保证 replay 决策一致**  
来源：[`src/soup_cli/commands/ship.py#L377-L429`](https://github.com/MakazhanAlpamys/Soup/blob/33cce1a4ca8954110f2ff365d59dbd65f2912844/src/soup_cli/commands/ship.py#L377-L429)

```python
def _verdict_from_evidence(payload: dict, *, forgetting_threshold: float) -> ShipVerdict:
    task = payload.get("task")
    if not isinstance(task, dict):
        _fail("evidence.task must be an object with 'mode', 'base', 'tuned'", _EXIT_RUNTIME)
    stored_floor = noise_floor_from_evidence(payload.get("noise_floor"))
    _warn_if_floor_widens(stored_floor, forgetting_threshold,
                          source="evidence-supplied")
    task_win = build_task_win(
        task.get("mode", "metric"), task["base"], task["tuned"],
        noise_floor=stored_floor,
    )
    deltas = compute_benchmark_deltas(
        base_scores, tuned_scores,
        forgetting_threshold=forgetting_threshold,
        noise_floor=stored_floor,
    )
    return decide_ship(task_win, deltas,
                       forgetting_threshold=forgetting_threshold,
                       noise_floor=stored_floor)
```

逻辑摘要：报告片段省略了中间 schema loop，但真实函数会逐 benchmark 验证 `base/tuned`。stored floor 会扩大某轴 gate，因此读取端必须告警且不能静默丢弃；否则同一 evidence 会 replay 成不同 verdict。边界是能修改 evidence 的人本来就能伪造分数，noise floor bounds/告警不是签名。

**代码块 3：`_measure_noise_floor()` 只测它真正能归因的轴**  
来源：[`src/soup_cli/commands/ship.py#L701-L772`](https://github.com/MakazhanAlpamys/Soup/blob/33cce1a4ca8954110f2ff365d59dbd65f2912844/src/soup_cli/commands/ship.py#L701-L772)

```python
def _measure_noise_floor(runs, suite_names, base_gen, *,
                         base_id, task_mode, task_eval,
                         forgetting_threshold):
    bundled = [name for name in suite_names if is_bundled_suite(name)]
    measure_task = task_mode == "metric"
    samples = []
    for index in range(runs):
        run = {name: score_bundled_suite(name, base_gen)
               for name in bundled}
        if measure_task:
            tasks = load_eval_tasks(task_eval)
            run[TASK_AXIS] = run_eval(base_id, tasks,
                                      generate_fn=base_gen).accuracy
        samples.append(run)
    floor = compute_noise_floor(samples)
    _warn_if_floor_widens(floor, forgetting_threshold, source="measured")
    return floor
```

逻辑摘要：bundled suites 才进入重复测量；非 bundled 与 judge-backed leg 1 明确跳过，因为把 judge sampling noise 标成 decode noise 是错误归因。这个“coverage 明示”比盲目生成一个全局 confidence 更可靠。边界是 max-min 对 N 很敏感，上游只允许 2–10 次，且未证明 N 足够。

**代码块 4：layer-streaming probe 失败不等于 fit，通过/拒绝根据真实测量状态分流**  
来源：[`src/soup_cli/trainer/stream_setup.py#L620-L703`](https://github.com/MakazhanAlpamys/Soup/blob/33cce1a4ca8954110f2ff365d59dbd65f2912844/src/soup_cli/trainer/stream_setup.py#L620-L703)

```python
def _run_stream_vram_probe(self, model, plan: _ProbePlan) -> None:
    peak = measure_step_peak_bytes(
        model, rows=plan.rows, seq_len=plan.seq_len,
        vocab_size=plan.vocab_size, device=str(self.device),
    )
    if peak is None:
        if plan.predicted_bytes > plan.available_bytes:
            self._close_stream_runtime()
            raise ValueError("measured probe failed and prediction does not fit")
        return
    if peak.failed or peak.oom:
        self._close_stream_runtime()
        raise ValueError("fit could not be established")
    fit = decide_measured_fit(
        measured_bytes=peak.peak_bytes,
        predicted_bytes=plan.predicted_bytes,
        available_bytes=plan.available_bytes,
    )
    if not fit.fits:
        self._close_stream_runtime()
        raise ValueError(fit.reason)
```

逻辑摘要：报告片段压缩了完整错误文本，但保留真实状态机：instrument failure、CUDA failure、OOM、measured fit 是不同状态；不把 probe 没跑成投影为通过。边界是该 probe 使用 synthetic causal-LM step，源码/measurement record明确偏好 loss 与更多架构尚未建立广泛有效性。

#### 依赖分析与供应链风险

- core dependencies：`typer>=0.9,<0.21`、`rich>=13`、`pydantic>=2`、`pyyaml>=6`、`huggingface-hub>=0.16`、`plotext>=5.2`；多数不是 exact pin。
- train extra：`torch>=2`、`transformers>=4.36,<5`、`peft>=0.7`、`trl>=0.14,<0.29`、`datasets`、`bitsandbytes`、`accelerate`；还有 vLLM、MLX、DeepSpeed、Unsloth、MCP、remote storage 等大量独立 extras，供应链/ABI/GPU 矩阵很大。
- **真实解析风险**：本机 `uv run --with pytest --with-editable .` 因项目 extras split 中 `mlx-lm>=0.31.3 → transformers>=5` 与 `all/train → transformers<5` 无解而失败；minimal core editable 安装可解析并通过 175 tests。不能把 minimal 成功外推为 `all`/MLX/train 可装。
- Python 限定 `>=3.10,<3.13`，源码注释说明上限与 CI matrix绑定；本机是 3.11。支持声明比“pip 能解析最新”更窄。
- 模型与数据可能来自 Hugging Face，`trust_remote_code` 是显式 authority surface；Apache-2.0 core 不覆盖用户选择的 weights/datasets 或外部 provider。
- `soup ship --evidence` 的 `config_sha` 是 unkeyed semantic hash，只检查 staleness；若伪造在 threat model 内，应使用签名/可信 CI artifact，而非把 hash 当真实性证明。

#### README / docs / release / issues / source 交叉核验

- README 的 one-YAML、layer streaming、`soup ship` 双腿 gate 与 `config/schema.py`、`trainer/stream_setup.py`、`commands/ship.py` 对应；不是 README-only API。
- v0.73.2 release 的 boxed answer、tool-call envelope、over-refusal、noise floor 与 `tests/test_v07302.py` 的真实回归用例一致；本机 targeted 175 tests通过，但没有复现上游模型/H100数字。
- `benchmarks/gate-v0.73.2-leg2-scoring.md` 主动保留 withdrawn/corrected readings，并区分 CPU 0 floor 与 H100 上游 floor；这是高质量证据习惯，但仍不是独立第三方复现。
- open issue #406 与 `ship.py:1083-1097` 交叉一致：task/general suite/judge/baseline/threshold 都从 `ShipConfig` 读，`noise_floor` 没有对应 config wiring。
- open issue #372 表明 launch hint 与真实 re-exec argv 是双真相源；即使 gate模块严谨，CLI其他 effect面仍有已知 drift。
- open issue #371 明确某些 reward-hack mode/ladder从未有效跑通；不能把仓库 tests 多或版本快直接等同于全功能成熟。

#### 可复用经验

- 当 Agent/模型评估决定是否发布时，应优先拆分“目标收益轴、回归轴、测量噪声、instrument failure、coverage”并分别出 receipt，因为一个 aggregate score 会把工具错误、未测与真实退化混在一起；边界是多轴仍需要版本/fixture治理。
- 当 evidence 要离线 replay 时，应优先把 scorer version、policy、noise floor、source/model/config hash 与原始分数一起持久化，因为只保存 verdict 会失去决策条件；边界是 unkeyed hash只检测漂移，不防伪。
- 当一个预测公式用来阻止高成本 effect 时，应优先用小规模实测 probe覆盖预测盲区，并把 probe failed/oom/refused/completed 分开；边界是 probe形状必须代表真实 workload，不能从一个 SFT shape外推所有任务。
- 当 CLI 提供 config-as-code 时，应优先保证所有 policy flags 都遵循同一 `CLI > config > default` 链并由同一 schema定义，因为遗漏一个 flag就会让生产 gate与仓库配置漂移；边界是配置一致不等于测量正确。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/audit-noise-replay/` 做纯 Python fixture，不加载模型：

1. 定义 `AxisReceipt{name, scorer_version, samples, coverage, floor, threshold, status}`。
2. 构造 stable、noisy、instrument-error、missing-axis、stale-scorer 五类 audit fixture。
3. 要求报告评分只在 `coverage=measured` 且 scorer/version一致时比较；工具异常必须 `blocked/error`，不能得 0 后误判为质量差。
4. 将 `policy_revision + source_hash + samples + floor + verdict` 写 JSON，再离线 replay；两次 verdict/hash必须一致。
5. 不改现有 orchestrator、不写 curated、不调用 provider/GPU。

#### 风险边界

- **License**：GitHub API/root LICENSE 为 Apache-2.0；weights、datasets、generated adapters、CUDA/ML libraries、optional providers分别审查。
- **维护活跃度**：pushed 2026-08-15T18:54:34Z，v0.73.2同日发布；高频变更同时意味着 scorer、dependency 与 config surface快速漂移。
- **安全风险**：模型/数据下载、`trust_remote_code`、MCP execute、training reward code、remote storage、serve endpoint、PR push均可扩大网络/代码/凭据 effect面；SECURITY.md把 path traversal、SSRF、injection、secret leakage、RLVR sandbox escape列为 scope。
- **正确性风险**：noise floor只覆盖 bundled和 metric task轴；judge noise未测；旧 baseline scorer尺度漂移；上游 measurement record也承认样本和硬件范围有限。
- **供应链风险**：extras图巨大，部分只下界；本机已经真实发现 all/MLX transformers constraint冲突。GPU/native ABI不能由 core tests证明。
- **不适用场景**：把单次 LLM judge 分数当 release truth、没有固定 scorer/fixture的跨版本比较、无沙箱加载不可信 remote code、直接在当前 shared cron下载大模型训练。
- **不能自动执行**：不安装 `[train]/[all]/[mlx]`，不下载 weights/datasets，不运行 cloud/GPU/MCP execute，不修改 Hermes provider/cron。

#### ⭐ Skill 升格判断

**需二次验证**；窄的 evidence/noise contract 可迁移，Soup 产品与训练代码暂不沉淀。

- **可直接抽象**：`instrument_error != regression`、per-axis coverage、scorer version、replayable evidence、terminal reason/exit taxonomy。
- **需二次验证**：先完成 synthetic audit replay fixture，再用最近 7 天历史报告的真实审计输出比较“单分数”与“带 coverage/floor receipt”的差异。
- **暂不沉淀**：不复制 Soup CLI、模型训练/streaming code、benchmark数值、阈值或测试全文进入 shared skill。
- **升格结论**：优先更新现有 GitHub-learning/verification/self-reflection契约，不新建 Soup-specific skill；今日仅 Hermes raw candidate，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/audit-noise-replay/{schema.json,fixtures/,measure.py,replay.py,test_contract.py,README.md}`。
2. **Hermes audit sidecar**：未来让 `scripts/github_learning_orchestrator.py` 读取真实 `evidence-receipt.json`，字段至少包括 `source_ref/tool/status/items/coverage/scorer_version/test_exit/artifact_hash`，不再只扫报告关键词。
3. **shared workflow**：fixture通过后，更新现有 `capabilities/skills/research/github-hot-project-learning/`（如当前目录存在）或 verification契约，要求 `blocked/unverified/partial/completed` 不互相投影。
4. **分层**：API JSON、clone、test stdout留 runtime；日报留 Hermes inbox；稳定 invariant经治理审查后才可能进入 curated。
5. **OpenClaw边界**：当前不存在且禁止调用；未来只复用 agent-neutral receipt schema，必须在其真实 runtime验证 scorer/effect映射。

### 项目 2：citrolabs/ego-lite

- **URL**：https://github.com/citrolabs/ego-lite
- **Stars / Forks / Language / License（GitHub API）**：**10,944 / 557 / JavaScript / MIT**。
- **查询时 updated / pushed**：2026-08-15T23:32:28Z / 2026-08-15T09:56:46Z。
- **固定源码版本**：GitHub API 和 clone HEAD 均为 `c46a439e7fbad90ad33dbea6c6af329b6009809f`；commit message `Merge pull request #248 from citrolabs/section9-lab-patch-3`。GitHub repo `pushed_at` 晚于这个 commit，说明 refs/非默认分支或其他仓库活动可能更新；本报告只绑定 default-branch commit。
- **release / issues 证据**：latest release `v1.2.3`（2026-08-11）；main skill frontmatter却为 `1.2.6`（2026-07-20），open issue #273也报告 app-bundled skill仍为1.2.3且遗漏目录。#204 报告跨 CDP session event waiter串线；#270/#173 报告 abandoned task spaces资源累积；#192 报告 skill触发范围过宽；#275 报告 redirect hang和unstable locator。

#### 一句话判断：为什么值得学

值得学的不是“共享真实登录态就免登录”，而是它把 browser control 建模成**有 owner 的 task space**，用 stable error code 把用户接管提升为 hard stop，并为 session/ref/event 设置过期、重附着和资源上限；同时源码和 issues 清楚说明边界：当前 open-source harness依赖独立的浏览器 app/`globalThis.ego`，用户登录态复用本身是高权限，不适合在 WSL cron中自动接入。

#### 解决的问题：替代了什么旧做法

1. 替代 Agent 与用户争用同一 tab：每个 Agent task有独立 Space，但README声称可继承用户登录态。
2. 替代逐 CLI tool来回：CLI从 stdin读取一段 JS，通过统一 `helperContext()` 注入 page/browser/taskSpaces/site/fetch/CDP surface，一次组合多步。
3. 替代只靠脆弱 selector：snapshot产生 backendNode ref与stable locator，resolver支持 ref/CSS/XPath/role/text并区分 transient/permanent失败。
4. 替代用户接管后 Agent继续重试：stable `EGO_TASK_SPACE_USER_IN_CONTROL/INACTIVE` 进入 hard-stop sink，即使上层 catch也丢弃普通输出并保留一次指导。
5. 替代 stale CDP session永久失败：2秒TTL、concurrent attach去重、session-lost时仅对隐式page-level调用重附着一次。
6. 但它没有完整资源/隔离保证：open issue #204指出event waiter可能跨session；#270/#173指出没有idle reclaim/budget；closed-source app与登录数据不在本仓源码审计范围。

#### 架构 / 实现与数据流

```text
Agent stdin JavaScript
       │ runMain → AsyncFunction
       ▼
helperContext()（CLI / embedded SDK 单一 surface）
       ├── page / locator / keyboard / mouse / waits
       ├── browser tabs / snapshot / screenshot
       ├── taskSpaces ownership + handoff + completion
       ├── site learnings: notes + declared node/browser tools
       └── fetch / raw CDP
                 │
                 ▼
globalThis.ego（独立 ego-lite app 提供的闭源 binding）
       ├── task space / tabs / snapshot
       └── CDP transport → Chromium target/session

state/control lane
stable error_code → hard-stop classification → output sink
session TTL/ref map/event buffer/dialog map → retry or fail
```

最关键的 chokepoints 是：`helperContext()` 决定 Agent权力面，`useOrCreate/claim/complete` 决定 task ownership，`buildEgoError()` 决定 hard stop，`browserCdp/ensureSession()` 决定 session identity/retry，`element-resolver` 决定目标歧义是否可重试。

#### Repo tree 摘要

固定 commit 共 **150 tracked files**：

```text
ego-lite/
├── package/ego-browser/
│   ├── src/
│   │   ├── run.ts / index.ts        # CLI 与 embedded SDK入口
│   │   ├── helpers.ts               # 单一 agent-facing helper surface、task spaces
│   │   ├── browser-runtime.ts       # CDP transport、session TTL、events/dialogs
│   │   ├── element-resolver.ts      # ref/locator/role/CSS/XPath、错误分类
│   │   ├── ref-map.ts / ref-state.ts
│   │   ├── driver/                  # nav/pointer/keyboard/waits/observe/files
│   │   ├── learning/                # site skill发现、验证、加载与执行
│   │   └── *.test.mjs               # colocated行为测试
│   ├── scripts/                     # build、mutation、real-browser E2E
│   ├── package.json / package-lock.json
│   └── test/skill-publish-workflow.test.js
├── skills/ego-browser/
│   ├── SKILL.md                     # agent workflow/ownership/handoff契约
│   ├── references/install.md        # macOS DMG/onboarding
│   ├── scripts/install.sh
│   └── learnings/                   # site-specific notes/tools/browser-tools
├── .claude* / .codex*               # 多 harness分发入口
├── README.md / AGENTS.md / install.md
└── LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `package/ego-browser/src/run.ts` | CLI effect入口 | stdin JS → AsyncFunction；统一context；hard stop时控制output flush |
| `package/ego-browser/src/helpers.ts` | Agent surface/ownership | task space create/use/claim/complete/handoff/takeover；site tool和facade |
| `package/ego-browser/src/ego-errors.ts` | stable terminal | error_code解析、owned wording、hard-stop marker、unknown code fallback |
| `package/ego-browser/src/browser-runtime.ts` | CDP/session | 15s request timeout、2s session TTL、重附着、10k event cap、dialog tracking |
| `package/ego-browser/src/element-resolver.ts` | target resolution | stale ref、role/name fallback、zero vs multiple match的transient/permanent分类 |
| `package/ego-browser/src/driver/observe.ts` | evidence surface | snapshot ref map重建、screenshot path、dialog/raw fallback |
| `package/ego-browser/src/learning/index.ts` | site skills | manifest声明、relative containment、dynamic import/evaluate工具 |
| `skills/ego-browser/SKILL.md` | 行为契约 | ownership、handoff、readback、semantic/visual/CDP三种workflow |

#### ⭐ 源码精读

**代码块 1：`runMain()` 执行 Agent 提交的任意 JS，这是最清楚的 authority boundary**  
来源：[`package/ego-browser/src/run.ts#L61-L130`](https://github.com/citrolabs/ego-lite/blob/c46a439e7fbad90ad33dbea6c6af329b6009809f/package/ego-browser/src/run.ts#L61-L130)

```typescript
export async function runMain(options: RunMainOptions = {}) {
  const argv = options.argv || process.argv.slice(2);
  if (argv[0] === "--doctor") return services.runDoctor(stdout);
  if (argv[0] === "--reload") {
    await services.resetConnection();
    return 0;
  }
  const code = options.stdinText !== undefined
    ? options.stdinText
    : await readAll(options.stdin || processStdin);
  if (!code.trim()) return 2;
  await execute(code, stdout);
  return 0;
}

async function execute(code: string, stdout: WritableLike) {
  const context = await executionContext();
  Object.assign(globalThis, context);
  const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
  const fn = new AsyncFunction(...Object.keys(context), `"use strict";\n${code}`);
  await fn(...Object.values(context));
}
```

逻辑摘要：它不是参数受限的 browser RPC，而是把 stdin code交给 Node `AsyncFunction`，helper只是便利surface；Agent代码同时在Node权限域运行。真实源码另有try/finally式screencast cleanup与hard-stop output处理。边界是 site/skill指令一旦诱导恶意JS，browser scope并不等于OS sandbox。

**代码块 2：`useOrCreateTaskSpace()` 不隐式 claim 用户空间，显式 ownership 才能转移**  
来源：[`package/ego-browser/src/helpers.ts#L193-L242`](https://github.com/citrolabs/ego-lite/blob/c46a439e7fbad90ad33dbea6c6af329b6009809f/package/ego-browser/src/helpers.ts#L193-L242)

```typescript
export async function useOrCreateTaskSpace(nameOrId) {
  const spaces = await listTaskSpaces();
  const existing = findMatchingTaskSpace(spaces, nameOrId);
  if (!existing) {
    if (typeof nameOrId === "number") throw new Error(`task space not found: ${nameOrId}`);
    return newTaskSpace(nameOrId);
  }
  if (isAgentOwned(existing.ownership)) {
    return selectTaskSpace(globalThis.ego, existing, "useOrCreateTaskSpace");
  }
  if (existing.ownership === "user") {
    return selectTaskSpace(globalThis.ego, existing, "useOrCreateTaskSpace");
  }
  throw new Error(`cannot use task space with ownership ${existing.ownership}`);
}

export async function claimTaskSpace(nameOrId) {
  const space = await findTaskSpace(nameOrId);
  return claimResolvedTaskSpace(space, "claimTaskSpace");
}
```

逻辑摘要：常规use不会自动扩大权限；user-owned被select后由binding抛稳定user-control错误，只有明确claim路径才转移ownership。边界是 `takeOverTaskSpace()` 源码没有ownership check，安全依赖SKILL.md中“必须用户明确确认”的行为契约，而不是代码强制。

**代码块 3：`browserCdp()` 对隐式 page session 的 lost错误只重附着一次**  
来源：[`package/ego-browser/src/browser-runtime.ts#L79-L143`](https://github.com/citrolabs/ego-lite/blob/c46a439e7fbad90ad33dbea6c6af329b6009809f/package/ego-browser/src/browser-runtime.ts#L79-L143)

```typescript
export async function browserCdp(method, params = {}, sessionId = undefined,
                                 timeoutMs = RESPONSE_TIMEOUT_MS) {
  const explicit = sessionId !== undefined;
  let effective = sessionId;
  if (!explicit && !BROWSER_LEVEL(method)) effective = await ensureSession();
  try {
    return await rawCdp(method, params, effective, timeoutMs);
  } catch (error) {
    const lost = SESSION_LOST.test(error?.message || "");
    if (lost && !explicit && !BROWSER_LEVEL(method)) {
      invalidateSession();
      const fresh = await ensureSession();
      return rawCdp(method, params, fresh, timeoutMs);
    }
    throw error;
  }
}
```

逻辑摘要：显式session和browser-level调用不被偷偷重定向；普通page调用可在stale session后重附着一次。`ensureSession()`还有2秒cache和`sessionInflight`去重。边界是error classification依赖message regex，且open issue #204说明event waiter仍可能未按active session过滤。

**代码块 4：stable error code 将用户接管变成不可绕开的 hard stop**  
来源：[`package/ego-browser/src/ego-errors.ts#L142-L159`](https://github.com/citrolabs/ego-lite/blob/c46a439e7fbad90ad33dbea6c6af329b6009809f/package/ego-browser/src/ego-errors.ts#L142-L159)

```typescript
export function buildEgoError(err: unknown, op?: string): Error & { error_code?: string } {
  const { code, message } = resolveEgoError(err);
  if (code === "EGO_TASK_SPACE_USER_IN_CONTROL" ||
      code === "EGO_TASK_SPACE_INACTIVE") {
    markHardStop(message);
  }
  const error: Error & { error_code?: string } = new Error(
    op ? `${op}: ${message}` : message,
  );
  if (code) error.error_code = code;
  return error;
}
```

逻辑摘要：hard stop在统一error birthplace被记录，即使上层Agent script catch异常，output sink也能丢弃普通缓冲输出并保留唯一指导；本机tests覆盖 swallowed/uncaught 两路。边界是stable code来自闭源binding，未知未来code只fallback native message，必须继续做兼容测试。

**代码块 5：元素歧义不是统一重试，0 match与multiple match分开**  
来源：[`package/ego-browser/src/element-resolver.ts#L46-L60`](https://github.com/citrolabs/ego-lite/blob/c46a439e7fbad90ad33dbea6c6af329b6009809f/package/ego-browser/src/element-resolver.ts#L46-L60)

```typescript
function matchCountKind(message: string): "transient" | "permanent" {
  const m = /matched (\d+)/.exec(message);
  const n = m ? Number(m[1]) : 0;
  return n > 1 ? "permanent" : "transient";
}

function selectorResolutionError(selector, result) {
  const message = exceptionText(result);
  if (/\bmatched \d+ elements\b/.test(message)) {
    return new ElementResolutionError(message, matchCountKind(message));
  }
  return new ElementResolutionError(`Invalid selector: ${selector}: ${message}`, "permanent");
}
```

逻辑摘要：0 match可能因页面尚未加载，可retry；multiple match是selector不唯一，盲重试不会解决，应永久失败并要求narrow。边界是classification仍从错误文案解析数字；open issue #275报告现实antd页面的`loc=unstable`和跨round ref失效仍造成操作不稳。

#### 依赖分析与供应链风险

- runtime package只有 `acorn ^8.16.0`；dev依赖包括 Rollup、TypeScript、esbuild、Prettier、lefthook。`package-lock.json` lockfile v3含resolved/integrity，本机 `npm ci --ignore-scripts`可复现安装29 packages。
- `package.json` 版本为 **0.1.0**，main skill frontmatter **1.2.6**，latest GitHub release **v1.2.3**，app版本又由issue报告为0.4.6.x；这是至少四个版本面，必须分别记录，不能笼统说“ego-lite 1.2.6”。
- 仓库没有根 `SECURITY.md`；有GitHub issue模板/CI，但未从本仓核验正式安全披露政策。
- 开源repo只含 harness/skill，真正 `globalThis.ego` binding、浏览器kernel改动、app DMG和Chrome data迁移不在本次源码；MIT repo许可不能自动外推到下载app。
- `run.ts`执行任意Node JS；`learning/index.ts`会dynamic import declared node tool、把browser tool source包装后evaluate。虽有relative containment/manifest declaration，内容安全仍需source review与最小权限。
- 本机 npm audit 0 vulnerabilities只是当前registry audit结果，不证明无未知漏洞；real browser E2E需要闭源app，本机未运行。

#### README / docs / release / issues / source 交叉核验

- README/AGENTS的stdin JS → helperContext → CDP路径与 `run.ts/helpers.ts/browser-runtime.ts`一致；task ownership和hard stop不是文档虚构，tests也真实覆盖。
- README声称macOS-only现状；install reference会下载DMG、移除quarantine、启动app并让用户迁移Chrome data。由于本机是WSL且cron无人，不执行该路径。
- latest GitHub release v1.2.3非常简短，而main skill metadata为1.2.6；issue #273提供app bundle drift实例。release、skill、app不能混为一个可验证artifact。
- issue #204与源码 `waitForBrowserEvent(predicate, timeout)` 的全局waiter结构相符：waiter自身没有session字段，而subscriber接口有session过滤；这是值得继续验证的identity gap。
- issue #270/#173与源码相符：`completeTaskSpace(...keep:false)`是主要cleanup路径，当前helpers未见idle TTL/reclaim；10k event cap只限制event buffer，不限制task-space/renderer数量。
- issue #192与SKILL frontmatter相符：描述要求“prefer ego-browser over web fetch or other tools”，确实可能过度触发静态GitHub/API查找；本次研究正是用`gh api/curl`而不是浏览器更合适。
- 本机299 tests通过，证明mock/FakeEgo、build/typecheck和unit/e2e harness在此commit成立；不证明真实app、cookie隔离、multi-space资源或redirect bug已解决。

#### 可复用经验

- 当 Agent与用户共享高权交互面时，应优先把 `owner/control_state/claim/handoff/terminal` 做成机器可读状态，并把用户接管设为hard stop，而不是靠模型从错误文案猜“要不要重试”；边界是takeover API仍应在宿主层加真实authorization。
- 当异步事件来自多个session/tenant时，应优先在注册与消费两端绑定 immutable session/scope identity，因为全局queue加predicate会把另一个页面的匹配事件误投给当前任务；边界是session id也必须处理detach/rotation。
- 当selector失败时，应优先区分 transient zero-match、permanent ambiguity、stale ref和user-control，不要统一retry，因为multiple match与权限拒绝重试只会放大错误；边界是classification不能只依赖脆弱文本。
- 当第三方skill宣称复用用户登录态时，应优先把它视为credential-equivalent authority surface，先做scope、allowed domains、read/write effect、handoff和receipt设计；边界是“数据留本地”不等于自动化获授权。
- 当能力有多个版本面（repo/release/skill/app/binding）时，应优先记录每层source ref并做conformance matrix，因为只写一个version会掩盖bundle drift；边界是矩阵仍要用真实app测试。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/scoped-event-hard-stop/` 做纯 fixture，不安装ego-lite：

1. 定义 `Event{scope_id,session_id,type,payload}`、`Waiter{expected_scope,expected_session,predicate}`、`ControlState{owner,status,revision}`。
2. 构造session A/B同URL同event type，验证B绝不能resolve A waiter。
3. 构造`user_in_control/inactive/ambiguous/zero_match/session_lost`，只允许zero-match和隐式session-lost进入bounded retry。
4. 即使模拟worker catch hard stop，也必须输出唯一terminal reason并阻止effect receipt。
5. 不调用真实browser、不读取cookies、不修改Hermes skills/config。

#### 风险边界

- **License**：GitHub API/root LICENSE为MIT；独立ego-lite app、Chromium、extensions、site tools和用户数据不自动由repo MIT覆盖。
- **维护活跃度**：repo API pushed为2026-08-15T09:56:46Z，但default main commit为2026-08-10；latest release v1.2.3、skill 1.2.6。活跃但version surface明显漂移。
- **安全风险**：继承Chrome登录态等同接触cookies/session；stdin任意Node JS、raw CDP、server/browser fetch、file upload/download、dynamic site tools都是高权effect面。
- **隐私风险**：snapshot、screenshot、site notes和browser fetch可能携带账号/页面私密信息；不能写shared raw或交给无关provider。
- **隔离/并发风险**：open issue #204的cross-session waiter、#270/#173的idle renderer积累、#267的cross-space DevTools都说明task space不应被当作强安全沙箱。
- **正确性风险**：unstable locator、跨round stale refs、redirect hangs、global mutable state/circular dependency会影响长任务；本机mock tests不能消除真实app gap。
- **供应链风险**：DMG/CDN、app bundle、skill bundle、repo package和site learning files是独立artifact；install脚本还会strip quarantine，不能无人值守执行。
- **不适用场景**：cron无人交互、WSL/Linux当前环境、静态GitHub/API查找、支付/发送/删除/账号设置、强租户隔离、无法人工处理login/captcha/handoff的任务。
- **不能自动执行**：不安装DMG/npx skill、不迁移Chrome data、不claim用户space、不调用raw CDP/登录态、不把ego-browser设为Hermes默认web工具。

#### ⭐ Skill 升格判断

**需二次验证**；ownership/hard-stop/session identity模式可抽象，ego-browser skill与app暂不沉淀。

- **可直接抽象**：stable terminal reason、user-control hard stop、explicit claim、per-session event identity、transient/permanent retry taxonomy。
- **需二次验证**：先跑pure fixture，再在未来隔离、无真实账号、低权公开页面环境做真实app conformance；特别复现issue #204、cleanup与version matrix。
- **暂不沉淀**：不复制上游`SKILL.md`、site learnings、install脚本、browser runtime或“prefer over all web tools”的触发描述。
- **升格结论**：优先更新已有effect-scope/subagent状态/verification契约；当前仅Hermes runtime candidate，不创建shared skill、不写curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/scoped-event-hard-stop/{schema.json,fixtures/,router.py,test_router.py,README.md}`。
2. **Hermes tool dispatcher**：未来任何长期browser/MCP/subagent event都携带`run_id/scope_id/session_id/owner/control_revision`；waiter消费前强匹配，不能只看payload。
3. **effect gate**：将`user_in_control/inactive`定义为terminal blocked，需要外部授权事件才能转移；Agent prose/自动retry不能改变owner。
4. **shared skill governance**：第三方skill触发描述先做routing conflict test；静态docs/repo/API继续优先`gh api/curl`，只有真实UI/login/rendered-state需求才候选browser。
5. **分层**：公开源码/API/test stdout留runtime，日报留inbox；任何cookies/snapshot/account data都不得写shared。OpenClaw当前不存在，不创建其adapter。

## 经验沉淀

1. 当自动审计或发布gate输出一个分数时，应优先同时记录每轴scorer version、coverage、measurement floor、instrument error与terminal reason，因为“0分/失败”可能是工具没跑、尺度漂移或真实回归三种不同事实；边界是receipt必须来自真实执行而非报告文本自述。
2. 当异步Agent共享browser、MCP、subagent或消息事件总线时，应优先把immutable `run/scope/session` identity写进waiter和event并在消费点重验，因为仅靠event type/predicate会发生跨任务串线；边界是session rotation需要明确迁移协议。
3. 当用户或另一个Agent持有控制权时，应优先将ownership denial建模为hard stop并要求显式授权事件，而不是让模型自行takeover/retry；边界是authorization必须由宿主验证，不能由assistant-authored prose伪造。
4. 当一个预测器用来决定是否执行昂贵或危险操作时，应优先用bounded probe验证高风险边界，并把probe failed/oom/refused/completed分开，因为预测公式和测试网格都可能漏掉真实shape；边界是probe也必须有资源上限。
5. 当第三方能力横跨repo、release、package、skill、app与native binding时，应优先逐层pin source ref和license并做conformance matrix，因为单一版本号/仓库许可会掩盖bundle drift与闭源authority；边界是pin不证明安全。
6. 当静态API/文档就能完成研究时，应优先使用`gh api/curl`而不是登录态browser，因为减少权限、隐私、交互和资源面；边界是必须渲染/认证/UI验证时才进入browser lane。

### 后续实验汇总

- `runtime/hermes/github-learning-poc/audit-noise-replay/`：per-axis coverage/floor/scorer/source receipt与离线replay。
- `runtime/hermes/github-learning-poc/scoped-event-hard-stop/`：scope/session waiter isolation、ownership hard stop和bounded retry。
- 两者都只用synthetic fixtures，不接provider/GPU/browser/cookie，不改config/provider/auth/env/cron/skills，不写curated active fact。

## 风险边界（跨项目）

1. **来源边界**：stars/forks/license/updated/pushed来自Repository API；commit/release/issues来自对应GitHub API；README/release/benchmark数字标明上游声明。
2. **实测边界**：Soup只验证compile与175个pure/core targeted tests；ego-lite只验证npm build/typecheck/mock/harness 299 tests。没有训练模型、GPU benchmark或真实browser app。
3. **权限边界**：不自动改Hermes模型/provider/auth/env/cron/skills，不调用OpenClaw，不安装第三方app/skill，不读取用户登录态。
4. **数据边界**：不下载私有数据/weights，不保存cookie/snapshot；公开repo clone/API留runtime且不是curated事实。
5. **许可边界**：Apache/MIT只对对应repo结论成立；外部weights/datasets/browser app/site tools/transitive deps单独审查。
6. **审计边界**：当前orchestrator仍以Markdown关键词计分，不能证明真实source/test receipts；本报告保存真实证据但尚未改审计器。
7. **长期记忆边界**：Candidate Facts/Skills只是二轮审计输入，未自动晋升`curated/memory/`。

## 明日继续

**最小动作**：先实现两个纯fixture POC并保存机器可读receipt；只有测试真实通过且与现有能力去重后，才提议更新shared skill。

1. `audit-noise-replay`：覆盖stable/noisy/error/missing/stale-scorer，要求offline replay verdict一致且instrument error不转成质量0分。
2. `scoped-event-hard-stop`：覆盖A/B session串线、user-control、inactive、zero/multiple match、session lost；只允许明确的bounded retry。
3. Soup继续：追踪issue #406是否把noise floor纳入config，并检查extras resolver冲突是否在后续commit修复；不得先装全量训练栈。
4. ego-lite继续：追踪#204/#270/#273/#275；若未来有隔离macOS环境，再用公开无登录页面做real app conformance，不在当前WSL cron安装。
5. 候选项目：`cordiverse/cordis`的spatiotemporal scope/fiber isolation可继续，但其README明示API不稳定，先读paper/source/tests再判断。

## 候选反哺

### Candidate Facts

- [ ] topic: gate必须区分instrument error、regression与unmeasured coverage | evidence: `Soup@33cce1a commands/ship.py`, `eval/gate.py`, v0.73.2 release及本机175 tests | 建议: update existing verification candidate | 安全级别: high
- [ ] topic: async event consumer必须绑定scope/session identity | evidence: `ego-lite@c46a439 browser-runtime.ts`与open issue #204 | 建议: create candidate pending real fixture | 安全级别: high
- [ ] topic: user-control应是不可自动绕过的hard stop | evidence: `ego-errors.ts`, `helpers.ts`, 本机299 tests | 建议: update effect-scope/subagent-state candidate | 安全级别: high
- [ ] topic: Soup当前extras解析存在all/MLX transformers约束冲突 | evidence: 本机真实uv resolver exit 1；`pyproject.toml` train `<5`与mlx-lm要求`>=5` | 建议: execution note/candidate only，不泛化到core/PyPI所有安装 | 安全级别: medium
- [ ] topic: ego-lite repo/release/skill/app存在多版本面漂移 | evidence: API release v1.2.3、main skill1.2.6、issue #273 | 建议: project risk candidate，后续版本需重验 | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: `evidence-noise-replay-contract` | 可复用场景: GitHub学习、教程学习、模型/agent eval、cron audit | 是否建议 shared: yes after fixture and dedupe | 原因: 跨Agent的scorer/coverage/error/receipt横切契约，优先更新existing verification skill
- [ ] 名称: `scoped-event-hard-stop` | 可复用场景: browser、MCP、subagent、parallel cron event routing | 是否建议 shared: yes after fixture | 原因: scope/session/ownership是Hermes与future-agent共同边界
- [ ] 名称: `external-capability-version-matrix` | 可复用场景: repo/release/package/skill/app/native多层接入 | 是否建议 shared: maybe/update governance | 原因: 与第三方skill install/governance重合，先去重不另建skill

### Candidate Open Questions

- [ ] 问题: 当前GitHub learning audit如何用真实sidecar receipt验证API/source/test覆盖，而非Markdown关键词？ | reason: adaptation | priority: high
- [ ] 问题: Soup issue #406修复后，noise floor policy/evidence config hash应该如何版本化而不把gate policy误当training recipe？ | reason: adaptation | priority: medium
- [ ] 问题: Soup的all/MLX resolver冲突是发布metadata bug、uv cross-split行为还是预期互斥extra，应如何对用户说明？ | reason: conflict | priority: high
- [ ] 问题: ego-lite issue #204在后续commit如何修复，download/network waiters是否都绑定active session？ | reason: gap | priority: high
- [ ] 问题: task space是便利隔离还是安全隔离，闭源app对cookie/storage/process的真实边界是什么？ | reason: gap | priority: high
- [ ] 问题: shared hub现有effect-scope/verification skills是否已覆盖ownership hard stop与session-scoped events，避免重复升格？ | reason: adaptation | priority: medium

### 不应自动落地

- 不安装Soup train/all/MLX extras，不下载模型/数据，不执行GPU/cloud/MCP mutation。
- 不安装ego-lite DMG/npx skill，不strip quarantine，不迁移Chrome profile，不读取或复用登录态。
- 不把第三方stdin JS/site learning直接暴露给Hermes高权terminal/file tools。
- 不修改provider/model/auth/env/cron/secret/skills，不调用或写入OpenClaw。
- 不把上游benchmark、issue复现或candidate直接写入curated active fact。
- 不复制两个项目源码/skill/docs到`capabilities/skills/`；只抽象并先做fixture。

## 报告与证据路径

- **Hermes inbox报告**：`inbox/hermes/daily/2026-08-16-github-learning.md`
- **运行证据**：`runtime/hermes/github-hot-project-learning/evidence/2026-08-16/`
- **项目卡片**：`runtime/hermes/github-learning/projects/MakazhanAlpamys-Soup.md`、`runtime/hermes/github-learning/projects/citrolabs-ego-lite.md`
- **经验追加**：`runtime/hermes/github-learning/lessons.md`
- **知识库projection（audit通过后由orchestrator复制）**：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-08-16-GitHub热门项目学习日报.md`
- **审计状态**：`runtime/hermes/github-hot-project-learning/status.json`
