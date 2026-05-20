# Continue-from-plan iteration pattern

Session: 2026-05-19 learning-promotion integration.

## Trigger

User says a short “继续” after a plan has already been created and partially executed.

## Lesson

Do not ask which branch to continue if the plan already defines a next step. Interpret “继续” as: read the current plan/state, execute the next pending step, update plan/state, and run verification.

## Pattern

1. Load/read the plan truth source and the current runtime state.
2. Identify the first pending or next safe step.
3. Execute that step with minimal scope.
4. Immediately update:
   - parent plan
   - subplan, if any
   - machine-readable state JSON
   - inbox/runtime note when useful
5. Run verification:
   - JSON parsing for touched state files
   - `promoter.py --dry-run`
   - `promoter.py`
   - `verify_bridge.py`
6. Final response should be compact: what advanced, files touched, current next step, verification result.

## Avoid

- Asking the user to choose among plan branches unless the plan itself has no ordering or the next action has meaningful side effects.
- Reporting only intentions.
- Updating chat state without updating the persisted plan/state files.
