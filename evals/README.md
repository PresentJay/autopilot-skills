# Native-goal pilot

This is an opt-in functional pilot, not a general performance benchmark. Read [the evidence and exclusions](../docs/evidence.md) before interpreting the numbers. All nine scored outputs met the small tasks; Autopilot used more tokens and time. Long-running usefulness remains untested.

## Bounded-task follow-up (2026-10-29)

`results/2026-10-29/` compares the previous preview at `7288f62`, the revised skill at `b4b1f3b`, and a strong goal under CLI 0.164.0. It retains all 13 matched-task attempts (nine completed, four timed out before agent output), separate routing probes, and the grading criteria fixed before execution. The revised tasks create no runtime records or explicit reference/template/checker reads. Aggregate goal tokens fell 21.8% against the previous skill in this sample; the document case increased 18.0%, and the strong goal still used less in total. No general saving or speedup is established.

The same runner was used for both revisions; a private wrapper selected an extracted skill tree for the previous arm. To reproduce, use separate checkouts of the two pinned revisions and run the same fixtures with the documented command/model/limits. The routing inputs are included under `routing-inputs/`; invoke the skill on those briefs to inspect pause protection and explicit durable records. The paused probe requires no changes, including to its supplied code; it is an inspection goal, not authorization to resume. The ordinary code rubric must not be applied to it.

The paused routing probe passed. Both explicit durable-record probes reached the wall limit before agent output, so the revised durable routing remains unverified; do not infer runtime compatibility from its structural tests. These probes are recorded separately from the 13 matched-task attempts.

The revised research arm had one failed start and a successful retry; its control also had a failed start and a successful retry. Retry metadata, shared global instructions/hooks, observed builtin app startup, non-random order, cache differences, and a temporary concurrency deviation are disclosed in the evidence page and JSON summary. Raw host events remain private.

## Inspect without model usage

The measured skill is pinned to commit `f4a6d33c600674beded74c5b5571408944650e85`; the summary includes per-file hashes. The current preview subsequently clarifies the non-goal fallback wording, which was not exercised by this pilot.

`fixtures/` contains the original missions and inputs. `results/2026-10-22/` contains exact prompts, generated outputs, Autopilot record samples, and a JSON summary with candidate/input hashes. Research/document grading was an unblinded supervising-agent review against the inputs; see the criteria in the summary. The supplied code tests can be rerun against each output by placing `discount.py` beside `fixtures/code/test_discount.py` in a temporary directory.

Public records omit raw events, authentication, global instructions, thread IDs, and machine paths. `<WORKDIR>` replaces a working-directory path where needed. Output text is otherwise preserved. The model's journals are evidence of what it recorded, not independent proof.

## Run deliberately

Requires Python 3.11+, an authenticated Codex CLI with native app-server goals, and access to your selected model. The tested CLI is 0.154.0. Live runs consume account usage and create persisted local Codex threads. They are never run by CI.

```sh
python3 evals/run_native_goals.py code plain \
  --model YOUR_MODEL --output /tmp/autopilot-pilot --live
```

Use `code`, `research`, or `documents`; arms are `plain`, `strong`, and `autopilot`. Repeat with a new output directory for each repetition. The runner refuses to overwrite completed runs. It discovers and disables installed skills for its child processes, disables configured MCP servers/plugins, and copies the candidate skill only for the Autopilot arm. It does not modify your configuration. Global host instructions may still apply; inspect the private run metadata.

The model receives workspace-only, offline instructions. Review your host's sandbox configuration before using untrusted fixtures. Do not publish raw run directories: they include local paths and host events. Review and redact artifacts before sharing them.

The scored pilot used the same protocol with a locally saved skill inventory. The portable runner adds discovery, explicit `--live`, private output placement, a nonzero exit on incomplete execution, and timeout handling that requires both goal and turn completion. A separate code/plain smoke run verifies this portable path; it is excluded from the nine scored results.

## What would make the next result informative?

Use longer tasks with actual interruptions and changed requirements. Fix the grading rubric before execution, randomize order, repeat each condition, and report failures alongside successes. Keep the strong-goal control. Measure correctness, user interventions, duplicate work, preserved edits, token accounting, and time separately. Do not infer billed cost from token totals alone.

[Evaluation issue #18](https://github.com/PresentJay/autopilot-skills/issues/18) coordinates that work. A fixture PR does not need paid model runs.
