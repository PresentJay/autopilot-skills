---
title: Cadence menu
---

# Cadence menu

| Choice | Effective delay | When? |
|---|---|---|
| `immediate` | 60 s (ScheduleWakeup floor) | Stress-testing the loop, urgent backlog burndown, or a session you'll be watching |
| `2m` | 120 s | Active dev session — fast feedback, stays inside Anthropic's prompt-cache window |
| `5m` | 300 s | Mild iteration; cheaper than 2m, slightly past the cache window |
| `15m` | 900 s | **Default.** Long-running missions where you check in every so often |
| `30m` | 1800 s | Idle-heavy missions; space cycles out so empty ones cost less |
| `1h+` | 3600 s+ | Survives session close. Auto-promotes to a `/schedule` cron (cloud) |
| `manual` | — | Demos, debugging, or any case where you want to drive each cycle yourself |

Idle auto-throttle: 3 consecutive empty cycles bump cadence one tier.
