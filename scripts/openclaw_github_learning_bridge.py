#!/usr/bin/env python3
"""Bridge OpenClaw GitHub learning cron output into shared inbox.

Reads an OpenClaw cron JSONL run log, extracts the latest successful run for a
specific date, writes the raw OpenClaw report to shared/inbox/openclaw/daily,
and persists a small runtime status panel for Hermes audit/push steps.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OPENCLAW_ROOT = Path(__file__).resolve().parents[2] / '.openclaw'
DEFAULT_JOB_ID = '7aa310ea-b264-40c8-b23a-ed655c565a69'
PIPELINE = 'github-hot-project-learning'
TZ = timezone(timedelta(hours=8))
TIME_FIELDS = ('endedAt', 'finishedAt', 'updatedAt', 'startedAt', 'createdAt', 'ts', 'timestamp')
SUMMARY_FIELDS = ('summary', 'result', 'output', 'message', 'text', 'content')
MANUAL_MARKERS = ('MANUAL_EDIT', 'manual_edit: true', '人工编辑')


def today_cst() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=today_cst(), help='Target date YYYY-MM-DD, default today Asia/Shanghai')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing files')
    parser.add_argument('--force', action='store_true', help='Overwrite manual-edit protected inbox file')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT, help='Shared hub root path')
    parser.add_argument('--openclaw-root', type=Path, default=DEFAULT_OPENCLAW_ROOT, help='OpenClaw data root path')
    parser.add_argument('--run-file', type=Path, default=None, help='OpenClaw cron JSONL run file override')
    parser.add_argument('--job-id', default=DEFAULT_JOB_ID, help='OpenClaw cron job id')
    parser.add_argument('--json', action='store_true', help='Print machine-readable JSON summary')
    return parser.parse_args()


def runtime_dir(shared_root: Path) -> Path:
    return shared_root / 'runtime' / 'hermes' / PIPELINE


def log(shared_root: Path, message: str) -> None:
    rd = runtime_dir(shared_root)
    rd.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(TZ).isoformat(timespec='seconds')
    with (rd / 'bridge.log').open('a', encoding='utf-8') as fh:
        fh.write(f'[{ts}] {message}\n')


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


def run_ts(record: dict[str, Any]) -> Any:
    for field in TIME_FIELDS:
        if record.get(field) is not None:
            return record.get(field)
    return None


def extract_summary(record: dict[str, Any]) -> str:
    for field in SUMMARY_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    # Some OpenClaw records store payloads under nested fields.
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


def find_record(target_date: str, runs_file: Path) -> tuple[dict[str, Any], str, list[str]]:
    warnings: list[str] = []
    matches: list[tuple[dict[str, Any], str]] = []
    if not runs_file.exists():
        raise FileNotFoundError(f'OpenClaw run file not found: {runs_file}')
    with runs_file.open('r', encoding='utf-8') as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(f'line {line_no}: json parse failed: {exc}')
                continue
            summary = extract_summary(record)
            if not summary or not is_ok(record):
                continue
            if record_date(record, summary) == target_date:
                matches.append((record, summary))
    if not matches:
        raise RuntimeError(f'No successful OpenClaw summary found for {target_date} in {runs_file}')
    return matches[-1][0], matches[-1][1], warnings


def redact_secrets(text: str) -> str:
    patterns = [
        (r'sk-[A-Za-z0-9_\-]{16,}', 'sk-[REDACTED]'),
        (r'(?i)(token\s*[=:]\s*)[^\s`"\']+', r'\1[REDACTED]'),
        (r'(?i)(api[_-]?key\s*[=:]\s*)[^\s`"\']+', r'\1[REDACTED]'),
        (r'(?i)(password\s*[=:]\s*)[^\s`"\']+', r'\1[REDACTED]'),
        (r'(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._\-]+', r'\1[REDACTED]'),
    ]
    redacted = text
    for pattern, repl in patterns:
        redacted = re.sub(pattern, repl, redacted)
    return redacted


def build_markdown(target_date: str, record: dict[str, Any], summary: str, job_id: str) -> str:
    safe_summary = redact_secrets(summary)
    return f"""---
source: openclaw-cron
pipeline: {PIPELINE}
job_id: {job_id}
run_status: ok
run_ts: '{run_ts(record)}'
needs_hermes_audit: true
---

# {target_date} — GitHub 热门项目每日学习（OpenClaw 原始输出）

## 桥接说明

- 本文件由 Hermes/shared 桥接脚本从 OpenClaw cron run 提取。
- 这是 OpenClaw 原始输出，不是最终审计结论。
- 禁止在本文件写入明文 secret；桥接时已执行基础脱敏。

## OpenClaw 原始报告

{safe_summary}
"""


def write_status(shared_root: Path, status: dict[str, Any]) -> Path:
    rd = runtime_dir(shared_root)
    rd.mkdir(parents=True, exist_ok=True)
    status_file = rd / 'status.json'
    status_file.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return status_file


def make_status(target_date: str, job_id: str, runs_file: Path, state_file: Path, record: dict[str, Any] | None, inbox_path: Path, written: bool, dry_run: bool, overall_status: str, error: str | None = None) -> dict[str, Any]:
    status: dict[str, Any] = {
        'date': target_date,
        'pipeline': PIPELINE,
        'openclaw': {
            'job_id': job_id,
            'run_found': record is not None,
            'run_status': 'ok' if record is not None else None,
            'run_ts': run_ts(record) if record is not None else None,
            'runs_file': str(runs_file),
            'state_file': str(state_file),
            'inbox_path': str(inbox_path),
            'inbox_written': written,
            'dry_run': dry_run,
        },
        'hermes': {
            'audit_path': None,
            'push_status': 'pending',
        },
        'obsidian': {
            'daily_path': None,
            'audit_path': None,
            'index_path': None,
        },
        'overall_status': overall_status,
        'updated_at': datetime.now(TZ).isoformat(timespec='seconds'),
    }
    if error:
        status['error'] = error
    return status


def main() -> int:
    args = parse_args()
    shared_root = args.shared_root
    openclaw_root = args.openclaw_root
    runs_file = args.run_file or (openclaw_root / 'cron' / 'runs' / f'{args.job_id}.jsonl')
    state_file = openclaw_root / 'cron' / 'jobs-state.json'
    inbox_path = shared_root / 'inbox' / 'openclaw' / 'daily' / f'{args.date}.md'
    try:
        datetime.strptime(args.date, '%Y-%m-%d')
        record, summary, warnings = find_record(args.date, runs_file)
        content = build_markdown(args.date, record, summary, args.job_id)
        if inbox_path.exists() and not args.force:
            existing = inbox_path.read_text(encoding='utf-8', errors='replace')
            if any(marker in existing for marker in MANUAL_MARKERS):
                raise RuntimeError(f'inbox has manual edit marker; use --force to overwrite: {inbox_path}')
        if args.dry_run:
            status = make_status(args.date, args.job_id, runs_file, state_file, record, inbox_path, False, True, 'dry_run_ready')
            summary_obj = {'ok': True, 'dry_run': True, 'status': status, 'warnings': warnings}
            if args.json:
                print(json.dumps(summary_obj, ensure_ascii=False, indent=2))
            else:
                print(f'target_date: {args.date}')
                print(f'run_file: {runs_file}')
                print(f'inbox_path: {inbox_path}')
                print('dry_run: true; no files written')
            return 0
        inbox_path.parent.mkdir(parents=True, exist_ok=True)
        inbox_path.write_text(content, encoding='utf-8')
        status = make_status(args.date, args.job_id, runs_file, state_file, record, inbox_path, True, False, 'openclaw_inbox_ready')
        status_file = write_status(shared_root, status)
        log(shared_root, f'bridged date={args.date} inbox={inbox_path}')
        summary_obj = {'ok': True, 'written': True, 'inbox_path': str(inbox_path), 'status_file': str(status_file), 'warnings': warnings}
        if args.json:
            print(json.dumps(summary_obj, ensure_ascii=False, indent=2))
        else:
            print(f'target_date: {args.date}')
            print(f'run_file: {runs_file}')
            print(f'inbox_path: {inbox_path}')
            print('written: true')
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI should persist clear failure.
        failure = make_status(args.date, args.job_id, runs_file, state_file, None, inbox_path, False, args.dry_run, 'bridge_failed', str(exc))
        status_file = write_status(shared_root, failure)
        log(shared_root, f'failed date={args.date} error={exc}')
        if args.json:
            print(json.dumps({'ok': False, 'status_file': str(status_file), 'error': str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f'error: {exc}', file=sys.stderr)
            print(f'status_file: {status_file}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
