---
layout: page
title: "Codex stopped before finishing: how to carry the task forward"
description: "Keep the goal, checked progress and next action when AI work is interrupted. Install Autopilot, request a durable record and explicitly resume it."
lang: en
translation_key: when-agent-stops
---

# Codex stopped before finishing. What should I keep?

If you keep telling an AI agent “continue” or explaining the same task in a new
session, keep a reusable brief and handoff with the work. Autopilot is an open
source skill for Codex and Claude Code that keeps the outcome, allowed scope,
completion checks and next action together when a task needs persistent records.

It cannot prevent a native goal from stopping, fix an app crash or keep a closed
app running. If a goal is cancelled unexpectedly, inspect the host's goal status
and error first. A saved mission helps describe what remains; it does not restart
the host. [Read the public evidence and limits](evidence.html).

## Try it on one real task

Install the skill:

```sh
npx skills add PresentJay/autopilot-skills --skill autopilot
```

In Codex, give it a bounded task and explicitly request records for another session:

```text
$autopilot Fix the import failure in this project. Reproduce the failure,
preserve my edits and the public API, and verify with the existing integration
tests. Keep the mission, state and verification journal in .autopilot.log/ so
another session can continue. Record the next action and any remaining failures.
Use available native goal mode until the checks pass or a blocker or host limit
is reached; reuse an active goal. Do not commit, publish or merge.
```

In Claude Code, replace `$autopilot` with `/autopilot`. Choose files and checks
that exist in your project. Native goal mode must be available in your host;
the skill does not provide its own background runner.

## Resume without repeating the whole brief

Open a session that can access the same project, installed skill and records.
Then explicitly authorize resuming the recorded mission:

```text
$autopilot resume the mission in .autopilot.log/. Resume this paused or
interrupted mission after confirming no previous run is still writing.
Read its mission, state and journal. Inspect my changes and partial results;
recheck evidence affected by changed files. Preserve my edits and the original
scope. Use available native goal mode until the recorded criteria pass or a
blocker or host limit is reached; reuse an active goal. Do not commit, publish
or merge.
```

These are usage examples, not a measured recovery transcript. Read-only
`$autopilot status` inspects the stored mission without resuming it. Name the
record directory if you have more than one mission. If another run is still
writing, do not start a competing writer. [See an actual public record](handoff-example.html).

## Autopilot, native goals or unlazy?

| Your need | Where to start |
| --- | --- |
| Continue a clear task within the host's execution limits | Native goal mode |
| Carry the brief, checked progress and next action into a later session | Autopilot with an explicit durable-record request |
| Define acceptance gates and verify substantial work before calling it done | [unlazy](https://github.com/Leonxlnx/unlazy) |

These workflows overlap. Autopilot verifies outcomes too; unlazy also addresses
incomplete work. The distinction is their emphasis, not an exclusive capability.
Installing Autopilot does not install unlazy. [Compare native goals](comparison.html).

## What would show that it helps?

Try one task with your existing goal instructions and one with a mission handoff.
Record how often you repeat instructions, which requirements get missed and the
effort needed to resume. Keep failed attempts. Autopilot has not yet demonstrated
a general reduction in supervision, time or cost. Share the input, expected
result and actual artifact in the repository's
[showcase form](https://github.com/PresentJay/autopilot-skills/issues/new?template=showcase.yml)
if you want to contribute a case.
