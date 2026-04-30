---
title: Mission schema
---

# Mission schema

Each section is a question answered during the boot interview. The full template lives at [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md).

## Q1. Mission

One line. The single objective the loop pursues.

## Q2. Operating mode

- `continuous` — until told to stop
- `bounded:N` — at most N cycles
- `monitor` — react to external events only

## Q3. Allow paths

Glob patterns the loop may modify. Anything not listed is read-only.

## Q4. Forbidden zones (absolute)

Branches, files, flags that are never touched. Default block-list:

- `main`, `master`, `release/*`
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/`
- `--force`, `--no-verify`, `git reset --hard`, `rm -rf` outside allow paths
- external API writes other than `gh` and `npm`

## Q5. Risk tier

- **L1** — discover + propose only
  - When? Audit-only setups, regulated environments, first-time mission for an unfamiliar repo.
- **L2** — small PRs (≤300 lines, ≤10 files) — *default*
  - When? Most repos. Reviewable diffs, CI gating, no auto-merge.
- **L3** — merge after green
  - When? Trusted infra, strong CI, repo where bot PRs can self-merge.
- **L4** — free mode (forbidden zones still absolute)
  - When? Large refactors planned with the user, multi-PR experiments. Q4 still blocks destructive ops.

## Q6. Cadence

See [Cadence menu](cadence.html).

## Q7. Escalation triggers

Default thresholds: 3 consecutive failures, diff cap exceeded, irreversible action, no-candidate behavior (`end` or `ask`).

## Q8. Auto-compaction

Threshold (60/70/80/90, default 80) and frequency (`every-cycle`, `threshold-only`, `off`).

## Q9. Update policy

The skill checks GitHub releases for newer versions of `PresentJay/autopilot-skills`.

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — default `every-24h`
- **on_update_available**:
  - `notify` — append a one-line notice to the cycle output
  - `prompt` *(default)* — show notice and ask "update now?"; on confirm, run `npx skills update PresentJay/autopilot-skills --yes`
  - `silent-auto` — run the update without asking

The check fails open: if the GitHub API errors or times out (5s), the cycle continues without blocking.

## Q10. Resume policy

Controls how the skill recovers from interruptions (host sleep, session crash, missed `ScheduleWakeup`, mid-cycle abort).

- **stale_threshold**: `2x-cadence` *(default)* / `4x-cadence` / `8x-cadence` — how long after `next_wakeup_at` to consider the loop stalled
- **on_resume**:
  - `auto-resume` *(default)* — silently detect stale state and run a fresh cycle
  - `prompt-confirm` — show diagnosis ("Missed N cycles. Resume?") and confirm before continuing
  - `manual-only` — only resume on explicit `/autopilot resume` or `/autopilot heal`

Phase 0.5 detects 5 patterns: crashed mid-cycle, missed wakeups, schedule lost, paused, escalated.

User signals: `/autopilot resume`, `/autopilot heal`, `/autopilot status`.
