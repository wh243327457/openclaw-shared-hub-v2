# 2026-08-15 GitHub 热门项目学习日报

> 执行器：Hermes。当前 OpenClaw runtime 不存在；本次未调用、启动、模拟或写入 OpenClaw。  
> 共享根：先运行 `python3 scripts/resolve_shared_root.py`，真实解析为当前 shared 根。  
> 研究窗口：2026-08-15 07:31–07:38（UTC+08:00）。Trending 通过 `curl` 读取，仓库元数据、commit、release、issues 均通过 `gh api` 读取。  
> 源码锚点：`cactus-compute/needle@4439dd02824ef655d1a6369760879fbee6fe36db`；`github/spec-kit@bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`。  
> 证据目录：`runtime/hermes/github-hot-project-learning/evidence/2026-08-15/`；Trending HTML 实际大小 652,800 bytes，SHA-256 为 `d4e2f3bc80cb4f99f02b8a6dfa4610eb8c00c2c7b36af43ed22e5695cef4ac2f`。  
> 数据边界：Stars、forks、updated/pushed 是查询时动态值；README 的模型大小、RAM、benchmark 等是上游声明。只有本报告明确列出的本机命令结果才算本机验证。

## 今日结论

今天的主线是：**把不确定的 Agent 选择放进确定性的执行外壳时，必须同时约束 schema、作用域、权限、状态与供应链。Needle 展示了“schema 编译约束 + 小模型本地路由”，但其便捷 `run()` 并不按 confidence 或 effect 自动拦截工具；Spec Kit 展示了“spec/plan/tasks + workflow 持久状态 + 多 Agent adapter”，但 Hermes 集成会直接写全局 skills，workflow shell step 仍以用户权限运行。对 Hermes/shared hub 最值得反哺的是一个窄的 `proposal → validate → authorize → execute → receipt` 契约，而不是自动安装任一上游项目。**

## 研究边界与真实验证

- **发现源**：`https://github.com/trending?since=daily` 的真实 HTML 中解析到 `cactus-compute/needle`、`github/spec-kit`、`infiniflow/ragflow`、`rustdesk/rustdesk`、`unslothai/unsloth`、`OpenCut-app/OpenCut` 等候选；Trending 只负责发现，关键元数据再由 GitHub Repository API 核验。
- **Needle 本机验证**：浅 clone 固定 main commit；`python3 -m compileall -q needle` 返回 exit 0；隔离 uv venv 安装 `.[test]` 后，`tests/test_tools.py` 为 **11 passed in 2.13s**。没有运行 engine-backed inference tests、没有下载或加载 `libneedle`、没有调用模型、没有执行真实工具，所以模型质量、14MB/28MB、confidence calibration 与本地推理速度均为**待核验/上游声明**。
- **Spec Kit 本机验证**：浅 clone 固定 main commit；`python3 -m compileall -q src` 返回 exit 0；隔离 uv venv 安装 `.[test]` 后，`tests/integrations/test_integration_hermes.py` 与 `tests/test_download_security.py` 合计 **231 passed in 4.21s**。测试使用临时 home，没有写当前 `~/.hermes`；没有执行 `specify init` 到真实项目、没有运行 shell workflow、没有安装 bundle/extension。
- **不自动执行**：不修改 Hermes 配置、模型、provider、auth、env、cron 或现有 skills；不把第三方工具接入生产 effect；不将候选直接写入 `curated/memory/`。

## 项目速览

下表均来自 2026-08-15 07:31–07:38（UTC+08:00）期间的真实 `gh api repos/{owner}/{repo}` 响应。`NOASSERTION` 表示 GitHub API 未识别仓库级许可证，不等于没有许可证；Stars 会变化。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed（UTC） | 今日判断 |
|---|---:|---:|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) | 128,493 | 11,483 | Python | MIT | 2026-08-14T23:31:51Z / 2026-08-14T16:44:52Z | **深读：SDD、workflow 状态、Hermes adapter、安全下载** |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 88,393 | 10,381 | Go | Apache-2.0 | 2026-08-14T23:30:29Z / 2026-08-14T14:26:58Z | RAG/Agent context layer；规模较大，今日不展开 |
| [unslothai/unsloth](https://github.com/unslothai/unsloth) | 71,488 | 6,447 | Python | Apache-2.0 | 2026-08-14T23:30:13Z / 2026-08-14T22:46:48Z | 本地训练/推理候选，依赖与 GPU 面未核验 |
| [rustdesk/rustdesk](https://github.com/rustdesk/rustdesk) | 120,631 | 18,463 | Rust | AGPL-3.0 | 2026-08-14T23:27:31Z / 2026-08-14T17:04:14Z | 高权远程桌面；license/effect 面不适合今日快速迁移 |
| [OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) | 83,135 | 8,230 | TypeScript | MIT | 2026-08-14T23:31:17Z / 2026-08-10T16:38:36Z | 视频编辑候选，与今日 Agent 外壳主线较弱 |
| [smicallef/spiderfoot](https://github.com/smicallef/spiderfoot) | 20,933 | 3,341 | Python | MIT | 2026-08-14T23:31:39Z / 2026-04-13T19:43:06Z | OSINT 工具，网络与隐私边界较大，未深读 |
| [cactus-compute/needle](https://github.com/cactus-compute/needle) | 5,583 | 372 | Python | MIT | 2026-08-14T23:28:33Z / 2026-08-14T19:00:52Z | **深读：小模型 tool calling、schema、confidence、量化** |
| [ToolJet/ToolJet](https://github.com/ToolJet/ToolJet) | 39,058 | 5,262 | JavaScript | AGPL-3.0 | 2026-08-14T23:26:55Z / 2026-08-14T14:11:22Z | 内部工具/Agent 平台，部署与 AGPL 边界较重 |

### 筛选说明

- `cactus-compute/needle` 是当日 Trending 候选，且上游前一日修复了 native envelope/JSON error handling；它能直接检验“模型提议与工具执行是否真正分离”。
- `github/spec-kit` 也是当日 Trending 候选，并已存在 Hermes integration；它能直接检验“跨 Agent 模板、全局 skill 安装、持久 workflow 与 shared hub 分层是否兼容”。
- 两项目 GitHub API license 都是 MIT；但 Needle 的仓库 `LICENSE` 是 MIT，而 `pyproject.toml:7` 声明 `Apache-2.0`，存在真实元数据冲突，发布包许可需要维护者确认，不能只看一个字段。

## 深读项目

### 项目 1：cactus-compute/needle

- **URL**：https://github.com/cactus-compute/needle
- **Stars / Forks / Language / License（GitHub API）**：**5,583 / 372 / Python / MIT**。
- **查询时 updated / pushed**：2026-08-14T23:28:33Z / 2026-08-14T19:00:52Z。
- **固定源码版本**：`4439dd02824ef655d1a6369760879fbee6fe36db`，commit message 为 `fix: improve error handling in Needle.complete method for needle_complete and JSON parsing`。
- **release/tag / issues 证据**：GitHub Releases API 返回空数组，但 Tags API 有 `v2.0.4`（commit `c949b6ce...`）等 tag；因此不能把 tag 自动称为 GitHub Release。Open issue #67 报告 structured extraction 的 malformed JSON、semantic false positive、nested array omission 与 confidence 暴露问题；open issue #36 质疑 checkpoint/LoRA 使用 pickle 的反序列化风险。

#### 一句话判断：为什么值得学

Needle 值得学的不是“14MB 就可以安全执行工具”这个宣传句，而是它把 Python 类型/docstring 转成 JSON schema、再交给 grammar-constrained native engine；同时源码清楚暴露了一个关键边界：**schema 合法只约束输出形状，不证明参数被输入证据支持，便捷 `run()` 也没有内建 confidence/effect authorization gate。**

#### 解决的问题：替代了什么旧做法

1. 替代把完整大模型与网络服务放到微型设备：README 声称把 45M 参数模型与 engine 打成单一 `.cact`/native runtime；本机未验证模型体积与 RAM。
2. 替代仅靠 prompt 请求 JSON：函数签名、`Literal`、`Annotated[Field]` 与 Pydantic schema 被转换成 JSON Schema，README/docs 声称 grammar 在 decode 时约束 call。
3. 替代所有工具都塞进上下文：README/docs 声称超过 5 个工具时通过内建 retrieval head 选 top five；本机未运行该路径。
4. 替代 Python 解释器内的纯 Python inference：Python wrapper 通过 `ctypes.CDLL` 绑定按平台下载的 native engine。
5. 但它**没有替代宿主授权**：`Needle.run()` 只按 call name 查 Python function 后执行，源码中未检查 confidence threshold、tool effect、target scope、用户批准或 retry policy。

#### 架构 / 实现与数据流

```text
Python function / Pydantic model / raw schema
        │ build_schema() / pydantic_schema()
        ▼
JSON tool catalog + optional system facts
        │ Needle.__init__ → bytes
        ▼
ctypes native boundary
        │ needle_init(system, tools, tool_index)
        │ needle_complete(text, token_budget, buffer)
        ▼
JSON envelope: type / calls / confidence / metrics
        │
        ├── complete(): caller owns validation + execution
        └── run(): name lookup → Python fn(**arguments) → JSON result → next turn

Training/export lane（与在线调用分离）
JSONL → tokenizer → JAX/Flax + LoRA → pickle checkpoint/adapter
      → CQ quantization + fixed tensor order → .cact → native engine
```

核心实现分成四层：`needle/agent/` 负责 schema/fetch，`needle/__init__.py` 负责 native binding 和 agent loop，`needle/model/` 负责 JAX 架构、训练、量化和 export，`tests/` 分离 schema、build、quantization 与 engine-backed inference。模型提议与 Python effect 在 `run()` 中会合，因此该函数是必须额外加 host policy 的最终 chokepoint。

#### Repo tree 摘要

固定 commit 共 43 个 tracked files：

```text
needle/
├── needle/
│   ├── __init__.py          # ctypes engine binding、Needle.complete/run/extract
│   ├── cli.py               # fetch/playground/finetune/build 等 CLI
│   ├── agent/
│   │   ├── tools.py         # Python typing/docstring/Pydantic → JSON schema
│   │   └── fetch.py         # 平台 tag、Hugging Face wheel、native library 提取
│   ├── model/
│   │   ├── architecture.py  # Simple Attention Network、Engram、GQA、Hadamard MLP
│   │   ├── quantize.py      # fake quant、CQ codebook/Hadamard、mixed bits
│   │   ├── finetune.py      # data generation、LoRA、pickle adapter
│   │   ├── export.py        # .cact header/tensor directory/packed weights
│   │   └── run.py           # pickle checkpoint load/merge
│   └── playground/          # 本地 HTTP UI
├── tests/                   # tools、inference、quantization、finetune、build
├── doc/apis.md              # call contract、confidence、offline setup
├── doc/finetuning.md
├── pyproject.toml / requirements.txt
├── README.md
└── LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `needle/agent/tools.py` | schema compiler | 解析 typing、Literal、list/dict、Pydantic、docstring Args、Field constraints |
| `needle/__init__.py` | runtime boundary | native library lookup/download、ctypes signature、complete envelope parsing、run tool loop |
| `needle/agent/fetch.py` | native supply chain | 根据 OS/arch 生成 wheel 名，从 `Cactus-Compute/needle2` 下载并提取动态库 |
| `needle/model/architecture.py` | model architecture | GQA、RoPE、Engram hashed n-gram table、Sinkhorn、多 residual lanes、Hadamard MLP |
| `needle/model/quantize.py` | quantization | group padding、Hadamard rotation、Lloyd-Max/CQ codebook、mixed precision |
| `needle/model/export.py` | deploy artifact | fixed 120-byte header、nameless tensor directory、64-byte alignment、packed CQ weights |
| `needle/model/finetune.py` / `run.py` | train checkpoint | OpenRouter synthetic data、LoRA、pickle dump/load；属于不可信 artifact 风险面 |
| `tests/test_tools.py` | deterministic schema tests | 本机实际运行 11 tests 全部通过 |

#### ⭐ 源码精读

**代码块 1：`build_schema(fn)` 把函数接口转换成机器约束**  
来源：[`needle/agent/tools.py#L110-L140`](https://github.com/cactus-compute/needle/blob/4439dd02824ef655d1a6369760879fbee6fe36db/needle/agent/tools.py#L110-L140)

```python
def build_schema(fn):
    signature = inspect.signature(fn)
    try:
        hints = typing.get_type_hints(fn, include_extras=True)
    except Exception:
        hints = {}
    description, arg_docs = _parse_doc(fn.__doc__)
    properties, required = {}, []
    for name, param in signature.parameters.items():
        if name in ("self", "cls") or param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        annotation = hints.get(name, param.annotation)
        schema = _json_type(annotation)
        if name in arg_docs and "description" not in schema:
            schema["description"] = arg_docs[name]
        field = _field_of(annotation, param.default)
        if field:
            field.apply(schema)
        properties[name] = schema
        has_default = param.default is not param.empty and not isinstance(param.default, Field)
        if not has_default and not _is_optional(annotation):
            required.append(name)
    return {"name": fn.__name__, "parameters": {"type": "object", "properties": properties, "required": required}}
```

逻辑摘要：宿主从真实 Python signature、resolved type hints、docstring 和 Field metadata 生成 schema；这是可确定性测试的外壳。但 `_json_type()` 对无法识别的复杂类型会退回 string，union 只取第一个非 None 类型，返回值注解也不进入工具 schema；因此“成功生成 schema”不等于完整表达 Python 语义。

**代码块 2：`Needle.run()` 是模型提议进入真实 effect 的 chokepoint**  
来源：[`needle/__init__.py#L119-L139`](https://github.com/cactus-compute/needle/blob/4439dd02824ef655d1a6369760879fbee6fe36db/needle/__init__.py#L119-L139)

```python
def run(self, query, max_steps=8, max_new_tokens=256):
    response = self.complete(query, max_new_tokens)
    executed = []
    for _ in range(max_steps):
        calls = response.get("function_calls") or []
        if response.get("type") != "call" or not calls:
            break
        results = []
        for call in calls:
            fn = self._functions.get(call.get("name"))
            if fn is None:
                results.append({"error": "unknown tool: " + str(call.get("name"))})
                continue
            try:
                results.append(fn(**(call.get("arguments") or {})))
            except Exception as exc:
                results.append({"error": str(exc)})
        executed.extend(results)
        response = self.complete(json.dumps(results, default=_jsonable), max_new_tokens)
    response["results"] = executed
    return response
```

逻辑摘要：有 `max_steps` 和函数名 allowlist，但没有检查 `response.success`、`confidence`、参数证据、tool effect、scope、用户批准、deadline 或幂等 key；tool exception 也被转成字符串继续反馈给模型。README 的 confidence threshold 是调用方责任。对 Hermes 来说只能把 Needle 放在 proposal lane，不能直接把高权 tools 交给 `run()`。

**代码块 3：`cq_quantize()` 的 Hadamard 旋转 + group codebook 量化**  
来源：[`needle/model/quantize.py#L134-L147`](https://github.com/cactus-compute/needle/blob/4439dd02824ef655d1a6369760879fbee6fe36db/needle/model/quantize.py#L134-L147)

```python
def cq_quantize(w, bits, group_size=128, codebook=None):
    cb = codebook if codebook is not None else jnp.asarray(_cq_codebook_np(bits, group_size))
    D, g = w.shape[-1], group_size
    pad = (-D) % g
    wp = jnp.pad(w, [(0, 0)] * (w.ndim - 1) + [(0, pad)]) if pad else w
    groups = wp.reshape(*wp.shape[:-1], -1, g).astype(jnp.float32)
    H = jnp.asarray(_cq_hadamard_np(g))
    rot = groups @ H
    norm = jnp.sqrt(jnp.sum(rot ** 2, axis=-1, keepdims=True))
    unit = rot / jnp.maximum(norm, 1e-12)
    norm = norm.astype(jnp.float16).astype(jnp.float32)
    deq = (_cq_nearest(unit, cb) * norm) @ H
    deq = deq.reshape(wp.shape).astype(w.dtype)
    return deq[..., :D] if pad else deq
```

逻辑摘要：最后一维补齐 group，正交 Hadamard 旋转后拆单位方向与范数，以最近 codebook centroid 近似方向，再逆旋转；这是训练/评估用的数值路径。它证明代码确有 CQ 实现，但不证明 README 的质量、速度、14MB 或 28MB 指标，本机也未执行模型 build/benchmark。

**代码块 4：native engine 的下载与加载没有在调用点固定 revision/hash**  
来源：[`needle/agent/fetch.py#L52-L64`](https://github.com/cactus-compute/needle/blob/4439dd02824ef655d1a6369760879fbee6fe36db/needle/agent/fetch.py#L52-L64)

```python
def fetch_library(version, dest_dir, tag=None):
    from huggingface_hub import hf_hub_download
    tag = tag or _platform_tag()
    wheel = "cactus_needle-{}-py3-none-{}.whl".format(version, tag)
    path = hf_hub_download(repo_id=HF_REPO, filename="python/" + wheel, repo_type="model")
    lib = _lib_name_for(tag)
    with zipfile.ZipFile(path) as archive:
        data = archive.read("needle/" + lib)
    out = os.path.join(dest_dir, lib)
    with open(out, "wb") as handle:
        handle.write(data)
    return out
```

逻辑摘要：版本和平台决定文件名，但 `hf_hub_download` 调用没有显式 `revision`、expected SHA-256 或签名；随后直接从 wheel 取动态库，`ctypes.CDLL` 会执行其 native 初始化。Hugging Face 客户端自身缓存机制不能替代应用层 pin/receipt。这也是本次刻意不运行 engine-backed tests 的原因之一。

#### 依赖分析与供应链风险

- `pyproject.toml` runtime dependencies：`huggingface_hub`、`numpy`、`jax`、`jaxlib`、`flax>=0.10.2`、`optax`、`sentencepiece`；除了 Flax 下界，均未 pin 版本。`requirements.txt` 也全部无版本。
- optional `gpu` 使用 `jax[cuda12]`；`metal` 则固定 `jax/jaxlib 0.4.38`、`flax 0.10.2`、`optax 0.2.4`。这会形成 CPU/GPU/Metal 三套不同解析图，需分别锁定和测试。
- 隔离安装本次解析并安装了 50 packages；仅运行 schema tests。安装成功不能外推 native engine、accelerator、LoRA 或 export 兼容。
- `finetune.py` 和 `run.py` 真实存在 `pickle.load()`；不可信 `.pkl` checkpoint/adapter 可触发 Python 反序列化代码执行。`.cact` 是另一种 fixed binary，但 build 前仍可能先读 pickle。
- `fetch_library()` 获取并加载 native dynamic library；需要固定 repo revision/file hash、限制下载大小、验证 wheel member 和记录 engine receipt。当前调用点未实现这些宿主级检查。
- **License 冲突**：GitHub API 和根 `LICENSE` 是 MIT，`pyproject.toml` 却写 Apache-2.0。发布包 metadata、源仓库许可与模型/weights 许可不能自动视为一致；在维护者修复或解释前，只适合机制研究，不复制模型/engine 到 shared。

#### README / docs / tag / issues / source 交叉核验

- README/docs 的“函数签名变 schema、`complete()` 返回 call、`run()` 执行 loop”与 `tools.py`、`__init__.py` 一致；但 docs 要求调用方按 confidence 决定 act/escalate，而 `run()` 本身没有 threshold。
- README 声称 grammar 保证 JSON/schema conformance；open issue #67 在前一 commit 报告 malformed locale number。当前 main commit新增 native rc 与 JSON parse error handling，能把 malformed envelope 转成 `RuntimeError`，但本机没有 native engine，**修复效果待核验**。
- Issue #67 还给出 schema-valid 但语义不 grounded 的例子，说明 grammar constraint 与 semantic correctness 必须分开；这是上游 issue 复现，不是本机模型复现。
- Issue #36 指出 pickle 风险；源码搜索确认当前 main 仍在 checkpoint/LoRA 路径使用 `pickle.load`，所以该风险面仍存在。
- Tags API 有 v2.0.4，但 Releases API为空；项目版本、engine version、tag、package metadata 必须分别记录，不能用“latest release”笼统替代。

#### 可复用经验

- 当小模型负责 tool selection 时，应优先把它限制为 **proposal generator**，再由宿主在调用点验证 `success + confidence policy + schema + effect + scope + authorization`；边界是 confidence 不是授权，也不能证明语义 grounded。
- 当 JSON grammar 能保证输出形状时，应优先继续做 source-grounding 与业务 invariant 检查，因为 schema-valid enum/number 仍可能是错误值；边界是确定性 validator 只能覆盖已编码规则。
- 当运行时需要自动下载并加载 native library 时，应优先固定 immutable revision/hash、限制 archive/member、记录平台与 engine receipt，再允许 load；边界是 hash 只证明字节身份，不证明无漏洞。
- 当训练 artifact 使用 pickle 时，应优先把不可信 checkpoint 隔离为拒绝/转换 lane，不能在高权 Agent 进程中直接加载；边界是迁移到安全 tensor format 仍需 shape/dtype/size budget。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/proposal-effect-gate/` 做**纯 Python synthetic fixture**，不加载 Needle engine：

1. 定义 `ToolProposal{name,args,confidence,success,source_ref}` 与 host-owned `ToolPolicy{effect,scope,min_confidence,requires_approval}`。
2. 构造 safe read、write、network、unknown-tool、low-confidence、schema-valid-but-business-invalid 六类 fixture。
3. 只有 `validate_schema → validate_business → authorize_effect_scope` 全通过才调用 mock function；其他返回 `blocked/denied/failed` 与 reason code。
4. 记录 proposal hash、policy revision、decision、mock effect receipt；验证 model prose 无法扩大权限。
5. 不安装 Needle、不下载 native library、不修改 Hermes tools/config。

#### 风险边界

- **License**：API/根 LICENSE 为 MIT，但 package metadata 为 Apache-2.0；模型 weights、native engine 与发布包许可范围待核验。
- **维护活跃度**：pushed 为 2026-08-14T19:00:52Z，最近 5 个 API commits 集中在 engine error、version、offline setup；活跃也意味着 package/engine/tag contract 快速漂移。
- **安全风险**：自动 native download/load、pickle checkpoint、Python tool execution、OpenRouter synthetic-data egress 都是 authority/data surfaces；`run()` 未强制 confidence/effect gate。
- **正确性风险**：grammar/schema 不能保证 grounded；issue #67 报告 nested omission、semantic false positive、duplicate calls。当前修复只在静态源码层核验，native 复现待核验。
- **供应链风险**：runtime dependencies 大多不 pin；JAX accelerator variants、HF model repo、wheel dynamic library 与 weights/package version是多个独立版本面。
- **不适用场景**：支付、删除、发送、生产写入、密钥操作、强租户隔离、高可靠 extraction，除非宿主先加独立授权、业务验证、沙箱与 receipt。
- **不能自动执行**：不把当前 Hermes 的 `terminal/write_file/patch` 直接暴露给 Needle；不加载未知 `.pkl/.cact/.so`；不把 README benchmark 晋升为事实。

#### ⭐ Skill 升格判断

**需二次验证**，只抽象 host gate，不迁移 Needle 模型/runtime。

- **可迁移候选**：`proposal-effect-gate` 的 agent-neutral schema；与既有 effect-scope、verification-first、subagent 四状态候选去重后，可能更新现有 shared workflow。
- **需二次验证**：先跑 synthetic fixtures，再在隔离、低权、无生产凭据的 profile 中接一个纯函数 toy tool，比较 proposal、decision 与 effect receipt；native engine hash/revision也必须记录。
- **暂不沉淀**：不复制模型权重、native library、CQ/JAX training code、pickle artifact、README benchmark 或 Needle-specific confidence threshold。
- **升格结论**：当前仅为 Hermes runtime POC candidate，不创建 shared skill、不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **Hermes runtime POC**：`runtime/hermes/github-learning-poc/proposal-effect-gate/{schema.json,policies.json,fixtures/,validate.py,test_gate.py,README.md}`，只用 mock tools。
2. **Hermes 工具入口**：若验证通过，在 host-owned tool dispatcher 增加 `effect/scope/approval/policy_revision` 检查；模型只能提交 proposal，不能直接调用底层 Python function。
3. **shared 研究契约**：在现有 GitHub learning/verification skill 中要求区分 `shape_valid`、`grounded`、`authorized`、`executed`、`receipt_verified`，避免把 schema-valid 投影为完成。
4. **分层**：clone、API JSON、test stdout 留 `runtime/hermes/`；本日报留 `inbox/hermes/daily/`；只有跨项目稳定 invariant 经评分、证据、去重、脱敏与审查后才进入 curated。
5. **OpenClaw 边界**：当前禁止且不存在，不调用、不写 adapter；未来 Agent 只能复用 agent-neutral schema，必须重新做其真实 tool chokepoint conformance。

### 项目 2：github/spec-kit

- **URL**：https://github.com/github/spec-kit
- **Stars / Forks / Language / License（GitHub API）**：**128,493 / 11,483 / Python / MIT**。
- **查询时 updated / pushed**：2026-08-14T23:31:51Z / 2026-08-14T16:44:52Z。
- **固定源码版本**：`bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`，commit message 为 `Add SpecAssay bundle to community catalog (#4125)`；`pyproject.toml` 此时为 `0.16.5.dev0`。
- **release / issues 证据**：最新 release `v0.16.4` 发布于 2026-08-14T15:48:31Z；body 包含 workflow validation、RunState TOCTOU、archive manifest UTF-8、auth host pattern、bundle integration 等修复。Open issue #4128 报告多 Agent 共用 `.specify/feature.json` 的 write-write race；closed issue #4067 记录 Junie 对 dotted command filename 不识别，说明每个 Agent adapter 必须有真实行为测试。

#### 一句话判断：为什么值得学

Spec Kit 值得学的是把 constitution/spec/plan/tasks/implementation 变成版本化 artifact，并用 integration adapter、workflow state、bundle provenance 和安全下载将其落到 30+ Agent；对当前 Hermes/shared hub 更重要的反面教材是：**“支持 Hermes”不等于可以直接安装到当前 profile——其 Hermes adapter 写全局 `~/.hermes/skills`，卸载还会删除全部 `speckit-*` 目录，必须先做 ownership/manifest/diff/rollback 设计。**

#### 解决的问题：替代了什么旧做法

1. 替代“直接让 coding Agent 写代码”：constitution → specify → clarify → plan → tasks → analyze/checklist → implement/converge 形成可审查阶段。
2. 替代每个 Agent 手工维护模板：integration registry/registrar 将同一 command template 渲染为 agent-specific command/skill 文件、参数占位符和调用分隔符。
3. 替代 workflow 只存在对话中：`RunState` 持久化 `state.json/inputs.json/workflow.yml/log.jsonl`，支持 pause/fail 后 resume。
4. 替代角色环境逐组件手装：bundle manifest 把 extension/preset/step/workflow 组成版本化计划，并记录贡献 provenance、引用计数和 bounded rollback。
5. 替代无界下载/解压：`_download_security.py` 约束 scheme、response bytes、archive format、entry/member/total size、path traversal、symlink/hardlink 与 Unicode/Windows path。
6. 但它没有提供 OS sandbox：workflow source 注释明确 `requires` 是 advisory，shell steps 以用户权限运行；gate 是流程控制，不是内核隔离。

#### 架构 / 实现与数据流

```text
Core templates + scripts + constitution/spec/plan/tasks artifacts
        │
        ├── Integration registry / CommandRegistrar
        │       ├── command-layout agents
        │       └── skills-layout agents（含 Hermes）
        │
        ├── Extension / Preset overlay stack
        │       project override > preset > extension > core
        │
        ├── Bundle resolver → install plan → primitive installers
        │       provenance records + conflict/refcount + bounded rollback
        │
        └── Workflow YAML
                load → resolve inputs → validate → RunState.create
                → step registry(command/prompt/shell/gate/control-flow/fan-out)
                → state save after step → pause/fail/resume/completed

Remote catalog/archive
        → URL/redirect policy → bounded read → format check
        → safe extraction → component validation/install
```

对 shared hub 最相关的是三条状态线：模板/skill 的 ownership，workflow 的 run state，bundle 的 component provenance。三者不能用一份 prose 或一个 `completed` flag 代替。

#### Repo tree 摘要

固定 commit 共 539 个 tracked files：

```text
spec-kit/
├── src/specify_cli/
│   ├── integrations/          # 30+ Agent adapter；含 hermes/__init__.py
│   ├── agents.py             # command registrar、frontmatter/path rewrite/containment
│   ├── workflows/            # engine、expression、catalog、11 类 step
│   ├── bundler/              # manifest/model/resolver/installer/provenance
│   ├── extensions/ / presets/# capability 与 template overlay
│   ├── _download_security.py # bounded HTTP/archive security primitives
│   └── _version.py           # self check/upgrade/verify/rollback guidance
├── templates/commands/       # constitution/specify/plan/tasks/implement 等源模板
├── scripts/{bash,powershell,python}/
├── workflows/                # workflow catalog/schema/architecture
├── extensions/ / presets/    # bundled + catalog content
├── bundles/                  # community bundle catalog snapshot
├── tests/                    # 161 tracked test files，含 Hermes/security/workflow/bundler
├── docs/ / examples/ / integrations/
├── pyproject.toml
├── SECURITY.md
└── LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/specify_cli/integrations/hermes/__init__.py` | Hermes adapter | 将 core templates 写到全局 skills；创建本地 marker；构建 `hermes chat -Q` dispatch；teardown 删除 `speckit-*` |
| `src/specify_cli/agents.py` | cross-Agent registrar | registry 单一配置源、frontmatter parser、path rewrite、containment、agent-specific filename/placeholder |
| `src/specify_cli/workflows/engine.py` | durable workflow | YAML validation、RunState atomic save/load、execute/resume、nested steps/fan-out、terminal status |
| `src/specify_cli/workflows/base.py` | typed state | StepContext、StepResult、StepStatus、RunStatus |
| `src/specify_cli/_download_security.py` | supply-chain boundary | HTTPS/loopback、bounded read、ZIP/tar format与安全提取、member预算 |
| `src/specify_cli/bundler/services/installer.py` | bundle effect | ownership/refcount、scoped rollback、record-on-success、idempotent refresh |
| `workflows/ARCHITECTURE.md` | docs contract | 11 step types、state paths、nested resume limitation、catalog cache |
| `tests/integrations/test_integration_hermes.py` | Hermes fixtures | 临时 home 下验证 global writes、marker、uninstall；本机定向测试通过 |

#### ⭐ 源码精读

**代码块 1：`HermesIntegration.setup()` 直接写全局 Hermes skills**  
来源：[`src/specify_cli/integrations/hermes/__init__.py#L76-L218`](https://github.com/github/spec-kit/blob/bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c/src/specify_cli/integrations/hermes/__init__.py#L76-L218)

```python
def setup(self, project_root, manifest, parsed_options=None, **opts):
    templates = self.list_command_templates()
    if manifest.project_root != project_root.resolve():
        raise ValueError("manifest.project_root does not match project_root")

    global_skills_dir = Path.home() / ".hermes" / "skills"
    global_skills_dir.mkdir(parents=True, exist_ok=True)
    created = []
    for src_file in templates:
        # parse frontmatter, render template, rebuild skill metadata
        skill_name = f"speckit-{src_file.stem.replace('.', '-')}"
        skill_dir = global_skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_bytes(skill_content.replace("\r\n", "\n").encode("utf-8"))
        created.append(skill_file)

    (project_root / ".hermes" / "skills").mkdir(parents=True, exist_ok=True)
    return created
```

逻辑摘要：manifest root containment 是积极检查，frontmatter 也做 line-anchored parse；但 global skills 不属于 project manifest 的普通文件清单。测试与 teardown 注释明确，全局 modified skill 仍会删除，且 teardown 遍历删除所有 `speckit-*`。当前 shared hub 以 `capabilities/skills` 为共享能力真相层，所以不能无人值守运行该 setup/teardown。

**代码块 2：`RunState.save()` 用锁 + temp + `os.replace` 持久化 run snapshot**  
来源：[`src/specify_cli/workflows/engine.py#L690-L737`](https://github.com/github/spec-kit/blob/bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c/src/specify_cli/workflows/engine.py#L690-L737)

```python
def save(self) -> None:
    runs_dir = self.runs_dir
    runs_dir.mkdir(parents=True, exist_ok=True)
    with self._lock:
        self.updated_at = datetime.now(timezone.utc).isoformat()
        state_data = {
            "run_id": self.run_id,
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "current_step_index": self.current_step_index,
            "current_step_id": self.current_step_id,
            "step_results": self.step_results,
            "workflow_dir": self.workflow_dir,
            "error": self.error,
        }
        self._atomic_write_json(runs_dir / "state.json", state_data)
        self._atomic_write_json(runs_dir / "inputs.json", {"inputs": self.inputs})

@staticmethod
def _atomic_write_json(path, data):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise
```

逻辑摘要：同一进程内用 lock 避免 fan-out mutation 与 serialization 竞态，单文件写采用 atomic replace；`load()` 还在构造路径前验证 run_id，避免 traversal。边界是 `state.json` 与 `inputs.json` 是两次 replace，不是跨文件事务；不同进程同 run_id 仍只有 last-writer 语义。workflow docs 也承认 nested step pause 后 resume 会重跑 parent body。

**代码块 3：`is_https_or_localhost_http()` 与 bounded read 把下载前置条件写进代码**  
来源：[`src/specify_cli/_download_security.py#L336-L429`](https://github.com/github/spec-kit/blob/bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c/src/specify_cli/_download_security.py#L336-L429)

```python
def is_https_or_localhost_http(url: str) -> bool:
    parsed = _parse_url(url)
    if parsed is None:
        return False
    return parsed.scheme == "https" or (
        parsed.scheme == "http" and _is_definite_loopback_host(parsed.hostname)
    )

def read_response_limited(response, *, max_bytes=MAX_DOWNLOAD_BYTES,
                          error_type=ValueError, label="download") -> bytes:
    _validate_max_bytes(max_bytes)
    try:
        return _read_limited(response, max_bytes)
    except _ReadLimitExceeded:
        raise error_type(f"{label!r} exceeds maximum size of {max_bytes} bytes")
```

逻辑摘要：只有 HTTPS 或 canonical loopback HTTP 进入下载路径；ambiguous numeric/Unicode/unspecified address 不授权 HTTP。read loop 每次最多 64 KiB，累计到上限后一字节即失败。代码注释坦白 DNS/hosts alias 的 connection-level rebinding 仍需外部保护，因此这不是完整 SSRF sandbox。

**代码块 4：`install_bundle()` 只回滚本次新装组件，并在全成功后写 provenance**  
来源：[`src/specify_cli/bundler/services/installer.py#L59-L177`](https://github.com/github/spec-kit/blob/bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c/src/specify_cli/bundler/services/installer.py#L59-L177)

```python
def install_bundle(project_root, plan, installer, manifest=None, refresh=False):
    records = load_records(project_root)
    result = InstallResult(bundle_id=plan.bundle_id)
    contributed, done = [], []
    try:
        for component in plan.components:
            if installer.is_installed(project_root, component):
                result.skipped.append(component)
                continue
            installer.install(project_root, component)
            done.append(component)
            result.installed.append(component)
            contributed.append(component)
    except Exception as exc:
        _rollback(project_root, installer, done)
        raise BundlerError("Failed to install bundle; no changes were recorded") from exc

    record = InstalledBundleRecord.create(
        bundle_id=plan.bundle_id, version=plan.version, components=contributed
    )
    save_records(project_root, upsert_record(records, record))
    return result
```

逻辑摘要：真实源码比片段还会区分本 bundle、其他 bundle 与独立安装组件，避免 update/remove 误归属；失败只回滚本次 `done`，不是全局事务。代码 docstring明确 primitive installer 自身若部分变更后抛错，仍可能留下未知状态；因此 shared hub 需要 effect receipt/readback，而不能仅信 record。

#### 依赖分析与供应链风险

- `pyproject.toml` runtime dependencies：`typer>=0.24.0`、`click>=8.2.1`、`rich`、`platformdirs`、`readchar`、`pyyaml>=6.0`、`packaging>=23.0`、`pathspec>=0.12.0`、`json5>=0.13.0`。多数只有下界或无版本 pin；可复现安装需要 lock/immutable source ref。
- wheel 强制打包 core templates、bash/PowerShell/Python scripts、extensions、workflows、presets 和 community catalog snapshot；“Python 包”实际携带可被 Agent/CLI执行的脚本与 instruction，审计面大于 import graph。
- 本次隔离 venv 解析 20 packages；231 个定向 Hermes/download-security tests 通过。没有跑完整 161-test-file suite，也没有运行真实 shell workflow、catalog network、bundle install 或 self-upgrade。
- release v0.16.4 与本次源码 main `0.16.5.dev0` 不同；本机测试结论只绑定 `bf88c9f...`，不能外推到 v0.16.4 wheel 或未来 main。
- 下载安全代码覆盖大小、格式、路径与 archive member，但 remote catalog/extension/bundle 的内容语义、作者身份和其中 shell/instruction effect仍需独立审核。

#### README / docs / release / issues / source 交叉核验

- README 的 SDD 阶段、extension/preset overlay、bundle 和 30+ integration 与 tree/source 对应；Hermes 是真实 integration class，不是 README-only 列表。
- `workflows/ARCHITECTURE.md` 的 sequential dispatch、11 step registry、state-after-each-step 和 resume 路径与 `engine.py` 一致；文档明确 nested pause resume 只到 top-level index，这是已知局限。
- v0.16.4 release body列出 `RunState` TOCTOU、workflow type validation、archive manifest、auth host pattern 等安全/正确性修复；本次 main source确有 run_id-before-path、atomic write 和 bounded archive primitives，但 release artifact未单独安装验证。
- Open issue #4128 指出 `.specify/feature.json` 在并发 Agent 下发生 singleton overwrite；这是 2026-08-15 仍 open 的设计 gap，shared hub 若并行执行不能复用该 singleton 作为 scope truth。
- Closed issue #4067 展示 dotted/hyphenated command 在 Junie 中行为不同；`agents.py` 当前按 integration output layout计算 filename/invoke separator，说明 cross-Agent adapter必须用真实 harness fixture，而非静态字符串映射。

#### 可复用经验

- 当一个模板要安装到多个 Agent 时，应优先维护 agent-neutral artifact、逐 Agent renderer 和真实 loader/filename/invocation fixture，因为文件生成成功不等于目标 Agent能发现；边界是 fixture仍需在真实版本上复跑。
- 当 Agent workflow 可 pause/resume/fan-out 时，应优先持久化 typed run state、immutable workflow copy、step receipt 与 atomic single-file snapshot；边界是跨文件、跨进程与 nested resume 仍需额外事务/identity设计。
- 当组件安装会写全局目录时，应优先建立 ownership manifest、pre-existing inventory、content hash、dry-run diff、backup 与 scoped uninstall，而不是按名称前缀批量删除；边界是 manifest也必须防漂移与替换竞态。
- 当 workflow 提供 shell step 或 remote extension 时，应优先把 instruction validation、OS sandbox、effect authorization 与下载安全分开，因为 HTTPS/安全解压不等于脚本获准执行；边界是 human gate不替代最小权限。
- 当多个 Agent 并行共享同一 checkout 时，应优先给每个 run 注入 immutable feature/worktree/scope identity并避免 singleton pointer写入，因为 last-writer state会静默串线；边界是环境变量隔离也不能解决同一输出文件的并发写。

#### 可尝试实验（30 分钟最小 demo）

在 `runtime/hermes/github-learning-poc/scoped-skill-install-plan/` 做不写真实 home 的 fixture：

1. 构造临时 `fake_home/.hermes/skills`，预置一个用户修改的 `speckit-plan` 与一个 foreign skill。
2. 生成 candidate install plan：`target/owner/source_ref/before_hash/after_hash/action`，默认 dry-run。
3. 验证 pre-existing modified skill 必须 `conflict/needs_user`，不能覆盖或在 uninstall 时按前缀删除。
4. 用 temp+replace 写单个 skill，再做 readback hash；模拟第二进程 revision change，要求 stale plan blocked。
5. 产出 rollback manifest 和 terminal receipt；不运行上游 `specify init`，不写当前 `~/.hermes`。

#### 风险边界

- **License**：GitHub API 与根 LICENSE 为 MIT；community extension/preset/bundle及其依赖各自许可不自动随 core MIT覆盖。
- **维护活跃度**：pushed 为 2026-08-14T16:44:52Z，v0.16.4 同日发布，main 已进入 0.16.5.dev0；高频发布要求 source/tag/wheel 分别 pin。
- **安全风险**：Hermes adapter写全局 skills；teardown按 `speckit-*` 前缀删除。workflow shell step以用户权限运行，`requires`不是 capability gate。remote content 即使安全下载也可能包含危险 instructions/scripts。
- **并发风险**：issue #4128 的 `.specify/feature.json` singleton race仍 open；RunState lock主要是进程内，跨进程同 run_id/同 artifact 仍需外部协调。
- **恢复边界**：single JSON atomic replace不是跨 `state.json + inputs.json + effect` 事务；nested pause会重跑 parent body，副作用步骤必须幂等或有 operation id/readback。
- **供应链风险**：依赖多为下界；wheel携带 scripts/templates/catalog snapshot；self-upgrade、catalog、bundle与integration写入是多个 mutation surfaces。
- **不适用场景**：当前默认 Hermes profile、共享 skill目录、含用户自定义 `speckit-*` 的 home、高权 shell workflow、多 Agent同 checkout并行写同 feature/artifact。
- **不能自动执行**：不在当前机器运行 `specify init --integration hermes`；不写/删 `~/.hermes/skills`；不运行 remote workflow shell或自升级；不修改 shared manifest。

#### ⭐ Skill 升格判断

**需二次验证**；部分机制可直接抽象，产品/模板不可直接迁移。

- **可直接抽象的窄机制**：atomic run snapshot、source copy、typed terminal、bounded archive extraction、bundle ownership/refcount，这些是 agent-neutral pattern。
- **需二次验证**：`scoped-skill-install-plan` fixture必须覆盖 pre-existing modified files、cross-process revision、dry-run/readback/rollback、symlink target与profile scope。
- **暂不沉淀**：不复制 Spec Kit core skills/templates/bundles，不安装 Hermes integration，不引入第二套 shared skill真相源。
- **升格结论**：优先更新现有 path-portability/shared-skill-governance/verification/GitHub-learning契约，而不是新增“spec-kit”shared skill；当前不写 curated active fact。

#### Hermes / shared hub 落地路径

1. **runtime POC**：`runtime/hermes/github-learning-poc/scoped-skill-install-plan/{inventory.py,plan.py,apply.py,fixtures/,tests/,README.md}`，根目录由 resolver提供，home用临时路径。
2. **shared skill governance**：未来所有第三方 skill引入先输出 `source_ref/license/owner/target/before_hash/action/conflict/rollback`；只有人工批准且验证通过才更新 `capabilities/skills/` 和 manifest。
3. **workflow state**：可把 `workflow.yml + inputs + state + log` 的分层模式用于 Hermes自主学习 POC，但 terminal必须再绑定 expected artifact/hash/audit score；不能仅复制 `completed`。
4. **并发 scope**：parallel Agent/run 使用 immutable `run_id + project/feature/worktree identity`，禁止共享 singleton current-feature pointer；shared写入仍经 lane/claim/lock治理。
5. **OpenClaw 边界**：当前不存在且禁止调用；未来若适配，只复用 schema/fixtures，各自在真实 workspace验证 filename、loader、ownership与effect，不共享本机 global skill状态。

## 经验沉淀

1. 当小模型或 Agent只负责选择工具时，应优先把输出当 proposal，并在宿主最终 chokepoint重验 schema、业务 invariant、effect、scope、authorization 与 policy revision，因为 grammar-valid/confidence高都不等于获准执行；边界是 validator本身也要有 adversarial fixtures。
2. 当第三方项目自动下载 native library、checkpoint、plugin、skill 或脚本时，应优先固定 immutable source/hash、限制大小/成员、记录 platform/version 并做 readback receipt，因为“官方 repo + HTTPS”不能证明运行字节和权限安全；边界是 hash不证明无漏洞。
3. 当跨 Agent模板需要写全局或共享目录时，应优先 dry-run inventory、ownership manifest、pre-existing conflict、content hash、backup与 scoped uninstall，因为名称前缀删除会误伤用户修改或另一控制面；边界是 manifest也需 revision/identity校验。
4. 当 workflow支持 pause/resume/fan-out时，应优先把 run identity、step status、artifact hash、operation id与 terminal receipt持久化，并明确 nested replay语义，因为 atomic state file不等于 effect事务；边界是副作用仍需幂等/readback。
5. 当多个 Agent在同一 checkout并行工作时，应优先使用 immutable feature/worktree/run scope并禁止 singleton context pointer写入，因为 last-writer-wins会静默跨任务污染；边界是 scope隔离仍不能替代共享文件锁/claim。
6. 当仓库 license字段互相冲突时，应优先标记“待核验”并停止源码/制品迁移，只允许抽象不受版权表达保护的工程机制；边界是 GitHub API license不是依赖、模型或发布物的完整许可审查。

### 后续实验汇总

- `runtime/hermes/github-learning-poc/proposal-effect-gate/`：synthetic tool proposal → host validation/authorization → mock effect receipt。
- `runtime/hermes/github-learning-poc/scoped-skill-install-plan/`：fake home 下 inventory/dry-run/conflict/hash/readback/rollback，不触碰当前 profile。
- 两个实验都不连接 provider、不加载 native engine、不执行真实高权工具、不改 config/provider/auth/env/cron、skills 或 curated。

## 风险边界（跨项目）

1. **来源边界**：Stars/forks/license/updated/pushed来自 GitHub Repository API；commit/release/issues来自相应 API；README模型指标与 issue复现均明确标注上游声明。
2. **执行边界**：Needle只运行 deterministic schema tests；Spec Kit只运行临时 home的 Hermes/download-security tests。没有运行模型 inference、真实 workflow shell、bundle install、global skill install。
3. **权限边界**：不自动改 Hermes配置、provider/model/auth/env/cron/secret/skills；不把模型 proposal、remote workflow或第三方 skill当授权。
4. **供应链边界**：不下载 Needle native engine，不加载 pickle，不运行 Spec Kit self-upgrade/catalog install；隔离 venv只用于定向测试。
5. **许可边界**：Needle 的 MIT/API/LICENSE 与 Apache package metadata冲突待核验；Spec Kit community组件需逐项审查，不能继承 core MIT结论。
6. **长期记忆边界**：本日报是 Hermes inbox raw research；候选 facts/skills只供审计，未自动写 `curated/memory/`。
7. **OpenClaw边界**：运行时不存在；本次没有调用、启动、写入或依赖 OpenClaw。

## 明日继续

**最小动作**：先实现两个纯 fixture POC，各跑一组失败注入测试；只有它们真实输出 blocked/conflict/readback receipt 后，才评估是否更新现有 shared verification/research契约。

1. `proposal-effect-gate`：验证 low-confidence、unknown tool、schema-valid但业务非法、write无批准、scope越界、mock success六类 case；输出 policy revision与receipt hash。
2. `scoped-skill-install-plan`：验证 modified pre-existing skill不覆盖不删除、symlink escape拒绝、stale revision拒绝、单文件atomic apply/readback、rollback inventory。
3. Needle后续：若要核验模型，只在隔离 profile固定 engine artifact hash，先跑 public low-risk toy tool；不接真实 Hermes tools。
4. Spec Kit后续：追踪 issue #4128 的并发 scope方案，并把 main、v0.16.4 tag/wheel、Hermes CLI版本分开做 conformance。
5. 候选项目：`infiniflow/ragflow` 的 context/provenance或 `cactus-compute/needle` 的 tool retrieval index可继续，但先检查 ACL、cache identity、license与真实 tests。

## 候选反哺

### Candidate Facts

- [ ] topic: grammar/schema constrained tool output仍需 host effect/scope/authorization gate | evidence: `cactus-compute/needle@4439dd0 needle/__init__.py:119-139` 与 issue #67 | 建议: update candidate only | 安全级别: high
- [ ] topic: third-party Hermes integration的global skill ownership必须显式建模 | evidence: `github/spec-kit@bf88c9f src/specify_cli/integrations/hermes/__init__.py:76-265` 与本机 231定向tests | 建议: create/update candidate only | 安全级别: high
- [ ] topic: Needle source/package license metadata冲突 | evidence: GitHub API/root LICENSE=MIT；`pyproject.toml:7=Apache-2.0` | 建议: dispute/pending verification，不晋升为稳定许可事实 | 安全级别: medium
- [ ] topic: Spec Kit同 checkout多 Agent singleton feature pointer存在open race报告 | evidence: GitHub issue #4128（2026-08-15仍open） | 建议: project risk candidate，不泛化为所有版本永久事实 | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: `proposal-effect-gate` | 可复用场景: 本地小模型/LLM/Agent proposal进入Hermes/shared工具前 | 是否建议 shared: yes, after fixture and dedupe | 原因: agent-neutral且与effect-scope/verification契约重合，优先更新既有能力
- [ ] 名称: `scoped-skill-install-plan` | 可复用场景: 第三方skill/plugin写本地profile或shared capabilities前 | 是否建议 shared: yes, after fixture | 原因: Hermes/future agent都需要ownership/diff/rollback；不能直接采用Spec Kit全局删除语义
- [ ] 名称: `durable-workflow-receipt` | 可复用场景: 自主学习cron的pause/resume/fan-out与artifact审计 | 是否建议 shared: maybe/update existing | 原因: 应与self-reflection、completion/receipt、verification-first去重，而非新增重叠skill

### Candidate Open Questions

- [ ] 问题: Needle当前 engine 2.0.2/main commit是否真正修复issue #67的malformed envelope，且confidence如何校准？ | reason: gap | priority: high
- [ ] 问题: Needle仓库/包/weights/native engine的实际许可分别是什么，MIT与Apache metadata冲突如何解释？ | reason: conflict | priority: high
- [ ] 问题: Spec Kit Hermes integration能否支持profile-scoped、manifest-owned、modified-file-preserving安装/卸载？ | reason: adaptation | priority: high
- [ ] 问题: issue #4128的feature scope race在后续release如何修复，是否同时覆盖shell/Python/PowerShell路径？ | reason: stale/adaptation | priority: medium
- [ ] 问题: shared hub的学习orchestrator能否从真实sidecar receipt审计source/test/effect，而非报告关键词？ | reason: adaptation | priority: medium

### 不应自动落地

- 不安装 Needle、不下载/加载其 native engine、weights、pickle checkpoint，不把真实 Hermes tools交给 `Needle.run()`。
- 不运行 `specify init --integration hermes`，不写或删除当前 `~/.hermes/skills`，不运行remote bundle/workflow/self-upgrade。
- 不复制两个项目的源码、模板、模型或skills进入 `capabilities/skills/`；只提出机制候选。
- 不因 MIT字段就忽略 Needle license冲突或第三方community组件许可。
- 不修改 provider/model/auth/env/cron/secret，不从 assistant-authored prose生成用户事实。
- 不把 candidate facts/skills自动写入 `curated/memory/`。

## 报告与证据路径

- **Hermes inbox报告**：`inbox/hermes/daily/2026-08-15-github-learning.md`
- **运行证据**：`runtime/hermes/github-hot-project-learning/evidence/2026-08-15/`
- **项目卡片**：`runtime/hermes/github-learning/projects/cactus-compute-needle.md`、`runtime/hermes/github-learning/projects/github-spec-kit.md`
- **经验追加**：`runtime/hermes/github-learning/lessons.md`
- **知识库 projection（audit通过后由orchestrator复制）**：`/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案/每日学习/2026-08-15-GitHub热门项目学习日报.md`
- **审计状态**：`runtime/hermes/github-hot-project-learning/status.json`
