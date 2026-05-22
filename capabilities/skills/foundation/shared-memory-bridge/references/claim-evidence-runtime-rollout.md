# Claim / Evidence / Runtime-only Rollout Pattern

This reference captures the reusable pattern from the Elephant Agent mechanism rollout into shared hub v2. Use it for future upgrades to long-term memory governance.

## When to use

Use this pattern when improving shared/curated memory, recall, promotion, reflection, or dashboarding without risking production behavior.

## Low-risk rollout sequence

1. **Baseline first**
   - Scan existing `curated/memory/facts/` and `curated/memory/projects/`.
   - Count frontmatter coverage, status fields, evidence-like text, and missing structured evidence.
   - Write reports under `runtime/<agent>/<project>/`, not curated.

2. **Schema as target, not migration**
   - Add a schema doc, e.g. `docs/curated-fact-claim-schema.md`.
   - Treat it as the target format for new claims.
   - Keep old facts warning-only until a human selects high-value items to migrate.

3. **Evidence-backed candidate template**
   - Add a candidate template that includes source paths, evidence refs, gates, decision notes, and `auto_apply_allowed: false`.
   - Daily learning,巡检,dreaming,reflection should produce candidates only.

4. **Warning-only checker**
   - Add a deterministic checker such as `scripts/check_curated_claims.py`.
   - It should emit JSON and warnings, not fail production validation during rollout.

5. **Recall before vector**
   - Start with frontmatter/text recall such as `scripts/shared_recall.py`.
   - Return explicit match classes: `strong`, `weak`, `conflict`, `none`.
   - Keep vector/sqlite-vec deferred until scale or quality actually requires it.

6. **Open questions as runtime**
   - Store unresolved uncertainty in `runtime/<agent>/open-questions/`.
   - Do not turn uncertainty directly into curated facts.

7. **Reflect worker as candidate-only**
   - Reflection jobs may find metadata gaps, stale reviews, possible conflicts, or retire candidates.
   - They must write JSONL under runtime only and never mutate curated active facts.

8. **Dashboard for review**
   - Generate a mini dashboard under runtime summarizing curated counts, warnings, open questions, and reflect candidates.
   - Use it to pick a small set of high-value facts for manual evidence-ref enrichment.

## Required safety boundaries

- Do not enable new cron during governance rollout unless explicitly approved.
- Do not auto-migrate old facts in bulk.
- Do not auto-write `active` curated facts from assistant-authored prose.
- Do not modify config/provider/model/secret files as part of memory-governance rollout.
- Do not copy source from external projects with unclear license; use clean-room mechanism borrowing.

## Verification bundle

From `<shared-root>` run at minimum:

```bash
python3 -m py_compile scripts/check_curated_claims.py scripts/shared_recall.py scripts/open_questions.py scripts/reflect_candidate_worker.py scripts/shared_memory_dashboard.py
python3 scripts/check_curated_claims.py --json
python3 scripts/shared_recall.py "共享中台 evidence" --json
python3 scripts/open_questions.py list --json
python3 scripts/reflect_candidate_worker.py --json
python3 scripts/shared_memory_dashboard.py --json
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
git diff --check
```

## Reporting language

Report warnings as expected rollout pressure when they come from legacy entries. Do not frame warning-only missing `evidence_refs` as failure unless `verify_bridge.py` fails or the user asked for strict migration.
