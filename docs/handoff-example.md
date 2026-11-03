---
layout: page
title: "What an AI task handoff contains: Autopilot's public execution records"
description: "Inspect a real Autopilot journal and state from a code pilot, plus a paused-mission check. Learn what the records show and what recovery claims remain untested."
lang: en
translation_key: handoff-example
---

# When an AI task stops, what should the next session inherit?

The useful handoff is a goal, scope, checked progress and next action that another
session can inspect. Autopilot's public evaluation contains an actual working
record. It does not yet demonstrate that the record makes recovery better.
This article describes repository evaluation artifacts, not a personal testimonial
or a new execution of the current release.

## The task and its record

In the [October 22 code pilot](https://github.com/PresentJay/autopilot-skills/blob/main/evals/results/2026-10-22/code-autopilot/input.json),
the agent was asked to cap a discount percentage at 100, preserve lower-percentage
behavior and leave user notes intact. The evaluated skill was preview revision
`f4a6d33`; current v2 uses persistent records only when they are needed.

The [actual journal](https://github.com/PresentJay/autopilot-skills/blob/main/evals/results/2026-10-22/code-autopilot/journal.md)
records the initial failing test, the change, checks of the result and preservation
of unrelated inputs. The [actual state](https://github.com/PresentJay/autopilot-skills/blob/main/evals/results/2026-10-22/code-autopilot/state.json)
connects acceptance criteria to verification methods, the target version and the
journal. These are concrete artifacts a later session could read, rather than
only a chat message saying “done.”

| Information to carry forward | What the public record contains |
| --- | --- |
| Intended outcome and scope | Discount cap, unchanged lower-range behavior and protected inputs |
| Observed failure and change | The failing test and the cap applied in `discount.py` |
| Checks and target version | Recorded test commands, criteria and version identity |
| Remaining work | Recorded completion state; a completed checkpoint in this case |

The supervising evaluation separately checked the produced code and original
inputs. A plausible state file on its own does not prove that its claims are
true. [Full conditions and limitations](evidence.html).

## A paused mission stayed paused

The [October 29 follow-up](https://github.com/PresentJay/autopilot-skills/blob/main/evals/results/2026-10-29/summary.json)
also inspected a paused mission without authorizing resumption. The original code
and records were preserved byte for byte. This supports respect for a pause; it
is not a successful-resume test. Two explicit durable-record probes reached the
wall limit without a completed turn, so that revised routing was not live-verified.

Neither experiment measured repeated briefing, missed requirements after a
handoff or long-running recovery reliability. All bounded task outputs passed
in the native-goal controls too. No general quality, speed or cost advantage is
established.

## Use the record in your own work

The [interrupted-work guide](when-agent-stops.html) includes installation and
copyable prompts for a durable mission, read-only status and explicit resume.
Keep a record when you need a handoff; short tasks do not automatically create one.
The skill cannot prevent host cancellation or restart a closed app.

The next research question is concrete: does a fresh session need fewer repeated
instructions or miss fewer requirements when it receives this record? That is
tracked in [the fresh-session comparison](https://github.com/PresentJay/autopilot-skills/issues/18).
