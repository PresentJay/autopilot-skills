---
name: autopilot
description: Self-driving mission runner — once started, runs an endless discover→analyze→plan→execute→verify→learn cycle on a user-defined mission until told to stop. Boot interview captures mission, allow/forbidden paths, risk tier, cadence, auto-compact threshold, escalation. Safety policy blocks forbidden zones at every phase, forces dry-run for risky ops, learns NOT-OK patterns from failures. Universal across AI coding agents (Claude Code, Codex, Cursor, Gemini, ...). Triggers - "autopilot", "self-drive", "자율주행", "auto drive", "autonomous mode", "run cycle".
version: 1.0.0
---

# Autopilot — Self-driving mission runner

You receive a mission from the user and run an autonomous loop until they tell you to stop. The domain is whatever the user defines in the mission file — code self-improvement, doc grooming, research synthesis, ops sweeps, anything that benefits from a tight discover→execute→learn cadence.

This skill replaces ad-hoc loops (ralph-loop, improve-airops) with a domain-agnostic orchestrator: per-project mission, mission-bound governance, idle-aware self-pacing via `ScheduleWakeup`, immutable milestone trail.

## Boot check

First action on every invocation: locate the mission file.

- Default path: `<repo-root>/.autopilot.log/mission.md`.
- Fallbacks (legacy / migration): `<repo-root>/.claude/autopilot/mission.md`. If found, offer migration to default path on first run.
- Outside a git repo: `~/.claude/autopilot/<session-id>/mission.md`.

Decision:

- **Missing** → run "Boot interview" below.
- **Exists, user explicitly says "new mission" / "reset" / "redo"** → back up to `mission.md.bak.<timestamp>`, run interview again.
- **Exists, normal call** → enter "Operating cycle".

## Boot interview (mission contract)

Goal: capture mission, scope, risk, cadence, compaction, escalation in 8 short questions. Use `AskUserQuestion`, one question per turn, narrowing if the answer is unclear.

**Inference from invocation args**: if the user passes hints in the same turn (e.g. `/autopilot mission="lint cleanup" risk=L2 cadence=15m`), parse `key=value` pairs and pre-fill matching answers. Show the pre-filled draft once and offer:

1. Start as-is
2. Modify a few questions (cascade to those only)
3. Re-do from scratch

Do **not** scan prior conversation, git history, or other artifacts. Args only. Cold start when no args given.

### Q1. Mission (one line)

What single objective is this loop pursuing? Examples to seed:
- "self-improvement of this repo (lint, coverage, dead code)"
- "post-merge cleanup for PR #123"
- "documentation tone consistency"
- "dashboard / UI polish"

Free text accepted.

### Q2. Operating mode

- **continuous** — run until told to stop *(default)*
- **bounded:N** — at most N cycles or until completion signal
- **monitor** — react only to external events (CI, new PR, log line)

### Q3. Allow paths

Glob patterns the loop may modify. Sensible defaults (user can prune):

- `packages/`, `apps/`, `docs/`, `settings/`, `scripts/`
- `README.md`, `CONTRIBUTING.md`, `AGENTS.md`

Anything not listed is **read-only**.

### Q4. Forbidden zones (absolute)

Pre-checked defaults (uncheck only with reason):

- `main`, `master`, `release/*` branches — never push directly
- `.env`, `*credentials*`, `secrets/*`, `*.pem`, `*.key`
- `infra/`, `terraform/`, `.github/workflows/` (unless explicitly allowed)
- destructive flags: `--force`, `--no-verify`, `git reset --hard`, `rm -rf` outside allow paths
- external API writes (only `gh` CLI and `npm` registry permitted)

### Q5. Risk tier

- **L1** — discover + propose only (read-only, populates a backlog/issues, no code changes)
- **L2** — small PRs (≤300 lines, ≤10 files, build/test/lint must be green) — *default*
- **L3** — merge after green (PR + auto-merge on success; main direct push still forbidden)
- **L4** — free mode (large refactors, multi-PR, experiments; **Q4 forbidden still absolute**)

### Q6. Cadence

How long after a cycle ends before the next one fires?

| Choice | Seconds | Notes |
|---|---|---|
| `immediate` | 60 (floor of ScheduleWakeup) | Most aggressive; high token cost |
| `2m` | 120 | Inside Anthropic prompt-cache window — efficient |
| `5m` | 300 | Just past cache window |
| `15m` | 900 | **default** — balanced |
| `30m` | 1800 | Relaxed |
| `1h+` | 3600+ | Auto-promote to a cron via `/schedule` (cloud) |
| `manual` | — | No auto wake; user must re-invoke |

Idle auto-throttle: 3 consecutive empty cycles bump cadence one tier up.

### Q7. Escalation triggers

Pre-checked defaults:

- consecutive failures ≥ 3 → escalate
- single proposal exceeds tier diff cap → split or escalate
- no candidate found:
  - `end` — terminate as mission complete *(default)*
  - `ask` — ask user for additional discovery tools
- irreversible action (DB DDL, external API write, force push) → always escalate
- ≥5 candidates discovered outside allow paths → propose mission expansion

### Q8. Auto-compaction

Long-running loops bump into the prompt-too-long ceiling. Compaction trims the conversation while keeping recent context.

- **threshold**: 60 / 70 / 80 / 90 — pause-and-compact when token usage crosses this percent. Default **80**.
- **frequency**:
  - `every-cycle` *(default)* — call `/compact` at the end of every cycle regardless of threshold (light compact; baseline for long sessions)
  - `threshold-only` — compact only when threshold is crossed
  - `off` — no compaction (user accepts the risk)

### Wrap

Render the proposed `mission.md` to the user. Wait for one explicit confirm before starting the first cycle. Save mission.md, state.json, and create `.autopilot.log/` and `.autopilot.milestones/` directories.

---

## Operating cycle (one cycle per invocation)

8 phases. Bail-out rule: if the per-cycle token budget exceeds 70%, save partial state under "split-cycle" and resume at the failed phase next time.

### Phase 1 — DISCOVER

Pick **one** tool from `mission.md` Tools list, different from the previous cycle. Capture output to ≤100 lines.

Default tool catalogue (user adds/removes per domain):

- `npm run lint`
- `npx ts-prune` / `npx knip` / `npx tsc --noEmit`
- `npm test --coverage` (look for 0%-coverage modules)
- `git log --oneline -20 origin/<base>..HEAD` (follow-up signals)
- `grep -rn "TODO\|FIXME"` within allow paths

The previous tool comes from the latest `journal/` entry's `Phase 1 도구` field.

### Phase 2 — TRIAGE

Filter discovery output:

- Inside `Q3 allow paths`? → consider
- Hits `Q4 forbidden`? → reject
- Matches a `NOT-OK pattern`? → reject (anti-pattern learned in a prior cycle)
- Too broad? → narrow to one sub-task
- Priority: 5+ pattern or 1 decisive defect → P1; minor cleanup → P2

If no candidate survives:

- Q2=`continuous` + Q7 idle=`end` → terminate as mission-complete, no `ScheduleWakeup`.
- Q2=`continuous` + Q7 idle=`ask` → escalate to user.
- Q2=`bounded` → terminate.

### Phase 3 — ANALYZE (impact / EDA)

For the surviving candidate, write to `proposals/<id>.md`:

- impacted files / modules / users
- reversibility (code = reversible, config = mostly reversible, DB or external write = irreversible)
- conflicts with other proposals
- evidence (the discovery output excerpt)

### Phase 4 — PLAN

- minimal diff to satisfy acceptance
- verify strategy (concrete commands)
- rollback strategy (`git restore`, feature flag, config revert)
- if Q5 cap is exceeded, split and process the first sub-task only
- prefer dry-run when available

If Q5=L1 → write the proposal and skip Phase 5/6 → straight to LEARN.

### Phase 5 — EXECUTE (safe)

- isolate on a working branch (`autopilot/<short-mission>` or as defined in mission.md)
- never push to `main`/`master`/`release/*` directly
- only modify files matching `Q3 allow paths`
- one commit = one candidate
- block destructive flags (`--force`, `--no-verify`, `reset --hard`) at the pre-execute check

### Phase 6 — VERIFY

Run `mission.md` Verify commands.

- all green → success path
- any red → `git restore` + Phase 7 fail path + add the regression pattern to `NOT-OK patterns`

### Phase 7 — LEARN

Append to `journal/YYYY-MM-DD.md`:

```markdown
## <ISO timestamp>

- **Phase 1 도구**: <name + 1-line summary>
- **후보**: <id, 1-line summary>
- **Triage**: passed | rejected (reason)
- **Plan**: <expected diff, verify, rollback>
- **Execute**: <commit hash or dry-run only>
- **Verify**: <green/red, which check, how>
- **결과**: success | failed | skipped | escalated
- **Lesson**: <one line — what the next cycle must know>
- **NOT-OK 갱신**: <pattern added, if any>
- **Cycle counter**: <after this cycle>
- **Next**: <ScheduleWakeup ETA or termination reason>
```

Update `mission.md` `NOT-OK patterns` if anything was learned.

#### Milestone auto-promotion

If the cycle hits any of these, copy the journal entry into `.autopilot.milestones/<date>-<slug>.md`:

1. **PR merged** — a tracked PR transitioned to `MERGED`
2. **Bounded mission completion** — Q2=bounded N reached, all green
3. **First zero-defect achievement** — first time a tracked defect category (lint errors, test failures, coverage gaps) hits zero. Track via `state.json` `defect_baselines.<category>.ever_zero` so repeats do not retrigger.
4. **Novel NOT-OK pattern** — first time this exact anti-pattern is added to `mission.md`

`.autopilot.milestones/` is **fixed and immutable**. The user may delete a wrong milestone manually; the skill will not recreate it unless a fresh trigger fires.

### Phase 8 — NEXT (auto-pace + auto-compact)

In this order:

1. Q8 frequency:
   - `every-cycle` → call built-in `/compact` now
   - `threshold-only` → call `/compact` if estimated token usage ≥ Q8 threshold
   - `off` → skip
2. Append a record to `state.json` `compaction_history`.
3. Q2 routing:
   - `continuous` / `monitor` → `ScheduleWakeup({ prompt: "/autopilot", delaySeconds: <Q6 mapping>, reason: "<why this delay>" })`
     - On 3+ consecutive idle cycles, bump cadence one tier (15m → 30m → 1h-cron → manual)
   - `bounded` and cycle ≥ N → terminate; mark `Mode: done`
   - `Phase 7 escalated` → no `ScheduleWakeup`; await user

---

## Safety policy (every phase)

1. **Forbidden zones (Q4) checked at every phase**, not just Execute. Match → abort + journal entry.
2. **Pre-execute deny-list**: `git push --force`, `git reset --hard`, `rm -rf <outside allow paths>`, DB DDL, external write APIs. Allowed only if mission.md explicitly opts them in.
3. **Q5=L4 still respects Q4.** Free mode is freedom of scope, not freedom of safety.
4. **Same candidate failing 3 times** → add to NOT-OK + move on. All candidates failing → escalate.
5. **Idle limit**: 3 consecutive empty cycles → cadence +1 tier. 10 cumulative idle cycles → propose termination.
6. **Token budget**: 70% per-cycle ceiling triggers split-cycle save instead of fail.
7. **External tools**: only `gh` CLI and `npm` registry. Anything else requires explicit mission.md opt-in.

---

## Interrupts and mission edits

- Any new user message during a wait window interrupts the next cycle.
- "stop autopilot" / "멈춰" / "pause" → no `ScheduleWakeup`, set mission.md `Mode: paused`, ask resume on next call.
- Mission edit request → back up mission.md, edit, apply on next cycle.

## Output protocol

End every cycle with ≤8 lines:

- Phase 1 tool used
- candidate id / title
- result (success / failed / escalated / idle)
- diff or PR link if any
- one-line lesson
- next cycle ETA (cadence)
- last line: exactly one of `AUTOPILOT_CYCLE_DONE`, `AUTOPILOT_PAUSED`, `AUTOPILOT_DONE`, `AUTOPILOT_ESCALATED`

## Termination

- explicit user stop
- bounded N reached
- escalated and user aborts
- 10 consecutive idle cycles + user agrees to end

Mark mission.md `Mode` to `done` / `paused` / `aborted` and append `MISSION_END` to the latest journal entry.

---

## Files this skill writes

```
<repo>/
├── .autopilot.log/                 # default; mission.md may rename via journal_root
│   ├── mission.md
│   ├── state.json
│   ├── proposals/<id>.md
│   └── journal/YYYY-MM-DD.md
└── .autopilot.milestones/          # FIXED — do not change in mission.md
    └── YYYY-MM-DD-<slug>.md
```

The user can rename `journal_root` (e.g. to `docs/improvement/` or `.claude/autopilot/`). `milestones_root` is hard-coded.

---

## Mission.md schema (shipped templates/mission.md is authoritative)

Sections, in order: created/mode/cycle counter, Q1 mission, Q2 operating mode, Q3 allow paths, Q4 forbidden, Q5 risk tier + diff cap, Q6 cadence, Q7 escalation, Q8 auto-compaction, Storage (journal_root, milestones_root), Inference provenance, Tools, Verify commands, NOT-OK patterns, Branch / PR convention.

See `templates/mission.md` for the canonical schema and `templates/state.json`, `templates/journal-entry.md`, `templates/proposal.md`, `templates/milestone.md` for the rest.
