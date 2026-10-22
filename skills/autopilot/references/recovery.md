# Status, pause, and recovery

Status is read-only. Read the current state and latest journal without modifying
files, checking for updates, scheduling work, or running target checks. Report
stored verification as historical evidence, not a new verification.

For resume/heal:

1. Honor a stored pause, abort, or user stop before any recovery. Only an explicit
   resume authorizes resuming a paused mission. A diagnostic request never does.
2. Read the mission, state, journal, host status, and target baseline/revision.
   Establish whether the previous run is still live. Never take over on age alone.
3. Inspect pre-existing edits, partial results, and externally created artifacts.
   Preserve them. Verify which work already succeeded before retrying.
4. If ownership is uncertain or targets changed unexpectedly, report the conflict
   and hand off without clearing files or marking the mission complete.
5. Continue from the last checked checkpoint. Revalidate any evidence affected by
   intervening changes. Do not replay a write solely because its response was lost.

`heal` requests diagnosis and safe recovery, not permission to discard work.
No automatic `git restore .`, `git clean -fd`, reset, stash, or document revision
replacement. Use a confirmed owned patch/revision only when an actual rollback
is authorized. Retain failed working directories and notes for inspection.

## Legacy v1 compatibility

The read-only state checker recognizes a state with no schema_version as legacy.
Do not rewrite it for status. Before migration, save an exact backup to a unique
file next to the state. If backup/validation fails, leave the original untouched.
Never migrate all projects or an active other session automatically.

When an authorized resume needs new fields, preserve unknown legacy fields and
old history. Add schema_version 1, a mission_id, target identity, criterion IDs,
and actual verification records. A legacy `done` or terminal marker alone is
not verified completion: inspect the old evidence, or leave criteria unresolved.
Do not fabricate checks to make a state validate. Save atomically and validate
before proceeding. Malformed or unknown future schemas require diagnosis rather
than reset-to-default. Backup paths belong in the handoff.

Read Q1–Q10 as old mission input. In particular:

- Q8 `frequency: every-cycle` / `threshold-only` becomes advisory-only, never a
  claim to execute compaction. Native host compaction owns conversation history.
- Q5 L1/L2/L3/L4 are historical scope hints, not new grants of access. L3 does not
  override the current user's PR approval rule. A diff cap limits scope only.
- Continuous missions need an explicit ongoing objective; no candidate is not
  proof of completion. Bounded counts still require acceptance checks.
- A stored next_wakeup_at is historical until an actual live schedule is checked.

Retain the existing journal_root and milestone directory. Milestones are optional
records of verified outcomes, including research/document completion. Never
rewrite old milestones or reconstruct deleted ones from an unverified marker.
