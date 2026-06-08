# ECC: 多 Agent 通用 Harness 操作系统

**学习日期**: 2026-06-08
**来源**: affaan-m/ECC (209k stars)
**状态**: curated

## 核心价值
- 261 skills + 64 agents + 84 commands 的统一管理
- agent.yaml 声明式 manifest (spec_version 0.1.0)
- 支持 Claude Code / Codex / Cursor / OpenCode / Gemini / Qwen / Trae / Zed / Kiro 等多 Agent

## 可迁移模式
1. **Skill 包管理**: 像操作系统一样管理 Agent 技能
2. **多 runtime 适配**: 一套 skills 适配多个 Agent runtime
3. **声明式配置**: agent.yaml 标准化配置格式

## 落地建议
- OpenClaw 可参考 ECC 的 skill 包管理架构
- Hermes 可借鉴 agent.yaml 的声明式配置模式
