# Host capabilities

Check the tools actually exposed in this session, not just installed binaries.
For each needed capability report supported, unavailable, or unknown. Reading a
CLI schema proves an API exists, not that this session may call it. Do not change
host settings, start a daemon, or create test schedules as capability detection.

| Need | Codex | Claude Code | Portable fallback |
|---|---|---|---|
| Explicit skill invocation | `$autopilot` | `/autopilot` | Host's skill selector |
| Continue toward a goal | Native `/goal` or exposed goal controls, when available | Native `/goal`, when available | One checkpoint and manual resume |
| Periodic work | Host's actual scheduled tasks, if exposed/configured | `/loop` or configured cloud/Desktop task | Report scheduling unavailable |
| Conversation compaction | Host automatic compaction; app-server has a separate integration API | Host context management | Save a handoff; do not fake compaction |
| Unattended structured job | `codex exec --json --output-schema` / SDK | Host-supported noninteractive interface | Manual invocation |

For code, research, and documents alike, the host owns turn lifecycle, permissions,
and scheduling. The skill owns the mission and evidence. Do not replace the host
with an infinite shell loop, a Stop hook, or a custom MCP server by default.

A goal tool requires the user's actual request to enter goal mode. Goal execution
is not timed scheduling and does not imply operation while a computer is asleep.
Keep the host goal status authoritative; store its identifier and last observation
only if exposed. Do not mark a goal complete just because one checkpoint passed.

A scheduled invocation should call the authorized mission in `run-once` mode;
never nest a second scheduler. Confirm creation by returned schedule ID and next
run; record cancellation only after confirmation. A sub-hour interval cannot be
silently promoted to a different cadence or cloud environment. Check access to
skills, local files, and durable state in that environment before enabling it.
Local desktop tasks need the machine/app running; web/cloud tasks do not inherit
a local folder, personal skill, or journal automatically.

Claude's `/loop` does not invoke skills marked disable-model-invocation: true.
Do not copy invocation-policy flags between hosts or assume scheduled skill
activation. Test the actual entrypoint. Keep normal discovery enabled unless the
user asks for explicit-only invocation; describing the repo must not start a run.

In Conductor, reuse its existing workspace and branch. Do not assume that the
Codex app's goal/scheduler UI or app-server APIs control the Conductor session.
Respect the host's rules for creating workspaces and naming branches.

MCP is optional: use available trusted tools for the mission's sources/actions.
Declare an MCP dependency only if the workflow really requires that server.
Tool annotations are hints, not enforcement. MCP Skills distribution and Tasks
handles require support on both sides; neither is a universal scheduler.

Current reference points (verify when integrating, not on every checkpoint):
- https://learn.chatgpt.com/docs/long-running-work
- https://learn.chatgpt.com/docs/automations
- https://learn.chatgpt.com/docs/non-interactive-mode
- https://code.claude.com/docs/en/goal
- https://code.claude.com/docs/en/scheduled-tasks
