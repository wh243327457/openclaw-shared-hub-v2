# Claim Warning Observation

This reference captures the rollout-phase pattern for shared memory warning analysis.

## What warning-only usually means

When `check_curated_claims.py` reports many warnings after introducing claim schema, the majority are usually not runtime failures. They typically indicate:

- legacy facts/projects still lacking claim frontmatter
- partially upgraded entries missing `claim_type`, `topic`, `source_paths`, `evidence_refs`, or `review_status`
- a few status values using old workflow labels that are not yet in the new enum

## Practical interpretation pattern

1. Group warnings by missing field.
2. Separate fully unstructured entries from partially upgraded entries.
3. Prioritize shared infrastructure facts and high-frequency operational facts first.
4. Do not bulk migrate everything in one sweep.
5. Re-run the warning checker after each small patch to verify real downward movement.

## What to do with the result

- Track the observation in a visible plan/todo, not only in chat.
- Use the dashboard to watch whether warning count drops.
- Keep vector/sqlite-vec deferred until text recall quality or scale is actually a bottleneck.

## Example warning clusters seen during rollout

- missing `claim_type`, `lens`, `topic`, `source_paths`, `review_status`
- missing `evidence_refs` on otherwise stable facts
- missing frontmatter on older facts/projects
- old project status values such as `approved_plan_landed` or `in_progress`
