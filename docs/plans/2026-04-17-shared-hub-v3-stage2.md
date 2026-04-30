# shared-hub-v3 stage2 计划

状态：implementation / capability-registry + agent-schema + promote-draft
日期：2026-04-17

## 目标

1. 在不触碰 v2 兼容层的前提下，为 v3 seed 增加最小 capability registry。
2. 增加 `schema/agent.schema.yaml`，把 `agents/*/agent.yaml` 的约束显式化。
3. 增加 `sandbox/` -> `truth/` 的 promote 协议草案与记录模板。
4. 扩展 `tools/shared_v3_verify.py`，继续保持 Python 标准库实现。

## 本批次范围

- 新增 `registry/capabilities/` 清单与各 agent 的 capability 声明。
- 新增 `schema/agent.schema.yaml`。
- 新增 `protocol/promote-protocol.md` 与 `protocol/promote-log-template.md`。
- 更新 `manifest.yaml`、`AGENTS.md`、`README.md`、`registry/manifest.yaml`、`tools/shared_v3_verify.py`。

## 非目标

1. 不引入 v2 `compat/`、`memory/`、`skills/` 回流到 v3 根目录。
2. 不实现真实的 promote 执行器或迁移脚本。
3. 不把 capability registry 设计成复杂的插件市场或多 workspace 联邦。

## 验证命令

```bash
bash next/shared-hub-v3/scripts/verify_v3.sh
```

预期：输出 `PASS` 与 `wrapper=PASS`，并且校验 capability registry、agent schema、promote protocol 三类 stage2 新增内容。
