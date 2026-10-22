# Execute and verify a checkpoint

Read the mission and last verified checkpoint. Check pause/stop state first.
If another live run owns the mission, do not write; use a separate target or
wait for explicit handoff. A timestamp alone does not establish that it died.

Choose the next meaningful action from the outcome and current evidence.
Discovery is optional when the user already supplied a concrete task. Do not
rotate tools mechanically or invent cleanup work to keep the loop busy.

Use the smallest coherent change or investigation. Record the hypothesis or
question, affected targets, expected result, and decisive check when the work
requires design or diagnosis. A tiny edit needs no separate proposal file.
Use the proposal template only when a proposal materially helps review.

Apply authorized work, then verify according to profiles.md. Distinguish:

- `progress`: a useful checkpoint passed, but some criteria remain.
- `no_candidate`: discovery found nothing actionable; it is not completion.
- `no_change`: a monitoring pass succeeded and found no relevant delta.
- `blocked`: required input/access is unavailable; preserve unresolved criteria.
- `failed`: the attempted change or check failed; preserve evidence and edits.
- `goal_verified`: all mission criteria passed against current artifacts.

`status` describes lifecycle; `last_result` describes the checkpoint outcome:

| Situation | status | last_result |
|---|---|---|
| Not started | fresh | null |
| Executing a checkpoint | running | previous result or null |
| Checkpoint ended with more work / successful monitoring | idle | progress / no_candidate / no_change |
| Required user input or access is missing | escalated | blocked |
| Failed/interrupted work is preserved for recovery | interrupted | failed |
| Finite mission fully verified | done | goal_verified |
| User paused or aborted | paused / aborted | keep the last observed result |

For an explicitly scoped research report, unresolved facts can be findings rather
than unmet deliverables; use the acceptance boundary in profiles.md. Do not use
`status: blocked`, which is not part of the state lifecycle.

A missing tool, inaccessible page, or failed query is not an empty result.
When a check fails, distinguish a regression from a pre-existing/environment
failure. Preserve changes for inspection; fix within scope or hand off.
Add a NOT-OK lesson only after establishing its conditions and cause. Do not
turn transient network errors into a permanent prohibition.

Update the journal and state with criterion IDs, target versions, methods,
results, evidence locations, and unresolved work. Do not record a check as
passed if it was skipped. Checks describe the actual command/reading/inspection,
not a command the model merely proposes. The state checker validates records;
it does not independently execute checks or prove their truth.

For a new state, use schema_version 1. Keep a finite set of criterion IDs in
`criteria`; `verification` contains the latest result per criterion. Only set
`status: done` with `last_result: goal_verified` when every criterion has a
passing record. `target_version` can be a commit plus dirty diff hash, document
revision/file hash, or dated research snapshot. Do not reuse stale evidence
following a relevant edit. A verified goal may be idle only for an ongoing
monitoring mission; an individual no-change pass never completes that mission.

A passing record has this shape (replace values with actual observations):

```json
{
  "criterion": "C1",
  "outcome": "pass",
  "method": "Read the cited source and compare the claim",
  "target_version": "report revision or source snapshot identifier",
  "evidence": "journal entry or captured check result"
}
```

Use `fail` or `unverified` when a check does not establish the criterion. An
existing passing record must not hide a newer failed or skipped check.

Write state using a temporary file in the same directory followed by atomic
replacement, preserving the previous state if writing/validation fails. Do not
follow symlinks or overwrite a journal owned by another run. This is a
single-writer convention, not a distributed lock or security boundary. If
concurrent ownership cannot be established, stop before modifying the target.

End with a short handoff: outcome, decisive evidence, remaining criteria, next
action. Preserve legacy cycle_count/heartbeat fields where useful. Set
next_wakeup_at only from a confirmed schedule; null otherwise. Continuing within
a native goal needs no fabricated wakeup. Stop at the agreed boundary; do not
start a new initiative after completing the mission.
