#!/usr/bin/env python3
"""Cron 自动化任务管理器。

Shared Hub 为唯一真相源。
所有 job 定义在 shared/config/cron-jobs.json。
Hermes 通过 sync 命令从 shared hub 读取。

用法：
    python3 scripts/cron_manager.py list                    # 列出所有 job
    python3 scripts/cron_manager.py add --name X --schedule Y --prompt Z
    python3 scripts/cron_manager.py remove --id <id>        # 需要确认
    python3 scripts/cron_manager.py sync                    # 同步到 Hermes
    python3 scripts/cron_manager.py diff                    # 查看差异
"""

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

TZ = timezone(timedelta(hours=8))
DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]
JOBS_FILE = 'config/cron-jobs.json'


def log(msg: str) -> None:
    ts = datetime.now(TZ).strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')


def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)


def load_jobs(shared_root: Path) -> list[dict]:
    """从 shared hub 加载 job 定义（统一 schedule 为字符串）。"""
    path = shared_root / JOBS_FILE
    if not path.exists():
        return []
    jobs = json.loads(path.read_text(encoding='utf-8'))
    for j in jobs:
        sched = j.get('schedule')
        if isinstance(sched, dict):
            j['schedule'] = sched.get('expr', sched.get('display', ''))
    return jobs


def save_jobs(jobs: list[dict], shared_root: Path) -> None:
    """保存 job 定义到 shared hub。"""
    path = shared_root / JOBS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding='utf-8')


def load_hermes_jobs(hermes_home: Path) -> list[dict]:
    """从 Hermes 本地加载 job（运行时状态）。"""
    path = hermes_home / 'cron' / 'jobs.json'
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding='utf-8'))
    return raw.get('jobs', [])


def sync_to_hermes(jobs: list[dict], hermes_home: Path) -> None:
    """将 shared hub 的 job 定义写入 Hermes cron。"""
    hermes_cron = hermes_home / 'cron' / 'jobs.json'
    hermes_cron.parent.mkdir(parents=True, exist_ok=True)

    # 读取现有的 Hermes 运行时数据（保留 last_run 等状态）
    existing = {}
    if hermes_cron.exists():
        raw = json.loads(hermes_cron.read_text(encoding='utf-8'))
        for j in raw.get('jobs', []):
            jid = j.get('id', j.get('job_id'))
            if jid:
                existing[jid] = j

    # 合并：shared hub 定义 + Hermes 运行时状态
    merged = []
    for job_def in jobs:
        jid = job_def.get('id')
        if jid in existing:
            # 保留运行时状态，更新定义
            merged_job = existing[jid].copy()
            for key in ['name', 'schedule', 'prompt', 'deliver', 'enabled', 'skills', 'script', 'no_agent', 'workdir']:
                if key in job_def:
                    merged_job[key] = job_def[key]
            merged.append(merged_job)
        else:
            # 新 job，直接添加
            merged.append({
                'id': jid,
                'name': job_def.get('name', ''),
                'schedule': job_def.get('schedule', ''),
                'prompt': job_def.get('prompt', ''),
                'deliver': job_def.get('deliver', ''),
                'enabled': job_def.get('enabled', True),
                'skills': job_def.get('skills', []),
                'script': job_def.get('script', ''),
                'no_agent': job_def.get('no_agent', False),
                'workdir': job_def.get('workdir', ''),
            })

    hermes_data = {'jobs': merged, 'updated_at': datetime.now(TZ).isoformat()}
    hermes_cron.write_text(json.dumps(hermes_data, indent=2, ensure_ascii=False), encoding='utf-8')


# ── 命令实现 ──────────────────────────────────────────────────

def cmd_list(shared_root: Path) -> None:
    """列出所有 job。"""
    jobs = load_jobs(shared_root)
    if not jobs:
        log('无 job 定义')
        return

    print(f'📋 共 {len(jobs)} 个自动化任务\n')
    print(f'{"ID":<14} {"状态":<4} {"类型":<6} {"调度":<16} {"名称"}')
    print('-' * 80)
    for j in jobs:
        jid = j.get('id', '?')[:12]
        status = '✅' if j.get('enabled', True) else '⏸️'
        owner = j.get('owner', '?')[:4]
        sched = j.get('schedule', '?')
        if isinstance(sched, dict):
            sched = sched.get('expr', sched.get('display', '?'))
        schedule = str(sched)[:14]
        name = j.get('name', '?')
        print(f'{jid:<14} {status:<4} {owner:<6} {schedule:<16} {name}')


def cmd_add(
    shared_root: Path,
    name: str,
    schedule: str,
    prompt: str,
    deliver: str = 'local',
    skills: Optional[list] = None,
    script: str = '',
    no_agent: bool = False,
    workdir: str = '',
    description: str = '',
) -> None:
    """添加新 job。"""
    jobs = load_jobs(shared_root)

    # 生成 ID
    job_id = uuid.uuid4().hex[:12]

    # 检查重名
    for j in jobs:
        if j.get('name') == name:
            log(f'⚠️ 已存在同名 job: {name} (id={j["id"]})')
            log('   请用不同的名称，或先 remove 旧的')
            return

    new_job = {
        'id': job_id,
        'name': name,
        'schedule': schedule,
        'prompt': prompt,
        'deliver': deliver,
        'enabled': True,
        'owner': 'user',
        'description': description,
    }
    if skills:
        new_job['skills'] = skills
    if script:
        new_job['script'] = script
    if no_agent:
        new_job['no_agent'] = True
    if workdir:
        new_job['workdir'] = workdir

    jobs.append(new_job)
    save_jobs(jobs, shared_root)
    log(f'✅ 已添加: {name} (id={job_id})')

    # 自动同步
    _auto_sync(shared_root)


def cmd_remove(shared_root: Path, hermes_home: Path, job_id: str, force: bool = False) -> None:
    """删除 job（需要确认）。"""
    jobs = load_jobs(shared_root)

    # 查找 job
    target = None
    for j in jobs:
        if j.get('id') == job_id:
            target = j
            break

    if not target:
        log(f'❌ 找不到 job: {job_id}')
        # 模糊匹配
        matches = [j for j in jobs if job_id in j.get('id', '') or job_id in j.get('name', '')]
        if matches:
            log('   你是不是想找:')
            for m in matches:
                log(f'     {m["id"]} — {m.get("name", "?")}')
        return

    # 确认
    if not force:
        print(f'\n⚠️  即将删除:')
        print(f'   ID: {target["id"]}')
        print(f'   名称: {target.get("name", "?")}')
        print(f'   调度: {target.get("schedule", "?")}')
        print(f'   类型: {target.get("owner", "?")}')
        print()
        confirm = input('确认删除？(y/N): ').strip().lower()
        if confirm != 'y':
            log('取消删除')
            return

    # 删除
    jobs = [j for j in jobs if j.get('id') != job_id]
    save_jobs(jobs, shared_root)
    log(f'🗑️  已删除: {target.get("name", job_id)}')

    # 自动同步
    _auto_sync(shared_root)


def cmd_sync(shared_root: Path, hermes_home: Path) -> None:
    """同步 shared hub → Hermes。"""
    jobs = load_jobs(shared_root)
    if not jobs:
        log('无 job 定义，跳过同步')
        return

    sync_to_hermes(jobs, hermes_home)
    log(f'✅ 已同步 {len(jobs)} 个 job 到 Hermes')


def cmd_diff(shared_root: Path, hermes_home: Path) -> None:
    """查看 shared hub 与 Hermes 的差异。"""
    shared_jobs = {j['id']: j for j in load_jobs(shared_root)}
    hermes_jobs = {j.get('id', j.get('job_id')): j for j in load_hermes_jobs(hermes_home)}

    shared_ids = set(shared_jobs.keys())
    hermes_ids = set(hermes_jobs.keys())

    only_shared = shared_ids - hermes_ids
    only_hermes = hermes_ids - shared_ids
    common = shared_ids & hermes_ids

    if not only_shared and not only_hermes:
        log('✅ 无差异，完全同步')
        return

    if only_shared:
        log(f'📋 Shared Hub 有但 Hermes 没有 ({len(only_shared)}):')
        for jid in only_shared:
            log(f'   + {shared_jobs[jid].get("name", jid)}')

    if only_hermes:
        log(f'⚠️  Hermes 有但 Shared Hub 没有 ({len(only_hermes)}):')
        for jid in only_hermes:
            j = hermes_jobs[jid]
            log(f'   ? {j.get("name", jid)} (id={jid})')
        log('   这些 job 可能需要导入到 shared hub，或手动删除')

    # 检查共同 job 的定义差异
    changed = []
    for jid in common:
        sh = shared_jobs[jid]
        he = hermes_jobs[jid]
        for key in ['name', 'schedule', 'prompt', 'deliver', 'enabled']:
            if sh.get(key) != he.get(key):
                changed.append((jid, key, sh.get(key), he.get(key)))

    if changed:
        log(f'📝 定义差异 ({len(changed)}):')
        for jid, key, sh_val, he_val in changed:
            log(f'   {jid}.{key}: shared="{str(sh_val)[:40]}" vs hermes="{str(he_val)[:40]}"')


def cmd_import(shared_root: Path, hermes_home: Path) -> None:
    """从 Hermes 导入 job 到 shared hub（迁移用）。"""
    shared_jobs = {j['id']: j for j in load_jobs(shared_root)}
    hermes_jobs = load_hermes_jobs(hermes_home)

    imported = 0
    for j in hermes_jobs:
        jid = j.get('id', j.get('job_id'))
        if not jid or jid in shared_jobs:
            continue

        # 转为 portable 格式
        portable = {
            'id': jid,
            'name': j.get('name', ''),
            'schedule': j.get('schedule', ''),
            'prompt': j.get('prompt', ''),
            'deliver': j.get('deliver', ''),
            'enabled': j.get('enabled', True),
            'owner': 'user',
        }
        for key in ['skills', 'script', 'no_agent', 'workdir']:
            if j.get(key):
                portable[key] = j[key]

        shared_jobs[jid] = portable
        imported += 1
        log(f'   + 导入: {portable.get("name", jid)}')

    if imported > 0:
        save_jobs(list(shared_jobs.values()), shared_root)
        log(f'✅ 导入了 {imported} 个 job 到 shared hub')
    else:
        log('✅ 无需导入，已全部在 shared hub 中')


def _auto_sync(shared_root: Path) -> None:
    """自动同步到 Hermes（如果 Hermes home 存在）。"""
    hermes_home = Path.home() / '.hermes'
    if (hermes_home / 'cron').exists():
        jobs = load_jobs(shared_root)
        sync_to_hermes(jobs, hermes_home)
        log(f'   → 已自动同步到 Hermes ({len(jobs)} 个 job)')


# ── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Cron 自动化任务管理器')
    parser.add_argument('action', choices=['list', 'add', 'remove', 'sync', 'diff', 'import'],
                        help='list/add/remove/sync/diff/import')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT)
    parser.add_argument('--hermes-home', type=Path, default=Path.home() / '.hermes')

    # add 参数
    parser.add_argument('--name', help='任务名称')
    parser.add_argument('--schedule', help='调度表达式')
    parser.add_argument('--prompt', help='任务指令')
    parser.add_argument('--deliver', default='local', help='推送目标')
    parser.add_argument('--skills', nargs='*', default=[], help='加载的 skills')
    parser.add_argument('--script', default='', help='脚本路径')
    parser.add_argument('--no-agent', action='store_true', help='纯脚本模式')
    parser.add_argument('--workdir', default='', help='工作目录')
    parser.add_argument('--description', default='', help='一句话描述')

    # remove 参数
    parser.add_argument('--id', help='Job ID')
    parser.add_argument('--force', action='store_true', help='跳过确认')

    args = parser.parse_args()

    if args.action == 'list':
        cmd_list(args.shared_root)
    elif args.action == 'add':
        if not all([args.name, args.schedule, args.prompt]):
            parser.error('add 需要 --name, --schedule, --prompt')
        cmd_add(args.shared_root, args.name, args.schedule, args.prompt,
                args.deliver, args.skills, args.script, args.no_agent,
                args.workdir, args.description)
    elif args.action == 'remove':
        if not args.id:
            parser.error('remove 需要 --id')
        cmd_remove(args.shared_root, args.hermes_home, args.id, args.force)
    elif args.action == 'sync':
        cmd_sync(args.shared_root, args.hermes_home)
    elif args.action == 'diff':
        cmd_diff(args.shared_root, args.hermes_home)
    elif args.action == 'import':
        cmd_import(args.shared_root, args.hermes_home)


if __name__ == '__main__':
    main()
