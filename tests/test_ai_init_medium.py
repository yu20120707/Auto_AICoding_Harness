from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiInitMediumIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_ai_init_medium_creates_medium_files_and_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium")

            self.assertEqual(result.returncode, 0, result.stderr)
            for path in [
                "AGENTS.md",
                ".ai/state.json",
                ".ai/implementation-plan.md",
                ".ai/run-trace.md",
                ".ai/verification.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["mode"], "medium")
            self.assertEqual(state["task_id"], "init-medium")

    def test_ai_status_after_medium_init(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium").returncode, 0)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("mode: medium", status.stdout)
            self.assertIn("medium files: present", status.stdout)
            self.assertIn("Fill .ai/implementation-plan.md", status.stdout)


if __name__ == "__main__":
    unittest.main()
