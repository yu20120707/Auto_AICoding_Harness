from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.task_state import (  # noqa: E402
    assert_valid_task_payload,
    assert_valid_transition,
    load_active_task_supplement,
    validate_task_payload,
    validate_task_status_consistency,
    validate_transition,
)


def valid_task_payload(**overrides: object) -> dict:
    payload = {
        "schema_version": 1,
        "id": "TASK-20260615-example",
        "mode": "large",
        "status": "planning",
        "source": {
            "epic": ".ai/epic.md",
            "spec": ".ai/spec.md",
            "plan": ".ai/implementation-plan.md",
        },
        "scope": ["core/task_state.py", "bin/ai-status"],
        "created_at": "2026-06-15T00:00:00+08:00",
        "updated_at": "2026-06-15T00:00:00+08:00",
        "review": {
            "status": "none",
            "last_review": None,
        },
        "approval": {
            "status": "none",
            "approved_by": None,
            "rejected_reason": None,
        },
        "artifacts": {
            "context_manifest": "context.jsonl",
            "review": "review.md",
            "rca": "rca.md",
            "final": "final.md",
        },
    }
    payload.update(overrides)
    return payload


class TaskStateUnitTest(unittest.TestCase):
    def test_valid_task_payload_passes_schema_validation(self) -> None:
        payload = valid_task_payload()

        self.assertEqual(validate_task_payload(payload), [])
        assert_valid_task_payload(payload)

    def test_invalid_task_payload_reports_clear_errors(self) -> None:
        payload = valid_task_payload(
            schema_version=2,
            mode="medium",
            status="done",
            scope="core/task_state.py",
            artifacts={"review": "review.md"},
        )
        del payload["source"]

        errors = validate_task_payload(payload)

        self.assertIn("missing required keys: source", errors)
        self.assertIn("unsupported schema_version: 2", errors)
        self.assertIn("invalid mode for task supplement: medium", errors)
        self.assertIn("invalid status: done", errors)
        self.assertIn("scope must be a list", errors)
        self.assertIn("artifacts missing required keys: context_manifest, final, rca", errors)
        with self.assertRaisesRegex(ValueError, "invalid task supplement"):
            assert_valid_task_payload(payload)

    def test_valid_transitions_pass(self) -> None:
        for current_status, next_status in [
            ("planning", "ready"),
            ("ready", "implementing"),
            ("implementing", "reviewing"),
            ("reviewing", "waiting_approval"),
            ("waiting_approval", "approved"),
            ("waiting_approval", "rejected"),
            ("rejected", "needs_fix"),
            ("needs_fix", "implementing"),
            ("approved", "finalizing"),
            ("finalizing", "completed"),
            ("blocked", "planning"),
        ]:
            with self.subTest(current_status=current_status, next_status=next_status):
                self.assertEqual(validate_transition(current_status, next_status), [])
                assert_valid_transition(current_status, next_status)

    def test_illegal_transition_fails(self) -> None:
        errors = validate_transition("planning", "completed")

        self.assertEqual(
            errors,
            ["illegal task transition: planning -> completed; allowed: blocked, implementing, ready"],
        )
        with self.assertRaisesRegex(ValueError, "planning -> completed"):
            assert_valid_transition("planning", "completed")

    def test_task_status_consistency_accepts_matching_gate_state(self) -> None:
        payload = valid_task_payload(status="waiting_approval")
        state = {"status": "WAITING_HUMAN_DIFF_APPROVAL"}

        self.assertEqual(validate_task_status_consistency(payload, state), [])

    def test_task_status_consistency_rejects_completed_before_workflow_done(self) -> None:
        payload = valid_task_payload(status="completed")
        state = {"status": "WAITING_HUMAN_DIFF_APPROVAL"}

        self.assertEqual(
            validate_task_status_consistency(payload, state),
            [
                "task supplement status conflicts with canonical workflow state: "
                "state status WAITING_HUMAN_DIFF_APPROVAL allows waiting_approval, got completed"
            ],
        )

    def test_unknown_transition_status_fails(self) -> None:
        self.assertEqual(validate_transition("unknown", "completed"), ["invalid current status: unknown"])
        self.assertEqual(validate_transition("planning", "unknown"), ["invalid next status: unknown"])


class TaskStateStatusIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_status_omits_task_supplement_when_missing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("task_chain: present (docs/ai/tasks/init-large)", status.stdout)
            self.assertNotIn("task_supplement:", status.stdout)

    def test_status_summarizes_valid_task_supplement(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            task_path = tmpdir / ".ai" / "tasks" / "init-large" / "task.json"
            task_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text(json.dumps(valid_task_payload(id="init-large"), indent=2) + "\n", encoding="utf-8")

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("task_supplement: present (.ai/tasks/init-large/task.json)", status.stdout)
            self.assertIn("task_supplement_id: init-large", status.stdout)
            self.assertIn("task_supplement_status: planning", status.stdout)
            self.assertIn("task_supplement_valid: yes", status.stdout)

    def test_status_accepts_supplement_that_matches_waiting_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)
            task_path = tmpdir / ".ai" / "tasks" / "init-large" / "task.json"
            task_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text(
                json.dumps(valid_task_payload(id="init-large", status="waiting_approval"), indent=2) + "\n",
                encoding="utf-8",
            )

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("status: WAITING_HUMAN_SPEC_APPROVAL", status.stdout)
            self.assertIn("task_supplement_status: waiting_approval", status.stdout)
            self.assertIn("task_supplement_valid: yes", status.stdout)

    def test_status_reports_invalid_task_supplement_without_failing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            task_path = tmpdir / ".ai" / "tasks" / "init-large" / "task.json"
            task_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text(json.dumps(valid_task_payload(id="other-task"), indent=2) + "\n", encoding="utf-8")

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("task_supplement_valid: no", status.stdout)
            self.assertIn("task id mismatch: state has init-large, task.json has other-task", status.stdout)

    def test_status_reports_conflicting_task_supplement_status(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)
            task_path = tmpdir / ".ai" / "tasks" / "init-large" / "task.json"
            task_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text(
                json.dumps(valid_task_payload(id="init-large", status="completed"), indent=2) + "\n",
                encoding="utf-8",
            )

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("status: WAITING_HUMAN_SPEC_APPROVAL", status.stdout)
            self.assertIn("task_supplement_status: completed", status.stdout)
            self.assertIn("task_supplement_valid: no", status.stdout)
            self.assertIn(
                "task supplement status conflicts with canonical workflow state: "
                "state status WAITING_HUMAN_SPEC_APPROVAL allows waiting_approval, got completed",
                status.stdout,
            )

    def test_small_and_medium_do_not_create_task_supplements_by_default(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertFalse((tmpdir / ".ai" / "tasks").exists())
            small_status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(small_status.returncode, 0, small_status.stderr)
            self.assertNotIn("task_supplement:", small_status.stdout)

        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium").returncode, 0)
            self.assertFalse((tmpdir / ".ai" / "tasks").exists())
            medium_status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(medium_status.returncode, 0, medium_status.stderr)
            self.assertNotIn("task_supplement:", medium_status.stdout)

    def test_loader_returns_absent_for_large_without_supplement(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            state = {"mode": "large", "task_id": "init-large"}

            result = load_active_task_supplement(tmpdir, state)

            self.assertIsNotNone(result)
            assert result is not None
            self.assertFalse(result.exists)
            self.assertEqual(result.errors, [])


if __name__ == "__main__":
    unittest.main()
