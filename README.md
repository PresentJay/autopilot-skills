# Autopilot

**Give your agent a mission it can carry forward.**

Autopilot is a portable mission workflow for code, research, and documents.
It keeps the outcome, scope, checks, and next action together so work can continue
without rebuilding the brief at every checkpoint. It uses your agent's tools and
native goal mode when available.

[Website](https://presentjay.github.io/autopilot-skills/) ·
[Evidence](docs/evidence.md) · [Roadmap](ROADMAP.md) ·
[Contribute](CONTRIBUTING.md) · [한국어](https://presentjay.github.io/autopilot-skills/ko/)

> **[v2.0.0 released](https://github.com/PresentJay/autopilot-skills/releases/tag/v2.0.0).**
> No speed or quality advantage over native goals has been established.

## Why use it?

Use Autopilot when a reusable mission and an inspectable handoff matter: improving
a repository over several checkpoints, investigating a question with incomplete
sources, or preparing a document from evidence. You get the same mission format
and recovery conventions across those tasks.

A well-specified one-off task may need only a native goal. Goals already support
continuation and completion checks. Autopilot earns its place only if its added
structure reduces repeated briefing, missed work, or supervision for your task.
See the [comparison and limits](docs/comparison.md).

## Install

```sh
npx skills add PresentJay/autopilot-skills --skill autopilot
```

In Codex, invoke `$autopilot`. In Claude Code, invoke `/autopilot`.
For execution across turns, explicitly request native goal mode in a host that
provides it. The skill itself cannot keep a closed app running.

```text
$autopilot Improve this repository's import reliability. Reproduce the failure,
fix it without changing the public API, and verify the existing integration tests.
Use native goal mode to continue until complete. Leave unrelated edits intact.
```

```text
$autopilot Compare these vendor specifications for latency and offline support.
Write a source-backed report. If a specification is inaccessible, report that
gap rather than inventing its contents. Use only the supplied files.
```

```text
$autopilot Turn source.txt into a brief for a nontechnical reader. Check every
figure and preserve the source's limitations. Keep my existing notes.
```

## Keep short tasks short

A task that can finish in the current invocation uses only the skill entrypoint.
It still verifies the output and preserves existing edits, but does not create
state/journal files, hash the whole workspace, or read the durable-mission guides.
An active native goal already owns its execution bookkeeping.

Use persistent records when work must continue in another session, monitoring
needs previous results, or you explicitly ask for an auditable mission record.
Existing mission records are always honored, including a stored pause.

## What stays with a durable mission

- `mission.md`: outcome, scope, acceptance criteria, stopping conditions.
- `state.json`: current checkpoint, observed results, and target version.
- A journal: evidence, unresolved work, and the next useful action.

The default directory is `.autopilot.log/`; existing custom paths are preserved.
`status` and `version` are read-only. `resume` inspects interrupted work before
continuing. `pause` records a pause. `run-once` limits work to one checkpoint.
An ordinary mission continues within the available execution until its agreed
boundary; it does not stop just because a checkpoint was recorded.

## Evidence and limitations

The [evidence page](docs/evidence.md) separates functional checks from comparative
performance. The state checker validates record structure, not the truth or
freshness of a check. Markdown scope rules are not a sandbox or a distributed lock.
Scheduling, permissions, compaction, and background execution belong to the host.
Installation compatibility does not establish tested runtime support.

Code, research, and document fixtures are included for repeatable evaluation.
Short fixtures cannot establish long-running reliability or user time saved.
Help us test those claims through the [roadmap](ROADMAP.md).

## Develop and contribute

```sh
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
```

No third-party Python runtime dependency is required. Use Python 3.11+ for the
optional native-goal pilot runner. Run live evaluations only when you intend to
spend model usage; CI runs deterministic checks only.

Start with a reproducible mission failure, make one focused change, and show its
effect on the actual artifact. [Contribution guide](CONTRIBUTING.md) ·
[Open issues](https://github.com/PresentJay/autopilot-skills/issues)

MIT · Built and maintained by [PresentJay](https://github.com/PresentJay).
