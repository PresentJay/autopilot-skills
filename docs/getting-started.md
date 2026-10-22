---
layout: page
title: "Get started"
lang: en
---

V2 is a preview under review. The default branch still contains v1.3. Install the preview explicitly:

```sh
git clone --branch improve/codex-missions-v2 https://github.com/PresentJay/autopilot-skills.git autopilot-skills-v2
npx skills add ./autopilot-skills-v2 --skill autopilot
```

In Codex invoke `$autopilot`; in Claude Code invoke `/autopilot`. Describe the outcome, allowed scope, completion checks, and stopping conditions. Code, research, and documents are equally supported; Git is not required.

An ordinary mission continues through useful checkpoints until verified completion, a blocker, a pause, or a user/host limit. A checkpoint alone is not a reason to stop. `run-once` is explicitly limited to one checkpoint. To continue across turns, explicitly request native goal mode when the host exposes it. Scheduling is a separate host capability.

For a clear one-off task, native goals may be enough. Autopilot adds a reusable mission brief and working record. Faster execution and better outcomes are not established; read the [pilot evidence](evidence.html).
