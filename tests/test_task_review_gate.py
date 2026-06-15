from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class TaskReviewGateIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_git(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=tmpdir, capture_output=True, text=True, check=False)

    def prepare_large_with_task_json(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
        task_path = tmpdir / ".ai" / "tasks" / "init-large" / "task.json"
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "id": "init-large",
                    "mode": "large",
                    "status": "planning",
                    "source": {
                        "epic": ".ai/epic.md",
                        "spec": ".ai/spec.md",
                        "plan": ".ai/implementation-plan.md",
                    },
                    "scope": [],
                    "created_at": "2026-06-15T00:00:00+08:00",
                    "updated_at": "2026-06-15T00:00:00+08:00",
                    "artifacts": {
                        "context_manifest": "context.jsonl",
                        "review": "review.md",
                        "rca": "rca.md",
                        "final": "final.md",
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_review_writes_waiting_task_gate_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large_with_task_json(tmpdir)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((tmpdir / ".ai" / "tasks" / "init-large" / "review.md").exists())
            approval = json.loads((tmpdir / ".ai" / "tasks" / "init-large" / "approval.json").read_text(encoding="utf-8"))
            self.assertEqual(approval["status"], "waiting")
            self.assertEqual(approval["review_type"], "spec")
            task = json.loads((tmpdir / ".ai" / "tasks" / "init-large" / "task.json").read_text(encoding="utf-8"))
            self.assertEqual(task["status"], "waiting_approval")

    def test_approve_updates_task_gate_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large_with_task_json(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec")

            self.assertEqual(result.returncode, 0, result.stderr)
            approval = json.loads((tmpdir / ".ai" / "tasks" / "init-large" / "approval.json").read_text(encoding="utf-8"))
            self.assertEqual(approval["status"], "approved")
            task = json.loads((tmpdir / ".ai" / "tasks" / "init-large" / "task.json").read_text(encoding="utf-8"))
            self.assertEqual(task["status"], "finalizing")

    def test_reject_updates_task_gate_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large_with_task_json(tmpdir)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-reject"), "spec")

            self.assertEqual(result.returncode, 0, result.stderr)
            approval = json.loads((tmpdir / ".ai" / "tasks" / "init-large" / "approval.json").read_text(encoding="utf-8"))
            self.assertEqual(approval["status"], "rejected")
            task = json.loads((tmpdir / ".ai" / "tasks" / "init-large" / "task.json").read_text(encoding="utf-8"))
            self.assertEqual(task["status"], "planning")


if __name__ == "__main__":
    unittest.main()
