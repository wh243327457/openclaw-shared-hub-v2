#!/usr/bin/env python3
"""生成 GitHub 热门项目每日学习指令。

读取历史审计反馈，分析昨日失败点，生成今日强化指令。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# 常量
DEFAULT_SHARED_ROOT = Path('/home/vany/agent/.openclaw/shared')
PIPELINE = 'github-hot-project-learning'
TZ = timezone(timedelta(hours=8))

# 默认技术栈
DEFAULT_TECH_STACK = [
    'Go', 'Rust', 'Python', 'TypeScript',
    'Kubernetes', 'Docker', 'Terraform',
    'AI/ML', 'LLM', 'WebAssembly'
]

# 默认领域
DEFAULT_DOMAINS = [
    'DevOps', 'AI/ML', '云原生', '安全', '性能优化',
    '分布式系统', '数据库', 'Web 框架', 'CLI 工具'
]


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='目标日期 YYYY-MM-DD')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不写文件')
    return parser.parse_args()


def read_audit_feedback(shared_root: Path) -> dict[str, Any]:
    """读取历史审计反馈。"""
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    if not feedback_file.exists():
        return {'feedbacks': [], 'failures': []}
    
    try:
        with feedback_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'读取审计反馈失败: {e}', file=sys.stderr)
        return {'feedbacks': [], 'failures': []}


def analyze_failures(feedbacks: list[dict]) -> list[dict]:
    """分析历史失败点，提取需要强化的方面。"""
    failures = []
    
    for fb in feedbacks[-7:]:  # 最近 7 天
        if fb.get('score', 0) < 16:  # 低于 16 分
            for issue in fb.get('issues', []):
                failures.append({
                    'date': fb.get('date'),
                    'issue': issue,
                    'score': fb.get('score')
                })
    
    return failures


def generate_enhanced_instructions(failures: list[dict]) -> str:
    """根据失败点生成强化指令。"""
    if not failures:
        return """- 今日无特殊强化要求，按照标准流程执行学习。
- 重点关注：深读项目的可迁移模式和实践价值。"""
    
    instructions = []
    instructions.append('### 今日强化重点')
    
    # 统计失败类型
    issue_counts: dict[str, int] = {}
    for f in failures:
        issue = f['issue']
        issue_counts[issue] = issue_counts.get(issue, 0) + 1
    
    # 按频率排序
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
    
    for issue, count in sorted_issues[:3]:  # 最多 3 个强化点
        instructions.append(f'- **{issue}** (最近 7 天失败 {count} 次)')
    
    return '\n'.join(instructions)


def generate_tech_stack(goals: str) -> list[str]:
    """根据学习目标生成推荐技术栈。"""
    # 简单实现：返回默认栈
    return DEFAULT_TECH_STACK


def generate_domains(goals: str) -> list[str]:
    """根据学习目标生成推荐领域。"""
    return DEFAULT_DOMAINS


def generate_daily_goals(date: str, failures: list[dict]) -> str:
    """生成今日学习目标。"""
    goals = []
    goals.append(f'## {date} 学习目标')
    goals.append('')
    goals.append('1. **发现**: 找到 3-5 个值得深读的热门项目')
    goals.append('2. **深读**: 完成 2-3 个项目的深度分析')
    goals.append('3. **沉淀**: 提取至少 3 条可复用经验')
    goals.append('4. **实践**: 设计 1 个可尝试的实验')
    
    if failures:
        goals.append('')
        goals.append('### 强化目标')
        for f in failures[:2]:
            goals.append(f'- 重点改进: {f["issue"]}')
    
    return '\n'.join(goals)


def generate_instruction_template(
    date: str,
    goals: str,
    tech_stack: list[str],
    domains: list[str],
    required_projects: str,
    audit_feedback: str,
    historical_failures: str,
    enhanced_instructions: str
) -> str:
    """生成完整的指令模板。"""
    template = f'''# GitHub 热门项目每日学习指令

**生成时间**: {date}
**生成来源**: Hermes 审计反馈系统
**版本**: v1.0

---

## 今日学习目标

{goals}

---

## 学习范围

### 推荐技术栈

{chr(10).join(f'- {t}' for t in tech_stack)}

### 推荐领域

{chr(10).join(f'- {d}' for d in domains)}

---

## 必读项目

{required_projects}

---

## 产出要求

### 1. 学习报告

**文件**: `shared/inbox/openclaw/daily/{date}.md`

**格式要求**:
```markdown
# GitHub 热门项目学习日报 - {date}

## 今日结论
一句话总结今日学习成果。

## 项目速览
简要列出今日发现的项目（5-10 个）。

## 深读项目
### 项目 1: owner/repo
- **一句话判断**: 为什么值得学
- **解决的问题**: 替代了什么旧做法
- **架构/实现**: 核心模块、数据流
- **可复用经验**: 至少 1 条「当……时，应优先……」格式
- **可尝试实验**: 30 分钟内能做的最小 demo
- **风险边界**: license、维护活跃度、安全风险

### 项目 2: ...
...

## 经验沉淀
今日学到的通用经验（不限于单个项目）。

## 明日继续
下一步最小动作。
```

### 2. 项目卡片

**文件**: `shared/runtime/openclaw/github-learning/projects/owner-repo.md`

**格式要求**:
```markdown
# owner/repo

## 基本信息
- 链接: https://github.com/owner/repo
- Stars: XXX
- Forks: XXX
- License: XXX
- 语言: XXX
- 最近更新: YYYY-MM-DD

## 一句话判断
为什么值得学。

## 核心价值
- 解决什么问题
- 有什么独特之处

## 可迁移模式
1. 模式名称: 具体描述 + 落地路径
2. ...

## 已知限制
1. ...
```

### 3. 经验沉淀

**文件**: `shared/runtime/openclaw/github-learning/lessons.md`

**格式要求**:
```markdown
# 学习经验沉淀

## 2026-05

### {date}
- 经验 1: ...
- 经验 2: ...
```

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

## 使用说明

### OpenClaw 学习流程

1. **读取本指令**: 确认今日学习目标和范围
2. **执行学习**: 按照产出要求完成学习
3. **提交产出**: 确保文件写入正确路径
4. **自检**: 对照质量标准自查

### Hermes 审计流程

1. **读取产出**: 检查 OpenClaw 的学习产出
2. **评分**: 按照质量标准评分（20 分制）
3. **反馈**: 写入审计反馈区
4. **强化**: 更新强化指令

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | {date} | 初始版本 |
'''
    return template


def write_instruction(shared_root: Path, content: str, date: str) -> Path:
    """写入指令文件。"""
    output_dir = shared_root / 'runtime' / 'hermes' / PIPELINE
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'instruction.md'
    with output_file.open('w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file


def main() -> None:
    args = parse_args()
    date = args.date
    shared_root = args.shared_root
    
    print(f'生成 {date} 学习指令...')
    
    # 1. 读取历史审计反馈
    feedback_data = read_audit_feedback(shared_root)
    feedbacks = feedback_data.get('feedbacks', [])
    
    # 2. 分析失败点
    failures = analyze_failures(feedbacks)
    
    # 3. 生成今日目标
    goals = generate_daily_goals(date, failures)
    
    # 4. 生成技术栈和领域
    tech_stack = generate_tech_stack(goals)
    domains = generate_domains(goals)
    
    # 5. 生成强化指令
    enhanced_instructions = generate_enhanced_instructions(failures)
    
    # 6. 构建审计反馈摘要
    audit_feedback = '暂无最近审计反馈' if not feedbacks else f'最近 {len(feedbacks)} 条反馈已记录'
    
    # 7. 构建历史失败点摘要
    historical_failures = '暂无历史失败点' if not failures else '\n'.join([
        f'- {f["date"]}: {f["issue"]} (得分: {f["score"]})'
        for f in failures[:5]
    ])
    
    # 8. 必读项目（默认为空，由 Hermes 或用户指定）
    required_projects = '今日无指定必读项目，由 OpenClaw 自主发现热门项目。'
    
    # 9. 生成指令模板
    instruction = generate_instruction_template(
        date=date,
        goals=goals,
        tech_stack=tech_stack,
        domains=domains,
        required_projects=required_projects,
        audit_feedback=audit_feedback,
        historical_failures=historical_failures,
        enhanced_instructions=enhanced_instructions
    )
    
    # 10. 写入文件
    if args.dry_run:
        print(instruction)
        print('\n[DRY-RUN] 未写入文件')
    else:
        output_file = write_instruction(shared_root, instruction, date)
        print(f'✅ 指令已生成: {output_file}')
        print(f'   - 失败点分析: {len(failures)} 个')
        print(f'   - 强化指令: 已生成')


if __name__ == '__main__':
    main()
