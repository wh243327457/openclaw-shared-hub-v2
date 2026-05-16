# Autonomous Learning System Rollout Notes

Session-specific rollout lessons for shared-memory-bridge class tasks: turning a long-running system design into an executable, resumable, cross-agent rollout.

## Proven file layout

Use a four-file core when turning a long-running system design into an executable, resumable rollout:

1. `curated/memory/projects/<project>.md` — long-term architecture and stable state.
2. `runtime/<agent>/<project>/implementation-plan.md` — task breakdown, phase tracking, and recovery point.
3. `runtime/<agent>/<project>/state.json` — machine-readable state machine.
4. `runtime/<agent>/<project>/templates/` — instruction, review, handoff, notification, promotion, and feedback templates.

For autonomous-learning style rollouts, add these runtime subdirectories before real dispatch:

- `dry-runs/` — manual simulation plans and instruction drafts.
- `agent-outputs/<agent>/` — real agent outputs collected by controller.
- `reviews/` — Hermes spec/quality review artifacts.
- `pending-approval/` — items requiring user approval before promotion, cron, or external push.
- `canary-runs/` — low-risk real executions before automation.

## Validated phase sequence

### Phase A — Skeleton landing

1. Create curated architecture/project note.
2. Create runtime implementation plan.
3. Create machine-readable configs (`agent-capabilities.json`, `learning-weights.json`, `learning-backlog.json`, `failover-policy.json`, `agent-health.json`, `blocked-tasks.json`, `state.json`).
4. Create role-specific templates.
5. Update `curated/memory/MEMORY.md` with an explicit project pointer.
6. Verify in this order:
   - Parse all JSON configs.
   - Run `promoter.py --dry-run`.
   - Run `promoter.py`.
   - Run `verify_bridge.py`.

### Phase B — Manual dry-run before real dispatch

Do not jump from skeleton directly to cron or real multi-agent execution. First generate controller-owned dry-run artifacts under `runtime/<agent>/<project>/dry-runs/`:

1. Daily/iteration plan derived from weights + backlog.
2. OpenClaw/browser-discovery instruction draft.
3. Claude Code/deep-analysis instruction draft.
4. Hermes self-review report.
5. Update `state.json` and `implementation-plan.md` to `PHASE_B_DRY_RUN_DONE` (or equivalent).

Dry-run artifacts must be clearly marked `DRY_RUN_ONLY` or `INSTRUCTION_ONLY_DO_NOT_EXECUTE`; they should not trigger external dispatch, notification, cron, or curated promotion.

### Phase C — Canary preparation

Before the first real small execution:

1. Check agent availability/health.
2. Create `agent-outputs/`, `reviews/`, `pending-approval/`, and `canary-runs/`.
3. Pick one low-risk task close to the system goal.
4. Execute only one narrow task.
5. Write results to runtime/inbox only.
6. Hermes performs Spec Review then Quality Review.
7. Require user approval before promotion, shared skill upgrade, cron, or external notification.

### Phase C execution lesson — controller-owned capture

For Claude Code / external-agent canaries, prefer this pattern for research or synthesis outputs:

```text
execution agent stdout -> Hermes captures stdout -> Hermes writes runtime file -> Hermes reviews
```

Do **not** make the execution agent the authority for writing shared runtime/curated files when a simple captured-output flow is enough. Direct-write canaries are more brittle: agents may hit max-turn limits, overthink path permissions, or fail before producing the target file. Controller-owned capture also keeps the promotion boundary clear.

Canary review rules:

- Execution agents may recommend promotion, but must not claim `review gates passed`, `approved for promotion`, or similar final authority.
- Hermes must treat any self-approval wording as a scope note in Spec Review.
- A successful canary proves the dispatch/review loop works; it does not prove content is stable enough for curated promotion.
- If the first real canary exposes a workflow pitfall, patch the instruction template before running a broader OpenClaw→Claude→Hermes chain.


## Template design pattern

Keep templates short and role-specific. Each instruction/review template should include:

- Purpose and role boundary.
- Inputs.
- Required output schema/fields.
- Write boundaries (especially: no direct curated writes by execution agents).
- Completion marker.
- Hermes review criteria.

For notifications, enforce the user's preferred full-flow format:

```text
计划：...
执行：...
审计：...
结果：...
收获：...
下一步：...
```

## Pitfalls found

- Do not treat `runtime` as long-term truth; it is executable state only.
- Do not update curated memory before the rollout skeleton is verified.
- Keep `implementation-plan.md`, `architecture-design-plan.md`, and `state.json` synchronized so a new model can resume from any of them.
- When updating the main index, add an explicit project pointer rather than relying on implicit discovery.
- Do not mark a dry-run as proof of agent execution quality; it only validates the protocol/instruction clarity.
- Do not enable cron, send notifications, or promote to curated from a dry-run.
- For Claude Code research/canary tasks, prefer `Claude stdout -> Hermes capture -> Hermes writes runtime file` over asking Claude Code to write shared files directly. In practice, direct writes can fail via max-turns exhaustion or conservative path/permission judgments even when Hermes has verified the directory exists and is writable.
- Execution agents must never self-declare `APPROVED_FOR_PROMOTION` or claim Hermes Spec/Quality Review gates have passed. They may only emit `promotion_recommendation: *_candidate`; Hermes owns review and promotion decisions.
- If Claude Code exits non-zero or misses a completion marker, still persist stdout/stderr into runtime so Hermes can audit the failure rather than losing evidence.
- For canary research/synthesis, avoid asking Claude Code to both generate content and write shared files if stdout capture is sufficient; Hermes should own the final write and review boundary.
- Treat execution-agent self-approval (`approved for promotion`, `review gates passed`) as a review finding, not as truth.

## Recovery-point rule

At the end of every phase, write a compact recovery point into the implementation plan:

- Current phase/status.
- Completed artifacts with paths.
- Verification results.
- Next smallest safe action.
- Whether user approval is required.
