---
title: Safety policy
---

# Safety policy

Enforced at every phase, not just at execute time.

## Forbidden zones

Q4 of the mission. Match → abort + journal entry. Even risk tier L4 respects Q4.

## Pre-execute deny-list

- `git push --force`
- `git reset --hard`
- `rm -rf <outside allow paths>`
- DB DDL
- external API writes

Allowed only if `mission.md` explicitly opts in.

## NOT-OK pattern auto-grow

Failed proposals add patterns to `mission.md` `NOT-OK patterns`. Future cycles avoid the same trap.

## Idle limit

3 consecutive empty cycles → cadence +1 tier. 10 cumulative idle → propose termination.

## Token budget

70% per-cycle ceiling triggers split-cycle save instead of fail.
