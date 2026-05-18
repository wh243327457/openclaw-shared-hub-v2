# OpenHuman 机制本地化会话参考

> 记录本次把 OpenHuman 调研结果转成 shared 项目骨架、runtime 计划和 Obsidian 计划的做法。

## 适用场景

当用户确认某个外部项目/文章中的机制“符合自我学习、持续升级、跨 agent 共享上下文”的方向时，不要停留在概念点评，直接把它落成三层产物：

1. **shared curated 项目骨架**：作为跨 agent 真相源。
2. **runtime 计划与状态**：用于可恢复执行、POC 分阶段推进。
3. **Obsidian 学习入口**：给人类可读、可复盘的长期文档。

## 本次落盘顺序

1. 先做外部调研与二轮复核，确认机制、风险、边界。
2. 将核心判断沉淀为 `curated/memory/projects/<project>.md`。
3. 同步 `curated/memory/MEMORY.md` 的索引入口。
4. 建立 `runtime/<agent>/<project>/implementation-plan.md`、`state.json`、`architecture.md`。
5. 为 POC 生成可复用模板（triage contract、source schema、compression rules）。
6. 再把人类可读版本写进 Obsidian 风格知识库。
7. 最后只做验证，不把 runtime 当真相源。

## 重要边界

- 不把外部项目本体当作系统依赖。
- 不把 GPL 源码直接复制进 Hermes/OpenClaw 核心。
- 不把 runtime/sqlite/cache/chunks 当作 curated 真相源。
- 需要 Hermes review 的结论，才允许晋升 curated。

## 这次形成的可复用模板

- Trigger triage：`drop / acknowledge / react / escalate`
- Source schema：canonical Markdown + provenance
- Token compression：自研规则，不复用 GPL 代码
- 项目状态流：`planned -> skeleton -> pocs -> review -> tested -> active`

## 什么时候复用这条参考

- 外部项目看起来像“机制样板”而不是“直接要接入的产品”。
- 用户明确说这套流程适合自我学习、升级、记忆、复盘、共享上下文。
- 需要把调研结果同时落到 shared、runtime 和 Obsidian。
