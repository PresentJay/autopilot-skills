import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/autopilot/scripts/check_state.py"
spec = importlib.util.spec_from_file_location("check_state", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class StateChecks(unittest.TestCase):
    def setUp(self):
        self.state = json.loads((ROOT / "skills/autopilot/templates/state.json").read_text())
        self.state.update(mission_id="mission-1", target="artifact://report/revision-1", criteria=["C1", "C2"])

    def completion(self):
        self.state.update(status="done", last_result="goal_verified")
        self.state["verification"] = [
            {"criterion": c, "outcome": "pass", "method": "inspect original source",
             "target_version": "revision-1", "evidence": "journal/checked-source"}
            for c in self.state["criteria"]]
        return self.state

    def test_new_template_is_valid_and_unverified(self):
        self.assertFalse(checker.validate(self.state)["completion_recorded"])

    def test_complete_requires_every_criterion(self):
        good = self.completion()
        self.assertTrue(checker.validate(good)["completion_recorded"])
        good["verification"].pop()
        with self.assertRaisesRegex(ValueError, "every criterion"):
            checker.validate(good)

    def test_empty_search_and_cycle_limit_are_not_completion(self):
        for result in ("no_candidate", "no_change", "progress", None):
            with self.subTest(result=result):
                state = copy.deepcopy(self.state)
                state.update(status="done", last_result=result, cycle_count=100)
                with self.assertRaisesRegex(ValueError, "done requires"):
                    checker.validate(state)

    def test_no_criteria_cannot_complete(self):
        self.state.update(status="done", last_result="goal_verified", criteria=[])
        with self.assertRaises(ValueError):
            checker.validate(self.state)

    def test_missing_or_failed_evidence_cannot_complete(self):
        for field in ("method", "evidence", "target_version"):
            state = copy.deepcopy(self.completion())
            state["verification"][0][field] = " "
            with self.subTest(field=field), self.assertRaises(ValueError):
                checker.validate(state)
        state = self.completion()
        state["verification"][0]["outcome"] = "unverified"
        with self.assertRaises(ValueError):
            checker.validate(state)

    def test_duplicate_and_unknown_criteria_are_rejected(self):
        for bad in ("duplicate", "unknown", "record"):
            state = copy.deepcopy(self.completion())
            if bad == "duplicate":
                state["criteria"].append("C1")
            elif bad == "unknown":
                state["verification"][0]["criterion"] = "C3"
            else:
                state["verification"].append(copy.deepcopy(state["verification"][0]))
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                checker.validate(state)

    def test_monitoring_without_delta_remains_incomplete(self):
        self.state.update(status="idle", last_result="no_change")
        self.assertFalse(checker.validate(self.state)["completion_recorded"])

    def test_code_research_document_and_monitor_targets_need_no_git(self):
        for target in ("/tmp/code@commit+diff", "https://example.test/research@2026-10-21", "doc://brief/revision-3", "source://weekly"):
            state = copy.deepcopy(self.state)
            state.update(status="running", run_id="run-1", target=target)
            self.assertFalse(checker.validate(state)["completion_recorded"])

    def test_schedule_needs_handle_and_matching_timestamp(self):
        self.state["next_wakeup_at"] = "2026-10-22T01:00:00Z"
        with self.assertRaisesRegex(ValueError, "schedule"):
            checker.validate(self.state)
        self.state["schedule"] = {"id": "schedule-1", "next_run_at": self.state["next_wakeup_at"]}
        checker.validate(self.state)
        self.state["schedule"]["next_run_at"] = "2026-10-23T01:00:00Z"
        with self.assertRaises(ValueError):
            checker.validate(self.state)

    def test_types_unknown_schemas_and_unowned_running_rejected(self):
        cases = [{"schema_version": 2}, {"schema_version": True}, {"cycle_count": True},
                 {"criteria": {}}, {"last_result": []}, {"status": []}, {"status": "blocked"},
                 {"status": "running", "run_id": None}, {"status": "idle", "mission_id": ""},
                 {"last_run_at": "2026-10-21"}, {"last_run_at": "not-a-date"}]
        for changes in cases:
            state = dict(self.state, **changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                checker.validate(state)

    def test_read_only_legacy_state_preserves_all_files(self):
        for status in ("fresh", "running", "done", "paused"):
            with tempfile.TemporaryDirectory() as name:
                root = Path(name)
                legacy = {"status": status, "unknown_custom_field": {"retain": True}}
                path = root / "state.json"
                path.write_text(json.dumps(legacy))
                (root / "user-notes.txt").write_text("unfinished user notes")
                before = {p.name: p.read_bytes() for p in root.iterdir()}
                result = checker.inspect(path)
                self.assertTrue(result["legacy"])
                self.assertFalse(result["completion_recorded"])
                self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})

    def test_cli_malformed_and_future_state_unchanged(self):
        for payload in ("{broken", "[]", '{"schema_version":2,"status":"fresh"}'):
            with tempfile.TemporaryDirectory() as name:
                path = Path(name) / "state.json"
                path.write_text(payload)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn("error", json.loads(result.stderr))
                self.assertEqual(path.read_text(), payload)


if __name__ == "__main__":
    unittest.main()
