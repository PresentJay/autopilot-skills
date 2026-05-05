---
layout: page
title: "Comparison — autopilot vs alternatives"
lang: en
---

# How autopilot fits next to other tools

You may already use a loop primitive (ralph-loop), a single-purpose skill template (impeccable), or a broader CLI swiss-army (gstack). This page is honest about what autopilot adds, what it overlaps with, and **when NOT to use it**.

## At a glance

| Tool | Primary purpose | Boots in | Domain | Auto-discovers work? | Self-heals? |
|---|---|---|---|---|---|
| **autopilot** | Self-driving missions across many domains | one slash command | any | ✅ via mission tools | ✅ Phase 0.5 |
| **ralph-loop** | Generic loop primitive (run prompt N times) | one slash command | any | ❌ user provides prompt each iter | ❌ |
| **impeccable** | Frontend design audit + fixes | one slash command | UI / design | ✅ within design domain | ❌ |
| **gstack** | CLI suite (browse, ship, qa, retro, ...) | install + N commands | dev workflow | partially per command | n/a |

## When to use which

- **You want a self-running loop on a domain you can describe in one line** → `autopilot`
- **You just want to repeat one prompt N times with no governance** → `ralph-loop`
- **You're polishing a frontend/landing/UX** → `impeccable` (or autopilot mission with `mission="design polish"`, but impeccable is purpose-built)
- **You need a kitchen-sink of dev shortcuts (browse, qa, ship, retro)** → `gstack`

The tools are **not mutually exclusive**. autopilot can drive impeccable cycles, gstack can run inside an autopilot mission, ralph-loop covers the bare-loop case autopilot is overkill for.

## What autopilot adds vs ralph-loop

- **Per-mission governance**: allow paths, forbidden zones, risk tier, diff caps — enforced every phase
- **Self-pacing**: chooses the next wakeup based on cadence + idle backoff; no need for `--max-iterations`
- **Self-healing**: detects mid-cycle crashes, missed wakeups, schedule-lost states (Phase 0.5)
- **Milestone trail**: auto-promotes important moments to an immutable directory
- **Update notifications**: 24h cached check against latest release with opt-in auto-update

ralph-loop is a primitive. autopilot is the shaped abstraction on top of that primitive that you'd otherwise hand-roll.

## What autopilot is NOT

- **Not a coding agent** — it orchestrates the agent you're already using (Claude Code, Codex, Cursor, Gemini). It does not bring its own model.
- **Not a CI replacement** — autopilot writes commits, not pipelines. CI still runs your tests.
- **Not opinionated about code style** — it reads `mission.md` only. Style is whatever your repo and the underlying agent already enforce.
- **Not a distributed orchestrator** — single repo, single mission per directory. For multi-repo fan-out use cron + `/schedule`.

## When NOT to use autopilot

- **One-off task** — overhead isn't worth it. Just ask the agent directly.
- **Hard real-time / production-critical writes** — autopilot is L2 by default (small PRs, never main). For prod ops use a purpose-built runbook.
- **Mission you can't describe in one sentence** — if you can't fill Q1, the mission isn't ready. Brainstorm first, autopilot second.
- **You don't trust the agent on the loop** — autopilot inherits the agent's judgment. If you're not ready to trust the agent on a 10-cycle run, start at L1 (read-only proposals).

## How to evaluate fit in 60 seconds

1. Can you write the mission in one sentence?
2. Are the allow paths a glob you'd be comfortable with the agent modifying without per-PR human approval?
3. Is the verify command something CI already runs (build / test / lint)?

If yes to all three → autopilot is the shape that fits.
