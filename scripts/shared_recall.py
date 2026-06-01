#!/usr/bin/env python3
"""Claim-aware recall helper for shared hub v2.

Reads curated facts/projects and ranks them as strong/weak/no match.
No embedding/vector dependency; safe text + frontmatter scoring for rollout.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

STATUS_STRONG={'active','approved'}
STATUS_WEAK={'draft','retired','superseded'}
STATUS_CONFLICT={'disputed'}

def parse_frontmatter(text: str) -> tuple[dict,str]:
    if text.startswith('---\n'):
        end=text.find('\n---',4)
        if end!=-1:
            block=text[4:end]
            body=text[end+4:]
            data={}
            current=None
            for raw in block.splitlines():
                if not raw.strip() or raw.lstrip().startswith('#'): continue
                if raw.startswith((' ', '-')): continue
                if ':' in raw:
                    k,v=raw.split(':',1)
                    data[k.strip()]=v.strip().strip('"\'')
            return data,body
    return {},text

def tokenize(q):
    return [t.lower() for t in re.findall(r'[\w\u4e00-\u9fff]+', q) if len(t)>1]

def doc_text(path, fm, body):
    keys=['claim_id','fact_id','claim_type','status','scope','lens','topic','subject','attribute','value_summary','source_agent']
    return ' '.join([str(fm.get(k,'')) for k in keys])+' '+body[:4000]

def classify(score, status, has_evidence):
    if status in STATUS_CONFLICT: return 'conflict'
    if status in STATUS_STRONG and score>=4 and has_evidence: return 'strong'
    if score>=2: return 'weak'
    return 'none'

def scan(root: Path, query: str, limit: int):
    terms=tokenize(query)
    paths=list((root/'curated/memory/facts').glob('*.md'))+list((root/'curated/memory/projects').glob('*.md'))
    out=[]
    for p in paths:
        text=p.read_text(encoding='utf-8',errors='replace')
        fm,body=parse_frontmatter(text)
        hay=doc_text(p,fm,body).lower()
        score=0
        matched=[]
        for t in terms:
            if t in hay:
                score+=1
                matched.append(t)
        topic=str(fm.get('topic') or fm.get('subject') or '')
        for t in terms:
            if t in topic.lower(): score+=2
        status=fm.get('status','') or ('active' if fm else 'unknown')
        has_evidence=bool(fm.get('evidence_refs') or fm.get('source') or fm.get('source_paths') or '证据' in body or '路径' in body)
        match=classify(score,status,has_evidence)
        if score or query=='*':
            rel=str(p.relative_to(root))
            out.append({'path':rel,'match':match,'score':score,'matched_terms':matched,'status':status,'topic':topic,'scope':fm.get('scope',''),'lens':fm.get('lens',''),'has_evidence':has_evidence,'summary':fm.get('value_summary') or first_heading(body)})
    rank={'strong':0,'weak':1,'conflict':2,'none':3}
    out.sort(key=lambda x:(rank.get(x['match'],9),-x['score'],x['path']))
    return out[:limit]

def first_heading(body):
    for line in body.splitlines():
        s=line.strip('# ').strip()
        if s: return s[:160]
    return ''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('query', nargs='?', default='*')
    ap.add_argument('--root', default='.')
    ap.add_argument('--limit', type=int, default=10)
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    res={'query':args.query,'results':scan(Path(args.root).resolve(),args.query,args.limit)}
    if args.json: print(json.dumps(res,ensure_ascii=False,indent=2))
    else:
        print(f"query={args.query} results={len(res['results'])}")
        for r in res['results']:
            print(f"[{r['match']}] score={r['score']} {r['path']} :: {r['summary']}")
if __name__=='__main__': main()
