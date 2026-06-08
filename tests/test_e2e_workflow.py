from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class EndToEndWorkflowTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_git(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_main_workflow_reaches_done(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)

            self.assertEqual(self.run_git(tmpdir, "init").returncode, 0)

            status0 = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status0.returncode, 0, status0.stderr)
            self.assertIn("status: UNINITIALIZED", status0.stdout)

            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "spec").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "spec").returncode, 0)

            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "plan").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "plan").returncode, 0)

            self.assertEqual(self.run_git(tmpdir, "add", ".").returncode, 0)
            agents = tmpdir / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8") + "\nlocal e2e change\n", encoding="utf-8")

            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "diff").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "diff").returncode, 0)

            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-context-pack")).returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-handoff")).returncode, 0)

            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-review"), "final").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-approve"), "final").returncode, 0)

            status1 = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status1.returncode, 0, status1.stderr)
            self.assertIn("status: DONE", status1.stdout)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "DONE")
            self.assertIsNone(state["current_gate"])
            for gate in ["spec", "plan", "diff", "final"]:
                self.assertIn(gate, state.get("approved_gates", []))

            for path in [
                ".ai/reviews/spec-review.md",
                ".ai/reviews/plan-review.md",
                ".ai/reviews/diff-review.md",
                ".ai/reviews/final-review.md",
                ".ai/approvals/spec-approval.md",
                ".ai/approvals/plan-approval.md",
                ".ai/approvals/diff-approval.md",
                ".ai/approvals/final-approval.md",
                ".ai/context-pack.md",
                ".ai/handoff.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
