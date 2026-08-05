# 2026-08-05 GitHub 热门项目学习日报

> 执行器：Hermes（本任务未调用 OpenClaw）  
> 研究时间：2026-08-05T07:30–07:42+08:00；GitHub API 元数据最终汇总时间约 2026-08-04T23:41:41Z。  
> 发现来源：真实抓取 [`github.com/trending?since=daily`](https://github.com/trending?since=daily)，并用 GitHub Search API 查询近期新仓库；速览元数据逐仓通过 `gh api repos/{owner}/{repo}` 复核。  
> 固定源码快照：`firecrawl/pdf-inspector@bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd`；`livekit/agents@04d00cbd311fa980f5276b7eb29aa099f2ea16ff`。  
> 证据目录：`runtime/hermes/github-hot-project-learning/api/2026-08-05/`；clone：`runtime/hermes/github-hot-project-learning/repos/`。  
> 数据边界：Stars、forks、updated/pushed 是动态值；GitHub Repository/License API 的仓库级 license 不能替代依赖、模型、数据、服务和发行制品审查。

## 今日结论

今天的主线是：**高成本或实时流水线不能把一次粗分类、单一 provider 或一个“成功”布尔值当成真相；应把输入先变成带原因和能力声明的分流结果，再由阶段化 pipeline、局部 fallback、终态与可观测证据完成闭环。** `pdf-inspector` 用 `PdfType + confidence + pages_needing_ocr + reason` 把 PDF 逐页路由到本地解析或 OCR；`livekit/agents` 用 capability-aware adapter、session lifecycle、provider fallback 与进程级资源边界管理实时 Agent。对 Hermes/shared hub 最可迁移的是窄契约：**reason-coded routing + stage capability envelope + fallback attempt receipt**，不是安装完整 PDF/voice 产品。

## 证据与执行摘要

- Trending HTML 真实下载到 `runtime/hermes/github-hot-project-learning/trending-2026-08-05.html`，大小 **628,705 bytes**；解析到 18 个仓库，包括 `firecrawl/pdf-inspector`、`livekit/agents`、`esengine/DeepSeek-Reasonix`、`TencentCloud/TencentDB-Agent-Memory`、`uber/ADR` 等。
- GitHub Search API 真实查询 `created:>=2026-07-20 stars:>20`，补充发现 `andrewyng/openworker`、`yc-software/qm`、`kvcache-ai/AgentENV`、`vercel-labs/scriptc` 等近期项目；它只是发现流，今日深读仍选择 Trending 中与文档处理、实时 Agent runtime 更相关且未在昨日深读的两个项目。
- 两个深读仓库均用 `git clone --depth 1` 获取；固定快照 tracked paths 分别为 **281**（pdf-inspector）和 **1,289**（livekit/agents）；研究/测试后两个 tracked worktree 均保持 clean。
- 元数据、License、commits、releases、issues、pulls、tags 的 API JSON 保存到 `runtime/hermes/github-hot-project-learning/api/2026-08-05/`。
- `pdf-inspector`：README、SECURITY、issues/PR、Cargo manifest 和关键 Rust 源码已交叉核验；本机没有 `cargo/rustc`，`cargo test --lib` 真实返回 **exit 127 / command not found**，所以 build、test、解析质量、资源预算与恶意 PDF 行为均标为**待核验**。
- `livekit/agents`：README、最新 GitHub Release、issues/PR、`MODEL_LICENSE`、core pyproject、session/STT fallback/worker 源码和测试已交叉核验。先做 Python core `compileall`，结果 **PASS**；随后用 `uv run --isolated --with-editable ./livekit-agents ... pytest` 跑 `tests/test_stt_fallback.py` 与 `tests/test_stt_prewarm.py`，真实结果 **8 passed in 0.22s**。没有连接 LiveKit、没有录音、没有调用 STT/LLM/TTS provider。
- `uv` 定向测试命令因仓库 workspace/source 配置构建大量本地 plugin package，并安装 **302 packages**；这反而揭示了“想测窄 core、解析成宽 workspace”的供应链与 CI 资源风险，不能把 8 个测试外推为整个 runtime 已验证。
- 两仓 Dependabot alerts endpoint 对当前 token 均返回 **HTTP 403 / not authorized**；不能写成“没有漏洞”。
- 未修改 Hermes/OpenClaw 配置、provider、模型、auth、env、cron；未把候选直接写入 curated 或 shared skills。

## 项目速览

下表 Stars/Forks/Language/License/Updated/Pushed 均来自 2026-08-04T23:41Z 左右的 GitHub Repository API。`open_issues_count` 未列出，因为 GitHub 该字段包含 PR，不能解释为缺陷数。

| 项目 | Stars | Forks | Language | License（GitHub API） | Updated / Pushed (UTC) | 今日判断 |
|---|---:|---:|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 266,448 | 23,826 | Shell | MIT | 2026-08-04T23:25:16 / 2026-08-04T22:02:12 | 高热 Agent skill 方法论；已有大量相邻治理能力，避免追热重复升格 |
| [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | 30,746 | 1,980 | Go | MIT | 2026-08-04T23:25:38 / 2026-08-04T21:55:01 | prefix-cache stability 的长驻 coding Agent；列入后续性能复现实验 |
| [browser-use/video-use](https://github.com/browser-use/video-use) | 19,293 | 2,404 | Python | MIT | 2026-08-04T23:31:06 / 2026-07-01T00:33:52 | 视频编辑 Agent；pushed 时间较旧，执行外部媒体工具风险较高 |
| [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 17,799 | 2,446 | PowerShell | MIT | 2026-08-04T23:30:10 / 2026-08-04T02:46:28 | 逆向/渗透 skill router；高权工具链，不在无人值守 cron 中运行 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | 13,522 | 1,271 | TypeScript | **NOASSERTION** | 2026-08-04T23:31:49 / 2026-08-03T12:49:18 | 与 shared hub 相关，但 API 未识别 license，禁止复制源码 |
| [livekit/agents](https://github.com/livekit/agents) | **12,387** | 3,477 | Python | **Apache-2.0** | 2026-08-04T23:31:10 / 2026-08-04T22:53:45 | **深读：实时 session lifecycle、capability adapter、局部 fallback** |
| [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector) | **9,944** | 654 | Rust | **MIT** | 2026-08-04T23:31:26 / 2026-08-04T23:22:25 | **深读：逐页分类、reason-coded OCR routing、阶段化提取** |
| [uber/ADR](https://github.com/uber/ADR) | 663 | 68 | Python | Apache-2.0 | 2026-08-04T23:18:19 / 2026-08-03T18:11:16 | Agent observability/security 候选；后续先核验 threat model 与运行权限 |

说明：Stars 不是成熟度、安全性或真实性证明；`updated_at` 可能由 issue/元数据活动推动，`pushed_at` 也可能来自非默认分支。源码结论均绑定固定 commit，而非浮动 `main`。

## 深读项目

### 1. firecrawl/pdf-inspector

- **URL**：https://github.com/firecrawl/pdf-inspector
- **Stars / Forks / Language / License（GitHub API）**：**9,944 / 654 / Rust / MIT**。
- **创建 / updated / pushed**：2026-02-06T19:44:47Z / 2026-08-04T23:31:26Z / 2026-08-04T23:22:25Z。
- **固定 commit**：[`bfd6c3eabbb0`](https://github.com/firecrawl/pdf-inspector/commit/bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd)，commit time 2026-08-04T23:22:25Z，修复 PDF string 中 escape-aware comment stripping。
- GitHub Releases API 返回空数组，但 tags API 有 `v0.7.0` 等 18 个 tag；固定 main 的 `Cargo.toml` version 为 `0.1.7`，README benchmark 又写 `pdf-inspector 0.2.6`。这些版本面不一致，不能把 main、crate、binding 与 tag 当成同一制品。

#### 一句话判断

`pdf-inspector` 值得学的不是“Rust 比 OCR 快”，而是它把 **便宜检测、逐页 OCR reason、位置化提取、layout/table 分析、Markdown projection**拆成阶段，并在 encoding/garbage/layout 不可靠时显式降级；这比对所有 PDF 一刀切 OCR 或把空 Markdown 当成功更适合作为 Agent ingestion 前置路由。

#### 解决的问题：替代了什么旧做法

1. 替代“所有 PDF 都送 OCR”的高延迟/高成本做法：先采样 content stream 的 text/image/path/font signals，再决定 TextBased/Scanned/ImageBased/Mixed。
2. 替代“整份文档只有一个 scanned 布尔值”的做法：输出 `pages_needing_ocr` 和每页 reason code，让混合 PDF 只把问题页交给 OCR。
3. 替代“检测和提取各 parse 一次”的重复 I/O：`process_pdf_with_options` 单次 load 后共享 `Document`。
4. 替代“有 Tj/TJ 就是可用文本”的过度乐观：还检查 unique chars、image domination、Identity-H/Type3/ToUnicode、vector text 和垃圾文本。
5. 替代“表格/分栏只有一个 heuristic”的脆弱做法：layout complexity 依序尝试 rect、line、heuristic table detectors，再做 column detection。
6. 替代“解析失败就沉默输出空文本”的做法：解析、加密、invalid structure、not-a-PDF 有 typed error；但 Mixed extraction 仍有 non-fatal 路径，因此消费者必须结合 reason/coverage 检查。

边界：这些判断是启发式，不是内容完整性证明。README 自报 benchmark 未在本机复现；issue #251/#252 显示 detect、extract、Markdown 和 needs_ocr 之间仍可能冲突，issue #260 也说明恢复文本后 table/column order 尚在演进。

#### 架构 / 实现与数据流

```text
PDF path / bytes
      │ validate header + load/decrypt/limited repair
      ▼
 shared lopdf::Document
      ├─ detector::detect_from_document
      │    └─ PdfType + confidence + page OCR reasons
      └─ extractor::extract_positioned_text...
           ├─ content_stream / fonts / ToUnicode / XObjects / links
           ├─ TextItem + PdfRect + PdfLine
           ├─ text_quality + layout complexity
           │    ├─ table: rect → line → heuristic
           │    └─ columns / reading order
           └─ markdown projection
                └─ PdfProcessResult / per-page / region APIs
                         │
                         ├─ trusted text lane
                         └─ OCR fallback lane（由调用方执行）
```

主路径先验证并加载文档，detector 用采样页信号得到分类和 reasons；只有非 Scanned/ImageBased 才继续位置化提取。Mixed 文档若普通提取为空/垃圾，会尝试 invisible text layer。随后全局 font stats、text quality、table/column complexity 和 tagged structure 共同生成 Markdown；如果 text-based 结果仍是垃圾，则撤销 Markdown 并把页面推向 OCR。

#### Repo tree 摘要

```text
pdf-inspector/                         # fixed commit tracked paths: 281
├── README.md / SECURITY.md / LICENSE # 产品入口、漏洞范围、MIT
├── Cargo.toml                        # crate/binaries/features；仓库没有 Cargo.lock
├── docs/ / examples/                 # Rust/Python/benchmark/debugging
├── external/bcmaps/                  # bundled CMaps，随 crate 发布
├── src/
│   ├── lib.rs                        # public API、single-load pipeline、quality gate
│   ├── detector.rs                   # PdfType、sampling、OCR reason
│   ├── extractor/                    # content/fonts/layout/links/XObjects
│   ├── tables/                       # rect/line/heuristic/grid/format
│   ├── markdown/                     # analysis/classify/convert/postprocess
│   ├── tounicode.rs / text_quality.rs# 字体解码与垃圾文本识别
│   └── bin/                          # pdf2md / detect-pdf / dump_ops
├── napi/ / wasm/ / src/python.rs     # Node、browser WASM、Python binding
└── tests/                            # integration fixtures；大量 unit tests 内联在模块
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `src/detector.rs` | 分类与 OCR 路由 | 采样策略、text/image/font/vector signals、confidence、逐页 reasons |
| `src/lib.rs` | composition root | single-load、typed result、Mixed/invisible fallback、quality/layout/Markdown gate |
| `src/extractor/mod.rs` | 位置化提取编排 | per-page extraction、context-only failure policy、clip、font cache、links/forms |
| `src/extractor/content_stream.rs` | PDF operator state machine | Tj/TJ/Td/Tm/q/Q、comment/string parsing；固定 commit 修复 escape bug |
| `src/tables/*` | 表格检测 | rect/line/heuristic 三种 detector 与 grid/cell formatting |
| `src/markdown/*` | semantic projection | font stats、heading/list/code/table、pre/post-process |
| `Cargo.toml` | 依赖与发布面 | Rust/Python/native/WASM 条件依赖和 explicit crate include allowlist |
| `SECURITY.md` | threat scope | crafted PDF 的 panic/OOB/UB/DoS 属于 in-scope |

#### 源码精读（固定 commit）

**代码块 1：分类不是只看 Tj/TJ，而是组合文本、图片、字体和采样比例**  
来源：[`src/detector.rs#L184-L334`](https://github.com/firecrawl/pdf-inspector/blob/bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd/src/detector.rs#L184-L334)

```rust
pub(crate) fn detect_from_document(
    doc: &Document,
    page_count: u32,
    config: &DetectionConfig,
) -> Result<PdfTypeResult, PdfError> {
    let pages = doc.get_pages();
    let (sample_indices, allow_early_exit) = match &config.strategy {
        ScanStrategy::EarlyExit => ((1..=total_pages).collect(), true),
        ScanStrategy::Full => ((1..=total_pages).collect(), false),
        ScanStrategy::Sample(max_pages) =>
            (distribute_pages((*max_pages).min(total_pages), total_pages), false),
        ScanStrategy::Pages(pages) => (validated_pages(pages, total_pages), false),
    };

    // A page counts as text only after operator count, image domination,
    // character diversity, vector-text and Type3 checks.
    if analysis.text_operator_count >= effective_min_ops
        && !is_image_dominated
        && analysis.unique_text_chars >= 5
        && !analysis.has_vector_text
        && !analysis.has_only_type3_fonts
    {
        pages_with_text += 1;
    }
    // ratio + image/vector/template evidence selects TextBased/Scanned/Mixed.
}
```

逻辑：默认配置实际是 `Sample(8)`（不是 detector enum 注释中的 EarlyExit），避免 image-only cover 误判整份文档。样本页只有同时满足最低 op、非 image-dominated、字符多样性、非 vector text、非 Type3-only 才计为 text page。边界是采样会漏掉未采样页的布局类别，阈值又依赖经验语料；issue #247/#254 正在要求更明确的 threshold/routing 文档。

**代码块 2：single-load pipeline 根据 typed stage 决定早退或继续**  
来源：[`src/lib.rs#L3592-L3687`](https://github.com/firecrawl/pdf-inspector/blob/bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd/src/lib.rs#L3592-L3687)

```rust
fn process_document(
    doc: Document,
    page_count: u32,
    options: PdfOptions,
    start: ProcessingTimer,
) -> Result<PdfProcessResult, PdfError> {
    let detection = detector::detect_from_document(&doc, page_count, &options.detection)?;

    if options.mode == ProcessMode::DetectOnly {
        return Ok(detection_only_result(detection, start));
    }
    if matches!(detection.pdf_type, PdfType::Scanned | PdfType::ImageBased) {
        return Ok(no_markdown_result(detection, start));
    }

    let font_cmaps = FontCMaps::from_doc(&doc);
    let result = extractor::extract_positioned_text_with_folio_context(
        &doc, &font_cmaps, options.page_filter.as_ref()
    );
    // Mixed + empty/garbage normal layer gets one invisible-text retry.
    // Later quality gates may still suppress Markdown and require OCR.
}
```

逻辑：stage 不是“每次重新打开文件”的独立脚本，而是在一个 parsed document 上推进；DetectOnly 和明显 image lane 早退，其他 lane 才承担 font/layout/Markdown 成本。Mixed fallback 只改变提取策略，不自动调用外部 OCR。边界是 `process_document` 本身非常大，分类、repair、quality、layout、projection 语义集中在同文件；版本快速变化时容易产生 cross-stage drift。

**代码块 3：逐页结果把不可靠文本清空，而不是让调用方误用**  
来源：[`src/lib.rs#L457-L605`](https://github.com/firecrawl/pdf-inspector/blob/bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd/src/lib.rs#L457-L605)

```rust
pub fn extract_pages_markdown_mem(
    buffer: &[u8],
    pages: Option<&[u32]>,
) -> Result<PagesExtractionResult, PdfError> {
    // Extract document context, then partition per page.
    for &page_0idx in pages_slice {
        let md = if has_text_quality_issue {
            String::new()
        } else {
            markdown::to_markdown_from_items_with_rects_and_lines(/* ... */)
        };
        let needs_ocr = ocr_reason.is_some()
            || md.trim().is_empty()
            || has_gid
            || is_garbage_text(&md);
        results.push(PageMarkdown {
            page: page_0idx,
            markdown: if needs_ocr { String::new() } else { md },
            needs_ocr,
            ocr_reason,
        });
    }
    Ok(PagesExtractionResult { pages: results, /* layout + reasons */ })
}
```

逻辑：调用方拿到的不是“可能坏但看起来像文本”的 Markdown；一旦 quality/reason/GID/empty/garbage 任一触发，页面输出清空并显式 `needs_ocr`。这很适合 ingestion 的 fail-loud routing。边界是 issue #252 报告 plain text PDF 可能被此 API 全部标 OCR，说明 conservative gate 自己也可能 false positive；必须保留原始 PDF、版本和可回放 fixture。

**代码块 4：table/layout 采用 ordered detectors，而非混在一个不可解释分数里**  
来源：[`src/lib.rs#L5635-L5741`](https://github.com/firecrawl/pdf-inspector/blob/bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd/src/lib.rs#L5635-L5741)

```rust
fn compute_layout_complexity(
    items: &[TextItem], column_items: &[TextItem],
    rects: &[PdfRect], lines: &[PdfLine],
) -> LayoutComplexity {
    for page in seen_pages {
        for band in split_side_by_side(page) {
            let (rect_tables, _) = tables::detect_tables_from_rects(/*...*/);
            if has_data_table(&rect_tables) { found_table = true; break; }
            let line_tables = tables::detect_tables_from_lines(/*...*/);
            if has_data_table(&line_tables) { found_table = true; break; }
            let heuristic_tables = tables::detect_tables_with_page_width(/*...*/);
            if has_data_table(&heuristic_tables) { found_table = true; break; }
        }
    }
    // Table knowledge is passed to column detection to reduce false columns.
}
```

逻辑：强证据 detector 先于弱 heuristic，并先按 side-by-side band 缩小作用域；TOC 与 data table 分开，table 结果还影响 column detector。可迁移点是“ordered evidence lanes + reason/provenance”，而不是 PDF 专用阈值。边界是 first-valid-wins 会隐藏其他 detector 分歧；若用于治理，应记录每 lane attempted/result，而不是只保留 winner。

#### 依赖分析与供应链风险

- root `Cargo.toml` 有 7 个基础 direct dependency：`pyo3`（optional）、`thiserror`、`log`、`regex`、`once_cell`、`unicode-normalization`、`ttf-parser`；native 条件再加 `lopdf/rayon/env_logger`，WASM 条件使用另一组 `lopdf` feature 加 `include_dir`。
- 仓库固定 commit **没有 `Cargo.lock`**。作为 library 这并不异常，但无人值守从源码构建时，semver 解析可能随 registry 变化；生产复现应由消费者 lockfile、`cargo vendor`/checksum 或发行 provenance 固定。
- `lopdf` 处理攻击者可控 PDF，是最关键 parser dependency；SECURITY 明确 crafted PDF 的 panic/OOB/UB/DoS 在 scope。Rust 内存安全降低部分风险，但压缩炸弹、巨大对象图、递归、CPU/内存放大仍需外部预算。
- `external/bcmaps/` 随 crate include allowlist 发布，Python/Node/WASM 又有各自打包链；repo MIT 不能替代 npm/PyPI/crates artifact、binding toolchain 与 bundled data 的 provenance 审核。
- README 说“single dependency on lopdf”与实际 Cargo manifest 的多个 direct dependencies 不一致；应以 manifest 为准。
- Dependabot API 403，且本机无 Cargo，未执行 `cargo audit`/build/test；依赖漏洞状态为**待核验**。

#### README / SECURITY / issues / commits 交叉核验

- README 的 detector→extractor→tables/layout→markdown 架构能在实际目录和 `process_document` 找到；single-load 也由 `process_pdf_with_options` 和 `process_document` 证实。
- SECURITY 明确 crafted PDF 的 memory safety 与 DoS 属于 in-scope，但没有给出文件大小、页数、对象数、解压量、递归或 wall-clock hard limits；“快”不等于抗恶意输入。
- 固定 commit 对应 closed PR #259 / issue #258，说明一个 escaped `\)` 可让 `%` 被误当 top-level comment并静默截断文本；这直接证明 parser 的“输出非空”不能代表内容完整。
- open issue [#251](https://github.com/firecrawl/pdf-inspector/issues/251) 报告 `process_pdf_bytes().markdown` 丢失 `extract_text_bytes()` 可见内容；[#252](https://github.com/firecrawl/pdf-inspector/issues/252) 报告 plain text PDF 被全部标 OCR；[#260](https://github.com/firecrawl/pdf-inspector/issues/260) 关注 text recovery 后 table/column order。状态只反映查询时 API，未复现这些样本。
- README benchmark 提供外部 reproducible branch，但本机无 Cargo、未下载 200-PDF corpus、未复现实验环境；0.875/0.470s 等上游数字不作为本报告运行结论。

#### 真实测试结果

```text
$ command -v cargo; command -v rustc
# 均无输出

$ cargo test --lib
/usr/bin/bash: cargo: command not found
cargo_test_exit=127

$ git rev-parse HEAD
bfd6c3eabbb075e8b2c0c252fdfdbb49f91ea7fd
$ git ls-files | wc -l
281
```

准确结论：源码已真实 clone 和静态精读，但当前环境未编译、未运行任何 Rust unit/integration test，也未喂入 PDF。分类准确率、Markdown 完整性、恶意输入资源预算、Python/Node/WASM binding、tag/crate 版本行为全部待核验。

#### 可复用经验

- 当输入可走便宜本地解析或昂贵 OCR/provider 两条 lane 时，应优先输出 `classification + confidence + per-unit reason` 再路由，因为全局布尔值无法表达 mixed/partial；边界是阈值需版本化且必须用真实 corpus 回归。
- 当 parser 可能产生非空但错误文本时，应优先把 encoding/garbage/coverage 检查放在 projection 前，并让不可信 unit 显式 blocked/fallback，因为“有输出”不等于“完整”；边界是 conservative gate 也会 false positive。
- 当多个 detector 从强证据到弱启发式竞争时，应优先采用 ordered lanes 并保留 attempted/result/provenance，因为单一融合分数难以解释路由；边界是 first-valid-wins 仍要记录被跳过/冲突的 lane。
- 当同一输入经历检测、提取、布局、格式化时，应优先单次 canonical load 后传递 typed stage output，因为重复 parse 既浪费又可能造成版本/repair 漂移；边界是大单体 composition root 需拆 contract tests。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/reason-coded-ingestion-routing/` 做纯 Python fixture，不安装 pdf-inspector：

1. `document-route.schema.json`：`input_id, detector_version, units[], class, confidence, reason_codes, attempted_lanes, selected_lane, terminal_state`。
2. synthetic units 覆盖：native text、scan、mixed、garbled、empty、detector/extractor disagreement、partial sample。
3. validator 要求 expensive fallback 必须有 reason；`empty/garbled/unobserved` 不得写 completed；projection 必须引用原输入 hash 与 detector revision。
4. 用 shared hub 现有历史文本/空文件做无害 fixture，不处理真实私有 PDF，不联网 OCR，不写 curated。

#### 风险边界

- **License**：仓库 GitHub API 与 LICENSE 为 MIT；Cargo/npm/PyPI dependencies、bundled CMaps、benchmark corpus、预编译 wheel/WASM/npm 制品另审。
- **维护活跃度**：固定 commit 距查询约 19 分钟，issues/PR 高活跃；但仓库仅约 6 个月，接口、tag 与版本面变化快，open issues 显示 cross-stage correctness 尚不稳定。
- **安全风险**：PDF 是复杂攻击面；compressed/object bombs、pathological content streams、字体/CMap、递归 XObject、巨大页数可能造成 CPU/内存 DoS。源码未见宿主级进程资源限制；需外部 timeout/memory/file-size sandbox。
- **内容完整性**：启发式会 false positive/negative；Markdown 不是 canonical PDF 证据，表格/顺序/隐藏文本/批注/签名均可能丢失。
- **版本风险**：Releases 为空但 tags 存在，Cargo/README/tag 版本不一致；部署前必须固定 artifact digest，不能只 pin `main`。
- **运行局限**：本机无 Cargo/Rustc，所有 build/test/benchmark/runtime 结论待核验。
- **不适用场景**：签名验证、法务取证、像素保真、复杂公式/图表、必须 100% 内容完整的归档，不应只依赖 Markdown extractor。
- **不可自动执行**：不把未知 PDF 直接送 hosted OCR，不在 Hermes 主进程内无预算解析，不自动上传私有文件，不自动改 ingestion config。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`reason-coded staged routing`，即 per-unit class/confidence/reason/attempted lane/terminal state；适用于 PDF、网页采集、GitHub source lane 和 provider fallback。
- **需验证**：先做 synthetic disagreement/partial/garbage fixtures，再选少量公开 PDF 在受限进程里 differential test；验证前不声称可直接迁移。
- **暂不沉淀**：PDF parser、OCR classifier 阈值、Rust tables/markdown 实现、bindings、Firecrawl 产品集成；它们是领域代码且本机无 runtime 证据。
- **今日动作**：只写 project card、runtime lessons 与 candidate；不创建 shared skill，不复制上游源码到 capabilities，不写 curated active fact。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/reason-coded-ingestion-routing/{schema.json,fixtures/,validate.py,test_contract.py,README.md}`。
2. GitHub 学习 source lane：未来可让 `scripts/github_learning_orchestrator.py` 的 source evidence 增加 `attempted/state/reason/items`，避免 API 403、空 release、缺 toolchain都折叠成空数组；先 sidecar POC，不直接改生产脚本。
3. 若验证通过，优先更新现有 `capabilities/skills/research/github-hot-project-learning/` 的 source outcome/coverage 条款，不新建 PDF 产品 skill。
4. raw clone/API/test stdout 留 `runtime/hermes/`；完整研究报告留 `inbox/hermes/daily/`；只有稳定、跨 Agent、去重后的契约才进入 curated/shared skill。
5. 当前 OpenClaw runtime 不存在；只设计 agent-neutral schema，不创建或调用 OpenClaw adapter。

---

### 2. livekit/agents

- **URL**：https://github.com/livekit/agents
- **Stars / Forks / Language / License（GitHub API）**：**12,387 / 3,477 / Python / Apache-2.0**。
- **创建 / updated / pushed**：2023-10-19T23:00:55Z / 2026-08-04T23:31:10Z / 2026-08-04T22:53:45Z。
- **固定 commit**：[`04d00cbd311f`](https://github.com/livekit/agents/commit/04d00cbd311fa980f5276b7eb29aa099f2ea16ff)，commit time 2026-08-04T16:20:19Z，message `Feat/anam support ai disclosure (#6695)`。
- 最新 GitHub Release：[`livekit-agents@1.6.8`](https://github.com/livekit/agents/releases/tag/livekit-agents%401.6.8)，published 2026-08-03T19:40:33Z；GitHub Release assets 为空。固定 main 晚于 release，源码结论不能外推到 1.6.8 PyPI artifact。

#### 一句话判断

LiveKit Agents 值得学的不是“接 50 个语音厂商”，而是它把 **session、Agent、model node、media I/O、fallback、worker process、recording/telemetry**做成不同生命周期层，并让 capability 决定是否包装 streaming adapter；对 Hermes 更有价值的是“能力协商 + 局部 fallback 状态机 + 资源/隐私显式开关”，不是迁移 WebRTC runtime。

#### 解决的问题：替代了什么旧做法

1. 替代把 STT→LLM→TTS 写成一个阻塞函数：`AgentSession` 管理 turn、interrupt、endpoint、tool steps、I/O、event 和 close lifecycle。
2. 替代 provider-specific application code：Agent node 接口和 plugin packages 把 STT/LLM/TTS/realtime 差异放在 adapter 层。
3. 替代“非 streaming provider 不可用”的做法：若 capability 声明 non-streaming 且有 VAD，则自动包 `StreamAdapter`；无 VAD 就明确报错。
4. 替代“provider 错误由外层整体重启 session”的做法：STT fallback 在 recognize/stream 局部切 provider，并独立恢复失效 provider。
5. 替代“fallback 内外层重复 retry”的指数放大：fallback 默认外层 `max_retry=0`，每 provider attempt 自己有 retry/timeout。
6. 替代“录音/trace/log/transcript 一个总开关”的粗粒度做法：`RecordingOptions` 可逐项控制并有 redaction 语义。
7. 替代所有 job 共用主进程：`AgentServer` 组合 process/thread pool、idle process、memory warning/limit、drain timeout、health/metrics。

边界：实时音频系统的 correctness 依赖网络、时序、provider、硬件、WebRTC 与用户隐私。定向 8 tests 只验证 STT fallback/prewarm 的 fake lane，不能证明完整 session、worker、录音、provider 或 release 制品。

#### 架构 / 实现与数据流

```text
LiveKit room / console / remote session
                  │
                  ▼
AgentServer / Worker
  ├─ dispatch + load + health + drain
  └─ ProcPool / ThreadPool → JobContext
                  │
                  ▼
             AgentSession
  ├─ media/text input + VAD + turn handling
  ├─ AgentActivity / Agent handoff / tool executor
  ├─ STT node ── capability adapter / fallback
  ├─ LLM node ── chat stream / tool calls
  ├─ TTS node ── sentence stream adapter / audio
  └─ events + metrics + recording + close terminal
                  │
                  ▼
      room output / transcript / telemetry
```

AgentServer 负责 job 分配和进程资源；JobContext 进入 AgentSession 后，session 组合全局 chat context、turn handling、model instances、tool policy、media I/O 与 event。每个 Agent 可以覆写 node 或局部 model；非 streaming STT/TTS 由 adapter 补 streaming surface。FallbackAdapter 在 provider 失败时切换，并并行探测恢复，但 session 仍负责不可恢复错误计数和终止。

#### Repo tree 摘要

```text
livekit-agents/                           # fixed commit tracked paths: 1,289
├── README.md / LICENSE / NOTICE          # 产品入口、Apache-2.0 notices
├── MODEL_LICENSE                         # LiveKit proprietary model 的额外限制
├── pyproject.toml / uv.lock              # 323-package lock graph、workspace sources
├── livekit-agents/
│   ├── pyproject.toml                    # core 31 direct deps、72 optional plugin groups
│   └── livekit/agents/
│       ├── worker.py / job.py / ipc/     # dispatch、process pool、memory/drain
│       ├── voice/                        # AgentSession、Agent、activity、turn、I/O
│       ├── stt/ / tts/ / llm/ / vad.py   # provider-neutral interfaces/adapters
│       ├── inference/                    # hosted model adapters
│       ├── telemetry/ / metrics/         # traces、usage、Prometheus
│       └── cli/ / testing.py / evals/    # app lifecycle、test/eval surface
├── livekit-plugins/                      # 大量 provider 独立 packages
├── tests/                                # fake providers + category-based tests
└── examples/                             # voice/avatar/industry samples
```

#### 关键源码文件

| 文件 | 用途 | 关键内容摘要 |
|---|---|---|
| `livekit-agents/livekit/agents/voice/agent_session.py` | session composition root | models、turn、recording、I/O、events、error counts、locks、start/close |
| `.../voice/agent.py` | Agent contract | instruction/tools/chat context、model override、node customization、stream adapters |
| `.../stt/fallback_adapter.py` | provider fallback | capability aggregation、attempt timeout/retry、availability、stream recovery |
| `.../worker.py` | job runtime | dispatch、load shedding、process/thread executor、memory limit、drain、health |
| `tests/test_stt_fallback.py` | fake regression tests | recognize/stream fallback、timeline offset、recovery failure isolation |
| `tests/test_stt_prewarm.py` | prewarm contract | 只 prewarm primary，non-streaming + VAD wrapping |
| `livekit-agents/pyproject.toml` | core dependency truth | 31 core deps、72 optional provider groups、Python 3.10–3.14 |
| `MODEL_LICENSE` | model legal boundary | LiveKit Models 仅能与 LiveKit Agents 使用，不等同 Apache repo code |

#### 源码精读（固定 commit）

**代码块 1：session 把 recording/connection/turn options 变成 typed runtime state**  
来源：[`agent_session.py#L101-L158`](https://github.com/livekit/agents/blob/04d00cbd311fa980f5276b7eb29aa099f2ea16ff/livekit-agents/livekit/agents/voice/agent_session.py#L101-L158)

```python
class RecordingOptions(TypedDict, total=False):
    audio: bool
    traces: bool
    logs: bool
    transcript: bool
    redaction: bool

_RECORDING_ALL_ON = {
    "audio": True, "traces": True, "logs": True,
    "transcript": True, "redaction": False,
}

def _resolve_recording_options(record: bool | RecordingOptions) -> RecordingOptions:
    if isinstance(record, bool):
        defaults = _RECORDING_ALL_ON if record else _RECORDING_ALL_OFF
        return RecordingOptions(**defaults)
    return RecordingOptions(**{**_RECORDING_ALL_ON, **record})

@dataclass
class SessionConnectOptions:
    stt_conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS
    llm_conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS
    tts_conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS
    max_unrecoverable_errors: int = 3
```

逻辑：recording 不是隐式 telemetry side effect，而是 audio/traces/logs/transcript/redaction 的 sparse policy；provider connection options 也按 STT/LLM/TTS 分开。可迁移到 Hermes 的是“每个 evidence/export lane 独立状态”，避免一个 `record=true` 隐含所有数据出口。边界是默认 sparse dict 从 all-on 合并；若调用者只写 `{"logs": false}`，audio/transcript 仍开，必须在隐私敏感场景使用 explicit all-off + allowlist，而非误读为最小记录。

**代码块 2：Agent node 根据 capability 决定 adapter，不默默伪造 streaming**  
来源：[`agent.py#L474-L521`](https://github.com/livekit/agents/blob/04d00cbd311fa980f5276b7eb29aa099f2ea16ff/livekit-agents/livekit/agents/voice/agent.py#L474-L521)

```python
@staticmethod
async def stt_node(agent, audio, model_settings):
    activity = agent._get_activity_or_raise()
    wrapped_stt = activity.stt

    if not activity.stt.capabilities.streaming:
        if not activity.vad:
            raise RuntimeError(
                "STT does not support streaming; add a VAD or wrap it explicitly"
            )
        wrapped_stt = stt.StreamAdapter(stt=wrapped_stt, vad=activity.vad)

    conn_options = activity.session.conn_options.stt_conn_options
    async with wrapped_stt.stream(conn_options=conn_options) as stream:
        forward_task = asyncio.create_task(_forward_input(audio, stream))
        try:
            async for event in stream:
                yield event
        finally:
            await utils.aio.cancel_and_wait(forward_task)
```

逻辑：capability 是适配决策输入；可以可靠补齐的 non-streaming→streaming 需要 VAD，缺 prerequisite 就 fail loudly。forward task 在 finally 被取消，避免 session close 后悬挂。边界是 metadata 来自 plugin implementation，仍需 conformance tests；StreamAdapter 改变 latency、segmentation 与 accuracy，不能当作语义等价。

**代码块 3：fallback 禁止嵌套默认 retry，并给每个 provider 独立状态**  
来源：[`fallback_adapter.py#L25-L107`](https://github.com/livekit/agents/blob/04d00cbd311fa980f5276b7eb29aa099f2ea16ff/livekit-agents/livekit/agents/stt/fallback_adapter.py#L25-L107)

```python
DEFAULT_FALLBACK_API_CONNECT_OPTIONS = APIConnectOptions(
    max_retry=0, timeout=DEFAULT_API_CONNECT_OPTIONS.timeout
)

class FallbackAdapter(STT):
    def __init__(self, stt: list[STT], *, vad=None,
                 attempt_timeout=10.0, max_retry_per_stt=1,
                 retry_interval=5):
        if not stt:
            raise ValueError("At least one STT instance must be provided.")
        # non-streaming instances require VAD and are wrapped explicitly
        self._status = [
            _STTStatus(available=True,
                       recovering_recognize_task=None,
                       recovering_stream_task=None)
            for _ in stt
        ]
```

逻辑：fallback 外层默认不再 retry，而由每个 provider attempt 使用受控 retry/timeout，避免 `outer_retry × providers × inner_retry` 放大。recognize 和 stream recovery 各有 task slot，减少一条恢复路径压住另一条。边界是成本、数据地域、license、质量和 secret scope 没有在该 adapter 的 selection state 中显式表达；“可用”也不等于“策略允许 fallback”。

**代码块 4：失败 provider 的恢复探测不阻塞主 fallback lane**  
来源：[`fallback_adapter.py#L320-L420`](https://github.com/livekit/agents/blob/04d00cbd311fa980f5276b7eb29aa099f2ea16ff/livekit-agents/livekit/agents/stt/fallback_adapter.py#L320-L420)

```python
async def _forward_input_task() -> None:
    async for data in self._input_ch:
        for stream in list(self._recovering_streams):
            try:
                forward(data, stream)
            except Exception:
                pass

        if main_stream is not None:
            try:
                forward(data, main_stream)
            except Exception:
                logger.exception("error happened in forwarding input")

for i, stt in enumerate(self._fallback_adapter._stt_instances):
    if status.available or all_failed:
        try:
            async with stt.stream(/* bounded options */) as main_stream:
                async for ev in main_stream:
                    self._event_ch.send_nowait(ev)
            return
        except Exception:
            mark_unavailable(stt)
    self._try_recovery(stt)
```

逻辑：recovery probe 是旁路，不应因 push/flush 错误跳过主 stream；这由 `test_stt_stream_recovery_failure_doesnt_block_main` 回归。可迁移点是“main lane 与 health probe failure isolation”。边界是 recovery streams 同样消费 audio，可能增加 provider 成本和数据外发；实际系统必须记录哪些 provider 收到了哪些帧，并受 consent/data-region policy 控制。

**代码块 5：worker 将 job 资源和生命周期从 session 层分离**  
来源：[`worker.py#L177-L238`](https://github.com/livekit/agents/blob/04d00cbd311fa980f5276b7eb29aa099f2ea16ff/livekit-agents/livekit/agents/worker.py#L177-L238)

```python
@dataclass
class ServerOptions:
    entrypoint_fnc: Callable[[JobContext], Awaitable[None]]
    request_fnc: Callable[[JobRequest], Awaitable[None]] = _default_request_fnc
    prewarm_fnc: Callable[[JobProcess], Any] = _default_setup_fnc
    load_fnc: Callable[[AgentServer], float] = _DefaultLoadCalc.get_load
    job_executor_type: JobExecutorType = _default_job_executor_type
    load_threshold: float = 0.7
    job_memory_warn_mb: float = 1000
    job_memory_limit_mb: float = 0       # disabled unless configured
    drain_timeout: int = 3600
    shutdown_process_timeout: float = 10.0
    permissions: WorkerPermissions = field(default_factory=WorkerPermissions)
    api_key: str | None = field(repr=False, default=None)
    api_secret: str | None = field(repr=False, default=None)
```

逻辑：dispatch admission、prewarm、load、executor、memory、drain、permissions 与 secret repr 属于 worker contract，不塞进 Agent prompt。边界是 `job_memory_limit_mb` 默认 0（禁用），default room permissions 多项为 true；安全部署仍需显式最小权限和资源 limit，字段存在不等于已 enforce。

#### 依赖分析与供应链风险

- `livekit-agents/pyproject.toml` 列出 **31 个 core direct dependencies**，包括 pinned `livekit==1.1.14`、LiveKit API/protocol/local-inference、aiohttp、PyJWT、protobuf、AV、NumPy、Pydantic、OpenTelemetry、Prometheus、OpenAI、sounddevice、watchfiles。
- 同一 manifest 有 **72 个 optional provider/plugin groups**；root uv workspace 配置列出 11 个 member globs/paths，`uv.lock` 解析为 **323 packages**，大小 972,387 bytes。
- core manifest 有 `exclude-newer = "7 days"`，但 LiveKit 自家包例外为 `0 days`；这能降低部分新包风险，却不是 provenance/签名，也会造成“同一 lock resolution policy 下 first-party 与 third-party freshness 不同”。
- 本次看似只跑两个 core test files，`uv --with-editable ./livekit-agents` 仍因 root workspace/source 解析构建大量本地 plugins，安装 302 packages；说明从 monorepo root 做窄验证可能意外扩大 build/code execution 面。
- media/native/cloud dependencies（`av`、`sounddevice`、local inference、provider SDKs）带来二进制 wheel、FFI、系统库和凭据风险；fake tests 不覆盖它们。
- Dependabot API 403；未执行 `uv audit`/OSV scan，且 open PR #6692 正在更新 `aiohttp` security release。不能声称 lock graph 无漏洞。

#### README / release / issues / license 交叉核验

- README 的 AgentServer→JobContext→AgentSession→Agent 分层与实际 `worker.py`、`agent_session.py`、`agent.py` 对应；provider-neutral node 与 plugin 目录也一致。
- 最新 release `livekit-agents@1.6.8` 于 2026-08-03 发布，无 GitHub asset；main 已有更新，因此 test 绑定 main commit，不证明 PyPI 1.6.8。
- open PR [#6690](https://github.com/livekit/agents/pull/6690) 要让 fallback adapter 报告 active instance 的 model/provider，说明固定 main 当前 `FallbackAdapter.model/provider` 仍固定写 `FallbackAdapter/livekit`，observability 无法完整反映实际 provider。
- open PR [#6697](https://github.com/livekit/agents/pull/6697) 讨论 stream 在产生 generation 前保持 retryable；[#6689](https://github.com/livekit/agents/pull/6689) 讨论 process init backoff；[#6692](https://github.com/livekit/agents/pull/6692) 是 aiohttp security update。这些均未合并到固定 commit，不外推。
- closed issue #6682 与 merged PR #6683 说明 TTS fallback 曾因共享 recovery task slot 让一条路径压制另一条；STT 当前源码已经拆 recognize/stream slots，但不证明所有 LLM/TTS/plugin fallback 都具有相同状态机。
- 仓库代码为 Apache-2.0；README 明确 turn detection models 另受 `MODEL_LICENSE` 约束。该 license 限制 LiveKit Models 只能与 LiveKit Agents 使用，并禁止用输出开发其他非 LiveKit models；不能把模型当 Apache 资产迁入 Hermes。
- 仓库没有 `SECURITY.md`（固定 tree 搜索为 0）；安全报告流程/支持版本为**待核验**。

#### 真实测试结果

```text
$ python3 -m compileall -q livekit-agents/livekit/agents
compileall livekit core: PASS

$ uv run --isolated --with-editable ./livekit-agents \
    --with 'pytest>=9.0.3,<9.1' \
    --with 'pytest-asyncio>=0.25.3' \
    --with 'pytest-asyncio-concurrent==0.5.2' \
    pytest -q tests/test_stt_fallback.py tests/test_stt_prewarm.py --disable-warnings
Installed 302 packages in 1.28s
........ [100%]
8 passed in 0.22s
```

```text
$ git rev-parse HEAD
04d00cbd311fa980f5276b7eb29aa099f2ea16ff
$ git ls-files | wc -l
1289
$ git status --short
# empty（tracked worktree clean）
```

覆盖：fake STT recognize/stream failover、start-time offset、provider recovery、broken recovery stream 与 main stream isolation、primary-only prewarm、non-streaming+VAD wrapping。准确边界：

- 只跑 2 个 test files / 8 tests，不是完整 unit suite。
- 没有启动 AgentServer/ProcPool/Room/console，没有 audio device/WebRTC/telephony。
- 没有读取或设置 `LIVEKIT_*` / provider key，没有调用 STT/LLM/TTS/API。
- 没有验证 recording/redaction、worker memory kill、drain、Windows、full provider plugin、release/PyPI provenance。
- 安装 302 packages 是测试环境事实，不代表生产必须启用 72 个 plugins；也不等于这些包安全。

#### 可复用经验

- 当 backend capability 不一致时，应优先用 versioned capability envelope 决定 adapter，并在 prerequisite 缺失时 fail loudly，因为“统一接口”不能靠静默伪造；边界是 capability declaration 必须经过 conformance tests。
- 当 fallback 跨多个 provider 时，应优先关闭外层重复 retry、为每个 attempt 设置 timeout/retry，并记录 active provider/attempt，因为嵌套 retry 会放大延迟、成本和不可观测性；边界是 fallback 还需 policy/consent/data-region gate。
- 当恢复探测与主服务并行时，应优先隔离 probe failure 和 main lane，并给每条路径独立 task/state，因为一个健康探针不应饿死正在服务的 fallback；边界是 probe 自身也会消费数据和费用。
- 当 telemetry/recording 涉及多类数据时，应优先逐 lane explicit opt-in/opt-out 并记录 redaction policy，因为一个总开关容易意外上传 audio/transcript；边界是 sparse all-on default 对隐私场景不够安全。
- 当 Agent job 有重资源或长连接时，应优先在 worker/process 层设置 load、memory、drain 和 permission，而不是只在 prompt 写限制；边界是默认 0 memory limit 或宽 permissions 仍需部署者收紧。

#### 30 分钟最小实验

在 `runtime/hermes/github-learning-poc/capability-fallback-receipt/` 做离线 fake adapter：

1. provider fixture：`capabilities, policy_tags, cost_class, data_region, attempts, fail_sequence`。
2. request policy：`required_capability, allowed_providers, max_attempts, deadline, fallback_allowed`。
3. receipt：每次 `provider, start/end, state, reason, retry_count`，exactly-one terminal；active provider 必须可见。
4. tests：non-streaming without adapter blocked、outer×inner retry prohibited、probe failure不阻塞 main、policy不允许时不 fallback、all failed 不是空 success。
5. 不调用真实 provider、不读取 key、不处理音频、不修改 Hermes model/provider/config。

#### 风险边界

- **License**：framework code Apache-2.0；NOTICE、72 个 plugin dependencies、provider SDK/API terms、模型与数据另审。`MODEL_LICENSE` 不是 Apache，禁止脱离 LiveKit Agents 使用 LiveKit Models。
- **维护活跃度**：固定 commit 查询前约 7 小时，最新 release 前一天发布，PR/commit 非常活跃；同时接口与 fallback/stream semantics 快速变化，升级风险高。
- **隐私/安全**：audio、video、transcript、logs、traces、MCP/tools、telephony 和 provider credentials 都可能出域；recording sparse default 为 all-on 基线，部署必须显式审查。
- **fallback 风险**：切 provider 可能改变地域、价格、retention、模型 license、语言质量与 aligned transcript capability；当前 adapter 的 active model/provider observability 仍有 open PR。
- **供应链**：core + 72 optional groups + native/media/provider SDK 面积大；一次窄测试安装 302 packages，monorepo workspace resolution 可能扩大 CI 攻击面。
- **资源风险**：worker 有 memory limit 字段但默认禁用；音视频 buffer、模型、插件和 process pool 可能占用大量内存/CPU。
- **运行局限**：只有 compileall + 8 fake tests；真实 network/audio/provider/session/process 行为待核验。
- **不适用场景**：Hermes/shared hub 当前不是实时 voice/WebRTC worker，不应迁移 AgentSession/AgentServer 或 provider ecosystem。
- **不可自动执行**：不启用 recording、MCP、telephony，不连接房间，不设置/读取 key，不安装全套生产 plugins，不修改 provider fallback。

#### Skill 升格判断

**需二次验证。**

- **可迁移候选**：`capability-aware fallback receipt`：required capability、adapter prerequisite、allowed provider、attempt state、active provider、terminal reason。
- **需验证**：用纯 fake provider 覆盖 nested retry、probe isolation、policy-denied fallback、deadline、all-failed terminal，再与现有 verification-first/effect-scope/orchestrator 四状态候选去重。
- **暂不沉淀**：LiveKit product integration、voice/session/WebRTC、plugins、turn detection model、recording runtime、worker process implementation；与当前 Hermes 目标不匹配且权限/依赖面过大。
- **今日动作**：只更新 project card、lessons 与日报 candidate；不安装服务、不创建 shared skill、不复制上游 agent skill、不写 curated active fact。

#### Hermes / shared hub 落地路径

1. POC：`runtime/hermes/github-learning-poc/capability-fallback-receipt/{schema.json,fake_providers.py,router.py,fixtures/,test_router.py,README.md}`。
2. Hermes 工具/provider 契约候选：在 adapter metadata 声明 `capabilities/effects/data_class`，在最终调用前由 host policy 校验；今天不改 `~/.hermes/config.yaml` 或 provider 配置。
3. 自主学习编排候选：source fetch、clone、test、KB projection 可视作 provider lanes，但 fallback 必须受明确 allowed source 与 deadline 限制，并记录 active lane，而不是吞掉 403/timeout。
4. shared skill 若验证通过，优先更新 `capabilities/skills/autonomous-learning/orchestrator-protocol/` 或 `research/github-hot-project-learning/` 的 fallback/receipt 小节，避免新建 LiveKit 产品 skill。
5. raw package/test logs 留 runtime；日报留 Hermes inbox；跨 Agent schema 经治理后才共享。当前不创建或调用 OpenClaw runtime。

## 横向对照：reason-coded routing 与 capability-aware fallback

| 层次 | pdf-inspector | livekit/agents | Hermes/shared hub 候选 |
|---|---|---|---|
| 输入身份 | PDF bytes/path、page | room/job/session、audio stream | run/source/artifact immutable ID |
| cheap classification | text/image/font/layout signals | provider capability + availability | source capability/precondition |
| partial unit | page + OCR reason | provider attempt/stream leg | evidence lane + item scope |
| fallback | caller把问题页送 OCR | STT provider switch + recovery probe | explicitly allowed adapter/source lane |
| completion | result + Markdown/reason | session events/terminal/error | exactly-one terminal + receipt + coverage |
| uncertainty | confidence、garbled、needs_ocr | unavailable、timeout、all failed | partial/blocked/unobserved/failed |
| hard boundary | untrusted PDF/resource budget | audio privacy/network/credentials/process | effect policy、secret boundary、runtime budget |

共同机制不是“自动 fallback 越多越好”，而是：先声明 unit、capability、reason 和 policy，再执行有界 fallback；任何 adapter、probe 或 projection 都必须留 receipt。差异是 PDF 的 fallback 往往改变计算成本，voice provider fallback 还会改变数据出域、license、价格和隐私，因此后者必须有更强 policy gate。

## 经验沉淀

1. 当输入可进入便宜或昂贵处理 lane 时，应优先输出 per-unit `class + confidence + reason` 再路由，因为整份资源的单一布尔值无法表达 mixed/partial；边界是 threshold 必须版本化并做真实 corpus 回归。
2. 当 parser/checker 产生非空结果时，应优先继续验证 encoding、coverage、garbage 与 stage consistency，因为“有输出”不等于“内容完整”；边界是 conservative gate 也会误杀，必须保留原输入和 replay fixture。
3. 当 backend capability 不一致时，应优先让 capability envelope 驱动 adapter，并在 prerequisite 缺失时 blocked，因为静默模拟能力会隐藏语义变化；边界是 self-declared capability 需要 conformance tests。
4. 当 fallback 包含多 provider 与多层 retry 时，应优先关闭外层重复 retry、限制每 attempt 的 deadline，并记录 active provider，因为嵌套 retry 会放大延迟和成本；边界是 fallback policy 还需覆盖地域、license、privacy 和 consent。
5. 当 recovery probe 与 main lane 并行时，应优先给它们独立 state/task 并隔离 probe failure，因为健康检查不应阻塞当前服务；边界是 probe 仍会消费输入、网络和费用。
6. 当多个 detector 从强证据到弱 heuristic 依次尝试时，应优先记录每 lane 的 attempted/result/provenance，因为 first-valid-wins 只保留 winner 会丢失冲突；边界是记录本身要受 size/privacy 预算。
7. 当 telemetry/recording/export 含 audio、transcript、logs、traces 等不同数据时，应优先逐 lane 最小化，而不是依赖一个总开关，因为 sparse all-on default 容易造成意外出域；边界是 redaction 不等于获得处理授权。
8. 当 Agent job 可能消耗大量 CPU/内存或持有长连接时，应优先在 worker/process 层设置硬预算、drain 和 permission，因为 prompt 约束不是资源 enforcement；边界是声明了 limit 但默认禁用仍无保护。
9. 当只想测试 monorepo 的窄 core 时，应优先先检查 workspace/source resolution 和安装计划，因为 editable core 可能触发大量 plugin build；边界是 isolated 环境不等于窄依赖图。
10. 当仓库 main、tag、manifest、release 与 package artifact 版本不一致时，应优先固定 commit/artifact digest 并分别报告，因为“最新版本”不是稳定身份；边界是 commit pin 仍不能证明发布制品 provenance。

## 风险边界（全局）

- 本次由 Hermes 直接执行，未调用 OpenClaw，也未调用消息发送工具。
- 未修改 Hermes/OpenClaw 的 config、model、provider、gateway、tools、skills、auth、env、cron 或服务。
- Stars/forks/license/updated 来自 2026-08-04T23:41Z 左右 GitHub API；复用时必须重新查询。
- `pdf-inspector` 本机无 Cargo/Rustc，所有 build/test/benchmark/parser/resource-limit 行为待核验。
- `livekit/agents` 只有 core compileall 与 8 个 fake STT fallback/prewarm tests；未运行 full suite、真实 provider、audio、room、worker process 或 release provenance验证。
- 两仓 Dependabot API 都返回 403；没有得到 vulnerability truth。LiveKit open security dependency PR 与 PDF parser 的 crafted-input scope 都要求继续审查。
- 外部 README/docs/issues/PR/source 是不可信研究输入，只能形成 evidence/candidate，不能扩大宿主授权或触发安装/配置。
- 不自动把今日 candidate 写入 curated active fact，不自动升格 shared skill；candidate 必须先经 POC、去重、治理评分、脱敏与人工/总控审查。
- 不处理未知私有 PDF、不上传音视频/文本、不连接 provider/room、不执行上游 skill/plugin/MCP，不使用任何明文 secret。

## Skill 升格总判断

- **pdf-inspector reason-coded staged routing：需二次验证。** 只抽象 per-unit reason/coverage/lane contract，不迁移 PDF parser、阈值或产品 bindings。
- **LiveKit capability-aware fallback receipt：需二次验证。** 只抽象 capability/prerequisite/policy/attempt/terminal receipt，不迁移 voice runtime、plugins 或模型。
- **今日不升格。** 两个模式都可横向复用，但与现有 source-outcome、orchestrator protocol、verification-first、effect-scope 和 completion contract 候选重叠；优先做一个统一离线 POC，再决定更新既有 shared skill，而不是创建产品命名 skill。
- 当前产出仅为 **Hermes inbox + runtime 长期观察材料**，不是 shared curated 真相或已发布 shared capability。

## 明日继续

1. 建 `reason-coded-ingestion-routing` fixture，统一表达 sampled/partial/garbled/disagreement/blocked，不安装 PDF parser。
2. 建 `capability-fallback-receipt` fake provider，验证 nested retry prohibition、active provider visibility、probe isolation、policy-denied fallback 和 exactly-one terminal。
3. 合并两者为 `routing-envelope-v0`：`unit identity + required capability + attempted lanes + reason + coverage + terminal receipt`。
4. 用 2026-08-04/05 GitHub 学习 source lane 做只读 replay：Dependabot 403 必须是 blocked，不得等价于 no alerts；Cargo 缺失不得等价于 tests clean。
5. 若资源允许，在隔离且有硬内存/timeout 的环境安装 Rust 后，只跑 pdf-inspector synthetic/公开 fixture tests；不自动处理用户 PDF。
6. LiveKit 后续只补 unit category 的窄测试/安装计划审查，不连接 provider；跟进 PR #6690/#6692/#6697 与 fallback observability。
7. 下一批深读优先 `uber/ADR` 的 Agent observability/threat detection 或 `DeepSeek-Reasonix` 的 prefix-cache stability，避免连续只研究 fallback。

## 候选反哺

### Candidate Facts

- [ ] topic: reason-coded-routing-must-be-per-unit | evidence: pdf-inspector `pages_needing_ocr + ocr_reasons_by_page` 与 Mixed/page quality gates | 建议: update existing source-outcome/completion candidate after fixture | 安全级别: medium
- [ ] topic: parser-output-needs-stage-consistency-checks | evidence: fixed commit 修复静默 text truncation；issue #251/#252 报告 detect/extract/Markdown disagreement | 建议: candidate for ingestion verification | 安全级别: high
- [ ] topic: fallback-retry-must-be-single-layer-and-receipted | evidence: LiveKit outer `max_retry=0` + per-STT bounded attempt + availability state | 建议: update orchestrator protocol after fake tests | 安全级别: high
- [ ] topic: recovery-probes-must-not-block-main-lane | evidence: LiveKit 独立 recovery task/stream 与 regression test；本机定向 tests通过 | 建议: update resilient adapter candidate | 安全级别: medium
- [ ] topic: sparse-recording-defaults-can-expand-data-egress | evidence: LiveKit RecordingOptions sparse dict merges from all-on | 建议: candidate privacy checklist, not user fact | 安全级别: high

### Candidate Skills / Workflow

- [ ] 名称: routing-envelope-v0 | 可复用场景: GitHub sources、网页/PDF ingestion、provider/tool fallback、KB projection | 是否建议 shared: yes（POC 与治理后更新既有 skill） | 原因: 跨 Agent 横切，但应与 source-outcome/orchestrator/completion 去重
- [ ] 名称: reason-coded-ingestion-routing | 可复用场景: mixed/partial document or source lanes | 是否建议 shared: no（先作为统一 envelope 的 fixture 子集） | 原因: 单独成 skill 容易过窄/重复
- [ ] 名称: livekit-agents-product-integration | 可复用场景: realtime voice/WebRTC | 是否建议 shared: no | 原因: 当前无业务授权，依赖、隐私、模型 license 和 provider 面过大
- [ ] 名称: pdf-inspector-product-integration | 可复用场景: PDF→Markdown | 是否建议 shared: no | 原因: 无本机 Rust runtime证据，且 parser/阈值是领域实现

### Candidate Open Questions

- [ ] 问题: source/result envelope 应如何统一 `confidence`（概率/启发式）与 `terminal_state`（确定性状态），避免调用方混用？ | reason: schema/adaptation | priority: high
- [ ] 问题: fallback receipt 是否必须记录数据实际发送到哪些 provider/probe，以及 region/license/cost policy revision？ | reason: privacy/governance | priority: high
- [ ] 问题: first-valid detector 如何保留 skipped/conflicting lane，同时控制 evidence 体积？ | reason: coverage/budget | priority: medium
- [ ] 问题: `uv` 在 monorepo root 的窄 core 测试为何解析/构建大量 plugin，如何在不改变 lock truth 的前提下做 truly minimal test env？ | reason: supply-chain/adaptation | priority: high
- [ ] 问题: pdf-inspector 的 Cargo/README/tag/crate/npm/PyPI 版本如何对应，是否有可验证 release provenance？ | reason: stale/provenance | priority: medium
- [ ] 问题: LiveKit PR #6690 合并后 active provider identity 是否覆盖 metrics、receipts 与 recovery probe？ | reason: observability/stale | priority: medium

### 不应自动落地

- 不安装或部署 LiveKit server/Agents，不连接 room/telephony/provider，不启用 recording，不使用 LiveKit Models，不复制受 MODEL_LICENSE 限制的资产。
- 不把未知 PDF 交给本机主进程或 hosted OCR，不上传私有文档，不把 Markdown 当法律/取证 canonical evidence。
- 不修改 Hermes/OpenClaw config、model、provider、tools、skills、auth、env、cron；当前任务不调用 OpenClaw。
- 不把今日 candidate 直接写入 curated active fact 或 shared skill manifest；先做 runtime POC、历史 replay、去重、治理评分、脱敏与人工/总控审查。
