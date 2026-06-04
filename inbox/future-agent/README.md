# future-agent inbox

This directory is the raw-write inbox for future-agent daily notes.

- Stable cross-agent truths belong in `curated/memory/` after review.
- Raw daily notes belong in `inbox/future-agent/daily/`.
- Runtime artifacts, caches, indexes, and temporary outputs belong in `runtime/future-agent/`.
- Do not store secrets here.
- Resolve the shared root with `scripts/resolve_shared_root.py` or `SHARED_HUB_ROOT`; do not hardcode host-specific absolute paths.
