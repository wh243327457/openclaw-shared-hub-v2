# GSD: Spec-driven 多 Phase Agent Pipeline

**学习日期**: 2026-06-08
**来源**: gsd-build/get-shit-done (64k stars)
**状态**: curated

## 核心价值
- 90+ workflows + 40+ agents 的任务编排
- 显式支持 Hermes runtime
- Orchestrator coordinates, not executes

## 可迁移模式
1. **Spec-driven**: 用 spec 文件定义任务，Agent 按 spec 执行
2. **多 Phase Pipeline**: 任务分阶段执行，每阶段有明确产出
3. **Orchestrator 模式**: Orchestrator 只负责发任务和收结果，不干预执行

## 落地建议
- Hermes Kanban 可参考 GSD 的 spec-driven 模式
- 自主学习系统可借鉴多 Phase Pipeline 设计
