# Session note: landing prioritization and runtime-only scaffolding

Date: 2026-05-17

## Trigger
The user asked whether multiple rounds of autonomous learning had produced anything actually applied, then asked to continue整理 and execute the landing plan.

## Durable lessons

### 1. Separate “learned” from “landed”
When reviewing learning pipelines, classify each item by operational status instead of summarizing all outputs equally:

| Class | Meaning |
|---|---|
| Landed / running | Has cron/script/runtime artifacts and verification path |
| Runtime scaffold | Has state/plan/templates but no cron/curated promotion |
| Planned | Curated design exists but no runtime directory or manual run |
| Local capability candidate | Useful workflow, but not yet cross-agent shared |

This avoids over-claiming that a learning note is already operational.

### 2. Good landing order
For this user’s multi-agent learning system, the practical sequence is:
1. Shared governance / bridge / reporting conventions
2. Existing GitHub learning loop hardening
3. Autonomous-learning runtime state and review gates
4. New OpenClaw web/watch minimal runtime scaffold
5. CodeGraph / bounded subagent as local capability before shared promotion

### 3. Runtime-only scaffold pattern
For a new system that is promising but not yet validated, create the minimal runtime bundle first:

```text
runtime/<agent>/<project>/
├── state.json
├── implementation-plan.md
├── instruction.md
├── report-template.md
├── sample-output.md
└── source-registry.md   # if discovery/source-based
```

Default gates:
- `cron_allowed: false`
- `curated_promotion_allowed: false`
- manual dry-run required before automation

### 4. CodeGraph capability judgment
CodeGraph should be judged as a local high-value code exploration capability before being promoted to shared. Evidence path:
- `src/search/query-parser.ts`: field-qualified query parsing and bounded edit distance
- `src/db/queries.ts`: SQLite/FTS query execution with parsed filters
- `src/context/index.ts`: natural-language task → exact/text search → subgraph → code blocks
- `src/mcp/server-instructions.ts`: tool routing guidance; `codegraph_context` is primary
- `src/mcp/tools.ts`: MCP tools including search/context/callers/callees/impact/node/explore

Promote to shared only after it is used across more than one agent workflow, not merely after one source read.

### 5. Push/report readability matters
The user explicitly disliked a cron learning report that stacked many long bullet paragraphs. Future autonomous-learning notifications should be short, table-first, and put paths at the end.
