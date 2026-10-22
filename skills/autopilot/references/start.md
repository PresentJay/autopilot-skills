# Start or run one checkpoint

Read applicable project instructions and any existing mission before writing.
`quick`, `--quick`, and `mission="..."` are input hints, not authorization to
replace an existing mission. Existing Q1–Q10 missions remain readable.

Fill four decisions from the user's request and established context:

1. Outcome and deliverables.
2. Allowed targets/actions and any forbidden scope.
3. Acceptance criteria and how each can be checked.
4. Stop conditions and whether this is finite work or ongoing monitoring.

Ask only about consequential gaps. Do not repeat a ten-question interview or
require a second generic confirmation after the user has already authorized
that exact work. If the user asks only for a plan, produce the plan.
Do not strengthen acceptance beyond the request. If the user explicitly asks
for a report of known gaps, access to every missing source is not automatically
a new prerequisite for completing that report. Separate deliverable coverage
from unresolved facts.

Use the mission template. Record criterion IDs so verification and state refer
to the same outcomes. Default to finite goal completion. Continue through useful
checkpoints within the current execution until the mission is verified, blocked,
paused, or reaches a user/host limit; a checkpoint alone is not a reason to stop.
A cycle count is a limit, not proof that the outcome was achieved.
Budget/time limits are optional user choices; do not
invent a token budget. `run-once` performs at most one checkpoint and does not
create or renew schedules. An authorized native goal may continue checkpoints.

Inspect actual host capabilities as described in hosts.md before promising
continuation. Do not create a goal merely because the skill was loaded.
A request to explicitly start goal mode may use an exposed goal tool; otherwise
work within the current turn or show the host's goal invocation to the user.

For code, use an existing isolated workspace/branch when provided. Honor branch
naming restrictions. For documents, identify the file or document ID and revision;
for research, identify questions, sources, and date scope. Git, npm, and PRs are
not universal prerequisites. Discover the project's real commands rather than
installing arbitrary linters with npx.

Before modifying a target, record its baseline and existing edits/revision.
Store runtime records inside the authorized journal directory, even for a
read-only target mission. If no writable journal destination is authorized,
keep a conversational handoff and report that durable recovery is unavailable.
Do not claim to enforce target access through a Markdown allow list.
