---
name: config-target-routing
description: 配置类任务的目标系统识别流程，避免把 Hermes / OpenClaw / shared 中台配置混用；用于修改模型、provider、gateway、tools、skills、auth、env、cron 等配置前的路由判断。
version: "1.0.0"
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [configuration, routing, hermes, openclaw, shared-hub]
    related_skills: [hermes-agent, shared-memory-bridge]
---

# Config Target Routing

## Overview

配置类任务必须先判断“目标系统是谁”，再读取或修改文件。这个 skill 的目标是避免在 Hermes、OpenClaw、shared 中台同时存在时，因为记忆中某个路径更显眼而误改错误系统。

核心原则：用户说“你 / 当前 agent / Hermes / 这个 agent”时，默认目标是 Hermes；只有明确提到 OpenClaw 或 OpenClaw 路径时才操作 OpenClaw；目标不清必须先问。

## When to Use

在以下任务前必须使用：

- 用户要求看配置、改配置、检查配置是否生效
- 新增、删除、切换模型或 provider
- 模型列表看不到某个模型
- 修改 gateway、tools、skills、auth、env、cron、streaming、fallback、profile
- 排查 Hermes / OpenClaw / shared 中台之间的配置冲突
- 用户只说“重启 / 改一下 / 看一下配置”，但没有明确目标系统

不要用于纯代码业务开发，除非该开发涉及 agent 自身配置。

## Target Decision Tree

1. 先看用户是否明确命名目标系统。
   - 包含 `Hermes`、`当前 agent`、`你`、`这个 agent`、`当前 CLI`、`当前网关`：目标是 Hermes。
   - 包含 `OpenClaw`、`openclaw`、OpenClaw workspace、OpenClaw 后台：目标是 OpenClaw。
   - 包含 `共享中台`、`shared`、`跨 agent`、`共享记忆`：目标是 shared 中台。

2. 再看路径证据。
   - `~/.hermes/`、`/root/.hermes/`：Hermes。
   - `/home/vany/openclaw-data/.openclaw/openclaw.json`、`/home/node/.openclaw/`：OpenClaw。
   - `/home/vany/openclaw-data/.openclaw/shared/`：shared 中台。

3. 如果目标仍不明确，先问：

   ```text
   这是改 Hermes 还是 OpenClaw？如果是当前这个 agent，我会按 Hermes 处理。
   ```

4. 禁止因为长期记忆里有 OpenClaw 配置路径，就默认操作 OpenClaw。

## Canonical Paths

| Target | Main config | Secrets / auth | Logs / runtime |
|---|---|---|---|
| Hermes | `~/.hermes/config.yaml` | `~/.hermes/.env`, `~/.hermes/auth.json` | `~/.hermes/logs/`, `~/.hermes/gateway_state.json` |
| OpenClaw | `/home/vany/openclaw-data/.openclaw/openclaw.json` | OpenClaw 自己的 agentDir / credential 文件 | `/home/vany/openclaw-data/.openclaw/` 下 runtime/workspace |
| shared 中台 | `/home/vany/openclaw-data/.openclaw/shared/manifest.yaml`, `AGENTS.md` | 禁止写入明文 secret | `shared/runtime/<agent>/` |

## Required Pre-Write Announcement

任何配置写入前，先明确一句：

```text
这次目标是 Hermes，我会修改 ~/.hermes/config.yaml。
```

或：

```text
这次目标是 OpenClaw，我会修改 /home/vany/openclaw-data/.openclaw/openclaw.json。
```

如果不能明确这句话，就不能写配置，必须先问用户。

## Safe Workflow

1. 识别目标系统。
2. 说明将要检查或修改的系统与文件。
3. 读取当前配置，只展示必要字段并隐藏 secret。
4. 写入前备份配置文件。
5. 做最小修改，不顺手改无关项。
6. 用配置解析或对应 CLI 验证。
7. 如配置需要重启才生效，说明并执行对应目标系统的重启方式。
8. 最后汇报：目标系统、修改文件、验证结果、是否需要用户动作。

## Common Pitfalls

1. 把“模型列表看不到”自动理解成 OpenClaw。
   - 修正：如果用户在 Hermes 会话中说“你这里 / 当前 agent”，默认 Hermes。

2. 看到记忆里有 OpenClaw base_url、token、openclaw.json，就直接改 OpenClaw。
   - 修正：记忆只能作为候选信息，不能替代本轮目标识别。

3. Hermes 配置与 OpenClaw 配置都存在时，不说明目标文件就写入。
   - 修正：写入前必须先声明目标系统和路径。

4. 把 shared 中台当成 OpenClaw 配置。
   - 修正：shared 是跨 agent 共享层，不是 OpenClaw 主配置；只写稳定事实、共享 skill、runtime 产物，不写 agent 私有 secret。

## Verification Checklist

- [ ] 已识别目标系统：Hermes / OpenClaw / shared / 不明确
- [ ] 不明确时已向用户追问
- [ ] 写入前已明确目标文件路径
- [ ] 没有把 secret 明文写入 shared
- [ ] 修改后已解析配置或执行对应 CLI 验证
- [ ] 最终回复包含目标系统、改动位置、验证结果
