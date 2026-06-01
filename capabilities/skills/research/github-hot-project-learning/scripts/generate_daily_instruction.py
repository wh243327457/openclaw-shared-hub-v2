#!/usr/bin/env python3
"""生成 GitHub 热门项目每日学习指令。

读取历史审计反馈，分析昨日失败点，生成今日强化指令。
输出到 shared/runtime/hermes/github-hot-project-learning/instruction.md
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DEFAULT_SHARED_ROOT = Path('/home/vany/agent/shared')
PIPELINE = 'github-hot-project-learning'
TZ = timezone(timedelta(hours=8))

DEFAULT_TECH_STACK = ['Go', 'Rust', 'Python', 'TypeScript', 'Kubernetes', 'Docker', 'Terraform', 'AI/ML', 'LLM', 'WebAssembly']
DEFAULT_DOMAINS = ['DevOps', 'AI/ML', '云原生', '安全', '性能优化', '分布式系统', '数据库', 'Web 框架', 'CLI 工具']


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst())
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def read_audit_feedback(shared_root: Path) -> dict[str, Any]:
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    if not feedback_file.exists():
        return {'feedbacks': [], 'failures': []}
    try:
        with feedback_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'feedbacks': [], 'failures': []}


def analyze_failures(feedbacks: list[dict]) -> list[dict]:
    """分析最近 7 天的审计问题（含通过但有扣分项的情况）。"""
    failures = []
    for fb in feedbacks[-7:]:
        score = fb.get('score', 0)
        issues = fb.get('issues', [])
        # 过滤掉"无"和空值
        real_issues = [i for i in issues if i and i != '无']
        if real_issues:
            for issue in real_issues:
                failures.append({
                    'date': fb.get('date'),
                    'issue': issue,
                    'score': score,
                    'passed': score >= 16,
                })
    return failures


def generate_enhanced_instructions(failures: list[dict]) -> str:
    if not failures:
        return '- 今日无特殊强化要求，按照标准流程执行学习。\n- 重点关注：深读项目的可迁移模式和实践价值。'
    instructions = ['### 今日强化重点']
    # 统计高频问题（含通过但重复出现的问题）
    issue_counts: dict[str, int] = {}
    for f in failures:
        issue_counts[f['issue']] = issue_counts.get(f['issue'], 0) + 1
    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        severity = '🔴' if count >= 3 else '🟡' if count >= 2 else '⚪'
        instructions.append(f'- {severity} **{issue}**（最近 7 天出现 {count} 次）')

    # 基于高频问题生成具体强化动作
    action_map = {
        '缺少 stars 数据': '每个深读项目必须用 GitHub API 查询 stars/forks/license，写入报告头部',
        '缺少 license 信息': '每个项目必须标注 License 类型（MIT/Apache-2.0/GPL 等），null 时标注"无 license"',
        '缺少 skill 升格判断': '每个深读项目必须有「Skill 升格判断」章节：可直接迁移 / 需二次验证 / 暂不沉淀',
        '源码深度不足': '每个深读项目必须包含：repo tree 摘要、关键源码文件列表、架构/数据流分析',
        '完全没有源码级分析': '禁止只复述 README，必须深入源码结构和实现细节',
        '可迁移经验偏少': '至少提炼 3 条「当……时，应优先……」格式的可迁移经验',
        '风险边界不完整': '每个项目必须覆盖：License、安全风险、维护活跃度、不适用场景',
    }
    actions = []
    for issue in issue_counts:
        if issue in action_map:
            actions.append(f'- ✅ {action_map[issue]}')
    if actions:
        instructions.append('')
        instructions.append('### 具体强化动作')
        instructions.extend(actions)

    return '\n'.join(instructions)


def generate_daily_goals(date: str, failures: list[dict]) -> str:
    lines = [f'## {date} 学习目标', '',
             '1. **发现**: 找到 3-5 个值得深读的热门项目',
             '2. **深读**: 完成 2-3 个项目的深度分析',
             '3. **沉淀**: 提取至少 3 条可复用经验',
             '4. **实践**: 设计 1 个可尝试的实验']
    if failures:
        lines += ['', '### 强化目标'] + [f'- 重点改进: {f["issue"]}' for f in failures[:2]]
    return '\n'.join(lines)


def build_instruction(date: str, goals: str, tech_stack: list[str], domains: list[str],
                      required_projects: str, audit_feedback: str, historical_failures: str,
                      enhanced_instructions: str) -> str:
    ts_list = '\n'.join(f'- {t}' for t in tech_stack)
    d_list = '\n'.join(f'- {d}' for d in domains)
    return f'''# GitHub 热门项目每日学习指令

**生成时间**: {date} | **来源**: Hermes 审计反馈系统 | **版本**: v2.0

---

## 今日学习目标

{goals}

---

## 学习范围

### 推荐技术栈
{ts_list}

### 推荐领域
{d_list}

---

## 必读项目

{required_projects}

---

## 产出要求

### 1. 学习报告
**文件**: `shared/inbox/openclaw/daily/{date}.md`

必须包含：
- **今日结论**（一句话总结今日学习主线）
- **项目速览**（5-10 个简要列出，含 Stars/Language/License）
- **深读项目**（每个必须包含以下全部内容）：
  - 一句话判断：为什么值得学
  - 解决的问题：替代了什么旧做法
  - **架构/实现**：核心模块、数据流、关键依赖
  - **repo tree 摘要**：目录结构 + 每层用途
  - **关键源码文件**：文件路径 + 用途 + 关键内容摘要
  - **可复用经验**：至少 1 条「当……时，应优先……」格式
  - **可尝试实验**：30 分钟内能做的最小 demo
  - **风险边界**：license、维护活跃度、安全风险、不适用场景
  - **⭐ Skill 升格判断**：可直接迁移 / 需二次验证 / 暂不沉淀（必须明确，禁止空话）
- **经验沉淀**（至少 3 条通用经验）
- **明日继续**（下一步最小动作）
- **候选反哺**（candidate facts / skills / open questions）

### 2. 项目卡片
**文件**: `shared/runtime/openclaw/github-learning/projects/owner-repo.md`

必须包含：
- 基本信息（链接、Stars、Forks、License、语言、最近更新）
- 一句话判断
- 核心价值
- 可迁移模式（含落地路径）
- 已知限制

### 3. 经验沉淀
**文件**: `shared/runtime/openclaw/github-learning/lessons.md`

按日期追加，每条经验需具体可操作。

---

## ⚠️ 质量标准（2026-05-30 强化版）

### 硬性要求（不达标直接不合格，16 分返工线）

| # | 维度 | 分值 | 要求 |
|---|------|------|------|
| 1 | 结构完整 | 4 | 五个必需章节齐全 |
| 2 | 深读数量 | 3 | ≥2 个深读项目 |
| 3 | **源码深度** | 3 | repo tree + 关键文件 + 架构分析 + 代码块 |
| 4 | **API 数据** | 2 | stars + license 来自 GitHub API |
| 5 | 可迁移经验 | 3 | ≥3 条「当……时，应优先……」格式 |
| 6 | 风险边界 | 2 | license + 安全 + 局限性 + 维护活跃度 |
| 7 | **Skill 升格** | 2 | 每个项目明确：可直接迁移 / 需二次验证 / 暂不沉淀 |
| 8 | 无幻觉 | 1 | 无可疑 stars 数字或未验证声明 |

### 禁止事项

- ❌ 只复述 README，不深入源码
- ❌ 没有 stars/license 实时数据
- ❌ 缺少 skill 升格判断
- ❌ 可迁移经验少于 3 条
- ❌ 风险边界只写一句话

---

## 深度学习与安全反哺要求

每日学习不只做项目摘抄，必须采用"深挖 → 机制抽象 → 反哺建议 → 安全边界"的结构。

### A. 深挖对象
- 明确今日深挖对象是项目、工具、机制还是故障案例。
- 每个深读对象至少核验 README/docs/release/issues 中的 2 类来源；关键 repo 元数据必须来自 GitHub API。

### B. 可验证证据
- 给出 GitHub 链接、核心文件/目录、版本/提交或查询时间。
- 不确定的结论必须标注"待核验"，不得编造。

### C. 核心机制
- 不只罗列功能；必须抽象出可迁移模式。
- 优先使用这种句式：`当……时，应优先……，因为……，边界是……`。

### D. 反哺到现有体系
每个深读项目至少判断一次是否可反馈到：
- shared curated memory / facts / projects
- shared skill / workflow
- Hermes 审计流程
- OpenClaw 每日学习 / 每日巡检
- runtime POC / open questions

### E. 安全边界
必须明确哪些内容不能自动执行：
- 不自动改配置、模型、provider、cron、secret。
- 不直接写 curated active fact，只提出 candidate。
- 不复制 license 不明或不兼容项目源码。
- 不从 assistant-authored prose 生成用户事实。
- 巡检类建议只输出风险、证据、影响、建议动作，不自动修复。

### F. 候选反哺
在日报末尾新增"候选反哺"小节，按以下格式输出：

```markdown
## 候选反哺

### Candidate Facts
- [ ] topic: ... | evidence: ... | 建议: create/update/retire/dispute | 安全级别: low/medium/high

### Candidate Skills / Workflow
- [ ] 名称: ... | 可复用场景: ... | 是否建议 shared: yes/no | 原因: ...

### Candidate Open Questions
- [ ] 问题: ... | reason: gap/conflict/stale/adaptation | priority: low/medium/high

### 不应自动落地
- ...
```

### G. 输出约束
- 候选反哺只作为 Hermes 二轮审计输入，不代表已落库。
- 如果触及安全/密钥/配置，必须只写变量名或占位符，不写明文值。
- 受 cron summary 截断限制，核心结论要短；完整证据应尽量写入 shared inbox/runtime 产物。

---

## 审计反馈区（Hermes 自动更新）

> 以下内容由 Hermes 审计后自动写入，请勿手动修改。

### 最近审计反馈
{audit_feedback}

### 历史失败点
{historical_failures}

### 强化指令
{enhanced_instructions}

---

## 版本历史
| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | {date} | 强化审计标准：源码深度、API 数据、skill 升格判断 |
| v1.0 | {date} | 初始版本 |
'''


def main() -> None:
    args = parse_args()
    date = args.date
    shared_root = args.shared_root

    feedback_data = read_audit_feedback(shared_root)
    feedbacks = feedback_data.get('feedbacks', [])
    failures = analyze_failures(feedbacks)

    goals = generate_daily_goals(date, failures)
    enhanced = generate_enhanced_instructions(failures)
    audit_fb = '暂无最近审计反馈' if not feedbacks else f'最近 {len(feedbacks)} 条反馈已记录'
    hist_fail = '暂无历史失败点' if not failures else '\n'.join(
        f'- {f["date"]}: {f["issue"]} (得分: {f["score"]})' for f in failures[:5])

    instruction = build_instruction(date, goals, DEFAULT_TECH_STACK, DEFAULT_DOMAINS,
                                    '今日无指定必读项目，由 OpenClaw 自主发现热门项目。',
                                    audit_fb, hist_fail, enhanced)

    if args.dry_run:
        print(instruction)
    else:
        output_dir = shared_root / 'runtime' / 'hermes' / PIPELINE
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'instruction.md'
        with output_file.open('w', encoding='utf-8') as f:
            f.write(instruction)
        print(f'✅ 指令已生成: {output_file}')


if __name__ == '__main__':
    main()
