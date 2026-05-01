---
title: Mission schema
---

# Mission schema

Each section is a question answered during the boot interview. The full template lives at [`skills/autopilot/templates/mission.md`](https://github.com/PresentJay/autopilot-skills/blob/main/skills/autopilot/templates/mission.md).

## Q1. Mission

One line. The single objective the loop pursues.

## Q2. Operating mode

- `continuous` — until told to stop.
  - When? Open-ended quality work (lint cleanup, dead-code grooming, doc polish) where you can't predict when it'll be done.
- `bounded:N` — at most N cycles.
  - When? You have a finite checklist (e.g. 5 specific tasks). Loop terminates after N successful or escalated cycles.
- `monitor` — react to external events only.
  - When? You want the loop to wake on signals (CI completion, new PR, log line) rather than on a timer.

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

When the loop should stop and ping you instead of pushing through.

- **3 consecutive failures** — same candidate failed 3 cycles → add to NOT-OK and move on. If every candidate fails, escalate.
- **Diff cap exceeded** — proposed change is larger than the tier allows → split into sub-tasks first, escalate if still over.
- **Irreversible action** — DB DDL, force-push, external API write — always escalate before running.
- **No candidate found**:
  - `end` *(default)* — treat as mission complete, no `ScheduleWakeup`.
  - `ask` — request more discovery tools from you.
- **≥5 candidates outside allow paths** — propose extending mission scope.

## Q8. Auto-compaction

Long missions hit prompt-too-long if context never gets trimmed. Compaction calls `/compact` to reset older history while keeping recent state.

- **threshold** — pause-and-compact when token usage crosses this percent.
  - When? Lower (60-70) for token-heavy work (large diffs, big files); higher (80-90) for normal docs/code cycles. Default **80**.
- **frequency**:
  - `every-cycle` *(default)* — light compact every cycle. Predictable cost, safest for long sessions.
  - `threshold-only` — compact only when the threshold is crossed. Saves tokens on short sessions.
  - `off` — no compaction. Use only for short bounded missions or when you handle context manually.

## Q9. Update policy

The skill checks GitHub releases for newer versions of `PresentJay/autopilot-skills`.

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — default `every-24h`
  - When? `every-24h` for daily-active repos; `every-boot` if you upgrade frequently and want zero lag; `weekly` for slower release cadences; `off` if you'll update manually.
- **on_update_available**:
  - `notify` — append a one-line notice to the cycle output. *When?* You read every cycle's output anyway.
  - `prompt` *(default)* — show notice and ask "update now?"; on confirm, run `npx skills update PresentJay/autopilot-skills --yes`. *When?* Watching occasionally and want explicit consent.
  - `silent-auto` — run the update without asking. *When?* Trusted setup, you don't review logs in detail.

The check fails open: if the GitHub API errors or times out (5s), the cycle continues without blocking.

## Q10. Resume policy

Controls how the skill recovers from interruptions (host sleep, session crash, missed `ScheduleWakeup`, mid-cycle abort).

- **stale_threshold**: `2x-cadence` *(default)* / `4x-cadence` / `8x-cadence` — how long after `next_wakeup_at` to consider the loop stalled.
  - When? `2x-cadence` for aggressive recovery (1 missed cycle = stalled). `4x-cadence` for stable infra with intermittent load. `8x-cadence` for long-cadence missions where overnight host sleep is normal.
- **on_resume**:
  - `auto-resume` *(default)* — silently detect stale state and run a fresh cycle. *When?* You trust the loop and don't want to break flow.
  - `prompt-confirm` — show diagnosis ("Missed N cycles. Resume?") and confirm before continuing. *When?* You want to know about every recovery.
  - `manual-only` — only resume on explicit `/autopilot resume` or `/autopilot heal`. *When?* Mission paused on purpose; you'll restart it yourself.

Phase 0.5 detects 5 patterns: crashed mid-cycle, missed wakeups, schedule lost, paused, escalated.

User signals: `/autopilot resume`, `/autopilot heal`, `/autopilot status`.
