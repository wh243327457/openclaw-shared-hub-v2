#!/usr/bin/env python3
"""审计反馈写入器。

在 Hermes 审计失败时，实时将失败点写入模板的审计反馈区。
用法: python3 audit_feedback_writer.py --date 2026-05-13 --score 14 --issues "问题1" "问题2" --strengths "优点1"
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
TEMPLATE_PATH = 'capabilities/skills/research/github-hot-project-learning/templates/daily-instruction.md'


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst())
    parser.add_argument('--score', type=int, required=True)
    parser.add_argument('--issues', nargs='+', default=[])
    parser.add_argument('--strengths', nargs='+', default=[])
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--dry-run', action='store_true')
    return parser.parse_args()


def load_audit_feedback(shared_root: Path) -> dict[str, Any]:
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    if not feedback_file.exists():
        return {'feedbacks': [], 'failures': []}
    try:
        with feedback_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'feedbacks': [], 'failures': []}


def save_audit_feedback(shared_root: Path, data: dict[str, Any]) -> None:
    feedback_file = shared_root / 'runtime' / 'hermes' / PIPELINE / 'audit-feedback.json'
    feedback_file.parent.mkdir(parents=True, exist_ok=True)
    with feedback_file.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_template_feedback(shared_root: Path, date: str, score: int, issues: list[str],
                             strengths: list[str], feedbacks: list[dict], dry_run: bool = False) -> None:
    template_file = shared_root / TEMPLATE_PATH
    if not template_file.exists():
        print(f'模板文件不存在: {template_file}', file=sys.stderr)
        return

    with template_file.open('r', encoding='utf-8') as f:
        content = f.read()

    # Build feedback section
    strength_list = '\n'.join(f'- {s}' for s in strengths) if strengths else '- 暂无'
    issue_list = '\n'.join(f'- {i}' for i in issues) if issues else '- 暂无'
    status = '✅ 通过' if score >= 16 else '❌ 需要改进'

    feedback_section = f'''### 最近审计反馈

**日期**: {date} | **得分**: {score}/20 | **状态**: {status}

**优点**:
{strength_list}

**问题**:
{issue_list}

'''

    # Replace section in template
    marker = '### 最近审计反馈'
    if marker in content:
        parts = content.split(marker, 1)
        # Find the next section marker
        rest = parts[1]
        next_markers = ['### 历史失败点', '---\n\n## 使用说明']
        end_pos = len(rest)
        for m in next_markers:
            pos = rest.find(m)
            if pos != -1 and pos < end_pos:
                end_pos = pos
        content = parts[0] + marker + '\n\n' + feedback_section + rest[end_pos:]

    if not dry_run:
        with template_file.open('w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ 模板已更新: {template_file}')


def main() -> None:
    args = parse_args()
    date = args.date
    score = args.score
    issues = args.issues
    strengths = args.strengths

    print(f'记录 {date} 审计结果 (得分: {score}/20)...')

    # Load and update feedback history
    feedback_data = load_audit_feedback(args.shared_root)
    feedbacks = feedback_data.get('feedbacks', [])
    new_feedback = {
        'date': date, 'score': score, 'issues': issues,
        'strengths': strengths, 'timestamp': datetime.now(TZ).isoformat()
    }
    feedbacks.append(new_feedback)

    if score < 16:
        feedback_data.setdefault('failures', []).append({'date': date, 'issues': issues})

    feedback_data['feedbacks'] = feedbacks

    if not args.dry_run:
        save_audit_feedback(args.shared_root, feedback_data)
        print('✅ 审计反馈已保存')

    # Update template
    update_template_feedback(args.shared_root, date, score, issues, strengths, feedbacks, args.dry_run)

    print(f'\n📊 审计结果:')
    print(f'   得分: {score}/20 | 状态: {"通过" if score >= 16 else "需要改进"}')
    if issues:
        print(f'   问题: {", ".join(issues)}')
    if strengths:
        print(f'   优点: {", ".join(strengths)}')


if __name__ == '__main__':
    main()
