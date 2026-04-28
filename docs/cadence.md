---
title: Cadence menu
---

# Cadence menu

| Choice | Effective delay | Notes |
|---|---|---|
| `immediate` | 60 s (ScheduleWakeup floor) | Most aggressive; high token cost |
| `2m` | 120 s | Inside Anthropic prompt-cache window |
| `5m` | 300 s | Just past cache window |
| `15m` | 900 s | **default** — balanced |
| `30m` | 1800 s | Relaxed |
| `1h+` | 3600 s+ | Auto-promotes to a `/schedule` cron (cloud) |
| `manual` | — | No auto wake; re-invoke yourself |

Idle auto-throttle: 3 consecutive empty cycles bump cadence one tier.
