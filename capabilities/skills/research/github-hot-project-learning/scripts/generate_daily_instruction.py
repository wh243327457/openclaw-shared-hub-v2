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
    failures = []
    for fb in feedbacks[-7:]:
        if fb.get('score', 0) < 16:
            for issue in fb.get('issues', []):
                failures.append({'date': fb.get('date'), 'issue': issue, 'score': fb.get('score')})
    return failures


def generate_enhanced_instructions(failures: list[dict]) -> str:
    if not failures:
        return '- 今日无特殊强化要求，按照标准流程执行学习。\n- 重点关注：深读项目的可迁移模式和实践价值。'
    instructions = ['### 今日强化重点']
    issue_counts: dict[str, int] = {}
    for f in failures:
        issue_counts[f['issue']] = issue_counts.get(f['issue'], 0) + 1
    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
        instructions.append(f'- **{issue}** (最近 7 天失败 {count} 次)')
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

**生成时间**: {date} | **来源**: Hermes 审计反馈系统 | **版本**: v1.0

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

必须包含：今日结论、项目速览(5-10个)、深读项目(每个含：一句话判断、解决的问题、架构/实现、可复用经验、可尝试实验、风险边界)、经验沉淀、明日继续。

### 2. 项目卡片
**文件**: `shared/runtime/openclaw/github-learning/projects/owner-repo.md`

必须包含：基本信息(链接/Stars/Forks/License/语言/最近更新)、一句话判断、核心价值、可迁移模式(含落地路径)、已知限制。

### 3. 经验沉淀
**文件**: `shared/runtime/openclaw/github-learning/lessons.md`

按日期追加，每条经验需具体可操作。

---

## 质量标准

### 硬性要求（不达标直接不合格）
1. **来源完整**: 仓库、README/docs/release/issue 链接齐全
2. **事实准确**: 关键事实可追溯，不臆测
3. **数据真实**: stars/forks/license 来自 GitHub API，标注查询时间
4. **深读完整**: 每个深读项目必须包含「可复用经验」和「风险边界」
5. **无截断**: 报告必须完整，不能中途截断

### 软性要求（扣分项）
1. **技术深度**: 讲清实现思路和边界
2. **可迁移性**: 能指出可复用的模式
3. **实践性**: 有可尝试的实验
4. **反宣传**: 能指出局限和不适用场景

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
