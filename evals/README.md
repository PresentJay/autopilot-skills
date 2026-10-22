# Native-goal pilot

This is an opt-in functional pilot, not a general performance benchmark. Read [the evidence and exclusions](../docs/evidence.md) before interpreting the numbers. All nine scored outputs met the small tasks; Autopilot used more tokens and time. Long-running usefulness remains untested.

## Inspect without model usage

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
