from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiStateIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_ai_state_uninitialized_outputs_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-state"))

            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads(result.stdout)
            self.assertFalse(state["initialized"])
            self.assertEqual(state["status"], "UNINITIALIZED")
            self.assertIsNone(state["mode"])

    def test_ai_state_initialized_outputs_state_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(init.returncode, 0, init.stderr)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-state"))

            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads(result.stdout)
            self.assertTrue(state["initialized"])
            self.assertEqual(state["mode"], "small")
            self.assertEqual(state["status"], "INIT")
            self.assertEqual(state["profile"], "cpp-linux-backend-system")

    def test_ai_state_invalid_argument_returns_two(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-state"), "--bad-flag")
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
