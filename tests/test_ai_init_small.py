from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class AiInitSmallIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_ai_status_uninitialized(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status: UNINITIALIZED", result.stdout)
            self.assertEqual(list(tmpdir.iterdir()), [])

    def test_ai_init_small_creates_base_files_and_state(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("CREATED AGENTS.md", result.stdout)

            expected_paths = [
                "AGENTS.md",
                "CLAUDE.md",
                ".github/copilot-instructions.md",
                "docs/ai",
                ".ai/.gitkeep",
                ".ai/templates",
                ".ai/state.json",
                "scripts/ai_build.sh",
                "scripts/ai_test.sh",
                "scripts/ai_check.sh",
            ]
            for path in expected_paths:
                self.assertTrue((tmpdir / path).exists(), path)

            state = json.loads((tmpdir / ".ai" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {
                    "schema_version": state["schema_version"],
                    "mode": state["mode"],
                    "profile": state["profile"],
                    "status": state["status"],
                    "current_gate": state["current_gate"],
                    "approved_gates": state["approved_gates"],
                    "created_by": state["created_by"],
                },
                {
                    "schema_version": 1,
                    "mode": "small",
                    "profile": "cpp-linux-backend-system",
                    "status": "INIT",
                    "current_gate": None,
                    "approved_gates": [],
                    "created_by": "Auto_AICoding_Harness",
                },
            )

    def test_second_ai_init_small_skips_existing_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            first = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(first.returncode, 0, first.stderr)

            state_before = (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8")
            second = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("SKIPPED AGENTS.md", second.stdout)
            state_after = (tmpdir / ".ai" / "state.json").read_text(encoding="utf-8")
            self.assertEqual(state_before, state_after)

    def test_force_init_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            first = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(first.returncode, 0, first.stderr)

            agents_path = tmpdir / "AGENTS.md"
            agents_path.write_text("user modified\n", encoding="utf-8")

            forced = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small", "--force")
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertIn("OVERWRITTEN AGENTS.md", forced.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("AGENTS.md"))
            self.assertTrue(backups, "expected AGENTS.md backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))
            self.assertIn("Project Type", agents_path.read_text(encoding="utf-8"))

    def test_generated_agent_instruction_files_are_safe_write_managed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            first = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(first.returncode, 0, first.stderr)

            copilot_path = tmpdir / ".github" / "copilot-instructions.md"
            copilot_path.write_text("user modified\n", encoding="utf-8")

            second = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("SKIPPED .github/copilot-instructions.md", second.stdout)
            self.assertEqual(copilot_path.read_text(encoding="utf-8"), "user modified\n")

            forced = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small", "--force")
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertIn("OVERWRITTEN .github/copilot-instructions.md", forced.stdout)
            backups = list((tmpdir / ".ai" / "backups").rglob("copilot-instructions.md"))
            self.assertTrue(backups, "expected Copilot instructions backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_ai_status_after_init(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")
            self.assertEqual(init.returncode, 0, init.stderr)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"))
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertIn("initialized: yes", status.stdout)
            self.assertIn("mode: small", status.stdout)
            self.assertIn("profile: cpp-linux-backend-system", status.stdout)
            self.assertIn("status: INIT", status.stdout)
            self.assertIn("AGENTS.md: yes", status.stdout)
            self.assertIn(".ai/state.json: yes", status.stdout)
            self.assertIn("docs/ai/: yes", status.stdout)
            self.assertIn("scripts/ai_check.sh: yes", status.stdout)

    def test_invalid_arguments_return_two(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            init = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "large")
            self.assertEqual(init.returncode, 2)

            status = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-status"), "--bad-flag")
            self.assertEqual(status.returncode, 2)


if __name__ == "__main__":
    unittest.main()
