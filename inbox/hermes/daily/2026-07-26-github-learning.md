# 2026-07-26 GitHub 热门项目学习日报

> 执行者：Hermes（未调用 OpenClaw）  
> 查询时间：2026-07-26T07:36:36+08:00  
> 趋势入口：<https://github.com/trending?since=daily>；元数据入口：`gh api repos/{owner}/{repo}`  
> 深读快照：`citrolabs/ego-lite@02ee972edf0685371c826c90421511f8a2940cd5`、`RyanCodrai/turbovec@d3aeaf831dbd47025be438ed8105a1b600d26805`、`andrewyng/aisuite@cb29165b00f719cceae6a82ed4621cbcb79aaaf7`。Stars 是查询时快照，会继续变化。

## 今日结论

今天的共同主线是：**Agent 系统要把高风险边界做成可执行的结构**——浏览器自动化用 task-space ownership、短期 ref 和副作用后验证；向量检索用稳定外部 ID、kernel 内 allowlist 与版本化文件校验；Agent runner 用逐工具 policy、乐观并发 state revision 和 trace event。三者都说明“功能可用”不等于“边界可信”。

## 研究方法与可验证证据

1. 真实抓取 GitHub Trending daily，并用 GitHub REST API 查询全部速览项目的 Stars、Forks、Language、License、`updated_at`、`pushed_at`。
2. 三个深读仓库均 shallow clone，固定到上方 commit；逐文件读取 README、docs、issues、关键源码与依赖清单。
3. 动态验证：
   - `ego-lite/package/ego-browser`：`npm ci && npm test`，真实结果 **299 passed / 0 failed**；npm audit 输出 **0 vulnerabilities**。构建同时报告 `state.ts -> browser-runtime.ts -> state.ts` circular dependency warning。
   - `aisuite`：用隔离 uv 环境运行 `tests/agents/test_state_store.py tests/agents/test_tool_policy.py tests/agents/test_runner.py`，真实结果 **16 passed in 0.50s**。
   - `turbovec`：尝试 `cargo test --workspace`，本机返回 `cargo: command not found`；所以 Rust 动态行为均为**源码/fixture 核验，运行待核验**，绝不写成测试通过。
4. Release / issue 交叉来源：ego-lite 最新 release `v1.2.5`（2026-07-17），近期 issues #143/#144/#88；aisuite 最新 release `v0.1.3`（2026-07-20），issues #369/#342；turbovec GitHub Releases API 返回 0 条，但 tags 存在 `v0.9.0` 至 `v0.2.0`，近期 issues #202/#206/#207/#200。

## 项目速览

> 下表全部 Stars / License 来自 2026-07-26T07:36:36+08:00 前后的 GitHub API 实际响应；`API updated_at` 是仓库元数据更新时间，不等于提交时间。

| 项目 | Stars | Forks | Language | License（API） | API updated_at | API pushed_at | 今日判断 |
|---|---:|---:|---|---|---|---|---|
| [block/buzz](https://github.com/block/buzz) | 11,863 | 942 | Rust | Apache-2.0 | 2026-07-25T23:34:07Z | 2026-07-25T23:14:37Z | 连续两日已深读，今天只观察高活跃租户/审计协作底座 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 12,933 | 885 | Go | Apache-2.0 | 2026-07-25T23:35:05Z | 2026-07-25T01:34:58Z | 前日已深读；`v1.7.16` 显示仍高频发布 |
| [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | 3,549 | 174 | JavaScript | MIT | 2026-07-25T23:35:58Z | 2026-07-25T15:39:13Z | **深读**：task space、CDP session、稳定 locator、site learning contract |
| [Automattic/harper](https://github.com/Automattic/harper) | 13,404 | 508 | Rust | Apache-2.0 | 2026-07-25T23:35:25Z | 2026-07-24T04:09:59Z | 昨日已深读；继续观察本地确定性质量门 |
| [Pumpkin-MC/Pumpkin](https://github.com/Pumpkin-MC/Pumpkin) | 9,699 | 655 | Rust | GPL-3.0 | 2026-07-25T23:35:56Z | 2026-07-25T17:57:45Z | GPL 边界明确，不向 shared 复制代码 |
| [permissionlesstech/bitchat](https://github.com/permissionlesstech/bitchat) | 28,679 | 4,277 | Swift | Unlicense | 2026-07-25T23:31:20Z | 2026-07-25T22:16:55Z | 高热度 P2P 通讯；安全与协议面大，本轮不仓促迁移 |
| [RyanCodrai/turbovec](https://github.com/RyanCodrai/turbovec) | 14,274 | 1,268 | Python | MIT | 2026-07-25T23:34:23Z | 2026-07-25T23:29:49Z | **深读**：在线量化、检索内过滤、稳定 ID、文件不变量 |
| [OtterMind/Chat2DB](https://github.com/OtterMind/Chat2DB) | 26,652 | 2,905 | Java | NOASSERTION | 2026-07-25T23:34:43Z | 2026-07-25T16:45:19Z | API 无可判定许可证；只观察，不复制源码 |
| [andrewyng/aisuite](https://github.com/andrewyng/aisuite) | 15,213 | 1,614 | Python | MIT | 2026-07-25T23:23:13Z | 2026-07-25T19:14:07Z | **深读**：runner/policy/state/trace 的生产外壳 |

---

## 深读项目

### 项目 1. citrolabs/ego-lite

- **仓库**：<https://github.com/citrolabs/ego-lite>
- **API 基本信息**：Stars: **3,549**；Forks: **174**；License: **MIT**；Language: JavaScript；`updated_at`: 2026-07-25T23:35:58Z；`pushed_at`: 2026-07-25T15:39:13Z。
- **固定快照**：[`02ee972`](https://github.com/citrolabs/ego-lite/commit/02ee972edf0685371c826c90421511f8a2940cd5)，commit time 2026-07-25T15:39:12Z。
- **Release / Issues**：[`v1.2.5`](https://github.com/citrolabs/ego-lite/releases/tag/v1.2.5) 发布于 2026-07-17；[#143](https://github.com/citrolabs/ego-lite/issues/143) 是 app-mode fullscreen 黑边，[#144](https://github.com/citrolabs/ego-lite/issues/144) 是导入中断留下 stale stage 文件，[#88](https://github.com/citrolabs/ego-lite/issues/88) 指出 task-space renderer cleanup 不完整。
- **一句话判断**：值得学的不是封闭浏览器本体，而是开源 harness 如何把 Agent 浏览器控制约束为 **owned task space → CDP session → semantic locator/ref → act → observe/verify → cleanup/handoff**。
- **解决的问题**：替代“Agent 与用户争抢同一浏览器 tabs、每步 CLI 往返、把临时 DOM ref 当稳定 selector、用户接管后仍盲重试”的旧做法。

#### 架构/实现与数据流

仓库明确说明：开源部分是 Node.js CDP harness 与 skill，ego lite 浏览器本体是独立下载、不是本仓库源码。CLI 从 stdin 接收 JS，`runMain()` 把 `helperContext()` 的 facades 注入执行作用域；facades 再进入 `browser-runtime.ts`、drivers 与 `element-resolver.ts`；snapshot 创建短期 backend-node refs；site learning 从 manifest 匹配 domain，加载 notes/tools/browser-tools。

```text
citrolabs/ego-lite/
├── package/ego-browser/
│   ├── src/index.ts                 # CLI / embedded SDK 双入口
│   ├── src/run.ts                   # stdin JS 执行与输出收口
│   ├── src/helpers.ts               # page/browser/taskSpaces/site/fetch 单一 helper surface
│   ├── src/browser-runtime.ts       # CDP transport、session TTL/retry、event/dialog buffer
│   ├── src/element-resolver.ts      # ref / role / text / CSS / XPath 解析与错误分类
│   ├── src/driver/                  # nav、pointer、keyboard、observe、waits、files
│   └── src/learning/                # manifest discovery、validation、site-tool execution
├── skills/ego-browser/
│   ├── SKILL.md                     # Agent 使用契约与 ownership/handoff 规则
│   └── learnings/{google,x-com}/    # manifest + notes + tools + browser-tools 示例
├── docs/                            # 用户文档资产
└── AGENTS.md                        # 维护者架构与测试约束
```

数据流：`stdin JS -> runMain -> helperContext facades -> task-space/tab selection -> CDP attach -> locator/ref resolution -> driver action -> snapshot/pageInfo/screenshot verification -> complete/handoff`。site learning 旁路为 `URL -> matching manifest -> validated relative file -> Node/browser tool`。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `package/ego-browser/src/browser-runtime.ts` | CDP transport/session | 15s request timeout、2s session cache、concurrent attach 去重、session lost 自动重附着、10k event cap |
| `package/ego-browser/src/element-resolver.ts` | 元素身份与错误语义 | 优先 backendNodeId；stale 时才 role/name fallback；0 match 是 transient，多 match/坏 selector 是 permanent |
| `package/ego-browser/src/helpers.ts` | API 单一真相面 | 构造 page/browser/taskSpaces/site facades；task-space name/id 与 ownership 规则；site tools 注入同一 helper context |
| `package/ego-browser/src/learning/index.ts` | 站点经验执行 | manifest 声明后动态 import；路径必须留在 site skill 目录；browser tool 包装后页面执行 |
| `package/ego-browser/src/learning/validate-learning-format.ts` | 学习包质量门 | 校验 domain、schema、相对路径、文件存在、callable；拒绝 `@N/ref=N` 临时 refs |
| `skills/ego-browser/SKILL.md` | 人机控制契约 | 用户控制是 hard stop；handoff 后只在明确确认时 takeover；完成时必须显式 keep/close |

#### 源码精读 1：session 是短租约，不是永恒句柄

固定源码：[`browser-runtime.ts#L79-L143`](https://github.com/citrolabs/ego-lite/blob/02ee972edf0685371c826c90421511f8a2940cd5/package/ego-browser/src/browser-runtime.ts#L79-L143)

```ts
export async function browserCdp(method, params = {}, sessionId = undefined,
                                 timeoutMs = RESPONSE_TIMEOUT_MS) {
  const explicit = sessionId !== undefined;
  let effective = sessionId;
  if (!explicit && !BROWSER_LEVEL(method)) effective = await ensureSession();
  try {
    return await rawCdp(method, params, effective, timeoutMs);
  } catch (error) {
    if (SESSION_LOST.test(error?.message || "") && !explicit && !BROWSER_LEVEL(method)) {
      invalidateSession();
      const fresh = await ensureSession();
      return rawCdp(method, params, fresh, timeoutMs);
    }
    throw error;
  }
}
```

逻辑摘要：自动注入的 page-level session 丢失时只 retry 一次；显式 session 与 browser-level method 不重试，避免把调用方指定语义悄悄改掉。`ensureSession()` 用 2s TTL 与 `sessionInflight` 去重并发 attach，按 preferred → active → last tab 选 target。**迁移点**是“缓存句柄 + 失效重建 + 并发去重 + 显式句柄不擅自替换”。

#### 源码精读 2：ref 解析保留身份，不静默点错同名元素

固定源码：[`element-resolver.ts#L63-L146`](https://github.com/citrolabs/ego-lite/blob/02ee972edf0685371c826c90421511f8a2940cd5/package/ego-browser/src/element-resolver.ts#L63-L146)

```ts
export async function resolveElementCenter(cdp, sessionId, refMap, selectorOrRef,
                                           iframeSessions = new Map()) {
  const refId = parseRef(selectorOrRef);
  if (refId) {
    const entry = refMap.get(refId);
    if (!entry) throw new ElementResolutionError(`Unknown ref: ${refId}`, "transient");
    try {
      const result = await send(cdp, "DOM.getBoxModel",
                                { backendNodeId: entry.backendNodeId }, effectiveSessionId);
      return { ...boxModelCenter(result.model), sessionId: effectiveSessionId };
    } catch (error) {
      if (error instanceof ElementResolutionError) throw error;
      // stale backend node 才 fallback 到 role/name
    }
  }
  // locator / raw selector paths ...
}
```

逻辑摘要：已解析但暂时没有可用 box 的节点保持 retryable，不为了“成功”而退化到同名节点；真正 stale 才 fallback。`matchCountKind()` 把多个匹配判成 permanent，阻止自动等待无限重试歧义 selector。这比“遇错就重试/点第一个”更适合副作用操作。

#### 源码精读 3：经验包必须声明、验证且禁用临时 ref

固定源码：[`learning/index.ts#L145-L176`](https://github.com/citrolabs/ego-lite/blob/02ee972edf0685371c826c90421511f8a2940cd5/package/ego-browser/src/learning/index.ts#L145-L176) 与 [`validate-learning-format.ts#L227-L236`](https://github.com/citrolabs/ego-lite/blob/02ee972edf0685371c826c90421511f8a2940cd5/package/ego-browser/src/learning/validate-learning-format.ts#L227-L236)

```ts
export async function runNodeSiteTool(siteId, toolName, args = {}, ctx, options = {}) {
  const { siteDir, manifest } = await findSiteSkill(siteId, options);
  const schema = toolSchemas(manifest, "nodeTools")[toolName];
  if (!schema) throw new Error(`Node tool ${toolName} is not declared`);
  const toolPath = relativeSitePath(siteDir, schema.path, "Node tool");
  const module = await import(`${pathToFileURL(toolPath).href}?t=${Date.now()}`);
  const tool = module[schema.callable];
  if (typeof tool !== "function") throw new Error(`missing Node callable`);
  return tool(ctx, args || {});
}
```

```ts
async function rejectTemporaryRefs(siteDir, relativePath, prefix, errors) {
  const text = await readFile(join(siteDir, relativePath), "utf8");
  if (/(?:@\d+\b|\bref=\d+\b)/.test(text)) {
    errors.push(`${prefix}: contains temporary snapshot ref; use stable locators instead`);
  }
}
```

逻辑摘要：只有 manifest 声明的工具可运行；路径拒绝 absolute、backslash 与 `..`，并再次验证 resolved path 未逃逸；validator 还拒绝把本次 snapshot 的 `@N` 写进长期经验。注意：Node site tool 仍是动态 import 的可信代码，因此 schema/path validation **不是 sandbox**。

#### 依赖分析与供应链风险

`package/ego-browser/package.json` 运行时直接依赖仅 `acorn ^8.16.0`；dev/build 依赖 Rollup、esbuild、TypeScript、Prettier、lefthook。lock 实际解析为 acorn 8.17.0、esbuild 0.28.1、rollup 4.62.0、typescript 5.9.3。`npm ci` 审计显示 0 vulnerabilities，但这只是当前 npm 数据库结果，不能证明无供应链风险。

风险：动态 import 的 site Node tool 拥有 helper context 与 Node 权限；browser tool 在页面 context 执行；`prepare` 会运行 lefthook install；真正浏览器是 closed-source separate download。依赖少降低面，但不能替代签名发布、安装脚本审查和 tool effect policy。

#### 可复用经验、实验与落地路径

- **当** Agent 与用户共享可变 GUI 资源、控制权可随时转移**时，应优先**把 ownership/handoff/takeover/cleanup 写成可观测状态机，而不是靠 prompt 礼貌约定；因为用户接管必须成为 hard stop，边界是宿主仍需可靠暴露状态。
- **可尝试实验（30 分钟）**：在 `runtime/hermes/github-learning-poc/browser-action-contract/` 写纯 fixture checker：输入 `{space_owner, selector_kind, effect, pre_observation, post_observation}`，输出 `allowed|blocked|needs_confirmation|failed`；不启动浏览器、不改配置。
- **Skill 升格判断：需二次验证。** “临时 ref 禁止持久化 + ownership hard stop + observe-act-verify”值得进入现有 browser/web workflow，但当前不能直接安装 ego skill：closed-source runtime、仅 macOS、并且上游 skill 触发描述要求覆盖其他浏览工具，可能与 Hermes 现有 tool routing 冲突。
- **Hermes/shared hub 落地路径**：
  1. runtime POC 放 `runtime/hermes/github-learning-poc/browser-action-contract/`；
  2. 将验证器接口定义为 `validate_action(action, observed_state) -> {status, reasons}`；
  3. 若 fixture 通过，再更新现有共享 browser/research skill（先查重 `capabilities/manifests/shared-skills.yaml`），不新建宽泛重复 skill；
  4. 长期经验候选仅写入日报 `Candidate Facts`，经治理评分后才进入 `curated/memory/facts/`；
  5. 不自动接入 OpenClaw、不安装应用、不改 Hermes tools/config。

#### 风险边界

- **License**：API 与根 LICENSE 均为 MIT；但浏览器应用是 separate closed-source download，不能把 repo license 外推到应用实现。
- **维护活跃度**：固定 commit 在 2026-07-25；release v1.2.5 距查询 9 天，活跃。
- **安全风险**：继承真实 login state、Node tool 动态 import、browser-side JS 执行都扩大权限面；用户接管检查只能减少误操作，不是恶意 skill sandbox。
- **局限/不适用**：README 明确当前只支持 macOS；本任务 WSL 无真实 ego runtime，299 tests 只验证开源 harness，不验证浏览器本体、真实网站兼容性或 README benchmark。

---

### 项目 2. RyanCodrai/turbovec

- **仓库**：<https://github.com/RyanCodrai/turbovec>
- **API 基本信息**：Stars: **14,274**；Forks: **1,268**；License: **MIT**；Language: Python（仓库含 Rust core/Python binding）；`updated_at`: 2026-07-25T23:34:23Z；`pushed_at`: 2026-07-25T23:29:49Z。
- **固定快照**：[`d3aeaf8`](https://github.com/RyanCodrai/turbovec/commit/d3aeaf831dbd47025be438ed8105a1b600d26805)，commit time 2026-07-25T23:21:44Z。
- **Release / Issues**：GitHub Releases API 返回 **0**；真实 tags 包括 `v0.9.0`、`v0.8.1` 等。[#202](https://github.com/RyanCodrai/turbovec/issues/202) 要求暴露可复现实验 calibration，[#206](https://github.com/RyanCodrai/turbovec/issues/206) 指出 rotation 跨线程/BLAS 不确定，[#207](https://github.com/RyanCodrai/turbovec/issues/207) 指出 pooled test 掩盖 per-coordinate 分布偏差，[#200](https://github.com/RyanCodrai/turbovec/issues/200) 指出 dotted namespace 持久化碰撞。
- **一句话判断**：它值得学的不只是 2–4 bit quantization，而是把**访问控制过滤推进 search kernel、把稳定外部 ID 与内部 slot 分离、把持久化格式不变量在分配前验证**。
- **解决的问题**：替代 float32 全量常驻、索引训练/重建、ANN 后置过滤导致结果不足、删除后 positional ID 漂移，以及未版本化二进制索引静默错读。

#### 架构/实现与数据流

```text
RyanCodrai/turbovec/
├── turbovec/src/
│   ├── lib.rs                  # TurboQuantIndex 生命周期、validation、cache、search API
│   ├── encode.rs               # normalize → rotate → TQ+ → quantize → pack → scale
│   ├── search.rs               # query rotation、LUT、SIMD/scalar dispatch、masked top-k
│   ├── id_map.rs               # stable u64 id ↔ internal slot
│   ├── io.rs                   # .tv/.tvim versioning、limits、fingerprint、load/write
│   ├── rotation.rs/codebook.rs # 随机正交旋转与 Lloyd-Max codebook
│   └── pack.rs                 # SIMD block layout
├── turbovec-python/
│   ├── src/lib.rs              # PyO3/Numpy binding
│   ├── python/turbovec/        # LangChain/LlamaIndex/Haystack/Agno adapters
│   └── tests/fixtures/         # legacy side-car compatibility fixtures
├── benchmarks/{suite,results}/ # 可重复脚本与 JSON 结果
└── docs/api.md                 # API、filter、file-format invariants
```

写入数据流：`vectors -> input validation -> L2 normalize -> random rotation -> first-batch TQ+ calibration/frozen reuse -> Lloyd-Max bucket -> bit planes -> per-vector renormalization scale -> append -> invalidate blocked cache`。查询数据流：`query -> validate -> rotate -> inverse calibration -> LUT -> runtime CPU dispatch -> block-level mask skip + lane-level allow -> top-k -> slot/external ID`。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `turbovec/src/lib.rs` | public index contract | dim/bit_width/value validation，OnceLock cache，first-add calibration，masked search |
| `turbovec/src/encode.rs` | quantization pipeline | Rayon normalize，matrix rotate，per-coordinate quantile calibration，fused quantize/scale/pack |
| `turbovec/src/search.rs` | scoring kernels | inverse TQ+，query LUT，AVX-512/AVX2/NEON/scalar runtime dispatch，masked top-k |
| `turbovec/src/id_map.rs` | stable identity | external `u64` ID 与 swap-remove slot 解耦 |
| `turbovec/src/io.rs` | untrusted file boundary | magic/version/size checked arithmetic、rotation fingerprint、legacy version handling |
| `docs/api.md` | file/API truth | v4 layout、effective_k、MAX_DIM、load-before-allocation checks |

#### 源码精读 1：first add 决定 calibration，空写不能污染状态

固定源码：[`lib.rs#L288-L368`](https://github.com/RyanCodrai/turbovec/blob/d3aeaf831dbd47025be438ed8105a1b600d26805/turbovec/src/lib.rs#L288-L368)

```rust
pub fn add(&mut self, vectors: &[f32]) {
    let dim = self.dim.expect("dim is not set");
    let n = vectors.len() / dim;
    assert_eq!(vectors.len(), n * dim);
    if n == 0 { return; } // 不让 empty first add 锁死 identity calibration

    let existing = if self.tqplus_shift.is_empty() {
        None
    } else {
        Some((self.tqplus_shift.as_slice(), self.tqplus_scale.as_slice()))
    };
    let (packed, scales, shift, scale_tq) = encode::encode(/* ... */, existing);
    // 首批保存 calibration；后续批次复用同一坐标系
    self.blocked = OnceLock::new();
}
```

逻辑摘要：empty first add 过去会把 identity calibration 锁死，后续再多样本也不拟合；现在真正 no-op。后续增量写复用首批 calibration，避免不同批次落在不同量化坐标系；写后仅 invalidates derived blocked cache，rotation/codebook 保持。

#### 源码精读 2：编码把统计校准与热 kernel 解耦

固定源码：[`encode.rs#L69-L157`](https://github.com/RyanCodrai/turbovec/blob/d3aeaf831dbd47025be438ed8105a1b600d26805/turbovec/src/encode.rs#L69-L157)

```rust
pub(crate) fn encode(vectors: &[f32], n: usize, dim: usize,
                     rotation: &[f32], boundaries: &[f32], centroids: &[f32],
                     bit_width: usize,
                     existing_calibration: Option<(&[f32], &[f32])>)
  -> (Vec<u8>, Vec<f32>, Vec<f32>, Vec<f32>) {
    assert!(dim != 0 && dim % 8 == 0);
    // rows 并行 normalize，再矩阵 rotate
    let (shift, scale_tq) = match existing_calibration {
        Some((s, sc)) => (s.to_vec(), sc.to_vec()),
        None => compute_tqplus_calibration(rotated, n, dim),
    };
    // per-row fused_quantize_scale_pack
    (packed, scales, shift, scale_tq)
}
```

逻辑摘要：TQ+ 在首批按每个 coordinate 的 5/95% quantile 拟合 shift/scale；少于 1000 samples 回退 identity。查询侧做 inverse calibration，把偏置折进 LUT bias，因此 SIMD scoring kernel 无需知道 TQ+。这是“把可变策略折叠到稳定热路径输入”的模式，但 issue #202/#206/#207 说明 calibration reproducibility 与 per-coordinate 检验仍需继续验证。

#### 源码精读 3：allowlist 必须进入 scorer，而不是结果后过滤

固定源码：[`lib.rs#L478-L589`](https://github.com/RyanCodrai/turbovec/blob/d3aeaf831dbd47025be438ed8105a1b600d26805/turbovec/src/lib.rs#L478-L589) 与 [`search.rs#L1310-L1362`](https://github.com/RyanCodrai/turbovec/blob/d3aeaf831dbd47025be438ed8105a1b600d26805/turbovec/src/search.rs#L1310-L1362)

```rust
pub fn search_with_mask(&self, queries: &[f32], k: usize,
                        mask: Option<&[bool]>) -> SearchResults {
    let packed_mask = mask.map(|m| { /* bool slots -> u64 bitset */ });
    let n_allowed = packed_mask.as_ref().map_or(self.n_vectors, |p| {
        p.iter().map(|w| w.count_ones() as usize).sum::<usize>()
    });
    let effective_k = k.min(self.n_vectors).min(n_allowed);
    let (scores, indices) = search::search(/* ... */, k, packed_mask.as_deref());
    SearchResults { scores, indices, nq, k: effective_k }
}
```

```rust
pub(crate) fn search(/* validated buffers */, k: usize, mask: Option<&[u64]>)
  -> (Vec<f32>, Vec<i64>) {
    let k = k.min(mask.map(popcount).unwrap_or(n_vectors));
    if k == 0 { return (Vec::new(), Vec::new()); }
    // query GEMM rotate -> inverse calibration -> LUT -> CPU-specific scorer
    // scorer skips fully-disallowed blocks and never inserts disallowed lanes
}
```

逻辑摘要：结果宽度明确收缩为 `min(k,n_allowed)`，不以 `-1/NaN` 假填充；block 没有 allowed slot 就不做 LUT scoring，lane 不允许就不进 heap。安全上关键是 allowlist 必须来自权威 ACL/tenant 过滤；kernel 内执行不代表 allowlist 本身正确。

#### 依赖分析与供应链风险

Rust core 直接依赖 `ndarray 0.17`、`rayon 1.10`、`ordered-float 4`、`rand 0.8`、`rand_chacha 0.3`、`rand_distr 0.4`、`statrs 0.17`、`faer 0.20`；Cargo.lock 实际版本依次为 0.17.2、1.11.0、4.6.0、0.8.5、0.3.1、0.4.3、0.17.1、0.20.2。Python binding 用 PyO3 0.27 / numpy 0.27（lock: 0.27.2 / 0.27.1），Python project 还要求 `numpy>=1.20`。

风险：BLAS/CPU backend 可能影响 rotation reproducibility（issue #206）；unsafe SIMD 依赖公共入口完整验证 buffer/scalars；多语言发布要同时保证 crate、wheel、CPU baseline 与 file format。API License MIT 不能替代所有 transitive crates/wheels 的 license 与 advisory review。

#### 可复用经验、实验与落地路径

- **当**检索结果受 tenant、ACL 或时间窗限制**时，应优先**让权威 allowlist 进入 ANN scorer/kernel，而不是先全库 top-k 再丢弃；因为后过滤可能漏足 k 个结果并浪费计算，边界是 allowlist 构造仍需 fail-closed。
- **可尝试实验（30 分钟）**：在 `runtime/hermes/github-learning-poc/retrieval-filter-contract/` 做纯 Python exact-search fixture，对比 pre-filter 与 post-filter 在高选择性 ACL 下的结果完整性，并验证 unknown tenant 返回 `blocked` 而不是 empty-as-clean；不安装 turbovec。
- **Skill 升格判断：需二次验证。** kernel 实现本身不应成为 skill；可沉淀的是“stable external id + authoritative prefilter + explicit effective_k + index schema/version/fingerprint”检索契约。先与 shared-memory index/runtime 现有实现对比、跑数据集与跨架构 fixture。
- **Hermes/shared hub 落地路径**：
  1. runtime POC 路径 `runtime/hermes/github-learning-poc/retrieval-filter-contract/`；
  2. 为未来 shared memory index adapter 预留 `search(query, scope, allow_ids, k) -> {status,hits,effective_k,index_version}`；
  3. `scope` 缺失、ACL lookup 失败、index/schema mismatch 均输出 `blocked`，不能退化全库检索；
  4. 若 POC 与真实索引 benchmark 通过，再更新 memory/retrieval 相关 shared skill；不把二进制 index 写 curated，index/cache 只能在 `runtime/hermes/`；
  5. 不把 issue 中仍有争议的性能/复现结论直接晋升 active fact。

#### 风险边界

- **License**：API 与根 LICENSE 为 MIT；仍需逐项审 transitive dependency。
- **维护活跃度**：固定 commit 与查询同日；tags 活跃，但 GitHub Releases API 为 0，不能声称有对应 GitHub release。
- **安全风险**：unsafe SIMD 注释明确错误 buffer/scalar 可越界读；公共 `from_parts`/loader validation 是 soundness boundary。恶意 index 文件需依靠 size cap、checked arithmetic、format validation。
- **局限/不适用**：README 性能/压缩数字未在本机复现；本机无 cargo，因此源码测试运行待核验。近似量化不适用于必须 exact similarity 的任务；首批小于 1000 时 TQ+ 回退 identity；rotation 跨 backend 可复现性仍有 open issue。

---

### 项目 3. andrewyng/aisuite

- **仓库**：<https://github.com/andrewyng/aisuite>
- **API 基本信息**：Stars: **15,213**；Forks: **1,614**；License: **MIT**；Language: Python；`updated_at`: 2026-07-25T23:23:13Z；`pushed_at`: 2026-07-25T19:14:07Z。
- **固定快照**：[`cb29165`](https://github.com/andrewyng/aisuite/commit/cb29165b00f719cceae6a82ed4621cbcb79aaaf7)，commit time 2026-07-25T19:14:04Z。
- **Release / Issues**：[`v0.1.3`](https://github.com/andrewyng/aisuite/releases/tag/v0.1.3) 发布于 2026-07-20；[#369](https://github.com/andrewyng/aisuite/issues/369) 报告 Groq/Ollama multi-turn tool calling 问题，[#342](https://github.com/andrewyng/aisuite/issues/342) 报告 PyPI dependency metadata 问题。
- **一句话判断**：aisuite 值得学的是把 provider-neutral 调用外包给薄 adapter 后，把真正的生产复杂度集中在 **runner state、per-tool policy、artifact/trace、continuation revision**。
- **解决的问题**：替代每个 provider 各写一套消息/tool loop、工具默认裸执行、跨进程 continuation 覆盖状态、subagent 与父 run 无 trace 关联的旧做法。

#### 架构/实现与数据流

README 明确仓库分两层：统一 Chat Completions API 与 Agents API；原 `platform/` 的 OpenWorker snapshot 已迁到独立仓库且未来会移除，不能把 snapshot 当 aisuite 稳定 public API。

```text
andrewyng/aisuite/
├── aisuite/client.py                # provider route、sync/async tool loop、MCP config
├── aisuite/providers/               # provider adapters
├── aisuite/agents/
│   ├── runner.py                    # run/continue、state/artifact/trace 组装
│   ├── policies.py                  # allow/deny/approval policy
│   ├── state_store.py               # memory/file store + optimistic revision
│   ├── postgres_state_store.py      # durable backend
│   ├── tools.py                     # Agent-as-tool 与 parent context 传播
│   └── types.py                     # Agent/RunState/RunResult/ToolMetadata contracts
├── aisuite/utils/tools.py           # schema inference、argument validation、policy chokepoint
├── aisuite/toolkits/{files,git,shell}.py
├── aisuite/mcp/                     # MCP config/client/schema conversion
├── aisuite/tracing/                 # events/sinks/store/viewer
├── tests/agents/                    # runner/policy/state/artifact/trace/subagent tests
└── platform/                        # OpenWorker 旧 snapshot，非未来稳定入口
```

数据流：`Agent + input -> Runner builds messages/context -> Client resolves provider -> model returns tool_calls -> Tools validates args -> tool policy evaluates at invocation chokepoint -> denied result or execution -> tool event/model trace -> RunResult -> optional dehydrated artifacts + StateStore revision`。Continuation 从 `RunResult` 或 `(Agent,state_store,thread_id)` 恢复。

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `aisuite/agents/runner.py` | 生命周期编排 | state/thread 成对约束、run/continue、trace context、artifact hydrate/dehydrate、result steps |
| `aisuite/utils/tools.py` | 真正执行 chokepoint | Pydantic arg validation、policy context、deny result、sync/async execution、trace preview |
| `aisuite/agents/policies.py` | policy primitives | AllowAll/DenyAll/AllowTools/RequireApproval；bool 或结构化 decision |
| `aisuite/agents/state_store.py` | continuation storage | schema_version、atomic `os.replace`、revision compare-and-swap、URL-quoted thread file |
| `aisuite/agents/tools.py` | subagent composition | Agent 包成 callable tool，传播 parent trace/group/tags/policy/artifact store |
| `pyproject.toml` | dependency surface | core Pydantic/docstring/httpx，provider/MCP/Postgres 作为 extras |

#### 源码精读 1：Runner 把工具策略与证据上下文一起下传

固定源码：[`runner.py#L118-L193`](https://github.com/andrewyng/aisuite/blob/cb29165b00f719cceae6a82ed4621cbcb79aaaf7/aisuite/agents/runner.py#L118-L193)

```python
async def _run_impl(agent, input, *, tool_policy=None,
                    state_store=None, thread_id=None, artifact_store=None, **kwargs):
    if (state_store is None) != (thread_id is None):
        raise ValueError("state_store and thread_id must be provided together.")
    if state_store is not None and state_store.load_state(thread_id) is not None:
        raise ThreadAlreadyExistsError("Use continue_sync(...) to continue")

    request_kwargs = {**agent.model_settings, **kwargs}
    if agent.tools:
        request_kwargs["tools"] = agent.tools
        request_kwargs["max_turns"] = effective_max_turns
    if tool_policy is not None:
        request_kwargs["tool_policy"] = tool_policy
        request_kwargs["tool_policy_context"] = {
            "agent_name": agent.name, "trace_id": active_trace_id,
            "group_id": effective_group_id, "messages": copy.deepcopy(messages),
        }
```

逻辑摘要：新 run 拒绝覆盖已存在 thread；policy 不是只拿 tool name，而是得到 agent/run/trace/group/tags/metadata/messages，便于 scope-aware 决策。注意上下文丰富也提高敏感数据泄露风险，policy/trace sink 不应默认持久化完整 secrets/messages。

#### 源码精读 2：policy 在参数验证后、函数调用前判定

固定源码：[`utils/tools.py#L440-L531`](https://github.com/andrewyng/aisuite/blob/cb29165b00f719cceae6a82ed4621cbcb79aaaf7/aisuite/utils/tools.py#L440-L531)

```python
def _prepare_tool_call(self, tool_call, tool_policy, tool_policy_context):
    # parse registered tool + Pydantic validate
    validated_args_dict = param_model(**arguments).model_dump()
    decision = self._evaluate_tool_policy(
        tool_policy, tool_policy_context, tool_name,
        validated_args_dict, tool_metadata,
    )
    if decision is not None and not decision.allowed:
        self._emit_tool_trace_event("tool.denied", tool_event)
        return {
            "denied": True,
            "result": {"error": "Tool call denied by policy",
                       "reason": decision.reason},
            # ...
        }
    self._emit_tool_trace_event("tool.allowed", tool_event)
    self._emit_tool_trace_event("tool.started", tool_event)
    return ctx
```

逻辑摘要：Pydantic 先把 argument 变成确定结构，再让 policy 判断；deny 不调用函数，而是作为 tool message 回给模型；allow/started/completed/failed 都可发 trace。边界：`tool_policy is None` 时默认执行，`ToolMetadata.requires_approval` 本身不会自动构成 enforcement，调用者必须配置 policy。

#### 源码精读 3：FileStateStore 用 revision + atomic replace 防覆盖

固定源码：[`state_store.py#L101-L148`](https://github.com/andrewyng/aisuite/blob/cb29165b00f719cceae6a82ed4621cbcb79aaaf7/aisuite/agents/state_store.py#L101-L148) 与 [`#L171-L182`](https://github.com/andrewyng/aisuite/blob/cb29165b00f719cceae6a82ed4621cbcb79aaaf7/aisuite/agents/state_store.py#L171-L182)

```python
class FileStateStore:
    def save_state(self, thread_id, state, *, revision=None, metadata=None):
        current = self.load_state(thread_id)
        _assert_revision(thread_id, current.revision if current else None, revision)
        stored = _next_stored_state(thread_id, state, current=current, metadata=metadata)
        self._write_stored_state(stored)
        return stored

    def _write_stored_state(self, stored):
        tmp_path = path.with_name(f".{path.name}.{new_id('tmp')}.tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(stored.to_dict(), handle, sort_keys=True)
        os.replace(tmp_path, path)
```

```python
def _assert_revision(thread_id, current_revision, expected_revision):
    if expected_revision is not None and current_revision != expected_revision:
        raise StateConflictError(
            f"expected {expected_revision}, found {current_revision}."
        )
```

逻辑摘要：文件替换避免 partial JSON；revision 提供乐观并发 check；continuation load 后用 `stored.revision` 保存下一版。边界：FileStateStore 没有跨进程 lock，两个 writer 仍可能同时通过 load/check 后先后 replace，CAS 不是原子事务；高并发应使用有事务语义的 backend 或外层锁。

#### 依赖分析与供应链风险

`pyproject.toml` core：Python ^3.10、`docstring-parser >=0.16,<1.0`、Pydantic ^2.10、httpx `>=0.27,<1`；providers / speech / MCP / Postgres 大多 optional extras。lock 核验：pydantic 2.13.4、docstring-parser 0.18.0、httpx 0.28.1、openai 1.107.0、anthropic 0.116.0、mcp 1.10.1、psycopg 3.3.4。

风险：`[all]` 会显著放大供应链与 credential 面；MCP 可启动外部 command；toolkits 含 shell/files/git；provider SDK 版本范围较宽，issue #342 还显示发布 metadata 可与源码声明偏离。因此只装最小 extras、校验 wheel metadata/lock，并把 command/tool execution 放 policy chokepoint。

#### 可复用经验、实验与落地路径

- **当**工具具有不同 effect/risk 且模型能自行选工具**时，应优先**在参数解析后、实际调用前执行逐工具 policy，并把 allow/deny/failure 写成结构化 evidence；因为 prompt 禁令不是 enforcement，边界是无 policy 时必须明确默认行为。
- **可尝试实验（30 分钟）**：在 `runtime/hermes/github-learning-poc/tool-policy-state-contract/` 用 fake tools 建 4 个 fixture：read allow、write deny、approval missing、stale revision conflict；输出四状态与 JSONL evidence，不调用真实 provider/MCP/shell。
- **Skill 升格判断：需二次验证。** policy/state/trace 模式与 shared hub 高度相关，但本地已有 verification-first、self-reflection、subagent 四状态等事实/能力，必须先去重；不直接把 aisuite runtime 引入 Hermes。
- **Hermes/shared hub 落地路径**：
  1. POC 定义 `ToolEffect = read|write|network|exec|config|secret` 与 `Decision = allowed|denied|needs_confirmation|blocked`；
  2. 在 Hermes 审计流程中把 effect/scope/evidence 作为工具执行前后记录，而不是改 provider；
  3. run state/checkpoints 写 `runtime/hermes/`，raw trace 写 `inbox/hermes/daily/` 或 runtime，不写 curated；
  4. 只有稳定 class-level contract 通过 fixtures 与治理审查后，才更新现有 shared verification/governance skill 与 manifest；
  5. OpenClaw/future-agent 只消费同一 effect schema，不复制 Python runner；本任务不触碰其运行时。

#### 风险边界

- **License**：API 与 LICENSE 为 MIT；provider SDK/MCP/toolkit 依赖另审。
- **维护活跃度**：固定 commit 在 2026-07-25；latest release v0.1.3 在 2026-07-20，活跃。
- **安全风险**：tool policy 默认为 optional；shell/files/git/MCP 能产生高副作用；trace/context 可能记录 arguments/messages/result preview；state/artifact store 需要脱敏与权限控制。
- **局限/不适用**：issue #369 表明 provider-specific multi-turn 差异仍会突破统一抽象；FileStateStore 的 revision check 不是跨进程原子 CAS；README 所示 OpenWorker 已迁独立 repo，`platform/` snapshot 不能作为稳定依赖。

---

## 经验沉淀

1. **当控制权或授权会在任务期间变化时，应优先在最终副作用 chokepoint 重验 ownership/effect/scope，并把用户接管视为 hard stop；因为早期授权不是永久租约，边界是宿主状态不可用时应 blocked。**
2. **当页面元素、向量 slot 或 run revision 是短期内部身份时，应优先另设稳定外部 identity，并显式校验 version/scope；因为内部位置会随 DOM、删除或并发变化，边界是稳定 ID 也不能替代当前授权。**
3. **当检索受 ACL/tenant 约束时，应优先把权威 allowlist 推到 scorer/kernel，而不是后置过滤；因为后过滤会造成结果缺失和额外计算，边界是 ACL 获取失败必须 fail-closed。**
4. **当可变策略会拖慢热路径时，应优先在边界预计算并折叠成稳定输入（如 calibration→LUT bias、policy→decision），同时版本化该变换；因为热 kernel 应保持简单，边界是预计算必须可复现、可失效。**
5. **当 Agent 工具可执行文件、网络、配置或 shell 时，应优先逐工具声明 effect/metadata，再在真实调用前执行 policy；因为 manifest/description 只是声明，边界是 `requires_approval` 没有 enforcement 就等于没有审批。**
6. **当状态跨进程 continuation 时，应优先使用 atomic write + revision check + durable transactional backend；因为只做 JSON overwrite 会丢更新，边界是文件级 compare-then-replace 仍不是跨进程原子 CAS。**
7. **当经验要长期复用时，应优先拒绝 snapshot ref、一次性 path、未核验 benchmark 与动态 stdout进入 shared skill；因为 class-level contract 必须稳定，边界是 raw 证据仍可留 inbox/runtime 待审。**
8. **当开源 harness 依赖 closed-source runtime 或可选外部服务时，应优先分别声明两者的 license、测试覆盖和信任边界；因为开源 tests 不能证明闭源本体行为，边界是不应把仓库 license 外推。**

### 今日最小综合实验

建议先实现 `runtime/hermes/github-learning-poc/effect-scope-contract/`：一个不联网、不改配置的 fixture runner，输入 `actor/scope/resource/effect/stable_id/revision/allowlist`，依次执行 `precondition -> policy -> deterministic operation -> postcondition -> evidence`，覆盖：用户接管、ACL lookup failed、ambiguous selector、stale revision、index version mismatch。预期只输出 `completed|blocked|denied|failed` 与原因；这能同时验证三个项目的共同机制，而不是分别复制框架。

## 风险边界（跨项目）

- GitHub API 的 Stars、License、更新时间是查询快照；License API 不是完整依赖 license 审计。
- 不自动安装 ego lite、turbovec、aisuite 到 Hermes；不自动运行 MCP/shell/browser 登录态；不自动改模型/provider/config/cron/secret。
- 不复制 closed-source 浏览器实现；不复制 GPL/NOASSERTION 项目源码；MIT/Apache 代码也不因许可宽松就自动进入 shared。
- 不把 README benchmark 当本机结论；ego harness tests 与 aisuite focused tests 已真实执行，turbovec 因缺 cargo 明确标为运行待核验。
- 不直接写 `curated/memory` active fact，不直接创建/修改 shared skill；本报告只提出候选，等待治理去重、评分、证据与审查。
- trace、messages、browser login state、vector index 都可能包含敏感内容：raw 只进 agent-local runtime/inbox，不能进 curated 或 Git 主线。

## Skill 升格总判断

- `citrolabs/ego-lite`：**需二次验证**。候选只取 ownership/handoff + stable locator + observe/verify contract，不安装其强触发 skill，不依赖闭源 runtime。
- `RyanCodrai/turbovec`：**需二次验证**。候选是 retrieval authorization/index integrity contract，不把算法/SIMD 实现包装成 skill。
- `andrewyng/aisuite`：**需二次验证**。候选是 effect-aware tool policy + revisioned continuation evidence，先与既有 shared verification/subagent/governance 能力去重。
- 今日没有“可直接迁移”项目：三项都触及高权限、持久状态或运行时依赖；直接升格会违背 shared skill 的稳定、可验证、跨 Agent 契约要求。

## Hermes/shared hub 落地路径

1. **实验层**：只创建 `runtime/hermes/github-learning-poc/effect-scope-contract/`，不进 curated/Git；fixture 不连接 provider、browser、MCP、外部索引。
2. **接口层**：定义可迁移 JSON schema：
   - request: `{actor, scope, resource, stable_id, revision, effect, constraints}`；
   - decision: `{status, reasons, evidence_refs, postcondition}`；
   - status 仅 `completed|blocked|denied|failed`。
3. **Hermes 接入候选**：将 schema 用于 `scripts/github_learning_orchestrator.py` 后续研究工具证据记录和本地 audit，不改变当前 provider/tools 配置。
4. **shared 接入候选**：先搜索/对比 `capabilities/manifests/shared-skills.yaml` 及 verification-first/subagent/governance 能力；优先更新已有 skill，避免新建宽泛 `agent-safety` 重复技能。
5. **记忆治理**：实验结果与真实 incident 达到稳定复用门槛后，再提交 `curated/memory/facts/` candidate，经评分、去重、脱敏、人工/总控审查；repo 原始分析永久保留 inbox/runtime。
6. **未来 Agent**：只依赖 portable schema 和 `scripts/resolve_shared_root.py`，禁止硬编码本机绝对路径；不要求 future-agent 使用同一语言/runtime。

## 明日继续

1. 安装隔离 Rust toolchain 前先检查任务政策；若允许，在 turbovec 固定 commit 运行 workspace tests，并复现一个小型 allowlist correctness fixture，不先跑昂贵 benchmark。
2. 阅读 turbovec `io.rs/from_parts` 与 issue #206 的复现上下文，验证 rotation fingerprint 在不同 thread/BLAS 下的实际边界。
3. 检查 ego-lite site learning Node tool 是否有 capability/effect metadata；若没有，设计不执行动态代码的 manifest static auditor。
4. 对 aisuite 运行跨进程 FileStateStore race fixture，确认 compare-then-replace 的冲突窗口；再评估 PostgresStateStore 事务行为。
5. 最小动作：实现上述 `effect-scope-contract` fixture POC，并以 blocked/denied/failed 断言，而不是只生成说明文档。

## 候选反哺

### Candidate Facts

- [ ] topic: transient internal identity must be separated from stable external identity | evidence: ego `backendNodeId/ref` lifecycle；turbovec `IdMapIndex`；aisuite state revision | 建议: create（与现有 identity/scope facts 去重后） | 安全级别: low
- [ ] topic: authorization filters belong at the final scorer/invocation chokepoint | evidence: turbovec `search_with_mask`/kernel mask；aisuite `_prepare_tool_call`；ego ownership hard-stop contract | 建议: update existing verification-first fact | 安全级别: medium
- [ ] topic: file revision check plus atomic replace is not transactional CAS | evidence: aisuite `load -> _assert_revision -> os.replace` 源码 | 建议: create only after race fixture | 安全级别: medium

### Candidate Skills / Workflow

- [ ] 名称: effect-scope-contract fixture workflow | 可复用场景: browser actions、tool calls、retrieval、continuation | 是否建议 shared: yes（POC 后） | 原因: 跨 Hermes/OpenClaw/future-agent 的通用副作用契约，但需先与现有 verification/governance skill 去重
- [ ] 名称: durable-learning-manifest static auditor | 可复用场景: 拒绝临时 ref、路径逃逸、未声明 effect 的长期工具 | 是否建议 shared: yes（先本地） | 原因: ego learning validator 提供机制证据；当前需补 effect/capability 与不执行 import 的安全设计
- [ ] 名称: retrieval authorization/index integrity contract | 可复用场景: shared memory index、多租户知识检索 | 是否建议 shared: no（当前） | 原因: 需要真实索引、ACL failure 与 schema migration fixtures 后再决定

### Candidate Open Questions

- [ ] 问题: ego site Node tool 的 manifest/path validation 是否足以限制 runtime capability，能否加入 effect metadata 和 sandbox？ | reason: gap | priority: high
- [ ] 问题: turbovec rotation fingerprint 在 issue #206 所述跨 BLAS/thread drift 下，是容忍合法差异还是可能接受召回下降？ | reason: conflict | priority: high
- [ ] 问题: aisuite FileStateStore 两个进程同时从 revision N 写 N+1 时是否会 silent last-writer-wins？ | reason: gap | priority: high
- [ ] 问题: 现有 shared verification/subagent skills 中哪个最适合承载 effect-scope schema，避免新增重复 skill？ | reason: adaptation | priority: medium

### 不应自动落地

- 不自动安装或启用 ego lite、turbovec、aisuite；不自动连接真实登录态、MCP、provider 或 shell。
- 不自动改 Hermes/OpenClaw 配置、模型、provider、cron、secret；本任务也不调用 OpenClaw。
- 不把候选直接写 curated active facts，不把 runtime index/trace/cache 提交 Git，不复制 license 不明或 closed-source 部分。
- 不用审计关键词替代真实验证；turbovec 测试因缺 cargo 仍是明确剩余风险。
