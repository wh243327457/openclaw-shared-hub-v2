# 配置目标路由校正会话 · 2026-05-16

## 问题描述

用户抱怨：每次让 Hermes 改配置，Hermes 都先改 OpenClaw，而不是先问或默认改 Hermes。

根因：记忆里 OpenClaw 配置路径（`/home/vany/openclaw-data/.openclaw/openclaw.json`）比 Hermes 路径更显眼，导致目标识别被记忆劫持，跳过了 skill 中规定的"先问目标"步骤。

## 校正措施

### 1. config-target-routing skill 更新

触发条件加严：
- **之前**："用户只说'改配置 / 重启'时才触发"
- **之后**："用户只说'改配置 / 重启 / 你这里 / 当前 agent / 你的配置'，没有明确说 OpenClaw"就触发

目标识别规则强化：
- 用户说"你 / 当前 agent / 当前 CLI / 当前网关 / Hermes / 这个 agent" → **直接默认 Hermes**，不用问
- 只有用户**明确**说 OpenClaw 或给出其路径时才操作 OpenClaw
- 记忆中 OpenClaw 配置路径更显眼 → 不能作为默认目标的理由

### 2. shared-memory-bridge skill 更新

配置目标识别章节增加：
- 常见触发词与预期目标表（含"Hermes"行默认 Hermes）
- 配置写入前强制自检清单（声明目标系统+文件路径）

### 3. shared 层 config-target-routing skill

新增 standalone skill：`capabilities/skills/foundation/config-target-routing/SKILL.md`
- 独立于 Hermes 本地 skill，可在 Hermes/OpenClaw 间共享
- 登记在 `capabilities/manifests/shared-skills.yaml`

## 关键教训

1. **路由不能依赖记忆中的路径显著性** — 如果某条路径在记忆里出现频率高，它就会变成隐性默认，绕过显式路由规则。需要用 skill 的触发条件强制做本轮自检。
2. **用户抱怨"你总是 X"是强烈的 skill 信号** — 说明问题重复出现，不是偶发，skill 需要记录防止再犯。
3. **配置类任务的默认目标必须显式声明** — 不能让用户靠抱怨来纠正，要从机制上保证每次配置写入前都有目标声明。

## 验证方法

用户下次说"改配置"时：
- Hermes 应先声明："目标系统：Hermes（因为你说的是'你'）"
- 只有用户说"OpenClaw"或给路径时才切 OpenClaw
- 不再出现"先改 OpenClaw 再问"的情况