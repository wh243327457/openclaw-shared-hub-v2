#!/usr/bin/env python3
"""Manage shared hub open questions in runtime only.

Open questions are uncertainty records for future review. They are not curated facts.
"""
from __future__ import annotations
import argparse, json, datetime, re
from pathlib import Path

def now(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
def load(path):
    if not path.exists(): return {'version':1,'questions':[]}
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def qid(topic):
    slug=re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+','-',topic).strip('-').lower()[:40] or 'question'
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+slug

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('action', choices=['list','add','resolve','export'])
    ap.add_argument('--root', default='.')
    ap.add_argument('--topic')
    ap.add_argument('--question')
    ap.add_argument('--source', default='manual')
    ap.add_argument('--id')
    ap.add_argument('--resolution')
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    path=Path(args.root).resolve()/'runtime/hermes/open-questions/questions.json'
    data=load(path)
    if args.action=='add':
        if not args.topic or not args.question: raise SystemExit('--topic and --question required')
        rec={'id':qid(args.topic),'topic':args.topic,'question':args.question,'status':'open','source':args.source,'created_at':now(),'updated_at':now(),'resolution':''}
        data['questions'].append(rec); save(path,data); result=rec
    elif args.action=='resolve':
        if not args.id: raise SystemExit('--id required')
        result=None
        for q in data['questions']:
            if q['id']==args.id:
                q['status']='resolved'; q['resolution']=args.resolution or ''; q['updated_at']=now(); result=q; break
        if not result: raise SystemExit('id not found')
        save(path,data)
    elif args.action=='export':
        out=Path(args.root).resolve()/'runtime/hermes/open-questions/open-questions.md'
        lines=['# Open Questions','', 'Runtime-only uncertainty queue. Do not treat as curated facts.','']
        for q in data['questions']:
            lines += [f"## {q['id']} — {q['topic']}", f"- status: {q['status']}", f"- source: {q.get('source','')}", f"- question: {q['question']}", f"- resolution: {q.get('resolution','')}", '']
        out.write_text('\n'.join(lines),encoding='utf-8'); result={'exported':str(out),'count':len(data['questions'])}
    else:
        result=data
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else result)
if __name__=='__main__': main()
