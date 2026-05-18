# Shared hub slimming iteration

Use this when auditing or optimizing a live shared hub that has become cognitively heavy or Git-heavy.

## Key distinction

Do not treat the whole shared directory as one class of asset. Split it into three mental layers:

```text
core/truth: curated + capabilities + manifest + AGENTS + core scripts/docs
edge/compat: memory + skills + compat as thin compatibility entries
bulk/raw: inbox + runtime + dreams/logs/cache/indexes
```

Core can be reviewed and committed. Bulk should generally stay out of mainline Git and should be summarized or promoted into curated facts/projects only after human/agent review.

## Iterative slimming sequence

1. **Plan first**: write a recoverable plan under `docs/plans/YYYY/MM/` with phase status. Do not start by deleting files.
2. **Phase 1 — stop the bleeding**: add `.gitignore` rules and governance text so new bulk does not enter `git status`:
   - `inbox/**/daily/dreaming/`
   - `compat/daily/dreaming/`
   - `inbox/**/daily/.dreams/`
   - `compat/daily/.dreams/`
   Keep already tracked files for a later dedicated PR.
3. **Phase 2 — thin compat**: make `compat/` a compatibility view, not a data store. Prefer `README.md` plus symlinks; remove tracked historical compat bulk with `git rm --cached` only after review. Also ignore legacy `compat/daily/20*.md` snapshots when they are kept locally for compatibility.
4. **Phase 3 — slim `MEMORY.md`**: keep it as an index and state block. Move `Promoted From Short-Term Memory` / score/source noise to an archive or curated fact/project summaries.
5. **Phase 4 — raw retention**: keep inbox as raw write input but stop making it a long-term reviewed corpus. Promote summaries to curated; leave raw local or archived.
6. **Phase 5 — shared skill governance**: shared skills are class-level contracts, not session logs. Merge repetitive references into class-level reference docs.
7. **Phase 6 — automated warnings**: teach `verify_bridge.py` to report top-level size, tracked bulk counts, runtime size, MEMORY line count, and oversized skill reference sets.
8. **Phase 7 — branch cleanup**: only delete remote branches after their PRs are merged and main carries the reviewed content.

## Verification pattern

Before and after each phase:

```bash
cd <shared-root>
git diff --check
python3 scripts/promoter.py --dry-run
python3 scripts/verify_bridge.py
readlink memory/MEMORY.md
readlink memory/facts
readlink memory/projects
readlink memory/daily
readlink skills
readlink compat/daily/.dreams
```

For ignore-rule changes, create temporary files under ignored dreaming paths and confirm `git status --short -- <file>` is empty, then delete the temp files.

## Pitfalls

- Do not remove historical bulk in the same PR that introduces the plan. First stop future growth; then remove tracked bulk in separate PRs.
- Do not equate `git rm --cached` with deletion. Prefer it when the goal is to keep local raw files but remove them from Git review.
- Do not let `compat/` become a second source of truth. It should bridge old paths to canonical locations.
- Do not let `curated/memory/MEMORY.md` accumulate raw promoted excerpts. It should be an entrypoint, not a transcript store.
