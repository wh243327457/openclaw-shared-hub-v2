#!/usr/bin/env python3
"""审计反馈写入器。

在 Hermes 审计失败时，实时将失败点写入模板的审计反馈区。
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
TEMPLATE_PATH = 'capabilities/skills/research/github-hot-project-learning/templates/daily-instruction.md'


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='审计日期')
    parser.add_argument('--score', type=int, required=True, help='审计得分 (0-20)')
    parser.add_argument('--issues', nargs='+', help='失败点列表')
    parser.add_argument('--strengths', nargs='+', help='优点列表')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def load_audit_feedback(shared_root: Path) -> dict[str, Any]:
    """加载历史审计反馈。"""
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    if not feedback_file.exists():
        return {'feedbacks': [], 'failures': []}
    
    try:
        with feedback_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'加载审计反馈失败: {e}', file=sys.stderr)
        return {'feedbacks': [], 'failures': []}


def save_audit_feedback(shared_root: Path, data: dict[str, Any]) -> None:
    """保存审计反馈。"""
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    feedback_file.parent.mkdir(parents=True, exist_ok=True)
    
    with feedback_file.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_template_feedback(
    shared_root: Path,
    date: str,
    score: int,
    issues: list[str],
    strengths: list[str],
    feedbacks: list[dict],
    dry_run: bool = False
) -> None:
    """更新模板中的审计反馈区。"""
    template_file = shared_root / TEMPLATE_PATH
    if not template_file.exists():
        print(f'模板文件不存在: {template_file}', file=sys.stderr)
        return
    
    # 读取模板内容
    with template_file.open('r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成反馈内容
    feedback_section = f'''### 最近审计反馈

**日期**: {date}
**得分**: {score}/20
**状态**: {'✅ 通过' if score >= 16 else '❌ 需要改进'}

**优点**:
{chr(10).join(f'- {s}' for s in strengths) if strengths else '- 暂无'}

**问题**:
{chr(10).join(f'- {i}' for i in issues) if issues else '- 暂无'}

---

### 历史失败点

{generate_failure_history(feedbacks)}

---

### 强化指令

{generate_enhanced_instructions(feedbacks)}
'''
    
    # 替换模板中的审计反馈区
    import re
    pattern = r'(## 审计反馈区（Hermes 自动更新）.*?### 最近审计反馈\n\n).*?(### 历史失败点\n\n).*?(### 强化指令\n\n)'
    replacement = f'\\1{feedback_section}'
    
    # 简单替换：找到标记区域并替换
    if '### 最近审计反馈' in content:
        # 分割内容
        parts = content.split('### 最近审计反馈')
        if len(parts) >= 2:
            # 找到结束标记
            end_marker = '---\n\n## 使用说明'
            if end_marker in parts[1]:
                after_feedback = parts[1].split(end_marker)[1]
                content = parts[0] + feedback_section + end_marker + after_feedback
    
    # 写回模板
    if not dry_run:
        with template_file.open('w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ 模板已更新: {template_file}')


def generate_failure_history(feedbacks: list[dict]) -> str:
    """生成历史失败点摘要。"""
    if not feedbacks:
        return '暂无历史失败点。'
    
    failures = []
    for fb in feedbacks[-7:]:  # 最近 7 天
        if fb.get('score', 0) < 16:
            issues = fb.get('issues', [])
            for issue in issues:
                failures.append(f"- {fb['date']}: {issue} (得分: {fb['score']})")
    
    return '\n'.join(failures[-5:]) if failures else '最近 7 天无失败记录。'


def generate_enhanced_instructions(feedbacks: list[dict]) -> str:
    """生成强化指令。"""
    if not feedbacks:
        return '- 今日无特殊强化要求。'
    
    # 分析最近失败点
    recent_failures = []
    for fb in feedbacks[-7:]:
        if fb.get('score', 0) < 16:
            recent_failures.extend(fb.get('issues', []))
    
    if not recent_failures:
        return '- 最近无失败记录，保持标准流程。'
    
    # 统计频率
    from collections import Counter
    issue_counts = Counter(recent_failures)
    
    instructions = ['### 今日强化重点', '']
    for issue, count in issue_counts.most_common(3):
        instructions.append(f'- **{issue}** (最近 7 天出现 {count} 次)')
    
    return '\n'.join(instructions)


def main() -> None:
    args = parse_args()
    date = args.date
    score = args.score
    issues = args.issues or []
    strengths = args.strengths or []
    
    print(f'记录 {date} 审计结果 (得分: {score}/20)...')
    
    # 1. 加载历史反馈
    feedback_data = load_audit_feedback(args.shared_root)
    feedbacks = feedback_data.get('feedbacks', [])
    
    # 2. 添加本次反馈
    new_feedback = {
        'date': date,
        'score': score,
        'issues': issues,
        'strengths': strengths,
        'timestamp': datetime.now(TZ).isoformat()
    }
    feedbacks.append(new_feedback)
    
    # 3. 更新历史失败点
    if score < 16:
        feedback_data.setdefault('failures', []).append({
            'date': date,
            'issues': issues
        })
    
    # 4. 保存反馈
    feedback_data['feedbacks'] = feedbacks
    if not args.dry_run:
        save_audit_feedback(args.shared_root, feedback_data)
        print(f'✅ 审计反馈已保存')
    
    # 5. 更新模板
    update_template_feedback(
        args.shared_root,
        date,
        score,
        issues,
        strengths,
        feedbacks,
        args.dry_run
    )
    
    # 6. 输出结果
    print(f'\n📊 审计结果:')
    print(f'   - 得分: {score}/20')
    print(f'   - 状态: {"通过" if score >= 16 else "需要改进"}')
    if issues:
        print(f'   - 问题: {", ".join(issues)}')
    if strengths:
        print(f'   - 优点: {", ".join(strengths)}')


if __name__ == '__main__':
    main()
