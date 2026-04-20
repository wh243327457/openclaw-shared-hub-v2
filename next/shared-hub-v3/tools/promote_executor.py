#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SANDBOX_ROOT = ROOT / 'sandbox'
TRUTH_ROOT = ROOT / 'truth'
PROMOTE_LOGS_DIR = TRUTH_ROOT / 'promote-logs'
MEMORY_FILE = TRUTH_ROOT / 'memory' / 'MEMORY.md'
BLOCK_START = '<!-- SHARED-V3-PROMOTE-ENTRIES:START -->'
BLOCK_END = '<!-- SHARED-V3-PROMOTE-ENTRIES:END -->'
CONTENT_KIND_TARGET_PREFIXES = {
    'memory-fact': 'truth/memory/facts/',
    'memory-project': 'truth/memory/projects/',
}
REQUIRED_FIELDS = [
    'record_id',
    'submitter_agent',
    'source_path',
    'target_path',
    'content_kind',
    'promoted_by',
    'decision',
    'promoted_at',
]


class PromoteError(Exception):
    pass


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith('---\n'):
        raise PromoteError('record must start with YAML frontmatter')

    closing = text.find('\n---\n', 4)
    if closing == -1:
        raise PromoteError('record frontmatter must end with closing --- fence')

    frontmatter = text[4:closing]
    body = text[closing + 5:]
    metadata: dict[str, str] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ':' not in line:
            raise PromoteError(f'invalid frontmatter line: {raw_line}')
        key, value = line.split(':', 1)
        metadata[key.strip()] = value.strip()
    return metadata, body


def validate_record(metadata: dict[str, str]) -> tuple[Path, Path]:
    for field in REQUIRED_FIELDS:
        if not metadata.get(field):
            raise PromoteError(f'missing required field: {field}')

    if metadata['decision'] != 'approved':
        raise PromoteError("decision must be 'approved'")

    if metadata['promoted_by'] != 'hermes':
        raise PromoteError("promoted_by must be 'hermes' in stage3")

    source_path = Path(metadata['source_path'])
    target_path = Path(metadata['target_path'])

    if source_path.is_absolute() or target_path.is_absolute():
        raise PromoteError('source_path and target_path must be relative paths')

    source_posix = source_path.as_posix()
    target_posix = target_path.as_posix()

    if not source_posix.startswith('sandbox/'):
        raise PromoteError('source_path must stay under sandbox/')
    if not target_posix.startswith('truth/'):
        raise PromoteError('target_path must stay under truth/')

    content_kind = metadata['content_kind']
    expected_prefix = CONTENT_KIND_TARGET_PREFIXES.get(content_kind)
    if expected_prefix and not target_posix.startswith(expected_prefix):
        raise PromoteError(
            f'target_path for {content_kind} must stay under {expected_prefix}'
        )

    source_abs = ROOT / source_path
    target_abs = ROOT / target_path
    if not source_abs.exists():
        raise PromoteError(f'source file does not exist: {source_posix}')

    return source_abs, target_abs


def load_log_metadata(path: Path) -> dict[str, str]:
    metadata, _ = parse_frontmatter(read_text(path))
    return metadata


def render_recent_entries() -> list[str]:
    entries: list[tuple[str, str]] = []
    if PROMOTE_LOGS_DIR.exists():
        for path in sorted(PROMOTE_LOGS_DIR.glob('*.md')):
            metadata = load_log_metadata(path)
            executed_at = metadata.get('executed_at', '')
            line = (
                f"- {executed_at} | {metadata.get('record_id', path.stem)} | "
                f"{metadata.get('content_kind', 'other')} | {metadata.get('target_path', '')}"
            )
            entries.append((executed_at, line))
    if not entries:
        return ['- none yet']
    entries.sort(key=lambda item: item[0], reverse=True)
    return [line for _, line in entries[:5]]


def update_memory_index() -> None:
    if not MEMORY_FILE.exists():
        raise PromoteError('truth/memory/MEMORY.md is missing')

    content = read_text(MEMORY_FILE)
    managed_block = '\n'.join(render_recent_entries())
    replacement = f'{BLOCK_START}\n{managed_block}\n{BLOCK_END}'

    if BLOCK_START in content and BLOCK_END in content:
        start = content.index(BLOCK_START)
        end = content.index(BLOCK_END) + len(BLOCK_END)
        content = content[:start] + replacement + content[end:]
    else:
        content = content.rstrip() + f'\n\n## Recent Promote Entries\n\n{replacement}\n'

    write_text(MEMORY_FILE, content)


def build_log_content(metadata: dict[str, str], executed_at: str, source_sha256: str, target_sha256: str) -> str:
    notes = metadata.get('notes', 'promoted by hermes stage3 executor')
    return (
        '---\n'
        f"record_id: {metadata['record_id']}\n"
        f"submitter_agent: {metadata['submitter_agent']}\n"
        f"source_path: {metadata['source_path']}\n"
        f"target_path: {metadata['target_path']}\n"
        f"content_kind: {metadata['content_kind']}\n"
        f"promoted_by: {metadata['promoted_by']}\n"
        f"decision: {metadata['decision']}\n"
        f"promoted_at: {metadata['promoted_at']}\n"
        f"executed_at: {executed_at}\n"
        f"source_sha256: {source_sha256}\n"
        f"target_sha256: {target_sha256}\n"
        f"notes: {notes}\n"
        '---\n\n'
        '# Promote Record\n\n'
        f"- 审核结论：{metadata['decision']}\n"
        '- 执行结论：promoted\n'
        f"- Source: {metadata['source_path']}\n"
        f"- Target: {metadata['target_path']}\n"
    )


def execute_promote(record_path: Path, dry_run: bool = False) -> str:
    metadata, _ = parse_frontmatter(read_text(record_path))
    source_abs, target_abs = validate_record(metadata)

    if dry_run:
        return (
            f"[promote-executor] DRY-RUN: {metadata['record_id']} | "
            f"{metadata['source_path']} -> {metadata['target_path']}"
        )

    target_abs.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_abs, target_abs)

    source_sha256 = sha256_file(source_abs)
    target_sha256 = sha256_file(target_abs)
    executed_at = now_utc()

    log_path = PROMOTE_LOGS_DIR / f"{metadata['record_id']}.md"
    log_content = build_log_content(metadata, executed_at, source_sha256, target_sha256)
    write_text(log_path, log_content)
    update_memory_index()

    return (
        f"[promote-executor] SUCCESS: {metadata['record_id']} | "
        f"{metadata['source_path']} -> {metadata['target_path']}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='shared-hub-v3 stage3 promote executor')
    parser.add_argument('record', help='relative or absolute path to approved promote record')
    parser.add_argument('--dry-run', action='store_true', help='validate only; do not copy or write logs')
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    record_path = Path(args.record)
    if not record_path.is_absolute():
        record_path = ROOT / record_path

    try:
        message = execute_promote(record_path, dry_run=args.dry_run)
        print(message)
        return 0
    except PromoteError as exc:
        print(f'[promote-executor] FAIL: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
