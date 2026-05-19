# Weekly core-memory promotion cadence

Use this when governing shared hub v2 summaries, promotion, and slimming.

## Cadence decision

The durable cadence confirmed in session:

- **Daily** produces a summary and candidate pool only.
- **Weekly** is the normal content-promotion point: review the last 7 days, decide accepted/deferred/rejected/duplicate/disputed, then promote only accepted items to core memory.
- **Monthly** is a structure/health review only: slimming, stale/disputed facts, runtime size, tracked raw/bulk, and shared skill reference pressure.

## Practical rules

1. Do not let daily jobs write `curated/memory` directly.
2. Do not treat monthly review as the default content-promotion gate; monthly should keep the structure healthy.
3. Weekly review may update:
   - `curated/memory/facts/`
   - `curated/memory/projects/`
   - `curated/memory/MEMORY.md` index entries
   - `capabilities/skills/`
4. Weekly review must preserve traceability: source daily summary/candidate, decision reason, evidence, and verification result.
5. After governance cadence changes, verify with:

```bash
python3 -m unittest tests/test_fact_governance.py
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
git diff --check
```

## Pitfall

If a user says “每周总结复盘到核心记忆中”, encode it as **daily summary → weekly core-memory promotion → monthly health review**, not as “monthly promotion” or “daily auto-promotion”.
