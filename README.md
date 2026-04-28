# autopilot-skills

Universal self-driving mission runner for AI coding agents.

Once you start `/autopilot`, it runs an endless **discover → analyze → plan → execute → verify → learn** cycle on your mission until you tell it to stop. Domain-agnostic — code self-improvement, doc grooming, ops sweeps, anything you can describe in one line.

Works on Claude Code, Codex CLI, Cursor, Gemini CLI, and 50+ other AI coding agents (via the [`skills`](https://github.com/vercel-labs/skills) ecosystem).

## Install

```bash
npx skills add PresentJay/autopilot-skills
```

That's it. The CLI auto-detects your AI harness and drops `SKILL.md` into the correct skills directory (`~/.claude/skills/autopilot/`, `~/.codex/skills/autopilot/`, etc.). No global install needed.

> Don't have `skills`? `npx` fetches it from npm on demand — just need Node 18+.

### Manual install (no npx)

If you prefer not to use the `skills` CLI:

```bash
git clone https://github.com/PresentJay/autopilot-skills
mkdir -p ~/.claude/skills/autopilot
cp -r autopilot-skills/skills/autopilot/* ~/.claude/skills/autopilot/
```

Replace `~/.claude/skills/` with your harness's skills directory.

## Use

```
/autopilot
```

First call: 8-question boot interview captures your mission, allow/forbidden paths, risk tier, cadence, auto-compact threshold, escalation rules.

Subsequent calls: one cycle per invocation. Idle/`continuous` mode auto-schedules the next cycle via `ScheduleWakeup`.

### One-line mission via args

Skip the interview for known answers:

```
/autopilot mission="lint cleanup" risk=L2 cadence=15m
```

Recognized keys: `mission`, `mode`, `allow`, `forbidden`, `risk`, `cadence`, `escalate_idle`, `compact`. Anything not provided falls back to defaults.

## Safety

The skill enforces these at **every** phase, not just at execute time:

- **Forbidden zones (Q4)** — `main`/`master`, secrets, infra, destructive flags. Non-negotiable.
- **Pre-execute deny-list** — `git push --force`, `git reset --hard`, `rm -rf <outside allow paths>`, DB DDL, external API writes. Blocked unless mission opts in.
- **Diff cap by risk tier** — L1 read-only, L2 ≤300 lines, L3 ≤500 lines, L4 user-approved.
- **NOT-OK pattern auto-grow** — failed proposals add anti-patterns; future cycles avoid the same trap.

## Storage

```
<repo>/
├── .autopilot.log/                 # mission, journal, proposals, state — mutable path
└── .autopilot.milestones/          # PR-merged / bounded-complete / first-zero-defect / novel-NOT-OK — fixed path
```

Add to `.gitignore` if you don't want runtime artifacts in git, or commit them for review-friendly history.

## Cadence

| Choice | Effective delay | Notes |
|---|---|---|
| `immediate` | 60 s | Most aggressive; high token cost |
| `2m` | 120 s | Inside Anthropic prompt-cache window |
| `5m` | 300 s | Just past cache window |
| `15m` | 900 s | **default** |
| `30m` | 1800 s | Relaxed |
| `1h+` | 3600 s+ | Auto-promotes to a `/schedule` cron (cloud) |
| `manual` | — | No auto wake; re-invoke yourself |

3 consecutive idle cycles bump the tier up automatically.

## Stop

- Type any new message — interrupts the next scheduled wake.
- "stop autopilot" / "멈춰" / "pause" — sets mission `Mode: paused`.
- Delete `.autopilot.log/mission.md` — cold start on next call.

## What's inside

- `skills/autopilot/SKILL.md` — the skill itself (orchestrator, safety policy, output protocol).
- `skills/autopilot/templates/` — `mission.md`, `state.json`, `journal-entry.md`, `proposal.md`, `milestone.md`.

## License

MIT — see [LICENSE](LICENSE).

## Origin

Built after observing that ad-hoc loops (e.g. ralph-loop) had two problems: bootstrap parsing bugs that locked them into infinite mode, and single-domain hard-coding. Autopilot is the meta-loop with proper interrupt/resume, mission-bound governance, and self-pacing via the `ScheduleWakeup` primitive — no plugin dependency required.
