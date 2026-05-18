---
name: priority-backlog-clearance
description: 按优先级依次收口积压任务的标准工作流
version: "1.0"
agent: hermes, openclaw, future
category: foundation
---

# priority-backlog-clearance

## 触发条件

- 用户问"还有什么没完成"或"推进一下"
- 积压了多个待办事项需要收口
- 项目进度需要更新

## 工作流

### 第一步: 快速盘点
1. 读取共享中台项目状态 `curated/memory/projects/*.md`
2. 检查最近 inbox daily 记录
3. 检查当前系统状态（服务、网络、工具可用性）

### 第二步: 排序
优先级标准：
1. **基础设施故障** — 影响所有后续任务
2. **远端同步阻塞** — 本地已就绪只差推送
3. **数据/记忆漏洞** — 缺少关键信息
4. **自动化缺失** — 手动重复性工作
5. **工具链恢复** — 提升执行效率
6. **新能力沉淀** — 知识与 skill 整理

### 第三步: 执行
- 用户说"只要最终报告"时：不汇报中间过程，批量执行后统一汇报
- 遇到阻塞时：记录根因，跳过并继续下一个优先级
- 每完成一个优先级后更新项目状态

### 第四步: 验证
- 运行 verify_bridge.py 确认无破坏
- 运行 promoter.py 刷新状态索引
- 检查 inbox 是否有新记录

## 输出格式

最终汇报应包含：
- 完成了哪些、失败了哪些
- 当前完成度
- 仍待闭环的事项
- 下一步建议

## 自我完善工作流（定期自主迭代）

当用户说“自我完善 / 自我迭代 / 把系统优化一下”时，按以下顺序执行：

### 第一步：审计
1. 读 `runtime/hermes/autonomous-learning/state.json`
2. 读 `runtime/hermes/autonomous-learning/learning-backlog.json`
3. 读 `scripts/verify_bridge.py` 最新输出
4. 读 `scripts/promoter.py --dry-run` 最新输出

### 第二步：可安全自动处理的项（P0/P1）
以下类型可以自主完成，不需要用户审批：
- 旧 fact 缺 metadata frontmatter（LEGACY_FACT_METADATA_MISSING）
- 脚本/测试一致性检查（验证测试覆盖是否与文档同步）
- 结构完整性检查（verify_bridge 所有路径是否存在）
- JSON 状态文件格式验证

**禁止自动处理**（必须保留人工审批边界）：
- curated 自动晋升
- 事实裁决（conflict resolution）
- secret 明文写入
- 治理策略变更

### 第三步：运行维护链路
```bash
# 顺序固定：测试 → dry-run → promoter apply → verify → governance scan
python3 -m unittest tests/test_fact_governance.py
python3 scripts/promoter.py --dry-run
python3 scripts/promoter.py
python3 scripts/verify_bridge.py
python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10
```

### 第四步：落盘
- 写 `inbox/hermes/daily/YYYY-MM-DD.md`（原始记录）
- 更新 `runtime/hermes/autonomous-learning/state.json`（状态变更）
- 更新 `runtime/hermes/autonomous-learning/learning-backlog.json`（backlog 变更）

### 第五步：汇报
汇报格式：
- 完成了哪些 / 失败了哪些
- 当前系统状态（治理模式、健康检查结果）
- 仍待闭环的项（需要用户审批）
- 下一步建议

---

## 当前使用场景

- 共享中台 v2 运维
- 多 agent 协作收口
- 定期自我迭代与整理
