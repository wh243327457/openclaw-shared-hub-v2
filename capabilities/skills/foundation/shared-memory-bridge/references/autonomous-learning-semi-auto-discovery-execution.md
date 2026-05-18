# Autonomous Learning Semi-Auto Discovery Execution Pattern

Context: after a plan-only semi-auto candidate packet is approved by the user/controller, execute exactly one low-risk discovery run before any deeper automation.

## When to use

Use this pattern when autonomous-learning is in semi-auto mode and the user says to continue after reviewing a candidate packet.

## Safe execution sequence

1. Read the selected `orchestrator-runs/<run_id>/instruction.md` and `run-state.json`.
2. Confirm the run is low-risk discovery and still has these gates false unless explicitly approved for this single run:
   - `cron_allowed`
   - `curated_promotion_allowed`
   - `external_notification_allowed`
   - `shared_skill_update_allowed`
3. Mark only `execution_allowed=true` for this run after user/controller approval.
4. Execute the discovery agent with a bounded prompt:
   - maximum 3 candidates
   - no deep analysis
   - runtime/inbox outputs only
   - explicit uncertainty field
   - completion marker required
5. Save executor stdout/stderr as runtime evidence under the run directory.
6. Require the raw discovery output to include:
   - `task_id`
   - `sources_checked`
   - `candidates`
   - `evidence_urls`
   - `uncertainty`
   - `raw_notes_path` when available
   - `completed: true/false`
   - `OPENCLAW_DISCOVERY_DONE`
7. Hermes performs Spec Review first, then Quality Review.
8. Update `run-state.json` and `state.json` with the reviewed runtime-only status.
9. Run JSON validation plus `promoter.py --dry-run` and `verify_bridge.py`.
10. Report plan → execution → audit → result → learning, without claiming curated promotion or full automation.

## OpenClaw discovery prompt shape

For OpenClaw container execution, prefer canonical shared paths inside the container:

- Runtime output: `/home/node/.openclaw/shared/runtime/openclaw/autonomous-learning/canary-outputs/<run_id>.md`
- Inbox output: `/home/node/.openclaw/shared/inbox/openclaw/daily/<date>-autonomous-learning-<topic>.md`

Prompt constraints should say:

```text
只做轻量 discovery，不做深度源码分析。
最多给出 3 个候选。
不写 curated memory。
不启用 cron。
不外发通知。
不创建或更新 shared skills。
如果不能联网或检索不足，请明确 uncertainty，不要编造。
```

## Review verdict language

If the discovery output satisfies required fields but has network or source coverage limits, use:

- Spec Review: `PASS_WITH_NOTES`
- Quality Review: `APPROVED_FOR_RUNTIME_LEARNING_NOT_CURATED_PROMOTION`

Do not promote to curated when candidate details are not independently verified.

## Important pitfall

Intermittent fetch/DNS errors during discovery should be captured as uncertainty and review notes, not hardened as a durable claim that GitHub/OpenClaw is broken. The durable lesson is: proceed with runtime-only evidence and require later verification before deep read or promotion.
