# Config-Target-Routing Correction Session

**Date**: 2026-05-16
**Context**: 用户抱怨 Hermes 每次改配置都默认改 OpenClaw，不是直接改 Hermes，也不是先问用户

---

## 用户原话

> "为什么每次我让你改配置，你都是先改openclaw的，不是直接改Hermes的？或者咨询我要改哪个？"

---

## 问题根因

虽然 `config-target-routing` 规则已经存在于 `shared-memory-bridge` SKILL.md 中，且 `AGENTS.md` 也有明确说明，但实际执行时没有遵守。

规则本身是对的，执行层面出了问题：
1. 规则表述不够强制（用词是"默认"而非"必须"）
2. 没有配置写入前的强制自检清单
3. 没有明确"违反即算错误"的表述

---

## 修复内容

更新了 `shared-memory-bridge` SKILL.md：

1. 将配置路由规则表述从"默认"改为"强制路由规则（必须遵守，违反即算错误）"
2. 新增"配置写入前强制自检清单"：操作前必须声明目标系统、目标文件、操作方式
3. 新增"常见触发词与预期目标"表格
4. 补充了 `config-target-routing` 技能的 manifest 登记信息

---

## 关键规则（必须遵守）

| 用户说 | 默认目标 | 正确文件 |
|---|---|---|
| "你 / Hermes / 当前 agent / 这个 agent / 当前 CLI" | Hermes | `~/.hermes/config.yaml` |
| "你 / Hermes 的模型 / 你用的模型" | Hermes | `~/.hermes/config.yaml` |
| "Hermes gateway / 你的 gateway" | Hermes | `~/.hermes/hermes-agent/` |
| "OpenClaw / openclaw 的配置" | OpenClaw | `/home/vany/openclaw-data/.openclaw/openclaw.json` |
| "shared / 共享中台 / 跨 agent" | shared 层 | `shared/` 根目录 |
| 只有"改配置"且无上下文 | **必须先问** | — |

---

## 教训

规则写在 SKILL.md 里不代表会被遵守。涉及跨系统高风险操作的规则，需要：
1. 明确的"禁止/必须"措辞，而非模糊的"默认/通常"
2. 操作前的强制检查清单
3. 具体的触发词对照表
