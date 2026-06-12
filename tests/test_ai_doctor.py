from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiDoctorIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_doctor_fails_when_state_missing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(".ai/state.json missing", result.stdout)

    def test_doctor_detects_mode_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            (tmpdir / ".ai" / "epic.md").write_text("# stray large file\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("mode mismatch detected", result.stdout)

    def test_doctor_detects_stray_medium_files_in_small_mode(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            for path in [
                ".ai/implementation-plan.md",
                ".ai/run-trace.md",
                ".ai/verification.md",
            ]:
                (tmpdir / path).write_text("stray\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("state is small but medium-mode files are present", result.stdout)

    def test_doctor_json_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn("checks", payload)
            self.assertIn("next_action", payload)
            self.assertFalse(payload["has_failures"])

    def test_doctor_accepts_medium_mode_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "medium").returncode, 0)

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"))
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("medium-mode files present", result.stdout)

    def test_doctor_detects_missing_large_scaffold(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            (tmpdir / ".ai" / "spec.md").unlink()

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("large mode state exists but large-mode files are missing", result.stdout)

    def test_doctor_detects_missing_large_task_chain_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)
            (tmpdir / "docs" / "ai" / "tasks" / "init-large" / "02-tech-design.md").unlink()

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-doctor"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("large task chain exists but required task evidence files are missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
