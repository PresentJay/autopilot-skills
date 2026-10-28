---
layout: page
title: "Native goals and Autopilot"
lang: en
---

A task that can finish in the current invocation reads only the skill entrypoint and verifies the requested output, without creating state/journal files or hashing the whole workspace. Persistent records are for cross-session handoffs, recurring monitoring, explicit record requests, or an existing mission. Existing pauses and user edits are always preserved.

For a clear one-off task, native goals may be enough. Autopilot adds a reusable mission brief and working record. Faster execution and better outcomes are not established; read the [pilot evidence](evidence.html).

An ordinary mission continues through useful checkpoints until verified completion, a blocker, a pause, or a user/host limit. A checkpoint alone is not a reason to stop. `run-once` is explicitly limited to one checkpoint. To continue across turns, explicitly request native goal mode when the host exposes it. Scheduling is a separate host capability.
