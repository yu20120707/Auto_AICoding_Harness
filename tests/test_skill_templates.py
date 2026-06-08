from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
README_PATH = REPO_ROOT / "README.md"
CAPABILITIES_PATH = REPO_ROOT / "docs" / "design" / "current-capabilities.md"
TARGET_STRUCTURE_PATH = REPO_ROOT / "docs" / "usage" / "generated-target-structure.md"


class SkillTemplatesIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def prepare_large(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

    def test_large_mode_generates_skill_templates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            for path in [
                ".agents/skills/README.md",
                ".agents/skills/methodology/design-before-code/SKILL.md",
                ".agents/skills/methodology/systematic-debugging/SKILL.md",
                ".agents/skills/methodology/verification-before-completion/SKILL.md",
                ".agents/skills/methodology/human-in-loop-development/SKILL.md",
                ".agents/skills/system/cpp-system-dev/SKILL.md",
                ".agents/skills/system/linux-debug/SKILL.md",
                ".agents/skills/system/network-programming/SKILL.md",
                ".agents/skills/system/concurrency-review/SKILL.md",
                ".agents/skills/system/performance-analysis/SKILL.md",
                ".agents/skills/system/cpp-api-abi-review/SKILL.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_skill_templates_have_expected_sections_and_terms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            skill_paths = [
                ".agents/skills/methodology/design-before-code/SKILL.md",
                ".agents/skills/methodology/systematic-debugging/SKILL.md",
                ".agents/skills/methodology/verification-before-completion/SKILL.md",
                ".agents/skills/methodology/human-in-loop-development/SKILL.md",
                ".agents/skills/system/cpp-system-dev/SKILL.md",
                ".agents/skills/system/linux-debug/SKILL.md",
                ".agents/skills/system/network-programming/SKILL.md",
                ".agents/skills/system/concurrency-review/SKILL.md",
                ".agents/skills/system/performance-analysis/SKILL.md",
                ".agents/skills/system/cpp-api-abi-review/SKILL.md",
            ]
            for skill_path in skill_paths:
                content = (tmpdir / skill_path).read_text(encoding="utf-8")
                for section in ["Purpose", "Use When", "Inputs", "Process", "Output", "Do Not"]:
                    self.assertIn(section, content, f"{skill_path} missing {section}")

            self.assertIn("spec", (tmpdir / ".agents/skills/methodology/design-before-code/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("root cause", (tmpdir / ".agents/skills/methodology/systematic-debugging/SKILL.md").read_text(encoding="utf-8").lower())
            verification_text = (tmpdir / ".agents/skills/methodology/verification-before-completion/SKILL.md").read_text(encoding="utf-8").lower()
            self.assertTrue("tests passed" in verification_text or "not run" in verification_text)
            self.assertIn("waiting_human", (tmpdir / ".agents/skills/methodology/human-in-loop-development/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("raii", (tmpdir / ".agents/skills/system/cpp-system-dev/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("strace", (tmpdir / ".agents/skills/system/linux-debug/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("eagain", (tmpdir / ".agents/skills/system/network-programming/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("atomic", (tmpdir / ".agents/skills/system/concurrency-review/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("baseline", (tmpdir / ".agents/skills/system/performance-analysis/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("abi", (tmpdir / ".agents/skills/system/cpp-api-abi-review/SKILL.md").read_text(encoding="utf-8").lower())

    def test_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            skill_path = tmpdir / ".agents" / "skills" / "system" / "cpp-system-dev" / "SKILL.md"
            skill_path.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ALREADY_LARGE", result.stdout)
            self.assertIn("SKIPPED .agents/skills/system/cpp-system-dev/SKILL.md", result.stdout)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), "user modified\n")

    def test_force_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            skill_path = tmpdir / ".agents" / "skills" / "system" / "network-programming" / "SKILL.md"
            skill_path.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .agents/skills/system/network-programming/SKILL.md", result.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("SKILL.md"))
            self.assertTrue(backups, "expected skill template backup")
            self.assertTrue(
                any("user modified" in backup.read_text(encoding="utf-8") for backup in backups),
                "expected overwritten skill content in backup",
            )

    def test_docs_are_synced_for_phase10_skills(self) -> None:
        combined = (
            README_PATH.read_text(encoding="utf-8")
            + "\n"
            + CAPABILITIES_PATH.read_text(encoding="utf-8")
            + "\n"
            + TARGET_STRUCTURE_PATH.read_text(encoding="utf-8")
        )
        self.assertIn("v1.0-phase10", combined)
        self.assertIn("skills templates", combined)
        self.assertIn("skills installation", combined)
        self.assertIn("subagent execution", combined)
        self.assertIn(".agents/skills/", combined)


if __name__ == "__main__":
    unittest.main()
