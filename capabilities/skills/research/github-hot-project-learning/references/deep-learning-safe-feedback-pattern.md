# Deep-learning safe feedback pattern

This reference captures the reusable learning-loop upgrade where external project research becomes actionable system improvement without letting the execution agent mutate production state.

## Pattern

Daily learning and daily inspection should move from summary-only output to:

```text
deep reading -> mechanism abstraction -> candidate feedback -> Hermes review -> safe landing
```

## Required output for OpenClaw / execution agent

For each deep-read object, require:

1. **Object and evidence**
   - Project/tool/mechanism/failure case name.
   - At least two source types when possible: README/docs/release/issues/source tree.
   - Query time and links.

2. **Mechanism abstraction**
   - Do not just list features.
   - Extract rules in the form: `当……时，应优先……，因为……，边界是……`.

3. **Feedback classification**
   - candidate fact
   - candidate skill/workflow
   - runtime POC
   - open question
   - do-not-land / observation only

4. **Safety boundary**
   - Execution agent must not modify config/provider/model/cron/secret.
   - Execution agent must not write active curated facts.
   - License-unclear source is mechanism-only; no source copying.

5. **Hermes second pass**
   - Hermes applies shared governance gates before Obsidian/curated/skill landing.
   - Failed or uncertain items stay in runtime/inbox.

## Push / reporting note

When the learning result cannot be pushed because platform push guard is active, say explicitly that content was generated and saved but Weixin was not actually sent. Do not bypass push guard or claim delivery success.
