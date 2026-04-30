# shared-hub-v3 stage1 计划

状态：seed / 可落盘验证
日期：2026-04-17

## 目标

1. 在当前 repo 内孵化一个自包含的 v3 seed，路径固定为 `next/shared-hub-v3/`
2. 保持 v2 现有 manifest / compat / legacy 语义不变
3. 先把 v3 的最小内核落出来：`manifest.yaml + agents/ + registry/ + truth/ + sandbox/`
4. 提供一个本地可执行的校验入口，验证骨架完整性与关键约束

## 非目标

1. 不改造现有 v2 根目录
2. 不在 v3 根目录实现 `compat/`、`memory/`、`skills/` 等旧兼容层
3. 不实现 v2 -> v3 迁移脚本
4. 不实现完整 capability registry
5. 不实现真实的 promote / adapter / shim 运行逻辑

## 文件清单

- `next/shared-hub-v3/README.md`
- `next/shared-hub-v3/AGENTS.md`
- `next/shared-hub-v3/manifest.yaml`
- `next/shared-hub-v3/agents/manifest.yaml`
- `next/shared-hub-v3/agents/hermes/agent.yaml`
- `next/shared-hub-v3/agents/openclaw/agent.yaml`
- `next/shared-hub-v3/agents/future-agent/agent.yaml`
- `next/shared-hub-v3/registry/manifest.yaml`
- `next/shared-hub-v3/truth/memory/MEMORY.md`
- `next/shared-hub-v3/truth/memory/facts/.gitkeep`
- `next/shared-hub-v3/truth/memory/projects/.gitkeep`
- `next/shared-hub-v3/sandbox/hermes/.gitkeep`
- `next/shared-hub-v3/sandbox/openclaw/.gitkeep`
- `next/shared-hub-v3/sandbox/future-agent/.gitkeep`
- `next/shared-hub-v3/schema/manifest.schema.yaml`
- `next/shared-hub-v3/policy/write-rules.yaml`
- `next/shared-hub-v3/tools/shared_v3_verify.py`
- `next/shared-hub-v3/scripts/verify_v3.sh`

## 验证命令

```bash
bash next/shared-hub-v3/scripts/verify_v3.sh
```

预期：输出 `PASS`，并返回 exit code 0。

## 下一批建议

1. 增加 `registry/capabilities/` 的最小声明格式
2. 增加 `schema/agent.schema.yaml`，把 agent 元数据也正式化
3. 增加 `sandbox/` -> `truth/` 的 promote 协议草案
4. 增加 Hermes adapter 约束文档，明确怎么从 v2 迁到 v3
