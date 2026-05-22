# Shared Recall Helper

`shared_recall.py` 是 claim-aware 的轻量召回助手，用于在没有向量库的情况下，从 `curated/memory/facts/` 与 `curated/memory/projects/` 中按 query 找相关长期上下文。

## 用法

```bash
cd <shared-root>
python3 scripts/shared_recall.py "共享中台 evidence" --json
python3 scripts/shared_recall.py "OpenClaw 每日学习"
```

## 匹配等级

| 等级 | 含义 |
|---|---|
| strong | active/approved + 命中充分 + 有证据线索 |
| weak | 有文本命中，但证据或状态不足 |
| conflict | disputed claim，只能作为冲突提示 |
| none | 低相关，不应默认注入上下文 |

## 安全边界

- 不读取 secret 文件。
- 不自动写 curated。
- 不依赖 embedding/vector 服务。
- `retired/superseded/disputed` 不作为强事实。
