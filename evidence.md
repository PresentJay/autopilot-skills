---
layout: page
title: "Evidence and limitations"
lang: en
---

# Does Autopilot earn its overhead?

**A general advantage over native goals is not demonstrated.** In the original small pilot, all three approaches met the supplied task requirements. Autopilot added a structured journal and state, but used more native-goal tokens and elapsed time. There is no measured quality, speed, or long-running reliability advantage here.

## Bounded-task follow-up — 2026-10-29

The preview now performs a bounded task directly from the entrypoint. It retains output verification and user-edit protection, but does not require durable state, journals, whole-workspace hash inventories, or the detailed mission guides. Existing paused missions are still honored. Persistent records remain available for handoffs, monitoring, and explicit record requests.

We reran the same three fixtures with a strong native goal, the previous preview ([7288f62](https://github.com/PresentJay/autopilot-skills/tree/7288f6223b0be0c4c1541d7fed09da8c9bdfda54/skills/autopilot)), and the revised skill ([b4b1f3b](https://github.com/PresentJay/autopilot-skills/tree/b4b1f3bd7fc69a256b11e82c2fdc76b152435b4b/skills/autopilot)). All used Codex **0.164.0**, **gpt-6-astra**, medium effort, the same prompts and 60,000-token/180-second limits. The CLI changed since the original pilot; do not present these as a controlled change from its 2.22× figure.

| Task | Strong goal tokens | Previous skill tokens | Revised skill tokens |
| --- | ---: | ---: | ---: |
| Code | 10,883 | 15,877 | 12,478 |
| Research | 4,578 | 17,715 | 7,321 |
| Documents | 5,734 | 16,215 | 19,132 |
| Total | **21,195** | **49,807** | **38,931** |

The revised skill used **21.8% fewer native-goal tokens than the previous skill in these completed runs**, and **1.84× the strong-goal total**. This is a descriptive sample, not an expected saving. **The document task increased by 18.0%**, even though it also avoided the extra records and reference reads. Cache counters differed between runs, and there is only one completed run per task/condition. Removing procedures does not guarantee lower measured token usage on every task. These counters are not an invoice.

All nine completed outputs met the original task requirements. Code outputs passed the two supplied tests and the 45-case numeric grid; original input files and user notes were preserved. The three revised tasks created **zero new runtime record files**, and their command traces showed **zero explicit reads of references/templates/checker source**. The research control delivered its report in the final answer, which the mission allows; we did not require an extra file just for grading. Semantic review remains unblinded and performed by the supervising agent.

Four initial attempts reached the wall limit with no agent output, no completed turn, and zero native-goal tokens reported. They are retained in the public summary. Those task/condition pairs were retried after concurrency reduced; the failed starts are not artifact-quality results. Runner processes briefly overlapped up to five despite a planned maximum of three. Shared load, non-random order, no cache control, and retries confound timing, so no speedup is claimed. The builtin apps server and the account's session-start hook were observed in the newer host despite disabling configured plugins/servers; no external app actions were used by the scored tasks. This is not a clean-system benchmark.

After these runs, the Codex UI default prompt was aligned with the conditional-record policy; that UI entrypoint itself was not live-tested. The measured entrypoint and references remain unchanged.

A separate paused-mission probe preserved all original code and records byte for byte. The explicit durable-record probe was attempted twice but reached the wall limit before any agent output; its revised routing is therefore **not live-verified**. Both failed probes are retained separately and are excluded from the task-token comparison.

The exact candidate/input hashes, prompts, artifacts, full thread counters, all attempts, and the prewritten grading/routing criteria are in [the follow-up results](https://github.com/PresentJay/autopilot-skills/tree/main/evals/results/2026-10-29). Long-session handoff effectiveness and broader quality advantages remain unproven.

## What was compared

On 2026-10-22, we ran three local tasks in three conditions: plain native goal, a native goal with explicit verification/preservation instructions, and that same stronger goal plus Autopilot v2 preview. One run per task and condition: **nine scored runs**, not nine repeated trials of the same task.

- **Code:** cap a discount percentage at 100; preserve lower-percentage behavior and user notes.
- **Research:** compare local vendor inputs, one unavailable; cite evidence and identify unknowns.
- **Documents:** write a short brief from supplied figures without inventing causal or revenue claims.

The mission text already includes reasonable requirements in all conditions. The stronger control adds explicit verification, scope, and uncertainty instructions. The measured skill is pinned to [f4a6d33](https://github.com/PresentJay/autopilot-skills/tree/f4a6d33c600674beded74c5b5571408944650e85/skills/autopilot). Exact prompts, inputs, outputs, record samples, and candidate file hashes are public in the [evaluation directory](https://github.com/PresentJay/autopilot-skills/tree/main/evals).

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

After the pilot, the host reference’s fallback wording was aligned with the main instructions: continue within the current turn instead of stopping after one checkpoint. All scored runs used native goals; the revised fallback itself has not been evaluated with live tasks.

## What the package checks establish

The deterministic suite checks state structure, version/reference consistency, legacy-state handling, and read-only preservation. It does **not** establish that a model's evidence is true. A plausible evidence string can pass the state checker without the referenced artifact existing. [Issue #19](https://github.com/PresentJay/autopilot-skills/issues/19) tracks artifact-bound evidence checks.

Native goals already provide continued execution and completion tracking. Autopilot's proposed benefit is reusable mission context and an inspectable handoff across code, research, and documents. That benefit needs direct testing before it becomes a performance claim.

Next: [fresh-session matched evaluation (#18)](https://github.com/PresentJay/autopilot-skills/issues/18), [interrupted recovery (#20)](https://github.com/PresentJay/autopilot-skills/issues/20), and [a more realistic research fixture (#21)](https://github.com/PresentJay/autopilot-skills/issues/21).
