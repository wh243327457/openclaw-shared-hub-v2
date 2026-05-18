#!/usr/bin/env python3
"""Health check for GitHub hot project learning pipeline.

Checks the OpenClaw run source, canonical shared inbox bridge output, Hermes
runtime status/audit markers, and Obsidian knowledge-base outputs. Exit codes:
0=green, 1=yellow, 2=red.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DEFAULT_SHARED_ROOT = Path('/home/vany/openclaw-data/.openclaw/shared')
DEFAULT_OPENCLAW_ROOT = Path('/home/vany/openclaw-data/.openclaw')
DEFAULT_JOB_ID = '7aa310ea-b264-40c8-b23a-ed655c565a69'
DEFAULT_KB_ROOT = Path('/mnt/d/system/selfSystem/03-学习/技术实践/GitHub 热门项目学习档案')
PIPELINE = 'github-hot-project-learning'
TZ = timezone(timedelta(hours=8))
TIME_FIELDS = ('endedAt', 'finishedAt', 'updatedAt', 'startedAt', 'createdAt', 'ts', 'timestamp')
SUMMARY_FIELDS = ('summary', 'result', 'output', 'message', 'text', 'content')


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='Target date YYYY-MM-DD, default today Asia/Shanghai')
    parser.add_argument('--json', action='store_true', help='Print JSON only')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT, help='Shared hub root path')
    parser.add_argument('--openclaw-root', type=Path, default=DEFAULT_OPENCLAW_ROOT, help='OpenClaw data root path')
    parser.add_argument('--run-file', type=Path, default=None, help='OpenClaw cron JSONL run file override')
    parser.add_argument('--job-id', default=DEFAULT_JOB_ID, help='OpenClaw cron job id')
    parser.add_argument('--kb-root', type=Path, default=DEFAULT_KB_ROOT, help='Obsidian knowledge-base root path')
    return parser.parse_args()


def parse_time_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        ts = float(value)
        if ts > 10_000_000_000:
            ts /= 1000.0
        return datetime.fromtimestamp(ts, TZ).date().isoformat()
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    match = re.search(r'\d{4}-\d{2}-\d{2}', raw)
    if match:
        return match.group(0)
    try:
        return datetime.fromisoformat(raw.replace('Z', '+00:00')).astimezone(TZ).date().isoformat()
    except ValueError:
        return None


def extract_summary(record: dict[str, Any]) -> str:
    for field in SUMMARY_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    for container in ('data', 'response', 'run', 'payload'):
        nested = record.get(container)
        if isinstance(nested, dict):
            nested_summary = extract_summary(nested)
            if nested_summary:
                return nested_summary
    return ''


def record_date(record: dict[str, Any], summary: str) -> str | None:
    for field in TIME_FIELDS:
        parsed = parse_time_value(record.get(field))
        if parsed:
            return parsed
    match = re.search(r'\d{4}-\d{2}-\d{2}', summary)
    return match.group(0) if match else None


def is_ok(record: dict[str, Any]) -> bool:
    status_values = [record.get('status'), record.get('lastRunStatus'), record.get('state')]
    return any(str(value).lower() in {'ok', 'success', 'succeeded', 'completed'} for value in status_values if value is not None)


def find_ok_run(target_date: str, runs_file: Path) -> dict[str, Any] | None:
    if not runs_file.exists():
        return None
    found = None
    with runs_file.open('r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            summary = extract_summary(record)
            if summary and is_ok(record) and record_date(record, summary) == target_date:
                found = record
    return found


def text_check(path: Path, contains: str | None = None) -> dict[str, Any]:
    exists = path.exists() and path.is_file() and path.stat().st_size > 0
    result: dict[str, Any] = {'path': str(path), 'exists': exists}
    if contains is not None:
        text = path.read_text(encoding='utf-8', errors='replace') if exists else ''
        result['contains'] = contains in text
    return result


def status_check(path: Path, target_date: str) -> dict[str, Any]:
    result = text_check(path)
    if not result['exists']:
        result['ok'] = False
        return result
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        result.update({'ok': False, 'error': f'json parse failed: {exc}'})
        return result
    result.update({
        'ok': data.get('date') == target_date and data.get('overall_status') in {'openclaw_inbox_ready', 'dry_run_ready', 'audit_ready', 'pushed'},
        'overall_status': data.get('overall_status'),
        'date': data.get('date'),
    })
    return result


def main() -> int:
    args = parse_args()
    datetime.strptime(args.date, '%Y-%m-%d')
    runs_file = args.run_file or (args.openclaw_root / 'cron' / 'runs' / f'{args.job_id}.jsonl')
    runtime_dir = args.shared_root / 'runtime' / 'hermes' / PIPELINE
    inbox = args.shared_root / 'inbox' / 'openclaw' / 'daily' / f'{args.date}.md'
    status = runtime_dir / 'status.json'
    bridge_log = runtime_dir / 'bridge.log'
    healthcheck_out = runtime_dir / f'healthcheck-{args.date}.json'
    daily = args.kb_root / '每日学习' / f'{args.date}-GitHub热门项目学习日报.md'
    audit = args.kb_root / '质量审计' / f'{args.date}-质量审计.md'
    index = args.kb_root / '00-总览索引.md'
    run = find_ok_run(args.date, runs_file)
    checks: dict[str, dict[str, Any]] = {
        'openclaw_run': {
            'ok': run is not None,
            'runs_file': str(runs_file),
            'job_id': args.job_id,
            'run_ts': next((run.get(field) for field in TIME_FIELDS if run and run.get(field) is not None), None) if run else None,
        },
        'openclaw_inbox': text_check(inbox, args.date),
        'runtime_status': status_check(status, args.date),
        'bridge_log': text_check(bridge_log, args.date),
        'obsidian_daily': text_check(daily),
        'obsidian_audit': text_check(audit, args.date),
        'obsidian_index': text_check(index, args.date),
    }
    for key, item in checks.items():
        if 'ok' not in item:
            item['ok'] = bool(item.get('exists')) and item.get('contains', True) is not False

    critical = ('openclaw_run', 'openclaw_inbox', 'runtime_status')
    missing_critical = [key for key in critical if not checks[key]['ok']]
    missing_noncritical = [key for key, value in checks.items() if not value['ok'] and key not in missing_critical]
    if missing_critical:
        level = 'red'
        exit_code = 2
    elif missing_noncritical:
        level = 'yellow'
        exit_code = 1
    else:
        level = 'green'
        exit_code = 0

    result = {
        'date': args.date,
        'pipeline': PIPELINE,
        'level': level,
        'ok': exit_code == 0,
        'checks': checks,
        'missing_critical': missing_critical,
        'missing_noncritical': missing_noncritical,
        'updated_at': datetime.now(TZ).isoformat(timespec='seconds'),
    }
    runtime_dir.mkdir(parents=True, exist_ok=True)
    healthcheck_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{PIPELINE} {args.date}: {level}")
        for key, item in checks.items():
            mark = '✅' if item['ok'] else '❌'
            print(f"{mark} {key}: {item.get('path') or item.get('runs_file')}")
        print(f'healthcheck_file: {healthcheck_out}')
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
