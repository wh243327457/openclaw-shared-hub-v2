#!/usr/bin/env python3
"""Generate a mini dashboard for shared memory health."""
from __future__ import annotations
import argparse, json, datetime, subprocess
from pathlib import Path

def count_files(p, glob='*.md'):
    return len(list(p.glob(glob))) if p.exists() else 0

def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    runtime = root / 'runtime/hermes/shared-memory-dashboard'
    runtime.mkdir(parents=True, exist_ok=True)

    facts = count_files(root / 'curated/memory/facts')
    projects = count_files(root / 'curated/memory/projects')
    inbox = {a: count_files(root / f'inbox/{a}/daily') for a in ['hermes', 'openclaw', 'future-agent']}
    oq = load_json(root / 'runtime/hermes/open-questions/questions.json') or {'questions': []}

    reflect_files = list((root / 'runtime/hermes/reflect-candidates').glob('*.jsonl'))
    reflect_count = 0
    for f in reflect_files:
        reflect_count += sum(1 for _ in f.open(encoding='utf-8', errors='ignore'))

    try:
        out = subprocess.check_output(['python3', 'scripts/check_curated_claims.py', '--json'], cwd=root, text=True)
        claims_json = json.loads(out)
    except Exception as e:
        claims_json = {'ok': False, 'error': str(e), 'total': 0, 'warning_count': 0}

    generated_at = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
    data = {
        'generated_at': generated_at,
        'curated': {'facts': facts, 'projects': projects, 'total': facts + projects},
        'inbox_daily_files': inbox,
        'claim_check': {
            'ok': claims_json.get('ok'),
            'mode': claims_json.get('mode'),
            'total': claims_json.get('total'),
            'warning_count': claims_json.get('warning_count'),
        },
        'open_questions': {
            'total': len(oq.get('questions', [])),
            'open': sum(1 for q in oq.get('questions', []) if q.get('status') == 'open'),
        },
        'reflect_candidates': {'jsonl_files': len(reflect_files), 'total_records': reflect_count},
        'phase7_vector_status': 'deferred; trigger only if text recall becomes insufficient or curated total grows substantially',
    }
    (runtime / 'dashboard.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# Shared Memory Mini Dashboard',
        '',
        f'Generated: {generated_at}',
        '',
        '## Status Snapshot',
        '',
        '| Area | Value |',
        '|---|---:|',
        f"| curated facts | {facts} |",
        f"| curated projects | {projects} |",
        f"| curated total | {facts + projects} |",
        f"| claim check warnings | {data['claim_check'].get('warning_count')} / {data['claim_check'].get('total')} |",
        f"| open questions | {data['open_questions']['open']} / {data['open_questions']['total']} |",
        f"| reflect candidates | {reflect_count} |",
        f"| Hermes inbox daily files | {inbox['hermes']} |",
        f"| OpenClaw inbox daily files | {inbox['openclaw']} |",
        f"| future-agent inbox daily files | {inbox['future-agent']} |",
        '',
        '## Interpretation',
        '',
        '- Claim metadata rollout is active but warning-only.',
        '- Evidence-backed promotion now has a template and checker.',
        '- Recall helper is text/frontmatter based; vector remains deferred.',
        '- Reflect worker only generates runtime candidates and does not mutate curated facts.',
        '',
        '## Next Review',
        '',
        '- Prioritize adding `evidence_refs` to high-value active facts.',
        '- Review open questions weekly.',
        '- Consider vector/sqlite-vec only after text recall quality or scale becomes a real bottleneck.',
        '',
    ]
    (runtime / 'dashboard.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else '\n'.join(lines))

if __name__ == '__main__':
    main()
