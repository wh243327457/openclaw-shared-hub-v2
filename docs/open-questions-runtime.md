# Open Questions Runtime

Open questions 用于记录“值得后续复核，但现在证据不足/不应直接晋升”的问题队列。

路径：`runtime/hermes/open-questions/questions.json`

## 用法

```bash
cd <shared-root>
python3 scripts/open_questions.py list --json
python3 scripts/open_questions.py add --topic shared.evidence --question "哪些旧 facts 值得优先补 evidence_refs？" --source phase4
python3 scripts/open_questions.py export
```

## 边界

- runtime-only，不是 curated memory。
- 不自动触发修复或配置修改。
- 每周治理复盘时可人工挑选问题转成 candidate。
