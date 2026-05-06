# autopilot-skills

[![Latest release](https://img.shields.io/github/v/release/PresentJay/autopilot-skills?label=release&color=4c1)](https://github.com/PresentJay/autopilot-skills/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-4c1)](LICENSE)
[![AI harnesses: 50+](https://img.shields.io/badge/harnesses-50%2B-4c1)](https://github.com/vercel-labs/skills#supported-harnesses)
[![Docs](https://img.shields.io/badge/docs-presentjay.github.io-4c1)](https://presentjay.github.io/autopilot-skills)
[![Languages: en · ko · zh · ja](https://img.shields.io/badge/docs-en%20·%20ko%20·%20zh%20·%20ja-4c1)](https://presentjay.github.io/autopilot-skills)

Universal self-driving mission runner for AI coding agents.

> 📘 Docs and quickstart: [presentjay.github.io/autopilot-skills](https://presentjay.github.io/autopilot-skills)

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

## Compare with peers

Already use `ralph-loop`, `impeccable`, or `gstack`? Read [the comparison page](https://presentjay.github.io/autopilot-skills/comparison.html) — what autopilot adds, what overlaps, **when not to use it**.

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

## Share your mission

Ran autopilot on something interesting? [Open a Showcase issue](https://github.com/PresentJay/autopilot-skills/issues/new?template=showcase.yml) — mission, cycles, outcome. Public learning is how the loop tunes itself across repos and domains.

## Built with itself

This repo's own grooming runs through autopilot. Concrete trail:

- The 4-language Pages site (en / ko / zh / ja) was translated, polished, and laid out across multiple autopilot cycles — landing, mission schema, safety, cadence, milestones, comparison.
- The mission-schema option pickers in 4 langs (Q2 + Q5–Q10) were generated by 7 autopilot cycles in PR [#11](https://github.com/PresentJay/autopilot-skills/pull/11).
- README badges, use-cases section, comparison page, and OG/Twitter card polish were each one autopilot cycle commit on the adoption mission.
- The `/autopilot version` signal in v1.2.0 is the kind of small surface autopilot is designed to ship: tight scope, single PR, full verification.

If you want to verify, the mission-bound journals live under `.autopilot.log/journal/` and the immutable milestone trail in `.autopilot.milestones/`.

## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=PresentJay/autopilot-skills&type=Date)](https://star-history.com/#PresentJay/autopilot-skills&Date)
