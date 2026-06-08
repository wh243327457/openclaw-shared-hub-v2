# agent.yaml: Agent 配置文件标准化趋势

**学习日期**: 2026-06-08
**来源**: ECC + GSD 等多个项目
**状态**: curated

## 核心价值
- spec_version=0.1.0 正在成为行业规范
- 声明式配置 Agent 的 skills、commands、hooks

## 标准字段
- name: Agent 名称
- description: Agent 描述
- skills: 技能列表
- commands: 命令列表
- hooks: 钩子列表
- spec_version: 规范版本

## 落地建议
- OpenClaw 可采用 agent.yaml 作为标准配置格式
- Hermes 可参考 agent.yaml 设计 Agent 配置规范
