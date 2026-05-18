# promote log template

用于记录一次 inbox → curated 晋升复盘。

## 基本信息

- 日期:
- 复盘人 / 总控:
- 扫描命令:
- 扫描范围:
- 验证命令:

## 候选条目

### 1. 候选标题

- 状态: candidate | accepted | rejected | deferred | duplicate
- 来源 agent:
- 来源路径:
- 来源证据:
- 风险检查:
  - secret: clear | redacted | blocked
  - duplicate: no | yes, covered by `...`
  - confidence: high | medium | low
- 建议目标:
- 实际写入:
- 备注:

## 本次写入 curated

- `curated/memory/facts/...`
- `curated/memory/projects/...`

## 本次拒绝 / 暂缓

- 条目:
- 原因:

## 验收结果

- `python3 scripts/promoter.py --dry-run --scan-promote-candidates --recent-limit 10`: pass | fail
- `python3 scripts/verify_bridge.py`: pass | fail

## 后续动作

- [ ] 更新 MEMORY.md 索引 / 自动状态块
- [ ] 更新项目状态文件
- [ ] 下次复盘日期
