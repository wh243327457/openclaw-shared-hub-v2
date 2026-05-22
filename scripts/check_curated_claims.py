#!/usr/bin/env python3
"""Warning-only checker for curated claim frontmatter.

This script intentionally does not fail on missing claim metadata during rollout.
It emits JSON so Hermes/OpenClaw can use it in dashboards and reviews.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

REQUIRED = [
    'claim_id','claim_type','status','confidence','scope','lens','topic',
    'source_agent','source_paths','evidence_refs','sensitivity',
    'created_at','updated_at','review_status'
]
ALIASES = {'claim_id':['fact_id'], 'evidence_refs':['source'], 'updated_at':['last_verified_at']}
STATUS_OK = {'active','retired','disputed','superseded','deleted'}


def parse_frontmatter(text: str) -> dict:
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---', 4)
    if end == -1:
        return {}
    block = text[4:end]
    data = {}
    last_key = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        if raw.startswith((' ', '-')):
            continue
        if ':' in raw:
            k, v = raw.split(':', 1)
            data[k.strip()] = v.strip().strip('"\'')
            last_key = k.strip()
    return data

def has_key(data, key):
    if key in data:
        return True
    return any(alias in data for alias in ALIASES.get(key, []))

def scan(root: Path):
    targets = list((root/'curated/memory/facts').glob('*.md')) + list((root/'curated/memory/projects').glob('*.md'))
    items=[]
    for p in sorted(targets):
        rel=str(p.relative_to(root))
        text=p.read_text(encoding='utf-8', errors='replace')
        fm=parse_frontmatter(text)
        missing=[k for k in REQUIRED if not has_key(fm,k)]
        warnings=[]
        if not fm:
            warnings.append('missing_frontmatter')
        if missing:
            warnings.append('missing_claim_fields:'+','.join(missing))
        status=fm.get('status')
        if status and status not in STATUS_OK and status not in {'draft','approved'}:
            warnings.append('unknown_status:'+status)
        if 'evidence_refs' not in fm and 'source' not in fm:
            warnings.append('missing_structured_evidence_refs')
        items.append({'path':rel,'frontmatter':bool(fm),'missing':missing,'warnings':warnings})
    return {'ok': True, 'mode':'warning-only', 'total':len(items), 'warning_count':sum(bool(i['warnings']) for i in items), 'items':items}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    result=scan(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok={result['ok']} mode={result['mode']} total={result['total']} warnings={result['warning_count']}")
        for item in result['items']:
            if item['warnings']:
                print('WARN', item['path'], '; '.join(item['warnings']))
if __name__=='__main__':
    main()
