#!/usr/bin/env python3
"""Read-only structural checks for Autopilot checkpoints, not an execution proof."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

STATUSES = {"fresh", "idle", "running", "interrupted", "escalated", "paused", "done", "aborted"}
RESULTS = {None, "progress", "no_candidate", "no_change", "blocked", "failed", "goal_verified"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(state):
    if not isinstance(state, dict):
        raise ValueError("State must be a JSON object")
    status = state.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        raise ValueError("Unknown or missing status")
    if "schema_version" not in state:
        return {"legacy": True, "status": status, "completion_recorded": False,
                "notice": "Legacy state: preserve it; inspect evidence before migration or completion"}
    if type(state["schema_version"]) is not int or state["schema_version"] != 1:
        raise ValueError("Unsupported schema_version; preserve the original state")
    for name in ("cycle_count", "consecutive_failures", "consecutive_idle"):
        value = state.get(name, 0)
        if type(value) is not int or value < 0:
            raise ValueError(f"{name} must be a nonnegative integer")
    result = state.get("last_result")
    if not (result is None or isinstance(result, str)) or result not in RESULTS:
        raise ValueError("Unknown last_result")
    criteria = state.get("criteria")
    if not isinstance(criteria, list) or not all(nonempty(c) for c in criteria):
        raise ValueError("criteria must be an array of nonempty IDs")
    if len(set(criteria)) != len(criteria):
        raise ValueError("Duplicate criterion IDs")
    records = state.get("verification")
    if not isinstance(records, list):
        raise ValueError("verification must be an array")
    checked = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each verification must be an object")
        criterion = record.get("criterion")
        if not nonempty(criterion) or criterion not in criteria or criterion in checked:
            raise ValueError("Verification has an unknown or duplicate criterion")
        outcome = record.get("outcome")
        if outcome not in ("pass", "fail", "unverified"):
            raise ValueError("Verification outcome must be pass, fail, or unverified")
        if outcome == "pass" and not all(nonempty(record.get(k)) for k in
                                          ("method", "target_version", "evidence")):
            raise ValueError("Passing verification needs method, target_version, and evidence")
        checked[criterion] = outcome
    complete = bool(criteria) and all(checked.get(c) == "pass" for c in criteria)
    if result == "goal_verified" and not complete:
        raise ValueError("goal_verified requires passing evidence for every criterion")
    if status == "done" and result != "goal_verified":
        raise ValueError("done requires last_result goal_verified, not an empty search or cycle limit")
    if status != "fresh" and not nonempty(state.get("mission_id")):
        raise ValueError("A started mission needs mission_id")
    if status == "running" and (not nonempty(state.get("run_id")) or not nonempty(state.get("target"))):
        raise ValueError("A running checkpoint needs run_id and target identity")
    for name in ("last_run_at", "cycle_started_at", "next_wakeup_at"):
        value = state.get(name)
        if value is not None:
            if not nonempty(value):
                raise ValueError(f"{name} must be an ISO timestamp or null")
            try:
                stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    raise ValueError("Timezone is required")
            except ValueError as exc:
                raise ValueError(f"{name} must include an ISO date, time, and timezone") from exc
    if state.get("next_wakeup_at") is not None:
        schedule = state.get("schedule")
        if not isinstance(schedule, dict) or not nonempty(schedule.get("id")) or schedule.get("next_run_at") != state["next_wakeup_at"]:
            raise ValueError("next_wakeup_at requires the confirmed schedule ID and matching next_run_at")
    return {"legacy": False, "status": status, "completion_recorded": result == "goal_verified" and complete,
            "criteria": len(criteria), "passed": sum(v == "pass" for v in checked.values()),
            "notice": "Record structure checked; verify actual evidence and current target versions separately"}


def inspect(path):
    return validate(json.loads(Path(path).read_text(encoding="utf-8")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="State file to inspect; never rewritten")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.state), ensure_ascii=False))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
