# 2026-06-04: v3 Deep Reading Fallback — Full Session Record

## Context

OpenClaw container was down. User requested deep project learning with detailed report.
Hermes executed the full pipeline using delegate_task subagents.

## What Happened

1. **Trending fetch**: delegate_task crawled github.com/trending, extracted 14 repos
2. **Selection**: headroom (+3,139★/day), open-notebook (24K★), trivy (35K★)
3. **Clone issues**: headroom and trivy clone timed out (>60s). Used GitHub API fallback.
4. **Deep reading**: 3 parallel delegate_task subagents, each reading 5-12 source files
5. **Report compilation**: 516 lines, 10 dimensions, 23/23 audit score
6. **Delivery**: Obsidian knowledge base + WeChat push

## Key Techniques

### GitHub API Fallback for Large Repos

When `git clone --depth 1` times out:
```bash
# Directory listing
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/" | jq -r '.[].name'

# File content (base64)
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/{path}" | jq -r '.content' | base64 -d
```

Unauthenticated: 60 req/hr. Sufficient for 3 projects × 10 files = 30 calls.

### Subagent Timeout Decomposition

When full-task delegate_task times out at 600s:
- Break into: (a) trending fetch, (b) per-project deep reads
- Each subagent 120-300s, well within 600s limit
- Compile report in parent session

### Deep Read Output Template (12 items)

Each project must include:
1. 一句话判断 2. 解决的问题 3. 架构/实现 4. repo tree
5. 关键源码文件 6. ⭐ 源码精读 (≥3 code blocks) 7. 依赖分析
8. 可复用经验 9. 可尝试实验 10. 风险边界
11. ⭐ Skill 升格判断 12. ⭐ 落地路径

### Audit v3 Scoring

10 dimensions, 23 points total:
- 结构完整 4 + 深读数量 3 + 源码深度 3 + 源码精读 2 + API 数据 2
- 可迁移经验 3 + 风险边界 2 + Skill 升格 2 + 落地路径 1 + 无幻觉 1
- PASS threshold: 16

## Results

| Project | Stars | Key Finding |
|---------|-------|-------------|
| headroom | 11,469 | ContentRouter + CCR reversible compression, Rust+PyO3 |
| open-notebook | 24,434 | LangGraph RAG fan-out, ContextBuilder, embedding mean-pooling |
| trivy | 35,566 | Artifact+Backend abstraction, 100+ Analyzer registration, WASM plugins |

## Lesson

When OpenClaw is unavailable, Hermes can produce equal-quality deep reads using
delegate_task with Claude Code subagents. The key is decomposition: don't try to
do everything in one subagent call.
