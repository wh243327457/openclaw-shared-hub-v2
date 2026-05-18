# future-agent 共享中台接入说明

本文定义 future-agent 接入共享中台 v2 的最小契约。future-agent 介入时，应先读取 canonical 入口，再写入自己的 inbox/runtime，不直接污染 curated。

## 读取顺序

1. `manifest.yaml`
2. `AGENTS.md`
3. `curated/memory/MEMORY.md`
4. 按需读取：
   - `curated/memory/facts/`
   - `curated/memory/projects/`
   - `capabilities/manifests/shared-skills.yaml`
   - `capabilities/skills/`

## 写入边界

- 原始工作记录：`inbox/future-agent/daily/YYYY-MM-DD.md`
- 临时产物 / cache / 日志：`runtime/future-agent/`
- 稳定事实：只在通过晋升审核后写入 `curated/memory/facts/`
- 项目状态：只在通过晋升审核后写入 `curated/memory/projects/`
- 跨 Agent 技能：通过 shared skill 升格流程进入 `capabilities/skills/`

## 禁止事项

- 禁止把明文 secret 写入 shared。
- 禁止把 runtime 产物写入 curated。
- 禁止把未验证的猜测直接写入 curated。
- 禁止绕过 `docs/promote-protocol.md` 自动晋升长期记忆。

## smoke test 记录格式

在首次接入时，写入 `inbox/future-agent/daily/YYYY-MM-DD.md`：

```markdown
## future-agent shared hub smoke test

- 时间:
- 读取入口:
  - manifest.yaml: ok / failed
  - AGENTS.md: ok / failed
  - curated/memory/MEMORY.md: ok / failed
  - capabilities/manifests/shared-skills.yaml: ok / failed
- 写入测试:
  - inbox/future-agent/daily/YYYY-MM-DD.md: ok / failed
  - runtime/future-agent/: ok / failed
- 结论:
- 问题:
```

## 验收命令

```bash
cd /home/vany/agent/.openclaw/shared
python3 scripts/verify_bridge.py
```
