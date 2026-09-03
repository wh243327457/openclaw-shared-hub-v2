# 2026-09-03 GitHub 热门项目学习日报

> 执行者：Hermes（未调用 OpenClaw）  
> GitHub API 查询时间：2026-09-03 07:30-07:42 CST  
> 深读源码固定版本：`firecrawl/anydoc@261fc257d17c3eab0f673be31c408fd9fdc2171a`、`dmmulroy/anti-slop@e8c4880471b23ab7f216fba7b27d173a6ef07d4c`  
> 证据范围：GitHub REST API、README、release/issues、固定提交源码、本机锁文件安装与测试。动态 Stars 仅代表上述查询快照。

## 今日结论

今天最值得迁移的不是某个热门工具本身，而是两种确定性质量外壳：**复杂文档先经过内容识别、统一模型、硬资源上限与显式终态，再交给 Agent；低证据 TypeScript 模式则在 AST/词法作用域层被拒绝，并要求断言留下可审计理由。**

## 项目速览

以下 Stars、Language、License、最近更新时间均由 GitHub API 实查；`updated_at` 是仓库活动时间，不等同于最新源码提交时间。

| 项目 | Stars | Language | License | GitHub `updated_at` | 快速判断 |
|---|---:|---|---|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 209,564 | TypeScript | MIT | 2026-09-02T23:30:26Z | 插件化 Agent harness，热度很高，但今日不重复深读既有主题 |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 26,588 | Shell | MIT | 2026-09-02T23:29:56Z | 文件化可恢复计划，与现有 completion/receipt 候选高度相关 |
| [firecrawl/anydoc](https://github.com/firecrawl/anydoc) | 20,047 | Rust | MIT | 2026-09-02T23:19:14Z | 多格式文档进入统一 Markdown/Document contract，适合深读增量变化 |
| [jdx/mise](https://github.com/jdx/mise) | 33,395 | Rust | MIT | 2026-09-02T23:29:22Z | 工具版本、环境变量和任务执行统一入口，成熟但范围较大 |
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | 40,939 | C++ | MIT | 2026-09-02T23:29:48Z | 进程内分析数据库，适合后续研究本地 evidence 查询层 |
| [CopilotKit/OpenBot](https://github.com/CopilotKit/OpenBot) | 3,898 | TypeScript | MIT | 2026-09-02T23:25:05Z | 先决策、后执行、全记录的 coworker runtime，需另做 authority 审查 |
| [dmmulroy/anti-slop](https://github.com/dmmulroy/anti-slop) | 4,008 | TypeScript | MIT | 2026-09-02T23:30:04Z | 用 Oxlint 把“丢证据再断言”等模式变成可执行质量门，今日重点深读 |

补充 API 快照：`anydoc` 1,210 forks、仓库 API 的 `open_issues_count=82`、`pushed_at=2026-08-28T02:13:16Z`；`anti-slop` 88 forks、`open_issues_count=3`、`pushed_at=2026-08-31T21:35:30Z`。GitHub 的 `open_issues_count` 同时包含 issue 与 PR，不能当纯 issue 数。

## 深读项目

### 1. firecrawl/anydoc

- **链接**：https://github.com/firecrawl/anydoc
- **固定版本**：`261fc257d17c3eab0f673be31c408fd9fdc2171a`；Cargo 版本 `0.2.4`
- **API 元数据**：Stars **20,047**；Forks **1,210**；Language **Rust**；License **MIT**；最近 push **2026-08-28T02:13:16Z**
- **Release / issue 证据**：`v0.2.4` 于 2026-08-27 发布，新增扫描页显式 `NeedsOcr` 与 opt-in hosted OCR；open issue [#128](https://github.com/firecrawl/anydoc/issues/128) 请求 `.eml/.msg` 支持。
- **一句话判断**：值得学的是“输入身份 → parser → canonical Document → 单一 serializer → typed terminal”的摄取契约，而不是直接安装上游 Agent Skill。
- **解决的问题**：替代按扩展名选择零散转换器、每种格式各写一套 Markdown 输出、扫描页静默丢失、调用方忘记配置解压/XML上限等旧做法。

#### 架构/实现与数据流

```text
bytes/path
  -> Format::from_bytes（内容/容器身份；CSV 才回退 extension/显式 format）
  -> formats::parse（DOC/DOCX/PPT/PPTX/表格/ODF/RTF/EPUB/CSV）
  -> model::Document（blocks/inlines/tables/notes/assets）
  -> render::markdown::document_to_markdown
  -> Markdown

特殊支路：PDF -> pdf-inspector -> Markdown；检测到真实空白扫描页则 NeedsOcr
边界外支路：Node/Python/CLI 在显式 opt-in 后可把整份 PDF 发往 hosted OCR
```

关键设计点：

1. `Format::from_bytes` 先识别 RTF/OLE/ZIP/PDF，并按规范中的 container identity 分流；不是对正文做模糊猜测。
2. 非 PDF 格式进入共享 `Document` 模型，使表格转义、脚注编号、锚点、列表等修复只做一次。
3. PDF 是公开例外：`pdf-inspector` 直接产生 Markdown；`to_document` 对 PDF 明确拒绝，避免伪装成统一模型。
4. 固定资源上限在库内不可配置；调用方漏配也不能关闭基础防线。
5. Node/Python/Wasm 是 core 的 adapter；hosted OCR 不是 Rust core 默认行为，且会发送整份文档。

#### repo tree 摘要

```text
anydoc/
├── src/
│   ├── lib.rs                 # 公共 API、格式解析入口、PDF 特殊路由
│   ├── error.rs               # ConvertError typed terminal
│   ├── formats/               # csv/doc/docx/epub/odf/pdf/ppt/pptx/rtf/sheet
│   ├── model/                 # canonical Document/Block/Inline/Table/Asset
│   ├── package/               # ZIP/XML/path/relationship 与资源限制
│   ├── render/markdown/       # 单一 GFM serializer
│   └── shared/                # 跨格式复用的列表、数学、HTML、资产等逻辑
├── node/                      # N-API binding 与 CLI
├── python/                    # PyO3/maturin binding
├── wasm/                      # browser WebAssembly adapter
├── tests/fixtures/            # 正常、畸形与 abuse 文档
├── tests/snapshots/           # 格式输出快照
├── tests/robustness.rs        # fixture mutation 不崩溃验证
├── fuzz/                      # cargo-fuzz targets
├── skills/                    # 上游自带文档转换 Agent Skill
└── Cargo.toml / Cargo.lock
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/lib.rs` | 公共入口 | 内容优先识别格式；PDF direct path；其余解析为 `Document` 后统一渲染 |
| `src/formats/detect.rs` | 内容/容器识别 | RTF marker、OLE stream、ZIP mimetype/relationship/content type/root element、PDF header |
| `src/formats/mod.rs` | parser 分派 | `Format` 到各 parser 的显式 match；PDF 对 document model 返回 Unsupported |
| `src/model/*` | canonical 模型 | blocks、inlines、tables、notes、assets 等格式无关结构 |
| `src/render/markdown/mod.rs` | GFM serializer | 锚点、脚注、block/list/table/code/math 的统一投影 |
| `src/package/limits.rs` | abuse 防线 | 解压、条目、XML 深度/节点、表格展开、资产和二进制记录硬上限 |
| `src/formats/pdf.rs` | PDF 特殊支路 | 二次核验 OCR 页，避免把缺页输出当完整成功 |
| `tests/robustness.rs`、`tests/fixtures/abuse/` | 对抗验证 | mutation 不 panic；zip bomb、deep XML、巨大 span/repeat 等必须硬失败 |

#### ⭐ 源码精读

**函数 1：`to_markdown_bytes` 把 PDF 例外与 canonical model 主路径写成显式分支。**

```rust
pub fn to_markdown_bytes(
    bytes: &[u8],
    format: impl Into<Option<Format>>,
) -> Result<String, ConvertError> {
    let format = resolve_format(bytes, format.into())?;
    if format == Format::Pdf {
        return formats::pdf::to_markdown(bytes);
    }
    Ok(document_to_markdown(&to_document(bytes, format)?))
}
```

逻辑摘要：先解析权威格式；PDF 直接调用 `pdf-inspector`，其他格式必须先产出 `Document`。优点是例外没有被接口叙述掩盖；边界是 PDF 无法通过 `to_document` 提供与其他格式相同的 assets/model 能力。

**函数 2：`from_bytes` 按强身份顺序检测，container signature 优先于内部偶然字节。**

```rust
pub(crate) fn from_bytes(bytes: &[u8]) -> Option<Format> {
    if bytes.starts_with(b"{\\rtf") { return Some(Format::Rtf); }
    if bytes.starts_with(&OLE_MAGIC) { return detect_ole(bytes); }
    if bytes.starts_with(b"PK\x03\x04") { return detect_zip(bytes); }
    if bytes[..bytes.len().min(1024)].windows(5).any(|w| w == b"%PDF-") {
        return Some(Format::Pdf);
    }
    None
}
```

逻辑摘要：RTF/OLE/ZIP 先按顶层身份处理，再在最多 1024 字节内找 PDF header。源码测试还验证“ZIP 内嵌 PDF”不会被误判为 PDF。CSV 没有签名，因此保持 `None`，由显式 format 或 extension 负责。

**函数 3：`parse` 是可审计的 parser 路由表。**

```rust
pub fn parse(bytes: &[u8], format: Format) -> Result<Document, ConvertError> {
    match format {
        Format::Excel => sheet::parse(bytes),
        Format::Csv => csv::parse(bytes),
        Format::Docx => docx::parse(bytes),
        Format::Odt | Format::Ods | Format::Odp => odf::parse(bytes),
        Format::Pptx => pptx::parse(bytes),
        Format::Epub => epub::parse(bytes),
        Format::Rtf => rtf::parse(bytes),
        Format::Doc if bytes.starts_with(b"{\\rtf") => rtf::parse(bytes),
        Format::Doc => doc::parse(bytes),
        Format::Ppt => ppt::parse(bytes),
        Format::Pdf => Err(ConvertError::Unsupported(/* ... */)),
    }
}
```

逻辑摘要：没有隐式 plugin discovery；每个格式的 owner 清楚。`.doc` 包装 RTF 是一个具名兼容分支。PDF 不伪造 `Document`，调用错误入口会得到稳定错误。

**函数 4：PDF 对“疑似 OCR”进行第二次提取核验，再决定终态。**

```rust
pub fn to_markdown(bytes: &[u8]) -> Result<String, ConvertError> {
    let result = pdf_inspector::process_pdf_mem(bytes).map_err(map_error)?;
    if !result.pages_needing_ocr.is_empty() {
        let flagged: Vec<u32> = result.pages_needing_ocr.iter().map(|page| page - 1).collect();
        let pages = pdf_inspector::extract_pages_markdown_mem(bytes, Some(&flagged))
            .map_err(map_error)?
            .pages_needing_ocr;
        if !pages.is_empty() {
            return Err(ConvertError::NeedsOcr { pages, page_count: result.page_count });
        }
    }
    // 非空 Markdown 才成功，否则 Unsupported
    /* ... */
}
```

逻辑摘要：初筛可能对短文本/图片多的页面过报，所以只对标记页二次提取；确认缺文本才返回 `NeedsOcr`。这是“便宜 classifier → bounded verifier → typed terminal”的可迁移实现。

#### 依赖分析与供应链风险

`Cargo.toml` 直接运行依赖：`cfb 0.14.0`、`csv 1.4.0`、`flate2 1`、`encoding_rs 0.8.35`、`log 0.4`、`pdf-inspector 1.14.2`、`quick-xml 0.41.0`、`zip 8.6.0`；开发依赖为 `insta 1`、`sha2 0.11`。项目要求 Rust 1.88。

真实检查：

- `cargo test`：lib **286 passed / 0 failed**；robustness **1 passed / 0 failed**；snapshots **9 passed / 0 failed / 1 ignored**；doc tests 0。被忽略项需要本地 gitignored samples corpus。
- 本机 smoke：`cargo run --example convert -- tests/fixtures/csv/handmade-quoted.csv` 成功，输出结构化 GFM 表格；单次观测为 **1.22ms**，这不是正式 benchmark。
- `cargo audit` 扫描锁文件 186 个 crate dependency，未报 vulnerability，但报两条 warning：`ttf-parser 0.25.1` **unmaintained**（RUSTSEC-2026-0192）和 `chacha20 0.10.1` **yanked**。`cargo tree -i` 显示两者都经 `pdf-inspector -> lopdf` 路径进入。
- 未运行 Node/Python/Wasm 全套 binding 测试、fuzz、hosted OCR 和 README 的 100 文档 benchmark，相关结论不能外推。

#### 可复用经验

- 当 Agent 摄取 DOCX/PDF/ZIP 等复杂文件时，应优先使用**内容/容器身份 + typed terminal + output hash/coverage**，因为扩展名和非空 Markdown 都不能证明内容完整；边界是 explicit format override 仍需 host policy。
- 当多种输入格式需要同一种输出时，应优先先构造**格式无关 canonical model**再投影，因为转义、表格、脚注与锚点修复可以集中复用；边界是 parser 在进入模型前漏掉的内容仍需格式级 coverage tests。
- 当 parser 面对不可信压缩包/XML/二进制输入时，应优先在库内设置**不可由调用方关闭的硬下限**，因为无人值守调用方可能漏配；边界是内存上限不能替代 CPU deadline、进程隔离和系统级资源控制。
- 当便宜检测器可能误报昂贵 fallback 时，应优先对候选单元做 bounded 二次核验并返回 reason-coded terminal，因为一次 heuristic 不能直接授权网络 OCR；边界是二次检测也有误差，需真实 corpus 校准。

#### 可尝试实验（30 分钟）

增量扩展已有 `runtime/hermes/github-learning-poc/document-ingestion-receipt/`：用公开/synthetic 的 CSV、text PDF、scanned PDF、伪扩展 ZIP 四个 fixture，输出 `source_hash / declared_extension / detected_format / converter_commit / terminal / coverage / output_hash / network_used`；强制 scanned PDF 在未授权时为 `blocked_needs_ocr`。不接 hosted OCR，不处理私有文件。

#### 风险边界

- **License**：仓库 API、Cargo manifest 与 `LICENSE` 均为 MIT；这不等于所有传递依赖、OCR 服务、输入文档版权都已完成合规审查。
- **维护活跃度**：固定提交最后一次 push 为 2026-08-28；`v0.2.4` 于 2026-08-27 发布，仓库 API 2026-09-03 查询仍有活动。短期活跃不证明长期维护。
- **安全风险**：复杂格式解析天然暴露压缩/XML/PDF 攻击面；虽然有 hard caps、abuse fixtures、mutation test，仍缺本次 fuzz、CPU deadline 与 sandbox 验证。RustSec 还有 unmaintained/yanked 传递依赖警告。
- **隐私/费用**：hosted OCR 会发送整份文档且不能只发缺 OCR 页；默认不可自动启用，必须显式授权、记录网络使用与目标服务。
- **局限/不适用**：PDF 不进入共享 `Document` 模型；扫描件需 OCR；`.eml/.msg` 尚是 issue；本次未核验宏、嵌入对象语义和全格式真实 corpus。

#### ⭐ Skill 升格判断

**需二次验证。** 已有 `document-ingestion-receipt` 候选和现有文件读取能力，今日不新增重复 shared skill，也不直接安装上游 skill。先补终态/coverage fixtures、传递依赖处置和 Hermes adapter 的真实 readback，再决定是否更新既有能力。

#### ⭐ Hermes / shared hub 落地路径

- Hermes POC：`runtime/hermes/github-learning-poc/document-ingestion-receipt/`
- 原始研究：`inbox/hermes/daily/2026-09-03-github-learning.md`
- 若验证通过，优先更新现有文档摄取/verification skill 的 contract，而非新建重复 skill；canonical 位置只能在 `capabilities/skills/` 下，并同步 `capabilities/manifests/shared-skills.yaml`。
- 建议 agent-neutral 接口：`ingest(input_ref, declared_format?, allow_network=false) -> {terminal, detected_format, coverage, source_hash, output_ref, output_hash, network_used, error_code}`。
- Hermes host adapter 负责真实 path resolution、预算、OCR 授权和 artifact readback；未来其他 agent 只能经 shared contract 自己实现 adapter，不能共享 runtime 临时路径。

---

### 2. dmmulroy/anti-slop

- **链接**：https://github.com/dmmulroy/anti-slop
- **固定版本**：tag `v0.1.2` 指向 `e8c4880471b23ab7f216fba7b27d173a6ef07d4c`
- **API 元数据**：Stars **4,008**；Forks **88**；Language **TypeScript**；License **MIT**；最近 push **2026-08-31T21:35:30Z**
- **Release / issue 证据**：GitHub Releases API 未返回 release；仓库有 `v0.1.2` annotated tag。固定提交对应 Actions CI 为 success。open issue [#37](https://github.com/dmmulroy/anti-slop/issues/37) 询问 TypeScript 7 支持；仓库自身 devDependency 已固定 `typescript 7.0.2`，但 issue 尚无结论，不能替维护者回答。
- **一句话判断**：它把“保留类型证据、边界只解析一次、必要断言说明 invariant、测试走真实 seam”等偏好变成 AST 规则，适合作为 Agent 生成代码后的确定性复核候选。
- **解决的问题**：替代只靠 prompt 要求“写安全 TypeScript”、人工 code review 才发现双重断言/宽化/模块 mock，以及 lint 规则以 npm 黑盒包漂移的旧做法。

#### 架构/实现与数据流

```text
Oxlint source parse + lexical scope
  -> src/index.ts 注册 15 条 generic rules
  -> rule visitor（CallExpression / TSAsExpression / type annotation 等）
  -> same-file alias/scope/evidence predicate
  -> context.report(stable messageId + source node)

可选支路：Effect 项目 -> src/effect/index.ts -> no-service-constructor-imports
分发方式：Agent Skill installer -> vendor src 到目标仓库 -> 配置 jsPlugins -> lint/typecheck/test
```

它刻意不使用 TypeScript type checker，而使用 Oxlint ESTree 与 lexical-scope API；因此能快速处理同文件 alias、shadowing、局部 const flow，但不推断 imported type 或跨文件 call signature。规则分成：

1. **证据保留**：`no-known-value-widening`、`no-widen-then-assert`、unknown/unsafe dictionary 相关规则。
2. **显式 invariant**：`require-safety-comment-for-type-assertion`。
3. **真实依赖 seam**：`no-module-mocking`。
4. **避免动态反射/临时 narrowing**：`no-reflect-get/apply`、`no-runtime-typeof`。
5. **框架策略隔离**：Effect-specific plugin 不默认加载。

#### repo tree 摘要

```text
anti-slop/
├── src/
│   ├── index.ts                       # generic plugin 注册表
│   ├── rules/                         # 15 条规则及逐规则 RuleTester 文件
│   ├── shared/                        # type alias、lexical scope、dictionary 分类等复用逻辑
│   └── effect/                        # 显式 opt-in 的 Effect 规则组
├── skills/install-anti-slop/
│   ├── SKILL.md                       # 安装/配置/验证契约
│   ├── scripts/install.mjs            # vendor copy，默认拒绝覆盖
│   └── assets/anti-slop/              # 与 src 同步的 vendored 副本
├── scripts/sync-skill-assets.mjs      # 检测 src 与 skill asset drift
├── .github/workflows/ci.yml           # Node 24 + pnpm install/check
├── package.json / pnpm-lock.yaml
└── LICENSE
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/index.ts` | 插件入口 | 用 `eslintCompatPlugin` 注册 15 条 generic rules |
| `src/rules/no-widen-then-assert.ts` | 跨局部 flow 检查 | 跟踪 immutable const、宽类型与后续窄断言；限制在同 function boundary |
| `src/rules/require-safety-comment-for-type-assertion.ts` | 断言证据门 | 非 `as const` 断言必须有邻近 `SAFETY:` 或配置 marker 且理由非空 |
| `src/rules/no-module-mocking.ts` | 测试架构约束 | 识别 global/imported `vi`/`jest` 的 mock/doMock/unstable_mockModule |
| `src/shared/type-alias-resolution.ts` | same-file 类型解析 | 建 lexical alias environment，处理 shadowing、泛型参数替换与递归匹配 |
| `skills/install-anti-slop/scripts/install.mjs` | vendoring | 默认复制到 `tools/oxlint/anti-slop`，目标存在则拒绝覆盖，`--force` 才替换 |
| `scripts/sync-skill-assets.mjs` | 漂移检查 | CI 确认 canonical `src/` 与分发 asset 一致 |

#### ⭐ 源码精读

**函数/构造 1：plugin entry 显式列出规则，framework policy 不混入 generic 默认。**

```ts
const antiSlopPlugin = eslintCompatPlugin({
  meta: { name: "anti-slop" },
  rules: {
    "no-chained-type-assertions": noChainedTypeAssertionsRule,
    "no-known-value-widening": noKnownValueWideningRule,
    "no-module-mocking": noModuleMockingRule,
    "no-widen-then-assert": noWidenThenAssertRule,
    "require-safety-comment-for-type-assertion": requireSafetyCommentForTypeAssertionRule,
    // 其余 generic rules 省略
  },
});
```

逻辑摘要：规则 registry 是静态、可审计的；Effect policy 在独立入口。迁移时可逐条启用，而不必接受作者全部 taste。

**函数 2：`noWidenThenAssertRule` 只报告同边界、声明后发生、证据确实被宽化再恢复的 flow。**

```ts
export const noWidenThenAssertRule = defineRule({
  createOnce(context) {
    let scopes = [];
    const checkAssertion = (node) => {
      const expression = assertedExpression(node);
      if (expression.type !== "Identifier") return;
      const variable = resolvedVariableForIdentifier(scopes, expression);
      if (variable === null) return;
      const widened = widenedBinding(variable, scopes);
      if (
        widened === null ||
        node.start <= widened.declaredAt ||
        functionBoundary(node) !== widened.boundary ||
        !assertionIsNarrower(context.sourceCode.text, widened.broadKind,
          widened.evidence, node.typeAnnotation)
      ) return;
      context.report({ node, messageId: "widenThenAssert" });
    };
    return { Program() { scopes = context.sourceCode.scopeManager.scopes; },
      TSAsExpression: checkAssertion, TSTypeAssertion: checkAssertion };
  },
});
```

逻辑摘要：不是看到 `as` 就报；它先解析 identifier 对应变量，再要求 immutable local binding 确实从已知值宽化，并在同 function boundary 内断言回窄类型。这降低跨闭包/可变状态误判，但也明确放弃跨文件和复杂数据流。

**函数 3：安全说明不是关键词装饰，marker 后必须有冒号和非空内容。**

```ts
function markerPattern(markers: readonly string[]): RegExp {
  const alternation = markers
    .map((marker) => marker.replaceAll(/[.*+?^${}()|[\]\\]/gu, String.raw`\$&`))
    .join("|");
  return new RegExp(
    String.raw`(?:^|[^\p{L}\p{N}_])(?:${alternation})\s*:\s*\S`,
    "u",
  );
}
```

逻辑摘要：配置 marker 会先做 regex escaping，随后要求词边界、冒号以及至少一个非空字符。它只能证明“写了理由”，不能证明 invariant 为真，因此仍需 schema/parser/test 或 reviewer 验证。

**函数 4：module mock 检查区分真实 test framework object 与局部同名变量。**

```ts
function moduleMockCall(sourceCode: SourceCode, callee: ESTree.Expression): boolean {
  if (!("property" in callee) || !("object" in callee) || !("computed" in callee)) return false;
  if (!isTestFrameworkObject(sourceCode, callee.object)) return false;
  const property = callee.property;
  const method = callee.computed
    ? property.type === "Literal" ? property.value : null
    : property.type === "Identifier" ? property.name : null;
  return method !== null && moduleMockMethods.has(method);
}
```

逻辑摘要：先通过 global reference 或 `vitest` / `@jest/globals` import binding 确认对象，再处理点访问和计算属性。目标不是语法洁癖，而是强迫生产代码暴露真实 dependency seam。

**函数 5：installer 默认拒绝覆盖已有 vendored copy。**

```js
if (existsSync(target) && !force) {
  console.error(`Refusing to overwrite ${target}. Re-run with --force only after reviewing the existing files.`);
  process.exit(1);
}
mkdirSync(dirname(target), { recursive: true });
cpSync(source, target, { recursive: true, force });
```

逻辑摘要：vendor 模式把升级责任交给目标仓库，同时以“存在即拒绝”阻止静默覆盖本地定制。边界是 `--force` 仍是整树替换；没有 ownership journal、backup 或三方 merge。

#### 依赖分析与供应链风险

`package.json` 为 `private: true`，没有官方 npm package，README 明确要求 vendor。精确依赖：运行依赖 `@oxlint/plugins 1.78.0`；开发依赖 `oxlint 1.78.0`、`tsx 4.23.12`、`typescript 7.0.2`、`@types/node 26.2.0`；package manager 固定 `pnpm 10.33.0`。

真实检查：

- 锁文件安装成功；`pnpm audit` 与 `pnpm audit --prod` 均返回 **No known vulnerabilities found**。这只覆盖 npm advisory 数据库与当前锁文件。
- `pnpm lint`、`pnpm typecheck`、`pnpm check:skill-assets` 均 exit 0；asset drift 检查明确输出 `Skill assets match src.`。
- 完整 `pnpm check` **未通过**：RuleTester 启动时 `@oxlint/plugins` 尝试分配 `ARRAY_BUFFER_SIZE`，真实报错 `RangeError: Array buffer allocation failed`。依赖源码注释说明 raw-transfer buffer 会预留约 **6 GiB virtual memory**。在本机 3.8 GiB RAM / 1 GiB swap 的 WSL 环境中，Node 22.14 与临时 Node 24.20 均复现；因此本次不能声称规则 tests 通过。固定提交的 GitHub Actions CI 为 success，只是上游环境证据，不能替代本机通过。
- pnpm 安装提示 `esbuild@0.28.2` build script 被忽略；本次 lint/typecheck 仍成功，但这不是完整安装生命周期验证。

#### 可复用经验

- 当 Agent 生成 TypeScript 后容易“先宽化再断言”时，应优先使用**词法 scope + immutable local flow** 的确定性检查，而不是只在 prompt 里禁止 `as unknown as`；边界是无 type checker 的 AST 规则看不到跨文件语义。
- 当类型断言确实无法避免时，应优先要求**紧邻、非空、可配置 marker 的 invariant 说明**，再由测试/解析器验证，因为裸断言没有审计线索；边界是注释存在不证明注释真实。
- 当测试依赖可替换时，应优先通过**真实 interface/service seam** 注入实现，而不是 module mock，因为 module mock 会隐藏模块初始化和依赖耦合；边界是遗留代码迁移成本高，不能一次性全仓强制。
- 当团队引入强 opinionated lint rules 时，应优先**逐规则观察 → warning → error**，并记录 baseline/误报/例外，而不是整体照搬作者 taste；边界是规则例外必须有 owner 与到期复审。
- 当本地 checker 因运行时资源或工具兼容失败时，应优先返回 **blocked/failed** 并保留真实错误，因为 lint/typecheck 绿色和上游 CI 不能替代规则 tests；边界是修复环境后仍需重新执行同一固定提交。

#### 可尝试实验（30 分钟）

在 `runtime/hermes/github-learning-poc/evidence-preserving-ts-gate/` 建一个 throwaway TypeScript fixture，只复制三类思想、不复制上游源码：`double assertion`、`known -> unknown -> assert`、`assertion without rationale`。先用当前项目自身 lint 配置观察 baseline，再设计 agent-neutral JSON finding schema：`rule_id / path / range / evidence / limitation / terminal`。由于上游 RuleTester 在本机 blocked，实验第一阶段只验证 contract 与 fixture 期望，不宣称替代 Oxlint 实现。

#### 风险边界

- **License**：GitHub API 与 `LICENSE` 均为 MIT；vendoring 会把后续更新、NOTICE/依赖审查和本地 fork 维护责任带入目标仓库。
- **维护活跃度**：固定 tag 日期为 2026-08-31，最近提交与 CI 活跃；但版本仅 `0.1.2`，API surface 与规则口径仍可能快速变化。
- **安全/供应链**：npm audit 0 findings 不证明 Oxlint native binary、安装脚本、未知漏洞或 vendored 后续差异安全；installer 有文件写入，`--force` 可覆盖整棵目标目录。
- **资源风险**：RuleTester 所用 Oxlint JS plugin path 会预留约 6 GiB virtual buffer，本机真实失败；低内存/受限虚拟地址环境不适合直接设为强制 gate，问题根因和上游支持边界仍待核验。
- **局限/不适用**：不使用 TypeScript checker，不解析 imported types/跨文件 call signature；许多规则体现作者偏好，不是普适标准；对 module mocking 的全面禁止不适合没有可替换 seam 的遗留系统。
- **执行边界**：今日不运行 installer 写入任何真实项目，不改 Hermes/OpenClaw 配置，不把这些规则直接升级为全局 error。

#### ⭐ Skill 升格判断

**需二次验证。** “证据保留型代码 gate”可迁移，但上游完整规则集不应直接升格：一是规则主观性强，二是本机 RuleTester blocked，三是 shared hub 已有 verification-first 候选，需要先去重。若实验证明三条窄规则对 Hermes 生成代码有效，应优先更新现有 verification/quality skill，而不是复制整个上游 skill。

#### ⭐ Hermes / shared hub 落地路径

- Hermes POC：`runtime/hermes/github-learning-poc/evidence-preserving-ts-gate/`
- 第一版只生成 findings，不自动改源码；Hermes 审计读取 stable `rule_id`、source range、evidence 和 checker terminal。
- 若二次验证通过：在现有 verification skill 的 `references/` 增加“evidence-preserving TypeScript gate”窄文档，deterministic checker 放该 skill 的 `scripts/`；只有确无相近能力才考虑新目录。
- 如最终成为 shared 能力，必须更新 `capabilities/manifests/shared-skills.yaml` 的 `scope/reference_policy/future_agent_readable`，并为各 host adapter 做 loader acceptance fixture；不能把 WSL 路径、当前 Node 路径或 runtime repo clone 写进 skill。
- 未来其他 agent 只消费 shared finding contract；是否启用、severity、目标 repo 与修改权限由各自 host 决定。当前未调用、未配置 OpenClaw。

## 经验沉淀

1. 当高权 Agent 摄取复杂二进制文档时，应优先让确定性 host 输出 `identity + coverage + typed terminal + artifact hash`，再把 Markdown 交给模型；边界是 hash 不证明提取语义完整。
2. 当多个格式最终服务同一 Agent 上下文时，应优先使用 canonical model 与单一 projection，避免各 parser 各自形成转义/脚注/表格语义；边界是格式特有信息必须显式声明损失。
3. 当检测器会触发 OCR、模型或网络 fallback 时，应优先执行 bounded verifier 并要求显式授权，因为 classifier 命中不是网络出域许可；边界是整文档上传还需隐私、费用和 retention 审查。
4. 当静态规则能表达“丢失证据再重建”的坏模式时，应优先把规则写成 fixture-tested deterministic gate，而不是反复扩充 prompt；边界是 AST checker 的 coverage 与误报必须公开。
5. 当 assertion、override 或危险例外不可避免时，应优先记录具体 invariant、owner、source location 与验证方式，而不是用通用 `SAFETY` 口号骗过 gate；边界是说明文本仍需独立证据。
6. 当第三方 checker 安装、lint、typecheck 成功但 tests 因资源失败时，应优先把整体状态标为 blocked/partial，不得把部分绿色投影成完成；边界是上游 CI 只能作为补充证据。
7. 当候选与已有 shared skill/POC 重叠时，应优先更新既有 class-level contract 并去重，而不是按每日热门项目新增 skill；边界是新机制确有独立触发条件和验证面时才单独升格。

## Hermes / shared hub 综合落地建议

本日只产生 raw 报告、runtime 卡片和候选，不写 curated active fact，不修改 config/provider/model/cron/secret。

建议统一为一个窄的“输入证据质量”链：

```text
untrusted input/code
  -> deterministic identity/parser/linter
  -> {terminal, coverage, findings, limitations, artifact_hash}
  -> Hermes review
  -> candidate promotion gate
  -> 人工/总控审核后，才允许更新 existing shared skill 或 curated fact
```

- 文档 lane 复用已有：`runtime/hermes/github-learning-poc/document-ingestion-receipt/`
- TypeScript lane 新建候选：`runtime/hermes/github-learning-poc/evidence-preserving-ts-gate/`
- 去重目标：`capabilities/skills/` 内现有 verification-first / shared governance / document-reading 类能力（具体归并前再通过 manifest 搜索确认）
- 任何 shared 写入前必须完成：真实 Hermes adapter test、scope/path portability、blocked/partial terminal、无 secret fixture、manifest 更新与审查。

## 明日继续

1. 最小动作：在低资源容器或调整 WSL memory 后，固定 `anti-slop@e8c4880` 复跑单个 RuleTester，确认 6 GiB virtual buffer 是环境约束、Oxlint 1.78 设计限制还是可配置路径；未跑通前保持 blocked。
2. 给 `document-ingestion-receipt` 增加四个公开 fixture，特别验证 scanned PDF 不会被投影成 completed，并记录 `network_used=false`。
3. 查询 anydoc 对 `ttf-parser` unmaintained 与 `chacha20` yanked 依赖的上游处置进度；只记录 issue/commit 证据，不自动升级依赖。

## 候选反哺

### Candidate Facts

- [ ] topic: complex-document ingestion 应分离 detected format、coverage、terminal 与 output hash | evidence: `anydoc` 固定提交 `src/lib.rs`、`src/formats/pdf.rs`、本机 296 个测试通过且 scanned/OCR 为 typed error | 建议: update（与既有 document-ingestion candidate 去重） | 安全级别: medium
- [ ] topic: deterministic checker 的“部分绿色”不能覆盖测试运行 blocked | evidence: `anti-slop` lint/typecheck/asset drift 通过，但 Node 22/24 RuleTester 均 `Array buffer allocation failed` | 建议: update verification-first fact candidate | 安全级别: low

### Candidate Skills / Workflow

- [ ] 名称: document-ingestion-receipt 增量验证 | 可复用场景: Hermes/未来 agent 摄取 PDF/DOCX/ZIP | 是否建议 shared: no（当前阶段） | 原因: 已有候选，先补 coverage/OCR/network/resource fixtures，避免重复 skill
- [ ] 名称: evidence-preserving TypeScript gate | 可复用场景: Agent 生成 TypeScript 后拒绝双重断言、证据宽化和无理由断言 | 是否建议 shared: no（当前阶段） | 原因: 上游规则主观、本机测试 blocked，先做三个窄 fixture 并与 verification skill 去重

### Candidate Open Questions

- [ ] 问题: Oxlint 1.78 JS plugin RuleTester 的约 6 GiB virtual buffer 在 WSL/容器中的官方最低资源与可配置路径是什么？ | reason: adaptation | priority: high
- [ ] 问题: anydoc 的 PDF direct path 如何与统一 Document/asset/coverage contract 对齐？ | reason: gap | priority: medium
- [ ] 问题: `ttf-parser` unmaintained 与 `chacha20` yanked 经 pdf-inspector/lopdf 引入，后续替换版本和实际可达性如何？ | reason: stale/security | priority: medium

### 不应自动落地

- 不自动安装 `npx skills add firecrawl/anydoc` 或 `dmmulroy/anti-slop`。
- 不自动启用 hosted OCR，不上传任何私有文档，不写入 API key。
- 不把 anti-slop 全规则直接设为项目级 error，不运行 `--force` 覆盖 vendored 目录。
- 不因 npm/cargo audit 没有 vulnerability 就宣称“无安全风险”；warning、未覆盖生态与未知漏洞仍存在。
- 不直接写 curated active fact，不修改 Hermes/OpenClaw 配置、模型、provider、cron 或 secret。
