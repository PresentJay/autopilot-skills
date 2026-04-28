---
title: Getting started
---

# Getting started

## Install

```bash
npx skills add PresentJay/autopilot-skills
```

Pick the harness when prompted, or install everywhere with `--all -g`.

## Start a mission

In your harness (Claude Code, Codex, Cursor, etc.):

```
/autopilot
```

First call: an 8-question interview. Skip questions you've already decided by passing args:

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

## Stop

- "stop autopilot" / "멈춰" / "pause" — sets `mission.md` Mode to `paused`.
- Delete `.autopilot.log/mission.md` — cold start on next call.
