---
name: autopilot
description: Self-driving mission runner — once started, runs an endless discover→analyze→plan→execute→verify→learn cycle on a user-defined mission until told to stop. Boot interview captures mission, allow/forbidden paths, risk tier, cadence, auto-compact threshold, escalation, update policy, resume policy. Safety policy blocks forbidden zones at every phase, forces dry-run for risky ops, learns NOT-OK patterns from failures. Self-heals after interrupted cycles or missed wakeups. Universal across AI coding agents (Claude Code, Codex, Cursor, Gemini, ...). Triggers - "autopilot", "self-drive", "자율주행", "auto drive", "autonomous mode", "run cycle", "resume autopilot", "heal autopilot".
version: 1.3.0
---

# Autopilot — Self-driving mission runner

You receive a mission from the user and run an autonomous loop until they tell you to stop. The domain is whatever the user defines in the mission file — code self-improvement, doc grooming, research synthesis, ops sweeps, anything that benefits from a tight discover→execute→learn cadence.

This skill replaces ad-hoc loops (ralph-loop, improve-airops) with a domain-agnostic orchestrator: per-project mission, mission-bound governance, idle-aware self-pacing via `ScheduleWakeup`, immutable milestone trail, **self-healing on interruption**, and **opt-in update notifications**.

## Boot check

First action on every invocation: locate the mission file.

- Default path: `<repo-root>/.autopilot.log/mission.md`.
- Fallbacks (legacy / migration): `<repo-root>/.claude/autopilot/mission.md`. If found, offer migration to default path on first run.
- Outside a git repo: `~/.claude/autopilot/<session-id>/mission.md`.

Decision:

- **Missing** → run "Boot interview" below.
- **Exists, user explicitly says "new mission" / "reset" / "redo"** → back up to `mission.md.bak.<timestamp>`, run interview again.
- **Exists, normal call or `/autopilot resume` / `/autopilot heal` / `/autopilot status`** → enter "Phase 0.5 — Resume + update check", then "Operating cycle".

## User signals

| Signal | Effect |
|---|---|
| `/autopilot` | Auto-detect stale state, then run a cycle (or no-op if mission complete) |
| `/autopilot resume` | Force `Mode: paused` → `active`, run a cycle |
| `/autopilot heal` | Force interruption recovery (clean working branch, mark crashed cycle, start fresh) |
| `/autopilot status` | Print current state from `state.json` + last journal entry (includes installed version line); do **not** run a cycle |
| `/autopilot version` (or `--version`, `-v`) | Print installed `version` from frontmatter, latest available from GitHub releases (cached), source URL; do **not** run a cycle |
| `/autopilot stop` / "멈춰" / "pause" | Set `Mode: paused`, no `ScheduleWakeup` |
| `/autopilot quick mission="X"` (or `/autopilot --quick`) | All Q's default-pre-filled, single confirm — **new in v1.3.0** |
| `/autopilot mission="X" risk=L2 cadence=15m ...` | Args parsed into Q1–Q10 pre-fills |

---

## Version display (new in v1.2.0)

`/autopilot version` (aliases: `--version`, `-v`) is a diagnostic-only signal. It does **not** run a cycle, ScheduleWakeup, or modify any file. Run order:

1. Read installed `version:` from this SKILL.md frontmatter.
2. Read `last_update_check_at` and `available_version` from `state.json` (if present).
3. If the cache is older than `Q9.check` interval (or missing), do **one** GitHub releases call (5s timeout, fail-open):

   ```bash
   curl -s --max-time 5 https://api.github.com/repos/PresentJay/autopilot-skills/releases/latest
   ```

   Update the cache fields on success; leave them on failure.
4. Print:

   ```
   autopilot v<installed>
     installed at: <SKILL.md absolute path>
     latest:       v<latest> (checked <ISO>, <fresh|cached|unknown>)
     source:       https://github.com/PresentJay/autopilot-skills

   Update: up-to-date
   ```

   When `latest > installed` (semver compare), replace the last line with:

   ```
   Update: v<installed> → v<latest> — npx skills update PresentJay/autopilot-skills
   ```

   When the cache is missing AND the live call failed, print `latest: unknown (offline)` and `Update: check skipped`.
5. Exit. Do not append to journal, do not bump heartbeat, do not call `ScheduleWakeup`.

`/autopilot status` reuses step 1 and step 4's first line so the installed version appears at the top of its diagnosis output too.

---

## Boot interview (mission contract)

Goal: capture mission, scope, risk, cadence, compaction, escalation, update policy, resume policy in 10 short questions. Use `AskUserQuestion`, one question per turn, narrowing if the answer is unclear.

**Inference from invocation args**: if the user passes hints in the same turn (e.g. `/autopilot mission="lint cleanup" risk=L2 cadence=15m`), parse `key=value` pairs and pre-fill matching answers. Show the pre-filled draft once and offer:

1. Start as-is
2. Modify a few questions (cascade to those only)
3. Re-do from scratch

Do **not** scan prior conversation, git history, or other artifacts. Args only. Cold start when no args given.

**Quick boot (new in v1.3.0)**: if `quick` (positional) or `--quick` is in the args, **all Q's default to safe values** (Q2=continuous, Q3=default, Q4=default, Q5=L2, Q6=15m, Q7=defaults, Q8=auto-suggest@80, Q9=every-24h prompt, Q10=2x auto-resume). Q1 still required (from `mission="X"` arg or one prompt). Single summary, single confirm — total one turn boot. Use this when the user already knows what they want and asked you to "just go".

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

### Q8. Compaction strategy (revised in v1.3.0)

Long-running loops bump into the prompt-too-long ceiling. **The agent cannot programmatically call `/compact`** in Claude Code, Codex, Cursor, or any current harness — `/compact` is a user-typed slash command. The skill therefore outputs a *suggestion* and relies on either the user typing `/compact` or, for genuinely long missions, `/schedule` cron promotion (each scheduled run is a fresh session — no compaction needed).

- **threshold**: 60 / 70 / 80 / 90 — surface advisory when token usage crosses this percent. Default **80**.
- **strategy**:
  - `auto-suggest` *(default)* — output `📦 /compact suggested (estimated ~N% used)` at the end of every cycle once threshold is crossed; do not block
  - `cron-promote` — explicitly recommend `/schedule "<cron> /autopilot"` so each cycle starts fresh; output the suggested cron line once
  - `off` — silent; user accepts prompt-too-long risk

If Q6 cadence is `1h+`, the skill auto-promotes to `/schedule` cron regardless of Q8 strategy (already in Phase 8 routing).

### Q9. Update policy (new in v1.1.0)

The skill ships with a `version` field in its frontmatter. Newer releases on `PresentJay/autopilot-skills` are detected by an unauthenticated GitHub releases API call (cached for 24h in `state.json.last_update_check_at`).

- **check**: `every-boot` / `every-24h` / `weekly` / `off` — default **`every-24h`**
- **on-update-available**:
  - `notify` — append a one-line notice to the cycle output (passive)
  - `prompt` *(default)* — show notice and ask "update now?"; on confirm, run `npx skills update PresentJay/autopilot-skills --yes` via Bash, then ask user to re-invoke `/autopilot`
  - `silent-auto` — run the update without asking (least recommended; only for trusted setups)

The check fails open: if GitHub API errors or times out (5s cap), skip silently and retry next interval. The skill never blocks on this check.

### Q10. Resume policy (new in v1.1.0)

Controls how the skill recovers from interruptions (host sleep, session crash, missed `ScheduleWakeup`, mid-cycle abort).

- **stale_threshold**: `2x-cadence` *(default)* / `4x-cadence` / `8x-cadence` — how long after `next_wakeup_at` to consider the loop stalled
- **on_resume**:
  - `auto-resume` *(default)* — silently detect stale state and run a fresh cycle
  - `prompt-confirm` — show diagnosis ("Missed N cycles. Resume?") and confirm before continuing
  - `manual-only` — only resume on explicit `/autopilot resume` or `/autopilot heal`

### Wrap

Render the proposed `mission.md` to the user. Wait for one explicit confirm before starting the first cycle. Save mission.md, state.json, and create `.autopilot.log/` and `.autopilot.milestones/` directories.

---

## Phase 0.5 — Resume + update check (new in v1.1.0)

Runs **once per invocation**: after boot check, before Phase 1 DISCOVER. **Note (v1.3.0):** Phase 0.5 is meaningful only at *invocation boundaries* — i.e., each fresh `/autopilot` call (manual or via `ScheduleWakeup`). Multiple cycles within a single conversation turn (no wakeup boundary) is batch execution, not self-driving — Phase 0.5 fires once at the top, not between in-turn cycles. Two independent sub-checks:

### Resume check

Read `state.json`:

```
status            : idle | running | interrupted | escalated | paused
last_run_at       : ISO timestamp or null
next_wakeup_at    : ISO timestamp or null
cycle_started_at  : ISO timestamp or null
```

Decision matrix (apply per `Q10.on_resume`):

| Condition | Diagnosis | Action |
|---|---|---|
| `cycle_started_at` is set AND `last_run_at` < `cycle_started_at` (or null) | Crashed mid-cycle | On `autopilot/<slug>` branch: `git restore .` + `git clean -fd`. Append `interrupted` entry to journal. Reset `status: idle`, `cycle_started_at: null`. Continue. |
| `next_wakeup_at` set AND `now - next_wakeup_at` > `Q10.stale_threshold × cadence` | Missed wakeups | Compute missed count = floor((now - next_wakeup_at) / cadence). Surface "🔁 Resumed after N missed cycles." per `Q10.on_resume`. Continue. |
| `next_wakeup_at` is null AND `Mode: active` | Schedule lost (post-failure with no record) | Surface "🔁 Schedule lost — re-arming." Continue and re-arm at end. |
| `Mode: paused` AND user signal != `/autopilot resume` | Intentionally paused | Print state, ask "resume?" If yes, set `Mode: active`. If no, exit. |
| `Mode: paused` AND user signal = `/autopilot resume` | Explicit resume | Set `Mode: active`. Continue. |
| `/autopilot heal` (any state) | Forced recovery | Treat as crashed-mid-cycle: `git restore .` + journal interrupted entry + status reset, regardless of detected state. |
| `/autopilot status` | Diagnostic only | Print state, last 3 journal entries, next_wakeup_at, missed count. **Do not** run a cycle. Exit. |
| All clean | Normal | Continue silently. |

Append every recovery to `state.json.interruption_history`:

```json
{ "at": "<ISO>", "type": "crashed-mid-cycle | missed-wakeups | schedule-lost | manual-heal", "recovered": true, "details": "..." }
```

### Update check

Run when (a) Q9.check ≠ `off` AND (b) `now - state.json.last_update_check_at > Q9.check interval` (or `last_update_check_at` is null).

```bash
LATEST=$(curl -s --max-time 5 https://api.github.com/repos/PresentJay/autopilot-skills/releases/latest | sed -nE 's/.*"tag_name": "v?([^"]+)".*/\1/p')
```

If LATEST is empty (network/API error), fail-open: skip and retry next interval.

If LATEST > current SKILL.md `version` (semver compare):
- `Q9.on-update-available = notify`: append "📦 Update v{current} → v{latest}: `npx skills update PresentJay/autopilot-skills`" to cycle output.
- `prompt`: show notice, ask "update now?". If yes:
  ```bash
  npx -y skills update PresentJay/autopilot-skills --yes
  ```
  Then surface "Updated. Re-invoke `/autopilot` to use v{latest}." and exit (do **not** continue cycle on stale skill code).
- `silent-auto`: run the update Bash command, exit with the same re-invoke prompt.

Cache result regardless of outcome:

```json
state.json.last_update_check_at = <now ISO>
state.json.available_version    = <latest tag or null>
```

---

## Operating cycle (one cycle per invocation)

8 phases. Bail-out rule: if the per-cycle token budget exceeds 70%, save partial state under "split-cycle" and resume at the failed phase next time.

**Heartbeat (every cycle):**
- At Phase 1 start: `state.json.cycle_started_at = now`, `status = running`.
- At Phase 8 end: `state.json.last_run_at = now`, `next_wakeup_at = now + cadence`, `cycle_started_at = null`, `status = idle`.

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
- **결과**: success | failed | skipped | escalated | interrupted
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

1. Update heartbeat (see "Heartbeat" above).
2. Q8 strategy (advisory only — agent cannot run `/compact`):
   - `auto-suggest` → if estimated token usage ≥ Q8 threshold, append `📦 /compact suggested (~N% used)` to cycle output
   - `cron-promote` → if cycle count ≥ 5 and Q6 cadence is sub-hour, append one-time `📅 Long mission detected — consider /schedule "@hourly /autopilot"`
   - `off` → skip both
3. Append the advisory event (not a real compaction) to `state.json.compaction_history` with `kind: "advisory"`.
4. Q2 routing:
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
8. **Update auto-run (Q9 silent-auto)**: only runs `npx skills update <repo> --yes`. No other commands.

---

## Interrupts and mission edits

- Any new user message during a wait window interrupts the next cycle.
- "stop autopilot" / "멈춰" / "pause" → no `ScheduleWakeup`, set mission.md `Mode: paused`, ask resume on next call.
- Mission edit request → back up mission.md, edit, apply on next cycle.

## Output protocol

End every cycle with ≤8 lines:

- Phase 1 tool used
- candidate id / title
- result (success / failed / escalated / idle / interrupted-recovered)
- diff or PR link if any
- one-line lesson
- next cycle ETA (cadence)
- (if applicable) update notice or resume diagnosis
- last line: exactly one of `AUTOPILOT_CYCLE_DONE`, `AUTOPILOT_PAUSED`, `AUTOPILOT_DONE`, `AUTOPILOT_ESCALATED`, `AUTOPILOT_RESUMED`, `AUTOPILOT_UPDATED`

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

Sections, in order: created/mode/cycle counter, Q1 mission, Q2 operating mode, Q3 allow paths, Q4 forbidden, Q5 risk tier + diff cap, Q6 cadence, Q7 escalation, Q8 auto-compaction, **Q9 update policy**, **Q10 resume policy**, Storage (journal_root, milestones_root), Inference provenance, Tools, Verify commands, NOT-OK patterns, Branch / PR convention.

See `templates/mission.md` for the canonical schema and `templates/state.json`, `templates/journal-entry.md`, `templates/proposal.md`, `templates/milestone.md` for the rest.
