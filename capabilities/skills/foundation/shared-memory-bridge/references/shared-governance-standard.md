# Shared governance standard compact reference

Use this when deciding how shared hub v2 governance is triggered.

## Trigger model

- **Daily summary**: runs every day; summarizes raw activity, candidates, risks, and user-decision items. It must not write curated memory or delete raw files.
- **Weekly review**: the only normal content-promotion trigger. It reviews the last 7 daily summaries/candidates and promotes accepted items into `curated/memory/facts/`, `curated/memory/projects/`, or shared skills.
- **Monthly health review**: structure-only review. It checks `MEMORY.md` length, stale/disputed facts, runtime size, tracked raw/bulk, and shared skill references.

## Hard boundary

Daily can see and summarize; weekly decides what becomes core memory; monthly keeps the structure slim.

## Verification

After governance changes, run:

```bash
python3 -m unittest tests/test_fact_governance.py
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
git diff --check
```
