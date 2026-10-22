---
layout: page
title: "Mission and evidence"
lang: en
---

V2 records outcome, scope and authorization, acceptance criterion IDs, execution/stopping conditions, and storage in `mission.md`. Use the packaged template rather than a fixed ten-question interview.

`state.json` uses `schema_version: 1` and records mission/run IDs, target, criterion IDs, verification records, status, and the last result. Evidence identifies the method and target version. The checker validates record structure, not truth or freshness.

Keep `.autopilot.log/` or the existing custom journal path. V1 Q1–Q10 missions remain readable. Status is read-only; before an authorized migration, make an exact backup and preserve unknown fields and history.

Read the current templates and conditional instructions in the packaged skill. No existing project state is migrated during installation.
