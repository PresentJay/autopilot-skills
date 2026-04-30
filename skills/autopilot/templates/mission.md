# Autopilot Mission

**Created**: <!-- ISO timestamp, set on first save -->
**Mode**: active <!-- active | active-manual | paused | done | aborted -->
**Cycle count**: 0

## Q1. Mission
<!-- one line — the loop's single objective -->

## Q2. Operating mode
<!-- continuous | bounded:N | monitor:event-list -->

## Q3. Allow paths
<!-- glob patterns the loop may modify; everything else is read-only -->
- packages/
- apps/
- docs/
- settings/
- scripts/
- README.md
- CONTRIBUTING.md

## Q4. Forbidden (absolute)
- main, master, release/* branches — never push directly
- .env, *credentials*, secrets/*, *.pem, *.key
- infra/, terraform/, .github/workflows/
- --force, --no-verify, git reset --hard, rm -rf outside allow paths
- external API writes (gh CLI / npm registry only)

## Q5. Risk tier
<!-- L1 | L2 | L3 | L4 -->

### Diff cap (per tier)
- L1: 0 lines (read-only)
- L2: ≤ 300 lines, ≤ 10 files
- L3: ≤ 500 lines, ≤ 15 files
- L4: user-approved limit

## Q6. Cadence
<!-- immediate (60s floor) | 2m | 5m | 15m | 30m | 1h | manual -->
<!-- default: 15m -->

## Q7. Escalation triggers
- consecutive_failures: 3
- on_idle_no_candidate: end <!-- end | ask -->
- diff_cap_exceeded: split_or_escalate
- irreversible_action: always_escalate
- mission_external_signals: extend_proposal

## Q8. Auto-compaction
- threshold: 80 <!-- 60 | 70 | 80 | 90 -->
- frequency: every-cycle <!-- every-cycle | threshold-only | off -->

## Q9. Update policy
- check: every-24h <!-- every-boot | every-24h | weekly | off -->
- on_update_available: prompt <!-- notify | prompt | silent-auto -->
- repo: PresentJay/autopilot-skills

## Q10. Resume policy
- stale_threshold: 2x-cadence <!-- 2x-cadence | 4x-cadence | 8x-cadence -->
- on_resume: auto-resume <!-- auto-resume | prompt-confirm | manual-only -->

## Storage
- journal_root: .autopilot.log/         <!-- mutable; you may change to e.g. docs/improvement/ or .claude/autopilot/ -->
- milestones_root: .autopilot.milestones/  <!-- FIXED — do not edit; the skill ignores changes -->

## Inference provenance
<!-- how each Q got its value: args | default | user -->
- Q1: default
- Q2: default
- Q3: default
- Q4: default
- Q5: default
- Q6: default
- Q7: default
- Q8: default
- Q9: default
- Q10: default

## Tools (auto-discover commands — add/remove for your domain)
- `npm run lint`
- `npx ts-prune`
- `npx knip --no-progress`
- `npx tsc --noEmit`
- `git log --oneline -20 origin/main..HEAD`
- `grep -rn "TODO\|FIXME"`

## Verify commands
- `npm run build`
- `npm test`
- `npm run lint`

## NOT-OK patterns (auto-grow)
<!-- starts empty; the LEARN phase appends patterns from failed cycles -->

## Branch / PR convention
- Working branch: `autopilot/<slug>`
- Commit format: `auto(<id>): <title>`
- PR base: <user-defined>
- PR body link: `.autopilot.log/journal/`
