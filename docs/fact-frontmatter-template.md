# Shared v2 Fact Frontmatter Template

Use this template only after a candidate has passed manual/controller review. Automation may suggest these fields, but must not write accepted curated facts without approval.

```yaml
---
fact_id: shared-v2-example-fact
status: active              # active | stale | superseded | disputed | deprecated
freshness_class: operational # static | slow_changing | operational | volatile
scope: shared-hub           # global | hermes | openclaw | future-agent | shared-hub | project:<name>
subject: shared-v2.example
attribute: behavior
value_summary: "Short human-readable value, no secrets"
created_at: 2026-05-16T00:00:00+08:00
updated_at: 2026-05-16T00:00:00+08:00
last_verified_at: 2026-05-16T00:00:00+08:00
review_due_at: 2026-06-16T00:00:00+08:00
source_refs:
  - inbox/hermes/daily/YYYY-MM-DD.md
conflict:
  status: none              # none | detected | evidence_requested | merge_needed | supersede_pending | resolved | disputed
  type: null                # direct | temporal | scope | authority | evidence_quality | duplicate_wording | secret_sensitive
  conflicting_fact_ids: []
  conflicting_candidate_refs: []
  resolution: null
  resolved_by: null
  resolved_at: null
supersedes: []
superseded_by: null
confidence: high            # low | medium | high
authority: hermes-controller # user | filesystem | official_doc | hermes-controller | openclaw | future-agent | external-doc
secret_checked: true
---
```

Rules:

- `review_due_at` is a review reminder, not a deletion TTL.
- `stale` does not mean false; it means review is needed.
- `disputed` must not be used as default truth in retrieval.
- `superseded` facts stay for audit trail but should not be preferred.
- Never place raw API keys, tokens, passwords, cookies, or private keys in `value_summary` or `source_refs`.
