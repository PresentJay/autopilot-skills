---
title: Milestones
---

# Milestones

When a cycle hits any of the four triggers, the journal entry is **also** written to `.autopilot.milestones/<date>-<slug>.md`. That folder is fixed; `mission.md` cannot relocate it.

## Triggers

1. **PR merged** — a tracked PR transitioned to `MERGED`.
2. **Bounded mission completion** — Q2=bounded N reached, all green.
3. **First zero-defect achievement** — first time a tracked defect category (lint, test, type, coverage) hits zero. Tracked via `state.json` `defect_baselines.<category>.ever_zero`.
4. **Novel NOT-OK pattern** — a pattern added to `mission.md` for the first time.

## Why fixed

Milestones are a curated trail of what mattered. Letting the path drift in `mission.md` would let users hide history; immutability protects the audit log.
