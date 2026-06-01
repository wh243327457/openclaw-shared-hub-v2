#!/usr/bin/env python3
"""Generate safe reflection candidates from curated/runtime signals.

This worker never writes active curated facts. It only emits candidate JSONL under runtime.
"""
from __future__ import annotations
import argparse, json, datetime
from pathlib import Path

def now(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
def frontmatter(text):
    if not text.startswith('---\n'): return {}
    end=text.find('\n---',4)
    if end==-1: return {}
    data={}
    for raw in text[4:end].splitlines():
        if ':' in raw and not raw.startswith((' ','-')):
            k,v=raw.split(':',1); data[k.strip()]=v.strip().strip('"\'')
    return data

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--limit', type=int, default=20)
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    out_dir=root/'runtime/hermes/reflect-candidates'
    out_dir.mkdir(parents=True,exist_ok=True)
    out_file=out_dir/(datetime.datetime.now().strftime('%Y-%m-%d')+'.jsonl')
    candidates=[]
    for p in sorted(list((root/'curated/memory/facts').glob('*.md'))+list((root/'curated/memory/projects').glob('*.md'))):
        text=p.read_text(encoding='utf-8',errors='replace')
        fm=frontmatter(text)
        missing=[]
        for key in ['evidence_refs','source_paths','review_status','topic','confidence']:
            if key not in fm: missing.append(key)
        if missing:
            candidates.append({
                'candidate_id': datetime.datetime.now().strftime('%Y%m%d')+'-reflect-'+p.stem,
                'candidate_type':'metadata_gap',
                'path':str(p.relative_to(root)),
                'summary':'Curated entry lacks claim metadata: '+', '.join(missing),
                'missing':missing,
                'safety':{'auto_apply_allowed':False,'writes_curated':False,'secret_checked':'not_applicable'},
                'suggested_action':'review_and_optionally_add_evidence_refs_or_claim_metadata',
                'created_at':now()
            })
        if len(candidates)>=args.limit: break
    with out_file.open('a',encoding='utf-8') as f:
        for c in candidates:
            f.write(json.dumps(c,ensure_ascii=False)+'\n')
    result={'ok':True,'mode':'candidate-only','output':str(out_file),'count':len(candidates),'candidates':candidates}
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else result)
if __name__=='__main__': main()
