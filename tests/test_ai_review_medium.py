from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiReviewMediumIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_plan_review_succeeds_in_medium_without_spec(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan")
            self.assertEqual(result.returncode, 0, result.stderr)

            review_path = tmpdir / ".ai" / "reviews" / "plan-review.md"
            self.assertTrue(review_path.exists())
            self.assertIn("Plan Review", review_path.read_text(encoding="utf-8"))

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "medium")
            self.assertEqual(state["status"], "WAITING_HUMAN_PLAN_APPROVAL")
            self.assertEqual(state["current_gate"], "plan")

    def test_final_review_succeeds_in_medium_without_spec(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "final")
            self.assertEqual(result.returncode, 0, result.stderr)

            review_path = tmpdir / ".ai" / "reviews" / "final-review.md"
            self.assertTrue(review_path.exists())
            self.assertIn("Final Review", review_path.read_text(encoding="utf-8"))

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "medium")
            self.assertEqual(state["status"], "WAITING_HUMAN_FINAL_APPROVAL")
            self.assertEqual(state["current_gate"], "final")


if __name__ == "__main__":
    unittest.main()
