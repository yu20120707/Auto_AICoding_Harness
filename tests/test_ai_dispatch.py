from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiDispatchIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_uninitialized_dispatch_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(
                tmpdir,
                str(REPO_ROOT / "bin" / "ai-dispatch"),
                "planner",
                "--scope",
                "docs/design/*",
                "--objective",
                "plan bounded hardening",
                "--expected-output",
                "plan + risks",
                "--result-location",
                ".ai/run-trace.md",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(".ai/state.json", result.stderr)

    def test_small_mode_dispatch_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)

            result = self.run_cmd(
                tmpdir,
                str(REPO_ROOT / "bin" / "ai-dispatch"),
                "planner",
                "--scope",
                "docs/design/*",
                "--objective",
                "plan bounded hardening",
                "--expected-output",
                "plan + risks",
                "--result-location",
                ".ai/run-trace.md",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("large mode", result.stderr)

    def test_large_mode_dispatch_appends_packet_skills(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
            self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

            result = self.run_cmd(
                tmpdir,
                str(REPO_ROOT / "bin" / "ai-dispatch"),
                "planner",
                "--scope",
                "docs/design/*",
                "--objective",
                "plan bounded hardening",
                "--expected-output",
                "plan + risks",
                "--result-location",
                ".ai/run-trace.md",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("APPENDED .ai/run-trace.md (dispatch: planner)", result.stdout)

            content = (tmpdir / ".ai" / "run-trace.md").read_text(encoding="utf-8")
            self.assertIn("## Dispatch ", content)
            self.assertIn("- role: planner", content)
            self.assertIn("- scope: docs/design/*", content)
            self.assertIn("methodology/task-contract-and-leveling", content)
            self.assertIn("methodology/source-driven-development", content)
            self.assertIn("- objective: plan bounded hardening", content)
            self.assertIn("- expected_output: plan + risks", content)
            self.assertIn("- result_location: .ai/run-trace.md", content)

    def test_missing_required_arguments_returns_argparse_error(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-dispatch"), "planner")

            self.assertEqual(result.returncode, 2)
            self.assertIn("--scope", result.stderr)


if __name__ == "__main__":
    unittest.main()
