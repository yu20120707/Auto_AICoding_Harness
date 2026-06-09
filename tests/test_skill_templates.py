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
SKILLS_ROOT = REPO_ROOT / "skills"

SKILL_NAMES = [
    "karpathy-guidelines",
    "task-router",
    "repo-onboarding-analysis",
    "source-driven-development",
    "planning-and-task-breakdown",
    "task-contract-and-leveling",
    "context-engineering",
    "systematic-debugging",
    "code-review-and-quality",
    "test-driven-development",
    "verification-before-completion",
    "skill-creator",
    "cpp-linux-system-engineering",
    "security-review",
    "performance-analysis",
]

SKILL_SOURCE_PATHS = [
    "skills/methodology/karpathy-guidelines/SKILL.md",
    "skills/methodology/task-router/SKILL.md",
    "skills/methodology/repo-onboarding-analysis/SKILL.md",
    "skills/methodology/source-driven-development/SKILL.md",
    "skills/methodology/planning-and-task-breakdown/SKILL.md",
    "skills/methodology/task-contract-and-leveling/SKILL.md",
    "skills/methodology/context-engineering/SKILL.md",
    "skills/methodology/systematic-debugging/SKILL.md",
    "skills/methodology/code-review-and-quality/SKILL.md",
    "skills/methodology/test-driven-development/SKILL.md",
    "skills/methodology/verification-before-completion/SKILL.md",
    "skills/methodology/skill-creator/SKILL.md",
    "skills/system/cpp-linux-system-engineering/SKILL.md",
    "skills/system/security-review/SKILL.md",
    "skills/system/performance-analysis/SKILL.md",
]

VERBATIM_UPSTREAM_SKILLS = {
    "skills/methodology/karpathy-guidelines/SKILL.md",
    "skills/methodology/source-driven-development/SKILL.md",
    "skills/methodology/planning-and-task-breakdown/SKILL.md",
    "skills/methodology/test-driven-development/SKILL.md",
}

VERBATIM_SKILL_MARKERS = {
    "skills/methodology/karpathy-guidelines/SKILL.md": "Surgical Changes",
    "skills/methodology/source-driven-development/SKILL.md": "Official Documentation",
    "skills/methodology/planning-and-task-breakdown/SKILL.md": "Acceptance criteria",
    "skills/methodology/test-driven-development/SKILL.md": "Red-Green-Refactor",
}


class SkillTemplatesIntegrationTest(unittest.TestCase):
    def run_cmd(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    def prepare_large(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

    def install_skills(self, dest: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return self.run_cmd(REPO_ROOT, str(REPO_ROOT / "bin" / "ai-install-skills"), "--dest", str(dest), *extra_args)

    def test_repository_skill_sources_exist(self) -> None:
        self.assertTrue((SKILLS_ROOT / "README.md").exists())
        for path in SKILL_SOURCE_PATHS:
            self.assertTrue((REPO_ROOT / path).exists(), path)

    def test_skill_sources_have_expected_sections_and_terms(self) -> None:
        for skill_path in SKILL_SOURCE_PATHS:
            content = (REPO_ROOT / skill_path).read_text(encoding="utf-8")
            self.assertIn("---", content, f"{skill_path} missing frontmatter")
            self.assertIn("name:", content, f"{skill_path} missing name frontmatter")
            self.assertIn("description:", content, f"{skill_path} missing description frontmatter")
            if skill_path in VERBATIM_UPSTREAM_SKILLS:
                self.assertNotIn("source:", content, f"{skill_path} should stay verbatim upstream")
                self.assertNotIn("upstream:", content, f"{skill_path} should stay verbatim upstream")
                self.assertNotIn("adaptation_notes:", content, f"{skill_path} should stay verbatim upstream")
                self.assertIn(VERBATIM_SKILL_MARKERS[skill_path], content, f"{skill_path} missing upstream section")
                continue

            self.assertIn("license:", content, f"{skill_path} missing license provenance")
            self.assertIn("source:", content, f"{skill_path} missing source provenance")
            self.assertIn("upstream:", content, f"{skill_path} missing upstream provenance")
            self.assertIn("adaptation_notes:", content, f"{skill_path} missing adaptation notes")
            self.assertGreaterEqual(len(content.splitlines()), 140, f"{skill_path} is still too condensed")
            for section in ["Purpose", "Use When", "Inputs", "Process", "Output", "Do Not"]:
                self.assertIn(section, content, f"{skill_path} missing {section}")

        self.assertIn("surgical", (SKILLS_ROOT / "methodology/karpathy-guidelines/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("complex", (SKILLS_ROOT / "methodology/task-router/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("repo onboarding", (SKILLS_ROOT / "methodology/repo-onboarding-analysis/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("official documentation", (SKILLS_ROOT / "methodology/source-driven-development/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("acceptance criteria", (SKILLS_ROOT / "methodology/planning-and-task-breakdown/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("rollback", (SKILLS_ROOT / "methodology/task-contract-and-leveling/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("call chains", (SKILLS_ROOT / "methodology/context-engineering/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("root cause", (SKILLS_ROOT / "methodology/systematic-debugging/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("red-green-refactor", (SKILLS_ROOT / "methodology/test-driven-development/SKILL.md").read_text(encoding="utf-8").lower())
        verification_text = (SKILLS_ROOT / "methodology/verification-before-completion/SKILL.md").read_text(encoding="utf-8").lower()
        self.assertTrue("tests passed" in verification_text or "not run" in verification_text)
        self.assertIn("review finding", (SKILLS_ROOT / "methodology/code-review-and-quality/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("installation behavior", (SKILLS_ROOT / "methodology/skill-creator/SKILL.md").read_text(encoding="utf-8").lower())
        system_text = (SKILLS_ROOT / "system/cpp-linux-system-engineering/SKILL.md").read_text(encoding="utf-8").lower()
        for term in ["raii", "strace", "eagain", "atomic", "api/abi", "cmake"]:
            self.assertIn(term, system_text)
        self.assertIn("secret", (SKILLS_ROOT / "system/security-review/SKILL.md").read_text(encoding="utf-8").lower())
        self.assertIn("baseline", (SKILLS_ROOT / "system/performance-analysis/SKILL.md").read_text(encoding="utf-8").lower())

    def test_large_mode_does_not_generate_project_skill_templates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            self.assertFalse((tmpdir / ".agents" / "skills").exists())

    def test_ai_install_skills_installs_all_global_skills(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-skills-") as tmp:
            dest = Path(tmp) / "codex-skills"

            result = self.install_skills(dest)
            self.assertEqual(result.returncode, 0, result.stderr)

            for skill_name in SKILL_NAMES:
                self.assertTrue((dest / skill_name / "SKILL.md").exists(), skill_name)
                self.assertIn(f"CREATED {skill_name}", result.stdout)

    def test_default_does_not_overwrite_global_skill(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-skills-") as tmp:
            dest = Path(tmp) / "codex-skills"
            self.assertEqual(self.install_skills(dest).returncode, 0)
            skill_path = dest / "cpp-linux-system-engineering" / "SKILL.md"
            skill_path.write_text("user modified\n", encoding="utf-8")

            result = self.install_skills(dest)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIPPED cpp-linux-system-engineering", result.stdout)
            self.assertEqual(skill_path.read_text(encoding="utf-8"), "user modified\n")

    def test_force_backs_up_and_overwrites_global_skill(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-skills-") as tmp:
            dest = Path(tmp) / "codex-skills"
            self.assertEqual(self.install_skills(dest).returncode, 0)
            skill_path = dest / "security-review" / "SKILL.md"
            skill_path.write_text("user modified\n", encoding="utf-8")

            result = self.install_skills(dest, "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN security-review", result.stdout)

            backups = list((Path(tmp) / "skill-backups").rglob("security-review/SKILL.md"))
            self.assertTrue(backups, "expected global skill backup")
            self.assertTrue(
                any("user modified" in backup.read_text(encoding="utf-8") for backup in backups),
                "expected overwritten global skill content in backup",
            )

    def test_skill_manifest_and_role_routing_are_documented(self) -> None:
        readme = (SKILLS_ROOT / "README.md").read_text(encoding="utf-8")

        for skill_name in SKILL_NAMES:
            self.assertIn(skill_name, readme)

        for role in ["planner", "explorer", "implementer", "reviewer", "evaluator"]:
            self.assertIn(f"`{role}`", readme)
        self.assertIn("Role To Skill Routing", readme)
        self.assertIn("global skill installation", readme)
        self.assertIn("do not bypass human gates", readme)
        self.assertIn("fuller workflow skills", readme)

    def test_skills_do_not_claim_third_party_install_or_execution_logic(self) -> None:
        combined = "\n".join((REPO_ROOT / path).read_text(encoding="utf-8").lower() for path in ["skills/README.md", *SKILL_SOURCE_PATHS])

        self.assertIn("do not execute anything by themselves", combined)
        self.assertIn("not installed implicitly by `git clone`", combined)
        for forbidden in [
            "curl | bash",
            "curl | sh",
            "pip install",
            "npm install",
            "plugin marketplace add",
        ]:
            self.assertNotIn(forbidden, combined)

    def test_removed_granular_skills_are_not_present(self) -> None:
        for removed in [
            "skills/methodology/design-before-code/SKILL.md",
            "skills/methodology/incremental-implementation/SKILL.md",
            "skills/system/network-programming/SKILL.md",
            "skills/system/concurrency-review/SKILL.md",
            "skills/system/cpp-api-abi-review/SKILL.md",
        ]:
            self.assertFalse((REPO_ROOT / removed).exists(), removed)

    def test_docs_are_synced_for_global_skills(self) -> None:
        combined = (
            README_PATH.read_text(encoding="utf-8")
            + "\n"
            + CAPABILITIES_PATH.read_text(encoding="utf-8")
            + "\n"
            + TARGET_STRUCTURE_PATH.read_text(encoding="utf-8")
        )
        self.assertIn("v1.6-subagent-packets", combined)
        self.assertIn("portable skill", combined)
        self.assertIn("ai-install-skills", combined)
        self.assertIn("subagent execution", combined)
        self.assertIn("skills/", combined)
        self.assertIn("karpathy-guidelines/SKILL.md", combined)
        self.assertIn("task-router/SKILL.md", combined)
        self.assertIn("repo-onboarding-analysis/SKILL.md", combined)
        self.assertIn("source-driven-development/SKILL.md", combined)
        self.assertIn("planning-and-task-breakdown/SKILL.md", combined)
        self.assertIn("test-driven-development/SKILL.md", combined)
        self.assertIn("skill-creator/SKILL.md", combined)
        self.assertIn("task-contract-and-leveling/SKILL.md", combined)
        self.assertIn("cpp-linux-system-engineering/SKILL.md", combined)
        self.assertIn("provenance", combined)
        self.assertIn("epic.md", combined)


if __name__ == "__main__":
    unittest.main()
