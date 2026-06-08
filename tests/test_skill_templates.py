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

SKILL_PATHS = [
    ".agents/skills/methodology/karpathy-guidelines/SKILL.md",
    ".agents/skills/methodology/task-contract-and-leveling/SKILL.md",
    ".agents/skills/methodology/context-engineering/SKILL.md",
    ".agents/skills/methodology/systematic-debugging/SKILL.md",
    ".agents/skills/methodology/code-review-and-quality/SKILL.md",
    ".agents/skills/methodology/verification-before-completion/SKILL.md",
    ".agents/skills/methodology/skill-creator/SKILL.md",
    ".agents/skills/system/cpp-linux-system-engineering/SKILL.md",
    ".agents/skills/system/security-review/SKILL.md",
    ".agents/skills/system/performance-analysis/SKILL.md",
]


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
                *SKILL_PATHS,
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_skill_templates_have_expected_sections_and_terms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            for skill_path in SKILL_PATHS:
                content = (tmpdir / skill_path).read_text(encoding="utf-8")
                self.assertIn("---", content, f"{skill_path} missing frontmatter")
                self.assertIn("name:", content, f"{skill_path} missing name frontmatter")
                self.assertIn("description:", content, f"{skill_path} missing description frontmatter")
                self.assertIn("source:", content, f"{skill_path} missing source provenance")
                self.assertIn("upstream:", content, f"{skill_path} missing upstream provenance")
                self.assertIn("license:", content, f"{skill_path} missing license provenance")
                self.assertIn("adaptation_notes:", content, f"{skill_path} missing adaptation notes")
                for section in ["Purpose", "Use When", "Inputs", "Process", "Output", "Do Not"]:
                    self.assertIn(section, content, f"{skill_path} missing {section}")

            self.assertIn("surgical", (tmpdir / ".agents/skills/methodology/karpathy-guidelines/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("rollback", (tmpdir / ".agents/skills/methodology/task-contract-and-leveling/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("call chains", (tmpdir / ".agents/skills/methodology/context-engineering/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("root cause", (tmpdir / ".agents/skills/methodology/systematic-debugging/SKILL.md").read_text(encoding="utf-8").lower())
            verification_text = (tmpdir / ".agents/skills/methodology/verification-before-completion/SKILL.md").read_text(encoding="utf-8").lower()
            self.assertTrue("tests passed" in verification_text or "not run" in verification_text)
            self.assertIn("review finding", (tmpdir / ".agents/skills/methodology/code-review-and-quality/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("adaptation_notes", (tmpdir / ".agents/skills/methodology/skill-creator/SKILL.md").read_text(encoding="utf-8").lower())
            system_text = (tmpdir / ".agents/skills/system/cpp-linux-system-engineering/SKILL.md").read_text(encoding="utf-8").lower()
            for term in ["raii", "strace", "eagain", "atomic", "api/abi", "cmake"]:
                self.assertIn(term, system_text)
            self.assertIn("secret", (tmpdir / ".agents/skills/system/security-review/SKILL.md").read_text(encoding="utf-8").lower())
            self.assertIn("baseline", (tmpdir / ".agents/skills/system/performance-analysis/SKILL.md").read_text(encoding="utf-8").lower())

    def test_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            skill_path = tmpdir / ".agents" / "skills" / "system" / "cpp-linux-system-engineering" / "SKILL.md"
            skill_path.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ALREADY_LARGE", result.stdout)
            self.assertIn("SKIPPED .agents/skills/system/cpp-linux-system-engineering/SKILL.md", result.stdout)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), "user modified\n")

    def test_force_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            skill_path = tmpdir / ".agents" / "skills" / "system" / "security-review" / "SKILL.md"
            skill_path.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .agents/skills/system/security-review/SKILL.md", result.stdout)

            backups = list((tmpdir / ".ai" / "backups").rglob("SKILL.md"))
            self.assertTrue(backups, "expected skill template backup")
            self.assertTrue(
                any("user modified" in backup.read_text(encoding="utf-8") for backup in backups),
                "expected overwritten skill content in backup",
            )

    def test_skill_manifest_and_role_routing_are_generated(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            readme = (tmpdir / ".agents" / "skills" / "README.md").read_text(encoding="utf-8")

            for skill_path in SKILL_PATHS:
                skill_name = Path(skill_path).parent.name
                self.assertIn(skill_name, readme)

            for role in ["planner", "explorer", "implementer", "reviewer", "evaluator"]:
                self.assertIn(f"`{role}`", readme)
            self.assertIn("Role To Skill Routing", readme)
            self.assertIn("do not make skills mandatory runtime dependencies", readme)
            self.assertIn("do not bypass human gates", readme)

    def test_skills_do_not_claim_install_or_execution_logic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            combined = "\n".join((tmpdir / path).read_text(encoding="utf-8").lower() for path in [".agents/skills/README.md", *SKILL_PATHS])

            self.assertIn("do not execute anything by themselves", combined)
            self.assertIn("not automatically installed globally", combined)
            for forbidden in [
                "curl | bash",
                "curl | sh",
                "pip install",
                "npm install",
                "plugin marketplace add",
                "install now",
            ]:
                self.assertNotIn(forbidden, combined)

    def test_removed_granular_skills_are_not_generated(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            for removed in [
                ".agents/skills/methodology/design-before-code/SKILL.md",
                ".agents/skills/methodology/incremental-implementation/SKILL.md",
                ".agents/skills/system/network-programming/SKILL.md",
                ".agents/skills/system/concurrency-review/SKILL.md",
                ".agents/skills/system/cpp-api-abi-review/SKILL.md",
            ]:
                self.assertFalse((tmpdir / removed).exists(), removed)

    def test_docs_are_synced_for_skill_consolidation(self) -> None:
        combined = (
            README_PATH.read_text(encoding="utf-8")
            + "\n"
            + CAPABILITIES_PATH.read_text(encoding="utf-8")
            + "\n"
            + TARGET_STRUCTURE_PATH.read_text(encoding="utf-8")
        )
        self.assertIn("v1.3-skill-creator-zh-readme", combined)
        self.assertIn("skills templates", combined)
        self.assertIn("skills installation", combined)
        self.assertIn("subagent execution", combined)
        self.assertIn(".agents/skills/", combined)
        self.assertIn("karpathy-guidelines/SKILL.md", combined)
        self.assertIn("skill-creator/SKILL.md", combined)
        self.assertIn("task-contract-and-leveling/SKILL.md", combined)
        self.assertIn("cpp-linux-system-engineering/SKILL.md", combined)
        self.assertIn("provenance", combined)
        self.assertIn("epic.md", combined)


if __name__ == "__main__":
    unittest.main()
