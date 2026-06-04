#!/usr/bin/env python3
"""共享中台一键同步工具。

新环境接入时，一条命令完成：
1. 克隆/拉取 shared hub
2. 安装脚本依赖
3. 同步 skills（shared → local）
4. 同步 cron jobs（如存在导出的定义）
5. 生成环境检查报告

用法：
    # 新环境首次接入
    python3 scripts/bootstrap.py init

    # 已有环境同步更新
    python3 scripts/bootstrap.py sync

    # 导出当前环境配置（用于备份/迁移）
    python3 scripts/bootstrap.py export

    # 检查环境完整性
    python3 scripts/bootstrap.py check
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))
DEFAULT_SHARED_ROOT = Path(__file__).resolve().parents[1]


def log(msg: str) -> None:
    ts = datetime.now(TZ).strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')


def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)


# ── 1. Init: 新环境首次接入 ──────────────────────────────────

def cmd_init(shared_root: Path, hermes_home: Path) -> None:
    """新环境首次接入：克隆 shared hub + 安装 + 同步。"""
    log('🚀 初始化共享中台接入...')

    # 1. 检查 shared hub 是否已存在
    if not (shared_root / '.git').exists():
        log('   克隆 shared hub...')
        result = run(f'git clone https://github.com/wh243327457/openclaw-shared-hub-v2.git {shared_root}')
        if result.returncode != 0:
            log(f'   ❌ 克隆失败: {result.stderr}')
            sys.exit(1)
        log('   ✅ 克隆完成')
    else:
        log('   ✅ shared hub 已存在')

    # 2. 安装依赖
    _install_deps(shared_root)

    # 3. 同步 skills
    _sync_skills(shared_root, hermes_home)

    # 4. 同步 cron jobs
    _sync_cron(shared_root, hermes_home)

    # 5. 环境检查
    _env_check(shared_root, hermes_home)

    log('🎉 初始化完成！')


# ── 2. Sync: 已有环境同步更新 ─────────────────────────────────

def cmd_sync(shared_root: Path, hermes_home: Path) -> None:
    """拉取最新 + 同步 skills + cron + 自动导出变化。"""
    log('🔄 同步更新...')

    # 1. git pull
    result = run('git pull --ff-only', cwd=shared_root)
    if result.returncode != 0:
        log(f'   ⚠️ git pull 失败: {result.stderr.strip()}')
    else:
        log('   ✅ 代码已更新')

    # 2. 同步 skills
    _sync_skills(shared_root, hermes_home)

    # 3. 同步 cron jobs
    _sync_cron(shared_root, hermes_home)

    # 4. 检测本地 cron 变化 → 自动导出到 config/
    _export_cron_if_changed(shared_root, hermes_home)

    log('✅ 同步完成')


# ── 3. Export: 导出当前环境配置 ────────────────────────────────

def cmd_export(shared_root: Path, hermes_home: Path) -> None:
    """导出当前环境的 cron jobs + skills 清单，用于备份/迁移。"""
    log('📦 导出环境配置...')

    export_dir = shared_root / 'runtime' / 'hermes' / 'exports'
    export_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(TZ).strftime('%Y-%m-%d_%H%M')

    # 1. 导出 cron jobs
    cron_file = hermes_home / 'cron' / 'jobs.json'
    if cron_file.exists():
        dest = export_dir / f'cron-jobs-{ts}.json'
        shutil.copy2(cron_file, dest)
        log(f'   ✅ cron jobs → {dest.name}')

    # 2. 导出 skills 清单
    skills_manifest = _scan_custom_skills(hermes_home)
    dest = export_dir / f'skills-manifest-{ts}.json'
    dest.write_text(json.dumps(skills_manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    log(f'   ✅ skills 清单 → {dest.name} ({len(skills_manifest)} 个自定义 skill)')

    # 3. 导出环境摘要
    summary = _build_env_summary(shared_root, hermes_home)
    dest = export_dir / f'env-summary-{ts}.json'
    dest.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    log(f'   ✅ 环境摘要 → {dest.name}')

    log(f'📦 导出完成: {export_dir}')


# ── 4. Check: 环境完整性检查 ──────────────────────────────────

def cmd_check(shared_root: Path, hermes_home: Path) -> None:
    """检查环境完整性，输出报告。"""
    _env_check(shared_root, hermes_home)


# ── 内部实现 ──────────────────────────────────────────────────

def _install_deps(shared_root: Path) -> None:
    """安装 shared hub 脚本依赖。"""
    log('   安装依赖...')
    req_file = shared_root / 'requirements.txt'
    if req_file.exists():
        result = run(f'pip install -q -r {req_file}')
        if result.returncode == 0:
            log('   ✅ pip 依赖已安装')
        else:
            log(f'   ⚠️ pip 安装部分失败: {result.stderr[:200]}')
    else:
        log('   ℹ️ 无 requirements.txt，跳过')


def _sync_skills(shared_root: Path, hermes_home: Path) -> None:
    """同步共享 skills 到本地 Hermes。"""
    log('   同步 skills...')
    shared_skills = shared_root / 'capabilities' / 'skills'
    local_skills = hermes_home / 'skills'

    if not shared_skills.exists():
        log('   ⚠️ shared/capabilities/skills/ 不存在')
        return

    synced = 0
    for skill_file in shared_skills.rglob('SKILL.md'):
        rel_path = skill_file.relative_to(shared_skills)
        local_path = local_skills / rel_path

        # 检查是否需要更新
        if local_path.exists():
            # 比较修改时间
            if skill_file.stat().st_mtime <= local_path.stat().st_mtime:
                continue

        # 复制（保留目录结构）
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_file, local_path)
        synced += 1

    if synced > 0:
        log(f'   ✅ 同步了 {synced} 个 skill')
    else:
        log('   ✅ skills 已是最新')


def _sync_cron(shared_root: Path, hermes_home: Path) -> None:
    """同步 cron jobs 定义（如果有导出的定义文件）。"""
    log('   检查 cron jobs...')
    cron_defs = shared_root / 'config' / 'cron-jobs.json'

    if not cron_defs.exists():
        log('   ℹ️ 无共享 cron 定义，跳过（可用 export 命令生成）')
        return

    # 读取共享定义
    shared_jobs = json.loads(cron_defs.read_text(encoding='utf-8'))

    # 读取本地 cron
    local_cron = hermes_home / 'cron' / 'jobs.json'
    if local_cron.exists():
        local_data = json.loads(local_cron.read_text(encoding='utf-8'))
        local_job_ids = {j.get('id', j.get('job_id')) for j in local_data.get('jobs', [])}
    else:
        local_job_ids = set()

    # 找出新增的 job
    new_jobs = [j for j in shared_jobs if j.get('id') not in local_job_ids]

    if new_jobs:
        log(f'   📋 发现 {len(new_jobs)} 个新 cron job，需要手动确认:')
        for j in new_jobs:
            log(f'      - {j.get("name", j.get("id", "?"))} ({j.get("schedule", "?")})')
        log('   ℹ️ 请用 Hermes cron 命令逐个添加，或合并到 jobs.json')
    else:
        log('   ✅ cron jobs 已同步')


def _scan_custom_skills(hermes_home: Path) -> list[dict]:
    """扫描自定义 skills，返回清单。"""
    skills_dir = hermes_home / 'skills'
    custom = []

    for skill_file in skills_dir.rglob('SKILL.md'):
        try:
            content = skill_file.read_text(encoding='utf-8')
            # 简单解析 frontmatter
            if '---' in content:
                fm_start = content.index('---') + 3
                fm_end = content.index('---', fm_start)
                fm = content[fm_start:fm_end]

                # 只导出自定义的
                if 'author: Hermes Agent' in fm or 'author: hermes' in fm:
                    rel = skill_file.relative_to(skills_dir)
                    name = ''
                    desc = ''
                    for line in fm.split('\n'):
                        if line.startswith('name:'):
                            name = line.split(':', 1)[1].strip()
                        if line.startswith('description:'):
                            desc = line.split(':', 1)[1].strip()

                    custom.append({
                        'name': name or rel.parent.name,
                        'path': str(rel.parent),
                        'description': desc[:100],
                        'file': str(skill_file),
                    })
        except Exception:
            pass

    return custom


def _build_env_summary(shared_root: Path, hermes_home: Path) -> dict:
    """构建环境摘要。"""
    return {
        'timestamp': datetime.now(TZ).isoformat(),
        'shared_root': str(shared_root),
        'hermes_home': str(hermes_home),
        'shared_scripts': len(list((shared_root / 'scripts').glob('*.py'))) if (shared_root / 'scripts').exists() else 0,
        'shared_skills': len(list((shared_root / 'capabilities' / 'skills').rglob('SKILL.md'))) if (shared_root / 'capabilities' / 'skills').exists() else 0,
        'local_skills_total': len(list((hermes_home / 'skills').rglob('SKILL.md'))) if (hermes_home / 'skills').exists() else 0,
        'local_skills_custom': len(_scan_custom_skills(hermes_home)),
        'cron_jobs': len(json.loads((hermes_home / 'cron' / 'jobs.json').read_text()).get('jobs', [])) if (hermes_home / 'cron' / 'jobs.json').exists() else 0,
        'curated_facts': len(list((shared_root / 'curated' / 'memory' / 'facts').glob('*.md'))) if (shared_root / 'curated' / 'memory' / 'facts').exists() else 0,
    }


def _export_cron_if_changed(shared_root: Path, hermes_home: Path) -> None:
    """检测本地 cron 变化，自动导出到 config/cron-jobs.json。"""
    local_cron = hermes_home / 'cron' / 'jobs.json'
    shared_cron = shared_root / 'config' / 'cron-jobs.json'

    if not local_cron.exists():
        return

    # 读取本地 cron jobs（清理为可移植格式）
    raw = json.loads(local_cron.read_text(encoding='utf-8'))
    local_jobs = raw.get('jobs', [])
    portable = []
    for j in local_jobs:
        clean = {
            'id': j.get('id', j.get('job_id')),
            'name': j.get('name', ''),
            'schedule': j.get('schedule', ''),
            'prompt': j.get('prompt', ''),
            'deliver': j.get('deliver', ''),
            'enabled': j.get('enabled', True),
            'skills': j.get('skills', []),
            'script': j.get('script', ''),
            'no_agent': j.get('no_agent', False),
            'workdir': j.get('workdir', ''),
        }
        clean = {k: v for k, v in clean.items() if v}
        portable.append(clean)

    # 比较是否有变化
    if shared_cron.exists():
        try:
            existing = json.loads(shared_cron.read_text(encoding='utf-8'))
            # 比较 id 集合和 prompt 内容
            existing_ids = {j.get('id') for j in existing}
            local_ids = {j.get('id') for j in portable}
            if existing_ids == local_ids:
                # 检查 prompt 是否变化
                existing_prompts = {j.get('id'): j.get('prompt', '') for j in existing}
                local_prompts = {j.get('id'): j.get('prompt', '') for j in portable}
                if existing_prompts == local_prompts:
                    return  # 无变化
        except Exception:
            pass

    # 有变化，导出
    shared_cron.parent.mkdir(parents=True, exist_ok=True)
    shared_cron.write_text(
        json.dumps(portable, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )
    log(f'   📋 cron 变化已导出 → config/cron-jobs.json ({len(portable)} 个 job)')

    # 自动 git add（不 commit，留给 auto-commit 脚本）
    result = run('git add config/cron-jobs.json', cwd=shared_root)
    if result.returncode == 0:
        log('   ✅ 已 git add')


def _env_check(shared_root: Path, hermes_home: Path) -> None:
    """环境完整性检查。"""
    log('🔍 环境检查...')
    issues = []

    # 1. shared hub
    if (shared_root / '.git').exists():
        log('   ✅ shared hub: git repo')
    else:
        issues.append('shared hub 不是 git repo')

    # 2. 关键脚本
    critical_scripts = [
        'reflection_engine.py',
        'github_learning_orchestrator.py',
        'generate_daily_instruction.py',
        'reading_plan_orchestrator.py',
    ]
    for script in critical_scripts:
        if (shared_root / 'scripts' / script).exists():
            log(f'   ✅ scripts/{script}')
        else:
            issues.append(f'缺少 scripts/{script}')

    # 3. 关键 skill
    critical_skills = [
        'autonomous-learning/self-reflection-engine',
        'autonomous-learning/orchestrator-protocol',
    ]
    for skill in critical_skills:
        skill_path = shared_root / 'capabilities' / 'skills' / skill / 'SKILL.md'
        if skill_path.exists():
            log(f'   ✅ skills/{skill}')
        else:
            issues.append(f'缺少 skills/{skill}')

    # 4. 本地 Hermes
    if (hermes_home / 'config.yaml').exists():
        log('   ✅ Hermes config.yaml')
    else:
        issues.append('缺少 Hermes config.yaml')

    if (hermes_home / 'cron' / 'jobs.json').exists():
        log('   ✅ Hermes cron jobs.json')
    else:
        issues.append('缺少 Hermes cron jobs.json')

    # 5. Python 依赖
    try:
        import json, pathlib  # noqa
        log('   ✅ Python 标准库')
    except ImportError:
        issues.append('Python 环境异常')

    # 总结
    if issues:
        log(f'⚠️ 发现 {len(issues)} 个问题:')
        for issue in issues:
            log(f'   - {issue}')
    else:
        log('✅ 环境完整，无问题')


# ── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='共享中台一键同步工具')
    parser.add_argument('action', choices=['init', 'sync', 'export', 'check'],
                        help='init: 新环境接入; sync: 同步更新; export: 导出配置; check: 环境检查')
    parser.add_argument('--shared-root', type=Path, default=DEFAULT_SHARED_ROOT,
                        help='共享中台根目录')
    parser.add_argument('--hermes-home', type=Path,
                        default=Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')),
                        help='Hermes 配置目录')
    args = parser.parse_args()

    if args.action == 'init':
        cmd_init(args.shared_root, args.hermes_home)
    elif args.action == 'sync':
        cmd_sync(args.shared_root, args.hermes_home)
    elif args.action == 'export':
        cmd_export(args.shared_root, args.hermes_home)
    elif args.action == 'check':
        cmd_check(args.shared_root, args.hermes_home)


if __name__ == '__main__':
    main()
