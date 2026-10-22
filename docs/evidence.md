---
layout: page
title: "Evidence and limitations"
lang: en
---

# Does Autopilot earn its overhead?

**Not demonstrated yet.** In this small pilot, all three approaches met the supplied task requirements. Autopilot added a structured journal and state, but used more native-goal tokens and elapsed time. There is no measured quality, speed, or long-running reliability advantage here.

## What was compared

On 2026-10-22, we ran three local tasks in three conditions: plain native goal, a native goal with explicit verification/preservation instructions, and that same stronger goal plus Autopilot v2 preview. One run per task and condition: **nine scored runs**, not nine repeated trials of the same task.

- **Code:** cap a discount percentage at 100; preserve lower-percentage behavior and user notes.
- **Research:** compare local vendor inputs, one unavailable; cite evidence and identify unknowns.
- **Documents:** write a short brief from supplied figures without inventing causal or revenue claims.

The mission text already includes reasonable requirements in all conditions. The stronger control adds explicit verification, scope, and uncertainty instructions. Exact prompts, inputs, outputs, record samples, and candidate file hashes are public in the [evaluation directory](https://github.com/PresentJay/autopilot-skills/tree/improve/codex-missions-v2/evals).

## Observed results

Each cell shows **native goal tokens / elapsed seconds**. These are not billed dollar costs. This is the native goal counter, not the thread’s full input/output token total. The JSON summary also includes the thread’s input, cached-input, output, and reasoning token counters; neither measure is an invoice. Accounting is specific to the host; elapsed time includes tool execution and polling overhead.

| Task | Goal | Strong goal | Strong goal + Autopilot |
| --- | ---: | ---: | ---: |
| Code | 5,725 / 27.2s | 6,333 / 38.5s | 11,871 / 59.0s |
| Research | 5,086 / 28.4s | 9,566 / 37.3s | 24,894 / 59.5s |
| Documents | 6,084 / 37.4s | 9,352 / 33.4s | 19,381 / 59.2s |

All nine outputs passed the artifact review. Across these three tasks, Autopilot used **56,146** native-goal tokens versus **25,251** for the stronger goal (**2.22×**) and **16,895** for the plain goal (**3.32×**). These are descriptive totals from one small sample, not expected multipliers for other work.

The Autopilot runs produced `state.json`, a verification journal, and an input baseline. They reused the supplied protected `mission.md`; acceptance criteria were recorded in the journal rather than rewriting the input. This establishes that the record was produced, **not that it made later work better**. No fresh-session handoff was scored.

## How outputs were checked

The supervising agent reran the two supplied code tests and independently checked 45 numeric cases for each code output, including negative prices/percentages and values immediately around the cap. Original source inputs and user notes were compared byte for byte in all nine runs. Research reports and briefs were read against the source statements and mission requirements.

The semantic review was **unblinded and performed by the supervising agent**, not a human panel or an independent evaluator model. The review criteria came from the existing missions; the additional numeric grid and publication rubric were written after execution. This is a functional pilot, not a preregistered benchmark. A native goal's `complete` status was not used as the quality oracle.

## Conditions and limits

- Codex CLI **0.154.0**, model identifier **gpt-6-astra**, medium effort. Model availability depends on the account; substitute your available model and report it.
- Same 60,000-token native goal budget and 180-second wall limit for every scored run. At most three simultaneous runs; order was not randomized.
- Native goals were created on persisted local threads. Automatic skill discovery, MCP servers, and plugins were disabled for the evaluation processes. Only the Autopilot arm explicitly read the copied skill. No user configuration was changed.
- The host still reported the account's global instruction file. It was shared across all arms; this is not a clean-system benchmark. Raw host events and private instruction paths are not published.
- No network or external services were permitted by the task instructions. Local sandbox policy and tool availability remain host responsibilities; the skill is not enforcement.
- Setup attempts with invalid process overrides or unsupported ephemeral goals were excluded before task execution. Two timing-calibration runs were excluded because the first harness stopped at goal completion before the final turn finished. The nine scored runs waited for both. These exclusions and the non-random ordering limit interpretation.
- The portable runner includes output-path/privacy checks, automatic discovery isolation, and stricter timeout accounting added after the scored runs. The prompts and scored conditions are unchanged; see its usage and smoke-check notes in `evals/README.md`.
- Tiny tasks, one attempt per condition, shared local resources, no cache control, no long execution, no human-intervention measurement, and no cross-host or cross-session trial. No claim about production ROI follows.

## What the package checks establish

The deterministic suite checks state structure, version/reference consistency, legacy-state handling, and read-only preservation. It does **not** establish that a model's evidence is true. A plausible evidence string can pass the state checker without the referenced artifact existing. [Issue #19](https://github.com/PresentJay/autopilot-skills/issues/19) tracks artifact-bound evidence checks.

Native goals already provide continued execution and completion tracking. Autopilot's proposed benefit is reusable mission context and an inspectable handoff across code, research, and documents. That benefit needs direct testing before it becomes a performance claim.

Next: [fresh-session matched evaluation (#18)](https://github.com/PresentJay/autopilot-skills/issues/18), [interrupted recovery (#20)](https://github.com/PresentJay/autopilot-skills/issues/20), and [a more realistic research fixture (#21)](https://github.com/PresentJay/autopilot-skills/issues/21).
