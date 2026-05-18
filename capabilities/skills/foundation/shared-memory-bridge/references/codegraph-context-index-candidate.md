# 2026-05-17 — CodeGraph 上下文索引候选规则

## 背景

自主学习任务学习了 `colbymchenry/codegraph`：本地优先的代码语义知识图谱，用 tree-sitter/WASM 抽取符号和关系，SQLite/FTS5 存储，图遍历支持 callers/callees/impact radius，并通过 MCP/context builder 给 coding agent 提供结构化上下文。

## 结论

值得作为“代码上下文索引 / 自然语言到符号查询”类能力候选，但在本地 POC 前不要升格为 shared skill。正确沉淀方式是先放 runtime 规则，再做一个仓库索引验证。

## 可迁移规则

1. **先索引再对话**：中大型 repo 不应先盲扫全仓；先建立结构化代码索引，再让 agent 查入口、调用链、影响范围。
2. **证据路径必须保留**：每条图谱结果要带 symbol、file path、edge/call relation、必要 snippet，避免压缩后不可追溯。
3. **索引新鲜度是前置条件**：查询前检查 git HEAD / file hash / 索引更新时间；过期必须重建或标 UNKNOWN。
4. **静态图谱不等于业务事实**：动态语言、框架约定、运行时注入可能漏边；图谱只能降低盲扫，不替代审计。
5. **缓存不进 curated**：`.codegraph/`、SQLite、FTS、cache 只能放项目本地 ignored 目录或 runtime，不写 curated/memory。

## 推荐自然语言查询模板

- “这个功能的入口在哪里？返回入口 symbol、文件路径、上游调用方。”
- “修改 `<symbol/file>` 的影响半径是什么？列 callers/callees 和置信度。”
- “这条 API 从 route 到 storage 的数据流是什么？只返回证据链。”
- “找到 `<keyword>` 相关配置、env、初始化逻辑；按证据强弱排序。”
- “为这个 bug 定位最可能的 3 个函数，并说明证据。”

## 升格为 skill 前的验证门槛

1. 至少对一个本地 repo 完成索引。
2. 记录索引耗时、产物位置、查询样例和失败模式。
3. 至少 3/5 查询能返回可用 symbol/file/edge 证据。
4. 与直接 search/read 对比，确认确实减少盲扫或提升定位质量。
5. 明确 cache/SQLite/runtime 不写 curated、不泄露 secret。

## 关联 runtime 产物

本次会话已在 shared runtime 写入：

```text
runtime/hermes/codegraph-context-rules/
├── README.md
├── state.json
├── rules.md
└── poc-plan.md
```

## 对 skill 的影响

该经验横跨 `mcp/native-mcp`、`software-development/codebase-inspection`、`foundation/shared-memory-bridge` 等能力边界。当前最合适做法是保留在 shared-memory-bridge references 中作为跨 agent 运行时/curated 边界示例；等 POC 完成后再创建或更新更专门的 code-context-index 类 skill。