# Changelog

All notable changes to autopilot-skills are documented here.

Format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/PresentJay/autopilot-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/PresentJay/autopilot-skills/releases/tag/v0.1.0
