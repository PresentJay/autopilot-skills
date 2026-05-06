# Changelog

All notable changes to autopilot-skills are documented here.

Format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] — 2026-05-05

### Changed
- **Q8 reframed as "compaction strategy" (truth-in-spec).** Earlier versions promised the skill would call built-in `/compact`, but the agent has no tool to invoke a slash command. Q8 now offers `auto-suggest` (default; surfaces a `📦 /compact suggested` advisory once threshold is crossed), `cron-promote` (recommend `/schedule` cron for genuinely long missions, where each scheduled run is a fresh session), and `off`. No silent failure when prompt-too-long is approaching — the user is told.
- **Phase 8 NEXT no longer pretends to compact.** Step 2 now appends the advisory to cycle output and writes `kind: "advisory"` (not `"compaction"`) to `state.json.compaction_history`.
- **Phase 0.5 boundary clarified.** Phase 0.5 (resume + update check) is meaningful only at invocation boundaries (fresh `/autopilot` call or `ScheduleWakeup` re-fire). Multiple cycles in a single conversation turn — without a wakeup boundary between them — is batch execution, not self-driving. Documented explicitly.

### Added
- **Quick boot (`--quick` / `/autopilot quick`).** All Q's default-pre-filled with safe values (continuous, defaults, L2, 15m, etc.); Q1 still required. Single summary, single confirm — total one-turn boot. Cuts the 10-question interview to one decision when the user already knows what they want.

### Notes
- Long-running self-drive in a single session is structurally bounded by harness limits (no programmatic compaction). Use Q6=`1h+` to promote to `/schedule` cron — each cron firing is a fresh session, no compaction needed.
- `state.json.compaction_history` schema is non-breaking — old entries with `kind: "every-cycle"` are read as advisories.

## [1.2.0] — 2026-05-02

### Added
- **`/autopilot version` user signal** (aliases: `--version`, `-v`) — prints installed version from frontmatter, latest available from GitHub releases (uses Q9 24h cache, falls back to one live 5s call), source URL, and an update hint. Diagnostic-only: does not run a cycle, schedule a wakeup, or modify files.
- **Version line in `/autopilot status`** — first line of status output now shows `autopilot v<installed>` for at-a-glance version visibility.

### Changed
- SKILL.md frontmatter `version`: 1.1.0 → 1.2.0.

### Notes
- The version check reuses the same `state.json.last_update_check_at` / `available_version` cache as Q9, so calling `/autopilot version` does not trigger an extra API request when the cache is fresh.
- Fail-open: if the live GitHub API call errors or times out, output prints `latest: unknown (offline)` and skips the update hint instead of blocking.

## [1.1.0] — 2026-04-28

### Added
- **Q9. Update policy** — every-boot / every-24h / weekly / off check against GitHub releases. On detection: notify (passive) / prompt (default; runs `npx skills update` on confirm) / silent-auto. 24h cache via `state.json.last_update_check_at`.
- **Q10. Resume policy** — controls self-healing after interruption. `auto-resume` (default), `prompt-confirm`, or `manual-only`. Stale threshold tunable (2x / 4x / 8x cadence).
- **Phase 0.5 — Resume + update check** — runs after boot check and before DISCOVER. Detects 5 failure modes (crashed mid-cycle, missed wakeups, schedule lost, paused, escalated) and recovers per Q10.
- **User signals** — `/autopilot resume`, `/autopilot heal`, `/autopilot status` for explicit recovery / diagnosis.
- **Heartbeat fields** in `state.json`: `last_run_at`, `next_wakeup_at`, `cycle_started_at`. Enables interruption detection.
- **`interruption_history`** in `state.json` — audit trail of every recovery event.

### Changed
- SKILL.md frontmatter `version`: 1.0.0 → 1.1.0.
- Output protocol gains two new terminal tokens: `AUTOPILOT_RESUMED`, `AUTOPILOT_UPDATED`.
- Mission interview is 10 questions (was 8). Q9 and Q10 default to safe values (`every-24h` + `prompt`, `2x-cadence` + `auto-resume`).

### Notes
- The update check fails open: if GitHub API errors or times out (5s cap), the cycle continues without blocking.
- The resume check writes to `state.json.interruption_history` for post-mortem visibility.

## [0.1.0] — 2026-04-28

### Added
- Initial release of the `autopilot` skill.
- 8-question boot interview (mission, mode, allow paths, forbidden zones, risk tier L1-L4, cadence, escalation, auto-compaction).
- 8-phase cycle: DISCOVER → TRIAGE → ANALYZE → PLAN → EXECUTE (safe) → VERIFY → LEARN → NEXT.
- Safety policy enforced every phase: forbidden zones, pre-execute deny-list, NOT-OK pattern auto-grow.
- Storage: `.autopilot.log/` (mutable) + `.autopilot.milestones/` (fixed).
- Milestone auto-promotion on PR-merged / bounded-complete / first-zero-defect / novel-NOT-OK.
- Cadence menu: immediate / 2m / 5m / 15m (default) / 30m / 1h+ → /schedule cron / manual.
- Templates: `mission.md`, `state.json`, `journal-entry.md`, `proposal.md`, `milestone.md`.

[Unreleased]: https://github.com/PresentJay/autopilot-skills/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/PresentJay/autopilot-skills/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/PresentJay/autopilot-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/PresentJay/autopilot-skills/compare/v0.1.0...v1.1.0
[0.1.0]: https://github.com/PresentJay/autopilot-skills/releases/tag/v0.1.0
